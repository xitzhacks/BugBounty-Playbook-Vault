---
title: "Cert Validation, Weak Secrets & Insecure Channels — the client trusts too much"
type: playbook
category: crypto-cert-validation
cwe: "CWE-295, CWE-321"
source_count: 8
full_bodies_available: 8
corpus: "h1-brain disclosed_reports.db (3,673 rows) · sha256 8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4"
list_accessed: "2026-11-07"
note: "Anchors: CRYPTO-168538 (Twitter iOS no cert validation, $2,100), CRYPTO-903424 (Nextcloud desktop, $300), CRYPTO-327674 (Slack http invite links, $350), CRYPTO-1387366 (k8s weak session secret, $250)."
---

# Cert Validation, Weak Secrets & Insecure Channels

## 1. Overview

Eight rows, **$3,680/7 paid** — the most reliably monetized module in this vault because each row
is a *client-side defect with a user-visible consequence*. Three sub-shapes: the app does not
validate the certificate, the secret is trivially guessable, or the upgrade path is HTTP.

**Case-stock (8 rows / $3,680):**

| Case | Target | Mechanism | Bounty |
|---|---|---|---|
| [CRYPTO-168538](https://hackerone.com/reports/168538) | x | Twitter iOS accepts any TLS cert → OAuth token theft | **$2,100** |
| [CRYPTO-327674](https://hackerone.com/reports/327674) | slack | Invitation reminders use `http://` links | **$350** |
| [CRYPTO-903424](https://hackerone.com/reports/903424) | nextcloud | Desktop client doesn't validate `nextcloud.com` cert | **$300** |
| [CRYPTO-435648](https://hackerone.com/reports/435648) | phabricator | TOTP secret shorter than RFC 4226 minimum | **$300** |
| [CRYPTO-505007](https://hackerone.com/reports/505007) | x | OSS builds resolve deps from untrusted spheres | **$280** |
| [CRYPTO-1387366](https://hackerone.com/reports/1387366) | kubernetes | `elections.k8s.io` Flask `SECRET_KEY = "N/A"` | **$250** |
| [CRYPTO-1039504](https://hackerone.com/reports/1039504) | ibb (OpenVPN) | build deps over HTTP without integrity checks | **$100** |
| [CRYPTO-852841](https://hackerone.com/reports/852841) | nextcloud | reduced permutations in `SecureRandom::generate` | - |

## 2. The mobile cert-validation row that paid $2,100

CRYPTO-168538 is the class's best-written impact: no jailbreak, no added CA, just a stock phone and
a proxy.

> Twitter on iOS newest two versions (6.62 and 6.62.1) are affected, other versions not tested.

> The iPhone were without any mobileconfig profiles installed - *no* we did not install any CA certificate in the CA store of the device. Really stock iPhones. The Twitter app does not check the SSL/TLS certificate of https://api.twitter.com .

The explicit "no, I did not install a CA" line is what makes the report uncontestable — copy that
discipline into every client cert finding.

## 3. Guessable secrets

CRYPTO-1387366 gives a reusable detection method plus the exact finding:

> @nagli and I discovered that `elections.k8s.io` uses a weak Flask SECRET_KEY, literally the string `N/A`, to sign authentication cookies.

The report also names its tooling ("CookieMonster") — a cheap way to make the methodology
reproducible. CRYPTO-435648 is the standards-based sibling: a 16-character base32 TOTP secret against
RFC 4226's 128-bit minimum / 160-bit recommendation.

## 4. Insecure channels

- CRYPTO-327674: `http://click.email.slack-core.com/?qs=…` — the click-through is downgradeable:

> The links in these reminders are http links.

- CRYPTO-1039504: build jobs fetch dependencies over `http` and check nothing:

> This opens the door to person-in-the-middle attacks, whereby an attacke

- CRYPTO-505007: the same problem generalized to a whole OSS organization (CWE-829 / CWE-494 tags in
  the body).

## 5. What pays, what doesn't

- **Paid**: a demonstrated interception (token/cookie captured) or a directly guessable secret that
  signs auth state.
- **Weak**: "the app uses SHA-1" without a break; `SecureRandom` charset reduction (CRYPTO-852841
  paid nothing, and the body itself argues the numbers remain unpredictable).
- Bring the proxy log or the forged cookie; the corpus's paid rows all do.

## 6. Cross-references

- `01_TLS-STARTTLS-Legacy-Protocol.md` — server-side transport failures.
- `02_Crypto-Primitives-Oracles-Signatures.md` — primitive-level breaks.
- `../18_Misconfiguration/` — header/HSTS rows that overlap.
