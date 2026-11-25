---
name: engagement-handoff
description: Cross-session engagement continuity for long-running bug-bounty or pentest work. Use when an engagement spans multiple sessions, when the user says "save everything to one file so I don't have to read all the others", or when starting a new session on a known target. Encodes the user's explicit preference for a single dated MASTER_<YYYY-MM-DD_HH-MM-SS>.md file at the engagement root that consolidates every sub-report, finding, scope note, and next step into one readable artifact, so a future session (or the user) gets full context from one read instead of digging through many per-task files.
---

# Engagement Handoff — Single Consolidated MASTER File

## When to use
- Engagement spans >1 session (bug bounty programs, multi-target pentests).
- User says things like "create a file with today date and time so you don't
  need to read everything", "save all work info in one file", "next time just
  see the one file and get the answer".
- Starting a session where a MASTER_*.md already exists for the target.

## The convention
At the END of a work session (or whenever the user asks), write ONE file:
```
<engagement-root>/MASTER_<YYYY-MM-DD_HH-MM-SS>.md
```
Get the timestamp with: `date "+%Y-%m-%d_%H-%M-%S"`

## What goes in the MASTER file
A self-contained snapshot — future reader should NOT need other files:
1. Header: engagement name, analyst, generated date/time, scope summary.
2. Active engagements section (if multiple) — one block each with:
   - scope / out-of-scope (critical for bug bounty)
   - status of each workstream (web, android, api, etc.)
   - confirmed findings (id, title, severity, one-line proof/context)
   - verified-safe items (so you don't re-test them)
   - pending / blocked items + why
3. Key facts that recur (e.g. a shared GCP project id, a key that appears in
   multiple targets, RAM/tooling constraints).
4. Skill list built this session.
5. QUICK REFERENCE block: copy-paste next-session status line + all key file
   paths + next-step checklist.

## Rules
- Date+time in the FILENAME (not just inside) — lets you keep history and
  always open the latest.
- Reference real sub-reports by absolute path for depth, but include the
  SUMMARY inline so the MASTER is readable alone.
- Don't just list file names — include the actual findings/decisions.
- If a prior MASTER exists, you may supersede it; keep the latest as source of
  truth. (Don't delete old ones — they're useful history.)

## Example layout for a bug-bounty folder
```
~/Bugbounty/line-works.com/
    MASTER_2026-08-18_00-25-45.md      <- read this first
    attack_surface/ENGAGEMENT_STATUS_*.md
    android/ANDROID_STATUS_*.md
    android/api_map/ENDPOINT_MAP.md
~/Bugbounty/issuehunt/Abeam/android/
    APK_SECURITY_REPORT.md
    work/apkleaks_report.txt
    MASTER_2026-08-18_01-22-11.md      <- cross-engagement master
```

## Pitfalls
- Don't write the master as ONLY a file index — that defeats the purpose; the
  user explicitly wants the ANSWERS in the one file, not pointers.
- Keep it terminal-readable (plain text, minimal markdown tables).
- Update it whenever a major finding lands, not only at session end — but always
  produce one at session close.
