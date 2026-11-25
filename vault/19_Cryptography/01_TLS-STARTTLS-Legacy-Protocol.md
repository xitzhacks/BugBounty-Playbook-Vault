---
title: "TLS / STARTTLS / Legacy Protocol — stripping, downgrade, and protocol injection"
type: playbook
category: crypto-tls-protocol
cwe: "CWE-757, CWE-326"
source_count: 7
full_bodies_available: 7
corpus: "h1-brain disclosed_reports.db (3,673 rows) · sha256 8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4"
list_accessed: "2026-11-07"
note: "Anchors: CRYPTO-144782 (Python smtplib STARTTLS stripping, $1,000), CRYPTO-1178562 (Ruby net/imap, $500), CRYPTO-1334763 (curl CVE-2021-22947)."
---

# TLS / STARTTLS / Legacy Protocol

## 1. Overview

Seven rows, **$1,500/2 paid**. The class is not "weak cipher" — it is *the upgrade never happened*
or *the downgrade was accepted silently*. STARTTLS stripping is the star: the client asks to
upgrade, the MITM answers "no such command", and the client continues in cleartext without
raising an error.

**Case-stock (7 rows / $1,500):**

| Case | Target | Mechanism | Bounty |
|---|---|---|---|
| [CRYPTO-144782](https://hackerone.com/reports/144782) | ibb (Python) | `smtplib` does not raise on unexpected STARTTLS reply → stripping | **$1,000** |
| [CRYPTO-1178562](https://hackerone.com/reports/1178562) | ruby | `net/imap` same failure (CVE-2016-0772) | **$500** |
| [CRYPTO-1334763](https://hackerone.com/reports/1334763) | curl | STARTTLS response pipelining → forged encrypted responses | - |
| [CRYPTO-166629](https://hackerone.com/reports/166629) | ibb (OpenSSL) | DROWN — SSLv2 cross-protocol | - |
| [CRYPTO-166634](https://hackerone.com/reports/166634) | ibb (OpenSSL) | SSLv2 doesn't block disabled ciphers (DROWN bypass) | - |
| [CRYPTO-288966](https://hackerone.com/reports/288966) | x | POODLE on multiple Twitter SMTP servers | - |
| [CRYPTO-953219](https://hackerone.com/reports/953219) | portswigger | Postfix SMTP interaction theft via MITM | - |

## 2. STARTTLS stripping — the library does not check the reply

CRYPTO-144782 states both the cause and the blast radius:

> Python's implementation of `smtplib` fails to raise an exception upon an unexpected response during negotiation of tls via the starttls protocol. This allows a MiTM capable of injecting smtp messages to force smtplib to

The report's version table is the era artifact worth copying into any report — ranges, not "all":

> python 2.7.2 - 2.7.11 (dates back ~14 years)
>  * python 3.0 - 3.5.1 (dates back ~7 years)

CRYPTO-1178562 is the same finding in Ruby, and it names the *caller* precondition that decides
exploitability:

> This may allow a malicious MITM to perform a starttls stripping attack if the client code does not explicitly set `usessl = true` on ` initialize` where it is disabled by default

## 3. Protocol injection at the upgrade boundary

CRYPTO-1334763 (curl CVE-2021-22947) is subtler: the attacker pipelines plaintext into the
STARTTLS handshake so the *first encrypted read* returns forged data.

> A man-in-the-middle can inject cleartext forged responses to future encrypted commands  by pipelining them to the STARTTLS response.

> Upon test failure, the downloaded file contains "You've been hacked!" rather than the requested mail.

## 4. Legacy protocol rows (DROWN / POODLE)

CRYPTO-166634 explains why the DROWN family paid nothing directly in this corpus but mattered:

> This is a DROWN-related issue that essentially circumvented the instructions on how to disable SSLv2 at the time. Its primary effect was that a lot of servers were vulnerable to DROWN even though they thought they had SSLv2 disabled.

CRYPTO-288966 shows the operational proof for POODLE — `nmap` script plus SMTP servers, not a
theoretical CVE mention.

## 5. What pays, what doesn't

- **Paid**: a library-level failure with a *client-visible* consequence (a MITM that wins), plus a
  reproducible test.
- **Not paid in this corpus**: "your server supports TLS 1.0" style hygiene, unless the program's
  VRT prices it.
- Include protocol/version ranges and the exact server response that should have aborted the
  handshake — that is the evidence triage needs.

## 6. Cross-references

- `02_Crypto-Primitives-Oracles-Signatures.md` — padding oracles and signature forgeries.
- `03_Cert-Validation-Weak-Secrets-Insecure-Channel.md` — the client half (no cert check).
- `../14_HTTP-Request-Smuggling/` — protocol-injection siblings.
