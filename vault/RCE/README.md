---
title: "Vault/RCE — command injection, code injection & deserialization playbook set"
type: index
category: "RCE (all three lanes in one vault: OS command injection·argument/protocol injection, server-side template injection & app-eval primitives, unsafe deserialization by language, memory-corruption execution, desktop-client load paths, devops-console exposure, cross-class chains, adjacent noise, DoD metadata corpus)"
built: "2026-11-05"
evidence: "150 roster rows from h1.security.nathan.sx mirror → 134 retrievable bodies read (125 resolved / 3 informative / 3 not-applicable / 3 duplicate) + 15 DoD VDP metadata-only rows kept as corpus block · 16 × 404 recorded"
bounty: "$270,868 roster-tagged grand total (JSON-verified $73,187/32 rows · list-stated $157,947/63 fetched rows · dead-404 list $39,734/12 rows) · pure class 01–07 $231,044/93 · adjacent+noise 08 $90/2 · DoD corpus 09 $0 · full reconciliation in references/case-register.md"
companion_vaults: "../XXE · ../CSRF · ../Open-Redirect · ../Authentication-Session"
case_id_scheme: "RCE-<HackerOne report id>"
quote_rule: "byte-true, (sic)-marked, from read bodies only; 404 rows recorded never quoted"
---

# Vault/RCE — the command injection · code injection · deserialization playbook set

One vault, three lanes, per the build order: the class's money in this corpus is
**execution reach**, and the corpus prices it coherently — flat tiers for engine bugs,
five-figure awards for sandbox RIP control and clean SSTI, $0 for claims.

## Start here

| # | File | What it gives you |
|---|---|---|
| 1 | [`RCE-Testing-Agent-Playbook.md`](RCE-Testing-Agent-Playbook.md) | **The executable protocol.** P0 program/policy read → P1 surface inventory (argument positions, engines, deserializers, consoles) → P2 probe protocol (math probe → timing oracle → OOB → boolean oracle → second-order) → P3 proof ladder → P4 modern hardening fingerprints → P5 kill-gates. |
| 2 | [`01_OS-Command-Injection.md`](01_OS-Command-Injection.md) | Shell metacharacters, argument injection, protocol injection, blind-timing oracle. Anchors: RCE-29839 (Shellshock $20,000 list), RCE-212696 (imgur `gm convert` space-argument injection, $5,000), RCE-73567 (Shopify `$(sleep 20)` blind proof, $3,000), RCE-214022 (Discourse second-order gzip backticks, $512 JSON). |
| 3 | [`02_Template-Injection-App-Primitives.md`](02_Template-Injection-App-Primitives.md) | Jinja2/Smarty/Liquid/Rails primitives — the 6/6 paid module. Anchors: RCE-125980 (Uber Jinja2 SSTI, $10,000 JSON — the corpus SSTI crown), RCE-164224 (Smarty `{php}`, $400), RCE-44513 (Web Console XFF parser differential, $500). |
| 4 | [`03_Unsafe-Deserialization.md`](03_Unsafe-Deserialization.md) | PHP `unserialize()` genome (18 engine bugs, all paid at $500–$3,000), Rails signed-cookie unmarshal, ysoserial lane, pickle, YAML `!php/object`, plugin POP. Anchors: RCE-134321 (Algolia secret→cookie RCE, $500 JSON), RCE-206227 ($2,500), RCE-153026 (Starbucks ysoserial error-differential). |
| 5 | [`04_Memory-Corruption-Code-Execution.md`](04_Memory-Corruption-Code-Execution.md) | The richest module ($106,100/36): Flash quartet ($37,500), mruby sandbox corpus (crown rows $20,000/$18,000/$10,000 + flat-rate crash batch), phar six-pack. Anchors: RCE-181879 (RIP 0x133713371337), RCE-183356 (codegen `break` corruption). |
| 6 | [`05_Desktop-Client-Load-Path.md`](05_Desktop-Client-Load-Path.md) | Other-users'-machine execution: Slack OpenSSL config hijack ($750), ownCloud QT plugin ($100), Brave save-page (duplicate). All three bodies real — smallest module, zero empty bodies. |
| 7 | [`06_Devops-Console-Exposure.md`](06_Devops-Console-Exposure.md) | The console *is* the primitive: RCE-231460 ("Open prod Jenkins", **$15,000 JSON**, metadata-only), RCE-258117 ($5,000 auth-flow test Jenkins), RCE-182104 (Udemy exposure chain, $300). |
| 8 | [`07_RCE-From-Other-Class-Chains.md`](07_RCE-From-Other-Class-Chains.md) | Delivery lanes from other classes: Drupal SQLi→session→exec ($3,000), GitLab file-read→marhalled cookies (critical), Redis→Sidekiq `instance_eval`, client-side template-injection reclass records (Uber $3,000/Shopify $1,000 paid as *client-side*) — titles never decided these classes. |
| 9 | [`08_Adjacent-Noise.md`](08_Adjacent-Noise.md) | The negative space: the MS-DOS joke row, junk/N-A submissions, mislabeled tags, theory rows (one got $50), the $40 mystery — exhibit shelf for the playbook kill-gates. |
| 10 | [`09_DoD-Corpus-Metadata.md`](09_DoD-Corpus-Metadata.md) | Fifteen resolved RCE rows, zero bodies, zero bounties, one third duplicates — the claim-report archetype, kept as a corpus block. |

## References (provenance layer)

| File | Contents |
|---|---|
| [`references/source-index.md`](references/source-index.md) | Roster provenance (nathan.sx mirror, 4,419 rows re-fetched byte-identical), the 8 title arms + 22-row documented supplemental passes (devops-console lane + memory-corruption crash batch), funnel (150→134·15 metadata-only→full read), bounty reconciliation, BBH taxonomy drift (`code` type page gone 2026-11-04; getinfo counts 82/101/32/30), era statistics, fetch mechanics, 7 limitations. |
| [`references/case-register.md`](references/case-register.md) | Row-per-row ledger of all 150 roster rows: case ID, team, substate, bounty (json/list/404-list labeled per row), class 01–09/dead, disposition note. Mystery waits: RCE-257207's $40, RCE-168485's $50. |
| [`references/blogs-index.md`](references/blogs-index.md) | §1 two byte-quoted command-injection guides (bugbountyhunter.com `command_injection` page — payload list + zseano sleep tip §1a; HackerOne Jobert July 7, 2017 how-to — timing oracle, generic/blind split, extraction ladder §1b) · §2 612 title-linked bugbountyhunting.com writeups curated by lane (54 cmd / 33 deser / 32 SSTI / 10 code-inject / 36 panels / 105 CVE / 13 gadget / 231 stories / 95 chains / 3 roundups) · §3 fifteen modern skill-cited cases (Metabase CVE-2023-38646, OpenSSH CVE-2023-38408, Confluence CVE-2023-22527, GiveWP POP→RCE CVE-2024-5932…) · §4 dropped-selection record. |
| [`references/archive/bodies-full-dump.txt`](references/archive/bodies-full-dump.txt) | All 134 retrieved report bodies, verbatim dump (5,090 lines) + the 16 dead headers. |
| [`references/archive/json/`](references/archive/json/) | All 150 raw JSON responses from `hackerone.com/reports/<id>.json` (16 are preserved 404 pages). |
| [`references/archive/bounty-reconciliation.json`](references/archive/bounty-reconciliation.json) | Per-row bounty reconciliation (src: json/mirror/404-mirror/none + class). |
| [`references/archive/http-codes.txt`](references/archive/http-codes.txt) | The 16 dead-404 ids as fetched. |
| [`references/archive/classes.json`](references/archive/classes.json) | The frozen 150-row module assignment (bodies-win classification). |
| [`references/archive/roster-meta.json`](references/archive/roster-meta.json) | Per-row team/substate/severity/weakness/disclosed metadata. |
| [`references/archive/mirror-all-rows.json`](references/archive/mirror-all-rows.json) | Full re-fetched mirror snapshot (4,419 rows). |
| [`references/archive/blog-raw-matches.json`](references/archive/blog-raw-matches.json) | The 643 raw RCE-class blog matches pre-curation. |

## How this vault was built (method)

1. **Roster**: full HTML of `h1.security.nathan.sx` (4,419 public H1 reports, frozen
   2017-09-12, re-fetched byte-identical this build), filtered by 8 title arms → 118 base
   rows + a documented 32-row supplemental pass (4 console rows incl. the `jenkins` grep,
   8 PHP archive/pickle crash rows, 17 mruby crash rows, 1 Perl crash row, 2 dead rows
   whose titles carried no arm) → 150 rows.
2. **Retrieval**: every report fetched from the public unauthenticated
   `hackerone.com/reports/<id>.json` endpoint, 1.4s spacing → 134×200, 16×404, zero
   transient failures (funnel arithmetic exact).
3. **Reading**: all 134 bodies read end-to-end (`archive/bodies-full-dump.txt`); every
   class decided by bodies, not titles. Nine title-arm rows reclassified on body read —
   e.g. three Angular/twine "template injection" rows are client-side XSS (module 07's
   reclass record); a CSRF-tagged row is IRC protocol injection (module 01); an
   "RCE" title token row is `instance_eval` queue-trust (module 07) — recorded.
   Read-time bounty guesses were then overruled by the mechanical ledger (e.g. the
   mruby crash batch's flat $800 tier, EdgeSwitch's $2,000 metadata row).
4. **Bounty accounting**: JSON `bounty_amount` where present ($73,187 across 32 rows),
   otherwise the mirror's list-stated figure ($157,947 across 63 rows), labeled per row;
   $39,734 sits on unrecoverable 404 rows (list figures; largest: RCE-141956 $20,000,
   RCE-142562 $10,000).
5. **Modules**: nine class modules (incl. one negative-space module and one metadata
   corpus block), each with verbatim evidence, case-stock tables with labeled bounties,
   what-pays/what-doesn't sections, and cross-references.
6. **Quote audit (zero-miss gate)**: all 111 blockquote probes across the README,
   playbook, nine modules and the bibliography were mechanically checked against their
   archived sources — 109 match exact after whitespace normalization; 2 are trailing-`…`
   fragment cuts whose displayed characters are byte-true prefixes of the source
   (module 02's Smarty ladder at the `{F115752}` marker, module 03's plugin-POP list at
   the "more information:" cut). Zero unanchored quotes remain.
7. **Bibliography**: two command-injection guides fetched and byte-quoted (BBH page +
   the HackerOne blog's July 2017 post — inside the mirror era); 612 community writeups
   title-linked (bodies not fetched this build — the index is a hunt queue, not proof);
   modern post-roster cases kept out of register counts.

## Coverage vs limitations

**Covered**: OS command injection incl. blind proof discipline (timing baseline, exact
delta, repeat), argument injection via space-filter gaps (`${IFS}`), protocol/grammar
injection (IRC, SMTP, git transport), second-order admin-writer chains; server-side
template injection across Jinja2/Smarty/Liquid + Rails render/Web-Console eval
primitives; unsafe deserialization by owner (PHP engine genome, app-level POP, Java
ysoserial, Python pickle, YAML bridge, Ruby CookieStore); memory-corruption execution
across Flash/phar/mruby-sandbox/Python/Perl; desktop-client load-path hijacks;
devops-console exposure pricing; cross-class chains (SQLi/XXE/upload/read/token/SOME/
queue-trust origins); the noise floor and the DoD claim-report corpus.

**Honest limitations**:
1. The roster is a 2013–2017 snapshot (era spread 2013×1 · 2014×5 · 2015×35 · 2016×32 ·
   2017×61 on live rows) — modern hardening is fingerprinted in playbook P4 and the
   bibliography, labeled as outside the corpus.
2. 16 rows are permanently dark (404) — recorded, never quoted; their list figures
   ($39,734/12) are kept in dead-list arithmetic.
3. 28 of 134 live bodies are metadata-only (`len=0`) — titles + figures recorded,
   no technique content, nothing invented. Fifteen of them (all DoD VDP rows) live in
   module 09 as the corpus block.
4. Blog bodies were not fetched this build — `blogs-index.md` §2 is a hunt queue,
   not proof; §1 is byte-quoted from two actually-fetched guide pages.
5. Weakness labels are era values and often wrong (29480 "CSRF" = command injection,
   125027 "Code Injection" = client-side XSS, 231460 "Information Disclosure" = console
   exposure, 183356 "Uncontrolled Resource Consumption" = codegen corruption) — register
   keeps the archive label, modules correct against the body ("bodies win").
6. The BBH taxonomy check is a dated snapshot (2026-11-04): the 2026-10-28-era `code`
   type page no longer resolves (source-index §4 records both states honestly).
7. No live testing was performed — validate against the hunt-rce / hunt-cicd /
   hunt-api-misconfig skill scenario matrices.

## The one-paragraph doctrine of this corpus

RCE in this corpus is priced by **what the flaw reaches, not how it fires**: a shell in
a device console paid $1,300–$2,750; the same shell in an imgur pipeline paid $5,000;
expressions in an engine the target's mail path evaluated paid $10,000; a sandbox whose
whole purpose was to forbid the jump paid $18,000–$20,000 for RIP control alone; an open
console door paid up to $15,000 with no exploit at all; and the crash reports —
unexploitable NULL derefs in a sandboxed interpreter, flat-rated $100–$800 — were a
paid product line of their own. The finds that converted class-knowledge into
money are tiny and testable (one parameter, one `sleep`, one space, one symlink in a
tarball, one backtick in an admin name), the honest boundaries ("there is a length
limit", "can not be exploited, but it can cause DoS") were priced rather than punished,
and every class boundary dispute in the register — template-vs-shell, blob-parser-vs-
engine, client-side-vs-server-side — was settled by reading the body, never the title.


<!-- CASESTOCK-LINK:BEGIN -->

## Case stock — vault (`_VAULT/`)

**803 disclosed reports** routed to this category · 183 with a bounty figure · **$588,438** · 534 full write-ups stored locally.

- Full list: [`_VAULT/by-vault-category/RCE.md`](../_VAULT/by-vault-category/RCE.md)
- Query: `sqlite3 ../_VAULT/reports.sqlite "SELECT id,bounty,title FROM reports WHERE ..."`
- Pull one write-up: `python3 ../_VAULT/scripts/extract_report.py <id>`

| Top paid | Program | Bounty |
|---|---|---|
| [1609965](https://hackerone.com/reports/1609965) RCE via the DecompressedArchiveSizeValidator and Project BulkImports (behind fea | GitLab | $33,510 |
| [1679624](https://hackerone.com/reports/1679624) Remote Command Execution via Github import | GitLab | $33,510 |
| [925585](https://hackerone.com/reports/925585) RCE via npm misconfig -- installing internal libraries from the public registry | PayPal | $30,000 |
| [455645](https://hackerone.com/reports/455645) Exposed Kubernetes API - RCE/Exposed Creds | Snapchat | $25,000 |
| [591295](https://hackerone.com/reports/591295) Potential pre-auth RCE on Twitter VPN | X / xAI | $20,160 |

_refreshed 2026-11-17 from the public HackerOne disclosed-report dataset_
<!-- CASESTOCK-LINK:END -->
