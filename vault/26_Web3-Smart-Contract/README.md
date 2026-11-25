---
title: "Vault/26 — Web3 / Smart Contract playbook set"
type: index
category: web3
built: "2026-11-07"
evidence: "2 classified rows → 2 retrievable bodies read (2 full-body / 0 metadata-only) · 0 adjacent rows"
bounty: "$1,000 across 1 row with a DB figure (WEB3-1651429) · 1 row carries no DB figure"
companion_vaults: "../XSS · ../Mobile · ../Authentication-Session"
case_id_scheme: "WEB3-<HackerOne report id>"
quote_rule: "byte-true, (sic)-marked, from read bodies only; missing figures recorded never invented"
---

# Vault/26 — Web3 / Smart Contract playbook set

Two rows, one program (MetaMask), and the vault's shape is already a lesson: the paid row
prices a *wallet prompt that lies by omission* ($1,000), while the unpaid row prices a
*browser that drops the last line of defense* (no figure). Both are "smart-contract"
adjacent — but the corpus's actual primitive in each case is wallet/browser parsing, not
the contract itself. This vault records the bucket exactly and refuses to inflate either
row into contract doctrine it does not demonstrate.

## Start here

| # | File | What it gives you |
|---|---|---|
| 1 | [`WEB3-Testing-Agent-Playbook.md`](WEB3-Testing-Agent-Playbook.md) | **The executable protocol.** P0 program/policy read → P1 parse/browser-logic surface inventory → P2 probe protocol (calldata fuzz → CSP parity matrix) → P3 proof ladder → P4 hardening fingerprints → P5 kill-gates. |
| 2 | [`00_web3-core.md`](00_web3-core.md) | Both rows: pre-0.5.0 calldata truncation → blind transfer/approve ($1,000); Android in-wallet browser ignoring CSP headers (`None`). |

## References (provenance layer)

| File | Contents |
|---|---|
| [`references/source-index.md`](references/source-index.md) | Corpus provenance (h1-brain DB `disclosed_reports`, sha256 `8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4`, 3,673 rows), classification funnel (`classified.json` bucket `web3` → 2, `module_map_all.json` `web3-core` → 2, `_adjacent` → 0), DB reconciliation, bounty accounting, era discipline, 7 limitations. |
| [`references/case-register.md`](references/case-register.md) | Row-per-row ledger of both bucket rows: case ID, team, bounty, module, evidence level, DB weakness. |
| [`references/archive/web3-bodies-full-dump.txt`](references/archive/web3-bodies-full-dump.txt) | Both bodies verbatim — the anchor for every quote. |
| [`references/archive/classes.json`](references/archive/classes.json) | Frozen module assignment for both rows. |

## Scoreboard (2 rows · 1 with a bounty figure · $1,000 · max $1,000)

| Case | Title (short) | Program | Bounty | CVE |
|---|---|---|---|---|
| [WEB3-1651429](https://hackerone.com/reports/1651429) | Bypass parsing of transaction data (ERC20 blind transfer) | metamask | **$1,000** (max) | — |
| [WEB3-1941767](https://hackerone.com/reports/1941767) | MetaMask Browser (Android) ignores CSP header | metamask | — | — |

Corpus program mix: metamask 2. Both bodies are full-body; no row is metadata-only.

## Vault map

| File | Content |
|---|---|
| `WEB3-Testing-Agent-Playbook.md` | Agent-facing operational playbook: P0–P5 phases, module↔phase table, non-goals. |
| `00_web3-core.md` | Single module covering both rows with case-stock table, byte-true quotes, what-pays/what-doesn't, cross-references. |
| `references/source-index.md` | Provenance, funnel, DB reconciliation, bounty accounting, era discipline, limitations. |
| `references/case-register.md` | 2-row ledger with DB metadata, evidence level, weakness labels. |
| `references/archive/web3-bodies-full-dump.txt` | Both bodies verbatim (anchor for every quote). |
| `references/archive/classes.json` | Frozen module assignment for both rows. |

## Cross-vault links

- `XSS/` — WEB3-1941767's DB weakness is `XSS - Reflected` and its payload is an XSS
  enabler; that vault owns the XSS payoff doctrine.
- `Mobile/` — WEB3-1941767 is an Android in-wallet browser; the Mobile vault owns the
  Android WebView evidence, this vault owns the CSP-parity row.
- `Authentication-Session/` — no corpus row reaches wallet-consent auth hardening, but
  WEB3-1651429's blind approve is a consent-prompt failure; cite the auth vault for the
  hardening posture.

## Coverage vs limitations

**Covered**: the complete `web3` classified bucket (2 rows) with per-row parse/browser
sink and bounty; the `web3-core` module assignment (`module_map_all.json`); DB
reconciliation for every row.

**Honest limitations**:
1. **Two-row, one-program corpus.** Both rows are MetaMask. No contract-level (Solidity)
   proof exists in this bucket — WEB3-1651429's contract is a test-dApp ERC20 deploy
   (solc 0.4.26) used to expose a wallet parser gap. Do not cite this vault for smart-
   contract exploitation doctrine.
2. **Half the corpus carries no figure.** WEB3-1941767 is `None` in the DB. $1,000 is a
   corpus floor; blank is not $0.
3. **Weakness labels are triage artifacts.** `Improper Input Validation` and
   `XSS - Reflected` label the two rows; both bodies are wallet/browser parsing behavior.
   Bodies win.
4. **Test-network PoC.** WEB3-1651429's reproduction runs on Rinkeby with a self-deployed
   token. The vault records the parser-gap evidence as filed; it does not claim mainnet
   reproduction.
5. **Self-assessed severity, undecided.** WEB3-1941767's researcher doubts the CSP gap is a
   vulnerability ("you could argue this is a defence-in-depth measure") and asks the
   program to decide. The vault keeps the row at its filed weight (`None`), not as a
   priced finding.
6. **Era honesty.** Rows span the solc-0.4.26 / Rinkeby era through MetaMask Android
   v6.1.1. Modern strict-length checking and WebView CSP parity are fingerprinted in
   playbook P4 and labeled outside the corpus.
7. **No live testing was performed.** Validate parser/CSP probes against test networks and
   wallets you control — never against production wallet sessions or mainnet funds.


<!-- CASESTOCK-LINK:BEGIN -->

## Case stock — vault (`_VAULT/`)

**3 disclosed reports** routed to this category · 0 with a bounty figure · **$0** · 3 full write-ups stored locally.

- Full list: [`_VAULT/by-vault-category/26_Web3-Smart-Contract.md`](../_VAULT/by-vault-category/26_Web3-Smart-Contract.md)
- Query: `sqlite3 ../_VAULT/reports.sqlite "SELECT id,bounty,title FROM reports WHERE ..."`
- Pull one write-up: `python3 ../_VAULT/scripts/extract_report.py <id>`

_refreshed 2026-11-17 from the public HackerOne disclosed-report dataset_
<!-- CASESTOCK-LINK:END -->
