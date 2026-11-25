---
title: "X-Frame-Options / CSP frame-ancestors — the missing or unsupported header"
type: playbook
category: clickjacking-headers
cwe: "CWE-1021"
source_count: 14
full_bodies_available: 14
corpus: "h1-brain disclosed_reports.db (3,673 rows) · sha256 8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4"
list_accessed: "2026-11-07"
note: "Anchors: CJ-591432 (Periscope ALLOW-FROM, $1,120), CJ-198622 (Chrome ignores ALLOW-FROM, $560), CJ-2119892 (Sketch ATO, $200), CJ-405342 ($80)."
---

# X-Frame-Options / CSP frame-ancestors — the header, and how it fails

## 1. Overview

Fourteen rows, **$1,960/4 paid**. This is the class's commodity tier: a page with no
`X-Frame-Options`, a `SAMEORIGIN` policy with unprotected sub-pages, or an `ALLOW-FROM` value the
browser silently ignores. Payments are small ($80–$1,120) unless the framed page performs a
state-changing action.

**Case-stock (14 rows / $1,960):**

| Case | Target | Mechanism | Bounty |
|---|---|---|---|
| [CJ-591432](https://hackerone.com/reports/591432) | x | `ALLOW-FROM https://twitter.com/` unsupported → Periscope frameable | **$1,120** |
| [CJ-198622](https://hackerone.com/reports/198622) | x | same `ALLOW-FROM` on periscope.tv, Chrome-specific | **$560** |
| [CJ-2119892](https://hackerone.com/reports/2119892) | pixiv | frame `sketch.pixiv.net/draw` → fake login → ATO | **$200** |
| [CJ-405342](https://hackerone.com/reports/405342) | bohemia | ylands.com, "many URLs" frameable | **$80** |
| [CJ-85624](https://hackerone.com/reports/85624) | x | player card iframe → wormable clickjacking | - |
| [CJ-154963](https://hackerone.com/reports/154963) | x | `cards.twitter.com` missing frame headers → email capture | - |
| [CJ-214087](https://hackerone.com/reports/214087) | yelp | `SAMEORIGIN` set, but not on all pages | - |
| [CJ-305128](https://hackerone.com/reports/305128) | yelp | "important functions" frameable | - |
| [CJ-355859](https://hackerone.com/reports/355859) | yelp | reservations page → private data + card misuse | - |
| [CJ-299009](https://hackerone.com/reports/299009) | semrush | SSO login page frameable | - |
| [CJ-289246](https://hackerone.com/reports/289246) | semrush | listed links without DENY/SAMEORIGIN | - |
| [CJ-765355](https://hackerone.com/reports/765355) | automattic | `refer.wordpress.com` campaign settings frameable | - |
| [CJ-765955](https://hackerone.com/reports/765955) | nordsecurity | `join.nordvpn.com` frameable | - |
| [CJ-921709](https://hackerone.com/reports/921709) | wordpress | donation page redirect | - |

## 2. The header bug that paid twice

Both Periscope rows hinge on one fact about `ALLOW-FROM`:

> The X-FRAME-OPTIONS header returned from https://www.periscope.tv is:
> ```
> X-Frame-Options: ALLOW-FROM https://twitter.com/
> ```
> But Chrome doesn't support this value for the header

CJ-591432 names the same cause for `canary-web.pscp.tv` and `canary-web.periscope.tv`:

> X-Frame-Options ALLOW-FROM https://twitter.com/ not supported by several Browser, this caused Clickjacking on Twitter Periscope subdomain

Operator note: when a report shows `ALLOW-FROM`, the finding is browser-dependent — say which
browser and version you proved it in. Firefox honored the directive for years; Chrome/Safari never
did.

## 3. `SAMEORIGIN` is not site-wide

CJ-214087:

> Yelp set its X-Frame-Options to SAME ORIGIN in its HTTP headers; but unfortunately our exploitation proves that not all the pages are protected.

The corpus's unpaid Yelp rows are the lesson in triage: "a page is frameable" without a
state-changing action behind it is informational. The paid Pixiv row ($200) is frameable *and*
leads to a fake login.

## 4. Impact statements that get paid

- CJ-2119892: `using  it we can trick the user to fake login with the use of clickjacking`
- CJ-355859: reservation flow → `exposure of victim Private Data (Email info) + Victim Credit Card MissUse`
- CJ-765355: `This clickjacking is on authenticated pages so it is very critical vulnerability.`

## 5. What pays, what doesn't

- **Paid band**: $80–$1,120. The ceiling in this corpus is a *platform-wide* clickjacking issue on
  a high-traffic subdomain, not a single form.
- **Unpaid**: bare "no X-Frame-Options" on marketing/static pages, duplicate sub-pages of an
  already-reported host, and reports with no browser-specific proof.
- Always include the PoC HTML and the exact header you observed; the corpus's paid rows all do.

## 6. Cross-references

- `02_Markup-RTLO-UI-Redress.md` — when markup injection *is* the clickjacking primitive.
- `03_Clickjacking-Enable-Chains.md` — clickjacking as one step in a longer exploit.
- `../18_Misconfiguration/` — header hygiene rows that overlap this bucket.
