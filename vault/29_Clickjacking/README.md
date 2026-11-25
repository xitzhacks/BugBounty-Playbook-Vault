---
title: "Clickjacking / UI Redressing — headers, markup overlays, and the chains that pay"
type: index
category: "Clickjacking / UI Redressing (frame headers · markup & RTLO overlays · enable-chains)"
built: "2026-11-07"
evidence: "23 rows from h1-brain disclosed_reports.db (3,673 rows; sha256 8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4) · 23/23 full bodies"
bounty: "$8,460 across 6 rows · 01 $1,960/4 · 02 $3,500/1 · 03 $3,000/1"
companion_vaults: "../XSS · ../CSRF · ../18_Misconfiguration · ../17_Privilege-Escalation"
case_id_scheme: "CJ-<HackerOne report id>"
quote_rule: "byte-true to references/archive/CJ-bodies-full-dump.txt"
---

# Vault/Clickjacking — the cheapest bug, priced by what the click does

Twenty-three disclosed cases. The header check is a commodity (most rows pay nothing); the money
is in the *consequence* of the click — $3,500 for a CSS-class overlay that swallows the whole page,
$3,000 for clickjacking a scanner's embedded browser into RCE.

## Start here

| # | File | What it gives you |
|---|---|---|
| 1 | [`CJ-Testing-Agent-Playbook.md`](CJ-Testing-Agent-Playbook.md) | Executable protocol: header audit → browser-specific proofs → impact framing → kill-gates |
| 2 | [`01_X-Frame-Options-and-CSP.md`](01_X-Frame-Options-and-CSP.md) | Missing header, `SAMEORIGIN` gaps, unsupported `ALLOW-FROM` — 14 rows, $1,960 |
| 3 | [`02_Markup-RTLO-UI-Redress.md`](02_Markup-RTLO-UI-Redress.md) | Sanitizer gaps, spoofed app CSS classes, RTLO — 5 rows, $3,500 |
| 4 | [`03_Clickjacking-Enable-Chains.md`](03_Clickjacking-Enable-Chains.md) | Self-XSS delivery, scanner RCE, link truncation — 4 rows, $3,000 |

## References (provenance layer)

| File | Contents |
|---|---|
| [`references/source-index.md`](references/source-index.md) | DB provenance, funnel, bounty accounting, era discipline, limitations |
| [`references/case-register.md`](references/case-register.md) | 23-row ledger with DB metadata |
| [`references/archive/CJ-bodies-full-dump.txt`](references/archive/CJ-bodies-full-dump.txt) | All 23 bodies verbatim (quote anchor) |
| [`references/archive/classes.json`](references/archive/classes.json) | Frozen id → module map |

## Scoreboard (23 rows · 6 paid · $8,460 · max $3,500)

| Case | Title (short) | Program | Bounty |
|---|---|---|---|
| CJ-662287 | RDoc wiki sanitizer → full-page click overlay (filed XSS) | gitlab | **$3,500** (max) |
| CJ-1274695 | Burp Scanner RCE via clickjacking + Chrome debug port | portswigger | **$3,000** |
| CJ-591432 | Periscope `ALLOW-FROM` unsupported → clickjacking | x | **$1,120** |
| CJ-198622 | periscope.tv `ALLOW-FROM` (Chrome) | x | **$560** |
| CJ-2119892 | `sketch.pixiv.net/draw` frame → fake login → ATO | pixiv | **$200** |
| CJ-405342 | ylands.com frameable | bohemia | **$80** |
| CJ-85624 | Player card → wormable clickjacking | x | - |
| CJ-154963 | `cards.twitter.com` missing frame headers → email capture | x | - |
| CJ-214087 | Yelp `SAMEORIGIN` gaps | yelp | - |
| CJ-305128 | Yelp important functions frameable | yelp | - |
| CJ-355859 | Yelp reservations → PII + card misuse | yelp | - |
| CJ-299009 | Semrush SSO page frameable | semrush | - |
| CJ-289246 | Semrush links without DENY/SAMEORIGIN | semrush | - |
| CJ-765355 | `refer.wordpress.com` campaign settings | automattic | - |
| CJ-765955 | `join.nordvpn.com` frameable | nordsecurity | - |
| CJ-921709 | WordPress donation page redirect | wordpress | - |
| CJ-289823 | Simplenote injected login form | automattic | - |
| CJ-291683 | Simplenote injected iframes | automattic | - |
| CJ-297547 | Simplenote Android forms | automattic | - |
| CJ-196222 | RTLO in Snapchat chat | snapchat | - |
| CJ-643274 | DM link truncation → Google credentials | x | - |
| CJ-892289 | self-XSS + clickjacking → ATO (Firefox) | imgur | - |
| CJ-953579 | clickjacking triggers self DOM-XSS | automattic | - |

## Cross-vault links

- `../XSS/` — the injection half of module 02 and 03.
- `../CSRF/` — clickjacking bypasses CSRF tokens; the two classes share impact framing.
- `../18_Misconfiguration/` — header hygiene rows that overlap.
- `../17_Privilege-Escalation/` — chains that end in ATO.

## Limitations

1. **Low payout class**: 6/23 rows paid, max $3,500, median paid $560 — do not prioritize this over
   injection classes.
2. **Bounty `-` ≠ unpaid.** 17 rows carry no figure.
3. **Browser-specific**: `ALLOW-FROM` behavior depends on browser/era; modern CSP
   `frame-ancestors` supersedes it, so old PoCs may no longer reproduce.
4. **Filed-class drift**: CJ-662287 is filed as XSS and CJ-643274 has no frame at all — the corpus
   bucket is keyword-derived; modules classify by body.
5. **No live re-testing** in this build.
6. **Ethics/scope**: clickjacking PoCs should not be used against real users; frame your own account.
7. **Quotes** byte-verified against the archive; `(sic)` marks author typos.


<!-- CASESTOCK-LINK:BEGIN -->

## Case stock — vault (`_VAULT/`)

**165 disclosed reports** routed to this category · 12 with a bounty figure · **$10,640** · 112 full write-ups stored locally.

- Full list: [`_VAULT/by-vault-category/29_Clickjacking.md`](../_VAULT/by-vault-category/29_Clickjacking.md)
- Query: `sqlite3 ../_VAULT/reports.sqlite "SELECT id,bounty,title FROM reports WHERE ..."`
- Pull one write-up: `python3 ../_VAULT/scripts/extract_report.py <id>`

| Top paid | Program | Bounty |
|---|---|---|
| [662287](https://hackerone.com/reports/662287) Cross-site Scripting (XSS) - Stored in RDoc wiki pages | GitLab | $3,500 |
| [1274695](https://hackerone.com/reports/1274695) RCE of Burp  Scanner / Crawler via Clickjacking  | PortSwigger Web Security | $3,000 |
| [591432](https://hackerone.com/reports/591432) Twitter Periscope Clickjacking Vulnerability | X / xAI | $1,120 |
| [198622](https://hackerone.com/reports/198622) Clickjacking Periscope.tv on Chrome | X / xAI | $560 |
| [34686](https://hackerone.com/reports/34686) Ошибка фильтрации | Mail.ru | $500 |

_refreshed 2026-11-17 from the public HackerOne disclosed-report dataset_
<!-- CASESTOCK-LINK:END -->
