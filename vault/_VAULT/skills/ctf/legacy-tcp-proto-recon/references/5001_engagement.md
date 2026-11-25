# Reference: 5001 "legacy network service" engagement (MISC, BI{...})

Target: http://2.29.10.21:5001/  (host also runs 8080 BrokerLink, 8000 Helios bot, 5000 Vaultify)
Challenge: "A legacy network service has produced evidence of unusual sessions and unexpected
activity. Connect to the service, investigate its behavior, and uncover what happened."

## Protocol (CONFIRMED, repeated runs)
- Raw TCP line protocol. Banner on connect: `200 broken-protocol/1.0 ready`
- Only TWO valid verbs (everything else -> `400 unknown command`):
    GET  <path>          -> 401 not authenticated
    AUTH <user> <pass>   -> 403 auth rejected
- Leading-space line (` GET /flag`) -> server treats as CONTINUATION: holds connection,
  no reply (b'' with OPEN). NOT an auth bypass.
- Empty line -> 400. Newline injection inside AUTH -> processed line-by-line (AUTH 403 + GET 401).

## Auth wall — ALL returned 403 (exhaustive)
- ~200 user:pass guesses: admin/admin, root/root, broker/broker, admin/monitor (was a FLAKE,
  not a bypass), legacy/legacy, reviewer/reviewer, service/..., corvid/corvid, etc.
- AUTH single-token, SASL (PLAIN/LOGIN/ANONYMOUS/EXTERNAL)+base64, base64(user:pass)
- NUL byte, tab, trailing/leading space, `;`, `` ` ``, `$(` injection
- JWT as AUTH arg: alg=none + kid brokerlink-2019, HS256 (empty/guess), Bearer <jwt>
  -> 5001 REJECTS the 8080 BrokerLink JWT (different auth; don't assume shared creds)
- newline injection (AUTH x\nGET /flag\n) -> each line separate: 403 + 401
- scenario-themed creds borrowed from 8080 BrokerLink

## Companion services (same host)
- 8080 BrokerLink (Flask): JWT verifier BROKEN — alg=none + kid brokerlink-2019 ACCEPTED.
  POST /api/v2/internal/documents/review with header X-Corvid-Channel: broker
  -> 403 "reviewer role required" (auth passed verifier; role is server-side).
  No JWKS/public key exposed (/.well-known/jwks.json, /api/v2/public_key -> 404) so
  algorithm-confusion (RS256->HS256) not directly possible. Box went DOWN (ConnectionError)
  mid-engagement — flaky infra.
- 8000 Helios Logistics support bot (separate challenge).
- Source map legacy-broker.9f14.js.map hint: "tokens minted before the 2026 rotation used
  kid 'brokerlink-2019' and are still honored by the verifier for backwards compatibility."

## What was NOT solved / open questions
- 5001 flag NOT obtained. Needs a valid credential or the intended "broken protocol" trick.
- The "broken-protocol/1.0" name implies a parsing quirk (smuggling / length-prefix / state
  machine) that was NOT found by blind probing — likely needs a hint or the protocol spec.
- 8080 BrokerLink: broken-JWT confirmed but needs a "reviewer" identity (real signing key or
  a specific verified sub/role mapping) to reach the flag.

## Repro recipes (scripts live in /home/user/Ctf/ctf7/legacy/)
- probe_final.py / dump_probe.py: verb + GET-path sweeps (the banner-timing false positive
  happened here — see SKILL.md Pitfalls).
- admin_monitor.py: the AUTH admin monitor "bypass" verification (confirmed 403 on retry).
- broker_kid.py / broker_claims.py / broker_channel.py: 8080 JWT kid/claim/channel brute.
- SEE skill scripts/probe_template.py for the CLEAN version to reuse next time.
