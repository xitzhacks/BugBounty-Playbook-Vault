---
title: "Crypto Primitives, Oracles & Signature Forgeries — CBC, JWE, length extension, gem signatures"
type: playbook
category: crypto-primitives
cwe: "CWE-327, CWE-347"
source_count: 10
full_bodies_available: 10
corpus: "h1-brain disclosed_reports.db (3,673 rows) · sha256 8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4"
list_accessed: "2026-11-07"
note: "Anchors: CRYPTO-728110 (Oracle OAM padding oracle, $3,000), CRYPTO-2038484 (Node DiffieHellman, $1,800), CRYPTO-213437 (JWE invalid-curve, $1,000), CRYPTO-126203 (CBC cut-and-paste, $500)."
---

# Crypto Primitives, Oracles & Signature Forgeries

## 1. Overview

Ten rows, **$6,425/6 paid**. Every row is a *construction* failure, not a "weak algorithm" complaint:
CBC without integrity, DH that never regenerates, a signature that can be moved between objects, a
hash that can be extended. The reports' value is in naming the primitive and showing the
consequence.

**Case-stock (10 rows / $6,425):**

| Case | Target | Mechanism | Bounty |
|---|---|---|---|
| [CRYPTO-728110](https://hackerone.com/reports/728110) | deptofdefense | CVE-2018-2879 padding oracle on `encquery` | **$3,000** |
| [CRYPTO-2038484](https://hackerone.com/reports/2038484) | ibb (Node) | `DiffieHellman` does not generate keys after `setPrivateKey` | **$1,800** |
| [CRYPTO-213437](https://hackerone.com/reports/213437) | ibb | JWE RFC 7516 invalid-curve attack across 4 libraries | **$1,000** |
| [CRYPTO-126203](https://hackerone.com/reports/126203) | uber | CBC cut-and-paste on a redirect token | **$500** |
| [CRYPTO-251572](https://hackerone.com/reports/251572) | zomato | length-extension on `md5(secret+url)` | **$100** |
| [CRYPTO-277534](https://hackerone.com/reports/277534) | iandunn-projects | timing attack on app-password compare | **$25** |
| [CRYPTO-275269](https://hackerone.com/reports/275269) | rubygems | gem signature forgery (reusable signature) | - |
| [CRYPTO-745276](https://hackerone.com/reports/745276) | ibb | Dragonblood / WPA3-EAP-pwd design flaws | - |
| [CRYPTO-1238470](https://hackerone.com/reports/1238470) | ibb | FragAttacks — Wi-Fi fragmentation/aggregation | - |
| [CRYPTO-1130416](https://hackerone.com/reports/1130416) | kubernetes | published SHA512 checksums wrong | - |

## 2. Oracles that still pay: the DoD padding oracle

CRYPTO-728110 is the corpus's crypto crown and its report shape is a template — CVE, asset, parameter,
attack class:

> We were able to identify CVE-2018-2879 in Oracle Access Manager

> It's possible to conduct padding oracle attack and recover plaintext from `encquery` parameter

## 3. API-level key-generation bug

CRYPTO-2038484 is the most modern-looking row: a Node crypto API that silently keeps a fixed key.

> DiffieHellman doesn't generate keys after setting a key

The PoC is three calls: `createDiffieHellman(1024)` → `setPrivateKey(Buffer.from("02",'hex'))` →
`generateKeys()`, and the private key stays `02`. Impact is not theoretical — every peer derives
the same shared secret.

## 4. Construction failures you can spot by reading code

- **CBC + attacker-chosen block movement** (CRYPTO-126203): the token is decrypted and re-encrypted
  without integrity, so blocks can be cut and pasted to change the appended data.
- **Length extension** (CRYPTO-251572): `md5(somescret + url) == t` is exactly the
  `secret-prefix MAC` anti-pattern.
- **Reusable signatures** (CRYPTO-275269): a gem signature is not bound to the artifact's contents.

> Inconsistencies in how `gem` processes gem files make it possible to reuse a signature from an existing signed gem and apply it to arbitrary contents. The forged gem will install even with `-P HighSecurity`.

- **Spec-level curve validation** (CRYPTO-213437): `node-jose`, `jose2go`, `Nimbus JOSE+JWT` and
  `jose4j` all accepted invalid curve points.

## 5. What pays, what doesn't

- **Paid**: oracle → plaintext recovery (even on a vendor product), key-generation defects with an
  evident shared-secret outcome, signature reuse that installs code.
- **Near-zero**: constant-time comparison nits in low-value plugins (CRYPTO-277534 paid $25).
- **Unpaid in this corpus**: protocol design papers (Dragonblood, FragAttacks) and checksum
  mismatches — real work, but coordination/no-figure rows.
- Always state the *recovered secret* or the *forged artifact*; the primitive alone triages low.

## 6. Cross-references

- `01_TLS-STARTTLS-Legacy-Protocol.md` — transport-layer siblings.
- `03_Cert-Validation-Weak-Secrets-Insecure-Channel.md` — key/secret handling.
- `../Race-Conditions/Library-Timing-Adjacent.md` — the timing-oracle rows.
