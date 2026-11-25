# VulnVerse — XSS lab implementation map (session reference)

Homegrown barracks.army-style platform at `/home/user/projects/vulnverse`
(Node 18+, Express 4, EJS, in-memory store, no DB). 27 XSS levels across
`reflected/dom/stored/blind`, plus 7 more labs in the roadmap.

## Layout that matters
```
server/index.js            bootstrap; refuses any bind except 127.0.0.1/localhost/::1
server/lib/store.js        sessions, attempts, flags, captured, variants, pacing
server/labs/xss.js         router: /xss/* console API + /x/* vulnerable targets
server/labs/xss-levels.js  level table: brief, render(), solution, fix, victim, variants
server/labs/grading.js     hint tiers, payload masking, filter-damage notes
views/xss/level.ejs        level page: brief/target/fix panes + docked console + flag modal
public/js/xsshero.js       page helper on every target: sig+flag from <meta>, beacon
public/js/console.js       attacker console: send, poll state, flag panel, modal, submit
scripts/verify-lab.js      headless Chrome matrix over every level × variant
scripts/verify-popup.js    alert()/onerror-only proof of popup + submit
```

## Wire format
- Target pages get `<meta name="vv-sig" content="...">` and
  `<meta name="vv-flag" content="flag{<app>_<lvl>_<10 hex>}">` only when the
  request carries `?vv=<sig>` belonging to a live attempt in the session.
- `POST /xss/api/beacon {sig, flag, note}` → `{ok, executed:true, captured, flag,
  alreadySolved, impact}`. Captured only when posted flag === expected.
- `POST /xss/api/flag {level, flag}` → solved only on exact match; wrong flag 400.
- `GET /xss/api/level/:id/state` → `{solved, captured, flag, attempts, ...}`.
- Test seam: `POST /xss/api/level/:id/attempt?variant=N` pins a randomised variant.

## The bug fixed (2026-10 session)
Symptom: learner types `<script>alert(1)</script>`, dialog fires, console says
"no callback — nothing executed". All 27 published solutions called
`XSSHERO()`, so only that call beaconed.

Fix:
1. `public/js/xsshero.js` — wrap `alert/confirm/prompt`; first dialog beacons
   `{sig, flag}` and then (after the payload's dialog closes) a native alert
   shows `XSS CONFIRMED ... FLAG: flag{...}`. Guards `reported`/`flagShown`.
   `XSSHERO()` kept and also announces the flag.
2. `views/xss/level.ejs` — `#flagmodal` markup + `data-captured` / `data-flag`
   on `#console`.
3. `public/js/console.js` — `openFlagPopup()` / `closeFlagPopup()`,
   `submitModalFlag()`, shared `postFlag()` + `applySolved()`; captured-on-load
   branch re-opens the popup after a reload (previously the flag was lost).
4. `public/css/site.css` — `.flagmodal` / `.fm-*` styles.
5. `scripts/verify-lab.js` — `page.on('dialog', d => d.dismiss())` on control +
   victim pages. Without it puppeteer v25 parks the renderer and the whole run
   hangs on 30s navigation timeouts once payloads start popping dialogs.
6. `scripts/verify-popup.js` + `npm run verify:popup`.

## Verification commands and observed results
```
npm start                                   # http://127.0.0.1:4173
npm run verify          # 40/40 level-variants solvable
npm run verify:popup    # 13/13 popup checks passed
```
Popup test cases: r1 via real UI (`alert(1)`), d1 DOM/fragment
(`onerror=alert(1)`), s1 stored staff view — each asserts dialog fired, flag
captured without `XSSHERO()`, popup carries the flag, submission solves, wrong
flag rejected.

Reload case: attempt on r2 with `?variant=1` and
`x" autofocus onfocus=alert(1) x="`; after capture, fresh page at
`/xss/level/r2` must auto-open the modal with the same flag. `bringToFront()`
is mandatory or headless Chrome skips autofocus.

## Gotchas seen
- `.server.pid` can point at a dead pid; `curl` → 000. Use `ss -ltnp` and
  `./scripts/dev.sh restart`.
- Restarting wipes sessions: every flag/sig/captured entry is in RAM.
- `/js/*` is served with `maxAge: '1h'`; hard-reload a long-open tab before
  concluding a fix didn't apply.
