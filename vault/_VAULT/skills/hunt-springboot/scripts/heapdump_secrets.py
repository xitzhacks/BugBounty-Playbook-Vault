#!/usr/bin/env python3
"""
heapdump_secrets.py — extract leaked secrets / flags from a Java HPROF heap dump
when naive `strings | grep` drowns in JAR-path noise or misses binary-delimited
property values.

Why this exists: a Spring Boot `actuator/heapdump` challenge (e.g. the
"actuatorlab" lab) stores the Spring `Environment` property sources in the dump,
but the property NAME and VALUE are separated by raw 0x21 ('!') delimiter bytes
inside HPROF record bodies — not adjacent in any `strings` line. A plain
`strings | grep 'aws.secret.key'` sees the name but NOT the value (the value
lives bytes away). This script reconstructs name->value pairs and pulls raw
secret bytes directly.

Usage:
  python3 heapdump_secrets.py /path/to/heapdump [--out findings.txt]
"""
import sys, re

def main():
    if len(sys.argv) < 2:
        print("usage: heapdump_secrets.py <heapdump> [--out file]")
        sys.exit(1)
    path = sys.argv[1]
    out = None
    if "--out" in sys.argv:
        out = sys.argv[sys.argv.index("--out") + 1]
    data = open(path, "rb").read()
    print(f"[i] loaded {len(data)} bytes from {path}")

    findings = []

    # 1) Raw AWS access key bytes (the '...' in 'AKIAQF...DHFI' is non-printable
    #    truncation in the strings view — grab raw to see if it's a real key or
    #    a redacted placeholder).
    for m in re.finditer(rb"AKIA[A-Z0-9]{2,40}", data):
        seg = m.group()
        after = data[m.end():m.end()+12]
        cont = ''.join(chr(b) if 32 <= b < 127 else '.' for b in after)
        findings.append(("AWS_ACCESS_KEY_ID", seg.decode() + "  (next bytes: " + cont + ")"))
        print(f"[+] AWS_ACCESS_KEY_ID: {seg.decode()}  next: {cont}")

    # 2) aws_secret_access_key=VALUE (value may be base64/url-safe chars)
    for m in re.finditer(rb"aws_secret_access_key=([^\"!\x00]{6,120})", data):
        val = m.group(1).decode(errors="replace").rstrip("!")
        findings.append(("AWS_SECRET_ACCESS_KEY", val))
        print(f"[+] AWS_SECRET_ACCESS_KEY: {val}")

    # 3) Spring Environment properties: name ends with '!', value is next
    #    printable run (separated by binary bytes). Reconstruct pairs.
    props = {}
    for m in re.finditer(rb"([a-zA-Z][a-zA-Z0-9_.\[\]]{3,80})!", data):
        key = m.group(1).decode()
        rest = data[m.end():m.end()+400]
        vm = re.match(rb"[\x00-\x1f\x21-\x2f]*([ -~]{2,200})", rest.lstrip(
            b"\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f"
            b"\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\r\x1c\x1d\x1e\x1f"))
        if vm:
            val = vm.group(1).decode().rstrip("!")
            if "/" in val or ";" in val:
                continue
            props[key] = val
    if props:
        print("\n[+] Reconstructed Spring Environment properties:")
        for k, v in props.items():
            findings.append(("ENV:" + k, v))
            print(f"    {k}  =  {v}")

    # 4) Explicit flag search (usually ABSENT in the dump — flag normally lives
    #    on the LIVE /actuator/env endpoint, not in plaintext here).
    flag_pat = re.compile(rb"flag\{[^}]*\}|ctf\{[^}]*\}|FLAG\{[^}]*\}|CTF\{[^}]*\}|flag\s*[:=]\s*[^\x00]{4,80}", re.I)
    flags = [f.group() for f in flag_pat.finditer(data)]
    if flags:
        print(f"\n[+] FLAG FOUND in dump: {flags[:5]}")
        for f in flags[:5]:
            findings.append(("FLAG", f.decode(errors="replace")))
    else:
        print("\n[!] No literal flag{...} in dump. For actuatorlab-style labs the flag")
        print("    is a property on the LIVE /actuator/env endpoint (e.g. flag /")
        print("    app.flag / secret.flag). Hit that URL; do NOT expect it here.")

    # 5) Distractor-token warning: random-looking alnum tokens (>=20 chars, mixed
    #    case or digits) are USUALLY class/method names or noise, not secrets.
    seen = set()
    print("\n[~] Low-confidence random tokens (likely noise — verify before using):")
    for t in re.findall(rb"[A-Za-z0-9]{20,40}", data):
        s = t.decode()
        if s in seen: continue
        seen.add(s)
        if any(c.isdigit() for c in s) or (any(c.islower() for c in s) and any(c.isupper() for c in s)):
            if not s.lower().startswith(("java","org","com","sun","io/","jdk")):
                print(f"    {s}")

    if out:
        with open(out, "w") as f:
            for k, v in findings:
                f.write(f"{k} = {v}\n")
        print(f"\n[+] wrote {len(findings)} findings to {out}")

if __name__ == "__main__":
    main()
