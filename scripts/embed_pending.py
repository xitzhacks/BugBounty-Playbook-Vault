#!/usr/bin/env python3
"""Embed chunks that exist without vectors (vec IS NULL), by id.

build_rag's INSERT OR IGNORE silently skips a row whose (kind,path,sha) already exists,
which leaves pre-inserted chunks permanently vectorless. This fills exactly those rows.
"""
import os, sqlite3, struct, time

DB = os.environ.get("VAULT_DB", os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "vault", "_VAULT", "reports.sqlite"))
MODEL = os.environ.get("EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
BATCH = 64

def main():
    con = sqlite3.connect(DB, timeout=180)
    todo = con.execute("SELECT id, text FROM chunks WHERE vec IS NULL").fetchall()
    print(f"pending chunks: {len(todo)}", flush=True)
    if not todo: return
    from fastembed import TextEmbedding
    model = TextEmbedding(model_name=MODEL, threads=os.cpu_count() or 4)
    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    done = 0; t0 = time.time()
    for i in range(0, len(todo), BATCH):
        batch = todo[i:i+BATCH]
        vecs = list(model.embed([t[:4000] for _, t in batch], batch_size=BATCH))
        rows = [(struct.pack(f"{len(v)}f", *v), MODEL, len(v), now, cid)
                for (cid, _), v in zip(batch, vecs)]
        con.executemany("UPDATE chunks SET vec=?, model=?, dim=?, built_at=? WHERE id=?", rows)
        con.commit(); done += len(rows)
        if done % 640 == 0 or done == len(todo):
            el = time.time() - t0
            print(f"updated {done}/{len(todo)} {done/el:.1f}/s eta {(len(todo)-done)/max(0.1,done/el)/60:.0f} min", flush=True)
    n = con.execute("SELECT COUNT(*) FROM chunks WHERE vec IS NOT NULL").fetchone()[0]
    print(f"DONE. chunks with vectors: {n}")

main()
