#!/usr/bin/env python3
"""Retrieval smoke test for a report corpus.

For N random reports that have a real body, build a query from the report's own title (content
words only) and check whether that report comes back in the top-k of the hybrid search.

Honest framing: title-derived queries are EASIER than operator questions, so this is a FLOOR,
not a quality score. It answers one question: can the index find a document we know exists?
Use it after every rebuild / chunker change / model swap — if recall@10 drops, the change broke
something. Then write a hand-made eval set for real quality.

Usage:
  eval_rag.py [N] [--db PATH] [--search /path/to/search.py] [--py /path/to/.venv/bin/python]
              [--k 10] [--seed 7]

Baseline (2026-11-16, 27,407 chunks, all-MiniLM-L6-v2, 15 title-derived queries):
  recall@1 60% · recall@5 80% · recall@10 87% · 1.2-1.6 s/query
"""
import argparse, json, os, random, re, sqlite3, subprocess, sys, time

STOP = set("the a an and or of to in on for with via from at by is are be as it this that how my your our".split())


def query_from(title: str) -> str:
    words = [w for w in re.findall(r"[A-Za-z0-9]{3,}", title.lower()) if w not in STOP]
    return " ".join(words[:7])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("n", nargs="?", type=int, default=15)
    ap.add_argument("--db", default=os.environ.get("CORPUS_DB",
                    "/home/user/projects/FAN/Vault/_VAULT/reports.sqlite"))
    ap.add_argument("--search", default=None, help="path to search.py")
    ap.add_argument("--py", default=None, help="python that has fastembed installed")
    ap.add_argument("--k", type=int, default=10)
    ap.add_argument("--seed", type=int, default=7)
    a = ap.parse_args()

    here = os.path.dirname(os.path.abspath(__file__))
    search = a.search or os.path.join(os.path.dirname(here), "search.py")
    py = a.py or sys.executable

    con = sqlite3.connect(a.db)
    con.row_factory = sqlite3.Row
    pool = con.execute(
        "SELECT id,title FROM reports WHERE id IN "
        "(SELECT id FROM bodies WHERE length(COALESCE(body,''))>1500)").fetchall()
    if not pool:
        sys.exit("no reports with a body >1500 chars — check the DB path/schema")
    random.seed(a.seed)
    sample = random.sample(pool, min(a.n, len(pool)))

    hits = {1: 0, 5: 0, 10: 0}
    rows, errors = [], 0
    t0 = time.time()
    for r in sample:
        q = query_from(r["title"])
        p = subprocess.run([py, search, q, "-k", str(a.k), "--json"],
                           capture_output=True, text=True, timeout=240)
        try:
            out = json.loads(p.stdout)
        except Exception:
            errors += 1
            rows.append((r["id"], "ERR"))
            continue
        ids = [h["report_id"] for h in out["hits"] if h.get("kind") == "report"]
        rank = ids.index(r["id"]) + 1 if r["id"] in ids else 0
        for kk in hits:
            if 0 < rank <= kk:
                hits[kk] += 1
        rows.append((r["id"], rank or "miss"))

    el = time.time() - t0
    print(f"# {len(sample)} title-derived queries, k={a.k}, {el/len(sample):.2f}s per query"
          + (f", {errors} errors" if errors else "") + "\n")
    print(f"{'report':>9}  {'rank':>5}")
    for rid, rank in rows:
        print(f"{rid:>9}  {str(rank):>5}")
    print()
    for kk in sorted(hits):
        print(f"recall@{kk:<2} = {hits[kk]}/{len(sample)} = {hits[kk]/len(sample):.0%}")
    if errors:
        print("\nERRORS present — fix the search path/venv before trusting these numbers.")
        sys.exit(1)


if __name__ == "__main__":
    main()
