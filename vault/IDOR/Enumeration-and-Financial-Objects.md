---
title: "Enumeration & Financial-Object Access Control"
type: playbook
category: enum
cwe: "CWE-204 (Observable Response Discrepancy), CWE-200, CWE-639"
case_ids: "IDOR-040, IDOR-068, IDOR-045, IDOR-052, IDOR-057-part, Activation/Veri-ENUM-adjacent 9 reports"
sources: "10 H1 reports"
evidence_split: "10 cases: full 6, summary 4"
archive_accessed: "2026-10-16"
---

# Enumeration & Financial-Object Access Control

## 1. Overview

Classical IDOR testing assumes the tester *knows* the object to target. This playbook records the
complementary class: **enumeration** — the tester can *discover* references in one of two ways:

1. **Response-envelope enumeration**: a check validates object X and returns a different
   response-body based on whether X exists, is registered, has a subscription, or has a first
   time.
2. **Financial-value enumeration**: where access control is intact for *data*, the object's
   *validity* has to be *tested against user money*; the tester can enforce that some ID is
   *valid* even without fetching its data. Specifically for cards, PINs, gift codes, or account
   balance.

Also captured: **rate limiting is the only defense against enumeration** — without rate limits,
the tester can run the entire space. Exploitation at scale has long been a specific issue in
modern, financial application design.

## 2. Case studies (verbatim)

### 2.1 IDOR-040 — Starbucks: card & PIN enumeration (full — the canonical case)

Full body:
> "**Card Enumeration:** In a POST request to the above
> https://www.starbucks.com/account/card/addcard URL, if an attacker sets the `Register.MyCard`
> attribute to **"FALSE"** they can enumerate the 16-digit Card Number without limits."

> "Another important note is all Starbucks locations have unactivated cards at their registers.
> It is highly possible for a threat actor to obtain a 16-digit card number from the next card in
> line, and sit on the account until it has been loaded up. Furthermore, in my research I've
> discovered **each card only increments a singular digit in their 16-digit number**. Because of
> this, a threat actor can easily discern which cards are about to be purchased, as well as which
> cards have been recently purchased."

> "**PIN Enumeration:** In a POST request to the second
> https://www.starbucks.com/account/card/Balance URL, an attacker can check the PIN of a card
> they've already added via the previous /addcard Card Enumeration method.
> If an attacker already knows the 16-digit card number ..., **if an attacker sets the
> `Register.MyCard` attribute to "TRUE"** they can enumerate the 8-digit PIN number without
> limits."

The flow: enumerate **card**, then enumerate **PIN**, both via *the same POST endpoint with a
parameter toggle* (Register.MyCard FALSE then TRUE). Report's own remediation:
> "My recommendation is to **add velocity checks to both the /addcard and /Balance pages when
> attempting to add a Starbucks gift card**. Additionally, CAPTCHA can be used as another
> authorization process."

**No bounty disclosed.** The flaw class here is *rate limiting as the sole security mechanism*.

### 2.2 IDOR-068 — Twitter ($420): composing tweets under another account's name

Full body:
> "When the Ads & Analytics feature is enabled in a user account, navigate to
> `https://ads.twitter.com/accounts/<redacted>/account_users.` ... the account owner is
> `abtest67` and this owner is assigning the role of `Ad Manager` with the **ability to compose
> promoted tweets** to the user `abtest66`."

> "It was observed that **this can be bypassed** by **removing the POST parameter
> `nullcast_flag=1`** in the request to the URL
> `https://ads.twitter.com/accounts/<redacted>/tweet_box/create_tweet?format=json`"

> "But, if in the above request, the parameter `nullcast_flag=1` is removed and the request
> re-sent ..., `abtest66` is able to actually **tweet** on behalf of `abtest67`. This is no
> longer just a **promoted** tweet."

**Bounty: $420.** Two flags: `nullcast_flag=1` is called by one client and not by a secondary
client; the server read that flag as *authorization*. One-parameter gate skip is a common
client/server disagreement.

### 2.3 IDOR-045 — Veris: delete any member of any organization (member enumeration cross-tenant)

Recorded for the *object-level authorization flaw* — see the cross-tenant playbook; here we
capture that **deletion of a *membership relationship*** is a *destructive* cross-tenant action
and includes an enumeration surface (it can be run repeatedly).

### 2.4 Uber — card/PIN-adjacent ratings (IDOR-052, IDOR-057-part)

Uber's **invoice** case (IDOR-041) illustrates "UUID-enumeration-confirmed" — see ID-Scoping
playbook. The Veris **`terminal`**-ID family showed numeric id enumeration that let a single
tenant's principal read+write *every* tenant's terminal details (IDOR-049..056). Highlights:
- **IDOR-052** — "Authentication Details of any Terminal/Gatekeeper" (the report logs that this
  is admin-only, yet testable via parameterization).
- **IDOR-057-part** — the tester labels "reset password" a data action; IDOR is on *"any
  account"* directly.

## 3. Method notes (from the case studies)

1. **The gcd indicator slot**: one variable + one feature* really makes all the difference for
   the account-holder (verified in vimeo IDOR-059).
2. **Two features can differ in one byte** — changing `Register.MyCard` toggles
   *enumeration-success* on Starbucks; **that one toggle** unblocked a NEW attack path that
   *transfers all the funds* to the tester.
3. **Rate limiting** is a compensating control and needs actual enforcement —
   "CAPTCHA and velocity checks" both.
4. **NotFound → success animations** in card-code enters tests. Data-returning 200 responses
   distinguish "the card number is good" and "it wasn't".
5. **For an increment that changes only the final digit**, the tester's own sample-of-1 source
   code shows that a direct value difference constrains the code power.

## 4. Payload corpus (all official / reconstructed)

```http
# Starbucks-style two-toggle enumeration
POST /account/card/addcard    {Register.MyCard:false}   → enumerate card
POST /account/card/Balance    {Register.MyCard:true}    → enumerate PIN
# Twitter flag-removal bypass
POST /accounts/<id>/tweet_box/create_tweet   [remove nullcast_flag=1]
# Rate-limitless handler
POST /api/v1/lookup   {"card":"...incrementing..."}
```

## 5. Remediation

1. **Every lookup code must be both rate-limited AND router-verifying** — the Starbucks case is
   the canonical fail when the rate limit sits only on the "front" route.
2. **Two flags never control different authorization results**: a flag toggling
   *authorization-critical* behavior is dangerous. Distinguish *data display* from *access
   grant*.
3. **Card/PIN-like enumerations should be truly randomized** (16-digit from a cryptographic
   pool, not "next card in the register's ordering").
4. **Velocity checks must trigger escalation, not just a message**; per-check interval, per-IP,
   per-account, with phone-number confirmation for financial operations.

## 6. Sources (verbatim)

| Case ID | Report | Evidence | Team | Weakness (assigned) | Title |
| --- | --- | --- | --- | --- | --- |
| IDOR-040 | [198494](https://hackerone.com/reports/198494) | full | starbucks | (none) | Card and PIN Enumeration Leading to Fraud |
| IDOR-068 | [31082](https://hackerone.com/reports/31082) | full | x | Violation of Secure Design Principles | Unauthorized Tweeting on behalf of Account Owners $420 |
| IDOR-045 | [120115](https://hackerone.com/reports/120115) | full | veris | Privilege Escalation | Deleting any member of any organization |
| IDOR-052 | [120293](https://hackerone.com/reports/120293) | full | veris | Privilege Escalation | Authentication details of any terminal |
| IDOR-057 | [42587](https://hackerone.com/reports/42587) | full | vimeo | Improper Authentication | IDOR reset password |
