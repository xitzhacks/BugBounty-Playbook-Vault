---
title: "Core Param Redirects — the endpoint+param lane, suffix/dot tricks, stored redirects"
type: playbook
category: core-param-redirects
cwe: "CWE-601"
source_count: 50
full_bodies_available: 50
corpus: "h1.security.nathan.sx roster (198 rows), bodies via hackerone.com/reports/<id>.json"
list_accessed: "2026-10-28"
note: "Anchor bodies: RDIR-2622 (Slack, $200 list), RDIR-125791 (uber.com root-path, $3,000 json), RDIR-145306 (Veris email-link redirect), RDIR-161991 (Shopify last_shop cookie). Claims trace to bodies read 2026-10-29."
---

# Core Param Redirects — the endpoint+param lane

## 1. Overview

Fifty corpus cases: the classic find — a parameter the server copies into `Location:` without
validating the destination. Alone this is Low (phishing); the corpus shows exactly two ways it
gets paid anyway: (a) the redirect is reachable on a **trusted surface** (login flows, emails,
admin panels) so the URL is brand-trusted; (b) the redirect target carries **state**
(authenticity_token POSTs, OAuth params). Four sub-families:

| Family | Cases |
|---|---|
| Plain param → Location | 2414, 2622, 2731, 4549, 6035, 12964, 13553, 6564, 22142, 141355, 131082, 131728, 113112, 258632, 188266, 153652, 145306, 163272, 217430, 231760 |
| Path-redirect family (// and dot-segments) | 39198, 45516, 125000, 125791, 119236, 123625, 160047, 163124, 169759, 214034, 215970, 211213, 57163, 52035, 77221, 114529 |
| Login/after-auth redirect params | 6357, 39631, 16718, 55546, 103772, 101962, 161991, 129091, 246897, 143265 |
| Suffix/host-trick variants on core params | 55546, 103772, 246897, 119236 (overlap rows counted once per module) |

**Case-ID scheme: `RDIR-<report id>`.**

## 2. The anchor — RDIR-125791 (uber.com, $3,000 json — class-topping fetch)

The whole body:

> Hello,
> To reproduce this issue, visit this URL: https://www.uber.com/en//example.com/
> This URL will redirect at [example.com](https://example.com/).

Five lines, $3,000. Lessons:

1. **Root-path redirects on the apex domain are the highest-trust lane** — the victim's address
   bar starts `https://www.uber.com/…` the entire way. No parameter is even needed: the *path*
   is the parameter (`/en//example.com/`).
2. **The title claims XSS; the body demonstrates only the redirect.** Bounty follows the
   chain-claim, evidence carries the redirect. The agent must do what this reporter didn't:
   capture the redirect landing with a payload, or report the redirect alone.
3. Double-slash after a path segment (`/en//example.com`) is a different validator path than
   double-slash at the root (`//example.com`) — test both positions.

## 3. The suffix/dot trick cluster (login + checkout params)

- **RDIR-55546 (ecommerce.shopify.com, $500 json)** — the canonical dot-suffix:
  > http://ecommerce.shopify.com/accounts?found_email=true&return_to=.mx%2F&user[email]=[REDACTED_EMAIL]
  > When victim enters the password he is redirected to http://ecommerce.shopify.com.mx/
  > This com.mx can be changed to multiple like .es .tw etc
- **RDIR-103772 (*.myshopify.com, $500 list)** — same trick on checkout_url:
  > Send this to victim:
  > http://sehyoginfoshop.myshopify.com/account/login?checkout_url=.np
  > Now when our victim logs in,
  > He will be redirected to
  > https://sehyoginfoshop.myshopify.com.np/
  > Which is not a shopify domain.
  >
  > Fix: While redirecting Use <shop-name>"/"$checkout_url instead of <shop-name>$checkout_url
- **RDIR-39631 (fabric.io, $280 json)** — @-authority trick on the login redirect:
  > https://www.fabric.io/login?redirect_url=@<payload>
  > for example : https://www.fabric.io/login?redirect_url=@google.com
- **RDIR-211213 (Nextcloud XMPP)** — combined slash+;@:
  > https://xmpp.nextcloud.com///;@www.google.com

Agent lesson: when a login/checkout URL ends in the domain (`shopify.com.mx`, `shop.np`),
the validator usually concatenates instead of comparing. Probe `=.mx/`, `=.np/`, `=@evil.com`,
`=;@evil.com` — each is a different parser bug (suffix-join, authority-confusion).

## 4. The path-redirect family (//, dot-segments, IP-integer)

- **RDIR-39198 (admin.c2fo.com)** — dot-segment, Location echo in body:
  > GET ///www.google.com/%2e%2e HTTP/1.1
  > HTTP Response:
  > Location: //www.google.com/%2e%2e/
- **RDIR-125000 (m.uber.com, $500 json)** — same shape on a paid endpoint:
  > `https://m.uber.com//youtube.com/%2F..`
  > Location: //youtube.com/%2F../
- **RDIR-57163 (hackerone.com)** — IP-integer host conversion, plus the filter asymmetry:
  > Here is the PoC that redirects to example.com IP address: https://hackerone.com/%2F1572395042
  > https://hackerone.com//hackerone.com - works
  > https://hackerone.com//hackerone1.com - doesn't work
- **RDIR-119236 (uber.com, $500 json)** — the https/http asymmetry (sic preserved):
  > But remove the `https://` and now you will be able to reach any website with the IP address.
- **RDIR-123625 (marketplace.informatica.com)** — proxy rewrite creates the redirect:
  > All requests containing a single quote: ' are met with a 302 redirect to the same URL, minus
  > the single quote. As the Location header uses a protocol-relative URL, this can be abused
  > to redirect people to arbitrary external sites.
- **RDIR-215970 (GitLab import, medium)** and **RDIR-214034 (GitLab todos host=)** — the
  `redirect_to params.merge(..)` anti-pattern the reporter pinned to source lines:
  > Bug is in Dashboard::TodosController line 10
  > Likey (sic)
  > Same bug in Projects::IssuesController line 32

## 5. Trusted-surface redirects

- **RDIR-145306 (sandbox.veris.in)** — the redirect rides a company email:
  > user will be redirected to evil website that comes from YOUR COMPANY email telling the user
  > to continue the registeration process . (sic)
  > redirect to his OWN website , listening on port , jacking the verification code !
- **RDIR-161991 (shopify.com/admin, $500 list)** — cookie-trusted redirect, team-written body:
  > Because input validation was missing, any `last_shop` value would be accepted, thereby
  > allowing an open redirect to any domain.
- **RDIR-143265 (zomato, informative)** — token-gated but token-reusable:
  > https://www.zomato.com/redirect?u=http%3A%2F%2Ftest.com&t=38dc43d5f007f4c5d974f6c74f065158&g=user-profile-website
  > The presence of parameter t which is being passed through the request is verified but same
  > value can be reused to any unauthenticated or authenticated user
- **RDIR-131082 (ownCloud pdfviewer, $150 json)** — unauthenticated, download-button trigger:
  > A non authenticated user can be easily tricked into following one of the following links

## 6. Agent execution template

```text
P0 — inventory: crawl + dork (site:example.com inurl:go|return|url|redirect|next)
     dork list from zseano guide §1 (blogs-index): go, return, r_url, returnUrl, returnUri,
     locationUrl, goTo, return_url, return_uri, ref=, referrer=, backUrl, returnTo, successUrl
P1 — cheapest-first per param:
     1. full URL        ?p=https://evil.com
     2. protocol-relative?p=//evil.com
     3. dot-segments    ?p=//evil.com/%2e%2e
     4. path position   /en//evil.com/  and  //evil.com
     5. suffix-join     ?p=.mx/   ?p=.np/
     6. authority       ?p=@evil.com   ?p=;@evil.com   ?p=[REDACTED_EMAIL]
     7. IP-integer      ?p=/1572395042 (DNS-to-int of your host)
P2 — read the Location: header. If browser-only divergence (IE suffix rules), name the browser.
P3 — escalate (see modules 03/06): does the redirect surface carry tokens, POSTs, or scripts?
P4 — re-test after fix: the corpus shows five fixed-then-rebroken clusters (module 04).
```

## 7. Validation gates

1. **Location: shows your domain** on a 30x from the target's origin — screenshot the raw header.
2. **No user action required**: GET-reachable, or name the exact click that triggers it (login,
   "Okay" button, download button).
3. **Trusted-URL claim proven**: paste the full victim-visible URL; show the target domain stays
   in the address bar until landing.
4. If severity is claimed above Low, the chain evidence must be attached (module 03/06 gates).

## 8. Adjacency

- Suffix-join tricks belong with Host-header confusion (module 05) — same "trust the prefix"
  psychology, different injection point.
- `redirect_to params.merge()` reports feed the framework-doctrine note in the playbook P2.

## 9. Archive-label honesty

- 18 of these 50 rows carry json bounties, 32 carry list figures; labels are in the register.
- 4 rows are informative with no fix status beyond substate (2414, 2731, 4549, 6035 — the Slack
  early era); their technique value is the parameter inventory, not the impact.
- 231760 is video-only (body: "Sir I make a video for clear understand. Watch that video." (sic))
  — kept for disposition honesty, no technique content.

## 10. Cross-references

- Module 03 for the token-carrying redirects that make this class pay.
- Module 04 for every fixed-then-rebroken case (the fixes here were attacked within weeks).
- `../CSRF/06_GET-State-Changes.md` for the GET-request state-change discipline.
