---
title: "Core Authentication Bypass — the server accepts an attacker without proving identity"
type: playbook
category: core-auth-bypass
cwe: "CWE-287"
source_count: 17
full_bodies_available: 17
corpus: "h1.security.nathan.sx roster (224 rows), bodies via hackerone.com/reports/<id>.json"
list_accessed: "2026-10-28"
note: "Anchor bodies: AUTH-2224 (Phabricator, $1,000 json), AUTH-245408 (Zomato, $1,000 json), AUTH-136169 (Uber OneLogin, $10,000 json), AUTH-138869 (Uber XMLRPC, $7,000 json), AUTH-215053 (Ubiquiti, $6,000 list). Claims trace to bodies read 2026-10-29."
---

# Core Authentication Bypass — login without proving identity

## 1. Overview

Seventeen corpus cases where the server mints a session for an attacker. No CSRF, no token
theft — the authentication decision itself is wrong. Three payout patterns the corpus shows:
(a) **identity-trust shortcuts** (email-domain lists, single-attribute login) pay $500–$1,000
because they reach *any* account; (b) **SSO plugin auto-provisioning** paid $10,000/$8,000/$7,000
because it reached *admin* on production domains; (c) **feature-gated ticket auth** paid
$6,000/$1,000 at a program that pays for internal-surface reach.

| Family | Cases | Bounty |
|---|---|---|
| Email-domain trust bypass (Phabricator family) | 2224 · 2233 · 4795 | $1,500 json |
| Login with only an identity attribute | 245408 · 98247 · 121469 | $1,427 json · $300 list |
| Ticket/feature-gated auth bypass | 215053 · 116504 | $7,000 list |
| SSO plugin auto-provisioning (OneLogin/WordPress) | 136169 · 136885 · 138869 | $25,000 json |
| Hosted-domain / internal-app reach | 143482 · 194832 · 201152 · 187705 | $3,500 list |
| External auth backends (SMB) | 148151 | - |
| Authorization-error data exposure | 129918 | $2,000 json |

## 2. Email-domain trust bypass — the Phabricator `auth.email-domains` family

Phabricator lets a program restrict registration to `@company.com` addresses. Three corpus
rows break the check three ways, all without owning the domain.

**AUTH-2224** (Phabricator, $1,000 json, resolved) — length-truncation. The body, verbatim:

> Email addresses are stored as `VARCHAR(128)`. However, Phabricator does not verify the length
> of an email address upon registration. This allows attackers to bypass the allowed
> email-domains defined in `auth.email-domains`.

> Now register with your 128 character email address with `@allowed-domain.com` appended to it.
> The `@allowed-domain.com` part will be truncated because MySQL can’t store it, and you will
> receive a verification email on your 128 character email address.

**AUTH-2233** (Phabricator, $500 json, resolved) — the fix-rebreak. Verbatim:

> This vulnerability has the same effect as my previously reported bug [#2224 Bypass
> `auth.email`-domains](https://hackerone.com/reports/2224), but uses a very different approach,
> bypassing the current fix.

> To replicate, register an account with following address: `[REDACTED_EMAIL]𝌆@allowed-domain.com`.

Unicode code point > `0xFFFF` truncates a `utf8` column mid-string. Two eras, two truncation
tricks, one lesson: a domain check on an unsanitized identifier is decoration.

**AUTH-4795** (concrete5, -, resolved) — the same text-template reused against a `VARCHAR(64)`
column where "the length is verified on client side only". Third family row; the pattern had
already propagated through Phabricator-derived installs.

Modern counterpart (bibliography, post-2017): zseano's *@company.com* signup guide — quoted in
`references/blogs-index.md` §1b — lands the same identity-trust failure via claim-flow pivots.

## 3. Login with only an identity attribute

**AUTH-245408** (Zomato, $1,000 json, high, resolved) — the canonical single-attribute login.
The team summary quotes the reporter's stripping method, verbatim:

> After testing the login flow for the three different options: Facebook, Google and password
> based, I noticed that Google login looked slightly weird in the fact that a lot of data was
> send besides the Google OAuth token. Thus I started stripping parameters one by one after
> which I noticed that only the email of a user was required to login.

> Thus I could login as any user on Zomato given I knew their email address.

The wire, verbatim from the body:

> ```http
> POST /v2/auth.json?isGoogle=true HTTP/1.1
> X-API-Key: [REDACTED_SECRET]
> Content-Type: application/x-www-form-urlencoded
> Content-Length: 21
> Host: api.zomato.com
> Connection: close
>
> email=[REDACTED_EMAIL]
> ```

**AUTH-98247** (Binary.com, $300 list, resolved) — cashier iframe carries the session: the
`<iframe id="cashiercont">` embeds `login.asp?…&PIN=<account_id>&Password=<hash>&Secret=<hash>`
and swapping `PIN` to another account id logs the attacker into that cashier account.
Verbatim mechanism line:

> Edit the `<iframe>` element and Change the `PIN` parameter value to the victim account id value

**AUTH-121469** (Badoo, $427 json, resolved) — video-only: the body is
"Please watch the attached video." Recorded as-is; no mechanism is published.

## 4. Ticket/feature-gated auth bypass (Ubiquiti)

**AUTH-215053** (Ubiquiti, $6,000 list, critical, resolved) — airControl's "Open Web-UI" left
device ticket-auth bypassable. Verbatim conditions:

> This system had a flaw that allowed unauthenticated access without a valid ticket, given
> these requirements were met:
> 1. A device was monitored by airControl.
> 2. The "Open Web-UI" airControl feature was used on the device since last reboot.
> 3. Device wasn't rebooted after #2.

**AUTH-116504** (Ubiquiti, $1,000 list, resolved) — team summary, verbatim:

> The researcher (ebrietas) demonstrated that access to our Internal corporate directory could
> be gained due to a misconfiguration in Google OpenID.  This involved using a non-UBNT Google
> account and modification to the URL.

## 5. SSO plugin auto-provisioning — the $25,000 OneLogin/WordPress trio

**AUTH-136169** (Uber, $10,000 json, resolved) — verbatim:

> The *.uber.com WordPress sites use OneLogin SAML-SSO instead of the normal WordPress login.
> The WordPress plugin shipped by OneLogin has a bug which allows anyone to login without a
> password or other authentication.

> The attacker can supply a username, email adress, name, and a role. If the username doesn't
> already exist in the WordPress database, then the plugin will create a new user (if the
> provisioning setting is on, which it was on the two sites I tested).

Admin reach was a guess away, verbatim:

> On newsroom.uber.com the role name apparently was simply "administrator" so I got that
> privilege on the system.

**AUTH-138869** (Uber, $7,000 json, resolved) — the plugin's leftover credential. Verbatim:

> When a user logs on one of your WordPress sites via OneLogin, the authentication plugin
> creates a new entry in the WordPress user database with the default password `@@@nopass@@@`.

> The OneLogin plugin does prevent logins through the normal *wp-login.php* page but fails to
> restrict the XMLRPC API. XMLRPC still honors the WordPress internal user database.

**AUTH-136885** (Uber, $8,000 json, resolved) — the body is the team's acknowledgment only
("Thanks for another great find @parth!"); mechanism not published. Recorded, not reconstructed.

## 6. Hosted-domain / internal-app reach

**AUTH-143482** (Shopify, $3,000 list, resolved) — team summary, verbatim:

> An Icinga monitoring server, which was intended to be accessible only by Shopify employees,
> had Google OAuth misconfigured such that all Google accounts were accepted (regardless of
> whether they belonged to the `shopify.com` hosted domain or not).

**AUTH-194832** (Shopify, $500 list, low, resolved) — the fix-rebreak, verbatim:

> This issue has the same impact as this one: #143482. But the fix is not complete, there is a
> shopify subdomain (VPN server) where you still can connect your google account.

**AUTH-201152** (Informatica, high, resolved) — internal pages reachable via URL-parameter
change; decommissioned on EOL. **AUTH-187705** (DoD, critical, resolved) — team summary:
"an unauthenticated user to browse the website as an authenticated user."

## 7. External auth backends / authorization-error exposure

**AUTH-148151** (ownCloud, -, resolved) — the external SMB auth app validates via share
*listing*, which Samba's default `map to guest = bad user` answers for anyone. Verbatim:

> This allows for the listing of shares regardless of user, but not further information.

> In it's current implementation, providing any username to the application will log you in as
> that user - even creating a new one if necessary.

**AUTH-129918** (Slack, $2,000 json, resolved) — team summary: an "authorization error that
allowed the viewing of sensitive information on the server" (token+secret), mitigated with an
access investigation.

## 8. Doctrine

- **Identity-trust shortcuts are the cheapest high-value class** in the corpus: one parameter
  stripped (245408), one column truncated (2224), one domain not checked (143482) — each is a
  full ATO because the payload is the identity itself.
- **Fix-rebreaks are a family trait**: 2233→2224, 194832→143482. Re-test the *fixed* surface
  with a different truncation/encoding before writing the class off.
- **Unchained class still pays here** — unlike redirect rows (module 03 of ../Open-Redirect),
  these bypasses pay $500–$10,000 *without chaining*, because reaching "any account" or
  "admin" is the impact. Payouts track what the flaw reaches: subscriber-only provisioning was
  worth $0 of the $10,000; the admin guess was the money.
- Empty-severity rows (era artifact, pre-2016 field) do not mean low impact: 136169 and
  245408 carry no severity but $10,000/$1,000 json bounties.
