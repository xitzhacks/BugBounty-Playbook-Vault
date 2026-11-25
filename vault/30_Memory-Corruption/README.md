---
title: "Vault/30_Memory-Corruption — buffer/heap/UAF/interpreter memory-corruption playbook set (last vault)"
type: index
category: "Memory Corruption (all memory-safety classes in one vault: heap/classic buffer overflow, use-after-free & double-free, out-of-bounds overread/read, integer overflow & type confusion, null-deref & stack crashes, adjacent & unclassified noise)"
built: "2026-11-07"
evidence: "352 vault rows (336 memory-corruption bucket + 16 unclassified merges) from the h1-brain DB (3,673 rows; sha256 8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4) — all 352 bodies archived verbatim · 320 bucket bodies read end-to-end (16 ≤100-char link-only stubs) · 137 bucket rows with CVEs"
bounty: "$250,652.09 vault total (155 rows) · bucket $233,652.09/145 ($10,000 max, 3-way tie) + unclassified merges $17,000/10 · module floors: Heap $76,573/44 · UAF $41,300/23 · OOB $30,192/27 · Int $10,100/19 · Null $74,487/31 · Adjacent $1,000/1 + $17,000/10 merges"
companion_vaults: "../RCE · ../Race-Conditions · ../21_Denial-of-Service (build-pending) · ../12_Business-Logic (build-pending) · ../Information-Disclosure (build-pending)"
case_id_scheme: "MEM-<HackerOne report id>"
quote_rule: "byte-true, (sic)-marked, from archived bodies only (references/archive/MEM-bodies-full-dump.txt); link-only rows never quoted"
---

# Vault/30_Memory-Corruption — the memory-corruption playbook set

One vault, six memory-safety classes, last in the build order: this corpus pays **program economies**, not bugs — flat tiers for Flash classes, $100–$10,000 for sandbox crash rows, CVE bookkeeping for library crashes, and valve file/service primitives at five figures. The class is IBB-heavy by definition: 224 of 336 bucket rows sit on the `ibb` program, and no web-native target in the corpus carried a memory award above four figures.

## Scoreboard (352 rows · 155 paid · $250,652.09 · max $10,000)

| Case | Title (short) | Program | Bounty |
|---|---|---|---|
| MEM-542180 | Left4Dead2 NAV file → EIP control | valve | **$10,000** (max) |
| MEM-826026 | Kernel UAF → arbitrary R/W (vault max) | playstation | **$10,000** |
| MEM-186723 / MEM-189633 | mruby crash crown ×2 | shopify-scripts | **$10,000** each |
| MEM-184661 / MEM-184857 / MEM-185794 | mruby initialize_never_ran / boxing tier | shopify-scripts | $8,000 each |
| MEM-1180252 | Steam SILK voice decoder overrun | valve | $7,500 |
| MEM-807772 | OOB → vtable call (entity index) | valve | $7,500 |
| MEM-119652 / MEM-151039 / MEM-56385 / MEM-151043 | Flash heap/UAF anchors | ibb | $5,000 each |
| MEM-2585375 | Apache mod_proxy NULL-deref DoS (CVE-2024-38477) | ibb | $4,920 |
| MEM-630462 | PuTTY SSH1 heap overflow | putty_h1c | $3,645.90 |
| MEM-1977252 | Brave V8 wallet UAF | brave | $3,000 |
| MEM-489102 | VLC stack overflow, SEH overwrite | vlc_h1c | $2,817.28 |
| MEM-1378946 | GHSL CodeQL CWE-787 query (max query row) | github-security-lab | $4,500 |
| MEM-2526041 / MEM-2526051 | nginx HTTP/3 termination | ibb | $2,600 each |
| MEM-2658447 | NGINX mp4 overread (CVE-2024-7347) | ibb | $2,142 |
| MEM-746766 | Python AST OOB ×2 CVEs | ibb | $2,000 |
| — | 145 further bucket-paid rows + 10 merge-paid query rows | — | −$133,427 |

Vault composition: ibb 224 · shopify-scripts 64 · valve 10 · torproject 7 · putty_h1c 5 · notepad++ 4 · nodejs 4 · ruby 3 · curl 3 · vlc/kubernetes/brave 2 each. IBB carries 49.9% of bucket bounty ($116,612/94); the mruby sandbox carries 27.4% ($64,000/32).

## Vault map

| File | Content |
|---|---|
| `MEM-Testing-Agent-Playbook.md` | Agent-facing operational playbook: economy classification (P0) → native surface inventory (P1) → probe protocol (P2) → proof ladder (P3) → hardening fingerprints (P4) → pre-report gates (P5) |
| `Heap-Class-Classic-Overflow.md` | 115 rows ($76,573): valve file-parser lane (NAV/SILK), Flash flood at $2,000 flat, PuTTY protocol parser, tcpdump fleet |
| `Use-After-Free-and-Double-Free.md` | 53 rows ($41,300): PlayStation kernel UAF → arbitrary R/W, Flash fleet, mruby sandbox UAFs, PHP unserialize fleet |
| `Out-of-Bounds-Overread-Reads.md` | 68 rows ($30,192): valve entity-index pattern, NGINX/Python parsers, PHP exif/GD gdb format, tcpdump $0 wall |
| `Integer-Overflow-and-Type-Confusion.md` | 33 rows ($10,100): fread/gzread null-write, itertools type confusion, 51-byte PHP batch |
| `Null-Deref-and-Stack-Crashes.md` | 59 rows ($74,487): mruby crash crown ($10,000 × 2, $8,000 × 3), service CVE crashes, unpaid-parrot tail |
| `Adjacent-and-Unclassified.md` | 24 rows ($18,000): GHSL CodeQL-query economy, leak/disclosure pair, hardening + joke + metadata noise |
| `references/source-index.md` | Provenance (h1-brain DB, sha256, 3,673 rows), funnel (3,673 → 336 → 352), bounty accounting, era discipline, 5 limits |
| `references/case-register.md` | 336-row full register + 16-row merge appendix: weakness/asset/CVE/bounty/module per row |
| `references/archive/MEM-bodies-full-dump.txt` | All 352 bodies verbatim (anchor for every quote) |
| `references/archive/classes.json` | Frozen module assignment (352 ids, each exactly once) |
| `references/archive/meta.json` | Build metadata (row counts, provenance pin) |

## Cross-vault links

- `RCE/` — its module 04 covers the same Flash/mruby economy from the execution angle; MEM mruby crown rows (Null module §2) are the successor reports to RCE-181879/181321 (RIP control / type confusion). The deserialization-vs-parser split (RCE 03 vs MEM 01/03) is documented per row.
- `Race-Conditions/` — MEM-826026's kernel UAF is a race (free-while-in-use); the Race playbook's sync ladder supplies its §2 exploit file.
- `21_Denial-of-Service/` (build-pending) — service CVE crashes in Null module §4 are its mirror territory; arrival-condition pricing is shared.
- `Information-Disclosure/` (build-pending) — Adjacent §3's disclosure pair (mruby heap-pointer leaks) are its pointer-leak canon inside a memory vault.
- `Cryptography/` (build-pending) — Adjacent §2's GHSL query CWE list (787/190/788) overlaps its integer-conversion class.

## Limitations

1. **Count basis vs master list.** Master row 30 cites "319 + 70 + 54" BBH-historic counts; this vault quotes only the h1-brain DB subset (336 bucket + 16 merges = 352). Bucket bounty is a corpus floor; `-` rows are undisclosed figures (Race rule), not failed reports.
2. **Weakness label ≠ taxonomy.** `Memory Corruption - Generic` (185/336) swallows every class; module split is mechanical (module_map) with borderline rows labeled adversely (MEM-113120 integer-overflow in Null module; MEM-478368 OOB write in OOB module).
3. **Link-only rows.** 10 bucket rows are ≤100-char ticket links (the 51-byte PHP batch, unserialize farm); 10 merge rows are GHSL one-liners. Methodological claims rest only on full bodies.
4. **Low web ROI.** This is the last vault by design (master row 30, "last, low ROI"): every five-figure row's target is game/console/sandbox. Web-only programs should not invoke the MEM playbook.
5. **Chainpay vs pure.** Only the kernel R/W UAF and the valve OOB→vtable priced above $5,000; pure crash rows cap at $2,000 (CVE-tier). Do not read EIP-control price as typical.
6. **Era honesty.** Tool choices are era evidence (2013–2025 CVE tags): Flash-era flat tiers, PHP 51-byte batches, and mruby crash prices are historical records, not current tables — P4 labels what moved.
7. **QA.** Every blockquote across the six modules and the playbook was byte-verified against the dump; `(sic)` marks author typos. Adverse merges are labeled, never normalized; every bucket id appears exactly once in `classes.json`.


<!-- CASESTOCK-LINK:BEGIN -->

## Case stock — vault (`_VAULT/`)

**898 disclosed reports** routed to this category · 282 with a bounty figure · **$467,758** · 789 full write-ups stored locally.

- Full list: [`_VAULT/by-vault-category/30_Memory-Corruption.md`](../_VAULT/by-vault-category/30_Memory-Corruption.md)
- Query: `sqlite3 ../_VAULT/reports.sqlite "SELECT id,bounty,title FROM reports WHERE ..."`
- Pull one write-up: `python3 ../_VAULT/scripts/extract_report.py <id>`

| Top paid | Program | Bounty |
|---|---|---|
| [2177925](https://hackerone.com/reports/2177925) Remote vulnerabilities in spp | PlayStation | $12,500 |
| [186723](https://hackerone.com/reports/186723) Crash: Overwriting NoMethodError with a builtin class crashes/corrupts memory | shopify-scripts | $10,000 |
| [189633](https://hackerone.com/reports/189633) Certain inputs cause tight C-level recursion leading to process stack overflow | shopify-scripts | $10,000 |
| [542180](https://hackerone.com/reports/542180) Malformed NAV file leads to buffer overflow and code execution in Left4Dead2.exe | Valve | $10,000 |
| [826026](https://hackerone.com/reports/826026) Use-After-Free In IPV6_2292PKTOPTIONS leading To Arbitrary Kernel R/W Primitives | PlayStation | $10,000 |

_refreshed 2026-11-17 from the public HackerOne disclosed-report dataset_
<!-- CASESTOCK-LINK:END -->
