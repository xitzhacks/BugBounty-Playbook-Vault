# Worked example — MPC additive secret-sharing mask-reuse

Challenge: "THE HUNT" (CRYPTO, 300 pts, author Tanmay M). Zip contained two
parts: "The Gate" (MPC math, below) and "The Chest" (Caesar cipher — see
`ctf-classical-cipher`; carved text `CL{Vqhoo_ri_dxuvf}` → Caesar shift 3 →
`CL{Snell_of_aursc}`).

## The Gate — challenge text
```
modulus p = 1000003
Protocol:
  A = x_A + r_AB - r_AC
  B = x_B + r_BC - r_BA
  C = x_C + r_CA - r_CB      (all mod p)
IMPORTANT: Someone's pairwise masks are accidentally reused between rounds.

Round 1 (calibration): Alice's private = 3141
  public A=414672 B=319077 C=567829  published sum=301575
Round 2 (target): Alice's private = ???
  public A=418850 B=530835 C=526081  published sum=475763
Goal: hidden Round-2 value.
```

## Solve
- Sum checks: `(A1+B1+C1)%p == 301575` ✓ ; `(A2+B2+C2)%p == 475763` ✓
  (masks cancel in the sum, so each sum equals the sum of the three privates).
- Alice's masks reused ⇒ `A2−A1 = xA2 − xA1`
  ⇒ `xA2 = 3141 + (418850 − 414672) mod 1000003 = 3141 + 4178 = 7319`.
- Answer: **7319**.

### Why not Bob/Carol?
Their Round-1 privates are NOT given, so only deltas (`B2−B1`, `C2−C1`) are
recoverable — not absolute values. The challenge hands exactly Alice's R1 value,
marking her as the anchored target. The fact that
`(S2−xA2) − (S1−xA1) mod p = 170010 ≠ 0` confirms ONLY Alice's masks were
reused (not all three) — exactly what the hint states. This nonzero mismatch is
the expected consistency signal, not a contradiction.

## Generic solver
`scripts/mpc_mask_reuse.py`:
```
python3 scripts/mpc_mask_reuse.py --p 1000003 --xA1 3141 \
  --A1 414672 --B1 319077 --C1 567829 --S1 301575 \
  --A2 418850 --B2 530835 --C2 526081 --S2 475763
```
→ prints `xA2 = 7319` and the consistency check.

## The "what was overlooked" framing
The team saw valid per-round records (sums matched, shares looked consistent)
but missed that a *reused mask* between rounds leaks the delta of the masked
party's private value. Because Alice's R1 private was published as calibration,
that delta is absolute. Fix = fresh independent masks every round (never reuse
pairwise randomness across sessions/rounds).
