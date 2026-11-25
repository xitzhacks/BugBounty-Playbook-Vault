#!/usr/bin/env python3
"""Index every markdown document in the Vault into the vault DB.

Adds table `documents` (+ FTS5 `documents_fts`) holding the full text of every .md we wrote:
playbook modules, agent playbooks, READMEs, case registers, class/category views.
Idempotent: rows are upserted by path; docs deleted from disk are removed from the index.
"""
import hashlib, os, re, sqlite3, time

VAULT = os.environ.get("VAULT_ROOT", os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "vault"))
DB = os.path.join(VAULT, "_VAULT", "reports.sqlite")

SCHEMA = """
CREATE TABLE IF NOT EXISTS documents(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  path TEXT UNIQUE NOT NULL,   -- vault-relative, e.g. "XSS/Reflected-XSS.md"
  dir  TEXT NOT NULL,          -- top-level vault dir, e.g. "XSS"
  name TEXT NOT NULL,          -- file name
  title TEXT, type TEXT, category TEXT, cwe TEXT,
  bytes INTEGER, lines INTEGER, sha256 TEXT,
  ingested_at TEXT NOT NULL,
  text TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS documents_dir ON documents(dir);
CREATE INDEX IF NOT EXISTS documents_type ON documents(type);
CREATE VIRTUAL TABLE IF NOT EXISTS documents_fts USING fts5(
  title, name, path, dir, text, content='documents', content_rowid='id', tokenize='porter unicode61'
);
CREATE TRIGGER IF NOT EXISTS documents_fts_ai AFTER INSERT ON documents BEGIN
  INSERT INTO documents_fts(rowid,title,name,path,dir,text) VALUES (new.id,new.title,new.name,new.path,new.dir,new.text);
END;
CREATE TRIGGER IF NOT EXISTS documents_fts_ad AFTER DELETE ON documents BEGIN
  INSERT INTO documents_fts(documents_fts,rowid,title,name,path,dir,text) VALUES ('delete',old.id,old.title,old.name,old.path,old.dir,old.text);
END;
CREATE TRIGGER IF NOT EXISTS documents_fts_au AFTER UPDATE OF title,name,path,dir,text ON documents BEGIN
  INSERT INTO documents_fts(documents_fts,rowid,title,name,path,dir,text) VALUES ('delete',old.id,old.title,old.name,old.path,old.dir,old.text);
  INSERT INTO documents_fts(rowid,title,name,path,dir,text) VALUES (new.id,new.title,new.name,new.path,new.dir,new.text);
END;
"""

def front(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m: return {}
    out = {}
    for line in m.group(1).splitlines():
        if ":" not in line: continue
        k, v = line.split(":", 1)
        out[k.strip().lower()] = v.strip().strip('"').strip("'")
    return out

def main():
    con = sqlite3.connect(DB)
    con.executescript(SCHEMA)
    seen = set()
    files = []
    for dp, dns, fns in os.walk(VAULT):
        dns[:] = [d for d in dns if not d.startswith(".") and d not in ("node_modules",)]
        if os.path.relpath(dp, VAULT).startswith(os.path.join("_VAULT", "skills")): continue
        for fn in fns:
            if fn.lower().endswith(".md"):
                files.append(os.path.join(dp, fn))
    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    for p in sorted(files):
        rel = os.path.relpath(p, VAULT)
        if rel.startswith("_VAULT/reports.sqlite"): continue
        if rel.startswith(os.path.join("_VAULT", "skills")): continue   # owned by ingest_skills.py
        try:
            raw = open(p, "rb").read()
            text = raw.decode("utf-8", errors="replace")
        except Exception as e:
            print("skip", rel, e); continue
        fm = front(text)
        top = rel.split(os.sep)[0] if os.sep in rel else "_root"
        con.execute("""INSERT INTO documents(path,dir,name,title,type,category,cwe,bytes,lines,sha256,ingested_at,text)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
            ON CONFLICT(path) DO UPDATE SET dir=excluded.dir,name=excluded.name,title=excluded.title,
              type=excluded.type,category=excluded.category,cwe=excluded.cwe,bytes=excluded.bytes,
              lines=excluded.lines,sha256=excluded.sha256,ingested_at=excluded.ingested_at,text=excluded.text""",
            (rel, top, os.path.basename(rel), fm.get("title") or os.path.splitext(os.path.basename(rel))[0],
             fm.get("type"), fm.get("category"), fm.get("cwe"), len(raw), text.count("\n") + 1,
             hashlib.sha256(raw).hexdigest(), now, text))
        seen.add(rel)
    # drop rows whose file no longer exists
    # skills/ rows are owned by ingest_skills.py — never treat them as stale here
    stale = [r[0] for r in con.execute("SELECT path FROM documents")
             if r[0] not in seen and not r[0].startswith("skills/")]
    for s in stale:
        con.execute("DELETE FROM documents WHERE path=?", (s,))
    con.commit()
    n = con.execute("SELECT COUNT(*) FROM documents").fetchone()[0]
    d = con.execute("SELECT COUNT(DISTINCT dir) FROM documents").fetchone()[0]
    b = con.execute("SELECT SUM(bytes) FROM documents").fetchone()[0]
    print(f"indexed {n} markdown documents across {d} vault dirs ({b:,} bytes) · removed {len(stale)} stale")
    for d_, c in con.execute("SELECT dir, COUNT(*) FROM documents GROUP BY 1 ORDER BY 2 DESC"):
        print(f"  {c:4d}  {d_}")

main()
