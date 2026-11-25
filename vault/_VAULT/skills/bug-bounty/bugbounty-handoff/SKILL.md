---
name: bugbounty-handoff
description: Bug bounty and pentest engagement handoff convention for this user. At the end of any multi-step assessment, write a single dated MASTER file so a future session can read ONE file instead of many. Use when the user says create a file with todays work, save everything, or after finishing a large recon/assessment chunk. Also covers cross-engagement daily logging and the one-file-to-resume pattern.
---

# Bug Bounty / Pentest Handoff — Consolidated Daily MASTER File

This user repeatedly asks for a single consolidated file containing the day's work,
dated with date AND time, so future sessions do not have to re-read every report.
Treat it as the primary handoff artifact. It is the antidote to "I had to dig through
all the files to understand what we did."

## When to create / update
- End of any multi-step bug bounty / red-team / pentest / mobile-assessment session.
- Whenever the user says: "create a file with today's work", "save it so I don't have
  to read everything", "make a master file", "save file with today date and time", or
  any variant. Take this seriously — the user values it highly.
- If a MASTER file for today already exists, UPDATE it (append / revise) rather than
  creating a second one with a new timestamp. One file per day, not per hour.

## Naming & location
- Filename: `MASTER_YYYY-MM-DD_HH-MM-SS.md`
  Generate the stamp with: `date "+%Y-%m-%d_%H-%M-%S"`
- Location: the engagement root (e.g. `~/Bugbounty/<target>/`) for single-target
  days, or `~/Bugbounty/` for days spanning multiple engagements.

## Required sections (make it self-contained)
1. Engagements active today (name, scope, current status).
2. Per-engagement summary: scope, what was done, findings WITH severity, key facts,
   verified-safe items, blocked items, pending decisions.
3. Skills created / updated today (name + absolute path).
4. Quick reference: absolute paths to all key files + a one-line status string a
   future session can paste to resume instantly.
5. Next steps (dynamic phase, tooling pending, etc.).

## Rules
- The MASTER is an INDEX + SUMMARY, not a replacement for depth. Per-target detailed
  reports still live in their own files; MASTER points to them.
- Include REAL values / results, not placeholders. A future session must be able to
  act from this file alone.
- Do NOT save out-of-program secrets / API keys into the MASTER (per the Google Maps
  key episode — the user explicitly said not to save it). Reference by project number
  or [REDACTED] and note "not part of program".
- Keep it plain-text friendly (terminal-renderable); minimal markdown decoration.

## Why this exists
User trigger (verbatim, typos preserved): "Creat a file which contain today all work
informwaiton so taht next tiem donot have to go through all file read and all jus see
the ine fiel and got the answer and understand save file with Today data and time name
tha you can use for persist info"
