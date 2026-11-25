---
title: "SQLI-Testing-Agent-Playbook — an executable procedure for any target"
type: agent-playbook
category: cross-category
cwe: "CWE-89"
corpus: "HackerOne disclosed reports, 2014–2022 era, list seeded from github.com/shreyaschavhan/h1-reports-for-reference TOPSQLI.md — 247 rows; 151 retrievable; 100 full bodies classified in this vault"
list_accessed: "2026-10-25"
note: "This file is the operating layer: it sequences the six category playbooks into an agent-executable procedure and binds every step to the case that proves it. Case-ID scheme: SQL-<report id>."
---

# SQLI-Testing-Agent-Playbook — an executable procedure for any target

## 0. Purpose and boundary

This playbook turns the vault's five technique playbooks (`Time-Based-Blind.md`,
`Boolean-and-Content-Oracle.md`, `Error-and-Union-Output.md`,
`Out-of-Band-Callback.md`, `Library-and-Framework-SQLi.md`) plus the escalation
file (`SQLi-to-RCE-Chains.md`) into a linear procedure an agent can execute
against any target whose bug-bounty scope authorizes SQL-injection testing.

Hard boundaries the corpus itself demonstrates (do not violate them even when
the technique would work):

- **No authentication bypass to reach injectors.** Cases that *found* their
  surface while logged in named the authorization level in the report
  (`SQL-59664`'s "authenticated users with privileges to edit page
  permissions" pattern — see `Library-and-Framework-SQLi.md` §3.2). Testing
  through accounts the program grants is fine; breaking login to reach more
  surface is not.
- **Extraction ceiling = scalar proofs unless scope says otherwise.** The
  corpus's own strongest reports stop at banners, counts, and single
  characters (`Time-Based-Blind.md` §6, `Boolean-and-Content-Oracle.md` §8).
- **Write-side and chain techniques are gated** on explicit program
  authorization (`Boolean-and-Content-Oracle.md` §8 gate 3;
  `SQLi-to-RCE-Chains.md` §8).
- **Rate discipline is a class invariant, not a courtesy** — one confirmed
  case *lost its test window* to target-side throttling
  (`Library-and-Framework-SQLi.md` §3.7's 503 note), and the remediation
  sections argue rate-limiting as the mitigation
  (`Time-Based-Blind.md` §10).

## 1. Phase P0 — inventory and carrier map

**Goal**: a list of *candidate injectors* (carrier, request shape) before any
payload is sent.

1. **Enumerate carriers** with the corpus's proven list, in hit-frequency
   order:
   - form/POST params, JSON body fields (incl. JSON inside query strings —
     SQL-1044698's `acctid` inside a JSON payload sent as a parameter),
   - GraphQL arguments (SQL-435066's `embedded_submission_form_uuid`),
   - admin/list surfaces: search boxes, sort fields, sort *direction* fields,
     filters, paging (`LIMIT`/`OFFSET`) parameters,
   - URI path segments that reach a query (SQL-319279's CSV route,
     SQL-1107536, SQL-374027's `/plugin/tag/…`),
   - HTTP headers: User-Agent (SQL-297478, SQL-771215), Referer
     (SQL-723044, SQL-1018621), cookies (SQL-761304),
   - base64/encoded envelopes: decode and re-treat inner fields as carriers
     (SQL-150156 workflow),
   - third-party surfaces the target loads (SQL-433792's analytics pixel),
   - mobile content providers if a platform target exists
     (`Library-and-Framework-SQLi.md` §4).
2. **Fingerprint the builder layer before touching the target's own code**:
   JS bundles, error pages, and response shapes leak the ORM/query-builder in
   use; map each carrier to the *position* it lands in (WHERE value? key
   name? ORDER BY? LIMIT? table/field name? INSERT VALUES?). Use
   `Library-and-Framework-SQLi.md` §5's position table as the template.
3. **Record the DBMS hypothesis channels** you already have (headers like
   `X-Powered-By`, error-page shapes, driver names in bundles) but do not
   trust them — the corpus shows body-internal DBMS mistakes
   (`Error-and-Union-Output.md` §4's MySQL/MSSQL drift note).

**Output**: carrier table `{request, parameter, position, auth-level}`.

## 2. Phase P1 — detection, cheapest first, one carrier at a time

Run this fixed order per carrier (each step's full evidence shapes live in the
cited playbook):

| # | Probe | Evidence expected | Authority |
|---|---|---|---|
| 1 | Quote pair: `'` vs `''` (and dereference diff) | syntax error names dialect; error gone on balance | `Error-and-Union-Output.md` §2 (SQL-519631 seven-step transcript; SQL-761304 pair) |
| 2 | Type mismatch: `1'=1` / `1''=1` (Oracle); numeric-vs-string flips | dialect announce (`ORA-01722`, `SqlException`, `You have an error in your SQL syntax`) | same §2 |
| 3 | Arithmetic boolean (no quotes): `OR 3*2=6 AND <const>=<const>` pairs | TRUE/FALSE band difference | `Boolean-and-Content-Oracle.md` §2.5 (SQL-1102591, SQL-1250293) |
| 4 | Condition pair: `AND 1=1` / `AND 1=0` | any band (status, content, redirect, JSON field) | `Boolean-and-Content-Oracle.md` §2 |
| 5 | Delay series: `sleep(0)/sleep(S)/sleep(2S)` (+ arithmetic forms `sleep(5*5)`, `sleep(5*5*0)`, `sleep(6*6-30)`) | monotone clock band | `Time-Based-Blind.md` §2 |
| 6 | Per-DBMS delay call conforming to dialect fingerprint | confirms engine (`WAITFOR DELAY`, `pg_sleep`, `BENCHMARK`, Oracle heavy query) | `Time-Based-Blind.md` §3 |
| 7 | Pollution/order-position probes for `ORDER BY`/`LIMIT`/`OFFSET` positions found in P0 | construct-query output or row-order diff | `Library-and-Framework-SQLi.md` §5, `Boolean-and-Content-Oracle.md` §3 |

**Stop rules baked into P1** (all corpus-native):

- If step 1–2 announce a dialect but the target exposes a WAF/IPS and the
  program's tooling rules are unclear — *stop and file the detection*
  (SQL-447742's exit, `Error-and-Union-Output.md` §2).
- If step 5 shows a delay band but the site's *baseline* overhead is
  sub-second-noisy, re-run the whole series with interleaved zeros before
  claiming (`Time-Based-Blind.md` §9 gates).
- If a carrier produces *no* band change in steps 3–5, downgrade expectation
  to "may still be injectable at a position step 7 covers" — ordering
  oracles and position injections produce no band on the main response
  (SQL-298176, SQL-273946).
- If OOB is the only remaining channel, fingerprint DBMS as MSSQL before
  attempting callback payloads (`Out-of-Band-Callback.md` §4 step 1).

## 3. Phase P2 — classify and descend the oracle ladder

Decision tree (each leaf = the playbook that owns extraction):

```
Band observable in response body/status/redirect/JSON?
├─ yes → Boolean-and-Content-Oracle.md   (band pair → known-value calibration
│                                         → length() → substr ladder)
└─ no
   ├─ Clock band observable?  → Time-Based-Blind.md
   │                           (series → multiplier calibration → per-DBMS call)
   ├─ Error text reachable and value-carrying?
   │    → Error-and-Union-Output.md    (updatexml/extractvalue/cast-echo/
   │                                     CELLSPRINT/union)
   ├─ MSSQL + no output channel at all?
   │    → Out-of-Band-Callback.md      (xp_dirtree callback; listener first)
   └─ Query rendered in row order / sort?  → ordering oracle
        (Boolean-and-Content-Oracle.md §3; SQL-273946, SQL-298176)
```

If *everything* fails but a library layer is in play, switch targets: the bug
may be in the builder, not the app (`Library-and-Framework-SQLi.md` §2 —
eight of that file's cases demonstrate on local installs, no victim site
needed; *"Observed constructed SQL queries"* is accepted evidence there).

## 4. Phase P3 — calibrated extraction (only after classification)

Ladder, in corpus order:

1. **Calibrate**: baseline latency (record it), response multiplier
   (`sleep(1)` ≠ 1 s ⇒ scale factor; SQL-488795's ×5 discovery), band
   deltas, oracle noise floor.
2. **Length first**: `length(database())`, `count(*)` bisections
   (SQL-648346's `length(database())=39`; SQL-982202's count bisect).
3. **Character/position next**: `substr(...,i,1)='c'` ladders
   (SQL-648346, SQL-117073, SQL-150156's script, SQL-1130874's `$where`
   regex loop) — one bit/character per request, never bulk.
4. **In-band shortcuts when available**: error-carried values
   (`updatexml concat`, `cast as date` echo, `CELLSPRINT` render,
   union banner) — one request per datum instead of per character
   (`Error-and-Union-Output.md` §3–4).
5. **Stop at the scalar ceiling** unless program scope explicitly authorizes
   deeper; prefer *own-record* extraction for any user-bound datum
   (SQL-298176 demonstrates with the author's own email).

## 5. Phase P4 — escalation decisions (gated)

Only with explicit authorization gates from the program:

- **Write-side proof** — the `Boolean-and-Content-Oracle.md` §2.5 shape:
  pre-create record → verify band on it → single-field write → post-verify
  (SQL-1044716's PUT sequence).
- **ATO chain** — token/2FA-secret leak via blind oracle → takeover →
  transient (restore-on-done, per SQL-1130874) → shell-class proof only via
  *demo instance you built* (`SQLi-to-RCE-Chains.md` §4/§5's Docker
  reconstruction).
- **Framework gadget chains** — only after inventorying the trusted
  far side (`SQLi-to-RCE-Chains.md` §6: session serializers, pickles,
  webhook script features).
- **Dependency rows** — if the reachable surface is a *framework/layer* bug,
  map component → known advisory → reproduce locally
  (`Library-and-Framework-SQLi.md` §6 step 7).

## 6. Phase P5 — report assembly (the corpus's ledger contract)

Every claim ships with, in this structure (all five sentences classes are
verbatim from the corpus):

1. **Carrier**: exact request (headers/params/path). The corpus prints full
   requests even for form-data carriers (`Out-of-Band-Callback.md` §2.2's
   multipart; `Time-Based-Blind.md` §2's raw series table).
2. **Band/oracle evidence**: paired payloads with their observed responses —
   never single screenshots (`Boolean-and-Content-Oracle.md` §9 gate 2).
3. **Series/repeatability transcripts** for time claims
   (`Time-Based-Blind.md` §9 gate 2).
4. **The ledger sentence**: what was *read*, exactly
   (SQL-982202: *"I have not exfiltrated any data with the exception of column names, the table name and the fact that there are 26 user accounts in this service."* —
   copy this shape).
5. **The scope sentence**: what was *not* done and why
   (SQL-923020: *"I only explored nonsensitive information."*; SQL-484801:
   *"I did not begin to extract any data about the server or database, since this may be contrary to the rules."*).
6. **Conditional claims labeled conditional** (SQL-361341's opening
   paragraph is the template — `SQLi-to-RCE-Chains.md` §3).
7. **Regression check before filing**: search whether the sink family had an
   earlier disclosed report on this target; if yes, note lineage
   (`Time-Based-Blind.md` §7 — five corpus cases are regressions).

## 7. Calibration constants (corpus-measured defaults)

- **Baseline overhead**: 0.25–0.9 s on ordinary targets of the era
  (`Time-Based-Blind.md` §2's zero-baselines) — require ≥3× baseline delta
  for sub-second claims.
- **Statement multipliers**: ×1 (most), ×5 observed (SQL-488795) — always
  measure, never assume. That case's own series, verbatim:
  *"By issuing sleep(0) response will be delayed to 0 seconds."* /
  *"By issuing sleep(1) response will be delayed to 5 seconds."* /
  *"By issuing sleep(5) response will be delayed to 25 seconds."* — followed by
  the analyst's conclusion:
  *"Apparently, SQL statement is executing 5 times on the database side, because response time always 5 times bigger than supplied sleep value."*
- **Delay values used in the corpus**: 1–32 s; smallest *proven-sufficient*
  demonstration series in the corpus used 0/3/6/9 with ~6.27 s observed at
  `sleep(6)` (SQL-374027).
- **Character-set floors**: SQL-150156's `string.digits + '_-@.'` seed plus
  letters — when extracting usernames/hosts.
- **Oracle response contract** (NoSQL): policy-on-true / error-on-false
  (SQL-1130721) and record-present / empty (SQL-1130874) — mirror these
  shapes for Mongo-targeted work.

## 8. Modernization notes (what the era corpus still teaches in 2026)

- **Still-current mechanics**: blind oracles, SHALL-order extraction ladders,
  position-family injections (sorting/paging remain nearly everywhere),
  operator injection in JSON APIs (GraphQL `$regex`/`$where` shapes in
  `SQLi-to-RCE-Chains.md` §4–§5), prototype-pollution→SQLi transfer
  (`Library-and-Framework-SQLi.md` §2.7), dependency-version rows.
- **Changed**: quote-eliminating magic quotes regimes (PHP ≤5.x) are gone,
  but plugin-ecosystem *reset* behaviors survive elsewhere — audit guards as
  *conditions*, not guarantees (`Error-and-Union-Output.md` §6).
- **Unchanged doctrine**: the corpus's exit/ledger discipline transfers
  verbatim; a 2019 "I stopped after the banner" report is still the correct
  2026 shape.
- **Where modern sources live**: the body-cited reference set (OWASP,
  PortSwigger, MongoDB operator docs, the Drupal advisory) is recorded in
  `references/blogs-index.md`; the full case register in
  `references/source-index.md`.

## 9. Vault file map

| File | Role | Confirmed cases |
|---|---|---|
| `Time-Based-Blind.md` | clock oracle; series method; carriers | 37 |
| `Boolean-and-Content-Oracle.md` | band pairs; ordering oracle; extraction ladder | 14 |
| `Error-and-Union-Output.md` | in-band value→error conversion; union rows | 20 |
| `Out-of-Band-Callback.md` | callback channel (MSSQL) | 1 |
| `SQLi-to-RCE-Chains.md` | write/read gadget chains incl. NoSQL | 4 |
| `Library-and-Framework-SQLi.md` | builder/layer sinks; position table | 21 |
| `README.md` | corpus stats, dispositions, limitations | — |

(97 classified + 1 adjacent + 2 negative-control rows = the 100 full bodies;
the 51 metadata-only and 96 HTTP-404 rows are ledgered in
`references/source-index.md`.)

## 10. The adjacent case and the negative controls (read before filing either kind)

- **SQL-687908 (Omise, $200 list, resolved) is the vault's one *adjacent*
  case, kept but not classified**: through Censys-origin-IP recon on
  `go.exchange` the reporter reached a **PgHero instance** (a live PostgreSQL
  dashboard) among ten origin IPs. The vault boundary rule in action — the
  finding is *internal-service exposure reached before any SQL injection*,
  labeled `Improper Access Control - Generic` in the archive; its SQL-side
  promise ("[ Can SQL Injection ]" in the title) is what the exposed
  *dashboard itself* would enable, not an injection the body demonstrates.
  An agent who finds an exposed DB dashboard should record it exactly this
  way: infrastructure exposure first (cross-vault: the SSRF vault's
  Internal-Service-Exposure class), injection claims only if a body proves
  them.
- **Positive negative-controls, quoted in
  `Boolean-and-Content-Oracle.md` §8**: SQL-131047 (Gratipay, informative) —
  *"I haven't managed to inject something, but I just want to make sure that
  this input is filtered."* — and SQL-115304 (Paragon Initiative Enterprises,
  not-applicable), header-probing the SQLi-prevention-guide authors' own
  site. Both are detection-only attempts without extraction: the era's own
  "prove it or don't submit" rows. They anchor the vault's kill-gate: a
  beautifully executed probe with no oracle demonstration is not a finding.

## 11. Dataset reproducibility

- Source list: `https://github.com/shreyaschavhan/h1-reports-for-reference/blob/master/tops_by_bug_type/TOPSQLI.md`
  (247 rows: parsed copy + row metadata in `/tmp/opencode/sqli/sqli_top_list.json`).
- Fetch method: `https://hackerone.com/reports/<id>.json`, unauthenticated,
  1.2 s spacing, everything cached under `/tmp/opencode/sqli/cache/`;
  digest corpus in `/tmp/opencode/sqli/bodies.txt`.
- Dispositions: `/tmp/opencode/sqli/disposition_table.md` (row-per-row ledger:
  full-body+category, metadata-only, HTTP-404).
- Classification: `/tmp/opencode/sqli/classification.json`; bounty
  accounting: `/tmp/opencode/sqli/bounty_acct.json`.

Any future agent can re-verify a quote by fetching the cached report JSON and
grepping the exact string; no quote in this vault was written from memory.
