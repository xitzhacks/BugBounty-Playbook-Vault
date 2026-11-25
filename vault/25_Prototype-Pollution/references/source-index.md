---
title: "Prototype Pollution source index — provenance, funnel, DB reconciliation, limitations"
type: source-index
built: "2026-11-07"
---

# Source index — Prototype Pollution build

## 1. Corpus provenance

- **Primary source**: `/home/user/tools/h1-brain/disclosed_reports.db` — the h1-brain pre-built
  SQLite corpus of publicly disclosed, bounty-awarded HackerOne reports (**3,673 rows**,
  table `disclosed_reports` with fields `id, title, vulnerability_information, weakness_name,
  program_handle, asset_identifier, asset_type, cve_ids, bounty_amount`). The DB was fetched
  from the repo's Git-LFS pointer and sha256-verified:
  `8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4`. No live HackerOne fetch
  this build.
- **Classifier outputs**: `/home/user/opencode-work/h1brain/classified.json` (bucket
  `prototype-pollution` = 4 rows) and `/home/user/opencode-work/h1brain/module_map_all.json`
  (`prototype-pollution.prototype-pollution` = 4 ids, `_adjacent` = 0). Bodies re-read from
  the DB for the archive dump; classified `id/title/body/program/bounty` match the DB for all
  4 rows.
- **In-vault archive**: `references/archive/pp-bodies-full-dump.txt` (4/4 bodies),
  `references/archive/classes.json` (frozen module assignment).

## 2. Classification funnel

1. **Keyword net** over all 3,673 rows: `classified.json` bucket `prototype-pollution` selected
   **4 rows** via `prototype pollution` / `__proto__` keyword arms
   (`src` = `None/keyword:prototype-pollution`). DB weakness labels: `Allocation of Resources
   Without Limits or Throttling` (712065, lodash), `Cross-site Scripting (XSS) - DOM` (998398),
   `Cross-site Scripting (XSS) - Stored` (1106238, 1280002). Bodies are the class authority;
   the module classifies by `__proto__` sink behavior.
2. **Module split** (frozen in `classes.json`): single module `prototype-pollution` holds all
   4 ids (712065, 998398, 1106238, 1280002). `_adjacent` = 0 — no adjacent rows.
3. **Per-body read**: all 4 bodies read end-to-end. Evidence: 4 full-body / 0 metadata-only.
4. **DB reconciliation**: every bucket row verified present in `disclosed_reports` with
   identical title and bounty. Programs match the classifier (nodejs-ecosystem, elastic,
   gitlab ×2). One CVE in the DB: PP-712065 → `["CVE-2020-8203"]`.

## 3. Bounty accounting

- **Rule**: DB `bounty_amount` where present; `None` recorded as no figure (not $0). Blank ≠
  unpaid — HackerOne does not always publish figures.
- Corpus: 2/4 rows carry figures, totaling **$6,000** ($3,000 + $3,000); max $3,000
  (PP-1106238, PP-1280002 — same program, same sink, sequential disclosures). See
  case-register.md for per-row labels and the arithmetic.
- **What the money prices**: pollution *plus* a named downstream consumer — app-wide DoS
  ($3,000) and stored XSS via the `template` gadget ($3,000). Library-level pollution and
  the gadget-proposal row record no figure.

## 4. Limits & era honesty

1. **Two-program corpus** — paid rows are one program (GitLab) on one library (Mermaid).
2. **Half the corpus at `None`** — $6,000 is a corpus floor; blank is not $0.
3. **DB weakness ≠ taxonomy** — Allocation/XSS labels; bodies decide the class.
4. **Sibling double count is program truth** — 1106238 → 1280002 is one investigation paid
   twice; keep both rows, do not double-count research effort in per-sink sums.
5. **Era**: lodash-4.17.15 through Mermaid-8.6.0; P4 hardening is outside-corpus doctrine.
6. **Quote discipline**: every blockquote is byte-true to
   `references/archive/pp-bodies-full-dump.txt`; `(sic)` where needed.
7. **No live testing** — in-scope test projects/issues only (playbook P0/P5).
