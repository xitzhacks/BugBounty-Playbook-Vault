---
title: "File Upload case register — 86-row ledger (65 fetched bodies + 21 dead-404 records)"
type: register
built: "2026-11-05"
roster: "h1.security.nathan.sx mirror (4,419 rows, frozen 2017-09-12), title-filter (7 arms → 86 rows, no supplemental; this build is a single-pass funnel)"
case_id_scheme: "FU-<HackerOne report id>"
bounty_rule: "JSON bounty_amount where present (labeled json) · otherwise mirror list figure (labeled list) · 404 rows recorded, never quoted, bounty mirrored as 404-list"
grand_total: "$71,869 all-envelope: class modules 01–09 $45,241/34 paid of 65 live (json $3,426/8 + list $41,815/26) · dead 404-list $26,628/12"
---

# Case register — File Upload

Substate mix (65 fetched): 58 resolved · 7 informative. All 65 fetched rows carry readable
text; 18 deliver it through the disclosed `summaries` field (`body_src=summaries` in
`archive/bodies-full-dump.txt`), the rest through `vulnerability_information`. Zero
dead-row conversions: every 404 stayed 404 over the funnel.

Class census: 01 authless/unrestricted upload → exec 8 · 02 upload-URL SSRF & file-read 6 ·
03 upload → stored XSS / content exec 7 · 04 file inclusion (LFI / include-bypass /
XXE-in-upload) 7 · 05 path traversal read/write/delete 9 · 06 RFD & browser download abuse 6 ·
07 server-side arbitrary file download 8 · 08 upload-ACL & cross-user access 6 ·
09 noise / harden /FP shelf 8 · dead 21.

Bounty arithmetic: JSON $3,426/8 + list $41,815/26 = **$45,241 / 34 paid rows of 65**.
Modules: 01 $20,770/4 · 02 $2,064/6 · 03 $3,295/6 · 04 $500/1 · 05 $8,512/7 · 06 $2,150/2 ·
07 $100/1 · 08 $2,750/5 · 09 $5,100/2. Dead 404-list: $26,628 across 12 of 21 rows.

Weakness census (65): Information Disclosure 11 · Violation of Secure Design Principles 11 ·
Code Injection 8 · XSS Generic 7 · Privilege Escalation 5 · Command Injection Generic 5 ·
Path Traversal 2 · Uncontrolled Resource Consumption 2 · IDOR 2 · SSRF 1 · Memory
Corruption 1 · CSRF 1 · Improper Authentication 1 · Unrestricted Upload of File with
Dangerous Type 1 · XXE 1 · Improper Access Control 1 · (none recorded) 5.

Severity census (65): critical 1 (FU-184596) · high 8 · medium 8 · low 4 · severity
recorded `none` 1 (FU-194351) · not recorded 43.

Era spread (65 disclosed): 2014×6 · 2015×8 · 2016×24 · 2017×27.

Cross-vault shares (11 rows also registered in other vaults): RCE 4836/6674/84374/116575/
135072/258117 (3 of these dead), XXE 105787/232614 (+142562), CSRF 158016 (NOISE shelf),
Open-Redirect 51265, Authentication-Session 258117. Each row below carries its cross note.

| Case | Team | Substate | Bounty | Class | Note |
|---|---|---|---|---|---|
| [FU-713](https://hackerone.com/reports/713) | HackerOne | resolved | $500 (list) | 02 | Profile photo uploaded from a user-supplied URL — the corpus's first upload-URL-fetch row; weakness col: SSRF |
| FU-1092 | Yahoo! | 404 | - | dead | 404 — roster-only record; mirror title: Directory Traversal |
| FU-1675 | Yahoo! | 404 | $1,390 (404-list) | dead | 404 — roster-only record; mirror title: Local file inclusion |
| [FU-3370](https://hackerone.com/reports/3370) | Ruby on Rails | resolved | $1,500 (list) | 05 | CVE-2014-0130 wildcard-segment traversal in the view resolver + backslash bypass of Rack::Protection::PathTraversal (`%5c../`) |
| FU-4836 | Yahoo! | 404 | $800 (404-list) | dead | 404 — RCE-4836 (404-list) carries the same record; mirror title: From Unrestricted File Upload to Remote Command Execution |
| FU-6674 | Yahoo! | 404 | $3,000 (404-list) | dead | 404 — RCE-6674 (404-list) carries the same record; mirror title names RCE/LFI/XSPA/SSRF on `sb*.geo.sp1.yahoo.com` |
| [FU-7929](https://hackerone.com/reports/7929) | HackerOne | informative | - | 09 | Arbitrary uploads land on `hackerone-attachments` S3 — hosting-misuse design note |
| FU-12388 | InVision | 404 | - | dead | 404 — roster-only record; mirror title: Multiple Upload Vulnerability File Upload + File Inclusion |
| [FU-14092](https://hackerone.com/reports/14092) | Slack | informative | - | 04 | Title says RFI; body shows external-image load on the crop page (`?url=`) — recorded as the lane's false-positive exhibit |
| [FU-18371](https://hackerone.com/reports/18371) | jsDelivr | resolved | - | 05 | Staging CDN traversal via overlong UTF-8 (`%c0%af` repeated) read `/etc/passwd` |
| FU-18851 | Sandbox Escape | 404 | $5,000 (404-list) | dead | 404 — roster-only record; mirror title: .NET Type Traversal Vulnerability CVE-2014-0257 |
| [FU-19532](https://hackerone.com/reports/19532) | Uzbey | resolved | - | 09 | No size check on picture upload — slowdown/DoS claim (harden-shelf) |
| FU-20616 | Mail.Ru | 404 | $1,000 (404-list) | dead | 404 — roster-only record; mirror title: e.mail.ru File upload "Chapito" circus |
| FU-20720 | Mail.Ru | 404 | $150 (404-list) | dead | 404 — roster-only record; mirror title: cloud.mail.ru File upload XSS using Content-Type header |
| FU-27704 | Square | 404 | $2,000 (404-list) | dead | 404 — roster-only record; mirror title: malicious file upload |
| [FU-31187](https://hackerone.com/reports/31187) | Bookfresh | resolved | - | 09 | Reflected XSS in the `bk` parameter of the upload-form view (POST-only) — upload-page XSS, not a file-upload sink (FP shelf) |
| [FU-39428](https://hackerone.com/reports/39428) | Phabricator | resolved | $500 (json) | 04 | Phame skin path traversed to attacker-writable `/tmp/test/` — LFI landing on RCE (php include) |
| [FU-39658](https://hackerone.com/reports/39658) | HackerOne | resolved | - | 06 | RFD on the triggers endpoint: stored trigger text reflected, `.bat` extension, `|| calc ||` — the corpus's first RFD row |
| [FU-43440](https://hackerone.com/reports/43440) | Ruby on Rails | resolved | $1,000 (list) | 05 | Arbitrary file-existence oracle in Action Pack (sibling of the CVE-2014-0130 family) |
| [FU-43850](https://hackerone.com/reports/43850) | Vimeo | resolved | $1,000 (list) | 08 | `clip_id` swap on `/upload/select_thumb` reaches thumbnails of private videos (cross-user upload ACL) |
| [FU-45368](https://hackerone.com/reports/45368) | Vimeo | resolved | $100 (list) | 03 | FTP upload path: unterminated filename XSS becomes the video title (auto-naming skips sanitization) |
| [FU-50658](https://hackerone.com/reports/50658) | HackerOne | resolved | - | 06 | `notifications.bat` RFD — report title reflected into a downloadable executable on the platform domain |
| [FU-51265](https://hackerone.com/reports/51265) | Flash | resolved | $2,000 (list) | 06 | Flash `FileReference` upload + 307/308 redirect cross-domain bypass (CVE-2015-0337); team column is literally Adobe's Flash program; cross-listed RDIR-51265 (Open-Redirect class 04) |
| FU-52383 | Dropbox Acquisitions | 404 | - | dead | 404 — roster-only record; mirror title: unknow files Upload in profile photo |
| [FU-59665](https://hackerone.com/reports/59665) | concrete5 | resolved | - | 04 | Dispatcher LFI via `Request::getPathInfo()` header-driven path override (X-Original-URL family) |
| [FU-73480](https://hackerone.com/reports/73480) | Ubiquiti Networks | resolved | $18,000 (list) | 01 | **Corpus crown**: authless arbitrary upload on airMAX via the airOS web server, with authentication bypass attached |
| [FU-84374](https://hackerone.com/reports/84374) | ownCloud | resolved | - | 01 | apps.owncloud.com content dir served an uploaded `.php5` (`phpinfo()`) — upload → RCE; row-10 lane also recorded as RCE-84374 (module 07) |
| [FU-97452](https://hackerone.com/reports/97452) | Shopify | resolved | $500 (json) | 08 | Staff without permission reaches admin-uploaded files (`/admin/rte/assets`) |
| [FU-97501](https://hackerone.com/reports/97501) | Shopify | resolved | $500 (list) | 02 | SVG upload with `xlink:href` makes the server-side parser fetch attacker URLs |
| [FU-97657](https://hackerone.com/reports/97657) | Slack | resolved | $200 (json) | 03 | Java applet `.class` uploaded as `image/jpeg` on slackatwork — applet XSS (team display: Slack) |
| [FU-97672](https://hackerone.com/reports/97672) | Twitter | resolved | $1,120 (list) | 03 | mopub app-icon upload: html-as-jpg + Content-Type swap → stored XSS on images.mopub.com |
| [FU-105787](https://hackerone.com/reports/105787) | Informatica | resolved | - | 04 | XXE in a file-upload feature (team-summary record, 71 B); XXE-class ledger line owned by XXE-105787 |
| [FU-107960](https://hackerone.com/reports/107960) | Ubiquiti Networks | resolved | $150 (list) | 06 | RFD on `community.ubnt.com` restapi session endpoint — `callback=\%22\|\|calc\|\|` |
| FU-111269 | Pornhub | 404 | $1,500 (404-list) | dead | 404 — roster-only record; mirror title: [ssrf] libav vulnerable during conversion of uploaded videos (live libav family: FU-115857) |
| [FU-114389](https://hackerone.com/reports/114389) | Zomato | resolved | - | 01 | Outdated MailPoet plugin on business-blog.zomato.com — remote-upload path to RCE |
| [FU-115857](https://hackerone.com/reports/115857) | Imgur | resolved | $800 (list) | 02 | vidgif playlist drives Lavf: SSRF + `concat:`/`subfile` `file:///etc/passwd` read — module-02 headline |
| [FU-116575](https://hackerone.com/reports/116575) | Legal Robot | resolved | $120 (list) | 01 | "Any file upload was accepted without filter" → RCE; unfiltered-upload confirmation record; also RCE-116575 (module 07) |
| [FU-122475](https://hackerone.com/reports/122475) | Imgur | resolved | $5,000 (list) | 05 | `/edit/process?imageid=../../` — second-largest live payout; traversal-file-read headline |
| [FU-126374](https://hackerone.com/reports/126374) | Uber | informative | - | 09 | Extension-only validation on driver documents lets plain text land as `.png` on uber-documents S3 (phishing shelf) |
| [FU-130591](https://hackerone.com/reports/130591) | Moneybird | resolved | $25 (list) | 03 | Stored XSS via SVG upload (Moneybird summary record) |
| [FU-131028](https://hackerone.com/reports/131028) | Moneybird | resolved | $100 (list) | 09 | Malicious-extension attachment upload — filter-hardening record |
| FU-134032 | New Relic | 404 | - | dead | 404 — roster-only record; mirror title: newrelic.com rails directory traversal vuln |
| [FU-135072](https://hackerone.com/reports/135072) | HackerOne | resolved | $2,500 (list) | 01 | Pre-disclosure ImageTragick: profile-picture upload passes ASCII to ImageMagick → MVG delegates command injection; reported upstream; RCE-135072 cross-registered with matching $2,500 (list) |
| FU-140548 | Mail.Ru | 404 | $160 (404-list) | dead | 404 — roster-only record; mirror title: [upload-X.my.mail.ru] /uploadphoto Insecure Direct Object References |
| [FU-142135](https://hackerone.com/reports/142135) | VK.com | resolved | $1,500 (json) | 03 | `upload.php?act=transport` callback eval chain → `requestAnimationFrame` gadget executes uploader-controlled JS |
| FU-142352 | Pornhub | 404 | $1,500 (404-list) | dead | 404 — roster-only record; mirror title: (Pornhub & Youporn & Brazzers ANDROID APP) Upload Malicious APK |
| FU-142562 | Pornhub | 404 | $10,000 (404-list) | dead | 404 — one dead row, three ledgers: FU-142562 here + RCE-142562 + XXE-142562; largest dead figure in this vault: unserialize → XXE file disclosure on `ams.upload.pornhub.com` |
| [FU-143903](https://hackerone.com/reports/143903) | Slack | resolved | $500 (list) | 08 | Upload into another member's private IM channel via channel id |
| [FU-145604](https://hackerone.com/reports/145604) | Nextcloud | informative | - | 09 | Avatar check passes image1.php carrying valid JPEG bytes (renamed server-side, so no live impact — harden shelf) |
| [FU-145950](https://hackerone.com/reports/145950) | Nextcloud | resolved | $250 (list) | 08 | Android copy-feature writes into a shared folder with no edit privilege |
| [FU-147570](https://hackerone.com/reports/147570) | concrete5 | resolved | - | 04 | Fix-bypass of FU-59665's `strpos()` patch: missing `../\`, `..\/`, `/\..`, `\/..` backslash variants |
| FU-150783 | OLX | 404 | - | dead | 404 — roster-only record; mirror title: Arbitrary File Reading |
| [FU-155690](https://hackerone.com/reports/155690) | Nextcloud | resolved | - | 03 | Theming logo/login uploads serve attacker HTML (`../data/themedinstancelogo`); PHP renders as text |
| [FU-158016](https://hackerone.com/reports/158016) | Instacart | resolved | $50 (json) | 02 | `list[remote_image_url]` SSRF — localhost:21 returns an SSH banner (also CSRF-158016 NOISE shelf; CSRF vault excluded it; FUP owns the class line) |
| [FU-158021](https://hackerone.com/reports/158021) | Instacart | resolved | $100 (json) | 05 | rmagick error leaks full upload tmp path `/var/app/20160809T225101Z/tmp/uploads/…` — path-disclosure exhibit |
| [FU-158505](https://hackerone.com/reports/158505) | Instacart | informative | - | 06 | RFD on `searches.bat` with `term="\|\|start chrome…"` (David Sopas) |
| [FU-159820](https://hackerone.com/reports/159820) | Instacart | resolved | $150 (list) | 02 | Upload list-image probe bundle: port/SSH banner, rmagick Tell, memory-overflow 502 |
| [FU-163421](https://hackerone.com/reports/163421) | Nextcloud | resolved | - | 05 | WP 4.5.3 `admin-ajax.php` `plugin=../../../…` traversal below `/dev/random` — traversal-DoS hybrid (sumofpwn advisory) |
| [FU-167481](https://hackerone.com/reports/167481) | Nextcloud | resolved | - | 08 | Android `FileUploader` sticky broadcasts readable by third-party receivers (upload metadata disclosure) |
| [FU-172694](https://hackerone.com/reports/172694) | Udemy | informative | - | 09 | Any-type upload to the bucket declared intended behavior (content enforced on egress) |
| [FU-179034](https://hackerone.com/reports/179034) | Paragon Initiative Enterprises | resolved | - | 04 | Gregwar RST `.. include::` directive → LFI to `/etc/hosts` in Airship CMS (sev high) |
| [FU-182557](https://hackerone.com/reports/182557) | Brave Software | informative | - | 06 | Downloadable-link naming: any site path becomes `.com`/`.exe` content — browser download-abuse (informative) |
| [FU-183568](https://hackerone.com/reports/183568) | WordPress | resolved | $350 (list) | 05 | BuddyPress `bp_avatar_set` `original_file` → arbitrary file **deletion** via `unlink()` (the corpus's delete primitive) |
| [FU-183925](https://hackerone.com/reports/183925) | U.S. Dept Of Defense | resolved | - | 07 | USTRANSCOM unrestricted file download / path traversal (summary record, sev low) |
| [FU-183978](https://hackerone.com/reports/183978) | U.S. Dept Of Defense | resolved | - | 07 | Army system LFI - crafted_URL_download (summary record, sev high) |
| [FU-184596](https://hackerone.com/reports/184596) | U.S. Dept Of Defense | resolved | - | 01 | Internet-reachable upload tool on a Navy system, sev critical, Command Injection weak col (summary record) |
| [FU-186326](https://hackerone.com/reports/186326) | U.S. Dept Of Defense | resolved | - | 07 | `downloadfile?fileString=…` traversal to `/etc/shadow` (summary record, sev low) |
| FU-187413 | Trello | 404 | - | dead | 404 — roster-only record; mirror title: SVG Uploads / Attachments can be viewed by anyone that knows the URL |
| [FU-191243](https://hackerone.com/reports/191243) | U.S. Dept Of Defense | resolved | - | 01 | Signature-based malicious-file test bypass (korprit) — upload-bypass shelf of the exec lane (sev medium) |
| FU-193877 | Trello | 404 | - | dead | 404 — roster-only record; mirror title: The contact page is vulnerable to self-XSS via upload file name |
| [FU-194351](https://hackerone.com/reports/194351) | Yelp | resolved | $100 (list) | 07 | yelpblog.com serves `wp-includes` PHP sources for download (severity recorded `none`) |
| [FU-196448](https://hackerone.com/reports/196448) | U.S. Dept Of Defense | resolved | - | 07 | DoD local file inclusion (fransrosen) — summary record, sev medium |
| [FU-201529](https://hackerone.com/reports/201529) | Ubiquiti Networks | resolved | $150 (list) | 01 | AirFibre 3.2 `login.cgi` multipart upload without auth into `tmp/upload` — disk-fill DoS surface; body notes the RCE combination gap |
| FU-202681 | arxius | 404 | - | dead | 404 — roster-only record; mirror title: XSS in content type header when uploading file |
| [FU-203515](https://hackerone.com/reports/203515) | WordPress | resolved | $350 (list) | 03 | WP 4.7.2 media-upload: oversized-filename interpolated into `file_exceeds_size_limit` l10n → XSS in the admin media manager |
| [FU-208481](https://hackerone.com/reports/208481) | U.S. Dept Of Defense | resolved | - | 07 | DoD remote file inclusion (sp1d3rs) — summary record, sev medium |
| [FU-213558](https://hackerone.com/reports/213558) | Discourse | resolved | $512 (json) | 05 | Restore-from-backup tar with symlink into `/uploads/…` → `/etc/passwd` read at `/uploads/…/[file].jpg` (FUP-owned ledger line; RCE README module-01 text cites the mechanics, no RCE register row) |
| FU-221928 | Trello | 404 | $128 (404-list) | dead | 404 — roster-only record; mirror title: Malicious file can be hidden as Card Attachment or Card Cover image |
| [FU-228377](https://hackerone.com/reports/228377) | Discourse | resolved | $64 (json) | 02 | IMG-in-message fetch follows redirects to `gopher://…:80/test123` + ftp — server-side request with Ruby UA |
| [FU-230714](https://hackerone.com/reports/230714) | U.S. Dept Of Defense | resolved | - | 07 | DotNetNuke EventsCalendar `downloaddoc.aspx?f=~/downloaddoc.aspx` (summary record, sev medium) |
| [FU-230870](https://hackerone.com/reports/230870) | U.S. Dept Of Defense | resolved | - | 07 | Second DoD instance of the same EventsCalendar primitive; body duplicated verbatim modulo row id |
| [FU-232614](https://hackerone.com/reports/232614) | Weblate | resolved | - | 04 | Uploaded XLF carries `<!DOCTYPE foo [ <!ENTITY xxe SYSTEM "file:///etc/passwd" >]>`; Weblate 2.15-dev; XXE-232614 cross-registered (full-body) |
| FU-248745 | Trello | 404 | - | dead | 404 — roster-only record; mirror title references unpatched FU-221928: Unviladate File Upload to XSS on trello-attachment Bucket |
| [FU-254200](https://hackerone.com/reports/254200) | Unikrn | resolved | $50 (list) | 05 | S3 avatar filename `test2../../../../../../test2.jpg` escapes the per-user directory and can overwrite bucket files (sev medium) |
| [FU-258117](https://hackerone.com/reports/258117) | Snapchat | resolved | $5,000 (list) | 09 | Test Jenkins via any Google account → script-console RCE; RCE-258117 module 06 + AUTH-258117 class-08 cross-ledgers carry same $5,000 (list); RCE build read it metadata-only, this build's re-read delivers a summaries body — page state moved |
| [FU-258460](https://hackerone.com/reports/258460) | Quora | resolved | $500 (list) | 08 | Exported `net.gotev.uploadservice.UploadService` — any installed app ships `app_webview/Cookies` to a chosen URL |
