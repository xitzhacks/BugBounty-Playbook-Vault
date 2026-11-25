---
title: "SSO / SAML / OAuth Identity Binding — when a third party vouches, who checks the voucher?"
type: playbook
category: sso-saml-oauth-binding
cwe: "CWE-290"
source_count: 17
full_bodies_available: 17
corpus: "h1.security.nathan.sx roster (224 rows), bodies via hackerone.com/reports/<id>.json"
list_accessed: "2026-10-28"
note: "Anchor bodies: AUTH-223014 (Uber SAML, $8,500 json, high), AUTH-114169/AUTH-215381 (Twitter Digits/Periscope, $2,520 list each), AUTH-65825 (Coinbase, $5,000 list), AUTH-127703 (Badoo, $852 list). Claims trace to bodies read 2026-10-29."
---

# SSO / SAML / OAuth Identity Binding — who checks the voucher?

## 1. Overview

Seventeen cases where a third party (Google, Facebook, Slack, Twitter Digits, Ubuntu One,
OneLogin SAML) vouches for the user — and the validation of that voucher fails. The corpus's
two biggest single payouts outside OneLogin auto-provisioning live here: the Uber SAML bypass
($8,500 json) and the Coinbase clickjacked OAuth authorization ($5,000 list). The lane pays
because every flaw *reaches an account or an internal system*, not because of chaining.

| Family | Cases | Bounty |
|---|---|---|
| SAML verification bypass | 223014 · 213789 | $8,500 json |
| SSO flow abuse (login CSRF / redirect) | 171398 · 178345 · 167828 | - |
| OAuth redirect_uri / callback validation | 2559 · 166942 · 114169 | $3,180 list |
| Third-party token acceptance | 101977 · 202177 | $100 list |
| OAuth authorize-endpoint CSRF | 215381 · 65825 | $7,520 list |
| Account-binding CSRF/link abuse | 127703 · 121827 · 225653 · 223475 | $852 list |
| OAuth registration-path bypass | 64946 | $40 list |

## 2. SAML verification bypass

**AUTH-223014** (Uber, high, $8,500 json, resolved) — team summary, verbatim:

> Due to improper SAML verification it was possible to bypass the OneLogin authentication on
> https://uchat.uberinternal.com and gain unauthorized access to internal chats.

Reporter's writeup linked in-body (blog.mish.re, 2017-09-06) — post-mirror bibliography only.
**AUTH-213789** (Nextcloud, low, resolved) — the php-saml implicit-boolean patch note, verbatim:

> This means that an implicit conversion to boolean of the values returned by openssl_verify()
> will convert an error state, signaled by the value -1, to a successful verification of the
> signature (represented by t

(-1 → truthy in PHP; signature validation returns *success on error*. Recorded as the library
advisory quote in the body; full text at the linked commit.)

## 3. SSO flow abuse (HackerOne SSO-SAML trio)

**AUTH-171398** (low, resolved) — login CSRF + open redirect + self-XSS exploitation plan,
verbatim:

> 1) Information Leak
>
> An attacker can use Logout CSRF + Login CSRF against a victim to steal all information sent
> by the victim to the HackerOne website while using the malicious session, including
> confidential bug reports.

> ```
> Malicious page -> HackerOne Login CSRF -> Self-XSS triggers -> Logout -> Wait user actions
> ```

**AUTH-178345** (low, resolved) — the patch bypass, verbatim:

> Recently, you have patched an open redirection issue which was reported as #171398.
> I found a bypass of that patch.

> 1. Add following in comment/report :
> ```https://hackerone.com/users//saml/sign_in?email=[REDACTED_EMAIL]&remember_me=true```

(double-slash skips the external-link warning page.)

**AUTH-167828** (-, resolved) — private-program discovery via SAML; team withheld the method
("we're not disclosing the method involved, but suffice to say it was very clever").

## 4. OAuth redirect_uri / callback validation

**AUTH-2559** (Slack, $100 list, resolved) — path-walk past redirect_uri validation, verbatim:

> Note i am bypassing the redirect_uri validation by using ../../

> http://givensite.com/redirect_url=https:/www.evilsite.com/a.php/complete?code=AQCbhUg1FiEQf5TyTesMgjP8zq

> So,then he can login into the victim account using code value.

**AUTH-166942** (Twitter Digits/Fabric, $560 list, resolved) — subdomain/path callback
tolerance leaks authorization to linked sites, verbatim:

> While authenticating digits to my Fabric account i have noticed that the callback_url is not
> solid i.e. any sub domain or any path is accepted as callback_url with host as fabric.io.

**AUTH-114169** (Twitter Digits, $2,520 list, resolved) — the host-validation bypass via
HTTP Parameter Pollution, verbatim:

> However, the validation can be bypassed with HPP (HTTP Parameter Pollution). If we supply
> multiple *h

(mechanism: duplicated `host` parameters — the validator sees the first, the redirect logic
the last). This row is module 08's HPP fingerprint's paying sibling — HPP as *delivery*, OAuth
binding as *impact*.

## 5. Third-party token acceptance

**AUTH-101977** (Imgur, -, resolved) — any Facebook app's access token accepted, verbatim:

> Hacker can build own facebook app and get victim's facebook access token and use that access
> token to login into imgur account

> Prevention: Validate access token and check app id is equal to 127621437303857

**AUTH-202177** (Instacart, low, $100 list, resolved) — the Google `id_token` accepted from
*any* app, verbatim:

> For example, I logged in with the app Meetup via login with Google. The id_token generated by
> Google for this app, when used with your /google_login_auth API, it's still get accepted.

## 6. OAuth authorize-endpoint CSRF

**AUTH-215381** (Twitter Periscope, $2,520 list, resolved) — verbatim:

> It was found that the authorize endpoint does not have any protection against CSRF.

> As one can see, there is no CSRF token or Origin validation.

> After a 3rd party application gets the *authorization cod

**AUTH-65825** (Coinbase, $5,000 list, resolved) — the same flaw on the *authorize button*,
delivered by clickjacking, verbatim:

> Due to a misconfiguration, the 'authorize' button on the OAuth authorization page was
> vulnerable to clickjacking.

> The bug was fixed by ensuring our OAuth-related responses included the same security headers
> (including X-Frame-Options) as the rest of the site.

CSRF/clickjacking own the delivery (../CSRF); the class owns the decision that an authorize
POST is state-changing and unguarded.

## 7. Account-binding CSRF & link abuse

**AUTH-127703** (Badoo, $852 list, resolved) — the `rt` state parameter leaks in a
service-worker script, verbatim:

> the only thing that protects from CSRF is the `rt` parameter which is unique for each
> user/session . I have noticed that the `rt` parameter is returned on almost all json
> responses so I tried to find a link that leaks it.

> if you open the link `https://eu1.badoo.com/worker-scope/chrome-service-worker.js ` you'll
> find a string variable `url_stats` containing the value of the `rt` parameter:

**AUTH-121827** (Badoo, $850 list, resolved) — the import-photos link replaces the victim's
Facebook binding on *cancel*, verbatim:

> 4- FB account of 'victim' is replaced with FB account of 'attacker' (Removed from 'victim'
> one)

> 5-Login via attacker FB account and you will be logged in 'User' account

**AUTH-225653** (Weblate, high, resolved) — the Ubuntu One OpenID association completes on
the victim's session via a CSRF'd POST, verbatim:

> 7. Attacker's Ubuntu account will be connected to victim , the attacker can then use login
> with Ubuntu and access victim's account.

**AUTH-223475** (Weblate, low, resolved) — sessions outliving their credentials, verbatim:

> The session remains active on the device in step 2. So I continue with a valid session from
> credentials not linked to any account at https://hosted.weblate.org

## 8. Registration-path bypass

**AUTH-64946** (Legal Robot, $40 list, resolved) — team summary, verbatim:

> Security researcher discovered that OAuth login bypassed the intended registration/waitlist
> process  during the private beta.

## 9. Doctrine

- **Every paying row reaches an account.** $8,500 (internal chat via SAML), $5,000
  (OAuth grant via clickjacking), $2,520 × 2 (Digits host bypass, Periscope authorize CSRF),
  $852/$850 (binding CSRF at Badoo) — the binding decision *is* authentication; breaking it is
  ATO or grant-theft on its own.
- **The four validation surfaces, in test order** (distilled from the corpus):
  1. `redirect_uri`/`callback_url` strictness — path walks (2559), subdomains (166942), HPP
     (114169);
  2. token *issuer* — which app minted the token (101977, 202177);
  3. authorize step CSRF/Origin (215381, 65825);
  4. binding/unbinding step CSRF + state-parameter leakage (127703, 225653, 121827).
- **State parameters leak through side channels** — 127703 found `rt` in a service-worker
  script, 225653 didn't even need it (unauthenticated POST). Any "unique per session" anti-CSRF
  value readable from a same-origin GET is decoration.
- **Fix-rebreak discipline** (178345): the #171398 patch was bypassed by a double slash.
  Re-test patched SSO endpoints with encoding/slash variants.
- Era note: SAML -1→true (213789) is php-saml 2.10.4-era; modern SAML JWT-confusion and XSW
  variants are bibliographic — see `references/blogs-index.md` §3.
