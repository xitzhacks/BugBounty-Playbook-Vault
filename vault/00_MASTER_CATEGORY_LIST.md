# MASTER VULNERABILITY CATEGORY LIST — PLAYBOOK BUILD SEQUENCE

Sources: BugBountyHunter disclosed stats (14,473 disclosed / $8.3M paid), h1.security.nathan.sx (4,419 reports / $2.03M paid), bugbountyhunting.com community writeups.

> Rule: we build ONE playbook per category, sequence-wise. Each playbook = entry-point mapping → methodology → payload arsenal → bypasses → disclosed report case studies → chains → validation gates → report template.

## CASE-STOCK DATASET LAYER

Alongside the playbooks sits `_VAULT/` — the full disclosed-vault built from the public HackerOne
disclosed-report dataset: **15,244 reports · 3,241 with a bounty figure · $4.93M ·
9,875 full write-ups stored (101 MB) · 2,647 summary-only · 2,722 delisted (404, never quoted)**.
It is the queryable case stock behind every playbook.

- `_VAULT/README.md` — provenance, counts, query recipes
- `_VAULT/all-reports.csv` — every report: id, title, program, severity, weakness, class, bounty, votes, date, has_body
- `_VAULT/reports.sqlite` — tables `reports` (metadata) + `bodies` (summary, full write-up, asset, CVEs)
- `_VAULT/by-class/NN_<CLASS>.md` — all rows of one class, richest first
- `_VAULT/by-vault-category/<dir>.md` — the same rows routed into the playbook dirs below
- `_VAULT/scripts/extract_report.py <id>` — dump one write-up as markdown

Per-directory case counts (rows · bounties) are listed in `_VAULT/README.md`; when a playbook
module cites a case, pull the verbatim body with `extract_report.py` rather than trusting a title.

## BUILD SEQUENCE (playbook status)

| # | Playbook Category | H1 Disclosed Count | Status |
|---|---|---|---|
| 1 | **XXE / XML Injection (all XML types)** — XXE, blind/OOB XXE, SOAP XXE, SAML XXE, SVG/DOCX/XLSX/PPTX XXE, error-based XXE, billion laughs, XML-RPC, XSLT, XInclude | 34 XXE + 3 XML Injection + 2 XML Entity Expansion | ✅ **DONE** → `XXE/` (README + Agent Playbook + 5 class modules + references; built 2026-10-27) |
| 2 | SQL Injection (incl. blind, NoSQL, ORM raw) | 318 + 70 input validation | ✅ exists → `SQLi/` (7 modules) |
| 3 | SSRF (incl. blind OOB, cloud metadata) | 278 | ✅ exists → `SSRF/` (7 modules) |
| 4 | XSS — Reflected / Stored / DOM / Blind | 978 + 621 + 589 + 167 | ✅ exists → `XSS/` (11 modules) |
| 5 | IDOR / Broken Access Control | 339 + 732 + 57 | ✅ exists → `IDOR/` (8 modules) |
| 6 | CSRF (incl. SameSite bypasses, login CSRF, JSON CSRF) | 488 | ✅ **DONE** → `CSRF/` (README + Agent Playbook + 7 class modules + references; built 2026-10-28) |
| 7 | Open Redirect (+ OAuth redirect flows) | 342 | ✅ **DONE** → `Open-Redirect/` (README + Agent Playbook + 8 class modules + references; built 2026-10-29) |
| 8 | Authentication Bypass / Session (fixation, MFA bypass, insufficient expiry) | 771 + 63 + 40 + 22 + 16 | ✅ **DONE** → `Authentication-Session/` (README + Agent Playbook + 8 class modules + references; built 2026-10-29) |
| 9 | RCE — Command Injection, Code Injection, Deserialization | 333 + 233 + 70 + 52 | ✅ **DONE** → `RCE/` (README + Agent Playbook + 9 class modules + references; built 2026-11-05) |
| 10 | File Upload / Path Traversal / LFI-RFI | 236 + 14 + 19 + 12 | ✅ **DONE** → `File-Upload/` (README + Agent Playbook + 9 class modules + references; built 2026-11-05) |
| 11 | Race Conditions / TOCTOU | 18 + 19 | ✅ **DONE** → `Race-Conditions/` (README + Agent Playbook + 6 class modules + references; 26 rows · $43,260; built 2026-11-07) |
| 12 | Business Logic (payment, coupons, logic flaws) | 378 | ✅ **DONE** → `12_Business-Logic/` (5 modules; 127 rows · $60,090) |
| 13 | Subdomain Takeover | 12 externally-controlled reference + DNS class | ✅ **DONE** → `13_Subdomain-Takeover/` (4 modules; 26 rows · $4,565) |
| 14 | HTTP Request Smuggling / Response Splitting / CRLF | 76 + 18 + 64 | ✅ **DONE** → `14_HTTP-Request-Smuggling/` (4 modules; 48 rows · $41,190) |
| 15 | Cache Poisoning / Web Cache Deception | 4 + 34 WCD-class | ✅ **DONE** → `15_Cache-Poisoning/` (3 modules; 15 rows · $6,506) |
| 16 | Information Disclosure (error messages, directory listing, debug, git/.env) | 1378 + 39 + 35 + 29 | ✅ **DONE** → `16_Information-Disclosure/` (6 modules; 362 rows · $281,925) |
| 17 | Privilege Escalation (app-level) | 460 | ✅ **DONE** → `17_Privilege-Escalation/` (5 modules; 172 rows · $106,265) |
| 18 | Misconfiguration (headers, TLS, CORS, methods, cookies) | 83 + 187 secure-design | ✅ **DONE** → `18_Misconfiguration/` (6 modules; 166 rows · $34,682) |
| 19 | Cryptography Issues (weak algo, padding oracles, JWT) | 187 + 14 + 11 | ✅ **DONE** → `19_Cryptography/` (4 modules; 46 rows · $55,105) |
| 20 | Rate Limiting / Brute Force / User Enumeration | 51 + 63 | ✅ **DONE** → `20_Rate-Limiting/` (4 modules; 64 rows · $19,105) |
| 21 | DoS / Resource Exhaustion (incl. decompression bombs) | 315 + 215 + 29 | ✅ **DONE** → `21_Denial-of-Service/` (5 modules; 240 rows · $275,868) |
| 22 | GraphQL / API-specific bugs | API class | ✅ **DONE** → `22_GraphQL/` (3 modules + merge; 19 rows · $58,340) |
| 23 | LDAP Injection / XPath Injection | 5 + XML class | ✅ **DONE** → `23_LDAP-XPath-Injection/` (corpus block; 12 rows · $19,000 — metadata-only) |
| 24 | Host Header Injection / Password Reset Poisoning | ATO chain class | ✅ **DONE** → `24_Host-Header-Injection/` (1 module; 4 rows · $800) |
| 25 | Prototype Pollution (client + server) | npm class | ✅ **DONE** → `25_Prototype-Pollution/` (1 module; 4 rows · $6,000) |
| 26 | Web3 / Smart Contract | NEW section | ✅ **DONE** → `26_Web3-Smart-Contract/` (1 module; 2 rows · $1,000) |
| 27 | LLM/AI (prompt injection, LLM01-06) | 5 + 3 + 1 + 1 | ✅ **DONE** → `27_LLM-AI/` (1 module; 1 row · $2,500) |
| 28 | Mobile (Android/iOS) | mobile class | ✅ **DONE** → `28_Mobile/` (2 modules; 13 rows · $6,310) |
| 29 | Clickjacking / UI Redressing | 131 | ✅ **DONE** → `29_Clickjacking/` (3 modules; 23 rows · $8,460) |
| 30 | Memory Corruption (buffer/heap/UAF — mostly IBB, low priority for web) | 319 + 70 + 54 | ✅ **DONE** → `30_Memory-Corruption/` (6 modules; 352 rows · $250,652) |

## PRIORITY RATIONALE

1. XXE first (your pick): highest per-report payouts in the H1 mirror range $700–$10,080; reconciled corpus total $50,227 across 44 rows ($29,367 in core XXE rows) — see `XXE/references/case-register.md`; it chains into SSRF + LFI + RCE + ATO.
2. Injection family next (SQLi, RCE) — classic Critical payers.
3. SSRF — pairs directly with XXE OOB infrastructure we already built.
4. XSS/access-control — highest volume = most finds.
5. Infra/config classes last — usually Info/Low unless chained.
