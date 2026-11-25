# Cosmos SDK App-Chain Audit (Go modules) — dYdX v4 style

The 10 Solidity bug classes still apply conceptually, but a Cosmos SDK app-chain
(dYdX v4, Osmosis, Injective, etc.) has a different execution + trust model.
Solidity greps are useless here; Go `x/<module>/keeper` review + the ante/proposal
trust model is the game. Derived from a dYdX v4 `protocol` audit.

## Module anatomy (where bugs live)
- `x/<module>/keeper/*.go` — `func (k Keeper) ...` = internal state mutation;
  `func (k msgServer) ...` = tx entry points. **Cross-module keeper calls carry
  the CALLER's auth**, not their own — a keeper-only module (e.g. `subaccounts`,
  no MsgServer) trusts every caller module. Map the caller graph; the auth
  boundary is the outermost msgServer.
- `x/<module>/types/tx.pb.go` + `proto/.../tx.proto` — `option (cosmos.msg.v1.signer)`
  declares WHO must sign. `= "authority"` → gov/module-gated; `= "subaccount_id"` /
  `= "sender"` → the named field's owner must sign (user-facing). ALWAYS read the
  .proto signer option before claiming "no auth check" — the signer annotation is
  the auth, enforced by the SDK ante, not by an in-handler `HasAuthority`.
- `types/msg_*.go` `ValidateBasic()` — stateless validation, runs before ante.

## The app-injected msg trust model (CRITICAL to get right)
Some msgs have NO in-handler authority check yet are safe because they are
**app-injected / proposer-only**. Check `lib/ante/app_injected_msg.go`
(`IsAppInjectedMsg`) and `app/ante/msg_type.go` (`ValidateMsgTypeDecorator`):
- App-injected msgs must be the ONLY msg in the tx, DeliverTx-only, proposer-built.
- dYdX examples: `MsgProposedOperations` (clob), `MsgAddPremiumVotes` (perpetuals),
  `MsgUpdateMarketPrices` (prices), `MsgAcknowledgeBridges` (bridge).
- Verdict: external forgery is blocked at the ante layer → these findings are
  **proposer-trust / likely downgraded** unless the keeper blindly trusts msg
  contents AND a downstream gov/delaymsg step also fails to re-validate.
- Pitfall: MAP-style structural scans flag these as "no authority check" SUSPECT.
  That is a STRUCTURAL flag, not a bug. Resolve it against the ante before rating.

## High-value bug classes for perp DEX / vault app-chains
1. **Vault share math (ERC4626 ported to Go)** — `MintShares`: first deposit mints
   1:1 when `totalShares==0`, later `deposit*totalShares/equity` with big.Int `Quo`
   (truncates). Look for MISSING virtual shares / min-first-deposit → inflation /
   donation attack. Enabling primitive: a user-facing transfer (`x/sending`
   `CreateTransfer`, no authority) into the pooled vault's deterministic module
   subaccount inflates equity WITHOUT minting shares. Transfers only collateral-check
   the SENDER, never the recipient credit.
2. **Collateral / withdrawal gating gaps** — freeze logic (negative-TNC seen,
   chain-outage) often keys on `updateType == Withdrawal || Transfer`. A `Deposit`-typed
   update path can skip the freeze. Enumerate every UpdateType and which guards apply.
3. **Matching integrity (CLOB)** — self-trade check comparing the FULL SubaccountId
   (owner+number) not owner → wash trading across one owner's own subaccounts
   (reward farming, premium/funding-sample nudging via recorded trade price).
   Zero-quote-quantum fills that only `log.ErrorLog` and continue → free position transfer.
4. **big.Int rounding direction** — `Quo` truncates toward zero. Check every division
   in redeem/mint/fee math: does rounding favor the protocol or the user? Read/decrement
   ordering: values computed from a snapshot read BEFORE a mutating cross-module call
   (e.g. `ProcessTransfer` that could reenter) can desync total vs per-owner sums.
5. **Invariants** — dYdX registers NONE via Cosmos `RegisterInvariants`; "invariants"
   are inline `panic(...)` guards in keeper logic. Treat those panics as the
   ground-truth guarantees. Absence of a post-condition assertion after paired
   state decrements (totalShares vs sum(ownerShares)) is a desync candidate.

## Workflow that worked
1. Read `MAP.md` (if a cartographer layer produced one) — gives handler:line,
   auth model, cross-module call counts, SUSPECT flags. Trust it for navigation,
   re-derive every verdict from source.
2. Batch-read the priority modules' keeper + msg_server + types in parallel.
3. For each SUSPECT: read the .proto signer option AND the ante model before rating.
4. Write `CANDIDATES.md` with exact `file:line` (source-read, not MAP-copied),
   severity-guess, actor (external vs proposer/gov-privileged), exploit sketch,
   and a local-PoC feasibility note. PoCs here are Go `testapp.NewTestAppBuilder(t).Build()`
   + keeper calls / `cargo`-free — NOT Foundry.
5. Include a "clearances" section: bug classes checked and cleared (funding clamp,
   premium-vote validation, signer auth) so L3/reviewers don't re-walk them.

## Grep starting points (Go, not Solidity)
```bash
# msgServer entry points and their auth
grep -rn "func (k msgServer)" x/*/keeper
grep -rn "HasAuthority\|GetAuthority" x/*/keeper
# proto signer options = the real auth
grep -rn "cosmos.msg.v1.signer" proto/
# app-injected / proposer-only set
grep -rn "IsAppInjectedMsg" lib/ante app/ante
# vault/share math and rounding
grep -rn "MintShares\|sharesToMint\|\.Quo(\|\.Mul(" x/vault/keeper
# inline invariant guards (no RegisterInvariants)
grep -rn "panic(" x/*/keeper | grep -i "invariant\|should never"
```
