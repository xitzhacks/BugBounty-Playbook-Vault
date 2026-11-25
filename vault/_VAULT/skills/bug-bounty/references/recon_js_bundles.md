---
name: recon_js_bundles
description: Decode gzip/brotli-compressed SPA JS bundles before grepping; passively confirm WordPress core version (the ?ver= trap + asset-hash comparison); wp2shell/CVE-2026-63030 version-range guard.
---

# Recon: Compressed JS Bundles & Passive WP Version

## 1. SPA JS bundles are compressed — decode before grep

Angular/React/Vue SPAs served from a CDN (CloudFront, etc.) usually return
minified bundles as **gzip or brotli**. `curl ... | grep` finds nothing because
the file is binary (gzip magic `\x1f\x8b`). Symptom: a ~7KB `index.js` that, when
grepped, yields zero endpoint/secret hits — it's a bootstrapper, and the real
code is in gzip'd vendor chunks.

Recipe:
```bash
curl -s "https://cdn.example.com/index-abc123.js" -o bundle.js
gunzip -t bundle.js && echo "gzip"          # probe; brotli has no -t, use file/magic
gunzip -c bundle.js > bundle.dec.js          # decode (keep original)
brotli -d -c bundle.js > bundle.dec.js 2>/dev/null   # brotli variant
cat bundle.dec.js | grep -oiE '(/api/[a-zA-Z0-9_./-]+|https?://[a-z0-9.-]*example[a-z0-9./_-]*)' | sort -u
```
Then grep decoded bundles for: `api|endpoint|baseURL|Authorization|Bearer|token|
oauth|client_id|redirect_uri`. Also hunt a CDN config json (`assets/config.json`,
`assets/environments/environment.json`) — often 403.

If the app lazy-loads (Angular `loadChildren`), the login page may only reference
framework chunks. The business-logic chunk isn't on the login HTML; mine archived
URLs (waybackurls/gau, the 139k-URL set) for real API paths instead of relying on
the single page's bundle list.

## 2. Passive WordPress core version confirmation

Generator tags, `readme.html` version, and `wp-includes/version.php` are commonly
stripped or 403'd on hardened WP. **Do NOT conclude a version from a random
`?ver=` on an asset** — that is frequently a plugin or **jQuery** build number, not
core. (Real case: `wp-includes/js/wp-tooltip.js?ver=7.1` was jQuery v3.7.1, NOT
WordPress 7.1.)

Reliable passive oracles:
- `?ver=` on **core** assets only: `wp-admin/css/common.css`, `wp-embed.min.js`,
  `wp-includes/js/jquery/jquery.js` (these map to the WP release build).
- RSS/Atom/RDF feed `<generator>` tag (often stripped too).
- REST root `wp-json/` namespaces — not a version, but confirms `/batch/v1`
  presence (the CVE-2026-63030 attack surface).
- `wp-json/wp/v2/users` often leaks a user object (id + slug) = user enum (usually
  low value / N/A per most programs' out-of-scope rules).

**Authoritative method — asset hash comparison:**
```bash
curl -s "https://target/wp-includes/js/wp-embed.min.js" -o t.js
md5sum t.js
for v in 6.9.4 6.9.5 7.0.1 7.0.2; do
  curl -sL "https://wordpress.org/wordpress-$v.tar.gz" -o wp-$v.tar.gz
  mkdir -p /tmp/cmp_$v && tar xzf wp-$v.tar.gz -C /tmp/cmp_$v
  echo "$v $(md5sum /tmp/cmp_$v/wordpress/wp-includes/js/wp-embed.min.js | awk '{print $1}')"
done
# matching md5 => exact core version
```
Note: the user may block the release download (OPSEC/caution). Respect it; without\nthe version you CANNOT claim a version-specific CVE.\n\n## Cross-reference: Akamai bypass + sitemap enumeration\nWhen Akamai/CDN blocks all terminal curl requests (403 Access Denied), use browser\nautomation (browser_navigate) to access sitemaps and RSS feeds. See\n`references/akamai_bypass_and_sitemap_enum.md` for the full technique.

## 3. Methodology guard — no CVE claim without version

A WP target with `/batch/v1` REST endpoint present is the **surface** for
CVE-2026-63030 (wp2shell, pre-auth RCE chain). The endpoint existing does NOT mean
the core is vulnerable. Affected ranges:
- RCE chain (CVE-2026-63030 + companion CVE-2026-60137): WP **6.9.0–6.9.4** and
  **7.0.0–7.0.1**.
- SQLi-only (CVE-2026-60137): WP **6.8.0–6.8.5** (not the full RCE chain).
- 7.1 Beta 1 vulnerable; Beta 2+ fixed. < 6.8 not affected.

Per bug-bounty discipline (NO theoretical bugs): confirm the exact core version via
§2 BEFORE reporting. **Never drop a test shell on prod just to learn the version** —
it violates the no-data-loss rule and isn't needed for a responsibly-disclosed
critical. Report "version unconfirmed, needs auth/hash comparison" as a lead, not a
finding.
