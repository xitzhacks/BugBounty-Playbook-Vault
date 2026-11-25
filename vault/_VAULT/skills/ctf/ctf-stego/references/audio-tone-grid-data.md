# Audio Stego — Tone-Grid Data Encoding (synthesized multi-tone audio)

A DIFFERENT class from reversed speech. Here the WAV is not a recording at all —
it is a **synthesized tone comb** that encodes bytes as simultaneous sine tones.
The "message" is machine-generated audio carrying text/data, not a hidden voice.

Worked example solved from scratch: `MSG.wav` (48 kHz mono PCM, 5.67 s) →
"Overjoyed to share that our baby boy Shree is here, mom and baby are doing great!"

## Recognition — how to tell this class from speech stego

Run these before assuming "reversed speech":

1. `whisper transcribe` returns **empty string** (not words). Strong signal it is
   not speech. NOTE: if you pass `initial_prompt` with flag-ish text, Whisper
   will HALLUCINATE that prompt back as the transcript. Always run one unbiased
   pass first; treat any "message" that echoes your prompt as noise.
2. Spectral flatness per frame ≈ 0.0000 (pure tones), not ~0.1-1.0 (speech/noise).
3. `sox file.wav -n stat` → very stable RMS, no silence gaps (synthesis, not speech).
4. Whole-file autocorrelation has strong peaks at exact multiples of a small
   block length (e.g. lag 1024 → corr 0.86). Real speech never does this.
5. Whole-file FFT shows razor-sharp lines exactly on a grid; measure `k = f / df`
   and check `k` is an integer. `df = sr / block_size` (48000/1024 = 46.875 Hz).
6. LSB balance ≈ 0.5 and LSB-byte printable ratio ≈ 0.37 → no LSB payload.
   Rule this out early so you don't burn time on it.

## Analysis recipe

### 1. Find the block size and grid
```python
import numpy as np
from scipy.io import wavfile
from scipy.signal import find_peaks
sr, x = wavfile.read("file.wav"); x = x.astype(np.float64)
xx = x - x.mean()
ac = np.correlate(xx, xx, 'full')[len(xx)-1:]; ac /= ac[0]
pk, _ = find_peaks(ac[:sr], height=0.2, distance=50)
# pick the peak p where len(x) % p == 0 and p >= 256
```
MSG.wav: `p = 1024` samples = 21.333 ms, `len(x) = 272384 = 266 * 1024`.
Grid: `df = sr / p` → 46.875 Hz. Every tone is `k * df` for integer k.

### 2. Segment into symbol groups
Concatenate consecutive blocks with identical tone sets into groups. MSG.wav:
blocks 0-15 and 250-265 are 16-tone **framing** markers (intro/outro); blocks
16-249 are the payload, 6 blocks (128 ms) per group → 40 groups.

### 3. Extract tones per group (flat-top window for accuracy)
```python
from scipy.signal import windows
wt = windows.flattop(4096)
seg = x[a*p:(b+1)*p][1024:1024+4096] * wt
X = np.abs(np.fft.rfft(seg, n=4096*4)) / wt.sum() * 2
fr = np.fft.rfftfreq(4096*4, 1/sr)
# quadratic-interpolate each local max, snap to nearest k*df, keep |f - k*df| < 3 Hz
```
Use a window that is long relative to the block and skip the group edges.

### 4. Find the bands
All tones fall into a small number of fixed frequency bands, each 16 grid steps
wide. Anchor at the global minimum k:
```python
kmin = min(k for group in groups for k in group)
bases = [kmin + 16*i for i in range(n_bands)]   # MSG.wav: [40,56,72,88,104,120]
```
Each band carries one 4-bit nibble: `nibble = k - base`.

MSG.wav bands (k, base 40/56/72/88/104/120), Hz:
| band | k range | Hz range |
|------|---------|----------|
| 0 | 40-55 | 1875-2578 |
| 1 | 57-70 | 2672-3281 |
| 2 | 72-87 | 3375-4078 |
| 3 | 88-103 | 4125-4828 |
| 4 | 104-119 | 4875-5578 |
| 5 | 120-135 | 5625-6328 |

### 5. Decode the nibbles → bytes (the part that needs brute force)
6 nibbles per group = 180 nibbles total = 120 bytes. The pairing of nibbles into
bytes is NOT the naive order. Brute-force all 6! permutations of the nibble
slots, build 3 bytes per group, and score by printable-character ratio:

```python
import itertools
def score(b): return sum(32 <= c < 127 for c in b) / len(b)
best = None
for perm in itertools.permutations(range(6)):
    out = []
    for row in nib:   # row = 6 nibbles for one group
        out.append(bytes([(row[perm[0]]<<4)|row[perm[1]],
                          (row[perm[2]]<<4)|row[perm[3]],
                          (row[perm[4]]<<4)|row[perm[5]]]))
    b = b"".join(out)
    if best is None or score(b) > best[0]:
        best = (score(b), perm, b)
```
MSG.wav winner: `perm = (1,0,3,2,5,4)` → `(n1<<4)|n0, (n3<<4)|n2, (n5<<4)|n4`,
score 0.775, and the result is clean English from byte 3 to byte 84. Also try
reversing group order and the whole nibble stream; the same permutation family
usually wins.

## Pitfalls

- **Phase is a red herring.** In this format every tone's phase is a deterministic
  function of its own k (measured phases were exact integer multiples of π/24,
  and the same k always had the same phase). Phase and amplitude carry NO data —
  only the frequency selection does. Don't waste time on phase demodulation.
- **Don't trust the first readable-looking decode.** Several permutations give
  ~0.77 printable. Only one gives grammatical English; check the actual text.
- **Tones are exactly periodic**, so a long FFT of a whole group resolves them
  cleanly; a short window smears them across bins and the k snap fails.
- **Framing blocks** (16 tones) at the start/end are not payload. Detect them by
  tone count per block, not by position.
- **Report structural findings as you go** (block size, grid, band count, tone
  count, band ranges) instead of running many silent analysis passes. The user is
  waiting on one answer; a short "here's what the file is" after the first
  characterization pass keeps them oriented.

## Reusable decoder

`scripts/decode_tone_grid.py` implements the whole pipeline generically:
block-size detection → grid snap → band extraction → nibble brute-force.
Validated on MSG.wav.
