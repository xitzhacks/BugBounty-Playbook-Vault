---
title: "DNS-delegation / GitHub / TLD — dangling NS, unclaimed repo, unregistered TLD"
type: playbook
category: subdomain-takeover
cwe: "CWE-16"
source_count: 3
full_bodies_available: 3
corpus: "h1-brain disclosed_reports.db (3,673 rows; sha256 8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4)"
list_accessed: "2026-11-07"
note: "Anchor bodies: SDTO-746000 (kubernetes, $250, CVE-2017-14389), SDTO-515574 (gsa_bbp, -), SDTO-1312365 (affirm, -). Claims trace to bodies read 2026-11-07."
---

# DNS-delegation / GitHub / TLD — dangling NS, unclaimed repo, unregistered TLD

## 1. Overview

Three corpus cases where the dangling pointer is below or beside the CNAME: a deleted NS delegation, a dead GitHub Pages repo, and a CNAME into an unregistered TLD. Combined bounty: **$250 (1 paid of 3 rows)**. Small module, but it holds the vault's only CVE (SDTO-746000, CVE-2017-14389) and proves the class extends past CNAMEs into delegation and registration gaps.

**Case-stock (3 rows / $250):**

| Case | Target | Mechanism | Bounty |
|---|---|---|---|
| [SDTO-746000](https://hackerone.com/reports/746000) | kubernetes — api.e2e-kops-aws-canary.test-cncf-aws.canary.k8s.io | Dangling Route 53 NS delegation | $250 (CVE-2017-14389) |
| [SDTO-515574](https://hackerone.com/reports/515574) | gsa_bbp — www.data.gov/labs (simple-api.github.io) | Unclaimed GitHub repo | - |
| [SDTO-1312365](https://hackerone.com/reports/1312365) | affirm — ██████.████.████████.com | CNAME to unregistered TLD | - |

## 2. Dangling NS delegation — SDTO-746000 (kubernetes, $250, CVE-2017-14389)

The NS-record primitive is stronger than a CNAME: you inherit the zone, not a hostname. SDTO-746000's body:

> I have found that your website http://api.e2e-kops-aws-canary.test-cncf-aws.canary.k8s.io is pointed via Name Server records to AWS route 53.

> These name server records have been deleted, I was able to create a matching zone file, and takeover full control of the domain, and all DNS records.

> It is possible to create any subdomain, MX records, A, AAAA, txt, PTR any records to control the domain.

MX control is the escalation: attacker receives mail to `*@canary.k8s.io`, which the reporter maps to password resets, Slack/Google OAuth grants, and SSL email-validation. CVE-2017-14389 is cited in the body with CVSS 7.5. This is the correct remedy class: remove the NS delegation, not a hostname record.

## 3. Unclaimed GitHub repo — SDTO-515574 (gsa_bbp, -)

Not subdomain DNS but the same vendor-slot orphan. `data.gov/labs` linked to `https://simple-api.github.io/api-offices/`; the repo 404'd. The reporter registered as `simple-api`, created repo `api-offices`, and served attacker content to anyone following the official pages. Claim steps in the body are five lines:

> 1. this domain was available to claim.
> 2. registered for new github account
> 3. used username "simple-api"
> 4. created a master-branch of repository with "api-offices"
> 5. created a simple index.html file.

No bounty figure. Lesson: check every GitHub Pages / repo link under official surfaces for 404s — the claim is free.

## 4. Unregistered TLD — SDTO-1312365 (affirm, -)

The only TLD-registration case. A CNAME target's TLD is not registered and not reserved for internal use (`.test`/`.example`/`.invalid`/`.localhost` are the only safe private TLDs). The reporter's impact line:

> As a result, an attacker can register for the `███` TLD to create and takeover **███████.████████.█████.com** subdomain.

The target hostname is redacted in the body (`███████.████.██████████.com`); asset field records `hackerone.affirm-odin.com`. Root cause is a human DNS-record error. Operator rule: `dig` the CNAME target itself and validate the TLD against `data.iana.org/TLD/tlds-alpha-by-domain.txt` — subdomain checks that stop at the CNAME miss this lane.

## 5. What pays/what doesn't

- 1 of 3 rows paid ($250, SDTO-746000). The paid row is the one with zone-wide control plus a CVE and CVSS; the other two are correct findings with no DB figure.
- NS orphans outrank CNAME orphans in impact (MX + arbitrary subdomains vs one hostname) but price lower here ($250) — the vault's ceiling is set by completed claims on trusted hosts (module 01's $1,000), not by DNS breadth. Reasonable inference from the corpus only; don't over-read it.

## 6. Cross-references

- Modules 01–02 hold the CNAME variants; this module is the delegation/registration remainder. The fix families overlap (`remove/inherit` the pointer).
- `Authentication-Session/` module 02 (session fixation/hijack) cites subdomain-takeover cookie-scope chains; SDTO-746000's impact paragraph states the wildcard-cookie version explicitly.
- `SSRF/` — NS takeover can seed SSRF allowlist bypasses the same way a CNAME takeover can; map MX/zone control to allowlist endpoints after claiming.
