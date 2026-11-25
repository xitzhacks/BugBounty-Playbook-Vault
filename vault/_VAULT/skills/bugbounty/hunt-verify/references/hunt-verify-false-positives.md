# Hunt-Verify — False-Positive Patterns (Session-Accumulated)

Collected from live recon sessions. Before claiming a finding, check these
patterns — each has fooled a hunter (or an automated tool) into a false positive.

---

## 1. Nuclei CVE Hit on Endpoint That Returns "Resource not found"

**Pattern:**
```
[CVE-2022-41697] [http] [medium] https://ghost.ably.com/ghost/api/admin/session
```
Nuclei scans the URL path against a known-vulnerable path pattern and reports a hit
when the endpoint EXISTS — even if it returns a JSON 404/403 "Resource not found"
rather than the actual exploitable behavior the CVE describes.

**Verification:** Hit the endpoint manually. Does it return the vulnerable response
described in the CVE, or just a normal "not found / access denied"? The path
existing ≠ the vulnerability being present.

---

## 2. HTTP 000 from curl = Not an HTTP Response

**Pattern:**
```
curl -skL --connect-timeout 5 "https://api.ably.com" -D - -o /dev/null 2>/dev/null | grep "HTTP:"
# (empty output)
curl ... | grep "HTTP:"; echo → 000
```

**Root causes (troubleshoot in this order):**
1. **DNS failure** — `nslookup api.ably.com` returns NXDOMAIN → host doesn't exist.
2. **Connection refused** — port 443 not listening → curl gets TCP RST, outputs 000.
3. **Timeout** — host resolves but never responds → curl times out, outputs 000.
4. **TLS failure** — cert mismatch or TLS version unsupported → curl aborts, outputs 000.

**Only a finding if:** the service is supposed to be reachable AND consistently
dead (DoS), not just a one-off connection error. Always troubleshoot with the
ladder: `nslookup` → `curl http://` (HTTP fallback) → `curl -k --connect-timeout 3`.

---

## 3. /_next/image Returns 400 — URL Not in Allowlist

**Pattern:**
```bash
curl "https://dashboards.ably.com/_next/image?url=http://169.254.169.254/&w=64&q=75"
# → HTTP 400 "Invalid url"
```
This is the Next.js image optimizer rejecting a URL not in `images.remotePatterns`.
A 400 is the **expected, correct** behavior — NOT a bypass. The optimizer is working.

**Real SSRF confirmation requires:** Either (a) the URL is in the allowlist AND
fetches internal content to the attacker, or (b) an OOB callback fires from your
unique marker. Status code alone is never enough.

---

## 4. CORS Header Present But No Credentials Flag

**Pattern:**
```
Access-Control-Allow-Origin: https://evil.com
(no Access-Control-Allow-Credentials: true)
```
Without `Access-Control-Allow-Credentials: true`, the browser will NOT send
cookies/Authorization headers on the cross-origin request → no credentialed
data read → NOT exploitable. Look for BOTH headers.

**Variant:** `Access-Control-Allow-Origin: *` with `Access-Control-Allow-Credentials: true`
is an invalid combo and browsers reject it. Only `null` or a specific origin
with credentials=true is exploitable.

---

## 5. Middleware Bypass Returns Different 200 Body But Still Blocked

**Pattern:**
```bash
# WITHOUT header:
curl "https://TARGET/api/v1/apps"
# → {"error":"Unauthorized"}, HTTP 200

# WITH x-middleware-subrequest:
curl -H "x-middleware-subrequest: middleware:middleware:middleware:middleware:middleware" "https://TARGET/api/v1/apps"
# → {"error":"Unauthorized"}, HTTP 200
```
Same body, same response → bypass did NOT work. The middleware either isn't
in the path for this route, or auth is enforced server-side (not in middleware).

**True bypass sign:** The body changes to include protected content (admin UI
HTML, PII data, tokens), NOT just a different status code or error message.

---

## 6. S3 Bucket Returns 403 — Bucket Exists But Private

**Pattern:**
```bash
curl "https://target-bucket.s3.amazonaws.com/"
# → HTTP 403 AccessDenied
```
This is NOT a misconfiguration. A private bucket correctly returns 403 for
unauthenticated listing. The exploitable case is 404 (bucket doesn't exist)
vs 403 (bucket exists and is private). Report only if you can list/get objects.

**Real finding requires:** 200 with bucket listing, or a specific object
accessible via a signed-URL bypass, or `s3:GetObject` permission on a test file.

---

## 7. Cloudflare WAF Blocks After Initial Access (403 Forbidden)

**Pattern:**
- Initial recon: endpoint returns data (e.g., `/api/token` returns a token)
- After a few requests: all subsequent requests return 403 Forbidden
- This is **rate limiting / bot protection**, not a vulnerability

**Mitigation:** Slow down requests, use rotating user agents, or rotate IPs.
Do NOT report "endpoints return 403" as a finding — that's the edge working.

---

## 8. Subdomain Resolves to CNAME of Another Service (Not Takeover)

**Pattern:** A subdomain has a CNAME pointing to a service (e.g., Heroku, Vercel)
that IS still active. The CNAME resolves fine, returns 200 or a proper error.

**Real takeover requires:** A CNAME pointing to a DELETED/UNCLAIMED service
that returns "No such app" or similar. A properly anchored CNAME is NOT takeover.

---

## Quick Triage Checklist

Before filing any report, run through:
- [ ] Did the endpoint actually return the vulnerable behavior, or just exist?
- [ ] Is HTTP 000 from a real HTTP response — is the service supposed to be up?
- [ ] Did the bypass return DIFFERENT content, not just a different status code?
- [ ] Did the SSRF fire an OOB callback with a UNIQUE marker?
- [ ] Does the CORS misconfig include `Access-Control-Allow-Credentials: true`?
- [ ] Does the S3 bucket return 403 (private) or 200 (misconfigured)?
- [ ] Is the 403 from Cloudflare bot protection, not the application being broken?
- [ ] Can I reproduce this from a clean browser with no prior cookies?
