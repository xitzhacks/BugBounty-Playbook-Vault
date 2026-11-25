# BugBazaar Task 1.2 — Verified Smali Injection Runbook

Context: BugBazaar_v1.2.1 APK reverse-engineering exercise for task 1.2.

## Why direct-APK patch was required
- `apktool b` fails on the decoded `BugBazaar_v1.2.1/` folder because `res/drawable` contains invalid `$`-prefixed filenames from animated drawables, e.g. `$avd_hide_password__0.xml`.
- Renaming those files is unsafe; it can break compiled resource references.
- Solution: patch only the modified smali into the original APK ZIP, then zipalign and sign.

## Verified fixed workflow
1. Unzip original APK into `unpacked/`
2. Overwrite `unpacked/smali/com/BugBazaar/ui/detectAppInt/checkroot.smali`
3. Repack: `zip -qr ../patched.zip .`
4. Align: `$BT/zipalign -v -p 4 patched.zip aligned.apk`
5. Strip old META-INF and sign with jarsigner + real debug keystore:
   - `zip -d aligned-unsigned.apk 'META-INF/*'`
   - `jarsigner -keystore debug.keystore ... aligned-unsigned.apk androiddebugkey`
6. Copy signed APK to target path for install.

## Do NOT do this
- `apksigner sign --ks /dev/null ...` — invalid keystore, fails with `Tag number over 30 is not supported`.
- `jarsigner` the raw `patched.zip` without zipalign.
- Rebuild from decoded folder unless you also fix every invalid `$` resource filename.

## Output APK used in session
`/home/user/Desktop/NS/Android/8. Android Reverse Engineering/1. Static Reverse Engineering/1.2/BugBazaar_task12_injected.apk`

## Log tag
`BugBazaar-Inject`

## Expected log lines
- `RootCheck: started`
- `RootCheck: native=true/false`
- `RootCheck: rootbeer=true/false`
- `RootCheck: not-rooted -> Signin` or `RootCheck: rooted -> showing alert`
