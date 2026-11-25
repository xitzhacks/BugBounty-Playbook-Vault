---
title: "Login / Signup / Logout CSRF — session-establishment and session-teardown forgery"
type: playbook
category: login-signup-logout-csrf
cwe: "CWE-352"
source_count: 24
full_bodies_available: 20
corpus: "h1.security.nathan.sx roster (229 rows), bodies via hackerone.com/reports/<id>.json"
list_accessed: "2026-10-28"
note: "Anchor bodies: CSRF-547 (H1, $100 list), CSRF-7531 (IRCCloud), CSRF-229528 (Weblate, medium). Claims trace to bodies read 2026-10-28."
---

# Login/Signup/Logout CSRF — forge the session, not the data

## 1. Overview

Login CSRF inverts the usual CSRF damage model: the attacker does not steal the victim's
session — the victim is **logged into the attacker's session**. The attacker's credentials are
submitted cross-site to the victim's browser; everything the victim does afterward (passwords,
documents, messages) lands inside an account the attacker controls. Twenty-four corpus cases use
this lane; most were paid small ($100) or marked informative — the corpus treats login CSRF as
the *seed* of larger chains (see module 03).

**Case-ID scheme: `CSRF-<report id>`.**

Three sub-mechanisms appear, each with a distinct defense:

| Sub-mechanism | Cases | Defense that fails |
|---|---|---|
| No token on the login form | 21069, 117195, 221043 (title-only), 14494 | the form simply has no CSRF field |
| Token exists but is attacker-fetchable | 7531, 7531-clone rows | pre-session token issued to anonymous requests |
| Login-by-link flows (email confirm / reset) | 547, 229528 | GET link establishes a session, so any GET is a login primitive |

## 2. The anchor — CSRF-547 (HackerOne self-report, $100 list-stated)

The entire body is two steps; the money line is the second:

> 1) Attacker creates a fake account and changes e-mail
> 2) The e-mail confirmation link can now be used to CSRF login someone into the fake account,
> then monitor actions performed by the victim or even interact with him.

Three lessons an agent must copy:

1. **The login primitive is a URL, not a form.** Email-confirmation links are GET requests that
   establish a session — so `<img src="https://target/confirm?token=…">` is a complete login-CSRF
   payload. Any GET-that-authenticates is attackable without JavaScript.
2. **The attacker needs a session of his own first.** Step 1 creates it; step 2 hands it to the
   victim. The pattern is always *attacker session → victim adopts attacker session*.
3. **Impact is surveillance, not destruction.** "monitor actions performed by the victim or even
   interact with him" — the correct impact narrative for login CSRF is victim behavior captured
   in attacker-controlled space, which is why triagers historically paid $100-and-up but not
   critical rates *unless chained* (module 03).

### 2.1 Protection present, token attacker-fetchable — CSRF-7531 (IRCCloud)

This is the more instructive failure: IRCCloud *had* login CSRF protection, and the report
defeats it end-to-end. The protection token endpoint accepts anonymous requests:

> An attacker can easily obtain a CSRF token from the server by initiating the following request:
>
> ```
> POST /chat/auth-formtoken HTTP/1.1
> Host: www.irccloud.com
> Cookie: session=
> Content-Length: 8
> _reqid=1
> ```
> Once this request is sent an attacker would receive a valid CSRF token. In my case I received
> "1397481736.3b1f59ae47e1a139e8a631b2589dfae2"

Then the standard self-submitting form — attacker email, attacker password, **the
anonymously-fetched token**:

```html
<form action="https://www.irccloud.com/chat/login" method="POST">
  <input type="hidden" name="email" value="ATTACKER-EMAIL" />
  <input type="hidden" name="password" value="ATTACKER-PASSWORD" />
  <input type="hidden" name="token" value="1397481736&#46;3b1f59ae47e1a139e8a631b2589dfae2" />
</form>
```

and the verdict:

> This has basically defeated the CSRF protection offered by the application.

Agent lesson: **a pre-session CSRF token that any anonymous visitor can mint is worth nothing.**
When a target claims login-CSRF protection, fetch the token page/call as an anonymous client
(`Cookie:` empty) and mint your own token before forging the login form. Also note the
`Cookie: session=` *empty-value* trick — some backends skip token issuance when no session
cookie exists, others don't check the value at all.

### 2.2 The two-link chain — CSRF-229528 (Weblate, medium)

Where the confirmation-link primitive is patched or missing, Weblate's variant builds it from
two product features — *"registration confirmation together with the password reset"*:

> 3. Attackers will send the confirmation link to the victim
> 4. Victim clicks the link and will automatically logged in to the attackers account.

and the second half is the part that makes it full surveillance:

> 2. Password reset link will sent to attackers email.
> 3. Attacker will click the reset link and will automatically logged in even did not supply the
> password.
> 4. Done. Attacker and Victim now logged in in the same account.

Agent lesson: when a registration flow *auto-logs-in on link click* and the same account's
password can be reset by its originating email, the attacker both plants the session (victim
clicks) and keeps a key to it (reset link). Hunt for **any flow where clicking a link from
email establishes a session**, then ask "who controls that email?"

## 3. Signup CSRF — accounts minted by the victim's browser

- **CSRF-178831 (Yelp, $500 list)** — the signup endpoint needs nothing from the victim:
  > Sign up request on `https://auto-api.yelp.com/account/create_secure` endpoint processes
  > without any checking headers (without cookies, csrf tokens and even user-agent).
  The PoC form is a bare HTML form with a `signature=` query parameter the researcher notes
  expires but *"is not very difficult to generate the new one"*. The impact lane is account
  farming: forced account creation at scale (spam, reputation laundering, name-squatting
  on email providers).
- **CSRF-230428 (Coinbase, informative)** — signup CSRF fires the *"verify email address"*
  flow at the victim; the report is honest that impact is the email-verification spam +
  forced-account lane.
- **CSRF-7332 (IRCCloud)** — registration flood; same class as 178831 with no token at all.
- **CSRF-109810 (Coinbase)** — "Create a New Account" signup CSRF, same forced-creation lane.
- **CSRF-221043 (Nextcloud portal, informative/medium claim)** — login form without token
  validation, PoC is the bare form; the era's template login-CSRF shape.
- **CSRF-50703 ($500 list, metadata-only)** — "CSRF in login form → ATO" claim; body withheld
  in the era export — recorded, the chain is asserted not demonstrated, cited nowhere.

Signup-CSRF validation gate: the *only* impact that pays is demonstrated forced creation
(attacker-controlled email/password pairs) — a blank signup form with a captcha is not a
finding (kill-gate K3 in the agent playbook).

## 4. Logout CSRF — the teardown lane

- **CSRF-13705 (Simplenote, resolved)** — the entire body is one line:
  > **Proof of Concept:**
  > `<img src="https://app.simplenote.com/logout">`
- **CSRF-7516 (IRCCloud)**, **CSRF-223329 (Weblate)**, **CSRF-244778 (WakaTime, duplicate)** —
  same shape.

Logout CSRF alone is a nuisance; its corpus value is as a **chain primitive**: forced logout
refreshes a fixed/known pre-auth token, invalidates a victim's in-progress state, or resets a
session for a fixation attack. It is also the cleanup step after login-CSRF chains.

## 5. Execution template

```
STEP 1 — inventory auth endpoints (unauthenticated):
  GET  /login, /signin, /signup, /register, /logout, /confirm, /verify
  note: which POST bodies carry a token field; which GETs establish state.

STEP 2 — login-CSRF mint test (anonymous):
  curl -s -c jar.txt https://target/login            # harvest any pre-session token
  curl -s -b jar.txt -X POST https://target/login \
       -d "user=ATT&pass=ATTPASS"                    # does it need a token at all?
  If a token is required: re-fetch it with `Cookie:` EMPTY / fresh jar → mint-again.
  A token minted anonymously = login-CSRF protection defeated (7531 pattern).

STEP 3 — link-authentication inventory:
  walk password-reset and email-confirm flows with YOUR OWN test account:
  does clicking the emailed link log you in (no password prompt)?
  If yes → the GET is a login primitive; craft <img src=LINK> login CSRF.

STEP 4 — forge and land:
  self-submitting form (POST) or bare <img>/<a> (GET) on an attacker page;
  victim = your SECOND test account's browser (two-account discipline, module gates).
  success state: second browser now shows ATTACKER's account name.

STEP 5 — impact step (mandatory):
  on the captured account, exercise the monitoring primitive the body describes:
  read something the victim's next action exposes; or demonstrate persistent
  adoption via reset-link control. Screenshot both browsers side by side.
```

## 6. Validation gates (all must pass)

1. **Two-browser proof**: browser A (victim) navigated by attacker page ends logged in as
   attacker B — username visible in the authenticated UI, not just a 302.
2. **Anonymous mint (when relevant)**: the 7531-style token fetch reproduced with an empty
   cookie jar, token value captured in evidence.
3. **Impact action recorded**: what the attacker can observe/do post-login — stated in the
   report the way 547 states it ("monitor actions… or even interact with him").
4. **GET-that-authenticates identified** with the exact URL parameter set.
5. **State restored** after testing (logout both, delete created accounts).

## 7. Adjacency

- **Clickjacking at the login page** — CSRF-14494 (Mavenlink) pairs the login form with UI
  redressing; module 00 (playbook P4) gates the two apart: clickjacking needs victim *eyes*,
  login CSRF does not.
- **Session fixation** — login CSRF and fixation are the same primitive viewed from different
  sides; if the login response *accepts* a pre-supplied session cookie, escalate through
  Vault/Auth-Session lanes (companion vault).
- **Signup-CSRF → email-verification spam** — pair with rate-limit findings (Vault/Rate-Limit).

## 8. Archive-label honesty

- CSRF-230428 is `informative` with an empty Impact section — kept as the honest example of a
  signup-CSRF report that under-argued impact.
- CSRF-117195 (Bitbucket) is `not-applicable`: body asserts *"There is no state parameter in
  bitbucket login request… possible to exploit login csrf"* — the absence of a PoC plus the
  not-applicable state makes it a **claim-without-proof** row; recorded, not cited as evidence
  of a mechanism.
- CSRF-6871/6872 are the JSON-verified pair ($100 each) — the only figures in this module with
  JSON provenance; everything else here is list-stated or unfigured.

## 9. Cross-references

- Module 03 (ATO chains) — email-change and reset-link chains built on this lane's primitives.
- Module 02 (OAuth state) — login CSRF via OAuth flows without `state`.
- [`../XXE/`](../XXE/) — same two-browser validation discipline.
- [`CSRF-Testing-Agent-Playbook.md`](CSRF-Testing-Agent-Playbook.md) — P1 step order, K-gates.
