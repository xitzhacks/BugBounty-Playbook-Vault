---
title: "FU Testing Agent Playbook — the executable protocol"
type: agent-playbook
category: fup-all
cwe: "CWE-434, CWE-22, CWE-98, CWE-918"
built: "2026-11-05"
corpus: "86 mirror rows → 65 bodies read (58 resolved / 7 informative) · 21×404 recorded · 0 metadata rows (18 summaries-sourced)"
bounty: "$71,869 all-envelope (JSON $3,426/8 · list $41,815/26 · dead-list $26,628/12) · class modules 01–09 $45,241/34 paid of 65"
companion_modules: "01 unrestricted-upload-exec · 02 upload-url-ssrf · 03 upload-stored-xss · 04 file-inclusion · 05 path-traversal · 06 rfd-browser-download · 07 server-file-download · 08 upload-acl · 09 adjacent-noise-shelf"
quote_rule: "byte-true, from read bodies only; 404 rows recorded never quoted"
---

# FU Testing Agent Playbook

Executable protocol derived from 65 read bodies (2014-2017 era) + guide doctrine from the
two byte-quoted sources (BBH `fileuploads` guide; PortSwigger academy frame) + modern
discipline from the hunt-file-upload skill matrices. Every step cites corpus evidence.
Run phases in order; abort at kill-gates. Crown-jewel doctrine up front: **payouts track
what the object reaches after landing** — an authless device CGI paid $18,000 (FU-73480)
because nothing between you and the disk asked who you were; a processor that obeyed
markup paid $800 (FU-115857) because the playlist reached `/etc/passwd`; the same class
*stopped* at an error message paid $25–$100. Do not charge HTTP-200-with-echo.

## P0 — Program classification & policy read (before any payload)

1. Program type: commercial vs VDP. The upload-class corpus is *program-shaded*: the five
   flagship prices ($18,000/$5,000/$2,500/$2,000/$1,500) span carrier-firmware, image
   platforms, a browser vendor, the reporting platform itself, and social-platform frame
   plumbing; the download lane's seven DoD rows resolved unpaid and carried severity tags
   only (marketplace award fixed sums). Read
   the policy's file-upload and path-disclosure clauses first — FU-158021's reporter
   correctly framed an unpriced-in-policy finding ("Firstly,I couldn't see anything about
   Path Disclosure in your policy") and still collected $100 (json).
2. Environment signal: hybrid estates (device lanes: airMAX/airFibre rows are
   authentication-omission buyers), CDN-served upload destinations (mopub/Instacart-era
   `*.amazonaws.com`), staging first (jsDelivr 18371 died on staging), and shared-platform
   plugins (Phabricator skins; WP/BuddyPress installs).
3. Kill-gate: no testing yet — P0 produces the *policy envelope* only, plus the egress
   rule (does the program allow connecting out to a personal listener? 97501/115857/228377
   all ran external probes).

## P1 — Surface inventory (upload-ingress, storage, serving, post-processing)

1. Enumerate every upload ingress by *consumer*, not by form: profile/photos, documents,
   attachments, avatars, theme/logo assets (155690), app icons (97672), restore/import
   (213558), API-received files (254200's `apiv2/user/upload`), plus the
   *non-form* lanes — FTP (45368), apps-platform stores (84374), device CGIs (73480,
   201529), and third-party-SDK surfaces (167481, 258460).
2. Enumerate the serving layer: where does the file render (CDN/`*-assets` subdomain/FPM)?
   Is a processor in the chain (ImageMagick/rmagick — 135072/158016; ffmpeg/Lavf — 115857)?
   What does the upload *page* itself echo (31187's `bk` style injection)?
3. Enumerate the stored-object's second life: who can list it (97452's `/admin/rte/assets`),
   who can read it (143903, 43850), can its goto-URL be name-controlled (254200)?
4. Kill-gate: if no upload of any kind exists but URL-based file read/download handlers
   exist (186326, 230714), proceed with module 07's shape (download-lane) — the vault
   counts it as the same class, lower priced.

## P2 — Probe protocol (from cheapest signal to hardest)

1. **The .txt ladder** (BBH guide §1a discipline, every era): upload `test.txt` — if
   accepted, the filter's shape is known; then `.html`, `.php`, `.xml`; then the
   URL-encoding bypass paragraph ("Null bytes, %00, New lines, %0d%0a and tabs, %09 %07")
   and the case variants (guide's caution: ".PhP, although uncommon in 2022"; the same
   rename race as 145604's `image1.php`).
2. **Filename smuggle**: `zseano.php/.jpg`, `test2../../.../test2.jpg` (254200),
   `Dinosaurs secret life<img src=x onerror=alert(1)>.png` (203515) — names echo into
   error l10n (WP), S3 keys (Unikrn), or title fields (45368).
3. **Content-type swap**: keep extension, swap MIME (97672's `.jpg`→`text/html`; both
   the guide's traversal and the mopub row annotate the same swap point).
4. **type=file → type=url flip** (713's opener): every remote-URL image field becomes a
   server-side fetch — probe localhost/ports/banners, then request external (97501 style
   netcat), then upstream log reading (228377's gopher hop).
5. **Processor-after-the-transfer**: upload the MVG (135072) or the
   playlist-with-`concat:` (115857); if error text is returned, harvest the
   delegate/tmp-path lines first (158021) and diff localhost responses for port oracles
   (159820).
6. **Traversal ladder on read params**: `imageid=../../../../../../../../../../etc/passwd`
   (122475); archive lanes: `ln -s` inside a tgz (213558); OS-mixed separators if a
   strpos() guard is visible (147570); double-encoded overlong UTF-8 `%25c0%25af`
   (18371) when a front decoder exists.
7. **Delete flows**: replay crop/delete (`original_file=…/../../wp-config.php`, 183568)
   with intercept-on-crop exactly as the body describes.
8. **RFD probes**: JSON reflection endpoints + appending `.bat`/`.cmd`
   (39658 → 50658 → 107960) and the redirect-with-307/308 upload test (51265's SWF shape).
9. **ACL probes**: second account A/B (43850), shelf-page listing (97452), id-swaps
   (`clip_id`, IM channel id 143903), and mobile: exported receipt + manifest lines
   (167481/258460 before claiming).
10. Kill-gate probe hygiene: chain each probe to its expected *observable* — banner text,
    tmp-path in a JSON error, authless-201 response, payload bytes at the landed URL —
    and stop at P3 when one lands.

## P3 — Proof ladder (the modest demonstrations paid)

1. Read evidence: bytes at the landed URL (213558 step 12, 122475's `/etc/passwd` title
   quote); payload in an error quote (158021); signature-defeat demo (191243).
2. Exec evidence: `phpinfo()` at the served path (84374), OOB hit on your listener
   (97501 nc lines, 135072 wget callback), deleting wp-config.php and site-down
   (183568's own impact sentence).
3. ACL evidence: `clip_id` A/B (43850), rte/assets screenshot equivalents (97452),
   channel-id upload with the receiving account observing (143903).
4. Mobile evidence: malicious receiver/service + the manifest lines from the body + stolen
   object at the listener (258460, 167481).
5. RFD evidence: browser-download orchestration page + the final interpreter receipt
   (107960 download-attribute + 51265 swf hosted on any site).

## P4 — Modern hardening fingerprints (never corpus doctrine)

- Signed/parameterized uploads (presigned POST URLs, per-object keys) as the default
  replacement for in-app multipart — the bar the guide's era never saw.
- Blob validation before accept: magic-byte + decode round-trip server-side — this is the
  class of fix that shakes 203515's filename-in-error family loose.
- Egress filtering on image/playlist processors (ffmpeg allowlists; ImageTragick-era
  delegate bans for web use).
- Keyed access instead of object listing (97452/43850 lanes): object-identity checks
  against the uploader, not URL-knowledge checks.
- CSPT research (client-side path traversal → CSRF, blogs-index §3 doyensec 2024) — the
  modern successor to the upload-URL lanes when SSRF is blocked; CSRF-lane cross-check.
- Test the *serving* side today: MIME sniffing (anotherhackerblog Pt.1/Pt.2) sits between
  97672 and 203515 on the same skeleton.
- Pricing memory (post-mirror ladder): LFI $13,337 ("springboard.google.Com") and the
  Starbucks webshell (506646) rows live in bibliography §3 only.

## P5 — Pre-report gates (kill-gates)

1. Say the observation the body said: each claim tied to an artifact (a URL, a log line, a
   renamed file).
2. Record the honest ceiling the body recorded: 201529's disk-fill ceiling, 155690's
   "executed that file as text", 158505's informative landing — these were *priced*.
3. Never claim the interpretation the title fuzzed (14092's `RFI` = `<img>` load) or the
   program's misfiled money (258117's Jenkins row) without the refile note.
4. Cross-vault checks: 135072/84374/116575/258117/142562 (RCE), 105787/232614 (XXE),
   158016 (CSRF), 51265 (Open-Redirect) — report each only under its class's correct lane;
   quote the other vault's register row as corroboration, never as double-count.
5. DoD lanes: severity tags (`critical 184596`, `high 183978`) never imply bounty scale;
   the seven DoD download rows read like sibling traces, not repeated claims.

## Module ↔ phase table

| Module | Phase emphasis | Skip if |
|---|---|---|
| 01 unrestricted→exec | P1(1) + P2(1)–(2) + P3(2) | No upload accepts stored content (WAF-only target) |
| 02 upload-url SSRF | P1(2) + P2(4)–(5) + P3(2) | All uploads are opaque pins with no remote-URL field |
| 03 upload stored-XSS | P2(1)–(3) + the serving-host check (P1(2)) | Serving host forbids HTML content-binding |
| 04 file inclusion | P1(3/4) + P2(6) + P3(1) | No include()/directive path reachable |
| 05 path traversal | P2(6)–(7) + P3(1)–(2) | All object writing pinned (fixed keys + signed locations) |
| 06 RFD/browser | P2(8) + P3(5) | No JSON reflection + browser served from same origin |
| 07 server download | P1(4) + P2(6) | No parameterized download handlers |
| 08 upload-ACL | P2(9) + P3(3)–(4) | Single-tenant uploads only |
| 09 shelf | P5 gates | n/a (it is the refile lane) |

## Non-goals

- Never inflate XXE payload-impact beyond what the chain shows (232614 states the RCE
  possibility but its proof is file-read; your report stays file-read scoped unless a
  second chain is shown).
- Never collide the cross-vault lanes: the money row lives in one register; cross-notes
  get a class line, not a second price.
- No live testing is prescribed by this vault's tables — every entry is evidence-derived
  (65 read bodies), not a lab attempt.
