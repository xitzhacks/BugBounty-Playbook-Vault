#!/usr/bin/env python3
"""Mixed-base log fragment reassembler for CTF challenges.

Usage:  python3 fragment_reassemble.py <booth_dir> [forced_base_alpha] [forced_base_beta] [forced_base_gamma]
  Reads booth_<name>.log files. Each non-comment line is JSON with keys:
    tag, valid, color, date, timestamp (ISO w/ tz offset), payload
  Booth color map: alpha=saffron, beta=white, gamma=green.

Behaviour:
  1. Keep entry only if valid==true AND tag=="CEREMONY" AND color matches booth AND date==target date.
  2. Decode payload with hex/b64/b32 (forced base if given, else pick the clean one).
  3. Print the chronological-UTC assembly AND brute-force single-brace permutations.
"""
import base64, re, json, os, itertools, sys
from datetime import datetime, timezone

def dec(s, m):
    try:
        if m == 'hex' and re.fullmatch(r'[0-9a-fA-F]+', s) and len(s) % 2 == 0:
            return bytes.fromhex(s).decode('latin1')
        if m == 'b64':
            return base64.b64decode(s + '=' * (-len(s) % 4)).decode('latin1')
        if m == 'b32':
            u = s.upper().replace('=', '')
            if re.fullmatch(r'[A-Z2-7]+', u):
                return base64.b32decode(u + '=' * (-len(u) % 8)).decode('latin1')
    except Exception:
        return None
    return None

def printable(s):
    return s and all(32 <= ord(c) < 127 for c in s)

def main(d, bases=None):
    bases = bases or {}
    tricolor = {'alpha': 'saffron', 'beta': 'white', 'gamma': 'green'}
    entries = []
    for booth, color in tricolor.items():
        path = os.path.join(d, f'booth_{booth}.log')
        for line in open(path):
            line = line.strip()
            if not line.startswith('{'):
                continue
            o = json.loads(line)
            if o.get('valid') is not True or o.get('tag') != 'CEREMONY':
                continue
            if o.get('color') != color or o.get('date') != '15-08-1947':
                continue
            entries.append((booth, o['timestamp'], o['payload']))

    decs = []
    for booth, ts, p in entries:
        forced = bases.get(booth)
        if forced:
            r = dec(p, forced)
            assert r is not None, f"{booth} {p} not decodable as {forced}"
            decs.append((booth, ts, r))
            continue
        for m in ('hex', 'b64', 'b32'):
            r = dec(p, m)
            if r is not None and printable(r):
                decs.append((booth, ts, r)); break
        else:
            raise SystemExit(f"no clean decode for {booth} {p}")

    decs_utc = sorted(decs, key=lambda x: datetime.fromisoformat(x[1]).astimezone(timezone.utc))
    chrono = ''.join(r for _, _, r in decs_utc)
    print(f"[+] genuine fragments: {len(decs)}")
    for booth, ts, r in decs_utc:
        print(f"    {booth:5} {ts} -> {r!r}")
    print(f"[+] CHRONO-UTC ASSEMBLY: {chrono}")

    if '{' in chrono and '}' in chrono:
        i, j = chrono.index('{'), chrono.index('}') + 1
        print(f"[+] BRACE-DELINEATED: {chrono[i:j]}")

    txts = [r for _, _, r in decs]
    hits = []
    for perm in itertools.permutations(txts):
        s = ''.join(perm)
        if s.count('{') == 1 and s.count('}') == 1 and s.endswith('}') and printable(s):
            hits.append(s)
    seen = set()
    print(f"[+] {len(hits)} brace-balanced permutations (deduped):")
    for s in hits:
        if s not in seen:
            seen.add(s); print(f"    {s}")
            if len(seen) >= 30:
                break

if __name__ == '__main__':
    d = sys.argv[1] if len(sys.argv) > 1 else '.'
    fb = {}
    if len(sys.argv) > 4:
        fb = {'alpha': sys.argv[2], 'beta': sys.argv[3], 'gamma': sys.argv[4]}
    main(d, fb)
