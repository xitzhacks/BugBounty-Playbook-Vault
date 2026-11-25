---
title: "DOS Testing Agent Playbook — the executable protocol"
type: agent-playbook
category: dos-all
cwe: "CWE-400 (with CWE-770/789/835/1333 and CWE-476/787 siblings)"
built: "2026-11-07"
corpus: "240 cases (221 bucket rows + 19 unclassified merges) — 238 full bodies + 2 GHSL metadata-only rows"
bounty: "$275,868 across 117 rows (bucket $238,864/106 · merges $37,004/11) · native $149,500/38 · redos $12,395/10 · http $20,250/8 · webapp $51,219/47 · adjacent+merges $42,504/14"
companion_modules: "01 native-memory-crash · 02 redos-regex-cpu · 03 http-protocol-flood · 04 webapp-resource-abuse · 05 adjacent-and-unclassified"
quote_rule: "byte-true, (sic)-marked, from archived bodies only (references/archive/DOS-bodies-full-dump.txt); metadata-only rows recorded never quoted"
---

# DOS Testing Agent Playbook

Executable protocol derived from 240 read bodies (2015–2025 era; corpus money concentrated
2015–2016 in the Shopify sandbox and 2023–2025 in the HTTP/2 and parser-CVE waves). Every
step cites corpus evidence. Run phases in order; abort at kill-gates. Crown-jewel doctrine
up front: **payouts track the shared victim and the measured burn, not the cleverness of
the payload** — the vault's $10,000s are two-line Ruby files that kill the parent MRI
(module 01), its $7,640 is a preview button that burns a core for 60 seconds (module 04),
and its $4,000s are header-triggered stdlib parses (module 02) and GOAWAY-avoiding frame
tricks (module 03). The class's biggest single premium is the *unbounded input × shared
resource* pair: one request commits work the server cannot cap.

## P0 — Program classification & policy read (before any payload)

1. Program type: commercial bounty vs VDP vs vendor lab. The corpus's native lane is
   almost entirely `shopify-scripts` (63 rows) and `ibb` (54 rows) — vendor/OSS programs
   that priced *distinct crash primitives* as flat tiers ($100–$10,000). The webapp lane
   is the reverse: SaaS targets (gitlab 11, x 10, rootstocklabs 6, nextcloud 6, brave 5)
   that price *measured availability loss*. Read which economy the program is in before
   choosing a target: the same null deref is $800 in a vendor lab and $0 on a SaaS site
   where you cannot reach the interpreter.
2. Policy envelope: DoS testing is *destructive by nature*. Modern programs almost
   universally ban or tightly scope DoS (cf. DOS-993582's quoted out-of-scope notice:
   "Any activity that could lead to the disruption of our service (DoS)"). P0 produces
   the written envelope: which hosts, which rate, which payload classes, and whether a
   single-request bounded burn (the corpus's safe shape — 60-second timeout, one core,
   clean recovery) is permitted. If the envelope is silent, the corpus's own discipline
   applies: **single request, single core, measured, recoverable** — never a flood, never
   a botnet, never sustained.
3. Kill-gate: no testing yet — P0 produces scope + the funnel note below.

**Funnel note (auditable surface).** This vault's corpus is 221 bucket rows
(`weakness_name = 'Uncontrolled Resource Consumption'` in the h1-brain DB) **plus 19
unclassified-merge rows** recovered from the 468-row unclassified pool (all with
`weakness_name None`). Before claiming completeness, state your funnel the way
`references/source-index.md` does: source, filter, merges, and what the merges
contained. A report that shows its funnel is trusted; a coverage claim without one is
not.

## P1 — Surface inventory (what to probe, mapped from corpus)

| Surface | Why it exhausts | Corpus proof |
|---|---|---|
| Sandboxed interpreters / Eval endpoints | Tenant code reaches C-level bugs; crash kills shared runner | module 01: 63 `shopify-scripts` rows; `MRubyEngine.new(...).sandbox_eval` shape |
| Core-library parsers (Range, Decimal, Time, URI) | Stdlib parse reachable from default-on headers/filters | DOS-181685/185775, module 02: `Time.rfc2822` via `ConditionalGet` |
| Regex compiles + render paths | Backtracking on file-view/markdown/auth/webhook | module 02: Rouge 1283484, color-validator 511381, webhook 1531958 |
| HTTP/2 frame handlers | CONTINUATION/SETTINGS buffering pre-END_HEADERS | module 03: 2334401, 2453322, 2586226 |
| Markdown/preview/move endpoints | Unbounded input → 60s CPU burn | module 04: 1543718, 1543584, 470067, 670572 |
| Multipart parsers | Unbounded parts → FD/memory exhaustion | module 04: 1904097, 1954937; merge 431561 |
| P2P / node daemons (UDP handlers, PeerExplorer) | One packet wedges shared node | module 04: 2105808, 363636, 1695472 |
| Cookie / object stores | Cookie bombs, huge names, token invalidation DoS | module 04: 57356, 777984, 210779, 1018037 |
| Cache keys / cacheable responses | Poisoned shared cache = persistent DoS | module 05: 1096609, 409370, 591302 |

Inventory rule from module 01 §4: for every parser you reach, classify the fix shape
(drop the runtime lookup / guard the transform / cap the length / cap the recursion) —
the report names the shape, the fix follows.

## P2 — Probe protocol (from cheapest signal to hardest)

Per candidate surface, in ascending blast radius, with the corpus's evidence standard:

1. **Single-request timing.** One textbook input (long string, deep nesting, big
   exponent) and a stopwatch. Corpus template: DOS-2258758 — "a single request took 4.4
   seconds on average" (1M unicode chars in a `UsernameField`). Baseline with normal
   input first; quote the delta, not the absolute.
2. **Parallel multiplier.** Same request ×N concurrent → fleet effect. Corpus template:
   DOS-1543718 — "Multiple requests can be issued in parallel to create a larger impact";
   DOS-2258758's 20-concurrent → 60 s waits + 504s. The parallel step is where a slow
   request becomes an availability finding.
3. **Boundary probes.** One below / at / above the suspected cap. Corpus templates:
   DOS-182484 (`n == CALL_MAXARGS` = 127, exact boundary), DOS-670572 (5,000-char cap
   bypassed per-block), DOS-350847 (1024-char request-URI limit bypassed via UTF-8
   expansion). A cap-bypass is a second finding on the same bug.
4. **Protocol-frame probes.** Stay under the server's declared limits while multiplying
   connections. Corpus template: DOS-2334401 (CONTINUATION frames "up to the limit ...
   so that connection is not dropped by a server (GOAWAY/ENHANCE_YOUR_CALM)"). If the
   server has no cap, say so — the absence is the finding.
5. **Sandbox/daemon probes.** One-liner payloads in the eval endpoint; check the
   *parent*. Corpus template: DOS-181828 ("crash in mruby_engine and the parent MRI
   Ruby process"). A child-only crash is a weak report; a parent crash is the finding.
6. **Timeout-defeat check.** For every timeout in the stack, test whether the payload
   runs *inside* the timeout's check interval. Corpus templates: DOS-2375446 ("timeouts
   and limiting request body size do not seem to work"), DOS-1531958 (Sidekiq job
   "stuck at 100% CPU ... (weeks later)"), DOS-799072 (1 byte/sec beats a 2 s timeout).

## P3 — Proof ladder (the modest demonstrations paid)

1. **Timed single request** (module 04's floor): screenshot the clock delta, quote the
   corpus template shape (4.4 s avg; 60 s timeout burn).
2. **Parallel burn** (module 04's multiplier): N concurrent → CPU saturated / 504s /
   FD exhaustion. DOS-1904097's "too many files being open and memory exhaustion" is the
   FD-end proof; DOS-1543718's "entire server is completely unavailable" is the
   DockerHub end proof.
3. **Parent-process crash** (module 01): child segfault → engine → parent MRI dead.
   Attach the minimal file + version/commit + lldb `EXC_BAD_ACCESS` (the era's proof
   format; see DOS-181232/184712).
4. **Persistent wedge** (module 04 §3): one packet, node never recovers on its own
   (DOS-2105808). Show the stuck state persisting after the attacker stops.
5. **Shared-cache poison** (module 05): poison → second visitor blocked. Always use
   the corpus's cache-buster discipline (bespoke query string so the live cache is not
   harmed — DOS-1160407/1173153/1181946 disclaimers are the honest template).

## P4 — Modern fingerprints (post-corpus hardening, labeled as outside the corpus)

- **HTTP/2 hardening**: `maxConcurrentStreams` + header-table caps + CONTINUATION
  timeouts (post-2024 patches for CVE-2024-24549/27316/34750). Fingerprint the *response*
  to a CONTINUATION burst (GOAWAY vs close) before assuming the 2024 shape.
- **Regex engines**: RE2/Rust-`regex` linear-time enforcement + compile-time input-size
  caps that count *unrolled* work (post-1518036). Fingerprint with the empty-repetition
  probe; byte caps alone are the vulnerable config.
- **Framework parsers**: bounded multipart parts + bounded header/Range sizes
  (Django 3.2.18+/Rack 3.x). Fingerprint the multipart-part count at which the
  framework starts 413ing.
- **Sandbox hardening**: typed C-API boundaries, `mrb_state` core-class pinning, fuzzed
  codegen. Fingerprint by running the corpus's minimal files against the *current*
  build and reporting the regression status, not by fuzzing blind.
- **Cache hardening**: cache keys that include `Host`/`Origin`/`X-Forwarded-*`, or
  `Vary` discipline (post-591302). Fingerprint with a cache-busted dual-origin test.

## P5 — Kill-gates (abort and reclass)

1. **Volume-only floods.** "Many requests made the site slow" with no unbounded input
   named → not a finding. The corpus's paid floods all bypass an accounting boundary.
2. **Unbounded client-only impact with no shared victim.** A hang that only affects your
   own browser tab → the floor of the class; file under the browser lane only with a
   second victim (DOS-970760's pixel-flood is the exception that proves the rule).
3. **Class-boundary claims.** Verification gaps (649533), CTF write-ups (1066851),
   prototype pollution filed as DoS (380873) → reclass to the owning vault, cite this
   vault as the impact pointer.
4. **No-figure rows are not failures.** `-` means the DB carries no figure (115/221
   bucket rows). Check for a CVE in the title before discounting; never state
   "unpaid" from `-` alone.
5. **Metadata-only rows are anchors, not evidence.** DOS-801230/1061211 ($2,800) carry
   no quotable technique. Record them; do not invent their payloads.
6. **Flood policy.** If the program's envelope does not explicitly allow sustained
   load, the entire flood lane (P2 rungs 2/4 sustained variants) is closed — the
   single-request bounded burn (rung 1) is the only permitted shape.

## Module ↔ phase map

| Phase | 01 Native | 02 ReDoS | 03 HTTP flood | 04 Webapp | 05 Adjacent |
|---|---|---|---|---|---|
| P0 scope | vendor-lab flat tiers | CVE-coordination | CVE-coordination | SaaS measured-loss | routing + funnel |
| P1 inventory | sandboxes, parsers | regex + render | frame handlers | preview/multipart/nodes | cache keys, merge pool |
| P2 probe | parent-crash one-liners | backtracking strings | sub-limit frame bursts | timing → parallel | poison + cache-buster |
| P3 proof | minimal file + trace | CPU profile | GOAWAY-avoidance math | timed burn + FD count | second-visitor block |
| P4 modern | pinned core classes | unrolled-work caps | stream caps | bounded parsers | Vary/key discipline |
| P5 kill | child-only crash | auth'd-only regex | capped-server flood | volume-only | impact≠class |

## Non-goals (what this playbook does not do)

- **No volumetric flood testing.** Sustained connection/request floods against live
  targets are out of scope unless the program's written envelope explicitly permits
  them; the corpus's flood rows are frame/handshake accounting bugs, demonstrated with
  minimal traffic.
- **No service disruption of shared tenants.** Multi-tenant wedges are demonstrated
  with the minimum blast radius that proves the shared-victim claim (one packet, one
  preview, one cached poison with a cache-buster) — never by taking the service down
  for other users.
- **No invented technique for metadata-only rows.** The two GHSL one-liners and the
  advisory-only rows are recorded with title + bounty + CVE only.
- **No cross-class claiming.** Cache poisoning, prototype pollution, 2FA, and business-
  logic rows are routed to their owning vaults; this playbook claims only the
  availability impact with a pointer.
- **No live exploitation beyond the corpus's safe shapes.** Every probe above is
  single-request, timed, recoverable, and policy-enveloped. Anything else is a
  different engagement.
