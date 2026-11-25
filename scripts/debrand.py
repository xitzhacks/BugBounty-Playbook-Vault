#!/usr/bin/env python3
"""De-brand: replace every 'vault' variant across our scripts and rename the data files."""
import os, re, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
REPL = [
    ("public HackerOne vault", "public HackerOne vault"),
    ("the public HackerOne dataset", "the public HackerOne dataset"),
    ("Vault class", "Vault class"),
    ("Reports routed", "Reports routed"),
    ("Vault", "Vault"),
    ("CASESTOCK-LINK", "CASESTOCK-LINK"),
    ("reports.sqlite", "reports.sqlite"),
    ("reports.sqlite", "reports.sqlite"),
    ("reports.jsonl", "reports.jsonl"),
    ("reports", "reports"),
    ("_VAULT", "_VAULT"),
    ("vault", "vault"),
]
for f in sorted(os.listdir(ROOT)):
    p = os.path.join(ROOT, f)
    if not (f.endswith((".py", ".sh")) and os.path.isfile(p)):
        continue
    s = open(p).read()
    for a, b in REPL:
        s = s.replace(a, b)
    open(p, "w").write(s)
    print("rewrote", f)

# rename data files
for old, new in [("reports.sqlite", "reports.sqlite"),
                 ("reports.jsonl", "reports.jsonl")]:
    o, n = os.path.join(ROOT, old), os.path.join(ROOT, new)
    if os.path.exists(o) and not os.path.exists(n):
        os.rename(o, n); print("renamed", old, "->", new)
for ext in ("-wal", "-shm"):
    o, n = os.path.join(ROOT, "reports.sqlite" + ext), os.path.join(ROOT, "reports.sqlite" + ext)
    if os.path.exists(o):
        os.rename(o, n); print("renamed", os.path.basename(o))
