---
title: "Validation Gaps & Bypasses — blank tokens, referer checks, type juggling, routing tricks"
type: playbook
category: validation-gaps-bypasses
cwe: "CWE-352"
source_count: 30
full_bodies_available: 30
corpus: "h1.security.nathan.sx roster (229 rows), bodies via hackerone.com/reports/<id>.json"
list_accessed: "2026-10-28"
note: "Anchor bodies: CSRF-52635 (UniFi, 8.2KB full-session PoC), CSRF-86022 (Phabricator, $450 list), CSRF-195156 (Shopify HTTP-auth API, $1,000 list). Claims trace to bodies read 2026-10-28."
---

# Validation Gaps & Bypasses — the token is there, the check is not

## 1. Overview

Thirty corpus cases split between two postures: (a) **token absent or accepted-blank** —
the server never validates; (b) **token present but the check is strippable** — referer-only,
Origin-only, loose comparison, routing artifacts. This is the highest *yield-per-minute* module:
blank-token probes cost seconds and the Localize/Slack/onpatient clusters all fell to them.

**Case-ID scheme: `CSRF-<report id>`.**

| Family | Cases |
|---|---|
| Token stripped/blank accepted | 99647, 99857, 120143, 163815, 151827, 15454, 2635, 2638, 143321, 208734, Localize ×8 (7870, 7916, 7962, 8216, 8218, 8224, 8226, 8273) |
| Referer/Origin-only checks | 52635, 251918 |
| Loose comparison (type juggling) | 86022 |
| Routing/extension artifacts | 95555 |
| Double-token confusion | 148517, 174470 |

## 2. The anchor — CSRF-52635 (UniFi v3.2.10, full session PoC)

The controller protects everything with **one Referer check**, and the body proves it in full —
the 401→200 sequence when the Referer is simply removed:

> the application has an insufficient Cross-Site Request Forgery protection in place by only
> checking whether the Referer Header is present and if its actual value matches the host where
> the system is running (default: 127.0.0.1).

The PoC then changes the administrator password with a **blank-referer iframe** (plus the
`enctype=text/plain` JSON-smuggling variant noted in module 06's boundary table):

> The following Proof-of-Concept will bypass the CSRF protection and change the password of the
> administrator. Basically all functionalities are vulnerable on the same way.

Agent lessons:

1. **Referer checks validate presence, not legitimacy** — blank-referer iframes
   (`<iframe src=…>` pages strip Referer under referrer-policy; era: meta-refresh/no-referrer
   tags) pass "is it there and does it match?" tests by removing the value entirely — the
   correct probe is *remove, don't spoof*.
2. **One endpoint's validation gap = all endpoints** ("Basically all functionalities are
   vulnerable on the same way") — but the agent must still enumerate; a middleware gap is
   per-route in most modern stacks.
3. The report's evidence standard is the corpus best: original request → stripped request →
   200 with state change → repeat for each class of action.

## 3. Blank-token clusters

- **Localize ×8 (7870, 7916, 7962, 8216, 8218, 8224, 8226, 8273)** — every POST carries a
  `CSRFToken` field and the server accepts **blank values**. One template, eight findings:
  settings save, project access add/remove, phrase edit, group create, invitations, watch.
- **CSRF-99647/99857 (onpatient)** — `X-CSRFToken` header removed from AJAX; server processes
  anyway. Same with **CSRF-2635/2638 (Slack-era)** — no token on support/comment POSTs.
- **CSRF-120143 (Veris)** — change-password with `csrfmiddlewaretoken` removed:
  > 7. Forward the request.
  > 8. You'll notice the success message as Password changed Successfully.
- **CSRF-163815/151827 (gratipay)** — the honest two-step: *"Gratipay is not validating csrf
  token at server side for few requests"* / *"it is obvious that the application uses no
  protection against CSRF and the token named **csrf_token** is being passed in the cookie
  instead of a post parameter"* (151827) — the cookie-only double-submit with no server state.
- **CSRF-208734 (BrickFTP)** — the null-value variant:
  > the problem is in the "authenticity_token" parameter which is not properly set well,
  > because it accept the null value which i bypassed it
  > 2-replace "authenticity_token" parameter value with null
- **CSRF-143321 (Veris)** — *unauthenticated* CSRF: user can input any value for the CSRF token —
  the token is accepted as *any* string, i.e. presence-without-binding.
- **CSRF-15454** — user-details update with no token field at all.
- **CSRF-45428 (Vimeo, informative)** — the anti-CSRF token present but *"it's not going to
  validate on server side"* on forgot-password — token-presence theater; also drives reset-mail
  flooding.
- **CSRF-45050 (Informatica community)** — `pm-delete.jspa` passes with neither referrer nor
  token check — victim private messages moved to trash.
- **CSRF-102376 (m.ok.ru, RU)** — ajax CSRF (`X-XTKN`) beaten via the `st.rtu` redirect-path
  parameter; photo-delete forged through the ajax lane.

## 4. Loose comparison — CSRF-86022 (Phabricator, $450 list)

The era's most technical bypass, verbatim core:

> PHP's string conversion rules [2] specify strings (when evaluated in a numeric context) with
> leading decimal, hexadecimal, infinity, NAN or radix (a '.') data optionally followed by an
> exponent are evaluated as floats. What this means is that a string like 00e13242 is cast to 0
> and as such, to PHP 0e94323 == 00e19384.

> Translated into code, this means that the following comparison:
>
>     (hash($randomSecret) == $user_input)
>
> will return true if hash($randomSecret) returns a hash in the form 0+[eE]\d+ and the
> $user_input is given as "0".

Agent lessons:

1. **Any token check written as `==` in PHP is a candidate magic-hash bypass** — the probe is
   a one-character payload: `0` (or `0e123`).
2. The body is a *research document*, not a PoC — it walks `PhabricatorHash::digest()` →
   `AphrontRequest::validateCSRF()` → `PhabricatorUser::validateCSRFToken($token)` line by
   line. That traceability is why it was paid despite being a library-level bug.
3. Modern note: PHP `===` and hash_equals() postdate the bug; the *probe* survives in any
   loose-comparison secret check (JWT secret comparison, CSRF tokens, API keys).

## 5. Routing artifacts — CSRF-95555 (Twitter cards, $280 list)

The token check keys on the endpoint path, and dropping the extension takes the request off
the protected route:

> `/i/cards/api/v1.json` token check bypassed by dropping `.json` extension.

(Summarized from the body read 2026-10-28; the full body walks the cards endpoint variants.)
Agent lesson: when a framework registers CSRF middleware per-format or per-route, **probe the
path with extensions removed, trailing slashes added, and casing changed** before concluding.

## 6. Double-token confusion — CSRF-148517/174470 (H1)

Pages carrying **two token forms** (one per component) where one form's token validates the
other's request — the corpus's smallest family, kept as the reminder that token *presence* is
not token *pairing*.

## 7. Execution template

```
STEP 1 — capture the protected request (any state change, POST).

STEP 2 — the four-strip sequence (cost: ~30 seconds):
  a. remove token field entirely          → replay
  b. token = "" (empty string)            → replay
  c. token = "null" / "0" / "x"           → replay (143321/208734)
  d. remove Referer header; then blank it → replay (52635)
  any 200 + state change = finding; document WHICH strip worked per endpoint.

STEP 3 — loose-comparison probe (PHP stacks):
  token = "0" → replay (86022). Also "0e1234567890".

STEP 4 — routing probes:
  drop file extensions (95555), add trailing slash, change case,
  HEAD/GET/POST method swap, _method override (103787/195156).

STEP 5 — enumerate the middleware gap:
  repeat step 2 across ALL state-changing endpoints; the corpus lesson
  ("all functionalities are vulnerable on the same way") is a claim to TEST,
  not assume.

STEP 6 — impact: chain the widest gap (module 03 chains; module 06 GET lane).
```

## 8. Validation gates (all must pass)

1. **Per-endpoint strip matrix in evidence** — which of the four strips landed where.
2. **State change verified in the UI/API read-back**, not just a 200.
3. **The 195156 standard for API lanes**: the *condition* (HTTP-auth session) is demonstrated —
   verbatim from its body:
   > I have found that if a user has authenticated through HTTP authentication (opened the
   > example URL that shopify provided him when he created the private application), all the
   > API endpoints will be vulnerable to CSRF.
4. **Framework/proxy artifact ruled out** before reporting (does the 200 come from the app or
   an auth-stripping proxy?).
5. **Era honesty for referer-only lanes**: blank-referer iframes need the specific
   no-referrer mechanics verified in the *current* browser (playbook P4).

## 9. Adjacency

- **Module 04** — token-design vs token-validation is the boundary; 143321/151827 sit on it.
- **Module 06** — GET-lane is "no check at all" taken to its endpoint.
- **Vault/Misconfig** — proxy/REMOTE_ADDR artifacts (134894) belong to infrastructure lanes.
- **hunt-csrf skill** — bypass table; **hunt-api-misconfig skill** — verb tampering overlap.

## 10. Cross-references

- [`references/blogs-index.md`](references/blogs-index.md) §1 — zseano's referer-blank and
  POST↔GET lessons (byte-quoted); §2 — community writeups.
- [`CSRF-Testing-Agent-Playbook.md`](CSRF-Testing-Agent-Playbook.md) — P1 strip-sequence step.
