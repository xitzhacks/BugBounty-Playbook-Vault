---
title: "Memory-corruption vault module — heap/classic buffer overflow (113 full-body + 2 link-only rows)"
type: playbook
category: memory-corruption
cwe: "CWE-122"
source_count: 115
full_bodies_available: "113/115"
corpus: "h1-brain disclosed_reports.db (sha256 8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4) — 352-row vault; 336-row memory-corruption bucket"
list_accessed: "2026-11-07"
note: "MEM module 1/6. Anchors: MEM-542180 (Left4Dead2 NAV EIP control, $10,000), MEM-1180252 (Steam SILK decoder, $7,500), MEM-630462 (PuTTY SSH1 heap overflow, $3,645.90), the Flash heap-overflow fleet ($2,000 × 10+). 44/115 rows carry bounty figures; module floor $76,573."
---

# Heap & Classic Buffer Overflow

## 1. Overview

The largest module in the vault by row count (115 rows, 44 paid, **$76,573**). It is the only module whose money comes from *client-side binary parsers* rather than server interpreters: the crown rows are a game map file and a voice codec, the long tail is PHP/GD image parsing, mruby sandbox overflows, and tcpdump protocol parsers. Doctrine: when attacker-controlled file bytes flow into a C function that trusts a length field, the report is one crafted file plus a debugger screenshot (EIP or ASan line) — and, against the right targets (valve), that is a five-figure payout with no web endpoint at all.

**Case-stock (115 rows / $76,573):**

| Case | Target | Mechanism | Bounty |
|---|---|---|---|
| [MEM-542180](https://hackerone.com/reports/542180) | valve | Malformed NAV file leads to buffer overflow and code execution in Left4Dead2.exe | $10,000 |
| [MEM-1180252](https://hackerone.com/reports/1180252) | valve | Buffer overrun in Steam SILK voice decoder | $7,500 |
| [MEM-119652](https://hackerone.com/reports/119652) | ibb | Adobe Flash Player ASnative(101,10) Memory Corruption Vulnerability | $5,000 |
| [MEM-151039](https://hackerone.com/reports/151039) | ibb | Adobe Flash Player TimedEvent.parent Memory Corruption Vulnerability | $5,000 |
| [MEM-630462](https://hackerone.com/reports/630462) | putty_h1c | Heap overflow happen when receiving short length key from ssh server using ssh protocol 1 | $3,645.90 |
| [MEM-119657](https://hackerone.com/reports/119657) | ibb | Adobe Flash Player Race Condition Vulnerability | $2,000 |
| [MEM-138516](https://hackerone.com/reports/138516) | ibb | Adobe Flash Player ContentFactory class Memory Corruption Vulnerability | $2,000 |
| [MEM-138517](https://hackerone.com/reports/138517) | ibb | Adobe Flash Player Metadata class Memory Corruption Vulnerability | $2,000 |
| [MEM-138518](https://hackerone.com/reports/138518) | ibb | Adobe Flash Player OpportunityGenerator class Memory Corruption Vulnerability | $2,000 |
| [MEM-145265](https://hackerone.com/reports/145265) | ibb | Adobe Flash Player ShimContentFactory class Memory Corruption Vulnerability | $2,000 |
| [MEM-145266](https://hackerone.com/reports/145266) | ibb | Adobe Flash Player ShimContentFactory.retrieveResolvers Memory Corruption Vulnerability | $2,000 |
| [MEM-145267](https://hackerone.com/reports/145267) | ibb | Adobe Flash Player ShimContentResolver.configure Memory Corruption Vulnerability | $2,000 |
| [MEM-145269](https://hackerone.com/reports/145269) | ibb | Adobe Flash Player ShimOpportunityGenerator class Memory Corruption Vulnerability | $2,000 |
| [MEM-145271](https://hackerone.com/reports/145271) | ibb | Adobe Flash Player ShimContentResolver(resolverType=0) class Memory Corruption Vulnerability | $2,000 |
| [MEM-145272](https://hackerone.com/reports/145272) | ibb | Adobe Flash Player ShimContentResolver(resolverType=1) class Memory Corruption Vulnerability | $2,000 |
| [MEM-151040](https://hackerone.com/reports/151040) | ibb | Adobe Flash Player ShimAdPolicySelector(adPolicySelectorType=0) class Memory Corruption | $2,000 |
| [MEM-397545](https://hackerone.com/reports/397545) | valve | Malformed .BMP file in Counter-Strike 1.6 may cause shellcode injection | $2,000 |
| [MEM-1352429](https://hackerone.com/reports/1352429) | ibb | CVE-2021-3711: SM2 decrypt  buffer overflow | $2,000 |
| [MEM-188102](https://hackerone.com/reports/188102) | ibb | 3 heap corruptions in PHP | $1,500 |
| [MEM-476168](https://hackerone.com/reports/476168) | ibb | Heap overflow in utf32be_mbc_to_code | $1,500 |
| [MEM-476179](https://hackerone.com/reports/476179) | ibb | Buffer over-write in finfo_open with malformed magic file. | $1,500 |
| [MEM-504761](https://hackerone.com/reports/504761) | ibb | phar_tar_writeheaders_int() buffer overflow | $1,500 |
| [MEM-1084342](https://hackerone.com/reports/1084342) | ibb | Buffer overflow in PyCArg_repr in _ctypes/callproc.c for Python 3.x to 3.9.1 | $1,500 |
| [MEM-484398](https://hackerone.com/reports/484398) | vlc_h1c | Buffer overflow in libavi_plugin memmove() call | $1,126.91 |
| [MEM-161193](https://hackerone.com/reports/161193) | ibb | imagegammacorrect allows arbitrary write access | $1,000 |
| [MEM-170138](https://hackerone.com/reports/170138) | ibb | SEH buffer overflow msgfmt_format_message | $1,000 |
| [MEM-535827](https://hackerone.com/reports/535827) | shopify-scripts | Buffer overflow in yywarning_s | $1,000 |
| [MEM-192362](https://hackerone.com/reports/192362) | shopify-scripts | Heap Overflow in mrb_arb_splice | $800 |
| [MEM-194906](https://hackerone.com/reports/194906) | shopify-scripts | Heap overflow due to off-by-one when expanding stack | $800 |
| [MEM-204421](https://hackerone.com/reports/204421) | shopify-scripts | Heap buffer oveflow with many arguments | $800 |
| [MEM-110722](https://hackerone.com/reports/110722) | ibb | Heap BufferOver Flow in escapeshellargs and escapeshellcmd functions | $500 |
| [MEM-153776](https://hackerone.com/reports/153776) | ibb | gdImageTrueColorToPaletteBody allows arbitrary write/read access | $500 |
| [MEM-167904](https://hackerone.com/reports/167904) | ibb | heap overflow in substr_replace | $500 |
| [MEM-167910](https://hackerone.com/reports/167910) | ibb | memory corruption in wordwrap function | $500 |
| [MEM-170260](https://hackerone.com/reports/170260) | ibb | imap_rfc822_parse_headers GS Violation | $500 |
| [MEM-175315](https://hackerone.com/reports/175315) | ibb | Illegal write access through Locale methods | $500 |
| [MEM-182420](https://hackerone.com/reports/182420) | ibb | Illegal write/read access caused by gdImageAALine overflow | $500 |
| [MEM-190933](https://hackerone.com/reports/190933) | ibb | Invalid parameter in memcpy function trough openssl_pbkdf2 | $500 |
| [MEM-192127](https://hackerone.com/reports/192127) | ruby | Buffer underflow in sprintf | $500 |
| [MEM-784186](https://hackerone.com/reports/784186) | nodejs | napi_get_value_string_X allow various kinds of memory corruption | $250 |
| [MEM-798301](https://hackerone.com/reports/798301) | filezilla | FileZilla 3.46.3 - 'Scale factor' Buffer Overflow | $250 |
| [MEM-550696](https://hackerone.com/reports/550696) | curl | CVE-2019-5436: Heap Buffer Overflow at lib/tftp.c | $200 |
| [MEM-208363](https://hackerone.com/reports/208363) | shopify-scripts | Memory corrouption in mrb_gc_mark | $100 |
| [MEM-218803](https://hackerone.com/reports/218803) | shopify-scripts | SIGABRT in sym_validate_len - symbol.c:44 | $100 |
| [MEM-66962](https://hackerone.com/reports/66962) | ibb | Misusing of FPU Instruction Could Cause Security Vulnerabilities in Adobe Flash Player | - |
| [MEM-112386](https://hackerone.com/reports/112386) | torproject | smartlist_add, smartlist_insert (may) cause heap corruption as a result of inadequate checks in smartlist_ensure_capacity | - |
| [MEM-112784](https://hackerone.com/reports/112784) | torproject | libevent (stack) buffer overflow in evutil_parse_sockaddr_port | - |
| [MEM-115702](https://hackerone.com/reports/115702) | torproject | [tor] libevent dns OOB read | - |
| [MEM-122256](https://hackerone.com/reports/122256) | ibb | Adobe Flash Player  Uninitialised Memory Corruption | - |
| [MEM-138025](https://hackerone.com/reports/138025) | torproject | Heap corruption via memarea.c | - |
| [MEM-139879](https://hackerone.com/reports/139879) | ibb | Adobe Flash Player Regular Expression UAF Remote Code Execution Vulnerability | - |
| [MEM-141839](https://hackerone.com/reports/141839) | ibb | Multiple vulnerabilities related to PCRE functions (already fixed) | - |
| [MEM-142472](https://hackerone.com/reports/142472) | ibb | CVE-2016-2177 Undefined pointer arithmetic in SSL code | - |
| [MEM-159992](https://hackerone.com/reports/159992) | ibb | memory allocator fails to realloc small block to large one | - |
| [MEM-160295](https://hackerone.com/reports/160295) | ibb | Heap overflow in curl_escape | - |
| [MEM-163459](https://hackerone.com/reports/163459) | torproject | potential memory corruption in or/buffers.c (particularly on 32 bit) | - |
| [MEM-168485](https://hackerone.com/reports/168485) | irccloud | Exposed, outdated nginx server (v1.4.6) potentially vulnerable to heap-based buffer overflow & RCE | - |
| [MEM-172403](https://hackerone.com/reports/172403) | ibb | Python 2.7 32-bit JSON encoding heap corruption | - |
| [MEM-174069](https://hackerone.com/reports/174069) | ibb | Buffer overflow in HTTP parse_hostinfo(), parse_userinfo() and parse_scheme() | - |
| [MEM-176279](https://hackerone.com/reports/176279) | ibb | Heap overflow in mysqlnd related to BIT fields (CVE-2016-7412) | - |
| [MEM-180562](https://hackerone.com/reports/180562) | ibb | Memory corruption in _php_math_number_format_ex() | - |
| [MEM-180572](https://hackerone.com/reports/180572) | ibb | Memory corruption due to missing check size in _php_math_number_format_ex() | - |
| [MEM-192318](https://hackerone.com/reports/192318) | shopify-scripts | mrb_vformat() heap overflow could lead to code execution | - |
| [MEM-192665](https://hackerone.com/reports/192665) | shopify-scripts | heap-buffer-overflow on mruby | - |
| [MEM-193773](https://hackerone.com/reports/193773) | shopify-scripts | SIGABRT - mrb_default_allocf | - |
| [MEM-195586](https://hackerone.com/reports/195586) | ibb | Memory corruption when parsing a hostile PHAR archive | - |
| [MEM-198452](https://hackerone.com/reports/198452) | shopify-scripts | SIGABRT - mrb_realloc_simple - gc.c - line:201 | - |
| [MEM-202960](https://hackerone.com/reports/202960) | ibb | CVE-2017-5204: The IPv6 parser in tcpdump before 4.9.0 has a buffer overflow in print-ip6.c:ip6_print() | - |
| [MEM-202965](https://hackerone.com/reports/202965) | ibb | CVE-2017-5341 The OTV parser in tcpdump before 4.9.0 has a buffer overflow in print-otv.c:otv_print() | - |
| [MEM-202967](https://hackerone.com/reports/202967) | ibb | CVE-2017-5484 The ATM parser in tcpdump before 4.9.0 has a buffer overflow in print-atm.c:sig_print() | - |
| [MEM-202968](https://hackerone.com/reports/202968) | ibb | CVE-2017-5342 In tcpdump before 4.9.0 a bug in multiple protocol parsers could cause a buffer overflow in print-ether.c:ether_print() | - |
| [MEM-202969](https://hackerone.com/reports/202969) | ibb | CVE-2017-5482 The Q.933 parser in tcpdump before 4.9.0 has a buffer overflow in print-fr.c:q933_print(). | - |
| [MEM-205284](https://hackerone.com/reports/205284) | shopify-scripts | SIGABRT - method_missing - mark_context_stack | - |
| [MEM-207983](https://hackerone.com/reports/207983) | ibb | read outside of buffer (heap buffer overflow) in S_regmatch - regexec.c:6057 | - |
| [MEM-209765](https://hackerone.com/reports/209765) | shopify-scripts | Heap buffer overflow in mruby value_move | - |
| [MEM-212882](https://hackerone.com/reports/212882) | shopify-scripts | SIGABRT in only mirb | - |
| [MEM-214000](https://hackerone.com/reports/214000) | shopify-scripts | SIGABRT - mirb and mruby | - |
| [MEM-215967](https://hackerone.com/reports/215967) | shopify-scripts | SIGABRT in mrb_debug_info_append_file | - |
| [MEM-216725](https://hackerone.com/reports/216725) | shopify-scripts | SIGABRT - in free | - |
| [MEM-221251](https://hackerone.com/reports/221251) | shopify-scripts | heap-buffer-overflow (read outside of buffer) in mrb_vm_exec() | - |
| [MEM-221785](https://hackerone.com/reports/221785) | ibb | OOB write in MDC2_Update() (CVE-2016-6303) | - |
| [MEM-221788](https://hackerone.com/reports/221788) | ibb | OOB write in BN_bn2dec() (CVE-2016-2182) | - |
| [MEM-227762](https://hackerone.com/reports/227762) | shopify-scripts | Heap Overflow in fiber_switch triggered from Fiber.transfer | - |
| [MEM-232150](https://hackerone.com/reports/232150) | ibb | heap-buffer-overflow (READ of size 11) in Perl 5.25.x | - |
| [MEM-233440](https://hackerone.com/reports/233440) | ibb | heap-buffer-overflow (READ of size 61) in Perl_re_intuit_start() | - |
| [MEM-237915](https://hackerone.com/reports/237915) | ibb | PHP mbstring / Oniguruma multiple remote heap/stack corruptions | - |
| [MEM-248601](https://hackerone.com/reports/248601) | ibb | PHP INI Parsing Stack Buffer Overflow Vulnerability | - |
| [MEM-248609](https://hackerone.com/reports/248609) | ibb | PHP OpenSSL zif_openssl_seal() heap overflow (wild memcpy) | - |
| [MEM-295380](https://hackerone.com/reports/295380) | shopify-scripts | heap-buffer-overflow in OP_R_BREAK | - |
| [MEM-337986](https://hackerone.com/reports/337986) | ibb | CVE-2018-6797:  A crafted regular expression can cause a heap buffer write overflow in Perl 5 giving a remote attacker control over bytes written | - |
| [MEM-351014](https://hackerone.com/reports/351014) | valve | Malformed .BSP Access Violation in CS:GO can lead to Remote Code Execution | - |
| [MEM-351016](https://hackerone.com/reports/351016) | valve | Malformed Skybox .TGA in Half-Life (GoldSRC) leads to Access Violation | - |
| [MEM-384214](https://hackerone.com/reports/384214) | ibb | heap-buffer-overflow (READ of size 48) in exif_read_data() | - |
| [MEM-470520](https://hackerone.com/reports/470520) | valve | RCE on Steam Client via buffer overflow in Server Info | - |
| [MEM-477073](https://hackerone.com/reports/477073) | ibb | ZeroMQ libzmq remote code execution | - |
| [MEM-482200](https://hackerone.com/reports/482200) | putty_h1c | puttygen: heap-buffer-overflow in mp_get_decimal() | - |
| [MEM-510336](https://hackerone.com/reports/510336) | ibb | Uninitialized read in exif_process_IFD_in_TIFF | - |
| [MEM-510887](https://hackerone.com/reports/510887) | ibb | [CVE-2018-18312] regcomp: heap-buffer-overflow write / reg_node overrun | - |
| [MEM-510888](https://hackerone.com/reports/510888) | ibb | [CVE-2018-18313] regcomp: heap-buffer-overflow read in S_grok_bslash_N | - |
| [MEM-641240](https://hackerone.com/reports/641240) | ibb | Basic Authentication Heap Overflow | - |
| [MEM-674540](https://hackerone.com/reports/674540) | ibb | mod_remoteip stack buffer overflow and NULL pointer dereference | - |
| [MEM-684603](https://hackerone.com/reports/684603) | curl | CVE-2019-5482: Heap buffer overflow in TFTP when using small blksize | - |
| [MEM-778610](https://hackerone.com/reports/778610) | ibb | Squid as reverse proxy RCE and data leak | - |
| [MEM-789034](https://hackerone.com/reports/789034) | ibb | Buffer Overflow in ext_lm_group_acl helper | - |
| [MEM-800324](https://hackerone.com/reports/800324) | ibb | Several protocol parsers in before 4.9.2 could cause a buffer overflow in util-print.c:bittok2str_internal() | - |
| [MEM-816637](https://hackerone.com/reports/816637) | ibb | CVE-2020-10938-buffer overflow/out-of-bounds write in compress.c:HuffmanDecodeImage() | - |
| [MEM-824771](https://hackerone.com/reports/824771) | ibb | UrnState Heap Overflow | - |
| [MEM-888986](https://hackerone.com/reports/888986) | ibb | [CVE-2020-10543] Buffer overflow caused by a crafted regular expression | - |
| [MEM-965914](https://hackerone.com/reports/965914) | nodejs | `fs.realpath.native` on darwin may cause buffer overflow | - |
| [MEM-1047086](https://hackerone.com/reports/1047086) | ibb | Heap buffer overflow vulnerability while processing a malformed TIFF file. | - |
| [MEM-1434056](https://hackerone.com/reports/1434056) | ibb | Buffer overflow in req_parsebody method in lua_request.c | - |
| [MEM-1455248](https://hackerone.com/reports/1455248) | ibb | Buffer Overflow in optimized_escape_html method | - |
| [MEM-1511619](https://hackerone.com/reports/1511619) | ibb | Read and write beyond bounds in mod_sed | - |
| [MEM-2621057](https://hackerone.com/reports/2621057) | ibb | libcurl: freeing stack buffer during x509 certificate parsing | - |
| [MEM-2974850](https://hackerone.com/reports/2974850) | ibb | CVE-2025-0725: Heap overflow in curl with Content-Encoding gzip and old libz versions | - |

## 2. The valve file-parser lane: crafted file → EIP control

MEM-542180 (valve, **$10,000**) is the cleanest statement of the lane — a navigation-mesh file parsed at map load:

> In the parsing routines of NAV files (which contain the navigation mesh used by the AI for survivor bots, zombies, and the AI director spawning system) a buffer overflow exists which can be used to control the EIP register and takeover code execution.

> Observe that EIP becomes 0x41414102, indicating that a buffer overflow has occurred and code execution is possible

The report adds the exploitability note that research on every modern game binary still starts from: a module that ships without ASLR removes the need for an infoleak. MEM-397545 (valve, **$2,000**) is the same lane in GoldSource-era form — a server-sent BMP overwriting the client's stack on connect. Together they fix the module's pricing rule: reach (remote file → code execution) sets the tier; the primitive (heap vs stack) does not.

## 3. The Steam SILK voice decoder (MEM-1180252, $7,500)

The second valve crown is a *protocol* parser, not a map file — compressed voice data decoded by the SteamWorks SDK:

> 8 bytes - steamid
> 1 byte - payload type
> 2 bytes - payload size
> <payload data>
> 4 bytes - CRC checksum

> There are numerous payload types available, including Opus PLC, Opus, SILK, Raw and Silence. The bug being considered here is specific to the SILK decoder.

Sizes are pulled from the attacker-controlled payload (`nPayloadSize` doubles each frame) — the classic trusted-length-field geometry. Pay note: decoder entry points reachable by *another player's voice packet* price like the file lane, because the delivery is network-local without any web surface.

## 4. The Flash heap fleet ($2,000 tier, 11+ rows)

Flash's contribution is a flat-rate fleet, all `ibb`, mostly $2,000 with two $5,000 anchors. Two report formats recur:

- **EIP-hijack rows** (MEM-119652, **$5,000**):
  > When ASnative(101,10) is called with a MovieClip object pointer, Flash Player is crashed due to an invalid EIP value. Carefully crafted swf file may allow the attacker to hijack the EIP, leading to shellcode execution in the context of affected application.
- **Type-confusion-by-uninitialized-field rows** (MEM-151039, **$5,000**):
  > Adobe Flash Player is prone to a vulnerability which leads to memory corruption because of uninitialize memory of TimedEvent.parent.
  > Normally, TimedEvent class should initialize the memory of its parent field.
  > The poc code trigger the crash while trying to build a TimeEvent Class by calling the contructor at 0x13371337.

(sic — "trigger", "contructor".) The body then ships AS3 PoC filling a `ByteArray` with `0x13371337` — the era's signature fill word. The unpaid sibling MEM-122256 (valgrind-tainted uninitialized-value report) shows the floor: a crash-without-crashes-well report at $0. This fleet is the vault's clearest era artifact: Adobe was paying flat rates for plugin-class memory corruption, and the RCE vault's Flash quartet (RCE-2106/2170/47232/47234, $10,000-tier list) is the same economy at a different tier.

## 5. Network-protocol parsers: PuTTY SSH1 and the tcpdump fleet

MEM-630462 (putty_h1c, **$3,645.90**) is the module's protocol-parsing exemplar — a malicious *server* attacking a client:

> There's no check in `ssh1_login_process_queue` function when read `servkey` and `hostkey` length from packet which may cause heap overflow.
> Remote code execution may be possible.

The body walks a full reproduction rig (patched OpenSSH sshd as SSH1 server, ASan-built PuTTY) — the "malicious server, benign client" direction that web hunters rarely test. Below it, the corpus carries cheaper protocol-parser rows: curl's TFTP heap overflow (MEM-550696, $200), Node's native realpath (MEM-965914, `-`), and the tcpdump parser fleet (MEM-202960–202969 cluster, OOB/overflow rows across IPv6/OTV/ATM/ether/Q.933, all `-`). Pricing tracks *deployment*: libraries every attacker must parse packets with at scale price highest.

## 6. What pays / what doesn't

- **Pays**: valve file/voice parsers ($2,000–$10,000) — remote file → code execution; Flash heap corruption at flat $2,000–$5,000; protocol parsers at $200–$3,646 (deployment-dependent); PHP/GD string-family $500 flat; mruby sandbox overflows $100–$1,000. 44/115 rows carry figures; 71 carry none — `-` means the DB row has no figure, not that triage rejected it.
- **Doesn't pay (in this corpus)**: MEM-122256's valgrind-only uninitialized report; MEM-139879's CVE-attached regex UAF (full exploit claimed in body, no figure); the entire tcpdump packet-printer fleet (correct CVEs, no figures). Pattern: a crash with a CVE is still ranked below demonstrated control — but Flash's $2,000 flat kept even non-exploit rows paid, so "no PoC, just CVE" is the valley, not a hard wall.
- **Link-only rows** (2): MEM-167904 / MEM-167910 bodies are single bugs.php.net links (`Please check: https://bugs.php.net/bug.php?id=72877` pattern) — keep them as corpus rows, quote the title only. The PHP flat $500 with a 51-byte body is itself data: the upstream-bug-ticket submission format was a paid product line in the ibb era.

## 7. Cross-references

- **RCE vault module 04** (`RCE/04_Memory-Corruption-Code-Execution.md`) covers the same Flash/mruby economy from the execution angle — read its §2 (RIP control) beside this module's §4, and treat RCE-181879's mruby Struct confusion as the interpreter cousin of §4's Flash fleet.
- **Null-Deref-and-Stack-Crashes** — MEM-489102 (VLC SEH stack overflow) and MEM-175587 (GD stack overflow) sit one column over; the heap-vs-stack split is a classifier convenience, not a security boundary.
- **Out-of-Bounds-Overread-Reads** — MEM-221251's heap-buffer-overflow READ is the bridge (classified OOB-read-adjacent; frozen here as heap).
- **Race-Conditions vault** — MEM-119657 (Flash race condition) is a TOCTOU bug wearing a heap-overflow costume; race primitives are this vault's industrial base.
