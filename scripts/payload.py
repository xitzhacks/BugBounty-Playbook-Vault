#!/usr/bin/env python3
"""Payload table CLI — copy-ready strings that someone actually used.

  python3 payload.py                    # census
  python3 payload.py XSS --grep svg     # payloads for a class containing 'svg'
  python3 payload.py SQLI --show 42     # print one payload with its source
"""
import argparse, os, sqlite3

DB = os.environ.get("VAULT_DB", os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "vault", "_VAULT", "reports.sqlite"))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cls", nargs="?")
    ap.add_argument("--grep")
    ap.add_argument("--show", type=int)
    ap.add_argument("--k", "-k", type=int, default=10)
    ap.add_argument("--kind", choices=["report", "skill", "playbook"])
    a = ap.parse_args()
    con = sqlite3.connect(DB); con.row_factory = sqlite3.Row

    if a.show:
        r = con.execute("SELECT * FROM payloads WHERE id=?", (a.show,)).fetchone()
        if not r: print("no payload", a.show); return
        print(f"class={r['cls']} kind={r['kind']} lang={r['lang'] or '-'} chars={r['chars']}")
        print(f"source: https://hackerone.com/reports/{r['report_id']}" if r["report_id"] else f"source: {r['path']} § {r['context']}")
        print("\n" + r["payload"])
        return

    if not a.cls:
        print(f"{'class':9} {'rows':>6}")
        for c, n in con.execute("SELECT cls, COUNT(*) FROM payloads GROUP BY 1 ORDER BY 2 DESC"):
            print(f"{c:9} {n:6d}")
        print("\nusage: python3 payload.py XSS --grep svg")
        return

    where, args = ["upper(cls)=upper(?)"], [a.cls]
    if a.grep:
        where.append("(lower(payload) LIKE ? OR lower(context) LIKE ?)")
        args += [f"%{a.grep.lower()}%", f"%{a.grep.lower()}%"]
    if a.kind:
        where.append("kind=?"); args.append(a.kind)
    rows = con.execute(f"""SELECT * FROM payloads WHERE {' AND '.join(where)}
                           ORDER BY score DESC, chars ASC LIMIT ?""", args + [a.k]).fetchall()
    if not rows: print("nothing matched"); return
    for r in rows:
        one = r["payload"].replace("\n", " ⏎ ")
        src = f"#{r['report_id']}" if r["report_id"] else (r["path"] or "")[-46:]
        print(f"[{r['id']}] {r['cls']:<8} {r['lang'] or '-':<8} {one[:150]}   ← {src}")
    print(f"\npython3 payload.py {a.cls} --show <id>  for the full string")

if __name__ == "__main__":
    main()
