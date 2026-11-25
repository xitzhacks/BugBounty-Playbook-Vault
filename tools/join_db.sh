#!/usr/bin/env bash
# Rejoin and verify the split reports.sqlite.
set -euo pipefail
cd "$(dirname "$0")/../vault/_VAULT"

if [ ! -s reports.sqlite ]; then
  echo "joining parts..."
  cat reports.sqlite.part-* > reports.sqlite
fi

if [ -f reports.sqlite.sha256 ]; then
  sha256sum -c reports.sqlite.sha256
fi

sqlite3 reports.sqlite "PRAGMA integrity_check;"
sqlite3 reports.sqlite "select 'reports',count(*) from reports union all select 'chunks',count(*) from chunks;"
echo "ok"
