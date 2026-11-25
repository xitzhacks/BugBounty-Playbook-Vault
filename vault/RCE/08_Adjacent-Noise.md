---
title: "Adjacent + noise — jokes, junk, mislabels, theory, best-practice: the corpus's negative space"
type: playbook
category: adjacent-noise
cwe: ""
source_count: 10
full_bodies_available: 9
corpus: "h1.security.nathan.sx roster (150 rows), bodies via hackerone.com/reports/<id>.json"
list_accessed: "2026-11-04"
note: "Negative-space module: claims trace to bodies read 2026-11-04; two rows carry tiny bounties ($50 + $40 list)."
---

# Adjacent + noise — what the RCE lane attracts and rejects

## 1. Overview

Ten rows, **$90/2 paid**. This is the dump lane, and it is where the era's lesson lives:
the class title "code/command execution" attracts jokes, unprovable theory, policy
quibbles, and mislabeled everything-else. Each row is quoted-not-summary where the body
is funny; none are class counts.

**Case-stock (10 rows / $90):**

| Case | Target | What it is | Bounty |
|---|---|---|---|
| [RCE-5499](https://hackerone.com/reports/5499) | MS-DOS (joke program) | "Arbitrary command execution in MS-DOS" — the famous resolved joke | - |
| [RCE-34917](https://hackerone.com/reports/34917) | block.io | client-side tickbox "bypass" + command-injection-sounding claim | - (informative) |
| [RCE-131452](https://hackerone.com/reports/131452) | gratipay | "PHP 5.4.45 is outdated and full of …" CVE list | - (N/A) |
| [RCE-146735](https://hackerone.com/reports/146735) | Uber | content spoofing labeled Command Injection | - (informative) |
| [RCE-168485](https://hackerone.com/reports/168485) | IRCCloud | outdated nginx 1.4.6 CVE theory, no PoC | $50 (list) |
| [RCE-194564](https://hackerone.com/reports/194564) | Nextcloud | SwiftMailer RCE research placeholder ("no exploitation yet") | - |
| [RCE-218342](https://hackerone.com/reports/218342) | Ruby | "RCE (Remote Code Execution) Vulnerability on Ruby" — junk title, no class | - (N/A) |
| [RCE-226896](https://hackerone.com/reports/226896) | Nextcloud | claimed exec() RCE; shown code carries escapeshellarg | - (N/A) |
| [RCE-244724](https://hackerone.com/reports/244724) | wakatime | unsafe-inline/unsafe-eval CSP best-practice | - |
| [RCE-257207](https://hackerone.com/reports/257207) | legalrobot | vague "Code injection" title | $40 (list) |

## 2. The joke, the junk, and the mislabel

**RCE-5499** is the corpus's running gag: a report against a program literally titled
MS-DOS, resolved without bounty, tagged Command Injection - Generic. It survives in the
roster because the mirror's title-arm matched it — the honest record of a lane's noise
floor. **RCE-218342** ("RCE (Remote Code Execution) Vulnerability on Ruby" against
program `ruby`, not-applicable) is the general-class-target junk row: an RCE claim with
no target, no trigger, no body substance — the N/A triage writes it for the reporter.

**RCE-146735** is the mislabel case: weakness tag Command Injection; body is content
spoofing. **RCE-34917** is the reflex claim: "bypassed tick box" + command-injection
implication, informative. Module-08 rows exist to keep the other modules clean — every
row here has a body-quote or a mechanical note in `references/case-register.md`, and the
playbook's P5 kill-gates cite them.

## 3. The theory row with $50 — RCE-168485

The one noise row with money: outdated nginx 1.4.6, heap-buffer-overflow CVE cited,
"potentially vulnerable", no PoC, resolved **$50 (list)**. Era lesson: unpatched-CVE
theory rows could *sometimes* squeeze a token bounty in 2016-2017 — the corpus shows it
plainly — but no version of this passes a modern triage (P5's kill-gate 4 exists
specifically for this row class).

**RCE-226896** is the reverse case: a claimed Nextcloud `exec()` RCE whose shown code
already contains `escapeshellarg($program)`; triage wrote not-applicable. Together with
**RCE-250587** (module 01, pattern-level PoC) and **RCE-131452** (CVE-list noise,
N/A), they are the playbook's "theory ≠ finding" exhibit shelf.

## 4. The $40 mystery row

RCE-257207 — "Code injection" as a whole title, `len=0` body, resolved, **$40 (list)**.
One of the strangest micro-bounties in the corpus; recorded as-is. Its class column
adjacent because nothing in the metadata demonstrates a class.

## 5. Cross-references

- RCE-194564's "research ongoing" placeholder is the honest-late-report artifact; the
  playbooks treat placeholder bodies as evidence of nothing.
- The cheatsheet reference for accepted-but-noise rows lives in the playbook's P5.
