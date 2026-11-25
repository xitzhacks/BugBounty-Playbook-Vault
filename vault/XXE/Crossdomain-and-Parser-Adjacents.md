---
title: "Crossdomain policy + XML parser internals — the adjacent classes, with boundaries"
type: playbook
category: crossdomain-and-parser-adjacents
cwe: "CWE-939 (policy) · CWE-843 (type confusion)"
source_count: 22
full_bodies_available: 7
corpus: "h1.security.nathan.sx roster (44 rows), bodies via hackerone.com/reports/<id>.json"
list_accessed: "2026-10-27"
note: "Two adjacent classes kept out of the XXE entity counts: Flash policy files and XML-parser memory bugs. Claims trace to bodies read 2026-10-27."
---

# Adjacent classes — crossdomain policy and XML parser internals

## 1. Overview

Two clusters matched the roster filter but are **not** entity-parsing bugs. They are kept here —
not laundered into XXE counts — because both live on the same attack surface an XXE hunter
patrols: the XML files a server *serves or parses*. The module teaches each class's own doctrine
and marks the boundary.

**Case-ID scheme: `XXE-<report id>`.**

---

# Part I — crossdomain.xml (Flash policy files)

## 2. The doctrine case — XXE-43070 (Vimeo, informative)

The three-conditions test, verbatim — the whole class fits in this paragraph:

> As a general rule, if the following three conditions are met, there is problem:
> 1. A crossdomain.xml file is hosted at the root of the host…
> 2. The crossdomain.xml is overly permissive.
> 3. There is either sensitive information on www.secret-site.com or there are sensitive actions
>    that can be performed.

and the disposition sentence that defines *informative* for this class:

> If #1 and #2 are met, but www.secret-site.com does not contain any sensitive information… there
> is no risk to having a wide open crossdomain.xml file.

The Vimeo policy itself was maximally open — `<allow-access-from domain="*" secure="false"/>` plus
`<allow-http-request-headers-from domain="*" headers="*"/>` — and the body still teaches the
general principle:

> the overly permissive crossdomain.xml file allows Flash to do things that even JavaScript is not
> allowed to do, mainly accessing cross domain resources.

## 3. The exploit-chain case — XXE-96662 (Badoo, $310 list)

The proof that conditions #1+#2+#3 pay: upload a Flash file *through the target itself* so it lands
on an allowed origin. The chain, byte-true in outline:

> This file can be a Flash file. This file is hosted at https://static-*.badoo.com which is an
> allowed domain because of the line `<allow-access-from domain="*.badoo.com"/>` in the
> crossdomain.xml file.
> The problem is that an attacker can upload a malicious Flash file and load it from an external
> website. This allows to read and update information of the current logged in user.

19 numbered PoC steps ending in full cross-origin read:

> 19. The content of the endpoint https://us1.badoo.com/settings is showed in the `<textarea>`.

with the POST-capability note — *"it's possible to make POST requests too"* — and the file dressed
as an image (`bug.jpg`). This is the same **upload-to-trusted-origin** trick the File-Upload
module's rename-bypass lane teaches (`bug.jpg` there, `bug.jpg` here — the era's favorite disguise).

## 4. The nuance cases — XXE-105463 / XXE-91604 (Imgur)

XXE-105463 prices the `secure="false"` attribute on an HTTPS host — a downgrade lane for a
*poisoned-DNS attacker only*:

> I can only think of one risk in setting secure to false: A user with a poisoned host file or DNS
> server might be diverted to a flash client on a fake http://subdomain.example.com.

XXE-91604 (metadata-only) carries the CSRF-token-read impact statement:

> The result page for http://api.imgur.com/ would include the CSRF token and the SWF file could
> make requests with the user's cookies.

Two severities for adjacent configs on one domain ($150 vs $50 list) — the difference is the
**HTTPS-boundary** violation (105463) vs plain over-permissiveness (91604).

## 5. The wide-open case — XXE-44652 (Mobile Vikings) — and the dark row

`domain="*"` on a consumer portal; body demonstrates the read shape. **XXE-105655** (Pornhub,
$50 list) is a **404** — recorded, nothing recoverable.

## 6. Flash-policy execution template (for the era's survivors)

1. Fetch `/crossdomain.xml` at **root of each subdomain** — policies are host-scoped.
2. Parse: `domain="*"` (max), wildcard subdomains, `secure="false"` on HTTPS hosts,
   `allow-http-request-headers-from` with `headers="*"`.
3. Find a **user-upload path that lands on an allowed origin** (§3's chain) or an HTTP-hosted SWF
   (§4's lane).
4. Prove with a **read of a response the user could see** — settings page, CSRF token in DOM —
   rendered into your page; stop there.
5. In 2026 this is a heritage lane (Flash EOL'd) — the *transferable* doctrine is: any
   cross-origin policy file (CORS, crossdomain, URLFrameOptions) is a bug **only** in combination
   with sensitive data/actions on the same origin (§2's test #3).

---

# Part II — XML parser internals (deserialization-adjacent)

## 7. The parser-memory cluster (4 rows, all PHP/Python IBB)

These are **type-confusion bugs in the parser runtimes**, reached through PHP `unserialize()` or
direct API misuse — the XML carrier is incidental; the bug is memory corruption:

- **XXE-55030** ($2,500 list): *"SoapClient's __call() method is prone to a type confusion
  vulnerability which can be used to gain remote code execution through unsafe unserialize()
  calls."* — `Z_ARRVAL_P` on `__default_headers` unchecked at soap.c:2906; PoC:
  `unserialize('O:10:"SoapClient":3:{s:3:"uri";s:1:"a";s:8:"location";s:22:"http://localhost/a.xml";s:17:"__default_headers";i:1337;}')`
- **XXE-104010** ($1,500 list): SOAP `serialize_function_call()` type confusion / RCE — body is a
  bare `bugs.php.net/bug.php?id=70388` pointer (era norm for IBB reports).
- **XXE-73245** ($500 list): full fake-HashTable exploit body (Taoguang Chen, 2015) — the deepest
  memory-corruption artifact in the corpus.
- **XXE-104000** ($500 JSON): Python `xmlparse_setattro()` type confusion — body is
  `bugs.python.org/issue25019`.

And the native-app row **XXE-10767** (Yahoo! Messenger `emoticons.xml` stack-BOF, **404**) — an
XML config file parsed by a desktop binary; recorded dark.

**Boundary rule**: these belong to the deserialization class — cross-ref
`hunt-deserialization` skill and `../XSS/` only where a gadget chain reaches the browser. An XXE
agent *records* them; it does not claim them.

## 8. The SAML verification boundary — XXE-223014 ($8,500 JSON) and siblings

`XXE-223014` is the roster's second-largest payout, and its team summary names the real class:

> Due to improper SAML verification it was possible to bypass the OneLogin authentication on
> https://uchat.uberinternal.com and gain unauthorized access to internal chats.

SAML **signature-verification** bugs (this row; Nextcloud's php-saml `openssl_verify() -1 → true`
implicit-bool fix XXE-213789, verbatim in-body: *"an error during signature verification is treated
as a successful verification"*) are **auth-class** bugs that ride XML — the SAML-XXE *entity* lane
lives in `Blind-OOB-and-Parameter-Entities.md` §5. Rows XXE-178345/171398/167828 (HackerOne
SSO-SAML open-redirect/CSRF/enumeration) are auth-flow rows entirely. Cross-ref: `hunt-saml`,
`hunt-auth-bypass`.

## 9. The config-disclosure row — XXE-173972 (ok.ru, $100 list)

`web.xml configuration file disclosure` at `*.mycdn.me` — a static WEB-INF exposure, not parser
behavior. Adjacent to the Java-XML carrier story (where `web.xml` lives, SOAP servlets usually
live too) — the *read* of it belongs to path-traversal/config-disclosure lanes. Team summary
verbatim: *"Several source files were accessible at *.mycdn.me"*.

---

# Part III — the boundary table

| Roster cluster | Bug class | Counted as XXE? | Owner |
|---|---|---|---|
| Entity file-read / OOB / exfil | CWE-611 | **Yes** | This vault's three modules |
| XML-RPC protocol abuse | logic/crypto | No (own module) | `XML-RPC-Chains.md` |
| crossdomain.xml | CWE-939 policy | No | This module Part I |
| Parser type confusion / BOF | CWE-843/787 | No | This module Part II → deserialization class |
| SAML verification | CWE-347 | No | `hunt-saml` skill |
| web.xml static exposure | CWE-538 | No | config-disclosure class |

**Cross-references**: `hunt-deserialization` (Part II), `hunt-saml` (§8), `hunt-cors`
(modern successor of Part I's cross-origin policy class), `File-Upload-and-Format-Vectors.md`
(the upload-to-trusted-origin trick family).
