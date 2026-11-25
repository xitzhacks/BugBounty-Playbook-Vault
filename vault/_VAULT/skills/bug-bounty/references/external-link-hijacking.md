# Broken Link Hijacking — Bug Bounty Triage

> Reference content for the `bug-bounty` skill. Companion to `offensive-osint/references/broken-link-hijacking.md`.

## What IS vs IS NOT submittable

**Not submittable alone (Low/Info — goes to Always Rejected list):**
- External links that return 404 on a page (broken link) — unless you can prove domain can be registered AND a script/resource is loaded from it.
- `preconnect` / `dns-prefetch` to a 404 domain — limited to timing-based fingerprint, not exploitable JS injection.

**Submittable when chained (conditionally valid):**
- `<script src="https://expired-domain.com/payload.js">` where the domain is available to register → attacker registers domain, serves JS that executes in target's origin context → potential cookie theft / XSS.
- `<link rel="stylesheet" href="https://expired-domain.com/style.css">` where domain is available → CSS injection can exfiltrate data via `url()` requests.
- `<img src="https://expired-domain.com/t.png">` where domain is available → tracking pixel injection (limited impact, usually Low/Medium).

## Testing Checklist

1. Extract all external resource references (`src`, `href`) + preconnect/dns-prefetch hints from target pages.
2. For each external domain, check DNS resolution — flag NXDOMAIN.
3. For resolving domains, check HTTP status of the specific referenced path — flag 404/403.
4. For non-resolving domains, check registration availability (whois).
5. Classify by usage: `<script src>` = highest priority, `<link>` = medium, preconnect = low.
6. To validate: register the domain (or use a similar-looking domain) and serve a verification beacon. If the target page attempts to load a resource from it, confirm via OOB callback.

## Severity

| Usage | Severity (if domain available + resource loaded) |
|---|---|
| `<script src>` from expired domain | HIGH (potential XSS under trusted origin) |
| `<link rel="stylesheet">` from expired domain | MEDIUM (CSS-based data exfiltration) |
| `<img src>` from expired domain | LOW-MEDIUM (tracking pixel) |
| `<link rel="preconnect">` from expired domain | LOW (timing fingerprint only) |
| `<font>` / `<video>` / `<audio>` from expired domain | LOW (resource loading, limited impact) |

## Impact Validation

The key question: does the target's page actually CAUSE THE BROWSER to make a request to the external domain? If yes, and the domain is available, the attacker can:
- Serve a JS payload (for `<script src>`) that executes in the target origin
- Serve a CSS payload (for `<link rel="stylesheet">`) that exfiltrates data via `url()`
- Serve a tracking pixel (for `<img src>`) that fires when the page loads

If the reference is only in `<link rel="preconnect">` or `<link rel="dns-prefetch">`, the browser performs DNS resolution + TCP/TLS handshake but does NOT load any resource. Impact is limited to:
- DNS resolution leak (domain name visible to DNS resolver)
- TLS connection to attacker (IP visible in network logs)
- TCP connect timing (fingerprinting)

## Real-World Example

From a TrendSpider assessment:
- `uptimiarum.eu` referenced as `<link rel="preconnect">` on 3 subdomains
- Domain resolves to 54.38.92.128 but returns nginx 404
- Root domain has SSL cert mismatch
- Domain appears expired/discontinued (uptime monitoring service)
- **Verdict**: LOW (preconnect only, no resource loading)

Compare with: if the same reference was `<script src="https://uptimiarum.eu/monitor.js">`, that would be HIGH (script injection under trusted origin).

## Tools

```bash
# Extract external domains from a page
curl -sk "https://target.example/" | grep -oP 'https?://[^/"]+' | grep -v target.example | sort -u

# Check DNS
dig +short A external-domain.com  # empty = unresolvable

# Check whois availability
whois external-domain.com | grep -iE "no match|not found|AVAILABLE"

# Verify specific path status
curl -sk -o /dev/null -w '%{http_code}' https://external-domain.com/path/required.js
```
