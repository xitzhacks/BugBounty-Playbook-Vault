---
name: vuln-lab-engineering
description: Build, extend, and verify intentionally-vulnerable training labs / CTF platforms (barracks.army-style, DVWA/PortSwigger-style, homegrown Node/EJS or opencode projects). Covers the attempt→beacon→flag→submit solve contract, execution detection that accepts a plain alert(1), auto flag popups, per-session variants + attempt pacing, gated solutions (write-up hidden until the first attempt), multi-lab wiring (shared console via data-api, beacon via meta tag, postMessage flow), fixing misaligned lab/challenge pages and stale-asset caches, and the headless self-test harness. Use when the user asks to create or fix a vulnerable lab, add a level or a challenges section, make the flag auto-pop on successful XSS, hide solutions until tried, fix a "misaligned" challenges/solutions page, change grading/solving, or prove every level is solvable.
---

# Vulnerable Lab / CTF Platform Engineering

Building the target is the easy half. The half that breaks is the **proof
chain** — how the platform knows code really ran, gets the flag out of the
victim page, and only then marks the level solved. Get that contract wrong and
the learner pops `alert(1)` and gets nothing.

## 0. Scope check
Applies to a platform the user owns or has written permission to run. These
labs are deliberately vulnerable: bind loopback only (`127.0.0.1`), refuse
routable binds, keep state in memory, and say so in the README.

## 1. The solve contract (do not drift)
```
POST /api/level/:id/attempt {payload}
  → issues per-session one-time sig + builds target URL containing payload
  → target page carries the flag as the page's own secret (+ <meta> sig)
payload executes in that page
  → beacons { sig, flag } to /api/beacon
  → server marks "captured" only if sig matches an attempt issued to THIS
    session and the posted flag equals the expected flag
POST /api/flag { level, flag }
  → exact match required → solved; wrong flag rejected, level stays unsolved
```
Rules that keep it honest and teachable:
- **Flag lives in the target page**, never in the lab bundle or the level
  table. Exfiltration is the only way out.
- **Callback ≠ solved.** Beacon proves execution; submission proves the learner
  actually read the page secret.
- **One-time signature per attempt**, validated against the session; unknown or
  expired sig → 400.
- Return the flag from the beacon **only** when it matches the expected value.
- Don't string-match payloads for solving. Grade separately (hints only).

## 2. Execution detection — accept the classic payload
The #1 complaint: *"the alert popped, why no flag?"* Cause: the helper only
beacons when the payload calls `XSSHERO()`. The learner typed
`<script>alert(1)</script>`.

Fix: load a page helper on every target (external `.js`, so a strict CSP still
allows it) that watches the dialogs the payload is already using:

```js
var native = {
  alert: window.alert.bind(window),
  confirm: window.confirm.bind(window),
  prompt: window.prompt.bind(window),
};
var reported = false, flagShown = false;

function send(note) {                 // one beacon per attempt
  if (reported || !SIG) return;
  reported = true;
  navigator.sendBeacon('/api/beacon',
    new Blob([JSON.stringify({ sig: SIG, flag: FLAG, note })],
             { type: 'application/json' }));
}
function announce() {                 // flag popup AFTER the payload's dialog
  if (flagShown || !FLAG) return;
  flagShown = true;
  native.alert('XSS CONFIRMED — your payload executed.\n\nFLAG:\n' + FLAG);
}
function executed(src) { send('auto:' + src); setTimeout(announce, 20); }

window.alert   = function (m) { var r = native.alert(m);   executed('alert');   return r; };
window.confirm = function (m) { var r = native.confirm(m); executed('confirm'); return r; };
window.prompt  = function (m, d) { var r = native.prompt(m, d); executed('prompt'); return r; };
```
Keep `XSSHERO()` as the explicit callback for write-ups — both paths beacon.
Guard with `reported` / `flagShown` so repeat dialogs don't spam.

## 3. Make the flag unavoidable in the UI
- Auto-open a **flag modal** on capture: the flag in a `<code>` block, prefilled
  submit input, "Submit flag" button, inline error on reject.
- Route both the docked panel form and the modal form through one `applySolved()`
  so badge, status, next-level CTA, and modal message never diverge.
- **Persist captured state server-side and render it into the page**
  (`data-captured`, `data-flag` on the console root). Reload must re-open the
  popup with the same flag — the submission step is what's missing otherwise.
- Show the flag in the target page too (dialog after the payload's own dialog),
  and in the lab. Two surfaces, one capture.

## 4. Grading / anti-cheat that stays fair
- Per-session randomised variants + paced attempts (e.g. 12/20s, short lockout).
- **Pacing must key the level id as a string.** `session.recent.filter(e =>
  e.level === Number(level))` silently matches nothing when ids are `r1`/`c4`
  (`NaN !== NaN`), so the documented throttle never engages. Normalise both
  sides (`String(level)`) and prove it with a 13-request burst → 12×200, then 429.
- **Gate the write-up behind the first attempt** — see §8.
- Hints unlocked by attempt history, closest hint masks the decisive token.
- Exam levels withhold endpoint/param until earned.
- **Test seam:** allow `?variant=N` on the attempt endpoint so the harness can
  pin every randomised variant; the level page already displays the chosen one.

## 5. Self-test harness (the deliverable is green output)
Three suites, all driving real headless Chrome over the real HTTP surface:
1. `verify-lab.js` — for every level × variant: create attempt, open the URL
   with the session cookie, let it execute, wait for capture, assert a **wrong
   flag is rejected**, submit the real flag, assert solved.
2. `verify-popup.js` — only plain proof payloads (`alert(1)`,
   `<img src=x onerror=alert(1)>`) across one reflected, one DOM, one stored
   level; assert dialog fired → flag captured → popup shows it → submit solves.
3. `verify-challenges.js` — for each challenge: assert the solution is locked and
   the payload string is **absent** from the locked HTML, then drive the real UI
   (`click #payload` → `type` → `click #send` → wait for `#flagmodal` → submit
   from the modal), assert solved, wrong flag rejected, and solution unlocked.

Drive the **UI path**, not just the API: the console JS is what the learner uses
and its `data-api` wiring is a separate failure mode. For pacing tests, open a
fresh `browser.createBrowserContext()` per burst so prior attempts don't skew
the count.

Puppeteer details (dialog handlers, `bringToFront`, cross-page cookies) live in
the **local-browser-automation** skill §7 — read it before writing the harness.

## 6. Adding a level — checklist
1. Pick the bug class from a real report corpus (H1/Bugcrowd write-ups), not
   from imagination: the sink, the filter and the payload shape come from the
   report's mechanism. See `references/xss-challenge-design-from-reports.md`.
2. Level entry: brief, target, sink, hints, solution, fix, `render()`, victim.
3. Route(s): attempt API + target page; flag/sig meta on every target render.
4. Register in the lab catalogue; mount the router.
5. Add to the self-test matrix; run all three suites.
6. Never render `solution` on the level page — mask it in hints, and keep the
   write-up behind the attempt gate (§8).

## 7. Pitfalls
- **Dead server with a stale pidfile** → `curl` returns 000 while `.server.pid`
  points at a gone pid. `ss -ltnp | grep <port>`, then `./scripts/dev.sh restart`.
- **In-memory sessions die on restart** — old attempt signatures stop matching;
  re-send after any restart.
- **Pacing 429s** during fast tests — use a fresh browser context per case or
  wait out `retryIn`; don't disable pacing for the user.
- **Pacing that never fires** because the id was coerced with `Number()` while
  level ids are strings. Burst-test it once (13 attempts → 429 on 13) instead of
  trusting the code reads correctly.
- **A "locked" solution page that still contains the payload** — hiding the tab
  is not gating. Grep the locked HTML for the solution string in the test.
- **Static `maxAge` caching** serves the old CSS/helper JS in a long-lived tab:
  the user reports "still broken" while every headless context looks fixed. Do
  not ask for a hard reload — version every asset URL (`?v=<ASSET_V>`, one value
  per process boot) and serve static with `maxAge: 0, etag: true`. Exact recipe
  and the layout traps that follow: `local-browser-automation`
  `references/ui-alignment-cache.md`.
- **Hidden iframes still execute dialogs** — blind levels will pop the flag
  dialog even though the page is never shown; that's fine, the console remains
  the evidence.
- A `goto`/`evaluate` that hangs after a successful payload is usually a
  **dialog**, not a server problem (see local-browser-automation §7).

## 8. Gated solutions (hide the answer until the learner tries)
Rule: before the first attempt the learner gets the brief and hints only; the
write-up unlocks on `attempts >= 1`. Hints: tier 1 free, tier 2 after 1 attempt,
tier 3 after 2.

Enforce in **three** layers — hiding the tab client-side is a fake gate:
1. **Page nav** — the `Solution` entry is a non-link badge (`<span>` with a lock)
   while locked; a real `<a href="?view=solution">` once unlocked.
2. **Server route** — `GET /:lab/:id/solution` renders a locked panel when
   `attempts === 0`. It must not include the payload/write-up in the response.
3. **Solutions index** — the navbar page lists the row as "Locked — attempt it
   first" with a hints link, and only links the write-up after an attempt.

Test both directions: locked HTML contains no payload string, unlocked HTML
does. This is the one thing a client-side check cannot fake.

## 9. Multi-lab wiring (one helper, several labs)
When the platform grows a second section (Challenges, SQLi, …), do not fork the
console/helper — parameterise them:
- **Beacon target** comes from `<meta name="vv-beacon">` on the target page,
  defaulting to the original path. One `xsshero.js` then serves every lab.
- **Console API base** comes from `data-api` on the console root
  (`/xss/api` vs `/challenges/api`). Mirror the endpoint shape per lab:
  `POST <api>/level/:id/attempt`, `GET <api>/level/:id/state`,
  `POST <api>/level/:id/reset`, `POST <api>/flag`, `POST <api>/beacon`.
- **Guard optional DOM nodes** (`#clear`, `#poke`, `#reset-level`) so a page
  without those buttons doesn't throw and kill the whole console script.
- **Sig lookup must filter by lab prefix** (`key.startsWith(lab + ':')`) — two
  labs share one `session.attempts` map.
- **Nav**: add the section to `topnav` and drive the active state from a
  `page.section` value; keep the solutions index gated server-side (§8).
- **postMessage levels** need a flow the console knows: load the target, then
  `frame.contentWindow.postMessage({ html: parsed }, '*')` after `onload`.
  Parse the payload box as JSON when possible — a structured-clone array walks
  past an escaper that only handles strings (`typeof v !== 'string'` returns it
  unchanged, and `innerHTML = array` stringifies it).

## 10. References
- `references/vulnverse-xss-lab.md` — the VulnVerse (Node/Express/EJS, 27 XSS
  levels) implementation map, beacon contract, the alert-hook + popup fix, and
  exact verification commands from a real session.
- `references/xss-challenge-design-from-reports.md` — four challenges built from
  documented H1 case studies (blocklist → DOM-020 regex → STOR-142 NFKC →
  DOM-018 structured clone), with working payloads, the gating recipe, and the
  assertions to copy into a self-test.
