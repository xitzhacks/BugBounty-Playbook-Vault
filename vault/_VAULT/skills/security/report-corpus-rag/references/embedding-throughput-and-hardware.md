# Embedding throughput and hardware choices for a report corpus

Measured on a CPU-only box: 8 cores, 15 GB RAM, no GPU, Debian/Kali. Corpus: 9,875 write-ups +
323 markdown docs → 28,497 section chunks.

## Measured

| Model | Runtime | Batched throughput | Dim | 27k chunks ETA | Verdict |
|---|---|---|---|---|---|
| embeddinggemma:300m | Ollama (`/api/embed`) | 0.2–0.7 chunks/s | 768 | ~11–38 h | unusable here |
| nomic-embed-text | Ollama | 0.3–0.4 chunks/s | 768 | >18 h | unusable here |
| bge-small-en-v1.5 | fastembed 0.9.x (ONNX) | 3.5 chunks/s | 384 | ~2.8 h | good quality, slow |
| all-MiniLM-L6-v2 | fastembed (ONNX) | 15.2 chunks/s | 384 | ~30 min | chosen |

Ollama also ignored `options.num_thread` (16 docs took 64 s at n=16 with num_thread=8). It is a
CPU-execution-path problem, not a model-quality problem — do not conclude "embeddings don't work".

Fastembed install without touching the system Python (PEP 668 blocks pip):

```bash
python3 -m venv .venv
.venv/bin/pip install --quiet fastembed numpy
.venv/bin/python -c "import fastembed; print(fastembed.__version__)"
```

## Choosing

- **No GPU:** MiniLM (384d) for the first pass, bge-small for a nightly re-embed if precision matters.
  Anything ≥1B params on CPU is a non-starter for a 20k+ chunk corpus.
- **With any GPU (even 8 GB):** bge-m3 (1024d, multilingual, strong on code/payload text) or
  Qwen3-Embedding-0.6B; then rerank with bge-reranker-base over the fused top-25.
- **Never:** a generative model as the embedder. Gemma 2/4 and Llama variants cannot emit embeddings;
  a "4B embedding model" on CPU runs ~1 chunk/s and loses to a 300M model that fits the box.

## Engineering rules

1. Benchmark 32 chunks through the exact runtime you plan to use *before* launching the full pass.
2. Store `model`, `dim`, `sha256(text)` per chunk row. Re-embedding a new model = filtered rebuild
   (`DELETE FROM chunks WHERE model <> ?`), never a mixed vector space.
3. Batch 32–64 texts per call; per-request overhead dominates below ~16.
4. Resume by `(sha256, model)` membership so a killed run costs nothing.
5. Log `done/total` + instantaneous rate every ~640 chunks; the ETA is what tells you a runtime is
   wrong within the first two minutes instead of two hours.
