---
title: "DOS source index — provenance, funnel, classification mechanics, limitations"
type: source-index
built: "2026-11-07"
---

# Source index — Denial of Service build

## 1. Roster provenance (h1-brain DB, sha256, 3,673 rows, funnel to 221)

- **Primary source**: `/home/user/tools/h1-brain/disclosed_reports.db` — the h1-brain pre-built SQLite corpus of publicly disclosed, bounty-awarded HackerOne reports (**3,673 rows**, verified). The DB file's sha256 is `8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4` (matches the repo's Git-LFS pointer; no live HackerOne fetch this build). Table `disclosed_reports`, columns `id, title, vulnerability_information, weakness_name, program_handle, asset_identifier, asset_type, cve_ids, bounty_amount`.
- **Bucket definition**: `weakness_name = 'Uncontrolled Resource Consumption'` (CWE-400). The DB contains exactly **221 such rows** (every bucket row verified: classified `src` = the same weakness string, DB `weakness_name` = the same for all 221). That is the funnel head for this vault: **3,673 → 221**.
- **Working copies**: `/home/user/opencode-work/h1brain/{classified.json, module_map_all.json, unclassified_classified.json, unlabeled_rows.json, dos_digest.md}`. In-vault archive: `references/archive/DOS-bodies-full-dump.txt` (240/240 bodies, verbatim), `references/archive/classes.json` (frozen module assignment for all 240 rows).
- **Byte-identity check**: every classified `body` is byte-identical to the DB `vulnerability_information` for all 221 bucket rows and all 19 merges (verified 240/240). The dump's bodies are therefore simultaneously the classifier's and the DB's — quotes verify against either.

## 2. Classification funnel

1. **Bucket net**: exact-weakness match → **221 rows**. All 221 bodies read end-to-end.
2. **Module split** (frozen in `classes.json`, from `module_map_all.json` dos assignment):
   `native_memory_crash_dos` 75 · `redos_regex_cpu_exhaustion` 20 · `http_protocol_flood_dos` 10 ·
   `webapp_resource_abuse` 100 · `_adjacent` 16. Sum: **75+20+10+100+16 = 221** — every
   bucket row in exactly one module, no dupes, no drops (verified mechanically).
3. **Unclassified-merge pass**: `unclassified_classified.json` assigns 19 dos ids from the
   classifier's `unclassified` pool (468 rows in `classified.json`; 506-row
   `unlabeled_rows.json` reflects classifier-snapshot drift). All 19 carry
   `weakness_name None` in the DB — the exact-weakness net necessarily missed them.
   `module_map_all.json` lists them under `_adjacent_unclassified`; this vault folds them
   into the last module (`05_Adjacent-And-Unclassified.md`, 35 rows total).
   Vault corpus: **221 + 19 = 240 rows**. The 19 merges are quarantined in the register's
   separate table and in module 05's case-stock so the bucket arithmetic stays
   re-derivable.
4. **Module assignment is by body read, not title.** The split's borderline cases are
   visible in the case-stock mechanisms: e.g. DOS-1746098 (locale-as-regex) and
   DOS-2258758 (UsernameField unicode) sit in 04 (endpoint) rather than 02 (engine);
   The Rack/Django parser rows split across 04 and the merge lane by label. Where the
   map and the body disagree, the body decided the prose and the map decided the
   `classes.json` row (recorded in the mechanism column).

## 3. Bounty accounting

- **Rule**: DB `bounty_amount` where present (verified: classified `bounty` == DB
  `bounty_amount` for all 221 bucket rows, 0 mismatches); `None` recorded as `-`
  (no figure — not evidence of non-payment).
- **Bucket**: **$238,864 / 106 rows** (115 rows carry no figure). Module ledger:
  01 $149,500/38 · 02 $12,395/10 · 03 $20,250/8 · 04 $51,219/47 · adjacent $5,500/3.
- **Merges**: **$37,004 / 11 rows** (8 carry no figure).
- **Vault grand total: $275,868 / 117 rows.** Max single row $10,000 (9 rows: the
  `shopify-scripts` mruby cluster ×8 plus merge DOS-185775). No `$0` rows: the corpus
  carries figures or `None`, never zero — a `-` must never be quoted as "unpaid".

## 4. Era discipline

- Rows span the full disclosure era (2015 mruby crash wave → 2025 CVE coordinations).
  The money is bimodal: the 2015–2016 `shopify-scripts` flat-tier era (modules 01,
  $149,500) and the 2023–2025 HTTP/2 + parser-CVE wave (modules 02/03, mostly
  vendor-coordinated). Tooling and fix shapes are historical record, not current
  guidance; the playbook's P4 is labeled "post-corpus hardening, outside the corpus".
- **Patch-shape stratum**: native rows quote their fixes (pin the core class 181910;
  guard the codegen transform 181828; cap the length arithmetic 112723). Parser rows
  quote their CVE and fixed version. Neither stratum is silently updated to today's
  versions — if a fix landed after the row, the row's body is the record.
- No live testing was performed — validate against the DOS playbook's P0 envelope
  (single-request, bounded, policy-permitted) only.

## 5. Limitations

1. **Label leakage (measured, not hypothetical).** The exact-weakness bucket missed
   $37,004 (13.4% of vault money) sitting behind `weakness_name None`. A label-only
   vault is a lower bound; this vault's merge pass recovers the measured 19, but the
   remaining 449 unclassified rows were not keyword-swept full-text for DoS this build.
2. **Bounty withholding.** 123 of 240 rows (115 bucket + 8 merges) carry no figure.
   Bounty-unknown is not bounty-zero; the corpus floor ($275,868) is not a total.
3. **Metadata-only rows.** DOS-801230 and DOS-1061211 are 54-byte GitHub-Security-Lab
   one-liners carrying $2,800 with no quotable technique. DOS-153093 is advisory-only.
   Nothing was invented for them; no quotes exist for them.
4. **Weakness labels ≠ taxonomy.** All 221 bucket rows share one weakness string, yet
   the corpus spans interpreter crashes, regex bombs, HTTP/2 floods, endpoint burns and
   cache poisons. Modules classify by body behavior; the register preserves the archive
   label.
5. **Quote discipline.** Every blockquote across the five modules, README and playbook is
   byte-true to `references/archive/DOS-bodies-full-dump.txt`; `(sic)` marks author
   typos ("derefence", "my local  web server" doubled spacing, "4.the" run-in).
   Verification method and results are reported in the build log (§6).
6. **Chainpay vs pure-DoS.** The vault's two largest webapp figures (1543718 $7,640;
   2105808 $5,000) pay for *measured shared-victim loss*, not chained primitives — DoS
   is the destination here. Adjacent-pool rows pay because another class (cache
   poisoning) supplies the availability loss; they are pointers, not claims.
7. **Snapshot date.** The DB snapshot (disclosures through 2025) freezes the corpus;
   post-2025 advisories (e.g. later Rack/Django/ReDoS fixes) are out of scope and
   would enter as a v2 sweep.

## 6. Quote verification (build log)

After writing, every blockquote in the vault's markdown was mechanically extracted and
checked against `DOS-bodies-full-dump.txt` (exact-line match after `
`-stripping, plus
whitespace-normalized substring match). Results and the classes.json membership check
(each of the 221 bucket ids appears exactly once; each of the 19 merges appears exactly
once; no other ids) are reported alongside this file's build. Any quote failing both
checks was fixed to the byte-true line before delivery.
