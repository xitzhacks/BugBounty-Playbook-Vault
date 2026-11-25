# Hybrid retrieval pitfalls that return zero results silently

Every item below produced a wrong answer with no error message. They are ordered by how long they
cost when undiscovered.

## 1. Filter applied after ranking (the big one)

```python
# WRONG — global top-200, then drop disallowed
sims = mat @ q
top = np.argsort(-sims)[:200]
hits = [ids[i] for i in top if ids[i] in allowed]
```

With a tight filter (class = IDOR **and** bounty ≥ $5000 → only 12 chunks in the whole index), the
global top-200 contained none of them. The vector leg returned 0 hits while BM25 returned 12, so the
UI showed results and nobody noticed half the pipeline was dead.

```python
# RIGHT — mask first, then rank
if filters:
    mask = np.fromiter((cid in allowed for cid in ids), dtype=bool, count=len(ids))
    sims = np.where(mask, sims, -1.0)
top = np.argsort(-sims)[:200]
```

Cost of masking the full matrix: ~11M float ops for 28k×384 — irrelevant next to the embedding call.

## 2. `NOT IN` against a subquery containing NULL

Chunk rows for internal documents carry `report_id = NULL`. This returns **0 rows even when a gap
exists**, because `x NOT IN (…, NULL, …)` evaluates to NULL:

```sql
-- WRONG: silently empty
SELECT count(*) FROM bodies b WHERE body <> '' AND b.id NOT IN (SELECT report_id FROM chunks);
```

Use `NOT EXISTS`, and if the number still looks clean, cross-check it against a `COUNT(DISTINCT)`:

```sql
SELECT count(*) FROM bodies b WHERE body <> '' AND NOT EXISTS (SELECT 1 FROM chunks c WHERE c.report_id = b.id);
SELECT count(DISTINCT report_id) FROM chunks;
```

## 3. Minimum-chunk-length filter drops whole reports

A splitter with `if len(body) < 300: skip` silently lost 1,205 reports (coverage 8,670/9,875).
Nothing errored; the index simply had no rows for them.

Gate: `count(distinct report_id) == count(*) from bodies where body <> ''`. Backfill every uncovered
report with one whole-body chunk, then re-run inference — the resume key makes it ~1,090 extra chunks.

## 4. `chunks_fts` desync after a schema change

If you `DROP TABLE chunks` while leaving `chunks_fts` (an external-content FTS5 table), BM25 starts
returning rowids that no longer resolve. Drop both, rebuild, and let the insert triggers refill FTS.

## 5. Dedupe at pack time, not retrieval time

The same bug filed twice occupies two top-k slots with near-identical text. Dedupe by
`(program, title similarity)` when packing the final 5–8 passages; retrieval should still keep both
so recall metrics stay honest.

## 6. Empty-body rows must not be cited

2,647 summary-only and 2,722 delisted rows sit in the same table as real write-ups. Filter on
`length(body) > 0` for evidence, surface the summary when it exists, and label the row
`(body not public / not stored)` — never let a retrieval result imply a payload that isn't there.

## 7. Query-time embedding must use the same model as the index

Loading vectors built by MiniLM and embedding the query with bge-small yields confident nonsense.
Read the model name from `SELECT DISTINCT model FROM chunks` and fail loudly on mismatch.

## 8. Latency reality check

Hybrid query over 28k chunks: 1.2–1.6 s (BM25 + 384-d brute force + one embed call). If it is much
slower, you are re-embedding the corpus or recomputing norms per query. Cache the matrix to `.npy`
keyed by `(model, row_count)` and normalise once.
