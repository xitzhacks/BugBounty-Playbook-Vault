---
title: "Host/Referer-Controlled Redirects — server-generated redirects from attacker-controlled headers"
type: playbook
category: host-referer-controlled-redirects
cwe: "CWE-601"
source_count: 6
full_bodies_available: 6
corpus: "h1.security.nathan.sx roster (198 rows), bodies via hackerone.com/reports/<id>.json"
list_accessed: "2026-10-28"
note: "Anchor bodies: RDIR-7357 (IRCCloud, $100 json), RDIR-210875 (Rockstar rsg.ms short-link poisoning, $300 list). Claims trace to bodies read 2026-10-29."
---

# Host/Referer-Controlled Redirects — no parameter needed

## 1. Overview

Six cases: the redirect comes from a **request header** (Host, Referer) that the server trusts
when it builds redirect targets. No parameter in the URL at all — which is why these evade every
param-focused scan and why they read as "misconfig" until you show the redirect.

| Mechanism | Cases |
|---|---|
| Host header echoed into redirect Location | 7357, 94637, 158019, 157465 (NA) |
| Referer validated/echoed into redirect | 5199 |
| Host header baked into generated short links | 210875 |

## 2. The anchor — RDIR-7357 (IRCCloud, $100 json)

> Please see the attached screenshot where I am sending a request to irccloud.com with an invalid
> HOST header and I am getting redirected to that domain. This is because the HOST header is not
> validated to ensure that the request is originating from that target host or not.

The body then carries both classic escalation frames, verbatim:

> For the first way, it can be exploited by poisoning a cache with the attacker's domain and then
> serving that poisoned response to legitimate users, causing them to redirect to the attacker's
> domain. This attack kind of varies depending on different web servers as they interpret duplicate
> Host headers in different ways.

> For the second way, I verified that the password reset functionality on the IRC Cloud website
> does not retrieve the Host header when sending emails. But, validating the Host header is always
> a good practice.

Agent lessons:

1. **Report the redirect, test the channels anyway.** The reporter verified password-reset
   *didn't* use Host — the honest negative result is in the body. Report scope: redirect +
   cache-poisoning frame.
2. Host-header redirects are usually proxy-rewrite artifacts (IRCCloud: Cloudflare `chk_jschl`
   era patterns) — name the hop when you can.
3. Duplicate-Host handling differences between web servers are part of the finding (the body
   cites the skeletonscribe practical-host-header-attacks piece).

## 3. The rest of the lane

- **RDIR-94637 (whisper.sh, $30 json)** — Host: crowdshield.com → `301 Location:
  https://crowdshield.com/`; the body's honest framing:
  > Attack vectors are somewhat limited but depends on how the host header is used by the
  > back-end application code. If code references the hostname used in the URL such as password
  > reset pages, an attacker could spoof the host header of the request in order to trick the
  > application to forwarding the password reset email to the attackers domain instead, etc.
  > Every major commercial web application scanner like Accunetix will report this same
  > vulnerability. (sic — Accunetix)
- **RDIR-158019 (instacart.com, $150 list)** — Host: google.com → `301 Location:
  https://google.com/`; same acunetix-cited framing; resolved.
- **RDIR-157465 (gratipay)** — same template text; **not-applicable** disposition. The copy-paste
  scanner-report shape of these three bodies (identical phrasing across whisper/instacart/gratipay)
  is itself a triage signal: value comes from *what the Host actually feeds* (links, emails,
  caches), not the echo.
- **RDIR-5199 (coinbase, informative)** — Referer-based redirect on the Cloudflare challenge path:
  > GET /cdn-cgi/l/chk_jschl HTTP/1.1
  > Host: coinbase.com
  > Referer: http://attacker.com
  > Notice the attacker's domain in the Referrer header. This value is not being validated on the
  > server side and as a result, the user is redirected to http://www.attacker.com
- **RDIR-210875 (Rockstar Social Club, $300 list)** — the paying variant: the Host lands in a
  **generated short link** (`rsg.ms/...`) that later redirects other users:
  > GET /feed/102126489/activity/2960911889698885091/share/Person/getcontent?_=1488725310707 HTTP/1.1
  > Host: socialclub.rockstargames.com.this.is.my.domain.evil.net
  > and it resulted in creating `http://rsg.ms/5350b75` if you visited it , you would be
  > redirected to
  > `https://socialclub.rockstargames.com.this.is.my.domain.evil.net/member/xerojuzto/feed/2960911889698885091`
  > #Consequences
  > 1- Phishing attacks
  > 2- Open redirects
  > 3- Cache poisoning and password reset leakage (Limited)

## 4. Agent execution template

```text
P0 — sweep: for every 30x the target emits, replay with Host: evil.com and Referer: https://evil.com.
     curl -s -D- -o /dev/null -H "Host: evil.com" https://target/ --resolve target:443:IP
     (or use a proxy that keeps SNI/Host split)
P1 — classify the Location source: rewrite-rule (nginx/bigip), app code, framework base-URL.
P2 — escalation channels, each tested not claimed:
     1. password-reset email links (receive the mail yourself)
     2. cache: does any cache sit in front? (duplicate-Host probes)
     3. generated links/shorteners that persist (the 210875 shape)
P3 — report: echo + one demonstrated channel. NA-rate honestly if no channel fires.
```

## 5. Validation gates

1. Location generated from the attacker header — two raw requests (legit Host vs evil Host) side
   by side.
2. A channel demonstrated for severity > Low (persisting short link > one-shot echo).
3. Negative results recorded in-report (7357's password-reset check is the model).

## 6. Adjacency

- Full Host-header doctrine (password-reset poisoning, cache poisoning as primary impact) is the
  master list row 24 vault — this module holds the redirect-shaped instances only.
- 210875 crosses into `../` cache-poisoning (row 15) territory; register keeps it here because the
  paid impact was the redirect.

## 7. Archive-label honesty

- 3 json ($100, $30, + none), 2 list ($150, $300), 1 NA. The identical phrasing across 94637,
  158019, 157465 suggests shared scanner-tooling origin; noted, not hidden.
- Severity ratings all low-or-none — the module's value is the escalation-channel checklist.

## 8. Cross-references

- Module 01 (suffix-join family — same trust-the-prefix psychology), master row 24 (Host-header
  vault, future), `../CSRF/05_Validation-Gaps-and-Bypasses.md` (referer-check class).
