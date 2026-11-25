---
title: "Adjacent & unclassified — enumeration, misfiled findings, and noise"
type: playbook
category: rate-limiting-adjacent
cwe: ""
source_count: 26
full_bodies_available: 26
corpus: "h1-brain disclosed_reports.db (3,673 rows) · sha256 8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4"
list_accessed: "2026-11-07"
note: "26 rows = 20 `_adjacent` + 6 `_adjacent_unclassified`. Top: RATE-982291 ($5,000, stored XSS — not this class), RATE-1394916 ($4,000, Apache 2.4.49 path traversal — not this class)."
---

# Adjacent & unclassified — what the rate-limit lane collects

## 1. Overview

Twenty-six rows, **$11,545/13 paid**. This module exists because keyword classifiers lie: the words
"rate limit" and "brute force" appear in reports about stored XSS, Apache CVEs, CSRF, path
traversal, and plain enumeration. Keeping them here, labeled, is the honest alternative to
deleting them.

**Case-stock (26 rows / $11,545 — top rows):**

| Case | What it actually is | Belongs to | Bounty |
|---|---|---|---|
| RATE-982291 | Stored XSS (HEY) | `../XSS/` | $5,000 |
| RATE-1394916 | Apache 2.4.49 path traversal/RCE | `../RCE/` | $4,000 |
| RATE-1024880 | Access-control/enumeration | `../IDOR/` | $1,900 |
| RATE-1592587 | Info disclosure | `../16_Information-Disclosure/` | $480 |
| RATE-834366, RATE-840598, RATE-840759, RATE-916704 | enumeration variants | this module (low value) | - |
| remainder (18 rows) | mixed CSRF/XSS/IDOR/traversal/service noise | see register | - |

## 2. The genuinely useful adjacent rows

The module is not pure noise: user/email enumeration without throttling is a real, reportable
finding when the program prices it. The corpus's enumeration rows cluster at $0–$500 and share one
shape — a distinct response (`"user not found"` vs. a timing/path difference) that the endpoint
serves at unlimited rate. Report it as *enumeration* with a measured request rate, not as
"no rate limit".

## 3. Why these rows matter to a worker

1. **Deduplication**: if you are about to submit "no rate limit on login", check whether the
   program has already resolved an enumeration report for that endpoint — the corpus shows both were
   filed and one was closed as informational.
2. **Classifier honesty**: this vault's own totals include $9,000 of money that is not rate-limiting.
   Totals are labeled; do not cite them as class value.
3. **Negative space**: the adjacent rows are the "kill-gate exhibits" for the playbook — the reports
   that looked like throttling and were not.

## 4. Cross-references

- `01`–`03` for the class itself.
- `../XSS/`, `../RCE/`, `../IDOR/`, `../16_Information-Disclosure/` for the misfiled rows.
