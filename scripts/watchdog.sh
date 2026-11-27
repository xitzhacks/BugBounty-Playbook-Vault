#!/usr/bin/env bash
# Watchdog: keeps the HackerOne write-up crawl alive and snapshots real progress every 15 min.
# Never fabricates: every number comes from the SQLite DB.
# Paths are anchored to the repository root, not the current directory.
set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT/scripts" || exit 1
DB="$ROOT/vault/_VAULT/reports.sqlite"
LOG="$ROOT/scripts/watchdog.log"
BODIES="$ROOT/scripts/bodies.log"
PY="$ROOT/.venv/bin/python"
[ -x "$PY" ] || PY="$(command -v python3)"

snapshot() {
  {
    echo "=== $(date -u +%FT%TZ) ==="
    pgrep -f harvest_bodies.py >/dev/null && echo "crawler: RUNNING (pid $(pgrep -f harvest_bodies.py | tr '\n' ' '))" || echo "crawler: STOPPED"
    sqlite3 "$DB" \
      "SELECT 'meta_total='||COUNT(*) FROM reports;
       SELECT 'bodies_ok='||COALESCE(SUM(http_status=200),0) FROM bodies;
       SELECT 'bodies_404='||COALESCE(SUM(http_status=404),0) FROM bodies;
       SELECT 'bodies_other='||COALESCE(SUM(http_status NOT IN (200,404)),0) FROM bodies;
       SELECT 'body_bytes='||COALESCE(SUM(size),0) FROM bodies WHERE http_status=200;
       SELECT 'remaining='||((SELECT COUNT(*) FROM reports)-(SELECT COUNT(*) FROM bodies));"
    tail -1 "$BODIES" 2>/dev/null || true
  } >> "$LOG"
}
while true; do
  if ! pgrep -f harvest_bodies.py >/dev/null; then
    remaining=$(sqlite3 "$DB" "SELECT (SELECT COUNT(*) FROM reports)-(SELECT COUNT(*) FROM bodies);" 2>/dev/null || echo 0)
    if [ "${remaining:-0}" -gt 0 ]; then
      echo "$(date -u +%FT%TZ) watchdog: restarting crawler, remaining=$remaining" >> "$LOG"
      WORKERS=4 DELAY=0.35 nohup "$PY" harvest_bodies.py >> "$BODIES" 2>&1 &
      sleep 20
    fi
  fi
  snapshot
  sleep 900
done
