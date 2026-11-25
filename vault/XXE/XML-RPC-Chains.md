---
title: "XML-RPC — the auth-bypass chain, the pingback DDoS, and the timing channel"
type: playbook
category: xmlrpc-chains
cwe: "CWE-611 (boundary: this module is XML-protocol abuse, not entity parsing)"
source_count: 22
full_bodies_available: 4
corpus: "h1.security.nathan.sx roster (44 rows), bodies via hackerone.com/reports/<id>.json"
list_accessed: "2026-10-27"
note: "Anchor body: XXE-138869 (Uber OneLogin bypass, $7,000 JSON-verified). Claims trace to bodies read 2026-10-27."
---

# XML-RPC — the protocol that outlived its parsers

## 1. Overview

XML-RPC endpoints are the XML surface that survives everywhere: WordPress `xmlrpc.php`, legacy
SOAP-fronted APIs, SSO bridges. This module owns the **protocol-abuse** lane — authentication
defeats, amplification, side channels — where the XML *format* is the carrier but the bug is in
the surrounding logic. (Entity parsing on these endpoints would fall to the In-Band/Blind
modules; none of this corpus's XML-RPC rows is entity-based.)

**Case-ID scheme: `XXE-<report id>`.**

## 2. The anchor case — XXE-138869 (Uber OneLogin bypass, $7,000 JSON)

The mechanism is a **default-password orphan** created by an SSO plugin, and the attack surface is
the API the SSO gate forgot, verbatim:

> When a user logs on one of your WordPress sites via OneLogin, the authentication plugin creates a
> new entry in the WordPress user database with the default password `@@@nopass@@@`.

> The OneLogin plugin does prevent logins through the normal *wp-login.php* page but fails to
> restrict the XMLRPC API. XMLRPC still honors the WordPress internal user database.

The full exploit is a single `curl`, byte-true:

```
curl 'https://newsroom.uber.com/xmlrpc.php' --data-binary "`cat options.xml`" -H 'Content-type: application/xml'
```

with `options.xml` a standard `<methodCall><methodName>wp.getOptions</methodName>` carrying
`<param><value>[REDACTED_EMAIL]</value></param><param><value>@@@nopass@@@</value></param>` — and
the response struct returns WordPress config (`software_version 4.4.3`, `blog_url`). The reporter
then escalated through the XML-RPC function inventory:

- `wp.newPost` — *"creating private posts too, e.g. for XSS-type attacks targeting administrators"*
- `metaWeblog.newMediaObject` — file upload, PoC'd with a `.key` file at
  `https://love.uber.com/wp-content/uploads/sites/5/2016/05/fooasfasfgdg.key`
- honest claim boundary: *"some of them could probably be used to achieve remote code execution"* —
  probable, not proven; the $7,000 priced the confirmed auth bypass + content/upload control on
  `love.uber.com` and `newsroom.uber.com`.

**The chain lesson**: SSO hardening applied to one auth surface (wp-login.php) while a second,
older surface (xmlrpc.php) still honored the same credential store. An agent's job is to
**enumerate every door that consults the same user database**, not just the patched one.

## 3. The amplification case — XXE-96294 (withinsecurity, pingback DDoS)

Discovery probe first — `demo.sayHello` as the liveness oracle, verbatim:

> `POST /xmlrpc.php HTTP/1.1 … <methodName>demo.sayHello</methodName>` … Notice that a successful
> response is received showing that the xmlrpc.php file is enabled.

Then the amplification primitive:

```xml
<methodCall>
<methodName>pingback.ping</methodName>
<params>
<param><value><string>http://173.243.56.36/</string></value></param>
<param><value><string>https://withinsecurity.com/2015/10/is-there-really-a-cybersecurity-skills-gap/</string></value></param>
</params>
</methodCall>
```

> As soon as the above request is sent, the victim host (173.243.56.36) gets an entry in its log
> file with a request originating from the withinsecurity.com domain verifying the pingback.
> This can be automated from multiple hosts and be used to cause a mass DDOS attack on the victim.

The shape: **source (victim) in param 1, own blog post in param 2** — WordPress relays the request.
One machine is noise; a botnet of pingback-enabled blogs is the historical attack. Validate with a
*single* callback to infrastructure you own, never against a third party.

## 4. The timing case — XXE-107296 (Automattic, $50 list)

Reported against Jetpack's XML-RPC signature check; the body demonstrates a hash-comparison
side channel via response-time measurement (weakness label: `Cryptographic Issues - Generic`).
Keep it as the reminder that XML-RPC auth plugins carry the same crypto failure modes as any
auth layer — timing, replay, enumeration — and the XML envelope is incidental. (For a full
timing-oracle discipline, cross-ref `../SQLi/Blind-SQLi.md`'s boolean-vs-time ladder.)

## 5. The exposure case — XXE-146093 (Nextcloud, informative)

*"XML-RPC Interface available"* is filed as one of several WordPress posture findings. Informative
disposition — availability of the endpoint alone is not a bug; it is the **precondition row** that
XXE-96294 (enabled pingback) and XXE-138869 (auth bypass) teach you to weaponize *only* when a
second factor (default credential, unrestricted method, signature flaw) exists.

## 6. Agent execution template

1. **Liveness oracle**: `demo.sayHello` (§3) — cheap, non-mutating, proves parsing + method dispatch.
2. **Method inventory**: WordPress core exposes ~80 functions (*"The XMLRPC system supports about
   80 functions by default"* — the anchor's count); enumerate `system.listMethods` where allowed.
3. **Credential-orphan hunt**: any SSO/LDAP/JIT-provisioned user is a candidate for a default or
   null credential (the `@@@nopass@@@` pattern); test the **API doors**, not just the login page.
4. **One-callback rule for pingback tests**: point param 1 at your own listener; logging a single
   verified relay is proof enough — mass-firing at third parties is out of bounds.
5. **Chain arithmetic**: endpoint-exposure (146093) + method-control + credential-orphan = the
   $7,000 shape; exposure alone = informative.

## 7. Validation gates

1. **A confirmed privileged operation** — the anchor created pages/posts and uploaded a file
   (URLs cited in-body); "could create" is not a gate.
2. **The credential mechanism named** — default password, bypassed check, or missing restriction,
   stated as the plugin's logic, verbatim if possible.
3. **Single-relay proof for DDoS claims** — one log entry from the target's domain, then stop.
4. **Scope labels** — Uber's `$7,000` and Automattic's `$50` are JSON/list-labeled in
   `references/case-register.md`; never blend bands.
5. **Impact narration honest** — probable-RCE framed as probable (§2's last quote); confirmed
   layers listed first.

## 8. Adjacency and boundaries

- **Not XXE**: none of these bodies fires an external entity — that boundary keeps the class
  counts honest (register §A vs §B).
- **Same-user-database doors**: modern equivalents are REST/XML-RPC dual surfaces on any CMS,
  SSO-bridged SaaS, and headless auth plugins. The door-enumeration rule transfers 1:1.
- **Post-roster modern cases** (blogs-index §2, title-only): Conviso's CVE-2024-43044 Jenkins
  agent file-read chain and the truesec PowerShell CLIXML deserialization attack are the
  XML-protocol-abuse successors.

**Cross-references**: entity-parsing lanes in `In-Band-File-Read.md` and
`Blind-OOB-and-Parameter-Entities.md`; SSO-verification bugs → `hunt-saml` skill scope
(`XXE-223014` boundary note in `Crossdomain-and-Parser-Adjacents.md` §7); upload-via-RPC chains →
`File-Upload-and-Format-Vectors.md`.
