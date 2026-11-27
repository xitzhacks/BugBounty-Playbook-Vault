#!/usr/bin/env bash
# Install: choose a supported Python, create the venv, join/verify the DB, smoke test.
# MCP registration is opt-in: VAULT_REGISTER_MCP=1 bash setup.sh
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
VAULT="$HERE/vault"
DB="$VAULT/_VAULT/reports.sqlite"

command -v sqlite3 >/dev/null 2>&1 || {
  echo "sqlite3 CLI is required (e.g. sudo apt install sqlite3)" >&2
  exit 1
}

select_python() {
  local cand major minor ver
  if [ -n "${PYTHON:-}" ]; then
    cand="$PYTHON"
  else
    for cand in python3.13 python3.12 python3.11 python3.10 python3; do
      command -v "$cand" >/dev/null 2>&1 || continue
      ver=$("$cand" -c 'import sys; print(sys.version_info.major, sys.version_info.minor)' 2>/dev/null) || continue
      major=${ver%% *}; minor=${ver##* }
      if [ "$major" = 3 ] && [ "$minor" -ge 10 ] 2>/dev/null; then
        echo "$cand"
        return 0
      fi
    done
    echo "ERROR: Python 3.10+ is required (python3.13 preferred)." >&2
    echo "       Found: $(python3 -V 2>&1 || echo 'no python3')." >&2
    echo "       Install python3.13 or set PYTHON=/path/to/python3.13." >&2
    return 1
  fi
  if ! command -v "$cand" >/dev/null 2>&1; then
    echo "ERROR: PYTHON=$cand is not on PATH." >&2
    return 1
  fi
  ver=$("$cand" -c 'import sys; print(sys.version_info.major, sys.version_info.minor)' 2>/dev/null) || {
    echo "ERROR: PYTHON=$cand cannot run Python." >&2; return 1; }
  major=${ver%% *}; minor=${ver##* }
  if [ "$major" != 3 ] || [ "$minor" -lt 10 ]; then
    echo "ERROR: Python 3.10+ is required; PYTHON=$cand is $($cand -V 2>&1)." >&2
    return 1
  fi
  echo "$cand"
}

PY="$(select_python)"
echo "== python env: $PY =="
"$PY" -m venv "$HERE/.venv" || {
  echo "ERROR: could not create .venv — install the venv package for $PY (e.g. python3.13-venv)." >&2
  exit 1
}
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
if [ "${VAULT_REGISTER_MCP:-0}" = "1" ]; then
  echo "== registering vault MCP with Hermes =="
  if command -v hermes >/dev/null 2>&1; then
    printf 'y\ny\n' | hermes mcp add vault \
      --command "$HERE/.venv/bin/python" --args "$HERE/scripts/mcp_server.py" || \
      echo "   registration failed; use the manual command in README.md"
  else
    echo "   hermes CLI not found; use the manual command in README.md"
  fi
else
  echo "== MCP registration skipped (opt-in) =="
  echo "   To register with Hermes: VAULT_REGISTER_MCP=1 bash setup.sh"
  echo "   Or follow the MCP section in README.md."
fi

echo
echo "Done. Tools: vault_search, vault_get_report, vault_plan, vault_bypass, vault_techniques, vault_get_chunk, vault_payloads, vault_stats"
