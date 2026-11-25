# Extract API Endpoints from JavaScript Files

## Why This Works

Modern SPAs (React, Vue, Angular, Next.js) bundle API routes into JS files. These often reveal:
- Hidden endpoints not linked from the UI
- ID-bearing URL patterns (e.g., `/api/users/{id}/profile`)
- Parameter names and expected formats
- Authorization logic (or lack thereof)

**Real example (2026-09-18):** On `3.82.11.95` (Barracks Kids), the `/js/parent.js` and `/js/kid.js` files revealed ALL API endpoints:
- `/api/parent/children` - parent's children list
- `/api/parent/children/{id}/activity` - IDOR-prone activity endpoint
- `/api/parent/children/{id}/play` - IDOR-prone play endpoint
- `/api/kid/chat/{id}/messages` - IDOR-prone chat messages
- `/api/profile/avatar` - SSRF-prone avatar upload
- `/api/kid/buddies/search?q=` - SQLi-prone search
- `/api/certificates/download?file=` - Path traversal download

Without JS analysis, these endpoints would have been missed.

## Extraction Commands

### Basic endpoint extraction
```bash
# Extract all API paths from a JS file
curl -s https://target.com/js/app.js | grep -oE '"/api/[^"]+"' | sort -u

# Extract fetch/axios calls with template literals
curl -s https://target.com/js/app.js | grep -oE 'fetch\(`[^`]+`' | sort -u

# Extract all URL-like patterns
curl -s https://target.com/js/app.js | grep -oE '(https?://[^"'\'' ]+|/api/[^"'\'' ]+|/v[0-9]+/[^"'\'' ]+)'
```

### Extract ID-bearing patterns
```bash
# Find paths with numeric IDs
curl -s https://target.com/js/*.js | grep -oE '/[a-z]+/[0-9]+' | sort -u

# Find paths with {id} placeholders
curl -s https://target.com/js/*.js | grep -oE '/[a-z]+/\{id\}' | sort -u

# Find template literal patterns with IDs
curl -s https://target.com/js/*.js | grep -oE '\$\{[a-zA-Z_]+\}' | sort -u
```

### For minified JS
```bash
# Beautify and extract
curl -s https://target.com/js/app.js | python3 -c "
import sys, re
content = sys.stdin.read()
# Find API paths
paths = re.findall(r'[\"'\'']/[a-zA-Z0-9/_-]+[\"'\'']', content)
for p in sorted(set(paths)):
    print(p)
"

# Find all fetch/ajax calls
curl -s https://target.com/js/app.js | grep -oE '(fetch|axios|api)\s*\(\s*["\x27|`]' | sort -u
```

### Multi-file extraction
```bash
# Download all JS files and extract endpoints
for js in $(curl -s https://target.com/ | grep -oE 'src="[^"]+\.js"' | sed 's/src="//;s/"//'); do
  echo "=== $js ==="
  curl -s "https://target.com$js" | grep -oE '"/api/[^"]+"' | sort -u
done

# Or with wget
wget -r -l 1 -A js https://target.com/ 2>/dev/null
grep -roh '"/api/[^"]+"' . | sort -u
```

## What to Look For

When analyzing extracted endpoints, flag:

1. **Numeric ID patterns**: `/api/{resource}/{number}` - classic IDOR target
2. **UUID patterns**: `/api/{resource}/{uuid}` - predictable UUIDs are IDOR-able
3. **Query parameters**: `?id=`, `?user_id=`, `?file=` - often missed in IDOR testing
4. **Admin endpoints**: `/api/admin/...` - check for missing authorization
5. **File operations**: `?file=`, `?path=`, `?template=` - path traversal/LFI candidates
6. **Search/filter**: `?q=`, `?search=`, `?filter=` - SQLi/XSS candidates
7. **Avatar/image fetch**: `?url=`, `?imageUrl=` - SSRF candidates

## Post-Extraction Workflow

1. **Catalog all endpoints** - group by resource type
2. **Identify ID-bearing paths** - these are your IDOR test targets
3. **Test without authentication** - some endpoints may be unauthenticated
4. **Test with two accounts** - create User A and User B, swap sessions
5. **Test all HTTP methods** - GET, POST, PUT, PATCH, DELETE on each endpoint
6. **Document authorization gaps** - which endpoints check ownership vs just authentication
