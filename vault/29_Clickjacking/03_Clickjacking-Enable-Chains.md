---
title: "Clickjacking-Enable Chains — where the click opens something bigger"
type: playbook
category: clickjacking-chains
cwe: "CWE-1021"
source_count: 4
full_bodies_available: 4
corpus: "h1-brain disclosed_reports.db (3,673 rows) · sha256 8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4"
list_accessed: "2026-11-07"
note: "Anchors: CJ-1274695 (Burp Scanner RCE via clickjacking, $3,000), CJ-643274 (DM link truncation → Google creds), CJ-892289 (self-XSS → ATO in Firefox), CJ-953579 (self DOM-XSS trigger)."
---

# Clickjacking-Enable Chains

## 1. Overview

Four rows, **$3,000/1 paid**. Every one is a clickjacking row whose value is the *next* step: a
self-XSS that only fires after a click, a scanner's embedded browser, a truncated link. The
clickjacking itself is worth nothing — the chain sets the price.

**Case-stock (4 rows / $3,000):**

| Case | Target | Mechanism | Bounty |
|---|---|---|---|
| [CJ-1274695](https://hackerone.com/reports/1274695) | portswigger | Burp's headless Chrome + clickjacking → remote-debugging GUID → RCE of scanner | **$3,000** |
| [CJ-643274](https://hackerone.com/reports/643274) | x | DM link truncation after 38 chars → fake YouTube → Google credential capture | - |
| [CJ-892289](https://hackerone.com/reports/892289) | imgur | frameable embed page + self-XSS → ATO (Firefox) | - |
| [CJ-953579](https://hackerone.com/reports/953579) | automattic | clickjacking triggers self DOM-based XSS on `api.tumblr.com/console` | - |

## 2. Self-XSS is not dead if you can make the victim click

CJ-892289:

> I discovered that have some endpoints that permits to frame imgur.com with some limitations, but even in this case, it is possible to carry out a proof of concept.

CJ-953579 is the same composition with a DOM sink: the console page has both a frameable endpoint
and a self DOM-XSS, so the click is the delivery.

> A attacker can exploit the clickjacking  to trigged the self DOM-based XSS

That is the canonical answer to "self-XSS is out of scope": show the click.

## 3. The $3,000 chain: clickjacking against tooling

CJ-1274695 is the corpus's most unusual row — the victim is a security tool's own embedded browser:

> Burp Suite utilizes an embedded Chrome browser for crawling and scanning web applications. The Chrome instance is launched in headless mode, with remote debugging enabled via the remote-debugging websocket port instead of remote-debugging-pipe. As a result, a known XSS vulnerability in Chrome can be leveraged in combination with a JavaScript port sniffing and ClickJacking attack to compromise the WebSocket GUID for the remote debugging channel.

Note the shape: clickjacking is used to *obtain a token* (the debug GUID), not to perform an action.
Look for frameable pages that reveal state to the framer.

## 4. UI deception without a frame

CJ-643274 is filed under clickjacking but is pure UI deception in a chat client:

> Because very long links in direct messages are truncated after 38 characters the malicious actors were able to provide a malicious link in a direct message that appeared as though it was to an authenticated YouTube video and caused a clickjacking scenario to occur.

## 5. What pays, what doesn't

- **Paid**: the chain terminates in ATO, credential capture, or code execution.
- **Unpaid**: a clickjacking PoC that only proves framing — the corpus's plain-header rows top out
  near $1,000 and most earn nothing.
- Write the chain as numbered steps with the victim's clicks counted; every paid row here does.

## 6. Cross-references

- `01_X-Frame-Options-and-CSP.md` — the enabling condition.
- `../XSS/` — self-XSS and DOM sinks.
- `../CSRF/` — clickjacking bypasses CSRF tokens; this module is the "one extra click" form.
