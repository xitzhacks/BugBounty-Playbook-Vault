# URL-corpus XSS sweep — pipeline, counters, and contamination traps

Built on a live engagement (trendspider.com, 2026-10) after the operator pushed back on a
page-sampled sweep: *"have you first collect urls then test for every parameter for reflection
then test xss? for each urls?"*. This file is the answer to that question as a procedure.

## Pipeline

```
stage 0  corpus        gau <domain>  +  katana -d 2 on N seeds  →  URLs with query strings
stage 1  map           dedupe → (host,path) → {params}          →  endpoint_params.json
stage 2  reflection    one marker per (endpoint,param)          →  reflection_results.jsonl
stage 3  encoding      hostile payload per reflective pair      →  encoding_results.jsonl
stage 4  execution     headless Chrome on survivors only        →  dom_xss_*.json
```

Measured counts on that engagement:

| Stage | Number |
|---|---|
| URLs with query strings (gau 3,704 + katana 1,312) | 5,016 |
| unique endpoints | 891 |
| endpoint+param pairs | 1,757 |
| requests issued (incl. retry) | 2,690 |
| unique reflective pairs after contamination filter | 325 |
| `SAFE:URLENC` / `SAFE:ENTITY` | 219 / 9 |
| `NO-ECHO` on hostile payload | 100 (all resolved: not reflective) |
| **RAW breakouts** | **0** |
| headless-Chrome execution runs | 110, **0 executions** |

## Stage 0–1 details

- Filter before mapping: drop static extensions (`.png|jpg|css|js|woff|pdf|xml|json|svg`),
  CDN / third-party-SaaS hosts, and malformed keys (`MVfs343d`, `ampaign`, `edium` come from
  broken archived URLs and pollute the map).
- Key the map by `(host, path)` — **store the scheme**, or the scanner later dies on
  `ValueError: unknown url type`. Rebuild as `https://{host}{path}` before scanning.
- `gau` covers the apex only on most targets; the app/help/support hosts come from `katana`
  seeds (`/login/`, `/register/?plan=…`, `/`, `/signin/`). Two crawl rounds added 9k query
  URLs the archive never had.

## The contamination trap (this is the one that wastes a session)

At 12 threads the estate answered `503` for 857 of 1,597 requests, and on retry `202` — a
SiteGround captcha page. That page **echoes the request URL**:

```html
<meta http-equiv="refresh" content="0;/.well-known/sgcaptcha/?r=%2Fpricing%2F&y=ipc:…">
```

So a marker-in-body detector reports a reflection for every throttled request. Rules:

1. Discard `202`, `503`, and `0` responses, and anything with `sg-captcha: challenge`.
2. Retry the discarded set at **3–5 threads** with exponential backoff (2s → 4s → 8s).
3. Only what survives both is a reflection.

### Getting past the captcha for the retry (SiteGround PoW)

The challenge is a 21-bit SHA1 proof of work; solve it once and keep the `_I_` cookie
(30-day lifetime):

- Parse `sgchallenge` (`<complexity>:<timestamp>:<rand>:<hash>:`) and `sgsubmit_url` from
  `/.well-known/sgcaptcha/?r=<path>`.
- Find `counter` such that `SHA1(challenge_bytes + minimal_big_endian(counter))` has
  `complexity` leading zero bits.
- Submit `?sol=base64(challenge_bytes + counter_bytes)&s=<elapsed_ms>:<hash_count>`; the
  response sets `_I_=<hash>-<ts>-<complexity>`.

**The `_I_` cookie is User-Agent bound.** It works only with the exact UA used when solving
(on this target `Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36`). Replaying it with
`curl/8.5.0` silently returned `202` again, which reads as "the bypass stopped working".
Carry the UA and the cookie together, in the same client.

Separate fingerprint note: a bare Chrome UA (no `Accept-Language`/`Sec-Fetch-*`) got a uniform
`403` on every URL of the same site, while `curl/8.5.0` got `200`. Pick one UA on purpose per
phase — see `recon-pitfalls` §12.

## Stage 3 details — resolving `NO-ECHO`

A pair can reflect a plain marker and then not contain the hostile payload at all. Three
distinct causes, and only one probe separates them:

```
cpmarkx          → no echo at all      => not reflective now (captcha/cache residue) — drop it
cpmarkx"         → quote survives      => attribute-context candidate, inspect the quoting
cpmarkx<         → tag survives        => RAW candidate, escalate to stage 4
cpmarkx%22%3E    → only encoded form   => URLENC, safe in HTML text
```

Record the answer per pair. "It didn't echo the payload" is not the same finding as "it
encoded the payload", and the difference shows up in the report.

## Stage 4

Only feed stage 4 with pairs that reached `RAW`/`RAWQ`, or with pages whose JS has a proven
source→sink edge. Strict hit definition (title equals bare marker, or payload-owned node id)
lives in `hunt-xss` SKILL.md and `scripts/dom_xss_dumpdom.py`; the tracker-pixel and
title-echo false positives documented there came from exactly this engagement.

## Artefact layout

```
pipeline/
  urls_q.txt  kata.txt  kata2.txt            # corpora
  endpoint_params.json                       # the map
  reflection_results.jsonl                   # pass 1 (pre-captcha fix — keep for audit)
  reflection_cookie.jsonl                    # captcha-bypassed retry
  encoding_final.jsonl                       # verdict per reflective pair
  context_summary.txt                        # og:url 190 / script 123 / attr 5 / Alpine 6
  reflection_scan.py retry_scan.py finalize.py
```
