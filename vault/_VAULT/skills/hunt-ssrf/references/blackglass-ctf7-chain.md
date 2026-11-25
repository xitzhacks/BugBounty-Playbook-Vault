# Blackglass CTF7 — worked SSRF/LFI/JWT chain (references for hunt-ssrf)

CTF7 challenge "Blackglass" (author Tanmay M, 600pt WEB, flag format `BI{...}`). A multi-service
Docker box; one service (the "partner platform", a webhook integration tester) is the SSRF sink that
reaches the others. Confirmed mechanics worth reusing:

## The SSRF sink (reflected webhook tester)
- App at `http://2.29.10.21:8082/` (Flask). Only two endpoints in `app.js`:
  - `POST /api/auth/login`  body `{"username","password"}` → `{"token":"<JWT>"}`
  - `POST /api/integrations/webhook/test`  headers `Authorization: Bearer <JWT>`, body
    `{"url","method","headers":{},"body":""}` → echoes `{"status":<code>, "response_preview":"<body>"}`
- The tester fetches `url` server-side and returns the BODY → **read SSRF, no OOB listener needed**.
- Login creds that worked: `settlement_ops` / `Asterveil#2026` (gives a JWT for the tester).
- Filter is a **literal hostname blocklist** ("Private and loopback ... not permitted"). Bypass with
  **decimal/hex IP encoding** of the target. Docker gateway `172.1.16.1` = decimal `2886795265`.
  `127.0.0.1` = `2130706433`. Loopback (`2130706433`) often 502-refused (separate container); the
  gateway IP (`2886795265`) reaches the colocated services.
- **Worker has NO egress to public IP** — netcat/callback listeners are unreachable. SSRF is internal-only.

## Internal services discovered (all on 172.1.16.1 / gateway 2886795265)
- `:5004` "path-tricks" — GET `/read?path=<file>` file reader. Says flag is in an env var.
- `:8080` "Corvid Capital BrokerLink" (Flask/Werkzeug) — `/api/v2/login`, `/api/v2/internal/documents/review`.
- `:8083` LedgerLock, `:8084` Asterveil (Express), `:8085` Aetheria — partner portals (cookie wall).
- `:3000`/:5000/:8000 are OTHER CTF7 challenges (TechCon / MAC-length-extension / Helios), not Blackglass.

## Flask LFI filter on 5004 (path-tricks) — characterization
- Logic: `if not os.path.isfile(path): return "Only regular files can be read."` THEN
  `if '/proc' in path or '/root' in path or '/app' in path: return 403` (filter DECODES the path
  before the substring check, so URL-encoding/double-encoding does NOT bypass it).
- `/etc/passwd` readable → LFI works; filter is path-specific.
- `/proc/self/environ` (the flag's location) is UNREACHABLE: every variant 403/404 —
  `/proc/self/environ`, `//proc`, `./proc`, `....//proc`, encoded/double/triple, `..` traversal,
  path-based `/read/<file>`, custom headers, `/tmp//dev/shm//run` symlink candidates, flag-file
  locations, source files (`/main.py` etc). Server message: "Nice try. Reading the reader would make
  this far too easy." → the env read is intentionally locked; the intended trick was NOT found.
- Lesson: when a Flask LFI does `isfile()` then a substring blocklist on `/proc`/`root`/`app` AND
  decodes before checking, the env (`/proc/self/environ`) is effectively unreachable by path tricks.
  Confirm the `isfile`-first behavior ("Only regular files can be read" for /dev) to know the filter shape.

## BrokerLink JWT (alg:none honored, role unforgeable)
- `/api/v2/internal/documents/review` requires `Authorization: Bearer <JWT>` + header
  `X-Corvid-Channel: broker`. Returns `{"error":"reviewer role required"}` for everything else
  (`channel header required` without the channel header).
- **Verifier does NOT verify the signature**: an HS256 token signed with a WRONG secret returns the SAME
  `reviewer role required` (not "invalid token"). So the role claim is read from the (unverified) payload.
- Legacy `kid: brokerlink-2019` tokens are "still honored" (source map `legacy-broker.9f14.js.map`):
  `POST /documents/review` with `X-Corvid-Channel: broker`. The review console is "unavailable on this
  node" (per console.5d3b.js) — flag is served by the internal review pipeline.
- Despite unverified signature, the **reviewer role is server-side / unforgeable**: ~200 token combos
  failed (alg:none, HS256, empty-secret, every role claim name/value — flat, nested, header, body,
  URI-namespaced, list/obj/bool, every kid, every channel except "broker", internal XFF headers,
  no-token, sub-as-reviewer, plausible 2019-key guesses). The role is NOT a forgeable claim.
- `/api/v2/login` → `401 {"error":"invalid"}` for all guessed creds, NoSQL injection, JWT-as-password,
  OAuth shapes. `/admin` → 403 GET / 405 POST (real route, access-controlled). No other endpoint (404).
- Lesson: a "signature not enforced" JWT is NOT automatically exploitable — if the required role/identity
  is resolved server-side (DB/user-record/kid→key mapping) rather than from the token claim, forging the
  token still fails. Confirm by testing a wrong-secret signature: same error as valid = unverified, but
  the gate may still read an unforgeable source.

## Anti-patterns to avoid (this user)
- Scattering: this user says "do one thing" / "continue" repeatedly when the agent fans out across
  services. Commit to ONE service/endpoint per turn; see ctf-methodology "CONVERGE ON ONE VECTOR".
- Full /24 or 1–10000 port scans in foreground time out (exit 124). Use a CURATED port list, or run in
  background with `notify_on_complete`. Decimal-encode the gateway and scan `:port/` per port.
- Don't re-run the login fetch inside every script — login ONCE, reuse the JWT (it's stable for the session).
