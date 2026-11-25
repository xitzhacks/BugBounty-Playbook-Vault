---
title: "File, Path, Error & Secret Leaks — .git, .env, stacks, dumps, and dumped tokens"
type: playbook
category: file-path-errors-secrets-leaks
cwe: "CWE-200"
source_count: 104
full_bodies_available: 104
corpus: "h1-brain disclosed_reports.db (sha256 8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4) — 362 rows"
list_accessed: "2026-11-07"
note: "Anchors: INFO-509924 (gitlab, $12,000), INFO-850447 (gitlab, $10,000), INFO-1256375 (shopify, $5,000), INFO-136454 (ibb, $3,000), INFO-1021906 (shopify, $2,900), INFO-2915647 (mozilla, $1,500). All quotes byte-true to references/archive/INFO-bodies-full-dump.txt."
---

# File, Path, Error & Secret Leaks — .git, .env, stacks, dumps, and dumped tokens

## 1. Overview

One hundred four rows, **$48,697/41 paid** (max $12,000) — the vault's second-richest module and its most heterogeneous: directory indexes, stack traces, dotfiles (`.git`, `.htpasswd`, `.DS_Store`), publicly listable buckets, hardcoded credentials in apps and repos, CI logs carrying tokens, and file-read primitives dressed as disclosures. The paid set splits into three economies: **two GitLab singulars** ($12,000 serialization, $10,000 workhorse file-read), a **$1,000–$5,000 mid-tier** of bucket exposures, atom-feed bypasses, and cross-domain script leaks, and a **$100–$500 floor** of dotfile/dotdir singles. Sixty-three rows carry no figure — the module's long tail is where the request-path hygiene findings live (full-path disclosures, verbose errors, S3 listings) and its zero figure does not mean zero value; DB `None` is a figure absence, not a rejection.

**Case-stock (104 rows / $48,697):**

| Case | Target | Mechanism | Bounty |
|---|---|---|---|
| [INFO-509924](https://hackerone.com/reports/509924) | gitlab | JSON serialization of any Project model results in all Runner tokens being exp… | $12,000 |
| [INFO-850447](https://hackerone.com/reports/850447) | gitlab | gitlab-workhorse bypass in Gitlab::Middleware::Multipart allowing files in `al… | $10,000 |
| [INFO-1256375](https://hackerone.com/reports/1256375) | shopify | Blog posts atom feed of a store with password protection can be accessed by an… | $5,000 |
| [INFO-136454](https://hackerone.com/reports/136454) | ibb | User credentials leak and arbitrary local file read/leak due to same-origin-po… | $3,000 |
| [INFO-1021906](https://hackerone.com/reports/1021906) | shopify | [Information Disclosure] Amazon S3 Bucket of Shopify Ping (iOS) have public ac… | $2,900 |
| [INFO-124100](https://hackerone.com/reports/124100) | shopify | Shopify GitHub Login and Password exposed all private source code might be ava… | $1,500 |
| [INFO-2244229](https://hackerone.com/reports/2244229) | x | Cross-Domain Leakage of X Username / UserID due to Dynamically Generated JS Fi… | $1,500 |
| [INFO-2915647](https://hackerone.com/reports/2915647) | mozilla | Netlify Authentication Token Exposed in Public Mozilla CI Logs | $1,500 |
| [INFO-2937622](https://hackerone.com/reports/2937622) | security | Public GitHub repositories for multiple HackerOne managed triage team profiles… | $1,200 |
| [INFO-1575014](https://hackerone.com/reports/1575014) | stripe | Limited path traversal in Node.js SDK leads to PII disclosure | $1,000 |
| [INFO-2467999](https://hackerone.com/reports/2467999) | mozilla | Jira Credential Disclosure within Mozilla Slack | $1,000 |
| [INFO-377107](https://hackerone.com/reports/377107) | owncloud | Possible to steal any protected files on Android | $750 |
| [INFO-1668723](https://hackerone.com/reports/1668723) | brave | Security token and handler name leak from window.braveBlockRequests | $700 |
| [INFO-213558](https://hackerone.com/reports/213558) | discourse | Arbitrary Local-File Read from Admin - Restore From Backup due to Symlinks | $512 |
| [INFO-2894283](https://hackerone.com/reports/2894283) | ibb | netrc and redirect credential leak | $505 |
| [INFO-375083](https://hackerone.com/reports/375083) | slack | Private application files can be uploaded to Slack via malicious uploader | $500 |
| [INFO-446238](https://hackerone.com/reports/446238) | gitlab | EXIF metadata not stripped from JPG group logos | $500 |
| [INFO-729040](https://hackerone.com/reports/729040) | shopify | Shopify's SF and LA offices Dashboard Information disclosed via Public Gist | $500 |
| [INFO-1491127](https://hackerone.com/reports/1491127) | security | Private invitation links/tokens leak to third-party analytics site | $500 |
| [INFO-1249056](https://hackerone.com/reports/1249056) | brave | Brave Browser permanently timestamps & logs connection times for all v2 domain… | $400 |
| [INFO-348443](https://hackerone.com/reports/348443) | gitlab | Snippet JS template allows attacker to read a user's private snippets | $300 |
| [INFO-218465](https://hackerone.com/reports/218465) | x | [staging-engineering.gnip.com] Publicly accessible GIT directory | $280 |
| [INFO-268888](https://hackerone.com/reports/268888) | x | Sensitive Information Disclosure https://cards-dev.twitter.com | $280 |
| [INFO-674774](https://hackerone.com/reports/674774) | x | AppLovin API Key hardcoded in a Github repo | $280 |
| [INFO-1940443](https://hackerone.com/reports/1940443) | snapchat | internal dev tokens disclosure | $250 |
| [INFO-302651](https://hackerone.com/reports/302651) | portswigger | Leak of Platform Authentication credentials via Repeater | $200 |
| [INFO-864712](https://hackerone.com/reports/864712) | zomato | Page has a link to google drive which has logos and a few customer phone recor… | $200 |
| [INFO-211418](https://hackerone.com/reports/211418) | rockstargames | Source Code Disclosure (CGI) | $150 |
| [INFO-262649](https://hackerone.com/reports/262649) | gsa_bbp | Information disclosure (system username) in the x-amz-meta-s3cmd-attrs respons… | $150 |
| [INFO-278191](https://hackerone.com/reports/278191) | x | Listing of Amazon S3 Bucket accessible to any amazon authenticated user (metri… | $140 |
| [INFO-64731](https://hackerone.com/reports/64731) | vkcom | Able to intercept app Traffic after choosing up the Secured Connection using S… | $100 |
| [INFO-147577](https://hackerone.com/reports/147577) | coinbase | Application error message | $100 |
| [INFO-158021](https://hackerone.com/reports/158021) | instacart | Image Upload Path Disclosure | $100 |
| [INFO-212067](https://hackerone.com/reports/212067) | algolia | An “algobot”-s GitHub access token was leaked | $100 |
| [INFO-880089](https://hackerone.com/reports/880089) | smartsheet | Smartsheet employees email disclosure through enpoint after login. | $100 |
| [INFO-1024668](https://hackerone.com/reports/1024668) | brave | Brave Browser potentially logs the last time a Tor window was used | $100 |
| [INFO-1121972](https://hackerone.com/reports/1121972) | acronis | admin password disclosure via log file | $100 |
| [INFO-1474017](https://hackerone.com/reports/1474017) | omise | Open S3 Bucket Accessible by any User | $100 |
| [INFO-2097377](https://hackerone.com/reports/2097377) | gitlab | Information Disclosure - Pvt Gitlab Issue Disclosing Through GitLab Unfiltered… | $100 |
| [INFO-231917](https://hackerone.com/reports/231917) | nextcloud | Shared file link - password protection bypass under certain conditions | $50 |
| [INFO-1079630](https://hackerone.com/reports/1079630) | acronis | licenses key disclosure | $50 |
| [INFO-46345](https://hackerone.com/reports/46345) | whisper | Directory index and information disclosure | - |
| [INFO-46366](https://hackerone.com/reports/46366) | whisper | Error stack trace | - |
| [INFO-91343](https://hackerone.com/reports/91343) | imgur | Information disclosure (No rate limting in forgot password & other login) | - |
| [INFO-163476](https://hackerone.com/reports/163476) | legalrobot | Information Disclosure in AWS S3 Bucket | - |
| [INFO-166265](https://hackerone.com/reports/166265) | yelp | Verification of E-Mail address possible on https://biz.yelp.com/login and http… | - |
| [INFO-166942](https://hackerone.com/reports/166942) | x | leaking Digits OAuth authorization to third party websites | - |
| [INFO-174645](https://hackerone.com/reports/174645) | files | Existence of Folder path by guessing the path through response | - |
| [INFO-175320](https://hackerone.com/reports/175320) | brave | 2 Directory Listing on ledger.brave.com & vault-staging.brave.com | - |
| [INFO-201984](https://hackerone.com/reports/201984) | ui | Wordpress directories/files visible to internet | - |
| [INFO-210572](https://hackerone.com/reports/210572) | rockstargames | Full path Disclosure in Rockstargames.com██████████ | - |
| [INFO-211477](https://hackerone.com/reports/211477) | shopify | Stealing users' facebook access tokens - kitcrm.com | - |
| [INFO-213942](https://hackerone.com/reports/213942) | phabricator | Differential "Show Raw File" feature exposes generated files to unauthorised u… | - |
| [INFO-248693](https://hackerone.com/reports/248693) | grab | Git repository found | - |
| [INFO-258084](https://hackerone.com/reports/258084) | nextcloud | Access to all files of remote user through shared file | - |
| [INFO-258460](https://hackerone.com/reports/258460) | quora | [Quora Android] Possible to steal arbitrary files from mobile device | - |
| [INFO-268382](https://hackerone.com/reports/268382) | gsa_bbp | Nginx misconfiguration leading to direct PHP source code download | - |
| [INFO-288955](https://hackerone.com/reports/288955) | irccloud | [IRCCloud Android] Theft of arbitrary files leading to token leakage | - |
| [INFO-301526](https://hackerone.com/reports/301526) | security | Invitation token leaks to https://bat.bing.com | - |
| [INFO-345152](https://hackerone.com/reports/345152) | shopify | Publicly Accessible Datadog link | - |
| [INFO-360811](https://hackerone.com/reports/360811) | starbucks | Information Leak - Github - JMS Information | - |
| [INFO-396467](https://hackerone.com/reports/396467) | snapchat | Github Token Leaked publicly for https://github.sc-corp.net | - |
| [INFO-397508](https://hackerone.com/reports/397508) | chaturbate | Web cache deception attack - expose token information | - |
| [INFO-397527](https://hackerone.com/reports/397527) | grab | Leaking sensitive information on Github lead full access to all Grab Slack cha… | - |
| [INFO-425719](https://hackerone.com/reports/425719) | shopify | Disclosure of Github Issues | - |
| [INFO-511440](https://hackerone.com/reports/511440) | zomato | credentials leakage in public lead to view dev websites | - |
| [INFO-612231](https://hackerone.com/reports/612231) | x | Github Token Leaked publicly for https://github.com/mopub | - |
| [INFO-753868](https://hackerone.com/reports/753868) | zenly | Insecure Storage and Overly Permissive API Keys in Android App | - |
| [INFO-853355](https://hackerone.com/reports/853355) | gitlab | Unauthorized access to private project security dashboard | - |
| [INFO-858915](https://hackerone.com/reports/858915) | shopify | CircleCI token in github repo allows for access to sensitive build information | - |
| [INFO-861940](https://hackerone.com/reports/861940) | semrush | OAuth `redirect_uri` bypass using IDN homograph attack resulting in user's acc… | - |
| [INFO-901775](https://hackerone.com/reports/901775) | shopify | Get analytics token using only apps permission | - |
| [INFO-962462](https://hackerone.com/reports/962462) | gitlab | Unauthorized user is able to access schedule pipeline variables and values | - |
| [INFO-966383](https://hackerone.com/reports/966383) | kubernetes | secret leaks in vsphere cloud controller manager log | - |
| [INFO-981796](https://hackerone.com/reports/981796) | basecamp | Information Disclosure of Garbage Collection Cycle | - |
| [INFO-1004412](https://hackerone.com/reports/1004412) | acronis | Possible LDAP username and password disclosed on Github | - |
| [INFO-1007988](https://hackerone.com/reports/1007988) | automattic | Able to comment/view in others support ticket at https://en.instagram-brand.co… | - |
| [INFO-1065041](https://hackerone.com/reports/1065041) | fetlife | Google API key leaked to Public | - |
| [INFO-1069039](https://hackerone.com/reports/1069039) | reddit | GPS metadata preserved when converting HEIF to PNG | - |
| [INFO-1122177](https://hackerone.com/reports/1122177) | reddit | Third party app could steal access token as well as protected files using inAp… | - |
| [INFO-1262907](https://hackerone.com/reports/1262907) | shopify | Apache Flink Dashboard exposure at https://streaming-sales-model-production.fl… | - |
| [INFO-1264725](https://hackerone.com/reports/1264725) | security | Information disclosure - Feedback is accessible on Public profile even after '… | - |
| [INFO-1337422](https://hackerone.com/reports/1337422) | nextcloud | Folder architecture and Filesizes of private file drop shares can be getten | - |
| [INFO-1338781](https://hackerone.com/reports/1338781) | nextcloud | User files is disclosed when someone called while the screen is locked | - |
| [INFO-1354334](https://hackerone.com/reports/1354334) | nextcloud | Error in Deleting Deck cards attachment reveals the full path of the website | - |
| [INFO-1405673](https://hackerone.com/reports/1405673) | shopify | Sidekiq dashboard exposed at notary.shopifycloud.com | - |
| [INFO-1484168](https://hackerone.com/reports/1484168) | automattic | De-anonymize anonymous tips through the Tumblr blog network | - |
| [INFO-1624152](https://hackerone.com/reports/1624152) | deptofdefense | insecure gitlab repositories at ████████ [HtUS] | - |
| [INFO-1626281](https://hackerone.com/reports/1626281) | snapchat | Password reset tokens sent to CSP reporting endpoints | - |
| [INFO-1643962](https://hackerone.com/reports/1643962) | gitlab | Path paths and file disclosure vulnerabilities at influxdb.quality.gitlab.net | - |
| [INFO-1662194](https://hackerone.com/reports/1662194) | omise | Secret API Key is logged in cleartext | - |
| [INFO-1762764](https://hackerone.com/reports/1762764) | expediagroup_bbp | Sensitive information for phpinfo.php at https://products.ean.com/ | - |
| [INFO-1784310](https://hackerone.com/reports/1784310) | nextcloud | Messages can still be seen on conversation after expiring when cron is misconf… | - |
| [INFO-1785145](https://hackerone.com/reports/1785145) | indrive | Full access to InDrive jira panel via exposed API token | - |
| [INFO-1989901](https://hackerone.com/reports/1989901) | mozilla | If rate limit is hit, IP address is leaked to anyone who tries to login | - |
| [INFO-2101165](https://hackerone.com/reports/2101165) | nextcloud | user_ldap app logs user passwords in the log file on level debug | - |
| [INFO-2180521](https://hackerone.com/reports/2180521) | security | Google Docs link in JS files allows editing & reading survey information | - |
| [INFO-2209665](https://hackerone.com/reports/2209665) | ibb | Secrets can be unmasked in the "Rendered Template" | - |
| [INFO-2376909](https://hackerone.com/reports/2376909) | nextcloud | Possible to enumerate valid files in password protected shares/files drop shar… | - |
| [INFO-2401648](https://hackerone.com/reports/2401648) | mozilla | two aws access key and secret key and database username and password exposed | - |
| [INFO-2404415](https://hackerone.com/reports/2404415) | security | View any user email using the Team's audit log section | - |
| [INFO-2412983](https://hackerone.com/reports/2412983) | mozilla | sentry Auth Token exposed publicly in docker hub image | - |
| [INFO-2828263](https://hackerone.com/reports/2828263) | ibb | Secrets not masked in UI when sensitive variables are set via Airflow cli | - |
| [INFO-2828271](https://hackerone.com/reports/2828271) | ibb | Apache Airflow: Sensitive Information Exposure in DAG Run Logs | - |

## 2. The two GitLab singulars: serialization and signed-param trust

INFO-509924 (**gitlab, $12,000**) is the module's crown — Quick Actions (`/move <project>`) serializes the full Project model of an inaccessible project into the notes response, including both runner tokens:

> The Quick Actions interpreter allows an attacker to reference a Project it does not have access to. The model attributes are then being serialized and returned to the user, which results in the Runner token (both encrypted and unencrypted) being returned to the user. This vulnerability is currently exploitable on GitLab.com.

> Write `/move <full path of any other project>` and click "Comment", a request to `/:namespace/:project/notes` is submitted

> This vulnerability gives any user who can create an Issue or comment on one the ability to obtain Runner tokens of Projects. This allows any user to register a runner for a project

The body prints `"runners_token"` and `"runners_token_encrypted"` from the live `gitlab.com` response. INFO-850447 (**gitlab, $10,000**) is its mirror — a file-read primitive that must be framed as disclosure because the read is *of other users' inflight uploads*:

> Using `[package]` as the field name causes the `@rewritten_fields` to contain:

> This could be done anywhere that accelerated uploads, eg the `UploadsController` or uploading a wiki file.

> * read unknown inflight files by using the symlinks in `/proc/PID/fd/XX` belonging to other users.

The two rows together teach the module's pricing rule: **a server-side file the attacker can fetch pays when the file belongs to someone else** (runner tokens of another project, another worker's temp file). The same primitive pointed at `allowed_paths` alone would be a traversal note; with `/proc/PID/fd` stealing it is a five-figure disclosure.

## 3. Buckets, feeds, and the password that isn't

INFO-1256375 (**shopify, $5,000**) is the feed-bypass anatomy: the HTML blog is password-gated (`401 error` at `/blogs/news.atom`), the *preview host* serves the atom feed unauthenticated:

> So without password we can't access the blog post atom feed at ```https://yourstore.myshopify.com/blogs/news.atom``` . But this can be bypass to access the atom feed of the blog posts.

> To bypass this try this link```https://dummytext2showpoc-store_id.shopifypreview.com/blogs/news.atom```.

> Disclosing atom feed of blog posts of password protected store

INFO-1021906 (**shopify, $2,900**) is the bucket twin — a Ping image URL (`https://ping-api-production.s3.us-west-2.amazonaws.com/oks██████`) whose bucket root lists "all images of other stores":

> Using this Bucket access, a hacker can steal all private images of other stores and the user who shared through Shopify Ping.

INFO-163476 (legalrobot, $0) is the negative control for the same shape — a publicly readable S3 directory listing the reporter *could not confirm* for write ("my personal AWS account is inactive") and which carries no figure. INFO-2244229 (**x, $1,500**) closes the section with the subtlest leak in the module: `twitter.com/sw.js` embeds `__INITIAL_STATE__` with the requestor's `userId`, and since SOP does not apply to `<script>` imports, any site can read the victim's ID:

> When requested with the cookie 'auth_token', the attribute '__INITIAL_STATE__ ' is populated in the following way:

> X users become precisely identifiable from any remote website.

## 4. Hardcoded secrets, CI logs, and dotfiles: the dump economy

INFO-124100 (**shopify, $1,500**) found Shopify's GitHub deploy password *inside the shipped iOS app* (`pod "SHPShareKit", git: "https://[REDACTED_CREDS]@github.com/Shopify/ios-share-kit"`), plus a second tier of "other private credentials" (Branch keys, Intercom, Mixpanel) —

> Podfile left inside application exposes GitHub Password for Shopify.

> Impact: Access to all source code of all programs Shopify makes, which would not be good :)

INFO-2915647 (**mozilla, $1,500**) is the CI-log version: a Netlify auth token in public Mozilla CI logs (`live.log`) with full Owner/Developer/Billing/Editor roles — "granting complete control over site management, deployments, billing, and content configurations." INFO-2467999 (**mozilla, $1,000**) is the Slack version (Jira Admin API keys in a `#███` channel, verified via `curl -u`). The dotfile singles form the floor: INFO-218465 (**x, $280**, `.git/logs/refs/heads/master` publicly accessible — "Publicly accessible GIT directory сan lead to leakage of source code and other private information"), INFO-147577 (**coinbase, $100**, an application error message that "may disclose sensitive information" and "the location of the file that produced the unhandled exception"), INFO-46366 ($0, error stack trace via a broken `wid` parameter), INFO-46345 ($0, directory index: "Directory index allowed in http://gateway.whisper.sh/"). INFO-1575014 (**stripe, $1,000**) is the module's path-normalization coda — `.`/`..` as an SDK identifier collapses a Retrieve into a List ("using `.` as checkout session id … leads to call [List all Checkout Sessions]"), returning PII unauthenticated:

> It is possible to use `.` and `..` as identifier in all API methods, which leads to calling the parent api method.

> The attacker can periodically call this method and grab PII, such as user's email address, name and address.

## 5. The unpriced tail: where hygiene findings live

Fifty-two rows carry no figure, and their titles are the module's checklist in miniature: `.git` and source-code downloads (INFO-248693, INFO-268382, INFO-211418), full-path disclosures (INFO-210572, INFO-1354334, INFO-158021), verbose errors and `phpinfo` (INFO-1762764), tokens in Docker images and GitHub repos (INFO-2412983, INFO-612231, INFO-396467), GPS metadata preserved through HEIF→PNG conversion (INFO-1069039), and log-file secrets (INFO-2101165 user passwords at debug level, INFO-2828271 Airflow DAG logs). The vault's playbook treats this tail as the *default hunt list* — these are the cheapest findings in the corpus to reproduce, and the absence of figures is a payout-publication artifact as much as a triage signal.

## 6. What pays, what doesn't

- **Pays at the top**: serialized tokens of *someone else's* project ($12,000), stolen inflight files of *someone else's* worker ($10,000), and password-gate bypasses with a live demonstration ($5,000). The multiplier is *another tenant's data*, reached by a *single request*.
- **Pays, floor**: dotfiles, indexes, and stack traces at $100–$500 — the cheapest reproducible findings in the vault. They pay when the file is real and fetchable (`.git` logs, `.htpasswd` via module 06, CI logs), and the price rises sharply when the leaked secret is *usable* (GitHub password $1,500, Netlify token $1,500, Jira keys $1,000).
- **Doesn't pay (here)**: the S3 *listing* the reporter could not fully verify (INFO-163476), and the 52 unpriced rows skew toward *potential* leaks ("might disclose", "possible to steal", "may be sensitive") — the P5 gate's "show the value" rule again.
- **The SDK-normalization exception**: INFO-1575014's `.`/`..` collapse paid $1,000 for what looks like a path trick, because the caller's sample-code frame made it a *reference-implementation* bug. Frame SDK bugs as such.

## 7. Cross-references

- Module 01 (`01_GraphQL-API-Objects-Exposure.md`) — INFO-509924 is the REST twin of the GraphQL serialization class; same fix (field-level authorization), different transport.
- Module 02 (`02_HackerOne-Reports-Bounty-Privacy.md`) — INFO-301526 (invitation token to `bat.bing.com`) and INFO-1491127 (invite links to Google Analytics) are this module's token-leak shape on the *analytics* vector; read together as "the leak is in the telemetry".
- Module 06 (`06_Adjacent-Disclosure-Noise.md`) — INFO-351555's Cloudinary secret and INFO-124100's Podfile password are the same "secret in shipped code" class; the adjacent module carries the bounty-less and unclassified side of it.
- Companion vault `../SSRF/` — INFO-850447's `/proc/PID/fd` file-steal is the disclosure face of a server-side read; input-validation there, exfil proof here.
