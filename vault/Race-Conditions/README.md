# Race Conditions / TOCTOU — Vault

**Case-ID scheme:** `RACE-<h1-id>` where `<h1-id>` is the row `id` in the h1-brain corpus DB (`/home/user/tools/h1-brain/disclosed_reports.db`, table `disclosed_reports`).

## Provenance (what this vault is built from)

- Source: h1-brain pre-built DB of publicly disclosed, bounty-awarded HackerOne reports — **3,673 rows**, full `vulnerability_information` bodies.
- DB fetched from the repo's Git-LFS pointer; sha256 verified `8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4`.
- Race bucket = 26 rows selected by (a) CWE-style weakness labels (`Time-of-check Time-of-use (TOCTOU) Race Condition`, `Concurrent Execution using Shared Resource with Improper Synchronization ('Race Condition')`) and (b) keyword net over titles/bodies (`race conditio…`/`toctou`/`double-spend`/`timing attack`). Classifier v1; all 26 bodies read end-to-end before module assignment.
- Evidence levels, honestly labeled:
  - **Full body** — 23/26 cases read end-to-end and quoted from body text.
  - **Metadata-only** — 3/26 GitHub-Security-Lab rows whose body is just *"This bug was reported directly to GitHub Security Lab."* (RACE-1301753, RACE-1496268, RACE-1943049); title + bounty only.

## Scoreboard (26 rows · 10 paid · $43,260 · max $15,250)

| Case | Title (short) | Program | Bounty | CVE |
|---|---|---|---|---|
| RACE-300305 | Email-confirm race → partner/employee ATO | shopify | **$15,250** (max) | — |
| RACE-822262 | Nupkg traversal + Gitaly race → arbitrary file read | gitlab | **$12,000** | CVE-2020-12448 |
| RACE-1438052 | Faucet race → over "coins_max" credit limit | cosmos | **$5,000** | — |
| RACE-1301753 | Java timing attack in crypto-result comparison | github-security-lab | **$4,500** | — |
| RACE-2078571 | curl `stat`→`fopen` race: cookie jar theft / file overwrite | ibb | **$2,480** | CVE-2023-32001 |
| RACE-1943049 | Python timing attack | github-security-lab | **$1,800** | — |
| RACE-1496268 | Java timing attack in header comparison | github-security-lab | **$1,000** | — |
| RACE-1540969 | CTF group join ×N | security | $500 | — |
| RACE-1990421 | libcurl `siglongjmp` unfenced global buffer → crash | ibb | $480 | CVE-2023-28320 |
| RACE-1566017 | Fake-follower inflation via like-endpoint race | judgeme | $250 | — |
| RACE-55140 | OAuth2 code/refresh_token exchange race → revocation bypass | ibb | None | — |
| RACE-772886 | Two reset endpoints keep both tokens valid | nordsecurity | None | — |
| RACE-801743 | Reddit `verify_purchase` race → 35× coin inflation | reddit | None | — |
| RACE-429026 | Retest confirm race → duplicated $500 payment | security | None | — |
| RACE-604534 | Double group join → undeletable member | security | None | — |
| RACE-541169 | `GitLab::UrlBlocker` DNS TOCTOU → full SSRF | gitlab | None | — |
| RACE-859962 | K8s apiserver proxy filter double-DNS TOCTOU | kubernetes | None | CVE-2020-8562 |
| RACE-768110 | NordVPN Windows config-swap TOCTOU → SYSTEM LPE | nordsecurity | None | — |
| RACE-2905013 | Tomcat write-servlet case-insensitivity race → RCE | ibb | None | CVE-2024-50379 |
| RACE-2106708 | HEAD-check / GET-use TOCTOU → RXSS filter bypass | security | None | — |
| RACE-488985 | GraphQL `claimCredential` race → multiple credential sets | security | None | — |
| RACE-1717650 | Stripe promo-code redemption-limit race (tab racing) | stripe | None | — |
| RACE-1037430 | "Free premium days" promo accept race ×3 | bumble | None | — |
| RACE-1460373 | Invite-endpoint race + cancel-refund loop → unlimited invites | fetlife | None | — |
| RACE-454949 | CTF flag re-submission ×70 for points | security | None | — |
| RACE-239359 | WooCommerce/Simplify md5 non-constant-time compare | automattic | None | — |

Corpus program mix: security 6 · ibb 4 · github-security-lab 3 · gitlab 2 · nordsecurity 2 · shopify, reddit, kubernetes, bumble, cosmos, fetlife, stripe, judgeme, automattic 1 each.

## Vault map

| File | Content |
|---|---|
| `RACE-Testing-Agent-Playbook.md` | Agent-facing operational playbook: entry-point mapping, tool ladder, root-cause evidence, validation gates, chains, report template |
| `Synchronization-and-Tooling.md` | Every sync technique evidenced in the corpus: curl `&` chains, tab racing, Burp parallel, Turbo Intruder gate script, `renameat2 RENAME_EXCHANGE`, NTFS oplocks, zero-TTL DNS |
| `Financial-Credit-and-Ledger-Races.md` | Mint-more-than-you-paid: Reddit coins, Badoo premium days, Stripe redemption limit, faucet over-limit, doubled retest payment, CTF points, fake followers |
| `Membership-and-Invitation-Races.md` | State-corruption: double group join / undeletable member, credential claim race, invitation farm + cancel-refund loop |
| `Account-ATO-and-Token-Races.md` | ATO chains: Shopify email-confirmation race ($15,250), OAuth2 token-pair explosion, NordVPN dual reset endpoints |
| `Check-Use-and-File-System-Races.md` | TOCTOU on validation: GitLab UrlBlocker SSRF, K8s proxy filter, HEAD/GET XSS-gate bypass, NordVPN LPE, curl fopen, Tomcat case RCE, nupkg traversal + Gitaly chain |
| `Library-Timing-Adjacent.md` | Native races + side-channel money: libcurl `siglongjmp`, GHSL Java/Python timing attacks ($7,300 of the corpus), WooCommerce md5 oracle |
| `references/source-index.md` | Provenance, funnel, classification mechanics, 5 limits |
| `references/case-register.md` | 26-row ledger with DB metadata, evidence level, CVEs |
| `references/archive/race-bodies-full-dump.txt` | All 26 bodies verbatim (anchor for every quote) |
| `references/archive/classes.json` | Frozen module assignment for all 26 rows |

## Cross-vault links

- `SSRF/` — RACE-541169 (GitLab UrlBlocker) and RACE-859962 (K8s proxy filter) are DNS-TOCTOU *SSRF* reports; the SSRF vault's internal-network play is the destination, this vault supplies the sync primitive.
- `Authentication-Session/` — RACE-772886 reset-token races and RACE-55140 OAuth token explosion belong to its token-invalidation module; cross-cite.
- `XSS/` — RACE-2106708 re-opens a fixed RXSS via a HEAD/GET TOCTOU gate; XSS-vault bypass modules should reference this as "guard bypass via double-request".
- `RCE/` — RACE-2905013 (Tomcat CVE-2024-50379) is an RCE delivered by a file-write race; RACE-768110 is SYSTEM LPE via config swap.
- `Business-Logic/` (upcoming master row 12) — the credit/ledger module is the race-condition slice of the same attack class; the Stripe/Fetlife cases are shared canon.
- `File-Upload/` — RACE-822262 packages a path traversal (their class) with a repository race (ours) into a $12,000 file read.

## Limitations

1. **Count basis differs from the master list.** Master row 11 cites "18 + 19" H1-disclosed counts from other sources; this vault quotes only the h1-brain DB subset (26 rows). A v2 sweep of the ~468-row unclassified pool may add cases.
2. **Weakness labels are historical triage artifacts** — the same class appears as `TOCTOU`, CWE-362 "Concurrent Execution", `SSRF`, `Code Injection`, `XSS - Reflected`, `Improper Authentication`, `Improper Access Control`, or unlabelled depending on triager. Bodies are the class authority.
3. **Bounty `None` ≠ unpaid.** It means the DB row has no figure. 16 of 26 rows carry no figure; $43,260 is a corpus-floor, not a total.
4. **3 GHSL rows are metadata-only** (RACE-1301753/1496268/1943049) — one-line bodies carrying $7,300 of real timing-attack payouts but no quotable technique.
5. **Chainpay vs racepay**: RACE-822262 ($12,000) and RACE-300305 ($15,250) pay because the race feeds another bug. Race-only reports top out at $5,000 (faucet).
6. **Era honesty** — tool choices are historical evidence (2016–2024 disclosures), not current best tooling.
7. **QA**: all block quotes in modules were byte-verified against `references/archive/race-bodies-full-dump.txt`; `(sic)` marks author typos.


<!-- CASESTOCK-LINK:BEGIN -->

## Case stock — vault (`_VAULT/`)

**95 disclosed reports** routed to this category · 18 with a bounty figure · **$37,946** · 60 full write-ups stored locally.

- Full list: [`_VAULT/by-vault-category/Race-Conditions.md`](../_VAULT/by-vault-category/Race-Conditions.md)
- Query: `sqlite3 ../_VAULT/reports.sqlite "SELECT id,bounty,title FROM reports WHERE ..."`
- Pull one write-up: `python3 ../_VAULT/scripts/extract_report.py <id>`

| Top paid | Program | Bounty |
|---|---|---|
| [300305](https://hackerone.com/reports/300305) Ability to bypass partner email confirmation to take over any store given an emp | Shopify | $15,250 |
| [1438052](https://hackerone.com/reports/1438052) Race condition in faucet when using starport | Cosmos | $5,000 |
| [1520931](https://hackerone.com/reports/1520931) Time-of-check to time-of-use vulnerability in the std::fs::remove_dir_all() func | Internet Bug Bounty | $4,000 |
| [2110030](https://hackerone.com/reports/2110030) Race Condition Enables Bypassing Verification Check | Tools for Humanity | $3,000 |
| [2078571](https://hackerone.com/reports/2078571) [curl] CVE-2023-32001: fopen race condition | Internet Bug Bounty | $2,480 |

_refreshed 2026-11-17 from the public HackerOne disclosed-report dataset_
<!-- CASESTOCK-LINK:END -->
