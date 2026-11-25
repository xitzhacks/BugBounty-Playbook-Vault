#!/usr/bin/env python3
"""
Solve a "combined LFSR XOR keystream" challenge.
Inputs (in directory given as argv[1], default cwd):
  cipher_spec.json : {deg_a, taps_a, deg_b, taps_b, combiner:"XOR", known_header}
  export.bin       : ciphertext = (known_header + flag) XOR keystream, keystream = LFSR_A XOR LFSR_B
Outputs the recovered plaintext (header + flag).
"""
import json, sys, os

def main():
    d = sys.argv[1] if len(sys.argv) > 1 else "."
    SPEC = json.load(open(os.path.join(d, "cipher_spec.json")))
    ct = open(os.path.join(d, "export.bin"), "rb").read()
    header = SPEC["known_header"].encode()
    deg_a = SPEC["deg_a"]; taps_a = SPEC["taps_a"]
    deg_b = SPEC["deg_b"]; taps_b = SPEC["taps_b"]

    def bfb(data, msb):
        out = []
        for byte in data:
            for i in range(8):
                out.append((byte >> (7 - i)) & 1 if msb else (byte >> i) & 1)
        return out

    def make_step(n, taps, out_msb, shift_left):
        mask = (1 << n) - 1; tm = 0
        for t in taps: tm |= (1 << t)
        def step(s):
            ob = (s >> (n - 1)) & 1 if out_msb else s & 1
            fb = (s & tm).bit_count() & 1
            ns = ((s << 1) | fb) & mask if shift_left else (s >> 1) | (fb << (n - 1))
            return ob, ns
        return step

    def seed_from(O, n, out_msb, sl):
        if (not out_msb) and (not sl):
            return sum(O[k] << k for k in range(n))
        if out_msb and sl:
            return sum(O[n - 1 - k] << k for k in range(n))
        return None

    def gen(step, seed, nb):
        s = seed; o = []
        for _ in range(nb):
            b, s = step(s); o.append(b)
        return o

    def to_bytes(bits, byte_msb):
        out = bytearray()
        for i in range(0, len(bits) - 7, 8):
            byte = 0
            for j in range(8):
                if byte_msb: byte = (byte << 1) | bits[i + j]
                else:         byte |= bits[i + j] << (7 - j)
            out.append(byte)
        return bytes(out)

    # Seed recovery model: Fibonacci, MSB-out, shift-left
    out_msb, sl = True, True
    sA = make_step(deg_a, taps_a, out_msb, sl)
    sB = make_step(deg_b, taps_b, out_msb, sl)
    M = len(header) * 8
    ctb = bfb(ct, True); hab = bfb(header, True)
    ks0 = [ctb[i] ^ hab[i] for i in range(M)]
    aseed = bseed = None
    for a in range(1 << deg_a):
        A = gen(sA, a, M)
        B = [ks0[i] ^ A[i] for i in range(M)]
        b = seed_from(B[:deg_b], deg_b, out_msb, sl)
        if b is None: continue
        if gen(sB, b, M) == B:
            aseed, bseed = a, b; break
    assert aseed is not None, "no consistent seed pair found"
    print(f"LFSR_A seed=0x{aseed:04x}  LFSR_B seed=0x{bseed:05x}")

    Nbits = len(ct) * 8
    A = gen(sA, aseed, Nbits); B = gen(sB, bseed, Nbits)
    ks = [A[i] ^ B[i] for i in range(Nbits)]

    # Try all packings to find the one matching the header
    for byte_msb in (True, False):
        dec = to_bytes(ks, byte_msb)
        pt = bytes(c ^ d for c, d in zip(ct, dec))
        if pt[:len(header)] == header:
            print("PLAINTEXT:", pt.decode('latin-1'))
            return
    # fallback: vary ct bit order too
    for ctb_msb in (True, False):
        ctb2 = bfb(ct, ctb_msb)
        for byte_msb in (True, False):
            ptbits = [ctb2[i] ^ ks[i] for i in range(Nbits)]
            pt = to_bytes(ptbits, byte_msb)
            if pt[:len(header)] == header:
                print("PLAINTEXT:", pt.decode('latin-1'))
                return
    print("header not matched; inspect keystream/seed model")

if __name__ == "__main__":
    main()
