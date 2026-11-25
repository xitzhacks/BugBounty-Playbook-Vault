---
title: "Subdomain Takeover source index — provenance, funnel, module mechanics, limitations"
type: source-index
built: "2026-11-07"
---

# Source index — Subdomain Takeover build

## 1. Corpus provenance

- **Primary source**: `/home/user/tools/h1-brain/disclosed_reports.db` — the h1-brain pre-built
  SQLite corpus of publicly disclosed HackerOne reports (**3,673 rows**), DB sha256
  `8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4`.
- **Working copies**: `/home/user/opencode-work/h1brain/classified.json` (bucket
  `subdomain-takeover`, 24 rows) and `module_map_all.json` (module assignment + merges).
  In-vault: `references/archive/SDTO-bodies-full-dump.txt` (26 bodies), `classes.json`, `meta.json`.

## 2. Classification funnel

1. **Labeled/keyword net** over 3,673 rows: weakness labels (`Subdomain Takeover`) plus keyword
   arms (`subdomain takeover`, `dangling`, `unclaimed`, `CNAME`, `NXDOMAIN`) → 24 rows.
2. **Body read**: all 24 read before assignment; 2 additional rows from the unclassified pool
   (cloudflare r2.dev custom-domain takeover; vine EC2 reassignment) were merged in via the
   unclassified classifier and are recorded separately as module 04.
3. **Module split** (frozen in `classes.json`):
   - 01 `cloud-cdn-paas-cname` 7 — S3/CloudFront/Heroku.
   - 02 `saas-hosted-service-claim` 14 — Statuspage/HubSpot/Ghost/Azure/Uberflip/Fastly/etc.
   - 03 `dns-delegation-github-tld` 3 — NS delegation, GitHub Pages, unregistered TLD.
   - 04 `_adjacent_unclassified` 2 — merges outside the bucket.

## 3. Bounty accounting

- **Rule**: DB `bounty_amount`; `-` when the DB has no figure. Blank ≠ unpaid.
- **10/26 rows** carry figures, totaling **$4,565**; max $1,125 (SDTO-1700276).
  Module totals: 01 $2,150/4 · 02 $900/3 · 03 $250/1 · 04 $1,265/2.

## 4. Era discipline

- Rows span 2015–2023. Provider hardening (S3 global namespace, CloudFront origin validation,
  SaaS ownership TXT records) changed the success rate materially; the fingerprints remain
  useful, the "free claim" assumption does not.
- Several rows are tagged `Misconfiguration` or `Privilege Escalation` on HackerOne; modules
  classify by the body's mechanism ("bodies win").

## 5. Limitations

1. **24-row bucket** is a disclosed-only slice; master-list row 13 points at an external DNS
   corpus (12 + DNS class) for volume.
2. **Low payout band**: plain takeover paid $100–$1,000 in this corpus; the $1,125 top row is a
   merge from outside the bucket.
3. **No live re-verification** — provider behavior today may differ (see §4).
4. **Chain evidence is thin**: only a handful of rows reach cookies/auth/OAuth; most stop at
   proof-of-control.
5. **Quote discipline**: every blockquote is byte-true to
   `references/archive/SDTO-bodies-full-dump.txt`; `(sic)` marks author typos.
