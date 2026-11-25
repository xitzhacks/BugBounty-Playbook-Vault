# Full-Read JS Bundle Extraction Recipe (re-runnable)

Used by `spa-bundle-recon`. No allow-list filtering — extract everything, dedup sorts signal.

## Download (decompress!)
```bash
curl -s --compressed -o js/chunk.js "https://TARGET/assets/chunk.abc.min.js"
file js/chunk.js   # "JavaScript/ASCII text" good; "gzip compressed data" = fix:
# for f in js/*.js; do mv "$f" "$f.gz"; gunzip "$f.gz"; done
```

## Extract all
```python
import re, glob, os, json
d = "js_dec"
alltext = "\n".join(open(f, encoding="utf-8", errors="ignore").read()
                    for f in glob.glob(f"{d}/*.js"))
urls = sorted(set(re.findall(r'https?://[^\s"\x27\\]+', alltext)))
wss  = sorted(set(re.findall(r'wss?://[^\s"\x27\\]+', alltext)))
rel  = sorted(set(re.findall(r'["\x27](/[a-zA-Z0-9_\-]+(?:/[a-zA-Z0-9_\-:.{}?=&]+)+)["\x27]', alltext)))
tmpl = sorted(set(re.findall(r'`([^`]*\/[a-zA-Z0-9_\-][^`]*)`', alltext)))
calls= sorted(set(re.findall(r'\b(?:get|post|put|delete|patch)\s*\(\s*["\x27](/[^"\x27]+)["\x27]', alltext)))
cfg  = re.findall(r'window\.__CONFIG__\s*=\s*(\{.*?\});', alltext, re.DOTALL)
for n in ("urls","rel","tmpl","calls"): print(n, len(vars()[n]))
# DO NOT restrict rel/calls to /api|/user|/v1 — that hides real endpoints.
```

## Archive diff (hidden endpoints)
```python
import re
from collections import Counter
c = Counter()
for line in open("wayback.txt", encoding="utf-8", errors="ignore"):
    for m in re.finditer(r'https?://([a-z0-9.\-]*TARGET\.com)(/[^?\s"\x27<>]*)', line, re.I):
        host, path = m.group(1).lower(), m.group(2)
        if re.search(r'\.(js|css|png|jpg|jpeg|gif|svg|woff|ttf|ico|mp4|webp)($|\?)', path, re.I):
            continue
        c[host + path] += 1
# api-ish keys (e.g. '/v1/','/api/','/users','/auth','/charge','/loot-boxes') present in
# archive but NOT in current bundles = hidden/legacy surface.
```

## Verify real API base
- grep bundle: `API_URL`, `PROXY_ENDPONT_PREFIX`, `baseURL`, `create({baseURL`
- probe both `https://TARGET/z/<p>` and `https://api.TARGET.com/v1/<p>`
- 405 on GET of a POST-only route (e.g. `/users/me/short-password/reset`) proves it exists
- 401 = auth-gated; 404 on wrong proxy path != non-existent
