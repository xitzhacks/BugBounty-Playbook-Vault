---
name: ctf-forensics
description: Solve CTF forensics/crypto challenges involving captured traffic, encoded/encrypted blobs, and artifact recovery. Use when given a pcap/trace/JSON capture or ciphertext to decode — especially BLE/IoT/OTA-style "recover the leaked X" challenges. Encodes the strict-validation brute-force discipline and the cross-reference target-identification methodology so future sessions don't reinvent them.
---

# CTF Forensics & Capture Analysis

## When to use
- A CTF challenge gives a capture/trace (pcap, BLE/serial/JSON log) and asks to recover a secret (flag, manifest, key).
- A challenge gives a ciphertext + contextual metadata (nonces, IDs, MACs, IVs) and expects you to derive the key.
- Any "decode this / recover the leaked X" forensics task.

## Operating workflow
1. RECON the artifact before touching crypto. Parse structure, enumerate entities (hosts, devices, sessions), separate signal from noise.
2. IDENTIFY the real target by cross-referencing records: the intended subject is usually the entity present in BOTH the "setup" traffic (pairing/handshake) AND the "interesting" traffic (the leak). Entities in only one stream are decoys.
3. EXTRACT exact bytes: ciphertext, IV/nonce, and every contextual field that could seed a key (handshake nonces, MAC addresses, IDs, timestamps).
4. HYPOTHESIZE the scheme. For an "easy" challenge the transform is usually simple (single cipher, key from given fields). Don't reach for exotic schemes first.
5. BRUTE with strict validation (see below). Never eyeball "looks readable".
6. VERIFY the winner parses/decodes to a real structure, then extract the flag.

## Multi-layer stego-archive challenges with decoy flags (e.g. "Residual Silence")
Some challenges wrap the flag in 3+ layers of noise + explicit decoys. Full method
in `references/stego_decoy_archive.md`. Summary:
1. **Recover the real key from noisy key-fragments** by base64-decoding every
   candidate, then cross-correlating on a shared template. The winner is the
   variant corroborated by the most files. Validate with `7z t -p'CAND' archive.7z`
   ("Everything is Ok") — opening an AES archive is ground truth that the key is real.
2. **Descend the container** (`7z x` → nested `unrar x`); the same key usually
   opens every layer. Watch for LYING extensions (`.jpg` that is really WebP/RIFF).
3. **Image layer = decoys + one real embedded flag.** Expect MANY fake flags with
   a *different* wrapper (`UNI6{...}` vs the real `TRIVARNA{...}`), in metadata /
   trailing bytes / fake RIFF chunks, explicitly taunting you. These are ALL noise.
   Once `grep TRIVARNA` finds nothing in readable bytes, the real flag is in the
   **DCT domain** (steghide/outguess) on the real JPEGs. ⚠️ **The recovered
   archive/container key is NOT automatically the stego passphrase** — in a live
   solve the 7z/rar key opened both layers but produced ZERO readable stego
   output. Treat it as the #1 candidate, then **brute a wide set** (every
   key-fragment variant + base64 + hashes of fragments + verbatim decoy strings +
   trivials). Full method, non-root binary install, and the
   outguess-"usable-bits"-is-not-proof pitfall → `references/stego_decoy_archive.md`;
   reusable brute → `scripts/stego_brute.py`. Pixel-LSB yields nothing on
   recompressed JPEGs by design.

## CRITICAL: strict validation (avoid false positives)
When brute-forcing many key×cipher combos, naive scoring (printable-ratio, keyword presence) produces MASSIVE false positives — ~1/256 random decryptions start with `{`, so a "starts with {" filter lights up constantly on garbage and misleads. Use a real validator instead:
- If plaintext should be JSON: `json.loads(decoded)` must succeed; prefer also requiring expected keys (manifest/signature/device/flag).
- If binary: check magic bytes (PK\x03\x04, \x89PNG, \x7fELF, %PDF, BZh9, \xfd7zXZ, GIF8).
- If a known prefix/flag format is given: require `decoded.startswith(b"FLAG{")`.
- Only surface candidates that pass a hard check. Printable-ratio is at best a tiebreaker, never a gate.

## Library note (tooling)
pycryptodome's `AESCCM`/`AESGCM` imports can be unavailable in some environments (stale/partial install). Prefer the `cryptography` package (`cryptography.hazmat.primitives.ciphers.aead.AESCCM/AESGCM`) for AEAD modes — it's reliable. For the bulk AES matrix, either library works; `cryptography.hazmat` is consistent.

## BLE / IoT capture specifics
- The hub is the common source of control/ACK frames; endpoints are per-frame src/dst.
- Pairing handshake = PAIR_INIT (from device, carries `nonce`) ↔ PAIR_ACK (from hub, carries `ack_nonce`).
- OTA/OTA_CHUNK frames carry `iv` + `payload_hex` (hex ciphertext) and `chunk_total`/`chunk_index`.
- Leaked device = one that BOTH completed pairing AND received the OTA. Other OTA destinations that never paired are decoys.
- Derive candidate keys from: the paired device's `nonce`+`ack_nonce`, both device+hub MACs, the OTA `iv`, and combinations (hashes, concatenations, arithmetic). See references/ble_capture_analysis.md.
- Block-aligned ciphertext (multiple of 16) suggests AES block mode; non-block-aligned suggests stream (RC4/CTR/ChaCha) or an appended auth tag.

## Noisy forensic logs & decoy detection
Many "forensics" challenges ship a huge artifact (~1000s of lines) that is ~99% DECOY: structurally-identical rows with VALID checksums (e.g. real md5(value) prefixes) to make you waste time verifying noise. The flag/secret is the ANOMALY, not the bulk.

### Technique A — decoy-regex diff (use when a clean decoy template exists)
1. Derive the strict regex (or exact template) of a normal decoy line from a few samples.
2. Extract lines that DON'T match — programmatic `splitlines()` + `re.match`, or shell `grep -vE '...'`. This collapses 2000 lines to the 2–5 real ones instantly.
3. ⚠️ Line-ending pitfall: artifacts may be `\\r\\n`. When a decoy regex looks correct but matches nothing, strip `\\r` first (`line.rstrip('\\r')` / `tr -d '\\r'`). Python `splitlines()` already handles this.

### Technique B — template-NORMALIZATION clustering (preferred; use when no clean regex exists)
When decoy lines ROTATE fields (IPs, ports, numbers, hex) so a single regex is awkward, normalize and count templates instead. Mask every variable token to a placeholder, then the dominant template IS the decoy and every other template is a real event.
- Mask order: IPv4 → long hex (`\\b[0-9a-fA-F]{8,}\\b`) → `HH:MM:SS` times → `YYYY-MM-DD` dates → bracketed `[...]` → bare `\\b\\d+\\b` → strip.
- Pick the template with the highest count as decoy; print every line whose normalized form differs.
- This collapses 2050 lines of rotating-IP decoy to exactly the 2–5 anomalous events (phishing download, powershell launch, PSEXESVC install, VPN pivot, exfil POST) with zero false negatives.
- Runnable: `scripts/decoy_log_anomaly.py <file>` (prints non-dominant templates; also handles `\\r\\n`).
- PITFALL: a `c<=3` filter can hide a real block that repeats ~5×; prefer "everything that ISN'T the single dominant template" so repeated real events still surface.

### Where the real data hides
- A config block embedded among decoys (e.g. `cipher_stack = ...` / `vigenere_key = ...`), or a log line whose component/timestamp breaks the template (`SMSC-GW1-INTERCEPT` vs the normal `SMSC-GW1-{GW,CORE,SEC,...}`; a `14:10` timestamp vs all others at `10:00`).
- Do NOT verify decoy checksums — filter them out. Valid checksums on decoy lines are a distraction.
- pcap note: C2 pcaps are usually JUST beacon polling (`GET /beacon/poll?id=N` × hundreds) + SMB noise (`TreeConnect PSEXESVC`). Verify it's only beacon/SMB before over-investing in the pcap for the key — it rarely contains the archive password. Dump via `tshark -r x.pcap -T fields -e tcp.payload` then unhexlify; `tshark -r x.pcap -q -z follow,tcp,ascii,N` per stream.

### PowerShell `-Enc` decode
`powershell -Enc <b64>` → `base64.b64decode(s)` then try UTF-16LE FIRST, then latin1. In one engagement a "standard" UTF-16LE decode produced mojibake while latin1 gave the readable command (`BycodeDownloadData`). Always print both. Runnable: `scripts/powershell_enc_decode.py <b64>`.

### ⚠️ REASSEMBLY pitfall (the most common way to get a *silently truncated* flag): the real
   artifact is often NOT on one physical line. It can (a) wrap across 2+ lines, and/or (b) have
   DECOY TEXT APPENDED AFTER the real data on the continuation line. If you decode only the first
   fragment you get something like `flag{xor_repeating_key_` — a plausible-looking prefix with no
   closing brace, which tempts you to stop. Always do a 2-line window reassembly pass: after
   isolating the anomaly set, concatenate any fragmented blob (hex/base64/JWT/config) across
   adjacent lines, strip the trailing decoy tail, THEN decode. See `references/multiline_wrapped_artifact.md`.
See `references/noisy_log_decoy_analysis.md` for a fully worked example (the SMS-interception challenge).

## Reversing a labeled X_THEN_Y cipher stack
When the challenge TELLS you the stack — e.g. `cipher_stack = ROT13_THEN_VIGENERE` — use it literally and do NOT brute a cipher space you've already been told. The label describes the ENCRYPT order; decrypt by reversing:
- `ROT13_THEN_VIGENERE` → encrypt = ROT13 first, then Vigenère(key). Decrypt = **Vigenère-decrypt first, then ROT13**.
- A dead giveaway mid-decode: after Vigenère-decrypt you'll see ROT13-shaped text (`synt{`→`flag{`, `ebg13`→`rot13`); finish with ROT13.
- Event wrapper note: the inner recovered string is often `flag{...}` but the event wants a custom wrapper (`TRIVARNA{...}`, `CTF{...}`). Strip the inner content and re-wrap; submit the full wrapped string.
- Reusable solver: `scripts/reverse_cipher_stack.py --stack 'ROT13_THEN_VIGENERE' --key JIOKEY --ct '<ciphertext>'`. Supports ROT13/VIGENERE/BASE64/CAESAR/ATBASH/REVERSE, decrypts in reverse order automatically.

## Legacy ZipCrypto (PKZIP) nested-archive challenges ("Endless Archive" class)
Distinct from WinZip-AES (below): these use **legacy PKZIP encryption** (`zip2john`
reports `$pkzip$`; `7z l -slt` shows `Encrypted = +` and `Method = ZipCrypto Deflate/Store`).
The archive nests: layer N holds `password_(N-1).txt` (encoded pw for the next
archive) + `(N-1).{rar|zip}`. Repeat down to a final secret. Classic CTF trope:
"A seemingly harmless archive" ⇒ weak ZipCrypto ⇒ **known-plaintext attack**.

### Telling ZipCrypto from WinZip-AES at a glance
- `unzip -l` / `7z l -slt`: `Method = ZipCrypto Deflate` / `ZipCrypto Store` ⇒ legacy PKZIP.
  `method=99` / `flag_bits=1` ⇒ WinZip AES (use the AES section below).
- `zip2john file.zip`: `$pkzip$...` ⇒ PKZIP; `$zip2$...` ⇒ WinZip AES.

### Step 1 — get the OUTER password (the real gate)
The OUTER archive's password is the seed and is almost always **narrative-derived**
or **provided in the challenge brief** — it is rarely a rockyou word. Systematic order
(stop and re-derive once a step works):
1. `7z t -p<CAND> archive.zip` → "Everything is Ok" = VALID, "Wrong password" = wrong.
   **This `7z t` check is the GROUND TRUTH for ZipCrypto** — use it, not `zipfile`
   (zipfile can't decrypt ZipCrypto reliably and gives misleading results).
2. Try description/seed words, event name, the challenge title, numbers-as-words,
   hashes of seeds (md5/sha1/sha256). See the AES section's narrative-derivation list.
3. Dictionary: `john --wordlist=rockyou.txt hash.txt` (after `zip2john`), or
   `fcrackzip -D -p rockyou.txt archive.zip`. **First gunzip rockyou:**
   `gunzip -kf /usr/share/wordlists/rockyou.txt.gz` (only the `.gz` ships by default,
   so a bare path 404s — verify the file exists before blaming the password).
4. Numeric / short brute: `fcrackzip -b -c '1' -l 1-8` (numeric) or `-c 'aA1' -l 1-6`.
5. **If all automated attempts fail, the seed is almost certainly in the challenge
   brief / provided by the event.** Ask the user for the starting password or the
   full `.md` rather than grinding hours of 6-char brute force.

### Step 2 — bkcrack known-plaintext attack (the elegant bypass)
If you have ≥12 **contiguous, known** plaintext bytes of ANY ZipCrypto entry
(Store OR Deflate — see the Deflate note below), bkcrack recovers the 3 internal
keys WITHOUT the password. Install: the version pinned in older notes rots and 404s —
fetch the LATEST release asset via the GitHub API instead:
  `ver=$(curl -sL https://api.github.com/repos/kimci86/bkcrack/releases/latest | python3 -c "import sys,json;print(json.load(sys.stdin)['tag_name'])")`
  then download the `bkcrack-*-Linux-x86_64.tar.gz` asset and run `./bkcrack`.
- Attack: `bkcrack -C archive.zip -c "entry.jpg" -p plaintext_file.bin -o 0`
  (`-p` takes a **FILE path**, not inline text — write the candidate to disk first.
  `-o 0` = plaintext starts at offset 0 of the (decompressed) entry data.)
- Needs ≥12 contiguous bytes; a WRONG plaintext still runs the FULL Z-search
  (~46 min for ~709k Z-values at ~3%/min; ~75+ min for ~1.1M). Batch candidate
  plaintexts as SEPARATE background processes and check each for `KEY1 KEY2 KEY3`
  (a correct hit prints keys in seconds; wrong ones never print them). Don't kill
  early — a live search only prints `Could not find the keys` at 100%.
- Decrypt once keys are known:
  `bkcrack -C archive.zip -c "entry.jpg" -k K1 K2 K3 -d out.bin`  (raw deflate stream)
  then `zlib.decompress(out_bin[12:])` (skip the 12-byte ZipCrypto header) to recover
  the original file. For a Store entry, `-d out.txt` is the plaintext directly.
- **Deflate entries ARE usable KPA targets** (corrects older notes): the plaintext at
  offset 0 is the ENTRY FILE's first bytes, NOT the compressed stream. For a known
  file type the header is fully predictable:
  - JPEG/Exif (APP1) = `FFD8 FFE1 0010 4578 6966 0000`  ← realistic modern form (phones/cameras)
  - JPEG/JFIF       = `FFD8 FFE0 0010 4A46 4946 0001`  ← older/standard form
  - PNG             = `8950 4E47 0D0A 1A0A 0000 000D`  (sig + IHDR chunk length)
  - GIF89a          = `4749 4638 3961`  (only 6 bytes — too short; bkcrack needs ≥8, so
    GIF usually fails unless you also know the 2-byte width + 2-byte height)
  ⚠️ **Exif vs JFIF trap:** a FAILED JFIF (`FFD8FFE0`) search is NOT proof it isn't a
  JPEG. Retry with **Exif `FFD8FFE1`** — that is what virtually all real-world `.jpg`
  photos actually start with. The single swap `E0→E1` is frequently the difference
  between "Could not find the keys" and a solve (seen live: JFIF search completed
  fully and failed; Exif was the correct candidate).
- **Sizing tell:** a 25-byte Store `.txt` ≈ `base64(16 random bytes)+"\n"`. That has
  NO predictable prefix ⇒ **known-plaintext is impossible** for that file, and the
  OUTER password must be a provided seed. Don't waste the sweep — go ask for the seed.
- **Stripped-local-header reconstruction** (when zip2john/bkcrack can't parse the zip):
  if the challenge deleted the local file header ("broke the vessel"), the central dir
  + EOCD often survive. Rebuild a parseable zip so the tools work:
  1. Parse the central-dir entry (skip the 4-byte `504b0102` sig, then 15 fields:
     verMade,verNeed,flag,method,modT,modD,crc,csize,usize,fnLen,extraLen,commLen,
     diskStart,intAttr,extAttr,lho) → recovers crc/csize/usize/fnLen/extraLen.
  2. Write a LOCAL header: sig `504b0304`, ver20, flag, method, 0,0, crc, csize, usize,
     fnLen, extraLen, then filename + extra(zeros).
  3. Append the RAW encrypted bytes from the original file (these already include the
     12-byte ZipCrypto header).
  4. Append the central dir + EOCD, PADDING so the central dir lands exactly at the
     EOCD's recorded central-dir offset.
  Then `zip2john` yields a `$pkzip$` hash and `bkcrack` runs normally. Full worked
  recipe → `references/zip_local_header_reconstruction.md`.

### Step 3 — descend the chain
Once you can open a layer, read `password_(N-1).txt`, DECODE it (base64/hex/rot13/
reverse/raw — see `scripts/nested_archive_solver.py`), and use it to open `(N-1)`.
Reusable solver: `scripts/nested_archive_solver.py <outer.zip> <outer_pw> [--start N]`
(auto-detects layer from filename, tries all decodings, stops at the flag layer).
Needs `7z` + `unrar`.

## Cracking the WinZip-AES "exfil archive" (the usual final gate)
A forensic/IR challenge often ends with an encrypted `target/exfil_*.zip` that CONTAINS `flag.txt` (and maybe a CSV). `unzip -l` showing `method=99` / `flag_bits=1` = WinZip AES-256; the encrypted inner file is NOT the flag — its CONTENTS are. You must crack the OUTER password. Decision tree (full detail + commands in `references/zip_aes_cracking.md`):

⚠️⚠️ **CRITICAL PITFALL — Python `zipfile` CANNOT decrypt WinZip AES (this wasted a full session).**
`zipfile.ZipFile(...).read(pwd=...)` raises `NotImplementedError` for **every** password when the
archive uses WinZip AES (compress_type 99). This means `try_zip(pw)` returns `False` on a WRONG
password AND ALSO on the CORRECT password — so **all your brute-force "0 hits" are meaningless
until you validate the cracker itself.** A session burned ~30 candidate lists (rockyou, vocab,
kill-chain permutations, natural-language sentences) all reporting "0" — but every one of those
negatives was a lie because `zipfile` never actually tested the password.
**Always validate AES zips with a tool that genuinely supports AES:**
- `7z t archive.zip -pPASSWORD` → "Everything is Ok" on success, "Wrong password" on fail.
- `pyzipper` (venv: `python3 -m venv .venv && . .venv/bin/activate && pip install pyzipper`), then
  `pyzipper.AESZipFile(z).read(name, pwd=[REDACTED_SECRET] — raises on wrong pw, returns bytes on success.
  In-process pyzipper brute is ~1000× faster than spawning `7z` per candidate.
- `john` + `zip2john` (natively supports WinZip AES). **Prefer john over hashcat** for this:
  hashcat `-m 13600` (WinZip AES) uses a DIFFERENT `$zip2$` layout than john's `zip2john` output,
  so feeding a john hash to hashcat fails with "Signature unmatched" / "No hashes loaded". Re-using
  john's hash for hashcat needs a non-trivial format conversion that isn't worth it.
**Sanity-check FIRST:** create a test AES zip with a KNOWN password and confirm your tool reports it
before trusting any "0 cracks" run. See `references/zip_aes_cracking.md` + `scripts/aes_zip_crack.py`.
⚠️ **VENV NOTE — `execute_code` runs OUTSIDE any venv.** A `pyzipper` import there throws
`ModuleNotFoundError`. Either install into the base env OR activate the venv *inside* the
heredoc (`cd dir && . .venv/bin/activate && python3 - <<'PY' ...`). Same for any execute_code
needing venv-only packages.

1. `zip2john archive.zip > hash.txt` (extract rockyou first if needed: `gunzip -kf /usr/share/wordlists/rockyou.txt.gz`).
2. `john --wordlist=rockyou.txt hash.txt` — full rockyou on AES (PBKDF2-SHA1) takes ~10 min. Run in background; poll the `.pot`. **Verify the hash is well-formed** (`$zip2$*0*3*0*...`) before trusting a 0-result.
3. ⚠️ **PITFALL — if plain rockyou returns 0 cracks, STOP running rules.** `--rules=best64` ONLY mutates words already IN the wordlist, so if rockyou didn't contain the base word, rules cannot help. Chasing best64 after a 0-crack rockyou is the #1 time sink on these challenges (hit live: 14.3M rockyou = 0, then 3 rules jobs were doomed).
4. ⚠️ **PITFALL — `john` with a process-substitution wordlist fails silently.** `john --wordlist=<(echo pw)` errors with `ftell: Illegal seek` and reports 0 cracks even though the password is present. **Always pass a real file wordlist** (`printf 'pw\n' > /tmp/kw.txt; john --wordlist=/tmp/kw.txt ...`). (A test zip with a known password verified john works fine with a real file — the earlier "0 cracks" with `<()` were the bug, not the password.)
4. CTF AES-zip passwords are almost always NARRATIVE-DERIVED, not dictionary words. Derive candidates from the evidence, in order:
   - **Every distinct token** across all artifacts → build a vocab file, brute it (fast, catches embedded keys).
   - **MITRE/Lockheed 7-stage kill-chain verb concatenations** (`recon_weaponization_delivery_exploitation_installation_c2_exfiltration`, etc.) with separators `""`/`"_"`/`"-"`/`"."` and case variants — brute all permutations (≈111k, runs in seconds).
   - **Chronological assembly** of the 7 anomalous timestamps or 7 IoC hostnames.
   - **The "weird hash" fields** in logs (e.g. sysmon `MD5=`) are classic key-stashes — try them byte-exact (lower/upper).
   - **Distinctive multi-word artifact strings** (`TreeConnect PSEXESVC`, `invoice_99824.pdf.exe`, the C2 domain).
5. If still nothing after a FULL pass (rockyou verified-good + vocab + kill-chain + timestamps +
   distinctive strings + the "weird hash" fields): **STOP grinding the same exhausted wordlists.**
   For HARD challenges the user will tell you to "recheck everything / think differently" — do exactly that:
   - **Re-examine every artifact fresh.** The two most "designed" (non-random) strings in a challenge
     are deliberate clues: try them literal, reversed, XOR'd byte-wise, hashed, as raw bytes, and as
     keys for each other. Look again at memory CSVs (one real row among thousands of decoy `netscan`
     rows), pcaps, emails (attachments / base64 / hidden keys), and hidden files (`find . -name ".*"`).
   - **Prove the pcap is/ isn't useful:** `tshark -r x.pcap -q -z io,phs`. If it's only DNS + beacon
     GETs with NO POST bodies / NO SMB data, the exfil bodies aren't in it — don't over-invest.
   - **Search the web for similar writeups:** `<event> <challenge name> writeup` (e.g. "Trivarna CTF
     2.0 The Seven-Stage Breach"). 1-solve challenges often have none — expected — but the event name
     surfaces context and confirms the flag wrapper.
   - **Try structural derivations you skipped:** 2-word passphrases from relevant vocab (separators +
     cases), MD5/SHA of reconstruction sentences, reverse/leet/ROT13 of core story words.
   - **The derivation rule is likely spelled out in the challenge's brief/`.md`** (e.g. "password =
     [REDACTED_SECRET] of the 7 MITRE technique IDs"). Get that file / get the password. Don't burn hours
     brute-forcing a passphrase the author expects you to *construct* from the narrative.

## Support files
- `scripts/aes_zip_crack.py` — **reliable WinZip-AES cracker** using pyzipper (NOT zipfile). Has `--selftest` (creates a known-pw AES zip to prove validation works), `--info`, `--try`, and wordlist modes. Use this instead of any `zipfile`-based brute loop.
- `scripts/reverse_cipher_stack.py` — decrypt a labeled `X_THEN_Y` stack in reverse order (ROT13/VIGENERE/BASE64/CAESAR/ATBASH/REVERSE). Use when the challenge GIVES you the stack.
- `scripts/decoy_log_anomaly.py` — template-normalization clustering: prints every non-dominant-template line (the real events) in decoy-stuffed logs. Handles \\r\\n.
- `scripts/powershell_enc_decode.py` — decode a PowerShell `-Enc` blob, printing UTF-16LE + latin1 + utf-8 (catches the mojibake-vs-readable trap).
- `references/stego_decoy_archive.md` — multi-layer stego-archive method: key-fragment recovery, container descent, decoy-flag recognition, DCT-stego finale.
- `references/ble_capture_analysis.md` — condensed BLE/OTA capture CTF methodology + worked target-identification.
- `references/noisy_log_decoy_analysis.md` — fully worked decoy-log example (SMS-interception challenge).
- `references/multiline_wrapped_artifact.md` — wrap/reassembly pitfall (truncated-flag trap).
- `references/zip_aes_cracking.md` — WinZip-AES exfil-archive cracking decision tree + commands + the "plain rockyou 0 ⇒ rules can't help" pitfall.
- `references/zip_local_header_reconstruction.md` — rebuild a ZIP whose local file header was stripped ("broke the vessel") so zip2john/bkcrack can parse it; includes the central-dir `struct.unpack` field order and bkcrack Z-search timing.

## Pitfalls
- Don't assume the key derivation you first think of is right — but brute a WIDE key space and gate on real parses, not "looks readable".
- The `iv` field is often a real IV, not the key — but try it as a key too (cheap).
- If NOTHING validates after a wide brute, the scheme likely isn't in your space — you're missing the method (often documented in the challenge's task/description file, e.g. `silent_pairing.md`). Get that file before guessing further.
- Don't over-invest in tooling installs mid-solve; the `cryptography` lib already covers AES/CCM/GCM/RC4 needs.
- When a challenge GIVES you the cipher stack (e.g. `cipher_stack = ROT13_THEN_VIGENERE`), use it literally and decrypt in REVERSE order — do not brute a scheme you were already told. Beginners commonly reverse the order wrong (they ROT13-first when the stack says ROT13-first-encrypt, i.e. Vigenère-decrypt first).
- Noisy-log challenges: the answer is the ANOMALY among the decoys, not a "special" bulk line. Build the decoy regex and diff against it; ignore decoy checksums (they're valid on purpose, to distract).
- **Wrap/reassembly trap**: the anomaly line can wrap across multiple lines, and the continuation
  may carry decoy text *after* the real data (e.g. `5522...0002d  #0001: session_id=...`). Decoding
  only the first fragment yields a truncated-but-plausible prefix (no closing brace). Reassemble the
  full blob across adjacent lines and strip the trailing decoy before decoding. See
  `references/multiline_wrapped_artifact.md`.
- **Truncated-display trap**: when a JWT/long token is shown through stdout it may be ellipsized
  (`eyJ...fSJ9`). The full value is in the file — read it from disk and validate each candidate
  (one is the clean JSON payload, others are corrupted decoys). Don't trust the truncated view.
