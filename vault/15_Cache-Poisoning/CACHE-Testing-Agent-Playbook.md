---
title: "Cache Testing Agent Playbook — the executable protocol"
type: agent-playbook
category: cache-poisoning
cwe: "CWE-524, CWE-525, CWE-444"
built: "2026-11-07"
corpus: "15 rows, 15 full bodies (h1-brain disclosed_reports.db)"
bounty: "$6,506/6 paid · header reflection $2,206/3 · path/implementation $4,300/2 · deception $0/0 recorded"
companion_modules: "01 unkeyed-header-reflection · 02 cache-deception-and-key-manipulation · 03 cache-implementation-and-path-tricks"
quote_rule: "byte-true to CACHE-bodies-full-dump.txt"
---

# CACHE Testing Agent Playbook

## P0 — Preconditions & safety (before any request)

1. **Confirm a cache exists**: look for `X-Cache`, `CF-Cache-Status`, `Age`, `Via`,
   `X-Served-By`. CACHE-1795197's proof pattern is the model — MISS then HIT:
   > 2. You should notice the `Cf-Cache-Status: MISS` header when first sending the request. After sending another request, you should see `Cf-Cache-Status: HIT`, confirming the redirect has been cached.
2. **Do not hit real users.** Poison only with a unique query string on a URL nobody else
   requests; CACHE-303730 says it plainly:
   > Please be careful when exploring this issue, as it's potentially quite easy to accidentally poison CloudFront's cache and antagonise your visitors.
3. **Kill-gate**: `Cache-Control: no-store`, `Vary` on the header you plan to use, or a
   per-user cache → stop.

## P1 — Cache key analysis

Enumerate what the cache *keys on* versus what the origin *reads*:

| Input the origin reads | Test | Evidence |
|---|---|---|
| `X-Forwarded-Host`, `X-Forwarded-Scheme`, `X-Forwarded-Proto`, `Forwarded` | reflect a marker, see if it is cached | CACHE-977851 / 303730 / 394016 / 1795197 |
| `User-Agent` | send a marker UA once, then request without it | CACHE-2917062 |
| Host case / trailing dot | `Evil.com` vs `evil.com` | CACHE-1374512 |
| Path normalization (`\` vs `/`, `%00`, `..`, `;`) | request both forms, compare cache key | CACHE-1695604 / 334709 / 1848940 |
| Extension → cacheability | append `.jpeg`/`.js`/`.css` to a dynamic path | CACHE-1698316 / 260697 |

## P2 — Differential probes

1. Send request **A** with a unique marker value in the candidate header.
2. Send request **B** *without* the header, same URL.
3. If **B** contains the marker, the entry is poisoned and keyless — that is the whole PoC.
4. For path differentials, request the normalized variant and check whether the response for
   the canonical path changes (CACHE-1695604's backslash → 404).

## P3 — Proof ladder

1. **Reflection** — the header appears in the body (weakest).
2. **Persistence** — response without the header still contains it (CACHE-977851).
3. **Cross-client** — a second browser/identity receives the payload.
4. **Impact** — JS execution (CACHE-303730), redirect of a `.js` asset (CACHE-1795197), CDN-wide
   404 (CACHE-1695604), or victim session/CSRF token stolen (CACHE-1698316).

## P4 — Modern hardening fingerprints

- CDNs now commonly key on `X-Forwarded-Host` where the origin actually uses it; test the
  broader set (`X-Forwarded-Scheme`, `X-Original-URL`, `X-Host`, `Forwarded`, `X-Forwarded-Port`).
- `Vary: *` and `no-store` on authenticated pages are the fix for deception rows.
- HTTP/2 pseudo-header normalization and CDN path canonicalization (backslash, `%2f`) collapse
  the implementation module's differentials on newer edges — retest, don't assume.
- Framework-level host checks now compare downcased hosts (CACHE-1374512's CVE).

## P5 — Kill-gates

1. **No cache entry** → it is a header-injection finding; move it to `../24_Host-Header-Injection/`.
2. **Reflection with `Vary` on the header** → not exploitable by caching; report only if the
   header reaches a non-cache sink (email link, reset token).
3. **Self-only impact** (your own cache entry) → nothing to report; find the victim path first.
4. **DoS rows** — confirm the 404/redirect survives for a second client before claiming mass impact.
5. **No victim demonstration** = no report; the corpus pays reach, never mechanism.

## Module ↔ phase table

| Phase | Modules | Paid pattern |
|---|---|---|
| P1 key analysis | 01, 03 | find the unkeyed input |
| P2 differential | 01, 03 | marker → re-request without marker |
| P3 proof | 01, 02 | second client gets payload / session |
| P4 hardening | 01, 03 | CDN `Vary`, path canonicalization |
| P5 gates | 02, 03 | deception needs a real secret in the page |

## Non-goals

- Browser cache poisoning via service workers beyond the AppCache row (CACHE-84601) — not
  evidenced elsewhere in the corpus.
- Cache-key squatting on third-party CDNs without an authorized target.
- DoS testing against production without written scope — use staging or a bounded request count.
