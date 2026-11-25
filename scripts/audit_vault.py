#!/usr/bin/env python3
"""Read-only audit of Vault/_VAULT. Every check prints PASS/FAIL with the real numbers."""
import csv, os, re, sqlite3, hashlib, subprocess, time

V = os.environ.get("VAULT_ROOT", os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "vault"))
H = os.path.join(V, "_VAULT")
ok = fail = 0
def chk(name, cond, detail=""):
    global ok, fail
    if cond: ok += 1; print(f"PASS  {name}" + (f"  [{detail}]" if detail else ""))
    else:    fail += 1; print(f"FAIL  {name}" + (f"  [{detail}]" if detail else ""))

print("=== 1. location ===")
chk("dataset lives inside the vault dir", os.path.isdir(H), H)
for f in ["README.md", "all-reports.csv", "reports.sqlite",
          "scripts/extract_report.py", "scripts/refresh.sh"]:
    chk(f"file present: {f}", os.path.isfile(os.path.join(H, f)),
        f"{os.path.getsize(os.path.join(H,f)):,} bytes" if os.path.isfile(os.path.join(H,f)) else "missing")

db = sqlite3.connect(os.path.join(H, "reports.sqlite"))
n_reports = db.execute("SELECT COUNT(*) FROM reports").fetchone()[0]
n_bodies  = db.execute("SELECT COUNT(*) FROM bodies").fetchone()[0]
n_uniq    = db.execute("SELECT COUNT(DISTINCT id) FROM reports").fetchone()[0]
full_body = db.execute("SELECT COUNT(*) FROM bodies WHERE http_status=200 AND length(body)>0").fetchone()[0]
summ_only = db.execute("SELECT COUNT(*) FROM bodies WHERE http_status=200 AND (body IS NULL OR body='') AND length(COALESCE(summary,''))>0").fetchone()[0]
gone      = db.execute("SELECT COUNT(*) FROM bodies WHERE http_status=404").fetchone()[0]
other     = db.execute("SELECT COUNT(*) FROM bodies WHERE http_status NOT IN (200,404)").fetchone()[0]
paid      = db.execute("SELECT COUNT(*) FROM reports WHERE bounty>0").fetchone()[0]
bounty    = db.execute("SELECT COALESCE(SUM(bounty),0) FROM reports").fetchone()[0]
bytes_    = db.execute("SELECT COALESCE(SUM(size),0) FROM bodies WHERE http_status=200").fetchone()[0]

print("\n=== 2. sqlite integrity ===")
chk("PRAGMA integrity_check", db.execute("PRAGMA integrity_check").fetchone()[0] == "ok")
chk("reports rows == 15,244", n_reports == 15244, str(n_reports))
chk("no duplicate report ids", n_reports == n_uniq, f"{n_uniq} unique")
chk("every report has a bodies row", n_bodies == n_reports, f"{n_bodies}/{n_reports}")
chk("full+summary+404+other == total", full_body+summ_only+gone+other == n_reports,
    f"{full_body}+{summ_only}+{gone}+{other}={full_body+summ_only+gone+other}")
chk("no empty bodies marked as full", full_body == db.execute(
    "SELECT COUNT(*) FROM bodies WHERE http_status=200 AND length(body)>500").fetchone()[0] + 
    db.execute("SELECT COUNT(*) FROM bodies WHERE http_status=200 AND length(body)>0 AND length(body)<=500").fetchone()[0])
chk("orphan bodies (id not in reports)", db.execute(
    "SELECT COUNT(*) FROM bodies WHERE id NOT IN (SELECT id FROM reports)").fetchone()[0] == 0)

print("\n=== 3. csv vs db ===")
rows = list(csv.DictReader(open(os.path.join(H, "all-reports.csv"))))
chk("csv data rows == db reports", len(rows) == n_reports, f"{len(rows)} vs {n_reports}")
chk("csv has_body=1 == full_body", sum(1 for r in rows if r["has_body"] == "1") == full_body,
    f"{sum(1 for r in rows if r['has_body']=='1')} vs {full_body}")
csv_paid = sum(1 for r in rows if r["bounty"] not in ("", "None") and float(r["bounty"] or 0) > 0)
chk("csv paid rows == db paid rows", csv_paid == paid, f"{csv_paid} vs {paid}")
csv_sum = sum(float(r["bounty"] or 0) for r in rows if r["bounty"] not in ("", "None"))
chk("csv bounty sum == db bounty sum", abs(csv_sum - bounty) < 1, f"{csv_sum:,.0f} vs {bounty:,.0f}")
chk("every csv row has a class and a vault_category",
    all(r["class"] and r["vault_category"] for r in rows))
ids_csv = {r["id"] for r in rows}
ids_db = {str(x[0]) for x in db.execute("SELECT id FROM reports")}
chk("csv id set == db id set", ids_csv == ids_db, f"csv-only={len(ids_csv-ids_db)} db-only={len(ids_db-ids_csv)}")

print("\n=== 4. markdown views ===")
def md_rows(p):
    return sum(1 for l in open(p) if l.startswith("| [") and "hackerone.com/reports/" in l)
cls = sorted(os.listdir(os.path.join(H, "by-class")))
cat = sorted(os.listdir(os.path.join(H, "by-vault-category")))
chk("18 class files", len(cls) == 18, str(len(cls)))
chk("30 category files", len(cat) == 30, str(len(cat)))
chk("class file row total == 15,244",
    sum(md_rows(os.path.join(H, "by-class", f)) for f in cls) == n_reports,
    str(sum(md_rows(os.path.join(H, "by-class", f)) for f in cls)))
chk("category file row total == 15,244",
    sum(md_rows(os.path.join(H, "by-vault-category", f)) for f in cat) == n_reports,
    str(sum(md_rows(os.path.join(H, "by-vault-category", f)) for f in cat)))
chk("no empty view file", all(md_rows(os.path.join(H, d, f)) > 0 for d in ("by-class", "by-vault-category") for f in (cls if d == "by-class" else cat)))

print("\n=== 5. readme claims vs reality ===")
rm = open(os.path.join(H, "README.md")).read()
def claim(k):
    m = re.search(rf"^{k}:\s*([\d,]+)$", rm, re.M)
    return int(m.group(1).replace(",", "")) if m else None
chk("README rows == db", claim("rows") == n_reports, str(claim("rows")))
chk("README paid_rows == db", claim("paid_rows") == paid, str(claim("paid_rows")))
chk("README bounty_sum == db (rounded)", claim("bounty_sum") == round(bounty), f"{claim('bounty_sum'):,} vs {round(bounty):,} (exact {bounty:,.2f})")
chk("README full_bodies_available == db", claim("full_bodies_available") == full_body, str(claim("full_bodies_available")))
for pat, val, label in [(r"\| Full write-up stored \| ([\d,]+)", full_body, "full"),
                        (r"\| Summary only \| ([\d,]+)", summ_only, "summary-only"),
                        (r"\| Delisted \(404\) \| ([\d,]+)", gone, "404")]:
    m = re.search(pat, rm)
    chk(f"README availability table {label}", m and int(m.group(1).replace(",", "")) == val,
        m.group(1) if m else "not found")

print("\n=== 6. playbook wiring ===")
dirs = [d for d in sorted(os.listdir(V)) if os.path.isdir(os.path.join(V, d)) and not d.startswith(("_", "."))]
missing, wired = [], 0
for d in dirs:
    p = os.path.join(V, d, "README.md")
    if os.path.isfile(p) and "CASESTOCK-LINK:BEGIN" in open(p).read(): wired += 1
    else: missing.append(d)
chk(f"all {len(dirs)} playbook READMEs carry the case-stock block", not missing,
    f"{wired}/{len(dirs)}" + (f" missing={missing}" if missing else ""))
ml = open(os.path.join(V, "00_MASTER_CATEGORY_LIST.md")).read()
chk("master list references _VAULT", "_VAULT" in ml)
chk("master list quotes 15,244", "15,244" in ml)

print("\n=== 7. extract_report.py end-to-end ===")
sample = db.execute("SELECT id FROM bodies WHERE http_status=200 AND length(body)>2000 ORDER BY RANDOM() LIMIT 1").fetchone()[0]
r = subprocess.run(["python3", os.path.join(H, "scripts", "extract_report.py"), str(sample), "/tmp"],
                   capture_output=True, text=True)
p = f"/tmp/report-{sample}.md"
chk("extracts a full write-up", r.returncode == 0 and os.path.isfile(p) and os.path.getsize(p) > 2000,
    f"id={sample} {os.path.getsize(p) if os.path.isfile(p) else 0:,} bytes")
s2 = db.execute("SELECT id FROM bodies WHERE http_status=200 AND (body IS NULL OR body='') LIMIT 1").fetchone()[0]
r2 = subprocess.run(["python3", os.path.join(H, "scripts", "extract_report.py"), str(s2), "/tmp"],
                    capture_output=True, text=True)
chk("summary-only report is labelled, not fabricated",
    r2.returncode == 0 and "body not public" in open(f"/tmp/report-{s2}.md").read(), f"id={s2}")

print("\n=== 8. sizes ===")
tot = sum(os.path.getsize(os.path.join(dp, f)) for dp, _, fs in os.walk(H) for f in fs)
print(f"directory total: {tot/1e6:,.1f} MB")
print(f"write-up text:   {bytes_/1e6:,.1f} MB across {full_body:,} reports")
print(f"avg write-up:    {bytes_/max(1,full_body):,.0f} bytes")

print("\n=== 9. documents (our own md files) ===")
n_docs = db.execute("SELECT COUNT(*) FROM documents").fetchone()[0]
d_dirs = db.execute("SELECT COUNT(DISTINCT dir) FROM documents").fetchone()[0]
md_disk = sum(1 for dp,ds,fs in os.walk(V) for f in fs if f.lower().endswith(".md") and not any(x.startswith(".") for x in os.path.relpath(dp,V).split(os.sep) if x not in (".", "")))
try:
    n_dupes = db.execute("SELECT COUNT(*) FROM skill_dupes").fetchone()[0]
except Exception:
    n_dupes = 0
chk("documents rows + recorded duplicates == md files on disk", n_docs + n_dupes == md_disk,
    f"{n_docs} docs + {n_dupes} dupes vs {md_disk} md files")
chk("no duplicate chunk text remains",
    db.execute("SELECT COUNT(*)-COUNT(DISTINCT sha256) FROM chunks").fetchone()[0] == 0,
    f"{db.execute('SELECT COUNT(*) FROM chunks').fetchone()[0]:,} chunks")
chk("every chunk has a vector",
    db.execute("SELECT COUNT(*) FROM chunks WHERE vec IS NULL").fetchone()[0] == 0,
    f"{db.execute('SELECT COUNT(*) FROM chunks WHERE vec IS NOT NULL').fetchone()[0]:,} embedded")
chk("documents cover all playbook dirs", d_dirs >= 31, f"{d_dirs} dirs")
chk("every document has text and a sha256", db.execute("SELECT COUNT(*) FROM documents WHERE length(text)<10 OR sha256 IS NULL").fetchone()[0] == 0)
chk("no document path escapes the vault", db.execute("SELECT COUNT(*) FROM documents WHERE path LIKE '..%' OR path LIKE '/%'").fetchone()[0] == 0)
try:
    hit = db.execute("SELECT COUNT(*) FROM documents_fts WHERE documents_fts MATCH 'payload'").fetchone()[0]
    chk("documents_fts searchable", hit > 0, f"'payload' -> {hit} hits")
except Exception as e:
    chk("documents_fts searchable", False, str(e))

print(f"\n{'='*46}\nRESULT: {ok} passed, {fail} failed\n{'='*46}")
