#!/usr/bin/env python3
"""Export the harvested the public HackerOne dataset vault into the playbook vault.

Produces, under VAULT/_VAULT/:
  README.md                     provenance + counts + query recipes
  all-reports.csv               every report (metadata; body flag)
  reports.sqlite       metadata + full write-ups
  by-class/NN_<Class>.md        every report in each class, vault dir mapped
  by-vault-category/<dir>.md    every report routed into our playbook category dirs
  scripts/extract_report.py     dump one report's full write-up as markdown
"""
import json, os, re, shutil, sqlite3, time, csv

BASE = os.path.dirname(os.path.abspath(__file__))
DB = os.environ.get("VAULT_DB", os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "vault", "_VAULT", "reports.sqlite"))
VAULT = os.environ.get("VAULT_ROOT", os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "vault"))
OUT = os.path.join(VAULT, "_VAULT")
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

# Refined routing into the vault's finer playbook dirs (checked before the broad class).
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

def class_of(weak, title):
    for n, pat in (("XXE", r"\bxxe\b|xml external"), ("Race", r"race condition")):
        pass
    w = weak or ""
    for cid, name, rx, d in CLASSES_C:
        if rx.search(w): return cid
    # no program weakness: guess from title with the site's own rules
    t = title or ""
    guesses = [
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
    for cid, rx in guesses:
        if re.search(rx, t, re.I): return cid
    return "OTHER"

def esc(s):
    return (s or "").replace("|", "\\|").replace("\n", " ").strip()

def main():
    # NEVER rmtree OUT: it holds the live DB, the skills mirror and the session docs.
    # Only the generated views are rebuilt.
    os.makedirs(OUT, exist_ok=True)
    for sub in ("by-class", "by-vault-category"):
        p_ = os.path.join(OUT, sub)
        if os.path.isdir(p_): shutil.rmtree(p_)
    os.makedirs(os.path.join(OUT, "by-class"), exist_ok=True)
    os.makedirs(os.path.join(OUT, "by-vault-category"), exist_ok=True)
    os.makedirs(os.path.join(OUT, "scripts"), exist_ok=True)
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    rows = con.execute("""SELECT r.id,r.title,r.program,r.severity,r.weakness,r.bounty,r.votes,r.reporter,
        r.disclosed_at,r.substate, (SELECT length(body) FROM bodies b WHERE b.id=r.id) AS blen
        FROM reports r""").fetchall()
    print("rows", len(rows))

    by_class, by_dir = {}, {}
    for r in rows:
        cid = class_of(r["weakness"], r["title"])
        by_class.setdefault(cid, []).append(r)
        d = None
        w = (r["weakness"] or "") + " " + (r["title"] or "")
        for dd, rx in REFINED:
            if rx.search(w): d = dd; break
        if d is None:
            for c in CLASSES_C:
                if c[0] == cid: d = c[3]; break
        d = d or "16_Information-Disclosure/"
        by_dir.setdefault(d, []).append(r)

    money = lambda v: f"${v:,.0f}" if v else "-"
    # ---- per class files
    names = {c[0]: (c[1], c[3]) for c in CLASSES_C}; names["OTHER"] = ("Other weaknesses", "-")
    for n, (cid, lst) in enumerate(sorted(by_class.items(), key=lambda kv: -len(kv[1])), 1):
        lst.sort(key=lambda r: (-(r["bounty"] or 0), -(r["votes"] or 0)))
        title, vdir = names.get(cid, (cid, "-"))
        paid = sum(r["bounty"] or 0 for r in lst); np_ = sum(1 for r in lst if r["bounty"])
        bodies = sum(1 for r in lst if r["blen"])
        p = os.path.join(OUT, "by-class", f"{n:02d}_{cid}.md")
        with open(p, "w") as f:
            f.write(f"""---
title: "Vault class {cid} — {title}"
type: dataset-view
class: "{title}"
vault_category: "{vdir}"
rows: {len(lst)}
paid_rows: {np_}
bounty_sum: {paid:,.0f}
full_bodies_available: {bodies}
source: "public HackerOne vault (hackerone disclosed), harvested {TODAY}"
---

# {cid} — {title}

{len(lst)} rows · {np_} with a bounty figure · **${paid:,.0f}** total · {bodies} with full write-up stored.
Playbook: `Vault/{vdir}` · Dataset: `Vault/_VAULT/reports.sqlite` (`SELECT * FROM reports WHERE ...`).

| Report | Program | Severity | Bounty | Votes | Disclosed | Weakness | Title |
|---|---|---|---|---|---|---|---|
""")
            for r in lst:
                dt = (r["disclosed_at"] or "")[:10]
                f.write(f"| [{r['id']}](https://hackerone.com/reports/{r['id']}) | {esc(r['program'])} | {esc(r['severity'])} | {money(r['bounty'])} | {r['votes'] or 0} | {dt} | {esc(r['weakness'])} | {esc(r['title'])} |\n")
    # ---- per vault category files
    for d, lst in sorted(by_dir.items()):
        lst.sort(key=lambda r: (-(r["bounty"] or 0), -(r["votes"] or 0)))
        paid = sum(r["bounty"] or 0 for r in lst); np_ = sum(1 for r in lst if r["bounty"])
        bodies = sum(1 for r in lst if r["blen"])
        slug = d.strip("/").replace("/", "_")
        p = os.path.join(OUT, "by-vault-category", f"{slug}.md")
        with open(p, "w") as f:
            f.write(f"""---
title: "Reports routed to Vault/{d}"
type: dataset-view
vault_category: "{d}"
rows: {len(lst)}
paid_rows: {np_}
bounty_sum: {paid:,.0f}
full_bodies_available: {bodies}
source: "public HackerOne vault (hackerone disclosed), harvested {TODAY}"
---

# → `Vault/{d}`

{len(lst)} rows routed here · {np_} paid · **${paid:,.0f}** · {bodies} full write-ups stored.

| Report | Program | Severity | Bounty | Votes | Disclosed | Weakness | Title |
|---|---|---|---|---|---|---|---|
""")
            for r in lst:
                dt = (r["disclosed_at"] or "")[:10]
                f.write(f"| [{r['id']}](https://hackerone.com/reports/{r['id']}) | {esc(r['program'])} | {esc(r['severity'])} | {money(r['bounty'])} | {r['votes'] or 0} | {dt} | {esc(r['weakness'])} | {esc(r['title'])} |\n")
    # ---- csv
    with open(os.path.join(OUT, "all-reports.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id","title","program","severity","weakness","class","vault_category","bounty","votes","reporter","disclosed_at","substate","has_body"])
        for r in sorted(rows, key=lambda r: -(r["bounty"] or 0)):
            cid = class_of(r["weakness"], r["title"])
            vdir = next((dd for dd, rx in REFINED if rx.search((r["weakness"] or "") + " " + (r["title"] or ""))), None)
            if not vdir:
                vdir = next((c[3] for c in CLASSES_C if c[0] == cid), "-")
            w.writerow([r["id"], r["title"], r["program"], r["severity"], r["weakness"], cid, vdir,
                        r["bounty"], r["votes"], r["reporter"], r["disclosed_at"], r["substate"], 1 if r["blen"] else 0])
    # ---- sqlite copy (replaced at the end by the refresh script)
    # the DB lives in OUT already; only copy when the source is a different file
    target = os.path.join(OUT, "reports.sqlite")
    if os.path.abspath(DB) != os.path.abspath(target):
        try:
            con.execute("VACUUM INTO ?", (target,))
        except Exception:
            shutil.copy(DB, target)
    # ---- README
    tot_paid = sum(r["bounty"] or 0 for r in rows); npaid = sum(1 for r in rows if r["bounty"])
    bodies = sum(1 for r in rows if r["blen"])
    st = con.execute("""SELECT SUM(http_status=200 AND length(body)>0) full_body,
        SUM(http_status=200 AND (body IS NULL OR body='')) summary_only,
        SUM(http_status=404) gone, SUM(http_status NOT IN (200,404)) other,
        SUM(size) bytes FROM bodies""").fetchone()
    full_body, summary_only, gone, other, bytes_ = [x or 0 for x in st]
    cls_table = "\n".join(
        f"| {cid} | {names.get(cid,('',''))[0]} | {len(l)} | ${sum(x['bounty'] or 0 for x in l):,.0f} | `by-class/` | `Vault/{names.get(cid,('','-'))[1]}` |"
        for cid, l in sorted(by_class.items(), key=lambda kv: -len(kv[1])))
    dir_table = "\n".join(
        f"| `{d}` | {len(l)} | ${sum(x['bounty'] or 0 for x in l):,.0f} | "
        f"[`by-vault-category/{d.strip('/')}.md`](by-vault-category/{d.strip('/')}.md) |"
        for d, l in sorted(by_dir.items(), key=lambda kv: -len(kv[1])))
    with open(os.path.join(OUT, "README.md"), "w") as f:
        f.write(f"""---
title: "Vault/_VAULT — the disclosed-report dataset behind the playbooks"
type: index
built: "{TODAY}"
rows: {len(rows)}
paid_rows: {npaid}
bounty_sum: {tot_paid:,.0f}
full_bodies_available: {bodies}
source: "public HackerOne disclosed-vault, harvested {TODAY}"
---

# Vault/_VAULT — the full vault

Every publicly disclosed HackerOne report exposed by the public HackerOne dataset, harvested {TODAY}:
**{len(rows):,} reports · {npaid:,} with a bounty figure · ${tot_paid:,.0f} · {bodies:,} with the full write-up stored.**

This is a *dataset layer*, not a playbook. The playbooks (`Vault/XXE/`, `Vault/RCE/`, …) stay the
teaching layer; this directory is the case stock you can query, sort and cite.

## Write-up availability (reconciled against `hackerone.com/reports/<id>.json`, {TODAY})

| State | Rows | Meaning |
|---|---|---|
| Full write-up stored | {full_body:,} | `bodies.body` holds the researcher's own write-up |
| Summary only | {summary_only:,} | HackerOne published the program summary; the researcher left the body blank |
| Delisted (404) | {gone:,} | Report no longer public on HackerOne — title/bounty kept from the list, body never quoted |
| Other status | {other:,} | fetch never resolved; not quoted |

{full_body + summary_only + gone + other:,} rows accounted for = the full list. Stored write-up text: {bytes_/1e6:,.0f} MB.
Nothing is invented: a row without a body is shown as such, and a 404 is never paraphrased.

## Files

| File | What it is |
|---|---|
| [`all-reports.csv`](all-reports.csv) | Every report, one row: id, title, program, severity, weakness, class, routed vault category, bounty, votes, reporter, disclosed date, substate, has_body |
| [`reports.sqlite`](reports.sqlite) | Tables `reports` (metadata, {len(rows):,} rows) and `bodies` (summary + full write-up + asset + CVEs). Query it directly. |
| `by-class/NN_<CLASS>.md` | All reports of one class, richest first |
| `by-vault-category/<dir>.md` | The same reports routed into our playbook directories |
| [`scripts/extract_report.py`](scripts/extract_report.py) | `python3 extract_report.py 510152` → writes that report's full write-up as markdown |
| table `documents` | Full text of every markdown document we wrote in this vault (playbooks, modules, registers, views), with title/type/category/sha256 + FTS5 index |
| table `documents_fts` | Full-text search over those documents |
| `scripts/refresh.sh` | Re-run the two harvesters and rebuild these views |

## Skills layer

Every skill in this profile is mirrored to `_VAULT/skills/` and indexed in `documents` (dir=`skills`),
so one hybrid query reaches doctrine and evidence together.

| Fact | Value |
|---|---|
| skills mirrored | 209 skills (SKILL.md + references/templates/scripts) |
| skill markdown indexed | 3,194 docs (identical copies stored once) |
| scoping | `search.py --source skills` (doctrine) · `--source vault` (playbooks + reports) |

```bash
sqlite3 reports.sqlite "SELECT dir,COUNT(*) FROM documents GROUP BY 1 ORDER BY 2 DESC LIMIT 5;"
```

## Bypass + technique indexes

| Table | Rows | What it answers |
|---|---|---|
| `techniques` | 1,409 | class → named technique → passage (`vault_techniques`, `techniques.py`) |
| `bypasses` | 8,739 | protection → passage → payload (`vault_bypass`, `bypass.py`) · 1,371 rows carry a literal payload |
| `payloads` | 19,278 | 19,278 unique fenced code blocks, classified + deduped (`vault_payloads`, `payload.py`) |

```bash
python3 techniques.py LFI --grep filter      # named techniques for a class
python3 bypass.py waf --grep cloudflare      # who got past a WAF, and with what
python3 bypass.py csp --show 42              # full passage + payloads
```
Tags: waf · csp · twofa · rate_limit · allowlist · sanitizer · earlier_fix · cors · authz

## Query recipes

```bash
sqlite3 reports.sqlite "SELECT id,program,bounty,title FROM reports WHERE weakness LIKE '%SQL injection%' AND bounty>0 ORDER BY bounty DESC LIMIT 20;"
sqlite3 reports.sqlite "SELECT id,title FROM bodies WHERE body LIKE '%X-Forwarded-Host%' LIMIT 20;"
sqlite3 reports.sqlite "SELECT program,COUNT(*),SUM(bounty) FROM reports GROUP BY 1 ORDER BY 3 DESC LIMIT 20;"
sqlite3 reports.sqlite "SELECT id,title,substr(body,1,600) FROM bodies WHERE body LIKE '%WAF%bypass%' LIMIT 5;"
sqlite3 reports.sqlite "SELECT path,title FROM documents_fts WHERE documents_fts MATCH 'cache poisoning' LIMIT 10;"
sqlite3 reports.sqlite "SELECT dir,COUNT(*) FROM documents GROUP BY 1 ORDER BY 2 DESC;"
```

## Coverage by class

| Class | Name | Rows | Bounties | View | Playbook |
|---|---|---|---|---|---|
{cls_table}

## Routed into our playbook categories

| Vault dir | Rows | Bounties | View |
|---|---|---|---|
{dir_table}

## Provenance & honesty

- Source is the public unauthenticated endpoints: `the public HackerOne dataset/api/reports` (the list) and
  `hackerone.com/reports/<id>.json` (the write-ups). No private data, no API key.
- Bounty figures are HackerOne's `bounty_amount`; a blank means no figure was shown, **not** that nothing was paid.
- Titles come from the program's published report. Severity/weakness are the program's own fields where set;
  where a program set no weakness the class is inferred from the title by their published rules —
  treat those as a keyword guess, not a fact.
- The repo (`~/Bugbounty/vault/the public HackerOne dataset`) pins `next@16.4.6`; the site is the reference
  implementation of the same idea as this vault: reports → class → playbook.
""")
    with open(os.path.join(OUT, "scripts", "extract_report.py"), "w") as f:
        f.write('''#!/usr/bin/env python3
"""Dump one report's full write-up as markdown: extract_report.py <id> [outdir]"""
import sqlite3, sys, os, json
here = os.path.dirname(os.path.abspath(__file__))
db = os.path.join(os.path.dirname(here), "reports.sqlite")
rid = int(sys.argv[1]); outdir = sys.argv[2] if len(sys.argv) > 2 else "."
con = sqlite3.connect(db); con.row_factory = sqlite3.Row
r = con.execute("SELECT * FROM bodies WHERE id=?", (rid,)).fetchone()
if not r: sys.exit(f"report {rid} not stored. Run: python3 ~/Bugbounty/vault/harvest_bodies.py (resumable)")
md = [f"# {r['title']}", "", f"- Program: {r['program']}", f"- Severity: {r['severity']}",
      f"- Weakness: {r['weakness']}", f"- Bounty: {r['bounty']}", f"- Reporter: {r['reporter']}",
      f"- Disclosed: {r['disclosed_at']}", f"- Asset: {r['asset']} ({r['asset_type']})",
      f"- CVEs: {r['cve_ids']}", f"- Source: https://hackerone.com/reports/{rid}", "", "## Summary", "",
      r["summary"] or "_(none)_", "", "## Write-up", "", r["body"] or "_(body not public / not stored)_"]
path = os.path.join(outdir, f"report-{rid}.md")
open(path, "w").write("\\n".join(md))
print(path)
''')
    with open(os.path.join(OUT, "scripts", "refresh.sh"), "w") as f:
        f.write("""#!/usr/bin/env bash
# Refresh the dataset layer: metadata -> write-ups -> vault views
set -e
cd ~/Bugbounty/vault
python3 harvest_meta.py
python3 harvest_bodies.py          # resumable; only fetches what is missing
python3 export_to_vault.py
python3 ingest_vault_docs.py       # index every vault .md into the same DB
python3 ingest_skills.py           # mirror + index all skills from ~/.hermes/profiles/batman/skills
python3 dedupe_chunks.py           # exact + near-duplicate chunk removal (tombstoned)
python3 build_techniques.py        # named-technique index (class -> technique -> chunk)
python3 build_bypasses.py          # protection -> passage -> payload index
python3 build_payloads.py          # fenced code blocks -> classified payload table
""")
    os.chmod(os.path.join(OUT, "scripts", "refresh.sh"), 0o755)
    print("class files:", len(by_class), "category files:", len(by_dir))

main()
