#!/usr/bin/env python3
"""powershell_enc_decode.py — decode a PowerShell -Enc base64 blob.

PowerShell -Enc expects base64 of UTF-16LE. But sometimes the intended readable
string is plain base64-of-ASCII (UTF-16LE decode yields mojibake). This prints BOTH
so you never miss the real command.

Usage:  python3 powershell_enc_decode.py <base64string>
"""
import sys, base64

def main():
    if len(sys.argv) < 2:
        print("usage: python3 powershell_enc_decode.py <base64>")
        sys.exit(1)
    enc = sys.argv[1].strip()
    raw = base64.b64decode(enc)
    print("bytes:", raw)
    try:
        print("UTF-16LE:", raw.decode('utf-16-le'))
    except Exception as e:
        print("UTF-16LE err:", e)
    print("latin1  :", raw.decode('latin1'))
    try:
        print("utf-8   :", raw.decode('utf-8'))
    except Exception as e:
        print("utf-8 err:", e)

if __name__ == "__main__":
    main()
