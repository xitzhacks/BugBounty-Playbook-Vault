---
title: "Authentication & Session source index — provenance, funnel, fetch mechanics, limitations"
type: source-index
built: "2026-10-29"
---

# Source index — Authentication & Session build

## 1. Roster provenance

- **Primary roster**: full HTML of `h1.security.nathan.sx` — 4,419 public HackerOne report rows,
  snapshot frozen **2017-09-12**. Same mirror as the `../XXE`, `../CSRF` and `../Open-Redirect`
  builds (byte-identical parse: 4,419 unique report rows).
- **Title filter** — 15 case-insensitive arms applied to mirror titles:
  `auth(s)? ?bypass|bypass(ing)? (the )?auth…` (bypass-core) · `logged ?in as|log(in|ged) as (any|another|admin)` (logged-in-as)
  · `session (fixation|hijack|management|handling|invalidation|expiration|expiry|validation|persistence|timeout|token)|insufficient session` (session-family)
  · `2fa|two[- ]factor|multi[- ]factor|mfa|otp|one[- ]time (pass|pin|password)|verification code` (mfa-2fa)
  · `broken( |-)auth|improper( |-)auth(entication)?` (broken-improper-auth) · `account takeover|impersonat` (ato-impersonation)
  · `password (reset|change)|reset (token|link|password)|forgot` (reset-token) · `logout|log ?out` (logout)
  · `email (change|verification|verify)|verif(y|ication) email` (email-change / email-verification)
  · `passwordless` (passwordless) · `sso|saml|single sign` (sso-saml) · `login (as|any|without)|log in` (login-any)
  · `token (expir|invalid)|expir(ed|ing) token` (token-expiry) · `cookie.*(invalidat|expir|session)|(session|cookie).*(invalidat)` (cookie-invalidation)
- Funnel: 4,419 mirror rows → **213 base-roster matches** (92 bounty-tagged on the list) →
  **188 retrieved bodies** read end-to-end + **36 dead-404** recorded.
- **Supplemental pass (documented, post-roster)**: an earlier preview arm (`oauth\s+auth…`)
  and the plain-cookie arm had been dropped when the 15-arm filter was frozen. A re-diff of
  preview matches against the frozen roster surfaced 60 dropped rows — 49 were cookie-flag /
  cookie-injection rows (correctly excluded: misconfig/XSS class), but **11 were auth-lane
  relevant**: 4 OAuth-binding titles (215381, 166942, 65825, 87040) + 7 session-cookie titles
  (15619, 178567, 83667, 6927, 232306, 177018, 46109). All 11 were fetched (10 live, 177018 →
  404) and folded into the corpus as `supplemental` rows. Final corpus: **224 rows = 188 live +
  36 dead**.

## 2. Fetch mechanics

- Unauthenticated `https://hackerone.com/reports/<id>.json` returns flat report objects
  (title, substate, severity_rating, bounty_amount, weakness, team{handle}, disclosed_at,
  vulnerability_information). No auth, no cookies. 1.4 s sleep between calls; no transient
  000s this build (one pass, 199 live-relevant fetches incl. supplemental).
- 404 rows: response body is empty → recorded in `http-codes.txt`, never quoted, never
  reconstructed. 36 dead IDs listed in `references/case-register.md` as `404` rows.
- Body dump: `dump.py` → `bodies.txt` (4,284 lines pre-supplemental, +supplemental pass),
  header format
  `===== AUTH-<id> | <title> | sev=<…> | bounty=<…> | substate=<…> | weak=<…> | len=<n>`;
  JSON-PARSE-ERROR rows mark the dead. All 188 live bodies read end-to-end on 2026-10-29
  (zero-length bodies: none).

## 3. Bounty reconciliation rule

JSON `bounty_amount` where present → labeled **json**. Otherwise the mirror list figure →
labeled **list** (the mirror is the frozen 2017-09-12 list state; several disclosures withhold
the amount — `has_bounty?: true` with `bounty_amount: null` — the list figure is the only
source and is labeled as such). Dead rows keep their list figure labeled **404-list**.
Per-row source lives in `archive/bounty-reconciliation.json`.

- JSON-stated: **$58,278 / 28 rows**
- List-stated: **$58,903 / 57 rows**
- Dead-404 list: **$6,238 / 13 rows** (of 36 dead)
- **Grand: $123,419 / 98 rows** — class modules 01–07: $99,360 / 71 rows; module 08
  adjacent+noise: $17,821 / 14 rows.

## 4. BugBountyHunter (bugbountyhunter.com) — taxonomy check

The vulnerability-type index (`/vulnerability/`) has **no** auth/session page — types are:
access_control, apitesting, bugbounty_toolkit, code, command_injection, csrf, fileuploads,
idor, javascript_files, notetaking, open_redirect, sql, ssrf, token, waybackmachine, xss, xxe.
The class's disclosed-stats ledger instead lives on `/disclosed/` (fetched 2026-10-28,
`bbh-disclosed.html`), which banks these CWE-bucket counts (reports / programs):

| CWE bucket | Reports | Programs |
|---|---|---|
| Improper Authentication - Generic (CWE-287) | 771 | 175 |
| Improper Restriction of Authentication Attempts (CWE-307) | 63 | 39 |
| Insufficient Session Expiration (CWE-613) | 40 | 31 |
| Authentication Bypass Using an Alternate Path or Channel (CWE-288) | 22 | 17 |
| Session Fixation (CWE-384) | 16 | 12 |
| Improper Authorization - Generic (CWE-285) | 29 | 57 |
| Incorrect Authorization (CWE-863) | 10 | 14 |
| Authentication Bypass by Primary Weakness (CWE-305) | 1 | 13 |
| Reliance on Cookies without Validation + Integrity Check (CWE-565) | 7 | 8 |
| Missing Authentication for Critical Function (CWE-306) | 5 | 7 |
| Exposure of Data Element to Wrong Session (CWE-488) | 1 | 5 |
| Authentication Bypass by Capture-replay (CWE-294) | 5 | 5 |

Mirror-era crossovers (corpus rows also counted in BBH buckets): AUTH-353/737/288 sit in the
Insufficient-Session-Expiration family; AUTH-2421/6504/135797/255020/193556/2582 in the
Session-Fixation family; AUTH-219205/172137/223014 in the Alternate-Path/Channel family.

## 5. Bug bounty blogs (bugbountyhunting.com)

Full index fetched once: 7,103 entries (`script.js`, 1,383,906 bytes). Auth-session arms
produced **559 raw matches** (`blog-raw-matches.json` in the build workspace), curated to
**303** in `references/blogs-index.md` §2 (originating-class filter, archive-mirror dedupe,
generic-impact titles dropped). Two zseano posts fetched and byte-quoted in §1 — both
post-mirror era (Nov 2017 / Jun 2018), bibliography only.

## 6. Era discipline

- The mirror froze **2017-09-12**; the corpus is a 2013–2017 snapshot (era spread:
  2013×1 · 2014×40 · 2015×20 · 2016×59 · 2017×68).
- Post-2017 cases enter only the bibliography (blogs-index §2/§3), never class counts, and
  modern hardening is fingerprints-in-P4, not corpus doctrine.
- Team names in the register are mirror list names (★ artifact stripped); handles come from
  the fetched JSON.

## 7. Limitations

- **Bounty withholding**: 150 live disclosures have `bounty_amount: null`; 52 (incl. the four
  supplemental OAuth rows) carry a list figure — labeled list. The other 98 live rows are
  bounty-unknown, not bounty-zero.
- **404 rows**: 36 of 224 (16%) — roster-only records; their bodies are gone and were never
  seen. Their class column says `dead` regardless of how auth-flavored the title reads.
- **zseano §1 quotes**: medium.com serves a Cloudflare challenge to curl; the two posts were
  fetched with the webfetch tool (rendered text) and transcribed to build-workspace files as
  the audit source. Vault blockquotes are audit-tested against those files; sentences were
  re-fetch spot-checked byte-identical (both posts re-fetched 2026-10-29 and the audit
  re-run against the fresh transcriptions). The honest label: quotes verified against a
  transcription of a successful fetch, not against curl-able bytes. Audit method: per-
  blockquote probe, exact-normalized matching; 2 of 264 probes matched only after
  whitespace-squash — Medium's renderer collapses list-item line breaks, removing the space
  the blockquote wrap restores (character sequence identical).
- **Title-only rows**: 9 live bodies are one-liners (136885, 90165, 13705, 226518, 179421,
  126235, 255020, 147204, 50703) — short reports are recorded as short; nothing is invented.
- **Russian-language bodies**: AUTH-90165 and AUTH-179421 (VK) were read with the team's
  English summary fields; quotes are marked with their language in module files.
