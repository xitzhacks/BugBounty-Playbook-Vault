---
title: "Self-XSS"
type: playbook
category: self-xss
cwe: "CWE-79"
source_count: 24
full_bodies_available: 24
summary_only: 0
archive_accessed: 2026-10-12
---

# Self-XSS

## 1. Overview

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

## 2. Root Cause and Technical Mechanics

The flow is identical to stored XSS except the victim and the attacker are the same
principal:

```
attacker pastes payload into their OWN field  →  stored/reflected
                                                →  only the attacker views it
```

### 2.1 The three shapes found in this archive

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

### 2.2 The self-XSS-as-bug-class argument

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

### 2.3 Self-XSS as a chain component

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

## 3. Attack Surface and Preconditions

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

## 4. Manual Testing Methodology

1. **Self-test in your own account first.** If it does not fire for you, it will not
   fire for anyone else either. Do not report a suspected self-XSS you have not
   reproduced.
2. **Then test the multi-user path immediately.** This is the high-value step and the
   one most researchers skip. If user B can trigger what user A stored, you have
   **stored XSS**, not self-XSS — re-file accordingly. Compare
   [`Stored-XSS.md`](Stored-XSS.md).
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

## 5. Input and Output Context Analysis

Contexts are the standard ones (see
[`Reflected-XSS.md`](Reflected-XSS.md) §5), with two self-XSS-specific observations:

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

## 6. Test Cases and Proof-of-Concepts

### 6.1 Historical payloads (verbatim from the cited reports)

| Case | Report | Field | Payload as submitted |
| --- | --- | --- | --- |
| SELF-008 | `125059` | password | `'>"><img src=x onmouseover =prompt(document.domain)>` |
| SELF-014 | `164027` | comment | `</textarea><img src="s" onmouseover=alert(1)>` and `</textarea><script>alert(1)</script>` |
| SELF-021 | `212721` | Jira Base URL | `javascript://alert(document.domain);%2f%2f@` |

### 6.2 Newly authored illustrations (not from the archive)

```text
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
```

**Escalation test — do this first.** After reproducing the self-XSS, repeat the same
payload from a **second account** and check whether the first account can trigger it.
If yes, stop filing self-XSS and file [`Stored-XSS.md`](Stored-XSS.md).

## 7. Encoding, Filtering, and Parsing Behavior

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

## 8. Impact and Severity Considerations

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

## 9. False Positives and Limitations

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

## 10. Remediation and Regression Testing

### 10.1 Remediation

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

### 10.2 Regression tests

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

## 11. Historical Bug Bounty Case Studies

Sourced facts only. All 24 sources were retrieved with full bodies. Inventory:
[`references/source-index.md`](references/source-index.md).

---

### SELF-021 — IE 11 Self-XSS on Jira Integration Preview Base Link

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

### SELF-014 — Reflected Self-XSS in the Comment section of Files Information

- **Program:** Nextcloud · **Report:** <https://hackerone.com/reports/164027>
- **Archive listing:** <https://h1.security.nathan.sx/nextcloud.html>
- **Published:** recorded in the archive listing · **Weakness:** `XSS - Generic`
- **Bounty:** $100 · **Severity:** not disclosed in the source
- **Body inspected:** Yes — **full report**.

**Affected feature:** `demo.nextcloud.com` → All Files → select a file → right-hand
details panel → **Comments**.

**Payloads (as submitted):**
```
</textarea><img src="s" onmouseover=alert(1)>
</textarea><script>alert(1)</script>
```

**Reproduction (as submitted):** paste the payload into the comment box, click **Post**,
then *"Click on the Edit Comments Button that will appear near the posted comment when
cursor was hovered over comment"* — *"THE APPLIED XSS PAYLOAD GETS EXECUTED WHILE
CLICKING THE EDIT BUTTON THAT APPEARS."*

**Root cause:** the comment is re-populated into a `<textarea>` on the edit path without
encoding, so `</textarea>` terminates the element.

**Researcher's own typing:** `Vulnerability Type: Reflected XSS`, `Vulnerability Found In
the test domain: demo.nextcloud.com`. It was paid at the self-XSS value of $100.

---

### SELF-008 — Self-XSS on Password Reset Form

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

### SELF-018 — (HackerOne SSO-SAML) Login CSRF, Open Redirect, and Self-XSS

- **Program:** HackerOne · **Report:** <https://hackerone.com/reports/171398>
- **Archive listing:** <https://h1.security.nathan.sx/security.html>
- **Weakness:** `XSS - Generic` · **Severity:** low · **Bounty:** not disclosed
- **Body inspected:** Yes — **full report**.

**PoC (source as submitted, redacted fields preserved):**
```html
<html>
<body>
	<iframe id="login_csrf_frame" src="████████" style="width:0;height:0;border:0;border:none;"></iframe>
	<script>
		setTimeout(function(){document.location.href = "https://hackerone.com/users/saml/sign_in?email=████&remember_me=true";}, 5000);
	</script>
</body>
</html>
```

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

### Supporting self-XSS sources (full bodies retrieved)

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

### BBH-001 methodology match (BugBountyHunter.com, page read 2026-10-17)

The XSS guide (<https://www.bugbountyhunter.com/vulnerability/?type=xss>) describes
the class exactly as this playbook frames it:

> *"Self XSS is XSS that only affects you. This could be in your account settings
> that only you can access. For these types of XSS I recommend looking for a cross
> site request forgery issue on login which you can use in a chain."*

That is the Starbucks/Teavana pattern above, stated as craft guidance rather than as
a report. The same page's impact section adds the escalation rule used across the
corpus: *"Test using the leaked session cookie on a fresh browser session and see if
you authenticate!"*

## 12. Professional Vulnerability Report Template

````markdown
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
````

**Reporting discipline.** Title it accurately — say "Self-XSS" in the title so triage
can triage it immediately. Lead the summary with the **broken flow**, not the payload.
State explicitly that you tested the multi-user path. Never claim victim account loss
you have not demonstrated.

## 13. References

- PortSwigger — What is self-XSS and is it a security issue?: <https://portswigger.net/research/self-xss>
- OWASP — XSS Prevention Cheat Sheet: <https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html>
- OWASP — CSRF Prevention Cheat Sheet (for the chain cases): <https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html>
- OWASP — URL handling / open redirect guidance: <https://cheatsheetseries.owasp.org/cheatsheets/Unvalidated_Redirects_and_Forwards_Cheat_Sheet.html>
- MDN — `javascript:` URL scheme: <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/void>
- Reports cited: <https://hackerone.com/reports/212721>, <https://hackerone.com/reports/164027>,
  <https://hackerone.com/reports/125059>, <https://hackerone.com/reports/171398>,
  <https://hackerone.com/reports/166709>, <https://hackerone.com/reports/177508>,
  <https://hackerone.com/reports/170156>, <https://hackerone.com/reports/178611>

## 14. Research Gaps and Further Investigation

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
