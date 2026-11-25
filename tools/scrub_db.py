#!/usr/bin/env python3
"""Redact secrets/PII inside the vault SQLite DB and rebuild FTS indexes."""
import sqlite3, sys, os, json, hashlib, collections, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scrub_lib import scrub

DB = sys.argv[1]
OUT = sys.argv[2] if len(sys.argv) > 2 else "scrub_db_report.json"

SKIP_TABLES = {
    "chunks_fts", "chunks_fts_data", "chunks_fts_idx", "chunks_fts_docsize",
    "chunks_fts_config", "documents_fts", "documents_fts_data", "documents_fts_idx",
    "documents_fts_docsize", "documents_fts_config",
}

con = sqlite3.connect(DB)
con.execute("PRAGMA journal_mode=MEMORY")
con.execute("PRAGMA synchronous=OFF")
con.execute("PRAGMA temp_store=MEMORY")

tables = [r[0] for r in con.execute(
    "select name from sqlite_master where type='table' and name not like 'sqlite_%'")]
tables = [t for t in tables if t not in SKIP_TABLES]

totals = collections.Counter()
report = {}
t0 = time.time()


def _flush(con, t, text_cols, batch):
    for item in batch:
        if item[0] == "row":
            _, vals, sets = item
            con.execute(f'UPDATE "{t}" SET {sets} WHERE rowid=?', vals)
        else:
            _, h, rid = item
            con.execute(f'UPDATE "{t}" SET sha256=? WHERE rowid=?', (h, rid))
    con.commit()

for t in tables:
    cols = [(r[1], r[2]) for r in con.execute(f'pragma table_info("{t}")')]
    text_cols = [c for c, typ in cols if (typ or "").upper().startswith(("TEXT", "CHAR", "CLOB", "VARCHAR"))]
    if not text_cols:
        report[t] = {"rows": 0, "changed": 0, "note": "no text cols"}
        continue
    sel = ", ".join(f'"{c}"' for c in text_cols)
    rows = con.execute(f'select rowid, {sel} from "{t}"').fetchall()
    changed = 0
    batch = []
    tcounts = collections.Counter()
    seen_sha = set()
    if t == "chunks":
        seen_sha = {r[0] for r in con.execute("select sha256 from chunks where sha256 is not null")}
    if t == "payloads":
        seen_sha = {r[0] for r in con.execute("select sha256 from payloads where sha256 is not null")}

    for row in rows:
        rid = row[0]
        vals = list(row[1:])
        new_vals = []
        row_changed = False
        for c, v in zip(text_cols, vals):
            nv, counts = scrub(v)
            if counts and nv != v:
                row_changed = True
                tcounts.update(counts)
            new_vals.append(nv)
        if row_changed:
            changed += 1
            # keep content hashes consistent where they exist
            if t == "chunks" and "sha256" in [c[0] for c in cols]:
                idx = text_cols.index("text") if "text" in text_cols else None
                if idx is not None and new_vals[idx] is not None:
                    h = hashlib.sha256(new_vals[idx].encode("utf-8", "ignore")).hexdigest()
                    if h not in seen_sha:
                        seen_sha.add(h)
                        batch.append(("sha256", h, rid))
            if t == "payloads" and "payload" in text_cols:
                idx = text_cols.index("payload")
                if new_vals[idx] is not None:
                    h = hashlib.sha256(new_vals[idx].encode("utf-8", "ignore")).hexdigest()
                    if h not in seen_sha:
                        seen_sha.add(h)
                        batch.append(("sha256", h, rid))
            sets = ", ".join(f'"{c}"=?' for c in text_cols)
            batch.append(("row", [*new_vals, rid], sets))
        if len(batch) >= 400:
            _flush(con, t, text_cols, batch)
            batch = []
    if batch:
        _flush(con, t, text_cols, batch)
    con.commit()
    totals.update(tcounts)
    report[t] = {"rows": len(rows), "changed": changed, "counts": dict(tcounts)}
    print(f"{t:16s} rows={len(rows):6d} changed={changed:6d} {dict(tcounts)}  [{time.time()-t0:.0f}s]")

# rebuild FTS from the (now sanitized) content tables
for fts in ("chunks_fts", "documents_fts"):
    try:
        con.execute(f"INSERT INTO {fts}({fts}) VALUES('rebuild')")
        con.commit()
        print(f"rebuilt {fts}")
    except sqlite3.Error as e:
        print(f"FTS rebuild {fts} failed: {e}")

con.execute("PRAGMA optimize")
con.commit()
con.close()

json.dump({"db": DB, "totals": totals, "tables": report,
           "seconds": round(time.time() - t0, 1)}, open(OUT, "w"), indent=1)
print("TOTAL", dict(totals), f"{time.time()-t0:.0f}s")
