---
title: "Vault/24 — Host Header Injection playbook set"
type: index
category: host-header
built: "2026-11-07"
evidence: "4 classified rows → 4 retrievable bodies read (4 full-body / 0 metadata-only) · 0 adjacent rows"
bounty: "$800 across 2 rows with DB figures (max $500, HOST-1783015) · 2 rows carry no DB figure"
companion_vaults: "../Open-Redirect · ../Cache-Poisoning · ../Authentication-Session · ../SSRF"
case_id_scheme: "HOST-<HackerOne report id>"
quote_rule: "byte-true, (sic)-marked, from read bodies only; missing figures recorded never invented"
---

# Vault/24 — Host Header Injection playbook set

Four rows, and the class's shape is already visible: the money follows *who consumes the host
value* — password-reset mails and verification links pay ($300 at Omise), a cache-poisoning
redirect demo and a newsletter-mail redirect row ride at no figure, and a subdomain-bypass row
pays $500 because "internal" hosts turn out to share one IP. The host header is a trust
decision, not a string.

## Start here

| # | File | What it gives you |
|---|---|---|
| 1 | [`HOST-Testing-Agent-Playbook.md`](HOST-Testing-Agent-Playbook.md) | **The executable protocol.** P0 program/policy read → P1 sink inventory (who consumes Host / X-Forwarded-Host / Referer) → P2 probe protocol (alternate-host → redirect → cache → mail) → P3 proof ladder → P4 hardening fingerprints → P5 kill-gates. |
| 2 | [`00_host-header-injection.md`](00_host-header-injection.md) | All 4 rows: mailing redirect (Starbucks), redirect + content-spoof (Omise $300), one-IP subdomain bypass (UrbanCompany $500), cache-poisoning redirect (Instacart). |

## References (provenance layer)

| File | Contents |
|---|---|
| [`references/source-index.md`](references/source-index.md) | Corpus provenance (h1-brain DB `disclosed_reports`, sha256 `8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4`, 3,673 rows), classification funnel (`classified.json` bucket `host-header` → 4, `module_map_all.json` `host-header-injection` → 4, `_adjacent` → 0), DB reconciliation, bounty accounting, era discipline, 7 limitations. |
| [`references/case-register.md`](references/case-register.md) | Row-per-row ledger of all 4 bucket rows: case ID, team, bounty, module, evidence level, DB weakness. |
| [`references/archive/host-bodies-full-dump.txt`](references/archive/host-bodies-full-dump.txt) | All 4 bodies verbatim — the anchor for every quote. |
| [`references/archive/classes.json`](references/archive/classes.json) | Frozen module assignment for all 4 rows. |

## Scoreboard (4 rows · 2 with bounty figures · $800 · max $500)

| Case | Title (short) | Program | Bounty | CVE |
|---|---|---|---|---|
| [HOST-158019](https://hackerone.com/reports/158019) | Host Header Injection/Redirection (Instacart) | instacart | — | — |
| [HOST-229498](https://hackerone.com/reports/229498) | Host header injection via newsletter signup | starbucks | — | — |
| [HOST-1444675](https://hackerone.com/reports/1444675) | Host Header Injection → Open Redirect + Content Spoofing | omise | **$300** | — |
| [HOST-1783015](https://hackerone.com/reports/1783015) | Host header bypass → multiple subdomains | urbancompany | **$500** (max) | — |

Corpus program mix: instacart, starbucks, omise, urbancompany — one row each. All four bodies
are full-body; no row is metadata-only.

## Vault map

| File | Content |
|---|---|
| `HOST-Testing-Agent-Playbook.md` | Agent-facing operational playbook: P0–P5 phases, module↔phase table, non-goals. |
| `00_host-header-injection.md` | Single module covering all 4 rows with case-stock table, byte-true quotes, what-pays/what-doesn't, cross-references. |
| `references/source-index.md` | Provenance, funnel, DB reconciliation, bounty accounting, era discipline, limitations. |
| `references/case-register.md` | 4-row ledger with DB metadata, evidence level, weakness labels. |
| `references/archive/host-bodies-full-dump.txt` | All 4 bodies verbatim (anchor for every quote). |
| `references/archive/classes.json` | Frozen module assignment for all 4 rows. |

## Cross-vault links

- `Open-Redirect/` — every row's terminal effect is an open redirect; that vault owns the
  redirect-destination doctrine, this vault owns the host-consumption primitive.
- `Cache-Poisoning/` — HOST-158019 names cache poisoning as the delivery; the cache vault
  owns the poisoning mechanics, this vault owns the host-reflection evidence.
- `Authentication-Session/` — password-reset / email-verification mail hardening lives there;
  HOST-1444675's verification-link row is its host-poisoning instance.
- `SSRF/` — HOST-1783015's DB weakness is SSRF (subdomain bypass via Host); the SSRF vault
  owns the internal-network play, this vault owns the Host-manipulation primitive.

## Coverage vs limitations

**Covered**: the complete `host-header` classified bucket (4 rows) with per-row sink,
consumer, and bounty; the `host-header-injection` module assignment (`module_map_all.json`);
DB reconciliation for every row.

**Honest limitations**:
1. **Four-row corpus.** One row each for mail-redirect, verification-mail, and subdomain-bypass
   patterns. Pattern-level pricing (e.g. "mail rows pay") rests on 2–3 points and is labeled
   as such — do not generalize into a tariff.
2. **Half the corpus carries no figure.** 2 of 4 rows are bunchmarked `None` in the DB
   (158019, 229498). $800 is a corpus floor; blank is not $0.
3. **Weakness labels are triage artifacts.** 158019 is labeled `Open Redirect`, 1783015
   `Server-Side Request Forgery (SSRF)`, the other two `None`. Bodies are the class
   authority; modules classify by body behavior.
4. **Screenshot-dependent PoCs.** HOST-229498 and HOST-1783015 rely on attached images/videos
   (`{F…}` markers) — the text quotes in this vault are the byte-true residue, not the full
   proof. No screenshot content is reconstructed.
5. **Era honesty.** Rows span 2016–2017 disclosures (Instacart 2016, Starbucks 2017).
   Modern allow-list / `X-Forwarded-Host` stripping hardening is fingerprinted in playbook
   P4 and labeled as outside the corpus.
6. **No password-reset row at a paid tier.** The class's most famous sink (reset-mail
   poisoning) appears only as a claim inside HOST-158019's generic paragraph. The vault
   does not price reset-mail poisoning from it.
7. **No live testing was performed.** Validate host-consumption probes against in-scope test
   mailboxes/accounts you control — never against production mail flows.


<!-- CASESTOCK-LINK:BEGIN -->

## Case stock — vault (`_VAULT/`)

**39 disclosed reports** routed to this category · 8 with a bounty figure · **$1,580** · 28 full write-ups stored locally.

- Full list: [`_VAULT/by-vault-category/24_Host-Header-Injection.md`](../_VAULT/by-vault-category/24_Host-Header-Injection.md)
- Query: `sqlite3 ../_VAULT/reports.sqlite "SELECT id,bounty,title FROM reports WHERE ..."`
- Pull one write-up: `python3 ../_VAULT/scripts/extract_report.py <id>`

| Top paid | Program | Bounty |
|---|---|---|
| [1783015](https://hackerone.com/reports/1783015) Host header injection that bypassed protection and allowed accessing multiple su | Urban Company | $500 |
| [1444675](https://hackerone.com/reports/1444675) Host Header Injection leads to Open Redirect and Content Spoofing or Text Inject | Omise | $300 |
| [182670](https://hackerone.com/reports/182670) Email link poisoning / Host header attack | Boozt Fashion AB | $200 |
| [1392935](https://hackerone.com/reports/1392935) XSS via X-Forwarded-Host header | Omise | $200 |
| [548094](https://hackerone.com/reports/548094) Internal Hostname disclosure from multiple Apache servers via blank host header  | Ping Identity | $150 |

_refreshed 2026-11-17 from the public HackerOne disclosed-report dataset_
<!-- CASESTOCK-LINK:END -->
