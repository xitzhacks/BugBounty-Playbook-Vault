# Build log — 15,244-report corpus + RAG layer (2026-11)

Concrete numbers from a real build, so the next one is calibrated rather than guessed.

## Harvest

- Source: a public aggregator's `/api/reports` (list, 152 pages × 100, rate limit 600/min) and
  `hackerone.com/reports/<id>.json` (write-ups, unauthenticated, `Accept: application/json`).
- 15,244 metadata rows in ~3 min; write-ups in ~2.5 h with 4 workers at ~2.5/s.
- Outcome: **9,875 full bodies / 2,647 summary-only / 2,722 delisted (404)** = 15,244. 101 MB of text.
- Bounties: 3,241 paid rows, $4,934,914.52 (report as "$4.93M"; the .52 matters if you say "exact").
- 404s are ~18% of a public list — normal, not a failure. Store them with status and never quote them.

Throughput notes:
- 4 threads with `DELAY=0.35` settled at ~2.5 items/s; 8 threads triggered 429s.
- On 429: honour `Retry-After` (5–60 s), retry up to 3×. A 45 s blind sleep per 429 stalls a worker
  for a minute and halves the crawl rate.
- Watchdog loop: every 15 min, if PID gone and `remaining>0`, restart; append DB counts to a log.

## Chunking / embedding

- 27,407 chunks from 9,875 bodies + 323 docs, then +1,090 backfill = 28,497 (all with vectors).
- avg chunk 690–900 chars after section splitting at 2,400/300.
- Embedding rate observations (8 cores, no GPU) — see SKILL.md table. Ollama was the trap:
  35k chunks would have taken ~20 h; fastembed MiniLM did it in ~35 min.
- `.venv` is mandatory: distro Python is PEP-668 managed; `pip install fastembed` fails system-wide.

## Bugs hit while building (all fixed, all cheap to avoid)

1. **Filter after rank** — `class=IDOR AND bounty>=5000` matched 12 chunks but the vector leg returned 0
   because the global top-200 contained none of them. Fix: mask `sims` before `argsort`.
2. **`NOT IN` with NULLs** — coverage check `id NOT IN (SELECT report_id FROM chunks)` returned 0
   uncovered while 1,205 reports were uncovered (doc chunks have NULL report_id). Fix: `NOT EXISTS`.
3. **Short-body reports dropped** — min chunk length 300 silently excluded 1,205 reports. Fix: backfill.
4. **Downloaded JS as binary** — CloudFront serves pre-compressed bundles; `curl` without
   `--compressed` gives gzip/brotli bytes. Same class of mistake as reading a 0-byte response as "empty".
5. **Audit script false alarms** — comparing a float money sum with `int()` (4934914.52 vs rounded
   4,934,915) and walking a hidden `.commandcode` dir. Fix the audit, then re-run; report both runs.

## Retrieval quality baseline

15 title-derived queries, k=10, 1.56 s/query: recall@1 60%, @5 80%, @10 87%.
A tight-filter query (`IDOR`, ≥$5k) returned 12 hits in 0.7 s after the mask fix.

## MCP server shape that worked

Single-file stdio JSON-RPC (newline-delimited), no dependencies:
`initialize` → `{protocolVersion:"2024-11-05", capabilities:{tools:{}}, serverInfo}`; `tools/list`;
`tools/call` → `{content:[{type:"text",text}]}`. Tools: search, get_report, plan(feature),
bypass(protection), stats. Each hit wrapped in `<<<EVIDENCE … EVIDENCE>>>`; hard cap 20k chars.

Register non-interactively:
```bash
printf 'y\n' | hermes mcp add <name> \
  --command /path/to/.venv/bin/python --args /path/to/mcp_server.py
```
Interactive prompt otherwise answers "Cancelled." and nothing is saved.

## Deployment of the result into a docs vault

- Generated views: `by-class/` (one file per class) and `by-vault-category/` (one per playbook dir),
  each a table of every row; totals must equal the corpus count (checked by grep-count, not by eye).
- Wire each playbook README with an idempotent marker block (`<!-- CASESTOCK-LINK:BEGIN/END -->`) and
  a re-run script that rewrites it in place — never append twice.
- Index the vault's own markdown into the same DB (`documents` + FTS) so doctrine and evidence are
  returned by one query.
