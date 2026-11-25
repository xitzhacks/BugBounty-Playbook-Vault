#!/bin/bash
# bt_autopair.sh <match>  — match = MAC (e.g. 60:55:56:..) or name substring (e.g. "Buds 3r")
# Keeps a scan alive, waits for the device to appear, removes stale bond, re-pairs
# (up to 8 tries), connects, then registers the A2DP sink via wpctl set-default.
set -u
MATCH="$1"
[ -z "$MATCH" ] && { echo "usage: bt_autopair.sh <mac-or-name-substring>"; exit 1; }
LOG=/tmp/bt_autopair.log
echo "[pair] start $(date) match=$MATCH" > "$LOG"
bluetoothctl power on >>"$LOG" 2>&1
bluetoothctl agent KeyboardDisplay >>"$LOG" 2>&1
bluetoothctl default-agent >>"$LOG" 2>&1

# TIGHT-SESSION LOOP: detect + remove + trust + pair + connect in ONE bluetoothctl
# session per cycle. Splitting these into separate `bluetoothctl` invocations (detect
# in one call, pair in another) lets the buds drop out of pairing mode in the gap →
# AuthenticationRejected. Keep them together so pair lands the instant they're seen.
for i in $(seq 1 300); do
  # keep a scan alive in the background (tracked separately so it doesn't die with us)
  if ! pgrep -f "bluetoothctl scan on" >/dev/null; then
    ( setsid bluetoothctl scan on >>"$LOG" 2>&1 & )
  fi
  # one session: wait for device, then remove+trust+pair+connect with no gaps
  OUT=$(bluetoothctl 2>&1 <<EOF
devices
EOF
)
  LINE=$(echo "$OUT" | grep -i "$MATCH" | head -1)
  if [ -n "$LINE" ]; then
    MAC=$(echo "$LINE" | awk '{print $2}')
    NAME=$(echo "$LINE" | cut -d' ' -f3-)
    echo "[pair] found $MAC ($NAME) attempt $i" >>"$LOG"
    # single session: remove stale bond, trust, then pair (retry in-session), then connect
    for a in $(seq 1 8); do
      SESS=$(bluetoothctl 2>&1 <<EOF
remove $MAC
trust $MAC
pair $MAC
EOF
)
      echo "$SESS" >>"$LOG"
      if echo "$SESS" | grep -q "Pairing successful"; then
        echo "[pair] PAIRED try $a" >>"$LOG"
        bluetoothctl connect "$MAC" >>"$LOG" 2>&1
        break
      fi
      sleep 2
    done
    for j in $(seq 1 20); do
      if wpctl status 2>/dev/null | grep -qi "bluez"; then
        SINK=$(wpctl status 2>/dev/null | grep -i "bluez" | head -1 | awk -F. '{print $1}' | tr -d ' ')
        [ -n "$SINK" ] && wpctl set-default "$SINK" >>"$LOG" 2>&1
        echo "[pair] AUDIO SINK $SINK DEFAULT" >>"$LOG"
        echo "[pair] COMPLETE" >>"$LOG"
        exit 0
      fi
      sleep 2
    done
    echo "[pair] paired but no audio sink (HSP/HFP only? re-pair to force A2DP)" >>"$LOG"
    exit 0
  fi
  sleep 3
done
echo "[pair] timeout — device never appeared (check it is in pairing mode / forgotten on other host)" >>"$LOG"
