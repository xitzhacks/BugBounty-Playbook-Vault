#!/usr/bin/env python3
"""MPC additive secret-sharing mask-reuse solver.

Protocol:  A = xA + rAB - rAC ; B = xB + rBC - rBA ; C = xC + rCA - rCB  (all mod p)
Published sum S = A+B+C == xA+xB+xC (mod p) because masks cancel pairwise.

If party X's masks are reused across two rounds, then for X:
   AX2 - AX1 = xX2 - xX1   =>   xX2 = xX1 + (AX2 - AX1) mod p
Only the party whose Round-1 private value is KNOWN can be recovered absolutely;
that party is the intended target.

Usage (defaults = solved "THE HUNT" Gate challenge):
  python3 mpc_mask_reuse.py \
    --p 1000003 --xA1 3141 \
    --A1 414672 --B1 319077 --C1 567829 --S1 301575 \
    --A2 418850 --B2 530835 --C2 526081 --S2 475763
"""
import argparse

def solve(p, xA1, A1, B1, C1, S1, A2, B2, C2, S2):
    print(f"p={p}")
    c1 = (A1 + B1 + C1) % p
    c2 = (A2 + B2 + C2) % p
    print(f"Round1 sum check A+B+C%p={c1} == S1? {c1 == S1}")
    print(f"Round2 sum check A+B+C%p={c2} == S2? {c2 == S2}")

    # Try each party as the reused-mask one. Only Alice is anchored (xA1 given).
    cands = {
        'Alice': (xA1 + (A2 - A1)) % p,
        'Bob':   (B2 - B1) % p,   # only delta; xB1 not given
        'Carol': (C2 - C1) % p,   # only delta; xC1 not given
    }
    print("\nPer-party (AX2-AX1) mod p  [recovered value IF that party's masks "
          "reused AND its R1 private known]:")
    for name, val in cands.items():
        anchored = (name == 'Alice')
        note = "  <-- ANCHORED (R1 private known = target)" if anchored \
               else "  (R1 private not given; delta only)"
        print(f"  {name:6s}: x2 = {val}{note}")

    xA2 = cands['Alice']
    print(f"\nIntended hidden value (Alice, anchored): {xA2}")
    mismatch = ((S2 - xA2) - (S1 - xA1)) % p
    print(f"Consistency: (S2-xA2)-(S1-xA1) mod p = {mismatch}  "
          f"(nonzero expected => only Alice's masks reused, not all)")
    return xA2

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--p', type=int, default=1000003)
    ap.add_argument('--xA1', type=int, default=3141,
                    help='known Round-1 private value (the anchored/target party)')
    ap.add_argument('--A1', type=int, default=414672)
    ap.add_argument('--B1', type=int, default=319077)
    ap.add_argument('--C1', type=int, default=567829)
    ap.add_argument('--S1', type=int, default=301575)
    ap.add_argument('--A2', type=int, default=418850)
    ap.add_argument('--B2', type=int, default=530835)
    ap.add_argument('--C2', type=int, default=526081)
    ap.add_argument('--S2', type=int, default=475763)
    a = ap.parse_args()
    solve(a.p, a.xA1, a.A1, a.B1, a.C1, a.S1, a.A2, a.B2, a.C2, a.S2)

if __name__ == '__main__':
    main()
