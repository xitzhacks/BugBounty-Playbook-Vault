---
title: "Adjacent & unclassified — GHSL CodeQL corpus and the IV-reuse row"
type: playbook
category: crypto-adjacent
cwe: "CWE-295, CWE-297, CWE-326, CWE-347"
source_count: 21
full_bodies_available: 20
corpus: "h1-brain disclosed_reports.db (3,673 rows) · sha256 8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4"
list_accessed: "2026-11-07"
note: "20 of 21 rows are GHSL one-liners (`This bug was reported directly to GitHub Security Lab.`, 54 bytes) — metadata-only, never quoted. The single full body is CRYPTO-170548 (Ruby OpenSSL GCM IV reuse, $500)."
---

# Adjacent & unclassified — the CodeQL corpus block

## 1. Overview

Twenty-one rows, **$43,600/21 paid** — and twenty of them have no readable body. This module is
cryptography's version of a DoD corpus: the metadata is the whole record, and the honest treatment
is a block, not invented technique.

**Case-stock (21 rows / $43,600):**

| Case | Program | Bounty | What the title tells us |
|---|---|---|---|
| [CRYPTO-170548](https://hackerone.com/reports/170548) | ruby | **$500** | Ruby OpenSSL library — IV reuse in GCM mode (**full body**) |
| CRYPTO-1094343 | github-security-lab | $4,500 | Java CWE-326: insufficient key size |
| CRYPTO-1184041 | github-security-lab | $4,500 | Java CWE-347: improper signature verification → auth bypass |
| CRYPTO-1212274 | github-security-lab | $4,000 | Java CWE-347 (variant) |
| CRYPTO-1219493 | github-security-lab | $4,000 | Java CWE-295: incorrect hostname verification → MITM |
| CRYPTO-896299 | github-security-lab | $1,800 | Java CWE-297: insecure JavaMail SSL configuration |
| CRYPTO-917454 | github-security-lab | $1,800 | Java CWE-273: unsafe certificate trust |
| CRYPTO-917456 | github-security-lab | $1,800 | Java CWE-295: incorrect hostname verification |
| CRYPTO-1100379 | github-security-lab | $1,800 | Java CWE-295: disabled certificate validation in JXBrowser |
| CRYPTO-1123360 | github-security-lab | $1,800 | Java CWE-327: more broken crypto algorithms |
| CRYPTO-1212272 | github-security-lab | $1,800 | Go CWE-326: insufficient key size |
| CRYPTO-1250306 | github-security-lab | $1,800 | Java CWE-295: insecure TrustManager |
| CRYPTO-1264781 | github-security-lab | $1,500 | Java CWE-295: insecure TrustManager (variant) |
| CRYPTO-1329260 | github-security-lab | $1,800 | Java: static initialization vector |
| CRYPTO-1481247 | github-security-lab | $1,800 | Java: ignored hostname verification |
| CRYPTO-1484086 | github-security-lab | $1,800 | C# CWE-759: password hash without salt |
| CRYPTO-1490400 | github-security-lab | $1,800 | Python CWE-338: insecure randomness |
| CRYPTO-1567588 | github-security-lab | $1,800 | Java CWE-321: hardcoded JWT secret keys |
| CRYPTO-1710575 | github-security-lab | $1,800 | C++ CWE-297: cert/host mismatch |
| CRYPTO-1161808 | github-security-lab | $1,000 | Java CWE-759: password hash without salt |
| CRYPTO-151868 | algolia | $100 | *(adjacent)* no rate limit on contact invites — misfiled keyword row |

## 2. The one full body: GCM IV reuse

CRYPTO-170548 is worth keeping in full because it is the construction error the CodeQL rows only
name abstractly: reusing an IV in GCM destroys confidentiality *and* authenticity.

> Ruby OpenSSL Library - IV Reuse in GCM Mode

GCM security collapses on nonce reuse — the second ciphertext leaks the XOR of plaintexts and the
authentication key can be recovered. Treat every "static IV" / "reused nonce" CodeQL hit as
potentially this severity.

## 3. How to use this block

- **Mapping table**: the CWE list here is the practical Java/Go/C#/Python crypto-query set —
  CWE-295/297 (transport trust), CWE-326/327 (strength/algorithms), CWE-347 (signature
  verification), CWE-321/338/759 (secrets/randomness/salted hashes). Use it as a review checklist
  on any codebase.
- **Pricing signal**: GHSL paid $1,000–$4,500 per accepted query. That is a *code-analysis*
  market, not an app-hunting market — do not extrapolate these figures to a web target.
- **Never quote** the twenty one-liners; there is nothing but the sentence
  `This bug was reported directly to GitHub Security Lab.`

## 4. The adjacent row

CRYPTO-151868 (rate limit on inviting contacts) is in this module only because the keyword net
caught it; its home is `../20_Rate-Limiting/`.

## 5. Cross-references

- `02_Crypto-Primitives-Oracles-Signatures.md` — the concrete constructions behind CWE-347/326.
- `03_Cert-Validation-Weak-Secrets-Insecure-Channel.md` — CWE-295/297 in application code.
- `../20_Rate-Limiting/` — CRYPTO-151868's real class.
