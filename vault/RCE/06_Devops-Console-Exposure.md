---
title: "Devops-console exposure — Jenkins class: the $15,000 panel, auth-flow consoles, source disclosure"
type: playbook
category: devops-console-exposure
cwe: "CWE-732"
source_count: 4
full_bodies_available: 1
corpus: "h1.security.nathan.sx roster (150 rows), bodies via hackerone.com/reports/<id>.json"
list_accessed: "2026-11-04"
note: "Anchors: RCE-231460 (Open prod Jenkins, $15,000 json — body absent), RCE-258117 ($5,000 list, body absent, cross-ref AUTH vault). Claims trace to bodies read 2026-11-04."
---

# Devops-console exposure — the console *is* the RCE primitive

## 1. Overview

Four rows, **$20,300/3 paid** — third-highest module total in the build, from essentially
one read body. The lesson: in the 2016-2017 era, unauthenticated or auth-bypassed build
/devops consoles were priced at RCE-class severity whether or not the reporter attached
a script-console screenshot. Three of four bodies are empty (`len=0`) — the module is
carried by title + severity + bounty discipline, exactly the metadata-only handling
source-index §7 records.

**Case-stock (4 rows / $20,300):**

| Case | Target | Mechanism | Bounty |
|---|---|---|---|
| [RCE-231460](https://hackerone.com/reports/231460) | snapchat | Open prod Jenkins instance | $15,000 (json), sev high |
| [RCE-258117](https://hackerone.com/reports/258117) | snapchat | RCE/LFI on test Jenkins via improper auth flow | $5,000 (list) |
| [RCE-182104](https://hackerone.com/reports/182104) | Udemy | exposed Jenkins (GitHub SSO) → source + creds + Sendgrid takeover | $300 (list), sev high |
| [RCE-167859](https://hackerone.com/reports/167859) | eternal | base alpha version code exposure | - |

## 2. The $15,000 row: what an exposed console is priced at

RCE-231460 — fourth-largest single figure in the whole ledger (behind two $20,000 rows
and the mruby $18,000; the largest console-lane figure) — is a **metadata-only row**: title "Open prod Jenkins instance",
`sev=high`, `bounty_amount=15000.0`, weakness tagged Information Disclosure, body absent.
No quotes exist and none are invented. What the corpus proves here is the *pricing*:
an unauthenticated production Jenkins panel in 2017 — a console whose script-console tab
is a Java code-execution primitive waiting for a click — sold at $15,000 with the
weakness tag filed under disclosure. That is the era's real-world RCE-price for a
*potential*, not proven, execution: exposure of the primitive was the bounty.

## 3. The auth-flow console: RCE-258117 and the auth vault overlap

RCE-258117 (test Jenkins, `sev=medium`, **$5,000 (list)**) — metadata-only, titled
"RCE/LFI on test Jenkins instance due to improper authentication flow". The mechanism is
the auth-lane bug (flow bypass) delivering a console; classing doctrine (originator
owns the class) would put it in the auth vault — and a companion Authentication-Session
build does cross-reference this row — but the console lane belongs to this module as
the delivery shelf. The pairing with module 03's RCE-98559 (same Jenkins tool, deser
lane, unpaid) shows two eras of the same console: 2015 wanted the *bug* shown
(Jenkins-deser), 2017 paid for the *door being open*.

## 4. The Udemy row: exposure → compromise chain

RCE-182104 (sev high, **$300 (list)**), the only body in the module, reads as a
completed-compromise claim: exposed Jenkins dashboard, source code disclosure, internal
credentials, third-party (Sendgrid) takeover potential. Its title says "Completed
Compromise & Source Code Disclosure" — the RCE-class framing rides the console's script
surface, and the bounty shows the panel-priced tier ($300) rather than the $5k-$15k of
cleaner-console rows. Honest note from the read: the visible body demonstrates exposure
and credential spill; the execution claim rides on what an exposed Jenkins implies.

## 5. What pays, what doesn't

- Jenkins exposure rows paid **$300 / $5,000 / $15,000** — a three-fold spread by year and program tier; the corpus cannot decompose the pricing further (two bodies
  absent), only record it.
- The unpaid row, RCE-167859 ("Base alpha version code exposure"), is exposure without a
  console — source/disclosure class, not execution-adjacent.
- Modern echo (P4): exposed console lanes today are auto-triaged as P1 on most programs —
  the era's $300 row would be the .git/$$$ class of blogs-index §2.5d. The corpus's
  generous-but-inconsistent console pricing is itself the era lesson.

## 6. Cross-references

- Module 03 holds the Jenkins Java-deser row (RCE-98559): same console, bug-owned lane.
- RCE-258117 cross-references the Authentication-Session vault's improper-auth-flow lane.
- Module 07's RCE-224198 (Sidekiq queue → `instance_eval`) is the same trust-boundary
  shape one layer deeper (job queue instead of console).
