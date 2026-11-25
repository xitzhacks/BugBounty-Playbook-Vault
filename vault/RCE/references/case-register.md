---
title: "RCE case register — 150-row ledger (134 fetched bodies + 16 dead-404 records)"
type: register
built: "2026-11-05"
roster: "h1.security.nathan.sx mirror (4,419 rows, frozen 2017-09-12), title-filter (8 arms → 118 rows) + documented supplemental pass (32 rows: devops/console 4 · PHP archive/pickle 8 · mruby crash batch 17 · Perl crash 1 · dead non-arm 2)"
case_id_scheme: "RCE-<HackerOne report id>"
bounty_rule: "JSON bounty_amount where present (labeled json) · otherwise mirror list figure (labeled list) · 404 rows recorded, never quoted, bounty mirrored as 404-list"
grand_total: "$270,868 roster-tagged across 107 rows ($73,187 json/32 + $157,947 list/63 + $39,734 dead-list/12) · pure class (01–07) $231,044/93 · adjacent+noise 08 $90/2 · DoD corpus 09 $0"
---

# Case register — RCE

Substate mix (134 fetched): 125 resolved · 3 informative · 3 duplicate · 3 not-applicable.
Class census: 01 command injection 17 · 02 template injection & app primitives 6 · 03 unsafe deserialization 28 · 04 memory corruption → code execution 37 · 05 desktop-client load path 3 · 06 devops-console exposure 4 · 07 chains from other classes 14 · 08 adjacent+noise 10 · 09 DoD metadata corpus 15 · dead 16.

Bounty arithmetic: JSON $73,187/32 + list $157,947/63 + dead-list $39,734/12 = **$270,868 / 107 rows**.
Class modules 01–07 carry **$231,044 (93 rows)**: 01 $51,862/14 · 02 $14,400/6 · 03 $28,075/25 · 04 $106,100/36 · 05 $850/2 · 06 $20,300/3 · 07 $9,457/7.
Module 08 (adjacent+noise) carries $90/2; module 09 (DoD Corp VDP corpus) carries $0/0 — fifteen resolved RCE rows with no bounty tier.

| Case | Team | Substate | Bounty | Class | Note |
|---|---|---|---|---|---|
| [RCE-1376](https://hackerone.com/reports/1376) | Yahoo! | 404 | - | dead | 404 — roster-only record; body gone; mirror title: HTML Code Injection |
| [RCE-2106](https://hackerone.com/reports/2106) | ibb | resolved | $10,000 (list) | 04 | Flash Player type confusion → code execution (CVE up, APSB13-28); $10,000 list; Adobe-direct |
| [RCE-2127](https://hackerone.com/reports/2127) | Yahoo! | 404 | $1,276 (404-list) | dead | 404 — roster-only record; body gone; mirror title: HK.Yahoo.Net Remote Command Execution |
| [RCE-2170](https://hackerone.com/reports/2170) | ibb | resolved | $10,000 (list) | 04 | Flash double free → code execution CVE-2014-0502 (watering-hole active); $10,000 list; Adobe-direct |
| [RCE-4836](https://hackerone.com/reports/4836) | Yahoo! | 404 | $800 (404-list) | dead | 404 — roster-only record; body gone; mirror title: From Unrestricted File Upload to Remote Command Execution |
| [RCE-5499](https://hackerone.com/reports/5499) | msdos | resolved | - | 08 | Arbitrary command execution in MS-DOS — the famous joke report, resolved; Command Injection tag |
| [RCE-6674](https://hackerone.com/reports/6674) | Yahoo! | 404 | $3,000 (404-list) | dead | 404 — roster-only record; body gone; mirror title: REMOTE CODE EXECUTION/LOCAL FILE INCLUSION/XSPA/SSRF, view-source:http://sb*.geo.sp1.yahoo.com/, 4/6/14, #SpringClean |
| [RCE-26700](https://hackerone.com/reports/26700) | Square | 404 | $2,000 (404-list) | dead | 404 — roster-only record; body gone; mirror title: CRITICAL Account takeover via AngularJS template injection in connect.squareup.com |
| [RCE-28445](https://hackerone.com/reports/28445) | ibb | resolved | $2,500 (list) | 03 | SPL ArrayObject unserialization type confusion (PHP security team); $0 |
| [RCE-29480](https://hackerone.com/reports/29480) | irccloud | resolved | $300 (json) | 01 | IRC channel name → server-side /usr/bin/ command injection; $300 json; protocol-argument lane (weakness tag CSRF is a mislabel) |
| [RCE-29839](https://hackerone.com/reports/29839) | ibb | resolved | $20,000 (list) | 01 | The Shellshock disclosure row itself (GNU Bash VDP on H1); $20,000 list; env-var function-definition injection |
| [RCE-31756](https://hackerone.com/reports/31756) | ibb | resolved | $3,000 (list) | 07 | Drupal CVE-2014-3704 pre-auth SQLi → sessions → RCE; $3,000 list; SQLi-origin |
| [RCE-34917](https://hackerone.com/reports/34917) | blockio | informative | - | 08 | client-side tickbox bypass + command-injection-looking claim; informative |
| [RCE-44513](https://hackerone.com/reports/44513) | rails | resolved | $500 (list) | 02 | Rails Web Console whitelist bypass via X-Forwarded-For parser differential → interactive code session; $0; dev-console lane anchor |
| [RCE-46019](https://hackerone.com/reports/46019) | rails | resolved | $500 (json) | 02 | Dynamic render path dir-traversal → RCE; metadata-only (body empty); $500 json; sev high |
| [RCE-47232](https://hackerone.com/reports/47232) | ibb | resolved | $10,000 (list) | 04 | Flash StageVideoAvailabilityEvent UAF → arbitrary code execution; $10,000 list; Chrome-scope |
| [RCE-47234](https://hackerone.com/reports/47234) | ibb | resolved | $7,500 (list) | 04 | Flash MessageChannel.send UAF → arbitrary code execution; $7,500 list |
| [RCE-49408](https://hackerone.com/reports/49408) | Mail.Ru | 404 | $300 (404-list) | dead | 404 — roster-only record; body gone; mirror title: RCE через JDWP |
| [RCE-55029](https://hackerone.com/reports/55029) | ibb | resolved | $2,500 (list) | 03 | DateTimeZone unserialize UAF (Taoguang Chen); $0; extensive write-up |
| [RCE-55030](https://hackerone.com/reports/55030) | ibb | resolved | $2,500 (list) | 03 | SoapClient.__call type confusion via unserialize → info leak/RCE; $0 |
| [RCE-55033](https://hackerone.com/reports/55033) | ibb | resolved | $3,000 (list) | 03 | unserialize() UAF (two bugs.php.net); $3,000 list |
| [RCE-55431](https://hackerone.com/reports/55431) | drchrono | resolved | $700 (list) | 07 | XXE claim → RCE (Code Injection tag); $0; XXE-origin |
| [RCE-59663](https://hackerone.com/reports/59663) | concretecms | resolved | - | 01 | concrete5 sender email → sendmail argument injection (RCE claim); $0; sendmail lane |
| [RCE-66929](https://hackerone.com/reports/66929) | Marktplaats | 404 | - | dead | 404 — roster-only record; body gone; mirror title: Multiple Apache  2.2.22 Vulnerabilities (XSS/ Code Exec/ DoS) |
| [RCE-67161](https://hackerone.com/reports/67161) | Mail.Ru | 404 | $200 (404-list) | dead | 404 — roster-only record; body gone; mirror title: Possible xWork classLoader RCE: shared.mail.ru |
| [RCE-73235](https://hackerone.com/reports/73235) | ibb | resolved | $1,500 (list) | 03 | unserialize UAF via fake __wakeup zval — full Taoguang Chen write; $0 |
| [RCE-73237](https://hackerone.com/reports/73237) | ibb | resolved | $1,000 (json) | 04 | phar_set_inode stack buffer overflow; $1,000 json |
| [RCE-73238](https://hackerone.com/reports/73238) | ibb | resolved | $1,000 (json) | 04 | phar over-read inside unserialize; $1,000 json |
| [RCE-73244](https://hackerone.com/reports/73244) | ibb | resolved | $1,500 (list) | 03 | DateInterval unserialize UAF; $0 |
| [RCE-73257](https://hackerone.com/reports/73257) | ibb | resolved | $500 (json) | 03 | yaml_parse !php/object unsafe deserialization; $500 json; YAML lane |
| [RCE-73259](https://hackerone.com/reports/73259) | ibb | resolved | $500 (json) | 03 | _pickle.c integer overflow (Python upstream); $500 json; pickle lane root |
| [RCE-73567](https://hackerone.com/reports/73567) | shopify | resolved | $3,000 (list) | 01 | Shopify wpt.ec2 blind RCE via $(sleep 20) timing proof — canonical blind-CONFIRMED case; $3,000 list |
| [RCE-84374](https://hackerone.com/reports/84374) | owncloud | resolved | - | 07 | ownCloud apps upload php5 executed; $0; upload-origin (row-10 lane) |
| [RCE-98259](https://hackerone.com/reports/98259) | shopify | resolved | $1,500 (json) | 02 | Shopify Liquid template "Limited RCE" — no-args execution boundary documented; $1,500 json |
| [RCE-98559](https://hackerone.com/reports/98559) | owncloud | resolved | - | 03 | ci.owncloud Jenkins Java deserialization (JBoss CLI port) → RCE; $0; Java lane + exposed-instance overlap |
| [RCE-103990](https://hackerone.com/reports/103990) | ibb | resolved | $500 (json) | 04 | phar_get_fp_offset NULL deref; $500 json |
| [RCE-103992](https://hackerone.com/reports/103992) | ibb | resolved | $500 (list) | 03 | _Unpickler_Read int overflow; $0; pickle lane |
| [RCE-103995](https://hackerone.com/reports/103995) | ibb | resolved | $1,000 (list) | 03 | SplDoublyLinkedList UAF; $0 |
| [RCE-103996](https://hackerone.com/reports/103996) | ibb | resolved | $1,000 (list) | 03 | SplObjectStorage UAF; $0 |
| [RCE-103997](https://hackerone.com/reports/103997) | ibb | resolved | $1,000 (list) | 03 | unserialize UAF (bugs.php.net 71187); $0 |
| [RCE-103998](https://hackerone.com/reports/103998) | ibb | resolved | $500 (list) | 03 | session deserializer UAF; $0; session-lane crossover |
| [RCE-103999](https://hackerone.com/reports/103999) | ibb | resolved | $500 (list) | 03 | GMP unserialize UAF; $0 |
| [RCE-104005](https://hackerone.com/reports/104005) | ibb | resolved | $500 (json) | 04 | zend_eval_const_expr NULL deref; $500 json; paid crash row |
| [RCE-104008](https://hackerone.com/reports/104008) | ibb | resolved | $1,000 (json) | 04 | phar_make_dirstream uninitialized pointer; $1,000 json |
| [RCE-104010](https://hackerone.com/reports/104010) | ibb | resolved | $1,500 (list) | 04 | SOAP serialize_function_call type confusion → RCE; $0; reported upstream to PHP program |
| [RCE-104012](https://hackerone.com/reports/104012) | ibb | resolved | $500 (json) | 03 | unserialize 32-bit int overflow; $500 json |
| [RCE-104016](https://hackerone.com/reports/104016) | ibb | resolved | $1,000 (json) | 03 | ArrayObject unserialization dangling pointer; $1,000 json |
| [RCE-104017](https://hackerone.com/reports/104017) | ibb | resolved | $1,000 (list) | 04 | str_ireplace arbitrary code execution; $0; link-only body |
| [RCE-104018](https://hackerone.com/reports/104018) | ibb | resolved | $1,500 (list) | 03 | multiple UAFs in unserialize; $0 |
| [RCE-104026](https://hackerone.com/reports/104026) | ibb | resolved | $500 (json) | 04 | phar invalid free; $500 json |
| [RCE-104027](https://hackerone.com/reports/104027) | ibb | resolved | $500 (json) | 04 | phar tar memory corruption; $500 json |
| [RCE-104465](https://hackerone.com/reports/104465) | square-open-source | resolved | $2,000 (list) | 01 | git-fastclone ext:// URL → arbitrary command execution; $0; git-transport lane |
| [RCE-105190](https://hackerone.com/reports/105190) | square-open-source | resolved | $2,000 (list) | 01 | git-fastclone Cocaine framework interpolation injection; $0; same tool, second bug |
| [RCE-113928](https://hackerone.com/reports/113928) | rails | resolved | $1,500 (json) | 02 | Rails render :inline RCE; metadata-only (body empty); $1,500 json |
| [RCE-116575](https://hackerone.com/reports/116575) | legalrobot | resolved | $120 (list) | 07 | RCE (upload) — metadata-only; $0; upload-origin |
| [RCE-116937](https://hackerone.com/reports/116937) | Zopim | 404 | $100 (404-list) | dead | 404 — roster-only record; body gone; mirror title: Chat History CSV Export Excel Injection Vulnerability |
| [RCE-119317](https://hackerone.com/reports/119317) | ui | resolved | $1,500 (list) | 01 | AirOS read-only user reaches shell-command execution; $0; auth-context nuance |
| [RCE-121940](https://hackerone.com/reports/121940) | ui | resolved | $1,300 (list) | 01 | Ubiquiti dl-fw.cgi shell injection + CSRF delivery; $0; full advisory embedded in body |
| [RCE-125027](https://hackerone.com/reports/125027) | uber | resolved | $3,000 (json) | 07 | Uber developer portal Angular template injection → reflected XSS (client-side); $3,000 json; XSS-lane reclass |
| [RCE-125980](https://hackerone.com/reports/125980) | uber | resolved | $10,000 (json) | 02 | Uber Jinja2 SSTI in rider.uber.com via email field — RCE claim with full walkthrough; $10,000 json; the corpus SSTI crown |
| [RCE-128750](https://hackerone.com/reports/128750) | ui | resolved | $1,500 (list) | 01 | AirOS server-side response regex injection → speed-test command injection; $0; server-controlled response lane |
| [RCE-131452](https://hackerone.com/reports/131452) | gratipay | not-applicable | - | 08 | outdated PHP 5.4.45 CVE list; not-applicable |
| [RCE-132658](https://hackerone.com/reports/132658) | New Relic | 404 | - | dead | 404 — roster-only record; body gone; mirror title: Stored Cross-Site Scripting via Angular Template Injection |
| [RCE-134321](https://hackerone.com/reports/134321) | algolia | resolved | $500 (json) | 03 | Rails secret_token.rb leaked on GitHub (Gitrob) → signed-cookie Ruby marshal deserialize RCE (id output); $500 json; Ruby lane |
| [RCE-134738](https://hackerone.com/reports/134738) | automattic | resolved | $1,337 (list) | 07 | WordPress SOME/XSS → plugin install → RCE (Cure53); $0; client-origin |
| [RCE-135072](https://hackerone.com/reports/135072) | security | resolved | $2,500 (list) | 01 | profile picture → ImageMagick MVG command injection (ImageTragick pre-disclosure, reported upstream); $0 |
| [RCE-137631](https://hackerone.com/reports/137631) | ruby | resolved | - | 01 | Net::SMTP RCPT TO header injection (Ruby upstream disclosure); $0; mail-protocol argument lane |
| [RCE-138824](https://hackerone.com/reports/138824) | LocalTapiola | 404 | $100 (404-list) | dead | 404 — roster-only record; body gone; mirror title: Remote Code Execution in NovaStor NovaBACKUP DataCenter backup software (Hiback) |
| [RCE-139398](https://hackerone.com/reports/139398) | ui | resolved | $2,750 (list) | 01 | AirOS redirect-injection third family row; $0 |
| [RCE-141956](https://hackerone.com/reports/141956) | Pornhub | 404 | $20,000 (404-list) | dead | 404 — roster-only record; body gone; mirror title: [phpobject in cookie] Remote shell/command execution |
| [RCE-142562](https://hackerone.com/reports/142562) | Pornhub | 404 | $10,000 (404-list) | dead | 404 — roster-only record; body gone; mirror title: [RCE] Unserialize to XXE - file disclosure on ams.upload.pornhub.com |
| [RCE-143966](https://hackerone.com/reports/143966) | ibb | resolved | $7,500 (list) | 01 | ImageTragick CVE-2016-3714 insufficient shell-char filtering → (potentially remote) code execution; $7,500 list |
| [RCE-146233](https://hackerone.com/reports/146233) | ibb | resolved | $1,000 (list) | 03 | PHP GC + unserialize UAF (72433); $0; discovered auditing an H1 vendor |
| [RCE-146235](https://hackerone.com/reports/146235) | ibb | resolved | $1,000 (list) | 03 | ZipArchive GC UAF (72434); $0 |
| [RCE-146593](https://hackerone.com/reports/146593) | Pornhub | 404 | $500 (404-list) | dead | 404 — roster-only record; body gone; mirror title: RCE Possible Via Video Manager Export using @ character in Video Title |
| [RCE-146735](https://hackerone.com/reports/146735) | uber | informative | - | 08 | content spoofing labeled Command Injection; informative |
| [RCE-153026](https://hackerone.com/reports/153026) | starbucks | resolved | - | 03 | JBoss JMXInvokerServlet ysoserial CommonsCollections1 on card.starbucks.in — file-found oracle proof; $0; Java anchor |
| [RCE-155657](https://hackerone.com/reports/155657) | owncloud | resolved | $100 (list) | 05 | ownCloud Windows client QT plugin in C:/ stem → DLL hijack → arbitrary code injection; $0; local-user prereq |
| [RCE-158330](https://hackerone.com/reports/158330) | gitlab | resolved | - | 07 | GitLab import token leak → admin → RCE claim; sev critical; $0; token-origin (row-8 lane) |
| [RCE-162955](https://hackerone.com/reports/162955) | slack | resolved | $750 (list) | 05 | Slack Windows client OpenSSL config load path → code injection into other users process; $0; same author |
| [RCE-163292](https://hackerone.com/reports/163292) | Dropbox | 404 | $1,458 (404-list) | dead | 404 — roster-only record; body gone; mirror title: Subtile Code Injection Vulnerability in Dropbox for Windows |
| [RCE-163547](https://hackerone.com/reports/163547) | New Relic | 404 | - | dead | 404 — roster-only record; body gone; mirror title: Java RMI (Remote Code Execution) |
| [RCE-164224](https://hackerone.com/reports/164224) | unikrn | resolved | $400 (list) | 02 | Smarty {php} block → file_get_contents(/etc/passwd) proven; $0; resolved |
| [RCE-167859](https://hackerone.com/reports/167859) | eternal | resolved | - | 06 | Base alpha version code exposure — metadata-only; $0; exposure-only |
| [RCE-168485](https://hackerone.com/reports/168485) | irccloud | resolved | $50 (list) | 08 | nginx 1.4.6 outdated CVE theory without PoC; resolved; theoretical-claim example |
| [RCE-178152](https://hackerone.com/reports/178152) | gitlab | resolved | - | 07 | GitLab import symlink → file read → secrets → marshalled cookies → RCE; sev critical; $0; file-read-origin |
| [RCE-181321](https://hackerone.com/reports/181321) | shopify-scripts | resolved | $20,000 (list) | 04 | mruby Array#to_h OOB via to_ary reentrancy → second-heap-groom RCE claim; $20,000 list |
| [RCE-181879](https://hackerone.com/reports/181879) | shopify-scripts | resolved | $18,000 (json) | 04 | mruby Struct type confusion → RIP control 0x133713371337; $18,000 json |
| [RCE-182104](https://hackerone.com/reports/182104) | udemy | resolved | $300 (list) | 06 | Udemy exposed Jenkins (GitHub SSO) → source/creds/Sendgrid takeover; exposure chain, no RCE shown; $0 |
| [RCE-182169](https://hackerone.com/reports/182169) | ibb | resolved | $500 (json) | 04 | Python FutureIter_throw type confusion → potential func-pointer overwrite; $500 json |
| [RCE-183356](https://hackerone.com/reports/183356) | shopify-scripts | resolved | $10,000 (json) | 04 | mruby break/||= OP_JMP bytecode OOB → spurious-code-execution claim with patch; $10,000 json |
| [RCE-184279](https://hackerone.com/reports/184279) | deptofdefense | resolved | - | 09 | DoD RCE metadata-only; sev critical |
| [RCE-185907](https://hackerone.com/reports/185907) | iandunn-projects | resolved | $25 (json) | 03 | WordPress plugin skeleton unchecked unserialize; $25 json |
| [RCE-185909](https://hackerone.com/reports/185909) | iandunn-projects | resolved | $50 (json) | 03 | audit-trail extension unserialize; $50 json |
| [RCE-186352](https://hackerone.com/reports/186352) | phabricator | resolved | $300 (json) | 07 | Phabricator install script over HTTP → MITM → root RCE; $300 json; supply-chain origin |
| [RCE-188078](https://hackerone.com/reports/188078) | brave | duplicate | - | 05 | Brave save-page .bat on TLD → command execution (duplicate status); $0; user-interaction prereq |
| [RCE-188284](https://hackerone.com/reports/188284) | deptofdefense | resolved | - | 09 | DoD RCE metadata-only; sev critical |
| [RCE-191884](https://hackerone.com/reports/191884) | x | resolved | - | 07 | Twitter Reverb unauth file-create/delete + ext=php → defacement; RCE claimed not achieved; $0; upload/DT-origin |
| [RCE-192318](https://hackerone.com/reports/192318) | shopify-scripts | resolved | $100 (list) | 04 | mrb_vformat heap overflow (%A%n) from fuzzing; $0 |
| [RCE-192485](https://hackerone.com/reports/192485) | shopify-scripts | resolved | $800 (list) | 04 | mrb_vm_exec NULL deref (pool null) — author states DoS, not exploitable; $0; negative example |
| [RCE-192567](https://hackerone.com/reports/192567) | deptofdefense | resolved | - | 09 | DoD RCE metadata-only; sev high |
| [RCE-194564](https://hackerone.com/reports/194564) | nextcloud | resolved | - | 08 | SwiftMailer RCE research placeholder (ongoing); $0; pointer row |
| [RCE-195950](https://hackerone.com/reports/195950) | ibb | resolved | $500 (list) | 03 | unserialize uninitialized-memory → full exploitation (afl-fuzz; PHP 7.0.14) with ROP; $0; PNG-era hands-on writeup |
| [RCE-196380](https://hackerone.com/reports/196380) | shopify-scripts | resolved | $800 (list) | 04 | mrb_vm_exec super() NULL deref crash; $0 |
| [RCE-196386](https://hackerone.com/reports/196386) | shopify-scripts | resolved | $800 (list) | 04 | mrb_vm_exec SIGSEGV (m->env->stack null); $0 |
| [RCE-197693](https://hackerone.com/reports/197693) | shopify-scripts | resolved | $800 (list) | 04 | mrb_vm_exec SIGSEGV line 1681 (proc->body.irep null); $0 |
| [RCE-197958](https://hackerone.com/reports/197958) | ui | resolved | $2,000 (list) | 01 | EdgeSwitch Web GUI root command injection — metadata-only body; media title/severity only |
| [RCE-200909](https://hackerone.com/reports/200909) | ibb | resolved | $500 (json) | 03 | unserialize OOB read (73825); $500 json |
| [RCE-201903](https://hackerone.com/reports/201903) | shopify-scripts | resolved | $100 (json) | 04 | mrb_vm_exec segfault; $100 json; paid crash row |
| [RCE-202582](https://hackerone.com/reports/202582) | shopify-scripts | resolved | $800 (list) | 04 | mrb_obj_instance_eval NULL deref; $0; DoS-grade |
| [RCE-202584](https://hackerone.com/reports/202584) | shopify-scripts | resolved | $800 (list) | 04 | mrb_vm_exec NULL deref; $0; DoS-grade |
| [RCE-202652](https://hackerone.com/reports/202652) | deptofdefense | resolved | - | 09 | DoD RCE metadata-only; sev critical |
| [RCE-202774](https://hackerone.com/reports/202774) | expressionengine | resolved | - | 07 | Type-juggling → PHP object injection → SQLi chain — metadata-only; $0; chain row |
| [RCE-203513](https://hackerone.com/reports/203513) | shopify-scripts | resolved | $100 (list) | 04 | mrb_vm_exec SIGSEGV 1312; $0 |
| [RCE-203600](https://hackerone.com/reports/203600) | deptofdefense | resolved | - | 09 | DoD RCE metadata-only; sev low |
| [RCE-205536](https://hackerone.com/reports/205536) | shopify-scripts | resolved | $800 (json) | 04 | mrb_vm_exec UAF; $800 json; paid |
| [RCE-206227](https://hackerone.com/reports/206227) | imgur | resolved | $2,500 (list) | 03 | GitLab Enterprise static Rails secret → RCE; sev critical; $0; same lane |
| [RCE-207710](https://hackerone.com/reports/207710) | shopify-scripts | resolved | $800 (list) | 04 | mrb heap UAF (recursive M.new(0) fuzz); $0 |
| [RCE-207983](https://hackerone.com/reports/207983) | ibb | resolved | $1,000 (list) | 04 | Perl S_regmatch heap over-read (rt.perl 129024); $0; Perl lane |
| [RCE-210429](https://hackerone.com/reports/210429) | shopify-scripts | resolved | $800 (list) | 04 | mrb_vm_exec NULL deref super() (second PoC); $0 |
| [RCE-210671](https://hackerone.com/reports/210671) | shopify-scripts | resolved | $800 (json) | 04 | mrb_vm_exec NULL derefs; $800 json; paid |
| [RCE-211381](https://hackerone.com/reports/211381) | deptofdefense | resolved | - | 09 | DoD RCE metadata-only; sev critical |
| [RCE-212022](https://hackerone.com/reports/212022) | deptofdefense | resolved | - | 09 | DoD RCE metadata-only; sev critical |
| [RCE-212696](https://hackerone.com/reports/212696) | imgur | resolved | $5,000 (list) | 01 | imgur gm convert argument injection in /edit/process?a=crop → -write pipe exfil; $5,000 list; space-argument lane anchor |
| [RCE-212985](https://hackerone.com/reports/212985) | deptofdefense | resolved | - | 09 | DoD RCE duplicate — metadata-only |
| [RCE-213069](https://hackerone.com/reports/213069) | deptofdefense | duplicate | - | 09 | DoD RCE duplicate — metadata-only |
| [RCE-213776](https://hackerone.com/reports/213776) | deptofdefense | duplicate | - | 09 | DoD RCE duplicate — metadata-only |
| [RCE-214022](https://hackerone.com/reports/214022) | discourse | resolved | $512 (json) | 01 | Discourse admin username backticks → gzip restore RCE; $512 json; second-order credentialed chain |
| [RCE-214845](https://hackerone.com/reports/214845) | shopify-scripts | resolved | $800 (list) | 04 | mrb_vm_exec SIGSEGV 1361; $0 |
| [RCE-216700](https://hackerone.com/reports/216700) | shopify-scripts | resolved | $800 (list) | 04 | heap UAF via recursive constructor fuzz; $0 |
| [RCE-217097](https://hackerone.com/reports/217097) | shopify-scripts | resolved | $100 (list) | 04 | method_missing crash → NULL deref (pc=0x0); $0 |
| [RCE-217790](https://hackerone.com/reports/217790) | shopify | resolved | $1,000 (json) | 07 | Shopify twine template injection → admin-context eval primitive → XSS; $1,000 json; XSS-lane reclass |
| [RCE-218342](https://hackerone.com/reports/218342) | ruby | not-applicable | - | 08 | RCE on Ruby language — junk submission; not-applicable |
| [RCE-221251](https://hackerone.com/reports/221251) | shopify-scripts | resolved | $800 (list) | 04 | heap-buffer-overflow READ in mrb_vm_exec 1556 (afl+ASan); $0 |
| [RCE-221287](https://hackerone.com/reports/221287) | libsass | resolved | - | 04 | libsass Sass::Eval NULL deref (geeknik fuzz); $0; crash batch (sass) |
| [RCE-221294](https://hackerone.com/reports/221294) | starbucks | resolved | - | 03 | JBoss deser on card.starbucks.in — metadata-only body; sev critical; $0 |
| [RCE-222294](https://hackerone.com/reports/222294) | shopify-scripts | resolved | $800 (json) | 04 | heap UAF vm.c:1247; $800 json; paid |
| [RCE-224198](https://hackerone.com/reports/224198) | gitlab | informative | - | 07 | GitLab Sidekiq queue → GitlabShellWorker instance_eval RCE from Redis access; $0; internal-trust prereq |
| [RCE-226245](https://hackerone.com/reports/226245) | deptofdefense | resolved | - | 09 | DoD RCE multiple — metadata-only; sev critical |
| [RCE-226896](https://hackerone.com/reports/226896) | nextcloud | not-applicable | - | 08 | Nextcloud exec() find — shown code uses escapeshellarg; not-applicable; rejected-claim example |
| [RCE-229199](https://hackerone.com/reports/229199) | deptofdefense | resolved | - | 09 | DoD Limited code execution — SSRF-tagged chain; sev high |
| [RCE-230234](https://hackerone.com/reports/230234) | wordpress | resolved | - | 07 | Angular template injection reflected XSS on mercantile.wordpress.org; $0; XSS-lane reclass |
| [RCE-231460](https://hackerone.com/reports/231460) | snapchat | resolved | $15,000 (json) | 06 | Open prod Jenkins instance — metadata-only (body empty); $15,000 json; sev high; weakness tag Information Disclosure |
| [RCE-231687](https://hackerone.com/reports/231687) | deptofdefense | resolved | - | 09 | DoD RCE metadata-only |
| [RCE-231926](https://hackerone.com/reports/231926) | deptofdefense | resolved | - | 09 | DoD RCE metadata-only |
| [RCE-232330](https://hackerone.com/reports/232330) | deptofdefense | resolved | - | 09 | DoD RCE — XXE-tagged chain; sev high |
| [RCE-244724](https://hackerone.com/reports/244724) | wakatime | resolved | - | 08 | unsafe-inline/unsafe-eval CSP best practice; $0; policy row |
| [RCE-250587](https://hackerone.com/reports/250587) | expressionengine | resolved | - | 01 | EE delete_directory exec() with user-controlled filename; pattern-level PoC only; escapeshellarg discipline discussion |
| [RCE-257207](https://hackerone.com/reports/257207) | legalrobot | resolved | $40 (list) | 08 | vague code injection title — metadata-only; $0 |
| [RCE-258117](https://hackerone.com/reports/258117) | snapchat | resolved | $5,000 (list) | 06 | RCE/LFI on test Jenkins via improper auth flow — metadata-only; $5,000 list; cross-ref AUTH vault |
