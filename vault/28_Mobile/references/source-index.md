---
title: "Mobile source index — provenance, funnel, DB reconciliation, module split, limitations"
type: source-index
built: "2026-11-07"
---

# Source index — Mobile build

## 1. Corpus provenance

- **Primary source**: `/home/user/tools/h1-brain/disclosed_reports.db` — the h1-brain pre-built
  SQLite corpus of publicly disclosed, bounty-awarded HackerOne reports (**3,673 rows**,
  table `disclosed_reports` with fields `id, title, vulnerability_information, weakness_name,
  program_handle, asset_identifier, asset_type, cve_ids, bounty_amount`). The DB was fetched
  from the repo's Git-LFS pointer and sha256-verified:
  `8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4`. No live HackerOne fetch
  this build.
- **Classifier outputs**: `/home/user/opencode-work/h1brain/unclassified_classified.json`
  (key `mobile` = a 13-id list: 176929, 221558, 283058, 283063, 328486, 414101, 519059,
  1011956, 1030295, 1142918, 1161956, 1189162, 1189168). Unlike the sibling vaults, the
  mobile ids carry no classified row payload — titles, bodies, programs, bounties, and CVEs
  were all re-read from the DB this build. `module_map_all.json` holds no `mobile` key.
- **In-vault archive**: `references/archive/mob-bodies-full-dump.txt` (13/13 bodies),
  `references/archive/classes.json` (frozen module assignment).

## 2. Classification funnel

1. **Id set** (`unclassified_classified.json` `mobile` = 13 ids) promoted by **per-body read**
   from the DB. All 13 bodies read end-to-end before module assignment ("bodies win"). DB
   `weakness_name` is null for all 13 rows — classification is by body behavior only.
   Evidence: 10 full-body / 3 metadata-only (1011956, 1030295, 1161956 — 54-byte GHSL
   pointer lines).
2. **Module split** (frozen in `classes.json`, mechanism-driven, recorded here so the bucket
   reconciliation is exact):
   - `android-webview-intent` (7 ids): 283058, 283063, 328486, 414101, 1011956, 1030295,
     1161956 — exported-activity / WebView / intent sinks + GHSL Android queries whose
     titles name those sinks (WebView loading, intent extra, Dex).
   - `ios-app-privacy` (6 ids): 176929, 221558, 519059, 1142918, 1189162, 1189168 —
     browser trust (Brave iOS), token-in-URL search leak (Grab), cross-surface setting
     override (Twitter), file-picker leak (Nextcloud), E2E key lifecycle (Nextcloud ×2).
   - **Documented adjustments vs. the prompt's sketch**: MOB-328486 (Zomato DeepLinkRouter
     → TreatsWebView, exported) is placed in Module A with its mechanism; MOB-1142918
     (Nextcloud `GET_CONTENT` file-picker leak, CVE-2021-32695) is placed in Module B with
     its mechanism. Every id is in exactly one module — verified by the ids-once check.
3. **DB reconciliation**: every id verified present in `disclosed_reports` with matching
   title, bounty, and body length. Programs: nextcloud 3 · irccloud 2 ·
   github-security-lab 3 · brave, grab, zomato, shipt, x 1 each. Two CVEs in the DB:
   MOB-1142918 → `CVE-2021-32695`, MOB-1189168 → `CVE-2021-32658`.

## 3. Bounty accounting

- **Rule**: DB `bounty_amount` where present; `None` recorded as no figure (not $0). Blank ≠
  unpaid — HackerOne does not always publish figures.
- Corpus: 7/13 rows carry figures, totaling **$6,810** (max $2,300, MOB-1011956 —
  metadata-only). Quotable subtotal $2,710 (414101 $350 + 221558 $200 + 519059 $560 +
  1189162 $1,500 + 1189168 $100); metadata subtotal $4,100 (1011956 $2,300 + 1030295
  $1,800). See case-register.md for per-row labels and the arithmetic.
- **What the money prices**: quotable figures price sink demonstrations and secret moves;
  metadata figures price GHSL detector authorship. The vault never blends them.

## 4. Limits & era honesty

1. **Bucket provenance differs from sibling vaults** — unclassified-id promotion by body
   read, not `classified.json` rows. The id set is recorded verbatim; no classified-row
   claims are made for mobile.
2. **Split is mechanism-driven** (Module A WebView/intent vs. Module B privacy/data), with
   328486/1142918 placed by mechanism and documented. The split is a vault design choice,
   not a classifier output (`module_map_all.json` has no mobile key).
3. **Metadata vs. quotable money must never be blended** ($4,100 vs. $2,710).
4. **Null weakness labels** — all 13 rows classify by body behavior only.
5. **Screenshot/video-dependent PoCs** (`{F…}` markers) — text payloads are byte-true;
   no image content reconstructed.
6. **Era**: 2016–2021 disclosures; P4 hardening is outside-corpus doctrine.
7. **No live testing** — in-scope test devices/builds only (playbook P0/P5).
