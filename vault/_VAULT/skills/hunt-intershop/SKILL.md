---
name: hunt-intershop
description: >-
  Hunt Intershop Commerce Management (ICM) + PWA storefronts. Covers detecting the
  Angular "intershop-pwa" shell, finding the ICM REST backend that the PWA talks to
  (usually a separate host from the WAF-fronted storefront), the
  /INTERSHOP/rest/WFS/{site}/{app}/{resource} URL scheme, the site-vs-application
  discovery oracle, anonymous basket/token semantics, the public configurations
  endpoint, ACAO:* that is NOT a CORS finding, custom REST extensions enumerated out
  of the bundle, the PWA's only dangerous HTML sinks, cXML/OCI PunchOut login params
  (sid/access-token, HOOK_URL/USERNAME/PASSWORD), and the authenticated IDOR matrix
  to run once a test account exists. Use whenever a target is a B2B/B2C shop, a
  multi-country commerce estate, or a storefront that fingerprints as Intershop.
---

# Hunt Intershop (ICM REST + PWA storefront)

Intershop powers a lot of enterprise B2B commerce. The storefront and the commerce
backend are **two different hosts with two different protection levels**, and the
backend is where all the interesting API surface lives. Most researchers only look at
the WAF-fronted storefront, conclude "blocked", and leave.

## 1. FINGERPRINTS

| Signal | Meaning |
|---|---|
| `ng-app-id="intershop-pwa"` in the served HTML | Angular Intershop PWA (SSR). Definitive. |
| `/INTERSHOP/rest/WFS/...`, `/INTERSHOP/web/WFS/...`, `/INTERSHOP/static/WFS/...` in JS | ICM REST/web/static tiers |
| Any reference to `pwa-ish-demo.test.intershop.com` | PWA bundle built from Intershop's demo |
| `Server: Apache` (not nginx) + `X-Permitted-Cross-Domain-Policies: none` on API responses | ICM origin directly |
| `authentication-token: encryption0@PBEWithMD5AndTripleDES:...` response header | ICM anonymous basket token |
| `/rest;loc=<locale>/` path segment | ICM REST application with locale matrix param |
| `dummyClientSecret` / `dummyClientId` in the bundle | PWA OAuth public-client placeholder — NOT a leaked secret |
| `punchout`, `cxml`, `oci` chunks/routes | PunchOut procurement integration (sid + access-token / HOOK_URL) |

**Do not confuse with SAP Commerce/Spartacus.** Both are Angular commerce SPAs with
`Authorization: Bearer ${token}` and an OAuth `access-token` query param. Spartacus says
`dummyClientSecret` too. The tell is the API path: Intershop = `/INTERSHOP/rest/WFS/`;
Spartacus = `/occ/v2/<baseSite>/`.

## 2. FIND THE BACKEND (the step everyone skips)

The PWA's API base is injected at runtime and is frequently **a different hostname** than
the storefront, sometimes not in your recon list at all. Get it from live browser traffic,
not from grep:

```python
# isolated Firefox + Marionette -> read the resource timeline (sync, no promise needed)
m.execute_script("return performance.getEntriesByType('resource')"
                 ".map(r=>r.initiatorType+' '+r.name).join('\\n')")
```
Filter for `xhr|fetch|intershop|rest`. That yields lines like:

```
xmlhttprequest https://<backend-host>/INTERSHOP/rest/WFS/<site>/rest;loc=en_US/<resource>
```

That backend host is now your primary target. Check whether it is CF-fronted at all —
very often the storefront is behind Cloudflare while the ICM origin answers plain curl.

## 3. URL SCHEME + THE SITE/APPLICATION ORACLE

```
/INTERSHOP/rest/WFS/{site}/{application}/{resource}
```

`{site}` is a base-site name (e.g. `<brand>-Site`, `<brand>-corporate-Site`);
`{application}` is `rest` for the REST API or `-` for the classic application.

Three response shapes give you a free enumeration oracle — use it instead of wordlists:

| Response | Means |
|---|---|
| `404` + `<TITLE>System status</TITLE>` (~150 B HTML) | **unknown site** |
| `404` + `Not Found (Application '<app>' not found in context of the site '<site>'.)` | **site EXISTS**, that app is not published there |
| `401 Unauthorized` (12 B text/plain) | app EXISTS but requires authentication |
| `200` + JSON | open resource |

So one request per candidate name tells you whether the site exists AND whether the app
is public. Enumerate both axes; a corporate/marketing site is usually public while the
actual B2B shop site requires auth.

## 4. RESOURCE MAP (what is usually open vs gated)

Open on a corporate site (observed): `categories` (may be empty if the catalogue lives in
a CMS, not ICM), `suggest?searchTerm=`, `cms/includes/...`, `configurations`,
`rzlocalizations?searchKeys=`, `<custom-extension>`.

Gated (`401 Authentication or token of registered user required`): `customers/-`,
`privatecustomers/-`, `customers/-/users/-`, `orders`, `personalization`,
`customers/-/baskets`, `baskets/{id}`.

Enumerate **custom extensions** out of the bundle — these are the client's own code and
the least-reviewed:
```bash
grep -ohE 'apiService\.(get|post|put|delete)\("[a-zA-Z0-9/_.:;{}$-]{1,60}"' main*.js | sort -u
```

## 5. ANONYMOUS BASKET — semantics, and why it is usually NOT a bug

```bash
curl -sk -X POST "$B/baskets" -H 'Content-Type: application/json' \
     -H 'Accept: application/vnd.intershop.basket.v1+json' -d '{}' -D -
```
`201` returns `Location: .../baskets/<id>` **and** an `authentication-token` header.
That token is the authorization for the basket. Verify before claiming IDOR:

- no token -> `404 basket.not_found.error`
- forged/garbage token -> `401 Unable to decode token`
- correct token -> `200`

If the matrix looks like that, **authorization is correctly enforced — report nothing.**
This is the single most common false IDOR on ICM.

Content negotiation matters on several resources: `configurations` needs
`Accept: application/vnd.intershop.configuration.v1+json`, `productprices`/`rz-stock`
behave differently, and a wrong/HTML Accept gets `406 Not Acceptable` (not an error worth
reporting).

## 6. CORS — ACAO:* is a NON-FINDING here

ICM sends `Access-Control-Allow-Origin: *` plus
`Access-Control-Allow-Headers: authorization, authentication-token, X-Captcha-Token,
UserOrganization, Content-Type` on every response, including preflight.
That wildcard forbids credentialed (cookie) reads, and the PWA keeps tokens in
localStorage/sessionStorage which a cross-origin page cannot read. Record it as an
architecture observation at most. Do not file it.

## 7. XSS — where the PWA can and cannot fire

- Angular escapes interpolations; a plain `<payload>` in `?searchTerm=`, `?errorKey=`,
  `?returnUrl=` etc. will NOT execute. Do not report reflection.
- The only genuinely dangerous sinks in a stock PWA bundle are:
  `sanitizer.bypassSecurityTrustHtml(...)` for icon SVG rendering (static),
  `props.safeHtml ? bypassSecurityTrustHtml(field.template)` (CMS field flag), and
  `insertAdjacentHTML("afterbegin", ...)` in the `ishServerHtml` directive (SSR fragment,
  not URL-derived). Confirm which of these exist and whether your input can reach one.
- ICM REST error reflection is real but inert:
  `?productFilter=<script>` -> `400 text/plain "Bad Request (productFilter <script> ... is undefined.)"`
  with `X-Content-Type-Options: nosniff`, and `Accept: text/html` returns `406`.
  Reflected-but-text/plain is **not** XSS. Same for `suggest` (JSON).
- Real XSS on this stack usually needs an authenticated write (profile/company/approver
  fields), so pair it with the IDOR matrix in §9.

## 8. PUNCHOUT LOGIN PARAMS (check, then close)

The PWA's auth interceptor logs in from URL params when they are present:
`?sid=<x>&access-token=<token>` (cXML) or
`?HOOK_URL=<url>&USERNAME=<u>&PASSWORD=<p>` (OCI).

Test whether it is even enabled by hitting the punchout route; a disabled feature returns
something like `/en/error?error=feature-deactivated&value=punchout`. If it IS enabled, the
realistic findings are (a) credentials-in-URL for the OCI variant, (b) login-CSRF via
`access-token` (victim logged into attacker's account). Both need a valid account to
demonstrate, so they belong with §9 rather than as a blind claim.

## 9. AUTHENTICATED IDOR MATRIX (needs one test account)

PWA routes tell you exactly which objects are ID-addressable:

`users/:B2BCustomerLogin`, `users/:B2BCustomerLogin/{profile,budget,roles}`,
`cost-centers/:CostCenterId`, `cost-centers/:CostCenterId/buyers`,
`requisition/:requisitionId` (`approver/`, `buyer/`), `quote/:productSku`,
`baskets/{id}`, `orders/{orderNo}`.

Method: two accounts, both directions, swap the identifier at every level. For `users/:login`
the swap is a *login string*, which is far more likely to be unvalidated than a GUID.

## 10. PITFALLS

- Registration/login may be broken by an **empty OAuth `client_id`**
  (`auth.<tld>/authorize?...&client_id=&redirect_uri=.../loading` -> Auth0 error page).
  That blocks self-registration and therefore authenticated IDOR. Say so explicitly and ask
  the operator for a test account instead of claiming the surface is clean.
- A site can exist yet serve an empty catalogue because products live in a CMS
  (Contentful/Sitecore). Empty `{"elements":[]}` is not "no products configured wrong" —
  it means you are querying the wrong tier.
- `productFilter` on `/products` takes *named* filters; an unknown name returns the
  reflection error above. Don't burn time fuzzing filter syntax.
- Some base sites are **IP-allowlisted by design** ("You can only order from an office").
  Do not attempt to bypass; note it as an intentional control.
- Sibling "backend" hostnames found in the bundle (`*-int-*`, `*-pre-*`) often have no
  public DNS. That is internal-only, not a finding and not a takeover.
- Deeper session detail and the exact observed response codes: see
  `references/intershop-session-notes.md`.
