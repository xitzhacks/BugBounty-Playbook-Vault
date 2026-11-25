---
title: "Misconfiguration source index — provenance, funnel, bounty accounting, limits"
type: source-index
built: "2026-11-07"
sha256: "8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4"
---

# Source index — Misconfiguration build (#18)

## 1. Roster provenance

- **Primary source**: `/home/user/tools/h1-brain/disclosed_reports.db` — the h1-brain pre-built SQLite corpus of publicly disclosed, bounty-awarded HackerOne reports (**3,673 rows**), sha256-verified this build as `8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4`. No live HackerOne fetch this build.
- **Classifier output**: `/home/user/opencode-work/h1brain/classified.json`, bucket `misconfig` = **152 rows** (`src` cells: "Violation of Secure Design Principles" 119 · "Misconfiguration" 17 · "Cleartext Transmission of Sensitive Information" 16; DB `weakness_name` verified identical to classified `src` on all 152 rows; classified title/body/program/bounty verified byte-identical to DB `vulnerability_information` on all 152 rows).
- **Merge surface**: `/home/user/opencode-work/h1brain/module_map_all.json` under `misconfig` → 7 keys totaling **166 ids**: `subdomain_takeover_dangling_state` 15 · `account_verification_rate_limiting` 19 · `headers_tls_transport_misconfig` 30 · `exposure_api_secrets_config` 59 · `spoofing_phishing_homograph_open_redirect` 19 · `_adjacent` 10 · `_adjacent_unclassified` 14.
- **Coverage arithmetic** (verified this build): 15+19+30+59+19+10 = **152 bucket rows** (every bucket id in exactly one of the six modules — no dupes, no skips); `_adjacent_unclassified` = **14 ids, none in the bucket** (all 14 live in `classified.json`'s `unclassified` bucket, 468 rows). Vault corpus = **166 rows** (152 bucket + 14 merges). The case register's main ledger covers the 152 bucket rows; the 14 merges are appended as a labeled bridge ledger (§4).
- **Sibling index**: `module_map_all.json` also carries `misconfig-ssl-tls` (11 ids, all already inside this vault: 99157, 131065, 180538, 210331, 214571, 386735, 576288, 703759, 1565622, 1753226, 1813831). It is a *view* over this bucket, not additional rows; the vault cites it for era context but adds no rows from it.

## 2. Classification funnel

1. **Bucket selection (classifier v1)**: the `misconfig` bucket in `classified.json` (152 rows). The classifier's weakest point is visible in the src distribution — 119/152 rows are labeled only by the catch-all "Violation of Secure Design Principles," so the bucket must be re-sorted by reading bodies, not labels.
2. **Module map**: `module_map_all.json` assigns the 152 to six named modules (five topical + `_adjacent`), and merges 14 `unclassified` rows into `_adjacent_unclassified`. **Overlap check**: buckets in `classified.json` are disjoint (misconfig ∩ {subdomain-takeover, rate-limiting, info-disclosure, …} = ∅ for every other bucket), and the `misconfig-ssl-tls` sibling is a 11-row subset-view of this vault. Final module split (frozen in `archive/classes.json`, 166 entries): 01 Subdomain-Takeover-and-Dangling-State 15 · 02 Account-Verification-and-Rate-Limiting 19 · 03 Headers-TLS-and-Transport-Misconfig 30 · 04 Exposure-API-Secrets-and-Config 59 · 05 Spoofing-Phishing-Homograph-and-Open-Redirect 19 · 06 Adjacent-and-Unclassified-Merges 24 (10 bucket-adjacent + 14 merges).
3. **Per-body read**: all 166 bodies read end-to-end before module writing ("bodies win"). Of the 166, **147 substantive bodies (>100 bytes)** carry the vault's doctrine; **9 are corpus-metadata rows** (2 curl HSTS 78-byte pointers in module 03; 1 algolia 100-byte bombardment claim in module 02; 10 GHSL 54-byte one-liners in module 06 — the 54-byte body is byte-identical `"This bug was reported directly to GitHub Security Lab."` across all ten). No body is empty; the minimum body length in the 152 is 78 bytes.
4. **Adjacent handling**: `_adjacent` (10) is a *bodies-wrong* exhibit — rows whose bodies belong to race/traversal/XSS/RCE/CSRF/business-logic and whose labels are "Violation of Secure Design Principles" (module 06 §2). `_adjacent_unclassified` (14) is the *sweep-queue* exhibit — classifier output, not label reuse (module 06 §3). The vault does **not** re-bucket anything; both pools stay in module 06 under their provenance labels.

## 3. Bounty accounting

- **Rule**: DB `bounty_amount` where present; classified `bounty` verified identical to DB on all 152 rows (zero mismatches). `None` recorded as `-` (no figure in DB) — blank ≠ unpaid; HackerOne does not always publish figures. No `bounty=0` cells exist.
- **Vault arithmetic**: bucket **$25,932/38 paid rows** + unclassified merges **$8,600/9** = **$34,532/47** across 166 rows. Module paid totals: 01 $4,000/3 · 02 $4,050/4 · 03 $2,311/6 · 04 $14,521/19 · 05 $900/5 · 06 (bucket-adjacent) $150/1 + (merges) $8,600/9. Per-row ledger in `case-register.md`.
- **Ceiling and concentration**: max $6,300 (MISCONF-1258871, exposed Cortex). Top five rows = $15,150 (43.9% of vault money in 5/47 paid rows). The $3,750 (MISCONF-815085, CRLF email accounts) and $3,000 (MISCONF-154425) rows dominate all other modules. Module 04's 19 paid rows hold $14,521 (42% of vault money in 36% of the rows) — the module is the vault's money center.
- **GHSL-merges accounting (honesty)**: the unclassified merges' $8,600 includes $5,550 from ten 54-byte one-liners (highest: 909374 $1,800 directory listing). Those five- and four-figure rows are priced telemetry with zero quotable technique. They are counted in vault totals but never cited as doctrine — the playbook and modules only *name* them.
- **Program mix (corpus-wide, descriptive)**: `security` (HackerOne's own program) 21 bucket rows (largest), brave 11, nextcloud 8, gitlab 8, ibb 6, mozilla 5, netflix-adjacent platform rows distributed. Merges: github-security-lab 10 of 14.

## 4. Era discipline

- The corpus spans ~2013–2024-era disclosures. Specific evidence varies by row (imgur-era PoCs never appear; curl CVE-2024-2004 and the 2023 Mozilla VPN disclosure are the modern tail). **Hardening fingerprints** (HSTS preload, punycode rendering, Actuator allowlists, OAuth token lifetimes) are given in the playbook P4 as expectations, never as corpus doctrine.
- **Lines that move** — claims that priced in their era may not price now, and vice versa: the $1 weak-cipher row (MISCONF-131065) is retained precisely as the priced warning; the torproject defensive review (MISCONF-115686) is retained as the no-effect negative example; the $1,800 GHSL directory-listing row is retained as priced-but-unquotable telemetry. Later-era modules (curl CVE-2022-30115/42916/43551/2024-2004, Nextcloud CVE-2020-8133/2023-28833/2024-22403, Brave CVE-2024-37406, Mozilla VPN 2023) are flagged as the bundle era of the corpus.
- **What changed**: managed CDNs and WAFs changed the takeover shape (module 01's CloudFront/S3 analysis is the modern form; the legacy CNAME forms are 2014–2019-era rows). The vault keeps era labels per row and does not modernize quotes.

## 5. Limitations

1. **Labels are triage artifacts.** "Violation of Secure Design Principles" covers 119/152 rows; module 06's ten prove the label false. The vault classifies by body ("bodies win") and records the bucket's src verbatim in the register's src column — but the registers' *module* column is the vault's reading, not the classifier's.
2. **Figure absence is not non-payment.** 119/166 rows carry no DB figure. The vault calls them "no figure" and never "$0" unless stated in-body; the only forced-$0-style rows are the $1 same-bounty row (131065) and module 06's nine no-figure adjacent rows (which are never counted as "unpaid class rows").
3. **GHSL one-liners are telemetry, not evidence.** 10 merges ($5,550) have no technique in the DB. The vault counts their dollars, names their titles, and quotes nothing from them.
4. **Cross-bucket overlaps exist at the seam.** The `misconfig-ssl-tls` sibling view (11 rows) and this vault's modules overlap by construction; companion vaults (13_Subdomain-Takeover, 14_HTTP-Request-Smuggling, 15_Cache-Poisoning, 16_Information-Disclosure, 20_Rate-Limiting) hold zero overlapping ids with this bucket (verified: bucket ∩ every sibling classifier bucket = ∅) but the same findings may appear in their prose as chain/teaching references.
5. **Tool choices are historical evidence.** Scanner output (SSLLabs grades, weak-cipher dumps, `openssl s_client`, Burp repeater/intruder) is quoted because the bodies record it, not because it is current best practice. Live-testing assumptions must be validated against current toolchain docs.

## Archive contents

| File | Contents |
|---|---|
| [`archive/MISCONF-bodies-full-dump.txt`](archive/MISCONF-bodies-full-dump.txt) | All 166 bodies verbatim, module-ordered then ascending id; anchor for every blockquote in the vault (334 KB). |
| [`archive/classes.json`](archive/classes.json) | Frozen module assignment: case id → module slug (166 entries). |
| [`archive/meta.json`](archive/meta.json) | Build metadata (row counts, source, sha256). |
