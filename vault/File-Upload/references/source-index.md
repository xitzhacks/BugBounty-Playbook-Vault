---
title: "File Upload source index — provenance, funnel, fetch mechanics, limitations"
type: source-index
built: "2026-11-05"
---

# Source index — File Upload build

## 1. Roster provenance

- **Primary roster**: full HTML of `h1.security.nathan.sx` — 4,419 public HackerOne report
  rows, snapshot frozen **2017-09-12**. This build reuses the byte-verified mirror copy
  archived in the `../RCE` vault (`references/archive/mirror-all-rows.json`, 1,105,968 bytes,
  re-fetched live 2026-11-04 and byte-parse identical to the XXE/CSRF/Open-Redirect/
  Authentication-Session builds); the artifact is re-archived here under
  `references/archive/mirror-all-rows.json`. Same mirror for all six vaults.
- **Title filter** — 7 case-insensitive arms applied to mirror titles (single-pass funnel,
  **no supplemental pass** — the one-pass reading of `bodies.txt` recast every candidate
  into exactly one of the nine modules, so the RCE-style rescue passes were unnecessary):

  | Arm | Pattern |
  |---|---|
  | upload | `\bupload` |
  | traversal | `traver(path)?\|directory traversal\|path traversal` (reducer: `traver`) |
  | lfi | `\bl\.?f\.?i\b\|local file inclus` |
  | rfi | `\br\.?f\.?i\b\|remote file inclus` |
  | file-read | `\bfiles?\s?(read\|stealing\|download)(ing)?\b\|\bdownload\s+arbitrary\b\|arbitrary file` |
  | incl | `file inclusion\|include\(?\s*\$\|require\(?\s*\$` |
  | malfile | `malicious file` |

  Union: **86 unique rows** (`archive/candidates.json`, arms recorded per row). Arm sizes
  before union: upload 52 · traversal 8 · file-read family 22 · inclusion family 20 ·
  malfile 5 (overlaps small; full matrix in build workspace scripts).

## 2. Fetch funnel

- **86 candidates → 65 × HTTP 200 + 21 × HTTP 404 · zero transient failures** — every
  report fetched live at `https://hackerone.com/reports/<id>.json` with 1.4 s spacing
  (2026-11-05, `fetch.log` + `http-codes.txt` in archive).
- Bodies: 65/65 fetched rows carry readable text — 47 through `vulnerability_information`,
  18 through the disclosed `summaries` content field (`body_src=summaries`).
  Zero metadata-only body rows — the first vault in the series with none.
- **Known-dead confirmations**: the funnel pre-confirmed three rows already recorded 404 in
  the RCE vault (4836, 6674, 142562) and two already recorded in the XXE vault (105787 live,
  232614 live, 142562 dead) — all re-fetched fresh this build per the fetch-everything rule.
- Control fetch for transient detection: a nonexistent report id returns 400 (not a
  network failure), matching the RCE build's control result.

## 3. Payload accounting (verification chain)

| Step | Count | Amount |
|---|---|---|
| JSON bounty_amount present | 8 live rows | $3,426 |
| Mirror figure, json empty | 26 live rows | $41,815 |
| Class modules 01–09 | 65 live rows | **$45,241** (34 paid rows) |
| Dead-404 mirror figures | 21 dead rows, 12 with figures | $26,628 |
| All-envelope | 86 rows | **$71,869** |
| Dead rows sharing the RCE dead-list | 3 rows (4836 $800 · 6674 $3,000 · 142562 $10,000) | $13,800 → net-of-RCE dead $12,828/9 |

Reconciliation file: `archive/bounty-reconciliation.json` (script-verified to the cent).

Label conflicts: none. For all 8 json-bounty rows the mirror display figure equals the json
amount (checked mechanically — no SRC-MISMATCH rows; contrast: the CSRF build carried a
$50/json label drift row, that vault excluded it, `CSRF-158016` lives here as real class 02).

## 4. BugBountyHunter (bugbountyhunter.com) — taxonomy check, re-verified 2026-11-05

The `/vulnerability/` type index (retains `command_injection`; 2026-10-28-era `code` and
`token` pages remain gone) has **never had a file-upload / traversal / LFI type page** —
the class's closest entries are the guide tags `fileuploads`, `javascript_files`
(fetched: `guides/?type=fileuploads`, 34,647 bytes, live this build — §1a of blogs-index
byte-quotes its prose). The four-lane ledger for this build therefore lives on the
`/disclosed/` statistical view. Weakness-bucket `getinfo?weakness=<id>` endpoints fetched
live 2026-11-05 (`bbh-getinfo-*.html` ×6 in archive); histogram sums:

| BBH weakness bucket (id) | Reports listed today | Top programs |
|---|---|---|
| Unrestricted Upload of File with Dangerous Type (6066) | 14 | Visma 2 · Slack 2 · Deptofdefense 2 |
| Path Traversal (3455) | 236 | Nodejs-ecosystem 63 · Deptofdefense 46 · Curl 12 |
| PHP Local File Inclusion (11104) | 1 | Deptofdefense 1 (Local File Read, no bounty paid) |
| Remote File Inclusion (3230) | 19 | Nodejs-ecosystem 3 · Mailru 2 · Security 2 |
| *(adjacent, fetched for boundary)* File and Directory Information Exposure (6297) | 9 | Deptofdefense 2 · Solana-bbp 1 |
| *(adjacent)* External Control of File Name or Path (9149) | 5 | Curl 4 · Singlestore 1 |

Master-list row 10 was frozen at `236 + 14 + 19 + 12` (2026-10-28 snapshot): today 236
(Path Traversal), 14 (Unrestricted Upload), 19 (RFI) match exactly; the `12` figure maps
to no single current bucket (nearest adjacent sums 6297=9, 9149=5 — recorded, not forced).
**BugBountyHunter's live taxonomy prices the class's modern volume exactly where this
vault's corpus does: the traversal bucket is an order of magnitude above the others.**

## 5. Limitations & honesty notes

- The mirror era (2013–2017) predates modern upload hardening (signed uploads, blob
  validation, egress filtering); the modern-side counterpart lives in blogs-index §3 only,
  never inside class counts (vault statute).
- 5 fetched rows carry no H1 weakness code (the era's NULL column style); for live rows the
  weakness census above comes straight from the fetched JSON.
- FU-258117's page state: the RCE build (2026-11-04) read this row metadata-only; this
  build's re-read delivers a `summaries`-sourced body and severs none of the figures
  ($5,000 list in both). Recorded, not reconciled away.
- The mirror's bounty display for dead rows is the list value the mirror froze on
  2017-09-12; where another vault already carries the same dead row (three cases), this
  vault tabulates the amount into its dead list AND keeps the cross note — no silent
  dedup, no double claim (both sums shown in §3).
- Bodied-fetch quote rule: only the 65 live rows are quotable; the 21 dead rows appear in
  this vault only as recorded ledger/bookkeeping artifacts.
