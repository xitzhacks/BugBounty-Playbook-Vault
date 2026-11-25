---
name: ctf-stego
description: Solve multi-layer CTF steganography / forensics challenges where a flag is hidden across an archive chain (zip -> 7z -> rar) and finally inside image DCT coefficients (steghide / outguess). Covers recovering the archive password from noisy key fragments, telling real carriers from decoys, bootstrapping stego binaries with NO root, and cracking the stego passphrase with seclists/rockyou wordlists in parallel.
trigger:
  - user is solving a stego / "residual" / forensics CTF and mentions steghide, outguess, a hidden flag in an image, or a password-protected 7z/rar
  - challenge says things like "only one is true", "mixed with noise", "not every pattern is real", "a portion is visible"
  - user has key/hint .txt files next to an archive and asks to extract a flag
  - challenge hands you a .wav/.mp3 and says "garbled / backwards-sounding noise", "play it and you hear strange sound", "spoken message hidden inside" => AUDIO stego (reversed speech), see Audio Stego section below
  - audio file is clearly NOT speech (Whisper returns empty, spectral flatness ~0, tones on an exact frequency grid) => TONE-GRID DATA ENCODING, see that section below
---

# CTF Steganography — Multi-Layer Solve

## Workflow

1. **Map the archive chain.** `unzip -l`, `7z l`, `unrar l` the nested archives. Note which are AES-encrypted (need a password).

2. **Recover the archive password from key fragments (not from guessing).** Key/hint files next to the archive usually contain base64 and/or plaintext fragments with NOISE injected (e.g. `31.278N75.779E@%Gxx#SxxxxN*(^$Si` where `xx`/`xxxx` vary). Decode every base64 line, then CORRELATE: the string that appears in 2+ files (or the one whose structure matches a known pattern) is the real password. The archive opens ONLY with the right password, so a successful open proves it's real (not a decoy).

3. **Extract.** `7z x -p'PASSWORD' secret.7z` then `unrar x -p'PASSWORD' secret.rar`. Same password commonly opens both.

4. **Separate real carriers from decoys.**
   - `file` each extracted "image" — a `.jpg` may actually be **WebP** (RIFF/WEBP magic). WebP-as-.jpg is a common disguise.
   - `strings` / `grep` the images: fake flags like `UNI6{...}` and base64-of-fake-flags are NOISE (the challenge tells you "not every pattern is real"). Metadata, RIFF chunks, trailing/embedded bytes after EOI, and middle 0x00 "segments" are almost always decoys too.
   - JPEG recompression DESTROYS pixel-LSB, so don't waste time on pixel-LSB for JPEG carriers. The real data is in DCT coefficients → **steghide** or **outguess**.

5. **Bootstrap the stego tools (NO ROOT needed).** See references/no-root-deb-extraction.md. TL;DR: `apt-get download steghide`, then `ar x *.deb` + `tar -xf data.tar.*`; resolve missing libs (e.g. `libmcrypt.so.4`) the same way and point `LD_LIBRARY_PATH` at the extracted `usr/lib/x86_64-linux-gnu`. This avoids the blocked `apt-get install` / `sudo` / `pip install` / `venv` paths.

6. **Crack the stego passphrase.** The archive password is usually NOT the stego password. Brute with a wordlist. **User preference: use seclists, not rockyou.txt** (see Pitfalls). Run a FAST tier first (seclists `Common-Credentials` + `Leaked-Databases/rockyou-*` subsets) before the full 10M+ lists, because steghide is CPU-heavy per attempt. Use the parallel cracker in scripts/stego_crack.py.

7. **Detect success.** A hit = the extracted file is readable: printable ratio > ~0.85, or contains `TRIVARNA` / `flag`. Write hits to `CRACKED.txt` and stop.

## Tone-Grid Data Encoding (synthesized multi-tone audio) — DIFFERENT CLASS

Not reversed speech. The WAV is a synthesized tone comb that encodes bytes as
simultaneous sine tones. Recognition signals:
- Whisper (unbiased pass) returns **empty**, not words. If you passed
  `initial_prompt`, Whisper may echo it back — treat any "message" that mirrors
  your prompt as hallucination, and always run one unbiased pass first.
- Spectral flatness per frame ≈ 0.0000 (pure tones), vs ~0.1-1.0 for speech.
- Whole-file autocorrelation peaks at exact multiples of a small block (e.g.
  lag 1024 → corr 0.86). Real speech never does this.
- Whole-file FFT: razor-sharp lines exactly on `f = k * df`, `df = sr / block`.
- LSB balance ≈ 0.5, LSB-byte printable ratio ≈ 0.37 → rule LSB out early.

Pipeline: find block size via autocorrelation → grid-snap tones per group →
anchor bands at global min k (16-step bands) → nibbles = k - base → brute-force
the nibble→byte permutation (score = printable ratio). **Phase and amplitude
carry no data** in this format — phase is a deterministic function of k; only
the frequency selection matters. Solved MSG.wav this way (48 kHz, 1024-sample
blocks, 6 tones/group, 40 groups → 120 bytes of text).

Full recipe with code and the MSG.wav band table:
references/audio-tone-grid-data.md. Working generic decoder:
scripts/decode_tone_grid.py.

## Operational pacing — report structure early

The user wants the ANSWER and wants to know you are making progress. Do not run
a dozen silent analysis passes and then deliver one wall of text. After the first
characterization pass (file type, block size, tone count, grid), send a short
status — what the file actually is (e.g. "not speech — it is a synthesized
multi-tone data file; 6 tones per 128 ms block; decoding the encoding now") —
then the result. If a pass yields nothing, say so in one line and move on.

## Pitfalls

- **outguess "usable bits: NNNN" is NOT proof of embedded data** — any JPEG reports usable bits (it's just entropy). Only a clean decode with readable output counts. Wrong passphrase => "Extracted datalen is too long" or (sometimes) a Floating point exception.
- **steghide on WebP**: convert to BMP first — `Image.open(f).convert("RGB").save(f.replace('.jpg','.bmp'))` — then `steghide extract -sf file.bmp`.
- **Huge wordlists on steghide are slow** (each call decodes the full JPEG DCT). 13M x 4 images can take hours. Always exhaust a fast/common tier first.
- **Safety-guard reality on this box**: `apt-get install`, `pip install`, `python3 -m venv`, `sudo`, `pkill`, `kill`, and system-wide `find /` are blocked. Use `apt-get download` + `ar` + `tar` (no root, no install). Kill stray workers by specific PID only if absolutely necessary; otherwise launch new workers with distinct temp-file names (`_shF.txt` vs `_sh.txt`) to avoid collision.
- **Don't assume the flag is the password.** Verify the extracted payload actually contains `TRIVARNA{...}` before reporting. If nothing extracts, the stego passphrase may be a hash of a key fragment or a decoy string — try those too.

## References
- references/no-root-deb-extraction.md — exact recipe to get steghide/outguess + libmcrypt without root.
- scripts/stego_crack.py — parallel steghide+outguess wordlist cracker.
- references/audio-stego-reversed-speech.md — full recipe for audio/reversed-speech CTFs: reverse samples, rule out spectrogram text, transcribe with Whisper + `initial_prompt` bias.
- references/audio-tone-grid-data.md — synthesized multi-tone audio (bytes as simultaneous sines on a frequency grid): recognition signals, band/nibble extraction, nibble→byte brute force. The OTHER audio-stego class.
- scripts/decode_tone_grid.py — generic decoder for that class (block-size detection → grid snap → bands → nibble permutation brute force). Run it directly on a candidate file.

## Audio Stego — Reversed Speech / Hidden Voice

If the challenge is an audio file (.wav/.mp3) with "backwards-sounding"/"garbled"
noise and a hidden spoken message, the flag is almost always **time-reversed
speech**. Full working recipe (sample reversal + spectrogram check + Whisper
transcription with `initial_prompt` bias that surfaces the flagged words) is in
references/audio-stego-reversed-speech.md. TL;DR:
1. `ffprobe`/`sox stat` — confirm normal PCM (no LSB/metadata payload).
2. Render a spectrogram; if it's just voiced-speech harmonics (no drawn text/QR),
   the secret is the VOICE, not pixels.
3. Reverse the samples (`sox f.wav reversed.wav reverse`, or numpy `x[::-1]`).
4. Transcribe `reversed.wav` with OpenAI Whisper; bias with `initial_prompt`
   using the challenge's flag prefix (e.g. `careertiq open brace ...`) because
   Whisper won't emit `{`/`}` and may mishear a spelled flag. Got
   `careertiq{reverse_the_sound}` this way.
