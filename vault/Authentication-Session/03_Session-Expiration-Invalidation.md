---
title: "Insufficient Session Expiration & Invalidation — the server forgets to kill sessions"
type: playbook
category: session-expiration-invalidation
cwe: "CWE-613"
source_count: 26
full_bodies_available: 26
corpus: "h1.security.nathan.sx roster (224 rows), bodies via hackerone.com/reports/<id>.json"
list_accessed: "2026-10-28"
note: "Anchor bodies: AUTH-353/AUTH-737 (HackerOne, $100 json each), AUTH-222082 (OWOX, critical), AUTH-250688/AUTH-245833 (Federalist), AUTH-226712 (Paragon). Claims trace to bodies read 2026-10-29."
---

# Insufficient Session Expiration & Invalidation — sessions that refuse to die

## 1. Overview

Twenty-six cases — the corpus's most duplicated lane. Logout, password change, account
deletion, org removal: none of them kill the session server-side. Individually these are
$0–$300 reports (and 18 of 26 paid nothing); the class's value is as a *post-exploitation
persistencer* and as a chaining anchor — the corpus's own reporters say so.

| Family | Cases | Bounty |
|---|---|---|
| Logout non-expiry (HackerOne's own program) | 284 · 288 · 353 · 737 · 20122 | $200 json · $200 list |
| Logout non-expiry (other programs) | 7041 · 152080 · 21172 · 13602 · 231041 · 244875 · 245124 | $100 list |
| Password-change non-invalidation | 145300 · 145430 · 148914 · 223327 · 226518 · 226712 | - |
| Signup/re-entry bypass after logout | 222082 | - (critical) |
| Backdoor session values | 250688 · 245833 | $450 list |
| Residual data after logout | 249798 · 232306 | $20 list |
| Browser-cache after logout | 7909 · 158270 | - |
| Session logon management | 11722 | - (informative) |

## 2. The HackerOne logout family — four ways to say one thing

**AUTH-353** ($100 json, resolved) — the clean minimal repro, verbatim:

> 1. Log into the website - hackerone.com.
> 2. Capture any request. For ex, profile edit page using burp proxy.
> 3. Logout from the website.
> 4. Replay the request captured in step 3 and notice it displays the proper response.

**AUTH-737** ($100 json, resolved, by Dawid Czagan) — the most precise mechanism of the four,
verbatim:

> When a request with an invalid authenticity_token is received, the user is logged out (tested
> for updating user's profile, which is available here:
> https://hackerone.com/diekatze/profile/edit) and the user receives a new session cookie,
> which is not authenticated at this point. However, the authenticated session cookie used by
> a user before logging out is still active.

**AUTH-288** ($100 list, resolved) — server-side vs client-side, verbatim:

> The cookie is cleared from the client side (browser), but is not cleared from the server
> side. If reused, it provides access to the user's account.

> Therefore, any session cookie can be reused to gain access to the user's account.

**AUTH-284** (resolved) — persistence window quantified, verbatim:

> 4) After 6 hrs or 8 hrs copy the same cookies in your Chrome using the same extension and you
>    will be logged into your account.The cookies are not getting expired once the user logs
>    out of his account.

**AUTH-20122** (informative) — the missing control surface: "there should a section to see all
active sessions and to terminate them."

Duplicates proving universality: AUTH-244875 and AUTH-245124 (WakaTime, both duplicate) replay
the same repro — 244875 even cites its ancestor verbatim: "Reference From : #353".

## 3. Password-change non-invalidation

The scene is two browsers; the bug is that changing the password kills neither.

**AUTH-226712** (Paragon bridge.cspr.ng, critical, N/A) — verbatim:

> Description : When a user changes his account password, all the sessions on other
> devices/browsers should expire.

**AUTH-145430** (help.nextcloud.com, informative) — verbatim:

> When the password of an account is changed from a session, other sessions doesn't expire!

**AUTH-148914** (CMS Airship, informative) — proposes the correct fix semantics, verbatim:

> Server-side session should expire after password is changed from one session, or it should
> ask (either logout from other devices/browsers OR don't destroy the session [Like facebook
> does when changing password])

**AUTH-223327** (Weblate, low, resolved) — replay proves the stale session still *writes*, verbatim:

> 3. Replay the captured request by changing any parameter(username or fullname)
> 4. You get a response saying our profile settings was updated.

**AUTH-145300** (Paragon, N/A) — reset-link variant: the first browser's session survives the
second browser's password change via reset link.

One-liners: AUTH-226518 ("no session logout after changing the password in
https://bridge.cspr.ng/").

## 4. Signup/re-entry bypass after logout

**AUTH-222082** (OWOX support.owox.com, critical, resolved) — logout doesn't fully expire the
Zendesk-hosted support session; the Sign-in button re-enters without credentials. Verbatim:

> Step 4 : Click on Sign in again, you won't be asked for login with Gmail or something like that.
> Successfully Logged In without entering username-password or gmail account.

Title says "Login Bypass"; the body's mechanism is incomplete expiry — the class lens that pays.

## 5. Backdoor session values (Federalist)

**AUTH-250688** (low, resolved) — `federalist.sid` survives logout AND re-binds to the *next*
login of *any* user. Verbatim:

> The user/attacker, who got once valid cookie `federalist.sid` from the account, can use it as
> backdoor for some time, because it is not actually invalidated on Logout.

> Actually, logout just invalidating GitHub access token, but session still can be valid.

Case 2 of the body shows the session value re-validating against a different user's login.

**AUTH-245833** (medium, resolved) — authorization state cached at login, verbatim:

> When user perform login to the Federalist through Github, federalist checks his Organization
> ID (but only upon login).

> Remove the user from organization, or leave organization
> 4) Try to create or delete the site. Federalist doesn't know that this user has no
>    permissions, and will allow him to use functions.

## 6. Residual data, cache, and logon management

- **AUTH-249798** (Legal Robot, low, resolved) — stale cookies still open the Intercom support
  chat after logout: "he can still use that session cookies to access the chat".
- **AUTH-232306** (Weblate, low, resolved, supplemental pass) — cookie expiration "set to future
  date" on session and CSRF cookies; body cites OWASP OTG-SESS-002.
- **AUTH-7909** (Localize, resolved) — back-button after logout shows browsed pages; verbatim:
  "Logging out from an application does not clear the browser cache of any sensitive
  information that have been stored." **AUTH-158270** (Certly, resolved) is the same finding
  with a link to 7909 in the body.
- **AUTH-11722** (Coinbase, informative) — simultaneous logon leaves the older session alive
  when a second user logs in from the same browser.

## 7. Doctrine

- **This class rarely pays directly** — $200 json + $200 list on HackerOne's own program
  (2013–2014 era) and $770/6 list across everyone else, 18 of 26 rows unpaid. Report it as the
  *second half of a chain*, not as the headline: the corpus's own 250688 says "can be dangerous
  in combination of others (like XSS, or malicious access to the user account)".
- **Where it does pay**: (a) self-claimed criticals on internal/partner surfaces (222082,
  226712) where logout implies a security boundary; (b) backdoor/re-bind cookie semantics
  (250688); (c) authorization-state staleness after org-membership changes (245833) — that one
  is really a JWT/session-as-identity-cache design bug.
- **The universal test**, from the bodies: capture request → logout → replay → check for a
  live authorized response (353); then from a second browser after password change (145430);
  then after org-membership revocation (245833).
- Modern hardening (P4): session revocation lists, `__Host-` cookies, refresh-token rotation —
  the 2014-era "cookie still works after logout" report is dead on mature programs; on young
  SaaS it still lands as Low.
