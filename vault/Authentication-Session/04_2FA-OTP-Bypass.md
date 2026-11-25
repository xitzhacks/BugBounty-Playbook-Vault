---
title: "2FA / OTP Bypass — the second factor exists but does not decide"
type: playbook
category: 2fa-otp-bypass
cwe: "CWE-308"
source_count: 29
full_bodies_available: 29
corpus: "h1.security.nathan.sx roster (224 rows), bodies via hackerone.com/reports/<id>.json"
list_accessed: "2026-10-28"
note: "Anchor bodies: AUTH-178293 (Shopify, $1,500 json), AUTH-163834/AUTH-167121/AUTH-179421 (VK trio, $3,050 json), AUTH-10554 (Coinbase, $1,000 json), AUTH-128085 (GitLab), AUTH-100509 (HackerOne, $1,000 json). Claims trace to bodies read 2026-10-29."
---

# 2FA / OTP Bypass — the second factor exists but does not decide

## 1. Overview

Twenty-nine cases — the corpus's biggest class by row count and, at $8,920, its third by
bounty. The bodies split the class into bypasses (the login flow accepts the attacker without
the second factor) and validation-design flaws (the code itself is wrong: reusable, unverified,
leaked, or brute-forceable). A distinct LegalRobot program family (10 rows) documents a whole
2FA rollout's bug harvest — mostly $20–$90 list rows, one high (enumeration).

| Family | Cases | Bounty |
|---|---|---|
| Login-flow 2FA bypass (session/step confusion) | 163834 · 167121 · 179421 · 90165 · 178293 · 128085 · 124845 · 130460 · 145629 | $4,050 json · $150 list |
| OTP brute force & rate limit | 128777 · 149598 | $100 json |
| OTP leak in error/response | 142221 · 247158 | $250 list (high) |
| OTP validation design (reuse, unverified, cross-account) | 67660 · 77076 · 66223 · 10554 | $1,250 json · $100 list |
| 2FA secret pre-generation | 100509 | $1,000 json |
| 2FA change governance | 16696 | - (informative) |
| LegalRobot 2FA-rollout family | 249337 · 249346 · 249431 · 249467 · 249695 · 250082 · 250243 · 251200 · 259415 · 259416 | $470 list |

## 2. Login-flow 2FA bypass — the VK trio and the state machine

**AUTH-163834** (VK, $1,000 json, resolved) — Russian title «Обход 2ух-шаговой авторизации /
2FA Bypass» (2FA bypass). Body is the team summary, verbatim:

> Был косяк в функционале завершения сессий. При обращении на login.vk.com с reset_hash любого
> пользователя, мы получали доступ к аккаунту жертвы минуя 2FA.

(Team summary: a flaw in the session-termination feature — hitting login.vk.com with any
user's `reset_hash` yielded access to the victim's account bypassing 2FA.)

**AUTH-167121** (VK, $1,050 json, resolved) — «Второй способ обхода 2FA» (a second 2FA
bypass). Team summary, verbatim: «Лазейка с релогином при смене IP у пользователя» (a loophole
in re-login on the user's IP change).

**AUTH-179421** (VK, $1,000 json, resolved) — «Новый 2FA Bypass». Team summary, verbatim:
«Косяк в функции смены пароля» (a flaw in the password-change function) — partial session
check. This is module 03's password-change non-invalidation lane *with* a 2FA outcome.

**AUTH-90165** (VK, $500 json, resolved) — Russian one-liner: «Отсутствие hash на вывод списка
резервных кодов» — no hash/CSRF check on the backup-codes listing, plus framing, leading to
2FA compromise. Cross-class note: delivery is CSRF (../CSRF lane), impact is 2FA loss.

**AUTH-178293** (Shopify, $1,500 json, resolved) — the SSO lane silently disables 2FA.
Verbatim:

> 3. Now your try to "Sign In with Google" `https://shop-1.myshopify.com/admin/auth/login?google_apps=1`
>
> What's weird is no two factor code is required and you directly land in Admin Panel

> Issue here is Two Factor Authorisation is disabled as soon as you "Sign In with Google" and
> now you cannot even enable it because you can't see any Two Factor Authenticator Tab in
> Accounts

> Also there is no indication to via mail or notification that Two Factor Authorisation has
> been disabled when Two Factor Authorisation is disabled

**AUTH-128085** (GitLab, -, resolved) — the canonical `otp_user_id` swap. Verbatim:

> - in the background, it sets Jane's user ID in `session[:otp_user_id]`
> - you now need to enter Jane's 2FA code in order to get access to the account

> - now add the `login` header to the request - the request now looks like:

…with `user[login]` = `john` — the OTP-submit step accepts a *different* login than the one
the password was checked against. Second-factor state carried in a session field that the
attacker controls.

**AUTH-124845** (Shopify, $500 json, resolved) — the enable-flow password gate bypassed by
replaying Account-1's SMS request with Account-2's cookies/uid. Verbatim:

> 4.Now i want to bypass password authentication in Account-2  so i replaced cookies , xsrf
> token , host and user_id in above request and keep authenticity_token same . Now request
> look loke this .

**AUTH-130460** (Zomato, $50 list, resolved) — team summary, verbatim: "OTP was not properly
checked on the session so it could have been bypassed by intercepting the server response and
changing its value to valid."

**AUTH-145629** (Algolia, $100 list, resolved) — session predates the factor, verbatim:

> 3.you will see that your account is already opened without do 2-factor authentication

## 3. OTP brute force & rate limit

**AUTH-128777** (Algolia, $100 json, resolved) — verbatim:

> There is no rate limit set for Two factor authentication, which demand for code sent to
> mobile. This code can be bruteforced easily to bypass this.

**AUTH-149598** (GitLab, -, resolved) — the most careful body in the class: measured the
window (10–19 attempts before throttling, 30–40 s stop), computed token validity (60 s with
drift), and argued the flaw is *system design*, not the out-of-scope "rate limiting" label.
Verbatim:

> It appears that initially, an attacker can submit anywhere from 10 - 19 requests to validate
> a 2FA before rate limiting kicks in.

## 4. OTP leaked or cross-wired

**AUTH-247158** (Foodpanda, high, resolved, $250 list) — team summary: "Attacker was able to
bypass the OTP verification needed while placing an order with a restaurant."
**AUTH-142221** (same lane, resolved) is the mechanism, verbatim:

> If wrong OTP is provided then the error message shows the session code which is the OTP in
> this case. Hence that session code can be used to verify the phone number and the order can
> be placed.

## 5. OTP validation design

**AUTH-67660** (WordPress.com, $100 list, resolved) — the MagicCode that never expires,
verbatim:

> I found out that verification code sent as SMS while enabling Two-Step Authentication can be
> reused infinitely for login.

**AUTH-77076** (Romit, $250 json, resolved) — server skips GA verification for
support-denied accounts, verbatim:

> The GA Code is not verified on the server side for the users whose "Verification
> application" has been DENIED by the Romit support Team

**AUTH-66223** (Coinbase, -, informative) — SMS codes valid across accounts sharing a phone
number, verbatim:

> Thank you.
> █████

(Title-linked mechanism: `account-A` + `code-B` accepted, verbatim from body: "I found myself
be logged in with two accounts and there is no problem there".)

**AUTH-10554** (Coinbase, $1,000 json, resolved) — 2FA-protected transfers bypassed through
the *internal* transfer endpoint, verbatim:

> The vulnerability exists in the transfer feature that allows you to transfer funds between
> all wallets under the same account (internal transfer). This feature is only visually
> available when you have at least two wallets, but it is not necessary to have two wallets to
> exploit this vulnerability.

> - Change the `transaction[to]` parameter to the Mongo BSON ID of the wallet you want to
>   transfer the BTCs to. This can be any wallet ID outside the account you were initiating an
>   internal transfer for.

> - Forward the request. The money is now transferred to the Coinbase wallet associated with
>   the ID specified under `transaction[to]`. No two-factor code was entered.

The transfer request itself carries `transaction[notes]` = "Bypassin' 2FA." — the corpus at
its most confident.

## 6. 2FA secret pre-generation (HackerOne)

**AUTH-100509** ($1,000 json, resolved) — the settings page pre-renders next-use secrets into
the DOM before activation, verbatim:

> requesting `https://hackerone.com/settings/authentication/edit` and parsing out the two factor
> authentication form will yield either…

> - the 2FA secret key and backup codes that *will* be used if 2FA is enabled for the first
>   time this session

> While *activating* 2FA or *confirming* backup codes regeneration requires knowledge of the
> user's password/TOTP code, reading the values out from the DOM does not (again, provided that
> you've compromised the user's session and are running script in their domain)

XSS-delivered (../XSS lane), but the *design flaw* — pre-generating secrets into HTML — is the
2FA class's own.

## 7. Change governance (Coinbase)

**AUTH-16696** (-, informative) — the reporter argues *for* a control: funds-freeze after 2FA
settings change. Verbatim thesis:

> That design keeps the 2FA from being defeated instantly if the user's email account has been
> breached.

## 8. The LegalRobot 2FA-rollout family (10 rows)

One program shipped 2FA in 2017; the bounty page harvested the rollout. All bodies are team
summaries (quoted verbatim in register):

- **AUTH-249337** (none, $60 list) — non-functional recovery codes ("improper error handling
  on the client during account recovery").
- **AUTH-249346** (medium, $90 list) — recovery-code fallback missing for TOTP-only users.
- **AUTH-249431** (medium, $90 list) — 2FA user enumeration via password reset ("users that
  had enabled 2FA were prompted for a second factor").
- **AUTH-249467** (high, -) — enumeration via login: "rejected *all* attempts for that user
  regardless of what password was used".
- **AUTH-249695** (none, $60 list) — client error handling: "the login progress spinner
  continued without interruption".
- **AUTH-250082** (medium, $60 list) — enhancement: email confirmation for recovery use.
- **AUTH-250243** (none, $60 list) — 2FA users skip regular logon hooks: "one action logs out
  other sessions when a new session begins. While there is no specific vulnerability from this
  issue *in isolation*, an attacker could use this as part of a larger attack strategy."
- **AUTH-251200** (none, $60 list) — missing TOTP `Issuer` parameter ("no direct security
  impact").
- **AUTH-259415** (-, $20 list) — 52-bit manual secret entry UX.
- **AUTH-259416** (-, $20 list) — factually wrong 2FA-disabled email.

## 9. Doctrine

- **The paying bypasses are state-machine bugs, not crypto bugs.** Every $500+ row here
  (178293, 163834, 167121, 179421, 100509) is "the flow reaches the authenticated state without
  evaluating the factor": factor silently disabled by another login method (178293), factor
  skipped via session-fixation hash (163834), factor skipped at re-login (167121), factor
  skipped at password change (179421), factor state carried in an attacker-writable session
  field (128085).
- **Validation-design flaws pay $100–$1,000**: reusable codes (67660), unverified codes
  (77076), codes valid across accounts sharing a phone (66223), and the internal-transfer
  endpoint exempt from the transfer factor (10554).
- **Brute force needs the window math** (149598): attempts-before-throttle × throttle-duration
  × token-validity → achievable guesses. A bare "no rate limit" title gets triaged to
  ../hunt-brute-force doctrine; the window math is what made GitLab resolve it.
- **Delivery-vs-impact discipline**: 90165 (CSRF-delivered 2FA loss) and 100509
  (XSS-delivered secret read) sit in this module because the *deciding flaw* is the 2FA
  design; the delivery class gets the cross-reference.
- Era note: the VK trio predates WebAuthn; the same state-machine bugs today hide behind
  remembering-devices and trust-on-first-login — P4 fingerprints those.
