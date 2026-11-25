---
title: "HTTP protocol flood DoS — CONTINUATION floods, slowloris, and connection-holding frames"
type: playbook
category: http-protocol-flood-dos
cwe: "CWE-400 (CWE-770 allocation without limits)"
source_count: 10
full_bodies_available: 10
corpus: "h1-brain disclosed_reports.db (3,673 rows; sha256 8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4) · bucket 'dos' = 221 rows, weakness 'Uncontrolled Resource Consumption'"
list_accessed: "2026-11-07"
note: "Anchor bodies: DOS-2586226 ($4,920), DOS-2334401 ($4,860), DOS-2453328 ($3,645). All 10 bodies read; quotes byte-true to references/archive/DOS-bodies-full-dump.txt."
---

# HTTP protocol flood DoS — frames that hold memory they never release

## 1. Overview

Ten rows, **$20,250/8 paid** — the vault's tightest, most modern module: one 2018 row
(384839), a Node.js cluster from the v13/v14 era (799072, 800140, 868834, 1043360), and a
2024 HTTP/2 wave where five of the vault's top web-facing figures sit. The shared
mechanism: a protocol feature that *buffers without a hard cap* — CONTINUATION frames
before `END_HEADERS`, chunk extensions the parser never walks, stream counters the
implementation miscounts — so the attacker commits bytes the server must hold while the
attacker holds nothing. The two Tomcat anchors:

> When processing an HTTP/2 stream, Tomcat did not handle some cases of excessive HTTP headers correctly. This led to a miscounting of active HTTP/2 streams which in turn led to the use of an incorrect infinite timeout which allowed connections to remain open which should have been closed.

> Since HTTP/2 connections are left open indefinitely, depending on configuration the DoS is caused either by the server running out of memory or by the open connections reaching maxConnections.

**Case-stock (10 rows / $20,250):**

| Case | Target | Mechanism | Bounty |
|---|---|---|---|
| [DOS-2586226](https://hackerone.com/reports/2586226) | ibb | HTTP/2 stream miscount → infinite-timeout leak (CVE-2024-34750) | $4,920 |
| [DOS-2334401](https://hackerone.com/reports/2334401) | ibb | CONTINUATION flood → HPACK OOM, GOAWAY-avoiding | $4,860 |
| [DOS-2453328](https://hackerone.com/reports/2453328) | ibb | CONTINUATION + RST race → Http2Session assert crash | $3,645 |
| [DOS-2375446](https://hackerone.com/reports/2375446) | ibb | unbounded chunk extension, timeouts don't help (CVE-2024-22019) | $3,495 |
| [DOS-2453322](https://hackerone.com/reports/2453322) | ibb | endless CONTINUATION buffered pre-413 → OOM (CVE-2024-27316) | $2,580 |
| [DOS-799072](https://hackerone.com/reports/799072) | nodejs | body 1 byte/sec slowloris keeps connection | $250 |
| [DOS-800140](https://hackerone.com/reports/800140) | nodejs | malformed HTTP/2 SETTINGS → SIGABRT | $250 |
| [DOS-868834](https://hackerone.com/reports/868834) | nodejs | unfinished HTTP/1.1 requests exhaust accept queue | $250 |
| [DOS-384839](https://hackerone.com/reports/384839) | ibb | crafted HTTP/2 requests exhaust connections (CVE-2018-1333) | - |
| [DOS-1043360](https://hackerone.com/reports/1043360) | nodejs | unknownProtocol HTTP/2 resource exhaustion | - |
## 2. The CONTINUATION flood: the 2024 HTTP/2 OOM wave

DOS-2334401 is the wave's defining report — headers sent in `HEADERS` + N×`CONTINUATION`
frames, each just under the server's header-byte limits, so no `GOAWAY/ENHANCE_YOUR_CALM`
fires, the headers sit in HPACK memory, and a few connections produce `OutOfMemoryError`:

> An attacker can send headers using HTTP/2 CONTINUATION frames up to the limit of header bytes, header size and connection overhead so that connection is not dropped by a server (GOAWAY/ENHANCE_YOUR_CALM). Once frames are sent a connection is left intact and a new connection starts. After a few connections like these the server crashes with (java.lang.OutOfMemoryError: Java heap space) in the code connected to HPackHuffman decoding.

The same report adds the operator's nightmare — no completed request, so no log line:

> It seems that finding a reason why the server is crashing can be challenging for the server admin because even a single full HTTP request is not made (note that the last CONTINUATION frame doesn't have END_HEADERS flag) so they won't see HTTP requests in the logs. I'm not aware of any configuration params that can prevent this attack. Thus, it seems the only mitigation is turning off HTTP/2 support (or code fix).

DOS-2453322 (httpd, CVE-2024-27316) is the pre-413 buffering variant — the server buffers
*in order to* send the error:

> HTTP/2 incoming headers exceeding the limit are temporarily buffered in nghttp2 in order to generate an informative HTTP 413 response. If a client does not stop sending headers, this leads to memory exhaustion.

DOS-2453328 (Node, nghttp2) is the crash variant — CONTINUATION state + abrupt RST
triggers the `Http2Session` destructor assertion:

> Server crashes instantly after sending a few HTTP/2 frames.

## 3. The chunk-extension hole: timeouts that don't help

DOS-2375446 (Node, CVE-2024-22019) is the module's most quotable impact paragraph,
because it names the exact defenses it defeats:

> This is a major issue because it allows unbounded resource (CPU, network bandwidth) consumption of the standard Node.js http server. The standard methods which could help blocking a malicious requests like timeouts and limiting request body size do not seem to work.

The bug: an unprocessed HTTP request with an unbounded chunk extension is read
without bound. The hunting translation generalizes: *any* unparsed protocol element that
sits outside the timeout/max-body accounting is a flood surface, and the report must
demonstrate the timeout defeat empirically (DOS-2375446's is the corpus proof).

## 4. The Node slowloris rows: holding, not flooding

The four Node rows (799072, 868834, 800140, 1043360, 384839-family) are parameter
variations on one idea — never finish the request:

> Attackers can cause a Denial of Service by sending HTTP request body data extremely slowly to keep a connection open by maintaining activity, and use resources over an extended period.

> An attacker can open an arbitrary number of HTTP connections and keep the server busy by never completing the request phase.

DOS-799072's repro is 1 byte/sec against a 2-second server timeout — the timeout only
bounds *idle* gaps, and 1 byte/sec is never idle. DOS-868834 enumerates the only two
timeouts Node has (`server.timeout`, `server.headersTimeout`) and notes that body
parsing lives in application middleware the core never bounds. DOS-800140 (malformed
SETTINGS → `SIGABRT`) is the fuzz-found crash end of the same lane; DOS-1043360
(`unknownProtocol`) the negotiation end. All five are flat $250 in this corpus — the era
price for Node core DoS.

## 5. The unpaid rows are the CVEs

DOS-384839 (CVE-2018-1333) and DOS-1043360 carry `-` in this DB snapshot. Both are
advisory records for shipped fixes. The pattern from module 02 repeats: in the protocol
lane, `-` correlates with "already fixed, CVE exists" — the report is coordination
provenance, and the bounty sits with the vendor's channel. Price accordingly (i.e., file
protocol floods as CVE hunts with a disclosure record, not as per-row bounty hunts).

## 6. What pays, what doesn't

- **GOAWAY-avoidance is the priced skill.** The $4,860 report's core insight is staying
  under header limits while multiplying connections. Reports that show the frame math
  (8 CONTINUATION × 100 headers, just under the cap) convert; reports that just call
  `h2load` don't.
- **Pre-413 buffering is a distinct bug class.** DOS-2453322's flaw only exists because
  the server is *polite* (buffers to compose a 413). If your target returns 413 without
  buffering, you have no finding — demonstrate the buffering first.
- **Timeout-defeat must be shown, not asserted.** DOS-2375446's sentence is the template:
  name the standard method, show it doesn't work on this input.
- **Log invisibility is an impact multiplier.** DOS-2334401's "no full request, no log"
  observation is worth quoting in every HTTP/2 report — it explains why the incident
  lasted.
- **What doesn't pay:** connection-count floods against servers with per-IP caps and
  timeouts that *do* fire. The paid floods all bypass an accounting boundary (stream
  count, chunk walk, header cap); a generic SYN flood is out of scope for this class.

## 7. Cross-references

- Module 01's Tor pre-auth loop (DOS-113424) is the same "no time bound" root cause on a
  non-HTTP control channel; the fixes (loop cap vs header cap) are the two halves of
  protocol-bound discipline.
- Module 04's Rack Range-header rows (merge pool, DOS-2520679) are HTTP-layer floods
  filed under webapp abuse — cite them when a header-parsing CVE touches a web framework.
- Module 05's cache-poisoning pool is the *availability* mirror: protocol floods exhaust
  the origin; cache poisons exhaust the shared cache. Same impact, different victim,
  different vault (`Cache-Poisoning/` owns the meiosis).
