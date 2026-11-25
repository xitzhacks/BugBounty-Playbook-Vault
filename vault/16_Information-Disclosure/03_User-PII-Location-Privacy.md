---
title: "User PII, Location & Privacy — enumerations, counters, and consent toggles"
type: playbook
category: user-pii-location-privacy
cwe: "CWE-359"
source_count: 128
full_bodies_available: 128
corpus: "h1-brain disclosed_reports.db (sha256 8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4) — 362 rows"
list_accessed: "2026-11-07"
note: "Anchors: INFO-3082917 (ibb, $4,323), INFO-125200 (uber, $3,000), INFO-253429 (torproject, $3,000), INFO-434763 (x, $2,940), INFO-472013 (x, $2,940), INFO-968165 (shopify, $2,500). All quotes byte-true to references/archive/INFO-bodies-full-dump.txt."
---

# User PII, Location & Privacy — enumerations, counters, and consent toggles

## 1. Overview

The vault's largest module: 128 rows, **$47,014/56 paid** (max $4,323). No row pays above $4,323 — this module is the corpus's proof that *privacy bugs price low and broadly*, in contrast to modules 02 and 04 where a single credential pays five figures. The paid rows cluster at $500 and below ($250–$1,000) with a thin $2,500–$4,323 ceiling. Programs are diffuse (no program exceeds ~10 rows; `x`, `shopify`, `security`, `brave`, `nextcloud`, `torproject` lead) and the weakness split is the vault's tidiest: 108 `Information Disclosure`, 17 `Privacy Violation`, 3 `Cleartext Storage`. Three mechanisms dominate the paid set: **enumerations** (response-differential counting over an unthrottled identifier space), **counters and caches that carry sessions** (shared caches, header mishandling), and **consent/permission toggles that silently flip** (email verification unsetting "Protect your Tweets", OAuth screens lying about DM access). Seventy-two rows carry no figure — the module's honesty problem: privacy reports are routinely filed informative and the DB records no figure, so the module's true paid rate is understated.

**Case-stock (128 rows / $47,014):**

| Case | Target | Mechanism | Bounty |
|---|---|---|---|
| [INFO-3082917](https://hackerone.com/reports/3082917) | ibb | Possible Sensitive Session Information Leak in Active Storage | $4,323 |
| [INFO-125200](https://hackerone.com/reports/125200) | uber | Lack of rate limiting on get.uber.com leads to enumeration of promotion codes … | $3,000 |
| [INFO-253429](https://hackerone.com/reports/253429) | torproject | Linux TBB SFTP URI allows local IP disclosure | $3,000 |
| [INFO-434763](https://hackerone.com/reports/434763) | x | Incorrect details on OAuth permissions screen allows DMs to be read without pe… | $2,940 |
| [INFO-472013](https://hackerone.com/reports/472013) | x | Changing email address on Twitter for Android unsets "Protect your Tweets" | $2,940 |
| [INFO-968165](https://hackerone.com/reports/968165) | shopify | Disclose customer orders details by shopify chat application. | $2,500 |
| [INFO-2421796](https://hackerone.com/reports/2421796) | security | Possible PII Disclosure via Advanced Vetting Process - ██████ | $2,500 |
| [INFO-1752146](https://hackerone.com/reports/1752146) | ibb | POST following PUT confusion | $2,400 |
| [INFO-882412](https://hackerone.com/reports/882412) | shopify | OrderListInitial leaks order details | $1,500 |
| [INFO-961929](https://hackerone.com/reports/961929) | shopify | Ability to see password protected content by bypassing the password page of sh… | $1,500 |
| [INFO-505424](https://hackerone.com/reports/505424) | x | Twitter ID exposure via error-based side-channel attack | $1,470 |
| [INFO-143935](https://hackerone.com/reports/143935) | x | [sms-be-vip.twitter.com] vulnerable to Jetleak | $1,260 |
| [INFO-421009](https://hackerone.com/reports/421009) | shopify | H1514 Deanonymizing Exchange Marketplace private listings | $1,000 |
| [INFO-975047](https://hackerone.com/reports/975047) | shopify | User sensitive information disclosure | $1,000 |
| [INFO-1021885](https://hackerone.com/reports/1021885) | basecamp | Bypass of image rewriting / tracking blocker via srcset | $1,000 |
| [INFO-1042716](https://hackerone.com/reports/1042716) | elastic | Async search stores authorization headers in clear text | $1,000 |
| [INFO-1392511](https://hackerone.com/reports/1392511) | security | HackerOne Staging uses Production data for testing | $1,000 |
| [INFO-715740](https://hackerone.com/reports/715740) | deptofdefense | [HTA2] Receiving████ access request on @wearehackerone.com email address | $750 |
| [INFO-1080437](https://hackerone.com/reports/1080437) | bumble | Bumble API exposes read status of chat messages | $600 |
| [INFO-142549](https://hackerone.com/reports/142549) | x | Information Disclosure through .DS_Store in ██████████ | $560 |
| [INFO-185862](https://hackerone.com/reports/185862) | x | Twitter for android is exposing user's location to any installed android app | $560 |
| [INFO-491473](https://hackerone.com/reports/491473) | x | Protected tweets exposure through the URL | $560 |
| [INFO-1225164](https://hackerone.com/reports/1225164) | x | Identify the mobile number of a twitter user | $560 |
| [INFO-353310](https://hackerone.com/reports/353310) | security | People who interviewed for HackerOne security analyst position can be enumerat… | $500 |
| [INFO-509574](https://hackerone.com/reports/509574) | security | Invited team member can disclosure slack channels | $500 |
| [INFO-958374](https://hackerone.com/reports/958374) | security | Pentester can obtain information about other pentesters who applied for the sa… | $500 |
| [INFO-968174](https://hackerone.com/reports/968174) | shopify | Disclose STUFF member name and make actions. | $500 |
| [INFO-1298809](https://hackerone.com/reports/1298809) | shopify | Senseitive data Related to Shopify Host -> https://shopify.zendesk.com/ | $500 |
| [INFO-1337624](https://hackerone.com/reports/1337624) | brave | Information disclosure-Referer leak | $500 |
| [INFO-1605962](https://hackerone.com/reports/1605962) | shopify | store internal email disclosed through shopify-data-exporter | $500 |
| [INFO-1626236](https://hackerone.com/reports/1626236) | deptofdefense | Critical sensitive information Disclosure. [HtUS] | $500 |
| [INFO-1551588](https://hackerone.com/reports/1551588) | ibb | CVE-2022-27775: Bad local IPv6 connection reuse | $480 |
| [INFO-2451113](https://hackerone.com/reports/2451113) | ibb | Proxy-Authorization header not cleared on cross-origin redirect in undici.requ… | $420 |
| [INFO-2243710](https://hackerone.com/reports/2243710) | ibb | Cookie headers are not cleared in cross-domain redirect in undici-fetch | $405 |
| [INFO-2390009](https://hackerone.com/reports/2390009) | ibb | Proxy-Authorization header is not cleared in cross-domain redirect in undici | $405 |
| [INFO-1668815](https://hackerone.com/reports/1668815) | brave | Persistent user tracking is possible using window.caches, by avoiding Brave Sh… | $400 |
| [INFO-1173436](https://hackerone.com/reports/1173436) | nextcloud | Default settings leak federated cloud id to lookup server of all users | $350 |
| [INFO-228399](https://hackerone.com/reports/228399) | discourse | Any authenticated user can download full list of users, including email | $256 |
| [INFO-258578](https://hackerone.com/reports/258578) | brave | application/x-brave-tab should not be readable. | $250 |
| [INFO-316810](https://hackerone.com/reports/316810) | security | Can read features from any user | $250 |
| [INFO-1161401](https://hackerone.com/reports/1161401) | nextcloud | Notification implicit PendingIntent in com.nextcloud.client allows to access c… | $250 |
| [INFO-300181](https://hackerone.com/reports/300181) | brave | Torrent Viewer extension web service available on all interfaces | $200 |
| [INFO-1072893](https://hackerone.com/reports/1072893) | logitech | Sensitive information disclosure to shared access user via streamlabs platform… | $200 |
| [INFO-2123957](https://hackerone.com/reports/2123957) | torproject | 'Request English versions of web pages for enhanced privacy' keeps previous (g… | $200 |
| [INFO-162822](https://hackerone.com/reports/162822) | instacart | Fetch private list metadata and any user's personal name | $150 |
| [INFO-178506](https://hackerone.com/reports/178506) | instacart | Access private list metadata | $100 |
| [INFO-257942](https://hackerone.com/reports/257942) | torproject | languagechange event fires simultaneously on all tabs | $100 |
| [INFO-258585](https://hackerone.com/reports/258585) | brave | OS username disclosure | $100 |
| [INFO-1215251](https://hackerone.com/reports/1215251) | nextcloud | Bypass of privacy filter / tracking pixel blocker | $100 |
| [INFO-1520685](https://hackerone.com/reports/1520685) | nextcloud | Moderator can enable cam/mic remotely if cam/mic-permission was disabled while… | $100 |
| [INFO-2215434](https://hackerone.com/reports/2215434) | security | Hacker email disclosed on submission at hackerone hactivity | $100 |
| [INFO-242727](https://hackerone.com/reports/242727) | nextcloud | Android content provider exposes password-protected share password hashes | $75 |
| [INFO-57918](https://hackerone.com/reports/57918) | whisper | Insecure Local Data Storage : Application stores data using a binary sqlite da… | $50 |
| [INFO-255978](https://hackerone.com/reports/255978) | unikrn | Non-Cloudflare IPs allowed to access origin servers | $50 |
| [INFO-428010](https://hackerone.com/reports/428010) | nextcloud | Talk / spreed: Disclosure of Room names and participants for password protecte… | $50 |
| [INFO-495525](https://hackerone.com/reports/495525) | iandunn-projects | XSSI: Quick Navigation Interface - leak of private page/post titles | $50 |
| [INFO-117902](https://hackerone.com/reports/117902) | vkcom | Дорк | - |
| [INFO-135756](https://hackerone.com/reports/135756) | shopify | View all deleted comments and rating of any app . | - |
| [INFO-136850](https://hackerone.com/reports/136850) | vimeo | Images and Subtitles Leakage from private videos | - |
| [INFO-145150](https://hackerone.com/reports/145150) | uber | Bulk UUID enumeration via invite codes | - |
| [INFO-155618](https://hackerone.com/reports/155618) | vimeo | Watch any Password Video without password | - |
| [INFO-163464](https://hackerone.com/reports/163464) | legalrobot | User Information sent to client through websockets | - |
| [INFO-174721](https://hackerone.com/reports/174721) | x | View liked twits of private account via publish.twitter.com | - |
| [INFO-174882](https://hackerone.com/reports/174882) | yelp | Requesting Show CheckIn Alert for Non Friend User | - |
| [INFO-193314](https://hackerone.com/reports/193314) | zendesk | SMTP user enumeration via mail.zendesk.com | - |
| [INFO-194721](https://hackerone.com/reports/194721) | yelp | Verification of email addresses possible through https://www.yelp.com/signup/f… | - |
| [INFO-196655](https://hackerone.com/reports/196655) | security | Disclose any user's private email through API | - |
| [INFO-222870](https://hackerone.com/reports/222870) | phabricator | IRC-Bot exposes information | - |
| [INFO-252580](https://hackerone.com/reports/252580) | torproject | Scrollbar Width permits detecting browser platform | - |
| [INFO-256647](https://hackerone.com/reports/256647) | torproject | Simple CSS line-height identifies platform | - |
| [INFO-271176](https://hackerone.com/reports/271176) | lyst | Bypassing one-time checkout router page (revealing payment information) | - |
| [INFO-282748](https://hackerone.com/reports/282748) | torproject | Detecting Tor Browser UI Language | - |
| [INFO-310105](https://hackerone.com/reports/310105) | automattic | Disclosure of 152 cookie names via crafted input | - |
| [INFO-318099](https://hackerone.com/reports/318099) | grab | Registration enabled on ███grab.com | - |
| [INFO-329957](https://hackerone.com/reports/329957) | x | Tracking of users on third-party websites using the Twitter cookie, due to a f… | - |
| [INFO-358007](https://hackerone.com/reports/358007) | bumble | Compromising the user ID | - |
| [INFO-361951](https://hackerone.com/reports/361951) | liberapay | Exploiting JSONP callback on /username/charts.json endpoint leads to informati… | - |
| [INFO-370777](https://hackerone.com/reports/370777) | udemy | [affiliates.udemy.com] Wordpress user admin information discloure | - |
| [INFO-374907](https://hackerone.com/reports/374907) | gsa_bbp | Root user disclosure in data.gov domain though x-amz-meta-s3cmd-attrs header | - |
| [INFO-378122](https://hackerone.com/reports/378122) | security | HackerOne customer submitted sensitive link to VirusTotal, exposing confidenti… | - |
| [INFO-386596](https://hackerone.com/reports/386596) | semmle | Email Not Completely Deleted after Deleting an account | - |
| [INFO-402410](https://hackerone.com/reports/402410) | bumble | Расшифровка всех типов шифрованных ID | - |
| [INFO-411822](https://hackerone.com/reports/411822) | chaturbate | Password protected rooms total number of viewers disclosure to unauthorized me… | - |
| [INFO-423506](https://hackerone.com/reports/423506) | shopify | H1514 Extract information about other sites (new sites) through Affiliate/Refe… | - |
| [INFO-430854](https://hackerone.com/reports/430854) | kaspersky | Kaspersky Password Manager allows websites to access user's address data | - |
| [INFO-477222](https://hackerone.com/reports/477222) | gitlab | Last build status and coverage leaked to unauthorized users | - |
| [INFO-488643](https://hackerone.com/reports/488643) | security | Disclosure of h1 challenges name through the calendar | - |
| [INFO-495497](https://hackerone.com/reports/495497) | gitlab | Know whether private project name exists or not within a group using link comm… | - |
| [INFO-508490](https://hackerone.com/reports/508490) | nextcloud | Nextcloud domain and name of every user leaked to lookup server | - |
| [INFO-540301](https://hackerone.com/reports/540301) | automattic | Wordpress VIP leaks email of the test a/c | - |
| [INFO-541020](https://hackerone.com/reports/541020) | valve | GetGlobalAchievementPercentagesForApp is missing the same release checks as Ge… | - |
| [INFO-604945](https://hackerone.com/reports/604945) | brave | Tor IP leak caused by the PDF Viewer extension in certain situations | - |
| [INFO-605608](https://hackerone.com/reports/605608) | gitlab | [information disclosure] Validate existence of a private project. | - |
| [INFO-636560](https://hackerone.com/reports/636560) | gitlab | Project Milestones Disclosed Via Groups When the Victim disabled milestones ac… | - |
| [INFO-666722](https://hackerone.com/reports/666722) | omise | Email enumeration at SignUp page | - |
| [INFO-723175](https://hackerone.com/reports/723175) | imgur | De-anonymization Attack: Cross Site Information Leakage | - |
| [INFO-724944](https://hackerone.com/reports/724944) | security | latest_activity_id and latest_activity_at may disclose information about inter… | - |
| [INFO-753725](https://hackerone.com/reports/753725) | nordsecurity | Disclosure of User Information | - |
| [INFO-813421](https://hackerone.com/reports/813421) | nordsecurity | Account deletion requests not entirely honoured. Misinformation even after see… | - |
| [INFO-874778](https://hackerone.com/reports/874778) | curl | CVE-2020-8169: Partial password leak over DNS on HTTP redirect | - |
| [INFO-948876](https://hackerone.com/reports/948876) | curl | CVE-2020-8231: Connect-only connections can use the wrong connection | - |
| [INFO-952771](https://hackerone.com/reports/952771) | kubernetes | CVE-2019-11250 remains in effect. | - |
| [INFO-961757](https://hackerone.com/reports/961757) | x | Twitter Media Studio Source Information Disclosure With Analyst Role | - |
| [INFO-1018336](https://hackerone.com/reports/1018336) | shopify | Customer's full name disclosure via Shopify Chat (by email lookup) | - |
| [INFO-1023572](https://hackerone.com/reports/1023572) | acronis | [acronis.secure.force.com] - Insecure Salesforce default/custom object permiss… | - |
| [INFO-1069335](https://hackerone.com/reports/1069335) | h1-ctf | How The Hackers Saved Christmas | - |
| [INFO-1070081](https://hackerone.com/reports/1070081) | automattic | information disclosure lead to disclose users private notes | - |
| [INFO-1077022](https://hackerone.com/reports/1077022) | brave | Brave Browser Tor Window leaks user's real IP to the external DNS server | - |
| [INFO-1083922](https://hackerone.com/reports/1083922) | shopify | [h1-2102] Information disclosure - ShopifyPlus add user displays existing Shop… | - |
| [INFO-1172852](https://hackerone.com/reports/1172852) | wordpress | PII of users can be downloaded from export pages | - |
| [INFO-1234406](https://hackerone.com/reports/1234406) | bumble | Exfiltrating a victim's exact location (to within 5m) | - |
| [INFO-1245741](https://hackerone.com/reports/1245741) | zenly | Friend Request Flow Exposes User Data | - |
| [INFO-1331728](https://hackerone.com/reports/1331728) | nextcloud | Cards in Deck are readable by any user | - |
| [INFO-1423704](https://hackerone.com/reports/1423704) | fetlife | Able to detect if a user is FetLife supporter although this user hides their s… | - |
| [INFO-1424291](https://hackerone.com/reports/1424291) | fetlife | Able to access private picture/video/writing when requesting for their JSON re… | - |
| [INFO-1590237](https://hackerone.com/reports/1590237) | automattic | Unauthenticated Private Messages DIsclosure via wordpress Rest API | - |
| [INFO-1782467](https://hackerone.com/reports/1782467) | indrive | Disclosure of users' ip address whenever they view my fright offer on image pr… | - |
| [INFO-1785079](https://hackerone.com/reports/1785079) | indrive | # Drivers can access the customers phone number, current location without gett… | - |
| [INFO-1886143](https://hackerone.com/reports/1886143) | security | information disclosure of another company bug on video. | - |
| [INFO-2032716](https://hackerone.com/reports/2032716) | security | An attacker can can view any hacker email via /SaveCollaboratorsMutation opera… | - |
| [INFO-2045722](https://hackerone.com/reports/2045722) | security | inviting collaborator using email disclose the hackerone account related to th… | - |
| [INFO-2063636](https://hackerone.com/reports/2063636) | x | Twitter Subscriptions Information Disclosure | - |
| [INFO-2134874](https://hackerone.com/reports/2134874) | security | Hackers two email disclosed on submission at hackerone hactivity | - |
| [INFO-2382120](https://hackerone.com/reports/2382120) | security | Creation of bounties through Customer API leads to private email disclosure | - |
| [INFO-2524939](https://hackerone.com/reports/2524939) | security | [Spot Check] - Ability to disclose metadata about Spot Checks (Number of Hacke… | - |
| [INFO-2534458](https://hackerone.com/reports/2534458) | linkedin | Can see phone numbers of others by providing mail address | - |
| [INFO-2610467](https://hackerone.com/reports/2610467) | fetlife | Able to see location coordinates in any event without permission to do so | - |
| [INFO-2737309](https://hackerone.com/reports/2737309) | mozilla | Information disclosure on password cancel endpoint | - |

## 2. Enumerations that mint identities: the invite-code census

INFO-125200 (**uber, $3,000**) is the module's richest enumeration — 5-character lowercase invite codes (36⁵ ≈ 60M) where two response strings distinguish "no account" from "Sign up now to claim your free gift from [First Name]":

> Invite codes are 5 alphanumeric (lower case) characters. This means there are 36 (26 + 10) possible options for each space in the invite code. In total this means there are 36^5 or 60,466,176 possible invite codes. Through enumerating through all possible invite codes, one can find the total number of Uber accounts and the first name associated with each of the uber accounts.

> When loading ```https://get.uber.com/invite/[Invite Code]```, one will see one of two possible messages. If you see only ```Create your account and get moving in minutes.``` then there is no account associated with that invite code. If you see ```Sign up now to claim your free gift from [First Name] ($15 off first ride)*.```, then there is an account associated with that invite code.

The reporter even supplied the `isAccount(code)` scanner and the sampling argument ("one can simply test a subset of that and extrapolate"). Its unpaid sibling INFO-145150 (uber, bulk UUID enumeration via invite codes) shows the same lane at $0-unpriced. INFO-505424 (**x, $1,470**) is the de-anonymization twin — a 403-vs-200 differential on `client-applications.json` detectable cross-site via `onload`/`onerror`, identifying a visiting user by their Twitter ID:

> Recently I discovered a privacy-related vulnerability in Twitter. An attacker exploiting this vulnerability can identify a user when they visit a malicious website.

> If the USER_ID is different from the ID of a currently logged in user the error 403 will be returned with the following JSON output

The pricing lesson: **a differential that yields a name-to-identifier binding pays ~$1,500–$3,000**; the same differential yielding only a count (INFO-410015 in module 02) paid $3,000 because it classified *programs*.

## 3. Sessions in caches and headers: the $4,323 ceiling

INFO-3082917 (**ibb, $4,323**) — the module max — is four lines long and pure cache poisoning:

> Active Storage, when serving files (blobs), incorrectly sends the Set-Cookie header containing the user's session cookie along with a Cache-Control: public header.

> Some certain caching proxies may cache this response, including the Set-Cookie header.

> This allows unrelated users accessing the cached content to obtain the original user's session cookie.

INFO-1042716 (**elastic, $1,000**) is the storage twin: async-search retains *authorization headers in clear text* in `.async-search`, retrievable by other superusers, with the lateral-movement note that LDAP/AD credential reuse makes it an impersonation path ("if you want to get the password of someone else on your cluster, then it's probably already there"). The undici trio (INFO-2243710 $405, INFO-2390009 $405, INFO-2451113 $420) prices the redirect-header variant — `Cookie` and `Proxy-Authorization` not cleared cross-domain — at the $400 floor. The header-caching family is where this module meets the Cache-Poisoning vault: the poison here is not a script but a *session*, and the cache is a *shared proxy*, not the victim's browser.

## 4. Consent toggles and lying screens: privacy by checkbox

INFO-472013 (**x, $2,940**) is a state-machine bug, not a data leak: verifying a new email address on Twitter for Android silently unsets "Protect your Tweets":

> Verifying a new email address on a Twitter account in the Android app causes the "Protect your Tweets" option to be unset, resulting in the user's tweets being made publicly visible.

> This can lead to a user's private tweets being exposed to the public until they realize this happened. An attacker does not need to be involved as they would need to have access to the user's account to

INFO-434763 (**x, $2,940**) prices the *lie*: an OAuth screen stating the app "Will not be able to: Access your direct messages" while the app can, in fact, read DMs:

> The OAuth screen can be tricked into saying that an app cannot read Direct Messages. Despite that, DMs can be read.

> This is false. The apps *can* read DMs.

> A user may not want a 3rd party app to have access to their DMs.

Both paid identically ($2,940) — the corpus's statement that *a consent UI that misstates its permissions is priced like the data it exposes*. INFO-185862 ($560, location exposed to any installed app), INFO-491473 ($560, protected tweets via URL), and INFO-1234406 ($0, exact location to within 5m on Bumble) are the same shelf at mobile prices.

## 5. Order lookups and access controls: PII behind guessing

INFO-968165 (**shopify, $2,500**) strips the email check down to its domain:

> This bug leads to disclose any store orders details ( including sensitive informations), through shopify chat app. the chat app can retrieve the orders details for unauthorized user.

> Remove the first part of the email (keep only @hotmail/gmail/yahoo...).

> In normal situation the orders IDs start form #1000, and in the verification required the email and ID, So the attacker can brut force on the ID and retrive the order information of that ID with the same email ISP because we removed the first email part.

INFO-253429 (**torproject, $3,000**) is the proxy-bypass twin — an `sftp://` URI makes the *local* SSH client connect outside Tor, leaking the user's IP ("After ~1 minute check http://104.131.180.179/ip,txt for your IP address") and, as the body notes, "the client can also be directed to local resources as well." INFO-2421796 (**security, $2,500**) closes the section on the H1 side: a vetting-terms CSV ("Name of Finder,Username,Advanced Finder Vetting,Address (optional),Finder's Country,Date signed") downloadable by any logged-in user.

## 6. What pays, what doesn't

- **Pays at the ceiling**: session-carrying caches ($4,323), enumerations that bind names to accounts ($3,000), proxy bypasses that leak IPs ($3,000), and consent violations priced at the data they expose ($2,940 ×2).
- **Pays, floor**: platform-fingerprinting singletons ($100–$250 — scrollbar width, CSS line-height, OS username, tab-synchrony), tracker-pixel and srcset leaks ($100), and header-clearing omissions (~$405). The fingerprint shelf is *priced*, which is why the playbook treats "detects Tor UI language" as a reportable signal rather than dismissing it.
- **Doesn't pay (here)**: 72 unpriced rows including serious claims (exact-location exfiltration, private-message REST disclosure, password-video bypass). The pattern matches module 02: broad capability titles without a shown value correlate with no figure. Show the value — a name, a count, a coordinate, a response blob.

## 7. Cross-references

- Modules 01–02 (`01_GraphQL-API-Objects-Exposure.md`, `02_HackerOne-Reports-Bounty-Privacy.md`) supply the *mechanisms* (GraphQL fields, JSON serialization, search oracles) for half this module's PII classes — INFO-415622's emails came through a GraphQL-adjacent endpoint, INFO-972355's through a GraphQL user query.
- Module 04 (`04_File-Path-Errors-Secrets-Leaks.md`) — INFO-1575014's Stripe SDK path-normalization row is filed here by mechanism (PII via `sessions/.`) but taught there; cross-cite when hunting SDK path handling.
- Companion vault `../Authentication-Session/` — INFO-3082917's session-cookie cache and INFO-1042716's stored auth headers are session-material disclosures; this module prices the *privacy* frame, that vault the *token* frame.
