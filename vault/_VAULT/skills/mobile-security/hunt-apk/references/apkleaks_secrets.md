# apkleaks secret patterns observed on a real production APK (tv.abema v10.179.0)

Reference for triaging apkleaks output during Android SAST. These are the
HIGH-VALUE hits that warrant a finding; most of apkleaks' output is framework
noise (tracking URLs, license links, class names).

## Real secret classes to flag (CWE-798 hardcoded credentials)
- [Twitter_Secret_Key] — RSA DER private key (starts `30820xxx...`).
  Two variants found: `twitter.android` and `twitter.android.beta`.
  VERIFY it's a real RSA key: DER structure `30 82 .. | 30 82 .. | 02 01 02`
  (SEQUENCE/SEQUENCE/INTEGER version=2). apkleaks truncates — recover full
  key from smali/dex if you need to prove it.
- [Facebook_Secret_Key] / FACEBOOK_SIGNATURE — RSA private key blob.
- [Facebook_ClientID] / [Twitter_ClientID] — app IDs (lower severity, but note).
- Braze API key (e.g. `37a6259cc0c1dae299a7866489dff0bd`) — SDK key shipped
  in app; disclosure finding, not full compromise.
- [Google_API_Key] — value shows as `«redacted:AIza…»` in strings.xml.
  Recover via: `aapt dump --values resources base.apk | grep -A1 google_api_key`
  or `grep -rhoE "AIza[0-9A-Za-z_-]{35}" work/apktool/`.
  Test usability: Maps JS loader returns 200 WITH OR WITHOUT a key (not proof);
  only real API calls (Geocode/Places/YouTube) prove it. API-restricted keys
  return REQUEST_DENIED/403 → Low (info-leak only).
- [Google_Cloud_Platform_OAuth] client IDs (`*.apps.googleusercontent.com`).
- [Authorization_Basic] — `basic =` empty is noise; a populated value is a find.

## Informational / attack-surface aids (not secrets themselves)
- [IP_Address] bare IPs (e.g. 2.10.9.0, 2.9.0.0) — likely internal/test endpoints.
- [LinkFinder] long URL/endpoint list — use to build API map; filter framework
  (Google/Play/Braze/NewRelic) from app-owned hosts.
- Real backend hosts seen: auth.abema.tv, gateway.p-c2-x.abema-tv.com,
  dev-streaming-api-cf.d-c2-x.abema-tv.com, zeus-api.d-c3-e.abema-tv.com,
  upload.abema.io, api.twitter.com, admob-gmats.uc.r.appspot.com, Braze SSE.
- [Mailto] support addresses.

## Noise to IGNORE
- [JSON_Web_Token] section is actually dependency VERSION STRINGS (androidGradlePluginVersion etc) — not JWTs.
- Endless `/com/braze/...`, `/com/squareup/...`, timezone/license/sdk class paths — framework.
- `http://schemas.android.com/...`, `http://www.apache.org/...` — XML namespaces.

## Reporting tier
HIGH/MED: Twitter/Facebook RSA private keys in binary.
MED:    Braze API key, populated Basic auth, usable Google key (rare).
LOW:    OAuth client IDs, API-restricted Google key, bare IPs, internal hosts.

## apkleaks run note (overlaps SKILL.md pitfalls)
Multidex APKs are SLOW and can OOM. Run background with memory cap:
`export _JAVA_OPTIONS="-Xmx2g" && apkleaks -f base.apk -o work/apkleaks_report.txt`
Do NOT set `ulimit -v` low — it breaks the JVM class-space allocation.
