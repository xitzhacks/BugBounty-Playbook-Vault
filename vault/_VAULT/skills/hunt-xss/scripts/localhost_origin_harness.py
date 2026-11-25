#!/usr/bin/env python3
"""Serve a PoC page at origin http://localhost WITHOUT binding port 80, plus a
beacon listener, so postMessage / CORS PoCs that compare exact origin strings can
actually be exercised.

Why: an origin guard written as `platforms.includes(event.origin)` compares the
verbatim string "http://localhost" (port 80 implied). Serving the PoC on :8080 gives
origin "http://localhost:8080" and is rejected — which reads like "the bug doesn't
reproduce". Without root you cannot bind :80, so force loopback through this proxy
instead.

Run:
    python3 localhost_origin_harness.py --root ./pocdir
    # then, in another shell:
    google-chrome --headless=new --no-sandbox --disable-gpu --disable-dev-shm-usage \
      --window-size=1200,900 --virtual-time-budget=25000 \
      --proxy-server=http://127.0.0.1:18888 \
      --proxy-bypass-list="<-loopback>" \
      --screenshot=/tmp/poc.png "http://localhost/"

    # interactive (watch the frame paint):
    google-chrome --proxy-server=http://127.0.0.1:18888 \
      --proxy-bypass-list="<-loopback>" "http://localhost/"

Beacon: in the PoC payload add
    body{background-image:url("http://127.0.0.1:19001/css-fired")}
A hit in <root>/callbacks.log proves the injected CSS/HTML went live. Loopback is a
"potentially trustworthy" origin, so an https page may fetch it without being blocked
as mixed content.

Gotchas baked in:
  * --proxy-pac-url does NOT override Chrome's implicit loopback bypass; only
    --proxy-server + --proxy-bypass-list="<-loopback>" does.
  * The proxy forwards absolute-URI requests to their REAL host and special-cases
    only `localhost`. A blanket rewrite breaks the iframe's own assets and the page
    looks broken for the wrong reason.
  * CONNECT tunnelling is implemented, otherwise an https iframe behind a global
    proxy never loads.

Before trusting any "it didn't fire" result, check the framed page's headers:
    curl -sk -D - -o /dev/null "https://target/" | grep -i frame-ancestors
If frame-ancestors only allows the target's own origin, the frame can never render
and there is no finding to demonstrate.
"""
import argparse
import http.server
import os
import select
import socket
import socketserver
import sys
import threading
import urllib.parse

HITS = []


def make_static(root):
    class Static(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **kw):
            super().__init__(*a, directory=root, **kw)

        def log_message(self, *a):
            pass

    return Static


class Proxy(http.server.BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    static_port = 18080

    def _forward(self):
        target = urllib.parse.urlsplit(self.path)
        host = target.hostname or "localhost"
        port = target.port or 80
        path = target.path or "/"
        if target.query:
            path += "?" + target.query

        connect_host, connect_port = host, port
        if host == "localhost":                      # only localhost maps to the PoC
            connect_host, connect_port = "127.0.0.1", self.static_port

        length = int(self.headers.get("Content-Length") or 0)
        body = self.rfile.read(length) if length else None

        try:
            conn = socket.create_connection((connect_host, connect_port), timeout=20)
        except Exception as exc:                     # noqa: BLE001
            self.send_error(502, f"upstream {host}:{port} failed: {exc}")
            return

        head = f"{self.command} {path} HTTP/1.1\r\nHost: {host}"
        if port not in (80, 443):
            head += f":{port}"
        head += "\r\n"
        for k, v in self.headers.items():
            if k.lower() in ("host", "proxy-connection", "connection"):
                continue
            head += f"{k}: {v}\r\n"
        head += "Connection: close\r\n\r\n"
        conn.sendall(head.encode() + (body or b""))

        data = b""
        while True:
            chunk = conn.recv(65536)
            if not chunk:
                break
            data += chunk
        conn.close()
        self.wfile.write(data)

    do_GET = do_POST = do_PUT = do_DELETE = _forward

    def do_CONNECT(self):
        host, _, port = self.path.partition(":")
        try:
            conn = socket.create_connection((host, int(port or 443)), timeout=20)
        except Exception:                            # noqa: BLE001
            self.send_error(502)
            return
        self.send_response(200, "Connection Established")
        self.end_headers()
        self.wfile.flush()
        socks = [self.connection, conn]
        try:
            while True:
                ready, _, _ = select.select(socks, [], [], 60)
                if not ready:
                    break
                for s in ready:
                    chunk = s.recv(65536)
                    if not chunk:
                        return
                    (conn if s is self.connection else self.connection).sendall(chunk)
        except Exception:                            # noqa: BLE001
            pass
        finally:
            conn.close()

    def log_message(self, *a):
        pass


def make_beacon(log_path):
    class Beacon(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            HITS.append(self.path)
            with open(log_path, "a") as fh:
                fh.write(self.path + "\n")
            sys.stdout.write(f"[beacon] {self.path}\n")
            sys.stdout.flush()
            self.send_response(200)
            self.send_header("Content-Type", "image/gif")
            self.send_header("Content-Length", "0")
            self.end_headers()

        def log_message(self, *a):
            pass

    return Beacon


def serve(handler, port):
    class Server(socketserver.ThreadingTCPServer):
        allow_reuse_address = True
        daemon_threads = True

    srv = Server(("127.0.0.1", port), handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".", help="directory containing index.html")
    ap.add_argument("--static-port", type=int, default=18080)
    ap.add_argument("--proxy-port", type=int, default=18888)
    ap.add_argument("--beacon-port", type=int, default=19001)
    args = ap.parse_args()

    root = os.path.abspath(args.root)
    if not os.path.exists(os.path.join(root, "index.html")):
        print(f"[!] no index.html in {root} — the browser will get a directory listing", file=sys.stderr)

    log_path = os.path.join(root, "callbacks.log")
    open(log_path, "w").close()
    Proxy.static_port = args.static_port

    serve(make_static(root), args.static_port)
    serve(Proxy, args.proxy_port)
    serve(make_beacon(log_path), args.beacon_port)

    print(f"static  :{args.static_port}  proxy :{args.proxy_port}  beacon :{args.beacon_port}")
    print(f"root    {root}")
    print(f"beacons {log_path}")
    print()
    print("open with:")
    print(f'  google-chrome --proxy-server=http://127.0.0.1:{args.proxy_port} \\')
    print('    --proxy-bypass-list="<-loopback>" "http://localhost/"')
    print()
    print("headless screenshot:")
    print(f'  google-chrome --headless=new --no-sandbox --disable-gpu --disable-dev-shm-usage \\')
    print('    --window-size=1200,900 --virtual-time-budget=25000 \\')
    print(f'    --proxy-server=http://127.0.0.1:{args.proxy_port} --proxy-bypass-list="<-loopback>" \\')
    print('    --screenshot=/tmp/poc.png "http://localhost/"')

    try:
        threading.Event().wait()
    except KeyboardInterrupt:
        print(f"\n[beacon] total hits: {len(HITS)}")


if __name__ == "__main__":
    main()
