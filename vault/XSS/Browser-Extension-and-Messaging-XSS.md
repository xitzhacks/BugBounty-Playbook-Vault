---
title: "Browser Extension and Messaging XSS"
type: playbook
category: browser-extension-and-messaging-xss
cwe: "CWE-79", "CWE-346"
source_count: 8
full_bodies_available: 8
summary_only: 0
archive_accessed: 2026-10-12
---

# Browser Extension and Messaging XSS

## 1. Overview

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

## 2. Root Cause and Technical Mechanics

### 2.1 Extensions as a DOM-injection source

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

### 2.2 `postMessage` — origin validation and data shape

`DOM-018` (`231053`, Shopify, $3,000) is the most instructive. Full case study in
[`DOM-Based-XSS.md`](DOM-Based-XSS.md) §11; the mechanics are summarised here because
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

### 2.3 Embedded SDKs — the trust boundary is the app, not the user

`BROW-008` (`217745`, Shopify, high, $800) and `FRAM-004` (`217790`, Shopify, high,
$1,000`) both concern the **Embedded App SDK**, where a malicious *installed app*
gains execution in the store admin's session.

`BROW-008`'s root cause: *"Buttons can define an `href` parameter which will open when
the button is clicked. The `href` parameter is not properly sanitized allowing a
malicious app to execute JavaScript in the context of the admin interface."* The
`clickButton` method passes `data.href` to `Page.visit(href, {reload: true})` with no
scheme validation — the same "URL field without a scheme allow-list" defect as
[`Self-XSS.md`](Self-XSS.md) `SELF-021`, but across a **trust boundary**.

The reporter also opened by cross-referencing, which is the correct practice:

> "This report is similar in impact, exploitability and root-cause as report #205701
> requiring an additional step of user-interaction."

### 2.4 Third-party embeds that fetch attacker content

`BROW-007` (`191909`, Discourse, high, $256) is an **image-link parser** failure:

> `http://host/path/to/image'onerror=alert(1);//.png`
>
> "We have an invalid image URL which finish with an image extension (PNG). By putting
> the `'` we are able to break the `img` tag in which the image url is included by the
> parser and add custom code, allowing us to run Javascript code. A malicious user
> could use the `$.getScript` function to load a malicious script."

A markdown image parser that validates the *extension* but not the *quote characters*
is a parser differential — the same family as
[`Filter-Bypass-and-Encoding.md`](Filter-Bypass-and-Encoding.md) §2.3.

## 3. Attack Surface and Preconditions

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

## 4. Manual Testing Methodology

### 4.1 For extensions you own

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

### 4.2 For `postMessage` listeners you own

1. **Find every listener** in your codebase and in shipped bundles.
2. **Check for `event.origin` validation** *before* any use of `event.data`.
3. **Probe with a non-matching origin first** — if a listener responds, origin
   validation is absent.
4. **Probe data shape.** Send: a string, an array, an object, a nested object, and
   objects with `toString`/`valueOf` overrides. A sanitiser that only handles strings
   is bypassable (`DOM-018`).
5. **Confirm the coercion step** — the fix is `String(event.data)` (or the expected
   type) *before* sanitising, not after.

### 4.3 For embedded apps and SDKs

1. **Establish that you can install a malicious app** on a target — otherwise the
   finding is out of scope.
2. **Enumerate every SDK method** that renders a value or accepts a URL.
3. **Test `href`-like parameters for scheme validation** (`javascript:`, `data:`,
   `vbscript:`).
4. **Test whether any value reaches a template engine or a DOM sink** — see
   [`Framework-and-Template-XSS.md`](Framework-and-Template-XSS.md).

### 4.4 For markdown / link parsers

Test that the parser validates the **whole construct**, not just the extension:
`'`, `"`, `<`, `>`, `)`, spaces, and `javascript:` inside the URL part.

## 5. Input and Output Context Analysis

| Context | Case | Break-out |
| --- | --- | --- |
| Extension writing remote text into the page | `DOM-016` | `a'"><h1`, `'"><img src=x onerror=` |
| Extension reading `location.hash` | `BROW-004` | `#<img src=x onerror=alert(1)>` |
| `postMessage` → sanitiser → DOM | `DOM-018` | clone-able object defeats escaping |
| SDK `href` → `Page.visit()` | `BROW-008` | unsanitised `href`, e.g. `javascript:` |
| SDK modal input → lodash/twine | `FRAM-004` | `data-define` attribute re-parsed |
| Markdown image `src` → `<img>` tag | `BROW-007` | `'onerror=…` before a `.png` extension |
| Served file, inline, trusted host | `BROW-006` | `.jpg` path renamed to `.html` |

## 6. Test Cases and Proof-of-Concepts

### 6.1 Historical payloads (verbatim from the cited reports)

| Case | Report | Payload / technique |
| --- | --- | --- |
| DOM-016 | `220494` | search GitHub for `'"><img src=x onerror=` and `a'"><h1` |
| BROW-004 | `119453` | `https://www.veris.in/?#<img src=x onerror=alert(1)>` |
| BROW-007 | `191909` | `http://host/path/to/image'onerror=alert(1);//.png` |
| DOM-018 | `231053` | clone-able object bypassing the postMessage escaping |
| BROW-008 | `217745` | unsanitised button `href` in the Embedded App SDK |
| BROW-006 | `191380` | remove `:large` from the image URL, append `%23.html` |

### 6.2 Newly authored illustrations (not from the archive)

**Extension DOM-write audit** (newly authored; run on your own extension):

```bash
# newly authored
grep -rnoE "(innerHTML|outerHTML|insertAdjacentHTML|document\.write|\.html\()" src/
```

**`postMessage` origin/shape probe.** Newly authored. Serve from a page you control:

```js
// newly authored — send to a target window
const w = window.open('https://TARGET/');
const probes = [
  'H1XSSMARKER9',                                  // plain string
  ['H1XSSMARKER9'],                                // array
  { toString: () => 'H1XSSMARKER9' },              // object with toString
  { a: { b: 'H1XSSMARKER9' } },                    // nested object
];
for (const p of probes) w.postMessage(p, 'https://TARGET');
```

If the target renders the marker as an **element** rather than as text, the escaping is
shape-dependent.

**SDK `href` scheme probe.** Newly authored:

```
javascript:alert(1)
javascript://alert(1);%2f%2f@
data:text/html,<h1>xss-marker
vbscript:msgbox(1)
```

**Markdown image parser probe.** Newly authored:

```
![x](http://h/i'onerror=alert(1)//.png)
![x](http://h/i"onerror=alert(1)//.svg)
![x](javascript:alert(1))
![x](<http://h/i onerror=alert(1)>)
```

**Safe proof.** Prefer `document.title='marker'` or a collaborator callback over
`alert(1)`. For `DOM-016` the researcher deliberately used inert search terms for the
HTML-injection stage before demonstrating execution.

## 7. Encoding, Filtering, and Parsing Behavior

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

## 8. Impact and Severity Considerations

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

## 9. False Positives and Limitations

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

## 10. Remediation and Regression Testing

### 10.1 Remediation

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

### 10.2 Regression tests

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

## 11. Historical Bug Bounty Case Studies

Sourced facts only. All 8 sources retrieved with full bodies. Inventory:
[`references/source-index.md`](references/source-index.md).

---

### DOM-018 — XSS on any Shopify shop via structured clone abuse in a postMessage listener

- **Program:** Shopify · **Report:** <https://hackerone.com/reports/231053>
- **Weakness:** `Cross-site Scripting (XSS) - DOM` · **Bounty:** $3,000
- **Severity / date:** not disclosed in the accessible source
- **Body inspected:** Yes — **full report**.
- Full case study also in [`DOM-Based-XSS.md`](DOM-Based-XSS.md) §11.

Root cause and team summary quoted verbatim in §2.2 above. The single most valuable
`postMessage` case in the archive: origin validation absent **and** escaping defeated by
object shape.

---

### DOM-016 — Unsanitised HTML from a browser extension leading to XSS on GitHub.com

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

### BROW-008 — XSS in the Shopify admin via "Button Objects" in a malicious app

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

### BROW-007 — XSS Vulnerability on Image link parser (Discourse)

- **Program:** Discourse · **Report:** <https://hackerone.com/reports/191909>
- **Weakness:** `XSS - Generic` · **Severity:** high · **Bounty:** $256
- **Body inspected:** Yes — **full report**.

**Affected feature:** the markdown parser's image-URL handling.

**Payload (as submitted):**
```
http://host/path/to/image'onerror=alert(1);//.png
```

**Root cause (researcher, verbatim):** *"We have an invalid image URL which finish with
an image extension (PNG). By putting the `'` we are able to break the `img` tag in
which the image url is included by the parser and add custom code, allowing us to run
Javascript code."*

**Impact as claimed:** *"A malicious user could use the `$.getScript` function to load a
malicious script."*

---

### BROW-006 — CRLF and XSS stored on ton.twitter.com

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
[`Reflected-XSS.md`](Reflected-XSS.md).

---

### BROW-004 — www.veris.in DOM based XSS

- **Program:** Veris · **Report:** <https://hackerone.com/reports/119453>
- **Weakness:** `XSS - Generic` · **Severity / Bounty:** not disclosed in the source
- **Body inspected:** Yes — **full report**.

**Payload (as submitted):** `https://www.veris.in/?#<img src=x onerror=alert(1)>`

**Researcher's statement, verbatim:** *"An attacked can execute arbitrary js at your
main page"* (sic).

**Supporting evidence supplied:** the vulnerable bundled source URL —
`https://www.veris.in/wp-content/plugins/Ultimate_VC_Addons/assets/min-js/ultimate.min.js?ver=7e111f63322706ef9e00ec1e58f2edf4`

---

### FRAM-004 (cross-reference) — twine template injection in the Embedded App SDK

- **Program:** Shopify · **Report:** <https://hackerone.com/reports/217790>
- Full case study in [`Framework-and-Template-XSS.md`](Framework-and-Template-XSS.md) §11.

Listed here because it shares this playbook's trust boundary — a malicious installed
app reaching the admin session — while its root cause is template injection.

## 12. Professional Vulnerability Report Template

````markdown
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
```
<source>  →  <code path>  →  <sink>  →  execution in <origin>
```

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
````

**Reporting discipline.** Include the ownership disclaimer. Prove the `postMessage`
listener actually responded. For extensions, state the install base if known. For SDK
findings, establish that malicious app installation is in scope. Cross-reference prior
art in your opening line.

## 13. References

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

## 14. Research Gaps and Further Investigation

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
