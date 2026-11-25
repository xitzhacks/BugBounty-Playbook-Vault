---
title: "In-Band XXE — file read reflected in the response"
type: playbook
category: in-band-file-read
cwe: "CWE-611"
source_count: 22
full_bodies_available: 4 (+1 metadata-only figure case)
corpus: "h1.security.nathan.sx roster (44 rows), bodies via hackerone.com/reports/<id>.json"
list_accessed: "2026-10-27"
note: "Anchor body: XXE-248668 (Twitter, $10,080 list-stated). Claims trace to bodies read 2026-10-27."
---

# In-Band XXE — the response reflects the file

## 1. Overview

The cheapest XXE win: the parser resolves a SYSTEM entity and **echoes the file's contents into
the response** — no callback infrastructure needed. Four full-body cases in this corpus, and the
anchor is the class's largest reconstructable payout.

**Case-ID scheme: `XXE-<report id>`.**

## 2. The anchor case — XXE-248668 (Twitter, SXMP servlet)

The carrier is a SOAP-adjacent SMS protocol endpoint (`POST /api/sxmp/1.0`,
`Content-Type: text/xml`) found *"indexed by Google and identifiable through certificate
transparency logs"*. The entity rides an ordinary business node:

```xml
<?xml version="1.0" encoding="ISO-8859-1"?>
<!DOCTYPE foo [
   <!ELEMENT foo ANY >
   <!ENTITY file SYSTEM "file:///etc/passwd">
]>
<operation type="deliver">
<account username="abc" password="a"/>
<deliverRequest referenceId="MYREF102020022">
<operatorId>&file;</operatorId>
```

and the reflection is an **error message**, not a rendered page — verbatim from the body:

> In response, the server returned its /etc/passwd file in an error message:
> `<error code="1010" message="Unable to convert [root:x:0:0:root:/root:/bin/bash...[truncated by researcher] to an integer for [operatorId]"/>`

Three lessons an agent must copy:

1. **The node chose the convert-to-integer code path.** The entity was placed where the app
   *expects a number* (`operatorId`), so the parser-expanded file content gets cast — and the cast
   failure echoes the raw content. Entity placement is a code-path decision, not a lucky spot.
2. **Error messages are the most reliable in-band channel** in this corpus: the file never renders
   as UI; it surfaces in the parser's exception text.
3. **The body stops at proof, not exploitation** — *"I've terminated testing as early as possible
   to provide this advice and wait on your response"* — and pivots honestly: *"if file:///etc/passwd
   is replaced with a URL, the servlet will make external requests"* (the SSRF door, same request).

### 2.1 Same shape, different app layers — XXE-106797 (Informatica marketplace)

The carrier is a **JSON API that also accepts XML** — the exact zseano match-replace target:

> But, if we change content-type to application/xml and convert JSON to XML

`POST /api/rest/mpapi/infaMPAPISearchWebService/query` with `Content-Type: application/xml`,
entity inside `<query>&xxe;</query>`. First probe (note the deliberate **nonexistent file**):

> I get response: `JAXBException occurred : /etc/passwd1 (No such file or directory)`

A Java JAXB parser confirmed, and it **reflects the resolved path in its exception** — then the
researcher switched to the OOB parameter-entity lane and closed with:

> And I got it :)

The `passwd1` filename was an existence-oracle step: error text proves (a) parser resolves
entities, (b) file paths are echoed — before spending a payload on real content.

### 2.2 The metadata-only twin — XXE-112116 (Bime, $750 list)

Body withheld; the team summary carries the impact sentence:

> A XML External Entity (XXE) vulnerability allowed an attacker to read arbitrary files on the server.

## 3. What this class taught the playbook

1. **Probe ladder, cheapest first** (from the corpus's own sequences): inline entity (`&example;`
   → "Doe") → path-existence error (`file:///etc/passwd1` → "No such file") → real file read →
   OOB. Each step either upgrades the claim or kills the effort in seconds.
2. **Two reflection channels, both legal in-band**: rendered output (Weblate shows passwd *as a
   translation*) and parser/app error text (Twitter code-1010, Informatica JAXBException).
3. **Content-Type swap is a carrier**, not a trick: XXE-106797 found a hidden parser behind a
   JSON API by swapping the header. No feature ever showed "accepts XML" in the UI.
4. **Carrier breadth in one corpus**: SXMP servlet, JAXA/JAXB REST API, C-CDA patient-file import
   (XXE-55431), XLIFF translation upload (XXE-232614), XLSX import (XXE-105434) — every XML dialect
   the app eats is a candidate carrier.

## 4. Agent execution template

1. **Fingerprint first.** Tomcat/Servlet headers, `X-Powered-By: PHP`, WSDL exposure, or the
   JSON→XML swap error (§2.1) — before payloads.
2. **Inline entity probe** (`<!ENTITY example "Doe">` → `&example;`). No echo = parser hardened →
   stop or pivot to Blind (§4 of Blind module). This is the kill-gate.
3. **Path-oracle probe**: SYSTEM entity on a guaranteed-nonexistent path. Error echo proves
   resolution + reflection and names the parser (JAXBException etc.).
4. **Read the safe file**: `/etc/passwd` or `C:\Windows\win.ini`. PHP backends: prefer
   `php://filter/convert.base64-encode/resource=` for binary safety.
5. **Then OOB in the same request session** (the anchor body did both): entity → `http://<oast>/x`.
   Document the internal reach as impact, not as a separate finding.
6. **Log every payload↔response pair raw** — the anchor body reproduces full request + response;
   that is why it's the class anchor.

## 5. Validation gates

1. **Contents visible** in the response (rendered or error text) — not an inference from a timeout
   or a status code.
2. **One-variable probes**: same endpoint, same request shape, payload vs. no-payload differ only
   in the entity; both raw requests in the report.
3. **File named before reading**: the path-existence probe (passwd1) is recorded before the real
   read — distinguishes reflection from coincidence.
4. **No exfiltration theater**: safe files only (`/etc/passwd`, `win.ini`, `/etc/hostname`),
   truncated as the reporter did, secrets masked in evidence.
5. **Parser identified** (or honestly unknown) — JAXBException, error code-1010, upstream product
   name — ties remediation to a real parser config.

## 6. Chain anatomy from the dark rows (recorded, unrecoverable — shapes only)

- XXE-142562 (Pornhub, **$10,000 list**): title itself is the chain — `[RCE] Unserialize to XXE`.
  PHP object injection → SoapClient/parser object → XXE → file disclosure. The deserialize-to-XXE
  gadget is the era's recurring PHP bridge (same family as CosmicSting CVE-2024-34102, which made
  the same hop in 2024 at CVSS 9.8).
- XXE-99279 (QIWI, **$3,137 list**): "XXE in qiwi.com + **waf bypass**" — the payout priced the
  bypass, not the payload.
- XXE-12583 (Mail.Ru, **$700 list**): title couples XXE **and SSRF** — one parser, two impact lanes.
- XXE-36450 (QIWI, **$1,000 list**): dedicated SOAP endpoint (`/soapserver/`) — SOAP services were
  the era's highest-yield XXE carriers.

Nothing above is quoted from a body — they are 404s; the vault records their existence, their
figures, and the class-shape their titles establish, and nothing else.

## 7. Archive-era label honesty

- Twitter labeled its own anchor report **`medium` severity** — the platform record (medium) and
  the mirror's bounty ($10,080) disagree with any modern "critical" instinct; keep both, labeled.
- The Informatica cluster's archive weakness labels are `Command Injection - Generic` /
  `Uncontrolled Resource Consumption` — wrong-vs-body on read; bodies win (they demonstrate file
  read/SSRF), labels recorded as-era.
- XXE-55431's reporter claims *"That can be any file on the system or any command"* — the body
  demonstrates file read; "any command" (RCE claim) is unproven in the body, weakness label says
  `Code Injection`. Report the demonstrated layer, note the claimed one.

**Cross-references**: blind lane in `Blind-OOB-and-Parameter-Entities.md`; upload carriers in
`File-Upload-and-Format-Vectors.md`; XML-RPC auth chain in `XML-RPC-Chains.md`; cloud-metadata
escalation in `../SSRF/Cloud-Instance-Metadata.md`.
