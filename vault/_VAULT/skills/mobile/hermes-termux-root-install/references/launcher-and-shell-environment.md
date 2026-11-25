# Launcher + shell environment for a Termux Hermes profile

The four fixes from §"Running the profile reliably", as copy-pasteable files.
Install them once and `godmode-open` works from any shell on the phone.

---

## 1. `~/.bashrc`

Restores the Termux environment and re-applies the DNS hosts mount. Without
this, `su` leaves `HOME=/data` and an empty `PREFIX`, and `hermes` is not found.

```sh
# Termux shell startup — restores the environment when you `su` into the app uid.
export HOME=/data/data/com.termux/files/home
export PREFIX=/data/data/com.termux/files/usr
export PATH=$PREFIX/bin:$PREFIX/sbin:$HOME/.local/bin:/system/bin:/system/xbin
export LD_LIBRARY_PATH=$PREFIX/lib
export TERM=xterm-256color

_termux_ensure_hosts() {
    local H=$PREFIX/var/lib/termux-hosts/hosts
    local TPID
    TPID=$(pidof com.termux 2>/dev/null | awk '{print $1}')
    [ -n "$TPID" ] || return 0
    nsenter -t "$TPID" -m -- cat /system/etc/hosts 2>/dev/null | grep -q "inference-api.nousresearch.com" && return 0
    nsenter -t "$TPID" -m -- mount -o bind "$H" /system/etc/hosts 2>/dev/null || true
}
_termux_ensure_hosts 2>/dev/null
unset -f _termux_ensure_hosts
```

## 2. `~/.profile`

```sh
if [ -f "$HOME/.bashrc" ]; then
    . "$HOME/.bashrc"
fi
```

## 3. `$PREFIX/etc/profile.d/zz-termux-env.sh`

Sourced by `$PREFIX/etc/profile` for bash login shells.

```sh
export HOME=/data/data/com.termux/files/home
export PREFIX=/data/data/com.termux/files/usr
export PATH=$PREFIX/bin:$PREFIX/sbin:$HOME/.local/bin:/system/bin:/system/xbin
export LD_LIBRARY_PATH=$PREFIX/lib
export TERM=xterm-256color
```

## 4. `$PREFIX/bin/hermes-shim`

A `/system/bin/sh` fallback that rebuilds the environment and execs the real
launcher. Works even when `HOME`, `PREFIX` and `PATH` are all stripped — which
is exactly the state a bare `su` leaves behind. This is the direct fix for
"bundled interpreter missing".

```sh
#!/system/bin/sh
: "${HOME:=/data/data/com.termux/files/home}"
export HOME
export PREFIX=/data/data/com.termux/files/usr
export PATH=$PREFIX/bin:$PREFIX/sbin:$HOME/.local/bin:/system/bin:/system/xbin
export LD_LIBRARY_PATH=$PREFIX/lib
export TERM=xterm-256color

H=$PREFIX/var/lib/termux-hosts/hosts
TPID=$(pidof com.termux 2>/dev/null | awk '{print $1}')
if [ -n "$TPID" ] && [ -f "$H" ]; then
    nsenter -t "$TPID" -m -- cat /system/etc/hosts 2>/dev/null | grep -q "inference-api.nousresearch.com" || \
        nsenter -t "$TPID" -m -- mount -o bind "$H" /system/etc/hosts 2>/dev/null
fi

exec "$PREFIX/lib/hermes-agent/bin/hermes" "$@"
```

## 5. `$PREFIX/bin/godmode-open` — the one-command launcher

Handles namespace entry, DNS mount, uid drop, and `--yolo` in one shot.
**This is the command to give the user.**

```sh
#!/data/data/com.termux/files/usr/bin/bash
# godmode-open — launch the godmode Hermes profile from anywhere on the phone.
#   godmode-open                 # interactive chat
#   godmode-open "your prompt"   # single-shot query
#   godmode-open -f file.txt     # query from a file
#   godmode-open -h              # help
set -euo pipefail

PREFIX=/data/data/com.termux/files/usr
export HOME=/data/data/com.termux/files/home
export PREFIX
export PATH=$PREFIX/bin:$PREFIX/sbin:/system/bin:/system/xbin
export LD_LIBRARY_PATH=$PREFIX/lib

# Locate a Termux process to borrow its mount namespace.
TPID=""
for attempt in $(seq 1 20); do
    TPID=$(pidof com.termux 2>/dev/null | awk '{print $1}')
    [ -n "$TPID" ] && break
    sleep 1
done
if [ -z "$TPID" ]; then
    echo "godmode-open: Termux is not running."
    echo "Start Termux first (tap the app), then run godmode-open again."
    exit 1
fi

# (Re)apply the DNS hosts bind-mount if it drifted.
ensure_dns() {
    local H=$PREFIX/var/lib/termux-hosts/hosts
    if [ ! -f "$H" ]; then
        mkdir -p "$PREFIX/var/lib/termux-hosts"
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
    fi
    nsenter -t "$TPID" -m -- cat /system/etc/hosts 2>/dev/null | grep -q "inference-api.nousresearch.com" && return 0
    nsenter -t "$TPID" -m -- mount -o bind "$H" /system/etc/hosts 2>/dev/null || true
}
ensure_dns

GOD_HOME=$HOME/.hermes/profiles/godmode
[ -d "$GOD_HOME" ] || { echo "godmode-open: profile not found at $GOD_HOME"; exit 1; }

cd "$HOME"
ENVP="HOME=$HOME PREFIX=$PREFIX PATH=$HOME/.local/bin:$PATH LD_LIBRARY_PATH=$LD_LIBRARY_PATH"

if [ $# -eq 0 ]; then
    exec nsenter -t "$TPID" -m -- setpriv --reuid=10313 --regid=10313 --clear-groups \
        env HOME="$HOME" PREFIX="$PREFIX" \
        PATH="$HOME/.local/bin:$PATH" LD_LIBRARY_PATH="$LD_LIBRARY_PATH" \
        godmode chat --yolo
elif [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
    sed -n '2,12p' "$0"
elif [ "$1" = "-f" ]; then
    [ $# -ge 2 ] || { echo "usage: godmode-open -f <file>"; exit 1; }
    exec nsenter -t "$TPID" -m -- setpriv --reuid=10313 --regid=10313 --clear-groups \
        env HOME="$HOME" PREFIX="$PREFIX" \
        PATH="$HOME/.local/bin:$PATH" LD_LIBRARY_PATH="$LD_LIBRARY_PATH" \
        godmode chat --oneshot --yolo --query-file "$2"
else
    exec nsenter -t "$TPID" -m -- setpriv --reuid=10313 --regid=10313 --clear-groups \
        env HOME="$HOME" PREFIX="$PREFIX" \
        PATH="$HOME/.local/bin:$PATH" LD_LIBRARY_PATH="$LD_LIBRARY_PATH" \
        godmode chat --oneshot --yolo -q "$*"
fi
```

**Gotchas when writing this script:**
- `PATH` inside the dropped-privilege `env` **must include `$HOME/.local/bin`**
  or the `godmode` wrapper is not found (`env: 'godmode': No such file or
  directory`). This is the single most common launcher bug.
- `setpriv --reuid/--regid/--clear-groups` is what drops from root to the app
  uid while keeping the namespace. `su 10313 -c` also works but re-runs shell
  init.
- Termux may not be running when the user tries this. Poll `pidof com.termux`
  briefly, then say so plainly instead of hanging.

## 6. Install order

```bash
adb push bashrc /data/local/tmp/ ; adb push profile /data/local/tmp/
adb push zz-termux-env.sh /data/local/tmp/ ; adb push hermes-shim /data/local/tmp/
adb push godmode-open /data/local/tmp/

adb shell "su 10313 -c '
  cp /data/local/tmp/bashrc   \$HOME/.bashrc
  cp /data/local/tmp/profile  \$HOME/.profile
  install -m 644 /data/local/tmp/zz-termux-env.sh \$PREFIX/etc/profile.d/
  install -m 755 /data/local/tmp/hermes-shim    \$PREFIX/bin/
  install -m 755 /data/local/tmp/godmode-open   \$PREFIX/bin/
  chmod 644 \$HOME/.bashrc \$HOME/.profile
'"
```

## 7. Verify each layer

```bash
# shell env restored
adb shell "su 10313 -c 'source \$HOME/.bashrc; echo \$PREFIX; which hermes'"

# login bash path
adb shell "su 10313 -c '\$PREFIX/bin/bash -lc \"which hermes; hermes --version\"'"

# stripped-env shim
adb shell "su 10313 -c 'unset HOME PREFIX PATH LD_LIBRARY_PATH; export HOME=/data; \
  \$PREFIX/bin/hermes-shim --version'"

# full launcher with a real query
adb shell "su -c 'export HOME=/data/data/com.termux/files/home PREFIX=/data/data/com.termux/files/usr; \
  export PATH=\$PREFIX/bin:/system/bin; cd \$HOME; \
  godmode-open \"echo OPEN_OK; id; how many skills?\"'"
```

Expect the launcher to return the profile's identity, a real skill count, and
`OPEN_OK` from the shell — not a claim that it ran.

## 8. Why the DNS mount alone was never enough

Sequence of mistakes that cost real time, so you can skip them:

1. Applied the bind-mount from a `su 10313 -c` shell → mount landed in init's
   namespace → Hermes still could not resolve.
2. Verified with `cat /system/etc/hosts` from that same shell → looked correct →
   concluded the mount was fine.
3. Only after checking `readlink /proc/<pid>/ns/mnt` did the namespace mismatch
   become visible.

Rule: **always compare namespaces**, never infer from file contents.

## 9. Hosts file must list every hostname Hermes touches

Minimal files (only `inference-api`) are not enough. Missing hosts surface as
`gaierror(7)` on unrelated-looking calls. Include at least:

```
inference-api.nousresearch.com   (the API)
hermes-assets.nousresearch.com   (updates, assets)
portal.nousresearch.com          (auth refresh)
models.dev                       (model metadata)
api.github.com, github.com       (skills/source fetches)
```

Resolve the IPv4 addresses from the **host** (which has working DNS) with
`getent ahostsv4 <host>`, then push the file. Cloudflare-fronted hosts return
 rotating addresses; pin two each.
