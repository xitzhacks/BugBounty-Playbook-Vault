---
title: "Memory-corruption vault module — null-deref & stack crashes (59 full-body rows)"
type: playbook
category: memory-corruption
cwe: "CWE-476"
source_count: 59
full_bodies_available: "59/59"
corpus: "h1-brain disclosed_reports.db (sha256 8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4) — 352-row vault; 336-row memory-corruption bucket"
list_accessed: "2026-11-07"
note: "MEM module 5/6. Anchors: the mruby crash crown — MEM-186723/189633 ($10,000), MEM-184661/184857/185794 ($8,000), MEM-201897 ($2,000) — plus MEM-2585375 (Apache NPV DoS, $4,920), MEM-489102 (VLC SEH stack, $2,817.28), MEM-175587 (GD stack, $1,500). 31/59 rows carry bounty figures; module floor $74,487."
---

# Null-Deref & Stack Crashes

## 1. Overview

Fifty-nine rows, 31 paid, **$74,487** — the vault's second-largest money module, and it is *almost entirely the mruby sandbox crash economy* plus a tail of CVE-grade service null derefs. Two tiers exist by program, not by severity: crash reports against the Shopify sandbox (`shopify-scripts`) price at **$100–$10,000 with the interface repeated per bug**, while crash reports against public servers (Apache, nginx, VLC) price as CVEs. Doctrine: a crash report is a priced product when it names the *target context* (sandbox/VM/CVE track); against general web targets it is a $0 finding. This module is the modern echo of RCE module 04's mruby crest — same sandbox, successor reports, higher prices.

**Case-stock (59 rows / $74,487):**

| Case | Target | Mechanism | Bounty |
|---|---|---|---|
| [MEM-186723](https://hackerone.com/reports/186723) | shopify-scripts | Crash: Overwriting NoMethodError with a builtin class crashes/corrupts memory | $10,000 |
| [MEM-189633](https://hackerone.com/reports/189633) | shopify-scripts | Certain inputs cause tight C-level recursion leading to process stack overflow | $10,000 |
| [MEM-184661](https://hackerone.com/reports/184661) | shopify-scripts | mruby-time: Crash host with uninitialized Time obj | $8,000 |
| [MEM-184857](https://hackerone.com/reports/184857) | shopify-scripts | Crash: calling Proc::initialize_copy with a Proc instance where initialize never ran leads to a crash | $8,000 |
| [MEM-185794](https://hackerone.com/reports/185794) | shopify-scripts | Crash: mrb_any_to_s can't handle NilClass, Symbol and Fixnum | $8,000 |
| [MEM-2585375](https://hackerone.com/reports/2585375) | ibb | important: Apache HTTP Server: Crash resulting in Denial of Service in mod_proxy via a malicious request (CVE-2024-38477) | $4,920 |
| [MEM-489102](https://hackerone.com/reports/489102) | vlc_h1c | VLC 4.0.0 - Stack Buffer Overflow (SEH) | $2,817.28 |
| [MEM-2526041](https://hackerone.com/reports/2526041) | ibb | CVE-2024-35200 in nginx | $2,600 |
| [MEM-2526051](https://hackerone.com/reports/2526051) | ibb | CVE-2024-31079 in nginx | $2,600 |
| [MEM-201897](https://hackerone.com/reports/201897) | shopify-scripts | Recursion causing uninitialized memory reads leading to a segfault | $2,000 |
| [MEM-175587](https://hackerone.com/reports/175587) | ibb | Stack Buffer Overflow in GD dynamicGetbuf | $1,500 |
| [MEM-272497](https://hackerone.com/reports/272497) | ibb | Perl $ENV Key Stack Buffer Overflow | $1,500 |
| [MEM-185957](https://hackerone.com/reports/185957) | shopify-scripts | Crash: A call to Symbol.new leads to a crash when inspecting the resulting object | $1,000 |
| [MEM-504951](https://hackerone.com/reports/504951) | valve | Malformed playlist.txt in GoldSrc games leads to Access Violation & arbitrary code execution | $1,000 |
| [MEM-621308](https://hackerone.com/reports/621308) | shopify-scripts | NULL pointer dereference in `mrb_check_frozen` | $1,000 |
| [MEM-214681](https://hackerone.com/reports/214681) | shopify-scripts | Null pointer dereference in ary_concat | $800 |
| [MEM-215891](https://hackerone.com/reports/215891) | shopify-scripts | Null pointer dereference in mrb_class | $800 |
| [MEM-217610](https://hackerone.com/reports/217610) | shopify-scripts | kh_put_iv SEGFAULT - mruby 1.2.0 | $800 |
| [MEM-218233](https://hackerone.com/reports/218233) | shopify-scripts | Null pointer dereference in OP_ENTER | $800 |
| [MEM-218567](https://hackerone.com/reports/218567) | shopify-scripts | SIGSEGV in array_copy - array.c:71 | $800 |
| [MEM-242354](https://hackerone.com/reports/242354) | shopify-scripts | Null pointer dereference with send/method_missing | $800 |
| [MEM-420115](https://hackerone.com/reports/420115) | shopify-scripts | Crash in mrb_ary_push | $800 |
| [MEM-135294](https://hackerone.com/reports/135294) | ibb | xml_parse_into_struct segmentation fault | $500 |
| [MEM-161198](https://hackerone.com/reports/161198) | ibb | wddx_deserialize null dereference with invalid xml | $500 |
| [MEM-161216](https://hackerone.com/reports/161216) | ibb | wddx_deserialize null dereference | $500 |
| [MEM-161217](https://hackerone.com/reports/161217) | ibb | wddx_deserialize null dereference in php_wddx_pop_element | $500 |
| [MEM-175316](https://hackerone.com/reports/175316) | ibb | stack-buffer-overflow through "ResourceBundle" methods | $500 |
| [MEM-305973](https://hackerone.com/reports/305973) | ibb | Inappropriately parsing HTTP response leads to PHP segment fault! | $500 |
| [MEM-1032086](https://hackerone.com/reports/1032086) | kubernetes | csi-snapshot-controller crashes when processing VolumeSnapshot with non-existing PVC | $500 |
| [MEM-505173](https://hackerone.com/reports/505173) | valve | Malformed map detailed texture files in GoldSrc games lead to Remote Code Execution | $350 |
| [MEM-2958097](https://hackerone.com/reports/2958097) | brave | Null Pointer Dereference by Crafted Response from AI Model | $100 |
| [MEM-113120](https://hackerone.com/reports/113120) | ibb | An integer overflow bug in php_implode() could lead heap overflow, make PHP to crash | - |
| [MEM-152232](https://hackerone.com/reports/152232) | ibb | NULL Pointer Dereference in exif_process_user_comment | - |
| [MEM-159690](https://hackerone.com/reports/159690) | ibb | stack buffer overflows in the curses module | - |
| [MEM-176226](https://hackerone.com/reports/176226) | ibb | CachingIterator null dereference when convert to string | - |
| [MEM-180908](https://hackerone.com/reports/180908) | ibb | NULL Pointer Dereference in WDDX Packet Deserialization with PDORow | - |
| [MEM-182140](https://hackerone.com/reports/182140) | ibb | libtiff 4.0.6 segfault / read outside of buffer (CVE-2016-9297) | - |
| [MEM-183239](https://hackerone.com/reports/183239) | shopify-scripts | SIGSEGV on mruby's mark_tbl() (Invalid memory access) | - |
| [MEM-191994](https://hackerone.com/reports/191994) | shopify-scripts | SIGSEGV mrb_obj_freeze() Manipulating Register RAX and RSI | - |
| [MEM-192578](https://hackerone.com/reports/192578) | shopify-scripts | kh_get_n2s() stack overrun | - |
| [MEM-195688](https://hackerone.com/reports/195688) | ibb | NULL Pointer Dereference while unserialize php object | - |
| [MEM-196380](https://hackerone.com/reports/196380) | shopify-scripts | SIGSEGV in mrb_vm_exec | - |
| [MEM-196498](https://hackerone.com/reports/196498) | shopify-scripts | Segmentation fault on program counter | - |
| [MEM-209937](https://hackerone.com/reports/209937) | shopify-scripts | SIGSEGV - mark_context_stack | - |
| [MEM-213255](https://hackerone.com/reports/213255) | shopify-scripts | SIGSEGV in str_buf_cat | - |
| [MEM-214845](https://hackerone.com/reports/214845) | shopify-scripts | SIGSEGV in mrb_vm_exec | - |
| [MEM-215447](https://hackerone.com/reports/215447) | shopify-scripts | SIGSEGV in mrb_class | - |
| [MEM-217083](https://hackerone.com/reports/217083) | shopify-scripts | SIGSEGV in mrb_str_inum | - |
| [MEM-217097](https://hackerone.com/reports/217097) | shopify-scripts | SIGSEGV in mrb_vm_exec | - |
| [MEM-219870](https://hackerone.com/reports/219870) | shopify-scripts | mirb only: stack-buffer-overflow (OOB write) in main() | - |
| [MEM-296198](https://hackerone.com/reports/296198) | shopify-scripts | SEGV on ary_concat | - |
| [MEM-480883](https://hackerone.com/reports/480883) | notepad-plus-plus | Stack overflow in XML Parsing | - |
| [MEM-480984](https://hackerone.com/reports/480984) | notepad-plus-plus | Stack overflow affecting "ext" field on stylers.xml configuration file | - |
| [MEM-495793](https://hackerone.com/reports/495793) | valve | Malformed .MDL triggers an Access Violation on GoldSRC (hl.exe) | - |
| [MEM-497255](https://hackerone.com/reports/497255) | notepad-plus-plus | A stack buffer overflow in BabyGrid.cpp can lead to program crashes via a malicious localization file | - |
| [MEM-798744](https://hackerone.com/reports/798744) | ibb | Null Pointer Dereference in PHP Session Upload Progress | - |
| [MEM-838127](https://hackerone.com/reports/838127) | ibb | mb_strtolower (UTF-32LE): stack-buffer-overflow at php_unicode_tolower_full (CVE-2020-7065) | - |
| [MEM-1753224](https://hackerone.com/reports/1753224) | ibb | CVE-2022-35260: .netrc parser out-of-bounds access | - |
| [MEM-2070810](https://hackerone.com/reports/2070810) | ibb | Potential NULL dereference in libssh's sftp server | - |

## 2. The mruby crown: $10,000 for two crash PoCs

The vault mirrors RCE module 04's sandbox economics at higher stakes: two one-line PoCs, $10,000 each, both *crash-only* claims priced as "corrupts memory." MEM-186723:

> Uhm, while testing this I seem to have broken `https://mruby.science`.. Ooops, sorry about that!

> Overwriting (at least, not sure about other triggers) `NoMethodError` with a builtin class like `Fixnum` or `Integer` leads to a rather interesting behavior.

> The root cause is that triggering the `NoMethodError` triggers another `NoMethodError` when `mrb_no_method_error in error.c` tries to call `new` on the new `NoMethodError`, which has no new.

The report form is the sandbox dialect: break the shared testing site, name the root cause, attach the fix delta, paste the `[BUG] Segmentation fault` trace. MEM-189633 (the other **$10,000**) is the recursion that bypasses the Ruby stack guard:

> Certain legal Ruby programs can cause a tight recursion on the C-level (without using `eval`) while spending very little of the Ruby-level stack. This precludes triggering a Ruby stack overflow exception and eventually leads to a process stack overflow and a segfault.

That sentence is the module's methodological core — *tight C-level recursion evades the language-level guardrail*. Both crown rows reached the text "crashes/corrupts memory" in their titles and were priced as safety-critical sandbox breaches, not DoS.

## 3. The $8,000 tier: initialize-never-ran (x2) and boxing introspection

Three rows at $8,000. MEM-184661:

> `Time::initialize_copy` performs its copy action even on `Time` objects on which `initialize` never ran, leading to a crash.

> The PoC crashes https://www.mruby.science/runs - didn't try Shopify production servers for the usual reasons.

MEM-184857 repeats the trick for `Proc::initialize_copy`, with the honest reach line quotable as pricing doctrine:

> I didn't look too close but as it's accessing a 0+OFFSET this might be usable to gain code execution. Otherwise it's just a DoS, further investigation is needed.

MEM-185794 (boxing-word introspection) prices a crash that only fires under one boxing scheme — scope honesty as paid content:

> When using `boxing_word.h` (haven't tested other boxing methods yet), `mrb_any_to_s` is unable to handle `NilClass`, `Symbol` and `Fixnum`.

Read across the tier: the sandbox paid *demonstrated* memory-safety impact per site, with escalation ($8,000) for object-lifecycle confusion and top rate ($10,000) for process-global corruption (error-class massacre, C-stack exhaustion).

## 4. The server tier: Apache, nginx, VLC, GD

Outside the sandbox the same crash earns a CVE and its price is public-program money. MEM-2585375 (**$4,920**) is the genre exemplar — security-email disclosure, CVE, upgrade line:

> null pointer dereference in mod_proxy in Apache HTTP Server 2.4.59 and earlier allows an attacker to crash the server via a malicious request.

> Users are recommended to upgrade to version 2.4.60, which fixes this issue.

MEM-489102 (**$2,817.28**, VLC SEH) is the "stack overflow with SEH overwrite" row whose summary front-loads the deliverable:

> Incorrect calculation of Buffer Size in rist module for VLC leading to Stack Overflow with SEH chain overwrite.

MEM-2526041/2526051 (nginx QUIC/HTTP3, **$2,600** each) state termination only. MEM-175587 (**$1,500**, GD `dynamicGetbuf`) adds the "real life examples" list of callers who pass user input — the reach argument for a stack overflow in an image function.

## 5. The unpaid tail (28 rows): same sounds, no economy

Twenty-eight rows carry no figure: mb_strtolower / curses / Notepad++ / valve MDL towers, and a shopify-scripts SIGSEGV run at `mrb_vm_exec` (196380, 214845, 217097), `mrb_class` (215447), `mrb_str_inum` (217083), `mark_context_stack` (209937). Two readings coexist, both worth stating: (a) the sandbox's bounty table only paid *some* crash reports (the table's filters are not in this corpus — paid membership is the only evidence), and (b) unpaid crashes on production-adjacent software (vLC, Notepads, AWS-adjacent controllers) still earn CVEs without money. The module's own pair proves the filter is program-side, not severity-side: MEM-184715's vm UAF ($1,000, found via ASan with the production-scope caveat) vs MEM-196380's vm SIGSEGV (`-`). Identical frame, different verdict.

## 6. What pays / what doesn't

- **Pays**: sandbox crashes with lifecycle/corruption flavor ($8,000–$10,000); recursion-evades-guard ($10,000); service CVE crashes ($1,500–$4,920, nginx/Apache/GD/VLC); stack overflows framed by attacker control ($1,500); sandbox NULL derefs at the sandbox rate ($800–$1,000).
- **Doesn't pay (in this corpus)**: the shopify SIGSEGV tail; MEM-2958097 (Brave AI-model NPV, $100 — the corpus's cheapest paid crash and its best token of the modern economy); MEM-505173's valve detail-file RCE ($350 — a priced remote-code-execution row below the integer module's floor, because the file had to be *requested* by a client via precache — arrival conditions noted in body). Pattern: arrival conditions (must be precached, must be processed by an admin's tool, must be viewer-driven) discount the payout, not the primitive.
- **MEM-113120** (integer-overflow bug classed here, `-`) is the classifier's borderline: title says overflow, body says heap overflow via `php_implode`. It stays frozen here; report-form users should sweep both modules for string-function length bugs.

## 7. Cross-references

- **RCE vault module 04 §6** — the fuzzer flat-rate economy ($100–$800) is the ancestor table; this module's $8,000–$10,000 crown shows the table's escalation for process-global corruption in detail.
- **Adjacent pool** — MEM-181319/192896 (mruby memory *disclosures*) complete the sandbox's hunting matrix: crash (§2), UAF (module 02), leak (adjacent). One sandbox, three modules.
- **DoS vault** (upcoming master row 21) — the server-tier rows (§4) are its mirror; the Apache close-framing is the CVE-track report form.
- **Race vault** — `kh_get_n2s() stack overrun` (192578) and the vm_exec SIGSEGV run are concurrency-adjacent crashes; the Race vault's synchronization module supplies the tooling; pricing doctrine stays in this module.
