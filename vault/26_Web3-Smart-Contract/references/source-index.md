---
title: "Web3 source index — provenance, funnel, DB reconciliation, limitations"
type: source-index
built: "2026-11-07"
---

# Source index — Web3 build

## 1. Corpus provenance

- **Primary source**: `/home/user/tools/h1-brain/disclosed_reports.db` — the h1-brain pre-built
  SQLite corpus of publicly disclosed, bounty-awarded HackerOne reports (**3,673 rows**,
  table `disclosed_reports` with fields `id, title, vulnerability_information, weakness_name,
  program_handle, asset_identifier, asset_type, cve_ids, bounty_amount`). The DB was fetched
  from the repo's Git-LFS pointer and sha256-verified:
  `8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4`. No live HackerOne fetch
  this build.
- **Classifier outputs**: `/home/user/opencode-work/h1brain/classified.json` (bucket
  `web3` = 2 rows) and `/home/user/opencode-work/h1brain/module_map_all.json`
  (`web3.web3-core` = 2 ids, `_adjacent` = 0). Bodies re-read from the DB for the archive
  dump; classified `id/title/body/program/bounty` match the DB for both rows.
- **In-vault archive**: `references/archive/web3-bodies-full-dump.txt` (2/2 bodies),
  `references/archive/classes.json` (frozen module assignment).

## 2. Classification funnel

1. **Keyword net** over all 3,673 rows: `classified.json` bucket `web3` selected **2 rows**
   via `web3` / `ERC20` / `MetaMask` arms (`src` = `None/keyword:web3`). DB weakness labels:
   `Improper Input Validation` (1651429), `Cross-site Scripting (XSS) - Reflected` (1941767).
   Bodies are the class authority: both are wallet/browser parsing behavior, not
   contract behavior.
2. **Module split** (frozen in `classes.json`): single module `web3-core` holds both ids
   (1651429, 1941767). `_adjacent` = 0 — no adjacent rows.
3. **Per-body read**: both bodies read end-to-end. Evidence: 2 full-body / 0 metadata-only.
4. **DB reconciliation**: every bucket row verified present in `disclosed_reports` with
   identical title and bounty. Programs match the classifier (metamask ×2).

## 3. Bounty accounting

- **Rule**: DB `bounty_amount` where present; `None` recorded as no figure (not $0). Blank ≠
  unpaid — HackerOne does not always publish figures.
- Corpus: 1/2 rows carry figures, totaling **$1,000** (WEB3-1651429). See case-register.md
  for per-row labels and the arithmetic.
- **What the money prices**: a test-network wallet-prompt parser demonstration. No row
  prices mainnet loss, contract exploitation, or the CSP gap.

## 4. Limits & era honesty

1. **Two-row, one-program corpus** — MetaMask only; no contract-level proof in the bucket.
2. **Half the corpus at `None`** — $1,000 is a corpus floor; blank is not $0.
3. **DB weakness ≠ taxonomy** — Input Validation / XSS labels; bodies decide the class.
4. **Test-network PoC** — Rinkeby + self-deployed token; no mainnet reproduction claimed.
5. **Self-assessed severity, undecided** — WEB3-1941767 filed with explicit doubt;
   kept at filed weight (`None`).
6. **Era**: solc-0.4.26/Rinkeby through MetaMask Android v6.1.1; P4 is outside-corpus.
7. **No live testing** — test networks/wallets only; no production sessions, no mainnet funds.
