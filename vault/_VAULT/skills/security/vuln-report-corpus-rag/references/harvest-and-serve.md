# Harvest + serve — concrete recipe from a 15,244-report build (2026-11)

## Endpoints

| Purpose | URL | Notes |
|---|---|---|
| report list | `https://hexbrainai.com/api/reports?limit=100&offset=N` | `{total, rows[]}`; limit max 100; 600 req/min/IP |
| write-up | `https://hackerone.com/reports/<id>.json` | public; `Accept: application/json`; no token |
| site classes | `https://hexbrainai.com/api/v1/list_classes` | key-gated; replicate the regex taxonomy locally instead |

Useful fields in the report JSON:
`title, vulnerability_information (body), summaries[].content, severity_rating, weakness.name,
bounty_amount, reporter.username, disclosed_at, submitted_at, structured_scope.{asset_identifier,
asset_type}, cve_ids[], team.handle / team.profile.name`.

## Schema (single file, FTS5 everywhere)

```sql
CREATE TABLE reports(id INTEGER PRIMARY KEY, title TEXT, program TEXT, severity TEXT,
  weakness TEXT, bounty REAL, votes INTEGER, reporter TEXT, disclosed_at TEXT, substate TEXT);
CREATE TABLE bodies(id INTEGER PRIMARY KEY, title TEXT, program TEXT, severity TEXT, weakness TEXT,
  bounty REAL, reporter TEXT, disclosed_at TEXT, submitted_at TEXT, asset TEXT, asset_type TEXT,
  cve_ids TEXT, summary TEXT, body TEXT, fetched_at TEXT, http_status INTEGER, size INTEGER);
CREATE TABLE documents(id INTEGER PRIMARY KEY AUTOINCREMENT, path TEXT UNIQUE, dir TEXT, name TEXT,
  title TEXT, type TEXT, category TEXT, cwe TEXT, bytes INTEGER, lines INTEGER, sha256 TEXT,
  ingested_at TEXT, text TEXT);
CREATE TABLE chunks(id INTEGER PRIMARY KEY AUTOINCREMENT, kind TEXT, report_id INTEGER, path TEXT,
  heading TEXT, text TEXT, chars INTEGER, sha256 TEXT, model TEXT, dim INTEGER, vec BLOB,
  built_at TEXT, UNIQUE(kind, report_id, path, sha256));
CREATE VIRTUAL TABLE reports_fts USING fts5(title, program_name, weakness, summary, body,
  content='reports', content_rowid='id', tokenize='porter unicode61');
-- same trigger trio for each fts table; chunks_fts over (heading, text)
```
Backup/mirror into the vault with `VACUUM INTO '<dest>'` (fails if dest exists — delete first).

## Crawler shape that held

```
4 threads, sleep 0.35 + jitter 0.4
on 429/403: sleep(min(60, max(5, Retry-After or 12))) , retry up to 3
on 404/410: store status, never retry again
commit every ~20 rows; print ok/fail/left every 20
resume: set difference reports.id − bodies.id, ordered by votes DESC (best first)
```

Watchdog (bash, background):
```
while true; do
  pgrep -f 'python3 harvest_bodies' >/dev/null || restart_if_rows_remain
  snapshot >> watchdog.log        # counts from sqlite, plus tail -1 of crawler log
  sleep 900
done
```
Note: `pgrep -f` inside the watchdog can match its own command string — confirm with
`ps -o pid,ppid,cmd` before concluding a duplicate crawler exists.

## Measured throughput (8-core CPU, 15 GB, no GPU)

- crawler: 2.0–2.6 req/s sustained; 15,244 ids ≈ 95 min; 8 concurrent → 429 storm.
- embeddings: Ollama embeddinggemma 0.2–0.7/s · nomic-embed-text 0.3–0.4/s ·
  fastembed bge-small 3.5/s · fastembed MiniLM-L6 15/s (chosen).
- chunking at 2.4k chars: 24.3 MB of bodies + 9.7 MB of docs → 27,407 chunks.
  Embedding at 15/s ≈ 30 min; at 0.5/s ≈ 15 h (i.e. the model choice is the whole schedule).

## Hybrid retrieval

```
bm25  : chunks_fts MATCH "term" OR "term" ... ORDER BY bm25(chunks_fts) LIMIT 80
vector: fastembed(query) · normalised matrix (cache .npy) → top 200 → filter → 80
fuse  : score += 1/(60 + rank) for each leg
pack  : dedupe by report_id, 5–8 passages, ≤8k chars, wrap in <<<EVIDENCE … EVIDENCE>>>
```
Filters in SQL: `program LIKE`, `severity =`, `bounty >=`, `substr(disclosed_at,1,4) =`, class →
LIKE pattern list (no REGEXP in stock sqlite).

## MCP server (stdio, no SDK needed)

Newline-delimited JSON-RPC. Handle `initialize` (return protocolVersion 2024-11-05, capabilities
`{tools:{}}`, serverInfo), `notifications/initialized` (no reply), `tools/list`, `tools/call`,
`ping`. Tool result shape: `{"content":[{"type":"text","text":...}],"isError":false}`.

Register:
```bash
printf 'y\n' | hermes mcp add vault --command <venv>/bin/python --args <path>/mcp_server.py
hermes mcp list
```
A bare `hermes mcp add` opens an "Enable all N tools?" prompt and prints `Cancelled.` if stdin
isn't a yes — pipe `y`.

## Audit checklist (run before saying "done")

1. `PRAGMA integrity_check` = ok; no duplicate ids; bodies rows == reports rows.
2. full + summary_only + 404 + other == total.
3. csv rows == db rows; csv paid == db paid; bounty sums equal within 1; id sets identical.
4. class views and category views each sum to total; no empty view file.
5. README frontmatter numbers == db; availability table == db.
6. every playbook README carries the case-stock markers.
7. `documents` sha256 == file sha256 for all rows (proves text is really stored).
8. `extract_report.py` works on a full body AND labels a summary-only row as "body not public".
