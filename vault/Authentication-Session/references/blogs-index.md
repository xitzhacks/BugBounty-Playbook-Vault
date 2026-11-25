---
title: "Authentication & Session blogs index — bibliography: zseano auth-flaw guides (byte-quoted), community writeup corpus (title-linked, curated 303 of 559), skill-cited modern cases"
type: bibliography
built: "2026-10-29"
byte_quoted_sources: 2 (zseano.medium.com posts, fetched via webfetch 2026-10-29; curl is Cloudflare-challenged on medium — audit source = fetched text, re-fetch spot-checked)
audit: "2026-10-29 zero-miss run: 264 blockquote probes across all 13 vault files — 262 exact-normalized matches, 2 matched only after whitespace-squash (Medium's line-break collapse removes spaces at list-item boundaries; character sequence otherwise identical)"
title_linked_sources: 303 curated of 559 raw matches (originating-class filter; archive-mirror duplicates dropped; generic impact-only titles dropped)
body_fetched_blog_sources: 2 ok · 0 failed
---

# Blogs Index — Authentication & Session

Quote rule (vault-wide): byte-true quotes only from sources actually fetched this build.
Everything else is title + link, marked `title-only`. Nothing below was written from memory.
Links are regenerated mechanically from the saved index, never hand-typed.

Curation rule for §2: kept entries whose **originating flaw** is authentication/session class;
entries whose originator is another class (XSS, CORS, IDOR, SQLi, smuggling, cache, takeover)
are dropped from the class sections — a representative set lives in §2.7 as chain bibliography.


## 1. Fetched and byte-quoted: two zseano auth-flaw guides

BugBountyHunter has **no** auth/session vulnerability-type page (taxonomy verified 2026-10-28 on
`/disclosed/` — types: access_control, apitesting, bugbounty_toolkit, code, command_injection,
csrf, fileuploads, idor, javascript_files, notetaking, open_redirect, sql, ssrf, token,
waybackmachine, xss, xxe). The §1 byte-quoted guides are therefore two fetched zseano posts.
Both are post-mirror era (Nov 2017 / Jun 2018) — bibliography, consistent with the era rule:
post-2017 cases never enter class counts.

### 1a. "How re-signing up for an account lead to account takeover" (Jun 26, 2018)

URL: `https://zseano.medium.com/how-re-signing-up-for-an-account-lead-to-account-takeover-3a63a628fd9f`

**The method, verbatim:**

> Tip: when testing a site you will be surprised at how many act different depending on user
> agent,device,language, session (logged in/out). When testing you should test from as many
> different angles as possible to check if anything is different / discover new endpoints.

> After signing up I will always simply re-visit the signup page because sometimes if it
> renders, entering another users email / changing some details can lead to unexpected results

> My first thought is: what happens if I re-visit this link? Sadly, it gave me a 404 error
> (tried on old session, still 404, figured token expired etc), however after submitting the
> form above again I visited the link again, except this time I tried it on a brand new
> session. The result: logged into my account without entering my password!

**The repo steps, verbatim:**

> Submit users' email you wish to takeover.
> Grab id in response
> Visit the /api/create url and…. we're in!

**The discipline, verbatim:**

> It is extremely easy to overlook such basic things, especially with so many different types
> of bugs to look for. Just take your time, understand your target, and understand what you're
> trying to achieve. Stick to one thing at a time.

Corpus pairing: the re-register/auto-login family — AUTH-245408 (Zomato email-only login),
AUTH-64946 (OAuth waitlist bypass), module 06 verification rows.

### 1b. "How signing up for an account with an @company.com email can have unexpected results" (Nov 15, 2017)

URL: `https://zseano.medium.com/how-signing-up-for-an-account-with-an-company-com-email-can-have-unexpected-results-7f1b700976f5`

**The flaw trigger, verbatim:**

> I don't know why but I just randomly thought, "This site doesn't require us to verify our
> account/email, so what would happen if our account email is *@organisation.com?". 2 minutes
> later, armed with a [REDACTED_EMAIL] account, I clicked "Claim".

**The pivot, verbatim:**

> I sat and stared at the screen and suddenly thought, "I wonder what will happen if we change
> our account email to one we control BEFORE pressing the submit button?" — So I did just that.

**The bypass of the email check, verbatim:**

> Then it hits me: I need to change my email BACK to [REDACTED_EMAIL] before clicking the
> link.

**The tldr, verbatim:**

> Signup using *@organisation.com email
> Click "Claim" on organisation.
> Change email to one we control & press submit.
> Change email back to *@organisation.com and click link.
> We're in! :)

**The related finding, verbatim:**

> A similar method was found by @securinti which enabled him to access internal communications
> on some companies via their helpdesk.

Corpus pairing: the auth.email-domains family — AUTH-2224 / AUTH-2233 (Phabricator),
AUTH-4795 (concrete5): register with a privileged-domain email without owning it. The zseano
post is the same identity-trust failure one era later.


## 2. Community writeup corpus (title-linked, curated)

Raw match pool: 559 writeups from the bugbountyhunting.com index (7,103 entries) matching the
auth-session arms. Curated to 303 by originating class. `title-only` throughout.

### 2.1 Core authentication bypass & login flaws

client-side auth enforcement, signup/re-register takeover, login-as identity confusion, vendor CVE bypasses. 64 entries.

- [Auth bypass: Leaking Google Cloud service accounts and projects](https://www.ezequiel.tech/2020/08/leaking-google-cloud-projects.html)

- [Zero-day in Sign in with Apple](https://bhavukjain.com/blog/2020/05/30/zeroday-signin-with-apple/)

- [Touch ID Authentication Bypass on Evernote and Dropbox IOS Apps](https://medium.com/@pig.wig45/touch-id-authentication-bypass-on-evernote-and-dropbox-ios-apps-7985219767b2)

- [Got Bounty with Account takeover (ATO ) Unicode-Case Mapping Collision !](https://medium.com/cyberverse/got-bounty-with-account-takeover-ato-unicode-case-mapping-collision-d23a7785e1be)

- [OK Google: bypass the authentication!](https://techblog.mediaservice.net/2020/01/ok-google-bypass-the-authentication/)

- [User Account Takeover via Signup Feature | Bug Bounty POC](https://blog.securitybreached.org/2020/01/22/user-account-takeover-via-signup-feature-bug-bounty-poc/)

- [A simple post auth bypass leads to unauthorized web server access](https://medium.com/@heinthantzin/a-simple-post-auth-bypass-leads-to-unauthorized-web-server-access-483c053c110e)

- [Asus’S Admin Panel Auth Bypass](https://medium.com/@mustafakhan_89646/asuss-admin-panel-auth-bypass-af5062584ddf)

- [#BugBounty — “User Account Takeover-I just need your email id to login into your shopping portal account”](https://medium.com/@logicbomb_1/bugbounty-user-account-takeover-i-just-need-your-email-id-to-login-into-your-shopping-portal-7fd4fdd6dd56)

- [Authentication bypass in NodeJS application — a bug bounty story](https://medium.com/@_bl4de/authentication-bypass-in-nodejs-application-a-bug-bounty-story-d34960256402)

- [It’s all in the detail: Email leak & Account takeover thanks to WayBackMachine & extensive knowledge about the program](https://medium.com/@zseano/its-all-in-the-detail-email-leak-account-takeover-thanks-to-waybackmachine-extensive-4be365580dd7)

- [Symantec Messaging Gateway authentication bypass](https://artkond.com/2018/10/10/symantec-authentication-bypass/)

- [Bypassing Authentication Using Javascript Debugger.](https://mohitdabas.wordpress.com/2018/09/18/bypassing-authentication-using-javascript-debugger/)

- [Authentication bypass in Cisco Meraki](https://blog.takemyhand.xyz/2018/06/authentication-bypass-in-cisco-meraki.html)

- [How re-signing up for an account lead to account takeover](https://medium.com/@zseano/how-re-signing-up-for-an-account-lead-to-account-takeover-3a63a628fd9f)

- [My Best Small Report Bounty Report in Private Program ( Django REST framework Admin Login ByPass )](https://www.mohamedharon.com/2018/04/my-best-small-report-bounty-report-in.html)

- [From JS to another JS files lead to authentication bypass](https://c0rni3sm.blogspot.com/2017/06/from-js-to-another-js-files-lead-to.html)

- [Inspect Element leads to Stripe Account Lockout Authentication Bypass](https://www.jonbottarini.com/2017/04/03/inspect-element-leads-to-stripe-account-lockout-authentication-bypass/)

- [$500 for Cracking Invitation Code For Unauthorized Access & Account Takeover](https://infosecwriteups.com/500-for-cracking-invitation-code-for-unauthorized-access-account-takeover-558c663fb947)

- [Account Takeover via Broken Authentication Workflow: Free Lifetime Streaming!](https://www.praetorian.com/blog/account-takeover-via-broken-authentication-workflow-free-lifetime-streaming/)

- [How I Discovered Authentication Bypass That Blocks Users from Accessing the Website ?](https://sayedv2.medium.com/how-i-discovered-authentication-bypass-that-blocks-users-from-accessing-the-website-93140fa180ac)

- [CVE-2024-27198 and CVE-2024-27199: JetBrains TeamCity Multiple Authentication Bypass Vulnerabilities](https://www.rapid7.com/blog/post/2024/03/04/etr-cve-2024-27198-and-cve-2024-27199-jetbrains-teamcity-multiple-authentication-bypass-vulnerabilities-fixed/)

- [Bypassing a login page and getting full admin access on an internal training platform](https://medium.com/@l_s_/bypassing-a-login-page-and-getting-full-admin-access-on-an-internal-training-platform-ff5abd88135e)

- [SSD Advisory – TP-LINK NCXXX Authentication Bypass](https://ssd-disclosure.com/ssd-advisory-tp-link-ncxxx-authentication-bypass/)

- [Auth Bypass Round Two](https://www.assetnote.io/resources/research/ivantis-pulse-connect-secure-auth-bypass-round-two)

- [CVE-2024-0204: Fortra GoAnywhere MFT Authentication Bypass Deep-Dive](https://www.horizon3.ai/cve-2024-0204-fortra-goanywhere-mft-authentication-bypass-deep-dive/)

- [High Signal Detection and Exploitation of Ivanti's Pulse Connect Secure Auth Bypass & RCE (CVE-2023-46805 & CVE-2024-21887)](https://www.assetnote.io/resources/research/high-signal-detection-and-exploitation-of-ivantis-pulse-connect-secure-auth-bypass-rce)

- [SonicWall WXA – Authentication Bypass and Remote Code Execution Vulnerability](https://www.praetorian.com/blog/sonicwall-wxa-authentication-bypass-and-rce-vulnerability/)

- [CVE-2023-4473 & CVE-2023-4474 - Authentication bypass and multiple blind OS command injection vulnerabilities in Zyxel’s NAS326 devices](https://bugprove.com/knowledge-hub/cve-2023-4473-and-cve-2023-4474-authentication-bypass-and-multiple-blind-os-command-injection-vulnerabilities-in-zyxel-s-nas-326-devices/)

- [Account takeover through register functionnality](https://web.archive.org/web/20240106050326/https://izn0u.github.io/2023/11/23/account-takeover-through-register-functionnality.html)

- [Customer account takeover in Shopify stores](https://ophionsecurity.com/blog/shopify-acount-takeover)

- [Cookieless DuoDrop: IIS Auth Bypass & App Pool Privesc in ASP.NET Framework (CVE-2023-36899 & CVE-2023-36560)](https://soroush.me/blog/2023/08/cookieless-duodrop-iis-auth-bypass-app-pool-privesc-in-asp-net-framework-cve-2023-36899/)

- [Bypass IIS Authorisation with this One Weird Trick - Three RCEs and Two Auth Bypasses in Sitecore 9.3](https://blog.assetnote.io/2023/05/10/sitecore-round-two/)

- [Clipchamp ( Microsoft Office Product) - Google IAP Authorization bypass allowed access to Internal Environment Leading to Zero Interaction Account takeover](https://blog.agilehunt.com/blogs/security/msrc-critical-google-iap-authorization-bypass-allows-access-to-internal-envirnment-leading-to-zero-interaction-account-takeover)

- [Authentication Bypass in Izanami Docker image 1.10.22 CVE-2023-22495](https://www.synacktiv.com/sites/default/files/2023-02/Synacktiv-Advisory-Izanami-CVE-2023-22495.pdf)

- [Bypassing authorization in Google Cloud Workstations \[Google VRP]](https://blog.stazot.com/auth-bypass-in-google-cloud-workstations/)

- [Authentication Bypass in Nexus manager (version 3.37.3–02)](https://sharanthehunter.medium.com/authentication-bypass-in-nexus-manager-version-3-37-3-02-712f0bdb2fb4)

- [23000$ for Authentication Bypass & File Upload & Arbitrary File Overwrite](https://medium.com/@h4x0r_dz/23000-for-authentication-bypass-file-upload-arbitrary-file-overwrite-2578b730a5f8)

- [FortiOS, FortiProxy, and FortiSwitchManager Authentication Bypass Technical Deep Dive (CVE-2022-40684)](https://www.horizon3.ai/fortios-fortiproxy-and-fortiswitchmanager-authentication-bypass-technical-deep-dive-cve-2022-40684)

- [Auth Bypass Via Exposed Credentials](https://crypt0g30rgy.github.io/post/AuthBypass)

- [Ability to login as google staff in Google Cloud Community](https://medium.com/@bhatiagaurav1211/ability-to-login-as-google-staff-in-google-cloud-community-57c45809de05)

- [Account Takeover via Response Manipulation](https://medium.com/@bughunt789/account-takeover-via-response-manipulation-96be568feb7e)

- [CVE-2022-1040 Sophos XG Firewall Authentication bypass](https://blog.viettelcybersecurity.com/cve-2022-1040-sophos-xg-firewall-authentication-bypass/)

- [External Authentication bypass in ingress-nginx](https://xvnpw.github.io/posts/external_authentication_bypass_in_ingress_nginx/)

- [CVE-2022-0540 - Authentication bypass in Seraph](https://blog.viettelcybersecurity.com/cve-2022-0540-authentication-bypass-in-seraph/)

- [Authentication bypass using root array](https://infosecwriteups.com/authentication-bypass-using-root-array-4a179242b9f7)

- [Auth Bypass in Google Assistant](https://feed.bugs.xdavidhu.me/bugs/0012)

- [Auth Bypass in com.google.android.googlequicksearchbox](https://feed.bugs.xdavidhu.me/bugs/0013)

- [Auth Bypass in ADOdb CVE-2021-3850](https://blog.sorcery.ie/posts/adodb_auth_bypass/)

- [ZohOwned :: A Critical Authentication Bypass on Zoho ManageEngine Desktop Central](https://srcincite.io/blog/2022/01/20/zohowned-a-critical-authentication-bypass-on-zoho-manageengine-desktop-central.html)

- [How I found the Authentication Bypass bug and Earn $$$$](https://medium.com/@thedarkwayg/bypass-authentication-1bfab09332fe)

- [Full account takeover through referral code.](https://hector0x.medium.com/broken-authentication-through-referral-code-25cd0e8bccc2)

- [Auth Bypass in Google Assistant](https://feed.bugs.xdavidhu.me/bugs/0011)

- [CVE-2021-43136 – FormaLMS – The evil default value that leads to Authentication Bypass](https://blog.hacktivesecurity.com/index.php/2021/10/05/cve-2021-43136-formalms-the-evil-default-value-that-leads-to-authentication-bypass/)

- [Improper phone number validation to account takeover](https://sheshasai.medium.com/improper-phone-number-validation-to-account-takeover-f8b78b08ed05)

- [SSD Advisory – NETGEAR D7000 Authentication Bypass](https://ssd-disclosure.com/ssd-advisory-netgear-d7000-authentication-bypass/)

- [Proxytoken: An Authentication Bypass In Microsoft Exchange Server](https://www.zerodayinitiative.com/blog/2021/8/30/proxytoken-an-authentication-bypass-in-microsoft-exchange-server)

- [Authentication Bypass | Easy P1 in 10 minutes](https://infosecwriteups.com/authentication-bypass-easy-p1-in-10-minutes-54d5a2093e54)

- [Auth Bypass in https://nearbydevices-pa.googleapis.com](https://feed.bugs.xdavidhu.me/bugs/0004)

- [Auth Bypass in Google Workspace Real Time Collaboration](https://feed.bugs.xdavidhu.me/bugs/0002)

- [Advisory: Cisco RV34X Series – Authentication Bypass and Remote Command Execution](https://onekey.com/blog/advisory-cisco-rv34x-authentication-bypass-remote-command-execution/)

- [Weird and very easy authentication bypass found with Google dorking](https://infosecwriteups.com/weird-and-very-easy-authentication-bypass-found-with-google-dorking-c13230a038ed)

- [Jira Auth Bypass bug in Google Acquisition (Apigee)](https://jayateerthag.medium.com/jira-authenticated-dashboard-access-in-google-acquisition-apigee-ff20cfe11d99)

- [Account Takeover - Smoking with ‘null’](https://shahjerry33.medium.com/account-takeover-smoking-with-null-e43df2c3bb41)

### 2.2 Session fixation, hijack & invalidation

logout non-invalidation, session theft, token lifecycle, password-change side effects. 19 entries.

- [\[Writeup]\[Bug Bounty]\[Instagram] Instagram Still Send New DMs and Video Calls to Device After Logout \[ID]\[EN]](https://fadhilthomas.github.io/facebook-white-hat-01/)

- [Broken session management leads to bypass 2FA and Permanent access to Facebook user’s](https://medium.com/@0xBarakat/broken-session-permanent-access-to-facebook-users-cfed68684113)

- [Session Expiration Bypass in Facebook Creator App](https://medium.com/@evilboyajay/session-expiration-bypass-in-facebook-creator-app-b4f65cc64ce4)

- [Yet Other Examples of Abusing CSRF in Logout](https://soroush.secproject.com/blog/2019/04/yet-other-examples-of-abusing-csrf-in-logout/) (logout-CSRF research — ../CSRF lane)

- [User Account Takeover \[Password Change]— Nice Catch!](https://medium.com/@rohitcoder/user-account-takeover-password-change-nice-catch-2293f4d272b2)

- [A simple Account takeover misusing JWT late expiration](https://obsidianterminal.blogspot.com/2019/03/a-simple-account-takeover-misusing-jwt.html)

- [OpenProject Session Management Security Vulnerability aka CVE-2017-11667](https://www.seekurity.com/blog/general/openproject-session-management-security-vulnerability/)

- [Vine Re-auth Bypass \[Twitter Bug Bounty]](https://ahussam.me/Vine-Reauth-Bypass/)

- [Forced SSO Session Fixation](https://infosecwriteups.com/forced-sso-session-fixation-5d3b457b79cb)

- [Securing the Computer Security Course: Discovering a Session Hijacking Vulnerability in EPFL's COM-301 Website](https://www.thomashouhou.com/post/vulnerability-in-epfl-computer-security-course)

- [Insecure Authentication Tokens leading to Account Takeover](https://www.vaadata.com/blog/insecure-authentication-tokens-leading-to-account-takeover/)

- [Simple Bugs 0x01: Password Changing to Account Takeover!](https://vitorfalcao.com/posts/simple-bugs/password-changing-to-ato/)

- [Cengage LTI Session Management Leakage](https://www.rapid7.com/blog/post/2022/12/20/cengage-lti-session-management-leakage/)

- [How I Gained Access To A Finance Company’s Accounts (Session Hijacking)](https://medium.com/@talhakarakumru/how-i-gained-access-to-a-finance-companys-accounts-session-hijacking-2c6c5d9d84bd)

- [The Underrated Bugs, Clickjacking, CSS Injection, Drag-Drop XSS, Cookie Bomb, Login+Logout CSRF…](https://medium.com/@renwa/the-underrated-bugs-clickjacking-css-injection-drag-drop-xss-cookie-bomb-login-logout-csrf-84307a98fffa) (clickjacking + login/logout-CSRF roundup — ../CSRF lane)

- [Pwning the portal: from database dump to session hijacking](https://www.bitcrack.net/pwning-the-portal-from-database-dump-to-session-hijacking/)

- [Pre-Auth RCE in Moodle Part II - Session Hijack in Moodle's Shibboleth](https://haxolot.com/posts/2022/moodle_pre_auth_shibboleth_rce_part2/)

- [Misconfiguration in Change-password Functionality Leads to Account Takeover](https://0x2m.medium.com/misconfiguration-in-change-password-functionality-leads-to-account-takeover-1314b5507abf)

- [You can’t stop me. MS Teams session hijacking and bypass](https://www.pentestpartners.com/security-blog/you-cant-stop-me-ms-teams-session-hijacking-and-bypass/)

### 2.3 2FA / OTP bypass

OTP brute force, factor bypass, 2FA state abuse, MFA implementation flaws. 77 entries.

- [How I By-pass the login page and 2FA authentication…..](https://medium.com/@merry6607/how-i-by-pass-the-login-page-and-2fa-authentication-3f33b06838c)

- [Account takeover by OTP bypass](https://medium.com/@bhavarth33/how-i-was-able-to-takeover-any-account-by-otp-bypass-bba698a725f)

- [Cracking the 2FA](https://medium.com/@rushikesh12gaikwad/cracking-the-2fa-215d24ccb29b)

- [Multi-factor Auth Bypass with Password Reset Function](https://vj0shii.info/multi-factor-auth-bypass-with-password-reset-function/)

- [Bypassing OTP via reset password](https://medium.com/bugbountywriteup/bypassing-otp-via-reset-password-f004a29020c)

- [How I bypassed 2fa in a 3 years old private program!](https://shivangx01b.github.io/2fa_bypass/)

- [Bypass 2FA like a Boss](https://medium.com/bugbountywriteup/bypass-2fa-like-a-boss-378787707ba)

- [From Recon to Bypassing MFA Implementation in OWA by Using EWS Misconfiguration](http://www.firstsight.me/2020/06/from-recon-to-bypassing-mfa-implementation-in-owa-by-using-ews-misconfiguration/)

- [Account Takeover via OTP Bruteforce (Apigee API)](https://medium.com/@vishnu0002/account-takeover-via-otp-bruteforce-apigee-api-9b5481c642df)

- [Story About OTP Bypass To Stored XSS](https://medium.com/@pallabjyoti218/story-about-otp-bypass-to-stored-xss-81bfd735c709)

- [My First Bug Bounty — 2 Factor Authentication Bypass](https://medium.com/@talatmehmood1995/my-first-bug-bounty-2-factor-authentication-bypass-b034812c8243)

- [Two Factor Authentication Bypass \[ $50 ]](https://medium.com/@aungpyaehackeronetester/two-factor-authentication-bypass-50-5b397e68cfed)

- [OTP Verification Bypass](https://medium.com/@rat010/otp-verification-bypass-ee17d68f8425)

- [OTP Bruteforce- Account Takeover](https://medium.com/@ranjitsinghnit/otp-bruteforce-account-takeover-faaac3d712a8)

- [OTP Bypass - Developer’s Check](https://medium.com/@shahjerry33/otp-bypass-developers-check-5786885d55c6)

- [2FA Bypass via Logical Rate Limiting Bypass](https://medium.com/@jeppe.b.weikop/2fa-bypass-via-logical-rate-limiting-bypass-25ae2a4e1835)

- [Bypass 2FA in a website](https://medium.com/sourav-sahana/bypass-2fa-in-a-website-d616eaead1e3)

- [Authentication Bypass](https://medium.com/@ultranoob/weird-and-simple-2fa-bypass-without-any-test-b869e09ac261)

- [BugBounty: How I Cracked 2FA (Two-Factor Authentication) with Simple Factor Brute-force !!! 😎](https://medium.com/clouddevops/bugbounty-how-i-cracked-2fa-two-factor-authentication-with-simple-factor-brute-force-a1c0f3a2f1b4)

- [How I was able to bypass OTP code requirement in Razer \[The story of a critical bug]](https://medium.com/bugbountywriteup/how-i-was-able-to-bypass-otp-token-requirement-in-razer-the-story-of-a-critical-bug-fc63a94ad572?)

- [OTP Manipulation](https://kishanchoudhary.com/OTP/otp_manipulation.html)

- [Instagram account is reactivated without entering 2FA ($500)](https://bugbountypoc.com/instagram-account-is-reactivated-without-entering-2fa/)

- [How to bypass a 2FA with a HTTP header](https://medium.com/@YumiSec/how-to-bypass-a-2fa-with-a-http-header-ce82f7927893)

- [How I hacked 40,000 user accounts of Microsoft using 2FA bypass(outlook.live.com)](https://medium.com/@goyalvartul/how-i-hacked-40-000-user-accounts-of-microsoft-using-2fa-bypass-outlook-live-com-13258785ec2f)

- [How I abused 2FA to maintain persistence after a password change (Google, Microsoft, Instagram, Cloudflare, etc)](https://medium.com/@lukeberner/how-i-abused-2fa-to-maintain-persistence-after-a-password-change-google-microsoft-instagram-7e3f455b71a1)

- [Yes I can see your OTP](https://medium.com/vulnerables/yes-i-can-see-your-otp-9334cd27f021)

- [Instagram Multi-factor authentication Bypass](https://medium.com/@vishnu0002/instagram-multi-factor-authentication-bypass-924d963325a1)

- [Bypass HackerOne 2FA requirement and reporter blacklist](https://medium.com/japzdivino/bypass-hackerone-2fa-requirement-and-reporter-blacklist-46d7959f1ee5)

- [\[Facebook Bug Bounty] How I was able to enumerate Instagram Accounts who had enabled 2FA (Two Step Verification) for additional protection](https://medium.com/@zk34911/facebook-bug-bounty-how-i-was-able-to-enumerate-instagram-accounts-who-had-enabled-2fa-two-step-fddba9e9741c)

- [How I bypassed State Bank of India OTP.](https://hackernoon.com/how-i-bypassed-state-bank-of-india-otp-f145469a9f1d)

- [Behind the Scenes: Discovering an OTP Leakage Bug in a Leading Broadband Services Website](https://infosecwriteups.com/behind-the-scenes-discovering-an-otp-leakage-bug-in-a-leading-broadband-services-website-480e0440394e)

- [When Certificates Fail: A Story of Bypassed MFA in Remote Access](https://edermi.github.io/post/2024/mfa_bypass_mtls/)

- [Instagram and Meta 2FA Bypass by Unprotected Backup Code Retrieval in Accounts Center](https://medium.com/@scriptshuva/instagram-and-meta-2fa-bypass-by-unprotected-backup-code-retrieval-in-accounts-center-c735ff650f10)

- [2FA Bypass - IDN Mischief](https://shahjerry33.medium.com/2fa-bypass-idn-mischief-157f06cb6904)

- [500$: MFA bypass By Race Condition](https://medium.com/@a13h1/500-mfa-bypass-by-race-condition-176421462902)

- [Tricky 2FA Bypass Leads to 4 digit Bounty $$$$](https://medium.com/@roohaa_n/tricky-2fa-bypass-leads-to-4-digit-bounty-3a148bc7d4a)

- [Bypass Two-Factor Authentication of Facebook Accounts ($25,300)](https://medium.com/@bazzounbassem/bypass-two-factor-authentication-of-facebook-accounts-25-300-7ae152d7836a)

- [Account Takeover via Custom OTP, No User Interaction Required!](https://bhavukjain.com/blog/2023/07/08/account-takeover-custom-otp/)

- [DOS attack possible on Reset 2FA feature of #Hackerone](https://medium.com/@lokesh.leads13/disallow-any-hackerone-user-permanent-access-to-his-her-own-hackerone-account-using-vulnerability-147ce9957692)

- [2FA Bypass Using Custom Cookie Parameter](https://medium.com/@sharp488/2fa-bypass-using-custom-cookie-parameter-cb270c8557d2)

- [Netflix — Bypassing Multi-Factor Authentication (MFA)](https://ltsirkov.medium.com/netflix-bypassing-multi-factor-authentication-mfa-53135c9d6d50)

- [Bypassing the 2FA /MFA — An Easy win](https://medium.com/@mehtashobhit98/bypassing-the-2fa-mfa-an-easy-win-9b059bf0ac75)

- [Mass Account takeover by bypassing 2 FA](https://z-sec.co/mass-account-takeover)

- [Two Factor Authentication Bypass On Facebook](https://medium.com/pentesternepal/two-factor-authentication-bypass-on-facebook-3f4ac3ea139c)

- [0 click Facebook Account Takeover and Two-Factor Authentication Bypass](https://medium.com/@yaala/account-takeover-and-two-factor-authentication-bypass-de56ed41d7f9)

- [OTP Leaking Through Cookie Leads to Account Takeover](https://ag3n7.medium.com/otp-leaking-through-cookie-leads-to-account-takeover-4fb96f255e2f)

- [2FA Enabled Accounts Can Bypass Authentication & Access Account After Deactivation](https://medium.com/@sharp488/2fa-enabled-accounts-can-bypass-authentication-access-account-after-deactivation-8276a586be82)

- [Access Any Owner Account without Authentication (Auth bypass + 2FA bypass)](https://medium.com/@sharp488/access-any-owner-account-without-authentication-auth-bypass-2fa-bypass-94d0d3ef0d9c)

- [Security and Privacy Failures in Popular 2FA Apps](https://www.usenix.org/system/files/sec23summer_198-gilsenan-prepub.pdf)

- [2FA Bypass due to information disclosure & Improper access control.](https://akashhamal0x01.medium.com/2fa-bypass-due-to-information-disclosure-improper-access-control-f9a5a8a4e0af)

- [My First And Second Bugs Are — 2FA Bypass](https://medium.com/@nireshpandian19/my-first-and-second-bugs-are-2fa-bypass-1f6fd823b467)

- [mfa bypass in private program, the abdulsec way](https://abdulsec.medium.com/mfa-bypass-in-private-program-the-abdulsec-way-f677fea209f7)

- [2FA Bypass Do Re Mi](https://medium.com/@ashlyn.lau_17206/2fa-bypass-do-re-mi-cfcfc3775d2e)

- [2FA Bypass via Google Identity & OAuth Login](https://medium.com/@sharp488/2fa-bypass-via-google-identity-oauth-login-6c991ac837af)

- [Chaining MFA-Enabled IAM Users with IAM Roles for Potential Privilege Escalation in AWS](https://www.praetorian.com/blog/stsgetsessiontoken-role-chaining-in-aws/)

- [2FA Bypass via Basic Authentication on private bug bounty program](https://medium.com/@sharp488/2fa-bypass-via-basic-authentication-on-private-bug-bounty-program-93bb457cd065)

- [2FA Bypass on private bug bounty program due to improper caching mechanism](https://medium.com/@sharp488/2fa-bypass-on-private-bug-bounty-program-due-to-improper-caching-mechanism-212c5912bd00)

- [2FA Bypass on private bug bounty program due to CSRF token misconfiguration](https://medium.com/@sharp488/2fa-bypass-on-private-bug-bounty-program-due-to-csrf-token-misconfiguration-5a9c82151a1)

- [Its all about 2fa bypass, or Account Takeover](https://medium.com/@anjaneyulukanakatla1996/its-all-about-2fa-bypass-or-account-takeover-f9521f0a03b5)

- [2FA Secret value disclosure leads to 2FA Bypass - Bug Bounty Writeup](https://www.cyberick.com/post/2fa-secret-value-disclosure-leads-to-2fa-bypass-bug-bounty-writeup)

- [How I could’ve bypassed the 2FA security of Instagram once again?](https://infosecwriteups.com/how-i-couldve-bypassed-the-2fa-security-of-instagram-once-again-43c05cc9b755)

- [A tale of 0-Click Account Takeover and 2FA Bypass.](https://infosecwriteups.com/a-tale-of-0-click-account-takeover-and-2fa-bypass-b369cd70e42f)

- [No Rate Limiting on OTP sending](https://medium.com/@noob_master/no-rate-limiting-on-otp-sending-39a3a9fc93f6)

- [2fa Bypass by changing Request method](https://medium.com/@arthbajpai277/2fa-bypass-by-changing-request-method-to-delete-500fd0ed12b8)

- [Mixed Messages: Busting Box’s MFA Methods](https://www.varonis.com/blog/box-mfa-bypass-sms)

- [2FA bypass by reading the documentation](https://noob3xploiter.medium.com/2fa-bypass-by-reading-the-documentation-3260a372d8a8)

- [How I earned $$$ by bypassing 2FA](https://medium.com/@mohamedtaha_42562/how-i-earned-by-bypassing-2fa-b5487942a86d)

- [Bypassing Box’s Time-based One-Time Password MFA](https://www.varonis.com/blog/box-mfa-bypass-totp/)

- [How I was able to revoke your Instagram 2FA](https://dhiyaneshgeek.github.io/web/security/2021/10/23/how-i-was-able-to-revoke-your-instagram-2fa/)

- [Pre-Denial Of Service (set-up 2FA on unverified account)](https://medium.com/@kalvik/pre-denial-of-service-set-up-2fa-on-unverified-account-8399af52ea2d)

- [Bypassing 2FA using OpenID Misconfiguration](https://youst.in/posts/bypassing-2fa-using-openid-misconfiguration/)

- [2FA Bypass via Forced Browsing](https://infosecwriteups.com/2fa-bypass-via-forced-browsing-9e511dfdb8df)

- [2FA Verification Bypass in Shapeshift \[shapeshift.com] (Write Up)](https://blog.evanricafort.com/2021/05/2fa-verification-bypass-in-shapeshift.html)

- [OTP brute-force via rate limit bypass](https://bilalabdulmuqeet.medium.com/brute-forcing-otp-via-bypassing-rate-limit-c5ee6b25c2a8)

- [Is Math.random() Safe? from missing rate limit to bypass 2fa and possible sqli](https://neroli.medium.com/is-math-random-safe-from-missing-rate-limit-to-bypass-2fa-and-possible-sqli-2a4ea66f82c5)

- [OTP Bypass Account Takeover to Admin Panel — Ft. Header Injection](https://logicbomb.medium.com/otp-bypass-account-takeover-to-admin-panel-ft-header-injection-16f2982a0136)

- [Abusing AirWatch MDM Services to Bypass MFA](https://emptynebuli.github.io/tooling/2020/12/11/aircross.html)

### 2.4 Password reset & verification tokens

reset poisoning, token leakage (Referer/X-Forwarded-Host), weak token design. 35 entries.

- [How I was able to take over any account via the Password Reset Functionality.](https://medium.com/@fatnassifiras45/how-i-was-able-to-take-over-any-account-via-the-password-reset-functionality-ef1659f8b481)

- [Password Reset Poisoning leading to Account Takeover](https://medium.com/@swapmaurya20/password-reset-poisoning-leading-to-account-takeover-f178f5f1de87)

- [Weak Cryptography in Password Reset to Full Account Takeover](https://medium.com/bugbountywriteup/weak-cryptography-in-password-reset-to-full-account-takeover-fc61c75b36b9)

- [User’s email disclosure via invalid password reset link \[$250]](https://medium.com/@godofdarkness.msf/users-email-disclosure-via-invalid-password-reset-link-250-c431ed46680e)

- [Password Reset Token Leak Via Referrer](https://medium.com/@shahjerry33/password-reset-token-leak-via-referrer-2e622500c2c1)

- [Account Takeover Through Password Reset Poisoning](https://medium.com/@vbharad/account-takeover-through-password-reset-poisoning-72989a8bb8ea)

- [Password Reset Vulnerability — Full Account takeover (Insecure Direct Object Reference)](https://medium.com/@protector47/password-reset-vulnerability-full-account-takeover-insecure-direct-object-reference-c4a9a3ea8268)

- [Password reset to full account takeover](https://medium.com/@hamzabet/password-reset-to-full-account-takeover-8a1e0a395987)

- [Full account Takeover via reset password function](https://medium.com/@khaled.hassan/full-account-takeover-via-reset-password-function-8b6ef15f346f)

- [How i HACKED admin account via password reset IDOR function of one private currency exchanger site](https://medium.com/@aayushpokhrel/how-i-hacked-admin-account-via-password-reset-idor-of-one-private-currency-exchanger-site-51723c7c8704)

- [Don’t Trust the Host Header for Sending Password Reset Emails](https://lightningsecurity.io/blog/host-header-injection/)

- [Account of the CEO Takeover via Password Reset | by Vlad](https://cristivlad.medium.com/account-of-the-ceo-takeover-via-password-reset-7e55c0175425)

- [Interesting Business Logic Error leads to Pre-Account Takeover via Verification bypass on GoogleVRP](https://medium.com/@jerryhackgather/interesting-business-logic-error-leads-to-pre-account-takeover-via-verification-bypass-on-googlevrp-d362f9469e3d)

- [Unlocking the Weak Spot: Exploiting Insecure Password Reset Tokens](https://sallam.gitbook.io/sec-88/bug-bounty/unlocking-the-weak-spot-exploiting-insecure-password-reset-tokens)

- [Secret Input Header leads to Password Reset Poisoning](https://medium.com/@mares.viktor/secret-input-header-leads-to-password-reset-poisoning-ad3081fd8488)

- [Understanding GitLab EE/CE Account TakeOver (CVE-2023-7028)](https://secops.group/understanding-gitlab-ee-ce-account-takeover-cve-2023-7028/)

- [Compromising Honda’s power equipment / marine / lawn & garden dealer eCommerce platform through a vulnerable password reset API](https://eaton-works.com/2023/06/06/honda-ecommerce-hack/)

- [Hunting For Password Reset Tokens By Spraying And Using HTTP Pipelining](https://www.trustwave.com/en-us/resources/blogs/spiderlabs-blog/hunting-for-password-reset-tokens-by-spraying-and-using-http-pipelining/)

- [Bypassing account lockout through password reset functionality](https://akashc99.medium.com/bypassing-account-lockout-through-password-reset-functionality-8ff5c256f380)

- [Ransacking your password reset tokens](https://positive.security/blog/ransack-data-exfiltration)

- [Android Application Forgot Password Token Leakage Leading to Account Takeover](https://medium.com/@cyberali/android-application-forgot-password-token-leakage-leading-to-account-takeover-8a0b28296531)

- [Admin account takeover via weird Password Reset Functionality](https://0xmahmoudjo0.medium.com/admin-account-takeover-via-weird-password-reset-functionality-166ce90b1e58)

- [Password Reset to Admin Access](https://medium.com/techiepedia/password-reset-to-admin-access-3b2a649bdc3)

- [\[$5K] Misconfigured Reset password that leads to Account Takeover (No user Interaction ATO)](https://medium.com/@noob.assassin/5k-misconfigured-reset-password-that-leads-to-account-takeover-no-user-interaction-ato-e6a36b8ef183)

- [Account Takeover (User + Admin) Via Password Reset](https://infosecwriteups.com/account-takeover-user-admin-via-password-reset-322b8020ea6)

- [You’ve Got (a Reset) Mail: A Security Analysis of Email-Based Password Reset Procedures](https://innotommy.com/You’ve%20Got%20%28a%20Reset%29%20Mail.pdf)

- [Pre-Account Takeover by Reversing a Weak Email Verification Token Algorithm](https://craighays.com/pre-account-takeover-by-reversing-a-weak-email-verification-token-algorithm/)

- [Trick to bypass rate limit of password reset functionality](https://4bdoz.medium.com/trick-to-bypass-rate-limit-of-password-reset-functionality-a9923d3d7c4b)

- [Joomla Password Reset Vulnerability And A Stored XSS For Full Compromise](https://fortbridge.co.uk/research/joomla-password-reset-vulnerability-and-stored-xss-for-full-compromise/)

- [Drupal Insecure Default Leads To Password Reset Poisoning](https://www.fortbridge.co.uk/research/drupal-insecure-default-leads-to-password-reset-poisoning/)

- [My Fourth Account takeover through password reset](https://seaman00o.medium.com/my-fourth-account-takeover-through-password-reset-28a36dfebaf)

- [Password reset code brute-force vulnerability in AWS Cognito](https://www.pentagrid.ch/de/blog/password-reset-code-brute-force-vulnerability-in-AWS-Cognito/)

- [Unauthenticated Account Takeover Through Forget Password](https://infosecwriteups.com/unauthenticated-account-takeover-through-forget-password-c120b4c1141d)

- [Account Takeover Via Reset Password Worth 2000$](https://ashutoshmishra00x0.medium.com/account-takeover-via-reset-password-worth-2000-de085851d81d)

- [Password Reset Token Leak via X-Forwarded-Host](https://saajan.bhujel.cyou/blog/web/2021-02-26-password-reset-token-leak-via-x-forwarded-host)

### 2.5 SSO / SAML / OAuth identity binding

redirect_uri/callback validation, token binding, SAML verification, IdP-surface research. 55 entries.

- [Pre-Account Takeover using OAuth Misconfiguration](https://vijetareigns.medium.com/pre-account-takeover-using-oauth-misconfiguration-ebd32b80f3d3)

- [Taking down the SSO, Account Takeover in the Websites of Kolesa due to Insecure JSONP Call](https://medium.com/bugbountywriteup/taking-down-the-sso-account-takeover-in-3-websites-of-kolesa-due-to-insecure-jsonp-call-facd79732e45)

- [Vulnerability – Account takeover using OAuth Misconfiguration](http://wisdomfreak.com/2020/05/account-takeover-using-oauth-misconfiguration/)

- [\[Case Study] OAuth Misconfiguration leads to Account Takeover](https://medium.com/@0xgaurang/case-study-oauth-misconfiguration-leads-to-account-takeover-d3621fe8308b)

- [BookMyShow account takeover using social login](https://medium.com/@madguyyy/bookmyshow-account-takeover-using-social-login-84178f116e42)

- [Story about Facebook Oauth Account Takeover](https://medium.com/@androgaming1912/story-about-facebook-oauth-account-takeover-6537ff32281b)

- [OAuth authentication bypass on Airbnb acquisition using 1-char Open Redirect](https://xpoc.pro/oauth-authentication-bypass-on-airbnb-acquisition-using-weird-1-char-open-redirect/)

- [Oauth Misconfiguration lead to complete account takeover](https://medium.com/@Jacksonkv22/oauth-misconfiguration-lead-to-complete-account-takeover-c8e4e89a96a)

- [Zero to Account Takeover: How I ‘Impersonated’ Someone Else Using Auth0](https://www.imperva.com/blog/2018/06/how-i-impersonated-someone-else-using-auth0/)

- [Account Takeover Due to Misconfigured Login with Facebook/Google](https://bhavukjain.com/blog/2017/12/20/facebook-google-login-misconfig/)

- [Slack SAML authentication bypass](https://blog.intothesymmetry.com/2017/10/slack-saml-authentication-bypass.html) (SAML-signature research; era 2017)

- [Road to (unauthenticated) recovery: downloading GitHub SSO bypass codes](https://ysx.me.uk/road-to-unauthenticated-recovery-downloading-github-saml-codes/)

- [Authentication bypass on Uber’s Single Sign-On via subdomain takeover](https://www.arneswinnen.net/2017/06/authentication-bypass-on-ubers-sso-via-subdomain-takeover/) (corpus lane: AUTH-219205 Uber chain)

- [Authentication bypass on Airbnb via OAuth tokens theft](https://www.arneswinnen.net/2017/06/authentication-bypass-on-airbnb-via-oauth-tokens-theft/)

- [Authentication bypass on Ubiquity’s Single Sign-On via subdomain takeover](https://www.arneswinnen.net/2016/11/authentication-bypass-on-sso-ubnt-com-via-subdomain-takeover-of-ping-ubnt-com/) (corpus lane: AUTH-172137 Ubiquiti chain)

- [Obtaining Login Tokens for an Outlook, Office or Azure Account](https://whitton.io/articles/obtaining-tokens-outlook-office-azure-account/)

- [Account Takeover via Access Token Leakage | by M’BAREK Imad](https://infosecwriteups.com/account-takeover-via-access-token-leakage-687276953408)

- [SAML Authentication Bypass Leading to Admin Panel Access](https://medium.com/@0x_xnum/saml-authentication-bypass-leading-to-admin-panel-access-24f23812ed76)

- [POST to XSS: Leveraging Pseudo Protocols to Gain JavaScript Evaluation in SSO Flows](https://security.lauritz-holtmann.de/post/sso-security-redirect-uri-iii/)

- [One Scheme to Rule Them All: OAuth Account Takeover](https://blog.ostorlab.co/one-scheme-to-rule-them-all.html)

- [Hijacking OAuth Code via Reverse Proxy for Account Takeover](https://blog.voorivex.team/hijacking-oauth-code-via-reverse-proxy-for-account-takeover)

- [crewjam/saml - IdP XSS Via Missing Binding Syntax Validation In ACS Location](https://doyensec.com/resources/Doyensec_SecurityAdvisory_crewjam_saml_Q32023.pdf)

- [nOAuth: Account Takeover via Microsoft Oauth](https://bibek-shah.medium.com/noauth-account-takeover-via-microsoft-oauth-cc653410b886)

- [SSO Gadgets II: Unauthenticated Client-Side Template Injection to Account Takeover using SSO Gadget Chain](https://security.lauritz-holtmann.de/post/csti-xss-sso-gadget-chain/)

- [Bypassing Okta SSO=> HTTPS/HTTP](https://rashahacks.com/bypassing-okta-sso-https-http/)

- [nOAuth: How Microsoft OAuth Misconfiguration Can Lead to Full Account Takeover](https://www.descope.com/blog/post/noauth)

- [AWS Identity Center (formerly known as AWS SSO): A Guide to Privilege Escalation and Identity and Access Management](https://www.cloudquery.io/blog/aws-priv-esc-identity-center)

- [Redash SAML Authentication Bypass](https://blog.calif.io/p/redash-saml-authentication-bypass)

- [Traveling with OAuth - Account Takeover on Booking.com](https://salt.security/blog/traveling-with-oauth-account-takeover-on-booking-com)

- [Bypassing SSO Authentication from the Login Without Password Feature Lead to Account Takeover](https://aidilarf.medium.com/bypassing-sso-authentication-from-the-login-without-password-feature-lead-to-account-takeover-d2322a33a208)

- [SSO Gadgets: Escalate (Self-)XSS to ATO](https://security.lauritz-holtmann.de/post/xss-ato-gadgets/)

- [Account takeover of Facebook/Oculus accounts due to First-Party access_token stealing](https://ysamm.com/?p=777)

- [CVE-2022-47966 SAML ShowStopper](https://blog.viettelcybersecurity.com/saml-show-stopper/)

- [Azure Active Directory Flaw Allowed SAML Persistence](https://www.secureworks.com/research/azure-active-directory-flaw-allowed-saml-persistence)

- [SyncJacking: Hard Matching Vulnerability Enables Azure AD Account Takeover](https://www.semperis.com/blog/syncjacking-azure-ad-account-takeover/)

- [Google SSO misconfiguration leading to Account Takeover](https://0x4kd.medium.com/google-sso-misconfiguration-leading-to-account-takeover-cf9bcf63e76e)

- [Amazon Cognito misconfiguration lead to account takeover](https://medium.com/@iknowhatodo/amazon-cognito-misconfiguration-lead-to-account-takeover-20694243ca40)

- [CVE-2022-25262 | JetBrains Hub single-click SAML response takeover](https://github.com/yuriisanin/CVE-2022-25262)

- [Bypass Apple Corp SSO on Apple Admin Panel](https://medium.com/@StealthyBugs/bypass-apple-corp-sso-on-apple-admin-panel-dbfb72c7e634)

- [Hacking AWS Cognito Misconfiguration to Zero Click Account Takeover](https://infosecwriteups.com/hacking-aws-cognito-misconfiguration-to-zero-click-account-takeover-36a209a0bd8a)

- [Facebook Oauth bypass](https://medium.com/@yaala/facebook-oauth-bypass-446a073e687d)

- [How I was able to take over accounts in websites deal with Github as an SSO provider](https://infosecwriteups.com/how-i-was-able-to-takeover-accounts-in-websites-deal-with-github-as-a-sso-provider-294290358e0c)

- [XXE in SAML SSO Writeup - Bug Bounty](https://www.cyberick.com/post/xxe-in-saml-sso-writeup-bug-bounty) (XXE originator — ../XXE lane)

- [The Story Of How I Bypass SSO Login](https://systemweakness.com/the-story-of-how-i-bypass-sso-login-6b93370196cf)

- [Flickr Account Takeover](https://security.lauritz-holtmann.de/advisories/flickr-account-takeover/)

- [Exploiting OAuth: Journey to Account Takeover](https://blog.dixitaditya.com/2021/11/19/account-takeover-chain.html)

- [Story of Account Takeover : Using Social Login with Mass Assignment Vulnerability to hack accounts !](https://kaif0x01.medium.com/story-of-account-takeover-using-social-login-with-mass-assignment-vulnerability-to-hack-accounts-21e4d5856f5e)

- [Oculus SSO “Account Linking” bug leads to account takeover on third party websites and inside VR Games/Apps](https://ysamm.com/?p=697)

- [Account takeover of Instagram accounts due to unrestricted permissions of third-party application’s generated tokens](https://ysamm.com/?p=684)

- [Facebook account takeover due to unsafe redirects after the OAuth flow](https://ysamm.com/?p=667)

- [Facebook account takeover due to a bypass of allowed callback URLs in the OAuth flow](https://ysamm.com/?p=646)

- [Stealing user passwords through a VPN’s SSO](https://blog.scrt.ch/2021/02/25/stealing-user-passwords-through-a-vpns-sso/)

- [OAuth Misconfiguration Leads to Full Account takeover](https://neroli.medium.com/oauth-misconfiguration-leads-to-full-account-takeover-22b032cb6732)

- [Oracle WebLogic - Multiple SAML Vulnerabilities (CVE-2018-2998/CVE-2018-2933)](https://pulsesecurity.co.nz/advisories/WebLogic-SAML-Vulnerabilities)

- [Duo Finds SAML Vulnerabilities Affecting Multiple Implementations](https://duo.com/blog/duo-finds-saml-vulnerabilities-affecting-multiple-implementations)

### 2.6 ATO chains from other classes (cross-vault bibliography)

originating flaw is XSS/CORS/IDOR/SQLi/smuggling/cache/host-header — impact reaches accounts; listed for chain craft, not class. 51 entries.

- [Chaining password reset link poisoning, IDOR, and information leakage to achieve account takeover at api.redacted.com](https://medium.com/bugbountywriteup/chaining-password-reset-link-poisoning-idor-account-information-leakage-to-achieve-account-bb5e0e400745)

- [GitHub Gist - Account takeover via open redirect - $10,000 Bounty](https://devcraft.io/2020/10/19/github-gist-account-takeover.html)

- [6k$ Worth Account Takeover via IDOR in Starbucks Singapore](http://www.kamilonurozkaleli.com/posts/starbucks-singapore-account-takeover/)

- [Watch your requests! Open redirect to a complete account takeover](https://ninetyn1ne.github.io/2020-10-05-open-redir-to-ato/)

- [Account Takeover via IDOR](https://blog.deteact.com/account-takeover-via-idor/)

- [Utilizing Lockdown: Blind Sqli leads to Account Takeover & Data Extraction](https://medium.com/@shakti.gtp/utilizing-lockdown-blind-sqli-leads-to-account-takeover-data-extraction-3705ce8bdb62)

- [From CRLF to Account Takeover](https://medium.com/@valeriyshevchenko/from-crlf-to-account-takeover-a94d7aa0d74e)

- [Account takeover CSRF Misconfiguration](http://wisdomfreak.com/2020/05/account-takeover-csrf-misconfiguration/)

- [SQL Injection Via Stopping the redirection to a login page](https://medium.com/@St00rm/sql-injection-via-stopping-the-redirection-to-a-login-page-52b0792d5592)

- [A Simple IDOR to Account Takeover](https://medium.com/@swapmaurya20/a-simple-idor-to-account-takeover-88b8a1d2ec24)

- [Chains on Chains!! Chaining several IDOR’s into Account Takeover(PART ONE)](https://medium.com/@masonhck357/chains-on-chains-chaining-several-idors-into-account-takeover-part-one-373627f2910f)

- [Full Account Takeover via Changing Email And Password of any User through API Parameters](https://medium.com/@adeshkolte/full-account-takeover-changing-email-and-password-of-any-user-through-api-parameters-3d527ab27240)

- [Account Takeover Using CSRF(json-based)](https://medium.com/@shub66452/account-takeover-using-csrf-json-based-a0e6efd1bffc)

- [IDOR — Account Takeover](https://medium.com/@saadahmedx/idor-account-takeover-1ff5a2d03b8b)

- [Account takeover using IDOR and the misleading case of error 403.](https://medium.com/bugbountywriteup/account-takeover-using-idor-and-the-misleading-case-of-error-403-cb42c96ea310)

- [My First CSRF to Account Takeover worth $750](https://medium.com/@nishantrustlingup/my-first-csrf-to-account-takeover-worth-750-1332641d4304)

- [Open-redirect to Account Takeover.](https://medium.com/@__rishabh__/open-redirect-to-account-takeover-e939006a9f24)

- [4x CSRFs Chained For Company Account Takeover](https://medium.com/a-bugz-life/4x-csrfs-chained-for-company-account-takeover-f9fada416986)

- [Facebook CSRF protection bypass which leads to Account Takeover](https://ysamm.com/?p=185)

- [Love Story Of A Account Takeover (Chaining Host Header Injection To Takeover Someones Account)](https://chainlover.blogspot.com/2018/11/love-story-of-account-takeover-chaining.html)

- [Lintern@ute Account Takeover via Cross site request forgery](https://medium.com/@adeshkolte/lintern-ute-account-takeover-via-csrf-adesh-kolte-307f7065ee74)

- [CSRF account takeover Explained Automated/Manual — Bug Bounty](https://medium.com/bugbountywriteup/csrf-account-takeover-explained-automated-manual-bug-bounty-447e4b96485b)

- [CSRF account takeover in a company worth 1B$](https://medium.com/bugbountywriteup/csrf-account-takeover-in-a-company-worth-1b-6e966813c262)

- [R-XSS -> CSRF bypass to account takeover/](https://nirmaldahal.com.np/r-xss-csrf-bypass-to-account-takeover/)

- [IDOR User Account Takeover By Connecting My Facebook Account with victims Account](https://blog.securitybreached.org/2018/09/16/idor-account-takeover-using-facebook/)

- [IDOR leads to account takeover](https://s0cket7.com/idor-account-takeover/)

- [Chaining Self XSS with UI Redressing is Leading to Session Hijacking (PWN users like a boss)](https://medium.com/bugbountywriteup/chaining-self-xss-with-ui-redressing-is-leading-to-session-hijacking-pwn-users-like-a-boss-efb46249cd14)

- [Facebook CSRF leading to full account takeover (fixed)](https://www.josipfranjkovic.com/blog/facebook-csrf-full-account-takeover)

- [Account Takeover via CSRF | by Hacking articles | Infosec Writeups](https://infosecwriteups.com/account-takeover-via-csrf-78add8c99526)

- [IDOR Vulnerability: A Journey to Full Account Takeover](https://awais0x01.medium.com/idor-vulnerability-a-journey-to-full-account-takeover-47c930139c27)

- [Self XSS + Login CSRF + OAuth = Account Takeover](https://medium.com/@l_s_/self-xss-login-csrf-oauth-account-takeover-6357f3395b49)

- [Race Condition Authentication Bypass leads to Full Account Takeover](https://medium.com/@keizobugbounty/race-condition-authentication-bypass-leads-to-full-account-takeover-6b5c9bc0a54d)

- [XSS to OAuth access token leak in office online which can be used to account takeover](https://gist.github.com/RenwaX23/0311842bb790ce98fe0cd8f41141fdf0)

- [HTTP Desync Attack (Request Smuggling) - Mass Account Takeover at a Cryptocurrency based asset and 121 other websites](https://github.com/AnkitCuriosity/Write-Ups/blob/main/HTTP%20Desync%20Attack%20(Request%20Smuggling).md)

- [Never underestimate the power of open redirect, a story of a full account takeover](https://www.bugbounty.info/2022/08/never-underestimate-power-of-open.html)

- [CSRF leads to Account Takeover | Samsung](https://bloggerrando.blogspot.com/2022/08/17-1.html)

- [UN United Nations Host Header Injection leads to any Full Account Takeover (ATO)](https://medium.com/@Bishoo97x/un-united-nations-host-header-injection-leads-to-any-full-account-takeover-ato-795bc9ebc670)

- [CRLF to Account takeover (chaining bugs)](https://medium.com/@moSec/crlf-to-account-takeover-chaining-bugs-21a25dfa1cdf)

- [CSRF leads to account takeover in Yahoo!](https://webs3c.com/t/csrf-leads-to-account-takeover-in-yahoo/93)

- [Account Takeover by Chaining Two IDORs](https://www.r29k.com/articles/bb/account-takeover-via-idors)

- [How an Open Redirection Leads to an Account Takeover?](https://infosecwriteups.com/how-an-open-redirection-leads-to-an-account-takeover-73ea883055d1)

- [Full Account Takeover via Open Redirection](https://medium.com/@vflexo/full-account-takeover-via-open-redirection-41c167db46)

- [IDOR vulnerability on invoice and weak password reset leads to account take over](https://medium.com/@damaidec/idor-vulnerability-on-invoice-and-weak-password-reset-leads-to-account-take-over-603b42143a8c)

- [Host Header Injection Lead To Account Takeovers](https://systemweakness.com/host-header-injection-lead-to-account-takeover-2f025a645d13)

- [thisclosed_#1 - Full Account Takeover of ANY user via Insecure Direct Object Reference (IDOR) on reset password functionality](https://blog.hckrt.com/blog/thisclosed_1/)

- [Massive Users Account Takeovers(Chaining Vulnerabilities to IDOR)😲](https://infosecwriteups.com/massive-users-account-takeovers-chaining-vulnerabilities-to-idor-ea4e1b6407d2)

- [chaining improper authentication to idor and no rate limit for mass account takeover](https://tox7cv3nom.github.io/2021/11/12/chaining-of-csrf-token-misconfiguration-and-no-rate-limit-leads-to-mass-account-takeover.html)

- [1st Bug Bounty WriteUp: Open Redirect To XSS on Login Page](https://nassimchami.medium.com/1st-bug-bounty-writeup-open-redirect-to-xss-on-login-page-313221da2879)

- [Chaining Open Redirect with XSS to Account Takeover](https://radianid.medium.com/chaining-open-redirect-with-xss-to-account-takeover-36acf218a6d5)

- [CSRF to Full Account Takeover](https://medium.com/@ashrafharb997/csrf-to-full-account-takeover-5196cef9d166)

- [How I chained P4 To P2 \[Open Redirection To Full Account Takeover]](https://medium.com/bugbountywriteup/how-i-chained-p4-to-p2-open-redirection-to-full-account-takeover-a28b09a94bf7)

### 2.7 Doctrine & research roundups

multi-bug surveys and method essays. 2 entries.

- [5 Ways to do Account Takeover in a Single Website](https://medium.com/@vasuyadav0786/5-ways-to-do-ato-in-a-single-website-cfe7e5da987e)

- [Exploits Explained: 5 Unusual Authentication Bypass Techniques](https://www.synack.com/blog/exploits-explained-5-unusual-authentication-bypass-techniques/)


## 3. Skill-cited modern cases (post-2017, bibliographic)

Modern hardening-era counterparts of the corpus lanes, cited by the hunt-auth-bypass /
hunt-mfa-bypass / hunt-session skills. URLs verified live this build (search-sourced or
mechanically derivable NVD links). Never counted in class totals.

- Jitsi Meet — Authentication Bypass via Token Forgery (JWT alg-confusion HS256 with public
  key as secret): https://github.com/jitsi/jitsi-meet/security/advisories/GHSA-45ff-37jm-xjfx
  (disclosed H1 report: https://hackerone.com/reports/1210502)
- Linktree — Account takeover, improper validation of JWT signature (expiration-date claim):
  https://hackerone.com/reports/1760403
- GitHub Enterprise — SAML XML signature wrapping / parser differential, CVE-2025-25291 &
  CVE-2025-25292: https://nvd.nist.gov/vuln/detail/CVE-2025-25291
- samlify — SAML signature stripping, CVE-2025-47949: https://nvd.nist.gov/vuln/detail/CVE-2025-47949
- Argo CD — token-audience confusion, CVE-2023-22482: https://nvd.nist.gov/vuln/detail/CVE-2023-22482
- jsonwebtoken (npm) — signature-verification bypass, default `none`/falsy secret,
  CVE-2022-23540: https://nvd.nist.gov/vuln/detail/CVE-2022-23540

## 4. Dropped from §2 (selection record)

~256 raw matches dropped: originating class is XSS/CORS/IDOR/SQLi/RCE/smuggling/cache/takeover
(kept only representatives in §2.7); ~40 generic "Account Takeover worth $X" titles with no
classifiable technique; web.archive.org mirrors of already-listed canonical links (31 pairs).
The full raw pool is saved at `archive/` level as `blog-raw-matches.json` in the build workspace.
