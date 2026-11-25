---
name: hunt-verify
description: Verification discipline for hunt-* skill findings - systematic prove-then-report playbook after each hunt-* technique fires.
category: bugbounty
---

# HUNT-VERIFY — Verification Discipline for Hunt Findings

## When to use

After ANY hunt-* skill test produces a "maybe interesting" response:
- Status code changed but body is identical (e.g., 200 vs 302)
- Status code stayed the same but body changed
- A header appeared/disappeared (CORS, auth cookie, CSP)
- Nuclei flagged something (CVE, misconfig, etc.)
- An API returned different error messages for valid vs invalid inputs

Do NOT report or mark severity until all applicable checks below pass.

---

## The Verification Gates

> Gates 1–5 verify a **positive** candidate. Gate 6 verifies a **negative** sweep — run it
> before publishing any "0 findings" result.

### Gate 1: With-Header vs Without-Header Differential

**Applied when:** Testing auth bypass, middleware bypass, SSRF URL allowlist, WAF bypass, cache poisoning.

Pattern used in practice:

```bash
# WITHOUT the bypass header - establishes baseline (blocked)
echo "=== WITHOUT header ==="
curl -skL --connect-timeout 10 "https://TARGET/protected/path" \
  -D - -o /tmp/without_body -w "HTTP %{http_code}" 2>/dev/null

# WITH the bypass header/payload - establishes test condition
echo "=== WITH bypass ==="
curl -skL --connect-timeout 10 \
  -H "x-middleware-subrequest: middleware:middleware:middleware:middleware:middleware" \
  "https://TARGET/protected/path" \
  -D - -o /tmp/with_body -w "HTTP %{http_code}" 2>/dev/null

# COMPARE: use real content diff, not just status codes
diff /tmp/without_body /tmp/with_body | head -20
```

**The trap:** Many apps return HTTP 200 for BOTH the login wall AND the real page. Status code match does NOT mean bypass failed. Always diff the body content and look for protected content markers (admin panels, PII, tokens, data tables) - NOT just the status code.

**Real-world example:** CVE-2025-29927 on a Next.js dashboard:
- WITHOUT header: 200 "Sign in to Ably Dashboards" login wall
- WITH header: 200 {"error":"Unauthorized"} (API) - different content but still blocked
- True bypass would return: 200 + actual dashboard HTML with user data

**Also apply to:**
- /_next/image SSRF: 400 (rejected by allowlist) is NOT a bypass. Look for actual image bytes or OOB callback.
- CORS: Access-Control-Allow-Origin: https://evil.com AND Access-Control-Allow-Credentials: true must BOTH be present AND you must be able to read a response body cross-origin.
- WAF bypass: status code same but response body length differs or content differs - check if the payload actually reached the backend.

### Gate 2: Unique-Marker OOB Gate

**Applied when:** Testing blind SSRF, blind SSTI, blind SQLi, command injection without output reflection.

Pattern:

```bash
# Generate a unique marker per test - never reuse "test" or "123"
MARKER="zqx$(date +%s)-$(openssl rand -hex 8)"
COLLAB="$MARKER.collab.example.com"

# 1) Inject the unique callback target
curl -s "https://TARGET/vulnerable-endpoint?url=http://$COLLAB" -o /dev/null

# 2) Wait, then check for the callback
curl -s "https://$COLLAB_DNS_PROVIDER/api/v1/records" | grep "$MARKER"
```

**Why unique markers matter:** Shared/reused OOB targets get noise from other scanners/tests. A unique marker confirms YOUR specific request reached the callback.

False-positive guards:
- 400/403 on the endpoint itself is NOT SSRF. The WAF may block http://169.254.169.254 but allow http://localhost:8080.
- If the response body is empty or a static error, the request was likely rejected at the edge (WAF, allowlist) - not processed by the backend.
- A successful SSRF often returns an error from the internal service (different error message than the WAF rejection) OR a valid response (image bytes, HTTP 200 from internal).

### Gate 3: Body-Content Match (Not Just Status)

**Applied when:** Any finding that relies on status codes (200/403/401/302).

```bash
BODY=$(curl -s "https://TARGET/protected/path")
echo "$BODY" | grep -oiE "(admin|profile|settings|api_key|token|email|role|password|user_id)" | sort -u
```

**The trap:** /_next/data/BUILD_ID/admin/users.json may return 200 but the body is {"not-found": true} - a Next.js 404 JSON, not actual data. The API route returns 401 with {"error":"Unauthorized"} - not auth bypass, the auth check is working.

### Gate 4: Repro-from-Scratch (10-Minute Rule)

**Applied when:** You think you have found something and are about to write a report.

1. Open an incognito/private browser window (NO cookies from any prior session).
2. Follow your EXACT steps from the report.
3. Arrive at the protected resource without valid credentials.
4. If you cannot reproduce it in 10 minutes, the finding is not solid.

### Gate 5: State-Change Requirement (for non-Informational)

**Applied when:** A bypass finding claims auth was circumvented.

Ask: What can the attacker DO right now?
- Authenticate as another user - ATO
- Access admin functions - privilege escalation
- Read other users' data - IDOR
- Execute commands - RCE

If the answer is only "I got a 200 instead of 302" or "I see an error message that reveals info" - that is Informational or Low, not Critical. No state change means appropriate severity capping.

### Gate 6: Negative-Result Validity (only for "0 findings" sweeps)

**Applied when:** about to publish ANY sweep that found nothing — "0/180 XSS", "no reflections",
"no IDOR", "no takeovers". A negative is a claim, and it needs evidence that the harness actually
inspected something. Two silent harness bugs in one session produced two false negatives:

- **Execution-form bug.** `m.execute_script("JSON.stringify({...})")` returns **`None`** (no
  exception) because Marionette evaluates the script as a function body. Every probe "returned
  nothing", the loop's `if d.get("x")` was falsy, and 180+ checks reported a clean target without
  inspecting a page. Only `return <expr>` yields a value — see `browser-isolation`.
- **Marker-substring bug.** The detector grepped for `H1Xtag1234` while the canary actually sent
  was `H1X"tag1234'<>/` — the inserted quote broke the match, so a *real* reflection was logged as
  "no reflection". Identical request counts: buggy run = 0 reflections, fixed run = 1.
  Rule: `canary = marker + hostile_suffix`, never interleave characters into the marker.

Mandatory checks before a negative ships:

```
[ ] Positive control passed: one known-reflecting input (or assert m.execute_script("return 1+1")==2)
    produced a hit in THIS run, with THIS harness.
[ ] Row count matches the plan (params × routes). A short file means the loop aborted, not "clean".
[ ] Per-probe error line is visible — a run of `err=...` / `None` must scream, not hide behind hits=0.
[ ] Every "reflection" was classified (emitted escaped? inside a framework state blob? text/plain?)
    BEFORE it was counted as a miss. Unclassified != absent.
[ ] Kill the two classic false-positive classes first: framework state blob (__INITIAL_STATE__,
    __NEXT_DATA__, ngrxState) and non-HTML content types (text/plain + nosniff, Accept: text/html
    -> 406). Both make "everything reflects, nothing is vulnerable" look like a finding.
```

**Blocked is not negative.** A run that dies on a WAF page (`Attention Required! | Cloudflare`),
a timeout, or a killed process proves nothing about the target. Persist the state *inside* the
artifact so a future session cannot misread it:

```json
{"rows": [{... "blocked": true, "t": "Attention Required! | Cloudflare"}], "hits": []}
```

A 1-row or truncated JSON is an **aborted** run. If you cannot reconstruct the original run,
say so explicitly — never cite the partial file as a "0 findings" result. When an analytic
argument exists (e.g. static sink trace: zero `location.*`/`queryParams` -> markup-sink edges),
prefer it over a payload run: it is reproducible and immune to WAF budget.

**Keep your failed run as the control.** After fixing a harness bug, the delta between the two
runs on identical inputs (0 vs 1 reflection; 0 vs N executions) is the strongest evidence that
the fix mattered — and it tells the next session which file to trust.

---

## False-Positive Catalog (Common in practice)

| Symptom | Actual cause | Verdict |
|---------|-------------|---------|
| 400 on /_next/image?url=http://169.254.169.254/... | URL not in images.remotePatterns allowlist - normal | NOT VULNERABLE |
| 403 on /admin + 403 on /_next/image | Cloudflare/WAF edge block, not backend logic | Need different bypass vector |
| Nuclei flags CVE on endpoint returning "Resource not found" | Scanner matched endpoint name, not actual vulnerable response | FALSE POSITIVE |
| /ghost/api/admin/session -> 404 | Endpoint does not exist in this Ghost version | FALSE POSITIVE |
| x-middleware-subrequest returns same response with/without header | Middleware not in path, or auth is server-side | NOT VULNERABLE |
| CORS header present but no Access-Control-Allow-Credentials: true | Cross-origin read blocked - credentials not sent | NOT VULNERABLE |
| S3 bucket returns 403 (not 404) | Bucket exists but private | NOT VULNERABLE |
| Subdomain returns 404 on CloudFront | CloudFront returns 404 for unknown host | Need NoSuchBucket to confirm |
| HTTP 000 from curl | Connection failed (DNS, timeout, TLS) - NOT an HTTP response | Troubleshoot connectivity |

HTTP 000 troubleshooting ladder:
1. nslookup host - if NXDOMAIN, host does not resolve
2. curl -v http://host/ (HTTP not HTTPS) - if works, TLS/cert issue
3. curl --connect-timeout 3 -k https://host/ - if works, DNS/TTL delay
4. Only report HTTP 000 as a finding if it is consistent service denial

---

## Related Skills & Chains

- All hunt-* skills - This verification playbook runs AFTER any hunt-* skill produces a candidate finding. The 4 gates convert interesting-response to verified, reportable vulnerability.
- triage-validation - The upstream gate that decides whether a finding survives severity assignment. hunt-verify feeds into it.
- evidence-hygiene - Redaction and PoC structure. Once hunt-verify says confirmed, evidence-hygiene handles proof capture.