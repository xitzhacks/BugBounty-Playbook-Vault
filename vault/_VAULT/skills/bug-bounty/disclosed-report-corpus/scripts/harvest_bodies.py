#!/usr/bin/env python3
"""Stage 2: fetch full write-ups from hackerone.com/reports/<id>.json (public, no auth).

Resumable: only ids missing from `bodies` are queued, so kill/restart is free.
Failures are stored with their http_status (404 = delisted, record and never retry).

Throughput: WORKERS=4 DELAY=0.35 sustains ~2.5 req/s. 8 workers -> ~40% 429.
On 429 honour Retry-After (10-15s). A 45-65s sleep collapses throughput; do not do that.

Run:   WORKERS=4 DELAY=0.35 python3 harvest_bodies.py
Env:   LIMIT=n to cap the batch, WORKERS, DELAY
"""
import json, time, os, sqlite3, random, threading, queue, urllib.request, urllib.error

OUT = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(OUT, "hexbrain_reports.sqlite")
WORKERS = int(os.environ.get("WORKERS", "4"))
DELAY = float(os.environ.get("DELAY", "0.35"))
LIMIT = int(os.environ.get("LIMIT", "0"))

con = sqlite3.connect(DB, check_same_thread=False, timeout=60)
con.execute("PRAGMA journal_mode=WAL")
con.executescript("""
CREATE TABLE IF NOT EXISTS bodies(
  id INTEGER PRIMARY KEY, title TEXT, program TEXT, severity TEXT, weakness TEXT, bounty REAL,
  reporter TEXT, disclosed_at TEXT, submitted_at TEXT, asset TEXT, asset_type TEXT, cve_ids TEXT,
  summary TEXT, body TEXT, fetched_at TEXT, http_status INTEGER, size INTEGER);
CREATE INDEX IF NOT EXISTS bodies_status ON bodies(http_status);
""")
con.commit()
lock = threading.Lock()


def fetch(rid):
    url = f"https://hackerone.com/reports/{rid}.json"
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": "hexbrain/0.1"})
            with urllib.request.urlopen(req, timeout=25) as r:
                return r.status, r.read()
        except urllib.error.HTTPError as e:
            if e.code in (404, 410):
                return e.code, b""
            if e.code in (403, 429):
                ra = e.headers.get("Retry-After") if getattr(e, "headers", None) else None
                try:
                    wait = float(ra) if ra else 12
                except Exception:
                    wait = 12
                time.sleep(min(60, max(5, wait)) + random.random() * 3)
                continue
            time.sleep(5 * (attempt + 1))
        except Exception:
            time.sleep(4 * (attempt + 1))
    return 0, b""


def worker(q, c):
    while True:
        try:
            rid = q.get_nowait()
        except queue.Empty:
            return
        try:
            st, raw = fetch(rid)
            with lock:
                if st == 200 and raw:
                    try:
                        j = json.loads(raw.decode("utf-8"))
                    except Exception:
                        j = None
                    if j:
                        sc = j.get("structured_scope") or {}
                        summary = "\n\n".join(x.get("content", "") for x in (j.get("summaries") or []) if x.get("content")) or None
                        con.execute("""INSERT OR REPLACE INTO bodies(id,title,program,severity,weakness,bounty,reporter,
                            disclosed_at,submitted_at,asset,asset_type,cve_ids,summary,body,fetched_at,http_status,size)
                            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                                    (rid, j.get("title"),
                                     (j.get("team") or {}).get("profile", {}).get("name") or (j.get("team") or {}).get("handle"),
                                     j.get("severity_rating"), (j.get("weakness") or {}).get("name"), j.get("bounty_amount"),
                                     (j.get("reporter") or {}).get("username"), j.get("disclosed_at"), j.get("submitted_at"),
                                     sc.get("asset_identifier"), sc.get("asset_type"), json.dumps(j.get("cve_ids") or []),
                                     summary, j.get("vulnerability_information"),
                                     time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), 200, len(raw)))
                        c["ok"] += 1
                    else:
                        c["bad"] += 1
                else:
                    con.execute("INSERT OR REPLACE INTO bodies(id,fetched_at,http_status,size) VALUES (?,?,?,?)",
                                (rid, time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), st, 0))
                    c["fail"] += 1
                if (c["ok"] + c["fail"] + c["bad"]) % 20 == 0:
                    con.commit()
                    print(f"ok={c['ok']} fail={c['fail']} bad={c['bad']} left={q.qsize()}", flush=True)
            time.sleep(DELAY + random.random() * 0.4)
        finally:
            q.task_done()


def main():
    have = {r[0] for r in con.execute("SELECT id FROM bodies")}
    todo = [r[0] for r in con.execute("SELECT id FROM reports ORDER BY votes DESC") if r[0] not in have]
    if LIMIT:
        todo = todo[:LIMIT]
    print(f"todo={len(todo)} already={len(have)}", flush=True)
    q = queue.Queue()
    for rid in todo:
        q.put(rid)
    c = {"ok": 0, "fail": 0, "bad": 0}
    ts = [threading.Thread(target=worker, args=(q, c), daemon=True) for _ in range(WORKERS)]
    [t.start() for t in ts]
    [t.join() for t in ts]
    con.commit()
    print(f"DONE ok={c['ok']} fail={c['fail']} bad={c['bad']}", flush=True)


main()
