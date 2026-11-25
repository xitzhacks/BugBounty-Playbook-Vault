# Firebase-Backed SPA — Passive Recon & ATO Surface Mapping

Use this when the target is a Single-Page App whose auth/session rides on Firebase
(email/password, phone, or IdP) plus a custom backend API. Common in JP/KR/CN betting,
fintech, and commerce apps. Everything below is passively doable with no user account.

## Step 1 — Extract the client config (this is the map)
Fetch the SPA entry HTML and grep for the inline config blob. Look for:
`window.__CONFIG__`, `window.__PRELOADED_STATE__`, `window._env_`, `runtimeConfig`,
`window.__FLAG_MAP__`, `firebaseConfig`.
The blob usually holds, in one place:
- `API_URL` (backend base, e.g. `https://api.x.jp/v1`)
- `CMS_SERVER_API_URL`, `PROXY_ENDPONT_PREFIX` (web often proxies API same-origin, e.g. `/z/v1`)
- `FIREBASE_API_KEY`, `FIREBASE_AUTH_DOMAIN`, `FIREBASE_PROJECT_ID`, `FIREBASE_APP_ID`,
  `FIREBASE_DATABASE_URL`, `FIREBASE_STORAGE_BUCKET`
- OAuth client IDs (Ponta `PONTA_WEB_CLIENT_ID`, PayPay, Apple `APPLE_PAY_MERCHANT_IDENTIFIER`)
- Payment/gateway keys (GMO, Braze, Sentry, Datadog) — EXPECTED in client, NOT bugs.
Save to `client_config.json`.

## Step 2 — Decompress JS bundles (curl gotcha)
`curl -s -o bundle.js URL` often saves **raw gzip bytes** (magic `1f 8b 08`) because the
CDN gzip-encodes and curl does NOT auto-decompress when writing to a file.
Detect: `file bundle.js` → "gzip compressed data". All your greps then silently match nothing.
Fix: re-download with `curl -s --compressed -o bundle.js URL` (or `gunzip`). Always verify
with `file`/`head -c 80` before parsing.

## Step 3 — Mine bundles for the auth flow & custom headers
Grep the (decompressed) bundles for:
- request-interceptor logic: `x-api-key`, `x-xsrf-token`, `Authorization: Basic`, custom
  flags like `X-WT-Draft` / `X-WT-Mirror` / `X-WT-API-Origin`, `X-Forwarded-For` (client-set).
- endpoint strings: `/v1/users/me/auth-token`, `/login`, `/connect/callback`, `/banks`,
  `/my/point/charge`, etc. These reveal the real backend route tree even when the API
  returns 401/404 to an unauth caller.
Find the function that turns a Firebase credential into a backend session
(e.g. `ApiLogin{firebaseIdToken, loginType, shortPassword}` → `/login` →
`POST /users/me/auth-token`). That exchange is the ATO pivot point.

## Step 4 — Firebase public-endpoint hardening checks (all passive, no user)
1. RTDB public read: `GET https://<project>.firebaseio.com/.json?shallow=true`
   → expect `401 {"error":"Permission denied"}`. `200` with data = public leak (bug).
2. `getProjectConfig`: `GET https://www.googleapis.com/identitytoolkit/v3/relyingparty/
   getProjectConfig?key=<API_KEY>` with header `Referer: <app origin>`.
   Reveals `authorizedDomains` (often leaks staging/preview hosts like `*.run.app`,
   `web-preview-stg.<brand>.bet`, `localhost`) and `signInOptions`.
3. API-key referer restriction: call an endpoint with EMPTY referer → expect
   `403 API_KEY_HTTP_REFERRER_BLOCKED`. If it works off-domain, the key is open (recon aid,
   and a sign the project is loosely configured).
4. Admin APIs: `createSessionCookie` → expect `401 ... API keys are not supported`
   (needs OAuth2). If callable with just the API key = misconfig.
5. Email enumeration: `verifyPassword` with a bad email returns `EMAIL_NOT_FOUND` while a
   real account returns `INVALID_PASSWORD`. This discloses registration — but many programs
   (e.g. IssueHunt/WinTicket) EXPLICITLY exclude username/email enumeration from scope.
   Do NOT report it; just note so you don't re-discover it.

## Step 5 — ATO hypotheses that need an account (cannot validate passively)
- OAuth link binding: when linking Ponta/PayPay/Apple, does the backend verify the OAuth
  identity (email/subject) equals the logged-in user? If linking is driven purely by the
  OAuth code/assertion without binding to the session, cross-account link abuse is possible.
- Session-token scoping: is the `/users/me/auth-token` result scoped strictly to the user
  whose `firebaseIdToken` was presented? Token-swap/confusion between accounts?
- IDOR on reset/link endpoints that return 405 to GET (j.mp) — the POST likely exists.

## Hardened vs vulnerable quick table
| Check | Hardened (good) | Vulnerable (bug) |
|-------|-----------------|------------------|
| RTDB read | 401 | 200 with records |
| API key referer | 403 off-domain | works anywhere |
| createSessionCookie | 401, needs OAuth2 | callable w/ API key |
| authorizedDomains | only prod hosts | wildcard / foreign domain |

## Scope discipline
- `authorizedDomains` leaks staging hosts. Check reachability (`curl -o /dev/null -w %{http_code}`).
  If `000`/dead, ignore. If live AND lower-security AND in-scope (`*.target.jp`), it's a lead.
- Embedded payment/gateway/analytics keys in client config are EXPECTED — not findings.
- Respect program rules: no fabricated accounts, no KYC/geo bypass, no destructive money flows
  on live betting/fintech platforms. Passive recon first; authenticated testing needs a
  legitimately obtained test account.
