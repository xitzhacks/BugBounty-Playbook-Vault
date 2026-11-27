---
title: "Eval harness — 40 operator questions, measured"
type: design
built: "2026-11-17"
baseline: "recall@5 80% → 92% after source balancing"
---

# Eval harness

## Why

The earlier title-derived eval used 15 queries (the current `eval_rag.py` defaults to 20) — it proved
a known document could be found and nothing else. This one uses operator phrasing, with ground truth
verified against the report bodies.

## Dataset — `eval/questions.jsonl`

40 questions, 18 classes, each row:

| field | meaning |
|---|---|
| q | the question as an operator would ask it ("rce via polyglot ascii file processed by imagemagick mvg in profile picture upload") |
| expect | the report id(s) that answer it — **verified**: the expected report's body contains the row's `marker` string |
| marker | the literal string used to prove the report is the right answer (e.g. `graphic-context`, `BillingDocumentDownload`, `DeleteStorySnaps`) |
| class | for the technique-coverage metric |
| tech | the technique name that should be surfaced for this class |

40 questions, every one verified: the expected report's body contains the row's marker.
Markers were checked against `bodies.body` before use; 6 were corrected after the first check failed.

## Metrics

1. **Recall@1 / @5 / @k and MRR** — does the right report appear.
2. **Technique coverage** — does the technique router name the right technique for that class. This is
   the metric that DVWA exposed: retrieving the right report while testing the wrong technique is a
   failed hunt.

## Baseline and the regression it caught

| Run | questions | recall@1 | recall@5 | recall@10 | MRR | technique coverage |
|---|---|---|---|---|---|---|
| merged index, no balancing | 25 | 36% | 80% | 80% | 0.54 | 68% |
| after source balancing | 25 | 36% | **92%** | 92% | **0.59** | 68% |
| **current, expanded set** | **40** | **40%** | **78%** | **78%** | **0.56** | **72%** |
| + cross-encoder rerank (jina-turbo-en, `--rerank`) | 40 | 45% | **70%** | 70% | 0.55 | 72% |

The expanded 40-question set is harder (SAML, CORS, prototype pollution, obscure reports), so recall@5
drops from 92% to 78% while MRR and technique coverage rise. That is the honest number to track from
now on — the 25-question figure was a smaller, easier set.

The first run exposed a real regression: after merging 27k skill chunks, doctrine crowded reports out of
the top-k — two SSRF questions and one IDOR question lost their expected report entirely. Skill passages
are longer and denser in keyword overlap than a report passage, so they win on BM25 and on cosine alike.

Fix in `search.py`: gather max(k*6, 40) fused candidates, split into reports and doctrine, then
interleave (report, doctrine, report, …). Both surfaces are represented; report-first keeps the
evidence in view.

## Remaining misses (honest)

9 of 40 miss on single-answer ground truth. Spot-checked example:

```
q28 "graphql introspection left enabled exposes the whole schema" → expected #419883
top-3:  [1] #2954320 (PII)   [2] skill graphql-introspection (doctrine)
        [3] #2886723 "GraphQL Introspection Enabled on Shopify API Endpoint"   ← a correct answer
```

The retriever put a valid introspection report at rank 3; the dataset only accepts #419883. Most of the
9 misses are this shape — multi-answer questions scored against one answer. An earlier attempt to widen
`expect` by marker matching made it *worse* (a GraphQL IDOR report was accepted as a "pdf generator"
answer), so the list was reverted to single verified answers and the ambiguity is recorded here instead.

## Cross-encoder rerank — tried, measured, left OFF

`search.py --rerank` re-scores the fused candidates with `jinaai/jina-reranker-v1-turbo-en`
(127 pairs/s once loaded). Measured over the same 40 questions:

| | recall@1 | recall@5 | MRR | wall clock |
|---|---|---|---|---|
| no rerank | 40% | 78% | 0.56 | 70 s |
| rerank | **45%** | **70%** | 0.55 | **416 s** |

It buys +5 pp at rank 1 and costs 8 pp at rank 5 plus 6× latency (the ONNX model loads per process
invocation, ~8 s of the 10 s per question). Same net effect you'd get from a coin flip on a corpus
where many reports are equally valid answers.

Decision: the flag stays (default off) so it can be retried per-target, but it is not in the default
path. The lesson is recorded because "add a reranker" is the standard advice and here it measured
negative — keep it as evidence, not as a default.

## Technique coverage 72% — what the other 32% means

Missing labels are techniques the doctrine describes in prose/bullets without a heading:
`phar`, `dos`, `information disclosure`, `access control`. The payload table now indexes 19,278 fenced
blocks (item D, shipped) — the next step is to derive technique names from payload context, not just
headings.

## Run it

```bash
cd <repo> && .venv/bin/python scripts/eval_run.py            # table + summary
.venv/bin/python scripts/eval_run.py --json | jq .summary
```
Historical run: 45 s for 25 questions (1.8 s/question); the shipped questions file has 40.
