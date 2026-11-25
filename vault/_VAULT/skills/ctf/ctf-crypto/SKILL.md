---
name: ctf-crypto
description: CTF cryptography & encoding challenges. Covers (1) common-factor / shared-prime RSA where two moduli share a prime p -> gcd(n1,n2) recovers p, factor both, derive private keys, decrypt; (2) split-flag textbook RSA (flag halved, each half encrypted under a different key); (3) mixed-base fragment reassembly — logs with hex/base64/base32 payloads, decoys, timestamps in different time zones, fragments logged out of order; (4) chained-encoding / "cipher cascade" blobs that must be peeled through several reversible transforms (incl. basE91 + keyed XOR) to reach the flag; (5) book ciphers / "numbered note" stego where a shared text is the key and number pairs (A//B) index word/char positions. Use when a CTF hands you 2+ RSA public keys + ciphertexts, relay/booth/log JSON files, a single opaque encoded blob plus a "remove each layer in order" description, or a long text + a list of numeric coordinate pairs.
---

# CTF Crypto & Encoding

## 0. SHA256 / Merkle–Damgård length-extension MAC forgery
A MAC computed as `mac = H(secret || message)` where H is SHA256/SHA1/MD5 (NOT
HMAC) is length-extendable. If you hold ONE valid (message, mac) pair and know
the secret length, you can append arbitrary bytes and compute a VALID mac for
the extended message — WITHOUT the secret.

Mechanism: H is iterated; the published `mac` is the internal compression state
after hashing (secret||message). Continue compressing from that state with the
glue padding (`0x80` + zeros + 64-bit length) followed by your appended block(s).
The server, hashing `secret || forged_message`, reproduces exactly that state.

Steps:
1. `forged_message = message + H_padding(secret_len + len(message)) + append`
   where `append` is your payload (e.g. `b"&role=admin"`). Last duplicate key
   usually wins in query parsers, so appended `role=admin` overrides the original.
2. `forged_mac = H_continue(mac_state, append + H_padding(total_len))`.
3. Send `forged_message` + `forged_mac`. Done — no secret involved.

PITFALL (bit us in a real solve; cost a failed attempt):
- urllib / requests / `urlencode` will PERCENT-ENCODE the `0x80` glue byte,
  turning it into the 3-char string "%80". If the server reads `message` via
  `request.args.get` (which often does NOT percent-decode), the hashed bytes
  become `b"%80"` (3 bytes) instead of `0x80` (1 byte) and the MAC mismatches
  ("bad MAC") — even though your crypto is correct.
- FIX: deliver the forged message BYTES VERBATIM. Use a raw-socket GET that
  escapes ONLY `&`->`%26` and `=`->`%3D`, leaving `0x80` glue bytes RAW (the
  server also accepted literal `%C2%80`). NEVER route the padding through
  urlencode/quote. Verify with a self-test against hashlib before firing.

Reusable tool: `scripts/sha256_length_extension.py` (self-tests vs hashlib,
then forges and can fire a raw-socket request). Worked example + full failure
log: `references/length_extension_mac.md`.

## When to load this
- Challenge ships `pubkeyN.txt` + `ciphertextN.txt` (or similar) and mentions RSA, "shared prime", "insufficient entropy", "common factor", "weak RNG".
- Challenge ships logs/JSON with `payload` fields in mixed encodings (hex / base64 / base32), plus decoys and "out of order" / "different time zones" / "split the message" hints.
- Challenge ships a single opaque blob with a "cipher cascade" / "multiple encodings chained" / "remove each layer in the correct order" description.
- Challenge exposes a MAC/API-token endpoint whose MAC is `SHA256(secret || message)` (or any plain Merkle–Damgård hash, NOT HMAC) and hands you ONE valid (message, mac) pair + the secret length, then asks you to "append" to the message / escalate a role / reach an admin action. That is SHA256 **length-extension** forgery (see Section 0).
- Challenge exposes an "MPC" / additive secret-sharing protocol with two rounds of public shares (A, B, C) + a published sum S (== sum of private values mod p), a hint that "pairwise masks are accidentally reused between rounds", and asks for a hidden private value. That is MPC mask-reuse (Section 6).
- Challenge is a reverse-engineering / "retro game / C2 client / loader" task whose flag is behind XTEA / TEA / XXTEA and the key is assembled from runtime state (game score, config, file fields). Recover the key by reading constants in the disassembly — you do NOT need to run/win the binary or dump live memory. That is Section 7.
- Challenge is forensics / "memory snapshot / partial memory region / encoded payload" where a base64 (or other) blob is buried in a mostly-random file and must be decoded to recover the flag. That is Section 8.
- Flag wrapper is DYNAMIC per event. Seen wrappers: `TRIVARNA{...}`, `CSEMA{...}`, `UNI6CTF{...}` (uppercase, usually a DECOY family), `uni6ctf{...}` (lowercase, REAL — treat as valid), `T{...}`. A user may say "flag format can be uni6ctf{} as well" — that means the REAL wrapper can be lowercase `uni6ctf{}` and is distinct from the uppercase `UNI6CTF{}` decoys. Never assume one fixed wrapper; reconstruct the literal string and, if the platform demands a fixed wrapper, rename the inner.

## 1. Common-factor (shared-prime) RSA
If `gcd(n1, n2) != 1`, the two moduli share a prime `p` (classic Debian-OpenSSL / weak-RNG reuse bug). Recover it:
```python
p = gcd(n1, n2)
q1, q2 = n1//p, n2//p
phi1 = (p-1)*(q1-1) ; d1 = pow(e, -1, phi1)
m1 = pow(c1, d1, n1)   # repeat for key 2
```
Then decode each `m` as fixed-width big-endian bytes: `k = (n.bit_length()+7)//8`, `m.to_bytes(k,'big').lstrip(b'\x00')`, concatenate the two halves. Test both half orders (`m1+m2` and `m2+m1`).
Full reusable solver: `scripts/rsa_common_factor.py` (takes a directory of `pubkeyN.txt`/`ciphertextN.txt`).

Pitfalls:
- Both `e` are usually `65537`; compute `d` per key if they differ.
- Textbook RSA (no padding) -> direct `pow(c,d,n)`.
- Decode each half independently before concatenating; leading nulls must be stripped.

## 2. Mixed-base fragment reassembly
Typical anatomy: one archive (sometimes a ZIP *renamed* `.log`/`.tgz`) containing per-source logs. Each line is JSON with `tag`, `valid`, `color`/`booth`, `date`, `timestamp` (with tz offset), `payload`.

Steps:
1. **Extract nested archives first.** A `*.log` may be a ZIP (`unzip`); `*.tgz` is `tar xzf`. Always peek magic bytes. (Seen: `booth.log` was itself a ZIP of `booth_alpha/beta/gamma.log`.)
2. **Filter decoys** — keep an entry ONLY if ALL hold:
   - `valid == true`
   - `tag == "CEREMONY"` (drop `PRACTICE` rehearsals)
   - `color` matches the booth's expected tricolor (alpha=saffron, beta=white, gamma=green) — wrong-color entry = decoy
   - `date` matches target date — wrong-date (e.g. 16-08 vs 15-08) entry = decoy
   - Explicit `valid:false` entries are decoys; their `payload` is often a HINT ("sort-by-string-is-wrong" = do NOT sort alphabetically).
3. **Decode each genuine payload** by its base. The three booths usually map to three bases (saffron=hex, white=b64, green=b32). A fragment decodes cleanly in exactly ONE base — that base is forced; verify byte-for-byte.
4. **Order the fragments.** "Different time zones" + "out of order" => parse each ISO timestamp WITH its offset, convert to UTC (`datetime.fromisoformat(ts).astimezone(timezone.utc)`), sort ascending, concatenate. This is the intended order.
5. **If order is still ambiguous**, brute-force all permutations (7 fragments = 5040) and keep candidates that form a single balanced `wrapper{...}` with printable inner; rank by English-likeness / keyword match.
6. **Assemble the flag.** Opening fragment usually contains `{`, closing contains `}`. If chronological order nests the brace mid-string, the intended flag is the brace-delimited substring (from `{` to `}`).

Pitfalls:
- Do NOT sort alphabetically — challenges plant a `valid:false` payload saying exactly that.
- Don't trust the literal wrapper — TRIVARNA/CSEMA/UNI6CTF/uni6ctf/T{ all seen. Submit the literal reconstructed string; if the platform demands a fixed wrapper, rename the inner.
- Decoys themselves often decode to clean `UNI6CTF{...}` strings — the REAL flag uses the same wrapper family (often lowercase `uni6ctf{}`) but different inner words. Uppercase `UNI6CTF{}` in a decoded fragment is a decoy, NOT the answer.
- base32 of a 7-char string yields 5 bytes; a stray non-printable byte is normal — don't discard the fragment.
- If NO permutation reads as English, suspect a missing decode layer (chained codec: b64-of-hex, ROT, etc.) — brute 1- and 2-layer codec chains per fragment. If still stuck, the intended order may be by timezone-offset magnitude or booth-internal time order; try both.

Reusable brute-forcer: `scripts/fragment_reassemble.py`. Worked example of this exact anatomy: `references/signal_sabha.md`.

## 3. Chained-encoding / "Cipher Cascade" blobs
Single opaque blob + "multiple encodings chained" / "remove each layer in the correct order". The chain is a sequence of keyless reversible transforms (base64, hex, base32, URL, ROT13/47, atbash, gzip/zlib, reverse) and/or keyed transforms (XOR with a repeating key or passphrase, RC4), often fronted by **basE91** (a 91-char alphabet that includes `%`, `+`, `/`, `[`, `\`, `{`, `}`).

Detection & approach:
1. **Check the alphabet.** If the blob is entirely within the basE91 alphabet, b91 is very likely the first (or an) outer layer: `b91(blob)` -> bytes. Reusable decoder in `scripts/cipher_cascade_peel.py`; the standard basE91 alphabet is hardcoded there.
2. **Pruned BFS peel.** Over keyless transforms, but PRUNE hard or it explodes (>3M nodes / timeout). Keep a node only if it is (a) printable text, (b) looks like a next-stage encoding (all base64/hex/b91 chars), or (c) compressed (gzip/zlib/raw-deflate magic). A reusable pruned peeler is in `scripts/cipher_cascade_peel.py`.
3. **If a flag prefix (e.g. `uni6ctf{`) appears after some decode, crib-drag.** Derive the XOR keystream from the known prefix: `key[i] = x[i] ^ prefix[i]`. If `x[i]^key[i]` reproduces the prefix exactly (prob ~0 by chance), the chain contains `b91 -> XOR`. Then:
   - Try repeating-key XOR at many periods — but if it garbles after the crib (period != short repeating word), the key is longer/derived.
   - Try keyword XOR/RC4 with event/theme words ("ciphercascade", "encoding", "layered", "uni6ctf", etc.) — often fails.
   - **Stop blind keyword guessing** once the prefix is the only recoverable part. A keyed stream (RC4 with unknown passphrase) or inner content that is itself further encoded cannot be brute-forced without the key/order.
4. **Get the intended order/key from the user.** "Remove each one in the correct order" means the challenge lists the encodings — paste them and wire them in exact sequence. Without that, the keyed layer is a dead end.

Pitfalls:
- A generic BFS over transforms (no pruning) explodes; always prune to printable/next-stage/compressed.
- The keyed-XOR layer is invisible to a keyless transform BFS — you must crib-drag explicitly.
- `uni6ctf{` (lowercase) emerging from `b91+XOR` is a REAL signal; uppercase `UNI6CTF{...}` decoded from a decoy fragment is NOT.
- basE91 output being binary (not further-base64) is expected; do NOT try to base64-decode binary.

Reusable tooling: `scripts/cipher_cascade_peel.py` (pruned BFS + crib-drag; runs on the worked example blob out of the box). Worked example & full failure log: `references/cipher_cascade.md`.

## 4. Book cipher / "numbered note" stego (handbill-as-book)
A public/shared text IS the key. A strip of number pairs indexes into it.
Classic historical / dead-drop CTF: a propaganda handbill + a strip of
`A//B` pairs; wardens dismiss the numbers as noise.

Detection:
- Challenge hands you TWO artifacts: a long text (book/article/manifesto)
  AND a list of coordinate pairs (often `A//B`, may have a trailing `-`).
- No key file, no password — the text itself is the key.

Scheme (verified):
- Pair `A//B` = the **B-th CHARACTER of the A-th WORD** (1-indexed) of the
  book text, after tokenizing into words with `re.findall(r"[A-Za-z']+", text)`.
- The lone `-` (e.g. `11//4-`) means "take the character BEFORE" (previous
  char of that word): `ci = b-2` when present.
- Other coordinate conventions also appear (line//word, word//letter-with-
  occurrence, char-of-whole-text). If `(word,char)` garbles the body but a
  mid-section reads as clean English, your BOOK TRANSCRIPTION differs from the
  encoder's — fix the source text, don't change the scheme. The clean-English
  hit is the proof the scheme is right.

Decode + prove it worked:
- Run the book through the solver; if the middle spells real words
  (`voice`, `cannot`, `chained`, `destroy`, `note`) the scheme is correct even
  if head/tail fragments look noisy (those drift from OCR word-choice variance
  between your transcription and the encoder's exact source text).
- The recovered string is the secret; in dead-drop challenges it often ends
  with an instruction like "destroy this note" (OPSEC — burn after reading).

Reusable solver: `scripts/book_cipher_decode.py`
  `python3 book_cipher_decode.py --book handbill.txt --pairs "26//1 1//2 ..."`
  (also reads pairs from stdin). Handles `A//B` and `A//B-`.

Pitfalls:
- Word tokenization must match the encoder's. `[A-Za-z']+` keeps `don't` as
  one word; switching to `[A-Za-z]+` shifts every index after a contraction.
- The dash is NOT "lowercase" — it's a coordinate tweak (previous char).
- Leading/trailing punctuation and line breaks in the book must match; a
  missing word at the top shifts ALL downstream indices. If decode breaks
  early, re-check the very first words of the book.
- If you only have a paraphrased transcription of the book (vision-OCR
  summarized it), indices will drift at the head/tail. Prefer exact text;
  if unavailable, the mid-section English hit still confirms the scheme.

## 5. Tooling
- `python3` stdlib only (no external deps) suffices for every recipe here.
- `unzip`, `tar` for nested archives.
- `scripts/book_cipher_decode.py` — book-cipher / numbered-note decoder.
- `scripts/sha256_length_extension.py` — length-extension MAC forger (Section 0).
- `scripts/mpc_mask_reuse.py` — MPC additive secret-sharing mask-reuse solver (Section 6).

## 6. MPC additive secret-sharing mask-reuse
A "multi-party computation" puzzle where each party's public share is an
additive secret-share with random masks:

    A = xA + rAB - rAC
    B = xB + rBC - rBA
    C = xC + rCA - rCB      (all arithmetic mod p)

Published sum `S = A + B + C ≡ xA + xB + xC (mod p)` because every mask cancels
(pairwise: each r appears + in one party and - in another). Round 1 (calibration)
gives ONE private value (e.g. xA1 known). Round 2 hides that same party's value.

The "overlooked" trick (verified on challenge "THE HUNT", author Tanmay M, 300
pts): the hint says *someone's* pairwise masks are **reused across rounds**.
If party X's masks are reused (r_xy round2 == r_xy round1 for all y != X), then
for party X the masks cancel identically:

    AX2 - AX1 = xX2 - xX1      =>      xX2 = xX1 + (AX2 - AX1) mod p

Which party? The challenge gives exactly ONE known private value (the calibration
value) — that party is the target, because only a party with a known R1 value can
be recovered *absolutely*. Apply the formula to that party.

Pitfalls:
- Do NOT assume ALL masks reused. That forces every party's delta equal, which
  contradicts the (consistent) sums and is the trap. "Someone's" = exactly one.
- The published shares A,B,C ALREADY include the masks — you never see the masks;
  you only exploit that (AX2-AX1) cancels them when reused.
- The sum equation gives xA+xB+xC, not any individual x. So a single party's
  recovered delta NOT equaling (S2-S1) is EXPECTED — it confirms exactly one
  party's masks were reused, not all. Use it as a consistency signal, not a
  contradiction.
- Modulo: do every subtraction mod p; Python `% p` handles negatives cleanly.
- Last duplicate key usually wins in query parsers — relevant if the MPC output
  is later fed into a length-extension-style append (see Section 0).

Reusable solver: `scripts/mpc_mask_reuse.py` (parses the protocol block, tries all
three reuse assumptions, prints each candidate and flags the anchored one).
Worked example: `references/mpc_mask_reuse.md`.

## 7. Recovering XTEA / TEA / XXTEA from a binary (reverse-engineering)
A "retro game / C2 client / loader" challenge often hides the flag behind a block
cipher whose 128-bit key (4×uint32) is assembled at runtime. XTEA is the most common.

Identification in the disassembly (`objdump -d -M intel binary`):
- 64-round loop. `sum` initialized to `0xC6EF3720` (= `0x9E3779B9 * 32`) and
  `sum -= 0x9E3779B9` each round => **XTEA DECRYPTION** (the published MAC-equivalent
  state is the final hash). Encryption starts `sum=0` and `sum += 0x9E3779B9`.
- Round body: first half updates `z` using `key[(sum>>11)&3]`; second half updates
  `y` using `key[sum&3]`. That (sum-index-keyed) pairing is the XTEA signature.
  (TEA uses four FIXED subkeys `0x9E3779B9*i` instead of the sum-indexed key table;
  XXTEA uses one loop over all words with `(z>>2)^(y<<3)`-style mixing.)
- The key is usually built from runtime state — e.g. a game sets `key[0]=0xdeadbeef`
  at score 100, `key[1]=0x1337c0de` at 200, `key[2]=0xcafebabe` at 300,
  `key[3]=0x8badf00d` at 400. Find the threshold/comparison instructions in `main`;
  read the constants, do NOT play the game or dump live memory.
- The decrypted blob is typically 4 blocks (32 bytes) printed via
  `printf("%s", buf)` right after the decrypt call.

Known-good pure-Python XTEA decrypt (no external deps) — verify by RE-ENCRYPTING
the output and confirming it equals the original ciphertext blob; if it round-trips
AND prints `ctf7{...}`, that's the flag:
```python
import struct
def xtea_dec(block, key, rounds=32):
    v0, v1 = struct.unpack('>II', block)
    sumv = 0xC6EF3720          # 0x9E3779B9 * 32
    delta = 0x9E3779B9
    for _ in range(rounds):
        v0 = (v0 - ((v1<<4 ^ v1>>5) + v1) ^ (sumv + key[sumv>>11 & 3])) & 0xFFFFFFFF
        sumv = (sumv - delta) & 0xFFFFFFFF
        v1 = (v1 - ((v0<<4 ^ v0>>5) + v0) ^ (sumv + key[sumv & 3])) & 0xFFFFFFFF
    return struct.pack('>II', v0, v1)
```
Full recipe + real solved-binary walkthrough: `references/xtea_from_binary.md`.

## 8. "Encoded payload" buried in a memory dump / random-padded file
Forensics challenge ("memory snapshot", "partial memory region", "Volatility" hint)
where the flag is a base64 (or other) blob tucked inside a mostly-random file.

Workflow:
1. **Locate the artifact.** `strings -a file | grep -i <process>` (e.g. `shadowd`).
   Look for `=== *_PAYLOAD_BEGIN/END ===` markers. The file is usually a synthetic
   ~512 KB blob: uniform random padding (entropy ~7.8) + ONE readable cluster with
   fake syslog lines. Volatility3 CANNOT parse it ("Unable to validate plugin
   requirements" — it is not a real image); the hint just means *use strings / forensic
   tooling*. Do not burn time forcing `vol`.
2. **Extract the payload EXACTLY.** Pull raw bytes between the markers — do NOT trust a
   `strings`/regex `[A-Za-z0-9+/]{16,}` match, which silently drops the trailing char
   (a 36-char payload can come back as 35). Verify char count: 36 base64 chars => 27
   bytes; 35 => 26 bytes. They decode to DIFFERENT blobs — getting this wrong wastes
   the entire downstream battery.
3. **Decode.** `base64 -d` (confirm with both Python `base64.b64decode` AND the system
   tool — they agree). If the result is ASCII `ctf7{...}`, done. If binary, run battery.
4. **Exhaustive decode battery** (let `payload`=base64 string, `dec`=its decode):
   - XOR: single byte 0..255; repeating 1–3 byte FULL brute (check `dec[i]^k==b'ctf7{'[i]`
     AND all-printable); keystreams = `shadowd`/`Parth`/`ctf7`/PID/`marker` and their
     MD5/SHA1/SHA256/SHA512/SHA3 keystreams; offsets & reversed keys; file-wide XOR with
     `dec` as a 27-byte repeating key.
   - Stream/block: RC4 (keys above); AES-ECB/CBC 16/24/32 (`cryptography` lib, key
     `"shadowd"*N` padded).
   - Arithmetic: ADD/SUB one-byte and repeating-key; ROL/ROR 1–7 bits; index variants
     (`dec[i]^i`, `dec[i]-i`).
   - Encoding: base-N (36/62/95) of the big integer; custom base64 alphabets — all 64
     rotations, keyword front/end/repeat/reverse, case-swapped (lower-before-upper),
     digit-first, reversed standard; byte→base64-char remap (`b%64`,`b//4`,`b&63`); base85.
   - Cross-challenge: XOR with a key reused from a sibling challenge (e.g. the XTEA dwords
     `deadbeef1337c0decafebabe8badf00d`).
5. **Pruning trick (big time-saver).** Compute `required_key[0] = dec[0] ^ ord('c')`.
   If it is >0x7F (e.g. `0xf0`), the key is **binary / hash-derived**, NOT a printable
   string — stop guessing printable keys and go straight to hash keystreams + custom
   base64. (In the solved Memory Shadows case required key was `f0f2e19059`; no hash of
   any obvious string matched and every printable/short-key transform failed — so either
   the encode was a private custom scheme or the intended answer is a wrap of the raw bytes.)
6. **If the battery exhausts with no `ctf7{`:** present the two last-resort UNVERIFIED
   candidates and ASK for the encoding/key — do not guess blindly forever:
   - hex-wrap: `ctf7{<dec.hex()>}`
   - payload-wrap: `ctf7{<payload>}`
   Request a hint (key derivation, cipher type, or the solve script).

Full worked run + exhaustive-transform log: `references/forensics_encoded_payload.md`.
