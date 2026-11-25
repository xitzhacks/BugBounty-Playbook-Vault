---
title: "Cache Implementation & Path Tricks — parser differentials, backslashes, NULLs, AppCache"
type: playbook
category: cache-implementation
cwe: "CWE-436"
source_count: 5
full_bodies_available: 5
corpus: "h1-brain disclosed_reports.db (3,673 rows) · sha256 8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4"
list_accessed: "2026-11-07"
note: "Anchors: CACHE-1695604 (Shopify CDN DoS, $3,800), CACHE-1848940 (Linkpop Amazon product poison, $500), CACHE-824753 (Squid CVE-2019-12520)."
---

# Cache Implementation & Path Tricks — the cache and the origin disagree

## 1. Overview

Five rows, **$4,300/2 paid**. This module is about *parser differentials*: the cache and the
origin normalize the URL differently, so one cache key maps to two different resources. That
is all a cache-poisoning primitive needs.

**Case-stock (5 rows / $4,300):**

| Case | Target | Mechanism | Bounty |
|---|---|---|---|
| [CACHE-1695604](https://hackerone.com/reports/1695604) | shopify | backslash-as-slash → 404 cached over every JS asset (DoS) | $3,800 |
| [CACHE-1848940](https://hackerone.com/reports/1848940) | shopify | `/dp/[victim]/../[attacker]` path traversal in a product cache | $500 |
| [CACHE-824753](https://hackerone.com/reports/824753) | ibb (Squid) | URL-decode collisions across domains; CVE-2019-12520 | - |
| [CACHE-334709](https://hackerone.com/reports/334709) | greenhouse | `%00` + long padding changes the cached embed response | - |
| [CACHE-84601](https://hackerone.com/reports/84601) | x (Twitter) | unknown-extension upload → no `Content-Type` → HTML5 AppCache poisoning | - |

## 2. Backslash → 404 → whole-CDN DoS

CACHE-1695604 is the highest-paid row and the simplest mechanism:

> This vulnerability exists as the cache server deals with the backslash as a  frontslash. However, the original server returns a 404 error when a backslash exists in the URL

> So, when an attacker sends a request with replacing the slashes with backslashes for a certain file, the server will return *404 Not Found* error page, and this error will be saved into the cache and any upcoming requests to this file will return *404 Not Found* error.

> This scenario could be exploited to cause DoS on nearly every Shopify website as all the javascript and static files used by Shopify websites are hosted on cdn.shopify.com.

The bounty ($3,800) tracks blast radius, not cleverness.

## 3. Path traversal inside a cache key

CACHE-1848940 abuses a product-link cache: the cached artifact is keyed on the *victim* ID
while the resolved content is the *attacker* ID:

> If an attacker uses a crafted link such as https://amazon.ca/dp/[VICTIM-PRODUCT-ID]/../[ATTACKER-PRODUCT-ID], anyone who will then try to use the "victim" product link https://amazon.ca/dp/[VICTIM-PRODUCT-ID] will be shown the attacker controlled product.

## 4. Library-level: Squid's decode collision

CACHE-824753 (CVE-2019-12520, silently fixed in Squid 4.10) is the class's canonical CVE:

> An attacker can cause Squid to return to the user attacker controlled data, for any domain. From Squid-4.7 and below both HTTPS and FTP could be poisoned. This is due to Squid URL decoding parts of the Request URL and using that to create a hash. Request that decode to the same URL will retrieve the same cached response even if they're from different domains.

## 5. NULL bytes, padding, and browser-side caches

- CACHE-334709: `%00` terminates the customer key but the remainder still reaches
  `Grnhse.Settings` — an injection into a JS config object served from a cacheable endpoint.
- CACHE-84601: upload an unknown extension so the origin omits `Content-Type`, the browser
  sniffs HTML, and an HTML5 AppCache manifest makes the XSS persist client-side:

> Since it allows uploading files, attackers can upload a cache manifest file (HTML5 AppCache) to control the cache behaviors over ton.twitter.com.

## 6. What pays, what doesn't

- Backslash/slash, `%00`, case, double-encoding, and path traversal are the five differentials
  worth testing on every cache. The paid ones here produced *mass* impact (a whole CDN, a
  product catalog), not a single defaced page.
- The two unpaid rows still carry real technique (Squid CVE, Twitter AppCache) — they are
  coordination/VDP rows, not rejected findings.
- Negative control: a differential you cannot key (e.g. per-user `Vary` cookie) is not
  exploitable — stop before you poison anyone.

## 7. Cross-references

- `01_Unkeyed-Header-Reflection.md` — header differentials rather than path differentials.
- `../21_Denial-of-Service/` — the cache-DoS rows overlap that vault's flood module.
- `../SSRF/` — URL-parser differentials are the same primitive in a different sink.
