---
title: "Open Redirect Testing Agent Playbook — the executable protocol"
type: agent-playbook
category: open-redirect-all
cwe: "CWE-601"
built: "2026-10-29"
corpus: "198 mirror rows → 129 bodies read (109 resolved / 15 informative / 3 duplicate / 2 not-applicable) · 69×404 recorded"
bounty: "$36,523 pure redirect-class (JSON-verified $16,070/26 rows · list-stated $24,163/42 fetched rows) · $3,710 adjacent/noise (module 08) · $6,658 dead-404 list figures · grand $46,891/92 rows"
companion_modules: "01 core-param · 02 oauth-sso · 03 token-ATO-chains · 04 filter-bypasses · 05 host-referer · 06 xss-chains · 07 opener-tabnabbing · 08 adjacent-noise"
quote_rule: "byte-true, (sic)-marked, from read bodies only; 404 rows recorded never quoted"
---

# Open Redirect Testing Agent Playbook

Executable protocol derived from 129 read bodies (2014–2017 era) + modern discipline from the
hunt-open-redirect skill. Every step cites its corpus evidence. Run phases in order; abort at
kill-gates. Crown-jewel doctrine up front, because it is the whole point of the class:
**open redirect alone is Low; chained to OAuth/token capture it is the class's $1,400–$3,000 lane.**

## P0 — Redirect-surface inventory (always first)

1. **Parameter inventory** (crawl + JS + dorks). The zseano guide's dork list, byte-quoted in
   `references/blogs-index.md` §1: `go, return, r_url, returnUrl, returnUri, locationUrl, goTo,
   return_url, return_uri, ref=, referrer=, backUrl, returnTo, successUrl` — plus corpus param
   names the guide omits: `redir` (2622, 16718), `retURL` (2414), `redirect_url` (39631),
   `redirect_to` (129091), `return_path` (77221), `return_to` (55546, 169759, 175168),
   `checkout_url` (103772, 159522), `continue` (6357), `next` (223326), `callback_url` (108113),
   `noredirect` flag pair (246897), `recipient` (49759), `host` (214034), `sub_link` (145306).
2. **Path-redirect probes** — no parameter needed: `//evil.com`, `/en//evil.com/`,
   `/%2F1572395042` (IP-integer), `///;@evil.com` (211213). Evidence: the two $3,000 rows are both
   *path* redirects (125791 uber `/en//example.com/`, 104087's re-break pattern).
3. **Header-generated redirects** (module 05): replay every 30x with `Host: evil.com` and
   `Referer: https://evil.com`. Evidence: 7357, 94637, 158019, 5199, 210875.
4. **Auth-flow inventory** (module 02): OAuth authorize endpoints, social-login URLs, SAML
   sign-in, app-callbacks. Evidence: 2575, 26962, 55525, 223326, 178345.
5. **Protection inventory** (module 04): interstitial/warning pages, signature-gated redirects,
   whitelists, encrypted targets. Evidence: 28865, 111968, 44157, 126203.

## P1 — Cheapest-first probes (seconds each, corpus-ordered)

| # | Probe | Cost | Corpus proof |
|---|---|---|---|
| 1 | `?p=https://evil.com` on every inventoried param | ~5s | 2622, 2414, 13553 |
| 2 | `?p=//evil.com` protocol-relative | ~5s | 76738, 77221, 113112, 160047 |
| 3 | Slash sweeps: `///`, `/////, /\/` | ~10s | 223326 (`///`), 175168 (`/////`) |
| 4 | Dot-segments `/%2e%2e` after path | ~5s | 39198, 125000 |
| 5 | Suffix-join `.mx/` `.np/` | ~5s | 55546, 103772 |
| 6 | Authority `@evil.com`, `;@evil.com` | ~5s | 155222, 211213, 39631 |
| 7 | IP-integer host | ~10s | 57163, 50752 |
| 8 | Path-position: `/en//evil.com/` | ~5s | 125791, 119236 |
| 9 | Host/Referer swap on 30x endpoints | ~30s | module 05 rows |
| 10 | OAuth error-redirect: `scope=WRONG&redirect_uri=attacker` | ~10s | 26962, 55525 |
| 11 | `response_type=token` hash-smuggling probe | ~10s | zseano §1; 99435 |
| 12 | Social-login `next=` sweep on connect/disconnect | ~30s | 223326, 224317, 238117 |

## P2 — Lane decision tree (which module owns the finding)

```text
Redirect confirmed →
├─ plain param/path redirect, no state at destination .......... 01 Core Param
├─ redirect inside OAuth/SAML/social flow ...................... 02 OAuth & SSO
├─ destination receives POST body / URL token / Referer ........ 03 Token-ATO chains
├─ redirect only works BY BYPASSING an existing protection ..... 04 Filter Bypasses
├─ redirect target comes from Host/Referer header, not a param .. 05 Host/Referer
├─ destination executes script (javascript:/data:/reflected) ... 06 XSS Chains
├─ no URL involved: window.opener / target=_blank / iframe ..... 07 Opener & Tabnabbing
└─ no redirect mechanism in body at all ........................ 08 Adjacent/Noise (record only)
```

## P3 — Escalation (only after a lane confirms)

1. **Ask "what state reaches the destination?"** — POST body (49759: authenticity_token),
   fragment (99435: `#access_token=`), referrer (140432), popup data (207170: xoxs).
   Capture on your infrastructure; prove the token *usable* (108113's "account renamed Pwn3d"
   standard).
2. **Trusted-surface escalation** — redirects that ride company emails (145306), admin panels
   (161991, 153652), or generate persistent links (210875's `rsg.ms` poisoning).
3. **Same-origin content escalation** (module 04): can the destination be attacker content on
   the target's origin (104087 SVG, 140447 HTML)? Then every same-origin validator re-breaks.
4. **Redirect-target compromise** (158148): own the hop, host the phish on the trusted chain.
5. **XSS handoff** (module 06): `javascript:`/`data:` targets; Referer-gated reflections
   manufactured by the flow itself (48516).

## P4 — Discipline gates

1. **Browser divergence is part of the finding** — 99435 (IE11/Edge only), 160498 (WebKit opener
   gap), 34084 (terminal preview ≠ download), 23386 (Firefox Android: no URL bar). Name
   browser+version; test in at least two engines.
2. **30x-only endpoints kill `javascript:` payloads** — zseano §1 (byte-quoted): *"If it's a 302
   redirect then it will not work, but if they are redirecting via javascript then it will work."*
   Identify the emission context before payload claims.
3. **Fix-watching is part of the loop** — five fixed-then-rebroken clusters in the corpus
   (155222 after 55546; 165046 after 159522; 178345 after 171398; 104087 after 2622; 28865's
   `/secure` variant). Re-test every fix you triggered within days.
4. **Encoding discipline for OAuth chains** (zseano §1, byte-quoted): encode the inner redirect
   once (`%3Fgoto%3D`), double-encode the FINAL URL when the flow redirects twice.
5. **Impact honesty**: redirect alone = Low. Every report above Low in this corpus carries a
   demonstrated chain. No "could potentially" phrasing — the corpus rejected rows (29480 NA-adjacent
   triage) show what noise looks like.
6. **Modern-era fingerprinting before payloads** (post-2017 hardening): SameSite-era session
   cookies and browser-default `rel=noopener` (2021) change 07's exploitability; OAuth redirect_uri
   exact-match validators and PKCE change 02's surface. Corpus claims older than these need a
   fingerprint step first.
7. **Rate/destructive discipline**: 191196 shows redirect bugs can be accidentally destructive
   (DoS) — never point redirects at production-shared infrastructure in testing.

## P5 — Report assembly (corpus templates)

1. **Header**: endpoint + param (or path/header source), method (302/303/301/client-side), browser
   matrix for conditional rows.
2. **Steps-to-reproduce block** (the 2414 shape — 4 lines: go, fill, intercept, submit), plus the
   raw `Location:` echo.
3. **Impact block in the victim's eyes** (119236's model):
   > A user can be sent a URL link that can lead to malicious content. The user will believe the
   > link is trust-worthy because it still has the name of Uber.
4. **Chain evidence** for above-Low claims: capture log / video / renamed-account proof.
5. **Fix suggestion** — corpus template (2622): *"Proper checks should be there on the redir
   parameter that should only allow to redirect on slack.com URL."* Prefer allowlist-of-destinations
   over string filters; module 04 documents five failed string filters.

### Kill-gates (any ⇒ do not submit)

- **K1**: No 30x/client-side redirect produced from the target origin (echo without emission).
- **K2**: The "redirect" is your own URL echoed in a 404/error page (text injection — module 08 class).
- **K3**: Destination validation holds in every shape after the full P1 matrix (12 probes minimum).
- **K4**: The only impact stated is "phishing could happen" with no trusted-surface or chain demo
  — this is the corpus's most-downgraded claim shape.
- **K5**: Content spoof only (213056 class) — belongs to a different vault; don't cross-file as redirect.
- **K6**: Browser-conditional finding reported without naming the browser or testing a second engine.
- **K7**: The redirect target requires attacker same-origin content but you haven't demonstrated
  the storage path (104087-class claims need the upload proof).
- **K8**: Fix-bypass claim without linking the original fixed report (the corpus's 155222/165046
  standard).

## References

- Modules 01–08 (same directory).
- `references/source-index.md` — provenance, funnel (198→129+69), era stats, bounty reconciliation.
- `references/case-register.md` — all 198 rows with per-row bounty labels and verdicts.
- `references/blogs-index.md` — §1 zseano guide (byte-quoted), §2 136 writeups, §3 modern cases.
- Companion skills: hunt-open-redirect (chain table, bypass payloads), hunt-ato (ATO chains).
