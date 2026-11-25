#!/usr/bin/env python3
"""Hybrid retrieval: FTS5 BM25 + vector cosine + RRF, with metadata filters applied BEFORE ranking.

  python3 hybrid_search.py reports.sqlite "ssrf gcp metadata pdf" --class SSRF -k 5
  python3 hybrid_search.py reports.sqlite "cache poisoning" --kind doc --json

Filters: --class --program --severity --min-bounty --year --kind report|doc
Requires fastembed + numpy; same EMBED_MODEL as the build.
"""
import argparse, json, os, sqlite3, sys
from collections import Counter

MODEL = os.environ.get("EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
CACHE = os.path.expanduser("~/.cache/corpus_rag")

CLASS_TERMS = {
 "XSS": ["%xss%", "%cross-site scripting%"], "CSRF": ["%csrf%"], "SSRF": ["%ssrf%"],
 "SQLI": ["%sql injection%"], "IDOR": ["%idor%", "%direct object%"],
 "RCE": ["%code injection%", "%command injection%", "%deserialization%", "%remote code%"],
 "TRAV": ["%path traversal%", "%file inclusion%"],
 "AUTH": ["%authentication%", "%password%", "%2fa%"],
 "ACL": ["%access control%", "%authorization%", "%privilege%"],
 "INFO": ["%information disclosure%", "%information exposure%"],
 "REDIR": ["%open redirect%"], "LOGIC": ["%business logic%", "%race condition%"],
 "MEM": ["%memory%", "%buffer%", "%overflow%"], "DOS": ["%denial of service%", "%resource%"],
 "INJ": ["%injection%", "%smuggling%", "%xxe%"], "CRYPTO": ["%cryptographic%", "%tls%", "%ssl%"],
 "CONF": ["%misconfiguration%", "%clickjacking%", "%cors%"],
}

def load_matrix(con):
    import numpy as np
    n = con.execute("SELECT COUNT(*) FROM chunks WHERE vec IS NOT NULL").fetchone()[0]
    os.makedirs(CACHE, exist_ok=True)
    tag = f"{MODEL.replace('/','_')}_{n}"
    mp, ip = os.path.join(CACHE, tag + ".npy"), os.path.join(CACHE, tag + ".ids.json")
    if os.path.exists(mp) and os.path.exists(ip):
        return np.load(mp), json.load(open(ip))
    rows = con.execute("SELECT id, vec, dim FROM chunks WHERE vec IS NOT NULL").fetchall()
    if not rows: sys.exit("no vectors — run build_rag.py first")
    mat = np.zeros((len(rows), rows[0][2]), dtype="float32")
    ids = []
    for i, (cid, blob, _d) in enumerate(rows):
        mat[i] = np.frombuffer(blob, dtype="float32"); ids.append(cid)
    nrm = np.linalg.norm(mat, axis=1, keepdims=True); nrm[nrm == 0] = 1
    mat = mat / nrm
    np.save(mp, mat); json.dump(ids, open(ip, "w"))
    return mat, ids

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("db"); ap.add_argument("query", nargs="+")
    ap.add_argument("--class", dest="cls"); ap.add_argument("--program")
    ap.add_argument("--severity"); ap.add_argument("--min-bounty", type=float, default=0)
    ap.add_argument("--year", type=int); ap.add_argument("--kind", choices=["report", "doc"])
    ap.add_argument("--k", "-k", type=int, default=5); ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    q = " ".join(a.query)
    con = sqlite3.connect(a.db); con.row_factory = sqlite3.Row

    where, args = [], []
    if a.program:  where.append("lower(r.program) LIKE ?");  args.append(f"%{a.program.lower()}%")
    if a.severity: where.append("lower(r.severity)=?");      args.append(a.severity.lower())
    if a.min_bounty: where.append("COALESCE(r.bounty,0)>=?"); args.append(a.min_bounty)
    if a.year:     where.append("substr(COALESCE(r.disclosed_at,''),1,4)=?"); args.append(str(a.year))
    if a.cls:
        pats = CLASS_TERMS.get(a.cls.upper(), [f"%{a.cls.lower()}%"])
        where.append("(" + " OR ".join("lower(r.weakness) LIKE ?" for _ in pats) + ")"); args += pats
    filt = (" AND " + " AND ".join(where)) if where else ""
    kind_sql = "AND c.kind=?" if a.kind else ""
    kind_args = [a.kind] if a.kind else []

    terms = [t for t in q.replace('"', " ").split() if len(t) > 1]
    match = " OR ".join(f'"{t}"' for t in terms[:12]) or '""'
    bm25 = []
    try:
        bm25 = [(r["id"], r["score"]) for r in con.execute(f"""
            SELECT c.id, bm25(chunks_fts) AS score FROM chunks_fts
            JOIN chunks c ON c.id = chunks_fts.rowid
            LEFT JOIN reports r ON r.id = c.report_id
            WHERE chunks_fts MATCH ? {kind_sql} {filt} ORDER BY score LIMIT 80""", [match] + kind_args + args)]
    except sqlite3.OperationalError as e:
        print("bm25 failed:", e, file=sys.stderr)

    import numpy as np
    from fastembed import TextEmbedding
    mat, ids = load_matrix(con)
    qv = next(iter(TextEmbedding(model_name=MODEL, threads=os.cpu_count() or 4).embed([q])))
    qv = qv / (np.linalg.norm(qv) or 1)
    sims = mat @ qv.astype("float32")

    if where or a.kind:  # FILTER BEFORE RANKING — otherwise a tight filter returns zero hits
        allowed = {r["id"] for r in con.execute(f"""
            SELECT c.id FROM chunks c LEFT JOIN reports r ON r.id = c.report_id
            WHERE 1=1 {filt} {kind_sql}""", args + kind_args)}
        mask = np.fromiter((cid in allowed for cid in ids), dtype=bool, count=len(ids)) if allowed \
               else np.zeros(len(ids), dtype=bool)
        sims = np.where(mask, sims, -1.0)

    vec = [(ids[i], float(sims[i])) for i in np.argsort(-sims)[:200] if sims[i] > -0.999][:80]

    K, fused = 60, {}
    for rank, (cid, _) in enumerate(bm25): fused[cid] = fused.get(cid, 0) + 1 / (K + rank + 1)
    for rank, (cid, _) in enumerate(vec):  fused[cid] = fused.get(cid, 0) + 1 / (K + rank + 1)

    out, seen = [], set()
    for cid, score in sorted(fused.items(), key=lambda kv: -kv[1])[:max(a.k * 4, 20)]:
        c = con.execute("""SELECT c.*, r.title, r.program, r.bounty, r.severity, r.weakness, r.disclosed_at
                           FROM chunks c LEFT JOIN reports r ON r.id=c.report_id WHERE c.id=?""", (cid,)).fetchone()
        key = c["report_id"] or c["path"]
        if key in seen: continue
        seen.add(key)
        out.append(dict(score=round(score, 4), kind=c["kind"], report_id=c["report_id"], path=c["path"],
                        heading=c["heading"], title=c["title"], program=c["program"], bounty=c["bounty"],
                        severity=c["severity"], weakness=c["weakness"], disclosed=c["disclosed_at"],
                        text=c["text"][:1600]))
        if len(out) >= a.k: break

    if a.json:
        print(json.dumps({"query": q, "legs": {"bm25": len(bm25), "vector": len(vec)}, "hits": out}, indent=2))
        return
    print(f"query: {q}\nlegs: bm25={len(bm25)} vector={len(vec)} fused={len(fused)}\n")
    for i, h in enumerate(out, 1):
        if h["kind"] == "report":
            print(f"[{i}] #{h['report_id']} {(h['title'] or '')[:95]}")
            print(f"    {h['program']} · {h['severity']} · {h['disclosed'] or ''} · score {h['score']}")
            print(f"    https://hackerone.com/reports/{h['report_id']}")
        else:
            print(f"[{i}] DOC {h['path']}  (score {h['score']})")
        print(f"    § {h['heading']}\n    " + h["text"][:400].replace("\n", "\n    ") + "\n")

main()
