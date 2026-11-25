#!/usr/bin/env python3
"""Audit a vulnerability-report corpus DB. Read-only. Prints PASS/FAIL and exits non-zero on failure.

  python3 audit_corpus.py <db.sqlite> [vault_root]

Checks: sqlite integrity, row reconciliation, csv-vs-db, view files, README frontmatter claims,
documents sha256 vs disk, FTS reachable. Nothing here writes.
"""
import csv, hashlib, os, re, sqlite3, sys

ok = fail = 0
def chk(name, cond, detail=""):
    global ok, fail
    if cond: ok += 1; print(f"PASS  {name}" + (f"  [{detail}]" if detail else ""))
    else:    fail += 1; print(f"FAIL  {name}" + (f"  [{detail}]" if detail else ""))

def main():
    if len(sys.argv) < 2:
        sys.exit("usage: audit_corpus.py <db.sqlite> [vault_root]")
    db_path = os.path.abspath(sys.argv[1])
    root = os.path.abspath(sys.argv[2]) if len(sys.argv) > 2 else os.path.dirname(db_path)
    con = sqlite3.connect(db_path)

    print("=== integrity ===")
    chk("PRAGMA integrity_check", con.execute("PRAGMA integrity_check").fetchone()[0] == "ok")
    reports = con.execute("SELECT COUNT(*) FROM reports").fetchone()[0]
    uniq = con.execute("SELECT COUNT(DISTINCT id) FROM reports").fetchone()[0]
    bodies = con.execute("SELECT COUNT(*) FROM bodies").fetchone()[0]
    chk("no duplicate report ids", reports == uniq, f"{uniq} unique of {reports}")
    chk("one bodies row per report", bodies == reports, f"{bodies}/{reports}")

    print("\n=== reconciliation ===")
    full = con.execute("SELECT COUNT(*) FROM bodies WHERE http_status=200 AND length(body)>0").fetchone()[0]
    summ = con.execute("SELECT COUNT(*) FROM bodies WHERE http_status=200 AND (body IS NULL OR body='')").fetchone()[0]
    gone = con.execute("SELECT COUNT(*) FROM bodies WHERE http_status=404").fetchone()[0]
    other = con.execute("SELECT COUNT(*) FROM bodies WHERE http_status NOT IN (200,404)").fetchone()[0]
    chk("full+summary+404+other == total", full+summ+gone+other == reports,
        f"{full}+{summ}+{gone}+{other}={full+summ+gone+other} of {reports}")

    print("\n=== csv vs db ===")
    csv_path = os.path.join(root, "all-reports.csv")
    if os.path.isfile(csv_path):
        rows = list(csv.DictReader(open(csv_path)))
        chk("csv rows == db reports", len(rows) == reports, f"{len(rows)} vs {reports}")
        ids_csv = {r["id"] for r in rows}
        ids_db = {str(x[0]) for x in con.execute("SELECT id FROM reports")}
        chk("csv id set == db id set", ids_csv == ids_db,
            f"csv-only={len(ids_csv-ids_db)} db-only={len(ids_db-ids_csv)}")
    else:
        print("  (no all-reports.csv, skipped)")

    print("\n=== views ===")
    for sub, expect in (("by-class", None), ("by-vault-category", None)):
        d = os.path.join(root, sub)
        if not os.path.isdir(d): print(f"  (no {sub}, skipped)"); continue
        files = [f for f in os.listdir(d) if f.endswith(".md")]
        total = sum(sum(1 for l in open(os.path.join(d, f)) if l.startswith("| [") and "hackerone.com/reports/" in l) for f in files)
        chk(f"{sub} row total == reports", total == reports, f"{total} in {len(files)} files")

    print("\n=== readme claims ===")
    rp = os.path.join(root, "README.md")
    if os.path.isfile(rp):
        rm = open(rp).read()
        def claim(k):
            m = re.search(rf"^{k}:\s*([\d,]+)$", rm, re.M)
            return int(m.group(1).replace(",", "")) if m else None
        if claim("rows") is not None: chk("README rows == db", claim("rows") == reports, str(claim("rows")))
        paid = con.execute("SELECT COUNT(*) FROM reports WHERE bounty>0").fetchone()[0]
        if claim("paid_rows") is not None: chk("README paid_rows == db", claim("paid_rows") == paid, str(claim("paid_rows")))
        money = con.execute("SELECT COALESCE(SUM(bounty),0) FROM reports").fetchone()[0]
        if claim("bounty_sum") is not None:
            chk("README bounty_sum == db (rounded)", claim("bounty_sum") == round(money),
                f"{claim('bounty_sum'):,} vs {round(money):,} (exact {money:,.2f})")
    else:
        print("  (no README, skipped)")

    print("\n=== documents vs disk ===")
    try:
        docs = con.execute("SELECT path, sha256, bytes FROM documents").fetchall()
    except sqlite3.OperationalError:
        docs = []
        print("  (no documents table, skipped)")
    bad = []
    for p, h, b in docs:
        fp = p if os.path.isabs(p) else os.path.join(root, p)
        if not os.path.isfile(fp): bad.append((p, "missing")); continue
        raw = open(fp, "rb").read()
        if hashlib.sha256(raw).hexdigest() != h: bad.append((p, "sha mismatch"))
        elif len(raw) != b: bad.append((p, "size mismatch"))
    if docs:
        chk(f"{len(docs)} documents identical to disk", not bad,
            f"{len(docs)-len(bad)} ok" + (f", first problem {bad[0]}" if bad else ""))

    print("\n=== fts reachable ===")
    for t in ("reports_fts", "documents_fts", "chunks_fts"):
        try:
            n = con.execute(f"SELECT COUNT(*) FROM {t} WHERE {t} MATCH 'security'").fetchone()[0]
            chk(f"{t} searchable", n > 0, f"{n} hits")
        except sqlite3.OperationalError as e:
            print(f"  ({t} absent: {e})")

    total_bytes = con.execute("SELECT COALESCE(SUM(size),0) FROM bodies WHERE http_status=200").fetchone()[0]
    print(f"\nwrite-up text stored: {total_bytes/1e6:,.1f} MB across {full:,} reports "
          f"(avg {total_bytes/max(1,full):,.0f} bytes)")
    print(f"\n{'='*46}\nRESULT: {ok} passed, {fail} failed\n{'='*46}")
    sys.exit(1 if fail else 0)

if __name__ == "__main__":
    main()
