#!/usr/bin/env python3
"""Retrieval smoke test: for N random reports with a real body, build a query from the report's
own title (a few content words) and check whether that report comes back in the top-k.
Honest label: title-derived queries, not hand-written operator questions. It measures whether the
index can find a known document at all — a floor, not the ceiling. N defaults to 20 (override as
the first argument); the earlier title-derived eval used 15 queries.
"""
import json, random, re, sqlite3, subprocess, os, sys, time

DB = os.environ.get("VAULT_DB", os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "vault", "_VAULT", "reports.sqlite"))
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PY = os.path.join(ROOT, ".venv", "bin", "python")
if not os.path.exists(PY):
    PY = sys.executable
N = int(sys.argv[1]) if len(sys.argv) > 1 else 20
K = 10
STOP = set("the a an and or of to in on for with via from at by is are be as it this that how my your our".split())

con = sqlite3.connect(DB); con.row_factory = sqlite3.Row
pool = con.execute("""SELECT id,title,program,weakness,bounty FROM reports
    WHERE id IN (SELECT id FROM bodies WHERE length(COALESCE(body,''))>1500)""").fetchall()
random.seed(7)
sample = random.sample(pool, N)

def query_from(title):
    words = [w for w in re.findall(r"[A-Za-z0-9]{3,}", title.lower()) if w not in STOP]
    return " ".join(words[:7])

hits1 = hits5 = hits10 = 0
rows = []
t0 = time.time()
for r in sample:
    q = query_from(r["title"])
    p = subprocess.run([PY, os.path.join(HERE, "search.py"),
                        q, "-k", str(K), "--json"], capture_output=True, text=True, timeout=180)
    try:
        out = json.loads(p.stdout)
    except Exception:
        rows.append((r["id"], "ERR", 0)); continue
    ids = [h["report_id"] for h in out["hits"] if h["kind"] == "report"]
    rank = ids.index(r["id"]) + 1 if r["id"] in ids else 0
    hits1 += 1 if rank == 1 else 0
    hits5 += 1 if 0 < rank <= 5 else 0
    hits10 += 1 if 0 < rank <= 10 else 0
    rows.append((r["id"], rank, round(out["legs"]["vector"] > 0)))

el = time.time() - t0
print(f"# {N} title-derived queries, k={K}, {el/N:.2f}s per query\n")
print(f"{'report':>9}  {'rank':>5}  title")
for rid, rank, _ in rows:
    t = con.execute("SELECT substr(title,1,70) FROM reports WHERE id=?", (rid,)).fetchone()[0]
    print(f"{rid:>9}  {str(rank) if rank else 'miss':>5}  {t}")
print(f"\nrecall@1  = {hits1}/{N} = {hits1/N:.0%}")
print(f"recall@5  = {hits5}/{N} = {hits5/N:.0%}")
print(f"recall@10 = {hits10}/{N} = {hits10/N:.0%}")
