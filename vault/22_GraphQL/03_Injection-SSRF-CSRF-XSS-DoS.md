---
title: "Injection, SSRF, CSRF, XSS & DoS through GraphQL — the transport is a normal endpoint"
type: playbook
category: graphql-injection-ssrf
cwe: "CWE-918, CWE-352, CWE-79"
source_count: 5
full_bodies_available: 5
corpus: "h1-brain disclosed_reports.db (3,673 rows) · sha256 8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4"
list_accessed: "2026-11-07"
note: "Anchors: GQL-1122408 (GitLab CSRF via GET, $3,370), GQL-1864188 (Exness SSRF, $3,000), GQL-1085546 (Shopify stored XSS, $1,600), GQL-2048725 (circular introspection DoS)."
---

# Injection, SSRF, CSRF, XSS & DoS through GraphQL

## 1. Overview

Five rows, **$8,470/4 paid**. GraphQL changes nothing about sinks — it only changes how you reach
them. What *is* GraphQL-specific: the endpoint accepts GET, it accepts batched operations, and
resolvers happily dereference URLs.

**Case-stock (5 rows / $8,470):**

| Case | Target | Mechanism | Bounty |
|---|---|---|---|
| [GQL-1122408](https://hackerone.com/reports/1122408) | gitlab | mutations executed via **GET** → CSRF protection bypass | **$3,370** |
| [GQL-1864188](https://hackerone.com/reports/1864188) | exness | `allTicks(source: <url>)` performs a server-side GET → SSRF | **$3,000** |
| [GQL-1085546](https://hackerone.com/reports/1085546) | shopify | `productUpdate` description → stored XSS on a shared Shopify domain | **$1,600** |
| [GQL-996041](https://hackerone.com/reports/996041) | reddit | upload + GraphQL unhandled type exception in the image pipeline | **$500** |
| [GQL-2048725](https://hackerone.com/reports/2048725) | sorare | circular introspection, no depth limit → single-request DoS | - |

## 2. GET mutations = CSRF

GQL-1122408 states the root cause in one sentence:

> Gitlab prevents CSRF in this functionality by sending a POST request with a X-CSRF-Token header. The bug I found here was that, when we send a GET request, the backend does not expect the X-CSRF-Token header. Using this, an attacker could leverage this to bypass the existing CSRF protection

The PoC is an auto-submitting form whose `method="GET"` carries the whole mutation in the `query`
parameter. Test every mutation endpoint with GET before you look for anything exotic.

## 3. Resolver-as-proxy (SSRF)

GQL-1864188:

> The query for `allTicks` allows setting the parameter `source` that is used to do `GET` requests,  this can be set arbitrarily .

> Please note that the `source` parameter in the graphQL request can be a full URL so that any `GET` request is possible.

Blind is still paid ($3,000) when the report proves DNS/HTTP interaction — use a collaborator.

## 4. Stored XSS through a mutation field

GQL-1085546 needs no bypass; the field accepts HTML by design and a second surface renders it:

> A stored cross site scripting vulnerability exists at `handshake-web-internal.shopifycloud.com` through the `product description` field.

Payload as filed: `<img src=x onerror=prompt(document.domain)>`. The value is the *shared domain*,
not the store itself.

## 5. DoS through schema shape

GQL-2048725:

> But the catch here is because of the no-depth limits an attacker can execute a circular introspection query which is leading to a single request denial of service which is affecting both instances same time. Users don't need to be authenticated for this attack which is an extreme condition.

Related corpus row GQL-996041 is the opposite failure — an unhandled type exception in an upload
flow that broke image processing rather than crashing the API.

## 6. What pays, what doesn't

- **Paid**: authenticated-only sink reached *pre-auth* (CSRF), SSRF, stored XSS on a shared origin.
- **Unpaid/weak**: introspection enabled (by design), query-complexity complaints without a
  measured impact, `__typename` enumeration alone.
- GraphQL's batching can amplify any of these — note when your payload can be multiplied per request.

## 7. Cross-references

- `../SSRF/`, `../XSS/`, `../CSRF/` — the sink classes in full.
- `../21_Denial-of-Service/` — protocol-level amplification and ReDoS.
