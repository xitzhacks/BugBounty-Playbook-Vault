---
title: "SSRF Knowledge Base — README"
type: index
candidates: 82
retrievable: 58
full_bodies_read: 45
confirmed_cases: 26
adjacent_cases: 3
metadata_only_rows: 11
excluded_after_read: 18
body_withheld_corpora: 13
bounty_total_confirmed: "$9,144"
bounty_total_ssrf_relevant: "$16,994"
bounty_total_on_404_rows: "$10,819 (archive-stated, unrecoverable)"
external_sources_read: 6
modern_layer_anchors: 1
archive_accessed: "2026-10-24"
archive_frozen: "2017-09-12"
case_id_scheme: "SRF-<HackerOne report id>"
built_for: "AI-agent executable testing"
---

# SSRF Knowledge Base

Built from **82 title-matched candidate reports** in a frozen 12 Sept 2017 mirror of
published HackerOne disclosures (`https://h1.security.nathan.sx/`, 4,419 rows), of which
**58 remained retrievable** at origin and **45 returned full readable bodies**. After
body-read classification: **26 confirmed SSRF cases across 6 category playbooks**,
plus 3 adjacent internal-service-exposure cases, 11 metadata-only rows kept at
honest evidence level, 18 excluded after body-read, and 24 now-404 titles recorded.
Companion to the XSS and IDOR knowledge bases in
[`../XSS/`](../XSS/README.md) and [`../IDOR/`](../IDOR/README.md).

## Start here

| File | Use it for |
| --- | --- |
| **[`SSRF-Testing-Agent-Playbook.md`](SSRF-Testing-Agent-Playbook.md)** | **Executing a test.** Phase-gated agent protocol: intake → surface mapping (S1–S10 sinks) → baseline → Route R1 9-rung ladder → calibration → GATE 3 validation → severity → reporting → remediation → regress. |
| [`references/source-index.md`](references/source-index.md) | Case provenance: every candidate's disposition (the 82-row table), bounty history, 404 roster, two-net discovery record. |
| [`references/blogs-index.md`](references/blogs-index.md) | The era methodology bibliography (6 sources) + the modern PortSwigger layer, with the recovery story of a dead aggregator. |
| The 6 category playbooks → | The evidence itself, per class (below). |

## Category playbooks

| File | Cases in file | What the class taught the playbook |
| --- | --- | --- |
| [`Port-Scan-and-Internal-Mapping.md`](Port-Scan-and-Internal-Mapping.md) | 12 | Differencing oracles beat "read it" — calibrate on known-open/known-closed ports first; channels: status codes, error strings, cURL codes (56/7/28), timing, subnet hints, banner-in-error. Includes the era's XSPA lexicon root. |
| [`Validation-Bypass-and-Scheme-Abuse.md`](Validation-Bypass-and-Scheme-Abuse.md) | 6 | The wrapper is the bug: `dict://`, `gopher://` via 302-relay, TFTP-over-UDP, `[::]` denylist slip; its era-quoted methodology source is the **SSRF bible. Cheatsheet**. |
| [`Cloud-Instance-Metadata.md`](Cloud-Instance-Metadata.md) | 3 | EC2 user-data + IMDS reachable from multi-tenant sinks; `0x7f.1`-style hex bypass; failure-email presence as an IMDS oracle; era precursors to IMDSv2's emergence. |
| [`Media-Processing-SSRF.md`](Media-Processing-SSRF.md) | 3 | FFmpeg/libav family: m3u8-in-upload, concat LFI, GAB2-in-AVI smuggling; full-file read via playlist chains; the corpus's most "modern-feeling" 2016 bugs. |
| [`Blind-SSRF-and-Callback.md`](Blind-SSRF-and-Callback.md) | 3 | Callback attribution loop: listener logs (IP+UA), product notification absence/presence, remote-party log entries; the era's weaponization — 162k-site pingback DDoS relay. |
| [`Internal-Service-Exposure.md`](Internal-Service-Exposure.md) | 6 | What the port oracle finds: Zookeeper `dump`/`envi`, Splunk default creds, command-injectable webtop — the consequences inventory. |

## Methodology and how this was built

1. **Archive harvesting.** The mirror's root index (4,419 published rows, frozen at
   12 Sept 2017; no per-vulnerability-type pages exist in it) was parsed into a dataset
   with title / team / weakness / severity / bounty / body fields.
2. **Two title-matching nets.** Net 1 (core SSRF patterns: "SSRF", "server side request
   forgery", "port scan", "internal", scheme words, XSPA) → 73 candidates; Net 2
   (media/URL-import wording: "video", "URL", "import", "webhook", "validator"
   patterns) → +9. Title-match was *filter only* — bodies decided classification.
3. **Conservative fetching.** Each candidate's public, unauthenticated JSON
   (`hackerone.com/reports/<id>.json`) was fetched at 1.2 s spacing with a disk cache.
   58/82 retrievable; 24 returned HTTP 404 (report no longer public) and are recorded
   in the source-index, not dropped. 45 full bodies resulted.
4. **Body-read classification.** Every full body was read and dispositioned: 26
   confirmed SSRF, 3 adjacent internal-service findings kept as evidence, 16 excluded
   as not-SSRF (XSS/IDOR/DoS/RCE/library advisories) with reasons recorded; the 13
   body-withheld rows stay at metadata level (titles/labels/bounty only). A
   library-advisory exception row (`SRF-73242`, libcurl) is kept at metadata level.
5. **Case IDs.** `SRF-<report id>` throughout, mirroring the
   [`IDOR`](../IDOR/README.md) and XSS vault conventions.
6. **Bounty rule.** JSON amount where present, else the archive's own
   "Paid Out"-table amount, labeled "(archive-stated)"; overlapping values agree.
7. **Bibliography.** The bugbountydaily links database used by the IDOR vault died
   mid-project (NXDOMAIN, zero Wayback captures — see
   [`references/blogs-index.md`](references/blogs-index.md) frontmatter). Its
   replacement is strictly more defensible: the six era sources **the corpus reports
   themselves cite** (XSPA 2012, Acunetix 2013, Sucuri 2014, SSRF-bible 2017, Habr
   2016, oss-security 2016) recovered by URL or Wayback and read in full, plus one
   clearly-separated modern PortSwigger anchor.

## Coverage statistics

| Metric | Value |
| --- | --- |
| Archive rows scanned | 4,419 |
| Title-matched candidates | 82 (net 1: 73, net 2: +9) |
| Retrieved from origin | 58 (24 × 404) |
| Full bodies read | 45 |
| Confirmed SSRF cases | 26 |
| Adjacent internal-service cases | 3 |
| Excluded after body-read | 18 (16 full-body reasons + 2 metadata titles) |
| Metadata-only rows kept | 11 (7 SSRF-labeled, 3 internal-exposure, 1 library advisory) |
| Era range of cases | 2013 – 09/2017 (SRF-1409 → SRF-243277) |
| Programs represented | 14 among the 26 confirmed + 3 adjacent (Shopify 5, Imgur 4, Nextcloud 3, WordPress/Automattic 3, Phabricator 2, Slack 2, Twitter 2, Mixmax 2, RelateIQ, Factlink, APITest.io, Instacart, Veris Labs, Discourse), plus VK, Bime, and Ok in the metadata-only rows |

### Bounty pyramid (SSRF-relevant, era amounts)

| Band | Amount | Cases |
| --- | --- | --- |
| Confirmed-SSRF total | **$9,144** | 26 (16 paid, JSON $514 + archive-stated $8,630) |
| Adjacent internal-service total | **$4,500** | 3 (SRF-73567 $3,000, SRF-154369 $1,000, SRF-158118 $500) |
| Metadata-only SSRF rows | **$3,350** | 7 (VK ×3, Ok $500, Bime $1,250, DoD $0) |
| **SSRF-relevant total** | **$16,994** | 36 |
| Archive-stated on now-404 rows | **$10,819** | 24 (incl. $3,000, $1,500, $1,000 titles) — recorded, not claimable |

Era-internal sanity anchors: the era's largest confirmed payout in this corpus is
Imgur's `SRF-115748` `vidgif/url` SSRF at **$2,000**; the smallest known is Instacart's
`SRF-158016` at **$50** (JSON-verified). Amounts are as-recorded history, not
guidance for modern triage.

## Limitations — read this before testing from these files

1. **Era labels are historical.** Several archive weakness labels are demonstrably
   wrong for the body ("Command Injection", "CSRF", "Code Injection",
   "Uncontrolled Resource Consumption" on pure-SSRF bodies). Bodies are the class
   authority; labels are recorded as-is in playbook "Archive-era labels" sections.
   Bounty/severity amounts are era history, not modern triage guidance.
2. **IMDSv2 and the modern layer.** The corpus predates instance-metadata defenses
   (IMDSv2 pinning, egress controls, `.internal` allowlisting). Cloud-Instance-Metadata
   playbook flags what changed; the PortSwigger MODERN-1 anchor is quoted for the
   bypass table modern triage expects.
3. **Metadata-only rows.** The 11 rows cite no-bodiness explicitly — no technical
   claim rests on them beyond title/label/bounty. Unauthenticated JSON retrieval
   withholds many 2016-2017 bodies; do not confuse "no body" with "no finding".
4. **404 rows.** 24 titles (some famous: New Relic, Yahoo `view-source`, Pornhub
   FFmpeg) can never be quoted — their numbers are recorded in the source-index and
   excluded from lesson-building.
5. **Excluded rows.** The 18 exclusions are recorded *with reasons* so a future
   re-classification can't silently re-include what was read and rejected.
6. **The "239" number.** A count of "239 SSRF reports" was requested for this vault
   and is **not reproducible from this archive**: the mirror has no
   vulnerability-type index pages or tags, and two independent title nets over all
   4,419 rows yield 82 candidates, of which bodies confirm 26. No source is cited
   for "239"; if you saw it somewhere (e.g. a live-site tag count, a different
   aggregator), point me at it and I'll reconcile the discrepancy honestly.
7. **Conservative access.** No auth, no access-control bypass, 1.2 s spacing,
   everything disk-cached; nothing was done against live HackerOne other than
   public JSON reads.

## Notes about the file list

- `SSRF-Testing-Agent-Playbook.md` — the executable protocol; starts from GATE 0
  and references category files by name at each route decision.
- `references/source-index.md` — §1 provenance & method, §2 the two nets, §3
  fetch log, §4 the 82-row disposition table (generated), §5 bounty totals &
  rule, §6 404 roster, §7 category routing map.
- `references/blogs-index.md` — the six era sources with verbatim quotes (including
  the dead-aggregator note), cited-but-not-read tech references, and the modern
  PortSwigger layer.
- The six category files share one structure: Overview → Case evidence (verbatim
  quotes with `(sic)` marks and glosses for non-English rows) → Anatomy/calibration →
  Agent execution template (context blocks) → Validation gates → Remediation →
  Archive-era labels/family notes. Misquoted text is corrected only if it changes
  technique; otherwise preserved with a `(sic)`.
- Quote discipline: every quote is verbatim from the case's own body or the
  bibliography's cached sources; era typos marked; Russian-language titles carry
  glosses.


<!-- CASESTOCK-LINK:BEGIN -->

## Case stock — vault (`_VAULT/`)

**324 disclosed reports** routed to this category · 102 with a bounty figure · **$175,059** · 167 full write-ups stored locally.

- Full list: [`_VAULT/by-vault-category/SSRF.md`](../_VAULT/by-vault-category/SSRF.md)
- Query: `sqlite3 ../_VAULT/reports.sqlite "SELECT id,bounty,title FROM reports WHERE ..."`
- Pull one write-up: `python3 ../_VAULT/scripts/extract_report.py <id>`

| Top paid | Program | Bounty |
|---|---|---|
| [2262382](https://hackerone.com/reports/2262382) Server Side Request Forgery (SSRF) via Analytics Reports | HackerOne | $25,000 |
| [1406938](https://hackerone.com/reports/1406938) Full Response SSRF via Google Drive | Dropbox | $17,576 |
| [826361](https://hackerone.com/reports/826361) SSRF on project import via the remote_attachment_url on a Note | GitLab | $10,000 |
| [1960765](https://hackerone.com/reports/1960765) Blind SSRF to internal services in matrix preview_link API | Reddit | $6,000 |
| [776017](https://hackerone.com/reports/776017) Half-Blind SSRF found in kube/cloud-controller-manager can be upgraded to comple | Kubernetes | $5,000 |

_refreshed 2026-11-17 from the public HackerOne disclosed-report dataset_
<!-- CASESTOCK-LINK:END -->
