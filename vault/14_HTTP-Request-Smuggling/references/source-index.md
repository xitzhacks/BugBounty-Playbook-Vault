---
title: "SMUG source index — provenance, funnel, classification mechanics, limitations"
type: source-index
built: "2026-11-07"
---

# Source index — HTTP Request Smuggling / CRLF build

## 1. Roster provenance

- **Primary source**: `/home/user/tools/h1-brain/disclosed_reports.db` — the h1-brain pre-built SQLite corpus of publicly disclosed, bounty-awarded HackerOne reports (**3,673 rows**, sha256-verified `8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4`). No live HackerOne fetch this build.
- **Row fields**: `id, title, vulnerability_information, weakness_name, program_handle, asset_identifier, asset_type, cve_ids, bounty_amount`, extracted in full for the 36 bucket rows as the case-register ledger. Full bodies in `vulnerability_information` (roster avg ~2.3 KB); per-row body lengths recorded in the register.
- **Working copies**: `/home/user/opencode-work/h1brain/{classified.json (bucket smuggling-crlf, 36 rows), module_map_all.json (smuggling-crlf module map)}`. In-vault archive: `references/archive/SMUG-bodies-full-dump.txt` (48 bodies = 36 + 12 unclassified merges, verbatim), `references/archive/classes.json` (frozen module assignment), `references/archive/meta.json`.

## 2. Classification funnel

1. **Bucket (classified)**: 36 rows under weakness labels `HTTP Request Smuggling` (23) and `CRLF Injection` (13) → 36-classified smuggling-crlf bucket in classifier v1 (per `classified.json`).
2. **Module split (bodies-win, frozen in `classes.json`)**:
   - **Request-Smuggling-Desync (module 01, 22 rows)**: parser-differential rows (CL.TE/TE.CL/TE.TE, obfuscated TE, llhttp grammar drift, trailer misparse, pause desync, client-side desync). The module_map name `http_request_smuggling_desync` is normalized to the RCE-style file name.
   - **CRLF-Header-Injection (module 02, 9 rows)**: response splitting, Set-Cookie forgery, library header validation gaps (undici/urllib), display-lane `%0d`, stored control-byte filenames.
   - **Email-Protocol-Injection (module 03, 4 rows)**: SMTP/newsletter/ iCalendar CRLF into mail transcripts, LDAP password → SMTP/Redis RESP, Grafana rendering_args config injection → RCE.
   - **Adjacent-and-Negative-Space (module 04, 13 rows)**: 1 bucket `_adjacent` (SMUG-246803 cart-quantity business logic, $250) + 12 `_adjacent_unclassified` merges drawn from the 468-row `unclassified` pool (of which the 2 Apache rows are genuinely smuggling/CRLF by body: SMUG-1391549 $1,200 and SMUG-1594627 $2,400).
3. **Per-body read**: all 48 bodies read end-to-end before module assignment ("bodies win"). 48/48 full bodies — three rows are ≈54–141 chars of which two are PDF-only pointers (SMUG-735748) and the CVE-2022-3221x trio one-liners; nothing is title-only. Weakness labels from triage were used as pointers only (the cart-quantity row carries the label `HTTP Request Smuggling`).
4. The remaining `unclassified` pool (468 rows per classifier v1; 506 rows in `unlabeled_rows.json` — classifier snapshot drift) is **not** in this vault beyond the 12 merges. A v2 keyword sweep may promote more rows later; until then the vault quotes only its 48.

## 3. Bounty accounting

- **Rule**: DB `bounty_amount` where present; `None` recorded as `-` (no figure). Blank ≠ unpaid — HackerOne does not always publish figures.
- Corpus: 19/36 bucket rows carry figures, totaling **$34,290** — module 01 $27,740/14 · module 02 $1,300/3 · module 03 $5,000/1 · bucket-adjacent $250/1. Max $5,000 (SMUG-1200647), next $4,660 ×3 (Tomcat trio).
- Including the 12 unclassified merges: **$41,190/23** (+$6,900/4), with the merges' 5-figure-free ceiling at $2,400 (SMUG-1594627).
- See `case-register.md` for the per-row ledger (DB weakness/asset/CVE/bounty) and the arithmetic that ties both totals together.

## 4. Era discipline

- Rows span the 2014–2024 disclosure era (id-order proxy: from SMUG-39181, 2014, to SMUG-2327341, 2024) without dates in the DB; era is never assumed from corpus folklore. The IIS/Apache/Sendmail-era validation samples (SMUG-409512, 2016) sit beside 2023-2024 llhttp/Tomcat parser CVEs.
- Smuggler/Turbo Intruder tooling evidence (smuggler `space1`, `tabprefix1`, "150+ types", Turbo Intruder victim-race scripts) is historical record; modern equivalents are fingerprints-in-P4, not corpus doctrine.
- The vendor-advisory rows (Apache advisories for SMUG-1594627, Tomcat security pages inside SMUG-2299692/2327341) are recorded as bodies read, not separately fetched.

## 5. Limitations

1. **Weakness labels ≠ taxonomy**: the same class is labeled `HTTP Request Smuggling` on a business-logic cart row, `CRLF Injection` on SMTP/Redis/RCE rows, and `HTTP Request Smuggling` on the Apache pairs; the classifier granularity stops at the bucket. Modules classify by body behavior.
2. **Attachment-only rows**: SMUG-735748 (CVE-2019-15605) ships a "PDF writeup" — no quotable payload text; the CVE-2022-3221x trio bodies are one-liners pointing at Original Reports. Nothing was invented for them.
3. **GHSL one-liners carry bounty weight without technique**: SMUG-761222/1401159 ($1,500/$1,800) are priced corpus facts with 54-char bodies — anchors, not evidence; five of the twelve merges are CodeQL detector tickets (see module 04 §3).
4. **Bounty `None` ≠ unpaid.** 17 of 36 bucket rows carry no figure; $34,290 is a corpus-floor, not a total. The two scariest impact proofs (slackb.com, Zomato) sit on the `-` rows.
5. **Quote discipline**: every blockquote across the four modules plus the playbook and README scoreboard anchors is byte-true to `references/archive/SMUG-bodies-full-dump.txt`; `(sic)` marks author typos. No invented quotes, no paraphrase passing as quotation.
6. **Chain inclusion is one-directional**: the Grafana row is counted as CRLF here and re-cited as RCE in `RCE/` — master-list row 14 remains the canonical home; nothing here double-counts bounty in this vault's totals.
