# OnePlus Nord Buds 3r — pairing notes ([REDACTED_PII]'s device)

- BT device name seen during scan: **"OnePlus Nord Buds 3r"**.
- To pair to a NEW host: **forget on the current phone first** (Settings → Bluetooth →
  device → Forget). Then buds in case → close lid → wait 3s → open lid → **hold case button
  ~3-5s** until LED flashes rapidly. Pairing window ~2 min.
- If previously connected to **"PRIYA"** (user's phone, an OnePlus 12R), it stays bonded and
  is invisible to other hosts until forgotten there. This is the usual cause of "not able to
  connect."
- Common failure: `Failed to pair: org.bluez.Error.AuthenticationRejected` = buds left pairing
  mode before the pair command ran. Re-trigger pairing mode and pair immediately (use
  `scripts/bt_autopair.sh` which retries up to 8×).
- When writing a watcher, match on the exact buds MAC or the substring **"Nord Buds 3r"** — NOT
  just "OnePlus", or it will pair to the phone (OnePlus 12R) instead.
- Verify audio: `wpctl status` should show a `bluez` sink; `wpctl set-default <id>` to route
  output there. If only HSP/HFP appears, re-pair to force A2DP.
