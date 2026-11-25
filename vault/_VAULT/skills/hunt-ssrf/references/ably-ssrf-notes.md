# Ably.com SSRF Notes

## Targets and Results

| Target | Endpoint | Payload Tested | Result | Verdict |
|--------|----------|----------------|--------|---------|
| ably.com | /api/notice?url= | https://collab.interact.sh | 403 Forbidden (Cloudflare) | Rate-limited, inconclusive |
| ably.com | /api/token?url= | https://collab.interact.sh | 403 Forbidden (Cloudflare) | Rate-limited, inconclusive |
| ghost.ably.com | /ghost/api/admin/session | POST with url= param | 403 "Access Denied" | Proper auth, not SSRF |
| metabase.ably.com | /api/database | ?url= | 401 Unauthorized | Auth-gated |
| rest.ably.io | /stats | ?url= | 401 (requires auth) | Auth-gated |
| dashboards.ably.com | /_next/image?url= | http://127.0.0.1:8080/ | 400 Bad Request | URL allowlist enforced |
| control.ably.net | /v1/apps | ?url= | 403 Forbidden | Cloudflare |

## False Positive: CVE-2022-41697 on ghost.ably.com

- Nuclei flagged `/ghost/api/admin/session` with CVE-2022-41697 (medium severity)
- Manual verification:
  - GET `/ghost/api/admin/session` → 404 "Resource not found"
  - POST `/ghost/api/admin/session` → 403 "Access Denied" with `{"errors":[...]}` JSON
- This is proper server-side auth rejection, NOT the vulnerable behavior described in CVE-2022-41697
- CVE-2022-41697 describes SSRF via session token endpoint in Ghost < 5.0 that allows fetching arbitrary URLs to steal session tokens
- Ghost v6.59 should be beyond the affected version range
- **Conclusion:** False positive — retract SSRF claim

## Cloud Metadata Tests

All targets on Heroku/Vercel/Cloudflare — metadata service not reachable via SSRF (no vulnerable URL-fetching sinks confirmed)

## S3 Bucket Checks

Checked 11 bucket names (ably-dev, ably-production, ably-assets, ably-cdn, ably-public, etc.) — all returned 404 (no public buckets)