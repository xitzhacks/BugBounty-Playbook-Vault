---
title: "Invocation-Layer Attacks: Mass Assignment & Secondary-Implementation Access Control"
type: playbook
category: invocation
cwe: "CWE-915 (Improperly Controlled Modification of Dynamically-Determined Object Attributes); CWE-285"
case_ids: "IDOR-063, IDOR-064, IDOR-065, IDOR-036, IDOR-038, IDOR-031, IDOR-009; external: mass-assignment blogs"
sources: "4 H1 + 3 external sources"
evidence_split: "4 cases: full 4; 3 external blogs full"
archive_accessed: "2026-10-16"
---

# Invocation-Layer Attacks: Mass Assignment & Secondary-Implementation Access Control

## 1. Overview

Two structurally different but behaviorally similar classes collected under one playbook, both
being **"the authorization is checked in one implementation layer only"** cases:

1. **Mass assignment** (CWE-915): a model binder accepts fields the developer never intended
   user-controlled, and a privileged flag rides in with the rest of the object.
2. **Secondary-implementation / client-side-control bypass** (often miss-categorized): a
   check enforced on one route or one app client is absent on the second path or second client.

Mass assignment is *not* an IDOR, but in this corpus it is the highest-bounty single *form* of
"you authorized what I told you to authorized" and is tested together with object-level
authorization because the same machine (an HTTP request that *binds many fields*) is being
probed.

## 2. Case studies (verbatim)

### 2.1 IDOR-064 — wakatime: change another user's leaderboard owner name

Full body:
> "I would like to mention a bug here that is regarding changing the name of the owner of a
> **private leaderboard**... via an API"

The tester had a *different* leaderboard (their own) — they relabelled the private-leaderboard's
owner name on another user's leaderboard. Same-server check existed and rejected one route, but
there was another request-level change path.

### 2.2 IDOR-063 — wakatime: create accounts tied to another user's e-mail (full)

Full body — the report approaches a **user-verification** endpoint:
> "I'm able to create accounts with the email verification that originates from the first account
> I created. After changing the confirm_email request body to a different email.. After I use
> that verification link that account is now under my control and bypasses authorization."

> "POST body:
> ```
> {"email":"███████"}
> ```"

Two lessons:
- **Verification links and account-binding tokens** aren't a *write-only* surface — they must be
  checked against **who currently holds them**. Here, test A's token plus test B's email =
  A's right.
- The second-half of the attack — "the account is now under my control" — escalates to *identity
  theft* even though the reviewer may have been shown a plain, non-privileged-actor bug.

### 2.3 IDOR-065 — wakatime: parallel "session duplication" (full)

Full body:
> "Due to improper validation of user before generating an API-KEY and improper measures taken at
> the time of password reset, **it is possible to generate a parallel session at the attacker's
> end.**
>
> Steps to Reproduce
> =============
> Attacker
> ---------
> - Create an account with victims email.
> - Download the coding platforms and get API-KEY.
> - He can code from the platforms using the victims API-key."

Half the case (Attacker) plus half (Victim) together create a *dual identity* bug same-user,
multiple-sessions style — a form of*session duplicationのある here the invocation layer
(API-KEY) has an auth-bypass on a *pre-registration* path.

### 2.4 IDOR-036 / IDOR-038 — Shopify: see Stale-Permission playbook

Both are secondary-implementation access-control issues (restricted role allowed via secondary
client-sub-URL). Already covered there; listed here for cross-reference because the tests are
identical in execution to form-field / parameter-mutation cases.

### 2.5 BLOG-006 — HoyaHaxa: Adobe ColdFusion CVE-2023-44350

Full blog body (external; modern-era). Adobe exposed its `argumentCollection` feature in ColdFusion; passing
a nested structure like:
```json
{"Application":{"env":"development"}}
```
sets **any variable scope** inside a remote CFC method. The blog author's summary:

> "A mass assignment vulnerability occurs when application code **allows a user to set or modify
> arbitrary objects or values without verifying that the user is authorized to do so.** ...
> If an attacker is able to control values related to sensitive actions such as access control,
> **authentication, and authorization**, he may be able to break the assumed logic and program
> flow with devastating results."

The test demonstrates the subclass: remote-CFC-functions route an `Application` scope value
from a URL parameter into the CFC's own ACL decision.

### 2.6 BLOG-005 — Rails mass assignment explainer (medium.com / jaeger.rob)

Full blog body. The author shows the *mechanics* of Rails mass assignment:
> "e.g., PATCH `http://localhost:3000/users/1?user[name]=NewName`"
> "I changed my controller to use strong parameters for the user's name only."

 teaches the modern-classic rules:
- `protect_from_forgery with: :exception` is the actual CSRF shield; for **APIs** being a
  separate context, use `:null_session` and **always bind white-listed params**.
- `ActiveModel::ForbiddenAttributesError` is thrown when param-binding is done poorly.

### 2.7 BLOG-003 — omarzzu₂ (omaralzughaibi): path normalization / mid-authoriz bypass

Full blog body:
> "So, we constructed the reset password request **without the [Authorization] header**. ...
> It worked — the access control was bypassed."
> "## Root Cause: Authorization Handler Logic Flaw
> - When the Authorization header was present, proper role checks were performed.
> - When the header was missing or empty, the **handler failed to enforce access control**,
>   allowing requests to proceed unauthenticated."

This is the *inverted* element from §1: the arrow inverted here is not that *the tester gained*
extra rights, but that the server **assumed authentication was enough** and dispatched the
request to the controller anyway.

Also shows **path normalizer disagreement**:
> "We crafted the path using a backslash:
> - `/updatePrice\\` appeared different to the middleware
> - Backend normalized the path to `/updatePrice`
> The middleware skipped validation, while the backend processed it correctly."

**Result:** "we were able to set the refund value to any amount" — the "refund manipulation"
chained on top of a "full admin takeover" (abusing an invitation flow — also bypassed by
removing the Authorization header).
This chained bug series shows that in modern APIs, invocation-layer authorization is *often*
interposed by a middle-layer system and that the "Authorization Header was absent" and
"Authorization Header path was different" cases both bypass the check.

## 3. Workflow

1. **Inventory every field your account has** (profile, admin UI role, config flags).
2. **For each, list any *model-binder* endpoint** that accepts *either* your field OR another
   user's fields as a separate nested key, and any that accept "config-like" data.
3. **Bind a privileged field against your own** account: e.g., `role`, `plan`, `is_admin`,
   `verified`, `domain`, etc. Expect to notice any 2xx response and what changed.
4. **Re-run every test with batched flag absence/presence** (omitting Authorization headers) as
   the check knob.
5. **Where a router framework normalizes paths**, fuzz a *slightly-wrong* path segment each way
   (`\`, `//`, `%2F`, `%20`, triple-slash, trailing `.`).

## 4. Remediation

1. **Never implement role check inside the Authorization-header presence check**; every request
   must carry both authentication and a single-role authorization decision.
2. **Finish denienieiff-decline**: if the header is *missing* or *empty*, do not "default-allow".
   Fall to "deny".
3. **Normalizing the path is not enough** — the ACL must run against the *normalized* path, and
   the router must use the *same* normalized value.
4. **Mass assignment: use parameter allow-lists** in every binding; parameter white-lists are
   not merely theoretical — one PR protects an entire class.
5. **Never bind to higher-privilege models an arbitrary field set**; bind to the *one* model the
   method intends to modify.

## 5. Sources (verbatim)

| Case | Source link | Evidence | Priority |
| --- | --- | --- | --- |
| IDOR-064 | [245340](https://hackerone.com/reports/245340) | full | medium |
| IDOR-063 | [244636](https://hackerone.com/reports/244636) | full | medium |
| IDOR-065 | [247225](https://hackerone.com/reports/247225) | full | low |
| IDOR-036 | [95589](https://hackerone.com/reports/95589) | full | medium |
| IDOR-038 | [154410](https://hackerone.com/reports/154410) | full | medium |
| IDOR-031 | [92481](https://hackerone.com/reports/92481) | summary | medium |
| IDOR-009 | [85720](https://hackerone.com/reports/85720) | full | medium |
| BLOG-006 | [hoyahaxa — ColdFusion CVE-2023-44350](https://www.hoyahaxa.com/2023/11/critical-variable-mass-assignment.html) | full | modern |
| BLOG-005 | [Rails Mass Assignment Explainer — Robbie Jaeger](https://medium.com/@jaeger.rob/exploring-rails-mass-assignment-vulnerability-b8b3d19e20b6) | full | fundamentals |
| BLOG-003 | [Path Normalization Beats Middleware — Omar Alzughaibi](https://omaralzughaibi.com/blog/path-normalization-authorization-bypass/) | full | modern |
