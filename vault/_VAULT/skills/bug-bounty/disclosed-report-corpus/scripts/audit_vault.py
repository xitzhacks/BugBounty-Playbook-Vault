#!/usr/bin/env python3
"""Read-only audit of the vault dataset layer. Prints PASS/FAIL per check and a final tally.

Every check compares the DB against the DB, the CSV, the md views, the README's own claims and the
files on disk — the README is a claim, never evidence.

Usage:
    python3 audit_vault.py
    VAULT=/path/to/Vault python3 audit_vault.py
"""
import csv, os, re, subprocess, sqlite3, sys

VAULT = os.environ.get("VAULT", "/home/user/projects/FAN/Vault")
H = os.environ.get("DATASET_DIR", os.path.join(VAULT, "_VAULT"))
DBP = os.path.join(H, "reports.sqlite")

ok = fail = 0


def chk(name, cond, detail=""):
    global ok, fail
    if cond:
        ok += 1; print(f"PASS  {name}" + (f"  [{detail}]" if detail else ""))
    else:
        fail += 1; print(f"FAIL  {name}" + (f"  [{detail}]" if detail else ""))


def main():
    print("=== 1. location ===")
    chk("dataset dir inside vault", os.path.isdir(H), H)
    for f in ("README.md", "all-reports.csv", "reports.sqlite",
              "scripts/extract_report.py", "scripts/refresh.sh"):
        p = os.path.join(H, f)
        chk(f"present: {f}", os.path.isfile(p), f"{os.path.getsize(p):,} B" if os.path.isfile(p) else "missing")

    db = sqlite3.connect(DBP)
    q = lambda s, *a: db.execute(s, a).fetchone()[0]
    n = q("SELECT COUNT(*) FROM reports")
    nb = q("SELECT COUNT(*) FROM bodies")
    full = q("SELECT COUNT(*) FROM bodies WHERE http_status=200 AND length(body)>0")
    summ = q("SELECT COUNT(*) FROM bodies WHERE http_status=200 AND (body IS NULL OR body='') AND length(COALESCE(summary,''))>0")
    gone = q("SELECT COUNT(*) FROM bodies WHERE http_status=404")
    other = q("SELECT COUNT(*) FROM bodies WHERE http_status NOT IN (200,404)")
    paid = q("SELECT COUNT(*) FROM reports WHERE bounty>0")
    bounty = q("SELECT COALESCE(SUM(bounty),0) FROM reports")
    bytes_ = q("SELECT COALESCE(SUM(size),0) FROM bodies WHERE http_status=200")

    print("\n=== 2. sqlite ===")
    chk("integrity_check ok", q("PRAGMA integrity_check") == "ok")
    chk("no duplicate report ids", n == q("SELECT COUNT(DISTINCT id) FROM reports"), str(n))
    chk("every report has a bodies row", nb == n, f"{nb}/{n}")
    chk("full+summary+404+other == total", full + summ + gone + other == n,
        f"{full}+{summ}+{gone}+{other}={full+summ+gone+other}")
    chk("no orphan bodies", q("SELECT COUNT(*) FROM bodies WHERE id NOT IN (SELECT id FROM reports)") == 0)

    print("\n=== 3. csv vs db ===")
    rows = list(csv.DictReader(open(os.path.join(H, "all-reports.csv"))))
    chk("csv rows == db reports", len(rows) == n, f"{len(rows)} vs {n}")
    chk("csv has_body=1 == full", sum(1 for r in rows if r["has_body"] == "1") == full)
    chk("csv paid rows == db", sum(1 for r in rows if float(r["bounty"] or 0) > 0) == paid)
    csv_sum = sum(float(r["bounty"] or 0) for r in rows if r["bounty"] not in ("", "None"))
    chk("csv bounty sum == db", abs(csv_sum - bounty) < 1, f"{csv_sum:,.2f} vs {bounty:,.2f}")
    chk("csv id set == db id set",
        {r["id"] for r in rows} == {str(x[0]) for x in db.execute("SELECT id FROM reports")})

    print("\n=== 4. md views ===")
    md_rows = lambda p: sum(1 for l in open(p) if l.startswith("| [") and "hackerone.com/reports/" in l)
    cls = sorted(os.listdir(os.path.join(H, "by-class")))
    cat = sorted(os.listdir(os.path.join(H, "by-vault-category")))
    chk("class file row total == total", sum(md_rows(os.path.join(H, "by-class", f)) for f in cls) == n,
        str(len(cls)) + " files")
    chk("category file row total == total", sum(md_rows(os.path.join(H, "by-vault-category", f)) for f in cat) == n,
        str(len(cat)) + " files")

    print("\n=== 5. readme claims ===")
    rm = open(os.path.join(H, "README.md")).read()
    def claim(k):
        m = re.search(rf"^{k}:\s*([\d,]+)$", rm, re.M)
        return int(m.group(1).replace(",", "")) if m else None
    chk("rows", claim("rows") == n)
    chk("paid_rows", claim("paid_rows") == paid)
    chk("bounty_sum (rounded; exact %.2f)" % bounty, claim("bounty_sum") == round(bounty), str(claim("bounty_sum")))
    chk("full_bodies_available", claim("full_bodies_available") == full)

    print("\n=== 6. wiring ===")
    dirs = [d for d in sorted(os.listdir(VAULT))
            if os.path.isdir(os.path.join(VAULT, d)) and not d.startswith(("_", "."))]
    missing = [d for d in dirs
               if not (os.path.isfile(os.path.join(VAULT, d, "README.md"))
                       and "CASESTOCK-LINK:BEGIN" in open(os.path.join(VAULT, d, "README.md")).read())]
    chk(f"all {len(dirs)} playbook READMEs carry case-stock block", not missing,
        str(missing) if missing else f"{len(dirs)}/{len(dirs)}")

    print("\n=== 7. extract end-to-end ===")
    sid = db.execute("SELECT id FROM bodies WHERE http_status=200 AND length(body)>2000 ORDER BY RANDOM() LIMIT 1").fetchone()[0]
    r = subprocess.run([sys.executable, os.path.join(H, "scripts", "extract_report.py"), str(sid), "/tmp"],
                       capture_output=True, text=True)
    p = f"/tmp/report-{sid}.md"
    chk("extracts full write-up", r.returncode == 0 and os.path.isfile(p) and os.path.getsize(p) > 2000, f"id={sid}")

    print("\n=== 8. documents ===")
    n_docs = q("SELECT COUNT(*) FROM documents")
    on_disk = sum(1 for dp, ds, fs in os.walk(VAULT) for f in fs
                  if f.lower().endswith(".md")
                  and not any(x.startswith(".") for x in os.path.relpath(dp, VAULT).split(os.sep) if x not in (".", "")))
    chk("documents == md on disk", n_docs == on_disk, f"{n_docs} vs {on_disk}")
    chk("all docs have text + sha256", q("SELECT COUNT(*) FROM documents WHERE length(text)<10 OR sha256 IS NULL") == 0)
    chk("no path escapes", q("SELECT COUNT(*) FROM documents WHERE path LIKE '..%' OR path LIKE '/%'") == 0)
    try:
        hits = q("SELECT COUNT(*) FROM documents_fts WHERE documents_fts MATCH 'payload'")
        chk("documents_fts searchable", hits > 0, f"{hits} hits")
    except Exception as e:
        chk("documents_fts searchable", False, str(e))

    print(f"\nwrite-up text: {bytes_/1e6:,.1f} MB across {full:,} reports")
    print(f"\n{'='*46}\nRESULT: {ok} passed, {fail} failed\n{'='*46}")
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
