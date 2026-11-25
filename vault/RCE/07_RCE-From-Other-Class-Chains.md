---
title: "RCE from other-class chains — SQLi→RCE, XXE→RCE, upload→RCE, file-read→RCE, token→RCE, some→RCE, queue-trust"
type: playbook
category: chains-from-other-classes
cwe: "CWE-78"
source_count: 14
full_bodies_available: 12
corpus: "h1.security.nathan.sx roster (150 rows), bodies via hackerone.com/reports/<id>.json"
list_accessed: "2026-11-04"
note: "Anchors: RCE-31756 (Drupal SQLi→RCE, $3,000 list), RCE-178152 (GitLab read→RCE, critical), RCE-224198 (Redis→Sidekiq eval). Claims trace to bodies read 2026-11-04."
---

# RCE from other-class chains — the originator owns the finding

## 1. Overview

Fourteen rows, **$9,457/7 paid**. Every row here is an execution *delivery* where the
flaw that got the attacker in is another class: SQLi (RCE-31756), XXE (RCE-55431),
file upload (RCE-84374, RCE-116575), token leakage (RCE-158330), arbitrary file read
(RCE-178152), SOME/XSS (RCE-134738), template-XSS (RCE-125027, RCE-230234, RCE-217790),
type-juggling→POI (RCE-202774), unauth-create/delete (RCE-191884), supply-chain download
(RCE-186352), and the queue-trust row (RCE-224198). The vault keeps them for one reason:
**the execution step is always the same small move** — the corpus's chains converge on
module 01–06's registry of "what becomes possible once you are in".

**Case-stock (14 rows / $9,457):**

| Case | Target | Originator class | Delivery to execution | Bounty |
|---|---|---|---|---|
| [RCE-31756](https://hackerone.com/reports/31756) | ibb (Drupal core row) | pre-auth SQLi | sessions + callbacks → PHP exec | $3,000 (list) |
| [RCE-178152](https://hackerone.com/reports/178152) | GitLab | export symlink → file read | secrets → marshalled cookies → RCE | - (critical) |
| [RCE-158330](https://hackerone.com/reports/158330) | GitLab | token leak | admin surface → RCE claim | - (critical) |
| [RCE-125027](https://hackerone.com/reports/125027) | Uber | Angular template injection | client-side XSS (class reclass) | $3,000 (json) |
| [RCE-134738](https://hackerone.com/reports/134738) | WordPress | SOME (plupload.flash.swf) | plugin install → RCE | $1,337 (list) |
| [RCE-217790](https://hackerone.com/reports/217790) | Shopify | twine template injection | admin-context eval primitive → XSS | $1,000 (json) |
| [RCE-55431](https://hackerone.com/reports/55431) | drchrono | XXE | file read → "(that can be any command)" claim | $700 (list) |
| [RCE-186352](https://hackerone.com/reports/186352) | Phabricator | HTTP install scripts | MITM binary swap → root RCE | $300 (json) |
| [RCE-116575](https://hackerone.com/reports/116575) | legalrobot | upload | upload → RCE (metadata-only) | $120 (list) |
| [RCE-84374](https://hackerone.com/reports/84374) | ownCloud | apps upload | php5 executed | - |
| [RCE-191884](https://hackerone.com/reports/191884) | Twitter Reverb | unauth create/delete + traversal | ext=php defacement; RCE claimed, not shown | - (low) |
| [RCE-202774](https://hackerone.com/reports/202774) | expressionengine | type juggling | PHP object injection → SQLi (chain row) | - (metadata) |
| [RCE-230234](https://hackerone.com/reports/230234) | WordPress | Angular template injection | reflected XSS (class reclass) | - |
| [RCE-224198](https://hackerone.com/reports/224198) | GitLab | queue-trust boundary | Sidekiq `GitlabShellWorker` `instance_eval` | - (informative) |

## 2. Drupal 7: the chain that ended in callbacks

RCE-31756 (**$3,000 (list)**, weakness SQL Injection) is the era's most famous chain —
SektionEins's CVE-2014-3704. The body names the exact halting point after the SQLi:

> Since Drupal uses PDO, multi-queries are allowed. So this SQL Injection can be used to
> insert arbitrary data in the database, dump or modify existing data or drop the whole
> database.

> With the possibility to INSERT arbitrary data into the database an attacker can execute
> any PHP code through a manipulated Session and Drupal features with callbacks.

That sentence is the module's thesis in miniature: SQLi writes the session row; a Drupal
callback executes it. The "RCE" in the title was the *impact statement*, documented by
object-level mechanics — and the vulnerable code shown is the `expandArguments` array-key
expansion (`:name_0` construction). The corresponding SQLi vault owns the trigger class;
this module records the delivery claim.

## 3. GitLab's file-read-to-RCE composition

RCE-178152 (critical, unpaid) — jobert's export-upload analysis. The chain: a symbolic
link inside a GitLab export tar + Ruby's `JSON.parse` error text → arbitrary file read;
then the singular move, quoted from the body's later sections:

> This results in an RCE because cookies can be marshalled and resigned again.

The mechanics are module 03's (Rails CookieStore — 134321/206227), reached through the
read primitive. This row is why the vault teaches the *composition* discipline: the same
 Rails-secret primitive that paid $500/$2,500 as a standalone recon find becomes a
critical chain here. RCE-158330 (critical, unpaid, metadata) is the token-flavored sibling.

## 4. Queue-trust: RCE-224198

RCE-224198 (informative, unpaid) is the module's most instructive *design* row. The trigger
is the Redis CLI (a trust boundary violation in itself), and the delivery is a
`instance_eval` sink:

> This results in code execution as the GitlabShellWorker allows any public method on the
> shell object to be executed. All ruby objects have inherited instance methods that result
> in remote code execution when an attacker controls the method name and at least one
> parameter.

The proposed fix names the class boundary:

> It is not necessary that GitLab execute arbitrary code from the job queue. Jobs may be
> whitelisted and executed only from a fixed list of tasks. Other GitLab service workers
> follow this more secure paradigm.

The triage landed **informative ($0)**: internal-prerequisite findings (Redis write) are
the mongo lane's rejection case — the corpus holds it for the design lesson, not the bounty.
Modern echo (P4): every Sidekiq/Resque/Celery deployment re-runs this exact question —
can a queue entry name a worker method? — and the modern answer is the fixed allow-list
this 2017 body proposed.

## 5. Client-side template injection rows: the reclass record

RCE-125027 (**$3,000 (json)**), RCE-217790 (**$1,000 (json)**), RCE-230234 (unpaid) are
AngularJS/twine template injection rows whose titles promise template injection, but whose
bodies are client-side — the payload executes in the victim's browser (Uber developer
portal, mercantile.wordpress.org, myshopify admin), reaching eval primitives and XSS.
Class doctrine (bodies win, not titles) mandated the reclass out of module 02; they live
here as the chain record with cross-references to the XSS vault. The honest headline:
**client-side template injection ≠ server-side RCE** — and the corpus paid **$3,000 and
$1,000 for the client-side versions anyway** (Uber and myshopify admin-trust contexts).

RCE-134738 (WordPress SOME, **$1,337 (list)** — the corpus's only l33t bounty) completes
the client-origin row set: Cure53's plupload.flash.swf SOME chain to plugin install RCE.

## 6. Upload & install-lane rows

RCE-84374 (ownCloud apps upload → php5 executed, unpaid), RCE-116575 (metadata-only,
$120 list), RCE-191884 (create/delete + `ext=php`, low, RCE "possible" — honestly-capped
claim, unpaid). RCE-186352 (**$300 (json)**) is the install-lane row: Phabricator's
install scripts fetching binaries over plain HTTP and `sudo`-executing them:

> The install_rhel-derivs.sh file download binaries over plain HTTP and run/install them
> using sudo without verification (checksum / GPG), thus:
> * active MITM attacker can modify the binaries with malicious code.
> * malformed target server infrastructure can deliver malicious code (server
>   hacked/DNS hijacked/etc..)
> The malicious code will run under ROOT.

The class is supply-chain-by-HTTP; the vault keeps it as a chain because the RCE requires
the external MITM position. Bibliography's dependency-confusion stories (blogs-index
§2.5c) are this lane's modern generation.

## 7. What pays, what doesn't

- Paid rows concentrate where the chain is *one* hop from bounty-grade impact
  (SQLi→session→exec $3,000; XSS-class reclasses $3,000/$1,000 on admin-trust contexts).
- Unpaid rows: the critical-but-unpaid GitLab pair (158330/178152 — GitLab VDP era paid
  selectively for full chains), every upload-lane row except the $120 metadata row, and
  the queue-trust row (prerequisite-heavy). The XXE-origin chain did pay, but only at the
  claim tier.
- The XXE row's price ($700) against its era (2015, drchrono) shows the *claim* pricing:
  the body demonstrates /etc/passwd read and then reaches for "(That can be any file on
  the system or any command)" — the command claim was paid at a claim-level tier.

## 8. Cross-references

- `../SQLi` vault owns RCE-31756's trigger class; `../XXE` owns 55431's; `../CSRF` and
  `../Open-Redirect` chains appear in blogs-index §2.6 ("CSRF to RCE", "open redirect to
  RCE" writeups); file-upload → RCE rows belong to the future file-upload vault (../)
  — its lane is recorded here as the delivery shelf only.
- Module 03 is the Deser mechanics reference for 178152's deliverable; module 06 for the
  console lanes.
