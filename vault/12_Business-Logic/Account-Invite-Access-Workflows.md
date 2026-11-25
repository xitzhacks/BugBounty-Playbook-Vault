---
title: "Account, invite & access workflows — invitation accounting, verification and status-gate bypasses"
type: playbook
category: account_invite_access_workflows
cwe: "CWE-840"
source_count: 32
full_bodies_available: 32
corpus: "h1-brain disclosed_reports.db, bucket business-logic (module account_invite_access_workflows, 32 rows, bodies-win)"
list_accessed: "2026-11-07"
note: "Claims trace to bodies read 2026-11-07 and archived in references/archive/BL-bodies-full-dump.txt; quotes byte-true."
---


# Account, invite & access workflows


Pattern: the workflow is the vulnerability. Invites, OTPs, verification flags and role checks are enforced in the happy path the UI renders, while the underlying endpoint enforces them nowhere — or enforces them against a state the attacker has already moved the account out of.


## 1. Overview


Case stock (32 rows / 12 paid / $9,010; bucket module `account_invite_access_workflows`):


| Case | Target | Mechanism | Bounty |
|---|---|---|---|
| [BL-226199](https://hackerone.com/reports/226199) | security | Changing Victim's JIRA Integration Settings Through Multiple Bugs | $1,000 |
| [BL-259400](https://hackerone.com/reports/259400) | legalrobot | Issues with Forgot password Error Handling | - |
| [BL-259415](https://hackerone.com/reports/259415) | legalrobot | Lengthy manual entry of 2FA secret | - |
| [BL-259416](https://hackerone.com/reports/259416) | legalrobot | Incorrect email content when disabling 2FA | - |
| [BL-331691](https://hackerone.com/reports/331691) | security | Email Forwarding invitations for Drafts are not marked as accepted,... | $500 |
| [BL-334205](https://hackerone.com/reports/334205) | security | Harvesting all private invites using leave program fast-tracked inv... | $2,500 |
| [BL-415398](https://hackerone.com/reports/415398) | chaturbate | Chaturbate "/chat_ignore_list/" endpoint does not check for Account... | - |
| [BL-422698](https://hackerone.com/reports/422698) | chaturbate | Update Chat Allowed By Option ( without age verification ) | - |
| [BL-428660](https://hackerone.com/reports/428660) | nextcloud | Gallery: No feedback for invalid password | $50 |
| [BL-463828](https://hackerone.com/reports/463828) | security | Submitting report through Embedded Submission form gives user indef... | $500 |
| [BL-549364](https://hackerone.com/reports/549364) | security | Account recovery text message is sending a wrong domain to users. | $500 |
| [BL-666632](https://hackerone.com/reports/666632) | x | Delete direct message history without access the proper conversatio... | $560 |
| [BL-712344](https://hackerone.com/reports/712344) | x | [Bypass fixed #664038 and #519059] Application settings change sett... | - |
| [BL-763177](https://hackerone.com/reports/763177) | phabricator | User can link non-public file attachments, leading to file disclose... | $500 |
| [BL-783258](https://hackerone.com/reports/783258) | localizejs | 2-factor authentication can be disabled when logged in without conf... | - |
| [BL-808287](https://hackerone.com/reports/808287) | nextcloud | Unrestricted file upload on the image of contacts | $100 |
| [BL-894569](https://hackerone.com/reports/894569) | gitlab | An attacker can run pipeline jobs as arbitrary user | - |
| [BL-999789](https://hackerone.com/reports/999789) | security | Getting New Invitations without Leaving Programs | - |
| [BL-1074047](https://hackerone.com/reports/1074047) | bumble | Misconfigured oauth leads to Pre account takeover | - |
| [BL-1088966](https://hackerone.com/reports/1088966) | security | Ability to invite a new member on Sandbox Program | - |
| [BL-1486417](https://hackerone.com/reports/1486417) | security | [Bypass] Ability to invite a new member in  sandbox Organization | - |
| [BL-1523584](https://hackerone.com/reports/1523584) | zomato | Attacker shall recieve order updates on whatsapp for users who have... | $300 |
| [BL-1664920](https://hackerone.com/reports/1664920) | security | Program managers can see draft reports using Export Reports feature | - |
| [BL-1675674](https://hackerone.com/reports/1675674) | linkedin | An Attacker Can Flag Draft Job Posts And Can Disclose The Draft Job... | - |
| [BL-1691603](https://hackerone.com/reports/1691603) | linkedin | A Unverified User Can Post Newsletter (Which Is Not Allowed Through... | - |
| [BL-1770797](https://hackerone.com/reports/1770797) | security | adding h1_analyst_* to username for normal users | $500 |
| [BL-2011431](https://hackerone.com/reports/2011431) | security | Asset Inventory Internal Descriptions are leaked in CSV export | - |
| [BL-2263294](https://hackerone.com/reports/2263294) | security | Cloud Computer Hackerone Triager can be Accessible for everyone [h1... | - |
| [BL-2430179](https://hackerone.com/reports/2430179) | security | Minor security issue with Hackerone Invitations from sandbox program | - |
| [BL-2450215](https://hackerone.com/reports/2450215) | security | Any user could upload attachments to pentest scoping form they don'... | - |
| [BL-2588329](https://hackerone.com/reports/2588329) | indrive | Change phone number OTP flaw leads to any phone number takeover | $2,000 |
| [BL-2712583](https://hackerone.com/reports/2712583) | mozilla | Bypass Email verification for monitoring at `monitor.mozilla.org` | - |


Corpus mix: 19 `security` (HackerOne's own program) rows dominate — invitation accounting is this module's center of gravity — plus one $2,000 identity-anchor (indrive phone OTP) and a $1,000 integration-hijack.


## 2. Invitation harvesting — BL-334205 (security, $2,500)


Two features that each look safe compose into invite farming: `security@` email-forwarding mints program participation without user action, and the Leave-Program survey fast-tracks a fresh invite:


> I have found a way that it is possible to harvest all private invitation using the new __Leave Program__ feature together with the `security@` email forwarding feature __without any user interaction__.




> But this is easy to exploit, just send an email to: `██████ > get invites > leave to ██████████ > get new invites came from fast-tracked > repeat`




> An attacker can harvest all private invitation without any user interaction, in a matter of few months you can have 100+ private invitation by just daily repeating the steps i provided above.


Goodwill note: `security@` delivery is the trigger, but the join itself is `Click the __Submit Vulnerability__ , you are now a participants.` — the report is honest that part of the cycle is a click.


## 3. Invite lifecycle flaws (the rest of the invitation cluster)


BL-331691 (security, $500): an invitation link for a draft program is never marked accepted, so one token admits every researcher who opens it:


> So, a member  can pass this token to other people and they will be added to the team.I used this token multiple times and it's still live.


BL-999789 (security, unpaid) replays the leave-survey request with a swapped `team_handle` to mint invites without ever leaving the second program. BL-1088966 and BL-1486417 (security, unpaid) invite users into sandbox programs/organizations the UI says cannot be invited into. BL-2430179 (security, unpaid) is the milder sibling: sandbox-organization invite emails omit the unverified-program warning.


## 4. Phone-number takeover via OTP that accepts anything — BL-2588329 (indrive, $2,000)


The corpus's identity anchor beyond HackerOne itself. A 4-digit change-phone OTP accepts `0000` for any number:


> When an user requests a phone number change inside the app, it will send a 4 digit code but if you place 0000, it will accept any number and update it into the app!!




> Any attacker can use the phone number for an account takeover or delete anyone account, or cancelling trips


This is business-logic, not brute-force: no rate-limit was defeated, the verifier simply accepted an invalid code. Pair with the rate-limit module's OTP-brute-force row (BL-1991376) for the contrast.


## 5. Integration and account-linking hijacks


BL-226199 (security, $1,000) chains five bugs to re-point a victim program's JIRA integration at an attacker's project:


> When a user already have a JIRA connected to his HackerOne program, if an attacker sends 
> a malicious link to him (with a malicious JIRA JWT token in it), clicking on `Link JIRA Instance to program` will change the JIRA account connected to the program and worst, it will automatically select the attacker's JIRA project without user interaction.


BL-1074047 (bumble, unpaid) is pre-account takeover: sign up first with the victim's email, then when the victim signs in via OAuth the attacker-set password is the only credential that works. BL-549364 (security, $500) is the low-ceremony end — account-recovery SMSs point users at an attacker-registrable lookalike domain (`supportahackerone.com`).


## 6. Status and role gates the UI renders but the server doesn't check


BL-422698 (chaturbate, unpaid): `allowed_chat` updates without age verification — intercept, swap the enum, forward. BL-415398 (chaturbate, unpaid): `/chat_ignore_list/` ignores disabled-account status no other Chaturbate endpoint skips. BL-783258 (localizejs, unpaid): 2FA disable requires a password the API never verifies — replay the POST to `/api/user/two-factor/set` with a wrong password. BL-1691603 (linkedin, unpaid): unverified users replay the newsletter-creation POST taken from a verified account. BL-1675674 (linkedin, unpaid): report/draft job IDs disclose unpublished postings. BL-712344 (x, unpaid): cross-app settings drift leaves `protected tweets` off. BL-666632 (x, $560): inverting a DM `conversation_id` deletes the other side's history.


BL-763177 (phabricator, $500) is the module's most elegant row: a low-privilege user plants `{F27}`-style private-file references in a public post; a higher-privileged editor's routine typo-fix silently republishes the private file.


> If a user references a file from a private location in a public location, the file permissions will silently be updated and the file will be made available publicly as well (if the user has permission to access the file; otherwise, permissions will remain unchanged).


## 7. Post-leave and post-hoc access


BL-463828 (security, $500): submitting a report through an embedded form keeps the profile visible after leaving the program. BL-1664920 (security, unpaid): `export_reports` includes draft reports the inbox correctly hides. BL-2011431 (security, unpaid): asset-inventory CSV exports the internal-only description. BL-2450215 (security, unpaid): attachments upload into any pentest scoping form whose ID is known. BL-2263294 (security, unpaid): a triager's cloud computer stays remote-shellable to everyone. BL-2712583 (mozilla, unpaid): verification tokens leak in the breaches API, so anyone can verify anyone's email.



## 8. Noise floor of this module (kept, honestly)


BL-259400, BL-259415, BL-259416 (legalrobot, unpaid) are UX bug reports (silent forgot-password, long 2FA secret, wrong email copy). BL-428660 (nextcloud, $50) is real but low: password-policy violations fail silently, leaving files public while users believe them protected. BL-894569 (gitlab, unpaid) is a serious CI-credential reuse chain filed as business-logic. BL-808287 (nextcloud, $100) is file-type policy. BL-1523584 (zomato, $300): order-ID IDOR subscribes the attacker to another user's WhatsApp order updates. BL-1770797 (security, $500): `h1_analyst_*` strings addable to normal usernames.


## 9. What pays / what doesn't


**Pays:** compounding workflow bugs (334205, $2,500 — harvested invites are a countable asset); universal-OTP acceptance (2588329, $2,000); five-bug chain stories (226199, $1,000); token-reuse with a demonstrated second join (331691, $500). **Doesn't price:** post-leave profile visibility without sensitive data (463828, still $500 here but framed as exactly that), sandbox-only invites (1088966/1486417, $0), and anything the reporter themselves asks to close (259400-class UX).


## 10. Cross-references


- Commerce module: BL-1301753-class entitlement abuse is this module's wallet-side twin.
- Rate-limit module: BL-1991376 (indrive SMS-code flooding) is the same vendor family as BL-2588329.
- Race vault `Membership-and-Invitation-Races`: BL-334205/331691 are their HackerOne-own-program counterparts.
