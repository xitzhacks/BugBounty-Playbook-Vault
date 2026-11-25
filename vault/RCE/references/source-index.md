---
title: "RCE source index — provenance, funnel, fetch mechanics, limitations"
type: source-index
built: "2026-11-05"
---

# Source index — RCE build

## 1. Roster provenance

- **Primary roster**: full HTML of `h1.security.nathan.sx` — 4,419 public HackerOne report rows,
  snapshot frozen **2017-09-12**, re-fetched live this build (`curl -sL`, HTTP 200, 1,105,968
  bytes; byte-parse identical: 4,419 unique rows). Same mirror as the `../XXE`, `../CSRF`,
  `../Open-Redirect` and `../Authentication-Session` builds.
- **Title filter** — 8 case-insensitive arms applied to mirror titles:
  `\brce\b|remote code execution|remote command execution|code execution|command injection|command execution` (rce-core) ·
  `unserializ|deserializ|serialize` (deser) · `arbitrary (code|command|os)|execut(e|ion).*(code|command)|code execu` (code-exec) ·
  `template injection|ssti|jinja|smarty|liquid|twig|freemarker|velocity` (ssti) · `code injection` (code-inject) · `\beval\b` (eval) ·
  `shellshock|bash.?shell` (shellshock) · `php object injection|phpobject` (poi).

  Funnel: 4,419 mirror rows → **118 base-roster matches** (re-derivable by running the
  8 arms over the mirror titles; arm-tag spread: rce-core 56 · code-exec 37 · deser 34 ·
  cmd-inject 20 · ssti 8 · code-inject 6 · eval 2 · shellshock 1 — one title can carry
  several arms) → all fetched.
- **Supplemental pass (documented, post-roster; 32 rows — the lane-coverage the base arms
  under-count), all fetched (30 live · 2 dead)**, grouped:
  (a) **Exposed console / device-console lane** (4) — 121940 (dl-fw.cgi device console,
  "shell injection" title), 167859, 182104, 231460 (Jenkins-family exposure titles; the
  three added by direct `jenkins` grep of mirror titles).
  (b) **PHP archive/pickle crash family** (8) — 73237, 73259, 103990, 103992, 104005,
  104008, 104026, 104027 (archive-parser + pickle-adjacent titles lacking RCE/code-exec
  wording).
  (c) **mruby crash batch** (17) — 192485, 196380, 196386, 197693, 201903, 202582,
  202584, 203513, 205536, 207710, 210429, 210671, 214845, 216700, 217097, 221251, 222294
  (SIGSEGV/NULL-deref/UAF crash-report titles).
  (d) **Perl crash** (1) — 207983 (S_regmatch heap over-read).
  (e) **Dead roster rows whose titles carried no arm** (2) — 66929 (Apache CVE list,
  "Code Exec/" miss), 116937.
  All 32 supplemental rows were classed by body read. Final corpus:
  **150 rows = 134 live + 16 dead**.
- **Verified zero-coverage notes**: the ImageMagick/ImageTragick, Struts/Jakarta and webshell
  title families produced **0 base hits on the mirror** (direct grep); ImageTragick-era rows in
  the corpus (135072, 143966) entered via the rce-core and code-exec arms. Recorded as a
  limitation, not reconstructed.

## 2. Fetch mechanics

- Unauthenticated `https://hackerone.com/reports/<id>.json` returns flat report objects
  (title, substate, severity_rating, bounty_amount, weakness, team{handle}, disclosed_at,
  vulnerability_information). No auth, no cookies. 1.4 s sleep between calls`fetch.sh`,
  UA header); single pass, zero transient 000s (150/150 answered).
- 404 rows: response body is empty → recorded in `http-codes.txt`, never quoted, never
  reconstructed. 16 dead IDs listed in `references/case-register.md` as `404` rows
  (dead rate 16/150 ≈ 10.7% — below the 16–20% seen on earlier vault builds).
- Body dump: `dump.py` → `bodies.txt` (5,090 lines), header format
  `===== RCE-<id> | <title> | sev=<…> | bounty=<…> | substate=<…> | weak=<…> | len=<n>`;
  JSON-PARSE-ERROR rows mark the dead. All 134 live bodies read end-to-end on 2026-11-04.

## 3. Bounty reconciliation rule

JSON `bounty_amount` where present → labeled **json**. Otherwise the mirror list figure →
labeled **list** (the mirror is the frozen 2017-09-12 list state; several disclosures
withhold the amount — the list figure is the only source and is labeled as such). Dead rows
keep their list figure labeled **404-list**. Per-row source lives in
`archive/bounty-reconciliation.json`.

- JSON-stated: **$73,187 / 32 rows**
- List-stated: **$157,947 / 63 rows**
- Dead-404 list: **$39,734 / 12 rows** (of 16 dead)
- **Grand: $270,868 / 107 rows** — class modules 01–07: **$231,044 / 93 rows**; module 08
  adjacent+noise: $90 / 2 rows; module 09 DoD corpus: $0 / 0.

Module ledger: 01 $51,862/14 · 02 $14,400/6 · 03 $28,075/25 · 04 $106,100/36 · 05 $850/2 ·
06 $20,300/3 · 07 $9,457/7 · 08 $90/2 · 09 $0/0.

## 4. BugBountyHunter (bugbountyhunter.com) — taxonomy check, re-verified 2026-11-04

The `/vulnerability/` type index **retains** a `command_injection` page ("Learning about
Command Injection" — used byte-quoted in blogs-index §1a), but the 2026-10-28-era `code`
type page **no longer resolves** (today `?type=code` serves the generic index shell; type
list today: access_control, apitesting, bugbounty_toolkit, command_injection, csrf,
fileuploads, idor, javascript_files, notetaking, open_redirect, sql, ssrf, waybackmachine,
xss, xxe). There is **no** deserialization type page. Taxonomy drift since the 2026-10-28
build: `code` and `token` type pages dropped.

The class's disclosed-stats ledger lives on `/disclosed/` (fetched 2026-11-04,
`bbh-disclosed.html`, 264,115 B). Bucket counts are ajax-loaded (`getinfo?weakness=<id>`),
not in the static table; the getinfo endpoints were fetched for the four RCE-relevant
buckets and return today's per-program histograms and listed-report counts:

| BBH weakness bucket (id) | Reports listed today | Top programs |
|---|---|---|
| Command Injection - Generic (55) | 82 | Nodejs-ecosystem 33 · Gitlab 13 · Ubnt 9 |
| Code Injection (8) | 101 | Deptofdefense 37 · Nodejs-ecosystem 28 · ibb 28 |
| OS Command Injection (3465) | 32 | Deptofdefense 11 · Nodejs-ecosystem 5 · Starbucks 5 |
| Deserialization of Untrusted Data (3245) | 30 | Deptofdefense 9 · Basecamp 4 · ibb 4 |

(Master-list row 9's historic bucket figures are from the 2026-10-28 snapshot; today's live
figures above are recorded, not silently overridden.)

## 5. Bug bounty blogs (bugbountyhunting.com)

Full index fetched once: 7,103 entries (`script.js`, 1,383,906 bytes). RCE-class arms
produced **643 raw matches** (`archive/blog-raw-matches.json`), curated to **612** in
`references/blogs-index.md` §2 (lane sections 2.1–2.7: 54 cmd / 33 deser / 32 ssti /
10 code-inject / 36 panels / 105 CVE / 13 gadget / 231 stories / 95 chains / 3 roundups;
31 web.archive duplicates dropped). Two sources fetched and byte-quoted in §1:
bugbountyhunter.com's command-injection guide (2026-11-04) and HackerOne's johnk
"how to command injections" blog post (July 7, 2017 — mirror era, fetched live 2026-11-04).

## 6. Era discipline

- The mirror froze **2017-09-12**; the corpus is a 2013–2017 snapshot (era spread of the
  134 live rows: 2013×1 · 2014×5 · 2015×35 · 2016×32 · 2017×61; the 16 dead rows carry
  no disclosed date).
- Post-2017 cases enter only the bibliography (blogs-index §2/§3), never class counts, and
  modern hardening is fingerprints-in-P4, not corpus doctrine.
- Team names in the register are mirror list names (★ artifact stripped); handles come from
  the fetched JSON (e.g., Flash rows show team `ibb` — the Internet Bug Bounty program
  administered the Adobe/Flash bounties).

## 7. Limitations

- **Bounty withholding**: 102 live rows carry no bounty figure (39 with neither json nor
  list amount). Bounty-unknown is not bounty-zero.
- **404 rows**: 16 of 150 (10.7%) — roster-only records; bodies never seen. Dead-list figures
  total $39,734/12 and are recorded but never quoted. RCE-141956 ([phpobject in cookie]
  $20,000) and RCE-142562 (Unserialize→XXE $10,000) are the largest dead rows; both are
  recorded in dead-list, not in class modules.
- **Metadata-only bodies**: 28 of 134 live bodies are empty (`len=0`): 46019, 113928,
  116575, 167859, 184279, 188284, 192567, 197958, 201903, 202652, 202774, 203600, 205536,
  210671, 211381, 212022, 212985, 213069, 213776, 221294, 226245, 229199, 231460, 231687,
  231926, 232330, 257207, 258117. These are classed from title + weakness + severity +
  substate only (module 09 holds the 15 DoD rows; the rest carry metadata-only notes in
  their modules). Nothing was invented for them; no quotes exist for them.
- **Quote sources**: every vault blockquote is byte-true from `bodies.txt` (the parsed,
  fetched json bodies) or from the two §1 fetched guide pages. Quote audit re-normalizes
  both sides per-blockquote; see the vault README audit line.
- **Weakness-tag mislabels**: several corpus rows carry misleading weakness tags
  (29480 CSRF-tagged but body is command injection; 125027/217790/230234 XSS-lane;
  231460/167859 info-disclosure-tagged; 183356 resource-consumption-tagged). Classification
  is by read body, never by tag; the register notes call out the lively mismatches.
- **DoD corpus**: 15 metadata-only resolved rows from the single DoD VDP program — kept
  together in module 09 because the program's substate+severity-only reporting pattern is
  itself the lesson (no bodies survive, $0 bounty tier, duplicates included).
