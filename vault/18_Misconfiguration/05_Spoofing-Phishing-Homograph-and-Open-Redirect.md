---
title: "Spoofing, phishing, homograph, and open redirect — trust the string, miss the binding"
type: playbook
category: spoofing_phishing_homograph_open_redirect
cwe: "CWE-707, CWE-931, CWE-601"
source_count: 19
full_bodies_available: 19
corpus: "h1-brain disclosed_reports.db 3,673 rows (sha256 8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4); misconfig bucket (152 rows)"
list_accessed: "2026-11-07"
note: "19 rows / $900 (5 paid). The smallest paid module per-row. All 19 bodies substantive. Every blockquote byte-true to references/archive/MISCONF-bodies-full-dump.txt."
---

# Spoofing, phishing, homograph, and open redirect — trust the string, miss the binding

## 1. Overview

Nineteen rows, **$900/5 paid** — the vault's cheapest module per finding and the one most likely to be closed as "informative" if filed carelessly. The family shares one root cause: **a string shown to the user (or used as a redirect target) is not bound to what it claims to be.** The corpus splits it into four lanes: **IDN/homograph handling** (the most crowded: Brave's homepage/redirect handling and Yelp/HackerOne's rendering), **content spoofing / text injection** (arbitrary text reflected into a trusted page), **address-bar and URL confusion** (the browser's own chrome lying), and **open redirect + email spoof** (the destination or the sender is attacker-chosen). The paid rows are exactly the ones that show the *deception in the user's own UI* — a redirect to an attacker domain from a trusted shortener, a safe-browsing bypass, an address bar that claims facebook.com.

**Case-stock (19 rows / $900):**

| Case | Target | Mechanism | Bounty |
|---|---|---|---|
| [MISCONF-126010](https://hackerone.com/reports/126010) | gratipay | verify.html email param → content spoof | - |
| [MISCONF-143975](https://hackerone.com/reports/143975) | security | Homograph skips warning on escalate view | - |
| [MISCONF-149798](https://hackerone.com/reports/149798) | nextcloud | DAV path text injection (CVE-2016-9468) | - |
| [MISCONF-154827](https://hackerone.com/reports/154827) | nextcloud | dir param spoofs breadcrumbs (CVE-2016-9467, $50) | $50 |
| [MISCONF-164137](https://hackerone.com/reports/164137) | legalrobot | CRLF in URL → content spoof (missing error page) | - |
| [MISCONF-172711](https://hackerone.com/reports/172711) | udemy | source_object_id reflected text injection | - |
| [MISCONF-172933](https://hackerone.com/reports/172933) | yelp | IDN rendered as Unicode → homograph (Yelp) | - |
| [MISCONF-175286](https://hackerone.com/reports/175286) | brave | Homepage accepts IDN; no punycode | - |
| [MISCONF-175958](https://hackerone.com/reports/175958) | brave | Address-bar spoof via setInterval (CVE-2016-9473, $200) | $200 |
| [MISCONF-182467](https://hackerone.com/reports/182467) | bumble | Email spoof via open mail relay (Badoo) | - |
| [MISCONF-210875](https://hackerone.com/reports/210875) | rockstargames | Host header → open redirect / phishing ($300) | $300 |
| [MISCONF-268984](https://hackerone.com/reports/268984) | brave | Homograph bypass via @ in homepage | - |
| [MISCONF-271324](https://hackerone.com/reports/271324) | security | Signed redirect bypassed by punycode→IDN swap | - |
| [MISCONF-317931](https://hackerone.com/reports/317931) | brave | Homograph bypass via /@ parsing | - |
| [MISCONF-327671](https://hackerone.com/reports/327671) | semrush | 404 text injection (u.semrush.com) | - |
| [MISCONF-385145](https://hackerone.com/reports/385145) | chaturbate | Redirect URL lacks homograph check (desktop) | - |
| [MISCONF-385372](https://hackerone.com/reports/385372) | chaturbate | Redirect URL lacks homograph check (mobile) | - |
| [MISCONF-1068505](https://hackerone.com/reports/1068505) | brave | Trailing dot bypasses blocklist ($250) | $250 |
| [MISCONF-1245051](https://hackerone.com/reports/1245051) | basecamp | Error page reflects path text ($100) | $100 |

## 2. Homograph doctrine: show the punycode

The module's citation-grade sentence lives in MISCONF-172933 (yelp):

> It would be safer to represent the Punycode version of the URL so that it would be apparent to the users that something wierd is going on. i.e show  http://xn--eby-7cd.com/ instead of http://ebаy.com/

> They both appear to be same when posted on yelp but actually 2nd is the original one and the 1st is actually https://www.xn--elp-cfd.com/

The Brave sequence (175286 → 268984 → 317931) is the corpus's best fix-bypass curriculum: homepage accepts the IDN verbatim; then an `@` before the IDN defeats a fix that only checked *after* `@`; then `/@` defeats the second fix. MISCONF-385145 (chaturbate) states the same check from the redirect side: the `external_link/?url=` endpoint performs no homograph normalization at all ("so it would be apparent that something weird is going on" when the punycode is shown).

MISCONF-271324 (security) is the one to file *with caveats*: the signed-redirect bypass (punycode→IDN swap plus `//` insertion) works only on already-signed URLs, and its impact is mobile-specific — the body says so honestly ("Mobile phone users are more likely to be affected"). MISCONF-143975 is the oddity that proves coverage paranoia: the external-link warning *exists*, but "when i click on show raw >escalate report, there is no external link warning page" — enforcement gaps in secondary UI are a misconfig family of their own (compare module 03's CSP-on-error-pages).

## 3. Content spoofing / text injection: reflected text, trusted context

- **Reflected credentials solicitation** — MISCONF-126010 (gratipay): a single `email=` parameter on `verify.html` renders "'your account has expired. You must renew it … send your login credentials to [REDACTED_EMAIL].'" This is the module's reference PoC for text injection: the injected string is not a script; it's a *social-engineering paragraph* rendered in a payment provider's template.
- **Path-reflected text** — MISCONF-1245051 (basecamp, **$100**) and MISCONF-327671 (semrush, 165 bytes): "Type any thing after slash, it will be reflected on the page." Together they show the cheap-filed end of the lane (no figure for the semrush twin) — one line of body, "Fix 404 error page" — kept as evidence that the lane's tail is scanner-grade.
- **DAV/files-app injection** — MISCONF-149798 (nextcloud, CVE-2016-9468) and MISCONF-154827 (nextcloud, **$50**, CVE-2016-9467): path segments and the `dir` parameter render attacker text in the trusted file UI. The paid twin's trick is worth stealing for filing: URL-encoded periods bypass the traversal filter, and a null byte kills the redirect that would have cleaned the parameter — *two filters, both needed, neither sufficient*.
- **URL-parameter reflection** — MISCONF-172711 (udemy): `source_object_id` is echoed inside a JSON error ("Invalid source object id: },{Kindly move to our new beta website evil.com") — text injection via an *error channel*, with the researcher's scope hedge ("Kindly mark it as informative in case if it is out of scope") intact. MISCONF-164137 (legalrobot) is the CRLF edition: `%0D%0AContent-Type…` in a URL crafts a spoofed error page — the CRLF pair to module 02's %0d%0a-account-creation row.

## 4. Address-bar and browser-chrome deception

MISCONF-175958 (brave, **$200**, CVE-2016-9473) is the module's most severe-looking row: a `setInterval` loop drives `location` to `https://facebook.com` while the body stays attacker content — "The URL would get spoofed to https://facebook.com (Even it shows Green lock so victim would believe) but the content remains the one which attackers have placed." MISCONF-1068505 (brave, **$250**) is its cheap sibling: a trailing dot in the hostname defeats the phishing blocklist ("http://3e1.cn./ is not blocked") while Chromium-based Brave blocks both — string normalization again, this time in a *defense* list. MISCONF-2501378 (module 04, **$100**) closes the braided family: URL eliding done wrong on Android shows long subdomains un-truncated, inviting the same misread. The shared lesson across browser and server: **normalization is a security control; every surface that renders a URL needs it, and the paid rows are the ones with screenshot-grade deception.**

## 5. Open redirect and email spoof

MISCONF-210875 (rockstargames, **$300**) is the module's paid open-redirect anchor and the only row that binds a *Host header* to a phishing primitive: the share-shortener builds links from `$_SERVER[HTTP_HOST]`, so an attacker-controlled Host mints a `rsg.ms` short link that 302s to the attacker's domain ("Did you notice the usage of `HTTP_HOST` which is variable and could be changed by sending different host header values"). MISCONF-182467 (bumble) is the email lane's textbook — an open relay form that lets anyone send mail "from" an admin address. Both are *sender/destination honesty* bugs: the system emits an identifier (short link, From address) whose binding to its owner was never checked.

## 6. What pays, what doesn't

- **Pays ($300/$250/$200/$100/$50):** every paid row in the module demonstrates deception in the victim's own UI or browser — open redirect via trusted shortener (**$300**), blocklist bypass (**$250**), address-bar spoof (**$200**), error-page reflection (**$100**), breadcrumb spoof (**$50**). The price is set by *how completely the victim's trust display is captured*, starting at $50 for a breadcrumb.
- **No figure (14 rows):** the IDN fleet (incremental fix-bypasses, unnormalized redirect endpoints), the email-spoof original, and the scanner-grade injections. The vault cannot prove non-payment; what the corpus proves is that incremental fix-bypasses *without* a new deception capture cluster at no-figure — file the bypass only when it re-captures a trust surface, not when it re-finds the same one.
- **Myth to retire** (from 1245051): "this attack is widely misunderstood as a kind of bug that brings no impact" — the researcher's own closing line is the triager's first reason to price it. File spoofing with the captured-trust screenshot or don't file it.

## 7. Cross-references

- Vault `Open-Redirect/` — MISCONF-210875 (Host-header shortener) and MISCONF-271324 (signed redirect) are that vault's specimens; this module owns their spoofing-mechanism half.
- Module 02 (§2) — MISCONF-815085's `%0d%0a` account creation and this module's MISCONF-164137 (CRLF content spoof) are the CRLF pair; vault `14_HTTP-Request-Smuggling/` is the desync home.
- Module 04 (§6) — URL-eliding row MISCONF-2501378 is this module's browser-chrome family filed under exposure because the bucket put it there; read the two §-sections together.
- Playbook P1–P2 — IDN/punycode inventory, redirect-signer diffing, error-page reflection sweep, trailing-dot normalization checks.
