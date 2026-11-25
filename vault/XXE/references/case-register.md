---
title: "XXE/XML case register — row-per-row disposition ledger"
type: ledger
generated: "2026-10-27"
rows: 44
case_id_scheme: "XXE-<HackerOne report id>"
dispositions: "full-body+classified (13) · metadata-only (8) · 404-dead (9) · adjacent-class (13) · pattern-noise (1)"
bounty_rule: "JSON bounty_amount where present, else h1.security.nathan.sx list-stated, visibly labeled"
---

# Case Register — XXE/XML corpus

Source roster: [`source-index.md`](source-index.md) (h1.security.nathan.sx, 44 pattern-matched rows from 4,419).
Bodies cached verbatim in [`archive/xxe-bodies-2026-10-27.txt`](archive/xxe-bodies-2026-10-27.txt); raw JSON in [`archive/h1-json-cache/`](archive/h1-json-cache/).

## A. Core XXE rows (22) — the class itself

| Case ID | Report | Team | Bounty | Disposition | Module |
|---|---|---|---|---|---|
| XXE-248668 | XXE on sms-be-vip.twitter.com in SXMP Processor | Twitter | **$10,080** list / JSON withholds (has_bounty=true) | full-body | In-Band-File-Read |
| XXE-232614 | Uploaded XLF files result in External Entity Execution | Weblate | — | full-body | File-Upload-and-Format-Vectors |
| XXE-229980 | XML entity expansion using svg file | Trello | — | **404** | File-Upload-and-Format-Vectors (recorded) |
| XXE-188743 | XXE on DoD web server | U.S. Dept Of Defense | — | metadata-only (sev **critical**, body withheld) | — |
| XXE-154096 | Blind OOB XXE At "http://ubermovement.com/" | Uber ★ | **$500** JSON | full-body | Blind-OOB-and-Parameter-Entities |
| XXE-142562 | [RCE] Unserialize to XXE — file disclosure on ams.upload.pornhub.com | Pornhub | **$10,000** list / **404** | **404** | recorded; chain anatomy in In-Band §6 |
| XXE-130661 | XXE issue | Moneybird | — | metadata-only (team summary: SVG upload XXE) | File-Upload-and-Format-Vectors |
| XXE-112116 | XXE in the Connector Designer | Bime | **$750** list | metadata-only (team summary: read arbitrary files) | In-Band-File-Read |
| XXE-106865 | [rev-app.informatica.com] — XXE via SAML | Informatica | — | full-body | Blind-OOB (SAML carrier §5) |
| XXE-106802 | [marketplace.informatica.com] — XXE | Informatica | — | **404** | recorded ( Informatica cluster) |
| XXE-106797 | [marketplace.informatica.com] — XXE | Informatica | — | full-body | In-Band-File-Read |
| XXE-105980 | XXE at host vpn.owncloud.com | ownCloud | — | full-body | Blind-OOB-and-Parameter-Entities |
| XXE-105787 | XXE in upload file feature | Informatica | — | metadata-only (team summary) | File-Upload-and-Format-Vectors |
| XXE-105753 | [app.informaticaondemand.com] XXE | Informatica | — | full-body | Blind-OOB (FTP exfil §4) |
| XXE-105434 | [rev-app.informatica.com] — XXE | Informatica | — | full-body | File-Upload-and-Format-Vectors (XLSX) |
| XXE-104620 | XXE in OAuth2 Applications gallery profile App logo | Coinbase | — | full-body (informative) | File-Upload-and-Format-Vectors (SVG-as-jpg) |
| XXE-99279 | XML External Entity (XXE) in qiwi.com + waf bypass | QIWI | **$3,137** list / **404** | **404** | recorded; WAF-bypass figure |
| XXE-72272 | Multiple endpoints are vulnerable to XML External Entity injection (XXE) | Pornhub | **$2,500** list / **404** | **404** | recorded |
| XXE-55431 | XML Parser Bug: XXE over which leads to RCE | drchrono | **$700** list | full-body | File-Upload-and-Format-Vectors (C-CDA) |
| XXE-36450 | [send.qiwi.ru] Soap-based XXE vulnerability /soapserver/ | QIWI | **$1,000** list / **404** | **404** | recorded (SOAP figure) |
| XXE-12583 | XXE and SSRF on webmaster.mail.ru | Mail.Ru | **$700** list / **404** | **404** | recorded (XXE→SSRF figure) |
| XXE-8091 | Full Path Disclosure / Info Disclosure in Importing XML Section! | Localize | — | full-body | File-Upload-and-Format-Vectors (import error path) |

## B. XML-RPC rows (4) — module: XML-RPC-Chains

| Case ID | Report | Team | Bounty | Disposition |
|---|---|---|---|---|
| XXE-138869 | OneLogin authentication bypass on WordPress sites via XMLRPC | Uber ★ | **$7,000** JSON | full-body |
| XXE-107296 | Possible Timing Side-Channel in XMLRPC Verification | Automattic | **$50** list | full-body |
| XXE-96294 | DDOS using xmlrpc.php | withinsecurity | — | full-body (pingback DDoS shape) |
| XXE-146093 | WordPress Vulnerabilities: … XML-RPC Interface available | Nextcloud | — | full-body (informative exposure) |

## C. SAML rows (5) — adjacent class → `../SQLi`-style boundary: these are auth-flow bugs, XXE lens only

| Case ID | Report | Team | Bounty | Disposition |
|---|---|---|---|---|
| XXE-223014 | SAML Authentication Bypass on uchat.uberinternal.com | Uber ★ | **$8,500** JSON | metadata-only (body withheld; team summary quotes improper SAML verification) |
| XXE-213789 | Update php-saml library to 2.10.5 | Nextcloud | — | full-body (openssl_verify() -1→true implicit bool) |
| XXE-178345 | Limited Open redirection using SSO-SAML | HackerOne ★ | — | full-body |
| XXE-171398 | (HackerOne SSO-SAML) Login CSRF, Open Redirect, Self-XSS | HackerOne ★ | — | full-body |
| XXE-167828 | Ability to enumerate private programs using SAML | HackerOne ★ | — | metadata-only |

## D. crossdomain.xml rows (6) — module: Crossdomain-and-Parser-Adjacents

| Case ID | Report | Team | Bounty | Disposition |
|---|---|---|---|---|
| XXE-105655 | [crossdomain.xml] Dangerous Flash Cross-Domain Policy | Pornhub | **$50** list / **404** | **404** |
| XXE-96662 | crossdomain.xml too permissive on eu1/us1.badoo.com | Badoo | **$310** list | full-body (SWF upload → full session read) |
| XXE-105463 | risk of having secure=false in a crossdomain.xml | Imgur | **$150** list | full-body |
| XXE-91604 | Crossdomain.xml settings on api.imgur.com too open | Imgur | **$50** list | metadata-only |
| XXE-44652 | Insecure crossdomain.xml | Mobile Vikings | — | full-body (`domain="*"`) |
| XXE-43070 | Misconfigured crossdomain.xml - vimeo.com | Vimeo | — | full-body (the doctrine: three-conditions test) |

## E. XML-parser-internals rows (5) — adjacent class (deserialization/memory; XML carrier)

| Case ID | Report | Team | Bounty | Disposition |
|---|---|---|---|---|
| XXE-55030 | SoapClient's __call() type confusion through unserialize() | PHP (IBB) | **$2,500** list | full-body |
| XXE-104010 | SOAP serialize_function_call() type confusion / RCE | PHP (IBB) | **$1,500** list | full-body (bugs.php.net/70388 pointer) |
| XXE-104000 | Python xmlparse_setattro() Type Confusion | Python (IBB) | **$500** JSON | full-body (bugs.python.org/25019 pointer) |
| XXE-73245 | Type Confusion Vulnerability in SoapClient | PHP (IBB) | **$500** list | full-body (full fake-HashTable exploit body) |
| XXE-10767 | Yahoo! Messenger emoticons.xml shortcut Value Handling Stack-BOF | Yahoo! | — | **404** (native-app XML surface) |

## F. Adjacent info-disclosure (1) + noise (1)

| Case ID | Report | Team | Bounty | Disposition |
|---|---|---|---|---|
| XXE-173972 | web.xml configuration file disclosure | ok.ru | **$100** list | metadata-only (WEB-INF static exposure — config-disclosure class, not XXE) |
| XXE-223367 | CSRF — Changing full name / secondary email via GET | Weblate | — | **noise** (title/body contain no XML term; matched the roster filter accidentally; pure CSRF case) |

## Bounty reconciliation

| Band | Amount | Composition |
|---|---:|---|
| JSON-verified | **$16,500** | 4 rows: 154096 $500 · 138869 $7,000 · 223014 $8,500 · 104000 $500 |
| List-stated, retrievable | **$16,340** | 11 rows: 248668 $10,080 · 55030 $2,500 · 104010 $1,500 · 112116 $750 · 55431 $700 · 173972 $100 · 96662 $310 · 105463 $150 · 73245 $500 · 107296 $50 · 91604 $50 |
| **Retrievable total** | **$32,840** | 35 rows |
| List-stated on 404 rows | **$17,387** | 6 rows with figures: 142562 $10,000 · 99279 $3,137 · 72272 $2,500 · 36450 $1,000 · 12583 $700 · 105655 $50 (229980, 106802, 10767 list no bounty) |
| **Grand total (list)** | **$50,227** | 44 rows — reconciles to the extracted roster |
