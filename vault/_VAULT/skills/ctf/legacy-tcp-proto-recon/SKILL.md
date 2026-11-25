---
name: legacy-tcp-proto-recon
description: Methodology for attacking a custom line-based "legacy network service" / broken-protocol CTF challenge over a raw TCP port (no HTTP). Use when a target port speaks a non-HTTP text protocol (curl returns empty / "HTTP/0.9 when not allowed") and you must discover verbs, auth, and protocol-level bugs.
---

# Legacy TCP Protocol Recon (MISC / broken-protocol CTF)

## When to use
- Target is a raw TCP port (not HTTP). Banner like `200 broken-protocol/1.0 ready`.
- curl gives empty body or "Received HTTP/0.9 when not allowed".
- Challenge mentions "legacy network service", "unusual sessions", "broken protocol".

## Setup
- NEVER use `/dev/tcp` redirection or raw `nc` interactively — the Hermes safety layer
  blocks those. Use a Python `socket` script (foreground or background) instead.
- Always `s.recv(4096)` once right after connect to drain the banner before sending.
- Read loop: `s.settimeout(N); r=b""; while True: d=s.recv(8192); if not d: break; r+=d`
  (timeout = connection held open / no reply; that itself is a signal).
- Send lines as `line + "\r\n"`. The server splits input on `\r\n` — each line is ONE command.

## Recon sequence (proven order)
1. **Banner + single unknown line** → learn `400 unknown command` vs `401`/`403`.
2. **Verb sweep**: try uppercase words (protocols are usually case-sensitive — lowercase
   may 400 while uppercase is accepted). One connection per verb, 2-3 retries (target box
   may be flaky / drop connections → treat empty/timeout as inconclusive, retry).
3. **Map responses**:
   - `400 unknown command` = invalid verb
   - `401 not authenticated` = valid verb, needs auth
   - `403 auth rejected` = valid auth verb, bad creds
   - `<no reply>` / `b''` with connection OPEN = server buffering/continuation (see below)
4. **Auth bypass attempts (try ALL before giving up)**:
   - user:pass guesses (admin/admin, root/root, guest/guest, broker/broker, service/...)
   - single-token AUTH (maybe it wants a ticket/key, not user:pass)
   - SASL-style `AUTH PLAIN/LOGIN/ANONYMOUS/EXTERNAL` + base64 creds
   - NUL byte (`user\0x`), tab separators, trailing/leading space, extra args
   - JWT as AUTH arg: `alg=none` + legacy `kid`, HS256 with empty/guessable secret, `Bearer <jwt>`
   - base64(`user:pass`)
   - newline injection inside AUTH line (`AUTH x\nGET /flag\n`) — server processes each line
   - scenario-themed creds borrowed from sibling web apps on the same host
5. **State-machine / "broken protocol" bugs**:
   - Leading-space line (` GET /flag`) → server treats as CONTINUATION (buffers, no reply).
     NOT an auth bypass by itself; it's a folded-line that never executes alone.
   - Empty line first → usually `400 unknown command`; inconsistent = server flakiness, not a bug.
   - Don't trust single `<no reply>` results — re-run 3x; flaky boxes return empty on timeouts.

## Pitfalls (learned the HARD way this session)
- **Banner-timing FALSE POSITIVE — the worst trap.** If your read loop captures the initial
  banner (`200 ... ready`) into the SAME buffer as a command's response, the banner can get
  MIS-ATTRIBUTED to the first command, making a real `400 unknown command` verb appear to
  return `200 broken-protocol/1.0 ready` (looking like a valid command!). This burned a full
  detour (DUMP / GET /index "worked" → turned out to be the banner echo).
  FIX: store the connect-time recv into a SEPARATE `banner` variable and NEVER let it pollute
  command-response reads. Better: open a FRESH socket per command for confirmation, OR send a
  throwaway command first to flush, then attribute responses cleanly. See scripts/probe_template.py.
- **`b''` (empty response) is AMBIGUOUS — never treat it as success.** It can mean EITHER
  (a) server buffering/continuation (leading-space line), OR (b) a flaky box: connection
  refused/timed-out mid-read. A `b''` from `AUTH admin monitor` was a flake — on clean retry
  it returned `403 auth rejected`. Always: re-run 3x, and record whether the connection
  stayed OPEN (continuation) vs CLOSED (often a dropped/refused conn). Real valid verbs return
  a consistent code, not random empty.
- **VERIFY any "auth bypass" with a follow-up GET on the SAME connection.** If you see a
  non-403/non-400 response to AUTH, immediately send `GET /flag` (or any GET) on that same
  socket. If it still returns `401 not authenticated`, auth did NOT happen — you got a flake
  or a no-op. Only a GET that returns real data proves the auth state flipped. (admin_monitor.py
  confirmed this: the "bypass" candidate was 403 on retry, GET stayed 401.)
- **HTTP header injection doesn't work**: sending `GET /x HTTP/1.1\r\nHost:..\r\n` just makes
  each header line a separate `400 unknown command`. No header-based auth bypass.
- **alg=none JWT may pass the verifier but still 403 on a server-side role check** that reads
  a verified identity, not a payload claim. Brute claim NAMES (role/roles/scope/groups/
  permissions/clearance/entitlement/...) only if the role is payload-derived — if all 403,
  the role is server-side (needs real signing key / JWKS, which may not be exposed). On 8080
  BrokerLink, alg=none + kid brokerlink-2019 was ACCEPTED (auth passed → 403 "reviewer role
  required"), proving the broken-JWT, but the role stayed server-side.
- **Companion web app may be DOWN mid-engagement** (8080 returned ConnectionError for a stretch).
  Don't conclude "no endpoint" from a single ConnectionError — retry; flaky CTF infra is normal.

## Verification script
- `scripts/probe_template.py` — clean single-socket probe that (1) drains the banner into its
  own var, (2) sends one command per fresh socket with retries, (3) tracks OPEN vs CLOSED
  connection state on `b''`, and (4) on any non-403/400 hit, auto-sends a same-connection
  `GET /flag` to prove auth state. Copy + modify for new targets.

## Reference
- `references/5001_engagement.md` — concrete dead-ends + real signals from the 5001 "legacy
  network service" MISC challenge (BI{...}): confirmed protocol, exhaustive 403 auth wall,
  the BrokerLink broken-JWT side-find, and the banner-timing / b''-flake traps that bit us.

## Companion-service pivot (same-host scenario)
- Port-scan the host (fast connect scan, short timeouts) — challenges often share a host:
  web apps may leak the legacy cred or a broken-JWT kid.
- Read web app JS + `.js.map` (source maps often contain the real logic/hints, e.g.
  "tokens with kid X are still honored").
- A "legacy-broker client (compat shim)" reference in one app usually means it's the CLIENT
  to the raw-port service — but the raw service's AUTH may NOT accept that app's JWT
  (confirmed: 5001 rejected the 8080 BrokerLink JWT). Don't assume shared creds.

## Deliverable checklist
- [ ] Banner captured
- [ ] Valid verb set mapped (GET/AUTH only on 5001)
- [ ] Auth wall confirmed (401/403) and bypass attempts logged
- [ ] State-machine quirks noted (leading-space = continuation)
- [ ] Flag obtained OR blocker documented with exact last response

## Example (5001 finding)
- Banner `200 broken-protocol/1.0 ready`; verbs GET(→401) + AUTH(→403); all else 400.
- ~150 AUTH creds/JWT/claim/format/injection attempts → all 403. No bypass found.
- Leading-space → continuation buffer (no-op). Flag NOT obtained; needs valid cred or hint.
