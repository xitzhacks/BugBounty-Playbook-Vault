---
title: "DOS case register — 240-row ledger (221 bucket rows + 19 unclassified merges)"
type: register
built: "2026-11-07"
roster: "h1-brain disclosed_reports.db (3,673 rows; sha256 8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4) · bucket 'dos' = 221 rows (weakness 'Uncontrolled Resource Consumption') + 19 _adjacent_unclassified merges (weakness None)"
case_id_scheme: "DOS-<HackerOne report id>"
bounty_rule: "DB bounty_amount where present (labeled $) · None = no figure in DB (not evidence of non-payment)"
module_rule: "frozen in archive/classes.json (module_map_all.json dos assignment; bodies-win)"
---

# Case register — Denial of Service / Resource Exhaustion

Corpus: 240 rows (221 bucket + 19 merges) · 117 with bounty figures · **$275,868** · max $10,000 (9 rows: 8 mruby + DOS-185775 merge) · evidence: 238 full-body / 2 metadata-only (DOS-801230, DOS-1061211).

Class census: 01_Native-Crash 75 (42797, 112723, 113424, 123119, 146936, 146944, 180695, 180977, 181232, 181642, 181677, 181685, 181695, 181828, 181871, 181874, 181910, 182027, 182274, 182484, 183231, 183356, 183405, 183425, 184712, 185041, 185387, 185899, 187305, 187536, 188313, 188326, 190133, 190863, 191328, 191689, 191938, 192485, 192532, 192734, 193075, 193077, 193081, 193724, 195580, 195842, 196386, 197693, 197694, 197719, 197723, 197916, 199764, 200387, 201905, 202362, 202582, 202584, 203513, 204047, 204628, 205884, 208526, 209449, 210429, 212107, 212456, 213261, 213779, 215854, 218570, 297383, 305972, 495508, 588562) · 02_ReDoS 20 (511381, 661722, 1000567, 1023899, 1283484, 1404789, 1518036, 1531958, 1929567, 1944515, 2012131, 2012135, 2064723, 2068004, 2402193, 2446427, 2792776, 2807139, 2872502, 3023605) · 03_HTTP-Flood 10 (384839, 799072, 800140, 868834, 1043360, 2334401, 2375446, 2453322, 2453328, 2586226) · 04_Webapp-Abuse 100 (57356, 94642, 125587, 128856, 163307, 176066, 176197, 181558, 181686, 201346, 210779, 216840, 221787, 221791, 221792, 288993, 303632, 324021, 357665, 363636, 364964, 406614, 418254, 470067, 500686, 504759, 505278, 506412, 507525, 549040, 557154, 583819, 670572, 679907, 702987, 713407, 752073, 764434, 767458, 768677, 774896, 777984, 784676, 812754, 819088, 833856, 858603, 861170, 861521, 867699, 882923, 903521, 903740, 905015, 921286, 970760, 975827, 1005421, 1018037, 1033107, 1041173, 1077136, 1147449, 1176794, 1237428, 1243724, 1253732, 1341957, 1514863, 1543584, 1543718, 1596252, 1606039, 1620170, 1635854, 1680241, 1685979, 1688199, 1695472, 1746098, 1904097, 1954937, 2012121, 2012122, 2012125, 2058337, 2105808, 2258758, 2412583, 2446433, 2446437, 2489843, 2559404, 2591681, 2644244, 2818147, 2987782, 3002543, 3013913, 3058919) · 05_Adjacent 16 (1096609, 409370, 1173684, 153093, 159820, 326639, 350847, 380873, 591302, 649533, 864701, 921704, 1066851, 1160407, 1173153, 1181946) · 05_Adjacent(Merge) 19 (185775, 204774, 216615, 431561, 496113, 752010, 753491, 783356, 801230, 880187, 993582, 1061211, 1627159, 1804128, 2071556, 2071561, 2520679, 2584376, 2939104).

Bounty arithmetic: bucket $238,864/106 (01 $149,500/38 + 02 $12,395/10 + 03 $20,250/8 + 04 $51,219/47 + 05-adjacent $5,500/3) + merges $37,004/11 = **$275,868/117**. Max single row $10,000 (9 rows). Module totals: 01 $149,500/38 · 02 $12,395/10 · 03 $20,250/8 · 04 $51,219/47 · 05 $42,504/14 (adjacent $5,500/3 + merges $37,004/11).

## Bucket rows (221)

| Case | Program | Asset | Asset type | CVE | Bounty | Module | Evidence | Note |
|---|---|---|---|---|---|---|---|---|
| [DOS-42797](https://hackerone.com/reports/42797) | rails | - | - | - | - | 01_Native-Crash | full | deeply nested params hash → SystemStackError in Action Pack |
| [DOS-57356](https://hackerone.com/reports/57356) | x | - | - | - | - | 04_Webapp-Abuse | full | DOM cookie bomb |
| [DOS-94642](https://hackerone.com/reports/94642) | whisper | - | - | - | $30 | 04_Webapp-Abuse | full | SMS invite form abuse |
| [DOS-112723](https://hackerone.com/reports/112723) | ibb | PHP | OTHER | - | - | 01_Native-Crash | full | PHP-FPM access-log snprintf length accounting → leak/overflow |
| [DOS-113424](https://hackerone.com/reports/113424) | torproject | - | - | - | - | 01_Native-Crash | full | tor pre-auth control loop spins → infinite CPU |
| [DOS-123119](https://hackerone.com/reports/123119) | ibb | PHP | OTHER | - | - | 01_Native-Crash | full | assign-by-ref to overloaded objects → UAF crash |
| [DOS-125587](https://hackerone.com/reports/125587) | security | hackerone.com | URL | - | - | 04_Webapp-Abuse | full | hogging all resources on hackerone.com |
| [DOS-128856](https://hackerone.com/reports/128856) | gratipay | - | - | - | $10 | 04_Webapp-Abuse | full | async email send abuse |
| [DOS-146936](https://hackerone.com/reports/146936) | ibb | PHP | OTHER | CVE-2015-8874 | $500 | 01_Native-Crash | full | imagefilltoborder stack overflow (CVE-2015-8874) |
| [DOS-146944](https://hackerone.com/reports/146944) | ibb | PHP | OTHER | - | $500 | 01_Native-Crash | full | NULL deref at _gdScaleVert (libgd) |
| [DOS-153093](https://hackerone.com/reports/153093) | wordpress | - | - | - | - | 05_Adjacent | full | WordPress DoS via CSRF (advisory-only body) |
| [DOS-159820](https://hackerone.com/reports/159820) | instacart | - | - | - | - | 05_Adjacent | full | list-image upload issues |
| [DOS-163307](https://hackerone.com/reports/163307) | instacart | - | - | - | $100 | 04_Webapp-Abuse | full | WordPress auth DoS |
| [DOS-176066](https://hackerone.com/reports/176066) | brave | - | - | - | - | 04_Webapp-Abuse | full | Brave browser DoS |
| [DOS-176197](https://hackerone.com/reports/176197) | brave | - | - | - | - | 04_Webapp-Abuse | full | Brave window-object DoS |
| [DOS-180695](https://hackerone.com/reports/180695) | shopify-scripts | - | - | - | $8,000 | 01_Native-Crash | full | 49,000× 'A' crashes mruby.science service |
| [DOS-180977](https://hackerone.com/reports/180977) | shopify-scripts | - | - | - | - | 01_Native-Crash | full | malformed exception → SIGABRT |
| [DOS-181232](https://hackerone.com/reports/181232) | shopify-scripts | - | - | - | $8,000 | 01_Native-Crash | full | splat+redo case → NULL deref crash |
| [DOS-181558](https://hackerone.com/reports/181558) | brave | - | - | - | $25 | 04_Webapp-Abuse | full | Brave code-snippet DoS |
| [DOS-181642](https://hackerone.com/reports/181642) | ibb | IBB (Legacy) | OTHER | CVE-2016-9273 | - | 01_Native-Crash | full | libtiff heap overflow / OOB read (CVE-2016-9273) |
| [DOS-181677](https://hackerone.com/reports/181677) | shopify-scripts | - | - | - | - | 01_Native-Crash | full | NULL deref parsing ternary operators |
| [DOS-181685](https://hackerone.com/reports/181685) | shopify-scripts | - | - | - | $10,000 | 01_Native-Crash | full | remove Range#initialize_copy → uninitialized object → NULL deref |
| [DOS-181686](https://hackerone.com/reports/181686) | brave | - | - | - | $25 | 04_Webapp-Abuse | full | Brave hangs loading snippet |
| [DOS-181695](https://hackerone.com/reports/181695) | shopify-scripts | - | - | - | $8,000 | 01_Native-Crash | full | undefined method_missing → NULL deref |
| [DOS-181828](https://hackerone.com/reports/181828) | shopify-scripts | - | - | - | $10,000 | 01_Native-Crash | full | non-closure lambda env → NULL deref, kills parent MRI |
| [DOS-181871](https://hackerone.com/reports/181871) | shopify-scripts | - | - | - | - | 01_Native-Crash | full | type confusion in mrb_no_method_error |
| [DOS-181874](https://hackerone.com/reports/181874) | shopify-scripts | - | - | - | - | 01_Native-Crash | full | invalid remove_method arg → SIGSEGV |
| [DOS-181910](https://hackerone.com/reports/181910) | shopify-scripts | - | - | - | $10,000 | 01_Native-Crash | full | Range=Array → RRange edges confused → type-confusion crash |
| [DOS-182027](https://hackerone.com/reports/182027) | shopify-scripts | - | - | - | - | 01_Native-Crash | full | SIGSEGV on mrb_ary_splice |
| [DOS-182274](https://hackerone.com/reports/182274) | shopify-scripts | - | - | - | - | 01_Native-Crash | full | TOCTOU in mrb_time_initialize → NULL deref |
| [DOS-182484](https://hackerone.com/reports/182484) | shopify-scripts | - | - | - | $10,000 | 01_Native-Crash | full | CALL_MAXARGS=127 boundary → invalid pointer deref |
| [DOS-183231](https://hackerone.com/reports/183231) | shopify-scripts | - | - | - | - | 01_Native-Crash | full | mrb_str_modify invalid memory access |
| [DOS-183356](https://hackerone.com/reports/183356) | shopify-scripts | - | - | - | $10,000 | 01_Native-Crash | full | A-or-equals break-while-break → bytecode corruption |
| [DOS-183405](https://hackerone.com/reports/183405) | shopify-scripts | - | - | - | $8,000 | 01_Native-Crash | full | Null target_class crash |
| [DOS-183425](https://hackerone.com/reports/183425) | shopify-scripts | - | - | - | $8,000 | 01_Native-Crash | full | C-invoked Ruby method via Object#send → segfault |
| [DOS-184712](https://hackerone.com/reports/184712) | shopify-scripts | - | - | - | $8,000 | 01_Native-Crash | full | invalid memory access in mrb_ary_concat |
| [DOS-185041](https://hackerone.com/reports/185041) | shopify-scripts | - | - | - | - | 01_Native-Crash | full | type confusion in mrb_exc_set → memory corruption |
| [DOS-185387](https://hackerone.com/reports/185387) | shopify-scripts | - | - | - | $1,000 | 01_Native-Crash | full | parse.y regression → NULL deref (fuzz-found) |
| [DOS-185899](https://hackerone.com/reports/185899) | shopify-scripts | - | - | - | $1,000 | 01_Native-Crash | full | array_copy upper-bound error → invalid memory write |
| [DOS-187305](https://hackerone.com/reports/187305) | shopify-scripts | - | - | - | $10,000 | 01_Native-Crash | full | zero-length heredoc id → parser infinite loop, SIGTERM-proof |
| [DOS-187536](https://hackerone.com/reports/187536) | shopify-scripts | - | - | - | $10,000 | 01_Native-Crash | full | codegen NODE_NEGATE unused value → NULL deref |
| [DOS-188313](https://hackerone.com/reports/188313) | shopify-scripts | - | - | - | $8,000 | 01_Native-Crash | full | bad memory access in kh_get_mt (hash table) |
| [DOS-188326](https://hackerone.com/reports/188326) | shopify-scripts | - | - | - | $10,000 | 01_Native-Crash | full | mrb_time_asctime buffer overflow (intermittent, ASAN-reliable) |
| [DOS-190133](https://hackerone.com/reports/190133) | shopify-scripts | - | - | - | $1,000 | 01_Native-Crash | full | invalid values to values_at → segfault |
| [DOS-190863](https://hackerone.com/reports/190863) | ibb | PHP | OTHER | - | $500 | 01_Native-Crash | full | imagefilltoborder stack overflow, truecolor |
| [DOS-191328](https://hackerone.com/reports/191328) | shopify-scripts | - | - | - | $100 | 01_Native-Crash | full | invalid memory access in mrb_str_format |
| [DOS-191689](https://hackerone.com/reports/191689) | shopify-scripts | - | - | - | $1,000 | 01_Native-Crash | full | NODE_NEGATE codegen error |
| [DOS-191938](https://hackerone.com/reports/191938) | shopify-scripts | - | - | - | - | 01_Native-Crash | full | SIGSEGV on mrb_get_args |
| [DOS-192485](https://hackerone.com/reports/192485) | shopify-scripts | - | - | - | - | 01_Native-Crash | full | SIGSEGV on mrb_vm_exec (NULL deref) |
| [DOS-192532](https://hackerone.com/reports/192532) | shopify-scripts | - | - | - | - | 01_Native-Crash | full | SIGABRT/SIGSEGV in mspace_free/mrb_default_allocf |
| [DOS-192734](https://hackerone.com/reports/192734) | shopify-scripts | - | - | - | - | 01_Native-Crash | full | SIGSEGV NULL pointer mrb_str_concat |
| [DOS-193075](https://hackerone.com/reports/193075) | shopify-scripts | - | - | - | - | 01_Native-Crash | full | SIGSEGV mrb_check_intern_str NULL pointer |
| [DOS-193077](https://hackerone.com/reports/193077) | shopify-scripts | - | - | - | - | 01_Native-Crash | full | mrb_str_modify writes to read-only memory |
| [DOS-193081](https://hackerone.com/reports/193081) | shopify-scripts | - | - | - | $800 | 01_Native-Crash | full | NULL pointer deref in mrb_str_prepend |
| [DOS-193724](https://hackerone.com/reports/193724) | shopify-scripts | - | - | - | - | 01_Native-Crash | full | SIGSEGV kh_resize_iv NULL deref |
| [DOS-195580](https://hackerone.com/reports/195580) | ibb | PHP | OTHER | - | - | 01_Native-Crash | full | hostile TIFF parse → crash |
| [DOS-195842](https://hackerone.com/reports/195842) | shopify-scripts | - | - | - | - | 01_Native-Crash | full | segfault in mrb_gc_mark |
| [DOS-196386](https://hackerone.com/reports/196386) | shopify-scripts | - | - | - | - | 01_Native-Crash | full | SIGSEGV mrb_vm_exec vm.c:1272 |
| [DOS-197693](https://hackerone.com/reports/197693) | shopify-scripts | - | - | - | - | 01_Native-Crash | full | SIGSEGV mrb_vm_exec line:1681 |
| [DOS-197694](https://hackerone.com/reports/197694) | shopify-scripts | - | - | - | - | 01_Native-Crash | full | SIGSEGV mrb_obj_extend line:413 |
| [DOS-197719](https://hackerone.com/reports/197719) | shopify-scripts | - | - | - | $800 | 01_Native-Crash | full | heap overflow in mrb_ary_splice |
| [DOS-197723](https://hackerone.com/reports/197723) | shopify-scripts | - | - | - | - | 01_Native-Crash | full | NULL deref in mrb_str_modify |
| [DOS-197916](https://hackerone.com/reports/197916) | shopify-scripts | - | - | - | $100 | 01_Native-Crash | full | crash in print_backtrace |
| [DOS-199764](https://hackerone.com/reports/199764) | shopify-scripts | - | - | - | - | 01_Native-Crash | full | abort in proc.c:143 |
| [DOS-200387](https://hackerone.com/reports/200387) | shopify-scripts | - | - | - | $100 | 01_Native-Crash | full | redo inside NODE_RESCUE codegen crash |
| [DOS-201346](https://hackerone.com/reports/201346) | ibb | OpenSSL (Legacy) | OTHER | CVE-2017-3730 | - | 04_Webapp-Abuse | full | bad (EC)DHE params crash client (CVE-2017-3730) |
| [DOS-201905](https://hackerone.com/reports/201905) | shopify-scripts | - | - | - | - | 01_Native-Crash | full | SIGSEGV vm.c:1214 |
| [DOS-202362](https://hackerone.com/reports/202362) | shopify-scripts | - | - | - | $100 | 01_Native-Crash | full | NULL deref in mrb_random_initialize |
| [DOS-202582](https://hackerone.com/reports/202582) | shopify-scripts | - | - | - | - | 01_Native-Crash | full | NULL deref in mrb_obj_instance_eval |
| [DOS-202584](https://hackerone.com/reports/202584) | shopify-scripts | - | - | - | - | 01_Native-Crash | full | NULL deref in mrb_vm_exec |
| [DOS-203513](https://hackerone.com/reports/203513) | shopify-scripts | - | - | - | - | 01_Native-Crash | full | SIGSEGV mrb_vm_exec line:1312 |
| [DOS-204047](https://hackerone.com/reports/204047) | shopify-scripts | - | - | - | $1,000 | 01_Native-Crash | full | segfault printing backtrace |
| [DOS-204628](https://hackerone.com/reports/204628) | shopify-scripts | - | - | - | - | 01_Native-Crash | full | segfault in sprintf/mrb_str_format |
| [DOS-205884](https://hackerone.com/reports/205884) | shopify-scripts | - | - | - | $100 | 01_Native-Crash | full | integer overflow in str_substr → OOB read/write |
| [DOS-208526](https://hackerone.com/reports/208526) | shopify-scripts | - | - | - | $800 | 01_Native-Crash | full | NULL deref in mark_context_stack |
| [DOS-209449](https://hackerone.com/reports/209449) | shopify-scripts | - | - | - | $800 | 01_Native-Crash | full | heap buffer overflow, long array assignment |
| [DOS-210429](https://hackerone.com/reports/210429) | shopify-scripts | - | - | - | - | 01_Native-Crash | full | NULL ptr deref mrb_vm_exec |
| [DOS-210779](https://hackerone.com/reports/210779) | x | - | - | - | - | 04_Webapp-Abuse | full | invalidating OAuth token breaks TweetDeck |
| [DOS-212107](https://hackerone.com/reports/212107) | shopify-scripts | - | - | - | $800 | 01_Native-Crash | full | NULL deref in mrb_class |
| [DOS-212456](https://hackerone.com/reports/212456) | shopify-scripts | - | - | - | - | 01_Native-Crash | full | SIGSEGV kh_get_n2s in symbol.c:37 |
| [DOS-213261](https://hackerone.com/reports/213261) | shopify-scripts | - | - | - | $800 | 01_Native-Crash | full | UAF → invalid pointer deref |
| [DOS-213779](https://hackerone.com/reports/213779) | shopify-scripts | - | - | - | - | 01_Native-Crash | full | SIGSEGV mrb_obj_value |
| [DOS-215854](https://hackerone.com/reports/215854) | shopify-scripts | - | - | - | $300 | 01_Native-Crash | full | garbage collector crash |
| [DOS-216840](https://hackerone.com/reports/216840) | ibb | OpenSSL (Legacy) | OTHER | CVE-2016-6304 | - | 04_Webapp-Abuse | full | OCSP extension unbounded memory (CVE-2016-6304) |
| [DOS-218570](https://hackerone.com/reports/218570) | shopify-scripts | - | - | - | $800 | 01_Native-Crash | full | invalid pointer deref in OP_ENTER |
| [DOS-221787](https://hackerone.com/reports/221787) | ibb | OpenSSL (Legacy) | OTHER | CVE-2016-6302 | - | 04_Webapp-Abuse | full | malformed SHA512 ticket DoS (CVE-2016-6302) |
| [DOS-221791](https://hackerone.com/reports/221791) | ibb | OpenSSL (Legacy) | OTHER | CVE-2016-6307 | - | 04_Webapp-Abuse | full | tls_get_message_header over-allocation (CVE-2016-6307) |
| [DOS-221792](https://hackerone.com/reports/221792) | ibb | OpenSSL (Legacy) | OTHER | CVE-2016-6308, CVE-2016-6307 | - | 04_Webapp-Abuse | full | dtls fragment over-allocation (CVE-2016-6308) |
| [DOS-288993](https://hackerone.com/reports/288993) | ibb | OpenSSL (Legacy) | OTHER | CVE-2016-6305 | $1,000 | 04_Webapp-Abuse | full | SSL_peek hang on empty record (CVE-2016-6305) |
| [DOS-297383](https://hackerone.com/reports/297383) | shopify-scripts | - | - | - | - | 01_Native-Crash | full | mruby heredoc notation crash |
| [DOS-303632](https://hackerone.com/reports/303632) | nodejs-ecosystem | fastify | SOURCE_CODE | CVE-2018-3711 | - | 04_Webapp-Abuse | full | Fastify large-JSON DoS |
| [DOS-305972](https://hackerone.com/reports/305972) | ibb | PHP | OTHER | CVE-2018-5711 | $500 | 01_Native-Crash | full | infinite loop in gdImageCreateFromGifCtx |
| [DOS-324021](https://hackerone.com/reports/324021) | rootstocklabs | bounty-node.rsk.co | URL | - | - | 04_Webapp-Abuse | full | debug JSON-RPC methods expose DoS |
| [DOS-326639](https://hackerone.com/reports/326639) | greenhouse | boards.greenhouse.io | URL | - | - | 05_Adjacent | full | for[] array reflected into cached JS settings |
| [DOS-350847](https://hackerone.com/reports/350847) | greenhouse | boards.greenhouse.io | URL | - | - | 05_Adjacent | full | 1024-char request-URI limit bypassed via UTF-8 expansion |
| [DOS-357665](https://hackerone.com/reports/357665) | brave | https://github.com/brave/browser-ios | SOURCE_CODE | - | - | 04_Webapp-Abuse | full | Brave iOS DoS |
| [DOS-363636](https://hackerone.com/reports/363636) | rootstocklabs | https://github.com/rsksmart/rskj | SOURCE_CODE | - | $4,000 | 04_Webapp-Abuse | full | PeerExplorer ping/pong connection leak |
| [DOS-364964](https://hackerone.com/reports/364964) | ibb | OpenSSL (Legacy) | OTHER | CVE-2018-0732 | - | 04_Webapp-Abuse | full | large DH param client DoS (CVE-2018-0732) |
| [DOS-380873](https://hackerone.com/reports/380873) | nodejs-ecosystem | lodash | SOURCE_CODE | CVE-2018-16487 | - | 05_Adjacent | full | lodash merge constructor.prototype pollution |
| [DOS-384839](https://hackerone.com/reports/384839) | ibb | Apache (Legacy) | OTHER | CVE-2018-1333 | - | 03_HTTP-Flood | full | crafted HTTP/2 requests exhaust connections (CVE-2018-1333) |
| [DOS-406614](https://hackerone.com/reports/406614) | ui | EdgeMAX | HARDWARE | - | - | 04_Webapp-Abuse | full | Edgemax resource-consumption DoS |
| [DOS-409370](https://hackerone.com/reports/409370) | security | www.hackerone.com | URL | - | $2,500 | 05_Adjacent | full | X-Forwarded-Host/Port poison → persistent redirect block |
| [DOS-418254](https://hackerone.com/reports/418254) | chaturbate | chaturbate.com | URL | - | $200 | 04_Webapp-Abuse | full | unrestricted POST size on roomlogin |
| [DOS-470067](https://hackerone.com/reports/470067) | gitlab | gitlab.com | URL | - | $3,000 | 04_Webapp-Abuse | full | Mermaid diagram freezes Issue page |
| [DOS-495508](https://hackerone.com/reports/495508) | putty_h1c | https://www.chiark.greenend.org.uk/~sgtatham/putty/ | SOURCE_CODE | - | - | 01_Native-Crash | full | assert len==1 aborts on remote-output streaming |
| [DOS-500686](https://hackerone.com/reports/500686) | x | *.twitter.com | WILDCARD | - | $1,120 | 04_Webapp-Abuse | full | unloadable twitter-mobile URL |
| [DOS-504759](https://hackerone.com/reports/504759) | nextcloud | nextcloud/3rdparty | SOURCE_CODE | - | - | 04_Webapp-Abuse | full | large avatar images burn CPU |
| [DOS-505278](https://hackerone.com/reports/505278) | ibb | PHP | OTHER | CVE-2018-10546 | - | 04_Webapp-Abuse | full | stream-filter DoS |
| [DOS-506412](https://hackerone.com/reports/506412) | hyperledger | https://github.com/hyperledger/fabric-sdk-node | SOURCE_CODE | - | $500 | 04_Webapp-Abuse | full | empty CA response crashes node |
| [DOS-507525](https://hackerone.com/reports/507525) | chaturbate | *.highwebmedia.com | WILDCARD | - | $400 | 04_Webapp-Abuse | full | camo.stream DoS |
| [DOS-511381](https://hackerone.com/reports/511381) | gitlab | gitlab.com | URL | - | $1,000 | 02_ReDoS | full | color-code validator regex → CPU 90%+ |
| [DOS-549040](https://hackerone.com/reports/549040) | gitlab | gitlab.com | URL | - | - | 04_Webapp-Abuse | full | GitLab math-render client exhaustion |
| [DOS-557154](https://hackerone.com/reports/557154) | gitlab | gitlab.com | URL | CVE-2019-15593 | $1,000 | 04_Webapp-Abuse | full | unlimited comment length → server+client DoS |
| [DOS-583819](https://hackerone.com/reports/583819) | x | *.periscope.tv | WILDCARD | - | $560 | 04_Webapp-Abuse | full | cookie injection DoS on periscope.tv |
| [DOS-588562](https://hackerone.com/reports/588562) | nextcloud | Desktop Client | DOWNLOADABLE_EXECUTABLES | CVE-2020-8229 | $100 | 01_Native-Crash | full | OCUtil.dll memory leak → DoS in desktop client |
| [DOS-591302](https://hackerone.com/reports/591302) | automattic | - | - | - | - | 05_Adjacent | full | Origin echoed into cached Access-Control-Allow-Origin |
| [DOS-649533](https://hackerone.com/reports/649533) | moneybird | moneybird.com | URL | - | - | 05_Adjacent | full | 2FA enable without email verify (adjacent noise) |
| [DOS-661722](https://hackerone.com/reports/661722) | ruby | https://github.com/ruby/ruby | SOURCE_CODE | - | - | 02_ReDoS | full | DigestAuth split_param_value catastrophic backtracking |
| [DOS-670572](https://hackerone.com/reports/670572) | gitlab | gitlab.com | URL | CVE-2019-15584, CVE-2019-9220 | - | 04_Webapp-Abuse | full | Mermaid 5000-char limit bypass via 100 blocks |
| [DOS-679907](https://hackerone.com/reports/679907) | roblox | Roblox Client | DOWNLOADABLE_EXECUTABLES | - | - | 04_Webapp-Abuse | full | FireServer malformed string freezes servers |
| [DOS-702987](https://hackerone.com/reports/702987) | gitlab | *.gitter.im | WILDCARD | - | - | 04_Webapp-Abuse | full | missing redirect_uri crashes OAuth authorize |
| [DOS-713407](https://hackerone.com/reports/713407) | security | hackerone.com | URL | - | - | 04_Webapp-Abuse | full | whitespace filename exception DoS |
| [DOS-752073](https://hackerone.com/reports/752073) | nordsecurity | *.nordvpn.com | WILDCARD | - | - | 04_Webapp-Abuse | full | xmlrpc.php bruteforce/DoS surface |
| [DOS-764434](https://hackerone.com/reports/764434) | security | hackerone.com | URL | - | - | 04_Webapp-Abuse | full | huge profile-pic name DoS |
| [DOS-767458](https://hackerone.com/reports/767458) | x | *.twitter.com | WILDCARD | - | $560 | 04_Webapp-Abuse | full | missing input validation → DoS |
| [DOS-768677](https://hackerone.com/reports/768677) | x | *.twitter.com | WILDCARD | - | $560 | 04_Webapp-Abuse | full | missing input validation → DoS |
| [DOS-774896](https://hackerone.com/reports/774896) | kubernetes | https://github.com/kubernetes/kubernetes | SOURCE_CODE | CVE-2020-8551 | - | 04_Webapp-Abuse | full | kubelet metric-cardinality exhaustion |
| [DOS-777984](https://hackerone.com/reports/777984) | nordsecurity | *.nordvpn.com | WILDCARD | - | - | 04_Webapp-Abuse | full | cookie-bomb DoS |
| [DOS-784676](https://hackerone.com/reports/784676) | x | com.atebits.Tweetie2 | APPLE_STORE_APP_ID | - | $560 | 04_Webapp-Abuse | full | crafted DM reactions crash iOS app |
| [DOS-799072](https://hackerone.com/reports/799072) | nodejs | https://github.com/nodejs/node | SOURCE_CODE | - | $250 | 03_HTTP-Flood | full | body 1 byte/sec slowloris keeps connection |
| [DOS-800140](https://hackerone.com/reports/800140) | nodejs | https://github.com/nodejs/node | SOURCE_CODE | - | $250 | 03_HTTP-Flood | full | malformed HTTP/2 SETTINGS → SIGABRT |
| [DOS-812754](https://hackerone.com/reports/812754) | nextcloud | nextcloud/server | SOURCE_CODE | CVE-2020-8295 | - | 04_Webapp-Abuse | full | password-reset request DoS |
| [DOS-819088](https://hackerone.com/reports/819088) | x | *.twitter.com | WILDCARD | - | - | 04_Webapp-Abuse | full | char-limit bypass → Twitter-app 500s |
| [DOS-833856](https://hackerone.com/reports/833856) | kubernetes | https://github.com/kubernetes/test-infra | SOURCE_CODE | - | - | 04_Webapp-Abuse | full | GCSArtifact.RealAll DoS |
| [DOS-858603](https://hackerone.com/reports/858603) | acronis | Acronis Cyber Protect Home Office (formerly Acronis True Image) | DOWNLOADABLE_EXECUTABLES | - | - | 04_Webapp-Abuse | full | log-file DoS in anti-ransomware service |
| [DOS-861170](https://hackerone.com/reports/861170) | security | https://ctf.hacker101.com | URL | - | - | 04_Webapp-Abuse | full | crafted request from old account DoS |
| [DOS-861521](https://hackerone.com/reports/861521) | clario | *.mackeeper.com | WILDCARD | - | $50 | 04_Webapp-Abuse | full | cookie injection → domain-wide DoS |
| [DOS-864701](https://hackerone.com/reports/864701) | nodejs-ecosystem | lodash | SOURCE_CODE | - | - | 05_Adjacent | full | lodash 4.17.15 prototype pollution |
| [DOS-867699](https://hackerone.com/reports/867699) | kubernetes | https://github.com/kubernetes/kubernetes | SOURCE_CODE | CVE-2020-8557 | $1,000 | 04_Webapp-Abuse | full | writing /etc/hosts fills node disk |
| [DOS-868834](https://hackerone.com/reports/868834) | nodejs | https://github.com/nodejs/node | SOURCE_CODE | CVE-2020-8251 | $250 | 03_HTTP-Flood | full | unfinished HTTP/1.1 requests exhaust accept queue |
| [DOS-882923](https://hackerone.com/reports/882923) | kubernetes | https://github.com/kubernetes/client-go | SOURCE_CODE | - | - | 04_Webapp-Abuse | full | client-go jsonpath DoS |
| [DOS-903521](https://hackerone.com/reports/903521) | nodejs-ecosystem | fastify | SOURCE_CODE | CVE-2020-8192 | $250 | 04_Webapp-Abuse | full | Fastify allErrors:true ajv DoS (default config) |
| [DOS-903740](https://hackerone.com/reports/903740) | x | *.twitter.com | WILDCARD | - | $1,120 | 04_Webapp-Abuse | full | twitter.com + mobile DoS |
| [DOS-905015](https://hackerone.com/reports/905015) | ibb | PHP | OTHER | CVE-2019-11048 | - | 04_Webapp-Abuse | full | long filenames OOM, temp files leak |
| [DOS-921286](https://hackerone.com/reports/921286) | x | *.twitter.com | WILDCARD | - | $560 | 04_Webapp-Abuse | full | Chrome DoS |
| [DOS-921704](https://hackerone.com/reports/921704) | automattic | - | - | - | - | 05_Adjacent | full | cached CORS Allow-Origin poison (duplicate family of 591302) |
| [DOS-970760](https://hackerone.com/reports/970760) | cs_money | support.cs.money | URL | - | $200 | 04_Webapp-Abuse | full | pixel-flood app-level DoS |
| [DOS-975827](https://hackerone.com/reports/975827) | automattic | *.tumblr.com | WILDCARD | - | - | 04_Webapp-Abuse | full | one-click permanent DoS |
| [DOS-1000567](https://hackerone.com/reports/1000567) | cs_money | wiki.cs.money | URL | - | $250 | 02_ReDoS | full | GraphQL search regex bomb (possible cmd injection) |
| [DOS-1005421](https://hackerone.com/reports/1005421) | automattic | api.tumblr.com | URL | - | - | 04_Webapp-Abuse | full | tumblr API cookie-manipulation DoS |
| [DOS-1018037](https://hackerone.com/reports/1018037) | basecamp | *.hey.com | WILDCARD | - | $1,000 | 04_Webapp-Abuse | full | very long hey.com name locks contacts |
| [DOS-1023899](https://hackerone.com/reports/1023899) | rails | https://github.com/rails/rails | SOURCE_CODE | CVE-2021-22880 | - | 02_ReDoS | full | ActiveRecord PostgreSQL Money ReDoS |
| [DOS-1033107](https://hackerone.com/reports/1033107) | nodejs | https://github.com/nodejs/node | SOURCE_CODE | CVE-2020-8277 | $250 | 04_Webapp-Abuse | full | DNS max-responses DoS |
| [DOS-1041173](https://hackerone.com/reports/1041173) | automattic | - | - | - | - | 04_Webapp-Abuse | full | invite permanently DoSs happy.tools |
| [DOS-1043360](https://hackerone.com/reports/1043360) | nodejs | https://github.com/nodejs/node | SOURCE_CODE | CVE-2021-22883 | - | 03_HTTP-Flood | full | unknownProtocol HTTP/2 resource exhaustion |
| [DOS-1066851](https://hackerone.com/reports/1066851) | h1-ctf | *.hackyholidays.h1ctf.com | WILDCARD | - | - | 05_Adjacent | full | CTF write-up miscategorized as DoS |
| [DOS-1077136](https://hackerone.com/reports/1077136) | slack | app.slack.com | URL | - | $1,500 | 04_Webapp-Abuse | full | html injection overrides document functions → crash |
| [DOS-1096609](https://hackerone.com/reports/1096609) | shopify | *.shopify.com | WILDCARD | - | $2,900 | 05_Adjacent | full | Host: :1337 poison → persistent cached DoS |
| [DOS-1147449](https://hackerone.com/reports/1147449) | sifchain | - | - | - | $50 | 04_Webapp-Abuse | full | xmlrpc.php/wp-json user-enum + DoS |
| [DOS-1160407](https://hackerone.com/reports/1160407) | gitlab | gitlab.com | URL | - | - | 05_Adjacent | full | x-http-method-override poisons Varnish-cached assets |
| [DOS-1173153](https://hackerone.com/reports/1173153) | exodus | *.exodus.com | WILDCARD | - | - | 05_Adjacent | full | Authorization header poisons Cloudflare-cached downloads |
| [DOS-1173684](https://hackerone.com/reports/1173684) | nextcloud | nextcloud/server | SOURCE_CODE | CVE-2021-32703 | $100 | 05_Adjacent | full | shareinfo endpoint unprotected (weak adjacency) |
| [DOS-1176794](https://hackerone.com/reports/1176794) | fetlife | fetlife.com | URL | - | $100 | 04_Webapp-Abuse | full | payload makes posts unavailable |
| [DOS-1181946](https://hackerone.com/reports/1181946) | security | hackerone.com | URL | - | - | 05_Adjacent | full | x-forwarded-scheme poisons Cloudflare cached JS |
| [DOS-1237428](https://hackerone.com/reports/1237428) | reddit | 918820076 | APPLE_STORE_APP_ID | - | - | 04_Webapp-Abuse | full | long shoutout string → 500s |
| [DOS-1243724](https://hackerone.com/reports/1243724) | mattermost | mattermost/mattermost-server | SOURCE_CODE | - | $150 | 04_Webapp-Abuse | full | large console messages DoS |
| [DOS-1253732](https://hackerone.com/reports/1253732) | mattermost | mattermost/mattermost-webapp | SOURCE_CODE | CVE-2021-37863 | $150 | 04_Webapp-Abuse | full | crafted message crashes viewers' webapp |
| [DOS-1283484](https://hackerone.com/reports/1283484) | gitlab | Your Own GitLab Instance | OTHER | - | $600 | 02_ReDoS | full | Rouge lexer cubic backtracking → 100% CPU |
| [DOS-1341957](https://hackerone.com/reports/1341957) | reddit | www.reddit.com | URL | - | - | 04_Webapp-Abuse | full | hash-collision DoS in Markdown parser |
| [DOS-1404789](https://hackerone.com/reports/1404789) | ibb | https://github.com/ruby | SOURCE_CODE | CVE-2021-41817 | - | 02_ReDoS | full | Ruby Date parsing ReDoS |
| [DOS-1514863](https://hackerone.com/reports/1514863) | ibb | https://github.com/apache/httpd | SOURCE_CODE | CVE-2022-22719 | - | 04_Webapp-Abuse | full | uninitialized value in lua req_parsebody |
| [DOS-1518036](https://hackerone.com/reports/1518036) | ibb | https://github.com/rust-lang/rust | SOURCE_CODE | CVE-2022-24713 | $4,000 | 02_ReDoS | full | (?:){4294967295} empty-repetition → infinite CPU |
| [DOS-1531958](https://hackerone.com/reports/1531958) | gitlab | Your Own GitLab Instance | OTHER | - | - | 02_ReDoS | full | webhook long header → Sidekiq 100% CPU for a year |
| [DOS-1543584](https://hackerone.com/reports/1543584) | gitlab | https://gitlab.com/gitlab-org/gitlab | SOURCE_CODE | - | $2,300 | 04_Webapp-Abuse | full | move_issue with crafted description burns 60s CPU |
| [DOS-1543718](https://hackerone.com/reports/1543718) | gitlab | https://gitlab.com/gitlab-org/gitlab | SOURCE_CODE | - | $7,640 | 04_Webapp-Abuse | full | issue-preview '![l' repeat burns 60s CPU |
| [DOS-1596252](https://hackerone.com/reports/1596252) | ibb | https://github.com/apache/httpd | SOURCE_CODE | CVE-2022-29404 | - | 04_Webapp-Abuse | full | lua_read_body DoS |
| [DOS-1606039](https://hackerone.com/reports/1606039) | ibb | https://github.com/curl/curl | SOURCE_CODE | CVE-2022-27781 | - | 04_Webapp-Abuse | full | CERTINFO never-ending busy-loop |
| [DOS-1620170](https://hackerone.com/reports/1620170) | mattermost | mattermost/mattermost-server | SOURCE_CODE | CVE-2022-3257 | $150 | 04_Webapp-Abuse | full | GIF upload OOM via API |
| [DOS-1635854](https://hackerone.com/reports/1635854) | hyperledger | https://github.com/hyperledger/fabric | SOURCE_CODE | CVE-2022-36023 | - | 04_Webapp-Abuse | full | Hyperledger Fabric remote DoS |
| [DOS-1680241](https://hackerone.com/reports/1680241) | mattermost | Mattermost Source Code | SOURCE_CODE | CVE-2022-4044 | - | 04_Webapp-Abuse | full | automatic-response-message DoS |
| [DOS-1685979](https://hackerone.com/reports/1685979) | mattermost | Mattermost Plugins | SOURCE_CODE | CVE-2022-4019 | - | 04_Webapp-Abuse | full | Playbook DoS |
| [DOS-1688199](https://hackerone.com/reports/1688199) | nextcloud | nextcloud/circles | SOURCE_CODE | CVE-2022-39330 | $250 | 04_Webapp-Abuse | full | sharee-recommendations DB exhaustion |
| [DOS-1695472](https://hackerone.com/reports/1695472) | hyperledger | https://github.com/hyperledger/indy-node | SOURCE_CODE | CVE-2022-31006 | $1,500 | 04_Webapp-Abuse | full | 500 parallel read requests block validators |
| [DOS-1746098](https://hackerone.com/reports/1746098) | ibb | https://github.com/django | SOURCE_CODE | CVE-2022-41323 | $2,400 | 04_Webapp-Abuse | full | locale param treated as regex → DoS |
| [DOS-1904097](https://hackerone.com/reports/1904097) | ibb | https://github.com/django | SOURCE_CODE | CVE-2023-24580 | $2,400 | 04_Webapp-Abuse | full | unlimited multipart parts → FD/memory exhaustion |
| [DOS-1929567](https://hackerone.com/reports/1929567) | ibb | https://github.com/ruby | SOURCE_CODE | CVE-2023-28756 | $4,000 | 02_ReDoS | full | Time.rfc2822 via Rack ConditionalGet → ReDoS |
| [DOS-1944515](https://hackerone.com/reports/1944515) | ibb | https://github.com/ruby | SOURCE_CODE | CVE-2023-28755 | - | 02_ReDoS | full | URI ReDoS (CVE-2023-28755) |
| [DOS-1954937](https://hackerone.com/reports/1954937) | ibb | https://github.com/rack/rack | SOURCE_CODE | - | $480 | 04_Webapp-Abuse | full | Multipart MIME parsing DoS (rack) |
| [DOS-2012121](https://hackerone.com/reports/2012121) | ibb | https://github.com/rack/rack | SOURCE_CODE | CVE-2022-44570 | $480 | 04_Webapp-Abuse | full | Range header parsing DoS (CVE-2022-44570) |
| [DOS-2012122](https://hackerone.com/reports/2012122) | ibb | https://github.com/rack/rack | SOURCE_CODE | CVE-2022-44571 | $480 | 04_Webapp-Abuse | full | Content-Disposition parsing DoS (CVE-2022-44571) |
| [DOS-2012125](https://hackerone.com/reports/2012125) | ibb | https://github.com/rack/rack | SOURCE_CODE | CVE-2022-44572 | $480 | 04_Webapp-Abuse | full | RFC2183 boundary parsing DoS (CVE-2022-44572) |
| [DOS-2012131](https://hackerone.com/reports/2012131) | ibb | https://github.com/rails | SOURCE_CODE | CVE-2023-22796 | $480 | 02_ReDoS | full | ActiveSupport underscore ReDoS (CVE-2023-22796) |
| [DOS-2012135](https://hackerone.com/reports/2012135) | ibb | https://github.com/rails | SOURCE_CODE | CVE-2023-22799 | $480 | 02_ReDoS | full | GlobalID ReDoS (CVE-2023-22799) |
| [DOS-2058337](https://hackerone.com/reports/2058337) | nextcloud | nextcloud/server | SOURCE_CODE | CVE-2023-45150 | - | 04_Webapp-Abuse | full | long calendar-invite emails hang server |
| [DOS-2064723](https://hackerone.com/reports/2064723) | ibb | https://github.com/apache/airflow | SOURCE_CODE | - | $540 | 02_ReDoS | full | unsanitized regex input hangs Airflow request |
| [DOS-2068004](https://hackerone.com/reports/2068004) | ibb | https://github.com/apache/airflow | SOURCE_CODE | - | $540 | 02_ReDoS | full | ReDoS before 2.6.3 (Airflow) |
| [DOS-2105808](https://hackerone.com/reports/2105808) | rootstocklabs | https://github.com/rsksmart/rskj | SOURCE_CODE | - | $5,000 | 04_Webapp-Abuse | full | single UDP packet wedges RSKJ forever |
| [DOS-2258758](https://hackerone.com/reports/2258758) | ibb | https://github.com/django | SOURCE_CODE | CVE-2023-46695 | $2,540 | 04_Webapp-Abuse | full | 1M unicode chars in UsernameField → 4.4s/request |
| [DOS-2334401](https://hackerone.com/reports/2334401) | ibb | https://github.com/apache/tomcat | SOURCE_CODE | CVE-2024-24549 | $4,860 | 03_HTTP-Flood | full | CONTINUATION flood → HPACK OOM, GOAWAY-avoiding |
| [DOS-2375446](https://hackerone.com/reports/2375446) | ibb | https://github.com/nodejs/node | SOURCE_CODE | CVE-2024-22019 | $3,495 | 03_HTTP-Flood | full | unbounded chunk extension, timeouts don't help (CVE-2024-22019) |
| [DOS-2402193](https://hackerone.com/reports/2402193) | ibb | https://github.com/django | SOURCE_CODE | CVE-2024-27351 | - | 02_ReDoS | full | Django Truncator.words ReDoS (CVE-2024-27351) |
| [DOS-2412583](https://hackerone.com/reports/2412583) | rootstocklabs | https://github.com/rsksmart/rskj | SOURCE_CODE | - | - | 04_Webapp-Abuse | full | modexp precompile bug: 8-min smart contract |
| [DOS-2446427](https://hackerone.com/reports/2446427) | ibb | https://github.com/rails | SOURCE_CODE | CVE-2024-26142 | - | 02_ReDoS | full | Accept header parsing ReDoS (CVE-2024-26142) |
| [DOS-2446433](https://hackerone.com/reports/2446433) | ibb | https://github.com/rack/rack | SOURCE_CODE | CVE-2024-26146 | - | 04_Webapp-Abuse | full | header parsing DoS (CVE-2024-26146) |
| [DOS-2446437](https://hackerone.com/reports/2446437) | ibb | https://github.com/rack/rack | SOURCE_CODE | CVE-2024-25126 | - | 04_Webapp-Abuse | full | Content-Type parsing DoS (CVE-2024-25126) |
| [DOS-2453322](https://hackerone.com/reports/2453322) | ibb | https://github.com/apache/httpd | SOURCE_CODE | CVE-2024-27316 | $2,580 | 03_HTTP-Flood | full | endless CONTINUATION buffered pre-413 → OOM (CVE-2024-27316) |
| [DOS-2453328](https://hackerone.com/reports/2453328) | ibb | https://github.com/nodejs/node | SOURCE_CODE | CVE-2024-27983 | $3,645 | 03_HTTP-Flood | full | CONTINUATION + RST race → Http2Session assert crash |
| [DOS-2489843](https://hackerone.com/reports/2489843) | rootstocklabs | https://github.com/rsksmart/rskj | SOURCE_CODE | - | - | 04_Webapp-Abuse | full | inefficient CODESIZE: 1.5-min contract |
| [DOS-2559404](https://hackerone.com/reports/2559404) | rootstocklabs | https://github.com/rsksmart/rskj | SOURCE_CODE | - | - | 04_Webapp-Abuse | full | huge error string: ~23s contract |
| [DOS-2586226](https://hackerone.com/reports/2586226) | ibb | https://github.com/apache/tomcat | SOURCE_CODE | CVE-2024-34750 | $4,920 | 03_HTTP-Flood | full | HTTP/2 stream miscount → infinite-timeout leak (CVE-2024-34750) |
| [DOS-2591681](https://hackerone.com/reports/2591681) | ibb | https://github.com/django | SOURCE_CODE | CVE-2024-38875 | $2,142 | 04_Webapp-Abuse | full | strip_punctuation brace bomb (CVE-2024-38875) |
| [DOS-2644244](https://hackerone.com/reports/2644244) | ibb | https://github.com/django | SOURCE_CODE | CVE-2024-41989 | $2,142 | 04_Webapp-Abuse | full | floatformat 'e' exponent blowup (CVE-2024-41989) |
| [DOS-2792776](https://hackerone.com/reports/2792776) | ibb | https://github.com/rails | SOURCE_CODE | CVE-2024-47888 | $505 | 02_ReDoS | full | Action Text blockquote ReDoS (CVE-2024-47888) |
| [DOS-2807139](https://hackerone.com/reports/2807139) | ibb | https://github.com/ruby | SOURCE_CODE | CVE-2024-49761 | - | 02_ReDoS | full | REXML ReDoS (CVE-2024-49761) |
| [DOS-2818147](https://hackerone.com/reports/2818147) | sorare | api.sorare.com | URL | - | $300 | 04_Webapp-Abuse | full | insufficient input verification → resource use |
| [DOS-2872502](https://hackerone.com/reports/2872502) | ibb | https://github.com/rails | SOURCE_CODE | CVE-2024-41128 | - | 02_ReDoS | full | query param filter ReDoS in Action Dispatch |
| [DOS-2987782](https://hackerone.com/reports/2987782) | ibb | https://github.com/ruby | SOURCE_CODE | - | - | 04_Webapp-Abuse | full | net/imap memory-exhaustion DoS |
| [DOS-3002543](https://hackerone.com/reports/3002543) | ibb | https://github.com/ruby | SOURCE_CODE | CVE-2024-43398 | $505 | 04_Webapp-Abuse | full | REXML DoS (CVE-2024-43398) |
| [DOS-3013913](https://hackerone.com/reports/3013913) | ibb | https://github.com/ruby | SOURCE_CODE | CVE-2025-27219 | - | 04_Webapp-Abuse | full | CGI::Cookie.parse DoS (CVE-2025-27219) |
| [DOS-3023605](https://hackerone.com/reports/3023605) | ibb | https://github.com/ruby | SOURCE_CODE | CVE-2025-27220 | - | 02_ReDoS | full | CGI::Util#escapeElement ReDoS (CVE-2025-27220) |
| [DOS-3058919](https://hackerone.com/reports/3058919) | discourse | try.discourse.org | URL | - | - | 04_Webapp-Abuse | full | large Markdown reply payload exhausts resources |

## Unclassified-merge rows (19)

These rows carry `weakness_name None` in the DB (hence outside the 221-row bucket) and were promoted into dos by `module_map_all.json` (`_adjacent_unclassified`). They are part of the vault corpus and of `classes.json`; the bucket-only subtotal above excludes them.

| Case | Program | Asset | Asset type | CVE | Bounty | Module | Evidence | Note |
|---|---|---|---|---|---|---|---|---|
| [DOS-185775](https://hackerone.com/reports/185775) | shopify-scripts | - | - | - | $10,000 | 05_Adjacent(Merge) | full | Decimal.new(self) → empty mpd_t assertion crash |
| [DOS-204774](https://hackerone.com/reports/204774) | shopify-scripts | - | - | - | - | 05_Adjacent(Merge) | full | proc{return} in ensure → sandbox segfault |
| [DOS-216615](https://hackerone.com/reports/216615) | shopify-scripts | - | - | - | - | 05_Adjacent(Merge) | full | N *case ... ary_concat segfault |
| [DOS-431561](https://hackerone.com/reports/431561) | rails | https://github.com/rails/rails | SOURCE_CODE | CVE-2018-16470 | - | 05_Adjacent(Merge) | full | Rack multipart worse-than-linear: 10k parts → 15–25s |
| [DOS-496113](https://hackerone.com/reports/496113) | notepad-plus-plus | - | - | - | - | 05_Adjacent(Merge) | full | Notepad++ header A*500 crash |
| [DOS-752010](https://hackerone.com/reports/752010) | nordsecurity | *.nordvpn.com | WILDCARD | CVE-2018-6389 | - | 05_Adjacent(Merge) | full | load-scripts.php ~3MB unauth amplification (CVE-2018-6389) |
| [DOS-753491](https://hackerone.com/reports/753491) | yelp | - | - | CVE-2018-6389 | - | 05_Adjacent(Merge) | full | blog.yelp.com load-scripts.php (CVE-2018-6389) |
| [DOS-783356](https://hackerone.com/reports/783356) | localizejs | localizestaging.com | URL | - | - | 05_Adjacent(Merge) | full | unbounded password length → DoS |
| [DOS-801230](https://hackerone.com/reports/801230) | github-security-lab | - | - | - | $1,000 | 05_Adjacent(Merge) | metadata | GHSL CodeQL ReDoS query (metadata-only body) |
| [DOS-880187](https://hackerone.com/reports/880187) | security | hackerone.com | URL | - | $2,500 | 05_Adjacent(Merge) | full | group-rename near-infinite loop burns CPU/mem |
| [DOS-993582](https://hackerone.com/reports/993582) | cs_money | 3d.cs.money | URL | - | - | 05_Adjacent(Merge) | full | single search-bar request DoS on 3d.cs.money |
| [DOS-1061211](https://hackerone.com/reports/1061211) | github-security-lab | - | - | - | $1,800 | 05_Adjacent(Merge) | metadata | GHSL Android NFE query (metadata-only body) |
| [DOS-1627159](https://hackerone.com/reports/1627159) | ibb | https://github.com/rack/rack | SOURCE_CODE | CVE-2022-30122 | $2,400 | 05_Adjacent(Merge) | full | Rack BROKEN_QUOTED multipart ReDoS (CVE-2022-30122) |
| [DOS-1804128](https://hackerone.com/reports/1804128) | ibb | https://github.com/rails | SOURCE_CODE | CVE-2022-23514 | $4,000 | 05_Adjacent(Merge) | full | PermitScrubber SVG-attribute backtracking (CVE-2022-23514) |
| [DOS-2071556](https://hackerone.com/reports/2071556) | ibb | https://github.com/rack/rack | SOURCE_CODE | CVE-2023-27539 | $2,540 | 05_Adjacent(Merge) | full | Rack header parsing slow-path (CVE-2023-27539) |
| [DOS-2071561](https://hackerone.com/reports/2071561) | ibb | https://github.com/ruby | SOURCE_CODE | CVE-2023-36617 | $2,540 | 05_Adjacent(Merge) | full | Ruby URI ReDoS after incomplete CVE-2023-28755 fix |
| [DOS-2520679](https://hackerone.com/reports/2520679) | ibb | https://github.com/rack/rack | SOURCE_CODE | CVE-2024-26141 | $5,420 | 05_Adjacent(Merge) | full | Range header → giant response (CVE-2024-26141) |
| [DOS-2584376](https://hackerone.com/reports/2584376) | ibb | https://github.com/rack/rack | SOURCE_CODE | CVE-2024-39316 | $2,642 | 05_Adjacent(Merge) | full | Accept-Encoding/Language ReDoS, unauthenticated |
| [DOS-2939104](https://hackerone.com/reports/2939104) | ibb | https://github.com/django | SOURCE_CODE | CVE-2024-42005, CVE-2024-56374 | $2,162 | 05_Adjacent(Merge) | full | IPv6 validation unbounded length (CVE-2024-42005/56374) |
