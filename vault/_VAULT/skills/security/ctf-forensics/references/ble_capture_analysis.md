# BLE / OTA Capture CTF Analysis (condensed)

## Capture shape (synthetic "csem-ble-sim" style seen in `silent_pairing`)
JSON with:
- `capture_format`, `note`, `target_hint` (often null), `packets[]`
- Packet types: PAIR_INIT, PAIR_ACK, OTA_CHUNK, ADV
- Each packet: `seq`, `type`, `timestamp`, `src`, `dst`, plus type-specific fields.

## Field roles
- Hub MAC = common source of PAIR_ACK and OTA_CHUNK (e.g. 85:F5:2A:F4:A1:11).
- PAIR_INIT (from device → hub): `nonce`
- PAIR_ACK (from hub → device): `ack_nonce`
- ADV: `src` (advertiser), `rssi` — usually noise/decoys, no crypto relevance.
- OTA_CHUNK: `src`(hub) `dst`(target device) `iv` `payload_hex` `chunk_index` `chunk_total`

## Target identification (the key insight)
The leaked device = the one in BOTH pairing records AND OTA. Cross-reference:
- paired_devices = set(PAIR_INIT.src) ∩ set(PAIR_ACK.dst)
- ota_targets   = set(OTA_CHUNK.dst)
- TARGET = paired_devices ∩ ota_targets
Entities in only one set are decoys (e.g. an OTA sent to a device that never paired is a red herring).

## Worked example (Silent Pairing)
- 5 paired bulbs, 3 OTA targets. Only D5:21:A8:29:00:16 is in both → TARGET.
- D5: nonce_init=1755000314 (= its PAIR_INIT timestamp — suspicious/intentional), ack_nonce=3443427423.
- D5 OTA: iv=ef42fe0a3322aee5043a2ca3b1a6fc80, 112-byte payload (7×16 → block-aligned AES).

## Key-space to brute (derive from TARGET's handshake)
- ni (nonce_init), an (ack_nonce), both as 4-byte BE/LE, concatenated 8+8, repeated to 16.
- ni_s = str(ni), an_s = str(an); hashes: sha256/md5/sha1 of every concatenation/sep (|, _, :, -) and order (ni+an, an+ni).
- hub MAC, dst MAC, iv as raw/hashed.
- arithmetic: ni^an, ni+an, abs(ni-an), sha256 of those strings.
- HMAC(ni,an), PBKDF2(ni, iv), sha256(ni)+sha256(an) concat.

## Cipher matrix
AES-128/192/256 × {CBC, CFB, OFB, CTR(8/16), ECB}; AES-CCM, AES-GCM; RC4; also XOR (single-byte, repeating key, IV-repeat). Pair each key with iv=given/zero/ni/an/mac where relevant.

## Validation (STRICT — see SKILL.md)
json.loads() must parse (and ideally carry expected keys). Do NOT gate on printable-ratio or "starts with {".

## Outcome note (this challenge)
Exhaustive brute over the above space produced 0 valid JSON decryptions → the actual key derivation lives in the challenge's task file (`silent_pairing.md`), NOT derivable from the JSON alone. Lesson: if a wide strict-validated brute yields nothing, obtain the scheme/spec file before guessing further.
