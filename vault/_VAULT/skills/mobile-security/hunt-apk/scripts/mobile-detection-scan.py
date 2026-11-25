#!/usr/bin/env python3
"""Enumerate mobile-app anti-tamper / detection signal strings.

Purpose
-------
Finds the detection SDK fingerprint, the threat-event name table, and the
human-readable message templates a mobile app uses when it refuses to run on
a rooted / instrumented device.

Use this BEFORE designing a bypass. Which SDK is doing the detection decides
whether a bypass can work at all (e.g. Magisk denylist defeats mount-based
checks but does nothing against a native-static SDK).

Inputs
------
  <apk-or-bundle>   a base.apk, a split_config.*.apk, or an already-extracted
                   assets/index.android.bundle

Typical flow
------------
  # 1. from the APK directly (reads the RN bundle out of it if present)
  python3 mobile-detection-scan.py threats  base.apk
  python3 mobile-detection-scan.py messages base.apk

  # 2. from an extracted bundle (fastest, no zip overhead)
  python3 mobile-detection-scan.py threats  assets/index.android.bundle
  python3 mobile-detection-scan.py context  assets/index.android.bundle MagiskManagerDetected

Exit codes: 0 = found something useful, 1 = no input / bad args,
            2 = input not readable.
"""
from __future__ import annotations

import re
import sys
import zipfile

# --- detection SDK fingerprints -------------------------------------------
SDK_SIGNATURES = {
    "Appdome": [
        b"AppdomeThreatEvent", b"registerAppdomeThreatEvents",
        b"Appdome_Threat_Event", b"Appdome Threat:",
    ],
    "BioCatch": [
        b"RootCheckConstants", b"DeviceIQRootedCollector",
        b"RootDetectionUtilsKt", b"DeviceIQFridaCollector",
        b"DeviceIQEmulatorCollector",
    ],
    "Promon": [b"com.promon", b"PromonShield"],
    "ThreatMetrix": [b"com.threatmetrix", b"ThreatMetrix"],
    "SafeDK": [b"com.safedk", b"SafeDK"],
    "dGuard": [b"dguard", b"DGuard"],
    "RootBeer": [b"RootBeer", b"rootbeer"],
    "FreeRASP": [b"freeRASP", b"Talsec"],
    "Home-grown": [b"isRooted", b"isDeviceRooted", b"rootDetected"],
}

# --- device-side signal strings ------------------------------------------
DEVICE_SIGNALS = [
    b"/system_ext/bin/su", b"/system/bin/su", b"/system/xbin/su", b"/sbin/su",
    b"/data/local/tmp/su", b"/su/bin/su", b"/data/local/bin/su",
    b"com.topjohnwu.magisk", b"/data/adb/magisk", b"/data/adb",
    b"ro.secure", b"ro.debuggable", b"ro.build.tags", b"test-keys",
    b"magisk", b"busybox", b"supersu", b"superuser", b"which su",
]

# --- SECOND GATE: the app's OWN dev/adb probe ----------------------------
# Independent of any detection SDK. The app reads Settings.Secure directly and
# can kill itself on dev-options alone, so a bypass that only clears the SDK
# signal still dies. Kotak 811 keeps this in Utils.checkDebuggerOption() with
# isDevEnabled/isADBEnabled cached fields; the RN bridge exposes it as
# isADBDisbled(Callback). Look for these when fingerprinting.
APP_DEV_PROBE = [
    b"development_settings_enabled",
    b"adb_enabled",
    b"isADBDisbled",        # yes, typo'd in the real bridge — match it verbatim
    b"checkDebuggerOption",
    b"isDevEnabled",
    b"isADBEnabled",
]

# --- message template patterns -------------------------------------------
MESSAGE_PATTERNS = [
    rb"[ -~]{12,200}Detected by App[ -~]{0,80}",
    rb"[ -~]{12,200}unblock your access[ -~]{0,80}",
    rb"[ -~]{12,200}Developer Mode[ -~]{0,120}",
    rb"[ -~]{12,200}at risk of being hacked[ -~]{0,120}",
    rb"[ -~]{12,200}rooted device[ -~]{0,120}",
    rb"[ -~]{8,120}Keep Using[ -~]{0,80}",
    rb"[ -~]{8,120}Go to Settings[ -~]{0,80}",
    rb"[ -~]{8,120}REF:[ -~]{0,80}",
    rb"[ -~]{8,120}Magic bytes read failed[ -~]{0,120}",
]


def clean(b: bytes) -> str:
    s = b.decode("utf-8", "replace")
    return "".join(c if 32 <= ord(c) < 127 else "." for c in s)


def load_bytes(path: str) -> bytes:
    """Read the target as raw bytes; if it is an APK, concatenate the dex
    files and any RN bundle so the caller gets one searchable blob."""
    with open(path, "rb") as f:
        head = f.read(4)
    if head[:2] != b"PK":
        with open(path, "rb") as f:
            return f.read()

    blob = bytearray()
    with zipfile.ZipFile(path) as z:
        names = sorted(z.namelist())
        for n in names:
            if (n.startswith("classes") and n.endswith(".dex")) or \
               n.endswith("index.android.bundle") or \
               n.endswith("resources.arsc") or \
               n.endswith(".so"):
                try:
                    blob += z.read(n)
                except Exception:
                    pass
    if not blob:
        with open(path, "rb") as f:
            return f.read()
    return bytes(blob)


def cmd_fingerprints(data: bytes) -> None:
    print("=== detection SDK fingerprints ===")
    hits = 0
    for sdk, sigs in SDK_SIGNATURES.items():
        found = [s.decode(errors="replace") for s in sigs if s in data]
        if found:
            hits += 1
            print(f"  {sdk:14s} -> {', '.join(found)}")
    if not hits:
        print("  (none of the known SDK signatures found)")
        print("  -> likely home-grown; enumerate custom strings instead")

    # Second, independent gate: the app's own dev-options probe.
    probe = [s.decode(errors="replace") for s in APP_DEV_PROBE if s in data]
    print()
    print("=== app-side dev/adb probe (second gate) ===")
    if probe:
        print(f"  PRESENT -> {', '.join(probe)}")
        print("  NOTE: this is independent of the SDK above. Clearing the SDK")
        print("  signal does NOT clear this one — the app can still self-kill")
        print("  on development_settings_enabled / adb_enabled alone.")
    else:
        print("  (not found — app does not probe dev options on its own)")


def cmd_threats(data: bytes) -> None:
    names = set()
    for m in re.finditer(rb"[A-Z][A-Za-z0-9]{2,40}Detected", data):
        names.add(m.group().decode())
    for m in re.finditer(rb"Detected[A-Z][A-Za-z0-9]{2,40}", data):
        names.add(m.group().decode())
    for m in re.finditer(rb"[A-Z][A-Za-z0-9]{2,40}Threat", data):
        names.add(m.group().decode())
    good = sorted(n for n in names if re.fullmatch(r"[A-Za-z0-9]{4,64}", n))
    print("=== threat-event names ===")
    for n in good:
        print("  ", n)
    print(f"\ntotal: {len(good)}")
    if not good:
        print("(no CamelCase *Detected / *Threat tokens — "
              "the app may name events differently)")


def cmd_messages(data: bytes) -> None:
    seen = set()
    print("=== message templates ===")
    for pat in MESSAGE_PATTERNS:
        for m in re.finditer(pat, data):
            s = re.sub(r"\s+", " ", clean(m.group())).strip()
            if len(s) > 20 and s not in seen:
                seen.add(s)
                print("-", s[:220])
    if not seen:
        print("  (no message templates found)")


def cmd_signals(data: bytes) -> None:
    print("=== device-side signal strings present ===")
    any_hit = False
    for k in DEVICE_SIGNALS:
        n = data.count(k)
        if n:
            any_hit = True
            i = data.find(k)
            print(f"  {k.decode():28s} x{n:<4} ...{clean(data[max(0, i - 50):i + 90])[:140]}...")
    if not any_hit:
        print("  (none found)")


def cmd_context(data: bytes, needle: str) -> None:
    nb = needle.encode()
    i = data.find(nb)
    if i < 0:
        print(f"not found: {needle}")
        return
    print(f"=== context for {needle} @ 0x{i:x} ===")
    print(clean(data[max(0, i - 250):i + 250]))


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__)
        return 1
    cmd, path = sys.argv[1], sys.argv[2]
    try:
        data = load_bytes(path)
    except OSError as e:
        print(f"cannot read {path}: {e}", file=sys.stderr)
        return 2
    print(f"# input: {path}  ({len(data):,} bytes)\n")
    if cmd == "fingerprints":
        cmd_fingerprints(data)
    elif cmd == "threats":
        cmd_threats(data)
    elif cmd == "messages":
        cmd_messages(data)
    elif cmd == "signals":
        cmd_signals(data)
    elif cmd == "context" and len(sys.argv) > 3:
        cmd_context(data, sys.argv[3])
    else:
        print(__doc__)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
