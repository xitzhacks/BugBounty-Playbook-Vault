---
name: web3-crew
description: Multi-agent bug-hunting crew for the K2 Lending Protocol (code-423n4/2026-04-k2, Code4rena). 5-layer hierarchy (Mapper -> Investigator -> Critic -> Architect -> Verifier) for Rust/Soroban smart-contract audit. Use when the user wants to run/extend the layered pipeline against the K2 target, or references "the web3 crew", "the agents", "k2 crew", or their hierarchy of Junior Dev / Senior Dev / Junior Manager / Senior Manager / Boss. PoCs are Rust `#[test]` in tests/c4/src/lib.rs (cargo test), NOT Foundry.
---

# web3-crew — K2 Lending Protocol Multi-Agent Audit Crew (Rust/Soroban)

A 5-layer agent hierarchy for the K2 Lending Protocol audit (Code4rena
2026-04-k2). Target is Rust on Stellar Soroban — NOT Solidity. PoCs are Rust
`#[test]` in `tests/c4/src/lib.rs` run via `cargo test --package k2-c4`, NOT
Foundry. Each layer is a narrow role; output of one feeds the next (a CHAIN,
run sequentially via delegate_task).

## The hierarchy
```
L5  BOSS / VERIFIER   (the user + main agent)  — final logic check, forge test, submission
L4  SENIOR MGR / ARCHITECT (subagent)          — exploit chain + Foundry PoC .t.sol
L3  JUNIOR MGR / CRITIC    (subagent)          — false-positive filter (KEEP/REJECT)
L2  SENIOR DEV / INVESTIGATOR (subagent)       — logic/math/access bugs, 10 classes
L1  JUNIOR DEV / MAPPER     (subagent)         — repo architecture map, no logic
```

## On-disk location
All role work-sets and scripts live at:
  /home/user/Project/web3-crew/

  README.md              overview + ethics
  orchestrator.md        runbook: how Boss chains the layers via delegate_task
  config.example.yaml    fill in target + RPC before running
  roles/
    junior_dev.md        L1 — The Mapper
    senior_dev.md        L2 — The Investigator (10 DeFi bug classes + grep)
    junior_mgr.md        L3 — The Critic (6-question false-positive gate)
    senior_mgr.md        L4 — The Architect (CHAIN.md + poctests/*.t.sol)
    boss.md              L5 — The Verifier (you)
  templates/
    ExploitPoC.t.sol     Foundry PoC scaffold

## How to run (Boss = main agent)
Read /home/user/Project/web3-crew/orchestrator.md. Summary:
1. Get from user: target repo path/URL + RPC (RPC optional => static-only).
2. Install tooling if missing: Foundry (`curl -L https://foundry.paradigm.xyz | bash; foundryup`),
   `pip install slither-analyzer web3`.
3. Clone/fetch target.
4. Run L1..L4 as SEQUENTIAL delegate_task calls, pasting the full role file
   contents into each subagent's `context` (subagents cannot load skills).
   Wait for each artifact (MAP.md -> CANDIDATES.md -> VERDICT.md -> CHAIN.md + poctests/).
5. Boss (you) verifies file:line refs, runs `forge test --fork-url $RPC`,
   drafts the Immunefi report. Submission is the user's call.

## Hard rules
- Sequential chain, NOT parallel (each layer needs the previous artifact).
- Subagents get the FULL role work-set pasted into context — they have no skill access.
- PoC only on forks/testnets/authorized contracts. Never exploit on mainnet.
- Boss is the only human-in-the-loop layer and owns submission + risk.
- Static-only mode (no RPC): L1-L3 run fully; L4 writes untested PoC templates only.
