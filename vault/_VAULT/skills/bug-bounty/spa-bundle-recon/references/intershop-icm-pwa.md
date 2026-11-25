# Intershop Commerce (ICM) + Angular PWA — backend discovery and API probe map

Worked example for the case where **the API base is NOT in the bundle** (Step 3b of the main
skill) plus a reusable platform recipe. Verified end-to-end on an enterprise B2B/B2C storefront
(2026-10); numbers below are measured, not illustrative.

Intershop is widespread in EU enterprise retail. The two halves are usually **separate hosts**:
an Angular "PWA" storefront behind a CDN, and a directly internet-facing **ICM** backend that
does NOT sit behind the same WAF. Finding the backend host is the whole game — the storefront is
the hardened part; the ICM API is where the API testing belongs.

---

## 1. Fingerprint — is it Intershop?

| Signal | Where |
|---|---|
| `ng-app-id="intershop-pwa"` on `<html>` | storefront HTML (Angular, SSR) |
| `/INTERSHOP/rest/WFS/...`, `/INTERSHOP/web/WFS/...`, `/INTERSHOP/static/WFS/...` | bundles or links |
| string `pwa-ish-demo.test.intershop.com` | main/vendor JS (vendor demo origin, harmless) |
| `application/vnd.intershop.<x>.v1+json` media types | bundle request headers (`basket`, `order`, `configuration`) |
| `ARRAffinity` / `ARRAffinitySameSite` cookies | ICM on Azure App Service / VM |
| `rest;loc=en_US` path segment | ICM REST resource URLs |

```bash
curl -sk https://<storefront>/ | grep -oE 'ng-app-id="[^"]+"'
grep -ohE 'INTERSHOP[a-zA-Z0-9/._-]{0,40}' js/*.js | sort -u
```

**Do not trust the archived URL corpus for this platform.** Old `/wps/wcm/connect/...`
(WebSphere) and `/.../*.nsf?OpenForm&Start=...` (Domino) paths 301 into the SPA and are dead —
archive names for `?Start=`, `?BaseTarget=`, `?FieldElemFormat=` were pure waste. The corpus is
only useful as *parameter names to try on the new app*.

---

## 2. Step 3b in practice — read the live XHR, not the bundle

`grep 'https://'` over the bundle returned only vendor demo hosts, because the API base is
runtime-configured. Get it from an already-loaded page. Marionette `execute_script` — remember
the `return`, or you silently get `None` (see `browser-isolation`):

```python
from marionette_driver.marionette import Marionette
m = Marionette('localhost', port=2828); m.start_session()
m.navigate("https://<storefront>/"); time.sleep(10)
print(m.execute_script("""
  return performance.getEntriesByType('resource')
    .map(r => r.initiatorType + ' ' + r.name)
    .filter(s => /xhr|fetch|rest|intershop|api/i.test(s)).join('\\n');
"""))
m.delete_session()
```

Observed (trimmed):

```
xmlhttprequest https://webshop-prod-live-backend.<tld>/INTERSHOP/rest/WFS/<corporate-Site>/rest;loc=en_US/rzlocalizations?searchKeys=pwa-
xmlhttprequest https://api.search.<vendor>.ai/api/auth
xmlhttprequest https://graphql.eu.contentful.com/content/v1/spaces/<id>/environments/master
```

That one line yields **three** facts the bundle cannot give you: backend host, base-site name,
and the exact path shape `/INTERSHOP/rest/WFS/<site>/rest;loc=<locale>/<resource>`.

`performance.getEntriesByType('resource')` is synchronous, costs no network, and enumerates
everything the page already fetched — it generalises to **any** SPA with a runtime-injected API
base (Spartacus/SAP Commerce, custom Angular/React, headless storefronts).

---

## 3. Base-site / application enumeration ORACLE (precise, cheap)

ICM answers differently for unknown-site / known-site+unknown-app / public-app / auth-app.
**Response byte size is the discriminator:**

| Response | Size | Meaning |
|---|---|---|
| `<HTML><HEAD><TITLE>System status</TITLE>...` 404 | **150 B** | site does not exist |
| `Not Found (Application '<app>' not found in context of the site '<site>'.)` 404 | **~81 B** | **site EXISTS**, app not published there |
| `{"elements":[],"type":"Categories"}` 200 | 35 B | public app, empty catalogue |
| `Unauthorized` 401 | 12 B | **app exists, requires auth** — the real shop |

```bash
B=https://webshop-prod-live-backend.<tld>/INTERSHOP/rest/WFS
for s in <tld> <tld>-Site <tld>-corporate-Site <tld>-dev-Site; do
  printf "%-30s " "$s"
  curl -sk -o /dev/null -w '%{http_code} %{size_download}\n' \
    "$B/$s/rest;loc=en_US/categories" -H 'Accept: application/json'
done
```

Then enumerate the **application** on a known site (`-`, `rest`, `web`, `pwa`, `inTRONICS`, …).
A `-` app returning `401 Unauthorized` is the B2B storefront app — authz enforced at app level,
no anonymous catalogue to hunt. Record and stop; do not fuzz object IDs.

Two requests per candidate, and it never touches the CDN, so it does not spend the WAF budget in
`recon-pitfalls` §11.

---

## 4. Public ICM endpoints worth reading

```bash
B="https://<backend>/INTERSHOP/rest/WFS/<site>/rest;loc=en_US"

# channel configuration — REQUIRES the vendor media type, else 406 Not Acceptable
curl -sk "$B/configurations" -H 'Accept: application/vnd.intershop.configuration.v1+json' | jq .
```

Leaks without auth: locales, currencies, price-display type, captcha-gated operations,
`UserRegistrationLoginType`, and **internal contact addresses**. Standard ICM → informational,
but it maps which auth flows exist (`forgotPassword`, `register`, `contactUs`) — i.e. what to
test next.

| Path | Anonymous | Note |
|---|---|---|
| `/categories`, `/products`, `/suggest` | 200 | empty on a corporate-only site |
| `/customers/-`, `/privatecustomers/-` | **401** | registered user required |
| `/orders` | **401** | auth required |
| `/personalization` | **401** | "not authenticated in expected context" |
| `/cms/includes/include.configuration.pagelet2-Include` | 200 | pagelet metadata |
| `/productprices`, `<custom>` resources | **406** | need a specific `Accept` |
| `/products?productFilter=<x>` | **400 text/plain** | reflects `<x>` unescaped — inert, see `hunt-xss` |

---

## 5. Anonymous basket — the correct 3-way authorization test

ICM issues an anonymous basket plus a token; this pattern is worth running because a failure is
a genuine cart-IDOR finding:

```bash
curl -sk -X POST "$B/baskets" -H 'Content-Type: application/json' \
     -H 'Accept: application/vnd.intershop.basket.v1+json' -d '{}' -D h.txt
# 201 + {"data":{"id":"<basketId>",...}} + authentication-token: encryption0@PBEWithMD5AndTripleDES:...

curl -sk "$B/baskets/<id>" -H 'Accept: application/vnd.intershop.basket.v1+json'   # 404 "cart could not be found"
curl -sk "$B/baskets/<id>" -H 'authentication-token: <forged>'                     # 401 "Unable to decode token"
curl -sk "$B/baskets/<id>" -H 'authentication-token: <real>'                       # 200
```

All three correct = enforced → **do not report**. CORS on every ICM response is
`Access-Control-Allow-Origin: *` with `authorization, authentication-token` allowed; that is
**not** exploitable (wildcard origin cannot carry cookies, and tokens live in `localStorage` on
the storefront origin). Architecture observation only.

---

## 6. Storefront-side surfaces worth naming

- Routes that name the IDOR surface: `users/:B2BCustomerLogin`, `cost-centers/:CostCenterId`,
  `quote/:productSku`, `requisition/:id`, `order/:id`, `page/:contentPageSlug`, `news/:newsSlug`.
- All gated behind an OIDC login. If the authorize URL ships an **empty `client_id`**,
  self-registration is broken and authenticated testing is impossible without operator-supplied
  credentials — say that early instead of burning hours.
- Punchout params (`sid` + `access-token`, `HOOK_URL` + `USERNAME` + `PASSWORD`) are cXML/OCI SSO.
  When deactivated the app redirects to `/error?error=feature-deactivated&value=punchout` and
  stores nothing — inert.
- URL params land only in the SSR `ngrxState` blob — verdict logic lives in `hunt-xss`.

---

## 7. Checklist

```
[ ] ng-app-id / INTERSHOP paths            → confirm platform
[ ] performance.getEntriesByType('resource') → backend host + base site + locale path
[ ] base-site oracle (150 vs 81 bytes)     → enumerate sites, then apps
[ ] `-` app 401                            → real shop, authz enforced → stop fuzzing
[ ] /configurations w/ vendor Accept       → map enabled auth flows
[ ] customers/orders/personalization 401   → authz present
[ ] POST /baskets + 3-way token test       → cart IDOR check
[ ] ACAO:* + localStorage                  → not exploitable, note as observation
[ ] storefront routes                      → IDOR names for when credentials arrive
```
