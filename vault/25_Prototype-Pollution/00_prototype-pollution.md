---
title: "Prototype Pollution — pollution alone is DoS; pollution plus a gadget is stored XSS"
type: playbook
category: prototype-pollution
cwe: "CWE-1321"
source_count: 4
full_bodies_available: 4
corpus: "h1-brain disclosed_reports.db (3,673 rows), bucket prototype-pollution (classified.json) -> module prototype-pollution (module_map_all.json)"
list_accessed: "2026-11-07"
note: "Anchor bodies: PP-1106238 (Mermaid DoS, $3,000), PP-1280002 (Mermaid stored XSS, $3,000), PP-712065 (lodash, CVE-2020-8203), PP-998398 (deparam + eval gadget). Claims trace to bodies read 2026-11-07."
---

# Prototype Pollution — pollution alone is DoS; pollution plus a gadget is stored XSS

## 1. Overview

Four rows, three sinks, **$6,000 / 2 rows with figures** (max $3,000, paid twice on one
program). The corpus prices a wire the other vaults do not: lodash server-side pollution
(PP-712065, `None`, CVE-2020-8203) and the Swiftype client hash parser (PP-998398, `None`)
demonstrate the sink without naming a downstream consumer that rung the payout bell — while
the two GitLab Mermaid rows convert the *same* sink (`__proto__` through an unsanitized
directive) first into a DoS characterization ($3,000) and then into a stored-XSS
weaponization with a named `template` gadget ($3,000 again). The module teaches the two-step
method that the paid pair exhibits: prove pollution, then name the gadget.

**Case-stock (4 rows / $6,000):**

| Case | Target | Mechanism | Bounty |
|---|---|---|---|
| [PP-712065](https://hackerone.com/reports/712065) | lodash (nodejs-ecosystem) | `merge`/`mergeWith`/`defaultsDeep` → `Object.prototype` (CVE-2020-8203) | — |
| [PP-998398](https://hackerone.com/reports/998398) | *.swiftype.com (elastic) | `deparam` hash parse → pollution → `eval` hook gadget → DOM XSS | — |
| [PP-1106238](https://hackerone.com/reports/1106238) | gitlab (Mermaid directive) | `%%{init:…}%%` `__proto__` merge → app-wide DoS | $3,000 |
| [PP-1280002](https://hackerone.com/reports/1280002) | gitlab (Mermaid directive) | `__proto__.template` pollute → stored XSS on search-bar touch | $3,000 |

## 2. The library lane: lodash (CVE-2020-8203)

PP-712065 (lodash 4.17.15, `None`) is the corpus's only server-side/library row and its only
CVE row. The sink sentence names the exact functions and the reach:

> The functions merge, mergeWith, and defaultsDeep can be tricked into adding or modifying properties of the Object prototype. These properties will be present on all objects.

After the framing ("I would like to report a prototype pollution vulnerability in lodash."]),
the PoC is the `zipObjectDeep` one-liner (`_.zipObjectDeep(['__proto__.z'],[123])`), and the
impact sentence is the vault's DoS anchor — server crash "guaranteed," RCE "in some cases."
The DB weakness label (`Allocation of Resources Without Limits or Throttling`) never mentions
pollution; the body is the (only) taxonomy here, and the vault classifies the row by its
`*.<id>.js` sink behavior, not its label. Recorded at `None`: a library-level pollution
report with no in-program gadget — the negative-space anchor for §6.

## 3. The client lane: Swiftype `deparam` + the eval gadget

PP-998398 (elastic, `None`) is the corpus's deepest single row even at no figure, because it
supplies what the paid rows assume: a *named gadget in the same file as the sink*. The hash
(`https://blog.swiftype.com/#__proto__[asd]=alert(document.domain)`) feeds a `deparam`
parser whose loop is annotated inline in the body with `//pollution here` — the
`c = c[u] = …` walk that follows attacker-controlled `__proto__` path segments:

> deparam function which parses location.hash in https://s.swiftypecdn.com/install/v2/st.js  is vulnerable to prototype pollution.
> There is a script gadget in the same js file which leads to XSS.

The gadget is `_convertStringHooksToFunctions`, which `eval()`s every hook string on the
config object — pollution plants the payload, the hook consumer fires it. The vault cites
this row as the *method* exemplar (sink + gadget + hash PoC in one file) and as a limit
case: no DB figure, so the module does not claim the method alone was priced.

## 4. The paid pair, step one: Mermaid as DoS (PP-1106238, $3,000)

PP-1106238 (GitLab, **$3,000**) is the same directive sink with the outcome capped at denial
of service — and the body says so honestly. The directive syntax (`%%{init: {<JSON_OBJECT>}}%%`)
merges attacker JSON into the config object with no sanitization:

> The issue is that directive JSON_OBJECT is lacking proper sanitization which means we can specify `__proto__` attribute to overwrite Object prototype.

The demonstrated payload (`'__proto__': {'polluted': 'asdf'}`) adds a `polluted` attribute to
"every new object in the application," and the Steps end at a broken page ("you can't comment
or perform any action except clicking on the left sidebar links"). The `bug` behavior is
stated as DoS, the expected behavior as a sanitization rule. The $3,000 attached to a DoS
*characterization* is the surprise this step teaches: a clean, reproducible, app-wide
breakage through a stored directive — filed before any weaponization — paid at the same tier
as the stored-XSS follow-up.

## 5. The paid pair, step two: the `template` gadget (PP-1280002, $3,000)

PP-1280002 (**$3,000**) opens by citing its predecessor ("I am continue investigating #1106238
(sic) and found additional vector for prototype pollution and stored xss") and then changes
exactly one thing: the polluted property. Instead of a junk `polluted` attribute, the
directive writes `__proto__.template` to an `<iframe>` payload carrying the reporter's
script:

> Mermaid allows setting __proto__ attribute in the directive which leads to stored XSS.

> This will pollute template attribute and, for example, if we click on the search bar after the page loaded, XSS will be executed. This still requires minimal user interaction.

That is the entire weaponization delta — same directive, same merge, new property name, and
the app's template consumer turned into the gadget. Two directives are needed (the body
repeats the `%%{init:…}%%` line twice), the touch point is a search-bar click, and the
impact sentence ("can steal some data or make any actions as user") is the stored-XSS
tariff. The vault's central doctrine is the pair read together: **prove pollution first
(DoS, paid), then name the consumer property (XSS, paid).** Neither row alone prices the
other's step. Analysts citing this vault must cite both halves.

## 6. What pays, what doesn't

- The corpus pays **pollution + named consumer**: PP-1280002's `template` gadget ($3,000)
  and even PP-1106238's app-wide DoS ($3,000) both name what the polluted property *does*
  (breaks the page; fires on search-bar touch). The two `None` rows (lodash library,
  Swiftype gadget-proposal) name sinks — and, in Swiftype's case, a gadget — without a paid
  downstream demonstration. The vault keeps the `None`s as "no figure," not $0.
- **Pollution prose without a consumer does not pay in this corpus.** "Properties present on
  all objects" is the sink sentence (PP-712065); the payout sentences are the DoS/XSS
  consequences (PP-1106238/1280002). Report writers in this class must fill the second
  sentence or expect the first to be scored as a library note.
- **The paid pair is one investigation, twice paid.** PP-1106238 → PP-1280002 is a
  sequential disclosure on one sink. Summing "per-sink value" across the vault double-counts
  the research effort; the register keeps both rows because the program did.
- **Interaction cost is stated, not hidden.** "If we click on the search bar" (PP-1280002)
  and "click anywhere" (PP-1106238) are in the paid reports. A gadget that needs a touch
  step still paid — but the step is written, and the playbook requires it written.

## 7. Cross-references

- `XSS/` — the terminal payoff of three rows (DOM, stored); that vault owns XSS doctrine.
- `RCE/` — lodash's downstream claim ("remote code execution … in some cases,"
  PP-712065); that vault owns execution doctrine.
- `Authentication-Session/` — no corpus row reaches auth, but the `template` consumer is
  the object-property-confusion shape; cite the auth vault for hardening posture.
- Playbook P2 (`PP-Testing-Agent-Playbook.md`) encodes the pollute-then-name-the-gadget
  ladder from §§4–5.
