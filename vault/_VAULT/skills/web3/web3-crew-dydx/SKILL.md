---
name: web3-crew-dydx
description: Run the 5-layer bug-hunting crew (Mapper → Investigator → Critic → Architect → Boss) against dYdX v4 protocol (Go / Cosmos SDK) or re-target it to another Go/Cosmos-SDK chain. Adapted from the K2/Soroban crew; produces MAP.md, CANDIDATES.md, VERDICT.md, CHAIN.md and runnable `go test` PoCs against testutil/app. Use when the user says "run the web3 crew", "audit dYdX", "hunt dYdX bugs", or gives a Cosmos-SDK repo + bounty scope.
---

# Web3 Crew — dYdX v4 / Go-Cosmos-SDK variant

A 5-layer agent hierarchy that hunts bugs in a Cosmos-SDK protocol repo. Each
layer runs as a `delegate_task` subagent (leaf, no skill access) with the FULL
role file pasted into `context`. Layer N's artifact is Layer N+1's input. YOU
(L5 / Boss) do the final file:line verification + actually run `go test`.

## When to use
- User gives a dYdX v4 (or any Go/Cosmos-SDK) target + bounty scope and says
  "run the crew" / "audit this" / "hunt bugs".
- Target stack is Go (not Solidity/Foundry, not Rust/Soroban). If the target is
  Solidity, use the `web3-audit` skill instead. If Rust/Soroban, the original
  `web3-crew` K2 variant.

## Prereqs (verify first)
- `go version` >= 1.22 (dYdX uses 1.24). `git`. Network for `go mod` downloads.
- Clone: `git clone --depth 1 https://github.com/dydxprotocol/v4-chain /home/user/Project/dydx-audit`
  then work in `/home/user/Project/dydx-audit/protocol`.
- Sanity build: `cd protocol && go build ./x/...` (proves toolchain + module path
  `github.com/dydxprotocol/v4-chain/protocol`).

## VERIFIED test harness API (do not guess — this is what makes PoCs compile)
```go
package keeper_test
import (
    "testing"
    testapp "github.com/dydxprotocol/v4-chain/protocol/testutil/app"
    "github.com/stretchr/testify/require"
)
tApp := testapp.NewTestAppBuilder(t).Build()
ctx := tApp.InitChain()
k := tApp.App.VaultKeeper          // or ClobKeeper / SubaccountsKeeper / SendingKeeper / PricesKeeper / PerpetualsKeeper
```
- Keepers are reached via `tApp.App.<X>Keeper` (pointer: `tApp.App` is `*app.App`).
- Seed state with keeper setters + `testapp.UpdateGenesisDocWithAppStateForModule`
  (see `x/vault/keeper/exploit_c_test.go` for a working genesis-seed helper).
- A REAL finding = the PoC test COMPILES and the assertion that proves the broken
  invariant FAILS (test errors). If it passes, the PoC is wrong — fix it.

## Crew files (under web3-crew/ after re-engineering)
- roles/junior_dev.md  (L1 Mapper — Go module map; never claims bugs)
- roles/senior_dev.md  (L2 Investigator — 11 dYdX bug classes w/ greps)
- roles/junior_mgr.md  (L3 Critic — invariant gate; KEEP/REJECT)
- roles/senior_mgr.md  (L4 Architect — exploit chain + Go PoC)
- roles/boss.md        (L5 You — verify + report)
- orchestrator.md      (sequential runbook via delegate_task)
- config.yaml          (target/scope/severity)
- templates/ExploitPoC.go (compiles against the real API; copy into x/<m>/keeper/)

## How to run (sequential, each waits for prior artifact)
1. L1 `delegate_task` goal: map `/home/user/Project/dydx-audit/protocol`, write
   MAP.md. context = full roles/junior_dev.md + REPO path. toolsets terminal/file/web.
2. L2 `delegate_task` goal: hunt bug classes using MAP.md, write CANDIDATES.md
   (exact file:line, source read). context = full roles/senior_dev.md + MAP path.
3. L3 `delegate_task` goal: filter CANDIDATES.md → VERDICT.md (KEEP/REJECT, cite
   failing gate #). context = full roles/junior_mgr.md + MAP + CANDIDATES path.
   Brief it on program scope (external-actor reachability; gov/validator-malice
   findings are usually out-of-scope; chain-linked findings must be judged together).
4. L4 `delegate_task` goal: for each KEPT finding, write CHAIN.md + a `_test.go`
   PoC; RUN `go test` until it compiles + fails-as-expected. context = full
   roles/senior_mgr.md + MAP + CANDIDATES + VERDICT path.
5. L5 YOU: read CHAIN.md + each PoC; re-read cited file:line; run
   `go test ./x/<m>/keeper/... -run TestExploit_C<NN> -v` yourself. Keep only
   verified + failing-as-expected. Draft the bounty report.

## Pitfalls (learned on the dYdX run)
- The original crew is hardcoded for K2 (Rust/Soroban, cargo, Foundry). DO NOT
  run it as-is against a Go repo — rewrite roles/orchestrator/template first.
- Subagents hallucinate file:line. Always re-verify cited lines yourself at L5.
- Severity: in `DepositToMegavault`, `MintShares` runs BEFORE the transfer, so a
  0-share deposit reverts the whole tx (victim funds NOT taken) → that's
  deposit-DoS/griefing (High), not single-tx theft (Critical). Check handler
  ordering before claiming theft.
- `MsgCreateTransfer` has NO authority check and `ValidateBasic` doesn't reject a
  module-owned recipient — that's the dYdX-specific C-02 root we found.
- Keep PoC in `package keeper_test`; import `testapp` + `require`; seed via
  genesis helper. Adding `_ = k; _ = ctx; _ = require.New` keeps the scaffold
  compiling before L4 fills it in.
- dYdX bounty: no mainnet testing, report via Cantina within 24h, no disclosure
  before fix+permission. Respect out-of-scope (read-only fns, third-party CVEs
  w/o exploit path, known/paid dupes).

## Re-targeting to another Go/Cosmos chain
Swap the module list in junior_dev.md, the bug classes in senior_dev.md, and the
keeper/TestApp API in senior_mgr.md + ExploitPoC.go (every Cosmos-SDK app has its
own `testutil/app`-style harness — find it and verify the constructor signature).
