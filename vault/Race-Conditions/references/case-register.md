---
title: "Race case register — 26-row ledger (h1-brain corpus)"
type: register
built: "2026-11-07"
roster: "h1-brain disclosed_reports.db (3,673 rows; sha256 8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4)"
case_id_scheme: "RACE-<HackerOne report id>"
bounty_rule: "DB bounty_amount where present (labeled $) · None = no figure in DB (not evidence of non-payment)"
module_rule: "frozen in archive/classes.json (bodies-win classification)"
---

# Case register — Race Conditions / TOCTOU

Corpus: 26 rows · 10 with bounty figures · **$43,260** · max $15,250 (RACE-300305) · evidence: 23 full-body / 3 metadata-only.

Class census: Financial-Credit-and-Ledger-Races 6 (801743, 429026, 1037430, 1717650, 1438052, 454949, 1566017) · Membership-and-Invitation-Races 4 (604534, 1540969, 488985, 1460373) · Account-ATO-and-Token-Races 3 (55140, 300305, 772886) · Check-Use-and-File-System-Races 7 (541169, 859962, 2106708, 768110, 2078571, 2905013, 822262) · Library-Timing-Adjacent 5 (1990421, 1301753, 1496268, 1943049, 239359) · Synchronization-and-Tooling spans all.

| Case | Team | Bounty | Module | Evidence | Note |
|---|---|---|---|---|---|
| [RACE-55140](https://hackerone.com/reports/55140) | ibb | - | Account-ATO | full | OAuth2 code/refresh exchange race; 11 providers tested, 6 vulnerable; exponential token mint |
| [RACE-239359](https://hackerone.com/reports/239359) | automattic | - | Library-Timing | full | WooCommerce Simplify md5 `===` oracle; hash_equals fix proposed |
| [RACE-300305](https://hackerone.com/reports/300305) | shopify | $15,250 | Account-ATO | full | Email-confirm race → partner/employee ATO; corpus max |
| [RACE-429026](https://hackerone.com/reports/429026) | security | - | Financial | full | Retest-confirm race; 5 curls; $500 double payment seen 2 weeks later |
| [RACE-454949](https://hackerone.com/reports/454949) | security | - | Financial | full | Same flag ×70 → 2 invitations; Race The Web tooling |
| [RACE-488985](https://hackerone.com/reports/488985) | security | - | Membership | full | GraphQL `claimCredential` race; 22 Intruder replays → multiple live test credentials |
| [RACE-541169](https://hackerone.com/reports/541169) | gitlab | - | Check-Use | full | UrlBlocker double-DNS TOCTOU → full SSRF incl. metadata |
| [RACE-604534](https://hackerone.com/reports/604534) | security | - | Membership | full | Double group join → undeletable member; self-rated Low |
| [RACE-768110](https://hackerone.com/reports/768110) | nordsecurity | - | Check-Use | full | NordVPN config-swap TOCTOU → SYSTEM LPE; NTFS oplocks |
| [RACE-772886](https://hackerone.com/reports/772886) | nordsecurity | - | Account-ATO | full | Dual reset endpoints, independent token stores; sequential window |
| [RACE-801743](https://hackerone.com/reports/801743) | reddit | - | Financial | full | `verify_purchase` race; 10 parallel → 9 minted; 35× projection |
| [RACE-822262](https://hackerone.com/reports/822262) | gitlab | $12,000 | Check-Use | full | Nupkg traversal + Gitaly race → arbitrary file read; CVE-2020-12448 |
| [RACE-859962](https://hackerone.com/reports/859962) | kubernetes | - | Check-Use | full | Apiserver proxy filter double-DNS TOCTOU; CVE-2020-8562 |
| [RACE-1037430](https://hackerone.com/reports/1037430) | bumble | - | Financial | full | Promo-accept race ×3; 3 days → 9 days premium |
| [RACE-1301753](https://hackerone.com/reports/1301753) | github-security-lab | $4,500 | Library-Timing | metadata | Java crypto-compare timing attack; one-line body |
| [RACE-1438052](https://hackerone.com/reports/1438052) | cosmos | $5,000 | Financial | full | Faucet cap race; 50 concurrent → 30 vs 11 cap; Go map root cause |
| [RACE-1460373](https://hackerone.com/reports/1460373) | fetlife | - | Membership | full | Invite race + cancel-refund loop; 10 curls, 1 debit |
| [RACE-1496268](https://hackerone.com/reports/1496268) | github-security-lab | $1,000 | Library-Timing | metadata | Java header-compare timing attack; one-line body |
| [RACE-1540969](https://hackerone.com/reports/1540969) | security | $500 | Membership | full | CTF group join ×N; Turbo Intruder gate script canon |
| [RACE-1566017](https://hackerone.com/reports/1566017) | judgeme | $250 | Financial | full | Like-endpoint race → fake followers |
| [RACE-1717650](https://hackerone.com/reports/1717650) | stripe | - | Financial | full | Redemption-limit race by tab racing; click-speed window |
| [RACE-1943049](https://hackerone.com/reports/1943049) | github-security-lab | $1,800 | Library-Timing | metadata | Python timing attack; one-line body |
| [RACE-1990421](https://hackerone.com/reports/1990421) | ibb | $480 | Library-Timing | full | libcurl `siglongjmp` unfenced global buffer; CVE-2023-28320 |
| [RACE-2078571](https://hackerone.com/reports/2078571) | ibb | $2,480 | Check-Use | full | curl `stat`→`fopen` race; CVE-2023-32001 |
| [RACE-2106708](https://hackerone.com/reports/2106708) | security | - | Check-Use | full | HEAD/GET TOCTOU → RXSS filter bypass |
| [RACE-2905013](https://hackerone.com/reports/2905013) | ibb | - | Check-Use | full | Tomcat write-servlet race → RCE; CVE-2024-50379 |

Bounty arithmetic: $15,250 + $12,000 + $5,000 + $4,500 + $2,480 + $1,800 + $1,000 + $500 + $480 + $250 = **$43,260** (10 rows).

Module totals: Financial $5,250/2 (1438052 $5,000 + 1566017 $250) · Membership $500/1 (1540969) · Account-ATO $15,250/1 (300305) · Check-Use $14,480/2 (822262 + 2078571) · Library-Timing $7,780/4 (1301753 + 1943049 + 1496268 + 1990421).
