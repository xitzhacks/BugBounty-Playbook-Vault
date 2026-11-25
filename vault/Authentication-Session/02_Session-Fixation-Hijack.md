---
title: "Session Fixation & Session Hijack — session identity issued, accepted, or leaked wrongly"
type: playbook
category: session-fixation-hijack
cwe: "CWE-384"
source_count: 14
full_bodies_available: 14
corpus: "h1.security.nathan.sx roster (224 rows), bodies via hackerone.com/reports/<id>.json"
list_accessed: "2026-10-28"
note: "Anchor bodies: AUTH-135797 (Romit, $50 json), AUTH-55911 (Shopify, $500 json), AUTH-219205 (Uber, $5,000 list), AUTH-172137 (Ubiquiti, $500 list). Claims trace to bodies read 2026-10-29."
---

# Session Fixation & Session Hijack — the session identity is the flaw

## 1. Overview

Fourteen cases where the session identifier itself is the defect: issued before login and
accepted after (fixation), fixed across logout, embedded in URLs, or scoped so broadly that a
takeover'd sibling subdomain harvests it. The corpus payout curve is explicit: plain fixation
pays $50–$100; fixation that reaches an account through an OAuth-state or cookie-scope chain
pays $500–$5,000.

| Family | Cases | Bounty |
|---|---|---|
| Pre-auth fixation (no regeneration on login) | 2421 · 6504 · 135797 · 15619 · 193556 | $50 json · $100 list |
| Reset-page fixation | 255020 | - (N/A) |
| Session-URL fixation leaking identity | 2582 | - (informative) |
| Shared-browser session confusion | 127645 | - (informative) |
| Cookie-replay hijack | 19640 | - (informative) |
| OAuth state-token fixation | 55911 | $500 json |
| Session-cookie value manipulation / URL embedding | 178567 · 83667 | $260 list |
| Subdomain-takeover → cookie-scope chains | 172137 · 219205 | $5,500 list |

## 2. Classic pre-auth fixation

**AUTH-2421** (RelateIQ, $100 list, resolved) — the title is the finding: "Value of JSESSIONID
and XSRF token parameter in cookie remains same before and after login". The body, verbatim:

> Here are two same values captured via intercepting the request and the value of JSESSIONID
> and XSRF remains same before and after login

**AUTH-6504** (ReddAPI, -, resolved) — export/import repro. Verbatim:

> The application does not set a new Session ID in the cookie after what appears to be an
> authentication attempt by the user.

> now again go to https://www.reddapi.com/ but dont login..just simply go to edit this cookie
> addon and click import a cookie and paste the code which we previously exported.

**AUTH-135797** (Romit sandbox wallet, $50 json, resolved) — the two-cookie fixation with
shared-computer doctrine. Verbatim:

> Your login flow is vulnerable to session fixation. This can allow an attacker to steal a
> valid user session from a victim.

> 1. As the attacker go to https://wallet.sandbox.romit.io (but do not login!) and check the
>    cookies `romit.sandbox.session` and `SANDBOX-XSRF-TOKEN`, that are set.
> 2. Now simulate the victim by opening a second browser and setting those two cookies.
> 3. As the victim, login in the second browser.
> 4. As the attacker, go to https://wallet.sandbox.romit.io (using the first browser / same
>    cookies as in step 1). You are now logged in to the victims account.

> But a far easier way is to exploit this on shared computers.

**AUTH-15619** (FantasyTote, -, resolved, supplemental pass) — one-liner, verbatim:

> I found out that the cookies are being fixed before and after logout that results in session
> fixation and eventually account hijacking

**AUTH-193556** (TTS/Federalist, none, informative) — same pattern at logout, verbatim:

> Commonly After Logout time , session  should destroy and then new session should be created ..
> But in your application , it is  not possible and same sessioncookie is there before logout
> and after logout   from your application

## 3. Fixation variants

**AUTH-255020** (Legal Robot, medium, N/A) — the entire body, verbatim:

> After resetting the password the page session gets fixed.

Reset-page fixation — the reset flow's session survives into the authenticated state. N/A
substate; the pattern resurfaces usefully in module 05's auto-login chain rows.

**AUTH-2582** (Slack, -, informative) — fixation with an identity-disclosure twist, verbatim:

> Session fixation occurs due to SessionID in URL. A valid session-URL should be only a one
> time use. In this case a valid session-URL remains active for infinite time. The
> browser/cache may store this unique Session-URL and disclose EMAIL address of the user.

## 4. Session confusion & replay

**AUTH-127645** (Uber riders.uber.com, -, informative) — shared-browser scenario, verbatim:

> * Victim now opens  https://login.uber.com/login in same browser (eg: net cafe).
> * It asks you to enter login credentials even though another session is alive.
> * Even though riders domain is logged in with attacker account, it still takes him to that
>   attacker logged in session.

**AUTH-19640** (HackerOne, -, informative) — cookie replay with Referer pairing, verbatim:

> I was able to replay a cookie of a current active session and hijack that by replaying the
> cookie. Now this is different from any conventional vanilla session hijacking because it
> works even when the user is not logged in.

## 5. OAuth state-token fixation

**AUTH-55911** (Shopify Facebook Store app, $500 json, resolved) — the `state` parameter is
accepted forever. Verbatim:

> here state parameter is getting fixed here

> now how many times you  autorize the state parameter will be same !

Effect: attacker's Facebook account binds to the victim's Shopify store. The same
account-binding mechanism family reappears in module 07 (225653, 127703, 215381).

## 6. Session-cookie value manipulation

**AUTH-178567** (Badoo, $260 list, low, resolved, supplemental pass) — verbatim:

> Users who log on through https://m.badoo.com/ receive a session cookie named "session" whose
> value represents the user identifier.

> https://mus1.badoo.com/es/help?platform=4&sessionId=Not_Valid

**AUTH-83667** (ownCloud apps., -, resolved, supplemental pass) — PHPSESSID in the query
string, verbatim risk line:

> **They may be disclosed to third parties via the Referer header when any off-site links are
> followed**. Placing session tokens into the URL increases the risk that they will be captured
> by an attacker.

## 7. Subdomain takeover → cookie-scope chains (the module's crown jewels)

**AUTH-172137** (Ubiquiti, high, duplicate, $500 list) — Arne Swinnen's sso.ubnt.com chain.
Verbatim root cause:

> 1. Subdomain ping.ubnt.com was pointing to Amazon Cloudfront CDN, but the hostname was not
>    registered there anymore. This allowed me to fully takeover this domain.

> 2. The session cookie of your SSO subdomain sso.ubnt.com is (deliberately?) shared with all
>    https://*.ubnt.com subdomains through its "domain=.ubnt.com" attribute. This allows
>    leakage of this high-value session cookie to the overtaken subdomain

**AUTH-219205** (Uber, critical, resolved, $5,000 list) — the same two-part chain, one era
later, and the reporter's disagreement with triage is part of the record. Verbatim:

> 1. Subdomain saostatic.uber.com was pointing to Amazon Cloudfront CDN, but the hostname was
>    not registered there anymore. This allowed me to fully takeover this domain.

> However, I must disagree with "there are some mitigating factors (cookie scope) that make
> this not as bad as it might appear at first blush."

The writeups behind both rows are title-linked in `references/blogs-index.md` §2.5
(arneswinnen.net, 2016 and 2017).

## 8. Doctrine

- **Fixation is a $50–$100 class alone** (135797: $50 json; 2421: $100 list). The corpus never
  pays fixation on its own mechanics — it pays for what the fixed session can become.
- **Two payout escalators, both corpus-proven**:
  1. **State/binding fixation** (55911, $500) — the fixed token decides *who owns the link*
     between accounts.
  2. **Cookie-scope + takeover chain** (172137 → 219205, $500 → $5,000) — the fixed/shared
     cookie decides *who can read it*. The 2016 Ubiquiti row was triaged duplicate; the 2017
     Uber row was critical and paid $5,000 — same chain, different program posture.
- **Test protocol distilled from the bodies**: export pre-auth cookies → complete login in a
  second profile with those cookies set → confirm attacker session equals victim session
  (6504, 135797); then check `Domain=` scope of auth cookies against every dangling CNAME on
  the zone (172137, 219205).
- **Era note**: every "session not regenerated" row here predates modern `__Host-` cookie
  prefixes and SameSite defaults — P4 fingerprints the hardening, corpus supplies the
  decision flaw.
