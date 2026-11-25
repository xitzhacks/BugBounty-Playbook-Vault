---
title: "Server-side arbitrary file download — the DoD-heaviest module"
type: playbook
category: file-download-server
cwe: "CWE-22 · CWE-200 · CWE-552"
source_count: 8
full_bodies_available: 8
corpus: "h1.security.nathan.sx roster (86 title-arm rows), bodies via hackerone.com/reports/<id>.json"
list_accessed: "2026-11-05"
note: "Anchor bodies: FU-186326 + FU-230714/230870 (psychomantis DoD download rows), FU-183978/196448/208481 (Army/DoD LFI-RFI summary rows), FU-194351 (yelpblog wp-includes download, the module's only priced row). Claims trace to bodies read 2026-11-05."
---

# Module 07 — the download lane: arbitrariness confirmed by URL, not by exploit

## 1. Overview

Eight rows, **$100/1 paid** — the vault's lowest-priced module and its most concentrated
program profile: seven of eight rows are DoD (the duplicate-guard: 184596/191243 belong to
module 01 — this module holds the download-shaped seven: 183925, 183978, 186326, 196448,
208481, 230714, 230870) plus one commercial row (194351, Yelp, $100 (list)). Four rows carry
the DoD official-voice summaries (body_src=summaries); 194351/186326 carry the fullest
bodies. The lane's economic ceiling is low because demonstrated *system/file* read without credentials or exfiltration of crown-jewel
content rarely detaches from the program's standard award schedule.

**Case-stock (8 rows / $100):**

| Case | Target | Shape | Sev | Bounty |
|---|---|---|---|---|
| [FU-183978](https://hackerone.com/reports/183978) | U.S. Dept Of Defense (Army) | LFI - download local files | high | - (json none) |
| [FU-196448](https://hackerone.com/reports/196448) | U.S. Dept Of Defense | LFI on a DoD website (fransrosen) | medium | - |
| [FU-208481](https://hackerone.com/reports/208481) | U.S. Dept Of Defense | RFI on a DoD website (sp1d3rs) | medium | - |
| [FU-230714](https://hackerone.com/reports/230714) | U.S. Dept Of Defense | DotNetNuke EventsCalendar `?f=~/…` | medium | - |
| [FU-230870](https://hackerone.com/reports/230870) | U.S. Dept Of Defense | same primitive, second instance | medium | - |
| [FU-186326](https://hackerone.com/reports/186326) | U.S. Dept Of Defense | `downloadfile?fileString=…:/pathtodocument` traversal | low | - |
| [FU-183925](https://hackerone.com/reports/183925) | U.S. Dept Of Defense | USTRANSCOM unrestricted download | low | - |
| [FU-194351](https://hackerone.com/reports/194351) | Yelp | wp-includes PHP sources downloadable | none* | $100 (list) |

(*) severity recorded literally as `none` in the JSON.

## 2. Anatomy

### 2.1 The official summary voice and its researchers

Four DoD bodies are mediawiki-style records — a standard sentence plus a credited
researcher. Byte-true, the lane's three shapes:

Army LFI (183978, Nahamsec): "A misconfigured Army website may have allowed unauthorized
users to remotely download local files, potentially revealing sensitive system or user
information. Nahamsec was able to demonstrate this vulnerability by crafting a particularly
formatted URL." — 196448 (fransrosen) and 208481 (sp1d3rs) repeat the DoD-standard sentence
with those same credits ("@fransrosen was able to demonstrate this vulnerability by crafting
a specially formatted URL.", "@sp1d3rs …"); 208481 is titled *Remote file inclusion* even
though its summary sentence is the download phrasing — the H1 title/summary mismatch
surfaced here is a real triage hazard in DoD rows.

USTRANSCOM (183925, ziot): "A misconfigured USTRANSCOM website allowed arbitrary system
files to be downloaded. ziot was able to demonstrate this vulnerability by downloading a
file from a specially crafted URL."

### 2.2 The payload-bearing pair

**FU-186326** carries both voices: the psychomantis official summary ("@psychomantis was
able to demonstrate this vulnerability by crafting a specially formatted URL") and the
researcher's addendum, byte-true:

> This website demonstrated a quite classic file disclosure vulnerability, the website
> contained a feature to download pdf's and documents off the website, this was quite
> similar to the events calendar file disclosure vulnerability. The website looked as
> followed, website.com/xxx/account/downloadfile?fileString=/pathtodocument/document.pdf.
> We could view the etc/shadow or other sensitive files by traversing the directory
> structure using ../ and access the files.

**FU-230714/230870** are the two instances of the *events calendar* shape the addendum
predicted. Byte-true (230714):

> This website used DotNetNuke EventsCalendar which is prone to an arbitrary-file-download
> vulnerability.  An example of what this looks like  is this,
> website.com/desktopmodules/eventscalendar/downloaddoc.aspx
> We can exploit this by appending ?f=~/downloaddoc.aspx  so it'd look like this,
> website.com/desktopmodules/eventscalendar/downloaddoc.aspx?f=~/downloaddoc.aspx

The two rows differ by one word in the official sentence ("and system" vs "or system") —
667 vs 666 chars — recorded as separate instances (the DoD corpus prices re-finds on
sibling estates, no dedupe).

### 2.3 The commercial outlier (194351)

**FU-194351** ($100 (list), severity literally `none`) — yelpblog.com serves *source*
bytes: "through which i am able to download any php files in wp-includes folder. For a PoC,
you can open https://www.yelpblog.com/wp-includes/wp-db.php, and the wp-db.php will be
download(along with all the data in it)" — the body's typos kept as-is ("can sensative
information"). The quick-win shape: the webserver serving `.php` files from `wp-includes`
as attachments instead of executing them.

## 3. Techniques (corpus-derived)

1. **Public-asset handlers are the seed**: `downloadfile`, `downloaddoc.aspx`, PDF viewers
   — the shape here is always a download endpoint that takes a path (186326, 230714).
   `?f=~/…` is the DotNetNuke known-weakness — sibling-site re-scan pays (230870).
2. **Enumerate the estate**: DoD rows repeat primitives across sub-domains/sys-owners —
   same bug × thousands of subdomains = multiple valid reports, per this module's pairs.
3. **Config/source download beats random-file read for triage**: wp-includes gets priced
   because it names a concrete crown-jewel file (194351).

## 4. Kill-gates

- "may have allowed" uncertainty language tracks DoD style, not weak findings — the rows
  still resolved; do not rewrite triage standards on that phrasing.
- No row here proves *authentication bypass* — state authenticated/unauthenticated clearly
  as the corps text does implicitly; the titles are plain file-inclusion-on-a-DoD-site
  statements.
- 184596/191243's upload-shaped rows live in module 01 — don't double-count them here; the
  DoD program-is-profile module split is by shape (upload vs download), not by program.
