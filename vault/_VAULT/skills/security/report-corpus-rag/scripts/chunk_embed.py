#!/usr/bin/env python3
"""Section-aware chunker + fastembed embedder for a report corpus.

Generic version of the pipeline that built a 28k-chunk index over 9,875 write-ups.
Run inside a venv with fastembed installed (see references/embedding-throughput-and-hardware.md).

  python3 chunk_embed.py --db /path/corpus.sqlite
  EMBED_MODEL=BAAI/bge-small-en-v1.5 python3 chunk_embed.py --db ...

Expected source tables (adapt the two SELECTs at the bottom of load_work if your schema differs):
  bodies(id, title, body, summary)      -- write-ups
  documents(path, text)                 -- our own markdown
"""
import argparse, hashlib, os, sqlite3, struct, time

SCHEMA = """
CREATE TABLE IF NOT EXISTS chunks(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  kind TEXT NOT NULL,            -- 'report' | 'doc'
  report_id INTEGER,
  path TEXT,
  heading TEXT,
  text TEXT NOT NULL,
  chars INTEGER,
  sha256 TEXT,
  model TEXT, dim INTEGER, vec BLOB,
  built_at TEXT,
  UNIQUE(kind, report_id, path, sha256)
);
CREATE INDEX IF NOT EXISTS chunks_report ON chunks(report_id);
CREATE VIRTUAL TABLE IF NOT EXISTS chunks_fts USING fts5(heading, text, content='chunks', content_rowid='id', tokenize='porter unicode61');
CREATE TRIGGER IF NOT EXISTS chunks_ai AFTER INSERT ON chunks BEGIN
  INSERT INTO chunks_fts(rowid,heading,text) VALUES (new.id,new.heading,new.text); END;
CREATE TRIGGER IF NOT EXISTS chunks_ad AFTER DELETE ON chunks BEGIN
  INSERT INTO chunks_fts(chunks_fts,rowid,heading,text) VALUES ('delete',old.id,old.heading,old.text); END;
"""

def split_md(text, maxc=2400, minc=300):
    """Headings open a section; oversized sections split on blank lines. Never cut mid-fence."""
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

def load_work(con):
    work = []
    for rid, title, body, summary in con.execute(
            "SELECT id, title, COALESCE(body,''), COALESCE(summary,'') FROM bodies WHERE length(COALESCE(body,''))>0"):
        txt = f"{summary}\n\n{body}" if summary and summary[:200] not in body[:500] else body
        for h, t in split_md(txt):
            work.append(("report", rid, None, h or title or "", t))
    covered = {w[1] for w in work}
    for rid, title, body in con.execute(
            "SELECT id, title, COALESCE(body,'') FROM bodies WHERE length(COALESCE(body,''))>0"):
        if rid not in covered and len(body.strip()) >= 40:          # backfill short reports
            work.append(("report", rid, None, title or "", body.strip()[:2400]))
    for path, text in con.execute("SELECT path, text FROM documents"):
        for h, t in split_md(text):
            work.append(("doc", None, path, h, t))
    return work

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", required=True)
    ap.add_argument("--batch", type=int, default=64)
    a = ap.parse_args()
    model_name = os.environ.get("EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

    con = sqlite3.connect(a.db, timeout=180)
    con.executescript(SCHEMA); con.commit()
    have = {(s, m) for s, m in con.execute("SELECT sha256, model FROM chunks WHERE vec IS NOT NULL")}
    work = load_work(con)
    todo = [w for w in work if (hashlib.sha256(w[4].encode()).hexdigest(), model_name) not in have]
    print(f"chunks total={len(work)} done={len(work)-len(todo)} todo={len(todo)} model={model_name}", flush=True)
    if not todo: return

    from fastembed import TextEmbedding
    model = TextEmbedding(model_name=model_name, threads=os.cpu_count() or 4)
    ins = ("INSERT OR IGNORE INTO chunks(kind,report_id,path,heading,text,chars,sha256,model,dim,vec,built_at) "
           "VALUES (?,?,?,?,?,?,?,?,?,?,?)")
    t0, done = time.time(), 0
    for i in range(0, len(todo), a.batch):
        batch = todo[i:i+a.batch]
        vecs = list(model.embed([b[4][:4000] for b in batch], batch_size=a.batch))
        now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        rows = [(k, rid, p, h, t, len(t), hashlib.sha256(t.encode()).hexdigest(), model_name, len(v),
                 struct.pack(f"{len(v)}f", *v), now) for (k, rid, p, h, t), v in zip(batch, vecs)]
        con.executemany(ins, rows); con.commit()
        done += len(rows)
        if done % 640 == 0 or done == len(todo):
            rate = done / (time.time() - t0)
            print(f"{done}/{len(todo)}  {rate:.1f}/s  eta {(len(todo)-done)/max(.1,rate)/60:.0f} min", flush=True)
    n = con.execute("SELECT COUNT(*) FROM chunks WHERE vec IS NOT NULL").fetchone()[0]
    print(f"DONE vectors={n}")

if __name__ == "__main__":
    main()
