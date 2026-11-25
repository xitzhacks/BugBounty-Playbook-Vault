---
title: "Credential Change & Email Verification — identity edits without proving the old identity"
type: playbook
category: credential-change-email-verification
cwe: "CWE-620"
source_count: 17
full_bodies_available: 17
corpus: "h1.security.nathan.sx roster (224 rows), bodies via hackerone.com/reports/<id>.json"
list_accessed: "2026-10-28"
note: "Anchor bodies: AUTH-29331 (HackerOne, $500 json), AUTH-147182/AUTH-147203 (FantasyTote), AUTH-223461 (Weblate, low), AUTH-98469 (Binary.com, $50 list), AUTH-156542 (Gratipay, $1 json). Claims trace to bodies read 2026-10-29."
---

# Credential Change & Email Verification — identity edits without proving the old identity

## 1. Overview

Seventeen cases about the *maintenance* half of authentication: changing email, username,
password, personal info — and the verification flows meant to guard them. This is the
corpus's least-paid class ($671 total) because most rows are informative, but it carries the
corpus's clearest ATO *recipe*: change the email → use forgot-password → own the account
(223461 spells it out end-to-end).

| Family | Cases | Bounty |
|---|---|---|
| Email change without verification / step-up | 147182 · 22203 · 45084 · 223461 | - ($0; 223461 low) |
| Password/info change without old password | 147203 · 146129 | - |
| Verification-flow bypass (username/email) | 29331 · 49304 · 98469 · 51166 · 156542 · 163467 · 64666 · 124151 · 80883 · 90643 · 260492 | $501 json · $170 list |

## 2. Email change without verification

**AUTH-147182** (FantasyTote, -, resolved) — the signup/email-change asymmetry, verbatim:

> When we try to signup with an email, it asks us for clicking a email validation link which is
> sent to our email, then we have to login, without clicking that link, we cannot login, but
> when we change email from user settings page/edit settings page, it doesn't asks us for
> validation..

Impact argument, verbatim:

> he can put any email like ([REDACTED_EMAIL]) and no verification is required, and the
> user can login with that email and access his account with the email [REDACTED_EMAIL]

**AUTH-22203** (Twitter, -, informative) — the Anand-family reset-link test applied to email
change, verbatim:

> Here  the password reset link of "[REDACTED_EMAIL]" which was old email address associated with
> twitter can be use to change the password of twitter account having  updated email address
> "[REDACTED_EMAIL]".

(Same mechanism as module 05's 17383/17474/23579 — verification lane carries the fix demand:
"As soon as new email address is updated all the previous links should also get expired.")

**AUTH-45084** (Vimeo, -, informative) — add-email with no verification and no password
confirmation, verbatim:

> Add a New Email to account without email verified and without password confirmation when the
> leaves open email ,Leading to the theft of account In less than a minute by reset password .

**AUTH-223461** (Weblate, low, resolved) — the complete recipe, verbatim:

> Since the e-mail could be used to reset the password of the account, an attacker, with
> temporary access to the victim's account (e.g. physical access to a device with an active
> session or by stealing the session etc.) could associate a new e-mail to the account, change
> the primary e-mail associated with the new one and then use the "forgot password"
> functionality to reset it, bypassing the current "password change" functionality
> ("/accounts/password" handler) that correctly requires the current password to be completed.

Email change = the step-up bypass around the password change that *does* ask for the old
password.

## 3. Password / info change without old password

**AUTH-147203** (FantasyTote, -, resolved) — verbatim:

> The password change mechanism which is located at https://www.fantasytote.com/users/edit is
> insecure as there is no old password field deployed in it. Any unauthorized user can access
> the account and can change the password directly without knowing the old password.

**AUTH-146129** (Instacart, -, informative) — "Current Password" field present but not
enforced, verbatim:

> Fill new information leaving "Current Password" blank
> 5. Click "Save Account Information"
> 6. The ​​"Personal Information" will be updated.

## 4. Verification-flow bypass

**AUTH-29331** (HackerOne, $500 json, resolved) — username change authorized by *any* email
to support, verbatim:

> I was asked for a confirmation from the same address without even verifying that the mail
> associated is of the original account or not. Moreover no email confirmation was sent to the
> original email to verify that the change has been made.

**AUTH-49304** (Vimeo, -, informative) — the confirmation goes to the *old* primary email,
verbatim:

> 4.Here come's the main part ( The confirmation link is sent the primary email of the attacker
> not to the one the attacker was going to add )

**AUTH-98469** (Binary.com, $50 list, resolved) — the verify link doubles as a reset link,
verbatim:

> Remove "step=account" from the URL, and tadaa! you will see once u enter the email you can
> change password!

**AUTH-51166** (IRCCloud, -, informative) — verification hash derived from the email
address only, verbatim:

> The hash value in the URL seems to be generated based on the entered email address. This
> tells me that the hash is not very strong. I would would have expected some randomness here
> as well

**AUTH-156542** (Gratipay, low, $1 json, resolved) — the unicode-lookalike resend confusion,
verbatim:

> 1. Mallory creates an a‎**1**‎ice@foo\.com email address, base64-encodes it, and sends Alice
>    a link https://gratipay.com/~alice/emails/verify.html?email2=YTFpY2VAZm9vLmNvbQ~~&nonce=x
> 2. When Alice opens the link, she sees a notification "The verification code for
>    [REDACTED_EMAIL] is bad. Resend verification email"
> 3. If she clicks the "Resend verification email" button, that fake a‎**1**‎ice@foo\.com email
>    will be automatically associated with her account, and a valid verification link will be
>    sent there.

**AUTH-163467** (Legal Robot, $120 list, resolved) — the email token leaks in user info,
verbatim:

> This contains some sensitive information, most notably the email token. A user can use this
> to bypass email verification and verify any email.

**AUTH-64666** (MapLogin, -, resolved) — 4-digit code, no rate limit, verbatim:

> Attacker will start brute force attack to get the correct verification code.Once Attacker
> gets the verification code,He will be able to use the Email id of victim on Maplogin account.

**AUTH-124151** (Zomato, -, resolved) — the verify-email link authenticates *and* leaks,
verbatim:

> When an user clicks on verify email address link, he/she is directly authenticated without a
> need of password, thereby bypassing authentication.

> Also, the verify email address link consist of ‘fbcid’ parameter which is just Base64
> encoded. It leaks sensitive data like unique user id, 4 digit code and email address of the
> user.

**AUTH-80883** (Gratipay, none, informative) — server-side email validation bypassed by
interception (`mymail%40gmail.com"><h1>` accepted). **AUTH-90643** (ownCloud, -,
informative) — no verification at registration ("anyone can use anyone's email without
verification"). **AUTH-260492** (Legal Robot, low, informative) — `john*[REDACTED_EMAIL]`
accepted as valid format.

## 5. Doctrine

- **The class's one ATO recipe** (223461): temporary session → change email (no step-up) →
  forgot-password → permanent ownership. Any email-change flow missing *both* old-password
  confirmation and re-verification is this recipe waiting for a reporter.
- **Where the money was**: identity edits with zero proof of intent (29331, $500 json — the
  only substantial payout) — because the *program itself* (HackerOne) treats username as
  identity.
- **Informative is the honest substate for most of this class**: 45084, 49304, 51166, 90643,
  22203, 146129 all informative. The corpus never padded them; the mechanics were right and
  the impact absent. Module 05 (reset-token) is where these designs turn into money.
- **Verification-link duality** (98469, 124151): when the same link both verifies and
  authenticates, every leak of that link is an ATO. Modern hardening (P4): separate tokens,
  POST-only confirmation, verified-email required before any identity edit.
