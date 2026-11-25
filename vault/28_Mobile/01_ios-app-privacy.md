---
title: "iOS & App Privacy — browser trust, token-in-URL, setting override, E2E key lifecycle"
type: playbook
category: ios-app-privacy
cwe: "CWE-707, CWE-359"
source_count: 6
full_bodies_available: 6
corpus: "h1-brain disclosed_reports.db (3,673 rows), unclassified_classified.json mobile ids -> module ios-app-privacy (this build)"
list_accessed: "2026-11-07"
note: "Anchor bodies: MOB-1189162 (Nextcloud E2E key verification, $1,500), MOB-519059 (Twitter setting override, $560), MOB-1142918 (Nextcloud file leak, CVE-2021-32695). Claims trace to bodies read 2026-11-07."
---

# iOS & App Privacy — browser trust, token-in-URL, setting override, E2E key lifecycle

## 1. Overview

Six rows, all full-body, **$2,360 / 4 rows with figures** (max $1,500). "Privacy" here is
not settings-page prose; it is three concrete failures: the *browser lies about the
address* (Brave iOS), the *app leaks the secret in the URL* (Grab), and the *app forgets
what it stored* (Twitter setting override, Nextcloud key lifecycle) — plus one file leak
through the platform's own file picker (Nextcloud, CVE-2021-32695). The module's rule:
privacy failures pay when they move a secret or a setting, not when they describe a
risk.

**Case-stock (6 rows / $2,360):**

| Case | Target | Mechanism | Bounty |
|---|---|---|---|
| [MOB-176929](https://hackerone.com/reports/176929) | brave (iOS) | Address-bar spoof: `document.write` + `google.com:1234` loop | — |
| [MOB-221558](https://hackerone.com/reports/221558) | grab (Android app web) | `auth_token` in GET URL + search indexing → cached private messages | $200 |
| [MOB-519059](https://hackerone.com/reports/519059) | x (Android) | Server-side setting override unprotects tweets on unrelated change | $560 |
| [MOB-1142918](https://hackerone.com/reports/1142918) | nextcloud (Android) | Evil `GET_CONTENT` picker → shares `shared_prefs` (CVE-2021-32695) | — |
| [MOB-1189162](https://hackerone.com/reports/1189162) | nextcloud (Desktop + Android) | Server swaps E2E public key → device encrypts to attacker | $1,500 |
| [MOB-1189168](https://hackerone.com/reports/1189168) | nextcloud (Android) | Account removal leaves E2E keys/mnemonic → re-login reads ciphertext | $100 |

## 2. The browser lies: Brave iOS address-bar spoof (MOB-176929, `None`)

The vault's only iOS row is a browser-trust row: the Brave-for-iOS address bar can be
spoofed with a `document.write("<h1>This is not Google</h1>")` + `document.location =
"https://google.com:1234"` + `setInterval` loop, PoC button included:

> I've found an address bar spoofing vulnerability in the latest version of Brave for iOS.

The body is 549 bytes — summary, version (1.2.16, "Android maybe?"), the PoC, a file
marker. No account, no credential flow, no follow-up action. The vault keeps the row at
`None` and cites it as the module's negative anchor: a browser-trust *demonstration*
without a downstream credential/consent action prices at no figure in this corpus. (The
Module-A WebView rows earn their antipode the same way: browser-reachable export without
a shipped consequence is a demo, not a payout.)

## 3. The URL leaks the secret: Grab messages in search cache ($200)

MOB-221558 (Grab, **$200**) is a "messages" finding whose leak channel is a URL. The
Android app loads private messages (OTPs, group invites) over GET with the `auth_token` in
the query string, on a host that allows search indexing; the token — and with it the
messages — lands in the search engine's cache, reachable by a `passenger
site:grab-attention.grabtaxi.com` DORK:

> It happens because the `https://grab-attention.grabtaxi.com` host allows search indexing, and can leak the auth_token to the Search Engines which also can lead to privilege escalation.

The Suggested fix is the module's portable sentence: disable indexing and change the method
GET → POST (or encrypt it). $200 is the corpus price for an *indexed secret*: the DORK
is the proof, the cache is the exfiltration, the GET is the root cause. Module readers
must cite the method diagnosis, not just the cache screenshot — the Information-Disclosure
vault owns cache doctrine; this module owns the app-channel (tokens in query strings)
diagnosis.

## 4. The app forgets what it stored: Twitter setting override ($560)

MOB-519059 (x, **$560**) is the vault's tidiest paid privacy row: set "Protect your Tweets"
on the web, then change any unrelated setting in the Android app ("Receive message
requests," "Show read receipts") and the tweets go public — the app overwrites the
server-side flag from its stale local state:

> The Android app overrides the "Protect your Tweets" setting set from outside the app in some cases when changing other settings.

> This can cause a user's tweets to unknowingly become public.

The body is honest about the odds ("that is less likely to succeed than with the previous
bug where only changing the email address was required") and the fallback ("you may have to
first explicitly unset …"). $560 is the corpus price for a *state-confusion* privacy bug:
the setting the user verified on one surface is silently un-set on another. The playbook
generalizes it as the cross-surface state test (P2 rung 3).

## 5. The file picker leaks the vault: Nextcloud `GET_CONTENT` (CVE-2021-32695, `None`)

MOB-1142918 (Nextcloud, `None`, CVE-2021-32695) is the module's scariest mechanism at no
figure: a PoC app advertising `ACTION_GET_CONTENT` (`EvilActivity`) answers the client's
shareable-directory upload picker, and the victim's picker — believing it uploads to her
own share — instead publicly shares `shared_prefs/com.nextcloud.client_preferences.xml`
with its account, storage path, and push token:

> if the victim click the poc app by accident, the secret file "/data/data/com.nextcloud.client/shared_prefs/com.nextcloud.client_preferences.xml" will be publicly shared and leaked.

The filed impact is one line ("arbitrary sensitive file under nextcloud android client
privacy directory /data/data/com.nextcloud.client leaked"). Module placement note: the
mechanism is a *file-picker* (intent) leak, not a WebView sink — Module A holds the
WebView/intent-`extra` rows; this row is privacy/data (what the app *stores*) and sits
here by mechanism. The adjustment is documented in the register and source-index; the row
is in exactly one module regardless.

## 6. The key lifecycle: Nextcloud E2E verification ($1,500) and clearing ($100)

The module closes with a two-row pair on one product and one question — *does the app
bind keys to the account lifecycle?* MOB-1189162 (Nextcloud, **$1,500**) answers no at
setup: a server admin replaces the user's E2E public key, a new device enrolls with the
nonce, and the device encrypts to the attacker's key:

> In short it breaks the whole premise of your end to end encryption. An evil admin is able to make the device encrypt to their key.

The RFC sentence ("Client checks if private key belongs to previously downloaded public
certificate") and the one-step remediation ("the clients should verify that the private
key matches with the public key and if not throw a big error") are the vault's
vendor-neutral hardening fingerprint (P4). MOB-1189168 (Nextcloud, **$100**,
CVE-2021-32658) answers no at teardown: remove the account, keep the keys and mnemonic on
device, re-add from the victim's device and read the ciphertext:

> Once you remove your account all information regarding that account should be removed.

* the keys
* the mnemonic

And "certainly when you re-add an account you should be asked to enter your mnemonic" —
at $100, the corpus prices the residual-access demonstration at roughly one-tenth the
verification failure. The pair read together is the module's doctrine: bind keys at setup
($1,500) and destroy them at teardown ($100) — or pay for both absences separately.

## 7. What pays, what doesn't

- The corpus pays **moved secrets and moved settings**: indexed `auth_token` ($200),
  silently un-set tweets ($560), server-swapped E2E keys ($1,500), uncleared E2E keys
  ($100). The token-in-URL row's DORK and the state-confusion row's 5-step repro are the
  paid shapes: a *visible channel* for the secret.
- **Demos without a secret do not pay in this corpus.** The Brave address-bar spoof
  (`None`) and the Nextcloud file-picker leak (`None`, despite a CVE) both demonstrate
  the channel; the DB records no figure for either. CVE-2021-32695 at `None` is the
  vault's sharpest reminder that a CVE is not a payout.
- **The pair-pricing is product-specific.** Nextcloud's setup ($1,500) vs. teardown ($100)
  split must not be generalized into "verification pays 15× clearing" beyond this
  product's two disclosures.
- **Interaction is a price term.** The Grab row needs the victim to have indexed messages
  (DORK surface); the Twitter row needs the cross-surface sequence ("may have to first
  explicitly unset"); the Nextcloud picker row needs the victim to click the PoC "by
  accident." All three are written in the bodies; the playbook requires them written.

## 8. Cross-references

- Module A (`00_android-webview-intent.md`) — the WebView-export rows; MOB-1142918's
  file-picker mechanism is the documented seam between the modules.
- `Information-Disclosure/` — MOB-221558's search-cache leak; that vault owns cache doctrine.
- `Authentication-Session/` — session/key trust posture for MOB-328486 (Module A) and
  the E2E lifecycle rows here.
- Playbook P2 (`MOB-Testing-Agent-Playbook.md`) encodes the browser-trust → secret-channel →
  cross-surface-state ladder from §§2–4.
