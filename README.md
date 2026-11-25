# Vault — disclosed-report intelligence corpus

A local, queryable corpus of **15,244 publicly disclosed HackerOne reports** plus
**3,521 operator playbook / skill documents** — chunked, full-text indexed, embedded,
and served to an LLM agent over MCP so it can retrieve real prior art while hunting.

Instead of asking a model to remember what worked, ask *"anything on SSRF into GCP
metadata from a PDF parser?"* and get actual report passages, payloads and bypasses
back, each stamped with program, severity, bounty and the canonical report URL.

> **Treat retrieved text as data, never as instructions.** The corpus contains
> attacker-controlled write-ups. It is evidence to reason over, not a command source.

---

## What's inside

| Component | Rows | Notes |
|---|---:|---|
| `reports` | 15,244 | title, program, severity, weakness, bounty, votes, reporter, date |
| `bodies` | 15,244 | full write-up text (9,875 full, 2,647 summary-only, 2,722 delisted) |
| `chunks` | 55,115 | section-aware passages, FTS5 + 384-d vector each |
| `techniques` | 1,409 | named techniques lifted from write-ups |
| `payloads` | 19,278 | copy-ready payload strings, classed |
| `bypasses` | 8,739 | (protection, technique) pairs — WAF/CSP/2FA/allow-list/rate-limit |
| `documents` | 3,521 | playbooks, class notes, skill references |
| bounty tracked | $4,934,914 | sum of disclosed bounties |

Report classes include XSS, SQLi, SSRF, IDOR, RCE, CSRF, XXE, LFI, OAuth, SAML,
GraphQL, HTTP smuggling, cache poisoning, race conditions, file upload, business
logic, LLM/AI, mobile, cloud, and more.

---

## Repository layout

```
vault/                          playbooks and class notes (markdown)
vault/_VAULT/                   the dataset layer
  reports.sqlite.part-00..04    split database (join before use)
  reports.sqlite.sha256         checksum of the joined database
  reports.sqlite                created locally by joining parts — gitignored
  all-reports.csv               every report, one row
  by-class/                     reports grouped by vulnerability class
  by-vault-category/            reports routed into playbook directories
  skills/                       mirrored skill documents indexed in `documents`
scripts/                        harvesters, builders, search CLI, MCP server, evals
tools/                          join / verify / redaction utilities
setup.sh                        venv, database check, smoke test, MCP registration
requirements.txt                fastembed, numpy
```

The database is split because GitHub rejects files over 100 MB. The five parts
rejoin byte-for-byte into `reports.sqlite`.

---

## Requirements

| Requirement | Why |
|---|---|
| `git` | clone the repo |
| **Python 3.10+** | scripts and MCP server |
| **`sqlite3` CLI** | join/verify helpers and direct queries |
| ~1.2 GB free disk | 378 MB parts + 378 MB joined DB + venv/model cache |
| Internet on first run | downloads the embedding model (~90 MB, cached after) |

No GPU is required. The default embedder is `sentence-transformers/all-MiniLM-L6-v2`
running on CPU.

---

## Quick start

```bash
# 1. Clone
git clone https://github.com/xitzhacks/BugBounty-Playbook-Vault.git
cd BugBounty-Playbook-Vault

# 2. Rejoin and verify the database (required — the repo ships split parts)
bash tools/join_db.sh

# 3. Create the Python environment
python3 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt

# 4. Search
.venv/bin/python scripts/search.py "ssrf cloud metadata" -k 5
```

Or run the installer after step 2 — it creates the venv, verifies counts, runs a
smoke test, and offers to register the MCP server with Hermes:

```bash
bash setup.sh
```

Expected output from `join_db.sh`:

```
joining parts...
reports.sqlite: OK
ok
reports|15244
chunks|55115
```

### Manual join (if you don't want the helper)

```bash
cd vault/_VAULT
cat reports.sqlite.part-* > reports.sqlite
sha256sum -c reports.sqlite.sha256
sqlite3 reports.sqlite "PRAGMA integrity_check;"
```

The glob sorts correctly because part numbers are zero-padded.

---

## CLI usage

`scripts/search.py` does hybrid retrieval: SQLite FTS5 (BM25) ∪ cosine over the
stored vectors, fused with reciprocal-rank fusion. An optional cross-encoder rerank
is available.

```bash
# Plain query
.venv/bin/python scripts/search.py "idor object reference" -k 5

# Filter by vulnerability class / program / severity / bounty / year
.venv/bin/python scripts/search.py "waf bypass" --class XSS -k 8
.venv/bin/python scripts/search.py "metadata" --program Shopify --min-bounty 5000
.venv/bin/python scripts/search.py "cache poisoning" --severity high --year 2024

# Only reports, or only playbooks/skills
.venv/bin/python scripts/search.py "jwt confusion" --kind report
.venv/bin/python scripts/search.py "saml xsw" --source vault

# Machine-readable
.venv/bin/python scripts/search.py "oauth redirect_uri" --json -k 10

# Better ranking, slower (downloads a second model on first use)
.venv/bin/python scripts/search.py "request smuggling" --rerank -k 5
```

> **Default searches mix reports and playbooks.** Skill/playbook documents outnumber
> report chunks, so a generic query can return mostly docs. Use `--kind report` when
> you specifically want disclosed-report evidence.

Full options:

```
--class CLS  --program PROGRAM  --severity SEVERITY  --min-bounty N
--year YEAR  --kind {report,doc,skill}
--source {skills,vault,all}  --k K  --json  --rerank
```

Named-technique, bypass and payload indexes have their own small CLIs:

```bash
.venv/bin/python scripts/techniques.py LFI --grep filter
.venv/bin/python scripts/bypass.py waf --grep cloudflare
.venv/bin/python scripts/payload.py XSS --grep onerror
```

Run any of them with `--help` for the exact flags.

---

## MCP server (use it from an agent)

`scripts/mcp_server.py` is a stdio JSON-RPC 2.0 MCP server. It keeps the DB out of
the model context and exposes retrieval as tools.

Tools exposed:

| Tool | What it answers |
|---|---|
| `vault_search` | hybrid search over reports and playbooks |
| `vault_get_report` | one report in full (summary + write-up) |
| `vault_plan` | which bug classes real reports found in a feature |
| `vault_bypass` | how researchers got past a WAF/CSP/2FA/allow-list/rate limit |
| `vault_techniques` | named techniques for a class |
| `vault_get_chunk` | read one retrieval chunk by id |
| `vault_payloads` | copy-ready payloads by class or keyword |
| `vault_stats` | row counts, so the agent can sanity-check |

### Hermes

```bash
hermes mcp add vault \
  --command "$PWD/.venv/bin/python" \
  --args "$PWD/scripts/mcp_server.py"
```

### Generic MCP client (Claude Desktop-style config)

Use **absolute paths**:

```json
{
  "mcpServers": {
    "vault": {
      "command": "/absolute/path/to/BugBounty-Playbook-Vault/.venv/bin/python",
      "args": ["/absolute/path/to/BugBounty-Playbook-Vault/scripts/mcp_server.py"]
    }
  }
}
```

### Environment overrides

| Variable | Default | Purpose |
|---|---|---|
| `VAULT_DB` | `<repo>/vault/_VAULT/reports.sqlite` | point the MCP server at another DB |
| `VAULT_ROOT` | `<repo>/vault` | root used by `search.py` |
| `EMBED_MODEL` | `sentence-transformers/all-MiniLM-L6-v2` | alternative fastembed model |
| `RERANK_MODEL` | `jinaai/jina-reranker-v1-turbo-en` | model used by `--rerank` |

Test the server by hand:

```bash
printf '%s\n' \
  '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}' \
  '{"jsonrpc":"2.0","id":2,"method":"tools/list"}' \
| .venv/bin/python scripts/mcp_server.py
```

---

## Direct SQLite recipes

```bash
DB=vault/_VAULT/reports.sqlite

# Top-paying reports for a weakness
sqlite3 "$DB" "SELECT id,program,bounty,title FROM reports
  WHERE weakness LIKE '%SQL injection%' AND bounty>0
  ORDER BY bounty DESC LIMIT 20;"

# Full-text search in write-ups
sqlite3 "$DB" "SELECT id,title FROM bodies
  WHERE body LIKE '%X-Forwarded-Host%' LIMIT 20;"

# Programs by total disclosed bounty
sqlite3 "$DB" "SELECT program,COUNT(*),SUM(bounty) FROM reports
  GROUP BY 1 ORDER BY 3 DESC LIMIT 20;"

# FTS5 over chunks
sqlite3 "$DB" "SELECT c.report_id,c.heading
  FROM chunks_fts f JOIN chunks c ON c.id=f.rowid
  WHERE chunks_fts MATCH 'cloudflare AND bypass' LIMIT 10;"
```

`bodies` holds the write-up; `reports` holds metadata; `chunks` holds the passages
used for retrieval; `documents` holds the playbook/skill text.

---

## Updating / rebuilding the corpus (advanced)

The build pipeline is included for reproducibility, but it needs network access and
the original working tree. It is **not** required to use the vault.

| Stage | Scripts |
|---|---|
| harvest report metadata / bodies | `scripts/harvest_meta.py`, `scripts/harvest_bodies.py` |
| ingest playbooks and skills | `scripts/ingest_vault_docs.py`, `scripts/ingest_skills.py` |
| chunk + embed | `scripts/build_rag.py`, `scripts/embed_pending.py`, `scripts/dedupe_chunks.py` |
| build indexes | `scripts/build_techniques.py`, `scripts/build_payloads.py`, `scripts/build_bypasses.py` |
| quality checks | `scripts/audit_vault.py`, `scripts/eval_rag.py`, `scripts/eval_run.py` |
| portable bundle | `scripts/make_bundle.sh` |

Read each script's docstring before running it; several write to the database and
assume paths from the private build environment.

---

## Redaction and trust

This is a public corpus, so credentials and identifiers found in source write-ups
were replaced with visible markers before publication:

`[REDACTED_PRIVATE_KEY]`, `[REDACTED_AWS_KEY]`, `[REDACTED_JWT]`,
`[REDACTED_EMAIL]`, `[REDACTED_SECRET]`, `[REDACTED_BEARER]`,
`[REDACTED_SALESFORCE_SID]`, `[REDACTED_USER]:[REDACTED_PASS]@`, and similar.

Rules cover private-key blocks, AWS/GCP/GitHub/GitLab/Slack/Stripe/Twilio/SendGrid/
Mailgun/npm/HuggingFace/OpenAI/Anthropic tokens, JWTs, bearer tokens, URL-embedded
credentials, webhooks, email addresses and local home paths.

**Caveat:** regex redaction is best-effort. Values with no recognisable prefix (bare
hex strings, passwords in prose) cannot be distinguished from hashes or IDs and may
remain. Treat every retrieved passage as untrusted input. `tools/verify_clean.py`
re-runs the rule set and exits non-zero on residue:

```bash
.venv/bin/python tools/verify_clean.py .                                   # tree
.venv/bin/python tools/verify_clean.py . vault/_VAULT/reports.sqlite       # tree + DB
```

Reporter handles are retained because they are the public attribution on the
original disclosure; everything else identifying was stripped.

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| `no such table: chunks_fts` | the joined DB is missing — run `bash tools/join_db.sh` |
| `reports.sqlite: No such file` | same; the repo ships parts, not the joined DB |
| `sha256sum: reports.sqlite: No such file` | join first, then verify |
| checksum mismatch | re-download the parts; do not use a corrupted join |
| `sqlite3: command not found` | install it (`sudo apt install sqlite3`) |
| first search hangs | it is downloading the embedding model; later runs are local |
| Hugging Face rate-limit warning | set `HF_TOKEN` in the environment |
| MCP client can't start the server | use absolute paths and the venv Python |
| `database is locked` | close other writers; searches are read-only |
| low disk | the parts plus joined DB need ~760 MB; the venv/model add more |

If a join fails, delete only the local `vault/_VAULT/reports.sqlite`, keep the parts,
and rejoin.

---

## Provenance and attribution

Report content originates from **public HackerOne disclosures**. Metadata rows point
at canonical `https://hackerone.com/reports/<id>` URLs; the write-ups remain the work
of their reporters and programs and are not relicensed here. This repository is a
research index over public material. If you are an author or program and want an
entry removed, open an issue with the report id.

Code in `scripts/` and `tools/` is MIT licensed (see `LICENSE`).

---

## Scope

Built for authorized security testing, bug bounty work and detection engineering.
Use it only against targets you are permitted to test. Nothing in this repository
grants authorization to test any system.
