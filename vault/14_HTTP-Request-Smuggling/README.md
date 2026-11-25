---
title: "HTTP Request Smuggling / CRLF vault — parser differentials, header injection, protocol smuggling & negative space"
type: index
category: "HTTP Request Smuggling / Response Splitting / CRLF (desync parser differentials, CRLF/header injection, email-plaintext-protocol injection, adjacent & negative space)"
built: "2026-11-07"
evidence: "36 bucket rows from h1-brain (full bodies, all read end-to-end) + 12 unclassified merges · 48 full-body in archive · 0 empty bodies"
bounty: "$34,290 bucket corpus-floor (19 rows) · $41,190 incl. adjacent merges (23 rows) · max $5,000 (SMUG-1200647) · 19/36 bucket rows carry figures (None = no figure, not $0)"
companion_vaults: "../RCE · ../Race-Conditions · ../SSRF · ../Authentication-Session · ../Cache-Poisoning (row 15)"
case_id_scheme: "SMUG-<HackerOne report id>"
quote_rule: "byte-true, (sic)-marked, from read bodies only; verified against archive/SMUG-bodies-full-dump.txt"
---

# Vault/14 — HTTP Request Smuggling / CRLF

The class's money here is **parser agreement**: when the front-end and back-end
count the same bytes differently, one redirects the victim to you. The corpus
prices it in tiers: CVEs against named tools (Tomcat, llhttp,
undici) pay flat per variant, hijack proofs against live hosts are unfigured,
and Set-Cookie forgery prices at Info unless the Grafana-shaped reach gives you
a shell.

## Start here

| # | File | What it gives you |
|---|---|---|
| 1 | [`SMUG-Testing-Agent-Playbook.md`](SMUG-Testing-Agent-Playbook.md) | **The executable protocol.** P0 program/pair classification → P1 surface inventory (parser pairs, header sinks, config writers) → P2 probe protocol (CL.TE baseline → obfuscation sweep → desync+victim race → CRLF oracle → SMTP oracle → config-CRLF → version fingerprint) → P3 proof ladder → P4 modern hardening fingerprints → P5 kill-gates. |
| 2 | [`01_Request-Smuggling-Desync.md`](01_Request-Smuggling-Desync.md) | Desync parser differentials (22 rows, $27,740): Tomcat trailer CVE-2023-45648 ($4,660), CSD CVE-2024-21733 ($4,660), CL.TE hijacks (slackb.com, Zomato), obfuscated TE catalogue, llhttp drift, Apache pause desync, Turbo Intruder victim-race weaponization. |
| 3 | [`02_CRLF-Header-Injection.md`](02_CRLF-Header-Injection.md) | CRLF/header injection (9 rows, $1,300): response splitting & Set-Cookie forgery, undici host/content-type gaps, urllib→Redis SSRF, OAuth redirect_uri, tweet `%0d` display trick, stored filename control bytes. |
| 4 | [`03_Email-Protocol-Injection.md`](03_Email-Protocol-Injection.md) | Plaintext-protocol injection (4 rows, $5,000): Grafana SMTP password → `rendering_args` → RCE ($5,000, vault max), nextcloud/calendar SMTP `RCPT TO`→`EHLO` oracle twins, ownCloud LDAP password → SMTP/Redis RESP → web shell/replication/SSH key. |
| 5 | [`04_Adjacent-and-Negative-Space.md`](04_Adjacent-and-Negative-Space.md) | Negative space (13 rows, $7,150): the $250 cart-quantity mislabel, Apache HTTP/2 + mod_proxy_ajp parser pairs (paid $1,200/$2,400 but bucket-unclassified), GHSL one-liners, CodeQL detector tickets, the classifier-vs-body lesson. |

## Scoreboard (36 bucket rows · 19 paid · $34,290 · max $5,000)

| Case | Title (short) | Program | Bounty | CVE |
|---|---|---|---|---|
| SMUG-1200647 | Grafana RCE via SMTP server parameter injection | aiven_ltd | **$5,000** (max) | — |
| SMUG-2327341 | Tomcat client-side desync (CSD) | ibb | **$4,660** | CVE-2024-21733 |
| SMUG-2299692 | Tomcat trailer misparse | ibb | **$4,660** | CVE-2023-45648 |
| SMUG-2280391 | Tomcat trailer size-limit desync | ibb | **$4,660** | — |
| SMUG-1667974 | Apache pause-based desync | ibb | **$4,000** | — |
| SMUG-1630667 | Multi-line TE parsing (llhttp) | ibb | $1,800 | CVE-2022-32215 |
| SMUG-1630668 | Flawed TE parsing (llhttp) | ibb | $1,800 | CVE-2022-32213 |
| SMUG-1630669 | Header-field delimiting (llhttp) | ibb | $1,800 | CVE-2022-32214 |
| SMUG-2032842 | CR-only delimiter (llhttp) | ibb | $1,800 | CVE-2023-30589 |
| SMUG-726773 | CL.TE on labs.data.gov (Turbo race, 67 reflections) | gsa_bbp | $750 | — |
| SMUG-713285 | pscp.tv/periscope.tv multi-subdomain desync | x | $560 | — |
| SMUG-965267 | webrick `AAAchunkedBBB` regex fake | ruby | $500 | — |
| SMUG-1002188 | Node duplicate TE (TE-TE) | nodejs | $250 | CVE-2020-8287 |
| SMUG-1238099 | llhttp chunk-extension newline | nodejs | $250 | CVE-2021-22960 |
| SMUG-1238709 | llhttp space-before-colon | nodejs | $250 | CVE-2021-22959 |
| SMUG-1878489 | undici `host` header CRLF | ibb | $600 | CVE-2023-23936 |
| SMUG-409512 | Apache mod_userdir response splitting | ibb | $500 | CVE-2016-4975 |
| SMUG-2147132 | Bugzilla OAuth `redirect_uri` CRLF | mozilla | $200 | — |
| SMUG-246803 | [spectacles cart-quantity] bucket-adjacent business logic | snapchat | $250 | — |
| SMUG-737140 | CL.TE hijack → bulk `d`-cookie theft, slackb.com | slack | - | — |
| SMUG-771666 | CL.TE `tabprefix1` → bulk X-Access-Token theft, api.zomato.com | zomato | - | — |
| SMUG-867952 | CL.TE leading-space TE, console.helium.com | helium | - | — |
| SMUG-919175 | Double TE + `identity` → cache poisoning, basecamp.com | basecamp | - | — |
| SMUG-867577 | Dual valid/invalid TE → unauth desync, launchpad.37signals.com | basecamp | - | — |
| SMUG-753939 | Leading-space TE → HMAC error reflection / DoS, fortmatic | magic-bbp | - | — |
| SMUG-922597 | Node CR-to-hyphen rename (`Content[CR]Length`) | nodejs | - | CVE-2020-8201 |
| SMUG-735748 | Malformed TE (PDF-only writeup) | nodejs | - | CVE-2019-15605 |
| SMUG-237357 | vpn.bitstrips.com Set-Cookie forgery | snapchat | - | — |
| SMUG-858650 | starbucks response splitting | starbucks | - | — |
| SMUG-712979 | Tweet `%0d` displayed-vs-parsed URL | x | - | — |
| SMUG-590020 | urllib CRLF → Redis packet SSRF | ibb | - | CVE-2019-9947 |
| SMUG-1402249 | Nextcloud leading/trailing control bytes in names | nextcloud | - | CVE-2022-24888 |
| SMUG-1664019 | undici `content-type` header CRLF | ibb | - | CVE-2022-35948 |
| SMUG-1054282 | ownCloud LDAP password → SMTP/Redis RESP | owncloud | - | — |
| SMUG-1509216 | Nextcloud calendar SMTP `RCPT TO` injection | nextcloud | - | — |
| SMUG-1516377 | Nextcloud iCalendar `ORGANIZER` SMTP injection | nextcloud | - | CVE-2022-31014 |

Corpus program mix: ibb 13 · nodejs 6 · nextcloud 3 · snapchat 2 · x 2 ·
basecamp 2 · aiven_ltd, slack, zomato, helium, starbucks, ruby, gsa_bbp,
magic-bbp, mozilla, owncloud 1 each. (+12 unclassified merges: ibb 4 ·
github-security-lab 5 · vimeo, ui, x 1 each).

## Vault map

| File | Content |
|---|---|
| `SMUG-Testing-Agent-Playbook.md` | Agent-facing operational playbook: P0–P5 phases, module↔phase table, non-goals |
| `01_Request-Smuggling-Desync.md` | CL.TE/TE.CL/TE.TE, obfuscated TE, llhttp grammar drift, trailer/pause/CSD rows, victim-race weaponization |
| `02_CRLF-Header-Injection.md` | Response splitting, Set-Cookie forgery, library validation gaps, display/storage lanes |
| `03_Email-Protocol-Injection.md` | SMTP/LDAP/Redis protocol injection, Grafana rendering_args RCE |
| `04_Adjacent-and-Negative-Space.md` | Mislabels, unclassified merges, detector tickets, the bodies-win ledger |
| `references/source-index.md` | Provenance (h1-brain DB, sha256, 3,673 rows), funnel (3,673→36), classification mechanics, 7 limitations |
| `references/case-register.md` | 48-row ledger with DB metadata (weakness/asset/CVE/bounty), class census, bounty arithmetic |
| `references/archive/SMUG-bodies-full-dump.txt` | All 48 bodies verbatim (anchor for every quote) |
| `references/archive/classes.json` | Frozen module assignment for all 48 rows |
| `references/archive/meta.json` | Build metadata snapshot |

## Cross-vault links

- `RCE/` — SMUG-1200647 (Grafana `rendering_args`→RCE, $5,000) and SMUG-1054282 (Redis→web shell) are RCE delivered by CRLF; its bullet case-sentences should cite this vault for the newline primitive.
- `Race-Conditions/` — SMUG-726773/867577/753939's Turbo Intruder `desync + N victim-race` scripts are the race vault's gate-sync primitive aimed at request poisoning instead of ledger state.
- `SSRF/` — SMUG-590020 (urllib CRLF → internal Redis packet stream), SMUG-919175 (smuggled `X-Forwarded-Host` cache poisoning): smuggled/poisoned dests are its internal-network play.
- `Authentication-Session/` — SMUG-737140/771666 (bulk session-cookie theft via request hijack) and SMUG-2147132 (redirect_uri session manipulation) are session-theft-via-protocol: the smuggle supplies the hijack, this vault supplies the token.
- `Cache-Poisoning/` (master row 15, upcoming) — SMUG-867577/919175 desync→poisoned-socket→persistent cache poisoning is the same technique in its persistence lane.
- `Business-Logic/` (master row 12, built) — SMUG-246803 (spectacles cart quantity) is business logic with a smuggling label; its technique lives there.

## Limitations

1. **Bucket boundary is classifier v1 (weakness labels `HTTP Request Smuggling` + `CRLF Injection`)**. The 36-row bucket is the vault's count basis; the 12 unclassified merges are included only via the documented module_map scan, and a v2 sweep of the 468-row pool may add more.
2. **Weakness labels are historical triage artifacts** — the same class is labeled `HTTP Request Smuggling` on a business-logic cart row, `CRLF Injection` on SMTP/RCE rows, `SSRF`/proxy labels on Apache/HTTP-2 rows, and unlabelled on GHSL one-liners. Bodies are the class authority.
3. **Bounty `None` ≠ unpaid.** It means the DB row has no figure. 17 of 36 bucket rows carry no figure; $34,290 is a corpus-floor, not a total.
4. **Attachment-only + one-liner rows** (SMUG-735748 PDF-only; CVE-2022-32213/32214/32215 trio one-liners pointing at Original Reports) carry no quotable payload — anchors, not evidence; five of the twelve merges are CodeQL detector tickets (module 04 §3).
5. **Chainpay vs pure smuggling**: SMUG-1200647 ($5,000, vault max) pays because the CRLF feeds `$IFS` shell-args on a renderer — the same class at `$0`-$750 when the reach is a mail spoof or a redirect proof.
6. **Era honesty** — desync tooling (smuggler 2018, Turbo Intruder victim-race scripts, llhttp-era CVEs) is historical evidence 2014–2024, not current best stack.
7. **QA**: all block quotes in modules were byte-verified against `references/archive/SMUG-bodies-full-dump.txt`; `(sic)` marks author typos.


<!-- CASESTOCK-LINK:BEGIN -->

## Case stock — vault (`_VAULT/`)

**214 disclosed reports** routed to this category · 49 with a bounty figure · **$118,670** · 142 full write-ups stored locally.

- Full list: [`_VAULT/by-vault-category/14_HTTP-Request-Smuggling.md`](../_VAULT/by-vault-category/14_HTTP-Request-Smuggling.md)
- Query: `sqlite3 ../_VAULT/reports.sqlite "SELECT id,bounty,title FROM reports WHERE ..."`
- Pull one write-up: `python3 ../_VAULT/scripts/extract_report.py <id>`

| Top paid | Program | Bounty |
|---|---|---|
| [510152](https://hackerone.com/reports/510152) Bypass for #488147 enables stored XSS on https://paypal.com/signin again | PayPal | $20,000 |
| [488147](https://hackerone.com/reports/488147) Stored XSS on https://paypal.com/signin via cache poisoning | PayPal | $18,900 |
| [1211724](https://hackerone.com/reports/1211724) HTTP Request Smuggling via HTTP/2 | Basecamp | $7,500 |
| [1478633](https://hackerone.com/reports/1478633) HTTP Request Smuggling in Transform Rules using hexadecimal escape sequences in  | Cloudflare Public Bug Bounty | $6,000 |
| [957881](https://hackerone.com/reports/957881) HTTP request smuggling (?) canpol.deti.mail.ru | Mail.ru | $5,000 |

_refreshed 2026-11-17 from the public HackerOne disclosed-report dataset_
<!-- CASESTOCK-LINK:END -->
