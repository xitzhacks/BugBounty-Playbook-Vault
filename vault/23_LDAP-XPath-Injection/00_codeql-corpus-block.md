---
title: "CodeQL corpus block — 11 LDAP/XPath rows, zero bodies, zero quotes"
type: playbook
category: codeql-corpus-block
cwe: "CWE-90, CWE-643"
source_count: 11
full_bodies_available: 0
corpus: "h1-brain disclosed_reports.db (3,673 rows), bucket ldap-xpath (classified.json) -> module codeql-corpus-block (module_map_all.json)"
list_accessed: "2026-11-07"
note: "Corpus block (cf. RCE module 09 DoD corpus): all 11 bodies are the 54-byte GHSL pointer line. Nothing is quoted; classification is title+CWE+bounty only. $19,000 across 8 rows with DB figures."
---

# CodeQL corpus block — eleven LDAP/XPath rows, zero bodies, zero quotes

## 1. Overview

Eleven rows, **$19,000 / 8 rows with bounty figures**, every one from `github-security-lab`,
every one a CodeQL-query report, every one metadata-only. The bodies in
`references/archive/lx-bodies-full-dump.txt` are byte-identical 54-byte pointer lines:

> This bug was reported directly to GitHub Security Lab.

There is no second sentence to quote in any of the 11 rows. The vault therefore keeps this
module as a corpus block for the same reason RCE module 09 keeps the DoD rows: deleting them
would falsify the roster; writing technique from them would invent evidence.

**Case-stock (11 rows / $19,000):**

| Case | Target | Mechanism | Bounty |
|---|---|---|---|
| [LX-787113](https://hackerone.com/reports/787113) | github-security-lab | CodeQL query for LDAP Injection, Java (CWE-90) | $3,000 |
| [LX-824925](https://hackerone.com/reports/824925) | github-security-lab | XPath Injection query, Java | — |
| [LX-852316](https://hackerone.com/reports/852316) | github-security-lab | XPath Injection query, Go (CWE-643) | $1,800 |
| [LX-956295](https://hackerone.com/reports/956295) | github-security-lab | LDAP injection vulnerability, Java | $2,500 |
| [LX-1050706](https://hackerone.com/reports/1050706) | github-security-lab | CodeQL to detect LDAP Injection, JavaScript (CWE-90) | — |
| [LX-1095708](https://hackerone.com/reports/1095708) | github-security-lab | Insecure LDAP authentication, Java (CWE-522) | $1,800 |
| [LX-1133572](https://hackerone.com/reports/1133572) | github-security-lab | Insecure LDAP endpoint configuration, Java (CWE-297) | $1,800 |
| [LX-1212273](https://hackerone.com/reports/1212273) | github-security-lab | LDAP Injection, Python (CWE-090) | $4,500 |
| [LX-1287575](https://hackerone.com/reports/1287575) | github-security-lab | LDAP Improper Authentication, Python (CWE-287) | $1,800 |
| [LX-1350076](https://hackerone.com/reports/1350076) | github-security-lab | Insecure LDAP Authentication, Python (CWE-522) | $1,800 |
| [LX-1397942](https://hackerone.com/reports/1397942) | github-security-lab | LDAP Injection All For One, Go (CWE-090) | — |

Language split (title-read): Java 5 · Python 3 · Go 2 · JavaScript 1. Query flavor: six rows
say "query / CodeQL" and five name the flaw (injection / insecure authentication / endpoint
configuration). CWE split (title-read): 090/90 ×3 · 522 ×2 · 287, 297, 643 ×1 each ·
LDAP-injection-unnumbered ×1 · XPath-unnumbered ×1. The `codeql-corpus-block` module key in
`module_map_all.json` holds exactly these 11 ids; `_adjacent_unclassified` holds one more
(1133573, XQuery Injection) which is not in this vault.

## 2. Why there are zero quotes

The vault quote rule is byte-true quotes from read bodies only. The only byte-available
sentence is the 54-byte GHSL pointer line, repeated 11 times; quoting it once in this section
documents the format and quoting it 11 more times would add no evidence. No technique
sentence exists in the corpus — no filter string, no LDAP filter, no XPath expression, no
PoC, no remediation paragraph. This section therefore records the *absence* as the finding
rather than paraphrasing a method into existence.

## 3. What the module is allowed to say

1. **The CodeQL-query archetype**: "CodeQL query for finding LDAP Injection (CWE-90)
   vulnerabilities in Java" (787113), "XPath Injection query in java" (824925), "Go/CWE-643:
   XPath Injection Query in Go" (852316), "[javascript] CWE-90: CodeQL to detect LDAP
   Injection" (1050706) — the bounty prices a detector, not a target. Six of the 11 titles
   announce the query; the payouts ($1,800–$3,000) price query authorship across languages.
2. **The flat-tier tell**: five rows at exactly $1,800 (852316, 1095708, 1133572, 1287575,
   1350076), plus exceptions at $2,500 (956295), $3,000 (787113), $4,500 (1212273), and three
   rows with no DB figure (824925, 1050706, 1397942). The flat tier is the GHSL query price;
   the exceptions carry title-level detail the vault cannot verify without bodies.
3. **The language-pairing tell**: Java rows cluster on injection + endpoint/authentication
   CWEs; Python rows are the only ones that split improper-authentication (287) from
   insecure-authentication (522); Go rows pair CWE-643 (XPath) with CWE-090 (LDAP). With no
   bodies, the pairing is a title census only — it must not be read as detector guidance.
4. **The authentication-vs-injection boundary**: CWE-287/297/522 rows (1095708, 1133572,
   1287575, 1350076) are configuration/authentication questions. Whether the underlying
   queries even test filter-breakout is unknowable from titles; the vault does not merge them
   into an injection methodology.

## 4. The adjacent row (explicitly out of scope)

LX-1133573 is *not* in this vault. It is the `_adjacent_unclassified` row in
`module_map_all.json` for this bucket: "Java: CWE-652 Improper Neutralization of Data
within XQuery Expressions ('XQuery Injection')", `github-security-lab`, bounty `None`,
54-byte body. XQuery is an XML-query sibling of XPath, so a future vault may absorb it; this
build keeps the 11-row bucket exact and names the row here so the bucket reconciliation is
auditable. It appears in no count, no case-stock table, and no archive dump in this vault.

## 5. What the corpus cannot price

No row demonstrates a live LDAP directory, a live XPath sink, a filter, a payload, or an
impact. The GHSL query bounties therefore say nothing about how a production LDAP/XPath
disclosure would be priced — and the adjacent XQuery row (unpriced in the DB) says nothing
either. Any LDAP/XPath payout estimate from this vault would be invention.

## 6. What pays, what doesn't

- The corpus pays **detector authorship**, flat: five rows at $1,800, one at $4,500
  (1212273, the vault max), one at $3,000 (787113), one at $2,500 (956295). The three
  unfixed rows (824925, 1050706, 1397942) carry no DB figure — blank is not zero.
- Nothing in the corpus pays for a *demonstrated* LDAP/XPath injection against a live
  target. There is no live-target row at any price. The gap is the vault's central honesty
  point: the most-cited money rows are the least quotable.
- **No-bounty vs no-body**: three rows lack figures; all 11 lack bodies. These are different
  absences. The $0 rows in other vaults (e.g. RCE module 09) still carry triage history;
  here every row is simultaneously body-less, so the module can only teach *absence
  discipline* — record, verify, never reconstruct.

## 7. Cross-references

- `XXE/` — the XQuery adjacent row (1133573) and the XML-query grammar family live
  next door; the XXE vault owns XQuery-adjacent parser doctrine if a future build absorbs it.
- `SQLi/` — string-concatenation injection methodology (filter-breakout → syntax error →
  blind enumeration) is the method family; this module supplies no body evidence for it.
- `Authentication-Session/` — the CWE-287/297/522 authentication-configuration rows overlap
  its defensive posture; cite this module for the GHSL pricing only.
- Playbook P5 (`LX-Testing-Agent-Playbook.md`) cites this module for the "no body, no class"
  gate: a metadata-only row is never cited as proof in a report.
