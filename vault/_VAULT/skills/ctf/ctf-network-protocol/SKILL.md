---
name: ctf-network-protocol
description: Raw TCP / line-based "legacy network service" CTF challenges where curl returns empty + "HTTP/0.9 when not allowed" (i.e. NOT HTTP — a custom text protocol). Covers banner grabbing, mapping valid verbs via 400 vs 401/403, hunting "broken protocol" parser-state anomalies (leading space, empty line, framing quirks), and correlating with companion web services (port scan + JS/source-map extraction) to recover creds or the protocol handshake. Use for MISC/Hard challenges phrased as "legacy network service", "unusual sessions", "investigate its behavior", "broken protocol", or any non-HTTP port that speaks a custom line protocol.
---

# CTF — Raw network-service / line protocol

## When to load
- Challenge says "legacy network service", "connect to the service", "investigate its behavior", "unusual sessions / unexpected activity", "broken protocol", and the flag is a non-standard wrapper (e.g. `BI{...}`).
- `curl http://host:port/` returns an EMPTY body and curl verbose shows `Received HTTP/0.9 when not allowed` → it is a raw line protocol, not HTTP. (Empty curl body is the SIGNAL, not a failure.)
- A port scan shows a listen that isn't a web server but you can connect to it.

## Workflow
1. **Confirm it's not HTTP.** `curl -s -v http://host:port/` — if you see `HTTP/0.9 when not allowed` or empty body, switch to a raw socket.
2. **Banner grab with a Python socket** (do NOT use `/dev/tcp` bash redirection — the safety layer blocks it; use `python3` or a script). Connect, read the first `recv` for the banner. The banner often names the protocol (e.g. `200 broken-protocol/1.0 ready`) and is a direct hint about the intended bug.
3. **Map verbs.** Send candidate UPPERCASE verbs one per connection (lowercase is often rejected with 400). Classify responses:
   - `400 unknown command` → verb doesn't exist
   - `401 not authenticated` / `403 auth rejected` → verb EXISTS but is gated (auth wall); the distinct code vs 400 confirms validity
   - `200 ...` or any structured reply → verb exists and responded
   - `b''` (empty) → AMBIGUOUS: see Pitfalls (usually flakiness, sometimes a real state shift)
4. **Map paths/args** on the valid verb(s) (usually GET): sweep `/flag`, `/sessions`, `/secret`, `/data`, `/admin`, `/logs`, `/audit`, etc. A 401 on all = auth required everywhere; note any path that behaves differently (e.g. trailing slash returns no 401).
5. **Hunt the "broken protocol" bug** (this is usually the intended vuln). Try framing quirks on a gated command and capture the FULL response with a long read window:
   - **Leading space**: `" GET /flag"` (space before verb) — observed to flip the parser into a no-reply / different state.
   - **Empty line first**: send `\r\n` then the command.
   - **Trailing slash / query string**: `GET /flag/` vs `GET /flag`.
   - **Inline token**: `GET /flag <token>`, `GET /flag?auth=x`.
   - **Control chars / NUL** inside the command.
   The exploit often arrives without a trailing `\n`; a size-capped or newline-breaking reader will truncate it — read raw into a buffer with a fixed timeout.
6. **Correlate with companion services (key technique).** These scenarios are usually multi-service. Port-scan the host (fast Python connect scan, 0.3s timeout) for siblings. For each web sibling:
   - Fetch `/`, grep for JS bundles, fetch the JS, and **always fetch the `.js.map` / source map** — source maps leak server-side logic (e.g. an `INTERNAL` API path, auth-header names, or a comment like "tokens with kid 'X' are still honored for backwards compatibility" = JWT alg-confusion / forged-kid bypass).
   - The sibling may contain the exact client that talks to your target service ("legacy-broker compat shim") → reveals the real AUTH format/creds or the handshake the protocol expects.
7. **Auth-bypass attempts** (only after mapping): if AUTH exists, try user:pass lists, single-token, SASL mechanisms (PLAIN/LOGIN/ANONYMOUS/EXTERNAL), and format tricks. If ALL return 403, cred-guessing is the WRONG path — the vuln is the protocol/state bug, not the password. Pivot to framing/state anomalies fast.

## Pitfalls
- **Flaky services masquerade as hidden commands.** When the box is overloaded, connections get refused / time out and your reader returns `b''`. This LOOKS like "valid command, no output" but it's noise. Rule: re-run any `b''` case 2x. If it's inconsistent → flakiness, IGNORE. A real valid verb returns a CONSISTENT code (400/401/403) every time. (Wasted many probes chasing phantom verbs SEARCH/NODE/NET/SCAN/STATS that were actually timeouts.)
- **`b''` from AUTH is NEVER an auth bypass — prove it with a same-connection GET.** In the 5001 engagement a full 34×38 credential MATRIX returned ONLY `b''` "hits" (admin/default, admin/corvid, admin/legacy, admin/P@ssw0rd, admin/monitor). Every one was a connection DROP under load, not auth success. Decisive test: re-run each 3× sending `AUTH x y` then immediately `GET /flag` on the SAME socket. A flake returns `403 auth rejected` then `401 not authenticated` consistently (true for all 5 `b''` candidates). RULE: a `b''` from AUTH is inconclusive at best — note whether the socket stayed OPEN (real continuation/buffering) vs CLOSED (dropped conn), and always follow with a same-connection GET; if GET still returns `401`, auth did NOT flip. Only a GET returning real data proves the auth state changed.
- **Banner-timing mis-attribution creates PHANTOM valid verbs.** If your read loop captures the connect-time banner (`200 ... ready`) into the SAME buffer as a command's response, the banner can get mis-attributed to the first command — making a real `400 unknown command` verb appear to return `200 broken-protocol/1.0 ready` (looking like a valid command!). This burned a full detour in 5001 (DUMP / GET /index "worked" → both were just the banner echo). FIX: store the connect-time recv in a SEPARATE `banner` variable and never let it pollute command-response reads; better, open a FRESH socket per command for confirmation, or send a throwaway command first to flush.
- **alg=none JWT may pass a sibling verifier but still 403 on a server-side role check** that reads a verified identity, not a payload claim. On the 5001 host, 8080 BrokerLink's JWT verifier was BROKEN: a forged `alg=none` JWT with `kid: brokerlink-2019` was ACCEPTED (`POST /api/v2/internal/documents/review` + header `X-Corvid-Channel: broker` → `403 reviewer role required`, proving auth passed the verifier). But the "reviewer" role was server-side: ~30 brute-forced claim names/values all → 403, and no JWKS/public key was exposed (/.well-known/jwks.json, /api/v2/jwks, /public_key all 404) so RS256→HS256 algorithm confusion was impossible. AND 5001 REJECTED that BrokerLink JWT as an AUTH arg → the two services did NOT share creds. Lesson: a broken JWT on a sibling app does NOT mean the raw-port service accepts it; don't assume shared credentials.
- **Don't use `/dev/tcp` redirection** in bash — the safety layer blocks it. Use a Python socket script.
- **Size-capped / newline-breaking readers miss exploit output.** If the flag comes back without a trailing `\n` or as a streaming blob, a loop that breaks on `b"\n"` truncates it. Read raw into a buffer with a fixed timeout and inspect the full bytes.
- **Empty curl body ≠ service down.** It means non-HTTP. Proceed to socket probing.
- **Don't over-invest in cred guessing** for a "broken protocol" challenge — the bug is the parser, not the password.

## Support
- `references/legacy_service_probe.md` — condensed recon recipe + the 5001 worked example (banner `200 broken-protocol/1.0 ready`; verbs GET→401, AUTH→403; leading-space `" GET /flag"` → no-reply anomaly; companion 8080 BrokerLink source map revealing `kid: brokerlink-2019` JWT still honored).
- `scripts/probe_service.py` — reusable raw-socket prober: banner grab + verb sweep (400/401/403 classification) + path sweep + framing-anomaly check, with consistent full-byte read.
