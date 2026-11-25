---
title: "GET State Changes — the img-tag lane"
type: playbook
category: get-state-changes
cwe: "CWE-352"
source_count: 28
full_bodies_available: 28
corpus: "h1.security.nathan.sx roster (229 rows), bodies via hackerone.com/reports/<id>.json"
list_accessed: "2026-10-28"
note: "Anchor bodies: CSRF-174328 (Slack, $500 JSON), CSRF-226418 (H1 JIRA, $500 JSON), CSRF-96470 (Shopify, $500 JSON). Claims trace to bodies read 2026-10-28."
---

# GET State Changes — the cheapest lane in the corpus

## 1. Overview

Twenty-eight cases perform state changes via GET — mutations reachable by `<img src>`, `<link>`,
script tags, or pasted URLs. No same-origin access, no JavaScript, no form needed: the *victim's
browser is the only requirement*. Three of this module's cases are $500 JSON-verified — the
GET lane punches far above its nuisance reputation when the mutated state is business-relevant.

**Case-ID scheme: `CSRF-<report id>`.**

| Impact tier | Cases |
|---|---|
| Private-data exfil door | 226418 (JIRA escalate, $500), 99708 (module 04) |
| Security-state mutation | 174328 (no_auth_mode, $500), 99321 (PayPal activate), 103351 (theme install) |
| Data export/identity binding | 96470 (export users, $500), 111216/114127 (disconnect) |
| Account-state / settings | 5946, 36980, 157956, 223333, 223345, 229405, 230863, 239170 |
| Content/social actions | 249234 ($50), 230837, 100820 (→ module 05), 113857/113865, 115323 |
| Commerce | 6378, 74595, 157993, 93154, 114430 |

## 2. The exfil anchor — CSRF-226418 (HackerOne, $500 JSON-verified)

One GET, private report details out:

> An attacker can steal private reports details through a CSRF in HackerOne report escalation
> to JIRA implementation.
> ### CSRF
> GET `https://hackerone.com/reports/[REPORT_NUMBER]/escalate`

The escalation *sends the private report's content to an external system* — attacker's JIRA —
making the GET a **data-exfiltration primitive**, the highest-value GET shape in the corpus.
Agent lesson: inventory GET endpoints that *copy/push/broadcast state elsewhere*; those are
exfil doors, not settings.

## 3. The security-state anchor — CSRF-174328 (Slack, $500 JSON-verified)

An integration forced out of authenticated mode via one img tag, verbatim PoC:

```html
<html>
<img src="https://vecchiowerther.slack.com/services/88143227125?no_auth_mode=1">
</html>
```

> If the admin will visit this website he will loose the github integration and switch to the
> unauthed mode.

The body's setup is why it pays: the program pre-approves integrations, a normal user cannot
install them — but *any* user holding the integration URI can CSRF the channel admin into
switching it to unauthed mode. **The mutated state weakens a security control.** Same tier as
PayPal-activation 99321 and theme-install 103351.

## 4. The export anchor — CSRF-96470 (Shopify, $500 JSON-verified)

The entire body is a one-line GET form:

```html
<form action="https://app.shopify.com/services/partners/api_clients/1105664/export_installed_users" method="GET">
</form>
```

> change the 1105664 app id to your app id the save as html file and run

Export-by-GET with an attacker-chosen id parameter — the object id in the URL is the *forgery
handle*: point it at your app, the victim's browser exports the install list to you.

## 5. The img-tag canon — CSRF-5946 / CSRF-111216

- **5946 (H1, $100 list)** — the corpus's most compact PoC:
  > how to make unread notifications read!
  > `<img src="https://hackerone.com/notifications/mark_as_read">`
- **111216 (Shopify twitter-commerce, $500 list)** — disconnect with referer-header request
  dump in evidence; the PoC:
  > `<img src="https://twitter-commerce.shopifyapps.com/auth/twitter/disconnect">`

Both are <img> payloads against GET mutations. **114127** (Zomato) is the form-method=GET
variant; **13705** (Simplenote logout, module 01) is the same payload on logout.

## 6. Execution template

```
STEP 1 — hunt the GET-mutation inventory:
  crawl authenticated app; collect every GET that mutates:
  /disconnect, /delete*, /remove*, /reset*, /export*, /escalate,
  /activate, /install*, /?mode=*, /?action=*, /toggle*.
  grep JS for window.location= mutations too.

STEP 2 — confirm the mutation is state-changing (not read):
  replay manually; verify read-back shows the change.

STEP 3 — forge the payload:
  <img src="..."> (fire-and-forget)
  <form method=GET action=...><input name=...></form> (parameterized)
  link on attacker page (needs a click — note the delta in the report).

STEP 4 — two-browser proof:
  victim browser logged in → loads attacker page →
  read-back in victim's own UI shows the mutation.

STEP 5 — impact tier selection (this determines the payout):
  exfil-door > security-state > data-export > identity > settings > content.
  State the tier explicitly; the corpus pays $500 at the top three tiers.
```

## 7. Validation gates (all must pass)

1. **Read-back proof** — the mutation visible in victim's authenticated UI after the img fires.
2. **No-click vs click required** — labeled; no-click img lane is the stronger report.
3. **Object-id handle documented** (96470 pattern) — attacker-controlled parameter in the GET.
4. **SameSite reality check** — modern browsers now block most cookie-bound GET mutations from
   cross-site `<img>` (SameSite=Lax allows *top-level* navigations only); the current-browser
   PoC must use top-level navigation (link/redirect) or document the frame/CSP context. Era
   rows had no such protection — label the difference in the field (playbook P4).
5. **Rate/state restore** — re-enable what was disabled (unauth-mode, PayPal, themes).

## 8. Adjacency

- **CSRF-114430 (shopify.com/plus, $500 JSON)** — the boundary case: a GET *parameter*
  (`insp_pingurln`) makes the victim's page fire an attacker-URL POST carrying page analytics —
  GET-state-change by injected third-party ping, labeled Information Disclosure in the archive.
  Verbatim POST data shows page title/UA/cross-domain context leaking.
- **CSRF-93154 (Imgur)** — token *removed* (not GET): form-validation token stripped, 200
  anyway — module 05 overlap, recorded in 06 as the noise-adjacent settings row it is.
- **Caching lane** — GET-state changes + shared caches = cache-poisoning door (Vault/Cache,
  row 15 pending; hunt-cache-poison skill).
- **Prefetch/scanner amplification** — img-GET lanes are exactly what link previewers fire;
  same payload shape, different victim (hunt-ssrf skill's link-preview matrix).

## 9. Cross-references

- Module 03 — GET lanes chain into ATO when the mutated state is an identity/2FA setting.
- [`references/blogs-index.md`](references/blogs-index.md) §1 — zseano's POST↔GET swap lessons
  (byte-quoted); §2 — writeup cluster on GET-CSRF.
- [`CSRF-Testing-Agent-Playbook.md`](CSRF-Testing-Agent-Playbook.md) — P2 lane decision: GET
  mutations are tested FIRST (cheapest), POST lanes second.
