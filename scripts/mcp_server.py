#!/usr/bin/env python3
"""MCP (stdio, JSON-RPC 2.0) server exposing the vault to the main agent.

Register once, then every session gets these tools without loading the DB into context:

  hermes mcp add vault --command "$PWD/.venv/bin/python" --args "$PWD/scripts/mcp_server.py"

(Registration is opt-in at install time: VAULT_REGISTER_MCP=1 bash setup.sh.)

Tools
  vault_search(query, class?, program?, severity?, min_bounty?, k?)  hybrid BM25+vector over reports and our docs
  vault_get_report(id)                                              one report in full
  vault_plan(feature)                                               which classes real reports found in a feature
  vault_bypass(protection?)                                         how researchers got past a protection
  vault_stats()                                                     counts, so the agent can sanity-check
All evidence is returned inside <<<EVIDENCE ... EVIDENCE>>> markers: data, never instructions.
"""
import json, os, re, sqlite3, subprocess, sys, collections

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.environ.get("VAULT_DB", os.path.join(os.path.dirname(HERE), "vault", "_VAULT", "reports.sqlite"))
ROOT = os.path.dirname(HERE)
PY = os.path.join(ROOT, ".venv", "bin", "python") if os.path.exists(os.path.join(ROOT, ".venv", "bin", "python")) else sys.executable

def run_search(args, k=5):
    cmd = [PY, os.path.join(HERE, "search.py")] + args + ["--json", "-k", str(k)]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    if p.returncode != 0:
        return {"error": (p.stderr or "search failed").strip()[:800]}
    try:
        return json.loads(p.stdout)
    except Exception:
        return {"error": "search returned non-JSON"}

def wrap(hits):
    out = []
    for h in hits:
        head = (f"REPORT #{h['report_id']} | {h['title']} | {h['program']} | {h['severity']} | "
                f"bounty {h['bounty']} | {h['disclosed']}\nhttps://hackerone.com/reports/{h['report_id']}"
                if h["kind"] == "report" else f"VAULT DOC {h['path']} § {h['heading']}")
        out.append(f"<<<EVIDENCE\n{head}\n\n{h['text'][:1400]}\nEVIDENCE>>>")
    return "\n\n".join(out) or "(no results)"

def tool_search(a):
    args = [str(a.get("query", ""))]
    if a.get("class"): args += ["--class", str(a["class"])]
    if a.get("program"): args += ["--program", str(a["program"])]
    if a.get("severity"): args += ["--severity", str(a["severity"])]
    if a.get("min_bounty"): args += ["--min-bounty", str(a["min_bounty"])]
    if a.get("rerank"): args.append("--rerank")
    r = run_search(args, int(a.get("k", 5)))
    if "error" in r: return r["error"]
    return f"query={r['query']} legs={r['legs']}\n\n" + wrap(r["hits"])

def tool_get_report(a):
    try:
        rid = int(a["id"])
    except (KeyError, TypeError, ValueError):
        return "vault_get_report expects an integer id (e.g. {\"id\": 1234567})"
    con = sqlite3.connect(DB); con.row_factory = sqlite3.Row
    r = con.execute("SELECT * FROM bodies WHERE id=?", (rid,)).fetchone()
    if not r: return f"report {rid} is not in the library"
    body = r["body"] or ""
    body = body if body else "(body not public / not stored — summary only)"
    return (f"<<<EVIDENCE\nREPORT #{r['id']} | {r['title']} | {r['program']} | {r['severity']} | "
            f"weakness {r['weakness']} | bounty {r['bounty']} | {r['disclosed_at']}\n"
            f"asset {r['asset']} ({r['asset_type']}) | CVEs {r['cve_ids']}\n\n"
            f"SUMMARY\n{r['summary'] or '-'}\n\nWRITE-UP\n{body[:12000]}\nEVIDENCE>>>")

def tool_plan(a):
    feature = str(a.get("feature", ""))
    r = run_search([feature], 24)
    if "error" in r: return r["error"]
    by = collections.defaultdict(list)
    for h in r["hits"]:
        if h["kind"] == "report": by[(h["weakness"] or "unclassified")].append(h)
    lines = [f"feature: {feature}", f"legs: {r['legs']}", ""]
    for w, hs in sorted(by.items(), key=lambda kv: -len(kv[1]))[:8]:
        lines.append(f"{len(hs)}x {w}")
        for h in hs[:2]: lines.append(f"   #{h['report_id']} {h['title'][:90]} (${h['bounty'] or 0:,.0f})")
    # attach named techniques for the top classes — this is the layer that made DVWA pass 3 shallow
    con = sqlite3.connect(DB)
    lines.append("\nTECHNIQUES to actually run:")
    for w, _ in sorted(by.items(), key=lambda kv: -len(kv[1]))[:4]:
        cls_guess = None
        low = w.lower()
        for key, rx in [("LFI", r"traversal|file inclusion|path traversal"), ("UPLOAD", r"upload"),
                        ("SQLI", r"sql"), ("XSS", r"xss|cross-site scripting"), ("SSRF", r"ssrf"),
                        ("IDOR", r"idor|object reference"), ("RCE", r"code inject|command inject|deserial|rce"),
                        ("XXE", r"xxe|xml"), ("AUTH", r"auth|password|session"), ("CSRF", r"csrf"),
                        ("CONF", r"misconfig|cors|clickjack|header")]:
            if re.search(rx, low): cls_guess = key; break
        cls_guess = cls_guess or ""
        rows = con.execute("""SELECT name, chunk_id FROM techniques WHERE cls=?
                              ORDER BY CASE confidence WHEN 'path' THEN 0 ELSE 1 END, length(name) DESC LIMIT 5""",
                           (cls_guess,)).fetchall()
        if rows:
            lines.append(f"  {w}:")
            for n, cid in rows: lines.append(f"    - {n[:80]} (chunk {cid})")
    return "\n".join(lines) + "\n\n" + wrap(r["hits"][:6])

TAGMAP = [("waf", r"waf|cloudflare|akamai|incapsula|imperva|modsecurity|sucuri"),
          ("csp", r"csp|content-security"), ("twofa", r"2fa|two.factor|mfa|otp"),
          ("rate_limit", r"rate.?limit|throttl|brute"), ("allowlist", r"allow.?list|whitelist|blocklist"),
          ("sanitizer", r"saniti|escape|filter|strip"), ("earlier_fix", r"fix|patch|regression"),
          ("cors", r"cors|access-control"), ("authz", r"authoriz|access control")]

def tool_bypass(a):
    prot = str(a.get("protection", "") or "")
    k = int(a.get("k", 6))
    tag = next((t for t, rx in TAGMAP if re.search(rx, prot.lower())), None)
    con = sqlite3.connect(DB)
    rows = []
    if tag:
        rows = con.execute("""SELECT id,tag,kind,report_id,path,title,program,passage,payloads,score
                              FROM bypasses WHERE tag=? AND score>=3
                              ORDER BY score DESC, CASE confidence WHEN 'code' THEN 0 ELSE 1 END LIMIT ?""",
                           (tag, k)).fetchall()
    if not rows:   # no tag match: fall back to hybrid search
        q = f"{prot} bypass filter waf csp allowlist sanitizer protection".strip()
        r = run_search([q], k)
        if "error" in r: return r["error"]
        return f"protection: {prot or '(any)'} [search fallback]\n" + wrap(r["hits"])
    out = [f"protection: {prot or '(any)'} → tag={tag} · {len(rows)} indexed bypasses\n"]
    for bid, tg, kind, rid, path, title, program, passage, payloads, sc in rows:
        head = f"#{rid} {title} ({program})" if rid else f"{path} § {title}"
        out.append(f"<<<EVIDENCE\n[{tg}] {head}\n"
                   f"https://hackerone.com/reports/{rid}\n\n{(passage or '')[:900]}\n"
                   f"\nPAYLOAD: {(payloads or '-')[:700]}\nEVIDENCE>>>")
    out.append("\nPassages are quoted from public write-ups — verify against the cited report before use.")
    return "\n\n".join(out)

def tool_stats(_a):
    con = sqlite3.connect(DB)
    def one(sql):
        return con.execute(sql).fetchone()[0]
    reports = one("SELECT COUNT(*) FROM reports")
    bodies = one("SELECT COUNT(*) FROM bodies WHERE length(COALESCE(body,''))>0")
    summary = one("SELECT COUNT(*) FROM bodies WHERE http_status=200 AND (body IS NULL OR body='')")
    delisted = one("SELECT COUNT(*) FROM bodies WHERE http_status=404")
    docs = one("SELECT COUNT(*) FROM documents")
    chunks = one("SELECT COUNT(*) FROM chunks WHERE vec IS NOT NULL")
    money = one("SELECT CAST(COALESCE(SUM(bounty),0) AS INT) FROM reports")
    return (f"reports={reports} bodies_full={bodies} summary_only={summary} delisted={delisted} "
            f"documents={docs} chunks_embedded={chunks} bounty_total=${money:,}")

def tool_techniques(a):
    cls = str(a.get("class", "") or "").upper()
    q = str(a.get("query", "") or "")
    k = int(a.get("k", 25))
    con = sqlite3.connect(DB)
    where, args = [], []
    if cls: where.append("upper(cls)=?"); args.append(cls)
    if q:
        where.append("(lower(name) LIKE ? OR lower(keywords) LIKE ?)")
        args += [f"%{q.lower()}%", f"%{q.lower()}%"]
    sql = "SELECT cls,name,path,chunk_id,confidence FROM techniques"
    if where: sql += " WHERE " + " AND ".join(where)
    sql += " ORDER BY CASE confidence WHEN 'path' THEN 0 ELSE 1 END, length(name) DESC LIMIT ?"
    rows = con.execute(sql, args + [k]).fetchall()
    if not rows: return f"no technique matched class={cls or '-'} query={q or '-'}"
    out = [f"techniques (class={cls or 'any'} query={q or 'any'}): {len(rows)}"]
    for c, n, p, cid, conf in rows:
        out.append(f"[{c}] {n[:90]}\n      {p or '-'} (chunk {cid}, {conf})")
    out.append("\nTo read one: vault_get_chunk(chunk_id) or vault_search with the technique name.")
    return "\n".join(out)

def tool_chunk(a):
    con = sqlite3.connect(DB); con.row_factory = sqlite3.Row
    r = con.execute("SELECT heading,text,path FROM chunks WHERE id=?", (int(a["chunk_id"]),)).fetchone()
    if not r: return f"chunk {a['chunk_id']} not found"
    return f"<<<EVIDENCE\n{r['path'] or 'report chunk'} § {r['heading']}\n\n{r['text'][:6000]}\nEVIDENCE>>>"

def tool_payloads(a):
    cls = str(a.get("class", "") or "").upper()
    q = str(a.get("query", "") or "")
    k = int(a.get("k", 5))
    con = sqlite3.connect(DB)
    where, args = [], []
    if cls: where.append("upper(cls)=?"); args.append(cls)
    if q:
        where.append("(lower(payload) LIKE ? OR lower(context) LIKE ?)")
        args += [f"%{q.lower()}%", f"%{q.lower()}%"]
    sql = "SELECT id,payload,lang,cls,kind,report_id,path,context FROM payloads"
    if where: sql += " WHERE " + " AND ".join(where)
    sql += " ORDER BY score DESC, chars ASC LIMIT ?"
    rows = con.execute(sql, args + [k]).fetchall()
    if not rows: return f"no payload matched class={cls or '-'} query={q or '-'}"
    out = [f"payloads (class={cls or 'any'} query={q or 'any'}): {len(rows)}"]
    for pid, pay, lang, c, kind, rid, path, ctx in rows:
        src = f"https://hackerone.com/reports/{rid}" if rid else (path or "")
        out.append(f"[{pid}] {c} · {lang or '-'} · {src}\n{(pay or '')[:600]}")
    out.append("\nQuoted from public write-ups — verify before use.")
    return "\n\n".join(out)

TOOLS = [
 dict(name="vault_search", description="Hybrid keyword+semantic search over 15,244 disclosed reports and our playbooks. Use before testing a bug class: real reports, with program, bounty and the passage that shows what was done.",
      inputSchema={"type":"object","properties":{"query":{"type":"string"},"class":{"type":"string"},"program":{"type":"string"},"severity":{"type":"string"},"min_bounty":{"type":"number"},"k":{"type":"integer"},"rerank":{"type":"boolean"}},"required":["query"]},
      fn=tool_search),
 dict(name="vault_get_report", description="Return one disclosed report in full (summary + write-up, payloads included).",
      inputSchema={"type":"object","properties":{"id":{"type":"integer"}},"required":["id"]}, fn=tool_get_report),
 dict(name="vault_plan", description="Describe a feature you are testing (e.g. 'profile picture upload', 'OAuth login') and get the bug classes real reports found in features like it, with examples.",
      inputSchema={"type":"object","properties":{"feature":{"type":"string"}},"required":["feature"]}, fn=tool_plan),
 dict(name="vault_bypass", description="How researchers got past a protection (WAF, CSP, 2FA, allow-list, sanitiser, rate limit, an earlier fix). Returns passages and payloads.",
      inputSchema={"type":"object","properties":{"protection":{"type":"string"},"k":{"type":"integer"}},"required":[]}, fn=tool_bypass),
 dict(name="vault_techniques", description="List the NAMED techniques that exist for a bug class (e.g. class=LFI -> 'PHP Filter-Chain to RCE', 'Path Traversal Encoding Bypasses'). Use this instead of asking for a class name directly: the index ranks technique names, not class words.",
      inputSchema={"type":"object","properties":{"class":{"type":"string"},"query":{"type":"string"},"k":{"type":"integer"}},"required":[]},
      fn=tool_techniques),
 dict(name="vault_get_chunk", description="Read one retrieval chunk by id (the how-to passage a technique points at).",
      inputSchema={"type":"object","properties":{"chunk_id":{"type":"integer"}},"required":["chunk_id"]}, fn=tool_chunk),
 dict(name="vault_payloads", description="Copy-ready payload strings that someone actually used, by class (XSS, SQLI, LFI, SSRF, RCE, UPLOAD...) or keyword. Use after vault_techniques when you need the literal payload.",
      inputSchema={"type":"object","properties":{"class":{"type":"string"},"query":{"type":"string"},"k":{"type":"integer"}},"required":[]},
      fn=tool_payloads),
 dict(name="vault_stats", description="Row counts for the library, so you can check what you are standing on.",
      inputSchema={"type":"object","properties":{}}, fn=tool_stats),
]

def reply(oid, result=None, error=None):
    msg = {"jsonrpc": "2.0", "id": oid}
    if error: msg["error"] = {"code": -32000, "message": str(error)}
    else: msg["result"] = result
    sys.stdout.write(json.dumps(msg) + "\n"); sys.stdout.flush()

def main():
    for line in sys.stdin:
        line = line.strip()
        if not line: continue
        if line.lower().startswith("content-length"): continue
        try: req = json.loads(line)
        except Exception: continue
        m, oid = req.get("method"), req.get("id")
        try:
            if m == "initialize":
                reply(oid, {"protocolVersion": "2024-11-05",
                            "capabilities": {"tools": {"listChanged": False}},
                            "serverInfo": {"name": "vault", "version": "1.0"}})
            elif m in ("notifications/initialized", "initialized"):
                continue
            elif m == "tools/list":
                reply(oid, {"tools": [{k: t[k] for k in ("name","description","inputSchema")} for t in TOOLS]})
            elif m == "tools/call":
                name = (req.get("params") or {}).get("name")
                args = (req.get("params") or {}).get("arguments") or {}
                t = next((x for x in TOOLS if x["name"] == name), None)
                if not t: reply(oid, error=f"unknown tool {name}"); continue
                out = t["fn"](args)
                reply(oid, {"content": [{"type": "text", "text": str(out)[:20000]}], "isError": False})
            elif m == "ping":
                reply(oid, {})
            else:
                reply(oid, error=f"unsupported method {m}")
        except Exception as e:
            reply(oid, error=e)

if __name__ == "__main__":
    main()
