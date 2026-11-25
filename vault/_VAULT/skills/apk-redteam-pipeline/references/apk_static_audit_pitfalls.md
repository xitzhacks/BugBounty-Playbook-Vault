# APK static audit — condensed pitfalls & reproduction (from a LINE WORKS XAPK session)

## 1. XAPK extraction (condensed)
```bash
7z x -y <name>.xapk -oextracted/
cat extracted/manifest.json        # package, version_name/code, permissions, split_apks[]
BASE=extracted/<package>.apk       # the base APK holds the DEX/logic
apktool d -f -o dec/apktool "$BASE"
jadx -j 4 -d dec/jadx "$BASE"      # 150MB+ base: run background, poll
```
`*.apk` glob does NOT match `*.xapk` / `*.apks` — search both extensions.

## 2. Verify "unrestricted key" correctly (HTTP 200 != success)
```bash
K="<full_39char_key_no_dots>"
for ep in \
  "https://maps.googleapis.com/maps/api/geocode/json?address=Tokyo&key=$K" \
  "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=Tokyo&inputtype=textquery&key=$K" \
  "https://maps.googleapis.com/maps/api/directions/json?origin=Tokyo&destination=Osaka&key=$K" ; do
  curl -s "$ep" | python3 -c "import sys,json;d=json.load(sys.stdin);print(d.get('status'),'|',d.get('error_message',''))"
done
```
- `status=OK` -> valid + unrestricted -> FILE IT.
- `status=REQUEST_DENIED` / "API key is invalid" -> placeholder/revoked -> RETRACT.
- BEFORE testing: ensure key has no literal `...` and is exactly 39 chars (`AIza`+35).

## 3. WebView JS-bridge origin-check audit (high-value, fast)
Count `shouldOverrideUrlLoading` impls vs those doing host validation:
```bash
grep -rln 'shouldOverrideUrlLoading' dec/apktool/smali* | wc -l            # total
grep -rln 'shouldOverrideUrlLoading' dec/apktool/smali* | while read f; do
  grep -qE 'getHost|getScheme|equals\(|indexOf|matches|startsWith' "$f" && echo "CHECK:$f"
done                                                                       # validated
```
WebViews with a bridge but NO origin check in `shouldOverrideUrlLoading` = addJavascriptInterface
live on arbitrary navigations = reportable (pair with web-XSS hunt to weaponize).
addJavascriptInterface call sites: `grep -rnE 'addJavascriptInterface' dec/apktool/smali*`.
High-signal sinks: mail viewer (message body->WebView), miniapp Bridge (native bridge for
3rd-party miniapps), dev/WebInterfaceTestActivity (JS+file+content access+bridge in prod).

## 4. Findings that HELD (evidence-backed) vs RETRACTED this session
HELD: cleartextTrafficPermitted="true" (base-config, no domain); over-broad FileProvider
  (external-path path="/"); un-origin-checked WebView bridges.
RETRACTED: "unrestricted Maps key" — was a placeholder string; body said REQUEST_DENIED.
LESSON: a config-level finding (cleartext, FileProvider) is trivially provable and defensible;
  a "secret leak" claim needs live BODY verification or it becomes a false positive.
