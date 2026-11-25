# Operator-consent pitfall — surgical enumeration over heavy scans

When the target is a single known app / CTF challenge / small scope, prefer CURATED
endpoint probing over a large ffuf wordlist brute.

## What happened
During the ch15 "Trust, but Never Verify" session, two full `ffuf` passes
(common.txt, then raft-medium-words) were fired at the target. The operator BLOCKED
both mid-run ("User denied this command"). Lesson: broad wordlist brute-forcing is not
wanted by default on these targets — confirm before launching, or skip it.

## Preferred approach on small/known targets
- Hand-pick a ~50-150 word list of likely route names:
  plan/flag/admin/premium/enterprise/account/dashboard/verify/upgrade/badge/api/secret/...
- Send each with the forged/auth cookie and the right method/body (not just status-code
  filters). This surfaced /premium/flag in one curated loop where ffuf was blocked.
- Reserve ffuf for: large multi-host recon, or after curated guesses are exhausted AND the
  operator has signed off.

## Why curated beats brute here
You control the request shape (JSON cookie, method, body, auth header), so the response is
semantically meaningful. A 50k-wordlist ffuf run only distinguishes by status/size and
burns the operator's patience + rate limits.

## Cross-ref
hunt-session Phase 9 — custom HMAC-signed session with unsigned trusted field uses exactly
this curated-route-discovery step to find the gated endpoint.

NOTE: this note belongs in the bug-bounty SKILL.md body under "Operator Notes", but the
body edit was blocked by a skill_manage frontmatter re-validation bug (the existing
description field exceeds the 1024-char limit the validator now enforces). Fold it into
the body once that is resolved.
