#!/usr/bin/env python3
"""Generic scorer for 'find the genuine item' CTF challenges.

Given many records, each with metadata + a printed value (e.g. stamp: BI{<hex>}),
brute-force (field-set x hash x transform) and report candidates that reproduce
EXACTLY ONE record's printed value. That unique record is the genuine one.

Adapt the `reps()` function to your record's fields. Works on the
CTF7 "Fake Flag Factory" unit_NNNN.dat layout out of the box.
"""
import json, hashlib, struct, glob, re, itertools, os

RECORDS_GLOB = 'challenge/unit_*.dat'   # adjust to your files
STAMP_RE = re.compile(r'BI\{([0-9a-fA-F]+)\}')

def parse_file(path):
    d = {'file': path}
    for line in open(path, errors='replace'):
        if ':' not in line:
            continue
        k, v = line.split(':', 1)
        k = k.strip(); v = v.strip()
        if k == 'Fake Flag Factory :: assembly line':
            continue
        if k == 'stamp':
            m = STAMP_RE.search(v)
            d['stamp_hex'] = m.group(1) if m else None
        else:
            d[k] = v
    return d

def reps(r):
    """Field representations for record r. Extend with your fields."""
    out = {}
    uid = int(r['unit_id']); nonce = r['nonce']
    out['uid_s']   = r['unit_id'].encode()
    out['uid_be4'] = struct.pack('>I', uid % 0x100000000)
    out['uid_le4'] = struct.pack('<I', uid % 0x100000000)
    out['nonce_s'] = nonce.encode()
    out['nonce_b'] = bytes.fromhex(nonce)
    out['nonce_be4'] = struct.pack('>I', int(nonce, 16) % 0x100000000)
    out['nonce_le4'] = struct.pack('<I', int(nonce, 16) % 0x100000000)
    for k in ['batch', 'shift', 'operator', 'qc']:
        if k in r:
            v = r[k] if not isinstance(r[k], list) else ''.join(r[k])
            out[k + '_s'] = v.encode()
    return out

def digest(x, hn):
    return {
        'md5':     hashlib.md5(x).digest()[:12],
        'sha1':    hashlib.sha1(x).digest()[:12],
        'sha256':  hashlib.sha256(x).digest()[:12],
        'sha512':  hashlib.sha512(x).digest()[:12],
        'blake2b': hashlib.blake2b(x, digest_size=12).digest(),
    }[hn]

def tr(d, t):
    if t == 'raw': return d
    if t == 'rev': return d[::-1]
    if t == 'sw':  return b''.join(d[i:i+4][::-1] for i in range(0, len(d), 4))
    raise ValueError(t)

def main():
    rows = [r for r in (parse_file(p) for p in glob.glob(RECORDS_GLOB)) if 'stamp_hex' in r]
    print(f"parsed {len(rows)} stamped records")
    data = [(r['unit_id'], r['stamp_hex'], reps(r)) for r in rows]
    block_names = list(reps(rows[0]).keys())
    hashfns = ['md5', 'sha1', 'sha256', 'sha512', 'blake2b']
    transforms = ['raw', 'rev', 'sw']
    scored = []
    for n in range(1, 5):
        for combo in itertools.combinations(block_names, n):
            for hn in hashfns:
                for trn in transforms:
                    cnt = 0; hit = None; ok = True
                    for uid, target, rp in data:
                        try:
                            x = b''.join(rp[k] for k in combo)
                        except KeyError:
                            ok = False; break
                        out = tr(digest(x, hn), trn).hex()
                        if out == target:
                            cnt += 1; hit = uid
                    if ok and cnt == 1:
                        scored.append((combo, hn, trn, hit))
                    elif ok and 1 < cnt <= 3:
                        scored.append((combo, hn, trn, hit))
    scored.sort(key=lambda s: -1 if s[0] == 1 else 0)
    print("UNIQUE-match candidates (combo, hash, transform, genuine_unit_id):")
    for s in scored:
        if isinstance(s[0], int):  # guarded above; normally tuple
            continue
        print(" ", s)
    if not scored:
        print("no candidate matched exactly 1 record; widen field reps or digest length")

if __name__ == '__main__':
    main()
