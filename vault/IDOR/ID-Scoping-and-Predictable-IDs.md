---
title: "ID-Scoping & Semi-Predictable Identifiers"
type: playbook
category: id-scoped
cwe: "CWE-639, CWE-340 (Predictable from Observable State)"
case_ids: "IDOR-015, IDOR-041, IDOR-042, IDOR-043, IDOR-045, IDOR-057, IDOR-058, IDOR-059, IDOR-060, IDOR-070, IDOR-071, IDOR-073"
sources: "12 H1 reports + 1 blog"
evidence_split: "12 cases: full 10, summary 2"
archive_accessed: "2026-10-16"
---

# ID-Scoping & Semi-Predictable Identifiers

## 1. Overview

Where cross-tenant bail covers "change an ID, get another user's data", **id-scoped** specifies a
distinct sub-flavor: the *identifier itself is scoped* by some property (ownership, join,
membership, session, org) that **disappears when the id is directly referenced**. Three flavors
captured here:

1. **Direct object id → "no check" when accessed out of context** — a former context, e.g., a
   role you once had, a session you once were granted, remains literally in the *object id path*.
2. **Sequential object id** — the exposed id increments and so enumerates all tenants.
3. **Leaked/various UUIDs used as scoping tokens** — a UUID "belongs to a user" rather than "the
   tenant is read", turning it into a bearer identifier.

## 2. Case studies (verbatim)

### 2.1 IDOR-015 — Instacart $100: private list metadata (full)

Full body:
> "When user creates a list, they can choose to not make it public. However the attacker can still
> access the information that user chose to hide.
> 1. Log in to Instacart.
> 2. Choose a private list that you want to see, for example the one with id = 10.
> 3. Go to https://www.instacart.com/api/v2/recipes/10
> 4. Response reveals all metadata of the list including title, description and image."

**Plus**: "Also, since list id is incremental it's easy to fetch metadata for all Instacart
lists, both public and private."

Classic "hide-in-UI" scoping bug: the visibility flag is known to the view path but not the API
path. And **the incremental id means the flag matters — otherwise it wouldn't be a finding.**
Claim is independent of private-flag status: private + gzip-fetched empty title still leaks
title/description/image.

### 2.2 IDOR-041 — Uber: arbitrary invoice download (summary evidence)

Program summary:
> "Due to an access control vulnerability it was possible to download arbitrary invoices if you
> had the invoice's UUID."

Two lessons: (a) invoice *number* alone is more of an enumerating identifier — the UUID — was the
attack surface, and (2) when a client passes a UUID, the ** granting** and **consuming** ends must
be linkage-checked; a UUID both proves identity AND scopes data in Uber's behavior. Closed as
duplicate (introduced internally before the report).

### 2.3 IDOR-042 — Uber: trips of other users (summary evidence)

Program summary:
> "Limited Disclosure at @maluko's request."

Title: "Information regarding trips from other users". Evidence: title-level; end-user
information on someone else's trip.

### 2.4 IDOR-043 — Udemy: gifts of other users via giftId (full)

Full body:
> "I recently purchased a gift for a friend, and noticed the share URL gift ID was simply
> numeric. I managed to access other people's gifts simply by **incrementing and decrementing
> the ID by 2**, I was able to verify that the price was dropped to 'Free', regardless of if I was
> logged in or not, and I was able to successfully redeem a gift to an account, even if it was
> not associated with the gift email, or the account that initially purchased the gift."

> "### Scope:
> This affects Udemy.com at the /gift/share/ endpoint. **Reveals name and email of recipient of
> gift, as well as exposing the gift redemption code.**
>
> ### Example URLs:
> https://www.udemy.com/gift/share/?giftId=559076 (mine)
> https://www.udemy.com/gift/share/?giftId=559078 (not mine, but still able to access it)"

Full flow + a working redemption path. No bounty disclosed — but note the tester's likely
mistake: *directed at the gift recipient*. Later but simpler gift leaks become a
redemption-code-leak case with loss-of-object (ownable).
[This case teaches depth: always test BOTH the data leak and the state-changing action.]

### 2.5 IDOR-057 — Vimeo: reset password for any account (title + summary evidence)

Title: "Vimeo.com Insecure Direct Object References Reset Password". Reporter body:
> "Please find a proof of concept for IDOR attack on famous vimeo.com. With this IDOR, attacker
> can reset any password, of any account and take controle of it."

Type: IDOR on "reset" requests where lookup was by user ID not by ownership. Recording here as
evidence — reports like *this* one usually carry the proof in attachments. No bounty disclosed.

### 2.6 IDOR-058 — Vimeo: private channel videos by parameter mutation (full)

Full body:
> "It allows an attacker to get unauthorized access to `Videos` of Channel whose privacy is set
> to 'Only moderators and people I choose' without being a member."

POST parameters — the tester identifies the widget URL and notes:
> "Go to ---> https://vimeo.com/tools/widget/montage (Use burp proxy and intercept the request)
> Now keep enumerating `badge_channel={any valid value}`, it will get you access to any videos."

**Also**: The video-carrying URL is a montage view of *any* user's channel-by-badge — i.e., the
user_id is whatever your session is, but the *channel* is not scoped to the principal. Accessing
the montage viewer with `badge_channel` mutations leaks any private-channel video.

### 2.7 IDOR-059 — Vimeo: forums object (full)

Full body:
> "Insecure Direct Object References. Dear Vimeo Team, i recently discovered a bug which allowed
> me to send comments in the forum in behalf on any user
>
> GET /forums/wanted_and_offered/topic:130606?comment_id=13010973&is_sticky=0&action=comment_edit_form"

"post/edit" as *another user* while holding a different user's session — parameter
`comment_id` mutation. (PDF attached in the report.)
[Post-2017: a comment id becomes a pseudo-token if you can post with someone else's account via
the edit URL; this is **write** scoping leak on `/edit_form` — should test ANY object endpoint
where the object id contains the owner id in the same full path.

### 2.8 IDOR-060 — Vimeo: read private comments by id-scoping (full)

Full body:
> "in combination with my previous bug i discovered [these bugs] ... get by using id-scoped
> references on a comment_" — a combination attack discovered on top of the forums bug.

### 2.9 IDOR-070 / IDOR-071 — Twitter/X: direct messages (full)

**IDOR-070 (52646)**:
> "I have access to deleted DM's. Once a DM is deleted a user/app will still be able to access
> the DM's using show DM endpoint ... When Sam DM's molly every DM gets a unique id like 123456
> and the DM can be accessed using the following API call,
> https://api.twitter.com/1.1/direct_messages/show.json?id={DM-id}"

**IDOR-071 (53858)**:
> "I found a way to access group DM's which i don't have access to, Conditions to be met:
> - Should have been in that DM group atleast once.
> ...
> But Eren can still access the DM's by just navigating himself to
> `https://mobile.twitter.com/a/messages/582225197727506432/delete` where 582225197727506432 is
> the DM id."

Two flakes:
- **Soft-delete scoping is a real class**: "deleted" hasn't really gone; both users can still
  read the DM. This touches GDPR/data-erasure and in-region deletion semantics.
- **Earlier membership defines access forever, unless the group itself was exited** —
  "should have been in that DM group at least once" is a soft membership check that the server
  does not re-verify on access. The server trusts a membership that no longer exists.

### 2.10 IDOR-073 — Twitter/X (translate.twitter.com): edit any comment (full)

Full body:
> "POC: https://translate.twitter.com/forum/getting-started/topics/7037/posts/43287/edit"

Direct object id path — then: the aleatoric post URL that the reporter uses. Waiting … the
reporter gives a parameter free URL — I saw "POC: [direct reveal path] /edit". **No bounty
disclosed.**

### 2.11 External blog URL — omarzzu: UUID pattern IDOR

Full blog body:
> "Upon examining the API request, I saw parameters like RequestId in the path and id in the JSON
> body. It became clear that the backend used UUIDs to identify user requests. I was curious if
> changing UUIDs could let me alter documents. So I created a second account, obtained its UUID,
> and tried updating it using my first account. I was able to do so, which indicated an IDOR
> vulnerability. However, since UUIDs are generally non-guessable, this might not be directly
> exploitable):
>
> But I didn't stop there. ... I noticed that all the UUIDs followed a specific pattern, such as:
>
> ```
> f6b168b5-A805-ef11-A832—005056066af7
> 13a6d3c4-Ab05-ef11-A832—005056066af7
> 972a6aad-Ab05-ee11-A832—005056066af7
> b542816d-Ab05-ef11-A832—005056066af7
> ```
>
> As you can see, all UUIDs followed the same pattern except for the **first segment**, which was
> variable. I was thrilled to discover that the UUID pattern was consistent across all accounts!"

> "Armed with this information, I could update any government document for anyone by simply
> guessing the first part of the UUID. And with no rate limits on the API, it made the process
> quite straightforward."

**Blog teaching** (which the modern playbook author highlights): **never** treat UUIDs as
unspoofable; the pattern *within* UUIDs frequently maps from a stable (often Microsoft-internal
GUID generation machine), so other-tenant ids are guessable. When the UUID has a static tail,
the UUID is **enumerable**; rate limits matter; this is *UUID-pattern-based IDOR*.

## 3. Workflow

1. **Test object references as you test each verb.** Try the same id on read, edit, delete,
   publish, and share; then on soft-deleted and group-exited versions.
2. **Discover the id surface**: URL paths, POST body, hidden form fields, JSON, custom headers.
3. **When an id is non-numeric**, try: prefix mutation, reproduce ordering, replace UUID
   positions, extension-like changes, null/empty ids, double-encoding, ...

## 4. Remediation

1. **Soft-deleted ≠ readable-by-others.** Verify that deleted objects reject or hide their data
   to *all* the parties that could read it once.
2. **Membership-loss semantics**: exiting a group must revoke access to its objects at the
   server, for every read path.
3. **Renew the id-scope each request** — don't rely on no-context id lookups.
4. **Do not rely on UUID entropy** — if UUID follows a Microsoft-internal mapping, one segment
   may enumerate; rate-limit and test for it.

## 5. Sources (verbatim)

| Case ID | Report | Evidence | Team | Weakness (assigned) | Title |
| --- | --- | --- | --- | --- | --- |
| IDOR-015 | [178506](https://hackerone.com/reports/178506) | full | instacart | Information Disclosure | Access private list metadata $100 |
| IDOR-041 | [115209](https://hackerone.com/reports/115209) | summary | uber | Improper Authentication | Unauthorized file (invoice) download |
| IDOR-042 | [127161](https://hackerone.com/reports/127161) | summary | uber | Information Disclosure | trips from other users |
| IDOR-043 | [119166](https://hackerone.com/reports/119166) | full | udemy | Improper Authentication | view others' gifts … |
| IDOR-057 | [42587](https://hackerone.com/reports/42587) | full | vimeo | Improper Authentication | IDOR reset password |
| IDOR-058 | [45960](https://hackerone.com/reports/45960) | full | vimeo | Privilege Escalation | private channel videos |
| IDOR-059 | [52176](https://hackerone.com/reports/52176) | full | vimeo | Improper Authentication | forums object |
| IDOR-060 | [52181](https://hackerone.com/reports/52181) | full | vimeo | Improper Authentication | read private comments |
| IDOR-070 | [52646](https://hackerone.com/reports/52646) | full | x | Improper Authentication | deleted DMs |
| IDOR-071 | [53858](https://hackerone.com/reports/53858) | full | x | Privilege Escalation | group DMs |
| IDOR-073 | [181748](https://hackerone.com/reports/181748) | full | x | Privilege Escalation | translate.twitter.com edit any comment |
| (blog) | omarzzu | full | (gov portal, redacted) | — | UUID pattern IDOR |

External blog: [omaralzughaibi.com/javascript-analysis-uuid-pattern-idor](https://omaralzughaibi.com/blog/javascript-analysis-uuid-pattern-idor)
