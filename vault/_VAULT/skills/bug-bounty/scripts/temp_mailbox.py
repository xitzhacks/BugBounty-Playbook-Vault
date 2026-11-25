#!/usr/bin/env python3
"""Throwaway mailbox via the mail.tm API — no key, no signup.

Use to TEST a target's disposable-email filter, or to receive a verification
link when a target does not block the domain. Most bounty targets DO block
mail.tm domains; read references/test-account-provisioning.md before assuming
this will carry a registration.

Usage:
  python3 temp_mailbox.py new [label]                 # create mailbox, print creds
  python3 temp_mailbox.py inbox <address> <password>  # list messages
  python3 temp_mailbox.py read <address> <password> <message_id>
  python3 temp_mailbox.py wait <address> <password> [seconds]   # poll for new mail

Credentials are cached in ./tempboxes.json.
"""
import json, os, secrets, string, sys, time
import urllib.error
import urllib.request

API = "https://api.mail.tm"
STORE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tempboxes.json")


def _req(path, data=None, token=None, method=None):
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    if token:
        headers["Authorization"] = "Bearer " + token
    body = json.dumps(data).encode() if data is not None else None
    req = urllib.request.Request(
        API + path, data=body, headers=headers,
        method=method or ("POST" if data is not None else "GET"))
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            raw = r.read().decode()
            return r.status, (json.loads(raw) if raw.strip() else {})
    except urllib.error.HTTPError as e:
        raw = e.read().decode()
        try:
            return e.code, json.loads(raw)
        except Exception:
            return e.code, {"raw": raw}


def _members(d):
    """mail.tm returns either a bare list or a hydra collection."""
    return d if isinstance(d, list) else d.get("hydra:member", [])


def new(label="x"):
    st, d = _req("/domains?page=1")
    domains = _members(d)
    if not domains:
        sys.exit(f"no domains available: {st} {d}")
    domain = domains[0]["domain"]
    local = "bb" + label + "".join(secrets.choice(string.ascii_lowercase + string.digits)
                                  for _ in range(8))
    address = f"{local}@{domain}"
    password = "".join(secrets.choice(string.ascii_letters + string.digits) for _ in range(18))
    st, acct = _req("/accounts", {"address": address, "password": password})
    if st not in (200, 201):
        sys.exit(f"account creation failed: {st} {acct}")
    st, tok = _req("/token", {"address": address, "password": password})
    rec = {"label": label, "address": address, "password": password,
           "token": tok.get("token")}
    boxes = json.load(open(STORE)) if os.path.exists(STORE) else []
    boxes.append(rec)
    json.dump(boxes, open(STORE, "w"), indent=2)
    print(json.dumps(rec, indent=2))
    print("\nNOTE: this domain is almost certainly on the target's disposable blocklist.")
    return rec


def _login(address, password):
    st, tok = _req("/token", {"address": address, "password": password})
    if "token" not in tok:
        sys.exit(f"login failed: {st} {tok}")
    return tok["token"]


def inbox(address, password):
    token = _login(address, password)
    st, d = _req("/messages?page=1", token=token)
    msgs = _members(d)
    for m in msgs:
        print(f"{m['id']}  {m.get('from', {}).get('address')}  "
              f"{m.get('subject')}  {m.get('createdAt')}")
    if not msgs:
        print("(empty)")
    return msgs


def read(address, password, mid):
    token = _login(address, password)
    st, m = _req(f"/messages/{mid}", token=token)
    print("SUBJECT:", m.get("subject"))
    print("FROM:", m.get("from"))
    for part in m.get("text") or []:
        print("---TEXT---"); print(part)
    for part in m.get("html") or []:
        print("---HTML (first 3000)---"); print(part[:3000])


def wait(address, password, seconds=120):
    seen = set()
    deadline = time.time() + int(seconds)
    while time.time() < deadline:
        for m in inbox(address, password):
            if m["id"] not in seen:
                seen.add(m["id"])
                read(address, password, m["id"])
                return m
        time.sleep(5)
    print("(timed out, no mail)")


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        print(__doc__); sys.exit(1)
    {"new": lambda: new(a[1] if len(a) > 1 else "x"),
     "inbox": lambda: inbox(a[1], a[2]),
     "read": lambda: read(a[1], a[2], a[3]),
     "wait": lambda: wait(a[1], a[2], a[3] if len(a) > 3 else 120)}[a[0]]()
