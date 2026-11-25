---
title: "Cross-Tenant / Object-Level Access Control"
type: playbook
category: cross-tenant
cwe: "CWE-639 (Authorization Bypass Through User-Controlled Key); CWE-284"
case_ids: "IDOR-001..IDOR-073 (subset)"
sources: "44 H1 reports + 2 external blogs"
evidence_split: "44 cross-tenant cases: full bodies 31, program summaries 13"
archive_accessed: "2026-10-16"
---

# Cross-Tenant / Object-Level Access Control

## 1. Overview

The core IDOR: one tenant's authenticated request reads or writes another tenant's object.
The server receives a reference (`id`, `uuid`, `site`, `path`, `blobstore_path`) and acts on the
object it points to **without checking that the authenticated principal owns or may access it**.

This playbook covers the highest-value class in the entire corpus: 44 of 73 cases (60%), including
every case above $1000. The name "cross-tenant" describes the *harm*; OWASP calls the class
"BOLA" (Broken Object Level Authorization) when it presents in an API.

### Statistically established variants observed

| Variant | Cases | Canonical |
| --- | --- | --- |
| Read other customer's data | 20 | IDOR-011 (gitlab), IDOR-014 (instacart), IDOR-030 (shopify $2500) |
| Write/modify other tenant's object | 10 | IDOR-023 (rockstargames), IDOR-048 (veris) |
| Delete other tenant's object | 9 | IDOR-046 (veris "Delete any group of any organization remotely") |
| State-changing action on other tenant (activate, expire-session, restart build) | 5 | IDOR-027 (shopify $1000 expire other user sessions), IDOR-013 (gsa fbi restart build) |

The read variant is 45% of all cross-tenant cases but required nothing more than *changing an ID*;
write and delete variants are the same test with different HTTP verbs.

## 2. Why these bugs succeeded (root causes from publics)

1. **Check the right verb, forget the wrong one.** A tenant check is applied on `GET`, missed on
   `POST/PATCH/DELETE`. (IDOR-073 — update via `edit` route paid; identical `delete` route missed.)
2. **Check exists on one feature, not on its sibling.** (IDOR-030: merchant→users search; the UI
   "customer list" restricted but the search endpoint did not check the customer↔shop relation at all.)
3. **Object exists ⇒ respond with full data.** Absence of an explicitly scoped query. Backend query
   is `WHERE terminal_id = ?` instead of `WHERE terminal_id = ? AND org_id = CURRENT_ORG`.
   (12 veris cases all follow this single missing-predicate pattern.)
4. **Trust a client-side marker.** (IDOR-034: `$admin=$page->headerreturn;` decides if admin
   functions are visible — then SWPaced `$app` depends on existing client trust.)
5. **Neglect indirect references.** Cross-tenant access through *derived* references — sharing
   (IDOR-011 sharing-group join), transfer token (IDOR-034 tax `scene=...&type_from` param),
   request-scoped path (`/api/v3/${org}/${app}/secrets/${sha}`) where path segment chosen by client.

## 3. Case studies (verbatim)

### 3.1 IDOR-011 — GitLab: share-chain leads to private repositories `$0 → priv-esc`

**Team:** gitlab (report 131210) **Weakness (program-assigned):** Privilege Escalation

Program behavior: private group page redirects to 404. The flaw: a group *shared via a project*
could join another group, inheriting rights. Exploit:
signup → project → group-link operation (server accepts `group_id` belonging to a private group)
→ then the once-private group becomes accessible → listing reveals **private repositories,
issues, milestones, and group members**.

Attack worked because the server checks *project owner* but not *target group*, and sharing-out is
granted by the project's share-out function — an ownership check on the wrong object.

### 3.2 IDOR-014 — Instacart $100: order chat logs cross-user

`GET /api/v2/order_deliveries/:order_delivery_id/order_change_logs` returned chat logs of *other
users' orders* by ID mutation (sequential IDs). Impact claimed and accepted: private
messages between shoppers/drivers/customers. Platform labeled Privilege Escalation.

### 3.3 IDOR-030 — Shopify $2500: merchant→any customer name

Shopify's official summary:

> "This issue allowed any merchant to search for users by their ID. The search would retrieve the
> first name and last name of any registered customer that belonged to any shop in Shopify."

Cross-tenant read at platform scale — every merchant can read every customer. Highest single
bounty in this class ($2500, tied with IDOR-034).

### 3.4 IDOR-034 — Shopify $2500: cross-shop hidden objects

`link_lists` feature accepted a `subject_id` parameter pointing at any shop's collection,
product, page, or blog — including **hidden** ones. Testers discovered attack formulation:

> "Open 'Inspect Element'
> - change value of element `link_list[links][][subject_id]` to any id from other shops
> - click on save then when page reloaded you will see data in box"

Post-save render leaks object metadata. The access decision happened on one parameter
(`subject_id`) that was never re-scoped on the client side.

### 3.5 IDOR-046..IDOR-056 — Veris: 12 reports, one missing predicate

Twelve separate reports in one program, all identical shape: numeric IDs in the request for
`group`, `venue`, `rule`, `terminal`, `gatekeeper`, `parent`, `member` objects 
(`TerminalID`, `venue_id`, ...). Server-side queries called `WHERE x_id = :param` with **no
organization scoping**; the platform is multi-tenant SaaS. Actions included both reads
(`Get anyone's Terminal Data`, `Get Rules of any organization`) and destructive writes
(`Set anyone's Terminal Data`, `Delete any member of any organization`, `Make Rule for Any
Group & Any Venue remotely`).

Bounties: **None disclosed** for any of the 12. Takeaway: volume of reports is not what drives
payout per report; the 12 reports together essentially proved "no object-level authorization
exists in the platform", a pattern worth reporting *once* with a full matrix.

### 3.6 IDOR-027 — Shopify $1000: expire an arbitrary user's session

`POST /admin/settings/account/expire_specific_users_sessions/7641433` — replacing the account ID
forces a logout on any user. Server never verified the session belonged to the authenticated
user. Report shows attack is "just changing the request"; no data exgregation required, just a
state-changing POST.

### 3.7 IDOR-013 — GSA BugBounty: restart any site's build

`{"site":<siteid>,"branch":"master"}` posted to `/v0/build/` (Federalist). Reporter states the
server "does not check do this site ID belongs to this user" and classifies it as a "partial
authentication bypass." Impact: any user can force-A/B any other user's site.

### 3.8 Blogs × 2: Multi-million-dollar modern cases (hacktus, omarzzu)

**BLOG-001 (hacktus.tech)** — "Fixed" IDOR turned into 5,000,000+ file leaks. File IDs were
obfuscated (`UserA_MyFile_1678886400_aBcDeF123.pdf`), so the classic IDOR from
`GET /api/v1/files/view/{file_id}` was *real but unexploitable*. Instead of giving up the test,
the researcher probed a *second* endpoint (`POST /api/v2/user/documents`) with an empty
`document_key`; the empty string was passed to the S3 list-objects call, which returned a
presigned list-all URL. Attack chain: fix bypass (empty string), leak IDs, re-run IDOR to download
other users' invoices. **Payout: one-hour triage, bug paid; impact estimate 5M+ files.**

**BLOG-002 (omarzzu)** — API that returns customer order data from a *user's* UUID instead of the
*order* UUID; request must contain a UUID but a *user* UUID leaks the object. Fix and discovery:
Replace the UUID with an *order* number and remove the UUID, and the endpoint "returned full data
response — including another user's UUID". Leaked UUID unlocked `/api/GetransactionsInfo/{UUID}`
which "knows about employee accounts", returning a JWT. The company performed $150M+ in funding;
final severity "critical" with admin takeover.

## 4. Payload corpus (2026-equivalents, supplied by playbook author — no "new bugs" invented)

```http
# Classic ID spread-read
GET /api/v2/order_deliveries/261972226/order_change_logs HTTP/1.1   # IDOR-014 style
# Empty string as key (BLOG-001 style)
{"document_key":"", "storage_id":""}
# Trusted-path bypass (IDOR-073/BLOG-002 style)
POST /dashboard/account/A/sharing/delete
bankUserId=<C>&_csrf=...
```

## 5. Testing workflow

1. Map all object references across all methods and all features (`id`, `uuid`, `site`,
   `subject_id`, `path`, `file`, `document_key`, `euid`...).
2. Map all **method/verb combinations**: for each reference found, check consistency across
   GET/POST/PATCH/DELETE (`/1=<verb>`).
3. Establish baseline: your own object (or empty-verb) returns data.
4. Swap ID to a non-owned object's; observe.
5. If blocked, test **sub-object** and **shared** modes (session-scoped container types).
6. If still blocked, test **derived references** (sharing links, transfer tokens/`from` ids,
   request-scoped path segments).
7. If still blocked, test **IDA-style other-principal** — user-another user (junior→senior),
   account-another account.
8. If the reference is opaque, try an **empty string**, encode-padded id, or `%00`-terminated id,
   then explore a second endpoint that can *mint* references (list, save, share, upload).

Evidential priority: capture requests where the server *accepts* the swapped reference even when
data isn't returned (that establishes the flaw even if the render path is blocked).

## 6. Remediation

1. **Never trust a client-side marker** (header flags, JS-driven admin roles).
2. Authorize at the **method/verb boundary**: for every endpoint, both "can the principal touch
   this object?" and "can the principal perform this verb on this object?" must be answered
   server-side.
3. Scope every query to the tenant: `WHERE ... AND tenant_id = current_tenant()` is the minimum,
   not a suggestion. Report occurrence in the 12 veris databases as the canonical demonstration.
4. For actions that "don't leak data" (delete, restart, expire), still treat as protected — the
   shopify $1000 case (IDOR-027) and gsa FBI (IDOR-013) prove these are as damaging as data reads.
5. **Do not rely on obfuscated IDs as an alternative to authorization** (BLOG-001's root cause).

## 7. Case study sources (verbatim IDs, all bounty-neutral)

| Case ID | Report | Evidence type | Team | Weakness (program-assigned) | Title |
| --- | --- | --- | --- | --- | --- |
| IDOR-011 | [131210](https://hackerone.com/reports/131210) | full | gitlab | Privilege Escalation | Privilege escalation to all private groups and repositories |
| IDOR-014 | [144000](https://hackerone.com/reports/144000) | full | instacart | Privilege Escalation | Authorization Bypass in Delivery Chat Logs |
| IDOR-030 | [92453](https://hackerone.com/reports/92453) | summary | shopify | Improper Authentication | unauthorized access to all customers first and last name |
| IDOR-034 | [93921](https://hackerone.com/reports/93921) | full | shopify | Improper Authentication | Unauthorized access to all collections, products, pages from other stores |
| IDOR-046..048 | [120121](https://hackerone.com/reports/120121), [120123](https://hackerone.com/reports/120123), [120126](https://hackerone.com/reports/120126) | full | veris | Privilege Escalation | Critical IDOR (delete group/venue/rule) |
| IDOR-049..056 | [120288](https://hackerone.com/reports/120288)..[120318](https://hackerone.com/reports/120318) | full | veris | Privilege Escalation | Terminal/Gatekeeper/Venue/Rule operations cross-org |
| IDOR-027 | [56511](https://hackerone.com/reports/56511) | full | shopify | Improper Authentication | IDOR expire other user sessions |
| IDOR-013 | [245872](https://hackerone.com/reports/245872) | full | gsa_bbp | IDOR (program-assigned) | Authenticated user can restart website build on another account |
| IDOR-023 | [204292](https://hackerone.com/reports/204292) | summary | rockstargames | CSRF | Critical IDOR insert/delete comments as another user |
| IDOR-019 | [153905](https://hackerone.com/reports/153905) | full | nextcloud | Privilege Escalation | IDOR — Disable sharing |
| IDOR-020 | [166581](https://hackerone.com/reports/166581) | summary | nextcloud | Privilege Escalation | Normal user can make admin delete shared folders |
| IDOR-015/041/042 | [178506](https://hackerone.com/reports/178506), [115209](https://hackerone.com/reports/115209), [127161](https://hackerone.com/reports/127161) | full / summary | instacart/uber | Info Disclosure | Private list metadata; trips of other users; invoice download |
| IDOR-043 | [119166](https://hackerone.com/reports/119166) | full | udemy | Improper Authentication | view others' gifts on /gift/share |

External blogs:
- BLOG-001: [How a "Fixed" IDOR and an Empty String Led to 5M+ File Leaks — Hacktus](https://hacktus.tech/how-a-fixed-idor-and-an-empty-string-led-to-5-million-file-leaks)
- BLOG-002: [From JavaScript Analysis To UUID Pattern Exploration Revealed a Critical IDOR! — Omar Alzughaibi](https://omaralzughaibi.com/blog/javascript-analysis-uuid-pattern-idor)

## 8. Report template (short-case)

```
Title: IDOR in <object> at <endpoint>: authenticated user <X> can <verb> object <Y>
Method+URI: <FULL HTTP REQUEST with your JWT, and victim's victim ID>
PoC (minimum):
  1. Own object baseline: 200 + data: <RESPONSE truncated>
  2. Other user object:   200 + data: <RESPONSE truncated>
  3. Other user write/delete: 200/204: <RESPONSE>
Impact (concrete): "any of N users can X", plus concrete object counts.
Severity suggestion: [session present] [writer/reader privilege not needed]
  - data read of any user PII: medium-high
  - cross-tenant object write/delete: high
  - cross-tenant read at platform scale: critical
[fix]: server-side tenant scoping plus object-level authorization
```

## 9. Cross-reference

- Own-action misuse → playbooks/own-action-misuse (shopify IDOR-027, IDOR-028, IDOR-031)
- Stale-permission → playbooks/stale-permission (shopify IDOR-036, IDOR-038, IDOR-046, mavenlink)
- Role-scoping → playbooks/role-scoping (shopify IDOR-033, IDOR-039, IDOR-031, algolia, H1)
