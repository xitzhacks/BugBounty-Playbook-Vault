#!/usr/bin/env python3
"""Stage 4: write/refresh a fenced 'Case stock' block in EVERY playbook README.

Idempotent by HTML markers: re-run after each export instead of hand-editing 30+ files.
Reads Vault/_HEXBRAIN/all-reports.csv, groups by vault_category, emits:
  rows / paid rows / bounty total / bodies stored, link to the full list, top-5 paid cases.
"""
import csv, os, re, time

VAULT = "/home/user/projects/FAN/Vault"
CSV = os.path.join(VAULT, "_HEXBRAIN", "all-reports.csv")
B, E = "<!-- HEXBRAIN-CASE-STOCK:BEGIN -->", "<!-- HEXBRAIN-CASE-STOCK:END -->"

rows = {}
with open(CSV) as f:
    for r in csv.DictReader(f):
        rows.setdefault(r["vault_category"].strip("/"), []).append(r)

for d, rs in sorted(rows.items()):
    readme = os.path.join(VAULT, d, "README.md")
    if not os.path.isfile(readme):
        print("skip (no README):", d)
        continue
    paid = sum(float(r["bounty"]) for r in rs if r["bounty"])
    npaid = sum(1 for r in rs if r["bounty"])
    withbody = sum(1 for r in rs if r["has_body"] == "1")
    top = sorted([r for r in rs if r["bounty"]], key=lambda r: -float(r["bounty"]))[:5]
    lines = [B, "", "## Case stock — hexbrain dataset (`_HEXBRAIN/`)", "",
             f"**{len(rs):,} disclosed reports** routed here · {npaid:,} with a bounty figure · "
             f"**${paid:,.0f}** · {withbody:,} full write-ups stored locally.", "",
             f"- Full list: [`_HEXBRAIN/by-vault-category/{d}.md`](../_HEXBRAIN/by-vault-category/{d}.md)",
             "- Query: `sqlite3 ../_HEXBRAIN/hexbrain-reports.sqlite \"SELECT id,bounty,title FROM reports WHERE ...\"`",
             "- Pull one write-up: `python3 ../_HEXBRAIN/scripts/extract_report.py <id>`", ""]
    if top:
        lines += ["| Top paid | Program | Bounty |", "|---|---|---|"]
        lines += [f"| [{t['id']}](https://hackerone.com/reports/{t['id']}) {t['title'][:80]} | {t['program']} | ${float(t['bounty']):,.0f} |" for t in top]
        lines.append("")
    lines += [f"_refreshed {time.strftime('%Y-%m-%d')} from hexbrainai.com public data_", E]
    block = "\n".join(lines)
    src = open(readme).read()
    if B in src and E in src:
        src = re.sub(re.escape(B) + r".*?" + re.escape(E), block, src, flags=re.S)
    else:
        src = src.rstrip() + "\n\n" + block + "\n"
    open(readme, "w").write(src)
    print("ok", d, len(rs))
