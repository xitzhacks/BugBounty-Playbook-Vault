---
title: "Upload → stored XSS & served-content execution"
type: playbook
category: upload-stored-xss
cwe: "CWE-434 · CWE-79"
source_count: 7
full_bodies_available: 7
corpus: "h1.security.nathan.sx roster (86 title-arm rows), bodies via hackerone.com/reports/<id>.json"
list_accessed: "2026-11-05"
note: "Anchor bodies: FU-142135 (vk.com upload.php callback eval chain, $1,500 json), FU-97672 (mopub html-as-jpg, $1,120 list), FU-203515 (WP 4.7.2 filename interpolation, $350 list). Claims trace to bodies read 2026-11-05."
---

# Module 03 — the upload lands, then it executes in someone's browser

## 1. Overview

Seven rows, **$3,295/6 paid**. The lane is a serving-side puzzle: an upload endpoint decides
what the *file becomes* on the receiving CDN — extension, content-type, filename. Stored
XSS is the failure mode whenever any one of the three is attacker-controlled while the
serving path renders active content. The corpus's trick ladder mirrors the BBH guide
(blogs-index §1a): extension filters, content-type swaps, filename smuggling — plus the
one genuinely exotic row (142135) where the *parameter attached to the upload endpoint* is
the browser-side sink.

**Case-stock (7 rows / $3,295):**

| Case | Target | Mechanism | Bounty |
|---|---|---|---|
| [FU-142135](https://hackerone.com/reports/142135) | VK.com | `upload.php?act=transport` callback → `parent.{callback}` eval chain | $1,500 (json) |
| [FU-97672](https://hackerone.com/reports/97672) | Twitter (mopub) | html-as-`.jpg` + Content-Type swap on app icons | $1,120 (list) |
| [FU-203515](https://hackerone.com/reports/203515) | WordPress | oversized-file error message interpolates filename (WP 4.7.2) | $350 (list) |
| [FU-97657](https://hackerone.com/reports/97657) | Slack | Java applet `.class` uploaded as `image/jpeg` (slackatwork) | $200 (json) |
| [FU-45368](https://hackerone.com/reports/45368) | Vimeo | FTP upload filename becomes unsanitized video title | $100 (list) |
| FU-155690 | Nextcloud | theming logo/login upload serves attacker HTML | - (list) |
| FU-130591 | Moneybird | stored XSS via SVG upload (summary record) | $25 (list) |

## 2. Anatomy

### 2.1 The serving-stack decision tree

**FU-97672** ($1,120 (list)) states the mopub ladder exactly as the body walks it:

> 1.Go to App settings and select a html file with .jpg extension.
> 2.Intercept the request and change the .jpg to .html and change the content type to
> text/html and it will upload the file.
> 3.Open the link of image in new file and XSS will pop up.

The multipart swap (extension stays, `Content-Type` follows the attacker) hands the CDN an
`.html` it stores like an icon. **FU-97657** ($200 (json)) is the applet variant — same
flow, browser-trust destination:

> Successfully uploaded file Applet3863.class with content type image/jpeg.
>
> The file is available at: http://slackatwork.com/wp-content/uploads/job-manager-uploads/company_logo/2015/11/Applet3863.class.

**FU-45368** ($100 (list)) is the FTP path: Vimeo Pro's engine "read file" naming —
`""><img src = x onerror=alert(2)>".mp4` becomes the auto-video title, because, per the
body, "I think it needs the same sanitization of the name as it's done after the manual
editing."

**FU-155690** records the "php-as-text" boundary honestly (Nextcloud theming): attacker
HTML renders (`it'll execute in client server`), but "Good news,I tried to upload an php
file but server executed that file as text" — XSS confirmed, RCE explicitly excluded.

### 2.2 The parameter beside the endpoint

**FU-142135** ($1,500 (json)) — vk.com's graffiti-to-documents transport. The page embeds
`upload.php?act=transport&…&callback=getUploadSvg`, whose script runs
`parent.{callback}(function(data){ sendData(url, data) })` — and `callback` is attacker-
chosen (the body pegs it to `/^[a-zA-Z0-9]*$/`). Two problems solve the exploit: the
`eval` inside `sendData` runs whatever the POST response returns, so the attacker points
its URL (built from GET params the request controls) at vk's own image proxy
(`upload.php?act=proxy_img&url=…` — hashes harvested via `upload_fails.php` + `role=share`)
carrying an [imagejs](http://jklmnn.de/imagejs/) GIF with JS inside. And `sendData` is
never called directly: the body hunts for a global whose name fits the `callback` pattern,
takes a callback argument, and calls it with an object — the byte-true find:

> Немного `for (... in window)` и такая функция была найдена - `requestAnimationFrame`

—the native frame-scheduler is the only global that fits: `parent.requestAnimationFrame(fn)`
schedules the anonymous function (with `sendData` in its body), the response text hits
`eval` — `alert(document.cookie)` in vk.com context. UA gate recorded in the report: the
chain dies on `/iphone|ipod|ipad|opera mini|opera mobi/i` agents (`ajx2q` is undefined
there) and needs a `requestAnimationFrame` implementation. $1,500 (json).

### 2.3 The filename that was never displayed-as-data

**FU-203515** ($350 (list)) — WP 4.7.1/4.7.2 media upload. The oversized-file error
message is built by string interpolation, not DOM text:

```js
function uploadSizeError( up, file, over100mb ) {
	var message;
	if ( over100mb )
		message = pluploadL10n.big_upload_queued.replace('%s', file.name) + ' ' + pluploadL10n.big_upload_failed.replace('%1$s', '<a class="uploader-html" href="#">').replace('%2$s', '</a>');
	else
		message = pluploadL10n.file_exceeds_size_limit.replace('%s', file.name);
```

with the PoC filename byte-true: `Dinosaurs secret life<img src=x  onerror=alert(1)>.png`.
The media-fix note the body attaches: "any file type can be used (.jar whatever) as the
vuln happens before the type is validated" — the error path fires before validation gates
run, which is why an *error message* is a sink at all.

**FU-130591** ($25 (list)) records the SVG-store fix in one sentence — vendor's summary
voice, the cheapest paid row in the module: "Researcher found a way to add XSS code to SVG
uploads in our software. We have improved our software by preventing SVG and HTML files to
be presented in the webbrowser to prevent XSS attacks."

## 3. Techniques (corpus-derived)

1. **Keep the extension, swap the Content-Type** — when URL-by-no-extension is how the
   CDN files your object, server validates the extension and serves the declared mime
   (97672).
2. **Happy-path image headers**: JPEG `FF D8 FF E0` bytes before `<script>` pass
   signature-scan images (module 01's 191243 + the BBH closing payload) — the same bytes
   that pass upload validation make the stored file render-active where the CDN sniffs.
3. **Handler pages around uploads** carry their own sinks: `upload.php` `callback=`
   parameters, filename echo into errors — quote-with-context and prove with the exact
   endpoint.
4. **FTP/API naming paths** are less-tested than browser upload paths (45368).

## 4. Kill-gates

- Stored-XSS rows need the *serving URL that executes* — 97672/97657's direct URLs are the
  proofs; claims without the served URL die.
- Where RCE-by-PHP is excluded, write the exclusion (155690's "executed that file as
  text" note) — half-proofs priced honestly hold the lane's $25-$100 floor.
