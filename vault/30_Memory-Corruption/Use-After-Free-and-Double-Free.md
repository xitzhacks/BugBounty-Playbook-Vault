---
title: "Memory-corruption vault module — use-after-free & double-free (50 full-body + 3 link-only rows)"
type: playbook
category: memory-corruption
cwe: "CWE-416"
source_count: 53
full_bodies_available: "50/53"
corpus: "h1-brain disclosed_reports.db (sha256 8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4) — 352-row vault; 336-row memory-corruption bucket"
list_accessed: "2026-11-07"
note: "MEM module 2/6. Anchors: MEM-826026 (PlayStation kernel UAF → arbitrary R/W, $10,000 — vault max), the Flash UAF fleet ($2,000 × 4 + $5,000 × 2), MEM-1977252 (Brave wallet UAF, $3,000), mruby vm UAFs ($100–$1,000). 23/53 rows carry bounty figures; module floor $41,300."
---

# Use-After-Free & Double-Free

## 1. Overview

Fifty-three rows carrying 23 figures (**$41,300**). The module's shape is inverted versus module 01: the money concentrates in a single kernel row while the bulk is interpreter UAFs (PHP `unserialize()` fleet, mruby `mrb_vm_exec`) and the Flash UAF fleet. Doctrine: a UAF report must name *what the freed object is reused as* — kernel rows price by primitive (arbitrary read/write), Flash rows by flat class rate, and PHP unserialize rows by the upstream-bugs.php.net ticket economy.

**Case-stock (53 rows / $41,300):**

| Case | Target | Mechanism | Bounty |
|---|---|---|---|
| [MEM-826026](https://hackerone.com/reports/826026) | playstation | Use-After-Free In IPV6_2292PKTOPTIONS leading To Arbitrary Kernel R/W Primitives | $10,000 |
| [MEM-56385](https://hackerone.com/reports/56385) | ibb | Double free vulnerability in Flash Player Settings Manager (CVE-2015-0346) | $5,000 |
| [MEM-151043](https://hackerone.com/reports/151043) | ibb | Adobe Flash Player PSDK Class Use After Free Vulnerability | $5,000 |
| [MEM-1977252](https://hackerone.com/reports/1977252) | brave | UAF on JSEthereumProvider | $3,000 |
| [MEM-119653](https://hackerone.com/reports/119653) | ibb | Adobe Flash Player ASnative(900,1).call(MovieClip) Use-After-Free Vulnerability | $2,000 |
| [MEM-119655](https://hackerone.com/reports/119655) | ibb | Adobe Flash Player ASnative(900,1).call(TextField) Use-After-Free Vulnerability | $2,000 |
| [MEM-122254](https://hackerone.com/reports/122254) | ibb | Adobe Flash Player TextField Use-After-Free Vulnerability | $2,000 |
| [MEM-1180380](https://hackerone.com/reports/1180380) | curl | CVE-2021-22901: TLS session caching disaster | $2,000 |
| [MEM-172562](https://hackerone.com/reports/172562) | ibb | LZMADecompressor.decompress Use After Free | $1,500 |
| [MEM-477896](https://hackerone.com/reports/477896) | ibb | Use after free and out of bounds read in xmlrpc_decode() | $1,500 |
| [MEM-478367](https://hackerone.com/reports/478367) | ibb | efree() on uninitialized Heap data in imagescale leads to use-after-free | $1,500 |
| [MEM-184715](https://hackerone.com/reports/184715) | shopify-scripts | Read after free in mrb_vm_exec with OP_ARYCAT reading R(B) | $1,000 |
| [MEM-193143](https://hackerone.com/reports/193143) | shopify-scripts | Use After Free in str_replace | $800 |
| [MEM-222294](https://hackerone.com/reports/222294) | shopify-scripts | heap-use-after-free in mrb_vm_exec - vm.c:1247 | $800 |
| [MEM-244904](https://hackerone.com/reports/244904) | shopify-scripts | Use after free in mruby-mpdecimal | $800 |
| [MEM-170144](https://hackerone.com/reports/170144) | ibb | wddx_deserialize use-after-free | $500 |
| [MEM-203002](https://hackerone.com/reports/203002) | ibb | Incorrect GC behavior in xxlimited could lead to use-after-free | $500 |
| [MEM-216151](https://hackerone.com/reports/216151) | ibb | Use-after-free in _asyncio_Future_remove_done_callback | $500 |
| [MEM-126797](https://hackerone.com/reports/126797) | torproject | Use-after-free during XML transformations (MFSA-2016-27) | $300 |
| [MEM-193719](https://hackerone.com/reports/193719) | shopify-scripts | Double free of filename after codegen error | $200 |
| [MEM-194884](https://hackerone.com/reports/194884) | shopify-scripts | Heap use-after-free during range creation | $200 |
| [MEM-200821](https://hackerone.com/reports/200821) | shopify-scripts | heap-use-after-free /home/operac/testafl/mruby/mrubylast/mruby/src/gc.c | $100 |
| [MEM-269568](https://hackerone.com/reports/269568) | ibb | Optionsbleed / CVE-2017-9798 | $100 |
| [MEM-18843](https://hackerone.com/reports/18843) | ibb | use-after-free vulnerability in Flash Player | - |
| [MEM-37240](https://hackerone.com/reports/37240) | ibb | Race condition in Flash workers may cause an exploitabl​e double free | - |
| [MEM-146200](https://hackerone.com/reports/146200) | ibb | _php_mb_regex_ereg_replace_exec - double free | - |
| [MEM-152266](https://hackerone.com/reports/152266) | ibb | Use After Free Vulnerability in SNMP with GC and unserialize() | - |
| [MEM-152281](https://hackerone.com/reports/152281) | ibb | Use After Free/Double Free in Garbage Collection | - |
| [MEM-155223](https://hackerone.com/reports/155223) | ibb | Use After Free Vulnerability in array_walk()/array_walk_recursive() | - |
| [MEM-159948](https://hackerone.com/reports/159948) | ibb | Use After Free Vulnerability in unserialize() | - |
| [MEM-172115](https://hackerone.com/reports/172115) | ibb | Multiple use after frees in obj2ast_* methods | - |
| [MEM-175982](https://hackerone.com/reports/175982) | ibb | Use-after-free in unserialize() | - |
| [MEM-180909](https://hackerone.com/reports/180909) | ibb | Use-after-free in ArrayObject Deserialization | - |
| [MEM-182474](https://hackerone.com/reports/182474) | ibb | Use After Free in PHP7 unserialize() | - |
| [MEM-193517](https://hackerone.com/reports/193517) | shopify-scripts | attempting double-free using the mruby compiler `mrbc` | - |
| [MEM-198732](https://hackerone.com/reports/198732) | ibb | Use After Free in unserialize() | - |
| [MEM-206109](https://hackerone.com/reports/206109) | shopify-scripts | mruby heap use-after-free | - |
| [MEM-207710](https://hackerone.com/reports/207710) | shopify-scripts | Heap use-after-free in mrb_vm_exec | - |
| [MEM-245956](https://hackerone.com/reports/245956) | ibb | Use-after-free in PHP7's unserialize() | - |
| [MEM-259390](https://hackerone.com/reports/259390) | ibb | Use-after-free in XML::LibXML::Node::replaceChild | - |
| [MEM-261335](https://hackerone.com/reports/261335) | ibb | Heap Use After Free Read in unserialize() | - |
| [MEM-261338](https://hackerone.com/reports/261338) | ibb | Heap Use After Free in unserialize() | - |
| [MEM-295276](https://hackerone.com/reports/295276) | shopify-scripts | heap-use-after-free in OP_RESCUE | - |
| [MEM-371135](https://hackerone.com/reports/371135) | ibb | CVE-2018-12882: heap-use-after-free in PHP 7.2 through 7.2.6, possible 7.2.7 | - |
| [MEM-481532](https://hackerone.com/reports/481532) | putty_h1c | heap-use-after-free (READ of size 8) in main() | - |
| [MEM-527042](https://hackerone.com/reports/527042) | ibb | CVE-2019-0196: mod_http2 with scoreboard Use-After-Free (Read) | - |
| [MEM-672245](https://hackerone.com/reports/672245) | ibb | Use After Free in GC with Certain Destructors | - |
| [MEM-677557](https://hackerone.com/reports/677557) | ibb | mod_http2, memory corruption on early pushes (CVE-2019-10081) | - |
| [MEM-680415](https://hackerone.com/reports/680415) | ibb | mod_http2, read-after-free in h2 connection shutdown (CVE-2019-10082) | - |
| [MEM-692040](https://hackerone.com/reports/692040) | ibb | PHP 7.3.3: Heap-use-after-free (READ of size 8) in match_at() | - |
| [MEM-950299](https://hackerone.com/reports/950299) | ibb | Use after free vulnerability  in phar_parse_zipfile | - |
| [MEM-988103](https://hackerone.com/reports/988103) | nodejs | Node.js: use-after-free in TLSWrap | - |
| [MEM-1997312](https://hackerone.com/reports/1997312) | ibb | CVE-2023-28319: UAF in SSH sha256 fingerprint check | - |

## 2. The kernel crown: IPV6_2292PKTOPTIONS (MEM-826026, $10,000)

Vault maximum, and the module's only five figures. A missing lock in `setsockopt` lets the researcher free a shared option buffer mid-processing — then hijack the freed structure's embedded pointer for arbitrary kernel read/write:

> Due to missing locks in option `IPV6_2292PKTOPTIONS` of `setsockopt` , it is possible to race and free the `struct ip6_pktopts ` buffer, while it is being handled by `ip6_setpktopt`. This structure contains pointers (`ip6po_pktinfo`) that can be hijacked to obtain arbitrary kernel R/W primitives. As a consequence, it is easy to have kernel code execution. This vulnerability is reachable from WebKit sandbox and is available in the latest FW, that is 7.02.

> Attached is a Proof-Of-Concept that achieves a Local Privilege Escalation on FreeBSD 9 and FreeBSD 12.

Two pricing lessons in one row. First, the *chain value* dominates: the report explicitly frames the UAF as reachable from the WebKit sandbox, landing kernel execution from a web sandbox — the PlayStation ibb economics price the primitive, not the parser. Second, it is a *race-condition UAF* (free-while-in-use): the Time-of-check module of the Race vault and this module describe the same bug from opposite ends. The module's second resolver-side row, curl's TLS session-cache UAF (MEM-1180380, $2,000, CVE-2021-22901), prices two orders lower because a library crash is ranked below a kernel primitive.

## 3. The Flash UAF fleet ($2,000 flat + $5,000 anchors)

The second-largest money cluster: MEM-56385 and MEM-151043 at **$5,000**, four ASnative/TextField rows at **$2,000**. Every body is the same template — Summary, Description, Impact, Credit, CVE — with the class claim carried entirely by the title + CVE. The fleet's doctrine is credential-by-class: knowing the AS3 call order (`ps.release()` then `ps_.currentTime`) matters more than the heap grooming. Two rows escape the template:

- MEM-37240 (CVE-2014-0574): a double free produced by *two Flash workers* racing `bytearray.clear()`. The body is the race primitive verbatim:
  > The issue occurs while sharing a bytearray between two workers. If both call bytearray.clear() at the same time, Flash does not correctly handle the race and may double free the array.
- MEM-18843 (unpaid): the oldest Flash UAF in the vault, written as an analyst's field log — page-heap toggles, redirect repro, debugger paste. It is the only Flash report that reads like an experiment rather than a bulletin stub, and it carries no figure. Contrast is the lesson: the stub template paid; the field log did not (in this DB snapshot).

## 4. Interpreter vm UAFs: mruby

The mruby sandbox rows (`shopify-scripts`) price at the sandbox rate — $100–$1,000 — and every report is an ASan paste plus a one-line Ruby trigger. MEM-244904 ($800) is representative:

> Running the following ruby script in mruby compiled with ASAN enabled causes a use after free error:

> ==8219==ERROR: AddressSanitizer: heap-use-after-free on address 0x60800000b9f0 at pc 0x00000073de47 bp 0x7ffc2a5efa90 sp 0x7ffc2a5efa88

MEM-184715 ($1,000) adds the scope caveat that makes the report triage-friendly: the UAF *doesn't* affect the production engine under its current limits — reach is stated, not oversold:

> Slightly different one, this is a use after free (as reported by an ASAN compiled binary). This one *doesn't* affect mruby-engine with the current instruction limit and memory limit, but if they are increased then it does.

MEM-295276 (`-`) is the same format with a `def…ensure…rescue…yield` trigger — the unpaid tail of the same mine. Note the cross-module shadow: MEM-216700 (adjacent-unclassified pool, same `mrb_vm_exec` UAF shape) reinforces that the vm_exec frame is the single most-reported mruby site in the corpus.

## 5. The PHP unserialize fleet

Eleven-plus rows (159948, 175982, 182474, 198732, 245956, 261335, 261338, 180909, 152266 …) — mostly link-only or short bodies (`The bug report at: https://bugs.php.net/bug.php?id=69425` is the entire body of MEM-198732). Paid members of the class sit in the Out-of-Bounds module (200909, 261336 at $500). Doctrine: the `unserialize()` UAF farm is a *PHP-engine* corpus, not an application corpus — the reports point at bugs.php.net, and the HackerOne row is the bounty wrapper. Quote nothing here; the title + `src` field is the evidence.

## 6. What pays / what doesn't

- **Pays**: kernel-R/W from a web-sandbox-reachable race ($10,000); Flash UAF flat ($2,000–$5,000); Brave V8 renderer UAF ($3,000 — modern browser-extension economy); mruby sandbox UAFs ($100–$1,000); PHP upstream-bug-linked UAFs ($500).
- **Doesn't pay (in this corpus)**: the Flash field-log row (MEM-18843), the Flash workers double-free (MEM-37240, full body, no figure), MEM-295276's vm UAF (full ASan body, no figure), and all 30 unpaid CVE-titled rows (mod_http2 trio, PHP 7.x match_at, Node TLSWrap). Pattern: unpaid = no sandbox/economy behind the report. The same ASan output pays $800 inside the Shopify sandbox and $0 on a bare `ibb` CVE row.
- **The double-free subset** is tiny: MEM-56385 ($5,000), MEM-146200 (`-`), MEM-193719 ($200), MEM-37240 (`-`). Double-free alone does not price the class; *which process* frees twice does.

## 7. Cross-references

- **Race-Conditions vault** — MEM-826026 (§2) and MEM-37240 (§3) are race UAFs; the Race playbook's `renameat2`/`oplock` sync ladder is this module's §2 exploit file.
- **RCE vault module 03** — the unserialize-UAF fleet (§5) belongs to the deserialization lane; the RCE vault files the phar/pickle rows under deserialization and `unserialize()` UAFs under memory corruption. This vault keeps the *memory-safety* half — read both.
- **Heap module** — MEM-56385's "double-free that could lead to code execution" (APSB language, $5,000) pairs with Heap §4's Flash fleet: same reporter economy, adjacent mechanism.
- **Adjacent pool** — MEM-216700 (mruby vm UAF, unpaid, unclassified) and MEM-1219491 (GHSL CWE-415 double-free *CodeQL query*, $1,800) are the two limit cases: no body vs. no bug.
