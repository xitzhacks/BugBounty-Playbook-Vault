---
title: "Adjacent & Noise Rows — text injection, content spoofing, redirect-target compromise, non-redirect roster matches"
type: playbook
category: adjacent-noise
source_count: 12
full_bodies_available: 12
corpus: "h1.security.nathan.sx roster (198 rows), bodies via hackerone.com/reports/<id>.json"
list_accessed: "2026-10-28"
note: "All 12 bodies read 2026-10-29. 1 true noise row (RDIR-29480); 11 adjacent rows recorded with dispositions. Bounty figures sit outside the pure-redirect-class totals."
---

# Adjacent & Noise Rows — what the title filter caught that isn't (exactly) this class

## 1. Overview

Twelve rows the title filter caught whose bodies put them outside the pure redirect class. They
are kept — the vault-wide discipline: **recorded, classified, excluded from class counts, never
silently dropped.** One is true noise; eleven are adjacent classes worth knowing from this corpus.

| Row | Class | Body verdict |
|---|---|---|
| RDIR-29480 | NOISE | IRC command injection — no redirect mechanism ($300 json) |
| RDIR-191196 | adjacent | G Suite authorization → ubereats.com HTTP-redirect DoS ($2,500 list) |
| RDIR-158148 | adjacent | reverb.twitter.com → reverb.guru; reporter RCE'd the redirect target ($560 list) |
| RDIR-218705 | adjacent | unregistered forward-domain in support docs |
| RDIR-213056 | adjacent | redirect_uri 404 path echo → content spoof |
| RDIR-114529-family | (in 01) | message+redirect content spoof — kept in 01 (param manipulation) |
| RDIR-106348/106350/138786 | adjacent | 404-page attacker-text echo (phishing) |
| RDIR-66994 | adjacent | soft-hyphen link-splitting (informative) |
| RDIR-209821 | adjacent | profile-statement malicious links (informative) |
| RDIR-151831 | adjacent | profile links not routed via redirect service (duplicate) |
| RDIR-186862 | adjacent | order-phishing via GET payment-id (informative) |

## 2. Why the adjacent rows matter anyway

- **RDIR-191196 ($2,500 list — the class's third-largest figure)** — a redirect *not on the web
  app*: the reporter pointed `ubereats.com` via G Suite A-record/authorization abuse and the
  redirect chain DoS'd customers. Team summary:
  > The combination of an authorization flaw in Google's G Suite and a misconfiguration on Uber's
  > behalf, allowed @uranium238 to set up an HTTP redirect for the domain ubereats.com. For some
  > UberEats customers, this resulted in not being able to use the service for a short period of
  > time.
  Lesson: the redirect surface includes **everything between the user and the origin** — DNS and
  auth-provider misconfig produce redirect bugs with Critical-scale impact and zero web payloads.
- **RDIR-158148 ($560 list)** — the redirect *target* was compromised:
  > http://reverb.twitter.com redirects requests to http://reverb.guru which hosts a vulnerable PHP
  > application. I managed to get RCE there which allows to modify the contents of this site, so
  > that reverb.twitter.com will redirect to a phishing page or force a malicious file download.
  Lesson: a redirect chain is only as trusted as its weakest hop. Owned redirect targets =
  phishing hosting on the trusted first hop. (The RCE itself — bulletproof-JPEG webshell — is
  `../` file-upload doctrine.)
- **404-text cluster (106348 $100 json, 106350 $250 json, 138786)** — two reporters, three
  programs, one template: 106348/106350 are the same reporter (djamel-ghorab; Algolia +
  withinsecurity), 138786 is a second reporter (kanwar) on Veris with the same template. The
  106350 echo, verbatim:
  > "It has been changed by a new one https://www.crowdcurity.com so go to the new one since this
  > one was not found on this server."
  Phishing-class, not redirect-class.
- **RDIR-66994 (Slack, informative)** — `%c2%ad` (soft hyphen) splits a pasted link into two
  clickable targets (`http://g` + `oogle.com`); browser-text-level phishing.
- **RDIR-186862 (PortSwigger, informative)** — order-id in GET (`CCPayment.aspx?id=`) lets an
  attacker pre-fill a payment page — phishing via parameter, no redirect.
- **RDIR-209821 / 151831 (gratipay)** — profile-statement links; proposed fix "redirect via the
  server" is the missing outbound-link service — the class's infrastructure angle.
- **RDIR-218705** — support doc advertises `@security-h1-forward.com` (unregistered) —
  forward-domain hygiene; caught by the `forward` arm.
- **RDIR-213056** — `logs.nextcloud.com/redirect_uri?<text>` 404 echoes path — content spoof.

## 3. Triage doctrine for the agent

1. **Noise happens; it pays to know why.** 29480 matched on "unvalidated" alone. When a row's body
   has no redirect mechanism, classify noise in the register and move on — but log the matched arm
   that caught it (helps tune future filters).
2. **Adjacent ≠ worthless.** 191196 is $2,500 and 158148 hosts malware on a trusted redirect chain —
   both are redirect-ecosystem finds whose mechanism lives in another module.
3. **Exclusion is from class counts, not from the record.** The register keeps every row with a
   verdict; module frontmatter counts exclude 08 rows.

## 4. Validation gates (for adjacent classes)

1. 404-text rows: show the echoed text + argue user-visible phishing context (106350's
   "It has been changed by a new one https://www.crowdcurity.com so go to the new one" echo is
   the demo).
2. Redirect-target compromise (158148): show the chain hop + the controlled content on the target.
3. DNS/auth-provider redirects (191196): show resolution + impact window (the DoS frame).

## 5. Archive-label honesty

- Module 08 tagged bounty: $3,710 ($2,500 + $560 + $250 + $100 + $300 noise) — sits outside the
  pure-redirect-class total of $36,523.
- 151831 is a duplicate disposition; 186862/209821/66994/213056 informative.

## 6. Cross-references

- Master list rows 12 (business logic — order-phishing), 29 (clickjacking — the GitLab weakness
  labels), 14 (response splitting), `../` file-upload doctrine (158148's webshell).
