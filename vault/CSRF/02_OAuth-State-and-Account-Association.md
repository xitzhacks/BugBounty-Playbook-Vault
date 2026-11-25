---
title: "OAuth State & Account Association CSRF — connect, authorize, attach"
type: playbook
category: oauth-state-association
cwe: "CWE-352"
source_count: 10
full_bodies_available: 11
corpus: "h1.security.nathan.sx roster (229 rows), bodies via hackerone.com/reports/<id>.json"
list_accessed: "2026-10-28"
note: "Anchor body: CSRF-215381 (Periscope, $2,520 list-stated — the class's largest figure). Claims trace to bodies read 2026-10-28."
---

# OAuth State & Account Association CSRF — the `state` parameter is the whole defense

## 1. Overview

Ten corpus cases ride OAuth/OIDC/OpenID flows. The pattern is uniform: an **authorization or
association step that changes server-side account state** (attach identity, authorize app,
replace connected account) with no `state`/CSRF token/no Origin check. The attacker completes
the flow *as himself*, intercepts the redirect, and feeds the victim the final leg — the victim
browsers' request does the binding.

**Case-ID scheme: `CSRF-<report id>`.**

| Flow shape | Cases | Payload |
|---|---|---|
| Login via OAuth (session establishment) | 2228, 118737, 117195 (module 01) | attacker's `code`+`state`/`oauth_token`+`verifier` to victim |
| App authorization (token grant) | 215381, 253128 | forged authorize POST |
| Social connect/attach (identity binding) | 104931, 111218, 55911, 225100, 225653 | attacker's callback URL to victim |

## 2. The anchor — CSRF-215381 (Periscope, $2,520 list-stated)

The vulnerable request is the *authorize* POST itself, verbatim:

```http
POST https://www.periscope.tv/oauthAuthorize HTTP/1.1
Content-Type: application/x-www-form-urlencoded
Cookie: sid=[...]
client_id=████&redirect_uri=https%3A%2F%2Fgetmevo.com%2Foauth%2Fperiscope?abc
```

> As one can see, there is no CSRF token or Origin validation.

Impact, stated with demonstrated endpoints:

> At minimum, I found endpoints that allow creating a broadcast
> (`https://public-api.periscope.tv/v1/broadcast/create`), tweeting it
> (`https://public-api.periscope.tv/v1/broadcast/publish`) and deleting a broadcast
> (`https://public-api.periscope.tv/v1/broadcast/delete`)

Agent lessons:

1. **The forgery is a form, not a redirect** — `redirect_uri` is *attacker-chosen* in the
   forged POST, so the victim's browser delivers the authorization `code` straight to
   `attacker.com`. This is the strongest OAuth-CSRF shape (code theft, not just state confusion).
2. **Impact = enumerate the granted scope.** The body proved real API powers ("full access…
   at minimum…") instead of arguing hypothetically — that is the $2,520 narrative.
3. The `?abc` suffix on `redirect_uri` is a probe artifact worth copying: it tests whether
   strict URI matching is enforced on the authorize endpoint.

## 3. Identity-binding — the Pinterest/Shopify cluster (CSRF-104931, $500 list)

The six-step chain is the canonical connect-CSRF proof, verbatim:

> 1. Victim(mshop2-2) already has Pinterest account connected.
> 2. Attacker(mshop3-2) doesn't have Pinterest account connected and attempts to connect a
>    Pinterest account.
> 3. Attacker authorize the shopify app to connect to his Pinterest account.
> 4. Attacker intercepts the redirection back to `pinterest-commerce.shopifyapps.com` and drop
>    the request. Attacker also captures the URL, e.g.
>    `https://pinterest-commerce.shopifyapps.com/auth/pinterest/callback?code=d0c18854a3359866774d479614081453d235962f`
> 5. Attacker induces Victim to load the above captured URL.
> 6. Victim's connected Pinterest account has been replaced with the attacker's Pinterest account.

and the fix line names the missing primitive:

> * Make use of the state parameter in OAuth, which is used to prevent CSRF, when connecting to
>   Pinterest.

Note the *replacement* semantics — even an already-connected victim loses their binding
(step 1 exists precisely to prove replacement works). **CSRF-111218** is the same bug in the
same program's second integration ("attach with no state"). **CSRF-225100** (Weblate, Facebook
connect) and **CSRF-225653** (Weblate, Ubuntu OpenID association → takeover) repeat the shape
across providers.

## 4. State parameter fixed / unvalidated

- **CSRF-55911 (Shopify FB store, $500 list)** — the *opposite* failure: a `state` parameter
  exists but is **fixed for every authorization** (state-fixation). Same callback-hijack proof;
  the fix is per-request state generation. Agent probe: run the connect flow twice, diff the
  `state` values — identical = fixation.
- **CSRF-118737 (thisdata, Google OAuth)** — login-CSRF shape, stated in one line:
  > Attacker directs victim to `/oauth/redirect?state={attacker's state}&code={attacker's code}`
  > Victim is now logged in as attacker
  > … state parameter is solution for this but in this case state parameter is [not validated
  against the session]
- **CSRF-2228 (Phabricator, Twitter OAuth 1.0A, $300 list)** — the pre-OAuth2 artifact, and its
  fix note is the module's doctrine for 1.0A flows:
  > Although the Twitter flow still uses OAuth 1.0A, which has no `state` parameter as in OAuth
  > 2, it is still possible to prevent this type of attack by setting an additional parameter in
  > the `oauth_callback` value.
  Attack steps verbatim: *"3. Attacker records and drops redirection to Phabricator (in order
  not to consume token) 4. Attacker directs victim to
  `/auth/login/twitter:twitter.com/?oauth_token=[REDACTED_SECRET]"*

## 5. Execution template

```
STEP 1 — inventory association surfaces:
  /connect/<provider>, /attach, /oauth/authorize, /oauthAuthorize,
  /auth/<provider>/callback, settings "connected accounts" panel.
  record: does the authorize/attach request carry state? token? Origin check?

STEP 2 — fixation diff:
  run the connect flow twice (same account): diff state/nonce/token values.
  identical → state-fixation (55911). absent → no-state (104931).

STEP 3 — attacker-completes-first:
  with TWO accounts (A victim, B attacker):
  B completes OAuth → intercept callback → capture full URL (code/state) → DROP it.
  feed the captured URL to A's browser (iframe/img/navigate).

STEP 4 — land and verify:
  A's account settings show B's identity bound (screenshot both browsers).
  for app-authorize: attacker app receives the code (check your redirect listener).

STEP 5 — impact step:
  what the binding grants: data write on behalf of victim (Pinterest commerce),
  full API (Periscope broadcast create/publish/delete), session establishment
  (118737). Demonstrate ONE real granted action.
```

## 6. Validation gates (all must pass)

1. **Two-account, two-browser proof** — binding change visible in victim's settings UI.
2. **Captured callback URL in evidence** (full query string; redact `code` tails).
3. **Fixation probe documented** when `state` exists-but-fixed (55911 pattern).
4. **Grant-scope enumeration** for authorize-lane cases (215381 pattern: name the API powers).
5. **No token consumption error** — dropped redirect must not 400 on replay in the victim's
   browser (if it does, the flow has one-time codes — report dies, gate K2).
6. **State restored** — disconnect bound accounts on both test accounts after proof.

## 7. Adjacency

- **Open redirect in `redirect_uri`** — validates the OAuth lane's redirect_target handling;
  Vault/Open-Redirect companion (342-row build pending).
- **Subdomain takeover at redirect_uri** — modern chains (SAML/OIDC ATO) — hunt-oauth skill's
  redirect_uri matrix; bibliographic here (post-roster).
- **CSRF-171398 (H1, SSO)** — chains SAML login-CSRF + open redirect + self-XSS into one
  report; shows the era triage shape for multi-bug bundles (see module 03 §3).

## 8. Archive-label honesty

- CSRF-215381's $2,520 is **list-stated** (JSON `bounty_amount` absent — `has_bounty` true,
  amount withheld, same condition as XXE-248668).
- CSRF-253128 (Rockstar SocialClub, $600) is **metadata-only** — "CSRF that steals private
  token" High claim recorded from title/team columns; no technique content, no quote.
- CSRF-223367 (Weblate) was initially parked in this module before its body read reclassified
  it to module 03 (identity-binding via activation link, not OAuth) — cross-vault note kept in
  both registers.

## 9. Cross-references

- Module 01 — OAuth login CSRF is the modern variant of 547's email-confirm login CSRF.
- Module 03 — what a successful binding becomes (ATO).
- `hunt-csrf` skill — Scenario B (OAuth CSRF) modern matrix; `hunt-oauth` skill — redirect_uri
  abuse; [`references/blogs-index.md`](references/blogs-index.md) — modern citations.
