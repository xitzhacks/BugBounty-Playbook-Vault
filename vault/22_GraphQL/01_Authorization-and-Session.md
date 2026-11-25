---
title: "GraphQL Authorization & Session — one schema, two authorization paths"
type: playbook
category: graphql-authz
cwe: "CWE-862, CWE-613"
source_count: 9
full_bodies_available: 9
corpus: "h1-brain disclosed_reports.db (3,673 rows) · sha256 8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4"
list_accessed: "2026-11-07"
note: "Anchors: GQL-1618347 ($25,000 private-program asset disclosure), GQL-1192460 ($1,370 deactivated user), GQL-417382 ($500 session revoke gap)."
---

# GraphQL Authorization & Session — the REST rules do not apply here

## 1. Overview

Nine rows, **$27,870/5 paid**. The pattern that repeats: the product enforces a rule in its
REST/view layer (session revoked, account disabled, staff lacks permission, program is private)
and forgets the GraphQL resolver. The GraphQL endpoint becomes an oracle that answers questions
the UI refuses.

**Case-stock (9 rows / $27,870):**

| Case | Target | Mechanism | Bounty |
|---|---|---|---|
| [GQL-1618347](https://hackerone.com/reports/1618347) | security | `node(id:)` fetch of `PolicyPageAssetGroup` discloses private-program assets, unauthenticated | **$25,000** |
| [GQL-1192460](https://hackerone.com/reports/1192460) | gitlab | Deactivated user still reads data via GraphQL (`:log_in` vs `:access_api` policy) | $1,370 |
| [GQL-417382](https://hackerone.com/reports/417382) | security | Revoking a session does not revoke its GraphQL access | $500 |
| [GQL-528940](https://hackerone.com/reports/528940) | shopify | Staff with no permissions reads `ActivityFeed` via GraphQL | $500 |
| [GQL-707406](https://hackerone.com/reports/707406) | security | `team(handle:){_id,industry}` reveals private programs | $500 |
| [GQL-608656](https://hackerone.com/reports/608656) | security | Disabled account keeps using GraphQL | - |
| [GQL-614355](https://hackerone.com/reports/614355) | gitlab | `namespace` query leaks data absent from REST API | - |
| [GQL-885539](https://hackerone.com/reports/885539) | x | Private list members via brute-forced snowflake IDs | - |
| [GQL-955286](https://hackerone.com/reports/955286) | security | `order_by: jira_status` count differential reveals Jira usage | - |

## 2. The $25,000 row: a `node()` lookup with no authz check

GQL-1618347 is the corpus's GraphQL crown and it is two lines long — a global Relay ID fetch:

```json
{"query":"{node(id:\"gid://hackerone/PolicyPageAssetGroupsIndex::PolicyPageAssetGroup/3981-41287\"){... on PolicyPageAssetGroupDocument{id,name}}}"}
```

> Without authorization

> Disclosing Sсope(Assets) in Private Programs

Lesson: the `node(id:)` / `object_from_id` pattern is the highest-yield GraphQL probe. Every
schema that implements the Relay spec exposes it, and authorization is frequently attached to
the *parent* resolver only.

## 3. Session and account-state gaps

GQL-417382:

> The new __REVOKE__ session feature will destroy the session of the selected device, that means any request that requires authorization should not work (`POST`, `GET`) __BUT__ i have observed that you forgot the `GraphQL` query request

GQL-1192460 names the policy split explicitly:

> When reading through the changelog for 13.11.2 i noticed that the rule for a deactivated user allows for :log_in (as it should) but it is restricted from :access_api(as it should)

> The GraphQL endpoint does not seam to use this rules when authorizing a user.

GQL-608656 is the same shape on the account-disable flow:

> After disabling the account, the user will be forced to `Enable` his account after logging in. However, many of actions are implemented using GraphQL endpoint which bypasses account reactivation process before use.

## 4. Permission-model bypass inside the resolver

GQL-528940 (Shopify staff, zero permissions):

> STAFF member with _NO EXPLICIT_ permissions can fetch store's activity feed by calling the vulnerable endpoint.

The report's own framing is the pattern to copy — compare the UI's denial with the resolver's
answer, and put both in the report.

## 5. Schema-oracle rows (no resolver bug, still money)

- GQL-707406: a single scalar field on `team` discloses that a private program exists:
  `{"query": "query {team(handle:\"...\"){_id,industry}}"}`
- GQL-614355: `namespace` returns fields the REST API 404s.
- GQL-955286: sorting by `jira_status` changes `total_count` — a side-channel that proves a
  hidden integration.
- GQL-885539: snowflake-ID brute force against a list-members query.

## 6. What pays, what doesn't

- **Paid**: cross-tenant data, private-program identity, deactivated/session-revoked access.
- **Unpaid**: "introspection is enabled" (by design for most public APIs) and theoretical
  authorization gaps without a concrete object you should not see.
- Report the *object* you obtained and the *policy* it violates; the query alone is not impact.

## 7. Cross-references

- `../IDOR/` — the same object-level authorization failure in REST.
- `../Authentication-Session/` — session revocation and account-disable semantics.
- `02_IDOR-Mutations-and-Type-Confusion.md` — mutation-side equivalents.
