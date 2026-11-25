---
title: "crypto case register — 46-row ledger (h1-brain corpus)"
type: register
built: "2026-11-07"
corpus: "h1-brain disclosed_reports.db (3,673 rows; sha256 8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4)"
case_id_scheme: "CRYPTO-<HackerOne report id>"
bounty_rule: "DB bounty_amount where present · '-' = no figure in DB (not evidence of non-payment)"
module_rule: "frozen in archive/classes.json"
---

# Case register — crypto

Corpus: 46 rows · 36 with bounty figures · **$55,105**.

Module census: crypto-primitives-oracles-signatures 10 rows/6 paid/$6,425 · tls-starttls-legacy-protocol 7 rows/2 paid/$1,500 · _adjacent 1 rows/1 paid/$100 · cert-validation-weak-secrets-insecure-channel 8 rows/7 paid/$3,680 · _adjacent_unclassified 20 rows/20 paid/$43,400.

| Case | Program | Bounty | Module | CVE | Title |
|---|---|---|---|---|---|
| [CRYPTO-126203](https://hackerone.com/reports/126203) | uber | $500 | crypto-primitives-oracles-signatures | - | CBC "cut and paste" attack may cause Open Redirect(even XSS) |
| [CRYPTO-144782](https://hackerone.com/reports/144782) | ibb | $1,000 | tls-starttls-legacy-protocol | CVE-2016-0772 | CVE-2016-0772 - python: smtplib StartTLS stripping attack |
| [CRYPTO-151868](https://hackerone.com/reports/151868) | algolia | $100 | _adjacent | - | No Rate Limit In Inviting Similar Contact Multiple Times |
| [CRYPTO-166629](https://hackerone.com/reports/166629) | ibb | - | tls-starttls-legacy-protocol | CVE-2016-0800 | Cross-protocol attack on TLS using SSLv2 (DROWN) (CVE-2016-0800) |
| [CRYPTO-166634](https://hackerone.com/reports/166634) | ibb | - | tls-starttls-legacy-protocol | CVE-2015-3197 | SSLv2 doesn't block disabled ciphers (CVE-2015-3197) |
| [CRYPTO-168538](https://hackerone.com/reports/168538) | x | $2,100 | cert-validation-weak-secrets-insecure-channel | CVE-2016-10511 | Twitter iOS fails to validate server certificate and sends oauth token |
| [CRYPTO-170548](https://hackerone.com/reports/170548) | ruby | $500 | _adjacent_unclassified | - | Ruby OpenSSL Library - IV Reuse in GCM Mode |
| [CRYPTO-213437](https://hackerone.com/reports/213437) | ibb | $1,000 | crypto-primitives-oracles-signatures | - | Critical vulnerability in JSON Web Encryption (JWE) - RFC 7516 Invalid C |
| [CRYPTO-251572](https://hackerone.com/reports/251572) | zomato | $100 | crypto-primitives-oracles-signatures | - | Length extension attack leading to HTML injection |
| [CRYPTO-275269](https://hackerone.com/reports/275269) | rubygems | - | crypto-primitives-oracles-signatures | - | Gem signature forgery |
| [CRYPTO-277534](https://hackerone.com/reports/277534) | iandunn-projects | $25 | crypto-primitives-oracles-signatures | - | Timing Attack in Google Authenticator - Per User Prompt |
| [CRYPTO-288966](https://hackerone.com/reports/288966) | x | - | tls-starttls-legacy-protocol | CVE-2014-3566 | POODLE SSLv3 bug on multiple twitter smtp servers (mx3.twitter.com,199.5 |
| [CRYPTO-327674](https://hackerone.com/reports/327674) | slack | $350 | cert-validation-weak-secrets-insecure-channel | - | Invitation reminder emails contain insecure links |
| [CRYPTO-435648](https://hackerone.com/reports/435648) | phabricator | $300 | cert-validation-weak-secrets-insecure-channel | - | TOTP Key is shorter than RFC 4226 recommended minimum |
| [CRYPTO-505007](https://hackerone.com/reports/505007) | x | $280 | cert-validation-weak-secrets-insecure-channel | - | [Twitter Open Source] Releases were & are built/executed/tested/released |
| [CRYPTO-728110](https://hackerone.com/reports/728110) | deptofdefense | $3,000 | crypto-primitives-oracles-signatures | CVE-2018-2879 | [HTAF4-213] [Pre-submission] CVE-2018-2879 (padding oracle attack in the |
| [CRYPTO-745276](https://hackerone.com/reports/745276) | ibb | - | crypto-primitives-oracles-signatures | CVE-2019-9498, CVE-2019-9499, CVE-2019-11235, CVE-2019-9497, CVE-2019-11234, CVE-2019-13377, CVE-2019-13456 | Dragonblood: Design and Implementation Flaws in WPA3 and EAP-pwd |
| [CRYPTO-852841](https://hackerone.com/reports/852841) | nextcloud | - | cert-validation-weak-secrets-insecure-channel | CVE-2020-8173 | Reduced purmations on encryption |
| [CRYPTO-896299](https://hackerone.com/reports/896299) | github-security-lab | $1,800 | _adjacent_unclassified | - | Java: CWE-297 Insecure JavaMail SSL configuration |
| [CRYPTO-903424](https://hackerone.com/reports/903424) | nextcloud | $300 | cert-validation-weak-secrets-insecure-channel | CVE-2021-22895 | SSL certificate not validated when registering with a provider |
| [CRYPTO-917454](https://hackerone.com/reports/917454) | github-security-lab | $1,800 | _adjacent_unclassified | - | Java: CWE-273 Unsafe certificate trust |
| [CRYPTO-917456](https://hackerone.com/reports/917456) | github-security-lab | $1,800 | _adjacent_unclassified | - | [Java] CWE-295 - Incorrect Hostname Verification - MitM |
| [CRYPTO-953219](https://hackerone.com/reports/953219) | portswigger | - | tls-starttls-legacy-protocol | CVE-2011-0411 | SMTP interaction theft via MITM |
| [CRYPTO-1039504](https://hackerone.com/reports/1039504) | ibb | $100 | cert-validation-weak-secrets-insecure-channel | - | Some build dependencies are downloaded over an insecure channel (without |
| [CRYPTO-1094343](https://hackerone.com/reports/1094343) | github-security-lab | $4,500 | _adjacent_unclassified | - | [Java] CWE-326: Query to detect weak encryption with an insufficient key |
| [CRYPTO-1100379](https://hackerone.com/reports/1100379) | github-security-lab | $1,800 | _adjacent_unclassified | - | [Java] CWE-295: Disabled certificate validation in JXBrowser |
| [CRYPTO-1123360](https://hackerone.com/reports/1123360) | github-security-lab | $1,800 | _adjacent_unclassified | - | [Java] CWE-327: Add more broken crypto algorithms |
| [CRYPTO-1130416](https://hackerone.com/reports/1130416) | kubernetes | - | crypto-primitives-oracles-signatures | - | SHA512 incorrect on most/many releases |
| [CRYPTO-1161808](https://hackerone.com/reports/1161808) | github-security-lab | $1,000 | _adjacent_unclassified | - | [Java] CWE-759: Query to detect password hash without a salt |
| [CRYPTO-1178562](https://hackerone.com/reports/1178562) | ruby | $500 | tls-starttls-legacy-protocol | CVE-2021-32066, CVE-2016-0772 | imap: StartTLS stripping attack (CVE-2016-0772). |
| [CRYPTO-1184041](https://hackerone.com/reports/1184041) | github-security-lab | $4,500 | _adjacent_unclassified | - | [JAVA]: CWE-347 - Improper Verification of Cryptographic Signature : Pot |
| [CRYPTO-1212272](https://hackerone.com/reports/1212272) | github-security-lab | $1,800 | _adjacent_unclassified | - | [GO]: CWE-326: Insufficient key size |
| [CRYPTO-1212274](https://hackerone.com/reports/1212274) | github-security-lab | $4,000 | _adjacent_unclassified | - | [JAVA]: CWE-347 - Improper Verification of Cryptographic Signature : Pot |
| [CRYPTO-1219493](https://hackerone.com/reports/1219493) | github-security-lab | $4,000 | _adjacent_unclassified | - | [Java] CWE-295 - Incorrect Hostname Verification - MitM |
| [CRYPTO-1238470](https://hackerone.com/reports/1238470) | ibb | - | crypto-primitives-oracles-signatures | CVE-2020-26140, CVE-2020-26143, CVE-2020-26145, CVE-2020-26144, CVE-2020-26139, CVE-2020-26146, CVE-2020-26147, CVE-2020-26142, CVE-2020-26141, CVE-2020-24588, CVE-2020-24587, CVE-2020-24586 | Fragmentation and Aggregation Flaws in Wi-Fi |
| [CRYPTO-1250306](https://hackerone.com/reports/1250306) | github-security-lab | $1,800 | _adjacent_unclassified | - | [Java]: CWE 295 - Insecure TrustManager - MiTM |
| [CRYPTO-1264781](https://hackerone.com/reports/1264781) | github-security-lab | $1,500 | _adjacent_unclassified | - | [Java]: CWE 295 - Insecure TrustManager - MiTM |
| [CRYPTO-1329260](https://hackerone.com/reports/1329260) | github-security-lab | $1,800 | _adjacent_unclassified | - | Java: Static initialization vector |
| [CRYPTO-1334763](https://hackerone.com/reports/1334763) | curl | - | tls-starttls-legacy-protocol | CVE-2021-22947 | CVE-2021-22947: STARTTLS protocol injection via MITM |
| [CRYPTO-1387366](https://hackerone.com/reports/1387366) | kubernetes | $250 | cert-validation-weak-secrets-insecure-channel | - | elections.k8s.io uses weak session secret key, may place elections at ri |
| [CRYPTO-1481247](https://hackerone.com/reports/1481247) | github-security-lab | $1,800 | _adjacent_unclassified | - | Java: An experimental query for ignored hostname verification |
| [CRYPTO-1484086](https://hackerone.com/reports/1484086) | github-security-lab | $1,800 | _adjacent_unclassified | - | [C#] CWE-759: Query to detect password hash without a salt |
| [CRYPTO-1490400](https://hackerone.com/reports/1490400) | github-security-lab | $1,800 | _adjacent_unclassified | - | Python: CWE-338 insecureRandomness |
| [CRYPTO-1567588](https://hackerone.com/reports/1567588) | github-security-lab | $1,800 | _adjacent_unclassified | - | [Java]: CWE-321 - Query to detect hardcoded JWT secret keys |
| [CRYPTO-1710575](https://hackerone.com/reports/1710575) | github-security-lab | $1,800 | _adjacent_unclassified | - | [CPP]: Add query for CWE-297: Improper Validation of Certificate with Ho |
| [CRYPTO-2038484](https://hackerone.com/reports/2038484) | ibb | $1,800 | crypto-primitives-oracles-signatures | CVE-2023-30590 | DiffieHellman doesn't generate keys after setting a key |
