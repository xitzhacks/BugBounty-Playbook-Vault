---
title: "Memory-corruption code execution — Flash VRP, phar & PHP genome, the mruby sandbox crash corpus, Python/Perl type confusion"
type: playbook
category: memory-corruption-execution
cwe: "CWE-787"
source_count: 37
full_bodies_available: 34
corpus: "h1.security.nathan.sx roster (150 rows), bodies via hackerone.com/reports/<id>.json"
list_accessed: "2026-11-04"
note: "Anchors: RCE-181879 (mruby Struct confusion, $18,000 json), RCE-181321 (mruby to_h UAF, $20,000 list), RCE-183356 (mruby bytecode, $10,000 json), the Flash quartet ($37,500 list), phar sextet ($4,500). Claims trace to bodies read 2026-11-04."
---

# Memory corruption → code execution — the sandbox crash economy

## 1. Overview

Thirty-seven rows, **$106,100/36 paid** — 39% of the vault's money in this module, the
single richest class in the build. Four lanes: (a) the **Adobe Flash quartet** — four
memory bugs each independently monetized ($10,000/$10,000/$10,000/$7,500 list through
the ibb program); (b) the **phar sextet** — PHP archive-parser memory bugs ($500-$1,000
each); (c) the **mruby crash corpus** — 21 rows where the Shopify sandbox (mruby-engine)
was ground down crash-by-crash, three flagship breaks paying $20,000/$18,000/$10,000 and
the crash batch flat-rated $100-$800; (d) **Python/Perl** engine bugs ($500+$1,000).
The doctrine this module teaches: a memory-safety bug in *any* interpreter or vm.c is a
code-execution candidate — crash reports were their own paid product line in this era.

**Case-stock (37 rows / $106,100):**

| Case | Target | Mechanism | Bounty |
|---|---|---|---|
| [RCE-181321](https://hackerone.com/reports/181321) | mruby (Shopify) | Array#to_h UAF via to_ary reentrancy → possible RCE | $20,000 (list) |
| [RCE-181879](https://hackerone.com/reports/181879) | mruby (Shopify) | Struct type confusion → RIP control | $18,000 (json) |
| [RCE-183356](https://hackerone.com/reports/183356) | mruby (Shopify) | `break`/`\|\|=` bytecode jump OOB → spurious bytecode | $10,000 (json) |
| [RCE-2106](https://hackerone.com/reports/2106) | Flash/ibb | type confusion → code execution (APSB13-28) | $10,000 (list) |
| [RCE-2170](https://hackerone.com/reports/2170) | Flash/ibb | double free → code execution (CVE-2014-0502) | $10,000 (list) |
| [RCE-47232](https://hackerone.com/reports/47232) | Flash/ibb | StageVideoAvailabilityEvent UAF → arbitrary code exec | $10,000 (list) |
| [RCE-47234](https://hackerone.com/reports/47234) | Flash/ibb | MessageChannel.send UAF → arbitrary code exec | $7,500 (list) |
| [RCE-104010](https://hackerone.com/reports/104010) | PHP (VDP) | SOAP serialize_function_call type confusion / RCE | $1,500 (list) |
| [RCE-104017](https://hackerone.com/reports/104017) | PHP (VDP) | str_ireplace arbitrary code execution | $1,000 (list) |
| [RCE-73237](https://hackerone.com/reports/73237) | PHP (VDP) | phar_set_inode stack buffer overflow | $1,000 (json) |
| [RCE-73238](https://hackerone.com/reports/73238) | PHP (VDP) | phar over-read in unserialize | $1,000 (json) |
| [RCE-104008](https://hackerone.com/reports/104008) | PHP (VDP) | phar_make_dirstream uninitialized pointer | $1,000 (json) |
| [RCE-192485](https://hackerone.com/reports/192485) | mruby | NULL deref (vm.c pool) | $800 (list) |
| [RCE-196380](https://hackerone.com/reports/196380) | mruby | NULL deref super() | $800 (list) |
| [RCE-196386](https://hackerone.com/reports/196386) | mruby | SIGSEGV vm.c:1272 (env->stack null) | $800 (list) |
| [RCE-197693](https://hackerone.com/reports/197693) | mruby | SIGSEGV vm.c:1681 (proc->body.irep null) | $800 (list) |
| [RCE-202582](https://hackerone.com/reports/202582) | mruby | NULL deref mrb_obj_instance_eval | $800 (list) |
| [RCE-202584](https://hackerone.com/reports/202584) | mruby | NULL deref mrb_vm_exec | $800 (list) |
| [RCE-207710](https://hackerone.com/reports/207710) | mruby | heap UAF (recursive fuzz) | $800 (list) |
| [RCE-210429](https://hackerone.com/reports/210429) | mruby | NULL ptr deref vm_exec | $800 (list) |
| [RCE-214845](https://hackerone.com/reports/214845) | mruby | SIGSEGV vm_exec | $800 (list) |
| [RCE-216700](https://hackerone.com/reports/216700) | mruby | heap UAF vm_exec | $800 (list) |
| [RCE-221251](https://hackerone.com/reports/221251) | mruby | heap-buffer-overflow READ vm.c:1556 | $800 (list) |
| [RCE-205536](https://hackerone.com/reports/205536) | mruby | UAF in mrb_vm_exec | $800 (json) |
| [RCE-210671](https://hackerone.com/reports/210671) | mruby | NULL pointer derefs vm_exec | $800 (json) |
| [RCE-222294](https://hackerone.com/reports/222294) | mruby | heap UAF vm.c:1247 | $800 (json) |
| [RCE-201903](https://hackerone.com/reports/201903) | mruby | segmentfault mrb_vm_exec (metadata-only) | $100 (json) |
| [RCE-192318](https://hackerone.com/reports/192318) | mruby | mrb_vformat heap overflow | $100 (list) |
| [RCE-203513](https://hackerone.com/reports/203513) | mruby | SIGSEGV vm.c:1312 | $100 (list) |
| [RCE-217097](https://hackerone.com/reports/217097) | mruby | SIGSEGV (method_missing, pc=0x0) | $100 (list) |
| [RCE-103990](https://hackerone.com/reports/103990) | PHP (VDP) | phar_get_fp_offset NULL deref | $500 (json) |
| [RCE-104026](https://hackerone.com/reports/104026) | PHP (VDP) | phar invalid free (tar metadata) | $500 (json) |
| [RCE-104027](https://hackerone.com/reports/104027) | PHP (VDP) | phar tar memory corruption | $500 (json) |
| [RCE-104005](https://hackerone.com/reports/104005) | PHP (VDP) | zend_eval_const_expr NULL deref | $500 (json) |
| [RCE-207983](https://hackerone.com/reports/207983) | Perl (VDP) | S_regmatch heap over-read (regexec.c:6057) | $1,000 (list) |
| [RCE-182169](https://hackerone.com/reports/182169) | Python (VDP) | FutureIter_throw type confusion | $500 (json) |
| [RCE-221287](https://hackerone.com/reports/221287) | libsass | Sass::Eval NULL deref (fuzz) | - |

(Note: 192485's body says the author could not exploit it — paid anyway at the flat rate.
The $18k row's substate: resolved, critical.)

## 2. The mruby crown: RIP control in the sandbox

RCE-181879 (critical, **$18,000 (json)**) is the cleanest statement of the lane's
endgame — instruction-pointer control inside a *sandboxed* interpreter, priced by what
the sandbox was protecting:

> I've been poking at mruby a bit more and I've found a vulnerability that allows an
> attacker to take control of the instruction pointer.

> I've attached a proof of concept script that when run in mruby will jump to
> `0x0000133713371337` and segfault.

> While the proof of concept script just jumps to an attacker controlled address and
> crashes, it would almost certainly be possible to achieve full remote code execution,
> especially given an arbitrary read/write primitive (which is easily created using the
> same techniques as in the proof of concept)

Read that twice: the PoC is a **jump to 0x133713371337** — a signature jump, not a shell —
and the award still lands at $18k. The lesson echoes the era's memory-safety programs
(Chrome, Flash): *demonstrated RIP control in the sandbox = remote-code-execution class*,
because the sandbox exists precisely to make that jump impossible. The reporter works the
same Shopify-sandbox lane — RCE-181321's body opens "This bug was found with `jmlb337`."

## 3. The bytecode corruption row: `break` inside `while`

RCE-183356 (high, **$10,000 (json)**) — one line of Ruby, opcode miscompilation:

> A ||= break while break

> An infinite family of programs is able to exploit this bug to crash the interpreter,
> execute spurious bytecode that wasn't generated for the current program or even set the
> machine instruction pointer to some junk value (making this a limited form of unwated
> code execution, even though the executed code isn't arbitrary).

(sic) "unwated". The body then walks the generated AST and bytecode, showing the
`OP_JMP` jumping beyond the `iseq` array ("there may be valid opcodes beyond the end"),
with each added `break` moving the jump target up — "can be increased almost without
bounds". The patch is included in the body. Class lesson: the *code generator* is part of
the attack surface; you do not need type confusion if the generated program's bytecode
itself can point the PC outside its own buffer.

## 4. The Flash quartet: watering-hole era money

Four rows, $37,500 total, all via the **ibb** (Internet Bug Bounty) program:
RCE-2106 (type confusion, APSB13-28, $10,000), RCE-2170 (double free, CVE-2014-0502,
$10,000, with the body noting active watering-hole exploitation against nonprofits and
human-rights sites), RCE-47232 (StageVideoAvailabilityEvent UAF, $10,000), RCE-47234
(MessageChannel.send UAF, $7,500). Bodies are short (APS bulletin links; the CVE/
assurance-list language carries the class). Two of them (2106, 2170) went direct-to-Adobe
and one carried the famous charity pledge in the body. This is the era when browser-
plugin memory bugs were the internet's most-sponsored code-execution lanes — the money
tracked weaponization, not the specific primitive.

## 5. The phar lane: archive parsers are deserializers with memory bugs

Six rows, $4,500: RCE-73237 (phar_set_inode stack buffer overflow, $1,000 json), RCE-73238
(phar over-read inside unserialize, $1,000 json), RCE-103990 (phar_get_fp_offset NULL
deref, $500), RCE-104008 (phar_make_dirstream uninitialized pointer, $1,000), RCE-104026
(invalid free in phar_tar_process_metadata, $500), RCE-104027 (tar entry-name memory
corruption, $500). The class note that makes this lane interesting cross-modular: phar
files carry **serialized metadata** — the same attacker-controlled byte stream module 03
studies, delivered through an *archive parser*. The crash batch here
(stack overflow / over-read / invalid free) shows the same
sanitizer-economy as the mruby lane at $500-$1,000 per entry.

## 6. The fuzzer corpus: flat rates for crash reports

Twenty-one mruby rows: the three crown rows (§2–§3) and eighteen flat-rate crash
reports — $800 × 14 entries (NULL derefs, UAFs, heap-buffer-overflow READ at 221251),
$100 × 4 entries (201903's json tier). Fifteen of the eighteen carry the crash proof in
the body (gdb or ASan register dumps); three are metadata-only (201903, 205536, 210671 —
title+bounty only). Most of those bodies are hand-written one-line Ruby PoCs — e.g.
196380's `0.instance_eval{super()}` — and 221251's ASan run credits afl-fuzz. The house
format of the ones with bodies: (1) the exact crash line number, (2) a gdb or ASan
register dump, (3) an explicit limit statement:

> It can not be exploited, but it can cause DoS

That from RCE-192485's body — and the row still shows **$800 (list)** in the register.
The flat-rate economy priced the *triage value* of crash reproducibility on a
sandbox-interpreter target. (The corpus does not show a single mruby reporter dismissed
for "just a crash" in the resolved set — that is what sandbox-oriented programs were
buying with flat tables.)

## 7. Python & Perl engine rows

RCE-182169 (Python `FutureIter_throw` type confusion, $500 json, low) — the body frames
it as "func-pointer overwrite potential" reported via the ibb-python program. RCE-207983
(Perl `S_regmatch` heap over-read, $1,000 list) — sanitizer output with the rt.perl
ticket. Pickle rows live in module 03 (they are deserialization bugs); these two are
pure engine memory safety. Both lanes pay $500-$1,000 flat: the VDP tiers for
interpreter bugs were uniform.

## 8. What pays, what doesn't

- Every Flash/phar/mruby row monetized (36/37 rows with bounty, including every DoS-grade
  crash). The unpaid row is 221287 (libsass NULL deref, unresolved-tier target).
- The **reach** sets the price within the lane: $800 flat for non-exploitable crashes →
  $10k-$20k for RIP control or codegen-corruption chains.
- Crash reports without a VM target context did NOT pay on general web programs (the
  libsass row). The lane's money required a sandbox or language VDP.
- Modern echo (P4): the flat-rate-for-crash model lives on in interpreter VDPs; the
  watering-hole Flash lane is dead, replaced in kind by Electron/Chromium renderer rows —
  bibliography (blogs-index §3), not corpus.

## 9. Cross-references

- Module 03 holds the *deserialization-format* memory bugs (pickle, phar-metadata) — the
  lane split is: bytes-format parsers = 03; interpreters/native VMs = 04.
- RCE-183356's codegen corruption pairs with module 02's engine-fingerprint paddles
  (Liquid/Smarty) — same insight: the engine is the surface.
- The ASan output format (221251, 216700) is the corpus's most-copied artifact form
  (quoting line numbers + shadow bytes) — playbook P2 borrows the format.
