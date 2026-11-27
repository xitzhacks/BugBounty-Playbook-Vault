#!/usr/bin/env python3
"""Hybrid search over the vault: BM25 (FTS5) + vector (fastembed) + reciprocal-rank fusion.

  python3 search.py "ssrf gcp metadata pdf parser"
  python3 search.py "password reset token" --class AUTH --min-bounty 1000 -k 8
  python3 search.py "cache deception" --kind doc          # our own playbooks only
  python3 search.py "xss svg upload" --json               # machine-readable, for agents

Filters: --class (hexbrain class id or a weakness substring), --program, --severity,
--min-bounty, --year, --kind report|doc, --k.
"""
import argparse, json, os, sqlite3, struct, sys, math, time

VAULT = os.environ.get("VAULT_ROOT", os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "vault"))
DB = os.path.join(VAULT, "_VAULT", "reports.sqlite")
MODEL = os.environ.get("EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
RERANK_MODEL = os.environ.get("RERANK_MODEL", "jinaai/jina-reranker-v1-turbo-en")
_RERANKER = None
CACHE = os.path.expanduser("~/.cache/vault_rag")

CLASS_RX = {
 "XSS": r"cross-site scripting|\bxss\b", "CSRF": r"cross-site request forgery|\bcsrf\b",
 "SSRF": r"server-side request forgery|\bssrf\b", "SQLI": r"sql injection",
 "IDOR": r"insecure direct object|\bidor\b",
 "RCE": r"code injection|command injection|remote code|deserialization|template injection|unrestricted upload",
 "TRAV": r"path traversal|file inclusion|directory traversal",
 "AUTH": r"authentication|brute force|session fixation|password|credential|2fa",
 "ACL": r"access control|authorization|privilege|permission",
 "INFO": r"information disclosure|information exposure|sensitive|privacy",
 "REDIR": r"open redirect|url redirection", "LOGIC": r"business logic|race condition|toctou",
 "MEM": r"buffer|overflow|use after free|memory|integer|uninitialized|type confusion",
 "DOS": r"denial of service|resource consumption|resource exhaustion",
 "INJ": r"injection|crlf|smuggling|response splitting|xml external|\bxxe\b",
 "CRYPTO": r"cryptograph|certificate|\bssl\b|\btls\b|encryption|hash",
 "CONF": r"misconfiguration|secure design|clickjacking|cors|subdomain takeover|cache poisoning",
}

def load_vectors(con):
    n = con.execute("SELECT COUNT(*) FROM chunks WHERE vec IS NOT NULL").fetchone()[0]
    os.makedirs(CACHE, exist_ok=True)
    tag = f"{MODEL.replace('/','_')}_{n}"
    mp, ip = os.path.join(CACHE, f"{tag}.npy"), os.path.join(CACHE, f"{tag}.ids.json")
    if os.path.exists(mp) and os.path.exists(ip):
        import numpy as np
        return np.load(mp), json.load(open(ip)), None
    import numpy as np
    rows = con.execute("SELECT id, vec, dim FROM chunks WHERE vec IS NOT NULL").fetchall()
    if not rows: return None, None, "no vectors yet — run build_rag.py"
    dim = rows[0][2]
    mat = np.zeros((len(rows), dim), dtype="float32")
    ids = []
    for i, (cid, blob, d) in enumerate(rows):
        mat[i] = np.frombuffer(blob, dtype="float32")
        ids.append(cid)
    norms = np.linalg.norm(mat, axis=1, keepdims=True); norms[norms == 0] = 1
    mat = mat / norms
    np.save(mp, mat); json.dump(ids, open(ip, "w"))
    return mat, ids, None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("query", nargs="+")
    ap.add_argument("--class", dest="cls")
    ap.add_argument("--program")
    ap.add_argument("--severity")
    ap.add_argument("--min-bounty", type=float, default=0)
    ap.add_argument("--year", type=int)
    ap.add_argument("--kind", choices=["report", "doc", "skill"])
    ap.add_argument("--source", choices=["skills", "vault", "all"], default="all")
    ap.add_argument("--k", "-k", type=int, default=5)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--rerank", action="store_true", help="cross-encoder rerank of the fused candidates")
    a = ap.parse_args()
    q = " ".join(a.query)
    con = sqlite3.connect(DB); con.row_factory = sqlite3.Row

    where, args = [], []
    if a.program: where.append("lower(r.program) LIKE ?"); args.append(f"%{a.program.lower()}%")
    if a.severity: where.append("lower(r.severity)=?"); args.append(a.severity.lower())
    if a.min_bounty: where.append("COALESCE(r.bounty,0)>=?"); args.append(a.min_bounty)
    if a.year: where.append("substr(COALESCE(r.disclosed_at,''),1,4)=?"); args.append(str(a.year))
    if a.cls:
        # plain LIKE terms per class (no REGEXP extension in stock SQLite)
        terms_for = {
            "XSS": ["%xss%", "%cross-site scripting%"], "CSRF": ["%csrf%"],
            "SSRF": ["%ssrf%"], "SQLI": ["%sql injection%"], "IDOR": ["%idor%", "%direct object%"],
            "RCE": ["%code injection%", "%command injection%", "%deserialization%", "%remote code%"],
            "TRAV": ["%path traversal%", "%file inclusion%"], "AUTH": ["%authentication%", "%password%", "%2fa%"],
            "ACL": ["%access control%", "%authorization%", "%privilege%"], "INFO": ["%information disclosure%", "%information exposure%"],
            "REDIR": ["%open redirect%"], "LOGIC": ["%business logic%", "%race condition%"],
            "MEM": ["%memory%", "%buffer%", "%overflow%"], "DOS": ["%denial of service%", "%resource%"],
            "INJ": ["%injection%", "%smuggling%", "%xxe%"], "CRYPTO": ["%cryptographic%", "%tls%", "%ssl%"],
            "CONF": ["%misconfiguration%", "%clickjacking%", "%cors%"],
        }
        pats = terms_for.get(a.cls.upper(), [f"%{a.cls.lower()}%"])
        where.append("(" + " OR ".join("lower(r.weakness) LIKE ?" for _ in pats) + ")")
        args += pats
    # source scoping: skills (mirrored skill docs) vs vault (playbooks + reports)
    if a.kind == "skill": where.append("c.path LIKE 'skills/%'")
    elif a.kind == "doc": where.append("c.path IS NOT NULL AND c.path NOT LIKE 'skills/%'")
    if a.source == "skills": where.append("c.path LIKE 'skills/%'")
    elif a.source == "vault": where.append("COALESCE(c.path,'') NOT LIKE 'skills/%'")
    filt = (" AND " + " AND ".join(where)) if where else ""

    # --- BM25 leg
    terms = [t for t in q.replace('"', " ").split() if len(t) > 1]
    match = " OR ".join(f'"{t}"' for t in terms[:12]) or '""'
    bm25 = []
    try:
        sql = """SELECT c.id, bm25(chunks_fts) AS score FROM chunks_fts
                 JOIN chunks c ON c.id = chunks_fts.rowid
                 LEFT JOIN reports r ON r.id = c.report_id
                 WHERE chunks_fts MATCH ? {} {} ORDER BY score LIMIT 80""".format(
                 "AND c.kind='doc'" if a.kind == "doc" else ("AND c.kind='report'" if a.kind == "report" else ""), filt)
        bm25 = [(r["id"], r["score"]) for r in con.execute(sql, [match] + args)]
    except sqlite3.OperationalError:
        try:
            sql = """SELECT c.id, bm25(chunks_fts) AS score FROM chunks_fts
                     JOIN chunks c ON c.id=chunks_fts.rowid WHERE chunks_fts MATCH ? ORDER BY score LIMIT 80"""
            bm25 = [(r["id"], r["score"]) for r in con.execute(sql, [match])]
        except Exception as e:
            print("bm25 failed:", e, file=sys.stderr)

    # --- vector leg
    vec_hits = []
    mat, ids, err = load_vectors(con)
    if mat is not None:
        from fastembed import TextEmbedding
        import numpy as np
        m = TextEmbedding(model_name=MODEL, threads=os.cpu_count() or 4)
        qv = next(iter(m.embed([q])))
        qv = qv / (np.linalg.norm(qv) or 1)
        sims = mat @ qv.astype("float32")
        # filter BEFORE ranking: a tight filter (e.g. class=bounty>5000) can hold almost no
        # neighbours of the global top-200, so mask the whole matrix first.
        # chunks.kind is only 'report'/'doc'; skills are marked by path, so do not
        # filter on kind for --kind skill (the path filter below already handles it).
        kind_sql = "" if a.kind in (None, "skill") else "AND c.kind=?"
        kind_args = [] if a.kind in (None, "skill") else [a.kind]
        if where or a.kind:
            allowed = {r["id"] for r in con.execute(
                f"""SELECT c.id FROM chunks c LEFT JOIN reports r ON r.id=c.report_id
                    WHERE 1=1 {filt} {kind_sql}""", args + kind_args)}
            if allowed:
                mask = np.fromiter((cid in allowed for cid in ids), dtype=bool, count=len(ids))
                sims = np.where(mask, sims, -1.0)
            else:
                sims = np.full_like(sims, -1.0)
        top = np.argsort(-sims)[:200]
        for i in top:
            if sims[i] <= -0.999: break
            vec_hits.append((ids[i], float(sims[i])))
            if len(vec_hits) >= 80: break

    # --- fuse (RRF)
    K = 60; fused = {}
    for rank, (cid, _) in enumerate(bm25): fused[cid] = fused.get(cid, 0) + 1 / (K + rank + 1)
    for rank, (cid, _) in enumerate(vec_hits): fused[cid] = fused.get(cid, 0) + 1 / (K + rank + 1)
    ranked = sorted(fused.items(), key=lambda kv: -kv[1])[:max(a.k * 4, 20)]

    gathered, seen = [], set()
    for cid, score in ranked:
        c = con.execute("""SELECT c.*, r.title, r.program, r.bounty, r.severity, r.weakness, r.disclosed_at
                           FROM chunks c LEFT JOIN reports r ON r.id=c.report_id WHERE c.id=?""", (cid,)).fetchone()
        key = c["report_id"] if c["report_id"] else c["path"]
        if key in seen: continue
        seen.add(key)
        gathered.append({
            "score": round(score, 4), "chunk_id": cid, "kind": c["kind"],
            "report_id": c["report_id"], "path": c["path"], "heading": c["heading"],
            "title": c["title"], "program": c["program"], "severity": c["severity"],
            "weakness": c["weakness"], "bounty": c["bounty"], "disclosed": c["disclosed_at"],
            "text": c["text"][:1600],
        })
        if len(gathered) >= max(a.k * 6, 40): break

    # Source balancing: doctrine (skill/vault docs) is longer and denser than a report passage, so
    # after merging skills into the index it crowded reports out of the top-k (measured: SSRF
    # questions lost their expected report entirely). Interleave report / doctrine so both surfaces
    # are represented, starting with the report.
    reps = [x for x in gathered if x["kind"] == "report"]
    docs_ = [x for x in gathered if x["kind"] != "report"]

    if a.rerank:
        global _RERANKER
        from fastembed.rerank.cross_encoder import TextCrossEncoder
        if _RERANKER is None:
            _RERANKER = TextCrossEncoder(model_name=RERANK_MODEL, threads=os.cpu_count() or 4)
        def _rr(items):
            if not items: return items
            sc = list(_RERANKER.rerank(q, [i["text"][:1400] for i in items]))
            for it, v in zip(items, sc): it["rerank"] = round(float(v), 3)
            return sorted(items, key=lambda x: -x["rerank"])
        reps, docs_ = _rr(reps), _rr(docs_)
    out = []
    i = j = 0
    while len(out) < a.k and (i < len(reps) or j < len(docs_)):
        if i < len(reps):
            out.append(reps[i]); i += 1
        if len(out) < a.k and j < len(docs_):
            out.append(docs_[j]); j += 1

    if a.json:
        print(json.dumps({"query": q, "legs": {"bm25": len(bm25), "vector": len(vec_hits)}, "hits": out}, indent=2))
        return
    print(f"query: {q}\nlegs: bm25={len(bm25)} vector={len(vec_hits)} fused={len(fused)}\n")
    for i, h in enumerate(out, 1):
        if h["kind"] == "report":
            print(f"[{i}] #{h['report_id']} {h['title'][:95]}")
            bits = [h["program"] or "-", h["severity"] or "-", f"${h['bounty']:,.0f}" if h["bounty"] else "-"]
            print(f"    {' · '.join(bits)} · {(h['disclosed'] or '')[:10]} · score {h['score']}")
            print(f"    https://hackerone.com/reports/{h['report_id']}")
        else:
            print(f"[{i}] VAULT {h['path']}  (score {h['score']})")
        if h["heading"]: print(f"    § {h['heading']}")
        print("    " + h["text"][:420].replace("\n", "\n    "))
        print()

if __name__ == "__main__":
    main()
