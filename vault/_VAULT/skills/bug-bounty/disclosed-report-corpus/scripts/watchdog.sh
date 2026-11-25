#!/usr/bin/env bash
# Watchdog for the HackerOne write-up crawl: keeps it alive, snapshots real progress every 15 min.
# Every number comes from SQLite — this script never estimates and never invents.
#   usage: bash watchdog.sh            (background it; log goes to watchdog.log)
#   stop:  pkill -f watchdog.sh       (do this once remaining = 0, before exporting)
set -u
cd "$(dirname "$0")/.." || exit 1
LOG=watchdog.log
PATTERN="python3 harvest_bodies.py"

snapshot() {
  {
    echo "=== $(date -u +%FT%TZ) ==="
    pgrep -f "$PATTERN" >/dev/null && echo "crawler: RUNNING" || echo "crawler: STOPPED"
    sqlite3 hexbrain_reports.sqlite \
      "SELECT 'meta_total='||COUNT(*) FROM reports;
       SELECT 'bodies_ok='||COALESCE(SUM(http_status=200),0) FROM bodies;
       SELECT 'bodies_404='||COALESCE(SUM(http_status=404),0) FROM bodies;
       SELECT 'bodies_other='||COALESCE(SUM(http_status NOT IN (200,404)),0) FROM bodies;
       SELECT 'full_writeups='||COALESCE(SUM(http_status=200 AND length(body)>0),0) FROM bodies;
       SELECT 'summary_only='||COALESCE(SUM(http_status=200 AND (body IS NULL OR body='')),0) FROM bodies;
       SELECT 'body_bytes='||COALESCE(SUM(size),0) FROM bodies WHERE http_status=200;
       SELECT 'remaining='||((SELECT COUNT(*) FROM reports)-(SELECT COUNT(*) FROM bodies));"
    tail -1 bodies.log 2>/dev/null
  } >> "$LOG"
}

while true; do
  if ! pgrep -f "$PATTERN" >/dev/null; then
    remaining=$(sqlite3 hexbrain_reports.sqlite \
      "SELECT (SELECT COUNT(*) FROM reports)-(SELECT COUNT(*) FROM bodies);")
    if [ "${remaining:-0}" -gt 0 ]; then
      echo "$(date -u +%FT%TZ) watchdog: restarting crawler, remaining=$remaining" >> "$LOG"
      WORKERS=4 DELAY=0.35 nohup python3 harvest_bodies.py >> bodies.log 2>&1 &
      sleep 20
    fi
  fi
  snapshot
  sleep 900          # 15-minute cadence, matches the operator's reporting expectation
done
