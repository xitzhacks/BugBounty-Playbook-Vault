---
title: "XXE/XML blogs index — the bibliography: zseano guide (byte-quoted), community writeup corpus (title-linked), payload libraries"
type: bibliography
built: "2026-10-27"
byte_quoted_sources: 1
title_linked_sources: 40
body_fetched_blog_sources: 0 (recorded honestly — none fetched this build)
---

# Blogs Index — XXE/XML

Quote rule (vault-wide): byte-true quotes only from sources actually fetched this build.
Everything else is title + link, marked `title-only`. Nothing below was written from memory.

## 1. BugBountyHunter — "Learning about XML Injection (XXE)" by @zseano (fetched 2026-10-27, byte-true)

URL: `https://www.bugbountyhunter.com/vulnerability/?type=xxe`

The guide's core operational claims, verbatim:

> Anytime you see a file upload feature **always** try upload an .XML file and try to read local files.

> A lot of developers sometimes forget to block .svg files as they are not seen as malicious.

> Mainly .svg files are used for XXE however with that said it **can be** vulnerable if the XML is
> parsed **server side**, for example: you receive a pingback from *their* server IP. It is
> **not vulnerable** when you view it **client side** and receive a pingback from **your ip**.

> Sometimes researchers will upload their .svg with XML, visit it & receive a pingback to their
> collaborator and think it's vulnerable. This is **your browser** rendering the SVG. The idea is
> you want the **server** to process the XML in the SVG when uploading.

> Anytime you see a request with `Content-Type:application/json` simply change it to
> `Content-Type:application/xml` but leave the post data as JSON. Send the request and see if it
> error's expecting valid XML.

> (Tip from @zseano:) Set a match-replace on Burp to change all Content-Type:application/json to
> Content-Type:application/xml. Now browse the website as normal and yes a lot of features may not
> work, but go check for any XML errors on burp!

> As well as this I **highly recommend** you run your own instance of Collaborator as
> `.burpcollaborator.net` is usually blocked.

The guide's exemplar report (title-linked): Rockstar Games emblem editor XXE —
`https://hackerone.com/reports/347139` — *"The feature by default allowed for XML, but researchers
found a way to make this malicious."* (report body NOT fetched this build; H1 returns no body at
that URL — recorded, not reconstructed).

## 2. bugbountyhunting.com community writeup corpus (index fetched 2026-10-27; bodies title-only)

Source: the site's `script.js` data array (28,587 lines) — @payloadartist's community index,
searchable at `https://bugbountyhunting.com/?q=xxe`. Every XXE/XML-relevant row:

| Writeup | Link |
|---|---|
| Full Local File Read via Error Based XXE using XLIFF File | pwn.vg/articles/2021-06/local-file-read-via-error-based-xxe |
| Out of Band XXE in an E-commerce IOS app | 0xgaurang.medium.com/out-of-band-xxe-in-an-e-commerce-ios-app-e22981f7b59b |
| h1{Error based XXE - bug bounty writeup} | f4d3.io/xxe_wild/ |
| XXE-scape through the front door: circumventing the firewall with HTTP request smuggling | honoki.net/2020/03/18/xxe-scape-through-the-front-door-circumventing-the-firewall-with-http-request-smuggling/ |
| $5,005 worth vulnerability Duplicated… Denial of Service - Billion LAUGH Attack (XXE) | (medium, via index) |
| A Tale of Two Formats: Exploiting Insecure XML and ZIP File Parsers to Create a Web Shell | spaceraccoon.dev/a-tale-of-two-formats-exploiting-insecure-xml-and-zip-file-parsers-to-create-a |
| External XML Entity via File Upload (SVG) | 0xatul.github.io/posts/2020/02/external-xml-entity-via-file-upload-svg/ |
| Exploiting Out Of Band XXE using internal network and php wrappers | mahmoudsec.blogspot.com/2019/08/exploiting-out-of-band-xxe-using.html |
| Disclose any main and 3rd party contributors email address and movie local path thru XML file in Plex TV - plex.tv | (medium, via index) |
| Exploiting XXE with local DTD files | mohemiv.com/all/exploiting-xxe-with-local-dtd-files/ |
| From blind XXE to root-level file read access | honoki.net/2018/12/from-blind-xxe-to-root-level-file-read-access/ |
| XSS to XXE in Prince v10 and below (CVE-2018-19858) | corben.io/XSS-to-XXE-in-Prince/ |
| XML XSS in *.yandex.ru by Accident | 0ktavandi.medium.com/… |
| An interesting XXE in SAP. | zain.sabahat.medium.com/… |
| OOB XXE in PrizmDoc (CVE-2018–15805) | mrnikhilsri.medium.com/… |
| SOAP-Based Unauthenticated Out-of-Band XML External Entity (OOB-XXE) in a Help Desk Software | mrnikhilsri.medium.com/… |
| XXE in IBM's MaaS360 Platform | blog.netspi.com/xxe-in-ibms-maas360-platform/ |
| Blind XML External Entities Out-Of-Band Channel Vulnerability : PayPal Case Study | (via index) |
| XXE at Bol.com | jonathanbouman.medium.com/xxe-at-bol-com-7d331186de54 |
| How I Found CVE-2018-8819: Out-of-Band (OOB) XXE in WebCTRL | coalfire.com/The-Coalfire-Blog/June-2018/… |
| From RSS to XXE: feed parsing on Hootsuite | ysx.me.uk/from-rss-to-xxe-feed-parsing-on-hootsuite/ |
| 0day writeup: XXE in uber.com | httpsonly.blogspot.com/2017/01/0day-writeup-xxe-in-ubercom.html |
| Papyal XML Upload Cross Site Scripting Vulnerability | blog.it-securityguard.com/bugbounty-papyal-xml-upload-cross-site-scripting-vulnerability/ |
| XML XSS via POST | zseano.com/blogs/1.html |
| Attacking PowerShell CLIXML Deserialization | truesec.com/hub/blog/attacking-powershell-clixml-deserialization |
| The Hunt for XXE to LFI: How I Uncovered CVE-2019–9670 in a Bug Bounty Program | infosecwriteups.com/the-hunt-for-xxe-to-lfi-… |
| Analysis of CVE-2024-43044 — From file read to RCE in Jenkins through agents | blog.convisoappsec.com/en/analysis-of-cve-2024-43044/ |
| Why nested deserialization is harmful: Magento XXE (CVE-2024-34102) | assetnote.io/resources/research/why-nested-deserialization-is-harmful-magento-xxe-cve-2024-34102 |
| Getting XXE in Web Browsers using ChatGPT | swarm.ptsecurity.com/xxe-chrome-safari-chatgpt/ |
| Hunting on ASPX Application For P1's [Unauthenticated SOAP, RCE, Info Disclosure] | (via index) |
| Weblogic Remote Code Execution (Exploiting CVE-2019-2725) | blog.cybercastle.io/weblogic-remote-code-execution-exploiting-cve-2019-2725/ |

## 3. Payload / technique libraries (canonical, title-linked)

- PayloadsAllTheThings — XXE Injection: `github.com/swisskyrepo/PayloadsAllTheThings/tree/master/XXE Injection` (zseano's guide links it as the payload book)
- Wallarm — "XXE that can bypass WAF protection": `lab.wallarm.com/xxe-that-can-bypass-waf-protection-98f679452ce0/` (zseano's guide links it for filtering work)
- OWASP — XML External Entity (XXE) Processing (cited verbatim inside XXE-248668's own body)

## 4. Post-roster disclosed reports (title-linked, from the hunt-xxe skill's verified citations — outside the mirror's date window)

| Report | Bounty | Class |
|---|---|---|
| h1 505947 — Mail.ru Pulse RSS/Atom feed XXE file read | $6,000 | in-band, feed carrier |
| h1 334488 — Open-Xchange blind XXE via PPTX import | $2,000 | OOXML + external DTD |
| h1 897244 — Zivver SVG profile picture XXE → SSRF | — | SVG server-side parse |
| h1 154096 — Uber Movement blind OOB | $500 | = register row (overlap) |
| CVE-2024-34102 — Adobe Commerce "CosmicSting" | CVSS 9.8 | nested deserialization → XXE → RCE |

## 5. Retrieval honesty

- **Byte-quoted (1):** the BugBountyHunter zseano XXE guide.
- **Index-fetched, body title-only (40):** bugbountyhunting.com rows + §3–§4 — titles and links are
  verbatim from the index; blog bodies were not fetched this build. Before any playbook claim cites
  one of these as *evidence*, fetch the body and re-quote — until then they are a hunt queue, not
  proof.
- **Dead/unreachable:** Rockstar h1 347139 returns no body at the public endpoint (recorded §1).
