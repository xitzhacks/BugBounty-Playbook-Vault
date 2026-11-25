---
title: "Stale-Permission & Own-Action-Misuse"
type: playbook
category: stale-perm
cwe: "CWE-285 (Improper Authorization); CWE-639"
case_ids: "IDOR-016, IDOR-017, IDOR-021, IDOR-022, IDOR-036, IDOR-038; IDOR-028; IDOR-027; IDOR-009, IDOR-031"
sources: "8 H1 reports + 1 blog"
evidence_split: "8 cases: full 6, summary 2"
archive_accessed: "2026-10-16"
---

# Stale-Permission & Own-Action-Misuse

## 1. Overview

Two paired defect patterns where the *server accepts an action the principal used to be or *is technically* authorized for, but current state violated:

- **Stale-permission:** a permission the principal **had earlier** (e.g., "invite" privilege at step 4)
  is revoked, but the server accepts the previously-issued action anyway.
- **Own-action-misuse:** the principal had permission for *some* object; the server's authorization
  check treats "any principal in this object's scope" as sufficient, letting a restricted
  principal misuse the flow to affect **another** principal's object on their behalf.

The two patterns matter because both produce "I had access" denials in triage and because testing
them requires *state transitions* rather than just ID swaps — a level of work most bug-bounty
testers skip.

## 2. Case studies (verbatim)

### 2.1 IDOR-016 — mavenlink: revocation race during in-flight request

**Team:** mavenlink (21210) — "privilege escalation"

Steps verbatim comparison (Y/B does the act, X/A changes B's roles mid-flight):
> "Access the user A console through browser X, and set the privilege of user B to Collaboration and
> also remove the invite privilege just corresponding to that user, as shown in image below. Now save it.
> Now move to user B again from where we left in step 4. Enter any email id and submit the request.
> You will see request will get completed successfully and given user will be invited, while this
> user **doesn't having any privilege to do so**."

Key teaching: The bug introduces a **TOCTOU** — the server validated the privilege once when the
form opened, then accepted the form POST later even though revocation completed in between. The
correct fix is re-authorizing on *submit*, not on *navigation*.

### 2.2 IDOR-036 — Shopify: limited-access user reaches admin activities feed

**Team:** shopify (95589) — "Privilege escalation and circumvention of permission to limited access user"

The **limited** user should see no activity feed at all. Test showed:
- `/admin/activity` → correctly blocked for limited user.
- `/admin/dashboard/activity_feed?activity_pages=XXXX&activity_filter=all` → **served**, allowing
  the limited user to "view all shop admin activities".

Two lessons: (a) permission must be enforced on the *data endpoint*, not on the *navigation UI*;
(b) the restricted route is frequently a **second, lower-privilege path** (here a dashboard
sub-endpoint) kept un-restricted. Always enumerate alternate routes for the same object.

### 2.3 IDOR-038 — Shopify: delete/modify own comment after access was removed

**Team:** shopify (154410) — "Delete/modify your own comment after limited access (IDOR)"

> "Now owner of the account limited access to orders, then he won't be able to access his comments
> and he won't be able to modify/delete his comments. **But this can be bypassed and he can still
> modify and delete his own comments.** Comment ID can be used in any other feature's comment
> section to delete/modify comments."

Two defects stacked: (a) access check happens on the *feature*, not on the *comment object*
itself; (b) changing path from /orders/comment/1 to /transfers/comment/1 reuses the same
comment-id scope. This is a **route-confusion inside object-level authorization** — the object is
legitimately the principal's own, but the feature access was removed; the server never checks
whether the *feature* is still authorized when the *id* is presented from a different route.

### 2.4 IDOR-028 — Shopify $1000: member without `ORDERS` access can still access via Order Printer app

Report body withheld (evidence: title + program summary). Verbatim title:

> "Privilege Escalation - A `MEMBER` with no ACCESS to `ORDERS` can still access the orders by
> using the `Order Printer APP`"

Classic own-action-misuse: the app integrations layer checks the *user*, not the *orders*, and
app integrations are a **second authorization surface** apps often forget. **Bounty paid: $1000.**

### 2.5 IDOR-031 — Shopify $500: limited user accesses Payments page

Shopify's own summary: "Users with the `Orders` permission were allowed to see the store's payment
gateway information. This page should have been restricted to users with the `Settings` permission
only." **Two exploitable facets:** (a) page reach, and (b) "adding payment methods"  — a write
action on `Settings`, executed by a principal restricted to orders.

### 2.6 IDOR-009 — romit (enter): any co-owner deletes another user's share

**Team:** enter (85720) — "IDOR on removing Share"

> "In case of Operator Wallets, only `Owner` has the permission to delete share with any user.
> But It is possible for any user to delete share for any other user."

The crux is distinguishing **re-sharing with someone** (allowed) from **removing someone else's
share** (Owner-only). Attack:

```
POST /dashboard/account/<accountID>/sharing/delete
bankUserId=<User C's ID>&_csrf=...
```

**Bounty: $250.** The tester's suggested fix says "verify that the user who is deleting the user
is actually an owner for that wallet" — object-level authorization on the *share-removing
operation*.

### 2.7 IDOR-021 / IDOR-022 — Phabricator: state-privilege bypass

- IDOR-021 (38965): "Phabricator Diffusion application allows unauthorized users to delete
  mirrors". **Bounty: $300.** Mirrors could be removed by users who could see the repo but not
  admin it.
- IDOR-022 (202499): "User with only Viewing Privilege can send message to Room". **Bounty: $300.**
  The report notes "**there's no form to send messages when the user access the room** since in
  theory it shouldn't be possible. However, messages via POST requests can still be sent and
  processed." Demonstrates UI-hiding vs API-enforcement: hiding the form is not authorization.
  Working POST provided verbatim:

```
POST /conpherence/update/1/ HTTP/1.1
...
__form__=1&action=message&text=TESTTEXT&latest_transaction_id=10&__wflow__=true...
```

### 2.8 IDOR-017 — Mixmax: add notes without contact access (summary evidence)

Report title: "Privilege escalation — User who does not have access is able to add notes to the
contact". Body withheld; title is official evidence.

## 3. Payload / workflow corpus

### 3.1 Stale-permission probing

1. Get the privilege form to open (or capture the action request once).
2. **Downgrade your own role** through the admin UI (or ask an admin in a test account).
3. Re-send the previously captured request without refreshing the page.
4. Any 2xx is a stale-permission bug.

```http
# captured while authorized
POST /invite                  # was: {"email":"[REDACTED_EMAIL]","role":"team_lead"}
# after downgrading user's role in a second tab:
# re-send identical POST → must be 403; if 2xx → TOCTOU/stale authorization
```

### 3.2 Own-action-misuse / secondary routes

1. Identify every *restricted* page or action (Settings, Payments, admin views).
2. Identify every **app or sub-endpoint** that touches the same data
   (`/admin/dashboard/*`, Order-Printer, Tax-overrides, RSS-file renders).
3. Test the restricted action via each secondary surface.
4. If blocked once, try `nullcast_flag=1` removal, wrong method, or content-type change.

## 4. Remediation

1. **Authorize on submit, not on render.** A form that was rendered to an authorized principal
   must still be re-authorized at POST time.
2. **Centralize authorization at the object level**, not the page level. Any object reachable by
   user U's *session* must be re-checked regardless of feature.
3. **App surfaces count.** Plugins, integrations, dashboards, and secondary render paths
   (activity feed path in IDOR-036, Order-Printer in IDOR-028) must carry the same ACL as the
   primary path.
4. **Never implement authorization as "UI hides the button."** IDOR-022 (phabricator $300) is the
   canonical demonstration: POST-only access bypasses any UI-only check.
5. **Distinguish owner/manager roles per-object, not per-service.** IDOR-009 (romit) fix:
   "verify that the user who is deleting the user is actually an owner for **that** wallet."

## 5. Sources (verbatim)

| Case ID | Report | Evidence | Team | Weakness (assigned) | Title |
| --- | --- | --- | --- | --- | --- |
| IDOR-016 | [21210](https://hackerone.com/reports/21210) | full | mavenlink | Privilege Escalation | privilege escalation (in-flight role revocation) |
| IDOR-036 | [95589](https://hackerone.com/reports/95589) | full | shopify | Improper Authentication | Privilege escalation and limited access circumvention |
| IDOR-038 | [154410](https://hackerone.com/reports/154410) | full | shopify | Privilege Escalation | Delete/modify your own comment after limited access (IDOR) |
| IDOR-028 | [64164](https://hackerone.com/reports/64164) | summary | shopify | Privilege Escalation | `MEMBER` with no ORDERS access via Order Printer APP |
| IDOR-031 | [92481](https://hackerone.com/reports/92481) | summary | shopify | Privilege Escalation | Accessing Payments page and adding payment methods with limited access |
| IDOR-009 | [85720](https://hackerone.com/reports/85720) | full | enter | Violation of Secure Design Principles | IDOR on removing Share |
| IDOR-021 | [38965](https://hackerone.com/reports/38965) | full | phabricator | Improper Authentication | unauthorized users delete mirrors |
| IDOR-022 | [202499](https://hackerone.com/reports/202499) | full | phabricator | Privilege Escalation | Viewing-privilege user can message room |
| IDOR-017 | [235059](https://hackerone.com/reports/235059) | summary | mixmax | Privilege Escalation | add notes to contact without access |

External: BLOG-002 (omarzzu) — PATH/UUIDs, second surface to clear stale state.
