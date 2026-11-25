---
title: "Subdomain Takeover — dangling DNS, claimable SaaS hosts, and the chains that make it pay"
type: index
category: "Subdomain Takeover (cloud/CDN/PaaS CNAME · SaaS-hosted service claim · DNS delegation & GitHub/TLD)"
built: "2026-11-07"
evidence: "26 rows from h1-brain disclosed_reports.db (3,673 rows; sha256 8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4) — 24 classified bucket + 2 documented unclassified merges · all full-body"
bounty: "$4,565 across 10 rows · module split: 01 $2,150/4 · 02 $900/3 · 03 $250/1 · 04 $1,265/2"
companion_vaults: "../17_Privilege-Escalation · ../18_Misconfiguration · ../XSS · ../Open-Redirect"
case_id_scheme: "SDTO-<HackerOne report id>"
quote_rule: "byte-true to references/archive/SDTO-bodies-full-dump.txt"
---

# Vault/Subdomain-Takeover — the DNS record outlived the service

Twenty-six disclosed cases, one mechanic: a DNS entry points at a provider where the resource
is gone, and anyone can claim it. The corpus prices plain takeover low ($100–$1,000) and pays
for the *chain* — a takeover that yields cookies, auth bypass, or OAuth redirects.

## Start here

| # | File | What it gives you |
|---|---|---|
| 1 | [`SDTO-Testing-Agent-Playbook.md`](SDTO-Testing-Agent-Playbook.md) | Executable protocol: enumeration → fingerprint → claim → proof gates |
| 2 | [`01_Cloud-CDN-PaaS-CNAME.md`](01_Cloud-CDN-PaaS-CNAME.md) | S3 / CloudFront / Heroku unclaimed origins — 7 rows, $2,150 |
| 3 | [`02_SaaS-Hosted-Service-Claim.md`](02_SaaS-Hosted-Service-Claim.md) | Statuspage, HubSpot, Ghost, Azure, Uberflip, Fastly — 14 rows, $900 |
| 4 | [`03_DNS-Delegation-GitHub-TLD.md`](03_DNS-Delegation-GitHub-TLD.md) | NS delegation, GitHub Pages, unregistered TLD — 3 rows, $250 |
| 5 | [`04_Adjacent-Unclassified.md`](04_Adjacent-Unclassified.md) | The two merge rows outside the bucket (cloudflare r2.dev $1,125, vine EC2 $140) |

## References (provenance layer)

| File | Contents |
|---|---|
| [`references/source-index.md`](references/source-index.md) | DB provenance, funnel, module mechanics, era discipline, limitations |
| [`references/case-register.md`](references/case-register.md) | 26-row ledger with DB metadata |
| [`references/archive/SDTO-bodies-full-dump.txt`](references/archive/SDTO-bodies-full-dump.txt) | All 26 bodies verbatim (quote anchor) |
| [`references/archive/classes.json`](references/archive/classes.json) | Frozen id → module map |

## Cross-vault links

- `../17_Privilege-Escalation/` — PRIV's subdomain module overlaps this bucket (24 rows shared
  by keyword); the cash cases there are access-control, not DNS.
- `../18_Misconfiguration/` — the same dangling-state rows surfaced under misconfig.
- `../XSS/` — a claimed host can serve scripts on the victim origin.
- `../Open-Redirect/` — OAuth `redirect_uri` validation often trusts the subdomain.

## Limitations

1. **Small bucket (24 + 2)** — master-list row 13 cites an externally-controlled DNS class, not
   this DB slice.
2. **Bounty `-` ≠ unpaid.** 16 of 26 rows carry no figure.
3. **Provider behavior drifts**: S3 bucket names are now globally reserved on takeover attempts,
   CloudFront requires a matching origin, and many SaaS vendors added claim verification — the
   primitives remain, the ease does not. This vault records what was true when reported.
4. **Plain takeover is often triaged Low/Medium**; the paid ceiling in this corpus comes from
   chains (cookie scope, auth bypass), which most rows do not complete.
5. **Never claim production infrastructure you do not own** — the corpus's own proofs stop at a
   benign proof-of-control page.
6. **Weakness labels are triage artifacts** (several rows are tagged Misconfiguration or
   Privilege Escalation); modules classify by the body.
7. **Quotes** are byte-verified against the archived bodies; `(sic)` marks author typos.


<!-- CASESTOCK-LINK:BEGIN -->

## Case stock — vault (`_VAULT/`)

**209 disclosed reports** routed to this category · 31 with a bounty figure · **$15,040** · 122 full write-ups stored locally.

- Full list: [`_VAULT/by-vault-category/13_Subdomain-Takeover.md`](../_VAULT/by-vault-category/13_Subdomain-Takeover.md)
- Query: `sqlite3 ../_VAULT/reports.sqlite "SELECT id,bounty,title FROM reports WHERE ..."`
- Pull one write-up: `python3 ../_VAULT/scripts/extract_report.py <id>`

| Top paid | Program | Bounty |
|---|---|---|
| [154425](https://hackerone.com/reports/154425) Subdomain takeover on http://fastly.sc-cdn.net/ | Snapchat | $3,000 |
| [104016](https://hackerone.com/reports/104016) Dangling pointer in the unserialization of ArrayObject items | Internet Bug Bounty | $1,000 |
| [352869](https://hackerone.com/reports/352869)  Subdomain Takeover Via Insecure CloudFront Distribution cdn.grab.com | Grab | $1,000 |
| [779442](https://hackerone.com/reports/779442) Subdomain takeover of storybook.lystit.com | Lyst | $1,000 |
| [387760](https://hackerone.com/reports/387760) Subdomain Takeover at test.shipt.com | Shipt | $750 |

_refreshed 2026-11-17 from the public HackerOne disclosed-report dataset_
<!-- CASESTOCK-LINK:END -->
