# WordPress oEmbed SSRF Triage Notes

## Key Facts
- WordPress oEmbed endpoint: `/wp-json/oembed/1.0/embed?url=<URL>`
- Only fetches URLs from **whitelisted oEmbed providers** (YouTube, Vimeo, Twitter, etc.)
- Internal IPs (169.254.169.254, localhost, 127.0.0.1) return `404 oembed_invalid_url` — NOT fetched
- The URL is validated against provider patterns, not actually fetched

## SG Captcha Interaction
- When `wpSGCacheBypass=1` cookie is active, oEmbed accepts URL params without SG Captcha challenge
- Without the bypass cookie, all requests return 202 (SG Captcha challenge)
- The PoW bypass requires browser context (timing, IP validation, headers)

## False-Positive Patterns
```
# These are NOT SSRF — URL is validated but not fetched:
GET /wp-json/oembed/1.0/embed?url=http://169.254.169.254/  → 404 oembed_invalid_url
GET /wp-json/oembed/1.0/embed?url=http://localhost/         → 404 oembed_invalid_url
GET /wp-json/oembed/1.0/embed?url=http://127.0.0.1/           → 404 oembed_invalid_url
```

## Validation
Always check:
1. Does the server actually make an outbound request to the URL? (Use OOB callback)
2. Is the URL whitelisted before fetching?
3. Does the oEmbed provider list include the target URL pattern?

## Internal Hostname Disclosure
WordPress user endpoint (`/wp-json/wp/v2/users`) may expose internal hostnames in the `url` field (e.g., `http://markets.trendspider.local`). This is information disclosure, not SSRF — the internal hostname doesn't resolve externally.
