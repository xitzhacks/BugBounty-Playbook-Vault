---
title: "Vault/XXE — XXE & All XML Injection playbook set"
type: index
category: "XXE / XML Injection (all types: in-band, blind OOB, error-based, container vectors, XML-RPC, policy files, parser internals)"
built: "2026-10-27"
evidence: "44 roster rows from h1.security.nathan.sx mirror → 35 retrievable (27 full bodies read) · 9 404 · 8 metadata-only"
bounty: "$50,227 grand total (list) · $16,500 JSON-verified · full reconciliation in references/case-register.md"
companion_vaults: "../SQLi · ../SSRF · ../XSS · ../IDOR"
case_id_scheme: "XXE-<HackerOne report id>"
quote_rule: "byte-true, (sic)-marked, from read bodies only; 404 rows recorded never quoted"
---

# Vault/XXE — the XXE & XML Injection playbook set

## Start here

| # | File | What it gives you |
|---|---|---|
| 1 | [`XXE-Testing-Agent-Playbook.md`](XXE-Testing-Agent-Playbook.md) | **The executable protocol.** P0 carrier inventory → P1 cheapest-first probes → P2 lane decision tree → P3 escalation → P4 discipline gates → P5 report assembly + kill-gates. Run this in the field. |
| 2 | [`In-Band-File-Read.md`](In-Band-File-Read.md) | Reflection lane: error-channel entity reads. Anchor: Twitter SXMP ($10,080 list-stated). |
| 3 | [`Blind-OOB-and-Parameter-Entities.md`](Blind-OOB-and-Parameter-Entities.md) | Callback lane: ping → parameter-entity exfil → FTP transport → SAML carrier. Anchor: Uber Movement ($500 JSON). |
| 4 | [`File-Upload-and-Format-Vectors.md`](File-Upload-and-Format-Vectors.md) | Container lane: XLF, XLSX, SVG, C-CDA import features + the client-side SVG trap. Anchor: Weblate XLF. |
| 5 | [`XML-RPC-Chains.md`](XML-RPC-Chains.md) | Protocol-abuse lane: SSO default-credential bypass ($7,000 JSON), pingback amplification, timing. |
| 6 | [`Crossdomain-and-Parser-Adjacents.md`](Crossdomain-and-Parser-Adjacents.md) | The two adjacent classes with boundary table: Flash policy files; PHP/Python parser memory bugs. |

## References (provenance layer)

| File | Contents |
|---|---|
| [`references/source-index.md`](references/source-index.md) | Roster provenance (nathan.sx mirror, 4,419 rows), filter pattern, funnel (44→35→27), era statistics, fetch mechanics, limitations. |
| [`references/case-register.md`](references/case-register.md) | Row-per-row ledger of all 44 roster rows: case ID, title, team, bounty (JSON vs list labeled), disposition, module assignment. Bounty reconciliation table. |
| [`references/blogs-index.md`](references/blogs-index.md) | Bibliography: zseano's XXE guide (byte-quoted), 40+ community writeups from bugbountyhunting.com (title-linked, honest), payload libraries, post-roster disclosed reports. |
| [`references/archive/xxe-bodies-2026-10-27.txt`](references/archive/xxe-bodies-2026-10-27.txt) | All 35 retrieved report bodies, verbatim dump (1,333 lines). |
| [`references/archive/h1-json-cache/`](references/archive/h1-json-cache/) | All 44 raw JSON responses from `hackerone.com/reports/<id>.json`. |

## How this vault was built (method)

1. **Roster**: full HTML of `h1.security.nathan.sx` (community mirror, 4,419 public H1 reports,
   frozen 2017-09-12) filtered for `xxe|xml|entity|soap|saml|xslt|xliff|web\.xml` → 44 rows.
2. **Retrieval**: every report fetched from the public unauthenticated `hackerone.com/reports/<id>.json`
   endpoint, 1.2s spacing, disk-cached → 35×200, 9×404.
3. **Reading**: all 35 bodies read end-to-end (`references/archive/`); classification decided by
   bodies, not titles. One roster match (XXE-223367) proved to be pure CSRF noise on body read and
   is recorded as such.
4. **Bounty accounting**: JSON `bounty_amount` where present ($16,500 across 4 rows), otherwise
   the mirror's list-stated figure, labeled everywhere; $17,387 sits on unrecoverable 404 rows.
5. **Modules**: five class modules + one adjacent-class module, each carrying verbatim evidence,
   an agent execution template, validation gates, and archive-label-honesty notes.
6. **Bibliography**: zseano's BugBountyHunter XXE guide fetched and byte-quoted; the
   bugbountyhunting.com writeup index mined for 40+ XXE/XML writeups, listed title-only (marked —
   fetch before citing as evidence); post-roster disclosed reports (Mail.ru Pulse $6,000,
   Open-Xchange PPTX $2,000, CosmicSting) kept out of register counts.

## Coverage vs limitations

**Covered**: entity file-read (reflected/error), blind OOB + parameter entities + FTP exfil,
container vectors (XLF/XLSX/SVG/C-CDA), SAML entity lane, XML-RPC protocol abuse (auth bypass,
pingback, timing), crossdomain policy doctrine, parser-memory adjacency, XML-RPC/SSRF chain doors.

**Honest limitations**:
1. The roster is a 2013–2018 snapshot (mirror frozen 2017-09-12) — modern parser-hardened
   defaults are the field reality; the playbook fingerprints hardening before payloads (P1).
2. 9 rows are permanently dark (404 at H1) — recorded, never quoted, $17,387 of list bounties.
3. 8 rows are metadata-only — team summaries quoted, no technique content.
4. Blog bodies were not fetched this build — `blogs-index.md` is a hunt queue, not proof.
5. No live testing was performed — every play step is corpus-derived; validate against the
   hunt-xxe skill's parser matrix in the field.

## The one-paragraph doctrine of this corpus

Every XXE finding in the roster is a **feature that eats XML nobody knew was XML**: an SMS
servlet, a translation import, a spreadsheet, a patient record, a SAML assertion, a login API,
an emblem uploader. The probes that found them are two-line diffs; the proofs are either an error
message that echoes a file or a callback with `Java/1.8.0_60` in it; and the payouts tracked the
**honesty** of the impact narrative — ping-only at $500, confirmed bypass at $7,000, demonstrated
read at $10,080.


<!-- CASESTOCK-LINK:BEGIN -->

## Case stock — vault (`_VAULT/`)

**199 disclosed reports** routed to this category · 41 with a bounty figure · **$59,092** · 128 full write-ups stored locally.

- Full list: [`_VAULT/by-vault-category/XXE.md`](../_VAULT/by-vault-category/XXE.md)
- Query: `sqlite3 ../_VAULT/reports.sqlite "SELECT id,bounty,title FROM reports WHERE ..."`
- Pull one write-up: `python3 ../_VAULT/scripts/extract_report.py <id>`

| Top paid | Program | Bounty |
|---|---|---|
| [505947](https://hackerone.com/reports/505947) XXE on pulse.mail.ru | Mail.ru | $6,000 |
| [2585378](https://hackerone.com/reports/2585378) important: Apache HTTP Server weakness in mod_rewrite when first segment of subs | Internet Bug Bounty | $4,920 |
| [2585381](https://hackerone.com/reports/2585381) important: Apache HTTP Server weakness with encoded question marks in backrefere | Internet Bug Bounty | $4,920 |
| [1637621](https://hackerone.com/reports/1637621) Command injection in GitHub Actions ContainerStepHost | GitHub | $4,000 |
| [2585374](https://hackerone.com/reports/2585374) moderate: Apache HTTP Server: mod_rewrite proxy handler substitution (CVE-2024-3 | Internet Bug Bounty | $2,600 |

_refreshed 2026-11-17 from the public HackerOne disclosed-report dataset_
<!-- CASESTOCK-LINK:END -->
