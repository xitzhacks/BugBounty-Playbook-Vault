---
title: "LDAP/XPath case register — 11-row ledger (h1-brain corpus)"
type: register
built: "2026-11-07"
roster: "h1-brain disclosed_reports.db (3,673 rows; sha256 8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4)"
case_id_scheme: "LX-<HackerOne report id>"
bounty_rule: "DB bounty_amount where present (labeled $) · None = no figure in DB (not evidence of non-payment)"
module_rule: "frozen in archive/classes.json (title+CWE census; zero bodies)"
---

# Case register — LDAP / XPath injection

Corpus: 11 rows · 8 with bounty figures · **$19,000** · max $4,500 (LX-1212273) · evidence: 0 full-body / 11 metadata-only.

Class census: codeql-corpus-block 11 (787113, 824925, 852316, 956295, 1050706, 1095708, 1133572, 1212273, 1287575, 1350076, 1397942) — single module, corpus block.

Bounty arithmetic: $4,500 + $3,000 + $2,500 + $1,800 + $1,800 + $1,800 + $1,800 + $1,800 = **$19,000** (8 rows). Five rows at the flat $1,800 GHSL query tier; three rows (824925, 1050706, 1397942) carry no DB figure.

Out-of-scope adjacent (not in any count): LX-1133573 ("Java: CWE-652 Improper Neutralization of Data within XQuery Expressions ('XQuery Injection')", github-security-lab, bounty None, 54-byte body) — the `_adjacent_unclassified` row in `module_map_all.json`, recorded so the bucket reconciliation is exact.

| Case | Language (title) | CWE (title) | Bounty | Module | Evidence | Note |
|---|---|---|---|---|---|---|
| [LX-787113](https://hackerone.com/reports/787113) | Java | CWE-90 | $3,000 | codeql-corpus-block | metadata | CodeQL query for finding LDAP Injection; GHSL query tier |
| [LX-824925](https://hackerone.com/reports/824925) | Java | (XPath query) | — | codeql-corpus-block | metadata | XPath Injection query in java; no figure |
| [LX-852316](https://hackerone.com/reports/852316) | Go | CWE-643 | $1,800 | codeql-corpus-block | metadata | XPath Injection Query in Go; flat tier |
| [LX-956295](https://hackerone.com/reports/956295) | Java | LDAP injection | $2,500 | codeql-corpus-block | metadata | LDAP injection vulnerability in Java |
| [LX-1050706](https://hackerone.com/reports/1050706) | JavaScript | CWE-90 | — | codeql-corpus-block | metadata | CodeQL to detect LDAP Injection; no figure |
| [LX-1095708](https://hackerone.com/reports/1095708) | Java | CWE-522 | $1,800 | codeql-corpus-block | metadata | Insecure LDAP authentication; flat tier |
| [LX-1133572](https://hackerone.com/reports/1133572) | Java | CWE-297 | $1,800 | codeql-corpus-block | metadata | Insecure LDAP endpoint configuration; flat tier |
| [LX-1212273](https://hackerone.com/reports/1212273) | Python | CWE-090 | $4,500 | codeql-corpus-block | metadata | LDAP Injection (Python); corpus max |
| [LX-1287575](https://hackerone.com/reports/1287575) | Python | CWE-287 | $1,800 | codeql-corpus-block | metadata | LDAP Improper Authentication; flat tier |
| [LX-1350076](https://hackerone.com/reports/1350076) | Python | CWE-522 | $1,800 | codeql-corpus-block | metadata | Insecure LDAP Authentication; flat tier |
| [LX-1397942](https://hackerone.com/reports/1397942) | Go | CWE-090 | — | codeql-corpus-block | metadata | LDAP Injection All For One; no figure |

Module totals: codeql-corpus-block **$19,000 / 8 rows** (1212273 $4,500 · 787113 $3,000 · 956295 $2,500 · 852316/1095708/1133572/1287575/1350076 $1,800 each).
