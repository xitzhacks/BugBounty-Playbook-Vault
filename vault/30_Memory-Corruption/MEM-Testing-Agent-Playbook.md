---
title: "MEM Testing Agent Playbook — memory corruption (IBB-heavy, low web ROI)"
type: agent-playbook
category: memory-corruption
cwe: "CWE-119, CWE-122, CWE-416, CWE-125, CWE-190, CWE-476"
built: "2026-11-07"
evidence: "352 vault rows (336 memory-corruption bucket + 16 unclassified merges) from the h1-brain DB (3,673 rows; sha256 8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4) · $250,652 total · 155 paid · max $10,000 · 6 class modules"
companion_modules: "heap-classic-overflow · use-after-free-double-free · out-of-bounds-overread-reads · integer-overflow-type-confusion · null-deref-stack-crashes · adjacent-and-unclassified"
quote_rule: "byte-true, (sic)-marked, from archived bodies only (references/archive/MEM-bodies-full-dump.txt); link-only rows never quoted"
---

# MEM Testing Agent Playbook

Executable protocol for the memory-corruption class, derived from 352 archived bodies. This is the **last vault** (master row 30) and the one with the lowest web ROI: the corpus pays IBB orders of magnitude away from the web money — flat-rate interpreter crashes, Flash tiers, sandbox prices, and valve file/service primitives. Invoke this playbook only when the target has a *native counterpart with a paid track*: an interpreter sandbox, a file-format parser in C, a game/engine asset pipeline, a protocol dissector, a browser/V8 extension. For web-only targets, memory-corruption rows are *not* your season.

Crown-jewel doctrine up front: **payouts track the program's economy, not the bug's severity**. A heap-UAF in a sandbox with a published table ($100–$10,000) out-prices a kernel UAF on a bare `ibb` CVE row ($0); valve prices *arrival conditions* (server-sent files, client-driven precaches) over primitives; tracker rows that say "crash" get CVE bookkeeping. The playbook engages by economy, not by word.

## P0 — Program classification & policy read (before any payload)

1. **Classify the program's economy**:
   - **Language-VDP / interpreter sandbox** (PHP/Perl/Python/ruby upstream-via-ibb; Shopify `shopify-scripts` mruby): yields per-bug flat rates, and in this corpus the *only* reliably paying crash lane. MEM module 05's crown (crash rows $8,000–$10,000; NULL-deref $100–$1,000) is the historical price list for today's interpreter tables.
   - **IBB engine tracks** (Adobe Flash-era, valve, tor, curl, putty): prices by asset class — browser plugin (flat tiers), game studio (reach-driven), open-source library (CVE bookkeeping mostly $0–$2,000).
   - **Detector/query track** (GitHub Security Lab rows): pays *queries* ($500–$4,500, adjacent module §2), not bugs — file query-pattern work only if the program explicitly accepts CodeQL-style deliverables.
2. **Read policy depth-first**: allowed asset types (the DB's `asset_type` — HARDWARE rows like the PlayStation kernel crown MEM-826026 sit in hardware programs), disclosure preconditions (Flash: CVE + advisory before H1), and the *format the program accepts* (upstream ticket link alone = $500 flat, module 04 §4).
3. **Kill-gate**: no testing yet — P0 produces the *economy envelope* only. If the target program carries no native assets, stop here (non-goals).

## P1 — Surface inventory (the native hunt queue)

Map the target into corpus-evidenced shapes, in bounty order:

1. **Sandboxed interpreters** — anything evaluating attacker strings in a constrained VM (module 05's mruby crest, crown $10,000/hit). Inventory method-call surface second: `initialize_copy`/`initialize` pairing (MEM-184661/184857), error-class rebinding (MEM-186723), boxing introspection (MEM-185794).
2. **File-format parsing** — uploaded/rendered formats (module 01: NAV/BMP/SILK/playlist), each with the trusted-length-field geometry (§3 source: `nPayloadSize` arithmetic; `nSize` fields; image `colorsTotal`). Inventory: every size coming from file bytes, not symbols.
3. **Network message handlers** — indexed lookups (module 03: `entitylist[ent_idx]`; symptom: lower bound only). Grep for `>= 0` without `< max` in handler code as the enumeration primitive.
4. **Message/format deserializers** — `unserialize()`-adjacent VM surfaces (module 02's PHP fleet) and `__setstate__` paths (module 04 MEM-175091). Inventory the trusted-types map.
5. **Interfaces that are not bugs**: hardened-client posture (adjacent §4: ASLR/DEP checklist), informational leaks (realloc), query-detection authoring, jokes. Keep them as *separate* report files, never as corruptions.
6. **Losing lanes to de-list now**: generic web apps with no native parsing tier; SNI/URL-parsing "ASM-surface" sweeps; FontAsset-map hunting — outside this corpus's evidence.

## P2 — Probe protocol (from cheapest signal to hardest)

Per candidate surface, in corpus-chronological order, with pricing attached:

1. **Integer-size probe** (module 04 §4): fuzz arguments that change allocation sizes near `INT_MAX`/`UINT_MAX` — the 51-byte batch's entire method (one function at a time, ticket per hit). gdb-dump the sign of the wrapped length: when the length prints negative, your overflow is the document.
2. **Truncated-input probe** (module 01 §5 / module 03 §4): supply files with declared sizes *larger* than payloads (SSH1 keys, image dimensions, mp4 atoms); check for unchecked copy loops. PuTTY's SSH1 `servkey`/`hostkey` row (MEM-630462) is the template.
3. **Recursion probe** (module 05 §2): define `to_i`-style coercion loops (`'' * self`) and self-referential bindings — if the guard is on the *language* stack, a C-level cycle spends nothing of it. Expect `$10,000`-class outcomes in sandboxes that re-implement the guard.
4. **Rebinding probes** (module 05 §2/§3): overwrite builtin constants with builtin classes (`NoMethodError = Fixnum`), remove standard methods (`NilClass.remove_method :to_s`), skip `initialize` and hit the copy/initialize pair. Read the move, not the VM: lifecycle-state confusion out-prices vm crashes.
5. **Array-index bound probe** (module 03 §2): send `ent_idx = max+1` faces: `2^31-2`, `-1`, `0x7fffffff`; if a handler lacks the upper check, first symptom is a stray virtual call, second is a crash.
6. **Race-synchronization probe** (module 02 §2): where the free-path spans threads (workers, token-caches, shared arrays), coordinate two threads against the same slot — the corpus's kernel crown is one lock away from its frees. (Sync tooling per the Race vault.)

## P3 — Proof ladder (the modest demonstrations paid)

1. **Interpreter format** (module 05 §§2–3): one-line Ruby + ASan/`[BUG]` trace + the reach paragraph ("*doesn't* affect mruby-engine with the current instruction limit…" — name what it costs the victim to raise) + local fix delta. **Crashes read as *unproved-until-print***.
2. **File/screen format** (module 01 §2): minimized crafted file + linear steps + "EIP becomes 0x41414102"-class register observed. No infoleak required to clear triage when the shipped module lacks ASLR (valve pattern).
3. **Extension/renderer format** (module 02 §3): V8 object-installation code walk proving a retained freed-object handle (Brave's `JSEthereumProvider` walk); price $3,000 at that shape.
4. **Decompiler-reference format** (module 03 §4): breakpoint numbers at the arithmetic past the array (`gd_interpolation.c:890`, `_gdContributionsAlloc (line_length=13, windows_size=9)`) — transcript is the proof.
5. **Upstream-ticket format** (module 04 §4): stable public ticket + fixed-in-days log:

> Memory corruption issue on mbstring extension, issue reported to PHP developers on 2016-03-26,  fixed 2016-03-29 and released at 2016-03-31, affected PHP 5.5 , PHP 5.6 and PHP 7.

6. **Honest-boundary bonus** (module 04 §2): show the byte you *cannot* write:

> Integer underflow in the  fread/gzread length parameter allows to write an arbitrary null byte on 64 bit platforms. This was identified with the help of ASAN and a custom fuzzer.

One arbitrary null byte, with debugger print of negative `len`, out-priced the loudest claim in the module.

## P4 — Modern hardening fingerprints (never corpus doctrine)

The corpus spans 2014–2025 CVE tags; today's hardening expectation is the *absence* of these surprises:

- **Heap/overflow**: allocator hardening (`_FORTIFY_SOURCE`, Clang SafeStack) — MEM-351014/MS's classic write class survived only in non-hardened Steam-era clients; note every corpus crash's build flags where they appear (PuTTY's ASan matrix row, clang 7.0.1).
- **Sandbox competition** (mruby-engine, Shopify script service, Worker Threads guards): the "doesn't affect mruby-engine with the current instruction limit" caveat is today's *actual control* — test both vanilla interpreter and the sandboxed product; report the **difference**.
- **Modern consumers where this class lives**: Browser engine (V8/TurboFan) extensions, game/sandbox asset codecs, zip/mp4 demuxers, chat-style voice-encoder stacks (SILK descendants), AVIF/HEIF, language runtimes (Rust-vs-C FFI seams), firmware update parsers.
- **Pose as the consumer**: never file a server-side "crash-only" row for a general web program; the corpus's standalone crashes are paid *inside* sandbox/VDP/IBB economies. If the client is the victim (module 01's BMP), the server is the delivery — state which side of the pipe your PoC lands on.

## P5 — Pre-report gates (kill-gates)

1. **Class gate** — name the memory primitive precisely (heap overflow vs stack overflow vs UAF vs OOB read; size_t wrap vs type confusion vs NULL deref). Title-convention alone ("Possible memory corruption") is silent in the register — be mechanical, not lyrical.
2. **Identity gate** — each quote-level claim must be reproducible from the archived body. Rows whose bodies are a single ticket link (51 bytes long) get cited as *corpus evidence of the form*, never quoted for technique.
3. **Drive the consumer** — the report must state what the freed/overwritten object is reused *as* (kernel pointer, vtable slot, SEH chain, worker thread). "Crash" `allocs a null byte write' gets the null byte's price — proportioned accurately — not RCE's.
4. **Arrival gate** — prove delivery lands on the victim without the victim's consent ergonomics being discounted into the payout: valve's player delivering `overviews/%MAPNAME%.bmp` at connect paid $2,000; precache-requiring attackers at $350 (MEM-505173). State the user interaction step.
5. **Query/Query gate** — know whether you're reporting a bug or promoting a detection: the GHSL rows paid $500–$4,500 for *patterns*, and every pattern-authored corpus row went to OWASP-query libraries. Get triaged there, or rework into per-bug reports.
6. **Noise gate** — the joke/metadata rows are the gallery: `Hi team adding the flag here` (MEM-1217702), patch-mail rows (MEM-203595), hardening-only rows (MEM-380102). If your row's reach reduces to "we think protections are absent" or "the flag is here", relabel before filing.

## Module ↔ phase table

| Phase | Corpus evidence (modules) | Anatomy of the paid pattern |
|---|---|---|
| P1 inventories interpreters/file/voice/handlers | 01 (§§2–5), 02 (§2), 03 (§2), 04 (§3), 05 (§§2–3) | One trusted length field; one lifecycle pair; one unbounded index |
| P2 probes size, recursion, rebinding, race | 04 (§4), 05 (§2), 03 (§2), 02 (§2) | Boundary sizes, recursion-to-C-stack, `NoMethodError = Fixnum`, lock-vs-free |
| P3 proofs ladder, honest bounds | 01 (§2), 04 (§2), 05 (§§2–3), 03 (§4), 02 (§3) | EIP/pixel-at-0x13371337, one null byte, sandbox trace |
| P4 hardening fingerprints | 01 (§6), 03 (§5), 05 (§5), 02 (§6) | Tier ceilings, parser amputations, sandbox economics |
| P5 kill-gates | 04 (§6: link-only), 05 (§5: unpaid SIGSEGV tail), 06 (§§4–5: noise/query shelf) | Silent-payout definition of theory/claim/noise |

## Non-goals

- **Memory-corruption exploitation (heap feng-shui, ROP chaining, kernel privilege escalation primitives)**: the corpus pays *evidence of control*, not working chains. Rule-the-boundary demos (EIP reaches a signature address) are the vault's endorsed deliverable; shellcode development is out.
- **Classic buffer-overflow web RCE** beyond file/format delivery (the target genuinely consuming the file — module 01): header/URL/query-triggered "crashes" in generic web apps belong to the DoS vault, not this one; they price at $0 here.
- **Aggregate-DoS (rate-limit exhaustion / resource-consumption)**: the corpus's crash rows price *crash fidelity*, not volume; load-shedding belongs to the DoS vault.
- **Bypassing this playbook's P0 envelope**: the corpus is IBB-heavy — vendored/native assets only. If the program has none, do not relax the gates; refer out.
