---
title: "Cache Poisoning case register — 15-row ledger (h1-brain corpus)"
type: register
built: "2026-11-07"
corpus: "h1-brain disclosed_reports.db (3,673 rows; sha256 8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4)"
case_id_scheme: "CACHE-<HackerOne report id>"
bounty_rule: "DB bounty_amount where present · '-' = no figure in DB (not evidence of non-payment)"
module_rule: "frozen in archive/classes.json"
---

# Case register — Cache Poisoning / Web Cache Deception

Corpus: 15 rows · 6 with bounty figures · **$6,506** · all 15 full-body.

Module census: 01 unkeyed-header-reflection 7 · 02 cache-deception-and-key-manipulation 3 · 03 cache-implementation-and-path-tricks 5.

| Case | Program | Bounty | Module | CVE | Title |
|---|---|---|---|---|---|
| [CACHE-84601](https://hackerone.com/reports/84601) | x | - | cache-implementation-path-manifest | - | XSS and cache poisoning via upload.twitter.com on ton.twitter.com |
| [CACHE-260697](https://hackerone.com/reports/260697) | discourse | - | cache-deception-key | - | CSRF-tokens on pages without no-cache headers, resulting in ATO when using Clo |
| [CACHE-303730](https://hackerone.com/reports/303730) | gsa_bbp | $750 | unkeyed-header-reflection | - | Defacement of catalog.data.gov via web cache poisoning to stored DOMXSS |
| [CACHE-334709](https://hackerone.com/reports/334709) | greenhouse | - | cache-implementation-path-manifest | - | Cache poisoning using NULL bytes and long URLs |
| [CACHE-394016](https://hackerone.com/reports/394016) | discourse | $256 | unkeyed-header-reflection | - | Web Cache Deception Attack (XSS) |
| [CACHE-824753](https://hackerone.com/reports/824753) | ibb | - | cache-implementation-path-manifest | CVE-2019-12520, CVE-2019-12524 | Cache Poisoning |
| [CACHE-977851](https://hackerone.com/reports/977851) | shopify | $1,000 | unkeyed-header-reflection | - | Cache poisoning via X-Forwarded-Host in www.shopify.com/partners/blog |
| [CACHE-1374512](https://hackerone.com/reports/1374512) | ibb | - | unkeyed-header-reflection | CVE-2021-22942 | The Host Authorization middleware in Action Pack is vulnerable to crafted X-Fo |
| [CACHE-1392935](https://hackerone.com/reports/1392935) | omise | $200 | unkeyed-header-reflection | - | XSS via X-Forwarded-Host header |
| [CACHE-1695604](https://hackerone.com/reports/1695604) | shopify | $3,800 | cache-implementation-path-manifest | - | DoS Vulnerability via Cache Poisoning on cdn.shopify.com and shopify-assets.sh |
| [CACHE-1698316](https://hackerone.com/reports/1698316) | expediagroup_bbp | - | cache-deception-key | - | Cache Deception Allows Account Takeover |
| [CACHE-1760213](https://hackerone.com/reports/1760213) | expediagroup_bbp | - | cache-deception-key | - | Cache Poisoning Allows Stored XSS Via hav Cookie Parameter (To Account Takeove |
| [CACHE-1795197](https://hackerone.com/reports/1795197) | glassdoor | - | unkeyed-header-reflection | - | Cache Poisoning allows redirection on JS files |
| [CACHE-1848940](https://hackerone.com/reports/1848940) | shopify | $500 | cache-implementation-path-manifest | - | URL Path Manipulation Enables Cache Poisoning of Amazon Affiliate Products in  |
| [CACHE-2917062](https://hackerone.com/reports/2917062) | trendyol | - | unkeyed-header-reflection | - | Cache Poisoning Allows Zero Interaction Store XSS |

Module totals: 01 $2,206/3 · 03 $4,300/2 · 02 $0/0 recorded.

Bounty arithmetic: 3,800 + 1,000 + 750 + 500 + 256 + 200 = **$6,506** (6 rows).
