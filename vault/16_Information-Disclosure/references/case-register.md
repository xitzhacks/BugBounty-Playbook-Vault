---
title: "INFO case register — 362-row ledger (h1-brain corpus: bucket-340 + 22 merges)"
type: register
built: "2026-11-07"
roster: "h1-brain disclosed_reports.db (3,673 rows; sha256 8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4) — classified.json info-disclosure bucket (340) + module_map_all _adjacent_unclassified merges (22)"
case_id_scheme: "INFO-<HackerOne report id>"
bounty_rule: "DB bounty_amount where present (labeled $) · - = no figure in DB (not evidence of non-payment)"
module_rule: "frozen in archive/classes.json (bodies-win classification; merges labeled 06)"
---

# Case register — Information Disclosure

Corpus: 362 rows · 161 with bounty figures · **$281,925** · bucket-340: $217,375/149, max $25,000 (INFO-3000510) · merges: $64,550/12, max $50,000 (INFO-1087489) · evidence: 356 full-body / 6 metadata-only (GHSL one-liners).

Class census: 01 GraphQL-API-Objects-Exposure 21 (13 paid, $19,252.2) · 02 HackerOne-Reports-Bounty-Privacy 51 (28 paid, $83,580) · 03 User-PII-Location-Privacy 128 (56 paid, $47,014) · 04 File-Path-Errors-Secrets-Leaks 104 (41 paid, $48,697) · 05 Protocol-Memory-Disclosure 17 (6 paid, $15,468) · 06 Adjacent-Disclosure-Noise 41 (= 19 in-bucket adjacent + 22 unclassified merges; 17 paid, $67,914).

Weakness census (362): `Information Disclosure` 302 · `Privacy Violation` 23 · `Cleartext Storage of Sensitive Information` 15 · `None` (merges) 22. CVE-carrying rows: 12 (see CVE column; concentrated in module 05).

Bounty arithmetic: $19,252.2 + $83,580 + $47,014 + $48,697 + $15,468 + $67,914 = **$281,925.2 (161 rows)**. Bucket-only: 01–05 adjacent (=321 rows: $214,011.2) minus nothing — formal split: bucket-340 = modules 01–05 ($214,011.2/144) + 19 `_adjacent` rows of module 06 ($3,364/5) = $217,375.2/149; merges = 22 rows of module 06 ($64,550/12).

| Case | Team | Bounty | Module | Evidence | CVE | Title (short) |
|---|---|---|---|---|---|---|
| [INFO-46345](https://hackerone.com/reports/46345) | whisper | - | 04 | full | — | Directory index and information disclosure |
| [INFO-46366](https://hackerone.com/reports/46366) | whisper | - | 04 | full | — | Error stack trace |
| [INFO-53004](https://hackerone.com/reports/53004) | coinbase | $100 | 06 | full | — | Blacklist bypass on Callback URLs |
| [INFO-57918](https://hackerone.com/reports/57918) | whisper | $50 | 03 | full | — | Insecure Local Data Storage : Application stores data using a binary sqlite database |
| [INFO-63324](https://hackerone.com/reports/63324) | ibb | $2,000 | 05 | full | CVE-2015-3044 | Flash Player information disclosure (etc.) CVE-2015-3044, PSIRT-3298 |
| [INFO-64731](https://hackerone.com/reports/64731) | vkcom | $100 | 04 | full | — | Able to intercept app Traffic after choosing up the Secured Connection using SSL (HTTPS) |
| [INFO-73276](https://hackerone.com/reports/73276) | ibb | $2,000 | 06 | full | CVE-2015-3044 · CVE-2015-3079 | Internet-based attacker can run Flash apps in local sandboxes by using special URL schemes (PSIRT-3299, CVE-20… |
| [INFO-91343](https://hackerone.com/reports/91343) | imgur | - | 04 | full | — | Information disclosure (No rate limting in forgot password & other login) |
| [INFO-117902](https://hackerone.com/reports/117902) | vkcom | - | 03 | full | — | Дорк |
| [INFO-124100](https://hackerone.com/reports/124100) | shopify | $1,500 | 04 | full | — | Shopify GitHub Login and Password exposed all private source code might be available. |
| [INFO-125200](https://hackerone.com/reports/125200) | uber | $3,000 | 03 | full | — | Lack of rate limiting on get.uber.com leads to enumeration of promotion codes and estimation of a lower bound … |
| [INFO-135756](https://hackerone.com/reports/135756) | shopify | - | 03 | full | — | View all deleted comments and rating of any app . |
| [INFO-136454](https://hackerone.com/reports/136454) | ibb | $3,000 | 04 | full | — | User credentials leak and arbitrary local file read/leak due to same-origin-policy violation |
| [INFO-136850](https://hackerone.com/reports/136850) | vimeo | - | 03 | full | — | Images and Subtitles Leakage from private videos |
| [INFO-142549](https://hackerone.com/reports/142549) | x | $560 | 03 | full | — | Information Disclosure through .DS_Store in ██████████ |
| [INFO-142773](https://hackerone.com/reports/142773) | torproject | - | 05 | full | — | 16 instances where return value of OpenSSL i2d_RSAPublicKey is discarded -- might lead to use of uninitialized… |
| [INFO-143935](https://hackerone.com/reports/143935) | x | $1,260 | 03 | full | — | [sms-be-vip.twitter.com] vulnerable to Jetleak |
| [INFO-145150](https://hackerone.com/reports/145150) | uber | - | 03 | full | — | Bulk UUID enumeration via invite codes |
| [INFO-147577](https://hackerone.com/reports/147577) | coinbase | $100 | 04 | full | — | Application error message |
| [INFO-148050](https://hackerone.com/reports/148050) | security | - | 02 | full | — | Know undisclosed Bounty Amount when Bounty Statistics are enabled. |
| [INFO-155618](https://hackerone.com/reports/155618) | vimeo | - | 03 | full | — | Watch any Password Video without password |
| [INFO-157699](https://hackerone.com/reports/157699) | security | - | 02 | full | — | Disclosure of external users invited to a specific report |
| [INFO-158021](https://hackerone.com/reports/158021) | instacart | $100 | 04 | full | — | Image Upload Path Disclosure |
| [INFO-159526](https://hackerone.com/reports/159526) | security | $500 | 02 | full | — | Information leakage of private program |
| [INFO-162822](https://hackerone.com/reports/162822) | instacart | $150 | 03 | full | — | Fetch private list metadata and any user's personal name |
| [INFO-163464](https://hackerone.com/reports/163464) | legalrobot | - | 03 | full | — | User Information sent to client through websockets |
| [INFO-163476](https://hackerone.com/reports/163476) | legalrobot | - | 04 | full | — | Information Disclosure in AWS S3 Bucket |
| [INFO-165131](https://hackerone.com/reports/165131) | instacart | $50 | 01 | full | — | Seemingly sensitive information at /api/v2/zones |
| [INFO-166265](https://hackerone.com/reports/166265) | yelp | - | 04 | full | — | Verification of E-Mail address possible on https://biz.yelp.com/login and https://biz.yelp.com/forgot |
| [INFO-166661](https://hackerone.com/reports/166661) | ruby | - | 05 | full | — | Arbitrary heap overread in strscan on 32 bit Ruby, patch included |
| [INFO-166942](https://hackerone.com/reports/166942) | x | - | 04 | full | — | leaking Digits OAuth authorization to third party websites |
| [INFO-174632](https://hackerone.com/reports/174632) | ibb | - | 05 | full | — | Information disclosure in mmap module - python 2.7.12 |
| [INFO-174645](https://hackerone.com/reports/174645) | files | - | 04 | full | — | Existence of Folder path by guessing the path through response |
| [INFO-174721](https://hackerone.com/reports/174721) | x | - | 03 | full | — | View liked twits of private account via publish.twitter.com |
| [INFO-174882](https://hackerone.com/reports/174882) | yelp | - | 03 | full | — | Requesting Show CheckIn Alert for Non Friend User |
| [INFO-175320](https://hackerone.com/reports/175320) | brave | - | 04 | full | — | 2 Directory Listing on ledger.brave.com & vault-staging.brave.com |
| [INFO-178506](https://hackerone.com/reports/178506) | instacart | $100 | 03 | full | — | Access private list metadata |
| [INFO-182358](https://hackerone.com/reports/182358) | security | $10,000 | 02 | full | — | Partial disclosure of report activity through new "Export as .zip" feature |
| [INFO-185862](https://hackerone.com/reports/185862) | x | $560 | 03 | full | — | Twitter for android is exposing user's location to any installed android app |
| [INFO-186230](https://hackerone.com/reports/186230) | security | $12,500 | 02 | full | — | Internal attachments can be exported via "Export as .zip" feature |
| [INFO-188719](https://hackerone.com/reports/188719) | security | $10,000 | 02 | full | — | Information Disclosure in /skills call |
| [INFO-193314](https://hackerone.com/reports/193314) | zendesk | - | 03 | full | — | SMTP user enumeration via mail.zendesk.com |
| [INFO-194721](https://hackerone.com/reports/194721) | yelp | - | 03 | full | — | Verification of email addresses possible through https://www.yelp.com/signup/facebook |
| [INFO-196655](https://hackerone.com/reports/196655) | security | - | 03 | full | — | Disclose any user's private email through API |
| [INFO-201984](https://hackerone.com/reports/201984) | ui | - | 04 | full | — | Wordpress directories/files visible to internet |
| [INFO-207321](https://hackerone.com/reports/207321) | shopify-scripts | - | 06 | full | — | Controlled address leak due to type confusion - ASLR bypass |
| [INFO-210190](https://hackerone.com/reports/210190) | security | $500 | 02 | full | — | Transitioning a Private Program to Public Does Not Clear Previously Private Updates to Hackers |
| [INFO-210572](https://hackerone.com/reports/210572) | rockstargames | - | 04 | full | — | Full path Disclosure in Rockstargames.com██████████ |
| [INFO-211418](https://hackerone.com/reports/211418) | rockstargames | $150 | 04 | full | — | Source Code Disclosure (CGI) |
| [INFO-211477](https://hackerone.com/reports/211477) | shopify | - | 04 | full | — | Stealing users' facebook access tokens - kitcrm.com |
| [INFO-212067](https://hackerone.com/reports/212067) | algolia | $100 | 04 | full | — | An “algobot”-s GitHub access token was leaked |
| [INFO-213558](https://hackerone.com/reports/213558) | discourse | $512 | 04 | full | — | Arbitrary Local-File Read from Admin - Restore From Backup due to Symlinks |
| [INFO-213942](https://hackerone.com/reports/213942) | phabricator | - | 04 | full | — | Differential "Show Raw File" feature exposes generated files to unauthorised users |
| [INFO-218465](https://hackerone.com/reports/218465) | x | $280 | 04 | full | — | [staging-engineering.gnip.com] Publicly accessible GIT directory |
| [INFO-219197](https://hackerone.com/reports/219197) | x | - | 06 | full | — | [██████████.gnip.com] .htpasswd disclosure |
| [INFO-221328](https://hackerone.com/reports/221328) | x | - | 06 | full | — | HTTP 401 response injection on "amp.twimg.com/amplify-web-player/prod/source.html" through "image_src" paramet… |
| [INFO-222870](https://hackerone.com/reports/222870) | phabricator | - | 03 | full | — | IRC-Bot exposes information |
| [INFO-228377](https://hackerone.com/reports/228377) | discourse | $64 | 06 | full | — | SSRF in upload IMG through URL |
| [INFO-228399](https://hackerone.com/reports/228399) | discourse | $256 | 03 | full | — | Any authenticated user can download full list of users, including email |
| [INFO-231917](https://hackerone.com/reports/231917) | nextcloud | $50 | 04 | full | CVE-2018-16467 · CVE-2019-5449 | Shared file link - password protection bypass under certain conditions |
| [INFO-237381](https://hackerone.com/reports/237381) | automattic | - | 06 | full | — | SSRF and local file disclosure in https://wordpress.com/media/videos/ via FFmpeg HLS processing |
| [INFO-242727](https://hackerone.com/reports/242727) | nextcloud | $75 | 03 | full | — | Android content provider exposes password-protected share password hashes |
| [INFO-247628](https://hackerone.com/reports/247628) | security | $1,500 | 02 | full | — | Reading redacted data via hackbot's answers |
| [INFO-248599](https://hackerone.com/reports/248599) | coinbase | $100 | 06 | full | — | Information disclosure same issue #176002 |
| [INFO-248693](https://hackerone.com/reports/248693) | grab | - | 04 | full | — | Git repository found |
| [INFO-252580](https://hackerone.com/reports/252580) | torproject | - | 03 | full | — | Scrollbar Width permits detecting browser platform |
| [INFO-253429](https://hackerone.com/reports/253429) | torproject | $3,000 | 03 | full | — | Linux TBB SFTP URI allows local IP disclosure |
| [INFO-255978](https://hackerone.com/reports/255978) | unikrn | $50 | 03 | full | — | Non-Cloudflare IPs allowed to access origin servers |
| [INFO-256647](https://hackerone.com/reports/256647) | torproject | - | 03 | full | — | Simple CSS line-height identifies platform |
| [INFO-257942](https://hackerone.com/reports/257942) | torproject | $100 | 03 | full | — | languagechange event fires simultaneously on all tabs |
| [INFO-258084](https://hackerone.com/reports/258084) | nextcloud | - | 04 | full | — | Access to all files of remote user through shared file |
| [INFO-258460](https://hackerone.com/reports/258460) | quora | - | 04 | full | — | [Quora Android] Possible to steal arbitrary files from mobile device |
| [INFO-258578](https://hackerone.com/reports/258578) | brave | $250 | 03 | full | — | application/x-brave-tab should not be readable. |
| [INFO-258585](https://hackerone.com/reports/258585) | brave | $100 | 03 | full | — | OS username disclosure |
| [INFO-262649](https://hackerone.com/reports/262649) | gsa_bbp | $150 | 04 | full | — | Information disclosure (system username) in the x-amz-meta-s3cmd-attrs response header on federation.data.gov |
| [INFO-268382](https://hackerone.com/reports/268382) | gsa_bbp | - | 04 | full | — | Nginx misconfiguration leading to direct PHP source code download |
| [INFO-268888](https://hackerone.com/reports/268888) | x | $280 | 04 | full | — | Sensitive Information Disclosure https://cards-dev.twitter.com |
| [INFO-269230](https://hackerone.com/reports/269230) | security | - | 02 | full | — | Emails of invited collaborators are disclosed in full in payload for report participants |
| [INFO-270993](https://hackerone.com/reports/270993) | security | - | 02 | full | — | resolved bugs in a program are public despite the program settings |
| [INFO-271176](https://hackerone.com/reports/271176) | lyst | - | 03 | full | — | Bypassing one-time checkout router page (revealing payment information) |
| [INFO-271506](https://hackerone.com/reports/271506) | security | - | 06 | full | — | Banned researcher gets email updates on a private program. |
| [INFO-278191](https://hackerone.com/reports/278191) | x | $140 | 04 | full | — | Listing of Amazon S3 Bucket accessible to any amazon authenticated user (metrics.pscp.tv) |
| [INFO-282748](https://hackerone.com/reports/282748) | torproject | - | 03 | full | — | Detecting Tor Browser UI Language |
| [INFO-288955](https://hackerone.com/reports/288955) | irccloud | - | 04 | full | — | [IRCCloud Android] Theft of arbitrary files leading to token leakage |
| [INFO-289568](https://hackerone.com/reports/289568) | security | - | 02 | full | — | Program profile metrics endpoint contains mean time to triage, even when turned off |
| [INFO-293299](https://hackerone.com/reports/293299) | security | - | 02 | full | — | Validation message in Bounty award endpoint can be used to determine program balances |
| [INFO-300181](https://hackerone.com/reports/300181) | brave | $200 | 03 | full | — | Torrent Viewer extension web service available on all interfaces |
| [INFO-301526](https://hackerone.com/reports/301526) | security | - | 04 | full | — | Invitation token leaks to https://bat.bing.com |
| [INFO-302651](https://hackerone.com/reports/302651) | portswigger | $200 | 04 | full | — | Leak of Platform Authentication credentials via Repeater |
| [INFO-302885](https://hackerone.com/reports/302885) | security | $500 | 05 | full | CVE-2017-15277 | ImageMagick GIF coder vulnerability leading to memory disclosure |
| [INFO-310105](https://hackerone.com/reports/310105) | automattic | - | 03 | full | — | Disclosure of 152 cookie names via crafted input |
| [INFO-310946](https://hackerone.com/reports/310946) | security | $2,000 | 02 | full | — | The request tells the number of private programs, the new system of authorization /invite/token |
| [INFO-316810](https://hackerone.com/reports/316810) | security | $250 | 03 | full | — | Can read features from any user |
| [INFO-318099](https://hackerone.com/reports/318099) | grab | - | 03 | full | — | Registration enabled on ███grab.com |
| [INFO-318399](https://hackerone.com/reports/318399) | security | $250 | 02 | full | — | Program profile_metrics.json contains time to triage for deptofdefense even it's turned off |
| [INFO-327088](https://hackerone.com/reports/327088) | security | - | 02 | full | — | Extra program metrics disclosed via /PROGRAM_NAME json response |
| [INFO-329957](https://hackerone.com/reports/329957) | x | - | 03 | full | — | Tracking of users on third-party websites using the Twitter cookie, due to a flaw in authenticating image requ… |
| [INFO-331489](https://hackerone.com/reports/331489) | nextcloud | - | 06 | full | CVE-2019-5453 | Extremly simple way to bypass Nextcloud-Client PIN/Fingerprint lock |
| [INFO-342978](https://hackerone.com/reports/342978) | security | $2,500 | 01 | full | — | Team object in GraphQL disclosed total number of whitelisted hackers |
| [INFO-343464](https://hackerone.com/reports/343464) | security | $2,500 | 01 | full | — | Team object in GraphQL discloses team group names and permissions |
| [INFO-345152](https://hackerone.com/reports/345152) | shopify | - | 04 | full | — | Publicly Accessible Datadog link |
| [INFO-347693](https://hackerone.com/reports/347693) | security | $2,500 | 02 | full | — | Program metrics disclosed response_efficiency_percentage via /program_name json response despite the team deci… |
| [INFO-348443](https://hackerone.com/reports/348443) | gitlab | $300 | 04 | full | — | Snippet JS template allows attacker to read a user's private snippets |
| [INFO-351555](https://hackerone.com/reports/351555) | reverb | - | 06 | full | — | Disclosure of all uploads to Cloudinary via hardcoded api secret in Android app |
| [INFO-353310](https://hackerone.com/reports/353310) | security | $500 | 03 | full | — | People who interviewed for HackerOne security analyst position can be enumerated and their personal email addr… |
| [INFO-356566](https://hackerone.com/reports/356566) | security | - | 06 | full | — | HackerOne support disclosing report state without checking user identity |
| [INFO-358007](https://hackerone.com/reports/358007) | bumble | - | 03 | full | — | Compromising the user ID |
| [INFO-360811](https://hackerone.com/reports/360811) | starbucks | - | 04 | full | — | Information Leak - Github - JMS Information |
| [INFO-361951](https://hackerone.com/reports/361951) | liberapay | - | 03 | full | — | Exploiting JSONP callback on /username/charts.json endpoint leads to information disclosure despite user's pri… |
| [INFO-367581](https://hackerone.com/reports/367581) | reverb | - | 02 | full | — | Basic auth details is still work on report ( 351555 ) |
| [INFO-370777](https://hackerone.com/reports/370777) | udemy | - | 03 | full | — | [affiliates.udemy.com] Wordpress user admin information discloure |
| [INFO-374907](https://hackerone.com/reports/374907) | gsa_bbp | - | 03 | full | — | Root user disclosure in data.gov domain though x-amz-meta-s3cmd-attrs header |
| [INFO-375083](https://hackerone.com/reports/375083) | slack | $500 | 04 | full | — | Private application files can be uploaded to Slack via malicious uploader |
| [INFO-377107](https://hackerone.com/reports/377107) | owncloud | $750 | 04 | full | — | Possible to steal any protected files on Android |
| [INFO-378122](https://hackerone.com/reports/378122) | security | - | 03 | full | — | HackerOne customer submitted sensitive link to VirusTotal, exposing confidential information |
| [INFO-380317](https://hackerone.com/reports/380317) | security | - | 02 | full | — | Team object exposes amount of participants in a private program to non-invited users |
| [INFO-386596](https://hackerone.com/reports/386596) | semmle | - | 03 | full | — | Email Not Completely Deleted after Deleting an account |
| [INFO-386997](https://hackerone.com/reports/386997) | security | $2,500 | 02 | full | — | Private program policy page still accessible after user left the program |
| [INFO-389454](https://hackerone.com/reports/389454) | starbucks | - | 06 | full | — | Backup Source Code Detected |
| [INFO-389600](https://hackerone.com/reports/389600) | security | - | 01 | full | — | TeamProfile exposes partially sensitive information through GraphQL |
| [INFO-391385](https://hackerone.com/reports/391385) | yelp | - | 06 | full | — | Unauthorized Use of Victim Credit Card |
| [INFO-396467](https://hackerone.com/reports/396467) | snapchat | - | 04 | full | — | Github Token Leaked publicly for https://github.sc-corp.net |
| [INFO-397031](https://hackerone.com/reports/397031) | security | - | 02 | full | — | Disclosure of top 10 vulnerability types for programs that haven't enabled the Insights feature |
| [INFO-397508](https://hackerone.com/reports/397508) | chaturbate | - | 04 | full | — | Web cache deception attack - expose token information |
| [INFO-397527](https://hackerone.com/reports/397527) | grab | - | 04 | full | — | Leaking sensitive information on Github lead full access to all Grab Slack channels |
| [INFO-399174](https://hackerone.com/reports/399174) | x | - | 02 | full | — | Access MoPub Reports Data even after Company removed you from their MoPub Account. |
| [INFO-402410](https://hackerone.com/reports/402410) | bumble | - | 03 | full | — | Расшифровка всех типов шифрованных ID |
| [INFO-409973](https://hackerone.com/reports/409973) | shopify | - | 01 | full | — | Some store settings/data are accessible to "No Access" permission users on GraphQL LiveView operation |
| [INFO-410015](https://hackerone.com/reports/410015) | security | $3,000 | 02 | full | — | Discrepancy in hacker profile report count may reveal existence of a private program by publishing a report |
| [INFO-411822](https://hackerone.com/reports/411822) | chaturbate | - | 03 | full | — | Password protected rooms total number of viewers disclosure to unauthorized members |
| [INFO-415622](https://hackerone.com/reports/415622) | shopify | $500 | 01 | full | — | PII disclosure -- Past team members & their email ID(personal email) can be viewed by Staff member with no per… |
| [INFO-417170](https://hackerone.com/reports/417170) | shopify | $500 | 01 | full | — | Using GraphQL, STAFF with NO explicit permissions on Store can retrieve Shopify Payments Balance. |
| [INFO-418474](https://hackerone.com/reports/418474) | security | $500 | 06 | full | — | Disclosing a private program in an external link if program is paused |
| [INFO-419883](https://hackerone.com/reports/419883) | shopify | $802.2 | 01 | full | — | H1514 [beerify.shopifycloud.com] GraphQL discloses internal beer consumption |
| [INFO-421009](https://hackerone.com/reports/421009) | shopify | $1,000 | 03 | full | — | H1514 Deanonymizing Exchange Marketplace private listings |
| [INFO-423388](https://hackerone.com/reports/423388) | shopify | $1,500 | 01 | full | — | H1514 Get access to non public information by pivoting with graphql queries |
| [INFO-423506](https://hackerone.com/reports/423506) | shopify | - | 03 | full | — | H1514 Extract information about other sites (new sites) through Affiliate/Referral pages |
| [INFO-425719](https://hackerone.com/reports/425719) | shopify | - | 04 | full | — | Disclosure of Github Issues |
| [INFO-428010](https://hackerone.com/reports/428010) | nextcloud | $50 | 03 | full | — | Talk / spreed: Disclosure of Room names and participants for password protected rooms |
| [INFO-430854](https://hackerone.com/reports/430854) | kaspersky | - | 03 | full | — | Kaspersky Password Manager allows websites to access user's address data |
| [INFO-434763](https://hackerone.com/reports/434763) | x | $2,940 | 03 | full | — | Incorrect details on OAuth permissions screen allows DMs to be read without permission |
| [INFO-446238](https://hackerone.com/reports/446238) | gitlab | $500 | 04 | full | — | EXIF metadata not stripped from JPG group logos |
| [INFO-452973](https://hackerone.com/reports/452973) | security | $500 | 02 | full | — | Inline banner on Report page discloses whether organization runs a private program |
| [INFO-472013](https://hackerone.com/reports/472013) | x | $2,940 | 03 | full | — | Changing email address on Twitter for Android unsets "Protect your Tweets" |
| [INFO-477222](https://hackerone.com/reports/477222) | gitlab | - | 03 | full | CVE-2019-5463 | Last build status and coverage leaked to unauthorized users |
| [INFO-488643](https://hackerone.com/reports/488643) | security | - | 03 | full | — | Disclosure of h1 challenges name through the calendar |
| [INFO-489146](https://hackerone.com/reports/489146) | security | - | 01 | full | — | Confidential data of users and limited metadata of programs and reports accessible via GraphQL |
| [INFO-491473](https://hackerone.com/reports/491473) | x | $560 | 03 | full | — | Protected tweets exposure through the URL |
| [INFO-493176](https://hackerone.com/reports/493176) | security | $2,500 | 02 | full | — | Partial report contents leakage - via HTTP/2 concurrent stream handling |
| [INFO-495497](https://hackerone.com/reports/495497) | gitlab | - | 03 | full | — | Know whether private project name exists or not within a group using link comments |
| [INFO-495525](https://hackerone.com/reports/495525) | iandunn-projects | $50 | 03 | full | — | XSSI: Quick Navigation Interface - leak of private page/post titles |
| [INFO-503300](https://hackerone.com/reports/503300) | unikrn | - | 06 | full | — | █████████ on CRM server without authorization |
| [INFO-505424](https://hackerone.com/reports/505424) | x | $1,470 | 03 | full | — | Twitter ID exposure via error-based side-channel attack |
| [INFO-508490](https://hackerone.com/reports/508490) | nextcloud | - | 03 | full | CVE-2019-15623 | Nextcloud domain and name of every user leaked to lookup server |
| [INFO-509574](https://hackerone.com/reports/509574) | security | $500 | 03 | full | — | Invited team member can disclosure slack channels |
| [INFO-509924](https://hackerone.com/reports/509924) | gitlab | $12,000 | 04 | full | — | JSON serialization of any Project model results in all Runner tokens being exposed through Quick Actions |
| [INFO-511440](https://hackerone.com/reports/511440) | zomato | - | 04 | full | — | credentials leakage in public lead to view dev websites |
| [INFO-516237](https://hackerone.com/reports/516237) | ibb | - | 05 | full | CVE-2019-9638 | Uninitialized read in exif_process_IFD_in_MAKERNOTE |
| [INFO-532225](https://hackerone.com/reports/532225) | zomato | $750 | 06 | full | — | [Zomato Order] Insecure deeplink leads to sensitive information disclosure |
| [INFO-540301](https://hackerone.com/reports/540301) | automattic | - | 03 | full | — | Wordpress VIP leaks email of the test a/c |
| [INFO-541020](https://hackerone.com/reports/541020) | valve | - | 03 | full | — | GetGlobalAchievementPercentagesForApp is missing the same release checks as GetSchemaForGame |
| [INFO-574639](https://hackerone.com/reports/574639) | x | $280 | 02 | full | — | Reports Modal in app.mopub.com Disclose by any user |
| [INFO-604945](https://hackerone.com/reports/604945) | brave | - | 03 | full | — | Tor IP leak caused by the PDF Viewer extension in certain situations |
| [INFO-605608](https://hackerone.com/reports/605608) | gitlab | - | 03 | full | — | [information disclosure] Validate existence of a private project. |
| [INFO-612231](https://hackerone.com/reports/612231) | x | - | 04 | full | — | Github Token Leaked publicly for https://github.com/mopub |
| [INFO-623588](https://hackerone.com/reports/623588) | ibb | - | 05 | full | CVE-2019-11038 | Uninitialized read in gdImageCreateFromXbm |
| [INFO-629892](https://hackerone.com/reports/629892) | grammarly | - | 06 | full | — | Lack of CSRF header validation at https://g-mail.grammarly.com/profile |
| [INFO-633001](https://hackerone.com/reports/633001) | gitlab | - | 01 | full | CVE-2019-15576 | Private System Note Disclosure using GraphQL |
| [INFO-636560](https://hackerone.com/reports/636560) | gitlab | - | 03 | full | CVE-2019-15577 | Project Milestones Disclosed Via Groups When the Victim disabled milestones access in project settings |
| [INFO-640488](https://hackerone.com/reports/640488) | security | - | 02 | full | — | Total bounties paid amount is disclosed because of redesign of the Program Profiles |
| [INFO-645264](https://hackerone.com/reports/645264) | security | - | 02 | full | — | Program Email Nofication settings ignored when being added as an external contributor |
| [INFO-654198](https://hackerone.com/reports/654198) | security | $500 | 02 | full | — | Manipulate hacker profile and private program hacktivity to expose your name as researchers who is actively su… |
| [INFO-663729](https://hackerone.com/reports/663729) | brave | - | 06 | full | — | [Brave browser] WebTorrent has DNS rebinding vulnerability |
| [INFO-666722](https://hackerone.com/reports/666722) | omise | - | 03 | full | — | Email enumeration at SignUp page |
| [INFO-669438](https://hackerone.com/reports/669438) | security | $500 | 06 | full | — | [Bypass #645264] Report title disclosure despite the program settings for email notification is set to "No Con… |
| [INFO-669776](https://hackerone.com/reports/669776) | security | - | 02 | full | — | Disclosure of Program email Title Report when being removed as contributor. Bypass for Report #645264 |
| [INFO-674757](https://hackerone.com/reports/674757) | security | $500 | 02 | full | — | Total Paid Bounty Paid can be disclose |
| [INFO-674774](https://hackerone.com/reports/674774) | x | $280 | 04 | full | — | AppLovin API Key hardcoded in a Github repo |
| [INFO-685909](https://hackerone.com/reports/685909) | security | - | 02 | full | — | Searching from Hacktivity returns hits for words in limited disclosure reports that are not visible |
| [INFO-689997](https://hackerone.com/reports/689997) | security | $500 | 02 | full | — | Disclosure of Email title report in quick award paypout email (no content mode) |
| [INFO-696266](https://hackerone.com/reports/696266) | security | $500 | 02 | full | — | "Bounties paid in the last 90 days" discloses the undisclosed bounty amount in program statistics |
| [INFO-707433](https://hackerone.com/reports/707433) | security | - | 01 | full | — | Disclosure of `payment_transactions` for programs via GraphQL query |
| [INFO-715192](https://hackerone.com/reports/715192) | security | $2,500 | 01 | full | — | Private program disclosure via `vpn_suspended` GraphQL query |
| [INFO-715740](https://hackerone.com/reports/715740) | deptofdefense | $750 | 03 | full | — | [HTA2] Receiving████ access request on @wearehackerone.com email address |
| [INFO-723175](https://hackerone.com/reports/723175) | imgur | - | 03 | full | — | De-anonymization Attack: Cross Site Information Leakage |
| [INFO-724944](https://hackerone.com/reports/724944) | security | - | 03 | full | — | latest_activity_id and latest_activity_at may disclose information about internal activities to unauthorized u… |
| [INFO-729040](https://hackerone.com/reports/729040) | shopify | $500 | 04 | full | — | Shopify's SF and LA offices Dashboard Information disclosed via Public Gist |
| [INFO-753725](https://hackerone.com/reports/753725) | nordsecurity | - | 03 | full | — | Disclosure of User Information |
| [INFO-753868](https://hackerone.com/reports/753868) | zenly | - | 04 | full | — | Insecure Storage and Overly Permissive API Keys in Android App |
| [INFO-770209](https://hackerone.com/reports/770209) | security | $2,500 | 01 | full | — | Unauthorized user can obtain `report_sources` attribute through Team GraphQL object |
| [INFO-800109](https://hackerone.com/reports/800109) | security | $500 | 02 | full | — | An invite-only's program submission state is accessible to users no longer part of the program |
| [INFO-803141](https://hackerone.com/reports/803141) | nordsecurity | - | 06 | full | — | Unauthorized User Can Delete Any User Account |
| [INFO-813421](https://hackerone.com/reports/813421) | nordsecurity | - | 03 | full | — | Account deletion requests not entirely honoured. Misinformation even after seeking clarification from customer… |
| [INFO-826176](https://hackerone.com/reports/826176) | security | - | 02 | full | — | program_analytics_benchmarks query shows information not visible in public |
| [INFO-838685](https://hackerone.com/reports/838685) | ibb | - | 05 | full | CVE-2020-1934 | Use of uninitialized value in ftp_getrc_msg method of mod_proxy_ftp.c |
| [INFO-848625](https://hackerone.com/reports/848625) | shopify | $500 | 01 | full | — | None permission staff member can identify installed application and products attached to it |
| [INFO-850447](https://hackerone.com/reports/850447) | gitlab | $10,000 | 04 | full | — | gitlab-workhorse bypass in Gitlab::Middleware::Multipart allowing files in `allowed_paths` to be read |
| [INFO-853355](https://hackerone.com/reports/853355) | gitlab | - | 04 | full | — | Unauthorized access to private project security dashboard |
| [INFO-858915](https://hackerone.com/reports/858915) | shopify | - | 04 | full | — | CircleCI token in github repo allows for access to sensitive build information |
| [INFO-861940](https://hackerone.com/reports/861940) | semrush | - | 04 | full | — | OAuth `redirect_uri` bypass using IDN homograph attack resulting in user's access token leakage |
| [INFO-864712](https://hackerone.com/reports/864712) | zomato | $200 | 04 | full | — | Page has a link to google drive which has logos and a few customer phone recordings |
| [INFO-871142](https://hackerone.com/reports/871142) | security | $500 | 02 | full | — | Disclosure of the name of a program that has a private part with an external link |
| [INFO-871749](https://hackerone.com/reports/871749) | security | - | 02 | full | — | Unauthorized access to metadata of undisclosed reports that were retested |
| [INFO-874778](https://hackerone.com/reports/874778) | curl | - | 03 | full | CVE-2020-8169 | CVE-2020-8169: Partial password leak over DNS on HTTP redirect |
| [INFO-880089](https://hackerone.com/reports/880089) | smartsheet | $100 | 04 | full | — | Smartsheet employees email disclosure through enpoint after login. |
| [INFO-880863](https://hackerone.com/reports/880863) | gitlab | - | 02 | full | — | Todos are not redacted when membership changes - Access to (confidential) issues and merge requests |
| [INFO-882412](https://hackerone.com/reports/882412) | shopify | $1,500 | 03 | full | — | OrderListInitial leaks order details |
| [INFO-886287](https://hackerone.com/reports/886287) | github-security-lab | $500 | 06 | metadata | — | Java: CWE-532 sensitive info logging |
| [INFO-901775](https://hackerone.com/reports/901775) | shopify | - | 04 | full | — | Get analytics token using only apps permission |
| [INFO-917875](https://hackerone.com/reports/917875) | shopify | $1,000 | 01 | full | — | STAFF "No-Permissions" on the Store can retrieve the details Order via exchangeReceiptSend |
| [INFO-948876](https://hackerone.com/reports/948876) | curl | - | 03 | full | CVE-2020-8231 | CVE-2020-8231: Connect-only connections can use the wrong connection |
| [INFO-952771](https://hackerone.com/reports/952771) | kubernetes | - | 03 | full | CVE-2020-8565 · CVE-2019-11250 | CVE-2019-11250 remains in effect. |
| [INFO-958374](https://hackerone.com/reports/958374) | security | $500 | 03 | full | — | Pentester can obtain information about other pentesters who applied for the same test, but weren't accepted |
| [INFO-961757](https://hackerone.com/reports/961757) | x | - | 03 | full | — | Twitter Media Studio Source Information Disclosure With Analyst Role |
| [INFO-961929](https://hackerone.com/reports/961929) | shopify | $1,500 | 03 | full | — | Ability to see password protected content by bypassing the password page of shopify preview URL for new develo… |
| [INFO-962462](https://hackerone.com/reports/962462) | gitlab | - | 04 | full | CVE-2020-13351 | Unauthorized user is able to access schedule pipeline variables and values |
| [INFO-966383](https://hackerone.com/reports/966383) | kubernetes | - | 04 | full | CVE-2020-8563 | secret leaks in vsphere cloud controller manager log |
| [INFO-968165](https://hackerone.com/reports/968165) | shopify | $2,500 | 03 | full | — | Disclose customer orders details by shopify chat application. |
| [INFO-968174](https://hackerone.com/reports/968174) | shopify | $500 | 03 | full | — | Disclose STUFF member name and make actions. |
| [INFO-972355](https://hackerone.com/reports/972355) | gitlab | - | 01 | full | — | Able to leak private email of any user given his/her username via graphql |
| [INFO-975047](https://hackerone.com/reports/975047) | shopify | $1,000 | 03 | full | — | User sensitive information disclosure |
| [INFO-978143](https://hackerone.com/reports/978143) | security | $2,500 | 01 | full | — | Team object in GraphQL disclosed private_comment |
| [INFO-981796](https://hackerone.com/reports/981796) | basecamp | - | 04 | full | — | Information Disclosure of Garbage Collection Cycle |
| [INFO-1004412](https://hackerone.com/reports/1004412) | acronis | - | 04 | full | — | Possible LDAP username and password disclosed on Github |
| [INFO-1007988](https://hackerone.com/reports/1007988) | automattic | - | 04 | full | — | Able to comment/view in others support ticket at https://en.instagram-brand.com/requests/dashboard |
| [INFO-1018336](https://hackerone.com/reports/1018336) | shopify | - | 03 | full | — | Customer's full name disclosure via Shopify Chat (by email lookup) |
| [INFO-1021885](https://hackerone.com/reports/1021885) | basecamp | $1,000 | 03 | full | — | Bypass of image rewriting / tracking blocker via srcset |
| [INFO-1021906](https://hackerone.com/reports/1021906) | shopify | $2,900 | 04 | full | — | [Information Disclosure] Amazon S3 Bucket of Shopify Ping (iOS) have public access of other users image |
| [INFO-1023572](https://hackerone.com/reports/1023572) | acronis | - | 03 | full | — | [acronis.secure.force.com] - Insecure Salesforce default/custom object permissions leads to information disclo… |
| [INFO-1023669](https://hackerone.com/reports/1023669) | shopify | - | 01 | full | — | Staff with no permissions can listen to Shopify Ping conversations by registering to its different WebSocket E… |
| [INFO-1024668](https://hackerone.com/reports/1024668) | brave | $100 | 04 | full | CVE-2020-8276 | Brave Browser potentially logs the last time a Tor window was used |
| [INFO-1026252](https://hackerone.com/reports/1026252) | github-security-lab | $1,800 | 06 | metadata | — | [Java] CWE-927: Sensitive broadcast |
| [INFO-1040166](https://hackerone.com/reports/1040166) | curl | - | 05 | full | CVE-2020-8284 | CVE-2020-8284: trusting FTP PASV responses |
| [INFO-1042716](https://hackerone.com/reports/1042716) | elastic | $1,000 | 03 | full | — | Async search stores authorization headers in clear text |
| [INFO-1054382](https://hackerone.com/reports/1054382) | portswigger | $1,000 | 06 | full | CVE-2021-29416 | HTML Injection in Swing can disclose netNTLM hash or cause DoS |
| [INFO-1065041](https://hackerone.com/reports/1065041) | fetlife | - | 04 | full | — | Google API key leaked to Public |
| [INFO-1067547](https://hackerone.com/reports/1067547) | automattic | - | 06 | full | — | Unauthenticated access to webmail at maildev.happytools.dev leading to compromised wordpress site api.happytoo… |
| [INFO-1069039](https://hackerone.com/reports/1069039) | reddit | - | 04 | full | — | GPS metadata preserved when converting HEIF to PNG |
| [INFO-1069335](https://hackerone.com/reports/1069335) | h1-ctf | - | 03 | full | — | How The Hackers Saved Christmas |
| [INFO-1070081](https://hackerone.com/reports/1070081) | automattic | - | 03 | full | — | information disclosure lead to disclose users private notes |
| [INFO-1072893](https://hackerone.com/reports/1072893) | logitech | $200 | 03 | full | — | Sensitive information disclosure to shared access user via streamlabs platform api |
| [INFO-1077022](https://hackerone.com/reports/1077022) | brave | - | 03 | full | CVE-2021-22917 | Brave Browser Tor Window leaks user's real IP to the external DNS server |
| [INFO-1079630](https://hackerone.com/reports/1079630) | acronis | $50 | 04 | full | — | licenses key disclosure |
| [INFO-1080437](https://hackerone.com/reports/1080437) | bumble | $600 | 03 | full | — | Bumble API exposes read status of chat messages |
| [INFO-1083922](https://hackerone.com/reports/1083922) | shopify | - | 03 | full | — | [h1-2102] Information disclosure - ShopifyPlus add user displays existing Shopify ID fullname |
| [INFO-1085332](https://hackerone.com/reports/1085332) | shopify | $1,900 | 01 | full | — | [h1-2102] shopApps query from the graphql at /users/api returns all existing created apps, including private o… |
| [INFO-1087489](https://hackerone.com/reports/1087489) | shopify | $50,000 | 06 | full | — | Github access token exposure |
| [INFO-1091303](https://hackerone.com/reports/1091303) | shopify | - | 01 | full | — | [h1-2102] [Yaworski's Broskis] Low privilege user can read POS PINs via graphql and elevate his privilege |
| [INFO-1101882](https://hackerone.com/reports/1101882) | curl | - | 06 | full | CVE-2021-22876 | CVE-2021-22876: Automatic referer leaks credentials |
| [INFO-1102546](https://hackerone.com/reports/1102546) | shopify | - | 06 | full | — | Is the Google Bucket Meant To Be Publicly Listable? https://cdn.shopify.com/shop-assets/ |
| [INFO-1121972](https://hackerone.com/reports/1121972) | acronis | $100 | 04 | full | — | admin password disclosure via log file |
| [INFO-1122177](https://hackerone.com/reports/1122177) | reddit | - | 04 | full | — | Third party app could steal access token as well as protected files using inAppBrowser |
| [INFO-1122661](https://hackerone.com/reports/1122661) | github-security-lab | $4,500 | 06 | metadata | — | [Java] CWE-312: Query to detect cleartext storage of sensitive information using Android SharedPreferences |
| [INFO-1122662](https://hackerone.com/reports/1122662) | github-security-lab | $1,800 | 06 | metadata | — | [Java] CWE-598: Use of GET Request Method with Sensitive Query Strings |
| [INFO-1145454](https://hackerone.com/reports/1145454) | ruby | $500 | 05 | full | CVE-2021-31810 · CVE-2020-8284 · CVE-2007-1562 | lib/net/ftp.rb: trusting PASV responses allow client abuse |
| [INFO-1161401](https://hackerone.com/reports/1161401) | nextcloud | $250 | 03 | full | CVE-2022-24886 | Notification implicit PendingIntent in com.nextcloud.client allows to access contacts |
| [INFO-1172852](https://hackerone.com/reports/1172852) | wordpress | - | 03 | full | — | PII of users can be downloaded from export pages |
| [INFO-1173436](https://hackerone.com/reports/1173436) | nextcloud | $350 | 03 | full | CVE-2021-32653 | Default settings leak federated cloud id to lookup server of all users |
| [INFO-1176461](https://hackerone.com/reports/1176461) | curl | $1,000 | 05 | full | CVE-2021-22898 | CVE-2021-22898: TELNET stack contents disclosure |
| [INFO-1215251](https://hackerone.com/reports/1215251) | nextcloud | $100 | 03 | full | CVE-2021-32707 | Bypass of privacy filter / tracking pixel blocker |
| [INFO-1219011](https://hackerone.com/reports/1219011) | security | $500 | 02 | full | — | Report Bulk endpoint "agree-on-going-public" action may reveal Report disclosure state for invite-only program… |
| [INFO-1223882](https://hackerone.com/reports/1223882) | curl | - | 05 | full | CVE-2021-22925 · CVE-2021-22898 | CVE-2021-22925: TELNET stack contents disclosure again |
| [INFO-1225164](https://hackerone.com/reports/1225164) | x | $560 | 03 | full | — | Identify the mobile number of a twitter user |
| [INFO-1234406](https://hackerone.com/reports/1234406) | bumble | - | 03 | full | — | Exfiltrating a victim's exact location (to within 5m) |
| [INFO-1241849](https://hackerone.com/reports/1241849) | basecamp | - | 06 | full | — | Information Disclosure .htaccess accesible for public |
| [INFO-1245741](https://hackerone.com/reports/1245741) | zenly | - | 03 | full | — | Friend Request Flow Exposes User Data |
| [INFO-1249056](https://hackerone.com/reports/1249056) | brave | $400 | 04 | full | — | Brave Browser permanently timestamps & logs connection times for all v2 domains ~/.config/BraveSoftware/Brave-… |
| [INFO-1256375](https://hackerone.com/reports/1256375) | shopify | $5,000 | 04 | full | — | Blog posts atom feed of a store with password protection can be accessed by anyone |
| [INFO-1262907](https://hackerone.com/reports/1262907) | shopify | - | 04 | full | — | Apache Flink Dashboard exposure at https://streaming-sales-model-production.flink.shopifykloud.com |
| [INFO-1264725](https://hackerone.com/reports/1264725) | security | - | 04 | full | — | Information disclosure - Feedback is accessible on Public profile even after 'disallowed' at https://hackerone… |
| [INFO-1276373](https://hackerone.com/reports/1276373) | algolia | - | 06 | full | — | Information disclosure -> 2fa bypass -> POST exploitation |
| [INFO-1285115](https://hackerone.com/reports/1285115) | security | - | 02 | full | — | Leaked H1's Employees Email addresses,meeting info on private bug bounty program ████████ |
| [INFO-1298809](https://hackerone.com/reports/1298809) | shopify | $500 | 03 | full | — | Senseitive data Related to Shopify Host -> https://shopify.zendesk.com/ |
| [INFO-1331728](https://hackerone.com/reports/1331728) | nextcloud | - | 03 | full | CVE-2021-39225 | Cards in Deck are readable by any user |
| [INFO-1337422](https://hackerone.com/reports/1337422) | nextcloud | - | 04 | full | CVE-2021-41233 | Folder architecture and Filesizes of private file drop shares can be getten |
| [INFO-1337624](https://hackerone.com/reports/1337624) | brave | $500 | 03 | full | — | Information disclosure-Referer leak |
| [INFO-1338781](https://hackerone.com/reports/1338781) | nextcloud | - | 04 | full | CVE-2021-41181 | User files is disclosed when someone called while the screen is locked |
| [INFO-1342422](https://hackerone.com/reports/1342422) | basecamp | - | 06 | full | — | Subdomain Takeover due to ████████ NS records at us-east4.37signals.com |
| [INFO-1354334](https://hackerone.com/reports/1354334) | nextcloud | - | 04 | full | CVE-2022-24906 | Error in Deleting Deck cards attachment reveals the full path of the website |
| [INFO-1365761](https://hackerone.com/reports/1365761) | github-security-lab | $1,800 | 06 | metadata | — | [Java] CWE-200: Query to detect exposure of sensitive information from android file intent |
| [INFO-1392511](https://hackerone.com/reports/1392511) | security | $1,000 | 03 | full | — | HackerOne Staging uses Production data for testing |
| [INFO-1405673](https://hackerone.com/reports/1405673) | shopify | - | 04 | full | — | Sidekiq dashboard exposed at notary.shopifycloud.com |
| [INFO-1423704](https://hackerone.com/reports/1423704) | fetlife | - | 03 | full | — | Able to detect if a user is FetLife supporter although this user hides their support badge in fetlife.com/conv… |
| [INFO-1424291](https://hackerone.com/reports/1424291) | fetlife | - | 03 | full | — | Able to access private picture/video/writing when requesting for their JSON response |
| [INFO-1474017](https://hackerone.com/reports/1474017) | omise | $100 | 04 | full | — | Open S3 Bucket Accessible by any User |
| [INFO-1484168](https://hackerone.com/reports/1484168) | automattic | - | 04 | full | — | De-anonymize anonymous tips through the Tumblr blog network |
| [INFO-1491127](https://hackerone.com/reports/1491127) | security | $500 | 04 | full | — | Private invitation links/tokens leak to third-party analytics site |
| [INFO-1520685](https://hackerone.com/reports/1520685) | nextcloud | $100 | 03 | full | CVE-2022-24890 | Moderator can enable cam/mic remotely if cam/mic-permission was disabled while user has activated cam/mic |
| [INFO-1526609](https://hackerone.com/reports/1526609) | github-security-lab | $1,800 | 06 | metadata | — | [Java]: CWE-200 - Query to detect insecure WebResourceResponse implementation |
| [INFO-1551588](https://hackerone.com/reports/1551588) | ibb | $480 | 03 | full | CVE-2022-27775 | CVE-2022-27775: Bad local IPv6 connection reuse |
| [INFO-1575014](https://hackerone.com/reports/1575014) | stripe | $1,000 | 04 | full | — | Limited path traversal in Node.js SDK leads to PII disclosure |
| [INFO-1584718](https://hackerone.com/reports/1584718) | shopify | $500 | 06 | full | — | Information disclosure ( Google Sales Channel ) |
| [INFO-1590237](https://hackerone.com/reports/1590237) | automattic | - | 03 | full | — | Unauthenticated Private Messages DIsclosure via wordpress Rest API |
| [INFO-1595281](https://hackerone.com/reports/1595281) | ibb | - | 05 | full | CVE-2022-28615 | Read beyond bounds in ap_strcmp_match() [zhbug_httpd_47.7] |
| [INFO-1595290](https://hackerone.com/reports/1595290) | ibb | - | 05 | full | CVE-2022-30556 | Controllable read beyond bounds in lua_websocket_readbytes() [zhbug_httpd_126] |
| [INFO-1595299](https://hackerone.com/reports/1595299) | ibb | - | 05 | full | CVE-2022-28614 | Read beyond bounds via ap_rwrite() [zhbug_httpd_47.2] |
| [INFO-1605962](https://hackerone.com/reports/1605962) | shopify | $500 | 03 | full | — | store internal email disclosed through shopify-data-exporter |
| [INFO-1624152](https://hackerone.com/reports/1624152) | deptofdefense | - | 04 | full | — | insecure gitlab repositories at ████████ [HtUS] |
| [INFO-1626236](https://hackerone.com/reports/1626236) | deptofdefense | $500 | 03 | full | — | Critical sensitive information Disclosure. [HtUS] |
| [INFO-1626281](https://hackerone.com/reports/1626281) | snapchat | - | 04 | full | — | Password reset tokens sent to CSP reporting endpoints |
| [INFO-1643962](https://hackerone.com/reports/1643962) | gitlab | - | 04 | full | — | Path paths and file disclosure vulnerabilities at influxdb.quality.gitlab.net |
| [INFO-1662194](https://hackerone.com/reports/1662194) | omise | - | 04 | full | — | Secret API Key is logged in cleartext |
| [INFO-1668723](https://hackerone.com/reports/1668723) | brave | $700 | 04 | full | — | Security token and handler name leak from window.braveBlockRequests |
| [INFO-1668815](https://hackerone.com/reports/1668815) | brave | $400 | 03 | full | — | Persistent user tracking is possible using window.caches, by avoiding Brave Shields |
| [INFO-1752146](https://hackerone.com/reports/1752146) | ibb | $2,400 | 03 | full | CVE-2022-32221 | POST following PUT confusion |
| [INFO-1762764](https://hackerone.com/reports/1762764) | expediagroup_bbp | - | 04 | full | — | Sensitive information for phpinfo.php at https://products.ean.com/ |
| [INFO-1782467](https://hackerone.com/reports/1782467) | indrive | - | 03 | full | — | Disclosure of users' ip address whenever they view my fright offer on image preview (Without interaction) |
| [INFO-1784310](https://hackerone.com/reports/1784310) | nextcloud | - | 04 | full | CVE-2023-26041 | Messages can still be seen on conversation after expiring when cron is misconfigured |
| [INFO-1785079](https://hackerone.com/reports/1785079) | indrive | - | 03 | full | — | # Drivers can access the customers phone number, current location without getting their offer accepted! |
| [INFO-1785145](https://hackerone.com/reports/1785145) | indrive | - | 04 | full | — | Full access to InDrive jira panel via exposed API token |
| [INFO-1826141](https://hackerone.com/reports/1826141) | security | $500 | 02 | full | — | HackerOne Undisclosed Report Leak via PoC of Full Disclosure on Hacktivity |
| [INFO-1869613](https://hackerone.com/reports/1869613) | security | - | 02 | full | — | Attachment in published HackerOne report exposure private program |
| [INFO-1886143](https://hackerone.com/reports/1886143) | security | - | 03 | full | — | information disclosure of another company bug on video. |
| [INFO-1940443](https://hackerone.com/reports/1940443) | snapchat | $250 | 04 | full | — | internal dev tokens disclosure |
| [INFO-1989901](https://hackerone.com/reports/1989901) | mozilla | - | 04 | full | — | If rate limit is hit, IP address is leaked to anyone who tries to login |
| [INFO-2032716](https://hackerone.com/reports/2032716) | security | - | 03 | full | — | An attacker can can view any hacker email via /SaveCollaboratorsMutation operation name |
| [INFO-2045722](https://hackerone.com/reports/2045722) | security | - | 03 | full | — | inviting collaborator using email disclose the hackerone account related to the user |
| [INFO-2053051](https://hackerone.com/reports/2053051) | security | - | 02 | full | — | Hackerone All Private Program Name Leaked to Public Via Collaborator OR Attacker can Easily Dump all Private P… |
| [INFO-2053396](https://hackerone.com/reports/2053396) | mozilla | - | 06 | full | — | Possibility of Deface through translation tool - www.mozilla.com |
| [INFO-2054222](https://hackerone.com/reports/2054222) | security | $500 | 02 | full | — | Usernames still visible on report export pdf despite "I want to redact all usernames" is selected |
| [INFO-2063636](https://hackerone.com/reports/2063636) | x | - | 03 | full | — | Twitter Subscriptions Information Disclosure |
| [INFO-2097377](https://hackerone.com/reports/2097377) | gitlab | $100 | 04 | full | — | Information Disclosure - Pvt Gitlab Issue Disclosing Through GitLab Unfiltered YouTube channel. |
| [INFO-2101087](https://hackerone.com/reports/2101087) | security | $2,500 | 02 | full | — | Able to see Bonus amount given to a report even if the bounty and Bonus is not visible to public or mentioned … |
| [INFO-2101165](https://hackerone.com/reports/2101165) | nextcloud | - | 04 | full | CVE-2023-48305 | user_ldap app logs user passwords in the log file on level debug |
| [INFO-2107680](https://hackerone.com/reports/2107680) | basecamp | $8,868 | 05 | full | — | AWS keys and user cookie leakage via uninitialized memory leak in outdated librsvg version in Basecamp |
| [INFO-2122644](https://hackerone.com/reports/2122644) | security | $500 | 02 | full | — | Names not completely redacted despite "Redact the names of the involved users" is selected |
| [INFO-2123957](https://hackerone.com/reports/2123957) | torproject | $200 | 03 | full | — | 'Request English versions of web pages for enhanced privacy' keeps previous (grayed out) settings |
| [INFO-2134874](https://hackerone.com/reports/2134874) | security | - | 03 | full | — | Hackers two email disclosed on submission at hackerone hactivity |
| [INFO-2180521](https://hackerone.com/reports/2180521) | security | - | 04 | full | — | Google Docs link in JS files allows editing & reading survey information |
| [INFO-2193454](https://hackerone.com/reports/2193454) | khealth | - | 06 | full | — | Information disclouser from URL parameter "access" lead to Account Takeover |
| [INFO-2209665](https://hackerone.com/reports/2209665) | ibb | - | 04 | full | CVE-2023-40712 | Secrets can be unmasked in the "Rendered Template" |
| [INFO-2213251](https://hackerone.com/reports/2213251) | security | $2,500 | 02 | full | — | New Search Feature: Search for non-public words in limited disclosure reports |
| [INFO-2215434](https://hackerone.com/reports/2215434) | security | $100 | 03 | full | — | Hacker email disclosed on submission at hackerone hactivity |
| [INFO-2243710](https://hackerone.com/reports/2243710) | ibb | $405 | 03 | full | CVE-2023-45143 | Cookie headers are not cleared in cross-domain redirect in undici-fetch |
| [INFO-2244229](https://hackerone.com/reports/2244229) | x | $1,500 | 04 | full | — | Cross-Domain Leakage of X Username / UserID due to Dynamically Generated JS File |
| [INFO-2264960](https://hackerone.com/reports/2264960) | exness | - | 06 | full | — | Unrestricted Access to Celery Flower Instance |
| [INFO-2278865](https://hackerone.com/reports/2278865) | security | $50 | 02 | full | — | Some limited confidential information can still be accessed after a user exits a private program |
| [INFO-2310620](https://hackerone.com/reports/2310620) | security | - | 02 | full | — | New Hacktivity features:Bounty rewards leakage Where programs doesn’t decide to disclose bounty in limited dis… |
| [INFO-2322082](https://hackerone.com/reports/2322082) | security | - | 02 | full | — | Being able to disclose IBB bounty table of any public program |
| [INFO-2376909](https://hackerone.com/reports/2376909) | nextcloud | - | 04 | full | — | Possible to enumerate valid files in password protected shares/files drop shares as well as spam folder with f… |
| [INFO-2382120](https://hackerone.com/reports/2382120) | security | - | 03 | full | — | Creation of bounties through Customer API leads to private email disclosure |
| [INFO-2387297](https://hackerone.com/reports/2387297) | mozilla | - | 06 | full | — | Bypass Email Verification on Add Email Monitoring |
| [INFO-2390009](https://hackerone.com/reports/2390009) | ibb | $405 | 03 | full | CVE-2024-24758 | Proxy-Authorization header is not cleared in cross-domain redirect in undici |
| [INFO-2401648](https://hackerone.com/reports/2401648) | mozilla | - | 04 | full | — | two aws access key and secret key and database username and password exposed |
| [INFO-2404415](https://hackerone.com/reports/2404415) | security | - | 04 | full | — | View any user email using the Team's audit log section |
| [INFO-2412983](https://hackerone.com/reports/2412983) | mozilla | - | 04 | full | — | sentry Auth Token exposed publicly in docker hub image |
| [INFO-2421796](https://hackerone.com/reports/2421796) | security | $2,500 | 03 | full | — | Possible PII Disclosure via Advanced Vetting Process - ██████ |
| [INFO-2451113](https://hackerone.com/reports/2451113) | ibb | $420 | 03 | full | CVE-2024-30260 | Proxy-Authorization header not cleared on cross-origin redirect in undici.request |
| [INFO-2467999](https://hackerone.com/reports/2467999) | mozilla | $1,000 | 04 | full | — | Jira Credential Disclosure within Mozilla Slack |
| [INFO-2524939](https://hackerone.com/reports/2524939) | security | - | 03 | full | — | [Spot Check] - Ability to disclose metadata about Spot Checks (Number of Hackers + Hackers Criteria) via "Spot… |
| [INFO-2534458](https://hackerone.com/reports/2534458) | linkedin | - | 03 | full | — | Can see phone numbers of others by providing mail address |
| [INFO-2599391](https://hackerone.com/reports/2599391) | ibb | $2,600 | 05 | full | CVE-2024-3416 | CVE-2024-3416: MTU of 4096 or greater without fragmentation may cause NGINX worker processes to leak previousl… |
| [INFO-2610467](https://hackerone.com/reports/2610467) | fetlife | - | 03 | full | — | Able to see location coordinates in any event without permission to do so |
| [INFO-2733994](https://hackerone.com/reports/2733994) | portswigger | $200 | 06 | full | — | cgi scripts wordlist entry for windmail.exe has payload that sends arbitrary file read result to third-party |
| [INFO-2737309](https://hackerone.com/reports/2737309) | mozilla | - | 03 | full | — | Information disclosure on password cancel endpoint |
| [INFO-2828263](https://hackerone.com/reports/2828263) | ibb | - | 04 | full | CVE-2024-50378 | Secrets not masked in UI when sensitive variables are set via Airflow cli |
| [INFO-2828271](https://hackerone.com/reports/2828271) | ibb | - | 04 | full | CVE-2024-45784 | Apache Airflow: Sensitive Information Exposure in DAG Run Logs |
| [INFO-2894283](https://hackerone.com/reports/2894283) | ibb | $505 | 04 | full | CVE-2024-11053 | netrc and redirect credential leak |
| [INFO-2915647](https://hackerone.com/reports/2915647) | mozilla | $1,500 | 04 | full | — | Netlify Authentication Token Exposed in Public Mozilla CI Logs |
| [INFO-2937622](https://hackerone.com/reports/2937622) | security | $1,200 | 04 | full | — | Public GitHub repositories for multiple HackerOne managed triage team profiles contain private HackerOne repor… |
| [INFO-3000510](https://hackerone.com/reports/3000510) | security | $25,000 | 02 | full | — | The /reports/:id.json endpoint discloses potentially sensitive user attributes when reporter summary is presen… |
| [INFO-3082917](https://hackerone.com/reports/3082917) | ibb | $4,323 | 03 | full | — | Possible Sensitive Session Information Leak in Active Storage |

Module totals: 01 $19,252.2/13 · 02 $83,580/28 · 03 $47,014/56 · 04 $48,697/41 · 05 $15,468/6 · 06 $67,914/17 (of which in-bucket adjacent $3,364/5 and unclassified merges $64,550/12).
Bucket arithmetic: modules 01–05 ($214,011.2/144) + in-bucket adjacent ($3,364/5) = bucket-340 **$217,375.2/149**, max $25,000 (INFO-3000510); merges $64,550/12, max $50,000 (INFO-1087489) — never folded into the bucket headline.
Asset types in DB (for reference only — register keeps program/bounty/module): URL dominates modules 01–02 (58/72 rows); SOURCE_CODE/WILDCARD grow in 03–05 (mobile + library surfaces). CVE column is DB `cve_ids` verbatim (`—` = `[]`).
