---
name: lfsr-xor-crib
description: Solve "combined LFSR XOR keystream" crypto challenges where two LFSRs (degrees n,m) are XORed to form a keystream that encrypts a known-header-prefixed flag. Given cipher_spec.json (degrees, taps, known_header) + ciphertext.bin, recover the seeds via crib-dragging brute force and decrypt to the flag. Use for CTF challenges mentioning LFSR, keystream, XOR, known plaintext header, taps, maximal-length.
---

# LFSR XOR Keystream Crib Attack

## When to use
Challenge provides:
- A spec with LFSR degrees + tap positions (e.g. deg_a=16 taps=[15,14,12,3], deg_b=17 taps=[16,13]), combiner "XOR".
- A known plaintext "crib" header string that precedes the secret (flag).
- A ciphertext file = `header + flag` XORed by keystream where `keystream = LFSR_A ⊕ LFSR_B`.

## Core technique
The keystream is LINEAR. The smaller LFSR (A, deg bits) has only 2^deg seeds → brute-force it.
For each A-seed:
1. Generate A's keystream bits over the crib length (crib_len_bytes * 8).
2. Derive keystream = ct_bits XOR crib_bits.
3. B_bits = keystream XOR A_bits.
4. Reconstruct B's seed from its first `deg_b` output bits (Fibonacci LFSR: if MSB-out + shift-left, seed[k]=B[deg_b-1-k]; if LSB-out + shift-right, seed[k]=B[k]).
5. Verify B's recurrence reproduces ALL crib-length B_bits. (There is usually exactly ONE consistent pair because deg_a+deg_b > crib bits.)

## CRITICAL PITFALL (cost me the first solve)
Once you have the TRUE seeds, generating the full keystream and XORing with ct may still give GARBAGE even though the seed pair is correct. This happens when the keystream's bit→byte packing order differs from the encryption's. The FIX: brute-force the packing. The model that recovered the seeds (Fibonacci, MSB-out, shift-left) is for SEED RECONSTRUCTION only — the ENCRYPTION packing is independent. Try all 4 combos:
- keystream bit list as-is, bytes MSB-first vs LSB-first: `pt = bytes(c ^ ks_byte for c,ks_byte in zip(ct, to_bytes(ks, byte_msb)))`
Also try reading ct bits in both MSB/LSB order then XOR ks then pack. One will produce `header` exactly at the start + coherent flag.

## Reference implementation
See `scripts/solve.py` (self-contained). Key functions:
- `make_step(n, taps, out_msb, shift_left)`: returns `step(state)->(output_bit, next_state)`. fb = popcount(state & tapmask) & 1.
- `seed_from(O, n, out_msb, sl)`: reverse first n output bits to seed.
- `gen(step, seed, nbits)`: produce keystream bits.
- `to_bytes(bits, byte_msb)`: pack bits to bytes.
- Brute loop over `range(1<<deg_a)`, verify `gen(sB,bseed,M)==B`.

## Typical flags
- deg_a=16 → 65536 iterations, trivial. deg_b=17 → seed from 17 bits.
- Tap positions given as bit indices 0..n-1 (or 1..n). Standard maximal-length: 16-bit taps often [15,14,12,3] (x^16+x^14+x^13+x^11+1 ≡ [15,13,12,10]? verify per challenge); 17-bit [16,13] (x^17+x^14+1). Trust the spec's exact taps.
- Known header is usually ASCII like "CSEM-EXPORT-V1:" or "flag{" prefix. The flag wrapper in the decrypted data may differ from the event's stated format (e.g. decrypted CSEMA{...} while event says TRIVARNA{...}) — submit what's actually in the ciphertext.

## Gotchas
- If combiner were nonlinear (e.g. AND/majority), this brute fails — but XOR is standard for "plain XOR" phrasing.
- Popcount: use Python `int.bit_count()` (3.10+) for speed; 65536 iterations must finish in seconds.
- Validate by checking `pt[:len(header)] == header` AND printable flag content, not just seed consistency.
