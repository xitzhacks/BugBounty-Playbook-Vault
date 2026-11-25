# Custom line-protocol / raw-socket MISC recon — worked example

## Scenario
Challenge "legacy network service" (MISC, BI{...} flag): `http://2.29.10.21:5001/`.
`curl` returned empty body + `Received HTTP/0.9 when not allowed` -> NOT HTTP. It is a
custom line protocol over TCP.

## Banner
Raw Python socket (socket.socket(), NOT /dev/tcp redirection — the safety layer blocks
that). On connect the server sent:
```
200 broken-protocol/1.0 ready
```
Every \r\n-separated line sent afterward is treated as one command.

## Verb / response mapping (the whole recon)
Sent candidate verbs one per line; reply codes are the map:
- GET /flag           -> 401 not authenticated    (verb EXISTS, needs auth)
- AUTH admin admin    -> 403 auth rejected         (verb EXISTS, bad cred)
- HELP/SESSION/LOG/... -> 400 unknown command      (verb does NOT exist)
- <no reply> / b''    -> almost always SERVER FLAKINESS, not a hidden command

After a 3x-retry sweep, only GET and AUTH are valid verbs. No other command exists.

## What failed (do not repeat)
- AUTH user:pass brute (~100 combos) -> all 403
- AUTH single-token list, SASL mechs, NUL/tab/format tricks -> all 403
- AUTH forged JWT (alg none + kid, HS256) -> 403
- HTTP-style requests with Authorization / X-Admin / Cookie headers -> still 401
- Leading-space / folded-line tricks: ` GET /flag` returns b'' because the parser treats
  it as a no-op/continuation buffer (the folded string literally does NOT match GET), NOT
  an auth bypass. Verified via hex dump.

## The real pivot: chained services
Port scan of the host (fast Python connect scan, not nmap which hangs) showed open:
5000, 5001 (target), 8000 (Helios support bot), 8080 (Corvid BrokerLink Flask).

8080 /status mentioned incident BL-2026-0812-17 + "legacy-broker client (compat shim)".
Reading /static/js/legacy-broker.9f14.js then its .js.map leaked, in sourcesContent:
- internal API: POST /api/v2/internal/documents/review with headers
  Authorization: Bearer <tok> and X-Corvid-Channel: broker
- comment: "tokens minted before the 2026 rotation used kid: 'brokerlink-2019' and are
  STILL honored by the verifier for backwards compatibility"

Forging an alg:none JWT with kid: brokerlink-2019 and POSTing to that endpoint:
- X-Corvid-Channel: broker -> 403 reviewer role required   (AUTH PASSED, role check hit)
- other channels -> 400 channel header required
So the JWT verifier IS broken (alg none accepted) but the reviewer role is server-side.
The 5001 credential/flag is almost certainly reachable through this chain, not by
guessing 5001's AUTH directly.

## Takeaways for any such challenge
1. curl empty + "HTTP/0.9" => switch to a raw socket, grab the banner.
2. Map verbs by 4xx code; require 3 consistent non-flaky reads before trusting a "new" verb.
3. If GET->401 / AUTH->403 for everything, the cred is NOT guessable — port-scan the host,
   read companion web apps' JS + .js.map, and pivot.
