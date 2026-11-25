---
title: "Adjacent + unclassified — cache poisoning, prototype pollution, and the 19 merge rows the bucket missed"
type: playbook
category: adjacent-and-unclassified
cwe: "CWE-400 (adjacent classes: CWE-524/1321/639)"
source_count: 35
full_bodies_available: 33
corpus: "h1-brain disclosed_reports.db (3,673 rows; sha256 8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4) · bucket 'dos' = 221 rows + 19 unclassified-merge rows (weakness None in DB)"
list_accessed: "2026-11-07"
note: "Two lanes in one last module: _adjacent (16 bucket rows) + _adjacent_unclassified (19 merge rows). Anchor bodies: DOS-1096609 ($2,900), DOS-409370 ($2,500), DOS-185775 ($10,000), DOS-2520679 ($5,420). Two GHSL rows are metadata-only. Quotes byte-true to references/archive/DOS-bodies-full-dump.txt."
---

# Adjacent + unclassified — the vault's negative space and its bucket-filter misses

## 1. Overview

Thirty-five rows, **$42,504/14 paid** — the vault's final module, which is two lanes
by design. The **adjacent lane (16 rows, $5,500/3)** holds bucket rows whose *impact* is
DoS but whose *mechanism* belongs to another class: cache poisoning (1096609 $2,900,
409370 $2,500, plus the greenhouse/automattic/gitlab/exodus/security cluster), lodash
prototype pollution (380873, 864701), a CSRF-framed WordPress DoS (153093), a 2FA
verification gap (649533), and a CTF write-up misfiled as DoS (1066851). The
**unclassified-merge lane (19 rows, $37,004/11)** holds rows the classifier's
`unclassified` pool (468 rows; 506 in `unlabeled_rows.json`) contained and
`module_map_all.json` promoted into dos under `_adjacent_unclassified` — every one has
`weakness_name None` in the DB, which is exactly why the 221-row bucket filter missed
them. Together they are the vault's honesty shelf: the adjacent pool shows what the
class attracts when the label is only the impact, and the merge pool shows what a
label-only bucket systematically drops.

**Case-stock (35 rows / $42,504):**

| Case | Target | Mechanism | Bounty |
|---|---|---|---|
| [DOS-185775](https://hackerone.com/reports/185775) | shopify-scripts | Decimal.new(self) → empty mpd_t assertion crash | $10,000 |
| [DOS-2520679](https://hackerone.com/reports/2520679) | ibb | Range header → giant response (CVE-2024-26141) | $5,420 |
| [DOS-1804128](https://hackerone.com/reports/1804128) | ibb | PermitScrubber SVG-attribute backtracking (CVE-2022-23514) | $4,000 |
| [DOS-1096609](https://hackerone.com/reports/1096609) | shopify | Host: :1337 poison → persistent cached DoS | $2,900 |
| [DOS-2584376](https://hackerone.com/reports/2584376) | ibb | Accept-Encoding/Language ReDoS, unauthenticated | $2,642 |
| [DOS-2071556](https://hackerone.com/reports/2071556) | ibb | Rack header parsing slow-path (CVE-2023-27539) | $2,540 |
| [DOS-2071561](https://hackerone.com/reports/2071561) | ibb | Ruby URI ReDoS after incomplete CVE-2023-28755 fix | $2,540 |
| [DOS-409370](https://hackerone.com/reports/409370) | security | X-Forwarded-Host/Port poison → persistent redirect block | $2,500 |
| [DOS-880187](https://hackerone.com/reports/880187) | security | group-rename near-infinite loop burns CPU/mem | $2,500 |
| [DOS-1627159](https://hackerone.com/reports/1627159) | ibb | Rack BROKEN_QUOTED multipart ReDoS (CVE-2022-30122) | $2,400 |
| [DOS-2939104](https://hackerone.com/reports/2939104) | ibb | IPv6 validation unbounded length (CVE-2024-42005/56374) | $2,162 |
| [DOS-1061211](https://hackerone.com/reports/1061211) | github-security-lab | GHSL Android NFE query (metadata-only body) | $1,800 |
| [DOS-801230](https://hackerone.com/reports/801230) | github-security-lab | GHSL CodeQL ReDoS query (metadata-only body) | $1,000 |
| [DOS-1173684](https://hackerone.com/reports/1173684) | nextcloud | shareinfo endpoint unprotected (weak adjacency) | $100 |
| [DOS-153093](https://hackerone.com/reports/153093) | wordpress | WordPress DoS via CSRF (advisory-only body) | - |
| [DOS-159820](https://hackerone.com/reports/159820) | instacart | list-image upload issues | - |
| [DOS-204774](https://hackerone.com/reports/204774) | shopify-scripts | proc{return} in ensure → sandbox segfault | - |
| [DOS-216615](https://hackerone.com/reports/216615) | shopify-scripts | N *case ... ary_concat segfault | - |
| [DOS-326639](https://hackerone.com/reports/326639) | greenhouse | for[] array reflected into cached JS settings | - |
| [DOS-350847](https://hackerone.com/reports/350847) | greenhouse | 1024-char request-URI limit bypassed via UTF-8 expansion | - |
| [DOS-380873](https://hackerone.com/reports/380873) | nodejs-ecosystem | lodash merge constructor.prototype pollution | - |
| [DOS-431561](https://hackerone.com/reports/431561) | rails | Rack multipart worse-than-linear: 10k parts → 15–25s | - |
| [DOS-496113](https://hackerone.com/reports/496113) | notepad-plus-plus | Notepad++ header A*500 crash | - |
| [DOS-591302](https://hackerone.com/reports/591302) | automattic | Origin echoed into cached Access-Control-Allow-Origin | - |
| [DOS-649533](https://hackerone.com/reports/649533) | moneybird | 2FA enable without email verify (adjacent noise) | - |
| [DOS-752010](https://hackerone.com/reports/752010) | nordsecurity | load-scripts.php ~3MB unauth amplification (CVE-2018-6389) | - |
| [DOS-753491](https://hackerone.com/reports/753491) | yelp | blog.yelp.com load-scripts.php (CVE-2018-6389) | - |
| [DOS-783356](https://hackerone.com/reports/783356) | localizejs | unbounded password length → DoS | - |
| [DOS-864701](https://hackerone.com/reports/864701) | nodejs-ecosystem | lodash 4.17.15 prototype pollution | - |
| [DOS-921704](https://hackerone.com/reports/921704) | automattic | cached CORS Allow-Origin poison (duplicate family of 591302) | - |
| [DOS-993582](https://hackerone.com/reports/993582) | cs_money | single search-bar request DoS on 3d.cs.money | - |
| [DOS-1066851](https://hackerone.com/reports/1066851) | h1-ctf | CTF write-up miscategorized as DoS | - |
| [DOS-1160407](https://hackerone.com/reports/1160407) | gitlab | x-http-method-override poisons Varnish-cached assets | - |
| [DOS-1173153](https://hackerone.com/reports/1173153) | exodus | Authorization header poisons Cloudflare-cached downloads | - |
| [DOS-1181946](https://hackerone.com/reports/1181946) | security | x-forwarded-scheme poisons Cloudflare cached JS | - |
## 2. The adjacent lane: DoS by cache poisoning

The cache-poisoning rows are the adjacent lane's money and its clearest chain into the
sibling vault. DOS-1096609 ($2,900, `themes.shopify.com`) poisons a shared cache with a
`Host: :1337` header so *every* subsequent visitor gets an unopened port:

> Poison your cache with HTTP header Host header with arbitrary PORT which is not opened. This attack may lead to Denial of Services

DOS-409370 ($2,500, HackerOne itself) is the one-liner:

> An attacker can persistently block access to any/all redirects on www.hackerone.com by using cache poisoning with the X-Forwarded-Port or X-Forwarded-Host headers to redirect users to an invalid port.

The rest of the cluster is the same technique against different cache keys: the
greenhouse `for[]` array reflected into cached JS (326639), the UTF-8-expansion bypass
of the 1024-char request-URI fix (350847), the WP-JSON `Origin`-echo poison (591302,
921704), the Varnish/GCP `x-http-method-override` poison (1160407), the Cloudflare
`Authorization` (1173153) and `x-forwarded-scheme` (1181946) poisons. DOS-591302's
opening sentence is the class thesis:

> The WP-JSON implementation on some wordpress.com websites I've tested is vulnerable to denial of service where by an attacker can provide an arbitrary `Origin` header in the request, which is then echoed back in the response via the `Access-Control-Allow-Origin` header, which is cached and served to other requests.

These rows stay in this vault because their *impact* is the DOS class — but every one of
them is cited from `Cache-Poisoning/` for the poisoning primitive. File DoS-as-pointer,
not as-home.

**Prototype pollution.** DOS-380873 (lodash 4.17.10) and DOS-864701 (4.17.15) are the
server-side prototype-pollution pair:

> It allows an attacker to inject properties on Object.prototype.

They sit adjacent because the DoS impact (object-shape corruption → crashes downstream)
is real, but the class belongs to `Prototype-Pollution/`. The vault keeps them so the
bucket arithmetic (221 = 75+20+10+100+16) remains complete and auditable.

**Noise with a DoS title.** DOS-153093's body is an advisory pointer ("My advisory can be
found in the attachment") — no quotable technique. DOS-649533 (2FA without email
verify) and DOS-1066851 (CTF write-up) have no DoS mechanism at all. They are in the
bucket, they are in the case-stock table, and they are the reason the playbook's kill-gates
exist.

## 3. The merge lane's crown: the $10,000 the bucket missed

DOS-185775 (**$10,000**) is the vault's second $10,000 row — and it is *not* in the
221-row bucket. The DB row has `weakness_name None`, so the exact-weakness filter
excluded it; `module_map_all.json` recovered it from the unclassified pool. The bug is
squarely module 01's class (a `Decimal.new(self)` assertion crash in mruby):

> When `Decimal` is initialized with itself, a new (empty) `mpd_t` will be created. To fill it with a value, `to_s` of the current instance is called, which accesses the empty `mpd_t`. This triggers an assertion, which leads to a crash.

Its siblings in the merge lane are the same story: DOS-204774 and DOS-216615 (both
`-$` mruby crashes) are module 01 mechanics with no bucket label. The merge lane's
lesson is methodological: **the 221-row bucket is a lower bound, not the class**. The
$37,004 in the merge lane is 13% of the vault's money hiding behind `weakness None`.

## 4. The merge lane's CVE wave and the amplification pair

The remaining paid merges are a coordinated-disclosure family: Rack Range-header giant
responses (2520679, $5,420), PermitScrubber backtracking (1804128, $4,000),
Accept-header ReDoS (2584376, $2,642), Rack header parsing (2071556, $2,540), Ruby URI
ReDoS (2071561, $2,540), Rack multipart ReDoS (1627159, $2,400), Django IPv6 (2939104,
$2,162), plus two GHSL metadata-only rows (801230, 1061211) whose 54-byte bodies
("This bug was reported directly to GitHub Security Lab.") carry $2,800 with no quotable
technique. The Range-header row is the family's thesis:

> Carefully crafted Range headers can cause a server to respond with an unexpectedly large response. Responding with such large responses could lead to a denial of service issue.

The body quotes the Rails advisory it coordinates with — same provenance pattern as the
in-bucket Rack trio (module 04 §5). DOS-752010/DOS-753491 (CVE-2018-6389) are the
amplification pair both directions: `load-scripts.php` generates ~3 MB for one
unauthenticated request:

> There is possibility in /wp-admin/load-scripts.php script to generate large (~3Mb) amount of data via simple non-authenticated request to server.

DOS-431561 (Rack multipart, 10,000 parts → 15–25 s) is the merge lane's in-bucket
duplicate-class proof — the same multipart exhaustion as DOS-1904097, one label to the
left:

> The multi-part body parsing in Rack and consequently Rails has a worse-than-linear performance relative to the number of parts in the request body.

DOS-880187 ($2,500, group-rename loop) and DOS-993582 (single search-bar request)
are the webapp-lane merges; DOS-496113 (Notepad++ `A*500` header crash) and
DOS-783356 (unbounded password length) are the one-liner tail.

## 5. What the two lanes teach about counting

- **Label-only buckets undercount by ~13%.** The merge lane's $37,004/$275,868 is the
  measured leakage of an exact-weakness funnel. Any vault built from a single weakness
  label should budget for a merge pass from the unclassified pool — and say so in
  `references/source-index.md`.
- **Impact ≠ class.** Nine of the 16 adjacent rows are more valuable as pointers to
  `Cache-Poisoning/` / `Prototype-Pollution/` than as DoS rows. The vault's job for
  them is *routing*, not claiming.
- **Metadata-only bodies carry money.** DOS-801230/1061211 ($2,800) and the adjacent
  lane's advisory-only DOS-153093 prove the corpus pays for rows you cannot quote.
  Record them; never invent technique for them.
- **What doesn't pay (and shouldn't be filed as DoS):** a verification gap (649533) or
  a CTF write-up (1066851) with a DoS-adjacent title. The case-stock table keeps them
  so the arithmetic stays honest; the playbook's P0 gate exists to stop the next one.

## 6. What pays, what doesn't

- **Cache-poison DoS paid $5,400 across two rows** (1096609 + 409370) — the only
  adjacent-lane money that is pure DoS impact. The unpaid cache cluster (7 rows) is the
  same primitive with no figure; file it as cache poisoning with a DoS *impact* section.
- **The merge lane out-pays the adjacent lane 7:1** ($37,004 vs $5,500). The bucket
  filter's misses were richer than its borderline includes — because `weakness None`
  hides both the mruby $10,000 and the Rack CVE family.
- **Prototype pollution as DoS paid $0** in this snapshot. File pollution as pollution;
  the DoS pointer adds nothing.
- **The method pays:** the vault's own funnel (221 bucket + 19 merges, reconciled
  row-by-row in `classes.json`) is the auditable surface. A DoS report that shows
  its funnel — what it searched, what it dropped, what the drops contained — is the
  report triage trusts.

## 7. Cross-references

- `Cache-Poisoning/` owns the mechanism for the nine cache rows (1096609, 409370,
  326639, 350847, 591302, 921704, 1160407, 1173153, 1181946); this module supplies the
  availability examples.
- `Prototype-Pollution/` owns DOS-380873/864701; `Authentication-Session/` owns
  DOS-649533's 2FA half.
- Modules 01/02/04 own the merge lane's mechanics as siblings (185775/204774/216615
  → module 01; 1804128/2584376/2071561/1627159 → module 02; 2520679/2071556/431561/
  2939104/880187/993582 → module 04). Each merge row's case-stock mechanism names the
  sibling module in prose above.
- `references/source-index.md` §2 documents the exact funnel (3,673 → 221 → 240) so a
  future sweep can re-derive it.
