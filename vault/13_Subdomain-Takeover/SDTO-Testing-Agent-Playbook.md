---
title: "Subdomain Takeover Testing Agent Playbook — the executable protocol"
type: agent-playbook
category: subdomain-takeover
cwe: "CWE-16, CWE-350"
built: "2026-11-07"
corpus: "26 rows (24 bucket + 2 merges), all full-body (h1-brain disclosed_reports.db)"
bounty: "$4,565/10 paid · 01 $2,150/4 · 02 $900/3 · 03 $250/1 · 04 $1,265/2"
companion_modules: "01 cloud-cdn-paas-cname · 02 saas-hosted-service-claim · 03 dns-delegation-github-tld · 04 adjacent-unclassified"
quote_rule: "byte-true to SDTO-bodies-full-dump.txt"
---

# SDTO Testing Agent Playbook

## P0 — Scope & ethics

1. Takeover testing is **claim testing**, not infrastructure acquisition. The corpus's proofs end
   at a harmless proof-of-control page; stop there.
2. Confirm the program's policy covers DNS assets. Many programs exclude "subdomain takeover of
   non-production assets" and pay only when session/cookies are reachable.

## P1 — Enumeration

1. Build the subdomain list (`crt.sh`, passive DNS, certificate transparency, wordlists).
2. Resolve CNAMEs specifically — the dangling record is nearly always a CNAME:
   `dig +short CNAME sub.example.com`, then compare against provider ranges.
3. High-yield provider fingerprints in this corpus: S3, CloudFront, Heroku, Statuspage, HubSpot,
   Ghost, Azure, Uberflip, Fastly, GitHub Pages, plus `r2.dev` custom domains.

## P2 — Fingerprint the failure mode

| Signal | Meaning | Evidence |
|---|---|---|
| `NoSuchBucket` / `The specified bucket does not exist` | S3 name claimable | module 01 |
| CloudFront `Bad request`/`ERROR: The request could not be satisfied` with no distribution | origin gone | module 01 |
| `No such app` / Heroku 404 boilerplate | app deleted | module 01 |
| Provider "not found" page for the exact host (`Statuspage`, `Ghost`, `HubSpot`) | name free to claim | module 02 |
| `NXDOMAIN` on a delegated NS zone | zone takeover | module 03 |
| `github.io` 404 with the repo unregistered | GitHub Pages claim | module 03 |

## P3 — Claim & prove

1. Register only the minimal resource (bucket name / app name / page) that satisfies the
   provider's ownership check.
2. Serve a **static proof-of-control** page — no collection, no JS that reads cookies.
3. Capture the before/after: the host now returns attacker-controlled content over the victim
   domain.
4. Record the DNS record verbatim (`dig` output) — that is the root cause artifact.

## P4 — Escalate to what pays

The corpus pays chains, not takeovers:

- **Cookie scope** — if the parent domain sets cookies without `__Host-`/`Domain` scoping, the
  claimed host can read or overwrite them (module 02's Uber/Ubiquiti chain rows).
- **OAuth redirects** — a whitelisted subdomain that you now control is a redirect sink.
- **CORS** — `Access-Control-Allow-Origin` trusting `*.victim.com`.
- **Email** — SPF/DKIM alignment from a claimed host can reach phish-grade trust.

## P5 — Kill-gates

1. **Provider blocks the claim** (name reserved, ownership TXT required) → not a finding; record
   and move on.
2. **Host serves only a generic 404** with no provider fingerprint → likely still owned; verify
   with multiple resolvers before reporting.
3. **No victim** — if nothing but a blank page can be served, triage will be Low; say so honestly
   (several corpus rows self-rate Low and still ship).
4. **Out-of-scope asset** — DNS entries for staging/internal hosts are frequently excluded.
5. **Never leave the claim in place** — release it after the proof and note the release in the report.

## Module ↔ phase table

| Phase | Modules | Paid pattern |
|---|---|---|
| P1 enumeration | 01, 02, 03 | CNAME/NS inventory |
| P2 fingerprint | 01, 02, 03 | provider 404 strings |
| P3 claim/proof | 01, 02, 03 | proof-of-control page |
| P4 escalation | 02, 04 | cookies, OAuth, CORS |
| P5 gates | all | claimability + victim path |

## Non-goals

- Mass claiming of third-party DNS without authorization.
- Serving content that interacts with real users' sessions — proof pages stay static.
- Assuming a takeover is paid: the corpus's paid band for plain takeover is $100–$1,000.
