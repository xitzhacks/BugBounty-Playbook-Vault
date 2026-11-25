# Multi-layer stego-archive challenges with decoy flags

A recurring CTF class (e.g. "Residual Silence"-style): the flag is split across
several *layers*, each padded with noise and *false patterns*, and ends in a
steganographic image layer. The challenge text always warns that "not every piece
is useful / not every pattern is real."

## Layer shape (observed)
1. A set of **key-fragment files** (key1..keyN, halfkey, etc.) — mix of plaintext
   and base64. Most decode to near-identical noise; ONE or a few are the real key.
2. A **container archive** (often 7z with AES, sometimes nesting a rar/zip with
   AES) protected by the recovered key.
3. Inside: **images** (jpg/webp/png) — the final layer.

## Step 1 — recover the real key from noisy fragments
- Base64-decode every candidate line. Real fragments decode to *coherent*,
  corroborated strings; noise decodes to garbage or `?`/`*` placeholders.
- Look for a **shared TEMPLATE** across fragments. Example template observed:
  `31.278N75.779E@%Gxx#SxxxxN*(^$Si` where `Gxx#SxxxxN` is a name/geo token.
  Fragments with the SAME token repeated across 2+ files are real; one-off
  variants are noise.
- Cross-correlate: the password is the variant corroborated by the most files
  (in one case `...@%Gur#Saran6...` appeared in 3 files and was the winner).
- Once you have a candidate, VALIDATE it against the archive, not by eyeballing:
  `7z t -p'CANDIDATE' archive.7z` → "Everything is Ok" = correct. This is ground
  truth (same as the ZipCrypto rule in the main skill).

## Step 2 — descend the container
- `7z x -p'KEY' -y -oout archive.7z` then inspect contents (`file`, `7z l`).
- Nested rar: `unrar x -p'KEY' secret.rar out/` — the SAME key usually opens every
  layer (you can't open an AES archive with a "decoy" key; if it opens, it's real).
- Note file extensions can LIE: `.jpg` files that are actually WebP (RIFF/VP8)
  are common in these challenges. Use `file` / `exiftool`, not the extension.
- steghide can't read WebP/BMP directly; convert WebP→BMP with Pillow if you must
  try steghide on a WebP (rare — most real stego carriers are real JPEGs).

## Step 3 — the image layer: decoys vs. the real flag
- Run `strings -n 4`, `exiftool`, `binwalk` on every image. You will find MANY
  fake flags. Recognition pattern:
  - Decoy flags use a DIFFERENT wrapper than the real one (e.g. `UNI6{...}` when
    the brief says the flag is `TRIVARNA{...}`).
  - They appear in metadata, trailing bytes after EOI, fake RIFF chunks
    (`UNI6`/`VU5J` chunk IDs), and as base64-of-the-decoy-flag.
  - They explicitly taunt: `UNI6{THIS_IS_NOT_THE_FLAG...}`, `WRONG_PATH_5678`,
    `MULTIPLE_FLAGS_EXIST_BUT_ONLY_ONE_IS_TRUE`. Treat ALL of these as noise.
  - `grep -rao TRIVARNA .` returns nothing → the real flag is NOT sitting in
    readable bytes; it is embedded.
- After exhausting metadata/strings/trailing-data, the intended method is
  **DCT-coefficient stego** (steghide / outguess) on the real JPEGs. This is the
  only method that survives JPEG recompression ("residual" theme) and matches
  "only one is true."

### PASSPHRASE STRATEGY (important — corrected from earlier guidance)
- The earlier assumption "the archive key IS the stego passphrase, just reuse it"
  is WRONG in practice. In a real solve the archive key opened both the 7z and the
  rar but produced **zero** readable stego output. Treat the archive key as only
  the **#1 candidate**, then brute a wide candidate set:
  - Every distinct geo/name variant from the key files (clean form AND its
    base64 form). Note small differences matter: `...@%Gur#Saran6` vs
    `...@%Gur#Saran5` vs `...@G%Gur#Samar5` are DIFFERENT keys.
  - The full decoy flag strings (UNI6{...} verbatim, including trailing hex) —
    "not every pattern is real" sometimes means one decoy IS the stego key.
  - Hashes (md5/sha1/sha256/sha512) of each key-fragment string — the H1 decoy
    literally says "KEEP_ANALYZING FILES AND HASHES".
  - Trivials: empty, `TRIVARNA`, the challenge name, sub-tokens (`GurSaran`, etc.).
- Gate on READABLE output (printable-ratio > ~0.8 OR contains the real flag
  wrapper), NOT on "Extracting usable bits" (see pitfall below).

### Running steghide / outguess WITHOUT root (locked-down Parrot/Kali)
sudo/apt-get install are often blocked (no passwordless sudo; PEP 668 for pip).
Get the binaries locally with `apt-get download` (no root needed to *download*,
only to *install*):
```
apt-get download steghide            # -> steghide_0.5.1-15_amd64.deb
apt-get download libmcrypt4          # steghide needs libmcrypt.so.4 at runtime
apt-get download outguess            # optional, if DCT stego might be outguess
mkdir x && cd x
ar x ../steghide_*.deb && tar -xf data.tar.*
# repeat for libmcrypt4 (extract) and outguess
```
Then run with `LD_LIBRARY_PATH` pointed at the extracted lib dir:
```
export LD_LIBRARY_PATH="$PWD/libm_extract/usr/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH"
./steghide_extract/usr/bin/steghide extract -sf IMG.jpg -p 'KEY' -xf out.txt
./outguess_extract/usr/bin/outguess -r -k 'KEY' IMG.jpg out.txt
```
`outguess` needs no extra lib; `steghide` needs `libmcrypt.so.4` resolved via
LD_LIBRARY_PATH. Verify with `ldd` — any "not found" must be satisfied the same
way (download the matching runtime .deb, extract, add to LD_LIBRARY_PATH).
Reusable brute: `scripts/stego_brute.py <images_dir> <keyfiles_dir>`.

## Pitfalls
- ⚠️ **The archive password is NOT automatically the stego passphrase.** Open the
  7z/rar with key A, then try key A for steghide — but if it fails, BRUTE the full
  key-variant set (clean + base64 + hashes + decoys). Do not stop at "reuse the
  key." (Earlier guidance that said "don't brute, just reuse" was wrong.)
- ⚠️ **outguess "Extracting usable bits: N bits" is NOT proof of embedded data.**
  Every JPEG reports usable bits even with no outguess payload. A wrong passphrase
  yields "Extracted datalen is too long: X > Y" (garbage length) or a Floating
  point exception (core dump, empty output). Only a CORRECT passphrase yields a
  file with readable content. So "usable bits present" must never be read as "real
  data here."
- The "GZ" magic (`\x1f\x8b`) inside JPEG entropy-coded scan segments is a
  COINCIDENCE, not an embedded gzip. Don't waste time trying to inflate random
  byte runs from the middle of a JPEG.
- Fake RIFF chunks (`UNI6`, `VU5J`) are not real WebP chunks (real ones are
  `VP8 `, `VP8L`, `VP8X`, `ANIM`, `ANMF`). A chunk ID that spells a flag wrapper
  is a decoy.
- Pixel-domain LSB (stegano-lsb, naive channel LSB) yields nothing on
  recompressed JPEGs — that's expected; the real data is in the DCT domain.
- Don't confuse steghide and outguess failure modes: steghide says "could not
  extract any data with that passphrase!"; outguess either dumps core (FPE) or
  prints "too long." Both mean "wrong key," unless readable output appears.
