---
title: "Cryptography Issues — transport, primitives, and the client's trust decisions"
type: index
category: "Cryptography (TLS/STARTTLS/legacy · primitives, oracles & signatures · cert validation, weak secrets & insecure channels · adjacent/unclassified merges)"
built: "2026-11-07"
evidence: "46 rows from h1-brain disclosed_reports.db (3,673 rows; sha256 8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4) — 26 bucket + 20 documented unclassified merges · all full-body"
bounty: "$55,105 across 36 rows · 01 $1,500/2 · 02 $6,425/6 · 03 $3,680/7 · merge pool $43,400/20 · adjacent $100/1"
companion_vaults: "../18_Misconfiguration · ../14_HTTP-Request-Smuggling · ../Race-Conditions · ../Authentication-Session"
case_id_scheme: "CRYPTO-<HackerOne report id>"
quote_rule: "byte-true to references/archive/CRYPTO-bodies-full-dump.txt"
---

# Vault/Cryptography — broken constructions, not broken algorithms

Forty-six disclosed cases (26 classified + 20 merged from the unclassified pool). The corpus never
pays for "outdated TLS"; it pays for **a demonstrated break**: a cert check that did not happen, a
cardinality mistake that leaks a secret, a signature that can be moved, a padding oracle that
recovers plaintext.

## Start here

| # | File | What it gives you |
|---|---|---|
| 1 | [`CRYPTO-Testing-Agent-Playbook.md`](CRYPTO-Testing-Agent-Playbook.md) | Executable protocol: identify construction → oracle/leak probe → proof ladder → kill-gates |
| 2 | [`01_TLS-STARTTLS-Legacy-Protocol.md`](01_TLS-STARTTLS-Legacy-Protocol.md) | STARTTLS stripping, protocol injection, DROWN/POODLE — 7 rows, $1,500 |
| 3 | [`02_Crypto-Primitives-Oracles-Signatures.md`](02_Crypto-Primitives-Oracles-Signatures.md) | CBC cut-and-paste, length extension, DH keygen, JWE curves, gem forgery — 10 rows, $6,425 |
| 4 | [`03_Cert-Validation-Weak-Secrets-Insecure-Channel.md`](03_Cert-Validation-Weak-Secrets-Insecure-Channel.md) | Missing cert validation, `SECRET_KEY="N/A"`, TOTP entropy, HTTP channels — 8 rows, $3,680 |
| 5 | [`04_Adjacent-and-Unclassified.md`](04_Adjacent-and-Unclassified.md) | The 20 merge rows (GHSL/CWE queries and adjacent findings) — $43,400/20 |

## References (provenance layer)

| File | Contents |
|---|---|
| [`references/source-index.md`](references/source-index.md) | DB provenance, funnel, bounty accounting, era discipline, limitations |
| [`references/case-register.md`](references/case-register.md) | 46-row ledger with DB metadata |
| [`references/archive/CRYPTO-bodies-full-dump.txt`](references/archive/CRYPTO-bodies-full-dump.txt) | All 46 bodies verbatim (quote anchor) |
| [`references/archive/classes.json`](references/archive/classes.json) | Frozen id → module map |

## Scoreboard (top paid rows)

| Case | Title (short) | Program | Bounty |
|---|---|---|---|
| CRYPTO-728110 | CVE-2018-2879 padding oracle (Oracle OAM) | deptofdefense | **$3,000** |
| CRYPTO-168538 | Twitter iOS fails cert validation, sends OAuth token | x | **$2,100** |
| CRYPTO-2038484 | Node `DiffieHellman` doesn't regenerate after `setPrivateKey` | ibb | **$1,800** |
| CRYPTO-213437 | JWE invalid-curve attack (4 libraries) | ibb | **$1,000** |
| CRYPTO-144782 | Python `smtplib` STARTTLS stripping | ibb | **$1,000** |
| CRYPTO-1178562 | Ruby `net/imap` STARTTLS stripping | ruby | $500 |
| CRYPTO-126203 | CBC cut-and-paste → open redirect/XSS | uber | $500 |
| CRYPTO-327674 | Slack invitation reminders over HTTP | slack | $350 |
| CRYPTO-903424 | Nextcloud desktop doesn't validate cert | nextcloud | $300 |
| CRYPTO-435648 | TOTP secret below RFC 4226 minimum | phabricator | $300 |

## Cross-vault links

- `../18_Misconfiguration/` — header/HSTS/cookie hygiene overlaps module 03.
- `../14_HTTP-Request-Smuggling/` — protocol-injection mechanics behind module 01.
- `../Race-Conditions/Library-Timing-Adjacent.md` — timing oracles.
- `../Authentication-Session/` — what a broken session secret enables.

## Limitations

1. **Bucket size 26**; the vault's headline money ($43,400) sits in the **merge pool**, which is
   mostly GitHub-Security-Lab CodeQL/CWE rows — labeled as such, not counted as class prose.
2. **Bounty `-` ≠ unpaid** (10 rows without figures in the bucket).
3. **Era drift**: DROWN/POODLE/STARTTLS-stripping are 2014–2021 rows; modern stacks default to
   TLS-only transports, so retest rather than cite.
4. **Construction classes are the durable part** — length extension, CBC without MAC, reusable
   signatures, and missing cert validation still ship today.
5. **No live testing** in this build; everything traces to archived bodies.
6. **Do not submit "weak cipher suite" reports** unless the program's VRT prices them (see §5 of
   module 01).
7. **Quotes** byte-verified against the archive; `(sic)` marks author typos.


<!-- CASESTOCK-LINK:BEGIN -->

## Case stock — vault (`_VAULT/`)

**390 disclosed reports** routed to this category · 59 with a bounty figure · **$65,118** · 288 full write-ups stored locally.

- Full list: [`_VAULT/by-vault-category/19_Cryptography.md`](../_VAULT/by-vault-category/19_Cryptography.md)
- Query: `sqlite3 ../_VAULT/reports.sqlite "SELECT id,bounty,title FROM reports WHERE ..."`
- Pull one write-up: `python3 ../_VAULT/scripts/extract_report.py <id>`

| Top paid | Program | Bounty |
|---|---|---|
| [1301753](https://hackerone.com/reports/1301753) Java: Timing attacks while comparing results of cryptographic operations | GitHub Security Lab | $4,500 |
| [1219493](https://hackerone.com/reports/1219493) [Java] CWE-295 - Incorrect Hostname Verification - MitM | GitHub Security Lab | $4,000 |
| [1888803](https://hackerone.com/reports/1888803) Use of Cryptographically Weak Pseudo-Random Number Generator in WebCrypto keygen | Internet Bug Bounty | $4,000 |
| [2435482](https://hackerone.com/reports/2435482) CVE-2024-2466: TLS certificate check bypass with mbedTLS (reward request) | Internet Bug Bounty | $2,580 |
| [113288](https://hackerone.com/reports/113288) OpenSSL Key Recovery Attack on DH small subgroups (CVE-2016-0701)  | Internet Bug Bounty | $2,500 |

_refreshed 2026-11-17 from the public HackerOne disclosed-report dataset_
<!-- CASESTOCK-LINK:END -->
