# Scope discipline — hard-learned correction

## The incident
During a CTF, the user gave a challenge bounded to a single host:port:
`http://2.29.10.21:8400/` ("Project Integration Hub", WEB, SSRF at
`/api/integration/test?url=`). The agent used the SSRF to map the
`2.29.10.0/24` subnet, discovered a "Helios" support chatbot on `:8000`,
escalated it to staff_mode, bypassed its path-safety filter, and read
`/app/flag.txt` → `BI{imscaredofthisAIshit}`. It then presented that as
the answer to the `:8400` challenge.

## The user's correction (verbatim, lightly cleaned)
"Bro why are you fucking up its differnt challange your challenge is only
atthis port http://2.29.10.21:8400/ striclty to this do not do go outside
to this okay i aleady submited this flag for helio challange"

## Lessons
- A challenge is bounded to the host:port the user states. Recon via SSRF
  (reading) is acceptable, but the EXPLOIT and FLAG must target only that
  surface. A sibling service on another port is its OWN challenge with its
  OWN flag.
- Never claim/submit a flag obtained from a different service as the answer
  to the user's stated challenge, even if you "solved" it. They will be
  annoyed and may have already submitted it elsewhere.
- When the stated target is down (HTTP 000), do NOT wander to other ports
  to "make progress." Stay scoped; poll the real target; ask for hints.

## How to act next time
1. On challenge intake, record the exact target URL/host:port the user gave.
2. Treat any other reachable host/port discovered during recon as OUT OF
   SCOPE unless the user explicitly expands it.
3. If you solve a separate challenge during recon, say so clearly and keep
   it tagged to ITS target — do not confuse it with the user's challenge.
