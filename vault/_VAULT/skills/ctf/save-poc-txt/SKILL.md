---
name: save-poc-txt
description: Append solved-CTF-challenge step-by-step writeups to a single consolidated poc.txt file. Trigger phrases (often misspelled by the user) include "save the stpes", "save poc", "save solved challenges", and "FOR SOLVED CHALLNAGES PLEASE SAVE THE STPES TO in /desktop". Never overwrite — always append.
---

# save-poc-txt

Standing user instruction: for every SOLVED challenge, record the step-by-step
methodology in ONE file. Do NOT overwrite — always APPEND.

## Target file
`/home/user/Desktop/poc.txt`
- Note: there is no `/desktop` mount on this box; the real path is
  `/home/user/Desktop/poc.txt`. Write there. `write_file` auto-creates dirs.
- If the file does not exist yet, create it with a short header block, then the
  first challenge. If it exists, APPEND only.

## APPEND procedure (never overwrite)
1. Read the tail of the file (last ~20 lines) to find where it ends.
2. Use the `patch` tool in REPLACE mode to add a new challenge block AFTER the
   last existing block. Anchor on the final line of the file (e.g. the
   trailing `====...` separator or the last `STATUS OF OTHER` section).
3. Prepend the new block with a separator line and a `STATUS` update that
   moves the just-solved challenge out of the "NOT YET SOLVED" list if present.

## Block format for each solved challenge
```
------------------------------------------------------------------------
 CHALLENGE: <name>  — SOLVED
 Target:      <url>
 Flag:        <flag>
 Category:    <short vuln class>
------------------------------------------------------------------------
<vuln summary>
STEP-BY-STEP
  <numbered, copy-pasteable commands / code>
WHY IT WORKED
  <brief>
MITIGATION (if relevant)
```

## Rules
- Only append challenges that are ACTUALLY SOLVED (flag captured / verified).
- Do NOT append in-progress challenges. Keep a "STATUS OF OTHER CHALLENGES
  (NOT YET SOLVED)" note at the bottom listing still-open ones.
- Keep commands copy-pasteable; redact secrets as [REDACTED].
- Plain text / minimal markdown (terminal-renderable).
