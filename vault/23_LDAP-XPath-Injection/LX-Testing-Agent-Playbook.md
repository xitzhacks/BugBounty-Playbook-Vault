---
title: "LX Testing Agent Playbook — the executable protocol"
type: agent-playbook
category: ldap-xpath
cwe: "CWE-90, CWE-643"
built: "2026-11-07"
corpus: "11 classified rows -> 0 bodies read (11 metadata-only GHSL rows) · corpus block; 1 adjacent XQuery row held outside"
bounty: "$19,000 across 8 rows with DB figures (max $4,500 LX-1212273) · 3 rows no figure"
companion_modules: "00 codeql-corpus-block (sole module; corpus block, zero quotes)"
quote_rule: "byte-true, from read bodies only; metadata-only rows recorded never quoted"
---

# LX Testing Agent Playbook — LDAP / XPath injection

*Evidence base: 11 classified GHSL rows, **zero read bodies** (corpus block). This playbook is therefore a *method-family protocol* (the LDAP/XPath query-injection family documented outside this vault) with the corpus block cited only for pricing and kill-gate discipline. Every corpus-derived claim below traces to the case-register; every technique step is labeled as non-corpus doctrine and must be validated against a lab directory/parser in scope — never quoted as if observed in this vault's closed corpus.*

## P0 — Program classification & policy read (before any payload)

1. Program type: this corpus contains only `github-security-lab` CodeQL-query rows. A
   commercial program with a live LDAP directory or XPath-backed XML service is a different
   asset class — read its scope and its *query-sink* rules (which bind parameters, which
   endpoints accept directory/XML queries) before probing. GHSL query bounties ($1,800 flat
   tier; $2,500/$3,000/$4,500 exceptions) price detector authorship, not target impact —
   never use them to estimate a live-target payout.
2. Environment signal: classify the stack — directory-backed auth (LDAP bind / search
   filters built from user input) vs XML-backed query (XPath/XQuery expressions built from
   user input) vs configuration-only posture (endpoint/TLS/auth settings, CWE-297/522/287
   family). Only the first two are injection surfaces; the third is hardening review.
3. Kill-gate: no testing yet — P0 produces the *policy envelope* only.

## P1 — Query-sink inventory (LDAP/XPath/XQuery builders)

1. **LDAP builders** — every place user input becomes an LDAP search filter, DN, or bind
   credential. Corpus rows name the languages the detectors covered (Java 5 · Python 3 · Go 2 ·
   JavaScript 1 — title census, `00_codeql-corpus-block.md` §1); inventory the same matrix
   in the target's stack: filter-concatenation sites, DN-construction sites, auth-bind sites.
2. **XPath/XQuery expressions** — every place user input becomes an XPath predicate, XQuery
   FLWOR/flow expression, or XML document selection. Corpus rows cover CWE-643 (XPath, Go)
   and CWE-90 (LDAP) families; the adjacent XQuery row (1133573, CWE-652, outside this
   vault) confirms XQuery belongs to the inventory matrix even though this build does not
   hold its body.
3. **Configuration posture** — endpoint/TLS/authentication settings (CWE-297/522/287 rows).
   Log them as hardening observations, not injection probes; the authentication vault owns
   the defensive posture.

## P2 — Probe protocol (from cheapest signal to hardest — non-corpus doctrine)

**Label: none of the steps in P2–P3 below is observed in this vault's corpus (the corpus has no bodies). They are the standard query-injection family from the SQLi/XXE vaults, stated so an agent has a lab protocol — and so the gap between corpus evidence and doctrine is explicit.**

1. **Filter-breakout probes** — metacharacter pairs for the grammar in play (LDAP filter
   operators, XPath quote/bracket closures). Single-character probes that produce *syntax
   errors* prove the sink before any enumeration.
2. **Syntax-error oracles** — distinguish parse errors from no-match results; a differential
   is the cheapest reliable sink confirmation and needs no exfiltration.
3. **Boolean enumeration** — true/false result sets (directory entries present/absent, XML
   nodes selected/none). Respect rate limits; directory services are often auth-coupled.
4. **Blind timing** — last resort only; directory/XML timing is noisy. Prefer error/boolean
   differentials.

## P3 — Proof ladder (the modest demonstrations hold up)

1. One syntax-error differential plus one boolean true/false pair per sink. No dump, no
   credential extraction — a lab directory with synthetic entries is the ceiling.
2. For authentication-configuration observations (CWE-297/522/287 family): state the
   setting, the expected binding behavior, and the observed gap. No bypass attempt against a
   production directory.
3. Title-only GHSL rows are never cited as proof in any report — their lesson is pricing
   only (playbook P5 gate 2).

## P4 — Modern hardening fingerprints (never corpus doctrine)

- **LDAP**: parameterized filter builders (escape all filter metacharacters at the API
  boundary), least-privilege bind identities, disable anonymous binds.
- **XPath/XQuery**: compile expressions with bound variables, never string-concatenate
  untrusted input into predicates; enable DTD/external-entity discipline on the parser.
- **General**: allow-listed query shapes over free-form expressions; structured logging of
  query-construction sites so inventory (P1) stays current.

## P5 — Pre-report gates (kill-gates)

1. **Class gate** — you can name the query grammar (LDAP filter / XPath / XQuery) and the
   construction site. A metadata-only analogy ("GHSL has a query for this") is not a
   finding — the corpus block's 11 rows are all in that state and paid $0 in technique terms.
2. **Identity gate** — you demonstrated injection, not hallucination: an error differential
   or boolean pair with a request log. Title-only rows are never proof.
3. **Boundary gate** — state what the bind identity / parser could not reach. Sandbox-bounded
   or bind-bounded queries are a *finding with a boundary* — write the boundary.
4. **Production gate** — directory/auth work stays in the lab. A probe against a production
   LDAP directory is an automatic kill, regardless of signal quality.
5. **Noise gate** — configuration observations (endpoint/TLS posture) filed as injection
   die here; file them as hardening review under Authentication-Session's posture.

## Module ↔ phase table

| Phase | Corpus evidence (module) | Anatomy |
|---|---|---|
| P1 inventories query builders | 00 (§1) | Language/CWE census (Java/Python/Go/JS; CWE-090/522/287/297/643) — the matrix to inventory in a target |
| P2 probes error→boolean→blind | _(none — non-corpus doctrine)_ | Error differential first, boolean pair second, blind timing last |
| P3 proofs ladder, honest boundaries | 00 (§6) | Lab-directory ceiling; GHSL flat-tier pricing as the only corpus money signal |
| P4 hardening fingerprints | 00 (§§3–4) | Parameterized builders; bound XPath variables; config-posture boundary |
| P5 kill-gates | 00 (§§2, 6) | "No body, no class" gate; title-only rows are pricing, never proof |

## Non-goals

- Detector authorship (writing a CodeQL query) — outside this agent protocol; the corpus
  block exists to record that GHSL bought detectors, not to teach query-writing.
- Live-target LDAP/XPath exploitation — outside any module's claims; P2–P3 are lab protocols.
- XQuery body doctrine — the single adjacent XQuery row (1133573) is held outside this vault;
  its technique, if ever needed, belongs to the XXE vault or a future build, cited here only
  to keep the bucket reconciliation exact.
