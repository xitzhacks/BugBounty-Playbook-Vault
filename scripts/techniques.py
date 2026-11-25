#!/usr/bin/env python3
"""Technique index CLI — answers "what named techniques exist for this class?".

  python3 techniques.py LFI
  python3 techniques.py SQLI --grep union
  python3 techniques.py --all | head -40

This is the layer DVWA pass 3 exposed as missing: the index could find "php filter chain" but a class
query ("file inclusion") returned frontmatter. Now the class query returns the technique names, each
pointing at the chunk that holds the how-to.
"""
import argparse, os, sqlite3, textwrap

DB = os.environ.get("VAULT_DB", os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "vault", "_VAULT", "reports.sqlite"))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cls", nargs="?")
    ap.add_argument("--grep", help="substring filter on technique name")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--show", type=int, metavar="CHUNK", help="print the chunk text for a chunk id")
    ap.add_argument("--k", type=int, default=40)
    a = ap.parse_args()
    con = sqlite3.connect(DB); con.row_factory = sqlite3.Row

    if a.show:
        r = con.execute("""SELECT c.heading, c.text, c.path FROM chunks c WHERE c.id=?""", (a.show,)).fetchone()
        if not r: print("no chunk", a.show); return
        print(f"# {r['heading']}\n# source: {r['path']}\n")
        print(r["text"][:4000])
        return

    where, args = [], []
    if a.cls: where.append("upper(cls)=upper(?)"); args.append(a.cls)
    if a.grep: where.append("lower(name) LIKE ?"); args.append(f"%{a.grep.lower()}%")
    sql = "SELECT cls,name,path,chunk_id,confidence FROM techniques"
    if where: sql += " WHERE " + " AND ".join(where)
    sql += " ORDER BY cls, CASE confidence WHEN 'path' THEN 0 ELSE 1 END, length(name) DESC LIMIT ?"
    rows = con.execute(sql, args + [a.k]).fetchall()
    cur = None
    for r in rows:
        if r["cls"] != cur:
            cur = r["cls"]; print(f"\n== {cur} ==")
        print(f"  {r['name'][:88]}")
        if r["path"]: print(f"     └ {r['path']}  (chunk {r['chunk_id']})")
    if not rows: print("no techniques matched")

if __name__ == "__main__":
    main()
