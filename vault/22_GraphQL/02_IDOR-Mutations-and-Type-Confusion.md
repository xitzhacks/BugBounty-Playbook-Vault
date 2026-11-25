---
title: "GraphQL IDOR, Mutations & Type Confusion — writes that skip the permission check"
type: playbook
category: graphql-idor-mutations
cwe: "CWE-639, CWE-843"
source_count: 4
full_bodies_available: 4
corpus: "h1-brain disclosed_reports.db (3,673 rows) · sha256 8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4"
list_accessed: "2026-11-07"
note: "Anchors: GQL-2122671 ($12,500 mass-delete via one query), GQL-2207248 ($5,000 billing IDOR), GQL-981472 ($2,000 fileCopy), GQL-858671 (type check → repo delete)."
---

# GraphQL IDOR, Mutations & Type Confusion

## 1. Overview

Four rows, **$19,500/3 paid**. Mutations are where GraphQL hurts: a single query parameter that
the UI never exposes can mass-modify or mass-read other tenants' objects. The corpus's paid rows
are the three biggest single-request impacts in this vault.

**Case-stock (4 rows / $19,500):**

| Case | Target | Mechanism | Bounty |
|---|---|---|---|
| [GQL-2122671](https://hackerone.com/reports/2122671) | security | `CreateOrUpdateHackerCertification` ID swap → delete anyone's certifications | **$12,500** |
| [GQL-2207248](https://hackerone.com/reports/2207248) | shopify | `BillDetails` / `BillingDocumentDownload` IDOR → PII + card last-4 | **$5,000** |
| [GQL-981472](https://hackerone.com/reports/981472) | shopify | undocumented `fileCopy` copies files across stores | **$2,000** |
| [GQL-858671](https://hackerone.com/reports/858671) | gitlab | `authorized_find` accepts any object type → Maintainer deletes repo | - |

## 2. One parameter, every record

GQL-2122671 is the cleanest "IDOR in a variable" write-up:

> While editing our **Licenses and certifications** if we change the ID number we can delete other users **Licenses and certifications**. it simply can be done by editing the ID number in our graphql query.

> If change the ID from 1 to X possible range then we can delete all the **Licenses and certifications** present between these.

That is a destructive mass-write — the reason it priced at $12,500 rather than an IDOR's usual
low band. When you find an IDOR in a mutation, check whether the identifier space is enumerable;
"delete all between 1 and X" is the impact sentence.

## 3. Read IDOR that returns financial PII

GQL-2207248:

> An IDOR on the `BillingInvoice` id on both `BillingDocumentDownload` and `BillDetails` graphql operations are leaking other merchants' ██████:

Impact list from the body: `email`, `full address`, `content of their invoice`,
`last 4 digits of credit card + type of credit card OR paypal email`, `shop impacted`.
That enumeration *is* the report — map every field the resolver returns before you submit.

## 4. Undocumented mutations

GQL-981472 shows why schema discovery matters even when introspection is disabled — the mutation
existed but was not in any UI:

> jack_mccracken is a skilled attacker he found an undocumented GraphQL API called `fileCopy`, he used this API to try to copy a file from his store `StorB`  to `StoreA` (where he is a staff member).

## 5. Type confusion at the relay layer

GQL-858671 is the Ruby-specific variant worth generalizing: the resolver authorized the *ability*
but never that the fetched node was the expected type:

> Here there is no check for whether the Object returned from `find_object` is a Snippet. I could specify any objec

A Maintainer — who cannot delete repositories — deleted one by supplying a repository ID to a
snippet-destroy mutation.

## 6. What pays, what doesn't

- **Paid**: cross-tenant writes, financial PII, mass destruction, permission-model bypass.
- **Unpaid**: mutations you can call on *your own* objects (that is the feature).
- Always test the mutation with `null`/foreign/typed-wrong IDs and record the resolver's response
  difference; the corpus's rows all include the exact operation name.

## 7. Cross-references

- `../IDOR/` — the REST twin of this module.
- `01_Authorization-and-Session.md` — read-side authorization gaps.
- `03_Injection-SSRF-CSRF-XSS-DoS.md` — mutations that reach other sinks.
