---
title: "Vault/18_Misconfiguration — exposure, dangling pointers, identity flows, headers, spoofing"
type: index
category: misconfiguration (subdomain takeover & dangling state; account verification & rate limiting; headers/TLS/transport; exposure/API/secrets/config; spoofing/phishing/homograph/open-redirect; adjacent+merges)
built: "2026-11-07"
evidence: "166 rows (152 classified misconfig bucket + 14 unclassified merges) from h1-brain DB (sha256 8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4) — 166 bodies read (147 substantive / 19 corpus-metadata rows: 2 curl HSTS 78-byte pointers, 1 algolia 100-byte claim, 10 GHSL 54-byte one-liners, ~6 short stubs: 100–200 bytes). No live H1 fetch this build."
bounty: "$34,532 vault total (bucket $25,932/38 + merges $8,600/9) · max $6,300 (MISCONF-1258871 exposed Cortex API) · next $3,750 (MISCONF-815085 %/%0d%0a account creation) · 47 paid rows. Full arithmetic in references/case-register.md."
companion_vaults: "13_Subdomain-Takeover · 14_HTTP-Request-Smuggling · 15_Cache-Poisoning · 16_Information-Disclosure · 19_Cryptography · 20_Rate-Limiting · Open-Redirect · Race-Conditions"
case_id_scheme: "MISCONF-<HackerOne report id>"
quote_rule: "byte-true, (sic)-marked, from read bodies only; GHSL one-liners and short CVE pointers recorded never quoted as technique"
---

# Vault/18_Misconfiguration — the six-module playbook set

`Need a name? Need a token? Need a trust anchor?` In this corpus the money sits in three URLs: an **exposed Cortex API** (MISCONF-1258871, $6,300), a **signup field that accepts `%0d%0a`** (MISCONF-815085, $3,750), and an **orphaned Fastly CNAME** (MISCONF-154425, $3,000). Everything else in the vault is the discipline that surrounds those three: proving a pointer is dangling, ordering a rate limit before its oracle, and never confusing a present header for a policy.

## Start here

| # | File | What it gives you |
|---|---|---|
| 1 | [`MISCONF-Testing-Agent-Playbook.md`](MISCONF-Testing-Agent-Playbook.md) | **The executable protocol.** P0 trust-surface read → P1 misconfig inventory (pointers, identity, headers, exposure, rendering) → P2 probe ladder (claim → flow-order → downgrade → shadow-diff → deception → boundary) → P3 proof ladder with read-backs → P4 hardening fingerprints → P5 kill-gates. |
| 2 | [`01_Subdomain-Takeover-and-Dangling-State.md`](01_Subdomain-Takeover-and-Dangling-State.md) | The abandoned pointer: Fastly/Heroku/Vercel/GSuite, UserVoice, Modulus, Instapage, plus S3-origin and repo-link takeovers. Anchors: MISCONF-154425 (Fastly $3,000), MISCONF-2706358/2899858 (Mozilla $500 pair), MISCONF-2262939 (rubygems S3 origin), MISCONF-2011298 (veneur.org). |
| 3 | [`02_Account-Verification-and-Rate-Limiting.md`](02_Account-Verification-and-Rate-Limiting.md) | Identity controls checked late or never: verification skips, token possession, SSO backdoor, 2FA downgrade, rate-limit ordering/scope/expiry, OTP/lockout, flood economics. Anchors: MISCONF-815085 ($3,750), MISCONF-57764 ($100), MISCONF-262830 (ordering), MISCONF-170310 (scope reset). |
| 4 | [`03_Headers-TLS-and-Transport-Misconfig.md`](03_Headers-TLS-and-Transport-Misconfig.md) | The downgrade is the vuln: cache deception ($800), semantic protocol-policy bypass ($560), privileged-scheme header ($400), sslstrip login ($350), emailed password ($200), $1 cipher inventory. Plus CSP/CORS/referrer discipline and the curl HSTS set. |
| 5 | [`04_Exposure-API-Secrets-and-Config.md`](04_Exposure-API-Secrets-and-Config.md) | The money module ($14,521/19): unauth Cortex+pprof ($6,300), visibility bypass ($1,370), forced-POST ($1,050), support-channel identity binding, secrets placement, notification/session lifecycles, broken-link hijacks — and the Tor defensive-review negative example. |
| 6 | [`05_Spoofing-Phishing-Homograph-and-Open-Redirect.md`](05_Spoofing-Phishing-Homograph-and-Open-Redirect.md) | Captured trust displays: Host-header shortener ($300), trailing-dot blocklist bypass ($250), address-bar spoof ($200), error-page reflection ($100), breadcrumb spoof ($50); Brave fix-bypass curriculum; punycode doctrine. |
| 7 | [`06_Adjacent-and-Unclassified-Merges.md`](06_Adjacent-and-Unclassified-Merges.md) | The negative-space + sweep queue: 10 bucket-adjacent rows (race/traversal/XSS/RCE/CSRF/logic bodies under a misconfig label) and 14 unclassified merges (4 substantive incl. $1,500 2FA removal + $550 CORS; 10 GHSL 54-byte one-liners, $5,550, metadata-only). |

## References (provenance layer)

| File | Contents |
|---|---|
| [`references/source-index.md`](references/source-index.md) | Roster provenance (h1-brain DB, sha256, 3,673 rows), classifier bucket (152) + merge surface (14), funnel to 166, bounty accounting, era discipline, 5 limits. |
| [`references/case-register.md`](references/case-register.md) | Row-per-row ledger: 152-row bucket table (team, src/weakness, asset, CVE, bounty, module) + 14-row merge bridge ledger; bounty arithmetic; 16 CVE rows. |
| [`references/archive/MISCONF-bodies-full-dump.txt`](references/archive/MISCONF-bodies-full-dump.txt) | All 166 bodies verbatim (anchor for every quote). |
| [`references/archive/classes.json`](references/archive/classes.json) | Frozen 166-row module assignment (case id → module slug). |
| [`references/archive/meta.json`](references/archive/meta.json) | Build metadata. |

## Scoreboard (166 rows · 47 paid · $34,532 · max $6,300)

| Case | Title (short) | Program | Bounty | CVE |
|---|---|---|---|---|
| MISCONF-1258871 | Unauth Cortex + pprof exposed | shopify | **$6,300** (max) | — |
| MISCONF-815085 | `%`/`%0d%0a` in email → mass accounts | security | **$3,750** | — |
| MISCONF-154425 | Dangling Fastly CNAME reclaimed | snapchat | **$3,000** | — |
| MISCONF-909374 | Directory listing (GHSL query) | github-security-lab | $1,800 | — |
| MISCONF-178293 | Sign-in-with-Google kills 2FA | shopify | $1,500 | — |
| MISCONF-1086781 | API bypasses visibility restriction | gitlab | $1,370 | — |
| MISCONF-837328 | WebSocket forces victim POST | quantopian | $1,050 | — |
| MISCONF-1626205 | Exposed setup-config → WP takeover | deptofdefense | $1,000 | — |
| MISCONF-2001913 | Email-to-ticket binds victim account | security | $1,000 | — |
| MISCONF-956967 | Hardcoded AWS credentials (GHSL) | github-security-lab | $1,000 | — |
| MISCONF-1165198 | Cookie HttpOnly query, Java (GHSL) | github-security-lab | $1,000 | — |
| MISCONF-1241576 | Cookie HttpOnly query, Go (GHSL) | github-security-lab | $1,000 | — |
| MISCONF-1241577 | Cookie HttpOnly query, JS (GHSL) | github-security-lab | $1,000 | — |
| MISCONF-1271944 | Cache deception → PII + CSRF | shopify | $800 | — |
| MISCONF-1213181 | Metalink credential leak | curl | $700 | CVE-2021-22923 |
| MISCONF-2437131 | Disabled protocol re-enabled | ibb | $560 | CVE-2024-2004 |
| MISCONF-426165 | CORS reflection + credentials | zomato | $550 | — |
| MISCONF-172289 | One-click integration → privileges | security | $500 | — |
| MISCONF-240083 | Payout change, no notification | security | $500 | — |
| MISCONF-297181 | referrer-policy leaks full URL | security | $500 | — |
| MISCONF-2166697 | GraphQL batching bulk reports | security | $500 | — |
| MISCONF-2706358 | Fastly domain claimed | mozilla | $500 | — |
| MISCONF-2899858 | CNAME claimed (firefox.com) | mozilla | $500 | — |
| MISCONF-1137966 | Spring Actuator query (GHSL) | github-security-lab | $500 | — |
| MISCONF-1089995 | Onion-Location opens chrome: URLs | brave | $400 | — |
| MISCONF-214571 | HTTP login page (sslstrip) | rockstargames | $350 | — |
| MISCONF-210875 | Host-header shortener → phishing | rockstargames | $300 | — |
| MISCONF-902970 | Insecure HSTS (GHSL) | github-security-lab | $250 | — |
| MISCONF-672623 | Username/token disclosure (Android) | nextcloud | $250 | CVE-2019-15611 |
| MISCONF-1068505 | Trailing dot defeats blocklist | brave | $250 | — |
| MISCONF-2337938 | Password emailed in cleartext | sheer_bbp | $200 | — |
| MISCONF-475098 | `dashboard.html` username shadows | gitlab | $200 | — |
| MISCONF-1188629 | LinkedIn link capturable | sifchain | $200 | — |
| MISCONF-175958 | Address-bar spoof | brave | $200 | CVE-2016-9473 |
| MISCONF-249319 | No API rate limit (DoS) | gsa_bbp | $150 | — |
| MISCONF-154827 | `dir` param breadcrumb spoof | nextcloud | $50 | CVE-2016-9467 |
| MISCONF-1454002 | Exported activity reads files | owncloud | $50 | — |
| MISCONF-57764 | Back-button skips verification | coinbase | $100 | — |
| MISCONF-246801 | Captcha bypass | coinbase | $100 | — |
| MISCONF-1202408 | Comment cap 1000/min | reddit | $100 | — |
| MISCONF-208480 | Subdomain site misconfigured | lyst | $100 | — |
| MISCONF-415272 | Binary not PIE | slack | $100 | — |
| MISCONF-1784162 | OAuth code never expires | nextcloud | $100 | CVE-2024-22403 |
| MISCONF-2501378 | URL eliding wrong | brave | $100 | CVE-2024-37406 |
| MISCONF-1245051 | Error page reflects path | basecamp | $100 | — |
| MISCONF-131065 | Weak ciphers inventory | gratipay | $1 | — |
| MISCONF-117739 | Image-count limit | gratipay | $1 | — |

## Vault map

| File | Content |
|---|---|
| `01_Subdomain-Takeover-and-Dangling-State.md` | Pointer-outlives-instance: DNS/CNAME/CDN, storage origins, repo links; claim mechanics + trust demo pricing |
| `02_Account-Verification-and-Rate-Limiting.md` | Registration/reporting enrollment controls: verification skips, OTP/lockout, rate-limit ordering/scope/expiry, flood economics |
| `03_Headers-TLS-and-Transport-Misconfig.md` | Downgrade doctrine: cache deception/poisoning, HSTS/CSP/CORS/referrer policy failures, sslstrip trilogy, credential transport |
| `04_Exposure-API-Secrets-and-Config.md` | Exposed operations planes, API shadow-diffs, secret placement, identity-binding failures, notification/session lifecycles, unclaimed namespaces |
| `05_Spoofing-Phishing-Homograph-and-Open-Redirect.md` | Captured-trust displays: IDN/punycode + fix bypasses, text injection, address-bar deception, open redirect, email spoof |
| `06_Adjacent-and-Unclassified-Merges.md` | Classification-drift exhibit (10 bodies that outvoted the label) + unclassified-merge sweep queue incl. GHSL one-liners |
| `MISCONF-Testing-Agent-Playbook.md` | P0–P5 executable protocol + module↔phase table + non-goals |
| `references/source-index.md` | Provenance, funnel, classification mechanics, 5 limits |
| `references/case-register.md` | 152-row bucket ledger + 14-row merge bridge; DB metadata, assets, CVEs |
| `references/archive/MISCONF-bodies-full-dump.txt` | All 166 bodies verbatim (quote anchor) |
| `references/archive/classes.json` | Frozen module assignment for all 166 rows |

## Cross-vault links

- `13_Subdomain-Takeover/` — module 01 is the misconfig-bucket slice; buckets are disjoint by construction (verified), so any overlap is prose cross-cite, not shared ids.
- `14_HTTP-Request-Smuggling/` — the CRLF pair (MISCONF-815085 ↔ MISCONF-164137) and header-splitting neighbors (MISCONF-806577, MISCONF-342693).
- `15_Cache-Poisoning/` — module 03's cache quartet (MISCONF-1271944, 631589, 1010858, 728664) is that vault's canon from the misconfig side.
- `16_Information-Disclosure/` — module 04's disclosure rows (Cortex, waitlist PII, `Referer` policy) are its Specimens.
- `19_Cryptography/` — module 04's MAC-ambiguity (661051) and token-lifetime (1784162) rows; HSTS/certificate behavior in module 03.
- `20_Rate-Limiting/` cross-cite — module 02 §4 + MISCONF-249319 (module 06) + MISCONF-2166697 (batching). The ordering/scope doctrine is this vault's closed-form contribution.
- `Open-Redirect/` — MISCONF-210875 and MISCONF-271324 are its specimens.
- `Race-Conditions/` — RACE-300305 (Shopify email-confirm race, $15,250) is module 02's verification-skip twin by TOCTOU; MISCONF-157996/165570 (module 06) are that vault's canon misclassified into this bucket.

## Limitations

1. **Labels are triage artifacts, and here they are useless.** 119/152 rows are labeled only by the catch-all "Violation of Secure Design Principles"; module 06's ten prove the label false from the bodies alone. The vault records the label verbatim and classifies by body — but nothing here should be filed from memory of the label.
2. **Figure absence is not non-payment.** 119/166 rows have no DB figure; only the $1 row is a *proven* same-bounty. The vault never calls a blank row "$0" unless stated in-body.
3. **Ten merges ($5,550) are telemetry without technique.** GHSL one-liners carry dollars and titles but no quotable text. Aggregated money without verbatim support is flagged wherever it appears (source-index §3) and never used as doctrine.
4. **Bucket overlaps at the seams.** The `misconfig-ssl-tls` module-map sibling (11 ids, see source-index §1) is a view over this vault; `13_Subdomain-Takeover`/`15_Cache-Poisoning`/etc. hold zero overlapping ids with this bucket but share doctrine in prose. Per-claim keep the id, not the intuition.
5. **Era drift within the vault.** 2014–2019-era rows (CSRF, RC4, 3DES, Flash `crossdomain.xml`) and 2022–2024 rows (curl CVE set, Nextcloud CVE set, Brave CVE-2024-37406, Mozilla VPN 2023) live side-by-side. Hardening expectations are stated per era in the playbook (P4) and are not back-applied to the corpus.
6. **Chain vs misconfig pricing.** The two biggest rows (index: $6,300 exposed API endpoint on a trusted domain, $3,750 registration/CRLF mass-account) pay because the misconfig hands a *trusted primitive*; pure hygiene (module 03's $1 same-bounty; module 05's breadcrumb $50) tops out at $100. Stay in the primitives.
7. **QA:** all block quotes in modules were byte-verified against `references/archive/MISCONF-bodies-full-dump.txt`; `(sic)` marks author typos. No invented quotes, no paraphrase passing as quotation. Every bucket id appears in exactly one module — verified (see report).


<!-- CASESTOCK-LINK:BEGIN -->

## Case stock — vault (`_VAULT/`)

**948 disclosed reports** routed to this category · 107 with a bounty figure · **$89,637** · 725 full write-ups stored locally.

- Full list: [`_VAULT/by-vault-category/18_Misconfiguration.md`](../_VAULT/by-vault-category/18_Misconfiguration.md)
- Query: `sqlite3 ../_VAULT/reports.sqlite "SELECT id,bounty,title FROM reports WHERE ..."`
- Pull one write-up: `python3 ../_VAULT/scripts/extract_report.py <id>`

| Top paid | Program | Bounty |
|---|---|---|
| [838635](https://hackerone.com/reports/838635) Spring Actuator endpoints publicly available and broken authentication | LY Corporation | $12,500 |
| [3113398](https://hackerone.com/reports/3113398) Internal Access to Hackerone confluence Docs | HackerOne | $12,500 |
| [1258871](https://hackerone.com/reports/1258871) Exposed Cortex API at https://cortex-ingest.shopifycloud.com/ | Shopify | $6,300 |
| [862589](https://hackerone.com/reports/862589) Spring Actuator endpoints publicly available, leading to account takeover | LY Corporation | $5,000 |
| [1428385](https://hackerone.com/reports/1428385) Send Fax from Anyone's HelloFax Account Due to Misconfigured Email Validation | Dropbox | $4,913 |

_refreshed 2026-11-17 from the public HackerOne disclosed-report dataset_
<!-- CASESTOCK-LINK:END -->
