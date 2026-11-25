#!/usr/bin/env python3
"""Mirror every skill into the vault and index its markdown in the same DB.

- Source: ~/.hermes/profiles/batman/skills (this profile's skills only)
- Skips: .hub, .curator_backups, .git and other hidden dirs (those are caches/backups, not skills)
- Copies .md + scripts/templates/references into Vault/_VAULT/skills/<skill>/...
- Indexes each .md as a row in `documents` (dir='skills'), so the existing chunker/embedder picks it up
- Dedupe: identical markdown (sha256) is stored once; the copy is recorded as a duplicate pointer
"""
import hashlib, os, shutil, sqlite3, time

SRC = os.path.expanduser("~/.hermes/profiles/batman/skills")
VAULT = os.environ.get("VAULT_ROOT", os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "vault"))
DST = os.path.join(VAULT, "_VAULT", "skills")
DB = os.path.join(VAULT, "_VAULT", "reports.sqlite")
EXTS = (".md", ".py", ".sh", ".yml", ".yaml", ".json", ".txt")
SKIP = {".hub", ".curator_backups", ".git", ".commandcode", "node_modules", "__pycache__"}

def front(text):
    if not text.startswith("---"): return {}
    try:
        head = text.split("---", 2)[1]
    except IndexError:
        return {}
    out = {}
    for line in head.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            out[k.strip().lower()] = v.strip().strip('"').strip("'")
    return out

def main():
    con = sqlite3.connect(DB)
    con.execute("""CREATE TABLE IF NOT EXISTS skill_dupes(
        path TEXT PRIMARY KEY, canonical TEXT NOT NULL, sha256 TEXT NOT NULL)""")
    if os.path.isdir(DST): shutil.rmtree(DST)
    os.makedirs(DST, exist_ok=True)

    seen_sha, copied, dupes, rows = {}, 0, 0, 0
    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    for root, dirs, files in os.walk(SRC):
        dirs[:] = [d for d in dirs if d not in SKIP and not d.startswith(".")]
        for fn in files:
            if not fn.lower().endswith(EXTS): continue
            src = os.path.join(root, fn)
            rel = os.path.relpath(src, SRC)                 # e.g. hunt-xss/SKILL.md
            try:
                raw = open(src, "rb").read()
            except Exception:
                continue
            sha = hashlib.sha256(raw).hexdigest()
            # mirror the file (scripts included, so the vault is self-contained)
            out = os.path.join(DST, rel)
            os.makedirs(os.path.dirname(out), exist_ok=True)
            open(out, "wb").write(raw)
            copied += 1
            if not fn.lower().endswith(".md"): continue

            text = raw.decode("utf-8", errors="replace")
            if sha in seen_sha:
                dupes += 1
                con.execute("INSERT OR REPLACE INTO skill_dupes(path,canonical,sha256) VALUES (?,?,?)",
                            (f"skills/{rel}", seen_sha[sha], sha))
                continue                      # identical content already indexed
            seen_sha[sha] = f"skills/{rel}"
            fm = front(text)
            con.execute("""INSERT INTO documents(path,dir,name,title,type,category,cwe,bytes,lines,sha256,ingested_at,text)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
                ON CONFLICT(path) DO UPDATE SET dir=excluded.dir,name=excluded.name,title=excluded.title,
                  type=excluded.type,category=excluded.category,cwe=excluded.cwe,bytes=excluded.bytes,
                  lines=excluded.lines,sha256=excluded.sha256,ingested_at=excluded.ingested_at,text=excluded.text""",
                (f"skills/{rel}", "skills", fn, fm.get("title") or os.path.splitext(fn)[0],
                 fm.get("type") or ("skill" if fn == "SKILL.md" else "reference"),
                 fm.get("category") or rel.split(os.sep)[0], fm.get("cwe"),
                 len(raw), text.count("\n") + 1, sha, now, text))
            rows += 1
    con.commit()
    n_skills = len({p.split(os.sep)[0] for p in seen_sha.values()})
    print(f"mirrored {copied} files, indexed {rows} markdown docs from {n_skills} skills, {dupes} duplicate docs skipped")
    print("vault copy:", DST)

main()
