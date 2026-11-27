---
title: "Building Vault — session record (2026-11-16)"
type: handoff
session_name: "Building Vault"
built: "2026-11-16"
---

# Building Vault — what this session did

Session name: **Building Vault**. Everything below is what actually ran, with the numbers the
database returned at the end.

## Objective

Take the public disclosed-report library (15,244 HackerOne reports), put it inside our playbook
vault, make every playbook point at its case stock, and index our own markdown into the same DB so
a retrieval layer can serve the main agent.

## What was built

| Step | Result |
|---|---|
| Harvest report list | 15,244 rows via the public `/api/reports` endpoint (152 pages, no key) |
| Harvest write-ups | 15,244 fetched: 9,875 full bodies, 2,647 summary-only, 2,722 delisted (404) |
| Dataset directory | `Vault/_VAULT/` — README, all-reports.csv, reports.sqlite, by-class/, by-vault-category/, scripts/ |
| Class views | 18 files, rows sum exactly 15,244 |
| Category views | 30 files, rows sum exactly 15,244 |
| Playbook wiring | 30/30 playbook READMEs carry a case-stock block (rows, paid rows, bounty total, top-5 paid) |
| Master list | `00_MASTER_CATEGORY_LIST.md` gained a CASE-STOCK DATASET LAYER section |
| Document index | 323 markdown files (9.7 MB of text) into `documents` + `documents_fts` |
| Audit | `audit_vault.py` — 41 checks, 0 failures |

## Numbers that matter

- 15,244 reports · 3,241 with a bounty figure · **$4,934,915** (exact 4,934,914.52)
- 9,875 full write-ups = 101.2 MB of researcher text · avg 10,244 bytes
- 2,647 summary-only · 2,722 delisted — recorded as such, never paraphrased
- Our own documents: 323 files, 273 hand-written playbook files + 49 generated views + 1 master list
- Older corpus (`~/tools/h1-brain/disclosed_reports.db`): 3,673 rows, 3,606 overlapping, 67 old-only
- DB now: `reports`, `bodies`, `documents`, `documents_fts` (+ chunks once the RAG build completes)

## Provenance / honesty rules kept

- Every figure is a query result, never an estimate.
- A row with no body says "body not public / not stored".
- A 404 row keeps its title and bounty from the list but its body is never quoted.
- Bounty blanks mean HackerOne showed none, not that nothing was paid.

## Naming

The dataset directory is `vault/_VAULT/`. Working scripts live in `scripts/` (run everything from the repository root):
`harvest_meta.py`, `harvest_bodies.py`, `export_to_vault.py`, `inject_case_stock.py`,
`ingest_vault_docs.py`, `audit_vault.py`, `build_rag.py`, `watchdog.sh`.

## How to pick this up later

1. `.venv/bin/python scripts/harvest_meta.py && .venv/bin/python scripts/harvest_bodies.py` — refreshes the library (resumable)
2. `.venv/bin/python scripts/export_to_vault.py && .venv/bin/python scripts/inject_case_stock.py && .venv/bin/python scripts/ingest_vault_docs.py`
3. `.venv/bin/python scripts/audit_vault.py` — must end at 0 failures before trusting anything
4. Query: `sqlite3 vault/_VAULT/reports.sqlite "SELECT ..."`
5. Pull a write-up: `python3 ../projects/FAN/Vault/_VAULT/scripts/extract_report.py <id>`

## Open items

- Retrieval layer (chunks + embeddings + hybrid search) — design in `RAG-DESIGN.md`
- Bypass library (protection → passage → payload) derived from the 9,875 bodies
- Fold the 67 old-only reports from the h1-brain corpus into `reports`
- Payload topic mirror for offline lookup
