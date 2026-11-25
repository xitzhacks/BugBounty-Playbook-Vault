---
title: "Subdomain dangling takeover — claimable DNS, S3/CloudFront/Webflow/Fastly re-registration"
type: playbook
category: subdomain-dangling-takeover
cwe: "CWE-732"
source_count: 24
full_bodies_available: 24
corpus: "h1-brain disclosed_reports.db (3,673 rows), priv-esc bucket + module_map_all.json merges"
list_accessed: "2026-11-07"
note: "Anchors: PRIV-779442 (lyst, $1,000), PRIV-716677 (gitlab Fastly CSP claim, $200). All 24 bodies read end-to-end. Bounty floor: $1,400/4 paid (20/24 no figure)."
---

# Subdomain Dangling Takeover — when the DNS outlives the resource

## 1. Overview

Twenty-four rows, **$1,400/4 paid** (20/24 carry no bounty figure — `None` ≠ $0). This is the smallest paid module in the vault by figure but the most mechanical: every row is the same shape — a CNAME, NXDOMAIN, or provider-side dangling record still points at a resource the owner no longer controls, and the hunter re-registers that resource and serves arbitrary content on the victim's subdomain. The class census is uniform (24/24 `Privilege Escalation` in the DB), and the program concentration is four vendors doing DNS at scale: starbucks 6, security (HackerOne's own `info.hacker.one`) 4, acronis 3, ui/uber/websummit/udemy/roblox/shopify/gitlab/lyst/btfs/exness/hostinger 1 each. The paid ceiling is low by design: $1,000 (lyst S3) is the module top, then $200 (gitlab), then $100/$100. The lesson is coverage and automation, not exploitation depth.

**Case-stock (24 rows / $1,400):**

| Case | Target | Mechanism | Bounty |
|---|---|---|---|
| [PRIV-779442](https://hackerone.com/reports/779442) | lyst — *.lyst.com | CNAME → unclaimed S3 bucket → register + static hosting | $1,000 |
| [PRIV-716677](https://hackerone.com/reports/716677) | gitlab — gitlab.com | Fastly free-TLS domain CSP-whitelisted → any-account claim | $200 |
| [PRIV-824909](https://hackerone.com/reports/824909) | btfs | uptime subdomain takeover | $100 |
| [PRIV-1256389](https://hackerone.com/reports/1256389) | acronis — Other Acronis Domains | cyberlynx.lu main-domain subdomain takeover | $100 |
| [PRIV-145224](https://hackerone.com/reports/145224) | ui | non-used CloudFront DNS entry → claimable origin | - |
| [PRIV-175070](https://hackerone.com/reports/175070) | uber | non-existent CloudFront distribution → claim | - |
| [PRIV-186766](https://hackerone.com/reports/186766) | starbucks — Other assets | non-used AWS S3 DNS record → register bucket | - |
| [PRIV-193056](https://hackerone.com/reports/193056) | websummit | dangling DNS → takeover | - |
| [PRIV-202767](https://hackerone.com/reports/202767) | security | UnbouncePages CNAME + vendor claim API (all customers) | - |
| [PRIV-208719](https://hackerone.com/reports/208719) | udemy | dangling DNS → takeover | - |
| [PRIV-209004](https://hackerone.com/reports/209004) | security | info.hacker.one dangling (takeover #2) | - |
| [PRIV-217358](https://hackerone.com/reports/217358) | security | info.hacker.one dangling (takeover #3) | - |
| [PRIV-220002](https://hackerone.com/reports/220002) | security | info.hacker.one dangling (takeover #4) | - |
| [PRIV-264494](https://hackerone.com/reports/264494) | roblox | creatorforum.roblox.com dangling → takeover | - |
| [PRIV-325336](https://hackerone.com/reports/325336) | starbucks — Other non domain specific items | svcgatewayus.starbucks.com dangling | - |
| [PRIV-365853](https://hackerone.com/reports/365853) | shopify — *.shopify.com | competition.shopify.com dangling | - |
| [PRIV-383564](https://hackerone.com/reports/383564) | starbucks | svcgatewaydevus / loadus dangling | - |
| [PRIV-388622](https://hackerone.com/reports/388622) | starbucks — Other non domain specific items | wfmnarptpc.starbucks.com dangling | - |
| [PRIV-661751](https://hackerone.com/reports/661751) | starbucks — Other non domain specific items | d02-1-ag.productioncontroller dangling | - |
| [PRIV-665398](https://hackerone.com/reports/665398) | starbucks — Other non domain specific items | datacafe-cert.starbucks.com dangling | - |
| [PRIV-952166](https://hackerone.com/reports/952166) | acronis — *.acronis.com | jet.acronis.com → unclaimed Webflow | - |
| [PRIV-953719](https://hackerone.com/reports/953719) | acronis — *.acronis.com | www.jet.acronis.com → unclaimed Webflow | - |
| [PRIV-1540252](https://hackerone.com/reports/1540252) | exness — Web Terminal | odoo-staging.exness.io dangling | - |
| [PRIV-1570591](https://hackerone.com/reports/1570591) | hostinger — www.hosting24.com | status.hosting24.com dangling | - |

## 2. The paid lane: re-register and serve

PRIV-779442 (lyst, **$1,000**) is the module's cleanest paid demonstration: a CNAME pointing at a bucket name that does not exist, the bucket re-registered, static hosting enabled, and a trivial XSS payload served as proof:

> The subdomain storybook.lystit.com had an CNAME record pointing to an unclaimed S3 bucket.

The body continues in the same register — the bucket name equals the subdomain string, no subdomain-verification step stops the re-registration, and the hunter serves a POC page plus a stored-XSS file. That is the whole template: resolve → NXDOMAIN/CNAME-to-missing → claim → serve.

## 3. CloudFront: the origin that validates nothing

PRIV-145224 (ui / Ubiquiti, no figure) is the module's most instructive unpaid row because the mechanism is named as a platform gap, not a victim misconfiguration:

> So lately I have discovered that CloudFront is not validating which user that connects a CNAME:d domain to a CloudFront Origin.

The hunter then claims `partners.ubnt.com` (DNS still points at CloudFront, no origin holds it as a CNAME) and serves a `/login` honeypot. The doctrine: when the cloud provider does not bind claimants to DNS owners, every stale DNS entry pointing at that provider is a standing takeover. PRIV-175070 (uber / rider.uber.com) is the same primitive against a non-existent distribution. The corpus never prices these rows above $0 in-record (no figure), but the text states the blast radius explicitly — fake login forms, spear-phishing on the real domain, and SSL issuance via file/meta verification on a domain the attacker now serves.

## 4. Vendor-API takeovers: the claim endpoint is the bug

PRIV-202767 (security / `info.hacker.one`, no figure) is the row most worth teaching as an operator, because the dangling record is only half the story — the vendor's claim API has no ownership check at all:

> While testing UnbouncePage services i saw that they block any domain that was already claimed, but i decided go  deeper and I found an 0day in their API which allows any user to claim any domain with a DNS entry pointing to -> __unbouncepages.com__, i think this bug compromises All Customers Domains at UnbouncePage Services

(sic) `go  deeper` (double space) in the original. The target list proves it: `info.hacker.one` was taken over four separate times (PRIV-202767/209004/217358/220002), each time the CNAME pointed at `app.unbounce.com` and each time the hunter claimed it through the same vendor API. The operator rule: when you find a dangling CNAME to a SaaS page-builder, the vendor's claim endpoint — not the DNS record — is the system you are attacking. It may let you claim *any* pointing domain, not just your own.

## 5. Fastly and the CSP-whitelisted domain: takeover as XSS precondition

PRIV-716677 (gitlab, **$200**) is the module's only row where the takeover is not the endgame but the precondition for a CSP bypass:

> The domain `gl-canary.freetls.fastly.net` is whitelisted in gitlab.com Content Security Policy.

The body walks the four-click claim (register → new service → use the generated free-TLS name → serve), then states the impact without needing to demonstrate it: any Fastly account can control the whitelisted domain, so client-side code can execute under a trusted CSP. The $200 price is the corpus's guide to this lane: it is the cheapest demonstration of a dangling-resource claim (no S3 bucket needed, no certificate needed) because the victim's own CSP does the trusting.

The remaining rows are filed without further quotes — the pattern repeats (Starbucks S3/CNAME sprawl ×6, Acronis Webflow ×2, Uber/Shopify/Roblox/Udemy/websummit/exness/hostinger ×1 each). All 24 bodies were read; no quote is invented for any row.

## 6. What pays/what doesn't

- **What pays ($1,400/4):** a served POC on the real subdomain (779442's static-hosted XSS file, $1,000), a claimable whitelisted domain with a working four-step claim procedure (716677, $200), and the two $100 rows (824909 uptime, 1256389 cyberlynx.lu). The corpus prices a wireframe POC (the 130-byte PRIV-1570591 body — a domain, a PoC link, one impact line — carries no figure) at nothing visible; it prices a served page at $100–$1,000 depending on program table.
- **What doesn't price above $0 in-record:** 20/24 rows carry no figure. That is the vault's central honesty note for this module — `None` is missing data, not proof of $0 — but the module's floor is unmistakable: a dangling record alone, without a served POC, has no corpus example of a payout. Every quoted payload is a served page or a claim API call.
- **Vendor-API takeovers:** the `info.hacker.one` ×4 sequence shows the repeatable variant — the same broken claim API pays four times on the same program because the underlying vendor bug (`unbouncepages.com` claim-any) was never fixed between rows. The modern equivalent is Subdomain Keeper / DNSteal-style enumeration plus a provider-claim test on *every* dangling CNAME, not just the victim's own.

## 7. Cross-references

- PRIV-1092859 (module 05) is this class one level deeper: dangling Route53 NS delegations in kOps docs let the hunter serve arbitrary records for an entire zone — same root cause (DNS outlives the resource), wider blast radius.
- The CSP-whitelisted Fastly claim (716677) is the XSS vault's "trusted host" precondition: cross-cite when a CSP allows a third-party domain.
- The playbook (PRIV-Testing-Agent-Playbook.md) P1 inventories dangling records before any claim attempt; P5 requires a served-page artifact.
