# Stored XSS: establishing whether you can even reach the write path

Reflected/DOM sweeps do not touch stored XSS. On any SaaS target the stored sinks (profile,
entity titles/descriptions, bot/alert names, notes, imported objects) sit behind a login, so
the first question is not "is it vulnerable" but **"can I get a session, and if not, which gate
stopped me?"**. Answer that explicitly, in writing, before the report claims coverage.

## Gates to probe, in order

### 1. Read the signup SPA before touching the API

Fetch `/register/` (and the marketing `/pricing/signup/<plan>/` page) and read the bundle.
On one engagement this exposed, without any auth:

- a `tokens` cookie = base64 JSON map of per-method form tokens
  (`user-create`, `check-coupon`, `subscription-create`, `create-paypal-order-…`)
- the RPC shape `POST /authentication/1/registration/<method>` with `{…, token}`
- plan IDs base64-encoded into the marketing HTML: `data-plan_id="Z28yNV9zdGFuZGFyZF9wcF8xbW8="`
  → `go25_standard_pp_1mo`

Tokens turned out to be **method-bound** (reusing `check-coupon`'s token on `get-tax-rate`
returned `wrong form token`). Verify that before assuming a token swap is a bug.

### 2. Determine whether "free" signup is actually free

```bash
GET /authentication/1/registration/billing-plans?plans=<planId>
→ {"id":"…","price":89,"trial":14,"trialOptions":{"paid":true,"price":19}}
```

Every reachable plan carried a **paid trial fee** ($19/$29/$39/$49). The SPA's `?ncc=1`
(no-credit-card) flag only skips the *UI*: `subscription-create` still failed server-side with
`Something went wrong please contact support`. Send a tampered plan object
(`price:0, trialOptions.paid:false`) to confirm the server resolves the plan by ID rather than
trusting the client payload — that is a correct implementation, and worth knowing before you
write "price manipulation" in your notes.

### 3. Disposable-email filter behaviour

The filter returns a field-level error you can read: `{"userDetails.email":{"indisposable":"Email is disposable"}}`.
Probe a handful of providers, plus the classic evasions — uppercase, `+alias`, trailing dot,
space. On this target all were blocked and the trailing-dot form was rejected as invalid.
Record the exact message: it tells the next session the filter exists and which layer owns it.

### 4. If the product runs a GraphQL signup, discover the schema from errors

GraphQL error messages are a free schema oracle:

```
mutation { signup(type:{}, credentials:{}, recaptcha:"") … }
→ Enum "AuthTypeInput" cannot represent non-enum value: {  }.

mutation { signup(type:BOGUS123, …) }
→ Value "BOGUS123" does not exist in "AuthTypeInput" enum.

mutation { signup(type:password, credentials:{…}, recaptcha:"") … }
→ Password is too weak          ← structurally accepted, reached business logic
→ Sorry, no bots allowed        ← reCAPTCHA is enforced server-side
```

The useful signal is the **transition**: once you reach password-strength or credential
validation, the mutation accepted your payload shape; the captcha rejection afterwards proves
the control is server-side and not merely a client gate. Try valid enum members systematically
(`token`, `password`, `id`, `google`, `apple`, …) — an "invalid enum" error for one value and a
different error for another tells you which are real.

### 5. Confirm the authenticated bundle is unreachable statically

Before spending time trying to read the gated SPA:

```bash
curl -sk -o /dev/null -w '%{http_code} %{redirect_url}\n' https://app/       # 302 → /login
curl -sk https://app/ngsw.json                                              # Angular SW manifest
curl -sk https://app/asset-manifest.json
curl -sk "http://web.archive.org/cdx/search/cdx?url=app.host*&output=text&fl=original"
```

No service-worker manifest, 403 on unknown CDN keys, and an empty wayback CDX each close a
door. An empty CDX is a *useful negative*: no archived JS means the gated chunk list cannot be
recovered from the archive.

### 6. Staging is the cheapest door — check it, then expect it to be broken

Before paying for a production trial, look for the staging estate (it is usually in the
sibling registrable domain named by production CSP `frame-ancestors` and by the Sentry
`tracesSampleOrigin` list). Two things make staging worth a look:

- **Test payment keys.** A staging register page will happily ship
  `pk_test_51H7o9sKb…` — meaning `pm_card_visa` should complete a "paid" plan for free and
  hand you an account on the same application code as production.
- **Relaxed policy.** Staging often has disposable-email filtering, captcha and email
  verification disabled or misconfigured.

Both were false on the engagement this note comes from, and the negative is worth recording:

```
subscription-create (staging, every fresh random address, gmail.com, outlook.com,
                    paymentMethodId: null and pm_card_visa)
→ {"result":"Customer with this email already exists","domain":"email"}
```

An error identical across *fresh* addresses, multiple domains and both payment modes is a
**broken backend**, not an email collision. Do not keep generating addresses — stop, record it,
and move to the next gate. Also check the staging CMS separately: a staging WordPress
(`wordpress-ts01-staging.<sibling>`) can be live while `?action=register` returns 302
(registration disabled), which closes that door too.

Scope discipline: a staging estate on a different registrable domain is the operator's call,
not yours. Test it if the evidence says it is theirs, and say so explicitly in the coverage
table rather than silently including or excluding it.

## What to report when the gate holds

- Coverage table gets an explicit row: `Stored XSS — not testable, account required`, with the
  specific gate (captcha / paid trial / basic auth) named.
- Never let "reflected + DOM clean" imply stored coverage. They are different sweeps.
- State what you *did* verify about the stored render path — e.g. "60 shared-entity titles
  sampled; `&`, `'`, `"` all emitted as `&amp;`, `&#39;`, `&#34;` in `<title>`, `og:title`
  (single-quoted attribute) and JSON-LD" — so the negative is evidence, not assertion.

## Ask for exactly this

One authenticated session is enough to run the stored matrix (chart title, description, bot
name, alert text, imported-entity name, notes). The concrete request to the operator:

> paste your `Cookie` header from `app.host` (`auth_token` + `AWSALB`), or the equivalent
> session cookie — I'll replay it and run the stored matrix in one pass.

Two accounts are only needed for IDOR/ATO cross-tenant checks, not for stored XSS.
