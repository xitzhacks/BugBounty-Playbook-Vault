---
title: "LDAP/XPath source index — provenance, funnel, DB reconciliation, limitations"
type: source-index
built: "2026-11-07"
---

# Source index — LDAP/XPath build

## 1. Corpus provenance

- **Primary source**: `/home/user/tools/h1-brain/disclosed_reports.db` — the h1-brain pre-built
  SQLite corpus of publicly disclosed, bounty-awarded HackerOne reports (**3,673 rows**,
  table `disclosed_reports` with fields `id, title, vulnerability_information, weakness_name,
  program_handle, asset_identifier, asset_type, cve_ids, bounty_amount`). The DB was fetched
  from the repo's Git-LFS pointer and sha256-verified:
  `8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4`. No live HackerOne fetch
  this build.
- **Classifier outputs**: `/home/user/opencode-work/h1brain/classified.json` (bucket
  `ldap-xpath` = 11 rows) and `/home/user/opencode-work/h1brain/module_map_all.json`
  (`ldap-xpath.codeql-corpus-block` = 11 ids, `_adjacent_unclassified` = 1 id). Bodies were
  re-read from the DB for the archive dump; the JSON classified rows match the DB on
  `id/title/body/program/bounty` for all 11 rows.
- **In-vault archive**: `references/archive/lx-bodies-full-dump.txt` (11/11 bodies — each the
  54-byte GHSL pointer line), `references/archive/classes.json` (frozen module assignment).

## 2. Classification funnel

1. **Keyword/labeled net** over all 3,673 rows: `classified.json` bucket `ldap-xpath` selected
   **11 rows** by keyword arms (`ldap` / `xpath`) where `weakness_name` is null — the rows
   entered via title keywords (`src` values `None/keyword:ldap`, `None/keyword:xpath`), not
   via triage labels. DB `weakness_name` is null for all 11 rows; language/CWE are read from
   titles only.
2. **Module split** (frozen in `classes.json`): `codeql-corpus-block` holds all 11 ids
   (787113, 824925, 852316, 956295, 1050706, 1095708, 1133572, 1212273, 1287575, 1350076,
   1397942). `_adjacent_unclassified` holds one more id (1133573, XQuery Injection, CWE-652)
   which is **not** in this vault — recorded so the bucket reconciliation is exact, excluded
   from every count.
3. **Per-body read**: all 11 bodies read from the DB. Each is 54 bytes
   (`This bug was reported directly to GitHub Security Lab.`). Evidence: 0 full-body /
   11 metadata-only. The vault is a corpus block (cf. RCE module 09); zero quotes.
4. **DB reconciliation**: every bucket row verified present in `disclosed_reports` with
   identical title, bounty, and body length (54). Programs match the classifier
   (`github-security-lab` ×11). No live-target row exists in the bucket.

## 3. Bounty accounting

- **Rule**: DB `bounty_amount` where present; `None` recorded as no figure (not $0). Blank ≠
  unpaid — HackerOne does not always publish figures.
- Corpus: 8/11 rows carry figures, totaling **$19,000** (max $4,500, LX-1212273). Five rows
  sit at the flat $1,800 GHSL query tier. See case-register.md for per-row labels and the
  arithmetic.
- **What the money prices**: GHSL CodeQL-query authorship tiers. No row prices a live LDAP
  directory or XPath sink; the module teaches absence discipline, not payout estimation.

## 4. Era discipline & limitations

1. **Single-source corpus**: all 11 rows are GHSL. No commercial-program LDAP/XPath row
   exists in this bucket to price a live-service ranking.
2. **Titles-only taxonomy**: language (Java 5 · Python 3 · Go 2 · JavaScript 1) and CWE
   (090/90 · 522 · 287 · 297 · 643) are title-read. DB weakness labels are null; a
   title-vs-body conflict cannot exist because no body exists.
3. **Adjacent row outside**: 1133573 (XQuery, CWE-652) is out of scope and out of every
   count. A future build may absorb it into the XXE vault; this vault names it so nothing
   is silently dropped or silently merged.
4. **Bounty `None` ≠ unpaid**: 3/11 rows have no figure; $19,000 is a corpus floor.
5. **Quote discipline**: zero blockquotes carry technique content. The single repeated
   GHSL pointer line is described, not used as evidence for any technique claim. No invented
   LDAP filters, XPath expressions, or remediation paragraphs.
6. **Playbook scope**: P2–P3 probe steps are labeled non-corpus doctrine (method family from
   the SQLi/XXE vaults). They must be validated against a lab directory/XML parser in
   scope, never presented as corpus-observed.
7. **No live testing was performed.** Directory/auth work stays in the lab (playbook P5,
   production gate).
