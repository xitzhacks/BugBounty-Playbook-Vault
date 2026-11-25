---
title: "Vault/CSRF — CSRF & SameSite-era request-forgery playbook set"
type: index
category: "CSRF (all types: login/signup/logout CSRF, OAuth state & account association, token design flaws, validation gaps & bypasses, GET state changes, chained impact — XSS/SSRF/ATO, commerce)"
built: "2026-10-28"
evidence: "229 roster rows from h1.security.nathan.sx mirror → 178 retrievable bodies read (136 resolved / 33 informative / 7 not-applicable / 2 duplicate; 7 noise-excluded) · 51 × 404 recorded"
bounty: "$36,504 CSRF-class grand total (JSON-verified $8,330/18 rows · list-stated $21,824/51 fetched rows · dead-404 $6,400/20 rows) · $1,650 SSRF/SQLi noise excluded · full reconciliation in references/case-register.md"
companion_vaults: "../XXE · ../SQLi · ../SSRF · ../XSS · ../IDOR"
case_id_scheme: "CSRF-<HackerOne report id>"
quote_rule: "byte-true, (sic)-marked, from read bodies only; 404 rows recorded never quoted"
---

# Vault/CSRF — the Cross-Site Request Forgery playbook set

## Start here

| # | File | What it gives you |
|---|---|---|
| 1 | [`CSRF-Testing-Agent-Playbook.md`](CSRF-Testing-Agent-Playbook.md) | **The executable protocol.** P0 carrier/token inventory → P1 cheapest-first strip matrix → P2 lane decision tree → P3 escalation → P4 discipline gates (incl. SameSite reality check) → P5 report assembly + K1–K8 kill-gates. |
| 2 | [`01_Login-Signup-Logout-CSRF.md`](01_Login-Signup-Logout-CSRF.md) | Session-establishment/teardown forgery. Anchors: CSRF-547 (email-confirm login CSRF), CSRF-7531 (anonymous token mint defeats protection), CSRF-229528 (two-link chain). |
| 3 | [`02_OAuth-State-and-Account-Association.md`](02_OAuth-State-and-Account-Association.md) | OAuth/OIDC/OpenID connect-attach-authorize lane. Anchor: CSRF-215381 (Periscope, $2,520 list — class's largest figure); Pinterest six-step binding proof. |
| 4 | [`03_Account-Takeover-Chains.md`](03_Account-Takeover-Chains.md) | The paying chains: email-change→reset, provider/2FA binding, deletion. Anchors: CSRF-6910 ($500), CSRF-127703 (Badoo `rt` leak, $852), CSRF-155774 (Slack 2FA-SMS, $500 JSON). |
| 5 | [`04_Token-Design-Flaws.md`](04_Token-Design-Flaws.md) | Leak/rotation/binding/framework doctrine. Anchors: CSRF-15412 ($1,000 JSON), CSRF-26647 (Django GA `__utmz` bypass, $1,000), CSRF-49935 (rails-ujs cross-origin tokens, $1,000). |
| 6 | [`05_Validation-Gaps-and-Bypasses.md`](05_Validation-Gaps-and-Bypasses.md) | Blank-token clusters, referer-only checks (CSRF-52635 UniFi), PHP type juggling (CSRF-86022), routing artifacts, double-token confusion. |
| 7 | [`06_GET-State-Changes.md`](06_GET-State-Changes.md) | The img-tag lane. Anchors: CSRF-226418 (JIRA exfil, $500 JSON), CSRF-174328 (no_auth_mode, $500 JSON), CSRF-96470 (export users, $500 JSON). |
| 8 | [`07_Chains-Commerce-Impact.md`](07_Chains-Commerce-Impact.md) | CSRF as delivery: stored-XSS (CSRF-125594 Uber server-compromise), SSRF (Press-This), persistent-CSRF purchase lock (CSRF-206319), commerce mutations, WordPress plugin cluster. |

## References (provenance layer)

| File | Contents |
|---|---|
| [`references/source-index.md`](references/source-index.md) | Roster provenance (nathan.sx mirror, 4,419 rows), filter pattern, funnel (229→178→157 full bodies), program histogram, era statistics, fetch mechanics, 7 limitations. |
| [`references/case-register.md`](references/case-register.md) | Row-per-row ledger of all 229 roster rows: case ID, team, bounty (JSON vs list labeled per row), class (01–07/noise/404), disposition notes. Bounty reconciliation + noise-row honesty + exact 404 list. |
| [`references/blogs-index.md`](references/blogs-index.md) | §1 zseano CSRF guide (fetched, byte-quoted: blank-token→clickjack chain, POST↔GET swap, JSON `=`-smuggling, referer injection, blank-referer iframe, Firefox data:-URI null-Origin) · §2 119 title-linked bugbountyhunting.com writeups (bodies not fetched — marked) · §3 five modern skill-cited cases (GitLab $3,370, Stripe $5,000, GitHub ES $10,000, Argo CD, H1 #1727221). |
| [`references/archive/bodies-full-dump.txt`](references/archive/bodies-full-dump.txt) | All 178 retrieved report bodies, verbatim dump (5,813 lines, fallback chain body→vulnerability_information→activity_summary). |
| [`references/archive/json/`](references/archive/json/) | All 229 raw JSON responses from `hackerone.com/reports/<id>.json` (51 are preserved 404 pages). |
| [`references/archive/bounty-reconciliation.json`](references/archive/bounty-reconciliation.json) | Per-row bounty reconciliation (src: json/mirror/404-mirror/none + class). |
| [`references/archive/http-codes.txt`](references/archive/http-codes.txt) | The 51 dead-404 ids as fetched. |

## How this vault was built (method)

1. **Roster**: full HTML of `h1.security.nathan.sx` (4,419 public H1 reports, frozen
   2017-09-12) filtered `csrf|cross[- ]?site request|same[- ]?site|request forgery` → 229 rows.
2. **Retrieval**: every report fetched from the public unauthenticated
   `hackerone.com/reports/<id>.json` endpoint, 1.2s spacing, disk-cached → 178×200, 51×404
   (one transient fetch failure, 257237, refetched by hand — funnel arithmetic exact).
3. **Reading**: all 178 bodies read end-to-end (`archive/bodies-full-dump.txt`); every class
   decided by bodies, not titles. Seven roster matches reclassified as noise on body read
   (4× SSRF, 1× SQLi-title dead, 2× FPD-on-failure) — recorded, excluded from class counts.
4. **Bounty accounting**: JSON `bounty_amount` where present ($8,330 across 18 rows),
   otherwise the mirror's list-stated figure, labeled per row; $6,400 sits on unrecoverable
   404 rows (list figures).
5. **Modules**: seven class modules, each with verbatim evidence, an agent execution
   template, validation gates, adjacency, and archive-label-honesty notes.
6. **Bibliography**: zseano's CSRF guide fetched and byte-quoted; 119 community writeups
   title-linked (bodies not fetched this build — marked); modern post-roster cases kept out
   of register counts.

## Coverage vs limitations

**Covered**: login/signup/logout CSRF (incl. anonymous-token minting), OAuth state-fixation
and identity-binding chains, CSRF→ATO (email-change→reset, providers, 2FA-SMS relay), token
leakage/rotation/binding/framework doctrine (GA `__utmz`, rails-ujs, SOP/UXSS read lanes,
type juggling), the four-strip validation-gap matrix, referer/origin absence-proofs, GET
state-change tiers, CSRF→XSS/SSRF chains, persistent/commerce CSRF, JSON content-type
smuggling.

**Honest limitations**:
1. The roster is a 2014–2017 snapshot (mirror frozen 2017-09-12) — SameSite=Lax-by-default
   (2020) and per-form framework tokens postdate it; playbook P4 fingerprints hardening
   before payloads and labels era-techniques.
2. 51 rows are permanently dark (404) — recorded, never quoted; $7,750 of list figures
   ($6,400 CSRF-class).
3. 21 rows are metadata-only — titles + figures recorded, no technique content.
4. Blog bodies were not fetched this build — `blogs-index.md` is a hunt queue, not proof.
5. Weakness labels are era values and often wrong (158016 "Code Injection", 76733
   "Information Disclosure") — register keeps the archive label, modules correct against
   the body ("bodies win").
6. No live testing was performed — validate against the hunt-csrf skill's scenario matrix.

## The one-paragraph doctrine of this corpus

CSRF in this corpus is **a settings primitive chained toward ownership**: the $100 reports
found the missing token and stopped; the $500+ reports walked one more step — the email
confirmed, the state parameter absent, the token leaked into a referer, the GET that pushes
private data outward — and each of those single extra steps converted a form-forgery nuisance
into an account takeover, an exfiltration door, or a purchase lock. The probes that found
them are a 30-second strip matrix; the payouts tracked the honesty of the *end-state* the
researcher could demonstrate.


<!-- CASESTOCK-LINK:BEGIN -->

## Case stock — vault (`_VAULT/`)

**516 disclosed reports** routed to this category · 87 with a bounty figure · **$60,528** · 310 full write-ups stored locally.

- Full list: [`_VAULT/by-vault-category/CSRF.md`](../_VAULT/by-vault-category/CSRF.md)
- Query: `sqlite3 ../_VAULT/reports.sqlite "SELECT id,bounty,title FROM reports WHERE ..."`
- Pull one write-up: `python3 ../_VAULT/scripts/extract_report.py <id>`

| Top paid | Program | Bounty |
|---|---|---|
| [1497169](https://hackerone.com/reports/1497169) CSRF protection bypass in GitHub Enterprise management console | GitHub | $10,000 |
| [2326194](https://hackerone.com/reports/2326194) Argo CD CSRF leads to Kubernetes cluster compromise | Internet Bug Bounty | $4,660 |
| [450796](https://hackerone.com/reports/450796) XSSI on refer.xoom.com allows stealing email addresses and posting to Twitter on | PayPal | $3,500 |
| [103787](https://hackerone.com/reports/103787) CSRF possible when SOP Bypass/UXSS is available  | HackerOne | $2,500 |
| [170552](https://hackerone.com/reports/170552) Slack integration setup lacks CSRF protection | HackerOne | $2,500 |

_refreshed 2026-11-17 from the public HackerOne disclosed-report dataset_
<!-- CASESTOCK-LINK:END -->
