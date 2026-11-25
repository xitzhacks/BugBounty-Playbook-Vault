# Root / Magisk Detection — Static Matrix + Bypass Reality

Use when a target app refuses to run on a rooted device and you need to know
WHAT it checks and WHETHER a given bypass can work. Distinguishing "the app
checks X" from "X is the thing firing" is the whole job.

## 1. Identify the detection SDK first (changes everything)

Grep the dex string tables and the RN bundle for SDK fingerprints BEFORE
thinking about bypasses. The bypass depends entirely on which SDK it is.

| SDK | Fingerprint strings | Where they live |
|---|---|---|
| **Appdome** | `AppdomeThreatEvent`, `registerAppdomeThreatEvents`, `Appdome_Threat_Event`, toast `REF: <hex> ... Detected by App` | RN bundle string table + a `*ThreatEvent*` TurboModule; detection itself is statically linked native, no Java class |
| **BioCatch** | `RootCheckConstants`, `DeviceIQRootedCollector`, `RootDetectionUtilsKt`, `BCDeviceSignalId$RootDetected` | dex (Java/Kotlin) |
| **Promon SHIELD / ThreatMetrix / SafeDK / dGuard** | vendor-named classes, `isRooted`, `RootBeer`, `com.promon.*` | dex |
| **Home-grown** | `isRooted`/`isDeviceRooted`/`rootDetected` + hardcoded path lists | dex |

If the app is **React Native / Hermes**, the JS bundle is a string mine:
`assets/index.android.bundle` holds detection event names, SDK keys and UI
strings even when the logic is native. `strings` over the bundle works directly
— no Hermes decompiler needed for triage.

### Extracting the threat-event taxonomy (re-runnable)

A single pass with a byte-level scanner recovers the full event-name table.
Event names are CamelCase ending in `Detected`/`Threat`; message templates are
readable sentences near those tokens. `scripts/mobile-detection-scan.py` does
this in one call and is the fastest way to enumerate what a given SDK build
can fire.

## 2. BioCatch root matrix (exact, from smali)

`DeviceIQRootedCollector.collect()` ORs SIX checks; any true => RootDetected.

1. `checkForSuBinary()` — `File.exists()` over a hardcoded list:
   `/data/local/su`, `/data/local/bin/su`, `/data/local/xbin/su`, `/sbin/su`,
   `/su/bin/su`, `/system/bin/su`, `/system/bin/.ext/su`,
   `/system/bin/failsafe/su`, `/system/sd/xbin/su`,
   `/system/usr/we-need-root/su`, `/system/xbin/su`, `/cache/su`, `/data/su`,
   `/dev/su`
2. `checkSuInPath()` — split `$PATH` on `:`, `File(dir,"su").canExecute()`
3. `checkRoSecure()` — `SystemProperties.get("ro.secure") == "0"`
4. `detectMagisk()` — `File(dir,"magisk").canExecute()` over `$PATH`
5. `checkForRWPaths()` — parse `mount`, match mount point against
   `/system`, `/system/bin`, `/system/sbin`, `/system/xbin`, `/vendor/bin`,
   `/sbin`, `/etc`, look for `rw`
6. `checkSuExists()` — `Runtime.exec("which su")`, exit 0 => true

Related collectors in the same SDK: `DeviceIQFridaCollector`
(`FridaDetected`, `FridaAttachDetected`, `FridaSpawnDetected`,
`FridaCustomDetected`) and `DeviceIQEmulatorCollector`.

**Consequence:** on a modern Magisk box where `su` is `/system_ext/bin/su`
(NOT in the hardcoded list) with `ro.secure=1`, `ro.debuggable=0`,
`release-keys`, and `/system` mounted ro — BioCatch returns FALSE. If the app
still blocks, the blocker is a different SDK (usually Appdome), not BioCatch.
Do not burn time on the wrong layer.

## 3. Appdome — why Magisk denylist is NOT enough

Appdome's `AdThreatEventTurboModule` (`NativeAdThreatEvent`) registers for
threat events and surfaces them as a toast + a kill. Constants seen in smali:
`AppdomeThreatEvent`, `threat_action`, `adb_enabled`, `dev_enabled`.

User-visible form (captured on device):
```
REF: 7144:C98A:531PHB Magisk Detected by App
```
plus a separate modal: `Developer Mode is on / Your device is at risk of being
hacked ...` with `Keep Using` / `Go to Settings`.

Empirically, on a device where `magisk --denylist add <pkg>` was applied and
**verified active** (Magisk logcat emits `logcat: revert [<pkg>] PID=[...]
UID=[...]`, proving Zygisk is loaded and unmounting for that process), Appdome
**still fired and the app still SIGKILLed itself**. Denylist hides mounts and
the su driver; it does NOT hide:
  - the installed `com.topjohnwu.magisk` package (PackageManager query)
  - `/data/adb/magisk` (readable)
  - Play Integrity / key-attestation signals Appdome evaluates out-of-band

### There are TWO independent gates — clearing one does not clear the other

Measured on Kotak 811 v5.5.9:
  - Tapping `Keep Using` on the Developer Mode modal does **not** stop the
    kill. The app still SIGKILLs itself seconds later.
  - The Developer Mode modal and the Magisk toast are **separate** Appdome
    threat events (`dev_enabled`/`adb_enabled` vs `MagiskManagerDetected`),
    each able to terminate the app on its own.

Consequence for the operator: a "keep using" button is NOT evidence the gate
is cleared, and dismissing a modal is not a bypass. Test the actual outcome
(app process alive + reaches login) after every stage, not the dialog state.

Effective order of attempts (cheapest first):
1. `pm hide com.topjohnwu.magisk` — removes the package-visibility signal.
2. `settings put global development_settings_enabled 0` — clears the
   `dev_enabled` threat event. **Do NOT also set `adb_enabled 0`** (see the
   transport trap below); clear dev-settings only and leave ADB alive.
3. Hide `/data/adb` from the app uid (Magisk module / bind-mount trick).
4. If still firing: hook the bridge (section 4) or patch the APK.

### TRANSPORT TRAP — never disable the adb you are standing on

`settings put global adb_enabled 0` is the framework gate for adbd itself. Run
it over USB adb and the ADB interface unenumerates **immediately**, killing your
own session. This happened in a real engagement: the stage-1 script set it, the
interface vanished, and the device was unreachable for the rest of the run.

The trap is worse than it looks because **the modem AT channel cannot undo it**.
After `adb_enabled=0`:
  - `ATD#19732864#` / `AT+USBDEBUG=0,1` still report `+USBDEBUG:1,NG_NONE OK`
    (the modem thinks it enabled it) but the ADB interface does not re-enumerate.
  - `AT+USBMODE=0..15` and comma variants return
    `+CME Error:PACM(AP),UNREGISTERED` — that channel cannot reach USB composition.
  - `usbreset <VID:PID>` + USB unbind/rebind re-enumerates to MTP+CDC only.
  - Wireless adb is also dead (`Connection refused`), so there is no second path.

Recovery is a **physical user action**: unplug/replug USB, unlock the phone, then
toggle USB debugging OFF→ON in Settings → Developer options. Scripted recovery
does not exist. Tell the operator this plainly and stop retrying.

Rule for any bypass script that must run over a live adb session: clear
`development_settings_enabled` (what the app actually reads in
`Utils.checkDebuggerOption`), never `adb_enabled`.

Do NOT assume "denylist enforced + entry present" means hidden. Confirm with
the Magisk revert logcat line, and confirm the app's actual behaviour
afterwards — the two are independent.

## 4. Definitive bypass — the Appdome bridge choke points

Because Appdome's detection is native-static, file/package hiding can never be
exhaustive against it. The reliable fix is to intercept the event at the Java
bridge. Four choke points, all verified in smali (Kotak 811 v5.5.9):

| # | Class | Member | Action |
|---|---|---|---|
| A | `...modules.threatevents.AdThreatEventTurboModule` | `handleAppdomeThreatEvent(Intent)` — `private final` | return immediately |
| B | same | `handleNotification(Intent)` — `private final` | return immediately |
| C | `com.biocatch...DeviceIQRootedCollector` | `collect(Context)` | return `null` |
| D | `...instantsavingsupiscanandpayrecharge.Utils` | `checkDebuggerOption(Context)`, `isDevEnabled()`, `isADBEnabled()` | force `false` |

Notes that make or break the hook:
- A and B are **private final**, not public — Xposed/Frida hooks them fine,
  but a naive `findAndHookMethod` on the wrong signature silently no-ops.
  Verify the exact signature against the smali before trusting the hook.
- D is the app's OWN probe (`Settings.Secure.development_settings_enabled` +
  `adb_enabled`) and is independent of Appdome's native path. Missing it leaves
  the Developer Mode modal firing even with A–C hooked.
- `Utils` field names are `isDevEnabled` / `isADBEnabled` (boolean) —
  `setBooleanField` works, but `checkDebuggerOption` re-reads Settings on every
  call, so hook the getter OR force the field after the read (do both).
- `BCDeviceSignalResult.Companion.success(Object)` is the normal return path;
  returning `null` from `collect` is enough — no need to construct a result.

Generated, signature-verified hook source:
`tools/hook_src/AppdomeSmother.java` in the engagement tree (regenerable with
`tools/make_xposed_hook.py`). Deploy as an LSPosed module scoped to the target
package; confirm with logcat tag `KotakBypass` and then verify the app actually
reaches the login screen.

## 5. Tooling pitfalls hit on a large banking APK

- **`jadx` can fail** on 140MB+ multidex APKs with
  `JadxRuntimeException: Can't create directory .../sources` even when the dir
  is writable, and `--no-res` variants behave inconsistently. Fallback:
  `baksmali d <apk> -o out` (per-dex: `baksmali d classes2.dex -o smali_classes2`).
  baksmali is slower but reliable; run it in background on big targets.
- **Native libs live in the split APKs**, not base.apk. A `find -name '*.so'`
  over the extracted base returns ZERO. Pull `split_config.arm64_v8a.apk` too —
  that is where `libloader.so`, `libreactnative.so`, etc. are.
- **RN Hermes bundle**: `strings assets/index.android.bundle` is enough to
  enumerate detection event names and SDK keys; a Hermes decompiler is only
  needed for control flow.
- **Toast text is truncated in logcat** by Samsung's privacy feature
  (`Text: SEF:` — 3 chars). The real text is only visible in a screenshot.
  `adb exec-out screencap -p` and read it; do not trust the events buffer.
- **`uiautomator dump`** can wedge adbd on some Samsung builds. Prefer
  `screencap` for "what is on screen right now".
- **A vision-model read of the screenshot** is worth one retry: the toast is
  a 900x164px overlay and is trivially legible to a vision model when OCR is
  not installed on the device.

## 6. Evidence to capture before touching anything

```
apk pull (base + split_config.arm64_v8a)      -> static analysis source
screencap of the block screen                  -> proves which SDK fired
logcat -d | grep -iE '<pkg>|Magisk'            -> denylist activity / kill
magisk --denylist ls + magisk --sqlite ...     -> bypass state
dumpsys package <pkg> | grep userId            -> uid for logcat correlation
```
Report the toast text and the SIGKILL timing as the proof, not a guess about
which check tripped.
