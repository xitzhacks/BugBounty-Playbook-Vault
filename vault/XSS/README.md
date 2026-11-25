---
title: "XSS Knowledge Base"
type: index
scope: "Public HackerOne XSS reports from h1.security.nathan.sx + BugBountyHunter.com FirstBlood corpus"
archive_accessed: 2026-10-12
bbh_corpus_added: 2026-10-17
sources_h1: 562
sources_bbh: 213
playbooks: 10
---

# XSS Knowledge Base

An evidence-based research library on Cross-Site Scripting, built from two corpora:

1. **562 public HackerOne reports** indexed in
   [Nathan's HackerOne archive](https://h1.security.nathan.sx/), spanning **80
   programs** (all pre-dating 2017-09-12).
2. **BugBountyHunter.com corpus** (added 2026-10-17): **207 disclosed FirstBlood
   hackevent XSS reports** (event-triaged, every body retrieved) plus **6
   methodology/guide pages read for craft discipline**. Catalogue:
   [`references/firstblood-index.md`](references/firstblood-index.md).

Every technical claim in the case studies is traceable to a specific report URL. Facts
extracted from reports are kept strictly separate from general methodology, and missing
data is marked *"Not disclosed in the source"* rather than filled in.

## Scope

**In scope.** Reflected, stored, DOM-based, and self XSS; context-based XSS (attribute,
JavaScript, URL, CSS, nested-parser); filter-bypass and encoding XSS; client-side and
server-side template injection with XSS impact; file-upload and SVG XSS; HTML injection;
browser-extension and `postMessage` XSS.

**Out of scope.** Server-side template injection reaching code execution (needs a
dedicated SSTI playbook — see [Research gaps](#research-gaps)); HTML injection not tied
to executable behaviour; general injection classes (SQLi, SSRF, CSRF) except where they
appear as chain components.

**Sibling knowledge base.** IDOR / broken object-level authorization is built the same way
(73 reports + 6 blogs, 7 category playbooks + agent playbook) in
[`../IDOR/`](../IDOR/README.md).

## Start here

| File | Use it for |
| --- | --- |
| **[`XSS-Testing-Agent-Playbook.md`](XSS-Testing-Agent-Playbook.md)** | **Executing a test.** A phase-gated procedure an AI agent or human follows to actually find XSS: authorize → map → reflect → classify context → route → escalate → validate → report → regress. Start here to *do* the work. |
| The 10 category playbooks below | *Understanding* the work. Deep technical reference per vulnerability class, with the historical case studies. |
- [`references/source-index.md`](references/source-index.md) | Looking up a source. All 562 HackerOne reports with case IDs, plus the BugBountyHunter corpus section. |
| [`references/firstblood-index.md`](references/firstblood-index.md) | Looking up a FirstBlood hackevent report. All 562 FirstBlood disclosures (207 XSS with full bodies + 355 non-XSS metadata rows). |

The agent playbook is the operational entry point; the category playbooks are its
deep-dive companions and are cross-referenced from it at every route.

## Category index

| Playbook | Sources | Full bodies | Summary-only | What it covers |
| --- | ---: | ---: | ---: | --- |
| [`Reflected-XSS.md`](Reflected-XSS.md) | 85 | 48 | 37 | The flagship playbook. Context analysis, testing methodology, inert→executable escalation ladder, false-positive discipline. |
| [`Stored-XSS.md`](Stored-XSS.md) | 154 | 127 | 27 | Cross-user execution, privilege escalation, admin-panel sinks, second-account methodology. |
| [`DOM-Based-XSS.md`](DOM-Based-XSS.md) | 22 | 18 | 4 | Fragment/`postMessage`/storage sources, sink enumeration, origin validation. |
| [`Context-Based-XSS.md`](Context-Based-XSS.md) | 196 | 168 | 28 | The large "Generic XSS" bucket, re-sorted by context and trust boundary. Blind XSS, chains, embeds. |
| [`Filter-Bypass-and-Encoding.md`](Filter-Bypass-and-Encoding.md) | 38 | 38 | 0 | Blocklist bypass, Unicode lookalikes, double encoding, parser differentials. |
| [`Framework-and-Template-XSS.md`](Framework-and-Template-XSS.md) | 4 | 4 | 0 | AngularJS, lodash/twine expression evaluation; the arithmetic-probe technique. |
| [`File-Upload-and-SVG-XSS.md`](File-Upload-and-SVG-XSS.md) | 18 | 13 | 5 | `Content-Type` differentials, SVG allow-list bypasses, MIME sniffing, historical Flash. |
| [`Self-XSS.md`](Self-XSS.md) | 24 | 24 | 0 | Self-inflicted XSS as a defect indicator and chain component; URL-validation flaws. |
| [`HTML-Injection.md`](HTML-Injection.md) | 13 | 11 | 2 | The markup-without-script boundary; non-browser sinks (email, exports, logs). |
| [`Browser-Extension-and-Messaging-XSS.md`](Browser-Extension-and-Messaging-XSS.md) | 8 | 8 | 0 | Extension content scripts, `postMessage` origin/shape validation, embedded-app SDKs. |

The "Sources" columns above count the HackerOne archive only. The FirstBlood corpus
adds FB-* case studies to **Stored-XSS** (FB-078, FB-051, FB-610 series, FB-1310
series), **Filter-Bypass-and-Encoding** (FB-082/189/131/150 + the BBH-001 filter-recon
flow), **DOM-Based-XSS** (FB-219 + JS-file sink keywords), **Reflected-XSS**
(FB-119/122/150/131 + discovery flow), **File-Upload-and-SVG** (BBH-003 upload flow),
and **Self-XSS** (BBH-001 chain guidance) — see the corpus section at the end of
`references/source-index.md`.

Supporting documentation:

- [`references/source-index.md`](references/source-index.md) — the complete inventory.
  **Every one of the 562 sources has its own row**, mapped to its destination playbook.
- [`references/archive/XSS-Knowledge-Base-Complete.md`](references/archive/XSS-Knowledge-Base-Complete.md)
  — a flat concatenation of the 12 canonical files, kept for offline reading or
  single-file import. Superseded by the agent playbook for execution; edit the
  originals, not this.

## Report coverage

**Discovery.** The archive's main index contains 4,419 report rows. 910 matched an XSS
search term. 562 were curated as genuine XSS sources; the remaining 348 were excluded
because HackerOne's own weakness field classified them as CSRF, command injection,
crypto, CRLF, or resource issues, or because the title matched incidentally.

**Evidence quality.** Of the 562 curated sources:

| Evidence level | Count | Share |
| --- | ---: | ---: |
| Full report body retrieved | 459 | 81.7% |
| Partial — HackerOne's official team disclosure summary only | 103 | 18.3% |
| Title-only | 0 | — |

An earlier stage of the sweep retrieved **299 additional titles that are no longer
publicly accessible** (HTTP 404 from HackerOne). Those were dropped during curation
because no metadata was retrievable *and* they did not carry an XSS-indicative title.
They are listed by weakness field in
[`references/source-index.md`](references/source-index.md) § *Sources excluded from the
curated set*.

**Authoritative classification.** HackerOne's own weakness field, across the 562:

| Weakness | Count |
| --- | ---: |
| `Cross-site Scripting (XSS) - Generic` | 514 |
| `Cross-site Scripting (XSS) - Stored` | 22 |
| `Cross-site Scripting (XSS) - Reflected` | 19 |
| `Cross-site Scripting (XSS) - DOM` | 7 |

That distribution is itself a finding: **91% of archived public XSS is filed as
"Generic."** "Generic" is an absence of classification, not a technique — which is why
[`Context-Based-XSS.md`](Context-Based-XSS.md) re-sorts that bucket by context rather
than passing it through.

**Published severity and bounty.** Recorded verbatim from HackerOne where available.
The strongest documented signal is Nextcloud `NC-SA-2017-008`
(`REFL-068`, <https://hackerone.com/reports/216812>): **CVSS v3 3.5
(AV:N/AC:L/PR:L/UI:R/S:U/C:L/I:N/A:N), CWE-79, rated low, $450** — the only archived XSS
case with a complete, sourced CVSS vector, a CWE identifier, a public advisory, and CVE
assignments (CVE-2017-0891).

## Second evidence corpus — BugBountyHunter.com (added 2026-10-17)

The HackerOne archive is frozen in 2017; this corpus fills the modern-technique gap.

**Discovery.** robots.txt permits content pages. All 26 content pages were fetched:
9 vulnerability-type guides (`/vulnerability/?type=…`), 6 guides (`/guides/?type=…`),
7 articles, and 4 static pages. The site's three **FirstBlood hackevent** listing
pages expose 562 disclosed reports from its live events; the **207 typed XSS reports**
(106 Stored XSS + 101 Reflective XSS) were each fetched at the
`/hackevents/report?id=` URL and parsed into
[`references/firstblood-index.md`](references/firstblood-index.md). The 355 non-XSS
reports are preserved as metadata rows in the same file.

**Evidence quality.** All 207 XSS reports were retrieved with their **full submitted
body**, the platform's type/severity triage, the endpoint/parameter/payload
declarations, and the organiser's closing comment. Severity distribution: **17
CRITICAL · 92 High · 95 Medium · 2 Low · 1 Informative**. Bounty information is
sparse by design: the site does not publish a per-report cash table — the corpus
shows a $1,500 bounty split between three collaborators (FB-078 family), two
discretionary awards after deduplication (FB-051, FB-131), and material awards
("Limited edition" hats) for the FB-1310 family. Nothing beyond this was claimed.

**Methodology pages read in full:** the XSS guide (`vulnerability/?type=xss`), the
javascript-files guide, and the file-uploads guide. Read at core-section level: the
open-redirect, CSRF, and waybackmachine pages. The remaining seventeen pages were
fetched and skimmed only — no technical claims are drawn from them. All routed pages
are listed with read levels in the corpus section of
[`references/source-index.md`](references/source-index.md).

**What this corpus uniquely contributes.** Blind XSS surfacing through logged
request metadata (login-attempt logs, User-Agent-on-upload), the hidden
store-time-parameter technique, six filter-reconnaissance probes with a
reflection-shape→response mapping, three-account comment-splitting for length-limited
stored fields, and a worked upload-filter decision flow — all post-2017 and largely
absent from the 2017-frozen archive. Caveat: these were practice-event labs on
deliberately vulnerable clones of real program patterns, so severities are the event
organiser's judgement, not production-program outcomes; the playbook uses them as
methodology anchors for that reason.

## Methodology

1. **Archive inspection.** Fetched the archive index and parsed all 4,419 rows into a
   structured dataset (team, bounty, title, report URL). Confirmed that the archive's
   per-program pages carry **only** `Team | Bounty | Title` plus a link — no report
   bodies.
2. **Candidate identification.** Matched XSS search terms across all titles (reflected,
   stored, DOM, self, attribute/JS/URL context, encoding, double-encoding, filter
   bypass, SVG/file, template injection). 910 candidates.
3. **Authoritative retrieval.** For each candidate, retrieved the public, unauthenticated
   HackerOne report endpoint to obtain program, weakness, severity, bounty, dates,
   structured scope, official disclosure summary, and — where published — the full
   researcher report body.
4. **Curation.** Excluded 348 candidates whose HackerOne weakness field was a non-XSS
   class. Retained the rest regardless of how weak the title was, because the retrieved
   weakness field is more reliable than the title.
5. **Classification.** Backbone = HackerOne's authoritative weakness field
   (Reflected / Stored / DOM). The `Generic` bucket was then sub-classified by evidence
   in titles and report bodies into context, self, SVG/file, framework/template,
   extension/messaging, HTML injection, and filter-bypass groups.
6. **Consolidation.** Sources sharing a root cause were merged into one playbook with an
   individual case-study subsection each, retaining separate rows and separate citations
   in the source index.
7. **Authoring.** Playbooks were written from retrieved evidence. Methodology sections
   are labelled as general; case-study sections contain only sourced facts.
8. **Second-corpus extension (2026-10-17).** Fetched all 26 BugBountyHunter.com
   content pages, enumerated the three FirstBlood hackevent listing pages, then
   fetched and parsed each of the 207 XSS-typed reports into
   [`references/firstblood-index.md`](references/firstblood-index.md). Read-level
   honesty applies (full vs core-section vs skimmed) and is recorded per page in the
   corpus section of `references/source-index.md`.

**Access and rate discipline.** `robots.txt` was checked (absent — GitHub Pages 404).
Requests were made at ~1.2 s intervals with 4xx responses not retried, and every fetched
page was cached to disk so the sweep was resumable. No authentication was used, no
access control was bypassed, and only public endpoints were read. For the
BugBountyHunter corpus, robots.txt explicitly allows the fetched paths; the same
interval and cache discipline was applied there.

## Known source limitations

1. **The archive is frozen at 12 September 2017.** Every source predates the removal of
   Flash, the mainstreaming of strict CSP, and all modern XSS sinks. Modern
   exploitability of any case here has **not** been re-tested and must not be assumed.
   The BugBountyHunter corpus (added 2026-10-17) covers 2021-2023 behaviour, but it
   comes from deliberately vulnerable practice labs, so its Hulu-style flows mirror
   real programs without being production programs — treat its payloads as
   methodology anchors, not proof of exploitability against any real target.
2. **No report bodies for 103 sources.** HackerOne withheld the original text and
   published only the team's disclosure summary. Those sections state the summary and
   mark everything else as undisclosed.
3. **299 XSS-titled entries are gone entirely.** No metadata could be retrieved. Several
   are titled as reflected XSS and would likely strengthen the playbooks.
4. **Self-reported severities are not comparable.** The archive mixes HackerOne severity
   ratings, CVSS vectors, and raw bounty figures across programs with different policies
   and eras. No cross-program severity comparison is supportable and none is attempted.
5. **Classification of the `Generic` bucket is inferential.** No program published a
   per-context taxonomy, so the sub-classification in
   [`Context-Based-XSS.md`](Context-Based-XSS.md) was derived from titles and bodies.
6. **Several sources are truncated in the archive itself.** `CONT-185`'s summary ends
   mid-sentence at *"but cannot really…"*.
7. **Historical payloads should not be replayed.** Payloads in §11 of each playbook are
   reproduced verbatim for analysis, clearly marked, and are unsuitable for use against
   current targets. Newly authored illustrations are marked as such in every file.
8. **Payloads are evidence, not guidance.** No file here should be read as a
   ready-to-deploy attack resource; the `CONT-129` `.tar.gz` construction and the
   `FRAM-001` sandbox escape are retained solely to document what was reported.

## Research gaps

Ordered by likely value.

1. **No Server-Side Template Injection playbook — the largest gap.** The archive contains
   SSTI reports (Flask/Jinja2, Smarty) that reach **server-side code execution**. Those
   are outside an XSS knowledge base by the merge rule, and they need their own file.
2. **`REFL-082` (Rockstar double-encoding) body withheld.** Its decode sequence is
   labelled a hypothesis in [`Reflected-XSS.md`](Reflected-XSS.md) §2.3 and §14. This is
   the single highest-value missing document for the encoding playbook.
3. **`STOR-142`'s endpoint is undisclosed.** The filter defect is documented precisely;
   the location is not, so a targeted regression test cannot be built from it.
4. **Only 4 framework/template sources.** HackerOne has no template-injection-XSS
   category, so these are scattered in `Generic`. A sweep of report bodies for `{{`,
   `${`, `{%`, `{#` would likely double the evidence base.
5. **No post-2017 evidence whatsoever.** Modern DOM sinks, Trusted Types, MV3
   extensions, SSR framework injection, and mXSS are entirely uncovered.
6. **Unicode/filter soundness is unexamined.** Only two sources document normalisation
   behaviour. Whether a filter over NFC/NFKC/NFD can be relied on is unanswered.
7. **Origin-isolation claims are unverified.** Several reports assert a file subdomain is
   a "sandbox"; none tested whether cookies, storage, or service workers were reachable.
8. **Email and export sinks are barely mined.** One archived source
   ([`HTML-001`](HTML-Injection.md)) covers a phishing-grade HTML injection into an
   email sent from the target's own domain — a small, high-yield surface worth
   original research.
9. **`DOM-018`'s clone-able object shape is undocumented** in the accessible source,
   leaving the `postMessage` shape-bypass probe conceptual rather than concrete.

## Traceability

Every case study carries a report URL. The full chain:

```
h1.security.nathan.sx  →  per-program archive page  →  hackerone.com/reports/<id>
                                                          ↓
                                        source-index.md  →  Case ID  →  playbook §11
```

- [`references/source-index.md`](references/source-index.md) — 562 rows, each with case
  ID, original title, report URL, archive URL, program, date, category, evidence
  quality, destination playbook, and limitations.
- Each playbook's §11 uses stable **Case IDs** (`REFL-082`, `STOR-142`, …) that match
  the source index exactly.
- Facts not present in a retrieved source are written as *"Not disclosed in the source."*
  Hypotheses are explicitly labelled as such.


<!-- CASESTOCK-LINK:BEGIN -->

## Case stock — vault (`_VAULT/`)

**2,528 disclosed reports** routed to this category · 539 with a bounty figure · **$540,043** · 1,438 full write-ups stored locally.

- Full list: [`_VAULT/by-vault-category/XSS.md`](../_VAULT/by-vault-category/XSS.md)
- Query: `sqlite3 ../_VAULT/reports.sqlite "SELECT id,bounty,title FROM reports WHERE ..."`
- Pull one write-up: `python3 ../_VAULT/scripts/extract_report.py <id>`

| Top paid | Program | Bounty |
|---|---|---|
| [1212067](https://hackerone.com/reports/1212067) Stored XSS in markdown via the DesignReferenceFilter  | GitLab | $16,000 |
| [1578400](https://hackerone.com/reports/1578400) New /add_contacts /remove_contacts quick commands susseptible to XSS from Custom | GitLab | $13,950 |
| [1731349](https://hackerone.com/reports/1731349) Stored XSS via Kroki diagram | GitLab | $13,950 |
| [1444682](https://hackerone.com/reports/1444682) XSS at jamfpro.shopifycloud.com | Shopify | $9,400 |
| [131450](https://hackerone.com/reports/131450) Stored XSS in developer.uber.com | Uber | $7,500 |

_refreshed 2026-11-17 from the public HackerOne disclosed-report dataset_
<!-- CASESTOCK-LINK:END -->
