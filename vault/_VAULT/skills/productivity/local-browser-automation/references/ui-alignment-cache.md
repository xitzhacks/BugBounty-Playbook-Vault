# UI alignment + asset cache — worked case

From a Node/Express/EJS lab platform where the user reported "still misaligned"
twice after a fix that measured correctly in headless Chrome.

## The trap: it was the cache, not the CSS

- `express.static(publicDir, { maxAge: '1h' })`
- `<link rel="stylesheet" href="/css/site.css">` — no version

Fresh puppeteer contexts fetched the new file; the user's long-lived tab kept
the old one for an hour. Every screenshot said "fixed", the user's screen said
"broken". Both were true.

**Check first when the user repeats a complaint after a verified fix:**

```bash
curl -sI http://127.0.0.1:PORT/css/site.css | grep -iE 'cache-control|etag'
curl -s http://127.0.0.1:PORT/ | grep -o 'site.css[^"]*'
```

If `max-age` is non-zero and the URL has no query, that is the bug.

**Fix (versioned URLs, per process boot):**

```js
// server/lib/assets.js
module.exports = { ASSET_V: String(Date.now()) };

// server/index.js
const { ASSET_V } = require('./lib/assets');
app.locals.assetV = ASSET_V;
app.use(express.static(publicDir, { maxAge: 0, etag: true }));

// views/partials/head.ejs
<link rel="stylesheet" href="/css/site.css?v=<%= assetV %>">

// views/.../level.ejs, detail.ejs
<script src="/js/console.js?v=<%= assetV %>"></script>

// server-rendered target pages (template strings)
<script src="/js/xsshero.js?v=${ASSET_V}"></script>
${scripts.map((s) => `<script src="${s}?v=${ASSET_V}"></script>`)}
```

Version *every* asset the page owns. The CSS-only version still leaves stale
console/helper JS behind.

## Measurement recipe

Probe geometry before touching CSS:

```js
const box = (sel) => {
  const b = document.querySelector(sel).getBoundingClientRect();
  return { x: Math.round(b.x), w: Math.round(b.width), right: Math.round(b.right) };
};
// 1. heading left edge === content container left edge
// 2. every cell inside its row/card bounds
// 3. no negative x on any cell (clipped off-screen)
// 4. document.documentElement.scrollWidth <= innerWidth
```

Run at 1400 / 1280 / 720 / 640. The failures below only appear at some widths.

## Failure modes seen (all reproduced)

### 1. Generic class-name collision
A new component used `.sol-row`, `.sol-name`, `.sol-class`, `.sol-link` —
names already defined *later* in the stylesheet for an older index page. The
later rules won: the row got `32px 190px 1fr auto` instead of the intended grid,
items wrapped to a second row and the link cell measured `x=-87`.

Fix: namespace the new component (`.chs-row`, `.chs-name`, …). Scoping under a
unique parent also works but renaming is clearer.

### 2. Responsive overrides before the base rules
`@media (max-width:1060px){ .chs-row{...} }` was placed above the base
`.chs-row{}` declaration added later. Same specificity, later rule wins → the
media query never applied and rows stayed five-across at 720px (names squeezed
to 90px). Append responsive overrides at the **end** of the file.

### 3. Pseudo-element counted as a grid item
```css
li { display:grid; grid-template-columns:30px 1fr; }
li::before { content: counter(x); }      /* becomes grid item 1 */
```
With `b` and `span` as items 2 and 3, the body text landed in the 30px column —
one word per line. Explicit placement:
```css
li { display:grid; grid-template-columns:30px 1fr; grid-template-rows:auto auto; }
li::before { grid-column:1; grid-row:1 / span 2; }
li b    { grid-column:2; grid-row:1; }
li span { grid-column:2; grid-row:2; min-width:0; }
```

### 4. Sibling containers with different widths
`.pagehead{max-width:1120px}` above `.ch-wrap{max-width:1180px}` → heading at
`x=164`, cards at `x=134`. One width per section:
```css
.pagehead.ch-pagehead { max-width: 1180px; }
```

### 5. `auto` columns collapse in header rows
Header `<span>`s had no content in the state/link columns, so `auto` sized to 0
and the fr tracks expanded: CHALLENGE label width 492 vs row 344. Pin the
content-dependent tracks in both templates:
```css
grid-template-columns: 76px minmax(0,1.3fr) minmax(0,1fr) 110px 300px;
```
Header padding must match the row's border+padding (`15px` vs `14px + 1px
border`) or every label is off by 1px.

### 6. Flex children stretch
A "Solution locked" pill in a flex tab bar had no `align-self`, so it stretched
to the full bar height (46px) and crossed the underline. `align-self:center` →
30px pill.

### 7. Tab labels offset by their own padding
`.views a{padding:11px 14px}` pushed the first tab's text 14px right of the
title. `.views a:first-child{padding-left:0}`. If the underline is the
container's `border-bottom`, it also starts at the container edge; move it to an
inset `::after` (`left:24px; right:24px`) so the rule, title and panels share an
edge.

## Probe-assertion gotchas (cost a false failure)

- **Borders.** Expected CTA width is `card.w - 2 - paddingLeft*2`; forgetting the
  2px of borders reports 235 vs 237 and fails a correct layout.
- **Right-aligned cells.** `justify-self:end` makes the box content-width, so
  `x`/`w` never match the column. Compare `right` edges (955 == 955,
  1271 == 1271).
- **Asset checks on the wrong page.** `console.js` is only on detail pages —
  asserting it on the catalogue fails correctly but for the wrong reason.
- **Keep the evidence script.** Deleting the ad-hoc verifier after a passing run
  left the tracker showing the earlier failed attempt. Leave it in `/tmp` with
  the `hermes-verify-` prefix.

## Workflow that ended the loop

1. `curl -sI` the stylesheet → confirm cache headers/URL.
2. Probe boxes at four widths; fix by root cause, not by nudging margins.
3. Re-probe until heading/content edges and column edges match numerically.
4. Screenshot and view — geometry catches clipping, images catch cramped layout.
5. Run the functional suites (UI flows), not just layout probes.
6. Report the numbers (h1 x == card x, header right == cell right) so the next
   "still broken" report has something concrete to compare against.
