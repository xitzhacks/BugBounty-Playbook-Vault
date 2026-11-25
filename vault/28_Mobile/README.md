---
title: "Vault/28 — Mobile (Android/iOS) playbook set"
type: index
category: mobile
built: "2026-11-07"
evidence: "13 rows (unclassified_classified.json mobile ids) → 10 retrievable bodies read (10 full-body / 3 metadata-only GHSL rows) · 2 modules"
bounty: "$6,810 across 7 rows with DB figures (max $2,300, MOB-1011956) · 6 rows carry no DB figure"
companion_vaults: "../XSS · ../Web3-Smart-Contract · ../Information-Disclosure · ../Authentication-Session"
case_id_scheme: "MOB-<HackerOne report id>"
quote_rule: "byte-true, (sic)-marked, from read bodies only; metadata-only rows recorded never quoted"
---

# Vault/28 — Mobile (Android/iOS) playbook set

Thirteen rows split by what the app *does* with untrusted input: one module for exported
activities that hand attacker bytes to a WebView (the Android intent/WebView family — the
vault's quotable core, 4 full bodies), one for app-privacy failures (browser trust,
token-in-URL, setting override, E2E key lifecycle — 6 full bodies). Three GHSL CodeQL-query
rows ride inside the first module as a labeled corpus block (metadata-only, zero quotes),
exactly as LDAP/XPath does for its whole bucket. The money is split across the seam: the
vault's biggest figure ($2,300) is a metadata-only query row; the biggest *quotable* figure
is a $1,500 E2E key-lifecycle row.

## Start here

| # | File | What it gives you |
|---|---|---|
| 1 | [`MOB-Testing-Agent-Playbook.md`](MOB-Testing-Agent-Playbook.md) | **The executable protocol.** P0 program/policy read → P1 exported-surface inventory → P2 probe protocol (exported-component → WebView → intent-extra → browser-trust) → P3 proof ladder → P4 hardening fingerprints → P5 kill-gates. |
| 2 | [`00_android-webview-intent.md`](00_android-webview-intent.md) | Exported-activity → WebView rows (IRCCloud ×2, Zomato, Shipt $350) + 3 GHSL metadata-only rows (corpus block inside the module). |
| 3 | [`01_ios-app-privacy.md`](01_ios-app-privacy.md) | Brave iOS address-bar spoof, Grab token-in-URL, Twitter setting override ($560), Nextcloud file leak (CVE-2021-32695) and E2E key lifecycle ($1,500 + $100). |

## References (provenance layer)

| File | Contents |
|---|---|
| [`references/source-index.md`](references/source-index.md) | Corpus provenance (h1-brain DB `disclosed_reports`, sha256 `8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4`, 3,673 rows), classification funnel (`unclassified_classified.json` `mobile` → 13 ids, DB reconciliation), module split, bounty accounting, era discipline, 7 limitations. |
| [`references/case-register.md`](references/case-register.md) | Row-per-row ledger of all 13 rows: case ID, team, bounty, module, evidence level, CVE. |
| [`references/archive/mob-bodies-full-dump.txt`](references/archive/mob-bodies-full-dump.txt) | All 13 bodies verbatim (10 full + 3 × 54-byte GHSL lines) — the anchor for every quote. |
| [`references/archive/classes.json`](references/archive/classes.json) | Frozen module assignment for all 13 rows. |

## Scoreboard (13 rows · 7 with bounty figures · $6,810 · max $2,300)

| Case | Title (short) | Program | Bounty | CVE |
|---|---|---|---|---|
| [MOB-176929](https://hackerone.com/reports/176929) | [ios] Address bar spoofing in Brave for iOS | brave | — | — |
| [MOB-221558](https://hackerone.com/reports/221558) | Private Grab Messages cached, token in GET | grab | **$200** | — |
| [MOB-283058](https://hackerone.com/reports/283058) | [IRCCloud Android] Arbitrary URLs in SAMLAuthActivity | irccloud | — | — |
| [MOB-283063](https://hackerone.com/reports/283063) | [IRCCloud Android] XSS in ImageViewerActivity | irccloud | — | — |
| [MOB-328486](https://hackerone.com/reports/328486) | [Zomato Android/iOS] Theft of user session (DeepLinkRouter) | zomato | — | — |
| [MOB-414101](https://hackerone.com/reports/414101) | Vulnerabilities in exported activity WebView | shipt | **$350** | — |
| [MOB-519059](https://hackerone.com/reports/519059) | Protected Tweets overridden by Android app | x | **$560** | — |
| [MOB-1011956](https://hackerone.com/reports/1011956) | CWE-749 Unsafe Android WebView loading (GHSL) | github-security-lab | **$2,300** (max, metadata) | — |
| [MOB-1030295](https://hackerone.com/reports/1030295) | Detect remote source from Android intent extra (GHSL) | github-security-lab | **$1,800** (metadata) | — |
| [MOB-1142918](https://hackerone.com/reports/1142918) | Leak arbitrary file under Nextcloud privacy directory | nextcloud | — | CVE-2021-32695 |
| [MOB-1161956](https://hackerone.com/reports/1161956) | Insecure Loading of a Dex File (GHSL) | github-security-lab | — | — |
| [MOB-1189162](https://hackerone.com/reports/1189162) | E2E public key not verified (Desktop + Android) | nextcloud | **$1,500** | — |
| [MOB-1189168](https://hackerone.com/reports/1189168) | Android app does not clear E2E keys | nextcloud | **$100** | CVE-2021-32658 |

Corpus program mix: nextcloud 3 · irccloud 2 · github-security-lab 3 · brave, grab, zomato,
shipt, x 1 each. Evidence: 10 full-body / 3 metadata-only (all three GHSL rows).

## Vault map

| File | Content |
|---|---|
| `MOB-Testing-Agent-Playbook.md` | Agent-facing operational playbook: P0–P5 phases, module↔phase table, non-goals. |
| `00_android-webview-intent.md` | Module A: exported-activity/WebView/intent rows (7 rows, 4 full-body) + labeled GHSL corpus block. |
| `01_ios-app-privacy.md` | Module B: browser/app-privacy/data-lifecycle rows (6 rows, all full-body). |
| `references/source-index.md` | Provenance, funnel, DB reconciliation, module split, bounty accounting, era discipline, limitations. |
| `references/case-register.md` | 13-row ledger with DB metadata, evidence level, CVEs. |
| `references/archive/mob-bodies-full-dump.txt` | All 13 bodies verbatim (anchor for every quote). |
| `references/archive/classes.json` | Frozen module assignment for all 13 rows. |

## Cross-vault links

- `XSS/` — the WebView rows terminate in XSS; that vault owns the XSS payoff doctrine for
  the `loadDataWithBaseURL` / `javascript:` sinks.
- `Web3-Smart-Contract/` — WEB3-1941767 (MetaMask Android browser ignores CSP) is the
  in-wallet-browser evidence; this vault owns exported-activity evidence, that vault owns
  the CSP-parity row.
- `Information-Disclosure/` — MOB-221558's token-in-URL search-cache leak and MOB-1142918's
  file leak are disclosure rows; that vault owns disclosure doctrine, this vault owns the
  app-channel evidence.
- `Authentication-Session/` — MOB-328486's session-token theft and MOB-1189162/1189168's
  key-lifecycle rows touch session/key trust; that vault owns the defensive posture.

## Coverage vs limitations

**Covered**: the complete `mobile` id set (13 rows) with per-row exported-surface, sink, and
bounty; the 2-module split (7 + 6) with every id in exactly one module; DB reconciliation
for every row.

**Honest limitations**:
1. **Bucket provenance differs from the sibling vaults.** Mobile rows come from
   `unclassified_classified.json` key `mobile` (a 13-id list, not classified rows) and were
   promoted by body read this build. The vault records the id set verbatim and keeps no
   `classified.json` claim for these rows.
2. **Module split adjusted by body (documented).** MOB-328486 (Zomato DeepLinkRouter →
   WebView, exported) sits in Module A (WebView/intent) with its mechanism, not in Module
   B; MOB-1142918 (Nextcloud `GET_CONTENT` file leak, CVE-2021-32695) sits in Module B
   (privacy/data) with its mechanism. Both adjustments are mechanism-driven and recorded
   in the register and source-index. Every id is in exactly one module regardless.
3. **Three metadata-only rows carry $4,100 of $6,810.** The GHSL rows (1011956 $2,300,
   1030295 $1,800, 1161956 `None`) are titles + figures only. The quotable vault total is
   $2,710; the metadata total is $4,100. The vault never blends them.
4. **Weakness labels are null.** All 13 DB rows have `weakness_name` null; classification is
   by body behavior only.
5. **Screenshot/video-dependent PoCs.** Several rows lean on `{F…}` markers; text payloads
   (ADB intents, `loadDataWithBaseURL` strings) are byte-true here. No image content is
   reconstructed.
6. **Era honesty.** Rows span 2016 (Grab) through 2021 (Nextcloud CVEs); modern
   `exported=false` defaults and E2E key-pair binding are fingerprinted in playbook P4
   and labeled outside the corpus.
7. **No live testing was performed.** Validate exported-component/WebView probes on test
   devices/builds in scope — never against production users' devices or accounts.


<!-- CASESTOCK-LINK:BEGIN -->

## Case stock — vault (`_VAULT/`)

**185 disclosed reports** routed to this category · 65 with a bounty figure · **$75,830** · 94 full write-ups stored locally.

- Full list: [`_VAULT/by-vault-category/28_Mobile.md`](../_VAULT/by-vault-category/28_Mobile.md)
- Query: `sqlite3 ../_VAULT/reports.sqlite "SELECT id,bounty,title FROM reports WHERE ..."`
- Pull one write-up: `python3 ../_VAULT/scripts/extract_report.py <id>`

| Top paid | Program | Bounty |
|---|---|---|
| [977212](https://hackerone.com/reports/977212) read new emails from any inbox IOS APP in notification center | Mail.ru | $10,000 |
| [138101](https://hackerone.com/reports/138101) Weak user aunthentication on mobile application - I just broken userKey secret p | Pornhub | $5,000 |
| [1122661](https://hackerone.com/reports/1122661) [Java] CWE-312: Query to detect cleartext storage of sensitive information using | GitHub Security Lab | $4,500 |
| [1378889](https://hackerone.com/reports/1378889) [Android] Directory traversal leading to disclosure of auth tokens | Slack | $3,500 |
| [1343528](https://hackerone.com/reports/1343528) Уязвимость в приложении для Android | VK.com | $3,000 |

_refreshed 2026-11-17 from the public HackerOne disclosed-report dataset_
<!-- CASESTOCK-LINK:END -->
