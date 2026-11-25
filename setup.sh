#!/usr/bin/env bash
# VPS install: python deps, verify DB, register the MCP server with Hermes.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
VAULT="$HERE/vault"
DB="$VAULT/_VAULT/reports.sqlite"

command -v sqlite3 >/dev/null 2>&1 || {
  echo "sqlite3 CLI is required (e.g. sudo apt install sqlite3)" >&2
  exit 1
}

echo "== python env =="
python3 -m venv "$HERE/.venv"
"$HERE/.venv/bin/pip" install --quiet --upgrade pip
"$HERE/.venv/bin/pip" install --quiet -r "$HERE/requirements.txt"
echo "   installed: $("$HERE/.venv/bin/python" -c 'import fastembed,numpy;print("fastembed",fastembed.__version__,"numpy",numpy.__version__)')"

echo "== database =="
bash "$HERE/tools/join_db.sh"
[ -s "$DB" ] || { echo "database missing/empty after join" >&2; exit 1; }
sqlite3 "$DB" "PRAGMA integrity_check;"

echo "== smoke test =="
"$HERE/.venv/bin/python" "$HERE/scripts/search.py" "ssrf cloud metadata" -k 2 | sed -n '1,6p'

echo
echo "== register with Hermes (MCP) =="
printf 'y\ny\n' | hermes mcp add vault --command "$HERE/.venv/bin/python" --args "$HERE/scripts/mcp_server.py" || \
  echo "   run manually: hermes mcp add vault --command $HERE/.venv/bin/python --args $HERE/scripts/mcp_server.py"

echo
echo "Done. Tools: vault_search, vault_get_report, vault_plan, vault_bypass, vault_techniques, vault_get_chunk, vault_payloads, vault_stats"
