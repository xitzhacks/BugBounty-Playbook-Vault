# Provisioning your own test accounts on a SaaS target

Most high-value classes (IDOR, stored XSS, SSRF via integrations, checkout/price logic,
cross-tenant authz) need a session. Programs routinely say "use your own test accounts".
This is the method for getting them when signup is self-serve — and for recognising fast
when it isn't possible without spending money or PII.

## Decision tree

```
Is signup public?
├─ No  → ask operator for a session (see "Borrowing a session" below)
└─ Yes → is there a no-CC / free-trial path?
         ├─ plan.price == 0 or trialOptions.paid == false → register, no payment
         ├─ trial carries a fee ($X charged at signup)      → STOP, needs operator decision
         └─ unknown                                          → reverse the flow (below)
```

## Reversing a SPA signup flow (30–45 min, unauth)

1. **Fetch the register shell** and list its JS bundles. Decompress gzipped responses
   (`file x.js` → `mv x.js x.js.gz && gunzip`). The shell is usually tiny; the real logic is
   in `register-app-*.js` / `register-lib-*.js`.
2. **Grep for RPC names**, not URLs — modern signups POST to a base path + method name:
   ```bash
   grep -oE '"/(authentication|api|registration)[a-zA-Z0-9_./{}-]{0,70}"' register-app-*.js | sort -u
   grep -oE '.{160}(user-create|subscription-create|check-coupon|get-tax-rate).{200}' register-app-*.js
   ```
3. **Capture the flow's own token mechanism.** The register page often sets a cookie that
   is a base64 JSON map of per-method form tokens:
   ```bash
   curl -sk -D - "https://target/register/?plan=<id>" -o /dev/null   # look at Set-Cookie
   python3 -c "import base64,json;print(json.loads(base64.b64decode('<value>'+'==')))"
   ```
   Client sends the matching token in the request body as `token`. **Verify the binding**:
   reuse method A's token on method B — a correct implementation answers
   `Internal server error (wrong form token)` or `The Token is required`. If it accepts the
   swap, that is a real finding (CSRF-token not bound to the action) — write it up.
4. **Find plan IDs.** Marketing pages embed them, frequently base64-encoded:
   ```bash
   grep -oE 'data-(trial_)?plan_id="[^"]*"' signup.html
   python3 -c "import base64;print(base64.b64decode('Z28yNV9zdGFuZGFyZF90cmlhbF8xbW8='+ '===').decode())"
   # → go25_standard_trial_1mo
   ```
   The plan list is usually readable unauthenticated:
   `GET /authentication/1/registration/billing-plans?plans=<id>` returns price, trial length,
   trial fee, and a full feature-limits map. This is also a cheap oracle: unknown plan → `[]`.
5. **Map required fields without creating records.** Send the create call with an empty body;
   a good backend returns 422 with per-field messages
   (`"The Email is required The Last name is required ..."`). That tells you exactly what the
   server needs before you touch real data.
6. **Confirm what is trusted.** Send the plan object with `price: 0` / `trialOptions.paid:false`
   alongside the legitimate plan id. If the response is unchanged, the server resolves the plan
   by id and ignores client pricing (no bug). If the response changes, you have price tampering.

## The two gates that actually stop you

### 1. Disposable-email blocklist

A register flow that returns `{"result":"Email is disposable"}` / field `indisposable` is
checking the domain against a package list (mailchecker / disposable-email-domains). Expect
every mainstream temp provider to be listed. Tested and blocked on one engagement:
`maxxspace.com` (mail.tm), `maildrop.cc`, `mailnesia.com`, `tempmail.plus`, `moakt.com`,
`yopmail.com` — including uppercase, `+alias`, and trailing-dot variants.

Useful diagnostics, in this order:
- **Check MX first** (`dig +short MX domain`). A provider with no MX (`inboxes.com`) passes
  domain filters but the signup dies later for a different reason — don't chase it.
- **Read the exact error.** "disposable" = domain blocked. A generic
  `Something went wrong please contact support` on a *non*-disposable domain means you cleared
  the filter and hit the next gate — that distinction is the whole diagnosis.
- Only then consider obscure providers; do not burn an hour cycling temp-mail domains. If two
  or three fail, the gate is deliberate.
- `scripts/temp_mailbox.py` creates and reads a mail.tm mailbox if you need a live inbox fast
  (it is on most blocklists — use it to test the filter, not to assume success).

### 2. Paid trial

`?ncc=1` / `?cc=n` (no-credit-card) flags are common in register SPAs — the client skips the
payment UI. That does **not** mean the server allows it. If every plan in the
`billing-plans` response has `trialOptions.paid: true` with a $ fee, `subscription-create`
will fail (`Something went wrong…`) no matter what you send, and no sale-tag/`_go=` campaign
cookie will change the preloaded plan. Verify by comparing `window.preloadedPlanData` across
several `_trendspider_sale_tag` / `_go` values before concluding a free plan exists.

### 2b. Prod gated on a paid trial? Check the staging estate for TEST payment keys

When production demands a card, the staging twin of the same app often runs the payment
provider in test mode — and staging is the same codebase, so an account there exercises the
same authenticated surfaces. Detect it in one request:

```bash
curl -sk 'https://staging-v3.target.com/register/?plan=<planId>&ncc=1' \
  | grep -oE 'pk_(test|live)_[A-Za-z0-9]+'
# pk_test_… → test mode: documented test cards / pm_card_visa can complete the flow
```

Then push the registration call with `paymentMethodId: "pm_card_visa"` (Stripe's public test
PaymentMethod identifier) — valid only against test keys.

**Validate the staging backend before investing in it.** The failure signature of a
*broken* staging customer service is unmistakable and is easy to misread as an email
filter: `subscription-create` returns
`{"result":"Customer with this email already exists","domain":"email"}` for **freshly
generated random addresses** — and continues to say it for unrelated domains
(`gmail.com`, `outlook.com`) and for `paymentMethodId: null` as well. If the same error
comes back for every identity you invent, the environment is not usable; stop. Do not
cycle temp-mail domains against it — you are no longer testing the filter.

Contrast that with the real filter signature, which names the problem:
`{"result":"Email is disposable"}` / field `indisposable`. Different message, different
gate, different next move.

Practical rule: one probe for `pk_test`, one registration attempt with a random address.
If it doesn't reach a payment or account-creation step, staging is a dead end — note it and
fall back to "Borrowing a session" below. Staging is also frequently a **different
registrable domain** than the program names (e.g. `*.chartcalc.com` for a `*.trendspider.com`
program) while still being referenced from the production CSP `frame-ancestors` and Sentry
config — that's evidence it is the target's infrastructure, but the scope call is the
operator's, not yours.

### 3. Captcha on signup (REST or GraphQL)

Some targets (SignalStack, i.e. the trading-automation side of a SaaS estate) put reCAPTCHA on
signup itself. Don't assume it is enforced — **prove it with the error ladder**, because argument
validation runs before the captcha check and the messages tell you which gate you are at:

```bash
# 1. shape/enum discovery — invalid enum value names the enum, not the values
curl -s -X POST https://app.target.com/graphql -H 'Content-Type: application/json' \
  -d '{"query":"mutation { signup(type:{}, credentials:{}, recaptcha:\"\") { key } }"}'
# → Enum "AuthTypeInput" cannot represent non-enum value: {  }.
#    Enum values are revealed by *absence* of this error: type:token and type:password accepted.
# 2. no recaptcha + weak password
# → {"errors":[{"message":"Password is too weak"}]}      # still before the captcha check
# 3. no recaptcha + strong password
# → {"errors":[{"message":"Sorry, no bots allowed"}]}     # captcha IS enforced server-side
```

Interpretation: step 2 passing means the request shape is right and the captcha is not validated
before credential checks; step 3 is the verdict. A hard `Sorry, no bots allowed` / `captcha
verification failed` on an empty token = gate is real, stop. Only if step 3 returns a token/account
do you proceed. Same ladder works for the `signin` mutation — which is also the cheapest way to
confirm a credential pair before you invest in a flow.

For a GraphQL-native signup the mutation text is in the bundle:
`grep -o 'mutation Signup(.\{0,600\}' index-*.js` gives you the exact argument names and types
(including required `recaptcha: String!`), so you never have to guess the input shape.

**Decision point:** a paid trial is the operator's money and the operator's identity. Stop and
ask. Do not sign up with a card, do not brute coupon codes to zero the fee, and do not create
a stack of junk accounts — programs count that as abusive enumeration.

## Borrowing a session when provisioning fails

The fastest unlock, and it costs the operator one click:

- Ask for the **Cookie header** from an authenticated browser session, not a screenshot.
  Needed pieces are the app auth cookie plus any load-balancer stickiness cookie (e.g.
  `auth_token=` + `AWSALB=`).
- Verify it immediately against a known auth'd endpoint before building tests on it
  (`GET /api/me` → 200 with identity, vs the unauth 401/403 baseline).
- One account gives you self-vs-self checks and write-path testing. A second account is
  required for real IDOR; ask for both up front, in the same request, or you will stall
  again ten minutes later.

## Evidence to keep

Save the register bundle, the decoded token map, the `billing-plans` JSON for each plan
tier, the filter error for each email domain tried, and the `subscription-create` failure
body. That set is what lets a later session say "this is blocked and here is why" in one
paragraph instead of re-deriving it.
