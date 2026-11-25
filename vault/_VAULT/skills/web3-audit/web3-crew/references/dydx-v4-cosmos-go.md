# dYdX v4 (Cosmos SDK / Go) — Crew Re-targeting Knowledge Bank

## Why this exists
The web3-crew ship default targets K2 (Rust/Soroban). dYdX v4 is **Go / Cosmos
SDK** — different language, different PoC harness (`testutil/app`, not Foundry /
cargo). The crew's 5 role files + orchestrator + PoC template were rewritten for
dYdX at `/home/user/Project/web3-crew/` (roles/*.md, orchestrator.md,
config.yaml, templates/ExploitPoC.go). This file is the portable knowledge bank.

## Re-targeting recipe (for ANY new target)
1. Identify the stack: Solidity → Foundry `.t.sol`; Soroban/Rust → `cargo
   #[test]`; **Cosmos SDK / Go → `go test` against the app's `testutil` harness**.
2. Rewrite `roles/junior_dev` (mapper) for the module layout of that stack.
3. Rewrite `roles/senior_dev` (investigator) with stack-specific bug classes.
4. Rewrite `roles/junior_mgr` (critic) with that stack's invariants.
5. Rewrite `roles/senior_mgr` (architect) + `templates/` for the REAL test-harness API.
6. Subagents get the full role file pasted into context (they have no skill access).
7. **Verify the PoC template actually compiles against the harness BEFORE dispatch**
   (a template that won't build wastes the L4 subagent's whole run).

## dYdX v4 module map (audit surface)
- `x/clob` — on-chain orderbook, orders, matches, liquidations, stateful orders,
  rate limits, equity tier, deleveraging, megavault.
- `x/perpetuals` — perpetual markets, funding ticks, open interest, collateral.
- `x/subaccounts` — collateral / asset & perpetual positions, withdrawals.
- `x/prices` — oracle price store, market params, smoothing/median.
- `x/vault` — megavault shares, deposit/withdraw, owner/operator.
- `x/rewards`, `x/vest`, `x/sending`, `x/bridge`, `x/ratelimit`, `x/affiliates`,
  `x/revshare`, `x/listing`, `x/govplus`, `x/feetiers`, `x/delaymsg`, `x/accountplus`.

## Bug classes (hunt ALL — grep patterns in roles/senior_dev.md)
1. Subaccounts collateral accounting (`UpdateSubaccounts`, `applyAssetUpdate`,
   `applyPerpetualUpdate`, `WithdrawableBalance`, `signed.Int` math).
2. CLOB orderbook/matching integrity (`ValidateOrder`, `ValidateMatchedOrders`,
   self-trade at crossed price, FOK/IOC/post-only, stateful-order replay, rate-limit split).
3. Liquidation / deleveraging (`ProcessLiquidation`, `OffsetSubaccount`, HF gate,
   insurance-fund drain).
4. Perpetuals funding (`MaybeProcessNewFundingTick` monotonicity,
   `FundingRateClampFactorPpm`, `ModifyOpenInterest`).
5. Prices oracle (`UpdatePrice`, `MinExchanges`, median, stale/expired).
6. Vault shares (`DepositToVault`/`WithdrawFromVault` rounding, first-depositor /
   donation attack, total==sum invariant, Owner vs Operator separation).
7. Authority / governance spoofing (`msg.Authority == k.GetAuthority()`; a
   missing check = anyone creates markets / clob pairs → CRITICAL).
8. Bridge / ratelimit (`bridgeEventId` replay/double-count, module-account bypass).
9. Signed-int overflow/underflow (`signed.Int` `.Sub`/`.Quo`, `big.Int` misuse).
10. DelayMsg / accountplus (cancel/modify auth, authenticator DoS).
11. Rewards / vest / revshare (double-count, vested>total mint, missing authority).

## PoC mechanic (VERIFIED against this repo version)
- Package: `package keeper_test` (matches peer tests in `x/<m>/keeper/`).
- App: `tApp := testapp.NewTestAppBuilder(t).Build()` then `ctx := tApp.InitChain()`.
- Keepers via `tApp.App.ClobKeeper` etc (App is a `*app.App` pointer).
- Seed state with keeper setters; call handlers like `k.PlaceOrder(ctx, order)`.
- Assert the broken invariant; a REAL bug = the assertion FAILS (proves the
  protocol guarantee is violated). If it passes, fix the exploit steps.
- Run: `cd protocol && go test ./x/clob/keeper/... -run TestExploit_C01 -v`.
- NEVER touch mainnet/testnet; the bounty prohibits mainnet testing.
- Respect out-of-scope: no read-only-only findings, no known/paid duplicates, no
  third-party CVEs without an exploit path against dYdX, no mainnet interaction.

## Severity (Cantina dYdX definitions)
- Critical: fund theft / insolvency / freeze / unauthorized mint ($150k–1m+).
- High: chain halt / settlement failure / matching-engine degradation ($50k–150k).
- Medium: staking / governance failures without fund loss ($5k–50k).
- Low: indexer/client display + event-parse issues, no on-chain impact ($50–5k).
