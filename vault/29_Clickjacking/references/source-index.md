---
title: "Clickjacking source index — provenance, funnel, bounty accounting, limitations"
type: source-index
built: "2026-11-07"
---

# Source index — Clickjacking build

## 1. Corpus provenance

- **Primary source**: `/home/user/tools/h1-brain/disclosed_reports.db` — h1-brain's pre-built
  SQLite corpus of publicly disclosed HackerOne reports (**3,673 rows**), sha256
  `8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4`.
- **Working copies**: `/home/user/opencode-work/h1brain/classified.json` (bucket `clickjacking`,
  23 rows) and `module_map_all.json`. In-vault:
  `references/archive/CJ-bodies-full-dump.txt` (23 bodies), `classes.json`, `meta.json`.

## 2. Classification funnel

1. **Keyword/label net**: `clickjack`, `ui redress`, `x-frame-options`, `frame-ancestors`,
   `iframe` + UI-redressing terms → 23 rows.
2. **Body read**: all 23 read; several rows are filed under XSS or made no use of frames at all
   (CJ-662287, CJ-643274) and are labeled accordingly in their modules.
3. **Module split** (frozen in `classes.json`):
   - 01 `x-frame-csp-header` 14
   - 02 `markup-rtlo-ui-redress` 5
   - 03 `clickjacking-enable-chain` 4

## 3. Bounty accounting

- **Rule**: DB `bounty_amount`; `-` when absent. Blank ≠ unpaid.
- **6/23 rows** carry figures, totaling **$8,460**; max $3,500 (CJ-662287).
  Module totals: 01 $1,960/4 · 02 $3,500/1 · 03 $3,000/1.

## 4. Era discipline

- Rows span 2014–2021. `X-Frame-Options: ALLOW-FROM` (CJ-198622, CJ-591432) is obsolete in modern
  Chromium; `frame-ancestors` is the current control. The *impact framing* (what the click does)
  transfers; the specific header claims often do not.
- Weakness/Filed-class drift is significant here: the only $3,500 row is filed as XSS.

## 5. Limitations

1. **Low-ROI class** in this corpus: 6/23 paid, median paid $560.
2. **Browser-specific claims** must be reproduced per browser; several rows are Firefox-era.
3. **17 rows have no bounty figure** — payout expectations here are a floor, not a ceiling.
4. **No live re-testing** — all mechanics trace to archived bodies.
5. **Quote discipline**: every blockquote is byte-true to
   `references/archive/CJ-bodies-full-dump.txt`; `(sic)` marks author typos.
