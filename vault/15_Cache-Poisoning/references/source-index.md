---
title: "Cache Poisoning source index — provenance, funnel, classification mechanics, limitations"
type: source-index
built: "2026-11-07"
---

# Source index — Cache Poisoning build

## 1. Corpus provenance

- **Primary source**: `/home/user/tools/h1-brain/disclosed_reports.db` — the h1-brain pre-built
  SQLite corpus of publicly disclosed, bounty-awarded HackerOne reports (**3,673 rows**). The
  repo ships the DB as a Git-LFS pointer; the real file was fetched from
  `media.githubusercontent.com` and sha256-verified:
  `8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4`.
- **Row fields**: `id, title, vulnerability_information, weakness_name, program_handle,
  asset_identifier, asset_type, cve_ids, bounty_amount`. Bodies live in
  `vulnerability_information`.
- **Working copies**: `/home/user/opencode-work/h1brain/classified.json` (classifier output),
  `module_map_all.json` (module assignment), `cache-poisoning_digest.md` (reading digest).
  In-vault archive: `references/archive/CACHE-bodies-full-dump.txt`, `classes.json`, `meta.json`.

## 2. Classification funnel

1. **Labeled/keyword net** over all 3,673 rows: weakness families (`Web Cache Deception`,
   `Cache Poisoning`, `HTTP Response Splitting`) plus keyword arms (`cache poison`,
   `web cache deception`, `X-Forwarded-Host`, `unkeyed`, `cache deception`) → bucket of 15.
2. **Body read**: all 15 bodies read before assignment ("bodies win").
3. **Module split** (frozen in `classes.json`):
   - `unkeyed-header-reflection` 7 — header value lands in a cacheable response.
   - `cache-deception-key` 3 — victim content stored where the attacker can fetch it.
   - `cache-implementation-path-manifest` 5 — path/parser/CVE-level differentials.
4. Sibling rows that live in other vaults: cache-DoS rows also surface in
   `../21_Denial-of-Service/` (DOS-adjacent pool), and host-header rows split to
   `../24_Host-Header-Injection/`.

## 3. Bounty accounting

- **Rule**: DB `bounty_amount` where present; `-` recorded when the DB has no figure. A blank
  is not evidence of non-payment.
- Corpus: **6/15 rows** carry figures, totaling **$6,506**; max $3,800 (CACHE-1695604).
  Module totals: 01 $2,206/3 · 03 $4,300/2 · 02 $0/0 recorded.

## 4. Era discipline

- Rows span 2015–2024. CDN behavior changed materially across that window: `Vary` handling,
  header keying, and path canonicalization are all stricter at the modern edge, so the
  techniques are *tests*, not guarantees.
- Weakness labels are historical triage values (XSS, Open Redirect, Information Disclosure);
  modules classify by the mechanism in the body.

## 5. Limitations

1. **Small bucket (15)** — the h1-brain corpus is a disclosed-only slice, not HackerOne's full
   cache-poisoning population. Master-list row 15 cites 4 + 34 externally.
2. **Nine rows have no bounty figure** — payout expectations in this vault are a floor.
3. **No live re-testing** was performed; all mechanics trace to archived bodies.
4. **Safety constraints** bound the class — you cannot safely mass-verify a CDN-wide poison, so
   the strongest evidence remains a single controlled second-client fetch.
5. **Quote discipline**: every blockquote in this vault is byte-true to
   `references/archive/CACHE-bodies-full-dump.txt`; `(sic)` marks author typos.
