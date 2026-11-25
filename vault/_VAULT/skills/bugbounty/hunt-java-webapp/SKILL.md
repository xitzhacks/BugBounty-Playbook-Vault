---
name: hunt-java-webapp
description: Hunt Java enterprise web applications and portals — Liferay JSONWS API enumeration, DWR (Direct Web Remoting) interface discovery and unauthenticated method invocation, jvmRoute/servlet-container fingerprinting, sibling-webapp discovery via SSO/IdP endpoints, and F5 BIG-IP ASM WAF recognition. Use when a target fingerprints as Java (jvmRoute cookie, JSESSIONID, .jsp, Liferay/Spring/Apache-Coyote headers) or when you find a /dwr/ path, a JSONWS catalog, or an enterprise portal with an SSO sidecar app.
sources: live-assessment
report_count: 1
---

## When to use this skill

Trigger when ANY of these appear:
- Cookie named `JSESSIONID`, or a value containing `jvmRoute` (e.g. `jvmRouteeVisaNode1`, `.jvmRouteevlifeb02`) — that is a Java servlet container load-balancer route, definitive proof of a Java backend.
- A path `/dwr/`, `/dwr/engine.js`, `/dwr/interface/*.js`, or `*.dwr` in JS bundles.
- Liferay: `/api/jsonws`, `/en/api/jsonws`, `p_auth` tokens, `p_p_id` / `p_p_lifecycle` params, portlet namespaces like `_Some_WAR_someportlet_`.
- A portal that has a separate `/SomeApp/` context with its own `JSESSIONID` path and an `/idpAuthRequest` or SSO bridge.
- Server headers `Apache-Coyote/1.1`, `Liferay-Portal`, `X-Powered-By: Servlet`, or a `TS01xxxxxx` cookie (F5 BIG-IP ASM).

DO NOT use for: pure PHP/Node/ASP.NET targets (use the stack-specific `hunt-*` skill).

---

## The core insight: Java portals leak a machine-readable API surface

Enterprise Java portals are built from remoting frameworks that publish the
server-side method catalog to the browser so the UI can call it. That catalog is
**frequently readable without authentication**, and the remoting endpoints
**frequently lack an auth filter** — the developers secured the *pages* (which
redirect to login) but not the *remoting servlet* underneath them.

Three surfaces to enumerate, in order of yield:

1. **DWR** (`/dwr/interface/*.js` + `/dwr/call/plaincall/*`) — highest yield.
   Publishes every Java method name + arity, and often executes them unauthenticated.
2. **Liferay JSONWS** (`/api/jsonws`) — full service catalog; needs a `p_auth`
   token but the catalog itself and many `get*` methods are reachable.
3. **SSO/IdP sidecar apps** — a second webapp under its own context path, often
   with its own weaker auth model and its own remoting endpoints.

---

## Phase 1 — Fingerprint (2 minutes)

```bash
# definitive Java signal: jvmRoute in a cookie value
curl -skI https://TARGET/ | grep -i 'set-cookie'
# Liferay?
curl -sk https://TARGET/ | grep -iE 'liferay|p_auth|p_p_id|portlet'
# what version?
curl -sk https://TARGET/api/jsonws 2>/dev/null | grep -oiE 'liferay[^"<]{0,40}'
```

Record: container (Tomcat/JBoss/WebLogic/WildFly), portal (Liferay/Spring/Jetspeed),
WAF (see Phase 4), and every distinct `JSESSIONID` *path* (each one is a separate app).

---

## Phase 2 — DWR enumeration (the high-yield path)

### 2.1 Find the interfaces

DWR ships a JS stub per exposed interface. They are public by design:

```bash
for f in $(curl -sk https://TARGET/APP/ | grep -oE 'dwr/interface/[a-zA-Z0-9_]+\.js' | sort -u); do
  echo "=== $f"; curl -sk "https://TARGET/APP/$f" | grep -oE 'p\.[a-zA-Z0-9_]+ = function\([^)]*\)'
done
```

The regex output gives you **every method name and its parameter arity**. A method
named `delete*`, `update*`, `post*`, `send*`, `save*`, `create*` is a write path —
note it. `get*`, `check*`, `validate*`, `verify*` are read/validation paths that
often leak data or act as oracles.

### 2.2 Reverse the wire protocol from engine.js

Do NOT guess the body format. It is in `dwr/engine.js`:

```bash
curl -sk https://TARGET/APP/dwr/engine.js -o engine.js
grep -o 'constructRequest:function.\{0,2000\}' engine.js
```

Look for how it builds `c0-scriptName`, `c0-methodName`, `cN-p0`, `callCount`,
`batchId`, `scriptSessionId`, `page`.

### 2.3 Invoke a method

Use `scripts/dwr_client.py` (ships with this skill). Minimal manual form:

```
POST /APP/dwr/call/plaincall/<interface>.<method>.dwr
Content-Type: text/plain

c0-scriptName=<iface>&c0-methodName=<method>&c0-id=0
&c0-p0={"httpMethod":"POST","script":"null","pageId":"/APP/<page>"}
&c1-scriptName=<iface>&c1-methodName=<method>&c1-id=0&c1-p0="arg0"
&callCount=2&batchId=1&instanceId=0
&page=%2FAPP%2F<page>&scriptSessionId=<any-uuid>&windowName=
```

### 2.4 The iterative param-discovery trick

If the body is wrong, DWR tells you **exactly which param is missing**, one at a
time:

```
{"__error__":"java.lang.IllegalArgumentException",
 "msg":"Failed to find parameter: scriptSessionId (check server log for more info)."}
```

Add it, resend, get the next one. The observed sequence on a real target:
`scriptSessionId` → `page` → `callCount` → `c0-scriptName`. Four iterations and
you have the working format. This is the fastest way to bootstrap an unknown DWR
deployment — treat each error as a free spec hint.

### 2.5 Parse the response

DWR replies are **JavaScript object literals, not JSON** (unquoted keys, single
quotes, `\uXXXX` escapes):

```javascript
//#DWR-REPLY
dwr.engine.remote.handleCallback("1","0",[{visaTypeId:"29",visaTypeName:"GCC Resident Visa",...}]);
```

Strip the `handleCallback(...)` wrapper, then convert the JS literal to JSON
(quote bare keys, normalise quotes). See `scripts/dwr_client.py` for a working
parser. `handleException(...)` means the call reached the server and threw —
that is still a reachability signal.

---

## Phase 3 — Liferay JSONWS

```bash
curl -sk https://TARGET/api/jsonws            # full catalog (~400KB), often public
curl -sk "https://TARGET/api/jsonws/context.list"   # list all service contexts
```

Custom contexts reveal the app's own service layer (`listtype`, `assetcategory`,
`journalarticle`, etc.). Every method needs `p_auth`; obtain it from any page
(`grep -o 'p_auth=[^&"]*'`). Unauthenticated calls fail with
`Invalid authentication token` — but the *catalog* and error differentials are
still intel. Test `get*` methods with `p_auth` from a low-privilege session.

---

## Phase 4 — Sibling apps and WAF

### Sibling-app discovery

A portal often fronts a second webapp. Look for a context path that 303-redirects
to the portal logout (`/c/portal/logout`) — that means "you are not authenticated
to *this* app" — and probe for an SSO bridge:

```bash
curl -sk -o /dev/null -w '%{http_code} %{redirect_url}\n' https://TARGET/SomeApp/
curl -sk https://TARGET/SomeApp/idpAuthRequest   # SSO/IdP handshake page
```

A page that returns 200 with its own JSESSIONID path is a **separate application**
with a separate auth model. Map its JS (`/SomeApp/js/*.js`) — its remoting
endpoints are usually weaker than the main portal's.

### F5 BIG-IP ASM WAF recognition

Signals:
- Cookie `TS01<hex>` (and often a second `TS01xxxxxx`).
- Body: `<title>Request Rejected</title> ... Your support ID is: <digits>`.

Behaviour: **signature + rate based, not an app fix.** It may allow a method name
today and block it tomorrow after volume. Two operational consequences:
- A tester must warm the session first (GET the hosting page) and throttle/rotate,
  or the WAF starts rejecting bare POSTs.
- A defender cannot rely on it — report the underlying missing-auth, not the WAF.
- Seeing the WAF appear mid-test is itself an IR observation (see
  `mid-engagement-ir-detection`).

---

## Phase 5 — Deciding what is a finding

| Observed | Verdict |
|---|---|
| Reference/config data returned unauthenticated (categories, type catalogs, service status) | **Report** — CWE-306 / CWE-200, Medium. Concrete data disclosed + whole method surface exposed. |
| Internal error strings / Java class names leaked | Include as supporting evidence, not standalone. |
| A `delete*`/`post*` method returns `true`/`false` unauthenticated with no confirmed data change | Report as **"mutating method has no auth check in front of it"** (CWE-306). Do NOT claim a write you did not confirm. |
| Another user's PII actually returned | Critical IDOR — but prove it with **two accounts you control** (A reads B), never by enumerating real users. |
| Only the method *names* are public, everything throws | Low/Informational — attack-surface disclosure. Still worth a note. |

### Before you answer "is there user data leaked?"

An unauthenticated endpoint returning 167 records *looks* like a breach. Almost
always it is reference data, and the difference between a defensible Medium 5.3
and a killed Critical is an **audit, not an impression**. Run
`scripts/pii_audit.py <artifacts-dir> --own-marker <your-test-data>`:

1. Regex-scan every artifact for PII shapes.
2. **RESOLVE every hit with context** — this is the actual work. Real resolutions
   from a Java-portal assessment: Liferay CMS `articleId`, Google Analytics
   property ID, HSTS `max-age`, epoch-ms build timestamps, framework constants,
   the tester's own placeholders, and the site's public footer contact details.
   Ten of ten benign. A regex match is a question, not an answer.
3. **Check JSON field NAMES**, not just values — value-regex misses
   unanticipated formats; a field named `passportNumber` cannot hide.
   `personal-data fields: NONE` + the field list is what a triager accepts.

Never claim a leak you resolved as benign, and never deny one you didn't
resolve. Full worked table + report block in
`references/pii-vs-breach-triage.md`.

### Prove IDOR with two accounts, never by enumeration

Reading real applicants' records to "prove" an IDOR is data theft, and reports
built on it get rejected. The proof is: account A requests account B's record,
one captured request/response pair. "A can read B" is the finding. If the
reference-data surface is clean, the PII question lives on the endpoint keyed on
a user-controlled ID, and it is answered with A-reads-B only.

**Evidence bar:** capture the verbatim request/response pair, the exact URL, and
the cookie state (or "no cookies — unauthenticated"). One clean pair per finding.

---

## Pitfalls

- **Don't grind a blocking gate — pivot to an alternate surface.** If a captcha /
  2FA / rate-limit blocks the path you picked, STOP solving the gate and enumerate
  for a different surface on the same target. On a live assessment, hours went into
  captcha OCR before the actual win — an unauthenticated DWR app — was found by
  simply probing a sibling context path. The gate was never the way in.
- **Fingerprint the stack BEFORE firing a version-specific CVE PoC.** A PHP RCE
  chain (e.g. `session.upload_progress` UAF) does nothing against a Java target.
  `jvmRoute` in a cookie ⇒ Java ⇒ a PHP exploit is wasted traffic. Check the stack,
  then pick the exploit.
- **Validate an exploit in a local lab, not on production.** Build the vuln's
  Docker lab, confirm the primitive and the chain there, and report the lab
  evidence. Firing a pre-auth RCE at a production host is impact, not proof — and
  on a non-consented host it is a crime, not a finding.
- **`scriptSessionId` can be any UUID at first, then stop working.** Early calls
  succeed with a random UUID; after volume the server/WAF may demand a
  server-issued session. If calls start throwing, re-warm the session and rotate.
- **DWR responses are not JSON.** A strict `json.loads` will fail. Parse JS literals.
- **The `cN` wire index is POSITIONAL, not the Java parameter number.** The
  `.js` stubs name parameters `p0..pN` and they **skip indices** when a Java
  param is excluded — e.g. `deleteDocument(p0, p2, callback)` or
  `getSearchVisaResult(p0..p10, p12, callback)`. If you build `cN` blocks from
  the Java parameter numbers you get
  `Failed to find parameter: cN-id` / `cN-scriptName` on a call whose format is
  otherwise correct. Build the arg blocks by **position** (`c1`, `c2`, ... in the
  order the args appear), one block per argument. Debugging signature: the error
  names a `cN` index *above* your argument count — that means your indexing
  scheme, not your body, is wrong.
- **Args go in their own `cN` blocks, not appended to `c0`.** `c0` carries the
  call metadata (`scriptName`/`methodName`/`id`/`p0` = the call struct); each
  argument gets a full block with its own `scriptName`+`methodName`+`id`+`p0`.
  Putting args as `c0-p1..` yields `Failed to find parameter: c1-id`. Both
  variants appear in the wild — if one errors, try the other, but check the
  error's `cN` index against what you sent.
- **Reuse one `Dwr` client across many calls and later calls silently fail.**
  On a long enumeration run the shared session accumulates state and methods
  that worked start throwing generic `java.lang.Throwable`. Use a **fresh
  session per method** for enumeration, and treat a sudden uniform
  "everything throws" as state contamination, not as the target changing.
- **A `p_auth` token is per-session and ephemeral.** Re-scrape it after every login;
  a stale token yields "Invalid authentication token", not a permission error.
- **Blank/red captcha image = session/auth mismatch.** The captcha is bound to the
  session that fetched it; fetch it in the same `requests.Session` that submits.

---

## Related skills

- `bb-methodology` — PART 0 mode confirmation and the 5-phase workflow this skill plugs into.
- `mid-engagement-ir-detection` — WAF appearing mid-test is a defensive observation worth logging.
- `evidence-hygiene` — request/response capture and redaction for the report.
- `hunt-idor` — once you have two accounts, for the A-reads-B proof pattern.
- `report-writing` — report format for the platform in scope.

## Support files

- `scripts/dwr_client.py` — working DWR v2 client: interface enumeration, method
  invocation with correct wire format, JS-literal response parser, iterative
  missing-param discovery.
- `references/java-portal-fingerprints.md` — Liferay/JSONWS notes, jvmRoute and
  F5 ASM signatures, sibling-app discovery recipe, and the observed
  error-sequence for bootstrapping an unknown DWR deployment.
- `references/pii-vs-breach-triage.md` — how to prove an unauthenticated
  data-exposure finding is NOT a breach: the resolve-every-hit table, the
  field-name structured check, and the report block that makes a Medium 5.3
  defensible instead of an overclaimed Critical.
- `scripts/pii_audit.py` — regex-scan + context-resolution + JSON field-name
  audit over an artifacts directory. Run it before answering "is user data
  leaked?"
