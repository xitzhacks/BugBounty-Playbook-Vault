---
title: "Race source index — provenance, funnel, classification mechanics, limitations"
type: source-index
built: "2026-11-07"
---

# Source index — Race Conditions build

## 1. Corpus provenance

- **Primary source**: `/home/user/tools/h1-brain/disclosed_reports.db` — the h1-brain pre-built SQLite corpus of publicly disclosed, bounty-awarded HackerOne reports (3,673 rows). The repo stores the DB as a Git-LFS pointer; the real file was fetched from `media.githubusercontent.com` and sha256-verified: `8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4`. No live HackerOne fetch this build.
- **Row fields**: `id, title, vulnerability_information, weakness_name, program_handle, asset_identifier, asset_type, cve_ids, bounty_amount`. Full report bodies in `vulnerability_information` (roster avg ~2.3 KB).
- **Working copies**: `/home/user/opencode-work/h1brain/{classified.json, race_bodies.txt}` (classifier output + 26-row digest). In-vault archive: `references/archive/race-bodies-full-dump.txt` (26/26 bodies), `references/archive/classes.json` (frozen module assignment), `references/archive/meta.json`.

## 2. Classification funnel

1. **Keyword/labeled net** over all 3,673 rows: CWE-style weakness labels (`Time-of-check Time-of-use (TOCTOU) Race Condition`, `Concurrent Execution using Shared Resource with Improper Synchronization ('Race Condition')`) plus keyword arms in title/body (`race conditio…`, `toctou`, `double-spend`, `timing attack`) → **26 rows**.
2. **Per-body read**: all 26 bodies read end-to-end before module assignment ("bodies win"). 23 full-body, 3 metadata-only (GitHub-Security-Lab one-liners, ~60 bytes each).
3. **Module split** (frozen in `classes.json`): Financial-Credit-and-Ledger 7 · Membership-and-Invitation 4 · Account-ATO-and-Token 3 · Check-Use-and-File-System 7 · Library-Timing-Adjacent 5.
4. The remaining `unclassified` pool (468 rows per classifier v1; 506 rows in `unlabeled_rows.json` — classifier snapshot drift) is **not** in this vault. A v2 keyword sweep may promote more rows into race later; until then the vault quotes only its 26.

## 3. Bounty accounting

- **Rule**: DB `bounty_amount` where present; `None` recorded as `-` (no figure). Blank ≠ unpaid — HackerOne does not always publish figures.
- Corpus: 10/26 rows carry figures, totaling **$43,260**; max $15,250 (RACE-300305). See case-register.md for per-row labels and module totals.

## 4. Limits & era honesty

1. **Season**: rows span 2016–2024 era disclosures. Tooling evidence (curl `&`, Burp Intruder, Race The Web) is historical record; Turbo Intruder gate scripts are the current-standard exemplar.
2. **Chainpay vs racepay**: the two biggest rows ($15,250, $12,000) pay because the race feeds another class (ATO, traversal). Pure-race ceiling in this corpus: $5,000.
3. **Metadata-only rows** (RACE-1301753, RACE-1496268, RACE-1943049) carry $7,300 with no readable body — anchors, not evidence.
4. **Weakness labels ≠ taxonomy**: same class appears as TOCTOU / CWE-362 / SSRF / Code Injection / XSS / Improper Auth / Improper Access Control / None. Modules classify by body behavior.
5. **Quote discipline**: every blockquote across the six class modules is byte-true to `references/archive/race-bodies-full-dump.txt`; `(sic)` marks author typos. No invented quotes, no paraphrase passing as quotation.
