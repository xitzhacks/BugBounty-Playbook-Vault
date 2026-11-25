---
title: "Adjacent and unclassified merges — other classes, labeled misconfig; the sweep queue"
type: playbook
category: adjacent-unclassified-merges
cwe: ""
source_count: 24
full_bodies_available: 24
corpus: "h1-brain disclosed_reports.db 3,673 rows (sha256 8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4); misconfig bucket (152 rows) + unclassified merges (14 rows)"
list_accessed: "2026-11-07"
note: "24 rows total: 10 bucket-adjacent + 14 unclassified merges. 14 substantive bodies; MISCONF-902970/909374/956967/1053048/1137966/1165198/1241576/1241577/1266540/1595009 are 54-byte GitHub-Security-Lab one-liners (see §3). All blockquotes byte-true."
---

# Adjacent and unclassified merges — other classes, labeled misconfig; the sweep queue

## 1. Overview

Twenty-four rows, **$8,750/10 paid** ($150 bucket-adjacent + $8,600 unclassified merges). This module exists for two honest reasons, and the vault states both up front. **First**, the bucket's classifier placed ten rows under "Violation of Secure Design Principles" whose *bodies* belong to other classes (race conditions, path traversal, XSS, memory corruption, CSRF, client-side DoS, business logic). **Second**, fourteen rows the classifier left in `unclassified` were merged into the misconfig module map by a later sweep (mostly GitHub-Security-Lab one-liners), and the build order puts them in this vault. The module is therefore two things at once: a **negative-space exhibit** (how classifier labels drift from body reality) and a **sweep queue** (real misconfigs still awaiting classification, with payouts already attached). It is the last module by design — like RCE vault module 08, it is where the corpus's mistakes are kept in public.

**Case-stock (24 rows / $8,750):**

| Case | Target | Mechanism | Bounty |
|---|---|---|---|
| [MISCONF-125250](https://hackerone.com/reports/125250) | uber | Surge-price avoidance (client logic) | - |
| [MISCONF-157996](https://hackerone.com/reports/157996) | instacart | Coupon redeem race (multiple redemption) | - |
| [MISCONF-165570](https://hackerone.com/reports/165570) | slack | Survey credit race ($100×N) | - |
| [MISCONF-205481](https://hackerone.com/reports/205481) | wordpress | unzip_file path traversal → code exec | - |
| [MISCONF-207042](https://hackerone.com/reports/207042) | security | Marketo postMessage XSS → form eavesdrop | - |
| [MISCONF-212074](https://hackerone.com/reports/212074) | shopify-scripts | mruby SIGSEGV (mrb_yield_with_class) | - |
| [MISCONF-249319](https://hackerone.com/reports/249319) | gsa_bbp | No API rate limit → parallel DoS ($150) | $150 |
| [MISCONF-334253](https://hackerone.com/reports/334253) | security | CSRF on Apply button (auto-submit) | - |
| [MISCONF-392728](https://hackerone.com/reports/392728) | slack | slack:// URL spawns unlimited desktop processes | - |
| [MISCONF-1877185](https://hackerone.com/reports/1877185) | 8x8-bounty | Unbounded date range → resource exhaustion | - |
| [MISCONF-178293](https://hackerone.com/reports/178293) | shopify | Sign-in-with-Google silently disables 2FA ($1,500) | $1,500 |
| [MISCONF-398797](https://hackerone.com/reports/398797) | starbucks | DVR default creds user/user | - |
| [MISCONF-426165](https://hackerone.com/reports/426165) | zomato | CORS reflects arbitrary Origin + credentials ($550) | $550 |
| [MISCONF-491753](https://hackerone.com/reports/491753) | brave | DMARC missing → From forgery | - |
| [MISCONF-902970](https://hackerone.com/reports/902970) | github-security-lab | Insecure HSTS (GHSL, $250) | $250 |
| [MISCONF-909374](https://hackerone.com/reports/909374) | github-security-lab | Directory listing (GHSL, $1,800) | $1,800 |
| [MISCONF-956967](https://hackerone.com/reports/956967) | github-security-lab | Hardcoded AWS credentials (GHSL, $1,000) | $1,000 |
| [MISCONF-1053048](https://hackerone.com/reports/1053048) | github-security-lab | Cookie Secure flag query (GHSL) | - |
| [MISCONF-1137966](https://hackerone.com/reports/1137966) | github-security-lab | Spring Actuator exposure query (GHSL, $500) | $500 |
| [MISCONF-1165198](https://hackerone.com/reports/1165198) | github-security-lab | Cookie HttpOnly query, Java (GHSL, $1,000) | $1,000 |
| [MISCONF-1241576](https://hackerone.com/reports/1241576) | github-security-lab | Cookie HttpOnly query, Go (GHSL, $1,000) | $1,000 |
| [MISCONF-1241577](https://hackerone.com/reports/1241577) | github-security-lab | Cookie HttpOnly query, JS (GHSL, $1,000) | $1,000 |
| [MISCONF-1266540](https://hackerone.com/reports/1266540) | github-security-lab | CORS misconfig query, Go (GHSL) | - |
| [MISCONF-1595009](https://hackerone.com/reports/1595009) | github-security-lab | Hardcoded JWT secret, Go (GHSL) | - |

## 2. The bucket-adjacent ten: bodies that outvoted the label

All ten carry the DB label "Violation of Secure Design Principles" (the bucket's src column), and all ten are something else when read:

- **Race conditions** — MISCONF-157996 (instacart: "There exists a race condition in redeeming coupons, allowing a user to redeem the same coupon multiple times"), MISCONF-165570 (slack: survey credited $200 for two async requests; POC literally `(command) & (command)`). Both are the Race-Conditions vault's canon, cited here as a classification-drift exhibit.
- **Path traversal → code execution** — MISCONF-205481 (wordpress `unzip_file`): "Extracting untrusted zip files using this function this could lead to code execution through placing arbitrary PHP files in the DocumentRoot of the webserver."
- **XSS** — MISCONF-207042 (security/Marketo): a `postMessage` frame-jump → cross-origin iframe XSS → contact-form eavesdropping. The body opens: "There's a scenario where the Marketo Forms solution … can actually be abused … to trigger an XSS in the Cross-Origin-iframe."
- **Memory corruption** — MISCONF-212074 (shopify-scripts): a one-function mruby PoC (`def a; instance_exec (){return}; a()ensure; end; a`) ending in SIGSEGV. The RCE vault's mruby crest exists in the misconfig bucket by label inertia.
- **CSRF** — MISCONF-334253 (security): "this button have no any validations/check protect for CSRF bug … which can lead to auto apply to program by used this link."
- **Business logic / resource consumption** — MISCONF-125250 (uber surge avoidance: change the pickup location on the confirmation screen, keep the non-surge fare), MISCONF-392728 (slack:// URL handler spawning desktop processes until freeze), MISCONF-1877185 (unbounded date range → server resource exhaustion, "the server will respond late as you increase the date range and the response size will increase a lot").
- **Rate limiting (the one true misconfig in the ten)** — MISCONF-249319 (gsa_bbp, **$150**): the Federalist API with no throttling and parallel execution ("Executing of 1000 parallel GET requests … lead to the complete instance inaccessibility"). It is filed adjacent because its *blast-radius framing* (theoretical DoS, "it can be a problem, or it not") reads more like a hardening complaint — and it is the only bucket-adjacent row with money, which is why the module keeps it as the pricing exhibit for "unbounded consumption."

## 3. The fourteen merges: real misconfigs, one-line bodies

The merge set is the primitive "unclassified pool" from `classified.json` (468 rows), matched by `module_map_all.json` to misconfig themes. Four are substantive; ten are GitHub Security Lab rows whose entire body is the same sentence:

> This bug was reported directly to GitHub Security Lab.

Their technique content is zero — title + bounty only, like the Race-Conditions vault's GHSL rows (RACE-1301753/1496268/1943049). The module teaches them as the corpus's most important *negative* fact about unclassified merges: **their payouts aggregate to $5,550 (909374 $1,800; 956967 $1,000; 1165198/1241576/1241577 $1,000 each; 1137966 $500; 902970 $250) with no quotable technique in the DB.** They are priced telemetry for "CodeQL query shipped" programs, not playbook doctrine; the titles, however, are a valid sweep queue:

| Title signal | LANG/query | Payout record |
|---|---|---|
| `CWE-548 J2EE directory listing` | Java | $1,800 |
| `CWE-798 hardcoded AWS credentials` | Java | $1,000 |
| `CWE-1004 cookie without HttpOnly ×3` | Java / Go / JavaScript | $1,000 each |
| `CWE-016 Spring Actuator exposure` | Java | $500 |
| `CWE-523 insecure HSTS` | Java | $250 |
| `CWE-614 cookie without Secure` | JavaScript | — |
| `CORS misconfiguration query` | Go | — |
| `Hardcoded JWT signing secret` | Go | — |

## 4. The four substantive merges: what the sweep found

- **Silent 2FA removal** — MISCONF-178293 (shopify, **$1,500**, merges' crown): enabling "Sign In with Google" at a store admin silently disables Google-Authenticator 2FA ("no two factor code is required and you directly land in Admin Panel … There is no indication to via mail or notification that Two Factor Authorisation has been disabled"). This is the correct home of the module-02 §3 finding; the merge queue is where it was caught.
- **CORS reflection with credentials** — MISCONF-426165 (zomato, **$550**): the attacker origin `developersxzomato.com` is reflected with `Access-Control-Allow-Credentials: true` over `*.zomato.com`. The body is the corpus's most complete CORS PoC (request/response + XHR-withCredentials console exploit) and slots directly into module 03 §4.
- **Default credentials** — MISCONF-398797 (starbucks DVR, no figure): `user`/`user` gains "full administrator access" to a store camera system. This is the only default-cred row in the vault's 166, and it is the row that proves default-credential scanning belongs in the misconfig sweep even though the classifier never bucketed it.
- **DMARC missing** — MISCONF-491753 (brave, no figure): no DMARC record → `From` forgery. Mail-authentication posture is the unclassified pool's third teaching: DKIM/SPF/DMARC inventory is a legitimate misconfig play and zero bodies in the classified bucket cover it.

## 5. What pays, what doesn't

- **Pays ($1,500/$550/$250/$1,000×3/$500/$1,800/$150):** the merges' substantive rows ($2,050) and the GHSL one-liners ($5,550) pay on *title+mechanism* with no readable technique; the bucket-adjacent ten pay exactly one row ($150). **The module's pricing lesson is the vault's most counterintuitive one:** for unclassified merges, the classifier's delay *is* the bounty — the program paid for query-shipped fixes before any hunter classified them.
- **What doesn't:** the nine bucket-adjacent rows carry no figure. Their technique rows (race, traversal, XSS, mruby crash) are taught as the drift exhibit — right technique, wrong bucket — and the register keeps the buckets' labels verbatim ("Violation of Secure Design Principles") so nobody re-files them from memory of the label.

## 6. Cross-references

- Vault `Race-Conditions/` (RACE-157996/165570 → this §2): the coupon/survey races are that vault's canon; MISCONF-249319 is the race vault's theoretical-DoS boundary case.
- Vault `20_Rate-Limiting/` cross-cite for MISCONF-249319 (§2) and module 02 §4 — the two rate-limit rows the classifier split across buckets.
- Module 03 (§4): MISCONF-426165 is filed here by merge but is module 03's CORS doctrine with the paid receipt — cite both.
- Module 02 (§3): MISCONF-178293 (silent 2FA removal) is the merges' crown and belongs in any 2FA checklist alongside MISCONF-587910.
- Playbook P5 — the adjacent module is the playbook's kill-gate source: right technique in the wrong bucket still needs the right blast radius, which eight of these ten rows never state.
