# Wrapped / Multi-line Anomaly Artifacts in Noisy Forensic Logs

## The problem
In "huge decoy log + 1 anomaly" challenges, the REAL artifact is not always on a single
physical line. It can wrap across two (or more) lines, and the continuation line may have
DECOY TEXT APPENDED AFTER the real data. If you decode only the first fragment you get a
silently truncated, unparseable result and waste time brute-forcing the "rest".

## Worked example (CSEMA "Captured Admin Token" challenge)
`auth_proxy_traffic.log`, ~2051 lines of decoys. The anomaly appears as:

```
L1200: 2026-08-03T15:00:00Z [WARN] [AUTH-PROXY] Intercepted admin session hex token: 363e2e3f22332a2b6d42574635333b31372c1a3257496d
L1201: 55223b2d073d39243e6d514742380d3f2a36333c06000000002d  #0001: session_id=SESS-0013 status=OK payload_checksum=c4ca4238
L1202: 2026-08-03T15:00:00.005Z [INFO] [AUTH-PROXY] Token encryption scheme: Repeating-Key XOR (Key ID: PROXYKEY2026)c4ca4238
```

- HEX1 (L1200) = `363e...3257496d`  (23 bytes)
- HEX2 (L1201) = `55223b...06000000002d` — the SECOND HALF of the same hex blob,
  followed by `  #0001: session_id=...` decoy tail appended on the same line.

### Failure mode
Decoding HEX1 alone with key `PROXYKEY2026`:
```
flag{xor_repeating_key_        <-- truncated, no closing brace, looks "almost right"
```
This is a trap: it reads like a valid prefix, so you might stop. But the flag is incomplete.

### Fix
1. Isolate anomaly lines (decoy-regex diff) — L1200/L1201/L1202 all surface.
2. Before decoding, SCAN the NEXT 1–2 lines for a continuation of the same artifact
   (more hex, a stacked config key, a JWT fragment).
3. For L1201, take only the hex BEFORE the `  #0001:` decoy tail, concatenate HEX1+HEX2.
4. Decode the full blob:
   `flag{xor_repeating_key_crib_drag_auth_proxy_2026}`  ✅

## Other wrap shapes seen
- **Stacked config anomalies**: a `[MSISDN_...]` block with `cipher_stack = ...` and
  `vigenere_key = ...` on separate lines after a decoy wall — read the whole block, not one line.
- **JWTs split mid-token**: when a token line is shown in truncated stdout (ellipsis `...`),
  the full token lives in the file — read it from disk, never trust the truncated display.
  Also: multiple "intercepted token" lines can exist; one is the valid JSON payload, another
  is a corrupted decoy (junk bytes after the header) — validate each, keep the clean one.

## Rule of thumb
After isolating the anomaly set, do a 2-line window reassembly pass: concatenate any
fragmented blob (hex / base64 / JWT / config) across adjacent lines, strip trailing decoy
noise, THEN decode/parse. Never decode a fragment that "looks almost complete".
