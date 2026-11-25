---
name: ssrf
description: >-
  Systematic methodology for identifying, verifying (within authorized scope),
  and documenting Server-Side Request Forgery (SSRF) vulnerabilities in web
  applications and APIs. Covers basic/blind/semi-blind SSRF, injection points
  (URL params, webhooks, file/image fetch, PDF generators, XXE, GraphQL),
  localhost and filter bypasses, cloud metadata (169.254.169.254) exploitation,
  OOB/collaborator detection, and remediation. Use when an endpoint takes a
  URL/host/file reference the server will fetch server-side.
---

# SKILL: SSRF Vulnerability Testing

## Purpose
Provide a repeatable methodology for finding Server-Side Request Forgery: a class
of bug where an attacker makes the *server* issue HTTP/other requests to an
attacker-chosen destination — internal services, cloud metadata, or the
attacker's own host (for blind confirmation).

## Inputs / Prerequisites
- Target application with any "fetch this URL / import / webhook / proxy" feature
- An OOB / collaborator endpoint for BLIND SSRF (e.g. interactsh, Burp
  Collaborator, your own hostname) — REQUIRED for blind confirmation
- Intercepting proxy (Burp / Caido)
- Authorization (written permission) for the in-scope target
- Understanding of which features cause server-side outbound requests

## Outputs / Deliverables
- SSRF Vulnerability Report (type: basic / blind / semi-blind)
- Proof of Concept (response reflection, or OOB interaction log)
- Affected endpoints + the exact parameter
- Impact Assessment (internal pivot, cloud cred theft, port scan, RFI)
- Remediation Recommendations

## Core Workflow

### 1. Understand SSRF Types
- Basic SSRF: server fetches the URL and returns the response to you
  (easy to see — e.g. "preview this URL" returns page contents).
- Blind SSRF: server fetches but response is never shown. Confirm via
  Out-Of-Band (OOB) interaction hitting your collaborator host.
- Semi-blind: timing/error differences reveal success/failure.

### 2. Find Injection Points (where does the server fetch?)
Highest-signal features:
- URL preview / "paste a link" / og:image fetchers
- Avatar / image import by URL (instead of upload)
- Webhook registration (Slack, Teams, custom callbacks)
- PDF / DOCX generators that embed remote images or HTML
- "Import from URL" (bookmarks, RSS, feeds, calendars)
- Proxy / translator / "fetch this page" features
- SSO / OAuth redirect_uri, "continue" / "next" params
- File converters, screenshot services, crawler/prerender
- XML upload → XXE (external entity = SSRF)
- GraphQL `query`/`URL` args, gRPC gateway
- Cloud object "custom domain" / "verify domain" callbacks

### 3. Detect — start local, escalate
Step A — verify control: point the param at a URL you control that returns a
unique string, confirm it's fetched & response shown (basic SSRF) OR your OOB
host got hit (blind SSRF).
Step B — localhost: `http://127.0.0.1:80`, `http://localhost/`,
`http://[::1]/`, `http://0.0.0.0/`.
Step C — cloud metadata:
  - AWS:      http://169.254.169.254/latest/meta-data/iam/security-credentials/
  - GCP:      http://169.254.169.254/computeMetadata/v1/?recursive=true
              (header: Metadata-Flavor: Google)
  - Azure:    http://169.254.169.254/metadata/instance?api-version=2021-02-01
  - DO:       http://169.254.169.254/metadata/v1.json
  - Oracle:   http://169.254.169.254/opc/v1/instance/
Step D — internal network sweep: `http://192.168.x.x`, `http://10.0.0.x`,
admin panels, K8s `https://kubernetes.default.svc`, Docker
`http://172.17.0.1:2375`.
Step E — protocol smuggling with Gopherus/SSRFmap (Redis, FastCGI, MySQL
UDF, SMTP) for RCE chains — only in authorized labs.

### 4. Bypass Filters (when 127.0.0.1 / 169.254.169.254 blocked)
Localhost alternatives: `http://127.1/`, `http://127.0.0.1.nip.io/`,
`http://0/`, `http://0x7f000001/`, `http://2130706433/` (decimal),
`http://0177.0.0.1/` (octal), `http://[::ffff:127.0.0.1]/`, `http://[::1]/`,
`http://localtest.me/`, `http://customer.packrepo.com@127.0.0.1/`,
registered domain resolving to 127.0.0.1 (sudo.cc, localtest.me, 127.0.0.1.sslip.io).
Whitelist bypass: `http://[REDACTED_EMAIL]/`, `http://expected.com/evil.com`,
`http://expected.com.evil.com/`, `http://[email protected]/`.
Scheme/encoding: `https://`, `file:///etc/passwd` (LFI+SSRF), `dict://`,
`gopher://`, `ftp://`, `http:/\\expected.com\@127.0.0.1/`, add trailing dot
`127.0.0.1.`, `%00`, CRLF in path, URL-encoded dots (`127.0.0.1` →
`127%2e0%2e0%2e1`), double-URL-encode.
DNS rebinding: resolve to public IP first, then 127.0.0.1 after TTL (tool:
singular / rbndr.us).
Time-of-check/time-of-use (TOCTOU): race the allow-list check.

### 5. Blind SSRF confirmation
- Use interact.sh CLI or Burp Collaborator; inject
  `http://<your-id>.interact.sh/` as the value.
- Watch for DNS + HTTP(S) hits from the target's egress IP.
- For port probing, point at `http://<id>.interact.sh:PORT` and observe which
  ports produce hits.
- Time-based: if `http://169.254.169.254:80` vs `:81` show different latency.

### 6. XXE-as-SSRF (classic)
```
<!DOCTYPE x [ <!ENTITY xxe SYSTEM "http://169.254.169.254/latest/meta-data/"> ]>
<root>&xxe;</root>
```
If the entity is echoed → basic SSRF via XML. If blind, use OOB entity:
`<!ENTITY % xxe SYSTEM "http://<id>.interact.sh"> %xxe;`.

## Common SSRF Parameters (fuzz list)
url, uri, link, src, href, file, doc, document, path, page, site, html, image,
img, media, video, audio, redirect, redirect_to, redirecturl, next, continue,
return, ret, returnurl, to, target, callback, webhook, hook, proxy, load,
fetch, fetch_url, import, feed, rss, api, endpoint, host, domain, ip, address,
server, data, u, uri, nav, goto, open, srcdoc, remote, source, base, ref,
preview, thumbnail, avatar, photo, picture, resource. (Full list in
references/ssrf_payloads.md.)

## Indicators of Vulnerability
- Response contains fetched content / differs when URL points to your host.
- OOB host receives DNS/HTTP hit when used as the value.
- Internal error (connection refused / timeout) when pointing at
  127.0.0.1 / metadata IP vs public IP.
- Different latency to open vs closed internal ports (blind port scan).

## Constraints & Limitations
- BLIND SSRF is invisible without an OOB channel — always set one up first.
- Some "SSRF" are fixed by egress allow-lists / VPC isolation (still report:
  defense-in-depth / info disclosure).
- file:// LFI-via-SSRF depends on the fetch library.
- Cloud metadata only works if IMDSv1 (no token) or the app can reach it.
- Always respect program rules — never pivot into out-of-scope internal hosts
  beyond proving the SSRF; do NOT exfiltrate other tenants' data.

## Remediation
- Allow-list by resolved IP + scheme; block link-local (169.254.0.0/16),
  loopback (127/8), RFC1918, and metadata IPs.
- Enforce IMDSv2 (token-required metadata) + hop-limit=1.
- Disable unused URL schemes (file://, gopher://, dict://).
- Egress firewall: server can only reach needed hosts/ports.
- Network policy / no-shared-VPC; separate metadata service.
- Validate & pin DNS after resolution (anti-rebinding).

## Operator notes (added — read-only first phase)
- Phase 0 (no OOB yet): grep discovered URLs for SSRF-prone parameter NAMES
  (script below). Produces a prioritized test list. Safe — no requests sent.
- Phase 1 (needs OOB host): inject collaborator URL into each candidate,
  confirm interaction. This is the real proof.
- For our Abema recon, the prime SSRF candidates are any "import/fetch/webhook/
  image-by-URL/redirect" params in the harvested URLs, plus OAuth redirect_uri
  and any /proxy or /fetch path. Extract with ssrf_recon.py.
