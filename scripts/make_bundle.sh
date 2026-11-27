#!/usr/bin/env bash
# Build a portable vault bundle for moving to a VPS.
set -euo pipefail
SRC_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC_VAULT="$SRC_ROOT/vault"
SRC_SCRIPTS="$SRC_ROOT/scripts"
OUTDIR="${VAULT_EXPORT_DIR:-$HOME/vault-export}"
mkdir -p "$OUTDIR"
STAGE="$OUTDIR/vault-$(date +%Y%m%d)"
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
cp "$SRC_SCRIPTS"/*.py "$SRC_SCRIPTS"/*.sh "$STAGE/scripts/" 2>/dev/null || true
mkdir -p "$STAGE/scripts/eval"; cp "$SRC_SCRIPTS"/eval/*.jsonl "$STAGE/scripts/eval/" 2>/dev/null || true

echo "[4/6] writing requirements + installer"
cat > "$STAGE/requirements.txt" <<'EOF'
fastembed>=0.9.1
numpy>=2.0
EOF

# Ship the same installer the repository uses — no second copy to drift out of sync.
cp "$SRC_ROOT/setup.sh" "$STAGE/setup.sh"
chmod +x "$STAGE/setup.sh"

echo "[5/6] manifest"
( cd "$STAGE"
  python3 - <<'PY' > /tmp/vault-bundle-files.txt
import os
rows = []
for dp, dn, fn in os.walk("."):
    dn[:] = [d for d in dn if d not in (".git", ".venv", "__pycache__")]
    for f in fn:
        if f == "MANIFEST.txt":
            continue
        p = os.path.join(dp, f)
        rows.append((p, os.path.getsize(p)))
for p, size in sorted(rows):
    print(size, p)
PY
  echo "# vault bundle manifest (size bytes, path)" > MANIFEST.txt
  cat /tmp/vault-bundle-files.txt >> MANIFEST.txt
  echo >> MANIFEST.txt
  echo "# sha256 of the database" >> MANIFEST.txt
  sha256sum vault/_VAULT/reports.sqlite >> MANIFEST.txt )

echo "[6/6] zip"
cd "$OUTDIR"
rm -f "$NAME.zip"
zip -q -r -9 "$NAME.zip" "$(basename "$STAGE")" >/dev/null
ls -lh "$NAME.zip"
sha256sum "$NAME.zip" > "$NAME.zip.sha256"
cat "$NAME.zip.sha256"
echo
echo "bundle: $OUTDIR/$NAME.zip"
du -sh "$STAGE"
