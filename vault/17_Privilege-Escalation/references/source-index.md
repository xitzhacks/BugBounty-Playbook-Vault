---
title: "Privilege Escalation source index — provenance, funnel, classification mechanics, limitations"
type: source-index
built: "2026-11-07"
---

# Source index — Privilege Escalation build

## 1. Roster provenance

- **Primary source**: `/home/user/tools/h1-brain/disclosed_reports.db` — the h1-brain pre-built SQLite corpus of publicly disclosed, bounty-awarded HackerOne reports (3,673 rows). The repo stores the DB as a Git-LFS pointer; the real file was fetched from `media.githubusercontent.com` and sha256-verified: `8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4`. No live HackerOne fetch this build.
- **Row fields**: `id, title, vulnerability_information, weakness_name, program_handle, asset_identifier, asset_type, cve_ids, bounty_amount`. Full report bodies in `vulnerability_information` (roster avg ~2.3 KB; this bucket's bodies run 54–16,763 bytes).
- **Working copies**: `/home/user/opencode-work/h1brain/{classified.json, module_map_all.json}` (classifier v1 output + module merge map). In-vault archive: `references/archive/PRIV-bodies-full-dump.txt` (172/172 bodies), `references/archive/classes.json` (frozen module assignment), `references/archive/meta.json`.

## 2. Classification funnel

- 3,673 DB rows → `classified.json` bucket `priv-esc` = **148 rows** (126 `Privilege Escalation` + 22 `Improper Authorization` by DB `weakness_name`; bucket key `src` is `Privilege Escalation` for all 148).
- `module_map_all.json` under `priv-esc` merges the bucket with **`_adjacent_unclassified` = 24 rows** from the classifier's `unclassified` pool (468 rows total; the 24 carry `weakness_name = None` in the DB). Merged modules:
  - `subdomain_dangling_takeover` 24 · `broken_access_control_staff_graphql` 71 · `local_privilege_escalation` 29 · `container_kernel_escape` 9 · `_adjacent` 15 · `_adjacent_unclassified` 24 → **172 rows**.
- The build merges the two adjacent pools into one last module (05 Adjacent-Merges, 39 rows: 15 + 24), per the adjacent-pool rule. Every bucket id appears in exactly one module — verified by the post-build count check (148/148, no duplicates; see the verification note below).
- **Per-body read**: all 167 full bodies were read end-to-end before module assignment ("bodies win"). Five GHSL query rows are metadata-only (54-byte one-liners, ~`This bug was reported directly to GitHub Security Lab.`): PRIV-891268/929288/1483919/1587150/1602234.
- The remaining `unclassified` pool (468 − 24 = 444 rows) is **not** in this vault. A future v2 sweep may promote more rows into priv-esc; until then the vault quotes only its 172.

## 3. Bounty accounting

- **Rule**: DB `bounty_amount` where present; `None` recorded as `-` (no figure). Blank ≠ unpaid — HackerOne does not always publish figures.
- Bucket (148): 62 rows carry figures, totaling **$94,075**.
- Merges (24): 10 rows carry figures, totaling **$12,190**.
- **Vault corpus: 72/172 rows carry figures, totaling $106,265**; max $12,000 (PRIV-689314, GitLab template copy). See `case-register.md` for per-row labels and module totals: 01 $1,400/4 · 02 $35,970/23 · 03 $7,050/17 · 04 $10,600/6 · 05 $51,245/22.
- The register pulls `weakness_name / asset_identifier / asset_type / cve_ids / bounty_amount` from the DB per row (not from `classified.json`), so any drift between the classifier export and the DB is visible. Fourteen rows carry CVEs (CVE-2016-4178, CVE-2016-9464, CVE-2019-15621/15624, CVE-2019-0211/6977/19501, CVE-2019-5736, CVE-2020-27194, CVE-2021-25737, CVE-2021-22921/29221/22117, CVE-2023-30586, CVE-2023-29198, CVE-2023-42663, CVE-2023-47037).

## 4. Era discipline

- The DB is a disclosed-report corpus with no per-row disclosure date in this slice; the vault therefore quotes no era statistics beyond the id-epoch mix (early rows in the 50k–200k range through 2023-era rows in the 2–3M range). Tool choices in the bodies (Burp Intruder, curl replays, manual Lua snippets) are historical evidence; the playbook's P4 is the modern hardening fingerprint, labeled as outside the corpus.
- Post-corpus hardening is fingerprints-in-P4, not corpus doctrine. Modern equivalents (safe DLL search mode, `COPY --no-dereference`, per-mutation server-side authz, dangling-record monitoring) are recorded as expectations, not as findings.
- Team names in the register are DB `program_handle` values (`security`, `ibb`, `shopify`, `acronis`, `gitlab`, …). The `security` handle is HackerOne's own platform program (2FA, mediation, GraphQL invitation, SCIM rows); `ibb` is the Internet Bug Bounty program (upstream/vendor rows).

## 5. Limitations

1. **Bucket-vs-merge split is provenance, not severity.** The 24 merges are in the vault because `module_map_all.json` assigns them to `priv-esc`; their `weakness_name` is `None` in the DB. The register keeps a `Source` column (`bucket` / `merge`) so the split stays auditable. Module 05's economics include both pools; no row was dropped for being a merge.
2. **GHSL metadata-only rows carry $5,100 with no technique.** Five rows (PRIV-891268 $1,800, PRIV-1483919 $1,800, PRIV-929288 $1,500, PRIV-1587150/1602234 $0) are 54-byte one-liners. They are anchors for pricing, never quoted as technique.
3. **Weakness tags are not taxonomy.** The same class appears as `Privilege Escalation`, `Improper Authorization`, or `None` (merges). The adjacent classified pool (module 05's 15) is labelled priv-esc but contains RCE, prototype pollution, sandbox bypass, and token theft. Modules classify by body behavior; the register keeps the archive label.
4. **Bounty `None` ≠ unpaid.** 100 of 172 rows carry no figure. $106,265 is a corpus floor, not a total. The two largest figures ($12,000, $10,000) are not close to the corpus's true ceiling — figure-less rows (e.g., PRIV-1249583's full ingress-token walkthrough) may have been paid without a published figure.
5. **No live testing was performed.** Validate against the hunt-idor / hunt-api-misconfig skill scenario matrices, and against module 02's role-matrix sweep where the target offers a staff surface.
