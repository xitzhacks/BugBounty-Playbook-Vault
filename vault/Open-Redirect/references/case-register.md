---
title: "Open Redirect case register — 198-row ledger (129 fetched bodies + 69 dead-404 records)"
type: register
built: "2026-10-29"
roster: "h1.security.nathan.sx mirror (4,419 rows, frozen 2017-09-12), title-filter"
case_id_scheme: "RDIR-<HackerOne report id>"
bounty_rule: "JSON bounty_amount where present (labeled json) · otherwise mirror list figure (labeled list) · 404 rows recorded, never quoted, bounty mirrored as 404-list"
grand_total: "$46,891 roster-tagged across 92 rows ($16,070 json/26 + $24,163 list/42 + $6,658 dead-list/24) · pure redirect-class (01–07) $36,523 · adjacent+noise 08 $3,710"
---

# Case register — Open Redirect

Substate mix (129 fetched): 109 resolved · 15 informative · 3 duplicate · 2 not-applicable.
Class census: 01 core 50 · 02 OAuth/SSO 13 · 03 token/ATO chains 8 · 04 filter bypasses 19 · 05 host/referer 6 · 06 XSS chains 7 · 07 opener/tabnabbing 14 · 08 adjacent+noise 12 · dead 69.

| Case | Team | Substate | Bounty | Class | Note |
|---|---|---|---|---|---|
| [RDIR-2414](https://hackerone.com/reports/2414) | RelateIQ | informative | - | 01 | retURL on relateiq.com sign-up POST redirects anywhere (informative) |
| [RDIR-2575](https://hackerone.com/reports/2575) | Slack | resolved | $100 (list) | 02 | slack.com/oauth/authorize redirect_uri — suffix .mx / attacker-hosted suffix accepted ($100 list) |
| [RDIR-2622](https://hackerone.com/reports/2622) | Slack | resolved | $200 (list) | 01 | slack.com/checkcookie?redir=<full-url> redirects anywhere ($200 list) |
| [RDIR-2731](https://hackerone.com/reports/2731) | Slack | informative | - | 01 | sehacure.slack.com/link?url= redirects; phishing/malware impact claim (informative) |
| [RDIR-4549](https://hackerone.com/reports/4549) | Slack | informative | - | 01 | <sub>.slack.com/link?url= straight redirect (informative) |
| [RDIR-5199](https://hackerone.com/reports/5199) | Coinbase | informative | - | 05 | coinbase /cdn-cgi/l/chk_jschl Referer: attacker.com → redirect to attacker (informative) |
| [RDIR-6035](https://hackerone.com/reports/6035) | Slack | informative | - | 01 | slack.com/link?url= no validation (informative) |
| [RDIR-6357](https://hackerone.com/reports/6357) | Khan Academy | resolved | - | 01 | khanacademy login?continue= — single-slash http:/www.olivierbeg.nl passes filter |
| [RDIR-6564](https://hackerone.com/reports/6564) | Khan Academy | resolved | - | 01 | smarthistory.khanacademy player.swf link= param redirects on click |
| [RDIR-7357](https://hackerone.com/reports/7357) | IRCCloud | resolved | $100 (json) | 05 | irccloud invalid Host header → redirect to attacker domain ($100 JSON) |
| [RDIR-7900](https://hackerone.com/reports/7900) | Respondly | resolved | - | 02 | app.respond.ly/_oauth/twitter/?requestTokenAndRedirect= full control of post-auth redirect |
| [RDIR-12949](https://hackerone.com/reports/12949) | Urban Dictionary | resolved | - | 02 | urbandictionary auth/facebook?origin= → post-connect redirect; reporter claims auth-token capture |
| [RDIR-12964](https://hackerone.com/reports/12964) | Urban Dictionary | resolved | - | 01 | urbanup.php?hostname= unvalidated redirect |
| [RDIR-13553](https://hackerone.com/reports/13553) | Factlink | informative | - | 01 | staging.fct.li ?url= no whitelist (informative) |
| [RDIR-16718](https://hackerone.com/reports/16718) | Slack | resolved | $100 (json) | 01 | <sub>.slack.com/?redir=llink?url= login-then-redirect ($100 JSON) |
| [RDIR-22142](https://hackerone.com/reports/22142) | Automattic | resolved | - | 01 | WP Feed Statistics plugin ?feed-stats-url=<base64-url>; six live sites listed |
| [RDIR-23386](https://hackerone.com/reports/23386) | HackerOne | resolved | $500 (json) | 07 | hackerone target=_blank — window.opener.location.replace back-tab hijack ($500 JSON) |
| [RDIR-25160](https://hackerone.com/reports/25160) | Phabricator | resolved | $400 (list) | 03 | secure.phabricator.com redirect → Disqus access_token capture (Facebook not affected) ($400 list) |
| [RDIR-26962](https://hackerone.com/reports/26962) | The Internet | resolved | $3,000 (json) | 02 | rfc6749 §4.1.2.1 — wrong-scope error auto-redirects to registered redirect_uri → provider-wide redirector ($3,000 JSON) |
| [RDIR-27987](https://hackerone.com/reports/27987) | HackerOne | resolved | $500 (list) | 07 | hackerone profile website field — same opener hijack post-23386 ($500 list) |
| [RDIR-28865](https://hackerone.com/reports/28865) | HackerOne | resolved | $500 (json) | 04 | hackerone /redirect?signature=&url= — /../redirect/ bypasses link filter; /secure variant ($500 JSON) |
| [RDIR-29480](https://hackerone.com/reports/29480) | IRCCloud | resolved | $300 (json) | 08 | NOISE — IRC command injection via unvalidated channel names; no redirect mechanism (caught by unvalidated arm) ($300 JSON) |
| [RDIR-34084](https://hackerone.com/reports/34084) | Twitter | resolved | $420 (list) | 04 | t.co 301 extended-ascii padding — script preview ≠ script downloaded in terminal ($420 list) |
| [RDIR-39198](https://hackerone.com/reports/39198) | C2FO | resolved | - | 01 | admin.c2fo.com ///www.google.com/%2e%2e — dot-segment path redirect, Location echoed |
| [RDIR-39631](https://hackerone.com/reports/39631) | Twitter | resolved | $280 (json) | 01 | fabric.io/login?redirect_url=@google.com — @-authority trick on login redirect ($280 JSON) |
| [RDIR-42240](https://hackerone.com/reports/42240) | Flash | resolved | $1,000 (list) | 04 | Chrome + Flash: 307 redirect carries POST + custom headers cross-origin ($1,000 list; reported to Google) |
| [RDIR-44157](https://hackerone.com/reports/44157) | Vimeo | resolved | - | 04 | vimeo tools/edit?image= filter (must contain vimeocdn.com/ + end in image ext) satisfied by attacker URL |
| [RDIR-45516](https://hackerone.com/reports/45516) | Zaption | resolved | - | 01 | zaption.com ///www.google.com/%2f%2e%2e — 303 Location echo |
| [RDIR-46818](https://hackerone.com/reports/46818) | Twitter | resolved | $560 (json) | 07 | twitter card iframe <script>top.window.location.href= — parent-tab redirect ($560 JSON) |
| [RDIR-48516](https://hackerone.com/reports/48516) | Twitter | resolved | $1,400 (list) | 06 | twitter /intent/favorite original_referer unescaped when Referer is twitter.com — event-handler injection on fav dialog ($1,400 list) |
| [RDIR-49759](https://hackerone.com/reports/49759) | Twitter | resolved | $1,400 (json) | 03 | mobile.twitter.com/messages/follow?recipient=/example.com — POST carries authenticity_token off-site ($1,400 JSON) |
| [RDIR-50752](https://hackerone.com/reports/50752) | Twitter | resolved | $560 (json) | 03 | mobile.twitter.com//1572395042/messages — integer-IP host receives authenticity_token ($560 JSON) |
| [RDIR-51265](https://hackerone.com/reports/51265) | Flash | resolved | $2,000 (list) | 04 | Flash FileReference upload + open redirect 307/308 → cross-domain policy bypass, UPLOAD_COMPLETE_DATA read ($2,000 list; CVE-2015-0337) |
| [RDIR-52035](https://hackerone.com/reports/52035) | HackerOne | resolved | $500 (json) | 01 | hackerone.com//example.com/ru/faq — language-change dropdown redirects to //example.com ($500 JSON) |
| [RDIR-55525](https://hackerone.com/reports/55525) | Shopify | resolved | $500 (json) | 02 | myshopify /admin/oauth/authorize invalid_scope → redirects redirect_uri with error params ($500 JSON) |
| [RDIR-55546](https://hackerone.com/reports/55546) | Shopify | resolved | $500 (json) | 01 | ecommerce.shopify.com/accounts?return_to=.mx%2F — dot-suffix trick redirects to shopify.com.mx after login ($500 JSON) |
| [RDIR-56662](https://hackerone.com/reports/56662) | Shopify | informative | - | 06 | <shop>.myshopify.com/admin/redirects accepts javascript:/data: URIs as redirect targets (informative) |
| [RDIR-57163](https://hackerone.com/reports/57163) | HackerOne | resolved | $500 (list) | 01 | hackerone.com/%2F1572395042 — IP-integer host redirect; //hackerone.com works, //hackerone1.com filtered |
| [RDIR-63158](https://hackerone.com/reports/63158) | HackerOne | resolved | $500 (list) | 04 | markdown [test](/\x08/evil.com) — control char defeats renderer, browser treats //evil.com absolute ($500 list) |
| [RDIR-66994](https://hackerone.com/reports/66994) | Slack | informative | - | 08 | ADJACENT — %c2%ad soft hyphen splits visible link into two clickable targets (informative) |
| [RDIR-67929](https://hackerone.com/reports/67929) | HackerOne | resolved | - | 04 | external-link warning page throws error page instead of redirect (resolved) |
| [RDIR-76738](https://hackerone.com/reports/76738) | Zaption | resolved | $25 (list) | 04 | zaption logout?returnTo=///evil.com — Location echoed ($25 list) |
| [RDIR-77221](https://hackerone.com/reports/77221) | Mavenlink | resolved | $25 (list) | 01 | mavenlink logout?return_path=//google.com ($25 list) |
| [RDIR-91332](https://hackerone.com/reports/91332) | Imgur | informative | - | 02 | imgur register/thirdparty/facebook?redirect= (informative) |
| [RDIR-94637](https://hackerone.com/reports/94637) | Whisper | resolved | $30 (json) | 05 | whisper.sh Host: crowdshield.com → 301 Location https://crowdshield.com/ ($30 JSON) |
| [RDIR-95640](https://hackerone.com/reports/95640) | Udemy | informative | - | 06 | udemy JWPlayer setup params via URL → logo.link=//google.com.ua redirect or data: URI XSS (informative) |
| [RDIR-99435](https://hackerone.com/reports/99435) | Badoo | resolved | $153 (list) | 03 | badoo external/redirector.phtml?state=<b64 IE-suffix url> — FB #access_token lands off-site (IE11/Edge only) ($153 list) |
| [RDIR-101962](https://hackerone.com/reports/101962) | Shopify | resolved | $500 (list) | 01 | app.shopify.com theme-preview domain_name= → example.com/admin redirect (medium-ish) |
| [RDIR-103772](https://hackerone.com/reports/103772) | Shopify | resolved | $500 (list) | 01 | <shop>.myshopify.com/account/login?checkout_url=.np — dot-suffix → shop.np after login ($500 list) |
| [RDIR-104087](https://hackerone.com/reports/104087) | Slack | resolved | $1,000 (json) | 04 | slack svg upload → checkcookie?redir=<files-pri svg> — re-broke every fixed redirect ($1,000 JSON) |
| [RDIR-106348](https://hackerone.com/reports/106348) | Algolia | resolved | $100 (json) | 08 | ADJACENT — 404 page echoes attacker text ($100 JSON) |
| [RDIR-106350](https://hackerone.com/reports/106350) | withinsecurity | resolved | $250 (json) | 08 | ADJACENT — 404 page echoes attacker text ($250 JSON) |
| [RDIR-108113](https://hackerone.com/reports/108113) | Twitter | resolved | $2,520 (list) | 03 | digits login callback_url=https://[REDACTED_EMAIL] — %ff→? in Location after validation → OAuth credential takeover ($2,520 list) |
| [RDIR-111968](https://hackerone.com/reports/111968) | HackerOne | resolved | $500 (list) | 04 | hackerone.com/zendesk_session return_to→support /ping/redirect_to_account?state=compayn:/ — interstitial bypass ($500 list) |
| [RDIR-113112](https://hackerone.com/reports/113112) | Paragon Initiative Enterprises | resolved | $50 (list) | 01 | paragonie.com//google.com/ double-slash root redirect ($50 list) |
| [RDIR-114529](https://hackerone.com/reports/114529) | Mapbox | resolved | $200 (list) | 01 | mapbox studio forbidden/?message=&redirect= — message spoof + /evil.com redirect on Okay ($200 list) |
| [RDIR-119236](https://hackerone.com/reports/119236) | Uber | resolved | $500 (json) | 01 | uber.com//216.58.217.206/calendar — https breaks, plain http://uber.com//<ip>/ reaches site ($500 JSON) |
| [RDIR-123625](https://hackerone.com/reports/123625) | Informatica | resolved | - | 01 | marketplace.informatica.com ' quote-stripped by BigIP rewrite; Location built protocol-relative → //google.com (low) |
| [RDIR-124620](https://hackerone.com/reports/124620) | HackerOne | resolved | - | 07 | hackerone issue-tracker/CVE links missing rel=noopener — realistic cross-org scenario (resolved) |
| [RDIR-125000](https://hackerone.com/reports/125000) | Uber | resolved | $500 (json) | 01 | m.uber.com//youtube.com/%2F.. 303 ($500 JSON) |
| [RDIR-125791](https://hackerone.com/reports/125791) | Uber | resolved | $3,000 (json) | 01 | uber.com/en//example.com/ redirects ($3,000 JSON; title claims reflected XSS, body demonstrates redirect only) |
| [RDIR-126203](https://hackerone.com/reports/126203) | Uber | resolved | $500 (json) | 04 | pages.et.uber.com Redirect.aspx?EQ=<CBC blob> — encryptor oracle via ?uuid= → cut-and-paste → arbitrary redirect ($500 JSON) |
| [RDIR-129091](https://hackerone.com/reports/129091) | Automattic | resolved | $75 (list) | 01 | wp-login.php?redirect_to= external after login ($75 list; second finding: 99% CPU from huge post id) |
| [RDIR-131082](https://hackerone.com/reports/131082) | ownCloud | resolved | $150 (json) | 01 | owncloud files_pdfviewer?file=<any-url> — download button redirects unauthenticated users ($150 JSON) |
| [RDIR-131728](https://hackerone.com/reports/131728) | Moneybird | resolved | $50 (list) | 01 | moneybird login unvalidated redirect; team added same-origin validation ($50 list) |
| [RDIR-138786](https://hackerone.com/reports/138786) | Veris | resolved | - | 08 | ADJACENT — 404 page echoes attacker text (veris) |
| [RDIR-140432](https://hackerone.com/reports/140432) | Gratipay | resolved | $10 (list) | 03 | facebook dialog/oauth redirect_uri=https://gratipay.com/~attacka/ — token to profile page referrer ($10 list) |
| [RDIR-140447](https://hackerone.com/reports/140447) | Slack | resolved | $500 (json) | 04 | slack files.uploadAsync binary-char HTML served inline → checkcookie/files-pri redirect chain; phished login page hosted on slack.com ($500 JSON) |
| [RDIR-141355](https://hackerone.com/reports/141355) | Ubiquiti Networks | resolved | $260 (list) | 01 | unifi.ubnt.com Controller Finder open redirect ($260 list) |
| [RDIR-143240](https://hackerone.com/reports/143240) | Mapbox | resolved | $500 (list) | 06 | mapbox /authorize/?redirect_uri=<attacker JSON> → unescaped authorize_url in template-modal-oauth → XSS ($500 list) |
| [RDIR-143265](https://hackerone.com/reports/143265) | Zomato | informative | - | 01 | zomato redirect?u=<any>&t=<published token>&g=user-profile-website — token reusable by anyone (informative) |
| [RDIR-145306](https://hackerone.com/reports/145306) | Veris | resolved | - | 01 | sandbox.veris register sub_link= rewrites email-verification link host → code jacking |
| [RDIR-145392](https://hackerone.com/reports/145392) | Nextcloud | resolved | - | 04 | nextcloud redirect_url → PHP header( ) folds %0d%0a%09 per RFC1945 → IE strips tab → set-cookie injection |
| [RDIR-151831](https://hackerone.com/reports/151831) | Gratipay | duplicate | - | 08 | ADJACENT — gratipay profile-statement links not routed via redirect service (duplicate) |
| [RDIR-153652](https://hackerone.com/reports/153652) | Shopify | resolved | - | 01 | <shop>.myshopify.com/admin/auth/login?redirect=../pages/about-us → attacker store page |
| [RDIR-155222](https://hackerone.com/reports/155222) | Shopify | resolved | $500 (list) | 04 | ecommerce.shopify.com return_to=@evil.com — bypass after 55546 fix ($500 list) |
| [RDIR-157465](https://hackerone.com/reports/157465) | Gratipay | not-applicable | - | 05 | gratipay Host header injection report — not-applicable disposition |
| [RDIR-158019](https://hackerone.com/reports/158019) | Instacart | resolved | $150 (list) | 05 | instacart Host: google.com → 301 Location google.com ($150 list) |
| [RDIR-158148](https://hackerone.com/reports/158148) | Twitter | resolved | $560 (list) | 08 | ADJACENT — reverb.twitter.com → reverb.guru; reporter RCE’d the redirect target, phishing-download hosting ($560 list) |
| [RDIR-158434](https://hackerone.com/reports/158434) | Shopify | resolved | $1,000 (list) | 04 | supporthiring.shopify.com path=%2F%2F double-slash bypass; 404 page redirects after 2s ($1,000 list) |
| [RDIR-159522](https://hackerone.com/reports/159522) | Shopify | resolved | $500 (list) | 04 | checkout_url=https://checkout.shopify.com/<attacker store_id> → attacker store redirect ($500 list) |
| [RDIR-160047](https://hackerone.com/reports/160047) | Shopify | resolved | $500 (json) | 01 | apps.shopify.com//blackfan.ru/ 301 ($500 JSON) |
| [RDIR-160498](https://hackerone.com/reports/160498) | Coinbase | resolved | $300 (list) | 07 | coinbase opener cleared but Safari/WebKit still exposes window.opener.location → rel=noreferrer noopener fix ($300 list) |
| [RDIR-161991](https://hackerone.com/reports/161991) | Shopify | resolved | $500 (list) | 01 | shopify.com/admin/* redirect trusted last_shop cookie value → any domain ($500 list) |
| [RDIR-163124](https://hackerone.com/reports/163124) | Skyliner | duplicate | - | 01 | skyliner.io/qa.skyliner.io //blackfan.ru 301 (duplicate; CWE-601 cited) |
| [RDIR-163272](https://hackerone.com/reports/163272) | Khan Academy | resolved | - | 01 | teavana CS program image_url=<png> stored external redirect (medium) |
| [RDIR-165046](https://hackerone.com/reports/165046) | Shopify | resolved | $500 (list) | 04 | bypass of 159522 fix: return_url=checkout.shopify.com/<victim_id>/../<attacker_id> → theme-editor iframe content change ($500 list) |
| [RDIR-165136](https://hackerone.com/reports/165136) | Mapbox | informative | - | 07 | mapbox editor target=_blank — full control of visitor window object (informative) |
| [RDIR-169759](https://hackerone.com/reports/169759) | Shopify | resolved | $500 (list) | 01 | <shop>.myshopify.com/admin/bulk return_to=/..//evil.com ($500 list) |
| [RDIR-171398](https://hackerone.com/reports/171398) | HackerOne | resolved | - | 02 | hackerone SSO-SAML: auto-startable sign_in?email= redirect + login-CSRF + self-XSS chain (low) |
| [RDIR-172746](https://hackerone.com/reports/172746) | WebSummit | resolved | - | 01 | websummit/moneyconf/collision /gates POST referrer=<external> redirects |
| [RDIR-175085](https://hackerone.com/reports/175085) | Nextcloud | resolved | - | 07 | nextcloud mail app URI-scheme filter misses ftp/relative → content spoof + opener control + accountID leak |
| [RDIR-175168](https://hackerone.com/reports/175168) | Shopify | resolved | $500 (list) | 04 | ecommerce.shopify.com/auth/shopify return_to=/////example.com (low) |
| [RDIR-177624](https://hackerone.com/reports/177624) | Badoo | resolved | $140 (json) | 06 | team.badoo.com/%0d%0adata:text/html... — CRLF in Location → data: URI XSS ($140 JSON) |
| [RDIR-178278](https://hackerone.com/reports/178278) | Informatica | resolved | - | 06 | parc.informatica.com Cloud_chat?endpoint= javascript: or http://evil.com — runs after form complete (medium) |
| [RDIR-178345](https://hackerone.com/reports/178345) | HackerOne | resolved | - | 02 | hackerone.com/users//saml/sign_in?email= — double-slash path skips External Link Warning (low) |
| [RDIR-181088](https://hackerone.com/reports/181088) | Coinbase | resolved | $100 (json) | 07 | coinbase external_redirect — bloomberg http link manipulated same-network → opener hijack ($100 JSON) |
| [RDIR-181225](https://hackerone.com/reports/181225) | Paragon Initiative Enterprises | resolved | - | 07 | paragonie airship target=_blank links missing rel=noopener noreferrer (resolved) |
| [RDIR-186862](https://hackerone.com/reports/186862) | PortSwigger Web Security | informative | - | 08 | ADJACENT — portswigger CCPayment.aspx?id= GET-phishing order payment (informative) |
| [RDIR-187006](https://hackerone.com/reports/187006) | U.S. Dept Of Defense | resolved | - | 01 | DoD site open redirect (team summary) |
| [RDIR-187969](https://hackerone.com/reports/187969) | U.S. Dept Of Defense | resolved | - | 01 | DoD site open redirect #2 (team summary) |
| [RDIR-188266](https://hackerone.com/reports/188266) | Shopify | resolved | - | 01 | <shop>.myshopify admin/authorize_gateway return_url= redirects on Activate (app-install flow) |
| [RDIR-191196](https://hackerone.com/reports/191196) | Uber | resolved | $2,500 (list) | 08 | ADJACENT — G Suite authorization + misconfig → ubereats.com HTTP-redirect DoS ($2,500 list) |
| [RDIR-196846](https://hackerone.com/reports/196846) | Starbucks | resolved | $375 (list) | 06 | starbucks/teavana <>//google.com root + any-param payload; <>javascript: executes ($375 list) |
| [RDIR-203726](https://hackerone.com/reports/203726) | Greenhouse.io | resolved | $100 (list) | 01 | greenhouse job-app resume_url/cover_letter_url accept arbitrary URLs → hiring-manager download redirects anywhere ($100 list) |
| [RDIR-207170](https://hackerone.com/reports/207170) | Slack | resolved | $3,000 (list) | 03 | Slack call-popup redirect + weak postMessage → xoxs-token theft from malicious site ($3,000 list; team summary) |
| [RDIR-209821](https://hackerone.com/reports/209821) | Gratipay | informative | - | 08 | ADJACENT — profile-statement URLs lead to malicious sites; no redirect mechanism (informative) |
| [RDIR-210875](https://hackerone.com/reports/210875) | Rockstar Games | resolved | $300 (list) | 05 | rockstargames share endpoint builds rsg.ms short link from HTTP_HOST → poisoned redirect target ($300 list) |
| [RDIR-211065](https://hackerone.com/reports/211065) | GitLab | resolved | - | 07 | gitlab environments external-url button — reverse tabnabbing, 404-page + phish-login page scenario (low) |
| [RDIR-211213](https://hackerone.com/reports/211213) | Nextcloud | resolved | - | 01 | xmpp.nextcloud.com///;@www.google.com — triple-slash + ;@ authority trick |
| [RDIR-212629](https://hackerone.com/reports/212629) | GitLab | resolved | - | 07 | gitlab https://[REDACTED_EMAIL] — parser treats as internal, drops rel=noreferrer (medium) |
| [RDIR-213056](https://hackerone.com/reports/213056) | Nextcloud | resolved | - | 08 | ADJACENT — logs.nextcloud.com/redirect_uri 404 echoes path → content spoof for phishing |
| [RDIR-213114](https://hackerone.com/reports/213114) | GitLab | resolved | - | 07 | gitlab AsciiDoc [text^] produces target=_blank without rel (medium) |
| [RDIR-214034](https://hackerone.com/reports/214034) | GitLab | resolved | - | 01 | gitlab dashboard/todos?page&host= — redirect_to params.merge; also Projects::IssuesController |
| [RDIR-215970](https://hackerone.com/reports/215970) | GitLab | resolved | - | 01 | gitlab <user>/<repo>/import?continue[to]=//google.com (medium) |
| [RDIR-217430](https://hackerone.com/reports/217430) | Starbucks | resolved | - | 01 | connect.teavana.com/<campaign> third-party account → redirect to fake campaign (medium) |
| [RDIR-218705](https://hackerone.com/reports/218705) | HackerOne | resolved | - | 08 | ADJACENT — support doc forwards to unregistered @security-h1-forward.com domain (title caught by forward arm) |
| [RDIR-220737](https://hackerone.com/reports/220737) | Mavenlink | resolved | $50 (list) | 07 | mavenlink work-sample website field — opener.location.replace on public profile ($50 list) |
| [RDIR-223326](https://hackerone.com/reports/223326) | Weblate | resolved | - | 02 | weblate accounts/login/github/?next=///google.com after-auth redirect (medium) |
| [RDIR-223718](https://hackerone.com/reports/223718) | Weblate | duplicate | - | 02 | hosted.weblate.org all five social providers ?next=///evil.com (duplicate) |
| [RDIR-224317](https://hackerone.com/reports/224317) | Weblate | resolved | - | 02 | weblate accounts/disconnect/google-oauth2/<id>/?next= (medium) |
| [RDIR-226408](https://hackerone.com/reports/226408) | Shopify | resolved | - | 02 | shopify Amazon Alexa app callback shop= accepts any domain (low) |
| [RDIR-231760](https://hackerone.com/reports/231760) | Coinbase | not-applicable | - | 01 | video-only body; not-applicable |
| [RDIR-236599](https://hackerone.com/reports/236599) | ExpressionEngine | resolved | - | 04 | ExpressionEngine Redirect.php stristr(HTTP_REFERER,$host) — host substring anywhere in attacker referer passes (medium) |
| [RDIR-238117](https://hackerone.com/reports/238117) | Weblate | resolved | - | 02 | weblate accounts/disconnect/email/<id>/?next= |
| [RDIR-244958](https://hackerone.com/reports/244958) | WakaTime | resolved | - | 03 | wakatime oauth/twitter/authorize?next=<own profile> → OAuth token leak (low) |
| [RDIR-246897](https://hackerone.com/reports/246897) | Twitter | resolved | $420 (list) | 01 | t.lv.twimg.com live_video_stream &noredirect=true→false + url=<any> ($420 list) |
| [RDIR-258632](https://hackerone.com/reports/258632) | ownCloud | informative | - | 01 | owncloud.com open redirect (informative, body minimal) |
| [RDIR-260278](https://hackerone.com/reports/260278) | Legal Robot | resolved | $20 (list) | 07 | legalrobot-uat eff.org target=_blank no rel ($20 list) |

## Dead rows (404 — recorded, never quoted)

| Case | Team | Title (mirror) | List bounty |
|---|---|---|---|
| RDIR-210384 | Mail.Ru | Open Redirect | - |
| RDIR-219458 | Mail.Ru | Open Redirect | - |
| RDIR-219599 | Mail.Ru | Open Redirection at https://it.mail.ru/ | - |
| RDIR-243062 | arxius | Open redirects protection bypass | - |
| RDIR-244721 | Mail.Ru | Open Redirect on [My.com] | - |
| RDIR-252894 | Dropbox | Missing URL sanitization in comments can be leveraged for phishing | - |
| RDIR-14699 | WePay | Open Redirect | $300 (404-list) |
| RDIR-25334 | Square | Open Redirect [FreshBook] | $250 (404-list) |
| RDIR-29263 | Square | Redirect while opening link in new tabs | $250 (404-list) |
| RDIR-37593 | Sucuri | Open Redirect in unmask.sucuri.net | $250 (404-list) |
| RDIR-38157 | QIWI | [qiwi.com] Open Redirect | $150 (404-list) |
| RDIR-45513 | Trello | [trello.com] Open Redirect | $64 (404-list) |
| RDIR-1429 | Yahoo! | URL Redirection | - |
| RDIR-2126 | Yahoo! | Insufficient validation of redirect URL on login page allows hijacking user name | - |
| RDIR-2322 | Yahoo! | Yahoo open redirect using ad | - |
| RDIR-2989 | OkCupid | Login destination open redirection | - |
| RDIR-4521 | Yahoo! | Open URL Redirection | - |
| RDIR-4570 | Yahoo! | Open redirect on tw.money.yahoo.com | - |
| RDIR-7731 | Yahoo! | ads.yahoo.com Unvalidate open url redirection | - |
| RDIR-11209 | Meteor | Open Url Reditection After authentication | - |
| RDIR-15298 | Yahoo! | Open Redirect via Request-URI | - |
| RDIR-17902 | DC Compendium | Forward Secrecy is disable | - |
| RDIR-19948 | Coin.co | Host header is not Validated resulting in Redirect | - |
| RDIR-20661 | WePay | oauth redirect uri validation bug leads to open redirect and account compromise | - |
| RDIR-44739 | Dropbox | Unvalidated Redirects and Stored XSS | - |
| RDIR-46497 | Square | Redirecting a victim elsewhere through shopseen 0auth | - |
| RDIR-50379 | Adobe | Open redirect and reflected xss in http://youthvoices.adobe.com/community?return | - |
| RDIR-66384 | Envoy | [dashboard.signwithenvoy.com] Open Redirect | - |
| RDIR-87804 | Mail.Ru | [rabota.mail.ru] Open Redirect | - |
| RDIR-96474 | Mail.Ru | [it.mail.ru] Open Redirect | - |
| RDIR-112224 | Mail.Ru | Logical Vulnerability : REDIRECTING on pw.mail.ru by Parameter Spoofing | - |
| RDIR-113332 | Mail.Ru | [api.login.icq.net] Open Redirect | - |
| RDIR-115860 | New Relic | [login.newrelic.com] XSS via return_to | - |
| RDIR-116315 | New Relic | open redirection at login | - |
| RDIR-122054 | Xero | Open-redirect on login.xero.com | - |
| RDIR-123172 | New Relic | Open redirection on login | - |
| RDIR-127741 | New Relic | Open redirection bypass | - |
| RDIR-131552 | New Relic | Login Open Redirect | - |
| RDIR-132251 | New Relic | Open redirection | - |
| RDIR-144525 | New Relic | Open redirection bypass . | - |
| RDIR-148640 | Dropbox | XSS, Unvalidated redirects & phishing website hosting on dropbox servers | - |
| RDIR-158034 | Trello | XSS and Open-Redirect via SVG | - |
| RDIR-163707 | Dropbox | XSS in OAuth Redirect Url | - |
| RDIR-167107 | OLX | XSS and Open Redirect on https://jobs.dubizzle.com/ | - |
| RDIR-172363 | Trello | Unvalidated/Open Redirect allowing attackers to implement phishing attack | - |
| RDIR-172696 | itBit Exchange | Open Redirect in https://exchange.itbit.com - False Positive | - |
| RDIR-177485 | New Relic | Open Redirect | - |
| RDIR-181939 | Mail.Ru | [qpt.mail.ru] CRLF Injection / Open Redirect | - |
| RDIR-192373 | Mail.Ru | [cooking.lady.mail.ru] Open Redirect | - |
| RDIR-192375 | Mail.Ru | [ml.money.mail.ru] Open Redirect | - |
| RDIR-193027 | CloudFlare | [http2.cloudflare.com] Open Redirect | - |
| RDIR-87027 | Keybase | [keybase.io] Open Redirect | $500 (404-list) |
| RDIR-100200 | QIWI | Open Redirect in meeting.qiwi.com | $100 (404-list) |
| RDIR-104896 | Zopim | [status.zopim.com] Open Redirect | $100 (404-list) |
| RDIR-159275 | Starbucks | Improper Validation on Cancel Link Redirect | $150 (404-list) |
| RDIR-164895 | LocalTapiola | Open redirection protection bypass (/cs/Satellite) | $400 (404-list) |
| RDIR-179328 | LocalTapiola | Open Redirect (verkkopalvelu.lahitapiola.fi) | $400 (404-list) |
| RDIR-179568 | Open-Xchange | Tab nabbing via window.opener | $666 (404-list) |
| RDIR-179763 | LocalTapiola | Suspicious browser fingerprinting(?) scripts on http://www.lahitapiola.fi/ redir | $100 (404-list) |
| RDIR-183796 | LocalTapiola | XSS and open redirect in verkkopalvelu.lahitapiola.fi | $450 (404-list) |
| RDIR-190188 | LocalTapiola | Open Redirect bypass and cookie leakage on www.lahitapiola.com | $400 (404-list) |
| RDIR-191387 | LocalTapiola | Reflected XSS and Open Redirect in several parameters (viestinta.lahitapiola.fi) | $450 (404-list) |
| RDIR-194207 | LocalTapiola | Reflected XSS and Open Redirect (verkkopalvelu.lahitapiola.fi) | $400 (404-list) |
| RDIR-206811 | Robinhood | Open Redirect located at https://www.robinhood.com/oauth2/authorize/? | $100 (404-list) |
| RDIR-216806 | Pornhub | Reflected XSS in login redirection module | $250 (404-list) |
| RDIR-219215 | Harvest | Client can redirect payment, causing payment discrepancy between Harvest and Pay | $400 (404-list) |
| RDIR-239503 | Maximum | Open Redirect & Information Disclosure [mijn.werkenbijdefensie.nl] | $350 (404-list) |
| RDIR-242314 | Maximum | Open redirect on https://werkenbijdefensie.nl/ | $50 (404-list) |
| RDIR-259151 | Trello | A CRLF injection into the redirect URL of https://trello.com/1/authorize can be  | $128 (404-list) |
