---
name: hunt-jwt
description: Hunt JWT (JSON Web Token) authentication vulnerabilities. Covers jku/JWK Set URL injection, kid injection/path traversal, RS256 to HS256 algorithm confusion, alg none, weak HMAC secrets, and JWT-library CVEs. Use when a target issues an Authorization Bearer token or stores JWTs in cookies or localStorage and you need to forge, tamper with, or bypass auth. CTF custom-JWT challenges (key rotation, JWKS, jku, kid) almost always collapse to one of these.
---

# Hunt JWT Vulnerabilities

## When to use
- Target sends an Authorization Bearer token or stashes JWTs in cookies/localStorage.
- A token looks like xxxxx.yyyyy.zzzzz (base64url.base64url.sig).
- Challenge/task text mentions custom JWT auth, key rotation, JWKS, jku, kid, or "bring your own key".
- You have a web app that uses a "legacy client" / compat shim and a `kid` you don't have the key for.

## Step -1 — Find the kid / key hint BEFORE forging (source-map leak)
If you don't have a token to read, the `kid` and even the validating endpoint are often
sitting in plain sight in the frontend:
1. Load the app's main JS (e.g. `/static/js/app.js`). Look for `Authorization: Bearer`,
   `X-...-Channel`, and the API base (e.g. `/api/v2/internal/...`).
2. Fetch the **source map** for that JS: same path + `.map`
   (e.g. `/static/js/legacy-broker.9f14.js.map`). It is a JSON with a `sourcesContent`
   array — the original TypeScript/JS source, which routinely contains comments like
   *"tokens minted before the 2026 rotation used kid 'brokerlink-2019' and are still
   honored by the verifier"* plus the exact internal endpoint + required headers.
   That comment IS the exploit hint: forge `alg:none` + `kid: brokerlink-2019` and POST to
   the leaked endpoint. This is the single most common way a "legacy client" JWT challenge
   hands you the key id without ever issuing a token.

## Step 0 — Decode and fingerprint (no verification needed to READ)
```python
import base64, json
def d(s):
    s += "=" * (-len(s) % 4)
    return json.loads(base64.urlsafe_b64decode(s))
tok = "<JWT>"
h, p = d(tok.split('.')[0]), d(tok.split('.')[1])
print("HEADER", h)
print("PAYLOAD", p)
```
Record: alg, typ, and especially the presence of jku (JWK Set URL), jwk (inline key), kid (key id), x5u/x5c. These header fields are where trust goes wrong.

## Step 0.5 — Non-standard / "custom JWT" fingerprinting (CTF token != RFC JWT)
A token `xxxxx.yyyyy.zzzzz` is NOT automatically an RFC JWT. Inspect BEFORE
assuming alg/HS256:
- Decode the HEADER with `json.loads` (not blind b64-urlsafe). If it is NOT
  `{"alg":...,"typ":"JWT"}` but a bare claim like `{"user_id":1}`, the server
  likely uses a custom scheme where the claim is in the HEADER, not the payload.
- Decode the PAYLOAD. If it is 5-20 raw bytes (e.g. `6a 93 fa 2c`), it is an
  OPAQUE blob (salt/nonce/uid-hash), NOT a JSON claim. The real user identifier
  is probably the header claim.
- Measure the SIGNATURE length. 20 bytes = HMAC-SHA1, 32 = HMAC-SHA256,
  48 = HMAC-SHA384, 64 = HMAC-SHA512. A 20-byte sig means HS1 → crack with
  **hashcat -m 160** (HMAC-SHA1, key=password, salt=DATA), NOT -m 16500 (JWT HS256).

### Cracking the HMAC when you don't have the key (hashcat -m 160)
Use mode 160. The "hash" is the sig hex; the "salt" is the `header.payload`
MESSAGE (hex or string).
```
MSG="eyJ1c2VyX2lkIjoxfQ.apP6LA"
MSGHX=$(printf '%s' "$MSG" | xxd -p | tr -d '\n')
echo "099978808173eca0b7f0cc5324bbd2f4473058c7:$MSGHX" > job.txt
hashcat -m 160 -a 0 -w 3 job.txt /usr/share/wordlists/rockyou.txt.gz
```
If rockyou AND a JWT-secrets list (https://raw.githubusercontent.com/wallarm/jwt-secrets/master/jwt.secrets.list,
~104k entries) BOTH exhaust with 0 recovered, the key is uncrackable from
wordlists → STOP brute-forcing. Move to an algorithm/verification attack.
(Pure-Python cracking over rockyou's 14M lines is too slow; always use hashcat.)

### "Modify for user N" when the HMAC key is uncrackable — decision tree
The goal is a token VALID for user 2/3/4/5. With no key, realistic paths (order):
1. **`alg:none`** — header `{"user_id":N,"alg":"none"}`, keep original opaque
   payload, EMPTY signature (`hdr.payload.`). Many parsers skip verification
   when alg=none.
2. **Signature-ignored / broken verification** — swap only the header's user_id,
   keep the ORIGINAL signature (`hdr.payload.<orig_sig>`). Works if the endpoint
   doesn't verify at all.
3. **Header claim is the identity** — in a custom scheme the user_id lives in the
   HEADER; changing only the header is enough, the binary payload is a fixed nonce
   the server expects unchanged.
Build all three variants per target user and TEST against the real endpoint to see
which the server accepts (200 with that user's data). You cannot know which is
correct without testing — obtain the endpoint + OK to send before claiming success.
4. If a PUBLIC key is leaked (source map / JWKS), use RS256→HS256 confusion.

NOTE: a token whose header is `{"user_id":1}` with NO `alg` field, a binary
payload, and a 20-byte sig is a deliberately "weird" CTF token — the intended
lesson is almost always alg:none or signature-ignored, NOT key recovery.

## Step 0.6 — Is verification even running? (wrong-secret probe)

Before spamming 20+ role-claim / kid / secret variants, confirm whether the verifier
checks the signature AT ALL. One diagnostic probe saves you from burning the whole
variant space on a wall that permutation can't open.

1. Forge a token with a DEFINITELY-wrong HMAC secret (e.g. `WRONG123`) — correct
   `alg`, correct `kid`, any payload.
2. Send it to the protected endpoint. Compare the error to a correctly-signed token.

| Wrong-secret result | Meaning | Next move |
|---|---|---|
| **IDENTICAL** error to the valid token (e.g. both → `403 "reviewer role required"`, NOT `401 "invalid token"`) | Signature is NOT verified. The verifier decodes the payload and checks a claim/identity. | The role is either (a) a payload claim you can set — but if 15+ claim names all failed, it's (b) resolved server-side from a verified identity (backend user row or the real legacy key). STOP mutating claims. Pivot to recovering the legacy key (source-map hint, JWKS endpoint, RS256→HS256 confusion if RSA) or finding a real login. |
| **DIFFERENT** error (wrong-secret → `401 "invalid token"` / `400`; valid → `403 role required`) | Verification IS running. | You must sign with the real key. Recover it: crack weak HMAC (hashcat -m 16500), find it in a source map / `.env` / JWKS, or use jku / RS256→HS256 confusion. |

This probe turned a 50-variant dead end into a 1-call diagnosis in the Blackglass/CTF7
BrokerLink (`kid:brokerlink-2019`) hunt: wrong-secret and valid-secret tokens both
returned `403 "reviewer role required"`, proving the role gate was server-side and
unforgeable — which redirected effort to finding the real legacy key instead of
spamming claims. (See also the `bb-methodology` anti-pattern on variant-spray without
a mechanism check — the user cue "do one thing" / "just see what it says" means converge
on ONE hypothesis and report the raw response, don't fire variant 51.)

## Attack classes (try in this order)
1. jku / JWK Set URL injection — the BYOK case. If the header carries jku and the server FETCHES that URL to obtain the verifying key with no host allowlist, you control the key. Forge an RS256 token, host your own JWKS where the server can reach it, point jku at it, sign with your private key, match kid. Full recipe in references/jku_injection_walkthrough.md; reusable forger in scripts/forge_jwt_jku.py.
2. kid injection — kid is used to locate a key (file path, DB row, env var). Test path traversal (../../../../dev/null), SQLi in the lookup, or a kid that resolves to a known/static key. Often pairs with a weak/empty HMAC secret.
3. Algorithm confusion (RS256 to HS256) — if the verifier keys off the token's alg rather than a fixed server config, resend with alg:HS256 and sign using the public key (PEM) as the HMAC secret.
4. alg none — some libs accept {"alg":"none","typ":"JWT"} with an empty signature. Try it.
5. Weak HMAC secret — HS256/384/512 with a guessable secret. Crack with jwt-cracker, hashcat -m 16500/16501/16502, or a wordlist plus jwt_tool.
6. Library CVEs — CVE-2015-9235 (alg none), CVE-2016-10555 (node-jsonwebtoken key confusion), CVE-2022-23529, CVE-2022-21449 (ECDSA signature exclusion), CVE-2020-28042. Check the lib version.

## Pitfalls (learned the hard way)
- Hosting the JWKS is the actual hard part. The server must be able to FETCH your jku URL. In 2026 many free hosts are dead/blocked or wrap content in HTML (so the server receives HTML, not JSON, and verification fails with 401). Mid-2026 status:
  - DEAD / BLOCKED / HTML-wrapped: transfer.sh, 0x0.st, catbox.moe, litterbox, tmpfiles.org (HTML wrapper), pastebin guest API (404), file.io, bashupload, webhook.site (unreliable/intercepted).
  - WORKS (raw JSON, serves body on GET): paste.rs/<id>.
  - BEST for CTF: run your own HTTP server on a publicly reachable IP and point jku at http://<your-public-ip>:8000/jwks.json. Use a logging server so you can see whether the target ever fetched it — a 401 with no inbound request means the server is not fetching jku (host unreachable/blocked) or you hit a route that does not validate.
- pyjwt + cryptography need a venv on modern Kali/Debian (PEP 668): python3 -m venv venv and . venv/bin/activate and pip install pyjwt cryptography requests.
- 401 does NOT necessarily mean a bad exploit. If you send the forged token to a route that does not enforce it (e.g. /api/login, which only checks creds), you get 401 from bad creds, not token rejection. Find the route that actually consumes the token/role. Brute /api/<word> with the forged token using a real API wordlist — seclists/Discovery/Web-Content/api/api-endpoints.txt is ~181k lines (too slow); use common-api-endpoints-mazen160.txt (174 lines) for speed, then expand.
- A 401 against a validating endpoint with a correctly forged admin token almost always means the server did NOT fetch your jku. Verify via your JWKS host's access log before changing the exploit.
- **alg none accepted ≠ you're in.** If alg:none (or HS256 with an empty/guessed secret) gets you PAST auth but the endpoint returns a 403 reviewer-role error (or similar), the verifier trusted your signature but the ROLE is resolved **server-side from the verified identity**, not from a payload claim you can set. Tried-and-failed claims: role, roles (list/str), scope, groups, permissions, reviewer:true, is_reviewer. The real path is either (a) the sub/user must match a server-side reviewer list (try values like reviewer, intake, doc.review, legacy), or (b) you need a token signed by the actual legacy key (recover the public key / find it in the source map or a JWKS endpoint and use RS256→HS256 confusion if the key is RSA). **Do NOT burn time spamming payload claims.** Run the Step 0.6 wrong-secret probe FIRST: if a token signed with WRONG123 returns the SAME 403 reviewer error (not 401 invalid token) as your valid token, signature verification is NOT running and the role is unforgeable — stop mutating claims and pivot to key recovery / real login. In the Blackglass/CTF7 BrokerLink hunt, ~50 claim/kid/secret variants all returned the identical 403; the wrong-secret probe was the single call that proved the gate was server-side and ended the permutation loop.
- **Read the source map, not just the minified JS.** The `.js.map` `sourcesContent` is where `kid` values, key-rotation comments, and internal endpoint URLs live. This is often the ONLY place the correct `kid` and endpoint are documented.

## Verification
- Re-decode your own forged token to confirm alg/jku/kid are set and the signature verifies locally against your public key.
- Send to a protected endpoint; success = 200 with role-dependent data or the flag.

## Overlap note
hunt-auth-bypass covers JWT forgery as one auth-bypass flavor; this skill is the JWT-specific deep dive (jku/kid/alg-confusion/CVEs plus hosting gotchas). Prefer this skill when the target clearly uses JWTs.
