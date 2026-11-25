---
title: "Password Reset Token Design — the token is the key; where it lives, how long it lives, who can use it"
type: playbook
category: reset-token-design
cwe: "CWE-640"
source_count: 20
full_bodies_available: 20
corpus: "h1.security.nathan.sx roster (224 rows), bodies via hackerone.com/reports/<id>.json"
list_accessed: "2026-10-28"
note: "Anchor bodies: AUTH-173551 (Uber, $10,000 json, critical), AUTH-143717 (Uber, $10,000 list), AUTH-17383/17474/23579 (reset-after-email-change family), AUTH-229417/229528 (Weblate auto-login chains). Claims trace to bodies read 2026-10-29."
---

# Password Reset Token Design — the token is the key

## 1. Overview

Twenty cases on the reset token's lifecycle. Three corpus-proven payout ladders:
(a) **token exposure** — the token in an HTTP response ($10,000 json, critical) or in the
passwordless-signup flow ($10,000 list); (b) **token lifecycle** — surviving email change,
password change, or a newer token ($100–$300 list each); (c) **auto-login reset design** —
Weblate's chains that turned reset links into login links and logout weapons. The Referer
leakage quartet is informative/low unless the token also fails to expire.

| Family | Cases | Bounty |
|---|---|---|
| Token exposed in response / passwordless-signup | 173551 · 143717 | $10,000 json + $10,000 list |
| Referer leakage (third-party reach) | 5691 · 13557 · 244434 · 253448 | $20 list |
| Token survives email change | 17383 · 17474 · 23579 · 145896 | $400 list |
| Token survives password change / newer token | 15166 · 220185 · 23921 · 118948 | $100 list |
| Token brute force (with enumeration chain) | 17512 | - (informative) |
| Auto-login reset chains (Weblate) | 223637 · 229417 · 229528 | - (low/medium) |
| Invalid-reset-link logout | 54610 | $100 list |
| Unverified mobile in reset | 33432 | - (informative) |

## 2. The crown: token exposure in the wire

**AUTH-173551** (Uber, critical, $10,000 json, resolved) — the team summary states the whole
class in two sentences, verbatim:

> With an email address for a valid Uber account, it was possible to take over that account
> because the reset token was exposed in the response of a password reset HTTP request. This
> meant an attacker could initiate password reset for an account and immediately receive the
> reset token for that account.

No chaining, no user interaction — the token lives in a response the attacker can read.
**AUTH-143717** (Uber, $10,000 list, resolved) is its sibling: the passwordless-signup
endpoint lets *state* be set to `CREATE_NEW_PASSWORD` for any registered phone number.
Verbatim request core:

> {"phoneNumberE164":"+xxxxxxxx","userWorkflow":"PASSWORDLESS_SIGNUP","userRole":"client","mobileCountryISO2":"XX","state":"CREATE_NEW_PASSWORD","newPasswordData":{"newPassword":"12345678911a!"}}

> {"phoneNumberE164":"+xxxxxxxx","serverState":"SUCCEEDED","serverStateData":{"nextState":"SIGN_IN"},"tripVerifyStateData":{},"userMessage":"New password has been created. Please login with the new Password.","userRole":"client","userWorkflow":"PASSWORDLESS_SIGNUP"}

Two eras, same doctrine: **the reset credential must never travel where the attacker can
read it, and a signup flow is a password-set flow** (this row doubles as module 06's
verification lane).

## 3. Referer leakage — where tokens go to leak

**AUTH-5691** (c2fo, -, informative) — the template finding, verbatim:

> As you can see it's a link from a "https" page to a "https" url. That means that the referrer
> will be send to the target. That means that the password reset token will be leaked to the
> "truste"-company through the referrer.

> A bad boy webmaster at the "truste"-company could collect the reset urls/token from the
> access.log.

**AUTH-13557** (Factlink, -, informative) — CSS fonts as the leak sink, verbatim Referer line:

> referer:https://factlink-staging.herokuapp.com/users/password/edit?reset_password_token=8GbCsdRTX3yx3wZzwPuy

**AUTH-244434** (WakaTime, -, resolved) — the footer's Twitter share button leaks the token,
and the body adds the compounder, verbatim:

> Plus this issue becomes a bit more critical because I notice we can use the reset password
> tokens more then once which is another issue.

**AUTH-253448** (Legal Robot, low, $20 list, resolved) — team summary, verbatim:

> A security researcher discovered that sensitive information, like password reset tokens could
> still be leaked to analytics services like Google Analytics or via the Referer [sic] header.
> Even though tokens were immediately invalidated, we decided to re-engineer the process to
> eliminate any possibility of token leakage.

The team's fix philosophy is the doctrine: **token leakage is only fatal when the token
survives; eliminate both**.

## 4. Token survives identity change — the Anand Prakash family

Three identical reports across three programs (HackerOne, Phabricator, Secret) and one
Nextcloud variant. **AUTH-17383** (HackerOne, $100 list, resolved), verbatim:

> 3) Login using the same password back and update your email address to "[REDACTED_EMAIL]" and verify
> the same.
> 4) Now logout and use the password reset link which was mailed to "[REDACTED_EMAIL]" in step 2.
> 5) Password will be changed.

> All previous password reset links should automatically expire once a user changes his email
> address.

**AUTH-17474** (Phabricator, $300 list, resolved) adds the deletion twist ("Remove
'[REDACTED_EMAIL]'"). **AUTH-23579** (Secret, -, resolved) repeats it. **AUTH-145896** (Nextcloud, -,
resolved) — same test from the control panel.

## 5. Token survives password change / newer issuance

**AUTH-15166** (Mail.ru, $100 list, resolved) — old token stays live after a newer one is
issued, verbatim:

> Now generally after the issuance of token02,the previous unused token should expire.But in
> case of mavenlink  its not happening.Both the tokens are remaining usable at the same time.

(Body says "mavenlink" in the explanation while the title/target is mail.ru — recorded as
written; the mechanism is the finding, the copy-paste is the reporter's.)

**AUTH-220185** (Skyliner, -, resolved) — same test after a *password change*: "You'll see the
password reset link is not expired even after password change."
**AUTH-23921** (concrete5, -, resolved) — survives "upto 10" password changes.
**AUTH-118948** (Mail.Ru, -, resolved) — policy-vs-reality: "According to your policy, reset
or change password link should be expired within 30 minutes."

## 6. Token brute force (chained with enumeration)

**AUTH-17512** (HackerOne, -, informative) — the chain thesis, verbatim:

> Things required to takeover complete account :
> ========================================
> 1. Valid email-id which is registered on hackerone.

> As everyone replying my bug reports know that there is no BRUTE FORCE protection. I am doing
> the same.

Enumeration (../hunt-idor lane supplies the email) + no token rate limit = takeover attempt;
triaged informative in 2014. The class that owns the impact is rate limiting
(../hunt-brute-force); this module owns the token's entropy defense.

## 7. Auto-login reset chains (Weblate)

**AUTH-223637** (Weblate, low, resolved) — reset link logs you in, verbatim:

> * You dont need to Change Your Password because you'll be logged in.

> **Scenario**
> Victim forgot to logout his/her Email Account on a Cafe/Internet Renting Shops.

**AUTH-229417** (-, resolved) — the fix-bypass combo report: reset links double as logout
weapons (Issue 1, "Bypass the Logout CSRF fix") *and* login links (Issue 2, bypassing
#223339's fix). Verbatim impact:

> 2. If an attacker gets successful to do logout the Victim. Victim will never log in with
>    his/her current password. He have to change the password unintentionally.

**AUTH-229528** (medium, resolved) — registration-confirmation link = login link; attacker
observes the victim inside the attacker's account, then resets the fake account's password to
take the session. Verbatim:

> 4. Victim clicks the link and will automatically logged in to the attackers account.
> 5. Done, victim will think that he/she is in his own account.

CSRF-owned lanes (login-CSRF, logout-CSRF) get the cross-reference (../CSRF); the *design*
decision — auth-state granted by following a link — is this module's.

## 8. Reset-adjacent state abuse

**AUTH-54610** (Slack, $100 list, resolved) — visiting an *invalid* reset link logs the user
out, weaponized by image embed, verbatim:

> `<img src='https://yourteamname.slack.com/reset/youareloggedout'>`

> You should not logout a user when an invalid password reset link is accessed rather than you
> should redirect a user to homepage whenever a password reset link is accessed when user is
> allready logged in.

**AUTH-33432** (Twitter, -, informative) — unverified mobile numbers usable for reset
routing, verbatim:

> so without verification Twitter should not associate the mobile number with account for the
> password reset purpose !

## 9. Doctrine

- **Two $10,000 rows, zero chaining** — token-in-response (173551) and
  signup-state-confusion (143717). When the reset credential is readable or the password-set
  state is attacker-chosen, severity is critical without further decoration.
- **Lifecycle is the multiplier**: the referer-leak reports are informative/low *until* the
  token also fails to expire (244434's "can use the reset password tokens more then once" is
  what made it resolved). Test both halves.
- **The 5-step identity-change test** (17383): request reset → don't use → change email → use
  old link → password changes. Apply it to: email change (17383/17474/23579/145896), password
  change (220185/23921), newer token issuance (15166), policy timeouts (118948).
- **Auto-login links are a design smell** (Weblate trio): a link that grants a session turns
  email compromise into account compromise and CSRF into logout/login control. Modern
  hardening (P4): magic-link login exists (Slack) but pairs with device prompts.
- **Unchained class payout ceiling, corpus-observed**: $100–$300 list for lifecycle bugs;
  $10,000 for exposure. Report lifecycle bugs honestly as Low — the corpus's resolved-lows
  (223637) never pretend otherwise.
