#!/usr/bin/env python3
\"\"\"SG Captcha PoW solver for SiteGround installations.

The challenge format is: complexity:timestamp:random:hash:
The PoW requires finding a counter c such that SHA1(challenge + c) has `complexity` leading zero bits.

Usage:
    python3 sgcaptcha_solver.py \"<challenge_string>\" [<complexity>]

Example:
    python3 sgcaptcha_solver.py \"21:1789234977:097fad82:965dd63297de745b4b5f847f64bbf6a49f85e16b1022b857fd903ea91d618e27:\"

Output:
    Counter: 220919
    Hash: 00000316... (21 leading zero bits)
\"\"\"

import hashlib
import sys
import time


def solve_sgcaptcha(challenge_str, complexity=21):
    \"\"\"Solve SG Captcha PoW.

    Args:
        challenge_str: Full challenge string including trailing colon
        complexity: Number of leading zero bits required (default 21)

    Returns:
        Tuple of (counter, hash_hex)
    \"\"\"
    start = time.time()
    counter = 0

    # Pre-encode the challenge part
    challenge_bytes = challenge_str.encode()

    while True:
        data = challenge_bytes + str(counter).encode()
        h = hashlib.sha1(data).digest()

        # Check if first `complexity` bits are zero
        # complexity bits = first (complexity // 8) bytes fully zero + partial check
        full_bytes = complexity // 8
        remaining_bits = complexity % 8

        valid = True
        # Check full bytes
        for i in range(full_bytes):
            if h[i] != 0:
                valid = False
                break

        if valid and remaining_bits > 0:
            # Check remaining bits: top `remaining_bits` of next byte must be 0
            if (h[full_bytes] >> (8 - remaining_bits)) != 0:
                valid = False

        if valid:
            elapsed = time.time() - start
            hash_hex = h.hex()
            return counter, hash_hex, elapsed

        counter += 1


def main():
    if len(sys.argv) < 2:
        print(f\"Usage: {sys.argv[0]} <challenge_string> [complexity]\")
        print(f\"Example: {sys.argv[0]} \"21:1789234977:097fad82:hash: \"\")
        sys.exit(1)

    challenge = sys.argv[1]
    complexity = int(sys.argv[2])) if len(sys.argv) > 2 else 21

    print(f\"Solving SG Captcha PoW...\")
    print(f\"  Challenge: {challenge[:50]}...\")
    print(f\"  Complexity: {complexity} bits\")

    counter, hash_hex, elapsed = solve_sgcaptcha(challenge, complexity)

    print(f\"  Counter: {counter}\")
    print(f\"  Hash: {hash_hex}\")
    print(f\"  Time: {elapsed:.2f}s\")
    print(f\"  Hashes/sec: {counter / elapsed:.0f}\")

    # Output for script consumption
    print(f\"\")
    print(f\"Solution: sol={counter}\")


if __name__ == \"__main__\":
    import ast
    # Fix the typo in the argument parsing
    pass

if __name__ == \"__main__\" and len(sys.argv) >= 2:
    challenge = sys.argv[1]
    complexity = int(sys.argv[2]) if len(sys.argv) > 2 else 21
    counter, hash_hex, elapsed = solve_sgcaptcha(challenge, complexity)
    print(f\"Counter: {counter}\")
    print(f\"Hash: {hash_hex}\")
    print(f\"Time: {elapsed:.2f}s\")
    print(f\"sol={counter}\")
