---
name: idor
description: >-
  Systematic methodology for identifying and exploiting Insecure Direct Object
  Reference (IDOR) vulnerabilities in web applications and REST APIs. Covers
  database-object and static-file references, parameter/UUID manipulation,
  detection with and without authentication, Burp Intruder enumeration, common
  vulnerable locations, and remediation. Use when testing access control on
  endpoints that take user/resource IDs.
---

# SKILL: IDOR Vulnerability Testing

## Purpose
Provide systematic methodologies for identifying and exploiting Insecure Direct
Object Reference (IDOR) vulnerabilities in web applications. Covers both
database object references and static file references, detection techniques using
parameter manipulation and enumeration, exploitation via Burp Suite, and
remediation strategies for securing applications against unauthorized access.

## Inputs / Prerequisites
- Target Web Application: URL of application with user-specific resources
- Multiple User Accounts: At least two test accounts to verify cross-user access
- Burp Suite or Proxy Tool: Intercepting proxy for request manipulation
- Authorization: Written permission for security testing
- Understanding of Application Flow: Knowledge of how objects are referenced
  (IDs, filenames)

## Outputs / Deliverables
- IDOR Vulnerability Report: Documentation of discovered access control bypasses
- Proof of Concept: Evidence of unauthorized data access across user contexts
- Affected Endpoints: List of vulnerable API endpoints and parameters
- Impact Assessment: Classification of data exposure severity
- Remediation Recommendations: Specific fixes for identified vulnerabilities

## Core Workflow

### 1. Understand IDOR Vulnerability Types
Direct Reference to Database Objects — apps reference DB records via
user-controllable parameters:
```
# Original (authenticated as User A)
example.com/user/profile?id=2023
# Manipulation (accessing User B's data)
example.com/user/profile?id=2022
```
Direct Reference to Static Files — apps expose file paths/names that enumerate:
```
# User A's receipt
example.com/static/receipt/205.pdf
# User B's receipt
example.com/static/receipt/200.pdf
```

### 2. Reconnaissance and Setup
- Create Multiple Test Accounts (attacker + victim).
- Identify Object References: numeric IDs in URL / params / body, file paths,
  GUIDs/UUIDs.
- Map User IDs and note patterns: sequential ints, auto-increment, predictable.

### 3. Detection Techniques
URL Parameter Manipulation:
```
GET /api/user/profile?id=1001   Cookie: session=attacker   -> own data
GET /api/user/profile?id=1000   Cookie: session=attacker   -> victim data? (VULN)
```
Request Body Manipulation:
```
POST /api/address/update  {"id":5,"userId":1001,...}
                               -> change userId to 1000 (victim) -> 200? (VULN)
```
HTTP Method Switching:
```
GET  /api/admin/users/1000 -> 403
POST /api/admin/users/1000 -> 200 (VULN!)
PUT  /api/admin/users/1000 -> 200 (VULN!)
```

### 4. Exploitation with Burp Suite
Manual: proxy -> login as attacker -> intercept request with ID -> modify to
victim ID -> forward -> observe victim data.
Intruder (Sniper, Numbers 1-10000) for enumeration. Battering Ram when the
same ID appears in multiple positions (URL + body).

### 5. Common IDOR Locations
- API: /api/user/{id}, /api/profile/{id}, /api/order/{id}, /api/invoice/{id},
  /api/document/{id}, /api/message/{id}, /api/address/{id}/update|delete
- Files: /download/invoice_{id}.pdf, /static/receipts/{id}.pdf,
  /uploads/documents/{filename}, /files/reports/report_{date}_{id}.xlsx
- Params: ?userId=, ?orderId=, ?documentId=, ?file=, ?account=

### Response Analysis
| Status | Meaning |
|---|---|
| 200 OK | Potential IDOR — verify data ownership |
| 403 Forbidden | Access control working |
| 404 Not Found | Resource doesn't exist |
| 401 Unauthorized | Auth required |
| 500 Error | Possible input validation issue |

### Common Vulnerable Parameters
User ids: userId, uid, user_id, account
Resource ids: id, pid, docId, fileId
Order/Tx: orderId, transactionId, invoiceId
Messaging: messageId, threadId, chatId
Files: filename, file, document, path

## Constraints and Limitations
- Requires at least two valid user accounts for verification.
- Some apps use session-bound tokens instead of IDs.
- UUID references harder to enumerate but not impossible.
- Rate limiting may restrict enumeration.
- Some IDOR requires chained vulnerabilities.

### Detection Challenges
- Horizontal (user→user) vs vertical (user→admin) escalation.
- Blind IDOR (response doesn't confirm access).
- Time-based IDOR in async operations.
- IDOR in websocket communications.

### Legal Requirements
- Only test applications with explicit authorization.
- Document all testing activities and findings.
- Do NOT access, modify, or exfiltrate real user data.
- Report findings through proper disclosure channels.

## Examples
Basic ID param IDOR, address-update IDOR, static-file IDOR, Burp Intruder
enumeration, horizontal→vertical escalation — see full prose in
`references/idor_full.md`.

## Troubleshooting
- All 403: try method switching, X-Original-URL / X-Rewrite-URL headers,
  parameter pollution (?id=1001&id=1000), URL-encoding variants, case variants.
- UUIDs instead of sequential: discover via response bodies, JS files, error
  messages, API list responses; try UUIDv1 time-based prediction.
- Session bound to user: test unauthenticated endpoints, password-reset/email
  verification flows, file up/download, API versioning (/api/v1 vs /v2),
  mobile API endpoints.
- Rate limiting: add delays, rotate IPs, target specific high-value IDs,
  off-peak testing.
- Can't verify impact: create unique data in victim account, look for PII
  markers, compare response lengths/timing, use secondary indicators.

## Remediation
- Server-side ownership validation on every object access.
- Use indirect references (/api/address/current-user/billing).
- Never trust client input; validate on server.

## Operator notes (added)
- Phase 0 (no creds): unauthenticated probing to find broken-access-control
  endpoints that return data without a token, and ID-pattern mapping from JS /
  historical URLs. This is legitimate recon and does NOT touch real user data
  if you only record status/length, never persist response bodies.
- Phase 1 (needs 2 accounts + token): true cross-account verification.

### Phase-0 recon script pattern (read-only, non-destructive)
A re-runnable probe that (1) loads discovered URLs, (2) masks ID segments
to templates (`{uuid}`/`{id}`/`{n}`), (3) fires benign opaque-ID GETs
UNAUTHENTICATED, (4) records ONLY status/length (never bodies), (5) flags
200+JSON-without-token as "investigate" and maps ID type per template.
Key output: drives enumeration strategy.

### ID-type lesson (from AbemaTV test)
Object IDs were OPAQUE RANDOM TOKENS (`/v1/users/8a9V7fWLujHBy9`,
`/v1/media/slots/8cciGVqn6uhKtB`), NOT sequential integers. Classic
Intruder enumeration (1->10000) is infeasible. Even if IDOR exists, you
need leaked/guessable victim IDs — only obtainable by being logged in (API
list responses leak other users' IDs) or from the JS bundle. So opaque-token
apps REQUIRE a victim ID source before cross-account testing is possible.

### Unauth-read lead that turned out benign
`/v1/media/slots/{id}` returned 200 + 3537 bytes unauthenticated (GET only;
POST/PUT/DELETE correctly 401). Body was PUBLIC program metadata (title,
cast, schedule, genre) with zero owner/PII fields — confirmed by grepping for
`"(userId|owner|email|name)"`. Slot IDs were already public (JS bundle +
gau history). By-design public endpoint, NOT IDOR. Always inspect the actual
unauth response before flagging — and confirm absence of owner/PII fields.

### Acquiring a victim-ID source — historical URL harvest (reusable)
When object IDs are opaque tokens (no sequential enumeration possible), you still
need REAL victim IDs to test cross-account access. A high-yield, non-obvious
source is the TARGET'S OWN historical URL corpus:
  - gau / waybackurls / alienvault / crt.sh over the in-scope roots.
  - Grep the harvested URL list for object-ref patterns, e.g.
    `/v1/users/([A-Za-z0-9]{8,})`, `/posts/(\d+)`, `/articles/-/(\d+)`.
  - On Abema this yielded 14,851 distinct leaked `/v1/users/{id}` values from
    gau history alone — a ready-made victim-ID wordlist. These are REAL object
    references the app emitted; once you hold ONE authorized session, replaying
    them is the exact BOLA/IDOR test. Save to e.g. `leaked_user_ids.txt`.

### Gating false-positive pitfall (web numeric-ID posts / CMS)
When probing web `/posts/{id}` or `/articles/{id}` endpoints, do NOT conclude
"member/paid content is leaking" just because gating KEYWORDS appear in the
response (会員限定 / 有料 / ログイン / limited / premium / subscribe). On
Ameba Ownd (and most SPA CMSes) those strings live in the global nav/footer
and fire on EVERY page regardless of access control. Verify the actual object
body is served:
  - Extract og:title + the article prose (JSON-LD / `__NEXT_DATA__` `text`
    fields, or the `<main>` body) and confirm real content bytes are returned
    unauthenticated. If the prose is present AND the page is meant to be
    members-only, THAT is the Broken Access Control finding. If it's a public
    promo post, it's a non-issue.
  - A real login wall shows as: 401 status, a redirect to /login, or a body
    that contains ONLY the login form (no article prose). Absence of that =
    content is readable.
  - Pitfall (from abema-ldh LDH posts): a "GATE"-flagged post was 111KB
    vs ~39KB free posts, BUT the extra bytes were unrelated nav/asset bloat,
    not gated content. Always grep the actual prose, not just size/keyword.
  - Further refinement (winticket.jp): when the SPA bundle is gzip-compressed,
    `curl` without `--compressed` saves raw gzip and the secret scanner reads
    binary garbage (false negative). Decompress bundles first — see js-secret-scan §2b.

### Per-target isolated folder + JS-endpoint-extraction workflow
For each new bug-bounty target, put everything in its OWN folder under
`~/Bugbounty/<target>/` (NOT a shared dir) so recon/exploit scripts,
harvested URLs, and findings never cross-contaminate between programs.
  - Write `target.txt` (scope), run subfinder+assetfinder -> `subs_raw.txt`,
    httpx -> `live_hosts.txt`.
  - Pull the SPA bundle manifest (homepage <script src>), download ALL
    `.js` into `js_files/`, then DON'T stop at the secret scan — the bundles
    are the highest-yield IDOR recon source:
      * grep for user-scoped path templates: `/my/...`, `/users/me`,
        `/users/-/{resource}/{id}`, `/{resource}/{id}` with IDs in the PATH.
      * grep object-param names: userId, uid, memberId, orderId, raceId,
        receiptId, transferId, messageId.
      * find the API base: look for `PROXY_ENDPOINT_PREFIX`, `baseURL`,
        `/api/` concatenation — and confirm it live (the api host may 404 while
        the SPA route 403s, meaning the proxy base differs from the obvious host).
  - Save the extracted surface to `idor_surface_from_js.txt` and use it to
    drive the Phase-1 cross-account harness once a token exists.

### Phase boundary — what unauthenticated probing CAN and CANNOT prove
- Unauth probing can ONLY prove: "the edge is correctly 401/403" (good) or
  "an endpoint returns data with no token" (broken). It CANNOT demonstrate a
  TRUE horizontal IDOR, because that requires an attacker session + a victim ID
  returning the VICTIM's data. By definition you need >=1 authorized account.
- Practical split:
  - Phase 0   : unauth edge check + ID-type mapping + harvest victim IDs.
  - Phase 0.5 : unauth LIVE characterization of candidate endpoints (status /
    length / gating check) to rank what to test once authed.
  - Phase 1   : with 1 token, replay leaked victim IDs across GET/POST/PUT/
    DELETE on /v1/users/{id}, /myvideo, /mylist, /gift/messages,
    /favorites/slots; record only status/length + which PII field NAMES appear
    (never persist PII values). Any 200 + owner/PII fields for a victim ID !=
    your own account = IDOR/BOLA. Add a 2nd account to prove horizontal
    escalation and try method tampering.
- Reusable harness: `scripts/idor_crossaccount.py` (Phase-1, token-gated,
  records no bodies). Set BASE to your target API, point IDS_FILE at your
  harvested victim-ID list, paste your token into AUTH_HEADER.

### UI-redaction bypass via alternate endpoint (DevHub CTF, learned live)
A common IDOR app has a VIEW endpoint that masks sensitive fields in the HTML
(e.g. `"api_key": "***REDACTED***"`) but a SIBLING endpoint that returns the same
object in cleartext. On DevHub: `/api/user/<id>` (HTML profile) redacted `api_key`,
but `/api/user/<id>/export` (JSON) returned `"api_key": "<real value>"` for ANY id.
So after confirming IDOR reachability on the redacting endpoint, ALWAYS probe sibling
paths for the same object in raw form:
  - `/api/user/<id>/export`  `/api/user/<id>/raw`  `/api/user/<id>/json`
  - `/api/user/<id>?format=json`  `/api/user/<id>/download`
  - GET with header `Accept: application/json` (sometimes flips HTML view -> JSON)
The flag is frequently the un-masked secret. Also note: IDOR + reach the ADMIN id
(enumerate sequentially; DevHub had `u_101`=me, `u_102`=teammate, `u_8f92a4`=admin —
mixed sequential + opaque, so enumerate the sequential range AND harvest ids from
the `/team` page's own API links).

### Login with in-page captcha (DevHub CTF, learned live)
When a login form shows a math/text captcha, the ANSWER is often rendered in the page
itself (e.g. "What is 9 + 3?") and/or pre-seeded into the session cookie
(`{"captcha_ans":12}`). Decode the Flask session cookie to read it, solve it, then POST
`username=&password=[REDACTED_SECRET]<answer>` (NOT multipart — use
`--data 'k=v&...'` urlencoded, since the form had no enctype). Re-grab the session
cookie after POST so the authenticated session is used for all follow-up requests.

### Reporting style for this operator
Lead with the VERDICT and the single concrete blocker (e.g. "no token yet"), keep
the explanation terse, and push detail into files (IDOR_FINDINGS.md, scripts).
This user wants execution over formality — output the finding + the single next
action, not a methodology lecture.

### Portal-specific: Track-application IDOR (Liferay portlets)
When the endpoint is a **form POST with captcha** keyed on an application number
(the "track your [process] application" pattern), the two-account method is:

1. Account B submits the process (visa application, order, etc.) and you record the
   resulting `reference_number` and `document_number` from their view/create response.
2. Account A (attacker) accesses the track page, solves the captcha, and submits with
   B's numbers. The response that matches B's content is the IDOR proving.

For portal patterns, see `references/track-application-portal-idor.md` for the
track-number lookup pattern and `references/track_idor.py` for a working harness.
