#!/usr/bin/env python3
"""Deduplicate chunks: identical passages, then near-identical technique blocks.

Pass 1 — exact: normalise (lowercase, punctuation stripped, whitespace collapsed) and hash.
         Any chunk whose normalised text already exists is dropped (first occurrence wins).
Pass 2 — near-duplicate (Jaccard >= 0.85 on 5-word shingles, MinHash + LSH banding) among
         our own documents/skills, where the same technique is written up in several skills.
         The survivor is the chunk from a SKILL.md if one exists, else the longest text.
Reports are excluded from pass 2 on purpose: two reports quoting the same request are evidence,
not duplicates.
"""
import hashlib, re, sqlite3, sys, time, collections
import numpy as np

DB = os.environ.get("VAULT_DB", os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "vault", "_VAULT", "reports.sqlite"))
JACCARD = 0.85
SHINGLE = 5
NUM_HASH = 64
BANDS, ROWS = 16, 4          # 16*4 = 64

def norm(t):
    t = t.lower()
    t = re.sub(r"[^a-z0-9\s\[\]{}()<>=/|;:.,'\"\\-]", " ", t)
    return re.sub(r"\s+", " ", t).strip()

def shingles(text):
    w = norm(text).split()
    if len(w) < SHINGLE: return {hash(tuple(w))}
    return {hash(tuple(w[i:i+SHINGLE])) for i in range(len(w) - SHINGLE + 1)}

P = 4294967311
A = np.random.default_rng(42).integers(1, P, NUM_HASH, dtype=np.int64)
B = np.random.default_rng(7).integers(0, P, NUM_HASH, dtype=np.int64)

def minhash(sh):
    if not sh: return np.zeros(NUM_HASH, dtype=np.uint32)
    arr = np.fromiter(sh, dtype=np.int64, count=len(sh)) % P
    return ((arr[:, None] * A[None, :] + B[None, :]) % P).min(axis=0).astype(np.uint32)

def main():
    con = sqlite3.connect(DB, timeout=180)
    t0 = time.time()
    rows = con.execute("SELECT id, kind, path, text FROM chunks").fetchall()
    print(f"chunks before: {len(rows)}")

    # ---- pass 1: exact
    seen, dup_ids = {}, []
    for cid, kind, path, text in rows:
        h = hashlib.sha256(norm(text).encode()).hexdigest()
        if h in seen: dup_ids.append(cid)
        else: seen[h] = cid
    print(f"pass1 exact duplicates: {len(dup_ids)}")
    if dup_ids:
        con.execute("CREATE TABLE IF NOT EXISTS chunk_tombstones(sha256 TEXT PRIMARY KEY, kind TEXT, path TEXT, removed_at TEXT)")
        con.executemany("""INSERT OR IGNORE INTO chunk_tombstones(sha256,kind,path,removed_at)
                           SELECT sha256,kind,path,datetime('now') FROM chunks WHERE id=?""", [(i,) for i in dup_ids])
    con.executemany("DELETE FROM chunks WHERE id=?", [(i,) for i in dup_ids]); con.commit()

    # ---- pass 2: near-duplicate among docs
    docs = con.execute("SELECT id, path, text FROM chunks WHERE kind='doc' AND vec IS NULL AND length(text)>120").fetchall()
    print(f"pass2 candidates (docs): {len(docs)}")
    rng = np.random.default_rng(42)
    sigs, sets, meta = [], [], []
    for cid, path, text in docs:
        sh = shingles(text)
        sets.append(sh); sigs.append(minhash(sh)); meta.append((cid, path, len(text)))
    if not sigs:
        print("nothing to compare"); return
    sigs = np.vstack(sigs)
    buckets = collections.defaultdict(list)
    for i in range(len(meta)):
        for b in range(BANDS):
            key = (b, sigs[i, b*ROWS:(b+1)*ROWS].tobytes())
            buckets[key].append(i)

    cand = set()
    for idxs in buckets.values():
        if len(idxs) < 2: continue
        for a in range(len(idxs)):
            for b in range(a+1, len(idxs)):
                cand.add((idxs[a], idxs[b]))
    print(f"pass2 candidate pairs: {len(cand)}")

    parent = list(range(len(meta)))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb: parent[rb] = ra

    for a, b in cand:
        sa, sb = sets[a], sets[b]
        if not sa or not sb: continue
        inter = len(sa & sb); j = inter / (len(sa) + len(sb) - inter)
        if j >= JACCARD: union(a, b)

    groups = collections.defaultdict(list)
    for i in range(len(meta)): groups[find(i)].append(i)
    gone = []
    for g in groups.values():
        if len(g) < 2: continue
        # survivor: SKILL.md first, then longest
        g.sort(key=lambda i: (not (meta[i][1] or "").endswith("SKILL.md"), -meta[i][2]))
        keep = g[0]
        for i in g[1:]: gone.append(meta[i][0])
    print(f"pass2 near-duplicates dropped: {len(gone)}")
    if gone:
        con.execute("CREATE TABLE IF NOT EXISTS chunk_tombstones(sha256 TEXT PRIMARY KEY, kind TEXT, path TEXT, removed_at TEXT)")
        con.executemany("""INSERT OR IGNORE INTO chunk_tombstones(sha256,kind,path,removed_at)
                           SELECT sha256,kind,path,datetime('now') FROM chunks WHERE id=?""", [(i,) for i in gone])
    con.executemany("DELETE FROM chunks WHERE id=?", [(i,) for i in gone]); con.commit()
    n = con.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]
    print(f"chunks after: {n}  (removed {len(rows)-n} total, {time.time()-t0:.1f}s)")

main()
