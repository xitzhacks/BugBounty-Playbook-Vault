#!/usr/bin/env python3
"""Reverse a labeled cipher stack of the form X_THEN_Y (CTF forensics).

Given the stack string, key(s), and ciphertext, decrypt in REVERSE order
(the label describes the ENCRYPT order; we undo it last-to-first).

Supported primitives: ROT13, VIGENERE, BASE64, CAESAR, ATBASH, REVERSE.

Example:
  python3 reverse_cipher_stack.py \
    --stack ROT13_THEN_VIGENERE --key JIOKEY \
    --ct 'bgbd{jxo_ker_izp13_qjdvyamf_qvwaxpj_zypzszvap_2026}'

  -> synt{fzf_cqh_ebg13_ivtrarer_gryrpbz_vagreprcg_2026}
  -> flag{sms_pdu_rot13_vigenere_telecom_intercept_2026}
"""
import argparse
import base64
import codecs


def rot13(s):
    return codecs.encode(s, "rot_13")


def atbash(s):
    out = []
    for c in s:
        if "a" <= c <= "z":
            out.append(chr(219 - ord(c)))
        elif "A" <= c <= "Z":
            out.append(chr(155 - ord(c)))
        else:
            out.append(c)
    return "".join(out)


def reverse_str(s):
    return s[::-1]


def caesar_dec(s, shift):
    out = []
    for c in s:
        if c.isalpha():
            base = ord("A") if c.isupper() else ord("a")
            out.append(chr(base + (ord(c) - base - shift) % 26))
        else:
            out.append(c)
    return "".join(out)


def vigenere_dec(ct, key):
    out = []
    ki = 0
    k = key.upper()
    for ch in ct:
        if ch.isalpha():
            base = ord("A") if ch.isupper() else ord("a")
            c = ord(ch) - base
            kc = ord(k[ki % len(k)]) - ord("A")
            out.append(chr(base + (c - kc) % 26))
            ki += 1
        else:
            out.append(ch)
    return "".join(out)


# stages that consume a key (popped from the --key list, last stage first)
KEYED = {"VIGENERE", "CAESAR"}

DECRYPTORS = {
    "ROT13": lambda s, k: rot13(s),
    "VIGENERE": lambda s, k: vigenere_dec(s, k),
    "BASE64": lambda s, k: base64.b64decode(s).decode("latin-1", "replace"),
    "CAESAR": lambda s, k: caesar_dec(s, int(k) if k else 0),
    "ATBASH": lambda s, k: atbash(s),
    "REVERSE": lambda s, k: reverse_str(s),
}


def main():
    ap = argparse.ArgumentParser(description="Reverse a labeled X_THEN_Y cipher stack.")
    ap.add_argument("--stack", required=True, help="e.g. ROT13_THEN_VIGENERE")
    ap.add_argument(
        "--key",
        default="",
        help="key for VIGENERE/CAESAR stages (comma-split, applied last-stage-first)",
    )
    ap.add_argument("--ct", required=True, help="ciphertext")
    args = ap.parse_args()

    stages = [s.strip().upper() for s in args.stack.split("_THEN_")]
    unknown = [s for s in stages if s not in DECRYPTORS]
    if unknown:
        raise SystemExit(f"unknown stage(s) {unknown}; known: {sorted(DECRYPTORS)}")

    keys = [k.strip() for k in args.key.split(",")] if args.key else []
    data = args.ct

    # decrypt in REVERSE order
    for stage in reversed(stages):
        key = keys.pop() if (keys and stage in KEYED) else ""
        data = DECRYPTORS[stage](data, key)
        print(f"after {stage:9s}: {data}")

    print("FINAL:", data)


if __name__ == "__main__":
    main()
