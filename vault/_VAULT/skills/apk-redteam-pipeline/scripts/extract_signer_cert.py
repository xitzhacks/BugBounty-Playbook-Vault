#!/usr/bin/env python3
"""
extract_signer_cert.py — Pull the APK V2/V3 signer certificate(s) from the APK Signing Block
and print subject / issuer / validity / SHA-256 fingerprint.

WHY: `keytool -printcert -jarfile` and `META-INF/*.RSA` extraction FAIL on V2/V3-only signed
APKs (no standalone .RSA file). This parses the signing block directly so you can prove an APK
is the genuine vendor build (anti-repak / provenance check) before reporting.

USAGE:
    python3 extract_signer_cert.py <base.apk>
    python3 extract_signer_cert.py /path/to/com.gworks.oneapp.works.apk

No external deps (stdlib + openssl on PATH for pretty-print).
"""
import struct, hashlib, subprocess, sys, os, tempfile

def find_signing_block(data):
    magic = b"APK Sig Block 42"
    idx = data.rfind(magic)
    if idx == -1:
        return None
    size_off = idx - 8
    (block_size,) = struct.unpack("<Q", data[size_off:size_off+8])
    return data[size_off - block_size:idx]

def collect_certs(block):
    certs = []
    i = 0
    while True:
        p = block.find(b"\x30\x82", i)
        if p == -1:
            break
        (ln,) = struct.unpack(">H", block[p+2:p+4])
        der = block[p:p+4+ln]
        if len(der) == 4 + ln and der[4] in (0x30, 0xA0, 0x02):
            certs.append(der)
        i = p + 1
    return certs

def main():
    if len(sys.argv) < 2:
        print("usage: extract_signer_cert.py <base.apk>")
        return 2
    apk = sys.argv[1]
    if not os.path.isfile(apk):
        print(f"[!] not found: {apk}")
        return 2
    with open(apk, "rb") as f:
        data = f.read()
    block = find_signing_block(data)
    if not block:
        print("[!] No APK Signing Block found (maybe V1-only). Try: keytool -printcert -jarfile")
        return 1
    certs = collect_certs(block)
    if not certs:
        print("[!] No embedded cert parsed from signing block.")
        return 1
    print(f"[*] Signer certificates found: {len(certs)}")
    for n, der in enumerate(certs[:5], 1):
        sha = hashlib.sha256(der).hexdigest()
        with tempfile.NamedTemporaryFile(suffix=".der", delete=False) as tf:
            tf.write(der); path = tf.name
        try:
            out = subprocess.check_output(
                ["openssl", "x509", "-inform", "DER", "-noout",
                 "-subject", "-issuer", "-dates", "-fingerprint", "-sha256"],
                stdin=open(path, "rb"), stderr=subprocess.DEVNULL).decode()
            print(f"\n--- Signer cert #{n} ---")
            print(out)
            print(f"(raw SHA256: {sha})")
        except Exception as e:
            print(f"[!] openssl parse failed for cert #{n}: {e}")
        finally:
            os.unlink(path)
    print("\n[CHECK] Compare Subject/Issuer to the official publisher. 'CN=Android Debug' = debug")
    print("        build (reject). Self-signed corp cert (O=nhn etc.) may be legit enterprise")
    print("        signing — confirm against the app's package namespace + Play/mirror listing.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
