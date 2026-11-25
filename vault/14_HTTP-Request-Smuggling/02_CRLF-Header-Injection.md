---
title: "CRLF / HTTP Header Injection — response splitting, Set-Cookie smuggling, library header validation gaps, URL-newline display tricks"
type: playbook
category: crlf-header-injection
cwe: "CWE-113"
source_count: 9
full_bodies_available: 9
corpus: "h1-brain disclosed_reports.db (sha256 8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4), bucket smuggling-crlf"
list_accessed: "2026-11-07"
note: "Anchors: SMUG-237357 (vpn.bitstrips.com Set-Cookie via %0a), SMUG-858650 (starbucks response splitting), SMUG-1878489 (undici host CVE-2023-23936, $600), SMUG-1664019 (undici content-type CVE-2022-35948). All 9 bodies read end-to-end 2026-11-07."
---

# CRLF / HTTP Header Injection — forge the response, not the request

## 1. Overview

Nine rows, **$1,300/3 paid** — the vault's thinnest money but the widest
technique spread. Where module 01 desyncs two servers, this module corrupts one
response stream: raw CR/LF reaches a header value, the response compiler accepts it,
and the attacker controls the next header — or the whole body. Evidence covers the
pure web lane (Set-Cookie forging on a session URL, an OAuth `redirect_uri` that
becomes a fake `location:` header), the library lane (Node `undici` failing to
validate `host` and `content-type`, urllib handing an injected Redis packet stream
to `SOCK_STREAM`), and the display lane (a `%0d` inside a tweet URL that the
rendering layer never shows). One row (Nextcloud) is about files whose names keep
their control bytes — a stored CRLF waiting for the response that quotes them.

**Case-stock (9 rows / $1,300):**

| Case | Target | Mechanism | Bounty |
|---|---|---|---|
| [SMUG-1878489](https://hackerone.com/reports/1878489) | Node undici (16.x/18.x/19.x) | `host` header taken raw in `processHeader` — no `headerCharRegex` check → CRLF (CVE-2023-23936) | $600 |
| [SMUG-409512](https://hackerone.com/reports/409512) | Apache mod_userdir 2.4.x | CR/LF in `Location`/outbound header value — response splitting (CVE-2016-4975) | $500 |
| [SMUG-2147132](https://hackerone.com/reports/2147132) | bugzilla.mozilla.org OAuth | `redirect_uri=%0d%0axxx:something` → attacker-chosen `xxx:` header + fake redirect | $200 |
| [SMUG-237357](https://hackerone.com/reports/237357) | vpn.bitstrips.com | `%0aSet-Cookie:malicious_cookie1` in session path → forged Set-Cookie on 302 | - |
| [SMUG-858650](https://hackerone.com/reports/858650) | www.starbucks.com | `%0d%0aset-cookie:foo%0d%0a%0d%0a` → response splitting on newsletter endpoint | - |
| [SMUG-712979](https://hackerone.com/reports/712979) | Twitter/X composer | `%0d` between two URLs: display says `fakewebsite.twitter.com`, link is `fakewebsite.tw`+`itter.com` | - |
| [SMUG-446271](https://hackerone.com/reports/446271) | ads.twitter.com | `?t=%0d%0atest:tested` → response splitting, attacker-set header | - (module 04) |
| [SMUG-590020](https://hackerone.com/reports/590020) | Python urllib | Unsanitized headers to `SOCK_STREAM` → attacker-controlled packet stream, internal Redis SSRF (CVE-2019-9947) | - |
| [SMUG-1402249](https://hackerone.com/reports/1402249) | nextcloud/server | `verifyPosixPath` trims *before* the control-character check → filenames keep `\n\r\t\v` (CVE-2022-24888) | - |

## 2. The web lane: forging headers on a live response

**SMUG-237357 (vpn.bitstrips.com)** is the minimal CRLF — one `%0a` in a URL path,
one forged `Set-Cookie` in the 302 that follows:

> By injecting a Carriage Return and Line Feed character, we are able to make the server issue a set-cookie header.

> As can be seen in the response, the server will issue a Set-Cookie header with an arbitrary value and that cookie will be set on the client.

The report's mitigation demand is the playbook line: "the application should strip
out any input which contains the %0d%0a URL encoded characters" (byte-true as
written).

**SMUG-858650 (starbucks)** goes one step further — the split ends in a full fake
body, the classic response-splitting definition:

> The vulnerability allows setting arbitrary headers, and also enables response splitting which can then be exploited further.

The PoC is a single `curl` with `--http1.1` and `%0d%0aset-cookie:foo%0d%0a%0d%0a`
in the prospect-email path.

**SMUG-2147132 (bugzilla.mozilla.org OAuth authorize)** is the redirect-parameter
variant — no auth needed, the `redirect_uri` becomes the header:

> CRLF / HTTP Header Injection.
> Allows you to set any headers/etc (Set-Cookie...)

The decoded observation is doable without a browser request at all: the `location:`
header renders as `xxx: something?error=invalid_scope`, i.e. the browser is
redirected to an attacker-parseable authority. The stated impact carries the
session-manipulation theory in full:

> Possible manipulation of user session / open redirect.

**SMUG-409512 (Apache mod_userdir, CVE-2016-4975, $500)** is the CVE shelf for the
same bug — one line:

> Possible CRLF injection allowing HTTP response splitting attacks for sites which use mod_userdir.

The fix reference is the lesson: httpd "prohibit CR or LF injection into the
'Location' or other outbound header key or value" from 2.4.25/2.2.32.

**SMUG-446271 (ads.twitter.com)** is module 04's simplest row, kept here in the
register (moved to Adjacent at read time, double-counted nowhere):

> an attacker can set new header

## 3. The library lane: when the client library writes the CRLF for you

**SMUG-590020 (Python urllib, CVE-2019-9947)** is three sentences and a pointer
to `bugs.python.org/issue35906`. Its impact line upgrades response splitting to
raw-socket SSRF:

> e.g. can exploit a internal redis server to send arbitrary packet data including ascii and non-ascii.

That is the library-gap lesson: urllib's own client code writes attacker bytes
onto a `SOCK_STREAM`; CRLF is not a browser-header trick, it is a wire-format
primitive for every plaintext protocol the socket reaches.

**SMUG-1664019 (undici content-type, CVE-2022-35948)** and **SMUG-1878489
(undici host, CVE-2023-23936, $600)** are the two paired undici validation gaps —
same library, same missing check in `request.js`, two different header fields:

> undici library should be protects HTTP headers from CRLF injection vulnerabilities. However, CRLF injection exists in the ‘content-type’ header of undici.request api.

(SMUG-1664019)

> The above snippet will perform two requests in a single request API call:

> undici library should be protects HTTP headers from CRLF injection vulnerabilities. However, CRLF injection exists in the ‘host’ header of undici.request api.

(SMUG-1878489)

The host-row body gives the source-level root cause — `request.host = val`
commented `// without headerCharRegex.exec(val)`, i.e. the validation regex exists
but the host branch skips it. Impact note verbatim: "All versions of the 19.x,
18.x and 16.x release lines." The pair is also the playbook's negative lesson for
*partial validation*: fixing `content-type` without `host` (or the reverse) is
two CVEs for one missing regex call.

## 4. Display lane and stored lane

**SMUG-712979 (Twitter/X)** is the only CRLF row that smuggles nothing on the
wire — the `%0d` is invisible to the person reading the tweet, and the hyperlink
it parses as is a different authority than the one displayed:

> When composing a tweet or a direct message it is possible to use a new line character (`%0d`) to seperate two URLs within the actual hyperlinking process, but not the URL displaying process.

The body also self-concedes the classification dispute ("I don't think this falls
under any real classification of issues other than 'CRLF injection', but even
then, it's definitely not the right category") — take it as a display-integrity
primitive, paid later when the phishing angle is explicit.

**SMUG-1402249 (nextcloud/server, CVE-2022-24888)** is the filter-ordering bug —
`trim()` runs *before* `scanForInvalidCharacters()`, so leading/trailing `\n\r\t\v`
survive into filenames on disk:

> It is possible to create files and folders that have leading and trailing `\n`, `\r`, `\t`, and `\v` characters. The server rejects files and folders that have these characters in the middle of their names, so this might be an opportunity for injection.

The report's closing hedge is the quote to keep: stored control bytes are a
hardening issue until a response quotes the name unfiltered:

> This may just be a hardening issue, but if the file or directory names are inserted into an HTTP response unfiltered, CRLF injection may occur.

## 5. What pays, what doesn't

- **Library CVEs pay per missed header field**: the two undici rows are the paid
  lane ($600 host; content-type unpaid in DB but CVE-2022-35948 through ibb) —
  Node ecosystem disclosures against `github.com/nodejs/node` are the module's
  ceiling. Django/Python/urllib got the same treatment at CVE level (no DB
  figure), reinforcing that *filed-upstream-against-source* is the price floor
  of this class.
- **The Apache CVE shelf (SMUG-409512, $500)** shows the vendor-advisory pricing:
  mod_userdir response splitting at 2.4.x was a "$500-while-the-vendor-still-fixed-
  2.2.32" find.
- **Web-hunt CRLFs on product code mostly carry no DB figure**: bitstrips ($no
  figure, 2017), starbucks ($no figure), Mozilla ($200), twitter ($no figure) —
  response splitting is priced Low/Info at triage unless the split demonstrably
  owns its victim's session (Mozilla's redirect_uri got the $200; the
  Set-Cookie forgeries got nothing recorded). The starbucks closing notes the
  honest impact ladder anyway:

> Possible impacts include;

- **Display-only tricks price at $0**: the tweet-%0d row's value is social-engineering
  leverage, and the corpus shows it at no figure — it is kept because its
  "displayed vs parsed" gap is the XSS-lens analogue of request smuggling.
- **Stored control-byte names (CVE-2022-24888)** reached only CVE with no corpus
  bounty — file-name-the-CRLF hygiene is hardening until the response quotes it.

## 6. Cross-references

- The undici `headerCharRegex` skip is the exact missing check in module 01's
  llhttp rows — one corpus of validators, two libraries, same class.
- urllib's Redis-packet trick (SMUG-590020) is the SMTP-payload twin of module 03:
  the Grafana row and the Nextcloud SMTP rows all turn one missing newline check
  into protocol injection against whatever the socket reaches next.
- Response splitting with a poisoned `Set-Cookie` is module 01's hijack economy
  without a second server — this module's forged header is SMUG-737140's
  Collaborator redirect, minus the desync.
- The Apache mod_userdir/mod_proxy rows (SMUG-409512 here, SMUG-1391549/1594627
  in module 04) jointly map the httpd parser-surface; the Cache-Poisoning vault
  (row 15) consumes both response-splitting and desync-poisoned caches.
