---
title: "Cache Deception & Key Manipulation — storing what belongs to the victim"
type: playbook
category: cache-deception
cwe: "CWE-525"
source_count: 3
full_bodies_available: 3
corpus: "h1-brain disclosed_reports.db (3,673 rows) · sha256 8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4"
list_accessed: "2026-11-07"
note: "Anchors: CACHE-1698316 (Abritel session → ATO), CACHE-260697 (Discourse CSRF token ATO), CACHE-1760213 (WAF bypass stored XSS). No bounty figures in the DB for this module."
---

# Cache Deception — make the cache store a page the attacker may not read

## 1. Overview

Three rows, **$0 in the DB** (no published figures — not evidence of non-payment). Cache
deception flips the poisoning direction: instead of making other users receive *your*
content, you make the cache store *another user's* authenticated content and then read it.

**Case-stock (3 rows):**

| Case | Target | Mechanism | Bounty |
|---|---|---|---|
| [CACHE-1698316](https://hackerone.com/reports/1698316) | expediagroup_bbp (abritel.fr) | `HASESSIONV3` in a cacheable search page → `ha.crumb` → ATO | - |
| [CACHE-260697](https://hackerone.com/reports/260697) | discourse | CSRF token pages without `no-cache` behind CloudFlare → ATO | - |
| [CACHE-1760213](https://hackerone.com/reports/1760213) | expediagroup_bbp | `hav` cookie → cached stored XSS → session extraction | - |

## 2. Session token in a cacheable page

CACHE-1698316 is the cleanest statement of impact:

> I'm able to extract user's session (HASESSIONV3) as it is disclosed in a cacheable page, allowing me to access  the `ha.crumb` token located in  `/traveler/profile/edit`

The delivery trick is the classic static-suffix bait — a search URL that ends in `.jpeg` so
the CDN classifies it as a static asset:

> 1->Visit https://www.abritel.fr/search/keywords:soissons-france-(xss)/minNightlyPrice/x.jpeg?triagethis

Attacker side:

> 1->Visit the same URL using any other browser or do

```bash
curl 'https://www.abritel.fr/search/keywords:soissons-france-(xss)/minNightlyPrice/x.jpeg?triagethis' --compressed | grep -i 'HASESSIONV3'
```

## 3. CSRF token without `no-cache`

CACHE-260697 explains why this is an ATO rather than a token leak:

> The TL;DR of issue is basically: `Discourse instance is vulnerable to account takeover if Discourse is served behind a CloudFlare proxy due to the lack of no-cache headers on pages with CSRF-tokens`.

> You might have heard about the Web Cache Deception attack. The idea is basically to fool the cache proxy, in this case CloudFlare, to cache content which belongs to the victim inside the CloudFlare proxy layer. This makes it possible for anyone in the same CloudFlare region to fetch the leaked data without any authentication.

The precondition is stated just as plainly — this is a *deployment* finding, not an app bug:

> Any URL having a file ending with one of [CloudFlare's mime types](https://support.cloudflare.com/hc/en-us/articles/200172516-Which-file-extensions-does-Cloudflare-cache-for-static-content-) will be cached for the whole region.

## 4. The chained follow-up: WAF bypass + stored XSS

CACHE-1760213 shows the second-order use — once you have cache control over a path, the WAF's
naive filter becomes bypassable by splitting the closing tag:

> abritel.fr has a strong WAF, however the server hides double quotes, allowing to bypass the WAF

> The server blocks `</script`but if I send `</sc"ript>`

> WAF is bypassed and the output is </script>

## 5. What pays, what doesn't

- The module's money is *unrecorded*: none of the three rows carries a bounty figure in the DB.
  Report the impact (session → ATO) rather than the mechanism; the mechanism alone triages as
  informational.
- Preconditions must be written explicitly: CDN in front, static-suffix cache rule, and a page
  that emits a secret without `Cache-Control: no-store`.
- Do not silently poison production caches — the corpus's own reports warn about hitting real
  visitors; use a dedicated account and a throwaway query string.

## 6. Cross-references

- `01_Unkeyed-Header-Reflection.md` — same cache, attacker-to-victim direction.
- `../16_Information-Disclosure/` — the data-exposure framing of the same leak.
- `../Authentication-Session/` — what to do with the stolen session/crumb.
