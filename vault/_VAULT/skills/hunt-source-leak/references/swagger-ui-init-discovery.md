# Swagger UI init.js Spec Discovery

## When the standard swagger.json endpoint is protected (418/403/404) but /api/docs or /swagger-ui returns a Swagger UI page.

Swagger UI loads its config from `swagger-ui-init.js` — this file contains the
full OpenAPI spec inlined as a JavaScript object. The spec JSON endpoint itself
may be blocked but the init.js is served as a static asset.

**Discovery path (2026-10, SignalStack):**
- `/api/docs/` → 301 redirect to `/api/docs/` → Swagger UI HTML
- `/api/docs/swagger.json` → 418 (stubbed Express route)
- `/api/docs/swagger-ui-init.js` → 200 (static asset, contains full spec)

**Extraction:**
```python
import requests, re, json5
r = requests.get("https://TARGET/api/docs/swagger-ui-init.js")
content = r.text
# Extract the spec object
m = re.search(r'"spec"\s*:\s*(\{.*?\})', content, re.DOTALL)
spec = json5.loads(m.group(1))
paths = list(spec.get('paths', {}).keys())
```

**Key insight**: When Swagger UI page loads but the JSON endpoint is protected,
check for `swagger-ui-init.js` — it's the static asset that contains the spec
and is often left accessible even when the dynamic endpoint is gated.