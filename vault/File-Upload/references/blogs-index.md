---
title: "File Upload blogs index — bibliography: file-upload guides (byte-quoted), community writeup corpus (title-linked, curated 209 of 224), modern hardening-era cases"
type: bibliography
built: "2026-11-05"
byte_quoted_sources: 2 (bugbountyhunter.com file-uploads guide + portswigger.net/web-security/file-upload, fetched live 2026-11-05)
title_linked_sources: 209 curated of 224 raw matches (lane filter; archive-mirror duplicates dropped)
body_fetched_blog_sources: 2 ok · 0 failed
---

# Blogs Index — File Upload

Quote rule (vault-wide): byte-true quotes only from sources actually fetched this build.
Everything else is title + link, marked nothing (§2 is a title-linked corpus, never
quoted). Links are regenerated mechanically from the saved index, never hand-typed.

Curation rule for §2: kept entries whose **lane** matches the class modules (upload-to-RCE,
traversal, inclusion/file-read, arbitrary-file primitives, webshell landing, browser
download abuse); dropped archive-mirror duplicates and one non-writeup; titles whose
technique names another class as the **originator** ("SSRF to Local File Read", "XXE to
LFI", "LFI to RCE"…) are kept here as chain bibliography — the corpus doctrine, same as
every vault in the series: modules teach the upload/traversal/inclusion primitives from
their own lane.

## 1. Fetched and byte-quoted: two file-upload guides

BugBountyHunter ships the class's guide tag `fileuploads` (no `vulnerability/` type page
exists for this class — taxonomy note in source-index §4). §1a is that guide page,
"Learning to test file uploads". §1b is PortSwigger's Web Security Academy file-upload
section — linked directly from the BBH guide's resources block, which makes it a preface of
this build. Both fetched live 2026-11-05 via plain curl, saved verbatim in
`references/archive/` (`bbh-fileuploads-guide.html` + `.txt` transcript,
`portswigger-fileupload.html` + `.txt` transcript).

### 1a. BugBountyHunter — "Learning to test file uploads" (fetched 2026-11-05)

URL: `https://www.bugbountyhunter.com/guides/?type=fileuploads`

The guide's opening frames the lane — filter-first thinking ("an an" sic — byte-true):

> Almost every website offers the ability for a user to upload a file, usually an an image
> for their profile photo or when sharing content. There is a 99% chance the developer has
> created a filter as to what files to allow and what to block, for example they won't want
> you uploading .html files for your profile photo!

The storage-egress warning that module 09's hosting rows (7929, 126374) enact one era
earlier — including the subdomain-rendering caveat:

> When testing file uploads you may find your file is uploaded to a third party domain,
> such as .amazonaws.com or even .cloudfront.net. This means the file has been stored on an
> external cloud service and thus the malicious file would not affect your target domain.
> However sometimes companies will add DNS records to subdomains pointing to their cloud
> service (usually S3 bucket). For example, media.example.com may be used to render images
> from their S3 bucket.

The extension ladder — the .txt probe that nearly every resolved row in this vault ran
(the guide's own italics, transcribed plain — no markup added):

> Testing file extension - Simple, I first test for .txt to check how strict the filter
> actually is. A .txt file is harmless and may not be filtered and may help me determine
> how they handle file uploads and they may be filtering based on
> malicious extensions, rather than valid extensions. If the .txt file is successful, then
> I know the file extension is trusted server side. So let's try cause some impact.

The byte-level Content-Type play (the ÿøÿà glyph pair is byte-true, including the ø):

> Leaving the file extension as .jpg along with the correct image headers (ÿøÿà for
> example), we could simply try changing the Content-Type to text/html.

And the filename smuggling paragraph — straight `won't` and curly `can’t` both byte-true in
this paragraph, exactly as the page renders:

> Testing filenames - Using certain characters in the actual filename can help bypass
> filters. For example what happens if you provide a file name of zseano.php/.jpg - the
> code may see .jpg and allow, but the server actually writes it to the server as
> zseano.php and misses everything after the forward slash. Other common characters to try
> are #, @, ;, \ +, &, `. Don't forget to try something as simple as case sensitive
> filters, .PhP, although uncommon in 2022 in my opinion.
>
> If the filename is saved based on your input, then you could check if the filename is on
> the page anywhere and you can smuggle XSS characters in the filename. Some developers may
> think users can’t save files with < and > in them, but we are simply modifying the
> request via our proxy tool (burp suite).

The guide closes with a real bounty payload — happy-path JPEG header carrying the script
(the payload block's `ÿØÿà` uses capital Ø — byte-true difference from the prose ÿøÿà):

```
------WebKitFormBoundaryoMZOWnpiPkiDc0yV
Content-Disposition: form-data; name="oauth_application[logo_image_file]"; filename="testing1.jpg"
Content-Type: text/html
ÿØÿà
<script>alert(0)</script>
```

### 1b. PortSwigger — Web Security Academy, "File upload vulnerabilities" (fetched 2026-11-05)

URL: `https://portswigger.net/web-security/file-upload`

The definitional frame (all apostrophes straight, byte-true):

> File upload vulnerabilities are when a web server allows users to upload files to its
> filesystem without sufficiently validating things like their name, type, contents, or
> size. Failing to properly enforce restrictions on these could mean that even a basic
> image upload function can be used to upload arbitrary and potentially dangerous files
> instead. This could even include server-side script files that enable remote code
> execution.

Impact decomposition — which is exactly how this vault's ledger splits modules 01/03/05:

> The impact of file upload vulnerabilities generally depends on two key factors:
>         Which aspect of the file the website fails to validate properly, whether that be
>         its size, type, contents, and so on.
>         What restrictions are imposed on the file once it has been successfully uploaded.

(transcript indents preserved). The worst-case sentence:

> In the worst case scenario, the file's type isn't validated properly, and the server
> configuration allows certain types of file (such as .php and .jsp) to be executed as
> code. In this case, an attacker could potentially upload a server-side code file that
> functions as a web shell, effectively granting them full control over the server.

### 2.1 · upload lane (76 of 83 raw)

- How I was rewarded a $1000 bounty after abusing File Upload functionality to Stored XSS Vulnerability leading to credential theft of a vistor in a website. — https://kunalkhubchandani.medium.com/how-i-was-rewarded-a-1000-bounty-after-abusing-file-upload-functionality-to-stored-xss-945a40ac6f94
- Unrestricted File Upload — https://binamrapandey.medium.com/unrestricted-file-upload-e95e1c6fb80
- Reveal the page admin that uploaded a video on the page in comment section — https://lokeshdlk77.medium.com/reveal-the-page-admin-that-uploaded-a-video-on-the-page-in-comment-section-9760e4a31453
- The YouTube bug that allowed unlisted uploads to any channel — https://medium.com/bugbountywriteup/the-youtube-bug-that-allowed-uploads-to-any-channel-3b41c7b7902a
- Unauthenticated File upload Vulnerability on Synology Sub-domain — https://blog.securelayer7.net/unauthenticated-file-upload-vulnerability-on-synology-sub-domain/
- Upload to the future — https://medium.com/bugbountywriteup/upload-to-the-future-1fd38fd502bd
- XSS, RCE &amp; HTML File Upload in same endpoint — https://medium.com/@sa1tama0/xss-rce-html-file-upload-in-same-endpoint-4a03348445f4
- My First Bug: Blind SSRF Through Profile Picture Upload — https://medium.com/@swaysthinking/my-first-bug-blind-ssrf-through-profile-picture-upload-72f00fd27bc6
- RCE via image upload functionality — https://medium.com/@escapesequence89/rce-via-image-upload-functionality-925c902943b8
- Guest Blog: From File Upload to RCE — https://www.synack.com/blog/guest-blog-from-file-upload-to-rce/
- How I was able to see Private Video Uploader Via Facebook Rights Manager.[Responsible Disclosure] — https://medium.com/@kishoretk/how-i-was-able-to-see-identity-of-a-private-video-up-loader-via-rights-manager-responsible-39d996517b6e
- Unrestricted CV File Upload — https://victoni.github.io/unrestricted-file-upload-on-pdf/
- Exploitation of the CVE-2018-15961 – Unrestricted File Upload in Adobe ColdFusion — https://supras.io/exploitation-of-the-cve-2018-15961-unrestricted-file-upload-in-adobe-coldfusion/
- Remote Image Upload Leads to RCE (Inject Malicious Code to PHP-GD Image) — https://medium.com/@asdqwedev/remote-image-upload-leads-to-rce-inject-malicious-code-to-php-gd-image-90e1e8b2aada
- ManageEngine ServiceDesk Plus: Arbitrary File Upload — https://medium.com/@ducanhbui/manageengine-servicedesk-plus-arbitrary-file-upload-4bab0bd00425
- How I Gain Unrestricted File Upload Remote Code Execution Bug Bounty — https://medium.com/@shayboy123/how-i-gain-unrestricted-file-upload-remote-code-execution-bug-bounty-381d0aab0dad
- Uploading Backdoor For Fun And Profit. — https://medium.com/@mohdaltaf163/uploading-backdoor-for-fun-and-profit-rce-db-cred-p1-2cdaa00e2125
- External XML Entity via File Upload (SVG) — https://0xatul.github.io/posts/2020/02/external-xml-entity-via-file-upload-svg/
- Arbitary File Upload too Stored XSS - Bug Bounty — https://m0chan.github.io/2020/02/04/Arbitary-File-Upload-Too-Stored-XSS.html
- Vimeo upload function SSRF — https://medium.com/@dPhoeniixx/vimeo-upload-function-ssrf-7466d8630437
- EXIF Geolocation Data Not Stripped From Uploaded Images — https://medium.com/@souravnewatia/exif-geolocation-data-not-stripped-from-uploaded-images-794d20d2fa7d
- Race Condition that could Result to RCE - (A story with an App that temporary stored an uploaded file within 2 seconds before moving it to Amazon S3) — https://medium.com/bugbountywriteup/race-condition-that-could-result-to-rce-a-story-with-an-app-that-temporary-stored-an-uploaded-9a4065368ba3
- Exploiting File Uploads Pt. 2 – A Tale of a $3k worth RCE. — https://anotherhackerblog.com/exploiting-file-uploads-pt-2/
- Exploiting File Uploads Pt. 1 – MIME Sniffing to Stored XSS #bugbounty — https://anotherhackerblog.com/exploiting-file-uploads-pt1/
- From file upload to email:pass — https://medium.com/@frostnull/from-file-upload-to-email-pass-dc7141aa1ff6
- Antihack.me Blind XSS To PHP File Upload Vulnerability — https://blog.saycure.io/2019/01/24/antihack-xss-2-php-upload/
- Uploading files to api.techprep.fb.com — https://ysamm.com/?p=12
- Abusing ACL Permissions to Overwrite other User’s Uploaded Files/Videos on s3 Bucket — https://medium.com/@armaanpathan/abusing-acl-permissions-to-overwrite-other-users-uploaded-files-videos-on-s3-bucket-162c8877728
- Unauthenticated user can upload an attachment at HackerOne — https://medium.com/@modam3r5/unauthenticated-user-can-upload-an-attachment-at-hackerone-aff2a0c573b8
- How i was able to upload files to api.techprep.fb.com — https://medium.com/@samm0uda/how-i-was-able-to-upload-files-to-api-techprep-fb-com-74308ff767b
- Path traversal while uploading results in RCE — https://blog.harshjaiswal.com/path-traversal-while-uploading-results-in-rce
- Chain The Bugs to Pwn an Organisation ( LFI + Unrestricted File Upload = Remote Code Execution ) — https://medium.com/@armaanpathan/chain-the-bugs-to-pwn-an-organisation-lfi-unrestricted-file-upload-remote-code-execution-93dfa78ecce
- How I hacked Apple.com (Unrestricted File Upload) — https://medium.com/@jonathanbouman/how-i-hacked-apple-com-unrestricted-file-upload-bcda047e27e3
- RCE by uploading a web.config — https://poc-server.com/blog/2018/05/22/rce-by-uploading-a-web-config/
- How I got stored XSS using file upload — https://medium.com/@vis_hacker/how-i-got-stored-xss-using-file-upload-5c33e19df51e
- Unrestricted File Upload to RCE \ —  Bug Bounty POC|https://blog.securitybreached.org/2017/12/19/unrestricted-file-upload-to-rce-bug-bounty-poc/
- How I could have mass uploaded from every Flickr account! — https://ret2got.wordpress.com/2017/10/05/how-i-could-have-mass-uploaded-from-every-flickr-account/
- Papyal XML Upload Cross Site Scripting Vulnerability — https://blog.it-securityguard.com/bugbounty-papyal-xml-upload-cross-site-scripting-vulnerability/
- Waze arbitrary file upload — http://blog.shashank.co/2013/12/waze-arbitrary-file-upload.html
- Arbitrary Upload Any File Extensions - Xelkomy's blog — https://blog.xelkomy.com/posts/Arbitrary-Upload-Any-File-Extetions/
- Spip Preauth RCE 2024: Part 2, A Big Upload — https://thinkloveshare.com/hacking/spip_preauth_rce_2024_part_2_a_big_upload/
- The Art of Intrusion: File Upload Bypass &amp; WAF XSS Evasion in AWS S3 Demystified — https://laburity.com/file-upload-bypass-waf-xss/
- CVE-2023-25365 / XSS via file upload bypass — https://cupc4k3.medium.com/cve-2023-25365-xss-via-file-upload-bypass-ddf4d2a106a7
- Unrestricted File Upload Lead to Stored XSS at Microsoft main domain — https://medium.com/@cavdarbashas/unrestricted-file-upload-lead-to-stored-xss-at-microsoft-main-domain-baa9cadac6bd
- Revisiting an Old Bug: File Upload to Code Execution — https://www.securifera.com/blog/2023/10/25/cve-2021-27198/
- Simple Bugs 0x02: Overwritting Uploaded Files — https://vitorfalcao.com/posts/simple-bugs/overwritting-files/
- Bug Bounty: como encontrei o bug Unrestricted File Upload — https://medium.com/@paulo_mota/bug-bounty-como-encontrei-o-bug-unrestricted-file-upload-dd1a61adc9fd
- Uploading the Webshell using filename of Content-Disposition Header Story! — https://ymohagheghi.medium.com/uploading-the-webshell-using-filename-of-content-disposition-header-story-59ba87752311
- Unrestricted file upload in Rocket TRUfusion Enterprise &lt;= 7.9.6.0 — https://www.synacktiv.com/sites/default/files/2022-11/trufusion_enterprise_unauthenticated_arbitrary_file_write.pdf
- SSRF &amp; LFI In Uploads Feature — https://medium.com/@raymond-lind/ssrf-lfi-in-uploads-feature-a134aa467abf
- 23000$ for Authentication Bypass &amp; File Upload &amp; Arbitrary File Overwrite — https://medium.com/@h4x0r_dz/23000-for-authentication-bypass-file-upload-arbitrary-file-overwrite-2578b730a5f8
- How I abused the file upload function to get a high severity vulnerability in Bug Bounty — https://infosecwriteups.com/how-i-abused-the-file-upload-function-to-get-a-high-severity-vulnerability-in-bug-bounty-7cdcf349080b
- LiveHelperChat - Remote Code Execution via Vulnerable Theme Upload Function — https://arben.sh/research/LiveHelperChat-RCE/
- File Upload Bypass to RCE == $$$$ — https://sagarsajeev.medium.com/file-upload-bypass-to-rce-76991b47ad8f
- How I earned 500$ by uploading a file: write-up of one of my first bug bounty — https://medium.com/@seeu-inspace/how-i-earned-500-by-uploading-a-file-write-up-of-one-of-my-first-bug-bounty-c174cf8ea553
- Filesatck Upload Advisory Summary — https://bishopfox.com/blog/filestack-upload-advisory
- Chained Bug: XML File Upload to XSS to CSRF to Full Account Take Over (ATO) — https://systemweakness.com/chained-bug-xml-file-upload-to-xss-to-csrf-to-full-account-take-over-ato-156409c41b57
- Exploiting a File Upload Vulnerability — A Directory Traversal Attack — https://systemweakness.com/exploiting-a-file-upload-vulnerability-a-directory-traversal-attack-419308cdb059
- XSS \ —  HTML Injection and File Upload Bypass in HUAWEI Subdomain|https://medium.com/@Bishoo97x/xss-html-injection-and-file-upload-bypass-in-huawei-subdomain-64966ba4f4ac
- Achieving Remote Code Execution via Unrestricted File Upload — https://medium.com/@haroonhameed_76621/achieving-remote-code-execution-via-unrestricted-file-upload-6050f360c218
- Remote Code Execution in .tgz File Upload — https://machevalia.blog/blog/remote-code-execution-in-tgz-file-upload
- SQL Injection - The File Upload Playground — https://shahjerry33.medium.com/sql-injection-the-file-upload-playground-6580b089d013
- XSS via file upload — https://sharmajijvs.medium.com/xss-via-file-upload-a2bcc1e5d7f7
- File Upload to RCE — https://ahmed8magdy.medium.com/file-upload-to-rce-538bb4128062
- Unrestricted File Upload Leads to SSRF and RCE — https://itsfading.github.io/posts/Unrestricted-File-Upload-Leads-to-SSRF-and-RCE/
- Bypassed! and uploaded a sweet reverse shell — https://infosecwriteups.com/bypassed-and-uploaded-a-sweet-reverse-shell-d15e1bbf5836
- Exploiting File Upload Functionality in Unique Way. — https://rohit-soni.medium.com/exploiting-file-upload-functionality-in-unique-way-6081b8f658dd
- Account takeover via stored XSS with arbitrary file upload — https://0xbadb00da.medium.com/account-takeover-via-stored-xss-with-arbitrary-file-upload-2774ec6cff51
- Exploiting Unrestricted File Upload to achieve Remote Code Execution on a bug bounty program — https://mase289.medium.com/exploiting-unrestricted-file-upload-to-achieve-remote-code-execution-on-a-bug-bounty-program-85661516712
- Bragging Rights: Killing File Uploads softly — https://infosecwriteups.com/bragging-rights-killing-file-uploads-softly-fba35a4e485a
- XSS in Facebook CDN due to improper filtering of uploaded files extensions — https://ysamm.com/?p=632
- Access files uploaded by employees to internal CDNs / Regenerate URL signature of user uploaded content. — https://ysamm.com/?p=606
- Self-XSS to rXSS via Uploaded File Name — https://enfinlay.github.io//xss/selfxss/upload/bugbounty/2021/02/09/selfxss-to-rxss-via-file-name.html
- XSS, RCE &amp; HTML File Upload in same endpoint — https://sa1tama0.medium.com/xss-rce-html-file-upload-in-same-endpoint-4a03348445f4
- Bypassing file upload filter by source code review in Bolt CMS — https://blog.stazot.com/boltcms-file-upload-bypass/
- Arbitary File Upload Vulnerability in Google Nest (Write Up) — https://blog.evanricafort.com/2015/12/arbitary-file-upload-vulnerability-in.html

### 2.2 · traversal lane (44 of 47 raw)

- Analysis of CVE-2019-14994 – Jira Service Desk Path Traversal leads to Massive Information Disclosure — https://samcurry.net/analysis-of-cve-2019-14994/
- RCE using Path Traversal — https://incogbyte.github.io/pathtraversal/
- Simple PathTraversal bypass — https://medium.com/@frostnull/hi-guys-again-here-bringing-an-experience-to-share-with-you-as-usual-i-will-overshadow-some-f85a1d5a8d8c
- Remote Code Execution via Path Traversal in the Device Metadata Authoring Wizard — https://posts.specterops.io/remote-code-execution-via-path-traversal-in-the-device-metadata-authoring-wizard-a0d5839fc54f
- Traversing the Path to RCE — https://hawkinsecurity.com/2018/08/27/traversing-the-path-to-rce/
- Prezi (map.prezi.com) Path Traversal — https://blog.it-securityguard.com/bug-bounty-prezi-map-prezi-com-path-traversal/
- Directory Traversal, SQL Injection and Server-Side Request Forgery — https://research.aurainfosec.io/disclosure/sagecrm2/
- Oracle Retail Xstore Suite: Pre-authenticated Path Traversal — https://www.synacktiv.com/advisories/oracle-retail-xstore-suite-pre-authenticated-path-traversal
- Path Traversal and Code Execution in CSLA.NET (CVE-2024-28698) — https://www.intruder.io/research/path-traversal-and-code-execution-in-csla-net-cve-2024-28698
- Exploiting Client-Side Path Traversal to Perform Cross-Site Request Forgery - Introducing CSPT2CSRF — https://blog.doyensec.com/2024/07/02/cspt2csrf.html
- The power of Client-Side Path Traversal: How I found and escalated 2 bugs through “../” — https://medium.com/@Nightbloodz/the-power-of-client-side-path-traversal-how-i-found-and-escalated-2-bugs-through-670338afc90f
- From an Innocent Client-Side Path Traversal to Account Takeover — https://kapytein.nl/from-an-innocent-client-side-path-traversal-to-account-takeover
- Wind River VxWorks tarExtract directory traversal vulnerability (CVE-2023-38346) — https://www.pentagrid.ch/en/blog/wind-river-vxworks-tarextract-directory-traversal-vulnerability/
- ZeroQlik: Achieving Unauthenticated Remote Code Execution via HTTP Request Tunneling and Path Traversal — https://www.praetorian.com/blog/qlik-sense-technical-exploit/
- Authenticated Arbitrary File Download (Path Traversal) — https://research.aurainfosec.io/disclosure/papercut/
- Hunting for Nginx Alias Traversals in the wild — https://labs.hakaioffsec.com/nginx-alias-traversal/
- RCE via Path Traversal vulnerability in Onlyoffice CommunityServer &lt; 12.5.2 (CVE-2023-34939) — https://github.com/firsov/onlyoffice/blob/main/CVE-2023-34939-PoC.md
- SharePoint Webpart Property Traversal Vulnerability Analysis (CVE-2022–38053, CVE-2023–21742, CVE-2023–21717) — https://testbnull.medium.com/phân-t%C3%ADch-lỗ-hổng-sharepoint-webpart-property-traversal-cve-2022-38053-cve-2023-21742-bc6931698a5f
- Directory Traversal and LFI worth $400 — https://medium.com/@hritkmjth/directory-traversal-and-lfi-worth-400-c4422785d3bd
- How I Earned $$$ for Excessive Data Exposure Through Directory Traversal Leads to Product Price Manipulation — https://mshibilmp.medium.com/how-i-earned-for-excessive-data-exposure-through-directory-traversal-leads-to-product-price-4582e5371774
- Directory Traversal Vulnerability in Huawei HG255s Products — https://infosecwriteups.com/directory-ttraversal-vulnerability-in-huawei-hg255s-products-dce941a1d015
- CVE-2019–6238: Apple XAR directory traversal vulnerability — https://yilmazcanyigit.medium.com/cve-2019-6238-apple-xar-directory-traversal-vulnerability-9a32ba8b3b7d
- Path Traversal Vulnerability in Payara Platform — https://sec-consult.com/vulnerability-lab/advisory/path-traversal-vulnerability-in-payara-platform/
- Chaining Path Traversal with SSRF to disclose internal git repo data in a Bank Asset — https://blog.niksthehacker.com/chaining-path-traversal-with-ssrf-to-disclose-internal-git-repo-data-in-a-bank-asset-8af4de6f12e
- Directory traversal in PDF viewing application. Leading to full database takeover — https://medium.com/@wrinnsec/directory-traversal-in-pdf-viewing-application-leading-to-full-database-takeover-376e68eadd86
- Practical Client Side Path Traversal Attacks — https://mr-medi.github.io/research/2022/11/04/practical-client-side-path-traversal-attacks.html
- Useless path traversals in Zyxel admin interface (CVE-2022-2030) — https://security.humanativaspa.it/useless-path-traversals-in-zyxel-admin-interface-cve-2022-2030/
- Path Traversal / Arbitrary File Write — https://labs.jumpsec.com/zoho-manageengine-desktop-central-path-traversal-arbitrary-file-write/
- Unrar Path Traversal Vulnerability affects Zimbra Mail — https://blog.sonarsource.com/zimbra-pre-auth-rce-via-unrar-0day/
- Meta's SparkAR RCE Via ZIP Path Traversal — https://blog.fadyothman.com/metas-sparkar/
- How I access other domains in infinityfree.net using Directory Traversal — https://xkurtph.medium.com/how-i-access-other-domains-in-infinityfree-net-using-directory-traversal-4625692d6a2d
- [ Directory Traversal attack ] How did I find it using GitHub — https://web.archive.org/web/20220306040035/https://medium.com/@1337Fenrir/how-did-i-find-directory-traversal-attack-using-github-9b051ed749ca
- Analyzing a PJL directory traversal vulnerability – exploiting the Lexmark MC3224i printer (part 2) — https://research.nccgroup.com/2022/02/18/analyzing-a-pjl-directory-traversal-vulnerability-exploiting-the-lexmark-mc3224i-printer-part-2/
- QRCDR ZeroDay Path Traversal Vulnerability — https://n0lsec.medium.com/qrcdr-path-traversal-vulnerability-bb89acc0c100
- Path Traversal Paradise — https://kuldeep.io/posts/path-traversal-paradise/
- Common Nginx Misconfiguration leads to Path Traversal — https://systemweakness.com/common-nginx-misconfiguration-leads-to-path-traversal-d58701e997bc
- GHSL-2021-1053: Path traversal in Grafana REST API - CVE-2021-43813, CVE-2021-43815 — https://securitylab.github.com/advisories/GHSL-2021-1053_Grafana/
- CVE-2021-43798 - Path Traversal Vulnerability In Grafana — https://j0vsec.com/post/cve-2021-43798/
- How I found the Grafana zero-day Path Traversal exploit that gave me access to your logs — https://labs.detectify.com/2021/12/15/zero-day-path-traversal-grafana/
- Why u should use burp to test Path Traversal Vulnerability and also get RXSS — https://infosecwriteups.com/why-u-should-use-burp-to-test-path-traversal-vulnerability-and-also-get-rxss-2743cbb16a3c
- Path Traversal in MobileSafari — https://feed.bugs.xdavidhu.me/bugs/0006
- Cmd Hijack - a command/argument confusion with path traversal in cmd.exe — https://hackingiscool.pl/cmdhijack-command-argument-confusion-with-path-traversal-in-cmd-exe/
- 5k$ for path traversal on *.paypal-corp.com subdomain — https://twitter.com/0x01alka/status/1001763583447969792
- Facebook FBML DOM Traversal (Information Disclosure) — https://maustin.net/articles/2011-08/FBML_dom_traversal

### 2.3 · inclusion / file-read lane (52 of 57 raw)

- Full Local File Read via Error Based XXE using XLIFF File — https://pwn.vg/articles/2021-06/local-file-read-via-error-based-xxe
- How i got my First Bug Bounty in Intersting Target (LFI to SXSS) — https://ph-hitachi.medium.com/how-i-got-my-first-bug-bounty-in-intersting-target-lfi-to-sxss-58fa5c4f5882
- RCE via LFI Log Poisoning - The Death Potion — https://shahjerry33.medium.com/rce-via-lfi-log-poisoning-the-death-potion-c0831cebc16d
- SSTI to Local File Read — https://www.r29k.com/articles/bb/ssti
- Leveraging LFI to RCE in a website with +20000 users — https://medium.com/bugbountywriteup/leveraging-lfi-to-rce-in-a-website-with-20000-users-129050f9982b
- Stealing local files using Safari Web Share API — https://blog.redteam.pl/2020/08/stealing-local-files-using-safari-web.html
- Local file read via XSS using PDF generate functionality — https://echopwn.com/local-file-read-via-xss-using-pdf-generate-functionality/
- SSRF \ —  Reading Local Files from DownNotifier server|https://www.openbugbounty.org/blog/leonmugen/ssrf-reading-local-files-from-downnotifier-server/
- My First LFI — https://cyberzombie.in/my-first-lfi/
- How I escalated RFI into LFI — http://hassankhanyusufzai.com/RFI_LFI_writeup/
- Bug Bounty - Information Disclosure through error message + WAF Bypass led to Local File Inclusion — https://spenkk.github.io/bugbounty/Local-File-Inclusion/
- Google bug bounty: LFI on production servers in “springboard.google.Com” — $13,337 USD — https://medium.com/@vulnerabilitylabs/bug-bounty-lfi-at-google-com-3c2e17d8c912
- Local File Inclusion in peering.google.com — https://www.updatelap.com/2019/05/local-file-inclusion-in-peeringgooglecom.html
- WRITE UP – GOOGLE BUG BOUNTY: LFI ON PRODUCTION SERVERS in “springboard.google.com” – $13,337 USD — https://omespino.com/write-up-google-bug-bounty-lfi-on-production-servers-in-redacted-google-com-13337-usd/
- Ssrf to Read Local Files and Abusing the AWS metadata — https://medium.com/@pratiky054/ssrf-to-read-local-files-and-abusing-the-aws-metadata-8621a4bf382
- PDFReacter SSRF to ROOT Level Local File Read which led to RCE — https://medium.com/@armaanpathan/pdfreacter-ssrf-to-root-level-local-file-read-which-led-to-rce-eb460ffb3129
- LFI To 10 Servers Pwn — https://nirmaldahal.com.np/lfi-to-10-server-pwn/
- LFI in Apigee portals — https://offensi.com/2019/01/31/lfi-in-apigee-portals/
- Magento – RCE &amp; Local File Read with low privilege admin rights — https://blog.scrt.ch/2019/01/24/magento-rce-local-file-read-with-low-privilege-admin-rights/
- Abusing MySQL clients to get LFI from the server/client — https://www.vesiluoma.com/abusing-mysql-clients/
- Exploiting SSRF like a Boss — Escalation of an SSRF to Local File Read! — https://medium.com/@zain.sabahat/exploiting-ssrf-like-a-boss-c090dc63d326
- Evernote For Windows Read Local File and Command Execute Vulnerabilities — https://paper.seebug.org/737/
- Local file inclusion at IKEA.com — https://medium.com/@jonathanbouman/local-file-inclusion-at-ikea-com-e695ed64d82f
- How we got LFI in apache Drill (Recon like a boss) — https://medium.com/bugbountywriteup/how-we-got-lfi-in-apache-drill-recon-like-a-boss-6f739a79d87d
- #BugBounty — ”Journey from LFI to RCE!!!”-How I was able to get the same in one of the India’s popular property buy/sell company. — https://medium.com/@logicbomb_1/bugbounty-journey-from-lfi-to-rce-how-a69afe5a0899
- LFI to Command Execution: Deutche Telekom Bug Bounty — https://medium.com/@maxon3/lfi-to-command-execution-deutche-telekom-bug-bounty-6fe0de7df7a6
-  Local File Read via XSS in Dynamically Generated PDF  — http://www.noob.ninja/2017/11/local-file-read-via-xss-in-dynamically.html
- From SSRF to Local File Disclosure — https://medium.com/@tungpun/from-ssrf-to-local-file-disclosure-58962cdc589f
- Upgrade from LFI to RCE via PHP Sessions — https://www.rcesecurity.com/2017/08/from-lfi-to-rce-via-php-sessions/
- One Cloud-based Local File Inclusion = Many Companies affected — https://panchocosil.blogspot.com/2017/05/one-cloud-based-local-file-inclusion.html
- Reading local files from Facebook’s server (fixed) — https://josipfranjkovic.blogspot.com/2014/12/reading-local-files-from-facebooks.html
- Magix Bug Bounty: magix.com (RCE, SQLi) and xara.com (LFI, XSS) — https://www.rcesecurity.com/2014/04/magix-bug-bounty-magix-com-rce-sqli-and-xara-com-lfi-xss/
- LFI in Nokia maps — http://blog.shashank.co/2013/10/lfi-in-nokia-maps.html
- IIS welcome page to source code review to LFI! — https://medium.com/@omarahmed_13016/iis-welcome-page-to-source-code-review-to-lfi-23ec581049f5
- The Hunt for XXE to LFI: How I Uncovered CVE-2019–9670 in a Bug Bounty Program — https://infosecwriteups.com/the-hunt-for-xxe-to-lfi-how-i-uncovered-cve-2019-9670-in-a-bug-bounty-program-5668e4afa806
- Unmasking an RFI to LFI Escalation — https://laburity.com/unmasking-an-rfi-to-lfi-escalation/
- Weird LFI and escalating the impact from High to Critical — https://medium.com/@snoopy101/weird-lfi-and-escalating-the-impact-from-high-to-critical-3e804f5366e9
- One LFI bypass to rule them all (using base64) — https://matan-h.com/one-lfi-bypass-to-rule-them-all-using-base64/
- Found SSRF and LFI in Just 10 minutes of using burp! — https://xelkomy.medium.com/found-ssrf-and-lfi-in-just-10-minutes-of-using-burp-492fddef3f3e
- A short tell of LFI from PDF link → Professor the Hunter — https://medium.com/@bughuntar/a-short-tell-of-lfi-from-pdf-link-professor-the-hunter-43a8be853e
- LFI - An Interesting Tweak — https://shahjerry33.medium.com/lfi-an-interesting-tweak-9c5638dbdd1b
- From Shodan Dork to Grafana 📊Local File Inclusion — https://varmaanu001.medium.com/from-shodan-dork-to-grafana-local-file-inclusion-e77dc4cfc264
- Critical Local File Read in Electron Desktop App — https://bugcrowd.com/disclosures/f7ce8504-0152-483b-bbf3-fb9b759f9f89/critical-local-file-read-in-electron-desktop-app
- URL filter bypass, RFI and XSS — https://bergee.it/blog/url-filter-bypass-rfi-and-xss/
- Local File Inclusion (interesting method) — https://captainhoook.medium.com/local-file-inclusion-interesting-method-8263c2cb7cd2
- Write Up – Apple N/A: PII Information, Full Contact List, Main Phone No. And Main Icloud Email Extracted; Bug Patched: Arbitrary Local File Read Via Zip File And Symlinks On Ios Files App. — https://omespino.com/write-up-apple-bug-bounty-n-a-arbitrary-local-file-read-via-zip-file-and-symlinks-usd/
- Write Up – Google VRP N/A: Arbitrary Local File Read (Macos) Via &amp;#x3c;&amp;#x61;&amp;#x3e; Tag And Null Byte (&amp;#x25;&amp;#x30;&amp;#x30;) In Google Earth Pro Desktop App — https://omespino.com/write-up-google-vrp-n-a-arbitrary-local-file-read-macos-via-a-tag-and-null-byte-in-google-earth-pro-desktop-app/
- Bug Bounty Guest Post: Local File Read via Stored XSS in The Opera Browser — https://blogs.opera.com/security/2021/09/bug-bounty-guest-post-local-file-read-via-stored-xss-in-the-opera-browser/
- Bypassing LFI (Local File Inclusion) — https://medium.com/@abhishake21/bypassing-lfi-local-file-inclusion-ebf4274e7027
- PHP fopen() function to local file inclusion — https://xhzeem.me/posts/PHP-fopen-function-to-local-file-inclusion/read/
- Spilling Local Files via XXE when HTTP OOB fails — https://blog.noob.ninja/spilling-local-files-via-xxe-when/
- Local File XSS Vulnerability in Wordpress.com (Write Up) — https://web.archive.org/web/20210511011807/https://blog.evanricafort.com/2015/12/local-file-xss-vulnerability-in.html

### 2.4 · arbitrary-file lane (35 of 35 raw)

- Arbitrary File Write On Client By ADB Pull — https://daeken.svbtle.com/arbitrary-file-write-by-adb-pull
- Chaining multiple low-impact bugs to arbitrary file read in GitLab — https://blog.nyangawa.me/security/GitLab-Local-File-Read/
- From blind XXE to root-level file read access — https://honoki.net/2018/12/from-blind-xxe-to-root-level-file-read-access/
- Arbitrary File Read in one of the largest CRMs — https://medium.com/@mantissts/arbitrary-file-read-in-one-of-the-largest-crms-658caa2f05d2
- Escalating XSS in PhantomJS Image Rendering to SSRF/Local-File Read — https://buer.haus/2017/06/29/escalating-xss-in-phantomjs-image-rendering-to-ssrflocal-file-read/
- Analysis of CVE-2024-43044 — From file read to RCE in Jenkins through agents — https://blog.convisoappsec.com/en/analysis-of-cve-2024-43044/
- From Limited file read to full access on Jenkins (CVE-2024-23897) — https://xphantom.nl/posts/crypto-attack-jenkins/
- ZSATrayManager Arbitrary File Deletion (CVE-2023-41969) — https://medium.com/csg-govtech/catch-me-if-you-can-local-privilege-escalation-in-zscaler-client-connector-7ad997bd7058
- Devfile file write vulnerability in GitLab — https://gitlab-com.gitlab.io/gl-security/security-tech-notes/security-research-tech-notes/devfile/
- CVE-2023-36049: Microsoft .NET CRLF Injection Arbitrary File Write/deletion Vulnerability — https://www.zerodayinitiative.com/blog/2024/3/6/cve-2023-36049-microsoft-net-crlf-injection-arbitrary-file-writedeletion-vulnerability
- Silverpeas App: Multiple CVEs leading to File Read on Server — https://rhinosecuritylabs.com/research/silverpeas-file-read-cves/
- Partial File Read in phpList &lt;= 3.6.12 (CVE-2023-35834) — https://www.synacktiv.com/sites/default/files/2023-07/synacktiv-phplist-partial-file-read.pdf
- LibreOffice Arbitrary File Write (CVE-2023-1883) — https://secfault-security.com/blog/libreoffice.html
- Avast Anti-Virus privileged arbitrary file create on virus restore (CVE-2023-1586) — https://the-deniss.github.io/posts/avast-privileged-arbitrary-file-create-on-restore/
- Avast Anti-Virus privileged arbitrary file create on virus quarantine (CVE-2023-1585 and CVE-2023-1587) — https://the-deniss.github.io/posts/2023/04/26/avast-privileged-arbitrary-file-create-on-quarantine.html
- PHP Filter Chains: File Read From Error-based Oracle — https://www.synacktiv.com/publications/php-filter-chains-file-read-from-error-based-oraclel
- A New Vector For “Dirty” Arbitrary File Write to RCE — https://blog.doyensec.com/2023/02/28/new-vector-for-dirty-arbitrary-file-write-2-rce.html
- EoP via Arbitrary File Write/Overwite in Group Policy Client “gpsvc” – CVE-2022-37955 — https://decoder.cloud/2023/02/16/eop-via-arbitrary-file-write-overwite-in-group-policy-client-gpsvc-cve-2022-37955/
- Doing it the researcher’s way: How I Managed to Get SSTI (Server Side Template Injection) which lead to arbitrary file reading on One of the Leading Payment Systems in Asia — https://medium.com/@jazdprince/doing-it-the-researchers-way-how-i-managed-to-get-ssti-server-side-template-injection-which-66b239ca0104
- Arbitrary File Corruption: End - to - End Encrypted Messaging Application — https://nmochea.medium.com/arbitrary-file-corruption-end-to-end-encrypted-messaging-application-674963dceef8
- CVE-2022-26113: FortiClient Arbitrary File Write As SYSTEM — https://rhinosecuritylabs.com/research/cve-2022-26113-forticlient-arbitrary-file-write-as-system/
- (ZOHO) Manage Engine Desktop Central – SQL Injection / Arbitrary File Write — https://labs.jumpsec.com/zoho-manage-engine-desktop-central-sql-injection-arbitrary-file-write/
- CVE-2021-3779: Ruby-MySQL Gem Client File Read (FIXED) — https://www.rapid7.com/blog/post/2022/06/28/cve-2021-3779-ruby-mysql-gem-client-file-read-fixed/
- CVE-2022-31749: WatchGuard Authenticated Arbitrary File Read/Write (Fixed) — https://www.rapid7.com/blog/post/2022/06/23/cve-2022-31749-watchguard-authenticated-arbitrary-file-read-write-fixed/
- Abusing Arbitrary File Deletes To Escalate Privilege And Other Great Tricks — https://www.zerodayinitiative.com/blog/2022/3/16/abusing-arbitrary-file-deletes-to-escalate-privilege-and-other-great-tricks
- Technical Advisory – Apple macOS XAR – Arbitrary File Write (CVE-2022-22582) — https://research.nccgroup.com/2022/03/15/technical-advisory-apple-macos-xar-arbitrary-file-write-cve-2022-22582/
- VMware vCenter earlier versions (7.0.2.00100) has unauthorized arbitrary file read + ssrf + xss vulnerability — https://github.com/l0ggg/VMware_vCenter
- Apple XAR – Arbitrary File Write (CVE-2021-30833) — https://research.nccgroup.com/2021/10/28/technical-advisory-apple-xar-arbitrary-file-write-cve-2021-30833/
- OVE-20210809-0001 Visual Studio Code .ipynb Jupyter Notebook XSS (Arbitrary File Read) — https://github.com/justinsteven/advisories/blob/master/2021_vscode_ipynb_xss_arbitrary_file_read.md
- Escalating XSS to Arbitrary File Read — https://www.pethuraj.com/blog/escalating-xss-to-arbitrary-file-read/
- GitLab Arbitrary File Read &amp; Write through Kroki - CVE-2021-22203 — https://ledz1996.gitlab.io/blog/writeups/CVE-2021-22203-gitlab-arbitrary-file-read-write-through-kroki
- Google Photos : Theft of Database &amp; Arbitrary Files Android Vulnerability — https://servicenger.com/blog/mobile/google-photos-theft-of-database-arbitrary-files-android-vulnerability/
- Facebook Messenger Desktop App Arbitrary File Read — https://medium.com/@renwa/facebook-messenger-desktop-app-arbitrary-file-read-db2374550f6d
- OpenEMR 5.0.1.3 Arbitrary File Actions — https://jsecu.github.io/2020/11/17/openemr/
- $$ Bounties for Unauthenticated file read in Cisco ASA CVE-2020–3452 — https://infosecwriteups.com/bounties-for-unauthenticated-file-read-in-cisco-asa-cve-2020-3452-9a0b9143370e

### 2.5 · webshell lane (2 of 2 raw)

- A Tale of Two Formats: Exploiting Insecure XML and ZIP File Parsers to Create a Web Shell — https://spaceraccoon.dev/a-tale-of-two-formats-exploiting-insecure-xml-and-zip-file-parsers-to-create-a
- How i found web shell on AntiHack.me and Awarded Gold Coin And SWAG — https://rudr4sarkar.blogspot.com/2019/01/how-i-found-web-shell-on-antihackme-and.html

### 2.6 · dropped records (15, with reason)

- *(dropped)* Should you be concerned about LastPass uploading your passwords to its server? — https://palant.info/2019/03/18/should-you-be-concerned-about-lastpass-uploading-your-passwords-to-its-server/ · policy commentary (LastPass), not a vulnerability writeup
- *(dropped)* SSRF &amp; LFI In Uploads Feature — https://web.archive.org/web/20220315080229/https://medium.com/@raymond-lind/ssrf-lfi-in-uploads-feature-321d83b93ec0 · archive-mirror duplicate of the asdqwedev PHP-GD writeup
- *(dropped)* Unrestricted CV File Upload — https://web.archive.org/web/20200601005729/https://vict0ni.me/unrestricted-file-upload-on-pdf/ · archive-mirror duplicate of the vict0ni CV upload writeup
- *(dropped)* Remote Image Upload Leads to RCE (Inject Malicious Code to PHP-GD Image) — https://asdqw3.medium.com/remote-image-upload-leads-to-rce-inject-malicious-code-to-php-gd-image-90e1e8b2aada · archive-mirror duplicate of the asdqwedev PHP-GD writeup
- *(dropped)* External XML Entity via File Upload (SVG) — https://web.archive.org/web/20200305081812/https://0xatul.github.io/posts/2020/02/external-xml-entity-via-file-upload-svg/ · archive-mirror duplicate of the 0xatul XMLEntity-SVG writeup
- *(dropped)* Arbitary File Upload too Stored XSS - Bug Bounty — https://web.archive.org/web/20200515015005/https://m0chan.github.io/2020/02/04/Arbitary-File-Upload-Too-Stored-XSS.html · archive-mirror duplicate of the m0chan stored-XSS writeup
- *(dropped)* Papyal XML Upload Cross Site Scripting Vulnerability — https://wss.sh/en/blog/bugbounty-papyal-xml-upload-cross-site-scripting-vulnerability/ · archive-mirror duplicate of the Papyal XML upload writeup
- *(dropped)* RCE using Path Traversal — https://web.archive.org/web/20201120053519/https://incogbyte.github.io/pathtraversal/ · archive-mirror duplicate of the incogbyte traversal writeup
- *(dropped)* Traversing the Path to RCE — https://blog.hawkeyesecurity.com/2018/08/27/traversing-the-path-to-rce/ · archive-mirror duplicate of the hawkinsecurity writeup
- *(dropped)* Prezi (map.prezi.com) Path Traversal — https://wss.sh/en/blog/bug-bounty-prezi-map-prezi-com-path-traversal/ · archive-mirror duplicate of the Prezi writeup blog link
- *(dropped)* LFI to 10 servers pwn — https://nirmaldahal.com.np/lfi-to-10-servers-pwn/ · duplicate slug of nirmaldahal LFI-to-10-servers
- *(dropped)* Bug Bounty - Information Disclosure through error message + WAF Bypass led to Lo — https://arben.sh/bugbounty/Local-File-Inclusion/ · mirror re-post of the spenkk error+WAF LFI writeup
- *(dropped)* LFI to 10 servers pwn — https://nirmaldahal.com.np/posts/2017/12/lfi-to-10-servers-pwn/ · duplicate slug of nirmaldahal LFI-to-10-servers
- *(dropped)* Upgrade from LFI to RCE via PHP Sessions — https://web.archive.org/web/20220818204507/https://www.rcesecurity.com/2017/08/from-lfi-to-rce-via-php-sessions/ · archive-mirror duplicate of the rcesecurity PHP-session writeup
- *(dropped)* One Cloud-based Local File Inclusion = Many Companies affected — http://panchocosil.blogspot.com/2017/05/one-cloud-based-local-file-inclusion.html · archive-mirror duplicate of the panchocosil writeup
## 3. Modern hardening-era cases (post-2017; bibliography only, never class counts)

The mirror corpus closed at the 2017-09-12 freeze. The upload class's modern stars — and
the hardening that changed the lane (signed uploads, blob/egress validation, per-user
isolation) — live here:

- **Webshell via File Upload on ecjobs.starbucks.com.cn** — HackerOne report 506646 (the
  BBH guide's own "Disclosed report" pointer, linked from §1a)
- **$23,000 for Authentication Bypass & File Upload & Arbitrary File Overwrite** — h4x0r_dz (medium.com/@h4x0r_dz)
- **Exploiting File Uploads Pt. 2 – A Tale of a $3k worth RCE** — anotherhackerblog.com
- **Exploiting File Uploads Pt. 1 – MIME Sniffing to Stored XSS** — anotherhackerblog.com
- **How I hacked Apple.com (Unrestricted File Upload)** — Jonathan Bouman
- **Google bug bounty: LFI on production servers in “springboard.google.Com” — $13,337 USD** — vulnerability-labs medium post
- **WRITE UP – GOOGLE BUG BOUNTY: LFI ON PRODUCTION SERVERS — $13,337 USD** — omespino
- **Local file inclusion at IKEA.com** — Jonathan Bouman
- **How I found the Grafana zero-day Path Traversal exploit** — labs.detectify.com (2021)
- **$$ Bounties for Unauthenticated file read in Cisco ASA CVE-2020–3452** — infosecwriteups
- **Facebook Messenger Desktop App Arbitrary File Read** — renwa (medium.com/@renwa)
- **The Hunt for XXE to LFI: CVE-2019–9670 in a Bug Bounty Program** — infosecwriteups
- **Zimbra pre-auth RCE via unrar** — blog.sonarsource.com (2022)
- **Exploiting Client-Side Path Traversal to Perform CSRF — CSPT2CSRF** — blog.doyensec.com (2024)
- **LiveHelperChat - Remote Code Execution via Vulnerable Theme Upload Function** — arben.sh
- **Path traversal while uploading results in RCE** — blog.harshjaiswal.com

Full links for these sixteen live in the §2 lists above (mechanically regenerated); §3
fixes their order and their role: the class's post-mirror price ladder runs
upload-bypass→stored-XSS at the low end, web shell / overwrite / file-write in the middle,
five-figure traversal and pre-auth RCE per product CVE at the top.

## 4. Selection record

- §1: 2 sources fetched, both 200, both archived verbatim. Quotes byte-true against the
  saved HTML/transcript pairs (`bbh-fileuploads-guide.txt`, `portswigger-fileupload.txt`);
  recorded byte facts: guide "an an" (sic); guide mixes straight `won't` with curly `can’t`
  in one paragraph; prose `ÿøÿà` vs payload `ÿØÿà` glyph difference kept as-is.
- §2: 224 raw title matches from the 7,103-entry index → 209 curated. 15 drops, every drop
  justified in §2.6 (14 archive-mirror/slug duplicates + 1 non-writeup). Zero curation
  silence — no entry removed without a reason line.
- §3: 16 modern cases, chosen for (a) a price or CVE anchor, (b) a mechanism this vault's
  modules cover, (c) era spread 2018→2024. No bounties are float-mixed into class counts.
- §2 links regenerated from `bugbountyhunting.com`'s own data array — never hand-typed.
