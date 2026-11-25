#!/usr/bin/env python3
"""
landscape_stamp.py — comprehensive "find the genuine stamp" scorer.

For a CTF challenge that hands you many records, each with metadata fields and a
claimed computed value (e.g. stamp: BI{<24hex>}), this brute-forces the derivation
space and reports EVERY candidate (field-set, hash, transform) that matches exactly
one record, together with that record's qc/validity status.

Correct derivation reproduces exactly ONE record; but a PLANTED DECOY can also be the
lone match and still be wrong — so we surface ALL exact-1 candidates and their qc, so
you can discard ones marked FAIL/invalid and hunt further if the "genuine-looking" one
is rejected. See ctf-verify-genuine skill for the full methodology + pitfalls.

ADAPT: edit parse() for your record format, and reps() for your field names.

Usage:  python3 landscape_stamp.py   (records in ./challenge/unit_*.dat)
"""
import glob, re, hashlib, struct
from itertools import combinations

# ---- 1) PARSE: adapt to your record format ----
def parse(path):
    t = open(path, errors='replace').read()
    d = {'file': path}
    for ln in t.splitlines():
        if ':' in ln and not ln.startswith('Fake Flag'):
            k, v = ln.split(':', 1)
            d[k.strip()] = v.strip()
    if 'stamp' not in d:
        return None
    m = re.search(r'BI\{([0-9a-fA-F]+)\}', d['stamp'])
    if not m:
        return None
    d['sh'] = m.group(1).lower()
    d['uid'] = int(d['unit_id'])
    d['nonce'] = d['nonce']
    return d

# ---- 2) FIELD REPRESENTATIONS: adapt field names here ----
def reps(r):
    uid = r['uid']; n = r['nonce']; nb = bytes.fromhex(n); ni = int(n, 16)
    out = {}
    out['nonce_b']      = nb
    out['nonce_b_rev']  = nb[::-1]
    out['nonce_be4']    = struct.pack('>I', ni % 0x100000000)
    out['nonce_le4']    = struct.pack('<I', ni % 0x100000000)
    out['nonce_s']      = n.encode()
    out['nonce_dec']    = str(ni).encode()
    out['uid_be2']      = struct.pack('>H', uid % 0x10000)
    out['uid_le2']      = struct.pack('<H', uid % 0x10000)
    out['uid_be4']      = struct.pack('>I', uid % 0x100000000)
    out['uid_le4']      = struct.pack('<I', uid % 0x100000000)
    out['uid_s']        = r['unit_id'].encode()
    out['uid_s3']       = ('%03d' % uid).encode()
    out['uid_s4']       = ('%04d' % uid).encode()
    out['uid_dec']      = str(uid).encode()
    return out

KEYS = list(reps({'unit_id': '1', 'nonce': '00000000'}).keys())

HF = {
    'md5':     lambda x: hashlib.md5(x).digest(),
    'sha1':    lambda x: hashlib.sha1(x).digest(),
    'sha256':  lambda x: hashlib.sha256(x).digest(),
    'sha512':  lambda x: hashlib.sha512(x).digest(),
    'blake2b': lambda x: hashlib.blake2b(x, digest_size=12).digest(),
}

def transforms():
    return {
        'raw': lambda d: d,
        'rev': lambda d: d[::-1],
        'sw':  lambda d: b''.join(d[i:i+4][::-1] for i in range(0, len(d), 4)),
        'rev_sw': lambda d: b''.join(d[i:i+4][::-1] for i in range(0, len(d), 4))[::-1],
    }

def windows(dg):
    out = []
    for s in range(0, max(1, len(dg) - 11)):
        out.append(dg[s:s+12])
    return out

# ---- 3) RUN ----
rows = [r for r in (parse(f) for f in sorted(glob.glob('challenge/unit_*.dat'))) if r]
print("stamped units parsed:", len(rows))
lens = set(len(r['sh']) for r in rows)
print("stamp hex-lengths present:", lens)

exact1 = []
for n in range(1, 4):  # single / pair / triple field combos
    for combo in combinations(KEYS, n):
        for hn, hf in HF.items():
            for tname, tf in transforms().items():
                cnt = 0; hit = None
                for r in rows:
                    try:
                        x = b''.join(reps(r)[k] for k in combo)
                    except KeyError:
                        cnt = -1; break
                    dg = hf(x)
                    matched = False
                    for w in windows(dg):
                        if tf(w).hex() == r['sh']:
                            matched = True; break
                    if matched:
                        cnt += 1; hit = (r['unit_id'], r.get('qc'))
                if cnt == 1:
                    exact1.append((combo, hn, tname, hit))
                elif 1 < cnt <= 3:
                    exact1.append((combo, hn, tname, f'MULTI{cnt}'))

print("\n=== EXACT-1 (or small-multi) candidate algorithms ===")
for e in exact1:
    print(e)
if not exact1:
    print("NONE  (no deterministic derivation found; likely keyed/secret or custom)")

# ---- 4) Dedicated PASS-only check ----
print("\n=== PASS-unit single-hash check ===")
for r in rows:
    if r.get('qc') != 'PASS':
        continue
    for kname, kv in reps(r).items():
        for hn, hf in HF.items():
            if hf(kv)[:12].hex() == r['sh']:
                print("PASS match:", r['unit_id'], kname, hn)
print("done PASS check")
