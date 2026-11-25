---
title: "Vault/Authentication-Session — Authentication Bypass & Session playbook set"
type: index
category: "Authentication & Session (all types: core auth bypass, session fixation & hijack, insufficient session expiration/invalidation, 2FA/OTP bypass, reset-token design, credential change & email verification, SSO/SAML/OAuth identity binding, adjacent cross-class rows)"
built: "2026-10-29"
evidence: "224 roster rows from h1.security.nathan.sx mirror (incl. documented 11-row supplemental pass) → 188 retrievable bodies read (138 resolved / 35 informative / 7 duplicate / 8 not-applicable) · 36 × 404 recorded"
bounty: "$123,419 roster-tagged grand total (JSON-verified $58,278/28 rows · list-stated $58,903/57 fetched rows · dead-404 $6,238/13 rows) · pure class 01–07 $99,360 · adjacent/noise module 08 $17,821 · full reconciliation in references/case-register.md"
companion_vaults: "../CSRF · ../XXE · ../Open-Redirect"
case_id_scheme: "AUTH-<HackerOne report id>"
quote_rule: "byte-true, from read bodies only; 404 rows recorded never quoted"
---

# Vault/Authentication-Session — the Authentication Bypass & Session playbook set

## Start here

| # | File | What it gives you |
|---|---|---|
| 1 | [`Authentication-Session-Testing-Agent-Playbook.md`](Authentication-Session-Testing-Agent-Playbook.md) | **The executable protocol.** P0 auth-surface inventory → P1 cheapest-first probe matrix (12 probes) → P2 lane decision tree → P3 deep exploitation (reach quantification, lifecycle compounding, 2FA state-machine trace, binding CSRF) → P4 modern hardening fingerprints → P5 reporting gates + kill-gates. |
| 2 | [`01_Core-Auth-Bypass.md`](01_Core-Auth-Bypass.md) | The server accepts an attacker without identity proof. Anchors: AUTH-2224/2233 (Phabricator email-domain truncation family), AUTH-245408 (Zomato email-only login, $1,000 json), AUTH-136169/138869 (Uber OneLogin/WordPress trio, $25,000 json), AUTH-215053 (Ubiquiti, $6,000 list). |
| 3 | [`02_Session-Fixation-Hijack.md`](02_Session-Fixation-Hijack.md) | The session identity itself is the flaw. Anchors: AUTH-135797 (Romit, $50 json), AUTH-55911 (Shopify state fixation, $500 json), AUTH-172137/219205 (subdomain-takeover cookie-scope chains, $500 → $5,000 list). |
| 4 | [`03_Session-Expiration-Invalidation.md`](03_Session-Expiration-Invalidation.md) | Sessions that refuse to die. Anchors: AUTH-353/737/288/284 (HackerOne's own program, $200 json + $200 list), AUTH-222082 (OWOX critical), AUTH-250688/245833 (Federalist backdoor/stale-authz). |
| 5 | [`04_2FA-OTP-Bypass.md`](04_2FA-OTP-Bypass.md) | The second factor exists but does not decide. Anchors: AUTH-178293 (Shopify SSO-disables-2FA, $1,500 json), AUTH-163834/167121/179421 (VK trio, $3,050 json), AUTH-128085 (GitLab otp_user_id swap), AUTH-10554 (Coinbase transfer bypass, $1,000 json), AUTH-100509 (H1 pre-generated secrets, $1,000 json). |
| 6 | [`05_Reset-Token-Design.md`](05_Reset-Token-Design.md) | The token is the key — where it lives, how long, who can use it. Anchors: AUTH-173551 (token-in-response, $10,000 json critical), AUTH-143717 (passwordless-signup, $10,000 list), AUTH-17383/17474/23579 (reset-after-email-change family), AUTH-229417/229528 (Weblate auto-login chains). |
| 7 | [`06_Credential-Change-Email-Verification.md`](06_Credential-Change-Email-Verification.md) | Identity edits without proving the old identity. Anchors: AUTH-29331 (H1 username change, $500 json), AUTH-147182/147203 (FantasyTote), AUTH-223461 (Weblate email-change→reset recipe), AUTH-98469 (Binary verify-link duality). |
| 8 | [`07_SSO-SAML-OAuth-Binding.md`](07_SSO-SAML-OAuth-Binding.md) | Who checks the voucher? Anchors: AUTH-223014 (Uber SAML, $8,500 json), AUTH-65825 (Coinbase clickjacked authorize, $5,000 list), AUTH-114169/215381 (Twitter Digits HPP / Periscope authorize-CSRF, $2,520 list each), AUTH-127703 (Badoo `rt` leak, $852 list). |
| 9 | [`08_Adjacent-Noise.md`](08_Adjacent-Noise.md) | The triage honesty ledger: 48 auth-arm titles whose bodies belong elsewhere (13 CSRF-owned, TLS/transport 7 incl. FREAK $7,500, Jenkins auth-flow RCE $5,000, XXE-in-SAML, OAuth-XSS) with cross-vault references. |

## References (provenance layer)

| File | Contents |
|---|---|
| [`references/source-index.md`](references/source-index.md) | Roster provenance (nathan.sx mirror, 4,419 rows), 15-arm title filter + documented supplemental pass (11 OAuth-lane/session-cookie rows), funnel (224 = 188 live + 36 dead), fetch mechanics, BBH taxonomy check (no auth/session type page; the CWE-bucket ledger), era discipline, limitations. |
| [`references/case-register.md`](references/case-register.md) | Row-per-row ledger of all 224 roster rows: case ID, team, substate, bounty (json vs list vs 404-list labeled per row), class (01–08/dead), disposition notes. |
| [`references/blogs-index.md`](references/blogs-index.md) | §1 two zseano auth guides (fetched, byte-quoted: re-signup auto-login takeover; @company.com signup claim pivots) · §2 303 curated title-linked writeups in 7 sections (core bypass, session, 2FA/OTP, reset/verification, SSO/OAuth, doctrine, cross-class chains) · §3 six modern skill-cited cases (Jitsi GHSA-45ff-37jm-xjfx, Linktree H1-1760403, GitHub ES CVE-2025-25291/25292, samlify CVE-2025-47949, Argo CD CVE-2023-22482, jsonwebtoken CVE-2022-23540). |
| [`references/archive/bodies-full-dump.txt`](references/archive/bodies-full-dump.txt) | All 188 retrieved report bodies, verbatim dump (incl. supplemental pass; header `AUTH-<id> | title | sev | bounty | substate | weak | len`). |
| [`references/archive/json/`](references/archive/json/) | All 224 raw JSON responses from `hackerone.com/reports/<id>.json` (36 are preserved 404 pages). |
| [`references/archive/bounty-reconciliation.json`](references/archive/bounty-reconciliation.json) | Per-row bounty reconciliation (src: json/list/404-list/none + class). |
| [`references/archive/http-codes.txt`](references/archive/http-codes.txt) | The 36 dead-404 ids as fetched. |

## How this vault was built (method)

1. **Roster**: full HTML of `h1.security.nathan.sx` (4,419 public H1 reports, frozen
   2017-09-12) filtered by 15 case-insensitive auth/session arms → 213 base rows; a
   documented supplemental pass re-admitted 11 OAuth-lane/session-cookie rows the frozen
   filter dropped → **224 rows**.
2. **Retrieval**: every report fetched from the public unauthenticated
   `hackerone.com/reports/<id>.json` endpoint, 1.4 s spacing, one pass → 188×200, 36×404
   (zero transient failures; funnel arithmetic exact).
3. **Reading**: all 188 bodies read end-to-end (`archive/bodies-full-dump.txt`); every class
   decided by bodies, not titles. AUTH-2559 reclassed 01→07 on body read (OAuth redirect_uri
   mechanism). 48 rows whose bodies belong to other classes recorded in module 08 with
   cross-references.
4. **Bounty accounting**: JSON `bounty_amount` where present ($58,278 across 28 rows),
   otherwise the mirror's list-stated figure ($58,903 across 57 fetched rows), labeled per
   row; $6,238 sits on unrecoverable 404 rows (13 list figures); the four supplemental OAuth
   rows carry `bounty_amount: null` + `has_bounty?: true` → list-labeled.
5. **Modules**: eight class modules, each with verbatim evidence, corpus-proven doctrine,
   test protocol, and era notes.
6. **Bibliography**: two zseano guides fetched and byte-quoted; 303 community writeups
   title-linked (curated from 559 raw matches; bodies not fetched this build — marked);
   modern post-roster cases kept out of register counts.

## Coverage vs limitations

**Covered**: core auth bypass (email-domain trust, single-attribute login, SSO-plugin
auto-provisioning, ticket/feature-gated auth), session fixation & hijack (incl. OAuth-state
fixation and cookie-scope × subdomain-takeover chains), insufficient session
expiration/invalidation (logout/password-change/stale-authz), 2FA/OTP bypass (state-machine
bypasses, brute-force windows, validation design, secret pre-generation, the LegalRobot
rollout family), reset-token design (wire exposure, lifecycle, referer leakage, auto-login
chains), credential change & email verification (the email-change→reset ATO recipe), SSO/
SAML/OAuth identity binding (redirect/callback validation, token-issuer checks,
authorize/binding CSRF, SAML verification).

**Honest limitations**:
1. The roster is a 2013–2017 snapshot (mirror frozen 2017-09-12; era spread 2013×1 ·
   2014×40 · 2015×20 · 2016×59 · 2017×68) — WebAuthn, `__Host-` cookies, SameSite defaults,
   PKCE and session-revocation lists postdate it; playbook P4 fingerprints hardening before
   payloads and labels era techniques.
2. 36 rows are permanently dark (404) — recorded, never quoted; their $6,238 in list figures
   never enters class doctrine.
3. 9 live bodies are one-liners (team acknowledgments or single sentences) — recorded as
   short; nothing invented.
4. VK bodies (163834/167121/179421/90165) are Russian-language; quotes use the team's own
   English summary fields, language-marked in module 04.
5. Blog bodies were not fetched this build (except the two zseano §1 guides) —
   `blogs-index.md` §2 is a hunt queue, not proof; the two §1 quotes are verified against
   transcriptions of successful fetches (medium serves curl a Cloudflare challenge — stated
   in source-index §7).
6. No live testing was performed — validate against the hunt-auth-bypass /
   hunt-mfa-bypass / hunt-session skills' scenario matrices.

## The one-paragraph doctrine of this corpus

Authentication & session flaws in this corpus pay for **what they reach, not what they are**:
the $10,000+ rows never chained anything — they simply reached *any account* or *admin*
(OneLogin auto-provisioning, token-in-response, passwordless-signup state confusion) — while
the same mechanics unchained (session fixation, logout non-expiry, missing email
re-verification) settled at $50–$300 or informative. The corpus's second doctrine is that
**fixes re-break**: three separate fix-rebreak rows (2233, 194832, 178345) and two Weblate
fix-bypass chains exist because the patched surface kept the same trust assumption. The
probes are cheap — a cookie export/replay, a request replay after logout, a parameter strip
on the login call, an OTP-field swap — but the report that pays is the one that demonstrates
cross-user reach end-to-end with two accounts.


<!-- CASESTOCK-LINK:BEGIN -->

## Case stock — vault (`_VAULT/`)

**1,096 disclosed reports** routed to this category · 220 with a bounty figure · **$376,558** · 718 full write-ups stored locally.

- Full list: [`_VAULT/by-vault-category/Authentication-Session.md`](../_VAULT/by-vault-category/Authentication-Session.md)
- Query: `sqlite3 ../_VAULT/reports.sqlite "SELECT id,bounty,title FROM reports WHERE ..."`
- Pull one write-up: `python3 ../_VAULT/scripts/extract_report.py <id>`

| Top paid | Program | Bounty |
|---|---|---|
| [1087489](https://hackerone.com/reports/1087489) Github access token exposure | Shopify | $50,000 |
| [745324](https://hackerone.com/reports/745324) Account takeover via leaked session cookie | HackerOne | $20,000 |
| [739737](https://hackerone.com/reports/739737) Token leak in security challenge flow allows retrieving victim's PayPal email an | PayPal | $15,300 |
| [1328546](https://hackerone.com/reports/1328546) Incorrect authorization to the intelbot service leading to ticket information | TikTok | $15,000 |
| [2443228](https://hackerone.com/reports/2443228) Account Takeover via Authentication Bypass in TikTok Account Recovery | TikTok | $12,000 |

_refreshed 2026-11-17 from the public HackerOne disclosed-report dataset_
<!-- CASESTOCK-LINK:END -->
