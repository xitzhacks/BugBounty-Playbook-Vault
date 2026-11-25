#!/usr/bin/env python3
"""
Nested encrypted-archive solver for "Endless Archive"-style CTF challenges.

Pattern it handles:
  Layer N (e.g. 2500.zip) contains:
    - password_(N-1).txt   -> ENCODED password for the next archive (N-1)
    - (N-1).{zip|rar}      -> the next encrypted archive
  Each layer hides the password for the next. The encoded password file is
  usually base64(16 random bytes)+"\\n" (25 bytes) or a labelled/hex/rot13 form.

Usage:
  python3 nested_archive_solver.py <outer_archive> <outer_password> [--start N]

It tries many decodings of each password file (raw/base64/hex/rot13/reverse)
and picks the one that actually opens the next archive, descending until it
reaches a layer with no further archive (the flag layer).

Requires: 7z (zipcrypto zips), unrar (rar). Pure-stdlib otherwise.
"""
import os, sys, subprocess, base64, codecs, argparse

def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)

def decode_password(raw: bytes):
    """Yield candidate plaintext strings for an encoded password file."""
    cands = []
    try:
        cands.append(raw.decode(errors="strict").strip())
    except Exception:
        pass
    s = raw.strip()
    for b in (s, s + b"=", s + b"==", s + b"==="):
        try:
            cands.append(base64.b64decode(b).decode(errors="strict").strip())
        except Exception:
            pass
    try:
        cands.append(bytes.fromhex(s.decode()).decode(errors="strict").strip())
    except Exception:
        pass
    try:
        cands.append(codecs.decode(s.decode(), "rot_13").strip())
    except Exception:
        pass
    try:
        cands.append(s.decode()[::-1].strip())
    except Exception:
        pass
    # de-dup, keep order
    seen = set()
    out = []
    for c in cands:
        if c and c not in seen:
            seen.add(c)
            out.append(c)
    return out

def extract(path, pw, dest, is_zip):
    os.makedirs(dest, exist_ok=True)
    if is_zip:
        r = run(["7z", "x", "-y", f"-p{pw}", f"-o{dest}", path])
        ok = "Everything is Ok" in (r.stdout + r.stderr) or bool(os.listdir(dest))
    else:
        r = run(["unrar", "x", "-y", f"-p{pw}", path, dest + "/"])
        ok = (r.returncode == 0) or bool(os.listdir(dest))
    return ok

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("archive")
    ap.add_argument("outer_password")
    ap.add_argument("--start", type=int, default=None, help="layer number of the outer archive")
    args = ap.parse_args()

    # infer start layer from filename like 2500.zip / 2499.rar
    import re
    m = re.search(r"(\d+)", os.path.basename(args.archive))
    layer = args.start if args.start else (int(m.group(1)) if m else None)
    if layer is None:
        print("Could not infer layer number; pass --start N"); sys.exit(1)

    cur = args.archive
    is_zip = cur.lower().endswith(".zip")
    pw = args.outer_password
    root = os.path.join(os.path.dirname(os.path.abspath(cur)), "chain_" + os.path.basename(cur).replace(".", "_"))

    while True:
        dest = os.path.join(root, f"L{layer}")
        print(f"[+] Layer {layer}: {os.path.basename(cur)}  pw={pw!r}")
        if not extract(cur, pw, dest, is_zip):
            print("   extraction FAILED; stop. (wrong pw or non-zipcrypto rar?)")
            break
        files = [f for f in os.listdir(dest) if os.path.isfile(os.path.join(dest, f))]
        pwfile = next((f for f in files if f.startswith("password_")), None)
        nextarch = next((f for f in files if f not in (pwfile,) and f.endswith((".rar", ".zip"))), None)
        if not pwfile:
            print("   NO password file -> final layer. Contents:")
            for f in files:
                p = os.path.join(dest, f)
                print(f"   --- {f} ---")
                print(open(p, "rb").read()[:500])
            break
        raw = open(os.path.join(dest, pwfile), "rb").read()
        print(f"   {pwfile}: {len(raw)} bytes -> {raw[:40]!r}")
        cands = decode_password(raw)
        print(f"   decode candidates ({len(cands)}): {cands[:8]}")
        if not nextarch:
            print("   NO next archive -> final flag file present:")
            for f in files:
                if f != pwfile:
                    print(open(os.path.join(dest, f), "rb").read()[:500])
            break
        np = os.path.join(dest, nextarch)
        nz = np.lower().endswith(".zip")
        opened = False
        for c in cands:
            if extract(np, c, os.path.join(root, f"L{layer-1}_try"), nz):
                pw, opened = c, True
                break
        if not opened:
            print("   NONE of the decoded candidates opened the next archive.")
            print("   raw password file was:", raw)
            break
        print(f"   => next password = [REDACTED_SECRET]")
        layer -= 1
        cur, is_zip = np, nz

if __name__ == "__main__":
    main()
