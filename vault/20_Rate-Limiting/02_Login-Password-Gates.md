---
title: "Login & Password Gates — brute force where the counter is missing"
type: playbook
category: rate-limiting-login
cwe: "CWE-307, CWE-521"
source_count: 17
full_bodies_available: 17
corpus: "h1-brain disclosed_reports.db (3,673 rows) · sha256 8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4"
list_accessed: "2026-11-07"
note: "Anchors: RATE-385381 (Chaturbate room passwords, $500), RATE-1435392 (Acronis login, $250), RATE-1392287 (current-password delete, $100), RATE-1192144 (Nextcloud, $100)."
---

# Login & Password Gates

## 1. Overview

Seventeen rows, **$1,050/5 paid**. The paid band is low ($100–$500) because most of these are
"login has no throttle" — a hygiene finding unless you convert it into a takeover story with a weak
password policy or a lockout side effect.

**Case-stock (17 rows / $1,050):**

| Case | Target | Mechanism | Bounty |
|---|---|---|---|
| [RATE-385381](https://hackerone.com/reports/385381) | chaturbate | `/roomlogin/user/` room password, 1k+ attempts unthrottled | **$500** |
| [RATE-1435392](https://hackerone.com/reports/1435392) | acronis | Login page without brute-force protection | **$250** |
| [RATE-1392287](https://hackerone.com/reports/1392287) | xvideos | Current-password check on delete-account unthrottled | **$100** |
| [RATE-1192144](https://hackerone.com/reports/1192144) | nextcloud | "Add to your Nextcloud" endpoint only throttles on the happy path | **$100** |
| [RATE-1192159](https://hackerone.com/reports/1192159) | nextcloud | (see register) | - |
| RATE-410451, RATE-411364, RATE-412526, RATE-708013, RATE-744692, RATE-790854, RATE-827484, RATE-1165225, RATE-1842114, RATE-1879549, RATE-2039447 | see register | login/brute-force variants | - |

## 2. "1k+ requests and still not blocked"

RATE-385381 is the clearest sustained-load proof in the module:

> I notice that rate limit are missing at the endpoint `/roomlogin/user/` which enable me to brute force on password field.

> I made 1k+ request but still server not block my request.

Numbers > adjectives: one thousand requests, no block, password field guessed. That is the report.

## 3. The gate nobody thinks of: current-password on destructive actions

RATE-1392287:

> This Attack happen when victim login in other device and forget to logout ,Then attacker can delete  it's account by brute force the current password because current password has no-rate limit.

Re-auth prompts (delete account, change email, disable 2FA, export data) are frequently unthrottled
even when the main login is protected — they are the best target in this module.

## 4. Partial protection is a finding

RATE-1192144 states the asymmetry precisely: the endpoint *does* have brute-force protection, but
only when a password-protected share is found first — so the enumeration path is free. Test both
branches of every endpoint: the "not found" branch is where the counter usually lives.

## 5. What pays, what doesn't

- **Paid**: sustained high-rate guessing against a real credential check, or a takeover chain
  (weak password policy + no throttle — RATE-1065186's 5-character minimum).
- **Weak**: a single 429 without a bypass attempt; CAPTCHA absence alone.
- State the exact endpoint, the request count, and the observed threshold (or its absence).

## 6. Cross-references

- `01_OTP-2FA-Reset-Token.md` — the code-based variants.
- `03_Throttle-Bypass-Vectors.md` — bypassing an existing counter.
- `../Authentication-Session/` — what success yields.
