---
title: "Vault/DOS — denial of service & uncontrolled resource consumption playbook set"
type: index
category: "Denial of Service (native memory crash / sandbox segfaults, ReDoS & regex CPU exhaustion, HTTP protocol floods, webapp resource abuse, adjacent cache-poisoning & unclassified merges)"
built: "2026-11-07"
evidence: "240 disclosed h1-brain corpus cases (221 bucket rows + 19 unclassified merges) · 238 full bodies read end-to-end + 2 GHSL metadata-only rows (DOS-801230, DOS-1061211) recorded never quoted"
bounty: "$275,868 across 117 rows (bucket $238,864/106 · merges $37,004/11) · native $149,500/38 · redos $12,395/10 · http $20,250/8 · webapp $51,219/47 · adjacent+merges $42,504/14 · full reconciliation in references/case-register.md"
companion_vaults: "../Cache-Poisoning · ../Prototype-Pollution · ../RCE · ../Authentication-Session · ../Business-Logic"
case_id_scheme: "DOS-<HackerOne report id>"
quote_rule: "byte-true, (sic)-marked, from archived bodies only (references/archive/DOS-bodies-full-dump.txt); metadata-only rows recorded never quoted"
---

# Vault/DOS — the denial of service playbook set

One vault, five lanes, one doctrine: **the corpus pays for unbounded work against a
shared victim**. The sandbox's two-line Ruby that kills the parent MRI ($10,000 ×8),
the preview button that burns a core for 60 seconds ($7,640), the header that parks a
webhook job at 100% CPU for a year, the frames that OOM Tomcat while staying under the
GOAWAY line, the single UDP packet that wedges a validator forever — different
mechanisms, same invariant: one request commits work the server cannot cap.

## Start here

| # | File | What it gives you |
|---|---|---|
| 1 | [`DOS-Testing-Agent-Playbook.md`](DOS-Testing-Agent-Playbook.md) | **The executable protocol.** P0 policy envelope (single-request, bounded discipline) → P1 surface inventory → P2 probe ladder (timing → parallel → boundary → frames → parent-crash → timeout-defeat) → P3 proof ladder → P4 modern fingerprints → P5 kill-gates. |
| 2 | [`01_Native-Memory-Crash-DoS.md`](01_Native-Memory-Crash-DoS.md) | **The richest module ($149,500/38).** The mruby $10,000 crash cluster + $8,000 tier + fuzzing flat rate. Anchors: DOS-181685 (Range excision), DOS-181828 (parent-MRI kill), DOS-183356 (bytecode corruption), DOS-187305 (SIGTERM-proof hang), DOS-42797 (Rails nested-hash StackError). |
| 3 | [`02_ReDoS-Regex-CPU-Exhaustion.md`](02_ReDoS-Regex-CPU-Exhaustion.md) | Compile-time bombs and header-triggered parses. Anchors: DOS-1518036 (`(?:){4294967295}`, $4,000), DOS-1929567 (`Time.rfc2822`, $4,000), DOS-511381 ($1,000), DOS-1283484 ($600), DOS-1531958 (year-long Sidekiq job). |
| 4 | [`03_HTTP-Protocol-Flood-DoS.md`](03_HTTP-Protocol-Flood-DoS.md) | CONTINUATION floods, chunk-extension holes, slowloris. Anchors: DOS-2586226 ($4,920), DOS-2334401 ($4,860), DOS-2453328 ($3,645), DOS-2375446 ($3,495), DOS-2453322 ($2,580). |
| 5 | [`04_Webapp-Resource-Abuse.md`](04_Webapp-Resource-Abuse.md) | Unbounded inputs and parser exhaustion (100 rows, $51,219/47). Anchors: DOS-1543718 (**$7,640**, vault webapp max), DOS-2105808 ($5,000), DOS-363636 ($4,000), DOS-470067 ($3,000), DOS-2258758 ($2,540), DOS-1904097 ($2,400). |
| 6 | [`05_Adjacent-And-Unclassified.md`](05_Adjacent-And-Unclassified.md) | The last module: 16 adjacent bucket rows + 19 unclassified merges ($42,504/14). Cache-poisoning cluster, lodash pollution, and the $10,000 the bucket missed (DOS-185775) + Rack CVE family. |

## Scoreboard (top 29 of 240 rows · 117 paid · $275,868 vault total · max $10,000 ×9)

| Case | Title (short) | Program | Bounty |
|---|---|---|---|
| DOS-181685 | mruby `Range#initialize_copy` NULL deref | shopify-scripts | **$10,000** (max) |
| DOS-181828 | mruby null deref kills parent MRI | shopify-scripts | **$10,000** |
| DOS-181910 | Range type-confusion DoS | shopify-scripts | **$10,000** |
| DOS-182484 | CALL_MAXARGS=127 segfault | shopify-scripts | **$10,000** |
| DOS-183356 | `break`/`||=` bytecode corruption | shopify-scripts | **$10,000** |
| DOS-187305 | zero-length heredoc infinite loop | shopify-scripts | **$10,000** |
| DOS-187536 | codegen NODE_NEGATE NULL deref | shopify-scripts | **$10,000** |
| DOS-188326 | `mrb_time_asctime` buffer overflow | shopify-scripts | **$10,000** |
| DOS-185775 | `Decimal.new(self)` assertion crash (merge) | shopify-scripts | **$10,000** |
| DOS-180695 | 49,000× `A` crashes mruby.science | shopify-scripts | $8,000 |
| DOS-181232 | mruby splat+redo NULL deref | shopify-scripts | $8,000 |
| DOS-181695 | `method_missing` NULL deref | shopify-scripts | $8,000 |
| DOS-184712 | `mrb_ary_concat` invalid access | shopify-scripts | $8,000 |
| DOS-1543718 | GitLab issue-preview 60s CPU burn | gitlab | $7,640 |
| DOS-2105808 | RSKJ single-packet wedge | rootstocklabs | $5,000 |
| DOS-2520679 | Rack Range-header giant response (merge) | ibb | $5,420 |
| DOS-2586226 | Tomcat HTTP/2 stream-count leak | ibb | $4,920 |
| DOS-2334401 | Tomcat CONTINUATION flood OOM | ibb | $4,860 |
| DOS-1518036 | `(?:){4294967295}` empty-repetition bomb | ibb | $4,000 |
| DOS-1929567 | Ruby `Time.rfc2822` ReDoS | ibb | $4,000 |
| DOS-363636 | PeerExplorer connection leak | rootstocklabs | $4,000 |
| DOS-1804128 | PermitScrubber backtracking (merge) | ibb | $4,000 |
| DOS-2453328 | Node HTTP/2 `Http2Session` assert crash | ibb | $3,645 |
| DOS-2375446 | Node chunk-extension unbounded read | ibb | $3,495 |
| DOS-470067 | Mermaid Issue-page freeze | gitlab | $3,000 |
| DOS-1096609 | Shopify `Host: :1337` cache poison | shopify | $2,900 |
| DOS-2453322 | httpd CONTINUATION pre-413 buffering | ibb | $2,580 |
| DOS-2258758 | Django UsernameField unicode burn | ibb | $2,540 |
| DOS-409370 | HackerOne X-Forwarded cache poison | security | $2,500 |

Corpus program mix: shopify-scripts 63 · ibb 54 (+ merges ibb-heavy) · gitlab 11 · x 10 ·
security 6 · rootstocklabs 6 · nextcloud 6 · brave 5 · automattic 5 · nodejs 5 ·
mattermost 5 · nodejs-ecosystem 4 · kubernetes 4 · hyperledger 3 · rails 2 (bucket; merges
add github-security-lab 2). Bucket total $238,864/106; merges $37,004/11; vault
$275,868/117 of 240.

## Vault map

| File | Content |
|---|---|
| `DOS-Testing-Agent-Playbook.md` | Agent-facing operational playbook: P0–P5 phases, module↔phase map, non-goals |
| `01_Native-Memory-Crash-DoS.md` | Sandbox segfaults & NULL derefs: the mruby $10,000 cluster, $8,000 tier, fuzzing flat rate, Rails/PHP-FPM/Tor/libgd rows |
| `02_ReDoS-Regex-CPU-Exhaustion.md` | Empty-repetition bombs, cubic lexers, header-triggered parses, the year-long webhook job |
| `03_HTTP-Protocol-Flood-DoS.md` | CONTINUATION floods, GOAWAY avoidance, chunk-extension holes, slowloris timing |
| `04_Webapp-Resource-Abuse.md` | Unbounded inputs (preview/move/comment), parser exhaustion (Django/Rack), P2P wedges, client freezes, cookie bombs |
| `05_Adjacent-And-Unclassified.md` | Cache-poisoning availability cluster, prototype pollution, the 19 merge rows (mruby $10,000 + Rack CVE family + amplification pair) |
| `references/source-index.md` | Provenance (h1-brain DB, sha256, 3,673 → 221 → 240), classification funnel, bounty accounting, era discipline, 7 limitations |
| `references/case-register.md` | 240-row ledger (221 bucket + 19 merges) with DB weakness/asset/CVE/bounty, class census, bounty arithmetic |
| `references/archive/DOS-bodies-full-dump.txt` | All 240 bodies verbatim (anchor for every quote) |
| `references/archive/classes.json` | Frozen module assignment for all 240 rows (every bucket id exactly once) |

## Cross-vault links

- `Cache-Poisoning/` — module 05's nine cache rows (1096609, 409370, 326639, 350847, 591302, 921704, 1160407, 1173153, 1181946) are availability *impacts* of poisoning primitives; the sibling vault owns the poisoning, this vault supplies the DoS examples.
- `Prototype-Pollution/` — DOS-380873/864701 (lodash `constructor.prototype`) sit adjacent here for their DoS impact; the pollution class belongs there.
- `RCE/` — module 01 shares its mruby corpus with RCE module 04 (same reports, opposite threat model; DOS-183356 / RCE-183356 is one report cited from both vaults).
- `Authentication-Session/` — DOS-649533's 2FA-without-email-verify half and DOS-1173684's shareinfo row belong to its modules; the DoS pointer is here.
- `Business-Logic/` — "unlimited comment length" is resource abuse here (557154); "unlimited invite/mint" is state abuse there. The work-vs-state test separates them.
- `Memory-Corruption/` (upcoming master row 30) — module 01's native crash rows are its web-facing slice; the vaults share DOS-181910's RCE caveat from opposite sides.

## Limitations

1. **The 221-row bucket is a label lower bound.** An exact-weakness filter missed $37,004 (13.4% of vault money) behind `weakness_name None`; the 19-row merge pass recovers the measured 19, but the remaining ~449 unclassified rows were not full-text swept for DoS this build.
2. **Bounty `None` ≠ unpaid.** 123 of 240 rows carry no figure in the DB (115 bucket + 8 merges). $275,868 is a corpus floor, not a total; the corpus carries no `$0` rows.
3. **2 GHSL rows are metadata-only** (DOS-801230, DOS-1061211: 54-byte bodies, $2,800, no quotable technique) plus DOS-153093's advisory-only body. Recorded, never reconstructed.
4. **Adjacent-pool rows are impact-only.** Cache poisoning, prototype pollution and the 2FA/CTF rows stay for bucket completeness; `Cache-Poisoning/` and `Prototype-Pollution/` own their mechanisms.
5. **Era honesty** — evidence spans the 2015 sandbox flat-tier era and the 2023–2025 CVE wave. Modern hardening is fingerprinted in playbook P4 and labeled outside the corpus; tooling is historical record.
6. **Chainpay vs pure-DoS**: the cache rows pay because poisoning supplies the availability loss, and the mruby rows pay because the sandbox supplies the shared victim. Pure "slow request" reports without a shared victim or an accounting bypass have no paid exemplar in this corpus.
7. **QA**: every blockquote in the five modules, this README and the playbook was byte-verified against `references/archive/DOS-bodies-full-dump.txt`; `(sic)` marks author typos. All 221 bucket ids + 19 merges appear exactly once in `references/archive/classes.json`.


<!-- CASESTOCK-LINK:BEGIN -->

## Case stock — vault (`_VAULT/`)

**578 disclosed reports** routed to this category · 163 with a bounty figure · **$310,610** · 457 full write-ups stored locally.

- Full list: [`_VAULT/by-vault-category/21_Denial-of-Service.md`](../_VAULT/by-vault-category/21_Denial-of-Service.md)
- Query: `sqlite3 ../_VAULT/reports.sqlite "SELECT id,bounty,title FROM reports WHERE ..."`
- Pull one write-up: `python3 ../_VAULT/scripts/extract_report.py <id>`

| Top paid | Program | Bounty |
|---|---|---|
| [170532](https://hackerone.com/reports/170532) Oracle Webcenter Sites administrative and hi-privilege access available directly | LocalTapiola | $18,000 |
| [181685](https://hackerone.com/reports/181685) Range#initialize_copy null pointer dereference | shopify-scripts | $10,000 |
| [181828](https://hackerone.com/reports/181828) Segfault in mruby, mruby_engine and the parent MRI Ruby due to null pointer dere | shopify-scripts | $10,000 |
| [181910](https://hackerone.com/reports/181910) Range constructor type confusion DoS | shopify-scripts | $10,000 |
| [182484](https://hackerone.com/reports/182484) Broken handling of maximum number of method call arguments leads to segfault | shopify-scripts | $10,000 |

_refreshed 2026-11-17 from the public HackerOne disclosed-report dataset_
<!-- CASESTOCK-LINK:END -->
