---
title: "Misconfiguration testing agent playbook — the executable protocol"
type: agent-playbook
category: misconfiguration-all
cwe: "CWE-829, CWE-287, CWE-799, CWE-16, CWE-319, CWE-200, CWE-707, CWE-601"
built: "2026-11-07"
corpus: "166 rows (152 classified misconfig bucket + 14 unclassified merges) → 166 bodies read · 47 paid · $34,532"
bounty: "bucket $25,932/38 + merges $8,600/9 = $34,532/47 · max $6,300 (MISCONF-1258871) · next $3,750 (MISCONF-815085)"
companion_modules: "01 subdomain-takeover-dangling-state · 02 account-verification-rate-limiting · 03 headers-tls-transport-misconfig · 04 exposure-api-secrets-config · 05 spoofing-phishing-homograph-open-redirect · 06 adjacent-unclassified-merges"
quote_rule: "byte-true, from read bodies only; GHSL one-liners and short pointers recorded never quoted as technique"
---

# Misconfiguration Testing Agent Playbook

Executable protocol derived from 166 read bodies (classified misconfig bucket 152 + unclassified merges 14) + the module map's frozen assignment (`references/archive/classes.json`). Crown doctrine up front: **payouts track demonstrated trust-capture, not flaw cleverness** — the $6,300 row is an *unauthenticated URL* with config + pprof read-back; the $3,750 row is a *registration form* that lets garbage past validation; the $3,000 row is a *cancelled CDN instance* reclaimed; the $0 rows are 115 rows with no figure, most of them shallow or theoretical. The vault's pricing slope is: read-back completeness (config dump > PoC page > token-oracle > scanner line). Run phases in order; abort at kill-gates. Every step cites corpus evidence.

## P0 — Scope and trust-surface read (before any request)

1. **Program shape.** This corpus's paid patterns need (a) a trusted name or origin (subdomain, shortener, support email, app bullet), (b) an instance the owner stopped operating, or (c) an unauthenticated operations plane. Read policy for allowed claim types (takeover PoC vs takeover prevention-only), test-account rules, and notification-channel abuse allowances. The corpus analog for "takeover with PoC required" is MISCONF-2899858's mozilla program note: *"Domain takeovers supported by a proof of concept … If the domain is pointing to a claimed instance by another company, then the report will not be eligible for bounty."*
2. **Kill-gate:** P0 produces the *trust inventory* only — every name, link, and token this program's users are taught to trust. No testing yet.

## P1 — Misconfiguration inventory (passive first)

1. **Pointers** — dangling CNAMEs (Fastly/Heroku/Vercel/GitHub Pages/GSuite, modules 01 §§2–3), unclaimed S3/bucket origins (01 §4), repo/docs links to dead domains (01 §5), capturable handles/social links (04 §6). Tool: `dig`/cert-transparency + CDN "unknown domain" error strings, all corpus-evidenced (Fastly "unknown domain", S3 `NoSuchBucket` XML).
2. **Identity flows** — signup/login/verification/OTP/resend/token-lifetime endpoints and their *order* (02 §§3–4): back-button landings, resend links, SSO backdoors, 2FA downgrade paths, session invalidation on password change.
3. **Headers and transport** — HSTS (with trailing-dot/IDN/case variants), CSP (renderer-consistency + host-list audit), CORS (reflection + credentials check), referrer-policy, TRACE/XST, mixed-content walk, cache-deception `/.css` path confusion, CPDoS third-party origins (03 §§2–4).
4. **Exposure** — unauthenticated `/config`, `/debug/pprof`, setup/install pages, `.idea`, Actuator-style paths (04 §2; merges 1137966/909374). *Reachability without credentials is the probe.*
5. **Rendering surfaces** — IDN/punycode handling, blocklists, URL eliding, error-page reflection, path reflection (05 §§2–4).
6. Out-list: cipher-strength inventories, theory memory-safety reviews, and time-only claims (04 §7's Tor row; 03 §6's $1 row) — hygiene, file as notes.

## P2 — Probe protocol (cheapest signal → strongest read-back)

1. **Claim, don't hypothesize** — module 01 ladder: dangling pointer → register the instance → serve content → record PoC URL (154425 → 2706358/2899858). A blind write without read-back dies (172549).
2. **Flow-order probes** — module 02 ladder: attempt the verification screen → back-button / skip / token-possession / SSO-trust-inheritance / downgrade-without-password (57764 → 229619 → 617896 → 587910). Then rate-limit position (before/after the oracle — 262830), scope (per-endpoint reset — 170310), expiry (792295), and resend cost (263010, 774050/854793, 1202408).
3. **Downgrade probes** — module 03 ladder: HTTP page carrying credentials → SSO cleartext leg → emailed password/token → `Referer` leak → protocol-policy semantics (214571 → 703759 → 2337938/342693 → 2437131). Cache-deception/poisoning probes (`<random>.css`, x-forwarded-port, CPDoS headers) only with *authenticated-victim* setup (1271944/631589/1010858).
4. **Shadow-diff the API** — module 04 ladder: UI-gated action vs API route (1086781), identity mutation without verification (906790), support-channel identity binding (2001913/2068830), secret placement (2129769/1213181), notification silence (240083/961841).
5. **Deception probes** — module 05 ladder: punycode rendering check → fix-bypass (@, /@, trailing dot) → error-page reflection → blocklist normalization → open-redirect header attack (210875) → address-bar capture (175958). Every spoofing probe needs a *victim-eye screenshot* (the captured-trust artifact).
6. **Boundary probes** — module 06 ladder for what misconfig means next: default-cred dialing where in scope (398797), mail-auth posture (491753), DNS/DMARC inventory.

## P3 — Proof ladder (modest demonstrations paired with read-backs)

1. Module 01's ladder: claim + serve + PoC URL. (Fastly pair for $500–$3,000.)
2. Module 02's ladder: account state visible without verification (mass-creation evidence for 815085-class rows; verified-flag change for 229619-class).
3. Module 03's ladder: downgrade victim capture (sslstrip log; hooked `Referer` log; cached PII read-back; cookie forged in victim cookie jar).
4. Module 04's ladder: config/pprof read-back, visibility flip read-back (200 response), victim-forced POST artifact, ticket-created-on-victim artifact — one wire capture each, no exfil of real users' PII.
5. Module 05's ladder: the victim-eye capture (short-link → attacker domain; address bar claiming facebook.com; blocklisted domain loading).
6. Module 06's ladder for merges: read back the 2FA removal or the CORS-reflected response; GHSL-class one-liners are **metadata-only** — never cited as technique.

## P4 — Modern hardening fingerprints (never corpus doctrine)

The 2015–2024 findings map to these modern *expectations*; a corpus-identical trigger on a modern stack usually means the hardening is absent, not that the class is dead:

- **Pointers**: DANE/CAA + pre-provisioning monitoring; modern CDNs refuse orphan claims only where the prior owner asserted them (the 01 pair); link checkers for docs.
- **Identity**: IdP account-linking never weaker than native verification (617896's lesson), step-up for security downgrades (587910/178293), token lifetimes (1784162's 10-minute anchor), notification as detection channel (240083/961841).
- **Transport**: HSTS preload + normalized hostnames (1565622/1753226/1813831), CSP with non-goog host allowlists (199779), CORS allowlist + credentials never reflected (235200/426165), TLS 1.3-only + disabled-protocol semantics (2437131).
- **Exposure**: ops planes on separate authn (1258871), setup pages disabled post-install (1626205), Actuator/pprof allowlisted (1137966).
- **Spoofing**: punycode rendering + IDNA normalization everywhere (172933's sentence is the spec), blocklist normalization w/ trailing dots (1068505), `rel=noopener` on all `_blank` (158002).

## P5 — Pre-report gates (kill-gates)

1. **Trust gate** — you can name the trust being captured (name, link, skin, sender, token) *and* show it captured. Scanner-line headers with no carrier die here (163676's bare "missing CSP" is the anti-exhibit).
2. **Read-back gate** — config, PII cache, changed state, or victim-eye artifact in hand. Blind writes, enumeration-free limits, and theory rows (115686) die here.
3. **Identity gate** — you state which identity the effect binds to (victim account, employee, collaborator, support desk). Token-possession-for-inbox-possession (229619) and From-header-as-identity (2001913/928255) fail this gate unless the binding is the finding.
4. **Ordering gate** — the rate limit fires *before* the oracle, covers the identity (not the endpoint), and expires (262830/170310/792295). Limits that fail any leg are filed as enumeration/limit-ordering, not as "no rate limit."
5. **Era gate** — cipher/protocol inventories need downgrade semantics (2437131); outdated-CVE theory needs its own PoC (module 06's 250587-analog class). The $1 row (131065) is the priced warning.
6. **Noise gate** — the module-06 gallery: race/traversal/XSS/crash/CSRF rows mislabeled as misconfig; incorrect buckets never rescue an out-of-scope bug. Match the platform's VRT, not the corpus label (the bucket's labels are "Violation of Secure Design Principles" 119× — useless for filing).

## Module ↔ phase table

| Phase | Corpus evidence (modules) | Anatomy of the paid pattern |
|---|---|---|
| P1 inventories pointers, identity, headers, exposure | 01 (§2-§5), 02 (§3-§4), 03 (§2-§5), 04 (§2-§6), 05 (§2-§5) | dangling CNAMEs; resend links; cache keys; /config reachability; IDN rendering |
| P2 probes claim → flow-order → downgrade → shadow-diff → deception | 01 §2, 02 §§3-4, 03 §§2-4, 04 §§2-4, 05 §§2-5 | serve PoC; back-button; sslstrip; API 403-expectation; victim-eye screenshot |
| P3 proofs with read-backs | 02 §2, 03 §2, 04 §§2-3 | account state; cached PII; config + pprof; victim-forced POST |
| P4 hardening fingerprints | 03 §2, 04 §4, 05 §4 | HSTS preload; CSP host audit; CORS allowlist; punycode |
| P5 kill-gates | 06 (§2-§3), 04 §7, 03 §6 | drift rows; Tor theory; $1 inventory; GHSL one-liners |

## Non-goals

- Cache-poisoning *weaponization* beyond misconfig causal rows (CPDoS details, cache-key taxonomy) — that lives in `15_Cache-Poisoning/`; this vault cites the corpus rows only.
- Proof-reading token/crypto *constructions* (MAC ambiguity 661051, key storage) beyond the misconfig framing — those belong to `19_Cryptography/`.
- Race-condition primitives as primary technique — the vault's race rows (157996/165570) are classification-drift exhibits; rate-limit *ordering* is the misconfig doctrine (module 02 §4 / `20_Rate-Limiting/`).
- Host-header attack internals beyond the redirect primitive — `24_Host-Header-Injection/` owns them.
- Live claim/takeover attempts on in-scope-but-unconsented infrastructure: read notifications and test-account rules first; for takeover PoCs use content you control (your own claimed instance, `haveanicetakeover-poc.html`-style markers) and remove/reset them on request — the corpus's politest PoCs (148770's wildcard surrender) are the standard.
