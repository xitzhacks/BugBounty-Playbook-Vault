---
title: "Vault/Open-Redirect — open redirect & OAuth-flow playbook set"
type: index
category: "Open Redirect (all types: core param/path redirects, OAuth/SAML redirect_uri flows, redirect→token/ATO chains, filter validation bypasses, Host/Referer-controlled redirects, redirect→XSS, opener control/reverse tabnabbing, adjacent-row triage)"
built: "2026-10-29"
evidence: "198 roster rows from h1.security.nathan.sx mirror → 129 retrievable bodies read (109 resolved / 15 informative / 3 duplicate / 2 not-applicable; 11 adjacent + 1 noise excluded from class counts) · 69 × 404 recorded"
bounty: "$46,891 roster-tagged grand total across 92 rows (JSON-verified $16,070/26 · list-stated $24,163/42 · dead-404 list $6,658/24) · pure redirect-class 01–07 $36,523 · adjacent/noise 08 $3,710 · full reconciliation in references/case-register.md"
companion_vaults: "../XXE · ../SQLi · ../SSRF · ../XSS · ../IDOR · ../CSRF"
case_id_scheme: "RDIR-<HackerOne report id>"
quote_rule: "byte-true, (sic)-marked, from read bodies only; 404 rows recorded never quoted"
---

# Vault/Open-Redirect — the Open Redirect & OAuth-flow playbook set

## Start here

| # | File | What it gives you |
|---|---|---|
| 1 | [`Open-Redirect-Testing-Agent-Playbook.md`](Open-Redirect-Testing-Agent-Playbook.md) | **The executable protocol.** P0 redirect-surface inventory → P1 cheapest-first probe matrix → P2 lane decision tree → P3 escalation → P4 discipline gates (browser divergence, fix-watching, modern-hardening fingerprinting) → P5 report assembly + K1–K8 kill-gates. |
| 2 | [`01_Core-Param-Redirects.md`](01_Core-Param-Redirects.md) | The param/path lane (50 cases). Anchors: RDIR-125791 (uber root-path `//example.com`, $3,000 JSON — class-topping), RDIR-55546/RDIR-103772 (suffix `.mx`/`.np` login+checkout, $1,400/$500 list), RDIR-39198/RDIR-125000 (path-redirect family), RDIR-161991 (trusted-surface `last_shop`). |
| 3 | [`02_OAuth-SSO-Redirect-Flows.md`](02_OAuth-SSO-Redirect-Flows.md) | The OAuth/SAML lane (13). Anchors: RDIR-26962 (rfc6749 error-redirect, $3,000 JSON), RDIR-2575 (Slack redirect_uri suffix, $100 list), the Weblate `next=` cluster (223326/223718/224317/238117), the SAML `sign_in` lane (171398 → 178345). |
| 4 | [`03_Redirect-Token-ATO-Chains.md`](03_Redirect-Token-ATO-Chains.md) | The paying chains: destination receives POST body / token / Referer (8). Anchors: RDIR-49759 (authenticity_token POST capture, $1,400 JSON), RDIR-108113 (Digits `%ff@` callback, $2,520 list), RDIR-99435 (Badoo IE11-only hash capture), RDIR-25160 (Disqus token). |
| 5 | [`04_Redirect-Filter-Validation-Bypasses.md`](04_Redirect-Filter-Validation-Bypasses.md) | Redirect only works by defeating an existing protection (19). Anchors: RDIR-104087 (Slack SVG re-breaks every fixed redirect, $1,000 JSON), RDIR-28865 (`/../redirect/` signature bypass), RDIR-51265 (Flash 307 browser-trust, $2,000 list), RDIR-126203 (CBC cut-and-paste EQ blob). |
| 6 | [`05_Host-Referer-Controlled-Redirects.md`](05_Host-Referer-Controlled-Redirects.md) | No parameter needed — the header lane (6). Anchors: RDIR-7357 (IRCCloud Host header, $100 JSON), RDIR-5199 (Coinbase `chk_jschl` Referer), RDIR-210875 (Rockstar Host-poisoned short link → rsg.ms). |
| 7 | [`06_Open-Redirect-to-XSS-Chains.md`](06_Open-Redirect-to-XSS-Chains.md) | The redirect target executes script (7). Anchors: RDIR-48516 (twitter `/intent/` original_referer wall-of-events, $1,400 list), RDIR-177624 (Badoo CRLF→data: URI), RDIR-143240 (Mapbox authorize_url template injection). |
| 8 | [`07_Opener-Control-Reverse-Tabnabbing.md`](07_Opener-Control-Reverse-Tabnabbing.md) | No URL involved — the tab lane (14). Anchors: RDIR-23386 (HackerOne window.opener doctrine, $500 JSON), RDIR-211065 (GitLab 404-disguise phishing), RDIR-160498 (Coinbase WebKit completeness), RDIR-212629 (GitLab parser bypass, medium). |
| 9 | [`08_Adjacent-Noise-Rows.md`](08_Adjacent-Noise-Rows.md) | The triage honest layer: 11 adjacent + 1 true noise (RDIR-29480 IRC command injection caught by the "unvalidated" arm). Adjacent anchor: RDIR-191196 (G Suite redirect → ubereats.com DoS, $2,500 list). |

## References (provenance layer)

| File | Contents |
|---|---|
| [`references/source-index.md`](references/source-index.md) | Roster provenance (nathan.sx mirror, 4,419 rows), filter pattern + rejected candidate arms, funnel (198→129+69, retry arithmetic exact), era statistics, program histogram, bounty-reconciliation table, companion sources, 7 limitations. |
| [`references/case-register.md`](references/case-register.md) | Row-per-row ledger of all 198 roster rows: case ID, team, substate, bounty (JSON vs list labeled per row), class (01–08/dead), disposition notes. Grand-total reconciliation + adjacent/noise honesty + exact 404 list. |
| [`references/blogs-index.md`](references/blogs-index.md) | §1 zseano open-redirect guide (fetched, byte-quoted: doctrine, 14-dork list, `response_type=token` hash smuggling, encode-once/double-encode, SSRF-blacklist bypass, 302-vs-javascript XSS note, 21-entry bypass list incl. fullwidth period) · §2 136 title-linked bugbountyhunting.com writeups in 8 sections + 4 filter-artifact rows · §3 six modern skill-cited cases (GitHub Gist ATO $10,000, Open Sesame, Airbnb 1-char, detectify OAuth paper, Rails 7.0, CVE-2022-33987). |
| [`references/archive/bodies-full-dump.txt`](references/archive/bodies-full-dump.txt) | All 129 retrieved report bodies, verbatim dump, plus the 69 dead-row markers (fallback chain body → vulnerability_information → activity_summary → team summaries[]). |
| [`references/archive/json/`](references/archive/json/) | All 198 raw JSON responses from `hackerone.com/reports/<id>.json` (69 are preserved 404 pages). |
| [`references/archive/roster-mirror-rows.json`](references/archive/roster-mirror-rows.json) | The 198 roster rows as parsed from the mirror (regeneration source). |
| [`references/archive/bounty-reconciliation.json`](references/archive/bounty-reconciliation.json) | Per-row bounty reconciliation (src: json/mirror/404-mirror/none + class). |
| [`references/archive/http-codes.txt`](references/archive/http-codes.txt) | The 69 dead-404 ids as fetched (full ledger, both attempts). |

## How this vault was built (method)

1. **Roster**: full HTML of `h1.security.nathan.sx` (4,419 public H1 reports, frozen
   2017-09-12) filtered on the redirect-family title pattern plus five targeted arms
   (tabnabbing/opener, phishing, `callback_url`, external-URL, URL-sanitize) → 198 rows; two
   broad candidate arms tested and rejected on body sampling (recorded in source-index §1).
2. **Retrieval**: every report fetched from the public unauthenticated
   `hackerone.com/reports/<id>.json` endpoint, 1.2s spacing → 129×200, 69×404; all 53 transient
   failures recovered on retry (funnel arithmetic exact). Session-restart note: the original
   fetch was cancelled and the workspace wiped; the roster was regenerated deterministically
   from the mirror (byte-identical, 198 rows / $46,891) and the fetch restarted from zero.
3. **Reading**: all 129 bodies read end-to-end (`archive/bodies-full-dump.txt`); every class
   decided by bodies, not titles. Twelve roster matches reclassified on body read — 11 adjacent,
   1 true noise (RDIR-29480 IRC command injection) — recorded in module 08, excluded from class
   counts, never silently dropped.
4. **Bounty accounting**: JSON `bounty_amount` where present ($16,070 across 26 rows),
   otherwise the mirror's list-stated figure, labeled per row; 43 fetched rows carry
   `has_bounty?:true` with the amount withheld (labeled list); $6,658 sits on unrecoverable
   404 rows (list figures).
5. **Modules**: eight modules (seven redirect lanes + the adjacent/noise triage layer), each
   with verbatim evidence, an agent execution template, validation gates, adjacency, and
   archive-label-honesty notes.
6. **Bibliography**: zseano's open-redirect guide fetched and byte-quoted (the only blog body
   fetched this build); 136 community writeups title-linked in eight sections; post-2017
   modern cases kept bibliographic only, never blended into register counts.

## Coverage vs limitations

**Covered**: core param/path redirects (suffix/dot tricks, integer-IP hostnames, path-segment
families, trusted-surface params), OAuth `redirect_uri` validator gaps and rfc6749
error-redirect flows, SAML `sign_in` + social-login `next=` lanes, redirect→token/ATO chains
(authenticity_token POST capture, OAuth hash capture, Digits `callback_url`, Disqus), the five
failed-string-filter bypass families plus the five fixed-then-rebroken clusters, Host/Referer
header-controlled redirects, redirect→XSS (`javascript:`/`data:`/reflected-context emission),
opener control and reverse tabnabbing (incl. the 404-disguise phishing upgrade), and the
adjacent/noise triage layer.

**Honest limitations**:
1. The roster is a 2014–2017 snapshot (mirror frozen 2017-09-12) — browser-default
   `rel=noopener` (2021), SameSite-era cookie behavior, OAuth exact-match validators and PKCE
   postdate it; playbook P4 fingerprints hardening before payloads and labels era-techniques.
2. 69 rows are permanently dark (404, 34.8% — the highest of the three vault builds) —
   recorded, never quoted; $6,658 of list figures.
3. 11 fetched rows expose no reporter body (empty info fields; team-summary fallback captured
   where the team wrote one; two rows are one-liners).
4. Blog bodies were not fetched this build (except the zseano guide) — `blogs-index.md` §2 is
   a hunt queue, not proof; `zseano.com/blogs/2.html` was unreachable (fetch failed twice,
   recorded title-only).
5. Weakness labels are era values and often wrong (RDIR-29480's "Open Redirect"-family label
   caught an IRC command injection) — the register keeps the archive label, modules correct
   against the body ("bodies win").
6. No live testing was performed — validate against the hunt-open-redirect skill's scenario
   matrix before relying on any payload in a modern target.

## The one-paragraph doctrine of this corpus

Open redirect in this corpus is a **trust-transfer primitive**, and the economics prove it:
the reports that found the redirect and argued "phishing could happen" stayed at $0–$100
(informative/none dominates: 98 of 129 severity-none), while every report above $1,000 did one
of three things — it showed the *destination* trusting attacker-chosen state (an
authenticity_token POSTed cross-domain, an OAuth `#access_token` hash, a `callback_url` the
server still signs), it showed the *tab* staying attacker-steerable after the hop
(window.opener, reverse tabnabbing, a 404 page disguising the swap), or it re-opened a door the
vendor had already nailed shut (five fixed-then-rebroken clusters; RDIR-104087's
"this trick make all fixed open redirect links vulnerable again"). Probes are seconds each;
the payout tracked which trusted surface the redirect touched, not the redirect itself.


<!-- CASESTOCK-LINK:BEGIN -->

## Case stock — vault (`_VAULT/`)

**340 disclosed reports** routed to this category · 68 with a bounty figure · **$32,194** · 210 full write-ups stored locally.

- Full list: [`_VAULT/by-vault-category/Open-Redirect.md`](../_VAULT/by-vault-category/Open-Redirect.md)
- Query: `sqlite3 ../_VAULT/reports.sqlite "SELECT id,bounty,title FROM reports WHERE ..."`
- Pull one write-up: `python3 ../_VAULT/scripts/extract_report.py <id>`

| Top paid | Program | Bounty |
|---|---|---|
| [26962](https://hackerone.com/reports/26962) open redirect in rfc6749 | Internet Bug Bounty | $3,000 |
| [1865991](https://hackerone.com/reports/1865991) Open Redirect Vulnerability in Action Pack | Internet Bug Bounty | $2,400 |
| [683298](https://hackerone.com/reports/683298) XSS and Open Redirect on MoPub Login | X / xAI | $1,540 |
| [49759](https://hackerone.com/reports/49759) Open Redirect leak of authenticity_token lead to full account take over. | X / xAI | $1,400 |
| [469803](https://hackerone.com/reports/469803) Open redirect at https://inventory.upserve.com/http://google.com/ | Upserve  | $1,200 |

_refreshed 2026-11-17 from the public HackerOne disclosed-report dataset_
<!-- CASESTOCK-LINK:END -->
