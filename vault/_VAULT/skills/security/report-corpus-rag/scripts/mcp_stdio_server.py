#!/usr/bin/env python3
"""Minimal MCP (stdio, JSON-RPC 2.0) server template over a report-corpus SQLite file.

Register with Hermes (the add command prompts on stdin):
  printf 'y\\n' | hermes mcp add corpus --command /path/.venv/bin/python --args /path/mcp_stdio_server.py
  hermes mcp list          # expect: corpus  ✓ enabled
Tools only appear in a NEW session.

Design rules baked in:
  - every passage is wrapped in <<<EVIDENCE ... EVIDENCE>>>: write-ups contain attacker payloads and
    sometimes instruction-shaped text; the main model must treat the block as data, never commands;
  - one hard cap per call (~8k chars) so a tool call can never flood the context;
  - every hit carries report id / program / date so the model cites instead of paraphrases;
  - a passage from a report with no stored body is labelled, never silently substituted.
"""
import json, os, sqlite3, sys

DB = os.environ.get("CORPUS_DB", "/path/to/corpus.sqlite")
SEARCH = os.environ.get("CORPUS_SEARCH", os.path.join(os.path.dirname(os.path.abspath(__file__)), "search.py"))
PY = sys.executable

def evidence(rows):
    out = []
    for r in rows:
        head = (f"REPORT #{r['report_id']} | {r['title']} | {r['program']} | {r['severity']} | {r['disclosed']}\n"
                f"https://hackerone.com/reports/{r['report_id']}" if r.get("report_id")
                else f"DOC {r.get('path')} § {r.get('heading')}")
        out.append(f"<<<EVIDENCE\n{head}\n\n{r['text'][:1400]}\nEVIDENCE>>>")
    return "\n\n".join(out) or "(no results)"

def tool_search(a):
    import subprocess
    args = [PY, SEARCH, str(a.get("query", "")), "--json", "-k", str(int(a.get("k", 5)))]
    for k, flag in (("class", "--class"), ("program", "--program"), ("severity", "--severity"), ("min_bounty", "--min-bounty")):
        if a.get(k): args += [flag, str(a[k])]
    p = subprocess.run(args, capture_output=True, text=True, timeout=180)
    if p.returncode != 0: return (p.stderr or "search failed")[:800]
    d = json.loads(p.stdout)
    return f"query={d['query']} legs={d['legs']}\n\n" + evidence(d["hits"])

def tool_get_report(a):
    con = sqlite3.connect(DB); con.row_factory = sqlite3.Row
    r = con.execute("SELECT * FROM bodies WHERE id=?", (int(a["id"]),)).fetchone()
    if not r: return f"report {a['id']} not in corpus"
    body = r["body"] if "body" in r.keys() and r["body"] else "(body not public / not stored — summary only)"
    return ("<<<EVIDENCE\nREPORT #%s | %s | %s | %s\n\nSUMMARY\n%s\n\nWRITE-UP\n%s\nEVIDENCE>>>"
            % (r["id"], r["title"], r["program"], r["severity"], r["summary"] or "-", body[:12000]))

def tool_stats(_a):
    con = sqlite3.connect(DB)
    one = lambda q: con.execute(q).fetchone()[0]
    return (f"reports={one('SELECT COUNT(*) FROM reports')} "
            f"bodies={one('SELECT COUNT(*) FROM bodies WHERE length(COALESCE(body,\"\"))>0')} "
            f"chunks={one('SELECT COUNT(*) FROM chunks WHERE vec IS NOT NULL')}")

TOOLS = [
    {"name": "corpus_search", "description": "Hybrid keyword+semantic search over the corpus. Returns passages with report id, program and date.",
     "inputSchema": {"type": "object", "properties": {"query": {"type": "string"}, "class": {"type": "string"},
                     "program": {"type": "string"}, "severity": {"type": "string"}, "min_bounty": {"type": "number"},
                     "k": {"type": "integer"}}, "required": ["query"]}, "fn": tool_search},
    {"name": "corpus_get_report", "description": "One report in full (summary + write-up).",
     "inputSchema": {"type": "object", "properties": {"id": {"type": "integer"}}, "required": ["id"]}, "fn": tool_get_report},
    {"name": "corpus_stats", "description": "Row counts, so the agent can sanity-check what it is standing on.",
     "inputSchema": {"type": "object", "properties": {}}, "fn": tool_stats},
]

def reply(oid, result=None, error=None):
    msg = {"jsonrpc": "2.0", "id": oid}
    if error: msg["error"] = {"code": -32000, "message": str(error)}
    else: msg["result"] = result
    sys.stdout.write(json.dumps(msg) + "\n"); sys.stdout.flush()

def main():
    for line in sys.stdin:
        line = line.strip()
        if not line or line.lower().startswith("content-length"): continue
        try: req = json.loads(line)
        except Exception: continue
        m, oid = req.get("method"), req.get("id")
        try:
            if m == "initialize":
                reply(oid, {"protocolVersion": "2024-11-05", "capabilities": {"tools": {"listChanged": False}},
                            "serverInfo": {"name": "corpus", "version": "1.0"}})
            elif m in ("notifications/initialized", "initialized"):
                continue
            elif m == "tools/list":
                reply(oid, {"tools": [{k: t[k] for k in ("name", "description", "inputSchema")} for t in TOOLS]})
            elif m == "tools/call":
                params = req.get("params") or {}
                t = next((x for x in TOOLS if x["name"] == params.get("name")), None)
                if not t: reply(oid, error=f"unknown tool {params.get('name')}"); continue
                reply(oid, {"content": [{"type": "text", "text": str(t["fn"](params.get("arguments") or {}))[:20000]}],
                            "isError": False})
            elif m == "ping":
                reply(oid, {})
            else:
                reply(oid, error=f"unsupported method {m}")
        except Exception as e:
            reply(oid, error=e)

if __name__ == "__main__":
    main()
