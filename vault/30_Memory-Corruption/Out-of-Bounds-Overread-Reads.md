---
title: "Memory-corruption vault module — out-of-bounds overread/read (all 68 rows full-body)"
type: playbook
category: memory-corruption
cwe: "CWE-125"
source_count: 68
full_bodies_available: "68/68"
corpus: "h1-brain disclosed_reports.db (sha256 8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4) — 352-row vault; 336-row memory-corruption bucket"
list_accessed: "2026-11-07"
note: "MEM module 3/6. Anchors: MEM-807772 (Source-engine OOB → RCE via entity-index, $7,500 — sole five-figure-adjacent overread), the exif/GD PHP fleet ($500–$1,500), MEM-746766 (Python AST OOB ×2 CVEs, $2,000), MEM-2658447 (NGINX mp4 overread, $2,142). 27/68 rows carry bounty figures; module floor $30,192."
---

# Out-of-Bounds Overread / Read

## 1. Overview

Sixty-eight rows, 27 paid, **$30,192** — the vault's only module where *every* row has a full body (no link-only rows). The economics invert module 01's: reads price low, so the module's money lives in reads that reach *virtual-function calls* (valve) and reads in *universally deployed parsers* (NGINX, Python AST, PHP exif/GD). Doctrine: an overread is a report of its reader — the bounty is set by what the caller does with the out-of-bounds pointer (crash = CVE bookkeeping, vtable call = RCE, worker termination = $2,142).

**Case-stock (68 rows / $30,192):**

| Case | Target | Mechanism | Bounty |
|---|---|---|---|
| [MEM-807772](https://hackerone.com/reports/807772) | valve | OOB reads in network message handlers leads to RCE | $7,500 |
| [MEM-2658447](https://hackerone.com/reports/2658447) | ibb | CVE-2024-7347: Buffer overread in the ngx_http_mp4_module | $2,142 |
| [MEM-746766](https://hackerone.com/reports/746766) | ibb | Two out-of-bounds array reads in Python AST builder (Re-opening 520612 with CVEs) | $2,000 |
| [MEM-478368](https://hackerone.com/reports/478368) | ibb | imagecolormatch Out Of Bounds Write on Heap | $1,500 |
| [MEM-593229](https://hackerone.com/reports/593229) | ibb | Out-of-bounds read in iconv.c:_php_iconv_mime_decode() due to integer overflow | $1,500 |
| [MEM-665330](https://hackerone.com/reports/665330) | ibb | Out of Bounds Memory Read in php_jpg_get16 | $1,500 |
| [MEM-675578](https://hackerone.com/reports/675578) | ibb | Out of Bounds Memory Read in exif_scan_thumbnail | $1,500 |
| [MEM-675580](https://hackerone.com/reports/675580) | ibb | Out of Bounds Memory Read in exif_process_user_comment | $1,500 |
| [MEM-161189](https://hackerone.com/reports/161189) | ibb | select_colors write out-of-bounds | $1,000 |
| [MEM-633607](https://hackerone.com/reports/633607) | shopify-scripts | Invalid read in `str_replace_partial` | $1,000 |
| [MEM-295680](https://hackerone.com/reports/295680) | shopify-scripts | Invalid read leading to a segfault | $800 |
| [MEM-891846](https://hackerone.com/reports/891846) | ibb | CVE-2020-9383 Floppy OOB read | $750 |
| [MEM-110720](https://hackerone.com/reports/110720) | ibb | Arbitary Memory Read via gdImageRotateInterpolated Array Index Out of Bounds | $500 |
| [MEM-135291](https://hackerone.com/reports/135291) | ibb | Out-of-bounds reads in zif_grapheme_stripos with negative offset | $500 |
| [MEM-141197](https://hackerone.com/reports/141197) | ibb | get_icu_value_internal out-of-bounds read | $500 |
| [MEM-141202](https://hackerone.com/reports/141202) | ibb | imagescale out-of-bounds read | $500 |
| [MEM-146940](https://hackerone.com/reports/146940) | ibb | pass2_no_dither out-of-bounds access | $500 |
| [MEM-152782](https://hackerone.com/reports/152782) | ibb | locale_accept_from_http out-of-bounds access | $500 |
| [MEM-152784](https://hackerone.com/reports/152784) | ibb | imagegif/output out-of-bounds access | $500 |
| [MEM-175310](https://hackerone.com/reports/175310) | ibb | Write out-of-bounds at number_format | $500 |
| [MEM-178144](https://hackerone.com/reports/178144) | ibb | imagecropauto out-of-bounds access | $500 |
| [MEM-200909](https://hackerone.com/reports/200909) | ibb | Out of bounds memory read in unserialize() | $500 |
| [MEM-477897](https://hackerone.com/reports/477897) | ibb | buffer overread in base64 code of the xmlrpc module | $500 |
| [MEM-778834](https://hackerone.com/reports/778834) | ibb | OOB read in php_strip_tags_ex | $500 |
| [MEM-831353](https://hackerone.com/reports/831353) | ibb | tcpdump before 4.9.3 has a heap-based buffer over-read related to aoe_print in print-aoe.c and lookup_emem in addrtoname.c | $500 |
| [MEM-964582](https://hackerone.com/reports/964582) | ibb | CVE-2017-13040 The MPTCP parser in tcpdump before 4.9.2 has a buffer over-read in print-mptcp.c, several functions. | $500 |
| [MEM-964583](https://hackerone.com/reports/964583) | ibb | CVE-2017-13041 The ICMPv6 parser in tcpdump before 4.9.2 has a buffer over-read in print-icmp6.c:icmp6_nodeinfo_print(). | $500 |
| [MEM-112632](https://hackerone.com/reports/112632) | torproject | [tor] libevent dns remote stack overread vulnerability | - |
| [MEM-114414](https://hackerone.com/reports/114414) | ibb | openssl_seal() uninitialized memory usage | - |
| [MEM-152231](https://hackerone.com/reports/152231) | ibb | Out of bound read in exif_process_IFD_in_MAKERNOTE | - |
| [MEM-160294](https://hackerone.com/reports/160294) | ibb | Memory Leakage In exif_process_IFD_in_TIFF (CVE-2016-7128) | - |
| [MEM-167888](https://hackerone.com/reports/167888) | ibb | Uninitialized Thumbail Data Leads To Memory Leakage in exif_process_IFD_in_TIFF | - |
| [MEM-167895](https://hackerone.com/reports/167895) | ibb | Out of bound when verify signature of zip phar in phar_parse_zipfile | - |
| [MEM-167896](https://hackerone.com/reports/167896) | ibb | Out of bound when verify signature of tar phar in phar_parse_tarfile | - |
| [MEM-170618](https://hackerone.com/reports/170618) | ibb | CVE-2016-7418 PHP Out-Of-Bounds Read in php_wddx_push_element | - |
| [MEM-188661](https://hackerone.com/reports/188661) | ibb | Invalid read when wddx decodes empty boolean element | - |
| [MEM-209949](https://hackerone.com/reports/209949) | ruby | Arbitrary heap exposure in JSON.generate | - |
| [MEM-221789](https://hackerone.com/reports/221789) | ibb | OOB read in TS_OBJ_print_bio() (CVE-2016-2180) | - |
| [MEM-221790](https://hackerone.com/reports/221790) | ibb | Certificate message OOB reads (CVE-2016-6306) | - |
| [MEM-241610](https://hackerone.com/reports/241610) | ibb | ap_find_token() Buffer Overread | - |
| [MEM-248659](https://hackerone.com/reports/248659) | ibb | PHP WDDX Deserialization Heap OOB Read in timelib_meridian() | - |
| [MEM-261336](https://hackerone.com/reports/261336) | ibb | Out of Bounds Memory Read in unserialize() | - |
| [MEM-268803](https://hackerone.com/reports/268803) | ibb | CVE-2017-12985: The IPv6 parser in tcpdump before 4.9.2 has a buffer over-read in ip6_print() | - |
| [MEM-268804](https://hackerone.com/reports/268804) | ibb | CVE-2017-12986 The IPv6 routing header parser in tcpdump before 4.9.2 has a buffer over-read in print-rt6.c:rt6_print(). | - |
| [MEM-268805](https://hackerone.com/reports/268805) | ibb | CVE-2017-13008 The IEEE 802.11 parser in tcpdump before 4.9.2 has a buffer over-read in print-802_11.c:parse_elements(). | - |
| [MEM-268806](https://hackerone.com/reports/268806) | ibb | CVE-2017-13009 The IPv6 mobility parser in tcpdump before 4.9.2 has a buffer over-read in print-mobility.c:mobility_print(). | - |
| [MEM-268807](https://hackerone.com/reports/268807) | ibb | CVE-2017-13010 The BEEP parser in tcpdump before 4.9.2 has a buffer over-read in print-beep.c:l_strnstart(). | - |
| [MEM-268808](https://hackerone.com/reports/268808) | ibb | CVE-2017-13038 The PPP parser in tcpdump before 4.9.2 has a buffer over-read in print-ppp.c:handle_mlppp(). | - |
| [MEM-283644](https://hackerone.com/reports/283644) | ibb | Out-Of-Bounds Read in timelib_meridian() | - |
| [MEM-344035](https://hackerone.com/reports/344035) | ibb | Heap Buffer Overflow (READ: 1786) in exif_iif_add_value | - |
| [MEM-456727](https://hackerone.com/reports/456727) | ibb | null pointer dereference in imap_mail | - |
| [MEM-475499](https://hackerone.com/reports/475499) | ibb | heap buffer overflow in phar_detect_phar_fname_ext | - |
| [MEM-477344](https://hackerone.com/reports/477344) | ibb | Heap Buffer Overflow (READ: 4) in phar_parse_pharfile | - |
| [MEM-480778](https://hackerone.com/reports/480778) | ibb | Heap-buffer-overflow in Perl__byte_dump_string (utf8.c) could lead to memory leak | - |
| [MEM-481335](https://hackerone.com/reports/481335) | notepad-plus-plus | Security check failure or stack buffer overrun (crash) | - |
| [MEM-510025](https://hackerone.com/reports/510025) | ibb | Invalid Read on exif_process_SOFn | - |
| [MEM-724243](https://hackerone.com/reports/724243) | ibb | Tcpdump before 4.9.3 has a buffer over-read in print-802_11.c (CVE-2018-16227) | - |
| [MEM-724253](https://hackerone.com/reports/724253) | ibb | Tcpdump before 4.9.3 has a buffer over-read in print-dccp.c:dccp_print_option() (CVE-2018-16229) | - |
| [MEM-781325](https://hackerone.com/reports/781325) | ibb | Out-of-bounds Read in php_strip_tags_ex | - |
| [MEM-802846](https://hackerone.com/reports/802846) | ibb | The VTP parser in tcpdump before 4.9.2 has a buffer over-read in print-vtp.c:vtp_print() | - |
| [MEM-802863](https://hackerone.com/reports/802863) | ibb | CVE-2017-13050: The RPKI-Router parser in tcpdump before 4.9.2 has a buffer over-read in print-rpki-rtr.c:rpki_rtr_pdu_print() | - |
| [MEM-802896](https://hackerone.com/reports/802896) | ibb | CVE-2017-13019:  The PGM parser in tcpdump before 4.9.2 has a buffer over-read in print-pgm.c:pgm_print() | - |
| [MEM-824163](https://hackerone.com/reports/824163) | ibb | Squid leaks previous content from reusable buffer | - |
| [MEM-852103](https://hackerone.com/reports/852103) | ibb | Out-of-Bound Read in urldecode() [CVE-2020-7067] | - |
| [MEM-1073363](https://hackerone.com/reports/1073363) | kubernetes | Index Out Of Bounds in protobuf unmarshalling | - |
| [MEM-1209681](https://hackerone.com/reports/1209681) | nodejs | OOB read in libuv | - |
| [MEM-1595296](https://hackerone.com/reports/1595296) | ibb | Read beyond bounds in mod_isapi.c [zhbug_httpd_41] | - |
| [MEM-2621062](https://hackerone.com/reports/2621062) | ibb | curl: stack-buffer overread during punycode conversions | - |

## 2. The valve entity-index pattern (MEM-807772, $7,500)

The module's citation row — an OOB read that becomes remote code execution because the reader feeds an unchecked index into a virtual call:

> In Source engine games there are many network messages sent from the server to the client that take an entity index. There is a common pattern among many of these messages for the lower bounds of the entity index to be checked but not the upper bounds. In many cases these out of bound reads get an entity pointer from that index then call a virtual function on it.

> I will be discussing the `GlowPropTurnOff` message specifically for the remainder of this report, however this OOB read pattern exists in other messages too. I have successfully tested this on a couple of other CS:GO user messages, and while I haven't tested it I also suspect that this bug pattern exists in the network messages of other Source games as well.

This is the vault's only overread priced like a write. The mechanism is invariant: *lower bound checked, upper bound trusted* — grep the handler table for `>= 0` without a `< max` clause and you have the class. The second half of the quote is the report form worth copying: name one fully-analyzed instance, claim the pattern, scope the tested set.

## 3. Universally deployed parsers: NGINX mp4 and the Python AST builder

Two reads in software everyone runs. MEM-2658447 (**$2,142**) — NGINX's mp4 module reading past its worker:

> NGINX Open Source and NGINX Plus have a vulnerability in the ngx_http_mp4_module, which might allow an attacker to over-read NGINX worker memory resulting in its termination, using a specially crafted mp4 file. The issue only affects NGINX if it is built with the ngx_http_mp4_module and the mp4 directive is used in the configuration file. Additionally, the attack is possible only if an attacker can trigger the processing of a specially crafted mp4 file with the ngx_http_mp4_module.

Deployment conditions (module built, directive used, attacker-triggerable file) are stated as *preconditions*, not buried — the report form that lands a $2,142 on a DoS-class reader. MEM-746766 (**$2,000**) is the same genre at Python: two AST-builder reads, two CVEs (CVE-2019-19274/19275), with the honest reach bound quoted verbatim:

> A service that takes Python snippets as payload, but doesn't necessarily execute them, could possibly be caused to crash, leading to a denial of service. Examples of such services include online playgrounds for static analysis tools, syntax highlighting & formatting services, etc.

Tooling surfaces as victims — the deployment pattern modern language programs should read.

## 4. The PHP exif/GD fleet: gdb transcript as proof

Fourteen GD/exif/image rows (110720 $500, 135291 $500, 141202 $500, 665330 $1,500, 675578 $1,500, 675580 $1,500, …). The house format is a gdb breakpoint transcript, not a PoC crash:

> Invalid memory access while applying bicubic scaling on images.

MEM-141202's body then pastes the breakpoint list (`gd_interpolation.c:890`, `_gdContributionsAlloc (line_length=13, windows_size=9)`) — the researcher showing *where the scaling loop's arithmetic leaves the array*, with ASan/gdb as the witness. The two $1,500 exif rows (675578/675580) carry the same fleet's high tier. Note the thematic overlap with module 05: MEM-593229's iconv overread is explicitly *caused by* an integer overflow — the class boundary paper is inside the bodies, not the classifiers.

## 5. The tcpdump packet-printer fleet (the $0 wall)

Twenty-plus tcpdump rows (831353 $500 the sole paid member; 268803–268808, 964582/964583 $500, 802846/802863/802896, 724243/724253, 202960-series in module 01 — all `-`). Printf-style protocol dissectors served as the packet-printer overread testbed of the 2017 era. Doctrinal reading: the fleet shows the floor of the class — a correctly-assigned CVE in a *packet printer* (a tool that displays pcaps, not a server) moved nothing beyond bookkeeping. The one paid row (831353, $500) is the exception that sets the ceiling for "dissector crash" reports.

## 6. What pays / what doesn't

- **Pays**: valve OOB→vtable call ($7,500); NGINX worker overread ($2,142); Python AST reads with CVEs ($2,000); PHP GD/exif reads at $500–$1,500 (image-parsing fleet); mruby invalid reads ($800–$1,000).
- **Doesn't pay**: tcpdump dissectors (CVE-only packet printers); MEM-824163's Squid reusable-buffer leak (information-class, no figure); MEM-1073363 (protobuf OOB, k8s, no figure); MEM-852103 (urldecode CVE, no figure). Pattern: unpaid = read disclosed without a *consumer* that pays for the primitive's consequences — dissectors, mirrors, and libraries with no executable call chain.
- **MEM-478368** ($1,500) is the boundary row — titled "Out Of Bounds Write" and classed here, because the report itself counts the write path *in bytes* (1,200-byte overrun of `imagecolormatch`'s buffer) and the write is a function argument evaluation, not a memory smash. See §4 for the overrun accounting.

## 7. Cross-references

- **Heap module** — the php_* family splits the same functions across both modules (read → here, write → there); the split is by impact verb, not by function.
- **Integer-Overflow module** — MEM-593229 (§4) is *filed* as this module's boundary case: integer overflow in, OOB read out. The playbook P2 probe ladder treats the two as one sweep.
- **Null-Deref module** — MEM-456727 (`null pointer dereference in imap_mail`, `-`) is the classifier's judgment call; an unchecked-null read is frozen there.
- **RCE vault module 04** — the exif/phar overread fleet's executable cousins.
