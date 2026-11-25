---
title: "Source index — provenance, fetch ledger, and dispositions for the 247-row corpus"
type: reference
category: source-index
corpus_rows: 247
retrievable: 151
full_bodies: 100
metadata_only: 51
http_404: 96
list_accessed: "2026-10-25"
note: "All fetching was unauthenticated GETs against hackerone.com/reports/<id>.json at 1.2 s spacing, responses cached. No auth tokens, no access-control bypass, no rate-pounding."
---

# Source index

## 1. Provenance

- **Source list**: `https://github.com/shreyaschavhan/h1-reports-for-reference/blob/master/tops_by_bug_type/TOPSQLI.md`
  — community-curated "top SQL injection reports by bounty" roster —
  33,291 bytes fetched 2026-10-25; parsed to 247 rows / 59 programs /
  $249,066 list-stated total. Parsed copy: `/tmp/opencode/sqli/sqli_top_list.json`.
- **Report fetch**: every listed report id resolved as
  `https://hackerone.com/reports/<id>.json` (public disclosure API,
  unauthenticated). 151 responses received (all JSON-parseable, zero
  withheld-unchecked); 96 returned **HTTP 404** (origin-dead).
- **Era heading**: disclosure years among the 100 full bodies:
  2014:5 · 2015:3 · 2016:6 · 2017:7 · 2018:10 · 2019:27 · 2020:15 · 2021:20 · 2022:7 —
  a 2014–2022 corpus with a 2019–2021 fat center (distinct from the SSRF
  vault's 2013–2017 ledger).
- **Weakness labels on the 100 full bodies** (archive-era values): SQL
  Injection 88 · None 5 · Code Injection 2 · Cross-site Scripting 1 ·
  Deserialization 1 · Command Injection 1 · Improper Access Control 1 ·
  Violation of Secure Design Principles 1. Playbooks treat *bodies* as the
  class authority (see each file's §Archive-era-label-honesty).

## 2. Programs (full 247-row list, top 16)

| Program | rows | | Program | rows |
|---|---:|---|---|---:|
| U.S. Dept Of Defense | 54 | | Uber | 6 |
| Mail.ru | 43 | | Automattic | 5 |
| Razer | 12 | | GitHub Security Lab | 5 |
| LocalTapiola | 11 | | MTN Group | 4 |
| Zomato | 10 | | Acronis | 4 |
| Node.js third-party modules | 8 | | Nextcloud | 4 |
| QIWI | 7 | | Informatica | 4 |
| Starbucks | 6 | | Rocket.Chat | 3 |

(43 of 59 programs have ≤3 rows each.)

## 3. Disposition funnel

| Disposition | rows | bounty accounting |
|---|---:|---|
| Full body + classified | 100 (97 classified + 1 adjacent + 2 negative-controls) | $27,311 mixed (15,000/8 rows JSON-verified + 12,311 list-stated) |
| Metadata-only (JSON present, body empty) | 51 | $64,600 (46,000/12 rows JSON-verified + 18,600 list-stated) |
| HTTP 404 (origin-dead) | 96 | $157,155 list-stated (recorded, not claimable) |
| **Total** | **247** | **$249,066** (matches list total exactly) |

Full row-per-row ledger: [`references/case-register.md`](case-register.md).
Bounty fields marked `JSON` are platform-recorded amounts from
hackerone.com/**reports/`<id>`.json; `list` amounts are as stated on the
source list itself — SSRF-vault bounty rule (JSON where present, else
list-stated, labeled).

## 4. Top list-bounty rows (≥$4,500 — the whole set in the register)

| bounty (list) | id | disposition | title/program |
|---:|---|---|---|
| $25,000 | #383127 | metadata-only | `report_xml.php … countryFilter` — Valve |
| $15,000 | #868436 | **404** | `city-mobil.ru` time-based — Mail.ru |
| $10,000 | #881901 | **404** | `fleet.city-mobil.ru` — Mail.ru |
| $7,500 | #818972 | **404** | unauth'd direct output — Mail.ru |
| $5,500 | #816254 | **404** | QIWI `TScenObject` (title says RCE) |
| $5,000 | #786044 | **404** | windows10.hi-tech.mail.ru blind — Mail.ru |
| $5,000 | #1525200 | **404** | files.palantir.com, CVE-2021-era — Palantir |
| $5,000 | #795291 | **404** | turboslim.lady.mail.ru blind — Mail.ru |
| $5,000 | #1024773 | **404** | delivery-club.ru (ClickHouse) — Mail.ru |
| $4,500 | #403616 | **404** | Zomato `/php/…` item_id |
| $4,500 | #273946 | **full body** | drivegrab ordering oracle — Grab (JSON $4,500) |
| $4,500 | #1241583 | **404** | GitHub Security Lab C++ pqxx connector |

Note the *Mail.ru shape*: all 43 of its rows are 404s — the program's
disclosure history cleansed from the public API. Recorded honestly rather
than reconstructed.

## 5. The 96 HTTP-404 rows (by program)

| Program | 404s |
|---|---:|
| Mail.ru | 43 |
| Razer | 12 |
| LocalTapiola | 11 |
| QIWI | 7 |
| GitHub Security Lab | 5 |
| Yahoo! | 3 |
| Tube8 / OLX / Vanilla / YouPorn | 2 each |
| (24 further programs) | 1 each |

Full id list with titles and list-bounties:
[`references/case-register.md`](case-register.md). These rows contributed
no claims anywhere in the vault; single-digit exceptions appear as
*(404 row, not retrievable)* notes only where the *list row itself*
carried a number worth surfacing (e.g. §4 above).

## 6. The 51 metadata-only rows

JSON metadata present (titles, severity, substates, disclosure dates,
sometimes bounty), body empty. They anchor funnel counts and the register;
none of their *content* is quoted as technique evidence anywhere in the
vault. Highest-value ones: #383127 ($25k, Valve), #258582 ($1,000, Zomato,
union-titled), #531051 ($4,000, Starbucks — a `sqlmap`-banner row per its
title only).

## 7. Fetch ledger mechanics (reproducibility)

- Scripts: `fetch_sqli.py` (list→ids→JSONs), `parse_sqli.py`
  (→ `raw_dataset.json`, `missing_ids.json`), `build_digest.py`
  (→ `bodies.txt`, 6,097 lines: bodied cases + metadata cases + MISSING
  blocks).
- Log: `/tmp/opencode/sqli/fetch_log.txt` — per-request status lines; all
  404s recorded there and in the register.
- Everything is re-runnable; the vault contains zero content that is not
  traceable to a cached artifact under `/tmp/opencode/sqli/`.

## 8. Known limitations (honest ledger)

1. **Corpus selection is the source list's, not ours** — "top by bounty" is
   the *relevance* lens; the vault makes no claim of a representative sample
   of SQLi. The 100 classified cases are the evidence base; the 147
   non-bodied rows are limits, not findings.
2. **Archive labels (weakness/severity) are era values** — 88/100 rows are
   labeled correctly enough for filing, but bodies overrule labels wherever
   they conflict (documented per playbook: XSS-label on a SQLi body, `None`
   weaknesses, severity drift).
3. **Third-party curator** — shreyaschavhan's list could contain rows whose
   bounty value differs from the platform record; where a JSON bounty
   existed it was used (20 rows, $61,000 JSON-verified platform total);
   every other amount is labeled list-stated.
4. **404 rows are unverifiable claims by nature** — titles and list-stated
   amounts are recorded but cannot be validated against report content; the
   Mail.ru/Razer/LocalTapiola/QIWI clusters ($124,310 of list value across
   73 dark rows) are
   permanently dark.
5. **Era gap** — bodies are 2014–2022; payloads not present in the corpus
   (e.g., modern WAF post-2022 technique evolutions) are *not* claimed; the
   agent playbook marks what is era-bound vs. current
   (`SQLI-Testing-Agent-Playbook.md` §8).
