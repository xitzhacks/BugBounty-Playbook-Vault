---
title: "LLM/AI source index — provenance, funnel, DB reconciliation, limitations"
type: source-index
built: "2026-11-07"
---

# Source index — LLM/AI build

## 1. Corpus provenance

- **Primary source**: `/home/user/tools/h1-brain/disclosed_reports.db` — the h1-brain pre-built
  SQLite corpus of publicly disclosed, bounty-awarded HackerOne reports (**3,673 rows**,
  table `disclosed_reports` with fields `id, title, vulnerability_information, weakness_name,
  program_handle, asset_identifier, asset_type, cve_ids, bounty_amount`). The DB was fetched
  from the repo's Git-LFS pointer and sha256-verified:
  `8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4`. No live HackerOne fetch
  this build.
- **Classifier outputs**: `/home/user/opencode-work/h1brain/classified.json` (bucket
  `llm-ai` = 1 row) and `/home/user/opencode-work/h1brain/module_map_all.json`
  (`llm-ai.prompt-injection` = 1 id, `_adjacent` = 0). Body re-read from the DB for the
  archive dump; classified `id/title/body/program/bounty` match the DB.
- **In-vault archive**: `references/archive/llm-bodies-full-dump.txt` (1/1 body),
  `references/archive/classes.json` (frozen module assignment).

## 2. Classification funnel

1. **Keyword/labeled net** over all 3,673 rows: `classified.json` bucket `llm-ai` selected
   **1 row** by `llm-ai` / `LLM01` arms (`src` = `None/keyword:llm-ai`). DB weakness label:
   `LLM01: Prompt Injection` (2372363) — the only modern-taxonomy label in this vault's
   corpus. Body behavior confirms the label (invisible Unicode-tag injection).
2. **Module split** (frozen in `classes.json`): single module `prompt-injection` holds the
   one id (2372363). `_adjacent` = 0 — no adjacent rows.
3. **Per-body read**: the single body read end-to-end. Evidence: 1 full-body / 0 metadata-only.
4. **DB reconciliation**: the bucket row verified present in `disclosed_reports` with
   identical title and bounty. Program matches the classifier (`security`).

## 3. Bounty accounting

- **Rule**: DB `bounty_amount` where present; `None` recorded as no figure (not $0). Blank ≠
  unpaid — HackerOne does not always publish figures.
- Corpus: 1/1 rows carry figures, totaling **$2,500** (max $2,500, LLM-2372363). See
  case-register.md for per-row labels and the arithmetic.
- **What the money prices**: a disciplined invisible-channel demonstration (tag-hidden
  payload + visible twin + 3× suggestion + decoder + remediation). No row prices beyond
  advisory-suggestion steering.

## 4. Limits & era honesty

1. **Single-row corpus** — one program, one channel, one target (Hai). No ranking doctrine.
2. **Invisible payloads need decode tooling** — archive preserves bytes verbatim; module
   quotes the visible ASCII twin, never the invisible stream as prose.
3. **Redacted suggestion** — Hai's suggestion text is redacted in the DB body; the vault
   does not guess it.
4. **Fake-victim corpus** — report/severity/account are synthetic fixtures; no real report
   is misdescribed.
5. **Era**: single 2020s-era LLM01 row; P4 hardening beyond render-or-drop is labeled
   outside-corpus doctrine.
6. **Quote discipline**: every blockquote is byte-true to
   `references/archive/llm-bodies-full-dump.txt`.
7. **No live testing** — in-scope test reports/accounts only (playbook P0/P5).
