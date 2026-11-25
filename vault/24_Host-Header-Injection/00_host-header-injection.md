---
title: "Host Header Injection — who consumes the host value decides the price"
type: playbook
category: host-header-injection
cwe: "CWE-707"
source_count: 4
full_bodies_available: 4
corpus: "h1-brain disclosed_reports.db (3,673 rows), bucket host-header (classified.json) -> module host-header-injection (module_map_all.json)"
list_accessed: "2026-11-07"
note: "Anchor bodies: HOST-1444675 (Omise, $300), HOST-1783015 (UrbanCompany, $500). Claims trace to bodies read 2026-11-07."
---

# Host Header Injection — who consumes the host value decides the price

## 1. Overview

Four rows, four programs, **$800 / 2 rows with figures** (max $500). The class's pricing rule
is visible in miniature: a bare redirect demo (Instacart, `None`) and a newsletter-mail
redirect (Starbucks, `None`) carry no listed figure, while a verification-mail redirect +
content-spoof bundle (Omise, $300) and a one-IP subdomain bypass (UrbanCompany, $500) do.
The host header is trusted in more places than developers admit — link generation, mail
templates, cache keys — and each consumer prices the flaw differently.

**Case-stock (4 rows / $800):**

| Case | Target | Mechanism | Bounty |
|---|---|---|---|
| [HOST-158019](https://hackerone.com/reports/158019) | instacart | `Host: google.com` → 301 to outside domain (cache-poisoning claim) | — |
| [HOST-229498](https://hackerone.com/reports/229498) | starbucks | Newsletter `Referer` → attacker URL in "Welcome" mail | — |
| [HOST-1444675](https://hackerone.com/reports/1444675) | omise | `X-Forwarded-Host: bing.com` → verification-link redirect + content spoof | $300 |
| [HOST-1783015](https://hackerone.com/reports/1783015) | urbancompany | Host swap → three "internal" subdomains on one IP | $500 |

## 2. The mail is the sink

Two of the four rows are the same shape: an attacker value is stored once and then rendered
into a *mail* the victim trusts. HOST-229498 (Starbucks) is the cleaner specimen because the
body names the capture point precisely — the *referrer attribute* on every newsletter signup
box, not the Host header itself — and then shows the mail consequence:

> There's a host header injection vulnerability via all newsletter signups in the referrer attribute. This works with all pages that have "Join our email list" signup boxes.

> As a result my url https://r1otnetsec.herokuapp.com/ is sent in place of the normal starbucks url. Clicking the image url sends the user to the malicious page.

The logo *and* the other links redirect; the researcher notes a per-session path tweak
("I can make another directory for the other links to redirect perfectly with the session
cookie name") and the credential-theft intent ("This makes it very easy to steal customer
credentials by redirect"). Both paid rows in the corpus share the mail-ward direction; the
two `None` rows do too, which is why the module prices *consumer trust* (transactional mail,
verification links) rather than the injection itself.

## 3. Verification-link + content-spoof: the paid bundle

HOST-1444675 (Omise, **$300**) is the vault's tightest paid row because it bundles two
consumers in one request (add `X-Forwarded-Host: bing.com` below the real Host):

> The https://dashboard.omise.co/test/dashboard website is vulnerable to an Open Redirection flaw if the server receives a crafted X-Forwarded-Host header.

The second consumer is the test/settings page, where the reflected URL under the trusted
domain presents attacker-chosen content ("a valid webpage with malicious recommendations and
the user believes the recommendation as it was from the stock website"). The impact section
names both prices explicitly — redirect to phishing, and spoofed content under the trusted
context — and the $300 tier is the corpus's answer to "redirect + spoof, one header."

## 4. The one-IP subdomain bypass: SSRF-labeled, Host-decided

HOST-1783015 (UrbanCompany, **$500**, the vault max) is the corpus's best *defensive-posture*
specimen: three subdomains (`av`, `ims`, `mesh`) that "should be presumably only for
internal/trusted sources" all answer on one IP, so a Host swap through Burp's Match-and-Replace
reaches them from the public hostname. The summary is one line:

> Ability to access certain subdomains (which should be presumably only for internal/trusted sources ) through host header manipulation.

The body is honest about its ceiling — the researcher could not confirm file access on the
mesh host, could not force an upload, and wrote the impact as a conditional ("Impact is
dependent on whether ability to access the subdomains in question is considered as a
bypass"). The DB weakness label (`Server-Side Request Forgery (SSRF)`) names the *consequence*;
the body names the *primitive* (host manipulation). Bodies win. The pricing lesson: the
bypass paid $500 as a *reach* finding even with access unconfirmed — the corpus prices the
shared-IP router, not the file read.

## 5. The generic-cache claim: Instacart, recorded at its actual weight

HOST-158019 (Instacart, `None`) is the corpus's most-quoted and least-priced row. Its first
paragraph is the class manifesto — developers trusting Host to "generate links, import scripts
and even generate password resets links" — and its PoC is a single request/response pair
(`Host: google.com` → `Location: https://google.com/`):

> Your website is vulnerable to Host Header Injection because the host header can be changed to something outside the target domain

> In many cases, developers are trusting the HTTP Host header value and using it to generate links, import scripts and even generate password resets links with its value. This is a very bad idea, because the HTTP Host header can be controlled by an attacker. This can be exploited using web-cache poisoning and by abusing alternative channels like password reset emails.

The vault keeps the row at its actual corpus weight: an unauthenticated redirect reflection
with a cache-poisoning *claim* and no cache-poisoning *demonstration* (no cached object, no
second victim, no TTL evidence). The module cites it for the consumer taxonomy (links, mail,
cache) and for the playbook's cache-proof gate — not as proof that the cache was poisoned.

## 6. What pays, what doesn't

- The corpus pays **consumed host values**, not reflections: Omise's verification-link
  redirect + content-spoof bundle ($300) and UrbanCompany's shared-IP subdomain reach ($500)
  both show a consumer downstream of the header. The two `None` rows (Instacart redirect
  reflection, Starbucks referrer→mail) show the primitive with the consumer present but the
  demo thinner — the DB records no figure, which the vault keeps as "no figure," not $0.
- **Bounce-back is not a finding.** A 301 that reflects an attacker Host proves the router
  trusts the header; it pays in this corpus only when a mail, a verification flow, a cache,
  or a shared-IP router consumes it. HOST-158019 is the negative-space anchor for that rule.
- **Honest ceilings paid here.** UrbanCompany's researcher could not confirm file access and
  said so ("I was unable to confirm"), and still collected $500 for the reach. The corpus
  rewards a *stated* boundary over an inflated claim — the playbook's boundary gate writes
  this down.
- **No password-reset row at a paid tier exists in this bucket.** The class's canonical sink
  appears only inside HOST-158019's generic paragraph. Do not price reset-mail poisoning
  from this vault; the Authentication-Session vault owns that pricing.

## 7. Cross-references

- `Open-Redirect/` — every row terminates in a redirect; that vault owns the
  destination-side doctrine.
- `Cache-Poisoning/` — HOST-158019 claims it; that vault owns the poisoning mechanics and
  proof standard (cached object + second victim).
- `Authentication-Session/` — verification/reset mail hardening; HOST-1444675 is its
  host-poisoning instance.
- `SSRF/` — HOST-1783015's DB label; that vault owns the internal-network play, this module
  owns the Host-manipulation primitive.
