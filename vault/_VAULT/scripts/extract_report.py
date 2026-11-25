#!/usr/bin/env python3
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
open(path, "w").write("\n".join(md))
print(path)
