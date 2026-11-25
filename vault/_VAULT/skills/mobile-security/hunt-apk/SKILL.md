---
name: hunt-apk
description: Mobile Android APK security assessment skill. Runs the full SAST plus DAST-prep checklist against one or more target APK or XAPK files. Covers AndroidManifest review, strings and resource secret extraction (Google, Firebase, AWS Cognito), network_security_config analysis, WebView and JS-bridge origin checks, SSL-pinning and root-detection presence, signature and Janus checks, Firebase misconfig probing, apkleaks automated sweep, and data-storage checks. Use at the START of any Android bug-bounty or mobile pentest task, or whenever the user drops an APK path and asks to check or hunt the android or run the APK checklist. Produces a consolidated per-APK report. Hardening-aware, distinguishes real findings from framework noise.
---

# HUNT-APK — Android APK Security Assessment Playbook

Target input: a folder or file path containing .apk / .xapk / .aab files.
Default working layout created under the target's parent:
  <target>/work/apktool/   (apktool decode: res + smali)
  <target>/work/jadx/      (jadx java sources)
  <target>/work/apkleaks_report.txt

## 0. Pre-flight (tooling)
Required: apktool, jadx, aapt/aapt2, keytool. Optional: apkleaks (pip in venv),
frida/objection (DAST, needs device). Install apkleaks safely:
```
python3 -m venv /tmp/akv && /tmp/akv/bin/pip install apkleaks
```
If apkleaks OOM-crashes on multidex: run with _JAVA_OPTIONS="-Xmx2g" and in
background (terminal background=true, notify_on_complete=true). Do NOT set
ulimit -v low — it breaks the JVM class space.

## 1. Inventory + decode (parallel background calls)
```
aapt dump badging base.apk | grep -E "package:|sdkVersion:|targetSdkVersion:|uses-permission:"
apktool d -f -o work/apktool base.apk          # background=true
jadx -d work/jadx --no-res -j 4 base.apk       # background=true
```
Signature / Janus:
```
python3 - <<'PY'
import zipfile
z=zipfile.ZipFile('base.apk'); n=z.namelist()
v1=any(x.startswith('META-INF/') and x.endswith(('.RSA','.DSA','.SF')) for x in n)
v2=b'APK Sig Block' in open('base.apk','rb').read()
print("Janus(V1-only) risk:", "YES" if v1 and not v2 else "NO (V2/V3 present)")
PY
```

## 2. SAST — MANUAL checklist

### 2.1 AndroidManifest.xml
- android:exported="true" components: enumerate, then SPLIT app-owned
  (<pkg> prefix) vs framework (Google/Play-Services/Firebase/Braze). Only
  app-owned unguarded exported activities/services/receivers are real risk.
  ```
  grep -E 'android:exported="true"' work/apktool/AndroidManifest.xml
  grep -iE '<pkg>'  # filter to app package
  ```
- READ_EXTERNAL_STORAGE / WRITE_EXTERNAL_STORAGE -> scoped-storage note.
- android:allowBackup="true" -> backup data-leak vuln (report if true).
- android:minSdkVersion < 28 -> auto-cleartext-by-default risk (informational).
- android:debuggable="true" -> report.
- android:requestLegacyExternalStorage="true" -> note.
- Activity exploit: adb shell am start -n <pkg>/<Activity>
- Backup exploit ref: https://github.com/rodolfomarianocy/Tricks-Pentest-Android-and-iOS-Applications/blob/main/insecure_data_storage_android.md#backups-for-sensitive-data

### 2.2 resources.arsc / res/values/strings.xml  (SECRETS)
apktool REDACTS key values in strings.xml as redacted:AIza. Recover real
values two ways:
```
aapt dump --values resources base.apk | grep -A1 -iE "google_api_key|google_crash_reporting_api_key|firebase_database_url|aws_identity"
grep -rhoE "AIza[0-9A-Za-z_-]{35}" work/apktool/ | sort -u
```
Check for:
- google_api_key, google_crash_reporting_api_key, CRASHLYTICS_API_KEY
  -> test with gmapsapiscanner logic / live call. NOTE: Maps JS loader serves
  to ALL (key-or-no-key); only real API calls prove usability. A key that
  returns REQUEST_DENIED/403 on data APIs is API-RESTRICTED (low impact).
- Firebase DB URL (*firebaseio.com) ->
  probe https://<app>.firebaseio.com/.json and /.settings/rules.json?auth=
  and storage https://firebasestorage.googleapis.com/v0/b/<bucket>/o.
  Deactivated(423)/list-disallowed = safe.
- AWS Cognito: aws_identity_pool_id like us-east-1:7e9426f7-... ->
  test unauthenticated Cognito creds.
- default_web_client_id, OAuth client ids, tokens.

### 2.3 res/xml/network_security_config.xml
- cleartextTrafficPermitted="true" at base-config (GLOBAL) -> critical.
  If scoped to localhost/10.0.2.2 only -> pass (dev only).
- debug-overrides trusts user CA -> MITM-able, no pinning.
- pin-set present? If ABSENT -> lack of SSL pinning (reportable).
- autosendlogs enabled without whitelist -> note.

### 2.4 Other static checks (smali grep)
```
grep -rln "addJavascriptInterface" work/apktool/smali*/
grep -rln "setJavaScriptEnabled"   work/apktool/smali*/
# dangerous combo = addJSI in a file that loads REMOTE/untrusted content w/o origin guard
grep -rln 'shouldOverrideUrlLoading' work/apktool/smali*/
# count guarded vs unguarded (host()/equals()/matches()/startsWith())
```
- Sensitive in source: grep -rhoiE "(api_key|access_token|secret|password|private_key|bearer|encryption_key|aes_key)" work/apktool/smali*/ (filter framework noise).
- Obfuscation: % of single/double-letter class names (R8/ProGuard).
- Janus: see section 1.
- Firebase / AWS: see section 2.2.
- assets/ dir: look for *.pem (PUBLIC KEY = safe; PRIVATE KEY = leak),
  *.js WebView bridges, GTM containers, *.db / prebuilt shared_prefs.

### 2.5 Data storage (static)
No prebuilt DB/shared_prefs ship in APK usually. At runtime (device):
```
cd /data/data/<pkg>
find . -type f -exec grep -i "SECRET\|token\|password" {} +
sqlite3 databases/<x>.db "SELECT * FROM <tbl>;"
cat shared_prefs/Prefs.xml
```
Check /js /www dirs for keys.

## 3. SAST — AUTOMATED
1. MobSF (preferred, all-in-one): docker run mobsf; or mobsf.live / mobexler.
2. apkleaks: apkleaks -f base.apk -o work/apkleaks_report.txt (covers ~40% of
   static; ALWAYS pair with manual 2.2/2.4 — apkleaks misses context).

## 4. DAST-PREP (static indicators; full DAST needs rooted device/emulator)
USER WORKFLOW PREFERENCE (mobile engagements): run the dynamic work ON THE
DEVICE, not from the laptop. Pull the APK to the phone, disassemble and probe
there, and only pull artifacts back when they're the deliverable. The user has
explicitly said "do this only using Termux, not this laptop" for on-device
engagements — respect that unless they say otherwise. If the device transport
drops mid-engagement (USB cable out, wireless adb refusing), say so plainly and
continue with whatever was already pulled, rather than retrying in a loop.

Bypass tooling reference (for when device is available):
- SSL pinning: Objection `android sslpinning disable`; Frida scripts;
  ConscryptTrustUserCerts Magisk module (NSC-based); apk-mitm.
- Root detection: Objection `android root disable`; Frida; Magisk + LSPosed
  modules (JustTrustMe, BypassRootCheckPro); Hidemyapplist.
- Screenshot/FLAG_SECURE: Objection `android ui FLAG_SECURE false`; Frida.
- Anti-debug/USB/Frida: frida codeshare scripts (universal-android-debugging-bypass,
  anti-frida-bypass, android-common-security-bypasses).
- Proxy/Emulator detect: Superproxy / Oxyproxy APKs.
- End-to-end encryption: AES observe via frida codeshare @dzonerzy/aesinfo.
- Insecure logging: adb logcat | grep -iE "password|token|username".
- Clipboard leak: check if creds persist in clipboard.

Static DAST-prep indicators to record NOW (no device):
- SSL pinning present? (NSC pin-set OR custom TrustManager/checkServerTrusted
  override in app code — NOT OkHttp Android10Platform framework class).
- Root detection libs? (RootBeer / subinary / isRooted in APP code).
  BEFORE proposing a bypass, identify WHICH SDK does the detection (Appdome,
  BioCatch, Promon, home-grown) — the bypass depends entirely on it. See
  references/root-detection-bypass.md for the exact BioCatch six-check matrix,
  why Magisk denylist is NOT enough against Appdome, the verified Appdome
  bridge choke points for the LSPosed hook, and the toolchain pitfalls
  (baksmali fallback, native libs in split APKs, RN bundle string mining,
  Samsung truncating toast text in logcat).
  Run `scripts/mobile-detection-scan.py fingerprints <apk>` FIRST — it
  identifies the SDK from the APK in one call, then `threats` / `messages`
  enumerate the event table and the exact block-screen text. Do not design a
  bypass before knowing which SDK is firing.
- FLAG_SECURE on sensitive screens? (FORCE_FLAG_SECURE / setFlags SECURE).
- Verbose logging sinks (count of android.util.Log invocations).

## 5. Reporting
Write <target>/APK_SECURITY_REPORT.md with sections:
manifest, secrets, NSC, other-static, DAST-prep, SUMMARY (CONFIRMED /
NOT-VULNERABLE / PENDING), NEXT STEPS (dynamic). Rate: global cleartext +
user-CA = Medium; lack of pinning = Medium; no root detect = Low/Med;
API-restricted key = Low (info-leak only).
ALSO write a dated MASTER_<YYYY-MM-DD_HH-MM-SS>.md at the engagement root that
consolidates every sub-report (apkleaks output, manifest notes, findings, next
steps) into ONE file — future sessions then read a single file for full context
(user preference: avoid re-reading many files; seen on both LINE WORKS and
Abeam engagements). See references/apkleaks_secrets.md for the concrete secret
categories found in real APKs (Twitter/Facebook RSA private keys, Braze key,
OAuth IDs) and the DER private-key verification trick.

## 6. Pitfalls (learned)
- **Never run a state-changing bypass step while the same session depends on
  that state.** If you are driving the engagement over adb, a step that
  disables adb destroys your own access mid-run. Check every command against
  "does this break my transport / my shell / the device's network?" before
  executing. When a step is destructive, run it LAST or make it conditional.
- **Report a self-inflicted break immediately.** If a bypass step kills the
  transport, say plainly what you did, what it broke, and exactly what the user
  must do physically — do not spend the remaining turns retrying connection
  loops or quietly continuing as if nothing happened. The user cannot fix what
  they do not know is broken.
- Maps JS loader returns 200 WITH or WITHOUT a key -> NOT proof a key works.
  Only real API calls prove usability; API-restricted keys return DENIED.
- apktool redacts secret string VALUES -> recover via aapt --values / grep AIza.
- gx/* / Android10Platform in smali = OkHttp framework, NOT app pinning.
- Distinguish app-owned exported components from framework ones (filter by pkg).
- apkleaks on big multidex APKs can OOM -> run background with -Xmx2g, not ulimit.
- Firebase deactivated / storage list disallowed = NOT vulnerable.
- apkleaks output triage: most of it is framework noise (version strings
  mislabeled as JWT, sdk class paths, tracking URLs). The HIGH-VALUE hits are
  [Twitter_Secret_Key]/[Facebook_Secret_Key] RSA DER private keys, populated
  [Authorization_Basic], Braze API key, usable Google key. See
  references/apkleaks_secrets.md for the full triage table.
- HEAVY TOOLS (apkleaks, jadx, MobSF) crash with signal 1 / OOM on low RAM.
  USER ENFORCED WORKFLOW: always run them with `terminal(background=true,
  notify_on_complete=true)` and a memory cap (`_JAVA_OPTIONS="-Xmx2g"` for JVM
  tools). If a run dies, RESTART it with the same cap — do not re-run in the
  foreground and do not raise RAM blindly. A venv python (`/tmp/akv/bin/python -m
  apkleaks`) avoids PEP 668 conflicts. DO NOT `ulimit -v` low — it breaks the JVM
  class-space allocation and causes the very crash you are trying to avoid.
- MobSF is a useful SECOND automated opinion after apkleaks+manual; install via
  venv/pip (not `curl|sh`, which the environment consent-guard blocks) or docker.
  Note: scanning a THIRD-PARTY app with MobSF is for internal/own testing only —
  confirm program scope before acting on results.
