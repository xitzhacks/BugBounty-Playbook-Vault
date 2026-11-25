---
title: "Mobile case register — 13-row ledger (h1-brain corpus)"
type: register
built: "2026-11-07"
roster: "h1-brain disclosed_reports.db (3,673 rows; sha256 8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4); id set from unclassified_classified.json key mobile (13 ids), bodies re-read from DB"
case_id_scheme: "MOB-<HackerOne report id>"
bounty_rule: "DB bounty_amount where present (labeled $) · None = no figure in DB (not evidence of non-payment)"
module_rule: "frozen in archive/classes.json (bodies-win, mechanism-driven split)"
---

# Case register — Mobile (Android/iOS)

Corpus: 13 rows · 7 with bounty figures · **$6,810** · max $2,300 (MOB-1011956, metadata-only) · evidence: 10 full-body / 3 metadata-only.

Class census: android-webview-intent 7 (283058, 283063, 328486, 414101, 1011956, 1030295, 1161956) · ios-app-privacy 6 (176929, 221558, 519059, 1142918, 1189162, 1189168). Documented mechanism placements: 328486 (DeepLinkRouter → WebView) in A; 1142918 (GET_CONTENT file leak) in B.

Bounty arithmetic: $2,300 + $1,800 + $1,500 + $560 + $350 + $200 + $100 = **$6,810** (7 rows). Quotable subtotal $2,710 / 5 rows (1189162 $1,500 + 519059 $560 + 414101 $350 + 221558 $200 + 1189168 $100); metadata subtotal $4,100 / 2 rows (1011956 $2,300 + 1030295 $1,800).

| Case | Team | Bounty | Module | Evidence | Note |
|---|---|---|---|---|---|
| [MOB-176929](https://hackerone.com/reports/176929) | brave | — | ios-app-privacy | full | [ios] Address bar spoofing (Brave iOS 1.2.16, `document.write` loop); no downstream action |
| [MOB-221558](https://hackerone.com/reports/221558) | grab | $200 | ios-app-privacy | full | `auth_token` in GET + search indexing → cached private messages (DORK proof) |
| [MOB-283058](https://hackerone.com/reports/283058) | irccloud | — | android-webview-intent | full | Exported SAMLAuthActivity → attacker `auth_url` WebView; credential-phishing title |
| [MOB-283063](https://hackerone.com/reports/283063) | irccloud | — | android-webview-intent | full | Exported ImageViewerActivity → attacker HTML/JS in `loadDataWithBaseURL` |
| [MOB-328486](https://hackerone.com/reports/328486) | zomato | — | android-webview-intent | full | Exported DeepLinkRouter → TreatsWebView + `httpHeaders`; user-token leak to arbitrary sites |
| [MOB-414101](https://hackerone.com/reports/414101) | shipt | $350 | android-webview-intent | full | Exported PushIOMessageViewActivity WebView: kill / XSS / LFI / asset read in one sink |
| [MOB-519059](https://hackerone.com/reports/519059) | x | $560 | ios-app-privacy | full | Android overrides server "Protect your Tweets" on unrelated setting change |
| [MOB-1011956](https://hackerone.com/reports/1011956) | github-security-lab | $2,300 | android-webview-intent | metadata | CWE-749 unsafe Android WebView loading query; corpus max, no body |
| [MOB-1030295](https://hackerone.com/reports/1030295) | github-security-lab | $1,800 | android-webview-intent | metadata | Remote source from Android intent extra query; no body |
| [MOB-1142918](https://hackerone.com/reports/1142918) | nextcloud | — | ios-app-privacy | full | Evil `GET_CONTENT` picker → shares `shared_prefs` XML; CVE-2021-32695 |
| [MOB-1161956](https://hackerone.com/reports/1161956) | github-security-lab | — | android-webview-intent | metadata | Insecure Dex loading query; no figure, no body |
| [MOB-1189162](https://hackerone.com/reports/1189162) | nextcloud | $1,500 | ios-app-privacy | full | Server swaps E2E public key → device encrypts to evil admin (Desktop + Android) |
| [MOB-1189168](https://hackerone.com/reports/1189168) | nextcloud | $100 | ios-app-privacy | full | Account removal leaves E2E keys/mnemonic → re-login reads ciphertext; CVE-2021-32658 |

Module totals: android-webview-intent **$4,450 / 3 rows** (1011956 $2,300 + 1030295 $1,800 + 414101 $350) · ios-app-privacy **$2,360 / 4 rows** (1189162 $1,500 + 519059 $560 + 221558 $200 + 1189168 $100).
