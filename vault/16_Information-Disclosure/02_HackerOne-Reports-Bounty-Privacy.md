---
title: "HackerOne Reports & Bounty Privacy — the platform disclosing itself"
type: playbook
category: hackerone-reports-bounty-privacy
cwe: "CWE-200"
source_count: 51
full_bodies_available: 51
corpus: "h1-brain disclosed_reports.db (sha256 8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4) — 362 rows"
list_accessed: "2026-11-07"
note: "Anchors: INFO-3000510 (security, $25,000), INFO-186230 (security, $12,500), INFO-182358 (security, $10,000), INFO-188719 (security, $10,000), INFO-410015 (security, $3,000), INFO-2213251 (security, $2,500). All quotes byte-true to references/archive/INFO-bodies-full-dump.txt."
---

# HackerOne Reports & Bounty Privacy — the platform disclosing itself

## 1. Overview

Fifty-one rows, **$83,580/28 paid** — the vault's richest module per-row and the source of its crown jewel. Forty-eight of 51 rows target the `security` team (HackerOne's own program); the exceptions are two `x` (MoPub) rows and one `gitlab`, `reverb` each. The corpus is therefore a self-audit: researchers billing HackerOne for HackerOne's own disclosure bugs, priced at HackerOne's own tiers. The money concentrates at the top — **the top four rows carry $57,500 (69% of the module)** — and every one of them is a *serialization or export* bug: a `.json` endpoint that serializes too much, an "Export as .zip" feature that packages redacted content, a settings call that serializes review-queue reports. The remaining forty-seven rows are the long tail of redaction, metrics, and notification-state leaks, mostly $500 flat or unpriced.

**Case-stock (51 rows / $83,580):**

| Case | Target | Mechanism | Bounty |
|---|---|---|---|
| [INFO-3000510](https://hackerone.com/reports/3000510) | security | The /reports/:id.json endpoint discloses potentially sensitive user attributes… | $25,000 |
| [INFO-186230](https://hackerone.com/reports/186230) | security | Internal attachments can be exported via "Export as .zip" feature | $12,500 |
| [INFO-182358](https://hackerone.com/reports/182358) | security | Partial disclosure of report activity through new "Export as .zip" feature | $10,000 |
| [INFO-188719](https://hackerone.com/reports/188719) | security | Information Disclosure in /skills call | $10,000 |
| [INFO-410015](https://hackerone.com/reports/410015) | security | Discrepancy in hacker profile report count may reveal existence of a private p… | $3,000 |
| [INFO-347693](https://hackerone.com/reports/347693) | security | Program metrics disclosed response_efficiency_percentage via /program_name jso… | $2,500 |
| [INFO-386997](https://hackerone.com/reports/386997) | security | Private program policy page still accessible after user left the program | $2,500 |
| [INFO-493176](https://hackerone.com/reports/493176) | security | Partial report contents leakage - via HTTP/2 concurrent stream handling | $2,500 |
| [INFO-2101087](https://hackerone.com/reports/2101087) | security | Able to see Bonus amount given to a report even if the bounty and Bonus is not… | $2,500 |
| [INFO-2213251](https://hackerone.com/reports/2213251) | security | New Search Feature: Search for non-public words in limited disclosure reports | $2,500 |
| [INFO-310946](https://hackerone.com/reports/310946) | security | The request tells the number of private programs, the new system of authorizat… | $2,000 |
| [INFO-247628](https://hackerone.com/reports/247628) | security | Reading redacted data via hackbot's answers | $1,500 |
| [INFO-159526](https://hackerone.com/reports/159526) | security | Information leakage of private program | $500 |
| [INFO-210190](https://hackerone.com/reports/210190) | security | Transitioning a Private Program to Public Does Not Clear Previously Private Up… | $500 |
| [INFO-452973](https://hackerone.com/reports/452973) | security | Inline banner on Report page discloses whether organization runs a private pro… | $500 |
| [INFO-654198](https://hackerone.com/reports/654198) | security | Manipulate hacker profile and private program hacktivity to expose your name a… | $500 |
| [INFO-674757](https://hackerone.com/reports/674757) | security | Total Paid Bounty Paid can be disclose | $500 |
| [INFO-689997](https://hackerone.com/reports/689997) | security | Disclosure of Email title report in quick award paypout email (no content mode… | $500 |
| [INFO-696266](https://hackerone.com/reports/696266) | security | "Bounties paid in the last 90 days" discloses the undisclosed bounty amount in… | $500 |
| [INFO-800109](https://hackerone.com/reports/800109) | security | An invite-only's program submission state is accessible to users no longer par… | $500 |
| [INFO-871142](https://hackerone.com/reports/871142) | security | Disclosure of the name of a program that has a private part with an external l… | $500 |
| [INFO-1219011](https://hackerone.com/reports/1219011) | security | Report Bulk endpoint "agree-on-going-public" action may reveal Report disclosu… | $500 |
| [INFO-1826141](https://hackerone.com/reports/1826141) | security | HackerOne Undisclosed Report Leak via PoC of Full Disclosure on Hacktivity | $500 |
| [INFO-2054222](https://hackerone.com/reports/2054222) | security | Usernames still visible on report export pdf despite "I want to redact all use… | $500 |
| [INFO-2122644](https://hackerone.com/reports/2122644) | security | Names not completely redacted despite "Redact the names of the involved users"… | $500 |
| [INFO-574639](https://hackerone.com/reports/574639) | x | Reports Modal in app.mopub.com Disclose by any user | $280 |
| [INFO-318399](https://hackerone.com/reports/318399) | security | Program profile_metrics.json contains time to triage for deptofdefense even it… | $250 |
| [INFO-2278865](https://hackerone.com/reports/2278865) | security | Some limited confidential information can still be accessed after a user exits… | $50 |
| [INFO-148050](https://hackerone.com/reports/148050) | security | Know undisclosed Bounty Amount when Bounty Statistics are enabled. | - |
| [INFO-157699](https://hackerone.com/reports/157699) | security | Disclosure of external users invited to a specific report | - |
| [INFO-269230](https://hackerone.com/reports/269230) | security | Emails of invited collaborators are disclosed in full in payload for report pa… | - |
| [INFO-270993](https://hackerone.com/reports/270993) | security | resolved bugs in a program are public despite the program settings | - |
| [INFO-289568](https://hackerone.com/reports/289568) | security | Program profile metrics endpoint contains mean time to triage, even when turne… | - |
| [INFO-293299](https://hackerone.com/reports/293299) | security | Validation message in Bounty award endpoint can be used to determine program b… | - |
| [INFO-327088](https://hackerone.com/reports/327088) | security | Extra program metrics disclosed via /PROGRAM_NAME json response | - |
| [INFO-367581](https://hackerone.com/reports/367581) | reverb | Basic auth details is still work on report ( 351555 ) | - |
| [INFO-380317](https://hackerone.com/reports/380317) | security | Team object exposes amount of participants in a private program to non-invited… | - |
| [INFO-397031](https://hackerone.com/reports/397031) | security | Disclosure of top 10 vulnerability types for programs that haven't enabled the… | - |
| [INFO-399174](https://hackerone.com/reports/399174) | x | Access MoPub Reports Data even after Company removed you from their MoPub Acco… | - |
| [INFO-640488](https://hackerone.com/reports/640488) | security | Total bounties paid amount is disclosed because of redesign of the Program Pro… | - |
| [INFO-645264](https://hackerone.com/reports/645264) | security | Program Email Nofication settings ignored when being added as an external cont… | - |
| [INFO-669776](https://hackerone.com/reports/669776) | security | Disclosure of Program email Title Report when being removed as contributor. By… | - |
| [INFO-685909](https://hackerone.com/reports/685909) | security | Searching from Hacktivity returns hits for words in limited disclosure reports… | - |
| [INFO-826176](https://hackerone.com/reports/826176) | security | program_analytics_benchmarks query shows information not visible in public | - |
| [INFO-871749](https://hackerone.com/reports/871749) | security | Unauthorized access to metadata of undisclosed reports that were retested | - |
| [INFO-880863](https://hackerone.com/reports/880863) | gitlab | Todos are not redacted when membership changes - Access to (confidential) issu… | - |
| [INFO-1285115](https://hackerone.com/reports/1285115) | security | Leaked H1's Employees Email addresses,meeting info on private bug bounty progr… | - |
| [INFO-1869613](https://hackerone.com/reports/1869613) | security | Attachment in published HackerOne report exposure private program | - |
| [INFO-2053051](https://hackerone.com/reports/2053051) | security | Hackerone All Private Program Name Leaked to Public Via Collaborator OR Attack… | - |
| [INFO-2310620](https://hackerone.com/reports/2310620) | security | New Hacktivity features:Bounty rewards leakage Where programs doesn’t decide t… | - |
| [INFO-2322082](https://hackerone.com/reports/2322082) | security | Being able to disclose IBB bounty table of any public program | - |

## 2. The $25,000 report: `/reports/:id.json` serializes the reporter

INFO-3000510 (**security, $25,000**) — the vault's bucket max — is one endpoint and one sentence:

> The.json endpoint of any disclosed report is leaking reporter's email, OTP backup codes, reporter's phone number, "graphql_secret_token", tshirt size all the reporter account's internal details etc.

> Reporter H1 account private data disclosed

Note the mechanics that earned the five-figure tier: the trigger is *conditional* ("when reporter summary is present"), the data class is *credentials* (OTP backup codes, `graphql_secret_token`), and the victim is *a third party* (the reporter, not the reporter-author). The report itself is 569 bytes — the shortest body among the module's top five — proof that in this corpus brevity with a credential class beats length. The `.json` suffix on an already-public disclosed report is the inversion of the usual disclosure bug: the HTML page was correctly redacted; the machine-readable twin was not. Compare module 01, where the same author's Team-object queries paid $2,500 flat: the price delta ($25,000 vs $2,500) is the credential class, not the technique.

## 3. Export-as-zip: the redaction that ships the original

The module's two most expensive *process* bugs are a fix and its incomplete fix. INFO-182358 (**security, $10,000**) caught the launch:

> But unfortunately it discloses comments of partially disclosed reports which supposed to be hidden..

> You'll see comments are getting disclosed!

> This way you can see all the partially disclosed reports comments.

INFO-186230 (**security, $12,500**) caught the patch's residue: an attachment removed from the thread survived inside the exported zip —

> I have found that i can still view the attachment after it is being removed on the thread.

> You will see that the image is still there, but base on the thread, you guys removed it on disclosed report.

The $2,500 *premium* on the follow-up ($12,500 vs $10,000) is the corpus's clearest statement of patch-confidence pricing: the second report cost HackerOne the same investigation twice and paid more for it. INFO-2054222 ($500, usernames visible on exported PDF despite "I want to redact all usernames") and INFO-1869613 ($0, attachment in published report exposing a private program) are the same shelf at lower tiers — export/redaction pipelines leaking what the UI withdrew.

## 4. Oracles that read redacted content: search, hackbot, and stream ordering

Three rows turn *search infrastructure* into a disclosure oracle. INFO-2213251 (**security, $2,500**) is the canonical write-up — Hacktivity search tests words against the *full* report, not the limited disclosure, so an attacker can extract a hidden secret character by character:

> An attacker can search for words in limited disclosure reports, and see if it exists in the full report. HackerOne will return whether the word exists in the full report, rather than in the limited part (e.g. summary/title ...) of the report

> For example, if there is a secret inside the full report (but not inside the limited portion), the attacker could leak it with a lot of tries.

> around 30 chars to try in each iteration * 40 (average length of a secret)

INFO-685909 ($0) is its earlier sibling — the same Hacktivity-search oracle discovered against limited-disclosure reports, with the reporter reasoning: "it seems probable this limited report is referencing" a redacted string "even though what's publicly available does not mention this." INFO-247628 (**security, $1,500**) moves the oracle into the duplicate-detection bot: hackbot matched on the *real* redacted text, not the black squares:

> I have then observed that the bot does not identify duplicated reports while using the same redacted text (the black squares), but it has identified the real text that it has already been redacted.

INFO-493176 (**security, $2,500**) is the timing-ordering variant at protocol level: HTTP/2 concurrent streams turn `/bugs.json` result-presence into an ordering oracle — "instead of timing, the ordering of responses is used, making the attack resilient to network jitter" — disclosing (un)disclosed report existence cross-site. All four share the disclosure anatomy this playbook's P2 will generalize: *a system that legitimately holds the secret and answers a low-bandwidth question about it*.

## 5. Metrics, bounty, and membership-state leaks: the $500 flat tier

The module's floor is remarkably uniform — twenty rows at $500, spanning every flavor of "the setting says hidden, the endpoint says otherwise": program metrics (`response_efficiency_percentage`, INFO-347693 at $2,500 is the tier-breaker), bounty aggregates ("Bounties paid in the last 90 days", INFO-696266), private-program existence (INFO-452973, INFO-871142, INFO-159526), post-exit access (INFO-386997 at $2,500, INFO-800109, INFO-2278865 at $50 — the module's lowest paid row, which prices the post-exit *confidential-information* claim at $50), and collaborator email disclosure (INFO-269230, INFO-157699, both unpriced). INFO-410015 (**security, $3,000**) is the tier's cleverest proof — a count oracle: the hacker's profile count excludes sandbox reports, so publishing a probe report and watching the count move tells you whether the external program is private or sandboxed:

> The profile page counts the number of created your reports. But it does not consider the reports that are created in the sandbox. Thus, after creating the report, we can find out whether the external program is a private program or a sandbox.

INFO-188719 (**security, $10,000**) is the opposite extreme of the same shelf — an entire review queue serialized by `https://hackerone.com/settings/skills`:

> IN respone of above request all reports submitted for review are getting disclosed.

At $10,000 for two sentences, it is the module's second-shortest top-tier body and its highest price-per-byte after INFO-3000510.

## 6. What pays, what doesn't

- **Pays at the top**: serialized credentials of a *third party* ($25,000), a whole review queue ($10,000), and redaction-pipeline leaks with a demonstrated second price ($10,000 → $12,500). The common currency is *other people's secrets the platform itself was holding*.
- **Pays, flat**: program-existence, metrics, and bounty-aggregate leaks at $500 each; count-oracle proofs that *demonstrate* the classification (INFO-410015's 129→130→131 progression) at $3,000.
- **Doesn't pay (here)**: twenty-three unpriced rows, including real bugs (INFO-2053051 all-private-program-name leak, INFO-1285115 employee-email leak, INFO-880863 GitLab todo redaction). The corpus cannot distinguish "rejected" from "unpublished figure" — but the unpriced set skews toward *broad dump claims* ("all private programs leaked") while the paid set skews toward *narrow executable proofs* (one endpoint, one query, one count delta). File the narrow proof.
- **The patch premium**: a bypass of a previous fix paid *more* than the original ($12,500 > $10,000). Re-testing disclosed fixes is a priced activity in this corpus.

## 7. Cross-references

- Module 01 (`01_GraphQL-API-Objects-Exposure.md`) — the Team-object oracle family (`report_sources`, `vpn_suspended`) is this module's private-program-existence shelf in GraphQL dress; both price the *classification* of a program, not its contents.
- Module 06 (`06_Adjacent-Disclosure-Noise.md`) — INFO-367581 (reverb, basic-auth still working after INFO-351555) is this module's boundary case: a HackerOne report *about* a Cloudinary secret that itself became the disclosure vector.
- Companion vault `../Authentication-Session/` — OTP backup codes and `graphql_secret_token` (INFO-3000510) are session-material disclosures; token-secrecy there, redaction here.
