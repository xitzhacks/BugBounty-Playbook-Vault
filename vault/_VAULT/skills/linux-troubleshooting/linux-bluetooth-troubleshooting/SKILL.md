---
name: linux-bluetooth-troubleshooting
description: Diagnose and fix Linux Bluetooth audio device pairing/connection failures (headsets, earbuds). Use when a BT device won't connect, won't pair, or pairs but has no audio. Covers the common "bonded to another device" trap, pairing-mode entry, and PipeWire/wireplumber A2DP sink setup. Applies to Parrot/Kali/Debian with bluez + PipeWire.
---

## First-pass diagnosis (run in parallel)
- `systemctl status bluetooth.service` — must be `active (running)`
- `rfkill list` — adapter not `soft blocked` / `hard blocked`
- `hciconfig` — adapter shows `UP RUNNING PSCAN`
- `systemctl --user status pipewire pipewire-pulse wireplumber` — audio daemons active
- `bluetoothctl devices` — what's already paired/known
- `bluetoothctl show` — controller `Powered: yes`

If adapter is up and daemons run but the device "won't connect", ~95% of cases are
**bonding/pairing-state**, not drivers.

## The #1 trap: device bonded to another host
A headset/earbud already paired to a phone (or other laptop) will **not advertise** to a new
host. Symptom: scans find other devices (the phone, Airdopes, etc.) but never the target buds.
Fix: **Forget the device on the OTHER host first** (phone Bluetooth → device → Forget). Only
then will it enter discoverable/pairing mode. This is the single most common "won't connect"
root cause.

## Entering pairing mode
- **Earbuds in case:** close lid → wait 3s → open lid → **hold case button ~3-5s** until LED
  flashes rapidly (white/blue). A single blink on open = "connected to phone" mode, NOT pairing.
- Some devices: hold power button 5-10s until LED flashes.
The pairing window is short (~2 min). Run the auto-pair script (below) so it catches them on
sight instead of racing the window manually.

## Auto-pair script
`scripts/bt_autopair.sh <MAC-or-name-substring>`. It keeps a scan alive, waits for the device
to appear, removes any stale bond, re-pairs (up to 8 tries), connects, then registers the A2DP
sink via `wpctl set-default`. Usage: `bash scripts/bt_autopair.sh "Buds 3r"` or the MAC.

## Verify audio sink
After connect: `wpctl status` should show a `bluez` sink under **Audio → Sinks**. Set default:
`wpctl set-default <sink-id>`. If no bluez sink appears, the profile may be HSP/HFP (call audio)
only — force A2DP by re-pairing or via `wpctl`/`pavucontrol`. A device stuck in HSP has
"connected but no/mono audio".

## Diagnose the ACTUAL failure reason (user asked "find the reason it failed")
When the user wants root-cause, not just a working pair, capture the precise bluez error.
Workflow:
1. Confirm the device is advertising NOW: `timeout 12 bluetoothctl scan on | grep -i '<name>'`.
   If NOTHING appears → it's still bonded to another host (see #1 trap) or not in pairing mode.
2. If it appears, attempt connect and capture the raw error: `bluetoothctl connect <MAC> 2>&1`.
   Map the error to cause:
   - `org.bluez.Error.Failed br-connection-refused` / `Failed to connect` with no pairing →
     device not paired (or bond still cached on one side). Run `remove` + `pair` + `connect`.
   - `org.bluez.Error.AuthenticationRejected` / `ConnectionAttemptFailed` → the buds left pairing
     mode before the pair call landed (window ~60–120s). Re-trigger pairing mode, pair immediately.
   - `Paired: yes` but no audio / no `bluez` sink in `wpctl status` → A2DP profile didn't
     register; re-pair, or force A2DP via `wpctl`/`pavucontrol` (device stuck in HSP/HFP).
   - `Connected: yes` then drops → weak signal, or phone re-grabbed the bond. Forget on phone again.
3. Dump full detail for the report: `bluetoothctl info <MAC>` (Name/Paired/Connected/UUIDs/Blocked).

## Pitfalls
- `bluetoothctl pair` → `AuthenticationRejected` = pairing window on the device timed out.
  Re-trigger pairing mode and pair immediately (the script retries).
- **Pairer race condition (seen this session):** a loop that does `bluetoothctl info` (detect),
  then separately `remove` + `trust` + `pair` + `connect` as independent calls, with sleeps
  between them, will hit `AuthenticationRejected` because the buds drop out of pairing mode in
  the gap. **Fix:** do scan + remove + trust + pair + connect in a SINGLE `bluetoothctl` session
  per cycle (pipe the commands in), with no gaps, retrying the whole cycle. The tight loop in
  `scripts/bt_autopair.sh` should already do this — verify it does NOT split detect and pair into
  separate invocations.
- **Broad `pkill` self-kill (seen this session):** `pkill -f bt_pair` / `pkill -f 'bluetoothctl scan'`
  matches the AGENT's own shell wrapper process (the command string contains those words) and
  SIGTERMs the shell → command returns `exit_code -15`. Use targeted PIDs from `pgrep` instead,
  or kill only the specific session via the process tool. Never `pkill -f` a pattern that also
  appears in the command you're running.
- A watcher that matches a broad keyword (e.g. "OnePlus") will grab the WRONG device (the
  phone) instead of the buds. Match on the exact buds MAC or a unique name substring.
- Run scans as a **tracked background process** (terminal `background=true`), not `nohup ... &`
  inside the agent shell wrapper — the wrapper can kill the subshell and the scan dies silently.
- `bluetoothctl` as non-root is fine if the user is in the `bluetooth` group (verify with `groups`).

## References
- `references/oneplus_buds_pairing.md` — OnePlus Nord Buds 3r specific quirks (this user's device).
