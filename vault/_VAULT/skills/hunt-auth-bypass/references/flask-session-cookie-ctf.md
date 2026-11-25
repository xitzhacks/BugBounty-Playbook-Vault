# Flask Signed-Session-Cookie Recon for "Thin-Surface" Auth/CTF Apps

## The pattern
Many CTF "admin API" / broken-access-control challenges are small Flask apps whose
only identity carrier is a signed `session` cookie (Flask `itsdangerous`, format
`payload.timestamp.signature`, each part base64url). The single highest-yield move is
to **decode the cookie BEFORE doing anything else** — it tells you the auth model and
whether you can forge identity.

LedgerLock (CTF7, `BI{...}` flag, login `[REDACTED_EMAIL]` / `Ledger@2026`)
was exactly this: the only JSON API was `GET /api/me` -> `{"id":1,"role":"employee",...}`,
the cookie decoded to `{"user_id":1}`, and every other `/api/*` returned
`404 {"error":"not_found"}`. The flag was an "administrative API" the brief referenced
but that did not surface through naive fuzzing.

## Decode + forge-test (run this first)
```python
import base64, requests

def decode(c):
    out = []
    for p in c.split('.'):
        p += '=' * (-len(p) % 4)
        try: out.append(base64.urlsafe_b64decode(p).decode('utf-8', 'replace'))
        except Exception: out.append(p)
    return out

S = requests.Session()
S.post("http://HOST/login", data={"email":E,"password":P}, allow_redirects=True)
raw = S.cookies.get("session")
print(decode(raw))          # -> ['{"user_id":1}', '<ts>', '<sig>']

# Forge test: tamper the payload, keep a bogus sig, replay an authed endpoint
body = base64.urlsafe_b64encode(b'{"user_id":6,"role":"admin"}').rstrip(b'=').decode()
r = requests.get("http://HOST/api/me", headers={"Cookie": f"session={body}.x.y"}, timeout=10)
print(r.status_code, r.text)   # 401 {"error":"authentication_required"} => sig ENFORCED
```

## Reading the result
- **Forged cookie -> 401 / session resets** => signature is verified. You CANNOT escalate
  by editing `user_id`/`role`/`is_admin` in the cookie. Pivot to a *logic* flaw:
  BOLA/IDOR on the API, a function-level access gap, or a sibling service.
- **Forged cookie accepted (no 401)** => direct auth bypass. Set `role:admin` /
  `user_id` of the admin account and walk the admin API surface.

## Thin-surface decision tree (when only /api/me exists)
1. `405` on `POST/PUT/PATCH/DELETE /api/me` => the route EXISTS but only GET is allowed.
   Not a vuln by itself; method-tampering won't help.
2. Distinguish a real JSON 404 (`{"error":"not_found"}`, ~22 bytes) from a Flask default
   **500 page** (1114 bytes, `<title>500 Internal Server Error</title>`). A 500 means a
   catch-all route crashed on that path — sometimes a real (hidden) route is partially
   matched. Re-hit it when the host is stable; a genuine 500 can leak a traceback /
   SECRET_KEY if debug mode is on.
3. If mass-assignment on `/api/me` (`{"role":"admin"}` etc.), header injection
   (`X-User-Id`, `X-Admin`, `X-Role`, `X-Forwarded-User`), and `/api/admin`,
   `/api/users`, `/api/employees` fuzzing all return 404/405, the brief's
   "administrative API" is likely either (a) a specific path the author expected you to
   reach via a hint, or (b) only reachable from a **sibling app on a neighbor port**
   (these CTF boxes bundle several apps on one host; the named port often flaps).
   Neighbor scan:
   `for p in 8000 8081 8082 8083 8084 8085 5000; do timeout 3 bash -c "cat < /dev/null > /dev/tcp/HOST/$p" && echo $p open; done`
4. **Don't loop.** Once the obvious surface is exhausted with no state change, ask the
   user/challenge author for the intended trigger instead of re-fuzzing the same
   wordlist. (This correction recurred on the same box's SENTINEL challenge too — the
   agent sprayed unlock-verbs instead of crafting the exfil side-channel payload.)

## What did NOT work on LedgerLock (negative results, to avoid repeating)
- IDOR via query params on `/api/me` (`?id=`, `?user_id=`, `?emp=EMP-0005`, ...) -> all
  returned the caller's own record (no cross-user read).
- Forged/unsigned cookies (any `user_id`, with or without `role:admin`) -> 401.
- `POST/PUT/PATCH/DELETE /api/me` with mass-assignment bodies -> 405.
- `/api/admin`, `/api/users`, `/api/employee/<id>`, `/api/export`, header injection ->
  404 `not_found` or 401.
- `/static/app.js` and other JS bundles -> 404 (UI is server-rendered, no client bundle).
- No Werkzeug debug console, no `/__debug__`, no config/.env exposure.
