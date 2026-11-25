---
title: "Adjacent & unclassified — cloudflare r2.dev takeover and vine EC2 reassignment"
type: playbook
category: subdomain-takeover
cwe: "CWE-16"
source_count: 2
full_bodies_available: 2
corpus: "h1-brain disclosed_reports.db (3,673 rows; sha256 8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4)"
list_accessed: "2026-11-07"
note: "Anchor bodies: SDTO-1700276 (cloudflare, $1,125), SDTO-191323 (x, $140). Both are outside the 24-row classified bucket; included as module_map_all _adjacent_unclassified. Claims trace to bodies read 2026-11-07."
---

# Adjacent & unclassified — cloudflare r2.dev takeover and vine EC2 reassignment

## 1. Overview

Two rows the module map filed under `_adjacent_unclassified` — outside the `subdomain-takeover` classified bucket (24 rows) but true to the class on body read. Combined bounty: **$1,265 (2 paid of 2 rows)** — including the vault's single largest figure. They are kept in a separate module so bucket arithmetic stays clean; bucket rows total $3,300, vault rows (bucket + adjacent) total $4,565.

**Case-stock (2 rows / $1,265):**

| Case | Target | Mechanism | Bounty |
|---|---|---|---|
| [SDTO-1700276](https://hackerone.com/reports/1700276) | cloudflare — r2.dev (R2 custom domains) | R2 public-bucket flag bypass → custom-domain claim | $1,125 |
| [SDTO-191323](https://hackerone.com/reports/191323) | x — mk.prd.vine.co | Stopped EC2 IP reassigned to another tenant | $140 |

## 2. Cloudflare R2 custom-domain takeover — SDTO-1700276 (cloudflare, $1,125)

The vault's largest bounty and its most modern primitive: not a dangling DNS record at all, but a server-side check removed while the UI flag stayed. The body:

> It is possible to take over any subdomain of `r2.dev` (possible also the base domain) and have it serve the contents of an R2 bucket in your account.

The technique is a mitmproxy addon flipping the `r2_publicbuckets` flag client-side (`Access to R2 public buckets ... is currently behind a flag. The server-side check for access to R2 public buckets was recently removed`). Adding `albert.r2.dev` as an R2 custom domain activates it, and the bucket's `pub-<public_id>.r2.dev` origin serves attacker content. Conversely, claiming first blocks the legitimate owner (`If the user tries to add the domain as a custom domain for their R2 bucket, the API will throw an error`). This is a vendor-side authorization class — DNS hygiene alone would not have caught it; the reporter found it by toggling feature flags.

## 3. EC2 elastic-IP reassignment — SDTO-191323 (x, $140)

The opposite era: `mk.prd.vine.co` pointed at an EC2 instance that was stopped and re-released to another customer, who now answers on 443 through `awselb/2.0`:

> It looks like the EC2 Instance at `mk.prd.vine.co` has been stopped and now it has been assigned to someone else

Evidence is a 426 → 400 error signature (`Server: awselb/2.0`) — IP-pool reassignment as the takeover mechanism. $140 is the floor price for a bare reassignment observation; the body shows no claimed content. Contrast with SDTO-1700276: same class, opposite proof depth, order-of-magnitude bounty difference.

## 4. What pays/what doesn't

- Both rows paid: $1,125 (novel vendor primitive, any `r2.dev` subdomain) and $140 (reassigned IP). The gap prices novelty: class knowledge (`orphan → claim` is expected) earns little; finding a new claim path earns the ceiling.
- Note the module-map provenance: these two ids were *not* in `classified.json` `subdomain-takeover` (the 24-row bucket). They entered via `module_map_all.json` `_adjacent_unclassified`. The vault counts them as vault rows (26) and labels bucket rows separately (24) wherever totals appear. Every bucket row is in exactly one module — verification section below.

## 5. Cross-references

- Module 01 (Cloud-CDN-PaaS-CNAME) holds the bucket's platform-name claims; this module's R2 row is the modern vendor-flag analogue.
- `priv-esc` subdomain-dangling module carries the same vendor-claim logic from the privilege side; cite for claim-flow detail.
- `Misconfiguration/` subdomain-takeover-dangling-state module is the configuration-hygiene view of the same orphan DNS.
