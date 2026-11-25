---
title: "Memory-corruption case register — 336-row ledger + 16-row merge appendix (h1-brain corpus)"
type: register
built: "2026-11-07"
roster: "h1-brain disclosed_reports.db (3,673 rows; sha256 8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4)"
case_id_scheme: "MEM-<HackerOne report id>"
bounty_rule: "DB bounty_amount where present (labeled $) · None/- = no figure in DB (not evidence of non-payment)"
module_rule: "frozen in archive/classes.json (bodies-win classification; 352 ids = 336 bucket + 16 unclassified merges)"
corpus: "336 memory-corruption bucket rows · 145 with bounty figures · $233,652.09 bucket floor · 137 rows with CVEs"
---

# Case register — Memory Corruption

Corpus (bucket): 336 rows · 145 with bounty figures · **$233,652.09** · max $10,000 (tied: MEM-542180 valve NAV / MEM-826026 PlayStation kernel UAF / MEM-186723, MEM-189633 shopify-scripts crash crown) · evidence: 320 full-body (body >100 chars) / 16 link-only (≤100 chars). Program mix: ibb 224 · shopify-scripts 64 · valve 10 · torproject 7 · putty_h1c 5 · notepad++ 4 · nodejs 4 · ruby 3 · curl 3 · vlc_h1c/kubernetes/brave 2 each · rest 1 each. Weakness labels (DB): Memory Corruption - Generic 185 · Buffer Over-read 34 · Heap Overflow 27 · Use After Free 26 · Classic Buffer Overflow 21 · NULL Pointer Dereference 18 · Out-of-bounds Read 14 · Stack Overflow 11. (DB weakness label verified identical to the classifier `src` on all 336 rows, 0 mismatches.)

Class census (frozen `classes.json`): Heap-Class-Classic-Overflow 115 (542180 valve crown … 2974850 curl heap) · Use-After-Free-and-Double-Free 53 (826026 kernel UAF … 1997312 curl UAF) · Out-of-Bounds-Overread-Reads 68 (807772 valve → 2621062 curl punycode) · Integer-Overflow-and-Type-Confusion 33 (127242 mbstring … 271330 format-string) · Null-Deref-and-Stack-Crashes 59 (186723/189633 crash crown … 2070810 libssh) · Adjacent-and-Unclassified 24 (8 bucket-adjacent + 16 merge appendix — 8 bucket-adjacent rows above includes 192896/181319/203595/380102/484930/503821/1217702/2779070; the 16 merge rows are appendix below).

Bounty arithmetic (bucket): Heap $76,572.81/44 · UAF $41,300/23 · OOB $30,192/27 · Int $10,100/19 · Null $74,487.28/31 · Adjacent $1,000/1 → $233,652.09/145 bucket. Merge appendix: $17,000/10 (10 × GHSL query rows $500–$4,500, 0 paid merges among 6 non-GHSL rows). **Vault total: $250,652.09 / 155 rows.**

Full-bucket row table (336 rows). Columns: Case | Team | Weakness (DB) | CVE | Bounty | Module | Title.

| Case | Team | Weakness | CVE | Bounty | Module | Title |
|---|---|---|---|---|---|---|
| [MEM-18843](https://hackerone.com/reports/18843) | ibb | Memory Corruption - Generic | — | - | UAF | use-after-free vulnerability in Flash Player |
| [MEM-37240](https://hackerone.com/reports/37240) | ibb | Memory Corruption - Generic | CVE-2014-0574 | - | UAF | Race condition in Flash workers may cause an exploitabl​e double free |
| [MEM-56385](https://hackerone.com/reports/56385) | ibb | Memory Corruption - Generic | CVE-2015-0346 | $5,000 | UAF | Double free vulnerability in Flash Player Settings Manager (CVE-2015-0346) |
| [MEM-66962](https://hackerone.com/reports/66962) | ibb | Memory Corruption - Generic | CVE-2015-3100 | - | Heap | Misusing of FPU Instruction Could Cause Security Vulnerabilities in Adobe Flash Player |
| [MEM-110720](https://hackerone.com/reports/110720) | ibb | Memory Corruption - Generic | — | $500 | OOB | Arbitary Memory Read via gdImageRotateInterpolated Array Index Out of Bounds |
| [MEM-110722](https://hackerone.com/reports/110722) | ibb | Memory Corruption - Generic | — | $500 | Heap | Heap BufferOver Flow in escapeshellargs and escapeshellcmd functions |
| [MEM-112386](https://hackerone.com/reports/112386) | torproject | Memory Corruption - Generic | — | - | Heap | smartlist_add, smartlist_insert (may) cause heap corruption as a result of inadequate checks in smartlist_ensure_capacity |
| [MEM-112632](https://hackerone.com/reports/112632) | torproject | Memory Corruption - Generic | — | - | OOB | [tor] libevent dns remote stack overread vulnerability |
| [MEM-112784](https://hackerone.com/reports/112784) | torproject | Memory Corruption - Generic | — | - | Heap | libevent (stack) buffer overflow in evutil_parse_sockaddr_port |
| [MEM-113120](https://hackerone.com/reports/113120) | ibb | Memory Corruption - Generic | — | - | Null | An integer overflow bug in php_implode() could lead heap overflow, make PHP to crash |
| [MEM-113122](https://hackerone.com/reports/113122) | ibb | Memory Corruption - Generic | — | - | Int | An integer overflow bug in php_str_to_str_ex() led arbitrary code execution. |
| [MEM-113268](https://hackerone.com/reports/113268) | ibb | Memory Corruption - Generic | — | - | Int | Integer overflow in wordwrap |
| [MEM-114414](https://hackerone.com/reports/114414) | ibb | Memory Corruption - Generic | — | - | OOB | openssl_seal() uninitialized memory usage |
| [MEM-115702](https://hackerone.com/reports/115702) | torproject | Memory Corruption - Generic | — | - | Heap | [tor] libevent dns OOB read |
| [MEM-119652](https://hackerone.com/reports/119652) | ibb | Memory Corruption - Generic | CVE-2016-0981 | $5,000 | Heap | Adobe Flash Player ASnative(101,10) Memory Corruption Vulnerability |
| [MEM-119653](https://hackerone.com/reports/119653) | ibb | Memory Corruption - Generic | CVE-2016-0982 | $2,000 | UAF | Adobe Flash Player ASnative(900,1).call(MovieClip) Use-After-Free Vulnerability |
| [MEM-119655](https://hackerone.com/reports/119655) | ibb | Memory Corruption - Generic | CVE-2016-0983 | $2,000 | UAF | Adobe Flash Player ASnative(900,1).call(TextField) Use-After-Free Vulnerability |
| [MEM-119657](https://hackerone.com/reports/119657) | ibb | Memory Corruption - Generic | CVE-2015-3103 | $2,000 | Heap | Adobe Flash Player Race Condition Vulnerability |
| [MEM-122254](https://hackerone.com/reports/122254) | ibb | Memory Corruption - Generic | CVE-2016-0990 | $2,000 | UAF | Adobe Flash Player TextField Use-After-Free Vulnerability |
| [MEM-122256](https://hackerone.com/reports/122256) | ibb | Memory Corruption - Generic | CVE-2016-0992 | - | Heap | Adobe Flash Player  Uninitialised Memory Corruption |
| [MEM-126797](https://hackerone.com/reports/126797) | torproject | Memory Corruption - Generic | CVE-2016-1964 | $300 | UAF | Use-after-free during XML transformations (MFSA-2016-27) |
| [MEM-127242](https://hackerone.com/reports/127242) | ibb | Memory Corruption - Generic | — | $1,000 | Int | Negative size parameter (-1) in memcpy mbfl_strcut |
| [MEM-135291](https://hackerone.com/reports/135291) | ibb | Memory Corruption - Generic | — | $500 | OOB | Out-of-bounds reads in zif_grapheme_stripos with negative offset |
| [MEM-135293](https://hackerone.com/reports/135293) | ibb | Memory Corruption - Generic | — | $500 | Int | bcpowmod accepts negative scale and corrupts _one_ definition |
| [MEM-135294](https://hackerone.com/reports/135294) | ibb | Memory Corruption - Generic | — | $500 | Null | xml_parse_into_struct segmentation fault |
| [MEM-138025](https://hackerone.com/reports/138025) | torproject | Memory Corruption - Generic | — | - | Heap | Heap corruption via memarea.c |
| [MEM-138516](https://hackerone.com/reports/138516) | ibb | Memory Corruption - Generic | CVE-2016-1098 | $2,000 | Heap | Adobe Flash Player ContentFactory class Memory Corruption Vulnerability |
| [MEM-138517](https://hackerone.com/reports/138517) | ibb | Memory Corruption - Generic | CVE-2016-1099 | $2,000 | Heap | Adobe Flash Player Metadata class Memory Corruption Vulnerability |
| [MEM-138518](https://hackerone.com/reports/138518) | ibb | Memory Corruption - Generic | CVE-2016-1100 | $2,000 | Heap | Adobe Flash Player OpportunityGenerator class Memory Corruption Vulnerability |
| [MEM-139879](https://hackerone.com/reports/139879) | ibb | Memory Corruption - Generic | CVE-2016-4121 | - | Heap | Adobe Flash Player Regular Expression UAF Remote Code Execution Vulnerability |
| [MEM-141197](https://hackerone.com/reports/141197) | ibb | Memory Corruption - Generic | — | $500 | OOB | get_icu_value_internal out-of-bounds read |
| [MEM-141202](https://hackerone.com/reports/141202) | ibb | Memory Corruption - Generic | — | $500 | OOB | imagescale out-of-bounds read |
| [MEM-141212](https://hackerone.com/reports/141212) | ibb | Memory Corruption - Generic | — | $500 | Int | Integer underflow / arbitrary null write in fread/gzread |
| [MEM-141839](https://hackerone.com/reports/141839) | ibb | Memory Corruption - Generic | — | - | Heap | Multiple vulnerabilities related to PCRE functions (already fixed) |
| [MEM-142472](https://hackerone.com/reports/142472) | ibb | Memory Corruption - Generic | CVE-2016-2177 | - | Heap | CVE-2016-2177 Undefined pointer arithmetic in SSL code |
| [MEM-143234](https://hackerone.com/reports/143234) | ibb | Memory Corruption - Generic | — | $500 | Int | Integer Overflow in _gd2GetHeader() resulting in heap overflow |
| [MEM-145265](https://hackerone.com/reports/145265) | ibb | Memory Corruption - Generic | CVE-2016-4150 | $2,000 | Heap | Adobe Flash Player ShimContentFactory class Memory Corruption Vulnerability |
| [MEM-145266](https://hackerone.com/reports/145266) | ibb | Memory Corruption - Generic | CVE-2016-4151 | $2,000 | Heap | Adobe Flash Player ShimContentFactory.retrieveResolvers Memory Corruption Vulnerability |
| [MEM-145267](https://hackerone.com/reports/145267) | ibb | Memory Corruption - Generic | CVE-2016-4152 | $2,000 | Heap | Adobe Flash Player ShimContentResolver.configure Memory Corruption Vulnerability |
| [MEM-145269](https://hackerone.com/reports/145269) | ibb | Memory Corruption - Generic | CVE-2016-4153 | $2,000 | Heap | Adobe Flash Player ShimOpportunityGenerator class Memory Corruption Vulnerability |
| [MEM-145271](https://hackerone.com/reports/145271) | ibb | Memory Corruption - Generic | CVE-2016-4154 | $2,000 | Heap | Adobe Flash Player ShimContentResolver(resolverType=0) class Memory Corruption Vulnerability |
| [MEM-145272](https://hackerone.com/reports/145272) | ibb | Memory Corruption - Generic | CVE-2016-4155 | $2,000 | Heap | Adobe Flash Player ShimContentResolver(resolverType=1) class Memory Corruption Vulnerability |
| [MEM-146200](https://hackerone.com/reports/146200) | ibb | Memory Corruption - Generic | — | - | UAF | _php_mb_regex_ereg_replace_exec - double free |
| [MEM-146360](https://hackerone.com/reports/146360) | ibb | Memory Corruption - Generic | — | - | Int | Heap Overflow Due To Integer Overflow |
| [MEM-146940](https://hackerone.com/reports/146940) | ibb | Memory Corruption - Generic | — | $500 | OOB | pass2_no_dither out-of-bounds access |
| [MEM-151039](https://hackerone.com/reports/151039) | ibb | Memory Corruption - Generic | CVE-2016-4182 | $5,000 | Heap | Adobe Flash Player TimedEvent.parent Memory Corruption Vulnerability |
| [MEM-151040](https://hackerone.com/reports/151040) | ibb | Memory Corruption - Generic | CVE-2016-4188 | $2,000 | Heap | Adobe Flash Player ShimAdPolicySelector(adPolicySelectorType=0) class Memory Corruption |
| [MEM-151043](https://hackerone.com/reports/151043) | ibb | Memory Corruption - Generic | CVE-2016-4248 | $5,000 | UAF | Adobe Flash Player PSDK Class Use After Free Vulnerability |
| [MEM-152231](https://hackerone.com/reports/152231) | ibb | Memory Corruption - Generic | — | - | OOB | Out of bound read in exif_process_IFD_in_MAKERNOTE |
| [MEM-152232](https://hackerone.com/reports/152232) | ibb | Memory Corruption - Generic | — | - | Null | NULL Pointer Dereference in exif_process_user_comment |
| [MEM-152266](https://hackerone.com/reports/152266) | ibb | Memory Corruption - Generic | — | - | UAF | Use After Free Vulnerability in SNMP with GC and unserialize() |
| [MEM-152281](https://hackerone.com/reports/152281) | ibb | Memory Corruption - Generic | — | - | UAF | Use After Free/Double Free in Garbage Collection |
| [MEM-152782](https://hackerone.com/reports/152782) | ibb | Memory Corruption - Generic | — | $500 | OOB | locale_accept_from_http out-of-bounds access |
| [MEM-152784](https://hackerone.com/reports/152784) | ibb | Memory Corruption - Generic | — | $500 | OOB | imagegif/output out-of-bounds access |
| [MEM-153776](https://hackerone.com/reports/153776) | ibb | Memory Corruption - Generic | — | $500 | Heap | gdImageTrueColorToPaletteBody allows arbitrary write/read access |
| [MEM-155223](https://hackerone.com/reports/155223) | ibb | Memory Corruption - Generic | — | - | UAF | Use After Free Vulnerability in array_walk()/array_walk_recursive() |
| [MEM-159690](https://hackerone.com/reports/159690) | ibb | Memory Corruption - Generic | — | - | Null | stack buffer overflows in the curses module |
| [MEM-159948](https://hackerone.com/reports/159948) | ibb | Memory Corruption - Generic | — | - | UAF | Use After Free Vulnerability in unserialize() |
| [MEM-159953](https://hackerone.com/reports/159953) | ibb | Memory Corruption - Generic | — | $500 | Int | integer overflow in curl_escape caused heap corruption |
| [MEM-159954](https://hackerone.com/reports/159954) | ibb | Memory Corruption - Generic | — | $500 | Int | integer overflow in base64_decode caused heap corruption |
| [MEM-159955](https://hackerone.com/reports/159955) | ibb | Memory Corruption - Generic | — | $500 | Int | integer overflow in bzdecompress caused heap corruption |
| [MEM-159992](https://hackerone.com/reports/159992) | ibb | Memory Corruption - Generic | — | - | Heap | memory allocator fails to realloc small block to large one |
| [MEM-160294](https://hackerone.com/reports/160294) | ibb | Memory Corruption - Generic | CVE-2016-7128 | - | OOB | Memory Leakage In exif_process_IFD_in_TIFF (CVE-2016-7128) |
| [MEM-160295](https://hackerone.com/reports/160295) | ibb | Memory Corruption - Generic | — | - | Heap | Heap overflow in curl_escape |
| [MEM-161189](https://hackerone.com/reports/161189) | ibb | Memory Corruption - Generic | — | $1,000 | OOB | select_colors write out-of-bounds |
| [MEM-161193](https://hackerone.com/reports/161193) | ibb | Memory Corruption - Generic | — | $1,000 | Heap | imagegammacorrect allows arbitrary write access |
| [MEM-161198](https://hackerone.com/reports/161198) | ibb | Memory Corruption - Generic | — | $500 | Null | wddx_deserialize null dereference with invalid xml |
| [MEM-161200](https://hackerone.com/reports/161200) | ibb | Memory Corruption - Generic | — | $500 | Int | wddx_deserialize allows illegal memory access |
| [MEM-161216](https://hackerone.com/reports/161216) | ibb | Memory Corruption - Generic | — | $500 | Null | wddx_deserialize null dereference |
| [MEM-161217](https://hackerone.com/reports/161217) | ibb | Memory Corruption - Generic | — | $500 | Null | wddx_deserialize null dereference in php_wddx_pop_element |
| [MEM-163459](https://hackerone.com/reports/163459) | torproject | Memory Corruption - Generic | — | - | Heap | potential memory corruption in or/buffers.c (particularly on 32 bit) |
| [MEM-167888](https://hackerone.com/reports/167888) | ibb | Memory Corruption - Generic | — | - | OOB | Uninitialized Thumbail Data Leads To Memory Leakage in exif_process_IFD_in_TIFF |
| [MEM-167895](https://hackerone.com/reports/167895) | ibb | Memory Corruption - Generic | — | - | OOB | Out of bound when verify signature of zip phar in phar_parse_zipfile |
| [MEM-167896](https://hackerone.com/reports/167896) | ibb | Memory Corruption - Generic | — | - | OOB | Out of bound when verify signature of tar phar in phar_parse_tarfile |
| [MEM-167903](https://hackerone.com/reports/167903) | ibb | Memory Corruption - Generic | — | $500 | Int | integer overflow in str_pad caused heap corruption |
| [MEM-167904](https://hackerone.com/reports/167904) | ibb | Memory Corruption - Generic | — | $500 | Heap | heap overflow in substr_replace |
| [MEM-167905](https://hackerone.com/reports/167905) | ibb | Memory Corruption - Generic | — | $500 | Int | integer overflow in pg_escape_bytea caused heap corruption |
| [MEM-167906](https://hackerone.com/reports/167906) | ibb | Memory Corruption - Generic | — | $500 | Int | integer overflow in imap_binary caused heap corruption |
| [MEM-167907](https://hackerone.com/reports/167907) | ibb | Memory Corruption - Generic | — | $500 | Int | integer overflow in preg_quote caused heap corruption |
| [MEM-167908](https://hackerone.com/reports/167908) | ibb | Memory Corruption - Generic | — | $500 | Int | integer overflow in fgets cause heap corruption |
| [MEM-167910](https://hackerone.com/reports/167910) | ibb | Memory Corruption - Generic | — | $500 | Heap | memory corruption in wordwrap function |
| [MEM-167911](https://hackerone.com/reports/167911) | ibb | Memory Corruption - Generic | — | $500 | Int | integer overflow in fgetcsv caused heap corruption |
| [MEM-167921](https://hackerone.com/reports/167921) | ibb | Memory Corruption - Generic | — | - | Int | integer overflow in xml_utf8_encode |
| [MEM-167931](https://hackerone.com/reports/167931) | ibb | Memory Corruption - Generic | — | - | Int | Memory Corruption in During Deserialized-object Destruction |
| [MEM-167977](https://hackerone.com/reports/167977) | ibb | Memory Corruption - Generic | — | - | Int | Missing type check when unserializing SplArray |
| [MEM-168485](https://hackerone.com/reports/168485) | irccloud | Memory Corruption - Generic | CVE-2014-0133 | - | Heap | Exposed, outdated nginx server (v1.4.6) potentially vulnerable to heap-based buffer overflow & RCE |
| [MEM-170138](https://hackerone.com/reports/170138) | ibb | Memory Corruption - Generic | — | $1,000 | Heap | SEH buffer overflow msgfmt_format_message |
| [MEM-170144](https://hackerone.com/reports/170144) | ibb | Memory Corruption - Generic | — | $500 | UAF | wddx_deserialize use-after-free |
| [MEM-170260](https://hackerone.com/reports/170260) | ibb | Memory Corruption - Generic | — | $500 | Heap | imap_rfc822_parse_headers GS Violation |
| [MEM-170618](https://hackerone.com/reports/170618) | ibb | Memory Corruption - Generic | CVE-2016-7418 | - | OOB | CVE-2016-7418 PHP Out-Of-Bounds Read in php_wddx_push_element |
| [MEM-170619](https://hackerone.com/reports/170619) | ibb | Memory Corruption - Generic | — | - | Int | PHP Integer Overflow in gdImageWebpCtx |
| [MEM-172115](https://hackerone.com/reports/172115) | ibb | Memory Corruption - Generic | — | - | UAF | Multiple use after frees in obj2ast_* methods |
| [MEM-172403](https://hackerone.com/reports/172403) | ibb | Memory Corruption - Generic | — | - | Heap | Python 2.7 32-bit JSON encoding heap corruption |
| [MEM-172411](https://hackerone.com/reports/172411) | ibb | Memory Corruption - Generic | CVE-2016-7398 | - | Int | Heap overflow caused by type confusion vulnerability in merge_param() |
| [MEM-172562](https://hackerone.com/reports/172562) | ibb | Memory Corruption - Generic | — | $1,500 | UAF | LZMADecompressor.decompress Use After Free |
| [MEM-174069](https://hackerone.com/reports/174069) | ibb | Memory Corruption - Generic | CVE-2016-7961 | - | Heap | Buffer overflow in HTTP parse_hostinfo(), parse_userinfo() and parse_scheme() |
| [MEM-175091](https://hackerone.com/reports/175091) | ibb | Memory Corruption - Generic | — | $1,000 | Int | chain.__setstate__ Type Confusion |
| [MEM-175310](https://hackerone.com/reports/175310) | ibb | Memory Corruption - Generic | — | $500 | OOB | Write out-of-bounds at number_format |
| [MEM-175311](https://hackerone.com/reports/175311) | ibb | Memory Corruption - Generic | — | $500 | Int | memcpy negative size parameter in php_resolve_path |
| [MEM-175312](https://hackerone.com/reports/175312) | ibb | Memory Corruption - Generic | — | $500 | Int | memcpy negative parameter _bc_new_num_ex |
| [MEM-175315](https://hackerone.com/reports/175315) | ibb | Memory Corruption - Generic | — | $500 | Heap | Illegal write access through Locale methods |
| [MEM-175316](https://hackerone.com/reports/175316) | ibb | Memory Corruption - Generic | — | $500 | Null | stack-buffer-overflow through "ResourceBundle" methods |
| [MEM-175587](https://hackerone.com/reports/175587) | ibb | Memory Corruption - Generic | — | $1,500 | Null | Stack Buffer Overflow in GD dynamicGetbuf |
| [MEM-175982](https://hackerone.com/reports/175982) | ibb | Memory Corruption - Generic | — | - | UAF | Use-after-free in unserialize() |
| [MEM-176226](https://hackerone.com/reports/176226) | ibb | Memory Corruption - Generic | — | - | Null | CachingIterator null dereference when convert to string |
| [MEM-176279](https://hackerone.com/reports/176279) | ibb | Memory Corruption - Generic | CVE-2016-7412 | - | Heap | Heap overflow in mysqlnd related to BIT fields (CVE-2016-7412) |
| [MEM-178094](https://hackerone.com/reports/178094) | ibb | Memory Corruption - Generic | — | $500 | Int | php_snmp_parse_oid integer overflow in memory allocation |
| [MEM-178144](https://hackerone.com/reports/178144) | ibb | Memory Corruption - Generic | — | $500 | OOB | imagecropauto out-of-bounds access |
| [MEM-180562](https://hackerone.com/reports/180562) | ibb | Memory Corruption - Generic | — | - | Heap | Memory corruption in _php_math_number_format_ex() |
| [MEM-180563](https://hackerone.com/reports/180563) | ibb | Memory Corruption - Generic | — | - | Int | Heap overflow due to integer overflow in bzdecompress() function |
| [MEM-180572](https://hackerone.com/reports/180572) | ibb | Memory Corruption - Generic | — | - | Heap | Memory corruption due to missing check size in _php_math_number_format_ex() |
| [MEM-180582](https://hackerone.com/reports/180582) | ibb | Memory Corruption - Generic | — | - | Int | Heap overflow due to integer overflow in php_escape_html_entities_ex() function |
| [MEM-180584](https://hackerone.com/reports/180584) | ibb | Memory Corruption - Generic | — | - | Int | Heap overflow due to integer overflow in pg_escape_string() function |
| [MEM-180908](https://hackerone.com/reports/180908) | ibb | Memory Corruption - Generic | — | - | Null | NULL Pointer Dereference in WDDX Packet Deserialization with PDORow |
| [MEM-180909](https://hackerone.com/reports/180909) | ibb | Use After Free | — | - | UAF | Use-after-free in ArrayObject Deserialization |
| [MEM-181073](https://hackerone.com/reports/181073) | ibb | Memory Corruption - Generic | — | - | Int | malloc negative size parameter |
| [MEM-181319](https://hackerone.com/reports/181319) | shopify-scripts | Memory Corruption - Generic | — | - | Adjacent | Memory disclosure in mruby String#lines method |
| [MEM-182140](https://hackerone.com/reports/182140) | ibb | Memory Corruption - Generic | CVE-2016-9297 | - | Null | libtiff 4.0.6 segfault / read outside of buffer (CVE-2016-9297) |
| [MEM-182420](https://hackerone.com/reports/182420) | ibb | Memory Corruption - Generic | — | $500 | Heap | Illegal write/read access caused by gdImageAALine overflow |
| [MEM-182474](https://hackerone.com/reports/182474) | ibb | Memory Corruption - Generic | — | - | UAF | Use After Free in PHP7 unserialize() |
| [MEM-183239](https://hackerone.com/reports/183239) | shopify-scripts | Memory Corruption - Generic | — | - | Null | SIGSEGV on mruby's mark_tbl() (Invalid memory access) |
| [MEM-184661](https://hackerone.com/reports/184661) | shopify-scripts | Memory Corruption - Generic | — | $8,000 | Null | mruby-time: Crash host with uninitialized Time obj |
| [MEM-184715](https://hackerone.com/reports/184715) | shopify-scripts | Memory Corruption - Generic | — | $1,000 | UAF | Read after free in mrb_vm_exec with OP_ARYCAT reading R(B) |
| [MEM-184857](https://hackerone.com/reports/184857) | shopify-scripts | Memory Corruption - Generic | — | $8,000 | Null | Crash: calling Proc::initialize_copy with a Proc instance where initialize never ran leads to a crash |
| [MEM-185794](https://hackerone.com/reports/185794) | shopify-scripts | Memory Corruption - Generic | — | $8,000 | Null | Crash: mrb_any_to_s can't handle NilClass, Symbol and Fixnum |
| [MEM-185957](https://hackerone.com/reports/185957) | shopify-scripts | Memory Corruption - Generic | — | $1,000 | Null | Crash: A call to Symbol.new leads to a crash when inspecting the resulting object |
| [MEM-186723](https://hackerone.com/reports/186723) | shopify-scripts | Memory Corruption - Generic | — | $10,000 | Null | Crash: Overwriting NoMethodError with a builtin class crashes/corrupts memory |
| [MEM-188102](https://hackerone.com/reports/188102) | ibb | Memory Corruption - Generic | — | $1,500 | Heap | 3 heap corruptions in PHP |
| [MEM-188661](https://hackerone.com/reports/188661) | ibb | Memory Corruption - Generic | — | - | OOB | Invalid read when wddx decodes empty boolean element |
| [MEM-189633](https://hackerone.com/reports/189633) | shopify-scripts | Memory Corruption - Generic | — | $10,000 | Null | Certain inputs cause tight C-level recursion leading to process stack overflow |
| [MEM-190933](https://hackerone.com/reports/190933) | ibb | Memory Corruption - Generic | — | $500 | Heap | Invalid parameter in memcpy function trough openssl_pbkdf2 |
| [MEM-191994](https://hackerone.com/reports/191994) | shopify-scripts | Memory Corruption - Generic | — | - | Null | SIGSEGV mrb_obj_freeze() Manipulating Register RAX and RSI |
| [MEM-192127](https://hackerone.com/reports/192127) | ruby | Memory Corruption - Generic | — | $500 | Heap | Buffer underflow in sprintf |
| [MEM-192235](https://hackerone.com/reports/192235) | shopify-scripts | Memory Corruption - Generic | — | $100 | Int | Integer Overflow in mrb_ary_set |
| [MEM-192318](https://hackerone.com/reports/192318) | shopify-scripts | Memory Corruption - Generic | — | - | Heap | mrb_vformat() heap overflow could lead to code execution |
| [MEM-192362](https://hackerone.com/reports/192362) | shopify-scripts | Memory Corruption - Generic | — | $800 | Heap | Heap Overflow in mrb_arb_splice |
| [MEM-192578](https://hackerone.com/reports/192578) | shopify-scripts | Memory Corruption - Generic | — | - | Null | kh_get_n2s() stack overrun |
| [MEM-192665](https://hackerone.com/reports/192665) | shopify-scripts | Memory Corruption - Generic | — | - | Heap | heap-buffer-overflow on mruby |
| [MEM-192896](https://hackerone.com/reports/192896) | shopify-scripts | Memory Corruption - Generic | — | $1,000 | Adjacent | Memory disclosure in timegm |
| [MEM-193143](https://hackerone.com/reports/193143) | shopify-scripts | Memory Corruption - Generic | — | $800 | UAF | Use After Free in str_replace |
| [MEM-193517](https://hackerone.com/reports/193517) | shopify-scripts | Memory Corruption - Generic | — | - | UAF | attempting double-free using the mruby compiler `mrbc` |
| [MEM-193719](https://hackerone.com/reports/193719) | shopify-scripts | Memory Corruption - Generic | — | $200 | UAF | Double free of filename after codegen error |
| [MEM-193773](https://hackerone.com/reports/193773) | shopify-scripts | Memory Corruption - Generic | — | - | Heap | SIGABRT - mrb_default_allocf |
| [MEM-194884](https://hackerone.com/reports/194884) | shopify-scripts | Memory Corruption - Generic | — | $200 | UAF | Heap use-after-free during range creation |
| [MEM-194906](https://hackerone.com/reports/194906) | shopify-scripts | Memory Corruption - Generic | — | $800 | Heap | Heap overflow due to off-by-one when expanding stack |
| [MEM-195586](https://hackerone.com/reports/195586) | ibb | Memory Corruption - Generic | — | - | Heap | Memory corruption when parsing a hostile PHAR archive |
| [MEM-195688](https://hackerone.com/reports/195688) | ibb | NULL Pointer Dereference | CVE-2016-10162 | - | Null | NULL Pointer Dereference while unserialize php object |
| [MEM-196380](https://hackerone.com/reports/196380) | shopify-scripts | Memory Corruption - Generic | — | - | Null | SIGSEGV in mrb_vm_exec |
| [MEM-196498](https://hackerone.com/reports/196498) | shopify-scripts | Memory Corruption - Generic | — | - | Null | Segmentation fault on program counter |
| [MEM-198452](https://hackerone.com/reports/198452) | shopify-scripts | Memory Corruption - Generic | — | - | Heap | SIGABRT - mrb_realloc_simple - gc.c - line:201 |
| [MEM-198732](https://hackerone.com/reports/198732) | ibb | Use After Free | — | - | UAF | Use After Free in unserialize() |
| [MEM-200821](https://hackerone.com/reports/200821) | shopify-scripts | Memory Corruption - Generic | — | $100 | UAF | heap-use-after-free /home/operac/testafl/mruby/mrubylast/mruby/src/gc.c |
| [MEM-200909](https://hackerone.com/reports/200909) | ibb | Out-of-bounds Read | CVE-2016-10161 | $500 | OOB | Out of bounds memory read in unserialize() |
| [MEM-201897](https://hackerone.com/reports/201897) | shopify-scripts | Memory Corruption - Generic | — | $2,000 | Null | Recursion causing uninitialized memory reads leading to a segfault |
| [MEM-202960](https://hackerone.com/reports/202960) | ibb | Memory Corruption - Generic | CVE-2017-5204 | - | Heap | CVE-2017-5204: The IPv6 parser in tcpdump before 4.9.0 has a buffer overflow in print-ip6.c:ip6_print() |
| [MEM-202965](https://hackerone.com/reports/202965) | ibb | Memory Corruption - Generic | CVE-2017-5341 | - | Heap | CVE-2017-5341 The OTV parser in tcpdump before 4.9.0 has a buffer overflow in print-otv.c:otv_print() |
| [MEM-202967](https://hackerone.com/reports/202967) | ibb | Memory Corruption - Generic | CVE-2017-5484 | - | Heap | CVE-2017-5484 The ATM parser in tcpdump before 4.9.0 has a buffer overflow in print-atm.c:sig_print() |
| [MEM-202968](https://hackerone.com/reports/202968) | ibb | Memory Corruption - Generic | CVE-2017-5342 | - | Heap | CVE-2017-5342 In tcpdump before 4.9.0 a bug in multiple protocol parsers could cause a buffer overflow in print-ether.c:ether_print() |
| [MEM-202969](https://hackerone.com/reports/202969) | ibb | Memory Corruption - Generic | CVE-2017-5482, CVE-2016-8575 | - | Heap | CVE-2017-5482 The Q.933 parser in tcpdump before 4.9.0 has a buffer overflow in print-fr.c:q933_print(). |
| [MEM-203002](https://hackerone.com/reports/203002) | ibb | Memory Corruption - Generic | — | $500 | UAF | Incorrect GC behavior in xxlimited could lead to use-after-free |
| [MEM-203595](https://hackerone.com/reports/203595) | shopify-scripts | Memory Corruption - Generic | — | - | Adjacent | forgot to add the patch |
| [MEM-204421](https://hackerone.com/reports/204421) | shopify-scripts | Memory Corruption - Generic | — | $800 | Heap | Heap buffer oveflow with many arguments |
| [MEM-205284](https://hackerone.com/reports/205284) | shopify-scripts | Memory Corruption - Generic | — | - | Heap | SIGABRT - method_missing - mark_context_stack |
| [MEM-206109](https://hackerone.com/reports/206109) | shopify-scripts | Memory Corruption - Generic | — | - | UAF | mruby heap use-after-free |
| [MEM-207710](https://hackerone.com/reports/207710) | shopify-scripts | Memory Corruption - Generic | — | - | UAF | Heap use-after-free in mrb_vm_exec |
| [MEM-207983](https://hackerone.com/reports/207983) | ibb | Heap Overflow | — | - | Heap | read outside of buffer (heap buffer overflow) in S_regmatch - regexec.c:6057 |
| [MEM-208363](https://hackerone.com/reports/208363) | shopify-scripts | Memory Corruption - Generic | — | $100 | Heap | Memory corrouption in mrb_gc_mark |
| [MEM-209765](https://hackerone.com/reports/209765) | shopify-scripts | Memory Corruption - Generic | — | - | Heap | Heap buffer overflow in mruby value_move |
| [MEM-209937](https://hackerone.com/reports/209937) | shopify-scripts | Memory Corruption - Generic | — | - | Null | SIGSEGV - mark_context_stack |
| [MEM-209949](https://hackerone.com/reports/209949) | ruby | Memory Corruption - Generic | CVE-2017-14064 | - | OOB | Arbitrary heap exposure in JSON.generate |
| [MEM-212241](https://hackerone.com/reports/212241) | ruby | Memory Corruption - Generic | CVE-2017-0898 | - | Int | sprintf combined format string attack |
| [MEM-212882](https://hackerone.com/reports/212882) | shopify-scripts | Memory Corruption - Generic | — | - | Heap | SIGABRT in only mirb |
| [MEM-213255](https://hackerone.com/reports/213255) | shopify-scripts | Memory Corruption - Generic | — | - | Null | SIGSEGV in str_buf_cat |
| [MEM-214000](https://hackerone.com/reports/214000) | shopify-scripts | Memory Corruption - Generic | — | - | Heap | SIGABRT - mirb and mruby |
| [MEM-214681](https://hackerone.com/reports/214681) | shopify-scripts | NULL Pointer Dereference | — | $800 | Null | Null pointer dereference in ary_concat |
| [MEM-214845](https://hackerone.com/reports/214845) | shopify-scripts | NULL Pointer Dereference | — | - | Null | SIGSEGV in mrb_vm_exec |
| [MEM-215447](https://hackerone.com/reports/215447) | shopify-scripts | NULL Pointer Dereference | — | - | Null | SIGSEGV in mrb_class |
| [MEM-215891](https://hackerone.com/reports/215891) | shopify-scripts | NULL Pointer Dereference | — | $800 | Null | Null pointer dereference in mrb_class |
| [MEM-215967](https://hackerone.com/reports/215967) | shopify-scripts | Memory Corruption - Generic | — | - | Heap | SIGABRT in mrb_debug_info_append_file |
| [MEM-216151](https://hackerone.com/reports/216151) | ibb | Use After Free | — | $500 | UAF | Use-after-free in _asyncio_Future_remove_done_callback |
| [MEM-216725](https://hackerone.com/reports/216725) | shopify-scripts | Memory Corruption - Generic | — | - | Heap | SIGABRT - in free |
| [MEM-217083](https://hackerone.com/reports/217083) | shopify-scripts | NULL Pointer Dereference | — | - | Null | SIGSEGV in mrb_str_inum |
| [MEM-217097](https://hackerone.com/reports/217097) | shopify-scripts | NULL Pointer Dereference | — | - | Null | SIGSEGV in mrb_vm_exec |
| [MEM-217610](https://hackerone.com/reports/217610) | shopify-scripts | Memory Corruption - Generic | — | $800 | Null | kh_put_iv SEGFAULT - mruby 1.2.0 |
| [MEM-218233](https://hackerone.com/reports/218233) | shopify-scripts | NULL Pointer Dereference | — | $800 | Null | Null pointer dereference in OP_ENTER |
| [MEM-218567](https://hackerone.com/reports/218567) | shopify-scripts | Memory Corruption - Generic | — | $800 | Null | SIGSEGV in array_copy - array.c:71 |
| [MEM-218803](https://hackerone.com/reports/218803) | shopify-scripts | Memory Corruption - Generic | — | $100 | Heap | SIGABRT in sym_validate_len - symbol.c:44 |
| [MEM-219870](https://hackerone.com/reports/219870) | shopify-scripts | Stack Overflow | — | - | Null | mirb only: stack-buffer-overflow (OOB write) in main() |
| [MEM-221251](https://hackerone.com/reports/221251) | shopify-scripts | Heap Overflow | — | - | Heap | heap-buffer-overflow (read outside of buffer) in mrb_vm_exec() |
| [MEM-221785](https://hackerone.com/reports/221785) | ibb | Heap Overflow | CVE-2016-6303 | - | Heap | OOB write in MDC2_Update() (CVE-2016-6303) |
| [MEM-221788](https://hackerone.com/reports/221788) | ibb | Heap Overflow | CVE-2016-2182 | - | Heap | OOB write in BN_bn2dec() (CVE-2016-2182) |
| [MEM-221789](https://hackerone.com/reports/221789) | ibb | Out-of-bounds Read | CVE-2016-2180 | - | OOB | OOB read in TS_OBJ_print_bio() (CVE-2016-2180) |
| [MEM-221790](https://hackerone.com/reports/221790) | ibb | Out-of-bounds Read | CVE-2016-6306 | - | OOB | Certificate message OOB reads (CVE-2016-6306) |
| [MEM-222294](https://hackerone.com/reports/222294) | shopify-scripts | Memory Corruption - Generic | — | $800 | UAF | heap-use-after-free in mrb_vm_exec - vm.c:1247 |
| [MEM-227762](https://hackerone.com/reports/227762) | shopify-scripts | Heap Overflow | — | - | Heap | Heap Overflow in fiber_switch triggered from Fiber.transfer |
| [MEM-232150](https://hackerone.com/reports/232150) | ibb | Heap Overflow | — | - | Heap | heap-buffer-overflow (READ of size 11) in Perl 5.25.x |
| [MEM-233440](https://hackerone.com/reports/233440) | ibb | Heap Overflow | — | - | Heap | heap-buffer-overflow (READ of size 61) in Perl_re_intuit_start() |
| [MEM-237915](https://hackerone.com/reports/237915) | ibb | Heap Overflow | CVE-2017-9224, CVE-2017-9226, CVE-2017-9227, CVE-2017-9228, CVE-2017-9229 | - | Heap | PHP mbstring / Oniguruma multiple remote heap/stack corruptions |
| [MEM-241610](https://hackerone.com/reports/241610) | ibb | Buffer Over-read | CVE-2017-7668 | - | OOB | ap_find_token() Buffer Overread |
| [MEM-242354](https://hackerone.com/reports/242354) | shopify-scripts | NULL Pointer Dereference | — | $800 | Null | Null pointer dereference with send/method_missing |
| [MEM-244904](https://hackerone.com/reports/244904) | shopify-scripts | Use After Free | — | $800 | UAF | Use after free in mruby-mpdecimal |
| [MEM-245956](https://hackerone.com/reports/245956) | ibb | Use After Free | — | - | UAF | Use-after-free in PHP7's unserialize() |
| [MEM-248601](https://hackerone.com/reports/248601) | ibb | Classic Buffer Overflow | CVE-2017-11628 | - | Heap | PHP INI Parsing Stack Buffer Overflow Vulnerability |
| [MEM-248609](https://hackerone.com/reports/248609) | ibb | Heap Overflow | CVE-2017-11144 | - | Heap | PHP OpenSSL zif_openssl_seal() heap overflow (wild memcpy) |
| [MEM-248659](https://hackerone.com/reports/248659) | ibb | Buffer Over-read | CVE-2017-11145 | - | OOB | PHP WDDX Deserialization Heap OOB Read in timelib_meridian() |
| [MEM-259390](https://hackerone.com/reports/259390) | ibb | Use After Free | CVE-2017-10672 | - | UAF | Use-after-free in XML::LibXML::Node::replaceChild |
| [MEM-261335](https://hackerone.com/reports/261335) | ibb | Use After Free | CVE-2017-12932 | - | UAF | Heap Use After Free Read in unserialize() |
| [MEM-261336](https://hackerone.com/reports/261336) | ibb | Buffer Over-read | CVE-2017-12933 | - | OOB | Out of Bounds Memory Read in unserialize() |
| [MEM-261338](https://hackerone.com/reports/261338) | ibb | Use After Free | CVE-2017-12934 | - | UAF | Heap Use After Free in unserialize() |
| [MEM-268803](https://hackerone.com/reports/268803) | ibb | Buffer Over-read | CVE-2017-12985 | - | OOB | CVE-2017-12985: The IPv6 parser in tcpdump before 4.9.2 has a buffer over-read in ip6_print() |
| [MEM-268804](https://hackerone.com/reports/268804) | ibb | Buffer Over-read | CVE-2017-12986 | - | OOB | CVE-2017-12986 The IPv6 routing header parser in tcpdump before 4.9.2 has a buffer over-read in print-rt6.c:rt6_print(). |
| [MEM-268805](https://hackerone.com/reports/268805) | ibb | Buffer Over-read | CVE-2017-13008 | - | OOB | CVE-2017-13008 The IEEE 802.11 parser in tcpdump before 4.9.2 has a buffer over-read in print-802_11.c:parse_elements(). |
| [MEM-268806](https://hackerone.com/reports/268806) | ibb | Buffer Over-read | CVE-2017-13009 | - | OOB | CVE-2017-13009 The IPv6 mobility parser in tcpdump before 4.9.2 has a buffer over-read in print-mobility.c:mobility_print(). |
| [MEM-268807](https://hackerone.com/reports/268807) | ibb | Buffer Over-read | CVE-2017-13010 | - | OOB | CVE-2017-13010 The BEEP parser in tcpdump before 4.9.2 has a buffer over-read in print-beep.c:l_strnstart(). |
| [MEM-268808](https://hackerone.com/reports/268808) | ibb | Buffer Over-read | CVE-2017-13038 | - | OOB | CVE-2017-13038 The PPP parser in tcpdump before 4.9.2 has a buffer over-read in print-ppp.c:handle_mlppp(). |
| [MEM-269568](https://hackerone.com/reports/269568) | ibb | Use After Free | CVE-2017-9798 | $100 | UAF | Optionsbleed / CVE-2017-9798 |
| [MEM-271330](https://hackerone.com/reports/271330) | ibb | Memory Corruption - Generic | — | - | Int | Format string implementation vulnerability, resulting in code execution |
| [MEM-272497](https://hackerone.com/reports/272497) | ibb | Stack Overflow | CVE-2017-12814 | $1,500 | Null | Perl $ENV Key Stack Buffer Overflow |
| [MEM-283644](https://hackerone.com/reports/283644) | ibb | Buffer Over-read | CVE-2017-16642, CVE-2017-11145 | - | OOB | Out-Of-Bounds Read in timelib_meridian() |
| [MEM-295276](https://hackerone.com/reports/295276) | shopify-scripts | Use After Free | — | - | UAF | heap-use-after-free in OP_RESCUE |
| [MEM-295380](https://hackerone.com/reports/295380) | shopify-scripts | Heap Overflow | — | - | Heap | heap-buffer-overflow in OP_R_BREAK |
| [MEM-295680](https://hackerone.com/reports/295680) | shopify-scripts | Out-of-bounds Read | — | $800 | OOB | Invalid read leading to a segfault |
| [MEM-296198](https://hackerone.com/reports/296198) | shopify-scripts | Memory Corruption - Generic | — | - | Null | SEGV on ary_concat |
| [MEM-305973](https://hackerone.com/reports/305973) | ibb | NULL Pointer Dereference | — | $500 | Null | Inappropriately parsing HTTP response leads to PHP segment fault! |
| [MEM-337986](https://hackerone.com/reports/337986) | ibb | Heap Overflow | CVE-2018-6797 | - | Heap | CVE-2018-6797:  A crafted regular expression can cause a heap buffer write overflow in Perl 5 giving a remote attacker control over bytes written |
| [MEM-344035](https://hackerone.com/reports/344035) | ibb | Buffer Over-read | CVE-2018-10549 | - | OOB | Heap Buffer Overflow (READ: 1786) in exif_iif_add_value |
| [MEM-351014](https://hackerone.com/reports/351014) | valve | Classic Buffer Overflow | — | - | Heap | Malformed .BSP Access Violation in CS:GO can lead to Remote Code Execution |
| [MEM-351016](https://hackerone.com/reports/351016) | valve | Classic Buffer Overflow | — | - | Heap | Malformed Skybox .TGA in Half-Life (GoldSRC) leads to Access Violation |
| [MEM-371135](https://hackerone.com/reports/371135) | ibb | Use After Free | CVE-2018-12882 | - | UAF | CVE-2018-12882: heap-use-after-free in PHP 7.2 through 7.2.6, possible 7.2.7 |
| [MEM-380102](https://hackerone.com/reports/380102) | nextcloud | Memory Corruption - Generic | CVE-2020-8230 | - | Adjacent | Missing memory corruption protection on Windows release built |
| [MEM-384214](https://hackerone.com/reports/384214) | ibb | Heap Overflow | CVE-2018-14851 | - | Heap | heap-buffer-overflow (READ of size 48) in exif_read_data() |
| [MEM-397545](https://hackerone.com/reports/397545) | valve | Classic Buffer Overflow | — | $2,000 | Heap | Malformed .BMP file in Counter-Strike 1.6 may cause shellcode injection |
| [MEM-420115](https://hackerone.com/reports/420115) | shopify-scripts | NULL Pointer Dereference | — | $800 | Null | Crash in mrb_ary_push |
| [MEM-456727](https://hackerone.com/reports/456727) | ibb | Out-of-bounds Read | CVE-2018-19935 | - | OOB | null pointer dereference in imap_mail |
| [MEM-470520](https://hackerone.com/reports/470520) | valve | Classic Buffer Overflow | — | - | Heap | RCE on Steam Client via buffer overflow in Server Info |
| [MEM-475499](https://hackerone.com/reports/475499) | ibb | Buffer Over-read | CVE-2019-9021 | - | OOB | heap buffer overflow in phar_detect_phar_fname_ext |
| [MEM-476168](https://hackerone.com/reports/476168) | ibb | Heap Overflow | CVE-2019-9023 | $1,500 | Heap | Heap overflow in utf32be_mbc_to_code |
| [MEM-476179](https://hackerone.com/reports/476179) | ibb | Heap Overflow | CVE-2015-8865 | $1,500 | Heap | Buffer over-write in finfo_open with malformed magic file. |
| [MEM-477073](https://hackerone.com/reports/477073) | ibb | Memory Corruption - Generic | CVE-2019-6250 | - | Heap | ZeroMQ libzmq remote code execution |
| [MEM-477344](https://hackerone.com/reports/477344) | ibb | Buffer Over-read | CVE-2018-20783 | - | OOB | Heap Buffer Overflow (READ: 4) in phar_parse_pharfile |
| [MEM-477896](https://hackerone.com/reports/477896) | ibb | Use After Free | CVE-2019-9020 | $1,500 | UAF | Use after free and out of bounds read in xmlrpc_decode() |
| [MEM-477897](https://hackerone.com/reports/477897) | ibb | Buffer Over-read | CVE-2019-9024 | $500 | OOB | buffer overread in base64 code of the xmlrpc module |
| [MEM-478367](https://hackerone.com/reports/478367) | ibb | Use After Free | CVE-2016-10166 | $1,500 | UAF | efree() on uninitialized Heap data in imagescale leads to use-after-free |
| [MEM-478368](https://hackerone.com/reports/478368) | ibb | Memory Corruption - Generic | CVE-2019-6977 | $1,500 | OOB | imagecolormatch Out Of Bounds Write on Heap |
| [MEM-480778](https://hackerone.com/reports/480778) | ibb | Buffer Over-read | CVE-2018-6798, CVE-2018-6797 | - | OOB | Heap-buffer-overflow in Perl__byte_dump_string (utf8.c) could lead to memory leak |
| [MEM-480883](https://hackerone.com/reports/480883) | notepad-plus-plus | Stack Overflow | — | - | Null | Stack overflow in XML Parsing |
| [MEM-480984](https://hackerone.com/reports/480984) | notepad-plus-plus | Stack Overflow | — | - | Null | Stack overflow affecting "ext" field on stylers.xml configuration file |
| [MEM-481335](https://hackerone.com/reports/481335) | notepad-plus-plus | Buffer Over-read | — | - | OOB | Security check failure or stack buffer overrun (crash) |
| [MEM-481532](https://hackerone.com/reports/481532) | putty_h1c | Use After Free | — | - | UAF | heap-use-after-free (READ of size 8) in main() |
| [MEM-482200](https://hackerone.com/reports/482200) | putty_h1c | Heap Overflow | — | - | Heap | puttygen: heap-buffer-overflow in mp_get_decimal() |
| [MEM-484398](https://hackerone.com/reports/484398) | vlc_h1c | Classic Buffer Overflow | CVE-2019-5439 | $1,126.91 | Heap | Buffer overflow in libavi_plugin memmove() call |
| [MEM-484930](https://hackerone.com/reports/484930) | putty_h1c | Memory Corruption - Generic | — | - | Adjacent | puttygen: 160MB memory leak while trying to extract openssh public key from crafted key file |
| [MEM-489102](https://hackerone.com/reports/489102) | vlc_h1c | Stack Overflow | — | $2,817.28 | Null | VLC 4.0.0 - Stack Buffer Overflow (SEH) |
| [MEM-495793](https://hackerone.com/reports/495793) | valve | Memory Corruption - Generic | — | - | Null | Malformed .MDL triggers an Access Violation on GoldSRC (hl.exe) |
| [MEM-497255](https://hackerone.com/reports/497255) | notepad-plus-plus | Stack Overflow | — | - | Null | A stack buffer overflow in BabyGrid.cpp can lead to program crashes via a malicious localization file |
| [MEM-503821](https://hackerone.com/reports/503821) | putty_h1c | Memory Corruption - Generic | — | - | Adjacent | Assertion `col >= 0 && col < line->cols' failed, process aborted while streaming ouput from remote server |
| [MEM-504761](https://hackerone.com/reports/504761) | ibb | Classic Buffer Overflow | CVE-2019-9675 | $1,500 | Heap | phar_tar_writeheaders_int() buffer overflow |
| [MEM-504951](https://hackerone.com/reports/504951) | valve | Stack Overflow | — | $1,000 | Null | Malformed playlist.txt in GoldSrc games leads to Access Violation & arbitrary code execution |
| [MEM-505173](https://hackerone.com/reports/505173) | valve | Stack Overflow | — | $350 | Null | Malformed map detailed texture files in GoldSrc games lead to Remote Code Execution |
| [MEM-510025](https://hackerone.com/reports/510025) | ibb | Buffer Over-read | CVE-2019-9640 | - | OOB | Invalid Read on exif_process_SOFn |
| [MEM-510336](https://hackerone.com/reports/510336) | ibb | Classic Buffer Overflow | CVE-2019-9641 | - | Heap | Uninitialized read in exif_process_IFD_in_TIFF |
| [MEM-510887](https://hackerone.com/reports/510887) | ibb | Heap Overflow | CVE-2018-18312 | - | Heap | [CVE-2018-18312] regcomp: heap-buffer-overflow write / reg_node overrun |
| [MEM-510888](https://hackerone.com/reports/510888) | ibb | Heap Overflow | CVE-2018-18313 | - | Heap | [CVE-2018-18313] regcomp: heap-buffer-overflow read in S_grok_bslash_N |
| [MEM-527042](https://hackerone.com/reports/527042) | ibb | Use After Free | CVE-2019-0196 | - | UAF | CVE-2019-0196: mod_http2 with scoreboard Use-After-Free (Read) |
| [MEM-535827](https://hackerone.com/reports/535827) | shopify-scripts | Classic Buffer Overflow | — | $1,000 | Heap | Buffer overflow in yywarning_s |
| [MEM-542180](https://hackerone.com/reports/542180) | valve | Classic Buffer Overflow | — | $10,000 | Heap | Malformed NAV file leads to buffer overflow and code execution in Left4Dead2.exe |
| [MEM-550696](https://hackerone.com/reports/550696) | curl | Heap Overflow | CVE-2019-5436 | $200 | Heap | CVE-2019-5436: Heap Buffer Overflow at lib/tftp.c |
| [MEM-593229](https://hackerone.com/reports/593229) | ibb | Buffer Over-read | CVE-2019-11039 | $1,500 | OOB | Out-of-bounds read in iconv.c:_php_iconv_mime_decode() due to integer overflow |
| [MEM-621308](https://hackerone.com/reports/621308) | shopify-scripts | NULL Pointer Dereference | — | $1,000 | Null | NULL pointer dereference in `mrb_check_frozen` |
| [MEM-630462](https://hackerone.com/reports/630462) | putty_h1c | Heap Overflow | — | $3,645.90 | Heap | Heap overflow happen when receiving short length key from ssh server using ssh protocol 1 |
| [MEM-633607](https://hackerone.com/reports/633607) | shopify-scripts | Out-of-bounds Read | — | $1,000 | OOB | Invalid read in `str_replace_partial` |
| [MEM-641240](https://hackerone.com/reports/641240) | ibb | Heap Overflow | CVE-2019-12527 | - | Heap | Basic Authentication Heap Overflow |
| [MEM-665330](https://hackerone.com/reports/665330) | ibb | Buffer Over-read | CVE-2019-11040 | $1,500 | OOB | Out of Bounds Memory Read in php_jpg_get16 |
| [MEM-672245](https://hackerone.com/reports/672245) | ibb | Use After Free | — | - | UAF | Use After Free in GC with Certain Destructors |
| [MEM-674540](https://hackerone.com/reports/674540) | ibb | Classic Buffer Overflow | CVE-2019-10097 | - | Heap | mod_remoteip stack buffer overflow and NULL pointer dereference |
| [MEM-675578](https://hackerone.com/reports/675578) | ibb | Out-of-bounds Read | CVE-2019-11041 | $1,500 | OOB | Out of Bounds Memory Read in exif_scan_thumbnail |
| [MEM-675580](https://hackerone.com/reports/675580) | ibb | Out-of-bounds Read | CVE-2019-11042 | $1,500 | OOB | Out of Bounds Memory Read in exif_process_user_comment |
| [MEM-677557](https://hackerone.com/reports/677557) | ibb | Use After Free | CVE-2019-10081 | - | UAF | mod_http2, memory corruption on early pushes (CVE-2019-10081) |
| [MEM-680415](https://hackerone.com/reports/680415) | ibb | Use After Free | CVE-2019-10082 | - | UAF | mod_http2, read-after-free in h2 connection shutdown (CVE-2019-10082) |
| [MEM-684603](https://hackerone.com/reports/684603) | curl | Heap Overflow | CVE-2019-5482, CVE-2019-5436 | - | Heap | CVE-2019-5482: Heap buffer overflow in TFTP when using small blksize |
| [MEM-692040](https://hackerone.com/reports/692040) | ibb | Use After Free | — | - | UAF | PHP 7.3.3: Heap-use-after-free (READ of size 8) in match_at() |
| [MEM-724243](https://hackerone.com/reports/724243) | ibb | Out-of-bounds Read | CVE-2018-16227 | - | OOB | Tcpdump before 4.9.3 has a buffer over-read in print-802_11.c (CVE-2018-16227) |
| [MEM-724253](https://hackerone.com/reports/724253) | ibb | Out-of-bounds Read | CVE-2018-16229 | - | OOB | Tcpdump before 4.9.3 has a buffer over-read in print-dccp.c:dccp_print_option() (CVE-2018-16229) |
| [MEM-746766](https://hackerone.com/reports/746766) | ibb | Buffer Over-read | CVE-2019-19274, CVE-2019-19275 | $2,000 | OOB | Two out-of-bounds array reads in Python AST builder (Re-opening 520612 with CVEs) |
| [MEM-778610](https://hackerone.com/reports/778610) | ibb | Classic Buffer Overflow | — | - | Heap | Squid as reverse proxy RCE and data leak |
| [MEM-778834](https://hackerone.com/reports/778834) | ibb | Buffer Over-read | CVE-2020-7059 | $500 | OOB | OOB read in php_strip_tags_ex |
| [MEM-781325](https://hackerone.com/reports/781325) | ibb | Out-of-bounds Read | — | - | OOB | Out-of-bounds Read in php_strip_tags_ex |
| [MEM-784186](https://hackerone.com/reports/784186) | nodejs | Memory Corruption - Generic | CVE-2020-8174 | $250 | Heap | napi_get_value_string_X allow various kinds of memory corruption |
| [MEM-789034](https://hackerone.com/reports/789034) | ibb | Classic Buffer Overflow | CVE-2020-8517 | - | Heap | Buffer Overflow in ext_lm_group_acl helper |
| [MEM-798301](https://hackerone.com/reports/798301) | filezilla | Classic Buffer Overflow | — | $250 | Heap | FileZilla 3.46.3 - 'Scale factor' Buffer Overflow |
| [MEM-798744](https://hackerone.com/reports/798744) | ibb | NULL Pointer Dereference | — | - | Null | Null Pointer Dereference in PHP Session Upload Progress |
| [MEM-800324](https://hackerone.com/reports/800324) | ibb | Classic Buffer Overflow | — | - | Heap | Several protocol parsers in before 4.9.2 could cause a buffer overflow in util-print.c:bittok2str_internal() |
| [MEM-802846](https://hackerone.com/reports/802846) | ibb | Buffer Over-read | CVE-2017-13033 | - | OOB | The VTP parser in tcpdump before 4.9.2 has a buffer over-read in print-vtp.c:vtp_print() |
| [MEM-802863](https://hackerone.com/reports/802863) | ibb | Buffer Over-read | CVE-2017-13050 | - | OOB | CVE-2017-13050: The RPKI-Router parser in tcpdump before 4.9.2 has a buffer over-read in print-rpki-rtr.c:rpki_rtr_pdu_print() |
| [MEM-802896](https://hackerone.com/reports/802896) | ibb | Buffer Over-read | CVE-2017-13019 | - | OOB | CVE-2017-13019:  The PGM parser in tcpdump before 4.9.2 has a buffer over-read in print-pgm.c:pgm_print() |
| [MEM-807772](https://hackerone.com/reports/807772) | valve | Out-of-bounds Read | — | $7,500 | OOB | OOB reads in network message handlers leads to RCE |
| [MEM-816637](https://hackerone.com/reports/816637) | ibb | Heap Overflow | CVE-2020-10938 | - | Heap | CVE-2020-10938-buffer overflow/out-of-bounds write in compress.c:HuffmanDecodeImage() |
| [MEM-824163](https://hackerone.com/reports/824163) | ibb | Buffer Over-read | CVE-2019-12528 | - | OOB | Squid leaks previous content from reusable buffer |
| [MEM-824771](https://hackerone.com/reports/824771) | ibb | Classic Buffer Overflow | CVE-2019-12526 | - | Heap | UrnState Heap Overflow |
| [MEM-826026](https://hackerone.com/reports/826026) | playstation | Use After Free | — | $10,000 | UAF | Use-After-Free In IPV6_2292PKTOPTIONS leading To Arbitrary Kernel R/W Primitives |
| [MEM-831353](https://hackerone.com/reports/831353) | ibb | Buffer Over-read | CVE-2017-16808 | $500 | OOB | tcpdump before 4.9.3 has a heap-based buffer over-read related to aoe_print in print-aoe.c and lookup_emem in addrtoname.c |
| [MEM-838127](https://hackerone.com/reports/838127) | ibb | Stack Overflow | CVE-2020-7065 | - | Null | mb_strtolower (UTF-32LE): stack-buffer-overflow at php_unicode_tolower_full (CVE-2020-7065) |
| [MEM-852103](https://hackerone.com/reports/852103) | ibb | Out-of-bounds Read | CVE-2020-7067 | - | OOB | Out-of-Bound Read in urldecode() [CVE-2020-7067] |
| [MEM-888986](https://hackerone.com/reports/888986) | ibb | Heap Overflow | CVE-2020-10543 | - | Heap | [CVE-2020-10543] Buffer overflow caused by a crafted regular expression |
| [MEM-891846](https://hackerone.com/reports/891846) | ibb | Buffer Over-read | CVE-2020-9383 | $750 | OOB | CVE-2020-9383 Floppy OOB read |
| [MEM-950299](https://hackerone.com/reports/950299) | ibb | Use After Free | CVE-2020-7068 | - | UAF | Use after free vulnerability  in phar_parse_zipfile |
| [MEM-964582](https://hackerone.com/reports/964582) | ibb | Buffer Over-read | CVE-2017-13040 | $500 | OOB | CVE-2017-13040 The MPTCP parser in tcpdump before 4.9.2 has a buffer over-read in print-mptcp.c, several functions. |
| [MEM-964583](https://hackerone.com/reports/964583) | ibb | Buffer Over-read | CVE-2017-13041 | $500 | OOB | CVE-2017-13041 The ICMPv6 parser in tcpdump before 4.9.2 has a buffer over-read in print-icmp6.c:icmp6_nodeinfo_print(). |
| [MEM-965914](https://hackerone.com/reports/965914) | nodejs | Classic Buffer Overflow | CVE-2020-8252 | - | Heap | `fs.realpath.native` on darwin may cause buffer overflow |
| [MEM-988103](https://hackerone.com/reports/988103) | nodejs | Use After Free | CVE-2020-8265 | - | UAF | Node.js: use-after-free in TLSWrap |
| [MEM-1032086](https://hackerone.com/reports/1032086) | kubernetes | NULL Pointer Dereference | CVE-2020-8569 | $500 | Null | csi-snapshot-controller crashes when processing VolumeSnapshot with non-existing PVC |
| [MEM-1047086](https://hackerone.com/reports/1047086) | ibb | Heap Overflow | CVE-2020-27829 | - | Heap | Heap buffer overflow vulnerability while processing a malformed TIFF file. |
| [MEM-1073363](https://hackerone.com/reports/1073363) | kubernetes | Buffer Over-read | — | - | OOB | Index Out Of Bounds in protobuf unmarshalling |
| [MEM-1084342](https://hackerone.com/reports/1084342) | ibb | Classic Buffer Overflow | CVE-2021-3177 | $1,500 | Heap | Buffer overflow in PyCArg_repr in _ctypes/callproc.c for Python 3.x to 3.9.1 |
| [MEM-1180252](https://hackerone.com/reports/1180252) | valve | Classic Buffer Overflow | — | $7,500 | Heap | Buffer overrun in Steam SILK voice decoder |
| [MEM-1180380](https://hackerone.com/reports/1180380) | curl | Use After Free | CVE-2021-22901 | $2,000 | UAF | CVE-2021-22901: TLS session caching disaster |
| [MEM-1209681](https://hackerone.com/reports/1209681) | nodejs | Buffer Over-read | CVE-2021-22918 | - | OOB | OOB read in libuv |
| [MEM-1217702](https://hackerone.com/reports/1217702) | h1-ctf | Out-of-bounds Read | — | - | Adjacent | Adam and the  Deadly  Injections |
| [MEM-1352429](https://hackerone.com/reports/1352429) | ibb | Classic Buffer Overflow | CVE-2021-3711 | $2,000 | Heap | CVE-2021-3711: SM2 decrypt  buffer overflow |
| [MEM-1434056](https://hackerone.com/reports/1434056) | ibb | Heap Overflow | CVE-2021-44790 | - | Heap | Buffer overflow in req_parsebody method in lua_request.c |
| [MEM-1455248](https://hackerone.com/reports/1455248) | ibb | Classic Buffer Overflow | CVE-2021-41816 | - | Heap | Buffer Overflow in optimized_escape_html method |
| [MEM-1511619](https://hackerone.com/reports/1511619) | ibb | Heap Overflow | CVE-2022-23943 | - | Heap | Read and write beyond bounds in mod_sed |
| [MEM-1595296](https://hackerone.com/reports/1595296) | ibb | Buffer Over-read | CVE-2022-28330 | - | OOB | Read beyond bounds in mod_isapi.c [zhbug_httpd_41] |
| [MEM-1753224](https://hackerone.com/reports/1753224) | ibb | Stack Overflow | CVE-2022-35260 | - | Null | CVE-2022-35260: .netrc parser out-of-bounds access |
| [MEM-1977252](https://hackerone.com/reports/1977252) | brave | Use After Free | — | $3,000 | UAF | UAF on JSEthereumProvider |
| [MEM-1997312](https://hackerone.com/reports/1997312) | ibb | Use After Free | CVE-2023-28319 | - | UAF | CVE-2023-28319: UAF in SSH sha256 fingerprint check |
| [MEM-2070810](https://hackerone.com/reports/2070810) | ibb | NULL Pointer Dereference | CVE-2023-3603 | - | Null | Potential NULL dereference in libssh's sftp server |
| [MEM-2526041](https://hackerone.com/reports/2526041) | ibb | NULL Pointer Dereference | CVE-2024-35200 | $2,600 | Null | CVE-2024-35200 in nginx |
| [MEM-2526051](https://hackerone.com/reports/2526051) | ibb | Stack Overflow | CVE-2024-31079 | $2,600 | Null | CVE-2024-31079 in nginx |
| [MEM-2585375](https://hackerone.com/reports/2585375) | ibb | NULL Pointer Dereference | CVE-2024-38477 | $4,920 | Null | important: Apache HTTP Server: Crash resulting in Denial of Service in mod_proxy via a malicious request (CVE-2024-38477) |
| [MEM-2621057](https://hackerone.com/reports/2621057) | ibb | Memory Corruption - Generic | CVE-2024-6197 | - | Heap | libcurl: freeing stack buffer during x509 certificate parsing |
| [MEM-2621062](https://hackerone.com/reports/2621062) | ibb | Buffer Over-read | CVE-2024-6874 | - | OOB | curl: stack-buffer overread during punycode conversions |
| [MEM-2658447](https://hackerone.com/reports/2658447) | ibb | Buffer Over-read | CVE-2024-7347 | $2,142 | OOB | CVE-2024-7347: Buffer overread in the ngx_http_mp4_module |
| [MEM-2779070](https://hackerone.com/reports/2779070) | hyperledger | Use After Free | — | - | Adjacent | Memory Leak in bytes_to_hexstring Function |
| [MEM-2958097](https://hackerone.com/reports/2958097) | brave | NULL Pointer Dereference | — | $100 | Null | Null Pointer Dereference by Crafted Response from AI Model |
| [MEM-2974850](https://hackerone.com/reports/2974850) | ibb | Heap Overflow | CVE-2025-0725 | - | Heap | CVE-2025-0725: Heap overflow in curl with Content-Encoding gzip and old libz versions |
## Appendix — unclassified merges (16 rows)

These 16 ids came from the classifier's `unclassified` pool (468 rows), merged into this vault's last module (`Adjacent-and-Unclassified`) at build time. They are **not** members of the 336-row bucket table above; `classes.json` carries them disjointly (352 ids total, each exactly once). Ten are GitHub Security Lab CodeQL-query reports (bodies: *"This bug was reported directly to GitHub Security Lab."*— titles carry CWE numbers, not research).

| Case | Team | Weakness | CVE | Bounty | Module | Title |
|---|---|---|---|---|---|---|
| [MEM-140865](https://hackerone.com/reports/140865) | ibb | — | — | - | Adjacent | Integer Overflow in php_html_entities() |
| [MEM-159686](https://hackerone.com/reports/159686) | ibb | — | — | - | Adjacent | integer overflow in the _csv module's join_append_data function |
| [MEM-159687](https://hackerone.com/reports/159687) | ibb | — | — | - | Adjacent | integer overflow in binascii.b2a_qp |
| [MEM-159696](https://hackerone.com/reports/159696) | ibb | — | — | - | Adjacent | Two vulnerabilities in the ssl module |
| [MEM-163087](https://hackerone.com/reports/163087) | ibb | — | — | - | Adjacent | use of uninitialized variables in operator.methodcaller |
| [MEM-216700](https://hackerone.com/reports/216700) | shopify-scripts | — | — | - | Adjacent | heap use-after-free in mrb_vm_exec() |
| [MEM-974370](https://hackerone.com/reports/974370) | github-security-lab | — | — | $1,800 | Adjacent | [CATENACYBER]: [CPP] CWE-476 Null Pointer Dereference : Another query to either missing or redundant NULL check |
| [MEM-1065401](https://hackerone.com/reports/1065401) | github-security-lab | — | — | $1,800 | Adjacent | CPP: CWE-191 into experimental this reveals a dangerous comparison |
| [MEM-1093242](https://hackerone.com/reports/1093242) | github-security-lab | — | — | $1,800 | Adjacent | ihsinme: CPP Add query for CWE-401 memory leak on unsuccessful call to realloc function |
| [MEM-1114027](https://hackerone.com/reports/1114027) | github-security-lab | — | — | $1,800 | Adjacent | ihsinme: CPP add query for CWE-788 Access of memory location after the end of a buffer using strncat. |
| [MEM-1122664](https://hackerone.com/reports/1122664) | github-security-lab | — | — | $1,000 | Adjacent | ihsinme: CPP add query for CWE-788 Access of memory location after the end of a buffer using strlen. |
| [MEM-1219491](https://hackerone.com/reports/1219491) | github-security-lab | — | — | $1,800 | Adjacent | ihsinme:CPP Add query for CWE-415 Double Free |
| [MEM-1378946](https://hackerone.com/reports/1378946) | github-security-lab | — | — | $4,500 | Adjacent | [cpp] CWE-787: query to detect unsigned integer to signed integer conversions used in pointer arithmetics |
| [MEM-1564100](https://hackerone.com/reports/1564100) | github-security-lab | — | — | $500 | Adjacent | [CPP]: Add query for CWE-190: Integer Overflow or Wraparound when using transform after operation |
| [MEM-1738939](https://hackerone.com/reports/1738939) | github-security-lab | — | — | $1,000 | Adjacent | [CPP]: Add query for CWE-125 Out-of-bounds Read with different interpretation of the string when use mbtowc |
| [MEM-1950659](https://hackerone.com/reports/1950659) | github-security-lab | — | — | $1,000 | Adjacent | CPP: Add query for CWE-369: Divide By Zero. |