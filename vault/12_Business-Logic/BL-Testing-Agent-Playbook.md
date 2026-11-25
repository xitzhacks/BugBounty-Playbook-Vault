---
title: "Business Logic Testing Agent Playbook — the executable protocol"
type: agent-playbook
category: business-logic
cwe: "CWE-840, CWE-799, CWE-366"
built: "2026-11-07"
corpus: "118 bucket rows (classified.json business-logic, DB-verified byte-identical) + 9 unclassified merges = 127 rows, 55 paid, $60,090"
bounty: "$60,090 corpus-floor (bucket $56,590/52 + merges $3,500/3) · commerce $19,150/8 · account/invite $9,010/12 · race $750/2 · rate-limit $3,100/6 · adjacent $24,580/24 · merges $3,500/3"
companion_modules: "commerce-payments-rewards · account-invite-access-workflows · race-condition-replay · rate-limit-state-abuse · adjacent-unclassified-noise"
quote_rule: "byte-true, from read bodies only, anchored in references/archive/BL-bodies-full-dump.txt"
---

# BL — Testing Agent Playbook (Business Logic)

Operational spine derived from 127 read bodies (all 127 full-body; corpus era ~2013–2024). Every quoted sentence is byte-true to `references/archive/BL-bodies-full-dump.txt`. Read the class modules before improvising.

Crown doctrine up front: **payouts track what the flaw touches in money, not how clever the tamper is.** The wallet-mint signature smuggle (BL-1295844, $7,500), the admin-approval overwrite (BL-1543159, $5,000) and the fee-discount replay (BL-1849626, $5,000) all pay because a real-money ledger moved; the same-author quantity tricks (BL-364843, BL-771694, BL-403783) carried no figure in the DB. Write the money delta into the report or the report does not exist.

## P0 — Program / policy read (before any interception)

1. Classify the program: commercial bounty program vs VDP vs the platform's own program. This corpus's account module is 19/32 `security` (HackerOne's own) rows — invitation accounting is the class's densest surface and it pays ($2,500, $1,000, $500 tier) because programs mint trust. The adjacent shelf's library programs (ibb/curl) pay flat by CVE tier, not by logic.
2. Find the money flows and the state machines on paper first: cart → checkout → payment callback; invite → accept → role; leave → re-invite; OTP issue → verify → change. The corpus's winning reports name the *unconsumed* or *replayable* transition (fee-discount accept never consumed, draft invite never marked accepted, leave-survey request re-sent with a swapped `team_handle`).
3. Read the policy for cash equivalents: which discounts, free trials, or plan upgrades the program prices, and whether client-side-only enforcement (BL-1070510's `is_active` flip, BL-672487's retailer cap) counts as in-scope in *this* program. If the program prices only server-side state, the client-edit rows (1070510, 1029027, 963774) are the kill-gate edge, not the core.
4. Kill-gate: no interception yet — P0 produces the *money-flow map* only.

## P1 — Entry-point inventory (what to probe, mapped from corpus)

| Surface | Why it is business-logic | Corpus proof |
|---|---|---|
| Cart / checkout / order-creation JSON | Quantity, totals, `unit_cost`, modifiers accepted from client | BL-364843 (negative qty), BL-771694 (`{"items":{"article_500":4,"article_1000":-2}}`), BL-403783 (0.1 qty), BL-361960 (sides count), BL-357929 (`quantity: 0` → 1) |
| Payment-provider redirect POST | Signature over concatenated fields; amount/currency parsed from the redirect body | BL-1295844 (Smart2Pay `hash(ALL_FIELDS_NAMES_VALUES_CONTACTED)`) |
| Approval / status PATCH APIs | `admin_approval`, `effective_status`, `eligible_for_bounty` settable by the owner API | BL-1543159 (PATCH ads status), BL-475660 (`eligible_for_bounty: true`), BL-460920 (bounty table via GraphQL) |
| One-time accept / claim endpoints | Never marked consumed; serial replay mints surplus | BL-1849626 (`/ajax/accept_fee_discount_offer` ×30), BL-331691 (draft invite token reused), BL-999789 (leave-survey replay) |
| Plan / product / order ID substitution | `plan_id`, `order_id`, `item_id`, `blogMembershipsId` user-enumerable; zero-price entries live | BL-511044 (`plan_Id 147` $0), BL-1213765 (order_id swap), BL-321938 (`item_id 18`), BL-882848 (education plan URL) |
| Invite / join / membership flows | Leave/rejoin loops, email-forwarding minting, sandbox UI lies | BL-334205 ($2,500), BL-331691 ($500), BL-999789, BL-1088966, BL-1486417 |
| OTP / verification endpoints | `0000` accepted, victim OTP accepted, token leaked in adjacent API | BL-2588329 ($2,000), BL-1443211, BL-2712583 |
| Role-gated settings POSTs | Age-verification, disabled-status, 2FA-password checks UI-only | BL-422698, BL-415398, BL-783258, BL-1691603 |
| Reconsumed GET/state probes | Most-recent-order keys, share-export URLs, draft exposure in exports | BL-1044285 ($2,900), BL-915140, BL-1664920 |

## P2 — Probe protocol (cheapest signal first)

1. **Serial replay before race.** Send the one-time action twice in a row. BL-1849626 was filed as a race and paid as a serial: `It seems a race was not even needed though, as I called it 30 times and 30 fee discounts were immediately applied to my account!` Only when serial fails do you escalate to the race module (03).
2. **Boundary values on every money field.** For each numeric the server trusts, sweep the corpus's edge set: negative quantity (364843, 771694), zero quantity (357929), fractional quantity (403783), above-max modifiers (361960), unbounded `rating` (2125049), swapped `order_id` (1213765), zero-price `plan_id` enumeration (511044), `amount_rounding: -1.0` (1089978). One field, six probes, then stop — the corpus rows each file exactly one delta.
3. **Response-editing probes.** The client-side-entitlement family: flip `is_active`/`"blocked":true` in the response (BL-1070510), return `merchants: []` to a cap endpoint (BL-672487), prepend a space to a paid identifier (BL-1029027), double-space an email (BL-963774), swap a Unicode lookalike (`İ`, BL-2033005). Each is a single response transformation; scope them as *server never re-validates* only if a second, account-level check also falls.
4. **State-machine walk.** Blueprint every transition the UI gates (leave program, delete account, cancel invite, downgrade plan) and replay the *request* after the transition the UI forbids: BL-999789 replays leave-survey with a new `team_handle`; BL-463828 views the program page after leaving; BL-1664920 exports drafts. The business rule defeated is always "you cannot do X after leaving Y."
5. **Parallel only at the end.** Turbo Intruder gate / grouped replay for gift-card (759247), credit-transfer (974892), location-limit (413759) and invite (1285538) rows — the module-03 ladder. State rung and hits-out-of-N in the report.

## P3 — Proof ladder (the demonstrations that paid)

1. **Real-money delta, screenshotted.** Steam wallet balance (1295844), fee-discount ledger $600,000 (1849626), delivered ad (1543159), reverb-bucks balance 7× (759247), helium credit balance (974892), 12 locations against a 4 cap (413759). The screenshot *is* the report.
2. **Countable surplus.** 100+ harvested invites (334205), 19 pending invites confirmed by support (999789), multiple memberships from one token (331691), live test credentials.
3. **Cross-principal effect.** Another user's order download links (1044285), another user's WhatsApp updates (1523584), another user's data credits (974892), a victim's JIRA project receiving the program's reports (226199).
4. **Config/state lies with a user-facing surface.** Eligible-for-bounty badges on a Response program (475660), recovery-SMS wrong domain (549364), `h1_analyst_*` usernames (1770797). Small money, but each has a literal screenshot.

## P4 — Modern hardening fingerprints (never corpus doctrine)

- **Money math**: server recomputes totals from catalog prices; quantities bounded (`0 < q ≤ max`, integer); no client-settable approval/status fields; plan IDs unguessable and zero-price plans disabled (BL-511044's own fix list).
- **Signatures**: length-prefixed / domain-separated, never `hash(name+value concat)` over attacker-controlled fields (1295844).
- **One-time actions**: consume-once flags checked in the same transaction as the grant; idempotency keys on payment/order endpoints; invitation tokens single-use, survey/leave requests bound to the (program, user) pair server-side (999789).
- **Identity**: OTPs with attempts budget and exact-match (2588329's `0000`; 1446107's post-verify mutation), verification tokens scoped to the requesting session, no token leakage in adjacent APIs (2712583).
- **Entitlements**: server-side re-validation of every paid feature per-request (1070510, 1029027, 672487, 963774) — Match-and-Replace should buy the attacker nothing.
- **Rate/state**: unthrottled endpoints budgeted (416906, 426547, 488923, 1051734); cookie-derived secrets (905816's `pd-pass_md5`) retired in favor of server-side session state.

## P5 — Pre-report gates (kill-gates)

1. **Delta gate.** Can you name the money/state delta and show it? `Actions speak louder`: quantity tricks, plan swaps and status flips die here without a before/after artifact. The corpus's honest self-limits (3136790's unfinished verification, 1089978's unverified gateway, 381356's undecided impact) all landed at or below $300.
2. **Server-side gate.** Does the effect survive outside your client? If your proof is a response edit with no server state, you have BL-1070510/672487 — reportable only where the program prices it; otherwise file under client-side and close.
3. **Boundary gate.** State what you did not reach (3136790: passport scan failed; harbor the honest stop, it paid $300; do not claim the full takeover).
4. **Privacy / PoC-harm gate.** Do not harvest other users' download links, payment tokens or credentials at scale to prove a point; the corpus's winners used their own accounts and one artifact each (1044285's most-recent-order only, 637267's own two accounts, 1365738's single image-name search).
5. **Theory gate.** Unverified-gateway math (1089978), offline-PoS MiTM without a live session (423467), prospective takeovers (1034023), and UX complaints (259400-class) are not findings; the adjacent shelf (`05`) prices them at $0 for a reason.

## Module ↔ phase table

| Phase | Corpus evidence (modules) | Anatomy of the paid pattern |
|---|---|---|
| P1 inventories money flows | 01 (§2–§8) | wallet POST, ads PATCH, accept-offer, plan/order IDs |
| P2 probes serial → boundary → state walk → parallel | 01 §4, 02 §3–§7, 03 §2–§5, 04 §2–§6 | replay, negative/zero/fractional qty, response edits, Turbo Intruder |
| P3 proofs: delta screenshot, countable surplus, cross-principal | 01 §2–§4, 02 §2–§4, 03 §2–§4 | wallet/ledger screenshots, invite counts, other-user artifacts |
| P4 hardening fingerprints | 01 §9, 02 §9, 04 §7 | server recomputation, consume-once, OTP budgets, entitlement revalidation |
| P5 kill-gates | 01 §9, 02 §8–§9, 05 §6 | theory/attempt/UX exhibits; server-side gate; PoC-harm gate |

## Non-goals

- Library/client CVE arithmetic (the curl/ibb shelf, module 05 §4): those are memory-safety and protocol classes priced flat by their own programs; this playbook does not price them.
- Smart-contract economics (BL-665798, BL-672664): protocol-level accounting proofs need test-net gas math, not web interception — the corpus rows are anchors, not procedure.
- Subdomain takeover mechanics (module 05 §3): inventory the dangling-resource catalog in the Subdomain-Takeover vault; here it is recorded only as bucket drift.
- Payment-card testing on live gateways: the corpus's winners used test stores, fake cards the program provided, or their own accounts (1849626 used a real Stripe account with disclosure).
