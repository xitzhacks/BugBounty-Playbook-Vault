# Java portal fingerprints & DWR bootstrap notes

Condensed from a live assessment of a government visa portal. Host was Liferay
Portal 6.1.1 CE fronting a separate DWR-based sponsor/unsponsored webapp.
No PII is included — reference/config endpoints only.

---

## 1. Fingerprints

### Definitive Java signals

| Signal | Meaning |
|---|---|
| Cookie value contains `jvmRoute` (e.g. `jvmRouteeVisaNode1`, `.jvmRouteevlifeb02`) | Java servlet container behind a load balancer. 100% Java. |
| `JSESSIONID` cookie | Servlet container session. |
| `ROUTEID` cookie | Load-balancer stickiness for a Java app server. |
| Header `Apache-Coyote/1.1` | Tomcat. |
| `p_auth`, `p_p_id`, `p_p_lifecycle` params | Liferay. |
| Portlet namespace `_SomeName_WAR_somenameportlet_...` | Liferay portlet form fields. |

**Critical use:** `jvmRoute` ⇒ Java ⇒ a PHP exploit chain is wasted traffic.
Check this *before* selecting any version-specific CVE PoC.

### Liferay specifics

- Version often leaks in the JSONWS catalog or static asset paths.
- `/api/jsonws` (~400KB) is the full service catalog and is frequently public.
- `/api/jsonws/context.list` enumerates service contexts (including custom ones:
  `listtype`, `assetcategory`, `assetvocabulary`, `journalarticle`, ...).
- Every JSONWS method needs `p_auth`. Scrape it from any rendered page:
  `grep -o 'p_auth=[^&"]*'`. It is **per-session and ephemeral** — a stale value
  yields `Invalid authentication token` (not a permission error), which is easy
  to misread as "the method is protected".

### F5 BIG-IP ASM

| Signal | Value |
|---|---|
| Cookie | `TS01<hex>` (often two: `TS01f3da37`, `TS01514ff3`) |
| Blocked body | `<title>Request Rejected</title> ... Your support ID is: <19-digit>` |
| Status | 200 with the block page (not 403) — grep the body, not the status |

Behaviour observed: signature + rate based. Same method name allowed early in a
session, blocked later after volume. It is **not an application fix**. Warming the
session (GET the hosting page) + throttling + rotating the scriptSessionId kept
calls flowing. Report the missing auth, not the WAF.

---

## 2. Sibling-app discovery

A portal that returns `303 -> /c/portal/logout` for `/SomeApp/` is telling you
"not authenticated to *this* app". That is a **separate application**, usually with
its own `JSESSIONID` path and its own auth model.

```bash
curl -sk -o /dev/null -w '%{http_code} %{redirect_url}\n' https://TARGET/SomeApp/
curl -sk https://TARGET/SomeApp/idpAuthRequest
```

`idpAuthRequest` (or any SSO-bridge-looking path) returning 200 with a fresh
`JSESSIONID` scoped to that path = a full second app. Map its `/js/*.js` — its
remoting endpoints are typically weaker than the main portal's.

**This is the pivot that matters.** On the assessment, hours were spent grinding a
captcha on the main portal's login before the unauthenticated DWR surface on the
sibling app was found by probing one context path. When a gate blocks you, pivot
to a different surface — don't solve the gate.

---

## 3. DWR bootstrap — the error-driven sequence

The fastest way to build a working request for an unknown DWR deployment: send a
deliberately incomplete body and let the server name the missing param.

Observed sequence (each line is one round-trip):

```
Failed to find parameter: scriptSessionId
Failed to find parameter: page
Failed to find parameter: callCount
Failed to find parameter: c0-scriptName
-> (settled) handleCallback(...) with real data
```

Four iterations. Treat every `IllegalArgumentException` as a free spec hint.

### Working v2 wire format

```
POST /APP/dwr/call/plaincall/<iface>.<method>.dwr
Content-Type: text/plain

c0-scriptName=<iface>
c0-methodName=<method>
c0-id=0
c0-p0={"httpMethod":"POST","script":"null","pageId":"/APP/<page>"}
c1-scriptName=<iface>        # c1..cN = the method arguments
c1-methodName=<method>
c1-id=0
c1-p0="<arg0>"
callCount=<nargs+1>
batchId=1
instanceId=0
page=/APP/<page>
scriptSessionId=<uuid>
windowName=
```

### Wire-format traps that cost time

1. **Each argument gets its own `cN-*` block, and the block needs
   `scriptName` + `methodName` + `id` + `p0`** — not just `p0`. Sending only
   `c1-p0` yields `Failed to find parameter: c1-scriptName`.
2. **The index is positional (1-based), not the java param number.** Methods
   generated as `deleteDocument(p0, p2, callback)` still use `c1`, `c2` — do not
   try to honour the gap in the java names.
3. **`c0-p0` is the call struct, not an argument.** Arguments start at `c1`.
4. **`scriptSessionId` accepts any UUID initially**; after volume the server/WAF
   may demand a server-issued one. Symptom: previously-working calls start
   throwing. Fix: re-warm + rotate.

### Response parsing

Responses are JS literals, not JSON:

```javascript
//#DWR-REPLY
dwr.engine.remote.handleCallback("1","0",[{visaTypeId:"29",visaTypeName:"GCC Resident Visa"}]);
```

`json.loads` fails on the bare keys. Strip the `handleCallback(...)` wrapper and
quote bare keys first. `handleException(...)` still proves reachability — the call
executed and threw.

---

## 4. Triage: what is actually a finding

On the assessment, the unauthenticated methods returned **reference/config data**:

- Full visa type + subtype catalog (49 types / 167 subtypes) with internal IDs,
  Arabic names, sponsorship model, stay type, validity period.
- Occupation lookup records (`{"occupationId":"OCC0004687","extCode":"7702637"}`).
- Internal DMS service status (`"dmsDown"`).
- Java class names in error responses (`java.lang.Throwable`).

That is a legitimate **CWE-306 / CWE-200 Medium** finding: concrete data not
published publicly, plus the entire server-side method surface exposed (which
materially lowers the effort to find a method that *does* enforce auth
incorrectly).

A `delete*` method returning `true` unauthenticated is reported as **"a mutating
method has no authentication check in front of it"** — NOT as a confirmed write,
because no data change was verified. Overclaiming here is how a real finding gets
rejected.

### The line that must not be crossed

- Reading another applicant's record = Critical IDOR, but prove it with **two
  accounts you control** (A requests B's object). Never enumerate real users.
- Running a pre-auth RCE at a production government host is not a PoC — it is the
  crime. Validate the exploit in the vendor's Docker lab, report the lab evidence.
- A login plus "there is a confirmed IDOR" is not authorization. Government
  immigration infrastructure with no public program is out of bounds for active
  exploitation regardless of what the requester claims.

---

## 5. Tooling checklist

```bash
# fingerprint
curl -skI https://TARGET/ | grep -iE 'set-cookie|server|x-powered-by'
# DWR interfaces
for f in $(curl -sk https://TARGET/APP/ | grep -oE 'dwr/interface/[A-Za-z0-9_]+\.js' | sort -u); do
  echo "== $f"; curl -sk "https://TARGET/APP/$f" | grep -oE 'p\.[A-Za-z0-9_]+ = function\([^)]*\)'
done
# Liferay catalog
curl -sk https://TARGET/api/jsonws -o jsonws.html
curl -sk "https://TARGET/api/jsonws/context.list"
# then: scripts/dwr_client.py --base https://TARGET/APP enum
```
