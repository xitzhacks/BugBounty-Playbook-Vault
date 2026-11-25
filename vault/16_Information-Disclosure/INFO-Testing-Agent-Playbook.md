---
title: "INFO Testing Agent Playbook — the executable protocol"
type: agent-playbook
category: info-disclosure-all
cwe: "CWE-200, CWE-359, CWE-212"
built: "2026-11-07"
corpus: "362 h1-brain corpus rows (bucket-340 + 22 unclassified merges) · 356 full bodies + 6 GHSL metadata-only one-liners · all bodies read end-to-end (classified bodies verified byte-equal to DB: 0 mismatches)"
bounty: "$281,925 across 161 rows (bucket-340 $217,375/149 · merges $64,550/12) · modules: 01 $19,252/13 · 02 $83,580/28 · 03 $47,014/56 · 04 $48,697/41 · 05 $15,468/6 · 06 $67,914/17"
companion_modules: "01 graphql-api-objects-exposure · 02 hackerone-reports-bounty-privacy · 03 user-pii-location-privacy · 04 file-path-errors-secrets-leaks · 05 protocol-memory-disclosure · 06 adjacent-disclosure-noise"
quote_rule: "byte-true, from archived bodies only; GHSL one-liners recorded never quoted as technique"
---

# INFO Testing Agent Playbook

Executable protocol derived from 362 h1-brain corpus rows + modern hardening fingerprints. Every step cites corpus evidence. Run phases in order; abort at kill-gates. Crown-jewel doctrine up front: **disclosure pays by whose data and what class, not by technique** — module 02's `/reports/:id.json` paid $25,000 because it serialized a *third party's* OTP codes and `graphql_secret_token`, module 04's GitLab serialization paid $12,000 because it serialized *another project*'s runner tokens, module 05's pixel paid $8,868 because the co-resident memory held *live AWS keys* — while the same primitives pointed at benign content paid $100 (INFO-53004's "not sensitive" probe pages) or $0 (the dotfile singles). The vault's highest per-finding premium: the credential-class field that needs no chain (module 06's $50,000 PAT; module 02's $25,000 JSON twin).

## P0 — Program classification & policy read (before any probe)

1. Program type: commercial bug bounty vs VDP vs platform self-audit. The corpus's `security` team (83 rows) priced *its own* disclosures at flat per-field tiers ($2,500 ×5 in module 01; $500 ×20 in module 02) — self-audits overpay for narrow executable proofs (INFO-3000510: 569 bytes → $25,000) and underpay for broad possibility claims. Read the program's disclosure rules first: which endpoints are in scope (`.json` twins? exports? GraphQL?), which data classes are *other people's* (the vault's price multiplier), and whether informative/out-of-scope for privacy data. The corpus's unpaid 201 rows are a policy lesson: many privacy findings were filed informative without figures — check the program's privacy exclusions *before* the P1 inventory.
2. Environment signal: classify the stack — GraphQL-first (module 01: HackerOne/Shopify field auth), serializer-heavy (module 04: Rails/GraphQL/REST twins of the same object), cache/CDN-fronted (module 03: Active Storage, async-search), image-pipeline (module 05: SVG/GIF conversion), mobile-shipped secrets (modules 04/06: Podfile, Cloudinary, PAT-in-app). Each signal selects a different P1 inventory.
3. Kill-gate: no probing yet — P0 produces the *policy envelope* only (in-scope surfaces, other-people's-data definition, credential-class list).

## P1 — Surface inventory (fields, serializers, exports, caches)

1. **GraphQL selection sets** — every object the UI shows partially: Team, User, Project, Order, SurveyRatingItem. Corpus evidence: INFO-978143 (`private_comment` via `node(id:)`), INFO-489146 (`otp_backup_codes`, `vpn_credentials`, `calendar_token` via `users()`), INFO-972355 (`user{email}`), INFO-633001 (system notes via `bodyHtml`). Inventory: introspection → per-object field diff vs the UI (fields present in schema, absent in UI = candidate disclosures).
2. **Serializers & machine twins** — `.json` suffixes, export features, feeds. Evidence: INFO-3000510 (`/reports/:id.json`), INFO-509924 (Quick Actions JSON response), INFO-182358/186230 (Export-as-zip), INFO-1256375 (`.atom` feed on the preview host), INFO-1575014 (Node SDK path normalization turning Retrieve into List). Inventory: every HTML page × its `.json`/`.atom`/`/feed` twin; every export button × the archive contents.
3. **Redaction pipelines** — the layer that *removes* data: export zips/PDFs, disconnected-role views, timed redaction. Evidence: INFO-2054222 (usernames on exported PDF), INFO-880863 (GitLab todos after membership change), INFO-1784310 (expired conversations still readable). Inventory: *redact-then-export* and *remove-then-export* pairs (module 02's $10,000→$12,500 pair is the cautionary tale: the fix shipped the residue).
4. **Caches, headers, and shared stores** — `Set-Cookie` on public-cacheable responses (INFO-3082917), authorization headers in search indexes (INFO-1042716), redirect header non-clearing (INFO-2243710 trio), CI logs and Slack exports (INFO-2915647, 2467999). Inventory: response-header audits (`Cache-Control` × `Set-Cookie`), log/index retention of credentials.
5. **Request-path hygiene** — dotfiles, indexes, verbose errors, full paths. Evidence: INFO-218465 (`.git` logs), INFO-46345 (directory index), INFO-46366 (stack trace), INFO-1354334 (full path in delete error), INFO-1021906 (bucket root listing). Inventory: `/.git/`, `/.env`, `/.htpasswd`, `/.htaccess`, `/.DS_Store`, directory listings, error-page verbosity, S3/GCS bucket roots.
6. Out-list: CVE-library rows in module 05 are *version fingerprints* (librsvg/NGINX/curl versions come from headers/ banners), not payload guesses — confirm the vulnerable component is actually the disclosed one before claiming the primitive.

## P2 — Probe protocol (from cheapest signal to hardest)

Per candidate surface, in corpus-evidence order, with pricing attached:

1. **Field oracle (single query/click)** — module 01's $2,500 flat: add the hidden field to one GraphQL query (`whitelisted_hackers{total_count}`, `report_sources`, `vpn_suspended`) or fetch the `.json` twin. The discriminators that paid were *classifiers* (non-empty = private; false = has-private-with-VPN), not bulk dumps. Price: $500–$2,500 per field when the JSON response carrying the value is shown.
2. **Differential count** (module 03's enumeration ladder) — INFO-125200's two-string invite differential (60M space, sample-and-extrapolate → $3,000) and INFO-505424's 403-vs-200 `onload`/`onerror` de-anonymizer ($1,470). Method: baseline two known-absent/known-present identifiers, then walk the ID space. Price binds *names to accounts* at ~$1,500–$3,000; counts-only at $500 (module 02's INFO-410015 progression: 129→130→131).
3. **Oracle-against-redacted** (module 02's search/bot tier) — INFO-2213251's character-by-character secret extraction via Hacktivity search (~1,200 tries for a 40-char secret) and INFO-247628's hackbot duplicate-match on *real* redacted text. Method: any system that indexes/holds the full secret and answers presence/absence. Price: $1,500–$2,500 when the extraction loop is demonstrated on a test secret.
4. **Enumeration & brute-force with throttling removed** (module 03's INFO-968165 order lookup) — strip the email local-part, walk `order_number` from `#1000`. Price: $2,500 when the *response carries other customers' order data* (show the blob).
5. **Cache/header & log sweep** (module 03/04's $400–$1,500 tier) — re-fetch blob URLs without cookies and inspect caches (`/.async-search`, `Set-Cookie` on public responses); grep public CI logs / Slack exports / Docker images for `auth:`/`token`/`apiKey`. Price climbs when the artifact is *usable* (Netlify Owner-role token $1,500; Jira Admin keys $1,000).
6. **Dotfile/bucket/feed sweep** (module 04/06's $100 floor) — the cheapest rung: `/.git/logs/refs/heads/master`, bucket-root listing, `.atom` on preview hosts, `.htpasswd`. Price: $100–$500 per real fetchable file; **benign content caps at ~$100** (INFO-53004).
7. Skeleton quote (module 01 — honest self-limit): INFO-415622's "I'm not too sure if this is intentional… kindly close this as `Informative`" still paid $500 — showing you stopped at the boundary is what era-triage rewarded.

## P3 — Proof ladder (the demonstrations that paid)

1. Module 01's JSON-response proof: query → raw JSON blob with the sensitive field visible (INFO-978143's `private_comment`, INFO-770209's `["HackerOne Platform"]`). Never "the field exists" alone.
2. Module 02's twins-and-zips: `.json` fetch showing credentials of a *third party* (INFO-3000510), export-then-extract showing redacted content inside the zip (INFO-186230), the count progression for the oracle (INFO-410015).
3. Module 03's enumeration artifact: two sample URLs (present/absent invite codes) + the scanner's hit rate on a sampled subset (INFO-125200); the cached response showing `Set-Cookie` (INFO-3082917).
4. Module 04's fetch proof: the bypass URL returning 200 with the feed content (INFO-1256375), the bucket-root listing (INFO-1021906), the SDK response containing PII (INFO-1575014). INFO-163476 (unverifiable S3 write) is the negative example — assertion without fetch caps the price.
5. Module 05's credential verification: recovered pixels → `aws sts get-caller-identity` output (INFO-2107680). The verification output is the price anchor for every memory read.
6. Module 06's chain or metadata honesty: demo the escalation you claim (gauth-secret → authenticator codes, INFO-1276373; sha512 proof, INFO-1087489) or label the row metadata-only (GHSL sextet) — never invent the body.

## P4 — Modern hardening fingerprints (never corpus doctrine)

The corpus maps to these modern *expectations*; a corpus-identical trigger on a modern stack usually means the hardening is absent, not that the class is dead:

- **GraphQL/API**: field-level authorization (not UI hiding — module 01's whole corpus), `PersistedQuery` allow-lists, depth/complexity limits (INFO-1085332's `first:10000` worked because no limit), private-by-default email/user fields (INFO-972355).
- **Serializers/exports**: per-field serializers (not model dumps — INFO-509924's `as_json` leaked both token forms), export-time redaction *inside* the archive (INFO-186230's residue), `.json`/`.atom` twins treated as public APIs (INFO-3000510, 1256375).
- **Privacy**: rate limits + non-differential responses on enumeration surfaces (INFO-125200's 60M space enumerated at API speed), `Vary: Cookie` / `Cache-Control: private` on session-bearing responses (INFO-3082917), consent-toggle state machines tested on every write path (INFO-472013's email-verify unset).
- **Hygiene**: dotfile denylists enforced at the *server*, not the framework (INFO-218465/219197), bucket policies default-deny with no public listing (INFO-1021906/1102546), log redaction for tokens (INFO-2915647's `live.log`, INFO-2101165's debug passwords), secret scanning on shipped apps/repos (INFO-124100's Podfile, INFO-351555's Cloudinary).
- **Memory/protocol**: patched image coders + sandboxed conversion (INFO-2107680's own mitigation advice: "moving image preview generation to an isolated environment"), HTTP/3 MTU-aware worker isolation (INFO-2599391), `sscanf == 2`-class strict parsing (INFO-1176461), PASV-address allow-listing (INFO-1145454).
- **Telemetry**: analytics/reporting URL filters checked on *every* sink (INFO-1491127/301526: invite links leaking to `google-analytics.com`/`bat.bing.com` — the filter exists, the coverage doesn't).

## P5 — Pre-report gates (kill-gates)

1. **Class gate** — you can name the disclosure primitive (field / serializer / oracle / enumeration / cache / path / memory) and *whose* data it is. "Information disclosure" without a data class dies here (module 06's benign-content $100 is the ceiling for "something leaked").
2. **Value gate** — you show the value, not the capability: the JSON blob, the count delta, the feed body, the verified credential output. Theory rows ("might disclose", "could be enumerated") die here (module 04's INFO-163476; module 01's unpriced INFO-489146 despite its catastrophic field list).
3. **Other-tenant gate** — state whether the data is the reporter's own, another user's, another project's, or another tenant's. The corpus prices them in that order ascending; a report that omits the tenant boundary misprices itself.
4. **Metadata gate** — GHSL-style one-liners, CVE-ledger rows, and metadata-only bodies are anchors, not evidence (module 05 §3, module 06 §3). They get *attributed* to their modules but are never cited as proof in any report you write.
5. **Version/patch gate** — outdated-CVE claims need your own fetch demo or die (module 05's pattern: INFO-2107680 proved liveness with `aws sts`; INFO-1176461 shipped the hex dump and the fix).
6. **Noise gate** — the "it's not disclosure"-check against module 06's gallery: joke/wordlist rows (INFO-2733994), content-free probe pages (INFO-53004's $100), and policy complaints. The mirror carries `.htpasswd`-class floor findings — the noise floor exists at every program, and the floor price is $100.

## Module ↔ phase table

| Phase | Corpus evidence (modules) | Anatomy of the paid pattern |
|---|---|---|
| P1 inventories fields/serializers/exports | 01 (§2–§4), 02 (§2–§3), 04 (§2–§4) | GraphQL diff, `.json` twins, export zips, feeds |
| P2 probes oracle/differential/enumeration | 01 §2, 02 §4, 03 §2, 04 §3-§4, 05 §2, 06 §4 | field oracle → count → search oracle → order walk → cache sweep |
| P3 proofs show the value | 01 §2, 02 §2–§3, 03 §2, 04 §2, 05 §2 | JSON blob, zip extract, sts output, bucket listing |
| P4 hardening fingerprints | 01 §6, 02 §6, 03 §6, 04 §6, 05 §6, 06 §6 | field auth, serializer allow-lists, Vary/Cache-Control, log redaction |
| P5 kill-gates | 06 (§2–§6), 04 §5, 05 §3 | benign $100, metadata sextet, ledger rows, capability-vs-value |

## Non-goals

- Memory-corruption *exploitation* (write primitives, heap feng shui): the corpus pays *reads*; exploitation technique belongs to the `../30_Memory-Corruption/` vault (upcoming).
- The full GraphQL/field-auth technique catalog (introspection craft, pagination abuse): the technique shelf is `../22_GraphQL/` (upcoming); this vault prices the fields, never the fuzzing.
- Disclosure *response* play (takedown, rotation, notification): the corpus proves *leakage*, and rotation advice (e.g., INFO-2915647's "Revoke the Token") is quoted as corpus text, not doctrine.
