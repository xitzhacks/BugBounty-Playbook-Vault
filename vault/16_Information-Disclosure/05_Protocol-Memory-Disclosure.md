---
title: "Protocol & Memory Disclosure — uninitialized reads, PASV trust, and stack contents"
type: playbook
category: protocol-memory-disclosure
cwe: "CWE-200"
source_count: 17
full_bodies_available: 17
corpus: "h1-brain disclosed_reports.db (sha256 8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4) — 362 rows"
list_accessed: "2026-11-07"
note: "Anchors: INFO-2107680 (basecamp, $8,868), INFO-2599391 (ibb, $2,600), INFO-63324 (ibb, $2,000), INFO-1176461 (curl, $1,000), INFO-302885 (security, $500). All quotes byte-true to references/archive/INFO-bodies-full-dump.txt."
---

# Protocol & Memory Disclosure — uninitialized reads, PASV trust, and stack contents

## 1. Overview

Seventeen rows, **$15,468/6 paid** (max $8,868) — the vault's smallest paid module per-row-count but its highest *per-finding* information density: this is the only module where the corpus pays for *memory the server never initialized*. No web form, no GraphQL field, no export feature: an outdated `librsvg`, an MTU, a TELNET suboption parser, a GIF coder. Eleven rows carry no figure, and they are all library CVEs (NGINX, Apache, libgd/libexif, Ruby, Python) — the module's dual nature is its lesson: the *mechanism* (uninitialized read) is identical whether the corpus prices it at $8,868 (a live Basecamp pixel leak) or $0 (a CVE ledger row). CVE coverage is the module's signature: 12 of 17 rows carry CVEs (CVE-2015-3044 through CVE-2024-3416), the most CVE-dense module in the vault.

**Case-stock (17 rows / $15,468):**

| Case | Target | Mechanism | Bounty |
|---|---|---|---|
| [INFO-2107680](https://hackerone.com/reports/2107680) | basecamp | AWS keys and user cookie leakage via uninitialized memory leak in outdated lib… | $8,868 |
| [INFO-2599391](https://hackerone.com/reports/2599391) | ibb | CVE-2024-3416: MTU of 4096 or greater without fragmentation may cause NGINX wo… | $2,600 |
| [INFO-63324](https://hackerone.com/reports/63324) | ibb | Flash Player information disclosure (etc.) CVE-2015-3044, PSIRT-3298 | $2,000 |
| [INFO-1176461](https://hackerone.com/reports/1176461) | curl | CVE-2021-22898: TELNET stack contents disclosure | $1,000 |
| [INFO-302885](https://hackerone.com/reports/302885) | security | ImageMagick GIF coder vulnerability leading to memory disclosure | $500 |
| [INFO-1145454](https://hackerone.com/reports/1145454) | ruby | lib/net/ftp.rb: trusting PASV responses allow client abuse | $500 |
| [INFO-142773](https://hackerone.com/reports/142773) | torproject | 16 instances where return value of OpenSSL i2d_RSAPublicKey is discarded -- mi… | - |
| [INFO-166661](https://hackerone.com/reports/166661) | ruby | Arbitrary heap overread in strscan on 32 bit Ruby, patch included | - |
| [INFO-174632](https://hackerone.com/reports/174632) | ibb | Information disclosure in mmap module - python 2.7.12 | - |
| [INFO-516237](https://hackerone.com/reports/516237) | ibb | Uninitialized read in exif_process_IFD_in_MAKERNOTE | - |
| [INFO-623588](https://hackerone.com/reports/623588) | ibb | Uninitialized read in gdImageCreateFromXbm | - |
| [INFO-838685](https://hackerone.com/reports/838685) | ibb | Use of uninitialized value in ftp_getrc_msg method of mod_proxy_ftp.c | - |
| [INFO-1040166](https://hackerone.com/reports/1040166) | curl | CVE-2020-8284: trusting FTP PASV responses | - |
| [INFO-1223882](https://hackerone.com/reports/1223882) | curl | CVE-2021-22925: TELNET stack contents disclosure again | - |
| [INFO-1595281](https://hackerone.com/reports/1595281) | ibb | Read beyond bounds in ap_strcmp_match() [zhbug_httpd_47.7] | - |
| [INFO-1595290](https://hackerone.com/reports/1595290) | ibb | Controllable read beyond bounds in lua_websocket_readbytes() [zhbug_httpd_126] | - |
| [INFO-1595299](https://hackerone.com/reports/1595299) | ibb | Read beyond bounds via ap_rwrite() [zhbug_httpd_47.2] | - |

## 2. The $8,868 pixel: SVG avatars leaking server memory

INFO-2107680 (**basecamp, $8,868**) is the module's crown and the vault's best single "memory disclosure" write-up. Basecamp converts SVG avatars with a stale librsvg in the *same unix process* as request handling, so an uninitialized block becomes image pixels:

> This version contains a vulnerability that allows leakage of the contents of an uninitialized memory block (that is, something is malloced, never initialized, and then used to build the preview image). Since it seems to be performed in the same unix process as the general request processing, it is possible for an attacker to steal sensitive data from this process, including basecamp configs (e.g., AWS keys) and requests of random users.

The proof loops a randomized avatar URL and greps the recovered pixels — yielding an RSA key fragment, `s3_backup` / `active_record_encryption` config, and *other users'* request headers (`COOKIE: █████`, `X_CSRF_TOKEN`, `REFERER`) — and then verifies liveness: `aws sts get-caller-identity` returning `arn:aws:iam::██████:user/bc3-storage`. The reporter's impact line states the class rule this vault will reuse in the playbook: "the attacker does not control which kind of information she will extract." Non-controllable, co-resident, credential-class — that combination is what $8,868 buys.

## 3. The CVE ledger: NGINX, curl, Flash, and the unpriced imprint

INFO-2599391 (**ibb, $2,600**, CVE-2024-3416) is eight lines: QUIC packets with MTU ≥ 4096 "can cause NGINX worker processes to leak previously freed memory" — paid because it is a *current, CVE-assigned, reproducible primitive*. INFO-1176461 (**curl, $1,000**, CVE-2021-22898) is the mechanism proof that would later apply to a whole family: `lib/telnet.c`'s `suboption()` checks `sscanf()`'s return as boolean instead of `== 2`, leaving gaps "that will contain whatever stack contents from previous operation of the application" — with the hex-dump receipt and the one-character fix (`== 2`). INFO-63324 (**ibb, $2,000**, CVE-2015-3044) is the Flash LSO primitive (cross-site Local Shared Object read/write, macromedia.com settings overwrite for camera/mic), and INFO-302885 (**security, $500**, CVE-2017-15277) the GIF-coder variant — a `gifoeb`-derived pixel recovery that disclosed "the linux version As well as Server path directory."

The eleven unpriced rows are the same shapes as *ledger entries*: NGINX `ap_rwrite()` / `ap_strcmp_match()` reads (INFO-1595299, INFO-1595281), Lua websocket bounded reads (INFO-1595290), `exif`/`gd` uninitialized reads (INFO-516237, INFO-623588), `mod_proxy_ftp` uninitialized use (INFO-838685), Ruby `strscan` heap over-read (INFO-166661), Python `mmap` disclosure (INFO-174632), OpenSSL return-value discards (INFO-142773), and the curl FTP-PASV/TELNET sequels (INFO-1040166, INFO-1223882 — "TELNET stack contents disclosure again"). The vault's doctrine, stated here so the playbook can enforce it: **a memory-disclosure CVE is a library fact; it becomes a bounty when the reporter shows it leaking *this program's* credentials** (INFO-2107680) or ships the working primitive with the fix (INFO-1176461). Ledger rows alone sit in the "no figure" set.

## 4. Protocol trust: PASV and the conned client

INFO-1145454 (**ruby, $500**, CVE-2021-31810 / CVE-2020-8284 / CVE-2007-1562) inverts the direction of every other row in the vault: the *client* is the victim. A malicious FTP server's PASV response "trick[s] `net/ftp` into connecting back to a given IP address and port, and this way potentially make it extract information about services that are otherwise private" — port scanning and banner grabbing through the client's own socket. INFO-1040166 (curl, $0, CVE-2020-8284) is the same trust bug lib-side. The pricing lesson: protocol-trust disclosures price at $500 when the *attacker must control the server*, because the primitive is real but the deployment precondition is heavy. The vault's P4 fingerprint will note that this class survives wherever a client library treats server-supplied addresses as authoritative.

## 5. The other unpriced mechanisms

Three rows extend the module beyond "uninitialized memory": INFO-174632 (Python `mmap` disclosure), INFO-166661 (32-bit Ruby `strscan` heap over-read with patch), INFO-142773 (16 discarded OpenSSL return values) — all unpriced, all *proactive-library* reports. They belong in the vault because they share the mechanism (a read the program never intended to answer) and because a hunter who finds them in a dependency *of a live target* converts them at the INFO-2107680 rate, not the ledger rate.

## 6. What pays, what doesn't

- **Pays at the top**: memory that leaks *live credentials of the same process* — AWS keys and session cookies recovered from pixels, verified with `aws sts` ($8,868). The verification output (`"Arn": "arn:aws:iam::…"`) is the price anchor; without it this is a crash-severity report.
- **Pays, CVE-grade**: current, precise, fix-included primitives (NGINX QUIC $2,600; telnet `== 2` $1,000; Flash LSO $2,000; GIF pixels $500). The fix hunk is part of the deliverable.
- **Doesn't pay (here)**: bare CVE pointers and library-audit rows (11 unpriced). Also note the direction asymmetry: client-trust rows (PASV) pay $500; server-memory rows pay 17× that when credentials materialize. Hunt the server side first.

## 7. Cross-references

- Module 04 (`04_File-Path-Errors-Secrets-Leaks.md`) — INFO-2107680's leaked `s3_backup` config and INFO-302885's GIF pixels are the memory face of the file/secret class; the AWS keys recovered in pixels are what module 04's token rows (INFO-2915647) leak in logs.
- Module 06 (`06_Adjacent-Disclosure-Noise.md`) — INFO-63324/73276 (Flash sandbox pair) straddle this module and the adjacent noise; the vault keeps the *mechanism* here and the *chain* there.
- Companion vault `../30_Memory-Corruption/` (upcoming) — the crash/over-read library corpus is the exploitation shelf; this module is the disclosure-pricing shelf for the same CVEs.
