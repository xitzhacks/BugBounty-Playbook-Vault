---
title: "Business-logic source index — provenance, funnel, classification mechanics, limitations"
type: source-index
built: "2026-11-07"
---

# Source index — Business Logic build

## 1. Corpus provenance

- **Primary source**: `/home/user/tools/h1-brain/disclosed_reports.db` — the h1-brain pre-built SQLite corpus of publicly disclosed, bounty-awarded HackerOne reports (3,673 rows). The repo stores the DB as a Git-LFS pointer; the real file was fetched from `media.githubusercontent.com` and sha256-verified: `8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4`. No live HackerOne fetch this build.
- **Row fields**: `id, title, vulnerability_information, weakness_name, program_handle, asset_identifier, asset_type, cve_ids, bounty_amount`. Full report bodies in `vulnerability_information` (bucket avg ~1.9 KB).
- **Working copies**: `/home/user/opencode-work/h1brain/{classified.json, module_map_all.json, unclassified_classified.json}` (classifier output + module map). In-vault archive: `references/archive/BL-bodies-full-dump.txt` (127/127 bodies), `references/archive/classes.json` (frozen module assignment).

## 2. Classification funnel

1. **Keyword/labeled net** over all 3,673 rows: CWE-style weakness label `Business Logic Errors` plus keyword arms in title/body over payment, order, cart, quantity, coupon, redeem, invite, verification, OTP, rate-limit and race vocabulary → **118 rows** in `classified.json` bucket `business-logic` (all 118 DB-verified: every field, including `vulnerability_information`, is byte-identical between `classified.json` and the DB — verified this build).
2. **module_map_all.json** partitions the bucket bodies-win into six modules: `commerce_payments_rewards` 28 · `account_invite_access_workflows` 32 · `race_condition_replay` 6 · `rate_limit_state_abuse` 21 · `_adjacent` 31 (bucket rows kept in the vault but other-class by body) · and merges 9 rows from the classifier's `unclassified` pool (`_adjacent_unclassified`, bodies pulled from the DB; they carry `weakness_name=None` and no `classified.json` entry).
3. **Per-body read**: all 127 bodies read end-to-end before module assignment ("bodies win"). 127 full-body, 0 metadata-only — the bucket has no one-liner bodies, so every module can quote.
4. **Freeze**: `references/archive/classes.json` maps each id to its module; `references/archive/BL-bodies-full-dump.txt` is the quote anchor.

## 3. Bounty accounting

- **Rule**: DB `bounty_amount` where present; `None` recorded as `-` (no figure). Blank is not unpaid — HackerOne does not always publish figures.
- Corpus: 55/127 rows carry figures, totaling **$60,090**; max $7,500 (BL-1295844). Bucket-only: 52 rows / $56,590; unclassified merges add 3 rows / $3,500 (1044285 $2,900; 434116 $300; 1566325 $300). See case-register.md for per-row labels and module totals.

## 4. Era discipline

Rows span roughly 2013-2024 era disclosures (2016-era legalrobot/nextcloud/zomato reports through 2023-era indrive/courier reports). Tooling evidence (Burp Intruder, Turbo Intruder gate scripts, Match-and-Replace response editing) is historical record; the business rule being broken does not date. Where a body states its own mitigations (e.g. BL-1070510 client-side is_active flip), the module records the server-side fix direction.

## 5. Limitations

1. **Bucket is not class.** 31 `_adjacent` rows (41% of vault paid money: $24,580 of $60,090) are subdomain takeovers, curl advisories and misconfiguration that the keyword net caught on `logic flaw` wording. The vault keeps them as an honest overflow shelf; their home vaults are cross-cited, not duplicated.
2. **Unclassified-merge asymmetry.** The 9 merged rows have no `classified.json` entry and no DB weakness label; their inclusion criterion is body read only. The remaining `unclassified` pool is not in this vault; a v2 sweep may promote more rows into business-logic later.
3. **Bounty `None` != unpaid.** 71 of 127 rows carry no figure; the $60,090 total is a corpus-floor, not a total. Five-figure rows are all real-money deltas, not rate-card maxima.
4. **Program `security` skew.** 19 of the bucket's 118 rows are HackerOne's own program (mostly invitation accounting). The class's biggest surplus is therefore measured against the platform that invented the class; vendor-diverse rows are the better pay-rate evidence.
5. **Quote discipline**: every blockquote across the five class modules is byte-true to `references/archive/BL-bodies-full-dump.txt`; `(sic)` where needed. No invented quotes, no paraphrase passing as quotation. No live testing was performed — validate against the hunt skill scenario matrices.

