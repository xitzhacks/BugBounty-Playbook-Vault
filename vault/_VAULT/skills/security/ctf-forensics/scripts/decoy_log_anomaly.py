#!/usr/bin/env python3
"""decoy_log_anomaly.py — surface the real events in decoy-stuffed forensic logs.

Normalizes each line (masks IPv4, long hex, HH:MM:SS, YYYY-MM-DD, [bracketed], bare
numbers) then treats the MOST COMMON normalized template as the decoy and prints
every line whose normalized form is NOT that dominant template. Handles \\r\\n.

Usage:  python3 decoy_log_anomaly.py <logfile> [logfile2 ...]
"""
import re, sys, collections

def normalize(line):
    s = line
    s = re.sub(r'\d{1,3}(?:\.\d{1,3}){3}', '<IP>', s)
    s = re.sub(r'\b[0-9a-fA-F]{8,}\b', '<H>', s)
    s = re.sub(r'\d{2}:\d{2}:\d{2}', '<T>', s)
    s = re.sub(r'\d{4}-\d{2}-\d{2}', '<D>', s)
    s = re.sub(r'\[[^\]]*\]', '[..]', s)
    s = re.sub(r'\b\d+\b', '<N>', s)
    return s.strip()

def main():
    for path in sys.argv[1:]:
        try:
            lines = open(path, encoding='utf-8', errors='replace').read().splitlines()
        except OSError as e:
            print(f"[!] {path}: {e}"); continue
        tmpl = collections.Counter(normalize(l) for l in lines)
        if not tmpl:
            print(f"{path}: empty"); continue
        dom, domc = tmpl.most_common(1)[0]
        out, seen = [], set()
        for i, l in enumerate(lines):
            t = normalize(l)
            if t != dom and t not in seen:
                seen.add(t); out.append((i, l))
        print(f"\n##### {path}  ({len(lines)} lines, dominant-template count={domc}, {len(out)} anomaly templates) #####")
        for i, l in out[:20]:
            print(f"  L{i}: {l[:220]}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python3 decoy_log_anomaly.py <logfile> [...]")
        sys.exit(1)
    main()
