---
title: "Subdomain takeover and dangling state — the abandoned pointer is the finding"
type: playbook
category: subdomain-takeover-dangling-state
cwe: "CWE-829, CWE-16"
source_count: 15
full_bodies_available: 15
corpus: "h1-brain disclosed_reports.db 3,673 rows (sha256 8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4); misconfig bucket (152 rows)"
list_accessed: "2026-11-07"
note: "15 rows / $4,000 (3 paid). Bodies read end-to-end. Claims trace to bodies read 2026-11-07; every blockquote is byte-true to references/archive/MISCONF-bodies-full-dump.txt."
---

# Subdomain takeover and dangling state — the abandoned pointer is the finding

## 1. Overview

Fifteen rows, **$4,000/3 paid**. The module's grammar is one sentence: a DNS record, a CNAME, or a link still points at a service instance the owner no longer controls, so whoever claims the instance inherits the victim's trust. The corpus pays the takeover when the name is trusted (`*.firefox.com`, `rubygems.org`, a `signup` host), and pays $0 when the name is orphaned and unused — the difference is demonstrated trust, not demonstrated syntax. Three of the findings are abuse of *deallocated infrastructure behind* the name (S3 buckets, CloudFront origins, deleted GitHub-linked domains) rather than DNS alone, which is why the module keeps DNS, storage, and link hygiene in one place: all three are "pointer outlives instance."

**Case-stock (15 rows / $4,000):**

| Case | Target | Mechanism | Bounty |
|---|---|---|---|
| [MISCONF-142096](https://hackerone.com/reports/142096) | slack | Neglected CNAME to inactive UserVoice | - |
| [MISCONF-148770](https://hackerone.com/reports/148770) | legalrobot | Modulus unclaimed domain + wildcard | - |
| [MISCONF-154425](https://hackerone.com/reports/154425) | snapchat | Dangling Fastly CNAME reclaimed on CDN | $3,000 |
| [MISCONF-159156](https://hackerone.com/reports/159156) | security | hacker.one CNAME to Instapage | - |
| [MISCONF-172549](https://hackerone.com/reports/172549) | reverb | Blind S3 bucket write | - |
| [MISCONF-172698](https://hackerone.com/reports/172698) | websummit | Heroku CNAME unclaimed (signup) | - |
| [MISCONF-201796](https://hackerone.com/reports/201796) | automattic | Desk CNAME to expired tenant | - |
| [MISCONF-1354066](https://hackerone.com/reports/1354066) | 8x8-bounty | Dangling GSuite CNAME (unclaimed) | - |
| [MISCONF-1487793](https://hackerone.com/reports/1487793) | sifchain | Vercel CNAME unclaimed | - |
| [MISCONF-2011298](https://hackerone.com/reports/2011298) | stripe | Repo links to uncontrolled veneur.org | - |
| [MISCONF-2262939](https://hackerone.com/reports/2262939) | ibb | Unclaimed S3 origin behind CloudFront | - |
| [MISCONF-2523654](https://hackerone.com/reports/2523654) | gitlab | Pages subdomain takeover | - |
| [MISCONF-2599840](https://hackerone.com/reports/2599840) | gitlab | Obsolete handbook subdomain | - |
| [MISCONF-2706358](https://hackerone.com/reports/2706358) | mozilla | Unregistered Fastly domain claimed | $500 |
| [MISCONF-2899858](https://hackerone.com/reports/2899858) | mozilla | CNAME to unregistered host claimed | $500 |

## 2. The paid core: cancelled instance, live record

MISCONF-154425 (snapchat, **$3,000**, the module's ceiling) is the canonical shape — a Fastly instance cancelled, the DNS record kept:

> I've found a snapchat cdn domain here which had a test instance of fastly setup but did not remove the dns record when the service was cancelled. This allowed me to create a Fastly instance to take it over.

MISCONF-2706358 (mozilla, **$500**) is the same bug one click further along — the name was never registered at the CDN at all:

> The domain **addons-preview-cdn.mozilla.net** was not registered within Fastly, which resulted in an error that says "Fastly error: unknown domain"  

> After registering this domain on Fastly, I was able to serve custom content on **addons-preview-cdn.mozilla.net**.

MISCONF-2899858 (mozilla, **$500**) adds the program-scope lesson every takeover hunter must file with: the company explicitly pays takeovers on trusted zones, but only with a proof of concept, and only where the name is not already claimed by someone else:

> Domain takeovers supported by a proof of concept for *.mozilla.org, *.mozilla.com, *.mozilla.net, *.firefox.com, *.mozgcp.net and *.mozaws.net in addition to the list of sites in scope. If the domain is pointing to a claimed instance by another company, then the report will not be eligible for bounty.

Doctrine: DNS archaeology first, claim second. The researcher who finds the dangling CNAME and then registers the instance has the report; the researcher who only finds the CNAME has a memo.

## 3. Claimable services across four eras

The corpus spans the whole claimable-platform lifecycle, and each row names its platform precisely enough to reproduce the claim today:

- **UserVoice (inactive tenant)** — MISCONF-142096: `feedback.screenhero.com` CNAMEs to `screenhero.uservoice.com` whose service is inactive, so the reporter claims the username and clones the site. The fix the body prescribes is still exact: remove CNAMEs for services no longer used.
- **Modulus.io unclaimed domain** — MISCONF-148770: the reporter creates an application, finds the victim domain already registered, then claims the wildcard `*.legalrobot.com` instead — and notes, acidly, that "Modulus will actually resolve the domain serving SSL, which is a really bad thing." Wildcard claims are the escalation when the apex is taken.
- **Instapage** — MISCONF-159156: `hacker.one` down through a third-party landing-page CNAME. Low-effort, high-trust: official-site impersonation is the impact statement.
- **Heroku names** — MISCONF-172698: `signup.websummit.net` points at `wsv1.herokuapp.com`, and the reporter argues the *name* `signup` is what makes it dangerous ("a perfect place to create a fake login/subscribe page to steal users credentials"). Name semantics are part of the impact argument.
- **Desk/expired tenant** — MISCONF-201796: `help.cloudup.com` → `cloudup.desk.com`. The reporter registers the Desk tenant and gains full control of the CNAME. The bodies are honest about the gaps (SSL errors, amateur framing); the takeover itself is the finding.
- **Vercel** — MISCONF-1487793: `proxies.sifchain.finance` CNAMEs to `cname.vercel-dns.com`, unclaimed at Vercel's team-domain check. The report's generic definition sentence is worth copying into any takeover report: "Subdomain takeover vulnerabilities occur when a subdomain (subdomain.example.com) is pointing to a service (e.g. GitHub pages, Heroku, etc.) that has been removed or deleted."
- **GSuite (unsuccessful)** — MISCONF-1354066: `docs.jitsi.net` 404s under `ghs.google`; the reporter claims it via Workspace. Filed as "unsuccessful GSuite takeover" because the claim was possible but the domain was not demonstrably in active use — the trust demo decides the tier.
- **GitLab Pages + obsolete subdomain** — MISCONF-2523654 / MISCONF-2599840: the same vendor, two flavors (Pages pages takeover; handbook subdomain removal). Both $0 in the DB (no figure published) — the module keeps them as technique exhibits, not pricing anchors.

## 4. Storage is the quieter takeover

MISCONF-2262939 (ibb, rubygems.org, no figure published) is the module's best technical write-up and the one most worth reading end-to-end (body 5,658 bytes): the `/names` endpoint returns S3's `NoSuchBucket` XML because the bucket `index.rubygems.org` does not exist; claiming the bucket in `us-west-2` makes the endpoint serve attacker-chosen content with attacker-chosen content-type; CloudFront caches it. The impact paragraph prices what this means for gem consumers:

> This bug would allow me to set the content-type using AWS S3 CLI to text/html and serve stored XSS on the page. This could affect a logged in maintainer in a very bad way.

> As these endpoints contain the checksums for the gems for different versions, a supply-chain-attack could probably have been attempted as the checksums could be set to anything the attacker wanted.

MISCONF-172549 (reverb) is the negative control for blind storage claims: the reporter can *write* to `reverb-ssh` but cannot list it, cannot prove ownership, and asks for an informative close. The module's rule: a blind write without an ownership proof or a read-back is a hypothesis, not a takeover.

## 5. Links are pointers too

MISCONF-2011298 (stripe) generalizes the bug beyond DNS: the `stripe/veneur` repository's sidebar linked to `veneur.org`, a domain no longer under Stripe's control. The body's three-step attack is the template for every "documentation points at dead infrastructure" report:

> - step one: control `https://veneur.org`, either because you are the current owner or you purchase the domain.
>   - step two: recreate the old site, but edit the installation instructions to reference malicious source code or a docker image built with malicious code.
>   - step three: a veneur user follows the instructions
>   - outcome: attacker-controlled code/image running inside a privileged environment.

It also records the modern scope discipline: the sidebar was fixed, but "Many of the 179 forks of this repository still contain the link to the uncontrolled domain" — fix propagation is part of the report.

## 6. What pays, what doesn't

- **Pays ($500–$3,000):** a cancelled instance with a live DNS record where the researcher claims the instance and serves content (154425 $3,000; 2706358 $500; 2899858 $500). The Fastly pair is the price anchor for "orphaned name, trusted zone, PoC served."
- **Does not pay in the DB record (no figure):** twelve rows, including technically complete takeovers (142096, 148770, 2262939, 172698, 1487793). `None` means no figure in the DB — not evidence of non-payment. The $0-for-certain rows the module *proves* are blind writes without proof (172549: "I can not list the files in the bucket and such can not be 100% sure you own it").
- **The trust demo is the product.** MISCONF-154425 was paid $3,000 even though the reporter concedes the domain "does not appear to be used anywhere on any snapchat properties." What converted it was the claim itself plus an ownership proof (Censys certificate chain), not traffic analysis. MISCONF-1354066, where the claim was possible but the name was demonstrably unused, carries no figure. The corpus prices *reclaimed trust*, and unused names reclaim nothing.
- **Claim mechanics win triage.** The mozilla program's own scope note (2899858 §2) is the kill-gate spec: proof of concept required, already-claimed instances out of scope. File accordingly.

## 7. Cross-references

- Vault `13_Subdomain-Takeover/` — the dedicated subdomain-takeover vault; this module's rows are the misconfig-bucket slice (see `references/source-index.md` §2 on the zero-overlap bucket split).
- Module 04 (§3) — broken-link hijacking (MISCONF-1212853, MISCONF-1239334) is this module's mechanism applied to usernames instead of DNS; same "unclaimed namespace" root cause.
- Module 03 (§4) — CloudFront/CDN cache behavior (MISCONF-2262939's cached attacker content) is the delivery half of module 03's cache-deception rows (MISCONF-1271944, MISCONF-631589).
- Playbook P1/P2 — DNS/CNAME inventory and claim mechanics.
