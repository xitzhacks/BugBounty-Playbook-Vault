# hexbrainai.com corpus — 2026-11-16 harvest

Session detail behind `disclosed-report-corpus`. Numbers are what the endpoints returned that day;
re-check before quoting.

## Corpus at harvest

- 15,244 reports total (`total` from `/api/reports`); 152 pages at limit 100, harvested with 0 missing.
- 14,614 with a program-set weakness; 3,241 with a bounty figure; **$4,934,915** summed bounties.
- Severity split: medium 3,553 · low 2,264 · high 1,952 · critical 995 · none 549 · null 5,931.
- Top programs: Mail.ru 896 · U.S. Dept Of Defense 884 · Internet Bug Bounty 794 · curl 683 ·
  Nextcloud 614 · HackerOne 607 · Shopify 467 · Node.js third-party modules 307 · GitLab 257 · X/xAI 248.

## Class distribution (hexbrain taxonomy, after title-guessing the nulls)

XSS 2,587 ($555k) · INFO 1,997 ($461k) · ACL 1,498 ($567k) · AUTH 1,367 ($417k) · CONF 1,265 ($118k) ·
MEM 917 ($472k) · RCE 843 ($625k) · DOS 637 ($332k) · OTHER 629 ($206k) · CSRF 530 ($69k) ·
LOGIC 490 ($144k) · CRYPTO 406 ($69k) · INJ 389 ($173k) · IDOR 373 ($186k) · REDIR 357 ($33k) ·
SQLI 332 ($185k) · SSRF 330 ($179k) · TRAV 199.

Routed into our playbook dirs — largest: XSS 2,528 · 16_Information-Disclosure ~1.9k ·
17_Privilege-Escalation ~1.4k · Authentication-Session ~1.3k · RCE 803 · IDOR 360 · Open-Redirect 340 ·
SQLi 327 · SSRF 324 · XXE 199 (the refined rules pull smuggling/CRLF, host-header and rate-limit rows
out of INJ/AUTH, which is why dir counts differ from class counts).

## Body crawl reality

- 4 workers @0.35 s delay ≈ 2.5 req/s sustained, ~1.5–2 h for 15k. Observed window-to-window rate
  swung 1.9 → 6.5 req/s (HackerOne throttling bursts), so never promise a single ETA.
- 8 concurrent → 9/24 requests 429. The limit sits around 3–4 req/s.
- ~19% of ids are 404: HackerOne delisted them. Same rate the h1 mirror showed (35/44 retrievable in
  the older roster) — treat it as normal, store the status, never quote a 404.
- Retry-After on 429 is single-digit to low-double-digit seconds. Sleeping 45–65 s per 429 dropped the
  crawl to ~34 reports/min; that sleep was the entire throughput problem.
- **Final reconciled result (all 15,244 fetched, 0 unresolved):**
  | State | Rows |
  |---|---|
  | Full write-up (`length(body)>0`) | 9,875 (101 MB) |
  | Summary only (200, empty body) | 2,647 |
  | Delisted (404) | 2,722 |
  | Other / unresolved | 0 |
  Final crawler pass logged `ok=12,234 fail=2,655`; the DB split above is authoritative — trust the
  reconciliation, not the last log line.

## The upstream site/repo

- `hexbrainai.com` — map home `/`, plus `/browse`, `/bypasses`, `/payloads`, `/cves`,
  `/class/<id>`, `/program/<name>`, `/report/<id>` (all public HTML, 200 without auth).
- `github.com/hackerspider1/hexbrainai.com` — Next.js 16.4.6, React 19.3, `node:sqlite` (Node ≥22.5),
  pnpm. DB at `data/hexbrain.db`, **gitignored**; `data/sources`, `data/subdomains` also ignored.
- Ingest chain: `ingest:import` (reddelexc CSV) → `ingest:details` (~50/min, resumable) →
  `ingest:index` (passages/sections + protection tags = the bypass library) → `ingest:payloads`
  (PayloadsAllTheThings) → `ingest:cves` (nuclei + KEV + EPSS) → `ingest:cvenow` → `ingest:subdomains`
  (Chaos) → `ingest:logos`.
- Public JSON: `/api/reports` (600/min, limit ≤100). `/api/v1/<tool>` and `/api/mcp` return 401
  without a key; keyed limits are 90/min, 5000/day, 240/address.
- MCP tools: list_classes, search_reports, get_report, get_testing_playbook, get_program_history,
  find_bypasses, find_payloads, plan_tests, find_cves, get_cve, get_attack_surface.
- `src/lib/taxonomy.ts` holds the class regexes + `TITLE_RULES` guesser — copied verbatim into
  `scripts/export_to_vault.py` so our routing matches theirs.

## Vault result

`/home/user/projects/FAN/Vault/_VAULT/` — README, all-reports.csv, reports.sqlite,
18 `by-class/` files, 30 `by-vault-category/` files, `scripts/`. Plus a `CASE-STOCK DATASET LAYER`
section in `Vault/00_MASTER_CATEGORY_LIST.md` and a fenced `CASESTOCK-LINK` block in all 30 playbook READMEs.

Renamed `_HEXBRAIN` → `_VAULT` (and `hexbrain-reports.sqlite` → `reports.sqlite`) at the operator's
instruction — he treats the corpus as his own project and wants the upstream product name absent from
the vault. His correction on the first attempt: *"DO NOT change the whole name of everything, just
rename hexbrain to vault that type, DO NOT CHANGE ANYTHING ELSE."* Mechanical rename only, then a
numbered change list + a NOT-TOUCHED list in the reply.

Final DB state (2026-11-16, audited 41/41): 52 MB, tables `reports` 15,244 · `bodies` 15,244 ·
`documents` 323 (all vault `.md`, 9.75 MB of text, `documents_fts` searchable, every row's sha256
verified against disk). Working scripts live in `~/Bugbounty/vault/`.

Older corpus for comparison (`/home/user/tools/h1-brain/disclosed_reports.db`, schema
`disclosed_reports(id, title, vulnerability_information, weakness_name, program_handle,
asset_identifier, asset_type, cve_ids, bounty_amount)`): 3,673 rows, 3,606 shared with the new
library, 67 old-only, **15,311 unique if unioned**. Offered to fold the 67 in; not done yet.

Open follow-ups deferred at session end: rebuild the bypass library locally from the stored bodies
(sections/report_tags/report_refs equivalent) and mirror `/payloads/<topic>` for offline payload lookup.
