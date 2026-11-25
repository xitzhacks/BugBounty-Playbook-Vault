---
name: disclosed-report-corpus
description: Build and refresh a queryable disclosed-report corpus (HackerOne write-ups) and wire it into the playbook vault as a dataset layer. Use when the user says "copy all the reports into the vault", points at hexbrainai.com / a hackerone-reports repo / an h1 mirror, asks to harvest disclosed reports, add case stock to playbooks, index the vault's own markdown into the DB, debrand/rename the dataset dir, or rebuild by-class / by-category report views. Covers the public endpoints, the two-stage harvest (metadata first, write-ups second), rate-limit behaviour, minimal-rename discipline, class routing into playbook dirs, idempotent case-stock injection into READMEs, the documents/documents_fts index, and the audit gates that must pass before reporting done.
---

# Disclosed-report corpus → playbook vault

The vault (`/home/user/projects/FAN/Vault`) has a **teaching layer** (playbooks per category) and
needs a **dataset layer**: every disclosed report, queryable, routed into the playbook dirs.
This skill builds and refreshes that layer. Scripts are in `scripts/`.

## Sources (all public, no key)

| Source | What you get | Notes |
|---|---|---|
| `https://hexbrainai.com/api/reports?limit=100&offset=N` | list: id, title, program, severity, weakness, bounty, votes, reporter, disclosed_at, substate + `total` | max limit **100**, 600 req/min per IP. 15,244 rows = 153 pages ≈ 90s |
| `https://hackerone.com/reports/<id>.json` | the full write-up (`vulnerability_information`), summaries, asset, CVEs, team | unauthenticated, the same door hexbrain itself uses |
| `https://raw.githubusercontent.com/reddelexc/hackerone-reports/master/data.csv` | id, title, program, upvotes, bounty, vuln_type | what `pnpm ingest:import` uses; weaker than the API |
| `hexbrainai.com/api/v1/<tool>`, `/api/mcp` | same data as MCP/REST tools | **401 without an API key** — do not bother |

`github.com/hackerspider1/hexbrainai.com` is the reference implementation of our exact concept
(Next.js 16, node:sqlite). Its DB (`data/hexbrain.db`) is **gitignored** — the repo ships the
pipeline, never the reports. Read `src/lib/taxonomy.ts` for their class regexes and their
title-based weakness guesser; steal those rules rather than reinventing them.

## Two-stage harvest — always in this order

1. **Metadata first** (`scripts/harvest_meta.py`) → `hexbrain_reports.jsonl` + `.sqlite` (table `reports`).
   Takes ~2 minutes for 15k. Do this first so the vault views exist and are useful immediately.
   Paginate `offset += 100`, dedupe by id, take `total` from page 1, stop at `offset >= total`.
2. **Write-ups second** (`scripts/harvest_bodies.py`) → table `bodies` (summary, body, asset,
   cve_ids, http_status). Resumable: it only queues ids **not already in `bodies`**, so a kill/restart
   costs nothing. Store `http_status` for failures too — 404s must be remembered, or every rerun
   re-fetches 3,000 dead ids.

Bodies for 15k take 1.5–2h. Run it with `terminal(background=true, notify_on_complete=true)` and do
the export work in parallel — never block the turn on it.

## Rate-limit facts (measured, not guessed)

- Plain `curl` to a report JSON: 0.4–0.6 s, no throttle.
- 8 concurrent → ~40% **429**. 4 workers @0.35 s delay ≈ **2.5 req/s sustained**, clean.
- A 429 must honour `Retry-After` and sleep ~10–15 s, then retry. The first version slept 45–65 s
  and collapsed throughput to 0.5 req/s — that sleep is the bug, not the limit.
- ~19% of ids in any public list are **404/delisted**. Expected. Record, never quote, never retry.

## Long-haul crawl discipline (the operator WILL ask for 15-minute progress)

A 15k-row body crawl runs 1–2 h with nothing to show for it. The operator's standing instruction is
*"give me progress every 15 minutes so it runs without any issue, must complete, don't get stuck,
don't hallucinate."* Treat that as the default contract for any harvest longer than ~20 minutes:

1. **Watchdog, not hope** — launch `scripts/watchdog.sh` in the background. Every 15 min it appends to
   `watchdog.log`: timestamp, whether the crawler PID is alive, and `bodies_ok / bodies_404 /
   body_bytes / remaining` read straight from SQLite. If the crawler died with work left, it restarts it
   (the crawler is resumable, so a restart is free). Then you report from that log, not from memory.
2. **Report only DB-derived numbers**, in this shape: `metadata rows / write-ups stored / delisted 404 /
   remaining / rate / ETA / crawler status`. If a number isn't in the DB or the log, don't state it.
3. **Re-read the state before every report** — `SELECT COUNT(*) FROM bodies` and the split query. Never
   carry a stale count forward; the crawl rate swings 1.9–6.5 req/s on HackerOne throttling, so an ETA
   from ten minutes ago is wrong.
4. **Say "no restarts needed" or "watchdog restarted it N times"** — that's the honesty marker that the
   pipeline is actually being watched rather than narrated.
5. Stop the watchdog (`pkill -f watchdog.sh`) once `remaining = 0`, then run the export. Leaving it alive
   keeps appending snapshots and can restart a crawler you deliberately ended.

## Routed into the vault

Output is `Vault/_VAULT/` (see `scripts/export_to_vault.py`):

```
README.md                     counts, provenance, SQL recipes, per-class + per-dir tables,
                              plus a retrieval-state table (full / summary-only / 404 / other)
all-reports.csv               every row incl. class + routed vault_category + has_body
reports.sqlite                VACUUM INTO copy — reports + bodies (+ documents, see below)
by-class/NN_<CLASS>.md        all rows of one class, richest first
by-vault-category/<dir>.md    same rows routed into the playbook dirs
scripts/extract_report.py <id>  one write-up as markdown
scripts/refresh.sh            harvester → export → doc index
```

> The dataset dir was renamed `_HEXBRAIN` → `_VAULT` (2026-11-16) at the operator's instruction:
> the corpus is his project, the upstream product name must not appear in the vault. Scripts and
> generated files carry only `_VAULT` / `reports.sqlite`.

Routing rule order matters: **refined dirs first, broad class second**. `subdomain takeover` →
`13_Subdomain-Takeover`, `request smuggling|crlf` → `14_HTTP-Request-Smuggling`,
`cache poison|deception` → `15_`, `brute force|rate limit` → `20_`, `graphql` → `22_`,
`ldap|xpath` → `23_`, `host header|reset poison` → `24_`, `prototype pollution` → `25_`,
`smart contract` → `26_`, `llm|prompt injection` → `27_`, `android|ios` → `28_`,
`clickjacking` → `29_`, `race condition` → `Race-Conditions/`, `xxe|xml external` → `XXE/`.
Otherwise fall back to the hexbrain class → dir table (XSS→XSS, INFO→16_, ACL→17_, AUTH→
Authentication-Session, CONF→18_, MEM→30_, RCE→RCE, DOS→21_, CSRF→CSRF, LOGIC→12_, CRYPTO→19_,
INJ→XXE, IDOR→IDOR, REDIR→Open-Redirect, SQLI→SQLi, SSRF→SSRF, TRAV→File-Upload).

Then `scripts/inject_case_stock.py` writes a fenced `<!-- CASESTOCK-LINK -->` block into
**every** playbook `README.md` (row count, paid count, bounty total, top-5 paid cases, query
one-liners). Fenced = idempotent; re-run it after every refresh instead of hand-editing 30 files.

Also add a `CASE-STOCK DATASET LAYER` section to `Vault/00_MASTER_CATEGORY_LIST.md` — the vault's
entry point must point at the dataset, or a future session never finds it.

## Index our own documents into the same DB

The corpus DB is also the vault's **document store**, not just a report mirror. `scripts/ingest_vault_docs.py`
walks every `.md` under `Vault/` and upserts into `documents` (path, dir, name, title, type, category,
cwe, bytes, lines, sha256, ingested_at, **full text**) plus an FTS5 table `documents_fts` over
title/name/path/dir/text, driven by triggers.

- Upsert **by path**; delete rows whose file vanished (report the count) so the index never drifts.
- Skip hidden dirs (`.commandcode`, `.git`) — they are not playbooks and inflate the count.
- After a rename wave, re-run it so stored `path` values match the new directory names.
- Cheap proof of integrity the operator asks for ("is it really in the DB?"): re-read every file,
  compare `sha256(raw)` to the stored hash and `len(raw)` to `bytes`, then show that
  `documents.text == open(path).read()` for one row. Print "N identical, 0 problems".
- Parity gate: `COUNT(*)=documents` must equal the number of `.md` files on disk.

## Verification gates (run `scripts/audit_vault.py` before saying "done")

41 checks, all read-only, all comparing **the DB against the DB, the CSV, the md views and the
README's own claims** — because the README is a claim, not evidence:

| Gate | What it asserts |
|---|---|
| location | dataset dir sits inside the vault, all expected files present and non-zero |
| sqlite | `PRAGMA integrity_check`=ok, no duplicate ids, no orphan bodies in either direction |
| reconcile | full + summary-only + 404 + other **== total** (prints the four numbers) |
| csv↔db | row count, paid count, bounty sum, `has_body=1` and id-set all identical |
| views | class files sum to total, category files sum to total, no empty view file |
| README | every frontmatter number and the availability table match the DB |
| wiring | every playbook README carries the case-stock fence; master list references the dataset |
| extract | one random full write-up extracts >2 KB; one summary-only row prints "body not public" |
| documents | documents == `.md` on disk, has text + sha256, no path escapes, FTS returns hits |

Exit is a pass/fail count. Report it verbatim ("41 passed, 0 failed"); never "should be fine".

## Rename / debrand requests — mechanical only, then report the diff

When the operator says *"remove that name", "it's our project now", "rename X to Y"*, he means a
**rename**, not an editorial pass. Correction received 2026-11-16: *"DO NOT change the whole name of
everything, just rename hexbrain to vault that type, DO NOT CHANGE ANYTHING ELSE."*

Do exactly this, in this order:

1. Move/rename the paths: dataset dir (`Vault/_HEXBRAIN` → `_VAULT`), working dir
   (`~/Bugbounty/hexbrain` → `~/Bugbounty/vault`), data files (`hexbrain_reports.sqlite` →
   `reports.sqlite`, `.jsonl` likewise), then update hardcoded absolute paths inside the scripts.
2. Replace **only the brand token** in text (`_HEXBRAIN` → `_VAULT`, `HexBrain` → `Vault`,
   `hexbrain` → `vault`). Do not reword sentences, retitle files, or "improve" prose you touch.
3. Regenerate the derived files from the scripts (`export_to_vault.py` → `inject_case_stock.py` →
   `ingest_vault_docs.py`) instead of sed-ing generated output; re-running is how paths stay coherent.
4. Delete the stale directory (`rm -rf _HEXBRAIN`) and the upstream repo clone — a leftover clone keeps
   the name in its directory path forever.
5. Prove it: name sweep (`grep -ril --include='*.md' --include='*.py' --include='*.sh' <token> Vault ~/Bugbounty`,
   bounded by `timeout` — an unbounded grep over `~/Bugbounty` times out on binaries), then re-run the audit.
6. Reply with a **numbered list of what changed** (path → path, token → token, tables added) and an
   explicit "NOT TOUCHED" list (report counts, bounties, routing, module prose). He asked for exactly
   that: *"let me know after change what you changed."*

Cosmetic artefacts that survive a pure rename (`Vault/_VAULT`, "Vault class XSS" in generated titles)
are acceptable — flag them in one line and offer to polish; do not silently rewrite.

## Pitfalls

- **Never dump 15k individual .md files.** SQLite + `extract_report.py` is the deliverable; md dumps
  are hundreds of MB of unqueryable noise.
- Re-run `export_to_vault.py` **after** the body crawl finishes, or the vault README keeps claiming
  "6 full write-ups stored" long after 12,000 exist.
- Bounty sum is the sum of `bounty_amount`; blank means no figure shown, **not** "unpaid" — say so in
  the README, or the numbers read as a pay-rate claim they can't support.
- Weakness is the program's own field only sometimes; where it is null the class is a title keyword
  guess. Label it as such.
- **`http_status = 200` is NOT "write-up stored".** Of 12,522 rows that returned 200, **2,647 had an
  empty `vulnerability_information`** — the program published a summary and the researcher wrote
  nothing. Counting 200s overstates the corpus by ~21% and reads as a false claim of completeness.
  Count `length(body) > 0`, and report the four-way split, which must reconcile exactly:
  full write-up + summary-only + delisted 404 + other = total. (2026-11-16: 9,875 + 2,647 + 2,722 + 0
  = 15,244.) `has_body` in the CSV must be `length(body) > 0`, not "the row exists in `bodies`".
- **Write the split into the README as a table** with a "rows accounted for = the full list" line. That
  one table is the whole honesty story: what was retrieved, what was blank upstream, what is gone.
  Never let the headline say "15,244 reports" without the retrieval state next to it.
- **SQLite counting traps**: `SUM(http_status=404)` works (boolean → 1/0) but `SUM(404)` sums the
  constant and returns nonsense (it printed 6,158,576 on 15k rows). Always `SUM(cond)` or
  `COUNT(*) FILTER (WHERE …)`, then assert the parts add up to the total before quoting anything.
- **`pgrep -f <pattern>` matches your own shell** when the pattern is in the command line you just ran,
  so you get PHANTOM extra PIDs and a false "duplicate crawler" alarm. Check with `ps -o pid,ppid,cmd`
  on the specific PIDs, and pattern on the interpreter (`pgrep -f "python3 harvest_bodies.py"`).
  Likewise `pkill -f harvest_bodies` killed the shell issuing it (exit -15) — kill by PID from `ps`
  output, or accept that the visible -15 is your own command.
- **`length(body) > 0` is still not "a real write-up".** After the four-way split reconciles, some
  "bodies" are 1–39 chars of whitespace (`"   "`, a stray newline). 2026-11-16: 115 of 9,875. When
  you report coverage (e.g. for a retrieval index) say "9,760 covered + 115 whitespace-only stubs =
  9,875", not "9,875 covered" — otherwise the first retrieval miss exposes the overstatement.
- Verify before reporting: `SELECT COUNT(*) FROM reports` must equal the API's `total`; check
  `SELECT http_status, COUNT(*) FROM bodies GROUP BY 1` to see the real 200/404 split.

### Audit-time failure modes (all seen 2026-11-16, all false alarms)

- **Float bounty sums**: `SUM(bounty)` on REALs gives 4934914.52, while the README renders
  `f"{x:,.0f}"` → `4,934,915`. Comparing with `int()` fails by one dollar. Compare `round(x)` and
  print the exact value alongside (`$4,934,914.52`), or you "discover" a data bug that isn't there.
- **`os.walk` root is `"."`**: a hidden-dir filter `any(part.startswith("."))` also drops the vault
  root, so a root-level file (`00_MASTER_CATEGORY_LIST.md`) vanishes and documents≠disk by 1.
  Filter with `if part not in (".", "")`.
- **Renamed fence markers duplicate blocks**: if the marker constant changes, the old
  `<!-- OLD:BEGIN -->…<!-- OLD:END -->` block is no longer matched and gets a second block appended.
  Strip the legacy fence explicitly (`re.sub(legacy_begin + ".*?" + legacy_end, "", src, flags=re.S)`)
  before writing the new one, then verify with `grep -c BEGIN` per README.
- **`grep` over `~/Bugbounty` unbounded** walks huge binaries and times out; always
  `timeout 90 grep -ril --include='*.md' --include='*.py'` and treat empty output as the pass condition.
- Column names in old corpora differ (`disclosed_reports.id/vulnerability_information/weakness_name`)
  from the new schema — union dedupe by id, and report overlap/old-only/union instead of assuming one
  dataset subsumes the other (2026-11-16: 3,673 old, 15,244 new, 3,606 shared, 67 old-only, 15,311 union).

## Scripts

`scripts/harvest_meta.py` · `scripts/harvest_bodies.py` · `scripts/export_to_vault.py` ·
`scripts/inject_case_stock.py` · `scripts/watchdog.sh` — the harvest/export pipeline above.

`scripts/ingest_vault_docs.py` — index every vault `.md` into `documents` + `documents_fts`
(full text, sha256, idempotent upsert, stale-row removal). Run last in `refresh.sh`.

`scripts/audit_vault.py` — the 30-odd gate audit (reconcile arithmetic, csv↔db, views, README
claims, wiring, extract end-to-end, documents parity). Run it before any "done" message and quote
its tally.

## Reference

`references/hexbrain-2026-11.md` — the 2026-11-16 harvest: exact counts, class distribution,
top programs, the repo's internals (schema, ingest commands, MCP tool list), and the vault layout
as it stands.

`references/vault-convention.md` — the playbook vault's file/module/frontmatter convention and its
evidence discipline (byte-true quotes, 404 rows recorded never quoted, labeled bounty figures).
Read it before authoring or re-wiring a playbook dir, and keep `00_MASTER_CATEGORY_LIST.md` current.
