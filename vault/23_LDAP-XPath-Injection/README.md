---
title: "Vault/23 — LDAP / XPath injection playbook set"
type: index
category: ldap-xpath
built: "2026-11-07"
evidence: "11 classified rows → 0 retrievable bodies (11 × metadata-only GitHub Security Lab rows) · 1 adjacent XQuery row held outside the vault · 0 quotes by design (corpus block)"
bounty: "$19,000 across 8 rows with DB figures (max $4,500, LX-1212273) · 3 rows carry no DB figure"
companion_vaults: "../XXE · ../SQLi · ../RCE · ../Authentication-Session"
case_id_scheme: "LX-<HackerOne report id>"
quote_rule: "byte-true, (sic)-marked, from read bodies only; metadata-only rows recorded never quoted"
---

# Vault/23 — LDAP / XPath injection playbook set

This vault is a **corpus block**, not a technique module: all 11 classified rows come from the
GitHub Security Lab program (CodeQL-query reports), every body is the same 54-byte pointer line,
and zero bodies survive to quote. Its value is the honest ledger — title, CWE, bounty tier, and
language per row — plus the negative-space lesson that a resolved bounty with no body is a
*claim*, not a finding.

## Start here

| # | File | What it gives you |
|---|---|---|
| 1 | [`LX-Testing-Agent-Playbook.md`](LX-Testing-Agent-Playbook.md) | **The executable protocol.** P0 program/policy read → P1 query-sink inventory (LDAP/XPath/XQuery builders) → P2 probe protocol (filter-breakout → syntax error → blind enumeration) → P3 proof ladder → P4 hardening fingerprints → P5 kill-gates. |
| 2 | [`00_codeql-corpus-block.md`](00_codeql-corpus-block.md) | All 11 rows listed side-by-side with title, language, CWE, and bounty tier. Zero technique quotes — the bodies do not exist in this corpus. |

## References (provenance layer)

| File | Contents |
|---|---|
| [`references/source-index.md`](references/source-index.md) | Corpus provenance (h1-brain DB `disclosed_reports`, sha256 `8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4`, 3,673 rows), classification funnel (`classified.json` bucket `ldap-xpath` → 11, `module_map_all.json` `codeql-corpus-block` → 11, `_adjacent_unclassified` 1 held outside), DB reconciliation, bounty accounting, era discipline, 7 limitations. |
| [`references/case-register.md`](references/case-register.md) | Row-per-row ledger of all 11 bucket rows: case ID, team, bounty, module, evidence level, CWE/language read from title. |
| [`references/archive/lx-bodies-full-dump.txt`](references/archive/lx-bodies-full-dump.txt) | All 11 bodies verbatim (each the 54-byte GHSL pointer line) — the anchor for the "zero quotes" decision. |
| [`references/archive/classes.json`](references/archive/classes.json) | Frozen module assignment for all 11 rows. |

## Scoreboard (11 rows · 8 with bounty figures · $19,000 · max $4,500)

Contributor rows from the classifier — no top-paid table is meaningful here because no technique
content exists; the full ledger is the register. Figures are DB `bounty_amount` where present;
`None` = no figure in the DB (not evidence of non-payment).

| Case | Language | CWE | Bounty |
|---|---|---|---|
| [LX-787113](https://hackerone.com/reports/787113) | Java | CWE-90 | $3,000 |
| [LX-824925](https://hackerone.com/reports/824925) | Java | (XPath query) | — |
| [LX-852316](https://hackerone.com/reports/852316) | Go | CWE-643 | $1,800 |
| [LX-956295](https://hackerone.com/reports/956295) | Java | LDAP injection | $2,500 |
| [LX-1050706](https://hackerone.com/reports/1050706) | JavaScript | CWE-90 | — |
| [LX-1095708](https://hackerone.com/reports/1095708) | Java | CWE-522 | $1,800 |
| [LX-1133572](https://hackerone.com/reports/1133572) | Java | CWE-297 | $1,800 |
| [LX-1212273](https://hackerone.com/reports/1212273) | Python | CWE-090 | **$4,500** (max) |
| [LX-1287575](https://hackerone.com/reports/1287575) | Python | CWE-287 | $1,800 |
| [LX-1350076](https://hackerone.com/reports/1350076) | Python | CWE-522 | $1,800 |
| [LX-1397942](https://hackerone.com/reports/1397942) | Go | CWE-090 | — |

## Vault map

| File | Content |
|---|---|
| `LX-Testing-Agent-Playbook.md` | Agent-facing operational playbook: P0–P5 phases, module↔phase table, non-goals. |
| `00_codeql-corpus-block.md` | Single module listing all 11 rows with CWE/language/bounty; zero quotes with explanation. |
| `references/source-index.md` | Provenance, funnel, DB reconciliation, bounty accounting, era discipline, limitations. |
| `references/case-register.md` | 11-row ledger with DB metadata, evidence level, CWE/language. |
| `references/archive/lx-bodies-full-dump.txt` | All 11 bodies verbatim (anchor for every quote — there are none). |
| `references/archive/classes.json` | Frozen module assignment for all 11 rows. |

## Cross-vault links

- `XXE/` — LDAP/XPath query builders sit in the same XML/directory grammar family; the adjacent
  XQuery row (1133573) belongs to that vault's neighborhood, held outside this corpus block.
- `SQLi/` — LDAP filters and XPath expressions are string-concatenation injection; treat the
  `SQLi` vault's filter-breakout methodology as the method family, not this vault's body evidence.
- `Authentication-Session/` — three rows (CWE-522/287/297) are authentication-configuration
  questions, not filter-breakout questions; the auth vault owns the defensive posture.

## Coverage vs limitations

**Covered**: the complete `ldap-xpath` classified bucket (11 rows) with per-row language/CWE/bounty;
the `codeql-corpus-block` module assignment (`module_map_all.json`); the single adjacent XQuery row
recorded as explicitly out-of-scope; DB reconciliation for every row.

**Honest limitations**:
1. **Zero bodies.** All 11 rows are 54-byte GHSL pointer lines. No technique, no payload, no PoC —
   nothing is quoted and nothing is reconstructed. This vault cannot teach LDAP/XPath exploitation
   from its own evidence; the playbook's probe phases are labeled as method-family doctrine, not
   corpus-observed steps.
2. **Single-source corpus.** Every row is `github-security-lab`. There is no commercial-program
   LDAP/XPath row in this bucket to price a live-service ranking; all bounties are CodeQL-query
   tiers (flat $1,800, exceptions $2,500/$3,000/$4,500).
3. **CWE from titles only.** Language and CWE come from report titles; weakness labels in the DB
   are null for all 11 rows. A title-vs-body conflict cannot exist here because no body exists.
4. **Adjacent row outside the vault.** 1133573 (XQuery Injection, CWE-652, GHSL, $None) is the
   `_adjacent_unclassified` row in `module_map_all.json`. It is recorded in the register's
   out-of-scope note and excluded from every count — not silently dropped, not silently merged.
5. **Bounty `None` ≠ unpaid.** 3 of 11 rows carry no DB figure; $19,000 is a corpus floor.
6. **Era honesty.** GHSL CodeQL-query bounties price detector authorship, not target impact.
   Do not use these tiers to estimate live LDAP/XPath payouts.
7. **No live testing was performed.** Validate LDAP/XPath probes against a lab directory/XML
   parser in scope — never against a production directory.


<!-- CASESTOCK-LINK:BEGIN -->

## Case stock — vault (`_VAULT/`)

**24 disclosed reports** routed to this category · 8 with a bounty figure · **$19,000** · 12 full write-ups stored locally.

- Full list: [`_VAULT/by-vault-category/23_LDAP-XPath-Injection.md`](../_VAULT/by-vault-category/23_LDAP-XPath-Injection.md)
- Query: `sqlite3 ../_VAULT/reports.sqlite "SELECT id,bounty,title FROM reports WHERE ..."`
- Pull one write-up: `python3 ../_VAULT/scripts/extract_report.py <id>`

| Top paid | Program | Bounty |
|---|---|---|
| [1212273](https://hackerone.com/reports/1212273) [Python] CWE-090: LDAP Injection  | GitHub Security Lab | $4,500 |
| [787113](https://hackerone.com/reports/787113) CodeQL query for finding LDAP Injection (CWE-90) vulnerabilities in Java | GitHub Security Lab | $3,000 |
| [956295](https://hackerone.com/reports/956295) LDAP injection vulnerability in Java | GitHub Security Lab | $2,500 |
| [852316](https://hackerone.com/reports/852316) Go/CWE-643: XPath Injection Query in Go | GitHub Security Lab | $1,800 |
| [1095708](https://hackerone.com/reports/1095708) [Java] CWE-522: Insecure LDAP authentication  | GitHub Security Lab | $1,800 |

_refreshed 2026-11-17 from the public HackerOne disclosed-report dataset_
<!-- CASESTOCK-LINK:END -->
