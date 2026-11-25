---
title: "Cryptography source index — provenance, funnel, bounty accounting, limitations"
type: source-index
built: "2026-11-07"
---

# Source index — Cryptography build

## 1. Corpus provenance

- **Primary source**: `/home/user/tools/h1-brain/disclosed_reports.db` — h1-brain's pre-built
  SQLite corpus of publicly disclosed HackerOne reports (**3,673 rows**), sha256
  `8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4`.
- **Working copies**: `/home/user/opencode-work/h1brain/classified.json` (bucket `crypto`, 26 rows),
  `module_map_all.json`, `unclassified_classified.json`. In-vault:
  `references/archive/CRYPTO-bodies-full-dump.txt` (46 bodies), `classes.json`, `meta.json`.

## 2. Classification funnel

1. **Labeled/keyword net**: weakness labels (`Cryptographic Issues`, `Weak Cryptography`, `Padding
   Oracle`, `Insufficient Entropy`) plus keyword arms (`cbc`, `padding oracle`, `starttls`,
   `certificate`, `jwt`, `hmac`, `iv reuse`, `signature`) → 26 rows.
2. **Unclassified merge**: the unclassified classifier assigned 20 further rows to crypto (19 GHSL
   CodeQL one-liners, 1 full body); they are kept as module 04, clearly labeled.
3. **Module split** (frozen in `classes.json`):
   - 01 `tls-starttls-legacy-protocol` 7
   - 02 `crypto-primitives-oracles-signatures` 10
   - 03 `cert-validation-weak-secrets-insecure-channel` 8
   - `_adjacent` 1 (CRYPTO-151868, rate-limit row)
   - 04 `_adjacent_unclassified` 20

## 3. Bounty accounting

- **Rule**: DB `bounty_amount`; `-` when absent. Blank ≠ unpaid.
- Bucket: **26 rows, 16 with figures, $11,705** (max $3,000, CRYPTO-728110).
- Merge pool: **20 rows, all with figures, $43,400** — 19 GHSL queries at $1,000–$4,500 plus
  CRYPTO-170548 ($500). Adjacent: 1 row, $100.
- Vault total used in the README: **$55,105 / 36 paid**; the merge pool is labeled separately
  wherever a total is quoted.

## 4. Era discipline

- Rows span 2014–2024. DROWN/POODLE/STARTTLS-stripping rows are historical coordination records;
  cert-validation and construction errors persist into current code.
- The GHSL block is a *code-query market* (paid per accepted query), not an application-bounty
  signal — pricing must not be extrapolated to web targets.
- Weakness labels are era triage values; modules classify by the body's mechanism.

## 5. Limitations

1. **Bucket of 26** is a disclosed-only slice; master-list row 19 cites 187 + 14 + 11 externally.
2. **Twenty rows have no readable body** (GHSL one-liners) and are never quoted.
3. **Merge pool inflates the headline total** — module 04 states this explicitly.
4. **No live testing**; all mechanics trace to archived bodies.
5. **Quote discipline**: every blockquote is byte-true to
   `references/archive/CRYPTO-bodies-full-dump.txt`; `(sic)` marks author typos.
