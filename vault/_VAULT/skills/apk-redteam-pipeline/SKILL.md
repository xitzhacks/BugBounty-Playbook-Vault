---
name: apk-redteam-pipeline
description: End-to-end Android APK red-team pipeline — automated APK acquisition (Play Store + apkpure + apkmirror fallback), jadx decompilation, secret/URL/JWT/Firebase grep, pinned-cert extraction, exported-component enumeration, Frida runtime instrumentation templates, intent-injection probes. Built from an authorized external red-team engagement where 7 APKs were pulled manually, 4 download attempts truncated, and a hardcoded JWT + 30 internal API endpoints were recovered from one of the apps. Use when target has a mobile app catalogue (Play Store developer page), when you find an APK URL hosted on a web server, or when post-recon mentions "mobile app" in scope.
sources: authorized-engagement
report_count: 1
---

## When to use this skill

Trigger when:
- Recon surfaces 1+ mobile apps under the target's developer name (Play Store dev page)
- A web app hosts `*.apk` files directly (e.g. `Recruitz.apk` found on a subdomain during one engagement)
- APK package IDs leaked via stealer logs (e.g. `com.<brand>.app`, `com.<brand>.<sub-brand>` patterns in stealer dump format)
- Customer-facing app, dealer/partner portal, or employee mobile companion app is in scope
- Bug bounty program lists Android in scope

DO NOT use for:
- iOS-only targets (different pipeline — IPA reverse, MobSF, frida-ios-dump)
- React Native / Flutter web apps already covered by JS bundle analysis
- Server-side only assessments

---

## Stage 0 — Inventory all org-owned apps

### Play Store developer-page scrape
```bash
# Find developer page from the target's brand name
curl -sk -A "Mozilla/5.0" "https://play.google.com/store/apps/developer?id=<Brand+Name>" -o /tmp/dev.html

# Extract package IDs
grep -oE 'id=[a-zA-Z0-9._]+' /tmp/dev.html | sort -u
```

Example output (anonymized — 7 packages typical for a multi-brand conglomerate):
```
com.events.<brand>build
com.<corp>.<sub-brand-1>
com.<corp>.<sub-brand-2>
com.<corp>.<flagship>
com.<corp>.<product-line-1>
com.<corp>.<product-line-2>
com.<corp>.<sub-brand-3>
```

### Cross-reference with stealer logs
Stealer-log format includes package names like `*@com.<corp>.<app>` — extract these from `creds_userpass.txt` if you have a leaked dump.

### Brand permutation guesses (multi-brand conglomerate patterns)
```
com.<brand>.app
com.<brand>.mobile  
com.<brand>.android
com.<brand>connect.app
in.<brand>.dealer
in.co.<brand>.app
```

---

## Stage 0.5 — CONFIRM THE EXACT TARGET (do this BEFORE any analysis)

PITFALL (real session): User said "analyze the APK in the android folder" but the session had
prior-target APKs (different org) sitting in ~/Bugbounty. The agent analyzed the WRONG org's
APKs for two full turns before the user corrected: "we are working on Linework not ather."
This wastes turns and produces findings for the wrong scope.

RULE: Before decompiling anything, print the exact path + package + version you are about to
analyze and confirm it matches what the user named. If multiple APKs exist under ~/Bugbounty,
ASK which target, or grep the user's stated target folder explicitly — never assume the
most-recently-touched APK is the intended one. Also confirm the FILE EXTENSION (see XAPK below).

## Stage 1 — APK acquisition

### Primary: APKPure direct (no auth required)
```bash
# Follow 302 redirects to actual download
curl -sk -L --max-time 60 \
  "https://d.apkpure.net/b/APK/<package_id>?version=latest" \
  -o "<package_id>.apk"

# Or via the legacy d-XX.winudf.com mirror chain (we saw this work)
```

### Secondary: APKMirror search
```bash
curl -sk -A "Mozilla/5.0" "https://www.apkmirror.com/?post_type=app_release&searchtype=apk&s=<brand>" \
  | grep -oE 'href="[^"]+\.apk[^"]*"' | sort -u
```

### Tertiary: APKPure web search
```bash
curl -sk "https://apkpure.com/search?q=<brand>" | grep -oE 'data-dt-app="[^"]+"'
```

### XAPK vs APK  (GLOBBING PITFALL — see below)
- `.xapk` = a zip containing multiple split APKs (base + config.armeabi-v7a + config.en + etc.)
  PLUS a top-level `manifest.json` (package_name, version_name/code, min_sdk, target_sdk,
  permissions list, split_apks[]). This `manifest.json` is the fastest way to get package +
  version + permission surface WITHOUT touching the DEX.
- FILE EXTENSION GOTCHA: `*.apk` glob / `find -iname '*.apk'` will NOT match a `.xapk` file.
  If the user says "the APK in the android folder" and your `*.apk` search returns nothing,
  search case-insensitively for `*.xapk` and `*.apks` too. (Real session: target was
  `linework.xapk` — a 271MB XAPK — and the `*.apk` glob missed it entirely.)

```bash
# Outer XAPK is just a zip — extract it
7z x -y linework.xapk -oextracted/          # lenient, handles truncation
cat extracted/manifest.json                 # -> package, version, permissions, splits

# The REAL app is the base APK inside (often named <package>.apk or base.apk)
BASE=extracted/com.gworks.oneapp.works.apk  # 171MB base; splits are config.*.apk
file "$BASE"                                 # "Zip archive data" = APK

# Decode manifest + config from the BASE apk
apktool d -f -o dec/apktool "$BASE"
aapt dump badging "$BASE" | grep -E "package:|minSdk|targetSdk"
aapt dump xmltree "$BASE" res/xml/network_security_config.xml 2>/dev/null

# Decompile the BASE apk (splits add resources only; base holds the DEX/logic)
jadx -j 4 -d dec/jadx "$BASE"
```

NOTE: `7z x` on the base .apk for resource/cert pulls is reliable; `unzip` can choke on
APK padding. For 150MB+ base APKs, jadx may take several minutes — run in background
(`terminal background=true notify_on_complete=true`) and poll, don't block the turn.

---

## Stage 2 — DEX decompilation (jadx)

```bash
# Install
brew install jadx          # macOS
# or
wget https://github.com/skylot/jadx/releases/latest/download/jadx-1.5.x.zip

# Decompile
jadx -d decompiled_<package>/ <package>.apk

# For XAPK that contains multiple APKs
for inner in extracted_<package>/*.apk; do
  jadx -d decompiled_<package>_$(basename "$inner" .apk)/ "$inner"
done
```

For a fast "strings only" pass without full decompilation:
```bash
find extracted_<package> -name "classes*.dex" -exec strings -8 {} \; > strings_<package>.txt
```

---

## Stage 3 — Secret grep (the 60-pattern catalog)

```bash
# URL grep — owned-domain references
grep -oE 'https?://[a-zA-Z0-9.-]+\.(target1|target2|target3)\.(com|io|net|in)[a-zA-Z0-9./_?=&%-]*' strings_<package>.txt | sort -u

# Internal IP / port URLs
grep -oE 'https?://(10\.|172\.(1[6-9]|2[0-9]|3[01])\.|192\.168\.|127\.)[0-9.]+(:[0-9]+)?[a-zA-Z0-9./_?=&-]*' strings_<package>.txt

# Cloud credentials
grep -oE 'AKIA[A-Z0-9]{16}'                            # AWS Access Key
grep -oE 'aws_secret_access_key[\s:=]+[A-Za-z0-9/+=]{40}' # AWS Secret
grep -oE 'AIza[A-Za-z0-9_-]{35}'                       # Google API key
grep -oE 'ya29\.[A-Za-z0-9_-]+'                        # Google OAuth refresh token
grep -oE 'gh[ps]_[A-Za-z0-9]{36}'                      # GitHub PAT
grep -oE 'glpat-[A-Za-z0-9_-]{20}'                     # GitLab PAT
grep -oE 'xox[pbar]-[A-Za-z0-9-]+'                     # Slack token
grep -oE 'sk-[A-Za-z0-9]{48}'                          # OpenAI API key
grep -oE 'sk-ant-[A-Za-z0-9_-]{90,}'                   # Anthropic API key
grep -oE 'AC[a-f0-9]{32}'                              # Twilio Account SID
grep -oE 'sk_live_[A-Za-z0-9]{24}'                     # Stripe live key
grep -oE 'pk_live_[A-Za-z0-9]{24}'                     # Stripe publishable
grep -oE 'mailgun-[A-Za-z0-9-]{40}'                    # Mailgun
grep -oE 'SG\.[A-Za-z0-9_-]{22}\.[A-Za-z0-9_-]{43}'    # SendGrid

# JWT (any algorithm)
grep -oE 'eyJ[A-Za-z0-9_-]+\.eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]*' strings_<package>.txt

# Firebase
grep -oE '"(api_key|project_id|database_url|storage_bucket|client_id|mobilesdk_app_id|google_app_id|gcm_defaultSenderId)"\s*:\s*"[^"]+"' \
  extracted_<package>/res/values/strings.xml \
  extracted_<package>/google-services.json \
  decompiled_<package>/resources/AndroidManifest.xml 2>/dev/null

# OAuth client secrets
grep -oE 'client_secret["\s:=]+[A-Za-z0-9_-]{24,}' strings_<package>.txt

# Hardcoded passwords (heuristic — many false positives, manual review)
grep -oE '"password"\s*:\s*"[^"]+"|password\s*=\s*"[^"]+"' decompiled_<package>/sources/**/*.java 2>/dev/null
```

### Real-world example finding (anonymized — from an authorized engagement)
```
# Customer-facing APK shipped a hardcoded URL of this shape:
https://api.<client>.example/<path-token>/<resource-token>?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.<payload>.<sig>

# Decoded JWT payload: {"sid":<int>,"iat":<unix-ts>,"exp":<unix-ts>}
# Expired ~8 years earlier — but path tokens + 30 /v1/* endpoints still useful intel
```

---

## Stage 4 — Pinned certificate extraction

```bash
# Find .cer / .der / .pem files in assets/
find extracted_<package>/assets -iname "*.cer" -o -iname "*.der" -o -iname "*.pem" -o -iname "*.crt" 2>/dev/null

# Or in network_security_config.xml
find extracted_<package> -name "network_security_config.xml" -exec cat {} \;

# For each cert, extract subject + SAN (might reveal new internal API hosts)
for cert in $(find extracted_<package>/assets -iname "*.cer"); do
  echo "=== $cert ==="
  openssl x509 -in "$cert" -noout -subject -issuer -dates 2>/dev/null
  openssl x509 -in "$cert" -noout -text 2>/dev/null | grep -E 'Subject:|DNS:|Issuer:|Validity'
done
```

### Real-world example
A customer-facing APK from an authorized engagement contained `assets/api_<service>_<domain>_com.cer` — revealed the existence of an `api.<service>.<domain>.example` asset that had NOT surfaced in passive recon.

---

## Stage 4.5 — Signer-cert / PROVENANCE verification (anti-repak check)

PITFALL (real session): The analyzed XAPK carried an `APKComboInstaller.url` pointing to
`apkcombo.com` — a third-party mirror. Before reporting, we had to PROVE the artifact is the
genuine vendor build, not a repackaged/mirror-modified copy (programs reject findings from a
non-canonical APK). The APK was V2/V3-signed, so `keytool -printcert -jarfile` and a
`META-INF/*.RSA` extract returned NOTHING — V2/V3 signatures live in the **APK Signing Block**,
not a standalone `.RSA` file.

RULE: For any APK pulled from a mirror (APKCombo/APKMirror/APKPure), extract the signer cert from
the signing block and confirm it matches the official publisher. Three corroboration crosses:
1. Google Play listing `play.google.com/store/apps/details?id=<pkg>` → package + publisher.
2. APKMirror/APKCombo list the SAME versionCode/versionName for that package, published by the
   vendor. (Mirrors re-host the UNMODIFIED Play-signed APK — they can't re-sign without breaking
   the Play update chain, so a mirror copy's signer cert == the official cert.)
3. Extracted signer cert subject/issuer + SHA-256 fingerprint.

Red flags: `CN=Android Debug` → debug build, not release (flag it). A self-signed corp cert
(e.g. `O=nhn, CN=sungho park`) is plausible for enterprise/side-load channels — confirm it's
consistent with the app's own package namespace (e.g. `com.navercorp.*` → NAVER/NHN lineage).

```bash
# Extract signer cert(s) from APK Signing Block -> openssl-readable DER
python3 scripts/extract_signer_cert.py <base.apk>
# prints subject/issuer/validity/SHA-256 for each signer cert
```

Cross-ref: `triage-validation` Q3 (root cause in in-scope asset) → add a provenance sub-check:
"is this the GENUINE binary?" before writing any mobile-static report. A finding proved only on a
repack is rejectable. See `references/apk_provenance_and_config_audit.md`.

## Stage 4.6 — network_security_config + WebView bridge AUDIT (highest-value mobile classes)

Two finding classes surfaced as the highest-value in a real LINE WORKS audit:

### (a) Cleartext + user-CA trust + missing pinning (F1 class)
`network_security_config.xml`:
- `<base-config cleartextTrafficPermitted="true" />` → applies GLOBALLY (no `domain-config`
  scoping) → any `http://` call is MITM-able.
- `<debug-overrides><trust-anchors><certificates src="user"/></trust-anchors></debug-overrides>`
  → user-installed CAs (Burp/mitmproxy) are trusted in the release build → silent TLS
  interception on a rooted/emulator device.
- Absence of `<pin-set>` → no cert pinning to block the above.
Combine: an on-device proxy with a user CA decrypts ALL traffic with no cert error. Report with a
re-runnable PoC that extracts + prints the config. Severity typically Medium (conditional on
attacker network position) unless chained with a data-exposure bug.

### (b) Un-origin-checked WebView JS bridges (highest-value; matches Ather GRID F2 pattern)
Grep for `addJavascriptInterface` across smali/jadx. For each bridge, check:
- Is `shouldOverrideUrlLoading` implemented, and does it enforce a host/origin allowlist?
  ```bash
  grep -rln 'shouldOverrideUrlLoading' dec/ | while read f; do
    echo "== $f =="; grep -E 'shouldOverrideUrlLoading|addJavascriptInterface' "$f"; done
  ```
- WebViews that load attacker-controllable content (deep links, mail/board message bodies,
  miniapp web content) WITH a live bridge + no origin check = JS-injection → native-method reach.
- `CoreWebView` / miniapp `Bridge` / mail-viewer WebView are prime suspects.
- Check `setAllowFileAccess` / `setAllowContentAccess` / `setJavaScriptEnabled` on the same
  WebView — file:// + content:// + JS + bridge is the dangerous combo.
Count "bridges with no origin check" vs "bridges with host validation" to scope the surface.
This class chains with (a): cleartext/no-pinning makes the bridge traffic interceptable.

See `references/apk_provenance_and_config_audit.md` for the F1 report structure + reproduction recipe.

## Stage 4.7 — Reconstruct the REAL backend API base URL + path from Retrofit/smali

Recon often surfaces a host (e.g. `cxtalk-service.line-works.com`) that resolves DNS and returns a
uniform error on EVERY path. That is frequently a STALE / DECOY name. The live API the app actually
calls is usually reconstructable from the DEX — do this BEFORE blind-fuzzing the decoy host.

### Step 1 — find the Retrofit interface + relative endpoint path
Grep smali/jadx for the `@GET`/`@POST` annotation (after r8 obfuscation it appears as
`.annotation runtime Lx50/f;` with `value = "relative/path"`):
```bash
grep -rn 'value = "home/widget' dec/
grep -rn 'Lx50/f;' dec/ | grep -iE 'value = "[a-z]'   # Retrofit @GET/@POST annotation body
```
This yields the endpoint path, e.g. `home/widget/023/small` (a `Home*Api` interface). Sibling
endpoints in the same package often share a SEQUENTIAL ID space (`021`, `022`, `023`...) — that is
a built-in enumeration / IDOR surface to test once authed.

### Step 2 — trace the Dagger @Provides builder to the base-URL class
The Retrofit interface is instantiated in a Dagger module method (e.g. `yn/c.smali` method `b`):
```smali
sget-object p1, Lcom/gworks/config/url/AliceServerUrl;->DEFAULT:L...;
invoke-virtual {p1}, ...->f()Ljava/lang/String;          # returns the base URL
invoke-virtual {p0, p1}, ...->f(Ljava/lang/String;)      # appends a segment e.g. "webhomegw"
```
So the full request path = `<BASE from AliceServerUrl.DEFAULT>` + `/webhomegw` + `/home/widget/023/small`.

### Step 3 — read the base-URL builder class
Open the builder (e.g. `com/gworks/config/url/AliceServerUrl$c.smali`). The method builds a
StringBuilder: `"https://alice." + <baseDomain>` (prod), `"https://alpha-alice."` (alpha),
`"https://stage-alice."` (stage). The real base host is `alice.<baseDomain>`.

### Step 4 — recognize PER-TENANT hosts (out of anonymous reach)
`<baseDomain>` is the LOGGED-IN TENANT's domain, NOT a fixed subdomain. So `alice.line-works.com`
and the decoy `cxtalk.line-works.com` will have NO public DNS A record — they only resolve for a
tenant whose domain is `<baseDomain>`. => the API is reachable ONLY with a valid tenant session +
that tenant's baseDomain. Do NOT burn time fuzzing the decoy: a uniform `400 "Invalid Path"` on
`/`, `/api`, `/api/v1`, `/v1`, `/health`, and other common prefixes is a strong signal it is NOT the
live API surface.
TEST PLAN (dynamic lane): run Frida / mitmproxy MITM on a rooted emulator — the app has NO cert
pinning and trusts the user CA via `<debug-overrides>` (see Stage 4.6 F1), so all traffic is
decryptable. Capture the real `alice.<tenant>/webhomegw/...` requests + Authorization headers, then
enumerate the sequential widget/object IDs for cross-tenant BOLA/IDOR using two own accounts.

### Decoy-host signal (caught in a real LINE WORKS engagement)
A host that resolves and returns the SAME short error for `/`, `/api`, `/api/v1`, `/v1`, `/health`,
and `/<common-path>` is almost certainly not serving the live API. Reconstruct the real endpoint from
the APK instead of fuzzing blind. Concrete walkthrough: `references/api_reconstruction_from_smali.md`.

## Stage 5 — Exported component enumeration

AndroidManifest.xml lists components. Exported ones (especially with `android:exported="true"` or implicit-export via intent-filter) can be triggered by other apps — potential intent-injection attack surface.

```bash
# Decode binary AndroidManifest if needed
apktool d <package>.apk -o decoded_<package>/    # apktool decodes binary manifest

# Or read directly from jadx output
cat decompiled_<package>/resources/AndroidManifest.xml | grep -E '<(activity|service|receiver|provider)' | head -50

# Filter exported
grep -E 'android:exported="true"' decompiled_<package>/resources/AndroidManifest.xml
```

For each exported component, check:
- Does it accept extras that flow into a WebView (intent → WebView → XSS / file://)
- Does it accept URI extras (potential SSRF via deep link)
- Does it pass extras to other Activities (intent redirection)

---

## Stage 6 — Firebase / cloud-service config inspection

```bash
# google-services.json — full Firebase config
find extracted_<package> -name "google-services.json" -exec cat {} \; | python3 -m json.tool

# Look for:
#   project_id   → can guess Firestore / RTDB URL: https://<project_id>.firebaseio.com/.json
#   storage_bucket → can guess GCS bucket: gs://<bucket>
#   web_api_key  → can use to enumerate Firebase tenant config

# Test if Firestore is publicly readable
curl -s "https://firestore.googleapis.com/v1/projects/<project_id>/databases/(default)/documents/users"

# Test if Realtime DB is publicly readable
curl -s "https://<project_id>.firebaseio.com/.json"

# Test if Storage Bucket is publicly listable
curl -s "https://firebasestorage.googleapis.com/v0/b/<bucket>/o"
```

---

## Stage 7 — Runtime instrumentation (Frida)

For when static analysis isn't enough — you want to dump tokens at runtime, bypass cert pinning, or trace API calls.

### Setup
```bash
pip install --break-system-packages frida-tools objection
adb devices  # ensure device/emulator connected
# Push frida-server to device (root required, or use rooted emulator like Genymotion / x86_64 AVD)
```

### Cert-pinning bypass (universal)
```javascript
// frida-script-pinning-bypass.js
Java.perform(function() {
    // OkHttp
    try {
        var CertificatePinner = Java.use('okhttp3.CertificatePinner');
        CertificatePinner.check.overload('java.lang.String', 'java.util.List').implementation = function() {
            console.log('[+] OkHttp pinning bypassed for: ' + arguments[0]);
            return;
        };
    } catch (e) {}
    // HttpsURLConnection
    try {
        var TrustManagerImpl = Java.use('com.android.org.conscrypt.TrustManagerImpl');
        TrustManagerImpl.verifyChain.implementation = function(chain) {
            console.log('[+] TrustManagerImpl verifyChain bypassed');
            return chain;
        };
    } catch (e) {}
});
```
```bash
frida -U -l frida-script-pinning-bypass.js -f <package_id> --no-pause
```

### Hook HTTP requests
```javascript
Java.perform(function() {
    var OkHttpClient = Java.use('okhttp3.OkHttpClient');
    var Request = Java.use('okhttp3.Request');
    var Call = Java.use('okhttp3.Call');
    
    OkHttpClient.newCall.implementation = function(req) {
        var url = req.url().toString();
        var headers = req.headers().toString();
        console.log('[REQ] ' + url);
        console.log('[HDRS] ' + headers);
        return this.newCall(req);
    };
});
```

### Quick token extraction via objection
```bash
objection --gadget com.target.app explore
# Inside:
android hooking watch class_method <class>.<method> --dump-args --dump-return
```

---

## Stage 7.5 — Smali instrumentation without apktool rebuild (PATCH/REBUILD FALLBACK)

Use case: you modified smali and need a runnable APK, but `apktool b` fails on the
decompiled folder.

### Pitfall — `$` in resource filenames breaks rebuild
Apktool can decompile an APK into `res/drawable/$avd_*` / `$m3_avd_*` / `$mtrl_*` files.
These filenames are INVALID for rebuild and cause aapt to exit 1:
`Invalid file name: must contain only [a-z0-9_.]`

### Fix A — rename bad resources before rebuild
```bash
find dec/res -name '$*' -print0 | xargs -0 -I{} bash -lc '
  d="{}"
  n=$(basename "$d")
  n="${n//\$/S}"
  mv -f "$d" "$(dirname "$d")/$n"
'
apktool b -o patched.apk dec/
```

### Fix B — direct APK patch + zipalign + jarsigner (preserves original resources)
When rebuild still fails, bypass aapt entirely and rebuild a valid installable APK by:
1) unpacking the original
2) overwriting only modified smali
3) zipaligning
4) signing with a real debug keystore via jarsigner

```bash
BASE=/path/to/original.apk
SMALI_PATCH=/path/to/modified/checkroot.smali
BT=/home/user/Android/Sdk/build-tools/36.1.0   # adjust if needed
D=/tmp/apk-patch
mkdir -p "$D/unpacked"
cd "$D/unpacked"
unzip -q "$BASE" -d .
mkdir -p smali/com/BugBazaar/ui/detectAppInt
cp "$SMALI_PATCH" smali/com/BugBazaar/ui/detectAppInt/checkroot.smali
cd "$D"
rm -f patched.zip aligned.apk aligned-unsigned.apk
zip -qr patched.zip -d unpacked/*
"$BT/zipalign" -v -p 4 patched.zip aligned.apk
keytool -genkeypair -keystore "$D/debug.keystore" -keyalg RSA -keysize 2048 -validity 10000 \
  -alias androiddebugkey -storepass android -keypass android -dname "CN=Android Debug" -noprompt >/dev/null
cp aligned.apk aligned-unsigned.apk
zip -d aligned-unsigned.apk 'META-INF/*' >/dev/null 2>&1 || true
jarsigner -keystore "$D/debug.keystore" -storepass android -keypass android aligned-unsigned.apk androiddebugkey
cp aligned-unsigned.apk "$BASE.injected-patched-signed.apk"
```

Pitfall: `apksigner --ks /dev/null` is invalid and will fail with `Tag number over 30 is not supported`. Use `jarsigner` with a real debug keystore as above.

Quality check before install:
```bash
# Confirm libs are present after repack
unzip -l "$BASE.injected-patched-signed.apk" | grep '^lib/' | head
```

Validation:
```bash
adb install -r "$BASE.injected-patched-signed.apk"
adb logcat -s BugBazaar-Inject
```

If you see `INSTALL_FAILED_INVALID_APK: Failed to extract native libraries, res=-2`, the APK package likely lost or misordered entries during zip/re-sign. Re-run Fix B with zipalign + jarsigner exactly as above, rather than signing the raw zip directly.

## Stage 7.6 — Smali Log.d injection pattern (teaching PoC)

Target: instrument a concrete app-side method to learn the full modify→rebuild→install→log
workflow. This avoids the common blocker of "I don't know which class makes HTTP calls."

Example target: `com.BugBazaar.ui.detectAppInt.checkroot.checkRootBeer()`

Smali injection template:
```smali
.method public checkRootBeer()V
    .locals 7

    # START LOG
    const-string v2, "BugBazaar-Inject"
    const-string v3, "RootCheck: started"
    invoke-static {v2, v3}, Landroid/util/Log;->d(Ljava/lang/String;Ljava/lang/String;)I

    # original native check
    invoke-static {}, Lcom/darvin/security/Native;->isMagiskPresentNative()Z
    move-result v0

    # LOG native result
    const-string v3, "BugBazaar-Inject"
    if-eqz v0, :cond_log_native_false
    const-string v4, "RootCheck: native=true"
    goto :cond_log_native_continue
    :cond_log_native_false
    const-string v4, "RootCheck: native=false"
    :cond_log_native_continue
    invoke-static {v3, v4}, Landroid/util/Log;->d(Ljava/lang/String;Ljava/lang/String;)I

    # original RootBeer check
    new-instance v1, Lcom/scottyab/rootbeer/RootBeer;
    iget-object v2, p0, Lcom/BugBazaar/ui/detectAppInt/checkroot;->context:Landroid/content/Context;
    invoke-direct {v1, v2}, Lcom/scottyab/rootbeer/RootBeer;-><init>(Landroid/content/Context;)V
    invoke-virtual {v1}, Lcom/scottyab/rootbeer/RootBeer;->isRooted()Z
    move-result v1

    # LOG rootbeer result
    const-string v3, "BugBazaar-Inject"
    if-eqz v1, :cond_log_rb_false
    const-string v4, "RootCheck: rootbeer=true"
    goto :cond_log_rb_continue
    :cond_log_rb_false
    const-string v4, "RootCheck: rootbeer=false"
    :cond_log_rb_continue
    invoke-static {v3, v4}, Landroid/util/Log;->d(Ljava/lang/String;Ljava/lang/String;)I

    # ... rest of original method, with branch-point logs added similarly
```

When the target APK lacks an obvious central HTTP caller in app smali, prefer this
instrumentation-teaching workflow over blind network logging. It still proves the
end-to-end patching pipeline and teaches smali register/branch mechanics.

## Stage 7.7 — End-to-end modify → rebuild → sign → install workflow (learning / lab APKs)

Use this when you need to demonstrate the full patching pipeline on a real APK and the
target is NOT a simple CTF-sized app. The PayTM session showed the exact sequence
that succeeded, and the exact blocker that stops a naive install.

### Verified sequence (works even when full rebuild fails)

```bash
APK=~/Downloads/net.one97.paytm.apk
WORK=~/Downloads/paytm-mod
KS=~/Downloads/paytm-hacklab.keystore
BT=/home/user/Android/Sdk/build-tools/36.1.0

# 1) Keystore (once)
keytool -genkeypair -v -keystore "$KS" -keyalg RSA -keysize 2048 -validity 10000 \
  -alias paytmkey -storepass android -keypass android \
  -dname "CN=learn lab, OU=lab, O=lab, L=city, ST=state, C=IN"

# 2) Decode — no-res keeps original resources and avoids the '$'-prefix / navigation-dir
#    aapt2 rebuild failures seen on modern apps.
apktool d --no-res -o "$WORK" "$APK"

# 3) Modify (examples)
sed -i 's/<application /<application android:debuggable="true" /' "$WORK/AndroidManifest.xml"
# add smali logging / hook in "$WORK/smali" or smali_classes*/

# 4) Rebuild
apktool b -f -o "$WORK/paytm-modified-nores.apk" "$WORK"

# 5) Sign
cd "$WORK"
jarsigner -verbose -keystore "$KS" -storepass android -keypass android \
  -signedjar paytm-signed-jar.jar paytm-modified-nores.apk paytmkey

# 6) Zipalign
"$BT/zipalign" -p -v 4 paytm-signed-jar.jar paytm-aligned.apk

# 7) Verify
jarsigner -verify -verbose -certs paytm-aligned.apk

# 8) Install
adb install -r paytm-aligned.apk
```

### Known install blocker: `INSTALL_FAILED_MISSING_SPLIT`

Modern Play-delivered APKs declare `android:requiredSplitTypes="base__abi,base__density"` in
the manifest. Apktool decode/build DROPS that split config. The rebuilt base APK alone is
therefore missing required splits, and `adb install` fails with:

```
Failure [INSTALL_FAILED_MISSING_SPLIT: Missing split for net.one97.paytm]
```

This is NOT a signing problem; it is a packaging problem. There are three paths:

1. Accept the limitation for learning: use `--no-res` + repack and accept that resource-heavy
   splits are absent. It still runs, shows the launcher icon, and lets you test smali/logic
   changes.
2. Recover splits from the original APK / XAPK and supply them on install:
   `adb install-multiple base.apk config.en.apk config.xxhdpi.apk ...`
3. Use a split-aware toolchain (`bundletool build-apks` / `bundletool install-apks`) instead
   of raw `adb install`. That requires re-generating the `bundletool`-style `splits0.xml`,
   which apktool does not preserve.

For most red-team / teaching use cases, path 1 is enough — the binary still installs and
the modified code path runs. Path 2 is the right next step if UI/rendering breaks.

### Why `--no-res` is often the right call for big real-world apps

Full-resource rebuild of large modern apps frequently fails before install:
- `res/navigation/` is invalid for older aapt.
- `res/drawable/$avd_*` / `$m3_avd_*` filenames break aapt2 compile.
- AAPT/AAPT2 mismatch in distro-packaged apktool vs Android SDK build-tools.

`apktool b --no-res` preserves original resources from `unknown/` + `assets/` and only
recompiles smali + manifest. That is the fastest path to a runnable modified APK.

## Stage 8 — Network traffic capture (via mitmproxy)

For deeper API discovery once pinning is bypassed.

```bash
# Run mitmproxy on host
mitmproxy --listen-port 8080

# Configure Android device proxy to host:8080
# Install mitmproxy CA cert on device:
#   - Pull from http://mitm.it on the device, or
#   - Push to /system/etc/security/cacerts/ on rooted device

# Use the Frida pinning bypass script while traffic flows through mitmproxy
# All API calls visible in mitmproxy UI
```

### Stage 8.0 — THE DEVICE PROXY IS A GLOBAL KILL-SWITCH: ALWAYS CLEAN UP

PITFALL (real session, user-impacting): after a pinning-bypass demo the assistant left
Android's global HTTP proxy pointed at `127.0.0.1:8080` while the `adb reverse` tunnel had
already been torn down. Every app on the phone then sent its traffic into the phone's OWN
loopback — a black hole — and the user reported "my wifi is showing no internet." Raw
`ping 8.8.8.8` still worked (ICMP ignores the proxy), which made it look like a DNS/wifi
fault instead of a proxy one. Do NOT touch the user's router/DNS/wifi: check the proxy first.

RULE: proxy + `adb reverse` are one unit. Tear down BOTH as the LAST step of any device work,
before you report "done":

```bash
adb shell settings put global http_proxy :0
adb shell settings delete global global_http_proxy_host
adb shell settings delete global global_http_proxy_port
adb reverse --remove-all
# verify
adb shell settings get global http_proxy          # expect ":0"
adb reverse --list                                # expect empty
```

**Diagnostic — is "no internet" actually an orphaned proxy?**
```bash
adb shell settings get global http_proxy          # anything but :0/null  = suspect
adb reverse --list                                # empty while proxy set  = black hole
adb shell "ping -c 2 8.8.8.8"                     # ICMP works  => network is FINE
adb shell "ping -c 2 google.com"                  # DNS+ICMP work => network is FINE
```
Pings pass but apps/browser fail => it is the proxy, not the network. Clearing it restores
connectivity immediately — no reboot, no router change. Note `adb reverse --list` can be
empty even while things work (it is per-connection and does not persist), so the proxy
setting is the authoritative signal.

### Stage 8.1 — CA injection via Magisk module (survives reboot, additive-only)

The cert filename MUST be the cert's `subject_hash_old`, or the Android trust store will not
load it (a friendly name like `mitmproxy.pem` is silently ignored):

```bash
HASH=$(openssl x509 -in ~/.mitmproxy/mitmproxy-ca-cert.pem -subject_hash_old -noout)
openssl x509 -in ~/.mitmproxy/mitmproxy-ca-cert.pem -outform PEM > "$HASH.0"

adb shell "su -c 'mkdir -p /data/adb/modules/mitmca/system/etc/security/cacerts'"
adb push "$HASH.0" /data/local/tmp/
adb shell "su -c 'cp /data/local/tmp/$HASH.0 /data/adb/modules/mitmca/system/etc/security/cacerts/'"
adb shell "su -c 'chmod 644 /data/adb/modules/mitmca/system/etc/security/cacerts/$HASH.0'"
adb reboot
adb shell "su -c 'ls /system/etc/security/cacerts/ | grep $HASH'"   # verify
```

Cleanup — the module only ADDS one cert; the real store stays intact:
```bash
adb shell "su -c 'rm -rf /data/adb/modules/<module-name>'"
adb reboot
```

### Stage 8.2 — CA injection and pinning are SEPARATE layers

CA injection only fixes the **trust** layer. If the app pins SPKI hashes (as
`tech.httptoolkit.pinning_demo` does — pinning `testserver.host`'s root/intermediate SPKI),
you still get `Certificate pinning failure!` because those keys are SERVER-SIDE and NOT in
the APK; a forged CA can never satisfy a pin. CA-only is the expected RED state; the GREEN 200
requires CA (trust) + Smali patch (pin removal, Stage 7.5/7.7) together. Say this explicitly
in the report so the evidence is never read as "CA alone bypassed pinning."

Smali patch for OkHttp pinning — replace the body of ALL THREE overloads with `.locals 0` +
`return-void`:
- `okhttp3.CertificatePinner.check(String, List)`
- `okhttp3.CertificatePinner.check(String, Certificate...)`
- `okhttp3.CertificatePinner.check$okhttp(String, Function0)`

Then rebuild (Stage 7.7), `zipalign -p 4`, `apksigner` with v1+v2 enabled, uninstall the
original, install the patched build.

---

## Decision tree — what to do with what you find

| Finding | Next move |
|---|---|
| Active JWT (not expired) | Test against the API host — does it grant access? Try sid manipulation |
| Expired JWT | Inspect path tokens / API endpoint structure — useful intel for post-VPN |
| AWS access key | Use `awscli` to test: `aws sts get-caller-identity` — many leaked keys still have permissions |
| Firebase project_id + web_api_key | Test public Firestore/RTDB/Storage read |
| Google API key (AIza*) | Test against `https://www.googleapis.com/customsearch/v1` etc. — see what API the key activates |

### VERIFICATION PITFALL — HTTP 200 is NOT "confirmed vulnerable" (real session)
When you curl a keyed endpoint to prove a leak, the HTTP TRANSPORT status is misleading:
- Google Maps/Places/Directions return **HTTP 200 with an error BODY**: `{"status":"REQUEST_DENIED","error_message":"The provided API key is invalid."}`. A naive `curl -w "%{http_code}"` check reports "200 = success" and you will file a FALSE POSITIVE.
- ALWAYS read the response BODY for the provider's own status field (`status`, `error_message`, `code`) before claiming the key works.

PLACEHOLDER-KEY TRAP (real session): A grep hit `AIzaSy...00Tc` looked like a Maps key, but
the literal `...` in the middle means it is a REDACTED/PLACEHOLDER string, NOT a real key.
Real Google keys are exactly `AIza` + 35 alphanumerics, no dots. The app rejected it as
"invalid" on every endpoint. Rule: after grepping `AIza[0-9A-Za-z_-]{35}`, verify the matched
string has NO literal `...` / redaction and is a full 39 chars; then do a live read-only GET and
parse the BODY status. Withdraw the finding if Google says "invalid" or "denied".

```bash
# Correct verification — check BODY status, not just HTTP code
K="<full_key_no_dots>"
curl -s "https://maps.googleapis.com/maps/api/geocode/json?address=Tokyo&key=$K" \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print('status=',d.get('status'),'|',d.get('error_message'))"
# Good: status=OK  -> key valid & unrestricted (file it)
# Bad:  status=REQUEST_DENIED, "API key is invalid" -> placeholder/revoked -> RETRACT
```

Also grep ALL split APKs for secrets (not just the base) — but in the XAPK case the base apk
held the only key; the 8 config.*.apk splits had none. One read-only GET per endpoint is enough;
do NOT hammer the API (respects provider quotas + avoids noise).
| Hardcoded HTTP URLs (http://) | Possible MITM via downgrade if cert pinning is missing |
| Pinned cert for internal host | New asset discovery — that host is real |
| Exported Activity with WebView | Test intent-injection → URL-loading abuse |
| Stack-trace artifacts (Stack Overflow URLs) | Identify the developer's questions → infer architecture |
| Hardcoded credentials | Spray immediately (respect any caps from related skills) |

---

## Anti-patterns

- **Don't grep only for "password"** — most secrets have specific high-signal patterns (AKIA, AIza, eyJ, etc.). Generic word grep produces too much noise.
- **Don't skip XAPK split APKs** — config.armeabi splits and config.<lang> splits sometimes contain different code paths.
- **Don't trust expired JWTs as "dead intel"** — the path structure, endpoint list, and signing algorithm are still useful. The 8-year-expired-JWT example above shows this.
- **Don't reverse only the latest version** — older APK versions (via APKMirror version history) sometimes have secrets removed in newer versions but still active server-side.
- **Don't ignore Firebase even if app looks "simple"** — Firebase rules misconfigurations (public read on Firestore) are extremely common.
- **Don't run Frida on a production device** — use rooted emulator or test device only.

---

## Tooling install (one-time)

```bash
brew install jadx p7zip
pip install --break-system-packages frida-tools objection
# Genymotion or AVD for rooted Android emulator
```

For APK download convenience, can add a `download-apk` shell function:
```bash
download-apk() {
  local pkg="$1"
  curl -sk -L --max-time 60 "https://d.apkpure.net/b/APK/$pkg?version=latest" -o "$pkg.apk"
  echo "Downloaded $(wc -c < "$pkg.apk") bytes"
  file "$pkg.apk"
}
```

---

## Bridge to neighboring skills

- `offensive-osint` — Play Store / APKMirror enum is part of broader OSINT
- `hunt-cloud-misconfig` — Firebase public-read is exactly this skill's specialty post-discovery
- `hunt-api-misconfig` — JWT manipulation once you have the algorithm + sample token
- `evidence-hygiene` — extracted secrets need redaction before report inclusion
- `redteam-mindset` — APK reverse on day-1 of an engagement, not as an afterthought

**References:**
- `references/apk_static_audit_pitfalls.md` — XAPK extraction recipe, the
  "HTTP 200 != success" key-verification pitfall (with curl+python body-status check).
- `references/apk_provenance_and_config_audit.md` — provenance (genuine vs repack) recipe, the
  F1 `network_security_config` cleartext+user-CA+no-pinning report structure, and the WebView
  `shouldOverrideUrlLoading` origin-check audit (highest-value bridge class).
- `references/bugbazaar_smali_injection_task12.md` — BugBazaar_v1.2.1 task 1.2 smali injection
  runbook, including why `apktool b` failed on `$`-prefixed resource filenames and the verified
  direct-APK patch + zipalign + jarsigner workflow that produced a working signed APK.
- `scripts/extract_signer_cert.py` — pulls V2/V3 signer cert from the APK Signing Block (keystore
  and `META-INF/*.RSA` fail on V2-only APKs). Run before any mobile-static report to prove the
  binary is the genuine vendor build.

---

## Real-world finding template (anonymized — authorized engagement)

**Finding: Hardcoded JWT + 30+ Internal API Endpoints in a customer-facing APK**

- Subject: Hardcoded artifacts in legacy mobile build reveal internal API surface
- Observations: Decompilation of `com.<client>.<app>` revealed embedded JWT (expired ~8 years earlier) and 30+ `/v1/*` endpoint paths against `api2.<client>.example` (internal-only externally)
- Description: APK ships with developer build artifacts. Path tokens are security-by-obscurity; API endpoint inventory is reconnaissance-grade.
- Impact: Post-VPN-foothold (via cred compromise), attacker has full API surface map without binary reverse. HS256 secret recovery (via SSRF/LFI) would yield arbitrary token forging.
- Recommendation: rotate HS256 secret, migrate to RS256, remove hardcoded URLs from builds, audit all org APKs.
- Evidence: extracted strings, decoded JWT, endpoint inventory

---

## Related Skills & Chains

- **`cloud-iam-deep`** — APK secret extraction frequently yields live AWS/GCP/Azure credentials. Chain primitive: jadx string-grep produces AWS Access Key ID + Secret → `cloud-iam-deep` `aws sts get-caller-identity` → role/policy enumeration → IAM privilege-escalation path (one of 24 documented AWS escalation patterns) → cloud-plane takeover. Same flow applies to GCP service-account JSON and Azure shared-access-signature tokens extracted from APK resources.
- **`hunt-api-misconfig`** — APK endpoint inventory hands you the API surface for free; mass-assignment, JWT, and CORS bugs are typical. Chain primitive: APK reveals `/v1/users/me` and `/v1/admin/users` → `hunt-api-misconfig` mass-assignment probes (`{is_admin:true}`) against `/v1/users/me` → admin role escalation → access to `/v1/admin/users`.
- **`hunt-rce`** — Hardcoded JWT signing secrets (HS256) extracted from APK enable arbitrary token forging. Chain primitive: APK strings yield HS256 secret → forge admin token → access admin API → if API has eval/template/sink → `hunt-rce` to server. Also: exported components with intent-injection sinks can reach `Runtime.exec` if app is local-installed.
- **`offensive-osint`** — APK is one node in the broader org recon graph; pair with breach corpora and cert transparency. Chain primitive: APK reveals internal API hostname `api2.example.com` → `offensive-osint` certificate-transparency lookup → discover sibling subdomains → expanded attack surface.
- **`redteam-report-template`** — APK findings need clear "what the binary leaks" framing because client engineers often dismiss mobile-static findings as "obfuscation problem." Chain primitive: validated finding (token/URL/secret extracted) → `triage-validation` 7-Question Gate (specifically: "does this credential still authenticate today?") → `redteam-report-template` packaging with explicit binary version + extraction reproduction steps.
