#!/usr/bin/env python3
"""
Reusable raw-socket prober for custom line-protocol CTF "legacy network service" challenges.
Usage: python3 probe_service.py HOST PORT
Classifies verbs (400 vs 401/403 vs 200 vs empty), sweeps paths, and tests framing anomalies.

Key design choices (learned the hard way):
- Reads raw into a buffer with a fixed timeout, NO size cap and NO newline-break,
  so exploit output that arrives without a trailing \\n is not truncated.
- Re-tests 'b\'\'' (empty) results to separate real parser-state shifts from server flakiness.
- Uses one connection per probe (state-reset) to avoid cross-request contamination on flaky boxes.
"""
import socket, time, sys

HOST = sys.argv[1] if len(sys.argv) > 1 else "2.29.10.21"
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 5001

def conn():
    s = socket.socket(); s.settimeout(6)
    s.connect((HOST, PORT)); s.recv(4096); return s   # read banner

def send_get_reply(s, line, read_wait=6.0):
    s.sendall((line + "\r\n").encode()); time.sleep(0.5)
    s.settimeout(read_wait)
    r = b""
    try:
        while True:
            d = s.recv(8192)
            if not d: break
            r += d
    except socket.timeout:
        pass
    return r

def probe(line, read_wait=4.0):
    """Open fresh connection, send one line, return raw reply (consistent across runs)."""
    try:
        s = conn(); r = send_get_reply(s, line, read_wait); s.close(); return r
    except Exception as e:
        return b"ERR " + str(e).encode()

def classify(r):
    if r.startswith(b"400"): return "BAD_VERB"
    if r.startswith(b"401") or r.startswith(b"403"): return "VALID_GATED"
    if r.startswith(b"200"): return "OK"
    if r == b"": return "EMPTY(ambiguous)"
    return "OTHER"

VERBS = ["GET","POST","AUTH","HELP","VERSION","STATUS","INFO","LIST","SHOW",
         "SESSION","SESSIONS","LOG","LOGS","FLAG","ADMIN","USER","PASS","DEBUG",
         "RUN","EXEC","PING","ECHO","QUIT","BYE"]
PATHS = ["/flag","/flags","/secret","/secrets","/sessions","/session","/data",
         "/admin","/logs","/log","/audit","/activity","/records","/trace","/",
         "/flag/","/secret/"]
FRAME = [' GET /flag', ' GET /sessions', ' GET /secret', ' GET /data',  # leading space
         'GET /flag/', 'GET /flag ', 'GET /flag?auth=admin',
         'AUTH', 'AUTH ', ' GET /flag HTTP/1.1']

print(f"=== banner ===")
try:
    s = socket.socket(); s.settimeout(6); s.connect((HOST, PORT))
    print(s.recv(4096)); s.close()
except Exception as e:
    print("connect err", e)

print("\n=== verb sweep ===")
for v in VERBS:
    r = probe(v, 2.5)
    print(f"  {v:10} {classify(r):14} {r[:80]!r}")

print("\n=== path sweep (GET) ===")
for p in PATHS:
    r = probe("GET " + p, 2.5)
    print(f"  GET {p:12} {classify(r):14} {r[:80]!r}")

print("\n=== framing anomalies (re-tested x2) ===")
for f in FRAME:
    hits = set()
    for _ in range(2):
        r = probe(f, 5.0)
        hits.add(classify(r))
    stable = len(hits) == 1
    print(f"  {f!r:24} classes={hits} {'STABLE' if stable else 'FLAKY'}")
print("done")
