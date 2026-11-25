---
title: "Host Header case register — 4-row ledger (h1-brain corpus)"
type: register
built: "2026-11-07"
roster: "h1-brain disclosed_reports.db (3,673 rows; sha256 8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4)"
case_id_scheme: "HOST-<HackerOne report id>"
bounty_rule: "DB bounty_amount where present (labeled $) · None = no figure in DB (not evidence of non-payment)"
module_rule: "frozen in archive/classes.json (bodies-win classification)"
---

# Case register — Host Header Injection

Corpus: 4 rows · 2 with bounty figures · **$800** · max $500 (HOST-1783015) · evidence: 4 full-body / 0 metadata-only.

Class census: host-header-injection 4 (158019, 229498, 1444675, 1783015) — single module.

Bounty arithmetic: $500 + $300 = **$800** (2 rows).

| Case | Team | Bounty | Module | Evidence | Note |
|---|---|---|---|---|---|
| [HOST-158019](https://hackerone.com/reports/158019) | instacart | — | host-header-injection | full | `Host: google.com` → 301 reflection; cache-poisoning claim without cache proof; DB weakness Open Redirect |
| [HOST-229498](https://hackerone.com/reports/229498) | starbucks | — | host-header-injection | full | Newsletter `Referer` → attacker URL in "Welcome" mail (logo + links); screenshot-dependent PoC |
| [HOST-1444675](https://hackerone.com/reports/1444675) | omise | $300 | host-header-injection | full | `X-Forwarded-Host: bing.com` → verification-link redirect + content spoof; paid bundle |
| [HOST-1783015](https://hackerone.com/reports/1783015) | urbancompany | $500 | host-header-injection | full | Host swap → three shared-IP subdomains (av/ims/mesh); file access unconfirmed; DB weakness SSRF |

Module totals: host-header-injection **$800 / 2 rows** (1783015 $500 + 1444675 $300).
