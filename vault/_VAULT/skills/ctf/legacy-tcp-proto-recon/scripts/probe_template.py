#!/usr/bin/env python3
"""
Clean recon probe for a raw line-protocol TCP service.
Encodes the pitfalls from the 5001 engagement:
  - banner drained into its OWN variable (never pollutes command responses)
  - one fresh socket per command, with retries
  - b'' tracked with connection state (OPEN=continuation, CLOSED=likely flake)
  - any non-403/non-400 hit auto-verified with a same-connection GET /flag
Usage: set HOST/PORT, edit COMMANDS / AUTH_PAIRS, run.
"""
import socket, time

HOST, PORT = "2.29.10.21", 5001
RETRY = 3

def banner_and_recv(sock, wait=4.0):
    """Drain banner first (separate!), then read command response."""
    sock.settimeout(2.0)
    banner = b""
    try:
        while True:
            d = sock.recv(8192)
            if not d:
                break
            banner += d
    except socket.timeout:
        pass
    return banner

def cmd_once(line, wait=4.0):
    """Fresh socket per command. Returns (banner, response, closed)."""
    for _ in range(RETRY):
        try:
            s = socket.socket()
            s.settimeout(6)
            s.connect((HOST, PORT))
            banner = banner_and_recv(s)          # SEPARATE var — the fix
            s.sendall((line + "\r\n").encode())
            time.sleep(0.4)
            s.settimeout(wait)
            r = b""; closed = False
            try:
                while True:
                    d = s.recv(8192)
                    if not d:
                        closed = True
                        break
                    r += d
            except socket.timeout:
                pass
            s.close()
            return banner, r, closed
        except Exception as e:
            last = str(e)
            time.sleep(0.3)
    return b"", b"ERR " + last.encode(), True

def verify_auth(line):
    """If AUTH returns non-403/non-400, prove it by GET on same socket."""
    s = socket.socket(); s.settimeout(6); s.connect((HOST, PORT)); banner_and_recv(s)
    s.sendall((line + "\r\n").encode()); time.sleep(0.4)
    s.settimeout(4); r=b""; 
    try:
        while True:
            d=s.recv(8192)
            if not d: break
            r+=d
    except socket.timeout: pass
    if b"403" not in r and b"400" not in r and r:
        s.sendall(b"GET /flag\r\n"); time.sleep(0.5)
        g=b""
        try:
            while True:
                d=s.recv(8192)
                if not d: break
                g+=d
        except socket.timeout: pass
        print(f"   AUTH hit! GET /flag -> {g[:300]!r}")
    s.close()

if __name__ == "__main__":
    COMMANDS = ["GET /flag", "GET /sessions", "AUTH admin admin", "DUMP", "LIST"]
    print("===== verb / command probe =====")
    for c in COMMANDS:
        b, r, closed = cmd_once(c)
        state = "OPEN" if not closed else "CLOSED"
        mark = "***" if (b"400" not in r and b"403" not in r and r) else "   "
        print(f"{mark} {c:18} [{state}] -> {r[:200]!r}")
        if mark.strip():
            verify_auth(c) if c.startswith("AUTH") else None
    print("done")
