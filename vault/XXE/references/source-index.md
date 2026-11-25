---
title: "XXE/XML source index — provenance, funnel, fetch mechanics"
type: provenance
roster_source: "https://h1.security.nathan.sx/ (community mirror of public HackerOne reports, 4,419 rows, $2,030,173 paid, last updated 2017-09-12)"
accessed: "2026-10-27"
pattern_rows: 44
retrievable: 35
full_bodies_read: 27 (26 classified + 1 noise-excluded on body read)
metadata_only_rows: 8
http_404_rows: 9
bounty_grand_total_listed: "$50,227 (JSON $16,500 across 4 rows + list-stated $33,727)"
companion_vaults: "../SSRF · ../SQLi · ../XSS · ../IDOR"
---

# Source Index — XXE/XML vault

## 1. Roster harvesting

The roster was the **h1.security.nathan.sx** mirror (per your instruction: "fetch from here all h1
reports"). The full HTML table (4,419 report rows, team/bounty/title columns, 17,747 source lines)
was fetched and pattern-filtered — *filter only, classification decided by bodies* — for:
`xxe|xml|entity|soap|saml|xslt|xliff|web\.xml` (case-insensitive).

- 44 rows matched (IDs extracted from the HTML `href` anchors — the text render strips them).
- One match was **noise** (XXE-223367, a pure-Weblate CSRF case whose title/body contain no XML
  term at all — the roster filter caught it through an unrelated coincidence). It is recorded in
  the register, excluded from all class counts.
- The mirror predates 2017-09-12: **every 2018–2026 XXE case (Mail.ru Pulse $6,000, Open-Xchange
  PPTX $2,000, Zivver SVG, CosmicSting, the bugbountyhunting.com blog corpus) is OUTSIDE this
  roster** and lives in [`blogs-index.md`](blogs-index.md), not in the register counts.

## 2. Program histogram (44 rows)

| Program | Rows | Notes |
|---|---:|---|
| Informatica | 6 | all rows one shared backend: rev-app ×2, marketplace ×2, upload feature, ondemand login |
| Uber ★ | 4 | $208,700 program total on the mirror; 2 rows are the class's biggest payouts |
| Imgur | 2 | crossdomain policy pair |
| Pornhub | 3 | 2 of 3 dead at origin ($12,500 listed between them) |
| QIWI | 2 | both SOAP/WAF-flavored XXE, both dead at origin ($4,137 listed) |
| HackerOne ★ | 3 | all SSO-SAML adjacent class |
| Weblate | 3 | XLF XXE (real), CSRF noise, and — in later sources — the XLF class anchor |
| Twitter | 1 | **$10,080** — largest reconstructable XXE payout |
| Vimeo / Badoo / Mobile Vikings / ok.ru / Mail.Ru / Localize / drchrono / Moneybird / Bime / Automattic / Coinbase / ownCloud / withinsecurity / Nextcloud / DoD | 16 | one to two rows each |
| PHP (IBB) / Python (IBB) / Yahoo! | 5 | parser-internals and native-app rows |

## 3. Funnel

| Stage | Count | Notes |
|---|---:|---|
| Roster rows | 44 | 43 after noise exclusion |
| Retrieved (HTTP 200) | 35 | public unauthenticated `hackerone.com/reports/<id>.json` |
| **HTTP 404 (origin-dead)** | **9** | 229980 · 142562 · 106802 · 105655 · 99279 · 72272 · 36450 · 12583 · 10767 — **$17,387 list-stated recorded, unrecoverable** |
| Full bodies present | 27 | 26 kept + 1 noise-excluded |
| Metadata-only (200, body withheld) | 8 | 188743, 130661, 112116, 105787, 167828, 173972, 223014, 91604 |

The 404 cluster is XXE-concentrated: Pornhub's unserialize→XXE ($10,000), QIWI's WAF-bypass XXE
($3,137) and SOAP XXE ($1,000), and Mail.ru's XXE→SSRF ($700) are all permanently dark — titles and
figures recorded, **nothing quoted, nothing reconstructed from memory or blogs** (same rule as the
SQLi vault's 96×404 roster).

## 4. Body-fetch mechanics (identical to the SQLi vault's method)

```bash
for id in $(cat ids.txt); do
  curl -s -m 25 -o "json/$id.json" -w "%{http_code}" "https://hackerone.com/reports/$id.json"
  sleep 1.2   # spacing discipline
done
```

- Public, unauthenticated endpoint only. No auth, no access-control bypass, no enumeration beyond
  the roster.
- Every response disk-cached: [`archive/h1-json-cache/`](archive/h1-json-cache/) (44 files).
- Bodies concatenated verbatim: [`archive/xxe-bodies-2026-10-27.txt`](archive/xxe-bodies-2026-10-27.txt)
  (1,333 lines, truncated at 12,000 chars/body, `(sic)` marks applied at quote time).
- `bounty_amount` exists on only 4 rows (JSON-verified $16,500). Notably XXE-248668 — the mirror's
  headline $10,080 Twitter row — returns `has_bounty?: true` with the amount withheld, so it is
  **list-stated, labeled as such everywhere**.

## 5. Era statistics

| Year (disclosed_at of retrievable bodies) | Count |
|---|---|
| 2013 (8091 era) | 1 |
| 2015 (43070…55431) | 5 |
| 2016 | 8 |
| 2017 | 18 |
| 2018 | 1 (213789) |

The corpus is a **2013–2018 snapshot with a 2016–2017 fat center** — the era when Java/JAXP and PHP
`DOMDocument`+`LIBXML_NOENT` defaults were still unhardened in production. Consequence for the
playbooks: mechanisms survive (entity parsing, parameter entities, error reflection), but the
*default-vulnerable* assumption does not — the agent playbook's §2 fingerprints parser hardening
before any payload is fired. Post-2018 XXE cases (browsers, PPTX, XLIFF, CosmicSting) are cited
from blogs-index only, never blended into register counts.

## 6. Limitations

1. **One-source roster, curated by a third party.** The mirror's bounty column is list-stated;
   wherever JSON carried a figure it was used and labeled. Grand total reconciles to the extracted
   roster, but the roster itself is not a complete H1 XXE census — it predates 2017-09-12.
2. **9 rows are permanently dark** (404). Titles + list bounties recorded; no technical claim in
   any playbook rests on them.
3. **8 rows are metadata-only.** Team summaries quoted where present; no technique content.
4. **Severity labels are era values** (Twitter SXMP `medium`, Informatica cluster `high` with
   weakness label `Command Injection`/`Uncontrolled Resource Consumption` — both wrong-vs-body;
   the register keeps the archive label, the playbook corrects it against the body, per the
   "bodies win" rule).
5. **Out-of-roster sources are bibliographic.** The zseano bugbountyhunter XXE guide and the
   bugbountyhunting.com writeup index were fetched 2026-10-27 and are byte-quoted where read;
   blog bodies NOT fetched this build are listed title-only and marked so. No claim in the
   playbooks depends on a title-only row.
6. **crossdomain.xml rows kept as their own class**, not laundered into "XXE" — they are Flash
   policy misconfigurations whose XML is incidental (module §8 draws the boundary).
