#!/usr/bin/env python3
"""Parallel steghide + outguess wordlist cracker for CTF stego images.

Run:  python3 stego_crack_run.py <steghide|outguess> <wordlist.txt> [procs=8]
A HIT = extracted payload readable (printable>0.85) or contains TRIVARNA/flag.
Hits -> CRACKED.txt + printed. Kill stray workers by specific PID only.
Launch new runs in a fresh copy of the dir (or change _sh/_og temp names) to avoid
collision with a still-running worker.

Set D/SH/OG/LIBM/IMGS to your layout (see references/no-root-deb-extraction.md).
NOTE: this is the canonical runnable file; ignore the older scripts/stego_crack.py.
"""
import os, sys, subprocess, math

D = "/home/user/Ctf/tri/Rev/Residual Silence/extracted/secret"  # adjust
SH = os.path.join(D, "steghide_extract/usr/bin/steghide")
OG = os.path.join(D, "outguess_extract/usr/bin/outguess")
LIBM = os.path.join(D, "libm_extract/usr/lib/x86_64-linux-gnu")
IMGS = ["H2", "H3", "H4", "H7"]   # real JPEG carriers; adjust


def _readable(data):
    return b"TRIVARNA" in data or sum(1 for b in data if 32 <= b < 127) / max(1, len(data)) > 0.85


def try_steghide(pw, img):
    out = os.path.join(D, "_sh.txt")
    if os.path.exists(out): os.remove(out)
    subprocess.run([SH, "extract", "-sf", os.path.join(D, img + ".jpg"), "-p", pw, "-xf", out],
                   capture_output=True, text=True,
                   env={**os.environ, "LD_LIBRARY_PATH": LIBM}, timeout=60)
    if os.path.exists(out) and os.path.getsize(out) > 0:
        data = open(out, "rb").read(); os.remove(out)
        return _readable(data), data
    if os.path.exists(out): os.remove(out)
    return False, None


def try_outguess(pw, img):
    out = os.path.join(D, "_og.txt")
    if os.path.exists(out): os.remove(out)
    r = subprocess.run([OG, "-r", "-k", pw, os.path.join(D, img + ".jpg"), out],
                       capture_output=True, text=True, timeout=60)
    if "too long" in r.stderr + r.stdout or "Floating" in r.stderr + r.stdout:
        if os.path.exists(out): os.remove(out)
        return False, None
    if os.path.exists(out) and os.path.getsize(out) > 0:
        data = open(out, "rb").read(); os.remove(out)
        return _readable(data), data
    if os.path.exists(out): os.remove(out)
    return False, None


def worker(mode, start, end, wl):
    fn = try_steghide if mode == "steghide" else try_outguess
    with open(wl, "r", errors="replace") as f:
        for i, line in enumerate(f):
            if i < start: continue
            if i >= end: break
            pw = line.rstrip("\n")
            if not pw: continue
            for img in IMGS:
                try:
                    ok, data = fn(pw, img)
                except Exception:
                    continue
                if ok:
                    with open(os.path.join(D, "CRACKED.txt"), "a") as o:
                        o.write(f"[{mode}] {img}.jpg pw={pw!r} -> {data[:200]!r}\n")
                    print(f"CRACKED [{mode}] {img}.jpg pw={pw!r} -> {data[:120]!r}")
                    sys.stdout.flush()


def orchestrate(mode, wl, procs=8):
    total = int(subprocess.check_output(["wc", "-l", wl]).split()[0])
    chunk = math.ceil(total / procs)
    ps = []
    for i in range(procs):
        s, e = i * chunk, min(s + chunk, total)
        p = subprocess.Popen([sys.executable, __file__, "worker", mode, str(s), str(e), wl],
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        ps.append(p)
        print(f"launched {mode} worker {i} [{s}:{e}] pid={p.pid}")
    cracked = False
    while ps:
        for p in list(ps):
            line = p.stdout.readline()
            if line:
                sys.stdout.write(line); sys.stdout.flush()
                if "CRACKED" in line: cracked = True
            if p.poll() is not None:
                for l in p.stdout: sys.stdout.write(l)
                ps.remove(p)
    print(f"ALL {mode} WORKERS DONE. cracked={cracked}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "worker":
        worker(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5])
    else:
        mode = sys.argv[1] if len(sys.argv) > 1 else "steghide"
        wl = sys.argv[2] if len(sys.argv) > 2 else os.path.join(D, "seclists.txt")
        procs = int(sys.argv[3]) if len(sys.argv) > 3 else 8
        orchestrate(mode, wl, procs)
