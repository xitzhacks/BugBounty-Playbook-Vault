# APK provenance + config/WebView audit — condensed recipe

## 1. Provenance check (genuine vs repack) — do this BEFORE any mobile report

A mirror-sourced APK (APKCombo/APKMirror/APKPure) must be proven the genuine vendor build.
Programs reject findings from non-canonical/repackaged binaries.

Steps:
1. Note the download source. If `APKComboInstaller.url` or similar points to a third-party
   mirror, treat as "unverified provenance" until crossed.
2. Google Play: `play.google.com/store/apps/details?id=<pkg>` → confirm package + publisher.
3. APKMirror/APKCombo: confirm SAME versionCode/versionName for that package, published by vendor.
   (Mirrors re-host the UNMODIFIED Play-signed APK; they cannot re-sign without breaking the
   Play update chain → mirror signer cert == official cert.)
4. Extract signer cert from the APK Signing Block:
   `python3 scripts/extract_signer_cert.py <base.apk>`
   - `CN=Android Debug` → debug build, flag.
   - Self-signed corp cert (e.g. `O=nhn`) → plausible enterprise/side-load; confirm against the
     app's own package namespace (`com.navercorp.*` → NAVER/NHN lineage).
5. Record the SHA-256 fingerprint in the report's provenance section so the triager can confirm.

## 2. F1 class — network_security_config cleartext + user-CA trust + no pinning

From the decoded `res/xml/network_security_config.xml` (apktool) or `aapt dump xmltree`:
- `<base-config cleartextTrafficPermitted="true"/>` → global cleartext (no domain-config scoping).
- `<debug-overrides><trust-anchors><certificates src="user"/></trust-anchors></debug-overrides>`
  → user CAs trusted in release build → silent TLS interception with Burp/mitmproxy user CA.
- No `<pin-set>` → no cert pinning.

Report structure (F1):
- Summary: global cleartext + user-CA trust + no pinning.
- PoC: re-runnable script that extracts + prints the config (proves it from the binary).
- Dynamic PoC: install user CA on emulator/rooted device, set proxy, launch app, observe
  decrypted traffic in proxy with no cert error.
- Impact: auth tokens / session cookies / mail-board-drive content interceptable by rogue Wi-Fi,
  MITM, or rooted-device-with-user-CA. No exploitation of users (local interception of own install).
- Severity: Medium (conditional on attacker network position) unless chained with data-exposure.
- CWE-319 / CWE-295; OWASP M3.

## 3. WebView JS-bridge origin-check audit (highest-value class)

1. `grep -rln 'addJavascriptInterface' dec/` → list every bridge.
2. For each, find the owning WebView and its `shouldOverrideUrlLoading`:
   ```bash
   grep -rln 'shouldOverrideUrlLoading' dec/ | while read f; do
     echo "== $f =="; grep -E 'shouldOverrideUrlLoading|addJavascriptInterface|setAllow(File|Content)Access|setJavaScriptEnabled' "$f"; done
   ```
3. Flag bridges where `shouldOverrideUrlLoading` returns false for any http(s) URL (no host
   allowlist) AND the WebView loads attacker-controllable content (deep links, mail/board bodies,
   miniapp web). Combos to watch: `setAllowFileAccess`/`setAllowContentAccess` + JS + bridge.
4. Count "bridges with no origin check" vs "bridges with host validation" to size the surface.
5. Chain with F1: cleartext/no-pinning makes bridge traffic interceptable.

## Retraction discipline (mobile)
If a key/secret "hit" turns out to be a placeholder (literal `...` in the middle, or Google
returns `REQUEST_DENIED / API key is invalid`), RETRACT — do not file. Document the retraction
in the report appendix (see `triage-validation` RETRACTION DISCIPLINE). HTTP 200 ≠ success; read
the provider's body status field.
