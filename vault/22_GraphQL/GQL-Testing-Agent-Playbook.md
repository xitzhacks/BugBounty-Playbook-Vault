---
title: "GraphQL Testing Agent Playbook — the executable protocol"
type: agent-playbook
category: graphql
cwe: "CWE-862, CWE-639, CWE-918"
built: "2026-11-07"
corpus: "19 rows (18 bucket + 1 merge), all full-body (h1-brain disclosed_reports.db)"
bounty: "$58,340/13 paid · 01 $27,870/5 · 02 $19,500/3 · 03 $8,470/4 · merge $2,500/1"
companion_modules: "01 authorization-and-session · 02 idor-mutations-and-type-confusion · 03 injection-ssrf-csrf-xss-dos"
quote_rule: "byte-true to GQL-bodies-full-dump.txt"
---

# GQL Testing Agent Playbook

## P0 — Preconditions

1. Find the endpoint (`/graphql`, `/api/graphql`, `/admin/api/graphql`, vendor paths like
   `/federal/graphql`). GQL-2048725 shows two instances sharing one domain.
2. Check policy: GraphQL is usually in scope as an API asset; *introspection* may be excluded as a
   finding by itself.
3. Record whether introspection is enabled, batched queries are accepted, and GET is allowed.

## P1 — Schema discovery (even with introspection off)

1. Introspection query → full type list, mutations, and field-level arguments.
2. If introspection is disabled: error-message field guessing (`Cannot query field "x"`),
   client bundle mining (the SPA ships its operations), and known Relay patterns.
3. Enumerate **mutations** first — the corpus's biggest payouts are write-side
   (GQL-2122671 $12,500, GQL-2207248 $5,000, GQL-981472 $2,000).

## P2 — Authorization mirror (the core probe)

For every rule the product enforces elsewhere, ask the resolver:

| Product rule | GraphQL probe | Evidence |
|---|---|---|
| Session revoked | replay a captured query with the dead token | GQL-417382 |
| Account disabled/deactivated | same, after disabling | GQL-608656, GQL-1192460 |
| Staff lacks permission | query the gated object as that staff account | GQL-528940 |
| Program is private | `team(handle:){_id,industry}`, `node(id:)` | GQL-707406, GQL-1618347 |
| REST 404s the object | query the same id through `namespace`/`node` | GQL-614355 |
| Object belongs to another tenant | swap `id` in the mutation variables | GQL-2122671, GQL-2207248 |

**`node(id:)` first.** GQL-1618347 is two lines and paid $25,000 — test every Relay ID you can
obtain against the global node resolver with an inline fragment for the target type.

## P3 — Sink testing

1. **GET accepted?** → CSRF (GQL-1122408). Build the auto-submitting form with the mutation in
   `query`.
2. **URL/argument fields?** → SSRF (GQL-1864188): set the field to a collaborator URL.
3. **HTML-bearing fields?** → stored XSS on the rendering surface (GQL-1085546).
4. **Deep/circular queries?** → DoS only with a measured impact (GQL-2048725); prefer proving
   cost/limits over taking the API down.

## P4 — Modern hardening fingerprints

- Persisted queries / allowlisting breaks ad-hoc introspection but not the operations the client
  ships — mine the bundle.
- Depth/complexity limits and query-cost analysis block circular introspection; batching limits
  block amplification.
- CSRF: many frameworks now reject GET for mutations and require `Content-Type: application/json`.
- Field-level authorization frameworks (e.g. policy-per-field) close the `node()` gap — verify
  per type rather than assuming the endpoint is uniformly protected.

## P5 — Kill-gates

1. **No object you should not see** → schema/enumeration notes are not findings.
2. **Introspection-only** → informational unless policy says otherwise.
3. **Self-tenant mutation** → feature, not bug.
4. **DoS without a measured cost/availability delta** → informational.
5. **Duplicate check**: the corpus's own rows are frequently marked "similar to #…" — search the
   program's disclosed reports before submitting.

## Module ↔ phase table

| Phase | Modules | Paid pattern |
|---|---|---|
| P1 discovery | 01, 02 | mutations and node IDs |
| P2 authz mirror | 01, 02 | rule enforced elsewhere, missing here |
| P3 sinks | 03 | GET→CSRF, URL→SSRF, HTML→XSS |
| P4 hardening | all | persisted queries, depth limits |
| P5 gates | 02, 03 | concrete object, concrete impact |

## Non-goals

- Generic introspection-report submissions.
- Query-complexity research without a target-specific impact.
- Brute-forcing ID spaces at scale (GQL-885539 did it, and it took hours) unless the program
  authorizes load.
