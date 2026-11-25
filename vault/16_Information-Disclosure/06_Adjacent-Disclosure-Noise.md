---
title: "Adjacent Disclosure Noise — chain origins, mislabels, and the $50,000 merge"
type: playbook
category: adjacent-disclosure-noise
cwe: ""
source_count: 41
full_bodies_available: 35
corpus: "h1-brain disclosed_reports.db (sha256 8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4) — 362 rows"
list_accessed: "2026-11-07"
note: "Merged _adjacent (19) + _adjacent_unclassified (22). Anchors: INFO-1087489 (shopify, $50,000), INFO-1122661 (github-security-lab, $4,500, metadata-only), INFO-73276 (ibb, $2,000), INFO-1054382 (portswigger, $1,000), INFO-1276373 (algolia, $0), INFO-2193454 (khealth, $0). All quotes byte-true to references/archive/INFO-bodies-full-dump.txt."
---

# Adjacent Disclosure Noise — chain origins, mislabels, and the $50,000 merge

## 1. Overview

The vault's closing module merges two classifier pools that could not be assigned to the five class modules: **19 `_adjacent` rows** (in-bucket but not classifiable — SSRF/DNS-rebinding chains, Flash sandbox escapes, auth bypasses whose *origin* is disclosure) and **22 `_adjacent_unclassified` rows** (drawn from the classifier's `unclassified` pool — webhook-style merges the module map grouped for this vault: hardcoded mobile secrets, GitHub-Security-Lab one-liners, `.htpasswd`/`.htaccess` singles). Combined: **41 rows, $67,914/17 paid**. The module holds the vault's single largest bounty (INFO-1087489, **$50,000**) and its most metadata-bound rows (six GitHub-Security-Lab one-liners) — the widest variance in the vault, which is exactly why it is last, not first. A reader who trusts this module's numbers without its provenance will misprice everything else.

**Case-stock (41 rows / $67,914):**

| Case | Target | Mechanism | Bounty |
|---|---|---|---|
| [INFO-1087489](https://hackerone.com/reports/1087489) | shopify | Github access token exposure | $50,000 |
| [INFO-1122661](https://hackerone.com/reports/1122661) | github-security-lab | [Java] CWE-312: Query to detect cleartext storage of sensitive information usi… | $4,500 |
| [INFO-73276](https://hackerone.com/reports/73276) | ibb | Internet-based attacker can run Flash apps in local sandboxes by using special… | $2,000 |
| [INFO-1026252](https://hackerone.com/reports/1026252) | github-security-lab | [Java] CWE-927: Sensitive broadcast | $1,800 |
| [INFO-1122662](https://hackerone.com/reports/1122662) | github-security-lab | [Java] CWE-598: Use of GET Request Method with Sensitive Query Strings | $1,800 |
| [INFO-1365761](https://hackerone.com/reports/1365761) | github-security-lab | [Java] CWE-200: Query to detect exposure of sensitive information from android… | $1,800 |
| [INFO-1526609](https://hackerone.com/reports/1526609) | github-security-lab | [Java]: CWE-200 - Query to detect insecure WebResourceResponse implementation | $1,800 |
| [INFO-1054382](https://hackerone.com/reports/1054382) | portswigger | HTML Injection in Swing can disclose netNTLM hash or cause DoS | $1,000 |
| [INFO-532225](https://hackerone.com/reports/532225) | zomato | [Zomato Order] Insecure deeplink leads to sensitive information disclosure | $750 |
| [INFO-418474](https://hackerone.com/reports/418474) | security | Disclosing a private program in an external link if program is paused | $500 |
| [INFO-669438](https://hackerone.com/reports/669438) | security | [Bypass #645264] Report title disclosure despite the program settings for emai… | $500 |
| [INFO-886287](https://hackerone.com/reports/886287) | github-security-lab | Java: CWE-532 sensitive info logging | $500 |
| [INFO-1584718](https://hackerone.com/reports/1584718) | shopify | Information disclosure ( Google Sales Channel ) | $500 |
| [INFO-2733994](https://hackerone.com/reports/2733994) | portswigger | cgi scripts wordlist entry for windmail.exe has payload that sends arbitrary f… | $200 |
| [INFO-53004](https://hackerone.com/reports/53004) | coinbase | Blacklist bypass on Callback URLs | $100 |
| [INFO-248599](https://hackerone.com/reports/248599) | coinbase | Information disclosure same issue #176002 | $100 |
| [INFO-228377](https://hackerone.com/reports/228377) | discourse | SSRF in upload IMG through URL | $64 |
| [INFO-207321](https://hackerone.com/reports/207321) | shopify-scripts | Controlled address leak due to type confusion - ASLR bypass | - |
| [INFO-219197](https://hackerone.com/reports/219197) | x | [██████████.gnip.com] .htpasswd disclosure | - |
| [INFO-221328](https://hackerone.com/reports/221328) | x | HTTP 401 response injection on "amp.twimg.com/amplify-web-player/prod/source.h… | - |
| [INFO-237381](https://hackerone.com/reports/237381) | automattic | SSRF and local file disclosure in https://wordpress.com/media/videos/ via FFmp… | - |
| [INFO-271506](https://hackerone.com/reports/271506) | security | Banned researcher gets email updates on a private program. | - |
| [INFO-331489](https://hackerone.com/reports/331489) | nextcloud | Extremly simple way to bypass Nextcloud-Client PIN/Fingerprint lock | - |
| [INFO-351555](https://hackerone.com/reports/351555) | reverb | Disclosure of all uploads to Cloudinary via hardcoded api secret in Android ap… | - |
| [INFO-356566](https://hackerone.com/reports/356566) | security | HackerOne support disclosing report state without checking user identity | - |
| [INFO-389454](https://hackerone.com/reports/389454) | starbucks | Backup Source Code Detected | - |
| [INFO-391385](https://hackerone.com/reports/391385) | yelp | Unauthorized Use of Victim Credit Card | - |
| [INFO-503300](https://hackerone.com/reports/503300) | unikrn | █████████ on CRM server without authorization | - |
| [INFO-629892](https://hackerone.com/reports/629892) | grammarly | Lack of CSRF header validation at https://g-mail.grammarly.com/profile | - |
| [INFO-663729](https://hackerone.com/reports/663729) | brave | [Brave browser] WebTorrent has DNS rebinding vulnerability | - |
| [INFO-803141](https://hackerone.com/reports/803141) | nordsecurity | Unauthorized User Can Delete Any User Account | - |
| [INFO-1067547](https://hackerone.com/reports/1067547) | automattic | Unauthenticated access to webmail at maildev.happytools.dev leading to comprom… | - |
| [INFO-1101882](https://hackerone.com/reports/1101882) | curl | CVE-2021-22876: Automatic referer leaks credentials | - |
| [INFO-1102546](https://hackerone.com/reports/1102546) | shopify | Is the Google Bucket Meant To Be Publicly Listable? https://cdn.shopify.com/sh… | - |
| [INFO-1241849](https://hackerone.com/reports/1241849) | basecamp | Information Disclosure .htaccess accesible for public | - |
| [INFO-1276373](https://hackerone.com/reports/1276373) | algolia | Information disclosure -> 2fa bypass -> POST exploitation | - |
| [INFO-1342422](https://hackerone.com/reports/1342422) | basecamp | Subdomain Takeover due to ████████ NS records at us-east4.37signals.com | - |
| [INFO-2053396](https://hackerone.com/reports/2053396) | mozilla | Possibility of Deface through translation tool - www.mozilla.com | - |
| [INFO-2193454](https://hackerone.com/reports/2193454) | khealth | Information disclouser from URL parameter "access" lead to Account Takeover | - |
| [INFO-2264960](https://hackerone.com/reports/2264960) | exness | Unrestricted Access to Celery Flower Instance | - |
| [INFO-2387297](https://hackerone.com/reports/2387297) | mozilla | Bypass Email Verification on Add Email Monitoring | - |

## 2. The $50,000 merge: a token in an employee's app

INFO-1087489 (**shopify, $50,000**) — 528 bytes, the vault's largest bounty and its shortest body per dollar — sits in the unclassified merge because its *title* ("Github access token exposure") is a secret, not a disclosure mechanism:

> While dissecting an application made by one of your employees I found his GitHub Personal Access Token (PAT), he's a member of the org with pull and push access to all of your repositories.

> Read and write access to all your private github repositories.

The proof is a sha512 of a public README at a named commit (`cea9c273391d`) — the corpus's most economical escalation proof — and the price ($50,000) is **2× the bucket max** (INFO-3000510's $25,000). The vault does *not* fold this row into the bucket's headline arithmetic: the bucket-340 max stays $25,000; the 362-row corpus max is $50,000. That distinction is the module's first lesson — a merged pool can dominate a vault's money without belonging to its class bucket. INFO-351555 (reverb, $0, hardcoded Cloudinary secret in `com/reverb/app/CloudinaryFacade.java`) is the same class with no figure — "I was able to access your account data" — and INFO-367581 (in module 02: basic auth still working) shows the secret surviving its own disclosure report.

## 3. The GitHub-Security-Lab sextet: money without bodies

Six rows (INFO-886287, 1026252, 1122661, 1122662, 1365761, 1526609) carry the one-line body `This bug was reported directly to GitHub Security Lab.` and **$13,400 of the module's $67,914** (INFO-1122661 alone $4,500, CWE-312 SharedPreferences cleartext; five others $500–$1,800 for CWE-200/532/598/927 query-detector rows). They are the vault's GHSL anchors: real payouts (a CodeQL-query bounty program), no quotable technique. The module's rule — quoted from the Race vault's discipline — applies: *metadata anchors, not evidence*. Any playbook step that "learns Android cleartext storage from INFO-1122661" would be invention; the step learns it from the CWE title and the five full-body Android rows around it (INFO-377107's `/data/data/` bypass, INFO-532225's deeplink).

## 4. Chain origins: where the disclosure feeds something else

The `_adjacent` pool is the vault's honesty shelf — rows whose *primary* class is elsewhere but whose disclosure leg is real. INFO-53004 (**coinbase, $100**) is a DNS-rebinding blacklist bypass whose disclosure is internal probe pages ("the pages found (:9177/status, :80/_hostmanager/healthcheck, :80/check, ...) are unproctected but not sensitive") — priced at $100 because the leaked content was benign, a clean statement of the vault's content-pricing rule. INFO-228377 (**discourse, $64**, SSRF via PM image URLs) and INFO-237381 (WordPress FFmpeg HLS SSRF+file-disclosure) are SSRF-origin disclosures; INFO-73276 (**ibb, $2,000**) is the Flash sandbox escape that "promote[s] the local sandbox to 'local trusted'" in combination with module 05's CVE-2015-3044 — priced as a *chain component*, not a standalone disclosure. INFO-1276373 (algolia, $0) names the full chain in its title — "Information disclosure -> 2fa bypass -> POST exploitation" — via a leaked `gauth_secret`, and INFO-2193454 (khealth, $0) shows the archive-mined variant: JWTs harvested with `waybackurls` + `grep "eyJ"` from a `sessions` URL parameter, walleted into account takeover ("Account Takeover" is the stated impact). The lesson the module teaches in section 6: **unpriced does not mean unimportant — it means the disclosure leg's price was collected by another class.**

## 5. The unpaid singles: dotfiles, buckets, and token uwu

INFO-219197 (x, `.htpasswd` disclosure on a gnip subdomain — "Protect the htpasswd file"), INFO-1241849 (basecamp, `.htaccess` accessible for public), INFO-389454 (starbucks, backup source code), INFO-1102546 (shopify, publicly listable Google bucket), INFO-1584718 (shopify, Google Sales Channel), INFO-511440's cousins in module 04 (credentials in public) — the cheapest-to-reproduce findings in the entire vault, all unpriced. INFO-1054382 (**portswigger, $1,000**) is the pool's most colorful paid row — Burp Suite proxying HTML-bearing requests renders `<img src>` to an attacker server, leaking the auditor's real IP, NetNTLM hashes (via `file://`), and even relaying SMB to RCE — and INFO-2733994 (**portswigger, $200**) is its joke control: a 20-year-old `windmail.exe` CGI wordlist entry still mailing `C:\boot.ini` to `[REDACTED_EMAIL]`, reported with the request to *remove the entry*, not to fix a server. Both are tool-as-victim disclosures, priced like the Burp user they endanger.

## 6. What pays, what doesn't

- **Pays at the top**: an org-wide credential (GitHub PAT, $50,000) — the vault's max, in a merge pool. The lesson is pool discipline: report vault money with its pool label or the headline misleads.
- **Pays, mid**: chain components with demoed escalation (Flash sandbox promotion $2,000; Burp Suite NetNTLM $1,000; Zomato deeplink $750) and GHSL metadata rows ($13,400/6) whose value is the *program*, not the body.
- **Doesn't pay (here)**: benign-content disclosures (INFO-53004's $100 for "not sensitive" probe pages) — the corpus's pure content-pricing datum. And the dotfile/bucket singles at $0 prove the floor: *reproducible but unpriced* is a publication artifact, not a severity claim. The playbook hunts them first because they are cheap, not because they are rich.

## 7. Cross-references

- Modules 01–05 — this module is the negative space *around* them: every mechanism here belongs to one of those modules' classes by body, and was pooled only because the classifier could not commit. When in doubt, classify by body behavior (the vault's bodies-win rule).
- Companion vaults: `../SSRF/` (INFO-53004, 228377, 237381, 663729), `../Subdomain-Takeover/` (INFO-1342422), `../Authentication-Session/` (INFO-1276373 gauth, 2193454 JWT, 2387297 verification-token), `../Open-Redirect/` / `../CSRF/` share the tail (221328, 629892).
