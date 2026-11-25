---
title: "HTML Injection"
type: playbook
category: html-injection
cwe: "CWE-79", "CWE-116"
source_count: 13
full_bodies_available: 11
summary_only: 2
archive_accessed: 2026-10-12
---

# HTML Injection

## 1. Overview

HTML injection is the injection of attacker-controlled **markup** without script
execution. It sits on a spectrum:

```
inert markup  →  HTML injection  →  script execution (XSS)
   (text)        (elements,           (CSP not present)
                  attributes,
                  no script)
```

Some reports in this archive stopped deliberately at the middle rung. **That restraint
is correct and this playbook documents it as a first-class outcome.**

> **Merge rationale.** HTML injection shares its root cause, its testing methodology,
> and its remediation with XSS — missing context-correct output encoding. It is
> separated from [`Context-Based-XSS.md`](Context-Based-XSS.md) only because the
> *demonstrated impact differs*, which changes how the report should be written and how
> a triager should read it. If you are looking for testing methodology, use
> [`Reflected-XSS.md`](Reflected-XSS.md) §4; this file covers the boundary cases and
> the non-browser sinks.

## 2. Root Cause and Technical Mechanics

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

### 2.1 Non-browser sinks — the genuinely distinct part

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

### 2.2 The restraint case — a model for triage

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

### 2.3 The correctly-filed negative result

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

## 3. Attack Surface and Preconditions

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

## 4. Manual Testing Methodology

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
   [`Reflected-XSS.md`](Reflected-XSS.md) §5.

## 5. Input and Output Context Analysis

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

## 6. Test Cases and Proof-of-Concepts

### 6.1 Historical payloads (verbatim from the cited reports)

| Case | Report | Payload |
| --- | --- | --- |
| HTML-008 | `179426` | `/en/block-index/1160457/%22%3E%3Ch1%3EXSS%20here` and `%22%3E%3Cmarquee%3EXSS%20here` |
| HTML-001 | `2735` | `You have been hacked. Click <a href="http://phishing-site">here</a> to reset your password.<div style="display:none">` |
| HTML-002 | `6843` | `dashboard/extend/connect/"%20onmouseover="alert(document.cookie)">` |
| HTML-005 | `146278` | `Host: -->test"<img src=a onerror=alert('xss')>` |
| HTML-012 | `200826` | `github-btn.html?#&user=<h1><marquee>HTML<br>…&type=follow` (PoC #1, Chrome/IE) |

### 6.2 Newly authored illustrations (not from the archive)

**Stage 1 — markup control (the correct primary test).** Newly authored.

```
"><h1>xss-marker
"><marquee>xss-marker
"><details open ontoggle=alert(1)>xss-marker
```

`HTML-008` used exactly the first two. The third is a modern, inert-until-interacted
markup probe.

**Stage 2 — external-resource proof (for email/PDF/export sinks).** Newly authored.

```html
<img src="https://COLLAB/?rendered=1" width="1" height="1">
<a href="https://COLLAB/">click</a>
```
A hit on `COLLAB` proves the sink rendered the markup **and** gives you the OOB
evidence the report needs.

**Stage 3 — attribute break-out (escalate toward XSS).** Newly authored.

```
" onmouseover="xss-marker
' onmouseover='xss-marker
```

**Safe proof.** External-resource callbacks beat `alert(1)` here: they prove rendering
*and* execution origin simultaneously, and they work in email clients that block
scripts.

## 7. Encoding, Filtering, and Parsing Behavior

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

## 8. Impact and Severity Considerations

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

## 9. False Positives and Limitations

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

## 10. Remediation and Regression Testing

### 10.1 Remediation

- **HTML-encode the output for its context** — the same rules as XSS
  ([`Reflected-XSS.md`](Reflected-XSS.md) §10.1). Encoding does not depend on whether
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

### 10.2 Regression tests

| Test | Asserts |
| --- | --- |
| `"><h1>`, `"><marquee>`, `"><details open ontoggle=…` in every reflecting field | markup escaped |
| Same, in every field that reaches an email/notification | email body escaped |
| External-resource probe in email/export output → no callback | no render |
| Assert exported logs/files are served `text/plain` + `nosniff` + `attachment` | inert format |
| Pair-bracket filter test cases: `<img src=x`, `<a href=x`, `<<h1>` | no bracket-pair filter remains |
| Assert CSP present **and** inspected for `unsafe-inline` | defence in depth, correctly configured |

## 11. Historical Bug Bounty Case Studies

Sourced facts only. Inventory: [`references/source-index.md`](references/source-index.md).

---

### HTML-008 — Reflected XSS on blockchain.info (markup injection, CSP-scoped)

- **Program:** Blockchain · **Report:** <https://hackerone.com/reports/179426>
- **Archive listing:** <https://h1.security.nathan.sx/blockchain.html>
- **Published:** 2016-11-01 · **Weakness:** `XSS - Generic` · **Severity:** medium
- **Bounty:** $100 · **Body inspected:** Yes — **full report**.

**Affected feature:** the final URL path segment of `https://blockchain.info/en/block-index/<id>/<segment>`.

**PoCs (as submitted):**
```
https://blockchain.info/en/block-index/1160457/%22%3E%3Ch1%3EXSS%20here
https://blockchain.info/en/block-index/1160457/%22%3E%3Cmarquee%3EXSS%20here
```

**Scope statement (researcher, verbatim):** *"Due to the strict Content Security Policy
which even blocks 'self', arbitrary javascript cannot be executed through this
vulnerability without some CSP bypass. Great! :)"*

**Test environment (stated):** Firefox 49.0.2 and Chrome 54.0.2840.71.

**Recommended remediation (researcher, verbatim):** *"Make sure to properly encode the
last part of the URL before printing it to the page. Another possible solution is to
make sure the URL matches a strict whitelist regexp, so that this part of the URL is
not put on the page at all if it looks fishy."*

---

### HTML-001 — HTML injection in "Invite Collaborators" (RelateIQ)

- **Program:** RelateIQ · **Report:** <https://hackerone.com/reports/2735>
- **Archive listing:** <https://h1.security.nathan.sx/relateiq.html>
- **Weakness:** `XSS - Generic` · **Severity / Bounty / date:** not disclosed in the source
- **Body inspected:** Yes — **full report**.

**Affected feature:** the **first name** field at registration; content reaches an
outbound **invitation email** sent from `[REDACTED_EMAIL]`.

**Payload (as submitted):**
```
You have been hacked. Click <a href="http://phishing-site">here</a> to reset your password.<div style="display:none">
```

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

### HTML-010 — HTML Injection possible due to bad filter (VK.com)

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

### HTML-012 — [github.algolia.com] DOM Based XSS github-btn.html

- **Program:** Algolia · **Report:** <https://hackerone.com/reports/200826>
- **Archive listing:** <https://h1.security.nathan.sx/algolia.html>
- **Weakness:** `XSS - Generic` · **Severity:** medium · **Bounty:** $100
- **Body inspected:** Yes — **full report**.

**Affected feature:** `https://github.algolia.com/github-btn.html`, parameters `user`,
`repo`, `type`.

**Vulnerable code (quoted in the report):** the script parses `window.location.href`
into `params`, then:
```js
"follow" == type && (mainButton.className += " github-me", text.innerHTML = "Follow @" + user, button.href = "https://github.com/" + user
```

**PoC #1 (as submitted) — HTML injection, Chrome/IE:**
```
https://github.algolia.com/github-btn.html?#&user=<h1><marquee>HTML<br>HTML<br>…&type=follow
```

**PoC #2 (as submitted) — XSS, IE:** an attacker page sets
`<meta http-equiv="X-UA-Compatible" content="IE=9">` and iframes the target with
`user=yrdy<script>alert(document.domain);alert(document.cookie);//&type=follow`.

**The reporter's browser split is the useful part:** PoC #1 is explicitly
*"HTML Injection for Chrome, Internet Explorer"*; PoC #2 is *"XSS for Internet Explorer
(using X-UA-Compatible IE=9)"*. Correctly scoped, correctly labelled.

---

### HTML-002 — Cross-Site Scripting in getMarketplacePurchaseFrame (concrete5)

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

### Supporting HTML-injection sources (full bodies retrieved)

- **HTML-011** `200753` — <https://hackerone.com/reports/200753> — Ubiquiti, medium.
  Same `github-btn.html` pattern on `nutty.ubnt.com` — a **per-deployment** instance of
  `HTML-012`, useful evidence that shared third-party embeds are inconsistently fixed.
- **HTML-005** `146278` — <https://hackerone.com/reports/146278> — Nextcloud. Log-file
  HTML injection; full case study in
  [`File-Upload-and-SVG-XSS.md`](File-Upload-and-SVG-XSS.md) §11.
- **HTML-006** `150179` — <https://hackerone.com/reports/150179> — Twitter.
  *"Html Injection and Possible XSS in sms-be-vip.twitter.com"* — note the researcher's
  own title hedged: possible XSS.
- **HTML-013** `206877` — <https://hackerone.com/reports/206877> — ownCloud, low.
  HTML injection in the Desktop Client.

## 12. Professional Vulnerability Report Template

````markdown
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
```
https://<host>/<path>?<param>="><h1>xss-marker
```
> `<h1>` renders as an element. Screenshot attached.

### Script execution attempt
```
https://<host>/<path>?<param>=...
```
> Result: <did not execute>. Reason: <CSP header / sanitiser / browser>. Header evidence
> pasted below.

```
content-security-policy: <the actual header>
```

## Remediation
HTML-encode for the output context. See §10.1.

## Test environment
Browser: <name + version> · Date: <YYYY-MM-DD>
````

**Reporting discipline.** State which rung you reached and **why you did not reach the
next**. Paste the CSP header rather than asserting it. Do not call markup injection
XSS. If the sink is an email or export, say so explicitly — it changes the impact
argument entirely.

## 13. References

- OWASP Cheat Sheet — XSS Prevention: <https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html>
- MDN — Content Security Policy: <https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSP>
- OWASP — HTML sanitization and validation: <https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html>
- OWASP — Email security / injection in mail bodies: <https://cheatsheetseries.owasp.org/cheatsheets/Email_Security_Cheat_Sheet.html>
- Reports cited: <https://hackerone.com/reports/179426>, <https://hackerone.com/reports/2735>,
  <https://hackerone.com/reports/198907>, <https://hackerone.com/reports/200826>,
  <https://hackerone.com/reports/6843>, <https://hackerone.com/reports/200753>,
  <https://hackerone.com/reports/146278>, <https://hackerone.com/reports/150179>,
  <https://hackerone.com/reports/206877>

## 14. Research Gaps and Further Investigation

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
