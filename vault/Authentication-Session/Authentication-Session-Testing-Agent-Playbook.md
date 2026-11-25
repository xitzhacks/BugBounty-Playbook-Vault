---
title: "Authentication & Session Testing Agent Playbook — the executable protocol"
type: agent-playbook
category: auth-session-all
cwe: "CWE-287"
built: "2026-10-29"
corpus: "224 mirror rows → 188 bodies read (138 resolved / 35 informative / 7 duplicate / 8 not-applicable) · 36×404 recorded"
bounty: "$123,419 roster-tagged (JSON $58,278/28 · list $58,903/57 · dead-list $6,238/13) · pure class 01–07 $99,360 · adjacent/noise 08 $17,821"
companion_modules: "01 core-bypass · 02 fixation-hijack · 03 expiry-invalidation · 04 2fa-otp · 05 reset-token · 06 credential-change-verification · 07 sso-saml-oauth · 08 adjacent-noise"
quote_rule: "byte-true, from read bodies only; 404 rows recorded never quoted"
---

# Authentication & Session Testing Agent Playbook

Executable protocol derived from 188 read bodies (2013–2017 era) + modern discipline from the
hunt-auth-bypass / hunt-mfa-bypass / hunt-session skills. Every step cites its corpus
evidence. Run phases in order; abort at kill-gates. Crown-jewel doctrine up front:
**authentication bypasses pay for what they reach** — module 01's $10,000 OneLogin row and
module 05's two $10,000 reset rows all reached *any account* with zero chaining, while the
same class unchained (fixation, logout non-expiry) stays a $50–$300 report.

## P0 — Auth-surface inventory (always first)

1. **Flow census**: enumerate every way to *become* logged-in — password login, OAuth/social
   (each provider), SAML/SSO, magic-link, passwordless, registration auto-login, mobile-app
   SSO. Corpus: Zomato's three parallel logins (245408), Shopify's Google-Apps lane (178293),
   Uber's passwordless-signup (143717), Weblate's confirmation auto-login (229528).
2. **Identity-edit census**: email change, username change, phone add/change, password
   change, personal info. For each: does it demand old password / re-verification? Corpus:
   147182, 223461, 147203, 146129.
3. **Reset/verification flows**: forgot-password, verify-email, resend-verification,
   recovery-code generation. Corpus: module 05's 20 rows.
4. **2FA census**: factors offered (TOTP/SMS/U2F/backup), enable/disable/reset paths,
   remember-device semantics. Corpus: module 04's 29 rows.
5. **Session cookie inventory**: name, `Domain=` scope, Secure/HttpOnly/SameSite flags,
   pre-auth vs post-auth values, logout behavior. Corpus: 2421, 135797, 172137, 219205,
   module 03's 26 rows.
6. **SSO/OAuth surface**: authorize endpoints, `redirect_uri`/`callback_url`/`host`
   parameters, state/rt parameters and where they leak. Corpus: module 07's 17 rows
   (2559, 166942, 114169, 127703).
7. **Email-domain trust config** (self-hosted SSO products): `auth.email-domains`,
   hosted-domain checks. Corpus: 2224, 2233, 4795, 143482, 258117.

## P1 — Cheapest-first probes (seconds each, corpus-ordered)

| # | Probe | Cost | Corpus proof |
|---|---|---|---|
| 1 | Export pre-auth cookies → login in second profile with those cookies → is attacker logged in as victim? | ~2min | 6504, 135797, 2421 |
| 2 | Capture any authed request → logout → replay | ~30s | 353, 737, 288, 284, 223327 |
| 3 | Replay reset link after using a newer one / after password change | ~1min | 15166, 220185, 23921 |
| 4 | Request reset → change email → use old link | ~1min | 17383, 17474, 23579, 145896, 22203 |
| 5 | Strip login-request parameters one by one (email-only login) | ~5min | 245408 |
| 6 | OTP-submit step: swap `login`/`otp_user_id` field to another user | ~2min | 128085, 124845 |
| 7 | Re-register on the signup page while logged in; re-visit old signup links | ~5min | zseano §1a; 64946 |
| 8 | OAuth login: which app's token is accepted? (`id_token`/`access_token` from another app) | ~10min | 101977, 202177 |
| 9 | `redirect_uri` variants: `../../`, sibling path, subdomain, HPP duplicate param | ~10s | 2559, 166942, 114169 |
| 10 | OTP error message / response manipulation — does the code echo? | ~2min | 142221, 247158, 130460 |
| 11 | 10–20 rapid OTP submissions — measure the throttle window | ~1min | 149598, 128777 |
| 12 | Sign out → does the *session* die server-side, or only the client cookie? 6–8 h later re-check | passive | 284, 250688 |

## P2 — Lane decision tree (which module owns the finding)

```text
Authentication failure confirmed →
├─ server mints attacker session without identity proof ....... 01 Core Bypass
│   ├─ email-domain/hosted-domain trust violated ............. (2224/2233/4795/143482)
│   ├─ single-attribute login ................................ (245408/98247)
│   ├─ SSO plugin auto-provisioning .......................... (136169/138869)
│   └─ feature/ticket-gated access ........................... (215053/116504)
├─ session identity issued/accepted wrongly ................... 02 Fixation/Hijack
│   ├─ no regeneration on login/logout ........................ (2421/6504/135797)
│   ├─ OAuth state fixed forever .............................. (55911)
│   └─ cookie scope + subdomain takeover chain ................ (172137/219205)
├─ sessions fail to die ....................................... 03 Expiry/Invalidation
│   ├─ logout replay .......................................... (353/737/288)
│   ├─ password-change survivors .............................. (145430/226712/223327)
│   └─ stale authorization cache .............................. (245833/250688)
├─ second factor does not decide .............................. 04 2FA/OTP
│   ├─ flow reaches authed state without factor ............... (178293/163834/128085)
│   ├─ code reusable/unverified/leaked ........................ (67660/77076/142221)
│   └─ brute-force window math ............................... (149598/128777)
├─ reset credential lifecycle ................................. 05 Reset Tokens
│   ├─ token readable in wire/response ........................ (173551/143717)
│   ├─ survives identity/password change ...................... (17383/15166/220185)
│   └─ referer leakage + non-expiry compound .................. (5691/244434/253448)
├─ identity edits without proof ............................... 06 Credential Change
│   └─ email change → forgot-password recipe .................. (223461/147182)
├─ third-party voucher accepted wrongly ....................... 07 SSO/OAuth Binding
│   ├─ redirect/callback validation gaps ...................... (2559/166942/114169)
│   ├─ token from wrong app accepted .......................... (101977/202177)
│   └─ authorize/bind step CSRF ............................... (215381/65825/225653)
└─ body says another class owns it ............................ 08 Adjacent → cross-ref
    (CSRF 13 rows · TLS/transport 7 · XXE-in-SAML · OAuth-XSS)
```

## P3 — Deep exploitation (once a lane confirms)

1. **Quantify the reach, then the payout follows.** "Any account" beats "my own account":
   245408 reached any email holder ($1,000), 136169 reached admin ($10,000), 173551 reached
   any valid email ($10,000 critical). Demonstrate cross-user reach before writing the report.
2. **Chain the lifecycle halves.** Referer leak (5691/244434) × non-expiry (15166/220185) ×
   email-change survival (17383) — report the *compound* when all three hold, cite the
   Weblate/LegalRobot fix philosophy (253448): "eliminate any possibility of token leakage"
   *and* immediate invalidation.
3. **2FA state-machine trace.** Draw every transition into/out of the OTP step
   (128085's `otp_user_id`), including parallel login methods (178293), session resets
   (163834), IP changes (167121), password changes (179421). The corpus's four VK/Shopify
   bypasses are all *transitions*, not crypto.
4. **Binding-step CSRF with leaked state** (127703): find the per-session anti-CSRF value in
   any same-origin GET (service-worker scripts, JSON responses), then CSRF the
   authorize/associate POST (215381, 225653).
5. **Cookie-scope × dangling-CNAME sweep** (172137 → 219205): enumerate zone for unregistered
   cloud hostnames; check auth-cookie `Domain=` against every takeover candidate. 2016 dup
   ($500) vs 2017 critical ($5,000) — same chain; program posture decides the bounty.
6. **Fix-rebreak immediately** (2233, 194832, 178345, 229417): every fixed row in the corpus
   re-broke with a different truncation/encoding/slash variant. First probe after any auth
   fix ships: repeat the original flow with one mutated element.

## P4 — Modern hardening fingerprints (test that defenses EXIST, don't report absence)

- Session: revocation on logout/password-change (353-era bugs), `__Host-` prefixes, SameSite,
  server-side session lists (20122's ask).
- 2FA: WebAuthn/U2F availability, remember-device binding, 2FA on sensitive re-auth,
  recovery-code burn-on-use, no pre-generated secrets in DOM (100509).
- OAuth/OIDC: exact-match `redirect_uri`, PKCE, state bound to session, id_token audience
  verification (202177-era bugs dead on modern stacks).
- Reset: token ≤15 min single-use, invalidated on any identity change, no auto-login
  (Weblate-era designs dead).
- Email-domain trust: validation server-side on full length (2224-era `VARCHAR(128)` bugs
  dead where length+format validated pre-insert).
- When absent on a modern target: these are *hardening gaps*, corpus doctrine says report as
  Low/info at best — the 2014-era bounties came from a pre-hardening era.

## P5 — Reporting gates (before any submission)

1. **Impact demonstrated, not implied**: a session reproduction with two accounts (A attacker,
   B victim) for every ATO claim — the corpus's accepted reports all show B reached from A
   (135797's 4 steps, 128085's Jane/John, 223461's recipe).
2. **Class honesty**: logout-CSRF is ../CSRF's row; FREAK is TLS's; XXE-in-SAML is XXE's.
   Only submit under auth/session when the *deciding flaw* is the authentication decision
   (module map 01–07).
3. **Severity follows reach**: any-account/admin = High/Critical; own-session/UX = Low;
   identity-edit-missing-step-up without ATO = Low/informative (module 06's informative wall
   is the honest baseline).
4. **Substate reality-check**: the corpus's 35 informative and 8 N/A rows were *correct*
   classifications of right-mechanism/wrong-impact findings — do not inflate.
5. **Era discipline**: cite corpus rows as era precedent (2013–2017), never as proof a modern
   target still pays; pair with P4 hardening status.

## Kill-gates (abort the report, keep the knowledge)

- Reproduction requires the victim to *not* be logged in anywhere and you to know their
  password → it's not a bypass; stop.
- OTP brute force without window math or a demonstrated throttle bypass (149598's standard).
- Fixation/hijack demonstrated only on your own two test accounts with no third-party reach
  and no shared-computer scenario → cap at Low or don't submit (135797's own framing).
- "Missing best practice" rows (no CAA, no HSTS absent MitM position, auto-logout too short
  complaints like 123897) → ../triage-validation always-rejected list.
- Token entropy claims without entropy math (17512 was informative even with a chain) →
  compute the space × rate first.
