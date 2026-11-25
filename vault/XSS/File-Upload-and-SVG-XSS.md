---
title: "File-Upload and SVG XSS"
type: playbook
category: file-upload-and-svg-xss
cwe: "CWE-79", "CWE-434"
source_count: 18
full_bodies_available: 13
summary_only: 5
archive_accessed: 2026-10-12
---

# File-Upload and SVG XSS

## 1. Overview

When a server accepts a file and later **serves it back under the site's own origin**,
the upload becomes an XSS primitive. This holds for SVG, for Flash (historical), and
for any format a browser will parse as active content.

The decisive variable is not the extension or the content — it is the **`Content-Type`
on the response when the file is served**. Serve an SVG as
`Content-Type: image/svg+xml` on your own origin and its `<script>` runs with your
origin's authority. Serve the identical bytes as `text/plain` and it is inert.

This is the one XSS class where the *correct* control is usually a response header
rather than input sanitisation, and the archive documents that conclusion directly.

## 2. Root Cause and Technical Mechanics

### 2.1 The origin-confused upload

```
attacker uploads active-content file
   →  stored on target origin (or a trusted subdomain)
   →  victim opens the direct URL
   →  browser parses it as active content in the target origin
   →  script executes with that origin's authority
```

`FILE-007` (`100565`, Slack) is the canonical report and the best-written in the
archive. The attacker's SVG:

```xml
<svg width="100%" height="100%" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" onload="alert('script')">
  <script type="text/javascript"><![CDATA[
  // some exploit code here
  ]]></script>
  <circle cx="50" cy="50" r="50" fill="green" />
</svg>
```

The researcher's framing: *"A SVG script and other DOM elements is equivalent to the
elements in HTML, so in the example above `alert('script')` will be executed on svg
load event."*

### 2.2 The `Content-Type` differential — the real control

`FILE-012` (`148853`, Paragon Initiative) makes the point explicitly and prescribes
the fix:

> "If you uploads any file thet can use for XSS (HTML,SWF,etc) the content type will
> change to `text/plain; charset=us-ascii`. But for images it will stay the same. so
> if you upload SVG with JS content it will work fine! The
> `Content-Type: image/svg+xml; charset=us-ascii` header will make this attack works."

And the team's own summary states the resolution:

> "The way browsers handle SVG files is terrible. If you're serving SVG files that your
> users can upload, **only allow them to be served as `text/plain`**."

**That single sentence is the correct remediation for the entire class.** It is
sourced, not inferred.

### 2.3 Parser/validator differentials inside the file

`STOR-144` (Shopify, `$5,000`, high) — see
[`Stored-XSS.md`](Stored-XSS.md) §7 — showed a documented SVG element/attribute
allow-list being disabled by an internal DTD entity:

```xml
<?xml version="1.0" encoding="ISO-8859-1"?>
<!DOCTYPE svg [
    <!ENTITY elem "">
]>
<svg onload="alert(document.domain);" height="16" width="16">
  &elem;
</svg>
```

Here the control was an allow-list rather than a header, and the bypass was a
**parser differential**. Both approaches appear in this archive; the header approach is
strictly simpler.

### 2.4 Mime-sniffing XSS on a download path

`CONT-129` (`126197`, Uber, $750) is the mirror image: the file is *not* meant to be
active content, but a browser sniffs it into being HTML.

The researcher's mechanism, verbatim: *"The MIME type of all the `.tar.gz` files is
`application/octet-stream`. Since the MIME type is not specified, browsers will
automatically try to determine the type of the file… Internet explorer scans the first
256 bytes of the file for `html` and if it finds `html` it will interpret the file as
HTML."*

PoC: build a `.tar.gz` containing `<html><script>alert(0)</script></html>` and upload
it to PyPI, mirrored by `archive.uber.com/pypi/simple/`.

**Controls here are `X-Content-Type-Options: nosniff` plus a real `Content-Type`.** The
IE-specific sniffing behaviour is historical; verify current-browser behaviour before
claiming impact, per §9.

### 2.5 Historical Flash sub-class

Five sources in this group involve Flash (`.swf`), including
`66121` (VK.com, IE), `134546` (`*flashmediaelement.swf*`), `44512` (Vimeo moogaloop
player), `91421` (Imgur, `swfupload.swf`), `88508` (Vimeo captions), `182160`
(PortSwigger, IE11), `200351` (Zomato `flashmediaelement.swf`), and
`91421`'s cross-origin SWF upload on Imgur.

**Flash is end-of-life.** These cases are retained because the *methodology* — a
third-party script object (`.swf`) that can be pointed at an attacker's content —
survives in modern forms: browser extensions, WebAssembly modules, PDF viewers, and
`<object>`/`<embed>` embeds. Treat the Flash reports as historical evidence of the
pattern, not as current findings.

## 3. Attack Surface and Preconditions

| Surface | Case | Execution origin |
| --- | --- | --- |
| File upload served on a trusted file domain | `FILE-007` (slack-files.com), `FILE-018` (`community.ubnt.com`), `FILE-012` | the file domain |
| Image galleries | `FILE-018` (Ubiquiti), `FILE-*` (Paragon airship) | the gallery host |
| Avatar / profile images | `FILE-*` | the serving origin |
| App icons (SVG) | `STOR-144` | `partners.shopify.com` + shop admin |
| Package mirrors / downloads | `CONT-129` | the mirror origin |
| Third-party media players | Flash group | any embedding page |

**Preconditions.** Usually just: upload a file, then get a victim to open its direct
URL. `FILE-007` adds a distribution step — the file must be shared to a victim via a
channel or DM, and *"this file can be shared via public link"*, after which the victim
must click the preview.

**A subdomain is not a mitigation by default.** `FILE-007`'s researcher engaged with
this directly and concluded it is a weak control: *"Although `slack-files.com` is a
sandbox domain, there are many ways to gain the victim's trust during phishing attack.
For example, an attacker might render a fake log-in form with 'You need to sign in to
see this file' message."*

## 4. Manual Testing Methodology

1. **Map every upload point** — images, avatars, attachments, exports, imports, icons,
   "custom logo", "theme file".
2. **Upload an SVG with a harmless `onload`** as the first test, since SVG survives most
   image pipelines:
   ```xml
   <svg xmlns="http://www.w3.org/2000/svg" onload="document.title='xss-marker'" width="1" height="1"/>
   ```
3. **Request the file's direct URL** and inspect the response headers:
   ```bash
   # newly authored — run against an authorised target
   curl -sI "$UPLOADED_FILE_URL"
   ```
   Record: `Content-Type`, `Content-Disposition`, `X-Content-Type-Options`.
4. **Judge by the header, not by the extension.** `image/svg+xml` → exploitable.
   `text/plain` → inert. `application/octet-stream` + `nosniff` → inert.
5. **Test the DTD/entity bypass** if the app allow-lists SVG attributes:
   `<!DOCTYPE svg [<!ENTITY elem "">]>` plus `onload=`.
6. **Test the extension/rename differential.** `BROW-006` (`191380`, Twitter,
   `$1,680`) changed `.jpg` → `.html` on the served path and got script execution.
7. **Test mime-sniffing** by embedding HTML-ish bytes at the start of a binary upload;
   confirm whether `nosniff` is present.
8. **Test the sandbox subdomain argument yourself** — check what cookies, storage and
   origins are reachable from the file domain. Do not assume "sandbox" means "isolated".

## 5. Input and Output Context Analysis

The "context" here is the **response context** the browser assigns to the file:

| Served as | Browser behaviour | Result |
| --- | --- | --- |
| `image/svg+xml` | parsed as XML/SVG | **active** — `<script>`, `onload`, `<a href="javascript:">` |
| `text/html` | parsed as HTML | **active** |
| `application/xhtml+xml` | parsed as XHTML | **active** |
| `text/plain` | displayed | inert |
| `application/octet-stream` **with** `nosniff` | downloaded | inert |
| `application/octet-stream` **without** `nosniff` | sniffed | possibly active — see `CONT-129` |
| Inline (no `Content-Disposition: attachment`) | rendered in origin | **active**, and same-origin for storage/cookie purposes |

Note the last row: a file served **inline** on the same origin is worse than one served
as an attachment, because it can also access same-origin storage. `HTML-005`
(`146278`, Nextcloud, log download) is the historical case where Firefox-on-Windows
offered to render a `text/plain` download as HTML — the team explained the mechanism
and concluded *"the document would only be executed locally."*

## 6. Test Cases and Proof-of-Concepts

### 6.1 Historical payloads (verbatim from the cited reports)

| Case | Report | Payload / technique |
| --- | --- | --- |
| FILE-007 | `100565` | `<svg … onload="alert('script')">` with an embedded `<script><![CDATA[…]]></script>` |
| STOR-144 | `232174` | `<!DOCTYPE svg [<!ENTITY elem "">]>` + `<svg onload="alert(document.domain);">` |
| CONT-129 | `126197` | `.tar.gz` whose content begins `<html><script>alert(0)</script></html>` |
| BROW-006 | `191380` | upload a `.jpg`, then request the path with `:large` removed and `%23.html` appended |
| HTML-005 | `146278` | `Host: -->test"<img src=a onerror=alert('xss')>` to poison a log file later downloaded |

### 6.2 Newly authored illustrations (not from the archive)

**Benign SVG marker** — sets `document.title`, no alert, no network:

```xml
<svg xmlns="http://www.w3.org/2000/svg" width="1" height="1"
     onload="document.title='H1XSSMARKER9'">
  <text x="0" y="10">xss-marker</text>
</svg>
```

**DTD/entity probe** (concept sourced from `STOR-144`; verify on your own test host):

```xml
<?xml version="1.0" encoding="ISO-8859-1"?>
<!DOCTYPE svg [ <!ENTITY elem "marker"> ]>
<svg xmlns="http://www.w3.org/2000/svg" width="1" height="1" onload="document.title='&elem;'">
  <text x="0" y="10">&elem;</text>
</svg>
```

**Extension/rename differential** — upload as `.jpg`, then request `path`, `path.jpg`,
`path.svg`, `path.html` and record the `Content-Type` of each.

**Header assertion script** (newly authored):

```bash
# newly authored — run against an authorised target
curl -sI "$FILE_URL" | grep -iE '^(content-type|content-disposition|x-content-type-options)'
```

**Safe proof.** Prefer `document.title='marker'` or a same-origin `fetch` to a
collaborator over `alert(1)`. `FILE-007`'s payload used a placeholder comment
(`// some exploit code here`) rather than a real exfiltration chain, which is the
responsible way to demonstrate the primitive.

## 7. Encoding, Filtering, and Parsing Behavior

| Control observed | Case | Verdict |
| --- | --- | --- |
| Re-serve uploads as `text/plain` | `FILE-012` | **sufficient** — the team's stated fix |
| SVG element/attribute allow-list | `STOR-144` | bypassed by DTD entity |
| `application/octet-stream`, no `nosniff` | `CONT-129` | sniffable → exploitable |
| Extension-based validation | `BROW-006` | bypassed by path rename |
| Image-only MIME preservation | `FILE-012`, `FILE-018` | the *bug* — SVG passes through |

The pattern is consistent: **controls were applied at the file, not at the response.**
Every bypass in this archive came from the browser interpreting the bytes differently
from whatever validated them.

## 8. Impact and Severity Considerations

| Report | Program | Severity | Bounty |
| --- | --- | --- | --- |
| `232174` STOR-144 | Shopify | high | $5,000 |
| `126197` CONT-129 | Uber | not disclosed | $750 |
| `191380` BROW-006 | Twitter | not disclosed | $1,680 |
| `212253` FILE-018 | Ubiquiti | medium | not disclosed |
| `148853` FILE-012 | Paragon Initiative | not disclosed | not disclosed |
| `213227` DOM-015 | Nextcloud | low | $250 (DOM, not upload) |

**Severity drivers, in order:**

1. **Same origin as the main site** > trusted subdomain > third-party host.
   `FILE-007`'s researcher argued the subdomain was a weak mitigation, not a defence.
2. **Cookies/storage reachable** from the serving origin. Check this; do not assume.
3. **Inline vs attachment.** Inline on the main origin is the worst case.
4. **Anonymous reachability.** `FILE-012`'s PoC needs nothing but the URL.

**Honest ceilings.** `HTML-005`'s team concluded the log-file injection
"would only be executed locally" — a correct self-limitation that shaped the rating.

## 9. False Positives and Limitations

- **"It's just an image file" is not a defence.** SVG is an image format and is
  parsed as a document. `FILE-007` demonstrates this directly.
- **"It's on a sandbox domain" needs testing, not asserting.** Measure what the origin
  can actually reach.
- **Stored ≠ served with a dangerous type.** Always inspect the response headers
  before reporting; a `text/plain` re-serve means there is no XSS.
- **Flash findings are historical.** Seven of this group's sources involve Flash.
  Flash is removed from all modern browsers; do not report a `.swf` XSS as a current
  issue without noting this.
- **Mime-sniffing is browser-specific.** `CONT-129`'s 256-byte scan is IE behaviour.
  Verify current browser behaviour, and check for `nosniff`, before claiming impact.
- **Third-party embeds.** Flash-player reports (`44512` Vimeo moogaloop,
  `200351` Zomato `flashmediaelement.swf`, `182160` PortSwigger) are vulnerabilities
  in the *embedding library*, and only in scope if that library is in scope. Attribute
  ownership carefully.
- **Do not report "file upload works" as XSS** — `CONT-129`'s underlying issue was a
  packaging workaround on PyPI, and the mirror merely served it.

## 10. Remediation and Regression Testing

### 10.1 Remediation

Primary control, per the archive's own conclusion (`FILE-012`):

1. **Serve user uploads with a safe `Content-Type`.** `text/plain` is the safest
   general choice for arbitrary user content.
2. **Add `X-Content-Type-Options: nosniff`** on every response that serves user content.
3. **Add `Content-Disposition: attachment`** for anything the user should download
   rather than view.
4. **Serve uploads from a separate, cookie-less origin** with no access to the main
   site's storage. Combine with 1–3; do not rely on it alone.
5. **Set `Content-Security-Policy: sandbox`** on the serving origin or the response
   where supported.
6. **If SVG must be accepted**, sanitise it with a hardened XML parser that rejects
   DTDs and entities, then strip to an allow-list — and verify with the bypass in §6.2.
   `STOR-144` shows allow-lists alone are not sufficient.
7. **Never trust the extension**, and never infer type from it.
8. **Validate by re-parsing, not by filename.** Then serve with the header that matches
   what you actually allowed.

### 10.2 Regression tests

| Test | Asserts |
| --- | --- |
| Upload benign SVG, fetch direct URL, assert `Content-Type` is not `image/svg+xml` | type safe |
| Same, assert `X-Content-Type-Options: nosniff` present | sniffing blocked |
| Same, assert `Content-Disposition` is `attachment` for binary types | inline rendering blocked |
| Upload SVG containing `<!DOCTYPE svg [<!ENTITY …>]>` | rejected or stripped |
| Fetch every uploaded file under `.svg`, `.html`, `.xml`, no-extension variants | type not inferred from extension |
| Embed a binary file containing `<html><script>` at offset 0 | not sniffed as HTML |
| From the serving origin, assert `document.cookie` and `localStorage` are unreachable | origin isolation |
| If SVGs are allowed, run the §6.2 probes against the rendered result | sanitiser holds |

## 11. Historical Bug Bounty Case Studies

Sourced facts only. Inventory: [`references/source-index.md`](references/source-index.md).

---

### FILE-007 — Executing scripts on slack-files.com using SVG

- **Program:** Slack · **Report:** <https://hackerone.com/reports/100565>
- **Archive listing:** <https://h1.security.nathan.sx/slack.html>
- **Weakness:** `XSS - Generic` · **Severity / Bounty:** not disclosed in the source
- **Body inspected:** Yes — **full report**.

**Affected feature:** file uploads on `slack-files.com`.

**Impact framing (researcher, verbatim):** *"Although `slack-files.com` is a sandbox
domain, there are many ways to gain the victim's trust during phishing attack. For
example, an attacker might render a fake log-in form with 'You need to sign in to see
this file' message and trick users into handing out their passwords."*

**Reproduction (as submitted):** create the SVG shown in §6.1 → upload to a channel or
DM → *"Click on message with just uploaded file."* The report also notes the file
*"can be shared via public link. In this case victim should click on image preview to
start script execute."*

**Expected behaviour (researcher):** *"Users expect that after clicking on message with
file they will see this file or file will b[e]…"* — i.e. the user's expectation is an
image, not a script-executing document.

---

### FILE-012 — Stored XSS using SVG

- **Program:** Paragon Initiative Enterprises · **Report:** <https://hackerone.com/reports/148853>
- **Archive listing:** <https://h1.security.nathan.sx/paragonie.html>
- **Weakness:** `XSS - Generic` · **Severity / Bounty:** not disclosed in the source
- **Body inspected:** Yes — **full report**.

**Researcher's mechanism, verbatim:**

> "If you uploads any file thet can use for XSS (HTML,SWF,etc) the content type will
> change to `text/plain; charset=us-ascii`. But for images it will stay the same. so if
> you upload SVG with JS content it will work fine! The
> `Content-Type: image/svg+xml; charset=us-ascii` header will make this attack works."

**Team resolution, verbatim:**

> "The way browsers handle SVG files is terrible. If you're serving SVG files that your
> users can upload, **only allow them to be served as `text/plain`**."

**Why it matters here:** the archive's clearest statement of the correct primary
remediation for this entire class, in a program's own words.

---

### FILE-018 — XSS via SVG file

- **Program:** Ubiquiti Networks · **Report:** <https://hackerone.com/reports/212253>
- **Archive listing:** <https://h1.security.nathan.sx/ubnt.html>
- **Weakness:** `XSS - Generic` · **Severity:** medium · **Bounty:** not disclosed
- **Body inspected:** Yes — **full report**.

**Affected feature:** image upload to the community gallery at
`https://community.ubnt.com/t5/media/gallerypage/user-id/559584`, served via the
image server at `community.ubnt.com/t5/image/serverpage/...`.

**Researcher's description:** *"I was able to upload an svg file to here. so i uploaded
an SVG file with XSS on its code and if the attacker give the link to his victim he can
grab it's victim's cookie. and regarding to your Upload image svg file it uploaded even
it has an error.."*

**Impact as claimed:** cookie theft on the gallery host, from a shareable link.

**Proposed fix (researcher):** *"Dont allow to upload an svg file because attacker can
put his payload to a SVG files."* Rejection-by-type is one valid option;
`FILE-012`'s `text/plain` re-serve is the alternative where SVG must be supported.

---

### STOR-144 — SVG allow-list bypass (Shopify sales channel icon)

- **Program:** Shopify · **Report:** <https://hackerone.com/reports/232174>
- **Severity:** high · **Bounty:** $5,000
- Full case study in [`Stored-XSS.md`](Stored-XSS.md) §11. Included here because the
  root cause is *inside the file format* rather than in the serving headers.

---

### CONT-129 — XSS in archive.uber.com due to MIME sniffing in IE

- **Program:** Uber · **Report:** <https://hackerone.com/reports/126197>
- **Archive listing:** <https://h1.security.nathan.sx/uber.html>
- **Weakness:** `XSS - Generic` · **Bounty:** $750 · **Severity:** not disclosed
- **Body inspected:** Yes — **full report**.

**Affected feature:** the PyPI mirror at `archive.uber.com/pypi/simple/`, which
mirrors uploaded `.tar.gz` files with `Content-Type: application/octet-stream`.

**Mechanism (researcher, verbatim):**

> "The MIME type of all the `.tar.gz` files is `application/octet-stream`. Since the
> MIME type is not specified, browsers will automatically try to determine the type of
> the file. Chrome and Firefox both do so by looking the first few bytes of the file.
> Internet explorer scans the first 256 bytes of the file for `html` and if it finds
> `html` it will interpret the file as HTML. So by creating a `.tar.gz` that contains
> `<html><script>alert(0)</script></html>` one can inject javascript into the page."

**How the upload is achieved (researcher):** *"By default pypi doesn't allow you to
create the `.tar.gz` manually… This can be bypassed by first building the `.tar.gz` by
doing `python setup.py sdist` to build the `.tar.gz` before uploading it with an
external program."*

**Team summary, verbatim:** *"archive.uber.com mirrors pypi. When downloading `.tar.gz`
files from archive.uber.com, the MIME type is `application/octet-stream`. Injecting
`<html><script>alert(0)</script>` into the start of the `.tar.gz` causes an XSS in
Internet Explorer due to MIME sniffing."*

---

### HTML-005 — Log pollution can lead to HTML Injection

- **Program:** Nextcloud · **Report:** <https://hackerone.com/reports/146278>
- **Archive listing:** <https://h1.security.nathan.sx/nextcloud.html>
- **Weakness:** `XSS - Generic` · **Bounty:** not disclosed
- **Body inspected:** Yes — **full report**.

**Affected feature:** the admin **log download** in the Nextcloud admin screen.

**PoC (as submitted):**
```
GET /nextcloud/index.php HTTP/1.1
Host: -->test"<img src=a onerror=alert('xss')>
User-Agent: Mozilla/5.0 (…)
```
Then download the log file and observe execution.

**Root cause (researcher):** the application inserts an HTML comment start tag when HTML
appears in the log, but the researcher *"was able to bypass this protection by inserting
a comment end tag and then the HTML code."*

**Team explanation, verbatim:** the log was delivered as JSON with an attachment
disposition forcing a download, *"However, Firefox running on Microsoft Windows would
offer the user to open the data in the browser as HTML document. Thus any injected data
in the log would be executed. While the document would only be executed locally…"*

### BBH-003 — Upload-filter reconnaissance flow (BugBountyHunter.com guide, read in full)

Source: <https://www.bugbountyhunter.com/guides/?type=fileuploads>. Sequenced
filter-mapping method, quoted from the page (frame assumption: *"the feature you are
testing only allows for .png and .jpg"*):

1. `.txt` first — *"A .txt file is harmless and may not be filtered and may help me
   determine how they handle file uploads and they may be filtering based on malicious
   extensions, rather than valid extensions. If the .txt file is successful, then I
   know the file extension is trusted server side."*
2. Extension-blocked? Re-test inside the multipart body with `filename="malicious.jpg%0d%0a.html"`
   — nulls, `%00`, new lines `%0d%0a`, tabs `%09 %07`; *"using Burp suite you could
   then RIGHT CLICK on %0d%0a in the request, Click Convert Selection and choose URL
   Decode… your payload will be sent url encoded and may bypass filters."*
3. `image/*` allow-lists admit SVG — *"an .svg file is considered an image! This
   would result in XSS"* — including the Laravel `nullable|image|max:1024` trap quoted
   in the guide.
4. Content-Type swap with matching magic bytes: keep `.jpg` plus the `ÿøÿà` JPEG
   header but send `Content-Type: text/html` — *"the server is happy to save your
   upload due to it being .jpg with the correct headers… but then uses the
   Content-Type when viewed"*; pair the header with a matching body opening
   (`<html>code` for text/html, `<?xml>` for application/xml). The guide closes with a
   real program payload: `filename="testing1.jpg"` / `Content-Type: text/html` /
   `ÿØÿà` + `<script>alert(0)</script>`.
5. Filename tricks: `zseano.php/.jpg` (server trims after the slash), `# @ ; \ + & `
   and a trailing backtick, case `.PhP` — and **XSS inside the filename**:
   `filename="<svg onload=confirm()>58832_300x300.jpg"`. Extension-less
   `filename="zseano."` or `.html` forms included with full request examples.
6. Third-party storage: `.amazonaws.com`/`.cloudfront.net` — *"sometimes companies
   will add DNS records to subdomains pointing to their cloud service… media.example.com
   may be used to render images from their S3 bucket"* — test the pinned media
   subdomain before declaring the payload harmless.

Corpus cross-link: FB-610/678/694 in [`Stored-XSS.md`](Stored-XSS.md) exercise the
guide's input-everywhere principle at the header level — the **User-Agent** sent with
the upload request is stored and rendered in the admin portal, so no filename
trickery is required.

## 12. Professional Vulnerability Report Template

````markdown
# Stored XSS via SVG upload on <feature> — served as <content-type>

## Summary
<Feature> accepts SVG uploads. The file is served from <origin> with
`Content-Type: <type>` and no `X-Content-Type-Options`, so SVG script content
executes in <origin> when a victim opens the direct URL.

## Severity
<rating> — <origin trust, cookie/storage reachability, inline vs attachment>

## Affected endpoint
Upload: `<upload endpoint>` · Served from: `<file origin>` · Program: <name>

## Vulnerability details
### Response headers (the defect)
```
$ curl -sI "<uploaded file URL>"
HTTP/2 200
content-type: image/svg+xml
content-disposition: inline
x-content-type-options: <absent>
```

### Root cause
User uploads are served with a content type the browser parses as active content.

## Proof of concept
### Upload (benign marker)
```xml
<svg xmlns="http://www.w3.org/2000/svg" width="1" height="1"
     onload="document.title='H1XSSMARKER9'"><text x="0" y="10">xss-marker</text></svg>
```

### Serve
1. Open `<file URL>` directly. `document.title` becomes `H1XSSMARKER9`.
2. Confirm origin `<origin>` in the console.

### Variants tested
| Path requested | Content-Type | Executes? |
| --- | --- | --- |
| `<url>` | `image/svg+xml` | yes |
| `<url>.html` | — | — |
| `<url>` with `%23.html` | — | — |

## Remediation
Serve uploads as `text/plain`, add `X-Content-Type-Options: nosniff` and
`Content-Disposition: attachment`; or reject SVG. See §10.1.

## Regression tests
<The header assertions in §10.2.>
````

**Reporting discipline.** Always paste the **actual response headers** — the finding
lives there. State whether cookies/storage were reachable from the serving origin
rather than assuming. Disclose Flash or IE-specific dependencies.

## 13. References

- OWASP Cheat Sheet — File Upload: <https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html>
- OWASP — Unrestricted File Upload: <https://owasp.org/www-community/vulnerabilities/Unrestricted_File_Upload/>
- MDN — `X-Content-Type-Options`: <https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Content-Type-Options>
- MDN — SVG as an image (`<img>` is safe; direct navigation is not): <https://developer.mozilla.org/en-US/docs/Web/SVG>
- W3C — Content-Type sniffing / MIME sniffing primer: <https://mimesniff.spec.whatwg.org/>
- Reports cited: <https://hackerone.com/reports/100565>, <https://hackerone.com/reports/148853>,
  <https://hackerone.com/reports/212253>, <https://hackerone.com/reports/232174>,
  <https://hackerone.com/reports/126197>, <https://hackerone.com/reports/146278>,
  <https://hackerone.com/reports/191380>

## 14. Research Gaps and Further Investigation

- **Flash-era reports dominate.** Seven of 18 sources are Flash, which is EOL. The
  *pattern* (a third-party media object pointed at attacker content) persists in
  browser extensions, WASM modules, and PDF viewers, but no source here covers those.
- **`HTML-005`'s Firefox-on-Windows behaviour is unverified today.** The mechanism is
  plausible but has not been re-tested; treat as historical.
- **Untested:** SVG sanitiser bypasses with modern libraries; `Content-Disposition`
  filename injection; polyglot files (valid image *and* valid HTML/SVG); PDF/Office
  active content; `<object>`/`<embed>` with `data:` URIs.
- **Origin-isolation claims were not verified.** Several reports assert a subdomain is
  a "sandbox". None test whether cookies, `localStorage`, or service workers are
  reachable from it. That is a measurable, high-value gap.
- **Suggested original research:** measure, across a sample of file-hosting
  subdomains, what same-origin resources remain reachable. The answer determines
  whether the "separate origin" mitigation is real.
