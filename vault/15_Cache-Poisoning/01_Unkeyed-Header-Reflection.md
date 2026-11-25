---
title: "Unkeyed Header Reflection — X-Forwarded-Host / Scheme / User-Agent poisoning"
type: playbook
category: cache-unkeyed-header
cwe: "CWE-444, CWE-524"
source_count: 7
full_bodies_available: 7
corpus: "h1-brain disclosed_reports.db (3,673 rows) · sha256 8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4"
list_accessed: "2026-11-07"
note: "Anchors: CACHE-977851 (Shopify, $1,000), CACHE-303730 (data.gov, $750), CACHE-1795197 (Glassdoor JS hijack), CACHE-2917062 (Trendyol store XSS)."
---

# Unkeyed Header Reflection — the header the cache forgot to key on

## 1. Overview

Seven rows, **$2,206/3 paid**. Every case is the same shape: the origin writes a request
header into the cached response body (or into a redirect), and the CDN's cache key does not
include that header. One attacker request poisons the entry; everyone else gets the payload.

**Case-stock (7 rows / $2,206):**

| Case | Target | Mechanism | Bounty |
|---|---|---|---|
| [CACHE-977851](https://hackerone.com/reports/977851) | shopify | `X-Forwarded-Host` in blog links, cached, persists after header removal | $1,000 |
| [CACHE-303730](https://hackerone.com/reports/303730) | gsa_bbp (catalog.data.gov) | `X-Forwarded-Host` → `data-site-root` attribute → DOMXSS, CloudFront cached | $750 |
| [CACHE-394016](https://hackerone.com/reports/394016) | discourse | `X-Forwarded-Host` → `woff2_url` in `@font-face` (5 hosts) | $256 |
| [CACHE-1392935](https://hackerone.com/reports/1392935) | omise | `X-Forwarded-Host` reflected → RXSS | $200 |
| [CACHE-1795197](https://hackerone.com/reports/1795197) | glassdoor | `X-Forwarded-Scheme` + `X-Forwarded-Host` → cached 301 on `/test.js` | - |
| [CACHE-2917062](https://hackerone.com/reports/2917062) | trendyol | `User-Agent` reflected into `sw.js` response, 3 requests to pin | - |
| [CACHE-1374512](https://hackerone.com/reports/1374512) | ibb (Rails) | `X-Forwarded-Host` case-variance bypass of Host Authorization | - |

## 2. The canonical proof: poison, then remove the header

CACHE-977851 is the two-screenshot report that costs nothing to triage — the poison survives
without the attacking header:

> run in loop requests with```  X-Forwarded-Host: your_hackerz_site.com ``` - after some time You will notice in response ``` your_hackerz_site.com ```

> now remove ``` X-Forwarded-Host  ``` - there still be our url:

And the safe-hunting note every cache report should carry, from CACHE-303730:

> Please be careful when exploring this issue, as it's potentially quite easy to accidentally poison CloudFront's cache and antagonise your visitors.

## 3. From link poisoning to stored XSS

CACHE-303730 turns a host-header reflection into DOMXSS because the attribute value is
consumed by JavaScript:

> The root problem is that the server trusts the X-Forwarded-Host HTTP header, and uses this to populate the 'data-site-root' and 'data-locale-root' attributes on the <body tag. Some JavaScript then fetches a JSON file from the URL specified in these attributes, and writes the response to the page without escaping it, leading to a DOMXSS vulnerability.

CACHE-394016 is the same primitive inside a stylesheet — the Discourse font URL:

> The Web application is vulnerable to XSS through the X-Forwarded-Host header.

CACHE-2917062 is the non-header-varied version: the reflection is in `User-Agent`, so the
attacker must send the poisoning request repeatedly to land on a cacheable variant:

> 4.Then change **User-Agent:** header value ``</script><img src=1 onerror="Function('ale'+'rt(document.cookie)')()">`` and add **sw.js** paramerter.
> 5.Send 3 request.

## 4. Redirect poisoning — the JS-file hijack

CACHE-1795197 shows the highest-leverage target: a cacheable `.js` path redirected by
`X-Forwarded-Scheme: http`:

> 2. You should notice the `Cf-Cache-Status: MISS` header when first sending the request. After sending another request, you should see `Cf-Cache-Status: HIT`, confirming the redirect has been cached.

> An attacker can use the same attack against valid JS files leading to full control over the loaded JS. If any Glassdoor websites import javascript files from `https://design.glassdoor.com/*` they are susceptible to a Stored XSS attack via Cache Poisoning.

## 5. Case-variance bypasses

CACHE-1374512 (Rails, CVE-2021-22942) is the framework-side variant: the Host Authorization
middleware compared the host ignoring case, so `Evil.com` passed a check written for
`evil.com`:

> when sending a request like the following where the URL has a mixed case characters

## 6. What pays, what doesn't

- **Paid**: reflected host → *cached* body that other users fetch ($1,000 / $750 / $256 / $200).
  The bounty tracks reach (how many visitors get the payload), not the injection itself.
- **Unpaid in this corpus**: framework CVEs (CACHE-1374512 — IBB coordination row, no figure),
  and cases where the demonstration stopped at "the header is reflected" without a cached
  entry or a victim path.
- **Kill-gate**: a host-header reflection with `Cache-Control: no-store`, `Vary: X-Forwarded-Host`,
  or a cache that refuses to store the response is not this class.

## 7. Cross-references

- `../24_Host-Header-Injection/` — the non-cached sibling class (password-reset poisoning, redirect).
- `../16_Information-Disclosure/` — cache-deception cases that leak session/PII rather than execute.
- `../29_Clickjacking/`, `../XSS/` — the payload reach these rows weaponize.
