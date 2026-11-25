# Sink vs data source — deciding latent vs exploitable

Reflection is half the work. The other half is reading the JavaScript and answering one
question per sink: **can an attacker write the value this sink renders?**

A sink fed by server-rendered HTML, DB content, or framework state is a *latent hardening
issue*. A sink fed by a field the attacker controls (URL param, profile field, bot/alert
name, webhook payload) is the finding. Reporting the first as XSS is how you get N/A'd.

---

## 1. Sink inventory — what to grep, per stack

```bash
# generic
grep -aoE '(innerHTML|outerHTML|insertAdjacentHTML|document\.write|eval\(|new Function)' bundle.js
# React
grep -aoE 'dangerouslySetInnerHTML|__html:' bundle.js
# Alpine.js
grep -oE 'x-html="[^"]{0,120}"' page.html | sort | uniq -c | sort -rn
# AngularJS (1.x)
grep -oE 'ng-bind-html="[^"]{0,120}"|trustAsHtml|ng-bind-html-unsafe' page.html app.js
# Vue
grep -aoE 'v-html|innerHTML' bundle.js
# sources that feed them
grep -aoE '(location\.(hash|search|href)|document\.referrer|postMessage)' bundle.js
```

Then, for **each** hit, write down the data source. If you cannot name the source, you do not
have a finding yet.

Note on framework noise: `dangerouslySetInnerHTML` appears 10–15× in every react-dom build
(internal property validation). Those are not app sinks. The app-level ones look like
`dangerouslySetInnerHTML:{__html:<expression>}` where the expression is a component prop or
API field — count the `__html:` occurrences and read each one.

---

## 2. Worked sink map (TrendSpider, 2026-10-18) — all latent, zero exploitable

| Stack | Sink | Data source | Attacker-writable? |
|---|---|---|---|
| Alpine (marketing) | `x-html="lastPriceWithCurrency"` ×41 | `window.__ts__tickers.<SYM>.render` from market data API | no |
| Alpine | `x-html="post.title.rendered"` / `post.excerpt_raw` / `post.categories_list` | WP REST content, editor-authored | no |
| Alpine | `x-html="notification.message"` | `form()` component ← API `message` / `errors[field][0]` | **checked, no** (see §3) |
| Alpine | `x-html="content"` | `/api/gdpr-notice/` response | no |
| Alpine | `x-html="html"` | `response.data.help` on demo-form success | no |
| Markets theme | `i.innerHTML = t.title` (search results) | `/wp-json/trendspider/v1/search?format=trendspider-elements` | **latent** — see §4 |
| Markets theme | `$refs.table.innerHTML = e.table` | `admin-ajax.php?action=get_congresstrading_table` | no — params echoed 0× |
| AngularJS 1.8.0/1.8.1 (register) | `ng-bind-html=":: shortPlanDescriptionHumanizedHTML"` (single occurrence) | string built from plan API fields (`price`, `trial`, `trialOptions`) | no |
| React (trading app) | 14 `dangerouslySetInnerHTML` | all react-dom internals; app code has none | n/a |
| React (trading widget) | `styleEl.innerText = payload.style.css` via `postMessage` | parent frame, origin-gated to `localhost`/`chartcalc.local`/2 CloudFront hosts | no remotely — CSS injection only |
| React (SignalStack) | `dangerouslySetInnerHTML:{__html: e.authentication.help}` (one app-level) | broker connector help text from provider config | no |

Result: **0 exploitable DOM sinks**; two documented latent issues. That is a legitimate,
reportable-to-yourself negative — and it is what you tell the operator instead of "still testing".

---

## 3. Auditing an HTML sink fed by API messages

Pattern: `jQuery('<div role="alert">' + msg + '</div>')` or `el.innerHTML = response.message`.
Server-controlled strings concatenated into HTML. The question is only whether the server ever
echoes input into those strings.

Method — submit hostile-but-valid-shaped values to every live form endpoint and read the
validation text back:

```bash
curl -sk -X POST https://target/api/forms/request-demo/ \
  -F 'name=<i>cpmarkX</i>' -F 'email=cpmark987abczq@bad' -F 'message=m' -F '_form_id=request_demo'
# -> {"errors":{"email":["Email address is not a valid email address"], ...}}   static strings
curl -sk -X POST https://target/api/forms/newsletter/ \
  -F 'firstName=cpmark987abczq' -F '_form_id=newsletter'
# -> {"errors":{"firstName":["This field can only contain letters."]}}           static + allowlist
```

If every message is a fixed string (or an allowlist rejects the payload before it reaches the
response), the sink is not reachable. If a message contains your input verbatim, you have DOM
XSS on the form page — then check whether the input can be prefilled from the URL to make it
non-self-XSS.

---

## 4. The `<mark>` highlight case — unencoded output that still isn't a bug

Search APIs that highlight matches return markup:

```
GET /wp-json/trendspider/v1/search?query=S%26P&format=trendspider-elements
-> [{"title":"SPGI - <mark>S&P</mark> Global Inc.","url":".../SPGI/"}]
```

The raw `&` proves **no output encoding is applied** to this field — a real hardening gap worth
noting. It is not exploitable: the highlighted span is a substring of the ticker/company name
stored in the DB, and there is no write path to those names. To promote a case like this you
must first obtain an attacker-writable row in the same table.

**Two control probes that settle it** (run these before you write either verdict — they take 10
seconds and they are the difference between "latent" and "maybe reflected"):

```bash
# 1. Is the highlighted text the DB value or my query string?
curl -sk '…/search?query=aapl&format=trendspider-elements'
#   -> "<mark>AAPL<\/mark> - Apple Inc."     lowercase query, UPPERCASE mark => DB value
#   if instead you get "<mark>aapl</mark>" the server interpolates YOUR string -> keep going

# 2. Does the hostile query reach the response at all?
curl -sk --get --data-urlencode 'query="><img src=x onerror=alert(1)>' \
     --data-urlencode 'format=trendspider-elements' '…/search'
#   -> []                                    no match, nothing echoed => not injectable

# 3. (context) does the API HTML-encode at all?
curl -sk '…/search?query=S%26P&format=trendspider-elements'
#   -> "<mark>S&P<\/mark>"                   raw & => encoding genuinely missing at the sink
```

Probe 1 is the discriminator nobody runs: case-flipping the query (`aapl` → `AAPL`) tells you
whose bytes are inside the markup. Probe 2 tells you whether the query is a source at all. Probe 3
confirms the encoding gap is real rather than an artefact of a benign entity name.

Classification rule:
- Unencoded output + attacker-writable source = **finding**.
- Unencoded output + DB/editor source = **hardening note**, one paragraph, not a submission.

---

## 5. Stored XSS when the write path is auth-gated

Do not write "stored XSS: not testable" and stop. Do this instead:

1. Enumerate every sink that renders stored content (profile fields, chart/scan titles,
   bot/alert names, webhook payload rendering, widget configs, shared-entity descriptions).
2. For each, state the **write path** and whether it needs auth.
3. Publish the sink map as the coverage artifact, with the exact list to test the moment a
   session exists. That is actionable; "untested" is not.

Verification of the public read-only surfaces you *can* reach is still worth doing — sample
20–60 stored objects and check how special characters are emitted in each context:

```python
# sampled titles containing &, ', " — check <title>, og:title (single-quoted attr!), JSON-LD
re.search(r"<meta property=\"og:title\" content='([^']*)'", body)
```

On TrendSpider, 60/60 sampled shared entities emitted `&amp;`, `&#39;`, `&#34;` consistently —
including inside a **single-quoted** `og:title` attribute where a raw `'` would have broken out.
That is the highest-risk context in the page and it held, which is what turns "probably safe"
into "verified safe".

---

## 6. Headless-browser verdict discipline

A DOM-XSS claim needs one of:

- `document.title` changed by the payload (`document.title='XSSMARK_x'`), checked in `--dump-dom`;
- a real node your payload created (`id="xssmark987"`) present in the serialized DOM;
- an OOB callback.

Never: "the marker string appears in the dumped DOM". VWO / AdRoll / Facebook / GTM pixels copy
the full current URL (query and fragment) into their `src`, URL-encoded, so your marker lands in
`outerHTML` on pages that executed nothing. This produced 10 false "EXECUTED" rows before the
detector was fixed to key on `document.title`.

Also: a `javascript:` payload in a fragment that never changes the title means nothing — it needs
a click, so it is a separate (weaker) claim.

---

## 7. Related

- `hunt-xss` SKILL.md → *Exhaustive Sweep → Emission-Form Classification* (the param-side pipeline)
- `hunt-xss` `scripts/xss_param_sweep.py` (steps 1–3 automated)
- `recon-pitfalls` §12 — when every page 403s, it may be UA fingerprinting, not hardening
