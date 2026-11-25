---
title: "Memory-corruption source index — provenance, funnel, classification mechanics, limitations"
type: source-index
built: "2026-11-07"
---

# Source index — Memory Corruption build

## 1. Corpus provenance

- **Primary source**: `/home/user/tools/h1-brain/disclosed_reports.db` — the h1-brain pre-built SQLite corpus of publicly disclosed, bounty-awarded HackerOne reports (3,673 rows verified at build time). sha256 verified: `8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4` (identical to the Race vault's provenance pin). No live HackerOne fetch this build.
- **Row fields**: `id, title, vulnerability_information, weakness_name, program_handle, asset_identifier, asset_type, cve_ids, bounty_amount`. Full report bodies in `vulnerability_information`.
- **Working copies**: `/home/user/opencode-work/h1brain/{classified.json, module_map_all.json}` (classifier output + module merge map). In-vault archive: `references/archive/MEM-bodies-full-dump.txt` (352/352 bodies), `references/archive/classes.json` (frozen module assignment), `references/archive/meta.json`.

## 2. Classification funnel

1. **Bucket extraction**: `classified.json` key `memory-corruption` = **336 rows** (`src` ∈ the 8 weakness labels: Memory Corruption - Generic 185 · Buffer Over-read 34 · Heap Overflow 27 · Use After Free 26 · Classic Buffer Overflow 21 · NULL Pointer Dereference 18 · Out-of-bounds Read 14 · Stack Overflow 11).
2. **Module merge map**: `module_map_all.json → memory-corruption` splits the bucket into **heap_classic_overflow 115 · use_after_free_double_free 53 · out_of_bounds_overread_read 68 · integer_overflow_type_confusion 33 · null_deref_stack_crashes 59 · _adjacent 8** (= 336 exactly, each id once).
3. **Unclassified merges**: `_adjacent_unclassified` = **16 rows** currently in `classified.json → unclassified` (468 rows): 10 GHSL CodeQL-query reports, 5 ibb upstream-link retries, 1 mruby `mrb_vm_exec` UAF. They never were bucket members. Merged into the vault's final module per the build brief; frozen disjointly (352 vault ids total).
4. **Freeze**: every body preserved in `MEM-bodies-full-dump.txt` so every quote is checkable; `classes.json` records the assignment. DB-side parity verified: bounty identical on all 336 bucket rows and all 16 merges, weakness/src identical on all 336 bucket rows, CVE field populated on 137 bucket rows, vulnerability_information non-empty on all 336 (16 bodies ≤100 chars — link-only stubs).

## 3. Bounty accounting

- **Rule**: DB `bounty_amount` where present (dump carries the number); `None` recorded as `-` (no figure in DB — never read as "unpaid", mirroring the Race vault).
- **Corpus**: 145/336 bucket rows carry figures, total **$233,652.09**; max $10,000 (three-way tie). Vault incl. merges: **$250,652.09/155**. Module totals: Heap $76,572.81/44 · UAF $41,300/23 · OOB $30,192/27 · Int $10,100/19 · Null $74,487.28/31 · Adjacent $1,000/1 (+ $17,000/10 merges). See `case-register.md`.
- **Economy split**: 94/145 paid rows are `ibb` ($116,612 = 49.9% of bucket money); the mruby sandbox (`shopify-scripts`) is the second economy at $64,000/32; valve's 10 rows carry $27,850 (only 4 paid). CEILING = behaviorally banked: no web-native target in this corpus carried a five-figure memory award — every $7,500+ row's target is a game/console/sandbox.

## 4. Era discipline

- **Flash era (2013–2016)**: 22 Flash-titled bucket rows; the heap/UAF fleet survived via Adobe's flat tiers. Every quote from this fleet is labeled by report order (the body *is* the finding; CVEs are assigned in the body).
- **PHP upstream-ticket era (2015–2017)**: ~40 rows are bugs.php.net tickets with H1 wrappers ($500 flat): the 51-byte batch, the unserialize-UAF farm, the GD/exif fleet.
- **mruby sandbox era (2016)**: 64 `shopify-scripts` rows carry the crash-report density of the corpus (SIGSEGV/ASan dumps + one-line Ruby), with the crown claims reaching $10,000.
- **Modern tail (2019–2025 CVE tags)**: NGINX (CVE-2024-7347/-35200/-31079), Apache (CVE-2024-38477), Brave, kubernetes, curl/punycode spawns. These re-observe that memory corruption is paid software-side pricing — hardening practice for these targets is the modern posture, not the corpus's Flash-era tier tables.

## 5. Limits & era honesty

1. **Count basis**: the master list (row 30) cites BBH-historic counts (319 + 70 + 54); this vault quotes only the h1-brain DB subset (336 bucket + 16 merges = 352). Bucket bounty is a corpus floor: `-` rows are undisclosed figures, not failed reports.
2. **Weakness labels ≠ taxonomy**: `Memory Corruption - Generic` (185) swallows heap, UAF, OOB, integer and type bugs alike; the module split is mechanical over the CDF (`classes.json`), with borderline rows labeled adversely (MEM-113120 integer overflow in Null module per the map's override; MEM-478368 OOB write in OOB module).
3. **Link-only rows are metadata-only**: 16 bucket rows have ≤100-char bodies (ticket links); plus 10 merge rows are GHSL one-liners. Methodological claims (probe ladders, price lists) are built only from full bodies; link rows are candidates only.
4. **Chainpay vs pure**: the corpus's only kernel UAF ($10,000) paid as an arbitrary-R/W primitive and the only valve OOB→vtable ($7,500) similarly; pure ledger-tier (crash-only CVE) rows top out at $2,000 (nginx CVE-tier). Do not read EIP-control price as typical.
5. **QA discipline**: every blockquote across the six class modules and the playbook was byte-verified against `references/archive/MEM-bodies-full-dump.txt`; `(sic)` marks author typos. Adverse merges are labeled (§3–§4), never normalized.
