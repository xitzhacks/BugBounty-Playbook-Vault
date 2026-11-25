#!/usr/bin/env python3
"""Eval harness: 25 operator-style questions with hand-verified ground truth.

Scores two things:
  1. RECALL of the report layer   – does the right report appear in top-k (1/5/10), plus MRR
  2. TECHNIQUE COVERAGE           – does the technique router name the right technique for that class

The second metric is the one that matters after the DVWA finding: a run can retrieve the right report
and still test the wrong technique.

  python3 eval_run.py            # full run
  python3 eval_run.py --k 10     # custom depth
"""
import argparse, json, os, re, sqlite3, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.environ.get("VAULT_DB", os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "vault", "_VAULT", "reports.sqlite"))
PY = os.path.join(HERE, ".venv", "bin", "python")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--k", type=int, default=10)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--rerank", action="store_true")
    a = ap.parse_args()

    qs = [json.loads(l) for l in open(os.path.join(HERE, "eval", "questions.jsonl"))]
    con = sqlite3.connect(DB)
    r1 = r5 = rk = 0
    mrr = 0.0
    t_hit = t_tot = 0
    rows = []
    t0 = time.time()

    for q in qs:
        cmd = [PY, os.path.join(HERE, "search.py"), q["q"], "-k", str(a.k), "--json"]
        if a.rerank: cmd.append("--rerank")
        p = subprocess.run(cmd,
                           capture_output=True, text=True, timeout=300)
        try:
            out = json.loads(p.stdout)
        except Exception:
            rows.append({**q, "rank": None, "error": p.stderr[:200]}); continue
        ids = [h["report_id"] for h in out["hits"] if h["kind"] == "report"]
        rank = None
        for i, rid in enumerate(ids, 1):
            if rid in q["expect"]:
                rank = i; break
        if rank == 1: r1 += 1
        if rank and rank <= 5: r5 += 1
        if rank and rank <= a.k: rk += 1
        if rank: mrr += 1.0 / rank

        # technique coverage: is the expected technique named for this class?
        techs = [x[0] for x in con.execute("""SELECT name FROM techniques WHERE upper(cls)=upper(?)
                                              ORDER BY CASE confidence WHEN 'path' THEN 0 ELSE 1 END LIMIT 400""",
                                           (q["class"],))]
        lab = (q.get("tech") or "").lower()
        hit = any(lab in t.lower() for t in techs) if lab else False
        t_tot += 1; t_hit += 1 if hit else 0
        rows.append({**q, "rank": rank, "tech_hit": hit,
                     "top": ids[:5], "techs_n": len(techs)})

    n = len(qs)
    res = {"questions": n, "k": a.k,
           "recall@1": round(r1/n, 3), "recall@5": round(r5/n, 3), "recall@k": round(rk/n, 3),
           "mrr": round(mrr/n, 3),
           "technique_coverage": round(t_hit/max(1, t_tot), 3),
           "seconds": round(time.time()-t0, 1)}
    if a.json:
        print(json.dumps({"summary": res, "rows": rows}, indent=2)); return
    print(f"{'id':>3} {'class':8} {'rank':>4} {'tech':>5}  question")
    for r in rows:
        print(f"{r['id']:3d} {r['class']:8} {str(r['rank'] or 'MISS'):>4} {str(r.get('tech_hit')):>5}  {r['q'][:58]}")
    print(f"\nrecall@1 = {res['recall@1']:.0%}   recall@5 = {res['recall@5']:.0%}   "
          f"recall@{a.k} = {res['recall@k']:.0%}   MRR = {res['mrr']:.2f}")
    print(f"technique coverage = {res['technique_coverage']:.0%}  (right technique named for the class)")
    print(f"{n} questions in {res['seconds']}s")

if __name__ == "__main__":
    main()
