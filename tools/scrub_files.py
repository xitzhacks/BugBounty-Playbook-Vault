#!/usr/bin/env python3
"""Redact secrets/PII from every text file in a vault tree."""
import os, sys, json, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scrub_lib import scrub, is_binary

ROOT = sys.argv[1]
OUT = sys.argv[2] if len(sys.argv) > 2 else "scrub_files_report.json"
totals = collections.Counter()
changed_files = []
scanned = 0

for dirpath, dirnames, filenames in os.walk(ROOT):
    for fn in filenames:
        p = os.path.join(dirpath, fn)
        if is_binary(p):
            continue
        try:
            with open(p, "r", encoding="utf-8", errors="strict") as f:
                txt = f.read()
        except (UnicodeDecodeError, OSError):
            try:
                txt = open(p, "r", errors="ignore").read()
            except OSError:
                continue
        scanned += 1
        new, counts = scrub(txt)
        if counts and new != txt:
            with open(p, "w", encoding="utf-8") as f:
                f.write(new)
            totals.update(counts)
            changed_files.append({"file": os.path.relpath(p, ROOT), "counts": counts})

json.dump({"root": ROOT, "scanned": scanned, "totals": totals,
           "changed_files": changed_files}, open(OUT, "w"), indent=1)
print(json.dumps({"scanned": scanned, "changed_files": len(changed_files),
                  "totals": totals}, indent=1))
