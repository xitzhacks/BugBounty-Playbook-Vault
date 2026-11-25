---
title: "OTP / 2FA / Reset-Token — brute-forcing the short code"
type: playbook
category: rate-limiting-otp
cwe: "CWE-307"
source_count: 11
full_bodies_available: 11
corpus: "h1-brain disclosed_reports.db (3,673 rows) · sha256 8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4"
list_accessed: "2026-11-07"
note: "Anchors: RATE-1406495 (Shopify owner login DoS, $900), RATE-1987062 (Nextcloud reset endpoint, $500), RATE-1394984 (Evernote 2FA code, $150)."
---

# OTP / 2FA / Reset-Token

## 1. Overview

Eleven rows, **$1,740/5 paid**. The class's premise is arithmetic: a 6-digit OTP is 10⁶ guesses, a
4-digit PIN is 10⁴. If the endpoint accepts guesses without a per-*code* counter, the code is a
formality. Note that the corpus's most expensive row here is not brute force at all — it is a
*lockout DoS*.

**Case-stock (11 rows / $1,740):**

| Case | Target | Mechanism | Bounty |
|---|---|---|---|
| [RATE-1406495](https://hackerone.com/reports/1406495) | shopify | Spray wrong passwords → lock any owner out for 24h | **$900** |
| [RATE-1987062](https://hackerone.com/reports/1987062) | nextcloud | Lost-password endpoint annotated everywhere except the one that matters | **$500** |
| [RATE-1394984](https://hackerone.com/reports/1394984) | evernote | 6-digit email confirmation brute-forced during 2FA setup | **$150** |
| [RATE-1691195](https://hackerone.com/reports/1691195) | nextcloud | Password-reset email flood (IP rotation) | $100 |
| [RATE-2245437](https://hackerone.com/reports/2245437) | — | (see register) | — |
| RATE-121696, RATE-158157, RATE-174668, RATE-271533, RATE-332632, RATE-751604, RATE-766578 | see register | OTP/reset variants | - |

## 2. The lockout DoS that paid $900

RATE-1406495 inverts the class: no guessing is needed, only patience and a victim email.

> I Found a Bug in which Hacker Have Ability to Disable the Login Attempt of any Shopify Owner With (Zero_Click)

Impact framing: availability of the account owner's login, not credential compromise. That is why it
priced above the brute-force rows.

## 3. "Protected everywhere except the endpoint that matters"

RATE-1987062 is the most instructive sentence in the module — it is how these bugs are born:

> In any case. The whole lostpassword flow is now annotated with bruteforce protection. Except the endpoint that actually matters.

Look for the asymmetry: the UI flow has throttling; the API endpoint it calls does not. Enumerate
the API behind every reset/OTP screen.

## 4. Short-code arithmetic, stated plainly

RATE-1394984:

> The confirmationCode is used for authentication of user's email and it can be brute forced. The code is only 6 digits long ,so it will not take much time to crack .

A report that shows the code length *and* the missing counter passes triage immediately. Add the
request rate you sustained (RATE-385381's "1k+ request but still server not block my request" is the
model).

## 5. What pays, what doesn't

- **Paid**: a demonstrable takeover path (2FA set-up code, reset token) or a lockout that affects
  another user.
- **Weak**: "no captcha" without an attempted rate; OTP length complaints when the endpoint does
  throttle (state the observed threshold).
- Always bisect the throttle: find the exact attempt count where blocking begins, and whether it
  keys on the code, the account, or the IP.

## 6. Cross-references

- `02_Login-Password-Gates.md` — password brute force without codes.
- `03_Throttle-Bypass-Vectors.md` — how the counter is defeated (XFF, IPv6, case).
- `../Authentication-Session/` — 2FA bypass by other means.
