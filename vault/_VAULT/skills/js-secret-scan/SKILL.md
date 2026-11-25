---
name: js-secret-scan
description: >-
  Scan a directory of JavaScript files (minified frontend bundles, extracted
  .js assets, leaked bundles) for hardcoded secrets, API keys, tokens, private
  keys, and credentials. Includes a ready-run scanner script plus a
  bug-bounty-specific false-positive triage playbook so you don't waste time
  on alphabet tables and localStorage key NAMES that masquerade as secrets.
---

# SKILL: JS Secret Scanning (with Frontend False-Positive Triage)

> Use when you have a folder of `.js` files — typically minified frontend
> bundles pulled from a target during recon — and need to find hardcoded
> secrets fast, WITHOUT drowning in false positives.

## 1. WHY THIS SKILL EXISTS

Running `grep`/`trufflehog` over minified frontend bundles produces huge
amounts of noise: DRM key-system UUIDs, base64 alphabet tables, UI label
strings, localStorage/config key *names* (e.g. `"abm_token"`), and public
CDN identifiers all match naive "key/secret/password" regexes. This skill
ships a tuned scanner + a triage checklist that compresses that noise down to
real findings.

**Core principle:** frontend JS is, by definition, PUBLIC. Anything found in
it is exposed to every visitor. So a "hit" is only reportable if it is a
*protected* secret (private key, live/secret API key, session token,
password) — NOT a public client ID, public token, or config key name.

## 2. WORKFLOW

```
1. Inventory the JS dir (count files, sizes, total bytes)
2. Run the scanner (scripts/scan_secrets.py) -> JSON + console report
3. Triage every HIGH-SIGNAL hit manually (rules in §4)
4. For each real candidate: extract surrounding context (±120 chars)
5. Classify: REAL SECRET / PUBLIC-BY-DESIGN / FALSE POSITIVE
6. Report only REAL SECRETS; note borderline items as Informational
```

## 2b. ANTI-PATTERN: gzip-compressed bundles (FALSE-NEGATIVE trap)

Modern SPAs (React/Vue/Next) are often served gzip-compressed. `curl`
WITHOUT `--compressed` saves the RAW gzip bytes; the bundle then starts with
the gzip magic `\x1f\x8b` (binary). A text-mode `open()` + regex scan reads
binary garbage and returns **NOTHING** — a falsely "clean" report. This burned
a live winticket.jp SPA: all 28 bundles were gzip, the first scan said "No
potential secrets found", and only `gunzip` revealed the (still non-secret)
Firebase error-code / alphabet-table content.

**Fix:** decompress before scanning. `scan_secrets.py` now auto-detects the
gzip magic and gunzips inline. If hand-scanning:
```bash
for f in js_files/*.js; do
  if [ "$(head -c2 "$f" | xxd -p | head -c4)" = "1f8b" ]; then
    mv "$f" "$f.gz" && gunzip -f "$f.gz"; fi
done
```
Symptom you hit this trap: scanner reports "No potential secrets" but
`head -c 300` shows `\x1f\x8b` / non-text bytes, OR the file is 5-10x
smaller than a real 100KB+ minified bundle should be.

## 3. THE SCANNER

`scripts/scan_secrets.py` (bundled with this skill) does:

- **Auto-decompresses gzip'd bundles** (§2b trap): detects `\x1f\x8b`
  magic and gunzips inline, so CDN-served `--compressed` JS is never
  scanned as binary garbage.
- ~60 known-format secret regexes (AWS, GCP, Stripe, GitHub, GitLab, Slack,
  Discord, Telegram, JWT, private-key blocks, DB connection strings, OpenAI,
  Anthropic, HuggingFace, Sentry, Azure, Square, Shopify, etc.)
- Context-based assignment scan: `key|token|secret|password|... = <value>`
  catches custom-named secrets the format regexes miss.
- Shannon-entropy scan for high-entropy standalone strings (length ≥ 20,
  entropy ≥ 4.5, excludes pure-hex md5/sha to cut false positives).
- Writes full machine-readable results to `secret_scan_results.json`.

Run it:

```bash
python3 scripts/scan_secrets.py
# edit JS_DIR at top of script, or pass the dir as first arg if you add that
```

Then ALWAYS manually verify the high-signal matches — the scanner is a
lead generator, not a verdict engine.

## 4. FALSE-POSITIVE TRIAGE RULES (frontend JS)

When a hit looks like a secret, check it against these before celebrating:

| Looks like | Usually is | Why |
|---|---|---|
| `discord token` regex match | Anti-bot interstitial (Cloudflare "Just a moment...") | Strings in challenge pages coincidentally match |
| `<digits>:<35-char-base64url>` that matches the Telegram bot-token regex, found in `cdn-cgi/challenge-platform/<h>/b/scripts/jsd/<hash>/main.js` | **Cloudflare challenge-platform path token** | It sits inside a CF-obfuscated `/jsd/oneshot/<rand>:<id>:<token>/` URL. The identical string was served on two unrelated hosts (`www` and `remoteaccess`) of the same target = platform constant, not a bot token. |
| "Credit Card (loose)" = 16-digit number inside `https://<32hex>@o<digits>.ingest.<region>.sentry.io/<project_id>` | **Sentry DSN** (public key + project id) | DSNs are public by design — the SDK ships them in every frontend bundle. Never reportable. |
| `dummyClientSecret` / `dummyClientId` literals | Public OAuth client placeholder (Intershop PWA, SAP Spartacus, other public-client SPAs) | The name says dummy and it carries no value; these storefronts are public clients using PKCE, so there is no confidential secret to leak. |
| `clientToken: "pub...."` | Datadog/analytics PUBLIC client token | `pub` prefix = embedded in every frontend by design |
| 64-hex next to an S3/API URL | Public client/app identifier | Hardcoded in public bundle = not protected |
| `edef8ba9-...`, `94ce86fb-...` | DRM key-system UUIDs (Widevine/FairPlay) | Public DRM spec constants |
| `password: "[REDACTED_SECRET]"` | UI label / i18n string | Japanese/translated text, not a value |
| `password: ""` or `password=[REDACTED_SECRET] | Empty / variable read | Never a literal |
| `key: "abm_token"`, `ACCESS_TOKEN: "[REDACTED_SECRET]"` | localStorage/config key NAME or endpoint PATH | Names, not values |
| `ABCDEFGHIJKLMNOPQRSTUVWXYZ...` | Base64/base58 alphabet tables | Crypto lib constants |
| `123456789ABCDEFGHJKLMNPQRSTUVWXYZ...` | Base58 alphabet (Bitcoin/etc.) | Lib constant |
| `Bearer <...>` literal | Rare in legit bundles | If present, HIGH priority — verify |

**Verify a hit with context extraction:**

```bash
cd js_files
# 120 chars either side of the matched string
grep -roE '.{120}THE_MATCHED_STRING.{120}' FILE.js | head -3
```

**Confirm a "Discord/Slack token" isn't a Cloudflare page:**

```bash
head -c 300 FILE.js   # look for <!DOCTYPE html> "Just a moment"
```

**Confirm a hex string is a real secret vs an identifier:**

```bash
grep -roE '.{100}THE_HEX.{60}' *.js | head
# If it sits next to a public URL (api-*.bucketeer.jp, *.abema.tv) -> public ID
```

**Worked false-positive case study (AbemaTV bundle, 52 minified files):**
the raw scanner flagged 168 "suspicious" hits in the largest file; EVERY
high-signal hit was a false positive. The triage that produced a credible
"no real secret" verdict:

| Scanner flag | Actually was | How cleared |
|---|---|---|
| `Discord Bot Token` regex | Cloudflare "Just a moment..." anti-bot HTML challenge | `head -c 300 file.js` -> `<!DOCTYPE html>` |
| `clientToken: "pub..."` | Datadog RUM *public* client token (`pub` = public by design) | `pub` prefix |
| 64-hex next to `api-*.bucketeer.jp` | Public client/app identifier (S3 pairing) | context beside public URL |
| `edef8ba9-...`, `94ce86fb-...` | DRM key-system UUIDs (Widevine/FairPlay, public spec) | known DRM constants |
| `password:"[REDACTED_SECRET]"` | UI/i18n label ("issue one-time password") | translated text, not a value |
| `password:""` / `password=[REDACTED_SECRET] | Empty / variable read | never a literal |
| `key:"abm_token"`, `ACCESS_TOKEN:"[REDACTED_SECRET]"` | localStorage/config key NAME or endpoint PATH | names, not values |
| `ABCDEFGHIJKLMNOPQRSTUVWXYZ...` | Base64/base58 alphabet tables (crypto lib) | library constants |

Lesson: the scanner is a LEAD GENERATOR, not a verdict engine. For every
high-signal hit, extract ±120 chars context, classify REAL SECRET /
PUBLIC-BY-DESIGN / FALSE POSITIVE, and NOTE the false-positive reasoning.
That discipline is what makes a "no findings" report credible instead of lazy.

## 5. WHAT COUNTS AS REPORTABLE (bug bounty)

- Private key blocks (`-----BEGIN ... PRIVATE KEY-----`)
- Live/secret API keys (Stripe `sk_live_`, AWS secret, GitHub `ghp_/gho_`,
  OpenAI `sk-`, etc.) — NOT publishable/test keys
- Session/access tokens with real entropy that grant auth
- Passwords assigned as literal values
- DB credentials / connection strings with embedded creds
- JWTs signed with a hardcoded secret (the secret, not the token, is the find)

Borderline (report as Informational / depends on program scope):
- Hardcoded public client identifiers in frontend (S3 bucket names, app IDs)
- Analytics public tokens (Datadog `pub...`, Google Maps, etc.)

NOT reportable:
- Anything "public by design" (see triage table)
- Config key names, endpoint paths, UI strings, DRM constants, alphabet tables

## 6. NEXT STEPS AFTER SCAN

Frontend bundles rarely yield leaked secrets but ALWAYS yield attack-surface
intel. After the secret scan, pivot to endpoint/path extraction for recon:

```bash
# API routes / paths from all bundles
grep -rhoE '"/[a-zA-Z0-9/_.-]+"|/api/[a-zA-Z0-9/_.-]+' *.js | sort -u > endpoints.txt
# Auth-related endpoints worth testing
grep -iE 'oauth|token|login|password|2fa|device' endpoints.txt
```

## 7. ANTI-PATTERN

Do NOT report "found a secret" off a raw regex match. Always (1) open the
context, (2) classify per §4/§5, (3) note the false-positive reasoning when
you clear a hit. This is what separates a credible researcher from noise in a
program's triage queue.
