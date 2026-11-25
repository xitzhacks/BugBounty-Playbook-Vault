---
title: "Vault/27 — LLM / AI playbook set"
type: index
category: llm-ai
built: "2026-11-07"
evidence: "1 classified row → 1 retrievable body read (1 full-body / 0 metadata-only) · 0 adjacent rows"
bounty: "$2,500 across 1 row with a DB figure (LLM-2372363) · 0 rows carry no figure"
companion_vaults: "../XSS · ../Authentication-Session"
case_id_scheme: "LLM-<HackerOne report id>"
quote_rule: "byte-true, (sic)-marked, from read bodies only; invisible payloads described, never concealed"
---

# Vault/27 — LLM / AI playbook set

One row, one program, $2,500 — the whole vault is a single demonstration that an invisible
prompt-injection payload (Unicode tag characters that render as blank but reach the model)
can steer Hai's severity suggestion. The corpus prices the *demonstration discipline*
(3× repetition + decode tool + remediation), not a capability ranking. This README says
nothing the module does not prove; the module teaches the only trick the corpus holds.

## Start here

| # | File | What it gives you |
|---|---|---|
| 1 | [`LLM-Testing-Agent-Playbook.md`](LLM-Testing-Agent-Playbook.md) | **The executable protocol.** P0 program/policy read → P1 invisible-channel inventory → P2 probe protocol (tag-hidden → visible-fake → Hai-suggestion triple) → P3 proof ladder → P4 hardening fingerprints → P5 kill-gates. |
| 2 | [`00_prompt-injection.md`](00_prompt-injection.md) | The single row: Unicode-tag invisible injection against Hai ($2,500), with the repetition proof and the render-or-drop remediation. |

## References (provenance layer)

| File | Contents |
|---|---|
| [`references/source-index.md`](references/source-index.md) | Corpus provenance (h1-brain DB `disclosed_reports`, sha256 `8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4`, 3,673 rows), classification funnel (`classified.json` bucket `llm-ai` → 1, `module_map_all.json` `prompt-injection` → 1, `_adjacent` → 0), DB reconciliation, bounty accounting, era discipline, 7 limitations. |
| [`references/case-register.md`](references/case-register.md) | Row-per-row ledger of the single bucket row: case ID, team, bounty, module, evidence level, DB weakness. |
| [`references/archive/llm-bodies-full-dump.txt`](references/archive/llm-bodies-full-dump.txt) | The single body verbatim — the anchor for every quote. |
| [`references/archive/classes.json`](references/archive/classes.json) | Frozen module assignment for the single row. |

## Scoreboard (1 row · 1 with a bounty figure · $2,500 · max $2,500)

| Case | Title (short) | Program | Bounty | CVE |
|---|---|---|---|---|
| [LLM-2372363](https://hackerone.com/reports/2372363) | LLM01: Invisible Prompt Injection | security (hackerone.com) | **$2,500** (max) | — |

Corpus program mix: security 1. The single body is full-body; no row is metadata-only.

## Vault map

| File | Content |
|---|---|
| `LLM-Testing-Agent-Playbook.md` | Agent-facing operational playbook: P0–P5 phases, module↔phase table, non-goals. |
| `00_prompt-injection.md` | Single module covering the one row with case-stock table, byte-true quotes, what-pays/what-doesn't, cross-references. |
| `references/source-index.md` | Provenance, funnel, DB reconciliation, bounty accounting, era discipline, limitations. |
| `references/case-register.md` | 1-row ledger with DB metadata, evidence level, weakness label. |
| `references/archive/llm-bodies-full-dump.txt` | The single body verbatim (anchor for every quote). |
| `references/archive/classes.json` | Frozen module assignment for the single row. |

## Cross-vault links

- `XSS/` — the injected fake report claims an XSS ("there is an xss on the home page") that
  does not exist; that vault owns the XSS payoff doctrine for the *visible* payload.
- `Authentication-Session/` — no corpus row reaches auth, but severity-suggestion steering
  ("suggesting higher severity") is a triage-bias posture; the auth vault owns the defensive
  review.

## Coverage vs limitations

**Covered**: the complete `llm-ai` classified bucket (1 row) with per-row invisible-channel
sink and bounty; the `prompt-injection` module assignment (`module_map_all.json`); DB
reconciliation for the row.

**Honest limitations**:
1. **Single-row corpus.** One program (security / hackerone.com), one channel (Unicode tag
   characters), one target (Hai). Nothing here ranks LLM vulnerabilities; the vault teaches
   the demonstrated trick and its proof discipline only.
2. **Invisible payloads need decode tooling.** The tag-character payload renders as blank;
   this vault's archive preserves the bytes verbatim, and the module quotes the *visible*
   ASCII twin (the "Additional details" payload) rather than the invisible stream. No
   invisible byte is silently reconstructed or paraphrased.
3. **Redacted suggestion.** The Hai severity suggestion in the body is redacted
   (`████████` markers). The vault does not guess its text; the repetition sentence
   ("We used the prompt injection payload 3 times") carries the proof.
4. **Fake-victim corpus.** The report, severity, and account (`rezo`) in the injected text
   are the reporter's synthetic fixtures. No real report is misdescribed in this vault.
5. **Era honesty.** A single 2020s-era LLM01 row. Modern prompt-injection defenses beyond
   the body's remediation (render-or-drop tag characters) are fingerprinted in playbook P4
   and labeled outside the corpus.
6. **No injection at scale.** The corpus demonstrates one advisory-suggestion steer, not
   arbitrary tool-use or data-exfiltration injection. Do not cite this vault for
   beyond-suggestion impact.
7. **No live testing was performed.** Validate prompt-injection probes against in-scope test
   reports/accounts you control — never against production triage flows.


<!-- CASESTOCK-LINK:BEGIN -->

## Case stock — vault (`_VAULT/`)

**6 disclosed reports** routed to this category · 1 with a bounty figure · **$1,600** · 6 full write-ups stored locally.

- Full list: [`_VAULT/by-vault-category/27_LLM-AI.md`](../_VAULT/by-vault-category/27_LLM-AI.md)
- Query: `sqlite3 ../_VAULT/reports.sqlite "SELECT id,bounty,title FROM reports WHERE ..."`
- Pull one write-up: `python3 ../_VAULT/scripts/extract_report.py <id>`

| Top paid | Program | Bounty |
|---|---|---|
| [2509022](https://hackerone.com/reports/2509022) Reflected XSS in AI Chat Bot Greetings at help.shopify.com via Markdown Image Re | Shopify | $1,600 |

_refreshed 2026-11-17 from the public HackerOne disclosed-report dataset_
<!-- CASESTOCK-LINK:END -->
