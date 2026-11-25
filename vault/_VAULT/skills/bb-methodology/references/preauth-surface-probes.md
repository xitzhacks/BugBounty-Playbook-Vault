# Pre-auth surface probes (company-run VDP, SPA + nginx/ALB)

Session: TrendSpider VDP, 2026-11-16. Company-run program, no published asset list, form submission.
Purpose: what a pre-auth pass on a modern SPA actually yields, and which "no" answers are real.

## The header gate that fakes a dead endpoint

```
POST /authentication/1/member/login/        (JSON body, Accept: application/json)
→ HTTP 403  <h1>403 Forbidden</h1>          ← nginx, no Origin/Referer

same request + Origin: https://<host> + Referer: https://<host>/login/ + browser UA
→ HTTP 200  {"success":false,"error":"invalid_credentials"}
```

Always re-send once with the browser header set before concluding anything about a POST endpoint.

## Probe set that produced clean negatives (and is cheap to repeat)

| Probe | Request shape | Expected clean result |
|---|---|---|
| S3 bucket listing | `GET https://<bucket>.s3.<region>.amazonaws.com/?list-type=2` | `AccessDenied` XML |
| Login open redirect | `?<param>=https://example.org/x` for redirect / next / return_url / redirectUrl / callback / target / r | server-rendered `<meta name="redirect-target" content="/">` unchanged |
| CORS | `Origin: https://evil.example` on `/`, `/api/`, auth route | no `Access-Control-Allow-*`; `OPTIONS` → 403 |
| User enumeration | 2 random emails + 1 plausible corporate address | identical body + error code; timings within jitter (n=1 is not signal) |
| 2FA send-code unauthenticated | POST with a nonexistent email | requires credentials (`invalid_credentials`) |
| App proxy auth | `GET /1/<thirdparty>/proxy/{,me}` | `403 {"error":"..._session_invalid"}` |
| Vendor widget DOM XSS | `<vendor>/charting_library/static/tv-chart.html#indicatorsFile=` | 404 — widget not served on that host |

Method exactly as in `bb-methodology`: marker-free, one request per probe, no enumeration of real users.

## Observations that are context, not findings

- Session cookie cleared as `auth_token=; Path=/; Expires=Thu, 01 Jan 1970` with **no HttpOnly / Secure /
  SameSite**. If the live cookie matches it is an enabler, but cookie-flag-only reports are "no meaningful
  impact" on most programs — it only counts inside a chain, and proving it needs a login.
- No HSTS on the app host. Hygiene.
- CSP with `script-src-attr 'unsafe-inline'` and `frame-src` listing widget hosts — the widget/postMessage
  surface is interesting but auth-gated.
- CDN block: marketing host (CloudFront + SiteGround, WordPress) flipped to 403/502 after ~6 fetches from
  the test IP. `/wp-json/`, `/xmlrpc.php`, `/feed/` all unreachable. Do not grind; revisit from a clean IP.

## Where the rest of the surface lives

Everything the program pays Medium/High for (IDOR on shared objects, stored XSS in user-named objects,
connector/account enumeration, SSRF in import/fetch features) sat behind login. Pre-auth yield on a
well-built SPA is legitimately near zero — that is a finding about the target, not about the tester.
Next step is a trial account (operator identity, not fabricated), then object-id work on share links.
