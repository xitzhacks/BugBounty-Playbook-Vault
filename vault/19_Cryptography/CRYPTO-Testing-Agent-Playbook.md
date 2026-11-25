---
title: "Crypto Testing Agent Playbook — the executable protocol"
type: agent-playbook
category: crypto
cwe: "CWE-327, CWE-295, CWE-347"
built: "2026-11-07"
corpus: "46 rows (26 bucket + 20 merges), all full-body (h1-brain disclosed_reports.db)"
bounty: "$55,105/36 paid · 01 $1,500/2 · 02 $6,425/6 · 03 $3,680/7 · merges $43,400/20 · adjacent $100/1"
companion_modules: "01 tls-starttls-legacy-protocol · 02 crypto-primitives-oracles-signatures · 03 cert-validation-weak-secrets-insecure-channel · 04 adjacent-and-unclassified"
quote_rule: "byte-true to CRYPTO-bodies-full-dump.txt"
---

# CRYPTO Testing Agent Playbook

## P0 — Define the class you are hunting

Cryptography findings are paid by **break**, not by **hygiene**. Before testing, decide which of
these you can demonstrate:

1. A secret recovered (plaintext, key, session).
2. A check that did not happen (certificate, integrity, signature binding).
3. A construction that lets you move/forge data (CBC cut-and-paste, length extension).
4. A key that is guessable or never regenerated.

Anything else is a configuration opinion — route it to `../18_Misconfiguration/`.

## P1 — Inventory constructions

| Signal in code/response | Class | Module |
|---|---|---|
| `Cipher.getInstance("AES/CBC/…")` without MAC | CBC malleability | 02 |
| `md5(secret + user_input)` used as a token | length extension | 02 |
| Signature not covering the payload (gem/zip/JWT fields) | forgery | 02 |
| DH/ECDH with `setPrivateKey`/fixed scalar | keygen defect | 02 |
| `starttls()` return value unchecked | stripping | 01 |
| `TrustManager`/`NSURLSession` permissive callbacks | no cert validation | 03 |
| `SECRET_KEY = "..."` literal / short TOTP secret | weak secret | 03 |
| `http://` links in transactional email or build scripts | insecure channel | 03 |

## P2 — Probe protocol

1. **Transport**: intercept with a proxy and a self-signed CA. If the client proceeds, that is the
   finding (CRYPTO-168538: stock iPhone, no CA installed).
2. **Oracle**: for padding/CBC, mutate one byte at a time and measure distinct error/length
   responses; build the decryption loop until a block is recovered.
3. **Fuzz-and-derive for keygen defects**: set a key, call the generate function, read the key back
   (CRYPTO-2038484).
4. **Token algebra**: decode, flip, re-encode. If the server accepts, capture the new behavior
   (redirect, XSS, privilege).

## P3 — Proof ladder

1. **Observation** — the code or behavior is wrong.
2. **Control** — the same input with a valid cert/valid MAC fails.
3. **Recovery/forgery** — plaintext, forged artifact, or captured token.
4. **Consequence** — ATO, redirect to attacker, code install, data exposure.

Report which rung you reached; the corpus's paid rows reach 3 and 4.

## P4 — Modern hardening fingerprints

- TLS: `min_version=TLSv1.2`, HSTS preload, no STARTTLS-only mail paths; certificate pinning in
  mobile.
- Crypto: AEAD (GCM/ChaCha20-Poly1305) instead of CBC; `hmac.compare_digest`/`hash_equals` for
  comparisons; RFC 4226/6238 minimum secret lengths.
- Signature schemes: content-addressed (transparency-log) artifact signing; JOSE libraries now
  validate curve points.
- Secrets: env-managed keys; scanner tools (e.g. the report's "CookieMonster") catch literal
  `SECRET_KEY`s.

## P5 — Kill-gates

1. **No break demonstrated** → informational; do not submit "weak algorithm" alone.
2. **Theoretical MITM without a client that skips validation** → not a finding.
3. **CVE mention without target verification** → run the check against the actual asset.
4. **Unpatched-but-unreachable code** → note it, price it low, or skip.
5. **Scope**: crypto library CVEs belong in the library program (ibb), not in every downstream app.

## Module ↔ phase table

| Phase | Modules | Paid pattern |
|---|---|---|
| P1 inventory | 02, 03 | construction/secret identification |
| P2 probe | 01, 02 | oracle loop / stripping MITM |
| P3 proof | 02, 03 | recovered plaintext / forged artifact |
| P4 hardening | 01, 03 | AEAD, pinning, secret management |
| P5 gates | all | break statement required |

## Non-goals

- Weak-cipher-suite scans (SSLLabs output) without a program that prices them.
- Academic protocol papers (Dragonblood, FragAttacks) — recorded as corpus rows, not as targets.
- Key-length opinions for legacy systems outside the program's scope.
