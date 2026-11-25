---
title: "INFO source index — provenance, funnel, classification mechanics, limitations"
type: source-index
built: "2026-11-07"
---

# Source index — Information Disclosure build

## 1. Corpus provenance

- **Primary source**: `/home/user/tools/h1-brain/disclosed_reports.db` — the h1-brain pre-built SQLite corpus of publicly disclosed, bounty-awarded HackerOne reports (**3,673 rows**). The repo stores the DB as a Git-LFS pointer; the real file was fetched from `media.githubusercontent.com` and sha256-verified this build: `8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4`. No live HackerOne fetch this build.
- **Row fields**: `id, title, vulnerability_information, weakness_name, program_handle, asset_identifier, asset_type, cve_ids, bounty_amount`. Full report bodies in `vulnerability_information`.
- **Working copies**: `/home/user/opencode-work/h1brain/{classified.json, module_map_all.json, info-disclosure_digest.md}` (classifier output + module map). In-vault archive: `references/archive/INFO-bodies-full-dump.txt` (362/362 bodies), `references/archive/classes.json` (frozen module assignment), `references/archive/build.py` (dump/classes generator).
- **Byte-equality check**: `classified.json` titles/bodies verified byte-equal to DB `title`/`vulnerability_information` for all 362 ids (0 mismatches) before any quoting. All vault quotes trace to the dump, which is generated directly from the DB.

## 2. Classification funnel

1. **Bucket (classified.json)**: `info-disclosure` = **340 rows** (DB weakness split: `Information Disclosure` 302 · `Privacy Violation` 23 · `Cleartext Storage of Sensitive Information` 15). All 340 ids verified present in `module_map_all.json` under `info-disclosure` with per-module split `graphql_api_objects_exposure` 21 · `hackerone_reports_bounty_privacy` 51 · `user_pii_location_privacy` 128 · `file_path_errors_secrets_leaks` 104 · `protocol_memory_disclosure` 17 (= 321) + `_adjacent` 19 = **340 exactly, zero duplicates, zero missing**.
2. **Merges (module_map_all.json `info-disclosure._adjacent_unclassified`)**: **22 rows** drawn from the classifier's `unclassified` pool (468 rows; verified 22/22 in `unclassified`, 0/22 in the bucket). Appended as the tail of module 06 (Adjacent). Vault total: **362 = 340 + 22**.
3. **Per-body read**: all 362 bodies read end-to-end (via the digest + DB; medium-length reads verified line-by-line for every quoted row). Evidence levels, honestly labeled: **356 full-body** (len > 80, quotable) + **6 metadata-only** GitHub-Security-Lab one-liners (`This bug was reported directly to GitHub Security Lab.`, len 54: INFO-886287, 1026252, 1122661, 1122662, 1365761, 1526609) — anchors, never quoted as technique.
4. **Module split** (frozen in `archive/classes.json`): 01 GraphQL-API-Objects-Exposure 21 · 02 HackerOne-Reports-Bounty-Privacy 51 · 03 User-PII-Location-Privacy 128 · 04 File-Path-Errors-Secrets-Leaks 104 · 05 Protocol-Memory-Disclosure 17 · 06 Adjacent-Disclosure-Noise 41 (= 19 adjacent + 22 unclassified).
5. The remaining `unclassified` pool (468 − 22 = 446 rows) is **not** in this vault. A v2 classifier sweep may promote more rows into disclosure later; until then the vault quotes only its 362.

## 3. Bounty accounting

- **Rule**: DB `bounty_amount` where present (labeled `$` in tables/register); `None`/`NULL` recorded as `-` (no figure). Blank ≠ unpaid — HackerOne does not always publish figures.
- Corpus: 161/362 rows carry figures, totaling **$281,925** (bucket-340: $217,375/149, max $25,000 INFO-3000510; unclassified merges: $64,550/12, max $50,000 INFO-1087489; in-module totals: 01 $19,252/13 · 02 $83,580/28 · 03 $47,014/56 · 04 $48,697/41 · 05 $15,468/6 · 06 $67,914/17). Only one row carries a non-integer bounty (INFO-419883 $802.2).
- Per-CVE rows: 12 of 362 carry non-empty `cve_ids` (concentrated in module 05: CVE-2015-3044 → CVE-2024-3416, plus INFO-231917, 508490, 952771, 1575014-class rows elsewhere). CVE counts are library facts, never added to bounty math.

## 4. Era discipline

- Rows are h1-brain disclosures spanning the corpus era (2013–2025-era disclosures, incl. INFO-2599391 CVE-2024-3416). All are *disclosed* reports; undated metadata rows (the 22 merges carry `weakness_name=None` in the DB) are classed by title/body only.
- Post-roster modern hardening enters only as playbook P4 fingerprints, never as corpus doctrine or class counts.
- Program handles in the register are DB `program_handle` values verbatim (`security` = HackerOne's own program; `ibb` = Internet Bug Bounty umbrella).

## 5. Weakness-tag reality

- Module weakness census (DB labels): 01 all `Information Disclosure` (21) · 02 all `Information Disclosure` (51) · 03 `Information Disclosure` 108 / `Privacy Violation` 17 / `Cleartext Storage` 3 · 04 `Information Disclosure` 88 / `Cleartext Storage` 12 / `Privacy Violation` 4 · 05 all `Information Disclosure` (17) · 06 `Information Disclosure` 17 / `Privacy Violation` 2 / `None` 22 (merges).
- **Bodies win**: INFO-1575014 is a path-traversal PII row taught in module 04 by mechanism; INFO-472013 is a state-toggle row in module 03 though its effect (public tweets) is a consent failure; INFO-53004 is a DNS-rebinding row whose *content* was (benignly) disclosed. The register keeps the DB label; the modules classify by behavior. Several titles are mislabels of class (SSRF, RCE, ATO, CSRF, takeover) whose *disclosure leg* is what this vault prices.

## 6. Limits & era honesty

1. **Pool discipline**: the vault headline must always state its pool. Bucket-340 ($217,375/149, max $25,000) is class-pure; the merges add $64,550/12 and the corpus max ($50,000, INFO-1087489). No total in the vault folds the merges silently.
2. **Metadata-only rows** (6 GHSL one-liners, §2): $13,400 with no readable body. They anchor the adjacent module's money; they prove nothing about technique.
3. **Bounty withholding**: 201/362 rows carry no figure. The paid set (161) skews toward narrow executable proofs; the unpriced set toward broad capability claims — a publication artifact as much as a triage signal (see each module's §6).
4. **Program skew**: `security` (83 rows) is HackerOne auditing itself; per-field flat pricing reflects that program's tiers. Cross-program rate comparisons (e.g., $2,500 Team fields vs $2,500 Shopify order lookups) compare different programs' tables, not one market.
5. **Quote discipline**: every blockquote across the six class modules, README, and playbook is byte-true to `references/archive/INFO-bodies-full-dump.txt`; `(sic)` marks author typos. No invented quotes, no paraphrase passing as quotation. Verification log: byte-exact check of every `> ` blockquote against the dump (see build report).
6. **Chain-origin rows** (module 06's SSRF/DNS-rebinding/ATO legs) price the *disclosure leg* only; the origin class's vault prices the exploit. Cross-citations name both so neither vault double-counts the bounty.
7. **No live testing** was performed. Endpoint evidence (HackerOne GraphQL fields, GitLab serializers, Shopify preview hosts) is historical record from disclosed reports; validate against the hunt-graphql / hunt-api-misconfig / hunt-auth skill matrices before writing any report.
