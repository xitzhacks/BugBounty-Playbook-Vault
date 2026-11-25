---
title: "Cloud & Instance Metadata via SSRF"
type: playbook
category: cloud-metadata
cwe: "CWE-918"
source_count: 3
full_bodies_available: 3
corpus: "HackerOne disclosed reports, 2013–2017 era, h1.security.nathan.sx archive"
archive_accessed: "2026-10-24"
note: "All claims below come from report bodies read in full this session. Severity/bounty figures are as recorded on HackerOne at disclosure time."
---

# Cloud & Instance Metadata via SSRF

## 1. Overview

This class is an SSRF whose target is the cloud's own metadata service: a
link-local web endpoint on `169.254.169.254` (or an equivalent per-platform
address) that the instance's hypervisor answers about the VM itself — hostname,
IAM role names, availability zone, and in the era-defining case, **user-data
startup scripts** that hold injected secrets.

The archive's evidence for this class is small but complete — three reports,
each demonstrating one distinct wire the attacker pulls:

1. `SRF-53088` — the canonical chain: an already-known SSRF is pointed at
   `169.254.169.254` on EC2 and OpenStack, and the report explains *why* user-data
   is the prize (startup scripts containing "passwords, private keys, source code").
2. `SRF-128685` — metadata read plus port-state readbacks on the same host: the
   metadata listing returned and a local admin panel (`:8081`) confirmed reachable —
   and the write-up reached metadata through a hex-notation host (`0x7f.1`), which
   shows a validator bypass being consumed by this class in the same report.
3. `SRF-243277` — the *blind* variant: no response is readable, but the webhook's
   own failure-email behaviour is used as an oracle to prove the metadata URL is
   reachable, then to enumerate paths under it (MAC addresses).

Era note (stated honestly, not evidenced in this corpus): all three predate
AWS's IMDSv2 token requirement (2023+). A modern replay of this playbook must
verify whether the target stack requires a `PUT /latest/api/token` exchange with
hop-limit rules before claiming a metadata read is possible. Nothing in this
corpus addresses either variant of that defence.

## 2. Case evidence

### SRF-53088 — SSRF vulnerability (access to metadata server on EC2 and OpenStack) · Phabricator — **$300**

- Link: <https://hackerone.com/reports/53088>
- Weakness label as recorded (historical): "Information Disclosure"
- Bounty: **$300**
- Program context: this is an *upgrade* report to `SRF-50537` (`#50537`, port-scan
  oracle on the same Phabricator macro feature, closed "Won't fix" upstream). The
  author raises the impact ceiling from "port scan" to "read the metadata service".
- Quote (that the metadata service is a single-instance loopback):
  > Given the multicast IP address, this server can only reached from the instance itself.
  *(sic — "can only reached")*
- Quote (what is at stake — the corpus's clearest impact statement for this class):
  > Plenty of interesting information are stored at /latest/meta-data/ ([hostname](http://169.254.169.254/latest/meta-data/hostname), private and public IP addresses, ...). However, the worst scenario is auto-starting instances, where a startup script is stored in [/latest/user-data](http://169.254.169.254/latest/user-data). These startup scripts may include passwords, private keys, source code, ...
- Quote (the follow-through targets beyond EC2):
  > Outside of EC2 and OpenStack, some services are commonly bound to localhost, including monitoring software, noSQL databases, administration interfaces, ...
- Evidence shown: test URLs with `/latest/meta-data/hostname` and `/latest/user-data`.
  Per-link disclosure of what the author actually read back is **not shown in the
  source** beyond these URLs — the report's claim is the *reachability* plus the
  documented public knowledge of what those endpoints hold. Do not over-read it as
  proof that secrets were returned in this test.

### SRF-128685 — SSRF on testing endpoint · APITest.IO — no bounty recorded

- Link: <https://hackerone.com/reports/128685>
- Weakness label as recorded (historical): "Privilege Escalation" — an
  object-lesson in archive-era label noise; the body is an SSRF.
- Bounties: none recorded on the report JSON.
- Quote (the sink):
  > The form at https://www.apitest.io/request accepts (among others) the "url" parameter. This feature allows to reach internal services (like the OpenStack metadata server) or services running on loopback.
- Quote (metadata evidence, in the report's format of URL → observed response):
  > http://169.254.169.254/meta-data (OpenStack metada) =&gt; directoty listing (instance-id, mac, local-ipv4, public-ipv4, network_config/content_path, SUBID, ipv6-addr, ipv6-prefix)
  *(sic — "metada", "directoty")*
- Quote (validator bypass used on the same field — hex shorthand for 127.0.0.1):
  > http://0x7f.1/ (nginx) =&gt; "If you see this page, the nginx web server is successfully installed and working. Further configuration is required."
  This line is doing two jobs at once: it proves the fetch happens server-side
  (a loopback-resolved name returned content) and that the input filter accepted a
  non-decimal host notation.
- Quote (chaining into a local admin surface):
  > http://0x7f.1:8081/ (vestacp admin panel) =&gt; &lt;a href="http://vestacp.com/"&gt;Powered by VESTA&lt;/a&gt;
- Quote (honest impact scoping at the end of the session):
  > The metadata server does't seem to host any sensitive data. However, access to port 8081 may allow to reconfigure the OS or services (untested).
  *(sic — "does't"; the author also notes in the same paragraph: "Additional services may exist, but it seems that my IP address (81.56.184.117) was just blacklisted on your side." — a reminder that these testing endpoints are monitored.*

### SRF-243277 — SSRF via webhook · Mixmax — no bounty recorded

- Link: <https://hackerone.com/reports/243277>
- Weakness label as recorded (historical): "Server-Side Request Forgery (SSRF)" —
  this one is textbook-modern for 2017.
- Quote (the class):
  > There exists an SSRF vulnerability with the account webhook feature, allowing an attacker to verify the existence of the EC2 metadata url and enumerate URL's.
- Method: the webhook is created pointing at `http://169.254.169.254/latest/meta-data/`
  and later triggered by email traffic. Because the feature emails the account owner
  when a webhook fails, **delivery vs failure of that email becomes the oracle**:
  > Note that an email is not sent saying the webhook failed. I tried for other internal urls such as 'http://localhost', but they sent a failure email, indicating that `http://169.254.169.254/latest/meta-data/` is open to the webhook.
- Enumeration ceiling (still oracle-only — content is not returned):
  > In addition to verifying that this endpoint exists, an attacker could enumerate endpoints on this domain. For example, an attacker could enumerate MAC addresses at `http://169.254.169.254/latest/meta-data/network/interfaces/macs/xx:xx:...`
- Author's proposed fix, verbatim:
  > Suggested fix:
  > Blacklist the AWS metadata url and any other sensitive internal urls.

## 3. Cross-case anatomy

| Step | SRF-53088 | SRF-128685 | SRF-243277 |
| --- | --- | --- | --- |
| Sink | Phabricator macro "URL" upload field | `/request` form "url" parameter | Account webhook URL |
| Validation in place | Port/protocol filter only (per SRF-50537 triage) | "url" accepted; loopback reached via `0x7f.1` hex notation | Internal URLs (e.g. `localhost`) acknowledged with a failure email — metadata exempt, so no IP denylist on the metadata range shown |
| Oracle type | Direct response (metadata URLs listed as reachable) | Direct response (metadata listing quoted) | Side-effect oracle: webhooks succeed = no failure email |
| Metadata endpoints evidenced | `/latest/meta-data/hostname`, `/latest/user-data` (EC2/OpenStack docs cited) | `/meta-data` directory listing with 8 field names | `/latest/meta-data/` root presence + path enumeration logic |
| What was returned to the attacker | Reachability + public documentation of contents; contents per-link not shown | Explicit field list from the listing | Nothing returned; existence and enumerability proven |
| Impact claim in report | user-data startup scripts can contain credentials | port `8081` admin panel reachable loopback-side | endpoint enumeration incl. MACs |

Failure-email side-channel notes for the playbook:

- The oracle is *asynchronous* (trigger by ordinary product use — here, sending and
  receiving email — and read the notification stream later). It still satisfied the
  archive-era standard of evidence: an observable, reproducible difference caused
  only by the tested URL.
- Modern equivalents of the same oracle idea: asynchronous job queues, export
  features, scheduled reports, anything with success/failure notifications driven
  by the fetch result.

## 4. Agent execution template

Run each context only against the exact sink class named; if a sink is missing,
mark "not applicable — no such sink observed". Never synthesise a URL form the
target does not implement.

### Context M1 — direct metadata read through a known SSRF sink

Prerequisite: an SSRF sink already confirmed to fetch arbitrary URLs (any of the
route R1–R3 outcomes in the parent playbook). Then:

1. Request the metadata address in all notations the parser may accept:
   `http://169.254.169.254/latest/meta-data/`, plus (loopback-family) `169.254.169.254`
   alternatives only if the sink normalises hosts — `SRF-128685`'s `0x7f.1` shows
   that notation bypasses belong on the same test list.
2. Record the raw response. Presence of `ami-id`, `instance-id`, `hostname`,
   `local-ipv4`, `public-ipv4`, `network/interfaces/macs/` establishes the class.
3. If `/latest/meta-data/` answers but a directory listing is not rendered, enumerate
   documented leaves one level at a time (`hostname`, `local-ipv4`, IAM/credentials
   paths): SRF-128685's listing establishes which fields exist for *OpenStack*-style
   clouds; per AWS, `Not disclosed in the source` — field-by-field verification is
   the agent's job, never assumed.
4. If user-data (`/latest/user-data` on EC2/OpenStack naming) is reachable, treat it
   as Cloud-credential-class evidence: SRF-53088 states user-data may include
   "passwords, private keys, source code" — quote what is actually returned; never
   paraphrase up. Redact secrets in evidence per repo evidence-hygiene rules.

### Context M2 — blind metadata proof via asynchronous oracles (Mixmax pattern)

1. Find a feature that accepts a URL and eventually emits success/failure feedback to
   the tester's account (webhooks, integrations, importers with notification).
2. Create two oracles in the same feature: one against a host known to fail
   (`https://localhost:` or an unroutable address — SRF-243277 used `'http://localhost'`
   as the failure benchmark), one against the metadata address.
3. Trigger both identically; record whether the failure notification fires for one
   and not the other. That asymmetry is the finding. Claims must state explicitly:
   "existence and path enumerability proven; response body not returned."
4. Optionally enumerate path families with the same oracle before reporting
   (SRF-243277 named the MAC path as the example).

### Context M3 — metadata-adjacent loopback service reads

Same session, same sink (SRF-128685 anatomy):

1. After metadata is reachable, scan the loopback set for admin surfaces: standard
   port list plus any port the product otherwise filters — the report's find was
   `:8081` (VestaCP panel).
2. Impact language stays at "configurable/reachable (untested intentions)" unless
   something further (a working privileged action) is actually performed — quote
   SRF-128685's "(untested)" self-discipline.

## 5. Validation gates

1. **OOB-or-it-didn't-happen** — every claim about reachability is backed by a
   response transcript (SRF-128685) or a reproducible side-effect asymmetry
   (SRF-243277). "Metadata is standard on cloud hosts" is background, never evidence.
2. **Two-way oracle check** — show the failure benchmark alongside the hit
   (SRF-243277's `http://localhost` benchmark) so triage can reproduce both sides.
3. **No secret paraphrasing** — if user-data or IAM credential paths return
   material, quote the *fact* it was returned and include a redacted excerpt
   consistent with the repo's evidence rules; do not paste credentials.
4. **IMDSv2 check is mandatory in the modern synthesis** — as above, this corpus
   cannot settle it; the agent must establish it per target.
5. **Rate/self-discipline note** — SRF-128685's author got field-blocked mid-session
   ("my address... was just blacklisted"); ration requests, same net result achieved.

## 6. Remediation as seen in the corpus + modern layer

From the source (SRF-243277): "Blacklist the AWS metadata url and any other
sensitive internal urls." From the source (SRF-53088's baseline purpose): denylist
the metadata range in any URL-fetching feature.

Modern layer (not evidenced in the corpus, flagged as modern knowledge):
network-layer metadata isolation (iptables/nftables/egress control on
`169.254.169.254`), IMDSv2 token mandatory + hop-limits, per-instance credential
boundaries — triage reviews of SSRF reports in 2026 do not compare equal unless the
agent reports which of these are in force.

## 7. Archive-era labels

| Case | Recorded weakness | Reality (per body) |
| --- | --- | --- |
| SRF-53088 | Information Disclosure | SSRF into metadata service (field not available in era taxonomy) |
| SRF-128685 | Privilege Escalation | SSRF read + loopback panel readback; the "escalation" language refers to internal reach, not RBAC |
| SRF-243277 | Server-Side Request Forgery (SSRF) | Correct class label for its time |

Severity implications carry the era's (lower) ceiling: $300 was a *paid* amount for
this class at Phabricator in 2015 — do not import that number as a modern
expectation.
