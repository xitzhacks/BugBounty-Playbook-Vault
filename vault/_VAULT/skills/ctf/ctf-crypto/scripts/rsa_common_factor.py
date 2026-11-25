#!/usr/bin/env python3
"""Common-factor (shared-prime) textbook RSA solver.

Usage:  python3 rsa_common_factor.py <dir>
  dir must contain pubkeyN.txt (lines: n = ..  e = ..) and ciphertextN.txt (decimal int).

Recovers p = gcd(n1,n2), factors both moduli, derives d per key, decrypts each
half, strips leading nulls, and prints both concatenation orders.
"""
import re, sys, os, glob
from math import gcd

def parse_pub(p):
    t = open(p).read()
    n = int(re.search(r'n\s*=\s*(\d+)', t).group(1))
    e = int(re.search(r'e\s*=\s*(\d+)', t).group(1))
    return n, e

def parse_ct(p):
    return int(re.search(r'(\d+)', open(p).read()).group(1))

def main(d):
    pubs = sorted(glob.glob(os.path.join(d, 'pubkey*.txt')))
    cts  = sorted(glob.glob(os.path.join(d, 'ciphertext*.txt')))
    assert len(pubs) >= 2, "need >=2 pubkeys"
    ns, es, cs = [], [], []
    for p, c in zip(pubs, cts):
        n, e = parse_pub(p); ns.append(n); es.append(e); cs.append(parse_ct(c))

    p = gcd(ns[0], ns[1])
    assert p != 1, "no shared prime (gcd==1) -- wrong technique"
    print(f"[+] shared prime p found ({p.bit_length()} bits)")
    msgs = []
    for i in range(len(ns)):
        q = ns[i] // p
        assert p * q == ns[i]
        phi = (p - 1) * (q - 1)
        d = pow(es[i], -1, phi)
        m = pow(cs[i], d, ns[i])
        k = (ns[i].bit_length() + 7) // 8
        txt = m.to_bytes(k, 'big').lstrip(b'\x00').decode('utf-8', 'replace')
        msgs.append(txt)
        print(f"[+] m{i+1} = {txt!r}")

    for order in (msgs, msgs[::-1]):
        s = ''.join(order)
        print(f"    concat: {s}")

if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else '.')
