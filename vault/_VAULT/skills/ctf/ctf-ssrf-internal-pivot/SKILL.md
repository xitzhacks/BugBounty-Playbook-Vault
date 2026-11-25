---
name: ctf-ssrf-internal-pivot
description: CTF technique for the SSRF-to-internal-file-read class ("path-tricks" / `/read?path=` challenges) plus the CONVERGE workflow discipline this user ([REDACTED_PII]) repeatedly demands. Capture from a CTF7 Blackglass session where the agent scattered across ~10 vectors (5004 LFI, BrokerLink JWT forge, Aetheria, port scans) instead of converging. Use whenever a CTF web challenge is an SSRF sink reaching internal services, and whenever this user says "do one thing" / "just see what it says".
---

# CTF SSRF → INTERNAL PIVOT + CONVERGE DISCIPLINE

## Part A — CONVERGE (this user's explicit correction)
The user repeatedly directs "do one thing" / "just see what it says" when stuck. This is a
workflow correction, not a one-off:
- Do NOT scatter across many unrelated vectors in one turn (e.g. a 5004 LFI trick AND a BrokerLink
  JWT forge AND an Aetheria injection AND a port scan simultaneously).
- Pick ONE most-likely vector. Exhaust it surgically. Report the DEFINITIVE wall (server's exact
  message, what you tried, why blocked). Then ask the user for the next vector.
- Re-confirming the same wall with a slightly different payload (150+ JWT claims, 180+ paths) is
  wasted requests and reads as flailing. Once a defense's shape is PROVEN, stop and report.
- This pairs with `ctf-methodology` (plan-then-execute, low-request-rate) and `hunt-ssrf`
  (reflected SSRF, decimal-IP loopback bypass, subnet-discovery).
- CONFIRMED WIN (CTF7 Blackglass): the breakthrough came from converging on the ONE unexplored
  port. After a full subnet scan, port 8081 returned `200` and was initially dismissed as "empty"
  — but reading its HOME PAGE revealed SENTINEL, an LLM-agent canary-exfil sub-challenge that held
  the flag. Lesson: **a 200 OK on a port is NEVER "empty"** — read the homepage and identify the
  service. A chat/assistant/SENTINEL UI is a live sub-challenge, not a decoy. The subnet-discovery
  step (Part C) must be followed by HOME-PAGE READING of every open port, not just a status check.
- Converge = pick the single most-likely vector, exhaust it surgically, report the proven wall, then
  move on. Multi-vector fan-out in one turn is the anti-pattern the user is correcting.

## Part B — profiling an internal `/read?path=` file service
When a reflected SSRF sink (webhook tester echoing `response_preview`) reaches an internal file
reader like `GET /read?path=<file>` and the flag is "in an env var", PROFILE the filter with a
FEW requests before spraying. The env is almost always at `/proc/self/environ`.

### Step 1 — baseline
Read `/etc/passwd`. Real contents ⇒ LFI works, filter is path-specific (not global). If even that
is blocked, the service uses a narrow allowlist — pivot elsewhere.

### Step 2 — profile the filter shape (read EXACT messages)
- `/proc/self/environ` → note msg (e.g. "Access to this file is restricted.")
- `proc/self/environ` (relative) → note msg (e.g. "Nice try. Reading the reader would make this
  far too easy."). A DIFFERENT msg than the absolute case proves two checks (absolute `/proc` +
  relative `proc/`).
- `/PROC/self/environ` → 404 (case-sensitive) ⇒ substring check, not prefix-only.
- `//proc/...`, `/proc/./self/environ`, `....//proc/...` → 403 ⇒ filter normalizes before checking.
- `%2Fproc%2Fself%2Fenviron` and `%252Fproc...` (double-encoded) → 403 ⇒ filter DECODES before
  checking ⇒ all encoding tricks are dead.

### Step 3 — infer the rule
Typical: `isfile(path)` FIRST (returns "Only regular files can be read" for `/dev/*`), THEN a
substring blocklist on `/proc`, `/root`, `/app`. ⇒ env is ONLY at `/proc/self/environ`; no
alternate path exists; the wall is by design.

### Step 4 — minimal exploit set (only AFTER profiling)
- `./proc/self/environ` — only if filter is absolute-`startswith` only (usually blocked).
- Symlink candidates at ALLOWED paths (`/tmp/*`, `/run/*`, `/dev/shm/*`) — only if container is
  known to symlink env there (else 404; don't spray).
- Custom headers (`X-File`, `X-Path`) — only if endpoint errors "Usage: GET /read?path=" for
  headers (proves it reads only the query param).
- Flag-file locations NOT under blocked prefixes (`/flag`, `/var/flag`, `/opt/flag`) — only if the
  challenge may have written env to a file at startup.

### Step 5 — STOP and report
If the filter (a) decodes before checking, (b) blocks `/proc`/`root`/`app` as substrings, and
(c) env is only at `/proc/self/environ`, it is a DELIBERATE wall. The "Reading the reader would
make this far too easy" message IS the author telling you the simple read is blocked. Converge,
report the proven wall, redirect to the user. The filter differential takes ~8 requests, not 180.

## Part C — related SSRF pivots (from `hunt-ssrf`)
- Reflected sink echoes body ⇒ read internal HTML/JSON directly, no OOB listener needed.
- Decimal/hex/octal IP encoding (`2130706433` = 127.0.0.1, `2886795265` = 172.1.16.1 gateway)
  defeats literal-string loopback filters; IPv6/`@`/domain tricks get caught.
- `502 Connection refused` on loopback ≠ service down; try the sink's PUBLIC IP (container isolation).
- Internal-portal cookie wall: reflected tester returns body only, no Set-Cookie ⇒ can't persist
  session; probe `/register`, `/api/me`, robots.txt, or pivot to a different internal service.
- Subnet-discovery: SSRF-portscan the gateway across curated ports; each open port may be its own
  challenge link in the chain. **After finding an open port, READ ITS HOME PAGE** — a 200 OK is
  never "empty". A chat/assistant/SENTINEL UI is a live sub-challenge. (CTF7 Blackglass: 8081 was
  found open but dismissed as empty until its homepage exposed SENTINEL, the canary-exfil flag
  host — see references/sentinel-llm-canary-exfil.md.)
- Flaky infra: CTF7 hosts drop connections ("000", empty body) intermittently. Don't conclude a
  service is dead from one 000 — retry 2-3x, and run a background watcher loop that auto-fires the
  probe when the host returns 200 (see references/sentinel-llm-canary-exfil.md for the pattern).

## Pitfall to avoid (observed this session)
Spraying 180+ path variants + 190+ JWT claim/kid combos + parallel port scans across 5 services in
one session is scattering. Profile first (Part B, ~8 requests), converge (Part A), report. The
user's "do one thing" is the signal to STOP multi-vector fan-out.

## References
- `references/sentinel-llm-canary-exfil.md` — full SENTINEL LLM-agent canary-exfil walkthrough:
  client event-map mechanics, the operator-unlock + macro→resolver side channel, capture caveats
  (in-response-JSON vs real egress), and the flaky-infra background-watcher pattern.
