#!/usr/bin/env python3
"""
aes_zip_crack.py — reliable WinZip-AES (.zip method 99) password cracker.

WHY THIS EXISTS:
  Python's stdlib `zipfile` CANNOT decrypt WinZip AES — it raises
  NotImplementedError for EVERY password (even the correct one). Any
  brute-force loop using `zipfile` reports false "0 hits". This script uses
  `pyzipper` (must be installed in an active venv) which genuinely validates
  AES passwords.

USAGE:
  # crack with a wordlist (one candidate per line)
  python3 aes_zip_crack.py archive.zip wordlist.txt

  # crack with a single candidate (quick check)
  python3 aes_zip_crack.py archive.zip --try "mypassword"

  # SELF-TEST: create a test AES zip with known pw, confirm detection works
  python3 aes_zip_crack.py --selftest

  # show info about the archive (salt, method) without cracking
  python3 aes_zip_crack.py archive.zip --info

Install pyzipper first (inside a venv):
  python3 -m venv .venv && . .venv/bin/activate && pip install pyzipper
NOTE: run this from the venv, since execute_code / other interpreters may
not see the venv's pyzipper.
"""
import sys, os

def _require_pyzipper():
    try:
        import pyzipper
        return pyzipper
    except ImportError:
        sys.exit("ERROR: pyzipper not importable. Activate the venv that has it "
                 "(python3 -m venv .venv && . .venv/bin/activate && pip install pyzipper).")

def archive_info(zp):
    pz = _require_pyzipper()
    with pz.AESZipFile(zp) as z:
        infos = z.infolist()
        print(f"entries: {len(infos)}")
        for i in infos:
            print(f"  name={i.filename!r} compress_type={i.compress_type} "
                  f"flag_bits={i.flag_bits} size={i.file_size}")
        # compress_type 99 == WinZip AES
        if infos and infos[0].compress_type == 99:
            print("  -> WinZip AES detected (method 99)")

def try_password(zp, pw):
    """Return True iff pw decrypts the first entry. Raises nothing."""
    pz = _require_pyzipper()
    try:
        with pz.AESZipFile(zp) as z:
            z.read(z.infolist()[0].filename, pwd=[REDACTED_SECRET]
        return True
    except Exception:
        return False

def crack_wordlist(zp, wordlist):
    n = 0
    with open(wordlist, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            pw = line.strip()
            if not pw:
                continue
            n += 1
            if try_password(zp, pw):
                print(f"FOUND: {pw}")
                return pw
            if n % 5000 == 0:
                print(f"  tested {n}...", flush=True)
    print(f"DONE_NONE (tested {n})")
    return None

def selftest():
    pz = _require_pyzipper()
    zp = "_aes_selftest.zip"
    KNOWN = "KNOWN_TEST_PW_2026"
    with pz.AESZipFile(zp, "w", compression=pz.ZIP_DEFLATED,
                       encryption=pz.WZ_AES) as z:
        z.setpassword(KNOWN.encode())
        z.writestr("x.txt", b"hello")
    print(f"created {zp} with password {KNOWN!r}")
    ok = try_password(zp, KNOWN)
    bad = try_password(zp, "definitely_wrong")
    print(f"  correct password accepted? {ok}  (expect True)")
    print(f"  wrong password rejected?   {not bad}  (expect True)")
    if ok and not bad:
        print("SELFTEST PASS — cracker validation is trustworthy.")
    else:
        print("SELFTEST FAIL — do NOT trust 0-crack results.")
    os.remove(zp)

def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__); sys.exit(2)
    if args[0] == "--selftest":
        selftest(); return
    if len(args) >= 1 and args[0].endswith(".zip") is False and args[0] != "--info":
        pass
    zp = args[0]
    if "--info" in args:
        archive_info(zp); return
    if "--try" in args:
        i = args.index("--try")
        pw = args[i+1]
        print(f"try {pw!r}: {'OK' if try_password(zp, pw) else 'NO'}")
        return
    # positional: archive + wordlist
    if len(args) < 2:
        print("need: archive.zip wordlist.txt  (or --try/--info/--selftest)"); sys.exit(2)
    crack_wordlist(zp, args[1])

if __name__ == "__main__":
    main()
