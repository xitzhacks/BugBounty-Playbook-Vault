---
title: "Vault/16_Information-Disclosure — the disclosure playbook set"
type: index
category: "Information Disclosure (GraphQL/API object exposure · HackerOne self-disclosure · user PII/location/privacy · file/path/error/secret leaks · protocol & memory disclosure · adjacent noise)"
built: "2026-11-07"
evidence: "362 h1-brain corpus rows (classified info-disclosure bucket 340 + 22 unclassified merges) — 356 full bodies + 6 GHSL metadata-only one-liners · all bodies read end-to-end (classified bodies verified byte-equal to DB vulnerability_information: 0 mismatches)"
bounty: "$281,925 across 161 rows (bucket-340 $217,375/149 · merges $64,550/12) · modules: 01 $19,252/13 · 02 $83,580/28 · 03 $47,014/56 · 04 $48,697/41 · 05 $15,468/6 · 06 (merged) $67,914/17 · excluded merge max $50,000 (INFO-1087489) — see references/case-register.md"
companion_vaults: "../22_GraphQL · ../SSRF · ../Authentication-Session · ../IDOR · ../Cache-Poisoning · ../15_Cache-Poisoning · ../18_Misconfiguration"
case_id_scheme: "INFO-<HackerOne report id>"
quote_rule: "byte-true, (sic)-marked, from archived bodies only (references/archive/INFO-bodies-full-dump.txt); GHSL one-liners recorded never quoted as technique"
---

# Vault/16_Information-Disclosure — the disclosure playbook set

One vault, six modules, one classifier's cut: the h1-brain `info-disclosure` bucket (340 rows) plus the two adjacent pools the unclassified merges added (22 rows) = **362 rows, $281,925/161 paid**. The bucket max is INFO-3000510 (**security, $25,000** — the HackerOne `/reports/:id.json` credential disclosure); the corpus max is INFO-1087489 (**shopify, $50,000** GitHub PAT, in the unclassified merge — labeled separately throughout so no headline misleads). The vault's doctrine: **disclosure pays by whose data and what class, not by technique** — a `$25,000` redacted-twin endpoint, a `$12,500` patch-residue export, an `$8,868` pixel of process memory, and a `$100` dotfile are the same primitive at four prices.

## Start here

| # | File | What it gives you |
|---|---|---|
| 1 | [`INFO-Testing-Agent-Playbook.md`](INFO-Testing-Agent-Playbook.md) | **The executable protocol.** P0 program/policy read → P1 field/endpoint inventory (GraphQL selection sets, serializers, exports, caches) → P2 probe protocol (field oracle → differential count → enumeration → cache/header → dotfile sweep) → P3 proof ladder → P4 modern hardening fingerprints → P5 kill-gates. |
| 2 | [`01_GraphQL-API-Objects-Exposure.md`](01_GraphQL-API-Objects-Exposure.md) | The field *is* the bug: one object, five $2,500 Team rows; Shopify's no-permission staff pivots; GitLab system-note/email split. Anchors: INFO-978143, INFO-770209, INFO-1085332, INFO-423388. |
| 3 | [`02_HackerOne-Reports-Bounty-Privacy.md`](02_HackerOne-Reports-Bounty-Privacy.md) | The platform disclosing itself: the $25,000 `.json` twin, the $10,000→$12,500 export fix/residue pair, search/hackbot/H2 oracles, the $500 metrics floor. Anchors: INFO-3000510, INFO-186230, INFO-182358, INFO-188719, INFO-2213251. |
| 4 | [`03_User-PII-Location-Privacy.md`](03_User-PII-Location-Privacy.md) | Enumerations (Uber invite census $3,000), session-carrying caches (Active Storage $4,323), consent toggles (X $2,940 ×2), order lookups. Anchors: INFO-3082917, INFO-125200, INFO-434763, INFO-472013, INFO-968165. |
| 5 | [`04_File-Path-Errors-Secrets-Leaks.md`](04_File-Path-Errors-Secrets-Leaks.md) | Dotfiles, buckets, feeds, dumps, and dumped tokens: GitLab runner serialization ($12,000), workhorse file-steal ($10,000), Shopify atom bypass ($5,000), S3/Ping bucket ($2,900), Podfile + CI-log tokens ($1,500 each). |
| 6 | [`05_Protocol-Memory-Disclosure.md`](05_Protocol-Memory-Disclosure.md) | Uninitialized reads, PASV trust, stack contents: the $8,868 librsvg pixel, NGINX QUIC ($2,600), curl TELNET ($1,000). Smallest paid module, densest per finding. |
| 7 | [`06_Adjacent-Disclosure-Noise.md`](06_Adjacent-Disclosure-Noise.md) | The negative space and the merge: the $50,000 PAT, the GHSL metadata sextet ($13,400 without bodies), chain origins (SSRF/DNS-rebinding priced $100 for benign content), dotfile singles at $0. |

## Scoreboard (362 rows · 161 paid · $281,925 · bucket max $25,000 · corpus max $50,000)

Top paid rows (bucket and merges distinguished):

| Case | Title (short) | Program / Module | Bounty |
|---|---|---|---|
| INFO-1087489 | GitHub access token exposure (employee PAT) | shopify / 06 *merge* | **$50,000** (corpus max) |
| INFO-3000510 | `/reports/:id.json` leaks reporter email, OTP codes, `graphql_secret_token` | security / 02 | **$25,000** (bucket max) |
| INFO-186230 | Internal attachments exportable via "Export as .zip" (fix residue) | security / 02 | **$12,500** |
| INFO-509924 | Quick Actions serializes Project → all Runner tokens | gitlab / 04 | **$12,000** |
| INFO-182358 | "Export as .zip" discloses partially-disclosed comments | security / 02 | **$10,000** |
| INFO-188719 | `/skills` call discloses all review-queue reports | security / 02 | **$10,000** |
| INFO-850447 | workhorse bypass reads `allowed_paths` + `/proc/PID/fd` files | gitlab / 04 | **$10,000** |
| INFO-2107680 | librsvg uninitialized memory → AWS keys + user cookies in pixels | basecamp / 05 | **$8,868** |
| INFO-1256375 | Blog atom feed bypasses password via preview host | shopify / 04 | **$5,000** |
| INFO-1122661 | CWE-312 SharedPreferences cleartext (GHSL metadata) | github-security-lab / 06 *merge* | **$4,500** |
| INFO-3082917 | Active Storage caches `Set-Cookie` (session leak) | ibb / 03 | **$4,323** |

Module totals: 01 $19,252/13 · 02 $83,580/28 · 03 $47,014/56 · 04 $48,697/41 · 05 $15,468/6 · 06 $67,914/17 (merged adjacent+unclassified).
Weakness census (362): `Information Disclosure` 302 · `Privacy Violation` 23 · `Cleartext Storage of Sensitive Information` 15 · `None` (unclassified merges) 22.
Program mix (top): security 83 (HackerOne self-audit) · shopify 36 · x 23 · ibb 21 · nextcloud 17 · gitlab 15 · brave 12 · automattic 8.

## References (provenance layer)

| File | Contents |
|---|---|
| [`references/source-index.md`](references/source-index.md) | Roster provenance (h1-brain DB, sha256, 3,673 rows), classification funnel (3,673 → 340 bucket + 22 merges → 362), bounty accounting, era discipline, 7 limitations. |
| [`references/case-register.md`](references/case-register.md) | Row-per-row ledger of all 362 rows: case ID, program, weakness, asset/CVE, bounty, module, evidence level. |
| [`references/archive/INFO-bodies-full-dump.txt`](references/archive/INFO-bodies-full-dump.txt) | All 362 bodies verbatim (anchor for every quote). |
| [`references/archive/classes.json`](references/archive/classes.json) | The frozen 362-row module assignment (bodies-win classification). |

## How this vault was built (method)

1. **Bucket**: `classified.json` `info-disclosure` = 340 rows (302 `Information Disclosure` + 23 `Privacy Violation` + 15 `Cleartext Storage` weakness labels in the DB). All 340 ids verified present in `module_map_all.json` (21+51+128+104+17 = 321) plus 19 `_adjacent` = 340 exactly; no duplicates.
2. **Merges**: 22 `_adjacent_unclassified` rows from the classifier's `unclassified` pool (468) appended as the tail of module 06 — vault total 362. The merges are labeled in every total (their $64,550/12 and their $50,000 max are never folded into bucket arithmetic).
3. **Bodies**: `classified.json` bodies verified byte-equal to DB `vulnerability_information` for all 362 ids (0 mismatches) before quoting; no live HackerOne fetch this build.
4. **Modules**: six playbooks, each with YAML frontmatter, case-stock table (all rows, bounty-sorted), byte-true quotes for top paid cases, §6 what-pays/what-doesn't, §7 cross-references.
5. **Quote audit (zero-miss gate)**: every blockquote was verified byte-exact against the dump (see report footnote); GHSL one-liners are recorded as metadata, never quoted as technique.

## Cross-vault links

- `../22_GraphQL/` (upcoming) — module 01 is its pricing shelf: field-exposure technique there, per-field dollars here.
- `../SSRF/` — INFO-53004's DNS-rebinding probe reads, INFO-228377/237381, and INFO-663729 are SSRF-origin disclosures; file here for the read, there for the request.
- `../Authentication-Session/` — OTP backup codes / `graphql_secret_token` (INFO-3000510), session-cookie caches (INFO-3082917), `gauth_secret` (INFO-1276373), archive-mined JWTs (INFO-2193454): token secrecy there, redaction pricing here.
- `../IDOR/` — INFO-509924 (serialization of inaccessible projects) and INFO-968165 (order lookup) are object-authorization failures whose *price* is disclosure; cite both when the consumer is a report template.
- `../Cache-Poisoning/` / `../15_Cache-Poisoning/` — INFO-3082917 (session cookie in public cache) is cache poisoning whose payload is a session, not a script.
- `../Race-Conditions/` — INFO-493176's HTTP/2 ordering oracle is the timing sibling of the race vault's oracle discipline; both price *ordering/differential* side channels.

## Coverage vs limitations

**Covered**: GraphQL object/array exposure (HackerOne + Shopify + GitLab), platform self-disclosure via serializers/exports/search/bot layers, PII enumeration and consent-state privacy, file/path/error/secret hygiene (dotfiles, buckets, feeds, logs, SDK normalization), protocol & memory reads (image coders, QUIC, TELNET/FTP clients), and the adjacent/merge negative space with chain origins.

**Honest limitations**:
1. **Pool discipline**: $50,000 (INFO-1087489) and $13,400 (GHSL metadata rows) come from the 22-row unclassified merge, not the 340-row bucket. Bucket-340 totals ($217,375/149, max $25,000) are the class-pure headline; 362-row totals are labeled wherever used.
2. **`None` bounty ≠ unpaid**: 201 of 362 rows carry no DB figure. HackerOne does not always publish figures; $281,925 is a corpus floor.
3. **6 GHSL metadata-only rows** (INFO-886287, 1026252, 1122661, 1122662, 1365761, 1526609) carry $13,400 with no quotable body — anchors, not evidence. No technique is built from them.
4. **Weakness labels are triage artifacts**: `Information Disclosure` (302), `Privacy Violation` (23), `Cleartext Storage` (15), and `None` (22) overlap heavily by body (e.g., INFO-1575014 is a *path-traversal* PII row; INFO-472013 is a *state-toggle* row). Modules classify by body behavior; the register keeps the DB label.
5. **Program skew**: `security` (83 rows, 47 in module 02 alone) is HackerOne auditing itself — per-field flat pricing ($2,500 ×5, $500 ×20) reflects that program's tiers, not a universal rate card.
6. **Era honesty**: rows span the h1-brain disclosure era (2015–2025-era disclosures incl. CVE-2024-3416); tooling and endpoint evidence is historical record, and modern hardening is fingerprinted in playbook P4, not asserted as doctrine.
7. **No live testing was performed** — validate against the hunt-graphql / hunt-api-misconfig / hunt-auth skill scenario matrices; every quote is archive-anchored, never re-fetched this build.


<!-- CASESTOCK-LINK:BEGIN -->

## Case stock — vault (`_VAULT/`)

**1,890 disclosed reports** routed to this category · 344 with a bounty figure · **$417,002** · 1,194 full write-ups stored locally.

- Full list: [`_VAULT/by-vault-category/16_Information-Disclosure.md`](../_VAULT/by-vault-category/16_Information-Disclosure.md)
- Query: `sqlite3 ../_VAULT/reports.sqlite "SELECT id,bounty,title FROM reports WHERE ..."`
- Pull one write-up: `python3 ../_VAULT/scripts/extract_report.py <id>`

| Top paid | Program | Bounty |
|---|---|---|
| [591813](https://hackerone.com/reports/591813) [Pre-Submission][H1-4420-2019] API access to Phabricator on code.uberinternal.co | Uber | $40,000 |
| [231460](https://hackerone.com/reports/231460) Open prod Jenkins instance | Snapchat | $15,000 |
| [911606](https://hackerone.com/reports/911606) Leaked JFrog Artifactory  username and password exposed on GitHub - https://snap | Snapchat | $15,000 |
| [1024899](https://hackerone.com/reports/1024899) file read on MCS servers via supplying a QCOW2 image with external backing file | Mail.ru | $15,000 |
| [186230](https://hackerone.com/reports/186230) Internal attachments can be exported via "Export as .zip" feature | HackerOne | $12,500 |

_refreshed 2026-11-17 from the public HackerOne disclosed-report dataset_
<!-- CASESTOCK-LINK:END -->
