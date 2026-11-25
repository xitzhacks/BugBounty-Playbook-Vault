---
title: "Exposure, APIs, secrets, and config — the thing you can reach is the thing that's wrong"
type: playbook
category: exposure_api_secrets_config
cwe: "CWE-200, CWE-16, CWE-798"
source_count: 59
full_bodies_available: 59
corpus: "h1-brain disclosed_reports.db 3,673 rows (sha256 8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4); misconfig bucket (152 rows)"
list_accessed: "2026-11-07"
note: "59 rows / $14,521 (19 paid) — by far the vault's largest module. All 59 bodies substantive. The Tor row (MISCONF-115686) is a defensive code review, kept as a negative example. All blockquotes byte-true."
---

# Exposure, APIs, secrets, and config — the thing you can reach is the thing that's wrong

## 1. Overview

Fifty-nine rows, **$14,521/19 paid** — 56% of the entire vault's bounty in one module. The bucket's center of gravity is here because "Violation of Secure Design Principles" (119 bucket-wide) concentrates in this module (46 of 59), and because exposure is the one misconfig family with an *instant* proof (open the URL; read the config; call the API). The module's lanes: **exposed services and debug surfaces** (metrics servers, pprof, setup pages), **API authorization gaps** (visibility bypasses, IDORs, unverified mutations), **secrets and tokens in the wrong place** (JS bundles, URLs, memory, error pages), **trust-boundary miscalibrations** (postMessage, quarantine, origin checks), **account-layer mutations** (notifications that don't fire, tickets that bind to the wrong identity), and a long tail of design-principle drift. The money story is one row: a $6,300 exposed metrics server that does the work of this whole module by itself.

**Case-stock (59 rows / $14,521):**

| Case | Target | Mechanism | Bounty |
|---|---|---|---|
| [MISCONF-80990](https://hackerone.com/reports/80990) | ui | .idea directory web-accessible | - |
| [MISCONF-96662](https://hackerone.com/reports/96662) | bumble | crossdomain.xml too permissive (Flash) | - |
| [MISCONF-115686](https://hackerone.com/reports/115686) | torproject | Uninitialized memory over wire (Tor, defensive) | - |
| [MISCONF-117739](https://hackerone.com/reports/117739) | gratipay | Image-count limit ($1) | $1 |
| [MISCONF-128121](https://hackerone.com/reports/128121) | gratipay | Username restriction bug | - |
| [MISCONF-129773](https://hackerone.com/reports/129773) | security | Prior attachments reusable on new report | - |
| [MISCONF-161301](https://hackerone.com/reports/161301) | instacart | SVG stored as PNG → stored XSS | - |
| [MISCONF-163067](https://hackerone.com/reports/163067) | uber | Password theft (limited scenario) | - |
| [MISCONF-168476](https://hackerone.com/reports/168476) | snapchat | Incoming-email hijack (sc-cdn) | - |
| [MISCONF-172289](https://hackerone.com/reports/172289) | security | One-click integration grants attacker privileges ($500) | $500 |
| [MISCONF-172545](https://hackerone.com/reports/172545) | reverb | Unlisted product readable via API (IDOR) | - |
| [MISCONF-172780](https://hackerone.com/reports/172780) | starbucks | Stale Disqus shortname | - |
| [MISCONF-201529](https://hackerone.com/reports/201529) | ui | Unauth file upload (AirFibre) | - |
| [MISCONF-208480](https://hackerone.com/reports/208480) | lyst | Improper site config at subdomain ($100) | $100 |
| [MISCONF-209917](https://hackerone.com/reports/209917) | security | javascript:/mailto: allowed in JIRA settings | - |
| [MISCONF-211149](https://hackerone.com/reports/211149) | gratipay | Dangerous jQuery behavior | - |
| [MISCONF-215044](https://hackerone.com/reports/215044) | brave | replaceState via blob URL (Brave iOS) | - |
| [MISCONF-240083](https://hackerone.com/reports/240083) | security | Payout change sends no notification ($500) | $500 |
| [MISCONF-274541](https://hackerone.com/reports/274541) | paragonie | Invited user can remove author owner | - |
| [MISCONF-278095](https://hackerone.com/reports/278095) | security | Invalid Host on /redirect | - |
| [MISCONF-297181](https://hackerone.com/reports/297181) | security | referrer-policy ignored; full URL leaks ($500) | $500 |
| [MISCONF-374106](https://hackerone.com/reports/374106) | brave | Downloads missing quarantine attribute | - |
| [MISCONF-387279](https://hackerone.com/reports/387279) | shopify | postMessage origin check accepts badexample.com | - |
| [MISCONF-415272](https://hackerone.com/reports/415272) | slack | Desktop binary not PIE / no ASLR ($100) | $100 |
| [MISCONF-475098](https://hackerone.com/reports/475098) | gitlab | Username 'dashboard.html' shadows pages ($200) | $200 |
| [MISCONF-634488](https://hackerone.com/reports/634488) | omise | Session survives password change + logout | - |
| [MISCONF-661051](https://hackerone.com/reports/661051) | nextcloud | MAC salt ambiguity → silent overwrite (CVE-2020-8133) | - |
| [MISCONF-668439](https://hackerone.com/reports/668439) | bcm | Attachment download IDOR | - |
| [MISCONF-672623](https://hackerone.com/reports/672623) | nextcloud | Username/token disclosure, Android (CVE-2019-15611, $250) | $250 |
| [MISCONF-761480](https://hackerone.com/reports/761480) | nordsecurity | Plaintext password in process memory | - |
| [MISCONF-837328](https://hackerone.com/reports/837328) | quantopian | WebSocket form-update forces victim POST ($1,050) | $1,050 |
| [MISCONF-902733](https://hackerone.com/reports/902733) | curve | Waitlist API returns PII; email brute force | - |
| [MISCONF-906790](https://hackerone.com/reports/906790) | acronis | Unverified email change → File Sync takeover | - |
| [MISCONF-927661](https://hackerone.com/reports/927661) | zomato | Price manipulation (<1 rupee) | - |
| [MISCONF-928255](https://hackerone.com/reports/928255) | gitlab | Spoofed email to GDPR endpoint deletes account | - |
| [MISCONF-944025](https://hackerone.com/reports/944025) | ibb | File-quarantine bypass; .fileloc/.url exec (CVE-2020-6797/6402) | - |
| [MISCONF-961841](https://hackerone.com/reports/961841) | security | 'Country' change sends no notification | - |
| [MISCONF-968328](https://hackerone.com/reports/968328) | brave | WebTorrent reverse tabnabbing | - |
| [MISCONF-981824](https://hackerone.com/reports/981824) | basecamp | DNS allows mail on behalf of other customers | - |
| [MISCONF-1086781](https://hackerone.com/reports/1086781) | gitlab | API bypasses restricted visibility ($1,370) | $1,370 |
| [MISCONF-1187018](https://hackerone.com/reports/1187018) | sifchain | HackerOne program URL → Wix (unconnected) | - |
| [MISCONF-1188629](https://hackerone.com/reports/1188629) | sifchain | Homepage LinkedIn link capturable ($200) | $200 |
| [MISCONF-1194293](https://hackerone.com/reports/1194293) | sifchain | Telegram link wrong scheme on desktop | - |
| [MISCONF-1212853](https://hackerone.com/reports/1212853) | kubernetes | Broken DriveScale link hijack (GitHub Pages) | - |
| [MISCONF-1213181](https://hackerone.com/reports/1213181) | curl | Metalink leaks creds cleartext (CVE-2021-22923, $700) | $700 |
| [MISCONF-1239334](https://hackerone.com/reports/1239334) | urbancompany | Security-page link hijack (username claim) | - |
| [MISCONF-1258871](https://hackerone.com/reports/1258871) | shopify | Unauth Cortex + pprof exposed ($6,300) | $6,300 |
| [MISCONF-1357013](https://hackerone.com/reports/1357013) | mattermost | Crafted signup email; session/account takeover (CVE-2021-37862) | - |
| [MISCONF-1454002](https://hackerone.com/reports/1454002) | owncloud | Exported activity reads protected files ($50) | $50 |
| [MISCONF-1626205](https://hackerone.com/reports/1626205) | deptofdefense | Exposed setup-config.php → WP takeover/RCE ($1,000) | $1,000 |
| [MISCONF-1781751](https://hackerone.com/reports/1781751) | nextcloud | Theming filename controllable + path leak (CVE-2023-28833) | - |
| [MISCONF-1784162](https://hackerone.com/reports/1784162) | nextcloud | OAuth code never expires (CVE-2024-22403, $100) | $100 |
| [MISCONF-1987680](https://hackerone.com/reports/1987680) | mozilla | VPN leaks traffic via local IPs | - |
| [MISCONF-2001913](https://hackerone.com/reports/2001913) | security | Email-to-ticket creates ticket on victim account ($1,000) | $1,000 |
| [MISCONF-2068830](https://hackerone.com/reports/2068830) | security | Unauth support ticket → delete request processed | - |
| [MISCONF-2129769](https://hackerone.com/reports/2129769) | fetlife | Mapbox access_token in frontend JS | - |
| [MISCONF-2166697](https://hackerone.com/reports/2166697) | security | GraphQL batching bulk-creates reports ($500) | $500 |
| [MISCONF-2501378](https://hackerone.com/reports/2501378) | brave | URL eliding wrong on Android (CVE-2024-37406, $100) | $100 |
| [MISCONF-2553026](https://hackerone.com/reports/2553026) | security | External-link warning no domain highlight (mobile) | - |

## 2. The crown row: an unauthenticated operations plane

MISCONF-1258871 (shopify, **$6,300**, 43% of the entire vault, the corpus's largest misconfig finding) is a Cortex metrics server exposed without authentication — and the report's four example URLs are the whole exploit:

> There is a Cortex metrics server running without authentication on https://cortex-ingest.shopifycloud.com/. This allows us to see the config for the server, call various Cortex APIs, and also exposes a Golang pprof debugger where we can see all the command-line arguments and DoS the server.

> * Cortex home: https://cortex-ingest.shopifycloud.com/
> * Cortex config: https://cortex-ingest.shopifycloud.com/config
> * Golang pprof home: https://cortex-ingest.shopifycloud.com/debug/pprof/
> * Golang pprof cmdline: https://cortex-ingest.shopifycloud.com/debug/pprof/cmdline?debug=1

> Information disclosure, no authentication

The doctrine generalizes: any *operations plane* (metrics, tracing, admin, setup) reachable without auth is priced as the operations plane, not as the web page it shares a domain with. MISCONF-1626205 (deptofdefense, **$1,000**) is the same doctrine one install-step earlier — an exposed `setup-config.php` lets the researcher host their own MySQL database server, complete the WordPress installation, and take the site to RCE (the body's phrase: "host their own MySQL database server and can successfully complete the"). MISCONF-96662 (bumble) is the Flash-era twin: a permissive `crossdomain.xml` lets an uploaded SWF read/update the logged-in user's data. MISCONF-80990 (ui) is the scanner twin of all three: `/.idea/workspace.xml` returns data-source credentials. The 2015–2025 lesson is unchanged; only the surface name rotates (.idea → pprof → setup-config → Actuator, see module 06's Spring Actuator queries).

## 3. API authorization gaps: the UI says no, the API says yes

- **Visibility bypass** — MISCONF-1086781 (gitlab, **$1,370**): a project-visibility restriction that the UI enforces ("restricted option") is bypassed by `PUT /api/v4/projects/27236` with `{"visibility": "internal"}` and a Bearer token. The body states the contract violation crisply: the API "should have the status code 403 if a restricted project visibility was selected."
- **Forced victim POST** — MISCONF-837328 (quantopian, **$1,050**): a WebSocket `form-update` event lets a collaborator overwrite the `#algo-id` element in the victim's page:

> Due to excessive control of victim's UI over algorithm collaboration feature one is able to force algorithm collaborator to issue malicious POST requests.

The victim's "Build Algorithm" button then POSTs to an attacker-chosen id.
- **Unverified mutation → takeover** — MISCONF-906790 (acronis): the name-change endpoint accepts an `email` field and changes the File Sync & Share identity without verification — the body's summary ends with the consequence:

> This allows user to pretend to be someone else. If the victim has not verified his email, the bug can allow attacker to take over his File Sync & Share account.

MISCONF-1357013 (mattermost, CVE-2021-37862) is the signup-link twin: a crafted `d=` parameter decouples the displayed email from the token-bound account, so the victim logs in with *your* email and you take back the account and check its chats.
- **IDOR tail** — MISCONF-172545 (reverb, unlisted product readable via `/api/listings/<id>/product_bundle`), MISCONF-668439 (bcm attachment download), MISCONF-275… none of these cleared a figure; the module teaches them as "compare UI gating to API gating" curriculum.
- **Identity-binding failures** — MISCONF-928255 (gitlab): a spoofed email to the GDPR endpoint deletes the account without interaction — the body's summary ends with the exact contract failure:

> Gitlab allows its user to exercise their GDPR rights (Right to Access/Delete) user data by sending an email to [REDACTED_EMAIL] however gitlab team doesn't ask for security question(i.e Date Of Birth) before deleting the user account moreover doesn't authenticate the incoming emails from their  instance which allows an attacker to delete user accounts without user interaction :

MISCONF-2001913 (security, **$1,000**): an email to `[REDACTED_EMAIL]` with the victim's address in `FROM` creates a ticket on the victim's support account, and the body's own words are:

> This would create a support ticket on victim's account , attacker can use this to create miscellaneous tickets on anyone's account or they can create ticket on behalf of **Hackerone** staff. You can check the ticket (441828) , I created this ticket by sending a fake email.

MISCONF-2068830 is its sibling (unauthenticated Freshdesk → account-deletion request *processed* by the agent). All three are "the email channel's From header is treated as identity" — file them together.

## 4. Secrets in the wrong place

- **Client-side secrets** — MISCONF-2129769 (fetlife): the Mapbox `access_token` shipped in frontend JS is reusable server-side ("I could freely use your token on my site, even though fetlife have `Referer: https://fetlife.com/`"). MISCONF-1213181 (curl, **$700**, CVE-2021-22923) is the transport edition: Metalink transfers leak `Authorization: Basic …` to different hosts over `http`/`ftp` — the body's phrase: "The credentials can be seen by the target host and anyone in man in the middle position:". (The trailing colon is the body's.)
- **Secrets in memory/URLs** — MISCONF-761480 (nordsecurity): the plaintext password sits in process memory and survives in crash dumps; MISCONF-672623 (nextcloud, **$250**, CVE-2019-15611): Android username + access-token disclosure; MISCONF-297181 (security, **$500**): the `referrer-policy` header is set ("bookmarked") but `www.hackerone.com` receives the full hacktivity URL — header discipline that fails only cross-host, exactly where passwords travel. MISCONF-661051 (nextcloud, CVE-2020-8133) is the cryptographic-control exhibit: an ambiguous `$passPhrase.$version.$position."a"` MAC salt means an attacker modifies block contents while the signature still verifies.
- **Never-provided vs wrongly-provided** — MISCONF-1784162 (nextcloud, **$100**, CVE-2024-22403): OAuth codes stored without timeout (“Your OAuth2 endpoint is not at all following best practices. When the authorization_code is generated it is stored without a timeout.”). MISCONF-387279 (shopify): the `postMessage` origin check accepts `badexample.com` for an app on `example.com` (suffix without boundary). MISCONF-374106 + MISCONF-944025: macOS quarantine not delegated to the OS — downloaded `.fileloc`/`.url` files execute arbitrary local files (CVE-2020-6797/6402).

## 5. Notifications, sessions, and the silent mutation

A misconfig cluster hiding in plain sight: **mutations that should notify but don't** — MISCONF-240083 (security, **$500**: payout-preference change sends no email), MISCONF-961841 (security, 'Country' change sends no notification), MISCONF-1781751 (nextcloud, theming `key` controllable → arbitrary filename + path disclosure). **Sessions that outlive their invalidation** — MISCONF-634488 (omise; the title carries the whole technique) pairs with module 02's MISCONF-194329. The doctrine: a secret-token lifecycle is only as strong as its *sinks* — the email notification is not UX polish; it is the victim's intrusion-detection channel.

## 6. Reachability as a family — broken links, sessions, and tokens

MISCONF-1187018 + MISCONF-1212853 + MISCONF-1239334 are module 01's mechanism restated for usernames and URLs: a HackerOne program page points at an unconnected Wix domain; a Kubernetes CSI page links to a claimed-on-GitHub `DriveScale` account; an Urban Company security page points at a 404 HackerOne username anyone can register (and the researcher registers it to prove the point). MISCONF-1188629 (sifchain, **$200**) seals it: a homepage LinkedIn link with no matching account "can be easily captured by someone else." The module's house rule: *any string the victim's browser follows to a namespace someone else can claim is a takeover primitive* — DNS (module 01), GitHub (here), social handle (here), package (module 01's S3 origin).

MISCONF-2166697 (security, **$500**) is the write-up to steal for rate-limit reports: GraphQL query batching creates ~75 reports per request, and with Turbo Intruder ~6,400 reports in ~40 seconds against an intended cap of 500. MISCONF-475098 (gitlab, **$200**) is this module's boundary case — "Issue shadowing" via a username literally named `dashboard.html` — filed here because the mechanism is a namespace/config quirk, and the module notes the boundary explicitly so nobody double-files it under business-logic.

## 7. What pays, what doesn't

- **Pays ($6,300–$50, 19 rows):** the module's top three (exposed operations plane $6,300; visibility bypass $1,370; forced-POST $1,050) are all *demonstrated* boundary crossings with a read-back (config, pprof cmdline, changed visibility, victim-forged POST). The $1,000 tier (setup-config takeover, email-to-ticket identity binding). The $500 tier (one-click privilege grant 172289, empty notification 240083, referrer disclosure 297181, GraphQL batching 2166697). The $50–$250 tail (Android token disclosure, LinkedIn capturable, OAuth no-timeout, URL eliding). The pattern: **price rises with the read-back's completeness.**
- **The negative example the module is built around** — MISCONF-115686 (torproject, 8,336 bytes): a meticulous defensive review (opening with the `tor_malloc`-to-`tor_calloc` replacement) with uninitialized-memory and heap-overflow theory, PoCs, and the honest admission:

> As for real exploitability, I spent some effort on creating a real, remote proof of concept for this, but because the data that write_escaped_data may process is the result a multitude of (to me) intricate processes it is hard to come up with a reliable attack.

No figure. It is the corpus's most thorough demonstration that *theory without a reachable effect* is catalogued as negative space, and its presence at the top of the module is deliberate.
- **Design-principle drift ($0 rows):** the 46 "Violation of Secure Design" rows carry mostly no figure — including some with real craft (postMessage suffix check, quarantine bypass, file-SVG stored XSS). The module teaches them as the next sweep's seed queue, not as priced precedent.

## 8. Cross-references

- Module 01 (§4, §5) — storage-origin and link takeovers (rubygems S3 origin, veneur.org) are this module's "unclaimed namespace" family with DNS-shaped clothing.
- Module 02 (§3) — unverified identity mutations (906790, 1357013) are the verification-skip family applied to profile endpoints.
- Module 03 (§4) — referrer-policy and CORS rows (297181 here; 235200/426165 there) are one "header set but unenforced" family split by bucket.
- Vault `20_Rate-Limiting/` cross-cite for 2166697 (batching caps) and module 02's ordering analysis; vault `16_Information-Disclosure/` for every PII-disclosure row in this module; vault `19_Cryptography/` for 661051 (MAC ambiguity) and 1784162 (token lifetimes).
- Playbook P1–P4 — exposure inventory, API shadow-diffing, secret-placement sweep, notification/session-lifecycle checks.
