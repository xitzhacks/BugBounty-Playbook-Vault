---
title: "SQL Injection Knowledge Base — README"
type: index
candidates: 247
retrievable: 151
full_bodies_read: 100
classified_cases: 97
adjacent_cases: 1
negative_control_cases: 2
metadata_only_rows: 51
http_404_rows: 96
bounty_total_confirmed: "$27,311 (JSON-verified $15,000 across 8 rows + list-stated $12,311)"
bounty_total_metadata_only: "$64,600 (JSON-verified $46,000 across 12 rows + list-stated $18,600)"
bounty_total_on_404_rows: "$157,155 (list-stated, unrecoverable)"
bounty_grand_total_listed: "$249,066 (matches source list exactly)"
external_sources_cached: 5
external_sources_unreachable: 3
archive_accessed: "2026-10-25"
era_range: "2014–2022 (bodies: 2015→2022 disclosures)"
case_id_scheme: "SQL-<HackerOne report id>"
built_for: "AI-agent executable testing"
---

# SQL Injection Knowledge Base

Built from the **247-row community roster**
[`TOPSQLI.md`](https://github.com/shreyaschavhan/h1-reports-for-reference/blob/master/tops_by_bug_type/TOPSQLI.md)
("top SQL injection reports by bounty"), of which **151 reports remained
retrievable** at origin on 2026-10-25 and **100 returned full readable bodies**.
After body-read classification: **97 confirmed cases across 6 category
playbooks**, plus 1 adjacent internal-exposure case (SQL-687908), 2 era-native
negative controls (SQL-115304, SQL-131047), 51 metadata-only rows kept at honest
evidence level, and **96 now-404 reports recorded** — including an entire
 Mail.ru cluster (all 43 of its rows are dead at origin) worth $80,150 of
list-stated bounty that can never be reconstructed. Companion to the SSRF, XSS,
and IDOR knowledge bases in [`../SSRF/`](../SSRF/README.md),
[`../XSS/`](../XSS/README.md), and [`../IDOR/`](../IDOR/README.md).

## Start here

| File | Use it for |
| --- | --- |
| **[`SQLI-Testing-Agent-Playbook.md`](SQLI-Testing-Agent-Playbook.md)** | **Executing a test.** Phase-gated agent protocol: P0 carrier inventory → P1 cheapest-first detection (quote pair → type mismatch → boolean pair → delay series → position probes) → P2 oracle-ladder decision tree → P3 calibrated extraction → P4 gated escalation → P5 report assembly, with stop rules and the adjacent/negative-control kill-gates. |
| [`references/source-index.md`](references/source-index.md) | Provenance: 247-row funnel, program histogram, bounty accounting (JSON vs list labeled), the 96×404 roster by program, era statistics, limitations. |
| [`references/case-register.md`](references/case-register.md) | Row-per-row disposition ledger: every listed id → full-body+category, metadata-only, or 404, with title/program/bounty. |
| [`references/blogs-index.md`](references/blogs-index.md) | The bibliography the bodies themselves cite (5 cached sources with byte-true quotes; 3 unreachable recorded honestly incl. a dead Google Groups post). |
| The 6 category playbooks → | The evidence itself, per class (below). |

## Category playbooks

| File | Cases | What the class taught the playbook |
| --- | ---: | --- |
| [`Time-Based-Blind.md`](Time-Based-Blind.md) | 37 | The corpus's dominant oracle: `SLEEP()`/`WAITFOR`/`pg_sleep`/`BENCHMARK` delay series with *interleaved zero-controls*, multiplier calibration (`×5` observed — measure, never assume), baseline-overhead discipline, and a per-DBMS call book. Carriers beyond form fields: cookies, User-Agent, Referer, JSON-in-param, GraphQL args. |
| [`Library-and-Framework-SQLi.md`](Library-and-Framework-SQLi.md) | 21 | The sink is upstream of the app: npm builders (typeorm ×3, `sql`, query-mysql, untitled-model, @azhou/basemodel, increments, typeorm+prototype-pollution), WordPress `prepare()`, GitLab `reorder()`, Concrete ×2, Serendipity, ImpressCMS backtick lane, MODx 404-logger INSERT, Nextcloud doctrine/dbal dependency row, and the two Android content-provider cases — with the position-family inventory (which clause went unquoted). |
| [`Error-and-Union-Output.md`](Error-and-Union-Output.md) | 20 | In-band value→error conversion: `updatexml`/`extractvalue` XPATH banners, PostgreSQL `cast as date` echo, Oracle `OWA_UTIL.CELLSPRINT`, MSSQL `@@LANGID`, query-echo error pages, and union-render rows — three distinct layers (detect / convert / second-row) an agent must separate. |
| [`Boolean-and-Content-Oracle.md`](Boolean-and-Content-Oracle.md) | 14 | Band pairs as ground truth: quote-balance pairs, arithmetic booleans without quotes, redirect-oracle pairs, the ordering oracle (row-order flips as TRUE/FALSE), extraction ladders (`length()` → `substr`), and the corpus's write-side proof shape. |
| [`SQLi-to-RCE-Chains.md`](SQLi-to-RCE-Chains.md) | 4 | Escalation anatomy: Drupal `expandArguments` → session write → PHP exec (CVE-2014-3704, $3,000; SektionEins-anchored); Liberapay SQLi → pickled notification → `sleep(500000)` gadget; two Rocket.Chat NoSQLi operator-injections (`$regex`, `$where`) → reset-token/2FA leak → admin webhook → `whoami` shell, demo-instance discipline and restore-on-done included. |
| [`Out-of-Band-Callback.md`](Out-of-Band-Callback.md) | 1 | One textbook-complete MSSQL case (SQL-272506): `xp_dirtree` on a set-variable → Collaborator DNS + WebDAV `PROPFIND` with `Microsoft-WebDAV-MiniRedir` UA, egress IP + timestamp logged — the channel when *no* in-band oracle exists. |

Plus, outside classification: 1 adjacent case (SQL-687908, origin-IP recon →
exposed PgHero dashboard — located in the agent playbook §10) and 2 negative
controls (Boolean playbook §8) that anchor the kill-gate.

## Methodology and how this was built

1. **Roster harvesting.** TOPSQLI.md (33,291 bytes, 2026-10-25) was parsed into
   247 rows / 59 programs / $249,066 list-stated total
   (`/tmp/opencode/sqli/sqli_top_list.json`). Title-match was *filter only* —
   bodies decided classification.
2. **Conservative fetching.** Every listed id resolved via the public,
   unauthenticated `hackerone.com/reports/<id>.json` at **1.2 s spacing**, all
   responses disk-cached. 151 retrievable; **96 returned HTTP 404**
   (origin-dead) and are recorded — not dropped — in the register.
3. **Body-read classification.** All 100 full bodies were read: 97 classified
   into the 6 playbooks, 1 adjacent (infrastructure-first exposure), 2 negative
   controls. The 51 metadata-only rows keep title/label/bounty only; no
   technical claim anywhere in this vault rests on them.
4. **Case IDs.** `SQL-<report id>` throughout, mirroring the
   [`IDOR`](../IDOR/README.md), [`XSS`](../XSS/README.md), and
   [`SSRF`](../SSRF/README.md) vault conventions.
5. **Bounty rule** (same as the SSRF vault): **JSON `bounty_amount` where
   present, else the list's stated amount, visibly labeled.** JSON amounts were
   platform-recorded for 20 rows ($61,000); every other figure is list-stated.
6. **Quote discipline.** Every quote is verbatim from the case's own body
   (`/tmp/opencode/sqli/bodies.txt`, 6,097 lines) or the bibliography's cached
   sources; era typos preserved with `(sic)` marks — *"sstill"*, *"qoutes"*,
   *"aposrophes"*, *"bassed"*, *"succesful"*, *"effected"*, *"injextion"*,
   *"flexed"*, and more survive on purpose.
7. **Bibliography.** The six sources the bodies cite were chased: 5 retrieved
   and byte-quoted (OWASP SQLi canon page, PortSwigger topic index, SektionEins
   Drupal advisory, MongoDB `$regex` and `$where` docs); 3 recorded as
   unreachable (the Rails Google Groups post is JS-gated everywhere including
   Wayback; mysqltutorial.org moved (404); Nextcloud's `h1#197` tracker is 404).

## Coverage statistics

| Metric | Value |
| --- | --- |
| List rows | 247 (59 programs) |
| Retrieved from origin | 151 (96 × 404) |
| Full bodies read | 100 (97 classified + 1 adjacent + 2 negative controls) |
| Metadata-only rows | 51 |
| Disclosure years (full bodies) | 2014:5 · 2015:3 · 2016:6 · 2017:7 · 2018:10 · 2019:27 · 2020:15 · 2021:20 · 2022:7 — a 2019–2021 fat center (the SSRF vault's ledger runs 2013–2017, so the two corpora barely overlap) |
| Programs among the 100 full bodies | DoD 33 · Node.js third-party modules 8 · Automattic 5 · MTN Group 4 · Acronis 4 · Informatica 4 · Rocket.Chat 3 · Concrete CMS 3 · Starbucks 3 · Nextcloud 3 · Uzbey 3 · Zomato 2 · Mail.ru 0* |
| Substates (151 retrievable) | resolved 144 · informative 3 · not-applicable 3 · duplicate 1 |
| Weakness labels (100 full bodies) | SQL Injection 88 · None 5 · Code Injection 2 · XSS 1 · Deserialization 1 · Command Injection 1 · Improper Access Control 1 · Violation of Secure Design 1 |
| Largest full-body payout | $4,500 — Grab `drivegrab.com` blind ordering-oracle (SQL-273946, JSON-verified) |
| Smallest paid | $1 — Gratipay (SQL-81701, JSON-verified) |
| Unpaid full bodies | 76 of 100 |

\* every one of Mail.ru's 43 rows is now a 404 — recorded, not claimable.

### Bounty pyramid (mixed-era amounts, JSON vs list labeled)

| Band | Amount | Composition |
| --- | ---: | --- |
| Full-body (classified+adjacent+negative) | **$27,311** | JSON $15,000 / 8 paid rows + list $12,311 / 16 paid rows (24 paid total) |
| Metadata-only rows | **$64,600** | JSON $46,000 / 12 rows + list $18,600 |
| **Retrievable total** | **$91,911** | 151 rows |
| List-stated on 404 rows | **$157,155** | 96 rows — recorded, unrecoverable |
| **Grand total (list)** | **$249,066** | 247 rows — reconciles to the source list exactly |

Sanity anchors: the 404 cluster hides the era's biggest single figures
(Valve's $25,000 `report_xml.php` row is metadata-only; Mail.ru's $15,000/$10,000
time-based rows are both 404s), while the largest *reconstructable* payout is
Grab's $4,500 blind-oracle report. Amounts are as-recorded history, not guidance
for modern triage.

## Limitations — read this before testing from these files

1. **The corpus is a curated "top by bounty" list, not a sample.** It
   over-represents large-currency programs (DoD 54 rows, Mail.ru 43) and
   under-represents classes that pay low; the vault makes no claim of
   representative coverage of SQLi as a field.
2. **404 rows are unverifiable by nature** — titles and list-stated amounts
   recorded; nothing quoted. 96 rows ($157,155 listed) are
   permanently dark, concentrated in four programs ($124,310 of it in
   Mail.ru/Razer/LocalTapiola/QIWI). Do not reconstruct from memory or
   secondary blogs — the vault doesn't, and neither should an agent.
3. **Archive labels (weakness/severity) are era values.** Where labels and
   bodies conflict, bodies win — documented per playbook (an XSS label on a
   SQLi body, `Code Injection` on boolean-arithmetic reports, `None` on entire
   NoSQL chains, a body claiming MySQL while its own evidence shows MSSQL).
4. **Metadata-only rows.** 51 rows anchor the funnel and the register only;
   no technique content exists for them here. "No body" is not "no finding" —
   unauthenticated JSON retrieval withholds bodies for several
   disclosed-but-withheld reports.
5. **Era gap: 2014–2022.** Payload mechanics are current where the mechanisms
   survive (blind oracles, ordering/paging positions, operator injection,
   prototype pollution) and obsolete where they don't (magic-quotes regimes);
   the agent playbook's §8 marks each boundary honestly.
6. **One-source bibliography by design.** Only sources *the bodies
   themselves cite* were chased; no external methodology literature was
   laundered into the corpus. Unreachable sources stay listed as unreachable.
7. **Conservative access.** No auth, no access-control bypass, 1.2 s spacing,
   everything disk-cached; against live HackerOne, only public JSON reads and
   the six bibliography fetches were performed.
8. **Third-party curator risk.** List-stated bounty values can drift from the
   platform record; wherever a JSON number existed it was used and labeled,
   and the grand total still reconciles — but two handfuls of rows' figures
   exist only as list claims.

## Notes about the file list

- `SQLI-Testing-Agent-Playbook.md` — the executable protocol; carries the
  calibration constants (0.25–0.9 s baseline overhead, `×5` multiplier trap,
  `sleep(5*5)` arithmetic forms), stop rules, and the report-ledger sentences
  the era's best reports used ("I have not exfiltrated…" / "I only explored
  nonsensitive information.").
- `references/source-index.md` — §1 provenance & era stats, §2 programs,
  §3 funnel + bounty reconciliation, §4 top rows, §5 the 404 roster by program,
  §6 metadata-only rows, §7 fetch mechanics, §8 limitations.
- `references/case-register.md` — the 247-row disposition ledger (generated).
- `references/blogs-index.md` — the body-cited bibliography with byte-true
  quotes and honest retrieval outcomes.
- The six category playbooks share one structure: Overview → Case evidence
  (verbatim quotes, `(sic)` marks) → Anatomy/calibration → Agent execution
  template → Validation gates → Remediation → Archive-era label honesty.
- Quote rule: misquoted text is corrected only if it changes technique —
  otherwise preserved verbatim with a `(sic)`; nothing was written from memory.


<!-- CASESTOCK-LINK:BEGIN -->

## Case stock — vault (`_VAULT/`)

**327 disclosed reports** routed to this category · 83 with a bounty figure · **$184,502** · 155 full write-ups stored locally.

- Full list: [`_VAULT/by-vault-category/SQLi.md`](../_VAULT/by-vault-category/SQLi.md)
- Query: `sqlite3 ../_VAULT/reports.sqlite "SELECT id,bounty,title FROM reports WHERE ..."`
- Pull one write-up: `python3 ../_VAULT/scripts/extract_report.py <id>`

| Top paid | Program | Bounty |
|---|---|---|
| [383127](https://hackerone.com/reports/383127) SQL Injection in report_xml.php through countryFilter[] parameter | Valve | $25,000 |
| [868436](https://hackerone.com/reports/868436) Time-Based SQL injection at city-mobil.ru | Mail.ru | $15,000 |
| [881901](https://hackerone.com/reports/881901) SQL injection at fleet.city-mobil.ru | Mail.ru | $10,000 |
| [852306](https://hackerone.com/reports/852306) SQL LIKE clauses wildcard injection | Mail.ru | $8,000 |
| [818972](https://hackerone.com/reports/818972) SQL Injection [unauthenticated] with direct output at https://news.mail.ru/ | Mail.ru | $7,500 |

_refreshed 2026-11-17 from the public HackerOne disclosed-report dataset_
<!-- CASESTOCK-LINK:END -->
