# Driving an On-Device Hermes Session over adb

How to run a real work session on the phone through a Termux Hermes profile,
instead of using the laptop. The user explicitly wants on-device work for
mobile engagements ("do this only using Termux, not this laptop").

## 1. Write the brief to the device, not inline on the command line

Long prompts passed inline through `adb shell "su 10313 -c '... -q \"$(cat ...)\"'"`
get mangled by nested quoting and by `su` argument handling. Put the brief in
a file and pass the file:

```bash
adb push brief.md /data/local/tmp/brief.md
adb shell "su 10313 -c 'cp /data/local/tmp/brief.md \$HOME/brief.md'"
adb shell "su 10313 -c 'export HOME=/data/data/com.termux/files/home PREFIX=/data/data/com.termux/files/usr; \
  export PATH=\$HOME/.local/bin:\$PREFIX/bin:\$PREFIX/sbin:/system/bin:/system/xbin; \
  export LD_LIBRARY_PATH=\$PREFIX/lib; cd \$HOME; \
  timeout 3000 godmode chat --oneshot --max-turns 60 -q \"\$(cat \$HOME/brief.md)\"'"
```

`--oneshot` implies exit after one answer; `--max-turns` bounds the agent loop.
There is no `--no-stream`.

## 2. Budget the run, and run it in the background

Exploit-generation and multi-tool turns regularly exceed 240s. Two failure
modes seen in practice:

- A local `timeout 240` kills the agent mid-tool-call and leaves a
  `KeyboardInterrupt` traceback that looks like a Hermes crash. It is not.
- Running it in the foreground blocks the session and you lose visibility.

Use `terminal(background=true, notify_on_complete=true)` with
`timeout 3000` and `--max-turns 60`, then `process(action='poll')` for
progress. The agent streams its reasoning, so the poll preview is genuinely
useful for steering.

## 3. Scope the agent's access deliberately

The profile has the full toolset. For a device-local engagement the useful
toolsets are `terminal`, `file`, and `delegation` — browser and computer_use
point at the laptop, not the phone, and will waste turns.

If the run needs to change device state (settings, pm, mounts), say so in the
brief and tell it explicitly what NOT to touch. In this engagement the brief
carried:

```
Do NOT touch /data/adb/service.d/termux-dns.sh or sitecustomize.py —
those are load-bearing for Hermes itself.
```

That guard matters: the agent has root and will happily "clean up" the very
DNS shim that keeps it online.

## 4. The device is the artifact store

The agent writes its own analysis/evidence trees under `~/Bugbounty/<target>/`
on the phone. Pull them back only when they are the deliverable — the brief
should ask for a final report the agent writes to a known path, then pull that
one file:

```bash
adb shell "su 10313 -c 'cat \$HOME/Bugbounty/<target>/reports/<file>.md'" > local.md
```

## 5. Transport reality

Wireless adb (`adb connect <phone-ip>:5555`) is the fallback when the USB
cable drops — and the cable does drop on this device. It worked for ~30 min
then adbd stopped accepting connections while the phone still pinged.

Symptoms and the honest response:
- `adb devices` empty + `lsusb` shows no Samsung  -> cable/physical link
- phone pings but `adb connect` says "Connection refused" -> adbd is dead;
  retrying in a loop does not help
- `adb` reports `device offline` -> `adb disconnect` then reconnect once

Do not retry the connection in a tight loop. Say the transport is dead, then
keep working on whatever was already pulled (the APK, the smali, the analysis)
so the engagement still moves. Reconnection is a user action.

### 5.1 USB enumerates MTP-only — recover ADB over the modem serial port

A Samsung phone plugged in but showing only `MTP mode` still exposes a **CDC ACM
serial port**. That port answers AT commands, and one of them enables the ADB
USB interface. This is the recovery path when `adb devices` is empty but the
device is physically present:

```bash
# 1. confirm what USB exposes (expect MTP + CDC ACM, NO "ADB Interface")
lsusb -d 04e8:6860 -v | grep -iE "iInterface"

# 2. find the serial device (class 02 = CDC ACM)
ls /dev/ttyACM*

# 3. prove the AT channel is alive
timeout 8 bash -c 'exec 3<>/dev/ttyACM0; stty -F /dev/ttyACM0 raw -echo; \
  printf "AT\r" >&3; timeout 3 cat <&3'
# -> "\r\nOK\r\n" means the modem channel is usable

# 4. Samsung USB-debug enable code -> enumerates the ADB interface
timeout 15 bash -c 'exec 3<>/dev/ttyACM0; stty -F /dev/ttyACM0 raw -echo; \
  printf "ATD#19732864#\r" >&3; timeout 3 cat <&3'
# -> "+USBDEBUG:1,NG_NONE  OK"

# 5. confirm the ADB interface appeared, then use it
lsusb -d 04e8:6860 -v | grep -i "ADB Interface"
adb kill-server; adb start-server; adb devices -l
```

Notes that make this work:
- `ATD#19732864#` is the Samsung USB-debug code; the reply
  `+USBDEBUG:<n>,NG_NONE OK` confirms the toggle.
- A `usbreset <VID:PID>` afterwards is sometimes needed to force re-enumeration.
- Many other candidate codes (`AT+USBMODE=*`, `ATD#72xx#`, `AT+DEVCON`) return
  `+CME Error:PACM(AP),UNREGISTERED` on this port — only the USBDEBUG family is
  permitted. Do not keep guessing; one working code is enough.
- **This path is one-way for a fatal setting**: if `adb_enabled` has already been
  set to 0, `ATD#19732864#` still reports success but the ADB interface does NOT
  re-enumerate, because the framework has adbd disabled. See §5.2.

### 5.2 Never disable the transport you are running on

`settings put global adb_enabled 0` tears down the ADB interface immediately —
including the USB interface you are driving the session through. This happened
in a real engagement and locked the device out for the rest of the run.

If it happens:
- `ATD#19732864#` / `AT+USBDEBUG` will **lie** (report OK, no interface).
- `usbreset` + unbind/rebind re-enumerates to MTP+CDC only.
- Wireless adb is also down, so there is no scripted second path.

Recovery is a **physical user action**: unplug/replug the cable, unlock the
phone, then toggle USB debugging OFF→ON in Settings → Developer options. Say so
plainly and stop retrying; do not burn the session on connection loops.

Rule: any script that runs over a live adb session must clear
`development_settings_enabled` (what the app actually reads) and must **never**
set `adb_enabled`.
