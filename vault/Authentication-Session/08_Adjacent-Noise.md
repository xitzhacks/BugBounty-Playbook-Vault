---
title: "Adjacent & Noise — auth-adjacent findings that belong to other classes, plus transport/idle noise"
type: playbook
category: adjacent-noise
cwe: "CWE-16"
source_count: 48
full_bodies_available: 48
corpus: "h1.security.nathan.sx roster (224 rows), bodies via hackerone.com/reports/<id>.json"
list_accessed: "2026-10-28"
note: "Anchor bodies: AUTH-258117 (Jenkins, $5,000 list, medium), AUTH-50170 (FREAK, $7,500 list), AUTH-257119 (WakaTime impersonation). Claims trace to bodies read 2026-10-29. Titles matched auth arms; bodies place the owning class elsewhere."
---

# Adjacent & Noise — where auth-arm titles land when bodies say otherwise

## 1. Overview

Forty-eight rows the title filter caught but whose bodies place the *owning* class elsewhere.
This module is the vault's triage honesty ledger: it records them with the cross-reference so
the eight real modules stay clean — and it shows what the auth arms actually harvested per
dollar: $17,821 of the roster's $123,419 sits here, mostly because transport-level and
TLS-impersonation reports ride auth-adjacent titles.

| Group | Cases (counts) | Bounty |
|---|---|---|
| CSRF-owned (login/logout/ATO-via-CSRF) | 2857 · 13705 · 7516 · 147204 · 223329 · 244778 · 50703 · 6907 · 6910 · 15476 · 152052 · 2857 · 157956 · 155774 | $2,070 |
| Third-party OAuth XSS (Twitter) | 87040 | $2,520 list |
| Impersonation/identity-abuse (not login) | 280 · 3722 · 97377 · 123743 · 257119 | $100 list |
| TLS / transport impersonation | 50170 · 241892 · 242622 · 224379 · 224287 · 6927 · 173251 | $7,500 list |
| RCE via auth-flow context | 258117 | $5,000 list |
| Open redirect via auth flow | 91332 · 223326 | - |
| DMARC / email-auth reports (not auth bypass) | 135283 · 115245 | - |
| Idle/timeout policy & misc | 123897 · 23913 · 134206 · 146838 · 243049 · 207552 · 176979 · 46109 · 115845 · 126235 · 98432 · 78781 · 18503 | $451 |
| XXE in SAML | 106865 | - (high) |
| Google Authenticator plugin audit | 172606 · 172609 | - (N/A) |

## 2. CSRF-owned rows → ../CSRF

Thirteen rows are login-CSRF, logout-CSRF, or CSRF-to-ATO chains: 2857, 6910 ("Full account
takeover using CSRF and password reset", $500 list), 6907/15476 (same title pair, $500 list
on the first), 50703 ("CSRF in login form would led to account takeover", $500 list), 7516
and 13705 and 223329 and 244778 (logout CSRF; 244778 duplicate), 147204 ("Bypass logout"),
152052 ("CSRF Full Account Takeover"), 157956 ("CSRF To change Email Notification Settings",
$50 list), 155774 ("CSRF - Add optional two factor mobile number", $500 json). The CSRF vault
owns all thirteen; listed here because auth-arm titles caught them.

## 3. Transport & TLS impersonation

**AUTH-50170** (HackerOne, $7,500 list, resolved) — FREAK, verbatim:

> Many TLS servers, including those hosting sensitive websites such as www.nsa.gov and
> connect.facebook.net, support weak EXPORT_RSA ciphersuites. By factoring their 512-bit
> ephemeral RSA keys, a network attacker is able to impersonate these websites to web browsers

TLS impersonation ≠ authentication bypass in the app sense — the vault keeps it here as the
transport-level sibling of module 07's voucher failures. The session-certificate rows
(241892/242622 — same inside.gratipay.com invalid-cert hijack, duplicate + N/A),
secure-flag missing (224379, low), session cookie over HTTP (6927), verification over
unencrypted channel (224287, low), and reset emails missing TLS (173251) complete the
transport group.

## 4. RCE via auth-flow context

**AUTH-258117** (HackerOne, medium, $5,000 list, resolved) — the corpus's best proof that
*authentication-flow misconfig* is a reach primitive even when the payload is another class,
verbatim:

> @nahamsec found a test Jenkins instance where they could login with any valid Google account.
>
> Once logged in, they gained the ability to execute arbitrary code via the Jenkins Script
> Console. This was a test jenkins instance with no access to source code or resources.

The auth flaw (any Google account accepted — the 143482 hosted-domain family!) reached RCE;
HackerOne paid $5,000 and classified medium. The RCE vault owns the payload; the *decision*
that any valid Google account = employee is module 01's family.

## 5. Impersonation & identity abuse (non-login)

- **AUTH-280** ($100 list, resolved) — "Real impersonation" (team summary; recorded as
  resolved, $100).
- **AUTH-257119** (WakaTime, resolved) — leaderboard invitation carries attacker-chosen Name
  + unconfirmed email, verbatim:

> Anyone can sign up with any email id and use the leadersboard invitation to invite anyone.
> This loophole can be leveraged for impersonation of any user to the victims.

- 3722 (incoming-webhook impersonation, informative), 97377 ("Hackerone impersonation"),
  123743 (H1 email impersonation) — same family.

## 6. Noise with a lesson

- **OAuth-surface XSS**: 87040 ("XSS on OAuth authorize/authenticate endpoint", $2,520 list,
  resolved) — XSS vault owns it; the OAuth lane gets the cross-ref.
- **XXE in SAML**: 106865 (rev-app.informatica.com, high, resolved) — XXE vault owns it
  (also blogs-index §2.5 lane note).
- **DMARC-title rows**: 135283 (not-applicable) and 115245 (duplicate) — bodies are DMARC/
  email-authentication reports, not application auth bypass. Title-filter false positives.
- **Idle policy & misc**: 123897 (auto-logout after 20 min, low, $1 json, informative),
  23913 (DMs persist after Twitter iOS logout — the module-03 lane's iOS variant),
  134206, 146838, 243049, 207552 (medium, informative — no security check at password change
  + mobile number), 176979 (low, $200 json), 46109 (cookie brute force, informative),
  115845 ($20 list, rate limit on email confirmation link), 126235 (text injection on
  check-otp, informative), 98432 ($280 list), 78781 ($150 list), 18503 (informative).
- **Open redirect via auth flow**: 91332 (informative), 223326 (medium, resolved) —
  ../Open-Redirect owns the class; both were caught here by "login with facebook"/
  "third-party authentication" titles.

## 7. Doctrine

- **Class ownership follows the body, not the title.** 13 of 48 rows here are CSRF-owned,
  7 transport-owned, and the biggest single bounty in the whole roster ($7,500 FREAK) sits in
  this module because its class is TLS, not authentication. Triage honesty beats vanity
  module membership.
- **But auth-*flow* context keeps a cross-reference**: 258117 and 106865 and 87040 all used
  an authentication surface as the *reach*, and their lessons belong in this vault's test
  lists even though their payouts belong to other vaults.
- **Fingerprint for P4**: the transport group is exactly what HSTS/mTLS/secure-flag/strict
  redirect validation killed after 2017 — when testing modern targets, these rows convert to
  "check the hardening is present", not findings on their own.
