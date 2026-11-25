---
title: "Android WebView & Intent — exported activities hand attacker bytes to WebViews; GHSL corpus block inside"
type: playbook
category: android-webview-intent
cwe: "CWE-707, CWE-749"
source_count: 7
full_bodies_available: 4
corpus: "h1-brain disclosed_reports.db (3,673 rows), unclassified_classified.json mobile ids -> module android-webview-intent (this build)"
list_accessed: "2026-11-07"
note: "Anchor bodies: MOB-414101 (Shipt exported WebView, $350), MOB-283058/MOB-283063 (IRCCloud exported pair), MOB-328486 (Zomato DeepLinkRouter). GHSL rows MOB-1011956/MOB-1030295/MOB-1161956 are metadata-only (corpus block). Claims trace to bodies read 2026-11-07."
---

# Android WebView & Intent — exported activities hand attacker bytes to WebViews; GHSL corpus block inside

## 1. Overview

Seven rows in two evidence tiers. The quotable tier is four exported-activity rows:
IRCCloud's SAMLAuthActivity (arbitrary-URL load) and ImageViewerActivity (HTML/JS
injection), Zomato's DeepLinkRouter (exported deep-link → TreatsWebView, session theft),
and Shipt's PushIO MessageViewActivity ($350, the module's only figure: kill, XSS, LFI,
asset read in one sink). The second tier is three GHSL CodeQL-query rows
(MOB-1011956 $2,300 · MOB-1030295 $1,800 · MOB-1161956 `None`) — Android WebView,
intent-extra, and Dex-loading queries, each a 54-byte body, zero quotes, exactly the
LDAP/XPath corpus-block pattern. Module total: **$4,450 / 3 rows with figures**
($350 + $2,300 + $1,800).

**Case-stock (7 rows / $4,450):**

| Case | Target | Mechanism | Bounty |
|---|---|---|---|
| [MOB-283058](https://hackerone.com/reports/283058) | irccloud (Android) | Exported SAMLAuthActivity → attacker `auth_url` in WebView | — |
| [MOB-283063](https://hackerone.com/reports/283063) | irccloud (Android) | Exported ImageViewerActivity → attacker URL in `loadDataWithBaseURL` HTML | — |
| [MOB-328486](https://hackerone.com/reports/328486) | zomato (Android/iOS) | Exported DeepLinkRouter → TreatsWebView with attacker `url` (+ `httpHeaders`) | — |
| [MOB-414101](https://hackerone.com/reports/414101) | shipt (Android) | Exported PushIOMessageViewActivity WebView (XSS / LFI / crash / asset) | $350 |
| [MOB-1011956](https://hackerone.com/reports/1011956) | github-security-lab | CWE-749 unsafe Android WebView loading (query) | $2,300 |
| [MOB-1030295](https://hackerone.com/reports/1030295) | github-security-lab | Remote source from Android intent extra (query) | $1,800 |
| [MOB-1161956](https://hackerone.com/reports/1161956) | github-security-lab | Insecure Dex loading, Java/Android (query) | — |

## 2. The IRCCloud pair: exported + WebView + no validation

Both IRCCloud rows are the same two-line recipe — `exported` activity reachable by any
app on the device (and, on new Androids, by Instant Apps from a browser) — with the sink
fed by an intent extra. MOB-283058 (SAMLAuthActivity) reads the extra and loads it:

> it means that it can be accessed by any third-party apps installed on the same device. On the newest Androids it also could be exploited by Android Instant Apps directly from a web-browser.

> It's dangerous because user doesn't see real URL. Attacker can open anything and specify any title (like "IRCCloud: Login Required"), and using that trick steal user credentials.

The impact is credential phishing through a legitimate client ("user doesn't see real URL"),
achieved with `adb shell am start … -e title "ATTAAACK" -e auth_url "http://google.com/"`.
MOB-283063 (ImageViewerActivity) is the code-execution half of the pair: the attacker URL
is concatenated into `loadDataWithBaseURL`'s HTML document (`<img src='…' onerror=…>`), so
the injected authority is the app's own WebView origin:

> so can be launched by arbitrary apps installed on the same device. On the newest Androids could be exploited also by Android Instant Apps directly from a web-browser (installation is not required).

> Inside this method attacker can inject arbitrary HTML/JS:

The pair is the module's method exemplar: manifest exports → extra → WebView, with the
ADB one-liner as the reproducibility baseline both rows share.

## 3. Zomato DeepLinkRouter: the exported deep-link session theft

MOB-328486 (Zomato, `None`) is the module's worst impact at no figure. The exported
`DeepLinkRouter` (scheme `zomato`, BROWSABLE) takes the incoming `zomato://…` URL, routes
host `treatswebview` to `TreatsWebViewActionBarActivity` with attacker-chosen `url` (and
`navigation_bar_title`), which calls `loadUrl(this.mWebViewURL, this.httpHeaders)`:

> is exported, and can be accessed by browser. When any WebView (in a client app, or a browser) meets a ``` zomato://etc ``` URL it will automatically launch Zomato app.

The local-server page is a single link (`zomato://treatswebview/?url=http://google.com…`)
and the filed impact is two lines:

> 1) Leakage of user tokens to arbitrary sites
> 2) XSS/Ability of open arbitrary sites in your internal WebView

The `httpHeaders` argument in the body's own code listing is the token-leak mechanism: the
attacker URL receives the app's authenticated headers. No third-party app is needed — the
browser is the delivery. The vault keeps the row at `None` and cites it as the module's
impact ceiling, not as a priced finding.

## 4. Shipt: one exported WebView, four payoffs ($350)

MOB-414101 (Shipt, **$350**) is the module's only quotable figure and its only
multi-payoff row: the exported `PushIOMessageViewActivity` (`exported=true`, PushIO SDK)
passes intent extras straight to the WebView, and the reporter demonstrates four payoffs
through the *same* sink — process kill (`chrome://crash`), phishing XSS (`javascript:`
prompt harvest), private-file read (`file:///data/data/…/pushio_store.xml`), and asset read
(`file:///android_asset/www/index.html`):

> Since the following activity `com.pushio.manager.iam.ui.PushIOMessageViewActivity` has `exported=true` it can be exploited by 3rd parties.

> With the help of a special intent, you can pass `if` blocks and load your own URL address or Javascript.

The `if`-block walk is the technique note: `content`, `url`, and `type` extras each steer
`mWebView.loadDataWithBaseURL` / `loadUrl`, so one intent covers JS, files, and crash.
$350 for four payoffs in this corpus is the WebView-sink price — the dossier the playbook
replicates (ADB + Java PoCs per payoff).

## 5. The GHSL corpus block (inside the module)

MOB-1011956 ("Java: CWE-749 Unsafe resource loading in Android WebView leaking to injection
attacks," $2,300), MOB-1030295 ("Java: Detect remote source from Android intent extra,"
$1,800), and MOB-1161956 ("porcupiney.hairs : Java/Android - Insecure Loading of a Dex File,"
`None`) are metadata-only CodeQL-query rows. Their titles name the exact sinks the four
quotable rows demonstrate (WebView loading, intent extras, Dex) — the detectors price the
same shapes the bodies prove. The module takes title + figure for these three and **zero
quotes** from them, per the LDAP corpus-block rule. Analysts must not add the $4,100
metadata total to the $350 quotable figure as if they were one price: they are two prices
for two artifacts (detector authorship vs. sink demonstration).

## 6. What pays, what doesn't

- The corpus pays **the demonstrated exported sink**, modestly: Shipt's four-payoff
  WebView at $350 is the quotable anchor. The three `None` exported rows (IRCCloud pair,
  Zomato) demonstrate equivalent or worse sinks at no listed figure — `None`, not $0.
- **Detector prices sit above sink prices here**: $2,300 + $1,800 for two metadata-only
  queries vs. $350 for a four-payoff demonstration. The vault reports the inversion
  honestly; it must not be read as "queries pay more than findings" beyond this corpus's
  three GHSL rows.
- **The ADB baseline is the reproducibility floor.** Every quotable row ships an
  `adb shell am start` PoC (plus Java). A WebView claim without an intent PoC is, in this
  corpus's terms, the metadata tier (title + figure, no body) — not a finding.
- **Browser-reachable export is the scariest sentence in the module** ("also could be
  exploited by Android Instant Apps directly from a web-browser," MOB-283058) — and it
  appears in the `None` rows. Scariest ≠ paidest; the vault keeps both facts.

## 7. Cross-references

- `XSS/` — the `loadDataWithBaseURL` / `javascript:` sinks terminate in XSS; that vault
  owns the XSS doctrine for these WebViews.
- `Web3-Smart-Contract/` — WEB3-1941767 (Android in-wallet browser) is the WebView-evidence
  sibling; that vault owns the CSP-parity row.
- Module B (`01_ios-app-privacy.md`) holds the browser-trust and key-lifecycle rows; the
  GHSL block (§5) sits here because its titles name WebView/intent/Dex sinks.
- Playbook P2 (`MOB-Testing-Agent-Playbook.md`) encodes the exported → WebView → intent-extra
  ladder from §§2–4.
