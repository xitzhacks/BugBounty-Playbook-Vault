---
title: "Business-logic case register — 127-row ledger (118 bucket + 9 unclassified merges; h1-brain corpus)"
type: register
built: "2026-11-07"
roster: "h1-brain disclosed_reports.db (3,673 rows; sha256 8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4)"
case_id_scheme: "BL-<HackerOne report id>"
bounty_rule: "DB bounty_amount where present (labeled $) · None/- = no figure in DB (not evidence of non-payment)"
module_rule: "frozen in archive/classes.json (bodies-win classification)"
corpus: "classified.json bucket business-logic (118 rows, weakness Business Logic Errors) + module_map_all.json _adjacent_unclassified merges (9 rows, bodies from DB)"
---

# Case register — Business Logic

Corpus: 127 rows (118 bucket + 9 unclassified merges) · 55 with bounty figures · **$60,090** · max $7,500 (BL-1295844) · evidence: 127 full-body.

Class census: commerce_payments_rewards 28 · account_invite_access_workflows 32 · race_condition_replay 6 · rate_limit_state_abuse 21 · _adjacent 31 · _adjacent_unclassified 9.

| Case | Team | Bounty | Module | Evidence | Note |
|---|---|---|---|---|---|
| [BL-145467](https://hackerone.com/reports/145467) | vimeo | - | _adjacent_unclassified | full | Downloading password protected / restricted videos
| [BL-225831](https://hackerone.com/reports/225831) | dashlane | - | _adjacent | full | Extract Billing admin email address using random team id
| [BL-226199](https://hackerone.com/reports/226199) | security | $1,000 | account_invite_access_workflows | full | Changing Victim's JIRA Integration Settings Through Multiple Bugs
| [BL-259400](https://hackerone.com/reports/259400) | legalrobot | - | account_invite_access_workflows | full | Issues with Forgot password Error Handling 
| [BL-259415](https://hackerone.com/reports/259415) | legalrobot | - | account_invite_access_workflows | full | Lengthy manual entry of 2FA secret
| [BL-259416](https://hackerone.com/reports/259416) | legalrobot | - | account_invite_access_workflows | full | Incorrect email content when disabling 2FA
| [BL-263760](https://hackerone.com/reports/263760) | x | $1,120 | _adjacent | full | Opportunity to obtain private tweets through search widget preview caches
| [BL-297359](https://hackerone.com/reports/297359) | x | - | rate_limit_state_abuse | full | No Rate Limit in email leads to huge Mass mailings
| [BL-312118](https://hackerone.com/reports/312118) | gitlab | $750 | rate_limit_state_abuse | full | Using GitLab to monitor and hijack domains in mass quantity.
| [BL-320355](https://hackerone.com/reports/320355) | shopify | - | _adjacent | full | myshopify.com domain takeover
| [BL-321938](https://hackerone.com/reports/321938) | zomato | - | _adjacent_unclassified | full | [www.zomato.com] Getting a complimentary dessert [Zomato Treats] on ordering a Meal at ...
| [BL-331691](https://hackerone.com/reports/331691) | security | $500 | account_invite_access_workflows | full | Email Forwarding invitations for Drafts are not marked as accepted, allowing multiple u...
| [BL-334205](https://hackerone.com/reports/334205) | security | $2,500 | account_invite_access_workflows | full | Harvesting all private invites using leave program fast-tracked invitation and security...
| [BL-336131](https://hackerone.com/reports/336131) | shopify | - | commerce_payments_rewards | full | Potential to abuse pricing errors in saved carts
| [BL-357929](https://hackerone.com/reports/357929) | reverb | - | commerce_payments_rewards | full | Items bought for free due to lacks of quantity controls
| [BL-361960](https://hackerone.com/reports/361960) | upserve | $500 | commerce_payments_rewards | full | Insufficient validation of sides/modifiers quantity
| [BL-364843](https://hackerone.com/reports/364843) | upserve | - | commerce_payments_rewards | full | OLO Total price manipulation using negative quantities
| [BL-381356](https://hackerone.com/reports/381356) | security | - | race_condition_replay | full | Client-Side Race Condition using Marketo, allows sending user to data-protocol in Safar...
| [BL-403602](https://hackerone.com/reports/403602) | basecamp | - | _adjacent | full | Attachments may be hijacked via AppCache+CookieBombing trick (bc3_production_blobs bucket)
| [BL-403783](https://hackerone.com/reports/403783) | zomato | - | commerce_payments_rewards | full | [www.zomato.com] Tampering with Order Quantity and paying less amount then actual amoun...
| [BL-413759](https://hackerone.com/reports/413759) | shopify | $500 | race_condition_replay | full | Race condition at create new Location
| [BL-415398](https://hackerone.com/reports/415398) | chaturbate | - | account_invite_access_workflows | full | Chaturbate "/chat_ignore_list/" endpoint does not check for Account status: Disabled  b...
| [BL-416906](https://hackerone.com/reports/416906) | chaturbate | - | rate_limit_state_abuse | full | Missing Rate Limitation at /apps/upload_app/ 
| [BL-422279](https://hackerone.com/reports/422279) | shopify | - | rate_limit_state_abuse | full | H1514 Simple phishing using auto-created modal with weak URL-pattern check in incontext...
| [BL-422331](https://hackerone.com/reports/422331) | aaf | - | commerce_payments_rewards | full | attacker can book unlimited tickets in free at https://aaf.com/checkout/order-received/...
| [BL-422698](https://hackerone.com/reports/422698) | chaturbate | - | account_invite_access_workflows | full | Update Chat Allowed By Option ( without age verification )
| [BL-423467](https://hackerone.com/reports/423467) | shopify | - | _adjacent | full | H1514 Ability to MiTM Shopify PoS Session to Takeover Communications
| [BL-426547](https://hackerone.com/reports/426547) | chaturbate | - | rate_limit_state_abuse | full | Missing Rate Limitation at /photo_videos/photoset/create
| [BL-428660](https://hackerone.com/reports/428660) | nextcloud | $50 | account_invite_access_workflows | full | Gallery: No feedback for invalid password
| [BL-434116](https://hackerone.com/reports/434116) | phabricator | $300 | _adjacent_unclassified | full | Exposing voting results on the Slowvote application without actually voting
| [BL-460920](https://hackerone.com/reports/460920) | security | $500 | rate_limit_state_abuse | full | Response program can create bounty table
| [BL-462503](https://hackerone.com/reports/462503) | gitlab | $1,000 | rate_limit_state_abuse | full | Claiming package names in GitLab's automatic package referencer.
| [BL-463828](https://hackerone.com/reports/463828) | security | $500 | account_invite_access_workflows | full | Submitting report through Embedded Submission form gives user indefinite access to a pr...
| [BL-475660](https://hackerone.com/reports/475660) | security | $500 | rate_limit_state_abuse | full | Response program can display "eligible for bounty" in scope area in program policy
| [BL-486629](https://hackerone.com/reports/486629) | zomato | - | commerce_payments_rewards | full | Improper validation allows user to unlock Zomato Gold multiple times at the same restau...
| [BL-488923](https://hackerone.com/reports/488923) | automattic | - | rate_limit_state_abuse | full | No Rate Limit on CrowdSignal Polls when Adding Comment
| [BL-511044](https://hackerone.com/reports/511044) | zomato | - | commerce_payments_rewards | full | [www.zomato.com] Availing Zomato Gold membership for free by tampering plan id(s) 
| [BL-549364](https://hackerone.com/reports/549364) | security | $500 | account_invite_access_workflows | full | Account recovery text message is sending a wrong domain to users.
| [BL-568832](https://hackerone.com/reports/568832) | automattic | - | rate_limit_state_abuse | full | No rate limit on app.crowdsignal.com (Finish quiz)
| [BL-592803](https://hackerone.com/reports/592803) | automattic | - | commerce_payments_rewards | full | Gaining unlimited bonus points on websites with WooCommerce Points and Rewards
| [BL-637267](https://hackerone.com/reports/637267) | upserve | - | _adjacent | full | Payment method token being sent to 3rd party analytics service
| [BL-665798](https://hackerone.com/reports/665798) | makerdao_bbp | - | commerce_payments_rewards | full | Earn free DAI interest (inflation) through instant CDP+DSR in one tx
| [BL-666632](https://hackerone.com/reports/666632) | x | $560 | account_invite_access_workflows | full | Delete direct message history without access the proper conversation_id
| [BL-672487](https://hackerone.com/reports/672487) | curve | - | commerce_payments_rewards | full | Business Logic Flaw - A non premium user can change/update retailers to get cashback on...
| [BL-672664](https://hackerone.com/reports/672664) | makerdao_bbp | - | commerce_payments_rewards | full | Steal collateral during `end` process, by earning DSR interest after `flow`.
| [BL-706934](https://hackerone.com/reports/706934) | ruby | $500 | _adjacent | full | Variant of CVE-2013-0269 (Denial of Service and Unsafe Object Creation Vulnerability in...
| [BL-712344](https://hackerone.com/reports/712344) | x | - | account_invite_access_workflows | full | [Bypass fixed #664038 and #519059] Application settings change settings that have been ...
| [BL-759247](https://hackerone.com/reports/759247) | reverb | - | race_condition_replay | full | Race Condition allows to redeem multiple times gift cards which leads to free "money"
| [BL-763177](https://hackerone.com/reports/763177) | phabricator | $500 | account_invite_access_workflows | full | User can link non-public file attachments, leading to file disclose on edit by higher-p...
| [BL-771694](https://hackerone.com/reports/771694) | semrush | - | commerce_payments_rewards | full | An attacker can buy marketplace articles for lower prices as it allows for negative qua...
| [BL-783258](https://hackerone.com/reports/783258) | localizejs | - | account_invite_access_workflows | full | 2-factor authentication can be disabled when logged in without confirming account password
| [BL-789260](https://hackerone.com/reports/789260) | nordsecurity | - | commerce_payments_rewards | full | Past payments using the Direct Debit method keep subscriptions active even if payments ...
| [BL-808287](https://hackerone.com/reports/808287) | nextcloud | $100 | account_invite_access_workflows | full | Unrestricted file upload on the image of contacts
| [BL-882848](https://hackerone.com/reports/882848) | gitlab | - | commerce_payments_rewards | full | Possibilty to purchase Ultimate - 1 Year (EDU or OSS)
| [BL-894569](https://hackerone.com/reports/894569) | gitlab | - | account_invite_access_workflows | full | An attacker can run pipeline jobs as arbitrary user
| [BL-905816](https://hackerone.com/reports/905816) | automattic | - | rate_limit_state_abuse | full | No Rate Limit when accessing "Password protection" enabled surveys leads to bypassing p...
| [BL-915140](https://hackerone.com/reports/915140) | automattic | - | _adjacent_unclassified | full | Users can bypass page restrictions via Export feature at "Share" feature in CrowdSignal
| [BL-963774](https://hackerone.com/reports/963774) | basecamp | - | commerce_payments_rewards | full | Premium Email Address Check Bypass - Hey
| [BL-965510](https://hackerone.com/reports/965510) | shopify | - | _adjacent_unclassified | full | Password protection can be removed for newly created development store 
| [BL-974892](https://hackerone.com/reports/974892) | helium | $250 | race_condition_replay | full | Race Condition of Transfer data Credits to Organization Leads to Add Extra free Data Cr...
| [BL-989415](https://hackerone.com/reports/989415) | cs_money | - | _adjacent_unclassified | full | Bypass restrict of member subscription to use custom background in https://3d.cs.money ...
| [BL-999789](https://hackerone.com/reports/999789) | security | - | account_invite_access_workflows | full | Getting New Invitations without Leaving Programs
| [BL-1029027](https://hackerone.com/reports/1029027) | imgur | - | commerce_payments_rewards | full | Bypass subscription
| [BL-1034023](https://hackerone.com/reports/1034023) | bumble | - | _adjacent | full | Possible (we need to wait for some time) takeover of subdomain badootech.badoo.com whic...
| [BL-1044285](https://hackerone.com/reports/1044285) | shopify | $2,900 | _adjacent_unclassified | full | Removing parts of URL from jQuery request exposes links for download of Paid Digital As...
| [BL-1051734](https://hackerone.com/reports/1051734) | automattic | - | rate_limit_state_abuse | full | [intensedebate.com] No Rate Limit On The report Functionality Lead To Delete Any Commen...
| [BL-1070510](https://hackerone.com/reports/1070510) | logitech | - | commerce_payments_rewards | full | Manipulating response leads to free access to Streamlabs Prime 
| [BL-1074047](https://hackerone.com/reports/1074047) | bumble | - | account_invite_access_workflows | full | Misconfigured oauth leads to Pre account takeover 
| [BL-1082847](https://hackerone.com/reports/1082847) | grammarly | - | _adjacent | full | Config override using non-validated query parameter allows at least reflected XSS by in...
| [BL-1088966](https://hackerone.com/reports/1088966) | security | - | account_invite_access_workflows | full | Ability to invite a new member on Sandbox Program
| [BL-1089978](https://hackerone.com/reports/1089978) | shopify | - | commerce_payments_rewards | full | [h1-2102] [Yaworski's Broskis] Suspected overcharge and chargebacks in PoS
| [BL-1112679](https://hackerone.com/reports/1112679) | security | $500 | _adjacent | full | Dangling cloud instance at vpn.inverselink.com
| [BL-1133118](https://hackerone.com/reports/1133118) | security | - | rate_limit_state_abuse | full | Hackerone is not properly deleting user id
| [BL-1172857](https://hackerone.com/reports/1172857) | curl | $800 | _adjacent | full | CVE-2021-22897: schannel cipher selection surprise
| [BL-1182864](https://hackerone.com/reports/1182864) | zomato | $350 | _adjacent | full | Subdomain takeover of fr1.vpn.zomans.com
| [BL-1213175](https://hackerone.com/reports/1213175) | curl | $700 | _adjacent | full | CVE-2021-22922: Wrong content via metalink not discarded
| [BL-1213765](https://hackerone.com/reports/1213765) | reddit | $500 | commerce_payments_rewards | full | IDOR to pay less for coin purchases on oauth.reddit.com via /api/v2/gold/paypal/create_...
| [BL-1234760](https://hackerone.com/reports/1234760) | curl | $1,000 | _adjacent | full | CVE-2021-22926: CURLOPT_SSLCERT mixup with Secure Transport
| [BL-1285538](https://hackerone.com/reports/1285538) | omise | - | race_condition_replay | full | Race condition on action: Invite members to a team
| [BL-1285598](https://hackerone.com/reports/1285598) | reddit | $5,000 | _adjacent | full | s3 bucket takeover presented in https://github.com/reddit/rpan-studio/blob/e1782332c75e...
| [BL-1295844](https://hackerone.com/reports/1295844) | valve | $7,500 | commerce_payments_rewards | full | Modify in-flight data to payment provider Smart2Pay
| [BL-1297689](https://hackerone.com/reports/1297689) | affirm | $500 | _adjacent | full | Subdomain takeover of www█████████.affirm.com
| [BL-1316650](https://hackerone.com/reports/1316650) | brave | $50 | _adjacent | full | unclaimed s3 bucket takeover in the 3 js file located on the github page of  brave soft...
| [BL-1322334](https://hackerone.com/reports/1322334) | automattic | - | commerce_payments_rewards | full | Ability to subscribe to inactive Post+ creators
| [BL-1337178](https://hackerone.com/reports/1337178) | nextcloud | - | rate_limit_state_abuse | full | objectId in share location can be set to open arbitrary URL or Deeplinks
| [BL-1364851](https://hackerone.com/reports/1364851) | trafficfactory | $200 | _adjacent | full | WordPress Plugin Update Confusion at trafficfactory.com
| [BL-1365738](https://hackerone.com/reports/1365738) | flickr | $500 | _adjacent | full | critical server misconfiguration lead to access to any user sensitive data which includ...
| [BL-1397826](https://hackerone.com/reports/1397826) | cosmos | $400 | _adjacent | full | Unclaimed official s3 bucket of tendermint(tendermint-packages) which is used by many o...
| [BL-1406926](https://hackerone.com/reports/1406926) | nextcloud | $100 | rate_limit_state_abuse | full | bypass forced password protection via circles app
| [BL-1443211](https://hackerone.com/reports/1443211) | mattermost | - | _adjacent_unclassified | full | Bypass Email Verification in Customer Portal
| [BL-1446107](https://hackerone.com/reports/1446107) | exness | - | rate_limit_state_abuse | full | Verification process done using different documents without corresponding to user infor...
| [BL-1486417](https://hackerone.com/reports/1486417) | security | - | account_invite_access_workflows | full | [Bypass] Ability to invite a new member in  sandbox Organization 
| [BL-1523584](https://hackerone.com/reports/1523584) | zomato | $300 | account_invite_access_workflows | full | Attacker shall recieve order updates on whatsapp for users who have activated whatsapp ...
| [BL-1538669](https://hackerone.com/reports/1538669) | omise | $100 | commerce_payments_rewards | full | IDOR Payments Status
| [BL-1543159](https://hackerone.com/reports/1543159) | reddit | $5,000 | commerce_payments_rewards | full | Able to approve admin approval and change effective status without adding payment detai...
| [BL-1565623](https://hackerone.com/reports/1565623) | ibb | $2,400 | _adjacent | full | CVE-2022-27778: curl removes wrong file on error
| [BL-1565624](https://hackerone.com/reports/1565624) | ibb | $2,400 | _adjacent | full | CVE-2022-27782: TLS and SSH connection too eager reuse
| [BL-1566325](https://hackerone.com/reports/1566325) | phabricator | $300 | _adjacent_unclassified | full | Conduit feed.publish API allows you to spoof other users or make it look like you have ...
| [BL-1614331](https://hackerone.com/reports/1614331) | ibb | $2,400 | _adjacent | full | CVE-2022-32207: Unpreserved file permissions
| [BL-1614332](https://hackerone.com/reports/1614332) | ibb | $480 | _adjacent | full | CVE-2022-32208: FTP-KRB bad message verification
| [BL-1664920](https://hackerone.com/reports/1664920) | security | - | account_invite_access_workflows | full | Program managers can see draft reports using Export Reports feature
| [BL-1675674](https://hackerone.com/reports/1675674) | linkedin | - | account_invite_access_workflows | full | An Attacker Can Flag Draft Job Posts And Can Disclose The Draft Job Posts Details [ Sim...
| [BL-1691603](https://hackerone.com/reports/1691603) | linkedin | - | account_invite_access_workflows | full | A Unverified User Can Post Newsletter (Which Is Not Allowed Through Application UI)
| [BL-1770797](https://hackerone.com/reports/1770797) | security | $500 | account_invite_access_workflows | full | adding h1_analyst_* to username for normal users 
| [BL-1849626](https://hackerone.com/reports/1849626) | stripe | $5,000 | commerce_payments_rewards | full | Fee discounts can be redeemed many times, resulting in unlimited fee-free transactions
| [BL-1874715](https://hackerone.com/reports/1874715) | ibb | $480 | _adjacent | full | CVE-2023-23914: HSTS ignored on multiple requests
| [BL-1874716](https://hackerone.com/reports/1874716) | ibb | $480 | _adjacent | full | CVE-2023-23915: HSTS amnesia with --parallel
| [BL-1912770](https://hackerone.com/reports/1912770) | ibb | $480 | _adjacent | full | CVE-2023-27533: TELNET option IAC injection
| [BL-1912777](https://hackerone.com/reports/1912777) | ibb | $480 | _adjacent | full | CVE-2023-27534: SFTP path ~ resolving discrepancy
| [BL-1912778](https://hackerone.com/reports/1912778) | ibb | $2,400 | _adjacent | full | CVE-2023-27535: FTP too eager connection reuse
| [BL-1912782](https://hackerone.com/reports/1912782) | ibb | $480 | _adjacent | full | CVE-2023-27536: GSS delegation too eager connection re-use
| [BL-1912783](https://hackerone.com/reports/1912783) | ibb | $480 | _adjacent | full | CVE-2023-27538: SSH connection too eager reuse still
| [BL-1991376](https://hackerone.com/reports/1991376) | indrive | - | rate_limit_state_abuse | full | the domain is truck-admin.eu-east-1.indriverapp.com and Enter the management system of ...
| [BL-2011431](https://hackerone.com/reports/2011431) | security | - | account_invite_access_workflows | full | Asset Inventory Internal Descriptions are leaked in CSV export
| [BL-2033005](https://hackerone.com/reports/2033005) | frontegg | - | rate_limit_state_abuse | full | Bypassing the block of Security Domain Restriction and normally invite blocked domains ...
| [BL-2125049](https://hackerone.com/reports/2125049) | indrive | - | commerce_payments_rewards | full | Unlimited fake rate to the passenger in city to city, Affected endpoint `/api/v1/review...
| [BL-2257374](https://hackerone.com/reports/2257374) | x | $250 | commerce_payments_rewards | full | Bypassing x profile verification to receive instant blue checkmark and unlimited profil...
| [BL-2263294](https://hackerone.com/reports/2263294) | security | - | account_invite_access_workflows | full | Cloud Computer Hackerone Triager can be Accessible for everyone [h1_analyst_lucas+view@...
| [BL-2430179](https://hackerone.com/reports/2430179) | security | - | account_invite_access_workflows | full | Minor security issue with Hackerone Invitations from sandbox program
| [BL-2450215](https://hackerone.com/reports/2450215) | security | - | account_invite_access_workflows | full | Any user could upload attachments to pentest scoping form they don't have access to
| [BL-2588329](https://hackerone.com/reports/2588329) | indrive | $2,000 | account_invite_access_workflows | full | Change phone number OTP flaw leads to any phone number takeover
| [BL-2616045](https://hackerone.com/reports/2616045) | automattic | - | race_condition_replay | full | Race condition on add 1 free domain
| [BL-2712583](https://hackerone.com/reports/2712583) | mozilla | - | account_invite_access_workflows | full |  Bypass Email verification for monitoring at `monitor.mozilla.org`
| [BL-2801036](https://hackerone.com/reports/2801036) | doppler | $250 | rate_limit_state_abuse | full | Availability Impact from Exploiting Project Name Vulnerabilities
| [BL-2914705](https://hackerone.com/reports/2914705) | cosmos | - | rate_limit_state_abuse | full | Making transfer v2 channel unupgradable through the forwarding 
| [BL-2917368](https://hackerone.com/reports/2917368) | cosmos | - | rate_limit_state_abuse | full | Replacing ICA active channel during the upgrade and a bit more
| [BL-3136790](https://hackerone.com/reports/3136790) | toolsforhumanity | $300 | commerce_payments_rewards | full | Unlock underage blocked app without support interaction using airplane mode

Bounty arithmetic: $7,500 (BL-1295844) + $5,000 (BL-1285598) + $5,000 (BL-1543159) + $5,000 (BL-1849626) + $2,900 (BL-1044285) + $2,500 (BL-334205) + $2,400 (BL-1565623) + $2,400 (BL-1565624) + $2,400 (BL-1614331) + $2,400 (BL-1912778) + $2,000 (BL-2588329) + $1,120 (BL-263760) + $1,000 (BL-226199) + $1,000 (BL-462503) + $1,000 (BL-1234760) + $800 (BL-1172857) + $750 (BL-312118) + $700 (BL-1213175) + $560 (BL-666632) + $500 (BL-331691) + $500 (BL-361960) + $500 (BL-413759) + $500 (BL-460920) + $500 (BL-463828) + $500 (BL-475660) + $500 (BL-549364) + $500 (BL-706934) + $500 (BL-763177) + $500 (BL-1112679) + $500 (BL-1213765) + $500 (BL-1297689) + $500 (BL-1365738) + $500 (BL-1770797) + $480 (BL-1614332) + $480 (BL-1874715) + $480 (BL-1874716) + $480 (BL-1912770) + $480 (BL-1912777) + $480 (BL-1912782) + $480 (BL-1912783) + $400 (BL-1397826) + $350 (BL-1182864) + $300 (BL-434116) + $300 (BL-1523584) + $300 (BL-1566325) + $300 (BL-3136790) + $250 (BL-974892) + $250 (BL-2257374) + $250 (BL-2801036) + $200 (BL-1364851) + $100 (BL-808287) + $100 (BL-1406926) + $100 (BL-1538669) + $50 (BL-428660) + $50 (BL-1316650) = **$60,090** (55 rows).

Module totals: commerce_payments_rewards $19,150/8 · account_invite_access_workflows $9,010/12 · race_condition_replay $750/2 · rate_limit_state_abuse $3,100/6 · _adjacent $24,580/24 · _adjacent_unclassified $3,500/3.

DB metadata columns (weakness_name / asset_identifier / asset_type / cve_ids) are preserved in this ledger's source rows: all 118 bucket rows carry `weakness_name=Business Logic Errors` in the DB; the 9 unclassified merges carry `None` (the classifier had not labeled them). CVE-bearing rows (18) are the curl/ibb shelf + nextcloud/ruby rows in module 05 §4 and module 04 — `CVE-2022-27778`, `CVE-2022-27782`, `CVE-2022-32207`, `CVE-2022-32208`, `CVE-2023-23914`, `CVE-2023-23915`, `CVE-2023-27533`, `CVE-2023-27534`, `CVE-2023-27535`, `CVE-2023-27536`, `CVE-2023-27538`, `CVE-2021-22897`, `CVE-2021-22922`, `CVE-2021-22926`, `CVE-2020-8181`, `CVE-2022-29163`, `CVE-2021-41180`, `CVE-2013-0269`.
