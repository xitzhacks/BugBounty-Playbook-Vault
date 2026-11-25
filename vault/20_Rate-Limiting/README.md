---
title: "Rate Limiting / Brute Force / Enumeration — the counter, and how it is defeated"
type: index
category: "Rate Limiting (OTP/2FA/reset codes · login & password gates · throttle bypass vectors · adjacent/unclassified)"
built: "2026-11-07"
evidence: "64 rows from h1-brain disclosed_reports.db (3,673 rows; sha256 8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4) — 58 bucket + 6 documented unclassified merges · all full-body"
bounty: "$19,105 across 28 rows · 01 $1,740/5 · 02 $1,050/5 · 03 $4,770/5 · 04 $11,545/13"
companion_vaults: "../Authentication-Session · ../18_Misconfiguration · ../24_Host-Header-Injection · ../16_Information-Disclosure"
case_id_scheme: "RATE-<HackerOne report id>"
quote_rule: "byte-true to references/archive/RATE-bodies-full-dump.txt"
---

# Vault/Rate-Limiting — when the limit does not exist, or does not matter

Sixty-four disclosed cases. The class pays modestly and reliably; the corpus's two highest single
payouts are *inversions* — a lockout DoS ($900) and a bypass of a prior fix ($3,500) — not plain
"no rate limit" reports.

## Start here

| # | File | What it gives you |
|---|---|---|
| 1 | [`RATE-Testing-Agent-Playbook.md`](RATE-Testing-Agent-Playbook.md) | Executable protocol: threshold bisect → key identification → bypass ladder → kill-gates |
| 2 | [`01_OTP-2FA-Reset-Token.md`](01_OTP-2FA-Reset-Token.md) | 2FA codes, reset tokens, lockout DoS — 11 rows |
| 3 | [`02_Login-Password-Gates.md`](02_Login-Password-Gates.md) | Login and re-auth prompts without counters — 17 rows |
| 4 | [`03_Throttle-Bypass-Vectors.md`](03_Throttle-Bypass-Vectors.md) | XFF, IPv6 subnets, IP rotation, per-surface gaps — 10 rows, $4,770 |
| 5 | [`04_Adjacent-and-Unclassified.md`](04_Adjacent-and-Unclassified.md) | Misfiled rows and enumeration noise — 26 rows |

## References (provenance layer)

| File | Contents |
|---|---|
| [`references/source-index.md`](references/source-index.md) | DB provenance, funnel, bounty accounting, era discipline, limitations |
| [`references/case-register.md`](references/case-register.md) | 64-row ledger with DB metadata |
| [`references/archive/RATE-bodies-full-dump.txt`](references/archive/RATE-bodies-full-dump.txt) | All 64 bodies verbatim (quote anchor) |
| [`references/archive/classes.json`](references/archive/classes.json) | Frozen id → module map |

## Scoreboard (64 rows · 28 paid · $19,105 · max $3,500)

| Case | Title (short) | Program | Bounty |
|---|---|---|---|
| RATE-1363672 | Storefront login throttle bypass (bypass of #708013 fix) | shopify | **$3,500** (max) |
| RATE-1406495 | Disable any Shopify owner's login for 24h (zero-click) | shopify | **$900** |
| RATE-165727 | Slack iOS `/api/auth.signin` unthrottled | slack | **$500** |
| RATE-1987062 | Nextcloud reset endpoint unprotected | nextcloud | **$500** |
| RATE-385381 | Chaturbate room-password brute force | chaturbate | **$500** |
| RATE-819930 | MoPub password brute force via IP change | x | **$420** |
| RATE-1435392 | Acronis login brute force | acronis | $250 |
| RATE-2627062 | Acronis `X-Forwarded-For` limit bypass | acronis | $250 |
| RATE-1394984 | Evernote 6-digit 2FA code brute force | evernote | $150 |
| RATE-1392287 | XVideos current-password check unthrottled | xvideos | $100 |
| RATE-1192144 | Nextcloud "Add to your Nextcloud" partial protection | nextcloud | $100 |
| RATE-1691195 | Nextcloud reset email flood | nextcloud | $100 |

## Cross-vault links

- `../Authentication-Session/` — 2FA/session bypass beyond throttling.
- `../18_Misconfiguration/` — proxy-header trust and forwarded-header handling.
- `../24_Host-Header-Injection/` — the header family abused in module 03.
- `../16_Information-Disclosure/` — enumeration-as-disclosure rows.

## Limitations

1. **Low payout band**: bucket max $3,500, median paid ~$110 — the corpus prices takeover chains, not
   missing counters.
2. **Adjacent money is not class money**: $9,000 of the vault total is stored XSS/Apache RCE rows
   caught by keyword drift (module 04).
3. **Bounty `-` ≠ unpaid.** 36 of 64 rows carry no figure.
4. **Rate-limit testing generates load**: the corpus's own proofs sent ≥1,000 requests. Only do this
   within program rules, with a capped, documented rate.
5. **Era drift**: IP-based counters were already considered weak by 2019–2023 (see module 03); modern
   implementations key on account+device.
6. **No live testing** in this build.
7. **Quotes** byte-verified against the archive; `(sic)` marks author typos.


<!-- CASESTOCK-LINK:BEGIN -->

## Case stock — vault (`_VAULT/`)

**342 disclosed reports** routed to this category · 46 with a bounty figure · **$39,800** · 212 full write-ups stored locally.

- Full list: [`_VAULT/by-vault-category/20_Rate-Limiting.md`](../_VAULT/by-vault-category/20_Rate-Limiting.md)
- Query: `sqlite3 ../_VAULT/reports.sqlite "SELECT id,bounty,title FROM reports WHERE ..."`
- Pull one write-up: `python3 ../_VAULT/scripts/extract_report.py <id>`

| Top paid | Program | Bounty |
|---|---|---|
| [125505](https://hackerone.com/reports/125505) Possibility to brute force invite codes in riders.uber.com | Uber | $5,000 |
| [1363672](https://hackerone.com/reports/1363672) Bypass a fix for report #708013 | Shopify | $3,500 |
| [1330529](https://hackerone.com/reports/1330529) Claiming the listing of a non-delivery restaurant through OTP manipulation | Eternal | $3,250 |
| [125200](https://hackerone.com/reports/125200) Lack of rate limiting on get.uber.com leads to enumeration of promotion codes an | Uber | $3,000 |
| [125707](https://hackerone.com/reports/125707) Possibility to enumerate and bruteforce promotion codes in Uber iOS App | Uber | $3,000 |

_refreshed 2026-11-17 from the public HackerOne disclosed-report dataset_
<!-- CASESTOCK-LINK:END -->
