---
title: "Role-Scoping & Vertical Privilege Escalation"
type: playbook
category: role-scoping
cwe: "CWE-284, CWE-269 (Improper Privilege Management)"
case_ids: "IDOR-026, IDOR-033, IDOR-039, IDOR-001, IDOR-037, IDOR-018, IDOR-019, IDOR-066, IDOR-067, IDOR-029, IDOR-004"
sources: "10 H1 reports"
evidence_split: "10 cases: full 9, summary 1"
archive_accessed: "2026-10-16"
---

# Role-Scoping & Vertical Privilege Escalation

## 1. Overview

Where **cross-tenant** bugs say "user A should not reach user B's object", **role-scoping** bugs
say "a *low-privilege principal of the same tenant* should not reach this object at all". The
object is not someone else's for the *user* — it's forbidden for their *role*.

Three sub-patterns in this corpus:

1. **Missing role check on a normal-looking admin surface.**
   *IDOR-033 (Shopify $500)*: "Missing authorization check on dashboard overviews".
   *IDOR-039 (Shopify $500)*: management-UI role-mapping where checking the wrong permission
   (`manage_apps` instead of `manage_shops`) allowed access (verbatim bug report).
2. **Two roles, one object; only one ACL.**
   *IDOR-001 (Algolia $400)*: restricted team members leak `/1/admin/*` routes.
   *IDOR-067 (weblate)*: the `/api/` does not enforce per-project access control.
   *IDOR-037 (Shopify $500)*: staff members can access admin-uploaded files.
3. **Admin-only roles that any principal can act as, by parameter or calling pattern.**
   *IDOR-052 (Veris)*: read terminal *auth details*, a clear admin-only feature.

## 2. Case studies (verbatim)

### 2.1 IDOR-026 — HackerOne: members can view ALL team members

**Team:** security (123572) — "Unauthorized Team members viewing". **Bounty: none disclosed.**

> "In a Team, a user that does not have an admin permission at
> `https://hackerone.com/[team_name]/team_members` can view the list of users in the Program by
> visiting `https://hackerone.com/[team_name]/team_members.json`."

Classic "unrestricted sub-JSON endpoint". Two fixes shown in the bug release — the UI path was
fine, the JSON path was a *separate* route that needed its own ACL check.

### 2.2 IDOR-033 — Shopify $500: dashboard-overview role scoping

Shopify's summary:

> "Users with access to view each channel's Overview could view parts of the Home screen, and vice
> versa. We fixed the issue by **correctly checking for each permission separately on the
> relevant endpoints**."

Note the wording in the fix — each *endpoint* needed its own role-check because multiple features
shared one route but different roles. Tests must probe every channel / app surface with a
role-restriction matrix.

### 2.3 IDOR-039 — Shopify $500: `Manage apps` permission gives shop access

Full body. The researcher spells the bug class:

> "Hello, I have found a permission problem in `https://partners.shopify.com` that allows a member
> with only 'Manage apps' permission to get various shop information and also list the staff
> account from inside that shop without having access the shop's admin area."

Attack steps verbatim:
> "1. Create a new partner account and add a business.
>  2. Invite a new member ... grant him **only** 'Manage apps' permission
>  3. Create a new Development Store.
>  4. Create a new staff member for that store...
>  5. Now, open another browser / incognito tab and activate the member account
>  6. Directly call the shop's detail link (has the form of https://partners.shopify.com/629528/stores/21360565..."

The reporter also notes: "because these are incremental ids, one can predict with a somewhat
accuracy what should come next by correlating the business id and the store id, then making some
math calculations. Then fine tune it by bruteforcing."

**Bounty: $500.** Note the tell-tale the reporter observed: when denied correctly, the app says
"You're missing the **Manage apps** permission required to view this page" — the wrong
permission. When the role check is done at the wrong layer, the error tells you what was checked
instead. That string is a *free reconnaissance source* for the *actual* ACL.

### 2.4 IDOR-001 — Algolia $400: restricted team member leaks all API logs

Full body. Steps:
> "1. Invite a new team member to your application and give him very restrictive rights. In my
>    case I gave him only `Search` rights and limited his access to an index called `test`.
> 2. Login as the new team member and go to https://www.aloglia.com/dashboard. You will be greeted
>    with a `You don't have access to the Algolia Dashboard.` error message.
> 3. Check in the page source for `signature` and copy its value...
>    Using this signature, you can perform queries now against `/1/admin/*`, even though you
>    don't have the rights."

Two endpoints shown, including `/1/admin/userlogs` — returning whole request + response bodies of
every query. **Bounty: $400.**

Two lessons:
- A **denied UI** tells the tester where *not* to go; a **backend signature leaked from the
  already-restricted page** is a free escalation token. Any path that leaks authorization
  *material* is a bug-stop of its own.
- `/admin/*` routes need *role checks*, not just authentication checks; signature-bearer +
  authenticated-user is not the same as admin-user.

### 2.5 IDOR-037 — Shopify $500: staff members reach admin-uploaded files

Full body:
> "### Test #1
> If the member has access only to the section Products, Inventory, & Collections
> 1. Go to the Products -> Product Name -> Description
> 2. Click the button -> Add Image
> 3. In the section Uploaded images are all files uploded by the admin, so we can simply add them
>    or download (screenshot attached)
>
> ### Test #2
> If the member has NO access to the ALL sections
> 1. So we can not go to the page Products but....
> 2. Lets go here https://*.myshopify.com/admin/rte/assets
> 3. And we will see all files uploaded by admin"

Direct URL: `/admin/rte/assets`. **Bounty: $500.** Note the reporter's framing — the reporter
tested *two* different restriction levels, producing two independent attack paths. Good practice.

### 2.6 IDOR-067 — weblate: `/api/` skips ACLs

Full body (fetched). Report specific:
> "The /api/ does not enforce access control on the translation files, allowing anyone to download
> full translation files. See the screenshot for an example project being viewed by an anonymous
> account that is configured to **have no permissions**."

Attack path: UI says Access Denied → `/api/components/testproject/testcomponent/translations/`
→ `file_url` fetches `http://192.168.1.129:8000/api/translations/testproject/testcomponent/en_CA/file/`.

### 2.7 IDOR-066 — weblate: deleted email retains access

Full body:
> "There is improper access control kind of vulnerability present in..." *access by an email
> address that has already been deleted from the authentication* — i.e., unlinking an email
> address doesn't remove existing authorization bound to that email.

### 2.8 IDOR-018 — Nextcloud: invited user with no EDIT privilege can upload

Full body. Steps:
> "+ Create any folder and invite a user in it without any edit privilege.
> + Now login from invited user account through **android app**.
> + Copy any file from your nextcloud root folder to shared folder.
> + Check nextcloud web app!! **Copied file will show in shared folder**"

Test surface: **Android app**, not the web UI. ACL is checked in one client but not the other.
The bug class: server must not distinguish "web" from "app" — the server-side ACL check has to be
platform-independent.

### 2.9 IDOR-019 — Nextcloud: IDOR disable sharing

Full body:
> "Users are shared files or folder. can disable this sharing.
>  +  use request: DELETE /nextcloud/ocs/v2.php/apps/files_sharing/api/v1/shares/{share_id}"

Reporter's specific claim: a *user's own* share ID can be disabled by a *user not holding the
share object's correct sharing role* — cross-scope shared-folder privilege enabling someone to
kill another user's outbound share.

### 2.10 IDOR-020 — Nextcloud (summary evidence): admin delete shared folder

Program summary (evidence: official summary):
> "Privilege escalation — Normal user can somehow make admin to delete shared folders"

### 2.11 IDOR-029 — Shopify (summary evidence): profile view

Program summary: "Normally a **full-access administrator** of a shop (other than the account
owner) should not be able to see the **account owner's** user profile. But a missing
authorization check allowed the account owner's profile to be viewed **if requested directly
by URL**."

## 3. Workflow

1. **Enumerate roles.** For each role create a test principal.
2. **Enumerate routes per role.** Visit every route and sub-endpoint as each role; save status
   codes for the role matrix.
3. **Look for mismatches.** Any pair `(role, route)` where an *allowed role* and *forbidden
   role* get the same response for the same object, or where a denied *page* is succeeded by an
   allowed *JSON sub-endpoint* acting on the same object.
4. **Hunt for authorization token leaks** on already-allowed pages: source-code strings that look
   like admin tokens or signatures.
5. **Look at app-platform surfaces**: mobile apps, partner/portal dashboards, RTE asset
   libraries — anywhere a *different ACL check* may have been implemented.

## 4. Payload corpus (reconstructed verbatim surfaces)

```http
# role-scoping mis-map detection (IDOR-039 style)
GET /629528/stores/21360565                       # restricted member role
# secondary route for same object (IDOR-026 style)
GET /<team>/team_members.json
# admin-only surface verified against wrong-role bearer (IDOR-001 style)
POST /1/admin/userlogs        {"applicationID":"APP_ID","signature":"SIGNATURE_FROM_PAGE",...}
# direct asset surface (IDOR-037 style)
GET /admin/rte/assets
# platform-agnostic ACL (IDOR-018 style: done via Android app)
POST /ocs/v2.php/apps/files_sharing/... (copy file into forbidden folder)
```

## 5. Remediation

1. **One ACL function, called from every route** — no secondary surface should bypass it. Each
   role-scoped route must pass `(principal, action, object)` to the same function.
2. **Centralize per-role check at the object/service layer**, not the page/view layer.
3. **Deny at the data layer.** "Members may not see other members" = filter the result *set*
   server-side; not "it is hidden in the UI".
4. **Different permission names to inspect in error messages** — if the message says "missing
   Manage apps permission", the test surface is wrong; fix the check, then message.
5. **Never trust client-generated authorization tokens alone**; if you hand a token to a
   restricted principal, make sure the token's authority (IDOR-001 `signature`) is *scoped*, and
   that the API endpoint validates *both* the token and the role of the principal.

## 6. Sources (verbatim)

| Case ID | Report | Evidence | Team | Weakness (assigned) | Title |
| --- | --- | --- | --- | --- | --- |
| IDOR-026 | [123572](https://hackerone.com/reports/123572) | full | security | Improper Authentication | Unauthorized Team members viewing |
| IDOR-033 | [93680](https://hackerone.com/reports/93680) | summary | shopify | Privilege Escalation | Missing authorization check on dashboard overviews |
| IDOR-039 | [243943](https://hackerone.com/reports/243943) | full | shopify | IDOR (assigned) | User with ONLY Manage apps permission … |
| IDOR-001 | [156520](https://hackerone.com/reports/156520) | full | algolia | Improper Authentication | Unauthorized team members can leak information … |
| IDOR-037 | [97452](https://hackerone.com/reports/97452) | full | shopify | Privilege Escalation | Staff members with no permission can access files |
| IDOR-067 | [232994](https://hackerone.com/reports/232994) | full | weblate | Improper Access Control - Generic | API Does Not Apply Access Controls |
| IDOR-066 | [223434](https://hackerone.com/reports/223434) | full | weblate | Improper Access Control - Generic | deleted email retains access |
| IDOR-018 | [145950](https://hackerone.com/reports/145950) | full | nextcloud | Improper Authentication | upload where invited user has no EDIT privilege |
| IDOR-019 | [153905](https://hackerone.com/reports/153905) | full | nextcloud | Privilege Escalation | IDOR - Disable sharing |
| IDOR-020 | [166581](https://hackerone.com/reports/166581) | summary | nextcloud | Privilege Escalation | normal user makes admin delete shared folders |
| IDOR-029 | [90671](https://hackerone.com/reports/90671) | summary | shopify | (Uncontrolled) Resource Consumption label | missing authorization on account-owner profile |
| IDOR-004 | [126861](https://hackerone.com/reports/126861) | summary | bumble | Privilege Escalation | Insecure Direct Object Reference on badoo.com |
