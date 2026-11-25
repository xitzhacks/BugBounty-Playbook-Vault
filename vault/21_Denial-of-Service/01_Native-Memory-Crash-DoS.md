---
title: "Native memory crash DoS — sandboxed-interpreter segfaults, NULL derefs, and the mruby $10,000 crash cluster"
type: playbook
category: native-memory-crash-dos
cwe: "CWE-400 (with CWE-476/787/416 siblings)"
source_count: 75
full_bodies_available: 75
corpus: "h1-brain disclosed_reports.db (3,673 rows; sha256 8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4) · bucket 'dos' = 221 rows, weakness 'Uncontrolled Resource Consumption'"
list_accessed: "2026-11-07"
note: "Anchor bodies: DOS-181685/181828/181910/182484/183356/187305/187536/188326 ($10,000 mruby cluster), DOS-181232/184712 ($8,000). All 75 bodies read; quotes byte-true to references/archive/DOS-bodies-full-dump.txt."
---

# Native memory crash DoS — the sandboxed interpreter that segfaults on demand

## 1. Overview

Seventy-five rows, **$149,500/38 paid** — 54% of the vault's money in this module, and the
single richest class in the build. The money is one product line: the **Shopify Scripts
sandbox** (`mruby-engine` wrapping mruby) was ground down crash-by-crash in 2015–2016, and
the program paid flat tiers for what should never have been reachable from sandboxed code —
eight flagship breaks at **$10,000**, seven more at **$8,000**, then $1,000 / $800 / $500 /
$300 / $100 run-offs. Around that core sit the non-mruby native rows that prove the class
is broader than one sandbox: Rails' nested-hash `SystemStackError` (42797), PHP-FPM's
`snprintf` length accounting (112723), Tor's pre-auth control loop (113424), a PHP UAF via
assign-by-ref (123119), libgd image crashes (146936/146944/190863/305972), libtiff
(181642/195580), Nextcloud's `OCUtil.dll` leak (588562) and PuTTY's `len == 1` abort
(495508). The doctrine this module teaches: a memory-safety bug in *any* interpreter, parser
or daemon reachable from untrusted input is a paid DoS on its own — and in a sandbox the
*crash itself* is the finding, because the sandbox exists precisely so one tenant cannot
kill the shared process.

**Case-stock (75 rows / $149,500):**

| Case | Target | Mechanism | Bounty |
|---|---|---|---|
| [DOS-181685](https://hackerone.com/reports/181685) | shopify-scripts | remove Range#initialize_copy → uninitialized object → NULL deref | $10,000 |
| [DOS-181828](https://hackerone.com/reports/181828) | shopify-scripts | non-closure lambda env → NULL deref, kills parent MRI | $10,000 |
| [DOS-181910](https://hackerone.com/reports/181910) | shopify-scripts | Range=Array → RRange edges confused → type-confusion crash | $10,000 |
| [DOS-182484](https://hackerone.com/reports/182484) | shopify-scripts | CALL_MAXARGS=127 boundary → invalid pointer deref | $10,000 |
| [DOS-183356](https://hackerone.com/reports/183356) | shopify-scripts | A-or-equals break-while-break → bytecode corruption | $10,000 |
| [DOS-187305](https://hackerone.com/reports/187305) | shopify-scripts | zero-length heredoc id → parser infinite loop, SIGTERM-proof | $10,000 |
| [DOS-187536](https://hackerone.com/reports/187536) | shopify-scripts | codegen NODE_NEGATE unused value → NULL deref | $10,000 |
| [DOS-188326](https://hackerone.com/reports/188326) | shopify-scripts | mrb_time_asctime buffer overflow (intermittent, ASAN-reliable) | $10,000 |
| [DOS-180695](https://hackerone.com/reports/180695) | shopify-scripts | 49,000× 'A' crashes mruby.science service | $8,000 |
| [DOS-181232](https://hackerone.com/reports/181232) | shopify-scripts | splat+redo case → NULL deref crash | $8,000 |
| [DOS-181695](https://hackerone.com/reports/181695) | shopify-scripts | undefined method_missing → NULL deref | $8,000 |
| [DOS-183405](https://hackerone.com/reports/183405) | shopify-scripts | Null target_class crash | $8,000 |
| [DOS-183425](https://hackerone.com/reports/183425) | shopify-scripts | C-invoked Ruby method via Object#send → segfault | $8,000 |
| [DOS-184712](https://hackerone.com/reports/184712) | shopify-scripts | invalid memory access in mrb_ary_concat | $8,000 |
| [DOS-188313](https://hackerone.com/reports/188313) | shopify-scripts | bad memory access in kh_get_mt (hash table) | $8,000 |
| [DOS-185387](https://hackerone.com/reports/185387) | shopify-scripts | parse.y regression → NULL deref (fuzz-found) | $1,000 |
| [DOS-185899](https://hackerone.com/reports/185899) | shopify-scripts | array_copy upper-bound error → invalid memory write | $1,000 |
| [DOS-190133](https://hackerone.com/reports/190133) | shopify-scripts | invalid values to values_at → segfault | $1,000 |
| [DOS-191689](https://hackerone.com/reports/191689) | shopify-scripts | NODE_NEGATE codegen error | $1,000 |
| [DOS-204047](https://hackerone.com/reports/204047) | shopify-scripts | segfault printing backtrace | $1,000 |
| [DOS-193081](https://hackerone.com/reports/193081) | shopify-scripts | NULL pointer deref in mrb_str_prepend | $800 |
| [DOS-197719](https://hackerone.com/reports/197719) | shopify-scripts | heap overflow in mrb_ary_splice | $800 |
| [DOS-208526](https://hackerone.com/reports/208526) | shopify-scripts | NULL deref in mark_context_stack | $800 |
| [DOS-209449](https://hackerone.com/reports/209449) | shopify-scripts | heap buffer overflow, long array assignment | $800 |
| [DOS-212107](https://hackerone.com/reports/212107) | shopify-scripts | NULL deref in mrb_class | $800 |
| [DOS-213261](https://hackerone.com/reports/213261) | shopify-scripts | UAF → invalid pointer deref | $800 |
| [DOS-218570](https://hackerone.com/reports/218570) | shopify-scripts | invalid pointer deref in OP_ENTER | $800 |
| [DOS-146936](https://hackerone.com/reports/146936) | ibb | imagefilltoborder stack overflow (CVE-2015-8874) | $500 |
| [DOS-146944](https://hackerone.com/reports/146944) | ibb | NULL deref at _gdScaleVert (libgd) | $500 |
| [DOS-190863](https://hackerone.com/reports/190863) | ibb | imagefilltoborder stack overflow, truecolor | $500 |
| [DOS-305972](https://hackerone.com/reports/305972) | ibb | infinite loop in gdImageCreateFromGifCtx | $500 |
| [DOS-215854](https://hackerone.com/reports/215854) | shopify-scripts | garbage collector crash | $300 |
| [DOS-191328](https://hackerone.com/reports/191328) | shopify-scripts | invalid memory access in mrb_str_format | $100 |
| [DOS-197916](https://hackerone.com/reports/197916) | shopify-scripts | crash in print_backtrace | $100 |
| [DOS-200387](https://hackerone.com/reports/200387) | shopify-scripts | redo inside NODE_RESCUE codegen crash | $100 |
| [DOS-202362](https://hackerone.com/reports/202362) | shopify-scripts | NULL deref in mrb_random_initialize | $100 |
| [DOS-205884](https://hackerone.com/reports/205884) | shopify-scripts | integer overflow in str_substr → OOB read/write | $100 |
| [DOS-588562](https://hackerone.com/reports/588562) | nextcloud | OCUtil.dll memory leak → DoS in desktop client | $100 |
| [DOS-42797](https://hackerone.com/reports/42797) | rails | deeply nested params hash → SystemStackError in Action Pack | - |
| [DOS-112723](https://hackerone.com/reports/112723) | ibb | PHP-FPM access-log snprintf length accounting → leak/overflow | - |
| [DOS-113424](https://hackerone.com/reports/113424) | torproject | tor pre-auth control loop spins → infinite CPU | - |
| [DOS-123119](https://hackerone.com/reports/123119) | ibb | assign-by-ref to overloaded objects → UAF crash | - |
| [DOS-180977](https://hackerone.com/reports/180977) | shopify-scripts | malformed exception → SIGABRT | - |
| [DOS-181642](https://hackerone.com/reports/181642) | ibb | libtiff heap overflow / OOB read (CVE-2016-9273) | - |
| [DOS-181677](https://hackerone.com/reports/181677) | shopify-scripts | NULL deref parsing ternary operators | - |
| [DOS-181871](https://hackerone.com/reports/181871) | shopify-scripts | type confusion in mrb_no_method_error | - |
| [DOS-181874](https://hackerone.com/reports/181874) | shopify-scripts | invalid remove_method arg → SIGSEGV | - |
| [DOS-182027](https://hackerone.com/reports/182027) | shopify-scripts | SIGSEGV on mrb_ary_splice | - |
| [DOS-182274](https://hackerone.com/reports/182274) | shopify-scripts | TOCTOU in mrb_time_initialize → NULL deref | - |
| [DOS-183231](https://hackerone.com/reports/183231) | shopify-scripts | mrb_str_modify invalid memory access | - |
| [DOS-185041](https://hackerone.com/reports/185041) | shopify-scripts | type confusion in mrb_exc_set → memory corruption | - |
| [DOS-191938](https://hackerone.com/reports/191938) | shopify-scripts | SIGSEGV on mrb_get_args | - |
| [DOS-192485](https://hackerone.com/reports/192485) | shopify-scripts | SIGSEGV on mrb_vm_exec (NULL deref) | - |
| [DOS-192532](https://hackerone.com/reports/192532) | shopify-scripts | SIGABRT/SIGSEGV in mspace_free/mrb_default_allocf | - |
| [DOS-192734](https://hackerone.com/reports/192734) | shopify-scripts | SIGSEGV NULL pointer mrb_str_concat | - |
| [DOS-193075](https://hackerone.com/reports/193075) | shopify-scripts | SIGSEGV mrb_check_intern_str NULL pointer | - |
| [DOS-193077](https://hackerone.com/reports/193077) | shopify-scripts | mrb_str_modify writes to read-only memory | - |
| [DOS-193724](https://hackerone.com/reports/193724) | shopify-scripts | SIGSEGV kh_resize_iv NULL deref | - |
| [DOS-195580](https://hackerone.com/reports/195580) | ibb | hostile TIFF parse → crash | - |
| [DOS-195842](https://hackerone.com/reports/195842) | shopify-scripts | segfault in mrb_gc_mark | - |
| [DOS-196386](https://hackerone.com/reports/196386) | shopify-scripts | SIGSEGV mrb_vm_exec vm.c:1272 | - |
| [DOS-197693](https://hackerone.com/reports/197693) | shopify-scripts | SIGSEGV mrb_vm_exec line:1681 | - |
| [DOS-197694](https://hackerone.com/reports/197694) | shopify-scripts | SIGSEGV mrb_obj_extend line:413 | - |
| [DOS-197723](https://hackerone.com/reports/197723) | shopify-scripts | NULL deref in mrb_str_modify | - |
| [DOS-199764](https://hackerone.com/reports/199764) | shopify-scripts | abort in proc.c:143 | - |
| [DOS-201905](https://hackerone.com/reports/201905) | shopify-scripts | SIGSEGV vm.c:1214 | - |
| [DOS-202582](https://hackerone.com/reports/202582) | shopify-scripts | NULL deref in mrb_obj_instance_eval | - |
| [DOS-202584](https://hackerone.com/reports/202584) | shopify-scripts | NULL deref in mrb_vm_exec | - |
| [DOS-203513](https://hackerone.com/reports/203513) | shopify-scripts | SIGSEGV mrb_vm_exec line:1312 | - |
| [DOS-204628](https://hackerone.com/reports/204628) | shopify-scripts | segfault in sprintf/mrb_str_format | - |
| [DOS-210429](https://hackerone.com/reports/210429) | shopify-scripts | NULL ptr deref mrb_vm_exec | - |
| [DOS-212456](https://hackerone.com/reports/212456) | shopify-scripts | SIGSEGV kh_get_n2s in symbol.c:37 | - |
| [DOS-213779](https://hackerone.com/reports/213779) | shopify-scripts | SIGSEGV mrb_obj_value | - |
| [DOS-297383](https://hackerone.com/reports/297383) | shopify-scripts | mruby heredoc notation crash | - |
| [DOS-495508](https://hackerone.com/reports/495508) | putty_h1c | assert len==1 aborts on remote-output streaming | - |
## 2. The $10,000 cluster: one-liner Ruby that kills the parent MRI

The eight $10,000 rows are the vault's crown evidence. Each is a two-to-five-line Ruby
program, run inside the sandbox, that segfaults `mruby-engine` and therefore the parent MRI
Ruby process — the blast radius is the whole Scripts runner, not one script.

DOS-181685 pairs a core-library excision with an ordinary method call:

> Removing `Range#initialize_copy` makes it possible to construct an uninitialized `Range` object. Calling (pretty much) any instance method on the uninitialized `Range` object afterwards causes mruby to dereference a null pointer, leading to a segfault.

DOS-181828 shows the mechanism the sandbox was supposed to contain — a *valid* program whose
non-closure lambda leaves `env` null at `vm.c:1266`:

> Certain valid Ruby programs are able to cause a segmentation fault in mruby through a null pointer derefence, which in turn leads to a crash in mruby_engine and the parent MRI Ruby process.

Note the author's typo, kept as-is: "derefence", not "dereference" — the quote rule is
byte-true with (sic) discipline, and the dump carries the original spelling.

DOS-181910 is the type-confusion exemplar, and the rare $10,000 row where the reporter
scopes the escalation *down* honestly:

> It's possible to crash mruby by redefining the `Range` class and then using the range literal syntax:

> It may be possible to achieve RCE through this vulnerability, but there are significant complicating factors and I have not spent the time trying to develop an RCE PoC.

DOS-182484 pins the trigger to a single integer boundary:

> Improper logic for handling of maximum number of method call arguments leads to dereferencing an invalid pointer in some cases, which causes a segfault in both mruby and mruby_engine (and the parent MRI).

> The crash only happens when the number of arguments, `n == CALL_MAXARGS`, which is 127. If a larger number of arguments are supplied, mruby doesn't crash but it doesn't appear to work as intended either. The intent of the design seems to had been to support a larger number of arguments than CALL_MAXARGS, but that they should then be passed as an array. However, calls with more than CALL_MAXARGS don't succeed, raising an ArgumentError instead.

DOS-183356 is the corpus's most dangerous crash by the reporter's own account — the
`||=`/loop/`break` family corrupts generated bytecode, so execution runs *spurious*
bytecode, not just a null pointer:

> Certain invalid inputs (invalid Ruby programs) crash mruby and mruby_engine (including the parent MRI VM). The programs always involve the `||=` operator, loops and the `break` keyword.

DOS-187305 is the only $10,000 row that is a *hang*, not a crash — and the hang is worse,
because it survives `SIGTERM`:

> Certain invalid Ruby programs (which should normally raise a syntax error) are able to cause an infinite loop in MRuby's parser which makes the mruby-engine sandbox (and consequently the MRI process it is running in) unresponsive to SIGTERM. The process begins looping forever and has to be terminated using SIGABRT or SIGKILL. The bug is caused by an improper handling of heredocs with a zero-length identifier.

DOS-187536 and DOS-188326 round out the cluster with codegen and overflow flavors. The
first is a `NODE_NEGATE` codegen bug reached via a dead `case` branch; the second is an
intermittent `mrb_time_asctime` overflow that only crashes reliably under ASAN — yet still
cleared the top tier, which tells you the program priced the *primitive*, not the crash
rate:

> This one doesn't always crash every time, but with ASAN on it will.

## 3. The $8,000 tier and the $800 flat rate: fuzzing as a paid product line

The $8,000 rows (181232, 184712, 181695, 183405, 183425, 188313, 180695) are the same
sandbox, one tier down — minimized one-liners, each with the crash minimized to the bare
bones. DOS-181232 and DOS-184712 are near-twins (both splat/`case` codegen bugs in
`ary_modify`/`mrb_ary_concat`), quoted to show the report *genre* — every body carries a
minimal file, a version stamp, and an lldb `EXC_BAD_ACCESS` trace:

> The following file causes a segmentation fault in mruby, which also causes a segmentation fault in mruby-engine. I've minimized this file down to the bare bones what crashes it, and renamed variables so you can see what is needed and what isn't.

Below that sits the long tail of deliberately un-glamorous crash reports: $800 for a NULL
deref in `mrb_str_prepend`, `$800` for a heap overflow in `mrb_ary_splice`, `$100` for a
backtrace crash — and **37 rows with no bounty figure at all** (the `None` block in the
case-stock table), which are the same mechanics without a published figure. The era lesson
is flat-rate memory-safety bounties: the program treated each *distinct* crash primitive as
a SKU. DOS-185387 states the method openly — fuzz, bisect, minimize:

> Just pulled the latest mruby code, and found that some of my fuzzing test cases now crash. Bisected it to commit `227daa881137d5251e03eea0883b9b574a1f064e`. Reverting this change no longer causes a crash.

DOS-180695 is the opposite extreme and still paid $8,000: no code, no trace, just a live
service test:

> When I sent 49000x "A" I was probably able to crash service running on https://www.mruby.science since new code can't be executed for now. Could you please verify what happened? Thanks.

**Non-mruby native rows.** DOS-42797 (Rails) is the web-facing crash in this module — a
deeply nested params hash recursion that re-triggers inside the exception handler:

> Attackers can cause an application to be unreachable, causing a denial of service condition.

DOS-112723 (PHP-FPM) is `snprintf` return-value accounting: the length variable grows past
the buffer, so the log write over-runs:

> The FastCGI Process Manager (FPM) SAPI of PHP was vulnerable to memory leak and buffer overflow in the access logging feature.

DOS-113424 (Tor) is pre-auth: no credentials needed to reach the spinning control-connection
loop.

## 4. What the patches have in common (fix shapes)

Reading the 75 bodies as a patch reviewer, the fixes recur in four shapes: (1) **drop the
runtime constant lookup** — DOS-181910's patch adds a `range_class` field to `mrb_state`
"following the pattern other core classes use"; (2) **guard the codegen transform** —
DOS-181828's peephole optimization is "not a valid transformation in certain contexts", and
DOS-191689/200387 repeat the unused-value pattern; (3) **bounds-check the length
arithmetic** — DOS-112723's `len += len2` and DOS-185899's `array_copy` upper bound; (4)
**cap the recursion** — DOS-42797's `normalize_encode_params`. The hunting translation:
when you find a crash, your report should name which of the four shapes the fix takes, and
quote the reporter's own minimal file — that is the format the era's triagers rewarded.

## 5. The honest ceiling: crash ≠ code execution

DOS-183356's reporter says the bug can "execute spurious bytecode that wasn't generated for
the current program or even set the machine instruction pointer to some junk value", then
immediately limits the claim: "making this a limited form of unwanted code execution, even
though the executed code isn't arbitrary". DOS-181910 does the same RCE scoping-down. The
module's pricing confirms it: these rows paid as DoS (top tier $10,000) *because* the
sandbox's threat model makes the crash alone a full finding — but nobody in this module
got the RCE vault's sandbox-RIP prices ($18,000–$20,000). File the crash as DoS, say the
RCE sentence explicitly with its limits, and let triage upgrade it. The reverse — filing
crash-only as RCE — is the noise-floor pattern the RCE vault's module 08 exists to record.

## 6. What pays, what doesn't

- **Sandbox escapes that crash the parent pay top tier.** All eight $10,000s are
  `sandbox_eval`-reachable one-liners. The multiplier is the blast radius: mruby → engine
  → parent MRI. Lesson: in a multi-tenant interpreter, prove the parent dies, not just
  the child.
- **Minimization quality is priced.** The $10,000 bodies carry version stamps, commits,
  minimal files and lldb traces; the $100 bodies are one-line crash logs. Same bug class,
  100× price spread — the report *is* the product.
- **No-figure rows are not failures.** 37 of 75 rows carry `bounty None` — a DB artifact,
  not a signal. The $800s prove the class paid even when the figure is missing upstream.
- **What doesn't pay in this module's logic:** a crash that only affects your own local
  binary, with no service, no sandbox, no parent process. Every paid row names the *shared*
  victim (sandbox, daemon, desktop client, Webrick/Thin production server).

## 7. Cross-references

- `RCE/` module 04 covers the same mruby corpus from the code-execution side (RCE-181879,
  RCE-181321, RCE-183356-as-RCE). This module's DOS-183356 is the *same report* filed
  under CWE-400; the two vaults cite it from opposite threat models. DOS-181910's RCE
  caveat is quoted here from the DOS side.
- DOS-42797's nested-hash recursion is the native-flavor sibling of module 04's
  unbounded-input rows (multipart parts, markdown payloads) — same "no depth cap" root,
  different layer.
- DOS-113424's pre-auth loop pairs with module 03's connection-holding floods: one spins
  CPU, the other holds sockets. Both are "no time bound" bugs; the fix shapes (loop cap vs
  timeout) differ.
