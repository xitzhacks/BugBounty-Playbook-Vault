---
title: "Vault class INJ — Injection and Smuggling"
type: dataset-view
class: "Injection and Smuggling"
vault_category: "XXE/"
rows: 389
paid_rows: 87
bounty_sum: 172,582
full_bodies_available: 263
source: "public HackerOne vault (hackerone disclosed), harvested 2026-11-17"
---

# INJ — Injection and Smuggling

389 rows · 87 with a bounty figure · **$172,582** total · 263 with full write-up stored.
Playbook: `Vault/XXE/` · Dataset: `Vault/_VAULT/reports.sqlite` (`SELECT * FROM reports WHERE ...`).

| Report | Program | Severity | Bounty | Votes | Disclosed | Weakness | Title |
|---|---|---|---|---|---|---|---|
| [510152](https://hackerone.com/reports/510152) | PayPal | high | $20,000 | 2687 | 2019-08-07 | HTTP Request Smuggling | Bypass for #488147 enables stored XSS on https://paypal.com/signin again |
| [488147](https://hackerone.com/reports/488147) | PayPal | high | $18,900 | 685 | 2019-08-07 | HTTP Request Smuggling | Stored XSS on https://paypal.com/signin via cache poisoning |
| [1211724](https://hackerone.com/reports/1211724) | Basecamp | critical | $7,500 | 300 | 2021-08-27 | HTTP Request Smuggling | HTTP Request Smuggling via HTTP/2 |
| [505947](https://hackerone.com/reports/505947) | Mail.ru |  | $6,000 | 264 |  | XML External Entities (XXE) | XXE on pulse.mail.ru |
| [1478633](https://hackerone.com/reports/1478633) | Cloudflare Public Bug Bounty | critical | $6,000 | 116 | 2022-05-16 | HTTP Request Smuggling | HTTP Request Smuggling in Transform Rules using hexadecimal escape sequences in the concat() function |
| [957881](https://hackerone.com/reports/957881) | Mail.ru |  | $5,000 | 241 |  | HTTP Request Smuggling | HTTP request smuggling (?) canpol.deti.mail.ru |
| [1200647](https://hackerone.com/reports/1200647) | Aiven Ltd | critical | $5,000 | 72 | 2022-11-08 | CRLF Injection | Grafana RCE via SMTP server parameter injection |
| [2585381](https://hackerone.com/reports/2585381) | Internet Bug Bounty | high | $4,920 | 51 | 2024-07-13 | Improper Input Validation | important: Apache HTTP Server weakness with encoded question marks in backreferences (CVE-2024-38474) |
| [2585378](https://hackerone.com/reports/2585378) | Internet Bug Bounty | high | $4,920 | 30 | 2024-07-13 | Improper Input Validation | important: Apache HTTP Server weakness in mod_rewrite when first segment of substitution matches filesystem path. (CVE-2024-38475) |
| [2280391](https://hackerone.com/reports/2280391) | Internet Bug Bounty | high | $4,660 | 93 | 2023-12-22 | HTTP Request Smuggling | Possibility of Request smuggling attack |
| [2327341](https://hackerone.com/reports/2327341) | Internet Bug Bounty | high | $4,660 | 57 | 2024-01-29 | HTTP Request Smuggling | CVE-2024-21733 Apache Tomcat HTTP Request Smuggling (Client- Side Desync) (CWE: 444) |
| [2299692](https://hackerone.com/reports/2299692) | Internet Bug Bounty | high | $4,660 | 51 | 2024-02-07 | HTTP Request Smuggling | Request Smuggling in Apache Tomcat (Important, CVE-2023-45648) |
| [1667974](https://hackerone.com/reports/1667974) | Internet Bug Bounty | high | $4,000 | 74 | 2022-08-25 | HTTP Request Smuggling | Pause-based desync in Apache HTTPD |
| [1637621](https://hackerone.com/reports/1637621) | GitHub | none | $4,000 | 32 | 2022-11-03 | Resource Injection | Command injection in GitHub Actions ContainerStepHost |
| [1575912](https://hackerone.com/reports/1575912) | Cloudflare Public Bug Bounty | critical | $3,100 | 46 | 2022-06-27 | HTTP Request Smuggling | HTTP request smuggling with Origin Rules using newlines in the host_header action parameter |
| [498052](https://hackerone.com/reports/498052) | New Relic |  | $3,000 | 490 |  | HTTP Request Smuggling | Password theft login.newrelic.com via Request Smuggling |
| [2585374](https://hackerone.com/reports/2585374) | Internet Bug Bounty | medium | $2,600 | 89 | 2024-08-12 | Improper Input Validation | moderate: Apache HTTP Server: mod_rewrite proxy handler substitution (CVE-2024-39573) CWE-20 Improper Input Validation |
| [2585373](https://hackerone.com/reports/2585373) | Internet Bug Bounty | medium | $2,600 | 19 | 2024-07-13 | HTTP Response Splitting | moderate: Apache HTTP Server: HTTP response splitting (CVE-2023-38709) |
| [2585384](https://hackerone.com/reports/2585384) | Internet Bug Bounty | medium | $2,600 | 16 | 2024-07-13 | Improper Input Validation | moderate: Apache HTTP Server proxy encoding problem (CVE-2024-38473) |
| [544096](https://hackerone.com/reports/544096) | Valve | high | $2,500 | 60 | 2021-05-06 | Improper Input Validation | [Source Engine] Material path truncation leads to Remote Code Execution |
| [197279](https://hackerone.com/reports/197279) | Airbnb | low | $2,500 | 37 | 2018-04-03 | HTTP Response Splitting | [m.airbnb.com] CRLF Injection |
| [1966083](https://hackerone.com/reports/1966083) | Internet Bug Bounty | medium | $2,400 | 22 | 2023-07-12 | Improper Input Validation | CVE-2023-28710 Apache Airflow Spark Provider Arbitrary File Read via JDBC |
| [1594627](https://hackerone.com/reports/1594627) | Internet Bug Bounty | medium | $2,400 | 21 | 2022-07-09 | HTTP Request Smuggling | Apache HTTP Server: mod_proxy_ajp: Possible request smuggling |
| [1895277](https://hackerone.com/reports/1895277) | Internet Bug Bounty | medium | $2,400 | 7 | 2023-04-16 | Improper Input Validation | Apache Airflow Google Cloud Sql Provider Remote Command Execution |
| [2921724](https://hackerone.com/reports/2921724) | Internet Bug Bounty | medium | $2,162 | 88 | 2025-03-07 | Improper Input Validation | Deadlock in x86 HVM standard VGA handling |
| [303744](https://hackerone.com/reports/303744) | Open-Xchange |  | $2,000 | 125 |  | Resource Injection | Arbitrary local system file read on open-xchange server |
| [334488](https://hackerone.com/reports/334488) | Open-Xchange |  | $2,000 | 86 |  | XML External Entities (XXE) | Blind XXE via Powerpoint files |
| [790634](https://hackerone.com/reports/790634) | GitLab | medium | $2,000 | 39 | 2021-08-19 | Resource Injection | When you call your branch the same name as a git hash, it could be checked out by dependents |
| [2032842](https://hackerone.com/reports/2032842) | Internet Bug Bounty | medium | $1,800 | 16 | 2023-08-28 | HTTP Request Smuggling | HTTP Request Smuggling via Empty headers separated by CR |
| [1888760](https://hackerone.com/reports/1888760) | Internet Bug Bounty | medium | $1,800 | 15 | 2023-04-09 | HTTP Request Smuggling | HTTP Request Smuggling Due to Incorrect Parsing of Header Fields |
| [1630668](https://hackerone.com/reports/1630668) | Internet Bug Bounty | medium | $1,800 | 13 | 2022-07-22 | HTTP Request Smuggling | CVE-2022-32213 - HTTP Request Smuggling Due to Flawed Parsing of Transfer-Encoding |
| [1630669](https://hackerone.com/reports/1630669) | Internet Bug Bounty | medium | $1,800 | 11 | 2022-07-22 | HTTP Request Smuggling | CVE-2022-32214 - HTTP Request Smuggling Due To Improper Delimiting of Header Fields |
| [1630667](https://hackerone.com/reports/1630667) | Internet Bug Bounty | medium | $1,800 | 6 | 2022-07-22 | HTTP Request Smuggling | CVE-2022-32215 - HTTP Request Smuggling Due to Incorrect Parsing of Multi-line Transfer-Encoding |
| [1512937](https://hackerone.com/reports/1512937) | GitHub Security Lab |  | $1,800 | 4 |  | XML External Entities (XXE) | [Python]: CWE-611: XXE |
| [1401159](https://hackerone.com/reports/1401159) | GitHub Security Lab |  | $1,800 | 3 |  | CRLF Injection | [Python]: CWE-079: HTTP Header injection |
| [347139](https://hackerone.com/reports/347139) | Rockstar Games | critical | $1,500 | 79 | 2018-08-01 | XML External Entities (XXE) | LFI and SSRF via XXE in emblem editor |
| [761222](https://hackerone.com/reports/761222) | GitHub Security Lab |  | $1,500 | 14 |  | CRLF Injection | Netty HTTP Response Splitting (CRLF Injection) due to disabled header validation |
| [1935628](https://hackerone.com/reports/1935628) | GitLab | low | $1,060 | 61 | 2024-10-08 | Resource Injection | HTML injection possible with soft email confirmations when Administrator manually confirms attacker email address |
| [590020](https://hackerone.com/reports/590020) | Internet Bug Bounty | medium | $1,000 | 341 | 2020-05-06 | CRLF Injection | CRLF Injection in urllib |
| [1078002](https://hackerone.com/reports/1078002) | Nextcloud | medium | $1,000 | 73 | 2021-04-15 | Resource Injection | Nextcloud Desktop Client RCE via malicious URI schemes |
| [786745](https://hackerone.com/reports/786745) | Mail.ru |  | $1,000 | 70 |  | Improper Input Validation | [API] ICQ user's avatar can be manipulated remotely |
| [977851](https://hackerone.com/reports/977851) | Shopify | low | $1,000 | 67 | 2020-09-11 | Improper Neutralization of HTTP Headers for Scripting Syntax | Cache poisoning via X-Forwarded-Host in www.shopify.com/partners/blog |
| [1651429](https://hackerone.com/reports/1651429) | MetaMask | low | $1,000 | 32 | 2023-04-10 | Improper Input Validation | Bypass parsing of transaction data, users on the phishing site will transfer/approve  ERC20 tokens without being alerted |
| [277341](https://hackerone.com/reports/277341) | Mail.ru |  | $1,000 | 12 |  | XML External Entities (XXE) | blind XXE when uploading avatar in mymail phone app |
| [2279572](https://hackerone.com/reports/2279572) | Shopify | low | $800 | 136 | 2025-03-27 | HTTP Response Splitting | HTTP Response Header Injection in shopify/pitchfork + Rack 3 |
| [276276](https://hackerone.com/reports/276276) | Mail.ru |  | $800 | 23 |  | XML External Entities (XXE) | Blind XXE on my.mail.ru |
| [726773](https://hackerone.com/reports/726773) | GSA Bounty | high | $750 | 160 | 2020-05-13 | HTTP Request Smuggling | HTTP Request Smuggling on https://labs.data.gov |
| [727974](https://hackerone.com/reports/727974) | Mail.ru |  | $750 | 18 |  | Improper Input Validation | [pandao.ru] possibility to attach arbitrary phone number to account registered via social network |
| [1878489](https://hackerone.com/reports/1878489) | Internet Bug Bounty | medium | $600 | 10 | 2023-03-29 | CRLF Injection | CRLF Injection in Nodejs ‘undici’ via host |
| [713285](https://hackerone.com/reports/713285) | X / xAI | high | $560 | 24 | 2020-09-10 | HTTP Request Smuggling | http request smuggling in pscp.tv and periscope.tv |
| [919988](https://hackerone.com/reports/919988) | Visma Public |  | $500 | 139 |  | HTTP Request Smuggling | HTTP Request Smuggling at app.workbox.dk |
| [694604](https://hackerone.com/reports/694604) | Lob |  | $500 | 123 |  | HTTP Request Smuggling | HTTP Request Smuggling on vpn.lob.com |
| [3279441](https://hackerone.com/reports/3279441) | Mozilla | low | $500 | 93 | 2026-04-27 | Improper Input Validation | Bypass of Restricted Keyword "Mozilla" in Display Name Field via Unicode Homoglyphs on addons.allizom.org |
| [347439](https://hackerone.com/reports/347439) | New Relic |  | $500 | 60 |  | CRLF Injection | [synthetics.newrelic.com] SMTP header injection leads to (mass) arbitrary email sending |
| [757100](https://hackerone.com/reports/757100) | Mail.ru |  | $500 | 57 |  | Improper Input Validation | HTML injection at face.city-mobil.ru |
| [296622](https://hackerone.com/reports/296622) | VK.com | medium | $500 | 18 | 2018-03-04 | XML External Entities (XXE) | Blind XXE on pu.vk.com |
| [409512](https://hackerone.com/reports/409512) | Internet Bug Bounty | medium | $500 | 17 | 2018-10-02 | CRLF Injection | mod_userdir CRLF injection (CVE-2016-4975) |
| [690387](https://hackerone.com/reports/690387) | Mail.ru |  | $500 | 12 |  | XML External Entities (XXE) | OOB XXE |
| [66386](https://hackerone.com/reports/66386) | Shopify |  | $500 | 5 | 2015-06-10 | CRLF Injection | [www.*.myshopify.com] CRLF Injection |
| [690295](https://hackerone.com/reports/690295) | Mail.ru |  | $500 | 5 |  | XML External Entities (XXE) | OOB XXE |
| [1238017](https://hackerone.com/reports/1238017) | Kubernetes | medium | $500 | 5 | 2022-06-02 | Resource Injection | AWS Load Balancer Controller Managed Security Groups can be replaced by an unprivileged attacker |
| [1238482](https://hackerone.com/reports/1238482) | Kubernetes | medium | $500 | 3 | 2022-06-02 | Resource Injection | AWS Load Balancer Controller can be used by an attacker to modify rules of any Security Group that they are able to tag |
| [1895316](https://hackerone.com/reports/1895316) | Internet Bug Bounty | low | $480 | 8 | 2023-04-16 | Improper Input Validation | CVE-2023-25692: Apache Airflow Google Provider: Google Cloud Sql Provider Denial Of Service and Remote Command Execution |
| [121489](https://hackerone.com/reports/121489) | LocalTapiola |  | $400 | 11 |  | CRLF Injection | CRLF injection in https://verkkopalvelu.lahitapiola.fi/ |
| [711679](https://hackerone.com/reports/711679) | Razer |  | $375 | 18 |  | HTTP Request Smuggling | Request Smuggling vulnerability due a vulnerable skipper reverse proxy running in the environment. |
| [1108504](https://hackerone.com/reports/1108504) | CS Money | medium | $300 | 77 | 2024-01-23 | Failure to Sanitize Special Elements into a Different Plane (Special Element Injection) | Html injection on subscription email |
| [2067247](https://hackerone.com/reports/2067247) | Sorare | low | $300 | 23 | 2023-08-01 | Improper Input Validation | Operation CreateOrUpdateSo5LineupMutation does not restrict multiple captains |
| [826463](https://hackerone.com/reports/826463) | Razer |  | $250 | 109 |  | Improper Handling of URL Encoding (Hex Encoding) | HTML injection in support.razer.com [IE only] |
| [1002188](https://hackerone.com/reports/1002188) | Node.js | low | $250 | 34 | 2021-01-07 | HTTP Request Smuggling | Potential HTTP Request Smuggling in nodejs |
| [246803](https://hackerone.com/reports/246803) | Snapchat | medium | $250 | 22 | 2017-08-12 | HTTP Request Smuggling | [spectacles.com] Bypassing quantity limit in orders |
| [1238709](https://hackerone.com/reports/1238709) | Node.js | medium | $250 | 18 | 2021-10-20 | HTTP Request Smuggling | HTTP Request Smuggling due to accepting space before colon |
| [1238099](https://hackerone.com/reports/1238099) | Node.js | medium | $250 | 7 | 2021-11-02 | HTTP Request Smuggling | HTTP Request Smuggling due to ignoring chunk extensions |
| [66257](https://hackerone.com/reports/66257) | Mail.ru |  | $250 | 5 |  | CRLF Injection | [s.mail.ru] CRLF Injection |
| [2147132](https://hackerone.com/reports/2147132) | Mozilla | low | $200 | 61 | 2023-10-28 | CRLF Injection | Security bug https://bugzilla.mozilla.org/oauth/authorize - CRLF Header injection via "redirect_uri" parameter |
| [1848118](https://hackerone.com/reports/1848118) | Acronis |  | $200 | 46 |  | Resource Injection | Render content from untrusted sources via web_preview endpoint on Acronis Cloud |
| [1514359](https://hackerone.com/reports/1514359) | EXNESS | low | $200 | 15 | 2022-04-13 | CRLF Injection | CRLF Injection - Http Response Splitting |
| [67386](https://hackerone.com/reports/67386) | Mail.ru |  | $160 | 7 |  | CRLF Injection | [my.mail.ru] CRLF Injection |
| [2541027](https://hackerone.com/reports/2541027) | Mattermost | low | $150 | 40 | 2024-10-01 | Improper Input Validation | Posts sent via websockets aren't sanitized properly |
| [953203](https://hackerone.com/reports/953203) | Eternal | low | $150 | 8 | 2020-08-11 | Failure to Sanitize Special Elements into a Different Plane (Special Element Injection) | [api.zomato.com] Abusing LocalParams (city_id) to Inject SOLR query |
| [215410](https://hackerone.com/reports/215410) | ownCloud | medium | $150 | 6 | 2017-07-06 | Resource Injection | HTML Injection in Owncloud |
| [3789570](https://hackerone.com/reports/3789570) | 8x8 | low | $100 | 72 | 2026-07-02 | Improper Input Validation | jitsi-meet: Prosody/Jigasi missing header whitelist in mod_filter_iq_rayo allows arbitrary SIP header injection and Caller ID spoofing |
| [1543770](https://hackerone.com/reports/1543770) | Reddit | low | $100 | 19 | 2022-07-04 | Improper Input Validation | Moderators can send messages to users from banned subreddits via `oauth.reddit.com/api/mod/conversations` |
| [592864](https://hackerone.com/reports/592864) | Nextcloud | medium | $100 | 15 | 2020-07-09 | CRLF Injection | Non-admin users can trigger writes to memcached by entering a malicious server as a share URL |
| [242408](https://hackerone.com/reports/242408) | VK.com | low | $100 | 7 | 2017-07-23 | CRLF Injection | Нет маркера на добавление песни в плейлист пользователя |
| [300622](https://hackerone.com/reports/300622) | VK.com | low | $100 | 7 | 2018-02-09 | CRLF Injection | Монипулирование на страницах пользоватлей значением "Подсказывать стикеры в полях ввода" |
| [95981](https://hackerone.com/reports/95981) | Deriv.com |  | $75 | 11 | 2015-11-15 | CRLF Injection | Http Response Splitting - Validate link |
| [79552](https://hackerone.com/reports/79552) | Gratipay | high | $40 | 6 | 2015-08-20 | CRLF Injection | [gratipay.com] CRLF Injection |
| [737140](https://hackerone.com/reports/737140) | Slack | critical | - | 870 | 2020-03-12 | HTTP Request Smuggling | Mass account takeovers using HTTP Request Smuggling on https://slackb.com/ to steal session cookies |
| [740037](https://hackerone.com/reports/740037) | LY Corporation | high | - | 565 | 2020-05-19 | HTTP Request Smuggling | Request smuggling on admin-official.line.me could lead to account takeover |
| [771666](https://hackerone.com/reports/771666) | Eternal | critical | - | 559 | 2020-07-09 | HTTP Request Smuggling | Stealing Zomato X-Access-Token: in Bulk using HTTP Request Smuggling on api.zomato.com |
| [684092](https://hackerone.com/reports/684092) | BlockDev Sp. Z o.o | critical | - | 466 | 2019-10-01 | Improper Input Validation | Steal ALL collateral during liquidation by exploiting lack of validation in `flip.kick` |
| [446271](https://hackerone.com/reports/446271) | X / xAI | medium | - | 439 | 2019-12-25 | CRLF Injection | CRLF injection |
| [409395](https://hackerone.com/reports/409395) | GitLab | critical | - | 363 | 2019-04-10 | Improper Input Validation | Bypass of GitLab CI runner slash fix in YAML validation |
| [500515](https://hackerone.com/reports/500515) | Starbucks | critical | - | 319 | 2019-11-13 | XML External Entities (XXE) | XXE at ecjobs.starbucks.com.cn/retail/hxpublic_v6/hxdynamicpage6.aspx |
| [867952](https://hackerone.com/reports/867952) | Helium | high | - | 300 | 2020-07-02 | HTTP Request Smuggling | HTTP request Smuggling |
| [248668](https://hackerone.com/reports/248668) | X / xAI | medium | - | 258 | 2017-07-26 | XML External Entities (XXE) | XXE on sms-be-vip.twitter.com in SXMP Processor |
| [483774](https://hackerone.com/reports/483774) | DuckDuckGo | critical | - | 218 | 2019-01-31 | XML External Entities (XXE) | XXE on https://duckduckgo.com |
| [395296](https://hackerone.com/reports/395296) | ██████ |  | - | 172 |  | XML External Entities (XXE) | Phone Call to XXE via Interactive Voice Response |
| [486732](https://hackerone.com/reports/486732) | DuckDuckGo | high | - | 159 | 2019-02-25 | XML External Entities (XXE) | Partial bypass of #483774 with Blind XXE on https://duckduckgo.com |
| [2372363](https://hackerone.com/reports/2372363) | HackerOne | medium | - | 159 | 2024-05-13 | LLM01: Prompt Injection | LLM01: Invisible Prompt Injection |
| [179828](https://hackerone.com/reports/179828) | Paragon Initiative Enterprises | critical | - | 147 | 2016-11-03 | XML External Entities (XXE) | DMARC  Not found for paragonie.com   URGENT |
| [836877](https://hackerone.com/reports/836877) | Informatica | critical | - | 138 | 2020-04-21 | XML External Entities (XXE) | XXE through injection of a payload in the XMP metadata of a JPEG file |
| [922597](https://hackerone.com/reports/922597) | Node.js | high | - | 134 | 2020-10-17 | HTTP Request Smuggling | HTTP Request Smuggling due to CR-to-Hyphen conversion |
| [2054283](https://hackerone.com/reports/2054283) | Node.js | medium | - | 122 | 2025-06-13 | HTTP Request Smuggling | Improper HTTP header block termination in llhttp |
| [312543](https://hackerone.com/reports/312543) | Semrush | critical | - | 115 | 2018-03-13 | XML External Entities (XXE) | XXE in Site Audit function exposing file and directory contents |
| [897244](https://hackerone.com/reports/897244) | Zivver |  | - | 112 |  | XML External Entities (XXE) | XXE Injection through SVG image upload leads to SSRF |
| [735748](https://hackerone.com/reports/735748) | Node.js | critical | - | 105 | 2020-03-07 | HTTP Request Smuggling | HTTP request smuggling using malformed Transfer-Encoding header |
| [3175695](https://hackerone.com/reports/3175695) | Mozilla | low | - | 98 | 2025-07-29 | Improper Input Validation | Bypass "No Links" Restriction in Biography via Protocol-Relative URL (//) |
| [227880](https://hackerone.com/reports/227880) | U.S. Dept Of Defense | critical | - | 97 | 2019-10-04 | XML External Entities (XXE) | XXE in DoD website that may lead to RCE |
| [1343492](https://hackerone.com/reports/1343492) | TikTok | low | - | 97 | 2021-10-30 | Improper Input Validation | HTML Injection on tiktoktutorials via firstName parameter |
| [2189960](https://hackerone.com/reports/2189960) | TikTok | medium | - | 97 | 2023-10-31 | CRLF Injection | CRLF injection leads to internal XSS on PangleGlobal |
| [712979](https://hackerone.com/reports/712979) | X / xAI | low | - | 96 | 2020-01-24 | CRLF Injection | Creating malformed URLs via new line character in-between two URLs leads to misrepresented hyperlinks in Tweets/DMs |
| [423073](https://hackerone.com/reports/423073) | HackerOne | high | - | 82 | 2018-10-25 | Improper Input Validation | Improper UUID validation results in bypass of #419896 |
| [3086301](https://hackerone.com/reports/3086301) | Brave Software | high | - | 77 | 2025-08-22 | LLM01: Prompt Injection | Prompt Injection via GitHub Patch in Brave AI Chat (Leo) |
| [3042984](https://hackerone.com/reports/3042984) | 1Password - Enterprise Password Manager | none | - | 75 | 2025-04-12 | Improper Neutralization of Formula Elements in a CSV File | #**CSV Injection in shared passwords leads to complete Private Vault Exfiltration** |
| [753939](https://hackerone.com/reports/753939) | Magic | medium | - | 74 | 2020-03-24 | HTTP Request Smuggling | HTTP SMUGGLING EXPOSED HMAC/DOS |
| [758445](https://hackerone.com/reports/758445) | Internet Bug Bounty | critical | - | 74 | 2021-08-26 | HTTP Response Splitting | HTTP Smuggling multiple issues in Squid 3.x & squid 4.x |
| [3175928](https://hackerone.com/reports/3175928) | Lichess | medium | - | 73 | 2025-06-06 | Improper Input Validation | ImageId Format Injection in Image Upload Endpoint |
| [3168691](https://hackerone.com/reports/3168691) | HackerOne | medium | - | 72 | 2026-04-16 | Improper Input Validation | Residual Malicious Payloads on HackerOne after Vulnerability Fixes |
| [315837](https://hackerone.com/reports/315837) | Mail.ru |  | - | 70 |  | XML External Entities (XXE) | blind XXE in autodiscover parser |
| [2076786](https://hackerone.com/reports/2076786) | inDrive | low | - | 66 | 2024-02-12 | CRLF Injection | Host Header Injection - internal.qa.delivery.indrive.com |
| [3062122](https://hackerone.com/reports/3062122) | Nintendo | critical | - | 65 | 2025-05-15 | Resource Injection | [Xenoblade Chronicles X: Definitive Edition] Unrestricted RPCs allow DoS and writing arbitrary flags remotely |
| [1157795](https://hackerone.com/reports/1157795) | Flickr | medium | - | 64 | 2024-07-06 | Improper Input Validation | Incorrect Deep-link validation leading to unresponsive application and device |
| [2370955](https://hackerone.com/reports/2370955) | HackerOne | none | - | 61 | 2024-05-28 | LLM01: Prompt Injection | LLM03: Training Data Poisoning via ASCII decoding |
| [3125832](https://hackerone.com/reports/3125832) | curl | high | - | 60 | 2025-05-04 | Improper Input Validation | HTTP/3 Stream Dependency Cycle Exploit |
| [52042](https://hackerone.com/reports/52042) | X / xAI |  | - | 59 | 2015-04-21 | CRLF Injection | HTTP Response Splitting (CRLF injection) in report_story |
| [684152](https://hackerone.com/reports/684152) | BlockDev Sp. Z o.o | high | - | 55 | 2019-09-26 | Improper Input Validation | Steal all MKR from `flap` during liquidation by exploiting lack of validation in `flap.kick` |
| [887462](https://hackerone.com/reports/887462) | curl | medium | - | 55 | 2020-12-05 | Improper Input Validation | CVE-2020-8177: curl overwrite local file with -J |
| [1533976](https://hackerone.com/reports/1533976) | GitLab | high | - | 55 | 2022-09-22 | Resource Injection | Content injection in Jira issue title enabling sending arbitrary POST request as victim |
| [2215418](https://hackerone.com/reports/2215418) | LinkedIn | low | - | 55 | 2024-01-29 | Improper Input Validation | Html injection in event Description |
| [758978](https://hackerone.com/reports/758978) | Mail.ru |  | - | 54 |  | XML External Entities (XXE) | XXE на webdav.mail.ru -  PROPFIND/PROPPATCH |
| [1409788](https://hackerone.com/reports/1409788) | GitLab | high | - | 54 | 2022-05-20 | Resource Injection | Arbitrary POST request as victim user from HTML injection in Jupyter notebooks |
| [433996](https://hackerone.com/reports/433996) | QIWI |  | - | 53 |  | XML External Entities (XXE) | XXE on ██████████ by bypassing WAF ████ |
| [965267](https://hackerone.com/reports/965267) | Ruby | low | - | 53 | 2020-10-29 | HTTP Request Smuggling | Potential HTTP Request Smuggling in ruby webrick |
| [3723248](https://hackerone.com/reports/3723248) | Node.js | medium | - | 49 | 2026-07-31 | HTTP Request Smuggling | HTTP Request Smuggling via Connection: close<TAB> in Node.js llhttp parser |
| [1623672](https://hackerone.com/reports/1623672) | Enjin | high | - | 47 | 2024-10-15 | Improper Neutralization of HTTP Headers for Scripting Syntax | Host header injection leads to account takeover |
| [409943](https://hackerone.com/reports/409943) | Node.js | medium | - | 45 | 2020-01-15 | HTTP Response Splitting | Http request splitting |
| [3590586](https://hackerone.com/reports/3590586) | Nextcloud | medium | - | 44 | 2026-04-20 | Resource Injection | position: fixed !important bypasses CSS sanitizer's fixed-position mitigation, enabling full-viewport phishing overlays. |
| [3133379](https://hackerone.com/reports/3133379) | curl | none | - | 42 | 2025-05-08 | CRLF Injection | CRLF Injection in `--proxy-header` allows extra HTTP headers (CWE-93) |
| [3802451](https://hackerone.com/reports/3802451) | Essity | medium | - | 42 | 2026-10-05 | Improper Output Neutralization for Logs | HTML Injection in Contact Form Email Enables Phishing via Legitimate ████████ Infrastructure |
| [99279](https://hackerone.com/reports/99279) | QIWI |  | - | 41 |  | XML External Entities (XXE) | XML External Entity (XXE) in qiwi.com + waf bypass |
| [1095645](https://hackerone.com/reports/1095645) | WordPress | medium | - | 41 | 2021-05-18 | XML External Entities (XXE) | Authenticated XXE |
| [2299069](https://hackerone.com/reports/2299069) | Nextcloud |  | - | 41 | 2024-02-08 | XML External Entities (XXE) | xmlrpc.php &wp-cron.php files are enabled, and will used for (DDOS),(DOS) and broutforce users attack. |
| [798686](https://hackerone.com/reports/798686) | Radancy |  | - | 40 |  | CRLF Injection | x-request-id header reflected in server response without sanitization |
| [1120982](https://hackerone.com/reports/1120982) | U.S. Dept Of Defense | high | - | 40 | 2021-04-20 | HTTP Request Smuggling | HTTP Request Smuggling |
| [188743](https://hackerone.com/reports/188743) | U.S. Dept Of Defense | critical | - | 38 | 2017-01-09 | XML External Entities (XXE) | XXE on DoD web server |
| [679969](https://hackerone.com/reports/679969) | Slack | medium | - | 37 | 2019-11-09 | Improper Input Validation | CSS Injection to disable app & potential message exfil |
| [715949](https://hackerone.com/reports/715949) | U.S. Dept Of Defense | critical | - | 37 | 2023-05-15 | XML External Entities (XXE) | [HTA2] XXE on https://███ via SpellCheck Endpoint. |
| [3702718](https://hackerone.com/reports/3702718) | curl | medium | - | 36 | 2026-04-29 | Improper Input Validation | MQTT state machine confusion: PINGRESP/DISCONNECT with non-zero remaining_length dispatches to stale nextstate |
| [1237700](https://hackerone.com/reports/1237700) | Semrush | medium | - | 35 | 2021-09-01 | Improper Input Validation | Improper input validation in projects leads to fully deny access to project resources |
| [1938106](https://hackerone.com/reports/1938106) | GitHub | medium | - | 35 | 2023-08-01 | Resource Injection | Smuggling content in PR with refs/replace in GitHub |
| [3590583](https://hackerone.com/reports/3590583) | Nextcloud | medium | - | 35 | 2026-04-20 | Resource Injection | Unquoted body background attribute enables CSS injection that bypasses remote image blocking |
| [858650](https://hackerone.com/reports/858650) | Starbucks | medium | - | 34 | 2020-09-01 | CRLF Injection | CRLF injection on www.starbucks.com |
| [762251](https://hackerone.com/reports/762251) | Starbucks | high | - | 32 | 2020-07-22 | XML External Entities (XXE) | Singapore - XXE at https://www.starbucks.com.sg/RestApi/soap11 |
| [1038594](https://hackerone.com/reports/1038594) | U.S. General Services Administration | low | - | 32 | 2021-04-10 | CRLF Injection | CRLF INJECTION |
| [367589](https://hackerone.com/reports/367589) | Starbucks | medium | - | 31 | 2020-03-17 | Improper Input Validation | athome.starbucks.com - URL parameter tampering of review forms permitted possible content injection |
| [53843](https://hackerone.com/reports/53843) | X / xAI |  | - | 30 | 2015-05-04 | CRLF Injection | HTTP Response Splitting (CRLF injection) due to headers overflow |
| [426238](https://hackerone.com/reports/426238) | Mail.ru |  | - | 30 |  | CRLF Injection | [screenshot.mail.ru] CRLF Injection |
| [1446090](https://hackerone.com/reports/1446090) | Krisp | medium | - | 30 | 2022-06-20 | Improper Input Validation | Add more seats by paying less via PUT /v2/seats request manipulation |
| [3621606](https://hackerone.com/reports/3621606) | Monero | medium | - | 30 | 2026-07-24 | CRLF Injection | ZMQ RPC Log Injection and Untrusted Payload Persistence |
| [3623064](https://hackerone.com/reports/3623064) | curl | low | - | 30 | 2026-03-25 | HTTP Request Smuggling | HTTP/1.1 Response Desynchronization via conflicting CL/TE headers in Proxy CONNECT |
| [3648681](https://hackerone.com/reports/3648681) | Node.js | medium | - | 30 | 2026-07-01 | HTTP Request Smuggling | Improper Input Validation — HTTP Response Parser Unconditionally Accepts Bare CR in Status Line |
| [955170](https://hackerone.com/reports/955170) | QIWI |  | - | 29 |  | HTTP Request Smuggling | HTTP Request Smuggling on api.flocktory.com Leads to XSS on Customer Sites |
| [587727](https://hackerone.com/reports/587727) | phpBB | medium | - | 28 | 2019-09-26 | Resource Injection | CSS injection via BB code tag "█████" |
| [919175](https://hackerone.com/reports/919175) | Basecamp | critical | - | 28 | 2020-10-28 | HTTP Request Smuggling | HTTP request smuggling on Basecamp 2 allows web cache poisoning |
| [1271276](https://hackerone.com/reports/1271276) | Mail.ru |  | - | 28 |  | CRLF Injection | [play.skillbox.ru] CRLF Injection |
| [3413764](https://hackerone.com/reports/3413764) | Revive Adserver | medium | - | 28 | 2025-11-19 | Improper Neutralization of Whitespace | Username normalization missing allows visually indistinguishable accounts (Whitespace-Based Impersonation) |
| [867577](https://hackerone.com/reports/867577) | Basecamp | critical | - | 27 | 2020-10-28 | HTTP Request Smuggling | Unauthenticated request smuggling on launchpad.37signals.com |
| [1098948](https://hackerone.com/reports/1098948) | Kartpay | medium | - | 27 | 2021-05-10 | HTTP Request Smuggling | Host Header Injection |
| [1509216](https://hackerone.com/reports/1509216) | Nextcloud | medium | - | 27 | 2022-12-27 | CRLF Injection | SMTP Command Injection in Appointment Emails via Newlines |
| [335339](https://hackerone.com/reports/335339) | Slack | medium | - | 26 | 2018-07-19 | Resource Injection | HTTP parameter pollution from outdated Greenhouse.io JS dependency |
| [3608522](https://hackerone.com/reports/3608522) | curl | low | - | 26 | 2026-03-17 | Improper Neutralization of Escape, Meta, or Control Sequences | Unescaped username in SASL DIGEST-MD5 response allows injection |
| [3630310](https://hackerone.com/reports/3630310) | curl | high | - | 26 | 2026-03-29 | Improper Input Validation | HTTP/2 server push accepts a non-authoritative :scheme=https over cleartext h2c, enabling HTTPS cache-key poisoning |
| [4025056](https://hackerone.com/reports/4025056) | curl | medium | - | 26 | 2026-09-19 | HTTP Request Smuggling | HTTP/1.1 response framing violation and unsafe connection reuse when transfer decoding is disabled |
| [526880](https://hackerone.com/reports/526880) | U.S. Dept Of Defense | high | - | 25 | 2019-10-08 | HTTP Request Smuggling | Request smuggling on ████████ |
| [742808](https://hackerone.com/reports/742808) | Evernote | critical | - | 25 | 2020-10-27 | XML External Entities (XXE) | Non-production Open Database In Combination With XXE Leads To SSRF |
| [745953](https://hackerone.com/reports/745953) | Chaturbate | low | - | 25 | 2019-12-18 | Improper Neutralization of Escape, Meta, or Control Sequences | Camo Image Proxy Bypass with CSS Escape Sequences |
| [1639364](https://hackerone.com/reports/1639364) | U.S. Dept Of Defense | medium | - | 25 | 2024-07-19 | Improper Input Validation | Local File Inclusion in download.php |
| [2017600](https://hackerone.com/reports/2017600) | GitHub | medium | - | 25 | 2023-11-29 | Resource Injection | Git Reference Ambiguity in GitHub - Commit Smuggling, Account Takeover, and Remote Code Execution |
| [237357](https://hackerone.com/reports/237357) | Snapchat | medium | - | 24 | 2017-06-15 | CRLF Injection | CRLF Injection at vpn.bitstrips.com |
| [2174818](https://hackerone.com/reports/2174818) | Cloudflare Public Bug Bounty | low | - | 24 | 2023-11-10 | Resource Injection | YAML schema injection risk in Swagger UI via schema_url parameter at developers.cloudflare.com |
| [3479203](https://hackerone.com/reports/3479203) | curl | critical | - | 24 | 2025-12-27 | CRLF Injection | HTTP/3 Protocol Smuggling and Header Injection via CRLF in QPACK value conversion |
| [192749](https://hackerone.com/reports/192749) | Starbucks | medium | - | 23 | 2017-03-09 | HTTP Response Splitting | [newscdn.starbucks.com] CRLF Injection, XSS |
| [3249936](https://hackerone.com/reports/3249936) | curl | medium | - | 23 | 2025-07-13 | HTTP Request Smuggling | HTTP Request Smuggling Vulnerability Analysis - cURL Security Report |
| [3708482](https://hackerone.com/reports/3708482) | curl | medium | - | 23 | 2026-05-06 | Improper Neutralization of Value Delimiters | wcurl treats some URL operands after -- as curl options |
| [1516377](https://hackerone.com/reports/1516377) | Nextcloud | medium | - | 22 | 2022-07-04 | CRLF Injection | SMTP Command Injection in iCalendar Attachments to Emails via Newlines |
| [2251074](https://hackerone.com/reports/2251074) | Nextcloud | medium | - | 22 | 2024-01-18 | Improper Handling of URL Encoding (Hex Encoding) | Improper handling of request URLs in nextcloud/guests allows guest users to bypass app allowlist |
| [2297561](https://hackerone.com/reports/2297561) | U.S. Dept Of Defense | medium | - | 22 | 2024-03-22 | Resource Injection | Resource Injection - [████████] |
| [2814750](https://hackerone.com/reports/2814750) | curl | low | - | 22 | 2025-09-26 | Improper Input Validation | Inconsistent URL Parsing in curl Leading to Potential SSRF and Access Control Bypass |
| [217058](https://hackerone.com/reports/217058) | HackerOne |  | - | 21 | 2017-05-03 | CRLF Injection | CRLF injection in info.hacker.one |
| [2573567](https://hackerone.com/reports/2573567) | U.S. Dept Of Defense | high | - | 21 | 2024-07-19 | XML External Entities (XXE) | XML External Entity (XXE) Injection |
| [3235428](https://hackerone.com/reports/3235428) | curl | medium | - | 21 | 2025-07-03 | CRLF Injection | CRLF injection in libcurl's SMTP client via --mail-from and --mail-rcpt allows SMTP command smuggling |
| [3793495](https://hackerone.com/reports/3793495) | curl | low | - | 21 | 2026-06-15 | HTTP Request Smuggling | Incomplete Suppression of  Transfer-Encoding: chunked Header in HTTP/2 After Redirect From HTTP/1.1 |
| [231508](https://hackerone.com/reports/231508) | Cuvva |  | - | 20 |  | CRLF Injection | CRLF Injection [vpn.corp.cuvva.com] |
| [648434](https://hackerone.com/reports/648434) | Internet Bug Bounty | critical | - | 20 | 2019-11-12 | HTTP Request Smuggling | Multiple HTTP Smuggling reports |
| [1166073](https://hackerone.com/reports/1166073) | UPchieve | low | - | 20 | 2022-06-15 | Improper Input Validation | Hyper Link Injection while signup |
| [1528242](https://hackerone.com/reports/1528242) | Stripe | low | - | 20 | 2022-05-18 | Improper Input Validation | Bypass global deny-lists by wrapping domains using "[]" in https://github.com/stripe/smokescreen |
| [3473384](https://hackerone.com/reports/3473384) | curl | low | - | 20 | 2025-12-21 | Improper Input Validation | Functional Regression in Digest Authentication: Failure to handle optional spaces and escaped quotes |
| [3477023](https://hackerone.com/reports/3477023) | curl | high | - | 20 | 2025-12-25 | CRLF Injection | Protocol Smuggling / CRLF Injection via Gopher Protocol allows Arbitrary Command Injection |
| [3481849](https://hackerone.com/reports/3481849) | curl |  | - | 20 | 2025-12-30 | HTTP Response Splitting | HTTP/2 and HTTP/3 Header Injection in curl |
| [3741744](https://hackerone.com/reports/3741744) | curl | none | - | 20 | 2026-06-11 | CRLF Injection | CRLF Injection via Custom HTTP Headers |
| [1073485](https://hackerone.com/reports/1073485) | Mail.ru |  | - | 19 |  | Resource Injection | [Biz] [Mailer] Кроп любых* изображений расположенных на сервере |
| [1762025](https://hackerone.com/reports/1762025) | GitHub | medium | - | 19 | 2023-03-09 | Resource Injection | Improper handling of null bytes in GitHub Actions Runner allows an attacker to set arbitrary environment variables |
| [3911605](https://hackerone.com/reports/3911605) | curl | medium | - | 19 | 2026-08-03 | CRLF Injection | SMTP CRLF injection in custom SMTP recipient operand allows additional SMTP commands after authentication |
| [97292](https://hackerone.com/reports/97292) | HackerOne |  | - | 18 | 2015-12-02 | CRLF Injection | HTTP header injection in info.hackerone.com allows setting cookies for hackerone.com |
| [232614](https://hackerone.com/reports/232614) | Weblate | high | - | 18 | 2017-06-02 | XML External Entities (XXE) | Uploaded XLF files result in External Entity Execution |
| [770548](https://hackerone.com/reports/770548) | 8x8 | high | - | 18 | 2020-04-10 | Improper Input Validation | Insecure OAuth redirection at [admin.8x8.vc] |
| [1081367](https://hackerone.com/reports/1081367) | QIWI |  | - | 18 |  | CRLF Injection | crlf injection на https://bug.qiwi.com |
| [1321070](https://hackerone.com/reports/1321070) | Adobe |  | - | 18 |  | XML External Entities (XXE) | AEM forms XXE Vulnerability |
| [1631228](https://hackerone.com/reports/1631228) | Stripo Inc | medium | - | 18 | 2024-02-15 | HTTP Request Smuggling | [demo.stripo.email] HTTP request Smuggling |
| [2237099](https://hackerone.com/reports/2237099) | Node.js | medium | - | 18 | 2024-05-03 | HTTP Request Smuggling | HTTP Request Smuggling via Content Length Obfuscation |
| [3387499](https://hackerone.com/reports/3387499) | curl |  | - | 18 | 2025-10-17 | CRLF Injection | SMTP Command Injection Vulnerability in libcurl 8.16.0 via RFC 3461 Suffix |
| [3641893](https://hackerone.com/reports/3641893) | curl | low | - | 18 | 2026-04-03 | Improper Input Validation | Cookie attribute TAB injection regression in Set-Cookie parsing |
| [3785919](https://hackerone.com/reports/3785919) | curl | high | - | 18 | 2026-06-08 | HTTP Response Splitting | libcurl: HTTP/1.x bare LF byte in response header value enables cookie jar pollution and POST body/credential exfiltration via redirect — RC=0, curl 8 |
| [3795615](https://hackerone.com/reports/3795615) | curl | medium | - | 18 | 2026-06-13 | HTTP Request Smuggling | Duplicate chunked Transfer-Encoding lets a malicious origin smuggle a response across reused HTTP proxy connections |
| [4023506](https://hackerone.com/reports/4023506) | curl | low | - | 18 | 2026-09-15 | CRLF Injection | libcurl LDAP LDIF: entry DN and attribute names written without RFC 2849 base64 encoding, allowing server line injection |
| [145128](https://hackerone.com/reports/145128) | Ubiquiti Inc. | low | - | 17 | 2017-03-31 | CRLF Injection | [account-global.ubnt.com] CRLF Injection |
| [415137](https://hackerone.com/reports/415137) | h1-5411-CTF |  | - | 17 | 2018-10-22 | Resource Injection | H1-5411 CTF Write-up by erbbysam and ziot |
| [601192](https://hackerone.com/reports/601192) | Shopify | low | - | 17 | 2019-07-04 | Resource Injection | HTML injection in https://interviewing.shopify.com/index.php?candidate= |
| [715996](https://hackerone.com/reports/715996) | X / xAI | high | - | 17 | 2020-11-18 | HTTP Request Smuggling | http request smuggling in  twitter.com |
| [812907](https://hackerone.com/reports/812907) | Urban Dictionary | medium | - | 17 | 2020-07-08 | CRLF Injection | Bypass voting restriction due to HTTP Header Injection |
| [1183335](https://hackerone.com/reports/1183335) | Stripe | low | - | 17 | 2023-03-06 | Resource Injection | Object injection in `stripe-billing-typographic` GitHub project via /auth/login |
| [1218708](https://hackerone.com/reports/1218708) | h1-ctf | critical | - | 17 | 2021-06-21 | XML External Entities (XXE) | HackerOne’s 100K CTF Writeup |
| [3584865](https://hackerone.com/reports/3584865) | curl | medium | - | 17 | 2026-03-08 | Improper Neutralization of Value Delimiters | In curl's SASL OAUTHBEARER authentication, including the SOH character (0x01) in the username corrupts the message structure. |
| [3963494](https://hackerone.com/reports/3963494) | curl | medium | - | 17 | 2026-08-24 | CRLF Injection | RTSP CRLF injection in libcurl allows CURLOPT_RTSP_* values to inject commands into independent sessions |
| [476257](https://hackerone.com/reports/476257) | MariaDB | medium | - | 16 | 2019-02-21 | CRLF Injection | CRLF injection at https://mariadb.org/. |
| [1063627](https://hackerone.com/reports/1063627) | Acronis | low | - | 16 | 2021-11-16 | HTTP Request Smuggling | HTTP Request Smuggling on https://consumer.acronis.com |
| [1217114](https://hackerone.com/reports/1217114) | h1-ctf | critical | - | 16 | 2021-06-21 | XML External Entities (XXE) | CCC H1 June 2021 CTF Writeup |
| [1610316](https://hackerone.com/reports/1610316) | TikTok | low | - | 16 | 2023-06-22 | Improper Input Validation | Improper user validation on mentions and hashtags |
| [3481595](https://hackerone.com/reports/3481595) | curl | medium | - | 16 | 2025-12-29 | CRLF Injection | SMTP CRLF Injection & Protocol Desynchronization in libcurl |
| [3564941](https://hackerone.com/reports/3564941) | Node.js | low | - | 16 | 2026-08-28 | HTTP Request Smuggling | HTTP Request Smuggling via Silent Header Truncation in Node.js HTTP Parser |
| [4098761](https://hackerone.com/reports/4098761) | curl | medium | - | 16 | 2026-10-15 | HTTP Request Smuggling | HTTP/1.1 connection reuse returns unsolicited server data as the next request's response (regression in 8.22.0) |
| [4113412](https://hackerone.com/reports/4113412) | curl | low | - | 16 | 2026-10-17 | Improper Input Validation | libcurl RTSP `CURLOPT_CRLF` conversion allows a request body to become a second RTSP request |
| [315865](https://hackerone.com/reports/315865) | Coinbase |  | - | 15 | 2018-04-02 | Resource Injection | Stored CSS Injection |
| [415202](https://hackerone.com/reports/415202) | h1-5411-CTF | critical | - | 15 | 2018-10-22 | XML External Entities (XXE) | Flag WriteUp |
| [777651](https://hackerone.com/reports/777651) | Stripo Inc | high | - | 15 | 2020-04-10 | HTTP Request Smuggling | HTTP Request Smuggling on my.stripo.email |
| [838647](https://hackerone.com/reports/838647) | WHO COVID-19 Mobile App | low | - | 15 | 2020-12-22 | Improper Input Validation | Improper Input Validation on User's Location on PUT /WhoService/putLocation Could Affect Availability/Falsify Users |
| [3295656](https://hackerone.com/reports/3295656) | curl | high | - | 15 | 2025-08-12 | Improper Input Validation | Unsafe Global IFS Modification in OS400 Shell Script Enables Command Injection and Parsing Flaws (CWE-78/CWE-20) |
| [66391](https://hackerone.com/reports/66391) | Yelp |  | - | 14 | 2017-11-09 | CRLF Injection | [engineeringblog.yelp.com] CRLF Injection |
| [165102](https://hackerone.com/reports/165102) | Internet Bug Bounty |  | - | 14 | 2016-09-01 | CRLF Injection | urllib HTTP header injection CVE-2016-5699 |
| [767097](https://hackerone.com/reports/767097) | Genasys Technologies |  | - | 14 |  | Improper Input Validation | Improper Input Validation on payment page |
| [824753](https://hackerone.com/reports/824753) | Internet Bug Bounty | high | - | 14 | 2021-08-26 | Improper Handling of URL Encoding (Hex Encoding) | Cache Poisoning |
| [845832](https://hackerone.com/reports/845832) | Lab45 | low | - | 14 | 2020-08-14 | XML Injection | SVG file upload leads to XML injection |
| [893085](https://hackerone.com/reports/893085) | 8x8 | high | - | 14 | 2020-10-21 | Improper Input Validation | 2FA Disable With Wrong Password - Response Tampering. |
| [1943013](https://hackerone.com/reports/1943013) | Mars | low | - | 14 | 2023-06-23 | CRLF Injection | CRLF Inection at `██████████` |
| [3509396](https://hackerone.com/reports/3509396) | curl | low | - | 14 | 2026-01-14 | Improper Input Validation | IMAP Protocol Desynchronization and Response Smuggling via Naive Literal Parsing |
| [3627638](https://hackerone.com/reports/3627638) | curl |  | - | 14 | 2026-03-26 | CRLF Injection | Security Vulnerability Report: Protocol Injection via Programmatic Options |
| [257207](https://hackerone.com/reports/257207) | Legal Robot | low | - | 13 | 2017-08-12 | Resource Injection | Code injection |
| [726765](https://hackerone.com/reports/726765) | Mail.ru |  | - | 13 |  | HTTP Response Splitting | HTTP-Response-Splitting leads to information disclosure (email, firstname, lastname) at https://tz.mail.ru |
| [1150799](https://hackerone.com/reports/1150799) | U.S. Dept Of Defense | high | - | 13 | 2021-06-15 | XML Injection | XML Injection / External Service Interaction (HTTP/DNS) On https://█████████.mil |
| [1613943](https://hackerone.com/reports/1613943) | curl | low | - | 13 | 2022-08-31 | Improper Input Validation | CVE-2022-35252: control code in cookie denial of service |
| [3823932](https://hackerone.com/reports/3823932) | curl | medium | - | 13 | 2026-06-26 | CRLF Injection | CURLOPT_HAPROXY_CLIENT_IP lacks input validation, enabling HAProxy PROXY protocol injection |
| [276427](https://hackerone.com/reports/276427) | Legal Robot | none | - | 12 | 2017-10-21 | CRLF Injection | Legal Robot |
| [335599](https://hackerone.com/reports/335599) | Mail.ru |  | - | 12 |  | CRLF Injection | CRLF injection mcs.mail.ru (leads to XSS) |
| [413115](https://hackerone.com/reports/413115) | 8x8 | medium | - | 12 | 2020-06-26 | CRLF Injection | CRLF injection agentcrm.8x8.com |
| [866382](https://hackerone.com/reports/866382) | Brave Software | high | - | 12 | 2020-06-04 | HTTP Request Smuggling | HTTP Request Smuggling |
| [1063493](https://hackerone.com/reports/1063493) | Acronis | low | - | 12 | 2021-11-16 | HTTP Request Smuggling | HTTP Request Smuggling on https://promosandbox.acronis.com |
| [1164452](https://hackerone.com/reports/1164452) | MTN Group | critical | - | 12 | 2022-09-01 | Improper Input Validation | Remote code execution due to unvalidated file upload |
| [244459](https://hackerone.com/reports/244459) | Internet Bug Bounty | medium | - | 11 | 2017-07-11 | HTTP Request Smuggling | Apache HTTP Request Parsing Whitespace Defects |
| [385239](https://hackerone.com/reports/385239) | Chaturbate | low | - | 11 | 2018-10-19 | Improper Input Validation | Add non-existent room moderator |
| [423437](https://hackerone.com/reports/423437) | Shopify | none | - | 11 | 2019-04-05 | Improper Input Validation | H1514 Shopify API ruby SDK session setup lacks input validation, resulting in SSRF and leakage of client secret |
| [471087](https://hackerone.com/reports/471087) | RATELIMITED | high | - | 11 | 2018-12-21 | HTTP Request Smuggling | Hackerone1 |
| [730779](https://hackerone.com/reports/730779) | Node.js | high | - | 11 | 2020-02-24 | Improper Input Validation | HTTP header values do not have trailing OWS trimmed |
| [1054282](https://hackerone.com/reports/1054282) | ownCloud | low | - | 11 | 2021-09-03 | CRLF Injection | Protocol Smuggling over LDAP password field |
| [1290872](https://hackerone.com/reports/1290872) | Twitter Algorithmic Bias | critical | - | 11 | 2021-09-08 | Improper Input Validation | Economic Harm through Twitter's Cropping Algorithm |
| [1820955](https://hackerone.com/reports/1820955) | Node.js | medium | - | 11 | 2023-02-22 | CRLF Injection | CRLF Injection in Nodejs ‘undici’ via host |
| [3414088](https://hackerone.com/reports/3414088) | curl | medium | - | 11 | 2025-11-10 | CRLF Injection | SMTP CRLF Command Injection in CURLOPT_MAIL_FROM and CURLOPT_MAIL_RCPT |
| [4027511](https://hackerone.com/reports/4027511) | curl | medium | - | 11 | 2026-09-14 | Improper Handling of URL Encoding (Hex Encoding) | Encoded slash traversal in the IPFS/IPNS URL rewrite escapes the configured gateway namespace |
| [39181](https://hackerone.com/reports/39181) | Vimeo |  | - | 10 | 2016-10-24 | CRLF Injection | [vimeopro.com] CRLF Injection |
| [643225](https://hackerone.com/reports/643225) | JamieWeb | medium | - | 10 | 2020-03-09 | HTTP Request Smuggling | HTTP Request Smuggling |
| [726117](https://hackerone.com/reports/726117) | curl | none | - | 10 | 2021-01-17 | Improper Input Validation | SMB access smuggling via FILE URL on Windows |
| [737315](https://hackerone.com/reports/737315) | Radancy |  | - | 10 |  | Resource Injection | 'X-Forwarded-Host' key used in input without sanitation - possible cache poisoning |
| [1294062](https://hackerone.com/reports/1294062) | Twitter Algorithmic Bias | critical | - | 10 | 2021-09-08 | Improper Input Validation | Underrepresentation Bias through Twitter's Cropping Algorithm |
| [3403880](https://hackerone.com/reports/3403880) | curl | medium | - | 10 | 2025-10-29 | Improper Input Validation | Logical Flaw in curl_url_set Leads to Inconsistent Query Parameter Encoding |
| [3414079](https://hackerone.com/reports/3414079) | U.S. Dept Of Defense | critical | - | 10 | 2026-01-12 | File Content Injection | DNN - Unrestricted Arbitrary File Upload #████████ |
| [501585](https://hackerone.com/reports/501585) | Monero | critical | - | 9 | 2019-07-03 | Resource Injection | Zero-amount miner TX + RingCT allows monero wallet to receive arbitrary amount of monero |
| [710654](https://hackerone.com/reports/710654) | U.S. Dept Of Defense | high | - | 9 | 2024-07-19 | XML External Entities (XXE) | XXE with RCE potential on the https://█████████ (CVE-2017-3548) |
| [840688](https://hackerone.com/reports/840688) | 8x8 | high | - | 9 | 2020-08-05 | Improper Input Validation | Send Phishing/Spam email from [REDACTED_EMAIL] to any email address. |
| [997381](https://hackerone.com/reports/997381) | U.S. Dept Of Defense | high | - | 9 | 2021-04-02 | XML Injection | XML Injection on https://www.█████████ (███ parameter) |
| [1156748](https://hackerone.com/reports/1156748) | Elastic | critical | - | 9 | 2021-04-29 | XML External Entities (XXE) | XXE in Enterprise Search's App Search web crawler |
| [1168205](https://hackerone.com/reports/1168205) | Ruby | high | - | 9 | 2022-02-04 | CRLF Injection | 'net/http': HTTP Header Injection in the set_content_type method |
| [1524692](https://hackerone.com/reports/1524692) | Node.js | medium | - | 9 | 2022-07-07 | HTTP Request Smuggling | HTTP Request Smuggling Due To Improper Delimiting of Header Fields |
| [3484431](https://hackerone.com/reports/3484431) | curl | high | - | 9 | 2026-01-02 | HTTP Request Smuggling | HTTP Request Smuggling and SSRF via CRLF Injection in Curl_add_custom_headers |
| [3484506](https://hackerone.com/reports/3484506) | curl | medium | - | 9 | 2026-01-02 | CRLF Injection | CRLF Injection in Gopher Protocol (`lib/gopher.c`) |
| [3633534](https://hackerone.com/reports/3633534) | curl | medium | - | 9 | 2026-03-30 | CRLF Injection | CRLF Injection in HAProxy PROXY Protocol via CURLOPT_HAPROXY_CLIENT_IP allows IP spoofing and protocol injection |
| [25275](https://hackerone.com/reports/25275) | Greenhouse.io |  | - | 8 | 2016-11-02 | CRLF Injection | [greenhouse.io] CRLF Injection / Insecure nginx configuration |
| [214763](https://hackerone.com/reports/214763) | Rockstar Games | low | - | 8 | 2017-05-23 | Failure to Sanitize Special Elements into a Different Plane (Special Element Injection) | Profile bio at rockstar is accepting control characters |
| [225936](https://hackerone.com/reports/225936) | U.S. Dept Of Defense | low | - | 8 | 2017-08-15 | CRLF Injection | Cross-site scripting (XSS) vulnerability on a DoD website |
| [232327](https://hackerone.com/reports/232327) | Ubiquiti Inc. | medium | - | 8 | 2017-07-04 | CRLF Injection | CRLF Injection on openvpn.svc.ubnt.com |
| [232330](https://hackerone.com/reports/232330) | U.S. Dept Of Defense | high | - | 8 | 2017-08-15 | XML External Entities (XXE) | Remote Code Execution (RCE) vulnerability in a DoD website |
| [234758](https://hackerone.com/reports/234758) | Mixmax | low | - | 8 | 2017-06-06 | CRLF Injection | CRLF Injection on https://vpn.mixmax.com |
| [241231](https://hackerone.com/reports/241231) | Rockstar Games | medium | - | 8 | 2017-08-25 | Resource Injection | flash injection in http://www.rockstargames.com/IV/imgPlayer/imageEmbed.swf |
| [838682](https://hackerone.com/reports/838682) | Mail.ru |  | - | 8 |  | HTTP Response Splitting | Http Response Splitting on  thumb.cloud.mail.ru |
| [906959](https://hackerone.com/reports/906959) | Node.js third-party modules | critical | - | 8 | 2020-08-22 | LDAP Injection | [cloudron-surfer] Denial of Service via LDAP Injection |
| [1025575](https://hackerone.com/reports/1025575) | Node.js third-party modules | medium | - | 8 | 2020-12-10 | HTTP Request Smuggling | Default behavior of Fastifys versioned routes can be used for cache poisoning when Fastify is used in combination with a http cache / CDN |
| [1064149](https://hackerone.com/reports/1064149) | WHO COVID-19 Mobile App | medium | - | 8 | 2021-01-12 | Improper Input Validation | Improper Input Validation on User's Location on PUT /WhoService/putLocation Could Affect Availability/Falsify Users |
| [1204695](https://hackerone.com/reports/1204695) | Ruby | high | - | 8 | 2022-11-24 | HTTP Response Splitting | RubyのCGIライブラリにHTTPレスポンス分割（HTTPヘッダインジェクション）があり、秘密情報が漏洩する |
| [1402249](https://hackerone.com/reports/1402249) | Nextcloud | medium | - | 8 | 2022-05-27 | CRLF Injection | Control character filtering misses leading and trailing whitespace in file and folder names |
| [1565619](https://hackerone.com/reports/1565619) | Internet Bug Bounty | medium | - | 8 | 2022-06-11 | Improper Input Validation | CVE-2022-27780: percent-encoded path separator in URL host |
| [1686935](https://hackerone.com/reports/1686935) | Internet Bug Bounty | low | - | 8 | 2022-11-05 | Improper Input Validation | CVE-2022-35252: control code in cookie denial of service |
| [2001873](https://hackerone.com/reports/2001873) | Node.js | medium | - | 8 | 2023-06-20 | HTTP Request Smuggling | HTTP Request Smuggling via Empty headers separated by CR |
| [2564265](https://hackerone.com/reports/2564265) | U.S. Dept Of Defense | high | - | 8 | 2026-01-12 | XML External Entities (XXE) | XML E██████ternal Entity (XXE) Injection in ███ |
| [2864414](https://hackerone.com/reports/2864414) | curl | high | - | 8 | 2025-07-07 | Improper Input Validation | Arbitrary File Deletion Vulnerability in curl Source Code via os.unlink() |
| [3418616](https://hackerone.com/reports/3418616) | curl | critical | - | 8 | 2025-11-10 | CRLF Injection | SMTP CRLF Injection in curl/libcurl via MAIL FROM/RCPT TO parameters |
| [3460184](https://hackerone.com/reports/3460184) | curl | low | - | 8 | 2025-12-11 | Improper Neutralization of Escape, Meta, or Control Sequences | Terminal Output Not Great |
| [3508799](https://hackerone.com/reports/3508799) | curl | low | - | 8 | 2026-01-14 | HTTP Response Splitting | Digest Authentication Header Injection |
| [39261](https://hackerone.com/reports/39261) | Dropbox |  | - | 7 |  | CRLF Injection | [monitor.sjc.dropbox.com] CRLF Injection |
| [114198](https://hackerone.com/reports/114198) | Mail.ru |  | - | 7 |  | CRLF Injection | [touch.lady.mail.ru] CRLF Injection |
| [154306](https://hackerone.com/reports/154306) | ownCloud |  | - | 7 | 2016-11-02 | CRLF Injection | [api.owncloud.org] CRLF Injection |
| [175529](https://hackerone.com/reports/175529) | Brave Software | medium | - | 7 | 2016-10-15 | HTTP Response Splitting | URI Obfuscation |
| [359290](https://hackerone.com/reports/359290) | U.S. Dept Of Defense | medium | - | 7 | 2019-12-02 | LDAP Injection | LDAP Injection at ██████ |
| [449627](https://hackerone.com/reports/449627) | Mail.ru |  | - | 7 |  | XML External Entities (XXE) | XXE крит |
| [481512](https://hackerone.com/reports/481512) | MariaDB | medium | - | 7 | 2019-02-04 | CRLF Injection | CRLF injection on https://buildbot.mariadb.org |
| [914801](https://hackerone.com/reports/914801) | Engel & Völkers Technology GmbH |  | - | 7 |  | XML External Entities (XXE) | XXE on www.publish.engelvoelkers.com |
| [1501679](https://hackerone.com/reports/1501679) | Node.js | medium | - | 7 | 2022-07-07 | HTTP Request Smuggling | HTTP Request Smuggling Due to Incorrect Parsing of Multi-line Transfer-Encoding |
| [1524555](https://hackerone.com/reports/1524555) | Node.js | medium | - | 7 | 2022-07-07 | HTTP Request Smuggling | HTTP Request Smuggling Due to Flawed Parsing of Transfer-Encoding |
| [1889474](https://hackerone.com/reports/1889474) | Internet Bug Bounty | high | - | 7 | 2023-04-09 | CRLF Injection | Ruby's CGI library has HTTP response splitting (HTTP header injection), leaking confidential information |
| [181939](https://hackerone.com/reports/181939) | Mail.ru |  | - | 6 |  | HTTP Response Splitting | [qpt.mail.ru] CRLF Injection / Open Redirect |
| [205796](https://hackerone.com/reports/205796) | Mail.ru |  | - | 6 |  | HTTP Response Splitting | CRLF инъекция на https://tz.mail.ru |
| [361189](https://hackerone.com/reports/361189) | Liberapay | none | - | 6 | 2018-06-03 | Resource Injection | Anyone can register organization legal type as "Soletrader" |
| [490997](https://hackerone.com/reports/490997) | MariaDB | medium | - | 6 | 2019-02-14 | CRLF Injection | [downloads.mariadb.org] CRLF injection in case of encoded query mark |
| [496293](https://hackerone.com/reports/496293) | Node.js third-party modules | high | - | 6 | 2020-01-27 | Improper Input Validation | [url-parse] Improper Validation and Sanitization |
| [753547](https://hackerone.com/reports/753547) | Polymail, Inc. |  | - | 6 |  | Improper Input Validation | Bug in OAuth Success Redirect URI Validation |
| [888176](https://hackerone.com/reports/888176) | Ruby on Rails |  | - | 6 | 2021-06-15 | Improper Neutralization of HTTP Headers for Scripting Syntax | HTTP Host injection in redirect_to function |
| [1204977](https://hackerone.com/reports/1204977) | Ruby | low | - | 6 | 2022-11-24 | HTTP Response Splitting | CGI::Cookieクラスにおけるセキュリティ上好ましくない仕様および実装 |
| [1294242](https://hackerone.com/reports/1294242) | Twitter Algorithmic Bias | critical | - | 6 | 2021-09-08 | Improper Input Validation | Underrepresentation Bias through Twitter's Cropping Algorithm #2: Favoring Animals over Black People |
| [1339787](https://hackerone.com/reports/1339787) | GitHub Security Lab |  | - | 6 |  | XML External Entities (XXE) | [Java]: Add XXE sinks |
| [1664019](https://hackerone.com/reports/1664019) | Internet Bug Bounty | medium | - | 6 | 2022-09-23 | CRLF Injection | CVE-2022-35948: CRLF Injection in Nodejs ‘undici’ via Content-Type |
| [1665156](https://hackerone.com/reports/1665156) | Node.js | medium | - | 6 | 2022-10-26 | HTTP Request Smuggling | HTTP Request Smuggling Due to Incorrect Parsing of Multi-line Transfer-Encoding (improper fix for CVE-2022-32215) |
| [1675191](https://hackerone.com/reports/1675191) | Node.js | medium | - | 6 | 2022-10-26 | HTTP Request Smuggling | HTTP Request Smuggling Due to Incorrect Parsing of Header Fields |
| [2831558](https://hackerone.com/reports/2831558) | curl |  | - | 6 | 2025-07-07 | CRLF Injection | netrc crlf injection |
| [3451305](https://hackerone.com/reports/3451305) | curl |  | - | 6 | 2025-12-04 | CRLF Injection | SMTP Protocol Injection via CRLF in CURLOPT_MAIL_FROM leading to Email Spoofing |
| [4121675](https://hackerone.com/reports/4121675) | curl | high | - | 6 | 2026-10-18 | CRLF Injection | CRLF injection in the RTSP request-line and Transport header via `CURLOPT_RTSP_STREAM_URI` and `CURLOPT_RTSP_TRANSPORT` |
| [4121689](https://hackerone.com/reports/4121689) | curl | high | - | 6 | 2026-10-18 | CRLF Injection | CRLF injection in the HTTP request-line via `CURLOPT_REQUEST_TARGET` (`--request-target`) |
| [15492](https://hackerone.com/reports/15492) | Mail.ru |  | - | 5 |  | CRLF Injection | [corp.mail.ru] CRLF Injection / Insecure nginx configuration |
| [154275](https://hackerone.com/reports/154275) | ownCloud |  | - | 5 | 2016-11-02 | CRLF Injection | [doc.owncloud.org] CRLF Injection |
| [277354](https://hackerone.com/reports/277354) | Inflection | none | - | 5 | 2017-11-01 | HTTP Response Splitting | HTTP Host Header Injection on app.goodhire.com |
| [1223565](https://hackerone.com/reports/1223565) | curl | high | - | 5 | 2021-07-21 | Improper Input Validation | CVE-2021-22924: Bad connection reuse due to flawed path name checks |
| [1630336](https://hackerone.com/reports/1630336) | Node.js | medium | - | 5 | 2022-10-26 | HTTP Request Smuggling | CVE-2022-32213 bypass via obs-fold mechanic |
| [1707977](https://hackerone.com/reports/1707977) | Nextcloud | low | - | 5 | 2022-11-25 | Resource Injection | XSS in Desktop Client via user status and information |
| [1711847](https://hackerone.com/reports/1711847) | Nextcloud | low | - | 5 | 2022-11-25 | Resource Injection | XSS in Desktop Client in call notification popup |
| [1718757](https://hackerone.com/reports/1718757) | Ruby | none | - | 5 | 2023-05-04 | CRLF Injection | Header CRLF Injection in Ruby Net::HTTP |
| [2861797](https://hackerone.com/reports/2861797) | curl |  | - | 5 | 2025-07-07 | CRLF Injection | curl mishandles `%0c%0b` sequences in HTTP responses leading to CRLF confusions, Headers and Cookies Injection |
| [3479984](https://hackerone.com/reports/3479984) | curl | critical | - | 5 | 2025-12-28 | CRLF Injection | CRLF Injection / Protocol Smuggling in libcurl via CURLOPT_USERNAME (IMAP) |
| [3505557](https://hackerone.com/reports/3505557) | curl | none | - | 5 | 2026-01-10 | CRLF Injection | CRLF Injection in HTTP header values allows arbitrary header injection |
| [3651975](https://hackerone.com/reports/3651975) | curl |  | - | 5 | 2026-04-06 | CRLF Injection | SMTP Command Injection via CRLF in libcurl MAIL_FROM / MAIL_RCPT (lib/smtp.c) |
| [4123654](https://hackerone.com/reports/4123654) | curl | low | - | 5 | 2026-10-19 | CRLF Injection | SCP upload with --crlf sends more bytes than the size declared to the server (same class curl refused for IMAP CVE-2026-87864 and RTSP) |
| [4124486](https://hackerone.com/reports/4124486) | curl | low | - | 5 | 2026-10-19 | CRLF Injection | RTSP ANNOUNCE/SET_PARAMETER upload with --use-ascii / CURLOPT_TRANSFERTEXT sends more body bytes than the declared Content-Length (incomplete fix of e |
| [4127756](https://hackerone.com/reports/4127756) | curl | low | - | 5 | 2026-10-19 | Improper Input Validation | urlapi: CURLUPART_HOST accepts text after an IPv6 zone ip and URL round trip changes the host |
| [214436](https://hackerone.com/reports/214436) | Blockchain | none | - | 4 | 2017-03-23 | HTTP Request Smuggling | HTTP Header Injection/HTTP_Response_Splitting |
| [245485](https://hackerone.com/reports/245485) | U.S. Dept Of Defense | medium | - | 4 | 2019-12-02 | CRLF Injection | CRLF Injection on ███████ |
| [277192](https://hackerone.com/reports/277192) | Inflection | none | - | 4 | 2017-10-24 | CRLF Injection | Host Header Injection and Cache Poisoning |
| [296632](https://hackerone.com/reports/296632) | Weblate | none | - | 4 | 2018-08-28 | Improper Neutralization of HTTP Headers for Scripting Syntax | Audit log validation |
| [1278891](https://hackerone.com/reports/1278891) | U.S. Dept Of Defense | medium | - | 4 | 2021-08-26 | LDAP Injection | [CVE-2021-29156] LDAP Injection at https://██████ |
| [1891474](https://hackerone.com/reports/1891474) | curl | low | - | 4 | 2023-03-22 | Failure to Sanitize Special Elements into a Different Plane (Special Element Injection) | CVE-2023-27533: Telnet option IAC injection |
| [1910810](https://hackerone.com/reports/1910810) | Internet Bug Bounty | medium | - | 4 | 2023-03-23 | HTTP Response Splitting | Apache HTTP Server: mod_proxy_uwsgi HTTP response splitting (CVE-2023-27522) |
| [3124103](https://hackerone.com/reports/3124103) | U.S. Dept Of Defense | medium | - | 4 | 2026-01-12 | Resource Injection | Swagger UI Injection via Config URL - `███` |
| [104620](https://hackerone.com/reports/104620) | Coinbase |  | - | 3 | 2015-12-16 | XML External Entities (XXE) | XXE in OAuth2 Applications gallery profile App logo |
| [123513](https://hackerone.com/reports/123513) | New Relic |  | - | 3 |  | CRLF Injection | Host Header Injection / Cache Poisoning |
| [125984](https://hackerone.com/reports/125984) | Uber |  | - | 3 | 2016-05-09 | CRLF Injection | CRLF Injection in developer.uber.com |
| [138332](https://hackerone.com/reports/138332) | Mail.ru |  | - | 3 |  | CRLF Injection | [torg.mail.ru] CRLF Injection |
| [176159](https://hackerone.com/reports/176159) | Brave Software | low | - | 3 | 2016-10-17 | HTTP Response Splitting | [iOS] URI Obfuscation in iOS application |
| [266030](https://hackerone.com/reports/266030) | Legal Robot | medium | - | 3 | 2018-02-01 | CRLF Injection | Add arbitrary value in reset password cookie |
| [901956](https://hackerone.com/reports/901956) | Mail.ru |  | - | 3 |  | CRLF Injection | SMTP Header Injection at http://abonement.ucs.ru |
| [1165223](https://hackerone.com/reports/1165223) | MTN Group | medium | - | 3 | 2021-12-11 | Improper Input Validation | Missing captcha and rate limit protection in help form |
| [36105](https://hackerone.com/reports/36105) | QIWI |  | - | 2 |  | CRLF Injection | CRLF Injection [ishop.qiwi.com] |
| [140851](https://hackerone.com/reports/140851) | Mail.ru |  | - | 2 |  | CRLF Injection | [sales.mail.ru] CRLF Injection |
| [184881](https://hackerone.com/reports/184881) | OWOX, Inc. | low | - | 2 | 2017-05-22 | HTTP Response Splitting | invalid URL parsing with and '@' |
| [283786](https://hackerone.com/reports/283786) | Inflection | none | - | 2 | 2017-10-31 | CRLF Injection | Host Header Injection or cache poisoning in multiple domains |
| [332708](https://hackerone.com/reports/332708) | Mail.ru |  | - | 2 |  | CRLF Injection | [dl.beepcar.ru] CRLF Injection |
| [473144](https://hackerone.com/reports/473144) | Nextcloud | low | - | 2 | 2021-02-14 | Resource Injection | Content spoofing on https://surveyserver.nextcloud.com |
| [771596](https://hackerone.com/reports/771596) | Node.js | medium | - | 2 | 2020-01-10 | CRLF Injection | CRLF Injection in legacy url API (url.parse().hostname) |
| [796013](https://hackerone.com/reports/796013) | New Relic |  | - | 2 |  | CRLF Injection | CRLF Injection in email address |
| [811366](https://hackerone.com/reports/811366) | Mail.ru |  | - | 2 |  | CRLF Injection | CRLF Injection in 301 Redirect allow to Set-Cookies for mail.ru |
| [907311](https://hackerone.com/reports/907311) | Node.js third-party modules | critical | - | 2 | 2020-08-22 | LDAP Injection | [meemo-app] Denial of Service via LDAP Injection |
| [981357](https://hackerone.com/reports/981357) | Agoric |  | - | 2 |  | Improper Input Validation | Improper Input Validation allows an attacker to "double spend" or "respend", violating the integrity of the message command history or causing DoS |
| [1278050](https://hackerone.com/reports/1278050) | U.S. Dept Of Defense | medium | - | 2 | 2021-08-19 | LDAP Injection | [CVE-2021-29156 on ForgeRock OpenAm] LDAP Injection in Webfinger Protocol! |
| [4127231](https://hackerone.com/reports/4127231) | curl | low | - | 2 | 2026-10-26 | Improper Input Validation | Derived cookie Path aborts cookie jar loading in curl 8.23.0 |
| [4130124](https://hackerone.com/reports/4130124) | curl | low | - | 2 | 2026-10-26 | Improper Neutralization of Escape, Meta, or Control Sequences | server filename with control characters printed to terminal (`-J`) |
| [16967](https://hackerone.com/reports/16967) | Mail.ru |  | - | 1 |  | CRLF Injection | my.mail.ru: HTTP Header Injection |
| [20400](https://hackerone.com/reports/20400) | Mail.ru |  | - | 1 |  | CRLF Injection | files.mail.ru: HTTP Header Injection |
| [231510](https://hackerone.com/reports/231510) | Gratipay | low | - | 1 | 2017-05-25 | HTTP Request Smuggling | Gratipay Website CSP "script-scr" includes "unsafe-inline" |
| [301592](https://hackerone.com/reports/301592) | Concrete CMS | low | - | 1 | 2018-01-12 | CRLF Injection | Host Header Injection allow HiJack Password Reset Link |
| [774883](https://hackerone.com/reports/774883) | curl |  | - | 1 | 2021-02-08 | Improper Input Validation | Division by zero if terminal width is 2 |
| [3972395](https://hackerone.com/reports/3972395) | curl |  | - | 1 | 2026-09-03 | Improper Input Validation | CVE-2026-80255: secure cookie attribute bypass with tab |
| [4112912](https://hackerone.com/reports/4112912) | curl | low | - | 1 | 2026-10-26 | Improper Input Validation | CVE-2026-111481: server-set cookie still aborts cookie jar |
| [688048](https://hackerone.com/reports/688048) | curl | medium | - | 0 | 2021-01-12 | Improper Handling of URL Encoding (Hex Encoding) | Incorrect IPv6 literal parsing leads to validated connection to unexpected https server. |
| [812969](https://hackerone.com/reports/812969) | curl |  | - | 0 | 2021-01-08 | Improper Input Validation | curl still vulnerable to SMB access smuggling via FILE URL on Windows |
| [3972403](https://hackerone.com/reports/3972403) | curl |  | - | 0 | 2026-10-14 | CRLF Injection | CVE-2026-87864: IMAP APPEND plus CRLF conversion command injection |
