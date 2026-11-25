---
title: "CSRF Testing Agent Playbook — the executable protocol"
type: agent-playbook
category: csrf-all
cwe: "CWE-352"
built: "2026-10-28"
corpus: "229 mirror rows → 178 bodies read (136 resolved / 33 informative / 7 not-applicable / 2 duplicate) · 51×404 recorded"
bounty: "$36,504 CSRF-class (JSON-verified $8,330/18 rows · list-stated $21,824/51 fetched rows · dead-404 $6,400/20 rows) · $1,650 SSRF/SQLi noise excluded"
companion_modules: "01 login/signup/logout · 02 oauth-state · 03 ATO-chains · 04 token-design · 05 validation-gaps · 06 GET-lane · 07 chains-commerce"
quote_rule: "byte-true, (sic)-marked, from read bodies only; 404 rows recorded never quoted"
---

# CSRF Testing Agent Playbook

Executable protocol derived from 178 read bodies (2014–2017 era) + modern discipline from the
hunt-csrf skill. Every step cites its corpus evidence. Run phases in order; abort at kill-gates.

## P0 — Carrier & token inventory (always first)

1. **Map the auth surface**: login, signup, logout, confirm/verify, password/email change,
   connected accounts, 2FA enroll, account delete, roles/providers/delegates, integration
   install/uninstall. Corpus evidence: the IRCCloud cluster found *six* distinct un-tokened
   endpoints in one app (7531, 6910, 7051, 7332, 7516); Localize found eight (7870–8273).
2. **Fingerprint the framework token** (name = the stack):
   `csrfmiddlewaretoken` (Django), `authenticity_token` (Rails), `crumb` (Slack-era Jenkins/
   Slack), `csrftoken` cookie (Django/mobilevikings), `X-CSRF-Token` header (H1-era Ember),
   `X-XSRF-TOKEN`/`_token` (Laravel), `__RequestVerificationToken` (ASP.NET). Note where it
   appears: form field, header, cookie, meta tag, JS bundle, 404 pages (136481), redirect
   URLs (196458).
3. **Record per-endpoint token presence** in a table before any probe. Evidence: 195156's
   finding is *conditional* (HTTP-auth sessions only) — inventory would have missed it without
   the auth-mode column.

## P1 — Cheapest-first probes (seconds each, corpus-ordered)

| # | Probe | Cost | Corpus proof |
|---|---|---|---|
| 1 | Remove token field → replay | ~5s | 99647/99857 (onpatient), 2635/2638 (Slack), 15454 |
| 2 | Token `=""` → replay | ~5s | Localize ×8 blank `CSRFToken` |
| 3 | Token `null`/`0`/arbitrary string → replay | ~5s | 208734 (BrickFTP null), 143321 (any value) |
| 4 | Remove Referer → replay; blank-referer iframe → replay | ~10s | 52635 (UniFi full 401→200) |
| 5 | GET-mutation inventory + `<img>` fire | ~10s | 5946, 111216, 174328, 226418 |
| 6 | Token `="0"` on PHP stacks (magic hash) | ~5s | 86022 (Phabricator `==`) |
| 7 | Path artifacts: drop extension, add slash, change case | ~10s | 95555 (Twitter cards `.json`) |

Any 200 + verified state change ⇒ a finding seed; classify by module table in P2.

## P2 — Lane decision tree (which module owns the finding)

```
Does the endpoint ESTABLISH a session (login/signup/confirm-link)?
 ├─ yes → 01_Login-Signup-Logout-CSRF.md
 │        └─ token-fetchable-anonymously? → 7531 sub-case (defeats "protection")
Does it CHANGE identity binding (OAuth connect/attach/authorize, 2FA, providers)?
 ├─ yes → 02_OAuth-State-and-Account-Association.md (authorize lane)
 │        or 03_Account-Takeover-Chains.md (providers/2FA/email lane)
 │        └─ chain to reset flow? → 03 §2 (email-change → reset → ATO)
Does the TOKEN itself leak/never-rotate/not-bind?
 ├─ yes → 04_Token-Design-Flaws.md (leakage / rotation / binding families)
Is the token PRESENT but strippable (P1 hits 1-4,6,7)?
 ├─ yes → 05_Validation-Gaps-and-Bypasses.md
Is the mutation reachable by GET (P1 hit 5)?
 ├─ yes → 06_GET-State-Changes.md (tier: exfil > security-state > export)
Is the write a CONTENT field the app renders, or a commerce/cart option?
 ├─ yes → 07_Chains-Commerce-Impact.md (XSS/SSRF/commerce chains)
```

## P3 — Escalation (only after a lane confirms)

1. **Settings → ATO** (module 03): email/identity change + reset/2FA flows — chain both,
   demonstrate login-as-victim from attacker browser.
2. **Read-the-token → forge** (module 04→05): leak (15412/196458/99708) then one forged
   state change with the stolen token.
3. **Write → stored XSS → privilege** (module 07): no-op probe first, one rendered payload,
   chain to admin/editor primitives named explicitly.
4. **GET → exfil door**: escalate the GET lane by finding push/export/escalate mutations
   (226418 standard).
5. **Impact-first pricing discipline** (corpus law): settings-only ≈ $100; binding/2FA ≈
   $500; demonstrated ATO ≈ $852–$2,500; chained-to-infrastructure ≈ highest. Never claim a
   tier you have not demonstrated (141344: CRITICAL claimed, $50 paid).

## P4 — Discipline gates

1. **Two-browser, two-account always** — victim B's authenticated UI shows the mutation;
   attacker A's browser shows the takeover/binding. Screenshots both.
2. **SameSite reality check (modern)** — era rows predate Lax defaults. Current-browser PoC:
   cross-site `<img>`/form POST are now cookie-blocked by default; document what still fires
   (top-level navigations, GET with same-site referrer chains, subdomain-in-cookie-scope
   cases, frame/embed contexts). An era-technique report that cannot fire today must say so.
3. **Strip, don't spoof** — referer/origin bypasses in this corpus are *absence* proofs
   (52635), not header-spoofing tricks.
4. **No-op probes before destructive ones** (125594 standard) — bogus ids, harmless actions,
   sacrificial accounts only.
5. **Era honesty** — GA `__utmz` injection (26647/14883) and Flash 307 (251918)/cross-site
   flashing (136481) lanes are era-techniques; fingerprint before claiming; cite the modern
   equivalents from blogs-index instead when the primitive is dead.
6. **State restore** (kill-gate K7) — revert every mutation; delete test accounts.
7. **404 discipline** — the 51 dead reports prove the pattern: record title + figure, quote
   nothing.

## P5 — Report assembly (corpus templates)

**Title**: `<Lane> CSRF on <endpoint> leading to <demonstrated impact>`
(corpus best: "CSRF in Connecting Pinterest Account" + step list; "Full account takeover using
CSRF and password reset").

**Body order** (from the paid bodies): summary with the *end-state* first → root cause
(the missing/failed validation, named parameter) → step list with request/response pairs →
impact as demonstrated actions (215381's endpoint list) → fix suggestion naming the primitive
(104931's "make use of the state parameter"; 101909's two-defense list).

**Impact-first pricing** (corpus law): demonstrated access > claimed severity. 141344 claims
CRITICAL, paid $50; 215381 enumerates granted endpoints, paid $2,520.

### Kill-gates (any ⇒ do not submit)

- K1: Only a missing token *field* observed, no validated state-change (6888-class noise).
- K2: The forged request fails in a current browser with no documented frame/navigation
  context that fires it (SameSite/COOP).
- K3: Signup-CSRF with no demonstrated forced creation.
- K4: Token-lifecycle findings without a demonstrated forge (46736-class informative).
- K5: Video-only PoCs (7436-class).
- K6: Claims resting on 404 rows or title-only metadata.
- K7: Any test state you cannot restore.
- K8: Impact argument that says "could potentially" — the report-writing rule: prove it or
  don't report.

## References

- Modules 01–07 in this directory (each carries the verbatim case evidence).
- [`references/source-index.md`](references/source-index.md) — provenance, funnel, era stats.
- [`references/case-register.md`](references/case-register.md) — 229-row disposition ledger.
- [`references/blogs-index.md`](references/blogs-index.md) — zseano guide (byte-quoted),
  writeup queue, modern citations.
- Skills: hunt-csrf (scenario matrix), hunt-ato, hunt-mfa-bypass, hunt-oauth, hunt-cache-poison.
