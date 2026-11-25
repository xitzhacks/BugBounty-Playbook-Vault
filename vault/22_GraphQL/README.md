---
title: "GraphQL / API-specific bugs — schema discovery, authorization gaps, and resolver sinks"
type: index
category: "GraphQL (authorization & session · IDOR/mutations/type confusion · injection/SSRF/CSRF/XSS/DoS)"
built: "2026-11-07"
evidence: "19 rows from h1-brain disclosed_reports.db (3,673 rows; sha256 8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4) — 18 bucket + 1 documented merge · all full-body"
bounty: "$58,340 across 13 rows · 01 $27,870/5 · 02 $19,500/3 · 03 $8,470/4 · merge $2,500/1"
companion_vaults: "../IDOR · ../Authentication-Session · ../SSRF · ../XSS · ../CSRF"
case_id_scheme: "GQL-<HackerOne report id>"
quote_rule: "byte-true to references/archive/GQL-bodies-full-dump.txt"
---

# Vault/GraphQL — one schema, many missing checks

Nineteen disclosed cases. The class's money is not in GraphQL's syntax; it is in the **second
authorization path** every GraphQL endpoint creates. The corpus's ceiling — $25,000 — is a
two-line `node(id:)` query that returned private-program assets without authorization.

## Start here

| # | File | What it gives you |
|---|---|---|
| 1 | [`GQL-Testing-Agent-Playbook.md`](GQL-Testing-Agent-Playbook.md) | Executable protocol: schema discovery → authz mirror → mutation probing → sink testing → kill-gates |
| 2 | [`01_Authorization-and-Session.md`](01_Authorization-and-Session.md) | Session revoke, disabled/deactivated users, staff-without-permission, private programs — 9 rows, $27,870 |
| 3 | [`02_IDOR-Mutations-and-Type-Confusion.md`](02_IDOR-Mutations-and-Type-Confusion.md) | ID swaps, undocumented mutations, Relay type confusion — 4 rows, $19,500 |
| 4 | [`03_Injection-SSRF-CSRF-XSS-DoS.md`](03_Injection-SSRF-CSRF-XSS-DoS.md) | GET-mutation CSRF, resolver SSRF, stored XSS, circular introspection — 5 rows, $8,470 |

## References (provenance layer)

| File | Contents |
|---|---|
| [`references/source-index.md`](references/source-index.md) | DB provenance, funnel, classification, bounty accounting, limitations |
| [`references/case-register.md`](references/case-register.md) | 19-row ledger with DB metadata |
| [`references/archive/GQL-bodies-full-dump.txt`](references/archive/GQL-bodies-full-dump.txt) | All 19 bodies verbatim (quote anchor) |
| [`references/archive/classes.json`](references/archive/classes.json) | Frozen id → module map |

## Scoreboard (19 rows · 13 paid · $58,340 · max $25,000)

| Case | Title (short) | Program | Bounty |
|---|---|---|---|
| GQL-1618347 | Private-program asset disclosure via `node(id:)` | security | **$25,000** (max) |
| GQL-2122671 | Mass-delete certifications via `CreateOrUpdateHackerCertification` | security | **$12,500** |
| GQL-2207248 | Billing IDOR (`BillDetails`) → PII + card last-4 | shopify | **$5,000** |
| GQL-1122408 | CSRF: mutations executable via GET | gitlab | **$3,370** |
| GQL-1864188 | SSRF in `allTicks(source:)` | exness | **$3,000** |
| GQL-1276992 | Private program handles via external-link filter (merge) | security | **$2,500** |
| GQL-981472 | Undocumented `fileCopy` cross-store copy | shopify | **$2,000** |
| GQL-1085546 | Stored XSS via `productUpdate` description | shopify | **$1,600** |
| GQL-1192460 | Deactivated user still reads data | gitlab | **$1,370** |
| GQL-417382 | Session revoke does not revoke GraphQL session | security | $500 |
| GQL-528940 | Staff with no permissions reads `ActivityFeed` | shopify | $500 |
| GQL-707406 | Private program industry disclosure | security | $500 |
| GQL-996041 | Unhandled type exception in image pipeline | reddit | $500 |
| GQL-858671 | Type check bypass → Maintainer deletes repo | gitlab | - |
| GQL-608656 | Disabled account keeps GraphQL access | security | - |
| GQL-614355 | `namespace` leaks what REST blocks | gitlab | - |
| GQL-885539 | Private list members via snowflake brute force | x | - |
| GQL-955286 | `jira_status` ordering side-channel | security | - |
| GQL-2048725 | Circular introspection DoS (Sorare) | sorare | - |

## Cross-vault links

- `../IDOR/` — the REST form of module 02's object-authorization failures.
- `../Authentication-Session/` — session/account-state semantics behind module 01.
- `../SSRF/`, `../XSS/`, `../CSRF/` — the sinks in module 03.
- `../21_Denial-of-Service/` — introspection/complexity DoS context.

## Limitations

1. **18-row bucket** is a disclosed-only slice; GraphQL testing advice from other sources is not
   part of this corpus.
2. **Bounty `-` ≠ unpaid.** 6 of 19 rows carry no figure.
3. **Schema specifics age fast** — `node(id:)` and `fileCopy` are examples of patterns, not a
   current schema map. Introspection is often disabled today; the authz-mirror probes still work.
4. **One merge row** (GQL-1276992) came from the unclassified pool and is labeled as such.
5. **Weakness labels are triage artifacts** (several rows tagged Privacy Violation or Information
   Disclosure); modules classify by body.
6. **No live testing** in this build — every claim traces to an archived body.
7. **Quotes** byte-verified against the archive; `(sic)` marks author typos.


<!-- CASESTOCK-LINK:BEGIN -->

## Case stock — vault (`_VAULT/`)

**78 disclosed reports** routed to this category · 28 with a bounty figure · **$89,172** · 58 full write-ups stored locally.

- Full list: [`_VAULT/by-vault-category/22_GraphQL.md`](../_VAULT/by-vault-category/22_GraphQL.md)
- Query: `sqlite3 ../_VAULT/reports.sqlite "SELECT id,bounty,title FROM reports WHERE ..."`
- Pull one write-up: `python3 ../_VAULT/scripts/extract_report.py <id>`

| Top paid | Program | Bounty |
|---|---|---|
| [1618347](https://hackerone.com/reports/1618347) Disclosing  PolicyPageAssetGroup in Private Programs via /graphql `gid://hackero | HackerOne | $25,000 |
| [3782701](https://hackerone.com/reports/3782701) Unauthenticated RCE in Taskcluster web-server via GraphQL filter argument (sift  | Mozilla | $12,000 |
| [3694007](https://hackerone.com/reports/3694007) Authenticated Elasticsearch Painless script execution via Query.search.sort_quer | HackerOne | $7,000 |
| [2207248](https://hackerone.com/reports/2207248) IDOR on GraphQL queries BillingDocumentDownload and BillDetails | Shopify | $5,000 |
| [858671](https://hackerone.com/reports/858671) Insufficient Type Check on GraphQL leading to Maintainer delete repository | GitLab | $4,000 |

_refreshed 2026-11-17 from the public HackerOne disclosed-report dataset_
<!-- CASESTOCK-LINK:END -->
