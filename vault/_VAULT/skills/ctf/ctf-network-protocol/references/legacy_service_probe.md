# Legacy network-service probe — recipe + worked example

## Reusable recon recipe (raw line protocol)
1. Detect non-HTTP: `curl -s -v http://HOST:PORT/` -> if `HTTP/0.9 when not allowed` or empty body, it's a custom line protocol.
2. Do NOT use `/dev/tcp` (safety-blocked). Use a Python socket script.
3. Per connection: connect, `recv(4096)` for banner, send line + `\r\n`, read with a fixed timeout into a raw buffer (no size cap / no newline-break so exploit output isn't truncated).
4. Classify: `400`=bad verb, `401/403`=valid-but-gated, `200`/structured=responded, `b''`=ambiguous (re-test x2 to separate flakiness from a real state shift).
5. Sweep verbs (UPPERCASE), then paths on the valid verb, then framing anomalies (leading space, empty line, trailing slash, control chars).

## Worked example — CTF host 2.29.10.21 (MISC, BI{...})
Scenario: "legacy network service", unusual sessions. Siblings on host: 5000 (Vaultify), 5001 (target), 5004 (dead), 8000 (Helios support bot), 8080 (Corvid Capital BrokerLink Flask).

Target 5001 behavior (CONFIRMED, consistent):
- Banner: `200 broken-protocol/1.0 ready`
- `GET /<path>` -> `401 not authenticated`
- `AUTH <anything>` -> `403 auth rejected` (100+ creds/mechanisms/tricks all failed -> vuln is NOT the password)
- every other verb -> `400 unknown command`
- REAL anomaly: `" GET /flag"` (LEADING SPACE before verb) -> `b''` no reply (parser state shift). Still under investigation when noted — read with a long window.

Companion 8080 BrokerLink = the key pivot:
- Login POSTs to `/api/v2/login`; on success stores `cvd.tok` in localStorage.
- `/status` references incident BL-2026-0812-17 + "legacy-broker client (compat shim)".
- JS `legacy-broker.9f14.js.map` (source map) leaked server logic:
  - `INTERNAL = /api/v2/internal`; `submitReview` POSTs to `INTERNAL/documents/review` with `Authorization: Bearer <token>`, header `X-Corvid-Channel: broker`.
  - Comment: tokens minted before 2026 rotation used `kid 'brokerlink-2019'` and are STILL honored by the verifier -> JWT algorithm-confusion / forged-kid (none alg or forge a token with that kid) is the 8080-side auth bypass.
- The 5001 legacy service is very likely the backend the broker client talks to; its AUTH format/creds may derive from a broker token.

Open lead at time of writing: confirm whether the leading-space anomaly on 5001 leaks data, and/or obtain a broker JWT via the `brokerlink-2019` kid and feed it to 5001 AUTH. Not yet solved.
