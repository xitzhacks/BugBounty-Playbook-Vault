---
title: "Vault/_VAULT — the disclosed-report dataset behind the playbooks"
type: index
built: "2026-11-17"
rows: 15244
paid_rows: 3241
bounty_sum: 4,934,915
full_bodies_available: 9875
source: "public HackerOne disclosed-vault, harvested 2026-11-17"
---

# Vault/_VAULT — the full vault

Every publicly disclosed HackerOne report exposed by the public HackerOne dataset, harvested 2026-11-17:
**15,244 reports · 3,241 with a bounty figure · $4,934,915 · 9,875 with the full write-up stored.**

This is a *dataset layer*, not a playbook. The playbooks (`Vault/XXE/`, `Vault/RCE/`, …) stay the
teaching layer; this directory is the case stock you can query, sort and cite.

## Write-up availability (reconciled against `hackerone.com/reports/<id>.json`, 2026-11-17)

| State | Rows | Meaning |
|---|---|---|
| Full write-up stored | 9,875 | `bodies.body` holds the researcher's own write-up |
| Summary only | 2,647 | HackerOne published the program summary; the researcher left the body blank |
| Delisted (404) | 2,722 | Report no longer public on HackerOne — title/bounty kept from the list, body never quoted |
| Other status | 0 | fetch never resolved; not quoted |

15,244 rows accounted for = the full list. Stored write-up text: 101 MB.
Nothing is invented: a row without a body is shown as such, and a 404 is never paraphrased.

## Files

| File | What it is |
|---|---|
| [`all-reports.csv`](all-reports.csv) | Every report, one row: id, title, program, severity, weakness, class, routed vault category, bounty, votes, reporter, disclosed date, substate, has_body |
| [`reports.sqlite`](reports.sqlite) | Tables `reports` (metadata, 15,244 rows) and `bodies` (summary + full write-up + asset + CVEs). Generated locally — see note below. |
| `by-class/NN_<CLASS>.md` | All reports of one class, richest first |
| `by-vault-category/<dir>.md` | The same reports routed into our playbook directories |
| [`scripts/extract_report.py`](scripts/extract_report.py) | `python3 extract_report.py 510152` → writes that report's full write-up as markdown |
| table `documents` | Full text of every markdown document we wrote in this vault (playbooks, modules, registers, views), with title/type/category/sha256 + FTS5 index |
| table `documents_fts` | Full-text search over those documents |
| `scripts/refresh.sh` | Re-run the two harvesters and rebuild these views |

> **Fresh clone:** `reports.sqlite` is **not committed** — the repo ships
> `reports.sqlite.part-*` plus `reports.sqlite.sha256` because of GitHub's file-size
> limit. Run `bash tools/join_db.sh` from the repository root to rejoin and verify it.
> The root `README.md` has the complete setup and usage guide.

## Skills layer

Every skill in this profile is mirrored to `_VAULT/skills/` and indexed in `documents` (dir=`skills`),
so one hybrid query reaches doctrine and evidence together.

| Fact | Value |
|---|---|
| skills mirrored | 209 skills (SKILL.md + references/templates/scripts) |
| skill markdown indexed | 3,194 docs (identical copies stored once) |
| scoping | `search.py --source skills` (doctrine) · `--source vault` (playbooks + reports) |

```bash
sqlite3 reports.sqlite "SELECT dir,COUNT(*) FROM documents GROUP BY 1 ORDER BY 2 DESC LIMIT 5;"
```

## Bypass + technique indexes

| Table | Rows | What it answers |
|---|---|---|
| `techniques` | 1,409 | class → named technique → passage (`vault_techniques`, `techniques.py`) |
| `bypasses` | 8,739 | protection → passage → payload (`vault_bypass`, `bypass.py`) · 1,371 rows carry a literal payload |
| `payloads` | 19,278 | 19,278 unique fenced code blocks, classified + deduped (`vault_payloads`, `payload.py`) |

```bash
python3 techniques.py LFI --grep filter      # named techniques for a class
python3 bypass.py waf --grep cloudflare      # who got past a WAF, and with what
python3 bypass.py csp --show 42              # full passage + payloads
```
Tags: waf · csp · twofa · rate_limit · allowlist · sanitizer · earlier_fix · cors · authz

## Query recipes

```bash
sqlite3 reports.sqlite "SELECT id,program,bounty,title FROM reports WHERE weakness LIKE '%SQL injection%' AND bounty>0 ORDER BY bounty DESC LIMIT 20;"
sqlite3 reports.sqlite "SELECT id,title FROM bodies WHERE body LIKE '%X-Forwarded-Host%' LIMIT 20;"
sqlite3 reports.sqlite "SELECT program,COUNT(*),SUM(bounty) FROM reports GROUP BY 1 ORDER BY 3 DESC LIMIT 20;"
sqlite3 reports.sqlite "SELECT id,title,substr(body,1,600) FROM bodies WHERE body LIKE '%WAF%bypass%' LIMIT 5;"
sqlite3 reports.sqlite "SELECT path,title FROM documents_fts WHERE documents_fts MATCH 'cache poisoning' LIMIT 10;"
sqlite3 reports.sqlite "SELECT dir,COUNT(*) FROM documents GROUP BY 1 ORDER BY 2 DESC;"
```

## Coverage by class

| Class | Name | Rows | Bounties | View | Playbook |
|---|---|---|---|---|---|
| XSS | Cross-site Scripting | 2587 | $555,389 | `by-class/` | `Vault/XSS/` |
| INFO | Information Disclosure | 1997 | $461,179 | `by-class/` | `Vault/16_Information-Disclosure/` |
| ACL | Access Control | 1498 | $567,225 | `by-class/` | `Vault/17_Privilege-Escalation/` |
| AUTH | Authentication | 1367 | $417,288 | `by-class/` | `Vault/Authentication-Session/` |
| CONF | Misconfiguration | 1265 | $117,847 | `by-class/` | `Vault/18_Misconfiguration/` |
| MEM | Memory Corruption | 917 | $472,258 | `by-class/` | `Vault/30_Memory-Corruption/` |
| RCE | Code Execution | 843 | $624,658 | `by-class/` | `Vault/RCE/` |
| DOS | Denial of Service | 637 | $331,820 | `by-class/` | `Vault/21_Denial-of-Service/` |
| OTHER | Other weaknesses | 629 | $206,452 | `by-class/` | `Vault/-` |
| CSRF | Cross-Site Request Forgery | 530 | $69,078 | `by-class/` | `Vault/CSRF/` |
| LOGIC | Business Logic | 490 | $143,609 | `by-class/` | `Vault/12_Business-Logic/` |
| CRYPTO | Cryptography | 406 | $68,808 | `by-class/` | `Vault/19_Cryptography/` |
| INJ | Injection and Smuggling | 389 | $172,582 | `by-class/` | `Vault/XXE/` |
| IDOR | Insecure Direct Object Reference | 373 | $186,488 | `by-class/` | `Vault/IDOR/` |
| REDIR | Open Redirect | 357 | $32,524 | `by-class/` | `Vault/Open-Redirect/` |
| SQLI | SQL Injection | 332 | $184,652 | `by-class/` | `Vault/SQLi/` |
| SSRF | Server-Side Request Forgery | 330 | $178,559 | `by-class/` | `Vault/SSRF/` |
| TRAV | Path Traversal | 297 | $144,499 | `by-class/` | `Vault/File-Upload/` |

## Routed into our playbook categories

| Vault dir | Rows | Bounties | View |
|---|---|---|---|
| `XSS/` | 2528 | $540,043 | [`by-vault-category/XSS.md`](by-vault-category/XSS.md) |
| `16_Information-Disclosure/` | 2483 | $614,744 | [`by-vault-category/16_Information-Disclosure.md`](by-vault-category/16_Information-Disclosure.md) |
| `17_Privilege-Escalation/` | 1336 | $518,575 | [`by-vault-category/17_Privilege-Escalation.md`](by-vault-category/17_Privilege-Escalation.md) |
| `Authentication-Session/` | 1096 | $376,558 | [`by-vault-category/Authentication-Session.md`](by-vault-category/Authentication-Session.md) |
| `18_Misconfiguration/` | 948 | $89,637 | [`by-vault-category/18_Misconfiguration.md`](by-vault-category/18_Misconfiguration.md) |
| `30_Memory-Corruption/` | 898 | $467,758 | [`by-vault-category/30_Memory-Corruption.md`](by-vault-category/30_Memory-Corruption.md) |
| `RCE/` | 803 | $588,438 | [`by-vault-category/RCE.md`](by-vault-category/RCE.md) |
| `21_Denial-of-Service/` | 578 | $310,610 | [`by-vault-category/21_Denial-of-Service.md`](by-vault-category/21_Denial-of-Service.md) |
| `CSRF/` | 516 | $60,528 | [`by-vault-category/CSRF.md`](by-vault-category/CSRF.md) |
| `19_Cryptography/` | 390 | $65,118 | [`by-vault-category/19_Cryptography.md`](by-vault-category/19_Cryptography.md) |
| `12_Business-Logic/` | 360 | $104,913 | [`by-vault-category/12_Business-Logic.md`](by-vault-category/12_Business-Logic.md) |
| `IDOR/` | 360 | $167,988 | [`by-vault-category/IDOR.md`](by-vault-category/IDOR.md) |
| `20_Rate-Limiting/` | 342 | $39,800 | [`by-vault-category/20_Rate-Limiting.md`](by-vault-category/20_Rate-Limiting.md) |
| `Open-Redirect/` | 340 | $32,194 | [`by-vault-category/Open-Redirect.md`](by-vault-category/Open-Redirect.md) |
| `SQLi/` | 327 | $184,502 | [`by-vault-category/SQLi.md`](by-vault-category/SQLi.md) |
| `SSRF/` | 324 | $175,059 | [`by-vault-category/SSRF.md`](by-vault-category/SSRF.md) |
| `File-Upload/` | 284 | $139,574 | [`by-vault-category/File-Upload.md`](by-vault-category/File-Upload.md) |
| `14_HTTP-Request-Smuggling/` | 214 | $118,670 | [`by-vault-category/14_HTTP-Request-Smuggling.md`](by-vault-category/14_HTTP-Request-Smuggling.md) |
| `13_Subdomain-Takeover/` | 209 | $15,040 | [`by-vault-category/13_Subdomain-Takeover.md`](by-vault-category/13_Subdomain-Takeover.md) |
| `XXE/` | 199 | $59,092 | [`by-vault-category/XXE.md`](by-vault-category/XXE.md) |
| `28_Mobile/` | 185 | $75,830 | [`by-vault-category/28_Mobile.md`](by-vault-category/28_Mobile.md) |
| `29_Clickjacking/` | 165 | $10,640 | [`by-vault-category/29_Clickjacking.md`](by-vault-category/29_Clickjacking.md) |
| `Race-Conditions/` | 95 | $37,946 | [`by-vault-category/Race-Conditions.md`](by-vault-category/Race-Conditions.md) |
| `22_GraphQL/` | 78 | $89,172 | [`by-vault-category/22_GraphQL.md`](by-vault-category/22_GraphQL.md) |
| `15_Cache-Poisoning/` | 62 | $24,306 | [`by-vault-category/15_Cache-Poisoning.md`](by-vault-category/15_Cache-Poisoning.md) |
| `25_Prototype-Pollution/` | 52 | $6,000 | [`by-vault-category/25_Prototype-Pollution.md`](by-vault-category/25_Prototype-Pollution.md) |
| `24_Host-Header-Injection/` | 39 | $1,580 | [`by-vault-category/24_Host-Header-Injection.md`](by-vault-category/24_Host-Header-Injection.md) |
| `23_LDAP-XPath-Injection/` | 24 | $19,000 | [`by-vault-category/23_LDAP-XPath-Injection.md`](by-vault-category/23_LDAP-XPath-Injection.md) |
| `27_LLM-AI/` | 6 | $1,600 | [`by-vault-category/27_LLM-AI.md`](by-vault-category/27_LLM-AI.md) |
| `26_Web3-Smart-Contract/` | 3 | $0 | [`by-vault-category/26_Web3-Smart-Contract.md`](by-vault-category/26_Web3-Smart-Contract.md) |

## Provenance & honesty

- Source is the public unauthenticated endpoints: `the public HackerOne dataset/api/reports` (the list) and
  `hackerone.com/reports/<id>.json` (the write-ups). No private data, no API key.
- Bounty figures are HackerOne's `bounty_amount`; a blank means no figure was shown, **not** that nothing was paid.
- Titles come from the program's published report. Severity/weakness are the program's own fields where set;
  where a program set no weakness the class is inferred from the title by their published rules —
  treat those as a keyword guess, not a fact.
- The repo (`~/Bugbounty/vault/the public HackerOne dataset`) pins `next@16.4.6`; the site is the reference
  implementation of the same idea as this vault: reports → class → playbook.
