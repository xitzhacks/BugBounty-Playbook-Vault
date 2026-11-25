# Exposed Dev Servers — production Vite / webpack-dev-server / Next-dev

A build tool left bound to the internet is a **source-code disclosure** primitive, and it is
routinely missed because the root URL returns a normal-looking SPA shell. The tell is a
development-only endpoint answering **200**, not a build artifact.

## Detection signatures (send these first, 4 requests)

| stack | dev-only path | proves |
|---|---|---|
| Vite | `GET /@vite/client` | dev server (179 KB `text/javascript`, contains HMR client) |
| Vite | `GET /src/main.jsx`, `/src/App.jsx` | raw source, not bundled |
| Vite | `GET /vite.config.js` | build config, proxy table, internal host/IP |
| Vite | `GET /package.json` | deps + scripts |
| Vite | `GET /node_modules/.vite/deps/_metadata.json` | dependency graph, lockfile hash |
| webpack-dev-server | `GET /__webpack_hmr`, `GET /webpack-dev-server/` | `text/event-stream` HMR |
| Next.js (dev) | `GET /_next/static/development/_buildManifest.js` | dev build |
| Angular | `GET /@angular/` or `/main.js` with `webpack-dev-server` headers | dev bundle |

A production build never serves `/@vite/client` — if it 200s, the dev server itself is exposed.

## What to extract, in this order

1. **`vite.config.js`** — `server.host` often an internal IP, `server.port`, `allowedHosts`,
   and the `proxy` table. The proxy table is the jackpot: it names production API origins and
   the path rewrite, e.g.
   ```js
   host: '172.31.101.197', port: 8505,
   proxy: { "/dev": { target: "https://prod-api.example.com",
                      rewrite: p => p.replace(/^\/dev/, "") } }
   ```
   That is: private IP + port + the API base you could not otherwise reach.
2. **Entry files** — `/src/main.jsx` imports enumerate the real tree
   (`pages/`, `contexts/`, `services/`, `hooks/`). Each is fetchable at its own path; walk the
   imports one level at a time to recover the whole app.
3. **Inline source maps** — Vite dev serves each module with
   `//# sourceMappingURL=data:application/json;base64,...` appended. Decode it to get the
   **original** file (comments, author emails, internal TODO notes) even if the served JS is
   transformed.
4. **Service modules** — the auth/service layer names every endpoint and header:
   ```bash
   grep -ohE 'fetch\([`"][^`"]+[`"]' *.js *.jsx | sort -u
   ```
   On one engagement this produced the full route map (`/admin`, `/enterprises`,
   `/chat/{sessionToken}`, `/reports/{taskId}`, `/reports/download?token=`, `/invite`,
   `/validate-token?invite_token=`) which was then tested for BAC.
5. **Env/config** — `package.json` scripts sometimes embed deploy hosts; `_metadata.json`
   pins dependency versions (CVE targeting).

## Escalation check — is it file read or disclosure only?

Vite bounds `/@fs/` with a serving allow-list. Test once and record the answer, because it is
the difference between "info disclosure" (P3) and "arbitrary file read" (P1):

```bash
curl -s -o /dev/null -w '%{http_code}\n' https://target/@fs/etc/passwd
# 403 + "The request id /etc/passwd is outside of Vite serving allow list" -> bounded
# 200 + root:x:0:0 -> arbitrary file read, escalate immediately
```

Also try one path **inside** the project root (`/@fs/<root>/package.json`); a 200 confirms the
allow-list root, which tells you how much of the disk is reachable.

## Verdict and severity

- Source disclosure alone: **P3 / Medium**, `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N` = 5.3.
  CWE-200 + CWE-540 (+CWE-668 for the internal-resource exposure).
- Bump to P2 when the source contains a live credential, or `/@fs/` escapes the project root.
- **Do not** claim "dev server = RCE" — Vite's allow-list and the absence of a write primitive
  make that wrong; state the bounded result explicitly so triage cannot rebut it.

## What makes the report survive triage

Include all four of these, because triage will ask:

1. `HTTP/2 200` + correct `content-type` for `/@vite/client` (proves dev mode, not a build).
2. The exact `vite.config.js` lines with the internal IP/port/proxy target.
3. A note that secrets were **searched and not found**, if that is the case — it prevents the
   "so where's the impact" downgrade.
4. The `/@fs/` 403 result, so the escalation question is pre-answered.

## Fix

Serve `vite build` output as static assets behind the CDN; never expose `vite dev` /
`vite preview`; strip `sourceMappingURL` from production artifacts.

## Worked case (2026-10, TNS VDP)

`https://tnsiqgen.ai.tnsi.com` served the Vite dev server. Recovered: 13 source files
(`AuthContext`, `LoginPage`, `ChatPage`, `authService` + 7 hooks), `vite.config.js` with
internal host `172.31.101.197:8505` and proxy `/dev -> https://tnsiq.ai.tnsi.com`,
`package.json`, and `_metadata.json`. The recovered route map was then probed: every endpoint
returned `401 {"message":"Unauthorized"}` except an intentionally public invite-token
validator, so the API authz held and the finding stayed information disclosure.
`/@fs/etc/passwd` -> `403 Restricted` (bounded, no file read).
