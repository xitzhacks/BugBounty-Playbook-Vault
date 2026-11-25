---
title: "WEB3 Testing Agent Playbook — the executable protocol"
type: agent-playbook
category: web3
cwe: "CWE-20"
built: "2026-11-07"
corpus: "2 classified rows -> 2 bodies read (2 full-body / 0 metadata-only) · 0 adjacent rows"
bounty: "$1,000 across 1 row with a DB figure (max $1,000 WEB3-1651429) · 1 row no figure"
companion_modules: "00 web3-core (sole module, 2 rows)"
quote_rule: "byte-true, from read bodies only; missing figures recorded never invented"
---

# WEB3 Testing Agent Playbook — Wallet parsing & in-wallet browser parity

*Evidence base: 2 disclosed h1-brain corpus cases (`WEB3-…`). Every quoted sentence in the module is byte-true to `references/archive/web3-bodies-full-dump.txt`. Read the module before improvising; this file is the operational spine. **Boundary**: this bucket contains no Solidity-proof row — do not use this playbook for contract exploitation.*

## P0 — Program classification & policy read (before any payload)

1. Program type: wallet program (extension / mobile) vs contract program. The corpus pays a
   *wallet prompt* gap ($1,000, WEB3-1651429) and leaves a *browser parity* gap unpriced
   (WEB3-1941767). Read policy for test-network and test-wallet rules now: self-deployed
   tokens and test wallets only; never production sessions or mainnet funds.
2. Environment signal: classify the surface — transaction parse/display (calldata decoders,
   transfer/approve prompts) vs in-wallet browsing (WebView, CSP handling). The two corpus
   rows are one of each; inventory both before probing either.
3. Kill-gate: no testing yet — P0 produces the *policy envelope* only.

## P1 — Parse/browser surface inventory

| Surface | Corpus proof | What to map |
|---|---|---|
| Calldata decoders (transfer/approve/…) | WEB3-1651429 (truncated value, no amount shown) | Every method the wallet decodes for display; where strictness forks from execution |
| Compiler-era behavior | WEB3-1651429 (solc < 0.5.0 lenient read) | Which deployed tokens the wallet must still display |
| In-wallet browser (Android WebView) | WEB3-1941767 (header CSP ignored, meta CSP enforced) | WebView version, CSP delivery modes (header vs `<meta>`), script gates |
| Wallet-connect state | WEB3-1941767 (already-"Connected" drain sketch) | Which pages inherit an enabled wallet provider |

## P2 — Probe protocol (parse fuzzer, then parity matrix)

1. **Calldata truncation fuzz** — self-deployed test token (test network), delete/shorten
   calldata bytes (the corpus deletes one value byte); compare *displayed* prompt vs
   *executed* effect. A prompt that omits amount/symbol/recipient on anomalous calldata
   is the paid signal (WEB3-1651429's "normal contract call").
2. **Approve path** — repeat for `approve` (the corpus lists both blind transfer and blind
   approve). Blind approve is the worse consent failure; name which you demonstrated.
3. **CSP parity matrix** — four cells: {header, `<meta>`} × {reference browser, in-wallet
   browser}, `script-src 'none'` with an `alert()` payload (WEB3-1941767's matrix). The
   paid signal — if any — is only the cell that diverges; the corpus's divergent cell
   (header × in-wallet) recorded `None`.
4. **Wallet-active consequence** — only if P2.3 diverges: with a test wallet already
   connected, show the script invoking a wallet action (approve/transfer) on the test
   network. A bare `alert()` screenshot is the kill (WEB3-1941767's `None`).

## P3 — Proof ladder (the modest demonstrations paid)

1. Parser gap: hex dumps of normal vs evil calldata (sighash/address/value rows), prompt
   screenshots (shown vs omitted fields), test-dApp steps, deploy receipts.
2. Parity gap (unpriced in corpus): four-cell matrix screenshots — reference blocked,
   in-wallet executed — plus the wallet-active step on a test wallet. Without the last
   step the row is a parity observation; file it as one.
3. Impact sentence names the user's blind action ("send/approve any number of tokens
   without knowing it," WEB3-1651429) — writer discipline: state which prompt field the
   user could not see.

## P4 — Modern hardening fingerprints (never corpus doctrine)

- **Strict-length decoding**: reject calldata whose length does not match the method
  signature before display; never fall back to a "normal contract call" prompt on
  unparsable data (WEB3-1651429's fork, closed).
- **Prompt completeness**: amount + symbol + recipient are hard requirements; a token
  symbol that cannot be resolved must fail closed, not omit.
- **WebView CSP parity**: in-wallet browsers enforce header CSP like reference browsers;
  `script-src` parity is the shipping gate (WEB3-1941767's gap).
- **Wallet-connect scoping**: provider exposure only after explicit per-site consent;
  already-connected inheritance is the drain sketch's enabler.

## P5 — Pre-report gates (kill-gates)

1. **Fork gate** — you named both parsers (execution vs display) and demonstrated the
   divergence on a test network. A contract-behavior claim without a parser fork dies here.
2. **Prompt gate** — you screenshot the misleading prompt (fields omitted). A malformed-
   calldata hex dump without the prompt dies here.
3. **Parity-consequence gate** — CSP divergence alone (bare `alert()`) dies here in this
   corpus (WEB3-1941767, `None`). Show the wallet-active step or file as an observation.
4. **Funds gate** — test network + self-owned wallet only. Any plan touching mainnet funds
   or another user's wallet dies here regardless of signal quality.
5. **Contract-doctrine gate** — Solidity/reentrancy/access-control claims die here: no
   corpus row demonstrates one. (A future contract-proof vault would own that class.)

## Module ↔ phase table

| Phase | Corpus evidence (module) | Anatomy of the paid pattern |
|---|---|---|
| P1 inventories parse surfaces | 00 (§§2–3) | calldata decoders + CSP delivery modes + connect state |
| P2 fuzzes truncation → parity | 00 (§§2–3) | one-byte delete; four-cell header/meta matrix |
| P3 proofs ladder, prompt-first | 00 (§§2–3) | hex + prompt screenshots; wallet-active step for parity |
| P4 hardening fingerprints | 00 (§§2–3) | strict-length reject; prompt completeness; WebView parity |
| P5 kill-gates | 00 (§§3–6) | fork gate; parity-consequence gate; funds gate |

## Non-goals

- Solidity exploitation (reentrancy, access control, overflow) — no corpus row
  demonstrates it; outside this vault's claims and this playbook's protocol.
- Mainnet fund-loss claims — test-network demonstrations only, per P0/P5.
- General mobile WebView hardening — owned by the `Mobile` vault; this playbook cites
  WEB3-1941767 only for CSP parity.
