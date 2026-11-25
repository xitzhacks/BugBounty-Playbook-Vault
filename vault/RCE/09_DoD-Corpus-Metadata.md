---
title: "DoD corpus — 15 metadata-only RCE rows from the Department of Defense VDP (substate+severity only)"
type: playbook
category: dod-corpus-meta
cwe: "CWE-78"
source_count: 15
full_bodies_available: 0
corpus: "h1.security.nathan.sx roster (150 rows), bodies via hackerone.com/reports/<id>.json"
list_accessed: "2026-11-04"
note: "Zero bodies survive; nothing is quoted; classification is title+severity+substate only. $0 bounty tier throughout."
---

# DoD corpus — fifteen RCE rows, zero bodies, zero bounties

## 1. Overview

Fifteen rows from the U.S. Department of Defense VDP, **$0 total** — every one resolved
(or duplicate), every one a `len=0` body. Their titles are uniform variants: "RCE on a
Department of Defense website", "Remote code execution vulnerability on a DoD website",
"Remote Code Execution (RCE) in a DoD website", "Remote Command Execution on a DoD
website", "Local Code Execution (RCE) in a DoD website" — with severities critical
(9×), high (1× plus the two SSRF/XXE-tagged chain rows), low (1×), none (2×, both
duplicates). Thirteen weakness tags say Code Injection; the two chain rows say SSRF/XXE.

**Case-stock (15 rows):**

| Case | Title | Substate | Severity |
|---|---|---|---|
| [RCE-184279](https://hackerone.com/reports/184279) | RCE on a Department of Defense website | resolved | critical |
| [RCE-188284](https://hackerone.com/reports/188284) | Remote code execution on an Army website | resolved | critical |
| [RCE-192567](https://hackerone.com/reports/192567) | Remote code execution vulnerability on a DoD website | resolved | high |
| [RCE-202652](https://hackerone.com/reports/202652) | Remote command execution (RCE) vulnerability on a DoD website | resolved | critical |
| [RCE-203600](https://hackerone.com/reports/203600) | Remote code execution vulnerability on a DoD website | resolved | low |
| [RCE-211381](https://hackerone.com/reports/211381) | Remote Code Execution (RCE) in a DoD website | resolved | critical |
| [RCE-212022](https://hackerone.com/reports/212022) | Remote Code Execution (RCE) in a DoD website | resolved | critical |
| [RCE-212985](https://hackerone.com/reports/212985) | Remote code execution vulnerability on a DoD website | resolved | critical |
| [RCE-213069](https://hackerone.com/reports/213069) | Remote Code Execution (RCE) in a DoD website | duplicate | (none) |
| [RCE-213776](https://hackerone.com/reports/213776) | Remote Command Execution on a DoD website | duplicate | (none) |
| [RCE-226245](https://hackerone.com/reports/226245) | Remote code execution (RCE) in multiple DoD websites | resolved | critical |
| [RCE-229199](https://hackerone.com/reports/229199) | Limited code execution vulnerability on a DoD website | resolved | high (SSRF-tagged) |
| [RCE-231687](https://hackerone.com/reports/231687) | Remote Code Execution (RCE) vulnerability in multiple DoD websites | resolved | critical |
| [RCE-231926](https://hackerone.com/reports/231926) | Remote Code Execution (RCE) vulnerability in a DoD website | resolved | critical |
| [RCE-232330](https://hackerone.com/reports/232330) | Remote Code Execution in a DoD website | resolved | high (XXE-tagged) |

## 2. What the module is allowed to say

Nothing about mechanics — no bodies survive, and the vault never reconstructs.
What the module records is the *pattern itself*:

1. **Severity inflation without evidence**: nine "critical" rows, all VDP, all unpaid.
   The DoD program assigned critical to RCE-class reports by title; no public body
   demonstrates any of them.
2. **Duplicate honesty**: RCE-213069/213776 — the same title family as 212985 (which
   resolved separately), marked duplicate. The corpus's only module with
   triage-duplicates: 2 of 15 rows.
3. **Weakness-tag tells**: 229199 tagged SSRF ("Limited code execution" — chain row),
   232330 tagged XXE — the two rows whose tags name an originator class, kept here
   because the titles promise code execution only. The other thirteen tags read
   "Code Injection" — the era's catch-all bucket for report-token RCE claims.
4. **The claim-report archetype**: "RCE in a DoD website" as a one-line submission — the
   module-08 playbook caution ("title-only RCE claims = nothing to review") has no
   bigger specimen set than this one.

## 3. Why they are not merged into other modules

The class-vault rule (bodies win) would otherwise leave them unclassifiable — and
deleting them would falsify the roster (the mirror lists them; the fetch pipeline
verified them). Keeping them as one corpus block preserves: the honest 150-row ledger,
the substate mix, and the negative-space lesson that a resolved-critical RCE with no
bounty and no body is a *claim*, not a finding.

## 4. Cross-references

- Module 08 holds the equivalent noise tier on commercial programs.
- Playbook P5 cites this module for the "no body, no bounty, no class" gate.
