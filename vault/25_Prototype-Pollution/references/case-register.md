---
title: "Prototype Pollution case register — 4-row ledger (h1-brain corpus)"
type: register
built: "2026-11-07"
roster: "h1-brain disclosed_reports.db (3,673 rows; sha256 8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4)"
case_id_scheme: "PP-<HackerOne report id>"
bounty_rule: "DB bounty_amount where present (labeled $) · None = no figure in DB (not evidence of non-payment)"
module_rule: "frozen in archive/classes.json (bodies-win classification)"
---

# Case register — Prototype Pollution

Corpus: 4 rows · 2 with bounty figures · **$6,000** · max $3,000 (PP-1106238, PP-1280002) · evidence: 4 full-body / 0 metadata-only.

Class census: prototype-pollution 4 (712065, 998398, 1106238, 1280002) — single module.

Bounty arithmetic: $3,000 + $3,000 = **$6,000** (2 rows — same program/sink, sequential disclosures).

| Case | Team | Bounty | Module | Evidence | Note |
|---|---|---|---|---|---|
| [PP-712065](https://hackerone.com/reports/712065) | nodejs-ecosystem | — | prototype-pollution | full | lodash 4.17.15 `merge`/`defaultsDeep` → `Object.prototype`; CVE-2020-8203; "Variable" impact; DB weakness Allocation of Resources… |
| [PP-998398](https://hackerone.com/reports/998398) | elastic | — | prototype-pollution | full | Swiftype `deparam` hash parse → pollution → `eval` hook gadget → DOM XSS; DB weakness XSS - DOM |
| [PP-1106238](https://hackerone.com/reports/1106238) | gitlab | $3,000 | prototype-pollution | full | Mermaid `__proto__` directive → app-wide DoS; paid Step 1 (characterization) |
| [PP-1280002](https://hackerone.com/reports/1280002) | gitlab | $3,000 | prototype-pollution | full | Mermaid `__proto__.template` → stored XSS on search-bar touch; paid Step 2 (weaponization) |

Module totals: prototype-pollution **$6,000 / 2 rows** (1106238 $3,000 + 1280002 $3,000).
