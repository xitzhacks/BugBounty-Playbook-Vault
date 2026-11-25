# Discovering unauthorized resolvers when introspection is off

Worked method + case study. Applies to any GraphQL endpoint where `__schema` is blocked
and field-name suggestions are absent.

## The three oracles, in order of value

### 1. Argument-signature oracle (schema recovery, no auth)

Any mutation called with **no arguments** is validated before the resolver runs, so the
error text leaks the signature:

```
mutation { appCreate { __typename } }
→ Argument "Mutation.appCreate(name:)" of type "String!" is required, but it was not provided.
→ Argument "Mutation.appCreate(redirectUri:)" of type "String!" is required, but it was not provided.
```

Repeat with the discovered args to enumerate the return type one field at a time:
valid fields are accepted, invalid ones return `Cannot query field "X" on type "AppCreate"`.
This recovered `key` and `secret` on an undocumented `AppCreate` type with introspection
disabled.

Non-existent mutations return `Cannot query field "createApp" on type "Mutation"` — so
this doubles as an existence oracle for names you guess.

Cost: 1 request per candidate name. A 30-name list is cheap and does not look like fuzzing.

### 2. Guard-vs-resolver discriminator (authorization)

Identical request shape, different error text:

| Response | Meaning |
|---|---|
| `Not Authorised!` / `Forbidden` / `UNAUTHENTICATED` / HTTP 401 | guard present |
| `Application not found`, `ValidationError`, TypeError (`Cannot read properties of undefined`) | no guard — business logic ran |
| `{"data":{"field":null}}`, zero errors | no guard — resolver completed |

A TypeError is the single strongest anonymous signal: it proves the request reached the
data layer and dereferenced a null user context. It is also, on its own, only CWE-209 —
fold it into the authz finding as supporting evidence, don't file it separately.

### 3. Sibling control (the part triagers look for)

Test a **guarded sibling in the same namespace** in the same run. "Six `appConnector*`
resolvers skip the guard, while `appCreate` in the same `app*` mutation namespace returns
`Not Authorised!`" is a code-path gap. Without the sibling control, a triager can argue the
whole namespace is intentionally public.

## Case study — SignalStack Connect API (trendspider.com bounty, 2026-10)

- Endpoint: `POST https://app.signalstack.com/graphql`, introspection blocked (13/13
  bypasses failed), no field suggestions.
- 6 unguarded root fields: `app`, `appConnector`, `appConnectorInit`,
  `appConnectorActivate`, `appConnectorActivateAccounts`, `actionsOrderCounters`.
- 9 guarded controls, incl. the sibling mutation `appCreate(name, redirectUri)`.
- Discriminator strings seen: `Not Authorised!` (code `UNAUTHENTICATED`),
  `Application not found` (`ValidationError`),
  `Cannot read properties of undefined (reading 'getActions')` (TypeError).
- Reproduced on two HTTP stacks (curl/libcurl and Python urllib) to kill
  tool-artefact arguments.

**Ceiling problem, and how to state it honestly.** The unguarded mutations take an app
UUID; `appCreate` (the only way to mint one) is guarded, and UUIDs are not enumerable.
So the primitive is proven but data return is not. Report at the demonstrated severity
(6.5 Medium, `PR:L` for "hold an app key"), state the unproven half explicitly in the
report body, and name the one thing that would close it (an account with one registered
app). Do not inflate to High on inference.

Also worth probing when you find this pattern:
- REST equivalents: on the same host, undocumented `/api/*` paths returned HTTP **418**
  with an empty body (catch-all), while real endpoints returned proper `401
  AuthenticationError`. 418/empty-body is a useful "route does not exist" signal that
  distinguishes it from "exists but gated".
- `/api/oauth/authorize` echo behaviour to confirm whether `app.key` is used as an OAuth
  `client_id` (it is, which is why "app key alone" is a weak credential).

## Reporting shape

1. Summary: how many fields admit anonymous requests, which ones mutate state.
2. Affected vs controls table, with the raw response for each class.
3. Steps to reproduce: three curls — unguarded mutation, unguarded query, guarded control.
4. Proven / not proven / what would close it — as separate labelled paragraphs.
5. Remediation: apply the same guard the sibling uses; stop treating `client_id` as an
   authorization credential.

---

## 4. Type-shape oracle — writing impact when you cannot get data

The hardest part of an unguarded-resolver report is the impact section when the credential you
need (app key, UUID, tenant id) is unobtainable. Do not hand-wave "could expose sensitive data".
Read the **shape** of the return type out of the schema instead. The validator answers *before*
the resolver runs, so this works anonymously and without introspection.

### Method

1. **Field existence + parent type name.** Send a candidate field; the error names both:
   ```
   { appConnector(key:"<uuid>", connectorKey:"<uuid>") { label } }
   → Cannot query field "label" on type "Connector".
   ```
   Any other response = the field exists. Same probe as Oracle 1, applied to return types.

2. **Field type, including scalars — the selection-on-scalar error.** Give a scalar field a
   selection set and the error prints its exact GraphQL type:
   ```
   { appConnector(...) { accounts { id } } }
   → Field "accounts" must not have a selection since type "JSON!" has no subfields.

   mutation { appConnectorInit(...) { credentials { id } } }
   → Field "credentials" must not have a selection since type "[String]" has no subfields.
   ```
   `JSON!` = serialized blob (the dataset). `[String]` = credential material. This is schema
   truth quoted from the server, not inference.

3. **Build the impact table.** Resolver → return type → confirmed fields, with the scalar types
   called out. Put it in the report where a data screenshot would normally go, and label which
   half is proven.

### Worked map — SignalStack Connect API (2026-10)

| Resolver | Kind | Returns | Fields confirmed | Type worth quoting |
|---|---|---|---|---|
| `app(key)` | query | `App` | key, name, description, redirectUris, createdAt | scalars; `secret` is NOT on `App` |
| `appConnector(key, connectorKey)` | query | `Connector` | key, status, providerId, **accounts** | `accounts: JSON!` |
| `appConnectorInit(key, connectorKey)` | mutation | `ProviderAuthentication` | type, help, **credentials** | `credentials: [String]` |
| `appConnectorActivate(...)` | mutation | `Connector` | as above | — |
| `appConnectorActivateAccounts(..., accountIds)` | mutation | `Connector` | as above | accepts `accountIds` |
| `actionsOrderCounters` | query | — | null-deref: `Cannot read properties of undefined (reading 'getActions')` | — |

Impact wording that survived review: *"`Connector.accounts` is a serialized `JSON!` blob — the
connected brokerage account dataset — and the three `appConnector*` mutations are the code path
that initialises, activates and account-binds a brokerage connector, which feeds the
order-execution path. An anonymous caller therefore reaches connector state and a state-changing
brokerage operation with no session, no user-consent check and no CSRF token."*

### Severity framing that follows from it

- Base: **6.5 Medium**, `AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:N` — `PR:L` = "holds an app key", a
  client identifier, not an admin credential.
- If the vendor confirms the resolvers trust the key alone: **8.1 High** (`C:H/I:H`), because
  `accounts` is the brokerage dataset and the mutations feed order routing.
- Ask the upgrade question in the report; don't claim the higher severity up front.

### Don't waste a pass hunting for a key in the bundles

Checked and confirmed empty: six public bundles (`ss_index`, `connector`, `trading_main`,
`index-*`, `register-app-*`, `markets_app`) contain **zero** UUIDs and zero
`appKey`/`clientId` assignments. Connector/SPA HTML and `/config*.json`-style paths return the
SPA shell or 404. App keys arrive at runtime via the OAuth URL, so static recovery isn't a path —
state that you looked, rather than implying you didn't.
