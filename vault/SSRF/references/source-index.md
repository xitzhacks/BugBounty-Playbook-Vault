---
title: "SSRF Vault Source Index — h1.security.nathan.sx archive"
type: reference
candidates: 82
retrievable: 58
full_bodies_read: 45
http404: 24
site: "https://h1.security.nathan.sx/"
archive_frozen: "12th September, 2017 (stated on the site's own last-updated line)"
accessed: "2026-10-24"
---

# SSRF Vault Source Index

## 1. Provenance

- Archive: [h1.security.nathan.sx](https://h1.security.nathan.sx/) — a static
  HackerOne disclosed-report mirror. Its own header states
  **"4,419 Bug Reports - $2,030,173 Paid Out - Last Updated: 12th September, 2017"**.
  `robots.txt` does not exist on the host (404), consistent with the standing
  practice used for the XSS and IDOR vaults of this repository.
- Site structure: one master index table (site root, 1.1 MB) plus per-program
  pages (`uber.html`, `slack.html`, ...) — **no vulnerability-type aggregation
  pages exist**. Discovery therefore ran over titles only, in two nets (below).
- Report bodies: fetched per-report from HackerOne's public unauthenticated
  JSON endpoint (`https://hackerone.com/reports/<id>.json`), 1.2 s request
  spacing, disk-cached under `/tmp/opencode/ssrf/cache/` (re-fetchable if the
  cache is cleared).
- Bounty rule for the tables below: the report-JSON amount where present;
  otherwise the amount stated in the archive's own bounty table, marked
  "(archive-stated)". Overlapping values agree in every observed case.

## 2. Discovery, honestly counted

- Net 1 (core title patterns): `ssrf` / `server-side request forgery`,
  `internal`, wrapper scheme names (`gopher|dict|phar|expect`), metadata terms
  (`169.254 | instance metadata | ec2`), `pingback`, `port scan`, callback
  terms, URL-validation terms, `localhost`, `intranet` → **73 candidates**
- Net 2 (media / URL-import wording): `ffmpeg | libav | m3u8 | hls | lavf |
  video-to-gif | conversion`, URL-side `upload/import/fetch/download/convert/
  validate/preview` → **9 new**
- Total title-matched candidates: **82** of the 4,419 rows.
- The instruction-side figure of "239 SSRF reports in this repo" was not
  reproducible: the archive has no SSRF-tagged page and no body search;
  82 is what the titles support under both nets. If the 239 figure came from
  another list, that list is not this archive's structure.

## 3. Fetch dispositions (the corpus shape of record)

| Group | n | Meaning |
| --- | --- | --- |
| Body-confirmed SSRF | 26 | body read in full; class assigned per body; routed to category files |
| Body-confirmed SSRF-adjacent (internal-service exposure) | 3 | body read; not SSRF primitives; kept for the SSRF-objective frame |
| Metadata-only, SSRF-titled/labelled | 7 | body withheld on unauthenticated retrieval; title/label/bounty only |
| Metadata-only, internal-service exposure | 3 | body withheld; exposure rows |
| Metadata-only, adjacent client-library row | 1 | libcurl URL request injection — era advisory row |
| Body-confirmed NOT SSRF (excluded) | 16 | XSS / authz / DoS / RCE / library-bug classes; per-body reasons in the table |
| Metadata-only NOT verifiable (excluded) | 2 | subdomain takeover + internal-CMS titles |
| HTTP 404 at origin | 24 | recorded titles/bounties; bodies unrecoverable |

Bounty totals (excluding exclusions and 404 rows): confirmed-26 **$9,144**
(JSON-verified $514; rest archive-stated) · adjacent-3 **$4,500** ·
metadata-SSRF-7 **$3,350** → SSRF-relevant disclosed total **$16,994**.
An additional **$10,819** (archive-stated) sits on the 24 now-404 rows —
recorded, not claimable without the bodies.

## 4. Full disposition table

| Case | Title (original) | Team (archive) | Weakness (recorded) | Bounty shown | Disposition and evidence |
| --- | --- | --- | --- | --- | --- |
| [SRF-1409](https://hackerone.com/reports/1409) | Proxy discloses internal web servers | [factlink](https://h1.security.nathan.sx/factlink.html) | Information Disclosure | – | full body read — confirmed SSRF (port-scan → Port-Scan-and-Internal-Mapping.md) |
| [SRF-2639](https://hackerone.com/reports/2639) | Stored XSS on this link https://sehacure.slack.com/help/requests/ | [slack](https://h1.security.nathan.sx/slack.html) | Cross-site Scripting (XSS) - Generic | – | full body read — excluded, not SSRF: Slack stored XSS on help/requests form — XSS class |
| [SRF-14127](https://hackerone.com/reports/14127) | SSRF on https://whitehataudit.slack.com/account/photo | [slack](https://h1.security.nathan.sx/slack.html) | Command Injection - Generic | $300 | full body read — confirmed SSRF (bypass-scheme → Validation-Bypass-and-Scheme-Abuse.md) |
| [SRF-16571](https://hackerone.com/reports/16571) | SSRF (Portscan) via Register Function (Custom Server) | [relateiq](https://h1.security.nathan.sx/relateiq.html) | Violation of Secure Design Principles | $250 | full body read — confirmed SSRF (port-scan → Port-Scan-and-Internal-Mapping.md) |
| [SRF-46072](https://hackerone.com/reports/46072) | Vulnerability with the way \ escaped characters in &lt;http://danlec.com&gt; style links are rendered | [security](https://h1.security.nathan.sx/security.html) | Cross-site Scripting (XSS) - Generic | $5,000 | full body read — excluded, not SSRF: H1 markdown link rendering ([danlec]) — XSS class |
| [SRF-49474](https://hackerone.com/reports/49474) | Cross site Port Scanning bug in twitter developers console | [twitter](https://h1.security.nathan.sx/twitter.html) | Cryptographic Issues - Generic | – | full body read — confirmed SSRF (port-scan → Port-Scan-and-Internal-Mapping.md) |
| [SRF-50537](https://hackerone.com/reports/50537) | Server Side Request Forgery in macro creation | [phabricator](https://h1.security.nathan.sx/phabricator.html) | Information Disclosure | – | full body read — confirmed SSRF (port-scan → Port-Scan-and-Internal-Mapping.md) |
| [SRF-53088](https://hackerone.com/reports/53088) | SSRF vulnerability (access to metadata server on EC2 and OpenStack) | [phabricator](https://h1.security.nathan.sx/phabricator.html) | Information Disclosure | $300 | full body read — confirmed SSRF (cloud-meta → Cloud-Instance-Metadata.md) |
| [SRF-55716](https://hackerone.com/reports/55716) | Force 500 Internal Server Error on any shop (for one user) | [shopify](https://h1.security.nathan.sx/shopify.html) | Uncontrolled Resource Consumption | $500 | full body read — excluded, not SSRF: per-user persistent 500-error DoS (CSRF-delivered) — no outbound fetch |
| [SRF-61312](https://hackerone.com/reports/61312) | Bypass of the SSRF protection (Slack commands, Phabricator integration) | [slack](https://h1.security.nathan.sx/slack.html) | - | $100 | full body read — confirmed SSRF (bypass-scheme → Validation-Bypass-and-Scheme-Abuse.md) |
| [SRF-67377](https://hackerone.com/reports/67377) | SSRF via 'Add Image from URL' feature | [shopify](https://h1.security.nathan.sx/shopify.html) | Violation of Secure Design Principles | $500 | full body read — confirmed SSRF (port-scan → Port-Scan-and-Internal-Mapping.md) |
| [SRF-67389](https://hackerone.com/reports/67389) | SSRF via 'Insert Image' feature of Products/Collections/Frontpage | [shopify](https://h1.security.nathan.sx/shopify.html) | Violation of Secure Design Principles | $500 | full body read — confirmed SSRF (port-scan → Port-Scan-and-Internal-Mapping.md) |
| [SRF-73237](https://hackerone.com/reports/73237) | Buffer Over flow when parsing tar/zip/phar in phar_set_inode | [php](https://h1.security.nathan.sx/php.html) | - | $1,000 | full body read — excluded, not SSRF: PHP phar buffer overflow — library advisory, not a web-target SSRF |
| [SRF-73238](https://hackerone.com/reports/73238) | Buffer Over-read in unserialize when parsing Phar | [php](https://h1.security.nathan.sx/php.html) | - | $1,000 | full body read — excluded, not SSRF: PHP phar buffer over-read — library advisory, not a web-target SSRF |
| [SRF-73242](https://hackerone.com/reports/73242) | libcurl: URL request injection | [internet](https://h1.security.nathan.sx/internet.html) | - | $3,000 | metadata only — adjacent client-library request-injection row |
| [SRF-73247](https://hackerone.com/reports/73247) | php_stream_url_wrap_http_ex() type-confusion vulnerability | [php](https://h1.security.nathan.sx/php.html) | - | $500 | full body read — excluded, not SSRF: php_stream_url_wrap_http_ex type-confusion — library advisory (URL-fetch code path), adjacent but not SSRF |
| [SRF-73567](https://hackerone.com/reports/73567) | Attention! Remote Code Execution at http://wpt.ec2.shopify.com/ | [shopify](https://h1.security.nathan.sx/shopify.html) | Command Injection - Generic | $3,000 | full body read — SSRF-adjacent internal-service exposure (Internal-Service-Exposure.md) |
| [SRF-77817](https://hackerone.com/reports/77817) | SSRF/XSPA в форме загрузки видео по URL | [ok](https://h1.security.nathan.sx/ok.html) | Uncontrolled Resource Consumption | $500 | metadata only (body withheld on unauthenticated retrieval) — SSRF class per title/label |
| [SRF-81083](https://hackerone.com/reports/81083) | Internal bounty and swag details disclosed as part of JSON response | [security](https://h1.security.nathan.sx/security.html) | Information Disclosure | $500 | full body read — excluded, not SSRF: H1 program-page JSON shows bounty/swag flags — info disclosure, no SSRF |
| [SRF-91816](https://hackerone.com/reports/91816) | Server Side Request Forgery In Video to GIF Functionality | [imgur](https://h1.security.nathan.sx/imgur.html) | Cross-Site Request Forgery (CSRF) | $1,600 | full body read — confirmed SSRF (bypass-scheme → Validation-Bypass-and-Scheme-Abuse.md) |
| [SRF-100926](https://hackerone.com/reports/100926) | Access to internal CMS containing private Data | [yelp](https://h1.security.nathan.sx/yelp.html) | Improper Authentication - Generic | $1,500 | full body read — excluded, not SSRF: Yelp internal CMS access — body withheld; title is authz/exposure, not demonstrated SSRF |
| [SRF-107336](https://hackerone.com/reports/107336) | Team Member(s) associated with a  Group have Read-only permission (Post internal comments) can post comment to all  | [security](https://h1.security.nathan.sx/security.html) | Privilege Escalation | $500 | full body read — excluded, not SSRF: H1 read-only member can post comments (is_internal=, comma bug) — authz, no SSRF |
| [SRF-108113](https://hackerone.com/reports/108113) | Bypassing callback_url validation on Digits | [twitter](https://h1.security.nathan.sx/twitter.html) | Open Redirect | $2,520 | full body read — excluded, not SSRF: Digits callback_url validation bypass → OAuth ATO — open-redirect class |
| [SRF-110801](https://hackerone.com/reports/110801) | Internal GET SSRF via CSRF with Press This scan feature | [automattic](https://h1.security.nathan.sx/automattic.html) | Cross-Site Request Forgery (CSRF) | $250 | full body read — confirmed SSRF (port-scan → Port-Scan-and-Internal-Mapping.md) |
| [SRF-112156](https://hackerone.com/reports/112156) | SSRF in the Connector Designer (REST and Elastic Search) | [bime](https://h1.security.nathan.sx/bime.html) | Privilege Escalation | $1,000 | metadata only (body withheld on unauthenticated retrieval) — SSRF class per title/label |
| [SRF-114134](https://hackerone.com/reports/114134) | Subdomain takeover in http://support.scan.me pointing to Zendesk (a Snapchat acquisition) | [snapchat](https://h1.security.nathan.sx/snapchat.html) | Cross-site Scripting (XSS) - Generic | $1,000 | full body read — excluded, not SSRF: Scan.me subdomain takeover (Zendesk) — takeover class |
| [SRF-115748](https://hackerone.com/reports/115748) | SSRF in https://imgur.com/vidgif/url | [imgur](https://h1.security.nathan.sx/imgur.html) | Uncontrolled Resource Consumption | $2,000 | full body read — confirmed SSRF (bypass-scheme → Validation-Bypass-and-Scheme-Abuse.md) |
| [SRF-115857](https://hackerone.com/reports/115857) | SSRF and local file read in video to gif converter | [imgur](https://h1.security.nathan.sx/imgur.html) | - | $800 | full body read — confirmed SSRF (media → Media-Processing-SSRF.md) |
| [SRF-115978](https://hackerone.com/reports/115978) | SSRF / Local file enumeration / DoS due to improper handling of certain file formats by ffmpeg | [imgur](https://h1.security.nathan.sx/imgur.html) | Command Injection - Generic | $1,000 | full body read — confirmed SSRF (media → Media-Processing-SSRF.md) |
| [SRF-119221](https://hackerone.com/reports/119221) | User with Read-Only permissions can edit the Internal comment Activities on Bug Reports After Revoke the team acces | [security](https://h1.security.nathan.sx/security.html) | Privilege Escalation | $500 | full body read — excluded, not SSRF: H1 revoked member edits internal comments — authz, no SSRF |
| [SRF-120219](https://hackerone.com/reports/120219) | SSRF issue | [bime](https://h1.security.nathan.sx/bime.html) | Command Injection - Generic | $250 | metadata only (body withheld on unauthenticated retrieval) — SSRF class per title/label |
| [SRF-124097](https://hackerone.com/reports/124097) | Wordpress  Pingback  DDoS Attacks in domain:  veris.in | [veris](https://h1.security.nathan.sx/veris.html) | Uncontrolled Resource Consumption | – | full body read — confirmed SSRF (blind-weapon → Blind-SSRF-and-Callback.md) |
| [SRF-128685](https://hackerone.com/reports/128685) | SSRF on testing endpoint | [apitest](https://h1.security.nathan.sx/apitest.html) | Privilege Escalation | – | full body read — confirmed SSRF (cloud-meta → Cloud-Instance-Metadata.md) |
| [SRF-134305](https://hackerone.com/reports/134305) | Private snippets in public / internal projects leaked though GitLab API | [gitlab](https://h1.security.nathan.sx/gitlab.html) | Information Disclosure | – | full body read — excluded, not SSRF: GitLab private-snippets API leak — authz issue |
| [SRF-137404](https://hackerone.com/reports/137404) | List of a ton of internal twitter servers available on GitHub | [twitter](https://h1.security.nathan.sx/twitter.html) | Information Disclosure | – | full body read — excluded, not SSRF: internal host inventory leaked to public GitHub — exposure/leak, no SSRF |
| [SRF-145524](https://hackerone.com/reports/145524) | Server side request forgery (SSRF) on nextcloud implementation. | [nextcloud](https://h1.security.nathan.sx/nextcloud.html) | - | – | full body read — confirmed SSRF (port-scan → Port-Scan-and-Internal-Mapping.md) |
| [SRF-154369](https://hackerone.com/reports/154369) | Unauthorized access to Zookeeper on http://locutus-zk3.ec2.shopify.com:2181 | [shopify](https://h1.security.nathan.sx/shopify.html) | Improper Authentication - Generic | $1,000 | full body read — SSRF-adjacent internal-service exposure (Internal-Service-Exposure.md) |
| [SRF-157986](https://hackerone.com/reports/157986) | Internal server error 500 at log.veris.in | [veris](https://h1.security.nathan.sx/veris.html) | Information Disclosure | – | full body read — excluded, not SSRF: Sentry error-page 500 + form DoS — no outbound fetch |
| [SRF-158016](https://hackerone.com/reports/158016) | Server side request forgery on image upload for lists | [instacart](https://h1.security.nathan.sx/instacart.html) | Code Injection | $50 | full body read — confirmed SSRF (port-scan → Port-Scan-and-Internal-Mapping.md) |
| [SRF-158118](https://hackerone.com/reports/158118) | Access to Splunk at https://apt.ec2.shopify.com:8089 | [shopify](https://h1.security.nathan.sx/shopify.html) | - | $500 | full body read — SSRF-adjacent internal-service exposure (Internal-Service-Exposure.md) |
| [SRF-159536](https://hackerone.com/reports/159536) | Open CouchDB on experiments.ec2.shopify.com:5984 | [shopify](https://h1.security.nathan.sx/shopify.html) | - | $500 | metadata only — internal-service exposure title (Internal-Service-Exposure.md) |
| [SRF-165048](https://hackerone.com/reports/165048) | Access to Splunk via shard3-db2.ec2.shopify.com endpoint | [shopify](https://h1.security.nathan.sx/shopify.html) | Improper Authentication - Generic | $500 | metadata only — internal-service exposure title (Internal-Service-Exposure.md) |
| [SRF-178184](https://hackerone.com/reports/178184) | SSRF in https://cards-dev.twitter.com/validator | [twitter](https://h1.security.nathan.sx/twitter.html) | Server-Side Request Forgery (SSRF) | $280 | full body read — confirmed SSRF (port-scan → Port-Scan-and-Internal-Mapping.md) |
| [SRF-180527](https://hackerone.com/reports/180527) | SSRF (open) - via GET request | [vkcom](https://h1.security.nathan.sx/vkcom.html) | Server-Side Request Forgery (SSRF) | $300 | metadata only (body withheld on unauthenticated retrieval) — SSRF class per title/label |
| [SRF-182557](https://hackerone.com/reports/182557) | links the user may download can be a malicious files | [brave](https://h1.security.nathan.sx/brave.html) | Code Injection | – | full body read — excluded, not SSRF: Brave download extension bug — extension class, no SSRF |
| [SRF-186230](https://hackerone.com/reports/186230) | Internal attachments can be exported via "Export as .zip" feature | [security](https://h1.security.nathan.sx/security.html) | Information Disclosure | $12,500 | full body read — excluded, not SSRF: H1 "Export as .zip" keeps removed attachment — retention issue, no SSRF |
| [SRF-189648](https://hackerone.com/reports/189648) | Server Side Request Forgery (SSRF) vulnerability in a DoD website | [deptofdefense](https://h1.security.nathan.sx/deptofdefense.html) | Server-Side Request Forgery (SSRF) | – | metadata only (body withheld on unauthenticated retrieval) — SSRF class per title/label |
| [SRF-197365](https://hackerone.com/reports/197365) | SSRF через Share-ботов | [vkcom](https://h1.security.nathan.sx/vkcom.html) | Server-Side Request Forgery (SSRF) | $300 | metadata only (body withheld on unauthenticated retrieval) — SSRF class per title/label |
| [SRF-204513](https://hackerone.com/reports/204513) | Infrastructure - Photon - SSRF | [wordpress](https://h1.security.nathan.sx/wordpress.html) | Server-Side Request Forgery (SSRF) | $350 | full body read — confirmed SSRF (bypass-scheme → Validation-Bypass-and-Scheme-Abuse.md) |
| [SRF-213358](https://hackerone.com/reports/213358) | SSRF at apps.nextcloud.com/developer/apps/releases/new | [nextcloud](https://h1.security.nathan.sx/nextcloud.html) | Server-Side Request Forgery (SSRF) | – | full body read — confirmed SSRF (port-scan → Port-Scan-and-Internal-Mapping.md) |
| [SRF-216389](https://hackerone.com/reports/216389) | Full access at an internal service of Shopify | [shopify](https://h1.security.nathan.sx/shopify.html) | Information Disclosure | $500 | metadata only — internal-service exposure title (Internal-Service-Exposure.md) |
| [SRF-222667](https://hackerone.com/reports/222667) | Possible SSRF in email server settings(SMTP mode) | [nextcloud](https://h1.security.nathan.sx/nextcloud.html) | Server-Side Request Forgery (SSRF) | – | full body read — confirmed SSRF (port-scan → Port-Scan-and-Internal-Mapping.md) |
| [SRF-224198](https://hackerone.com/reports/224198) | Missing/Breach of Internal Security Boundary - Access to Job Queue Results in Remote Code Execution | [gitlab](https://h1.security.nathan.sx/gitlab.html) | Violation of Secure Design Principles | – | full body read — excluded, not SSRF: GitLab Sidekiq queue → RCE — internal trust-boundary RCE, not SSRF |
| [SRF-226756](https://hackerone.com/reports/226756) | local file disclosure via FFmpeg hls processing | [vkcom](https://h1.security.nathan.sx/vkcom.html) | Information Disclosure | $1,000 | metadata only (body withheld on unauthenticated retrieval) — SSRF class per title/label |
| [SRF-228377](https://hackerone.com/reports/228377) | SSRF in upload IMG through URL | [discourse](https://h1.security.nathan.sx/discourse.html) | Information Disclosure | $64 | full body read — confirmed SSRF (bypass-scheme → Validation-Bypass-and-Scheme-Abuse.md) |
| [SRF-236301](https://hackerone.com/reports/236301) | Blind SSRF due to img tag injection in career form | [mixmax](https://h1.security.nathan.sx/mixmax.html) | Server-Side Request Forgery (SSRF) | – | full body read — confirmed SSRF (blind-weapon → Blind-SSRF-and-Callback.md) |
| [SRF-237381](https://hackerone.com/reports/237381) | SSRF and local file disclosure in https://wordpress.com/media/videos/ via FFmpeg HLS processing | [automattic](https://h1.security.nathan.sx/automattic.html) | Information Disclosure | $800 | full body read — confirmed SSRF (media → Media-Processing-SSRF.md) |
| [SRF-243277](https://hackerone.com/reports/243277) | SSRF via webhook | [mixmax](https://h1.security.nathan.sx/mixmax.html) | Server-Side Request Forgery (SSRF) | – | full body read — confirmed SSRF (cloud-meta → Cloud-Instance-Metadata.md) |
| [SRF-1066](https://hackerone.com/reports/1066) | Bypass of anti-SSRF defenses in YahooCacheSystem (affecting at least YQL and Pipes) | [yahoo](https://h1.security.nathan.sx/yahoo.html) | – | – (archive-stated) | HTTP 404 at origin — recorded, unrecoverable |
| [SRF-4461](https://hackerone.com/reports/4461) | Server Side Request Forgery | [yahoo](https://h1.security.nathan.sx/yahoo.html) | – | $500 (archive-stated) | HTTP 404 at origin — recorded, unrecoverable |
| [SRF-6674](https://hackerone.com/reports/6674) | REMOTE CODE EXECUTION/LOCAL FILE INCLUSION/XSPA/SSRF, view-source:http://sb*.geo.sp1.yahoo.com/, 4/6/14, #SpringCle | [yahoo](https://h1.security.nathan.sx/yahoo.html) | – | $3,000 (archive-stated) | HTTP 404 at origin — recorded, unrecoverable |
| [SRF-12583](https://hackerone.com/reports/12583) | XXE and SSRF on webmaster.mail.ru | [mailru](https://h1.security.nathan.sx/mailru.html) | – | $700 (archive-stated) | HTTP 404 at origin — recorded, unrecoverable |
| [SRF-14033](https://hackerone.com/reports/14033) | connect.mail.ru: SSRF | [mailru](https://h1.security.nathan.sx/mailru.html) | – | $300 (archive-stated) | HTTP 404 at origin — recorded, unrecoverable |
| [SRF-56828](https://hackerone.com/reports/56828) | SSRF vulnerablity in app webhooks | [dropbox](https://h1.security.nathan.sx/dropbox.html) | – | $512 (archive-stated) | HTTP 404 at origin — recorded, unrecoverable |
| [SRF-97395](https://hackerone.com/reports/97395) | Potential SSRF in sales.mail.ru | [mailru](https://h1.security.nathan.sx/mailru.html) | – | $300 (archive-stated) | HTTP 404 at origin — recorded, unrecoverable |
| [SRF-111269](https://hackerone.com/reports/111269) | [ssrf] libav vulnerable during conversion of uploaded videos | [pornhub](https://h1.security.nathan.sx/pornhub.html) | – | $1,500 (archive-stated) | HTTP 404 at origin — recorded, unrecoverable |
| [SRF-111950](https://hackerone.com/reports/111950) | [allods.my.com] SSRF / XSPA | [mailru](https://h1.security.nathan.sx/mailru.html) | – | $150 (archive-stated) | HTTP 404 at origin — recorded, unrecoverable |
| [SRF-117158](https://hackerone.com/reports/117158) | SSRF на element.mail.ru | [mailru](https://h1.security.nathan.sx/mailru.html) | – | $250 (archive-stated) | HTTP 404 at origin — recorded, unrecoverable |
| [SRF-122697](https://hackerone.com/reports/122697) | Server Side Browsing - localhost open port enumeration | [newrelic](https://h1.security.nathan.sx/newrelic.html) | – | – (archive-stated) | HTTP 404 at origin — recorded, unrecoverable |
| [SRF-137229](https://hackerone.com/reports/137229) | Dropbox apps Server side request forgery | [dropbox](https://h1.security.nathan.sx/dropbox.html) | – | – (archive-stated) | HTTP 404 at origin — recorded, unrecoverable |
| [SRF-138721](https://hackerone.com/reports/138721) | SSRF &amp; XSS (W3 Total Cache) | [pornhub](https://h1.security.nathan.sx/pornhub.html) | – | $1,000 (archive-stated) | HTTP 404 at origin — recorded, unrecoverable |
| [SRF-139970](https://hackerone.com/reports/139970) | JIRA account misconfig causes internal info leak | [newrelic](https://h1.security.nathan.sx/newrelic.html) | – | – (archive-stated) | HTTP 404 at origin — recorded, unrecoverable |
| [SRF-141304](https://hackerone.com/reports/141304) | Blind SSRF on synthetics.newrelic.com | [newrelic](https://h1.security.nathan.sx/newrelic.html) | – | – (archive-stated) | HTTP 404 at origin — recorded, unrecoverable |
| [SRF-141682](https://hackerone.com/reports/141682) | SSRF on synthetics.newrelic.com permitting access to sensitive data | [newrelic](https://h1.security.nathan.sx/newrelic.html) | – | – (archive-stated) | HTTP 404 at origin — recorded, unrecoverable |
| [SRF-144724](https://hackerone.com/reports/144724) | SSRF in sitecheck.sucuri.net | [sucuri](https://h1.security.nathan.sx/sucuri.html) | – | $250 (archive-stated) | HTTP 404 at origin — recorded, unrecoverable |
| [SRF-146875](https://hackerone.com/reports/146875) | http://newrelic.com SSRF/XSPA | [newrelic](https://h1.security.nathan.sx/newrelic.html) | – | – (archive-stated) | HTTP 404 at origin — recorded, unrecoverable |
| [SRF-148764](https://hackerone.com/reports/148764) | [idor] Unauthorized Read access to all the private posts(Including Photos,Videos,Gifs) | [pornhub](https://h1.security.nathan.sx/pornhub.html) | – | $1,500 (archive-stated) | HTTP 404 at origin — recorded, unrecoverable |
| [SRF-151086](https://hackerone.com/reports/151086) | SSRF allows access to internal services like Ganglia | [dropbox](https://h1.security.nathan.sx/dropbox.html) | – | $729 (archive-stated) | HTTP 404 at origin — recorded, unrecoverable |
| [SRF-170151](https://hackerone.com/reports/170151) | SSRF in account webhook (through API) | [trello](https://h1.security.nathan.sx/trello.html) | – | $128 (archive-stated) | HTTP 404 at origin — recorded, unrecoverable |
| [SRF-198690](https://hackerone.com/reports/198690) | SSRF in alerts.newrelic.com exposes entire internal network | [newrelic](https://h1.security.nathan.sx/newrelic.html) | – | – (archive-stated) | HTTP 404 at origin — recorded, unrecoverable |
| [SRF-242831](https://hackerone.com/reports/242831) | Local File Disclosure via ffmpeg | [arxius](https://h1.security.nathan.sx/arxius.html) | – | – (archive-stated) | HTTP 404 at origin — recorded, unrecoverable |
| [SRF-243470](https://hackerone.com/reports/243470) | another local file disclosure via ffmpeg | [arxius](https://h1.security.nathan.sx/arxius.html) | – | – (archive-stated) | HTTP 404 at origin — recorded, unrecoverable |

## 5. Notation

- "Team (archive)" links to the archive's program page for that row.
- "Weakness (recorded)" is HackerOne's era label — the vault files document,
  case by case, where that label is wrong.
- "Bounty shown" is blank (–) where neither source records an amount.

## 6. Category-file routing map (shorthand)

| File | Cases |
| --- | --- |
| Cloud-Instance-Metadata.md | SRF-53088, SRF-128685, SRF-243277 |
| Port-Scan-and-Internal-Mapping.md | SRF-1409, SRF-49474, SRF-50537, SRF-16571, SRF-178184, SRF-145524, SRF-213358, SRF-222667, SRF-67377, SRF-67389, SRF-158016, SRF-110801 |
| Validation-Bypass-and-Scheme-Abuse.md | SRF-91816, SRF-14127, SRF-115748, SRF-61312, SRF-204513, SRF-228377 |
| Media-Processing-SSRF.md | SRF-115857, SRF-115978, SRF-237381 |
| Blind-SSRF-and-Callback.md | SRF-236301 (anchor), SRF-243277 (xref), SRF-124097, SRF-197365 (metadata) |
| Internal-Service-Exposure.md | SRF-73567, SRF-154369, SRF-158118 + metadata rows SRF-159536, SRF-165048, SRF-216389 |

## 7. External bibliography

The era methodology sources the corpus reports themselves cite (XSPA 2012,
Acunetix 2013, Sucuri 2014, Habr/oss-security 2016, "SSRF bible" 2017) plus the
clearly-separated modern PortSwigger anchor are quoted, verified, and
provenance-tagged in [`blogs-index.md`](blogs-index.md) — including the record of
why the bugbountydaily aggregator used by the sibling vaults could not be used
here (NXDOMAIN as of 2026-10-24, no Wayback captures).
