#!/usr/bin/env python3
"""Generic decoder for tone-grid audio steganography.

An audio file is not speech but a synthesized comb of sine tones whose
frequencies sit on an exact grid f = k * (sr / block). Tones are grouped into
symbols; each symbol carries N 4-bit nibbles (one per frequency band), and the
nibbles assemble into bytes in an unknown permutation.

Usage:
    python3 decode_tone_grid.py FILE.wav [--sr 48000] [--max-block 8192]

Pipeline:
  1. detect block size from whole-file autocorrelation
  2. snap tones to the grid k * (sr / block)
  3. segment into symbol groups (consecutive blocks with identical tone sets)
  4. split tones into bands anchored at the global minimum k
  5. brute-force the nibble->byte permutation, scored by printable ratio

Validated on MSG.wav (48 kHz mono, 1024-sample blocks, 6 tones/group,
40 payload groups -> 120 bytes of text).
"""
import argparse
import itertools
import sys

import numpy as np
from scipy.io import wavfile
from scipy.signal import find_peaks, windows


def detect_block_size(x, sr, max_block=8192):
    """Find the sample period the signal is built from."""
    xx = x - x.mean()
    n = len(xx)
    ac = np.correlate(xx, xx, "full")[n - 1:]
    ac /= ac[0]
    lim = min(n // 2, max_block)
    pk, props = find_peaks(ac[:lim], height=0.2, distance=50)
    cands = []
    for p, h in zip(pk, props["peak_heights"]):
        if p < 64:
            continue
        # prefer periods that divide the file length
        divides = (n % p) == 0
        cands.append((divides, h, int(p)))
    cands.sort(key=lambda t: (not t[0], -t[1]))
    if not cands:
        raise SystemExit("no autocorrelation peaks — not a periodic tone comb?")
    return cands[0][2]


def group_tones(x, sr, block, df, edge_trim=0.25):
    """Return list of (start_block, end_block, sorted k list)."""
    n = len(x)
    nb = n // block
    blocks = x[: nb * block].reshape(nb, block)

    def tones_of(b):
        seg = blocks[b].copy()
        # trim edges to avoid bleed from neighbouring symbols
        t = int(block * edge_trim)
        seg = seg[t: block - t] if block - 2 * t > 64 else seg
        seg = seg * np.hanning(len(seg))
        X = np.abs(np.fft.rfft(seg, n=max(8192, len(seg) * 4)))
        fr = np.fft.rfftfreq(len(X), 1 / sr)
        thr = X.max() * 0.15
        out = []
        for i in range(2, len(X) - 2):
            if X[i] > thr and X[i] >= X[i - 1] and X[i] >= X[i + 1]:
                a, b, c = X[i - 1], X[i], X[i + 1]
                d = 0.5 * (a - c) / (a - 2 * b + c + 1e-12)
                f = fr[i] + d * (fr[1] - fr[0])
                k = int(round(f / df))
                if abs(f - k * df) < df * 0.2:
                    out.append(k)
        return tuple(sorted(set(out)))

    fps = [tones_of(b) for b in range(nb)]
    groups = []
    for b, fp in enumerate(fps):
        if not fp:
            continue
        if groups and groups[-1][2] == fp:
            groups[-1] = (groups[-1][0], b, fp)
        else:
            groups.append((b, b, fp))
    return groups


def split_bands(groups, n_bands):
    """Anchor bands at the global minimum k, 16 grid steps apart."""
    kmin = min(min(g[2]) for g in groups)
    bases = [kmin + 16 * i for i in range(n_bands)]
    syms = []
    for a, b, ks in groups:
        nib = []
        ok = True
        for base in bases:
            matches = [k for k in ks if base <= k < base + 16]
            if len(matches) != 1:
                ok = False
                break
            nib.append(matches[0] - base)
        if ok and len(nib) == n_bands:
            syms.append((a, b, nib))
    return bases, syms


def score_bytes(b):
    if not b:
        return 0.0
    return sum(32 <= c < 127 for c in b) / len(b)


def brute_force_bytes(syms, n_nib):
    """Try every nibble-slot permutation; return the best-scoring decode."""
    best = None
    for perm in itertools.permutations(range(n_nib)):
        if n_nib % 2:
            continue
        out = []
        for _, _, nib in syms:
            out.append(bytes(
                (nib[perm[i]] << 4) | nib[perm[i + 1]]
                for i in range(0, n_nib, 2)
            ))
        b = b"".join(out)
        s = score_bytes(b)
        if best is None or s > best[0]:
            best = (s, perm, b)
    return best


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--sr", type=int, default=None)
    ap.add_argument("--max-block", type=int, default=8192)
    ap.add_argument("--n-bands", type=int, default=6)
    ap.add_argument("--min-groups", type=int, default=2,
                    help="ignore groups shorter than this many blocks (framing)")
    args = ap.parse_args()

    sr, x = wavfile.read(args.file)
    if x.ndim > 1:
        x = x.mean(axis=1)
    x = x.astype(np.float64)
    sr = args.sr or sr
    print(f"file: {args.file}  sr={sr}  samples={len(x)}  dur={len(x)/sr:.3f}s")

    block = detect_block_size(x, sr, args.max_block)
    df = sr / block
    print(f"block size: {block} samples ({block/sr*1000:.2f} ms)  "
          f"grid df={df:.4f} Hz  blocks={len(x)//block}")

    groups = group_tones(x, sr, block, df)
    print(f"tone groups: {len(groups)}")
    counts = sorted({len(g[2]) for g in groups})
    print(f"distinct tone counts: {counts}")

    # payload = groups with the modal tone count and enough duration
    from collections import Counter
    modal = Counter(len(g[2]) for g in groups).most_common(1)[0][0]
    payload = [g for g in groups if len(g[2]) == modal
               and (g[1] - g[0] + 1) >= args.min_groups]
    print(f"modal tone count={modal}; payload groups={len(payload)}")

    bases, syms = split_bands(payload, args.n_bands)
    print(f"bases: {bases}  symbols decoded: {len(syms)}")
    if not syms:
        raise SystemExit("band split failed — try --n-bands")

    s, perm, b = brute_force_bytes(syms, args.n_bands)
    print(f"\nbest permutation {perm}  printable={s:.3f}")
    print("=" * 60)
    print(b.decode("ascii", errors="replace"))
    print("=" * 60)
    print(f"hex: {b.hex()}")


if __name__ == "__main__":
    main()
