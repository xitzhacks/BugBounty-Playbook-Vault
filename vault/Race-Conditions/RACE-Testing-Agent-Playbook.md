# RACE — Testing Agent Playbook (Race Conditions / TOCTOU)

*Evidence base: 26 disclosed h1-brain corpus cases (`RACE-…`). Every quoted sentence is byte-true to `references/archive/race-bodies-full-dump.txt`. Read the class modules before improvising; this file is the operational spine.*

## 0. When to load this playbook

Any endpoint whose effect the user can trigger **multiple times while paying for it once** (or once while paying for it many times), or any **validate-then-act** sequence observable in two dependent requests. Trigger phrases from this corpus: redeem, claim, invite, join, verify purchase, confirm email, retest, accept promo, faucet, followers, credential, reset.

## 1. Entry-point mapping (what to probe, mapped from corpus)

| Endpoint shape | Why it races | Corpus proof |
|---|---|---|
| Purchase verify / payment callback (`verify_purchase`, retest confirm) | Money state written per request, transaction check lags ledger write | RACE-801743 (10 parallel → 9 through), RACE-429026 ($500 ×N) |
| Promo / coupon / redemption-limit endpoints | "limit" enforced as read-check then increment | RACE-1717650 (limit 1 redeemed 2×, **by tab racing**) |
| Email confirm + email change | Two-side validation without a DB transaction | RACE-300305 (**$15,250**, ATO chain) |
| Grant/token exchange (`/oauth/token`) | Code/refresh liveness checked then consumed | RACE-55140 (11 targets, 6 vulnerable) |
| Password reset (two endpoints) | Token invalidation scoped per-endpoint only | RACE-772886 |
| Join / claim / invite / flag submit | INSERT without UNIQUE or with check-then-insert | RACE-604534, RACE-1540969, RACE-488985, RACE-1460373, RACE-454949 |
| Faucets / credit-issuing with cap | Cap read from a shared, unsynchronized map | RACE-1438052 (50 concurrent → 30/11 tokens) |
| Non-consumable upvote/like counters | Counter update not atomic vs. spam filters | RACE-1566017 ($250) |
| SSRF filters & URL blocklists (server) | DNS resolved once for check, once for use | RACE-541169, RACE-859962 |
| Content-type gates (server) | HEAD-check, GET-use | RACE-2106708 |
| Local: config validate → privileged exec; `stat` → `fopen` | File swapped between check and use | RACE-768110, RACE-2078571, RACE-2905013 |

## 2. Tool ladder (manual → engineered, all evidenced in corpus)

1. **curl `&` chains** — the zero-tooling baseline two corpus reports used verbatim:
   RACE-429026: `3. Execute the request on the command line in the form \`(request) & (request) & ...\`. In testing, I executed the command 5 times.` and RACE-1460373 chains 10 curls: `This is a chain of 10 curl commands in the form of \`curl_command_1 & curl_command_2 & ... & curl_command_10\`.`
   > Beats nothing but noise; window must be ≥~100 ms. 10–20 parallel curls, then check state.
2. **Multi-tab manual racing** — for wide (human-speed) windows, no proxy needed:
   RACE-1717650: `4.Hit both link's pay/subscribe button as fast as you can.` → `5. Both payment will be successful using one coupon two times.` and RACE-300305 exploits a `1,100 - 2,500 ms` gap across two tabs.
3. **Burp Intruder parallel / "Race The Web"** — legacy mid-tier; RACE-488985 ran 22 Intruder requests (`I then sent this request to burp suite intruder and got 22 responses , 21 of them had the same response as this`); RACE-454949 argues `Race The Web` beats Intruder: `With this tool we can send the requests faster than we could with Burp Intruder. Getting better results.`
4. **Turbo Intruder single-connection gate** — current standard captured inside RACE-1540969's script:
   ```
   engine = RequestEngine(endpoint=target.endpoint,
                          concurrentConnections=100,
                          requestsPerConnection=100,
                          pipeline=True)
   for i in range(30):
       engine.queue(target.req, gate='race1')
   engine.openGate('race1')
   ```
   RACE-1037430 used the stock race.py example against Badoo's promo endpoint.
5. **Filesystem/DNS sync primitives** for server-side TOCTOU: `renameat2(RENAME_EXCHANGE)` swap loop (RACE-2078571), NTFS opportunistic locks via BaitAndSwitch (RACE-768110), zero-TTL alternating DNS (RACE-541169: `resolve a domain to alternating addresses with a low (or zero) Time To Live`).

Pick rung 1 first — it also proves the window is wide enough for the rungs above to matter.

## 3. Root-cause evidence to collect (turns "same response" into a report)

- **Missing DB transaction / non-atomic check-then-act** — RACE-300305 names it: `eventually your email will be changed and be validated due to not (properly) using a DB transaction`.
- **Unsafe language structures** — RACE-1438052: `We believe the root cause of the issues is the go mapping which is not advised for concurrency`.
- **Unfenced shared state** — RACE-1990421: `libcurl used a global buffer that was not mutex protected and a multi-threaded application might therefore crash`.
- **Endpoint-duplicated logic** — RACE-772886: two reset endpoints with independent token stores.
- Screenshot the minted surplus: balance (RACE-1438052 `it is 30 which should have not been more than 11`), premium days (RACE-1037430 `9 days from today`), payment line-item (RACE-429026 `a $500 payment was sent from HackerOne 2 weeks ago`).

## 4. Validation gates (must pass before writing anything)

1. **Serial control fails, parallel succeeds.** Send the same request twice sequentially: must be rejected/absorbed. If serial ALSO succeeds, you have insufficient-program-state, not a race — file under Business-Logic instead.
2. **Effect demonstrated on the account, not just in traffic.** N× credits, double payment, member list with duplicates, days extended — a screenshot with the delta.
3. **At least one full beat of the tool ladder executed** (state which rung). Probabilistic windows: RACE-55140 warns `Race Condition is probabilistic vulnerability. It may be needed to do few attempts with PoC to reproduce it.` — disclose attempt count.
4. **Blast radius stated honestly.** RACE-604534 self-rates Low (`Ofcourse this is a low severity` (sic)) and still ships; don't inflate to pay for the run.
5. **Identity cleanup / self-rules compliance** — new test account where platform requires it (RACE-454949 created one and offered the email back).

## 5. Chains that pay (race as the multiplier, not the payload)

- **Email-validate race → partner/employee ATO → store takeover** (RACE-300305, $15,250): the race only mints a `confirmed` flag on an attacker-controlled email; the takeover comes from Shopify's collaborator-conversion trust in validated emails.
- **Path traversal write + repository-server race → arbitrary file read** (RACE-822262, $12,000): `By combining the bug with a race condition in Gitaly which I used several times before (#762421, #732330). It could finally be used to read sensitive files in a GitLab instance.`
- **DNS TOCTOU → full SSRF → cloud metadata** (RACE-541169): `send GET and POST HTTP requests to arbitrary hosts, including the localhost, cloud metadata services and the local network, and read the HTTP response.`
- **HEAD/GET TOCTOU → re-open a patched RXSS** (RACE-2106708): a bypass bug whose value equals the original XSS finding.
- **Config-swap TOCTOU → SYSTEM** (RACE-768110) and **write-servlet race → RCE** (RACE-2905013): local primitives, catastrophic receivers.

## 6. Report skeleton (mirroring corpus style)

```
Summary: <what races, what mints/stays>
Steps To Reproduce:
  1..N with exact request (method, path, headers, body) and the tool rung
  4. parallel count and hits-out-of-N ("I did 10 parallel requests and got 9 of them through")
Impact: <state delta with proof artifact; business cost>
Similar Reports: <corpus siblings, e.g. RACE-604534 ↔ RACE-1540969>
```

Historical labels observed for the same class: `TOCTOU Race Condition`, `Concurrent Execution using Shared Resource with Improper Synchronization ('Race Condition')`, `SSRF`, `Code Injection`, `XSS - Reflected`, `Improper Authentication`, `Improper Access Control`, or None. Match the platform's VRT, not the corpus label.

## 7. Negative controls / always-reject list

- Rate-limit flakiness, 200-empty responses, or duplicated mail *without state delta* — not a finding.
- Same-flag submission that doubles *leaderboard display only* with server count consistent — timing display bug.
- Brute-forcing a code (searchable, not time-window) — Rate-Limiting class, not race.
- Non-constant-time comparisons mined *purely* for user enumeration — choose Rate-Limiting/Enumeration cadence; timing claims belong in Library-Timing-Adjacent with response-delta statistics.
