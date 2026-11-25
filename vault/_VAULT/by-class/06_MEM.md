---
title: "Vault class MEM — Memory Corruption"
type: dataset-view
class: "Memory Corruption"
vault_category: "30_Memory-Corruption/"
rows: 917
paid_rows: 286
bounty_sum: 472,258
full_bodies_available: 806
source: "public HackerOne vault (hackerone disclosed), harvested 2026-11-17"
---

# MEM — Memory Corruption

917 rows · 286 with a bounty figure · **$472,258** total · 806 with full write-up stored.
Playbook: `Vault/30_Memory-Corruption/` · Dataset: `Vault/_VAULT/reports.sqlite` (`SELECT * FROM reports WHERE ...`).

| Report | Program | Severity | Bounty | Votes | Disclosed | Weakness | Title |
|---|---|---|---|---|---|---|---|
| [2177925](https://hackerone.com/reports/2177925) | PlayStation | high | $12,500 | 197 | 2024-04-25 | Classic Buffer Overflow | Remote vulnerabilities in spp |
| [826026](https://hackerone.com/reports/826026) | PlayStation | high | $10,000 | 741 | 2020-07-06 | Use After Free | Use-After-Free In IPV6_2292PKTOPTIONS leading To Arbitrary Kernel R/W Primitives |
| [943231](https://hackerone.com/reports/943231) | PlayStation | high | $10,000 | 298 | 2021-01-12 | Double Free | SOCK_RAW sockets reachable from Webkit process allows triggering double free in IP6_EXTHDR_CHECK |
| [1340942](https://hackerone.com/reports/1340942) | PlayStation | high | $10,000 | 280 | 2022-09-21 | Incorrect Calculation of Buffer Size | size_t-to-int vulnerability in exFAT leads to memory corruption via malformed USB flash drives |
| [542180](https://hackerone.com/reports/542180) | Valve | critical | $10,000 | 268 | 2020-03-25 | Classic Buffer Overflow | Malformed NAV file leads to buffer overflow and code execution in Left4Dead2.exe |
| [2900606](https://hackerone.com/reports/2900606) | PlayStation | high | $10,000 | 236 | 2025-04-18 | Use After Free | sys_fsc2h_ctrl kernel stack free |
| [3320669](https://hackerone.com/reports/3320669) | PlayStation | high | $10,000 | 228 | 2026-05-01 | Double Free | Double fdrop on a socket through sys_netcontrol |
| [1441103](https://hackerone.com/reports/1441103) | PlayStation | high | $10,000 | 143 | 2022-09-20 | Use After Free | Use-after-free in setsockopt IPV6_2292PKTOPTIONS (CVE-2020-7457) |
| [186723](https://hackerone.com/reports/186723) | shopify-scripts | high | $10,000 | 20 | 2017-03-01 | Memory Corruption - Generic | Crash: Overwriting NoMethodError with a builtin class crashes/corrupts memory |
| [189633](https://hackerone.com/reports/189633) | shopify-scripts | high | $10,000 | 12 | 2017-03-14 | Memory Corruption - Generic | Certain inputs cause tight C-level recursion leading to process stack overflow |
| [584603](https://hackerone.com/reports/584603) | Valve | critical | $9,000 | 209 | 2021-05-27 | Out-of-bounds Read | RCE on CS:GO client using unsanitized entity ID in EntityMsg message |
| [1707287](https://hackerone.com/reports/1707287) | Internet Bug Bounty | critical | $8,000 | 89 | 2025-01-18 | Use of Externally-Controlled Format String | CVE-2022-40604: Apache Airflow: Format String Vulnerability |
| [184857](https://hackerone.com/reports/184857) | shopify-scripts | high | $8,000 | 4 | 2016-12-16 | Memory Corruption - Generic | Crash: calling Proc::initialize_copy with a Proc instance where initialize never ran leads to a crash |
| [185794](https://hackerone.com/reports/185794) | shopify-scripts | high | $8,000 | 4 | 2016-12-16 | Memory Corruption - Generic | Crash: mrb_any_to_s can't handle NilClass, Symbol and Fixnum |
| [184661](https://hackerone.com/reports/184661) | shopify-scripts | high | $8,000 | 3 | 2016-12-16 | Memory Corruption - Generic | mruby-time: Crash host with uninitialized Time obj |
| [807772](https://hackerone.com/reports/807772) | Valve | critical | $7,500 | 219 | 2021-05-04 | Out-of-bounds Read | OOB reads in network message handlers leads to RCE |
| [1180252](https://hackerone.com/reports/1180252) | Valve | critical | $7,500 | 196 | 2021-09-13 | Classic Buffer Overflow | Buffer overrun in Steam SILK voice decoder |
| [463286](https://hackerone.com/reports/463286) | Valve | critical | $7,500 | 109 | 2021-05-05 | Classic Buffer Overflow | Specially Crafted Closed Captions File can lead to Remote Code Execution in CS:GO and other Source Games |
| [1070835](https://hackerone.com/reports/1070835) | Valve | critical | $7,500 | 66 | 2021-05-17 | Out-of-bounds Read | CS:GO Server -> Client RCE through OOB access in CSVCMsg_SplitScreen + Info leak in HTTP download |
| [876719](https://hackerone.com/reports/876719) | Valve | critical | $7,500 | 35 | 2021-05-27 | Array Index Underflow | Signedness issue in ClassInfo message handler leads to RCE on CS:GO client |
| [12497](https://hackerone.com/reports/12497) | Internet Bug Bounty |  | $7,500 | 4 | 2014-10-07 | Memory Corruption - Generic | Adobe Flash Player FileReference Use-after-Free Vulnerability |
| [733267](https://hackerone.com/reports/733267) | Valve | critical | $5,000 | 173 | 2021-05-10 | Classic Buffer Overflow | [Portal 2] Remote Code Execution via voice packets |
| [537550](https://hackerone.com/reports/537550) | Open-Xchange |  | $5,000 | 46 |  | Memory Corruption - Generic | Memory corruption in imap-parser.c |
| [56385](https://hackerone.com/reports/56385) | Internet Bug Bounty |  | $5,000 | 35 | 2019-10-18 | Memory Corruption - Generic | Double free vulnerability in Flash Player Settings Manager (CVE-2015-0346) |
| [960244](https://hackerone.com/reports/960244) | GitLab | high | $5,000 | 16 | 2020-11-02 | Type Confusion | Insufficient Type Check leading to Developer ability to delete Project, Repository, Group, ... |
| [151043](https://hackerone.com/reports/151043) | Internet Bug Bounty |  | $5,000 | 4 | 2019-11-12 | Memory Corruption - Generic | Adobe Flash Player PSDK Class Use After Free Vulnerability |
| [31408](https://hackerone.com/reports/31408) | Internet Bug Bounty |  | $5,000 | 2 | 2015-03-11 | Memory Corruption - Generic | Adobe Flash Player Out-of-Bound Read/Write Vulnerability |
| [119652](https://hackerone.com/reports/119652) | Internet Bug Bounty |  | $5,000 | 1 | 2019-11-12 | Memory Corruption - Generic | Adobe Flash Player ASnative(101,10) Memory Corruption Vulnerability |
| [139879](https://hackerone.com/reports/139879) | Internet Bug Bounty |  | $5,000 | 1 | 2019-11-12 | Memory Corruption - Generic | Adobe Flash Player Regular Expression UAF Remote Code Execution Vulnerability |
| [151039](https://hackerone.com/reports/151039) | Internet Bug Bounty |  | $5,000 | 1 | 2019-11-12 | Memory Corruption - Generic | Adobe Flash Player TimedEvent.parent Memory Corruption Vulnerability |
| [2585375](https://hackerone.com/reports/2585375) | Internet Bug Bounty | high | $4,920 | 27 | 2024-07-13 | NULL Pointer Dereference | important: Apache HTTP Server: Crash resulting in Denial of Service in mod_proxy via a malicious request (CVE-2024-38477) |
| [2018680](https://hackerone.com/reports/2018680) | GitHub Security Lab |  | $4,500 | 0 |  | Memory Corruption - Generic | cpp: if (a+b>c) a=c-b is incorrect if a+b overflows |
| [1549636](https://hackerone.com/reports/1549636) | Internet Bug Bounty | high | $4,000 | 26 | 2022-05-28 | Double Free | CVE-2022-28738: Double free in Regexp compilation |
| [630462](https://hackerone.com/reports/630462) | PuTTY (European Commission - DIGIT) | high | $3,646 | 309 | 2019-09-20 | Heap Overflow | Heap overflow happen when receiving short length key from ssh server using ssh protocol 1 |
| [255510](https://hackerone.com/reports/255510) | Mail.ru |  | $3,500 | 23 |  | Buffer Over-read | При передаче в ID сообщения нулевого байта, происходит вывод какого-то буфера. |
| [513154](https://hackerone.com/reports/513154) | Valve | critical | $3,000 | 229 | 2019-09-17 | Array Index Underflow | Unchecked weapon id in WeaponList message parser on client leads to RCE |
| [484745](https://hackerone.com/reports/484745) | Valve | critical | $3,000 | 26 | 2021-05-04 | Stack Overflow | GoldSrc: Buffer Overflow in DELTA_ParseDelta function leads to RCE |
| [489102](https://hackerone.com/reports/489102) | VLC (European Commission - DIGIT) | high | $2,817 | 62 | 2020-02-10 | Stack Overflow | VLC 4.0.0 - Stack Buffer Overflow (SEH) |
| [2526051](https://hackerone.com/reports/2526051) | Internet Bug Bounty | medium | $2,600 | 32 | 2024-07-01 | Stack Overflow | CVE-2024-31079 in nginx |
| [2526041](https://hackerone.com/reports/2526041) | Internet Bug Bounty | medium | $2,600 | 21 | 2024-07-01 | NULL Pointer Dereference | CVE-2024-35200 in nginx |
| [550625](https://hackerone.com/reports/550625) | Valve | high | $2,500 | 48 | 2021-05-06 | Stack Overflow | [CS:GO] Unchecked texture file name with TEXTUREFLAGS_DEPTHRENDERTARGET can lead to Remote Code Execution |
| [363195](https://hackerone.com/reports/363195) | Block.one |  | $2,500 | 25 |  | Heap Overflow | [FG-VD-18-100] Heap Buffer Overflow Vulnerability in EOS's forked repository of Binaryen Library and also in latest Binaryen Library Parent Repository |
| [1546935](https://hackerone.com/reports/1546935) | SKALE Network | medium | $2,500 | 23 | 2022-07-07 | Classic Buffer Overflow | Stack Buffer Overflow via `gmp_sprintf`in `BLSSignature` and `BLSSigShare` |
| [363209](https://hackerone.com/reports/363209) | Block.one |  | $2,500 | 13 |  | Classic Buffer Overflow | [FG-VD-18-101] Buffer Overflow Vulnerability in EOS's WAVM Library and also in latest WAVM Library Parent Repository |
| [35102](https://hackerone.com/reports/35102) | Internet Bug Bounty |  | $2,500 | 1 | 2014-06-27 | Memory Corruption - Generic | Locale::parseLocale Double Free |
| [2658447](https://hackerone.com/reports/2658447) | Internet Bug Bounty | medium | $2,142 | 43 | 2024-08-27 | Buffer Over-read | CVE-2024-7347: Buffer overread in the ngx_http_mp4_module |
| [2806356](https://hackerone.com/reports/2806356) | Cosmos |  | $2,000 | 34 | 2024-11-19 | Buffer Over-read | Heap-Buffer-Overread in contains_whitespace when calling parser_validate after supplying a maliciously crafted buffer to parser_parse |
| [746766](https://hackerone.com/reports/746766) | Internet Bug Bounty | medium | $2,000 | 15 | 2021-08-25 | Buffer Over-read | Two out-of-bounds array reads in Python AST builder (Re-opening 520612 with CVEs) |
| [1352429](https://hackerone.com/reports/1352429) | Internet Bug Bounty | high | $2,000 | 15 | 2021-09-27 | Classic Buffer Overflow | CVE-2021-3711: SM2 decrypt  buffer overflow |
| [119657](https://hackerone.com/reports/119657) | Internet Bug Bounty |  | $2,000 | 5 | 2019-11-12 | Memory Corruption - Generic | Adobe Flash Player Race Condition Vulnerability |
| [201897](https://hackerone.com/reports/201897) | shopify-scripts | low | $2,000 | 4 | 2017-02-28 | Memory Corruption - Generic | Recursion causing uninitialized memory reads leading to a segfault |
| [30567](https://hackerone.com/reports/30567) | Internet Bug Bounty |  | $2,000 | 3 | 2015-03-11 | Memory Corruption - Generic | Adobe Flash Player MP4 Use-After-Free Vulnerability |
| [36279](https://hackerone.com/reports/36279) | Internet Bug Bounty |  | $2,000 | 2 | 2015-03-11 | Memory Corruption - Generic | Adobe Flash Player MP4 Use-After-Free Vulnerability |
| [47012](https://hackerone.com/reports/47012) | Internet Bug Bounty |  | $2,000 | 2 | 2015-03-25 | Memory Corruption - Generic | Adobe Flash Player Out-of-Bound Access Vulnerability |
| [138516](https://hackerone.com/reports/138516) | Internet Bug Bounty |  | $2,000 | 2 | 2019-11-12 | Memory Corruption - Generic | Adobe Flash Player ContentFactory class Memory Corruption Vulnerability |
| [138517](https://hackerone.com/reports/138517) | Internet Bug Bounty |  | $2,000 | 2 | 2019-11-12 | Memory Corruption - Generic | Adobe Flash Player Metadata class Memory Corruption Vulnerability |
| [138518](https://hackerone.com/reports/138518) | Internet Bug Bounty |  | $2,000 | 2 | 2019-11-12 | Memory Corruption - Generic | Adobe Flash Player OpportunityGenerator class Memory Corruption Vulnerability |
| [145265](https://hackerone.com/reports/145265) | Internet Bug Bounty |  | $2,000 | 2 | 2019-11-12 | Memory Corruption - Generic | Adobe Flash Player ShimContentFactory class Memory Corruption Vulnerability |
| [145266](https://hackerone.com/reports/145266) | Internet Bug Bounty |  | $2,000 | 2 | 2019-11-12 | Memory Corruption - Generic | Adobe Flash Player ShimContentFactory.retrieveResolvers Memory Corruption Vulnerability |
| [145267](https://hackerone.com/reports/145267) | Internet Bug Bounty |  | $2,000 | 2 | 2019-11-12 | Memory Corruption - Generic | Adobe Flash Player ShimContentResolver.configure Memory Corruption Vulnerability |
| [145271](https://hackerone.com/reports/145271) | Internet Bug Bounty |  | $2,000 | 2 | 2019-11-12 | Memory Corruption - Generic | Adobe Flash Player ShimContentResolver(resolverType=0) class Memory Corruption Vulnerability |
| [145272](https://hackerone.com/reports/145272) | Internet Bug Bounty |  | $2,000 | 2 | 2019-11-12 | Memory Corruption - Generic | Adobe Flash Player ShimContentResolver(resolverType=1) class Memory Corruption Vulnerability |
| [151040](https://hackerone.com/reports/151040) | Internet Bug Bounty |  | $2,000 | 2 | 2019-11-12 | Memory Corruption - Generic | Adobe Flash Player ShimAdPolicySelector(adPolicySelectorType=0) class Memory Corruption |
| [119653](https://hackerone.com/reports/119653) | Internet Bug Bounty |  | $2,000 | 1 | 2019-11-12 | Memory Corruption - Generic | Adobe Flash Player ASnative(900,1).call(MovieClip) Use-After-Free Vulnerability |
| [119655](https://hackerone.com/reports/119655) | Internet Bug Bounty |  | $2,000 | 1 | 2019-11-12 | Memory Corruption - Generic | Adobe Flash Player ASnative(900,1).call(TextField) Use-After-Free Vulnerability |
| [122254](https://hackerone.com/reports/122254) | Internet Bug Bounty |  | $2,000 | 1 | 2019-11-12 | Memory Corruption - Generic | Adobe Flash Player TextField Use-After-Free Vulnerability |
| [145269](https://hackerone.com/reports/145269) | Internet Bug Bounty |  | $2,000 | 1 | 2019-11-12 | Memory Corruption - Generic | Adobe Flash Player ShimOpportunityGenerator class Memory Corruption Vulnerability |
| [1219491](https://hackerone.com/reports/1219491) | GitHub Security Lab |  | $1,800 | 6 |  | Memory Corruption - Generic | ihsinme:CPP Add query for CWE-415 Double Free |
| [974370](https://hackerone.com/reports/974370) | GitHub Security Lab |  | $1,800 | 1 |  | Memory Corruption - Generic | [CATENACYBER]: [CPP] CWE-476 Null Pointer Dereference : Another query to either missing or redundant NULL check |
| [402566](https://hackerone.com/reports/402566) | Valve | high | $1,500 | 163 | 2020-09-22 | Classic Buffer Overflow | [Half-Life 1] Malformed map name leads to memory corruption and code execution |
| [827729](https://hackerone.com/reports/827729) | Open-Xchange |  | $1,500 | 105 |  | NULL Pointer Dereference | Null pointer dereference in SMTP server function smtp_string_parse |
| [483572](https://hackerone.com/reports/483572) | Intel Corporation |  | $1,500 | 77 |  | Memory Corruption - Generic | [FG-VD-19-009] Intel(R) Trace Analyzer and Collector 2019 Memory Corruption Vulnerability Notification |
| [520717](https://hackerone.com/reports/520717) | Lob |  | $1,500 | 68 |  | Use After Free | Old WebKit HTML agent in Template Preview function has multiple known vulnerabilities leading to RCE |
| [593229](https://hackerone.com/reports/593229) | Internet Bug Bounty | high | $1,500 | 58 | 2020-10-12 | Buffer Over-read | Out-of-bounds read in iconv.c:_php_iconv_mime_decode() due to integer overflow |
| [1084342](https://hackerone.com/reports/1084342) | Internet Bug Bounty | high | $1,500 | 51 | 2021-08-25 | Classic Buffer Overflow | Buffer overflow in PyCArg_repr in _ctypes/callproc.c for Python 3.x to 3.9.1 |
| [722327](https://hackerone.com/reports/722327) | Internet Bug Bounty | critical | $1,500 | 42 | 2020-11-09 | Buffer Underflow | CVE-2019-11043: a buffer underflow in fpm_main.c can lead to RCE in php-fpm |
| [237915](https://hackerone.com/reports/237915) | Internet Bug Bounty | critical | $1,500 | 35 | 2019-10-14 | Heap Overflow | PHP mbstring / Oniguruma multiple remote heap/stack corruptions |
| [675578](https://hackerone.com/reports/675578) | Internet Bug Bounty | high | $1,500 | 20 | 2020-11-09 | Out-of-bounds Read | Out of Bounds Memory Read in exif_scan_thumbnail |
| [172562](https://hackerone.com/reports/172562) | Internet Bug Bounty | critical | $1,500 | 16 | 2016-12-05 | Memory Corruption - Generic | LZMADecompressor.decompress Use After Free |
| [478367](https://hackerone.com/reports/478367) | Internet Bug Bounty | critical | $1,500 | 16 | 2020-10-10 | Use After Free | efree() on uninitialized Heap data in imagescale leads to use-after-free |
| [477896](https://hackerone.com/reports/477896) | Internet Bug Bounty | critical | $1,500 | 8 | 2020-11-09 | Use After Free | Use after free and out of bounds read in xmlrpc_decode() |
| [665330](https://hackerone.com/reports/665330) | Internet Bug Bounty | critical | $1,500 | 8 | 2020-11-09 | Buffer Over-read | Out of Bounds Memory Read in php_jpg_get16 |
| [272497](https://hackerone.com/reports/272497) | Internet Bug Bounty | high | $1,500 | 4 | 2019-11-12 | Stack Overflow | Perl $ENV Key Stack Buffer Overflow |
| [478368](https://hackerone.com/reports/478368) | Internet Bug Bounty | high | $1,500 | 4 | 2020-10-10 | Memory Corruption - Generic | imagecolormatch Out Of Bounds Write on Heap |
| [135152](https://hackerone.com/reports/135152) | Internet Bug Bounty |  | $1,500 | 3 | 2016-05-05 | Memory Corruption - Generic | Integer overflow in ZipArchive::getFrom* |
| [476168](https://hackerone.com/reports/476168) | Internet Bug Bounty | critical | $1,500 | 3 | 2020-11-09 | Heap Overflow | Heap overflow in utf32be_mbc_to_code |
| [675580](https://hackerone.com/reports/675580) | Internet Bug Bounty | high | $1,500 | 3 | 2020-11-09 | Out-of-bounds Read | Out of Bounds Memory Read in exif_process_user_comment |
| [476178](https://hackerone.com/reports/476178) | Internet Bug Bounty | critical | $1,500 | 2 | 2020-11-09 | Buffer Underflow | Negative size parameter in mb_split |
| [476179](https://hackerone.com/reports/476179) | Internet Bug Bounty | high | $1,500 | 2 | 2020-11-09 | Heap Overflow | Buffer over-write in finfo_open with malformed magic file. |
| [504761](https://hackerone.com/reports/504761) | Internet Bug Bounty | high | $1,500 | 2 | 2020-11-09 | Classic Buffer Overflow | phar_tar_writeheaders_int() buffer overflow |
| [73239](https://hackerone.com/reports/73239) | Internet Bug Bounty |  | $1,500 | 1 | 2015-03-18 | Memory Corruption - Generic | ZIP Integer Overflow leads to writing past heap boundary |
| [73256](https://hackerone.com/reports/73256) | Internet Bug Bounty |  | $1,500 | 1 | 2015-05-18 | Memory Corruption - Generic | PHP yaml_parse/yaml_parse_file/yaml_parse_url Double Free |
| [152772](https://hackerone.com/reports/152772) | Internet Bug Bounty |  | $1,500 | 1 | 2019-11-12 | Memory Corruption - Generic | Inadequate error handling in bzread() |
| [175587](https://hackerone.com/reports/175587) | Internet Bug Bounty | high | $1,500 | 1 | 2019-11-12 | Memory Corruption - Generic | Stack Buffer Overflow in GD dynamicGetbuf |
| [188102](https://hackerone.com/reports/188102) | Internet Bug Bounty |  | $1,500 | 1 | 2019-11-12 | Memory Corruption - Generic | 3 heap corruptions in PHP |
| [546644](https://hackerone.com/reports/546644) | Open-Xchange |  | $1,200 | 26 |  | Use After Free | Two heap use-after-free errors in IMAP operations |
| [503208](https://hackerone.com/reports/503208) | VLC (European Commission - DIGIT) | medium | $1,135 | 77 | 2019-07-24 | Double Free | Access Violation Reading EXPLOITABLE_0228 |
| [484398](https://hackerone.com/reports/484398) | VLC (European Commission - DIGIT) | medium | $1,127 | 25 | 2019-06-12 | Classic Buffer Overflow | Buffer overflow in libavi_plugin memmove() call |
| [502816](https://hackerone.com/reports/502816) | VLC (European Commission - DIGIT) | medium | $1,121 | 106 | 2019-07-24 | Integer Underflow | Access Violation Reading in libfaad_plugin |
| [352869](https://hackerone.com/reports/352869) | Grab | medium | $1,000 | 142 | 2021-02-24 | Array Index Underflow | Subdomain Takeover Via Insecure CloudFront Distribution cdn.grab.com |
| [116773](https://hackerone.com/reports/116773) | Internet Bug Bounty |  | $1,000 | 64 | 2019-10-15 | Memory Corruption - Generic | Type Confusion Vulnerability - SOAP / make_http_soap_request() |
| [504951](https://hackerone.com/reports/504951) | Valve | high | $1,000 | 62 | 2019-09-17 | Stack Overflow | Malformed playlist.txt in GoldSrc games leads to Access Violation & arbitrary code execution |
| [424447](https://hackerone.com/reports/424447) | Internet Bug Bounty | critical | $1,000 | 52 | 2019-09-25 | Integer Overflow | Integer overflow leading to buffer overflow |
| [535827](https://hackerone.com/reports/535827) | shopify-scripts |  | $1,000 | 33 | 2019-09-04 | Classic Buffer Overflow | Buffer overflow in yywarning_s |
| [317557](https://hackerone.com/reports/317557) | Mail.ru |  | $1,000 | 31 |  | Write-what-where Condition | Race condition на market.games.mail.ru |
| [161189](https://hackerone.com/reports/161189) | Internet Bug Bounty |  | $1,000 | 23 | 2019-10-31 | Memory Corruption - Generic | select_colors write out-of-bounds |
| [175091](https://hackerone.com/reports/175091) | Internet Bug Bounty | medium | $1,000 | 14 | 2016-12-05 | Memory Corruption - Generic | chain.__setstate__ Type Confusion |
| [354650](https://hackerone.com/reports/354650) | Internet Bug Bounty | medium | $1,000 | 14 | 2018-10-31 | Buffer Underflow | [CVE-2018-6913] heap-buffer-overflow in S_pack_rec |
| [621308](https://hackerone.com/reports/621308) | shopify-scripts |  | $1,000 | 9 | 2019-09-04 | NULL Pointer Dereference | NULL pointer dereference in `mrb_check_frozen` |
| [184715](https://hackerone.com/reports/184715) | shopify-scripts |  | $1,000 | 8 | 2016-12-18 | Memory Corruption - Generic | Read after free in mrb_vm_exec with OP_ARYCAT reading R(B) |
| [192896](https://hackerone.com/reports/192896) | shopify-scripts | low | $1,000 | 7 | 2017-01-31 | Memory Corruption - Generic | Memory disclosure in timegm |
| [633607](https://hackerone.com/reports/633607) | shopify-scripts |  | $1,000 | 7 | 2019-09-04 | Out-of-bounds Read | Invalid read in `str_replace_partial` |
| [1738939](https://hackerone.com/reports/1738939) | GitHub Security Lab |  | $1,000 | 7 |  | Memory Corruption - Generic | [CPP]: Add query for CWE-125 Out-of-bounds Read with different interpretation of the string when use mbtowc |
| [109843](https://hackerone.com/reports/109843) | Internet Bug Bounty |  | $1,000 | 3 | 2019-10-15 | Memory Corruption - Generic | Uninitialized pointer in phar_make_dirstream() |
| [110352](https://hackerone.com/reports/110352) | Internet Bug Bounty |  | $1,000 | 3 | 2016-03-31 | Memory Corruption - Generic | Perl 5.22 VDir::MapPathA/W Out-of-bounds Reads and Buffer Over-reads |
| [110417](https://hackerone.com/reports/110417) | Internet Bug Bounty |  | $1,000 | 3 | 2019-10-15 | Memory Corruption - Generic | Heap corruption in tar/zip/phar parser |
| [170138](https://hackerone.com/reports/170138) | Internet Bug Bounty |  | $1,000 | 3 | 2019-10-13 | Memory Corruption - Generic | SEH buffer overflow msgfmt_format_message |
| [185957](https://hackerone.com/reports/185957) | shopify-scripts | low | $1,000 | 3 | 2016-12-16 | Memory Corruption - Generic | Crash: A call to Symbol.new leads to a crash when inspecting the resulting object |
| [20616](https://hackerone.com/reports/20616) | Mail.ru |  | $1,000 | 2 |  | Memory Corruption - Generic | e.mail.ru: File upload "Chapito" circus |
| [161193](https://hackerone.com/reports/161193) | Internet Bug Bounty |  | $1,000 | 2 | 2019-10-13 | Memory Corruption - Generic | imagegammacorrect allows arbitrary write access |
| [127242](https://hackerone.com/reports/127242) | Internet Bug Bounty |  | $1,000 | 1 | 2019-10-13 | Memory Corruption - Generic | Negative size parameter (-1) in memcpy mbfl_strcut |
| [146202](https://hackerone.com/reports/146202) | Internet Bug Bounty |  | $1,000 | 1 | 2019-11-12 | Memory Corruption - Generic | Invalid free in phar_extract_file() |
| [104014](https://hackerone.com/reports/104014) | Internet Bug Bounty |  | $1,000 | 0 | 2015-11-05 | Memory Corruption - Generic | libcurl duphandle read out of bounds |
| [109175](https://hackerone.com/reports/109175) | Internet Bug Bounty |  | $1,000 | 0 | 2016-01-20 | Memory Corruption - Generic | Use After Free in sortWithSortKeys() |
| [420115](https://hackerone.com/reports/420115) | shopify-scripts |  | $800 | 37 | 2019-09-04 | NULL Pointer Dereference | Crash in mrb_ary_push |
| [204421](https://hackerone.com/reports/204421) | shopify-scripts |  | $800 | 12 | 2017-02-28 | Memory Corruption - Generic | Heap buffer oveflow with many arguments |
| [193143](https://hackerone.com/reports/193143) | shopify-scripts |  | $800 | 7 | 2017-01-31 | Memory Corruption - Generic | Use After Free in str_replace |
| [214681](https://hackerone.com/reports/214681) | shopify-scripts | low | $800 | 7 | 2017-04-15 | NULL Pointer Dereference | Null pointer dereference in ary_concat |
| [295380](https://hackerone.com/reports/295380) | shopify-scripts | none | $800 | 6 | 2018-01-17 | Heap Overflow | heap-buffer-overflow in OP_R_BREAK |
| [194906](https://hackerone.com/reports/194906) | shopify-scripts |  | $800 | 5 | 2017-02-07 | Memory Corruption - Generic | Heap overflow due to off-by-one when expanding stack |
| [295680](https://hackerone.com/reports/295680) | shopify-scripts | low | $800 | 5 | 2017-12-28 | Out-of-bounds Read | Invalid read leading to a segfault |
| [296198](https://hackerone.com/reports/296198) | shopify-scripts |  | $800 | 5 | 2018-01-17 | Memory Corruption - Generic | SEGV on ary_concat |
| [192362](https://hackerone.com/reports/192362) | shopify-scripts | low | $800 | 4 | 2017-01-12 | Memory Corruption - Generic | Heap Overflow in mrb_arb_splice |
| [295276](https://hackerone.com/reports/295276) | shopify-scripts |  | $800 | 4 | 2018-01-17 | Use After Free | heap-use-after-free in OP_RESCUE |
| [215891](https://hackerone.com/reports/215891) | shopify-scripts | low | $800 | 3 | 2017-04-15 | NULL Pointer Dereference | Null pointer dereference in mrb_class |
| [217610](https://hackerone.com/reports/217610) | shopify-scripts | medium | $800 | 3 | 2017-04-13 | Memory Corruption - Generic | kh_put_iv SEGFAULT - mruby 1.2.0 |
| [218233](https://hackerone.com/reports/218233) | shopify-scripts | low | $800 | 3 | 2017-04-15 | NULL Pointer Dereference | Null pointer dereference in OP_ENTER |
| [221712](https://hackerone.com/reports/221712) | shopify-scripts |  | $800 | 3 | 2017-05-07 | Memory Corruption - Generic | Null pointer dereferences in kh_copy_mt |
| [222294](https://hackerone.com/reports/222294) | shopify-scripts | medium | $800 | 3 | 2017-05-21 | Memory Corruption - Generic | heap-use-after-free in mrb_vm_exec - vm.c:1247 |
| [218567](https://hackerone.com/reports/218567) | shopify-scripts | medium | $800 | 2 | 2017-04-13 | Memory Corruption - Generic | SIGSEGV in array_copy - array.c:71 |
| [242354](https://hackerone.com/reports/242354) | shopify-scripts |  | $800 | 2 | 2017-06-23 | NULL Pointer Dereference | Null pointer dereference with send/method_missing |
| [244904](https://hackerone.com/reports/244904) | shopify-scripts |  | $800 | 1 | 2017-07-06 | Use After Free | Use after free in mruby-mpdecimal |
| [667242](https://hackerone.com/reports/667242) | Valve | medium | $750 | 80 | 2020-09-22 | Write-what-where Condition | [steam client] Opening a specific steam:// url overwrites files at an arbitrary location |
| [675710](https://hackerone.com/reports/675710) | Valve | critical | $750 | 11 | 2021-05-04 | Stack Overflow | [GoldSrc] Remote Code Execution using malicious WAD list in BSP file |
| [891846](https://hackerone.com/reports/891846) | Internet Bug Bounty | high | $750 | 3 | 2021-08-22 | Buffer Over-read | CVE-2020-9383 Floppy OOB read |
| [866597](https://hackerone.com/reports/866597) | Open-Xchange |  | $550 | 5 |  | Buffer Over-read | Pre-auth buffer over-read in Dovecot NTLM implementation |
| [996041](https://hackerone.com/reports/996041) | Reddit | medium | $500 | 65 | 2021-10-27 | Type Confusion | Image queue default key of 'None' and GraphQL unhandled type exception |
| [827051](https://hackerone.com/reports/827051) | Open-Xchange |  | $500 | 30 |  | Use After Free | Use after free in smtp_server_connection_handle_command |
| [1032086](https://hackerone.com/reports/1032086) | Kubernetes | medium | $500 | 15 | 2020-12-03 | NULL Pointer Dereference | csi-snapshot-controller crashes when processing VolumeSnapshot with non-existing PVC |
| [116372](https://hackerone.com/reports/116372) | Internet Bug Bounty |  | $500 | 14 | 2019-10-15 | Memory Corruption - Generic | Use-After-Free / Double-Free in WDDX Deserialize |
| [170144](https://hackerone.com/reports/170144) | Internet Bug Bounty |  | $500 | 14 | 2019-11-03 | Memory Corruption - Generic | wddx_deserialize use-after-free |
| [241202](https://hackerone.com/reports/241202) | Internet Bug Bounty | low | $500 | 14 | 2017-08-15 | Integer Overflow | Unsafe arithmetic in PyString_DecodeEscape |
| [195586](https://hackerone.com/reports/195586) | Internet Bug Bounty | medium | $500 | 12 | 2019-10-13 | Memory Corruption - Generic | Memory corruption when parsing a hostile PHAR archive |
| [831353](https://hackerone.com/reports/831353) | Internet Bug Bounty | medium | $500 | 12 | 2021-07-23 | Buffer Over-read | tcpdump before 4.9.3 has a heap-based buffer over-read related to aoe_print in print-aoe.c and lookup_emem in addrtoname.c |
| [114172](https://hackerone.com/reports/114172) | Internet Bug Bounty |  | $500 | 7 | 2019-10-15 | Memory Corruption - Generic | Out-of-Bound Read in phar_parse_zipfile() |
| [167904](https://hackerone.com/reports/167904) | Internet Bug Bounty |  | $500 | 7 | 2019-11-12 | Memory Corruption - Generic | heap overflow in substr_replace |
| [167906](https://hackerone.com/reports/167906) | Internet Bug Bounty |  | $500 | 7 | 2019-11-12 | Memory Corruption - Generic | integer overflow in imap_binary caused heap corruption |
| [167910](https://hackerone.com/reports/167910) | Internet Bug Bounty |  | $500 | 7 | 2019-11-12 | Memory Corruption - Generic | memory corruption in wordwrap function |
| [182420](https://hackerone.com/reports/182420) | Internet Bug Bounty | low | $500 | 7 | 2019-10-31 | Memory Corruption - Generic | Illegal write/read access caused by gdImageAALine overflow |
| [271330](https://hackerone.com/reports/271330) | Internet Bug Bounty | medium | $500 | 7 | 2019-10-13 | Memory Corruption - Generic | Format string implementation vulnerability, resulting in code execution |
| [167911](https://hackerone.com/reports/167911) | Internet Bug Bounty |  | $500 | 6 | 2019-11-12 | Memory Corruption - Generic | integer overflow in fgetcsv caused heap corruption |
| [200909](https://hackerone.com/reports/200909) | Internet Bug Bounty | medium | $500 | 6 | 2017-05-28 | Out-of-bounds Read | Out of bounds memory read in unserialize() |
| [305973](https://hackerone.com/reports/305973) | Internet Bug Bounty | low | $500 | 6 | 2019-11-12 | NULL Pointer Dereference | Inappropriately parsing HTTP response leads to PHP segment fault! |
| [146940](https://hackerone.com/reports/146940) | Internet Bug Bounty |  | $500 | 5 | 2019-10-31 | Memory Corruption - Generic | pass2_no_dither out-of-bounds access |
| [159953](https://hackerone.com/reports/159953) | Internet Bug Bounty |  | $500 | 5 | 2019-11-12 | Memory Corruption - Generic | integer overflow in curl_escape caused heap corruption |
| [159955](https://hackerone.com/reports/159955) | Internet Bug Bounty |  | $500 | 5 | 2019-11-12 | Memory Corruption - Generic | integer overflow in bzdecompress caused heap corruption |
| [167901](https://hackerone.com/reports/167901) | Internet Bug Bounty |  | $500 | 5 | 2019-11-12 | Memory Corruption - Generic | integer overflow in pg_escape_string caused heap corruption |
| [167905](https://hackerone.com/reports/167905) | Internet Bug Bounty |  | $500 | 5 | 2019-11-12 | Memory Corruption - Generic | integer overflow in pg_escape_bytea caused heap corruption |
| [159954](https://hackerone.com/reports/159954) | Internet Bug Bounty |  | $500 | 4 | 2019-11-12 | Memory Corruption - Generic | integer overflow in base64_decode caused heap corruption |
| [167902](https://hackerone.com/reports/167902) | Internet Bug Bounty |  | $500 | 4 | 2019-11-12 | Memory Corruption - Generic | integer overflow in php_ldap_do_escape caused heap corruption |
| [167903](https://hackerone.com/reports/167903) | Internet Bug Bounty |  | $500 | 4 | 2019-11-12 | Memory Corruption - Generic | integer overflow in str_pad caused heap corruption |
| [167908](https://hackerone.com/reports/167908) | Internet Bug Bounty |  | $500 | 4 | 2019-11-12 | Memory Corruption - Generic | integer overflow in fgets cause heap corruption |
| [190933](https://hackerone.com/reports/190933) | Internet Bug Bounty | low | $500 | 4 | 2017-02-08 | Memory Corruption - Generic | Invalid parameter in memcpy function trough openssl_pbkdf2 |
| [964583](https://hackerone.com/reports/964583) | Internet Bug Bounty | high | $500 | 4 | 2021-07-09 | Buffer Over-read | CVE-2017-13041 The ICMPv6 parser in tcpdump before 4.9.2 has a buffer over-read in print-icmp6.c:icmp6_nodeinfo_print(). |
| [1564100](https://hackerone.com/reports/1564100) | GitHub Security Lab |  | $500 | 4 |  | Memory Corruption - Generic | [CPP]: Add query for CWE-190: Integer Overflow or Wraparound when using transform after operation |
| [166080](https://hackerone.com/reports/166080) | Internet Bug Bounty |  | $500 | 3 | 2019-11-12 | Memory Corruption - Generic | null pointer dereference in set_conversion_mode due uncheck _ctypes_conversion_errors |
| [167907](https://hackerone.com/reports/167907) | Internet Bug Bounty |  | $500 | 3 | 2019-11-12 | Memory Corruption - Generic | integer overflow in preg_quote caused heap corruption |
| [724243](https://hackerone.com/reports/724243) | Internet Bug Bounty | critical | $500 | 3 | 2020-02-13 | Out-of-bounds Read | Tcpdump before 4.9.3 has a buffer over-read in print-802_11.c (CVE-2018-16227) |
| [724253](https://hackerone.com/reports/724253) | Internet Bug Bounty | critical | $500 | 3 | 2020-02-13 | Out-of-bounds Read | Tcpdump before 4.9.3 has a buffer over-read in print-dccp.c:dccp_print_option() (CVE-2018-16229) |
| [964582](https://hackerone.com/reports/964582) | Internet Bug Bounty | high | $500 | 3 | 2021-07-09 | Buffer Over-read | CVE-2017-13040 The MPTCP parser in tcpdump before 4.9.2 has a buffer over-read in print-mptcp.c, several functions. |
| [110720](https://hackerone.com/reports/110720) | Internet Bug Bounty |  | $500 | 2 | 2019-11-12 | Memory Corruption - Generic | Arbitary Memory Read via gdImageRotateInterpolated Array Index Out of Bounds |
| [110722](https://hackerone.com/reports/110722) | Internet Bug Bounty |  | $500 | 2 | 2019-11-12 | Memory Corruption - Generic | Heap BufferOver Flow in escapeshellargs and escapeshellcmd functions |
| [117651](https://hackerone.com/reports/117651) | Internet Bug Bounty |  | $500 | 2 | 2019-10-15 | Memory Corruption - Generic | Multiple Heap Overflow due to integer overflows \| xml/filter_url/addcslashes |
| [129771](https://hackerone.com/reports/129771) | Internet Bug Bounty |  | $500 | 2 | 2016-05-02 | Memory Corruption - Generic | Python 2.7 strop.replace Integer Overflow |
| [135291](https://hackerone.com/reports/135291) | Internet Bug Bounty |  | $500 | 2 | 2019-10-13 | Memory Corruption - Generic | Out-of-bounds reads in zif_grapheme_stripos with negative offset |
| [161198](https://hackerone.com/reports/161198) | Internet Bug Bounty |  | $500 | 2 | 2019-10-13 | Memory Corruption - Generic | wddx_deserialize null dereference with invalid xml |
| [161200](https://hackerone.com/reports/161200) | Internet Bug Bounty |  | $500 | 2 | 2019-10-31 | Memory Corruption - Generic | wddx_deserialize allows illegal memory access |
| [161217](https://hackerone.com/reports/161217) | Internet Bug Bounty |  | $500 | 2 | 2019-10-13 | Memory Corruption - Generic | wddx_deserialize null dereference in php_wddx_pop_element |
| [167909](https://hackerone.com/reports/167909) | Internet Bug Bounty |  | $500 | 2 | 2019-11-12 | Memory Corruption - Generic | integer overflow in recode_string caused heap corruption |
| [168029](https://hackerone.com/reports/168029) | Internet Bug Bounty |  | $500 | 2 | 2019-11-12 | Memory Corruption - Generic | ldap_escape could produce string larger than 2Gb |
| [170260](https://hackerone.com/reports/170260) | Internet Bug Bounty |  | $500 | 2 | 2019-10-31 | Memory Corruption - Generic | imap_rfc822_parse_headers GS Violation |
| [175310](https://hackerone.com/reports/175310) | Internet Bug Bounty | low | $500 | 2 | 2017-02-07 | Memory Corruption - Generic | Write out-of-bounds at number_format |
| [175312](https://hackerone.com/reports/175312) | Internet Bug Bounty | low | $500 | 2 | 2017-02-07 | Memory Corruption - Generic | memcpy negative parameter _bc_new_num_ex |
| [178094](https://hackerone.com/reports/178094) | Internet Bug Bounty | low | $500 | 2 | 2019-11-12 | Memory Corruption - Generic | php_snmp_parse_oid integer overflow in memory allocation |
| [178144](https://hackerone.com/reports/178144) | Internet Bug Bounty | low | $500 | 2 | 2019-10-13 | Memory Corruption - Generic | imagecropauto out-of-bounds access |
| [180109](https://hackerone.com/reports/180109) | Internet Bug Bounty | low | $500 | 2 | 2019-11-12 | Memory Corruption - Generic | crash in gzcompress and 3 other compress functions |
| [203002](https://hackerone.com/reports/203002) | Internet Bug Bounty | low | $500 | 2 | 2019-11-12 | Memory Corruption - Generic | Incorrect GC behavior in xxlimited could lead to use-after-free |
| [216151](https://hackerone.com/reports/216151) | Internet Bug Bounty | low | $500 | 2 | 2019-11-12 | Use After Free | Use-after-free in _asyncio_Future_remove_done_callback |
| [248601](https://hackerone.com/reports/248601) | Internet Bug Bounty | medium | $500 | 2 | 2019-10-14 | Classic Buffer Overflow | PHP INI Parsing Stack Buffer Overflow Vulnerability |
| [248609](https://hackerone.com/reports/248609) | Internet Bug Bounty | medium | $500 | 2 | 2019-10-14 | Heap Overflow | PHP OpenSSL zif_openssl_seal() heap overflow (wild memcpy) |
| [248659](https://hackerone.com/reports/248659) | Internet Bug Bounty | medium | $500 | 2 | 2019-10-14 | Buffer Over-read | PHP WDDX Deserialization Heap OOB Read in timelib_meridian() |
| [283644](https://hackerone.com/reports/283644) | Internet Bug Bounty | medium | $500 | 2 | 2019-10-14 | Buffer Over-read | Out-Of-Bounds Read in timelib_meridian() |
| [477897](https://hackerone.com/reports/477897) | Internet Bug Bounty | medium | $500 | 2 | 2020-11-09 | Buffer Over-read | buffer overread in base64 code of the xmlrpc module |
| [778834](https://hackerone.com/reports/778834) | Internet Bug Bounty | medium | $500 | 2 | 2020-11-09 | Buffer Over-read | OOB read in php_strip_tags_ex |
| [73259](https://hackerone.com/reports/73259) | Internet Bug Bounty |  | $500 | 1 | 2015-06-27 | Memory Corruption - Generic | Integer overflow in _pickle.c |
| [113798](https://hackerone.com/reports/113798) | Internet Bug Bounty |  | $500 | 1 | 2019-10-13 | Memory Corruption - Generic | Null pointer deref with ob_start with compact |
| [113799](https://hackerone.com/reports/113799) | Internet Bug Bounty |  | $500 | 1 | 2019-10-13 | Memory Corruption - Generic | Null pointer deref with ob_start with get_defined_vars |
| [135293](https://hackerone.com/reports/135293) | Internet Bug Bounty |  | $500 | 1 | 2019-10-13 | Memory Corruption - Generic | bcpowmod accepts negative scale and corrupts _one_ definition |
| [135294](https://hackerone.com/reports/135294) | Internet Bug Bounty |  | $500 | 1 | 2019-10-13 | Memory Corruption - Generic | xml_parse_into_struct segmentation fault |
| [141197](https://hackerone.com/reports/141197) | Internet Bug Bounty |  | $500 | 1 | 2019-10-13 | Memory Corruption - Generic | get_icu_value_internal out-of-bounds read |
| [141202](https://hackerone.com/reports/141202) | Internet Bug Bounty |  | $500 | 1 | 2019-10-31 | Memory Corruption - Generic | imagescale out-of-bounds read |
| [141212](https://hackerone.com/reports/141212) | Internet Bug Bounty |  | $500 | 1 | 2019-10-13 | Memory Corruption - Generic | Integer underflow / arbitrary null write in fread/gzread |
| [143234](https://hackerone.com/reports/143234) | Internet Bug Bounty |  | $500 | 1 | 2019-11-12 | Memory Corruption - Generic | Integer Overflow in _gd2GetHeader() resulting in heap overflow |
| [147125](https://hackerone.com/reports/147125) | Internet Bug Bounty |  | $500 | 1 | 2019-11-12 | Memory Corruption - Generic | Integer Overflow in gdImagePaletteToTrueColor() resulting in heap overflow |
| [152782](https://hackerone.com/reports/152782) | Internet Bug Bounty |  | $500 | 1 | 2019-10-13 | Memory Corruption - Generic | locale_accept_from_http out-of-bounds access |
| [152784](https://hackerone.com/reports/152784) | Internet Bug Bounty |  | $500 | 1 | 2019-10-13 | Memory Corruption - Generic | imagegif/output out-of-bounds access |
| [153776](https://hackerone.com/reports/153776) | Internet Bug Bounty |  | $500 | 1 | 2019-10-31 | Memory Corruption - Generic | gdImageTrueColorToPaletteBody allows arbitrary write/read access |
| [161216](https://hackerone.com/reports/161216) | Internet Bug Bounty |  | $500 | 1 | 2019-10-31 | Memory Corruption - Generic | wddx_deserialize null dereference |
| [167921](https://hackerone.com/reports/167921) | Internet Bug Bounty |  | $500 | 1 | 2019-11-12 | Memory Corruption - Generic | integer overflow in xml_utf8_encode |
| [167977](https://hackerone.com/reports/167977) | Internet Bug Bounty |  | $500 | 1 | 2019-11-12 | Memory Corruption - Generic | Missing type check when unserializing SplArray |
| [168027](https://hackerone.com/reports/168027) | Internet Bug Bounty |  | $500 | 1 | 2019-11-12 | Memory Corruption - Generic | gzdecode does NOT check output string size which leads to an overflow |
| [168028](https://hackerone.com/reports/168028) | Internet Bug Bounty |  | $500 | 1 | 2019-11-12 | Memory Corruption - Generic | gzuncompress does NOT check output string size which leads to an overflow |
| [175311](https://hackerone.com/reports/175311) | Internet Bug Bounty | low | $500 | 1 | 2017-02-07 | Memory Corruption - Generic | memcpy negative size parameter in php_resolve_path |
| [175315](https://hackerone.com/reports/175315) | Internet Bug Bounty | low | $500 | 1 | 2019-10-13 | Memory Corruption - Generic | Illegal write access through Locale methods |
| [175316](https://hackerone.com/reports/175316) | Internet Bug Bounty | low | $500 | 1 | 2019-10-13 | Memory Corruption - Generic | stack-buffer-overflow through "ResourceBundle" methods |
| [176226](https://hackerone.com/reports/176226) | Internet Bug Bounty | low | $500 | 1 | 2019-11-12 | Memory Corruption - Generic | CachingIterator null dereference when convert to string |
| [180110](https://hackerone.com/reports/180110) | Internet Bug Bounty | low | $500 | 1 | 2019-11-12 | Memory Corruption - Generic | crash in implode() function |
| [180111](https://hackerone.com/reports/180111) | Internet Bug Bounty | low | $500 | 1 | 2019-11-12 | Memory Corruption - Generic | crash in bzcompress function |
| [180112](https://hackerone.com/reports/180112) | Internet Bug Bounty | low | $500 | 1 | 2019-11-12 | Memory Corruption - Generic | iconv() function missing string length check |
| [180113](https://hackerone.com/reports/180113) | Internet Bug Bounty | low | $500 | 1 | 2019-11-12 | Memory Corruption - Generic | crash in get_icu_value_internal function |
| [180588](https://hackerone.com/reports/180588) | Internet Bug Bounty | low | $500 | 1 | 2019-11-12 | Memory Corruption - Generic | Invalid memory access in zend_strtod() function |
| [180589](https://hackerone.com/reports/180589) | Internet Bug Bounty | low | $500 | 1 | 2019-11-12 | Memory Corruption - Generic | crash in simplestring_addn function |
| [180590](https://hackerone.com/reports/180590) | Internet Bug Bounty | low | $500 | 1 | 2019-11-12 | Memory Corruption - Generic | Invalid memory access in spl_filesystem_dir_open function |
| [180591](https://hackerone.com/reports/180591) | Internet Bug Bounty | low | $500 | 1 | 2019-11-12 | Memory Corruption - Generic | Invalid memory access in php_basename function |
| [180592](https://hackerone.com/reports/180592) | Internet Bug Bounty | low | $500 | 1 | 2019-11-12 | Memory Corruption - Generic | Invalid memory access in spl_filesystem_info_set_filename function |
| [181073](https://hackerone.com/reports/181073) | Internet Bug Bounty | low | $500 | 1 | 2019-11-12 | Memory Corruption - Generic | malloc negative size parameter |
| [320222](https://hackerone.com/reports/320222) | Internet Bug Bounty | medium | $500 | 1 | 2019-10-14 | Array Index Underflow | memory corruption while parsing HTTP response |
| [103990](https://hackerone.com/reports/103990) | Internet Bug Bounty |  | $500 | 0 | 2015-09-29 | Memory Corruption - Generic | Null pointer dereference in phar_get_fp_offset() |
| [103994](https://hackerone.com/reports/103994) | Internet Bug Bounty |  | $500 | 0 | 2015-09-12 | Memory Corruption - Generic | Python 3.3 - 3.5 product_setstate() Out-of-bounds Read |
| [104004](https://hackerone.com/reports/104004) | Internet Bug Bounty |  | $500 | 0 | 2015-08-02 | Memory Corruption - Generic | Mem out-of-bounds write (segfault) in ZEND_ASSIGN_DIV_SPEC_CV_UNUSED_HANDLER |
| [104005](https://hackerone.com/reports/104005) | Internet Bug Bounty |  | $500 | 0 | 2015-08-02 | Memory Corruption - Generic | null pointer deref (segfault) in zend_eval_const_expr |
| [104006](https://hackerone.com/reports/104006) | Internet Bug Bounty |  | $500 | 0 | 2015-08-23 | Memory Corruption - Generic | Null pointer deref (segfault) in spl_autoload via ob_start |
| [104011](https://hackerone.com/reports/104011) | Internet Bug Bounty |  | $500 | 0 | 2015-10-15 | Memory Corruption - Generic | AddressSanitizer reports a global buffer overflow in mkgmtime() function |
| [104012](https://hackerone.com/reports/104012) | Internet Bug Bounty |  | $500 | 0 | 2015-10-15 | Memory Corruption - Generic | Integer overflow in unserialize() (32-bits only) |
| [104013](https://hackerone.com/reports/104013) | Internet Bug Bounty |  | $500 | 0 | 2015-01-26 | Memory Corruption - Generic | heap buffer overflow in enchant_broker_request_dict() |
| [104022](https://hackerone.com/reports/104022) | Internet Bug Bounty |  | $500 | 0 | 2015-06-27 | Memory Corruption - Generic | hotshot pack_string Heap Buffer Overflow |
| [104024](https://hackerone.com/reports/104024) | Internet Bug Bounty |  | $500 | 0 | 2015-07-25 | Memory Corruption - Generic | array.fromstring Use After Free |
| [104025](https://hackerone.com/reports/104025) | Internet Bug Bounty |  | $500 | 0 | 2015-07-02 | Memory Corruption - Generic | use after free in load_newobj_ex |
| [104027](https://hackerone.com/reports/104027) | Internet Bug Bounty |  | $500 | 0 | 2015-05-12 | Memory Corruption - Generic | Memory Corruption in phar_parse_tarfile when entry filename starts with null |
| [114024](https://hackerone.com/reports/114024) | Internet Bug Bounty |  | $500 | 0 | 2019-11-12 | Memory Corruption - Generic | Stack overflow when decompressing tar archives |
| [763403](https://hackerone.com/reports/763403) | Valve | high | $450 | 24 | 2020-08-19 | Classic Buffer Overflow | [GoldSrc] RCE via malformed BSP file |
| [796555](https://hackerone.com/reports/796555) | Open-Xchange |  | $400 | 11 |  | Memory Corruption - Generic | access to stack memory beyond array boundaries |
| [966834](https://hackerone.com/reports/966834) | Open-Xchange |  | $400 | 5 |  | Buffer Over-read | Incomplete fix for CVE-2020-12673 : Specially crafted NTML message leads to buffer over read |
| [967457](https://hackerone.com/reports/967457) | Open-Xchange |  | $400 | 2 |  | Buffer Over-read | Buffer overread off by one in `rpa_read_buffer`, incomplete fix for CVE-2020-12674 |
| [505173](https://hackerone.com/reports/505173) | Valve | medium | $350 | 30 | 2019-09-17 | Stack Overflow | Malformed map detailed texture files in GoldSrc games lead to Remote Code Execution |
| [769014](https://hackerone.com/reports/769014) | Valve | high | $350 | 23 | 2020-08-19 | Classic Buffer Overflow | [GoldSrc] RCE via 'spk' Console Command |
| [126797](https://hackerone.com/reports/126797) | Tor |  | $300 | 10 | 2017-10-21 | Memory Corruption - Generic | Use-after-free during XML transformations (MFSA-2016-27) |
| [798301](https://hackerone.com/reports/798301) | FileZilla | low | $250 | 16 | 2020-11-21 | Classic Buffer Overflow | FileZilla 3.46.3 - 'Scale factor' Buffer Overflow |
| [1073363](https://hackerone.com/reports/1073363) | Kubernetes | none | $250 | 13 | 2021-08-30 | Buffer Over-read | Index Out Of Bounds in protobuf unmarshalling |
| [391097](https://hackerone.com/reports/391097) | Block.one |  | $250 | 10 |  | Classic Buffer Overflow | [FG-VD-18-125] Buffer Overflow Vulnerability in Latest EOS's EOSIO.WASMSDK Repository |
| [391099](https://hackerone.com/reports/391099) | Block.one |  | $250 | 10 |  | Classic Buffer Overflow | [FG-VD-18-126] Buffer Overflow Vulnerability in Latest EOS's EOSIO.WASMSDK Repository II |
| [784186](https://hackerone.com/reports/784186) | Node.js | high | $250 | 7 | 2020-07-02 | Memory Corruption - Generic | napi_get_value_string_X allow various kinds of memory corruption |
| [127918](https://hackerone.com/reports/127918) | Uber |  | $250 | 1 | 2016-06-13 | Memory Corruption - Generic | Easy spam with USE My PHONE Feature |
| [193719](https://hackerone.com/reports/193719) | shopify-scripts |  | $200 | 6 | 2017-02-07 | Memory Corruption - Generic | Double free of filename after codegen error |
| [194884](https://hackerone.com/reports/194884) | shopify-scripts | low | $200 | 5 | 2017-02-07 | Memory Corruption - Generic | Heap use-after-free during range creation |
| [23852](https://hackerone.com/reports/23852) | Mail.ru |  | $150 | 1 |  | Memory Corruption - Generic | money.mail.ru: Странное поведение SMS |
| [249786](https://hackerone.com/reports/249786) | VK.com | low | $100 | 13 | 2018-03-04 | Heap Overflow | Отсутствие flood контроля в ИСТОРИЯХ вк |
| [269568](https://hackerone.com/reports/269568) | Internet Bug Bounty | low | $100 | 8 | 2018-05-03 | Use After Free | Optionsbleed / CVE-2017-9798 |
| [208363](https://hackerone.com/reports/208363) | shopify-scripts | high | $100 | 6 | 2017-04-17 | Memory Corruption - Generic | Memory corrouption in mrb_gc_mark |
| [139940](https://hackerone.com/reports/139940) | LocalTapiola |  | $100 | 4 |  | Memory Corruption - Generic | Exploiting Secure Shell (SSH) on mobilelt.lahitapiola.fi |
| [192665](https://hackerone.com/reports/192665) | shopify-scripts | none | $100 | 4 | 2017-02-10 | Memory Corruption - Generic | heap-buffer-overflow on mruby |
| [192235](https://hackerone.com/reports/192235) | shopify-scripts |  | $100 | 3 | 2017-01-12 | Memory Corruption - Generic | Integer Overflow in mrb_ary_set |
| [200821](https://hackerone.com/reports/200821) | shopify-scripts |  | $100 | 3 | 2017-02-07 | Memory Corruption - Generic | heap-use-after-free /home/operac/testafl/mruby/mrubylast/mruby/src/gc.c |
| [218803](https://hackerone.com/reports/218803) | shopify-scripts | medium | $100 | 2 | 2017-05-02 | Memory Corruption - Generic | SIGABRT in sym_validate_len - symbol.c:44 |
| [222171](https://hackerone.com/reports/222171) | shopify-scripts |  | $100 | 2 | 2017-05-07 | Memory Corruption - Generic | heap use after free in fiber_switch |
| [865195](https://hackerone.com/reports/865195) | Open-Xchange |  | $50 | 14 |  | Buffer Over-read | reading the stack data of the imap process |
| [832227](https://hackerone.com/reports/832227) | Open-Xchange |  | $50 | 9 |  | Buffer Over-read | Buffer over-reads in i_stream_zlib_read |
| [900548](https://hackerone.com/reports/900548) | Open-Xchange |  | $50 | 9 |  | Buffer Over-read | Buffer over read from `smtp_command_parse_parameters` |
| [891069](https://hackerone.com/reports/891069) | Open-Xchange |  | $50 | 5 |  | NULL Pointer Dereference | null dereference in `sieve_address_do_validate` (or redundant null check) |
| [891080](https://hackerone.com/reports/891080) | Open-Xchange |  | $50 | 5 |  | NULL Pointer Dereference | Null pointer deference in call to `mail_get_flags` |
| [831290](https://hackerone.com/reports/831290) | Open-Xchange |  | $50 | 3 |  | NULL Pointer Dereference | Null pointer dereference in SMTP server function smtp_command_parse_data_with_size |
| [908894](https://hackerone.com/reports/908894) | Open-Xchange |  | $50 | 3 |  | NULL Pointer Dereference | Null dereference or redundant null check in `mail_crypt_load_global_private_key` for plugin mail-crypt |
| [836036](https://hackerone.com/reports/836036) | Open-Xchange |  | $50 | 2 |  | Buffer Over-read | Multiple buffer over reads in mbox_from_parse |
| [836045](https://hackerone.com/reports/836045) | Open-Xchange |  | $50 | 2 |  | Buffer Over-read | Buffer overread in parse_angle_addr called from message_address_parse_path |
| [894446](https://hackerone.com/reports/894446) | Open-Xchange |  | $50 | 0 |  | NULL Pointer Dereference | Null dereference in mcht_relational_validate ext-relational-common.c:136 |
| [965881](https://hackerone.com/reports/965881) | Open-Xchange |  | $50 | 0 |  | NULL Pointer Dereference | Null dereference in `cmd_denotify_operation_execute` |
| [470520](https://hackerone.com/reports/470520) | Valve | critical | - | 1289 | 2019-03-15 | Classic Buffer Overflow | RCE on Steam Client via buffer overflow in Server Info |
| [397545](https://hackerone.com/reports/397545) | Valve | high | - | 321 | 2020-02-27 | Classic Buffer Overflow | Malformed .BMP file in Counter-Strike 1.6 may cause shellcode injection |
| [2101076](https://hackerone.com/reports/2101076) | HackerOne | high | - | 228 | 2024-02-04 | Improper Null Termination | HackerOne SAML signup domain enforcement bypass results in unauthorized access to HackerOne PullRequest organization |
| [351014](https://hackerone.com/reports/351014) | Valve | critical | - | 154 | 2018-07-19 | Classic Buffer Overflow | Malformed .BSP Access Violation in CS:GO can lead to Remote Code Execution |
| [146845](https://hackerone.com/reports/146845) | HackerOne |  | - | 125 | 2016-08-03 | Memory Corruption - Generic | Race Conditions in Popular reports feature. |
| [2958097](https://hackerone.com/reports/2958097) | Brave Software | low | - | 116 | 2025-03-26 | NULL Pointer Dereference | Null Pointer Dereference by Crafted Response from AI Model |
| [480883](https://hackerone.com/reports/480883) | Notepad++ | high | - | 99 | 2019-08-25 | Stack Overflow | Stack overflow in XML Parsing |
| [495793](https://hackerone.com/reports/495793) | Valve | high | - | 90 | 2019-10-09 | Memory Corruption - Generic | Malformed .MDL triggers an Access Violation on GoldSRC (hl.exe) |
| [419896](https://hackerone.com/reports/419896) | HackerOne | high | - | 87 | 2018-10-09 | Improper Null Termination | Unauthenticated user can upload an attachment to the last updated report draft |
| [1350653](https://hackerone.com/reports/1350653) | PlayStation | high | - | 86 | 2022-05-11 | Heap Overflow | Remote kernel heap overflow |
| [1180380](https://hackerone.com/reports/1180380) | curl | high | - | 76 | 2021-05-26 | Use After Free | CVE-2021-22901: TLS session caching disaster |
| [477344](https://hackerone.com/reports/477344) | Internet Bug Bounty | high | - | 72 | 2020-10-10 | Buffer Over-read | Heap Buffer Overflow (READ: 4) in phar_parse_pharfile |
| [3399016](https://hackerone.com/reports/3399016) | Nextcloud | none | - | 65 | 2026-05-01 | Improper Null Termination | Improper input validation On Exported deep-link handler crashes `FileDisplayActivity` on crafted external URL — Denial-of-Service |
| [3083428](https://hackerone.com/reports/3083428) | Node.js | low | - | 59 | 2025-05-15 | Memory Corruption - Generic | Corrupted pointer in node::fs::ReadFileUtf8(const FunctionCallbackInfo<Value>& args) when args[0] is a string. |
| [3591956](https://hackerone.com/reports/3591956) | curl | high | - | 58 | 2026-04-29 | Use After Free | Use-After-Free in SMB connection reuse (req->path dangling pointer after needle destruction) |
| [832750](https://hackerone.com/reports/832750) | Valve | high | - | 55 | 2020-08-19 | Stack Overflow | Buffer overflow In hl.exe's launch -game argument allows an attacker to execute arbitrary code locally or from browser |
| [2187833](https://hackerone.com/reports/2187833) | curl | high | - | 55 | 2023-10-11 | Heap Overflow | CVE-2023-38545: socks5 heap buffer overflow |
| [2629968](https://hackerone.com/reports/2629968) | curl | low | - | 53 | 2024-08-01 | Buffer Over-read | CVE-2024-7264: ASN.1 date parser overread |
| [2823554](https://hackerone.com/reports/2823554) | curl | critical | - | 53 | 2024-11-07 | Buffer Underflow | Buffer overflow in strcpy |
| [480984](https://hackerone.com/reports/480984) | Notepad++ | medium | - | 51 | 2019-08-25 | Stack Overflow | Stack overflow affecting "ext" field on stylers.xml configuration file |
| [3788482](https://hackerone.com/reports/3788482) | MariaDB | critical | - | 51 | 2026-09-08 | Stack Overflow | Stack Buffer Overflow in mariadb-dump quote_name() Allows Malicious Server to Execute Arbitrary Code on Client |
| [176279](https://hackerone.com/reports/176279) | Internet Bug Bounty | medium | - | 50 | 2019-11-12 | Memory Corruption - Generic | Heap overflow in mysqlnd related to BIT fields (CVE-2016-7412) |
| [484930](https://hackerone.com/reports/484930) | PuTTY (European Commission - DIGIT) | low | - | 46 | 2019-11-03 | Memory Corruption - Generic | puttygen: 160MB memory leak while trying to extract openssh public key from crafted key file |
| [3523349](https://hackerone.com/reports/3523349) | curl | medium | - | 46 | 2026-01-26 | Integer Underflow | Integer Underflow in src/var.c |
| [2871792](https://hackerone.com/reports/2871792) | curl | critical | - | 45 | 2024-12-02 | Classic Buffer Overflow | Buffer Overflow Vulnerability in strcpy() Leading to Remote Code Execution |
| [3693636](https://hackerone.com/reports/3693636) | Monero | high | - | 44 | 2026-08-05 | NULL Pointer Dereference | wallet-rpc crash via malformed /gettransactions response (empty txs → vector::front() in check_tx_key / check_tx_proof) |
| [3736889](https://hackerone.com/reports/3736889) | Node.js | high | - | 44 | 2026-05-23 | NULL Pointer Dereference | NULL pointer dereference in node:sqlite DatabaseSync#applyChangeset() via malformed SQLite changeset |
| [897606](https://hackerone.com/reports/897606) | Nintendo | none | - | 43 | 2020-12-18 | Heap Overflow | [3DS][SSL][SDK] Unchecked number of audio channels in Mobiclip SDK leads to RCE in eShop movie player |
| [1113025](https://hackerone.com/reports/1113025) | Internet Bug Bounty | high | - | 43 | 2021-04-08 | Integer Overflow | Integer overflow in CipherUpdate |
| [3897914](https://hackerone.com/reports/3897914) | MariaDB | high | - | 43 | 2026-09-08 | Out-of-bounds Read | Out-of-bounds read in MariaDB .frm parsing enables RCE via vtable hijacking |
| [280912](https://hackerone.com/reports/280912) | QIWI |  | - | 42 |  | Buffer Over-read | apache access.log leakage via long request on https://rapida.ru/ |
| [384477](https://hackerone.com/reports/384477) | Internet Bug Bounty | medium | - | 42 | 2019-10-21 | Integer Overflow | Int Overflow lead to Heap OverFlow in exif_thumbnail_extract of exif.c |
| [2551512](https://hackerone.com/reports/2551512) | Nintendo | low | - | 42 | 2026-08-07 | Stack Overflow | [Wii U/3DS/Switch] Improper bounds check in StationURL in all NEX clients leading to remote crash/RCE |
| [3717365](https://hackerone.com/reports/3717365) | curl |  | - | 42 | 2026-05-07 | Improper Null Termination | mbedTLS private-key blob null-termination asymmetry in lib/vtls/mbedtls.c (mbed_load_privkey) |
| [3620748](https://hackerone.com/reports/3620748) | AWS VDP | medium | - | 41 | 2026-05-28 | Array Index Underflow | V1Plugin.Decrypt panics on empty ciphertext (Remote DoS) |
| [838127](https://hackerone.com/reports/838127) | Internet Bug Bounty | high | - | 40 | 2020-10-21 | Stack Overflow | mb_strtolower (UTF-32LE): stack-buffer-overflow at php_unicode_tolower_full (CVE-2020-7065) |
| [216330](https://hackerone.com/reports/216330) | Legal Robot | medium | - | 39 | 2017-07-30 | Classic Buffer Overflow | Big XSS vulnerability! |
| [2887487](https://hackerone.com/reports/2887487) | curl | high | - | 39 | 2024-12-08 | Classic Buffer Overflow | Buffer Overflow Risk in Curl_inet_ntop and inet_ntop4 |
| [895769](https://hackerone.com/reports/895769) | Nintendo | none | - | 38 | 2020-12-18 | Use After Free | [3DS][SSL] Use of uninitialized class member leads to RCE in eShop movie player |
| [1977252](https://hackerone.com/reports/1977252) | Brave Software | critical | - | 38 | 2023-10-11 | Use After Free | UAF on JSEthereumProvider |
| [2298307](https://hackerone.com/reports/2298307) | curl | high | - | 38 | 2024-01-02 | Heap Overflow | Buffer Overflow Vulnerability in WebSocket Handling |
| [3598358](https://hackerone.com/reports/3598358) | curl | high | - | 38 | 2026-03-12 | Off-by-one Error | urlapi: off-by-one in custom scheme validation skips last character |
| [1434056](https://hackerone.com/reports/1434056) | Internet Bug Bounty | high | - | 36 | 2022-01-04 | Heap Overflow | Buffer overflow in req_parsebody method in lua_request.c |
| [1813453](https://hackerone.com/reports/1813453) | Nintendo | critical | - | 36 | 2025-07-06 | Memory Corruption - Generic | [MK8DX] Improper ranking/replay file parsing |
| [2611669](https://hackerone.com/reports/2611669) | Nintendo | medium | - | 36 | 2024-09-30 | Stack Overflow | [Switch, PIA/MK8DX] Stack buffer overflow and potential RCE in PIA (LAN/LDN, possibly NEX) room info deserialization |
| [3294999](https://hackerone.com/reports/3294999) | curl | low | - | 36 | 2025-09-10 | Buffer Over-read | CVE-2025-9086: Out of bounds read for cookie path |
| [3575245](https://hackerone.com/reports/3575245) | curl | medium | - | 36 | 2026-02-26 | Classic Buffer Overflow | Integer Overflow in curl_multi_get_handles() Leading to Heap Buffer Overflow |
| [3770768](https://hackerone.com/reports/3770768) | Nintendo | high | - | 35 | 2026-10-15 | Stack Overflow | [Switch] Remote stack buffer overflow in the LDN/LP2P DHCP server leads to control-flow hijack |
| [1210450](https://hackerone.com/reports/1210450) | Internet Bug Bounty | medium | - | 34 | 2021-08-27 | Off-by-one Error | 1-byte heap buffer overflow in DNS resolver |
| [2559516](https://hackerone.com/reports/2559516) | curl | medium | - | 34 | 2024-07-24 | Free of Memory not on the Heap | CVE-2024-6197: freeing stack buffer in utf8asn1str |
| [3591944](https://hackerone.com/reports/3591944) | curl | medium | - | 34 | 2026-03-11 | Use After Free | CVE-2026-3805: use after free in SMB connection reuse |
| [350119](https://hackerone.com/reports/350119) | Valve | medium | - | 33 | 2018-08-28 | Classic Buffer Overflow | Buffer overflows in demo parsing |
| [3709605](https://hackerone.com/reports/3709605) | Tor | medium | - | 33 | 2026-09-10 | Out-of-bounds Read | Conflux-queued zero-length RELAY_END triggers heap out-of-bounds read |
| [3738654](https://hackerone.com/reports/3738654) | AWS VDP | none | - | 33 | 2026-06-11 | Out-of-bounds Read | Firecracker Out-of-bounds Read/Write Local Privilege Escalation Vulnerability |
| [187134](https://hackerone.com/reports/187134) | PortSwigger Web Security | high | - | 32 | 2016-12-07 | Memory Corruption - Generic | JSBeautifier BApp: Race condition leads to memory disclosure |
| [334709](https://hackerone.com/reports/334709) | Greenhouse.io | medium | - | 32 | 2018-09-16 | Improper Null Termination | Cache poisoning using NULL bytes and long URLs |
| [2621062](https://hackerone.com/reports/2621062) | Internet Bug Bounty | low | - | 31 | 2024-09-22 | Buffer Over-read | curl: stack-buffer overread during punycode conversions |
| [3896671](https://hackerone.com/reports/3896671) | MariaDB |  | - | 31 | 2026-09-30 | Out-of-bounds Read | Connector/C Out-of-bounds read in `unpack_fields()` from short metadata field |
| [351016](https://hackerone.com/reports/351016) | Valve | high | - | 30 | 2018-08-28 | Classic Buffer Overflow | Malformed Skybox .TGA in Half-Life (GoldSRC) leads to Access Violation |
| [687887](https://hackerone.com/reports/687887) | Nintendo | none | - | 30 | 2021-04-20 | Heap Overflow | [3DS][StreetPass] Buffer Overflow in Super Mario Maker level decompression |
| [923240](https://hackerone.com/reports/923240) | Nintendo | none | - | 30 | 2021-01-18 | Heap Overflow | [3DS][StreetPass] Heap Overflow in Swapnote parser leads to userland StreetPass RCE |
| [3242005](https://hackerone.com/reports/3242005) | curl | high | - | 30 | 2025-07-09 | Use After Free | Use-After-Free in OpenSSL Keylog Callback via SSL_get_ex_data() in libcurl |
| [3283232](https://hackerone.com/reports/3283232) | curl |  | - | 30 | 2025-08-06 | Use After Free | Use After Free (that leads to arbitrary Write for some versions) |
| [3804525](https://hackerone.com/reports/3804525) | curl | critical | - | 30 | 2026-06-16 | Memory Corruption - Generic | Vulnerability Report: Buffer Overflow in Path Sanitization |
| [477073](https://hackerone.com/reports/477073) | Internet Bug Bounty | high | - | 29 | 2019-09-12 | Memory Corruption - Generic | ZeroMQ libzmq remote code execution |
| [824771](https://hackerone.com/reports/824771) | Internet Bug Bounty | critical | - | 29 | 2021-08-26 | Classic Buffer Overflow | UrnState Heap Overflow |
| [1562515](https://hackerone.com/reports/1562515) | Glovo | critical | - | 29 | 2022-05-17 | Integer Overflow | Integer overflow vulnerability |
| [1781096](https://hackerone.com/reports/1781096) | Cloudflare Public Bug Bounty | low | - | 29 | 2023-07-31 | Memory Corruption - Generic | 💥💥Crash report -Cloudflare WARP doesn't verify text length in "Excluded Host" name input data💥💥 |
| [2981245](https://hackerone.com/reports/2981245) | curl | none | - | 29 | 2025-02-08 | Memory Corruption - Generic | ("possible") UAF |
| [3094406](https://hackerone.com/reports/3094406) | curl | high | - | 29 | 2025-04-27 | Heap Overflow | Heap‑based buffer overflow in curl -K <config_file> allows arbitrary write . |
| [3137657](https://hackerone.com/reports/3137657) | curl |  | - | 28 | 2025-05-10 | Memory Corruption - Generic | Memory Leak |
| [3282709](https://hackerone.com/reports/3282709) | curl | medium | - | 28 | 2025-08-02 | Integer Overflow | Integer Overflow in schannel.c TLS Data Transmission |
| [3434510](https://hackerone.com/reports/3434510) | curl | high | - | 28 | 2025-11-20 | Buffer Over-read | Out-of-bounds read in HTTP method handling causes undefined behavior and potential crash This is sharp, Gaurav. We’ve got a real memory-safety bug ins |
| [3516186](https://hackerone.com/reports/3516186) | curl | critical | - | 28 | 2026-01-19 | Integer Overflow | Cookie Max-Age Integer Overflow Vulnerability |
| [988103](https://hackerone.com/reports/988103) | Node.js | high | - | 27 | 2021-01-05 | Use After Free | Node.js: use-after-free in TLSWrap |
| [3117697](https://hackerone.com/reports/3117697) | curl |  | - | 27 | 2025-04-29 | Double Free | Double Free Vulnerability in `libcurl` Cookie Management (`cookie.c`) |
| [3279804](https://hackerone.com/reports/3279804) | curl | high | - | 27 | 2025-07-31 | Use After Free | Stack use-after-scope in HTTP/3 POST request processing via CURLOPT_POSTFIELDS |
| [3751715](https://hackerone.com/reports/3751715) | curl |  | - | 27 | 2026-05-25 | Buffer Over-read | Heap-OOB read in urlapi `redirect_url()` via `CURLU_GUESS_SCHEME` + `CURLU_NO_GUESS_SCHEME` flow |
| [499](https://hackerone.com/reports/499) | Ruby |  | - | 26 | 2013-11-22 | Memory Corruption - Generic | Ruby: Heap Overflow in Floating Point Parsing |
| [2559558](https://hackerone.com/reports/2559558) | curl | low | - | 26 | 2024-06-19 | NULL Pointer Dereference | NULL dereference when encoding DN of x509 certificate |
| [3022041](https://hackerone.com/reports/3022041) | curl |  | - | 26 | 2025-03-06 | Use After Free | Use after free (read) in curl_multi_perform with DoH and Proxy options, and resolve timeouts |
| [3344663](https://hackerone.com/reports/3344663) | curl |  | - | 26 | 2025-09-18 | Integer Overflow | Security Analysis Report: CURL Integer Overflow Vulnerability |
| [3409193](https://hackerone.com/reports/3409193) | curl | none | - | 26 | 2025-11-03 | Array Index Underflow | HackerOne |
| [282518](https://hackerone.com/reports/282518) | Infogram | medium | - | 25 | 2024-02-01 | Classic Buffer Overflow | Memory Corruption via Large Pixels |
| [2604391](https://hackerone.com/reports/2604391) | curl | low | - | 25 | 2024-07-24 | Buffer Over-read | CVE-2024-6874: macidn punycode buffer overread |
| [2779070](https://hackerone.com/reports/2779070) | Linux Foundation Decentralized Trust | low | - | 25 | 2024-10-24 | Use After Free | Memory Leak in bytes_to_hexstring Function |
| [3240792](https://hackerone.com/reports/3240792) | Monero |  | - | 25 | 2026-04-06 | Integer Overflow | Reported RPC Overflow |
| [3597359](https://hackerone.com/reports/3597359) | curl | medium | - | 25 | 2026-03-11 | NULL Pointer Dereference | NULL Pointer Dereference (DoS) in libcurl SFTP QUOTE command parsing due to missing return statement |
| [3620753](https://hackerone.com/reports/3620753) | AWS VDP | medium | - | 25 | 2026-05-28 | Array Index Underflow | V2Plugin.Decrypt panics on empty ciphertext (Remote DoS) |
| [547630](https://hackerone.com/reports/547630) | curl | low | - | 24 | 2020-12-05 | Incorrect Calculation of Buffer Size | CVE-2019-5435: An integer overflow found in /lib/urlapi.c |
| [2974850](https://hackerone.com/reports/2974850) | Internet Bug Bounty | low | - | 24 | 2025-04-27 | Heap Overflow | CVE-2025-0725: Heap overflow in curl with Content-Encoding gzip and old libz versions |
| [3324190](https://hackerone.com/reports/3324190) | curl | none | - | 24 | 2025-09-04 | Out-of-bounds Read | Heap-buffer-overflow (Out-of-Bounds Read) in DoH hostname encoding |
| [500](https://hackerone.com/reports/500) | Internet Bug Bounty |  | - | 23 | 2013-11-07 | Memory Corruption - Generic | OpenSSH: Memory corruption in AES-GCM support |
| [284807](https://hackerone.com/reports/284807) | Gratipay |  | - | 23 | 2017-10-31 | Array Index Underflow | i am The bug |
| [337986](https://hackerone.com/reports/337986) | Internet Bug Bounty | high | - | 23 | 2018-05-19 | Heap Overflow | CVE-2018-6797:  A crafted regular expression can cause a heap buffer write overflow in Perl 5 giving a remote attacker control over bytes written |
| [469997](https://hackerone.com/reports/469997) | Nintendo | none | - | 23 | 2025-06-27 | Stack Overflow | NEX: Stack overflow in UnicodeToUtf8 |
| [1240162](https://hackerone.com/reports/1240162) | HackerOne | medium | - | 23 | 2021-08-05 | Off-by-one Error | Mishandling of hackerone clear background checks resulting in disclosure of other hacker's information |
| [2819666](https://hackerone.com/reports/2819666) | curl | high | - | 23 | 2024-11-06 | Use of Externally-Controlled Format String | Exploitable Format String Vulnerability in curl_mfprintf Function |
| [3306456](https://hackerone.com/reports/3306456) | curl | medium | - | 23 | 2025-08-20 | Buffer Over-read | Curl parse_connect_to_string Heap-Overread Leading to Denial of Service via CURLOPT_CONNECT_TO |
| [3521639](https://hackerone.com/reports/3521639) | Nextcloud | low | - | 23 | 2026-09-05 | Integer Overflow | Improper Input Validation and Integer Overflow in timeamount parameter of files_retention app |
| [3638715](https://hackerone.com/reports/3638715) | curl | medium | - | 23 | 2026-03-31 | Use After Free | Use-After-Free race condition in url_move_hostname() via shared connection pool |
| [3766217](https://hackerone.com/reports/3766217) | MariaDB | medium | - | 23 | 2026-10-04 | Stack Overflow | libmariadb ( mariadb-connector-c ): stack overflow via server-controlled field->length in prepared-statement codec |
| [3782405](https://hackerone.com/reports/3782405) | MariaDB |  | - | 23 | 2026-09-15 | Stack Overflow | Stack Buffer-Overflow in MariaDB Charset_collation_map_st::insert_or_replace() |
| [3913007](https://hackerone.com/reports/3913007) | Nextcloud | none | - | 23 | 2026-10-18 | Buffer Over-read | SMTP header injection via C-escape `\r` in the recipient display name |
| [3973245](https://hackerone.com/reports/3973245) | curl |  | - | 23 | 2026-09-10 | Out-of-bounds Read | 55: Heap-buffer-overflow read in `curl_formadd_ccsid()` with binary form data |
| [241610](https://hackerone.com/reports/241610) | Internet Bug Bounty | medium | - | 22 | 2017-08-10 | Buffer Over-read | ap_find_token() Buffer Overread |
| [481532](https://hackerone.com/reports/481532) | PuTTY (European Commission - DIGIT) | low | - | 22 | 2019-11-03 | Use After Free | heap-use-after-free (READ of size 8) in main() |
| [792895](https://hackerone.com/reports/792895) | Revive Adserver | low | - | 22 | 2020-03-12 | Array Index Underflow | bypass old password with array in /admin/account-user-email.php |
| [1763817](https://hackerone.com/reports/1763817) | Node.js | medium | - | 22 | 2023-01-11 | Array Index Underflow | Take over subdomain undici.nodejs.org.cdn.cloudflare.net |
| [3774279](https://hackerone.com/reports/3774279) | curl | low | - | 22 | 2026-06-11 | Use After Free | heap-use-after-free in state.referer when CURLOPT_REFERER replaced or cleared after perform |
| [3824331](https://hackerone.com/reports/3824331) | Node.js | medium | - | 22 | 2026-10-23 | NULL Pointer Dereference | Null Dereference in X509ToObject |
| [458929](https://hackerone.com/reports/458929) | Valve | high | - | 21 | 2020-03-25 | Classic Buffer Overflow | Malformed BSP in GoldSrc Engine may cause shellcode injection |
| [2252307](https://hackerone.com/reports/2252307) | curl | critical | - | 21 | 2023-11-15 | Classic Buffer Overflow | Buffer overflow and affected url:-https://github.com/curl/curl/blob/master/docs/examples/hsts-preload.c |
| [3261310](https://hackerone.com/reports/3261310) | curl |  | - | 21 | 2025-07-28 | Use After Free | OpenSSL HTTP/3 bogus CURLINFO_TLS_SSL_PTR |
| [3516202](https://hackerone.com/reports/3516202) | curl | none | - | 21 | 2026-01-19 | Use After Free | Cookie Replacement Use-After-Free Vulnerability |
| [1913733](https://hackerone.com/reports/1913733) | curl | medium | - | 20 | 2023-05-24 | Use After Free | CVE-2023-28319: UAF in SSH sha256 fingerprint check |
| [2493548](https://hackerone.com/reports/2493548) | curl | critical | - | 20 | 2024-05-08 | Type Confusion | Incorrect Type Conversion in interpreting IPv4-mapped IPv6 addresses and below `curl` results in indeterminate SSRF vulnerabilities. |
| [3261248](https://hackerone.com/reports/3261248) | curl |  | - | 20 | 2025-07-23 | Type Confusion | GnuTLS CURLINFO_TLS_SESSION / CURLINFO_TLS_SSL_PTR type confusion |
| [3452725](https://hackerone.com/reports/3452725) | curl | high | - | 20 | 2025-12-05 | Use After Free | Title: Use-After-Free in cURL Test Suite via Improper Cleanup of Global Handle |
| [482200](https://hackerone.com/reports/482200) | PuTTY (European Commission - DIGIT) | low | - | 19 | 2019-11-03 | Heap Overflow | puttygen: heap-buffer-overflow in mp_get_decimal() |
| [3292590](https://hackerone.com/reports/3292590) | curl | high | - | 19 | 2025-08-09 | Buffer Over-read | Heap Buffer Overflow in Curl_memdup0() via CURLOPT_COPYPOSTFIELDS/CURLOPT_POSTFIELDSIZE Mismatch |
| [3302518](https://hackerone.com/reports/3302518) | curl | medium | - | 19 | 2025-08-18 | Use After Free | ## Title  Heap Use-After-Free Vulnerability in `curl` Leading to Potential Code Execution |
| [3445332](https://hackerone.com/reports/3445332) | Revive Adserver | low | - | 19 | 2026-01-14 | Use of Externally-Controlled Format String | INI Format string injection in Revive Adserver 6.0.4 settings |
| [3580247](https://hackerone.com/reports/3580247) | curl | none | - | 19 | 2026-03-03 | Use After Free | Use after free in hyperfifo example |
| [3723315](https://hackerone.com/reports/3723315) | Monero | medium | - | 19 | 2026-08-05 | Array Index Underflow | wallet-rpc describe_transfer uses real_output_in_tx_index instead of real_output: cold-wallet pre-sign review shows wrong ring member |
| [3824303](https://hackerone.com/reports/3824303) | curl | low | - | 19 | 2026-06-28 | Use After Free | UAF read in mev_pollset_diff() trace path after curl_easy_pause() in socket callback |
| [3913012](https://hackerone.com/reports/3913012) | Nextcloud | none | - | 19 | 2026-09-18 | Buffer Under-read | Persistent SMTP header injection via identity `organization` / `name` |
| [4689](https://hackerone.com/reports/4689) | Internet Bug Bounty |  | - | 18 | 2014-03-24 | Memory Corruption - Generic | SPDY memory corruption |
| [212241](https://hackerone.com/reports/212241) | Ruby | medium | - | 18 | 2017-09-22 | Memory Corruption - Generic | sprintf combined format string attack |
| [271355](https://hackerone.com/reports/271355) | Avito | critical | - | 18 | 2021-04-24 | Memory Corruption - Generic | [avito.ru] ImageMagick uninitialized image palette |
| [481335](https://hackerone.com/reports/481335) | Notepad++ | low | - | 18 | 2019-05-06 | Buffer Over-read | Security check failure or stack buffer overrun (crash) |
| [510887](https://hackerone.com/reports/510887) | Internet Bug Bounty | critical | - | 18 | 2019-09-25 | Heap Overflow | [CVE-2018-18312] regcomp: heap-buffer-overflow write / reg_node overrun |
| [789034](https://hackerone.com/reports/789034) | Internet Bug Bounty | high | - | 18 | 2021-07-28 | Classic Buffer Overflow | Buffer Overflow in ext_lm_group_acl helper |
| [980856](https://hackerone.com/reports/980856) | Brave Software | medium | - | 18 | 2020-12-16 | Array Index Underflow | https://publishers.basicattentiontoken.org/favicon.ico is Vulnerable to CVE-2017-7529 |
| [3337561](https://hackerone.com/reports/3337561) | curl | high | - | 18 | 2025-09-14 | Classic Buffer Overflow | Multiple Unsafe strcpy() Function Calls Leading to Potential Buffer Overflow Vulnerabilities in cURL 8.16.1-DEV |
| [3340109](https://hackerone.com/reports/3340109) | curl | high | - | 18 | 2025-09-16 | Stack Overflow | Stack Buffer Overflow in cURL Cookie Parsing Leads to RCE |
| [3399774](https://hackerone.com/reports/3399774) | curl |  | - | 18 | 2025-10-25 | Heap Overflow | Integer Overflow to Heap Overflow in DoH Response Handling |
| [3769676](https://hackerone.com/reports/3769676) | MariaDB | medium | - | 18 | 2026-09-03 | Stack Overflow | Stack Overflow DoS in ST_GeomFromGeoJSON Allows Any Authenticated User to Crash the Entire Server |
| [3896507](https://hackerone.com/reports/3896507) | MariaDB | medium | - | 18 | 2026-10-11 | Memory Corruption - Generic | Server crash (stack-overflow DoS) via unbounded recursion in MariaDB WKB GEOMETRYCOLLECTION parser |
| [317005](https://hackerone.com/reports/317005) | GSA Bounty | low | - | 17 | 2019-08-26 | Off-by-one Error | Subdomain Takeover due to unclaimed domain pointing to AWS |
| [440758](https://hackerone.com/reports/440758) | Valve | low | - | 17 | 2020-02-27 | Classic Buffer Overflow | Potential buffer overflow in demoplayer module of GoldSource Engine |
| [778610](https://hackerone.com/reports/778610) | Internet Bug Bounty | critical | - | 17 | 2021-08-26 | Classic Buffer Overflow | Squid as reverse proxy RCE and data leak |
| [2956023](https://hackerone.com/reports/2956023) | curl | low | - | 17 | 2025-02-05 | Integer Overflow to Buffer Overflow | CVE-2025-0725: gzip integer overflow |
| [3341476](https://hackerone.com/reports/3341476) | curl | low | - | 17 | 2025-09-18 | Integer Overflow | int overflow in krb5_read_data() leads to (possible) massive `recv()` write |
| [3470095](https://hackerone.com/reports/3470095) | curl | high | - | 17 | 2025-12-20 | Out-of-bounds Read | Heap Buffer Over-Read via Malicious SMB Server READ_ANDX Response |
| [3833629](https://hackerone.com/reports/3833629) | Node.js | high | - | 17 | 2026-08-28 | Use After Free | Re-entrant `nghttp2_session_mem_send()` during `nghttp2_session_mem_recv()` causes heap-use-after-free in Node.js HTTP/2 |
| [4033971](https://hackerone.com/reports/4033971) | curl | medium | - | 17 | 2026-09-19 | Use After Free | Use-after-free of the internal multi->admin easy handle via the documented CURLMOPT_NOTIFYFUNCTION callback |
| [550696](https://hackerone.com/reports/550696) | curl | low | - | 16 | 2019-05-31 | Heap Overflow | CVE-2019-5436: Heap Buffer Overflow at lib/tftp.c |
| [825091](https://hackerone.com/reports/825091) | Monero | high | - | 16 | 2021-10-11 | Array Index Underflow | Array Index Underflow--http rpc |
| [1289029](https://hackerone.com/reports/1289029) | Mail.ru |  | - | 16 |  | Memory Corruption - Generic | [185.30.178.57:8080] - Vulnerable to Jetleak |
| [1764858](https://hackerone.com/reports/1764858) | curl | low | - | 16 | 2022-12-26 | Use After Free | CVE-2022-43552: HTTP Proxy deny use-after-free |
| [3355213](https://hackerone.com/reports/3355213) | curl | medium | - | 16 | 2025-09-26 | Use After Free | Use-after-free when POST body buffer is freed before transfer |
| [3392174](https://hackerone.com/reports/3392174) | curl | high | - | 16 | 2025-10-21 | Classic Buffer Overflow | Buffer Overflow in WebSocket Handshake (lib/ws.c:1287) |
| [3480712](https://hackerone.com/reports/3480712) | curl | low | - | 16 | 2025-12-29 | Buffer Under-read | Telnet Suboption Buffer Pointer Underflow in lib/telnet.c leads to Out-of-Bounds Read |
| [3771139](https://hackerone.com/reports/3771139) | MariaDB |  | - | 16 | 2026-09-15 | Buffer Over-read | Heap Memory Disclosure via Integer Underflow in Item_func_json_arrayagg::cut_max_length in MariaDB Server |
| [3910393](https://hackerone.com/reports/3910393) | MariaDB |  | - | 16 | 2026-10-12 | Stack Overflow | Stack Buffer Overflow in MariaDB CONNECT storage engine when reading DOUBLE columns from TABLE_TYPE=DOS tables |
| [168485](https://hackerone.com/reports/168485) | IRCCloud |  | - | 15 | 2016-10-15 | Memory Corruption - Generic | Exposed, outdated nginx server (v1.4.6) potentially vulnerable to heap-based buffer overflow & RCE |
| [259390](https://hackerone.com/reports/259390) | Internet Bug Bounty | medium | - | 15 | 2017-09-16 | Use After Free | Use-after-free in XML::LibXML::Node::replaceChild |
| [641240](https://hackerone.com/reports/641240) | Internet Bug Bounty | high | - | 15 | 2021-08-26 | Heap Overflow | Basic Authentication Heap Overflow |
| [2990139](https://hackerone.com/reports/2990139) | curl | medium | - | 15 | 2025-02-20 | Use of Externally-Controlled Format String | Format string vulnerability, curl_msnprintf() function |
| [3264469](https://hackerone.com/reports/3264469) | curl |  | - | 15 | 2025-07-24 | Use After Free | Use after free (or assert triggered) with failed allocations in openssl |
| [3427460](https://hackerone.com/reports/3427460) | curl | low | - | 15 | 2025-11-15 | Incorrect Calculation of Buffer Size | Incorrect sizeof() in Rustls Backend Memory Allocation |
| [3462525](https://hackerone.com/reports/3462525) | curl | critical | - | 15 | 2025-12-12 | Stack Overflow | Buffer Overflow in cURL Internal printf Function |
| [3665363](https://hackerone.com/reports/3665363) | curl | none | - | 15 | 2026-04-11 | Integer Overflow | Integer Overflow/Signedness Mismatch in Printf Precision for HTTP/2 Trailer Headers |
| [4690](https://hackerone.com/reports/4690) | Internet Bug Bounty |  | - | 14 | 2014-03-24 | Memory Corruption - Generic | SPDY heap buffer overflow |
| [37240](https://hackerone.com/reports/37240) | Internet Bug Bounty |  | - | 14 | 2019-11-12 | Memory Corruption - Generic | Race condition in Flash workers may cause an exploitabl​e double free |
| [221833](https://hackerone.com/reports/221833) | Homebrew | medium | - | 14 | 2017-04-19 | Stack Overflow | [https://jenkins.brew.sh] Jenkins in Debug Mode with Stack Traces Enabled |
| [263663](https://hackerone.com/reports/263663) | Tor | critical | - | 14 | 2023-11-28 | Incorrect Calculation of Buffer Size | Zip bomb |
| [495789](https://hackerone.com/reports/495789) | Valve | medium | - | 14 | 2020-02-27 | Memory Corruption - Generic | Malformed .WAV triggers an Access Violation on GoldSRC (hl.exe) |
| [1269242](https://hackerone.com/reports/1269242) | curl | medium | - | 14 | 2021-09-15 | Double Free | CVE-2021-22945: UAF and double-free in MQTT sending |
| [3230082](https://hackerone.com/reports/3230082) | curl | high | - | 14 | 2025-06-30 | Stack Overflow | Stack-based Buffer Overflow in TELNET NEW_ENV Option Handling |
| [3418528](https://hackerone.com/reports/3418528) | curl | medium | - | 14 | 2025-11-10 | Classic Buffer Overflow | Unsafe use of strcpy in Curl_ldap_err2string (packages/OS400/os400sys.c) — stack-buffer-overflow (PoC + ASan) |
| [3444904](https://hackerone.com/reports/3444904) | curl | critical | - | 14 | 2025-12-01 | Heap Overflow | Heap Buffer Overflow in TFTP |
| [3484319](https://hackerone.com/reports/3484319) | curl | high | - | 14 | 2026-01-01 | Integer Overflow | MQTT Protocol Violation & Integer Overflow in libcurl |
| [3781201](https://hackerone.com/reports/3781201) | MariaDB | medium | - | 14 | 2026-10-07 | Integer Underflow | Pre-authentication `size_t` integer underflow → out-of-bounds read / server crash in MariaDB `caching_sha2_password` (auth_mysql_sha2) via an RSA-OAEP |
| [3856148](https://hackerone.com/reports/3856148) | MariaDB | critical | - | 14 | 2026-10-07 | Use After Free | Low-privilege RCE in MariaDB: SYS_REFCURSOR cursor-array use-after-free chained with an ST_Area heap over-read |
| [3916059](https://hackerone.com/reports/3916059) | curl | low | - | 14 | 2026-09-02 | Use After Free | CVE-2026-18924: HTTP/2 server push UAF |
| [144482](https://hackerone.com/reports/144482) | Ruby |  | - | 13 | 2016-06-21 | Memory Corruption - Generic | StringIO strio_getline() can divulge arbitrary memory |
| [193773](https://hackerone.com/reports/193773) | shopify-scripts | low | - | 13 | 2017-02-05 | Memory Corruption - Generic | SIGABRT - mrb_default_allocf |
| [340012](https://hackerone.com/reports/340012) | Monero | low | - | 13 | 2018-04-25 | Buffer Over-read | Buffer out of bound read in miniupnpc xml parser |
| [371135](https://hackerone.com/reports/371135) | Internet Bug Bounty | medium | - | 13 | 2018-09-01 | Use After Free | CVE-2018-12882: heap-use-after-free in PHP 7.2 through 7.2.6, possible 7.2.7 |
| [384214](https://hackerone.com/reports/384214) | Internet Bug Bounty | medium | - | 13 | 2018-09-01 | Heap Overflow | heap-buffer-overflow (READ of size 48) in exif_read_data() |
| [456727](https://hackerone.com/reports/456727) | Internet Bug Bounty | high | - | 13 | 2020-11-09 | Out-of-bounds Read | null pointer dereference in imap_mail |
| [1217702](https://hackerone.com/reports/1217702) | h1-ctf | critical | - | 13 | 2021-06-18 | Out-of-bounds Read | Adam and the  Deadly  Injections |
| [3617719](https://hackerone.com/reports/3617719) | curl | none | - | 13 | 2026-03-25 | Out-of-bounds Read | Function `do_pubkey()` can have out-of-bound read issue |
| [3760016](https://hackerone.com/reports/3760016) | Node.js | high | - | 13 | 2026-06-25 | Integer Overflow | Node.js WebCrypto AES Integer Overflow Leads to Remote Process Abort (DoS) |
| [3823985](https://hackerone.com/reports/3823985) | curl | low | - | 13 | 2026-06-28 | Use After Free | Use-after-free in `mev_forget_socket` when `curl_easy_pause()` is called from a `CURL_POLL_REMOVE` socket callback (incomplete fix of CVE-2026-9080) |
| [3833577](https://hackerone.com/reports/3833577) | curl |  | - | 13 | 2026-06-30 | Use After Free | heap-use-after-free in curl_easy_cleanup() called from callback |
| [57505](https://hackerone.com/reports/57505) | Shopify |  | - | 12 | 2015-10-15 | Memory Corruption - Generic | amazon aws s3 bucket content is public :-  http://shopify.com.s3.amazonaws.com/ |
| [112057](https://hackerone.com/reports/112057) | Internet Bug Bounty |  | - | 12 | 2019-10-14 | Memory Corruption - Generic | Heapoverflow in zipimporter module |
| [298246](https://hackerone.com/reports/298246) | Ruby | medium | - | 12 | 2018-03-30 | Buffer Under-read | controlled buffer under-read in pack_unpack_internal() |
| [824163](https://hackerone.com/reports/824163) | Internet Bug Bounty | high | - | 12 | 2021-08-26 | Buffer Over-read | Squid leaks previous content from reusable buffer |
| [1897203](https://hackerone.com/reports/1897203) | curl | low | - | 12 | 2023-03-20 | Double Free | CVE-2023-27537: HSTS double-free |
| [1906897](https://hackerone.com/reports/1906897) | Internet Bug Bounty | medium | - | 12 | 2023-03-18 | Use After Free | UAF in OpenSSL up to 3.0.7 |
| [3459636](https://hackerone.com/reports/3459636) | curl |  | - | 12 | 2025-12-09 | Stack Overflow | Stack Buffer Overflow in cURL wolfSSL Backend (lib/vtls/wolfssl.c) |
| [3479019](https://hackerone.com/reports/3479019) | curl | low | - | 12 | 2025-12-27 | Integer Overflow | Security hardening: missing integer overflow check in curl_load_library() |
| [3733934](https://hackerone.com/reports/3733934) | curl |  | - | 12 | 2026-05-18 | Use After Free | CURLOPT_HSTS_CTRL disables shared HSTS without share guard — use-after-free and double-free |
| [3771144](https://hackerone.com/reports/3771144) | MariaDB |  | - | 12 | 2026-09-14 | Use After Free | Use-After-Free in BTREE Index Traversal via Stale key_version in heap_update() in MariaDB Server |
| [261335](https://hackerone.com/reports/261335) | Internet Bug Bounty | medium | - | 11 | 2018-11-27 | Use After Free | Heap Use After Free Read in unserialize() |
| [268805](https://hackerone.com/reports/268805) | Internet Bug Bounty | high | - | 11 | 2019-10-08 | Buffer Over-read | CVE-2017-13008 The IEEE 802.11 parser in tcpdump before 4.9.2 has a buffer over-read in print-802_11.c:parse_elements(). |
| [274998](https://hackerone.com/reports/274998) | Tor |  | - | 11 | 2023-11-28 | Memory Corruption - Generic | Use of unitialized value in crypto_pk_num_bits (src/common/crypto.c:971) |
| [322935](https://hackerone.com/reports/322935) | Internet Bug Bounty | critical | - | 11 | 2019-09-26 | Off-by-one Error | Exim off-by-one RCE vulnerability |
| [344035](https://hackerone.com/reports/344035) | Internet Bug Bounty | medium | - | 11 | 2018-06-01 | Buffer Over-read | Heap Buffer Overflow (READ: 1786) in exif_iif_add_value |
| [684603](https://hackerone.com/reports/684603) | curl | medium | - | 11 | 2020-11-14 | Heap Overflow | CVE-2019-5482: Heap buffer overflow in TFTP when using small blksize |
| [1753224](https://hackerone.com/reports/1753224) | Internet Bug Bounty | low | - | 11 | 2022-12-03 | Stack Overflow | CVE-2022-35260: .netrc parser out-of-bounds access |
| [3101127](https://hackerone.com/reports/3101127) | curl | critical | - | 11 | 2025-06-28 | Memory Corruption - Generic | Buffer Overflow in curl MQTT Test Server (tests/server/mqttd.c) via Malicious CONNECT Packet |
| [3153971](https://hackerone.com/reports/3153971) | curl | medium | - | 11 | 2025-06-28 | Stack Overflow | Stack Buffer Overflow in curl's OpenSSL Provider Handling |
| [3476928](https://hackerone.com/reports/3476928) | curl | low | - | 11 | 2025-12-25 | Integer Overflow | Integer Overflow in `curl_easy_escape()` may lead to heap buffer overflow and stack memory disclosure on 32-bit platforms |
| [3575475](https://hackerone.com/reports/3575475) | curl | none | - | 11 | 2026-02-26 | Buffer Underflow | Curl Telnet Handler Buffer Overflow |
| [3771147](https://hackerone.com/reports/3771147) | MariaDB |  | - | 11 | 2026-09-15 | Classic Buffer Overflow | Stack Buffer Overflow via Crafted keyseg->start/ keyseg->length in .MYI File (MariaDB MyISAM) |
| [3973213](https://hackerone.com/reports/3973213) | curl |  | - | 11 | 2026-09-07 | Use After Free | 54: Rejected HTTP/2 push destroys MIME callback state still used by parent (use-after-free) |
| [4044441](https://hackerone.com/reports/4044441) | Weblate | low | - | 11 | 2026-10-30 | Use of Externally-Controlled Format String | Translation discovery crashes on crafted filenames (regex substitution injection) |
| [181319](https://hackerone.com/reports/181319) | shopify-scripts | high | - | 10 | 2016-12-16 | Memory Corruption - Generic | Memory disclosure in mruby String#lines method |
| [196498](https://hackerone.com/reports/196498) | shopify-scripts | low | - | 10 | 2017-02-05 | Memory Corruption - Generic | Segmentation fault on program counter |
| [218966](https://hackerone.com/reports/218966) | Dropbox |  | - | 10 |  | Classic Buffer Overflow | avrecode: global-buffer-overflow in get_neighbor() |
| [390499](https://hackerone.com/reports/390499) | Monero |  | - | 10 | 2018-09-28 | Stack Overflow | Stack Overflow in JSON RPC Server |
| [684567](https://hackerone.com/reports/684567) | Internet Bug Bounty | high | - | 10 | 2019-09-11 | Memory Corruption - Generic | Linux kernel: CVE-2017-7308: a signedness issue in AF_PACKET sockets |
| [721333](https://hackerone.com/reports/721333) | Internet Bug Bounty | medium | - | 10 | 2021-07-28 | Classic Buffer Overflow | Buffer Overflow in smblib.c |
| [888986](https://hackerone.com/reports/888986) | Internet Bug Bounty | medium | - | 10 | 2020-11-09 | Heap Overflow | [CVE-2020-10543] Buffer overflow caused by a crafted regular expression |
| [1261225](https://hackerone.com/reports/1261225) | Nextcloud | low | - | 10 | 2022-03-09 | Incorrect Calculation of Buffer Size | High memory usage for generating preview of broken image |
| [3229490](https://hackerone.com/reports/3229490) | curl | high | - | 10 | 2025-06-30 | Heap Overflow | Heap Buffer Overflow in libcurl curl_slist_append via Unterminated String |
| [3911968](https://hackerone.com/reports/3911968) | curl | medium | - | 10 | 2026-08-04 | Use After Free | Heap use-after-free (write) in mev_forget_socket() via reentrant curl_easy_pause() — incomplete fix for CVE-2026-9080 |
| [209949](https://hackerone.com/reports/209949) | Ruby |  | - | 9 | 2017-09-25 | Memory Corruption - Generic | Arbitrary heap exposure in JSON.generate |
| [260468](https://hackerone.com/reports/260468) | Legal Robot | none | - | 9 | 2017-09-05 | Incorrect Calculation of Buffer Size | first name and last name restrictions bypass |
| [268320](https://hackerone.com/reports/268320) | Tor | low | - | 9 | 2023-11-28 | Array Index Underflow | solving TOR vulnerability, in other to make bruteforce difficult |
| [395531](https://hackerone.com/reports/395531) | Kaspersky | medium | - | 9 | 2018-08-15 | Heap Overflow | test report |
| [511317](https://hackerone.com/reports/511317) | Monero | low | - | 9 | 2019-05-10 | Use After Free | Potential use-after-free due to struct array_entry_t lacking an explicit copy constructor |
| [684573](https://hackerone.com/reports/684573) | Internet Bug Bounty | high | - | 9 | 2019-09-11 | Memory Corruption - Generic | Linux kernel: CVE-2017-1000112: a memory corruption due to UFO to non-UFO path switch |
| [751904](https://hackerone.com/reports/751904) | Eternal | none | - | 9 | 2019-12-05 | Heap Overflow | Zomato Map server going out of memory while resizing map image |
| [3156384](https://hackerone.com/reports/3156384) | curl | medium | - | 9 | 2025-07-01 | Heap Overflow | Heap buffer overflow vulnerability in conncache.c: incorrect use of pointer arrays resulting in out-of-bounds memory writes. |
| [3395666](https://hackerone.com/reports/3395666) | curl | low | - | 9 | 2025-10-28 | Heap Overflow | libcurl MQTT PUBLISH length overflow (heap overflow) |
| [3470073](https://hackerone.com/reports/3470073) | curl | medium | - | 9 | 2025-12-25 | Out-of-bounds Read | Heap Buffer Over-Read via Malicious SMB Server READ_ANDX Response |
| [3897588](https://hackerone.com/reports/3897588) | MariaDB |  | - | 9 | 2026-09-07 | Incorrect Calculation of Buffer Size | KILL authorization trusts the presented login name instead of the authenticated anonymous account |
| [4030333](https://hackerone.com/reports/4030333) | curl | high | - | 9 | 2026-10-14 | Use After Free | CVE-2026-92392: HTTP/2 upload Use-After-Free |
| [4135291](https://hackerone.com/reports/4135291) | curl | low | - | 9 | 2026-10-23 | Use After Free | Heap-use-after-free in libcurl's multi event machinery (curl_multi_remove_handle() from a socket callback nested under a notify callback) |
| [1356](https://hackerone.com/reports/1356) | Internet Bug Bounty |  | - | 8 | 2014-02-06 | Memory Corruption - Generic | PHP Heap Overflow Vulnerability in imagecrop() |
| [152266](https://hackerone.com/reports/152266) | Internet Bug Bounty |  | - | 8 | 2019-10-13 | Memory Corruption - Generic | Use After Free Vulnerability in SNMP with GC and unserialize() |
| [192578](https://hackerone.com/reports/192578) | shopify-scripts | low | - | 8 | 2017-03-09 | Memory Corruption - Generic | kh_get_n2s() stack overrun |
| [229511](https://hackerone.com/reports/229511) | Weblate | low | - | 8 | 2017-06-02 | Memory Corruption - Generic | No Rate Limiting at /contact |
| [240659](https://hackerone.com/reports/240659) | Stellar.org |  | - | 8 | 2017-06-30 | Heap Overflow | heap-buffer-overflow (READ of size 1) in cpptoml::parser::consume_whitespace() |
| [257376](https://hackerone.com/reports/257376) | Weblate | none | - | 8 | 2017-09-16 | Memory Corruption - Generic | Missing Restriction On String Size |
| [347282](https://hackerone.com/reports/347282) | Internet Bug Bounty | high | - | 8 | 2019-08-27 | Double Free | Linux kernel: CVE-2017-6074: DCCP double-free vulnerability |
| [363850](https://hackerone.com/reports/363850) | Liberapay | none | - | 8 | 2018-07-05 | Classic Buffer Overflow | Improper Data Validation / Unvalidated Input |
| [365968](https://hackerone.com/reports/365968) | Node.js | critical | - | 8 | 2018-07-15 | Array Index Underflow | Your page has 2 blocking CSS resources. This causes a delay in rendering your page. |
| [497255](https://hackerone.com/reports/497255) | Notepad++ | low | - | 8 | 2019-05-07 | Stack Overflow | A stack buffer overflow in BabyGrid.cpp can lead to program crashes via a malicious localization file |
| [2621057](https://hackerone.com/reports/2621057) | Internet Bug Bounty | medium | - | 8 | 2024-08-23 | Memory Corruption - Generic | libcurl: freeing stack buffer during x509 certificate parsing |
| [3037326](https://hackerone.com/reports/3037326) | curl |  | - | 8 | 2025-06-28 | Use After Free | Free of uninitialized pointer in doh_decode_rdata_name() |
| [3037583](https://hackerone.com/reports/3037583) | curl |  | - | 8 | 2025-06-30 | Integer Overflow | Buffer Overflow in curl's Rustls Backend |
| [3045390](https://hackerone.com/reports/3045390) | curl | none | - | 8 | 2025-06-30 | Double Free | Double free caused by mqtt_doing() |
| [3404025](https://hackerone.com/reports/3404025) | curl | medium | - | 8 | 2025-10-31 | Heap Overflow | SOCKS5 Heap Buffer Overflow via Malicious HTTP Redirect with Oversized Hostname |
| [3406123](https://hackerone.com/reports/3406123) | curl |  | - | 8 | 2025-10-31 | Buffer Over-read | Buffer over-read,, Missing NUL termination in addvariable() causes undefined behavior |
| [3417428](https://hackerone.com/reports/3417428) | curl | medium | - | 8 | 2025-11-10 | Integer Overflow | libcurl MQTT `CURLOPT_POSTFIELDSIZE_LARGE` overflow leads to immediate DoS |
| [3427343](https://hackerone.com/reports/3427343) | curl | medium | - | 8 | 2025-11-15 | Off-by-one Error | Off-by-One Buffer Overflow in SMB Path Handler |
| [3466883](https://hackerone.com/reports/3466883) | curl | medium | - | 8 | 2025-12-16 | Stack Overflow | Curl Alt-Svc Parser Stack Buffer Overflow |
| [3466896](https://hackerone.com/reports/3466896) | curl | medium | - | 8 | 2025-12-16 | Heap Overflow | Heap Overflow in cURL AmigaOS Socket Implementation |
| [3480078](https://hackerone.com/reports/3480078) | curl | high | - | 8 | 2025-12-28 | Buffer Over-read | Heap Buffer Over-read in lib/http2.c (on_header) handling PUSH_PROMISE frames |
| [3493602](https://hackerone.com/reports/3493602) | curl | high | - | 8 | 2026-01-08 | Classic Buffer Overflow | Stack Buffer Overflow in mprintf.c formatting function (fallback path) |
| [3508701](https://hackerone.com/reports/3508701) | curl |  | - | 8 | 2026-01-14 | Use After Free | Use-After-Free in curl_easy_nextheader when reusing header handle across requests |
| [3682666](https://hackerone.com/reports/3682666) | curl | high | - | 8 | 2026-04-29 | Use After Free | Use-after-free in `curl_easy_ssls_export()` during callback re-entrancy |
| [4122039](https://hackerone.com/reports/4122039) | curl | critical | - | 8 | 2026-10-19 | Use After Free | libcurl shared-HSTS-cache race leads to use-after-free with attacker-controlled function-pointer call |
| [4123749](https://hackerone.com/reports/4123749) | curl | none | - | 8 | 2026-10-19 | Use After Free | WebSocket decoder use-after-free when curl_easy_pause() unpauses from a debug callback |
| [115702](https://hackerone.com/reports/115702) | Tor |  | - | 7 | 2017-10-19 | Memory Corruption - Generic | [tor] libevent dns OOB read |
| [152231](https://hackerone.com/reports/152231) | Internet Bug Bounty |  | - | 7 | 2016-08-30 | Memory Corruption - Generic | Out of bound read in exif_process_IFD_in_MAKERNOTE |
| [192127](https://hackerone.com/reports/192127) | Ruby |  | - | 7 | 2017-03-05 | Memory Corruption - Generic | Buffer underflow in sprintf |
| [207983](https://hackerone.com/reports/207983) | Internet Bug Bounty | medium | - | 7 | 2017-05-28 | Heap Overflow | read outside of buffer (heap buffer overflow) in S_regmatch - regexec.c:6057 |
| [209937](https://hackerone.com/reports/209937) | shopify-scripts |  | - | 7 | 2017-05-13 | Memory Corruption - Generic | SIGSEGV - mark_context_stack |
| [214000](https://hackerone.com/reports/214000) | shopify-scripts |  | - | 7 | 2017-05-13 | Memory Corruption - Generic | SIGABRT - mirb and mruby |
| [223454](https://hackerone.com/reports/223454) | Weblate | low | - | 7 | 2017-05-18 | Memory Corruption - Generic | Missing restriction on string size of Full Name at https://demo.weblate.org/accounts/register/ |
| [259555](https://hackerone.com/reports/259555) | Internet Bug Bounty | low | - | 7 | 2018-05-07 | Heap Overflow | heap-buffer-overflow (WRITE of size 8) in Perl_pp_reverse() |
| [261336](https://hackerone.com/reports/261336) | Internet Bug Bounty | medium | - | 7 | 2018-11-27 | Buffer Over-read | Out of Bounds Memory Read in unserialize() |
| [261338](https://hackerone.com/reports/261338) | Internet Bug Bounty | medium | - | 7 | 2018-11-27 | Use After Free | Heap Use After Free in unserialize() |
| [268804](https://hackerone.com/reports/268804) | Internet Bug Bounty | high | - | 7 | 2019-10-08 | Buffer Over-read | CVE-2017-12986 The IPv6 routing header parser in tcpdump before 4.9.2 has a buffer over-read in print-rt6.c:rt6_print(). |
| [311884](https://hackerone.com/reports/311884) | Ubiquiti Inc. | high | - | 7 | 2018-06-19 | Use of Externally-Controlled Format String | Format String Vulnerability in the EdgeSwitch restricted CLI |
| [475499](https://hackerone.com/reports/475499) | Internet Bug Bounty | critical | - | 7 | 2020-10-10 | Buffer Over-read | heap buffer overflow in phar_detect_phar_fname_ext |
| [510888](https://hackerone.com/reports/510888) | Internet Bug Bounty | critical | - | 7 | 2019-09-25 | Heap Overflow | [CVE-2018-18313] regcomp: heap-buffer-overflow read in S_grok_bslash_N |
| [709072](https://hackerone.com/reports/709072) | U.S. Dept Of Defense | high | - | 7 | 2020-05-14 | Improper Null Termination | Null byte Injection in https://████/ |
| [724217](https://hackerone.com/reports/724217) | Internet Bug Bounty | critical | - | 7 | 2020-02-13 | Buffer Underflow | tcpdump: CVE-2018-14879 - buffer overflow in tcpdump.c:get_next_file() |
| [800324](https://hackerone.com/reports/800324) | Internet Bug Bounty | critical | - | 7 | 2021-08-22 | Classic Buffer Overflow | Several protocol parsers in before 4.9.2 could cause a buffer overflow in util-print.c:bittok2str_internal() |
| [802846](https://hackerone.com/reports/802846) | Internet Bug Bounty | high | - | 7 | 2021-08-22 | Buffer Over-read | The VTP parser in tcpdump before 4.9.2 has a buffer over-read in print-vtp.c:vtp_print() |
| [987090](https://hackerone.com/reports/987090) | U.S. Dept Of Defense | critical | - | 7 | 2020-10-16 | Array Index Underflow | https://██████ vulnerable to CVE-2020-3187 - Unauthenticated arbitrary file deletion in Cisco ASA/FTD |
| [1721098](https://hackerone.com/reports/1721098) | curl | low | - | 7 | 2022-10-27 | Out-of-bounds Read | CVE-2022-35260: .netrc parser out-of-bounds access |
| [1722065](https://hackerone.com/reports/1722065) | curl | medium | - | 7 | 2022-11-26 | Double Free | CVE-2022-42915: HTTP proxy double-free |
| [2509402](https://hackerone.com/reports/2509402) | U.S. Dept Of Defense |  | - | 7 | 2024-06-18 | Out-of-bounds Read | Out-Of-Bounds Memory Read on ███ |
| [2552179](https://hackerone.com/reports/2552179) | curl | low | - | 7 | 2024-06-18 | Type Confusion | Incorrect Encoding Conversion in hostname  results in indeterminate SSRF vulnerabilities |
| [3508321](https://hackerone.com/reports/3508321) | curl | low | - | 7 | 2026-01-14 | Buffer Over-read | Integer-underflow leads to heap over-read in TFTP implementation |
| [3531737](https://hackerone.com/reports/3531737) | Node.js | medium | - | 7 | 2026-03-30 | Missing Release of Memory after Effective Lifetime | Memory leak in Node.js HTTP/2 server via WINDOW_UPDATE on stream 0 leads to resource exhaustion |
| [3684614](https://hackerone.com/reports/3684614) | curl | high | - | 7 | 2026-04-29 | Out-of-bounds Read | Heap-buffer-overflow in `Curl_ssl_push_certinfo_len()` — sole bounds check is `DEBUGASSERT` |
| [3871977](https://hackerone.com/reports/3871977) | MariaDB | medium | - | 7 | 2026-10-12 | Memory Corruption - Generic | Connector/ODBC: malicious server's long version string wraps size_t PrefixLen via negative _snprintf return, causing heap out-of-bounds write |
| [3920633](https://hackerone.com/reports/3920633) | MariaDB | medium | - | 7 | 2026-11-04 | Out-of-bounds Read | Connector/ODBC: SqlwcsOctetLen sizes UTF-16 with a byte-oriented helper, reading past the caller's buffer and sending client memory to the server |
| [3971462](https://hackerone.com/reports/3971462) | curl | low | - | 7 | 2026-09-14 | Memory Corruption - Generic | Heap-use-after-free in CURLOPT_REFERER when passed a CURLINFO_REFERER pointer |
| [4024268](https://hackerone.com/reports/4024268) | curl | none | - | 7 | 2026-09-15 | Memory Corruption - Generic | Out-of-bounds read in curl_formadd when CURLFORM_NAMELENGTH is explicitly 0 |
| [4099194](https://hackerone.com/reports/4099194) | curl | low | - | 7 | 2026-10-14 | Buffer Over-read | CVE-2026-107928: info leak uploading over WebSockets with GnuTLS |
| [5466](https://hackerone.com/reports/5466) | MS-DOS |  | - | 6 | 2014-04-01 | Memory Corruption - Generic | Bug in Source Code Files(v1.1) |
| [99686](https://hackerone.com/reports/99686) | Mail.ru |  | - | 6 |  | Memory Corruption - Generic | [w1.dwar.ru] Core Dump |
| [112386](https://hackerone.com/reports/112386) | Tor |  | - | 6 | 2017-10-19 | Memory Corruption - Generic | smartlist_add, smartlist_insert (may) cause heap corruption as a result of inadequate checks in smartlist_ensure_capacity |
| [112632](https://hackerone.com/reports/112632) | Tor |  | - | 6 | 2017-10-19 | Memory Corruption - Generic | [tor] libevent dns remote stack overread vulnerability |
| [112784](https://hackerone.com/reports/112784) | Tor |  | - | 6 | 2017-10-19 | Memory Corruption - Generic | libevent (stack) buffer overflow in evutil_parse_sockaddr_port |
| [126598](https://hackerone.com/reports/126598) | Tor |  | - | 6 | 2017-10-19 | Memory Corruption - Generic | Overreads/overcopies in torsocks |
| [138025](https://hackerone.com/reports/138025) | Tor |  | - | 6 | 2017-10-19 | Memory Corruption - Generic | Heap corruption via memarea.c |
| [140865](https://hackerone.com/reports/140865) | Internet Bug Bounty |  | - | 6 | 2019-10-13 | Memory Corruption - Generic | Integer Overflow in php_html_entities() |
| [146185](https://hackerone.com/reports/146185) | Internet Bug Bounty |  | - | 6 | 2019-10-13 | Memory Corruption - Generic | Integer Overflow in Length of String-typed ZVAL |
| [163459](https://hackerone.com/reports/163459) | Tor |  | - | 6 | 2017-10-19 | Memory Corruption - Generic | potential memory corruption in or/buffers.c (particularly on 32 bit) |
| [167888](https://hackerone.com/reports/167888) | Internet Bug Bounty |  | - | 6 | 2019-11-12 | Memory Corruption - Generic | Uninitialized Thumbail Data Leads To Memory Leakage in exif_process_IFD_in_TIFF |
| [175230](https://hackerone.com/reports/175230) | Internet Bug Bounty |  | - | 6 | 2016-12-30 | Memory Corruption - Generic | Double-free in X509 parsing |
| [182140](https://hackerone.com/reports/182140) | Internet Bug Bounty | medium | - | 6 | 2019-10-04 | Memory Corruption - Generic | libtiff 4.0.6 segfault / read outside of buffer (CVE-2016-9297) |
| [193517](https://hackerone.com/reports/193517) | shopify-scripts | high | - | 6 | 2017-02-07 | Memory Corruption - Generic | attempting double-free using the mruby compiler `mrbc` |
| [214845](https://hackerone.com/reports/214845) | shopify-scripts |  | - | 6 | 2017-05-13 | NULL Pointer Dereference | SIGSEGV in mrb_vm_exec |
| [215967](https://hackerone.com/reports/215967) | shopify-scripts |  | - | 6 | 2017-05-13 | Memory Corruption - Generic | SIGABRT in mrb_debug_info_append_file |
| [216725](https://hackerone.com/reports/216725) | shopify-scripts |  | - | 6 | 2017-05-13 | Memory Corruption - Generic | SIGABRT - in free |
| [233440](https://hackerone.com/reports/233440) | Internet Bug Bounty | low | - | 6 | 2017-06-05 | Heap Overflow | heap-buffer-overflow (READ of size 61) in Perl_re_intuit_start() |
| [237125](https://hackerone.com/reports/237125) | Mixmax | low | - | 6 | 2017-07-16 | Memory Corruption - Generic | no string size restriction on team name |
| [245956](https://hackerone.com/reports/245956) | Internet Bug Bounty | medium | - | 6 | 2019-10-13 | Use After Free | Use-after-free in PHP7's unserialize() |
| [284951](https://hackerone.com/reports/284951) | Monero | low | - | 6 | 2018-04-25 | Out-of-bounds Read | Out-of-bounds read when importing corrupt blockchain with monero-blockchain-import |
| [296991](https://hackerone.com/reports/296991) | Internet Bug Bounty | critical | - | 6 | 2019-11-12 | Use After Free | Exim use-after-free vulnerability while reading mail header involving BDAT commands |
| [335533](https://hackerone.com/reports/335533) | Node.js | high | - | 6 | 2020-02-13 | Memory Corruption - Generic | HTTP/2 Denial of Service Vulnerability |
| [356763](https://hackerone.com/reports/356763) | Open-Xchange |  | - | 6 |  | Classic Buffer Overflow | Buffer overflow in sha3 |
| [510025](https://hackerone.com/reports/510025) | Internet Bug Bounty | high | - | 6 | 2020-10-10 | Buffer Over-read | Invalid Read on exif_process_SOFn |
| [686823](https://hackerone.com/reports/686823) | curl | medium | - | 6 | 2020-11-14 | Double Free | CVE-2019-5481: krb5: double-free in read_data() after realloc() fail |
| [876257](https://hackerone.com/reports/876257) | Stripo Inc | medium | - | 6 | 2020-07-13 | Integer Overflow | Integer Overflow (CVE_2017_7529) |
| [1455248](https://hackerone.com/reports/1455248) | Internet Bug Bounty | medium | - | 6 | 2022-01-22 | Classic Buffer Overflow | Buffer Overflow in optimized_escape_html method |
| [1511619](https://hackerone.com/reports/1511619) | Internet Bug Bounty | high | - | 6 | 2022-04-14 | Heap Overflow | Read and write beyond bounds in mod_sed |
| [3872248](https://hackerone.com/reports/3872248) | MariaDB | medium | - | 6 | 2026-10-12 | Out-of-bounds Read | Connector/C++: heap out-of-bounds read when malicious server field length exceeds declared column length in binary result path |
| [3896684](https://hackerone.com/reports/3896684) | MariaDB |  | - | 6 | 2026-11-04 | Out-of-bounds Read | Connector/C Out-of-bounds read from unterminated GSSAPI SPN in `parse_server_packet()` |
| [3909248](https://hackerone.com/reports/3909248) | MariaDB | medium | - | 6 | 2026-09-07 | Heap Overflow | MariaDB: heap buffer overflow in ha_tina::chain_append() lets a low-privileged user crash the server via CSV row deletion |
| [3915935](https://hackerone.com/reports/3915935) | MariaDB | high | - | 6 | 2026-10-07 | Use After Free | Heap Use-After-Free in Materialized_cursor::open via SYS_REFCURSOR Array Reallocation |
| [3920647](https://hackerone.com/reports/3920647) | MariaDB | medium | - | 6 | 2026-11-04 | Out-of-bounds Read | Connector/ODBC: MADB_Stmt::ArrayOffset is not reset when an exception unwinds out of MADB_StmtExecute, so the next paramset reads out of bounds |
| [4033108](https://hackerone.com/reports/4033108) | curl |  | - | 6 | 2026-10-14 | Use After Free | Retry-independent time-condition HTTP/2 UAF |
| [4085412](https://hackerone.com/reports/4085412) | curl | medium | - | 6 | 2026-10-05 | Out-of-bounds Read | Rustls backend discloses out-of-bounds heap data during legal IMAP upload cancellation |
| [4166602](https://hackerone.com/reports/4166602) | curl | low | - | 6 | 2026-11-03 | Use After Free | Re-entrant curl_easy_pause UAF in cw-pause |
| [2170](https://hackerone.com/reports/2170) | Internet Bug Bounty |  | - | 5 | 2014-02-27 | Memory Corruption - Generic | Flash double free vulnerability leads to code execution |
| [19532](https://hackerone.com/reports/19532) | Uzbey |  | - | 5 | 2014-08-22 | Memory Corruption - Generic | Missing "size check" on files to upload could make memory leaks. |
| [47227](https://hackerone.com/reports/47227) | Internet Bug Bounty |  | - | 5 | 2015-03-25 | Memory Corruption - Generic | Race condition in workers may cause an exploitable double free by abusing bytearray.compress() |
| [119033](https://hackerone.com/reports/119033) | Cakebet |  | - | 5 | 2016-03-28 | Memory Corruption - Generic | Sender policy framework (SPF) records evaluation return (Too many DNS lookups) error |
| [123091](https://hackerone.com/reports/123091) | New Relic |  | - | 5 |  | Memory Corruption - Generic | No Rate Limitation on Promo Code |
| [142472](https://hackerone.com/reports/142472) | Internet Bug Bounty |  | - | 5 | 2016-09-20 | Memory Corruption - Generic | CVE-2016-2177 Undefined pointer arithmetic in SSL code |
| [146182](https://hackerone.com/reports/146182) | Internet Bug Bounty |  | - | 5 | 2019-10-13 | Memory Corruption - Generic | Integer Overflow/Heap Overflow in json_encode()/json_decode() |
| [146184](https://hackerone.com/reports/146184) | Internet Bug Bounty |  | - | 5 | 2019-10-13 | Memory Corruption - Generic | Integer Overflow in addcslashes()/addslashes() |
| [155223](https://hackerone.com/reports/155223) | Internet Bug Bounty |  | - | 5 | 2019-10-13 | Memory Corruption - Generic | Use After Free Vulnerability in array_walk()/array_walk_recursive() |
| [170618](https://hackerone.com/reports/170618) | Internet Bug Bounty |  | - | 5 | 2020-10-10 | Memory Corruption - Generic | CVE-2016-7418 PHP Out-Of-Bounds Read in php_wddx_push_element |
| [172403](https://hackerone.com/reports/172403) | Internet Bug Bounty | low | - | 5 | 2019-10-13 | Memory Corruption - Generic | Python 2.7 32-bit JSON encoding heap corruption |
| [175982](https://hackerone.com/reports/175982) | Internet Bug Bounty | medium | - | 5 | 2019-10-13 | Memory Corruption - Generic | Use-after-free in unserialize() |
| [182089](https://hackerone.com/reports/182089) | Pushwoosh | low | - | 5 | 2016-11-22 | Memory Corruption - Generic | Spam Some one using (user.saveInvite) system |
| [182474](https://hackerone.com/reports/182474) | Internet Bug Bounty | medium | - | 5 | 2019-10-13 | Memory Corruption - Generic | Use After Free in PHP7 unserialize() |
| [183239](https://hackerone.com/reports/183239) | shopify-scripts | high | - | 5 | 2016-12-17 | Memory Corruption - Generic | SIGSEGV on mruby's mark_tbl() (Invalid memory access) |
| [202965](https://hackerone.com/reports/202965) | Internet Bug Bounty | high | - | 5 | 2019-10-08 | Memory Corruption - Generic | CVE-2017-5341 The OTV parser in tcpdump before 4.9.0 has a buffer overflow in print-otv.c:otv_print() |
| [202967](https://hackerone.com/reports/202967) | Internet Bug Bounty | high | - | 5 | 2019-10-08 | Memory Corruption - Generic | CVE-2017-5484 The ATM parser in tcpdump before 4.9.0 has a buffer overflow in print-atm.c:sig_print() |
| [205284](https://hackerone.com/reports/205284) | shopify-scripts |  | - | 5 | 2017-03-29 | Memory Corruption - Generic | SIGABRT - method_missing - mark_context_stack |
| [212931](https://hackerone.com/reports/212931) | Internet Bug Bounty | high | - | 5 | 2018-05-16 | Memory Corruption - Generic | heap-buffer-overflow (buffer read overrun) in curl: ourWriteOut() src/tool_writeout.c:115 |
| [213255](https://hackerone.com/reports/213255) | shopify-scripts |  | - | 5 | 2017-04-27 | Memory Corruption - Generic | SIGSEGV in str_buf_cat |
| [214449](https://hackerone.com/reports/214449) | Gratipay | high | - | 5 | 2017-03-20 | Heap Overflow | Content-Length restriction bypass to heap overflow in gip.rocks. |
| [214576](https://hackerone.com/reports/214576) | shopify-scripts |  | - | 5 | 2017-05-13 | Double Free | SIGABRT - mirb - Double Free |
| [215447](https://hackerone.com/reports/215447) | shopify-scripts |  | - | 5 | 2017-05-13 | NULL Pointer Dereference | SIGSEGV in mrb_class |
| [221287](https://hackerone.com/reports/221287) | LibSass | high | - | 5 | 2017-06-08 | NULL Pointer Dereference | null pointer dereference in Sass::Eval::operator()(Sass::Map*) |
| [221785](https://hackerone.com/reports/221785) | Internet Bug Bounty | low | - | 5 | 2017-05-25 | Heap Overflow | OOB write in MDC2_Update() (CVE-2016-6303) |
| [221788](https://hackerone.com/reports/221788) | Internet Bug Bounty | low | - | 5 | 2017-05-25 | Heap Overflow | OOB write in BN_bn2dec() (CVE-2016-2182) |
| [221789](https://hackerone.com/reports/221789) | Internet Bug Bounty | low | - | 5 | 2017-05-25 | Out-of-bounds Read | OOB read in TS_OBJ_print_bio() (CVE-2016-2180) |
| [221790](https://hackerone.com/reports/221790) | Internet Bug Bounty | low | - | 5 | 2017-05-25 | Out-of-bounds Read | Certificate message OOB reads (CVE-2016-6306) |
| [232150](https://hackerone.com/reports/232150) | Internet Bug Bounty | low | - | 5 | 2017-05-28 | Heap Overflow | heap-buffer-overflow (READ of size 11) in Perl 5.25.x |
| [247028](https://hackerone.com/reports/247028) | Internet Bug Bounty | high | - | 5 | 2019-10-14 | Use After Free | CVE-2017-10966: Heap-use-after-free in Irssi <1.0.4 |
| [255587](https://hackerone.com/reports/255587) | Internet Bug Bounty | medium | - | 5 | 2018-05-16 | Buffer Over-read | CVE-2017-1000101: cURL: URL globbing out of bounds read |
| [321686](https://hackerone.com/reports/321686) | Node.js third-party modules | medium | - | 5 | 2018-04-08 | Out-of-bounds Read | `atob` allocates uninitialized Buffers when number is passed in input on Node.js 4.x and below |
| [321692](https://hackerone.com/reports/321692) | Node.js third-party modules | high | - | 5 | 2018-05-12 | Out-of-bounds Read | `base64-url` below 2.0 allocates uninitialized Buffers when number is passed in input |
| [321704](https://hackerone.com/reports/321704) | Node.js third-party modules | low | - | 5 | 2018-06-14 | Out-of-bounds Read | `njwt` allocates uninitialized Buffers when number is passed in base64urlEncode input |
| [674540](https://hackerone.com/reports/674540) | Internet Bug Bounty | medium | - | 5 | 2019-11-07 | Classic Buffer Overflow | mod_remoteip stack buffer overflow and NULL pointer dereference |
| [1209681](https://hackerone.com/reports/1209681) | Node.js | medium | - | 5 | 2021-07-05 | Buffer Over-read | OOB read in libuv |
| [1595296](https://hackerone.com/reports/1595296) | Internet Bug Bounty | low | - | 5 | 2022-07-09 | Buffer Over-read | Read beyond bounds in mod_isapi.c [zhbug_httpd_41] |
| [3431180](https://hackerone.com/reports/3431180) | curl |  | - | 5 | 2025-11-18 | Double Free | Double free in tool_ssls_load() |
| [3506159](https://hackerone.com/reports/3506159) | curl | high | - | 5 | 2026-01-10 | Out-of-bounds Read | Heap Out-of-Bounds Read in lib/http2.c via Malformed PUSH_PROMISE Headers |
| [3508500](https://hackerone.com/reports/3508500) | curl | high | - | 5 | 2026-01-13 | Integer Overflow | integer Overflow in MQTT Protocol Handling Allows Bypassing Message Size Limit |
| [3736234](https://hackerone.com/reports/3736234) | curl | none | - | 5 | 2026-05-17 | NULL Pointer Dereference | NULL pointer dereference in libcurl URL API redirect_url() with CURLU_DEFAULT_SCHEME |
| [3751697](https://hackerone.com/reports/3751697) | curl | low | - | 5 | 2026-06-24 | Buffer Over-read | CVE-2026-10536: HTTP/2 stream-dependency tree UAF |
| [3751701](https://hackerone.com/reports/3751701) | curl | none | - | 5 | 2026-06-01 | Use After Free | Use-after-free in `curl_easy_duphandle()` with HTTP/2 stream-dependency tree |
| [3973219](https://hackerone.com/reports/3973219) | curl |  | - | 5 | 2026-09-07 | Out-of-bounds Read | 57: Heap out-of-bounds read in `curl_easy_escape_ccsid()` / `curl_easy_unescape_ccsid()` |
| [6389](https://hackerone.com/reports/6389) | Internet Bug Bounty |  | - | 4 | 2014-03-31 | Memory Corruption - Generic | Integer overflow in strop.expandtabs |
| [7941](https://hackerone.com/reports/7941) | Localize |  | - | 4 | 2014-04-22 | Memory Corruption - Generic | A Serious Bug on SIGNUP Process! |
| [55029](https://hackerone.com/reports/55029) | Internet Bug Bounty |  | - | 4 | 2015-02-27 | Memory Corruption - Generic | Use after free vulnerability in unserialize() with DateTimeZone |
| [73246](https://hackerone.com/reports/73246) | Internet Bug Bounty |  | - | 4 | 2015-04-14 | Memory Corruption - Generic | Use-after-free in php_curl related to CURLOPT_FILE/_INFILE/_WRITEHEADER |
| [73491](https://hackerone.com/reports/73491) | Ubiquiti Inc. |  | - | 4 | 2016-04-01 | Memory Corruption - Generic | Buffer Overflow in PHP of the AirMax Products |
| [74004](https://hackerone.com/reports/74004) | Ubiquiti Inc. |  | - | 4 | 2016-04-07 | Memory Corruption - Generic | Other Buffer Overflow in PHP of the AirMax Products |
| [83803](https://hackerone.com/reports/83803) | ownCloud |  | - | 4 | 2015-09-11 | Memory Corruption - Generic | apps.owncloud.com: SSL Server Allows Anonymous Authentication Vulnerability (SMTP) |
| [124737](https://hackerone.com/reports/124737) | Internet Bug Bounty |  | - | 4 | 2019-10-13 | Memory Corruption - Generic | Multiple Heap Overflows in php_raw_url_encode/php_url_encode |
| [126416](https://hackerone.com/reports/126416) | Internet Bug Bounty |  | - | 4 | 2019-10-13 | Memory Corruption - Generic | Integer Overflow in php_raw_url_encode |
| [145458](https://hackerone.com/reports/145458) | Nextcloud |  | - | 4 | 2016-07-17 | Memory Corruption - Generic | nextcloud.com: Mail Bombing ( No Rate Limiting On Sending Emails On Contact us Page) |
| [146180](https://hackerone.com/reports/146180) | Internet Bug Bounty |  | - | 4 | 2019-10-13 | Memory Corruption - Generic | Integer Overflow in SplFileObject::fread |
| [146183](https://hackerone.com/reports/146183) | Internet Bug Bounty |  | - | 4 | 2019-10-13 | Memory Corruption - Generic | Integer Overflow in nl2br() |
| [152267](https://hackerone.com/reports/152267) | Internet Bug Bounty |  | - | 4 | 2019-10-13 | Memory Corruption - Generic | Use After Free in unserialize() with Unexpected Session Deserialization |
| [152281](https://hackerone.com/reports/152281) | Internet Bug Bounty |  | - | 4 | 2019-10-13 | Memory Corruption - Generic | Use After Free/Double Free in Garbage Collection |
| [159948](https://hackerone.com/reports/159948) | Internet Bug Bounty |  | - | 4 | 2019-10-13 | Memory Corruption - Generic | Use After Free Vulnerability in unserialize() |
| [159992](https://hackerone.com/reports/159992) | Internet Bug Bounty |  | - | 4 | 2019-10-14 | Memory Corruption - Generic | memory allocator fails to realloc small block to large one |
| [160294](https://hackerone.com/reports/160294) | Internet Bug Bounty |  | - | 4 | 2019-11-12 | Memory Corruption - Generic | Memory Leakage In exif_process_IFD_in_TIFF (CVE-2016-7128) |
| [167931](https://hackerone.com/reports/167931) | Internet Bug Bounty |  | - | 4 | 2019-10-13 | Memory Corruption - Generic | Memory Corruption in During Deserialized-object Destruction |
| [170619](https://hackerone.com/reports/170619) | Internet Bug Bounty | low | - | 4 | 2020-10-10 | Memory Corruption - Generic | PHP Integer Overflow in gdImageWebpCtx |
| [172411](https://hackerone.com/reports/172411) | Internet Bug Bounty | low | - | 4 | 2017-05-30 | Memory Corruption - Generic | Heap overflow caused by type confusion vulnerability in merge_param() |
| [180908](https://hackerone.com/reports/180908) | Internet Bug Bounty | low | - | 4 | 2019-10-13 | Memory Corruption - Generic | NULL Pointer Dereference in WDDX Packet Deserialization with PDORow |
| [180909](https://hackerone.com/reports/180909) | Internet Bug Bounty | medium | - | 4 | 2019-10-13 | Use After Free | Use-after-free in ArrayObject Deserialization |
| [191994](https://hackerone.com/reports/191994) | shopify-scripts | low | - | 4 | 2017-02-10 | Memory Corruption - Generic | SIGSEGV mrb_obj_freeze() Manipulating Register RAX and RSI |
| [192318](https://hackerone.com/reports/192318) | shopify-scripts | none | - | 4 | 2017-02-10 | Memory Corruption - Generic | mrb_vformat() heap overflow could lead to code execution |
| [196380](https://hackerone.com/reports/196380) | shopify-scripts |  | - | 4 | 2017-03-01 | Memory Corruption - Generic | SIGSEGV in mrb_vm_exec |
| [198452](https://hackerone.com/reports/198452) | shopify-scripts |  | - | 4 | 2017-03-29 | Memory Corruption - Generic | SIGABRT - mrb_realloc_simple - gc.c - line:201 |
| [198732](https://hackerone.com/reports/198732) | Internet Bug Bounty | medium | - | 4 | 2019-10-13 | Use After Free | Use After Free in unserialize() |
| [198927](https://hackerone.com/reports/198927) | Ruby | none | - | 4 | 2017-10-25 | Memory Corruption - Generic | Parsing invalid unicode codepoints using json c extension (2.0.1+) triggers a segfault |
| [212882](https://hackerone.com/reports/212882) | shopify-scripts |  | - | 4 | 2017-04-27 | Memory Corruption - Generic | SIGABRT in only mirb |
| [216700](https://hackerone.com/reports/216700) | shopify-scripts |  | - | 4 | 2017-05-13 | Memory Corruption - Generic | heap use-after-free in mrb_vm_exec() |
| [217083](https://hackerone.com/reports/217083) | shopify-scripts |  | - | 4 | 2017-05-13 | NULL Pointer Dereference | SIGSEGV in mrb_str_inum |
| [217097](https://hackerone.com/reports/217097) | shopify-scripts |  | - | 4 | 2017-05-13 | NULL Pointer Dereference | SIGSEGV in mrb_vm_exec |
| [217747](https://hackerone.com/reports/217747) | U.S. Dept Of Defense | low | - | 4 | 2017-06-23 | NULL Pointer Dereference | Information disclosure vulnerability on a DoD website |
| [221289](https://hackerone.com/reports/221289) | LibSass | medium | - | 4 | 2017-08-10 | Use After Free | heap-use-after-free in Sass::SharedPtr::incRefCount() |
| [245221](https://hackerone.com/reports/245221) | Mapbox | high | - | 4 | 2017-07-11 | NULL Pointer Dereference | null pointer dereference and segfault in tile-count-merge |
| [247640](https://hackerone.com/reports/247640) | Ruby |  | - | 4 | 2017-09-24 | Memory Corruption - Generic | Ruby 2.4.1 has "Stack consistency error" and aborts when processing return statement within a case statement |
| [250581](https://hackerone.com/reports/250581) | Internet Bug Bounty |  | - | 4 | 2019-10-04 | Buffer Over-read | CVE-2017-11367: Global buffer overflow (READ of size 4) in shoco C library |
| [268806](https://hackerone.com/reports/268806) | Internet Bug Bounty | high | - | 4 | 2019-10-08 | Buffer Over-read | CVE-2017-13009 The IPv6 mobility parser in tcpdump before 4.9.2 has a buffer over-read in print-mobility.c:mobility_print(). |
| [268807](https://hackerone.com/reports/268807) | Internet Bug Bounty | high | - | 4 | 2019-10-08 | Buffer Over-read | CVE-2017-13010 The BEEP parser in tcpdump before 4.9.2 has a buffer over-read in print-beep.c:l_strnstart(). |
| [278231](https://hackerone.com/reports/278231) | Internet Bug Bounty |  | - | 4 | 2018-05-16 | Buffer Over-read | Out of bounds read in libcurl's IMAP FETCH response parser |
| [321687](https://hackerone.com/reports/321687) | Node.js third-party modules | high | - | 4 | 2018-05-11 | Out-of-bounds Read | `base64url` allocates uninitialized Buffers when number is passed in input on Node.js 4.x and below |
| [321702](https://hackerone.com/reports/321702) | Node.js third-party modules | low | - | 4 | 2018-06-14 | Out-of-bounds Read | `put` allocates uninitialized Buffers when non-round numbers are passed in input |
| [323017](https://hackerone.com/reports/323017) | Internet Bug Bounty | medium | - | 4 | 2019-10-14 | Out-of-bounds Read | Two vulnerability in GNU binutils |
| [330351](https://hackerone.com/reports/330351) | Node.js third-party modules | medium | - | 4 | 2018-05-11 | Out-of-bounds Read | `byte` allocates uninitialized buffers and reads data from them past the initialized length |
| [335608](https://hackerone.com/reports/335608) | Node.js | critical | - | 4 | 2020-02-13 | NULL Pointer Dereference | Denial of Service: nghttp2 use of uninitialized pointer |
| [480778](https://hackerone.com/reports/480778) | Internet Bug Bounty | high | - | 4 | 2019-10-24 | Buffer Over-read | Heap-buffer-overflow in Perl__byte_dump_string (utf8.c) could lead to memory leak |
| [527042](https://hackerone.com/reports/527042) | Internet Bug Bounty | medium | - | 4 | 2019-09-10 | Use After Free | CVE-2019-0196: mod_http2 with scoreboard Use-After-Free (Read) |
| [591770](https://hackerone.com/reports/591770) | curl | none | - | 4 | 2019-10-04 | Integer Overflow | Signed integer overflow in tool_progress_cb() |
| [661847](https://hackerone.com/reports/661847) | curl | low | - | 4 | 2021-01-01 | Integer Overflow | Integer overflows in tool_operate.c at line 1541 |
| [802863](https://hackerone.com/reports/802863) | Internet Bug Bounty | high | - | 4 | 2021-08-22 | Buffer Over-read | CVE-2017-13050: The RPKI-Router parser in tcpdump before 4.9.2 has a buffer over-read in print-rpki-rtr.c:rpki_rtr_pdu_print() |
| [875775](https://hackerone.com/reports/875775) | curl | high | - | 4 | 2020-05-18 | Double Free | Invalid write (or double free) triggers curl command line tool crash |
| [965914](https://hackerone.com/reports/965914) | Node.js | medium | - | 4 | 2020-10-17 | Classic Buffer Overflow | `fs.realpath.native` on darwin may cause buffer overflow |
| [1178337](https://hackerone.com/reports/1178337) | Node.js | high | - | 4 | 2021-09-10 | Improper Null Termination | Improper handling of untypical characters in domain names |
| [1340650](https://hackerone.com/reports/1340650) | UPchieve | medium | - | 4 | 2022-03-26 | NULL Pointer Dereference | No Rate Limiting for Password Reset Email Leads to Email Flooding |
| [1423496](https://hackerone.com/reports/1423496) | U.S. Dept Of Defense | critical | - | 4 | 2022-01-19 | Use of Externally-Controlled Format String | ██████████ running a vulnerable log4j |
| [3468410](https://hackerone.com/reports/3468410) | curl |  | - | 4 | 2025-12-17 | Memory Corruption - Generic | Heap buffer overflow in Curl_ipv4_resolve_r due to incorrect buffer alignment and size calculation on AmigaOS |
| [3973152](https://hackerone.com/reports/3973152) | curl |  | - | 4 | 2026-09-14 | Type Confusion | 37: `curl_mprintf` `%F` format specifier not consumed, causing variadic argument desynchronization |
| [8093](https://hackerone.com/reports/8093) | Localize |  | - | 3 | 2014-04-22 | Memory Corruption - Generic | infinite number of new project creation! |
| [55017](https://hackerone.com/reports/55017) | Internet Bug Bounty |  | - | 3 | 2015-02-04 | Memory Corruption - Generic | Multiple Python integer overflows |
| [73235](https://hackerone.com/reports/73235) | Internet Bug Bounty |  | - | 3 | 2015-03-17 | Memory Corruption - Generic | Use After Free Vulnerability in unserialize() |
| [73244](https://hackerone.com/reports/73244) | Internet Bug Bounty |  | - | 3 | 2015-03-17 | Memory Corruption - Generic | Use after free vulnerability in unserialize() with DateInterval |
| [74025](https://hackerone.com/reports/74025) | Ubiquiti Inc. |  | - | 3 | 2016-04-07 | Memory Corruption - Generic | Yet another Buffer Overflow in PHP of the AirMax Products |
| [103999](https://hackerone.com/reports/103999) | Internet Bug Bounty |  | - | 3 | 2015-09-01 | Memory Corruption - Generic | Use after free vulnerability in unserialize() with GMP |
| [105463](https://hackerone.com/reports/105463) | Imgur |  | - | 3 | 2016-03-03 | Memory Corruption - Generic | risk of having secure=false in a crossdomain.xml |
| [135283](https://hackerone.com/reports/135283) | Paragon Initiative Enterprises |  | - | 3 | 2016-05-16 | Memory Corruption - Generic | Email Authentication Bypass |
| [143022](https://hackerone.com/reports/143022) | Internet Bug Bounty |  | - | 3 | 2016-06-26 | Memory Corruption - Generic | Heap corruption via Python 2.7.11 IOBase readline() |
| [148763](https://hackerone.com/reports/148763) | Paragon Initiative Enterprises |  | - | 3 | 2016-07-01 | Memory Corruption - Generic | Email spoofing in [REDACTED_EMAIL] |
| [167512](https://hackerone.com/reports/167512) | Internet Bug Bounty |  | - | 3 | 2019-11-12 | Memory Corruption - Generic | CVE-2016-7163 OpenJPEG opj_pi_create_decode Integer Overflow Vulnerability |
| [167895](https://hackerone.com/reports/167895) | Internet Bug Bounty |  | - | 3 | 2019-11-12 | Memory Corruption - Generic | Out of bound when verify signature of zip phar in phar_parse_zipfile |
| [167896](https://hackerone.com/reports/167896) | Internet Bug Bounty |  | - | 3 | 2019-11-12 | Memory Corruption - Generic | Out of bound when verify signature of tar phar in phar_parse_tarfile |
| [167955](https://hackerone.com/reports/167955) | Internet Bug Bounty |  | - | 3 | 2019-11-12 | Memory Corruption - Generic | CVE-2016-4796 OpenJPEG color_cmyk_to_rgb Out-of-Bounds Read Vulnerability |
| [174069](https://hackerone.com/reports/174069) | Internet Bug Bounty | medium | - | 3 | 2017-05-30 | Memory Corruption - Generic | Buffer overflow in HTTP parse_hostinfo(), parse_userinfo() and parse_scheme() |
| [198733](https://hackerone.com/reports/198733) | Internet Bug Bounty | medium | - | 3 | 2019-10-13 | Type Confusion | Type Confusion in Object Deserialization |
| [202960](https://hackerone.com/reports/202960) | Internet Bug Bounty | high | - | 3 | 2019-10-08 | Memory Corruption - Generic | CVE-2017-5204: The IPv6 parser in tcpdump before 4.9.0 has a buffer overflow in print-ip6.c:ip6_print() |
| [203595](https://hackerone.com/reports/203595) | shopify-scripts |  | - | 3 | 2017-03-29 | Memory Corruption - Generic | forgot to add the patch |
| [206109](https://hackerone.com/reports/206109) | shopify-scripts |  | - | 3 | 2017-04-27 | Memory Corruption - Generic | mruby heap use-after-free |
| [219870](https://hackerone.com/reports/219870) | shopify-scripts | high | - | 3 | 2017-05-09 | Stack Overflow | mirb only: stack-buffer-overflow (OOB write) in main() |
| [221251](https://hackerone.com/reports/221251) | shopify-scripts | high | - | 3 | 2017-05-09 | Heap Overflow | heap-buffer-overflow (read outside of buffer) in mrb_vm_exec() |
| [222108](https://hackerone.com/reports/222108) | Homebrew | medium | - | 3 | 2017-04-19 | Stack Overflow | Stack Trace on jenkins.brew.sh |
| [226200](https://hackerone.com/reports/226200) | shopify-scripts | critical | - | 3 | 2017-05-30 | Write-what-where Condition | OP_SCALL in LHS of a OP_ASGN resulting in arbitrary memory write |
| [227762](https://hackerone.com/reports/227762) | shopify-scripts | high | - | 3 | 2017-05-30 | Heap Overflow | Heap Overflow in fiber_switch triggered from Fiber.transfer |
| [235842](https://hackerone.com/reports/235842) | Ruby | medium | - | 3 | 2017-10-25 | Memory Corruption - Generic | Ruby 2.3.x and 2.2.x still bundle DoS vulnerable verision of libYAML |
| [247027](https://hackerone.com/reports/247027) | Internet Bug Bounty | high | - | 3 | 2019-10-04 | NULL Pointer Dereference | CVE-2017-10965: Null pointer dereference in Irssi <1.0.4 |
| [260414](https://hackerone.com/reports/260414) | Internet Bug Bounty | high | - | 3 | 2019-10-08 | Use After Free | CVE-2017-12858: Heap UAF in _zip_buffer_free() / Double free in _zip_dirent_read() |
| [262665](https://hackerone.com/reports/262665) | Internet Bug Bounty | medium | - | 3 | 2019-10-04 | NULL Pointer Dereference | CVE-2017-5969: libxml2 when used in recover mode, allows remote attackers to cause a denial of service (NULL pointer dereference) |
| [268808](https://hackerone.com/reports/268808) | Internet Bug Bounty | high | - | 3 | 2019-10-08 | Buffer Over-read | CVE-2017-13038 The PPP parser in tcpdump before 4.9.2 has a buffer over-read in print-ppp.c:handle_mlppp(). |
| [276255](https://hackerone.com/reports/276255) | Tor |  | - | 3 | 2019-10-04 | Memory Corruption - Generic | Use of unitialized value in token_check_object (src/or/parsecommon.c:224) |
| [295740](https://hackerone.com/reports/295740) | Internet Bug Bounty | high | - | 3 | 2019-11-12 | Buffer Over-read | GarlicRust - heartbleed style vulnerability in major I2P C++ router implementations |
| [320269](https://hackerone.com/reports/320269) | Node.js third-party modules | high | - | 3 | 2018-05-12 | Out-of-bounds Read | `npmconf` (and `npm` js api) allocate and write to disk uninitialized memory content when a typed number is passed as input on Node.js 4.x |
| [321701](https://hackerone.com/reports/321701) | Node.js third-party modules | low | - | 3 | 2018-06-14 | Out-of-bounds Read | `utile` allocates uninitialized Buffers when number is passed in input |
| [335495](https://hackerone.com/reports/335495) | Node.js | high | - | 3 | 2020-02-13 | Heap Overflow | Out of order TLS handshake / application data messages lead to segmentation fault |
| [503821](https://hackerone.com/reports/503821) | PuTTY (European Commission - DIGIT) | low | - | 3 | 2019-11-03 | Memory Corruption - Generic | Assertion `col >= 0 && col < line->cols' failed, process aborted while streaming ouput from remote server |
| [541354](https://hackerone.com/reports/541354) | Node.js third-party modules | high | - | 3 | 2019-04-28 | Buffer Over-read | A specifically malformed MQTT Subscribe packet crashes MQTT Brokers using the mqtt-packet module for decoding |
| [584757](https://hackerone.com/reports/584757) | Internet Bug Bounty | low | - | 3 | 2020-10-10 | NULL Pointer Dereference | Null Pointer Dereference in phar_create_or_parse_filename |
| [600359](https://hackerone.com/reports/600359) | curl |  | - | 3 | 2021-02-08 | Integer Overflow | Integer overflow in the source code tool_cb_prg.c |
| [677557](https://hackerone.com/reports/677557) | Internet Bug Bounty | high | - | 3 | 2019-10-15 | Use After Free | mod_http2, memory corruption on early pushes (CVE-2019-10081) |
| [832217](https://hackerone.com/reports/832217) | Rocket.Chat | high | - | 3 | 2021-03-18 | Classic Buffer Overflow | Android App Crashes while sending message to users/ on channel |
| [1047086](https://hackerone.com/reports/1047086) | Internet Bug Bounty | high | - | 3 | 2021-07-09 | Heap Overflow | Heap buffer overflow vulnerability while processing a malformed TIFF file. |
| [1065517](https://hackerone.com/reports/1065517) | h1-ctf | critical | - | 3 | 2021-01-11 | Buffer Over-read | h1 hacky holidays CTF solution |
| [1130792](https://hackerone.com/reports/1130792) | Open-Xchange |  | - | 3 |  | NULL Pointer Dereference | Null pointer dereference in lib-sieve after calling sieve_binary_block_index |
| [1913110](https://hackerone.com/reports/1913110) | Internet Bug Bounty | low | - | 3 | 2023-03-23 | Double Free | CVE-2023-27537: HSTS double-free |
| [3238249](https://hackerone.com/reports/3238249) | curl | medium | - | 3 | 2025-07-07 | Integer Overflow | Integer Overflow Risk in HTTP/2 Proxy Window Size Calculations |
| [3749204](https://hackerone.com/reports/3749204) | curl | low | - | 3 | 2026-06-24 | Use After Free | CVE-2026-9080: UAF after pause in socket callback |
| [3754343](https://hackerone.com/reports/3754343) | curl | low | - | 3 | 2026-06-24 | Use After Free | CVE-2026-9546: sending old referer |
| [3831345](https://hackerone.com/reports/3831345) | curl |  | - | 3 | 2026-06-30 | Use After Free | CURLSHOPT_UNSHARE race can cause UAF in shared SSL session cache during HTTPS transfer |
| [3891319](https://hackerone.com/reports/3891319) | MariaDB | medium | - | 3 | 2026-11-04 | Stack Overflow | Stack buffer overflow in 9 of 10 Connector/ODBC catalog functions via unbounded name |
| [3891337](https://hackerone.com/reports/3891337) | MariaDB | medium | - | 3 | 2026-11-04 | Type Confusion | Connector/ODBC SQLGetDescRec treats descriptor handle as statement handle, heap OOB write on every call |
| [4105853](https://hackerone.com/reports/4105853) | curl | medium | - | 3 | 2026-10-19 | Out-of-bounds Read | libcurl TLS shorter-retry mismatch discloses client heap memory during cancelled IMAPS upload |
| [4118643](https://hackerone.com/reports/4118643) | curl | low | - | 3 | 2026-10-26 | Use After Free | OpenSSL provider OSSL_LIB_CTX used after free via the connection shutdown list (CVE-2026-80229 fix incomplete) |
| [10767](https://hackerone.com/reports/10767) | Yahoo! |  | - | 2 |  | Memory Corruption - Generic | Yahoo! Messenger v11.5.0.228 emoticons.xml shortcut Value Handling Stack-Based Buffer Overflow |
| [28640](https://hackerone.com/reports/28640) | Internet Bug Bounty |  | - | 2 | 2019-11-12 | Memory Corruption - Generic | Ericsson Erlang OTP Core Allocation Subsystem Integer Overflow (All Versions) |
| [36264](https://hackerone.com/reports/36264) | Internet Bug Bounty |  | - | 2 | 2014-11-12 | Memory Corruption - Generic | mod_proxy_fcgi buffer overflow |
| [38170](https://hackerone.com/reports/38170) | Internet Bug Bounty |  | - | 2 | 2014-10-04 | Memory Corruption - Generic | Misc Python bugs (Memory Corruption & Use After Free) |
| [47779](https://hackerone.com/reports/47779) | Internet Bug Bounty |  | - | 2 | 2015-04-06 | Memory Corruption - Generic | Heap overflow in H. Spencer’s regex library on 32 bit systems |
| [48100](https://hackerone.com/reports/48100) | Internet Bug Bounty |  | - | 2 | 2015-03-01 | Memory Corruption - Generic | Bad Write in TTF font parsing (win32k.sys) |
| [66962](https://hackerone.com/reports/66962) | Internet Bug Bounty |  | - | 2 | 2019-11-12 | Memory Corruption - Generic | Misusing of FPU Instruction Could Cause Security Vulnerabilities in Adobe Flash Player |
| [73234](https://hackerone.com/reports/73234) | Internet Bug Bounty |  | - | 2 | 2014-12-30 | Memory Corruption - Generic | out of bounds read crashes php-cgi |
| [73236](https://hackerone.com/reports/73236) | Internet Bug Bounty |  | - | 2 | 2015-03-15 | Memory Corruption - Generic | X509_to_X509_REQ NULL pointer deref |
| [73249](https://hackerone.com/reports/73249) | Internet Bug Bounty |  | - | 2 | 2015-05-18 | Memory Corruption - Generic | Multiple use after free bugs in element module |
| [73250](https://hackerone.com/reports/73250) | Internet Bug Bounty |  | - | 2 | 2015-05-03 | Memory Corruption - Generic | Multiple use after free bugs in heapq module |
| [73251](https://hackerone.com/reports/73251) | Internet Bug Bounty |  | - | 2 | 2015-05-03 | Memory Corruption - Generic | Multiple use after free bugs in json encoding |
| [73252](https://hackerone.com/reports/73252) | Internet Bug Bounty |  | - | 2 | 2015-05-03 | Memory Corruption - Generic | Use after free in get_filter |
| [91604](https://hackerone.com/reports/91604) | Imgur |  | - | 2 | 2015-12-09 | Memory Corruption - Generic | Crossdomain.xml settings on api.imgur.com too open |
| [103995](https://hackerone.com/reports/103995) | Internet Bug Bounty |  | - | 2 | 2015-09-01 | Memory Corruption - Generic | Use After Free Vulnerability in unserialize() with SplDoublyLinkedList |
| [103996](https://hackerone.com/reports/103996) | Internet Bug Bounty |  | - | 2 | 2015-09-01 | Memory Corruption - Generic | Use After Free Vulnerability in unserialize() with SplObjectStorage |
| [103997](https://hackerone.com/reports/103997) | Internet Bug Bounty |  | - | 2 | 2015-09-01 | Memory Corruption - Generic | Use After Free Vulnerability in unserialize() |
| [104018](https://hackerone.com/reports/104018) | Internet Bug Bounty |  | - | 2 | 2015-08-05 | Memory Corruption - Generic | Multiple Use After Free Vulnerabilites in unserialize() |
| [108681](https://hackerone.com/reports/108681) | Internet Bug Bounty |  | - | 2 | 2019-10-13 | Memory Corruption - Generic | Use After Free Vulnerability in WDDX Packet Deserialization |
| [108683](https://hackerone.com/reports/108683) | Internet Bug Bounty |  | - | 2 | 2019-10-13 | Memory Corruption - Generic | Session WDDX Packet Deserialization Type Confusion Vulnerability |
| [112860](https://hackerone.com/reports/112860) | Internet Bug Bounty |  | - | 2 | 2019-11-12 | Memory Corruption - Generic | UAF  in xmlparser_setevents (2) |
| [113268](https://hackerone.com/reports/113268) | Internet Bug Bounty |  | - | 2 | 2019-10-14 | Memory Corruption - Generic | Integer overflow in wordwrap |
| [120903](https://hackerone.com/reports/120903) | Internet Bug Bounty |  | - | 2 | 2019-11-12 | Memory Corruption - Generic | putty pscp client-side post-auth stack buffer overwrite when processing remote file size |
| [125397](https://hackerone.com/reports/125397) | Internet Bug Bounty |  | - | 2 | 2016-05-17 | Memory Corruption - Generic | Null pointer deref (segfault) in stream_context_get_default |
| [135945](https://hackerone.com/reports/135945) | Internet Bug Bounty |  | - | 2 | 2016-05-03 | Memory Corruption - Generic | EVP_EncryptUpdate overflow (CVE-2016-2106) |
| [141676](https://hackerone.com/reports/141676) | Bime |  | - | 2 | 2016-06-27 | Memory Corruption - Generic | Bime Unable to load Data Sources |
| [141839](https://hackerone.com/reports/141839) | Internet Bug Bounty |  | - | 2 | 2019-11-12 | Memory Corruption - Generic | Multiple vulnerabilities related to PCRE functions (already fixed) |
| [144485](https://hackerone.com/reports/144485) | Ruby |  | - | 2 | 2016-06-21 | Memory Corruption - Generic | Heap corruption in string.c tr_trans() due to undersized buffer |
| [146360](https://hackerone.com/reports/146360) | Internet Bug Bounty |  | - | 2 | 2019-11-12 | Memory Corruption - Generic | Heap Overflow Due To Integer Overflow |
| [148914](https://hackerone.com/reports/148914) | Paragon Initiative Enterprises |  | - | 2 | 2016-07-02 | Memory Corruption - Generic | Session Management Issue CMS Airship |
| [150626](https://hackerone.com/reports/150626) | Internet Bug Bounty | low | - | 2 | 2019-11-12 | Memory Corruption - Generic | Heap Buffer Overflow |
| [152232](https://hackerone.com/reports/152232) | Internet Bug Bounty |  | - | 2 | 2016-08-30 | Memory Corruption - Generic | NULL Pointer Dereference in exif_process_user_comment |
| [152280](https://hackerone.com/reports/152280) | Internet Bug Bounty |  | - | 2 | 2019-11-12 | Memory Corruption - Generic | Stack-based buffer overflow vulnerability in virtual_file_ex |
| [153863](https://hackerone.com/reports/153863) | Internet Bug Bounty |  | - | 2 | 2019-11-12 | Memory Corruption - Generic | heap-buffer-overflow (write) simplestring_addn simplestring.c |
| [159690](https://hackerone.com/reports/159690) | Internet Bug Bounty |  | - | 2 | 2019-11-12 | Memory Corruption - Generic | stack buffer overflows in the curses module |
| [160295](https://hackerone.com/reports/160295) | Internet Bug Bounty |  | - | 2 | 2019-11-12 | Memory Corruption - Generic | Heap overflow in curl_escape |
| [167947](https://hackerone.com/reports/167947) | Internet Bug Bounty |  | - | 2 | 2019-11-12 | Memory Corruption - Generic | CVE-2016-3183 OpenJPEG sycc422_to_rgb Out-of-Bounds Read Vulnerability |
| [167953](https://hackerone.com/reports/167953) | Internet Bug Bounty |  | - | 2 | 2019-11-12 | Memory Corruption - Generic | CVE-2016-3182 OpenJPEG color_esycc_to_rgb Out-of-Bounds Read Vulnerability |
| [172115](https://hackerone.com/reports/172115) | Internet Bug Bounty | low | - | 2 | 2019-11-12 | Memory Corruption - Generic | Multiple use after frees in obj2ast_* methods |
| [195688](https://hackerone.com/reports/195688) | Internet Bug Bounty | medium | - | 2 | 2019-11-12 | NULL Pointer Dereference | NULL Pointer Dereference while unserialize php object |
| [202968](https://hackerone.com/reports/202968) | Internet Bug Bounty | high | - | 2 | 2019-10-08 | Memory Corruption - Generic | CVE-2017-5342 In tcpdump before 4.9.0 a bug in multiple protocol parsers could cause a buffer overflow in print-ether.c:ether_print() |
| [202969](https://hackerone.com/reports/202969) | Internet Bug Bounty | high | - | 2 | 2019-10-08 | Memory Corruption - Generic | CVE-2017-5482 The Q.933 parser in tcpdump before 4.9.0 has a buffer overflow in print-fr.c:q933_print(). |
| [207710](https://hackerone.com/reports/207710) | shopify-scripts |  | - | 2 | 2017-04-13 | Memory Corruption - Generic | Heap use-after-free in mrb_vm_exec |
| [209765](https://hackerone.com/reports/209765) | shopify-scripts | medium | - | 2 | 2017-04-13 | Memory Corruption - Generic | Heap buffer overflow in mruby value_move |
| [221163](https://hackerone.com/reports/221163) | LibSass | high | - | 2 | 2019-10-05 | Heap Overflow | heap-buffer-overflow (read outside of buffer) in Sass::Prelexer::exactly<(char)92>(char const*) - libsass/src/lexer.hpp:92 |
| [227344](https://hackerone.com/reports/227344) | Internet Bug Bounty | high | - | 2 | 2019-11-12 | Integer Overflow | CVE-2017-8798 - miniupnp getHTTPResponse chunked encoding integer signedness error |
| [255125](https://hackerone.com/reports/255125) | Legal Robot |  | - | 2 | 2018-02-24 | Improper Null Termination | Null Byte Injection in all fields of Profile |
| [268803](https://hackerone.com/reports/268803) | Internet Bug Bounty | high | - | 2 | 2019-10-08 | Buffer Over-read | CVE-2017-12985: The IPv6 parser in tcpdump before 4.9.2 has a buffer over-read in ip6_print() |
| [272097](https://hackerone.com/reports/272097) | Internet Bug Bounty | medium | - | 2 | 2017-12-11 | Integer Underflow | Interger overflow in eval trigger write out of bound |
| [276253](https://hackerone.com/reports/276253) | Tor | none | - | 2 | 2017-10-31 | Memory Corruption - Generic | Use of uninitialized value in networkstatus_parse_vote_from_string (src/or/routerparse.c:3533) |
| [320166](https://hackerone.com/reports/320166) | Node.js third-party modules | medium | - | 2 | 2018-04-28 | Out-of-bounds Read | `concat-with-sourcemaps` allocates uninitialized Buffers when number is passed as a separator |
| [321670](https://hackerone.com/reports/321670) | Node.js third-party modules | medium | - | 2 | 2018-05-11 | Out-of-bounds Read | `stringstream` allocates uninitialized Buffers when number is passed in input stream on Node.js 4.x and below |
| [340053](https://hackerone.com/reports/340053) | Node.js |  | - | 2 | 2020-01-15 | Use After Free | Use After Free in crypto.randomFill |
| [380102](https://hackerone.com/reports/380102) | Nextcloud | medium | - | 2 | 2020-08-14 | Memory Corruption - Generic | Missing memory corruption protection on Windows release built |
| [515322](https://hackerone.com/reports/515322) | Mail.ru |  | - | 2 |  | Out-of-bounds Read | FLV FILE FORMAT (AUDIOSES.DLL) Out of Bounds |
| [627245](https://hackerone.com/reports/627245) | curl |  | - | 2 | 2021-02-08 | Integer Overflow | Integer overlow in "header_append" function |
| [680415](https://hackerone.com/reports/680415) | Internet Bug Bounty | medium | - | 2 | 2019-10-15 | Use After Free | mod_http2, read-after-free in h2 connection shutdown (CVE-2019-10082) |
| [692040](https://hackerone.com/reports/692040) | Internet Bug Bounty | medium | - | 2 | 2020-10-12 | Use After Free | PHP 7.3.3: Heap-use-after-free (READ of size 8) in match_at() |
| [765664](https://hackerone.com/reports/765664) | curl | low | - | 2 | 2021-01-08 | Heap Overflow | Heap Buffer Overflow (READ of size 1) in ourWriteOut |
| [802896](https://hackerone.com/reports/802896) | Internet Bug Bounty | high | - | 2 | 2021-08-22 | Buffer Over-read | CVE-2017-13019:  The PGM parser in tcpdump before 4.9.2 has a buffer over-read in print-pgm.c:pgm_print() |
| [805010](https://hackerone.com/reports/805010) | Internet Bug Bounty | medium | - | 2 | 2020-11-09 | Improper Null Termination | PHP link() silently truncates after a null byte on Windows |
| [852103](https://hackerone.com/reports/852103) | Internet Bug Bounty | medium | - | 2 | 2020-10-12 | Out-of-bounds Read | Out-of-Bound Read in urldecode() [CVE-2020-7067] |
| [962832](https://hackerone.com/reports/962832) | Solana BBP |  | - | 2 |  | Buffer Under-read | Buffer can be readable through Debug on metrics.solana.com |
| [1438393](https://hackerone.com/reports/1438393) | U.S. Dept Of Defense | critical | - | 2 | 2022-01-19 | Use of Externally-Controlled Format String | ███ ████████ running a vulnerable log4j |
| [1468962](https://hackerone.com/reports/1468962) | curl | low | - | 2 | 2022-03-09 | Classic Buffer Overflow | Binary output bypass |
| [1589847](https://hackerone.com/reports/1589847) | curl | low | - | 2 | 2022-06-05 | Heap Overflow | Heap overflow via HTTP/2 PUSH_PROMISE |
| [1997312](https://hackerone.com/reports/1997312) | Internet Bug Bounty | medium | - | 2 | 2023-06-25 | Use After Free | CVE-2023-28319: UAF in SSH sha256 fingerprint check |
| [3735193](https://hackerone.com/reports/3735193) | curl | medium | - | 2 | 2026-06-24 | Double Free | CVE-2026-8925: SASL double-free |
| [4024222](https://hackerone.com/reports/4024222) | curl | none | - | 2 | 2026-10-14 | Memory Corruption - Generic | CVE-2026-92391: curl_mime_free stack overflow by recursion |
| [4116527](https://hackerone.com/reports/4116527) | curl | low | - | 2 | 2026-10-26 | Use After Free | CVE-2026-111878: OpenSSL provider UAF on TLS shutdown |
| [4124722](https://hackerone.com/reports/4124722) | curl | low | - | 2 | 2026-10-20 | Use After Free | WebSocket send queue use-after-free during nested curl_ws_send() |
| [17688](https://hackerone.com/reports/17688) | Internet Bug Bounty |  | - | 1 | 2014-07-25 | Memory Corruption - Generic | LZ4 Core |
| [18843](https://hackerone.com/reports/18843) | Internet Bug Bounty |  | - | 1 | 2019-11-12 | Memory Corruption - Generic | use-after-free vulnerability in Flash Player |
| [20671](https://hackerone.com/reports/20671) | Internet Bug Bounty |  | - | 1 | 2014-06-24 | Memory Corruption - Generic | integer overflow in 'buffer' type allows reading memory |
| [47232](https://hackerone.com/reports/47232) | Internet Bug Bounty |  | - | 1 | 2015-03-25 | Memory Corruption - Generic | Use after free during the StageVideoAvailabilityEvent can result in arbitrary code execution |
| [47234](https://hackerone.com/reports/47234) | Internet Bug Bounty |  | - | 1 | 2015-03-25 | Memory Corruption - Generic | Use After Free in Flash MessageChannel.send can cause arbitrary code execution |
| [55033](https://hackerone.com/reports/55033) | Internet Bug Bounty |  | - | 1 | 2015-01-20 | Memory Corruption - Generic | Use after free vulnerability in unserialize() |
| [66724](https://hackerone.com/reports/66724) | LibSass |  | - | 1 | 2015-06-11 | Memory Corruption - Generic | type confusion in Sass::ParserState::ParserState(Sass::ParserState const&) |
| [73240](https://hackerone.com/reports/73240) | Internet Bug Bounty |  | - | 1 | 2015-05-12 | Memory Corruption - Generic | Integer overflow in ftp_genlist() resulting in heap overflow |
| [73255](https://hackerone.com/reports/73255) | Internet Bug Bounty |  | - | 1 | 2015-05-12 | Memory Corruption - Generic | str_repeat() sign mismatch based memory corruption |
| [73260](https://hackerone.com/reports/73260) | Internet Bug Bounty |  | - | 1 | 2015-06-27 | Memory Corruption - Generic | Integer overflow in _json_encode_unicode leads to crash |
| [112858](https://hackerone.com/reports/112858) | Internet Bug Bounty |  | - | 1 | 2019-11-12 | Memory Corruption - Generic | UAF in xmlparser_setevents (1) |
| [113120](https://hackerone.com/reports/113120) | Internet Bug Bounty |  | - | 1 | 2019-11-12 | Memory Corruption - Generic | An integer overflow bug in php_implode() could lead heap overflow, make PHP to crash |
| [113122](https://hackerone.com/reports/113122) | Internet Bug Bounty |  | - | 1 | 2019-11-12 | Memory Corruption - Generic | An integer overflow bug in php_str_to_str_ex() led arbitrary code execution. |
| [114414](https://hackerone.com/reports/114414) | Internet Bug Bounty |  | - | 1 | 2019-11-12 | Memory Corruption - Generic | openssl_seal() uninitialized memory usage |
| [118855](https://hackerone.com/reports/118855) | Internet Bug Bounty |  | - | 1 | 2016-03-27 | Memory Corruption - Generic | CVE-2016-0799 memory issues in BIO_*printf functions |
| [119873](https://hackerone.com/reports/119873) | Internet Bug Bounty |  | - | 1 | 2016-03-27 | Memory Corruption - Generic | BN_hex2bn/BN_dec2bn NULL pointer deref/heap corruption (CVE-2016-0797) |
| [119989](https://hackerone.com/reports/119989) | Internet Bug Bounty |  | - | 1 | 2016-03-28 | Memory Corruption - Generic | b2i_PVK_bio heap corruption |
| [122256](https://hackerone.com/reports/122256) | Internet Bug Bounty |  | - | 1 | 2019-11-12 | Memory Corruption - Generic | Adobe Flash Player  Uninitialised Memory Corruption |
| [125400](https://hackerone.com/reports/125400) | New Relic |  | - | 1 |  | Memory Corruption - Generic | Too many included lookups |
| [135027](https://hackerone.com/reports/135027) | Internet Bug Bounty |  | - | 1 | 2016-05-03 | Memory Corruption - Generic | Potential double free in EVP_DigestInit_ex |
| [135944](https://hackerone.com/reports/135944) | Internet Bug Bounty |  | - | 1 | 2016-05-03 | Memory Corruption - Generic | EVP_EncodeUpdate overflow (CVE-2016-2105) |
| [135946](https://hackerone.com/reports/135946) | Internet Bug Bounty |  | - | 1 | 2016-05-03 | Memory Corruption - Generic | EBCDIC overread (CVE-2016-2176) |
| [144484](https://hackerone.com/reports/144484) | Ruby |  | - | 1 | 2016-06-21 | Memory Corruption - Generic | Heap corruption in DateTime.strftime() on 32 bit for certain format strings |
| [146200](https://hackerone.com/reports/146200) | Internet Bug Bounty |  | - | 1 | 2019-11-12 | Memory Corruption - Generic | _php_mb_regex_ereg_replace_exec - double free |
| [159687](https://hackerone.com/reports/159687) | Internet Bug Bounty |  | - | 1 | 2019-11-12 | Memory Corruption - Generic | integer overflow in binascii.b2a_qp |
| [159988](https://hackerone.com/reports/159988) | Internet Bug Bounty |  | - | 1 | 2019-11-12 | Memory Corruption - Generic | Heap Overflow due to integer overflows |
| [167510](https://hackerone.com/reports/167510) | Internet Bug Bounty |  | - | 1 | 2019-11-12 | Memory Corruption - Generic | CVE-2016-5157 OpenJPEG opj_dwt_interleave_v Out-of-Bounds Write Vulnerability |
| [167957](https://hackerone.com/reports/167957) | Internet Bug Bounty |  | - | 1 | 2019-11-12 | Memory Corruption - Generic | CVE-2016-1924 OpenJPEG opj_tgt_reset Out-of-Bounds Read Vulnerability |
| [180562](https://hackerone.com/reports/180562) | Internet Bug Bounty | low | - | 1 | 2019-11-12 | Memory Corruption - Generic | Memory corruption in _php_math_number_format_ex() |
| [180563](https://hackerone.com/reports/180563) | Internet Bug Bounty | low | - | 1 | 2019-11-12 | Memory Corruption - Generic | Heap overflow due to integer overflow in bzdecompress() function |
| [180572](https://hackerone.com/reports/180572) | Internet Bug Bounty | low | - | 1 | 2019-11-12 | Memory Corruption - Generic | Memory corruption due to missing check size in _php_math_number_format_ex() |
| [180582](https://hackerone.com/reports/180582) | Internet Bug Bounty | low | - | 1 | 2019-11-12 | Memory Corruption - Generic | Heap overflow due to integer overflow in php_escape_html_entities_ex() function |
| [180584](https://hackerone.com/reports/180584) | Internet Bug Bounty | low | - | 1 | 2019-11-12 | Memory Corruption - Generic | Heap overflow due to integer overflow in pg_escape_string() function |
| [188661](https://hackerone.com/reports/188661) | Internet Bug Bounty | medium | - | 1 | 2019-11-12 | Memory Corruption - Generic | Invalid read when wddx decodes empty boolean element |
| [264481](https://hackerone.com/reports/264481) | Tor | high | - | 1 | 2017-10-02 | Stack Overflow | Stack overflow in UnbindFromTree (browser can be crashed remotely) |
| [274997](https://hackerone.com/reports/274997) | Tor |  | - | 1 | 2017-10-25 | Memory Corruption - Generic | Use of uninitialized value in memarea_strdup (src/common/memarea.c:369) |
| [287666](https://hackerone.com/reports/287666) | Internet Bug Bounty | high | - | 1 | 2019-11-12 | Classic Buffer Overflow | CVE-2017-13089 wget stack smash |
| [287667](https://hackerone.com/reports/287667) | Internet Bug Bounty | high | - | 1 | 2019-11-12 | Classic Buffer Overflow | CVE-2017-13090 wget heap smash |
| [292500](https://hackerone.com/reports/292500) | Coinbase |  | - | 1 | 2018-04-09 | Type Confusion | User provided values passed to PHP unset() function |
| [363658](https://hackerone.com/reports/363658) | Liberapay | none | - | 1 | 2018-06-10 | Classic Buffer Overflow | Buffer overflow |
| [518097](https://hackerone.com/reports/518097) | curl | high | - | 1 | 2021-01-08 | Heap Overflow | libcurl: SMTP end-of-response out-of-bounds read - CVE-2019-3823 |
| [536954](https://hackerone.com/reports/536954) | Node.js | high | - | 1 | 2020-02-13 | Improper Null Termination | Vulnerability in http-parser & embedded NULL header handling |
| [636013](https://hackerone.com/reports/636013) | curl | low | - | 1 | 2021-02-08 | Classic Buffer Overflow | huge COLUMNS causes progress-bar to buffer overflow |
| [662412](https://hackerone.com/reports/662412) | curl | low | - | 1 | 2021-02-08 | Integer Overflow | Integer overflow  at line 1603 in the src/operator.c file |
| [694449](https://hackerone.com/reports/694449) | curl | low | - | 1 | 2021-02-08 | Classic Buffer Overflow | Buffer write overflow when forming dns over http request |
| [696822](https://hackerone.com/reports/696822) | curl | low | - | 1 | 2021-02-08 | Memory Corruption - Generic | Potential invocation of qsort on uninitialized memory during cookie save |
| [707006](https://hackerone.com/reports/707006) | curl | low | - | 1 | 2021-02-08 | Use After Free | use after free in cookie.c |
| [724134](https://hackerone.com/reports/724134) | curl | low | - | 1 | 2021-01-08 | Use After Free | Race condition with CURL_LOCK_DATA_CONNECT can cause connections to be used at the same time |
| [781325](https://hackerone.com/reports/781325) | Internet Bug Bounty | medium | - | 1 | 2020-11-09 | Out-of-bounds Read | Out-of-bounds Read in php_strip_tags_ex |
| [798744](https://hackerone.com/reports/798744) | Internet Bug Bounty | medium | - | 1 | 2020-11-09 | NULL Pointer Dereference | Null Pointer Dereference in PHP Session Upload Progress |
| [805013](https://hackerone.com/reports/805013) | Internet Bug Bounty | medium | - | 1 | 2020-11-09 | Improper Null Termination | DirectoryIterator class silently truncates after a null byte |
| [816637](https://hackerone.com/reports/816637) | Internet Bug Bounty | critical | - | 1 | 2021-08-22 | Heap Overflow | CVE-2020-10938-buffer overflow/out-of-bounds write in compress.c:HuffmanDecodeImage() |
| [887744](https://hackerone.com/reports/887744) | h1-ctf | critical | - | 1 | 2020-06-25 | Buffer Underflow | [H1-2006 2020]  Got the flag |
| [962839](https://hackerone.com/reports/962839) | Solana BBP |  | - | 1 |  | Heap Overflow | Heap memory can be accessible through metrics.solana.com |
| [966347](https://hackerone.com/reports/966347) | Node.js third-party modules | high | - | 1 | 2020-08-27 | Buffer Over-read | [bl] Uninitialized memory exposure via negative .consume() |
| [995699](https://hackerone.com/reports/995699) | Kubernetes | medium | - | 1 | 2021-01-07 | NULL Pointer Dereference | csi-snapshot-controller crashes when processing VolumeSnapshot with non-existing PVC |
| [1463013](https://hackerone.com/reports/1463013) | curl | low | - | 1 | 2022-03-09 | Use After Free | Occasional use-after-free in multi_done() libcurl-7.81.0 |
| [1485379](https://hackerone.com/reports/1485379) | curl | high | - | 1 | 2022-03-09 | Classic Buffer Overflow | Use of Unsafe function \|\| Strcpy |
| [4102061](https://hackerone.com/reports/4102061) | curl | low | - | 1 | 2026-10-26 | Use After Free | CVE-2026-111480: pause UAF from within callback |
| [4122239](https://hackerone.com/reports/4122239) | curl | medium | - | 1 | 2026-10-26 | Use After Free | CVE-2026-111952: OpenSSL provider use-after-free again |
| [4123190](https://hackerone.com/reports/4123190) | curl | low | - | 1 | 2026-10-26 | Use After Free | CVE-2026-111954: upload reader failed redirect UAF |
| [49378](https://hackerone.com/reports/49378) | Dropbox |  | - | 0 |  | Memory Corruption - Generic | Create N Accounts In Dropbox Irrespective Of Domain |
| [103992](https://hackerone.com/reports/103992) | Internet Bug Bounty |  | - | 0 | 2015-09-26 | Memory Corruption - Generic | Integer overflow in _Unpickler_Read |
| [104028](https://hackerone.com/reports/104028) | Internet Bug Bounty |  | - | 0 | 2015-06-18 | Memory Corruption - Generic | Improved fix for bug #69545 (Integer overflow in ftp_genlist() resulting in heap overflow) |
| [116352](https://hackerone.com/reports/116352) | Gratipay | none | - | 0 | 2016-02-15 | Memory Corruption - Generic | nginx SPDY heap buffer overflow for https://grtp.co/ |
| [117818](https://hackerone.com/reports/117818) | LeaseWeb |  | - | 0 | 2016-02-22 | Memory Corruption - Generic | MISSING SPF RECORDS & MISSING DKIM POLICY |
| [159686](https://hackerone.com/reports/159686) | Internet Bug Bounty |  | - | 0 | 2019-11-12 | Memory Corruption - Generic | integer overflow in the _csv module's join_append_data function |
| [281682](https://hackerone.com/reports/281682) | Tor | medium | - | 0 | 2017-10-24 | Classic Buffer Overflow | Crashes/Buffer at 0x2C0086,name=PBrowser::Msg_Destroy |
| [304115](https://hackerone.com/reports/304115) | Ruby | none | - | 0 | 2018-02-23 | Integer Underflow | Integer Underflow @ ossl_cipher_pkcs5_keyivgen |
| [315037](https://hackerone.com/reports/315037) | Node.js third-party modules | medium | - | 0 | 2019-04-03 | Classic Buffer Overflow | Media parsing in canvas is at least vulnerable to Denial of Service through multiple vulnerabilities |
| [510336](https://hackerone.com/reports/510336) | Internet Bug Bounty | critical | - | 0 | 2020-10-10 | Classic Buffer Overflow | Uninitialized read in exif_process_IFD_in_TIFF |
| [672245](https://hackerone.com/reports/672245) | Internet Bug Bounty | medium | - | 0 | 2020-11-09 | Use After Free | Use After Free in GC with Certain Destructors |
| [687734](https://hackerone.com/reports/687734) | curl | medium | - | 0 | 2021-01-12 | Double Free | Double-free of `trailers_buf' on `Curl_http_compile_trailers()` failure |
| [872089](https://hackerone.com/reports/872089) | curl | low | - | 0 | 2021-01-08 | Incorrect Calculation of Buffer Size | Curl_auth_create_plain_message integer overflow leads to heap buffer overflow |
| [883606](https://hackerone.com/reports/883606) | Open-Xchange |  | - | 0 |  | NULL Pointer Dereference | Missing (or redundant) null check in `dcrypt_openssl_sign` |
| [950299](https://hackerone.com/reports/950299) | Internet Bug Bounty | medium | - | 0 | 2020-11-09 | Use After Free | Use after free vulnerability  in phar_parse_zipfile |
| [965774](https://hackerone.com/reports/965774) | Open-Xchange |  | - | 0 |  | NULL Pointer Dereference | A specifically designed sieve script can cause a DoS in lib-sieve during sieve script compilation via NULL pointer dereference |
| [1564922](https://hackerone.com/reports/1564922) | curl | low | - | 0 | 2022-06-09 | Integer Overflow | Integer overflows in unescape_word() |
