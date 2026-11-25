---
name: spa-bundle-recon
description: Audit minified SPA, webpack, React, or Vue JS bundles for hidden API attack surface. Use when a web target ships a frontend bundle (assets/*.min.js, chunks, source maps) and you need to map endpoints, auth headers, API keys, and OAuth config before hunting. Encodes the critical "READ EVERY FILE COMPLETELY, no grep allow-listing" lesson plus the curl-gzip, proxy-base, and live-archive pitfalls that cause real endpoints to be missed. Trigger words include JS bundle, SPA, webpack, source map, React, chunk, frontend recon, endpoint extraction, client-side API discovery.
---

# SPA / JS Bundle Source Recon

Goal: recover the FULL API attack surface from a minified frontend so you don't miss
endpoints, auth headers, keys, or staging hosts.

## THE #1 MISTAKE (cost a real engagement real findings)
Do NOT pre-filter extraction with allow-lists like `grep '/api|/user|/v1'`. That hides
attacker-relevant routes. In one engagement, allow-list grep missed `/firebase/tokens/:registrationToken`,
`/maintenance.json`, `/update-short-password`, and the entire `/loot-boxes/*` (gacha/invite)
+ `/prediction-comments` API. They surfaced ONLY after a COMPLETE file read with no filtering.

Operator rule: load every bundle fully; extract ALL paths/URLs/template-literals/call-sites;
let dedup sort signal from noise. The user explicitly corrected this: "NO grep. NO Filtering.
read each file completely."

## Step 1 — Download (DECOMPRESS)
Servers gzip-encode. A bare `curl` saves raw gzip (magic `1f 8b 08`); your parser reads garbage.
```bash
curl -s --compressed -o js/chunk.js "https://TARGET/assets/chunk.abc.min.js"
file js/chunk.js   # must say "JavaScript/ASCII text", NOT "gzip compressed data"
# recover if already grabbed compressed: for f in js/*.js; do mv "$f" "$f.gz"; gunzip "$f.gz"; done
```

## Step 2 — Complete extraction (no allow-list)
```python
import re, glob, os
d = "js_dec"
alltext = "\n".join(open(f, encoding="utf-8", errors="ignore").read() for f in glob.glob(f"{d}/*.js"))
urls = sorted(set(re.findall(r'https?://[^\s"\x27\\]+', alltext)))
wss  = sorted(set(re.findall(r'wss?://[^\s"\x27\\]+', alltext)))
rel  = sorted(set(re.findall(r'["\x27](/[a-zA-Z0-9_\-]+(?:/[a-zA-Z0-9_\-:.{}?=&]+)+)["\x27]', alltext)))
tmpl = sorted(set(re.findall(r'`([^`]*\/[a-zA-Z0-9_\-][^`]*)`', alltext)))  # placeholder
calls = sorted(set(re.findall(r'\b(?:get|post|put|delete|patch)\s*\(\s*["\x27](/[^"\x27]+)["\x27]', alltext)))
cfg  = re.findall(r'window\.__CONFIG__\s*=\s*(\{.*?\});', alltext, re.DOTALL)
```
Capture: absolute URLs, relative paths (even `/a/b` noise), template-literal paths
(backticks = dynamic construction), `e.post/e.get(... "/...")` call sites, and inline
`window.__CONFIG__` / env (API base, keys, OAuth client ids, staging hosts in
`authorizedDomains`). Do NOT restrict `rel`/`calls` to `/api|/user|/v1`.

## Step 3 — Find the REAL API base (proxy vs origin)
Client often calls the API via a same-origin proxy prefix (`baseURL = "/z"`) but the edge
(CDN/Varnish) may 404 that prefix. The REACHABLE surface is usually the origin
(`https://api.target.com/v1`). Before declaring an endpoint dead:
- grep bundle for `API_URL`, `PROXY_ENDPONT_PREFIX`, `baseURL`, `create({baseURL`
- probe BOTH `https://TARGET/z/<path>` AND `https://api.TARGET.com/v1/<path>`
- watch double-prefix bugs (`api.com/v1` + `/v1/users` => `/v1/v1/users`)
- capture auth header shape: `Authorization: Bearer <jwt>` from a `token` cookie,
  `X-XSRF-TOKEN` double-submit, App Check, custom `X-*` (draft/mirror/feature-flag
  headers are ATO/IDOR leads)

**The base is often a same-origin VERSION PREFIX, and a catch-all shell will hide that from you.**
Angular builds ship the prefix in their environment object — grep for it explicitly rather than
assuming the API sits at `/`:
```bash
grep -ohE '(baseHttpServerPath|baseWebsocketServerPath|activitiesBaseUrl|settingsBaseUrl|engagementBaseUrl|apiBaseUrl|API_URL)\s*:\s*"[^"]*"' main*.js
# e.g. {production:true, baseHttpServerPath:"/3.0/", activitiesBaseUrl:"/3.0/", settingsBaseUrl:"/3.0/"}
```
Cost of missing it: probing `w/event/1/token` returned the **91 KB SPA HTML shell with status 200**
— which reads as "the API returned the app, this endpoint doesn't exist" — while
`3.0/w/event/1/token` returned the real API's JSON (`401 MissingSecurityContext`) and
`3.0/document/<id>/file?token=` returned `500 jwt malformed`. Same host, same paths, opposite
conclusions.

Rule: **if several unrelated probed paths all return the identical byte-for-byte HTML shell, you
have hit the router's catch-all — that is not evidence the endpoints are absent.** Confirm by hashing
two responses and comparing sizes; then either extract the prefix from the env object above or take
it from the live XHR (Step 3b). A single 200-with-shell response must never be recorded as a
negative for an endpoint.

## Step 3b — API base NOT in the bundle? Read the LIVE XHR, not the source

Some SPAs inject the API base at runtime (Angular `environment` replaced at deploy, ICM/PWA,
Spartacus). Then `grep 'https://'` returns only vendor demo hosts and you conclude "no API base
here" — wrong. Ask the already-loaded page what it fetched:

```python
# isolated Firefox + Marionette (see browser-isolation); the `return` is mandatory
m.execute_script("""
  return performance.getEntriesByType('resource')
    .map(r => r.initiatorType + ' ' + r.name)
    .filter(s => /xhr|fetch|rest|api|graphql/i.test(s)).join('\\n');
""")
```

Synchronous, no network, and it surfaces exactly what the bundle hides: backend host, base
site/tenant, locale path shape, third-party APIs (search, CMS, analytics). Generalises to any
runtime-configured frontend.

Worked platform example: `references/intershop-icm-pwa.md` — Intershop ICM + Angular PWA, including
the base-site/application enumeration **oracle** (150-byte "System status" = unknown site;
81-byte "Application 'x' not found in context of site 'y'" = **site exists**; 401 on the `-` app =
the real auth-gated shop), the `configurations` endpoint that needs a vendor `Accept` media type,
and the 3-request anonymous-basket authorization test.

## Step 4 — Live archive reveals hidden endpoints
`waybackurls TARGET.com` (background, slow) surfaces routes NOT in current bundles
(legacy/mobile APIs). Mine, filter static assets, keep `/v1/ /api/ /users /auth /charge
/loot-boxes`. Diff vs current bundles = hidden attack surface (gacha state, prediction
APIs) = prime authenticated IDOR/race targets.

## Step 5 — Confirm with read-only probes
Status-only, unauth first. 200/405 (method-not-allowed) proves the route exists; 401 =
auth-gated (bring a test account); 404 on wrong proxy path is NOT proof of non-existence.

## Authored reference
`references/full_read_recipe.md` — exact re-runnable Python extraction + archive-mining snippet.
