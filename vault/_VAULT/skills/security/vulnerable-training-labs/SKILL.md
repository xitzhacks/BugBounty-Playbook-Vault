---
name: vulnerable-training-labs
description: Build and extend deliberately vulnerable practice platforms (XSS/CTF-style labs and challenges) — flag contracts, execution beacons, gated solutions, difficulty ladders derived from disclosed reports, and headless verification that proves every level is solvable. Use when authoring or fixing a local training app such as VulnVerse, adding challenge levels, wiring flag submission, or gating write-ups until a first attempt.
---

# Vulnerable Training Labs

For building the thing, not attacking it: local platforms where a learner breaks
deliberately vulnerable apps and the server proves the break happened.

Read `references/vulnverse-contract.md` for a fully worked implementation
(routes, meta contract, four challenge designs, verification commands).

To *attack* a stock lab (DVWA and friends) rather than build one — session bootstrap, the
low→medium bypass table, and paste-ready curl chains for SQLi/CMDi/LFI/upload-RCE/XSS/CSRF —
read `references/dvwa-attack-chains.md`.

## 1. Non-negotiable safety shell

- Bind to loopback only and **refuse to start** on any other interface. A lab is
  a loaded gun pointed at whoever runs it; make the bind guard hard-coded, not a
  config default.
- In-memory state only. Killing the process must reset every session, flag and
  stored record.
- Mark every target page visibly: "intentionally vulnerable · do not deploy".

## 2. The flag contract (this is what makes a level gradeable)

A level is solved only when a flag that lives **in the target page** is
exfiltrated and submitted. Never string-match the payload.

1. Attempt: `POST /<lab>/api/level/:id/attempt` → one-time `sig` + a URL that
   will render the payload + a per-session, per-level flag.
2. The flag is planted in the target page as `<meta name="vv-flag">` alongside
   `<meta name="vv-sig">`. The lab UI never receives it.
3. Payload executes in the page → calls `XSSHERO()` **or** opens any dialog →
   helper posts `{sig, flag}` to the beacon endpoint.
4. Beacon accepts only a signature issued **to this session for this attempt**;
   it stores `captured` only if the posted flag matches the issued flag.
5. Submission: `POST /<lab>/api/flag` requires a live attempt **and** captured
   state, rejects a wrong flag, and only then marks the level solved.

Design consequences:

- **Hook the dialogs.** Wrap `window.alert/confirm/prompt`, keep the natives,
  and beacon on the first dialog *caused by the payload*. Without this, a
  learner who types the classic `alert(1)` sees a popup and the lab says "no
  callback" — the single most common "the lab is broken" report.
- Show the flag where the learner is looking: a dialog in the target page right
  after their own dialog closes, and a lab-side modal with a prefilled submit
  box. Popup ≠ solved; submission is still required.
- Persist `captured` + flag into the page (`data-captured`, `data-flag`) so a
  reload after capture still lets the learner submit. Easy to miss, and it
  strands anyone who refreshes.
- Put the beacon URL in `<meta name="vv-beacon">` and read it in the helper, so
  multiple labs share one helper file instead of hard-coding a path.

## 3. Gated solutions

The write-up is earned, not shown:

- Server-side gate: `attempts === 0` → render the **locked panel**, not the
  write-up. Hiding the nav link is not a gate.
- Assert in tests that the locked page does **not** contain the working payload
  string, and that it does after one attempt.
- A `/solutions` index must list per-level rows as "Locked — attempt it first"
  with a hints-only link; don't leak payloads there either.
- Hint ladder: tier 1 free, tier 2 after 1 attempt, tier 3 after 2. A wrong
  guess still counts as an attempt — the point is to make them act.
- Endpoint/parameter stay withheld until the first attempt; the console builds
  the request, so the learner can always make the first move.

## 4. Console flows

Support three flows behind one console script (`data-api`, `data-flow`,
`data-level` attributes):

- `link`: set `iframe.src` to the URL containing the payload.
- `submit`: persist the payload, then open the staff/bot view that renders it.
- `postmessage`: load the page, then `frame.contentWindow.postMessage({html: <box>}, '*')`
  after `load`. **JSON-parse the payload box** when it is valid JSON, so an
  array/object is delivered through the structured clone algorithm — that is the
  whole technique for a string-only escaper bypass.

## 5. Designing challenges from real reports

Do not invent mechanics; lift one documented bug per challenge and rebuild the
minimum app that reproduces it:

| Difficulty | Mechanic to build | Report shape |
|---|---|---|
| Basic | blocklist that removes one tag name; event-handler vector beats it | FILT/REFL tag-blacklist |
| Medium | regex sanitiser before `innerHTML`; parser repairs the leftover `<` | DOM-020 (grab.com) |
| Hard | filter runs **before** Unicode NFKC normalisation; fullwidth delimiters fold after validation | STOR-142/143 (Rockstar) |
| Expert | `postMessage` with no origin check + escaper that only handles strings; array bypasses it | DOM-018 (Shopify) |

Keep the source payload verbatim when it exists (e.g. the fullwidth string), and
cite the case ID in the brief and write-up. The difficulty is the discovery, not
the typing.

## 6. Verification: three suites, all headless

1. **Answer-key suite** — every level and every randomised variant, driving the
   real target URL in a browser, asserting capture → submit → solved.
2. **Execution suite** — only `alert(1)` / `onerror=alert(1)` payloads, asserting
   auto-beacon, flag popup and submission on reflected, DOM and stored flows.
3. **Gating suite** — locked before attempt, payload absent while locked,
   unlocked after one attempt, wrong flag rejected, UI modal submit solves.

Rules for all of them:

- Attach `page.on('dialog', d => d.dismiss())` **before** the first navigation
  and on every new page, or CDP dialogs park the renderer (see
  `local-browser-automation` §7).
- Register pacing as part of the suite: N rapid attempts on one level must end
  in `429`.
- Reset between runs is unnecessary (state is in RAM); use a fresh session per
  case when a test needs a clean attempt count.

## 7. Pitfalls that already cost time

- **Rate limiter vs string ids.** `e.level === Number(level)` never matches ids
  like `r1`/`c4`; the throttle silently never fires. Normalise both sides to
  `String(level)`.
- **One helper, many labs.** Hard-coded `/xss/api/beacon` breaks the moment a
  second lab exists. Meta-driven endpoint from day one.
- **Blind levels still pop dialogs.** A hidden iframe executes and shows the
  flag dialog; if that breaks the blind fantasy, accept it as the reward or
  suppress the second dialog for hidden frames.
- **CSP levels need a file, not inline.** The helper must be served as
  `/js/xsshero.js`; inline `<script>` dies under `script-src`.
- **Class-name collisions in a shared stylesheet.** New lab UI components must
  not reuse generic `.sol-row`-style names; see `local-browser-automation` §9
  for the measured layout-QA loop.

## 8. Reporting the work

Show real output: suite counts, a captured flag, a `429` from the throttle, and
the measured alignment numbers. Never claim "verified" from reading code.
