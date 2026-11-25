---
title: "Vault/File-Upload — file upload, path traversal & file-inclusion playbook set"
type: index
category: "File Upload (all four lanes in one vault: unrestricted/authless upload→exec, upload-URL fetch→SSRF/file-read, upload→stored XSS/content-exec, file inclusion LFI-RFI + XXE-in-upload, plus the traversal read/write/delete lane, RFD & browser download abuse, server-side file download, upload-ACL, adjacent noise shelf)"
built: "2026-11-05"
evidence: "86 roster rows from h1.security.nathan.sx mirror → 65 retrievable bodies read (58 resolved / 7 informative) · 21 × 404 recorded · zero metadata-only rows (18 of 65 bodies via the disclosed `summaries` field)"
bounty: "$71,869 all-envelope grand total (JSON-verified $3,426/8 rows · list-stated $41,815/26 fetched rows · class modules 01–09 $45,241/34 paid of 65 · dead-404 list $26,628/12 rows, of which $13,800/3 rows also sit on the RCE vault's dead-list) · full reconciliation in references/case-register.md"
companion_vaults: "../RCE · ../XXE · ../CSRF · ../Open-Redirect · ../Authentication-Session"
case_id_scheme: "FU-<HackerOne report id>"
quote_rule: "byte-true, (sic)-marked, from read bodies only; 404 rows recorded never quoted"
---

# Vault/File-Upload — the upload · traversal · inclusion playbook set

One vault, four lanes, per the build order (master-list row 10): the class's money in this
corpus is **what the uploaded/fetched object reaches** — a device upload CGI paid $18,000;
a frame-boundary callback gadget beside `upload.php` paid $1,500; a parameterized image
processor reading `../` paid $5,000; and the inclusion rows paid almost nothing because
their landing state was usually just a file. The honest center of the class: the *transfer*
is nearly always sound; the money hides in what happens after.

## Start here

| # | File | What it gives you |
|---|---|---|
| 1 | [`FU-Testing-Agent-Playbook.md`](FU-Testing-Agent-Playbook.md) | **The executable protocol.** P0 program/policy read → P1 surface inventory (upload endpoints, storage paths, processors, serving CDNs, restore/import paths) → P2 probe protocol (.txt ladder → content-type swap → filename smuggle → URL-fetch flip → traversal encoding) → P3 proof ladder → P4 modern hardening fingerprints → P5 kill-gates. |
| 2 | [`01_Unrestricted-Upload-Exec.md`](01_Unrestricted-Upload-Exec.md) | When the sink falls through: executed uploads and authless device CGIs. Anchors: FU-73480 (airMAX $18,000 list — class crown), FU-84374 (ownCloud `.php5` RCE), FU-135072 (ImageTragick MVG, $2,500 list), FU-201529 (AirFibre honest limitation, $150). |
| 3 | [`02_Upload-URL-SSRF-File-Read.md`](02_Upload-URL-SSRF-File-Read.md) | The **all-paid module** ($2,064/6): upload-from-URL as SSRF chassis. Anchors: FU-713 (the corpus opener, $500), FU-115857 (vidgif `concat:` + `file:///etc/passwd`, $800), FU-158016 ($50 json SSRF-noise cross-registered as CSRF-158016). |
| 4 | [`03_Upload-Stored-XSS-Content-Exec.md`](03_Upload-Stored-XSS-Content-Exec.md) | Serving-side battles: extension/content-type/filename/filename-error sinks. Anchors: FU-142135 (vk.com callback eval chain, $1,500 json), FU-97672 (mopub html-as-jpg, $1,120), FU-203515 (WP 4.7.2 filename in error l10n, $350). |
| 5 | [`04_File-Inclusion-LFI-RFI.md`](04_File-Inclusion-LFI-RFI.md) | include() and its cousins: dispatcher override (FU-59665), fix-review bypass (FU-147570), include→RCE (FU-39428 $500 json), parser-directive LFI (FU-179034), XXE-in-upload (FU-232614/105787 XXE cross-ledgers), and the corpus's RFI false-positive exhibit (FU-14092). |
| 6 | [`05_Path-Traversal.md`](05_Path-Traversal.md) | Read/write/delete ladder. Anchors: FU-122475 (Imgur `$5,000` read), FU-3370 (Rails CVE-2014-0130 + `%5c` bypass, $1,500), FU-183568 (BuddyPress arbitrary delete, $350), FU-254200 (S3 bucket escape, $50), FU-213558 (tar symlink restore, $512 json). |
| 7 | [`06_RFD-Browser-Download-Abuse.md`](06_RFD-Browser-Download-Abuse.md) | `.bat`/`.cmd` RFD ladder + the Flash upload CVE. Anchors: FU-51265 (CVE-2015-0337, $2,000 list, team literally "Flash"), FU-107960 (ubnt restapi $150), FU-39658/50658 (HackerOne's own RFD rows), FU-158505 (Sopas). |
| 8 | [`07_Server-Side-File-Download.md`](07_Server-Side-File-Download.md) | The DoD-heaviest module: downloadfile/downloaddoc.aspx shapes + wp-includes source download. Anchors: FU-194351 (Yelp, module's only priced row $100), FU-186326 + FU-230714/230870 (psychomantis pair), four credited summary voices. |
| 9 | [`08_Upload-ACL-Access.md`](08_Upload-ACL-Access.md) | Access-control on uploads, incl. the mobile shift. Anchors: FU-43850 (Vimeo `$1,000` two-account A/B proof), FU-97452 (Shopify rte/assets, $500 json), FU-258460 (Quora exported UploadService, $500). |
| 10 | [`09_Adjacent-Noise-Upload-Shelf.md`](09_Adjacent-Noise-Upload-Shelf.md) | The shelf: S3-hosting design notes (FU-7929), intended-behavior rows (172694), a size-check harden row, a GET/POST asymmetry XSS, and the title-misfiled $5,000 Jenkins row (FU-258117, RCE/AUTH cross-ledgers). |

## References (provenance layer)

| File | Contents |
|---|---|
| [`references/source-index.md`](references/source-index.md) | Roster provenance (nathan.sx mirror re-used from the RCE archive), the 7 title arms (upload/traversal/lfi/rfi/file-read/incl/malfile), funnel (86→65×200 · 21×404 · 0 transients), bounty reconciliation chain, BBH taxonomy check (no file-upload type page; getinfo buckets 236/14/1/19/9/5 vs the master-list's legacy `236+14+19+12`), era spread, 5 limitations. |
| [`references/case-register.md`](references/case-register.md) | Row-per-row ledger of all 86 roster rows: case ID, team, substate, bounty (json/list/404-list labeled per row), class 01–09/dead, disposition note. The header carries the weakness census, severity census, era spread, and the 11-row cross-vault share map. |
| [`references/blogs-index.md`](references/blogs-index.md) | §1 two byte-quoted file-upload guides (bugbountyhunter.com `fileuploads` guide page — the extension ladder, content-type play, filename smuggle, closing JWT-header payload §1a; PortSwigger's Web Security Academy file-upload frame — definitional block, impact decomposition, web-shell worst case §1b) · §2 209 title-linked bugbountyhunting.com writeups curated by lane (76 upload / 44 traversal / 52 inclusion-file-read / 35 arbitrary-file / 2 webshell, 15 drops with reasons) · §3 sixteen modern hardening-era cases (Starbucks webshell 506646, Google springboard LFI $13,337, Grafana zero-day traversal, CSPT2CSRF…) · §4 dropped-selection record. |
| [`references/archive/bodies-full-dump.txt`](references/archive/bodies-full-dump.txt) | All 65 retrieved report bodies, verbatim dump (1,408 lines) + the 21 dead headers. |
| [`references/archive/json/`](references/archive/json/) | All 86 raw JSON responses from `hackerone.com/reports/<id>.json` (21 are preserved 404 pages). |
| [`references/archive/bounty-reconciliation.json`](references/archive/bounty-reconciliation.json) | Per-row bounty reconciliation (json/list/404-list/none + module) — script-verified to the cent. |
| [`references/archive/http-codes.txt`](references/archive/http-codes.txt) & `fetch.log` | The 21 dead-404 ids as fetched; fetch timing log. |
| [`references/archive/classes.json`](references/archive/classes.json) | The frozen 86-row module assignment (bodies-win classification) + cross-vault map. |
| [`references/archive/roster-meta.json`](references/archive/roster-meta.json) | Per-row team/substate/severity/weakness/disclosed metadata. |
| [`references/archive/mirror-all-rows.json`](references/archive/mirror-all-rows.json) | The full mirror snapshot (4,419 rows; shared source of every vault in the series). |
| [`references/archive/bbhunt-fup-raw.json`](references/archive/bbhunt-fup-raw.json) | The 224 raw file-upload-class blog matches pre-curation. |
| [`references/archive/bbh-*` + `portswigger-*`] | The fetched §1 sources (HTML + text transcripts) and the BBH `/disclosed/` page, script index, `index-all.json`, guide page, and six weakness `getinfo` endpoints. |

## How this vault was built (method)

1. **Roster**: the byte-verified `h1.security.nathan.sx` mirror copy (4,419 rows, frozen
   2017-09-12, shared with all prior vaults), filtered by 7 case-insensitive title arms —
   `upload`, `traver`, `l\.?f\.?i`/`local file inclus`, `r\.?f\.?i`/`remote file inclus`,
   the file-read/`arbitrary file` family, `file inclusion`/`include($`/`require($`, and
   `malicious file` → **86 unique rows, single-pass funnel, no supplemental pass** (each
   of the 86 recast into exactly one module or the dead-list on body read).
2. **Retrieval**: every report fetched live from the public unauthenticated
   `hackerone.com/reports/<id>.json` endpoint, 1.4 s spacing → 65×200, 21×404, zero
   transient failures (three of the 404s re-confirm rows already dead in the RCE build).
3. **Reading**: all 65 bodies read end-to-end (`archive/bodies-full-dump.txt`); every
   class decided by bodies, not titles. Body-field differences handled honestly: 47 rows
   carry `vulnerability_information`, 18 carry the disclosed `summaries` field (mostly the
   DoD-voice rows and vendor-summary rows — 0 rows metadata-only, a series first).
4. **Bounty accounting**: JSON `bounty_amount` where present ($3,426 across 8 rows),
   otherwise the mirror's list-stated figure ($41,815 across 26 rows), labeled per row;
   $26,628 sits on 404 rows (12 with figures; largest FU-142562 $10,000 — which is also
   RCE-142562 and XXE-142562), with the $13,800 three-row overlap against the RCE
   dead-list kept visible, never silently deduped.
5. **Modules**: nine class modules (incl. the FP/harden shelf), each with verbatim
   evidence, case-stock tables with labeled bounties, corpus-derived techniques, and
   kill-gates.
6. **Quote audit (zero-miss gate)**: §1 of the bibliography checked mechanically against
   its two archived transcripts (8/8 blockquote blocks matched after whitespace
   normalization); all module blockquotes and payload/code fences checked against
   `bodies-full-dump.txt` (this build's probe count: 43/43 fences+blockquotes verified,
   zero misses, plus a separate multi-line inline-quote pass). Zero unanchored quotes
   remain.
7. **Bibliography**: two file-upload guides fetched and byte-quoted (the BBH guide page +
   PortSwigger's academy frame — both inside this build's fetch set, linked from each
   other); 209 community writeups title-linked (bodies not fetched — the index is a hunt
   queue, not proof); 16 modern post-roster cases kept out of register counts.

## Coverage vs limitations

**Covered**: unrestricted/authless upload → execution and device compromise (device
file-serve CGIs, processor delegates, carrier-firmware uploaders); upload-from-URL SSRF and file-read
(error-leak, SVG `xlink:`, playlist `concat:`, redirect scheme-hopping); upload → stored
XSS/served-content execution (content-type swaps, applet trust, callback gadget hunting,
filename-in-error interpolation); file inclusion (dispatcher path override, fix bypass by
separator permutation, include-to-RCE via writable landing, parser directives, XLIFF
external entities); path traversal read/write/delete (processor params, archive symlinks,
bucket-path escape, unlink flows, path-disclosure pricing); reflected file download and
browser download naming (307/308 re-upload); server-side arbitrary file download (DoD
estate shapes); upload-ACL across server and Android lanes; the noise floor with its own
doctrine (hosting-misuse, intended-behavior, misfiled money rows).

**Honest limitations**:
1. The roster is a 2013–2017 snapshot (era spread 2014×6 · 2015×8 · 2016×24 · 2017×27 on
   live rows) — modern upload hardening (signed uploads, blob validation, egress
   filtering, CSPT research) is fingerprinted in playbook P4 and bibliography §3 only,
   labeled outside the corpus.
2. 21 rows are permanently dark (404) — recorded, never quoted; their list figures
   ($26,628/12) are kept in dead-list arithmetic, with the RCE-shared three kept visible.
3. 18 of 65 live bodies arrive through the `summaries` field rather than
   `vulnerability_information` — vendor/DoD summary voice; nothing invented, technique
   granularity capped accordingly. Zero `len=0` metadata rows (a series first).
4. Blog bodies were not fetched — `blogs-index.md` §2 is a hunt queue, not proof; §1 is
   byte-quoted from two actually-fetched guide sources.
5. Weakness labels are era mislabels in places (e.g. FU-20720's dead title reads "File
   upload XSS using Content-Type header", FU-97501's weakness col reads "CSRF" for an
   SSRF-by-SVG row,
   FU-18371's reads "Command Injection" for a traversal, FU-107960's weak col is `None`
   for a paid RFD row) — the register keeps the archive label; modules correct against
   the body ("bodies win").
6. The BBH taxonomy check is a dated snapshot (2026-11-05): the master-list's legacy
   `+12` figure maps to no single live bucket (nearest adjacent: 6297=9, 9149=5) —
   source-index §4 records the drift without forcing a match.
7. No live testing was performed — validate against the hunt-file-upload scenario
   matrices of the bug-bounty skillset before executing.

## The one-paragraph doctrine of this corpus

Upload-class money in this corpus is priced by **what happens after the bytes land**:
the webserver that executes them paid up to $18,000 on a device that never asked who was
uploading; the image processor that obeyed markup paid $800–$5,000 depending on whether
it read one file or obeyed a playlist; the CDN that let a swap decide its content type
paid $200–$1,500; and the plain file-in-the-directory rows — include without a writable
landing, listing without a scope check — paid $25–$500 or nothing at all. The finds that
converted class-knowledge into money are small and gradable (one `type=file`→`type=url`
toggle, one `../` in a filename, one `callback=` gadget name, one extra `..` past the
numbered folder), the honest ceilings were priced rather than punished (201529's "cannot
utilize for RCE" disk-fill DoS closed at $150 (list); 158021's policy-gap path disclosure
at $100 (json)), and every lane-boundary dispute in the register — RFI-title-vs-image-load,
ACL-vs-IDOR, upload-title-vs-console-auth — was settled by reading the body, never the
title.


<!-- CASESTOCK-LINK:BEGIN -->

## Case stock — vault (`_VAULT/`)

**284 disclosed reports** routed to this category · 45 with a bounty figure · **$139,574** · 215 full write-ups stored locally.

- Full list: [`_VAULT/by-vault-category/File-Upload.md`](../_VAULT/by-vault-category/File-Upload.md)
- Query: `sqlite3 ../_VAULT/reports.sqlite "SELECT id,bounty,title FROM reports WHERE ..."`
- Pull one write-up: `python3 ../_VAULT/scripts/extract_report.py <id>`

| Top paid | Program | Bounty |
|---|---|---|
| [1439593](https://hackerone.com/reports/1439593) Arbitrary file read  via the bulk imports UploadsPipeline | GitLab | $29,000 |
| [827052](https://hackerone.com/reports/827052) Arbitrary file read via the UploadsRewriter when moving and issue | GitLab | $20,000 |
| [1132378](https://hackerone.com/reports/1132378) Arbitrary file read during project import | GitLab | $16,000 |
| [822262](https://hackerone.com/reports/822262) Path traversal in Nuget Package Registry | GitLab | $12,000 |
| [3962925](https://hackerone.com/reports/3962925) Launchpad file read leaks production keys | Basecamp | $9,337 |

_refreshed 2026-11-17 from the public HackerOne disclosed-report dataset_
<!-- CASESTOCK-LINK:END -->
