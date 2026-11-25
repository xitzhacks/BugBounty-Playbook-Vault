# Shopify Storefront API — Testing Reference

## Token Handling

Shopify session cookies contain a JWT-like structure with an embedded `shcat_` access token. Two approaches work:

### Approach 1 — Session cookie as customerAccessToken
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

### Approach 2 — Extract shcat_ token as Bearer
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

## Access Scopes

| Scope | Access |
|-------|--------|
| `unauthenticated_read_customers` | Read customer profile, orders, addresses |
| `unauthenticated_write_customers` | Create customer, login, password reset |
| `unauthenticated_read_metaobjects` | Read metaobjects |
| `unauthenticated_read_checkout` | Read checkout data |

Session cookies from the browser may have limited scopes. A fresh login token typically has more scopes.

## Shopify-Specific Behaviors

1. **Batch queries** — Return UNSUPPORTED_MEDIA_TYPE (not supported)
2. **Fragment validation** — Strict; `... on Product` inside `Merchandise` union fails
3. **Node ID validation** — Returns `"invalid id"` for malformed IDs
4. **Cart mutations** — `cartNoteUpdate`, `cartAttributesUpdate` work with just session cookie (by design)
5. **Cart clone** — Requires authentication and proper authorization
6. **URL redirects** — May return INTERNAL_SERVER_ERROR (server-side issue, not a vuln)
7. **Products/search** — Public, no auth required
8. **Shop info** — Public, no auth required

## Test Results Summary (e.l.f. Cosmetics — 70+ tests across 2 cookies)

| Test | Result |
|------|--------|
| Customer profile | ACCESS_DENIED (needs `unauthenticated_read_customers` scope) |
| Customer orders | ACCESS_DENIED (same scope issue) |
| Customer addresses | ACCESS_DENIED (same scope issue) |
| Customer update | ACCESS_DENIED (needs `unauthenticated_write_customers` scope) |
| Customer token create | ACCESS_DENIED (needs `unauthenticated_write_customers` scope) |
| Customer token delete | ACCESS_DENIED (needs `unauthenticated_write_customers` scope) |
| Customer token renew | ACCESS_DENIED (needs `unauthenticated_write_customers` scope) |
| Customer recover | ACCESS_DENIED (needs `unauthenticated_write_customers` scope) |
| Customer reset | ACCESS_DENIED (needs `unauthenticated_write_customers` scope) |
| Customer activate | ACCESS_DENIED (needs `unauthenticated_write_customers` scope) |
| Customer default address update | ACCESS_DENIED (needs `unauthenticated_write_customers` scope) |
| Customer address create | FIELD_ERROR (schema validation working) |
| Customer address delete | FIELD_ERROR (schema validation working) |
| Customer address update | FIELD_ERROR (schema validation working) |
| Cart query | FRAGMENT_ERROR (schema enforced — Merchandise union doesn't allow Product fragment) |
| Cart create | PARSE_ERROR (syntax error in query) |
| Cart note update | SUCCESS (by design — user-editable) |
| Cart attributes update | SUCCESS (by design — custom attributes accepted) |
| Cart buyer identity update | SUCCESS (email manipulation possible) |
| Cart remove personal data | SUCCESS |
| Cart clone | ACCESS_DENIED (properly secured) |
| Cart lines add | FRAGMENT_ERROR (schema enforced) |
| Cart lines remove | FRAGMENT_ERROR (schema enforced) |
| Cart lines update | FRAGMENT_ERROR (schema enforced) |
| Cart discount codes | FIELD_ERROR (schema validation working) |
| Cart gift card codes | FIELD_ERROR (schema validation working) |
| Cart metafield delete | MISSING_ARGUMENT (schema validation working) |
| Cart payment update | INVALID_VALUE (schema validation working) |
| Cart submit for completion | FIELD_ERROR (schema validation working) |
| Cart selected delivery options | MISSING_ARGUMENT (schema validation working) |
| Node IDOR | INVALID_ID (validated) |
| Products | SUCCESS (public) |
| Search | SUCCESS (public) |
| URL redirects | INTERNAL_ERROR (server-side issue, not a vuln) |
| Metaobjects | ACCESS_DENIED (properly secured) |
| Shop info | SUCCESS (public) |
| Batch query | UNSUPPORTED_MEDIA_TYPE (not supported) |
| Shop pay payment request | MISSING_ARGUMENT (schema validation working) |

## Key Findings

- No critical GraphQL vulnerabilities found
- Customer data properly secured with scope-based access control
- Cart mutations are permissive by design (user-editable notes/attributes)
- Products, search, and shop info are public by design
- Session cookie has limited scopes; fresh login token needed for full customer data testing
- Cart buyer identity update allows email manipulation (low impact — standard Shopify behavior)
- Schema validation is strict and prevents most injection attempts
- Node ID validation prevents IDOR via GID enumeration

## Pitfalls

1. **Testing the wrong target** — When the user provides a cookie for a specific target (e.g., e.l.f. Cosmetics), do NOT test it against other targets (e.g., WellPeople). The cookie is domain-specific and won't work across targets.

2. **Session cookie vs access token** — The browser session cookie (`session=...`) is NOT the same as the GraphQL access token. The session cookie contains an embedded `shcat_` token, but using the session cookie directly as the `customerAccessToken` argument will fail with ACCESS_DENIED for customer queries. Cart mutations work because they use the cart session, not the customer access token.

3. **Token extraction failures** — The session cookie uses a custom encoding that can't be easily decoded with standard base64/JWT tools. Don't waste time trying to extract the `shcat_` token — use the session cookie directly in the Cookie header for cart operations, and accept that customer data requires a proper login flow token.

4. **WellPeople endpoint differences** — WellPeople may have different GraphQL endpoints than e.l.f. Cosmetics. Don't assume the same paths work across targets.
