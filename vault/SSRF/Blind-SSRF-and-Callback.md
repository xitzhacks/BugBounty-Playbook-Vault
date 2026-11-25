---
title: "Blind SSRF, Callback Confirmation & Weaponized SSRF"
type: playbook
category: blind-ssrf
cwe: "CWE-918"
source_count: 3
full_bodies_available: 2
corpus: "HackerOne disclosed reports, 2013–2017 era, h1.security.nathan.sx archive"
archive_accessed: "2026-10-24"
note: "SRF-197365 is metadata-level only (body withheld on unauthenticated retrieval). Cross-references to SRF-243277 live in the Cloud-Metadata file."
---

# Blind SSRF, Callback Confirmation & Weaponized SSRF

## 1. Overview

Blind SSRF in this corpus means: **no response channel returns attacker-readable
content, so the proof of the request is an event you control the receiver of** —
a hit on your listener, or a change in the way only-accessible side-effects (a
failure email, a job outcome) behave. Two confirmed case bodies + one metadata-only
row carry this file, plus one weaponization case where an SSRF-capable feature is
used *as a proxy to attack third parties from the target's network position*.

The weaponization case matters to ethics boundaries more than to exploitation:
SRF-124097 (WordPress pingback) shows a site's own feature becoming a node in a
third-party DDoS. Its triage discipline (what is a *bug against the reporting
target* vs "a configuration concern of the whole ecosystem") is part of the file —
archive-era labels deserve that historical note explicitly.

## 2. Case evidence

### SRF-236301 — Blind SSRF due to img tag injection in career form · Mixmax — no bounty recorded

- Link: <https://hackerone.com/reports/236301>
- Weakness label as recorded: "Server-Side Request Forgery (SSRF)".
- Quote (the sink and the injection, exactly as reported):
  > There is SSRF vulnerability due to img tag injection in career form. Attacker can inject multiple tags and perform multiple requests on remote hosts.
- Steps (verbatim skeleton):
  > 1. Visit https://mixmax.com/careers.
  > 2. Click on `Apply now`.
  > 3. Insert img tag `<img src=https://your_choice.com>` in all the fields.
  > 4. Click on `Send Application`.
  > 5. Check server logs.
- Readback (attribution is the lesson — an automated proxy fetched, not the target
  itself):
  > I got the following ip and user-agent headers.
  > IP: 66.249.84.213
  > User-Agent: Mozilla/5.0 (Windows NT 5.1; rv:11.0) Gecko Firefox/11.0 (via ggpht.com GoogleImageProxy)
- Interpretation duty stated here so agents inherit it: the readback's UA block
  "via ggpht.com GoogleImageProxy" means the fetcher was **Google's image proxy**,
  whose own infrastructure rendered the submitted form content — the empirical
  demo of "content you submit reaches a fetcher". The report does not name which
  internal host the target fetched, i.e. **blind attribution to Mixmax's own
  servers is not shown** — keep that in the impact discussion, never upgrade it.

### (cross-reference) SRF-243277 · Mixmax — the failure-email oracle

Body is in Cloud-Instance-Metadata.md (`3.` "blind variant"). Its machine: webhook
URL fetch → notification asymmetry proves reachability. Keep it as this file's
second anchor for "async side-effects as OOB".

### SRF-124097 — Wordpress Pingback DDoS Attacks in domain: veris.in · Veris Labs — no bounty recorded

- Link: <https://hackerone.com/reports/124097>
- Weakness label as recorded (historical): "Uncontrolled Resource Consumption".
- Quote (the class):
  > Wordpress blogs that have xmlrpc.php enabled for pingbacks, trackbacks, etc. can be made as a part of a huge botnet causing a major DDOS. The website veris.in has the xmlrpc.php file enabled and could thus be potentially used for such an attack against other victim hosts.
- The XML payload verbatim (compressed onto the meaningful lines):
  > `<methodCall>` / `<methodName>pingback.ping</methodName>` /
  > `<param><value><string>http://victim.com</string></value></param>` /
  > `<param><value><string>https://veris.in/anypost</string></value></param>`
- Result and arm mechanics:
  > - As soon as the above request is sent, the victim host gets an entry in its log file with a request originating from the veris.in domain verifying the pingback.
  > - This can be automated from multiple hosts and be used to cause a mass DDOS attack on the victim.
- Post-archive triage-scoping commentary (flagged, not in the corpus): later-era
  programs frequently rejected reports against "your blog is used in pingback
  botnets" and reward only where actual security *of the target* is proven. This
  case is kept because it documents the era's acceptance window AND because the
  same `pingback.ping` call doubles as a **port-scan primitive against arbitrary
  hosts** (the pingback target runs on the reporting camp's own network state).
  Historical labels qualify: "Uncontrolled Resource Consumption".
- Era root source, recovered and quoted in [BLOG-006](references/blogs-index.md)
  (Sucuri, 2014 — cited by this report body itself): 162,000 legit WordPress sites
  attacking one victim, the exact one-curl `pingback.ping` arming command, and the
  era's framing dilemma — "In many cases this same issue is categorized as a
  feature, one that many plugins use, so in therein lies the dilemma." *(sic)*

### SRF-197365 — SSRF через Share-ботов · (Russian-language report; gloss: "SSRF via Share bots") — **$300**

- Link: <https://hackerone.com/reports/197365>
- Weakness label as recorded: "Server-Side Request Forgery (SSRF)" — and the
  report paid out **$300** at time of disclosure (per its JSON).
- Evidence level: **metadata only** — the body was withheld on unauthenticated
  retrieval, so no step or transcript can be quoted. The program/team name is not
  visible in the JSON snapshot read; the archive's own row (title and bounty) is
  the primary evidence.
- It matters to this file for one specific reason: title says "Share bots",
  i.e. the SSRF-sink is a *user-visible share feature fetched server-side* — same
  sink family as SRF-236301's career-form. Route it into sink-class inventory V-slot
  with the metadata-only honesty level.

## 3. Anatomy — the callback & side-effect inference loop

| Channel | How it lands in evidence | Case |
| --- | --- | --- |
| Your listener's logs | request arrives at your server (IP + UA recorded) | SRF-236301 |
| Product's own notifications | failure email present vs absent per probe | SRF-243277 |
| The target's remote-party log entry | the victim site's log records a connection from the target's address | SRF-124097 |

(The era's detectors formalized the first channel exactly — BLOG-001's AcuMonitor
alert carried "the IP address of the server that made this request and the
User-agent used in the request" into the finding; see
[references/blogs-index.md](references/blogs-index.md).)

## 4. Agent execution template

### Context B1 — injected-render blind SSRF (career-form lines)

1. Enumerate forms that render markup into a stored record visible to server-side
   processing (job applications, contact/admin forms, email/MIME bodies, PDF
   exporters). Not file uploads; not user endpoints that render in *their* browser.
2. Inject a single `<img src=https://YOUR-LISTENER/probe-id>` into each field.
3. Read your listener; record IP + UA + timing. Run whois / ASN analysis against
   the source (SRF-236301's own postmortem text) before claiming which owner
   fetched. If the UA shows an intermediary (GoogleImageProxy, email scanner), the
   claim rests at "submitted markup reaches a fetcher" — classify impact accordingly.
4. Variation per field; keep one listener URL per field so attribution per field
   is unambiguous. SRF-236301 injects in "all the fields" — reproduce this audit
   discipline, not its single-URL proof, when the mapping matters.

### Context B2 — async-notification side-effect oracles

Model 100% on SRF-243277 (Cloud-Metadata file): create two identical probes
control + candidate; only a *change in the product's own emitted signal counts*
(notification presence, job outcome, ticket copy). Trigger each identically, keep
timestamps, and never conflate "would seem to fail" with "did fail".

### Context B3 — pingback/weaponization assessment (careful, ethically)

1. Confirm the engagement scope allows attacking third-party infrastructure —
   most don't; if not, record into the *target-only* frame: your target's feature
   fetches *my* URLs (B1) and so can be a honeypot; assert no third-party abuse.
2. For scope-approved work: single pingback.ping, victim URL = your listener,
   and per SRF-124097's own line, the *log entry proves the origin* — record the
   target's actual sending IP, not assumptions.
3. For courts/triage: the (era) outcome on Veris Labs came with no bounty recorded —
   the archive preserves one title, one step-by-step, and no reward figure.
   Present modern-era rejections honestly ("No bounty" in this file, and why).

## 5. Validation gates

1. READ: an OOB hit exists → it is a *channel*, not a finding. The finding is
   the sink. State it that way (SRF-236301's own text does exactly this).
2. Every callback chain names the fetcher (UA/IP attribution): intermediary
   proxy (ggpht.com) vs target-resident infra, with "assumed fetcher" only
   when attribution shows it.
3. Side-effect oracles are executed twice (control vs candidate) with traceable
   timestamps; "control" means the *same feature* with an unroutable or
   loopback known to be denied (SRF-243277's `http://localhost` control).
4. Weaponization claims never present a third-party abuse as *impact against
   the target* unless the target's network position actually grants them the
   privilege shown; file SRF-124097's reading "used for such an attack against
   other victim hosts" is the era's loosest case — cite as such.
5. Metadata-only rows (SRF-197365) are included with that label everywhere they
   are cited; no paraphrasing of a withheld body.

## 6. Archive-era labels in this file

- SRF-236301 "Server-Side Request Forgery (SSRF)" — proper.
- SRF-124097 "Uncontrolled Resource Consumption" — tracks the usage, not the bug
  gene (which is meta-commentary in 2026 hindsight); keep both readings cited.
- SRF-197365 "Server-Side Request Forgery (SSRF)" — proper, body withheld.
