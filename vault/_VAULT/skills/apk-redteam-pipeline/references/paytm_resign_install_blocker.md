# PayTM APK — resign/reinstall learning session (2026-10-30)

Artifact: `/home/user/Downloads/net.one97.paytm.apk`
Package: `net.one97.paytm`

## Keystore
`/home/user/Downloads/paytm-hacklab.keystore` alias `paytmkey` pass `android`

## Successful steps
- `apktool d --no-res -o ~/Downloads/paytm-smali net.one97.paytm.apk`
- add `android:debuggable="true"` to `<application>`
- `apktool b -f -o paytm-modified-nores.apk .`
- `jarsigner -signedjar paytm-signed-jar.jar paytm-modified-nores.apk paytmkey`
- `/home/user/Android/Sdk/build-tools/36.1.0/zipalign -p -v 4 paytm-signed-jar.jar paytm-aligned.apk`
- `jarsigner -verify -verbose -certs paytm-aligned.apk` → `jar verified`

## Install blocker (verbatim)
```
adb install -r paytm-aligned.apk
adb: failed to install paytm-aligned.apk: Failure [INSTALL_FAILED_MISSING_SPLIT: Missing split for net.one97.paytm]
Performing Streamed Install
```

Root cause: original manifest has `android:requiredSplitTypes="base__abi,base__density"`.
Apktool rebuild dropped required split configs, so a base-only APK is incomplete.

## Why full rebuild is hard on this APK
- Full decode → build hits aapt2 error: invalid resource entry names like `$avd_hide_password__0`.
- `res/navigation/` invalid for distro aapt.
- AAPT vs AAPT2 mismatch between `/usr/bin/aapt` and `/home/user/Android/Sdk/build-tools/36.1.0/aapt2`.

## Lesson
For large Play-signed apps, prefer `apktool d --no-res` + direct repack + jarsigner + zipalign.
That produces a runnable, installable base APK even when full resource rebuild is infeasible.
