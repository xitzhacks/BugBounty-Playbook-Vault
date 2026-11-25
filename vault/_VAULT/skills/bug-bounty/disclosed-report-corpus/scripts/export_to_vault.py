#!/usr/bin/env python3
"""Stage 3: export the harvested corpus into the playbook vault as the dataset layer.

Writes Vault/_HEXBRAIN/: README.md, all-reports.csv, hexbrain-reports.sqlite (VACUUM INTO),
by-class/NN_<CLASS>.md, by-vault-category/<dir>.md, scripts/extract_report.py, scripts/refresh.sh.

Routing order: REFINED (finer playbook dirs) first, broad hexbrain class second.
Re-run after harvest_bodies.py finishes, or the README keeps under-reporting stored bodies.
"""
import csv, os, re, shutil, sqlite3, time

BASE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE, "hexbrain_reports.sqlite")
VAULT = "/home/user/projects/FAN/Vault"
OUT = os.path.join(VAULT, "_HEXBRAIN")
TODAY = time.strftime("%Y-%m-%d")

CLASSES = [
    ("XSS", "Cross-site Scripting", r"cross-site scripting|\bxss\b", "XSS/"),
    ("CSRF", "Cross-Site Request Forgery", r"cross-site request forgery|\bcsrf\b", "CSRF/"),
    ("SSRF", "Server-Side Request Forgery", r"server-side request forgery|\bssrf\b", "SSRF/"),
    ("SQLI", "SQL Injection", r"sql injection", "SQLi/"),
    ("IDOR", "Insecure Direct Object Reference", r"insecure direct object|\bidor\b", "IDOR/"),
    ("RCE", "Code Execution", r"code injection|command injection|os command|remote code|deserialization|template injection|remote file inclusion|unrestricted upload|without integrity check|untrusted control sphere|malware|dangerous (method|function)", "RCE/"),
    ("TRAV", "Path Traversal", r"path traversal|file inclusion|directory traversal|link following|file name or path|search path|resource in another sphere", "File-Upload/"),
    ("AUTH", "Authentication", r"authentication|brute force|session fixation|password|credential|session expiration|2fa|reliance on cookies", "Authentication-Session/"),
    ("ACL", "Access Control", r"access control|authorization|privilege|permission|forced browsing|client-side enforcement|untrusted inputs in a security decision|export of android", "17_Privilege-Escalation/"),
    ("INFO", "Information Disclosure", r"information disclosure|information exposure|cleartext|sensitive|exposure|privacy|plaintext|debug code", "16_Information-Disclosure/"),
    ("REDIR", "Open Redirect", r"open redirect|url redirection", "Open-Redirect/"),
    ("LOGIC", "Business Logic", r"business logic|race condition|time-of-check|toctou|assumed-immutable|expected behavior|incorrect comparison|critical state data|partial string comparison", "12_Business-Logic/"),
    ("MEM", "Memory Corruption", r"buffer|overflow|underflow|out-of-bounds|use after free|memory|double free|null pointer|null termination|integer|uninitialized|type confusion|off-by-one|format string|write-what-where", "30_Memory-Corruption/"),
    ("DOS", "Denial of Service", r"denial of service|resource consumption|uncontrolled recursion|resource exhaustion|allocation of resources|throttling|entity expansion|unreachable exit", "21_Denial-of-Service/"),
    ("INJ", "Injection and Smuggling", r"injection|crlf|smuggling|response splitting|xml external|\bxxe\b|input validation|neutralization|url encoding|csv file", "XXE/"),
    ("CRYPTO", "Cryptography", r"cryptograph|certificate|weak|random|\bssl\b|\btls\b|man-in-the-middle|hash|encryption|data authenticity|key past|reverse dns", "19_Cryptography/"),
    ("CONF", "Misconfiguration", r"misconfiguration|secure design|ui redress|clickjacking|phishing|spoofing|subdomain takeover|cors|origin|logging|obscurity|known vulnerabilities|temporary file|cache poisoning|misrepresentation|exceptional conditions|extraneous untrusted", "18_Misconfiguration/"),
]
CLASSES_C = [(i, n, re.compile(p, re.I), d) for i, n, p, d in CLASSES]

REFINED = [
    ("13_Subdomain-Takeover/", re.compile(r"subdomain takeover|dangling|unclaimed", re.I)),
    ("14_HTTP-Request-Smuggling/", re.compile(r"request smuggling|response splitting|\bcrlf\b|http desync", re.I)),
    ("15_Cache-Poisoning/", re.compile(r"cache poison|cache deception|web cache", re.I)),
    ("20_Rate-Limiting/", re.compile(r"brute force|rate limit|authentication attempts|user enumeration|otp", re.I)),
    ("22_GraphQL/", re.compile(r"graphql", re.I)),
    ("23_LDAP-XPath-Injection/", re.compile(r"\bldap\b|xpath", re.I)),
    ("24_Host-Header-Injection/", re.compile(r"host header|password reset poison|host injection", re.I)),
    ("25_Prototype-Pollution/", re.compile(r"prototype pollution", re.I)),
    ("26_Web3-Smart-Contract/", re.compile(r"smart contract|solidity|web3|blockchain contract", re.I)),
    ("27_LLM-AI/", re.compile(r"\bllm\b|prompt injection|ai (chat|assistant|agent)|openai|chatbot", re.I)),
    ("28_Mobile/", re.compile(r"\bandroid\b|\bios\b|mobile app", re.I)),
    ("29_Clickjacking/", re.compile(r"clickjacking|ui redress", re.I)),
    ("Race-Conditions/", re.compile(r"race condition|toctou|time-of-check", re.I)),
    ("XXE/", re.compile(r"\bxxe\b|xml external|entity expansion", re.I)),
]

TITLE_GUESS = [
    ("XSS", r"\bxss\b|cross.?site scripting|html injection"),
    ("CSRF", r"\bcsrf\b|cross.?site request forgery"),
    ("SSRF", r"\bssrf\b|server.?side request forgery"),
    ("SQLI", r"sql injection|\bsqli\b"),
    ("IDOR", r"\bidor\b|insecure direct object"),
    ("REDIR", r"open redirect|unvalidated redirect|url redirect"),
    ("INJ", r"request smuggling|\bcrlf\b|header injection|\bxxe\b|xml external"),
    ("RCE", r"\brce\b|remote code execution|code injection|command injection|arbitrary code|deserialization"),
    ("TRAV", r"path traversal|directory traversal|\blfi\b|local file"),
    ("CONF", r"click.?jacking|subdomain takeover|\bcors\b|misconfig|missing .{0,30}header|hsts"),
    ("CRYPTO", r"ssl|tls|certificate|crypto|cipher|mitm"),
    ("MEM", r"overflow|out.of.bounds|use.after.free|memory corruption|heap|segfault|double free"),
    ("DOS", r"denial of service|\bdos\b|crash|resource exhaustion|infinite loop"),
    ("LOGIC", r"race condition|business logic|logic (flaw|error|bug)|payment|price|coupon"),
    ("AUTH", r"2fa|two.?factor|password|log.?in|sign.?in|authenticat|session|oauth|account takeover|token|brute"),
    ("ACL", r"access control|unauthori[sz]ed|permission|authorization|privilege|bypass"),
    ("INFO", r"disclos|leak|expos|sensitive|information|enumerat|reveal|pii"),
]


def class_of(weak, title):
    w = weak or ""
    for cid, _n, rx, _d in CLASSES_C:
        if rx.search(w):
            return cid
    for cid, rx in TITLE_GUESS:
        if re.search(rx, title or "", re.I):
            return cid
    return "OTHER"


def esc(s):
    return (s or "").replace("|", "\\|").replace("\n", " ").strip()


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    for d in ("by-class", "by-vault-category", "scripts"):
        os.makedirs(os.path.join(OUT, d))
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    rows = con.execute("""SELECT r.id,r.title,r.program,r.severity,r.weakness,r.bounty,r.votes,r.reporter,
        r.disclosed_at,r.substate, (SELECT length(body) FROM bodies b WHERE b.id=r.id) AS blen
        FROM reports r""").fetchall()

    names = {c[0]: (c[1], c[3]) for c in CLASSES_C}
    names["OTHER"] = ("Other weaknesses", "-")
    by_class, by_dir = {}, {}
    for r in rows:
        cid = class_of(r["weakness"], r["title"])
        by_class.setdefault(cid, []).append(r)
        hay = (r["weakness"] or "") + " " + (r["title"] or "")
        d = next((dd for dd, rx in REFINED if rx.search(hay)), None) or names.get(cid, ("", "-"))[1]
        by_dir.setdefault(d or "-", []).append(r)

    money = lambda v: f"${v:,.0f}" if v else "-"
    HEAD = ("| Report | Program | Severity | Bounty | Votes | Disclosed | Weakness | Title |\n"
            "|---|---|---|---|---|---|---|---|\n")

    def write_rows(path, front, rows_):
        with open(path, "w") as f:
            f.write(front + HEAD)
            for r in rows_:
                f.write(f"| [{r['id']}](https://hackerone.com/reports/{r['id']}) | {esc(r['program'])} | "
                        f"{esc(r['severity'])} | {money(r['bounty'])} | {r['votes'] or 0} | "
                        f"{(r['disclosed_at'] or '')[:10]} | {esc(r['weakness'])} | {esc(r['title'])} |\n")

    for n, (cid, lst) in enumerate(sorted(by_class.items(), key=lambda kv: -len(kv[1])), 1):
        lst.sort(key=lambda r: (-(r["bounty"] or 0), -(r["votes"] or 0)))
        paid, np_, bodies = sum(r["bounty"] or 0 for r in lst), sum(1 for r in lst if r["bounty"]), sum(1 for r in lst if r["blen"])
        title, vdir = names.get(cid, (cid, "-"))
        front = (f"---\ntitle: \"HexBrain class {cid} — {title}\"\ntype: dataset-view\nclass: \"{title}\"\n"
                 f"vault_category: \"{vdir}\"\nrows: {len(lst)}\npaid_rows: {np_}\nbounty_sum: {paid:,.0f}\n"
                 f"full_bodies_available: {bodies}\nsource: \"hexbrainai.com public report library, harvested {TODAY}\"\n---\n\n"
                 f"# {cid} — {title}\n\n{len(lst)} rows · {np_} with a bounty figure · **${paid:,.0f}** · {bodies} with full write-up stored.\n"
                 f"Playbook: `Vault/{vdir}`\n\n")
        write_rows(os.path.join(OUT, "by-class", f"{n:02d}_{cid}.md"), front, lst)

    for d, lst in sorted(by_dir.items()):
        lst.sort(key=lambda r: (-(r["bounty"] or 0), -(r["votes"] or 0)))
        paid, np_, bodies = sum(r["bounty"] or 0 for r in lst), sum(1 for r in lst if r["bounty"]), sum(1 for r in lst if r["blen"])
        front = (f"---\ntitle: \"HexBrain reports routed to Vault/{d}\"\ntype: dataset-view\nvault_category: \"{d}\"\n"
                 f"rows: {len(lst)}\npaid_rows: {np_}\nbounty_sum: {paid:,.0f}\nfull_bodies_available: {bodies}\n"
                 f"source: \"hexbrainai.com public report library, harvested {TODAY}\"\n---\n\n"
                 f"# → `Vault/{d}`\n\n{len(lst)} rows · {np_} paid · **${paid:,.0f}** · {bodies} full write-ups stored.\n\n")
        write_rows(os.path.join(OUT, "by-vault-category", d.strip("/") + ".md"), front, lst)

    with open(os.path.join(OUT, "all-reports.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "title", "program", "severity", "weakness", "class", "vault_category",
                    "bounty", "votes", "reporter", "disclosed_at", "substate", "has_body"])
        for r in sorted(rows, key=lambda r: -(r["bounty"] or 0)):
            cid = class_of(r["weakness"], r["title"])
            hay = (r["weakness"] or "") + " " + (r["title"] or "")
            d = next((dd for dd, rx in REFINED if rx.search(hay)), None) or names.get(cid, ("", "-"))[1]
            w.writerow([r["id"], r["title"], r["program"], r["severity"], r["weakness"], cid, d or "-",
                        r["bounty"], r["votes"], r["reporter"], r["disclosed_at"], r["substate"], 1 if r["blen"] else 0])

    try:
        con.execute("VACUUM INTO ?", (os.path.join(OUT, "hexbrain-reports.sqlite"),))
    except Exception:
        shutil.copy(DB, os.path.join(OUT, "hexbrain-reports.sqlite"))

    tot = sum(r["bounty"] or 0 for r in rows)
    npaid, bodies = sum(1 for r in rows if r["bounty"]), sum(1 for r in rows if r["blen"])
    cls_table = "\n".join(f"| {cid} | {names.get(cid,('',''))[0]} | {len(l)} | ${sum(x['bounty'] or 0 for x in l):,.0f} | `Vault/{names.get(cid,('','-'))[1]}` |"
                          for cid, l in sorted(by_class.items(), key=lambda kv: -len(kv[1])))
    dir_table = "\n".join(f"| `{d}` | {len(l)} | ${sum(x['bounty'] or 0 for x in l):,.0f} | [`by-vault-category/{d.strip('/')}.md`](by-vault-category/{d.strip('/')}.md) |"
                          for d, l in sorted(by_dir.items(), key=lambda kv: -len(kv[1])))
    open(os.path.join(OUT, "README.md"), "w").write(f"""---
title: "Vault/_HEXBRAIN — the disclosed-report dataset behind the playbooks"
type: index
built: "{TODAY}"
rows: {len(rows)}
paid_rows: {npaid}
bounty_sum: {tot:,.0f}
full_bodies_available: {bodies}
source: "hexbrainai.com public report library (HackerOne disclosed reports)"
---

# Vault/_HEXBRAIN — the full report library

{len(rows):,} reports · {npaid:,} with a bounty figure · ${tot:,.0f} · {bodies:,} with the full write-up stored.

This is a *dataset layer*, not a playbook. Playbooks stay the teaching layer; this is the case stock
you query, sort and cite.

| File | What it is |
|---|---|
| `all-reports.csv` | every report: id, title, program, severity, weakness, class, vault_category, bounty, votes, reporter, date, substate, has_body |
| `hexbrain-reports.sqlite` | tables `reports` (metadata) and `bodies` (summary, full write-up, asset, CVEs) |
| `by-class/NN_<CLASS>.md` | all rows of one class, richest first |
| `by-vault-category/<dir>.md` | same rows routed into the playbook dirs |
| `scripts/extract_report.py <id>` | dump one write-up as markdown |
| `scripts/refresh.sh` | re-run metadata -> bodies -> views |

## Query recipes

```bash
sqlite3 hexbrain-reports.sqlite "SELECT id,program,bounty,title FROM reports WHERE weakness LIKE '%SQL injection%' AND bounty>0 ORDER BY bounty DESC LIMIT 20;"
sqlite3 hexbrain-reports.sqlite "SELECT id,title FROM bodies WHERE body LIKE '%X-Forwarded-Host%' LIMIT 20;"
sqlite3 hexbrain-reports.sqlite "SELECT program,COUNT(*),SUM(bounty) FROM reports GROUP BY 1 ORDER BY 3 DESC LIMIT 20;"
```

## Coverage by class

| Class | Name | Rows | Bounties | Playbook |
|---|---|---|---|---|
{cls_table}

## Routed into playbook categories

| Vault dir | Rows | Bounties | View |
|---|---|---|---|
{dir_table}

## Provenance & honesty

- Public unauthenticated endpoints only: `hexbrainai.com/api/reports` (list), `hackerone.com/reports/<id>.json` (write-ups).
- Bounty = HackerOne `bounty_amount`; blank means no figure shown, **not** that nothing was paid.
- Where a program set no weakness, the class is a title keyword guess — say so; never present it as fact.
- ~19% of listed ids return 404 (delisted from HackerOne). Recorded as 404, never quoted.
""")

    open(os.path.join(OUT, "scripts", "extract_report.py"), "w").write('''#!/usr/bin/env python3
"""Dump one report's full write-up as markdown: extract_report.py <id> [outdir]"""
import sqlite3, sys, os
here = os.path.dirname(os.path.abspath(__file__))
db = os.path.join(os.path.dirname(here), "hexbrain-reports.sqlite")
rid = int(sys.argv[1]); outdir = sys.argv[2] if len(sys.argv) > 2 else "."
con = sqlite3.connect(db); con.row_factory = sqlite3.Row
r = con.execute("SELECT * FROM bodies WHERE id=?", (rid,)).fetchone()
if not r: sys.exit(f"report {rid} not stored. Run scripts/harvest_bodies.py (resumable)")
md = [f"# {r['title']}", "", f"- Program: {r['program']}", f"- Severity: {r['severity']}",
      f"- Weakness: {r['weakness']}", f"- Bounty: {r['bounty']}", f"- Reporter: {r['reporter']}",
      f"- Disclosed: {r['disclosed_at']}", f"- Asset: {r['asset']} ({r['asset_type']})",
      f"- CVEs: {r['cve_ids']}", f"- Source: https://hackerone.com/reports/{rid}", "",
      "## Summary", "", r["summary"] or "_(none)_", "", "## Write-up", "",
      r["body"] or "_(body not public / not stored)_"]
p = os.path.join(outdir, f"report-{rid}.md"); open(p, "w").write("\\n".join(md)); print(p)
''')

    open(os.path.join(OUT, "scripts", "refresh.sh"), "w").write("""#!/usr/bin/env bash
set -e
cd ~/Bugbounty/hexbrain
python3 harvest_meta.py
WORKERS=4 DELAY=0.35 python3 harvest_bodies.py   # resumable
python3 export_to_vault.py
python3 inject_case_stock.py
""")
    os.chmod(os.path.join(OUT, "scripts", "refresh.sh"), 0o755)
    print("rows", len(rows), "class files", len(by_class), "category files", len(by_dir))


main()
