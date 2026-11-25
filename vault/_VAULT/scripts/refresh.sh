#!/usr/bin/env bash
# Refresh the dataset layer: metadata -> write-ups -> vault views
set -e
cd ~/Bugbounty/vault
python3 harvest_meta.py
python3 harvest_bodies.py          # resumable; only fetches what is missing
python3 export_to_vault.py
python3 ingest_vault_docs.py       # index every vault .md into the same DB
python3 ingest_skills.py           # mirror + index all skills from ~/.hermes/profiles/batman/skills
python3 dedupe_chunks.py           # exact + near-duplicate chunk removal (tombstoned)
python3 build_techniques.py        # named-technique index (class -> technique -> chunk)
python3 build_bypasses.py          # protection -> passage -> payload index
python3 build_payloads.py          # fenced code blocks -> classified payload table
