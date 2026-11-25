---
title: "Host Header source index — provenance, funnel, DB reconciliation, limitations"
type: source-index
built: "2026-11-07"
---

# Source index — Host Header build

## 1. Corpus provenance

- **Primary source**: `/home/user/tools/h1-brain/disclosed_reports.db` — the h1-brain pre-built
  SQLite corpus of publicly disclosed, bounty-awarded HackerOne reports (**3,673 rows**,
  table `disclosed_reports` with fields `id, title, vulnerability_information, weakness_name,
  program_handle, asset_identifier, asset_type, cve_ids, bounty_amount`). The DB was fetched
  from the repo's Git-LFS pointer and sha256-verified:
  `8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4`. No live HackerOne fetch
  this build.
- **Classifier outputs**: `/home/user/opencode-work/h1brain/classified.json` (bucket
  `host-header` = 4 rows) and `/home/user/opencode-work/h1brain/module_map_all.json`
  (`host-header.host-header-injection` = 4 ids, `_adjacent` = 0). Bodies re-read from the DB
  for the archive dump; classified `id/title/body/program/bounty` match the DB for all 4 rows.
- **In-vault archive**: `references/archive/host-bodies-full-dump.txt` (4/4 bodies),
  `references/archive/classes.json` (frozen module assignment).

## 2. Classification funnel

1. **Keyword net** over all 3,673 rows: `classified.json` bucket `host-header` selected **4 rows**
   via `host header` / `host-header` keyword arms (`src` = `None/keyword:host-header`). DB
   weakness labels: `Open Redirect` (158019), `None` (229498, 1444675),
   `Server-Side Request Forgery (SSRF)` (1783015) — triage labels, not taxonomy. Bodies are
   the class authority; all 4 classify as host-consumption by body behavior.
2. **Module split** (frozen in `classes.json`): single module `host-header-injection` holds all
   4 ids (158019, 229498, 1444675, 1783015). `_adjacent` = 0 — no adjacent rows.
3. **Per-body read**: all 4 bodies read end-to-end. Evidence: 4 full-body / 0 metadata-only.
4. **DB reconciliation**: every bucket row verified present in `disclosed_reports` with
   identical title and bounty. Programs match the classifier (instacart, starbucks, omise,
   urbancompany).

## 3. Bounty accounting

- **Rule**: DB `bounty_amount` where present; `None` recorded as no figure (not $0). Blank ≠
  unpaid — HackerOne does not always publish figures.
- Corpus: 2/4 rows carry figures, totaling **$800** ($300 + $500); max $500 (HOST-1783015).
  See case-register.md for per-row labels and the arithmetic.
- **What the money prices**: consumed host values — verification-link redirect + content
  spoof ($300) and shared-IP subdomain reach ($500). Bare reflections record no figure.

## 4. Limits & era honesty

1. **Four-row corpus** — one row per pattern; no generalization into a tariff.
2. **Screenshot-dependent PoCs** (`{F…}` markers) — text quotes are the byte-true residue;
   no screenshot content reconstructed.
3. **DB weakness ≠ taxonomy** — Open Redirect / SSRF / None labels; bodies decide the class.
4. **No password-reset row at a paid tier** — reset-mail pricing is outside this bucket.
5. **Era**: 2016–2017 disclosures; P4 hardening is labeled outside-corpus doctrine.
6. **Quote discipline**: every blockquote is byte-true to
   `references/archive/host-bodies-full-dump.txt`; `(sic)` where needed.
7. **No live testing** — test mailboxes/accounts only (playbook P0/P5).
