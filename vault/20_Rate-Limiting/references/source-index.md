---
title: "Rate Limiting source index — provenance, funnel, bounty accounting, limitations"
type: source-index
built: "2026-11-07"
---

# Source index — Rate Limiting build

## 1. Corpus provenance

- **Primary source**: `/home/user/tools/h1-brain/disclosed_reports.db` — h1-brain's pre-built
  SQLite corpus of publicly disclosed HackerOne reports (**3,673 rows**), sha256
  `8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4`.
- **Working copies**: `/home/user/opencode-work/h1brain/classified.json` (bucket `rate-limiting`,
  58 rows), `module_map_all.json`, `unclassified_classified.json`. In-vault:
  `references/archive/RATE-bodies-full-dump.txt` (64 bodies), `classes.json`, `meta.json`.

## 2. Classification funnel

1. **Labeled/keyword net**: weakness labels (`Improper Restriction of Excessive Authentication
   Attempts`, `Uncontrolled Resource Consumption`) plus keyword arms (`rate limit`, `brute force`,
   `throttl`, `enumeration`, `otp`, `2fa`, `verification code`) → 58 rows.
2. **Adjacent triage**: the module map isolated 20 in-bucket rows that are dominated by
   enumeration or misfiled classes (`_adjacent`), and 6 further rows came from the unclassified
   classifier (`_adjacent_unclassified`).
3. **Module split** (frozen in `classes.json`):
   - 01 `otp-2fa-reset-token` 11
   - 02 `login-password-gates` 17
   - 03 `throttle-bypass-vectors` 10
   - 04 `_adjacent` 20 + `_adjacent_unclassified` 6

## 3. Bounty accounting

- **Rule**: DB `bounty_amount`; `-` when absent. Blank ≠ unpaid.
- Bucket: **58 rows, 25 with figures, $18,275** (max $3,500, RATE-1363672).
- Merges: **6 rows, 3 with figures, $830**.
- Vault total: **$19,105 / 28 paid** — module 04 carries **$11,545**, of which ~$9,000 is
  non-class money (stored XSS, Apache RCE) caught by keyword drift. Always cite the module, not the
  vault total, when discussing class value.

## 4. Era discipline

- Rows span 2015–2024. IP-only counters were already recognized as weak by 2019+; modern
  implementations key on account+device.
- The corpus's highest payout (RATE-1363672) is a *bypass of a prior fix* — evidence that re-testing
  closed reports is the highest-yield move in this class.

## 5. Limitations

1. **58-row bucket** is a disclosed-only slice; master-list row 20 cites 51 + 63 externally.
2. **Module 04 inflates the vault total** — labeled in every place the total appears.
3. **Testing produces load**; the corpus's own proofs sent ≥1,000 requests. Program rules first.
4. **No live testing** in this build.
5. **Quote discipline**: every blockquote is byte-true to
   `references/archive/RATE-bodies-full-dump.txt`; `(sic)` marks author typos.
