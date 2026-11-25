---
title: "CSRF source index — provenance, funnel, fetch mechanics"
type: provenance
roster_source: "https://h1.security.nathan.sx/ (community mirror of public HackerOne reports, 4,419 rows, $2,030,173 paid, last updated 2017-09-12)"
accessed: "2026-10-28"
pattern_rows: 229
retrievable: 178
full_bodies_read: 178 (177 classified + 7 noise/adjacent-excluded on body read; 21 metadata-only)
http_404_rows: 51
bounty_grand_total_csrf_class: "$36,504 (JSON-verified $8,330 across 18 rows incl. one $50 noise row; list-stated on fetched rows $21,824 across 51; dead-404 list figures $6,400 across 20)"
companion_vaults: "../XXE · ../SQLi · ../SSRF · ../XSS · ../IDOR"
---

# Source Index — CSRF vault

## 1. Roster harvesting

Roster = the **h1.security.nathan.sx** mirror (full HTML, 4,419 report rows, 17,747 source lines,
frozen 2017-09-12), filtered — *filter only, classification decided by bodies* — with:

```
csrf|cross[- ]?site request|same[- ]?site|request forgery   (case-insensitive)
```

- **229 rows matched.** The loose `request forgery` arm drags in SSRF/SQLi titles; those were
  kept in the register and excluded from CSRF class counts on body read (see §6 noise).
- Case-ID scheme: `CSRF-<H1 report id>`.
- All 229 ids queued for fetch; fetch loop transiently lost one response (257237 — logged no
  HTTP code, wrote no file), refetched by hand → **178 retrievable, 51 × 404**. The funnel
  arithmetic is 229 = 178 + 51 exactly.
- The mirror predates 2017-09-12: every 2018–2026 CSRF case (GitLab #1122408 $3,370, Stripe
  #1483327 $5,000, GitHub Enterprise CVE-2022-23732 $10,000, Argo CD CVE-2024-22424) is OUTSIDE
  this roster and lives in [`blogs-index.md`](blogs-index.md), not in register counts.

## 2. Program histogram (229 rows)

| Program | Rows | Notes |
|---|---:|---|
| IRCCloud | 10 | the login-CSRF + email-change→reset ATO cluster (7531, 6910, 7051, 7332, 7516…) |
| Localize | 10 | blank-`CSRFToken`-accepted POST cluster (7870…8273) |
| Shopify | 10 | OAuth state fixation, GET state changes, HTTP-auth API CSRF, GA token leak |
| Weblate | 9 | login/logout/connect/reset-link CSRF cluster (223329…229528) |
| HackerOne ★ | 8 | self-reports: login CSRF 547, mark_as_read img 5946, SOP/UXSS $2,500 |
| Coinbase | 7 | set-as-primary GET, token-over-HTTP $1,000, signup session |
| Twitter | 7 | GA `__utmz` bypass, Periscope OAuth $2,520, disconnect img, cards `.json` |
| Vimeo | 5 | API playground $1,000, cross-site flashing $750, forgot-password no-validation |
| Badoo | 4 | `rt` service-worker leak ATO $852, delete-account $280 |
| Phabricator | 4 | login CSRF 2228, type-juggling $450, logout 2857, SSRF-adjacent 50537 |
| Slack | 3 | crumb-after-logout 2628, 2FA-SMS add $500, unauth-mode img $500 |
| Teavana / Rockstar / ok.ru / WePay / Zendesk / LocalTapiola / Square / Yahoo! / Harvest / concrete5 / gratipay / Ubiquiti / WordPress(.com) | 38 | one to six rows each |
| DoD / Nextcloud / Instacart / Imgur / stopthehacker / Mavenlink / Yelp / drchrono / Keybase / onpatient / pinion.gg / BrickFTP / mobilevikings / m.ok.ru / VK / WakaTime / Khan Academy / Zomato / Uber / GitLab / Akismet / Zapier / LegalRobot / Veris / Informatica / others | rest | mostly single rows |

## 3. Funnel

| Stage | Count | Notes |
|---|---:|---|
| Roster rows | 229 | title-filter on the 4,419-row mirror |
| Retrieved (HTTP 200) | 178 | public unauthenticated `hackerone.com/reports/<id>.json`, flat-format era export |
| **HTTP 404 (origin-dead)** | **51** | exact list in [`case-register.md`](case-register.md) §404 — **$7,750 list figures recorded ($6,400 on CSRF-class rows), unrecoverable, never quoted** |
| Full bodies present | 157 | incl. 7 noise/adjacent bodies that reclassified on read |
| Metadata-only (200, body withheld/empty) | 21 | e.g. 253128 SocialClub $600, 90165 ok.ru $500, 149589 WP add-admin $1,337 |

Dead-cluster note: the 404s include the register's juiciest claims — Zendesk "[CRITICAL] CSRF
leading to account take over" (102194, $500), Keybase "Stealing CSRF Tokens" (77065, $500),
Zendesk delete-subdomain (132049, $500), Square ×2 (30004/30011, $500 each). Titles and figures
are recorded; **no technical claim in any playbook rests on them.**

## 4. Body-fetch mechanics (identical to the XXE vault's method)

```bash
for id in $(cat ids.txt); do
  curl -s -m 25 -o "json/$id.json" -w "%{http_code}" "https://hackerone.com/reports/$id.json"
  sleep 1.2   # spacing discipline
done
```

- Public, unauthenticated endpoint only. No auth, no access-control bypass, no enumeration
  beyond the roster.
- Every response disk-cached: [`archive/json/`](archive/json/) (229 files; the 51 404s are
  preserved as error pages, never parsed as evidence).
- Bodies concatenated verbatim: [`archive/bodies-full-dump.txt`](archive/bodies-full-dump.txt)
  (5,813 lines, `body` → `vulnerability_information` → `activity_summary` fallback chain,
  `(sic)` marks applied at quote time).
- The era JSON is **flat** (top-level `title/state/substate/body/bounty_amount/weakness.name`),
  unlike the XXE build's `data.attributes` wrapper — [`archive/bounty-reconciliation.json`]
  (archive/bounty-reconciliation.json) carries the per-row reconciliation.
- `bounty_amount` exists on 18 rows ($8,330; includes the $50 SSRF-noise row CSRF-158016 — pure
  CSRF-class JSON-verified is $8,280 on 17 rows). Every other figure is **list-stated** and
  labeled per row in the register.

## 5. Era statistics

The flat export carries no dates; era is bounded by the mirror freeze (2017-09-12, max id
257237) and H1's sequential ids:

| ID band | Era (approx) | Character |
|---|---|---|
| 547 – 13705 (2014) | early H1 | login-CSRF primitives, token lifecycle reports, GET-lane noise |
| 21069 – 76733 (2015) | mature early | IRCCloud/Coinbase clusters, UniFi referer bypass, SOP/UXSS $2,500 |
| 86022 – 148890 (2015–2016) | fat center | Phabricator type-juggling, Localize blank-token cluster, concrete5, GA `__utmz` |
| 149589 – 215381 (2016–2017) | late | Teavana persistent-CSRF, Periscope OAuth $2,520, Shopify HTTP-auth $1,000 |
| 221043 – 257237 (2017) | final months | Nextcloud portal login, Weblate cluster, metadata-heavy tail |

Corpus is a **2014–2017 snapshot**. Consequence: SameSite (2016 spec, 2020 enforcement) and
modern framework defaults (Django/Spring/Rails per-form tokens) postdate most rows — mechanisms
survive, the *default-vulnerable* assumption does not. The playbook (P1) fingerprints framework
hardening before firing any payload. Post-2017 cases are cited from blogs-index only, never
blended into register counts.

## 6. Limitations

1. **One-source roster, curated by a third party.** The mirror's bounty column is list-stated;
   wherever JSON carried a figure it was used and labeled. The register's grand total
   reconciles to the extracted roster ($39,504 tagged − $1,650 SSRF-noise − $1,350 dead-SQLi
   mislabel = $36,504 CSRF-class).
2. **51 rows are permanently dark** (404). Titles + list bounties recorded; nothing quoted,
   nothing reconstructed.
3. **21 rows are metadata-only.** Titles + substate + weakness labels kept; no technique content.
4. **Weakness labels are era values and often wrong.** CSRF-158016 (Instacart) is labeled
   "Code Injection", CSRF-76733 (Slack) "Information Disclosure" — bodies decide; the register
   keeps the archive label, modules correct it against the body ("bodies win" rule).
5. **Noise rows kept honest.** Seven roster matches are not CSRF by body/type: four SSRF
   (91816, 158016, 189648, 145524, 50537), one SQLi title (191601, dead), two FPD-on-failure
   (148890, 150018) — recorded in the register, excluded from every class count.
6. **Out-of-roster sources are bibliographic.** zseano's CSRF guide (fetched, byte-quoted),
   119 bugbountyhunting.com title-linked writeups (bodies not fetched this build), and the
   five modern skill-cited cases live in [`blogs-index.md`](blogs-index.md). No playbook claim
   depends on a title-only row.
7. **No live testing was performed** — every play step is corpus-derived; validate against the
   hunt-csrf skill's scenario matrix in the field.
