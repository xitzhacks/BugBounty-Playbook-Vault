---
title: "Format-Vector XXE — XLSX, XLF, SVG, C-CDA, and import-feature carriers"
type: playbook
category: file-upload-format-vectors
cwe: "CWE-611"
source_count: 22
full_bodies_available: 5 (+2 metadata-only + 1 adjacent-FPD + 1 404)
corpus: "h1.security.nathan.sx roster (44 rows), bodies via hackerone.com/reports/<id>.json"
list_accessed: "2026-10-27"
note: "Anchor body: XXE-232614 (Weblate XLF, sev=high). Claims trace to bodies read 2026-10-27."
---

# Format-Vector XXE — when the XML hides inside a container

## 1. Overview

The highest-yield XXE lane in the corpus is not a raw XML endpoint — it is an **import feature**
that parses XML derived from a file the user supplies: XLIFF translation exports, XLSX
spreadsheets (which are ZIPs of XML), C-CDA patient records, SVG images. The UI never says
"XML"; the parser sits one layer behind the file extension.

**Case-ID scheme: `XXE-<report id>`.**

## 2. The anchor case — XXE-232614 (Weblate, XLF)

Reported against *"Weblate 2.15-dev"*, sev **high**. The reporter states the capability gate and
the default-expansion risk, verbatim:

> Weblate users in the Translate group (or those with the ability to upload translation files) can
> trigger XML External Entity Execution.

> The core of the vulnerability is in how the translate-toolkit processes .XLF files. The XLIFF
> standard is XML based, and thus supports by default standard XML functionality including external
> entity execution.

The reproduction is a four-step recipe an agent can transplant to any upload-back workflow:

1. *"Go to a component, and download its translations as XLF"*
2. *"Add the following two lines after the "<?xml" tag, and replace one of the translation texts
   with "&xxe;""* —
   ```xml
   <!DOCTYPE foo [ <!ELEMENT foo ANY >
   <!ENTITY xxe SYSTEM "file:///etc/passwd" >]>
   ```
3. *"Upload the file back to the server"*
4. *"Observe the contents of the passwd file as a translation"*

The payload is the **canonical inline general entity** — no parameter entities, no OOB, no
staging DTD. The reflection channel is the application's own UI: the passwd file *renders as a
translation row*. And the reporter prices the class precisely, naming the mitigating factors the
program will weigh:

> The mitigating factors here for you are that some account priveleges are required to upload
> tranlation files, although by default this gets rolled into the @Translate group.

## 3. The container variant — XXE-105434 (Informatica, XLSX)

XLSX is a ZIP of XML parts; the import parser eats `xl/worksheets/sheet1.xml` — the researcher
opened the archive and *wrote the prologue into a worksheet*, with `PUBLIC` in place of `SYSTEM`
(same effect for resolution, occasionally different filter behavior):

> 1. Open file xxe.xlsx like zip-archive
> 2. Read file xxe.xlsx\xl\worksheets\sheet1.xml
>
> In file I wrote XXE payload:
> `<!DOCTYPE foo [  <!ELEMENT foo ANY ><!ENTITY xxe PUBLIC "lol" "file:///etc/passwd" >]>`

and the reflection is the full passwd rendered through the import result — 29 accounts, ending in
the infrastructure fingerprint that reads like a confessional:

> ec2-user:x:500:500::/home/ec2-user:/bin/bash
> …
> dataprep:x:504:505::/home2/dataprep:/bin/bash

`ec2-user`, `scom`, `nslcd`, `dataprep`, `zabbix` — the file disclosed not just accounts but the
deployment topology (AWS EC2, SCOM monitoring, LDAP sync, a *dataprep* product user). Archive
severity: `high`, weakness label `Uncontrolled Resource Consumption` — wrong-vs-body on both; the
body demonstrates full arbitrary file read.

## 4. The healthcare variant — XXE-55431 (drchrono, C-CDA)

Same recipe on a medical-record import, verbatim:

> 3. Click on ' Update patient (via C-CDA XML).'
> 4. Select the file I attached, (AXAX000001.xml), I download it from your site and added there
> struct for my exploit.
> 5. Click on 'Preview' and you'll see the content of /etc/passwd, (That can be any file on the
> system or any command).

Note the claim inflation at the end — *"(That can be any file on the system **or any command**)"* —
the body demonstrates file read in a Preview pane; the "any command" (RCE) claim is unproven in
body and unclaimed by the team. The weakness label is `Code Injection`. Record demonstrated, note
claimed. Also note the reporter *downloaded the file from the site itself* and edited it — the
download-mutate-upload loop again (identical to the XLF anchor).

## 5. The image variant — SVG (XXE-104620 Coinbase, XXE-130661 Moneybird)

XXE-104620's entire body, verbatim:

> upload svg photo (XML based) as App logo contain XML payload renamed to .jpg server start
> execute this XML payload

Two operational facts in one sentence: the **rename-to-.jpg bypass** (extension filter sees an
image; the parser sees XML), and the decisive qualifier **"server start execute"** — the parse
must happen server-side. Coinbase disposed it *informative* (the logo path had no sensitive
backing); the technique itself was real. The reporter even cites prior art:
*"the same vulnerability was in https://www.coinbase.com/careers … one year ago"*.

XXE-130661 (Moneybird, metadata-only) team summary confirms the standard fix shape:

> Researcher found an XXE issue in SVG files uploaded to our software. We gave improved our
> software to actively scan for these vulnerabilities and prevent any harm.

**The server-vs-client trap** (zseano's guide, byte-quoted in `references/blogs-index.md` §1):
if the pingback arrives from *your own IP*, your **browser** rendered the SVG — not a bug. It is
only a bug when the callback's source IP is the **target's** egress.

## 6. The no-egress successor — error-based via local DTD

Post-roster, bibliographic (blogs-index §2): mohemiv's *Exploiting XXE with local DTD files* and
honoki's *From blind XXE to root-level file read access* — when outbound connections are firewalled,
spawn the **local** DTD already on disk (`/usr/share/xml/…`, Java runtime DTDs) and force a
parameter-entity collision whose error message carries the file. pwn.vg's XLIFF writeup is the
modern version of this exact module's carrier (error-based XXE via XLIFF upload). These are a hunt
queue, not proof — fetch before citing as evidence.

## 7. The adjacent-FPD case — XXE-8091 (Localize) — honest boundary label

Matched the roster because it lives in the **Import XML section**, but on body read it is **not
entity XXE**: it is PHP array-parameter type juggling → error → full path disclosure, verbatim:

> POST : http://www.localize.io/import/ [project ID] … Content-Disposition: form-data;
> name="importFileXML"; filename=""

> I just Added "[]" after *import[overwrite]* and Replied.
> `Warning: trim() expects parameter 1 to be string, array given in
> /var/www/vhosts/lvps178-77-99-228.dedicated.hosteurope.de/httpdocs_localize/index.php on line 410`

The lesson an agent keeps: **an import feature's error paths leak before any entity is fired** —
the same POST slot that discloses paths on step 0 is the slot the entity rides on step 1. Kept in
this module as carrier evidence, recorded in the register as adjacent (`Information Disclosure`),
never counted as XXE.

## 8. Metadata-only upload rows + the dark row

- **XXE-105787** (Informatica, sev high): *"The attacker was able to execute XXE in one of the
  file upload feature."* — team summary only.
- **XXE-130661** (Moneybird): quoted §5.
- **XXE-229980** (Trello, **404**): title recorded — *"XML entity expansion using svg file"* —
  the billion-laughs lane on SVG; nothing else recoverable.

## 9. Agent execution template

1. **Enumerate every file-consuming import** (translation import, spreadsheet import, patient
   record import, logo/avatar upload, report import) — the corpus's carriers were all *features*,
   not debug endpoints.
2. **Round-trip first**: download a legitimate file from the feature itself (both anchors did);
   you inherit a schema-valid skeleton that survives validation.
3. **Inject the prologue**: two DOCTYPE lines after `<?xml`, one entity reference dropped into an
   existing text node — the anchor's minimal diff.
4. **Container-aware**: for XLSX/XLTX/PPTX/DOCX, unzip → edit the inner part → rezip; sheet1.xml
   is the usual first read (§3).
5. **Rename games**: `.svg→.jpg` and content-type mismatches are the bypass lane (§5); the judge
   is *who* parses — server IP callback or nothing.
6. **Reflection or OOB**: rendered-as-data (§2, §3) > error text (In-Band module §2.1) > OOB
   callback (Blind module) > local-DTD error oracle (§6).

## 10. Validation gates

1. **The file you uploaded is the file that was parsed** — round-trip provenance shown (downloaded
   from the feature, modified, uploaded; both anchors document this).
2. **Contents or callback attributable to the target** — passwd text in the UI (§2/§3), or a
   callback with the server's egress IP/runtime; browser-rendered SVG pingbacks are a kill.
3. **Privilege context stated** — the anchor reports its own gate (@Translate group); don't bury
   an auth requirement that halves severity.
4. **Minimal diff PoC** — two lines + one `&xxe;` (§2's exact diff) beats a Frankenstein file;
   reviewers can diff it.
5. **Claims ≤ body** — "any command" stays unclaimed until shown (§4 discipline).

**Cross-references**: reflected-error channel in `In-Band-File-Read.md`; OOB ladder in
`Blind-OOB-and-Parameter-Entities.md`; PHP-array type-juggling FPD adjacent to
`../XSS/`-class error disclosure; SVG client-side rendering trap canonized in
`references/blogs-index.md` §1.
