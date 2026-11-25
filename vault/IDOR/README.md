---
title: "IDOR Knowledge Base — README"
type: index
cases: 73
bounties_disclosed: 19
bounty_total: "$14,470"
evidence_split: "55 full bodies / 18 program summaries / 0 title-only"
archive_accessed: "2026-10-16"
archive_frozen: "2017-09-12"
external_blogs_read: 6
built_for: "AI-agent executable testing"
---

# IDOR Knowledge Base

Built from **73 public HackerOne IDOR-class reports** (13 programs) plus **5 external
methodology blogs**, curated and classified so an AI agent can read the playbooks and repeat the
same testing on any target of the same behaviour. Companion to the XSS knowledge base in
[`../XSS/`](../XSS/README.md).

## Start here

| File | Use it for |
| --- | --- |
| **[`IDOR-Testing-Agent-Playbook.md`](IDOR-Testing-Agent-Playbook.md)** | **Executing a test.** Phase-gated agent protocol: authorize → map principals/references/verbs → discover → route → escalate → validate → severity → report → regress. |
| [`references/source-index.md`](references/source-index.md) | Looking up a case. All 73 reports with case IDs, evidence type, bounty, and playbook routing. |
| The 7 category playbooks below | *Understanding* each IDOR class, with case studies and payload corpora. |

## Category playbooks

| Playbook | Cases | What it covers |
| --- | --- | --- |
| [`Cross-Tenant-Object-Level.md`](Cross-Tenant-Object-Level.md) | 34 | The core IDOR: swap an id/uuid/path, reach another tenant's object. Read/write/delete variants; $2500 Shopify flagship cases; GitLab share-chain; Hacktus/omarzzu modern chains. |
| [`Role-Scoping-and-Vertical-Escalation.md`](Role-Scoping-and-Vertical-Escalation.md) | 10 | Low-privilege principal reaches a high-privilege surface: team_members.json, /admin/* endpoints, partner-portal role-mapping, app-platform surfaces. |
| [`Parameter-Gate-and-Hidden-Functions.md`](Parameter-Gate-and-Hidden-Functions.md) | 10 | Unlinked/hidden surfaces, parameter toggles that switch off checks, path-segment references; the four DoD cases. |
| [`Stale-Permission-and-Own-Action.md`](Stale-Permission-and-Own-Action.md) | 7 | In-flight permission revocation (TOCTOU), own-object routes after access was revoked, secondary app surfaces that skip the primary check. |
| [`ID-Scoping-and-Predictable-IDs.md`](ID-Scoping-and-Predictable-IDs.md) | 7 | Soft-delete/membership-loss semantics, incremental ids, UUID-pattern exploitation (omarzzu). |
| [`Invocation-Layer-Mass-Assignment.md`](Invocation-Layer-Mass-Assignment.md) | 3 | Mass assignment reaching ACL logic; missing-Authorization-header bypass; path-normalization middleware confusion. |
| [`Enumeration-and-Financial-Objects.md`](Enumeration-and-Financial-Objects.md) | 2 | Card/PIN/gift enumerability; rate-limit-only defenses; the Starbucks fraud-capable case. |

## Methodology and how this was built

1. **Archive harvesting.** `https://h1.security.nathan.sx/index.html` (4,419 published rows,
   frozen at 12 Sept 2017) was parsed with an authoritative `weakness`-field-aware title
   wrapper, narrowing to **203 title-matched candidates** for IDOR-class intent.
2. **Conservative fetching.** Report JSON was fetched from `https://hackerone.com/reports/<id>.json`
   (public, unauthenticated) at 1.2s spacing with a disk cache; 202 fetched, of which
   **151 returned real bodies** and 51 were 404 (report no longer public).
3. **Evidence-classification.** Each of the 151 was read; 73 were confirmed IDOR-class against
   the case-study corpus, and each received a case ID (`IDOR-NNN`) ordered by program.
   Evidence split: **55 full bodies** and **18 program summaries** (official text recovered
   from Wayback Machine where the body was withheld).
4. **Sub-classification.** Cases were classified into 7 classes by their *own demonstrated
   evidence* (cross-tenant / stale-perm / role-scoping / id-scoped / param-gate / invocation /
   enumeration), then written into the 7 category playbooks with verbatim quotes, request
   dumps, and payload corpora.
5. **Blogs.** bugbountydaily.com's link database (621 curated cybersecurity blog links) was
   filtered; **21 candidates** were title/metadata-classified; **6 were fetched and read in
   full** as BLOG-001..BLOG-004 (IDOR-class) and BLOG-005..BLOG-006 (mass-assignment
   methodology); the other 15 were read or skimmed for classification and excluded for domain
   reasons (k8s / cloud-IAM / CI-CD race / SAML etc.); they remain listed in the index for
   transparency.
6. **No fiction.** Where a case's body was withheld, only the program summary was quoted, and
   the reader is told so. Where a fact is unknown, the playbook says "Not disclosed in the
   source." No CVSS / severities / bounties / dates were invented.

## Coverage statistics

| Metric | Value |
| --- | --- |
| Total cases | 73 |
| Reports with disclosed bounty | 19 |
| Total recorded bounty | **$14,470** |
| Full body available | 55 |
| Program summary only | 18 |
| Programs represented | 13 (Shopify 13, Veris 12, Twitter/X 6, Vimeo 5, DoD 4, wakatime 4, Nextcloud 3, HackerOne 3, 6 others 2 each, 10 programs 1 each) |
| Time range | 2014-03 .. 2017-09-12 (archive frozen) + 2016–2025 external blogs |

### Severity / reward pyramid (from the corpus)

| Tier | Counts | Typical severity anchors |
| --- | --- | --- |
| $2,000–$2,500 | 3 | cross-tenant read at platform scale (Shopify) |
| $500–$2,000 | 4 | cross-tenant object write, platform functionality |
| $100–$500 | 8 | chat-log / invoice / metadata reads; ticket-bombing |
| $0 (no bounty) | 45 | still published and triaged as valid but rewarded undisclosed |
|Enumeration | 12 | basic, rate-limit-defended |

## Limitations

1. **All H1 bounty cases predate 12 September 2017.** No *modern* object-level OWASP API Top 10
   (BOLA/BFLA) techniques look the same in the archive; classifying by `weakness` field labels
   can mislabel by 2017-era program practice. All easier cases (BLOG-001..6) are modern 2016+
   reference works.
2. **No automatic scanners.** The 73 H1 cases were all submitted manually — no single
   dynamic-scanner entry. Build-and-discover work is also manual.
3. **`Register.MyCard` variants** confirmed manually per-app; the same pattern is not guaranteed
   elsewhere.
4. **The evidence split has a title-host bias**: 12 of the 73 cases are title-only *summary*,
   meaning only the program's official disclosure survived, not the researcher's body.
5. **Program-summary-only cases cannot be automated-learning cases.** For example, for
   4 DoD cases only the program summary exists; a reviewer should not design an auto-learn test
   for those cases.

## Notes about the file list

- This README is descriptive only; it is not the testing work.
- The *agent playbook* is the execution entry point and cross-links out to category playbooks.
- Case IDs `IDOR-001..IDOR-073` are stable; they are the join key across all files.
- To regenerate `references/source-index.md` after edits, run
  `python3 /tmp/opencode/idor/gen_index.py` (kept as the dataset's authoritative tool).

*Built 2026-10-17. Evidence surfaces verified 2026-10-16.*


<!-- CASESTOCK-LINK:BEGIN -->

## Case stock — vault (`_VAULT/`)

**360 disclosed reports** routed to this category · 80 with a bounty figure · **$167,988** · 162 full write-ups stored locally.

- Full list: [`_VAULT/by-vault-category/IDOR.md`](../_VAULT/by-vault-category/IDOR.md)
- Query: `sqlite3 ../_VAULT/reports.sqlite "SELECT id,bounty,title FROM reports WHERE ..."`
- Pull one write-up: `python3 ../_VAULT/scripts/extract_report.py <id>`

| Top paid | Program | Bounty |
|---|---|---|
| [743953](https://hackerone.com/reports/743953) Steal private objects of other projects via project import | GitLab | $20,000 |
| [767770](https://hackerone.com/reports/767770) Private objects exposed through project import | GitLab | $20,000 |
| [1819832](https://hackerone.com/reports/1819832) Delete anyone's content spotlight remotely. | Snapchat | $15,000 |
| [3862641](https://hackerone.com/reports/3862641) IDOR allows user to access report details via reference.json endpoint | HackerOne | $15,000 |
| [415081](https://hackerone.com/reports/415081) IDOR to add secondary users in www.paypal.com/businessmanage/users/api/v1/users | PayPal | $10,500 |

_refreshed 2026-11-17 from the public HackerOne disclosed-report dataset_
<!-- CASESTOCK-LINK:END -->
