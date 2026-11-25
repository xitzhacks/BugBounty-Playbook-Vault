# ASP.NET WebForms XSS — field notes (from win.net-square.com:1051/add_comment1.aspx)

## Target fingerprint
- `Server: Microsoft-IIS/7.5`, `X-AspNet-Version: 4.0.30319`
- Form fields: `__EVENTTARGET`, `__EVENTARGUMENT`, `__VIEWSTATE`,
  `__VIEWSTATEGENERATOR`, `__EVENTVALIDATION`, `txtName`, `txtEmail`, `txtComment`
- Postback param `rptPaging$ctl03$btnPage` (pager control)

## Request Validation behavior (empirically confirmed)
Error returned when blocked:
```
Server Error ... A potentially dangerous Request.Form value was detected
from the client (txtComment="...").
System.Web.HttpRequestValidationException
```
- BLOCKED: literal `<` `>`  AND numeric entities `&#60;` `&#62;`
  (numeric entities are decoded BEFORE validation, so they trip it too)
- PASSED: named entities `&lt;` `&gt;`; any payload with no `<`/`>`/`&`-entity
- Takeaway: the "entity-encode to bypass" trick works ONLY with NAMED
  entities on this class of filter. Numeric `&#60;` is NOT a reliable bypass.

## Why the obvious payloads did not execute
Every injection landed inside a `<textarea>` and was auto HTML-encoded by
ASP.NET:
- `" onfocus=alert(1) autofocus x="` -> `&quot; onfocus=alert(1) autofocus x=&quot;`
- `&lt;img src=x onerror=alert(1)&gt;` -> `&amp;lt;img ... &amp;gt;`
The submission page is a self-echoing form with NO separate comment-display
view (probed 12+ candidate endpoints; only `/add_comment1.aspx` existed;
marker submission showed 0 re-occurrences). => No live sink. Secure by design.

## Other sinks to check on similar apps (the missing piece here)
If a SEPARATE page renders stored comments as HTML, re-run the matrix there:
- comment list / feed (`/view_comments.aspx`, `/comments.aspx`)
- profile / bio fields
- admin moderation view
A `<div>` or `value=""`/`href=""` reflection (not a textarea) is where
`" onfocus=alert(1) autofocus x="` or `&lt;svg onload=alert(1)&gt;` would fire.

## form-urlencoded field-separator gotcha
User's own pasted request had `txtComment=&&#60;svg...` — the doubled `&`
split the value so the payload never reached `txtComment` (server saw a
malformed extra field). Always encode `&`->`%26`, `#`->`%23`, or use a
library that encodes the body (Python `requests` `data=` dict does this).

## False-positive trap (scanner design)
A naive "`<script>` present in response" check matches the page's OWN
`<script type="text/javascript"> //<![CDATA[` block. Guard by:
1. matching the PAYLOAD specifically (e.g. `onfocus=alert(1)`), AND
2. confirming it is NOT inside a textarea:
   `inside = t[:i].rfind('<textarea') > t[:i].rfind('</textarea')`
3. confirming it is not `&quot;`-wrapped (still encoded).

## Minimal working curl (named-entity, passes filter)
```
curl -s "http://HOST/add_comment1.aspx" \
  --data "__EVENTTARGET=rptPaging%24ctl03%24btnPage" \
  --data "__EVENTARGUMENT=" \
  --data "__VIEWSTATE=<FRESH>" \
  --data "__VIEWSTATEGENERATOR=4D0FA771" \
  --data "__EVENTVALIDATION=<FRESH>" \
  --data "txtName=test&txtEmail=example%40xyz.com" \
  --data-urlencode "txtComment=<svg onload=alert(1)>"
```
Note: `--data-urlencode` safely encodes `&`/`#`. Use it instead of
hand-built bodies.
