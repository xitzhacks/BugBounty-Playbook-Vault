---
name: hermes-termux-root-install
description: Install Hermes Agent into Termux on a rooted Android when the bundled install-hermes-termux.sh fails (non-debuggable/Play Store Termux, broken app-uid DNS). Offline deb push + dpkg as the Termux uid.
tags: [hermes, termux, android, magisk, install, adb]
---

# Hermes Agent → Termux over root (offline deb path)

Use when `./install-hermes-termux.sh` fails on a device that is rooted but whose
Termux is **not debuggable** (`run-as: package not debuggable`) — typically a
Play Store Termux (`versionName=googleplay.*`). The script's `run-as` runner is
dead, and on many ROMs the app uid also has **broken DNS** while root resolves
fine, so apt inside the app cannot fetch the repo either.

## Diagnosis (30 seconds)

```
adb shell run-as com.termux id          # -> "package not debuggable"
adb shell su -c id                       # -> uid=0(root) ... context=u:r:magisk:s0
adb shell 'su -c "ping -c 1 -W 3 hermes-assets.nousresearch.com"'   # works
adb shell 'su 10313 -c "ping -c 1 -W 3 hermes-assets.nousresearch.com"'  # unknown host
adb shell dumpsys package com.termux | grep versionName   # googleplay.* = Play build
```

Play Store Termux also **lacks `$PREFIX/etc/apt/keyrings/`** support — the
script's `signed-by=$PREFIX/etc/apt/keyrings/...` line is silently ignored, so
use `[trusted=yes]` or `trusted.gpg.d` instead.

## Fix: install offline from the host

The .deb is self-contained (bundled python 3.14 + node + venv), so no network is
needed on the phone at all.

```bash
# 1. resolve the live version + size from the repo (host)
curl -fsSL https://hermes-assets.nousresearch.com/releases/termux/canary/dists/hermes-canary/main/binary-aarch64/Packages \
  | grep -E '^(Version|Size|Filename):'

# 2. download + verify size against the Packages stanza
curl -fL -o hermes-agent.deb \
  https://hermes-assets.nousresearch.com/releases/termux/canary/pool/h/<Filename>

# 3. push and install AS THE TERMUX UID (dpkg cannot run as root)
adb push hermes-agent.deb /data/local/tmp/hermes-agent.deb
adb shell 'su -c "chmod 644 /data/local/tmp/hermes-agent.deb"'
P=/data/data/com.termux/files/usr
adb shell "su 10313 -c 'export HOME=/data/data/com.termux/files/home PREFIX=$P PATH=$P/bin:/system/bin LD_LIBRARY_PATH=$P/lib; $P/bin/dpkg -i /data/local/tmp/hermes-agent.deb'"

# 4. verify
adb shell "su 10313 -c 'export HOME=/data/data/com.termux/files/home PREFIX=$P PATH=$P/bin:/system/bin LD_LIBRARY_PATH=$P/lib; hermes --version'"
```

## Pitfalls

- **Never run `apt-get`/`dpkg` as root inside Termux.** Termux's apt prints
  `Ability to run this command as root has been disabled permanently for safety
  purposes.` and exits 0 — which looks like success and is not. Always
  `su <termux-uid> -c '...'`.
- **`su 10313 -c "sh script.sh"` works; `su 0 sh -c '...'` does not** on this
  Magisk build (`/system/bin/sh: sh: No such file or directory` — PATH is not
  set up for the `su 0 <cmd>` form). Use `su -c "cmd"` for root one-liners.
- **Ownership/labels need no repair when dpkg runs as the app uid.** Files land
  as `u0_a313:u0_a313` with `u:object_r:app_data_file:s0` by construction. Only
  run a `chown`/`chcon` pass if you extracted the payload as root.
- **`/system/etc/hosts` is read-only** and a bind-mount over it is the only
  in-place fix for app-uid DNS. Prefer the offline deb path — it sidesteps DNS
  entirely.
- **Termux uid** is not fixed: get it with
  `adb shell pm list packages -U com.termux | sed -n 's/.*uid:\([0-9]*\).*/\1/p'`.
- **Cleanup:** remove `/data/local/tmp/hermes-agent.deb` (173 MB) after install.

## When the user asks to "just open it" / "make it work when I type hermes"

Deliver ONE command, not a procedure. The user repeatedly asked for exactly
this ("open it and let me know command to open", "make it work when i type
hermes"). Build the launcher (`godmode-open`) and lead with it, then list the
short variants. Do not answer with a namespace explanation first — give the
command, then the one-line explanation.

Preferred response shape:
```
godmode-open              # interactive
godmode-open "prompt"     # one-shot
godmode-open -f q.txt     # from a file
```
Then, only if asked, the details. Report status in plain language and state
what you verified (real output, not "should work").

## Post-install

No provider is configured, so `hermes` offers the setup wizard on every launch
until one is set:

```bash
hermes setup model          # interactive, on the phone
# or non-interactive against an OpenAI-compatible endpoint:
hermes config set providers.mine.api "http://<host>:11434/v1"
hermes config set providers.mine.name "mine"
hermes config set providers.mine.default_model "<model>"
hermes config set providers.mine.key_env "MY_API_KEY"
hermes config set model.provider "custom:mine"
hermes config set model.default "<model>"
echo 'MY_API_KEY=...' >> ~/.hermes/.env
```

`key_env` (not `api_key`) is the credential pointer; the key lives in
`~/.hermes/.env`.

**Always export `HOME` when driving hermes over adb**, or it reads
`/data/user/0/com.termux/.hermes` instead of `files/home/.hermes` and looks
unconfigured forever.

**Building a custom profile + persona** (e.g. a named operator profile with
SOUL.md + system-prompt overlay + prefill): see references/custom-profile-persona.md
for the exact keys (`agent.system_prompt`, `prefill_messages_file`), the
`-p`-scoped skill-install ordering trap, and how to verify the persona actually
loaded with a canary prompt instead of trusting config values.

**Running a real work session on the phone through that profile** (driving a
Termux Hermes profile over adb, backgrounding long runs, scoping its tools,
the transport-failover dance): see references/on-device-session-over-adb.md.

**Making the profile launchable from any shell on the phone** (the `godmode-open`
launcher, `~/.bashrc` / `.profile` / `profile.d` / `hermes-shim` environment
fixes, and the namespace + DNS + approvals + vision failure modes that make a
perfectly configured profile fail at launch): see
references/launcher-and-shell-environment.md. Start there when the user says
"hermes is not working" or "bundled interpreter missing".

**If the device is plugged in but `adb devices` is empty** (USB enumerates
MTP+CDC ACM only): the phone's modem serial port answers AT commands and
`ATD#19732864#` enables the ADB USB interface. Full recipe in
references/on-device-session-over-adb.md §5.1. Do NOT, however, use
`settings put global adb_enabled 0` to clear an app's dev-mode check while you
are driving the session over adb — that tears down the interface and the AT
channel cannot bring it back (§5.2).

## Post-install gotchas on Termux (verified 2026-11-07, v0.22.0 canary)

### 1. `dpkg -i` fails as the app uid unless `$PREFIX/sbin` is on PATH
`dpkg` warns `2 expected programs not found` (`dpkg-deb`,
`start-stop-daemon`). Export
`PATH=$PREFIX/bin:$PREFIX/sbin:/system/bin:/system/xbin` before running it.
Root's own PATH is missing `$PREFIX/sbin`; `$PREFIX/bin` alone is not enough.

### 2. Root cannot `chown`/`chmod` inside `/data/data/com.termux`
`su -c "chown u0_a313 file"` fails with Permission denied even as uid 0
(Magisk's sandboxed root). Always write files **as the app uid**:
`su 10313 -c 'cp /data/local/tmp/x dest'`. The one exception is creating
directories in `/data/adb` (Magisk tree) — that is root-owned and fine.

### 3. App-uid DNS is dead → Hermes cannot reach the API
`dumpsys netd` shows the Termux uid in the **SYSTEM** network-permission group,
not **NETWORK**, so netd never answers its DNS. Raw IP works (`curl
--resolve` → 200), `ping <host>` fails, `ping 8.8.8.8` works. `getprop` shows no
DNS entries at all — this is a permission-class issue, not a resolver config.

Fix without touching app code: bind-mount a hosts file **into Termux's own
mount namespace** (never a global mount — that breaks every other app's DNS).
The file must list **every** hostname Hermes touches, not just the API host —
see references/launcher-and-shell-environment.md §9:

```bash
H=$PREFIX/var/lib/termux-hosts/hosts
mkdir -p "$(dirname "$H")"
printf '%s\n' \
  '127.0.0.1       localhost' \
  '::1             ip6-localhost' \
  '104.18.0.79     inference-api.nousresearch.com' \
  '104.18.1.79     inference-api.nousresearch.com' \
  '104.18.0.79     hermes-assets.nousresearch.com' \
  '104.18.1.79     hermes-assets.nousresearch.com' \
  '66.33.60.193    portal.nousresearch.com' \
  '104.21.51.36    models.dev' \
  '172.67.220.122  models.dev' \
  '20.207.73.85    api.github.com' \
  '140.82.121.6    api.github.com' \
  '140.82.112.3    github.com' \
  > "$H"
chmod 644 "$H"
```

Apply it **inside Termux's namespace** — this is the step that is easy to get
wrong, because a shell started with `su 10313 -c` is in init's namespace:

```bash
TPID=$(pidof com.termux | awk '{print $1}')
su -c "nsenter -t $TPID -m -- mount -o bind $H /system/etc/hosts"
```

Verify scoping with `readlink /proc/<pid>/ns/mnt` — Termux's ns must differ from
init's (`/proc/1/ns/mnt`) and from other apps'. **Comparing namespaces is the
only reliable check**; `cat /system/etc/hosts` from the wrong namespace looks
identical and will mislead you.

Persist across reboots with a Magisk `/data/adb/service.d/termux-dns.sh` that
`nsenter -t $(pidof com.termux) -m -- mount -o bind ...` (idempotent, grep the
hosts file first). Termux may not be running at boot, so poll `pidof com.termux`
for up to ~2 min. A boot wipes the mount, so also re-apply it on every launch
from `~/.bashrc` and from the launcher (§Running the profile reliably).

### 4. Skills all hidden: `sys.platform == "android"` gates them out
On Termux, CPython reports `sys.platform == "android"`, and the bundled skills
declare `platforms: [linux, macos, windows]`. `skill_matches_platform_list`
(agent/skill_utils.py) therefore filters out **every** skill: `skills_list`
returns `{"skills": [], "message": "No skills found in skills/ directory."}`
even though 59 SKILL.md files are on disk. `HERMES_PLATFORM` does **not** help
(only the `environments:` gate reads it).

Fix with a venv `sitecustomize.py` — no app-code edits, no per-skill edits:

```python
# $PREFIX/lib/hermes-agent/venv/lib/python3.14/site-packages/sitecustomize.py
import sys
if sys.platform == "android":
    sys.platform = "linux"
```

Result: 0 → 54 skills visible. Leave `platform.system()` alone (Hermes uses it
only for display strings).

### 5. Bundled skills land in the root home, not the new profile
`hermes skills install ...` run without `-p` installs into
`~/.hermes/skills/` (the `default` profile). For a named profile, run
`hermes -p <name> skills install ...`, or the new profile gets 0 skills.

### 6. `--yolo` / sandbox-free CLI for unattended runs
Non-interactive over adb: `hermes -p <profile> chat --oneshot -q "..."`.
`--no-stream` does not exist; `--oneshot` implies exit after one answer. Long
exploit-generation turns can exceed 240s — budget 560s+ and pass
`--max-turns 12`, or your local `timeout` will kill it mid-tool-call with a
KeyboardInterrupt traceback that looks like a Hermes crash.

**Two things that silently zero out your results, and the exact fix:**

1. **Commands get BLOCKED.** `-q` runs with no user present, so Hermes refuses
   anything its danger heuristic flags (`BLOCKED: Command flagged as
   dangerous`). Fix in the profile config: `approvals: {mode: off}` plus
   `--yolo` on the command line. Without this the agent reports success and
   runs nothing.
2. **Vision returns 404.** The aux vision model defaults to a PAID model
   (`google/gemini-3.6-flash`) that free accounts cannot use. Fix:
   `auxiliary.vision` pinned to a free model (see
   references/launcher-and-shell-environment.md for the YAML).

Both are profile-config changes, not app-code changes. Check them before
concluding the profile is broken.

**Debugging rule that saves the most time:** when a network call fails inside
Hermes but works from your shell, compare mount namespaces first
(`readlink /proc/<pid>/ns/mnt`), not DNS. A shell started with
`su 10313 -c` is in init's namespace while Termux is in its own, so a hosts
bind-mount can be perfectly applied and still invisible to Hermes.

## Running the profile reliably (the four things that silently break it)

A profile can be perfectly configured and still fail at launch. These are the
four failure modes seen in practice, in the order they bite. Full recipes and
the ready-to-install launcher script are in
**references/launcher-and-shell-environment.md**.

### A. Hermes must RUN inside Termux's mount namespace

Binding the hosts file is necessary but **not sufficient**. The Hermes process
must be spawned **inside Termux's own mount namespace**, or it resolves nothing
even though `cat /system/etc/hosts` looks correct from your shell.

```bash
readlink /proc/1/ns/mnt                 # init:    mnt:[4026534109]
readlink /proc/$(pidof com.termux)/ns/mnt   # termux: mnt:[4026534508]
```

A shell started with `su 10313 -c '...'` lands in **init's** namespace. Every
Hermes launch from there dies with `[Errno 7] No address associated with
hostname`, while a plain `curl` from the same shell works — which makes it look
like a DNS problem rather than a namespace problem. Launch instead with:

```bash
su -c 'nsenter -t $(pidof com.termux) -m -- su 10313 -c "godmode chat ..."'
```

### B. Terminal commands are BLOCKED in single-query mode

`hermes ... chat --oneshot -q "..."` runs with **no user present to approve**,
so Hermes refuses anything its danger heuristic flags:

```
BLOCKED: Command flagged as dangerous (script execution via -e/-c flag)
but single-query mode (-q) runs without a user present to approve it.
```

This silently kills most real work. Two fixes, both needed:

```yaml
# <profile>/config.yaml
approvals:
  mode: off          # canonical bypass: yolo OR session-yolo OR mode=off
terminal:
  timeout: 600       # long scans exceed the default
```

and pass `--yolo` on the command line. `approvals.mode: off` is the one that
works for unattended/adb-driven runs; `--yolo` alone is process-scoped and
frozen at import.

### C. Vision fails with a paid-model 404

The aux vision model defaults to `google/gemini-3.6-flash`, which needs credits.
On a free account every `vision_analyze` returns:

```
404 - Model 'google/gemini-3.6-flash' requires available credits.
```

Pin it to a free model:

```yaml
auxiliary:
  vision:
    provider: nous
    base_url: https://inference-api.nousresearch.com/v1
    model: meituan/longcat-2.5:free
    download_timeout: 30
```

### D. `su` shells lose the Termux environment

Typing `hermes` after `su` gives **"bundled interpreter missing"** (or
`hermes: inaccessible or not found`) even though the install is fine. Cause:
`su` starts `/system/bin/sh`, which sources nothing, so `HOME=/data`,
`PREFIX` is empty, and `PATH` has no Termux dirs. The launcher then cannot find
its own bundled python.

Fix with three small files (see the reference for exact contents):

| File | Purpose |
|---|---|
| `~/.bashrc` | restores HOME/PREFIX/PATH/LD_LIBRARY_PATH; re-applies the DNS mount |
| `~/.profile` | sources `.bashrc` for login shells |
| `$PREFIX/etc/profile.d/zz-termux-env.sh` | env for bash login shells |
| `$PREFIX/bin/hermes-shim` | `/system/bin/sh` fallback that works with a fully stripped env |

Then either `bash -lc 'hermes ...'` or just use the launcher:

```
godmode-open                 # interactive
godmode-open "prompt"        # one-shot
godmode-open -f query.txt    # from a file
```

## Transport failover: USB dies mid-session → wireless adb

A USB cable can drop at any time (physically absent from `lsusb`, not just an
adb-server glitch). The phone is usually still on the LAN. Fail over instead of
stopping:

```bash
adb devices -l                     # empty / offline
lsusb | grep -iE '04e8|samsung'    # confirms the CABLE is gone, not adb
ping -c 2 <phone-ip>               # is the device alive?
adb connect <phone-ip>:5555        # wireless adb (needs it enabled once)
```

Once connected, use the TCP transport id everywhere (`adb -s 192.168.1.6:5555
shell ...`) — serial-numbered USB ids stop working. Wireless adb is enough for
the full workflow: root shell, su, APK pull, screencap, logcat.

If wireless adb later stops accepting (`Connection refused` while `ping` still
works), adbd has died or been toggled — that needs a physical action on the
phone. Report it as a hard blocker rather than retrying in a loop; the remaining
work can be done from artifacts already pulled to the laptop.
