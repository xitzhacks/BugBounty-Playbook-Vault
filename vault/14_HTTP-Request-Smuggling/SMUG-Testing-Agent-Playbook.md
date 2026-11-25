---
title: "SMUG Testing Agent Playbook — HTTP request smuggling / CRLF executable protocol"
type: agent-playbook
category: smuggling-crlf
cwe: "CWE-444, CWE-113, CWE-74"
built: "2026-11-07"
corpus: "36 bucket rows (22 desync · 9 CRLF · 4 email · 1 adjacent) + 12 unclassified merges · all bodies read"
bounty: "$34,290 bucket corpus-floor (19 rows) · $41,190 incl. adjacent merges (23 rows) · max $5,000 (SMUG-1200647 Grafana SMTP→RCE)"
companion_modules: "01 request-smuggling-desync · 02 crlf-header-injection · 03 email-protocol-injection · 04 adjacent-negative-space"
quote_rule: "byte-true, (sic)-marked, from read bodies only; verified against archive/SMUG-bodies-full-dump.txt"
---

# SMUG — Testing Agent Playbook (HTTP Request Smuggling / CRLF Injection)

*Evidence base: 36 classified bucket rows + 12 unclassified merges (`SMUG-…`), max $5,000 (SMUG-1200647). Every cited sentence is byte-true to `references/archive/SMUG-bodies-full-dump.txt`. Read the class modules before improvising; this file is the operational spine.*

Crown-jewel doctrine up front: **payouts track what the flaw reaches, not how it
fires**. The corpus's ceiling is $4,660 for a Travis-sized Tomcat trailer parse
disagreement (module 01, CVE-2023-45648) and $5,000 for a newline in an SMTP
password that reaches a renderer shell (module 03) — while full request hijacks
executed on slackb.com and api.zomato.com sit at *no recorded figure*.

## P0 — Program classification & policy read (before any payload)

1. Program type decides the ledger: ibb upstream disclosures against
   `github.com/apache/tomcat`/`github.com/nodejs/node` paid flat per CVE variant
   ($1,800–$4,660); web-hunt desync proof paid $250–$750 for redirection
   evidence; Set-Cookie forgeries and display tricks paid nothing. Read the policy
   for *spraying desync payloads at live traffic* — several reports admit
   probabilistic victim poisoning.
2. Environment signal: inventory the front-end/back-end pair (proxy vendor +
   origin stack). Every paid class row is a *pair disagreement*, and the famous
   smuggler payload families (`space1`, `tabprefix1`, "150+ types") exist to
   find pairs that disagree.
3. Kill-gate: no testing yet — P0 produces the *diff-hunt envelope* (which pairs,
   which mutations, whose traffic) only.

## P1 — Surface inventory (parser pairs, header sinks, config writers)

1. **Framing headers on both sides** — every request path where both
   `Content-Length` and `Transfer-Encoding` can be present, plus nodes that pass
   `Transfer-Encoding` through (the `Transfer-Encoding : chunked` space-before-colon
   row, SMUG-737140) and llhttp-backed Node origins (space-before-CR/LF,
   `Content[CR]Length`, CR-alone delimiters).
2. **Header-value sinks** — anything the response compiler concatenates: OAuth
   `redirect_uri` (SMUG-2147132), session-path values (SMUG-237357), prospect-email
   paths (SMUG-858650), tweet/DM status (SMUG-712979), client-library
   `host`/`content-type` (undici), filenames echoed into responses (SMUG-1402249).
3. **Config/protocol writers** — managed-service config fields (SMTP passwords,
   `user_config` JSON), LDAP binds, mailer `RCPT TO`/`MAIL FROM` construction,
   iCalendar `ORGANIZER` pipelines, any `SOCK_STREAM` text-protocol client
   (urllib→Redis).
4. Out-list: single-server smuggling fantasies (no second parser, no differential)
   — not a finding in this class.

## P2 — Probe protocol (from cheapest differential to hardest)

Per candidate pair/sink, in era chronological order, with pricing attached:

1. **CL.TE/TE.CL baseline** — send the smuggler `space1`/`tabprefix1` probes
   against a suspected pair and watch for front-uses-CL/back-uses-TE. The corpus
   canonicals:
   SMUG-737140: "The `space1` payload places a space character in between `Transfer-Encoding` and the colon `:`. This is enough for the frontend to not understand the request as TE and instead as CE but not enough for the backend to process it in the same way."
   SMUG-771666: "I have custom tools to evaluate over 150 types of HTTP Smuggling Payloads." / "Sometimes you may just see DNS requests to your collaborator. Send the payload out as many times required to see an HTTP request." (probabilistic hit admission).
2. **Obfuscation-mutation sweep** — one mutation per probe class of module 01 §4:
   space-before-colon, tab-after-colon, leading space, dual/invalid TE, TE+`identity`,
   duplicate TE (TE-TE), substring TE (`AAAchunkedBBB`), CR-to-hyphen rename,
   chunk-extension newline, CR-alone delimiter, oversized trailer header vs.
   trailer-without-colon. SMUG-1238099 gives the byte-level discipline: "By following the ABNF of chunk extensions one can see that the only allowed bytes in this area are 0x09, 0x21-0x7e and 0x80-0xff. But `llhttp` allows any byte. This is the bug."
3. **Desync + victim race** — the weaponization shape of the two paid web rows:
   desync request followed by N `target.req` copies in Turbo Intruder. SMUG-726773: "The purpose of the following Turbo Intruder script is to send a desync request followed by 14 requests in quick succession to increase the chances of catching the desync-ed request such that it would not poison the request of another user who happens to be browsing the page."
   SMUG-867577 triples the class grammar: "An attacker can desynchronise frontend and backend servers, leaving the socket to the backend server poisoned with a harmful response."
4. **CRLF oracle / split check** — Set-Cookie forging (`%0a`/`%0d%0a` variants),
   fake-body splits (`%0d%0a%0d%0a`), `redirect_uri`/`Location` forgery. SMUG-858650: "The vulnerability allows setting arbitrary headers, and also enables response splitting which can then be exploited further."
5. **SMTP/protocol oracle** — when a mailer field looks suspect, use the
   non-blind transcript: inject `EHLO a` and read the banner the error string
   hands back (module 03). SMUG-1509216: "The errors in SMTP are returned in the response, thus making this a non-blind injection."
6. **Config-layer CRLF** — for API-driven service config, CRLF inside a field
   that opens a new INI/config section. SMUG-1200647: "SMTP server password configuration setting accepts new line characters." / "This can be used to set non-exported configuration variables. Using this CRLF-injection, the `rendering_args` of grafana image renderer can be modified which leads to code execution on the Grafana server."
7. **Version/patch fingerprint** — name the exact vulnerable range before
   writing anything: Tomcat `<11.0.0-M11/10.1.13/9.0.80/8.5.93` (CVE-2023-45648),
   Node 16.x/18.x/19.x undici host (CVE-2023-23936), ATS pairs. SMUG-2299692 again: "Apache Tomcat supports Trailer Section. However, we found that in version prior than 11.0.0-M11, 10.1.13, 9.0.80, 8.5.93, Apache Tomcat cannot properly parse the trailer section if there's no colon in the trailer header's line."

## P3 — Proof ladder (the modest demonstrations paid)

1. **Desync proof** — front-says-one / back-says-two in one response pair
   ("ATS will see one request to `/` and Node will see two requests, one to `/` and one to `/admin`"), plus a poisoned-victim redirect captured server-side at your Collaborator (the 67-reflection screenshot class, SMUG-726773).
2. **Hijack proof** — the smuggled request line swaps the target endpoint and
   the victim's material arrives at your pixel (SMUG-737140: "At this point you just attacked an arbitrary slack customer and have access to her `d` session cookie."; SMUG-771666: "Attacker can achieve victim session takeover in bulk and steal all information from the victim." — the claimed ceiling).
3. **CRLF proof** — header forgery shown in a decoded response (Set-Cookie on a
   302, `xxx: something` `location:`, `%0d%0a` fake body) and, where it lifts,
   the phrase from the doctrine: "Possible manipulation of user session / open redirect."
4. **Protocol proof** — full SMTP transcript or RESP payload with the injected
   command farm — SMUG-1054282's three published payloads (web shell, slave
   replication, SSH key) are the paid-free shape of this tier.
5. **Config-impact proof** — end-to-end: reverse shell or file write from the
   injected directive (SMUG-1200647 `nc -n -lvp 4444`).
6. **Honest-boundary statement** — where the desync cannot be read back
   (SMUG-1238099's ATS connection hang, SMUG-713285's high-traffic
   "hard to prove … without exploiting numerous genuine users") say so, and
   price it as send-only.

## P4 — Modern hardening fingerprints (never corpus doctrine)

- **Framing strictness**: proxies must reject whitespace between header name and
  colon (RFC 7230 §3.2.4) and CR-without-LF delimiters; llhttp grammar tightened
  per patch (module 01 §5 CVEs are the before-state).
- **Trailer handling**: trailer parsing that throws on over-limit headers
  instead of re-queuing the stream (CVE-2023-45648/2280391 sibling).
- **Header validation in code**: every `request.js`-style value pass must run
  the character regex, including the `host` assignment (undici host gap); PHP/Python/Node
  header writers must reject CR/LF in every escaping branch, not just `content-type`.
- **Filter ordering**: validate *after* trimming only; better, reject rather
  than strip.
- **Config-writer discipline**: service-config fields must not accept section
  delimiters (`[...]`) or embedded newlines; `rendering_args`-style shell-arg
  directives must not be writable through an SMTP form.
- **Mailer hygiene**: every envelope field (`RCPT TO`, `MAIL FROM`, `ORGANIZER`)
  must reject CR/LF before handing to the SMTP library; SMTP error propagation back
  to HTTP responses should be suppressed to keep the oracle dark.

## P5 — Pre-report gates (kill-gates)

1. **Differential gate** — you can name the two parsers and the exact bytes each
   counts differently. A single-server CRLF fantasy dies here (module 04's
   cart-quantity row is business logic, not smuggling).
2. **Direction gate** — state which request boundary moved (front vs back,
   CL vs TE, which TE mutation), and export a raw-byte PoC in hex or `nc`, not
   just a header-screenshot opinion.
3. **Impact gate** — show the *second* request landing somewhere observable
   (victim redirect, Collaborator hit, two-line access log, SMTP banner). Desync
   without a counted victim response is a $250 "potential", not a hijack.
4. **Prerequisite gate** — write the auth/env context down, especially
   admin-only fields (SMUG-1054282 "Privileges required: Admin" is the honest
   template) — admin wrappers turn a $0 finding into a $0 finding.
5. **Non-blind gate** — no speculative impact ladders ("session hijacking,
   cache poisoning, XSS" as a paragraph) without a captured artifact.
6. **Classifier-noise gate** — check the target class library (CodeQL detector
   tickets, Log Injection, CWE-117 look-alikes) against the module-04 negative
   space before filing.

## Module ↔ phase table

| Phase | Corpus evidence (modules) | Anatomy of the paid pattern |
|---|---|---|
| P1 inventories parser pairs | 01 (§1, §4), 02 (§1) | `Content-Length` + mutated TE; desync/trailer pairs |
| P2 probes mutations & oracle | 01 (§3-§5), 02 (§2-§3), 03 (§3-§5) | `space1`/`tabprefix1` → SMTP `EHLO` oracle |
| P3 proofs ladder, honest boundaries | 01 (§2-§3), 03 (§2) | access-log pair; Collaborator hit; reverse shell |
| P4 hardening fingerprints | 01 (§5), 02 (§3), 03 (§6) | RFC reject rules; host-regex; filter ordering |
| P5 kill-gates | 04 (§3-§6) | theory/detector/no-class rows; advisory Apache pairs |

## Non-goals

- Cache-poisoning *weaponization* depth: this vault proves desync→cache poisoning
  as an endpoint (`X-Forwarded-Host` poisoning, SMUG-919175); the Cache-Poisoning
  vault (master row 15) owns the poisoning taxonomy.
- Smuggler-scanner payload catalogues beyond what module 01's bodies evidence:
  we cite the scanners' names (`space1`, `tabprefix1`, "150+ types") as
  artifacts, not as a re-derived library.
- Response-splitting *into XSS* or stored-CRLF filename chaining beyond what
  SMUG-1402249 and the HTTP/2 pseudo-header row evidence — kept as cross-cites,
  not doctrine.
