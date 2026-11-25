---
title: "IDOR Testing Playbook — Agent Execution Protocol"
type: playbook
execution: agent
version: 1.0
date: 2026-10-17
evidence_base: "73 public HackerOne reports (13 programs) + 5 external blogs"
date_range_of_cases: "2014-03 .. 2017-09-12 (archive frozen); blogs 2016-2025"
source_index: references/source-index.md
category_playbooks: [Cross-Tenant-Object-Level.md, Stale-Permission-and-Own-Action.md, Role-Scoping-and-Vertical-Escalation.md, ID-Scoping-and-Predictable-IDs.md, Parameter-Gate-and-Hidden-Functions.md, Invocation-Layer-Mass-Assignment.md, Enumeration-and-Financial-Objects.md]
---

# IDOR Testing Playbook — Agent Execution Protocol

## 0. How to Use This Document

You are an agent performing **authorized** access-control testing (IDOR / BOLA). This document
is your procedure. It is written as phases; each phase states an **Objective**, its **Inputs**,
the **Actions** to take, the **Output** you must produce, and a **GATE** you must pass before
continuing.

**Protocol rules — non-negotiable:**

1. **Never skip Phase 0.** If authorization is not confirmed in writing, stop and say so.
2. **Never skip a GATE.** A failed gate means go *back*, not forward. Most rejected IDOR reports
   fail a gate that was skipped.
3. **Never claim what you did not observe.** If you did not capture the request and response,
   you do not have a finding. Write "Not observed" — never infer.
4. **Prefer the least-destructive proof.** Read before write, write before delete. Report the
   strongest true claim, and only that claim.
5. **Cite evidence.** Every claim needs a raw HTTP request/response pair or a screenshot of a
   before/after state.
6. **State the identity pair.** Every IDOR claim must name *two* principals: whose session you
   had, and whose object you touched. This is not optional.

**Notation:** `→` is a control-flow step. `GATE n` blocks on failure. Commands are templates;
substitute real values.

---

## Phase 0 — Intake and Scope Validation `GATE 0`

**Objective.** Establish that you are permitted to test, and what "permitted" covers.

**Actions.**

1. Read the program's policy. Record: in-scope assets; out-of-scope; forbidden methods; whether
   rate limits are explicit; whether *state-changing PoCs* are allowed. Many programs
   explicitly restrict DELETE / purchase / fund-transfer PoCs — record that before you design
   them. (Corpus evidence: DoD cases IDOR-005..008 tested modification; other programs
   discourage destructive steps.)
2. Match each target against the in-scope list; record the exact in-scope entry.
3. **Enumerate prior art.** The program's list of already-known bugs matters more for IDOR than
   for other classes — multi-user flows are big and other researchers test them continuously.
4. Note whether you may create test accounts and, if so, how many; and whether you may test as a
   limited-permission user.

**Output.** Scope table: `target | in-scope basis | accounts allowed | destructive PoC? | prior art`.

**`GATE 0`** — all false ⇒ stop. If not every target is in-scope, drop it and say why in the
report.

> **Evidence note.** In the corpus, 299 archive-listed IDOR-class reports no longer resolve
> (404). Prior art can disappear; it must be checked *at test time*, not from archive.

---

## Phase 1 — Attack Surface Mapping `GATE 1`

**Objective.** Inventory every identity, every object reference, and every action the
application exposes.

**Actions.**

1. **Map principals.** You need *at least two accounts per role you intend to test* plus, when
   possible, one admin and one restricted-staff principal. Corpus distribution:
   shopify (13 reports) and veris (12) each needed merchant/admin; instacart needed a buyer and
   a *shopper* agent; GitLab needed ordinary jane + a private group owner; algolia needed two
   levels (`Search`-only plus `Search`-plus-signature).
2. **Map every object reference** the system uses:
   - **Numeric IDs** (27 of 73 corpus cases tested them — instacart `list_id`, veris
     `terminal_id`, udemy `giftId`, shopify `subject_id`, gsa `siteid`).
   - **UUIDs** (13 cases; omarzzu demonstrates UUID-partial-pattern exploitability;
     hacktus proves the "obfuscated" key can still leak).
   - **Composite keys or path-segment references** (`/sites/<siteid>/builds`, brickftp `path=...`,
     ads.twitter `blobstore_path`, fabric `organization/<id>/mopub/activate`).
   - **Leaked/token-scoped references** (hacktus: pre-signed URL leak — an id isn't the reference
     if a URL exists that carries the access with it).
3. **Walk the mobile app separately from the web app** — Nextcloud IDOR-018 was an
   Android-only path; server-side ACL must not differ per client, but the bug may surface only
   in one.
4. **Catalogue every *action*, not just reads** — per the corpus, write/delete cases are ~40%
   (44/73): DELETE (veris), transfer/activation, expire-session, edit-a-public-comment.
   Actions that don't *look* like data leaks (IDOR-013 restart build; IDOR-027 expire
   sessions) are severity-equal to leaks in practice.
5. **Catalogue "hidden function" surfaces**: `/api/` alternate of `/`, `/json` variant,
   admin subdomain, partner-specific app path, RSS/RTE asset endpoint. These are where
   access control is most often missing (see Parameter-Gate playbook, IDOR-024, IDOR-010).

**Output.** `surfaces.md` — tables of principals, object references, actions, hidden surfaces.

**`GATE 1`** — you must have (a) ≥2 testable principals, (b) ≥5 distinct object references, and
(c) ≥2 hidden-function surfaces. If any is missing, go back and enumerate more.

---

## Phase 2 — Reflection & Reference Discovery `GATE 2`

**Objective.** For each reference, determine where and when the application exposes data about
*other* object instances.

**Actions.**

1. **List every field your request contains** for each action; then identify *which* of those
   the server *derives* the object from.
2. **Establish baseline.** Record the 200-response for *your own* object on every reference.
   Two data points:
   - Same response but *with* the object's data ⇒ check applied and returned data.
   - Same response but *without* object data ⇒ ownership was checked and data hidden — the
     second means your test space exists but with different function shape.
3. **Compare request-bound reference vs response-bound reference.** Corpora history:
   on the Uber *invoice* case (IDOR-041), the client passes a UUID (authorization carrier) but
   accommodation *by number* surfaced data response.
4. **Identify references that *carry* privileges with them** (algolia `signature`, wakatime's
   `confirm_email/<uuid>`, pre-signed URLs from hacktus). Those references must be tested in *the
   same "who sent it" way as credentials*.
5. **Check every redirect param** for 302-to-foreign-id differences.
6. **Check OPTIONS/method versions of each reference**; method descriptors can differ — see
   IDOR-073 (edit route) vs IDOR-059's own-action (edit-vs-delete routes).
7. **Record rate limits / pattern-of-block behavior** per reference — the rate limit may be
   the only line of defense you're testing against (starbucks IDOR-040, veris read enumeration,
   and the "no rate limits" omarzzu₂ case).

**Output.** `references.csv`: `ref | verbs it accepts | source of ref (form/URL/JSON/mobile) | own-object 200 response | non-owned 403/404 | ref carries auth? | rate-limited?`.

**`GATE 2`** — every object reference has: verbs, a tested baseline (200), at least one foreign
test result, and rate-limit status. Missing columns⇒ back up.

---

## Phase 3 — Route Selection `GATE 3`

**Objective.** Choose the correct playbook for each confirmed object-reference.

Selection: **one route per finding.** Match by what has been confirmed:

| Confirmed result ⇒ playbook | Skip to |
| --- | --- |
| Read/write/delete an object that belongs to *another tenant/principal* — by swapping id/uuid/path | **Cross-Tenant-Object-Level.md** |
| Action succeeded *because you remembered having the right earlier*, or you used a *permission you never had* — downgraded-in-flight | **Stale-Permission-and-Own-Action.md** |
| A *same-tenant, different-role* object was reachable — you, a low-privilege-role user, reached something a manager-admin role should guard | **Role-Scoping-and-Vertical-Escalation.md** |
| Semantic scoping leaked: the id used is itself the *pointer to the tenant*, is a "soft-deleted" version, or a leaked UUID | **ID-Scoping-and-Predictable-IDs.md** |
| Hidden function, unlinked action, parameter toggle, path normalizer disagreement | **Parameter-Gate-and-Hidden-Functions.md** |
| Mass assignment or missing/empty Authorization header | **Invocation-Layer-Mass-Assignment.md** |
| Enumeration of a *financial* object (card, PIN, gift code) or the only defense was rate-limiting | **Enumeration-and-Financial-Objects.md** |

Ambiguity: report the class you think it is *and* the next-best class; when in doubt, both may
apply. Use the *narrower* class in the title.

**`GATE 3`** — one route chosen for each finding; the finding cannot be routed if no object level
was actually crossed.

---

## Phase 4 — Escalation Ladder `GATE 4`

**Objective.** Establish the **strongest true claim**, no stronger.

Ladder rungs; **stop at the first that succeeds**; report the reached rung.

| Rung | Probe | Establishes |
| --- | --- | --- |
| 0 | text-only reflection of foreign id | reference exists |
| 1 | Read foreign object (GET or list) | **cross-tenant read** |
| 2 | Write foreign object (POST/PATCH to `name`, `note`, etc.) | cross-tenant write |
| 3 | Delete/modify-state of foreign object (DELETE, restart, expire) | cross-tenant destructive |
| 4 | Record *privilege reach* — you as junior reach functionality that should be manager/admin | vertical escalation |
| 5 | Show *financial/token transfer* — money, gift code, PIN, card | fraud-capable severity |
| 6 | Impact quantification: the object can be iterated (rate limit absence) or serialized (bank-level) | scale impact |

**`GATE 4`** — the statement you are about to make must be exactly:
*"Principal `<A>` (session of `<role>`), acting via `<endpoint>`, reached object `<owned by B>`
(success state: 2xx / data present / state changed)."* With every element observed. Without the
A/B pair, the finding is un-usable.

---

## Phase 5 — Validation and Triage `GATE 5`

**5.1 Gates — all must pass:**

| # | Gate | Fails if |
| --- | --- | --- |
| V1 | Two-principal identity stated | You did not show *who* sent and *whose* object (main reason for rejection) |
| V2 | Real response captured | You inferred "this should work" without the response body |
| V3 | Correct route/verb | You sent it via the wrong verb, or sent a different action |
| V4 | Feature-access vs object-access stated | You did not distinguish whether the flaw is *feature-level* or *ownership-level* |
| V5 | Minimal PoC | You attempted a destructive transfer when a read was sufficient |
| V6 | Rate limit tested | You did not report the rate-limit status — if the limit defends the bug, say so |
| V7 | Alternate routes checked | You did not test the equivalent route (json / api / mobile / secondary app) |
| V8 | Prior art checked | You did not check the program's public list |
| V9 | Authorization material handled | You were still holding a token a teammate shared (algolia `signature`) |
| V10 | Verbs differentiated | You did not check the same reference on GET/POST/PATCH/DELETE |
| V11 | Evidence linked | Screenshots + HTTP dumps attached; not just a story |

**5.2 Common false positives — check each explicitly:**

- ❌ **"500 error = success"** — server-side crash is NOT a granted access.
- ❌ **Same response different format** — all-2xx responses to *different* actions can be a
  *rate-limiting* defense, not an ACL (compare response *bodies*, not status). Preferred check:
  match boby response content encoding.
- ❌ **Object-of-same-principal** (marked "same-user-same-owner") — test ownership *and*
  cross-tenancy; the same object via a *different session* must return the same *denial*
  verdict. If it doesn't, the bug is a *session* bug, not object-level.
- ❌ **Auth-carrying identifier** — an object reference that *carries* authorization (pre-signed
  URL, signature, `confirm_email/<uuid>`) must be tested as *who held the identifier*, not
  who tested it.
- ❌ **Prior-art/known confirmed** — before writing, check: has the program already accepted it
  in sweeten hits? Review your *title wording* against the accepted-bug list.

**`GATE 5`** — all V1..V11 must pass. Document each in the report; a failed gate kills the
report.

---

## Phase 6 — Severity Determination

**Severity is set by two variables, not by the payload:**

1. **Who executed the action?** (their role, and what they could have reached without it)
2. **What is the object boundary?** (tenant vs role vs feature)

**6.1 Anchors from the corpus (recorded values, not recommendations):**

| Case | Action | Recorded severity / bounty |
| --- | --- | --- |
| IDOR-014 (instacart) | Read other customer's **chat logs** | $100 |
| IDOR-001 (algolia) | Information disclosure + query log read from all indexes | $400 |
| IDOR-024 (HackerOne) | Ticket-bombing via ticket invite link | $500 |
| IDOR-025 (HackerOne) | Invited-user access (mediation link) | $500 |
| IDOR-010 (brickftp) | **Read foreign files including same-prefix file dump** | $600 |
| IDOR-034 (shopify) | Cross-shop hidden-object leak | $2500 |
| IDOR-030 (shopify) | Cross-tenant **any customer's name** | $2500 |
| IDOR-032 (shopify) | Cross-tenant collections | $2000 |
| IDOR-027 / IDOR-028 (shopify) | State-change (expire session); cross-shop via app $1000 | $1000 |
| IDOR-040 (starbucks) | Fraud-capable card+PIN | none disclosed |

Drivers, derived: **who** can do it, and **at what boundary**. "Junior can reach manager-only"
is the least severity; "any tenant reads any tenant" is the highest. Alibaba's
"same-functionality app *almost* identical bugs" (IDOR-001 vs IDOR-033) show that a *signature*
being held by a low-privilege role vs a *missing self-role check* produce severity $400 vs $500.

**6.2 Requirements:**

1. **State the viewer explicitly**: name the *role* that can trigger this and the *privileged*
   role that should have blocked it.
2. **Name the object boundary**: cross-tenant, cross-role, same-role feature.
3. **Only claim what you walked.** Chained impact (leak ⇒ takeover) must be demonstrated in
   your session or cite a report that did it: omarzzu (leak ⇒ JWT ⇒ admin takeover) is the
   canonical modern chain reference.
4. **Disclose your cookie / Authorization-header state**: if you were *authenticated but
   unprivileged*, say so — this is the whole class.
5. **Published metrics only where a source publishes them**: the corpus contains no CVSS
   severity; do not compute CVSS unless the vendor publishes.

---

## Phase 7 — Reporting

**Required elements, in order:**

1. **Title** — describe the class and the boundary: `Cross-tenant read at <endpoint>` (not
   "IDOR" alone). Add **the two principals** as text (e.g., "userA fetches userB").
2. **Summary** — endpoint; principal A's role; principal B's object; action; security impact.
3. **Repro steps with exact commands** — one request to prove A's *own* baseline, one to prove
   B's object is reachable, one to prove the state changed if you claim destructive damage.
4. **PoC details** — dump HTTP requests *and* responses verbatim; do not narrate.
5. **Impact with quantification** — counts (`all installs' invoices`, `all users' cards`).
   From the corpus: IDOR-013 (gsa) shows the *impact* is quantified by the count of affected
   accounts (single site), while IDOR-040 has *fraud capability* impact that is
   pseudo-quantified from one probe.
6. **Rate-limit status** — enumerate what defends it; this is the reviewer's first question on
   an enumeration finding.
7. **Suggested fix** — object-level authorization at the tenant or role boundary; a request to
   fix at the wrong level (UI-only) is the most common misleading report.
8. **Environment** — browser + version, endpoint, date.

**(Evidence-Base note)** For a continuous study on *what to report*, the **detailed** templates
in the category playbooks (`Cross-Tenant-Object-Level.md` §8, `Parameter-Gate…` §5) matter more
than the short form here.

---

## Phase 8 — Remediation Alley

**The fix pattern you should recommend (from corpus)** — context-correct, at the boundary *of
the object*:

| Flaw confirmed | Fix |
| --- | --- |
| ID swapped (cross-tenant) | `WHERE owner = current_principal OR is_shared(current_principal)` at every route; not just the feature page |
| Api-level route bypassing UI | Same ACL function on every route/`content-type`/method; not separately in UI logic |
| Hidden route (unlinked admin list) | Authorization middleware for every route, and a test for *every* route |
| Parameter gate skipped | The parameterized call must repeat the ACL; never treat a second client as a different identity |
| UUID pattern leak | Non-sequential UUIDs must use cryptographic randomness; even with crypto-random, object-level authorization must remain |
| Invocation-layer | Every authorization decision must bind `principal + verb + object + boundary`, not the presence of a header |

---

## Phase 9 — Post-Reporting `GATE 6`

1. **Reproducibility check.** A different researcher reading the report must be able to run it
   without contacting you.
2. **Sibling objects test.** Test where the same object goes; one object per endpoint and one
   related list per principal (the veris pattern: 12 reports on one engine). Reports that test
   these, batched and a single sponsor recommendation (object-level authorization at the
   tenant/role boundary), are *more* valuable than 12 individual reports.
3. **File regression suite**: for each finding, verify the *same request as your own role*
   still succeeds, so fix-affecting changes don't break legitimate user flows.

**`GATE 6`** — When you have delivered, exit. Do not let the gate pull you into a discussion in
which the object-level credential is still held against you.

---

## Appendix A — Object-Reference Cheat Sheet

| Reference type | Typical exploit shape | Corpus cases |
| --- | --- | --- |
| Sequential integer id | Change id; range-scan to reach sibling objects | IDOR-014, 015, 043, 046-056, interpretation |
| UUID | If guessable by pattern (omarzzu₂) | IDOR-041 (UUID); |
| path-segment (`/sites/<id>`) | Change segment; cross-tenant write | IDOR-013 (gsa FBI restart build) |
| File path | Change path; prefix matching trick | IDOR-010 |
| Pre-signed / token-carrying URL | Use the URL then treat re-scope with different actor | hacktus (BLOG-001); Uber IDOR-041 |
| Enumeration-validated (e.g., `Register.MyCard`) | Parameter toggles validation path | IDOR-040 |
| Object-tyned response hides foreign | jsonResponse key is foreign id; enumerability varies | IDOR-041, IDOR-030 |

## Appendix B — Verb-testing Table

| Method | On the same object reference |
| --- | --- |
| GET | read; query params often unfiltered |
| POST | create/act; object may be referenced by id in body or URL |
| PATCH/PUT | modify; frequently uses same object id |
| DELETE | remove; often forgets scope |
| OPTIONS | method surfaceIAM |

**Remember:** *the bug is usually in the least test-invested verb.*

## Appendix C — Evidence Base and Its Limits

Derived from **73 public HackerOne reports** across **13 programs** and **5 external blogs**, all
retrieved 2026-10-16. Archive frozen at **12 September 2017**.

| Evidence level | Reports | Meaning |
| --- | --- | --- |
| Full researcher body | 55 | Complete reproduction happens here |
| Program's official summary only | 18 | Body withheld, but the program's own disclosure exists |
| Title-only | 0 | None: every case has body or summary |

**Limits you must respect:**

1. **All H1 cases predate 12 September 2017.** Pre-2017-era tools and taxonomies: BOLA, BFLA
   didn't exist as terms; reports categorize as "Improper Authentication - Generic",
   "Privilege Escalation", "Information Disclosure", "Insecure Direct Object Reference (IDOR)".
   Treat as historical evidence of *method*, not as names. Modern OWASP API Top 10 (BOLA/BFLA)
   has the same underlying flaw.
2. **There are no automatic scanners.** All 73 cases were manual — there was no single
   dynamic-scanner bug. The commonly tested iOS/Windows case IDOR-052 also found this.
3. **Programs-specific severity is not comparable across programs.** The $2500 Shopify payouts
   should not anchor a $250 expectation elsewhere.
4. **No post-2017 techniques in the H1 bodies.** Trusted Types, MV3, SAML-assertion-format
   issues, API-gateway state handling, OpenSearch-style *modern* BOLA are not in the H1 archive.
   The odyssey on IDOR techniques continues in the 5 external blogs (2016-2025).
5. **299 archive-listed candidates returned HTTP 404** and could not be retrieved; they are
   recorded in `idor_candidates_titles.json`, not reconstructed.

---

## Appendix D — Quick Reference: One-Page Run Card

```
0  AUTHORIZE ............. gate: in-scope per target, accounts allowed
1  MAP ................... principals, object refs, verbs, hidden surfaces
2  REFERENCE DISCOVER .... baseline own-object 200; foreign result per verb
3  ROUTE ................. gate: which playbook class (route per finding)
4  ESCALATE .............. gate: A/B principals stated; strong evidence
5  VALIDATE .............. gate: V1-V11, incl. rate limit + alternate routes + app/client variants
6  SEVERITY .............. role & boundary; quantification; no CVSS invention; prior-art checked
7  REPORT ................ class+boundary in title; steps + full dump; role + object named
8  FIX ................... object-level authorization per class in Appendix table
9  SIBLINGS .............. same pattern across every route/method+verb
10 DONE .................. gate: someone else can reproduce without you
```

**Three rules that decide most outcomes:**
1. **Name the two principals.** Without A-who and B-whose, a reviewer can't tell an IDOR from
   noise.
2. **Test every verb** for the same object reference; your read-only test has a write twin
   (IDOR-046 "delete any group of any organization" vs IDOR-050 "get terminal data" — same
   object family, two languages).
3. **Test the second implementation** — `/json`, alternate API, mobile app path, admin
   subdomain. Many cases in this corpus are "route A denies, route B allows".

---

*Compiled 2026-10-17 from 73 public HackerOne IDOR-class reports (19 bounty totals
$14,470) and 5 external blogs. Archive last updated 2017-09-12; archive accessed
2026-10-16.*
