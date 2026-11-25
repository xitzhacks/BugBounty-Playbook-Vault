---
title: "Markup, RTLO & injected UI — when the page renders attacker chrome"
type: playbook
category: clickjacking-markup
cwe: "CWE-1021, CWE-79"
source_count: 5
full_bodies_available: 5
corpus: "h1-brain disclosed_reports.db (3,673 rows) · sha256 8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4"
list_accessed: "2026-11-07"
note: "Anchors: CJ-662287 (GitLab RDoc full-page overlay, $3,500 — vault max), CJ-289823/CJ-291683/CJ-297547 (Simplenote forms), CJ-196222 (RTLO filename spoof)."
---

# Markup, RTLO & injected UI

## 1. Overview

Five rows, **$3,500/1 paid**. This module is the corpus's demonstration that clickjacking is not
only an iframe problem: unsanitized markup gives the attacker the same "click on something you did
not intend" outcome from *inside* the page, and Unicode direction overrides do it at the
filename level.

**Case-stock (5 rows / $3,500):**

| Case | Target | Mechanism | Bounty |
|---|---|---|---|
| [CJ-662287](https://hackerone.com/reports/662287) | gitlab | RDoc wiki sanitizer allows `class` on image links → full-page invisible click overlay | **$3,500** |
| [CJ-289823](https://hackerone.com/reports/289823) | automattic | Simplenote desktop renders injected `<form>` → credential phishing | - |
| [CJ-291683](https://hackerone.com/reports/291683) | automattic | injected iframes in a note preview → form-based UI redressing | - |
| [CJ-297547](https://hackerone.com/reports/297547) | automattic | Simplenote Android still renders full forms | - |
| [CJ-196222](https://hackerone.com/reports/196222) | snapchat | U+202E (RTLO) in message → `songexe.mp3` displays as `songexe.mp3` | - |

## 2. The $3,500 overlay: `class` is the whole exploit

CJ-662287 is filed as XSS but is structurally clickjacking — an invisible anchor covering the
page:

> When creating an RDoc wiki page it's possible to use a large number of html tags and attributes that are normally sanitized, when creating a linkable image of the format `{<img src>}[link]`

> This will place a link taking over the entire page and intercept any clicks, `atwho-view select2-drop-mask pika-select` are just some real classes that make the links position absolute with a high z-index.

The report goes further — the same primitive builds a credential form inside a modal:

> Another attack that is more likely to work would be to create a form in a modal, which could be used to ask for a username and password:

That is the module's highest-value technique: **spoof the app's own CSS classes** rather than
inventing new markup.

## 3. Client-rendered note apps: forms are the attack

CJ-289823:

> One can inject HTML into a note and create a login form that sends the user's details to a third-party server.

CJ-291683 is the iframe variant inside the same product family, and CJ-297547 shows the Android
client had not received the fix:

> The Simplenote Android application (1.5.6) still allows users to embed fully-fledged forms.

## 4. RTLO: the filename-level deception

CJ-196222 is the smallest-impact row and still instructive — the UI renders the Unicode override
and hides the real extension:

> There seems to be no filtering of strange unicode characters such as U+202E which is an Right-To-Left-Override.

## 5. What pays, what doesn't

- **Paid**: markup that reproduces a *trusted UI* (login form, approval button) inside the real
  origin, or an overlay that intercepts clicks on a privileged action.
- **Unpaid**: raw HTML injection that only defaces; RTLO alone (it is a nuisance finding unless it
  gates a download or a payment).
- Report the sanitizer gap *and* the resulting UI — the GitLab row's price comes from the CSS-class
  overlay, not from "HTML is allowed".

## 6. Cross-references

- `../XSS/` — the injection classes that deliver this markup.
- `01_X-Frame-Options-and-CSP.md` — the iframe form of UI redressing.
- `../18_Misconfiguration/` — sanitizer/header configuration rows.
