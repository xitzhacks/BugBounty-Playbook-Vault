---
title: "Vault class IDOR — Insecure Direct Object Reference"
type: dataset-view
class: "Insecure Direct Object Reference"
vault_category: "IDOR/"
rows: 373
paid_rows: 85
bounty_sum: 186,488
full_bodies_available: 166
source: "public HackerOne vault (hackerone disclosed), harvested 2026-11-17"
---

# IDOR — Insecure Direct Object Reference

373 rows · 85 with a bounty figure · **$186,488** total · 166 with full write-up stored.
Playbook: `Vault/IDOR/` · Dataset: `Vault/_VAULT/reports.sqlite` (`SELECT * FROM reports WHERE ...`).

| Report | Program | Severity | Bounty | Votes | Disclosed | Weakness | Title |
|---|---|---|---|---|---|---|---|
| [743953](https://hackerone.com/reports/743953) | GitLab | critical | $20,000 | 254 | 2022-06-07 | Insecure Direct Object Reference (IDOR) | Steal private objects of other projects via project import |
| [767770](https://hackerone.com/reports/767770) | GitLab | critical | $20,000 | 133 | 2022-06-07 | Insecure Direct Object Reference (IDOR) | Private objects exposed through project import |
| [1819832](https://hackerone.com/reports/1819832) | Snapchat | high | $15,000 | 801 | 2023-03-06 | Insecure Direct Object Reference (IDOR) | Delete anyone's content spotlight remotely. |
| [3862641](https://hackerone.com/reports/3862641) | HackerOne | critical | $15,000 | 372 | 2026-10-01 | Insecure Direct Object Reference (IDOR) | IDOR allows user to access report details via reference.json endpoint |
| [415081](https://hackerone.com/reports/415081) | PayPal | high | $10,500 | 797 | 2019-07-30 | Insecure Direct Object Reference (IDOR) | IDOR to add secondary users in www.paypal.com/businessmanage/users/api/v1/users |
| [3124517](https://hackerone.com/reports/3124517) | GitHub | high | $10,000 | 276 | 2025-09-23 | Insecure Direct Object Reference (IDOR) | Arbitrary Read of Another Users private repository without Authorization |
| [977212](https://hackerone.com/reports/977212) | Mail.ru |  | $10,000 | 186 |  | Insecure Direct Object Reference (IDOR) | read new emails from any inbox IOS APP in notification center |
| [1145428](https://hackerone.com/reports/1145428) | Uber | high | $5,750 | 58 | 2021-08-12 | Insecure Direct Object Reference (IDOR) | Chain of vulnerabilities in Uber for Business Vouchers program allows for attacker to perform arbitrary charges to victim's U4B payment account |
| [1213237](https://hackerone.com/reports/1213237) | Reddit | high | $5,000 | 267 | 2021-10-21 | Insecure Direct Object Reference (IDOR) | Deleting all DMs on RedditGifts.com |
| [2207248](https://hackerone.com/reports/2207248) | Shopify | medium | $5,000 | 187 | 2024-02-08 | Insecure Direct Object Reference (IDOR) | IDOR on GraphQL queries BillingDocumentDownload and BillDetails |
| [1658418](https://hackerone.com/reports/1658418) | Reddit | high | $5,000 | 163 | 2022-08-04 | Insecure Direct Object Reference (IDOR) | Getting access of mod logs from any public or restricted subreddit with IDOR vulnerability |
| [950507](https://hackerone.com/reports/950507) | Mail.ru |  | $5,000 | 31 |  | Insecure Direct Object Reference (IDOR) | Possible access to the car's photo and registration by its ID on [fleet.city-mobil.ru] |
| [1250037](https://hackerone.com/reports/1250037) | Stripe | critical | $3,000 | 149 | 2022-01-21 | Insecure Direct Object Reference (IDOR) | Email change or personal data change on the account. |
| [723461](https://hackerone.com/reports/723461) | Mail.ru |  | $3,000 | 125 |  | Insecure Direct Object Reference (IDOR) | [api.pandao.ru] IDOR for order delivery address |
| [2483666](https://hackerone.com/reports/2483666) | HackerOne | low | $2,500 | 110 | 2024-06-19 | Insecure Direct Object Reference (IDOR) | [IDOR] Improper Access Control on Embedded Submission Form |
| [1392630](https://hackerone.com/reports/1392630) | TikTok | medium | $2,500 | 74 | 2021-12-03 | Insecure Direct Object Reference (IDOR) | IDOR the ability to view support tickets of any user on seller platform |
| [924914](https://hackerone.com/reports/924914) | Mail.ru |  | $2,500 | 42 |  | Insecure Direct Object Reference (IDOR) | Access to information about any video and its owner via GraphQL endpoint [dictor.mail.ru] |
| [397137](https://hackerone.com/reports/397137) | New Relic |  | $2,500 | 37 |  | Insecure Direct Object Reference (IDOR) | [NR Insights] Pull any Insights/NRQL data from any NR account |
| [459443](https://hackerone.com/reports/459443) | New Relic |  | $2,500 | 28 |  | Insecure Direct Object Reference (IDOR) | [NR Insights] IDOR - Modify the filter settings for any NR Insights dashboard through internal_api endpoint |
| [462321](https://hackerone.com/reports/462321) | New Relic |  | $2,000 | 8 |  | Insecure Direct Object Reference (IDOR) | Ability to view monitor names of other NR accounts through internal API (v3) via "monitor_id" parameter |
| [1751258](https://hackerone.com/reports/1751258) | GitLab | medium | $1,730 | 29 | 2023-06-02 | Insecure Direct Object Reference (IDOR) | Attacker is able to create,Edit & delete notes and leak the title of a victim's private personal snippet |
| [380410](https://hackerone.com/reports/380410) | Pornhub |  | $1,500 | 266 |  | Insecure Direct Object Reference (IDOR) | idor allows you to delete photos and album from a gallery |
| [681473](https://hackerone.com/reports/681473) | Pornhub |  | $1,500 | 248 |  | Insecure Direct Object Reference (IDOR) | IDOR allows any user to edit others videos |
| [349291](https://hackerone.com/reports/349291) | New Relic |  | $1,500 | 77 |  | Insecure Direct Object Reference (IDOR) | IDOR via internal_api "users" endpoint |
| [980511](https://hackerone.com/reports/980511) | Shopify | medium | $1,500 | 72 | 2020-10-22 | Insecure Direct Object Reference (IDOR) | A staff member with no permissions can edit Store Customer Email |
| [332381](https://hackerone.com/reports/332381) | New Relic |  | $1,500 | 63 |  | Insecure Direct Object Reference (IDOR) | Internal API endpoint discloses full account name of email address associated with unconfirmed user |
| [320173](https://hackerone.com/reports/320173) | New Relic |  | $1,500 | 37 |  | Insecure Direct Object Reference (IDOR) | Bypass of my three other reports #267636 + #255894 + #271861 - (IDOR) Ability to see full name associated with other New Relic accounts |
| [514897](https://hackerone.com/reports/514897) | Eternal | medium | $1,500 | 29 | 2020-07-15 | Insecure Direct Object Reference (IDOR) | Possible to enumerate Addresses of users using AddressId and guessing the delivery_subzone |
| [267636](https://hackerone.com/reports/267636) | New Relic |  | $1,500 | 15 |  | Insecure Direct Object Reference (IDOR) | [NR Synthetics] (IDOR) Ability to see full name associated with other New Relic accounts through workaround of #255894 |
| [419875](https://hackerone.com/reports/419875) | New Relic |  | $1,500 | 14 |  | Insecure Direct Object Reference (IDOR) | [NR Alerts/Synthetics] IDOR through /policies.json with Synthetics exposes full name of other NR users |
| [344309](https://hackerone.com/reports/344309) | New Relic |  | $1,500 | 10 |  | Insecure Direct Object Reference (IDOR) | Adding a new user discloses their full name in the "Users" section of NR Alerts notification channels page |
| [347665](https://hackerone.com/reports/347665) | New Relic |  | $1,500 | 5 |  | Insecure Direct Object Reference (IDOR) | Permissions leaks the full name of other NR accounts - Regression of #267636 |
| [1410498](https://hackerone.com/reports/1410498) | Judge.me | high | $1,250 | 47 | 2022-03-31 | Insecure Direct Object Reference (IDOR) | IDOR: leak buyer info & Publish/Hide foreign comments |
| [2528293](https://hackerone.com/reports/2528293) | GitLab | medium | $1,160 | 117 | 2024-10-01 | Insecure Direct Object Reference (IDOR) | IDOR Exposes All Machine Learning Models |
| [1892200](https://hackerone.com/reports/1892200) | GitLab | medium | $1,160 | 22 | 2023-06-02 | Insecure Direct Object Reference (IDOR) | Attacker can create malicious child epics linked to a victim's epic in an unrelated group |
| [484339](https://hackerone.com/reports/484339) | Mail.ru |  | $1,000 | 33 |  | Insecure Direct Object Reference (IDOR) | [api.pandao.ru] IDOR позволяет изменять адрес любого пользователя |
| [271393](https://hackerone.com/reports/271393) | New Relic |  | $1,000 | 16 |  | Insecure Direct Object Reference (IDOR) | NR Internal_API call allows me to read the events/violations/policies/messages of ANY New Relic account (AND pull data from infrastructure) |
| [853130](https://hackerone.com/reports/853130) | Shopify | medium | $750 | 13 | 2020-07-14 | Insecure Direct Object Reference (IDOR) | IDOR on stocky application-Low Stock-Varient-Settings-Columns |
| [1646340](https://hackerone.com/reports/1646340) | Showmax |  | $700 | 31 |  | Insecure Direct Object Reference (IDOR) | delete the subaccount from the user id |
| [869705](https://hackerone.com/reports/869705) | OPPO |  | $600 | 73 |  | Insecure Direct Object Reference (IDOR) | Arbitrary thread deletion on c.realme.com |
| [404797](https://hackerone.com/reports/404797) | Eternal | low | $600 | 67 | 2018-09-05 | Insecure Direct Object Reference (IDOR) | IDOR to delete images from other stores |
| [1718574](https://hackerone.com/reports/1718574) | Linktree | medium | $600 | 55 | 2022-10-25 | Insecure Direct Object Reference (IDOR) | A malicious admin can be able to permanently disable a Owner(Admin) to access his account |
| [2541962](https://hackerone.com/reports/2541962) | pixiv | medium | $500 | 149 | 2026-01-18 | Insecure Direct Object Reference (IDOR) | Disclose Hidden Comments on Media Section of hub.vroid.com |
| [819807](https://hackerone.com/reports/819807) | Nextcloud | high | $500 | 141 | 2020-04-19 | Insecure Direct Object Reference (IDOR) | Missing ownership check on remote wipe endpoint |
| [2848610](https://hackerone.com/reports/2848610) | TikTok | low | $500 | 131 | 2025-02-20 | Insecure Direct Object Reference (IDOR) | IDOR on ads.tiktok.com Allows Unauthorized Product Addition |
| [2381816](https://hackerone.com/reports/2381816) | Tools for Humanity | medium | $500 | 91 | 2024-05-09 | Insecure Direct Object Reference (IDOR) | IDOR - Leaking of team data (name, email, ID, member ID) via POST /api/v1/graphql  `FetchMemberships` operation |
| [1323406](https://hackerone.com/reports/1323406) | Affirm | medium | $500 | 87 | 2021-12-06 | Insecure Direct Object Reference (IDOR) | IDOR to view order information of users and personal information |
| [1626508](https://hackerone.com/reports/1626508) | U.S. Dept Of Defense | high | $500 | 77 | 2024-06-27 | Insecure Direct Object Reference (IDOR) | IDOR leading unauthenticated attacker to download documents discloses PII of users and soldiers via https://www.█████████/Download.aspx?id= [HtUS] |
| [703894](https://hackerone.com/reports/703894) | GitLab | low | $500 | 49 | 2021-02-02 | Insecure Direct Object Reference (IDOR) | View the Starred Projects in a Private Profile |
| [743687](https://hackerone.com/reports/743687) | Mail.ru |  | $500 | 48 |  | Insecure Direct Object Reference (IDOR) | IDOR of users |
| [308610](https://hackerone.com/reports/308610) | Valve | medium | $500 | 34 | 2018-05-09 | Insecure Direct Object Reference (IDOR) | Read Access to all comments on unauthorized forums' discussions! IDOR! |
| [243943](https://hackerone.com/reports/243943) | Shopify | medium | $500 | 33 | 2017-07-19 | Insecure Direct Object Reference (IDOR) | IDOR [partners.shopify.com] - User with ONLY Manage apps permission is able to get shops info and staff names from inside the shop |
| [1559739](https://hackerone.com/reports/1559739) | TikTok | low | $500 | 25 | 2022-07-22 | Insecure Direct Object Reference (IDOR) | IDOR in report download functionality on ads.tiktok.com |
| [790829](https://hackerone.com/reports/790829) | Razer |  | $500 | 21 |  | Insecure Direct Object Reference (IDOR) | IDOR in eform.molpay.com leads to see other users application forms with private data |
| [754044](https://hackerone.com/reports/754044) | Razer |  | $500 | 12 |  | Insecure Direct Object Reference (IDOR) | [Razer Pay Mobile App] IDOR within /v1_IM/friends/queryDrawRedLog allowed unauthorised access to read logs |
| [287378](https://hackerone.com/reports/287378) | Mail.ru |  | $500 | 8 |  | Insecure Direct Object Reference (IDOR) | Possibility to view subdepartments for arbitrary domain |
| [285432](https://hackerone.com/reports/285432) | Open-Xchange |  | $400 | 13 |  | Insecure Direct Object Reference (IDOR) | IDOR - setAttribute action of user object in API |
| [948481](https://hackerone.com/reports/948481) | Mail.ru |  | $400 | 5 |  | Insecure Direct Object Reference (IDOR) | В самокате можно просматривать и изменять данные любого заказа без авторизации |
| [661978](https://hackerone.com/reports/661978) | Phabricator |  | $300 | 36 | 2019-08-29 | Insecure Direct Object Reference (IDOR) | IDOR bug to See hidden slowvote of any user even when you dont have access right |
| [302485](https://hackerone.com/reports/302485) | Open-Xchange |  | $300 | 14 |  | Insecure Direct Object Reference (IDOR) | IDOR allow to extract all registered email |
| [544329](https://hackerone.com/reports/544329) | X / xAI | medium | $289 | 141 | 2019-06-14 | Insecure Direct Object Reference (IDOR) | IDOR and statistics leakage in Orders |
| [788375](https://hackerone.com/reports/788375) | Visma Public |  | $250 | 49 |  | Insecure Direct Object Reference (IDOR) | A user can view the name and number of a customer in another company if the GUID is known |
| [265258](https://hackerone.com/reports/265258) | Eternal | high | $250 | 41 | 2017-10-22 | Insecure Direct Object Reference (IDOR) | IDOR to cancel any table booking and leak sensitive information such as email,mobile number,uuid |
| [808997](https://hackerone.com/reports/808997) | Visma Public |  | $250 | 24 |  | Insecure Direct Object Reference (IDOR) | [IDOR]Ability to View/Delete/Edit (Forward to attachment archive) Email of other user if GUID is known. |
| [333767](https://hackerone.com/reports/333767) | Open-Xchange |  | $250 | 12 |  | Insecure Direct Object Reference (IDOR) | IDOR to view other user folder name |
| [809967](https://hackerone.com/reports/809967) | Visma Public |  | $250 | 5 |  | Insecure Direct Object Reference (IDOR) | [IDOR]Ability to edit Description of api_key's of other users. |
| [811566](https://hackerone.com/reports/811566) | Visma Public |  | $250 | 5 |  | Insecure Direct Object Reference (IDOR) | [IDOR]Ability to Pause & Resume the Invoice of other users If GUID is known. |
| [2590608](https://hackerone.com/reports/2590608) | Internet Bug Bounty | low | $249 | 34 | 2024-10-16 | Insecure Direct Object Reference (IDOR) | fs.fchown/fchmod bypasses permission model |
| [906907](https://hackerone.com/reports/906907) | IRCCloud | high | $200 | 66 | 2020-07-26 | Insecure Direct Object Reference (IDOR) | IDOR with Geolocation data not stripped from images |
| [3484601](https://hackerone.com/reports/3484601) | Nextcloud | low | $200 | 19 | 2026-09-17 | Insecure Direct Object Reference (IDOR) | Team membership information returned on API level based on ID |
| [3511998](https://hackerone.com/reports/3511998) | Nextcloud | low | $150 | 87 | 2026-05-08 | Insecure Direct Object Reference (IDOR) | Private circle can be added to another circle via API despite visibility restriction |
| [847876](https://hackerone.com/reports/847876) | Mail.ru |  | $150 | 20 |  | Insecure Direct Object Reference (IDOR) | IDOR in tracking driver logs at city-mobil.ru |
| [916704](https://hackerone.com/reports/916704) | Nextcloud | medium | $150 | 20 | 2020-09-29 | Insecure Direct Object Reference (IDOR) | Access control missing while viewing the attachments in the "All boards" |
| [923851](https://hackerone.com/reports/923851) | Mail.ru |  | $150 | 16 |  | Insecure Direct Object Reference (IDOR) | IDOR of contracts on dictor.mail.ru |
| [952174](https://hackerone.com/reports/952174) | Mail.ru |  | $150 | 6 |  | Insecure Direct Object Reference (IDOR) | Ability to edit the address of any company by its id on [corporate.city-mobil.ru] |
| [959329](https://hackerone.com/reports/959329) | Mail.ru |  | $150 | 5 |  | Insecure Direct Object Reference (IDOR) | В самокат имеется возможность просмотра суммы заказа и номера заказа по ID [smart.space] |
| [1086453](https://hackerone.com/reports/1086453) | Mail.ru |  | $150 | 5 |  | Insecure Direct Object Reference (IDOR) | restaurant.delivery-club.ru - возможность получить информацию об чужих акциях. |
| [958769](https://hackerone.com/reports/958769) | Mail.ru |  | $150 | 3 |  | Insecure Direct Object Reference (IDOR) | Возможность просмотра коментариев к чужим обращениям [corporate.city-mobil.ru] |
| [3467641](https://hackerone.com/reports/3467641) | Basecamp | low | $100 | 76 | 2026-03-16 | Insecure Direct Object Reference (IDOR) | Unauthenticated access to private files on app.fizzy.do via Active Storage URLs leads to information disclosure |
| [1182465](https://hackerone.com/reports/1182465) | Acronis | medium | $100 | 48 | 2021-08-31 | Insecure Direct Object Reference (IDOR) | IDOR on www.acronis.com API lead to steal private business user information |
| [835005](https://hackerone.com/reports/835005) | Helium | medium | $100 | 40 | 2020-05-27 | Insecure Direct Object Reference (IDOR) | Organization Takeover via invitation API |
| [1727044](https://hackerone.com/reports/1727044) | Liberapay | medium | $100 | 34 | 2022-10-09 | Insecure Direct Object Reference (IDOR) | Email Address Exposure via Gratipay Migration Tool |
| [344145](https://hackerone.com/reports/344145) | Eternal | low | $100 | 21 | 2018-04-28 | Insecure Direct Object Reference (IDOR) | [www.zomato.com] IDOR - Gold Subscription Details, Able to view "Membership ID" and "Validity Details" of other Users |
| [297751](https://hackerone.com/reports/297751) | Nextcloud | low | $100 | 18 | 2018-02-08 | Insecure Direct Object Reference (IDOR) | Registered users can change app password permissions for any user |
| [245969](https://hackerone.com/reports/245969) | Eternal | low | $50 | 25 | 2017-11-28 | Insecure Direct Object Reference (IDOR) | Use any User to Follow you (Increase Followers) [IDOR] |
| [762510](https://hackerone.com/reports/762510) | HackerOne | none | - | 471 | 2019-12-20 | Insecure Direct Object Reference (IDOR) | How the Bug stole hacking |
| [2122671](https://hackerone.com/reports/2122671) | HackerOne | high | - | 395 | 2023-08-29 | Insecure Direct Object Reference (IDOR) | IDOR - Delete all Licenses and certifications from users account using CreateOrUpdateHackerCertification GraphQL query |
| [751577](https://hackerone.com/reports/751577) | Nord Security |  | - | 387 |  | Insecure Direct Object Reference (IDOR) | IDOR allow access to payments data of any user |
| [1969141](https://hackerone.com/reports/1969141) | HackerOne | high | - | 346 | 2023-05-03 | Insecure Direct Object Reference (IDOR) | Insecure Direct Object Reference (IDOR) - Delete Campaigns |
| [2442008](https://hackerone.com/reports/2442008) | HackerOne | critical | - | 340 | 2024-04-29 | Insecure Direct Object Reference (IDOR) | Attachment disclosure via summary report |
| [2487889](https://hackerone.com/reports/2487889) | HackerOne | critical | - | 266 | 2024-05-23 | Insecure Direct Object Reference (IDOR) | Insecure Direct Object Reference (IDOR) Allows Viewing Private Report Details via /bugs.json Endpoint |
| [876300](https://hackerone.com/reports/876300) | Starbucks | critical | - | 260 | 2020-07-28 | Insecure Direct Object Reference (IDOR) | Singapore - Account Takeover via IDOR |
| [3154983](https://hackerone.com/reports/3154983) | Mozilla | high | - | 244 | 2025-06-03 | Insecure Direct Object Reference (IDOR) | IDOR: Account Deletion via Session Misbinding – Attacker Can Delete Victim Account |
| [703058](https://hackerone.com/reports/703058) | Roblox | medium | - | 233 | 2020-04-26 | Insecure Direct Object Reference (IDOR) | Insecure redirect rule results in bypassing ban redirect on certain pages |
| [1966006](https://hackerone.com/reports/1966006) | Unikrn | high | - | 232 | 2023-07-17 | Insecure Direct Object Reference (IDOR) | An IDOR that can lead to enumeration of a user and disclosure of email and phone number within cashier |
| [1475520](https://hackerone.com/reports/1475520) | TikTok | high | - | 216 | 2022-03-02 | Insecure Direct Object Reference (IDOR) | IDOR delete any Tickets on ads.tiktok.com |
| [391092](https://hackerone.com/reports/391092) | Yelp | critical | - | 214 | 2020-08-19 | Insecure Direct Object Reference (IDOR) | I.D.O.R To Order,Book,Buy,reserve On YELP FOR FREE (UNAUTHORIZED USE OF OTHER USER'S CREDIT CARD) |
| [2218334](https://hackerone.com/reports/2218334) | HackerOne | medium | - | 210 | 2023-10-25 | Insecure Direct Object Reference (IDOR) | IDOR vulnerability in unreleased HackerOne Copilot feature |
| [1661113](https://hackerone.com/reports/1661113) | Reddit | high | - | 208 | 2022-09-30 | Insecure Direct Object Reference (IDOR) | IDOR allows an attacker to modify the links of any user |
| [915114](https://hackerone.com/reports/915114) | Automattic | critical | - | 202 | 2020-11-18 | Insecure Direct Object Reference (IDOR) | IDOR when editing users leads to Account Takeover without User Interaction at CrowdSignal |
| [2633771](https://hackerone.com/reports/2633771) | HackerOne | medium | - | 178 | 2025-06-08 | Insecure Direct Object Reference (IDOR) | IDOR Vulnerability at AddTagToAssets operation name |
| [974222](https://hackerone.com/reports/974222) | Automattic | high | - | 177 | 2020-11-18 | Insecure Direct Object Reference (IDOR) | IDOR leads to Edit Anyone's Blogs / Websites |
| [2868084](https://hackerone.com/reports/2868084) | TikTok | medium | - | 167 | 2025-01-24 | Insecure Direct Object Reference (IDOR) | Unauthorized Access to TikTok Account [Private Videos] via API Endpoint |
| [536853](https://hackerone.com/reports/536853) | HackerOne | low | - | 161 | 2019-04-23 | Insecure Direct Object Reference (IDOR) | Unreleased CTF Levels are Revealed on /group/user/ID1?user=USERID endpoint |
| [534794](https://hackerone.com/reports/534794) | GitLab | high | - | 148 | 2019-12-11 | Insecure Direct Object Reference (IDOR) | Importing GitLab project archives can replace uploads of other users |
| [1403176](https://hackerone.com/reports/1403176) | Acronis | medium | - | 146 | 2021-11-30 | Insecure Direct Object Reference (IDOR) | IDOR vulnerability (Price manipulation) |
| [2495989](https://hackerone.com/reports/2495989) | MercadoLibre | critical | - | 144 | 2025-03-06 | Insecure Direct Object Reference (IDOR) | Sale cancellations from other sellers without restrictions |
| [1773609](https://hackerone.com/reports/1773609) | MTN Group | critical | - | 135 | 2024-10-05 | Insecure Direct Object Reference (IDOR) | IDOR at mtnmobad.mtnbusiness.com.ng leads to PII leakage. |
| [3085742](https://hackerone.com/reports/3085742) | Bykea | medium | - | 128 | 2025-06-13 | Insecure Direct Object Reference (IDOR) | IDOR on in-app hardcoded zombie endpoint |
| [990878](https://hackerone.com/reports/990878) | CS Money | medium | - | 127 | 2020-09-28 | Insecure Direct Object Reference (IDOR) | IDOR in https://3d.cs.money/ |
| [2524562](https://hackerone.com/reports/2524562) | WakaTime |  | - | 126 | 2024-06-02 | Insecure Direct Object Reference (IDOR) | IDOR to view order information of users and personal information |
| [1116387](https://hackerone.com/reports/1116387) | Uber | medium | - | 123 | 2021-04-29 | Insecure Direct Object Reference (IDOR) | IDOR leads to leak analytics of any restaurant |
| [1733627](https://hackerone.com/reports/1733627) | TikTok | high | - | 123 | 2023-01-27 | Insecure Direct Object Reference (IDOR) | IDOR for changing privacy settings on any memories |
| [1618100](https://hackerone.com/reports/1618100) | A.S. Watson Group |  | - | 118 |  | Insecure Direct Object Reference (IDOR) | PII Disclosure At `theperfumeshop.com/register/forOrder` |
| [1716300](https://hackerone.com/reports/1716300) | LinkedIn | high | - | 117 | 2023-03-29 | Insecure Direct Object Reference (IDOR) | Unauthorized User can View Subscribers of Other Users Newsletters |
| [1137819](https://hackerone.com/reports/1137819) | Uber | medium | - | 112 | 2021-05-28 | Insecure Direct Object Reference (IDOR) | IDOR leads to See analytics of Loyalty Program in any restaurant. |
| [1777095](https://hackerone.com/reports/1777095) | LinkedIn | high | - | 112 | 2022-12-07 | Insecure Direct Object Reference (IDOR) | Unauthorized access to resumes stored on LinkedIn |
| [1527906](https://hackerone.com/reports/1527906) | TikTok | medium | - | 109 | 2022-09-01 | Insecure Direct Object Reference (IDOR) | IDOR on TikTok Ads Endpoint |
| [2374730](https://hackerone.com/reports/2374730) | Bykea | high | - | 108 | 2025-06-13 | Insecure Direct Object Reference (IDOR) | Broken Access Control (IDOR) in Booking Detail and Bids Could Leads to Sensitive Information Disclosure |
| [3560256](https://hackerone.com/reports/3560256) | GitHub | medium | - | 108 | 2026-05-19 | Insecure Direct Object Reference (IDOR) | Cross-repository IDOR in `/settings/security_analysis/bypass_reviewers` allows unauthorized delegated bypass reviewer modification |
| [1286332](https://hackerone.com/reports/1286332) | TikTok | high | - | 107 | 2022-05-06 | Insecure Direct Object Reference (IDOR) | Multiple IDORs in family pairing api |
| [1328278](https://hackerone.com/reports/1328278) | Stripe | medium | - | 100 | 2022-01-19 | Insecure Direct Object Reference (IDOR) | User can pay using archived price by manipulating the request sent to `POST /v1/payment_pages/for_plink` |
| [1608735](https://hackerone.com/reports/1608735) | LinkedIn | medium | - | 99 | 2023-08-24 | Insecure Direct Object Reference (IDOR) | IDOR allows an attacker to delete anyone's featured photo. |
| [1770858](https://hackerone.com/reports/1770858) | Semrush | critical | - | 99 | 2024-03-07 | Insecure Direct Object Reference (IDOR) | IDOR vulnerability reveals additional information |
| [2756402](https://hackerone.com/reports/2756402) | Mars | critical | - | 98 | 2024-11-26 | Insecure Direct Object Reference (IDOR) | █████████ when adding branches to your account |
| [915127](https://hackerone.com/reports/915127) | Automattic | high | - | 94 | 2020-11-18 | Insecure Direct Object Reference (IDOR) | IDOR when moving contents at CrowdSignal |
| [2291999](https://hackerone.com/reports/2291999) | LinkedIn | high | - | 94 | 2024-03-12 | Insecure Direct Object Reference (IDOR) | An attacker can submit arbitrary projects to their service accounts and obtain full information on projects of other users. |
| [3506183](https://hackerone.com/reports/3506183) | GitHub | high | - | 92 | 2026-03-05 | Insecure Direct Object Reference (IDOR) | Missing Access Control in MigrationFile allows attacker to upload files to any Migration |
| [1034346](https://hackerone.com/reports/1034346) | HackerOne | high | - | 91 | 2020-11-17 | Insecure Direct Object Reference (IDOR) | Security@ email forwarding and Embedded Submission drafts can be used to obtain copy of deleted attachments from other HackerOne users |
| [697412](https://hackerone.com/reports/697412) | Kindred Group |  | - | 89 |  | Insecure Direct Object Reference (IDOR) | [unibet.com] Delete messages via IDOR at /mom-api/messages/unibet_█████████@unibet/ |
| [1734639](https://hackerone.com/reports/1734639) | LinkedIn | medium | - | 87 | 2026-03-06 | Insecure Direct Object Reference (IDOR) | IDOR to make someone attend or leave an event |
| [1005315](https://hackerone.com/reports/1005315) | Mail.ru |  | - | 86 |  | Insecure Direct Object Reference (IDOR) | Access User Tickets via IDOR in [widget.support.my.games] |
| [2028450](https://hackerone.com/reports/2028450) | Rocket.Chat | low | - | 86 | 2024-10-13 | Insecure Direct Object Reference (IDOR) | IDOR vulnerability leads to Deleting message after leaving/getting banned from group using message ID |
| [984965](https://hackerone.com/reports/984965) | TikTok | high | - | 84 | 2021-04-02 | Insecure Direct Object Reference (IDOR) | Cross-Tenant IDOR ( graphql `AddRulesToPixelEvents` query ) allowing to add, update, and delete rules of any Pixel events on the platform |
| [1808719](https://hackerone.com/reports/1808719) | LinkedIn | high | - | 84 | 2023-08-24 | Insecure Direct Object Reference (IDOR) | Attackers can use TRIAL Premium only by paying **IDR 10,000.00** from the original price of `IDR462,400.00` per month |
| [2382484](https://hackerone.com/reports/2382484) | Mozilla | high | - | 84 | 2024-03-07 | Insecure Direct Object Reference (IDOR) | IDOR on Delete Email address features |
| [3360354](https://hackerone.com/reports/3360354) | Nextcloud | low | - | 84 | 2026-02-06 | Insecure Direct Object Reference (IDOR) | WebAuthn app was updated based on public key |
| [2921830](https://hackerone.com/reports/2921830) | TikTok | low | - | 82 | 2025-06-27 | Insecure Direct Object Reference (IDOR) | Unauthorized Access to Private Video Description via Translation API for Private Accounts |
| [2867022](https://hackerone.com/reports/2867022) | Bykea | medium | - | 80 | 2025-06-26 | Insecure Direct Object Reference (IDOR) | Improper Access Control Allows Trip Hijacking and Passenger/Driver PII Disclosure |
| [2968039](https://hackerone.com/reports/2968039) | Autodesk | high | - | 80 | 2025-02-21 | Insecure Direct Object Reference (IDOR) | Insecure Direct Object Reference (IDOR) in GraphQL deleteProfileImages Mutation |
| [262661](https://hackerone.com/reports/262661) | HackerOne | low | - | 79 | 2017-09-02 | Insecure Direct Object Reference (IDOR) | IDOR on HackerOne Feedback Review |
| [2944357](https://hackerone.com/reports/2944357) | Yelp | high | - | 79 | 2025-01-29 | Insecure Direct Object Reference (IDOR) | Unauthorized Reservation Cancellation Through IDOR Vulnerability |
| [3604288](https://hackerone.com/reports/3604288) | LinkedIn | medium | - | 77 | 2026-03-24 | Insecure Direct Object Reference (IDOR) | Access to Deactivated LinkedIn Company Pages via Competitor Analytics API |
| [717729](https://hackerone.com/reports/717729) | HackerOne | medium | - | 76 | 2019-10-25 | Insecure Direct Object Reference (IDOR) | Reporter, external users, collaborators can mark sent swag awarded to reporter as unsent |
| [2861888](https://hackerone.com/reports/2861888) | Bykea | medium | - | 76 | 2025-06-13 | Insecure Direct Object Reference (IDOR) | Ability to increase any customer offered fare (BAC) |
| [1816900](https://hackerone.com/reports/1816900) | Semrush | high | - | 74 | 2024-03-05 | Insecure Direct Object Reference (IDOR) | IDOR allows information disclosure |
| [3734326](https://hackerone.com/reports/3734326) | Rocket.Chat | high | - | 74 | 2026-05-25 | Insecure Direct Object Reference (IDOR) | Autotranslate DDP Method Exposes Private Messages Without Authentication or Room Access Check |
| [2965357](https://hackerone.com/reports/2965357) | Autodesk | medium | - | 73 | 2025-02-19 | Insecure Direct Object Reference (IDOR) | Insecure Direct Object Reference (IDOR) Vulnerability in Autodesk User Profile |
| [3799010](https://hackerone.com/reports/3799010) | Nextcloud | medium | - | 73 | 2026-08-14 | Insecure Direct Object Reference (IDOR) | TaskProcessing callback authorization bypass allows ex-members to post as Assistant Talk Bot |
| [1656380](https://hackerone.com/reports/1656380) | Reddit | medium | - | 72 | 2022-10-03 | Insecure Direct Object Reference (IDOR) | Reddit talk promotion offers don't expire, allowing users to accept them after being demoted |
| [3869124](https://hackerone.com/reports/3869124) | Weblate | high | - | 72 | 2026-08-30 | Insecure Direct Object Reference (IDOR) | **Unauthenticated IDOR allows modification of payment customer billing information** |
| [2024284](https://hackerone.com/reports/2024284) | Glassdoor |  | - | 71 |  | Insecure Direct Object Reference (IDOR) | IDOR vulnerability on profile picture changing mechanism which discloses other user's profile picture. |
| [3527771](https://hackerone.com/reports/3527771) | GitHub | medium | - | 71 | 2026-03-19 | Insecure Direct Object Reference (IDOR) | Add labels to arbitrary issues/prs & compromise github actions label checks |
| [2962056](https://hackerone.com/reports/2962056) | Autodesk | medium | - | 69 | 2025-02-19 | Insecure Direct Object Reference (IDOR) | IDOR Vulnerability Allowing Unauthorized Profile Picture Change |
| [843160](https://hackerone.com/reports/843160) | Mail.ru |  | - | 68 |  | Insecure Direct Object Reference (IDOR) | Account takeover through password reset in cups.mail.ru |
| [3417162](https://hackerone.com/reports/3417162) | lemlist | critical | - | 68 | 2025-11-17 | Insecure Direct Object Reference (IDOR) | Authentication Bypass in Subscription Management Endpoint |
| [510759](https://hackerone.com/reports/510759) | HackerOne | low | - | 67 | 2019-09-06 | Insecure Direct Object Reference (IDOR) | IDOR in Report CSV export discloses the IDs of Custom Field Attributes of Programs |
| [1096560](https://hackerone.com/reports/1096560) | X / xAI | critical | - | 67 | 2021-05-26 | Insecure Direct Object Reference (IDOR) | Ability to add arbitrary images/descriptions/titles to ohter people's issues via IDOR on getrevue.co |
| [1947924](https://hackerone.com/reports/1947924) | Rockstar Games | medium | - | 67 | 2023-08-17 | Insecure Direct Object Reference (IDOR) | Insecure Direct Object Reference allows Crew Invite deletion |
| [2322663](https://hackerone.com/reports/2322663) | MTN Group | medium | - | 66 | 2025-01-31 | Insecure Direct Object Reference (IDOR) | Insecure direct Object Reference(Horizontal Escalation) |
| [2393021](https://hackerone.com/reports/2393021) | Mars | high | - | 66 | 2024-11-21 | Insecure Direct Object Reference (IDOR) | Upload profile photo and  Pets addition - IDOR |
| [469372](https://hackerone.com/reports/469372) | Kaspersky | medium | - | 65 | 2019-11-25 | Insecure Direct Object Reference (IDOR) | Web protection component in Anti-Virus products family uses predictable links for certificate warnings |
| [717716](https://hackerone.com/reports/717716) | HackerOne | medium | - | 65 | 2019-10-21 | Insecure Direct Object Reference (IDOR) | Any user with access to program can resume and suspend HackerOne Gateway |
| [842625](https://hackerone.com/reports/842625) | Rocket.Chat | critical | - | 65 | 2020-06-14 | Insecure Direct Object Reference (IDOR) | account takeover on 3.0.1 version |
| [1581528](https://hackerone.com/reports/1581528) | LinkedIn | medium | - | 65 | 2022-07-20 | Insecure Direct Object Reference (IDOR) | Can access the job name, creator name and can report any draft/under review/rejected job |
| [797685](https://hackerone.com/reports/797685) | Semrush | medium | - | 64 | 2020-04-02 | Insecure Direct Object Reference (IDOR) | IDOR in marketing calendar tool |
| [1148697](https://hackerone.com/reports/1148697) | Uber | high | - | 64 | 2022-04-07 | Insecure Direct Object Reference (IDOR) | Chain of IDORs Between U4B and Vouchers APIs Allows Attackers to View and Modify Program/Voucher Policies and to Obtain Organization Employees' PII |
| [2210179](https://hackerone.com/reports/2210179) | GitHub | medium | - | 64 | 2024-01-08 | Insecure Direct Object Reference (IDOR) | View Repo and Title of Any Private Check Run |
| [2586584](https://hackerone.com/reports/2586584) | U.S. Dept Of Defense | medium | - | 64 | 2024-07-19 | Insecure Direct Object Reference (IDOR) | IDOR leads to PII Leak |
| [1555376](https://hackerone.com/reports/1555376) | TikTok | medium | - | 63 | 2022-09-20 | Insecure Direct Object Reference (IDOR) | IDOR on Tagged People |
| [1505567](https://hackerone.com/reports/1505567) | TikTok | medium | - | 62 | 2022-05-16 | Insecure Direct Object Reference (IDOR) | Privilege Escalation on TikTok for Business |
| [983070](https://hackerone.com/reports/983070) | Logitech | low | - | 61 | 2020-11-26 | Insecure Direct Object Reference (IDOR) | IDOR when creating App on [platform.streamlabs.com/api/v1/store/whitelist] with user_id field |
| [1737943](https://hackerone.com/reports/1737943) | Flickr | medium | - | 61 | 2024-07-06 | Insecure Direct Object Reference (IDOR) | IDOR may allow access to non-public photos |
| [1061292](https://hackerone.com/reports/1061292) | U.S. General Services Administration | high | - | 60 | 2021-05-07 | Insecure Direct Object Reference (IDOR) | TAMS registration details API for admins open at https://tamsapi.gsa.gov/user/tams/api/usermgmnt/pendingUserDetails/ |
| [2894018](https://hackerone.com/reports/2894018) | Bykea | medium | - | 60 | 2025-06-12 | Insecure Direct Object Reference (IDOR) | Lack of Feedback Validation Permits Arbitrary Driver Ratings |
| [3304830](https://hackerone.com/reports/3304830) | Nextcloud | low | - | 60 | 2026-05-08 | Insecure Direct Object Reference (IDOR) | Files drop share links for end-to-end encrypted folders allowed to drop files into other folders of the share owner |
| [1644436](https://hackerone.com/reports/1644436) | EXNESS | medium | - | 58 | 2022-12-05 | Insecure Direct Object Reference (IDOR) | IDOR in Stats API Endpoint Allows Viewing Equity or Net Profit of Any MT Account |
| [1695454](https://hackerone.com/reports/1695454) | Automattic | critical | - | 58 | 2022-11-01 | Insecure Direct Object Reference (IDOR) | IDOR in API applications (able to see any API token, leads to account takeover) |
| [2085185](https://hackerone.com/reports/2085185) | IBM | critical | - | 57 | 2023-08-31 | Insecure Direct Object Reference (IDOR) | IDOR in upload videos of a Channel on https://video.ibm.com |
| [2357113](https://hackerone.com/reports/2357113) | Publitas | medium | - | 57 | 2024-03-13 | Insecure Direct Object Reference (IDOR) | Unauthorized Access to Offline Publication Cover Pages via SOURCE_DOCUMENT_ID |
| [2456603](https://hackerone.com/reports/2456603) | IBM | critical | - | 57 | 2024-05-01 | Insecure Direct Object Reference (IDOR) | Insecure Direct Object Reference Protection bypass by changing HTTP method in IBM Your Learning endpoint. |
| [3275810](https://hackerone.com/reports/3275810) | Nextcloud | low | - | 57 | 2025-12-05 | Insecure Direct Object Reference (IDOR) | Calendar app allowed booking appointments without the generated token |
| [1901713](https://hackerone.com/reports/1901713) | Acronis | high | - | 56 | 2024-11-13 | Insecure Direct Object Reference (IDOR) | IDOR in backup recovery functionality |
| [3401612](https://hackerone.com/reports/3401612) | Revive Adserver | high | - | 56 | 2025-11-19 | Insecure Direct Object Reference (IDOR) | IDOR Vulnerability in Banner Deletion |
| [447930](https://hackerone.com/reports/447930) | HackerOne | high | - | 54 | 2019-01-11 | Insecure Direct Object Reference (IDOR) | Embedded submission form UUIDs can be enumerated through GraphQL node interface, exposing sensitive program details |
| [1744194](https://hackerone.com/reports/1744194) | TikTok | high | - | 52 | 2022-11-10 | Insecure Direct Object Reference (IDOR) | Business Suite "Get Leads" Resulting in Revealing User Email & Phone |
| [2213900](https://hackerone.com/reports/2213900) | U.S. Dept Of Defense | medium | - | 52 | 2023-12-21 | Insecure Direct Object Reference (IDOR) | IDOR to delete profile images in https:███████ |
| [725569](https://hackerone.com/reports/725569) | Automattic |  | - | 51 | 2019-12-01 | Insecure Direct Object Reference (IDOR) | [IDOR] Attacker user can Approve/Decline AFK on the behalf of other users |
| [950881](https://hackerone.com/reports/950881) | Automattic | critical | - | 50 | 2020-11-18 | Insecure Direct Object Reference (IDOR) | IDOR when editing email leads to Account Takeover on Atavist |
| [1373784](https://hackerone.com/reports/1373784) | Lark Technologies | high | - | 50 | 2022-01-25 | Insecure Direct Object Reference (IDOR) | Able to steal private files by manipulating response using Compose Email function of Lark |
| [783708](https://hackerone.com/reports/783708) | Semrush | medium | - | 49 | 2020-02-28 | Insecure Direct Object Reference (IDOR) | IDOR in semrush academy |
| [3051155](https://hackerone.com/reports/3051155) | IBM |  | - | 49 | 2025-04-29 | Insecure Direct Object Reference (IDOR) | Information disclosure on IBM training service endpoint |
| [1592587](https://hackerone.com/reports/1592587) | LinkedIn | medium | - | 48 | 2022-10-05 | Insecure Direct Object Reference (IDOR) | IDOR - Delete technical skill assessment result & Gained Badges result of any user |
| [2618486](https://hackerone.com/reports/2618486) | Reddit | low | - | 47 | 2024-08-09 | Insecure Direct Object Reference (IDOR) | IDOR lets a malicious user reveal the unpinned achievement badges of any Reddit user |
| [2212555](https://hackerone.com/reports/2212555) | Glassdoor |  | - | 46 |  | Insecure Direct Object Reference (IDOR) | Unauthorized Access to Deleted Interviews on Glassdoor Platform |
| [3527788](https://hackerone.com/reports/3527788) | GitHub | medium | - | 46 | 2026-08-25 | Insecure Direct Object Reference (IDOR) | Add labels to arbitrary issues/prs via Memex Bulk Update to compromise github actions label gating |
| [715054](https://hackerone.com/reports/715054) | Starbucks | medium | - | 45 | 2020-09-22 | Insecure Direct Object Reference (IDOR) | China - IDOR on Reservation Staging/Non Production Site - https://reservation.stg.starbucks.com.cn |
| [1592596](https://hackerone.com/reports/1592596) | Automattic | low | - | 45 | 2022-08-04 | Insecure Direct Object Reference (IDOR) | Sensei LMS IDOR to send message |
| [2073950](https://hackerone.com/reports/2073950) | Mars | medium | - | 45 | 2024-02-14 | Insecure Direct Object Reference (IDOR) | IDOR in one subdomain of █████████ -> change information of pets without athorization! |
| [2132183](https://hackerone.com/reports/2132183) | Mars | critical | - | 45 | 2024-01-30 | Insecure Direct Object Reference (IDOR) | IDOR to account takeover on POST to █████████ by changing member_id parameter |
| [1813450](https://hackerone.com/reports/1813450) | LinkedIn | medium | - | 44 | 2023-05-12 | Insecure Direct Object Reference (IDOR) | Attackers do not need to Pay for a Subscription to get the `Discussion Group URL` in `Paid Learning` |
| [300179](https://hackerone.com/reports/300179) | Mavenlink | low | - | 43 | 2019-02-27 | Insecure Direct Object Reference (IDOR) | User uploaded portfolio files can be accessed by any user even after deleted |
| [1586950](https://hackerone.com/reports/1586950) | TikTok | low | - | 43 | 2023-06-02 | Insecure Direct Object Reference (IDOR) | IDOR in family pairing API |
| [1837309](https://hackerone.com/reports/1837309) | LinkedIn | medium | - | 43 | 2023-05-17 | Insecure Direct Object Reference (IDOR) | Anyone can view the results of linkedin skill test -if failed to earn a badge or if the badge earned is kept private: both cases results can be viewed |
| [3713682](https://hackerone.com/reports/3713682) | Rocket.Chat | medium | - | 43 | 2026-05-18 | Insecure Direct Object Reference (IDOR) | IDOR: autotranslate.translateMessage Full Message Content Leak |
| [2586641](https://hackerone.com/reports/2586641) | U.S. Dept Of Defense | medium | - | 42 | 2024-07-19 | Insecure Direct Object Reference (IDOR) | IDOR  leads to view other user Biographical details (Possible PII LEAK) |
| [316789](https://hackerone.com/reports/316789) | Starbucks | high | - | 41 | 2018-07-20 | Insecure Direct Object Reference (IDOR) | Able to purchase a gift card with any amount |
| [681001](https://hackerone.com/reports/681001) | New Relic |  | - | 40 |  | Insecure Direct Object Reference (IDOR) | User can run monitors at private locations, which he has no access to |
| [946323](https://hackerone.com/reports/946323) | Lark Technologies | medium | - | 40 | 2022-01-13 | Insecure Direct Object Reference (IDOR) | [IDOR] Modify other team's reminders via reminderId parameter |
| [1848176](https://hackerone.com/reports/1848176) | U.S. Department of State | high | - | 40 | 2023-04-11 | Insecure Direct Object Reference (IDOR) | IDOR in TalentMAP API can be abused to enumerate personal information of all the users |
| [2586662](https://hackerone.com/reports/2586662) | U.S. Dept Of Defense | medium | - | 40 | 2024-07-19 | Insecure Direct Object Reference (IDOR) | IDOR : Modify other users demographic details |
| [3382343](https://hackerone.com/reports/3382343) | Nextcloud | medium | - | 40 | 2026-04-14 | Insecure Direct Object Reference (IDOR) | BOLA/IDOR in Out-of-Office API allows any authenticated user to read other users' absence data |
| [1387320](https://hackerone.com/reports/1387320) | Lark Technologies | high | - | 39 | 2022-01-25 | Insecure Direct Object Reference (IDOR) | Able to steal private files by manipulating response using Auto Reply function of Lark |
| [3353057](https://hackerone.com/reports/3353057) | SingleStore | low | - | 39 | 2026-07-01 | Insecure Direct Object Reference (IDOR) | Insecure Direct Object Reference (IDOR) allows creating folders. |
| [322661](https://hackerone.com/reports/322661) | Shopify | medium | - | 38 | 2018-05-01 | Insecure Direct Object Reference (IDOR) | Replace other user files in Inbox messages |
| [909863](https://hackerone.com/reports/909863) | Shopify | medium | - | 38 | 2021-02-07 | Insecure Direct Object Reference (IDOR) | Low privileged user can create high privileged user's KITCRM authorization token and can read and write message to KIT |
| [861849](https://hackerone.com/reports/861849) | RGhost | medium | - | 37 | 2020-05-13 | Insecure Direct Object Reference (IDOR) | Idor on the DELETE /comments/ |
| [3518758](https://hackerone.com/reports/3518758) | Nextcloud |  | - | 37 | 2026-04-07 | Insecure Direct Object Reference (IDOR) | IDOR on ██████ via direct photo URL leads to unauthorized access to deleted and other users' photos |
| [547663](https://hackerone.com/reports/547663) | Trint Ltd | medium | - | 36 | 2019-06-22 | Insecure Direct Object Reference (IDOR) | IDOR in changing shared file name |
| [739752](https://hackerone.com/reports/739752) | Mail.ru |  | - | 36 |  | Insecure Direct Object Reference (IDOR) | IDOR в списке пользователей по домену в relap.io |
| [766437](https://hackerone.com/reports/766437) | Starbucks | high | - | 36 | 2020-02-11 | Insecure Direct Object Reference (IDOR) | Thailand - Insecure Direct Object Reference permits an unauthorized user to transfer funds from a victim using only the victims Starbucks card |
| [1372216](https://hackerone.com/reports/1372216) | GitLab | medium | - | 35 | 2022-02-22 | Insecure Direct Object Reference (IDOR) | IDOR in "external status check" API leaks data about any status check on the instance |
| [3353035](https://hackerone.com/reports/3353035) | SingleStore | low | - | 35 | 2026-07-01 | Insecure Direct Object Reference (IDOR) | Delete any folder for any user within the organization |
| [287789](https://hackerone.com/reports/287789) | BOHEMIA INTERACTIVE a.s. | high | - | 34 | 2018-09-17 | Insecure Direct Object Reference (IDOR) | IDOR to view User Order Information |
| [868590](https://hackerone.com/reports/868590) | Lab45 | medium | - | 34 | 2020-05-12 | Insecure Direct Object Reference (IDOR) | IDOR on deleting drafts on https://apps.topcoder.com/wiki/users/viewmydrafts.action via discardDraftId parameter |
| [977597](https://hackerone.com/reports/977597) | Mail.ru |  | - | 34 |  | Insecure Direct Object Reference (IDOR) | [api-site.city-mobil.ru] Improper access control leads to information disclosure |
| [1272478](https://hackerone.com/reports/1272478) | MTN Group | critical | - | 34 | 2022-09-04 | Insecure Direct Object Reference (IDOR) | IDOR Leads To Account Takeover Without User Interaction |
| [1654657](https://hackerone.com/reports/1654657) | TikTok | medium | - | 34 | 2022-09-21 | Insecure Direct Object Reference (IDOR) | Add products to any livestream. |
| [1784681](https://hackerone.com/reports/1784681) | Nextcloud | medium | - | 34 | 2023-04-12 | Insecure Direct Object Reference (IDOR) | Ability to read any emails through IDOR on Nextcloud Mail |
| [227522](https://hackerone.com/reports/227522) | Radancy |  | - | 33 |  | Insecure Direct Object Reference (IDOR) | IDOR in editing courses |
| [269937](https://hackerone.com/reports/269937) | Eternal | high | - | 33 | 2017-10-27 | Insecure Direct Object Reference (IDOR) | [www.zomato.com] IDOR - Leaking all Personal Details of all Zomato Users through an endpoint |
| [291721](https://hackerone.com/reports/291721) | HackerOne | medium | - | 33 | 2017-11-23 | Insecure Direct Object Reference (IDOR) | IDOR on Program Visibilty (Revealed / Concealed) against other team members |
| [663431](https://hackerone.com/reports/663431) | HackerOne | low | - | 33 | 2019-12-13 | Insecure Direct Object Reference (IDOR) | IDOR in Bugs overview enables attacker to determine the date range a hackathon was active |
| [971422](https://hackerone.com/reports/971422) | Mail.ru |  | - | 33 |  | Insecure Direct Object Reference (IDOR) | IDOR смена email пользователя через Ситимобил Бизнес |
| [361984](https://hackerone.com/reports/361984) | Yelp | medium | - | 32 | 2020-08-19 | Insecure Direct Object Reference (IDOR) | I.D.O.R TO EDIT ALL USER'S CREDIT CARD INFORMATION+(Partial credit card info disclosure) |
| [1952771](https://hackerone.com/reports/1952771) | Mars | high | - | 32 | 2023-06-23 | Insecure Direct Object Reference (IDOR) | ████ ' can change any account email and cannot retrieve his account and access it ' at ███ |
| [1509057](https://hackerone.com/reports/1509057) | TikTok | low | - | 31 | 2022-08-16 | Insecure Direct Object Reference (IDOR) | IDOR on TikTok Seller |
| [2705507](https://hackerone.com/reports/2705507) | Nextcloud | low | - | 31 | 2024-11-18 | Insecure Direct Object Reference (IDOR) | Share information of Tables app is not limited to affected users |
| [3689633](https://hackerone.com/reports/3689633) | Discourse | medium | - | 31 | 2026-08-26 | Insecure Direct Object Reference (IDOR) | Hidden/restricted tags can be mutated through synonym ID paths without per-tag authorization |
| [156537](https://hackerone.com/reports/156537) | Ubiquiti Inc. |  | - | 30 | 2016-11-29 | Insecure Direct Object Reference (IDOR) | IDOR Causing Deletion of any account |
| [1085782](https://hackerone.com/reports/1085782) | U.S. Dept Of Defense | critical | - | 30 | 2021-02-18 | Insecure Direct Object Reference (IDOR) | █████████ IDOR leads to disclosure of PHI/PII |
| [3137895](https://hackerone.com/reports/3137895) | Nextcloud | medium | - | 30 | 2025-12-05 | Insecure Direct Object Reference (IDOR) | Missing ownership check in Tables app allows moving columns into tables of other users |
| [3138721](https://hackerone.com/reports/3138721) | Nextcloud | medium | - | 30 | 2025-12-05 | Insecure Direct Object Reference (IDOR) | Tables app allowed users to view columns metadata information of any table |
| [230328](https://hackerone.com/reports/230328) | Nextcloud | medium | - | 29 | 2017-09-16 | Insecure Direct Object Reference (IDOR) | IDOR unsubscribe Anyone from NextClouds Newsletters by knowing their Email |
| [964010](https://hackerone.com/reports/964010) | Azbuka Vkusa | high | - | 29 | 2021-11-15 | Insecure Direct Object Reference (IDOR) | IDOR - Other user's delivery address disclosed |
| [969223](https://hackerone.com/reports/969223) | U.S. Dept Of Defense | critical | - | 29 | 2020-09-29 | Insecure Direct Object Reference (IDOR) | IDOR to Account Takeover on https://████/index.html |
| [2112973](https://hackerone.com/reports/2112973) | Nextcloud | medium | - | 29 | 2023-11-21 | Insecure Direct Object Reference (IDOR) | Enabling Birthday Contact to any user |
| [254151](https://hackerone.com/reports/254151) | Uber | low | - | 28 | 2019-01-25 | Insecure Direct Object Reference (IDOR) | IDOR in activateFuelCard id allows bulk lookup of driver uuids |
| [261221](https://hackerone.com/reports/261221) | Mavenlink | low | - | 28 | 2018-09-09 | Insecure Direct Object Reference (IDOR) | Participation of expired account holders in Projects can occure financial loss to Mavenlink |
| [858662](https://hackerone.com/reports/858662) | Starbucks | low | - | 28 | 2020-05-19 | Insecure Direct Object Reference (IDOR) | Thailand - IDOR on www.starbuckscardth.in.th: A logged in user could view any Thailand Starbucks card balance if they knew that Starbucks card number |
| [1448550](https://hackerone.com/reports/1448550) | MTN Group | critical | - | 28 | 2022-12-01 | Insecure Direct Object Reference (IDOR) | Remove Every User, Admin, And Owner Out Of Their Teams on developers.mtn.com via IDOR + Information Disclosure |
| [1698006](https://hackerone.com/reports/1698006) | MTN Group | critical | - | 28 | 2022-10-13 | Insecure Direct Object Reference (IDOR) | IDOR  [mtnmobad.mtnbusiness.com.ng] |
| [3259610](https://hackerone.com/reports/3259610) | U.S. Dept Of Defense | high | - | 28 | 2026-01-12 | Insecure Direct Object Reference (IDOR) | Unauthenticated Users Can Access Other Users’ Bug Report Attachments via Broken Access Control |
| [439729](https://hackerone.com/reports/439729) | GitLab | low | - | 27 | 2019-09-19 | Insecure Direct Object Reference (IDOR) | Add and Access to Labels of any Private Projects/Groups of Gitlab(IDOR) |
| [747612](https://hackerone.com/reports/747612) | Mail.ru |  | - | 27 |  | Insecure Direct Object Reference (IDOR) | [city-mobil.ru/taxiserv/] Disclosure  information about drivers |
| [1196976](https://hackerone.com/reports/1196976) | U.S. Dept Of Defense | high | - | 27 | 2021-06-30 | Insecure Direct Object Reference (IDOR) | IDOR while uploading ████ attachments at [█████████] |
| [1965640](https://hackerone.com/reports/1965640) | Mars | medium | - | 27 | 2023-06-22 | Insecure Direct Object Reference (IDOR) | ████ ' can add animal to other account ' at ██████ |
| [3247386](https://hackerone.com/reports/3247386) | Nextcloud | medium | - | 27 | 2025-12-05 | Insecure Direct Object Reference (IDOR) | Participants were able to blindly delete poll drafts of other users by ID |
| [283419](https://hackerone.com/reports/283419) | Mavenlink | medium | - | 26 | 2018-02-09 | Insecure Direct Object Reference (IDOR) | [app.mavenlink.com] IDOR to view sensitive information |
| [587687](https://hackerone.com/reports/587687) | Trint Ltd | low | - | 26 | 2019-07-03 | Insecure Direct Object Reference (IDOR) | IDOR to update folder name of other user |
| [884159](https://hackerone.com/reports/884159) | Shopify |  | - | 26 | 2020-08-19 | Insecure Direct Object Reference (IDOR) | Ability to generate shipping labels in another store orders |
| [2587953](https://hackerone.com/reports/2587953) | U.S. Dept Of Defense | high | - | 26 | 2024-07-19 | Insecure Direct Object Reference (IDOR) | Email Takeover leads to permanent account deletion |
| [429000](https://hackerone.com/reports/429000) | U.S. Dept Of Defense | critical | - | 25 | 2019-04-08 | Insecure Direct Object Reference (IDOR) | Access to all █████████ files, including CAC authentication bypass |
| [674195](https://hackerone.com/reports/674195) | GitLab | high | - | 25 | 2020-08-26 | Insecure Direct Object Reference (IDOR) | Stealing data from customers.gitlab.com without user interaction |
| [1066203](https://hackerone.com/reports/1066203) | Stripe | high | - | 25 | 2022-03-08 | Insecure Direct Object Reference (IDOR) | GRAPHQL cross-tenant IDOR giving write access thought the operation UpdateAtlasApplicationPerson |
| [1159367](https://hackerone.com/reports/1159367) | EXNESS | medium | - | 25 | 2022-04-13 | Insecure Direct Object Reference (IDOR) | Access control vulnerability (read-only) |
| [1005020](https://hackerone.com/reports/1005020) | Bumble | medium | - | 24 | 2020-12-25 | Insecure Direct Object Reference (IDOR) | Identify unique user ID of all the profiles |
| [194594](https://hackerone.com/reports/194594) | Uber | medium | - | 23 | 2018-12-19 | Insecure Direct Object Reference (IDOR) | IDOR on partners.uber.com allows for a driver to override administrator documents |
| [245872](https://hackerone.com/reports/245872) | GSA Bounty | medium | - | 23 | 2017-09-05 | Insecure Direct Object Reference (IDOR) | [IDOR] The authenticated user can restart website build or view build logs on any another Federalist account |
| [827158](https://hackerone.com/reports/827158) | Glassdoor |  | - | 23 |  | Insecure Direct Object Reference (IDOR) | IDOR Vulnerability in Job Preferences |
| [1690044](https://hackerone.com/reports/1690044) | U.S. Dept Of Defense | medium | - | 23 | 2022-10-14 | Insecure Direct Object Reference (IDOR) | IDOR leaking PII data via VendorId parameter |
| [1818969](https://hackerone.com/reports/1818969) | LinkedIn | medium | - | 23 | 2023-05-15 | Insecure Direct Object Reference (IDOR) | [ Continuation Report from #1814842 ] Can create articles using other users' NewsLetters |
| [2967032](https://hackerone.com/reports/2967032) | U.S. Dept Of Defense | high | - | 23 | 2026-01-12 | Insecure Direct Object Reference (IDOR) | IDOR Exposes PII of Tens of Thousands of Users and Supervisors |
| [265284](https://hackerone.com/reports/265284) | Concrete CMS | critical | - | 22 | 2018-04-15 | Insecure Direct Object Reference (IDOR) | 'cnvID' parameter vulnerable to Insecure Direct Object References |
| [328337](https://hackerone.com/reports/328337) | Mail.ru |  | - | 22 |  | Insecure Direct Object Reference (IDOR) | IDOR widget.support.my.com |
| [365504](https://hackerone.com/reports/365504) | Valve | low | - | 22 | 2019-01-07 | Insecure Direct Object Reference (IDOR) | Comment restriction in subsection "Workshop" of domain "steamcommunity.com" can be bypassed using IDOR |
| [685338](https://hackerone.com/reports/685338) | U.S. Dept Of Defense | high | - | 22 | 2024-07-19 | Insecure Direct Object Reference (IDOR) | Unauth IDOR to mass account takeover without user interaction on the ███████ (https://███████.edu/) |
| [726163](https://hackerone.com/reports/726163) | Moneybird | low | - | 22 | 2021-09-21 | Insecure Direct Object Reference (IDOR) | IDOR in https://moneybird.com/user/accountant_company/edit(change company name) |
| [883731](https://hackerone.com/reports/883731) | Rockstar Games | low | - | 22 | 2021-03-02 | Insecure Direct Object Reference (IDOR) | Minor Account Privacy can Set to Everyone. |
| [914331](https://hackerone.com/reports/914331) | Palo Alto Software | medium | - | 22 | 2020-11-26 | Insecure Direct Object Reference (IDOR) | IDOR on notes to HTML injection |
| [915133](https://hackerone.com/reports/915133) | Automattic | medium | - | 22 | 2020-11-18 | Insecure Direct Object Reference (IDOR) | IDOR at 'media_code' when addings media to questions |
| [1174734](https://hackerone.com/reports/1174734) | EXNESS | medium | - | 22 | 2022-04-13 | Insecure Direct Object Reference (IDOR) | Access control vulnerability (read/write) |
| [3780709](https://hackerone.com/reports/3780709) | Revive Adserver | medium | - | 22 | 2026-06-25 | Insecure Direct Object Reference (IDOR) | Missing ownership validation allows cross‑manager tracker–campaign linking |
| [264919](https://hackerone.com/reports/264919) | Eternal |  | - | 21 | 2017-11-28 | Insecure Direct Object Reference (IDOR) | [www.zomato.com] IDOR - Delete/Deactivate any special menu of any Restaurants from Zomato |
| [395246](https://hackerone.com/reports/395246) | U.S. Dept Of Defense | critical | - | 21 | 2019-04-05 | Insecure Direct Object Reference (IDOR) | ███████ Site Exposes █████████ forms |
| [854290](https://hackerone.com/reports/854290) | Palo Alto Software | critical | - | 21 | 2020-05-13 | Insecure Direct Object Reference (IDOR) | IDOR on update user preferences |
| [1571578](https://hackerone.com/reports/1571578) | TikTok | medium | - | 21 | 2022-09-21 | Insecure Direct Object Reference (IDOR) | Create product discounts of any shop |
| [1587374](https://hackerone.com/reports/1587374) | LinkedIn | medium | - | 21 | 2022-11-30 | Insecure Direct Object Reference (IDOR) | Campaign Account Balance and History Disclosed in API Response |
| [1755555](https://hackerone.com/reports/1755555) | Nextcloud | low | - | 21 | 2023-01-09 | Insecure Direct Object Reference (IDOR) | Possibility to delete files attached to deck cards of other users |
| [1947376](https://hackerone.com/reports/1947376) | Mars | medium | - | 21 | 2023-06-23 | Insecure Direct Object Reference (IDOR) | ███████  ' can delete any animal from other account  '  at ██████████ |
| [228383](https://hackerone.com/reports/228383) | U.S. Dept Of Defense | high | - | 20 | 2019-10-04 | Insecure Direct Object Reference (IDOR) | IDOR on DoD Website exposes FTP users and passes linked to all accounts! |
| [268167](https://hackerone.com/reports/268167) | Cuvva |  | - | 20 |  | Insecure Direct Object Reference (IDOR) | Insecure Direct Object Reference (IDOR) Allowing me to claim other user's photos (driving license and selfies) as mine |
| [318751](https://hackerone.com/reports/318751) | Shopify | medium | - | 20 | 2018-03-05 | Insecure Direct Object Reference (IDOR) | Access to Private Photos of Apps in App section(IDOR) |
| [783332](https://hackerone.com/reports/783332) | Starbucks | medium | - | 20 | 2020-03-17 | Insecure Direct Object Reference (IDOR) | Singapore - IDOR in campaign.starbucks.com.sg |
| [317332](https://hackerone.com/reports/317332) | Vend VDP | medium | - | 19 | 2018-05-02 | Insecure Direct Object Reference (IDOR) | Improper access control on adding a Register to an Outlet |
| [344284](https://hackerone.com/reports/344284) | Instacart | high | - | 19 | 2018-05-25 | Insecure Direct Object Reference (IDOR) | View & add to cart unlisted items via IDOR |
| [389250](https://hackerone.com/reports/389250) | U.S. Dept Of Defense | medium | - | 19 | 2022-02-14 | Insecure Direct Object Reference (IDOR) | IDOR |
| [736065](https://hackerone.com/reports/736065) | QIWI |  | - | 19 |  | Insecure Direct Object Reference (IDOR) | IDOR редактирование любого вишлиста |
| [762707](https://hackerone.com/reports/762707) | Polymail, Inc. |  | - | 19 |  | Insecure Direct Object Reference (IDOR) | Metadata leakage via IDOR |
| [888729](https://hackerone.com/reports/888729) | Helium | high | - | 19 | 2020-07-10 | Insecure Direct Object Reference (IDOR) | Read-Only user can delete users |
| [1505609](https://hackerone.com/reports/1505609) | U.S. General Services Administration | medium | - | 19 | 2022-05-26 | Insecure Direct Object Reference (IDOR) | Read Other Users Reports Through Cloning |
| [1687415](https://hackerone.com/reports/1687415) | U.S. Dept Of Defense |  | - | 19 | 2023-01-06 | Insecure Direct Object Reference (IDOR) | IDOR when editing email leads to Mass Full ATOs (Account Takeovers) without user interaction on https://██████/ |
| [1118638](https://hackerone.com/reports/1118638) | U.S. General Services Administration | medium | - | 18 | 2021-04-24 | Insecure Direct Object Reference (IDOR) | IDOR at training.smartpay.gsa.gov/reports/quizzes-taken-by-user |
| [264754](https://hackerone.com/reports/264754) | Eternal |  | - | 17 | 2017-12-28 | Insecure Direct Object Reference (IDOR) | [www.zomato.com] IDOR - Delete/Deactivate ANY/ALL Promos through a Post Request at **clients/promoDataHandler.php** |
| [1004750](https://hackerone.com/reports/1004750) | U.S. Dept Of Defense | critical | - | 17 | 2020-11-09 | Insecure Direct Object Reference (IDOR) | IDOR + Account Takeover  [UNAUTHENTICATED] |
| [217558](https://hackerone.com/reports/217558) | Radancy |  | - | 16 |  | Insecure Direct Object Reference (IDOR) | Possible to view and takeover other user's education and courses @ mijn.werkenbijdefensie.nl |
| [749887](https://hackerone.com/reports/749887) | Mail.ru |  | - | 16 |  | Insecure Direct Object Reference (IDOR) | relap.io IDOR |
| [952095](https://hackerone.com/reports/952095) | LY Corporation | medium | - | 16 | 2022-04-18 | Insecure Direct Object Reference (IDOR) | Deleting someone else's profile image with a GraphQL query in programming education service (https://entry.line.me) |
| [1825227](https://hackerone.com/reports/1825227) | Cloudflare Public Bug Bounty | medium | - | 16 | 2023-04-10 | Insecure Direct Object Reference (IDOR) | Session mismatch leading to potential account takeover (local access required) |
| [244636](https://hackerone.com/reports/244636) | WakaTime | low | - | 15 | 2017-07-03 | Insecure Direct Object Reference (IDOR) | IDOR create accounts and verify them with original account email |
| [281296](https://hackerone.com/reports/281296) | RBKmoney | high | - | 15 | 2018-01-29 | Insecure Direct Object Reference (IDOR) | IDOR in merchant.rbmonkey.com allows deleting eShops of another user |
| [511779](https://hackerone.com/reports/511779) | HackerOne | low | - | 15 | 2019-04-25 | Insecure Direct Object Reference (IDOR) | Moving a report to a different program doesn't reassign the Custom Field Values |
| [791289](https://hackerone.com/reports/791289) | Mail.ru |  | - | 15 |  | Insecure Direct Object Reference (IDOR) | idor leads to leak order information |
| [912161](https://hackerone.com/reports/912161) | Lark Technologies | medium | - | 15 | 2021-03-17 | Insecure Direct Object Reference (IDOR) | Messages disclosure via search feature of other users group(Cross-Tenant). |
| [1048540](https://hackerone.com/reports/1048540) | U.S. Dept Of Defense | medium | - | 15 | 2021-04-08 | Insecure Direct Object Reference (IDOR) | IDOR on https://██████ via POST UID enables database scraping |
| [230870](https://hackerone.com/reports/230870) | U.S. Dept Of Defense | medium | - | 14 | 2017-07-05 | Insecure Direct Object Reference (IDOR) | Arbitary file download vulnerability on a DoD website |
| [253929](https://hackerone.com/reports/253929) | OLX |  | - | 14 |  | Insecure Direct Object Reference (IDOR) | I found a way to instantly take over ads by other users and change them (IDOR) |
| [260604](https://hackerone.com/reports/260604) | Legal Robot | none | - | 14 | 2017-08-16 | Insecure Direct Object Reference (IDOR) | Update any profile |
| [701160](https://hackerone.com/reports/701160) | Starbucks | medium | - | 14 | 2019-12-12 | Insecure Direct Object Reference (IDOR) | India - An Insecure Direct Object Reference (IDOR) allowed unauthorized access to view card index number and monetary balance |
| [1744264](https://hackerone.com/reports/1744264) | Reddit | critical | - | 14 | 2023-05-18 | Insecure Direct Object Reference (IDOR) | read and message other user's messages |
| [1107130](https://hackerone.com/reports/1107130) | Mail.ru |  | - | 13 |  | Insecure Direct Object Reference (IDOR) | IDOR to edit test/poll/quiz on relap.io |
| [1450117](https://hackerone.com/reports/1450117) | Nextcloud | medium | - | 13 | 2022-05-20 | Insecure Direct Object Reference (IDOR) | Nextcloud Deck : Possibility for anyone to add a stack with existing tasks on anyone's board |
| [1489470](https://hackerone.com/reports/1489470) | U.S. Dept Of Defense | high | - | 13 | 2022-04-07 | Insecure Direct Object Reference (IDOR) | Authorization bypass -> IDOR -> PII Leakage |
| [1536936](https://hackerone.com/reports/1536936) | MTN Group | critical | - | 13 | 2022-12-01 | Insecure Direct Object Reference (IDOR) | Unprotected Direct Object Reference |
| [283407](https://hackerone.com/reports/283407) | RecargaPay |  | - | 12 |  | Insecure Direct Object Reference (IDOR) | IDOR exposes receipts of all users. |
| [1004745](https://hackerone.com/reports/1004745) | U.S. Dept Of Defense | high | - | 12 | 2020-11-23 | Insecure Direct Object Reference (IDOR) | View another user information with IDOR vulnerability |
| [1174387](https://hackerone.com/reports/1174387) | EXNESS | medium | - | 12 | 2022-04-13 | Insecure Direct Object Reference (IDOR) | Acess control vulnerability (read/write) |
| [1679276](https://hackerone.com/reports/1679276) | Automattic | medium | - | 12 | 2022-10-19 | Insecure Direct Object Reference (IDOR) | IDOR able to buy a plan with lesser fee |
| [215384](https://hackerone.com/reports/215384) | GitLab | medium | - | 11 | 2017-03-30 | Insecure Direct Object Reference (IDOR) | [Subgroups] Unprivileged User Can Disclose Private Group Names |
| [230714](https://hackerone.com/reports/230714) | U.S. Dept Of Defense | medium | - | 11 | 2017-07-05 | Insecure Direct Object Reference (IDOR) | Arbitary file download vulnerability on a DoD website |
| [313050](https://hackerone.com/reports/313050) | Eternal | medium | - | 11 | 2018-04-25 | Insecure Direct Object Reference (IDOR) | IDOR in treat subscriptions |
| [338477](https://hackerone.com/reports/338477) | ExpressionEngine | low | - | 11 | 2018-04-20 | Insecure Direct Object Reference (IDOR) | [EE] change the author of post using the author_id |
| [847452](https://hackerone.com/reports/847452) | U.S. Dept Of Defense | high | - | 11 | 2020-05-14 | Insecure Direct Object Reference (IDOR) | Full Account Take-Over of ████████ Members via IDOR |
| [226640](https://hackerone.com/reports/226640) | Mail.ru |  | - | 10 |  | Insecure Direct Object Reference (IDOR) | IDOR in tender.mail.ru leading to Information Disclosure |
| [498351](https://hackerone.com/reports/498351) | U.S. Dept Of Defense | medium | - | 10 | 2019-12-02 | Insecure Direct Object Reference (IDOR) | [█████] Get all tickets (IDOR) |
| [741683](https://hackerone.com/reports/741683) | U.S. Dept Of Defense | high | - | 10 | 2020-05-14 | Insecure Direct Object Reference (IDOR) | idor on upload profile functionality |
| [956799](https://hackerone.com/reports/956799) | Mail.ru |  | - | 9 |  | Insecure Direct Object Reference (IDOR) | IDOR zakazaka (состояние заказа и перезаказ) |
| [1107126](https://hackerone.com/reports/1107126) | Mail.ru |  | - | 9 |  | Insecure Direct Object Reference (IDOR) | IDOR to delete test/poll/quiz on relap.io |
| [1627974](https://hackerone.com/reports/1627974) | U.S. Dept Of Defense | medium | - | 9 | 2022-11-18 | Insecure Direct Object Reference (IDOR) | IDOR on ███████ [HtUS] |
| [1680818](https://hackerone.com/reports/1680818) | Rockstar Games | low | - | 9 | 2022-09-06 | Insecure Direct Object Reference (IDOR) | Modifying Sprunk vs eCola crew data |
| [215326](https://hackerone.com/reports/215326) | VK.com | low | - | 8 | 2017-06-07 | Insecure Direct Object Reference (IDOR) | Подмена SSL-сертификата для любой группы в секции Управление группой->Работа с API неавторизированным пользователем. |
| [230026](https://hackerone.com/reports/230026) | U.S. Dept Of Defense | medium | - | 8 | 2019-12-02 | Insecure Direct Object Reference (IDOR) | Insecure Direct Object Reference on in-scope .mil website |
| [271861](https://hackerone.com/reports/271861) | New Relic |  | - | 8 |  | Insecure Direct Object Reference (IDOR) | Bypass of my two other reports #267636 + #255894 - (IDOR) Ability to see full name associated with other New Relic accounts |
| [277377](https://hackerone.com/reports/277377) | Inflection | none | - | 8 | 2017-11-01 | Insecure Direct Object Reference (IDOR) | Amount Manipulation Buy Unlimited Credits in just $1.00 |
| [307978](https://hackerone.com/reports/307978) | LocalTapiola |  | - | 8 |  | Insecure Direct Object Reference (IDOR) | Authorization issue on 'valtakirjat' (/e2/verkkopalvelu/) |
| [388554](https://hackerone.com/reports/388554) | U.S. Dept Of Defense | critical | - | 8 | 2020-05-11 | Insecure Direct Object Reference (IDOR) | ████ █████ exposes highly sensitive information to public |
| [959697](https://hackerone.com/reports/959697) | Dropcontact | high | - | 8 | 2020-08-18 | Insecure Direct Object Reference (IDOR) | Idor for firstpromoter service |
| [978768](https://hackerone.com/reports/978768) | GitLab | high | - | 8 | 2020-09-14 | Insecure Direct Object Reference (IDOR) | Adding everyone to the repo due to the lack of rate limit |
| [3883840](https://hackerone.com/reports/3883840) | Revive Adserver | medium | - | 8 | 2026-11-11 | Insecure Direct Object Reference (IDOR) | Cross-agency disclosure in website listing |
| [246819](https://hackerone.com/reports/246819) | Pornhub |  | - | 7 |  | Insecure Direct Object Reference (IDOR) | Private videos can be added to our playlists |
| [361133](https://hackerone.com/reports/361133) | Liberapay | none | - | 7 | 2018-06-02 | Insecure Direct Object Reference (IDOR) | Able to View other users income history |
| [879960](https://hackerone.com/reports/879960) | 8x8 | low | - | 7 | 2020-07-27 | Insecure Direct Object Reference (IDOR) | IDOR: Adding Contacts to Other User Groups |
| [1579820](https://hackerone.com/reports/1579820) | Nextcloud | medium | - | 7 | 2022-07-06 | Insecure Direct Object Reference (IDOR) | Ownership check missing when updating or deleting attachments |
| [1628012](https://hackerone.com/reports/1628012) | U.S. Dept Of Defense | medium | - | 7 | 2022-09-14 | Insecure Direct Object Reference (IDOR) | IDOR Lead  To VIEW & DELETE & Create api_key [HtUS] |
| [450882](https://hackerone.com/reports/450882) | Starbucks | medium | - | 6 | 2018-12-20 | Insecure Direct Object Reference (IDOR) | Able to bypass information requirements before launching a Chat. |
| [751281](https://hackerone.com/reports/751281) | Mail.ru |  | - | 6 |  | Insecure Direct Object Reference (IDOR) | [city-mobil.ru/taxiserv/] IDOR leads to driver account takeover |
| [787886](https://hackerone.com/reports/787886) | New Relic |  | - | 6 |  | Insecure Direct Object Reference (IDOR) | Ability to run monitors' jobs of other accounts and to read these jobs content (including the secure credentials values) |
| [3929216](https://hackerone.com/reports/3929216) | Revive Adserver | medium | - | 6 | 2026-11-11 | Insecure Direct Object Reference (IDOR) | Cross-agency delivery rule set creation |
| [3958112](https://hackerone.com/reports/3958112) | Revive Adserver | medium | - | 6 | 2026-11-11 | Insecure Direct Object Reference (IDOR) | Missing campaign ownership check in zone bulk linking |
| [651966](https://hackerone.com/reports/651966) | Mail.ru |  | - | 5 |  | Insecure Direct Object Reference (IDOR) | [auto.mail.ru] IDOR на редактирование поста любого юзера. |
| [800608](https://hackerone.com/reports/800608) | U.S. Dept Of Defense | medium | - | 5 | 2022-03-18 | Insecure Direct Object Reference (IDOR) | IDOR - Delete Users Saved Projects |
| [232562](https://hackerone.com/reports/232562) | Cuvva |  | - | 4 |  | Insecure Direct Object Reference (IDOR) | IDOR spam anyone's cellphone number through Cuvva app link |
| [284963](https://hackerone.com/reports/284963) | Semrush | high | - | 4 | 2018-03-13 | Insecure Direct Object Reference (IDOR) | Insecure Direct Object Reference on API without API key |
| [462173](https://hackerone.com/reports/462173) | Dropbox |  | - | 4 |  | Insecure Direct Object Reference (IDOR) | Disclose anonymous accessible link on embedded files in paper dropbox sessions |
| [763258](https://hackerone.com/reports/763258) | Mail.ru |  | - | 4 |  | Insecure Direct Object Reference (IDOR) | information disclosure via IDOR on "https://target.my.com/api/v2/coverage/segment.json?id={id}" endpoint |
| [859357](https://hackerone.com/reports/859357) | Mail.ru |  | - | 4 |  | Insecure Direct Object Reference (IDOR) | [capsula.mail.ru] overriding order info |
| [765565](https://hackerone.com/reports/765565) | New Relic |  | - | 3 |  | Insecure Direct Object Reference (IDOR) | Cross-account reading of Insights dashboards through GraphQL |
| [786109](https://hackerone.com/reports/786109) | New Relic |  | - | 3 |  | Insecure Direct Object Reference (IDOR) | Attacker can create new account inside any partnership with no approve from the Partnership owner |
| [882258](https://hackerone.com/reports/882258) | Nextcloud | low | - | 3 | 2021-02-14 | Insecure Direct Object Reference (IDOR) | New users can read all Nextcloud Deck data from previous user with same username |
| [975749](https://hackerone.com/reports/975749) | New Relic |  | - | 3 |  | Insecure Direct Object Reference (IDOR) | IDOR - User is able to download charts/dashboards from cross accounts |
| [708182](https://hackerone.com/reports/708182) | Mail.ru |  | - | 2 |  | Insecure Direct Object Reference (IDOR) | IDOR позволяет изменить информацию о пользователе. |
| [834065](https://hackerone.com/reports/834065) | Mail.ru |  | - | 2 |  | Insecure Direct Object Reference (IDOR) | Improper access control leading to deletion of Greeting videos on {https://smtp.8mar.mail.ru/} |
| [3831102](https://hackerone.com/reports/3831102) | Revive Adserver | high | - | 1 | 2026-11-11 | Insecure Direct Object Reference (IDOR) | Access control bypass due to request precedence issue in global input registration |
