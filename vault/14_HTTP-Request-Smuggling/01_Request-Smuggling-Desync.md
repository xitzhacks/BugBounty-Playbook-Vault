---
title: "HTTP Request Smuggling & Desync — CL.TE / TE.CL / obfuscated Transfer-Encoding, duplicate headers, trailer and llhttp parser differentials"
type: playbook
category: http-request-smuggling-desync
cwe: "CWE-444"
source_count: 22
full_bodies_available: 22
corpus: "h1-brain disclosed_reports.db (sha256 8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4), bucket smuggling-crlf"
list_accessed: "2026-11-07"
note: "Anchors: SMUG-2299692 (Tomcat trailer CVE-2023-45648, $4,660), SMUG-2327341 (Tomcat client-side desync CVE-2024-21733, $4,660), SMUG-2280391 (Tomcat trailer size limit, $4,660), SMUG-1667974 (Apache pause desync, $4,000). All 22 bodies read end-to-end 2026-11-07."
---

# HTTP Request Smuggling & Desync — two parsers, one connection

## 1. Overview

Twenty-two rows, **$27,740/14 paid** — the vault's money module. The class is a
*parser differential*, never a single-server bug: a front-end (proxy, load balancer,
framework) and a back-end disagree about where request N ends and request N+1 begins,
so bytes the attacker controls are left on the connection to prepend to, splice into, or
replace a victim's request. Corpus evidence splits into four parser families: the
classic **Content-Length / Transfer-Encoding disagreement** (CL.TE, TE.CL, TE.TE), the
**obfuscated Transfer-Encoding header** (space before colon, tab after colon, leading
space, duplicate headers, `identity` suffix), the **Node `llhttp` grammar drift** (CR
without LF, chunk-extension newline, space before colon) and the **Tomcat trailer /
Apache pause** rows. Tooling runs from a single Burp Repeater send to the Turbo
Intruder `desync + N victim-race` script; impact tops at bulk session hijack and
cache poisoning, bottoms at speculative "potential" parser bugs the reporter never
weaponized.

**Case-stock (22 rows / $27,740):**

| Case | Target | Mechanism | Bounty |
|---|---|---|---|
| [SMUG-2327341](https://hackerone.com/reports/2327341) | Apache Tomcat 8.5/9.0 | Client-side desync: server misprocesses Content-Length of POSTs → victim browser desync (CVE-2024-21733) | $4,660 |
| [SMUG-2299692](https://hackerone.com/reports/2299692) | Apache Tomcat <11.0.0-M11/10.1.13/9.0.80/8.5.93 | Trailer-section misparse (line without colon skipped) → proxy sees one request, Tomcat sees two (CVE-2023-45648) | $4,660 |
| [SMUG-2280391](https://hackerone.com/reports/2280391) | Apache Tomcat 9.0.82 | Trailer header over size limit throws → one request treated as multiple | $4,660 |
| [SMUG-1667974](https://hackerone.com/reports/1667974) | Apache HTTPD | Pause-based desync → server-side smuggling + TLS-defeating MITM JS injection | $4,000 |
| [SMUG-1630667](https://hackerone.com/reports/1630667) | Node/llhttp | Incorrect parsing of multi-line Transfer-Encoding (CVE-2022-32215) | $1,800 |
| [SMUG-1630668](https://hackerone.com/reports/1630668) | Node/llhttp | Flawed parsing of Transfer-Encoding (CVE-2022-32213) | $1,800 |
| [SMUG-1630669](https://hackerone.com/reports/1630669) | Node/llhttp | Improper delimiting of header fields (CVE-2022-32214) | $1,800 |
| [SMUG-2032842](https://hackerone.com/reports/2032842) | Node 20.2.0/llhttp | Empty headers separated by CR alone delimit a `Transfer-Encoding: chunked` header (CVE-2023-30589) | $1,800 |
| [SMUG-726773](https://hackerone.com/reports/726773) | labs.data.gov | Front uses TE, back uses CL → Turbo Intruder desync + 14 victim races → Collaborator redirect; 67 reflections | $750 |
| [SMUG-713285](https://hackerone.com/reports/713285) | pscp.tv / periscope.tv | CL/TE disagreement on many subdomains; desync → DoS, CSRF/cookie bridge, victim request poisoning | $560 |
| [SMUG-965267](https://hackerone.com/reports/965267) | ruby/webrick | `Transfer-Encoding: AAAchunkedBBB` fakes a chunked request via regex match | $500 |
| [SMUG-1002188](https://hackerone.com/reports/1002188) | Node.js (+HAProxy) | Duplicate `Transfer-Encoding` header: Node reads first only, proxy reads the false one (CVE-2020-8287) | $250 |
| [SMUG-1238099](https://hackerone.com/reports/1238099) | Node 16.3.0/llhttp + ATS 9.0.0 | llhttp ignores chunk extensions → `\n` hides a smuggled `/admin` request from the proxy (CVE-2021-22960) | $250 |
| [SMUG-1238709](https://hackerone.com/reports/1238709) | Node 16.3.0/llhttp | Space before colon in `Content-Length :` accepted → proxy ignores, Node honors (CVE-2021-22959) | $250 |
| [SMUG-737140](https://hackerone.com/reports/737140) | slackb.com | CL.TE: `Transfer-Encoding : chunked` → request hijack → 301 leaks `d` session cookies to Collaborator | - |
| [SMUG-771666](https://hackerone.com/reports/771666) | api.zomato.com | CL.TE `tabprefix1` (tab after TE colon) → bulk `X-Access-Token` theft via Collaborator redirect | - |
| [SMUG-867952](https://hackerone.com/reports/867952) | console.helium.com | CL.TE via leading-space `Transfer-Encoding` → `200 OK` where `401` expected; claimed session/cache impact | - |
| [SMUG-919175](https://hackerone.com/reports/919175) | basecamp.com | Double `Transfer-Encoding: chunked` + `identity` → desync + `X-Forwarded-Host` cache poisoning | - |
| [SMUG-867577](https://hackerone.com/reports/867577) | launchpad.37signals.com | Dual valid/invalid TE (`chunked` + `foo`) → unauthenticated desync, socket poisoning, cookie capture | - |
| [SMUG-753939](https://hackerone.com/reports/753939) | dashboard.fortmatic.com | Leading-space TE header → next valid request gets reflected S3 HMAC error page (DoS) | - |
| [SMUG-735748](https://hackerone.com/reports/735748) | (Node, PDF writeup) | Malformed `Transfer-Encoding` via attached PDF (CVE-2019-15605) — attachment only | - |
| [SMUG-922597](https://hackerone.com/reports/922597) | Node.js | CR in header name converted to hyphen → `Content[CR]Length` becomes Content-Length Node-only (CVE-2020-8201) | - |

## 2. The crown rows: Tomcat trailer desync and client-side desync

The three Tomcat rows are the vault's ceiling — $4,660 each, clean CVE-backed
disclosures against `https://github.com/apache/tomcat`, and the only rows where the
*body* is written as an upstream security advisory rather than a web-hunt proof.

**SMUG-2299692 (CVE-2023-45648)** names the whole differential in one paragraph:
where Tomcat skips a colon-less trailer line, NGINX counts the same bytes as the
second request:

> Apache Tomcat supports Trailer Section. However, we found that in version prior than 11.0.0-M11, 10.1.13, 9.0.80, 8.5.93, Apache Tomcat cannot properly parse the trailer section if there's no colon in the trailer header's line. It will skip the following lines until the last line with a valid colon-separated key-value header pair, which can be leveraged to perform HTTP request smuggling.

> If we send the following payload, the headers of the second request **(Line 12-15)** will be regarded as the trailer section of the first request, while the content of the second request **(Line 17-19)** is processed as the second request. When sending this payload to other HTTP implementations such as NGINX, **Line 12-21** would be the second request.

The proof is two logged requests (`POST /benign_path` then `GET /evil_path`) with a
copy-paste `nc` one-liner — no proxy gymnastics, because the divergence is named.
Impact is stated exactly:

> It can be leveraged to perform HTTP request smuggling in order to bypass security mechanisms when Apache Tomcat is deployed behind a reverse proxy.

**SMUG-2280391** is the same parser family by a second route — an oversized trailer
header makes Tomcat split one request into two:

> Request smuggling was possible by throwing an IOException with the upper size limit of the trailer header.
> Confirmed with tomcat version 9.0.82.

> A trailer header that exceeded the header size limit could cause Tomcat to treat a single request as multiple requests leading to the possibility of request smuggling when behind a reverse proxy.

**SMUG-2327341 (CVE-2024-21733)** is the client-side desync (CSD) crown, aimed at
the *victim browser connection* rather than a proxy back-end:

> Client-side de-sync (CSD) vulnerabilities occur when a web server fails to correctly process the Content-Length of POST requests. By exploiting this behavior, an attacker can force a victim's browser to de-synchronize its connection with the website, causing sensitive data to be smuggled from the server and/or client connections.

> An attacker can force a victim's browser to de-synchronize its connection with the website, causing sensitive data to be smuggled from the server and/or client connections.

Note the boundary honesty: the PoC is a single `Content-Length: 6` POST with a
one-letter body, and the body says "In some cases, this can leak sensitive data such
as clear-text credentials" — the class lesson is that a Content-Length mishandling
turns the *browser's* connection into the smuggle medium.

## 3. CL.TE / TE.CL hijacks: the slackb.com and Zomato payloads

Two rows carry the strongest impact proofs in the corpus — full request hijacks
executed with an off-the-shelf smuggling scanner plus one Burp Collaborator URL, both
against high-traffic API hosts, neither with a bounty figure in the DB (which records
the *absence* of a figure, not a $0 finding).

**SMUG-737140 (slackb.com)** defines the primitive cleanly before weaponizing it:

> A CLTE is a webrequest that has both the `Transfer-Encoding: chunked` header (specified in some abnormal way) and the `Content-Length: ` header. According to the RFC when both headers are specified the TE always takes priority. However, if the TE header is malformed the webrequest may get interpreted differently between the frontend and the backend server. The CLTE issue found on slackb.com is when the frontend server interprets the request sized using `Content-Length` and the backend server interprets the request using the `Transfer-Encoding: chunked` method. This causes a desync on the webrequest and can poison the backend socket causing data to be pre-pended to the next webrequest from a victim. The `space1` payload places a space character in between `Transfer-Encoding` and the colon `:`. This is enough for the frontend to not understand the request as TE and instead as CE but not enough for the backend to process it in the same way.

The kill is a hijack through a smuggled request line — the 301's `d` cookie goes to
the attacker's Collaborator:

> At this point you just attacked an arbitrary slack customer and have access to her `d` session cookie.
> From here you can plug the session cookie into your browser and have full account takeover, Scrape all data and move onto the next victim.

Tooling note preserved in the body: `smuggler -u https://slackb.com` with the
`space1` test is the entire scanner — one flag, one payload class.

**SMUG-771666 (api.zomato.com)** is the same shape over a *tab* mutation
(`tabprefix1`, 150+ payload types evaluated), with bulk token theft as the claim:

> I have custom tools to evaluate over 150 types of HTTP Smuggling Payloads.

> the frontend server rejects that line and processes the whole request using the length of 51 found in the Content-Length header and forwards all 51 bytes of data to the backend server. The backend server sees the same HTTP request and processes the `Transfer-Encoding : chunked` as a normal chunked request. The issue is that the chucked request specifies 0 bytes of data and the remaining data of the 51 bytes is left on socket to poison the next customer request that comes into the backend server.

> Attacker can achieve victim session takeover in bulk and steal all information from the victim.

The triage note worth copying into any playbook — "Sometimes you may just see DNS
requests to your collaborator. Send the payload out as many times required to see an
HTTP request" — is the probabilistic-poisoning admission.

## 4. Obfuscated Transfer-Encoding: the parser-mutation catalog

The telemetric lesson of this module is that most web-front-end smugglable
differentials are one stray character in the `Transfer-Encoding` line. Evidenced
mutations, one per row:

- **Space before colon** (`Transfer-Encoding : chunked`, `Content-Length : 5`) —
  SMUG-737140 (`space1`), SMUG-726773 (`Transfer-Encoding : chunked`), SMUG-1238709.
  The labs.data.gov row states it compactly:

> The application appears to be vulnerable to HTTP request smuggling due to a disagreement between the front-end and back-end server, where the front-end server uses the Transfer-Encoding header to determine content in the HTTP body, but back-end server uses the Content-Length header, which causes a desync.

- **Tab after colon** (`Transfer-Encoding:\tchunked`, smuggler's `tabprefix1`) —
  SMUG-771666, payload excerpt as in §3.
- **Leading space** (` Transfer-Encoding: chunked`) — SMUG-867952, SMUG-753939.
  The fortmatic row fired it at a login endpoint and watched the error page of the
  poisoned next request reflect back:

> The back end leaked the hmac the back end reflected back the hmac key encryption type, and a lot of details.

> The miss configuration with the back end cause it to reflect back the error page when the next valid request comes through. This will lead to a DOS serve this error page when visitor view the website.

- **Dual/invalid TE** (`Transfer-Encoding: chunked` + `Transfer-Encoding: foo`) —
  SMUG-867577, which reads the differential explicitly:

> The desync occurs when sending a request with a `Content-Length` header and a valid `Transfer-Encoding` header followed by an invalid `Transfer-Encoding` header. The frontend server only examines the second `Transfer-Encoding` which is invalid, so it uses the `Content-Length` instead. However the backend server prioritises the valid `Transfer-Encoding` header and therefore ignores the `Content-Length`.

- **Double TE with `identity` suffix** (`Transfer-Encoding: chunked` +
  `Transfer-encoding: identity`) — SMUG-919175, combined with an `X-Forwarded-Host`
  redirect to poison the cache:

> Using HTTP request smuggling attack, It is possible to poison the cache with the off-site redirect response using `X-Forwarded-Host` request header in smuggled request.

- **Duplicate TE ignored after first** (TE-TE) — SMUG-1002188:

> Attacker can use two same header field make TE-TE HTTP Request Smuggling attack.

> But nodejs only identify the first header field and ignore the after.

- **Substring match** (`Transfer-Encoding: AAAchunkedBBB`) — SMUG-965267, whose
  prose is the mechanism:

> a attacker may use  a ```Transfer-Encoding: AAAchunkedBBB``` header to fake a legal header. than can make a HTTP Request Smuggling attack.

- **CR-to-hyphen rename** (`Content[CR]Length`) — SMUG-922597:

> Apparently, node.js converts CR in HTTP request headers to hyphen before parsing.

> Consider an HTTP request with Content[CR]Length header . Suppose a proxy in front of node.js ignores the Content[CR]Length header (and therefore assumes a 0-length body). node, on the other hand, converts the CR to a hyphen and uses the value of the (newly formed...) Content-Length header. HTTP Request Smuggling ensues.

## 5. Node llhttp grammar drift and the Apache pause

Four paid rows ($1,800 twice over) are llhttp strictness failures, and one Apache
row is the timing variant. They are the parser-is-the-bug lane: no new technique,
just bytes RFC 7230 forbids that the parser accepts.

**CR without LF (SMUG-2032842, CVE-2023-30589):**

> The `llhttp` parser in the http module in Node v20.2.0 does not strictly use the CRLF sequence to delimit HTTP requests.

> The CR character (without LF) is sufficient to delimit HTTP header fields in the llhttp parser. According to RFC7230 section 3, only the CRLF sequence should delimit each header-field.

The wire trick is `X-Abc:\rxTransfer-Encoding: chunked` — one bare CR turns a
harmless header into a TE header only the back-end sees.

**Chunk-extension newline (SMUG-1238099, CVE-2021-22960):**

> `llhttp` doesn't try to parse the chunk extension properly, but simply ignores every byte until it reaches a `\r` (source: https://github.com/nodejs/llhttp/blob/master/src/llhttp/http.ts#L736-L739). By following the ABNF of chunk extensions one can see that the only allowed bytes in this area are 0x09, 0x21-0x7e and 0x80-0xff. But `llhttp` allows any byte. This is the bug.

> By sending the data above when ATS is a proxy in front of Node, ATS will see one request to `/` and Node will see two requests, one to `/` and one to `/admin`. Note that all lines are terminated by CRLF (`\r\n`) and that `\n` should be replaced with an LF character.

The body is honest about the limit: with ATS hanging after chunked requests the
smuggler gets no response — control of the smuggled request, not its answer.

**Space before colon (SMUG-1238709, CVE-2021-22959):**

> The ``llhttp`` parser in the ``http``module in Node 16.3.0 accepts requests with a space (SP) right after the header name before the colon.

> The proxy would see the first and the second GET-request. But Node would see the first and the third GET-request.

**The CVE-2022-3221x trio (SMUG-1630667/1630668/1630669, $1,800 each)** are
one-line disclosures whose bodies point at the Original Reports; the shared Impact is
the class boilerplate:

> Depending on the specific web application, HRS can lead to cache poisoning, bypassing of security layers, stealing of credentials and so on.

Their register notes carry the CVE-to-technique map; there is no quotable payload.

**Pause-based desync (SMUG-1667974, Apache HTTPD, $4,000)** — two sentences, the
whole finding:

> Apache was vulnerable to a pause-based desync.

> This enables server-side HTTP Request Smuggling when Apache is deployed as a back-end server, and it also enables MITM attackers to inject arbitrary JavaScript in spite of TLS.

It is the module's only timing-based differential: the *pause* between
front-end and back-end processing is the desync, not a header byte.

## 6. What pays, what doesn't

- **Named-parser disclosures pay flat and guaranteed**: every Node/llhttp and
  Tomcat row with a CVE carries $1,800–$4,660; the three Tomcat rows are the
  corpus ceiling and all three are upstream-ibb filings against `github.com/apache/tomcat`
  or Node source (`github.com/nodejs/node`). Parser-drift CVEs are priced per variant
  (the CVE-2022-32213/32214/32215 trio at $1,800 each makes that literal).
- **Weaponized hijacks print impact, not bounties**: the two scariest rows here
  (slackb.com bulk `d`-cookie theft, Zomato bulk token theft) carry no DB figure at
  all; the one paid web-hunt row, labs.data.gov at $750, proved only redirection
  (67 Collaborator reflections, a `hopefully404` ploy) — desync *proof* is paid
  $250–$750, desync *theft* is what the reports claim for more.
- **DoS-only and attachment-only rows charge nothing in the DB**: fortmatic's
  reflected HMAC error page (desync real, value low) and SMUG-735748's PDF-only
  writeup (no quotable body):

> Please see the attached PDF for a writeup of this vulnerability.

- **"Potential" parser bugs with a toy stack and no front-end earn $250–$500**:
  webrick's substring regex and Node+HAProxy TE-TE both end with the same honest
  impact line:

> It is possible to smuggle the request and disrupt the user experience.

- **The high-traffic honest-limits row is SMUG-713285 ($560)**: pscp.tv/periscope.tv
  covers DoS, CSRF/cookie bridging and victim-request poisoning, but the report
  itself admits:

> seems that many subdomains in pscp.tv and periscope.tv vulenrable

(sic: "vulenrable")

> on a live site with a high volume of traffic like [www.pscp.tv] .it can be hard to prove request smuggling exists without exploiting numerous genuine users in the process.

## 7. Cross-references

- The Turbo Intruder `desync + 14 victim races` script from SMUG-726773 and the
  race-like victim-race structure in SMUG-867577/753939 (1,400 queued `target.req`
  copies) are the same synchronization primitive as the Race vault's Turbo Intruder
  gate module — one socket, N racing requests, one poisoned victim.
- Cache poisoning via smuggled `X-Forwarded-Host` redirects (SMUG-919175) hands
  off to the Cache Poisoning vault (master row 15) as web cache poisoning; the
  SSRF reader should note the 301-with-stolen-cookie shape in SMUG-737140
  is the Authentication-Session revocation problem.
- Parser-grammar twins: SMUG-2032842's bare-CR and SMUG-1402249's CRLF-filter
  holes are the same character-class story told on opposite sides of the proxy.
- SMTP newline injection (SMUG-1200647/1509216/1516377) is the same CRLF grammar
  against a plaintext protocol — see module 03; the Grafana row is the paid proof
  that "header injection" reaches RCE in the RCE vault's terms.
- The Apache rows (SMUG-1667974, SMUG-1594627 in module 04) belong in the
  Misconfiguration/TLS-era reading of front-end trust.
