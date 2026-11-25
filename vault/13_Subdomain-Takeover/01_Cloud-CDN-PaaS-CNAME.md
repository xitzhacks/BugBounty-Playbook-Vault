---
title: "Cloud / CDN / PaaS CNAME — unclaimed S3/CloudFront/Heroku claim"
type: playbook
category: subdomain-takeover
cwe: "CWE-16"
source_count: 7
full_bodies_available: 7
corpus: "h1-brain disclosed_reports.db (3,673 rows; sha256 8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4)"
list_accessed: "2026-11-07"
note: "Anchor bodies: SDTO-352869 (grab, $1,000), SDTO-207576 (shopify, $500), SDTO-424669 (shopify, $500), SDTO-317005 (gsa_bbp, $150). Claims trace to bodies read 2026-11-07."
---

# Cloud / CDN / PaaS CNAME — unclaimed S3/CloudFront/Heroku claim

## 1. Overview

Seven corpus cases where a subdomain CNAMEs into cloud infrastructure that no longer exists: the DNS still points at S3, CloudFront, or Heroku, but the bucket/distribution/app was deleted or never created. Anyone can claim the orphaned name and serve content on the victim's domain. Combined bounty in this module: **$2,150 (4 paid of 7 rows)**. The two auth-bypass chains (Ubiquiti, Uber) carry no DB bounty figure but are the module's ceiling evidence; the paid rows cluster at $150–$1,000 for plain takeover.

**Case-stock (7 rows / $2,150):**

| Case | Target | Mechanism | Bounty |
|---|---|---|---|
| [SDTO-352869](https://hackerone.com/reports/352869) | grab — cdn.grab.com | Unregistered CloudFront distribution | $1,000 |
| [SDTO-207576](https://hackerone.com/reports/207576) | shopify — s3.shopify.com | Unregistered S3 bucket | $500 |
| [SDTO-424669](https://hackerone.com/reports/424669) | shopify — tim-exclusive.shopify.com | Unclaimed Heroku instance | $500 |
| [SDTO-317005](https://hackerone.com/reports/317005) | gsa_bbp — 18f.domains.api.data.gov | Unclaimed CloudFront distribution | $150 |
| [SDTO-172137](https://hackerone.com/reports/172137) | ui — ping.ubnt.com → sso.ubnt.com | CloudFront orphan + wildcard SSO cookie → ATO | - |
| [SDTO-219205](https://hackerone.com/reports/219205) | uber — saostatic.uber.com → auth.uber.com | CloudFront orphan + wildcard SSO cookie → ATO | - |
| [SDTO-294201](https://hackerone.com/reports/294201) | semrush — news-static.semrush.com | Unregistered S3 bucket | - |

## 2. Unregistered CloudFront distribution — SDTO-352869 (grab, $1,000)

SDTO-352869 is the module's paid anchor. The start state is three lines of DNS evidence:

> I have found that your website cdn.grab.com is pointed via a cname to a cloudfront instance

> cdn.grab.com => *.cloudfront.net

> This was not registered on Amazon Aws Cloudfront.

The takeover proof is one URL: `http://cdn.grab.com/index.html` serving attacker HTML; the fix offered is to remove the CNAME or transfer the distribution registration. No chaining was needed: full control of the CDN hostname is the finding.

## 3. Unregistered S3 bucket — SDTO-207576 (shopify, $500) and SDTO-294201 (semrush, -)

SDTO-207576 states the S3 primitive in full, including the DNS chain in the body:

> The subdomain s3.shopify.com was pointed using CNAME to Amazon S3, but no bucket with that name was registered. This meant that anyone could sign up for Amazon S3, claim the bucket as their own and then serve content on s3.shopify.com.

Impact as filed is stored XSS via an uploaded HTML page, plus phishing on a first-party hostname. SDTO-294201 is the same shape on SEMrush:

> The subdomain news-static.semrush.com was pointed using CNAME to Amazon S3, but no bucket with that name was registered. This meant that anyone could sign up for Amazon S3, claim the bucket as their own and then serve content on news-static.semrush.com

Claims order differs (SDTO-294201), mechanism identical. Operator rule: `dig` + `nslookup` the CNAME, then attempt the vendor's claim flow before reporting — orphan evidence alone is not a takeover.

## 4. Unclaimed Heroku instance — SDTO-424669 (shopify, $500)

> I have found that your website tim-exclusive.shopify.com is pointed via a cname to an unclaimed Heroku Instance

> This was not registered on Heroku.

The proof is `http://tim-exclusive.shopify.com/` serving attacker content. Same lesson as S3: PaaS names are claimed first-come-first-served, so a dangling CNAME is an open registration endpoint. The message template (remove CNAME / return registration) repeats across SDTO-352869, SDTO-424669, and SDTO-746000.

## 5. CloudFront orphan → SSO authentication bypass — SDTO-172137 (ui, -) and SDTO-219205 (uber, -)

Both rows chain a CloudFront orphan to a wildcard-scoped SSO cookie. SDTO-172137 on Ubiquiti:

> Subdomain ping.ubnt.com was pointing to Amazon Cloudfront CDN, but the hostname was not registered there anymore. This allowed me to fully takeover this domain. It is now serving content of my own webserver, both over http and https.

> The session cookie of your SSO subdomain sso.ubnt.com is (deliberately?) shared with all https://*.ubnt.com subdomains through its "domain=.ubnt.com" attribute.

SDTO-219205 on Uber is the same two-step primitive against `saostatic.uber.com` → `auth.uber.com`:

> Subdomain saostatic.uber.com was pointing to Amazon Cloudfront CDN, but the hostname was not registered there anymore. This allowed me to fully takeover this domain. It is now serving content of my own webserver, both over http and https (highly similar to [175070](https://hackerone.com/reports/175070) - however, I must disagree with "there are some mitigating factors (cookie scope) that make this not as bad as it might appear at first blush.").

The ATO needs no further escalation: any page under the taken-over host receives the SSO session cookie, which the reporter maps to full impersonation on every service behind SSO. Neither row carries a DB bounty figure; the census treats them as evidence, not revenue. Lesson for operators: after claiming the orphan, enumerate `Domain=.` cookie scope on sibling hosts — the chain is where the money lives.

## 6. What pays/what doesn't

- Paid rows are plain claims ($150–$1,000). SDTO-352869 ($1,000, CloudFront), SDTO-207576 + SDTO-424669 ($500 each, S3/Heroku), SDTO-317005 ($150, CloudFront). All four show the orphan, the claim, and a live PoC URL. The $150 row was filed against an out-of-scope domain and still paid — orphan hygiene at scale is itself the value.
- Unpaid rows include the two strongest chains (SDTO-172137, SDTO-219205, no figure) and SDTO-294201 (-). Absence of a figure is a DB gap, not a verdict: the register records `-`, per the bounty rule.
- What doesn't pay on its own in this corpus is a bare dangling record: every paid row demonstrates control of the hostname (index page served), not just a CNAME observation.

## 7. Cross-references

- Module 02 (SaaS-hosted-service-claim) is the paired lane: same orphan-then-claim primitive against Statuspage/Ghost/HubSpot/Mashery third-party SaaS instead of AWS/Heroku platform names.
- Module 03 (DNS-delegation-github-tld) holds the NS-record and GitHub-repo variants of the same dangling DNS root cause.
- `priv-esc` subdomain-dangling module and `misconfig` subdomain-takeover module overlap this class from the privilege/configuration side; cite `priv-esc` for chain-impact framing.
