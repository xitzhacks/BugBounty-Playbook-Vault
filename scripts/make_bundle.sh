#!/usr/bin/env bash
# Build a portable vault bundle for moving to a VPS.
set -euo pipefail
SRC_VAULT="$(cd "$(dirname "$0")/.." && pwd)/vault"
SRC_SCRIPTS="$(cd "$(dirname "$0")" && pwd)"
STAGE="$HOME/vault-export/vault-$(date +%Y%m%d)"
NAME="vault-bundle-$(date +%Y%m%d)"

rm -rf "$STAGE"; mkdir -p "$STAGE/scripts"

echo "[1/6] copying playbooks + dataset (excluding venv/caches)"
rsync -a --exclude '__pycache__' --exclude '*.pyc' --exclude '.venv' \
      --exclude '_VAULT/reports.sqlite' \
      "$SRC_VAULT/" "$STAGE/vault/"

echo "[2/6] consistent DB snapshot (VACUUM INTO, no WAL sidecars)"
sqlite3 "$SRC_VAULT/_VAULT/reports.sqlite" "PRAGMA wal_checkpoint(TRUNCATE);" >/dev/null
sqlite3 "$SRC_VAULT/_VAULT/reports.sqlite" "VACUUM INTO '$STAGE/vault/_VAULT/reports.sqlite'"
sqlite3 "$STAGE/vault/_VAULT/reports.sqlite" "PRAGMA integrity_check;" | sed 's/^/      integrity: /'

echo "[3/6] copying scripts"
cp "$SRC_SCRIPTS"/*.py "$SRC_SCRIPTS"/*.sh "$SRC_SCRIPTS"/eval/questions.jsonl "$STAGE/scripts/" 2>/dev/null || true
mkdir -p "$STAGE/scripts/eval"; cp "$SRC_SCRIPTS"/eval/*.jsonl "$STAGE/scripts/eval/" 2>/dev/null || true

echo "[4/6] writing requirements + installer"
cat > "$STAGE/requirements.txt" <<'EOF'
fastembed>=0.9.1
numpy>=2.0
EOF

cat > "$STAGE/setup.sh" <<'EOF'
#!/usr/bin/env bash
# VPS install: python deps, verify DB, register the MCP server with Hermes.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
VAULT="$HERE/vault"
DB="$VAULT/_VAULT/reports.sqlite"

echo "== python env =="
python3 -m venv "$HERE/.venv"
"$HERE/.venv/bin/pip" install --quiet --upgrade pip
"$HERE/.venv/bin/pip" install --quiet -r "$HERE/requirements.txt"
echo "   installed: $("$HERE/.venv/bin/python" -c 'import fastembed,numpy;print("fastembed",fastembed.__version__,"numpy",numpy.__version__)')"

echo "== database =="
sqlite3 "$DB" "PRAGMA integrity_check;"
sqlite3 "$DB" "select 'reports='||count(*) from reports; select 'chunks='||count(*) from chunks; select 'techniques='||count(*) from techniques; select 'bypasses='||count(*) from bypasses; select 'payloads='||count(*) from payloads;"

echo "== paths in scripts point at Kali's home; fix them for this box =="

echo "== smoke test =="
"$HERE/.venv/bin/python" "$HERE/scripts/search.py" "ssrf cloud metadata" -k 2 | head -6

echo
echo "== register with Hermes (MCP) =="
printf 'y\n' | hermes mcp add vault --command "$HERE/.venv/bin/python" --args "$HERE/scripts/mcp_server.py" || \
  echo "   run manually: hermes mcp add vault --command $HERE/.venv/bin/python --args $HERE/scripts/mcp_server.py"

echo
echo "Done. Tools: vault_search, vault_get_report, vault_plan, vault_bypass, vault_techniques, vault_get_chunk, vault_payloads, vault_stats"
EOF
chmod +x "$STAGE/setup.sh"

echo "[5/6] manifest"
( cd "$STAGE" && find . -type f ! -name MANIFEST.txt -printf '%s %p\n' | sort -k2 > /tmp/vfiles.txt
  echo "# vault bundle manifest (size bytes, path)" > MANIFEST.txt
  cat /tmp/vfiles.txt >> MANIFEST.txt
  echo >> MANIFEST.txt
  echo "# sha256 of the database" >> MANIFEST.txt
  sha256sum vault/_VAULT/reports.sqlite >> MANIFEST.txt )

echo "[6/6] zip"
cd "$HOME/vault-export"
rm -f "$NAME.zip"
zip -q -r -9 "$NAME.zip" "$(basename "$STAGE")" >/dev/null
ls -lh "$NAME.zip"
sha256sum "$NAME.zip" > "$NAME.zip.sha256"
cat "$NAME.zip.sha256"
echo
echo "bundle: $HOME/vault-export/$NAME.zip"
du -sh "$STAGE"
