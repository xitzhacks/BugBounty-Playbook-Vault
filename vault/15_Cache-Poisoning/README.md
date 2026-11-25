---
title: "Cache Poisoning & Web Cache Deception — the two directions of a poisoned cache"
type: index
category: "Cache Poisoning / Web Cache Deception (unkeyed header reflection · cache deception & key manipulation · implementation/path differentials)"
built: "2026-11-07"
evidence: "15 rows from h1-brain disclosed_reports.db (3,673 rows; sha256 8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4) · 15/15 full bodies read"
bounty: "$6,506 across 6 rows · module split: header reflection $2,206/3 · deception $0/0 recorded · path/implementation $4,300/2"
companion_vaults: "../24_Host-Header-Injection · ../16_Information-Disclosure · ../21_Denial-of-Service · ../XSS"
case_id_scheme: "CACHE-<HackerOne report id>"
quote_rule: "byte-true to references/archive/CACHE-bodies-full-dump.txt; (sic) marks author typos"
---

# Vault/Cache-Poisoning — poison the entry, or store the victim's page

Fifteen disclosed cases, one fork in the road: **poisoning** (attacker content reaches other
users) or **deception** (another user's content is stored where the attacker can read it).
The corpus pays the first far better — $3,800 for a CDN-wide 404, $1,000 for a blog link
swap — because the bounty tracks how many visitors are hit.

## Start here

| # | File | What it gives you |
|---|---|---|
| 1 | [`CACHE-Testing-Agent-Playbook.md`](CACHE-Testing-Agent-Playbook.md) | Executable protocol: cache-detection → key analysis → differential probes → poison/verify → kill-gates |
| 2 | [`01_Unkeyed-Header-Reflection.md`](01_Unkeyed-Header-Reflection.md) | `X-Forwarded-Host` / `X-Forwarded-Scheme` / `User-Agent` reflected into cached bodies and redirects — 7 rows, $2,206 |
| 3 | [`02_Cache-Deception-and-Key-Manipulation.md`](02_Cache-Deception-and-Key-Manipulation.md) | Session/CSRF-token pages without `no-cache` → ATO — 3 rows |
| 4 | [`03_Cache-Implementation-and-Path-Tricks.md`](03_Cache-Implementation-and-Path-Tricks.md) | Backslash, `%00`, traversal, Squid decode collision, AppCache — 5 rows, $4,300 |

## References (provenance layer)

| File | Contents |
|---|---|
| [`references/source-index.md`](references/source-index.md) | DB provenance, classification funnel, bounty accounting, era discipline, limitations |
| [`references/case-register.md`](references/case-register.md) | 15-row ledger with DB weakness/asset/CVE/bounty metadata |
| [`references/archive/CACHE-bodies-full-dump.txt`](references/archive/CACHE-bodies-full-dump.txt) | All 15 bodies verbatim (quote anchor) |
| [`references/archive/classes.json`](references/archive/classes.json) | Frozen id → module map |

## Scoreboard (15 rows · 6 paid · $6,506 · max $3,800)

| Case | Title (short) | Program | Bounty |
|---|---|---|---|
| CACHE-1695604 | DoS via cache poisoning: backslash→404 on cdn.shopify.com | shopify | **$3,800** (max) |
| CACHE-977851 | Cache poisoning via `X-Forwarded-Host` on partners blog | shopify | **$1,000** |
| CACHE-303730 | Defacement of catalog.data.gov → stored DOMXSS | gsa_bbp | **$750** |
| CACHE-1848940 | Linkpop Amazon product cache poisoning via path traversal | shopify | **$500** |
| CACHE-394016 | Web cache deception / XSS via `X-Forwarded-Host` (Discourse) | discourse | **$256** |
| CACHE-1392935 | XSS via `X-Forwarded-Host` | omise | **$200** |
| CACHE-1795197 | Poisoned redirect on `.js` files (Glassdoor) | glassdoor | - |
| CACHE-2917062 | Zero-interaction store XSS via `User-Agent` | trendyol | - |
| CACHE-1698316 | Cache deception → session → ATO (Abritel) | expediagroup_bbp | - |
| CACHE-260697 | CSRF-token pages cacheable behind CloudFlare | discourse | - |
| CACHE-1760213 | `hav` cookie → cached stored XSS → ATO | expediagroup_bbp | - |
| CACHE-824753 | Squid URL-decode cache collision (CVE-2019-12520) | ibb | - |
| CACHE-334709 | NULL bytes + long URLs in Greenhouse embed | greenhouse | - |
| CACHE-84601 | Unknown-extension upload → AppCache poisoning | x | - |
| CACHE-1374512 | Rails Host Authorization case-variance (CVE-2021-22942) | ibb | - |

## Cross-vault links

- `../24_Host-Header-Injection/` — the same headers, uncached sinks (reset poisoning, redirect).
- `../16_Information-Disclosure/` — deception rows read as data exposure.
- `../21_Denial-of-Service/` — CACHE-1695604 is a DoS delivered by cache state.
- `../XSS/` — the payloads these caches store and serve.

## Limitations

1. **Age spread**: 2015–2024. CDN defaults changed (CloudFront/Cloudflare now key on more
   headers and honor `Vary` better) — treat the primitives as tests to run, not as guaranteed
   current behavior.
2. **Bounty `-` ≠ unpaid.** Nine of fifteen rows carry no figure in the DB.
3. **Deception rows are $0 in the corpus** — the impact (session → ATO) is stronger than the
   recorded price; do not use this module to set payout expectations.
4. **Weakness labels are triage artifacts** (several rows are tagged XSS or Open Redirect);
   modules classify by the body's mechanism.
5. **No live testing** was performed for this vault — all claims trace to the archived bodies.
6. **Safety**: cache poisoning affects live users. The corpus's own reports warn about it; test
   on your own account and a unique query string.
7. **Quotes** are byte-verified against `references/archive/CACHE-bodies-full-dump.txt`.


<!-- CASESTOCK-LINK:BEGIN -->

## Case stock — vault (`_VAULT/`)

**62 disclosed reports** routed to this category · 15 with a bounty figure · **$24,306** · 37 full write-ups stored locally.

- Full list: [`_VAULT/by-vault-category/15_Cache-Poisoning.md`](../_VAULT/by-vault-category/15_Cache-Poisoning.md)
- Query: `sqlite3 ../_VAULT/reports.sqlite "SELECT id,bounty,title FROM reports WHERE ..."`
- Pull one write-up: `python3 ../_VAULT/scripts/extract_report.py <id>`

| Top paid | Program | Bounty |
|---|---|---|
| [622122](https://hackerone.com/reports/622122) DoS on PayPal via web cache poisoning | PayPal | $9,700 |
| [1695604](https://hackerone.com/reports/1695604) DoS Vulnerability via Cache Poisoning on cdn.shopify.com and shopify-assets.shop | Shopify | $3,800 |
| [1096609](https://hackerone.com/reports/1096609) https://themes.shopify.com::: Host header web cache poisoning lead to DoS | Shopify | $2,900 |
| [409370](https://hackerone.com/reports/409370) Denial of service via cache poisoning | HackerOne | $2,500 |
| [977851](https://hackerone.com/reports/977851) Cache poisoning via X-Forwarded-Host in www.shopify.com/partners/blog | Shopify | $1,000 |

_refreshed 2026-11-17 from the public HackerOne disclosed-report dataset_
<!-- CASESTOCK-LINK:END -->
