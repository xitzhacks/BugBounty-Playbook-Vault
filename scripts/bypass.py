#!/usr/bin/env python3
"""Bypass index CLI — "someone hit this protection before; here is the passage and the payload".

  python3 bypass.py                        # census of protections
  python3 bypass.py waf --grep cloudflare  # filter within a tag
  python3 bypass.py csp --show 42          # full passage + payloads for one row
"""
import argparse, os, sqlite3

DB = os.environ.get("VAULT_DB", os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "vault", "_VAULT", "reports.sqlite"))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tag", nargs="?")
    ap.add_argument("--grep")
    ap.add_argument("--show", type=int)
    ap.add_argument("--k", "-k", type=int, default=8)
    ap.add_argument("--min-score", type=int, default=3)
    a = ap.parse_args()
    con = sqlite3.connect(DB); con.row_factory = sqlite3.Row

    if a.show:
        r = con.execute("SELECT * FROM bypasses WHERE id=?", (a.show,)).fetchone()
        if not r: print("no row", a.show); return
        print(f"tag={r['tag']} kind={r['kind']} confidence={r['confidence']}")
        if r["report_id"]: print(f"report: https://hackerone.com/reports/{r['report_id']}  {r['title']} ({r['program']})")
        if r["path"]: print(f"source: {r['path']} § {r['title'] or ''}")
        print("\n--- passage ---\n" + (r["passage"] or ""))
        print("\n--- payloads ---\n" + (r["payloads"] or "(none captured)"))
        return

    if not a.tag:
        print(f"{'tag':12} {'rows':>6} {'payload':>8}")
        for t, n, c in con.execute("""SELECT tag, COUNT(*), SUM(score>=3) FROM bypasses
                                      GROUP BY 1 ORDER BY 2 DESC"""):
            print(f"{t:12} {n:6d} {c or 0:13d}")
        print("\nusage: python3 bypass.py waf --grep cloudflare")
        return

    where, args = ["tag=?", "score>=?"], [a.tag, a.min_score]
    if a.grep:
        where.append("(lower(passage) LIKE ? OR lower(payloads) LIKE ?)")
        args += [f"%{a.grep.lower()}%", f"%{a.grep.lower()}%"]
    rows = con.execute(f"""SELECT * FROM bypasses WHERE {' AND '.join(where)}
                           ORDER BY score DESC, CASE confidence WHEN 'code' THEN 0 ELSE 1 END, id LIMIT ?""",
                       args + [a.k]).fetchall()
    if not rows: print("nothing for", a.tag); return
    for r in rows:
        head = (f"#{r['report_id']} {r['title'][:70]} ({r['program']})" if r["report_id"]
                else f"{r['path']} § {r['title'] or ''}")
        print(f"\n[{r['id']}] {head}   [{r['confidence']}]")
        p = (r["passage"] or "").replace("\n", " ")
        print("    " + p[:300])
        if r["payloads"]:
            print("    payload: " + r["payloads"].split("\n---\n")[0][:200].replace("\n", " | "))
    print("\npython3 bypass.py " + a.tag + " --show <id>  for the full passage")

if __name__ == "__main__":
    main()
