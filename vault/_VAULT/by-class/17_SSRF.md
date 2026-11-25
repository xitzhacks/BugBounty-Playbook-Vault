---
title: "Vault class SSRF — Server-Side Request Forgery"
type: dataset-view
class: "Server-Side Request Forgery"
vault_category: "SSRF/"
rows: 330
paid_rows: 104
bounty_sum: 178,559
full_bodies_available: 171
source: "public HackerOne vault (hackerone disclosed), harvested 2026-11-17"
---

# SSRF — Server-Side Request Forgery

330 rows · 104 with a bounty figure · **$178,559** total · 171 with full write-up stored.
Playbook: `Vault/SSRF/` · Dataset: `Vault/_VAULT/reports.sqlite` (`SELECT * FROM reports WHERE ...`).

| Report | Program | Severity | Bounty | Votes | Disclosed | Weakness | Title |
|---|---|---|---|---|---|---|---|
| [2262382](https://hackerone.com/reports/2262382) | HackerOne | critical | $25,000 | 529 | 2023-12-08 | Server-Side Request Forgery (SSRF) | Server Side Request Forgery (SSRF) via Analytics Reports |
| [1406938](https://hackerone.com/reports/1406938) | Dropbox |  | $17,576 | 302 |  | Server-Side Request Forgery (SSRF) | Full Response SSRF via Google Drive |
| [826361](https://hackerone.com/reports/826361) | GitLab | high | $10,000 | 359 | 2020-06-07 | Server-Side Request Forgery (SSRF) | SSRF on project import via the remote_attachment_url on a Note |
| [1960765](https://hackerone.com/reports/1960765) | Reddit | high | $6,000 | 344 | 2023-04-26 | Server-Side Request Forgery (SSRF) | Blind SSRF to internal services in matrix preview_link API |
| [1409727](https://hackerone.com/reports/1409727) | Lark Technologies | critical | $5,000 | 124 | 2022-01-28 | Server-Side Request Forgery (SSRF) | Full read SSRF via Lark Docs `import as docs` feature |
| [776017](https://hackerone.com/reports/776017) | Kubernetes | high | $5,000 | 21 | 2020-10-30 | Server-Side Request Forgery (SSRF) | Half-Blind SSRF found in kube/cloud-controller-manager can be upgraded to complete SSRF (fully crafted HTTP requests) in vendor managed k8s service. |
| [2585385](https://hackerone.com/reports/2585385) | Internet Bug Bounty | high | $4,920 | 45 | 2024-07-13 | Server-Side Request Forgery (SSRF) | important: Apache HTTP Server on WIndows UNC SSRF (CVE-2024-38472) |
| [923132](https://hackerone.com/reports/923132) | Dropbox |  | $4,913 | 360 |  | Server-Side Request Forgery (SSRF) | Server Side Request Forgery (SSRF) at app.hellosign.com leads to AWS private keys disclosure |
| [2429894](https://hackerone.com/reports/2429894) | Internet Bug Bounty | high | $4,860 | 74 | 2024-03-29 | Server-Side Request Forgery (SSRF) | Libuv: Improper Domain Lookup that potentially leads to SSRF attacks |
| [746024](https://hackerone.com/reports/746024) | LY Corporation | high | $4,500 | 135 | 2020-03-25 | Server-Side Request Forgery (SSRF) | SSRF on music.line.me through getXML.php |
| [2612028](https://hackerone.com/reports/2612028) | Internet Bug Bounty | high | $4,263 | 19 | 2024-08-27 | Server-Side Request Forgery (SSRF) | important: Apache HTTP Server: SSRF with mod_rewrite in server/vhost context on Windows (CVE-2024-40898) |
| [398799](https://hackerone.com/reports/398799) | GitLab | high | $4,000 | 238 | 2019-03-14 | Server-Side Request Forgery (SSRF) | Unauthenticated blind SSRF in OAuth Jira authorization controller |
| [1628209](https://hackerone.com/reports/1628209) | U.S. Dept Of Defense | critical | $4,000 | 46 | 2022-09-14 | Server-Side Request Forgery (SSRF) | SSRF in Functional Administrative Support Tool pdf generator (████) [HtUS] |
| [333419](https://hackerone.com/reports/333419) | Slack | critical | $3,500 | 323 | 2020-03-12 | Server-Side Request Forgery (SSRF) | TURN server allows TCP and UDP proxying to internal network, localhost and meta-data services |
| [374737](https://hackerone.com/reports/374737) | HackerOne | low | $3,500 | 143 | 2018-07-04 | Server-Side Request Forgery (SSRF) | Blind SSRF on errors.hackerone.net due to Sentry misconfiguration |
| [1864188](https://hackerone.com/reports/1864188) | EXNESS | medium | $3,000 | 261 | 2023-07-24 | Server-Side Request Forgery (SSRF) | SSRF in graphQL query (pwapi.ex2b.com) |
| [892049](https://hackerone.com/reports/892049) | Lark Technologies | critical | $3,000 | 178 | 2021-02-05 | Server-Side Request Forgery (SSRF) | Stored XSS & SSRF in Lark Docs |
| [855276](https://hackerone.com/reports/855276) | GitLab | high | $3,000 | 36 | 2020-09-08 | Server-Side Request Forgery (SSRF) | Injection of `http.<url>.*` git config settings leading to SSRF |
| [1062888](https://hackerone.com/reports/1062888) | TikTok | high | $2,727 | 162 | 2021-02-15 | Server-Side Request Forgery (SSRF) | External SSRF and Local File Read via video upload due to vulnerable FFmpeg HLS processing |
| [2301565](https://hackerone.com/reports/2301565) | HackerOne | medium | $2,500 | 140 | 2024-01-30 | Server-Side Request Forgery (SSRF) | Server Side Request Forgery (SSRF) in webhook functionality |
| [893856](https://hackerone.com/reports/893856) | Mail.ru |  | $2,500 | 91 |  | Server-Side Request Forgery (SSRF) | Blind SSRF in horizon-heat |
| [907819](https://hackerone.com/reports/907819) | Mail.ru |  | $2,500 | 54 |  | Server-Side Request Forgery (SSRF) | Blind SSRF in magnum upgrade_params |
| [818109](https://hackerone.com/reports/818109) | Mail.ru |  | $2,500 | 34 |  | Server-Side Request Forgery (SSRF) | MCS Graphite SSRF: internal network access |
| [777664](https://hackerone.com/reports/777664) | Razer |  | $2,000 | 60 |  | Server-Side Request Forgery (SSRF) | [SSRF] Server-Side Request Forgery at https://sea-web.gold.razer.com/dev/simulator via notify_url Parameter |
| [446593](https://hackerone.com/reports/446593) | GitLab | medium | $2,000 | 30 | 2019-08-30 | Server-Side Request Forgery (SSRF) | GitLab's GitHub integration is vulnerable to SSRF vulnerability |
| [1540906](https://hackerone.com/reports/1540906) | Uber | medium | $2,000 | 30 | 2022-05-26 | Server-Side Request Forgery (SSRF) | Full read SSRF in flyte-poc-us-east4.uberinternal.com |
| [712103](https://hackerone.com/reports/712103) | Mail.ru |  | $1,500 | 132 |  | Server-Side Request Forgery (SSRF) | SSRF in clients.city-mobil.ru |
| [265050](https://hackerone.com/reports/265050) | Rockstar Games | medium | $1,500 | 83 | 2017-10-28 | Server-Side Request Forgery (SSRF) | Blind SSRF in emblem editor (2) |
| [288353](https://hackerone.com/reports/288353) | Rockstar Games | high | $1,500 | 52 | 2018-01-12 | Server-Side Request Forgery (SSRF) | SMB SSRF in emblem editor exposes taketwo domain credentials, may lead to RCE |
| [997926](https://hackerone.com/reports/997926) | Open-Xchange |  | $1,500 | 49 |  | Server-Side Request Forgery (SSRF) | SSRF - Unchecked Snippet IDs for distributed files |
| [707014](https://hackerone.com/reports/707014) | LY Corporation | medium | $1,350 | 56 | 2020-08-02 | Server-Side Request Forgery (SSRF) | Get-based SSRF limited to HTTP protocol on https://resizer.line-apps.com/form |
| [826097](https://hackerone.com/reports/826097) | PlayStation | high | $1,000 | 148 | 2021-03-30 | Server-Side Request Forgery (SSRF) | SSRF chained to hit internal host leading to another SSRF which allows to read internal images. |
| [811136](https://hackerone.com/reports/811136) | PlayStation | high | $1,000 | 103 | 2021-01-12 | Server-Side Request Forgery (SSRF) | SSRF on image renderer |
| [429617](https://hackerone.com/reports/429617) | Shopify | medium | $1,000 | 90 | 2019-03-14 | Server-Side Request Forgery (SSRF) | Reverse Proxy misroute leading to steal X-Shopify-Access-Token header |
| [1719719](https://hackerone.com/reports/1719719) | Acronis | critical | $1,000 | 71 | 2022-10-13 | Server-Side Request Forgery (SSRF) | mail.acronis.com is vulnerable to zero day vulnerability CVE-2022-41040 |
| [305974](https://hackerone.com/reports/305974) | Internet Bug Bounty | medium | $1,000 | 58 | 2019-11-12 | Server-Side Request Forgery (SSRF) | Inappropriate URL parsing may cause security risk! |
| [1624140](https://hackerone.com/reports/1624140) | U.S. Dept Of Defense | critical | $1,000 | 57 | 2022-10-14 | Server-Side Request Forgery (SSRF) | SSRF to read AWS metaData at https://█████/ [HtUS] |
| [1544133](https://hackerone.com/reports/1544133) | Kubernetes | medium | $1,000 | 51 | 2022-12-10 | Server-Side Request Forgery (SSRF) | SSRF vulnerability can be exploited when a hijacked aggregated api server such as metrics-server returns 30X |
| [867521](https://hackerone.com/reports/867521) | Snapchat | medium | $1,000 | 49 | 2020-12-18 | Server-Side Request Forgery (SSRF) | CreatorID leaked from public content posted to SnapMaps |
| [785384](https://hackerone.com/reports/785384) | Mail.ru |  | $1,000 | 33 |  | Server-Side Request Forgery (SSRF) | Blind SSRF on [relap.io] |
| [296045](https://hackerone.com/reports/296045) | Open-Xchange |  | $850 | 49 |  | Server-Side Request Forgery (SSRF) | SSRF in VCARD photo upload functionality |
| [299135](https://hackerone.com/reports/299135) | Open-Xchange |  | $850 | 33 |  | Server-Side Request Forgery (SSRF) | SSRF - RSS feed, blacklist bypass (301 re-direct) |
| [299130](https://hackerone.com/reports/299130) | Open-Xchange |  | $850 | 32 |  | Server-Side Request Forgery (SSRF) | SSRF - RSS feed, blacklist bypass (IP Formatting) |
| [293847](https://hackerone.com/reports/293847) | Open-Xchange |  | $850 | 20 |  | Server-Side Request Forgery (SSRF) | SSRF in /appsuite/api/autoconfig |
| [725307](https://hackerone.com/reports/725307) | Open-Xchange |  | $850 | 15 |  | Server-Side Request Forgery (SSRF) | Unchecked URL in attachment datasource |
| [361793](https://hackerone.com/reports/361793) | Open-Xchange |  | $850 | 10 |  | Server-Side Request Forgery (SSRF) | [SSRF] PDF documentconverterws |
| [200224](https://hackerone.com/reports/200224) | Mail.ru |  | $800 | 14 |  | Server-Side Request Forgery (SSRF) | SSRF на https://target.my.com/ |
| [347850](https://hackerone.com/reports/347850) | Mail.ru |  | $800 | 13 |  | Server-Side Request Forgery (SSRF) | Attacker can send requests from mail.ru server |
| [411466](https://hackerone.com/reports/411466) | Mail.ru |  | $800 | 6 |  | Server-Side Request Forgery (SSRF) | Чтение файлов на сервере и раскрытие директорий mediator.media |
| [299473](https://hackerone.com/reports/299473) | GitLab | high | $750 | 36 | 2018-04-27 | Server-Side Request Forgery (SSRF) | Evaluating Ruby code by injecting Rescue job on the system_hook_push queue through web hook |
| [188482](https://hackerone.com/reports/188482) | Pornhub |  | $750 | 18 |  | Server-Side Request Forgery (SSRF) | Unsecured Kibana/Elasticsearch instance |
| [1166977](https://hackerone.com/reports/1166977) | Mail.ru |  | $750 | 16 |  | Server-Side Request Forgery (SSRF) | [la.mail.ru] - SSRF + кража cookie |
| [843256](https://hackerone.com/reports/843256) | 8x8 | high | $700 | 23 | 2020-06-08 | Server-Side Request Forgery (SSRF) | Open TURN relay abuse is possible due to lack of peer access control (Critical) |
| [863553](https://hackerone.com/reports/863553) | Open-Xchange |  | $550 | 12 |  | Server-Side Request Forgery (SSRF) | SSRF protection bypass in /appsuite/api/oxodocumentfilter addfile action |
| [865652](https://hackerone.com/reports/865652) | Open-Xchange |  | $550 | 10 |  | Server-Side Request Forgery (SSRF) | Blind SSRF in /appsuite/api/oxodocumentfilter&action=addfile |
| [223203](https://hackerone.com/reports/223203) | Shopify | low | $500 | 81 | 2017-09-22 | Server-Side Request Forgery (SSRF) | SVG Server Side Request Forgery (SSRF) |
| [3522157](https://hackerone.com/reports/3522157) | DuckDuckGo | medium | $500 | 77 | 2026-09-17 | Server-Side Request Forgery (SSRF) | SSRF with bypass leads to client side hosting / vulnerabilities ( XSS and others ) |
| [570537](https://hackerone.com/reports/570537) | Pornhub |  | $500 | 61 |  | Server-Side Request Forgery (SSRF) | SSRF and local file disclosure by video upload on https://www.redtube.com/upload |
| [409701](https://hackerone.com/reports/409701) | Shopify | low | $500 | 56 | 2019-04-04 | Server-Side Request Forgery (SSRF) | SSRF in hatchful.shopify.com |
| [574133](https://hackerone.com/reports/574133) | Pornhub |  | $500 | 53 |  | Server-Side Request Forgery (SSRF) | SSRF and local file disclosure by video upload on https://www.tube8.com/ |
| [303378](https://hackerone.com/reports/303378) | Open-Xchange |  | $500 | 43 |  | Server-Side Request Forgery (SSRF) | SSRF - Blacklist bypass for mail account addition |
| [366638](https://hackerone.com/reports/366638) | Uber | critical | $500 | 37 | 2023-03-23 | Server-Side Request Forgery (SSRF) | [data-07.uberinternal.com] SSRF in Portainer app lead to access to Internal Docker API without Auth |
| [574134](https://hackerone.com/reports/574134) | Pornhub |  | $500 | 35 |  | Server-Side Request Forgery (SSRF) | SSRF and local file disclosure by video upload on http://www.youporn.com/ |
| [1783015](https://hackerone.com/reports/1783015) | Urban Company | medium | $500 | 33 | 2022-12-21 | Server-Side Request Forgery (SSRF) | Host header injection that bypassed protection and allowed accessing multiple subdomains |
| [1072873](https://hackerone.com/reports/1072873) | Acronis |  | $500 | 30 |  | Server-Side Request Forgery (SSRF) | SSRF when configuring Website Backup on Acronis Cloud |
| [220009](https://hackerone.com/reports/220009) | HackerOne |  | $500 | 25 | 2017-10-03 | Server-Side Request Forgery (SSRF) | Lack of input sanitization in Marketo form leads to execution of HTML in lead emails |
| [686363](https://hackerone.com/reports/686363) | Mail.ru |  | $500 | 17 |  | Server-Side Request Forgery (SSRF) | Blind SSRF on sentry.dev-my.com due to Sentry misconfiguration |
| [180434](https://hackerone.com/reports/180434) | Internet Bug Bounty | medium | $500 | 10 | 2018-01-11 | Server-Side Request Forgery (SSRF) | cURL / libcURL - CVE-2016-8624 invalid URL parsing with '#' |
| [305978](https://hackerone.com/reports/305978) | Internet Bug Bounty | low | $500 | 6 | 2019-11-12 | Server-Side Request Forgery (SSRF) | Urllib connects to a wrong host |
| [872094](https://hackerone.com/reports/872094) | GitHub Security Lab |  | $500 | 1 |  | Server-Side Request Forgery (SSRF) | CodeQL query to detect SSRF in Python |
| [738015](https://hackerone.com/reports/738015) | Open-Xchange |  | $450 | 37 |  | Server-Side Request Forgery (SSRF) | SSRF - Office Documents - Image URL |
| [1391729](https://hackerone.com/reports/1391729) | GitHub Security Lab |  | $450 | 4 |  | Server-Side Request Forgery (SSRF) | Yet another SSRF query for Go |
| [1391771](https://hackerone.com/reports/1391771) | GitHub Security Lab |  | $450 | 4 |  | Server-Side Request Forgery (SSRF) | Yet another SSRF query for Go |
| [737163](https://hackerone.com/reports/737163) | Open-Xchange |  | $400 | 41 |  | Server-Side Request Forgery (SSRF) | SSRF - Image Sources in HTML Snippets - 727234 bypass |
| [737161](https://hackerone.com/reports/737161) | Open-Xchange |  | $400 | 37 |  | Server-Side Request Forgery (SSRF) | SSRF - URL Attachments - 725307 bypass |
| [792953](https://hackerone.com/reports/792953) | Open-Xchange |  | $400 | 4 |  | Server-Side Request Forgery (SSRF) | SSRF - Guard - Unchecked HKP servers |
| [792960](https://hackerone.com/reports/792960) | Open-Xchange |  | $400 | 4 |  | Server-Side Request Forgery (SSRF) | SSRF - Guard - Unchecked WKS servers |
| [272095](https://hackerone.com/reports/272095) | GSA Bounty | medium | $300 | 41 | 2020-05-05 | Server-Side Request Forgery (SSRF) | SSRF/XSPA in labs.data.gov/dashboard/validate |
| [850114](https://hackerone.com/reports/850114) | Phabricator | medium | $300 | 28 | 2020-05-15 | Server-Side Request Forgery (SSRF) | SSRF in notifications.server configuration |
| [97395](https://hackerone.com/reports/97395) | Mail.ru |  | $300 | 15 |  | Server-Side Request Forgery (SSRF) | Potential SSRF in sales.mail.ru |
| [14033](https://hackerone.com/reports/14033) | Mail.ru |  | $300 | 4 |  | Server-Side Request Forgery (SSRF) | connect.mail.ru: SSRF |
| [197365](https://hackerone.com/reports/197365) | VK.com |  | $300 | 4 | 2017-04-22 | Server-Side Request Forgery (SSRF) | SSRF через Share-ботов |
| [816848](https://hackerone.com/reports/816848) | Visma Public |  | $250 | 42 |  | Server-Side Request Forgery (SSRF) | SSRF in the application's image export functionality |
| [1702864](https://hackerone.com/reports/1702864) | Nextcloud | medium | $250 | 33 | 2023-02-10 | Server-Side Request Forgery (SSRF) | SSRF via filter bypass due to lax checking on IPs |
| [1608039](https://hackerone.com/reports/1608039) | Nextcloud | low | $250 | 30 | 2022-09-16 | Server-Side Request Forgery (SSRF) | SSRF via potential filter bypass with too lax local domain checking |
| [1595006](https://hackerone.com/reports/1595006) | Nextcloud | medium | $250 | 17 | 2022-09-03 | Server-Side Request Forgery (SSRF) | Unauthenticated SSRF in 3rd party module "cerdic/csstidy" |
| [3576823](https://hackerone.com/reports/3576823) | Nextcloud | medium | $250 | 17 | 2026-10-27 | Server-Side Request Forgery (SSRF) | SSRF on Nextcloud Whiteboard Application via Recordings to Unauthorised Access to Whiteboards |
| [1391727](https://hackerone.com/reports/1391727) | GitHub Security Lab |  | $250 | 4 |  | Server-Side Request Forgery (SSRF) | Yet another SSRF query for Javascript |
| [1391726](https://hackerone.com/reports/1391726) | GitHub Security Lab |  | $250 | 3 |  | Server-Side Request Forgery (SSRF) | Yet another SSRF query for Javascript |
| [1008846](https://hackerone.com/reports/1008846) | GitHub Security Lab |  | $250 | 1 |  | Server-Side Request Forgery (SSRF) | Java: CWE-918 - Server Side Request Forgery (SSRF) |
| [1108418](https://hackerone.com/reports/1108418) | Logitech | medium | $200 | 41 | 2021-02-24 | Server-Side Request Forgery (SSRF) | SSRF allows reading AWS EC2 metadata using "readapi" variable in Streamlabs Cloudbot |
| [1716069](https://hackerone.com/reports/1716069) | Omise | medium | $200 | 36 | 2023-04-26 | Server-Side Request Forgery (SSRF) | The endpoint '/test/webhooks' is vulnerable to DNS Rebinding |
| [514224](https://hackerone.com/reports/514224) | GSA Bounty | low | $150 | 43 | 2019-08-26 | Server-Side Request Forgery (SSRF) | SSRF in Search.gov via ?url= parameter |
| [216533](https://hackerone.com/reports/216533) | Mail.ru |  | $150 | 21 |  | Server-Side Request Forgery (SSRF) | ssrf xspa [https://prt.mail.ru/] 2 |
| [258237](https://hackerone.com/reports/258237) | Mail.ru |  | $150 | 11 |  | Server-Side Request Forgery (SSRF) | [et.mail.ru] ssrf 2 |
| [120298](https://hackerone.com/reports/120298) | Mail.ru |  | $150 | 10 |  | Server-Side Request Forgery (SSRF) | SSRF/XSPA [parapa.mail.ru] 2 |
| [120216](https://hackerone.com/reports/120216) | Mail.ru |  | $150 | 3 |  | Server-Side Request Forgery (SSRF) | SSRF/XSPA [parapa.mail.ru] |
| [191543](https://hackerone.com/reports/191543) | Mail.ru |  | $150 | 2 |  | Server-Side Request Forgery (SSRF) | ssrf xspa [https://prt.mail.ru/] |
| [111950](https://hackerone.com/reports/111950) | Mail.ru |  | $150 | 1 |  | Server-Side Request Forgery (SSRF) | [allods.my.com] SSRF / XSPA |
| [833758](https://hackerone.com/reports/833758) | LY Corporation | medium | $100 | 33 | 2022-10-06 | Server-Side Request Forgery (SSRF) | Blind SSRF in social-plugins.line.me |
| [736867](https://hackerone.com/reports/736867) | Nextcloud | medium | $100 | 18 | 2020-03-14 | Server-Side Request Forgery (SSRF) | SSRF protection bypass |
| [61312](https://hackerone.com/reports/61312) | Slack |  | $100 | 14 | 2016-09-14 | Server-Side Request Forgery (SSRF) | Bypass of the SSRF protection (Slack commands, Phabricator integration) |
| [427835](https://hackerone.com/reports/427835) | Nextcloud | medium | $100 | 11 | 2019-12-12 | Server-Side Request Forgery (SSRF) | Server-Side request forgery in New-Subscription feature of the calendar app |
| [1131608](https://hackerone.com/reports/1131608) | LY Corporation | low | $100 | 11 | 2022-04-18 | Server-Side Request Forgery (SSRF) | SSRF occurrence in website preview used by LINE Official Account Manager (https://manager.line.biz) |
| [885975](https://hackerone.com/reports/885975) | Lyft |  | - | 653 |  | Server-Side Request Forgery (SSRF) | My Expense Report resulted in a Server-Side Request Forgery (SSRF) on Lyft |
| [341876](https://hackerone.com/reports/341876) | Shopify | medium | - | 587 | 2018-05-23 | Server-Side Request Forgery (SSRF) | SSRF in Exchange leads to ROOT access in all instances |
| [530974](https://hackerone.com/reports/530974) | Snapchat |  | - | 421 | 2020-11-30 | Server-Side Request Forgery (SSRF) | Server-Side Request Forgery using Javascript allows to exfill data from Google Metadata |
| [632101](https://hackerone.com/reports/632101) | GitLab | high | - | 350 | 2020-04-18 | Server-Side Request Forgery (SSRF) | Server Side Request Forgery mitigation bypass |
| [549882](https://hackerone.com/reports/549882) | Vimeo | critical | - | 276 | 2019-12-13 | Server-Side Request Forgery (SSRF) | SSRF  leaking internal google cloud data through upload function [SSH Keys, etc..] |
| [748069](https://hackerone.com/reports/748069) | Mail.ru |  | - | 272 |  | Server-Side Request Forgery (SSRF) | SSRF on fleet.city-mobil.ru leads to local file read |
| [1189367](https://hackerone.com/reports/1189367) | Evernote | critical | - | 264 | 2021-12-06 | Server-Side Request Forgery (SSRF) | Full read SSRF in www.evernote.com that can leak aws metadata and local file inclusion |
| [748128](https://hackerone.com/reports/748128) | Mail.ru |  | - | 237 |  | Server-Side Request Forgery (SSRF) | SSRF & LFR on city-mobil.ru |
| [878779](https://hackerone.com/reports/878779) | GitLab | critical | - | 229 | 2020-08-07 | Server-Side Request Forgery (SSRF) | Full Read SSRF on Gitlab's Internal Grafana |
| [508459](https://hackerone.com/reports/508459) | Omise | high | - | 214 | 2019-06-28 | Server-Side Request Forgery (SSRF) | SSRF in webhooks leads to AWS private keys disclosure |
| [398641](https://hackerone.com/reports/398641) | DuckDuckGo | high | - | 165 | 2018-09-09 | Server-Side Request Forgery (SSRF) | SSRF on duckduckgo.com/iu/ |
| [644238](https://hackerone.com/reports/644238) | Lark Technologies | critical | - | 164 | 2021-03-29 | Server-Side Request Forgery (SSRF) | Server Side Request Forgery |
| [3024673](https://hackerone.com/reports/3024673) | Autodesk | critical | - | 161 | 2025-03-18 | Server-Side Request Forgery (SSRF) | SSRF in Autodesk Rendering leading to account takeover |
| [3176157](https://hackerone.com/reports/3176157) | PortSwigger Web Security | none | - | 144 | 2025-10-08 | Server-Side Request Forgery (SSRF) | DNS Rebinding SSRF in Burp Suite MCP Server Enables Internal Network Access via send_http1_request Tool |
| [2300358](https://hackerone.com/reports/2300358) | inDrive | high | - | 141 | 2024-01-16 | Server-Side Request Forgery (SSRF) | SSRF in https://couriers.indrive.com/api/file-storage |
| [739962](https://hackerone.com/reports/739962) | Mail.ru |  | - | 130 |  | Server-Side Request Forgery (SSRF) | SSRF in filtering on relap.io |
| [643622](https://hackerone.com/reports/643622) | Semrush | medium | - | 125 | 2019-08-19 | Server-Side Request Forgery (SSRF) | SSRF In Get Video Contents |
| [1832494](https://hackerone.com/reports/1832494) | EXNESS | medium | - | 120 | 2023-10-25 | Server-Side Request Forgery (SSRF) | Blind SSRF on https://my.exnessaffiliates.com/ allows for internal network enumeration |
| [3165242](https://hackerone.com/reports/3165242) | Lichess | critical | - | 116 | 2025-06-03 | Server-Side Request Forgery (SSRF) | Server-Side Request Forgery (SSRF) via Game Export API |
| [776634](https://hackerone.com/reports/776634) | h1-ctf | critical | - | 108 | 2020-02-03 | Server-Side Request Forgery (SSRF) | [H1-415 2020] CTF Writeup |
| [727330](https://hackerone.com/reports/727330) | Slack | medium | - | 97 | 2021-06-09 | Server-Side Request Forgery (SSRF) | Header modification results in disclosure of Slack infra metadata to unauthorized parties |
| [853068](https://hackerone.com/reports/853068) | Mail.ru |  | - | 95 |  | Server-Side Request Forgery (SSRF) | [city-mobil.ru] SSRF & limited LFR on /taxiserv/photoeditor/save endpoint via base64 POST parameter |
| [2932960](https://hackerone.com/reports/2932960) | Stripo Inc | critical | - | 92 | 2025-12-01 | Server-Side Request Forgery (SSRF) | [my.stripo.email] Blind SSRF Vulnerability in Stripo App Export via Missing Endpoints Export Email Message to Zapier |
| [794099](https://hackerone.com/reports/794099) | Semrush | high | - | 86 | 2020-04-30 | Server-Side Request Forgery (SSRF) | SSRF and LFI in site-audit tool |
| [381129](https://hackerone.com/reports/381129) | Slack | medium | - | 84 | 2019-02-22 | Server-Side Request Forgery (SSRF) | SSRF in api.slack.com, using slash commands and bypassing the protections. |
| [1153862](https://hackerone.com/reports/1153862) | QIWI |  | - | 77 |  | Server-Side Request Forgery (SSRF) | SSRF на https://qiwi.com с помощью "Prerender HAR Capturer" |
| [2696271](https://hackerone.com/reports/2696271) | IBM | medium | - | 75 | 2024-10-03 | Server-Side Request Forgery (SSRF) | SSRF via host header let access localhost via https://go.dialexa.com |
| [369451](https://hackerone.com/reports/369451) | GitLab | medium | - | 72 | 2019-04-12 | Server-Side Request Forgery (SSRF) | SSRF in CI after first run |
| [541169](https://hackerone.com/reports/541169) | GitLab | high | - | 72 | 2019-12-12 | Server-Side Request Forgery (SSRF) | GitLab::UrlBlocker validation bypass leading to full Server Side Request Forgery |
| [2697592](https://hackerone.com/reports/2697592) | IBM | high | - | 71 | 2024-09-19 | Server-Side Request Forgery (SSRF) | SSRF and secret key disclosure found on Turbonomic endpoint |
| [756149](https://hackerone.com/reports/756149) | Nord Security |  | - | 70 |  | Server-Side Request Forgery (SSRF) | Blind SSRF on debug.nordvpn.com due to misconfigured sentry instance |
| [392859](https://hackerone.com/reports/392859) | Hacker Target |  | - | 69 |  | Server-Side Request Forgery (SSRF) | Sending Emails from  DNSDumpster - Server-Side Request Forgery to Internal SMTP Access |
| [2077985](https://hackerone.com/reports/2077985) | Semrush | high | - | 66 | 2024-03-06 | Server-Side Request Forgery (SSRF) | Lack of sanitization of the billing address in pdf invoice |
| [1875484](https://hackerone.com/reports/1875484) | 8x8 | medium | - | 65 | 2023-05-15 | Server-Side Request Forgery (SSRF) | connect.8x8.com: Blind SSRF via /api/v2/chats/image-check allows for Internal Ports scan |
| [3634400](https://hackerone.com/reports/3634400) | arkadiyt-projects | high | - | 65 | 2026-03-31 | Server-Side Request Forgery (SSRF) | SSRF Filter Bypass via Unblocked NAT64 Local-Use IPv6 Prefix (64:ff9b:1::/48) |
| [810401](https://hackerone.com/reports/810401) | Lark Technologies | medium | - | 64 | 2021-04-27 | Server-Side Request Forgery (SSRF) | SSRF with information disclosure |
| [2731133](https://hackerone.com/reports/2731133) | AWS VDP | high | - | 62 | 2024-10-04 | Server-Side Request Forgery (SSRF) | External service interaction (HTTP) |
| [3445890](https://hackerone.com/reports/3445890) | Basecamp | medium | - | 62 | 2025-12-22 | Server-Side Request Forgery (SSRF) | Link unfurling calls out to arbitrary URLs and the private-network guard misses link-local addresses |
| [1220688](https://hackerone.com/reports/1220688) | MTN Group | high | - | 61 | 2022-08-21 | Server-Side Request Forgery (SSRF) | Blind SSRF External Interaction on ████████ |
| [1379080](https://hackerone.com/reports/1379080) | MTN Group | medium | - | 60 | 2024-09-26 | Server-Side Request Forgery (SSRF) | SSRF Keycloak before 13.0.0 - CVE-2020-10770 on https://sponsoredata.mtn.ci |
| [1092230](https://hackerone.com/reports/1092230) | GitLab | high | - | 58 | 2021-07-13 | Server-Side Request Forgery (SSRF) | FogBugz import attachment full SSRF requiring vulnerability in *.fogbugz.com |
| [780036](https://hackerone.com/reports/780036) | h1-ctf | critical | - | 56 | 2020-02-03 | Server-Side Request Forgery (SSRF) | [h1-415 2020] Multiple vulnerabilities leading to leaking of secret user files |
| [2697601](https://hackerone.com/reports/2697601) | IBM | high | - | 56 | 2024-09-19 | Server-Side Request Forgery (SSRF) | SSRF and secret key disclosure found on Turbonomic endpoint |
| [411865](https://hackerone.com/reports/411865) | Chaturbate | high | - | 54 | 2018-10-21 | Server-Side Request Forgery (SSRF) | Blind SSRF at https://chaturbate.com/notifications/update_push/ |
| [1055823](https://hackerone.com/reports/1055823) | Helium | high | - | 54 | 2021-05-26 | Server-Side Request Forgery (SSRF) | SSRF By adding a custom integration on console.helium.com |
| [1300585](https://hackerone.com/reports/1300585) | Elastic | medium | - | 54 | 2023-05-05 | Server-Side Request Forgery (SSRF) | blind Server-Side Request Forgery (SSRF)  allows scanning internal ports |
| [1467044](https://hackerone.com/reports/1467044) | Cloudflare Public Bug Bounty | low | - | 54 | 2022-08-31 | Server-Side Request Forgery (SSRF) | Blind SSRF on platform.dash.cloudflare.com Due to Sentry misconfiguration |
| [1086206](https://hackerone.com/reports/1086206) | Acronis | medium | - | 53 | 2024-08-27 | Server-Side Request Forgery (SSRF) | Blind SSRF vulnerability on cz.acronis.com |
| [2015554](https://hackerone.com/reports/2015554) | Mozilla | none | - | 53 | 2024-01-12 | Server-Side Request Forgery (SSRF) | Internal Blind Server-Side Request Forgery (SSRF) allows scanning internal ports |
| [386292](https://hackerone.com/reports/386292) | Slack | medium | - | 52 | 2019-02-22 | Server-Side Request Forgery (SSRF) | Bypass of the SSRF protection in Event Subscriptions parameter. |
| [1886954](https://hackerone.com/reports/1886954) | Rocket.Chat | high | - | 52 | 2024-08-04 | Server-Side Request Forgery (SSRF) | Unauthenticated full-read SSRF via Twilio integration |
| [3465156](https://hackerone.com/reports/3465156) | Node.js | medium | - | 52 | 2026-02-12 | Server-Side Request Forgery (SSRF) | Node.js permission model bypass via unchecked Unix Domain Socket connections (UDS) |
| [356765](https://hackerone.com/reports/356765) | Slack | medium | - | 51 | 2018-07-12 | Server-Side Request Forgery (SSRF) | Internal SSRF bypass using slash commands at api.slack.com |
| [1410214](https://hackerone.com/reports/1410214) | Stripe | low | - | 51 | 2022-03-23 | Server-Side Request Forgery (SSRF) | Bypassing domain deny_list rule in Smokescreen via trailing dot leads to SSRF |
| [1043801](https://hackerone.com/reports/1043801) | Mail.ru |  | - | 49 |  | Server-Side Request Forgery (SSRF) | BLIND SSRF ON http://jsgames.mail.ru via avaOp parameter |
| [3623149](https://hackerone.com/reports/3623149) | Nextcloud | medium | - | 48 | 2026-09-30 | Server-Side Request Forgery (SSRF) | SSRF via User-Controlled Push proxyServer in Notifications Push Registration |
| [713](https://hackerone.com/reports/713) | HackerOne |  | - | 44 | 2014-02-15 | Server-Side Request Forgery (SSRF) | Upload profile photo from URL |
| [522203](https://hackerone.com/reports/522203) | Mail.ru |  | - | 44 |  | Server-Side Request Forgery (SSRF) | SSRF |
| [751625](https://hackerone.com/reports/751625) | Polymail, Inc. |  | - | 43 |  | Server-Side Request Forgery (SSRF) | XSPA on API service endpoint |
| [793704](https://hackerone.com/reports/793704) | Node.js third-party modules | medium | - | 43 | 2020-03-09 | Server-Side Request Forgery (SSRF) | Server-Side Request Forgery (SSRF) in Ghost CMS |
| [3887969](https://hackerone.com/reports/3887969) | Weblate | high | - | 43 | 2026-09-02 | Server-Side Request Forgery (SSRF) | SSRF via URL Parser Differential in `normalize_request_url` (wlc) |
| [971590](https://hackerone.com/reports/971590) | Sony | critical | - | 42 | 2022-10-06 | Server-Side Request Forgery (SSRF) | SSRF on http://www.███████/crossdomain.php via url parameter |
| [3383095](https://hackerone.com/reports/3383095) | arkadiyt-projects | critical | - | 42 | 2025-10-19 | Server-Side Request Forgery (SSRF) | DNS Rebinding Attack |
| [3479692](https://hackerone.com/reports/3479692) | Nextcloud |  | - | 41 | 2026-03-31 | Server-Side Request Forgery (SSRF) | Unauthenticated SSRF via Public Reference API -Sharing Token Bypass |
| [198690](https://hackerone.com/reports/198690) | New Relic |  | - | 39 |  | Server-Side Request Forgery (SSRF) | SSRF in alerts.newrelic.com exposes entire internal network |
| [2115212](https://hackerone.com/reports/2115212) | Nextcloud | medium | - | 38 | 2024-01-01 | Server-Side Request Forgery (SSRF) | DNS pin middleware can be tricked into DNS rebinding allowing SSRF |
| [1241149](https://hackerone.com/reports/1241149) | Acronis | low | - | 37 | 2022-02-22 | Server-Side Request Forgery (SSRF) | FULL SSRF |
| [1869714](https://hackerone.com/reports/1869714) | Nextcloud | low | - | 37 | 2024-01-10 | Server-Side Request Forgery (SSRF) | Blind SSRF in Mail App |
| [758948](https://hackerone.com/reports/758948) | Mail.ru |  | - | 36 |  | Server-Side Request Forgery (SSRF) | Blind SSRF на calendar.mail.ru при импорте календаря |
| [895551](https://hackerone.com/reports/895551) | Mail.ru |  | - | 35 |  | Server-Side Request Forgery (SSRF) | Grafana SSRF in grafana.instamart.ru |
| [1538056](https://hackerone.com/reports/1538056) | Radancy |  | - | 35 |  | Server-Side Request Forgery (SSRF) | Blind SSRF at packagist.maximum.nl |
| [900618](https://hackerone.com/reports/900618) | Mail.ru |  | - | 34 |  | Server-Side Request Forgery (SSRF) | SSRF at jira.plazius.ru - CVE-2019-8451 |
| [3366484](https://hackerone.com/reports/3366484) | curl | medium | - | 34 | 2025-10-03 | Server-Side Request Forgery (SSRF) | Unsanitized IPFS CID Allows SSRF Against Configured Gateway |
| [500468](https://hackerone.com/reports/500468) | Starbucks | high | - | 33 | 2019-04-03 | Server-Side Request Forgery (SSRF) | SSRF at ideas.starbucks.com |
| [3608558](https://hackerone.com/reports/3608558) | phpBB | medium | - | 33 | 2026-05-30 | Server-Side Request Forgery (SSRF) | Blind POST SSRF via Web Push Notification Endpoint |
| [271224](https://hackerone.com/reports/271224) | Eternal | critical | - | 32 | 2018-02-28 | Server-Side Request Forgery (SSRF) | SSRF in https://www.zomato.com████ allows reading local files and website source code |
| [517461](https://hackerone.com/reports/517461) | Lob |  | - | 31 |  | Server-Side Request Forgery (SSRF) | Blind SSRF/XSPA on dashboard.lob.com + blind code injection |
| [771465](https://hackerone.com/reports/771465) | Smule | none | - | 31 | 2020-01-17 | Server-Side Request Forgery (SSRF) | Open redirect bypass &  SSRF Security Vulnerability |
| [287245](https://hackerone.com/reports/287245) | HackerOne |  | - | 30 | 2017-11-09 | Server-Side Request Forgery (SSRF) | Blind SSRF in "Integrations" by abusing a bug in Ruby's native resolver. |
| [310036](https://hackerone.com/reports/310036) | U.S. Dept Of Defense | medium | - | 30 | 2019-12-02 | Server-Side Request Forgery (SSRF) | SSRF vulnerability on ██████████ leaks internal IP and various sensitive information |
| [674800](https://hackerone.com/reports/674800) | Valve | high | - | 30 | 2024-07-30 | Server-Side Request Forgery (SSRF) | /applications/dpc_(get\|post) provide full access to api.steampowered.com with the Dota2 API key |
| [978823](https://hackerone.com/reports/978823) | Lab45 | critical | - | 30 | 2021-09-16 | Server-Side Request Forgery (SSRF) | SSRF to AWS file read |
| [1622432](https://hackerone.com/reports/1622432) | Stripo Inc | critical | - | 29 | 2024-02-15 | Server-Side Request Forgery (SSRF) | [SSRF] my.stripo.email via the setup-wizard parameter |
| [247680](https://hackerone.com/reports/247680) | Imgur | high | - | 28 | 2020-08-13 | Server-Side Request Forgery (SSRF) | SSRF in imgur video GIF conversion |
| [642675](https://hackerone.com/reports/642675) | Infogram | low | - | 28 | 2020-05-24 | Server-Side Request Forgery (SSRF) | Bypass for blind SSRF #281950 and #287496 |
| [1890719](https://hackerone.com/reports/1890719) | U.S. Dept Of Defense | high | - | 28 | 2023-04-14 | Server-Side Request Forgery (SSRF) | Unauthenticated Blind SSRF at https://█████ via xmlrpc.php file |
| [3473145](https://hackerone.com/reports/3473145) | Rocket.Chat | high | - | 28 | 2026-07-29 | Server-Side Request Forgery (SSRF) | Unauthenticated SSRF in Voxtelesys integration ('checkUrlForSsrf' Bypass via DNS rebinding) |
| [3393664](https://hackerone.com/reports/3393664) | Rocket.Chat | high | - | 27 | 2026-06-11 | Server-Side Request Forgery (SSRF) | SSRF via improper validation after DNS name resolution in the link-preview feature |
| [395521](https://hackerone.com/reports/395521) | DuckDuckGo | critical | - | 25 | 2018-10-31 | Server-Side Request Forgery (SSRF) | SSRF vulnerability on proxy.duckduckgo.com (access to metadata server on AWS) |
| [587012](https://hackerone.com/reports/587012) | Mail.ru |  | - | 25 |  | Server-Side Request Forgery (SSRF) | Blind SSRF [ Sentry Misconfiguraton ] |
| [2902856](https://hackerone.com/reports/2902856) | Nextcloud | medium | - | 25 | 2025-12-23 | Server-Side Request Forgery (SSRF) | [nextcloud/mail] Blind SSRF to Internal Network via "List-Unsubscribe" SMTP Header when allow_local_remote_servers is allowed |
| [3383079](https://hackerone.com/reports/3383079) | Rocket.Chat | medium | - | 25 | 2026-06-11 | Server-Side Request Forgery (SSRF) | SSRF via Improper Redirect Validation in Rocket.Chat oEmbed Function |
| [771382](https://hackerone.com/reports/771382) | Stripo Inc | critical | - | 24 | 2020-02-19 | Server-Side Request Forgery (SSRF) | SSRF & unrestricted file upload on https://my.stripo.email/ |
| [941178](https://hackerone.com/reports/941178) | Kubernetes | medium | - | 24 | 2021-10-07 | Server-Side Request Forgery (SSRF) | SSRF for kube-apiserver cloudprovider scene |
| [1088975](https://hackerone.com/reports/1088975) | Mail.ru |  | - | 24 |  | Server-Side Request Forgery (SSRF) | [int.ucs.ru] Доступ ко внутренней сети UCS через забытый прокси Fiddler на 217.25.235.214:7459 |
| [783392](https://hackerone.com/reports/783392) | lemlist | medium | - | 23 | 2020-05-28 | Server-Side Request Forgery (SSRF) | SSRF in img.lemlist.com that leads to Localhost Port Scanning |
| [891270](https://hackerone.com/reports/891270) | Node.js third-party modules | critical | - | 23 | 2020-06-28 | Server-Side Request Forgery (SSRF) | [Uppy] Internal Server side request forgery (bypass of #786956) |
| [1006599](https://hackerone.com/reports/1006599) | TikTok | low | - | 23 | 2020-12-17 | Server-Side Request Forgery (SSRF) | Blind SSRF in ads.tiktok.com |
| [1125389](https://hackerone.com/reports/1125389) | Mail.ru |  | - | 23 |  | Server-Side Request Forgery (SSRF) | [Plazius] SSRF через некорректно сконфигурированный Fiddler 46.148.201.206:10121 |
| [253558](https://hackerone.com/reports/253558) | Cloudflare Vulnerability Disclosure |  | - | 22 |  | Server-Side Request Forgery (SSRF) | SSRF |
| [441090](https://hackerone.com/reports/441090) | GitLab | high | - | 22 | 2020-11-23 | Server-Side Request Forgery (SSRF) | CRLF injection & SSRF in git:// protocal lead to arbitrary code execution |
| [786956](https://hackerone.com/reports/786956) | Node.js third-party modules | high | - | 22 | 2020-03-02 | Server-Side Request Forgery (SSRF) | Server Side Request Forgery in Uppy npm module |
| [204513](https://hackerone.com/reports/204513) | WordPress | medium | - | 21 | 2017-07-17 | Server-Side Request Forgery (SSRF) | Infrastructure - Photon - SSRF |
| [206894](https://hackerone.com/reports/206894) | Lyst | low | - | 21 | 2017-10-18 | Server-Side Request Forgery (SSRF) | SSRF at iris.lystit.com |
| [397402](https://hackerone.com/reports/397402) | MariaDB | medium | - | 21 | 2018-10-13 | Server-Side Request Forgery (SSRF) | SSRF on jira.mariadb.org |
| [925527](https://hackerone.com/reports/925527) | Bitwarden | low | - | 21 | 2020-09-11 | Server-Side Request Forgery (SSRF) | Blind HTTP GET SSRF via website icon fetch (bypass of pull#812) |
| [1023920](https://hackerone.com/reports/1023920) | Stripo Inc | low | - | 21 | 2020-12-11 | Server-Side Request Forgery (SSRF) | SSRF external interaction |
| [1747596](https://hackerone.com/reports/1747596) | U.S. Department of State | low | - | 21 | 2023-03-24 | Server-Side Request Forgery (SSRF) | Bypassing Whitelist to perform SSRF for internal host scanning |
| [215105](https://hackerone.com/reports/215105) | GitLab | medium | - | 20 | 2017-11-09 | Server-Side Request Forgery (SSRF) | SSRF vulnerability in gitlab.com via project import. |
| [243277](https://hackerone.com/reports/243277) | Mixmax |  | - | 20 | 2017-07-18 | Server-Side Request Forgery (SSRF) | SSRF via webhook |
| [288950](https://hackerone.com/reports/288950) | HackerOne |  | - | 20 | 2017-11-16 | Server-Side Request Forgery (SSRF) | Additional bypass allows SSRF for internal netblocks |
| [1115139](https://hackerone.com/reports/1115139) | Shopify | low | - | 20 | 2021-12-02 | Server Side Request Forgery | Bypassing HTML filter in "Packing Slip Template" Lead to SSRF to Internal Kubernetes Endpoints |
| [145524](https://hackerone.com/reports/145524) | Nextcloud |  | - | 19 | 2016-06-17 | Server-Side Request Forgery (SSRF) | Server side request forgery (SSRF) on nextcloud implementation. |
| [243865](https://hackerone.com/reports/243865) | Concrete CMS |  | - | 19 | 2018-01-06 | Server-Side Request Forgery (SSRF) | SSRF thru File Replace |
| [1370731](https://hackerone.com/reports/1370731) | Acronis | high | - | 19 | 2022-07-13 | Server-Side Request Forgery (SSRF) | CVE-2021-40438 on cp-eu2.acronis.com |
| [3470649](https://hackerone.com/reports/3470649) | curl | high | - | 19 | 2025-12-18 | Server-Side Request Forgery (SSRF) | File URL UNC Path Access (Windows SSRF) |
| [602498](https://hackerone.com/reports/602498) | Mail.ru |  | - | 17 |  | Server-Side Request Forgery (SSRF) | SSRF On [ allods.mail.ru ] |
| [178184](https://hackerone.com/reports/178184) | X / xAI | medium | - | 16 | 2017-04-06 | Server-Side Request Forgery (SSRF) | SSRF in https://cards-dev.twitter.com/validator |
| [358119](https://hackerone.com/reports/358119) | DuckDuckGo | high | - | 16 | 2018-08-15 | Server-Side Request Forgery (SSRF) | SSRF in proxy.duckduckgo.com via the image_host parameter |
| [808169](https://hackerone.com/reports/808169) | Kubernetes | low | - | 16 | 2021-01-07 | Server-Side Request Forgery (SSRF) | Blind SSRF on velodrome.canary.k8s.io |
| [1354335](https://hackerone.com/reports/1354335) | Mail.ru |  | - | 16 |  | Server-Side Request Forgery (SSRF) | SSRF + RCE через fastCGI в  POST /api/nr/video |
| [860939](https://hackerone.com/reports/860939) | LY Corporation | medium | - | 15 | 2022-04-18 | Server-Side Request Forgery (SSRF) | SSRF restricted to HTTP/HTML on LINE Social Plugins (https://social-plugins.line.me/) |
| [863221](https://hackerone.com/reports/863221) | Concrete CMS | low | - | 15 | 2021-10-04 | Server-Side Request Forgery (SSRF) | SSRF bypass |
| [1895874](https://hackerone.com/reports/1895874) | Nextcloud | medium | - | 15 | 2023-10-19 | Server-Side Request Forgery (SSRF) | Responsive Server-side Request Forgery (SSRF) |
| [3303283](https://hackerone.com/reports/3303283) | Nextcloud | medium | - | 15 | 2026-09-17 | Server-Side Request Forgery (SSRF) | Unauthenticated blind SSRF in Circles signature verification bypasses Nextcloud local-address protections |
| [115857](https://hackerone.com/reports/115857) | Imgur |  | - | 14 | 2016-04-16 | Server-Side Request Forgery (SSRF) | SSRF and local file read in video to gif converter |
| [344032](https://hackerone.com/reports/344032) | New Relic |  | - | 14 |  | Server-Side Request Forgery (SSRF) | Blind SSRF in Ticketing Integrations Jira webhooks leading to internal network enumeration and blind HTTP requests |
| [689245](https://hackerone.com/reports/689245) | GitLab | medium | - | 14 | 2020-08-17 | Server-Side Request Forgery (SSRF) | SSRF In plantuml (on plantuml.pre.gitlab.com) |
| [709951](https://hackerone.com/reports/709951) | GitLab | medium | - | 14 | 2023-05-30 | Server-Side Request Forgery (SSRF) | Blind SSRF in FogBugz project import |
| [1067443](https://hackerone.com/reports/1067443) | Shopify | none | - | 14 | 2021-02-12 | Server-Side Request Forgery (SSRF) | Screenshot Service leaks X-ABS-App-Token |
| [1379656](https://hackerone.com/reports/1379656) | Omise | medium | - | 14 | 2022-03-22 | Server-Side Request Forgery (SSRF) | The endpoint '/test/webhooks' is vulnerable to DNS Rebinding |
| [1691501](https://hackerone.com/reports/1691501) | U.S. Dept Of Defense | high | - | 14 | 2022-10-14 | Server-Side Request Forgery (SSRF) | Blind SSRF via image upload URL downloader on https://██████/ |
| [1704024](https://hackerone.com/reports/1704024) | U.S. Dept Of Defense | high | - | 14 | 2023-06-23 | Server-Side Request Forgery (SSRF) | External service interaction ( DNS and HTTP ) in www.████████ |
| [1913095](https://hackerone.com/reports/1913095) | Nextcloud | low | - | 14 | 2023-05-30 | Server-Side Request Forgery (SSRF) | Blind SSRF as normal user from mailapp |
| [754025](https://hackerone.com/reports/754025) | Stripo Inc | medium | - | 13 | 2020-04-10 | Server-Side Request Forgery (SSRF) | SSRF in Export template to ActiveCampaign |
| [913276](https://hackerone.com/reports/913276) | Bitwarden | medium | - | 13 | 2020-08-07 | Server-Side Request Forgery (SSRF) | Server-Side Request Forgery in "icons.bitwarden.net" |
| [1736390](https://hackerone.com/reports/1736390) | Nextcloud | low | - | 13 | 2023-02-06 | Server-Side Request Forgery (SSRF) | Mail app - blind SSRF via imapHost parameter |
| [3791168](https://hackerone.com/reports/3791168) | curl | medium | - | 13 | 2026-06-10 | Server-Side Request Forgery (SSRF) | curl-ipv4-percent-normalization-SSRF |
| [3973228](https://hackerone.com/reports/3973228) | curl |  | - | 13 | 2026-08-29 | Server-Side Request Forgery (SSRF) | 50: CMake `HTTP_ONLY` does not disable SSH backends — SCP and SFTP remain usable |
| [227806](https://hackerone.com/reports/227806) | QIWI |  | - | 12 |  | Server-Side Request Forgery (SSRF) | [qiwi.me] No limits on image download requests |
| [280511](https://hackerone.com/reports/280511) | Infogram | medium | - | 12 | 2017-12-06 | Server-Side Request Forgery (SSRF) | Server Side Request Forgery on JSON Feed |
| [287496](https://hackerone.com/reports/287496) | Infogram | low | - | 12 | 2017-11-08 | Server-Side Request Forgery (SSRF) | Internal Ports Scanning via Blind SSRF  (URL Redirection to beat filter) |
| [781295](https://hackerone.com/reports/781295) | h1-ctf | critical | - | 12 | 2020-02-04 | Server-Side Request Forgery (SSRF) | [h1-415 2020] SSRF in a headless chrome with remote debugging leads to sensible information leak |
| [809248](https://hackerone.com/reports/809248) | GitLab | medium | - | 12 | 2020-09-08 | Server-Side Request Forgery (SSRF) | SSRF into Shared Runner, by replacing dockerd with malicious server in Executor |
| [895824](https://hackerone.com/reports/895824) | h1-ctf | critical | - | 12 | 2020-09-14 | Server-Side Request Forgery (SSRF) | [h1-2006 2020] Bounty payments are done ! |
| [956296](https://hackerone.com/reports/956296) | GitHub Security Lab |  | - | 12 |  | Server-Side Request Forgery (SSRF) | Golang : Improvements to Golang SSRF query |
| [997376](https://hackerone.com/reports/997376) | U.S. Dept Of Defense | high | - | 12 | 2021-04-02 | Server-Side Request Forgery (SSRF) | External Service Interaction (HTTP/DNS) on https://www.███  (██████████ parameter) |
| [1018568](https://hackerone.com/reports/1018568) | phpBB | low | - | 12 | 2020-12-20 | Server-Side Request Forgery (SSRF) | Server Side Request Forgery in 'Jabber settings' in Admin Control Panel |
| [4129950](https://hackerone.com/reports/4129950) | curl | high | - | 12 | 2026-10-21 | Server-Side Request Forgery (SSRF) | IDN decoding inserts authority delimiters and can redirect proxy CONNECT to a different host |
| [180527](https://hackerone.com/reports/180527) | VK.com |  | - | 11 | 2017-02-09 | Server-Side Request Forgery (SSRF) | SSRF (open) - via GET request |
| [448598](https://hackerone.com/reports/448598) | Uber | high | - | 11 | 2021-02-25 | Server-Side Request Forgery (SSRF) | [usuppliers.uber.com] - Server Side Request Forgery via XXE OOB |
| [738553](https://hackerone.com/reports/738553) | Stripo Inc | medium | - | 11 | 2019-12-18 | Server-Side Request Forgery (SSRF) | SSRF in /cabinet/stripeapi/v1/siteInfoLookup?url=XXX |
| [781281](https://hackerone.com/reports/781281) | h1-ctf | critical | - | 11 | 2020-02-03 | Server-Side Request Forgery (SSRF) | [h1-415 2020] Chain of vulnerabilities leading to account takeover and unauthorized access of sensitive internal resources |
| [893305](https://hackerone.com/reports/893305) | h1-ctf | critical | - | 11 | 2020-06-22 | Server-Side Request Forgery (SSRF) | [H1-2006 2020] CTF Writeup |
| [1580495](https://hackerone.com/reports/1580495) | Stripe | low | - | 11 | 2022-10-19 | Server-Side Request Forgery (SSRF) | Bypassing domain deny_list rule in Smokescreen via double brackets [[]] which leads to SSRF |
| [1628102](https://hackerone.com/reports/1628102) | U.S. Dept Of Defense | high | - | 11 | 2022-09-14 | Server-Side Request Forgery (SSRF) | Full read SSRF at █████████ [HtUS] |
| [1741525](https://hackerone.com/reports/1741525) | Nextcloud | low | - | 11 | 2023-02-06 | Server-Side Request Forgery (SSRF) | Mail app - Blind SSRF via Sierve server fonctionnality and sieveHost parameter |
| [1746582](https://hackerone.com/reports/1746582) | Nextcloud | low | - | 11 | 2023-02-06 | Server-Side Request Forgery (SSRF) | Mail app - blind SSRF via smtpHost parameter |
| [207477](https://hackerone.com/reports/207477) | U.S. Dept Of Defense | medium | - | 10 | 2019-12-02 | Server-Side Request Forgery (SSRF) | SSRF in ███████ |
| [301924](https://hackerone.com/reports/301924) | GitLab | medium | - | 10 | 2018-04-30 | Server-Side Request Forgery (SSRF) | SSRF vulnerability in gitlab.com webhook |
| [382048](https://hackerone.com/reports/382048) | U.S. Dept Of Defense | medium | - | 10 | 2019-12-02 | Server-Side Request Forgery (SSRF) | Server-Side Request Forgery (SSRF) |
| [385178](https://hackerone.com/reports/385178) | Chaturbate | medium | - | 10 | 2018-09-20 | Server-Side Request Forgery (SSRF) | Blind SSRF on image proxy camo.stream.highwebmedia.com |
| [427227](https://hackerone.com/reports/427227) | Mail.ru |  | - | 10 |  | Server-Side Request Forgery (SSRF) | Server side request forgery |
| [432277](https://hackerone.com/reports/432277) | Mail.ru |  | - | 10 |  | Server-Side Request Forgery (SSRF) | SSRF на api.icq.net |
| [887766](https://hackerone.com/reports/887766) | h1-ctf | critical | - | 10 | 2020-06-18 | Server-Side Request Forgery (SSRF) | [H1-2006 2020]   CTF Writeup |
| [1369312](https://hackerone.com/reports/1369312) | Concrete CMS | low | - | 10 | 2022-11-25 | Server-Side Request Forgery (SSRF) | SSRF mitigation bypass using DNS Rebind attack |
| [236301](https://hackerone.com/reports/236301) | Mixmax | low | - | 9 | 2017-07-19 | Server-Side Request Forgery (SSRF) | Blind SSRF due to img tag injection in career form |
| [327480](https://hackerone.com/reports/327480) | Informatica | medium | - | 9 | 2018-08-16 | Server-Side Request Forgery (SSRF) | SSRF on infawiki.informatica.com and infawikitest.informatica.com |
| [382612](https://hackerone.com/reports/382612) | Shopify | low | - | 9 | 2018-07-19 | Server-Side Request Forgery (SSRF) | Potential SSRF and disclosure of sensitive site on *shopifycloud.com |
| [659565](https://hackerone.com/reports/659565) | Lark Technologies | low | - | 9 | 2021-03-18 | Server-Side Request Forgery (SSRF) | Server Side Request Forgery |
| [879803](https://hackerone.com/reports/879803) | Node.js third-party modules | high | - | 9 | 2021-06-28 | Server-Side Request Forgery (SSRF) | Bypass of SSRF Vulnerability |
| [1057531](https://hackerone.com/reports/1057531) | Automattic | high | - | 9 | 2020-12-15 | Server-Side Request Forgery (SSRF) | GET /api/v2/url_info endpoint is vulnerable to Blind SSRF |
| [1553841](https://hackerone.com/reports/1553841) | curl | medium | - | 9 | 2022-05-11 | Server-Side Request Forgery (SSRF) | CVE-2022-27780: percent-encoded path separator in URL host |
| [3508785](https://hackerone.com/reports/3508785) | curl | high | - | 9 | 2026-01-14 | Server-Side Request Forgery (SSRF) | Gopher Protocol Command Injection (SSRF Smuggling) |
| [236349](https://hackerone.com/reports/236349) | Shopify | medium | - | 8 | 2018-07-11 | Server-Side Request Forgery (SSRF) | [out-of-scope] toxiproxy: Lack of CSRF protection allows an attacker to gain access to internal Shopify network |
| [406387](https://hackerone.com/reports/406387) | U.S. Dept Of Defense | high | - | 8 | 2019-10-08 | Server-Side Request Forgery (SSRF) | SSRF on ████████ |
| [901050](https://hackerone.com/reports/901050) | Mail.ru |  | - | 8 |  | Server-Side Request Forgery (SSRF) | Blind SSRF on http://info.ucs.ru/settings/check/ |
| [1119224](https://hackerone.com/reports/1119224) | U.S. Dept Of Defense | critical | - | 8 | 2021-03-24 | Server-Side Request Forgery (SSRF) | SSRF due to CVE-2021-26855 on ████████ |
| [1623685](https://hackerone.com/reports/1623685) | U.S. Dept Of Defense | medium | - | 8 | 2022-09-14 | Server-Side Request Forgery (SSRF) | SSRF ACCESS AWS METADATA - █████ |
| [229199](https://hackerone.com/reports/229199) | U.S. Dept Of Defense | high | - | 7 | 2017-07-05 | Server-Side Request Forgery (SSRF) | Limited code execution vulnerability on a DoD website |
| [359288](https://hackerone.com/reports/359288) | GitLab | medium | - | 7 | 2018-07-16 | Server-Side Request Forgery (SSRF) | Potensial SSRF via Git repository URL |
| [471520](https://hackerone.com/reports/471520) | Nutanix | high | - | 7 | 2022-04-25 | Server-Side Request Forgery (SSRF) | Local file disclosure through SSRF at next.nutanix.com |
| [746541](https://hackerone.com/reports/746541) | Nextcloud | medium | - | 7 | 2020-03-01 | Server-Side Request Forgery (SSRF) | SSRF on local storage of iOS mobile |
| [773888](https://hackerone.com/reports/773888) | 8x8 | medium | - | 7 | 2020-06-09 | Server-Side Request Forgery (SSRF) | xmlrpc.php file enabled |
| [782979](https://hackerone.com/reports/782979) | Stripo Inc | medium | - | 7 | 2020-01-28 | Server-Side Request Forgery (SSRF) | Information disclosure through Server side resource forgery |
| [800909](https://hackerone.com/reports/800909) | Stripo Inc | high | - | 7 | 2020-03-24 | Server-Side Request Forgery (SSRF) | Blind SSRF while Creating Templates |
| [846184](https://hackerone.com/reports/846184) | BlockDev Sp. Z o.o | critical | - | 7 | 2020-04-14 | Server-Side Request Forgery (SSRF) | Blind SSRF at https://chat.makerdao.com/account/profile |
| [895780](https://hackerone.com/reports/895780) | h1-ctf | critical | - | 7 | 2020-06-18 | Server-Side Request Forgery (SSRF) | [h1-2006 2020] CTF Walkthrough |
| [906890](https://hackerone.com/reports/906890) | Mail.ru |  | - | 7 |  | Server-Side Request Forgery (SSRF) | SSRF in www.ucs.ru |
| [1183472](https://hackerone.com/reports/1183472) | U.S. Dept Of Defense | medium | - | 7 | 2022-04-29 | Server-Side Request Forgery (SSRF) | SSRF due to  CVE-2021-27905 in www.████████ |
| [1364797](https://hackerone.com/reports/1364797) | Concrete CMS | low | - | 7 | 2022-11-25 | Server-Side Request Forgery (SSRF) | SSRF - pivoting in the private LAN |
| [189648](https://hackerone.com/reports/189648) | U.S. Dept Of Defense | low | - | 6 | 2017-08-15 | Server-Side Request Forgery (SSRF) | Server Side Request Forgery (SSRF) vulnerability in a DoD website |
| [300513](https://hackerone.com/reports/300513) | U.S. Dept Of Defense | medium | - | 6 | 2019-12-02 | Server-Side Request Forgery (SSRF) | WebLogic Server Side Request Forgery |
| [704621](https://hackerone.com/reports/704621) | curl | critical | - | 6 | 2021-01-08 | Server-Side Request Forgery (SSRF) | SSRF via maliciously crafted URL due to host confusion |
| [815084](https://hackerone.com/reports/815084) | Node.js third-party modules | low | - | 6 | 2020-06-04 | Server-Side Request Forgery (SSRF) | [Limited bypass of #793704] Blind SSRF in Ghost CMS |
| [847101](https://hackerone.com/reports/847101) | Stripo Inc | high | - | 6 | 2020-07-13 | Server-Side Request Forgery (SSRF) | SSRF via Export Service in  ActiveCampaign |
| [852413](https://hackerone.com/reports/852413) | Stripo Inc | high | - | 6 | 2020-06-30 | Server-Side Request Forgery (SSRF) | SSRF in my.stripo.email |
| [1066914](https://hackerone.com/reports/1066914) | h1-ctf | critical | - | 6 | 2021-01-11 | Server-Side Request Forgery (SSRF) | [ Hacky Holidays CTF ] Completely taken down the Grinch Networks |
| [1250305](https://hackerone.com/reports/1250305) | GitHub Security Lab |  | - | 6 |  | Server-Side Request Forgery (SSRF) | [Java] CWE-918: Added URLClassLoader and WebClient SSRF sinks |
| [1538144](https://hackerone.com/reports/1538144) | GitHub Security Lab |  | - | 6 |  | Server-Side Request Forgery (SSRF) | [Python]: Add Server-side Request Forgery sinks |
| [146875](https://hackerone.com/reports/146875) | New Relic |  | - | 5 |  | Server-Side Request Forgery (SSRF) | http://newrelic.com SSRF/XSPA |
| [996273](https://hackerone.com/reports/996273) | U.S. Dept Of Defense | high | - | 5 | 2021-01-12 | Server-Side Request Forgery (SSRF) | SSRF in login page using fetch API exposes victims IP address to attacker controled server |
| [1119228](https://hackerone.com/reports/1119228) | U.S. Dept Of Defense | critical | - | 5 | 2021-03-24 | Server-Side Request Forgery (SSRF) | CVE-2021-26855 on ████████ resulting in SSRF |
| [1389905](https://hackerone.com/reports/1389905) | GitHub Security Lab |  | - | 5 |  | Server-Side Request Forgery (SSRF) | C# : Add query to detect Server Side Request Forgery |
| [1512936](https://hackerone.com/reports/1512936) | GitHub Security Lab |  | - | 5 |  | Server-Side Request Forgery (SSRF) | [Java]: Add JDBC connection SSRF sinks |
| [1663788](https://hackerone.com/reports/1663788) | Internet Bug Bounty | medium | - | 5 | 2022-09-23 | Server-Side Request Forgery (SSRF) | [CVE-2022-35949]: undici.request vulnerable to SSRF using absolute / protocol-relative URL on pathname |
| [1712240](https://hackerone.com/reports/1712240) | Yelp | medium | - | 5 | 2022-09-28 | Server-Side Request Forgery (SSRF) | Server-side request forgery  (ssrf) |
| [213358](https://hackerone.com/reports/213358) | Nextcloud |  | - | 4 | 2017-04-20 | Server-Side Request Forgery (SSRF) | SSRF at apps.nextcloud.com/developer/apps/releases/new |
| [482634](https://hackerone.com/reports/482634) | U.S. Dept Of Defense | critical | - | 4 | 2019-10-08 | Server-Side Request Forgery (SSRF) | https://████████ Impacted by DNN ImageHandler SSRF |
| [890555](https://hackerone.com/reports/890555) | h1-ctf | critical | - | 4 | 2020-06-18 | Server-Side Request Forgery (SSRF) | [H1-2006 2020] CTF write-up |
| [1051431](https://hackerone.com/reports/1051431) | Engel & Völkers Technology GmbH |  | - | 4 |  | Server-Side Request Forgery (SSRF) | Blind SSRF on infodesk.engelvoelkers.com via proxy.php |
| [1061010](https://hackerone.com/reports/1061010) | GitHub Security Lab |  | - | 4 |  | Server-Side Request Forgery (SSRF) | Java: Add SSRF query for Java |
| [1066801](https://hackerone.com/reports/1066801) | h1-ctf | critical | - | 4 | 2021-01-11 | Server-Side Request Forgery (SSRF) | Hacky Holidays CTF Writeup |
| [1391772](https://hackerone.com/reports/1391772) | GitHub Security Lab |  | - | 4 |  | Server-Side Request Forgery (SSRF) | Yet another SSRF query for Go |
| [191216](https://hackerone.com/reports/191216) | GitLab | medium | - | 3 | 2017-11-28 | Server-Side Request Forgery (SSRF) | SSRF via git Repo by URL Abuse |
| [374818](https://hackerone.com/reports/374818) | Hanno's projects | low | - | 3 | 2018-11-09 | Server-Side Request Forgery (SSRF) | SSRF in rompager-check |
| [764517](https://hackerone.com/reports/764517) | Stripo Inc | low | - | 3 | 2020-03-24 | Server-Side Request Forgery (SSRF) | SSRF leads to internal port scan |
| [1004847](https://hackerone.com/reports/1004847) | Ian Dunn | none | - | 3 | 2020-10-12 | Server-Side Request Forgery (SSRF) | SSRF Possible through /wordpress/xmlrpc.php |
| [1049624](https://hackerone.com/reports/1049624) | curl | none | - | 3 | 2021-01-08 | Server-Side Request Forgery (SSRF) | Abusing URL Parsers by long schema name |
| [1068433](https://hackerone.com/reports/1068433) | h1-ctf | critical | - | 3 | 2021-01-11 | Server-Side Request Forgery (SSRF) | 12 Days of CTF Walkthroughs |
| [1391724](https://hackerone.com/reports/1391724) | GitHub Security Lab |  | - | 3 |  | Server-Side Request Forgery (SSRF) | Yet another SSRF query for Javascript |
| [1391725](https://hackerone.com/reports/1391725) | GitHub Security Lab |  | - | 3 |  | Server-Side Request Forgery (SSRF) | Yet another SSRF query for Go |
| [1391728](https://hackerone.com/reports/1391728) | GitHub Security Lab |  | - | 3 |  | Server-Side Request Forgery (SSRF) | Yet another SSRF query for Javascript |
| [4461](https://hackerone.com/reports/4461) | Yahoo! |  | - | 2 |  | Server-Side Request Forgery (SSRF) | Server Side Request Forgery |
| [222667](https://hackerone.com/reports/222667) | Nextcloud | medium | - | 2 | 2017-05-15 | Server-Side Request Forgery (SSRF) | Possible SSRF in email server settings(SMTP mode) |
| [1069141](https://hackerone.com/reports/1069141) | h1-ctf | critical | - | 1 | 2021-01-11 | Server-Side Request Forgery (SSRF) | Infiltrating into Grinch-Networks and saving Christmas! |
