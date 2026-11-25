---
title: "Open Redirect source index — provenance, funnel, fetch mechanics, limitations"
type: source-index
built: "2026-10-29"
---

# Source index — Open Redirect build

## 1. Roster provenance

- **Primary roster**: full HTML of `h1.security.nathan.sx` — 4,419 public HackerOne report rows,
  snapshot frozen **2017-09-12**. Same mirror as `../XXE` and `../CSRF` builds (byte-identical parse:
  4,419 unique report rows).
- **Title filter** (case-insensitive, applied to mirror titles):
  `redirect|redirection|redir|forward(ed|ing)?|unvalidated|open[- ]?url|url[- ]?(forwarding|redirection)|return[-_ ]?to|returnurl|return[-_ ]?url|goto`
  plus targeted arms `phishing|tabnabbing|opener|window\.open|malicious (site|website|url|link)|url sanitiz|callback_url|External URL page`.
- Funnel: 4,419 mirror rows → **198 matched** (92 bounty-tagged on the list, list-sum $46,891) →
  **129 retrieved bodies** read end-to-end + **69 dead-404** recorded.
- Candidate-arm audit before finalizing: a broad `location|url|uri|next` arm was tested and rejected
  (+73 rows, dominated by OpenSSL CVEs, XSS rows, URL-spoofing browser rows); a `spoof` arm was
  tested and rejected (+92 rows, email/content spoofing). The five targeted arms above added 21 rows
  (tabnabbing/opener lane, the Slack/link-phishing cluster, Digits `callback_url`, Gratipay
  malicious-site row).
- **Known filter gaps**: title-filter-only rostering (same discipline as XXE/CSRF builds) — a report
  titled without any filter word is absent from the roster even if its body is an open redirect.
  Conversely every roster row whose body proved non-redirect is kept in the register as noise/adjacent,
  never silently dropped.

## 2. Retrieval funnel (exact arithmetic)

| Stage | Count |
|---|---|
| Mirror rows parsed (unique report ids) | 4,419 |
| Title-filter matches (roster) | 198 |
| Fetch attempt 1 (background): 200-ok / 404 / transient-000 | 88 / 57 / 53 |
| Fetch attempt 2 (retry of the 53 transient only) | 41 ok / 12 × 404 |
| **Final**: 200-ok bodies | **129** |
| **Final**: dead 404s (57 + 12, ledger in `http-codes.txt`) | **69** |
| Bodies with content after fallback chain (body → vulnerability_information → activity_summary → team summaries[]) | 129 |
| 200-ok rows with title only (empty info fields) | 11 (team-summary fallback used) |

- Session-interruption note: the original fetch (162 done) was cancelled by a harness restart and the
  entire `/tmp/opencode/redirect` workspace was wiped; the roster was regenerated deterministically
  from the mirror (198 rows, 92 bounty-tagged, $46,891 — byte-identical), and the fetch restarted from
  zero. Funnel numbers above are from the surviving final state, mechanically regenerated.
- 404 handling: dead rows are **recorded** in `case-register.md` (title/team/list-bounty from the
  mirror) and in `archive/http-codes.txt`; never quoted; their list figures sit in the dead-404
  bounty bucket.

## 3. Era statistics (129 fetched bodies, from JSON metadata)

- Disclosed at: **2014: 22 · 2015: 21 · 2016: 48 · 2017: 38** — a 2014–2017 corpus (mirror freeze
  2017-09-12). Every post-2017 community writeup stays in `blogs-index.md` as bibliography only.
- Severity ratings (JSON): none 98 · medium 15 · low 14 · high 2 — consistent with the class's
  "Low alone, High chained" economics.

## 4. Program histogram (all 198 roster rows)

Shopify 16 · HackerOne 12 · Mail.Ru 11 · Slack 10 · Twitter 9 · New Relic 8 · LocalTapiola 7 ·
Yahoo! 7 · GitLab 5 · Uber 5 · Trello 4 · Dropbox 4 · Weblate 4 · Coinbase 4 · (others ≤3).

## 5. Bounty reconciliation (rule: JSON first, list fallback, labels everywhere)

| Bucket | Rows | Amount |
|---|---|---|
| JSON `bounty_amount` verified | 26 | $16,070 |
| List-stated (fetched; JSON present but amount withheld) | 42 | $24,163 |
| Live-tagged total | 68 | $40,233 |
| Dead-404 list figures (24 of 69 dead rows tagged) | 24 | $6,658 |
| **Roster-tagged grand total** | **92** | **$46,891** |
| Class modules 01–07 (pure redirect class) | 63 tagged | $36,523 |
| Module 08 adjacent+noise | 5 tagged | $3,710 |

- 43 fetched rows carry `has_bounty?:true` with `bounty_amount:null` — the H1 API confirms a bounty
  exists but withholds the amount; those rows are labeled **list** (mirror figure), per the
  vault-wide bounty rule.
- Largest figures: $3,000 × 2 (26962 rfc6749 error-redirect; 125791 uber root-path) · $2,520
  (108113 Digits callback) · $2,500 (191196 G Suite redirect-DoS, adjacent) · $2,000 (51265 Flash 307)
  · $1,400 × 2 (49759 authenticity_token; 48516 /intent/ XSS).

## 6. Companion sources fetched this build

- `bugbountyhunter.com/vulnerability/?type=open_redirect` — zseano's "Learning about Open Url
  Redirects" guide (fetched, byte-quoted in `blogs-index.md` §1). Category page confirms the
  BugBountyHunter taxonomy label: **"Open Redirects (+Oauth flows)"**, 3 labs.
- `bugbountyhunter.com` disclosed-stats page — Open Redirect row verified:
  **135 programs, 342 disclosed** (the master-list figure).
- `bugbountyhunting.com` writeup index (script.js, 7,103 entries) → 148 redirect-class entries →
  140 unique (8 dupes) → 136 kept + 4 filter-artifact noise (`blogs-index.md` §2).
- zseano.com/blogs/2.html ("Open URL redirects to grab FB OAuth Tokens") — **fetch failed twice**
  (timeout); recorded title-only in §2. Nothing was written from memory about its contents.

## 7. Limitations

1. Mirror freeze 2017-09-12: no 2018+ platform hardening (post-2017 discourse lives in the
   bibliography only; register counts never blend it).
2. Title-only rostering: sub-titled open redirects inside multi-bug reports are included only when
   the mirror title matched (e.g. 171398 matched on "Open Redirect" inside an SSO-SAML triple).
3. 404 bodies unrecoverable: 69/198 (34.8%) — higher than CSRF (22%) and XXE; small 2015-era
   programs (Vimeo/Zaption/C2FO era) purge or hide reports most often.
4. 11 fetched rows expose no reporter body (empty info fields; team-summary fallback captured
   where the team wrote one; two rows are one-liners: 258632 "Open redirect on owncloud.com").
5. The bounty layer mixes two sources by rule (JSON vs mirror list); both are labeled per row in
   the register. No cross-check disagreement was found between JSON and list figures on rows
   carrying both.
6. Community writeups (§2) are title-linked; their bodies were not fetched this build.
7. Severity `none` dominates (98/129) — per-report impact was usually argued in prose, not scored;
   module validation gates reconstruct impact arguments from the paying cases.
