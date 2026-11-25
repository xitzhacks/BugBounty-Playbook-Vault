---
title: "Parameter-Gate & Hidden-Function Access Control"
type: playbook
category: param-gate
cwe: "CWE-285, CWE-425 (Direct Request)"
case_ids: "IDOR-009, IDOR-010, IDOR-012, IDOR-019, IDOR-023, IDOR-024, IDOR-025, IDOR-052, IDOR-066, IDOR-069, IDOR-006, IDOR-010, IDOR-007, IDOR-005, IDOR-008"
sources: "13 H1 reports + 1 blog"
evidence_split: "13 cases: full 9, summary 4"
archive_accessed: "2026-10-16"
---

# Parameter-Gate & Hidden-Function Access Control

## 1. Overview

Here the server *does* know who you are and there *is* a role you have; the bug is that **access
control is implemented as hiding the button / page from the UI**, or the server accepts a
parameter that **switches off** its own check.

Two sub-patterns, both demonstrated by full evidence:

1. **Hidden route / unlinked page**: every admin function exists at a route, and *the only
   enforcement is whether the route is linked from the UI*. (Most of the DoD cases.)
2. **Parameter gate / functional check**: the server decides to skip its own ACL because some
   parameter is present/absent, or because the *request* is asking for a lookup of a
   *non-existent* user/object (an empty-object bypass).

Both are distinct from "cross-tenant read" — the flaw is not that the wrong *object* was
authorized; it is that a hidden **function** (an admin-only page, a bulk action, a
second-implementation of the same feature) was left un-authorized.

## 2. Case studies (verbatim)

### 2.1 DoD 4-tuple: 3 IDOR + 1 privilege escalation

All four have official-summary evidence only (body withheld). Titles + summaries:

| Case | Report | Program summary |
| --- | --- | --- |
| IDOR-005 | [184933](https://hackerone.com/reports/184933) | "A Department of Defense website was vulnerable to an insecure direct object reference vulnerability (IDOR) which may allow an attacker to **modify web content or certain database parameters**. @uranium238 was able to demonstrate this vulnerability by **manipulating web objects in a particular way**." |
| IDOR-006 | [199644](https://hackerone.com/reports/199644) | "…exposed to a privilege escalation vulnerability, which could have allowed **remote administrator access** to the website." |
| IDOR-007 | [203311](https://hackerone.com/reports/203311) | "A DoD website was configured in a manner that allowed a remote user to **bypass a file access control**. …could have allowed the user to **view potentially sensitive system files**. …by crafting a **specially formatted URL**." |
| IDOR-008 | [207099](https://hackerone.com/reports/207099) | "…vulnerable to an IDOR attack which may allow an attacker to **modify web content or certain database parameters**. …by manipulating web objects **in a clever way**." |

Combined lesson (this is why they're grouped): a single "hidden function" class yields
*four+ separate valid cases* against one DoD target: read, write, admin access, and file-ACL
bypass. The DoD program treated each as independently payable.

**BLOG-003 (omarzzu₂)** extends the class into modern practice: same pattern but via
`/updatePrice\\` — path normalizer disagrees with router, middleware sees a *different route*
than the one the backend executes (backslash variant reached the underlying controller).

### 2.2 IDOR-010 — Files (BrickFTP) $600: hidden-function QuickLink path bypass

Full body — one of the best demonstrations in the corpus:

> "This is a bug in the file sharing feature QuickLink. The file access control is flawed which
> allows an attacker to download not just the shared file, but **any file that has the same name
> prefix as the shared file**."

Tester's setup (verbatim):
> ```
> bar
> foo
> foobar/secret
> footer.php
> ```
> "Let's say I want to share `foo` … GET request … Notice that the `path` variable contains foo,
> if we change it to `bar`, it will tell us: *Invalid path for bundle*.
>
> However, any other path starting with `foo` can be downloaded. For example
> https://pwn.brickftp.com/bundles/download?code=23a17148e&path=footer.php&x=767de6540
> This would also allow to download any file in `foobar/`"

Prefix-matching bug. The hidden function is the *whole `path` parameter itself* — it's a
second surface behind a first surface (the share bundle), and one is auth'd on the file, the
other on a *prefix test*. **Bounty: $600.**

### 2.3 IDOR-012 — GITLab: private group names of subgroups (full)

Full body:
> "While exploring Subgroups... Unprivileged User Can **Disclose Private Group Names**"

The program labeled this Insecure Direct Object Reference (IDOR). Fast-critical for
*reconnaissance*: a unprivileged user can list the *names* of private subgroups of any group by
walking the group's `children.json` route. Names alone can seed lots of downstream bugs — a
landing field for future tester effort.

### 2.4 IDOR-024 — HackerOne $500: external-user deletion ticket-bombing

Full body:
> "In the program portal, there is an option to add external people as participants in a bug
> report. The admin can then remove this person as well if needed.
> The request for removing an external reporter looks like:
>
> ```
> DELETE /reports/<report_id>/external_users/<user_id> HTTP/1.1
> ```
>
> It was observed that by simply changing the value of `<user_id>` in the above URL, it is
> possible to generate a delete notification for the user associated with that particular user id
> even though **that user was never invited as a participant** for that bug report in the first
> place."

"A malicious admin can possibly generate notifications within a bug report of removing
participants which they never added which might be a little confusing to other admins."
**Bounty: $500.**

Program summary (id-linked): demonstrated by removing a participant who had never been added.
Multiple program staff gave one user repeated deletion-tickets by *roasting* ticket-nuking;
also usable for the residual negative case, delivering free key-recon (a ticket used to
blackhole test the message-not-spoofed path).

### 2.5 IDOR-025 — HackerOne $500: mediation invite link

Summary:
> "When a company user requests mediation on a report, a support ticket is created for the
> HackerOne team to investigate. @kirkj found out that the support ticket **included an
> invitation link**, and that some support reps may include it inadvertently within email
> replies. If HackerOne had not accepted the invitation by then, any user with access to the
> support invitation link would be able to access..."

### 2.6 IDOR-069 — Twitter ads: creating unauthorized audience lists

Full body:
> "While creating a new audience list at the URL
> `https://ads.twitter.com/accounts/<redacted>/audience_manager/create_list_audience`, under
> `Data security and privacy` it is clearly mentioned that [...]. During testing, it was observed
> that it is possible to load an audience list from a **completely different account that you
> are not authorized to have access to**."

> "* Now, logout of this account and authenticate into a different account. Follow all the steps
> above but instead of uploading the same CSV file as above, submit a random file and intercept...
> parameter `blobstore_path` in the POST body ...
> blobstore_path=%2Fta_data%2F2812522204%2F1413168758432.txt"

Classic upload-then-reference scoping bug: the CSV file is uploaded first to
`upload.twitter.com`, then its path is a bare parameter in another POST. The path references
another account's contained file. The tester says "The X-CSRF-Token, session cookies and the
account IDs are redacted below" — full attack is a two-chain (upload + reuse).

### 2.7 IDOR-052 — Veris: read any terminal's authentication details

Summary from 3.1 of Cross-Tenant playbook, but the *scoping* flavor here: the tester reports
that reading "Authentication Details of any Terminal/Gatekeeper" is admin-only, yet fetchable by
any tenant via the same semantically-visible terminal-id parameter.

### 2.11 Instagram — private posts via oEmbed + UA + block-state (BLOG-004, 2023)

External blog — [003random, "How I Exposed Instagram's Private Posts by Blocking Users"](https://003random.com/posts/meta-bountycon-instagram-writeup/) — read in full.

The chain combines three independently-insufficient controls, each a separate sub-object with
its own scoping decision:

1. **oEmbed endpoint** — `GET https://www.instagram.com/api/v1/oembed/?url=...` returns 403
   `Private media` for private accounts, and 404 `No Media Match` if the requesting user is
   **blocked** by the post's owner:
   > "the media is a URL to the instragram CDN, with special auth tokens that allow you to view
   > the post."
2. **User-Agent gate** — the same endpoint has *separate*, weaker logic for mobile UAs:
   > "the behavior seen from my Chrome instance can only be replicated by either placing
   > `android` or `iphone` in the user agent, no matter the position or context."
3. **Block-state as an oracle** — blocking a user flips the CDN-token response between
   distinguishable states, and *the tester controls the block*, creating a differential:
   > "If the endpoint returns valid JSON, then the script.onload is fired. Otherwise the
   > script.onerror is fired, meaning that we have blocked the current visitor on Instagram."

Result: "we have a chain that allows us to bypass Meta's various security restrictions to
retrieve posts and media that are normally inaccessible" — cross-principal media-scoped read by
successfully combining a media gate, a UA gate, and an attack-controlled state toggle.

## 3. Workflow

1. **Inventory every action** the product can do; find each *route* and *param* that reaches it.
2. **Inventory every parameter that can switch check behavior on/off** — flags, verbs, types,
   sizes, empty strings, `right` values.
3. **Inventory all routes with the same object** — the "second implementation" surface,
   `/api/`-other `/v2/`, `/admin/`, other mime-types (`json`), mobile-API paths.
4. **Inventory all hidden surfaces** — is the admin backend present but unlinked? Export as
   CSV? Test "request error pages" too (safest hidden surface: error pages, robots list, etc.).
5. **Direct requests for routes that failed *some* ACL; then check the bulk/CSV/JSON route.**

## 4. Remediation

1. **Server-side enforcement is the only ACL.** "Hide admin buttons from insufficient
   privileges" is not authentication, it is UX.
2. **Every route and every surface** must repeat the check: `/json` variants, `/api/`
   paths, upload-only parameterized paths, platform-specific app paths (android/iOS), admin
   sub-domains — none is a safe default.
3. **Do not derive authorization from file prefix matching** — implement exact-path ACL.
4. **Parameters in second-step calls** (post-upload references like `blobstore_path`) must be
   verified against the calling principal's own data-upload list.

## 5. Sources (verbatim)

| Case ID | Report | Evidence | Team | Weakness (assigned) | Title |
| --- | --- | --- | --- | --- | --- |
| IDOR-005 | [184933](https://hackerone.com/reports/184933) | summary | deptofdefense | Privilege Escalation | Insecure direct object reference on a DoD website |
| IDOR-006 | [199644](https://hackerone.com/reports/199644) | summary | deptofdefense | Privilege Escalation | Privilege Escalation on a DoD Website |
| IDOR-007 | [203311](https://hackerone.com/reports/203311) | summary | deptofdefense | Improper Authentication | Bypass file access control on a DoD website |
| IDOR-008 | [207099](https://hackerone.com/reports/207099) | summary | deptofdefense | Violation of Secure Design Principles | IDOR in a DoD website |
| IDOR-010 | [214001](https://hackerone.com/reports/214001) | full | files | (none) | QuickLink file ACL incorrectly enforced |
| IDOR-012 | [215384](https://hackerone.com/reports/215384) | full | gitlab | IDOR (assigned) | Unprivileged user discloses private group names |
| IDOR-024 | [46397](https://hackerone.com/reports/46397) | full | security | Violation of Secure Design Principles | Insecure Direct Object Reference vulnerability $500 |
| IDOR-025 | [123420](https://hackerone.com/reports/123420) | summary | security | Improper Authentication | Mediation link accepted by other users $500 |
| IDOR-069 | [31188](https://hackerone.com/reports/31188) | full | x | Violation of Secure Design Principles | Creating Unauthorized Audience Lists |
| IDOR-052 | [120293](https://hackerone.com/reports/120293) | full | veris | Privilege Escalation | Authentication details of any terminal |

External: **BLOG-003** (omarzzu₂ — path normalization/missing authorization header), and
**BLOG-001** (hacktus — second-implementation `/api/v2/user/documents` surface).

**Also read but excluded (not IDOR-class domains):** k8s nodes/proxy RBAC (grahamhelton),
Google Cloud Build TOCTOU (adnanthekhan), and the ColdFusion mass-assignment CVE writeup
(hoyahaxa — covered in Invocation-Layer-Mass-Assignment.md instead).
