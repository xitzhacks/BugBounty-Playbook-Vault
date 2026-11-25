#!/usr/bin/env python3
"""Build the retrieval layer over the report library: section-aware chunks + embeddings.

Stores in _VAULT/reports.sqlite:
  chunks(id, kind, report_id, path, heading, text, chars, sha256, model, dim, vec BLOB)
  chunks_fts (FTS5 over heading+text)

Embeddings: fastembed (ONNX, CPU). Default all-MiniLM-L6-v2 (384-dim, ~15 chunks/s here).
Swap models with EMBED_MODEL=... ; rows record which model built them, so a re-embed is a
filtered rebuild, never a silent mix. Resumable: sha256 + model key skips finished work.
"""
import hashlib, os, sqlite3, struct, sys, time

VAULT = os.environ.get("VAULT_ROOT", os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "vault"))
DB = os.path.join(VAULT, "_VAULT", "reports.sqlite")
MODEL = os.environ.get("EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
MAXC = int(os.environ.get("CHUNK_CHARS", "2400"))
MINC = int(os.environ.get("MIN_CHARS", "300"))
BATCH = int(os.environ.get("BATCH", "64"))

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
CREATE INDEX IF NOT EXISTS chunks_model ON chunks(model);
CREATE VIRTUAL TABLE IF NOT EXISTS chunks_fts USING fts5(heading, text, content='chunks', content_rowid='id', tokenize='porter unicode61');
CREATE TRIGGER IF NOT EXISTS chunks_ai AFTER INSERT ON chunks BEGIN
  INSERT INTO chunks_fts(rowid,heading,text) VALUES (new.id,new.heading,new.text); END;
CREATE TRIGGER IF NOT EXISTS chunks_ad AFTER DELETE ON chunks BEGIN
  INSERT INTO chunks_fts(chunks_fts,rowid,heading,text) VALUES ('delete',old.id,old.heading,old.text); END;
"""

def split_md(text, maxc=MAXC, minc=MINC):
    """Section-aware split: headings open a section, oversized sections split on blank lines."""
    out, cur, head = [], [], ""
    def flush():
        nonlocal cur, head
        body = "\n".join(cur).strip()
        if len(body) >= minc:
            while len(body) > maxc:
                cut = body.rfind("\n\n", 0, maxc)
                if cut < minc: cut = body.rfind("\n", 0, maxc)
                if cut < minc: cut = maxc
                out.append((head, body[:cut].strip()))
                body = body[cut:].strip()
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
    covered = {w[1] for w in work if w[0] == "report"}
    backfill = 0
    for rid, body, summary, title in con.execute(
            "SELECT id, body, summary, title FROM bodies WHERE length(COALESCE(body,''))>0"):
        if rid in covered: continue
        txt = (body or "").strip()
        if len(txt) < 40: continue
        work.append(("report", rid, None, title or "", txt[:2400]))
        backfill += 1
    if backfill: print(f"backfill chunks for short-body reports: {backfill}", flush=True)
    doc_covered = set()
    for path, text in con.execute("SELECT path, text FROM documents"):
        made = split_md(text)
        for h, t in made:
            work.append(("doc", None, path, h, t))
        if made: doc_covered.add(path)
    doc_backfill = 0
    for path, text in con.execute("SELECT path, text FROM documents"):
        if path in doc_covered: continue
        t = (text or "").strip()
        if len(t) < 40: continue
        work.append(("doc", None, path, os.path.splitext(os.path.basename(path))[0], t[:2400]))
        doc_backfill += 1
    if doc_backfill: print(f"backfill chunks for short docs: {doc_backfill}", flush=True)
    con.execute("CREATE TABLE IF NOT EXISTS chunk_tombstones(sha256 TEXT PRIMARY KEY, kind TEXT, path TEXT, removed_at TEXT)")
    dead = {r[0] for r in con.execute("SELECT sha256 FROM chunk_tombstones")}
    todo = [w for w in work
            if (hashlib.sha256(w[4].encode()).hexdigest(), MODEL) not in have
            and hashlib.sha256(w[4].encode()).hexdigest() not in dead]
    print(f"chunks total={len(work)} already={len(work)-len(todo)} todo={len(todo)} model={MODEL}", flush=True)
    if not todo:
        print("nothing to do"); return
    if os.environ.get("NO_EMBED") == "1":
        ins = ("INSERT OR IGNORE INTO chunks(kind,report_id,path,heading,text,chars,sha256,model,dim,vec,built_at) "
               "VALUES (?,?,?,?,?,?,?,'',0,NULL,?)")
        now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        rows = [(k, rid, p, h, t, len(t), hashlib.sha256(t.encode()).hexdigest(), now) for (k, rid, p, h, t) in todo]
        con.executemany(ins, rows); con.commit()
        print(f"chunked only (NO_EMBED=1): {len(rows)} chunks inserted, no vectors")
        return
    from fastembed import TextEmbedding
    model = TextEmbedding(model_name=MODEL, threads=os.cpu_count() or 4)
    ins = ("INSERT OR IGNORE INTO chunks(kind,report_id,path,heading,text,chars,sha256,model,dim,vec,built_at) "
           "VALUES (?,?,?,?,?,?,?,?,?,?,?)")
    done = 0; t0 = time.time()
    for i in range(0, len(todo), BATCH):
        batch = todo[i:i+BATCH]
        vecs = list(model.embed([b[4][:4000] for b in batch], batch_size=BATCH))
        now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        rows = [(k, rid, p, h, t, len(t), hashlib.sha256(t.encode()).hexdigest(), MODEL, len(v),
                 struct.pack(f"{len(v)}f", *v), now) for (k, rid, p, h, t), v in zip(batch, vecs)]
        con.executemany(ins, rows); con.commit()
        done += len(rows)
        if done % 640 == 0 or done == len(todo):
            el = time.time() - t0
            print(f"embedded {done}/{len(todo)}  {done/el:.1f}/s  eta {(len(todo)-done)/max(0.1,done/el)/60:.0f} min", flush=True)
    n = con.execute("SELECT COUNT(*) FROM chunks WHERE vec IS NOT NULL").fetchone()[0]
    print(f"DONE chunks with vectors={n}", flush=True)

main()
