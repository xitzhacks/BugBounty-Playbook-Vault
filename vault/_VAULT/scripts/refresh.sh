#!/usr/bin/env bash
# Refresh the dataset layer: metadata -> write-ups -> vault views.
# All paths are relative to the repository root, never the build host's home.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
SCRIPTS="$ROOT/scripts"
PY="$ROOT/.venv/bin/python"
[ -x "$PY" ] || PY="$(command -v python3)"

cd "$SCRIPTS"
"$PY" harvest_meta.py
"$PY" harvest_bodies.py          # resumable; only fetches what is missing
"$PY" export_to_vault.py
"$PY" ingest_vault_docs.py       # index every vault .md into the same DB
"$PY" ingest_skills.py           # needs VAULT_SKILLS_SRC or a source directory argument
"$PY" dedupe_chunks.py           # exact + near-duplicate chunk removal (tombstoned)
"$PY" build_techniques.py        # named-technique index (class -> technique -> chunk)
"$PY" build_bypasses.py          # protection -> passage -> payload index
"$PY" build_payloads.py          # fenced code blocks -> classified payload table
