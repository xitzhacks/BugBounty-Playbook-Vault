# RVDP Pattern — Responsible Vulnerability Disclosure Programs (no-automation rule)

Source case: Ather Energy RVDP (https://www.atherenergy.com/bug-bounty), tested 2026-07-28.

## What an RVDP is
A company-run disclosure program, NOT a platform like H1/Bugcrowd. Key differences from
a normal bounty:
- Rewards are usually **discretionary** ("at the discretion of [company]").
- They frequently **explicitly ban automated tools/scripts** with disqualification wording.
- A named IN-SCOPE asset list (e.g. 4 web hosts + 2 mobile apps) — everything else is out.
- A long OUT-OF-SCOPE vulnerability-class list (self-XSS, open-redirect, rate-limit,
  headers/methods, host-header injection, CSRF login/logout, user enumeration, DoS,
  SPF/DMARC, SSL/TLS, price-manipulation-without-transaction, etc.).
- Confidentiality clauses: no public disclosure, report to a named security email.

## The trap
Standard bug-bounty recon starts with subfinder -> gau -> katana -> ffuf -> nuclei. On an
RVDP with an automation ban, doing that FIRST = instant disqualification + possible IP
block. This is the single most common first-move mistake on RVDP targets.

## Correct approach (passive-only recon)
- Read scope page FIRST (see PART 0.5).
- Passive subdomain sources only: `subfinder` (passive), `assetfinder`, crt.sh cert
  transparency (`https://crt.sh/?q=%25.target.com&output=json`). NO dnsx/shuffledns
  brute-force, NO naabu port scan, NO active probing beyond single GETs.
- JS/URL analysis: fetch the page, download referenced JS bundles, statically grep for
  API endpoints / subdomains / secret candidates. (Reading what the browser already
  serves is passive; no fuzzing.)
- Manual browsing of the named in-scope hosts only. Respect edge WAF (Cloudflare bot
  mgmt will 403 curl; use a real browser / normal UA for single GETs).
- If a host hard-blocks the browser (Cloudflare "Sorry, you have been blocked"), STOP
  hammering — it trips their WAF and violates "no disruptive testing".

## Authentication reality
The rewarded bug classes (IDOR on account data, broken access control, auth bypass) sit
BEHIND a valid session. On an RVDP you:
- Must NOT access others' PII — test on YOUR OWN account data only.
- Ideally use TWO self-owned accounts to replay object IDs for horizontal IDOR.
- Prep authenticated request templates for the user to run; do NOT fabricate sessions.

## Report shape
Email to the named security address with the program's exact subject/body format.
Impact-first, proof-of-concept as an attachment sent directly (not uploaded to 3rd-party
sites). No public disclosure without written consent.
