---
title: "SMUG case register — 36-row ledger (bucket smuggling-crlf) + 12 unclassified merges (h1-brain corpus)"
type: register
built: "2026-11-07"
roster: "h1-brain disclosed_reports.db (3,673 rows; sha256 8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4)"
case_id_scheme: "SMUG-<HackerOne report id>"
bounty_rule: "DB bounty_amount where present (labeled $) · None = no figure in DB (not evidence of non-payment)"
module_rule: "frozen in archive/classes.json (bodies-win classification)"
---

# Case register — HTTP Request Smuggling / CRLF

Corpus: 36 bucket rows · 19 with bounty figures · **$34,290** · max $5,000 (SMUG-1200647) · +12 unclassified merges · **$41,190/23** all-in · evidence: 48 full-body (incl. 3 PDF/one-line anchors).

Class census: Request-Smuggling-Desync (01) 22 (713285, 726773, 735748, 737140, 753939, 771666, 867577, 867952, 919175, 922597, 965267, 1002188, 1238099, 1238709, 1630667, 1630668, 1630669, 1667974, 2032842, 2280391, 2299692, 2327341) · CRLF-Header-Injection (02) 9 (237357, 409512, 590020, 712979, 858650, 1402249, 1664019, 1878489, 2147132) · Email-Protocol-Injection (03) 4 (1054282, 1200647, 1509216, 1516377) · Adjacent-and-Negative-Space (04) 13 = 1 bucket-adjacent (39181, 145128, 165102, 246803, 446271, 761222, 963816, 1135875, 1135876, 1368721, 1391549, 1401159, 1594627).

| Case | Team | Weakness (DB) | Asset · Type | CVE | Bounty | Module | Evidence | Title |
|---|---|---|---|---|---|---|---|---|
| [SMUG-39181](https://hackerone.com/reports/39181) | vimeo | — | — · — | — | - | 04-Adjacent | full | [vimeopro.com] CRLF Injection |
| [SMUG-145128](https://hackerone.com/reports/145128) | ui | — | — · — | — | - | 04-Adjacent | full | [account-global.ubnt.com] CRLF Injection |
| [SMUG-165102](https://hackerone.com/reports/165102) | ibb | — | Python (Legacy) · OTHER | CVE-2016-5699 | - | 04-Adjacent | full | urllib HTTP header injection CVE-2016-5699 |
| [SMUG-237357](https://hackerone.com/reports/237357) | snapchat | CRLF Injection | — · — | — | - | 02-CRLF | full | CRLF Injection at vpn.bitstrips.com |
| [SMUG-246803](https://hackerone.com/reports/246803) | snapchat | HTTP Request Smuggling | — · — | — | $250 | 04-Adjacent | full | [spectacles.com] Bypassing quantity limit in orders |
| [SMUG-409512](https://hackerone.com/reports/409512) | ibb | CRLF Injection | Apache (Legacy) · OTHER | CVE-2016-4975 | $500 | 02-CRLF | full | mod_userdir CRLF injection (CVE-2016-4975) |
| [SMUG-446271](https://hackerone.com/reports/446271) | x | — | *.twitter.com · WILDCARD | — | - | 04-Adjacent | full | CRLF injection |
| [SMUG-590020](https://hackerone.com/reports/590020) | ibb | CRLF Injection | Python (Legacy) · OTHER | CVE-2019-9947 | - | 02-CRLF | full | CRLF Injection in urllib |
| [SMUG-712979](https://hackerone.com/reports/712979) | x | CRLF Injection | *.twitter.com · WILDCARD | — | - | 02-CRLF | full | Creating malformed URLs via new line character in-between two URLs leads to misr |
| [SMUG-713285](https://hackerone.com/reports/713285) | x | HTTP Request Smuggling | *.periscope.tv · WILDCARD | — | $560 | 01-Desync | full | http request smuggling in pscp.tv and periscope.tv |
| [SMUG-726773](https://hackerone.com/reports/726773) | gsa_bbp | HTTP Request Smuggling | labs.data.gov · URL | — | $750 | 01-Desync | full | HTTP Request Smuggling on https://labs.data.gov |
| [SMUG-735748](https://hackerone.com/reports/735748) | nodejs | HTTP Request Smuggling | https://github.com/nodejs/node · SOURCE_CODE | CVE-2019-15605 | - | 01-Desync | full | HTTP request smuggling using malformed Transfer-Encoding header |
| [SMUG-737140](https://hackerone.com/reports/737140) | slack | HTTP Request Smuggling | slackb.com · URL | — | - | 01-Desync | full | Mass account takeovers using HTTP Request Smuggling on https://slackb.com/ to st |
| [SMUG-753939](https://hackerone.com/reports/753939) | magic-bbp | HTTP Request Smuggling | — · — | — | - | 01-Desync | full | HTTP SMUGGLING EXPOSED HMAC/DOS  |
| [SMUG-761222](https://hackerone.com/reports/761222) | github-security-lab | — | — · — | — | $1,500 | 04-Adjacent | full | Netty HTTP Response Splitting (CRLF Injection) due to disabled header validation |
| [SMUG-771666](https://hackerone.com/reports/771666) | zomato | HTTP Request Smuggling | *.zomato.com · WILDCARD | — | - | 01-Desync | full | Stealing Zomato X-Access-Token: in Bulk using HTTP Request Smuggling on api.zoma |
| [SMUG-858650](https://hackerone.com/reports/858650) | starbucks | CRLF Injection | www.starbucks.com · URL | — | - | 02-CRLF | full | CRLF injection on www.starbucks.com |
| [SMUG-867577](https://hackerone.com/reports/867577) | basecamp | HTTP Request Smuggling | launchpad.37signals.com · URL | — | - | 01-Desync | full | Unauthenticated request smuggling on launchpad.37signals.com |
| [SMUG-867952](https://hackerone.com/reports/867952) | helium | HTTP Request Smuggling | https://helium-console-dev.herokuapp.com/ · URL | — | - | 01-Desync | full | HTTP request Smuggling |
| [SMUG-919175](https://hackerone.com/reports/919175) | basecamp | HTTP Request Smuggling | basecamp.com · URL | — | - | 01-Desync | full | HTTP request smuggling on Basecamp 2 allows web cache poisoning |
| [SMUG-922597](https://hackerone.com/reports/922597) | nodejs | HTTP Request Smuggling | https://github.com/nodejs/node · SOURCE_CODE | CVE-2020-8201 | - | 01-Desync | full | HTTP Request Smuggling due to CR-to-Hyphen conversion |
| [SMUG-963816](https://hackerone.com/reports/963816) | github-security-lab | — | — · — | — | - | 04-Adjacent | full | [javascript] CWE-117: CodeQL query to detect Log Injection |
| [SMUG-965267](https://hackerone.com/reports/965267) | ruby | HTTP Request Smuggling | https://github.com/ruby/ruby · SOURCE_CODE | — | $500 | 01-Desync | full | Potential HTTP Request Smuggling in ruby webrick |
| [SMUG-1002188](https://hackerone.com/reports/1002188) | nodejs | HTTP Request Smuggling | https://github.com/nodejs/node · SOURCE_CODE | CVE-2020-8287 | $250 | 01-Desync | full | Potential HTTP Request Smuggling in nodejs |
| [SMUG-1054282](https://hackerone.com/reports/1054282) | owncloud | CRLF Injection | owncloud/user_ldap · SOURCE_CODE | — | - | 03-Email | full | Protocol Smuggling over LDAP password field |
| [SMUG-1135875](https://hackerone.com/reports/1135875) | github-security-lab | — | — · — | — | - | 04-Adjacent | full |  Java : Add query for detecting Log Injection vulenrabilities |
| [SMUG-1135876](https://hackerone.com/reports/1135876) | github-security-lab | — | — · — | — | - | 04-Adjacent | full |  Java : Add query for detecting Log Injection vulenrabilities |
| [SMUG-1200647](https://hackerone.com/reports/1200647) | aiven_ltd | CRLF Injection | Aiven for Grafana managed and hosted service · OTHER | — | $5,000 | 03-Email | full | Grafana RCE via SMTP server parameter injection |
| [SMUG-1238099](https://hackerone.com/reports/1238099) | nodejs | HTTP Request Smuggling | https://github.com/nodejs/node · SOURCE_CODE | CVE-2021-22960 | $250 | 01-Desync | full | HTTP Request Smuggling due to ignoring chunk extensions |
| [SMUG-1238709](https://hackerone.com/reports/1238709) | nodejs | HTTP Request Smuggling | https://github.com/nodejs/node · SOURCE_CODE | CVE-2021-22959 | $250 | 01-Desync | full | HTTP Request Smuggling due to accepting space before colon |
| [SMUG-1368721](https://hackerone.com/reports/1368721) | github-security-lab | — | — · — | — | - | 04-Adjacent | full | [Python]: CWE-117 Log Injection  |
| [SMUG-1391549](https://hackerone.com/reports/1391549) | ibb | — | https://github.com/apache/httpd · SOURCE_CODE | CVE-2021-33193 | $1,200 | 04-Adjacent | full | Request line injection via HTTP/2 in Apache mod_proxy |
| [SMUG-1401159](https://hackerone.com/reports/1401159) | github-security-lab | — | — · — | — | $1,800 | 04-Adjacent | full | [Python]: CWE-079: HTTP Header injection |
| [SMUG-1402249](https://hackerone.com/reports/1402249) | nextcloud | CRLF Injection | nextcloud/server · SOURCE_CODE | CVE-2022-24888 | - | 02-CRLF | full | Control character filtering misses leading and trailing whitespace in file and f |
| [SMUG-1509216](https://hackerone.com/reports/1509216) | nextcloud | CRLF Injection | nextcloud/calendar · SOURCE_CODE | — | - | 03-Email | full | SMTP Command Injection in Appointment Emails via Newlines |
| [SMUG-1516377](https://hackerone.com/reports/1516377) | nextcloud | CRLF Injection | nextcloud/calendar · SOURCE_CODE | CVE-2022-31014 | - | 03-Email | full | SMTP Command Injection in iCalendar Attachments to Emails via Newlines |
| [SMUG-1594627](https://hackerone.com/reports/1594627) | ibb | — | https://github.com/apache/httpd · SOURCE_CODE | CVE-2022-26377 | $2,400 | 04-Adjacent | full | Apache HTTP Server: mod_proxy_ajp: Possible request smuggling |
| [SMUG-1630667](https://hackerone.com/reports/1630667) | ibb | HTTP Request Smuggling | https://github.com/nodejs/node · SOURCE_CODE | CVE-2022-32215 | $1,800 | 01-Desync | full |  CVE-2022-32215 - HTTP Request Smuggling Due to Incorrect Parsing of Multi-line  |
| [SMUG-1630668](https://hackerone.com/reports/1630668) | ibb | HTTP Request Smuggling | https://github.com/nodejs/node · SOURCE_CODE | CVE-2022-32213 | $1,800 | 01-Desync | full |  CVE-2022-32213 - HTTP Request Smuggling Due to Flawed Parsing of Transfer-Encod |
| [SMUG-1630669](https://hackerone.com/reports/1630669) | ibb | HTTP Request Smuggling | https://github.com/nodejs/node · SOURCE_CODE | CVE-2022-32214 | $1,800 | 01-Desync | full | CVE-2022-32214 - HTTP Request Smuggling Due To Improper Delimiting of Header Fie |
| [SMUG-1664019](https://hackerone.com/reports/1664019) | ibb | CRLF Injection | https://github.com/nodejs/node · SOURCE_CODE | CVE-2022-35948 | - | 02-CRLF | full | CVE-2022-35948: CRLF Injection in Nodejs ‘undici’ via Content-Type |
| [SMUG-1667974](https://hackerone.com/reports/1667974) | ibb | HTTP Request Smuggling | https://github.com/apache/httpd · SOURCE_CODE | — | $4,000 | 01-Desync | full | Pause-based desync in Apache HTTPD |
| [SMUG-1878489](https://hackerone.com/reports/1878489) | ibb | CRLF Injection | https://github.com/nodejs/node · SOURCE_CODE | CVE-2023-23936 | $600 | 02-CRLF | full | CRLF Injection in Nodejs ‘undici’ via host |
| [SMUG-2032842](https://hackerone.com/reports/2032842) | ibb | HTTP Request Smuggling | https://github.com/nodejs/node · SOURCE_CODE | CVE-2023-30589 | $1,800 | 01-Desync | full | HTTP Request Smuggling via Empty headers separated by CR |
| [SMUG-2147132](https://hackerone.com/reports/2147132) | mozilla | CRLF Injection | bugzilla.mozilla.org · URL | — | $200 | 02-CRLF | full | Security bug https://bugzilla.mozilla.org/oauth/authorize - CRLF Header injectio |
| [SMUG-2280391](https://hackerone.com/reports/2280391) | ibb | HTTP Request Smuggling | https://github.com/apache/tomcat · SOURCE_CODE | — | $4,660 | 01-Desync | full | Possibility of Request smuggling attack |
| [SMUG-2299692](https://hackerone.com/reports/2299692) | ibb | HTTP Request Smuggling | https://github.com/apache/tomcat · SOURCE_CODE | CVE-2023-45648 | $4,660 | 01-Desync | full | Request Smuggling in Apache Tomcat (Important, CVE-2023-45648) |
| [SMUG-2327341](https://hackerone.com/reports/2327341) | ibb | HTTP Request Smuggling | https://github.com/apache/tomcat · SOURCE_CODE | CVE-2024-21733 | $4,660 | 01-Desync | full | CVE-2024-21733 Apache Tomcat HTTP Request Smuggling (Client- Side Desync) (CWE:  |

Bounty arithmetic: $5,000 + $4,660×3 + $4,000 + $1,800×4 + $750 + $600 + $560 + $500×2 + $250×4 + $200 = **$34,290** (19 rows).

Module totals: 01 Desync $27,740/14 · 02 CRLF $1,300/3 · 03 Email $5,000/1 · bucket-adjacent ($250/1, single row) = $34,290.
Unclassified merges add $6,900/4 (1391549 $1,200 + 1594627 $2,400 + 1401159 $1,800 + 761222 $1,500); grand total with merges **$41,190/23**.

| Unclassified merges (all in module 04): 39181 vimeopro · 145128 ui · 165102 ibb (CVE-2016-5699) · 446271 x · 761222 github-security-lab $1,500 · 963816 github-security-lab · 1135875 github-security-lab · 1135876 github-security-lab · 1368721 github-security-lab · 1391549 ibb $1,200 (CVE-2021-33193) · 1401159 github-security-lab $1,800 (CWE-079) · 1594627 ibb $2,400 (CVE-2022-26377) |
