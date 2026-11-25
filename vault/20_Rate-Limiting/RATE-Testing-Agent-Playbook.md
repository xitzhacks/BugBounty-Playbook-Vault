---
title: "Rate Limiting Testing Agent Playbook — the executable protocol"
type: agent-playbook
category: rate-limiting
cwe: "CWE-307, CWE-799, CWE-204"
built: "2026-11-07"
corpus: "64 rows (58 bucket + 6 merges), all full-body (h1-brain disclosed_reports.db)"
bounty: "$19,105/28 paid · 01 $1,740/5 · 02 $1,050/5 · 03 $4,770/5 · 04 $11,545/13"
companion_modules: "01 otp-2fa-reset-token · 02 login-password-gates · 03 throttle-bypass-vectors · 04 adjacent-and-unclassified"
quote_rule: "byte-true to RATE-bodies-full-dump.txt"
---

# RATE Testing Agent Playbook

## P0 — Scope & load discipline

1. Rate-limit testing means generating requests. Check the program's rules for automated testing
   volume **before** the first burst; keep a written cap (e.g. 200 requests, 5 req/s) and stop when
   a threshold is found.
2. Never aim at production login systems of unrelated users. Use your own accounts and, where
   possible, your own tenant.
3. Decide the class you are claiming: **missing limit**, **bypassable limit**, **lockout DoS**, or
   **enumeration**.

## P1 — Threshold bisect

1. Pick the credential check (login, OTP verify, reset-token consume, current-password prompt,
   room password, invite code).
2. Send wrong credentials at a fixed rate; record the attempt number where the response changes
   (`429`, a "too many attempts" body, or a lockout message).
3. State the threshold precisely: "blocked at attempt 121" beats "no rate limit".

## P2 — Identify the counter key

Vary one input at a time and re-run the bisect:

| Variation | If the counter resets | Evidence |
|---|---|---|
| `X-Forwarded-For` / `Forwarded` / `X-Real-IP` | counter keys on a client header | RATE-225897, RATE-2627062 |
| Source IP (second connection from another host) | counter keys on IP | RATE-819930 |
| IPv6 address inside the same /64 or /48 | counter keys on /128 | RATE-1154003 |
| Host/path case, trailing slash, HTTP version | counter scoped per route | (test) |
| Mobile/GraphQL/legacy endpoint | counter scoped per surface | RATE-165727, RATE-1363672 |
| After a successful auth | counter cleared by success | RATE-1065186 |

## P3 — Proof ladder

1. **Missing counter** — sustained guesses with no block (RATE-385381: "1k+ request but still server
   not block").
2. **Bypass of an existing counter** — block, then unblock by varying one input (RATE-1363672:
   $3,500).
3. **Success** — a real credential/code accepted after the limit (RATE-1065186).
4. **Impact** — ATO, account lockout of another user (RATE-1406495), or data enumeration.

## P4 — Modern hardening fingerprints

- Account+device keyed counters with exponential backoff (not IP-only).
- OTP: per-code attempt counters, code invalidation on N failures, and short TTLs.
- Re-auth prompts on destructive actions are now commonly throttled — verify, do not assume.
- Proxy headers: `REMOTE_ADDR` from a trusted-proxy list only; IPv6 blocking at /64 or wider.
- Enumeration: uniform responses and timing, plus per-identifier throttles.

## P5 — Kill-gates

1. **One 429 without a bypass attempt** → not a finding.
2. **No credential check behind the endpoint** → nothing to brute force.
3. **Enumeration without a distinct oracle** → not a finding.
4. **Load beyond program rules** → stop; the finding is worthless if the report is rejected for
   testing violations.
5. **Lockout DoS** → confirm it hits a *different* account and state the duration; that is what paid
   $900 here.

## Module ↔ phase table

| Phase | Modules | Paid pattern |
|---|---|---|
| P1 bisect | 01, 02 | threshold or its absence |
| P2 key id | 03 | header/IP/subnet/per-surface reset |
| P3 proof | 01, 03 | success or lockout |
| P4 hardening | 01, 03 | account-keyed counters, OTP TTL |
| P5 gates | 04 | noise separation |

## Non-goals

- Credential-stuffing research against real users.
- "No CAPTCHA" as a standalone finding.
- Brute force without a success or a takeover chain — the corpus pays chains.
