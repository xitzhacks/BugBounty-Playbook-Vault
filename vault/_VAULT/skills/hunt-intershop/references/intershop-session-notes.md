# Intershop session notes — observed behaviour (authorized VDP engagement, 2026)

Concrete request/response records backing `hunt-intershop`. Target identity removed where it
does not matter; keep the response shapes, they are the reusable part.

## A. Storefront vs backend split

- Storefront `www.<target>` = Angular `intershop-pwa`, SSR, **Cloudflare-fronted**.
  Plain curl -> `403`, `cf-mitigated: challenge`, `<title>Just a moment...</title>`, ~5.6 KB.
  With a Firefox UA + `Sec-Fetch-*` + `--compressed` -> **200, 36,914 B** of real SSR HTML.
  See `recon-pitfalls` §9 and its `scripts/cf_curl.sh`.
- Backend `webshop-prod-live-backend.<target>` = ICM origin, `Server: Apache`,
  **no Cloudflare**, answers plain curl. This is where every useful request went.
- Other hosts leaked by the bundle: `webshop-int-live-backend`, `webshop-pre-live-backend`
  -> no public DNS (internal).
- CNAME of the prod backend: `ish34-<customer>icmprod-lv.westeurope.cloudapp.azure.com`.
  All eight ICM VMs (prod/pre/int/inta x lv/ed) resolve — relevant to takeover triage.

## B. Site / application oracle (verbatim responses)

```
GET /INTERSHOP/rest/WFS/<brand>-Site/rest;loc=en_US/categories
404  81 B  Not Found (Application 'rest' not found in context of the site '<brand>-Site'.)
        -> site EXISTS, app 'rest' not published here

GET /INTERSHOP/rest/WFS/<brand>-Site/-/categories
401  12 B  Unauthorized
        -> app '-' EXISTS on the B2B site, auth required  (this is the real shop API)

GET /INTERSHOP/rest/WFS/<brand>-corporate-Site/rest;loc=en_US/categories
200  35 B  {"elements":[],"type":"Categories"}
        -> corporate site public, catalogue empty (products come from Contentful)

GET /INTERSHOP/rest/WFS/doesnotexist-Site/rest;loc=en_US/categories
404 150 B  <HTML><HEAD><TITLE>System status</TITLE></HEAD>...
        -> unknown site
```
Site names tried and rejected (all 150 B "System status"): `<brand>-acc/dev/tst/test/staging/
internal/b2b/business-Site`, `<brand>-webshop-Site`, `<brand>-shop-Site`, `<brand>-nl/de-Site`.

## C. Anonymous basket — authorization correctly enforced

```
POST /baskets  (Content-Type: application/json, Accept: application/vnd.intershop.basket.v1+json, -d '{}')
201  Location: .../baskets/GjoKAgNHIxAAAAGh.MQuuVBa
     authentication-token: encryption0@PBEWithMD5AndTripleDES:<b64>|<b64>|s<salt>

GET /baskets/GjoKAgNHIxAAAAGh.MQuuVBa                       -> 404 {"code":"basket.not_found.error"}
GET ... + authentication-token: <forged>                    -> 401 Unable to decode token
GET ... + authentication-token: <real>                      -> 200
```
=> not an IDOR. Basket id + token are both required and the token is integrity-protected.

## D. Gated resources (all `401 Authentication or token of registered user required`)

`customers/-`, `privatecustomers/-`, `customers/-/users/-`, `orders`, `personalization`,
`customers/-/baskets`.

Open resources observed: `suggest?searchTerm=`, `cms/includes/include.configuration.pagelet2-Include`,
`configurations` (needs `Accept: application/vnd.intershop.configuration.v1+json` -> 2,079 B),
`rzlocalizations?searchKeys=`.

## E. Custom extensions found by grepping the bundle

```bash
grep -ohE 'apiService\.(get|post|put|delete)\("[a-zA-Z0-9/_.:;{}$-]{1,60}"' main.*.js | sort -u
```
Result set included: `baskets/current`, `baskets/current/addresses`, `categories`,
`cms/includes/...`, `configurations`, `countries`, `customers/-`, `personalization`,
`privatecustomers/-`, `productfilters`, `productprices`, `products`, `rz-stock`, `suggest`,
`security/password`, `security/reminder`, `users/processtoken`,
`customers/-/users/-`, `token/logout`.

`security/password` (forgot-password) and `users/processtoken` are the highest-value
authenticated targets (reset-link poisoning, token processing).

## F. XSS negatives (recorded so they are not re-tested)

- ICM error reflection: `GET /products?productFilter=<script>alert(1)</script>` ->
  `400 text/plain` `Bad Request (productFilter <script>alert(1)</script> is undefined.)`.
  `Accept: text/html` -> `406 Not Acceptable`; `X-Content-Type-Options: nosniff` present.
  Reflected but not executable.
- 180-route/param browser matrix (`searchTerm,q,errorKey,errorType,returnUrl,redirect,page,
  pageSize,sortKey,view,categoryId,sku,B2BCustomerLogin,landingPageId,newsSlug,
  contentPageSlug,code,state,message,query` across home/search/error/login/register/page/
  news/campaign/loading) -> 0 executions, 0 raw reflections of `"><img src=x onerror=...>`.
- PunchOut disabled: `/en/punchout?sid=...` -> `/en/error?error=feature-deactivated&value=punchout`.

## G. Auth state

- Storefront login/register redirects to `<auth-host>/authorize?response_type=code&
  client_id=&state=...&redirect_uri=https%3A//www.<target>/en/loading&scope=openid email
  offline_access&code_challenge=...&screen_hint=signup` — **empty client_id** -> Auth0 error
  -> SPA "Oops!, something went wrong". Self-registration unusable; authenticated IDOR needs an
  operator-supplied account.

## H. CORS observed (non-finding, recorded once)

```
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: HEAD,DELETE,POST,GET,OPTIONS,PUT,PATCH
Access-Control-Allow-Headers: authorization,Accept,X-Captcha-Token,authentication-token,UserOrganization,Content-Type
Access-Control-Expose-Headers: error-missing-attributes,FieldNames,authentication-token,error-key,error-type,location,error-invalid-attributes
```
Static `*`, no `Access-Control-Allow-Credentials`, reflected identically for
`Origin: https://evil.example.com` and in preflight => not exploitable.
