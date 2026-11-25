---
title: "MOB Testing Agent Playbook — the executable protocol"
type: agent-playbook
category: mobile
cwe: "CWE-707"
built: "2026-11-07"
corpus: "13 rows -> 10 bodies read (10 full-body / 3 metadata-only GHSL rows) · 2 modules"
bounty: "$6,810 across 7 rows with DB figures (max $2,300 MOB-1011956 metadata) · quotable $2,710 / 4 rows"
companion_modules: "00 android-webview-intent (7 rows) · 01 ios-app-privacy (6 rows)"
quote_rule: "byte-true, from read bodies only; metadata-only rows recorded never quoted"
---

# MOB Testing Agent Playbook — Android/iOS exported surfaces & app privacy

*Evidence base: 13 disclosed h1-brain corpus cases (`MOB-…`), max $2,300 metadata, quotable max $1,500 (MOB-1189162). Every quoted sentence in the modules is byte-true to `references/archive/mob-bodies-full-dump.txt`. Read the line-pointers before improvising; this file is the operational spine.*

## P0 — Program classification & policy read (before any payload)

1. Program type: commercial bug bounty (app) vs VDP vs GHSL detector program. The corpus
   pays demonstrated exported sinks modestly (Shipt $350), privacy-secret moves ($100–$1,500),
   and records detector prices ($2,300/$1,800 metadata) *above* sink prices. Read policy for
   test-device/build rules now: in-scope builds and test accounts only.
2. Environment signal: classify the app surface — exported activities / deep links (Module A)
   vs browser/app trust + secret handling (Module B). The two modules are mechanism-split
   (see P1); inventory both.
3. Kill-gate: no testing yet — P0 produces the *policy envelope* only.

## P1 — Exported-surface inventory

| Surface | Corpus proof | What to map |
|---|---|---|
| Exported activities (manifest `exported` + intent filters) | MOB-283058 (SAMLAuthActivity), MOB-283063 (ImageViewerActivity), MOB-414101 (PushIOMessageViewActivity) | `AndroidManifest.xml` exported flags, `intent-filter` actions/schemes, extra names |
| Deep-link routers (scheme handlers) | MOB-328486 (`zomato://` router → TreatsWebView) | Custom schemes, host-routing branches (`treatswebview`), header attachment (`httpHeaders`) |
| File-picker answers (`GET_CONTENT` / `OPENABLE`) | MOB-1142918 (evil picker steals `shared_prefs`) | Every picker the app calls; what "upload" ultimately reads |
| Browser trust (in-app browser address bar) | MOB-176929 (Brave iOS spoof) | Address-bar binding to the loaded origin |
| Secret handling (`auth_token` in URL; stored settings; E2E keys) | MOB-221558 (GET token), MOB-519059 (setting override), MOB-1189162/MOB-1189168 (key lifecycle) | Token placement, cross-surface state, setup/teardown binding |

Enumerate *every* exported component and *every* secret-storage point, then probe per surface
before chaining surfaces.

## P2 — Probe protocol (ADB baseline → WebView → intent → trust)

1. **ADB baseline** — `adb shell am start -n <pkg>/<activity> -e <extra> …` for every
   exported activity. Every quotable Module-A row ships this one-liner (plus a Java PoC).
   A WebView claim without an intent PoC is the metadata tier, not a finding.
2. **WebView sink read** — trace each extra to its WebView call (`loadUrl`,
   `loadDataWithBaseURL`, `httpHeaders` attach). MOB-414101's `if`-block walk (one intent
   → JS / files / crash / asset) is the template: name *every* payoff through the sink,
   including crash and asset reads.
3. **Intent-extra / picker probes** — remote-source extras (cf. GHSL title MOB-1030295) and
   picker answers (MOB-1142918). Remember the browser is a delivery channel: a BROWSABLE
   scheme + Instant-App reach (MOB-283058's sentence) skips the "installed app" step.
4. **Secret-channel probes** — tokens in URLs (MOB-221558's GET → DORK → cache), cross-surface
   state overrides (MOB-519059's 5-step sequence), key setup/teardown binding
   (MOB-1189162's evil-admin swap; MOB-1189168's remove-and-re-add). State the victim
   interaction each needs ("clicks by accident," "may have to first unset").

## P3 — Proof ladder (the modest demonstrations paid)

1. Intent PoC (ADB + Java) firing against the reporter's own device/build; screenshot of the
   attacker content loaded inside the app's WebView.
2. Multi-payoff table where the sink supports it (MOB-414101's kill / XSS / LFI / asset).
3. Secret proof: DORK result (MOB-221558), before/after setting state (MOB-519059),
   server-swap → encrypt-to-attacker sequence (MOB-1189162), remove → re-add → decrypt
   sequence (MOB-1189168). One sequence per claim, screenshots named.
4. Browser-trust demo: spoof page + loop PoC against the reporter's device — without a
   downstream credential/consent action it is a `None`-tier demo (MOB-176929); write the
   action or accept the tier.

## P4 — Modern hardening fingerprints (never corpus doctrine)

- **Manifest discipline**: `exported=false` by default on every activity; exported
  components allow-listed by signature permission where the feature needs them
  (MOB-283058/283063/414101's exact lesson).
- **WebView discipline**: never load intent extras into `loadUrl`/`loadDataWithBaseURL`
  without origin allow-listing; never attach app `httpHeaders` to attacker-chosen URLs
  (MOB-328486's token leak).
- **Secret handling**: tokens in POST/encrypted bodies, never GET query strings; secrets
  never in search-indexable URLs (MOB-221558's fix: disable indexing + POST).
- **State discipline**: server is the source of truth for user settings; clients never
  overwrite server state from stale local copies (MOB-519059's override).
- **Key lifecycle**: verify private↔public binding at enrollment ("if not, throw a big
  error," MOB-1189162) and destroy keys + mnemonic at account removal (MOB-1189168).
- **Browser trust**: address bar bound to the loaded origin; no `document.write` spoof
  surface (MOB-176929's loop).

## P5 — Pre-report gates (kill-gates)

1. **Intent gate** — you have the ADB + Java PoC reproducing against your build. A manifest
   screenshot without a firing intent dies here.
2. **Sink gate** — you named the WebView call (or the secret channel) that consumed the
   attacker bytes. "Exported activity" with no sink dies here.
3. **GHSL gate** — metadata-only query titles are pricing, never proof (MOB-1011956/
   1030295/1161956). Do not cite them as technique evidence in any report.
4. **Interaction gate** — victim-interaction steps ("clicks by accident," cross-surface
   sequence, already-connected state) are written, as in every paid row's body.
5. **Device gate** — reporter's own device/build and test accounts only. Any plan touching
   production users' devices or accounts dies here regardless of signal quality.

## Module ↔ phase table

| Phase | Corpus evidence (modules) | Anatomy of the paid pattern |
|---|---|---|
| P1 inventories exported surfaces | 00 (§§2–4), 01 (§§2–6) | exported flags; deep-link branches; picker answers; secret points |
| P2 probes ADB → WebView → trust | 00 (§§2–4), 01 (§§2–6) | `am start` baseline; `if`-block payoff table; DORK; state sequences |
| P3 proofs ladder, intent-first | 00 (§§2–4), 01 (§§3–6) | ADB+Java; four-payoff table ($350); DORK ($200); key sequences ($1,500/$100) |
| P4 hardening fingerprints | 00 (§§2–4), 01 (§§3–6) | `exported=false`; WebView allow-lists; POST tokens; key binding |
| P5 kill-gates | 00 (§§5–6), 01 (§7) | intent gate; sink gate; GHSL gate; device gate |

## Non-goals

- Detector authorship (GHSL CodeQL queries) — outside this agent protocol; the three
  metadata rows exist to price detectors, not to teach query-writing.
- General OS exploit development (kernel, baseband, firmware) — outside every module's
  claims; the vault covers exported app surfaces and app-held secrets only.
- Cross-app victim exploitation — all PoCs run on the reporter's own device/build; victim
  interaction steps are described, never executed against real users.
