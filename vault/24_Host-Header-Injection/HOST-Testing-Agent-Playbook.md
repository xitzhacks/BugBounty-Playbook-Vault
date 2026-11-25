---
title: "HOST Testing Agent Playbook — the executable protocol"
type: agent-playbook
category: host-header
cwe: "CWE-707"
built: "2026-11-07"
corpus: "4 classified rows -> 4 bodies read (4 full-body / 0 metadata-only) · 0 adjacent rows"
bounty: "$800 across 2 rows with DB figures (max $500 HOST-1783015) · 2 rows no figure"
companion_modules: "00 host-header-injection (sole module, 4 rows)"
quote_rule: "byte-true, from read bodies only; missing figures recorded never invented"
---

# HOST Testing Agent Playbook — Host Header Injection

*Evidence base: 4 disclosed h1-brain corpus cases (`HOST-…`). Every quoted sentence in the module is byte-true to `references/archive/host-bodies-full-dump.txt`. Read the module before improvising; this file is the operational spine.*

## P0 — Program classification & policy read (before any payload)

1. Program type: commercial bug bounty vs VDP. The corpus pays consumed host values —
   verification links ($300, HOST-1444675) and shared-IP subdomain reach ($500,
   HOST-1783015) — and records no figure for bare reflections. Read policy for allowed
   mail-testing now: only test mailboxes/accounts you control. Never send attacker-host
   mail to production recipients.
2. Environment signal: classify the stack — which components consume `Host`,
   `X-Forwarded-Host`, and `Referer`? The corpus names four consumers: link generation
   (HOST-158019), newsletter mail (HOST-229498), verification/config pages (HOST-1444675),
   and vhost routing (HOST-1783015). Inventory all four before probing any.
3. Kill-gate: no testing yet — P0 produces the *policy envelope* only.

## P1 — Sink inventory (who consumes the host value)

| Consumer | Corpus proof | What to map |
|---|---|---|
| Link / password-reset generation | HOST-158019 ("generate links … even generate password resets links") | Every absolute URL the app mails or renders |
| Newsletter / marketing mail | HOST-229498 (referrer → logo + links in "Welcome" mail) | Signup `Referer` capture points and mail templates |
| Verification / settings pages | HOST-1444675 (dashboard redirect + content spoof, `X-Forwarded-Host`) | `X-Forwarded-Host` handling per page + mailed link |
| Vhost routing / shared-IP router | HOST-1783015 (three subdomains, one IP) | All hostnames on the target IP; which "internal" hosts share it |
| Cache keys | HOST-158019 (claim only) | `Host`-keyed cache entries — journal, do not assume |

Enumerate *every* endpoint that mints a link or mail, then test host-consumption per endpoint
serially before testing cache interactions.

## P2 — Probe protocol (from cheapest signal to hardest)

1. **Alternate-Host reflection** — one request with `Host: <attacker-domain>` (or
   `X-Forwarded-Host: <attacker-domain>` below the real Host, HOST-1444675's exact recipe).
   A 301/200 that reflects the attacker host proves the router trusts the header; nothing
   more. HOST-158019's `Host: google.com` → `Location: https://google.com/` is the
   baseline probe.
2. **Consumer confirmation** — trigger the mail/page the host value lands in. Starbucks'
   capture point was the signup `Referer`, not the Host header (HOST-229498): always test
   *both* header and referrer delivery routes before concluding a consumer exists.
3. **Subdomain reach (vhost)** — Burp Match-and-Replace Host with each sibling hostname on
   the shared IP (HOST-1783015's method). Record which hosts answer, which need auth,
   which serve files — and state what you could not confirm (the $500 row's honesty).
4. **Cache interaction** — only after 1–3: request the cached object, then a second,
   clean fetch proving the poisoned copy is served. A single reflected 301 is the
   kill-gate (HOST-158019 never crossed it).

## P3 — Proof ladder (the modest demonstrations paid)

1. Reflected redirect: request + response pair, attacker domain in `Location`, shown once.
2. Mail proof: the test mailbox's rendered mail with attacker URL in logo/links (or
   verification flow redirected), screenshot named per recipient, test account only.
3. Content-spoof proof: the spoofed recommendation rendered under the trusted domain.
4. Subdomain proof: public-hostname access to an "internal" host's surface — list endpoints
   reached and *explicitly* note any file/upload attempt you could not confirm.

## P4 — Modern hardening fingerprints (never corpus doctrine)

- **Allow-listed Host**: server rejects/allowlists Host at the edge; `X-Forwarded-Host`
  stripped unless the proxy is trusted and the value is allow-listed.
- **Absolute URLs from config**: mail/link generation reads the canonical domain from
  server config, never from the request Host/Referer (HOST-229498's lesson).
- **Vhost isolation**: internal hosts bind to loopback/private interfaces, not the public
  IP (HOST-1783015's lesson — one IP, one router, zero internal reach).
- **Cache keys**: `Host`/`X-Forwarded-Host` normalized or excluded from cache keys
  (HOST-158019's claimed lane).

## P5 — Pre-report gates (kill-gates)

1. **Consumer gate** — you name the downstream consumer (mail link, verification flow,
   cache object, vhost surface). A bare reflection dies here (HOST-158019 at no figure).
2. **Identity gate** — you demonstrated the consumer acted on the attacker value (inbox
   screenshot, second-fetch cache hit, internal-host response). A request log alone is
   not the finding.
3. **Boundary gate** — state what you could not reach (HOST-1783015 could not confirm file
   access — and still paid). Unconfirmed file/upload claims die here.
4. **Recipient gate** — test mailboxes only. Any plan that mails production users dies here
   regardless of signal quality.
5. **Noise gate** — reflection without a consumer, and cache claims without a cached-object
   proof, die here (the HOST-158019 pattern).

## Module ↔ phase table

| Phase | Corpus evidence (module) | Anatomy of the paid pattern |
|---|---|---|
| P1 inventories consumers | 00 (§§2–4) | mail / verification / settings / vhost / cache — HOST-229498's Referer route, HOST-1444675's X-Forwarded-Host |
| P2 probes reflection → consumer | 00 (§§2–5) | `Host` → 301 (158019); `X-Forwarded-Host` → link (1444675); Host swap → subdomain (1783015) |
| P3 proofs ladder, honest ceilings | 00 (§§2–4) | mail render; spoof render; reach-with-unconfirmed-files (1783015) |
| P4 hardening fingerprints | 00 (§§3–4) | config-canonical URLs; allow-listed Host; vhost isolation |
| P5 kill-gates | 00 (§§5–6) | consumer gate; recipient gate; cache-proof gate |

## Non-goals

- Cache-poisoning mechanics beyond the host-consumption primitive — owned by the
  `Cache-Poisoning` vault; this vault cites HOST-158019's claim only as a negative example.
- Password-reset-mail exploitation against production users — outside every module's
  claims; only in-scope test accounts, per P0/P5.
- Subdomain-takeover of dangling-DNS hosts — the `Subdomain-Takeover` vault owns that
  class; HOST-1783015 is live-host vhost reach, not DNS takeover.
