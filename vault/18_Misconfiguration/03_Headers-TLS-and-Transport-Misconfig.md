---
title: "Headers, TLS, and transport misconfig — the downgrade is the vuln"
type: playbook
category: headers_tls_transport_misconfig
cwe: "CWE-319, CWE-655, CWE-16"
source_count: 30
full_bodies_available: 28
corpus: "h1-brain disclosed_reports.db 3,673 rows (sha256 8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4); misconfig bucket (152 rows)"
list_accessed: "2026-11-07"
note: "30 rows / $2,311 (6 paid). 28 substantive bodies; MISCONF-1753226 / MISCONF-1813831 are 78-byte CVE pointers (HSTS IDN bypasses). 11 of these rows are also indexed under the module_map misconfig-ssl-tls sibling (see source-index §2). All blockquotes byte-true."
---

# Headers, TLS, and transport misconfig — the downgrade is the vuln

## 1. Overview

Thirty rows, **$2,311/6 paid** — the vault's tidiest pricing study, because nearly every row is a *downgrade*: somewhere on the path (page → POST, app → API, client → server) the transport does the sensitive thing in cleartext, or the hardening header that was supposed to prevent it is missing, malformed, or silently ignored. The module sorts naturally into four lanes: **security headers and policy** (CSP/CORS/X-Frame/referrer discipline), **TLS and certificates** (ciphers, protocols, HSTS, cert validation), **cleartext behavior of clients** (login POSTs, VPNs, emailed passwords, toolkits), and **cache** (the deception/poisoning twins that nine other misconfig vaults keep circling). Only the cache-deception and header-injection rows clear $500; classic scanner-grade output (RC4, 3DES, SSLv3) floors at $0–$1, which is why the module exists as a *negative-space curriculum*: it shows exactly where the money stops.

**Case-stock (30 rows / $2,311):**

| Case | Target | Mechanism | Bounty |
|---|---|---|---|
| [MISCONF-99157](https://hackerone.com/reports/99157) | slack | RC4 suites enabled | - |
| [MISCONF-131065](https://hackerone.com/reports/131065) | gratipay | Weak TLS/SSH ciphers ($1) | $1 |
| [MISCONF-158002](https://hackerone.com/reports/158002) | instacart | Missing rel=noreferrer (reverse tabnabbing) | - |
| [MISCONF-163676](https://hackerone.com/reports/163676) | legalrobot | Missing CSP header | - |
| [MISCONF-180538](https://hackerone.com/reports/180538) | yelp | Cert validation fails on IDN vanity domains | - |
| [MISCONF-199779](https://hackerone.com/reports/199779) | security | CSP img-src exfil via GA hosting | - |
| [MISCONF-210331](https://hackerone.com/reports/210331) | rockstargames | SSLv3 POODLE live | - |
| [MISCONF-214571](https://hackerone.com/reports/214571) | rockstargames | Login POST via HTTP (sslstrip) ($350) | $350 |
| [MISCONF-222692](https://hackerone.com/reports/222692) | wordpress | TRACE enabled (XST) | - |
| [MISCONF-235200](https://hackerone.com/reports/235200) | semrush | CORS wildcard + credentials | - |
| [MISCONF-250729](https://hackerone.com/reports/250729) | security | CSP absent on error pages | - |
| [MISCONF-342693](https://hackerone.com/reports/342693) | semrush | Reset token leaks in Referer | - |
| [MISCONF-386735](https://hackerone.com/reports/386735) | chaturbate | Login page over HTTP / no HSTS | - |
| [MISCONF-409518](https://hackerone.com/reports/409518) | grammarly | HTTP Wikipedia link leaks Referer + window.opener | - |
| [MISCONF-536669](https://hackerone.com/reports/536669) | zendesk | Test target sends creds in Authorization header | - |
| [MISCONF-576288](https://hackerone.com/reports/576288) | chainlink | No SSL + no HTTPS redirect (cleartext) | - |
| [MISCONF-631589](https://hackerone.com/reports/631589) | lyst | Cache deception leaks PII | - |
| [MISCONF-703759](https://hackerone.com/reports/703759) | bumble | SSO forwarded over HTTP | - |
| [MISCONF-728664](https://hackerone.com/reports/728664) | gsa_bbp | CPDoS via X-CF-APP-INSTANCE | - |
| [MISCONF-806577](https://hackerone.com/reports/806577) | nordsecurity | Unencoded ; → arbitrary Set-Cookie | - |
| [MISCONF-813159](https://hackerone.com/reports/813159) | helium | Invite URL IDs in cleartext → admin takeover | - |
| [MISCONF-1010858](https://hackerone.com/reports/1010858) | acronis | Cache poisoning via x-forwarded-port | - |
| [MISCONF-1089995](https://hackerone.com/reports/1089995) | brave | Onion-Location opens chrome: URLs ($400) | $400 |
| [MISCONF-1271944](https://hackerone.com/reports/1271944) | shopify | Cache deception leaks PII + CSRF token ($800) | $800 |
| [MISCONF-1565622](https://hackerone.com/reports/1565622) | ibb | HSTS trailing-dot bypass (CVE-2022-30115) | - |
| [MISCONF-1753226](https://hackerone.com/reports/1753226) | ibb | HSTS IDN bypass (CVE-2022-42916) | - |
| [MISCONF-1813831](https://hackerone.com/reports/1813831) | ibb | HSTS IDN bypass (CVE-2022-43551) | - |
| [MISCONF-1987687](https://hackerone.com/reports/1987687) | mozilla | VPN leaks plaintext to server IP | - |
| [MISCONF-2337938](https://hackerone.com/reports/2337938) | sheer_bbp | Password emailed in cleartext ($200) | $200 |
| [MISCONF-2437131](https://hackerone.com/reports/2437131) | ibb | Disabled protocol stays allowed (CVE-2024-2004, $560) | $560 |

## 2. The paid lane: cache deception wins, scanner output doesn't

MISCONF-1271944 (shopify, **$800**) is the module's ceiling and the corpus's cleanest web-cache-deception write-up — path confusion with `.css` suffix, authenticated victim caches PII plus a live CSRF token, attacker reads it unauthenticated:

> Web cache deception (WCD) is an attack where an attacker tricks a caching proxy into erroneously storing private information transmitted over the Internet and subsequently gains unauthorized access to that cached data.

> This URL will be interpreted as a CSS file from the cache server, resulting in the web page being cached (with the personal information of the authenticated user embedded). Your website, instead, returns a 404 not found error page that includes some user's personal information.

MISCONF-631589 (lyst) is the same technique stated as a state machine — log in, visit `…/blahblah.css`, the cache stores the page *with* the session's PII, and any later visitor reads it (email, member id readable from source):
> In that case, this url: https://www.lyst.com/shop/trends/mens-dress-shoes/blahblah.css can be visited in Private Mode and still you will be shown as "LOGGED IN" and then check the Source code you will get your email, member id ,etc..

MISCONF-1010858 (acronis) is the poisoning twin: `x-forwarded-port` destroys the cache key, a junk port value gets cached, and every subsequent visitor receives the 404-as-cache. MISCONF-728664 (gsa_bbp) completes the cache quartet from the DoS side (CPDoS via `X-CF-APP-INSTANCE: xxx:1` — a bad instance header 404s everything, and the CDN caches the 404).

The scanner-output floor is explicit: MISCONF-131065 (gratipay, **$1**) lists TLS_ECDHE_RSA_WITH_3DES_EDE_CBC_SHA and CBC SSH ciphers field-by-field and awards a dollar; MISCONF-99157 (slack, RC4) and MISCONF-210331 (rockstargames, POODLE) likewise $0. The module's rule: **cipher/protocol reports are only reports when they are downgrades with a victim.** MISCONF-2437131 (ibb, **$560**, curl CVE-2024-2004) clears the bar precisely because it is a *semantic* downgrade — an app that explicitly disables protocols is silently re-enabled:

> When a protocol selection parameter option disables all protocols without adding any then the default set of protocols would remain in the allowed set due to an error in the logic for removing protocols. The below command would perform a request to curl.se with a plaintext protocol which has been explicitly disabled.

And the HSTS trio (1565622 CVE-2022-30115, 1753226 CVE-2022-42916, 1813831 CVE-2022-43551) shows the same principle inside HSTS itself: the hardening header is present but its hostname normalization is wrong (trailing dot, IDN), so the attacker walks around it.

## 3. Cleartext behavior: who sends what, where

- **The sslstrip trilogy.** MISCONF-214571 (rockstargames, **$350**): the login *page* is HTTP even though the POST goes over HTTPS — so MITM strips the page and the credential falls. MISCONF-386735 (chaturbate) states the mitigation doctrine:

> If any part of a site is required to be protected by SSL, the entire site should be protected by SSL.

MISCONF-576288 (chainlink): no SSL and no HTTPS redirect at all. **The trilogy's shared insight** is that the vulnerability is not "HTTPS missing" — it's the page that *carries the password* negotiating below the layer that protects the POST.
- **SSO downgrade.** MISCONF-703759 (bumble): the odnoklassniki SSO leg is HTTP, so the attacker both steals the third-party credentials *and* performs login-CSRF by binding their own credentials to the victim's state parameter. One cleartext leg, two classic attacks.
- **The emailed password** — MISCONF-2337938 (sheer_bbp, **$200**) is a two-paragraph report that should embarrass the industry:

> After successfully signup as a fan, the password was then sent to email by cleartext

MISCONF-342693 (semrush) is the token edition: reset pages leak the token in `Referer` to any social link on the page. Both are transport-discipline failures with direct account-takeover arithmetic.
- **Toolkits as cleartext.** MISCONF-536669 (zendesk): the "Test target" button ships the admin's own username/password in a Basic `Authorization` header to an arbitrary internet host — a vendor-configured integration exfiltrating operator credentials. MISCONF-1089995 (brave, **$400**) is a header-trust bug: `Onion-Location` is honored for `chrome:`/`javascript:` schemes, so a web page can restart the browser, or restart-loop it. MISCONF-806577 (nordsecurity): unencoded `;` in `?coupon=` lets the query string forge additional `Set-Cookie` headers — session fixation / cookie bomb from a URL parameter.

## 4. Headers: presence isn't policy

- **CSP bypass via allowed hosts** — MISCONF-199779 (security): `img-src 'self' data: www.google-analytics.com` plus an unclosed-quote `<img>` injection turns Google Analytics (hosting user content) into an exfiltration oracle for CSRF tokens. MISCONF-250729 (security): CSP "not applied to error pages" — the 404 renderer drops the policy, so `%`/`%"` at the endpoint re-opens inline event handlers. MISCONF-163676 (legalrobot): no CSP header at all, third-party image injection as the whole PoC. The three rows teach CSP review order: *present? → renderer-consistent? → host list safe?*
- **CORS misconfig** — MISCONF-235200 (semrush, response `Access-Control-Allow-Credentials: true` with a caller-supplied origin) is the textbook: "Trusting arbitrary origins effectively disables the same-origin policy, allowing two-way interaction by third-party web sites." MISCONF-426165 (module 06, **$550**) is the same bug with a live PoC — origin reflection with credentials over `*.zomato.com`.
- **Token transport in headers** — the header lane's mirror image: MISCONF-409518 (grammarly) leaks `Referrer` + `window.opener` over an HTTP Wikipedia link; MISCONF-158002 (instacart) omits `rel=noreferrer` so a new tab can rewrite the opener's URL (reverse tabnabbing); MISCONF-297181 (module 04, referrer-policy set but ignored cross-origin) completes the triptych. The kill-gate version of this lesson is in playbook P5: a missing header is only a finding with a carrier URL.
- **CRLF-adjacent** — MISCONF-806577's cookie injection and MISCONF-222692 (wordpress, TRACE/XST) sit on the smuggling boundary; the module keeps them here because the sink is a *header decision*, not a request-smuggling desync.

## 5. Client protocols: certs and VPNs

MISCONF-180538 (yelp): X.509 validation fails on international vanity domains — the user-facing truth that "cert errors" are also a transport-misconfig class. MISCONF-1987687 (mozilla VPN, 9,935 bytes, no figure) documents plaintext leakage to the VPN server's IP on Linux/Android, with the coordinated-disclosure framing (66 VPNs, CERT/CC, embargo language) that modern VPN research files under. MISCONF-813159 (helium): an invite URL carrying org/inviter IDs in cleartext lets a registrant rewrite the receiver ID and *become an administrator* — transport and identity in one parameter.

## 6. What pays, what doesn't

- **Pays ($800/$560/$400/$350/$200/$1):** cache deception with live PII+token recovery ($800), a semantic protocol-policy downgrade ($560), a privileged-scheme header bug ($400), an sslstrip-able login page ($350), an emailed password ($200), and the corpus's $1 same-bounty for cipher inventory ($1). The ratio is the lesson: **demonstrated downgrade of a stated policy** pays; inventory pays a dollar.
- **Doesn't ($0 rows in this module):** 24 rows with no figure — including real but unpaid hardware (curl HSTS CVEs, VPN plaintext, CORS grammar, CSP absence). The module is honest about why: the DB records no figure for most of them, so the vault cannot prove non-payment; what it can prove is the *shape* of the paid ones.
- **Anti-pattern** (from 131065): a scanner dump with no victim interaction and no downgrade semantics is filed as hygiene, not vulnerability. Programs price the dollar to teach the difference.

## 7. Cross-references

- Vault `15_Cache-Poisoning/` — the cache-deception/poisoning twins (MISCONF-1271944, 631589, 1010858, 728664) are that vault's core canon seen from the misconfig side; vault `13_Subdomain-Takeover/` owns the CDN-origin half (module 01 §4).
- Module 06 (§3) — MISCONF-426165 (CORS reflection, **$550**) is this module's §4 CORS section with the paid receipt.
- Module 05 (§4) — MISCONF-210875 (Host-header → open redirect, **$300**) is the header-trust family member filed under spoofing because its payload is a redirect.
- Playbook P1 (header/TLS inventory), P2 (downgrade ladder), P4 (hardening fingerprints: HSTS preload, CSP host audit, CORS allowlist).
