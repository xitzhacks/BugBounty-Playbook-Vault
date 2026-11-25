---
title: "Account verification and rate limiting — identity controls checked too late, or not at all"
type: playbook
category: account-verification-rate-limiting
cwe: "CWE-287, CWE-799, CWE-841"
source_count: 19
full_bodies_available: 18
corpus: "h1-brain disclosed_reports.db 3,673 rows (sha256 8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4); misconfig bucket (152 rows)"
list_accessed: "2026-11-07"
note: "19 rows / $4,050 (4 paid). 18 substantive bodies; MISCONF-171205 is a 100-byte one-liner (bombardment claim). All blockquotes byte-true to references/archive/MISCONF-bodies-full-dump.txt."
---

# Account verification and rate limiting — identity controls checked too late, or not at all

## 1. Overview

Nineteen rows, **$4,050/4 paid** — and the money is concentrated in a single row. The module holds two failure families that share a root cause (the server checks identity too late, then too weakly, then too late again): **email/phone verification that can be skipped, forged, or flood-attacked** (the bulk of the module: consent, verification states, and account-creation flows) and **rate limiting that exists on paper but collapses under ordering, scope, or reset bugs** (password endpoints, OTPs, SMS, referral and comment endpoints). The pricing lesson is brutal and consistent: the one six-figure-row-equivalent finding ($3,750) is a *registration validation* bug that scales to unlimited accounts; the seven $100 findings in this module's history are all "the control exists but is shallow" — captcha, back-button, comment caps at 1,000/minute, which triage prices as friction, not as a break.

**Case-stock (19 rows / $4,050):**

| Case | Target | Mechanism | Bounty |
|---|---|---|---|
| [MISCONF-57764](https://hackerone.com/reports/57764) | coinbase | Back-button skips email verification ($100) | $100 |
| [MISCONF-160109](https://hackerone.com/reports/160109) | instacart | iOS brute force / lockout bypass | - |
| [MISCONF-163467](https://hackerone.com/reports/163467) | legalrobot | Info leak bypasses email verification | - |
| [MISCONF-170310](https://hackerone.com/reports/170310) | security | Password endpoint resets rate limit | - |
| [MISCONF-171205](https://hackerone.com/reports/171205) | algolia | Referral email bomb (100B) | - |
| [MISCONF-194329](https://hackerone.com/reports/194329) | nextcloud | No session invalidation on password change | - |
| [MISCONF-229619](https://hackerone.com/reports/229619) | shopify | Resend link verifies unowned email | - |
| [MISCONF-246801](https://hackerone.com/reports/246801) | coinbase | Captcha bypass at signup ($100) | $100 |
| [MISCONF-262830](https://hackerone.com/reports/262830) | unikrn | Rate limit last stage → enumeration | - |
| [MISCONF-263010](https://hackerone.com/reports/263010) | unikrn | Phone-verify resend → SMS cost/spam | - |
| [MISCONF-587910](https://hackerone.com/reports/587910) | security | 2FA disabled without password | - |
| [MISCONF-617896](https://hackerone.com/reports/617896) | gitlab | Salesforce login skips email verification (CVE-2019-5486) | - |
| [MISCONF-743545](https://hackerone.com/reports/743545) | bumble | SMS recovery-code brute force | - |
| [MISCONF-774050](https://hackerone.com/reports/774050) | yelp | Confirmation-email flood (Yelp) | - |
| [MISCONF-792295](https://hackerone.com/reports/792295) | bumble | 4-digit OTP never expires | - |
| [MISCONF-815085](https://hackerone.com/reports/815085) | security | % / %0d%0a accepted in email → mass accounts ($3,750) | $3,750 |
| [MISCONF-854793](https://hackerone.com/reports/854793) | brave | Confirmation-email flood (Brave) | - |
| [MISCONF-1040047](https://hackerone.com/reports/1040047) | automattic | Signup email-verification bypass (Tumblr) | - |
| [MISCONF-1202408](https://hackerone.com/reports/1202408) | reddit | Comment rate limit 1000/min ($100) | $100 |

## 2. The crown row: garbage in the email field, unlimited accounts out

MISCONF-815085 (security / HackerOne itself, **$3,750**, the second-largest figure in the entire vault) is a registration-input-validation bug. The signup email field accepts `%` and `%0d%0a` (CRLF) as legitimate address characters:

> Hackerone SignUp feature is misconfigured with email parameter. Email address parameter is accepting % and %0d%0a character along with genuine email address. Using this technique hackerone user account can be created but cannot be verified as there is not possible to verify those invalid email accounts. Basically random use of invalid email address, attacker can create multiple accounts.

> As email address field always being verified with any special character (except @ and .) but here email is accepting % and line termination char %0d%0a

> >>Garbage value can be stored in database using user account signup form
> >>Multiple account can be created, just like if any use has real account with his email address, then also account can be created by adding %0d%0a or % char

The doctrine is about *where* validation lives: the form validated against a character blacklist that forgot CRLF metacharacters, while the mail path needed them validated. Any program whose signup handler shells out to a mailer, an SMTP layer, or a header-bearing message with the raw email field inherits this class. The CRLF neighbor is MISCONF-164137 (module 05): `%0D%0A` surfacing as page content via error responses — same metacharacters, different sink.

## 3. Verification that never happened

The module's $0 rows are the negative space, and they teach the same lesson from the other side: *a verification that fails is only a finding if the flow continues without it.*

- **Back-button skip** — MISCONF-57764 (coinbase, **$100**):

> Here simply we can bypass this validation and can successfully login to the application without verifying the validation email which comes to the user.Using this the attacker can create so many spoofed accounts.

The six-step repro (signup → verification screen → back button → login with fresh creds) is the cleanest verification-skip write-up in the corpus.
- **Forged confirmation token** — MISCONF-229619 (shopify, no figure): the email-change resend link verifies the new address even for an address the user does not own ("Go to `https://accounts.shopify.com/email-change/<Confirmation-TOKEN>/` and the email will be verified even though you don't own it"). Token possession stood in for inbox possession.
- **SSO backdoor** — MISCONF-617896 (gitlab, CVE-2019-5486, no figure): Salesforce's admin-created arbitrary email lets a user "signup with any email domain they want, effectively bypass all email domain whitelist/blacklist restriction." The interesting mechanism is trust inheritance: the IdP's account semantics are stronger than the relying party's verification.
- **Silent 2FA removal** — MISCONF-587910 (security, no figure): "Password not checked when disabling 2FA on HackerOne" — a settings endpoint that trusts the session alone for a security downgrade.
- **Session survives password change** — MISCONF-194329 (nextcloud, no figure): no logout of other sessions after credential change — the verification counterpart to 587910. Both are "privileged identity operation guarded by session presence only."

## 4. Rate limits that collapse: ordering, reset, and floods

- **Ordering** — MISCONF-262830 (unikrn, no figure) is the module's best rate-limiting write-up. The WAF rejects over-registration with a "Suspicious Activity" message, but the check runs *last* in the handler — after email-existence and password-strength oracles:

  > Unikrn increases the registration security by requiring user to enter a secured password and providing a rate limit on registration, after several attempt the server denies over-registration by returning "Suspicious Activity - Multiple Accounts Detected. Please contact support at [REDACTED_EMAIL] with further questions". However the rate limit get executed in the last stage of the registration process, still allows the attacker to enumerate account on this page.

  The body's fix is one sentence: move the rate-limit check to the first stage. Every enumeration report should copy this handler-ordering framing.
- **Scope reset** — MISCONF-170310 (security, no figure): `/users/sign_in` returns 429 properly, but `POST /users/password` resets the counter ("This however, does work all the time on /users/password endpoint"). A rate limit budgeted per-endpoint instead of per-identity is a rate limit that doesn't exist.
- **OTP brute force** — MISCONF-743545 (bumble, no figure): "It's possible to bruteforce recovery code from SMS as iOS application doesn't have limits for incorrect inputs. I have tried 50+ different combinations until I reached code from SMS." MISCONF-792295 (bumble, no figure) is the sibling: a 4-digit OTP that never expires. MISCONF-160109 (instacart, no figure) is the platform variant: the iOS app's brute-force and lockout-bypass controls are weaker than the web's.
- **Cost attacks** — MISCONF-263010 (unikrn, no figure): the phone-verification resend endpoint can be replayed to exhaust the SMS delivery system:

> Improper validation at Phone verification is allowing an attacker to exhaust the SMS delivery system probably increasing the cost of the subscription for that SMS service.
- **Flood economy** — MISCONF-774050 (yelp) and MISCONF-854793 (brave): confirmation-email resends without throttling → inbox bombing of any victim address. MISCONF-171205 (algolia, 100-byte body) is the same claim in one line: "It is possible to bombard the referral requests to the same email any number of times." The module keeps it as a metadata row — claim recorded, technique absent.
- **Cap set too high** — MISCONF-1202408 (reddit, **$100**): "The add comment endpoint has a speed limit, but the number is set too high, so speed limiting is activated when you write more than 1000 comments per minute." And MISCONF-246801 (coinbase, **$100**): captcha bypass at signup. These are the $100 tier of this class — friction defects, priced as such.

## 5. What pays, what doesn't

- **Pays ($3,750; $100 ×3):** input-validation at registration that scales to mass account creation (815085), and the three $100 friction defects (57764 verification skip, 246801 captcha, 1202408 cap). The $100 cluster is the module's most common paid outcome — small, real, and deliberately under-priced as a signal to close the gate.
- **Denies nothing, but pays nothing in the DB (15 rows):** the rate-limit ordering, OTP, flood, and verification-skip rows above carry no figure. Their value in the corpus is methodological — they are the exhibits the playbook cites when it says *order your challenges: count, timeout, binding of code to identity, resend discipline.*
- **The anti-pattern to avoid** (from 262830): testing only whether a limit *exists* ("Suspicious Activity" fires after N tries) and filing the limit-bypass. The paid-adjacent lesson is that the limit must be tested for *position* (does it fire before or after the oracle?), *scope* (per-endpoint vs per-identity), and *expiry* (OTP lifetime, code binding), in that order.

## 6. Cross-references

- Module 02's verification-skip family is the account-layer twin of module 04's unverified-email-change rows (MISCONF-906790 — changing another surface's email without verification, File Sync & Share takeover) and MISCONF-2001913/2068830 (email-driven support tickets as identity operations).
- The CRLF pair (MISCONF-815085 here, MISCONF-164137 in module 05) is the smuggling-crlf vault's registration-flow specimen.
- The race-condition vault's RACE-300305 (Shopify email-confirm race, $15,250) is the TOCTOU sibling of this module's verification-skip family — same "validated flag exists" primitive, reached by timing rather than by flow order.
- Playbook P2 (auth/verification probe ladder) and P3 (enumeration-vs-account proof).
