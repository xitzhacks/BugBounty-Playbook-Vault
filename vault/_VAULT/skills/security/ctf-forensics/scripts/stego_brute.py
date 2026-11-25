#!/usr/bin/env python3
"""
stego_brute.py - brute-force steghide + outguess passphrases on a set of images.

Usage:
  stego_brute.py <images_dir> <keyfiles_dir> [--steg-only] [--outg-only]

For every image (real JPEGs .jpg; WebP are converted to .bmp for steghide), it
tries a wide candidate passphrase set built ONLY from the provided key files:
  - every raw line from each key file
  - every distinct geo/name variant (regex 31.278N75.779[EW]... )
  - the clean form AND its base64 form for each
  - md5/sha1/sha256/sha512 of each key-fragment string
  - the full decoy flag strings found verbatim (UNI6{...})
  - trivials: empty, TRIVARNA, challenge name, common sub-tokens

Success = a produced output file whose content is >80% printable OR contains the
real flag wrapper. It deliberately does NOT treat outguess "usable bits" as
success (that is just JPEG entropy — see ctf-forensics skill references).

Requires: steghide + outguess binaries + libmcrypt.so.4 (extracted via
`apt-get download`, see references/stego_decoy_archive.md). Set LD_LIBRARY_PATH
to the extracted lib dir before running if steghide needs it.

This script is intended to be COPIED and adapted per challenge (paths to the
steghide/outguess binaries, the flag wrapper, the candidate derivation).
"""
import os, sys, re, base64, hashlib, subprocess, glob

IMAGES_DIR = sys.argv[1] if len(sys.argv) > 1 else "."
KEYS_DIR   = sys.argv[2] if len(sys.argv) > 2 else "."
FLAG_WRAP  = b"TRIVARNA"
STEGHIDE   = os.environ.get("STEGHIDE_BIN", "steghide_extract/usr/bin/steghide")
OUTGUESS   = os.environ.get("OUTGUESS_BIN", "outguess_extract/usr/bin/outguess")
LIBDIR     = os.environ.get("LD_LIBRARY_PATH", "")

def build_candidates(keys_dir):
    cands = set()
    for f in glob.glob(os.path.join(keys_dir, "*.txt")):
        for line in open(f, "rb").read().decode("latin1", "replace").splitlines():
            s = line.strip()
            if s:
                cands.add(s)
                # decoded b64 variant
                try:
                    dec = base64.b64decode(s, validate=True).decode("latin1")
                    cands.add(dec)
                except Exception:
                    pass
                # geo/name variant via regex on raw + decoded
                for src in (s, dec):
                    for m in re.findall(r"31\.278N75\.779[EW][^\r\n@]{0,2}[@%][^\\\r\n]{0,40}", src):
                        cands.add(m)
    # hashes of each
    for s in list(cands):
        b = s.encode("latin1", "replace")
        for fn in (hashlib.md5, hashlib.sha1, hashlib.sha256, hashlib.sha512):
            cands.add(fn(b).hexdigest())
            cands.add(fn(b).hexdigest().upper())
    # base64 of all
    for s in list(cands):
        try:
            cands.add(base64.b64encode(s.encode("latin1", "replace")).decode())
        except Exception:
            pass
    # trivials + sub-tokens
    for t in ["", "TRIVARNA", "trivarna", "ResidualSilence", "residual",
              "Gur", "Gar", "Gun", "Saran", "Saran6", "Naman", "Samar",
              "Sarin", "Sarun", "GurSaran", "GurSaran6"]:
        cands.add(t)
    return sorted(cands)

def main():
    env = dict(os.environ)
    if LIBDIR:
        env["LD_LIBRARY_PATH"] = LIBDIR + ":" + env.get("LD_LIBRARY_PATH", "")

    cands = build_candidates(KEYS_DIR)
    print(f"[*] {len(cands)} candidate passphrases")

    # gather images (real jpg + convert webp to bmp for steghide)
    imgs = []
    for p in glob.glob(os.path.join(IMAGES_DIR, "*.jpg")):
        imgs.append((p, "jpg"))
    # try steghide on bmp versions of webp too
    try:
        from PIL import Image
        for p in glob.glob(os.path.join(IMAGES_DIR, "*.jpg")):
            if open(p, "rb").read(4) == b"RIFF":
                bmp = p[:-4] + ".bmp"
                Image.open(p).convert("RGB").save(bmp)
                imgs.append((bmp, "bmp"))
    except Exception:
        pass

    hits = []
    for path, kind in imgs:
        for pw in cands:
            # steghide (jpg + bmp)
            if kind in ("jpg", "bmp") and os.path.exists(STEGHIDE):
                out = os.path.join(IMAGES_DIR, "_sb.txt")
                if os.path.exists(out): os.remove(out)
                subprocess.run([STEGHIDE, "extract", "-sf", path, "-p", pw,
                                "-xf", out], capture_output=True, text=True,
                               env=env, timeout=60)
                if os.path.exists(out) and os.path.getsize(out) > 0:
                    data = open(out, "rb").read()
                    if FLAG_WRAP in data or (sum(1 for x in data if 32 <= x < 127) / max(1, len(data)) > 0.8):
                        hits.append(("steghide", os.path.basename(path), pw, data[:150]))
                        print(f"[+] STEGHIDE HIT {os.path.basename(path)} pw={pw!r}")
                if os.path.exists(out): os.remove(out)
            # outguess (jpg only)
            if kind == "jpg" and os.path.exists(OUTGUESS):
                out = os.path.join(IMAGES_DIR, "_ob.txt")
                if os.path.exists(out): os.remove(out)
                r = subprocess.run([OUTGUESS, "-r", "-k", pw, path, out],
                                   capture_output=True, text=True, env=env, timeout=60)
                err = r.stderr + r.stdout
                if "too long" in err or "Floating" in err:
                    if os.path.exists(out): os.remove(out)
                    continue
                if os.path.exists(out) and os.path.getsize(out) > 0:
                    data = open(out, "rb").read()
                    if FLAG_WRAP in data or (sum(1 for x in data if 32 <= x < 127) / max(1, len(data)) > 0.8):
                        hits.append(("outguess", os.path.basename(path), pw, data[:150]))
                        print(f"[+] OUTGUESS HIT {os.path.basename(path)} pw={pw!r}")
                if os.path.exists(out): os.remove(out)

    print(f"[*] done. readable hits: {len(hits)}")
    for h in hits:
        print("   ", h[0], h[1], "pw=", h[2], "->", h[3])

if __name__ == "__main__":
    main()
