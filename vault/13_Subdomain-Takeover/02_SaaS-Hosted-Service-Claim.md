---
title: "SaaS-hosted-service-claim — Statuspage/Ghost/HubSpot/Mashery and small-SaaS custom-domain orphans"
type: playbook
category: subdomain-takeover
cwe: "CWE-16"
source_count: 14
full_bodies_available: 14
corpus: "h1-brain disclosed_reports.db (3,673 rows; sha256 8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4)"
list_accessed: "2026-11-07"
note: "Anchor bodies: SDTO-1474784 (zenly, $750), SDTO-195350 (slack, $100), SDTO-49663 (vimeo, -), SDTO-335330 (roblox, -). Claims trace to bodies read 2026-11-07."
---

# SaaS-hosted-service-claim — Statuspage/Ghost/HubSpot/Mashery and small-SaaS custom-domain orphans

## 1. Overview

Fourteen corpus cases where the orphan is not AWS but a third-party SaaS custom-domain slot: Statuspage, Podbean/FeedPress, GitBook, Mashery, WordPress domain mapping, HubSpot, Ghost, Unbounce, Uberflip, Wix, Brandpad, Squarespace, Wix again. The shape is constant — CNAME points at the SaaS, the SaaS account that owned the slot is gone, so the first new account to register the hostname wins. Combined bounty in this module: **$900 (3 paid of 14 rows)** — the lowest paid rate in the vault, which is itself informative: small-SaaS orphans pay only when the reporter proves the claim, and most rows here are claim-evidence rather than cash.

**Case-stock (14 rows / $900):**

| Case | Target | Mechanism | Bounty |
|---|---|---|---|
| [SDTO-1474784](https://hackerone.com/reports/1474784) | zenly — brand.zen.ly | Brandpad custom-domain claim | $750 |
| [SDTO-195350](https://hackerone.com/reports/195350) | slack — podcasts.slack-core.com | FeedPress/Podbean redirect claim | $100 |
| [SDTO-1963213](https://hackerone.com/reports/1963213) | omise — accessday.opn.ooo | Unclaimed Wix site | $50 |
| [SDTO-49663](https://hackerone.com/reports/49663) | vimeo — status.vimeo.com | Unconnected Statuspage.io | - |
| [SDTO-181665](https://hackerone.com/reports/181665) | ui — moderator.ubnt.com | Google-hosted orphan (same as #179110) | - |
| [SDTO-223625](https://hackerone.com/reports/223625) | udemy — coding-exercises.udemy.com | GitBook trailing-dot claim | - |
| [SDTO-275714](https://hackerone.com/reports/275714) | starbucks — developer.openapi.starbucks.com | Mashery custom-domain claim | - |
| [SDTO-295330](https://hackerone.com/reports/295330) | wordpress — code.wordpress.net | WordPress domain-mapping orphan | - |
| [SDTO-335330](https://hackerone.com/reports/335330) | roblox — devrel.roblox.com | Unclaimed HubSpot instance | - |
| [SDTO-368119](https://hackerone.com/reports/368119) | udemy — engineering.udemy.com | Inactive Ghost.io instance | - |
| [SDTO-407355](https://hackerone.com/reports/407355) | greenhouse — demo.greenhouse.io | Unbounce Pages orphan | - |
| [SDTO-863551](https://hackerone.com/reports/863551) | security — resources.hackerone.com | Unregistered Uberflip hub | - |
| [SDTO-1183296](https://hackerone.com/reports/1183296) | sifchain — sifchain.finance | Unclaimed Wix site (apex) | - |
| [SDTO-1527405](https://hackerone.com/reports/1527405) | imgur — 8ybhy85kld9zp9xf84x6.imgur.com | Squarespace custom-domain claim | - |

## 2. Statuspage.io — SDTO-49663 (vimeo, -)

The cleanest small-SaaS statement in the vault:

> Your subdomain status.vimeo.com is pointing to hosted.statuspage.io, but no statuspage was connected to it. This means that anyone can claim the subdomain by setting up a statuspage.io site and using "status.vimeo.com" as the name!

Impact as filed is login-form phishing on a first-party domain plus session-cookie access. No bounty figure in DB. Operator note: the Vendor fix is DNS removal, not account transfer — the reporter states it directly, so the report can own the remediation line.

## 3. Brandpad claim, paid — SDTO-1474784 (zenly, $750)

The module's paid anchor. Brandpad is small; the evidence chain is the full template (error page + dig + live takeover):

> I just went to `brand.zen.ly` and it shows an error "Not Found", also I've checked the CNAME is pointing to `brandpad.io`, which means it can be added to any account.

> I was able to takeover `brand.zen.ly` by registering at **Brandpad**.

Note the paid pattern vs unpaid siblings: reporter registered, claimed, and visited the live hostname. Rows that only describe the orphan (no claim) cluster at `-` in this module.

## 4. Slack Podcasts + HubSpot chains — SDTO-195350 ($100), SDTO-335330 (-)

SDTO-195350 is a research-style row on `slack-core.com`:

> I noticed `slack-core.com` is used for Slack's call infrastructure. I had never seen that domain before, so I decided to find out what else was running on it. It turned out `podcasts.slack-core.com` was pointing to a Podcast and RSS hosting service called Feed.Press. However, there was no Feed.Press account associated with `podcasts.slack-core.com`, which allowed me to register it and start serving my content from this domain.

The reporter is explicit that impact is minimal because the host is not on Slack's root domain. $100 is consistent with that honesty.

SDTO-335330 (Roblox) is the chain ceiling of the small-SaaS lane:

> Due to unclaimed or expired Hubspot instance an attacker is able to claim and serve content from `devrel.roblox.com` and perform different kind of attacks which i shared in impact section.

The body maps the claim to `.ROBLOSECURITY` cookie theft (wildcard scope), CORS-whitelisted chat reads, and Google Workspace mail control. No DB bounty figure — same pattern as the vault's CloudFront chains: the chain is evidenced, the payout is not in the DB.

## 5. The unpaid claim shelf (template rows)

The remaining rows repeat the Brandpad evidence template against other SaaS slots. Worth knowing as fingerprints, none with bounty figures:

- **Mashery** — SDTO-275714 (starbucks): `developer.openapi.starbucks.com` serves a `Mashery Proxy`, trial account plus host entry claims the name with no error.
- **Ghost** — SDTO-368119 (udemy): `engineering.udemy.com` CNAMEs to an inactive `ghost.io` host; a paid Ghost publication named `udemy-engineering-blog` passes validation and inherits SSL.
- **GitBook trailing dot** — SDTO-223625 (udemy): GitBook-hosted site takeover via trailing dot (couples with the earlier XSS report #222337 and H1 #174417).
- **WordPress mapping** — SDTO-295330 (wordpress): `code.wordpress.net` shows `Warning! Domain mapping upgrade for this domain not found.`
- **Unbounce** — SDTO-407355 (greenhouse): `demo.greenhouse.io` → `unbouncepages.com`; reporter could not afford the subscription, so the row is evidence-only (explains the `-`).
- **Uberflip** — SDTO-863551 (security): `resources.hackerone.com` shows `Non-hub domain` with CNAME to `read.uberflip.com`; signup problems blocked a live claim test.
- **Wix (apex)** — SDTO-1183296 (sifchain): the *apex* domain itself is an unclaimed Wix CNAME; reporter lacked a premium account to complete the claim.
- **Squarespace** — SDTO-1527405 (imgur): random-hash subdomain claimed, but custom-domain upload needs a paid upgrade; proof via `mrbaka.squarespace.com` account link only.
- **Small-SaaS confirmations** — SDTO-181665 (Google hosting, 216.58.203.243 `ghs.google.com`), SDTO-1963213 (Wix CDN, accessday.opn.ooo, **$50**): cheapest paid row in the vault.

## 6. What pays/what doesn't

- Only 3 of 14 rows carry figures: SDTO-1474784 ($750), SDTO-195350 ($100), SDTO-1963213 ($50). The paid row is the one with a completed claim; the two cheap rows are explicitly low-impact. SDTO-407355/1183296/1527405 show the counter-case from the reporter's side: claim blocked by cost or account limits, row left as orphan evidence, no figure.
- Weakness labels here are noisy (`XSS - Generic` on SDTO-181665/195350, `CSRF` on SDTO-49663, `Phishing` on SDTO-407355, `None` on 4 rows). Modules classify by body behavior; the label is triage, not taxonomy.
- The template's impact boilerplate (malware / phishing / XSS / auth bypass) repeats verbatim across SDTO-1474784, SDTO-1527405, and SDTO-1183296. Don't copy it — write what your claim actually reaches.

## 7. Cross-references

- Module 01 (Cloud-CDN-PaaS-CNAME) is the platform-name analogue; same DNS root cause, different vendor claim flow.
- Module 03 holds the delegation-orphan variants (NS records, GitHub Pages repo) that share this lane's "vendor slot still points at you" mechanism.
- `Authentication-Session/` module 02 cites SDTO-172137/219205-class cookie-scope chains; the HubSpot row here is the SaaS flavour.
