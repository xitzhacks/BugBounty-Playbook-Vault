---
name: session-handoff
description: End-of-session consolidated master file for bug-bounty / security engagements. The user explicitly requires a single dated file containing ALL work (findings, status, file index, next steps) so the next session reads ONE file instead of digging through many. Use whenever wrapping up a task, completing an engagement phase, or the user says "create a file with today's date" / "so I don't have to read everything" / "save it with today's date and time name".
---

# Session Handoff — one master file per session

## The rule
When finishing work (or on user request), write a SINGLE consolidated file at the
engagement / target root:
```
<root>/MASTER_YYYY-MM-DD_HH-MM-SS.md
```
It must contain everything needed to resume cold: scope, what was done, findings
with severity, file index of deeper reports, blocked items, and next steps. The
user reads THIS one file next time — do not make them open 5 sub-reports.

## What to include
- Engagement/target identity + scope (in/out).
- Status line: what's done, what's blocked.
- Findings table (id, title, severity, status).
- File index: absolute paths of all sub-reports / tool outputs.
- Key facts / gotchas (e.g. a key that appears in two places; RAM limits).
- Next steps (dynamic phase, device needed, etc.).
- Quick-reference block (copy-paste next session).

## Why
User asked for this twice: "create a file with today date and time so you don't
need to read everything, just see the one file and get the answer." It is the
user's preferred persistence format — honour it every session, not optional.

## Variant — the user names the session ("save this chat as <Name>")

When the user says "save this chat with Building Vault name" (or any name), they want a readable
record of the *work*, not a transcript. Write it at `<project root>/<NAME>.md`
(e.g. `Vault/_VAULT/BUILDING-VAULT.md`) with frontmatter
`title / type: handoff / session_name / built: YYYY-MM-DD`, then:

1. Objective — one sentence.
2. What was built — table of step → verified result.
3. Numbers that matter — counts, totals, sizes, copied from the DB/tool output, never estimated.
4. Provenance / honesty rules kept — what is never claimed (delisted rows, blank bounties, guesses).
5. Where the code lives — absolute paths of the scripts.
6. How to pick this up later — copy-paste commands in order, ending with the verification step.
7. Open items — started but unfinished.

A named save does not replace the dated MASTER file for engagements: the named file is the
narrative, MASTER is the state. Cross-link them when both exist.

## Pitfalls
- Don't dump raw tool output; summarize. The file is for fast comprehension.
- Use the EXACT date-time filename format `MASTER_YYYY-MM-DD_HH-MM-SS.md` so it
  sorts and is findable.
- Keep it under the engagement root (e.g. ~/Bugbounty/...), NOT /tmp — it must
  survive session end.
- For multi-engagement days, one MASTER per engagement root is cleaner than a
  single mega-file; cross-link them.
