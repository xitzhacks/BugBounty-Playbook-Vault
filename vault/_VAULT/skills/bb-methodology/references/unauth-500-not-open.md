# False-Positive Guard: unauthenticated 500 != open endpoint

Technique surfaced 2026-07-28 testing Ather Energy (Next.js). A recurring false positive
in API/auth-bypass hunting: hitting an /api/* endpoint with NO session returns HTTP 500
(generic framework error page), and the hunter reads it as "the endpoint is open /
unauthenticated". It usually is NOT.

## Why the 500 happens
Many SPA/Next.js apps use a centralized API client (axios/fetch wrapper) configured with
`withCredentials: "same-origin"` (or `credentials: "include"`). The /api/* route handler
dereferences `req.session.user` / the verified token at the top. When you call it with no
session cookie, the handler throws inside that dereference -> uncaught exception -> 500.
The 500 is a *missing-session crash*, not evidence the endpoint is reachable without auth.

## How to tell the difference (do NOT guess)
1. Grep the downloaded JS bundles for the API-client constructor. Search for
   `withCredentials`, `credentials:`, `baseURL`, `Authorization`, `Cookie`. If the client
   sends credentials by default, unauthenticated calls are expected to 401/500.
2. Look for a centralized wrapper (e.g. `NEXT_SERVER_API.post(...)`) — if every endpoint
   goes through it and it attaches the session, the auth is at the client boundary.
3. Confirm with a session: replay the SAME request WITH a valid session cookie. If it now
   returns 200 + real data (or a proper 400 for bad input), the endpoint was gated all
   along — the earlier 500 was the missing-session crash.

## Contrast: what an actually-open endpoint looks like
- 200 with data even with no session, OR
- 401/403 with a clean "unauthorized" JSON (handler rejected you at the auth check),
  NOT a 500 stack-trace page.
A 500 error HTML page is the signature of "reached code, lacked context to proceed."

## Cross-check against discipline rules
This guard is consistent with the Body-Diff Rule and OOB Gate in bb-methodology: a 500
status alone is never a finding. Always determine whether the 500 is an auth crash (needs
session to confirm) vs. an exposed handler (returns data). When in doubt, obtain a session
and re-test — do not report reachability as an auth-bypass.
