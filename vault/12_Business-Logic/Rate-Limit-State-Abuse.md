---
title: "Rate-limit & state abuse — unthrottled endpoints, brute-forceable state and mass-claim logic"
type: playbook
category: rate_limit_state_abuse
cwe: "CWE-841"
source_count: 21
full_bodies_available: 21
corpus: "h1-brain disclosed_reports.db, bucket business-logic (module rate_limit_state_abuse, 21 rows, bodies-win)"
list_accessed: "2026-11-07"
note: "Claims trace to bodies read 2026-11-07 and archived in references/archive/BL-bodies-full-dump.txt; quotes byte-true."
---


# Rate-limit & state abuse


Pattern: an endpoint whose action is bounded by business rules is guarded by nothing. Unthrottled creation, comment, poll, report and email endpoints let volume become the attack; or a state secret (OTP, password-cookie) is brute-forceable because checking it is unthrottled.


## 1. Overview


Case stock (21 rows / 6 paid / $3,100; bucket module `rate_limit_state_abuse`):


| Case | Target | Mechanism | Bounty |
|---|---|---|---|
| [BL-297359](https://hackerone.com/reports/297359) | x | No Rate Limit in email leads to huge Mass mailings | - |
| [BL-312118](https://hackerone.com/reports/312118) | gitlab | Using GitLab to monitor and hijack domains in mass quantity. | $750 |
| [BL-416906](https://hackerone.com/reports/416906) | chaturbate | Missing Rate Limitation at /apps/upload_app/ | - |
| [BL-422279](https://hackerone.com/reports/422279) | shopify | H1514 Simple phishing using auto-created modal with weak URL-patter... | - |
| [BL-426547](https://hackerone.com/reports/426547) | chaturbate | Missing Rate Limitation at /photo_videos/photoset/create | - |
| [BL-460920](https://hackerone.com/reports/460920) | security | Response program can create bounty table | $500 |
| [BL-462503](https://hackerone.com/reports/462503) | gitlab | Claiming package names in GitLab's automatic package referencer. | $1,000 |
| [BL-475660](https://hackerone.com/reports/475660) | security | Response program can display "eligible for bounty" in scope area in... | $500 |
| [BL-488923](https://hackerone.com/reports/488923) | automattic | No Rate Limit on CrowdSignal Polls when Adding Comment | - |
| [BL-568832](https://hackerone.com/reports/568832) | automattic | No rate limit on app.crowdsignal.com (Finish quiz) | - |
| [BL-905816](https://hackerone.com/reports/905816) | automattic | No Rate Limit when accessing "Password protection" enabled surveys ... | - |
| [BL-1051734](https://hackerone.com/reports/1051734) | automattic | [intensedebate.com] No Rate Limit On The report Functionality Lead ... | - |
| [BL-1133118](https://hackerone.com/reports/1133118) | security | Hackerone is not properly deleting user id | - |
| [BL-1337178](https://hackerone.com/reports/1337178) | nextcloud | objectId in share location can be set to open arbitrary URL or Deep... | - |
| [BL-1406926](https://hackerone.com/reports/1406926) | nextcloud | bypass forced password protection via circles app | $100 |
| [BL-1446107](https://hackerone.com/reports/1446107) | exness | Verification process done using different documents without corresp... | - |
| [BL-1991376](https://hackerone.com/reports/1991376) | indrive | the domain is truck-admin.eu-east-1.indriverapp.com and Enter the m... | - |
| [BL-2033005](https://hackerone.com/reports/2033005) | frontegg | Bypassing the block of Security Domain Restriction and normally inv... | - |
| [BL-2801036](https://hackerone.com/reports/2801036) | doppler | Availability Impact from Exploiting Project Name Vulnerabilities | $250 |
| [BL-2914705](https://hackerone.com/reports/2914705) | cosmos | Making transfer v2 channel unupgradable through the forwarding | - |
| [BL-2917368](https://hackerone.com/reports/2917368) | cosmos | Replacing ICA active channel during the upgrade and a bit more | - |


## 2. Mass-claim of names and domains — BL-462503 (gitlab, $1,000) and BL-312118 (gitlab, $750)


GitLab auto-links npm packages by name assumption; the reporter claims the name on npm and the trusted page now routes users to the malicious module:


> The problem is that GitLab currently assumes that packages have been uploaded to a registry by default.




> An adversary can trick an unsuspecting user into installing and executing a malicious package from the npm registry. What makes this attack possible is the fact that the package appears to belong to a trusted entity due to GitLab linking to the malicious packet from the project's page.


The domain row generalizes it: unlimited custom domains per repository, no ownership proof, so a script claims every domain pointed at GitLab's IP overnight:


> First, I wrote a fully-fledged exploit that hijacks unclaimed domains. In under 5s I managed to secure 110 domains.




> GitLab allows setting an unlimited number of domains for a single repository.


## 3. HackerOne program-state abuse — BL-460920 and BL-475660 (security, $500 each)


A Response (non-bounty) program can create a full bounty table via the GraphQL `updateBountyTable` mutation —


> Create bounty table in response program and show it in home page.


— and the `eligible_for_bounty` flag, once set under a bounty program, persists through a switch to Response:


> "variables":{"input_0":{"team_id":"Z2lkOi8vaGFja2Vyb25lL1RlYW0vMzYxNzE=","asset_type":"URL","asset_identifier":"google.com","eligible_for_bounty":true,"eligible_for_submission":true,"instruction":"","reference":"","clientMutationId":"0"},"first_1":250,"types_2":"ARGUMENT"}




> where `eligible for bounty: true` remains permanent from backend even if we switch from h1 bounty program to response program.


## 4. Brute-force-through-the-cookie — BL-905816 (automattic, unpaid)


The survey password gate is rate-limited, but the cookie it sets is `pd-pass_<surveyid> = md5(password)`. Brute-force the cookie directly, unthrottled:


> And basically this is `pd-pass_SURVEYID=md5(password)`, it encrypts the right password with MD5 and if you visit the survey page with this cookie, you can see the survey.




> So, I tried to brute force this cookie with Burp Suite's `Payload Processing` feature. (it encrypts your value with any hash type). And it worked, there is no rate limit when directly accessing to the survey page with password cookie.




BL-1991376 (indrive, unpaid) is the OTP sibling: a 4-digit admin SMS code blasted 6000–7000 within the expiry window found the code in 8 attempts.


## 5. Unthrottled volume endpoints (the unpaid bulk)


BL-416906 (chaturbate): `/apps/upload_app/` creates unlimited apps. BL-426547 (chaturbate): `/photo_videos/photoset/create` creates unlimited albums. BL-488923/568832 (automattic): CrowdSignal poll comments and quiz-completion are unthrottled. BL-1051734 (automattic): report-a-comment spam deletes any comment once the report threshold is hit. BL-297359 (x): `/web-client/api/ad-units/email-instructions` sends unlimited integration emails. BL-1406926 (nextcloud, $100): circles bypass admin-forced password protection on shares — a policy-gate the rate-limit pass drifted across.



## 6. Bypass-by-normalization and identity-state rows


BL-2033005 (frontegg, unpaid) invites blocked domains with `İ` for `i` — the deny-list never normalizes Unicode. BL-1446107 (exness, unpaid) re-PATCHes KYC identity fields after verification. BL-1133118 (security, unpaid): alias emails survive account deletion. BL-1337178 (nextcloud, unpaid): `objectId` in shared locations becomes an arbitrary deeplink. BL-2801036 (doppler, $250): a malicious project name stored by one user logs out every other member (DoS by stored string). BL-2914705/2917368 (cosmos, unpaid) are protocol-state abuses — packet-forwarding locks channel upgrades; ICA active-channel replacement during upgrades.


## 7. What pays / what doesn't


**Pays:** names/domains with demonstrated redirection (462503 $1,000; 312118 $750 — both GitLab, both with a live claim artifact); program-trust confusion with a user-facing lie (460920/475660, $500 each). **Doesn't price (here):** pure volume rows with no demonstrated downstream harm (416906, 426547, 488923, 568832, 297359 — all $0), and clever-in-theory protocol rows (2914705, 2917368, $0).


## 8. Cross-references


- Rate-Limiting vault (`20_Rate-Limiting/`): the adjacent vault defines the class; this module is its bucket-slice.
- Commerce module §7: BL-592803's points farm is the same volume logic pointed at rewards.
- Account module §4: BL-2588329 vs BL-1991376 — accepted-invalid OTP vs brute-forced OTP.
