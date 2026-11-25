---
title: "PP Testing Agent Playbook — the executable protocol"
type: agent-playbook
category: prototype-pollution
cwe: "CWE-1321"
built: "2026-11-07"
corpus: "4 classified rows -> 4 bodies read (4 full-body / 0 metadata-only) · 0 adjacent rows"
bounty: "$6,000 across 2 rows with DB figures (max $3,000 PP-1106238 ×2) · 2 rows no figure"
companion_modules: "00 prototype-pollution (sole module, 4 rows)"
quote_rule: "byte-true, from read bodies only; missing figures recorded never invented"
---

# PP Testing Agent Playbook — Prototype Pollution

*Evidence base: 4 disclosed h1-brain corpus cases (`PP-…`). Every quoted sentence in the module is byte-true to `references/archive/pp-bodies-full-dump.txt`. Read the module before improvising; this file is the operational spine.*

## P0 — Program classification & policy read (before any payload)

1. Program type: commercial program with a client bundle or server merge path, vs library
   program (lodash-style: the sink is the dependency, not the product). The corpus pays
   *in-program* pollution-plus-consumer ($3,000 × 2, GitLab/Mermaid) and records no figure
   for library-level pollution (PP-712065, CVE-2020-8203). Read policy for allowed
   stored-content testing now: test projects/issues you control only.
2. Environment signal: classify the sink family — deep-merge/config-merge, hash/query
   parsing (`deparam`-style), or directive/config injection (`%%{init:…}%%`-style). Each
   family feeds the polluter differently; inventory by family (P1).
3. Kill-gate: no testing yet — P0 produces the *policy envelope* only.

## P1 — Merge/parse-site inventory (where untrusted keys meet objects)

| Sink family | Corpus proof | What to map |
|---|---|---|
| Deep merge / defaults (`merge`, `defaultsDeep`, `zipObjectDeep`) | PP-712065 (lodash 4.17.15) | Every merge that walks attacker-influenced keys |
| Hash / query parsers (`deparam`-style) | PP-998398 (`location.hash` → `c = c[u]` walk) | Parsers that recurse into attacker-controlled paths |
| Directive / config injection | PP-1106238/1280002 (`%%{init:…}%%` → config merge) | User-stored config/directive surfaces merged into app objects |
| _Namespace keys_ (`__proto__`, `constructor`, `prototype`) | All 4 rows | Every merge site's handling of the three keys |

Then enumerate *every* object property the app reads *after* the merge — the gadget
candidates (§P2 rung 2).

## P2 — Probe protocol (pollute → name the gadget → climb)

1. **Canary pollution** — write a junk canary property (`polluted: asdf`, PP-1106238's
   payload) through the same sink and observe it on a fresh object. This is the $3,000
   Step-1 proof: app-wide breakage or a visible canary, reproduced on a clean page.
2. **Gadget search in the same file/stack** — list every property the app reads off the
   merged object (template engines/options, hook registries, `eval`-family consumers).
   PP-998398's gadget (`eval(hookFunction)`) and PP-1280002's (`template`) both live in the
   sink's own file/stack. One property per candidate; test the `__proto__.<property>` write.
3. **Payoff ladder** — DoS (break comments/actions, PP-1106238) → stored XSS via the named
   consumer (search-bar touch, PP-1280002) → server-side escalation only with a separate
   execution proof (PP-712065 claims RCE "in some cases" without one — do not claim it
   without one).
4. **Interaction honesty** — write the touch step if the gadget needs one ("if we click on
   the search bar"). The paid rows state it; the playbook requires it.

## P3 — Proof ladder (the modest demonstrations paid)

1. Canary: directive/parser payload stored and re-rendered on a clean session; screenshot
   of the canary or breakage (PP-1106238's "can't comment" page).
2. Gadget: the `__proto__.<consumer>` payload plus the touch step, alert firing in the
   reporter's controlled project (PP-1280002).
3. Non-interactive variant if it exists — state it; otherwise state the interaction.
4. Library rows: dependency version + `Object.prototype` canary + honest impact ceiling
   (PP-712065's "Variable" — written, not inflated).

## P4 — Modern hardening fingerprints (never corpus doctrine)

- **Key hardening at merge boundaries**: strip `__proto__` / `constructor` / `prototype`
  before any deep merge `Object.assign({}, a, b)` walk; merge into `Object.create(null)`
  dictionaries where attacker keys are expected.
- **Parser hardening**: allow-listed hash/query keys (PP-998398's lesson — a parser that
  recurses into any `[...]` path is the vulnerability).
- **Directive hardening**: schema-validate directive JSON before merging into config; keep
  style-only fields (`fontFamily`, `themeCSS`) allow-listed (PP-1106238's exact surface).
- **Consumer hardening**: never `eval()` config-sourced hooks (PP-998398's gadget); template
  properties are never read from pollutable config.

## P5 — Pre-report gates (kill-gates)

1. **Pollution gate** — you proved the canary landed on `Object.prototype` in a clean
   session. Sink-name alone dies here.
2. **Consumer gate** — you named the property the app reads and demonstrated *its*
   consequence (DoS page, XSS alert). "Properties present on all objects" with no consumer
   dies here (the PP-712065 pattern at `None`).
3. **Interaction gate** — the touch step (if any) is written in the Steps, as in both paid
   rows. Hidden interaction is a kill.
4. **Version gate** — dependency/version named (PP-712065's `lodash 4.17.15`), tested on
   the live target, local-instance only as supplement. CVE-echo without a live demo dies here.
5. **Noise gate** — prototype folklore ("you can pollute anything") without a sink file and
   a consumer dies here.

## Module ↔ phase table

| Phase | Corpus evidence (module) | Anatomy of the paid pattern |
|---|---|---|
| P1 inventories merge/parse sites | 00 (§§2–4) | lodash merge; `deparam` hash walk; Mermaid directive merge |
| P2 pollutes canary → names gadget | 00 (§§3–5) | `polluted` canary → `template` gadget → search-bar touch |
| P3 proofs ladder, honest ceilings | 00 (§§2–5) | DoS page ($3,000) → stored XSS ($3,000); "Variable" impact (712065) |
| P4 hardening fingerprints | 00 (§§4–5) | key stripping; parser allow-lists; directive schema |
| P5 kill-gates | 00 (§6) | consumer gate; interaction gate; library-at-`None` gate |

## Non-goals

- Prototype-pollution *detector* authorship (CodeQL queries, scanners) — outside this
  agent protocol; the LDAP vault's corpus-block pattern is the precedent for keeping
  detector pricing separate from target findings.
- Unbounded gadget hunting beyond the sink's own file/stack — the paid rows found their
  gadgets in-file; chain-hunting across the whole bundle is outside every module's claims.
- Server RCE via pollution without a separate execution proof — outside this vault (see
  `RCE/`); PP-712065's RCE sentence is recorded as a claim, not doctrine.
