---
title: "Web3 core — wallet parsers that lie by omission (blind approve) and browsers that drop the last defense (CSP)"
type: playbook
category: web3-core
cwe: "CWE-20"
source_count: 2
full_bodies_available: 2
corpus: "h1-brain disclosed_reports.db (3,673 rows), bucket web3 (classified.json) -> module web3-core (module_map_all.json)"
list_accessed: "2026-11-07"
note: "Anchor bodies: WEB3-1651429 (MetaMask parser gap, $1,000), WEB3-1941767 (MetaMask Android CSP gap, None). Claims trace to bodies read 2026-11-07."
---

# Web3 core — wallet parsers that lie by omission (blind approve) and browsers that drop the last defense (CSP)

## 1. Overview

Two rows, one program (MetaMask), **$1,000 / 1 row with a figure** (max $1,000). The bucket
name says "smart contract"; the bodies say *wallet parsing* twice. WEB3-1651429 pays $1,000
because the wallet's transaction prompt hid the amount on truncated calldata (a blind
transfer/approve on a phishing site); WEB3-1941767 records `None` because the Android
in-wallet browser ignored `Content-Security-Policy` headers — a gap its own researcher
debated filing. The corpus prices the prompt, not the contract, and the module refuses to
inflate either row into Solidity doctrine.

**Case-stock (2 rows / $1,000):**

| Case | Target | Mechanism | Bounty |
|---|---|---|---|
| [WEB3-1651429](https://hackerone.com/reports/1651429) | metamask | pre-0.5.0 calldata truncated one byte → wallet shows no amount (transfer/approve) | $1,000 |
| [WEB3-1941767](https://hackerone.com/reports/1941767) | metamask (Android browser) | CSP header ignored (`script-src 'none'` still executes) → wallet-active XSS | — |

## 2. The paid row: calldata truncation → blind transfer/approve (WEB3-1651429, $1,000)

The primitive is a parser strictness gap across two strictness regimes. Tokens compiled with
`solc < 0.5.0` do not check that calldata length matches parameter types — "it will load the
calldata as long as the params types need, regardless of the actual input length" — while
MetaMask's display parser cannot parse "unusual length" calldata like normal at all. The PoC
deletes one byte from the value field (…`989700` → …`9897`):

> The methods compiled with Solc below 0.5.0 will not check if the length of the input calldata matches the params types. It will load the calldata as long as the params types need, regardless of the actual input length. And the insufficient parts will be read as byte(00).

The wallet-side consequence is the payout sentence: on a phishing-site connection, the
transfer/approve prompt shows "a normal contract call without showing send to address, send
amount and token symbol," and:

> The attacker can induce the victims to send/approve any number of tokens without knowing it.

Note what the row does *not* prove about the contract: the token contract itself behaves
normally (it accepts the padded/truncated read). The bug is the *display parser* forking
from the *execution parser*. That fork — strictness mismatch between what the chain reads
and what the wallet shows — is the vault's only priced primitive, and the Steps (fork the
test dApp, deploy with solc 0.4.26, Rinkeby, `Create Token` → `Transfer Tokens` /
`Approve Tokens`) are written against a self-controlled test token, not a mainnet victim.

## 3. The unpriced row: the in-wallet browser drops CSP (WEB3-1941767, `None`)

The second MetaMask row is an Android-browser parity gap: pages that block
`<script>alert('Javascript is executed.')</script>` under `Content-Security-Policy:
script-src 'none'` in Chrome still execute it in the MetaMask browser — but only when the
policy arrives as a *header*. The `<meta>`-tag delivery is enforced in both browsers; the
header delivery is enforced in one:

> it seems that the browser in MetaMask ignores any Content-Security-Policy headers.

> Notice how our javascript IS executed despite the `Content-Security-Policy: script-src 'none'` header.

The impact chain is a wallet-drain sketch (site already "Connected" → XSS invokes the
transaction), and the researcher files it with an explicit self-doubt — "you could argue this
is a defence-in-depth measure and not a vulnerability" — resolving it only by the wallet's
own security burden ("you would expect it to be 'on par' with the security of any other
browser, if not more secure since we are dealing with crypto currencies/assets"). The DB
records no figure. The vault keeps the row at its filed weight: a *parity observation*
with a drain sketch, not a priced finding. Module readers must not cite WEB3-1941767 as
evidence that CSP gaps pay in this corpus — the corpus says the opposite (the parser-gap
row paid; the parity row did not, at least not in the DB).

## 4. The vault's boundary: no contract doctrine

Neither row demonstrates a contract-side bug (reentrancy, access control, overflow). The
only contract in the corpus is WEB3-1651429's self-deployed test ERC20 (solc 0.4.26) used
as a *trigger* for the wallet parser. A future Web3 vault with Solidity-proof rows would
own that doctrine; this vault owns the wallet/browser parse evidence and says so in every
section that might be over-cited.

## 5. What the corpus cannot price

No row prices mainnet fund loss, no row prices a contract exploit, and no row prices the
CSP gap. The single $1,000 prices a *test-network parser demonstration* whose impact
sentence claims blind approve at arbitrary amounts. Whether that impact would price higher
on mainnet is unknowable from this bucket — the vault writes the sentence, the price, and
the gap.

## 6. What pays, what doesn't

- The corpus pays **the prompt that misleads**: WEB3-1651429 ($1,000) hid the amount on
  truncated calldata and showed a "normal contract call." The wallet-consent surface is the
  priced primitive — not the token, not the chain.
- **Defense-in-depth parity does not pay at a listed figure here**: WEB3-1941767
  (`None`) is a full reproduction (meta-vs-header matrix, version named, drain sketch) that
  the DB leaves unpriced. The researcher's own doubt ("for you to decide") is part of the
  finding's weight. CSP-parity reports must demonstrate a *wallet-active* consequence in
  the report body — a script-execution screenshot alone would, in this corpus, be the same
  `None`.
- **Strictness forks are the portable lesson**: execution parser (lenient) vs display parser
  (strict) is the mechanism that paid. Any future parse-differential row should name both
  parsers. Rows that name neither are library notes, not findings — the PP-vault rule in
  Web3 dress.

## 7. Cross-references

- `XSS/` — WEB3-1941767's DB weakness (`XSS - Reflected`) and drain sketch; that vault
  owns XSS payoff doctrine.
- `Mobile/` — WEB3-1941767 is an Android WebView evidence row; that vault owns the
  Android-browser corpus.
- `Authentication-Session/` — wallet-consent hardening posture for blind approve
  (WEB3-1651429); cite the auth vault for the defensive side.
- Playbook P2 (`WEB3-Testing-Agent-Playbook.md`) encodes the calldata-fuzz and CSP-parity
  matrices from §§2–3.
