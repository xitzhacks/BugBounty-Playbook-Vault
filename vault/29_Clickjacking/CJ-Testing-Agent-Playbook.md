---
title: "Clickjacking Testing Agent Playbook — the executable protocol"
type: agent-playbook
category: clickjacking
cwe: "CWE-1021"
built: "2026-11-07"
corpus: "23 rows, all full-body (h1-brain disclosed_reports.db)"
bounty: "$8,460/6 paid · 01 $1,960/4 · 02 $3,500/1 · 03 $3,000/1"
companion_modules: "01 x-frame-options-and-csp · 02 markup-rtlo-ui-redress · 03 clickjacking-enable-chains"
quote_rule: "byte-true to CJ-bodies-full-dump.txt"
---

# CJ Testing Agent Playbook

## P0 — Is it worth testing?

1. Clickjacking is usually triaged Informational/Low unless a **state-changing, authenticated
   action** sits behind the frameable page. Check the program's VRT before spending time.
2. Build the list of *sensitive* pages first: password change, email change, API key
   create/delete, payout settings, admin approval, OAuth consent, delete-account.
3. Discard marketing pages — the corpus's unpaid rows are almost all of that kind.

## P1 — Header audit

1. `curl -sI` each sensitive URL and record `X-Frame-Options` and
   `Content-Security-Policy: frame-ancestors`.
2. Flag: **(a)** header absent, **(b)** `ALLOW-FROM …` (unsupported in Chrome/Safari — CJ-198622,
   CJ-591432), **(c)** `SAMEORIGIN` only on the root while sub-flows lack it (CJ-214087),
   **(d)** CSP present but a subdomain lacks it.
3. Check redirects and POST-consent pages separately — CSRF-style flows often drop headers.

## P2 — Prove the frame

1. Minimal PoC:

```html
<iframe src="https://target/sensitive-action" frameborder="0"></iframe>
```

2. Escalate to the "clickjacking with a decoy" form: an opaque overlay plus the framed action
   positioned under the cursor.
3. Record browser + version. `ALLOW-FROM` rows are only valid in browsers that honor it.

## P3 — Impact framing (what actually pays)

| Framing | Corpus evidence |
|---|---|
| Fake login inside the real origin | CJ-2119892 ($200) |
| Email/credential capture via framed card | CJ-154963 |
| Reservation/payment action behind the click | CJ-355859 |
| Full-page click interception via injected CSS classes | CJ-662287 ($3,500) |
| Self-XSS made triggerable | CJ-892289, CJ-953579 |
| Enablement of a tool compromise | CJ-1274695 ($3,000) |

State the action, the victim type (logged-in user / admin), and whether CSRF tokens are bypassed
by the click.

## P4 — Modern hardening fingerprints

- `Content-Security-Policy: frame-ancestors 'self'` is the current control; `X-Frame-Options` is
  legacy and `ALLOW-FROM` is dead in Chromium.
- Framing protections on the *document* are bypassed by same-site framing, so check subdomain
  takeovers/overlays too.
- Sanitizers now strip `class`/`style` on user markup — the CJ-662287 primitive is worth retesting
  on any wiki/README renderer.
- Tools that embed browsers (scanners, kiosks, Electron apps) are a growing target class.

## P5 — Kill-gates

1. **No sensitive action** → informational; do not submit unless policy prices header gaps.
2. **Frame blocked by CSP** → stop.
3. **Duplicate host** — check the program's disclosed list first (the corpus has several yelp/semrush
   duplicates).
4. **Browser-only claim without a browser** → not a finding.
5. **Do not use real users' sessions** — self-account PoCs only.

## Module ↔ phase table

| Phase | Modules | Paid pattern |
|---|---|---|
| P1 headers | 01 | missing/unsupported directive |
| P2 proof | 01, 02 | frame or injected overlay |
| P3 impact | 02, 03 | fake login / ATO / RCE |
| P4 hardening | 01, 02 | CSP, sanitizer class stripping |
| P5 gates | all | sensitive action or chain |

## Non-goals

- Reporting every frameable URL on a domain.
- Pure RTLO filename tricks without a download/payment consequence.
- Clickjacking against third-party embeds the target does not control.
