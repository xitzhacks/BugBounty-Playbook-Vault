#!/usr/bin/env python3
"""Append/refresh a 'Case stock' block in each playbook README pointing at the _VAULT dataset.
Idempotent: the block is fenced by HTML markers and rewritten in place."""
import csv, os, re, time

VAULT = os.environ.get("VAULT_ROOT", os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "vault"))
CSV = os.path.join(VAULT, "_VAULT", "all-reports.csv")
B, E = "<!-- CASESTOCK-LINK:BEGIN -->", "<!-- CASESTOCK-LINK:END -->"

rows = {}
with open(CSV) as f:
    for r in csv.DictReader(f):
        rows.setdefault(r["vault_category"].strip("/"), []).append(r)

out = []
for d, rs in sorted(rows.items()):
    readme = os.path.join(VAULT, d, "README.md")
    if not os.path.isfile(readme):
        out.append(f"skip (no README): {d}"); continue
    paid = sum(float(r["bounty"]) for r in rs if r["bounty"])
    npaid = sum(1 for r in rs if r["bounty"])
    withbody = sum(1 for r in rs if r["has_body"] == "1")
    top = sorted([r for r in rs if r["bounty"]], key=lambda r: -float(r["bounty"]))[:5]
    lines = [B,
             "",
             "## Case stock — vault (`_VAULT/`)",
             "",
             f"**{len(rs):,} disclosed reports** routed to this category · {npaid:,} with a bounty figure · "
             f"**${paid:,.0f}** · {withbody:,} full write-ups stored locally.",
             "",
             f"- Full list: [`_VAULT/by-vault-category/{d}.md`](../_VAULT/by-vault-category/{d}.md)",
             "- Query: `sqlite3 ../_VAULT/reports.sqlite \"SELECT id,bounty,title FROM reports WHERE ...\"`",
             "- Pull one write-up: `python3 ../_VAULT/scripts/extract_report.py <id>`",
             ""]
    if top:
        lines += ["| Top paid | Program | Bounty |", "|---|---|---|"]
        lines += [f"| [{t['id']}](https://hackerone.com/reports/{t['id']}) {t['title'][:80]} | {t['program']} | ${float(t['bounty']):,.0f} |" for t in top]
        lines.append("")
    lines.append(f"_refreshed {time.strftime('%Y-%m-%d')} from the public HackerOne disclosed-report dataset_")
    lines.append(E)
    block = "\n".join(lines)
    src = open(readme).read()
    src = re.sub(r"<!-- legacy -->?", "", src, flags=re.S)
    if B in src and E in src:
        src = re.sub(re.escape(B) + r".*?" + re.escape(E), block, src, flags=re.S)
    else:
        src = src.rstrip() + "\n\n" + block + "\n"
    open(readme, "w").write(src)
    out.append(f"ok {d}: {len(rs)} rows")

print("\n".join(out))
