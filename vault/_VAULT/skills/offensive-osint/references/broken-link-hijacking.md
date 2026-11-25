# Broken Link Hijacking
> Reference for the `offensive-osint` skill.

When a target page references an external domain as a resource source (`<script src>`, `<img src>`, `<link href>`) or a `preconnect`/`dns-prefetch` hint, and that domain either does NOT resolve or returns a broken response (404/403 with no useful content), the domain may be available to register — letting an attacker serve malicious content under a domain the target already trusts in its HTML/CSP.

## Methodology

### Step 1: Extract all external references

From the rendered HTML of every alive target page, extract:
- `src="https://..."` (scripts, images, iframes)
- `href="https://..."` (stylesheets, links)
- `<link rel="preconnect" href="https://...">` and `<link rel="dns-prefetch" href="https://...">`

Skip resource URLs whose domain is the same as the target. Focus on third-party domains.

### Step 2: Check DNS resolution

For each unique external domain, check DNS resolution. Domains that fail to resolve (`NXDOMAIN` or `SERVFAIL`) are candidates for registration.

```bash
for d in $(cat external_domains.txt); do
  if ! dig +short A "$d" | grep -qE '^[0-9]+\.'; then
    echo "UNRESOLVABLE: $d"
  fi
done
```

### Step 3: Check HTTP status of the specific referenced path

Even if the domain resolves, check whether the specific path the target references returns a 404 or error. A domain can resolve but serve no content at the referenced path.

```bash
curl -sk -m 10 -I "https://external-domain.com/path/file.js" -w '%{http_code}\n'
```

### Step 4: Check domain registration availability

For domains that fail DNS resolution, check WHOIS to see if the domain is available to register:

```bash
whois external-domain.com | grep -iE "no match|not found|AVAILABLE|No entries"
```

For `.eu` domains, use EURid's WHOIS. For other TLDs, check the registrar's availability API.

## Real-World Findings

From a TrendSpider assessment:
- **uptimiarum.eu** — found as `<link rel="preconnect" href="https://www.uptimiarum.eu">` on trendspider.com, share.trendspider.com, and university.trendspider.com.
  - DNS resolves to an IP but returns a 404 (nginx default page).
  - The root domain has an SSL certificate mismatch (cert exists for a different domain).
  - This suggests the domain was previously registered for uptime monitoring but the service has been discontinued.
  - **Impact: LOW** — only used as `preconnect` (tells the browser to DNS-prefetch + TCP connect), no actual JavaScript or resources are loaded from this domain. The browser only establishes a connection.
  - If any actual `<script src>` or `<img src>` referenced a broken domain, the impact would be MEDIUM-HIGH (script injection under the target's trusted origin).

## Detection Checklist

- [ ] Extract all external domains from `src`, `href`, `preconnect`, `dns-prefetch` attributes
- [ ] Check DNS resolution for each domain (flag NXDOMAIN/SERVFAIL)
- [ ] Check HTTP status of each referenced path (flag 404/403/5xx)
- [ ] For domains with DNS that 404: check WHOIS for registration availability
- [ ] For domains that resolve but serve errors: check if the domain has an active website or is just a parked/expired domain
- [ ] Classify impact by usage context:
  - `<script src>` → MEDIUM-HIGH (potential XSS under trusted origin)
  - `<img src>` → LOW-MEDIUM (tracking/pixel injection)
  - `<link rel="preconnect">` → LOW (timing fingerprint only)
  - `<link rel="stylesheet">` → MEDIUM (CSS injection, potential data exfil)

## Tools

```bash
# Extract external domains from a page
curl -sk -m 10 "https://target.example/" | grep -oP 'https?://[^/"]+' | sort -u

# Check DNS resolution
for d in $(cat domains.txt); do dig +short A "$d" || echo "UNRESOLVABLE: $d"; done

# Check HTTP status of referenced paths
curl -sk -m 10 -o /dev/null -w '%{http_code} %{url_effective}\n' "https://domain/path"

# WHOIS check (generic)
whois domain.com | head -5
```
