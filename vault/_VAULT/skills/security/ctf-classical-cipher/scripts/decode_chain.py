#!/usr/bin/env python3
"""Reusable decoders for classical/modern CTF cipher chains.

Each function is self-contained; call from execute_code or a script.
Only standard library used.
"""
import re, json, itertools, string


def atbash(s: str) -> str:
    o = []
    for c in s:
        if 'a' <= c <= 'z':
            o.append(chr(219 - ord(c)))
        elif 'A' <= c <= 'Z':
            o.append(chr(155 - ord(c)))
        else:
            o.append(c)
    return ''.join(o)


def caesar(s: str, k: int) -> str:
    out = []
    for c in s:
        if 'a' <= c <= 'z':
            out.append(chr((ord(c) - 97 + k) % 26 + 97))
        elif 'A' <= c <= 'Z':
            out.append(chr((ord(c) - 65 + k) % 26 + 65))
        else:
            out.append(c)
    return ''.join(out)


def codepoints(s: str):
    return [hex(ord(c)) for c in s]


def cjk_shift_brute(s: str, lo=0, hi=0x110000):
    """Brute a uniform codepoint offset K so decode is printable ASCII.
    Returns list of (score, K, decoded) sorted by score desc."""
    cps = [ord(c) for c in s]
    best = []
    for K in range(0x4000, 0xA000):  # tune range per challenge
        dec = ''.join(chr(o - K) if 0 <= o - K < 0x110000 else '\ufffd' for o in cps)
        ps = sum(1 for ch in dec if 32 <= ord(ch) < 127)
        ls = sum(1 for ch in dec if ch.isalpha())
        best.append((ps * 2 + ls, K, dec))
    best.sort(reverse=True)
    return best[:5]


def emoji_mod26(s: str, base: int = 0x1F300) -> str:
    return ''.join(chr((ord(c) - base) % 26 + 97) for c in s)


def emoji_mod26_scan(s: str, lo=0x1F000, hi=0x1F700):
    """Try emoji->letter bases; print ones starting with a readable word."""
    for b in range(lo, hi):
        out = emoji_mod26(s, b)
        if out.startswith(('flag', 'the', 'key', 'dec', 'cha', 'lin')):
            print(f"  base {hex(b)}: {out}")


def vigenere_dec(s: str, key: str) -> str:
    out = []
    ki = 0
    for c in s:
        k = ord(key[ki % len(key)]) - 65
        if 'a' <= c <= 'z':
            out.append(chr((ord(c) - 97 - k) % 26 + 97)); ki += 1
        elif 'A' <= c <= 'Z':
            out.append(chr((ord(c) - 65 - k) % 26 + 65)); ki += 1
        else:
            out.append(c)
    return ''.join(out)


def extract_forms(html: str):
    """From a Google Forms page, pull every 'Decode it' string (header + ciphertext)."""
    m = re.search(r'FB_PUBLIC_LOAD_DATA_\s*=\s*(\[.*?\]);', html, re.S)
    if not m:
        return []
    j = json.loads(m.group(1))
    parts = []

    def walk(o):
        if isinstance(o, str):
            if o.startswith('Decode it'):
                parts.append(o)
        elif isinstance(o, list):
            for x in o:
                walk(x)
        elif isinstance(o, dict):
            for v in o.values():
                walk(v)
    walk(j)
    return parts


def null_cipher_strip(s: str, fillers=None):
    """Atbash, then remove constant filler runs to expose hidden letters."""
    a = atbash(s)
    if fillers is None:
        fillers = ['abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
                   '`_^]\\[', '@?>=<;:9876543210/.-,+*)',
                   'ZYXWVUTSRQPONMLKJIHGFEDCBA', 'zyxwvutsrqponmlkjihgfedcba']
    for f in fillers:
        a = a.replace(f, '')
    return ''.join(ch for ch in a if ch.isalpha())


if __name__ == '__main__':
    # quick self-test
    print(atbash('sggkh://ulinh.tov/zFUwWCQgOzmkCuD67'))
    print(caesar('GMBH|N3yQ:wL5sU8{O2rM9dE6xG4~', -1))
