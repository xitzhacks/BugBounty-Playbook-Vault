#!/usr/bin/env python3
"""
Reusable strict-validation crypto brute-forcer for CTF forensics.
Plug in: ct (ciphertext bytes), iv (bytes), and `ingredients` (dict of name->bytes)
that could seed a key (nonces, MACs, ids, iv itself).

It runs a wide key-space x cipher-matrix and ONLY prints decryptions that pass a
HARD validator (valid JSON by default). No printable-ratio / "starts with {"
false-positive leaking. Adapt the `validate()` fn for other expected shapes
(binary magic, flag prefix, etc).

Usage: edit the CONFIG block at the bottom, then: python3 crypto_bruteforce.py
"""
import json, hashlib, struct
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers.aead import AESCCM, AESGCM

def validate(b):
    """Return (score, info). score>0 means a real hit. Default: valid JSON."""
    if not b:
        return 0.0, "empty"
    try:
        obj = json.loads(b.decode("utf-8", "replace").strip())
        good = isinstance(obj, dict) and any(
            k in obj for k in ["manifest", "signature", "device", "version",
                               "firmware", "sign", "key", "hash", "flag", "model"])
        return (2.0 if good else 1.0), type(obj).__name__
    except Exception:
        return 0.0, None

def dec(k, mode, ivsrc, d):
    try:
        if mode in (modes.CBC, modes.CFB, modes.OFB):
            c = Cipher(algorithms.AES(k), mode(ivsrc), backend=default_backend())
        else:
            c = Cipher(algorithms.AES(k), mode(), backend=default_backend())
        x = c.decryptor(); return x.update(d) + x.finalize()
    except Exception:
        return None

def ctr_dec(k, ivsrc, d, cb=8):
    try:
        c = Cipher(algorithms.AES(k), modes.CTR(ivsrc[:cb].ljust(cb, b"\x00")),
                   backend=default_backend())
        x = c.decryptor(); return x.update(d) + x.finalize()
    except Exception:
        return None

def xor(b, key):
    ks = (key * (len(b) // len(key) + 1))[:len(b)]
    return bytes(a ^ b for a, b in zip(b, ks))

def build_keys(ing):
    K = {}
    for n, v in ing.items():
        for alg in ("sha256", "md5", "sha1"):
            fn = {"sha256": hashlib.sha256, "md5": hashlib.md5, "sha1": hashlib.sha1}[alg]
            K[f"{alg}({n})"] = fn(v).digest()
        K[f"raw({n})"] = v
    names = list(ing.keys())
    for i in range(len(names)):
        for j in range(len(names)):
            if i == j:
                continue
            a, b = names[i], names[j]
            blob = ing[a] + ing[b]
            for alg in ("sha256", "md5"):
                K[f"{alg}({a}+{b})"] = {"sha256": hashlib.sha256, "md5": hashlib.md5}[alg](blob).digest()
    return K

def run(ct, iv, ingredients, extra_ivs=None):
    K = build_keys(ingredients)
    hits = []
    ivsrcs = {"given": iv, "zero": b"\x00" * 16}
    if extra_ivs:
        ivsrcs.update(extra_ivs)
    for kn, kv in K.items():
        if not kv or len(kv) < 16:
            continue
        for L in (16, 24, 32):
            if len(kv) < L:
                continue
            k = kv[:L]
            for ivn, ivs in ivsrcs.items():
                ivs16 = (ivs * (16 // len(ivs) + 1))[:16] if len(ivs) < 16 else ivs[:16]
                for mname, m in (("CBC", modes.CBC), ("CFB", modes.CFB), ("OFB", modes.OFB)):
                    o = dec(k, m, ivs16, ct)
                    if o:
                        s, info = validate(o)
                        if s > 0:
                            hits.append((s, kn, L, f"AES{L}-{mname}/{ivn}", info, o))
                o = ctr_dec(k, iv, ct, 8)
                if o:
                    s, info = validate(o)
                    if s > 0:
                        hits.append((s, kn, L, f"AES{L}-CTR8", info, o))
                o = dec(k, lambda: modes.ECB(), iv, ct)
                if o:
                    s, info = validate(o)
                    if s > 0:
                        hits.append((s, kn, L, f"AES{L}-ECB", info, o))
            for nlen in (7, 8, 11, 12, 13):
                for tlen in (4, 8, 16):
                    if len(ct) <= tlen:
                        continue
                    try:
                        pt = AESCCM(k, tag_length=tlen).decrypt(iv[:nlen], ct[:-tlen] + ct[-tlen:], None)
                        s, info = validate(pt)
                        if s > 0:
                            hits.append((s, kn, L, f"CCM-n{nlen}-t{tlen}", info, pt))
                    except Exception:
                        pass
            try:
                pt = AESGCM(k).decrypt(iv[:12], ct, None)
                s, info = validate(pt)
                if s > 0:
                    hits.append((s, kn, L, "GCM", info, pt))
            except Exception:
                pass
        o = xor(ct, kv)
        s, info = validate(o)
        if s > 0:
            hits.append((s, kn, len(kv), "XOR-kv", info, o))
    hits.sort(key=lambda h: h[0], reverse=True)
    return hits

# ---------------- CONFIG (edit per challenge) ----------------
if __name__ == "__main__":
    ct = bytes.fromhex("a9b1743472d8a2ff486879331a1eeabc5c8b7c5903d66f147092daa66d58b300f3"
                       "45b4c0c05178f32fd34049c0d02aa21aa92d9302da17fe598fa4a46a24164a0e316"
                       "b07d708804edbcc22072ee815fcc601caf2015dfbc96ad5b1a536f3f719365915cbe"
                       "bd88c61bc8b60cbb90d21fa")
    iv = bytes.fromhex("ef42fe0a3322aee5043a2ca3b1a6fc80")
    ni, an = 1755000314, 3443427423
    DST = bytes.fromhex("D521A8290016")
    HUB = bytes.fromhex("85F52AF4A111")
    ingredients = {
        "ni": ni.to_bytes(4, "big"),
        "an": an.to_bytes(4, "big"),
        "dst": DST,
        "hub": HUB,
        "iv": iv,
    }
    results = run(ct, iv, ingredients)
    print(f"[*] valid decryptions (score>0): {len(results)}")
    for s, kn, L, mode, info, o in results[:10]:
        print(f"\n[score={s}] key={kn} {L}b {mode} ({info})")
        print("   ", o[:120])
    if not results:
        print("  NONE. No scheme in this key-space validated. Obtain the scheme/spec before guessing more.")
