---
title: "Throttle Bypass Vectors — X-Forwarded-For, IPv6 subnets, IP rotation, case tricks"
type: playbook
category: rate-limiting-bypass
cwe: "CWE-307, CWE-348"
source_count: 10
full_bodies_available: 10
corpus: "h1-brain disclosed_reports.db (3,673 rows) · sha256 8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4"
list_accessed: "2026-11-07"
note: "Anchors: RATE-1363672 (Shopify Storefront bypass of a prior fix, $3,500 — vault max), RATE-165727 (Slack iOS login, $500), RATE-819930 (MoPub IP change, $420), RATE-2627062 (Acronis XFF)."
---

# Throttle Bypass Vectors

## 1. Overview

Ten rows, **$4,770/5 paid**. This module is the answer to "the endpoint does throttle": the counter
is keyed on something the attacker controls. The corpus's largest rate-limiting payout lives here —
a *bypass of a fix* for an earlier report.

**Case-stock (10 rows / $4,770):**

| Case | Target | Vector | Bounty |
|---|---|---|---|
| [RATE-1363672](https://hackerone.com/reports/1363672) | shopify | Second Storefront mutation still unthrottled after the #708013 fix | **$3,500** |
| [RATE-165727](https://hackerone.com/reports/165727) | slack | Web has a limit; the mobile `/api/auth.signin` does not | **$500** |
| [RATE-819930](https://hackerone.com/reports/819930) | x (MoPub) | Counter keyed on IP → rotate IP | **$420** |
| [RATE-2627062](https://hackerone.com/reports/2627062) | acronis | `X-Forwarded-For` spoofing | **$250** |
| [RATE-1691195](https://hackerone.com/reports/1691195) | nextcloud | "IP rotate extension of burp suite" | $100 |
| [RATE-225897](https://hackerone.com/reports/225897) | dashlane | `X-Forwarded-For` on `ws1.dashlane.com` | - |
| [RATE-507012](https://hackerone.com/reports/507012) | unikrn | Cloudflare Access bypass on CRM login | - |
| [RATE-1065186](https://hackerone.com/reports/1065186) | reddit | Limit returns an error but still authenticates | - |
| [RATE-1154003](https://hackerone.com/reports/1154003) | nextcloud | IPv6 /128 hardcode vs /48 allocations | - |
| [RATE-2230915](https://hackerone.com/reports/2230915) | nextcloud | `getRemoteAddress()` trusts proxy headers | - |

## 2. Bypassing a fix is worth more than the original finding

RATE-1363672's summary is the whole lesson:

> `customerAccessTokenCreate` mutation in the Storefront API does not correctly throttle login attempts. An issue in similar report https://hackerone.com/reports/708013 was already fixed, however, there is still a bypass.

Six months after the first fix, a different mutation in the same API was unthrottled — and paid
$3,500. Always re-test sibling endpoints after a fix.

## 3. Per-surface inconsistency

RATE-165727:

> On Slack Web Application there is rate limit implemented. After performing 4-6 failed 2FA Attempt, Rate limit logic will ge Triaged and ask user to wait for next attempt(preventing automated 2FA Attempts)

> I tested the same using iOS App(iOS 9.3.3 iPad Air 2) and found that API Endpoint "/api/auth.signin" have no rate limit implemented.

Mobile APIs, GraphQL mutations, and legacy endpoints are the usual gaps.

## 4. Attacker-controlled keys

- **IP**: RATE-819930's phrasing is the classic —
  > I sent out nearly 1,000 requests, and I was virtually banned on request about 120. But when I changed my IP and tried logging in, I was logged into the account without any additional checks
- **Header**: `X-Forwarded-For` (RATE-225897, RATE-2627062) — the counter keys on a client-supplied
  value.
- **IPv6 subnet math**: RATE-1154003 —
  > Nextcloud hardcodes IPv6 subnets to /128. End users get at least a /64 subnet (more than the whole IPv4 address space!), most providers assign even larger subnets like /48.
- **Proxy-header trust**: RATE-2230915 — `getRemoteAddress()` reads `REMOTE_ADDR`/trusted proxies, so
  any accepted forwarding header moves the counter.
- **Third-party gate**: RATE-507012 — Cloudflare Access in front, application login behind; the
  gate is the thing to bypass.

## 5. The inversion row

RATE-1065186 deserves its own line: the rate limit *fires* but does not stop the request.

> Although the server sends a message when attempting to brute force the login endpoint, if you enter the right credentials the server will ignore that error and will give access to the account.

Always send the correct password *after* the limit engages. Some implementations only decorate the
response.

## 6. What pays, what doesn't

- **Paid**: a demonstrated bypass of an *existing* protection (the corpus's $3,500 and $500 rows).
- **Weak**: spoofing a header that the server ignores — verify the counter actually moved by watching
  the block threshold.
- Method: pick a known-blocked state, then vary exactly one input (header, IP, path case, HTTP
  version) until requests succeed again.

## 7. Cross-references

- `01_OTP-2FA-Reset-Token.md`, `02_Login-Password-Gates.md` — the targets being bypassed.
- `../18_Misconfiguration/` — proxy-header trust and forwarded-header handling.
- `../24_Host-Header-Injection/` — the header-spoofing family.
