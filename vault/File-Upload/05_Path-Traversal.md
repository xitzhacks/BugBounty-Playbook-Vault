---
title: "Path traversal — read, write, delete, and the file-existence oracle"
type: playbook
category: path-traversal
cwe: "CWE-22"
source_count: 9
full_bodies_available: 9
corpus: "h1.security.nathan.sx roster (86 title-arm rows), bodies via hackerone.com/reports/<id>.json"
list_accessed: "2026-11-05"
note: "Anchor bodies: FU-122475 (Imgur $5,000 list), FU-3370 (Rails CVE-2014-0130 $1,500 list), FU-183568 (BuddyPress deletion), FU-213558 (Discourse symlink restore, $512 json). Claims trace to bodies read 2026-11-05."
---

# Module 05 — the ../ ladder: traversal read / write / delete

## 1. Overview

Nine rows, **$8,512/7 paid** — second-richest module absolute, first per-row average among
the big lanes. The corpus's traversal rows split by *verb*: **read** (122475 Imgur $5,000
(list), 3370/$1,500 and 43440/$1,000 Rails framework rows, 18371 jsDelivr, 213558 Discourse
$512 (json)), **write/overwrite** (254200 Unikrn S3-bucket escape $50 (list)), **delete**
(183568 BuddyPress `unlink()` $350 (list) — the vault's only deletion primitive), and the
**hybrids**: 163421 (WordPress admin-ajax traversal → `/dev/random` DoS) and 158021
(Instacart $100 (json) — the path-disclosure exhibit). BBH's live bucket math (source-index
§4) says the same thing about volume: Path Traversal 236 reports — an order of magnitude
over every other file bucket.

**Case-stock (9 rows / $8,512):**

| Case | Target | Verb | Mechanism | Bounty |
|---|---|---|---|---|
| [FU-122475](https://hackerone.com/reports/122475) | Imgur | read | `imageid=` traversal under `/edit/process` | $5,000 (list) |
| [FU-3370](https://hackerone.com/reports/3370) | Ruby on Rails | read | view-resolver wildcard segment + backslash bypass | $1,500 (list) |
| [FU-43440](https://hackerone.com/reports/43440) | Ruby on Rails | oracle | arbitrary file-existence disclosure in Action Pack | $1,000 (list) |
| [FU-213558](https://hackerone.com/reports/213558) | Discourse | read | tar restore symlink → `/uploads/…/.jpg` | $512 (json) |
| [FU-183568](https://hackerone.com/reports/183568) | WordPress (BuddyPress) | delete | `bp_avatar_set` `original_file` → `unlink()` | $350 (list) |
| [FU-158021](https://hackerone.com/reports/158021) | Instacart | disclose | rmagick error echoes upload tmp path | $100 (json) |
| [FU-254200](https://hackerone.com/reports/254200) | Unikrn | write | `../` in S3 avatar filename escapes user dir | $50 (list) |
| [FU-163421](https://hackerone.com/reports/163421) | Nextcloud site (WP 4.5.3) | DoS | admin-ajax `plugin=../../../…/dev/random` | - (list) |
| [FU-18371](https://hackerone.com/reports/18371) | jsDelivr | read | overlong UTF-8 `%c0%af` on staging CDN | - (list) |

## 2. Anatomy

### 2.1 The read rows

**FU-122475** is the module's money row ($5,000 (list), summary-sourced). Its whole
mechanism fits one sentence plus the payload — byte-true:

> Filepaths were able to traverse up outside of their intended directory when using the
> /edit/process API endpoint.
>
> Insufficient imageid filtration in image editor allowed an attacker to read arbitrary
> files. An attacker could read files by setting file path in imageid GET param in
> /edit/process API endpoint -
> http://imgur.com/edit/process?imageid=../../../../../../../../../../etc/passwd

**FU-3370** is the framework-engineering row — Rails' view resolver both leaks and
under-defends. Two byte-true carries:

> If an attacker made a request `GET /help/../../../Gemfile`, ActionView::FileSystemResolver
> returns Gemfile from project root as the matching view.

> However, Rack::Protection::PathTraversal can be bypassed using backslashes:
> `GET /help/%5c../%5c../%5c../Gemfile`. The resolver uses Dir.glob, which escapes
> backslashes unless File::FNM_NOESCAPE flag is used.

The report attaches fixes *for the framework* (this is Rails' own program) — the corpus's
one case where the hunter wrote the patch (CVE-2014-0130 family; sibling FU-43440 is the
existence-oracle variant whose 122-byte body is the upstream rails-security link:
"This bug was reported directly to the Rails team: https://groups.google.com/forum/#!topic/rubyonrails-security/23fiuwb1NBA").

**FU-18371** (jsDelivr staging, unpaid) is the byte-encoding exhibit:
`http://staging.jsdelivr.net//..%25c0%25af..%25c0%25af…/etc/passwd` — double-encoded
overlong UTF-8 `%c0%af` walking eight levels. Cache/CDN IIS-inherited handling still
unfolds it; *staging* domains carry it first.

**FU-213558** (Discourse, $512 (json)) is the archive row: restore-from-backup tars accept
a symlink — byte-true core steps:

> 6. Create a symlink to `/etc/passwd` In the /uploads/ folder of the backup, e.g.
> `/uploads/default/original/1X/[file].jpg`.
>  * example: `ln -s /etc/passwd /home/symlink/files/uploads/default/original/1X/7ad2e8f5fe02890f20503044b604e29e6f3718fd.png`
> 7. Create a .tar.gz from the extracted files.
> 8. Upload the newly crafted tar to the server.
> 9. Enable `Restore from Backups` in settings if it's not enabled.
> 10. Restore from the backup that uploaded.
> 11. Go to the uploaded file in your browser after it uploads, e.g.
>  * http://try.discourse.org/uploads/default/original/1X/[file].jpg
> 12. ---> You were able to read file contents of `/etc/passwd` due to the symlink being
> extracted from the tar.

### 2.2 The write row (254200)

**FU-254200** (medium, $50 (list)) — Unikrn's S3 avatar path. The body's mechanism
sentence, byte-true:

> I was able to escape from the unique directory (where the user's avatar is stored after
> uploading -`https://unikrn-files.s3-eu-west-1.amazonaws.com/users/<userid>/<date>/<filename+params>`)
> in the S3 bucket using `../` characters in the filename (for example,
> `test../../../../../../test.jpg`) on the `https://unikrn.com/apiv2/user/upload` endpoint.
> It was possible to upload arbitrary files to the any other directory, and also overwrite
> existing files (which could belong to other users) and resources.

The JSON request turns `filename` into `test2../../../../../../test2.jpg` and step 6
concludes "You now have test2.jpg in the root of your bucket." The vendor's closing note,
byte-true: "Final comment: nothing from that bucket was ever exposed to any user except
the uploader, also nothing in the bucket is there for real archiving purposes." — and the
report's own severity argument (overwrite of files "which could belong to other users")
carried it to $50 (list) and medium rather than informative. Overwrite-ability is what
converts bucket-write into reportable-write.

### 2.3 The delete row (183568)

**FU-183568** (high, $350 (list)) — BuddyPress's crop flow deletes what `original_file`
names after traversal:

> original_file=http%3A%2F%2Flocalhost%2F~sam%2Fwordpress%2Fwp-content%2Fuploads%2Favatars%2F2%2F../../../../../wp-config.php

with the impact sentence byte-true: "The wp-config.php file will be deleted when unlink()
is called and the blog will then be unavailable," and the author's own constraint insight
("(constraining to the upload directory would still allow you to delete, say, other users
avatars"). Deletion has no read-verify-proof duty — the *observable site-down* plus the
DB config name does the proving.

### 2.4 Hybrids and the disclosure exhibit

- **FU-163421** (WP 4.5.3 on nextcloud.com): Subscriber-role admin-ajax repeated thousand-
  fold against `plugin=../../../../../../../../../../dev/random&action=update-plugin`
  ("# exhaust apache" in the poc) — a traversal racing a blocking read; sev recorded by
  resolvable fix (updated WP), body unpaid.
- **FU-158021** ($100 (json), Instacart) — the rmagick error paths, byte-true:
  `Original Error: no decode delegate for this image format `/var/app/20160809T225101Z/tmp/uploads/1470789216-24489-0001-8854/full_redirect_2.svg'`
  — temp-path disclosure priced at exactly the floor the policy put on it ("Firstly,I couldn't
  see anything about Path Disclosure in your policy,so I've decided to report it."). It is
  module 02's error-leak lesson in rmagick dress.

## 3. Techniques (corpus-derived)

1. **Read is priced, existence is priced lower**: full-content read via CDN/processor
   params (122475) top the module ($5,000); existence oracles land at $1,000 (43440).
2. **Encoding rounds**: `%c0%af` overlong UTF-8 through double-decoders (18371); `%5c../`
   backslash-through-glob (3370); OS-mixed `../\` (module 04's 147570) — one ladder, three
   decoders.
3. **Archive-verbs**: tars with symlinks (213558) walk where filenames cannot; check every
   restore/import path for extraction without re-aliasing.
4. **The verb decides the proof**: read → payload URL with `/etc/passwd` bytes; delete →
   wp-config.md gone and site down; write → file at bucket root; DoS → exhaustion script.
5. **State the policy when the class is uncertain** (158021) — a priced path-disclosure row
   exists because the reporter framed it against the missing policy clause.

## 4. Kill-gates

- No traversal row in the corpus was paid for a payload that *only* returned a 200: read
  rows quote bytes (122475's `/etc/passwd`, 213558's step 12), write rows show the landed
  object, delete rows show the consequence.
- The `/uploads/…` symlink read (213558) needed Admin; the corpus prices admin-gated reads
  too, but says so — do not present Admin-only read as anonymous-read.
- 43850's `select_thumb` (module 08 cross-user) shows the boundary: reaching *private
  content* through a traversal-adjacent param is IDOR territory — classify by sink, not
  by the word "upload" in the URL.
