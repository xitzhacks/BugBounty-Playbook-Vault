---
title: "rate-limiting case register — 64-row ledger (h1-brain corpus)"
type: register
built: "2026-11-07"
corpus: "h1-brain disclosed_reports.db (3,673 rows; sha256 8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4)"
case_id_scheme: "RATE-<HackerOne report id>"
bounty_rule: "DB bounty_amount where present · '-' = no figure in DB (not evidence of non-payment)"
module_rule: "frozen in archive/classes.json"
---

# Case register — rate-limiting

Corpus: 64 rows · 28 with bounty figures · **$19,105**.

Module census: _adjacent 20 rows/10 paid/$10,715 · otp-2fa-reset-token 11 rows/5 paid/$1,740 · throttle-bypass-vectors 10 rows/5 paid/$4,770 · _adjacent_unclassified 6 rows/3 paid/$830 · login-password-gates 17 rows/5 paid/$1,050.

| Case | Program | Bounty | Module | CVE | Title |
|---|---|---|---|---|---|
| [RATE-49170](https://hackerone.com/reports/49170) | yelp | - | _adjacent | - | Information disclosure - emails disclosed in response > staging.seatme.u |
| [RATE-121696](https://hackerone.com/reports/121696) | slack | - | otp-2fa-reset-token | - | Bypass  two-factor authentication |
| [RATE-158157](https://hackerone.com/reports/158157) | instacart | - | otp-2fa-reset-token | - | shopper login_code's can be brute forced |
| [RATE-165727](https://hackerone.com/reports/165727) | slack | $500 | throttle-bypass-vectors | - | Rate-limit bypass |
| [RATE-174668](https://hackerone.com/reports/174668) | bumble | $140 | otp-2fa-reset-token | - | No rate-limit in SERVER_SECURITY_CHECK |
| [RATE-206653](https://hackerone.com/reports/206653) | automattic | - | _adjacent_unclassified | - | Captcha bypass for the most important function - At en.instagram-brand.c |
| [RATE-209008](https://hackerone.com/reports/209008) | automattic | - | _adjacent | - | Authentication Bypass - Chaining two vulnerabilities leads to account ta |
| [RATE-225897](https://hackerone.com/reports/225897) | dashlane | - | throttle-bypass-vectors | - | Throttling Bypass - ws1.dashlane.com |
| [RATE-257335](https://hackerone.com/reports/257335) | unikrn | $25 | _adjacent | - | ssh: unprivileged users may hijack due to backdated ssh version open por |
| [RATE-271533](https://hackerone.com/reports/271533) | instacart | $50 | otp-2fa-reset-token | - | Bruteforcing password reset tokens, could lead to account takeover |
| [RATE-272839](https://hackerone.com/reports/272839) | unikrn | $40 | _adjacent | - | Weak Session ID Implementation - No Session change on Password change |
| [RATE-275186](https://hackerone.com/reports/275186) | instacart | $150 | _adjacent_unclassified | - | Get all instacart emails - missing rate limit on /accounts/register |
| [RATE-332632](https://hackerone.com/reports/332632) | bohemia | - | otp-2fa-reset-token | - | (Possible) staff account takeover via reset token bruteforce at helpdesk |
| [RATE-385381](https://hackerone.com/reports/385381) | chaturbate | $500 | login-password-gates | - | Rate limit missing at room login |
| [RATE-410451](https://hackerone.com/reports/410451) | security | - | login-password-gates | - | User login page doesn't implement any form of rate limiting |
| [RATE-411364](https://hackerone.com/reports/411364) | hyperledger | - | login-password-gates | - | Brute Force of fabric-ca server admin account |
| [RATE-412526](https://hackerone.com/reports/412526) | chaturbate | - | login-password-gates | - | No rate limit in stats api token endpoint |
| [RATE-413505](https://hackerone.com/reports/413505) | chaturbate | - | login-password-gates | - | No rate limit in affiliate statsapi endpoint |
| [RATE-418145](https://hackerone.com/reports/418145) | chaturbate | - | _adjacent_unclassified | - | No rate limiting in changing room subject. |
| [RATE-418151](https://hackerone.com/reports/418151) | chaturbate | - | _adjacent_unclassified | - | No rate limiting in starting up a bot. |
| [RATE-507012](https://hackerone.com/reports/507012) | unikrn | - | throttle-bypass-vectors | - | bypass Claudflare access crm.mautic.com |
| [RATE-662218](https://hackerone.com/reports/662218) | nextcloud | $150 | _adjacent | CVE-2019-15620 | Talk - Leak of password-protected room name via already existent resourc |
| [RATE-708013](https://hackerone.com/reports/708013) | shopify | - | login-password-gates | - | StoreFront API allows for a brute force attack on customer login by not  |
| [RATE-744692](https://hackerone.com/reports/744692) | bumble | - | login-password-gates | - | The login of Hotor Not is Vulnerable to bruteforce. |
| [RATE-751604](https://hackerone.com/reports/751604) | nordsecurity | - | otp-2fa-reset-token | - | No Rate Limit On Forgot Password Page Of NordVPN |
| [RATE-766578](https://hackerone.com/reports/766578) | affirm | - | otp-2fa-reset-token | - | Absence of Token expiry leads to Unauthorized login Access |
| [RATE-783708](https://hackerone.com/reports/783708) | semrush | - | _adjacent | - | IDOR in semrush academy |
| [RATE-790854](https://hackerone.com/reports/790854) | x | - | login-password-gates | - | NO username used in authenthication to www.mopub.com leading to direct p |
| [RATE-807924](https://hackerone.com/reports/807924) | shopify | - | _adjacent | - | CSRF on connecting Paypal as Payment Provider |
| [RATE-819930](https://hackerone.com/reports/819930) | x | $420 | throttle-bypass-vectors | - | Ability to bruteforce mopub account’s password due to lack of rate limit |
| [RATE-827484](https://hackerone.com/reports/827484) | acronis | - | login-password-gates | - | Missing rate limit for current password field (Password Change) Account  |
| [RATE-834366](https://hackerone.com/reports/834366) | security | $500 | _adjacent | - | Login CSRF vulnerability on hackerone.com |
| [RATE-838510](https://hackerone.com/reports/838510) | nextcloud | $250 | _adjacent | - | user can bypass password enforcement when federated sharing is enabled |
| [RATE-840598](https://hackerone.com/reports/840598) | nextcloud | $100 | _adjacent | CVE-2020-8202 | Possible denial of service when entering a loooong password |
| [RATE-840759](https://hackerone.com/reports/840759) | security | $500 | _adjacent | - | Reflected XSS on www.hackerone.com and resources.hackerone.com |
| [RATE-916704](https://hackerone.com/reports/916704) | nextcloud | $150 | _adjacent | CVE-2020-8235 | Access control missing while viewing the attachments in the "All boards" |
| [RATE-982291](https://hackerone.com/reports/982291) | basecamp | $5,000 | _adjacent | - | HEY.com email stored XSS |
| [RATE-1024880](https://hackerone.com/reports/1024880) | basecamp | - | _adjacent | - | SSL expired subdomain leads to API swap with main and flagged cookies. U |
| [RATE-1065186](https://hackerone.com/reports/1065186) | reddit | - | throttle-bypass-vectors | - | Weak rate limit could lead to ATO due to weak password protection mechan |
| [RATE-1154003](https://hackerone.com/reports/1154003) | nextcloud | - | throttle-bypass-vectors | CVE-2021-22915 | Ratelimiting can be bypassed using IPv6 subnets |
| [RATE-1165225](https://hackerone.com/reports/1165225) | reddit | - | login-password-gates | - | [dubsmash] Username and password bruteforce |
| [RATE-1192144](https://hackerone.com/reports/1192144) | nextcloud | $100 | login-password-gates | CVE-2021-32741 | Add to your nextcloud endpoint is not properly protected |
| [RATE-1192159](https://hackerone.com/reports/1192159) | nextcloud | $100 | login-password-gates | CVE-2021-32705 | public webdav endpoint not bruteforce protected |
| [RATE-1363672](https://hackerone.com/reports/1363672) | shopify | $3,500 | throttle-bypass-vectors | - | Bypass a fix for report #708013 |
| [RATE-1392287](https://hackerone.com/reports/1392287) | xvideos | $100 | login-password-gates | - | No-Rate limit of current password on delete account endpoint(https://www |
| [RATE-1394916](https://hackerone.com/reports/1394916) | ibb | $4,000 | _adjacent | CVE-2021-41773 | Path traversal and file disclosure vulnerability in Apache HTTP Server 2 |
| [RATE-1394984](https://hackerone.com/reports/1394984) | evernote | $150 | otp-2fa-reset-token | - | Email Verification Bypass by bruteforcing when setting up 2FA |
| [RATE-1406495](https://hackerone.com/reports/1406495) | shopify | $900 | otp-2fa-reset-token | - | Ability to Disable the Login Attempt of any Shopify Owner for 24 hrs  (Z |
| [RATE-1435392](https://hackerone.com/reports/1435392) | acronis | $250 | login-password-gates | - | Missing brute force protection on login page on www.acronis.com |
| [RATE-1559262](https://hackerone.com/reports/1559262) | ibb | $480 | _adjacent_unclassified | - | rubygems.org Batching attack to `confirmation_token` by bypass rate limi |
| [RATE-1587374](https://hackerone.com/reports/1587374) | linkedin | - | _adjacent | - | Campaign Account Balance and History Disclosed in API Response |
| [RATE-1592587](https://hackerone.com/reports/1592587) | linkedin | - | _adjacent | - | IDOR - Delete technical skill assessment result & Gained Badges result o |
| [RATE-1608735](https://hackerone.com/reports/1608735) | linkedin | - | _adjacent | - | IDOR allows an attacker to delete anyone's featured photo. |
| [RATE-1627961](https://hackerone.com/reports/1627961) | deptofdefense | - | _adjacent | - | Account takeover on ███████ [HtUS] |
| [RATE-1691195](https://hackerone.com/reports/1691195) | nextcloud | $100 | throttle-bypass-vectors | - | Missing rate limiting on password reset functionality allows to send lot |
| [RATE-1842114](https://hackerone.com/reports/1842114) | nextcloud | - | login-password-gates | CVE-2023-25820 | Missing brute force protection on password confirmation modal |
| [RATE-1879549](https://hackerone.com/reports/1879549) | nextcloud | - | login-password-gates | CVE-2023-32319 | Basic auth header on WebDAV requests is not bruteforce protected |
| [RATE-1987062](https://hackerone.com/reports/1987062) | nextcloud | $500 | otp-2fa-reset-token | CVE-2023-35172 | Password reset endpoint is not brute force protected |
| [RATE-2039447](https://hackerone.com/reports/2039447) | automattic | - | login-password-gates | - | Entering passwords on the Share Login Page can lead to a brute-force att |
| [RATE-2230915](https://hackerone.com/reports/2230915) | nextcloud | - | throttle-bypass-vectors | CVE-2023-49792 | Bruteforce protection in password verification can be bypassed |
| [RATE-2245437](https://hackerone.com/reports/2245437) | nextcloud | - | otp-2fa-reset-token | CVE-2023-49790 | App PIN code can be bypassed in Files iOS |
| [RATE-2627062](https://hackerone.com/reports/2627062) | acronis | $250 | throttle-bypass-vectors | - | Rate limit bypass on passport.acronis.work using X-Forwarded-For request |
| [RATE-2633771](https://hackerone.com/reports/2633771) | security | - | _adjacent | - | IDOR Vulnerability at AddTagToAssets operation name |
| [RATE-2915502](https://hackerone.com/reports/2915502) | xvideos | $200 | _adjacent_unclassified | - | Lack of Rate Limiting on Account Creation Endpoint   |
