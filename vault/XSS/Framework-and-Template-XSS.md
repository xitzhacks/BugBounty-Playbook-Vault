---
title: "Framework and Template XSS"
type: playbook
category: framework-and-template-xss
cwe: "CWE-79", "CWE-1336"
source_count: 4
full_bodies_available: 4
summary_only: 0
archive_accessed: 2026-10-12
---

# Framework and Template XSS

## 1. Overview

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

## 2. Root Cause and Technical Mechanics

```
attacker input  →  template engine compiler  →  expression evaluation  →  code execution
```

### 2.1 Client-side template injection — AngularJS

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
```
q=wrtz{{(_="".sub).call.call({}[$="constructor"].getOwnPropertyDescriptor(_.__proto__,$).value,0,"alert(1)")()}}zzzz
```

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

### 2.2 Template escapes in an escaping engine — lodash/twine

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

### 2.3 The arithmetic probe — the universal confirmation

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

## 3. Attack Surface and Preconditions

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

## 4. Manual Testing Methodology

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

## 5. Input and Output Context Analysis

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

## 6. Test Cases and Proof-of-Concepts

### 6.1 Historical payloads (verbatim from the cited reports)

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

### 6.2 Newly authored illustrations (not from the archive)

**Stage 1 — evaluation probe (no code execution).** Newly authored; the concept is
sourced from `FRAM-001`/`FRAM-003`.

```
?q=A{{7*7}}B        → expect A49B          (AngularJS)
?p=A${7*7}B         → expect A49B          (lodash _.template)
{{7*7}}                                   (Jinja2 / Twig server-side)
{$smarty.version}                         (Smarty)
```

`A`/`B` sentinels matter: they prove the value was *spliced into* a template rather
than echoed.

**Stage 2 — marker execution.** Newly authored.

```js
// Newly authored: execute a benign marker instead of an alert.
{{constructor.constructor('document.title="H1XSSMARKER9"')()}}
```

**Stage 3 — context, for reporting.**

```js
document.domain   // the origin in which the template evaluated
angular.version   // the engine version, for the fix
```

**Regression probe for escaping-engine second sinks.** Newly authored. Put a
sentinel into a value that lands in an attribute consumed by another engine, and check
whether it is re-parsed:

```
value = 'A" data-x="B'   →  does data-x appear as a *new* attribute or as text?
```

## 7. Encoding, Filtering, and Parsing Behavior

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

## 8. Impact and Severity Considerations

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

## 9. False Positives and Limitations

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

## 10. Remediation and Regression Testing

### 10.1 Remediation

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

### 10.2 Regression tests

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

## 11. Historical Bug Bounty Case Studies

Sourced facts only. All 4 sources retrieved with full bodies. Inventory:
[`references/source-index.md`](references/source-index.md).

---

### FRAM-001 — Reflected XSS on developer.uber.com via Angular template injection

- **Program:** Uber · **Report:** <https://hackerone.com/reports/125027>
- **Archive listing:** <https://h1.security.nathan.sx/uber.html>
- **Weakness:** `XSS - Generic` · **Bounty:** $3,000 · **Severity:** not disclosed
- **Body inspected:** Yes — **full report**.

**Affected feature:** `https://developer.uber.com/docs/deep-linking`, parameter `q`.

**Reproduction (as submitted) — the model report for this class:**
```
https://developer.uber.com/docs/deep-linking?q=wrtz{{7*7}}
```
> "If you view the rendered source of the resulting page, you'll find the string
> `wrtz49`, showing the input has been evaluated."

**Escalation (as submitted):** an Angular sandbox escape designed for IE 11 —
```
q=wrtz{{(_="".sub).call.call({}[$="constructor"].getOwnPropertyDescriptor(_.__proto__,$).value,0,"alert(1)")()}}zzzz
```

**Methodological notes (reporter's own words):** *"This URL uses an Angular sandbox
escape to obtain arbitrary JavaScript execution and execute alert(1). It's designed to
work in Internet Explorer 11, but the technique could probably be used to target other
browsers given sufficient effort."* — an honest browser-scoping statement.

**Prior art cited by the reporter:** `http://blog.portswigger.net/2016/01/xss-without-html-injection`

---

### FRAM-004 — XSS via twine template injection in Shopify.API.Modal.input

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

### FRAM-003 — Stored XSS via AngularJS Injection

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

### FRAM-002 — Angular injection in the profile name of onpatient

- **Program:** drchrono · **Case ID:** `FRAM-002` · **Report:**
  <https://hackerone.com/reports/141240>
- **Weakness:** `XSS - Generic` · **Severity / Bounty / date:** not disclosed in the source
- **Body inspected:** Yes — **full report**.

Same program, same class, **different field** — the profile name rather than the
referral address. Filed by a different researcher. Retained as a separate case study
because it demonstrates a distinct field and therefore a distinct (per-field)
remediation, even though the root cause is identical.

---

### Supporting note

A related but distinct program appears elsewhere in this knowledge base under
Framework-adjacent classification: `HTML-012` (`200826`, Algolia) and `HTML-011`
(`200753`, Ubiquiti) are both `github-btn.html` embeds where a `user` parameter is
read from `window.location` and written with `text.innerHTML = "Follow @" + user` —
an `innerHTML` DOM sink rather than a template-expression sink. See
[`HTML-Injection.md`](HTML-Injection.md) and
[`DOM-Based-XSS.md`](DOM-Based-XSS.md).

## 12. Professional Vulnerability Report Template

````markdown
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
```
$ angular.version
<version>
```

### Evaluation proof (no code execution)
```
https://<host>/<path>?<param>=A{{7*7}}B
```
> Rendered source contains `A49B` — the input is being evaluated as a template.

### Root cause
<Where user input reaches the compiler rather than a variable slot.>

## Proof of concept
### Inert evaluation
> (as above)

### Marker execution
```
?q={{constructor.constructor('document.title="H1XSSMARKER9"')()}}
```
> `document.title` is `H1XSSMARKER9`; execution in origin `<origin>`.

## Remediation
Never compile user input as template source; bind as a variable value. See §10.1.

## Regression tests
<The `A{{7*7}}B` assertion, plus the stored multi-user test if applicable.>
````

**Reporting discipline.** Lead with the **arithmetic probe** — it is the strongest and
safest evidence in this class. Record the engine version. Check the *rendered source*,
not the HTTP response. Do not claim server-side code execution. State the viewer for
stored variants and test the multi-user path.

## 13. References

- PortSwigger — Client-side template injection: <https://portswigger.net/web-security/dom-based/client-side-template-injection>
- PortSwigger research cited by FRAM-001 — "XSS without HTML injection": <http://blog.portswigger.net/2016/01/xss-without-html-injection-1/>
- OWASP — DOM based XSS: <https://cheatsheetseries.owasp.org/cheatsheets/DOM_Based_XSS_Cheat_Sheet.html>
- AngularJS security guidance (note: AngularJS 1.x is EOL): <https://docs.angularjs.org/guide/security>
- AngularJS sandbox bypass research: <https://github.com/AngularJs/AngularJS>
- MDN — `_.template` / lodash documentation: <https://lodash.com/docs/4.17.4#template>
- Reports cited: <https://hackerone.com/reports/125027>, <https://hackerone.com/reports/217790>,
  <https://hackerone.com/reports/141463>, <https://hackerone.com/reports/141240>

## 14. Research Gaps and Further Investigation

- **Only 4 sources.** This is the smallest playbook here and the most under-sourced
  relative to how common the bug is. HackerOne's taxonomy has no template-injection-XSS
  category, so these reports are scattered across `XSS - Generic` — the inventory in
  [`references/source-index.md`](references/source-index.md) should be re-mined for
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
