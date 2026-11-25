# Noisy Forensic Log / Decoy Detection — worked example

Challenge: "Intercepted Independence Activation SMS" (CSEMA / Trivarna CTF, easy, 100pts).
Two forensic artifacts in the zip:
- `sms_gateway_routing.log` — ~2051 lines
- `gsm_7bit_intercept.conf` — config audit dump

Both were ~99% DECOY: thousands of structurally-identical lines with VALID MD5-based
checksums, designed to bury the real data and make you waste time verifying noise.

## Decoy signatures (the template to diff against)
Log decoy line (all 2050 normal lines match this exact shape):
```
^2026-08-03T[0-9:.]+Z \[(DEBUG|INFO|WARN)\] \[SMSC-GW1-(GW|CORE|SEC|SYS|NET|AUTH|DB)\] Trace event #[0-9]+: session_id=SESS-[0-9]+ status=OK payload_checksum=[0-9a-f]+$
```
- Timestamps all in `10:00:00`–`10:00:1x`. Real line was at `14:10` with component `SMSC-GW1-INTERCEPT`.
- `payload_checksum=` carries a real md5(value) prefix — passes verification → lulls you into trusting it.

Conf decoy line:
```
^param_[0-9]+ = value_[0-9]+ # audit_ok=true checksum=[0-9a-f]+$
^\[SMSC_POLICY_[0-9]+\]$
```
- The `checksum=` values are valid md5(value) prefixes. Again, a distraction.

## Anomaly extraction technique
1. Build the strict regex of the decoy line shape (from a few samples).
2. Filter to lines that DON'T match: programmatic `splitlines()` + `re.match`, or `grep -vE '...'`.
   This collapses 2051 lines → the 4 real ones instantly.
3. ⚠️ Line-ending pitfall: files may be `\r\n`. GNU `grep -vE` with `$` still anchors before
   `\r` so it usually works, but when a decoy regex looks correct yet matches nothing, strip `\r`
   first (`line.rstrip('\r')` / `tr -d '\r'`). Python `splitlines()` handles it automatically.
4. The 4 anomalous lines were: the intercept WARNING, the `Encrypted Payload:` line (ciphertext
   inline), the ciphertext line itself, and a `Key Alias Header` line.

## Real data recovered
Hidden config block among the decoys (in the .conf):
```
[MSISDN_+919****3210]
msisdn = +919****3210
cipher_stack = ROT13_THEN_VIGENERE
vigenere_key = JIOKEY
```
Anomalous log line (the ciphertext):
`Encrypted Payload: ... bgbd{jxo_ker_izp13_qjdvyamf_qvwaxpj_zypzszvap_2026}`

## Decryption (see scripts/reverse_cipher_stack.py)
`ROT13_THEN_VIGENERE` = encrypt ROT13 first, then Vigenère(key). Decrypt in REVERSE:
1. Vigenère-DECRYPT with key `JIOKEY`
   → `synt{fzf_cqh_ebg13_ivtrarer_gryrpbz_vagreprcg_2026}`
   (note `synt{`→`flag{`, `ebg13`→`rot13` — confirms the ROT13 layer underneath)
2. ROT13 the result
   → `flag{sms_pdu_rot13_vigenere_telecom_intercept_2026}`
3. Event wrapper is `flag{...}` but submit as `TRIVARNA{...}` → re-wrap the inner content.

Final flag: `TRIVARNA{sms_pdu_rot13_vigenere_telecom_intercept_2026}`

## Generic lesson
When a forensic artifact is "mostly noise," the answer is the ANOMALY, not the bulk.
Always compute the decoy template and diff against it. Valid checksums on decoy lines are a
distraction — don't verify decoys, FILTER them.
