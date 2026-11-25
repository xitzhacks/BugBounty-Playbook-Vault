---
title: "SSRF Testing Playbook — Agent Execution Protocol"
type: agent-playbook
category: ssrf
cwe: "CWE-918"
sources: "h1.security.nathan.sx archive (4,419 rows, frozen 2017-09-12) — 2 discovery nets → 82 SSRF-titled candidates → 58 retrievable → 45 full bodies read"
evidence_line: "26 body-confirmed SSRF cases + 3 body-confirmed SSRF-adjacent internal-service cases + 8 metadata-level SSRF rows + 18 confirmed-not-SSRF exclusions + 24 reports now HTTP 404 (recorded)"
programs_covered: "Phabricator, Imgur, Slack, Shopify, Nextcloud, APITest.IO, Mixmax, Instacart, WordPress/Automattic, Twitter, RelateIQ, Factlink, Discourse; GitLab / HackerOne rows appear only as non-SSRF exclusions; libcurl/php advisories entered as adjacent metadata rows"
archive_accessed: "2026-10-24"
---

# SSRF Testing Playbook — Agent Execution Protocol

## 0. How to Use This Document

A deterministic pass through **Gate 0 (scope)** → **Phase 1 (sink inventory)** →
**Phase 2 (validation baseline)** → **Phase 3 (Route R1: the SSRF ladder)** →
**Phase 4 (calibration discipline)** → **Gate 3 (validation)** → **Phases 5–7
(severity, report, remediation)** → **Gate 5 (post-reporting hygiene)**, with the
case evidence of this vault as anchors at each step.

The agent reading this must be able to reproduce the era evidence:

- Category files (source quotes, anatomy tables): `Cloud-Instance-Metadata.md`,
  `Port-Scan-and-Internal-Mapping.md`, `Validation-Bypass-and-Scheme-Abuse.md`,
  `Media-Processing-SSRF.md`, `Blind-SSRF-and-Callback.md`,
  `Internal-Service-Exposure.md`.
- Source-index: `references/source-index.md` (per-case fetch disposition table,
  exclusions, 404 roster).

Standing discipline inherited from the other vaults of this repository:

1. Quotes are verbatim from report bodies read in full; `(sic)` marks odd original
   wording; any inference outside the source is labelled (modern-knowledge labels
   say so explicitly).
2. **Severity/labels are historical.** Archive-era weakness labels misname their
   own bugs (`SRF-14127` "Command Injection - Generic" is a scheme-wrapper escape;
   `SRF-110801` "Cross-Site Request Forgery (CSRF)" is an SSRF; `SRF-91816` CSRF
   label, SSRF body). The *body* is the class authority. Use labels as
   provenance, never as attestation.
3. Case IDs: `SRF-<report id>` (e.g. `SRF-53088`) as tabulated in
   `references/source-index.md`.
4. The category files separate corpus-evidenced technique from post-archive
   modern layer; an agent never fuses the two in one sentence.
5. An agent never touches a sink class whose feature is absent on the target:
   mark "not applicable — no such sink observed" instead of inventing parameters.

## Phase 0 — Intake and Scope Validation `GATE 0`

Inputs: target domain(s), written scope. Before any request:

1. Confirm the engagement records authorization for:
   a. URL-fetching tests that cause the *server* to make outbound connections
      (the SSRF contract), including loopback/CONFIG-limited internal probing;
   b. YES/NO for cloud instance metadata probing (`169.254.169.254` family);
   c. YES/NO for file-read chains via media parsers (Media-Processing file);
   d. YES/NO for third-party weaponization (pingback/telemetry) — most scopes
      deny this; default = NOT APPROVED.
2. Write the approved probe list to the session log before contacting anything.
3. A silent scope is a NO for (b), (c), (d): record "not approved by scope —
   not attempted". This vault's era cases (SRF-53088 metadata; SRF-237381
   file-read) show why these stay scope-gated.
4. Note contact-rate constraints (target policy, cloud-provider policy in
   modern engagements, and the archive's own warning that monitored test
   surfaces blacklisted a probing IP mid-session in SRF-128685).

Gate 0 exit: written authorization exists for the whole probe list.

## Phase 1 — Attack Surface Mapping `GATE 1`

SSRF is *sink-first* hunting. Build the sink inventory before touching anything:
the corpus's anchors live in features that accept a URL — not in a magic payload.

### Sink classes S1–S10 with their evidence anchors

| ID | Sink class | Probe concept | Corpus anchors |
| --- | --- | --- | --- |
| S1 | image / resource from URL in editors and pickers | URL → server fetch → render result | SRF-67377, SRF-67389, SRF-158016, SRF-228377 |
| S2 | webhook URL settings (account/project integrations) | save + trigger; watch its notifications | SRF-243277 |
| S3 | integration / connector / command URLs (slash-command style) | edit integration, supply URL, execute | SRF-61312, SRF-14127 |
| S4 | media conversion (video→gif, thumbnails, HLS processing) | feed converter fields / crafted media | SRF-115857, SRF-115978, SRF-237381 |
| S5 | URL validators / embed previews / card renderers | the validator UI is your readout | SRF-178184, SRF-49474, SRF-110801 (CSRF delivery leg) |
| S6 | custom "server" fields (registration, SSO/mail config) | supply host, read the connect outcome | SRF-16571, SRF-222667 |
| S7 | URL proxy / fetch-by-URL / shortener services | shortened entry → internal fetch | SRF-1409 |
| S8 | CDN resize / media transform fetches | transform params + redirect leg | SRF-204513 |
| S9 | pingback / link-notification handlers (scope-gated) | third-party fetch — verify scope | SRF-124097 |
| S10 | by-form media (career/contact form content rendered server-side) | inject `<img src=…>` | SRF-236301, SRF-197365 (metadata-only anchor) |

Procedure:

1. Walk the product surface (maps, JS, docs, settings): list *every* input that
   takes a URL; annotate trigger privilege (anonymous user? any user? admin?).
2. For each sink, record: who can trigger it, what result it shows, whether the
   fetch is synchronous, whether failure produces a user-visible signal
   (webhook failure email in SRF-243277), and whether content is returned.
3. Classify each sink into one of three channels — **read-back** (content or
   parsed features returned), **band/oracle** (differential status/error/timing),
   **blind** (callback or side-effect only). This is the routing input for
   Phase 3 rungs.
4. If no URL-taking input exists on the entire product, record that and stop —
   there is no SSRF surface to test.

Gate 1 exit: sink inventory table complete with channel classification.

## Phase 2 — Validation Baseline (no internal probing yet)

For each in-scope sink:

1. Record **legitimate control traffic**: a normal external URL the target
   fetches on your behalf (webhook to your own listener, image by URL from your
   own host). Keep the listener transcript as the baseline event.
2. Map the validation profile: scheme-swap (`http` vs `https`), port-swap
   (80/443 vs 8080/6379/25), hostname notations (`0x7f.1`-style hex shorthand
   trailing SRF-128685, `0.0.0.0`, `localhost`, IPv6 brackets), and length edge
   edges. Note the exact error per probe.
3. Decide the channel per sink from those errors, using the §1 channel table of
   `Port-Scan-and-Internal-Mapping.md`.

## Phase 3 — Route R1: the SSRF Ladder

One route, nine rungs, each rung's evidence anchored in the corpus. A rung is
never entered before its prerequisite rung produced evidence on the same sink.

- **Rung 1 — Reach**: prove the server made the request. Pattern (a) band
  difference Per sink's channel (Port-Scan §2), pattern (b) listener hit with
  IP+UA log (Blind B1). Anchor: SRF-236301, SRF-178184.
- **Rung 2 — Scheme inventory**: wrapper probes per Validation-Bypass V1 —
  verify the CLIENT's fingerprint (`CLIENT libcurl 7.22.0` era-quotes;
  SRF-14127 / SRF-115748). No wrapper claim without inbound transcript.
- **Rung 3 — Notation gaps**: IPv6 bracket, hex shorthand, decimal variants —
  each change confirmed by body first (SRF-61312's `[::]` + SRF-128685's
  `0x7f.1`). No host/notation abbreviation from memory.
- **Rung 4 — Redirect-relayed second leg**: attacker redirect chain —
  gopher/`ftp`/userinfo-credentials legs with second-leg transcripts
  (SRF-115748/228377/204513).
- **Rung 5 — Port-state differencing**: calibrate on known-open/known-closed
  external control pair (SRF-67389's `scanme.nmap.org:1` vs `:22`), then
  behavior the scan into internal space *within scope* (SRF-16571's localhost
  list, SRF-145524's port 80/8080 readback).
- **Rung 6 — Loopback/internal services**: process readback only — Zookeeper
  `dump` / `envi` / `stat` / `ruok` per SRF-154369, Splunk / CouchDB-level
  read-only checks (Internal-Service-Exposure I1).
- **Rung 7 — Cloud metadata**: address + path table (Cloud-Metadata M1),
  with IMDS-token modernization note in every claim.
- **Rung 8 — Enumerated deeper reads**: metadata subtree enumeration
  (Cloud-Metadata M2) or media pipeline file-read chains (Media-Processing F1)
  — explicit authorization required; no defaults.
- **Rung 9 — Third-party weaponization**: pingback/proxy-out abuse attempts —
  scope-approved only; most commonly recorded as "not approved" (Blind B3).

## Phase 4 — Calibration discipline (in-session rules)

1. **Controls first**: known-open and known-closed external bands recorded
   before internal probes (SRF-67389's pattern).
2. **Band naming**: one band per band, exact output strings preserved verbatim
   (SRF-178184's "ERROR: Fetching the page failed because other errors."
   appears verbatim — reproduce, never paraphrase it as "port closed").
3. **Cache management**: use a request-variant parameter per attempt to avoid
   stacked caches (SRF-204513's "bump n+1 on resize param or add a new param")
   and record each variant used.
4. **Attribution discipline**: name the fetcher in every claim. UA + IP whois
   before asserting origin — intermediaries (SRF-236301's "(via ggpht.com
   GoogleImageProxy)") do not show the target's network.
5. **No parallel-barrage**: linear spacing of probes per target sink rate-limit
   respect (the SRF-128685 shortfall is the archive's warning itself).

## Phase 5 — Validation and Triage `GATE 3`

Before anything reaches the report, all claims carry their gate:

1. **OOB or it didn't happen** — listener hit, notification asymmetry, or full
   readback is the floor; silence + "libcurl supports it" is hypothesis, not a
   report. (Blind file gates)
2. **Two-band rule** — both open and closed bands shown for port-state claims.
3. **Attribution rule** — fetcher named with UA/IP evidence; intermediary
   requests, if they are present, change the claim wording.
4. **Scheme-claim receipt rule** — every wrapper claim's inbound records
   (Headers/HANDSHAKE output) are attached (Validation-Bypass §5).
5. **IMDS-modern check rule** — metadata claims determine whether the current
   token requirement exists; write "unverified against modern token-mode
   server settings" if undetermined; never conflate with the era's `GET`-only.
6. **Metadata-only honesty** — rows known by title/label are labelled
   `evidence level: metadata` each time they are cited (full list in
   `references/source-index.md`).
7. **No paraphrasing up** — impact statements copy the observed level.
   SRF-91816's "it may also be possible…" wording is speculation per its own
   writing — cite it as speculation, not proof.

## Phase 6 — Severity Determination

1. Order the impact ladder per the era's *recorded* payouts and their
   modernization direction: metadata-credential readback > internal-service
   interaction > wrapper/scheme matrix > internal-port mapping > external
   proxying.
   Recorded on the confirmed set: `SRF-115748 $2,000` (wrapper matrix, era
   largest), `SRF-91816 $1,600`, `SRF-115978 $1,000`, `SRF-67377 $500` /
   `SRF-67389 $500` / `SRF-14127 $300` (archive-stated side), `SRF-53088 $300`
   (JSON-verified: metadata service reachable), `SRF-178184 $280`,
   `SRF-204513 $350`, `SRF-115857 $800` / `SRF-237381 $800` (file-read
   pipelines), `SRF-16571 $250` / `SRF-110801 $250`, `SRF-228377 $64`
   (JSON-verified), `SRF-158016 $50` (JSON-verified). Amounts labeled
   "archive-stated" come from the archive bounty table only.
2. Modernization ceiling: the corpus cannot state modern cloud values — apps
   running cross-cloud internal estates must be re-weighed by the reporting
   program: *who owns the data behind the fetched address*, not which library
   accepted the scheme.
3. Twists: third-party weaponization (SRF-124097) is typically moderated
   relative to target-own impact — era label "Uncontrolled Resource
   Consumption" is treated historical.

## Phase 7 — Reporting

Per-target reporting structure (adapt in-casing to program format):

1. **Observations** — one line per rung with its band evidence.
2. **Description** — sink inventory slot, exact URL/shape, which leg fetched,
   fetch-side attribution.
3. **Impact** — per-level anchored; distinct line for *what level of read*
   (banner/status readback vs metadata listing vs user-data file bytes).
4. **Verification** — transcript/screenshot and the two-band table.
5. **Remediation** — from the corpus fix lines plus a separate "post-archive
   modern layer" paragraph (egress control at the fetch node; pinned client
   schemes; redirect leg parsing — labeled as modern additions).
6. Era mention of the 404-era reports (source-index roster) as historical
   context only — "fixed/behaviour since, unknown".

## Phase 8 — Remediation anchors

From era sources (quote the exact line in the report):

- SRF-14127: "…with NOT port whitelist and with NOT disabled wrappers" — the
  anti-pattern phrase for missing allowlists.
- SRF-50537 (full list): deny local/private ranges, deny uncommon ports, rate
  limit, don't follow redirects to localhost/LAN "either via HTTP redirects, or
  DNS records."
- SRF-204513: manual one-request-at-a-time redirect parsing; enable certificate
  validation post-era (the era's `CURLOPT_SSL_VERIFYPEER` statement).
- SRF-1409: "once your proxy is also able to follow redirects, it should reject
  redirects to internal hosts as well."
- SRF-110801: POST-method scan URLs with token, and "the address 0.0.0.0 should
  not be allowd for scanning/scraping."
- SRF-243277: "Blacklist the AWS metadata url and any other sensitive internal
  urls." — era answer; the *modern layer* note goes separately (network-layer
  denial of metadata ranges, token-required flagging).

## Phase 9 — Post-Reporting `GATE 5`

1. Evidence hygiene: redact your own listener addresses proportionate to what
   they reveal; do not paste raw credentials that file-read chains returned
   (redact per the vault suite's evidence-hygiene discipline).
2. Clean up probes: delete webhooks/entries created for tests; explain what was
   removed in your closing note (mirrors the era phenomena of monitored test
   blacklists seen in SRF-128685).
3. Log dispositions per sink in the target notes (sink ID, rung reached, band
   evidence, era anchors used) — mirrors this repo's `source-index` structure.
4. Archive this vault's links in the useful citations list of your final report.

## Appendix A — Category files and their anchors

| File | Anchored era cases | What it proves |
| --- | --- | --- |
| Cloud-Instance-Metadata.md | SRF-53088, SRF-128685, SRF-243277 | metadata reach, listings, blind-oracle path enumeration |
| Port-Scan-and-Internal-Mapping.md | SRF-16571, SRF-178184, SRF-50537, SRF-67377, SRF-67389, SRF-145524, SRF-213358, SRF-222667, SRF-158016, SRF-1409, SRF-110801, SRF-49474 | per-band channel table; calibration-first method |
| Validation-Bypass-and-Scheme-Abuse.md | SRF-14127, SRF-115748, SRF-61312, SRF-204513, SRF-228377, SRF-91816 | wrapper/redirect/notation gate escapes |
| Media-Processing-SSRF.md | SRF-115857, SRF-115978, SRF-237381 (+404-era family) | playlist/parser-initiated SSRF + file-read chains |
| Blind-SSRF-and-Callback.md | SRF-236301, SRF-243277 (xref), SRF-124097, SRF-197365 (metadata) | callback/black-effect oracles; weaponization scope rules |
| Internal-Service-Exposure.md | SRF-73567, SRF-154369, SRF-158118 + 3 metadata rows | the targets an SSRF aims at; payout frame (era) |

## Appendix B — One-Page Run Card

```
GATE 0    approvals (metadata Y/N, file-read Y/N, third-party Y/N)
Phase 1   sink inventory S1..S10, channel per sink (read/band/blind)
Phase 2   validation baseline (no internal probes before bands recorded)
Route R1  ladder rungs 1..9, per-rung gate in category files
Phase 4   calibration: controls first, exact bands, rate respect
GATE 3    OOB floor, two-band rule, attribution rule, scheme receipts,
          IMDS modernization, metadata-only honesty, no paraphrasing up
Phase 7   report: rung lines, exact transcripts, both bands, anchored impact
Phase 8   remediation quotes from corpus + separated modern notes
GATE 5    delete probes, redact, disposition log in session notes
```

## Appendix C — Evidence base and its limits

1. All cases are 2013–2017 era disclosed reports mirrored from a frozen 2017
   archive snapshot. Library versions, defaults (e.g. Zookeeper 3.5.1-alpha),
   and the internal estate described are *of that time*.
2. Bounty amounts cited are as recorded on the reports; no era-average can be
   inferred from one corpus.
3. 24 candidate reports, including well-known titles (newrelic
   `SSRF in alerts.newrelic.com exposes entire internal network`, mail.ru family,
   Yahoo `view-source:...XSPA/SSRF`), are now HTTP 404 on the origin — era-known
   titles recorded in `references/source-index.md`, no content claims possible.
4. 18 candidate reports the vault excluded after body-read as not SSRF
   (XSS/IDOR/DoS/RCE/library advisories classes) — recorded with reasons in
   `references/source-index.md` so no future re-classification substitutes.
5. Metadata-only rows (no body) are always cited with that provenance; no
   technical claims rest on them beyond title/label/bounty.
6. The era's external methodology set — XSPA taxonomy (2012), the Acunetix primer
   (2013), the **"SSRF bible. Cheatsheet"** rev 1.03 (2017, scheme matrix + exploit
   catalog + DNS-pinning race), the FFmpeg family root source and its oss-security
   CVE record — is recovered and quoted in
   [`references/blogs-index.md`](references/blogs-index.md). When a sink class here
   needs a payload craft that the corpus cases don't show in full, the bible's
   catalog and the Habr/YUV4MPEG2 workflow are the era-authenticated fallbacks.
