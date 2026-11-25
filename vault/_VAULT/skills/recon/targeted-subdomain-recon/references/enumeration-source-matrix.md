# Enumeration source matrix — what each source actually returned

Worked example: a 2026 SaaS engagement (`trendspider.com` + related registrable
domains). Numbers are real; use them to calibrate expectations, not as a
substitute for running the sources.

## Per-source yield

| Source | Command | Unique names contributed |
|---|---|---|
| subfinder `-all` | `subfinder -d root -silent -all` | 26 |
| assetfinder | `assetfinder --subs-only root` | 16 |
| certspotter | `api.certspotter.com/v1/issuances?...&expand=dns_names` | 12 (free tier truncates) |
| hackertarget | `api.hackertarget.com/hostsearch/?q=root` | 16 |
| crt.sh | `crt.sh/?q=%25.root&output=json` | **0 — HTTP 502 on every attempt across the whole session** |
| dnsx brute, 100k bitquark | `dnsx -d root -w bitquark-subdomains-top100000.txt -t 150` | 8 new (incl. `ftp`, `mail`, `webmail`, `autoconfig`) |
| subfinder on sibling domains | `subfinder -d sibling.com` | 10 + 7 — **found the staging cluster** |
| wayback CDX | `web.archive.org/cdx/search/cdx?url=host*` | 0 snapshots for the app host |

Lesson: the highest-value names came from **sibling-domain enumeration**, not
from deepening the primary root. Always ask "what other registrable domains does
this company own?" — CSP headers, Sentry DSNs, cookie `Domain=` attributes and
JS config objects name them.

## Funnel to report

```
48 candidate names
   ↓ dnsx -a -resp
87 DNS records (multiple A records per name)
   ↓ httpx -status-code -title -tech-detect
30 live hosts
   ↓ classification
 7 SPA shells (no server-side params)
 5 302 → login (auth-gated app)
 5 403 (mail infra / WAF)
 4 RFC1918-only (k8s ingress names)
 9 full HTTP apps (marketing, WP, helpdesk, trade widgets)
```

Publish the funnel with a status per host. "I enumerated" is not a claim anyone
can audit; "48 → 87 → 30, here is each host's status" is.

## RFC1918 k8s names — the test and the negative result

Names like `compliance.ts01-prod-main.k8s.example.com` resolved to
`10.200.26.7`, `10.200.88.241`, `10.200.147.246`. Before calling them
unreachable, their `Host` header was sent to all four public ALB IPs:

| ALB IP | `Host: compliance...` | `Host: nginx-front...` | Verdict |
|---|---|---|---|
| 15.197.163.95 | 301 → apex | 301 → apex | default vhost |
| 3.33.128.125 | 301 → apex | 301 → apex | default vhost |
| 35.208.227.99 | 200, generic 1385-byte page | 200, same page | default vhost |
| 52.33.193.40 | connection failure | connection failure | not routable |

No internal service reachable through the public load balancers. Two signals
prove "default vhost, not the real service": **every internal name returns a
byte-identical body**, and the status matches what a bare IP request returns.

## Sibling-domain tell-tales that paid off

- Production `Content-Security-Policy: frame-ancestors 'self' https://*.sibling.com`
  → sibling domain is theirs, staging lives there.
- Sentry init config listing `staging-v1..v5.sibling.com` as trace origins.
- `Set-Cookie: ...; Domain=.primary.com` on an app host → cookie scope covers
  every sibling subdomain.
- A staging register page shipped `pk_test_...` (Stripe publishable test key) —
  the only environment where a free paid-plan signup would have been possible.

Scope note: a different registrable domain is still the operator's call, even
when the evidence says it is theirs. Test it, document it, and flag the scope
question explicitly rather than silently including or excluding it.
