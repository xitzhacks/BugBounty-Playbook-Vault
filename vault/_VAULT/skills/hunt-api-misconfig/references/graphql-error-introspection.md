# GraphQL Error-Based Introspection

## When introspection is blocked but error messages still leak schema

Even when `__schema` and `__typename` queries are blocked (returning "Not allowed"),
GraphQL error messages can leak schema information when you send invalid queries.

**Case Study (2026-10, app.signalstack.com/graphql)**:

| Query | Error message | Schema info leaked |
|-------|--------------|--------------------|
| `{providers{id,name}}` | "Field 'providers' must not have a selection since type 'String' has no subfields" | `providers` returns a String (serialized JSON), not a list type |
| `{providers}` | 200 with data | Full JSON of 42 broker configs |
| `{me{id}}` | "Cannot query field 'me' on type 'Query'" | No `me` field on Query type |
| `{user{id,name,email}}` | "Cannot query field 'id' on type 'User'" | `User` type exists, but has no `id` field |
| `{connectors{id,...}}` | "Cannot query field 'id' on type 'Connector'" | `Connector` type exists, no `id` field |
| `{accounts{id}}` | "Cannot query field 'accounts' on type 'Query'" | No `accounts` query field |
| `{__typename}` | "Not allowed" | Introspection blocked |
| `{__schema{...}}` | "Not allowed" | Introspection blocked |

**Technique**: Send queries with known/non-existent field names and read the error
messages. GraphQL servers reveal:
1. Which types exist (mentioned in error: "on type 'User'")
2. Which fields exist on each type (error says field 'id' doesn't exist)
3. Which query fields are available (error says 'accounts' is not a query field)
4. Field return types (error says type 'String' has no subfields → means providers returns String)

**Detection**: Look for GraphQL endpoints where `__schema` returns "Not allowed" or
"Forbidden" but arbitrary queries return structured error messages with type/field names.

**Exploitation path**: Once you map which types and fields exist via error messages,
construct valid queries against the fields that DO exist. In this case, `{providers}`
returns 200 data (the provider list as a JSON string).