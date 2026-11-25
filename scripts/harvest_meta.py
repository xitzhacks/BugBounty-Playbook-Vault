#!/usr/bin/env python3
"""Harvest all disclosed-report metadata from the public the public HackerOne dataset /api/reports endpoint."""
import json, time, sys, sqlite3, os, urllib.request, urllib.error

BASE = "https://the public HackerOne dataset/api/reports"
OUT = os.path.dirname(os.path.abspath(__file__))
JSONL = os.path.join(OUT, "reports.jsonl")
DB = os.environ.get("VAULT_DB", os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "vault", "_VAULT", "reports.sqlite"))   # one canonical DB, one place

def get(url, tries=4):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "vault-harvest/1.0", "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=40) as r:
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            body = e.read()[:300].decode(errors="replace")
            print(f"HTTP {e.code} {body}", flush=True)
            if e.code == 429:
                time.sleep(65); continue
            time.sleep(3 + i * 3)
        except Exception as e:
            print("ERR", e, flush=True); time.sleep(3 + i * 3)
    return None

def main():
    first = get(BASE + "?limit=100&offset=0")
    if not first:
        sys.exit("first page failed")
    total = first["total"]
    print("total reports:", total, flush=True)
    rows = first["rows"]
    seen = {r["id"] for r in rows}
    offset = 100
    while offset < total:
        d = get(f"{BASE}?limit=100&offset={offset}")
        if not d:
            print("page failed at", offset, flush=True); time.sleep(10); continue
        new = [r for r in d["rows"] if r["id"] not in seen]
        for r in new:
            seen.add(r["id"]); rows.append(r)
        offset += 100
        print(f"{offset}/{total} ({len(rows)} unique)", flush=True)
        time.sleep(0.2)
    with open(JSONL, "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    con = sqlite3.connect(DB)
    con.execute("""CREATE TABLE IF NOT EXISTS reports(id INTEGER PRIMARY KEY,title TEXT,program TEXT,severity TEXT,
        weakness TEXT,bounty REAL,votes INTEGER,reporter TEXT,disclosed_at TEXT,substate TEXT)""")
    con.execute("DELETE FROM reports")
    con.executemany("INSERT OR REPLACE INTO reports VALUES (?,?,?,?,?,?,?,?,?,?)",
        [(r.get("id"),r.get("title"),r.get("program"),r.get("severity"),r.get("weakness"),r.get("bounty"),
          r.get("votes"),r.get("reporter"),r.get("disclosed_at"),r.get("substate")) for r in rows])
    con.commit()
    print("written", len(rows), "rows ->", JSONL, DB, flush=True)

main()
