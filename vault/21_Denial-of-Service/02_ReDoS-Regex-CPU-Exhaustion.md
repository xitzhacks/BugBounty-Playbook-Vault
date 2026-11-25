---
title: "ReDoS / regex CPU exhaustion — catastrophic backtracking and empty-repetition bombs"
type: playbook
category: redos-regex-cpu-exhaustion
cwe: "CWE-400 (ReDoS family; CWE-1333)"
source_count: 20
full_bodies_available: 20
corpus: "h1-brain disclosed_reports.db (3,673 rows; sha256 8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4) · bucket 'dos' = 221 rows, weakness 'Uncontrolled Resource Consumption'"
list_accessed: "2026-11-07"
note: "Anchor bodies: DOS-1518036 and DOS-1929567 ($4,000), DOS-511381 ($1,000), DOS-1283484 ($600). All 20 bodies read; quotes byte-true to references/archive/DOS-bodies-full-dump.txt."
---

# ReDoS / regex CPU exhaustion — one request, one core, forever

## 1. Overview

Twenty rows, **$12,395/10 paid** — the smallest paid module by dollars, and the most
modern-weighted: half the paid rows are 2023–2025 CVE-class disclosures (Ruby URI/Time,
Django, REXML, CGI, Action Text) where the *fix is already shipped* and the report is a
coordinated-disclosure record. The two $4,000 anchors define the class. DOS-1518036 is the
pure algorithmic bomb — a regex that allocates zero bytes while the compiler attempts
billions of empty repetitions, defeating every memory-based mitigation:

> Rust's regex crate guarantees a linear time complexity with regex length for compilation of untrusted regexes. However, existing mitigations for known malicious regexes are based on memory usage and, as such, do not mitigate repetitions of empty sub-expressions. For example, the following payload triggers such an issue:

> This will cause the regex compiler to attempt to create 4294967295 instances of an empty sub-expression, which will ultimately allocate zero bytes and therefore bypass existing memory-based mitigations. This can be further weaponised to create an exponential time complexity with regex length by using repetitions of repetitions, e.g.:

DOS-1929567 is the header-driven counterpart — a stdlib time parser reachable from any
`ConditionalGet` request:

> ReDoS occurs when `Time.rfc2822` accepts user input.

**Case-stock (20 rows / $12,395):**

| Case | Target | Mechanism | Bounty |
|---|---|---|---|
| [DOS-1518036](https://hackerone.com/reports/1518036) | ibb | (?:){4294967295} empty-repetition → infinite CPU | $4,000 |
| [DOS-1929567](https://hackerone.com/reports/1929567) | ibb | Time.rfc2822 via Rack ConditionalGet → ReDoS | $4,000 |
| [DOS-511381](https://hackerone.com/reports/511381) | gitlab | color-code validator regex → CPU 90%+ | $1,000 |
| [DOS-1283484](https://hackerone.com/reports/1283484) | gitlab | Rouge lexer cubic backtracking → 100% CPU | $600 |
| [DOS-2064723](https://hackerone.com/reports/2064723) | ibb | unsanitized regex input hangs Airflow request | $540 |
| [DOS-2068004](https://hackerone.com/reports/2068004) | ibb | ReDoS before 2.6.3 (Airflow) | $540 |
| [DOS-2792776](https://hackerone.com/reports/2792776) | ibb | Action Text blockquote ReDoS (CVE-2024-47888) | $505 |
| [DOS-2012131](https://hackerone.com/reports/2012131) | ibb | ActiveSupport underscore ReDoS (CVE-2023-22796) | $480 |
| [DOS-2012135](https://hackerone.com/reports/2012135) | ibb | GlobalID ReDoS (CVE-2023-22799) | $480 |
| [DOS-1000567](https://hackerone.com/reports/1000567) | cs_money | GraphQL search regex bomb (possible cmd injection) | $250 |
| [DOS-661722](https://hackerone.com/reports/661722) | ruby | DigestAuth split_param_value catastrophic backtracking | - |
| [DOS-1023899](https://hackerone.com/reports/1023899) | rails | ActiveRecord PostgreSQL Money ReDoS | - |
| [DOS-1404789](https://hackerone.com/reports/1404789) | ibb | Ruby Date parsing ReDoS | - |
| [DOS-1531958](https://hackerone.com/reports/1531958) | gitlab | webhook long header → Sidekiq 100% CPU for a year | - |
| [DOS-1944515](https://hackerone.com/reports/1944515) | ibb | URI ReDoS (CVE-2023-28755) | - |
| [DOS-2402193](https://hackerone.com/reports/2402193) | ibb | Django Truncator.words ReDoS (CVE-2024-27351) | - |
| [DOS-2446427](https://hackerone.com/reports/2446427) | ibb | Accept header parsing ReDoS (CVE-2024-26142) | - |
| [DOS-2807139](https://hackerone.com/reports/2807139) | ibb | REXML ReDoS (CVE-2024-49761) | - |
| [DOS-2872502](https://hackerone.com/reports/2872502) | ibb | query param filter ReDoS in Action Dispatch | - |
| [DOS-3023605](https://hackerone.com/reports/3023605) | ibb | CGI::Util#escapeElement ReDoS (CVE-2025-27220) | - |
## 2. The two $4,000 shapes: compile-time bombs and header-triggered parses

**Compile-time (1518036).** The payload is `(?:){4294967295}` — repetitions of an *empty*
sub-expression. The regex crate's linear-time guarantee covers regex length, not the
unrolled instance count, and memory accounting sees zero bytes. The weaponized form nests
repetitions (`{64}{64}…`) for 64⁶ instances. Every modern "we cap regex size" defense
that counts bytes misses this; the fix must bound *unrolled work*, and the report says so
by construction.

**Request-triggered (1929567).** `Time.rfc2822` parses the `If-Modified-Since` header via
`Rack::ConditionalGet`, which Rails enables by default — so a single unauthenticated
request reaches the backtracking pattern. The class lesson: ReDoS is priced by the
*default-on* header path, not by the exotic endpoint. (The reporter first filed
1485501; this row is the ibb disclosure record.)

## 3. The GitLab lane: app-level regexes at $1,000 and $600

DOS-511381 is the app-level classic — a color-code validator in
`app/validators/color_validator.rb` that any label/broadcast author reaches:

> An attacker can exhaust the server's CPU with this vulnerability, and cause a continuous DoS.

DOS-1283484 is the dependency lane — the Rouge syntax highlighter's lexer regexes have
"cubic worst-case complexity", and GitLab renders them on every file view and markdown
render:

> Gitlab is using the ruby gem "rouge" which has a ReDoS vulnerability. In rouge, the lexers used to parse programming languages rely heavily on regular expressions. Some of the regular expressions have cubic worst-case complexity and are vulnerable to Regular Expression Denial of Service (ReDoS). By crafting malicious input, an attacker can cause Denial of Service.

The pricing teaches dependency triage: the same backtracking bug is $1,000 in a validator
you own and $600 in a gem you vendor — but the *fix coordination* (upstream first, then
the app) is the reportable work, and both bodies record the upstream-report date.

## 4. The year-long job: when ReDoS outlives the timeout

DOS-1531958 (no figure in DB, but the corpus's best engineering write-up) is the ReDoS
that breaks the resource model: a webhook receiver returns a long header, Ruby's
`net/http` regex runs at 100% CPU in a Sidekiq job, and the job-scoped timeout never
fires because it is only checked *between* header lines:

> This causes the `web_hook` Sidekiq job to get stuck at 100% CPU utilisation until the regular expression processing is complete (weeks later).

The reporter explicitly contrasts this with #1252116 (connection held open) — CPU
exhaustion that *bypasses the fix* for the earlier DoS. Hunting translation: when a
service's timeout is checked between chunks, a single uninterruptible regex pass is the
bypass, and the report should demonstrate it with a job that lives for weeks.

## 5. The unpaid decade and the 2023–2025 CVE wave

Ten of the twenty rows carry no figure — including every 2024–2025 advisory-style row
(2402193, 2446427, 2792776, 2807139, 2872502, 3023605). These are coordinated-disclosure
records: the CVE is the deliverable, the H1 row is provenance. DOS-661722 (WEBrick
DigestAuth) is the pre-2020 unpaid exemplar and the module's cleanest payload, quoted
from its body:

> Sample attack string that causes catastrophic backtracking: a="\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b

Note the literal `\b` (backslash-b) in the attack string — backslashes, not word-boundary
tokens; the triager reproduces it by pasting the fenced block, not by reasoning about
the pattern. DOS-1000567 (GraphQL `search`) carries the parenthetical "(AND probably a
kind of command injection)" — the module's one class-boundary hedge, kept in the
case-stock mechanism because the title admits it.

## 6. What pays, what doesn't

- **Default-on header paths pay $4,000** (1929567): the pattern must be reachable without
  special privileges. `Time.rfc2822` via `ConditionalGet` needs no auth, no special
  content-type — that is the whole value proposition.
- **Zero-byte bombs beat byte caps** (1518036): if the defense counts bytes, repetitions
  of empty groups are free. Reports that demonstrate the cap-bypass explicitly (zero
  bytes allocated, infinite time) price highest in this corpus.
- **Timeout-bypass is a separate finding** (1531958): a regex that runs *inside* the
  timeout check defeats the previous fix. Show the long-lived job, not just the slow
  request.
- **CVE-coordinated rows may show `-`.** Half this module is triage/provenance rows for
  shipped fixes; `-` means the DB carries no figure, not that nobody worked. Don't
  discount a ReDoS because its row shows `-` — check for a CVE in the title first.
- **What doesn't pay:** a regex that only *you* can trigger with a debug header on a
  localhost you control. The paid rows all reach a shared render path (file view,
  markdown, auth, webhook).

## 7. Cross-references

- Module 04's Django/Rack rows (1746098 locale-regex, 2258758 UsernameField, 1954937
  multipart) are ReDoS-adjacent parser bugs filed under webapp abuse; the split here is
  by *engine* (regex crate / Ruby regex) vs by *endpoint* (form/multipart). Cite both
  sides when a parser row carries a CVE.
- Module 05's merge pool holds the ReDoS sequel rows the bucket filter missed (1804128,
  2584376, 2071561, 1627159) — same class, `weakness None` in DB. Their quotes live in
  module 05 §3.
- The `RCE/` vault's timing-oracle doctrine (sleep-baseline) is the cousin technique:
  both classes are measured in milliseconds, but ReDoS is filed with CPU profiles, not
  response deltas.
