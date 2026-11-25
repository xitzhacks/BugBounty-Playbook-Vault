---
title: "Webapp resource abuse — unbounded inputs, parser exhaustion, and single-request CPU burns"
type: playbook
category: webapp-resource-abuse
cwe: "CWE-400 (with CWE-770/789/835 siblings)"
source_count: 100
full_bodies_available: 100
corpus: "h1-brain disclosed_reports.db (3,673 rows; sha256 8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4) · bucket 'dos' = 221 rows, weakness 'Uncontrolled Resource Consumption'"
list_accessed: "2026-11-07"
note: "Anchor bodies: DOS-1543718 ($7,640), DOS-2105808 ($5,000), DOS-363636 ($4,000), DOS-470067 ($3,000), DOS-2258758 ($2,540). All 100 bodies read; quotes byte-true to references/archive/DOS-bodies-full-dump.txt."
---

# Webapp resource abuse — the endpoint that does unbounded work on one request

## 1. Overview

One hundred rows, **$51,219/47 paid** — the vault's volume module and its best
hunting textbook: not one mechanism but the full taxonomy of "the server does more work
than the request should cost." The anchors span the space: GitLab's issue-preview CPU
burn (1543718, **$7,640**, the vault's top webapp figure), an RSKJ single-packet wedge
(2105808, $5,000), a PeerExplorer connection leak (363636, $4,000), a Mermaid client
freeze (470067, $3,000), and Django's UsernameField unicode burn (2258758, $2,540).
Around them: the Mermaid-bypass sequel (670572), the comment-length bomb (557154), the
multipart FD exhaustion (1904097, $2,400), RSK smart-contract precompile burns
(2412583/2489843/2559404), a long tail of cookie bombs, browser crashes and One-click
DoSes, and the Rack/Django parser-CVE family the other modules split by engine. DOS-1543718's
summary — the module's thesis — is a single sentence:

> Previewing an issue with a specially-crafted description results in high CPU usage for 60 seconds (request timeout).

**Case-stock (100 rows / $51,219):**

| Case | Target | Mechanism | Bounty |
|---|---|---|---|
| [DOS-1543718](https://hackerone.com/reports/1543718) | gitlab | issue-preview '![l' repeat burns 60s CPU | $7,640 |
| [DOS-2105808](https://hackerone.com/reports/2105808) | rootstocklabs | single UDP packet wedges RSKJ forever | $5,000 |
| [DOS-363636](https://hackerone.com/reports/363636) | rootstocklabs | PeerExplorer ping/pong connection leak | $4,000 |
| [DOS-470067](https://hackerone.com/reports/470067) | gitlab | Mermaid diagram freezes Issue page | $3,000 |
| [DOS-2258758](https://hackerone.com/reports/2258758) | ibb | 1M unicode chars in UsernameField → 4.4s/request | $2,540 |
| [DOS-1746098](https://hackerone.com/reports/1746098) | ibb | locale param treated as regex → DoS | $2,400 |
| [DOS-1904097](https://hackerone.com/reports/1904097) | ibb | unlimited multipart parts → FD/memory exhaustion | $2,400 |
| [DOS-1543584](https://hackerone.com/reports/1543584) | gitlab | move_issue with crafted description burns 60s CPU | $2,300 |
| [DOS-2591681](https://hackerone.com/reports/2591681) | ibb | strip_punctuation brace bomb (CVE-2024-38875) | $2,142 |
| [DOS-2644244](https://hackerone.com/reports/2644244) | ibb | floatformat 'e' exponent blowup (CVE-2024-41989) | $2,142 |
| [DOS-1077136](https://hackerone.com/reports/1077136) | slack | html injection overrides document functions → crash | $1,500 |
| [DOS-1695472](https://hackerone.com/reports/1695472) | hyperledger | 500 parallel read requests block validators | $1,500 |
| [DOS-500686](https://hackerone.com/reports/500686) | x | unloadable twitter-mobile URL | $1,120 |
| [DOS-903740](https://hackerone.com/reports/903740) | x | twitter.com + mobile DoS | $1,120 |
| [DOS-288993](https://hackerone.com/reports/288993) | ibb | SSL_peek hang on empty record (CVE-2016-6305) | $1,000 |
| [DOS-557154](https://hackerone.com/reports/557154) | gitlab | unlimited comment length → server+client DoS | $1,000 |
| [DOS-867699](https://hackerone.com/reports/867699) | kubernetes | writing /etc/hosts fills node disk | $1,000 |
| [DOS-1018037](https://hackerone.com/reports/1018037) | basecamp | very long hey.com name locks contacts | $1,000 |
| [DOS-583819](https://hackerone.com/reports/583819) | x | cookie injection DoS on periscope.tv | $560 |
| [DOS-767458](https://hackerone.com/reports/767458) | x | missing input validation → DoS | $560 |
| [DOS-768677](https://hackerone.com/reports/768677) | x | missing input validation → DoS | $560 |
| [DOS-784676](https://hackerone.com/reports/784676) | x | crafted DM reactions crash iOS app | $560 |
| [DOS-921286](https://hackerone.com/reports/921286) | x | Chrome DoS | $560 |
| [DOS-3002543](https://hackerone.com/reports/3002543) | ibb | REXML DoS (CVE-2024-43398) | $505 |
| [DOS-506412](https://hackerone.com/reports/506412) | hyperledger | empty CA response crashes node | $500 |
| [DOS-1954937](https://hackerone.com/reports/1954937) | ibb | Multipart MIME parsing DoS (rack) | $480 |
| [DOS-2012121](https://hackerone.com/reports/2012121) | ibb | Range header parsing DoS (CVE-2022-44570) | $480 |
| [DOS-2012122](https://hackerone.com/reports/2012122) | ibb | Content-Disposition parsing DoS (CVE-2022-44571) | $480 |
| [DOS-2012125](https://hackerone.com/reports/2012125) | ibb | RFC2183 boundary parsing DoS (CVE-2022-44572) | $480 |
| [DOS-507525](https://hackerone.com/reports/507525) | chaturbate | camo.stream DoS | $400 |
| [DOS-2818147](https://hackerone.com/reports/2818147) | sorare | insufficient input verification → resource use | $300 |
| [DOS-903521](https://hackerone.com/reports/903521) | nodejs-ecosystem | Fastify allErrors:true ajv DoS (default config) | $250 |
| [DOS-1033107](https://hackerone.com/reports/1033107) | nodejs | DNS max-responses DoS | $250 |
| [DOS-1688199](https://hackerone.com/reports/1688199) | nextcloud | sharee-recommendations DB exhaustion | $250 |
| [DOS-418254](https://hackerone.com/reports/418254) | chaturbate | unrestricted POST size on roomlogin | $200 |
| [DOS-970760](https://hackerone.com/reports/970760) | cs_money | pixel-flood app-level DoS | $200 |
| [DOS-1243724](https://hackerone.com/reports/1243724) | mattermost | large console messages DoS | $150 |
| [DOS-1253732](https://hackerone.com/reports/1253732) | mattermost | crafted message crashes viewers' webapp | $150 |
| [DOS-1620170](https://hackerone.com/reports/1620170) | mattermost | GIF upload OOM via API | $150 |
| [DOS-163307](https://hackerone.com/reports/163307) | instacart | WordPress auth DoS | $100 |
| [DOS-1176794](https://hackerone.com/reports/1176794) | fetlife | payload makes posts unavailable | $100 |
| [DOS-861521](https://hackerone.com/reports/861521) | clario | cookie injection → domain-wide DoS | $50 |
| [DOS-1147449](https://hackerone.com/reports/1147449) | sifchain | xmlrpc.php/wp-json user-enum + DoS | $50 |
| [DOS-94642](https://hackerone.com/reports/94642) | whisper | SMS invite form abuse | $30 |
| [DOS-181558](https://hackerone.com/reports/181558) | brave | Brave code-snippet DoS | $25 |
| [DOS-181686](https://hackerone.com/reports/181686) | brave | Brave hangs loading snippet | $25 |
| [DOS-128856](https://hackerone.com/reports/128856) | gratipay | async email send abuse | $10 |
| [DOS-57356](https://hackerone.com/reports/57356) | x | DOM cookie bomb | - |
| [DOS-125587](https://hackerone.com/reports/125587) | security | hogging all resources on hackerone.com | - |
| [DOS-176066](https://hackerone.com/reports/176066) | brave | Brave browser DoS | - |
| [DOS-176197](https://hackerone.com/reports/176197) | brave | Brave window-object DoS | - |
| [DOS-201346](https://hackerone.com/reports/201346) | ibb | bad (EC)DHE params crash client (CVE-2017-3730) | - |
| [DOS-210779](https://hackerone.com/reports/210779) | x | invalidating OAuth token breaks TweetDeck | - |
| [DOS-216840](https://hackerone.com/reports/216840) | ibb | OCSP extension unbounded memory (CVE-2016-6304) | - |
| [DOS-221787](https://hackerone.com/reports/221787) | ibb | malformed SHA512 ticket DoS (CVE-2016-6302) | - |
| [DOS-221791](https://hackerone.com/reports/221791) | ibb | tls_get_message_header over-allocation (CVE-2016-6307) | - |
| [DOS-221792](https://hackerone.com/reports/221792) | ibb | dtls fragment over-allocation (CVE-2016-6308) | - |
| [DOS-303632](https://hackerone.com/reports/303632) | nodejs-ecosystem | Fastify large-JSON DoS | - |
| [DOS-324021](https://hackerone.com/reports/324021) | rootstocklabs | debug JSON-RPC methods expose DoS | - |
| [DOS-357665](https://hackerone.com/reports/357665) | brave | Brave iOS DoS | - |
| [DOS-364964](https://hackerone.com/reports/364964) | ibb | large DH param client DoS (CVE-2018-0732) | - |
| [DOS-406614](https://hackerone.com/reports/406614) | ui | Edgemax resource-consumption DoS | - |
| [DOS-504759](https://hackerone.com/reports/504759) | nextcloud | large avatar images burn CPU | - |
| [DOS-505278](https://hackerone.com/reports/505278) | ibb | stream-filter DoS | - |
| [DOS-549040](https://hackerone.com/reports/549040) | gitlab | GitLab math-render client exhaustion | - |
| [DOS-670572](https://hackerone.com/reports/670572) | gitlab | Mermaid 5000-char limit bypass via 100 blocks | - |
| [DOS-679907](https://hackerone.com/reports/679907) | roblox | FireServer malformed string freezes servers | - |
| [DOS-702987](https://hackerone.com/reports/702987) | gitlab | missing redirect_uri crashes OAuth authorize | - |
| [DOS-713407](https://hackerone.com/reports/713407) | security | whitespace filename exception DoS | - |
| [DOS-752073](https://hackerone.com/reports/752073) | nordsecurity | xmlrpc.php bruteforce/DoS surface | - |
| [DOS-764434](https://hackerone.com/reports/764434) | security | huge profile-pic name DoS | - |
| [DOS-774896](https://hackerone.com/reports/774896) | kubernetes | kubelet metric-cardinality exhaustion | - |
| [DOS-777984](https://hackerone.com/reports/777984) | nordsecurity | cookie-bomb DoS | - |
| [DOS-812754](https://hackerone.com/reports/812754) | nextcloud | password-reset request DoS | - |
| [DOS-819088](https://hackerone.com/reports/819088) | x | char-limit bypass → Twitter-app 500s | - |
| [DOS-833856](https://hackerone.com/reports/833856) | kubernetes | GCSArtifact.RealAll DoS | - |
| [DOS-858603](https://hackerone.com/reports/858603) | acronis | log-file DoS in anti-ransomware service | - |
| [DOS-861170](https://hackerone.com/reports/861170) | security | crafted request from old account DoS | - |
| [DOS-882923](https://hackerone.com/reports/882923) | kubernetes | client-go jsonpath DoS | - |
| [DOS-905015](https://hackerone.com/reports/905015) | ibb | long filenames OOM, temp files leak | - |
| [DOS-975827](https://hackerone.com/reports/975827) | automattic | one-click permanent DoS | - |
| [DOS-1005421](https://hackerone.com/reports/1005421) | automattic | tumblr API cookie-manipulation DoS | - |
| [DOS-1041173](https://hackerone.com/reports/1041173) | automattic | invite permanently DoSs happy.tools | - |
| [DOS-1237428](https://hackerone.com/reports/1237428) | reddit | long shoutout string → 500s | - |
| [DOS-1341957](https://hackerone.com/reports/1341957) | reddit | hash-collision DoS in Markdown parser | - |
| [DOS-1514863](https://hackerone.com/reports/1514863) | ibb | uninitialized value in lua req_parsebody | - |
| [DOS-1596252](https://hackerone.com/reports/1596252) | ibb | lua_read_body DoS | - |
| [DOS-1606039](https://hackerone.com/reports/1606039) | ibb | CERTINFO never-ending busy-loop | - |
| [DOS-1635854](https://hackerone.com/reports/1635854) | hyperledger | Hyperledger Fabric remote DoS | - |
| [DOS-1680241](https://hackerone.com/reports/1680241) | mattermost | automatic-response-message DoS | - |
| [DOS-1685979](https://hackerone.com/reports/1685979) | mattermost | Playbook DoS | - |
| [DOS-2058337](https://hackerone.com/reports/2058337) | nextcloud | long calendar-invite emails hang server | - |
| [DOS-2412583](https://hackerone.com/reports/2412583) | rootstocklabs | modexp precompile bug: 8-min smart contract | - |
| [DOS-2446433](https://hackerone.com/reports/2446433) | ibb | header parsing DoS (CVE-2024-26146) | - |
| [DOS-2446437](https://hackerone.com/reports/2446437) | ibb | Content-Type parsing DoS (CVE-2024-25126) | - |
| [DOS-2489843](https://hackerone.com/reports/2489843) | rootstocklabs | inefficient CODESIZE: 1.5-min contract | - |
| [DOS-2559404](https://hackerone.com/reports/2559404) | rootstocklabs | huge error string: ~23s contract | - |
| [DOS-2987782](https://hackerone.com/reports/2987782) | ibb | net/imap memory-exhaustion DoS | - |
| [DOS-3013913](https://hackerone.com/reports/3013913) | ibb | CGI::Cookie.parse DoS (CVE-2025-27219) | - |
| [DOS-3058919](https://hackerone.com/reports/3058919) | discourse | large Markdown reply payload exhausts resources | - |
## 2. The single-request CPU burn: preview, move, comment

DOS-1543718's payload is a 349,525-repetition image-macro string (`'![l' * int(1048576/3 - 1)`)
against the markdown preview path; the server burns a full CPU for the 60-second request
timeout, and parallel previews burn parallel cores:

> Previewing an issue with a specially-crafted description results in high CPU usage for 60 seconds (request timeout).

> Multiple requests can be issued in parallel to create a larger impact.

DOS-1543584 (`move_issue`, $2,300) is the same bug through a different endpoint — the
preview endpoint is not special; the *markdown renderer* is. DOS-557154 ($1,000) is the
unbounded-comment variant, hitting both sides at once:

> There is no limit to the number of characters in the issue comments, which allows a DoS attack. The DoS attack affects both server-side and client-side.

The hunting shape is consistent: **one authenticated request, textbook input, 60-second
burn**. The report's job is the parallel multiplier (N previews → N cores) and the
"entire server unavailable" DockerHub demonstration — method (a) time it, (b) parallelize
it, (c) show the fleet effect.

## 3. The wedge: one packet, forever

DOS-2105808 ($5,000) is the module's purest "one request" finding — a single UDP packet
that RSKJ's `UDPServer` processes *only*, forever, so no other node's packets are ever
read:

> 4.the `UDPServer` is going to process *only* one UDP packet forever and it prevents to process other packages received from different nodes. In a while (some minutes left) the application crashes.

(The leading `4.` and missing space are the body's — kept byte-true.) DOS-363636 ($4,000)
is the connection-management sibling: `PeerExplorer` ping/pong mishandling leaks
established connections until the node cannot accept peers. Both pay because the victim
is *shared infrastructure* (a validator / P2P node), not a single user session — the
blast-radius rule from module 01, in webapp dress.

## 4. The client freeze: Mermaid and the browser that never draws

DOS-470067 ($3,000) inverts the direction — the DoS is the *reader's* browser, not the
server:

> An attacker could exploit Mermaid available in Markdown and cause DoS.

The payload is pasted into an Issue comment; every subsequent viewer of the Issue page
freezes. DOS-670572 then bypasses the 5,000-character Mermaid mitigation by splitting the
payload across 100 code blocks — the corpus's cleanest "fix was a length cap, the cap
was per-block" lesson. The browser-lane rows around them (Brave 176066/176197/357665,
Chrome 921286, Twitter 903740/819088, X 57356/777984/1005421) are the same impact with
lower tiers: the victim is a client, the fix is a renderer cap, the price is smaller.

## 5. The parser family: Django, Rack, and the 2024 CVE wave

The middle of the table is a coordinated-disclosure family: Django multipart FD/memory
exhaustion (1904097, $2,400), locale-as-regex (1746098, $2,400), UsernameField unicode
(2258758, $2,540), `strip_punctuation` brace bombs (2591681, $2,142), `floatformat`
exponent blowup (2644244, $2,142), and the Rack trio (2012121/2012122/2012125, $480
each) plus REXML (3002543, $505) and CGI::Cookie (3013913, `-`). Two quotations carry
the method:

> In Django versions before 4.2.7, 4.1.13, and 3.2.23, I sent a POST request to the admin login page using Burp Suite, editing the request to send over 1 million invalid unicode characters to my local  web server running Django. (I used: "¾")

> After submitting, a single request took 4.4 seconds on average.

and the multipart root cause, stated in one sentence:

> In Django 3.2.x before 3.2.18, 4.0.x before 4.0.10 and 4.1.x before 4.1.7, the multipart request parser was subject to a Denial of Service attack. The multipart request parser processes the request body on endpoints with a form and any other POST endpoints as well. The parser was processing an unlimited number of empty/file multipart-parts. For each file part a new temporary file was opened and kept open for the entire duration of the request. The parsing and tracking of an unbound number of parts/files can lead to too many files being open and memory exhaustion.

Note the doubled space in "my local  web server" — the body's, preserved. The
UsernameField arithmetic (4.4 s × 20 concurrent → 60 s waits + 504s) is the module's
template for single-request → fleet conversion.

## 6. What pays, what doesn't

- **One request, shared victim, measured burn.** Every top figure (1543718, 2105808,
  363636, 2258758) is a *single* request with a *timed* effect and a *parallel* multiplier.
  The 60-second timeout is not a mitigation story — it is the measured payload duration.
- **Client-side freezes pay less than server-side burns.** Mermaid-on-the-reader ($3,000)
  vs preview-on-the-server ($7,640): same renderer, different victim. Prefer the
  server-side variant in your report; note the client variant as breadth.
- **Cap-bypasses are their own findings.** DOS-670572's 100-block split of a capped
  payload is a second report on the same bug. When a fix is a length limit, test the
  limit's *scope* (per-block? per-field? per-request?).
- **Cookie bombs and char-limit bypasses are the floor, not the ceiling.** The X/Twitter
  ($560 each) and browser ($25–$100) rows prove the class pays even for one-click
  client DoSes — but the per-report value collapses fast. File them; don't build a
  campaign around them.
- **What doesn't pay:** "I sent many requests and the site was slow." Every paid row
  here names the *unbounded* input (comment length, multipart parts, unicode count) and
  the *missing cap*. Unboundedness, not volume, is the finding.

## 7. Cross-references

- Module 02 owns the regex-engine variants of the parser family (1518036, 1929567);
  this module owns the endpoint variants (1746098, 2258758, 1954937). A Django locale
  report is both — cite the module by the engine your PoC stresses.
- Module 03's CONTINUATION floods are the protocol-layer version of this module's
  "unbounded input" — header bytes here, HTTP/2 frames there. Same hunt, different
  layer of the stack.
- Module 05's merge pool holds the Rack sequel CVEs (2520679, 2071556, 1627159) and the
  CVE-2018-6389 amplification pair (752010, 753491) — the bucket filter's misses, same
  class. Module 05 §4 quotes them.
- The `Business-Logic/` boundary: "unlimited comment length" is resource abuse here;
  "unlimited invite/mint" is business-logic there. The test is whether the harm is
  *work* (CPU/memory/FDs) or *state* (credits/memberships).
