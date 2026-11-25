---
title: "CSRF case-register — 229 mirror-filtered rows: disposition ledger + bounty reconciliation"
type: case-register
built: "2026-10-28"
roster: 229 rows (h1.security.nathan.sx mirror, title-filter csrf|cross-site request|samesite|request forgery)
fetched: 178 report bodies (hackerone.com/reports/<id>.json, flat-format era export)
dead_404: 51 rows (recorded, never quoted, never reconstructed)
bounty_rule: JSON bounty_amount where present; else mirror list figure; labeled per row. 404 figures are list-stated only.
bounty_totals: JSON-verified $8,330 on 18 rows (incl. $50 SSRF-noise row CSRF-158016 — pure-CSRF $8,280/17); mirror-only on fetched CSRF-class rows $21,824 on 51 rows; dead-404 CSRF-class $6,400 on 20 rows; CSRF-class grand total $36,504. Noise rows (SSRF/SQLi/FPD by body or type) $3,000 excluded, shown separately.
---

# Case Register — CSRF

Case-ID scheme: `CSRF-<H1 report id>`. Every fetched body was read end-to-end. Classes are
mechanism-primary: 01 Login/Signup/Logout · 02 OAuth-State/Association · 03 ATO-Chains ·
04 Token-Design-Flaws · 05 Validation-Gaps/Bypasses · 06 GET-State-Changes · 07 Chains-Commerce ·
NOISE (adjacent, excluded from CSRF counts) · 404-dead.

## Ledger (sorted by report ID)

| Case-ID | Team | Bounty (src) | Class | Note |
|---|---|---|---|---|
| CSRF-547 | HackerOne ★ | $100 (list) | 01 Login/Signup/Logout | H1 self. Login CSRF via email-confirmation link -> victim logged into attacker fake account. |
| CSRF-1620 | Yahoo! | — | 404-dead |  |
| CSRF-2228 | Phabricator | $300 (list) | 02 OAuth-State/Association | Phabricator. Login CSRF via Twitter OAuth 1.0A flow, no state; related to #774. Attacker drops redirect, feeds victim attacker callback. |
| CSRF-2628 | Slack | $100 (list) | 04 Token-Design-Flaws | Slack. Crumb (anti-CSRF token) not expired after logout; username change possible. |
| CSRF-2635 | Slack | — | 05 Validation-Gaps/Bypasses |  |
| CSRF-2638 | Slack | — | 05 Validation-Gaps/Bypasses |  |
| CSRF-2857 | Phabricator | — | 04 Token-Design-Flaws |  |
| CSRF-2974 | OkCupid | — | 404-dead |  |
| CSRF-4461 | Yahoo! | $500 (list-404) | 404-dead |  |
| CSRF-5946 | HackerOne ★ | $100 (list) | 06 GET-State-Changes | H1 self. <img src=.../notifications/mark_as_read> GET state change. |
| CSRF-6378 | Khan Academy | — | 06 GET-State-Changes |  |
| CSRF-6700 | Yahoo! | $400 (list-404) | 404-dead |  |
| CSRF-6702 | Yahoo! | $200 (list-404) | 404-dead |  |
| CSRF-6871 | IRCCloud | $100 (json) | 01 Login/Signup/Logout |  |
| CSRF-6872 | IRCCloud | $100 (json) | 01 Login/Signup/Logout |  |
| CSRF-6888 | IRCCloud | — | 07 Chains-Commerce |  |
| CSRF-6910 | IRCCloud | $500 (list) | 03 ATO-Chains | IRCCloud. CSRF on /chat/user-settings email change -> password reset -> full ATO. |
| CSRF-7051 | IRCCloud | — | 01 Login/Signup/Logout |  |
| CSRF-7116 | IRCCloud | — | 03 ATO-Chains |  |
| CSRF-7332 | IRCCloud | — | 01 Login/Signup/Logout |  |
| CSRF-7436 | IRCCloud | — | 07 Chains-Commerce |  |
| CSRF-7516 | IRCCloud | — | 01 Login/Signup/Logout |  |
| CSRF-7531 | IRCCloud | $100 (list) | 01 Login/Signup/Logout | IRCCloud. Login-CSRF "protection" bypassed: auth-formtoken fetchable anonymously, attacker pre-fetches valid token. |
| CSRF-7608 | Yahoo! | $400 (list-404) | 404-dead |  |
| CSRF-7849 | Automattic | — | 07 Chains-Commerce |  |
| CSRF-7863 | Localize | — | 07 Chains-Commerce |  |
| CSRF-7865 | Localize | — | 01 Login/Signup/Logout |  |
| CSRF-7870 | Localize | — | 05 Validation-Gaps/Bypasses |  |
| CSRF-7916 | Localize | — | 05 Validation-Gaps/Bypasses |  |
| CSRF-7936 | Secret | — | 01 Login/Signup/Logout |  |
| CSRF-7962 | Localize | — | 05 Validation-Gaps/Bypasses |  |
| CSRF-8216 | Localize | — | 05 Validation-Gaps/Bypasses |  |
| CSRF-8218 | Localize | — | 05 Validation-Gaps/Bypasses |  |
| CSRF-8224 | Localize | — | 05 Validation-Gaps/Bypasses |  |
| CSRF-8226 | Localize | — | 05 Validation-Gaps/Bypasses |  |
| CSRF-8273 | Localize | — | 05 Validation-Gaps/Bypasses |  |
| CSRF-8767 | CloudFlare | — | 404-dead |  |
| CSRF-8806 | CloudFlare | — | 404-dead |  |
| CSRF-8843 | StopTheHacker | — | 07 Chains-Commerce |  |
| CSRF-8849 | CloudFlare | — | 404-dead |  |
| CSRF-8943 | CloudFlare | — | 404-dead |  |
| CSRF-9062 | Mail.Ru | — | 404-dead |  |
| CSRF-10563 | Coinbase | $100 (json) | 06 GET-State-Changes | Coinbase. set-as-primary via GET form (JSON $100). |
| CSRF-10829 | Coinbase | $100 (list) | 06 GET-State-Changes | Coinbase. set-as-primary GET, duplicate-class of 10563 (mirror $100). |
| CSRF-12034 | CloudFlare | — | 404-dead |  |
| CSRF-13555 | Factlink | — | 01 Login/Signup/Logout |  |
| CSRF-13583 | Factlink | — | 01 Login/Signup/Logout |  |
| CSRF-13639 | Factlink | — | 07 Chains-Commerce |  |
| CSRF-13705 | Automattic | — | 01 Login/Signup/Logout |  |
| CSRF-13856 | Twitter | — | 07 Chains-Commerce |  |
| CSRF-14494 | Mavenlink | — | 01 Login/Signup/Logout |  |
| CSRF-14702 | WePay | — | 404-dead |  |
| CSRF-14751 | WePay | — | 404-dead |  |
| CSRF-14883 | Twitter | — | 04 Token-Design-Flaws |  |
| CSRF-15412 | Coinbase | $1,000 (json) | 04 Token-Design-Flaws | Coinbase. CSRF token delivered over HTTP on docs page -> attacker on same network reads it, bypass complete. |
| CSRF-15454 | FanFootage | — | 05 Validation-Gaps/Bypasses |  |
| CSRF-17312 | Uzbey | — | 07 Chains-Commerce |  |
| CSRF-17900 | DC Compendium | — | 404-dead |  |
| CSRF-18507 | WePay | $150 (list-404) | 404-dead |  |
| CSRF-18698 | RelateIQ | $190 (list) | 03 ATO-Chains | Password reset request has no CSRF token (resubmitted POC for #18685). |
| CSRF-21069 | Mavenlink | $100 (list) | 01 Login/Signup/Logout | Mavenlink. Login CSRF with csrfmiddlewaretoken parameter removed entirely. |
| CSRF-23150 | Square | — | 404-dead |  |
| CSRF-25128 | Twitter | — | 07 Chains-Commerce |  |
| CSRF-25405 | WePay | — | 404-dead |  |
| CSRF-26647 | Django | $1,000 (list) | 04 Token-Design-Flaws | Django. GA __utmz cookie injection (cookie-setting XSS via utmcsr) overwrites CSRF referrer check; works on any Django site (Blackfan). |
| CSRF-26866 | WePay | $350 (list-404) | 404-dead |  |
| CSRF-30004 | Square | $500 (list-404) | 404-dead |  |
| CSRF-30011 | Square | $500 (list-404) | 404-dead |  |
| CSRF-30015 | Square | $250 (list-404) | 404-dead |  |
| CSRF-30142 | 99designs | — | 404-dead |  |
| CSRF-36980 | Twitter | — | 06 GET-State-Changes |  |
| CSRF-37301 | InVision | $150 (list-404) | 404-dead |  |
| CSRF-42728 | Ruby on Rails | — | 07 Chains-Commerce |  |
| CSRF-44146 | Vimeo | $1,000 (list) | 04 Token-Design-Flaws | Vimeo. API playground weak CSRF -> API calls on behalf of another user ($1,000). |
| CSRF-45050 | Informatica | — | 05 Validation-Gaps/Bypasses | Informatica community. pm-delete.jspa no referrer/token check -> trash victim messages. |
| CSRF-45428 | Vimeo | — | 05 Validation-Gaps/Bypasses | |
| CSRF-46736 | Romit | — | 04 Token-Design-Flaws |  |
| CSRF-47357 | Mobile Vikings | — | 04 Token-Design-Flaws | MobileVikings. X-CSRFToken from ANOTHER valid account accepted -> token not session-bound. |
| CSRF-49935 | Ruby on Rails | $1,000 (list) | 04 Token-Design-Flaws | Rails (GitHub, Ben Toews). rails-ujs sends CSRF tokens to other origins via data-remote links/forms; CSP-safe token theft. |
| CSRF-49974 | Romit | $50 (json) | 04 Token-Design-Flaws | Token unchanged after login; shared-workstation scenario ($50). |
| CSRF-50537 | Phabricator | — | NOISE-adjacent |  |
| CSRF-50703 | Ubiquiti Networks | $500 (list) | 01 Login/Signup/Logout | |
| CSRF-52635 | Ubiquiti Networks | $500 (list) | 05 Validation-Gaps/Bypasses | UniFi v3.2.10 (rcesecurity). Full 401->200 flow: referer check only; blank-referer iframe PoC changes admin password; enctype text/plain JSON smuggling. |
| CSRF-55911 | Shopify | $500 (json) | 02 OAuth-State/Association | Shopify Facebook store app. OAuth state parameter FIXED (same every authorization) -> attacker code+state links attacker FB account to victim store ($500). |
| CSRF-59660 | concrete5 | — | 07 Chains-Commerce |  |
| CSRF-64184 | concrete5 | — | 07 Chains-Commerce |  |
| CSRF-65167 | Legal Robot | $20 (list) | 07 Chains-Commerce |  |
| CSRF-65808 | concrete5 | — | 07 Chains-Commerce |  |
| CSRF-74595 | DigitalSellz | — | 06 GET-State-Changes |  |
| CSRF-76733 | Zaption | $25 (list) | 04 Token-Design-Flaws |  |
| CSRF-77065 | Keybase | $500 (list-404) | 404-dead |  |
| CSRF-83239 | ownCloud | — | 07 Chains-Commerce |  |
| CSRF-84372 | ownCloud | — | 03 ATO-Chains |  |
| CSRF-84395 | ownCloud | — | 03 ATO-Chains |  |
| CSRF-85565 | ownCloud | — | 07 Chains-Commerce |  |
| CSRF-86022 | Phabricator | $450 (list) | 05 Validation-Gaps/Bypasses | Phabricator. PHP loose-comparison type juggling on validateCSRFToken (== vs ===); sha1 0e... magic-hash reduction ($450). |
| CSRF-90165 | VK.com | $500 (json) | 03 ATO-Chains | ok.ru (RU). CSRF in backup-token retrieval + framing -> 2FA compromise ($500, body withheld in era; metadata-only here). |
| CSRF-91816 | Imgur | $1,600 (list) | NOISE-adjacent | NOISE. Body is SSRF in imgur vidgif url= param; mirror weakness column says CSRF — era mislabel, excluded from CSRF counts. |
| CSRF-93154 | Imgur | — | 06 GET-State-Changes |  |
| CSRF-95555 | Twitter | $280 (list) | 05 Validation-Gaps/Bypasses | Twitter. /i/cards/api/v1.json token check bypassed by dropping .json extension ($280). |
| CSRF-96470 | Shopify | $500 (json) | 06 GET-State-Changes | Shopify. export_installed_users via GET form, app id parameter ($500). |
| CSRF-99321 | Shopify | $500 (list) | 06 GET-State-Changes |  |
| CSRF-99647 | drchrono | $100 (list) | 05 Validation-Gaps/Bypasses |  |
| CSRF-99708 | HackerOne ★ | $500 (json) | 04 Token-Design-Flaws | H1. report_id path traversal (..%2F..%2F..%2F) makes page load /auth/slack/callback?...&asd=.json -> X-CSRF-Token leaks on GET; Slack oauth state not defeated ($500). |
| CSRF-99857 | drchrono | $100 (list) | 05 Validation-Gaps/Bypasses |  |
| CSRF-100820 | Twitter | $560 (list) | 05 Validation-Gaps/Bypasses | Curator collections POST, no token. |
| CSRF-101909 | Ubiquiti Networks | $200 (list) | 03 ATO-Chains |  |
| CSRF-102194 | Zendesk | $500 (list-404) | 404-dead |  |
| CSRF-102376 | ok.ru | $500 (list) | 05 Validation-Gaps/Bypasses | ok.ru (RU). st.rtu param open-redirect-ish path -> X-XTKN ajax CSRF (photo delete). |
| CSRF-103351 | Shopify | $500 (list) | 06 GET-State-Changes |  |
| CSRF-103787 | HackerOne ★ | $2,500 (json) | 04 Token-Design-Flaws | H1. SOP bypass/UXSS -> read token off /settings/profile/edit; tokens not per-action; _method PATCH/DELETE; cdn-cgi/trace framing gap ($2,500). |
| CSRF-104931 | Shopify | $500 (list) | 02 OAuth-State/Association | Shopify. Pinterest connect: attacker completes own OAuth, drops redirect, feeds victim the callback URL -> victim connected to attacker Pinterest ($500). |
| CSRF-109810 | Coinbase | — | 01 Login/Signup/Logout | "Create a New Account" signup CSRF. |
| CSRF-109839 | Udemy | $25 (list) | 07 Chains-Commerce |  |
| CSRF-110801 | Automattic | $250 (list) | 07 Chains-Commerce | WordPress. Press-This scan GET CSRF -> internal SSRF via 0.0.0.0/127.0.0.1 ($250). |
| CSRF-111216 | Shopify | $500 (list) | 06 GET-State-Changes | Shopify twitter-commerce. GET /auth/twitter/disconnect via <img> ($500). |
| CSRF-111218 | Shopify | $500 (list) | 02 OAuth-State/Association | Shopify pinterest-commerce. OAuth callback attach with no state ($500). |
| CSRF-111262 | ownCloud | — | 04 Token-Design-Flaws |  |
| CSRF-113857 | Zomato | — | 06 GET-State-Changes |  |
| CSRF-113865 | Zomato | — | 06 GET-State-Changes |  |
| CSRF-114127 | Zomato | — | 06 GET-State-Changes |  |
| CSRF-114430 | Shopify | $500 (json) | 06 GET-State-Changes | shopify.com/plus. insp_pingurln GET param -> page fires attacker-URL POST with analytics (info disclosure) ($500). |
| CSRF-115248 | Zomato | — | 07 Chains-Commerce |  |
| CSRF-115323 | Paragon Initiative Enterprises | — | 06 GET-State-Changes |  |
| CSRF-117195 | Gratipay | — | 01 Login/Signup/Logout |  |
| CSRF-118737 | ThisData | — | 02 OAuth-State/Association |  |
| CSRF-119148 | New Relic | — | 404-dead |  |
| CSRF-120143 | Veris | — | 05 Validation-Gaps/Bypasses |  |
| CSRF-123092 | New Relic | — | 404-dead |  |
| CSRF-123095 | New Relic | — | 404-dead |  |
| CSRF-123339 | LocalTapiola | $500 (list-404) | 404-dead |  |
| CSRF-123900 | Gratipay | — | 04 Token-Design-Flaws |  |
| CSRF-125594 | Uber ★ | — | 07 Chains-Commerce | Uber eng.uber.com. WP Fluid Responsive Slideshow plugin AJAX (frs_save) no nonce -> CSRF->stored JS->admin->theme/plugin editor->server-side compromise. |
| CSRF-127703 | Badoo | $852 (list) | 03 ATO-Chains | Badoo. rt param (CSRF-equivalent) leaked inside chrome-service-worker.js url_stats var -> link attacker gmail -> full ATO ($852, CRITICAL claim). |
| CSRF-129002 | LocalTapiola | $300 (list-404) | 404-dead |  |
| CSRF-131108 | Automattic | $75 (list) | 07 Chains-Commerce | Akismet. cancel account/subscription, add sites — all un-CSRF'd ($75). |
| CSRF-132049 | Zendesk | $500 (list-404) | 404-dead |  |
| CSRF-133847 | concrete5 | — | 07 Chains-Commerce |  |
| CSRF-134894 | Paragon Initiative Enterprises | — | 04 Token-Design-Flaws |  |
| CSRF-136481 | Vimeo | $750 (list) | 04 Token-Design-Flaws | Vimeo (opnsec). moogaloop.swf cross-site flashing + crossdomain.xml *.vimeocdn.com -> read XSRF token from 404 page -> make videos public ($750). |
| CSRF-137008 | Udemy | — | 07 Chains-Commerce |  |
| CSRF-137229 | Dropbox | — | 404-dead |  |
| CSRF-140275 | New Relic | — | 404-dead |  |
| CSRF-140377 | Gratipay | — | 04 Token-Design-Flaws |  |
| CSRF-141065 | drchrono | $100 (list) | 04 Token-Design-Flaws |  |
| CSRF-141344 | drchrono | $50 (list) | 03 ATO-Chains | onpatient. POST /api/v3/providers adds attacker email to providers list -> ATO ($50, CRITICAL claim). |
| CSRF-143321 | Veris | — | 05 Validation-Gaps/Bypasses |  |
| CSRF-144147 | Uber ★ | — | 07 Chains-Commerce |  |
| CSRF-145524 | Nextcloud | — | NOISE-adjacent |  |
| CSRF-145583 | Nextcloud | — | 07 Chains-Commerce |  |
| CSRF-148156 | Mail.Ru | — | 404-dead |  |
| CSRF-148417 | Instacart | — | 07 Chains-Commerce |  |
| CSRF-148517 | HackerOne ★ | — | 05 Validation-Gaps/Bypasses |  |
| CSRF-148890 | Paragon Initiative Enterprises | — | NOISE-adjacent |  |
| CSRF-149589 | WordPress | $1,337 (list) | 07 Chains-Commerce | WordPress. CSRF to add admin ($1,337; body not in JSON era export). |
| CSRF-150018 | Paragon Initiative Enterprises | — | NOISE-adjacent |  |
| CSRF-150586 | OLX | — | 404-dead |  |
| CSRF-151827 | Gratipay | — | 05 Validation-Gaps/Bypasses |  |
| CSRF-152013 | Rockstar Games | $750 (list) | 07 Chains-Commerce | Rockstar. set.php age param POST CSRF -> stored XSS on get.php ($750). |
| CSRF-152052 | concrete5 | — | 03 ATO-Chains |  |
| CSRF-152569 | Harvest | $100 (list-404) | 404-dead |  |
| CSRF-152586 | Harvest | $250 (list-404) | 404-dead |  |
| CSRF-153580 | Ian Dunn | — | 07 Chains-Commerce |  |
| CSRF-155726 | Coinbase | — | 04 Token-Design-Flaws |  |
| CSRF-155774 | Slack | $500 (json) | 03 ATO-Chains | Slack. 2FA SMS add w/o crumb; attacker nc server relays scode=196206 back into victim verify form ($500). |
| CSRF-156992 | New Relic | — | 404-dead |  |
| CSRF-157270 | New Relic | — | 404-dead |  |
| CSRF-157956 | Instacart | $50 (list) | 06 GET-State-Changes |  |
| CSRF-157993 | Instacart | $100 (list) | 06 GET-State-Changes |  |
| CSRF-158016 | Instacart | $50 (json) | NOISE-adjacent | NOISE. Body is SSRF on list-image upload (list[remote_image_url]=http://127.0.0.1:21 leaked SSH banner); weakness column says Code Injection — excluded from CSRF counts. |
| CSRF-161408 | Mail.Ru | — | 404-dead |  |
| CSRF-163815 | Gratipay | — | 05 Validation-Gaps/Bypasses |  |
| CSRF-164546 | Harvest | $150 (list-404) | 404-dead |  |
| CSRF-165923 | Boozt Fashion AB | — | 404-dead |  |
| CSRF-166231 | Legal Robot | — | 07 Chains-Commerce |  |
| CSRF-171398 | HackerOne ★ | — | 02 OAuth-State/Association |  |
| CSRF-172707 | Udemy | — | 07 Chains-Commerce |  |
| CSRF-174228 | Gratipay | — | 04 Token-Design-Flaws |  |
| CSRF-174328 | Slack | $500 (json) | 06 GET-State-Changes |  |
| CSRF-174470 | HackerOne ★ | — | 05 Validation-Gaps/Bypasses |  |
| CSRF-177472 | Starbucks | $250 (list) | 07 Chains-Commerce |  |
| CSRF-177508 | Starbucks | $375 (list) | 07 Chains-Commerce |  |
| CSRF-177635 | Starbucks | $150 (list) | 07 Chains-Commerce |  |
| CSRF-177639 | Starbucks | $375 (list) | 07 Chains-Commerce |  |
| CSRF-178241 | Mail.Ru | — | 404-dead |  |
| CSRF-178384 | OLX | — | 404-dead |  |
| CSRF-178831 | Yelp | $500 (list) | 01 Login/Signup/Logout | Yelp. auto-api signup processes w/o cookies/tokens/UA; hidden-form account farming ($500). |
| CSRF-182487 | GitLab | — | 04 Token-Design-Flaws | GitLab. authenticity_token valid across accounts -> delete another user's account. |
| CSRF-188692 | Robinhood | — | 404-dead |  |
| CSRF-189648 | U.S. Dept Of Defense | — | NOISE-adjacent |  |
| CSRF-191601 | LocalTapiola | $1,350 (list-404) | 404-dead |  |
| CSRF-191608 | U.S. Dept Of Defense | — | 07 Chains-Commerce |  |
| CSRF-191831 | U.S. Dept Of Defense | — | 07 Chains-Commerce |  |
| CSRF-192131 | Badoo | $280 (json) | 03 ATO-Chains |  |
| CSRF-195156 | Shopify | $1,000 (list) | 05 Validation-Gaps/Bypasses | Shopify. API endpoints CSRF-able when user used HTTP-auth example URL; _method overrides PUT/PATCH/DELETE ($1,000). |
| CSRF-196458 | Shopify | $500 (list) | 04 Token-Design-Flaws | apps.shopify.com. Post-login redirect carries authenticity_token in URL -> attacker's GA Real-Time captures victim token ($500). |
| CSRF-196715 | Mail.Ru | — | 404-dead |  |
| CSRF-198470 | Starbucks | — | 07 Chains-Commerce |  |
| CSRF-200683 | LocalTapiola | $50 (list-404) | 404-dead |  |
| CSRF-202808 | U.S. Dept Of Defense | — | 07 Chains-Commerce |  |
| CSRF-206319 | Starbucks | $750 (list) | 07 Chains-Commerce | Teavana. GiftCert-AddToBasket persistent CSRF -> gift card permanently stuck in cart, credit-card option gone, account can never purchase (High). |
| CSRF-208734 | BrickFTP | $100 (list) | 05 Validation-Gaps/Bypasses |  |
| CSRF-215381 | Twitter | $2,520 (list) | 02 OAuth-State/Association | Twitter Periscope. OAuth authorize POST no token/origin check -> attacker app gains full API access; code exchanged -> broadcast tweet ($2,520). |
| CSRF-216161 | Udemy | — | 07 Chains-Commerce |  |
| CSRF-217555 | Maximum | $150 (list-404) | 404-dead |  |
| CSRF-221043 | Nextcloud | — | 01 Login/Signup/Logout | |
| CSRF-223329 | Weblate | — | 01 Login/Signup/Logout |  |
| CSRF-223333 | Weblate | — | 06 GET-State-Changes |  |
| CSRF-223345 | Weblate | — | 06 GET-State-Changes |  |
| CSRF-223367 | Weblate | — | 03 ATO-Chains | Cross-vault row: excluded from XXE as pure CSRF. Attacker's registration activation link, used by a logged-in victim, adds attacker's email as victim's secondary email + renames them (medium). |
| CSRF-225100 | Weblate | — | 02 OAuth-State/Association |  |
| CSRF-225653 | Weblate | — | 02 OAuth-State/Association |  |
| CSRF-226418 | HackerOne ★ | $500 (json) | 06 GET-State-Changes | H1. GET escalate-to-JIRA CSRF -> private report details exfil ($500). |
| CSRF-226612 | Mixmax | — | 07 Chains-Commerce |  |
| CSRF-229405 | Weblate | — | 06 GET-State-Changes |  |
| CSRF-229528 | Weblate | — | 01 Login/Signup/Logout |  |
| CSRF-230428 | Coinbase | — | 01 Login/Signup/Logout |  |
| CSRF-230436 | Coinbase | — | 01 Login/Signup/Logout |  |
| CSRF-230688 | VK.com | $100 (json) | 05 Validation-Gaps/Bypasses | VK (RU). CSRF on stream-key reset ($100, metadata-only body). |
| CSRF-230837 | Zomato | — | 06 GET-State-Changes |  |
| CSRF-230863 | Weblate | — | 06 GET-State-Changes |  |
| CSRF-239170 | Bumble | — | 06 GET-State-Changes |  |
| CSRF-244778 | WakaTime | — | 01 Login/Signup/Logout |  |
| CSRF-245346 | WakaTime | — | 06 GET-State-Changes |  |
| CSRF-249234 | Zomato | $50 (json) | 06 GET-State-Changes | Zomato. post_twitter_authenticate.php type=posttweet&message= -> tweet on victim Twitter ($50). |
| CSRF-250430 | Cuvva | — | 404-dead |  |
| CSRF-251918 | Unikrn | $40 (list) | 05 Validation-Gaps/Bypasses | pinion.gg. Flash + 307-redirect CSRF updates Ad Frequency % ($40). |
| CSRF-253128 | Rockstar Games | $600 (list) | 02 OAuth-State/Association | Rockstar SocialClub. CSRF steals private token (High; body not in era export). |
| CSRF-257237 | Udemy | — | 07 Chains-Commerce | "CSRF Token" — empty body, informative; era noise floor. |

## Sub-state mix (fetched 178)

Resolved 136 · Informative 33 · Not-applicable 7 · Duplicate 2.

## Noise rows (excluded from CSRF counts — bodies/types decide)

- CSRF-91816 (Imgur, mirror $1,600): body is **SSRF** in `/vidgif/url`; mirror weakness column says CSRF — era mislabel.
- CSRF-158016 (Instacart, $50): body is SSRF on list-image upload (`list[remote_image_url]=http://127.0.0.1:21` leaked SSH banner).
- CSRF-189648 (DoD, resolved): title is SSRF; weakness column SSRF. Title-only (no body in era export).
- CSRF-145524 (Nextcloud): body is SSRF via federation trusted-server curl.
- CSRF-191601 (LocalTapiola, $1,350 list-404): title is SQLi. Dead-404 anyway; kept out of CSRF counts.
- CSRF-148890 / CSRF-150018 (Paragonie airship): bodies are Full-Path-Disclosure **on CSRF-validation-failure** — adjacent, kept honest as FPD.
- CSRF-50537 (Phabricator): body is SSRF in meme-creation macro — adjacent.

## 404 rows (51) — recorded, never quoted, never reconstructed

1620, 2974, 4461, 6700, 6702, 7608, 8767, 8806, 8849, 8943, 9062, 12034, 14702, 14751, 17900, 18507, 23150, 25405, 26866, 30004, 30011, 30015, 30142, 37301, 77065, 102194, 119148, 123092, 123095, 123339, 129002, 132049, 137229, 140275, 148156, 150586, 152569, 152586, 156992, 157270, 161408, 164546, 165923, 178241, 178384, 188692, 191601, 196715, 200683, 217555, 250430. That is all 51 — the archive's `http-codes.txt` is the authority.

Notable dead rows by list figure: 191601 (LocalTapiola team, "SQL Injection on /webApp/sijoitustalousuk email-parameter ", $1,350); 4461 (Yahoo! team, "Server Side Request Forgery", $500); 30004 (Square team, "CSRF on adding clients", $500); 30011 (Square team, "square google calendar integration CSRF,https://squareup.c", $500); 77065 (Keybase team, "Stealing CSRF Tokens", $500); 102194 (Zendesk team, "[CRITICAL] CSRF leading to account take over", $500); 123339 (LocalTapiola team, "CSRF allows attacker to delete item from customer's &quot;", $500); 132049 (Zendesk team, "[HIGH RISK] CSRF could potentially delete a zendesk subdom", $500); 6700 (Yahoo! team, "CSRF Token missing on http://baseball.fantasysports.yahoo.", $400); 7608 (Yahoo! team, "invite1.us2.msg.vip.bf1.yahoo.com/ - CSRF/email disclosure", $400); 26866 (WePay team, "Critical : Account removing using CSRF attack", $350); 129002 (LocalTapiola team, "The PdfServlet-functionality used by the &quot;Tee vakuutu", $300). Figures are list-stated only; no body was ever retrieved for any of these.
