---
title: "Adjacent & negative space — triage artifacts, mislabeled rows, and the unclassified merges: what the bucket's keyword net drags in"
type: playbook
category: adjacent-negative-space
cwe: ""
source_count: 13
full_bodies_available: 13
corpus: "h1-brain disclosed_reports.db (sha256 8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4), bucket smuggling-crlf incl. module_map_all _adjacent + _adjacent_unclassified merges"
list_accessed: "2026-11-07"
note: "1 bucket-adjacent (SMUG-246803, $250) + 12 unclassified merges drawn from the 468-row unclassified pool. Bodies read 2026-11-07; triage-artifact rows never counted as class evidence."
---

# Adjacent & negative space — what the bucket's net drags in

## 1. Overview

Thirteen rows, **$7,150/5 paid** (bucket-adjacent $250/1 + unclassified merges
$6,900/4). This module is the negative space, and the corpus pattern is stable:
the class title attracts rows whose actual class is different — cart-quantity
logic, HTTP/2 pseudo-header parsing, AJP forwarding, CodeQL *detector-design*
tickets mislabeled CRLF by the keyword net, and five GitHub-Security-Lab
one-liners. None of these is counted by the class modules; each is kept, quoted
where the body is quotable, and catalogued so the class boundary is visible.
The register assigns all 13 here via `classes.json`; the bounty arithmetic is
preserved so the vault's totals reconcile.

**Case-stock (13 rows / $7,150):**

| Case | Target | What it actually is | Bounty |
|---|---|---|---|
| [SMUG-1391549](https://hackerone.com/reports/1391549) | Apache mod_proxy HTTP/2 | `:method` pseudo-header with spaces → HTTP/1.1 request-line injection on downgrade (unclassified merge) | $1,200 |
| [SMUG-1594627](https://hackerone.com/reports/1594627) | Apache mod_proxy_ajp ≤2.4.53 | Inconsistent request interpretation → request smuggling to the AJP back end (unclassified merge) | $2,400 |
| [SMUG-1401159](https://hackerone.com/reports/1401159) | GitHub Security Lab | "[Python]: CWE-079 HTTP Header injection" — one-line GHSL body (unclassified merge) | $1,800 |
| [SMUG-761222](https://hackerone.com/reports/761222) | GitHub Security Lab | "Netty HTTP Response Splitting (CRLF Injection)" — one-line GHSL body (unclassified merge) | $1,500 |
| [SMUG-246803](https://hackerone.com/reports/246803) | spectacles.com (snapchat) | Business logic: cart quantity edited in URL (`:2500`/`:25000`), no server-side check (bucket `_adjacent`) | $250 |
| [SMUG-39181](https://hackerone.com/reports/39181) | vimeopro.com | CRLF Set-Cookie PoC (`%0dSet-Cookie:test=test;domain=.vimeopro.com`) (unclassified merge) | - |
| [SMUG-145128](https://hackerone.com/reports/145128) | account-global.ubnt.com | CRLF in `?` param → forged `Set-Cookie:crlf=injection` (unclassified merge) | - |
| [SMUG-165102](https://hackerone.com/reports/165102) | python.org / Red Hat | urllib HTTP header injection pointer (CVE-2016-5699) — body is two links (unclassified merge) | - |
| [SMUG-446271](https://hackerone.com/reports/446271) | ads.twitter.com | `?t=%0d%0atest:tested` response splitting (unclassified merge; first recorded in module 02) | - |
| [SMUG-963816](https://hackerone.com/reports/963816) | GitHub Security Lab | "[javascript] CWE-117: CodeQL query to detect Log Injection" — detector ticket, not a find (unclassified merge) | - |
| [SMUG-1135875](https://hackerone.com/reports/1135875) | GitHub Security Lab | "Java: Add query for detecting Log Injection vulenrabilities" (sic) — detector ticket (unclassified merge) | - |
| [SMUG-1135876](https://hackerone.com/reports/1135876) | GitHub Security Lab | Same title as 1135875 — duplicate ticket (unclassified merge) | - |
| [SMUG-1368721](https://hackerone.com/reports/1368721) | GitHub Security Lab | "[Python]: CWE-117 Log Injection" — detector ticket (unclassified merge) | - |

## 2. The two Apache rows that are smuggling in fact, merge in name

Two of the most technically credible rows in the whole intake carry
`_adjacent_unclassified` labels — not because the technique is off-class, but
because the classifier's weakness-name net never saw them. Both land on the
module-01/02 boundary (both are parser differentials against Apache front-ends)
and are kept here so `classes.json` reconciliation stays exact; the playbook
reads them as module-01 lanes.

**SMUG-1391549 (mod_proxy HTTP/2, $1,200)** — the `:method` pseudo-header with
spaces case. The body's own report-to-Apache quote is the mechanism:

> It fails to reject HTTP requests that contain spaces in the :method HTTP/2 pseudo-header. This leads to a request-line injection vulnerability when it downgrades the requests to HTTP/1.1 and routes them on to the backend.

> Provided the back-end server tolerates trailing junk in request lines, this enables attackers to bypass front-end security rules, poison web caches, and > change the protocol to HTTP/0.9 or 1.0, potentially enabling further attacks. I have identified some vulnerable systems in the wild.

The downgraded forward becomes `GET /anything HTTP/1.1 / HTTP/1.1` — the
front-end sees one request, the back-end parses two, which *is* request
smuggling; impact in full:

> This lets attackers bypass front-end security rules like block-rules and escape subfolders. In some cases it may enable further attacks via protocol-downgrades and cache poisoning.

**SMUG-1594627 (mod_proxy_ajp, $2,400)** is the vendor-advisory twin, body a
single paragraph:

> Inconsistent Interpretation of HTTP Requests ('HTTP Request Smuggling') vulnerability in mod_proxy_ajp of Apache HTTP Server allows an attacker to smuggle requests to the AJP server it forwards requests to.

> Information disclosure, RCE

## 3. The GHSL one-liners: header-injection/HTTP-splitting CodeQL work

Five unclassified merges are one-line GHSL bodies carrying real bounty weight
($1,500 and $1,800 for two of them) with zero quotable technique:

> This bug was reported directly to GitHub Security Lab.

Rows SMUG-761222 (Netty response splitting/CRLF, $1,500) and SMUG-1401159
(CWE-079 HTTP header injection, $1,800) are priced like detector work at GHSL
and recorded as anchors, not evidence. Three more — SMUG-963816,
SMUG-1135875, SMUG-1135876, SMUG-1368721 — are not finds at all but
*detector tickets* ("CodeQL query to detect Log Injection", "Add query for
detecting Log Injection vulenrabilities" (sic)) the keyword net pulled in on
`injection` wording. They are the cleanest demonstration of why this vault's
counts read bodies: a ticket whose body is one line and whose title is a
detector design is not a desync, a CRLF, or evidence of either.

## 4. The bucket-adjacent and the small fry

**SMUG-246803 (spectacles.com, $250)** is the bucket's own `_adjacent` row — a
business-logic cart-quantity bypass labeled "HTTP Request Smuggling" by the
classifier and resolved by its body:

> Problem originates from limiting the quantity of the items is with just the UI elements just before adding to cart. After adding to cart step there is no checking step.

> You will see the accessories quantity will be 25000 and the price will be updated according to that.

Its $250 is kept in corpus arithmetic (and in the register), but the technique
belongs in the Business-Logic vault (master row 12).

The remaining unclassified merges are module-02 twins whose only function is
class-breadth evidence: **SMUG-39181** (`http://www.vimeopro.com/crlftest%0dSet-Cookie:test=test;domain=.vimeopro.com`, result: "Creating a
cookie-param" — cookie on the 301), **SMUG-145128** (ubnt `?` CRLF → forged
`Set-Cookie:crlf=injection;domain=.ubnt.com;`, impact spelled out as "XSS via
Cookie, session fixation or bypass Double-Submit Cookie CSRF protection"),
**SMUG-165102** (the CVE-2016-5699 pointer — two URLs, no body), and
**SMUG-446271** (ads.twitter.com, first catalogued in module 02). Their
absence from the bounty column is the vault pattern: the 2014-2016-era web
CRLFs that only forge a cookie were Info/None at triage.

## 5. What pays, what doesn't

- **Bodies win, titles never decide** — the recurring lesson: the two highest
  paid rows in this module ($1,200, $2,400) are vendor-advisory Apache
  disagreements whose *class* is request smuggling by any technical test and
  whose *bucket* is unclassified by the classifier's weakness net; the
  $250 cart row is bucketed smuggling but business logic by its body.
- **Detector tickets ($0 of technique)** vs solid one-liner GHSL finds ($1,200
  average where figured): the triage system distinguishes, even when the
  classifier does not.
- The module's total ($7,150) is excluded from every class-module total in the
  README — it stays in corpus grand arithmetic only (see `source-index.md`
  §3), exactly as RCE's adjacent+noise row stays out of its pure-class
  accounting.

## 6. Cross-references

- SMUG-1391549/1594627 read as module-01 (Apache parser differentials) and
  module-02 (mod_userdir) lanes; their home modules are 01/02, their ledger
  home is here, so the counts reconcile without double-counting technique.
- The five one-line GHSL bodies replicate the Race vault's metadata-only
  problem — size `len=54` is the `Race-Conditions` "one-line body" shelf.
- SMUG-246803 cross-cites `12_Business-Logic/` (master row 12), whose
  quantity-control lane owns the identical client-side-limit shape.
