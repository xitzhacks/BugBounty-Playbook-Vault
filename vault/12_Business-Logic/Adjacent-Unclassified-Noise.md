---
title: "Adjacent + unclassified-merged noise — everything the bucket's keyword net caught that is not business logic"
type: playbook
category: adjacent-noise
cwe: "CWE-707"
source_count: 40
full_bodies_available: 40
corpus: "h1-brain disclosed_reports.db, bucket business-logic adjacent pools (_adjacent 31 + _adjacent_unclassified 9 merged, bodies-win)"
list_accessed: "2026-11-07"
note: "Negative-space module: claims trace to bodies read 2026-11-07 and archived in references/archive/BL-bodies-full-dump.txt; quotes byte-true."
---


# Adjacent + unclassified-merged noise


Forty rows from two pools: `_adjacent` (31 bucket rows the bodies-win pass kept as business-logic but that are other classes — subdomain takeover, curl CVEs, misconfiguration, deserialization, payments plumbing) and `_adjacent_unclassified` (9 rows from the classifier's unclassified pool merged in on body read — all nine are genuine business-logic and are discussed first as true positives the funnel missed; the bucket's 118 rows are all inside modules 01–05, this module is the overflow shelf). $28,080/27 paid — the module's money is dominated by one S3-takeover row that is not business-logic at all.


## 1. Overview


Case stock (40 rows / 27 paid / $28,080; pools `_adjacent` + `_adjacent_unclassified`):


| Case | Target | Mechanism | Bounty |
|---|---|---|---|
| [BL-225831](https://hackerone.com/reports/225831) | dashlane | Extract Billing admin email address using random team id | - |
| [BL-263760](https://hackerone.com/reports/263760) | x | Opportunity to obtain private tweets through search widget preview ... | $1,120 |
| [BL-320355](https://hackerone.com/reports/320355) | shopify | myshopify.com domain takeover | - |
| [BL-403602](https://hackerone.com/reports/403602) | basecamp | Attachments may be hijacked via AppCache+CookieBombing trick (bc3_p... | - |
| [BL-423467](https://hackerone.com/reports/423467) | shopify | H1514 Ability to MiTM Shopify PoS Session to Takeover Communications | - |
| [BL-637267](https://hackerone.com/reports/637267) | upserve | Payment method token being sent to 3rd party analytics service | - |
| [BL-706934](https://hackerone.com/reports/706934) | ruby | Variant of CVE-2013-0269 (Denial of Service and Unsafe Object Creat... | $500 |
| [BL-1034023](https://hackerone.com/reports/1034023) | bumble | Possible (we need to wait for some time) takeover of subdomain bado... | - |
| [BL-1082847](https://hackerone.com/reports/1082847) | grammarly | Config override using non-validated query parameter allows at least... | - |
| [BL-1112679](https://hackerone.com/reports/1112679) | security | Dangling cloud instance at vpn.inverselink.com | $500 |
| [BL-1172857](https://hackerone.com/reports/1172857) | curl | CVE-2021-22897: schannel cipher selection surprise | $800 |
| [BL-1182864](https://hackerone.com/reports/1182864) | zomato | Subdomain takeover of fr1.vpn.zomans.com | $350 |
| [BL-1213175](https://hackerone.com/reports/1213175) | curl | CVE-2021-22922: Wrong content via metalink not discarded | $700 |
| [BL-1234760](https://hackerone.com/reports/1234760) | curl | CVE-2021-22926: CURLOPT_SSLCERT mixup with Secure Transport | $1,000 |
| [BL-1285598](https://hackerone.com/reports/1285598) | reddit | s3 bucket takeover presented in https://github.com/reddit/rpan-stud... | $5,000 |
| [BL-1297689](https://hackerone.com/reports/1297689) | affirm | Subdomain takeover of www█████████.affirm.com | $500 |
| [BL-1316650](https://hackerone.com/reports/1316650) | brave | unclaimed s3 bucket takeover in the 3 js file located on the github... | $50 |
| [BL-1364851](https://hackerone.com/reports/1364851) | trafficfactory | WordPress Plugin Update Confusion at trafficfactory.com | $200 |
| [BL-1365738](https://hackerone.com/reports/1365738) | flickr | critical server misconfiguration lead to access to any user sensiti... | $500 |
| [BL-1397826](https://hackerone.com/reports/1397826) | cosmos | Unclaimed official s3 bucket of tendermint(tendermint-packages) whi... | $400 |
| [BL-1565623](https://hackerone.com/reports/1565623) | ibb | CVE-2022-27778: curl removes wrong file on error | $2,400 |
| [BL-1565624](https://hackerone.com/reports/1565624) | ibb | CVE-2022-27782: TLS and SSH connection too eager reuse | $2,400 |
| [BL-1614331](https://hackerone.com/reports/1614331) | ibb | CVE-2022-32207: Unpreserved file permissions | $2,400 |
| [BL-1614332](https://hackerone.com/reports/1614332) | ibb | CVE-2022-32208: FTP-KRB bad message verification | $480 |
| [BL-1874715](https://hackerone.com/reports/1874715) | ibb | CVE-2023-23914: HSTS ignored on multiple requests | $480 |
| [BL-1874716](https://hackerone.com/reports/1874716) | ibb | CVE-2023-23915: HSTS amnesia with --parallel | $480 |
| [BL-1912770](https://hackerone.com/reports/1912770) | ibb | CVE-2023-27533: TELNET option IAC injection | $480 |
| [BL-1912777](https://hackerone.com/reports/1912777) | ibb | CVE-2023-27534: SFTP path ~ resolving discrepancy | $480 |
| [BL-1912778](https://hackerone.com/reports/1912778) | ibb | CVE-2023-27535: FTP too eager connection reuse | $2,400 |
| [BL-1912782](https://hackerone.com/reports/1912782) | ibb | CVE-2023-27536: GSS delegation too eager connection re-use | $480 |
| [BL-1912783](https://hackerone.com/reports/1912783) | ibb | CVE-2023-27538: SSH connection too eager reuse still | $480 |
| [BL-145467](https://hackerone.com/reports/145467) | vimeo | Downloading password protected / restricted videos | - |
| [BL-321938](https://hackerone.com/reports/321938) | zomato | [www.zomato.com] Getting a complimentary dessert [Zomato Treats] on... | - |
| [BL-434116](https://hackerone.com/reports/434116) | phabricator | Exposing voting results on the Slowvote application without actuall... | $300 |
| [BL-915140](https://hackerone.com/reports/915140) | automattic | Users can bypass page restrictions via Export feature at "Share" fe... | - |
| [BL-965510](https://hackerone.com/reports/965510) | shopify | Password protection can be removed for newly created development store | - |
| [BL-989415](https://hackerone.com/reports/989415) | cs_money | Bypass restrict of member subscription to use custom background in ... | - |
| [BL-1044285](https://hackerone.com/reports/1044285) | shopify | Removing parts of URL from jQuery request exposes links for downloa... | $2,900 |
| [BL-1443211](https://hackerone.com/reports/1443211) | mattermost | Bypass Email Verification in Customer Portal | - |
| [BL-1566325](https://hackerone.com/reports/1566325) | phabricator | Conduit feed.publish API allows you to spoof other users or make it... | $300 |


## 2. Unclassified-merge true positives (9 rows — the funnel's miss, vault's gain)


Each of these is a clean business-logic primitive the keyword classifier put in `unclassified`; the DB has no weakness label for any of them:


- **BL-1044285 (shopify, $2,900)** is the merge pool's richest row: the `get_download_link` jQuery request works with an *empty* `checkout_token`, returning the most recent (anyone's) order's download links.


> This could lead an attacker simply getting every possible download link of the most recent order placed!!!


- **BL-434116 (phabricator, $300)**: an illegal `vote%5B%5D` vote_id unlocks poll results that are otherwise gated behind voting.


> An unauthorized user can see poll results without making a vote as required by an admin.


- **BL-1566325 (phabricator, $300)**: `feed.publish` accepts any `authorPHID` — forged feed stories attributing token awards to anyone.


> An attacker can make make it look a user has performed an action which the user did not perform (awarding  a token), this could result in the relevant user being disabled if it is suspected that the account was compromised.


- **BL-321938 (zomato, unpaid)**: a free `item_id 18` plan swap drops Zomato Treats from ₹149 to ₹0 — the module-01 `plan_id` primitive. BL-915140 (automattic, unpaid): survey Share exports leak restricted pages by URL. BL-965510 (shopify, unpaid): dev-store password removed via GraphQL `PreferencesSave`. BL-989415 (cs_money, unpaid): prime background via direct API. BL-145467 (vimeo, unpaid): password-protected video download via the ATV API — access control, not logic, but kept as the merge pool's cleanest exhibit. BL-1443211 (mattermost, unpaid): victim's OTP reused in the attacker's email-verify.


## 3. The subdomain-takeover cluster (8 rows — other vault's money)


**BL-1285598 (reddit, $5,000)** — the vault's third-largest figure belongs to an unclaimed S3 bucket referenced by Reddit's build scripts, a textbook takeover that has nothing to do with business logic:


> An attacker can takeover the s3 bucket and can host his malicious content with the name (cef_binary_${1}_macosx64.tar.bz2) as presented in the code and can spread ransomware and many malicious files.


The rest are the standard dangling-resource catalog: BL-1297689 (affirm, $500, S3 bucket), BL-1112679 (security, $500, Workday IP), BL-1182864 (zomato, $350, signed-EC2 IP), BL-1397826 (cosmos, $400, tendermint-packages bucket), BL-1316650 (brave, $50, brave-extensions bucket), BL-320355 (shopify, unpaid, the reporter's own confession of a domain-takeover *attempt*), BL-1034023 (bumble, unpaid, prospective Medium takeover). Their home vault is `13_Subdomain-Takeover/`; here they document bucket drift.



## 4. The curl/ibb CVE shelf (15 rows — library logic, not app logic)


The bucket absorbed an entire run of curl/ibb advisories: connection-reuse flaws (1565624, 1912778, 1912782, 1912783), cipher/cert mixups (1172857, 1234760), HSTS amnesia (1874715, 1874716), wrong-file removal (1565623), metalink hash-not-enforced (1213175), FTP-KRB verify (1614332), unpreserved permissions (1614331), TELNET injection (1912770), SFTP tilde (1912777), plus ruby JSON unsafe object creation (706934). All paid — the language/library programs pay flat — but none is a web business-logic flaw:


> As a result for example TLS connection with  lower security (`CURLSSLOPT_ALLOW_BEAST`,` CURLSSLOPT_NO_REVOKE`) connection reused when it should no longer be.




> Modified or tampered files are kept and possibly incorrectly assumed valid


Kept because the keyword net's business-logic arm matched `logic flaw` wording in the advisory text; the vault's call is that the flaw is a client library's, not an application's business rule.


## 5. Genuine business-logic that drifted into _adjacent


A handful of `_adjacent` rows really are business-logic and would sit in modules 01–04 if the map had been coarser: BL-225831 (dashlane, unpaid) enumerates billing-admin emails by `teamId`; BL-263760 (x, $1,120) revives private/deleted tweets from widget preview caches; BL-637267 (upserve, unpaid) reuses a `payment_method_token` across accounts; BL-403602 (basecamp, unpaid) hijacks attachment buckets via AppCache+CookieBombing. BL-423467 (shopify, unpaid) is a PoS WebSocket MiTM with a receiver-public-key override — more crypto than logic. BL-1082847 (grammarly, unpaid) is config-override XSS with business-logic side effects. BL-1365738 (flickr, $500) is the legacy-server credential dump — misconfiguration, kept as the shelf's most expensive non-takeover row. BL-1364851 (trafficfactory, $200) is WordPress plugin-update confusion (supply-chain, its own class).


## 6. What pays / what doesn't


**Pays:** the takeover rows (1285598 $5,000; 1297689 $500), the curl shelf at flat rates ($480–$2,400), one cache-logic row (263760, $1,120), one legacy-misconfig row (1365738, $500). **Doesn't price:** attempts and near-misses (320355, 1034023 — $0), and every genuinely adjacent concept (423467, 1082847 — $0). The lesson of the shelf: these rows pay under *their* classes' rules; the business-logic bucket name is the only thing being tested here.


## 7. Cross-references


- `13_Subdomain-Takeover/` — §3's natural home; the cross-cite is recorded there.
- `19_Cryptography/` — BL-423467's key-override is their class; BL-1172857's cipher confusion is theirs too.
- Modules 01–04: §5's four drifted rows are their hunting ground.
