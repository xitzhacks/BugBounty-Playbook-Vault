---
title: "Noise / harden / informative shelf — the talking ledger of the upload lane"
type: playbook
category: upload-noise-shelf
cwe: "CWE-434 (adjacent) · CWE-693"
source_count: 8
full_bodies_available: 8
corpus: "h1.security.nathan.sx roster (86 title-arm rows), bodies via hackerone.com/reports/<id>.json"
list_accessed: "2026-11-05"
note: "Anchor bodies: FU-258117 (Snapchat Jenkins $5,000 — cross-ledger), FU-7929 (H1 S3 hosting, the shelf's doctrinal row), FU-126374 (Uber text upload). Claims trace to bodies read 2026-11-05."
---

# Module 09 — the shelf: intended behavior, harness notes, and the misfiled money row

## 1. Overview

Eight rows, **$5,100/2 paid** — and the $5,000 (list) is FU-258117, a title-arm duplicate
whose body makes it AUTH-class (Jenkins auth flow), not an upload bug at all. It sits here
because the funnel pulled it by title; the register carries the cross-ledger notes. The
other seven are the lane's genuine furniture: hosting-misuse design notes (7929, 126374,
172694), a size-check harden row (19532), a bypass-with-no-impact-moment (145604, 131028),
and one upload-page XSS that is really a GET/POST asymmetry story (31187).

**Case-stock (8 rows / $5,100):**

| Case | Target | Shelf role | Bounty |
|---|---|---|---|
| [FU-258117](https://hackerone.com/reports/258117) | Snapchat | misfiled by title — Jenkins auth-flow RCE (RCE-258117/AUTH-258117 cross-ledgers) | $5,000 (list) |
| [FU-7929](https://hackerone.com/reports/7929) | HackerOne | S3 attachment hosting-misuse, design note | - (list) |
| [FU-126374](https://hackerone.com/reports/126374) | Uber | text-as-PNG into uber-documents S3 (phishing) | - (list) |
| [FU-131028](https://hackerone.com/reports/131028) | Moneybird | malicious-extension attachments — filter shipped | $100 (list) |
| [FU-172694](https://hackerone.com/reports/172694) | Udemy | "That is intended behavior" | - (list) |
| [FU-31187](https://hackerone.com/reports/31187) | Bookfresh | reflected XSS on the upload-form view (GET/POST asymmetry) | - (list) |
| [FU-145604](https://hackerone.com/reports/145604) | Nextcloud | php-in-JPEG bypass, no live impact (rename) | - (list) |
| [FU-19532](https://hackerone.com/reports/19532) | Uzbey | missing size check → leak/DoS claim | - (list) |

## 2. The shelf's own quotes

### 2.1 The doctrinal row (7929)

**FU-7929** is the lane's most-cited design argument, byte-true:

> This allows for uploading malware such as
> [msf-payload-x86.jpg.exe](https://hackerone-attachments.s3.amazonaws.com/production/000/006/741/bf60ba068e72e767b93d3fa35c89a36639dd1f19/msf-payload-x86.jpg.exe?AWSAccessKeyId=[REDACTED_AWS_KEY]&Expires=1397769394&Signature=aoXXsjuCqUjReIFLzMtXYyMO5us%3D) or whatever.
> Beyond free hosting this could potentially be used to entice teams into downloading stuff
> they probably don't want.

with the reporter's own restraints — "I could imagine this to be working as intended but
still believe it would be good to consider restrictions even if the result is to not
enforce any." Informative, and the vendor shipping the warning banner is the shelf's happy
ending. **FU-126374** (Uber) is the same discussion with a mitigation already in place:
"When the file extension (```.png``` in our case) and the MIME type (```image/png```)
match, Internet Explorer will not render it as HTML, it is only willing to render it as
plain text." — extension/MIME *agreement* closes the render path; the row still argues the
phishing residual on `uber-documents.s3.amazonaws.com`.

### 2.2 The implemented-filters row (131028, 172694)

**FU-131028** ($100 (list), Moneybird) closes paid: "This researcher found a vulnerability
in which it was possible to upload attachments with malicious extensions. We have
implemented a security filter to prevent these attachments to be uploaded." **FU-172694**
(Udemy) records the vendor denial itself, byte-true: "The investigator found that he can
upload any file type to our upload bucket.  That is intended behavior - file content is
enforced before moving it out of our upload bucket." — egress validation as the declared
control.

### 2.3 The harden + bypass rows (145604, 19532)

**FU-145604** (Nextcloud avatar, informative): "We can bypass Avatar Upload image
verification and extension  uploading a php file or any other extension binding a valide
jpeg image  , there is no risk for the moment because the avatar is renamed to
avatar_upload on the remote server" — signature+extension checks pass; the rename saves the
day; the row is the exact signature of why one keeps both checks under review. **FU-19532**
(Uzbey) is the size-check companion, typos intact: "So i first tried to upload a file of
about 2,52 GB (see the pic) and no warning messaege about the size wasn't displayed (such
as a 413 error message), and the site was unable to charge the page".

### 2.4 The GET/POST asymmetry story (31187)

**FU-31187** (Bookfresh upload_form view, resolved unpaid) — the reflected XSS on the
*upload page*, not the upload mechanic: `<style>body{ background-color: #[VALUE_OF_BK]; }</style>`
with "you are only protecting the `GET` requests. So, if I do a `POST` request the value of
`bk` is shown in the page without encoding or removing the tags." It sits on the shelf for
vault bookkeeping only — sink is web-XSS-class; lesson (POST-guard gap) is real.

### 2.5 The misfiled money row (258117)

**FU-258117** ($5,000 (list)) — test Jenkins reachable with any Google account ("@nahamsec
found a test Jenkins instance where they could login with any valid Google account"), body
links the recon blog. No upload mechanism anywhere; module 09 holds the row so the funnel
stays closed, and the cross-ledgers do their job: RCE-258117 (module 06) + AUTH-258117
(class 08). The RCE build read it metadata-only; this build's re-fetch delivered the
495-byte summaries body — page state moved between pulls, recorded in the register.

## 3. Techniques (corpus-derived)

1. **Content-enforcement on the way out, not the way in** (172694) is a valid defense to
   *describe*, and testing it means fetching egressed bytes — not trusting the UI.
2. **Free-hosting arguments get informative** unless concrete downstream risk (7929's own
   climb: "Actual exploitation would likely depend on obfuscating the filename to look more
   innocent, general human errors, a certain trust in files being served from
   `hackerone-attachments.*.amazonaws.com` or separate issues entirely.").
3. **The lint**: any "malicious file upload" title whose body shows backend auth/console
   issues gets refiled (258117) before it contaminates class stats.

## 4. Kill-gates

- A row leaves the shelf only by *demonstrating* the module-level primitive (stored XSS
  97672-style, RCE 84374-style). 19532's own climb "that colud also make a dangerous
  memory leak or exploitable overflows" ("colud" sic) stays a harden note — speculation is
  not a sink.
- Money rows on the shelf are recheck rows, not price anchors: neither $5,000 (258117) nor
  $100 (131028) belongs to upload-class pricing; both are bookkeeping entries.
