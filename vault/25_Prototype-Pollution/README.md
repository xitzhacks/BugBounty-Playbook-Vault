---
title: "Vault/25 — Prototype Pollution playbook set"
type: index
category: prototype-pollution
built: "2026-11-07"
evidence: "4 classified rows → 4 retrievable bodies read (4 full-body / 0 metadata-only) · 0 adjacent rows"
bounty: "$6,000 across 2 rows with DB figures (max $3,000, PP-1106238 ×2) · 2 rows carry no DB figure"
companion_vaults: "../XSS · ../RCE · ../Authentication-Session"
case_id_scheme: "PP-<HackerOne report id>"
quote_rule: "byte-true, (sic)-marked, from read bodies only; missing figures recorded never invented"
---

# Vault/25 — Prototype Pollution playbook set

Four rows, and the class's pricing line runs through the middle of them: every row *pollutes*
`Object.prototype` — lodash server-side (CVE-2020-8203), a client-side `deparam` hash parser,
and two sibling Mermaid directive rows on GitLab — but only the rows that *weaponize* the
pollution into stored XSS with a named gadget pay ($3,000 × 2, same program, sequential
reports). Pollution alone is a DoS sentence; pollution plus a gadget is a stored-XSS finding.

## Start here

| # | File | What it gives you |
|---|---|---|
| 1 | [`PP-Testing-Agent-Playbook.md`](PP-Testing-Agent-Playbook.md) | **The executable protocol.** P0 program/policy read → P1 merge/parse-site inventory → P2 probe protocol (canary → gadget search → XSS/DoS/RCE ladder) → P3 proof ladder → P4 hardening fingerprints → P5 kill-gates. |
| 2 | [`00_prototype-pollution.md`](00_prototype-pollution.md) | All 4 rows: lodash library (CVE-2020-8203), Swiftype `deparam` + eval gadget, Mermaid DoS then Mermaid stored-XSS (the paid pair). |

## References (provenance layer)

| File | Contents |
|---|---|
| [`references/source-index.md`](references/source-index.md) | Corpus provenance (h1-brain DB `disclosed_reports`, sha256 `8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4`, 3,673 rows), classification funnel (`classified.json` bucket `prototype-pollution` → 4, `module_map_all.json` `prototype-pollution` → 4, `_adjacent` → 0), DB reconciliation, bounty accounting, era discipline, 7 limitations. |
| [`references/case-register.md`](references/case-register.md) | Row-per-row ledger of all 4 bucket rows: case ID, team, bounty, module, evidence level, DB weakness + CVE. |
| [`references/archive/pp-bodies-full-dump.txt`](references/archive/pp-bodies-full-dump.txt) | All 4 bodies verbatim — the anchor for every quote. |
| [`references/archive/classes.json`](references/archive/classes.json) | Frozen module assignment for all 4 rows. |

## Scoreboard (4 rows · 2 with bounty figures · $6,000 · max $3,000)

| Case | Title (short) | Program | Bounty | CVE |
|---|---|---|---|---|
| [PP-712065](https://hackerone.com/reports/712065) | Prototype pollution attack (lodash) | nodejs-ecosystem (lodash) | — | CVE-2020-8203 |
| [PP-998398](https://hackerone.com/reports/998398) | Prototype Pollution → XSS (Swiftype `deparam`) | elastic (*.swiftype.com) | — | — |
| [PP-1106238](https://hackerone.com/reports/1106238) | Stored XSS via Mermaid Prototype Pollution (DoS step) | gitlab | **$3,000** | — |
| [PP-1280002](https://hackerone.com/reports/1280002) | Stored XSS via Mermaid Prototype Pollution (XSS step) | gitlab | **$3,000** | — |

Corpus program mix: gitlab 2 · nodejs-ecosystem 1 · elastic 1. All four bodies are
full-body; no row is metadata-only.

## Vault map

| File | Content |
|---|---|
| `PP-Testing-Agent-Playbook.md` | Agent-facing operational playbook: P0–P5 phases, module↔phase table, non-goals. |
| `00_prototype-pollution.md` | Single module covering all 4 rows with case-stock table, byte-true quotes, what-pays/what-doesn't, cross-references. |
| `references/source-index.md` | Provenance, funnel, DB reconciliation, bounty accounting, era discipline, limitations. |
| `references/case-register.md` | 4-row ledger with DB metadata, evidence level, weakness labels + CVE. |
| `references/archive/pp-bodies-full-dump.txt` | All 4 bodies verbatim (anchor for every quote). |
| `references/archive/classes.json` | Frozen module assignment for all 4 rows. |

## Cross-vault links

- `XSS/` — three of the four rows *terminate* in XSS (DOM via gadget, stored via Mermaid);
  that vault owns the XSS payoff doctrine, this vault owns the pollution primitive.
- `RCE/` — lodash pollution is the server-side RCE-precursor (`merge`/`defaultsDeep`);
  PP-712065's impact sentence claims RCE "in some cases." The RCE vault owns execution
  doctrine; this vault owns the `__proto__` sink evidence.
- `Authentication-Session/` — no corpus row chains pollution into auth, but the PP-1280002
  `template` gadget is an object-property consumer of the same shape as token/option
  confusion; cite the auth vault for the hardening posture.

## Coverage vs limitations

**Covered**: the complete `prototype-pollution` classified bucket (4 rows) with per-row sink,
gadget, and bounty; the `prototype-pollution` module assignment (`module_map_all.json`);
DB reconciliation for every row.

**Honest limitations**:
1. **Two-program corpus.** All paid rows are one program (GitLab) on one library (Mermaid) —
   a single researcher's two-step investigation. The "pollution + gadget pays" rule rests on
   one paid pair plus two unpaid rows and is labeled as such.
2. **Half the corpus carries no figure.** PP-712065 (lodash, CVE-2020-8203) and PP-998398
   (Swiftype) are `None` in the DB. $6,000 is a corpus floor; blank is not $0.
3. **Weakness labels are triage artifacts.** The lodash row is labeled `Allocation of
   Resources Without Limits or Throttling`; the other three are all labeled XSS (DOM /
   Stored ×2). Bodies are the class authority.
4. **Sibling-row double count is program truth.** PP-1106238 (DoS characterization) and
   PP-1280002 (XSS weaponization) are separate disclosures on one sink, each paid $3,000.
   The vault keeps both rows; analysts summing "per-sink" value should not double-count the
   research effort.
5. **Screenshot/video-dependent PoCs.** PP-1106238/1280002 PoCs lean on `{F…}` markers;
   the text payloads (`%%{init:…}%%` directives, `# __proto__` hash) are byte-true here.
6. **Era honesty.** Rows span the lodash-4.17.15 era through the Mermaid-8.6.0 era; modern
   `Object.create(null)` / `__proto__`-key-hardening is fingerprinted in playbook P4 and
   labeled outside the corpus.
7. **No live testing was performed.** Validate pollution probes against in-scope test
   accounts/projects you control — never against production issues or traffic.


<!-- CASESTOCK-LINK:BEGIN -->

## Case stock — vault (`_VAULT/`)

**52 disclosed reports** routed to this category · 2 with a bounty figure · **$6,000** · 51 full write-ups stored locally.

- Full list: [`_VAULT/by-vault-category/25_Prototype-Pollution.md`](../_VAULT/by-vault-category/25_Prototype-Pollution.md)
- Query: `sqlite3 ../_VAULT/reports.sqlite "SELECT id,bounty,title FROM reports WHERE ..."`
- Pull one write-up: `python3 ../_VAULT/scripts/extract_report.py <id>`

| Top paid | Program | Bounty |
|---|---|---|
| [1106238](https://hackerone.com/reports/1106238) Stored XSS via Mermaid Prototype Pollution vulnerability | GitLab | $3,000 |
| [1280002](https://hackerone.com/reports/1280002) Stored XSS via Mermaid Prototype Pollution vulnerability | GitLab | $3,000 |

_refreshed 2026-11-17 from the public HackerOne disclosed-report dataset_
<!-- CASESTOCK-LINK:END -->
