---
title: "OAuth & SSO Redirect Flows — redirect_uri validation, error-redirects, social-login next=, SAML"
type: playbook
category: oauth-sso-redirect-flows
cwe: "CWE-601"
source_count: 13
full_bodies_available: 13
corpus: "h1.security.nathan.sx roster (198 rows), bodies via hackerone.com/reports/<id>.json"
list_accessed: "2026-10-28"
note: "Anchor bodies: RDIR-26962 (rfc6749 error-redirect, $3,000 json), RDIR-2575 (Slack OAuth redirect_uri suffix, $100 list), RDIR-55525 (Shopify invalid_scope, $500 json). Claims trace to bodies read 2026-10-29."
---

# OAuth & SSO Redirect Flows — when the auth flow itself is the redirector

## 1. Overview

Thirteen cases where the redirect happens *inside an authentication protocol* — OAuth
`redirect_uri`, social-login `next=`, SAML `sign_in`, or the spec-mandated error redirect.
These pay better than core params because a poisoned OAuth redirect can carry codes and tokens
(module 03) and because validators exist here — so the finds are **bypasses of real filters**.

| Family | Cases |
|---|---|
| OAuth redirect_uri validation gaps | 2575, 26962, 55525, 7900, 140432 (token half in module 03) |
| Social-login next= (Weblate cluster) | 223326, 223718 (dup), 224317, 238117, 91332 |
| SAML sign_in lane | 178345, 171398 |
| App-callback params | 226408 |

## 2. The anchor — RDIR-26962 (open redirect in rfc6749, $3,000 json)

The corpus's most-cited OAuth finding: the **spec-mandated error redirect** is itself an open
redirector, verbatim:

> If the request fails due to a missing, invalid, or mismatching
>    redirection URI, or if the client identifier is missing or invalid,
>    the authorization server SHOULD inform the resource owner of the
>    error and MUST NOT automatically redirect the user-agent to the
>    invalid redirection URI.

> Namely I prepare a url that is in this form:
> http://victim.com/authorize?response_type=code&client_id=bc88FitX1298KPj2WS259BBMa9_KCfL3&scope=WRONG_SCOPE&redirect_uri=http://attacker.com
> and this is works as an open redirector.

> I have notified also this issue to the OAuth mailing list.
> See also http://www.ietf.org/mail-archive/web/oauth/current/msg13367.html

Agent lessons:

1. **Register a client, then send a bad scope** — if the error path redirects to your
   `redirect_uri`, the provider is a public redirector. The RFC's "MUST NOT automatically
   redirect" to an *invalid* redirection URI is doing no work here because the URI is *valid*
   (yours) — the redirect is spec-compliant and still attacker-chosen.
2. The reporter escalated by process, not payload: notified the IETF list. Impact framing =
   "every rfc6749-strict provider is affected" — that framing is what carries $3,000 on a
   self-registered client.
3. Fix framing from the body: "A solution would be to return error 400 rather than redirect to
   the redirect URI or always show the consent screen (at least once until the app is accepted
   by the user) even in case of wrong parameter rather than redirect..."

## 3. redirect_uri validator gaps

- **RDIR-2575 (Slack, $100 list)** — suffix acceptance:
  > Surprisingly If I point the redirect_uri to http://www.google.com.mx (see .mx suffix) the
  > endpoint will be accepted, infact endpoint like http://www.google.com.attacker.com will be
  > accepted too. The server doesn't block these suffix attacks.
- **RDIR-55525 (Shopify, $500 json)** — the invalid-scope redirect with signed params:
  > This will redirect with an error to ...
  > <https://www.facebook.com/abc?error=invalid_scope&hmac=07657fed...&shop=prans.myshopify.com&signature=...>
  > Simple patch :
  > ===========
  > Only a error should be shown and no redirection should take place so as to protect users.
- **RDIR-7900 (respond.ly)** — parameter-controlled post-auth redirect:
  > https://app.respond.ly/_oauth/twitter/?requestTokenAndRedirect=https://hackerone.com
  > Recommendation: make sure the `requestTokenAndRedirect` paramater only accepts hosts on
  > whitelisted domains. (sic)
- **RDIR-226408 (Shopify Alexa app, low)** — third-party app callback accepts any `shop=`.

## 4. Social-login next= — the Weblate cluster

Four resolved rows + one duplicate, all `next=` on auth endpoints:

> https://demo.weblate.org/accounts/login/github/?next=///google.com
> After authenticating, the user will be immediately redirected to the attacker-specified
> target. I believe this affects all third-party authentication providers on the Weblate
> platform. (RDIR-223326)

> ### Signing in via Facebook :
> + https://hosted.weblate.org/accounts/login/facebook/?next=///evil.com
>
> ### Signing in via Gmail :
> + https://hosted.weblate.org/accounts/login/google-oauth2/?next=///evil.com
>
> ### Signing in via Github:
> + https://hosted.weblate.org/accounts/login/github/?next=///evil.com
>
> ### Signing in via Bitbucket:
> + https://hosted.weblate.org/accounts/login/bitbucket/?next=///evil.com
>
> ### Signing in via Gitlab:
> + https://hosted.weblate.org/accounts/login/gitlab/?next=///evil.com

(RDIR-223718)

Disconnect flows too (RDIR-224317, 238117): `accounts/disconnect/google-oauth2/<id>/?next=`.
**Triple-slash is the working form here** — test `///`, `//`, `/\/` separately; validators
handle them differently (compare module 04's `/%2F%2F` and `/..//` rows).

- **RDIR-91332 (imgur, informative)** — `register/thirdparty/facebook?redirect=` post-registration.

## 5. SAML sign_in lane (HackerOne)

- **RDIR-171398 (low)** — the triple bug chain, verbatim structure:
  > 1) Information Leak — An attacker can use Logout CSRF + Login CSRF against a victim to steal
  > all information sent by the victim to the HackerOne website while using the malicious
  > session, including confidential bug reports.
  > 2) Open Redirect — Since the SSO-SAML login flow can be started automatically
  > (`GET https://hackerone.com/users/saml/sign_in?email=███`) by an attacker and it redirects to
  > external URLs, the attacker can redirect the user to anywhere.
  > 3) Self-XSS Possible Exploitation — Some stored Self-XSS's (internal areas accessed just by
  > the victim, etc.) can be exploited through Login CSRF.
  Plus the config-domain footnote: `hackerone..com`, `hackerone.com.`, `.hackerone.com` —
  "[REDACTED_EMAIL] would redirect the victim to the attacker external login flow".
- **RDIR-178345 (low)** — the patch-bypass one day later:
  > https://hackerone.com/users//saml/sign_in?email=[REDACTED_EMAIL]&remember_me=true (Without
  > external warning page)
  → double-slash in the *path* (`users//saml`) skips the External Link Warning interstitial.

## 6. Agent execution template

```text
P0 — inventory: find /oauth/authorize, /dialog/oauth, accounts/login/*, /saml/sign_in,
     /auth/<provider>/callback; note every registered app you can create.
P1 — redirect_uri validator matrix (self-registered app):
     1. exact-match    redirect_uri=https://trusted.com/callback (baseline)
     2. suffix         https://www.google.com.mx / https://www.google.com.attacker.com
     3. path-position  https://trusted.com//evil.com
     4. error-redirect scope=WRONG_SCOPE&redirect_uri=https://attacker.com
     5. response_type  code→token (module 03 hash smuggling)
P2 — social login next= matrix: ///, //, /\/, @-authority, single-slash scheme (http:/)
P3 — SAML/SSO lane: does sign_in auto-start from GET? does it redirect externally?
     does the interstitial (warning page) catch it? try path double-slash bypass.
P4 — chain: capture what lands in the attacker-controlled redirect (module 03 gates).
```

## 7. Validation gates

1. The redirect fires **inside the protocol flow** (log the authorize → Location sequence), not
   on a static link.
2. For error-redirect findings: the error is *triggered by your chosen parameter* while
   `redirect_uri` stays attacker-controlled — show both.
3. For validator gaps: show the accepted-vs-rejected pair (the 2575 shape).
4. Interstitial bypass (178345): show both URLs — with and without the warning page.

## 8. Adjacency

- Token capture completes these chains — module 03 is the escalation half.
- Login-CSRF pairing (171398) cross-references `../CSRF/01_Login-Signup-Logout-CSRF.md`.
- RFC6749 error-redirect applies to the `../SSRF` vault's OAuth lanes too.

## 9. Archive-label honesty

- 2 of 13 rows json-bountied ($3,000 + $500), 1 list ($100), 10 untagged — this lane pays through
  chaining, not the redirect itself.
- 223718 sits as **duplicate** in the register (of 223326) — the cluster's spread is still
  five-provider coverage from one platform.

## 10. Cross-references

- Module 03 (token capture), Module 04 (the fix-bypass lane), `../CSRF/02_OAuth-State-and-Account-Association.md`.
