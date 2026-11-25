# Worked example — SHA256 length-extension MAC forgery

Challenge: "Vaultify" (CRYPTO, 400 pts, author Tanmay M). Difficulty Medium.

## API description (as returned by GET /)
```
{
  "auth": "mac = SHA256(secret || message)  (no HMAC)",
  "endpoints": {
    "/api/command": "GET ?message=<raw bytes>&mac=<hex> -- runs an authenticated command. role=admin unlocks the flag."
  },
  "hint": "The message is authenticated, not encrypted. What can you APPEND to it while keeping the MAC valid?",
  "secret_length_bytes": 16,
  "service": "Vaultify Token API",
  "your_token": {
    "mac": "ae68dbfc5b5473c14f39ec67ce049770104978eaf9c36e95375a7780eb0226b8",
    "message": "user=guest&action=view&role=user"
  }
}
```

## The vuln
MAC = SHA256(secret || message), NOT HMAC. secret=16 bytes. We hold one valid
(message, mac). Because SHA256 is iterative, the published mac equals the
internal compression state after (secret||message). We can continue hashing
from that state to append bytes and compute a valid mac — no secret needed.

## Attack
1. forged_message = message + sha256_padding(16+len(message)) + b"&role=admin"
   - The glue padding makes the server, when it hashes secret||forged_message,
     reproduce exactly our extended state.
2. forged_mac = SHA256-continue(mac_state, b"&role=admin" + padding(full_len))
3. Server parses the query string; LAST duplicate `role=` wins, so role=admin.

## Failure log (the real lesson)
- urllib/requests version REJECTED with {"error":"bad MAC"} even though the
  crypto was proven correct (matched hashlib on 500 random trials).
- Cause: urllib percent-encodes the 0x80 glue byte -> literal "%80" (3 chars).
  If the server reads `message` via request.args.get (which did NOT
  percent-decode here), the hashed bytes become b"%80" (3 bytes) instead of
  0x80 (1 byte) -> MAC mismatch.
- Fix: raw-socket GET, escaping only & -> %26 and = -> %3D, leaving 0x80 glue
  bytes RAW (also accepted: literal "%C2%80"). Using raw bytes succeeded.

## Success response
```
{"admin":true,"authenticated":true,
 "flag":"BI{m3rkl3_d4mg4rd_l3ngth_3xt3ns10n_pwn3d}",
 "message_seen":"user=guest&action=view&role=user\u0080\u0000...&role=admin"}
```

## Why "what was overlooked"
The valid guest token "appeared valid" but the team missed that a valid MAC
can be EXTENDED — they conflated message authentication with message
integrity/boundary enforcement. Fix = HMAC (or any MAC not length-extendable).

## Reusable tool
`scripts/sha256_length_extension.py` — self-tests against hashlib, then forges
and can fire a raw-socket request:
```
python3 scripts/sha256_length_extension.py \
  --secret-len 16 \
  --message "user=guest&action=view&role=user" \
  --mac ae68dbfc5b5473c14f39ec67ce049770104978eaf9c36e95375a7780eb0226b8 \
  --append "&role=admin" \
  --host 2.29.10.21 --port 5000 --path /api/command
```
