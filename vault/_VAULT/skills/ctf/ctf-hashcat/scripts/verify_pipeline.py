#!/usr/bin/env python3
"""verify_pipeline.py — prove a hashcat argon2 crack setup is correct before a long job.

Why: Argon2 is slow (~17 H/s on CPU). If your mode/salt/params are wrong, a 7-hour
mask attack silently exhausts with 0 recoveries. Validate the whole chain on a
known password ("test") using the EXACT same salt and parameters as the target hash.

Usage:
  1. Extract salt + params from the target hash line, e.g.
     $argon2id$v=19$m=65536,t=3,p=4$i/eOmAF+Qg40JHQAt4J/2A$sSPcLIMzrICGjBh3G5IcYZ
       type   = ID
       memory = 65536, time = 3, parallelism = 4
       salt_b64 = i/eOmAF+Qg40JHQAt4J/2A
  2. python3 verify_pipeline.py <target_hash> <known_password>
     e.g.  python3 verify_pipeline.py '$argon2id$v=19$m=65536,t=3,p=4$i/eOmAF+Qg40JHQAt4J/2A$sSPcLIMzrICGjBh3G5IcYZ' test
  3. The script writes verify.hash + verify.wl and runs:
       ./hashcat.bin -m 70000 -a 0 -D 1 --force target.hash verify.wl
     Expect to see "...:test" and "Status: Cracked".
"""
import sys, base64, subprocess, os
import argon2
from argon2.low_level import Type

def parse(hashline: str):
    # $argon2id$v=19$m=65536,t=3,p=4$SALT$HASH
    parts = hashline.strip().split("$")
    # parts[0] == '' ; parts[1] == 'argon2id' ; parts[2] == 'v=19'
    # parts[3] == 'm=...,t=...,p=...' ; parts[4] == salt ; parts[5] == hash
    assert parts[1].startswith("argon2"), "not an argon2 hash"
    typ = Type.ID if "id" in parts[1] else (Type.I if parts[1] == "argon2i" else Type.D)
    m, t, p = (int(x.split("=")[1]) for x in parts[3].split(","))
    salt = base64.b64decode(parts[4] + "==")  # pad to multiple of 4
    return typ, m, t, p, salt

def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)
    target, known = sys.argv[1], sys.argv[2]
    typ, m, t, p, salt = parse(target)
    h = argon2.low_level.hash_secret(
        known.encode(), salt, time_cost=t, memory_cost=m,
        parallelism=p, hash_len=32, type=typ,
    ).decode()
    with open("/tmp/verify.hash", "w") as f:
        f.write(h + "\n")
    with open("/tmp/verify.wl", "w") as f:
        f.write(known + "\nzzzz\n")
    print(f"[+] minted known hash: {h}")
    print(f"[+] params: type={typ.name} m={m} t={t} p={p} salt_len={len(salt)}")
    hc = os.path.join(os.path.dirname(__file__), "..", "hashcat.bin")
    # fall back to PATH
    cmd = [hc, "-m", "70000", "-a", "0", "-D", "1", "--force",
           "/tmp/verify.hash", "/tmp/verify.wl"]
    if not os.path.exists(hc):
        cmd[0] = "hashcat"
    print("[*] running:", " ".join(cmd))
    r = subprocess.run(cmd, capture_output=True, text=True)
    out = r.stdout + r.stderr
    for line in out.splitlines():
        if "Cracked" in line or "Recovered" in line or line.startswith("$argon2"):
            print(line)
    if "Cracked" in out:
        print("[+] PIPELINE OK — mode/salt/params are correct. Proceed with the real attack.")
    else:
        print("[!] Did NOT crack the known password. Check mode (70000), salt base64 padding, params.")

if __name__ == "__main__":
    main()
