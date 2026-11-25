# JS Bundle Recon — Reading Client Bundles for Sensitive Info

Passive, read-only extraction of config / secrets / attack-surface from frontend
JavaScript bundles (React/Vite, Next.js, Webflow, Angular). Use during authorized
bug-bounty or red-team recon when the target ships a SPA or uses heavy client JS.

## Why "read", not "grep"

Minified bundles are ~2–5 MB of library noise (Ant Design, React internals, CSS-in-JS
template strings). A bare `grep -i secret` returns hundreds of false hits from style
keys (`secret` appears in `boxShadow`), function names, and font strings. The reliable
method is: **fetch the full bundle, then extract assignment / context patterns** with
regex over the parsed text. Treat grep as a triage hint only, never as the finding.

User preference (this operator): "analyze each js file line by line... Without grepping
DO it by reading." Honor it — fetch and context-extract, don't stop at keyword grep.

## Workflow

1. Fetch the host HTML. Extract every `<script src="...">` and inline `<script>` blob.
   - Vite/React SPA: main bundle is `/assets/index-<hash>.js` (also `/assets/*.js` chunks).
   - Next.js: `/_next/static/chunks/<hash>.js`, `/_next/static/chunks/pages/*.js`.
   - Webflow: `cdn.prod.website-files.com/<siteid>/.../*.js` custom-code snippets + `webflow.*.js`.
2. Fetch each bundle. Save locally (e.g. `/home/user/Bugbounty/<target>_main.js`).
3. Run line-by-line context extraction (Python `re.finditer` on the patterns below).
   Print the surrounding ~80 chars of context for each hit — that context is the proof.
4. Build the **subdomain / API map** from extracted `https://*.target.com` URLs and
   `baseUrl`/`endpoint` assignments. Probe discovered hosts passively (HEAD / status
   code only) to confirm reachability. Do NOT attack without authorization.
5. De-noise: drop CSS/style strings, React/antd internals, W3C/MathML/font URLs,
   `momentjs.com` / `reactjs.org` doc links.

## High-value patterns (copy-paste into a Python scan)

```python
import re
bundle = open("target_main.js").read()

pat_assignment = re.compile(
    r'["\'](?:api|apiBase|apiUrl|baseURL|baseUrl|endpoint|backend|server|graphql|'
    r'rest|clientId|client_id|secret|token|apiKey|api_key|privateKey|accessKey|'
    r'NEXT_PUBLIC|REACT_APP|VITE_|VUE_APP)[A-Za-z_]*["\']\s*[:=]\s*["\'][^"\']{3,200}["\']',
    re.I)

pat_uuid = re.compile(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', re.I)
pat_domain = re.compile(r'https?://([a-z0-9.-]+\.(?:com|io|ai|co|net|org|dev))', re.I)
pat_frontegg = re.compile(r'frontegg[-_]?(vendor|tenant|user)[-_]?id["\s:=]+["\']?([0-9a-f-]{30,})', re.I)
pat_demo = re.compile(r'(clientId|secret)\s*:\s*["\'](CLIENT_ID_[0-9a-f-]+|SECRET_[0-9a-f-]+)["\']', re.I)

for p in (pat_assignment, pat_frontegg, pat_demo):
    for m in p.finditer(bundle):
        s = m.group(0)
        if re.search(r'(color|font|padding|margin|component|module|function|return|var |const )', s, re.I) and len(s) < 50:
            continue
        # print s + 80 chars context
```

## Frontegg identifier block (common in B2B SaaS SPAs)

Frontegg is an embedded-auth vendor. Its client bundle typically leaks:
- `clientId` (public by design — NOT the finding)
- `x-frontegg-api-key` (often a placeholder like `my-frontegg-api-key`)
- `frontegg-vendor-id`, `frontegg-tenant-id`, `frontegg-user-id` → **internal UUIDs**
- Full API surface: `/identity/resources/impersonation/v1`, `/tenants/api-tokens/*`,
  `/directory/.../scim2`, `/account/saml/callback`, `/account/oidc/callback`,
  `/ehr/callback`, `/docusign-return`

**Finding = the internal vendor/tenant/user UUIDs + the full auth/API surface map**,
not the public clientId. These pre-map the tenant's attack surface for an authorized
tester. Mark severity INFO/LOW unless demonstrated impact exists.

## Worked example (Insight Health, 2026-08)

From `app.insighthealth.ai/assets/index-*.js`:
- Frontegg clientId `49d00095-0a11-47c5-854b-fc3e2d04f709` (prod)
- `frontegg-vendor-id 04ae2174-...`, `frontegg-tenant-id 02e6ab6f-...`, `frontegg-user-id e5c397a1-...`
- Demo token pair `CLIENT_ID_16806d3d-...` / `SECRET_16806d3d-...` (preview-only)
- Undocumented subdomains via `baseUrl` assignments: `safe.api`, `careai`,
  `admin/aiva/ambient/integrations/magicdocs/magicflow .api.insighthealth.ai`
- 3rd-party keys: Stripe `js.stripe.com/v3`, Datadog, GetVIM, Docusign, Segment,
  Personsync clientId `f3083002-...`

Disclosed as an informational/HoF courtesy email (see `report-writing` template
`templates/disclosure-email.md`). No patient data touched; passive only.

## RoE notes

- Passive extraction only. Do not use extracted IDs/tokens to authenticate or attack
  unless you have a legitimate account / written authorization.
- Healthcare/HIPAA targets: never touch production patient data; stay read-only.
- Don't call every `clientId` a "leak" — distinguish public-by-design vs internal IDs.
