#!/usr/bin/env python3
"""Chunk + embed a report corpus into <DB> (SQLite). Resumable, incremental, model-tagged.

Usage:
  EMBED_MODEL=sentence-transformers/all-MiniLM-L6-v2 CHUNK_CHARS=2400 \
      python3 build_rag.py /path/to/reports.sqlite

Schema created (idempotent):
  chunks(...)  + chunks_fts (FTS5)
Expects tables: bodies(id,body,summary,title) and optionally documents(path,text).
Requires: pip install fastembed  (ONNX, CPU-friendly; ~15 chunks/s for MiniLM on 8 cores)
"""
import hashlib, os, sqlite3, struct, sys, time

DB = sys.argv[1] if len(sys.argv) > 1 else "reports.sqlite"
MODEL = os.environ.get("EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
MAXC = int(os.environ.get("CHUNK_CHARS", "2400"))
MINC = int(os.environ.get("MIN_CHARS", "300"))
BATCH = int(os.environ.get("BATCH", "64"))

SCHEMA = """
CREATE TABLE IF NOT EXISTS chunks(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  kind TEXT NOT NULL, report_id INTEGER, path TEXT, heading TEXT,
  text TEXT NOT NULL, chars INTEGER, sha256 TEXT,
  model TEXT, dim INTEGER, vec BLOB, built_at TEXT,
  UNIQUE(kind, report_id, path, sha256));
CREATE INDEX IF NOT EXISTS chunks_report ON chunks(report_id);
CREATE VIRTUAL TABLE IF NOT EXISTS chunks_fts USING fts5(heading, text, content='chunks',
  content_rowid='id', tokenize='porter unicode61');
CREATE TRIGGER IF NOT EXISTS chunks_ai AFTER INSERT ON chunks BEGIN
  INSERT INTO chunks_fts(rowid,heading,text) VALUES (new.id,new.heading,new.text); END;
CREATE TRIGGER IF NOT EXISTS chunks_ad AFTER DELETE ON chunks BEGIN
  INSERT INTO chunks_fts(chunks_fts,rowid,heading,text) VALUES ('delete',old.id,old.heading,old.text); END;
"""

def split_md(text, maxc=MAXC, minc=MINC):
    """Headings open a section; oversized sections split on blank lines. Code blocks stay intact."""
    out, cur, head = [], [], ""
    def flush():
        nonlocal cur, head
        body = "\n".join(cur).strip()
        if len(body) >= minc:
            while len(body) > maxc:
                cut = body.rfind("\n\n", 0, maxc)
                if cut < minc: cut = body.rfind("\n", 0, maxc)
                if cut < minc: cut = maxc
                out.append((head, body[:cut].strip())); body = body[cut:].strip()
            if body: out.append((head, body))
        cur = []
    for ln in text.splitlines():
        if ln.startswith("#"):
            flush(); head = ln.lstrip("#").strip()[:120]; cur = [ln]
        else:
            cur.append(ln)
    flush()
    return out

def main():
    con = sqlite3.connect(DB, timeout=180)
    con.executescript(SCHEMA); con.commit()
    have = {(r[0], r[1]) for r in con.execute("SELECT sha256, model FROM chunks WHERE vec IS NOT NULL")}
    work = []
    for rid, body, summary, title in con.execute(
            "SELECT id, body, summary, title FROM bodies WHERE length(COALESCE(body,''))>0"):
        txt = body or ""
        if summary and summary[:200] not in txt[:500]:
            txt = f"{summary}\n\n{txt}"
        for h, t in split_md(txt):
            work.append(("report", rid, None, h or (title or ""), t))

    # BACKFILL: a body that produced no chunk must still be reachable (short/stub write-ups)
    covered = {w[1] for w in work if w[0] == "report"}
    back = 0
    for rid, body, summary, title in con.execute(
            "SELECT id, body, summary, title FROM bodies WHERE length(COALESCE(body,''))>0"):
        if rid in covered: continue
        txt = (body or "").strip()
        if len(txt) < 40: continue
        work.append(("report", rid, None, title or "", txt[:2400])); back += 1
    print(f"backfill chunks for short-body reports: {back}", flush=True)

    try:
        for path, text in con.execute("SELECT path, text FROM documents"):
            for h, t in split_md(text):
                work.append(("doc", None, path, h, t))
    except sqlite3.OperationalError:
        pass  # no documents table in this corpus

    todo = [w for w in work if (hashlib.sha256(w[4].encode()).hexdigest(), MODEL) not in have]
    print(f"chunks total={len(work)} already={len(work)-len(todo)} todo={len(todo)} model={MODEL}", flush=True)
    if not todo: return

    from fastembed import TextEmbedding
    model = TextEmbedding(model_name=MODEL, threads=os.cpu_count() or 4)
    ins = ("INSERT OR IGNORE INTO chunks(kind,report_id,path,heading,text,chars,sha256,model,dim,vec,built_at)"
           " VALUES (?,?,?,?,?,?,?,?,?,?,?)")
    done, t0 = 0, time.time()
    for i in range(0, len(todo), BATCH):
        batch = todo[i:i+BATCH]
        vecs = list(model.embed([b[4][:4000] for b in batch], batch_size=BATCH))
        now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        rows = [(k, rid, p, h, t, len(t), hashlib.sha256(t.encode()).hexdigest(), MODEL,
                 len(v), struct.pack(f"{len(v)}f", *v), now)
                for (k, rid, p, h, t), v in zip(batch, vecs)]
        con.executemany(ins, rows); con.commit(); done += len(rows)
        if done % 640 == 0 or done == len(todo):
            el = time.time() - t0
            print(f"embedded {done}/{len(todo)}  {done/el:.1f}/s  eta "
                  f"{(len(todo)-done)/max(0.1, done/el)/60:.0f} min", flush=True)
    print("DONE chunks with vectors=%d" % con.execute(
        "SELECT COUNT(*) FROM chunks WHERE vec IS NOT NULL").fetchone()[0], flush=True)

main()
