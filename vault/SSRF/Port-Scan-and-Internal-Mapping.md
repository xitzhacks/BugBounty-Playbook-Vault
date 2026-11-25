---
title: "Port Scanning & Internal Network Mapping over SSRF"
type: playbook
category: port-scan-oracle
cwe: "CWE-918"
source_count: 12
full_bodies_available: 12
corpus: "HackerOne disclosed reports, 2013–2017 era, h1.security.nathan.sx archive"
archive_accessed: "2026-10-24"
note: "Every claim traces to bodies read in full this session. Bounty figures are those recorded on the reports."
---

# Port Scanning & Internal Network Mapping over SSRF

## 1. Overview

The archive's single largest SSRF cluster is not "read internal data" but **measure
the inside of the network** — with the server doing the measuring, through a URL
parameter that the target validates only loosely (or straight-through). Twelve
confirmed cases show that the era's port-scan reports were carried by *differencing
oracles*: a response or behaviour difference between "port answers" and "port does
not answer".

The lesson the cluster teaches is procedural, and it is the same in every case:
first calibrate the oracle on a known-open and a known-closed port, then run it on
the internal set. The channel differs per report — status code, error string,
cURL error code, response time, response headers, or a service banner leaking into
an error message — but the calibration step is universal.

Channels found in the corpus, by provenance:

| Channel | Cases | First provenance |
| --- | --- | --- |
| Error-string / status-code differs per connect outcome | SRF-16571, SRF-145524, SRF-67389, SRF-178184, SRF-213358 | case rows below |
| cURL error code (56 / 7 / 28 differencing) | SRF-50537 | server-side curl, macro upload |
| Response-content oracle (page fetched vs not, metatag count) | SRF-178184, SRF-49474 | validator/'console' endpoints |
| Timing (HTTP RTT) | SRF-67377 | admin image-from-URL |
| Same-subnet vs not-exists hint | SRF-222667 | SMTP settings tester |
| Banner-in-error (SSH banner consumed as an HTTP status line) | SRF-158016 | image-by-URL importer |
| Full content return (read internal pages, not just ports) | SRF-1409 | URL proxy |
| Internal proxy/scan through browser-relayed CSRF | SRF-110801 | Press This scanner |

**Era lexicon note.** The era's own name for much of this category was **XSPA**
("cross-site port attacks") — titles in the corpus still carry it (`SRF-77817`:
"SSRF/XSPA в форме загрузки видео по URL"; `SRF-49474`'s era grouping). The taxonomy
this file's channel table descends from was published by Riyaz Walikar in 2012 and
recovered for the vault from the Wayback Machine — see
[BLOG-003](references/blogs-index.md) in the bibliography: five XSPA attack classes,
and the same calibration-then-difference doctrine ("unique error messages, response
byte size and response timing can be used to identify port status").

## 2. Case evidence

### SRF-16571 — SSRF (Portscan) via Register Function (Custom Server) · RelateIQ — **$250** (archive-stated)

- Link: <https://hackerone.com/reports/16571>
- Weakness label as recorded (historical): "Violation of Secure Design Principles"
- Quote (the sink — note it hides inside a *registration* feature):
  > the custom server option during registration allows performing portscans (or "Server Side Request Forgery") from "relateiq" systems to external (and potential internal systems).
- The request is a GWT-RPC call calling `validateOffice365Account` with the server
  string `https://127.0.0.1:1` — and the payload is the connect outcome:
  > The URL "https://127.0.0.1:1" can be changed to a different IP/DNS and TCP Port. Based on the response received it is possible to identify if a port is open, or closed/filtered.
- Quote (calibration, verbatim):
  > An open port results into a HTTP Status of 504 (Gateway Timeout), or an error message of "The underlying connection was closed: An unexpected error occurred on a send" in the HTTP response.
  > A closed port usually results into a message of "Unable to connect to the remote server".
- Result (localhost, nmap top-50 equivalent):
  > For localhost on the top50 (nmap) ports the following were found open:
  > - 80
  > - 135
  > - 445
  > - 3389
  > - 49152
  > - 49154

### SRF-49474 — Cross site Port Scanning bug in twitter developers console · Twitter — no bounty recorded

- Link: <https://hackerone.com/reports/49474>
- Weakness label as recorded (historical): "Cryptographic Issues - Generic" — era
  label noise again; the body is a proxy-scan through the developer console.
- Quote (the impact phrasing that defines "proxy scan"):
  > This vulnerability allow a port scanning a remote machine on internet . an attacker can scan a remote machine through this vulnerability using twitter ip as a proxy . *(sic)*
- The oracle is textual and explicit in the console; the report's ports
  (80 open / 8080 closed / 2082 cPanel password-protected / 809) show the
  **three-outcome** value of banner capture: open-HTTP, closed, and
  open-but-authenticated each produce a distinguishable result.

### SRF-50537 — Server Side Request Forgery in macro creation · Phabricator — no bounty recorded

- Link: <https://hackerone.com/reports/50537>
- Weakness label as recorded: "Information Disclosure". Upstream, the Phabricator
  ticket for the same sink (`T6755`) was closed "Won't fix" — but that detail is
  only known through SRF-53088's citation, marked as such here.
- Quote (the mechanism — error transcription differentials):
  > Entering in different styles of URL can lead to CURL errors returning data that provides information to the attacker with suitable knowledge. *(sic — "Entering in")*
- The report's calibration set, verbatim from the body (ellipses shorten the cURL
  boilerplate only):
  > http://localhost:22/ → `Could not fetch URL: [cURL/56] (http://localhost:22/) <CURLE_RECV_ERROR> ...`
  > This error suggests that there is a port open on port 22 on the server machine (ie, ssh server running)
  > http://localhost:21/ → `Could not fetch URL: [cURL/7] (http://localhost:21/) <CURLE_COULDNT_CONNECT> ...`
  > This error suggests that ther is NOT a port open on port 21 on the server machine (ie, no ftp server) *(sic — "ther")*
  > http://google.com:22/ → `Could not fetch URL: [cURL/28] ... <CURLE_OPERATION_TIMEDOUT> This request took too long to complete.`
  > This error also suggests a closed port
  > http://localhost/ → `Could not fetch URL: [HTTP/500] Internal Server Error <!DOCTYPE html> ...`
  > This shows an open port, serving up HTTP responses, in this case, a 500 error (accessing phabricator by a different domain name)
  > http://google.com/ → no cURL error, but `You must upload an image.`
  > Suggests open port serving HTTP responses, 200 most likely
- The redirect and DNS vectors, verbatim:
  > http://davenport.net.nz/test.php
  > This HTTP 302 redirect to http://localhost/, and gives the same result
  > http://testing.allthethings.co.nz/
  > Same, but via DNS
  > http://testing6.allthethings.co.nz/
  > Same, but via DNS (and IPv6 localhost)
- Quote (the author's vector summary):
  > Note that you can also get internal addresses, either via HTTP redirect, DNS entry, or direct IP.
- Quote (the remediation list, era terminology preserved):
  > - Disallow localhost, and any RFC1914 ip's (private LAN) *(sic — RFC 1918 is the private-range RFC; author wrote 1914)*
  > - Disallow unusual ports
  > - Rate limit requests
  > - Don't follow redirects to localhost and/or local LAN IP's, either via HTTP redirects, or DNS records.
- Quote (one line in the closing): "I found that non HTML files returned would be saved, and perhaps viewed" — non-HTML responses (e.g. CSS/JS) materialise in the product, which gives the case its read-back.

### SRF-178184 — SSRF in https://cards-dev.twitter.com/validator · Twitter — **$280** (archive-stated)

- Link: <https://hackerone.com/reports/178184>
- Weakness label as recorded: "Server-Side Request Forgery (SSRF)" — the label is
  correct taxonomy this time.
- Quote (regression — a same-vulnerability-after-fix story, quote verbatim):
  > After my previous report (2 years ago)  https://hackerone.com/reports/30860 you fixed the vulnerability, but now it looks like this fix was reverted and the same problem exists again. *(sic — double space)*
- The calibration transcript is the corpus's cleanest triple-band oracle against
  `0.0.0.0`; verbatim, with the report's own arrows and spellings:
  > 1. Closed port on localhost
  > http://0.0.0.0:123 -&gt; ERROR: Fetching the page failed because other errors.
  > 2. Open port but not HTPP *(sic)*
  > http://0.0.0.0:22 -&gt; ERROR: Failed to fetch page due to: ChannelClosed
  > 3. Open HTPP port *(sic)*
  > http://0.0.0.0:4680
  > -&gt;
  > INFO:  Page fetched successfully
  > INFO:  2 metatags were found
  > WARN:  Not whitelisted
  A fourth band exists in the transcript: "Existing folder" prints "2 metatags were
  found" while "5. None existis folder" *(sic)* ends "WARN:  No metatags found" — so
  the oracle resolves paths on the host too.
- Quote (windup impact):
  > Disaster scenario:
  > Find open HTTP service running on local infrastructure with ability to execute commands.
  > For example:
  > http://0.0.0.0:4680/system/command.php?command=[ROOT_COMMAND]

### SRF-145524 — Server side request forgery (SSRF) on nextcloud implementation. · Nextcloud — no bounty recorded

- Link: <https://hackerone.com/reports/145524>
- Sink: federation "trusted server" — admin adds a peer with `url=http://...`
- Quote (the side-channel oracle in decoded form — the same wording appears in the report):
  > {"message":"Client error response [url] http:\/\/127.0.0.1\/status.php [status code] 404 [reason phrase] Not Found"}
  > This indicates that port **80** of the localhost is open.
- And the closed-band counterpart:
  > {"message":"cURL error 7: Failed to connect to 127.0.0.1 port 8080: Connection refused"}
  > We received an error because the PORT 8080 of localhost was blocked.
- The lesson: the product tried to be helpful with libcurl error text and both bands
  are readable in-band *without any attacker infrastructure at all*.

### SRF-213358 — SSRF at apps.nextcloud.com/developer/apps/releases/new · Nextcloud — no bounty recorded

- Link: <https://hackerone.com/reports/213358>
- Sink: the app-store release form's "Download Link area".
- Quote (calibration, per the author's own gloss):
  > Enter https://127.0.0.1:22 (SSH) or https://127.0.0.1:80 (HTTP) (Download Link area)
  > You will get this error &lt;screenshot&gt; means the 22 port is opened, the same with 80
- "`but if you entered https://127.0.0.1:21 (Telnet) you will get this error … means the 21 port isn't opened`" — note the author's scheme/project slip ("Telnet" over
  `https://`; the transcript shows only the port mattering in-band).

### SRF-222667 — Possible SSRF in email server settings(SMTP mode) · Nextcloud — no bounty recorded

- Link: <https://hackerone.com/reports/222667>
- Sink: admin SMTP `server address` field; the validation itself leaks the answer.
- Quote (the four bands, verbatim — screenshot-file references left as in the source):
  > 2.Set server address to "172.17.1.0`,then you will get screenshot(nextcloud1.png),it means not on the same network segment
  > 3.Set server address to "172.17.0.0`,then you will get screenshot(nextcloud2.png),it means the address not exists or doesn't open any port to access
  > 4.Set server address to "172.17.0.1` and port to empty,then the test email will send successfully! it means this host exists and opens a smtp port
  > 5.Set server address to "172.17.0.1` and port to `22`,then you will get screenshot(nextcloud3.png),it means the address exists,but can not access to the port *(sic — spacing)*
- Distinctive: a *detection of the neighbour's network state* (the "not on the same
  network segment" wording) — i.e. the mismatch between tested host and the probe
  origin's subnet is itself disclosed. That band is unique in this corpus; the agent
  playbooks elsewhere treat it as unknown.

### SRF-67377 — SSRF via 'Add Image from URL' feature · Shopify — **$500** (archive-stated)

- Link: <https://hackerone.com/reports/67377>
- Weakness label as recorded: "Violation of Secure Design Principles"
- Quote (the redirect trap):
  > Despite that URLs are validated it is possible to use a redirect trick to force to connect to any port.
- Quote (timing channel explicitly named):
  > Then using HTTP RTT it is possible to know arbitrary port's status. *(sic — "arbitrary port's")*
- The technique is time-based differencing, so the report is honest about needing a
  network dump: "The network dump is in attachment."
- Case context: the same reporter continued in SRF-67389 (below) and moved the
  technique to a JSON admin endpoint.

### SRF-67389 — SSRF via 'Insert Image' feature of Products/Collections/Frontpage · Shopify — **$500** (archive-stated)

- Link: <https://hackerone.com/reports/67389>
- Weakness label as recorded: "Violation of Secure Design Principles"
- Quote (the exact scheme/port filter observed, and its outcome code):
  > If `src` uses schemes that are not `http` or `https`, or the  another `port` then server responds with `HTTP/1.1 422 Unprocessable Entity`. *(sic — "the  another")*
- Quote (the differencing oracle, complete):
  > If the server returns `HTTP/1.1 500 Internal Server Error` then the port is opened and if the server returns `HTTP/1.1 422 Unprocessable Entity` then the port is closed.
- Worked example in the open (calibration on a public pest, exactly as a real hunt
  would do first):
  > Example of scanning ports for scanme.nmap.org host (TCP ports 1 - is closed, TCP port 22 - is opened):
  > `src=http%3A%2F%2Fhettoteam.tk/r.php?r=http://scanme.nmap.org:1`: HTTP code is 422.
  > `src=http%3A%2F%2Fhettoteam.tk/r.php?r=http://scanme.nmap.org:22`: HTTP code is 500

### SRF-158016 — Server side request forgery on image upload for lists · Instacart — **$50**

- Link: <https://hackerone.com/reports/158016>
- Weakness label as recorded (historical): "Code Injection" — era label noise.
- Quote (the banner oracle — the same error message that the reporter had:
  SSH-vs-HTTP banner becomes an HTTP 'wrong status line'):
  > http://127.0.0.1:21 and you will get as response:
  > ```
  > {json}
  > {
  > 	"meta":
  > 	{
  > 		"code": 400,
  > 		...
  > 		"errors": ["Image could not download file: wrong status line: "SSH-2.0-OpenSSH_6.6.1p1 Ubuntu-2ubuntu2.3""]
  > 	}
  > }
  > ```
  > Which shows that it tried to connect to the SSH port on localhost.
- Small but instructive impact: the same error channel proves service
  identification, not just open/close — an SSH daemon *banner* flows into
  the response body.

### SRF-1409 — Proxy discloses internal web servers · Factlink (team `factlink` in the archive row) — no bounty recorded

- Link: <https://hackerone.com/reports/1409>
- Weakness label as recorded: "Information Disclosure"
- Quote (the full class — read-back, not just ports):
  > I found a bug that allows users of your proxy to retrieve pages from your internal web servers -- in this case, the `172.16.64.0/24` subnet. As an example, please see [this link](http://fct.li/?url=https://172.18.64.13). As you will see, it returns the HTML of your Chef server (which, I assume, cannot be accessed from the internet).
- The author numeric case `172.18.64.13` vs subnet `172.16.64.0/24` shows real-world
  internal subnets crossing RFC-documented ranges; keep the quote as evidence, do
  not "correct" it.
- Quote (the only fix line the source offers and it is precise):
  > Please note that once your proxy is also able to follow redirects, it should reject redirects to internal hosts as well.

### SRF-110801 — Internal GET SSRF via CSRF with Press This scan feature · WordPress — **$250** (archive-stated)

- Link: <https://hackerone.com/reports/110801>
- Weakness label as recorded (historical): "Cross-Site Request Forgery (CSRF)" — the
  class is a two-hop chain (CSRF into an admin URL scanner).
- Quote (the class, with the payload that traps other logged-in admins anywhere):
  > The filter does not validate for `0.0.0.0:PORT` and allows the attacker to make the victim send GET request to servers priate127.0.0.1:PORT, localhost:PORT or anything which can be accessed via 0.0.0.0 *(sic — "priate127.0.0.1")*
- Quote (the delivery gadget — a blog-hosted `<img>` tag whose URL is the SSRF):
  > - Victim visits bad site with a content of`&lt;img src="//myWordpress.com/wp-admin/press-this.php?u=htto://0.0.0.0:8080&amp;url-scan-submit=Scan" /&gt; `*(sic — "htto://")*
- Quote (the fix list):
  > The scan/scrape should be a POST request using a csrf token or etc.
  > The address 0.0.0.0 should not be allowd for scanning/scraping. *(sic — "allowd")*
- Chain note for the playbook suite: this is the corpus's direct SSRF-into-CSRF
  instance — the XSS vault's stored-XSS-into-admin playbook touches an identical
  delivery shape but with a script result.

## 3. Calibration first — the cluster's common run card

Every strong case in the cluster calibrates before scanning. The cluster's shared
run card, restated from the cases (with quotes where they are quotes):

1. Resolve the **sink** (which feature issues an attacker-controlled URL).
2. Select the **oracle channel** the target least redacts (status code vs error text
   vs timing vs content vs metatags — see the §1 table).
3. Two-point calibrate with a port you already know (SRF-67389's `scanme.nmap.org:1`
   vs `:22`) and a known-closed port on the internal address, then record the bands.
4. Enumerate with the **exact same wording** as band-classification; never extend to
   content-harvesting in the same pass unless the oracle showed full read-back
   (SRF-1409 is the exception showing a *content* channel).

## 4. Agent execution template

### Context P1 — admin "content-editor" image/link-from-URL sinks

Shopify lines of business (SRF-67377, SRF-67389, SRF-158016 are the anchors):

1. Enumerate any rich-content editor, theme file, collection, product image feature
   that accepts a URL (NOT upload-by-file — those are the File-Upload vault's class).
2. Map validation by feeding three probe frames: scheme-swapped, non-standard port,
   loopback (`0x7f.1` hex notation included). Capture the exact error per frame.
3. Calibrate bands per §3 with `scanme.nmap.org` as the external control pair.
4. Run the bands against loopback ports and, if safe/authorised, two RFC-address
   families (per target's guidance) — but never more than the scope contract.

### Context P2 — registration/profile "custom server" and SSO fields

SRF-16571 anchor. Teams often wire `validateOffice365Account`-style probes for
registration; GWT or RPC-encoded endpoints are worth replaying with
`Content-Type: text/x-gwt-rpc` kept; test the *server* field only.

### Context P3 — validator, crawler, preview, scanner endpoints

SRF-178184, SRF-49474, SRF-110801 anchors. Any endpoint that fetches a URL and
reports back a *human-readable* answer (metatag counts, "port X is open", embed
previews). The human-readable part is what makes the oracle sharable — prefer these
sinks above all others for reliability. Chain note: when the sink is
CSRF-triggered (SRF-110801) the *delivery* needs a victim's logged-in browser; treat
that as impact-chain evidence, not as a directly-reproducible primitive.

### Context P4 — error-echo sinks (nextcloud family)

SRF-145524, SRF-222667, SRF-213358 anchors. When the app echoes libcurl error text
or a human-coded connectivity hint, you get bands without deploying attacker
infrastructure. Probe list: loopback (0.0.0.0/localhost/127.0.0.1 notations incl.
hex `0x7f.1`), same-subnet RFC hosts, and the metadata address (per Cloud-Metadata
playbook).

## 5. Validation gates

1. Both bands must be shown (open evidence + closed evidence) before any claim.
2. A timing channel needs repeat counts — no single-shot RTT claims (SRF-67377's
   author attached network dumps; do the same quality bar).
3. "Internal" language requires the addresses to be internal *per the target's own
   scope statement* — quotes about `172.16/24` subnets in SRF-1409 only prove that
   the affected service could reach them; scope-confession is the tester's job.
4. If the sink triggers asynchronously or behind admin-only UI, record channel
   availability + trust boundary separately (SRF-110801 needs a victim; SRF-16571
   needs only a fresh session).
5. Era limitation is codified here: none of these cases shows a metadata credential
   read or a clear PII payoff — the file stays "mapping" only; escalate via the
   other playbook files (Cloud-Metadata, Media-Processing).

## 6. Remediation flowing from the cases themselves

- SRF-50537: deny local/private ranges, deny unusual ports, rate-limit, and
  "Don't follow redirects to localhost and/or local LAN IP's, either via HTTP
  redirects, or DNS records."
- SRF-1409: reject redirect-to-internal at the proxy layer.
- SRF-110801: "The scan/scrape should be a POST request using a csrf token".
- Modern layer (flagged, not in corpus): response-body redaction plus a
  connect-error normalisation would erase most of the band set; the archive cases
  all predate such pattern.

## 7. Archive-era labels

10 of 12 cases carry a weakness label other than the modern name; the distinct
era labels used were "Information Disclosure" (twice), "Violation of Secure
Design Principles" (three times), "Cross-Site Request Forgery (CSRF)", "Code
Injection", "Cryptographic Issues - Generic", and "None". They show the era
taxonomy could not express SSRF-beyond-portscan consistently. Two exact-SSRF
labels appear (SRF-178184, SRF-213358). Use labels as provenance metadata only,
never as attestation.
