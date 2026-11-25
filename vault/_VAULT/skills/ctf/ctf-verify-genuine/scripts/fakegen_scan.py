#!/usr/bin/env python3
"""
fakegen_scan.py — CTF genuine-item diagnostic.

Goal: decide whether the "fake" stamps share a generator you can invert, or are
independent noise. Score every candidate formula by HOW MANY records it matches.

Reads records from a dir of `unit_NNNN.dat`-style files (each a `key: value` text
blob containing a `stamp: BI{<hex>}` line). Reports every formula matching >=MIN
records, plus the overall max, so you can see if a shared generator exists.

If the best formula matches only 1 (or <5) records -> fakes are NOISE -> the
genuine item needs a secret/structural quirk you cannot brute-force from metadata.
If a formula matches many records -> that is the FAKE generator; the outlier is genuine.

Adapt `reps()` / `cands` to your field names. Run:
    python3 fakegen_scan.py <records_dir> [min_match=5]
"""
import sys, glob, re, hashlib, struct
from collections import Counter

MIN = int(sys.argv[2]) if len(sys.argv) > 2 else 5
base = sys.argv[1] if len(sys.argv) > 1 else 'challenge'

def parse(d):
    for ln in open(d, errors='replace'):
        if ln.startswith('stamp:'):
            m = re.search(r'BI\{([0-9a-fA-F]+)\}', ln)
            if m: return m.group(1).lower()
    return None

def meta(d):
    out = {}
    for ln in open(d, errors='replace'):
        if ':' in ln and not ln.startswith('Fake Flag'):
            k, v = ln.split(':', 1); out[k.strip()] = v.strip()
    return out

files = sorted(glob.glob(base + '/unit_*.dat'))
rows = []
for f in files:
    sh = parse(f)
    if not sh: continue
    md = meta(f)
    rows.append({'sh': sh, 'uid': int(md['unit_id']), 'nonce': md['nonce'],
                 'ni': int(md['nonce'], 16)})
print("stamped:", len(rows))

def tf(b, k):
    if k == 'raw': return b
    if k == 'rev': return b[::-1]
    return b''.join(b[i:i+4][::-1] for i in range(0, 12, 4))

def reps(u, n):
    return {
        'n_hex': bytes.fromhex(n), 'n_hex_rev': bytes.fromhex(n)[::-1],
        'n_ascii': n.encode(), 'n_int_be': struct.pack('>I', int(n, 16)),
        'n_int_le': struct.pack('<I', int(n, 16)), 'n_ascii8_rev': n[::-1].encode(),
        'u_str': str(u).encode(), 'u_be4': struct.pack('>I', u),
        'u_le4': struct.pack('<I', u), 'u_be2': struct.pack('>H', u),
        'u_le2': struct.pack('<H', u),
    }

formula_hits = Counter()
formula_units = {}
cands = {}
for r in rows:
    R = reps(r['uid'], r['nonce'])
    for k, v in R.items():
        cands.setdefault(k, {})[r['uid']] = v

# single-field hashes
for fld in cands:
    for hn in ['md5', 'sha1', 'sha256', 'sha512']:
        for tk in ['raw', 'rev', 'sw']:
            cnt = 0; units = []
            for r in rows:
                dg = hashlib.new(hn, cands[fld][r['uid']]).digest()[:12]
                if tf(dg, tk).hex() == r['sh']:
                    cnt += 1; units.append(r['uid'])
            if cnt >= MIN:
                formula_hits[(fld, hn, tk)] = cnt; formula_units[(fld, hn, tk)] = units

# double-field (no separator + a few separators)
for f1 in cands:
    for f2 in cands:
        if f1 == f2: continue
        for sep in [b'', b'_', b':', b'|']:
            for hn in ['md5', 'sha1', 'sha256']:
                for order in ['12', '21']:
                    cnt = 0; units = []
                    for r in rows:
                        a = cands[f1][r['uid']]; b = cands[f2][r['uid']]
                        msg = a + sep + b if order == '12' else b + sep + a
                        dg = hashlib.new(hn, msg).digest()[:12]
                        if dg.hex() == r['sh']:
                            cnt += 1; units.append(r['uid'])
                    if cnt >= MIN:
                        key = (f'{f1}{"+sep+" if order=="12" else ""}|{f2}', hn, sep)
                        formula_hits[key] = cnt; formula_units[key] = units

print("formulas matching >=%d units:" % MIN, len(formula_hits))
if formula_hits:
    for k, c in formula_hits.most_common(20):
        print(" ", k, c, "units:", formula_units[k][:10])
else:
    print("NO formula matches >=%d units -> fakes are independent noise; genuine is NOT a metadata hash." % MIN)
