---
title: "CSRF blogs index — bibliography: zseano guide (byte-quoted), community writeup corpus (title-linked), skill-cited modern cases"
type: bibliography
built: "2026-10-28"
byte_quoted_sources: 1
title_linked_sources: 119 (bugbountyhunting.com index) + 5 skill-cited modern cases
body_fetched_blog_sources: 0 (none fetched this build — recorded honestly)
---

# Blogs Index — CSRF

Quote rule (vault-wide): byte-true quotes only from sources actually fetched this build.
Everything else is title + link, marked `title-only`. Nothing below was written from memory.

## 1. BugBountyHunter — "Learning about Cross Site Request Forgery" by @zseano (fetched 2026-10-28, byte-true)

URL: `https://www.bugbountyhunter.com/vulnerability/?type=csrf`

The guide's operational claims, verbatim:

> I always start with what should contain CSRF tokens, such as updating your account information. I
> want to get a feel for how they are handling security and how testing for something such as a
> blank csrf token may be handled server-side.

**The blank-token → clickjacking chain** (a four-digit bounty, told in full):

> When updating the email of my account, sending a blank csrfToken value would actually cause the
> changes I wanted to make to be reflected but with an error: CSRF_token is invalid. Please submit
> again.. Take note what I say there. The changes I attempted to make were reflected, but weren't
> saved.

> Thanks to the lack of X-FRAME-OPTIONS, I was able to submit the request to update email, then
> iframe the result and clickjack the user into forcing a click onto "submit".

**The POST→GET / GET→POST lane:**

> As well as this, changing the request from POST to GET (and vice versa) and seeing how they
> handle the request as they may only be validating $_POST variables and $_GET works differently.

with the img-tag form: `<img src='https://www.example.com/changePassword?newPassword=oops'>`

**JSON CSRF via text/plain forms — the `=` smuggling lesson:**

> If it ends in =, then it will error, so pay attention to the fact you may need to "smuggle" = in
> your payload. … It should always end with } to close the JSON payload.

> Try and make use of the = character so your payload doesn't end with it.

His real contact-list-exfil PoC carries the full JSON skeleton in an input NAME with the trailing
`value='@gmail.com'` — and the Gmail-plus delivery trick:

> Thanks to the way google mail works, an email sent to [REDACTED_EMAIL] will actually go to
> [REDACTED_EMAIL]. (sic: rendered as [email protected] in page text)

**XML via form post — payload in the NAME, not the value:**

> When it comes to XML a basic XML payload will work, however you are setting it as the NAME, NOT
> the value. … Having a trailing = doesn't matter here.

**Referer/Origin bypass set, verbatim:**

> Some sites only check if it contains their website url, meaning we can just create a
> file/folder on our site to send the CSRF request from. —
> `https://www.yoursite.com/https://www.theirsite.com/`

> Submitting a form inside an iframe will actually give you a blank referer … some developers are
> checking for if the referrer header is found and then executing the anti-csrf code. If no
> referrer is found, no code is executed.

> This will only work on Firefox but if base64 encoded your form above and then submitted it inside
> an iframe, the Origin header is set to null, or sometimes not sent at all. Some sites will only
> check if the header is present ;)

## 2. bugbountyhunting.com community writeup corpus (index fetched 2026-10-28; bodies title-only)

Source: the site's `script.js` data array — @payloadartist's community index. 119 unique CSRF
rows. The ones that map onto this vault's modules (full list preserved in the raw index dump):

**CSRF → Account Takeover lane (§1 of the playbook):**
- Facebook CSRF bug which lead to Instagram Partial account takeover | ysamm.com/?p=379
- Hacking Facebook accounts using CSRF in Oculus-Facebook integration | josipfranjkovic.com/blog/hacking-facebook-oculus-integration-csrf
- Facebook CSRF leading to full account takeover (fixed) | josipfranjkovic.com/blog/facebook-csrf-full-account-takeover
- Stealing Facebook access_tokens using CSRF in device login flow | josipfranjkovic.com/blog/hacking-facebook-csrf-device-login-flow
- [CRITICAL]-class writeups: "CSRF account takeover in a company worth 1B$", "My First CSRF to Account Takeover worth $750", "4x CSRFs Chained For Company Account Takeover" (medium/a-bugz-life)
- CSRF Bypass Using Domain Confusion Leads To ATO | infosecwriteups.com/csrf-bypass-using-domain-confusion-leads-to-ato

**Token-leakage lane (§3):**
- Leaking WordPress CSRF Tokens for Fun, $1337 bounty, and CVE-2017-5489 | ahussam.me/Leaking-WordPress-CSRF-Tokens/
- Leaking Amazon.com CSRF Tokens Using Service Worker API | ahussam.me/Amazon-leaking-csrf-token-using-service-worker/
- rails-ujs will send CSRF tokens to other origins (= roster row XXE-nope, CSRF-49935)
- Victim's Anti CSRF Token could be exposed to Third-party Applications installed on user's Device (500$) | rohitcoder.medium.com

**JSON/GraphQL/Content-Type lanes (§4):**
- [TOKOPEDIA] Site-wide CSRF through GraphQL request | rafiem.github.io/bugbounty/tokopedia/site-wide-csrf-graphql/
- Account Takeover Using CSRF(json-based) | medium.com/@shub66452/account-takeover-using-csrf-json-based
- How I exploit the JSON CSRF with method override technique | medium.com/@secureITmania
- JSON CSRF in Microsoft Bing Maps Collections | infosecwriteups.com
- JSON CSRF attack on a Social Networking Site[Hackerone Platform] | medium.com/@pig.wig45

**CSRF→RCE / chained-critical lane (§6):**
- WordPress 5.1 CSRF to Remote Code Execution | blog.ripstech.com/2019/wordpress-csrf-to-rce/ (and sonarsource mirror)
- CSRF to RCE bug chain in Prestashop v1.7.6.4 and below | blog.stazot.com/prestashop-csrf-to-rce-article/
- SSD Advisory – XenForo RCE Via CSRF | ssd-disclosure.com
- LedgerSMB – CVE-2024-23831: Privilege escalation through CSRF attack on "setup.pl" | twelvesec.com
- Ubiquiti UniFi v3.2.10 Generic CSRF Protection Bypass | rcesecurity.com

**SameSite-era bypasses (§5):**
- Bypass SameSite Cookies Default to Lax and get CSRF | medium.com/@renwa/bypass-samesite-cookies-default-to-lax
- Bypassing SameSite=lax cookie restrictions to preform CSRF resulting to a horizontal privilege escalation | medium.com/@deadoverflow
- The Underrated Bugs: Clickjacking, CSS Injection, Drag-Drop XSS, Cookie Bomb, Login+Logout CSRF | medium.com/@renwa

**CSRF+XSS chains (§6):**
- Self-XSS + CSRF to Stored XSS | medium.com/@renwa
- That Escalated Quickly: From partial CSRF to reflected XSS to complete CSRF to Stored XSS | medium.com/@ciph3r7r0ll
- CSRF + Stored XSS Leading to Full Account Takeover | medium.com/@bag0zathev2
- Chained Bug: XML File Upload to XSS to CSRF to Full Account Take Over (ATO) | systemweakness.com
- A smorgasbord of a bug chain: postMessage, JSONP, WAF bypass, DOM-based XSS, CORS, CSRF… | jub0bs.com/posts/2023-05-05

**Modern research (§5/§6):**
- Exploiting Client-Side Path Traversal to Perform Cross-Site Request Forgery — Introducing CSPT2CSRF | blog.doyensec.com/2024/07/02/cspt2csrf.html
- CSRFing VS Code's Debug Adapter Protocol | mcnulty.blog/posts/dap-csrf
- CSRF Vulnerability In The NodeJS Ecosystem | fortbridge.co.uk/research
- CSRF In JSF 2.0: Predicting CSRF Tokens For Apache MyFaces | certitude.consulting/blog/en/csrf-myfaces-2/
- Cross-Site Request Forgery in Facebook (GraphQL) | philippeharewood.com/facebook-graphql-csrf/

## 3. Skill-cited modern disclosed cases (hunt-csrf skill, verified citations — outside the mirror's 2017 window)

| Case | Bounty | Lane |
|---|---|---|
| GitLab h1 #1122408 — GraphQL mutations via GET | $3,370 | GET-state-change (§4) |
| Stripe Dashboard h1 #1483327 — middleware globally disabled, `enctype=text/plain` JSON | $5,000 | JSON + framework misconfig (§4) |
| GitHub Enterprise Server h1 #1497169 — path traversal past CSRF scope (CVE-2022-23732) | $10,000 | token-scope bypass (§2) |
| Argo CD CVE-2024-22424 — SameSite=Lax moot under sibling-subdomain control + no Content-Type enforcement | — | SameSite/origin (§5) |
| HackerOne #1727221 — social-account-link CSRF → ATO | — | OAuth-link lane (§1) |

## 4. Retrieval honesty

- **Byte-quoted (1):** the BugBountyHunter zseano CSRF guide.
- **Index-fetched, body title-only (119):** bugbountyhunting.com rows + §3 — titles and links are
  verbatim from the index; blog bodies were not fetched this build. Before any playbook claim cites
  one of these as *evidence*, fetch the body and re-quote — until then they are a hunt queue, not
  proof.
- Skill-cited cases (§3) carry the skill's own verified citations (IDs, figures); treat as
  pre-validated but re-verify at report time.
