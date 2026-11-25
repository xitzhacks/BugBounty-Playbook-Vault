# VulnVerse — worked contract (reference implementation)

Project: `/home/user/projects/vulnverse` · Node + Express + EJS · loopback only
· `npm start` → http://127.0.0.1:4173 · `./scripts/dev.sh start|stop|restart|status`.

## File map

```
server/index.js              mounts /xss, /x, /challenges, /c, /solutions
server/lib/store.js          sessions, flags, attempts, pacing, records (all RAM)
server/labs/xss.js           27-level lab router + target apps
server/labs/xss-levels.js    the level table (brief/hints/solution/render)
server/labs/challenges.js    4 challenge table + API + target apps + gated /solutions
public/js/xsshero.js         page helper: dialog hook + XSSHERO + beacon
public/js/console.js         shared attacker console (data-api / data-flow)
public/js/targets/*.js       client-side sinks per challenge/level
views/{xss,challenges,hub}/  EJS views
scripts/verify-lab.js        answer-key suite   (npm run verify)
scripts/verify-popup.js      alert()-only suite (npm run verify:popup)
scripts/verify-challenges.js gating suite       (npm run verify:challenges)
```

## Page contract (both labs)

```html
<meta name="vv-sig"    content="<one-time signature>">
<meta name="vv-flag"   content="flag{app_level_hex}">
<meta name="vv-beacon" content="/challenges/api/beacon">   <!-- defaults /xss/api/beacon -->
<script src="/js/xsshero.js"></script>
```

`xsshero.js` wraps `alert/confirm/prompt`, keeps the natives, and on the first
dialog *or* `XSSHERO()` posts `{sig, flag}` to `vv-beacon`. It then pops the
flag in a native alert. One beacon per page load (`reported` guard).

## API contract

| XSS lab | Challenges |
|---|---|
| `POST /xss/api/level/:id/attempt` | `POST /challenges/api/level/:id/attempt` |
| `GET /xss/api/level/:id/state` | same shape under challenges |
| `POST /xss/api/beacon` | `POST /challenges/api/beacon` |
| `POST /xss/api/flag` | `POST /challenges/api/flag` |

`/api/flag` body `{level, flag}`; requires a live attempt **and** captured flag;
wrong flag → 400. Solve marks `store.solve(session, LAB, id, impact)`.

## The four challenges (`LAB = 'challenges'`)

| id | diff | name / app | flow | target | working payload |
|---|---|---|---|---|---|
| c1 | Basic | Search That Echoes / TicketHive | `link` `q` | `/c/search` | `<svg/onload=alert(1)>` |
| c2 | Medium | Banner That Parses / SwiftCart | `link` fragment | `/c/deals` | `<<a/:<"a">img src=# onerror=alert(1)>` |
| c3 | Hard | Feed That Normalises / Rockford Social | `submit` | `/c/feed?r=` | `†‡•＜img src=a onerror=javascript:alert('hacked')>…‰€` |
| c4 | Expert | Wallet That Trusts / PayNest | `postmessage` | `/c/wallet` | `["<img src=x onerror=alert(1)>"]` |

Mechanics: c1 strips only `<script>`; c2 `raw.replace(/<\/?\w+[^>]*\/?>/g,'')`
then `innerHTML`; c3 strips ASCII tags on write then `.normalize('NFKC')` on
render; c4 listener has no origin check and `esc()` returns non-strings
unchanged, so an array reaches `innerHTML`.

## Gating

`attempts = store.labState(session,'challenges').attempts[id] || 0`

- `solutionUnlocked = attempts >= 1`; `/challenges/:id/solution` renders a
  locked panel when false (never the payload).
- Hint tier: 1 free, 2 at one attempt, 3 at two.
- `/solutions` rows: "Locked — attempt it first" + hints-only link.
- Detail page: `<span class="views-locked">Solution locked</span>` instead of the
  tab link; server enforces independently.

## Console

`#console data-level data-flow data-solved data-captured data-flag data-api`

- `api` defaults `/xss/api`; challenges pass `/challenges/api`.
- On load with `data-captured=true`, reopens the flag modal from `data-flag`
  (reload fix).
- `postmessage` flow: after iframe `load`, `JSON.parse(payload)` when valid,
  then `postMessage({html: value}, '*')`.
- Flag modal ids: `#flagmodal #fm-flag #fm-form #fm-input #fm-msg #fm-close`.

## Verification (all must stay green)

```
npm run verify             40/40 level-variants
npm run verify:popup       13/13 execution/flag checks
npm run verify:challenges  27/27 gating + flag checks
```

All three dismiss dialogs (`page.on('dialog', d => d.dismiss())`) — required, or
payload dialogs hang puppeteer until the 30s timeout.

## Lessons baked into this codebase

- `store.paceCheck` must compare `String(level)`; `Number('c4')` made pacing a
  no-op. Burst test: 12×200 then 429.
- Challenge UI container is 1180px; `.pagehead.ch-pagehead` matches it.
- Challenge solution rows are `.chs-*`; the XSS index owns `.sol-row` (a
  collision silently overrode the grid and clipped the lock cell).
- Responsive overrides for `.chs-row` live at the END of site.css.

## Where to mine more challenges

`/home/user/projects/FAN/Vault/XSS/` — playbooks per class with §11 case studies:
Reflected, Stored, DOM, Context, Filter-Bypass, Framework, File-Upload/SVG,
Self, HTML-Injection, Browser-Extension/Messaging. Each case has program,
payload (often verbatim), root cause and bounty — pick a mechanic, rebuild the
minimum app, keep the payload where published.
