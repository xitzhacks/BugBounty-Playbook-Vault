---
title: "GraphQL & API Object Exposure — fields that read without permission"
type: playbook
category: graphql-api-objects-exposure
cwe: "CWE-200"
source_count: 21
full_bodies_available: 21
corpus: "h1-brain disclosed_reports.db (sha256 8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4) — 362 rows"
list_accessed: "2026-11-07"
note: "Anchors: INFO-978143 (security, $2,500), INFO-770209 (security, $2,500), INFO-715192 (security, $2,500), INFO-342978 (security, $2,500), INFO-1085332 (shopify, $1,900). All quotes byte-true to references/archive/INFO-bodies-full-dump.txt."
---

# GraphQL & API Object Exposure — the field *is* the bug

## 1. Overview

Twenty-one rows, **$19,252/13 paid** (max $2,500 ×5 flat). Every paid row in this module is the same shape: an authenticated (or unauthenticated) caller asks the GraphQL schema for a field the UI never shows them, and the resolver answers. The corpus's two programs dominate it — **HackerOne's own `security` team (8 rows, all flat $2,500)** and **Shopify (10 rows, $500–$1,900)** — which is the module's central lesson: the schema authors knew the objects were sensitive (private comments, report sources, whitelist counts), the UI gated them, the GraphQL layer did not. Two GitLab rows and one Instacart row round it out. Nobody in this module needed a race, a bypass, or a chain: one POST with the right selection set.

**Case-stock (21 rows / $19,252):**

| Case | Target | Mechanism | Bounty |
|---|---|---|---|
| [INFO-342978](https://hackerone.com/reports/342978) | security | Team object in GraphQL disclosed total number of whitelisted hackers | $2,500 |
| [INFO-343464](https://hackerone.com/reports/343464) | security | Team object in GraphQL discloses team group names and permissions | $2,500 |
| [INFO-715192](https://hackerone.com/reports/715192) | security | Private program disclosure via `vpn_suspended` GraphQL query | $2,500 |
| [INFO-770209](https://hackerone.com/reports/770209) | security | Unauthorized user can obtain `report_sources` attribute through Team GraphQL o… | $2,500 |
| [INFO-978143](https://hackerone.com/reports/978143) | security | Team object in GraphQL disclosed private_comment | $2,500 |
| [INFO-1085332](https://hackerone.com/reports/1085332) | shopify | [h1-2102] shopApps query from the graphql at /users/api returns all existing c… | $1,900 |
| [INFO-423388](https://hackerone.com/reports/423388) | shopify | H1514 Get access to non public information by pivoting with graphql queries | $1,500 |
| [INFO-917875](https://hackerone.com/reports/917875) | shopify | STAFF "No-Permissions" on the Store can retrieve the details Order via exchang… | $1,000 |
| [INFO-419883](https://hackerone.com/reports/419883) | shopify | H1514 [beerify.shopifycloud.com] GraphQL discloses internal beer consumption | $802.2 |
| [INFO-415622](https://hackerone.com/reports/415622) | shopify | PII disclosure -- Past team members & their email ID(personal email) can be vi… | $500 |
| [INFO-417170](https://hackerone.com/reports/417170) | shopify | Using GraphQL, STAFF with NO explicit permissions on Store can retrieve Shopif… | $500 |
| [INFO-848625](https://hackerone.com/reports/848625) | shopify | None permission staff member can identify installed application and products a… | $500 |
| [INFO-165131](https://hackerone.com/reports/165131) | instacart | Seemingly sensitive information at /api/v2/zones | $50 |
| [INFO-389600](https://hackerone.com/reports/389600) | security | TeamProfile exposes partially sensitive information through GraphQL | - |
| [INFO-409973](https://hackerone.com/reports/409973) | shopify | Some store settings/data are accessible to "No Access" permission users on Gra… | - |
| [INFO-489146](https://hackerone.com/reports/489146) | security | Confidential data of users and limited metadata of programs and reports access… | - |
| [INFO-633001](https://hackerone.com/reports/633001) | gitlab | Private System Note Disclosure using GraphQL | - |
| [INFO-707433](https://hackerone.com/reports/707433) | security | Disclosure of `payment_transactions` for programs via GraphQL query | - |
| [INFO-972355](https://hackerone.com/reports/972355) | gitlab | Able to leak private email of any user given his/her username via graphql | - |
| [INFO-1023669](https://hackerone.com/reports/1023669) | shopify | Staff with no permissions can listen to Shopify Ping conversations by register… | - |
| [INFO-1091303](https://hackerone.com/reports/1091303) | shopify | [h1-2102] [Yaworski's Broskis] Low privilege user can read POS PINs via graphq… | - |

## 2. The HackerOne `Team` object: one object, five $2,500 rows

INFO-978143 (**security, $2,500**) is the cleanest unauthenticated read in the corpus — a `node(id:)` global-ID query against `hackerone.com/graphql` returning a `private_comment` the reporter could not have seen anywhere else:

> Hi Team, Some private(I think) part of GraphQL reveals to us

> Without authorization

> As we can see, the `key` field takes the value `scope`, we don't see in which program this happens, but we can see the comments of the participant, and as we can see, it has the status private

The discriminator the reporter used is worth stealing: the response carries both `key` and a `private_comment` field, and the comment's *status* is itself private — the bug is proven by the field's presence, not by its contents (the body redacts the value with `████`). INFO-770209 (**security, $2,500**) shows the inference version of the same bug: `report_sources` is non-empty exactly when the program is private, so the field is a private-program oracle:

> If this parameter is not empty, then the program is private. - `["HackerOne Platform"]`

> `{"data":{"team":{"_id":"█████","report_sources":["HackerOne Platform"]}}}` - `["HackerOne Platform"]` - private program

INFO-715192 (**security, $2,500**) makes the oracle explicit in prose — `vpn_suspended=false` on an external program that also has a private program reveals the private side because sandbox programs have no VPN:

> If an external program (which also has private program) has enabled VPN , then value of vpn_suspended become false, so with this information, an attacker can find external programs which have private program, because there is no VPN feature in sandbox mode (all other external programs will be in sandbox mode)

INFO-343464 (**security, $2,500**) and INFO-342978 (**security, $2,500**) are the enumeration pair — group names and permissions (`team_member_groups{id,name,permissions}`) and a head-count of IP-whitelisted staff (`whitelisted_hackers{total_count}`), each a single `team(handle:)` query:

> Because of the communications error, we can disclose the data - `team_member_groups{id,name,permissions}`

> Again, because of the link error, I can see the number, but I can't see these links. Analogue #310946

The flat $2,500 across five reports from the same author (haxta4ok00) is the pricing signal: HackerOne paid per *field*, not per impact tier. The unpaid sibling INFO-489146 (security, $0) names the full blast radius the flat rate implies — `otp_backup_codes`, `account_recovery_phone_number`, `vpn_credentials`, `calendar_token` all readable via `users()` — but carries no bounty figure, so it anchors the lesson without pricing it.

## 3. Shopify's no-permission staff lane: the schema doesn't check the caller

The Shopify cluster is the module's second act — every row is a staff member with **no permissions** asking GraphQL for data their role forbids. INFO-423388 (**shopify, $1,500**) states the class rule directly:

> It is possible to pivot with queries to get access to information you shouldn't have access to according to docs located at https://help.shopify.com/en/api/graphql-admin-api/reference/queryroot

> User with no home access can use locations query to find out store locations and address

The pivots span store geography, inventory (`inventoryLevel`), marketing budgets, and publication API keys (`query{publications(first: 100){edges{node{name, id, supportsFuturePublishing, app{apiKey}}}}}`) — INFO-423388's line "Note it doesn't say access denied." is the module's motto. INFO-1085332 (**shopify, $1,900**) is the bulk-exfiltration proof: `shopApps(first:10000)` including `"isPrivate":true`, searchable in the response:

> In the response, if you search for `"isPrivate":true` you will see also private apps.

INFO-917875 (**shopify, $1,000**) shows the side-effectful variant — `exchangeReceiptSend` mints an order-authenticate link and sends it by SMS to a phone number the staff member supplies, so the disclosure is delivered, not merely displayed. INFO-415622 (**shopify, $500**) is the PII bridge to module 03: past partner-team members' personal emails, and — worse — *updated* emails after the ex-member changed them at `https://accounts.shopify.com/account`, visible to current staff with no permissions. The `$500` (vs `$1,900` for private-app bulk read) prices the PII *of departed staff* below the PII *of the store*.

## 4. GitLab system notes and email lookup: the UI/API split

INFO-633001 (gitlab, $0) proves the REST/UI-vs-GraphQL split: private system notes — moves to private projects, duplicates of confidential issues, mentions of confidential issues — are "properly hidden in REST and UI" but readable at `https://gitlab.com/-/graphql-explorer`:

> They are properly hidden in REST and UI, but you can still see them in graphql

INFO-972355 (gitlab, $0) is the smallest possible disclosure — `user(username:"<victim>"){email, username}` against an account with private email settings:

> Leaks private emails of users by just knowing their usernames. Attacker can use this bug for mass leakage of gitlab users private emails.

Both carry no bounty figure; kept because they name the two fixes that generalize: field-level authorization (not UI hiding) and private-by-default email fields on the user object.

## 5. The unpaid tail and what it still teaches

Eight rows carry no figure. Their titles complete the map: `payment_transactions` for programs (INFO-707433), POS PINs readable by a low-privilege user (INFO-1091303), store settings for "No Access" users (INFO-409973), Ping conversation listening (INFO-1023669). The absence of a figure is not evidence of non-payment (DB `None` ≠ $0), but the pattern across the module is legible: paid rows all show the *response carrying the sensitive value* (a JSON blob, a count, a link), while several unpaid rows describe capability without showing the value. That is the P5 gate this vault's playbook will enforce.

## 6. What pays, what doesn't

- **Pays, flat**: a single GraphQL field that returns a sensitive value on a private object. Five HackerOne Team-object fields paid identically ($2,500 each) regardless of whether the value was a comment, a boolean, or a head-count. Price the *field*, show the JSON response.
- **Pays, tiered**: Shopify's schema-pivot rows paid by data sensitivity — bulk private-app list $1,900, cross-permission pivot $1,500, order-link delivery $1,000, departed-staff PII $500. The ladder is about *whose* data and *how much*, not about query cleverness.
- **Doesn't pay (in this corpus)**: capability claims without a visible value. INFO-489146's catastrophic field list (OTP backup codes, VPN credentials) is the most damaging description in the module and carries no figure — triage paid for the five narrow proofs, not the broad one.
- **The oracle lesson**: a boolean/count field (`report_sources`, `vpn_suspended`, `whitelisted_hackers{total_count}`) pays the same as a content field. If the field's *value* classifies the object (private/public, sandboxed/live), it is a disclosure even when the value itself looks innocuous.

## 7. Cross-references

- Module 02 (`02_HackerOne-Reports-Bounty-Privacy.md`) holds the REST/JSON twin of this class — INFO-3000510's `/reports/:id.json` disclosure is the same "field the UI hides, the API serves" shape without GraphQL.
- Module 03 (`03_User-PII-Location-Privacy.md`) — INFO-415622's departed-staff emails and INFO-972355's email lookup are GraphQL *mechanisms* for the PII *class*; read them together.
- The companion `../22_GraphQL/` vault (upcoming) is the technique shelf (introspection, field enumeration); this module is the *pricing* shelf — what each field type was worth.
