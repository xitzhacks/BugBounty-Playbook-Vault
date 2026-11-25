#!/usr/bin/env python3
"""Verify a vault tree/DB is clean: any scrub() hit left = residue."""
import os, sys, json, sqlite3, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scrub_lib import scrub, is_binary

ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = sys.argv[2] if len(sys.argv) > 2 else None
OUT = sys.argv[3] if len(sys.argv) > 3 else "verify_report.json"

totals = collections.Counter()
examples = collections.defaultdict(list)
changed_files = set()

if os.path.isdir(ROOT):
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in (".git", ".venv", "__pycache__")]
        for fn in filenames:
            p = os.path.join(dirpath, fn)
            if is_binary(p):
                continue
            try:
                txt = open(p, "r", errors="ignore").read()
            except OSError:
                continue
            _, counts = scrub(txt)
            if counts:
                rel = os.path.relpath(p, ROOT)
                changed_files.add(rel)
                totals.update(counts)
                for k in counts:
                    if len(examples[k]) < 3:
                        examples[k].append({"file": rel})

if DB and os.path.exists(DB):
    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True, timeout=120)
    skip = {t for t in []}
    tables = [r[0] for r in con.execute(
        "select name from sqlite_master where type='table' and name not like 'sqlite_%'")]
    tables = [t for t in tables if "_fts" not in t]
    for t in tables:
        cols = [r[1] for r in con.execute(f'pragma table_info("{t}")')
                if (r[2] or "").upper().startswith(("TEXT", "CHAR", "CLOB", "VARCHAR"))]
        if not cols:
            continue
        cur = con.execute(f'select rowid, {", ".join(chr(34)+c+chr(34) for c in cols)} from "{t}"')
        for row in cur:
            for c, v in zip(cols, row[1:]):
                _, counts = scrub(v)
                if counts:
                    totals.update(counts)
                    for k in counts:
                        if len(examples[k]) < 3:
                            examples[k].append({"table": t, "rowid": row[0], "col": c})
    con.close()

result = {"root": ROOT, "db": DB, "files_with_residue": len(changed_files),
          "totals": totals, "examples": examples}
json.dump(result, open(OUT, "w"), indent=1)
print(json.dumps({"files_with_residue": len(changed_files), "totals": totals}, indent=1))
for k, ex in examples.items():
    print(k, "->", ex[:2])
sys.exit(1 if totals else 0)
