---
name: local-browser-automation
description: Drive a real or local browser via CDP for web interaction, screenshots, scraping, and site work using browser-use or browser-harness. Use whenever a task needs browser control on the user's machine for clicking, typing, JS rendering, logged-in sessions, or bot-protected pages. CRITICAL USER RULE baked in — NEVER touch the user's logged-in or default browser profile. Always launch a separate throwaway incognito Chrome with its own temp user-data-dir. Also covers the install path that works in locked-down environments (uv via pip, not curl pipe sh, and no nohup, use terminal background=true).
---

# Local Browser Automation — Isolated Chrome + CDP

## 0. HARD RULE (user preference, non-negotiable)
NEVER automate the user's default or logged-in browser. The user explicitly said
"use chrome with no profile, do not touch my account logged chrome."
- Identify the user's real browser first (it may be Brave, not Chrome — check
  `ps aux | grep -iE "[c]hrome|[b]rave|[f]irefox"`). Leave it alone.
- Launch a SEPARATE instance with a throwaway temp profile:
  `--user-data-dir=/tmp/bu-chrome-prof --incognito --no-sync --disable-sync`
- This guarantees zero access to saved logins, cookies, or sync data.

## 1. Install browser-use (env-safe path)
Some environments BLOCK `curl ... | sh` and `nohup`/shell-background wrappers.
Use pip-based install instead:
```
pip3 install --break-system-packages uv          # or: python3 -m pip install uv
export PATH="$HOME/.local/bin:$PATH"
uv python install 3.12                            # fetches CPython 3.12.x
uv venv --python 3.12 /home/user/.venvs/...      # OR a venv of your choice
uv pip install -U browser-use                    # latest stable
```
(Replace the venv path as appropriate. uv also installs `browser-harness`,
`browser-use`, `browser-use-tui`, `browseruse`, `bu` bins.)

## 2. Register the skill
```
/home/user/.venvs/<v>/bin/browser-use skill install
# installs SKILL.md to ~/.agents/skills/browser-use/ etc.
```

## 3. Launch an ISOLATED Chrome (background=true, NOT nohup)
```
google-chrome \
  --remote-debugging-port=9223 \
  --user-data-dir=/tmp/bu-chrome-prof \
  --no-first-run --no-default-browser-check \
  --no-sync --disable-sync --incognito \
  --new-window about:blank
# run with terminal(background=true) so Hermes tracks the pid
```
Use a NON-default port (9223, not 9222) to avoid clashing with any existing
Chrome the user may have open with debugging enabled.

## 4. Connect browser-use to THAT instance
The harness defaults to the running Chrome on 9222. Point it at our isolated
instance via env var:
```
export CDP_URL="http://127.0.0.1:9223"
export CHROME_DEBUG="1"
/home/user/.venvs/<v>/bin/browser-use <<'PY'
new_tab("https://example.com")
print(page_info())
PY
```
Verify: `curl -s http://127.0.0.1:9223/json/version` should return the Chrome
version and a webSocketDebuggerUrl. Confirm the only Chrome with a profile is
`/tmp/bu-chrome-prof` (your throwaway), and the user's real browser shows no
`user-data-dir` from you.

## 5. Diagnostics
- `browser-use doctor` → checks chrome-running / daemon-alive / active-connections.
- If "Chrome isn't running — launching it", the harness may auto-launch (it will
  use its OWN temp profile, which is also fine — still isolated from the user).
- Cloud auth (`browser-harness auth login`) is OPTIONAL and not needed for local.

## 6. Pitfalls
- `curl | sh` for uv → BLOCKED by consent guard in some envs. Use pip install uv.
- `nohup ... &` / `setsid` → blocked ("use terminal(background=true)"). Use the
  tool's background=true instead.
- Browser shows an "Allow remote debugging?" popup → that is EXPECTED when the
  harness connects; it is per-connection approval, not a re-ask. Only requires
  action if the harness explicitly asks the USER to tick a checkbox (it won't,
  when Chrome was launched WITH --remote-debugging-port already set).
- If the daemon dies between sessions, re-launch the isolated Chrome (step 3)
  before running browser-use again.

## 7. Puppeteer / puppeteer-core page pitfalls (v22+)
These bite any scripted CDP run (self-tests, PoC harnesses, screenshot rigs):

- **Dialogs park the renderer.** `Page.javascriptDialogOpening` is emitted as a
  `dialog` event, and with NO listener puppeteer does NOT auto-dismiss — the
  page (and every `goto` / `evaluate` on it) hangs until the 30s navigation
  timeout, which reads like a dead server. Always attach before first
  navigation:
  ```js
  page.on('dialog', (d) => d.dismiss().catch(() => {}));
  ```
  Register it on the control page AND every new page. If the test intentionally
  asserts dialog text, push `d.message()` to an array first, then dismiss.
- **Never navigate a page whose renderer is dialog-blocked** — open a fresh page
  for the next step instead of reusing it.
- **Headless Chrome skips autofocus in background tabs.** Payloads/UI that rely
  on `autofocus` + `onfocus` silently do nothing. Call
  `await page.bringToFront()` before `goto`.
- **Shared cookies across pages:** read them once via CDP
  (`Network.getAllCookies` on a control page), then
  `client.send('Network.setCookie', { name, value, domain: '127.0.0.1', path: '/' })`
  before navigating a new page.
- **Launch args that keep CI/headless stable:** `--no-sandbox
  --disable-dev-shm-usage --disable-gpu`; `headless: 'new'`.

## 8. Raw CDP over websocket-client (when puppeteer/playwright aren't installed)

`websocket-client` is usually present on a Kali box even when playwright isn't. Driving Chrome
directly is ~40 lines and needs no extra install:

```python
subprocess.Popen(["google-chrome","--headless=new","--no-sandbox","--disable-gpu",
                  "--disable-dev-shm-usage","--remote-debugging-port=9223",
                  "--remote-allow-origins=*","about:blank"])
# poll http://127.0.0.1:9223/json/version, then pick a target from /json
ws = websocket.create_connection(page["webSocketDebuggerUrl"], timeout=30)
```

- **`--remote-allow-origins=*` is mandatory** for the DevTools websocket. Without it the handshake
  fails with `Handshake status 403 Forbidden — Rejected an incoming WebSocket connection from the
  http://127.0.0.1:9222 origin`. That message reads like a broken browser; it is a missing flag.
- Message shape: `{"id": n, "method": "Runtime.evaluate", "params": {...}}`; read frames until
  `msg["id"] == n` — events interleave and will otherwise be mistaken for the reply.
- Results are triple-nested: `resp["result"]["result"]["value"]`. Screenshots:
  `Page.captureScreenshot {"format":"png"}` → base64 in `["result"]["data"]`.
- Wait for load by **polling** `Runtime.evaluate("document.readyState")` rather than relying on
  `Page.loadEventFired`; then add a short sleep before interacting with SPA handlers (a React
  `useEffect`-registered listener mounts after `complete`).
- **A blank screenshot is not a failed run.** SPAs that wait on a parent handshake render an empty
  body while their listeners are live. Assert on DOM facts — `querySelectorAll('style').length`,
  `document.body.className`, `getComputedStyle(el,'::before').content` — and treat the image as
  secondary evidence. Retry the interaction in a loop (15 × 400 ms) instead of firing once.
- Serve a page at a privileged origin (e.g. `http://localhost`) without root by routing only that
  host through a local proxy: Chrome `--proxy-server=http://127.0.0.1:<port>
  --proxy-bypass-list="<-loopback>"`. A PAC file does **not** override Chrome's implicit loopback
  bypass. The proxy needs CONNECT tunnelling so the rest of the page's HTTPS still loads.

## 9. Layout / visual QA — measure, don't eyeball

When the complaint is "the UI is misaligned", do not start editing CSS from a
screenshot. Probe geometry first, then screenshot to confirm.

Probe per page (see `scripts/layout-probe.js`):

```js
const r = (sel) => { const b = document.querySelector(sel).getBoundingClientRect();
  return { x: Math.round(b.x), w: Math.round(b.width), right: Math.round(b.right) }; };
// heading must share a left edge with the content container
// every cell must sit inside its row/card bounds
// document.documentElement.scrollWidth - innerWidth must be <= 0
```

- Run at **1400 / 1280 / 720 / 640** — a layout that is perfect at desktop is
  often broken at one breakpoint only.
- Negative `x` on any cell means it is clipped off the left edge; that is a
  real bug, not a rounding artefact.
- Screenshot after the numbers pass, and only then use vision — images catch
  taste problems (cramped, run-on labels) that geometry cannot.

Failure modes that keep recurring:

1. **Component class-name collision.** A generic name (`.sol-row`) already
   defined later in the stylesheet silently wins over a new component's rules:
   items wrap and one cell lands at `x < 0`. Namespace new components
   (`.chs-row`) or scope every rule under a unique parent; don't add a second
   `.foo` definition and hope order works.
2. **Media queries before the base rules are dead.** In a monolithic CSS file,
   an `@media` block placed above the component's base declaration is overridden
   by that declaration. Append responsive overrides at the END of the file.
3. **Pseudo-elements are grid items.** `li::before` with a counter plus
   `grid-template-columns: 30px 1fr` puts the body text in the 30px column
   (one word per line). Give the counter `grid-column/grid-row` explicitly, or
   position it absolutely and pad the item.
4. **Space-between footers overflow.** `justify-content: space-between` with
   `white-space: nowrap` children on a narrow card pushes the second child past
   the border. Allow `flex-wrap: wrap` or stack the children.
5. **Sibling containers disagree on width.** A shared header (`.pagehead`,
   1120px) sitting above a section wrapper (1180px) outdents the heading by
   30px — measured `h1.x=164, cards.x=134`. Use one width per section for both
   header and content, via a modifier (`.pagehead.ch-pagehead{max-width:1180px}`).
6. **Empty grid header cells collapse `auto` columns.** A column-header row
   with five spans over `... auto auto` computes different fr tracks than the
   data rows (whose cells have content in those columns), so CLASS/STATUS labels
   land over the wrong values. Pin those tracks in **both** templates
   (`grid-template-columns: 76px 1.3fr 1fr 110px 300px`).
7. **Flex children stretch.** A status/lock badge placed in a flex tab bar
   stretches to full bar height and crosses the underline. `align-self: center`.

### Stale CSS reads as "you didn't fix it"

When the user says *still* broken after a verified fix, check the response
before re-debugging. `express.static(..., {maxAge:'1h'})` plus an unversioned
`<link href="/css/site.css">` means their browser keeps the old layout for an
hour while every fresh headless context looks correct.

Fix properly instead of asking for a hard reload:
```js
// server/lib/assets.js — one value per process boot
module.exports = { ASSET_V: String(Date.now()) };
// app.locals.assetV = ASSET_V;  and  maxAge: 0, etag: true
<link rel="stylesheet" href="/css/site.css?v=<%= assetV %>">
<script src="/js/console.js?v=<%= assetV %>"></script>
```
Version every asset URL the page owns (CSS, console JS, target scripts, helper
JS). One normal F5 then fetches the current file.

### Probe-assertion gotchas

- Width math must subtract **both borders and both paddings**:
  `card.w - 2 - paddingLeft*2`. Off-by-2 looks like a layout bug in the test.
- Right-aligned cells (`justify-self: end`) have content-width boxes; compare
  their **right edges**, not `x`/width, against the header cell.
- Only assert an asset URL on a page that actually loads it (console JS is on
  detail pages, not the catalogue).
- Keep the ad-hoc verification script on disk after the run. Deleting it can
  leave the verification tracker pointing at an earlier failed attempt.

`scripts/layout-probe.js` is the re-runnable version: pass URL + selectors,
get x/width/right + horizontal overflow per viewport, non-zero exit on failure.
Deeper notes and the exact fixes: `references/ui-alignment-cache.md`.
