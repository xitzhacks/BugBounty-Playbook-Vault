---
title: "Broken access control, staff & GraphQL authorization — role matrices, deactivated accounts, project templates, OTP binding"
type: playbook
category: broken-access-control-staff-graphql
cwe: "CWE-862"
source_count: 71
full_bodies_available: 71
corpus: "h1-brain disclosed_reports.db (3,673 rows), priv-esc bucket + module_map_all.json merges"
list_accessed: "2026-11-07"
note: "Anchors: PRIV-689314 (GitLab template copy, $12,000), PRIV-418767 (2FA bypass via embedded submission, $10,000). All 71 bodies read. Shopify staff cluster dominates (19 rows)."
---

# Broken Access Control, Staff & GraphQL — the server trusts the role you don't have

## 1. Overview

Seventy-one rows, **$35,970/23 paid** (48/71 carry no figure). This is the largest module by rows and the second-largest by figure, and it is the vault's doctrinal center: the highest-priced flaws in the corpus are all here, and they share one mechanism — an authorization check that either does not exist, exists on one code path but not the other, or exists against a role the attacker was never granted. The program concentration is Shopify-weighted (19 rows: staff settings, POS, Stocky, Plus SAML, partners) plus the platform-program clusters (security 7: HackerOne's own 2FA, mediation, GraphQL invitation; gitlab 5; nextcloud 5). The DB weakness split is 51 `Privilege Escalation` / 20 `Improper Authorization` — the register keeps the tag, the module classifies by the missing check.

**Case-stock (71 rows / $35,970):**

| Case | Target | Mechanism | Bounty |
|---|---|---|---|
| [PRIV-689314](https://hackerone.com/reports/689314) | gitlab — gitlab.com | User-namespace template copy: group check bypassed → import private project | $12,000 |
| [PRIV-418767](https://hackerone.com/reports/418767) | security — hackerone.com | embedded submission form bypasses program 2FA (+ blacklist) | $10,000 |
| [PRIV-1330529](https://hackerone.com/reports/1330529) | zomato — *.zomato.com | OTP sent to attacker number, code verified against victim resId | $3,250 |
| [PRIV-2930811](https://hackerone.com/reports/2930811) | cosmos — CosmWasm | use any non-enabled CosmWasm capability | $2,000 |
| [PRIV-1245736](https://hackerone.com/reports/1245736) | shopify — Shopify Developed Apps | unprivileged Stocky user → POST /users/create_admin | $1,600 |
| [PRIV-1193062](https://hackerone.com/reports/1193062) | gitlab — Your Own GitLab Instance | external maintainer → project token bot = internal guest | $1,020 |
| [PRIV-1113289](https://hackerone.com/reports/1113289) | gitlab — gitlab.com | guest creates test cases | $650 |
| [PRIV-1112297](https://hackerone.com/reports/1112297) | gitlab — gitlab.com | reporter uses Move-to to upload design | $600 |
| [PRIV-1819668](https://hackerone.com/reports/1819668) | brave — https://github.com/brave/brave-core | Brave News opens arbitrary chrome: URLs | $600 |
| [PRIV-331223](https://hackerone.com/reports/331223) | shopify — your-store.myshopify.com | deactivated staff still receives order notifications | $500 |
| [PRIV-411930](https://hackerone.com/reports/411930) | security | external-program maintainer updates churned programs | $500 |
| [PRIV-412988](https://hackerone.com/reports/412988) | security — hackerone.com | request mediation on published reports | $500 |
| [PRIV-423198](https://hackerone.com/reports/423198) | shopify — your-store.myshopify.com | low-priv staff edits packaging slips / views product+shipping | $500 |
| [PRIV-860348](https://hackerone.com/reports/860348) | shopify — your-store.myshopify.com | no-permission staff deletes POS staff (GraphQL) | $500 |
| [PRIV-202499](https://hackerone.com/reports/202499) | phabricator | viewer can send room messages | $300 |
| [PRIV-300099](https://hackerone.com/reports/300099) | zomato — *.zomato.com | dashboard_handler.php review control | $300 |
| [PRIV-1021776](https://hackerone.com/reports/1021776) | cs_money — cs.money | cancelled txns via Steam ID only | $300 |
| [PRIV-176979](https://hackerone.com/reports/176979) | coinbase | Coinbase authentication issue | $200 |
| [PRIV-300454](https://hackerone.com/reports/300454) | zomato — *.zomato.com | restaurant_menus_handler.php escalation | $200 |
| [PRIV-173969](https://hackerone.com/reports/173969) | instacart | full access to any list | $150 |
| [PRIV-144000](https://hackerone.com/reports/144000) | instacart | delivery chat-log authorization bypass | $100 |
| [PRIV-147369](https://hackerone.com/reports/147369) | slack | call in unpaid-account channel | $100 |
| [PRIV-148467](https://hackerone.com/reports/148467) | vkcom | moderator deletes editors' scheduled posts | $100 |
| [PRIV-52707](https://hackerone.com/reports/52707) | vimeo | invite any user to group without follow | - |
| [PRIV-59505](https://hackerone.com/reports/59505) | drchrono | staff Create/Update patients permission ignored | - |
| [PRIV-93020](https://hackerone.com/reports/93020) | vkcom | deleted-page name / university disclosure (VK) | - |
| [PRIV-151459](https://hackerone.com/reports/151459) | slack | post on restricted channel | - |
| [PRIV-153905](https://hackerone.com/reports/153905) | nextcloud | disable sharing IDOR (CVE-2016-9464) | - |
| [PRIV-154410](https://hackerone.com/reports/154410) | shopify | delete/modify own comment after limited access | - |
| [PRIV-157412](https://hackerone.com/reports/157412) | secnews | query private posts / change post meta | - |
| [PRIV-159512](https://hackerone.com/reports/159512) | security | mediation on too-old reports | - |
| [PRIV-165229](https://hackerone.com/reports/165229) | nextcloud | mask external storage shared by admin | - |
| [PRIV-167846](https://hackerone.com/reports/167846) | shopify | deleted-post + admin function access (forum) | - |
| [PRIV-175490](https://hackerone.com/reports/175490) | shopify | deactivated staff logs into mobile app | - |
| [PRIV-181748](https://hackerone.com/reports/181748) | x | forum comment edit via post_id IDOR | - |
| [PRIV-254588](https://hackerone.com/reports/254588) | shopify — partners.shopify.com | removed staff creates dev stores | - |
| [PRIV-300881](https://hackerone.com/reports/300881) | mavenlink | deleted member re-adds self | - |
| [PRIV-324006](https://hackerone.com/reports/324006) | pingidentity — https://ort-admin.pingone.com/* | SaaS admin modify/delete/get users | - |
| [PRIV-403039](https://hackerone.com/reports/403039) | automattic | WooCommerce map_meta_cap blacklist → shop-manager | - |
| [PRIV-411337](https://hackerone.com/reports/411337) | chaturbate — chaturbate.com | reset link survives email change | - |
| [PRIV-416983](https://hackerone.com/reports/416983) | shopify — Shopify Developed Apps | removed Apps staff modifies flow connections | - |
| [PRIV-493324](https://hackerone.com/reports/493324) | gitlab — gitlab.com | admin impersonation → any-user to gitlab admin | - |
| [PRIV-508493](https://hackerone.com/reports/508493) | nextcloud — nextcloud/server | group admin wipes data dir (CVE-2019-15624) | - |
| [PRIV-605720](https://hackerone.com/reports/605720) | security — hackerone.com | program-only member → admin | - |
| [PRIV-619484](https://hackerone.com/reports/619484) | nextcloud — nextcloud/server | read-only share → write sub-folders (CVE-2019-15621) | - |
| [PRIV-633245](https://hackerone.com/reports/633245) | nextcloud — nextcloud/server | delete permission added on reshare | - |
| [PRIV-763994](https://hackerone.com/reports/763994) | shopify — Shopify Developed Apps | Stocky: disclose any store data via email | - |
| [PRIV-792927](https://hackerone.com/reports/792927) | security — hackerone.com | GraphQL ReportInvitation leaks email by username | - |
| [PRIV-802011](https://hackerone.com/reports/802011) | kubernetes — https://github.com/kubernetes/test-infra | Grafana improper authorization | - |
| [PRIV-810320](https://hackerone.com/reports/810320) | helium — https://helium-console-dev.herokuapp.com/ | read-only deletes higher-priv members (DELETE endpoint) | - |
| [PRIV-833782](https://hackerone.com/reports/833782) | wordpress — BuddyPress Core | authenticated edit/trash BuddyPress Emails | - |
| [PRIV-905543](https://hackerone.com/reports/905543) | shopify — your-store.myshopify.com | low-priv adds/removes sales-register cash | - |
| [PRIV-910300](https://hackerone.com/reports/910300) | shopify — your-store.myshopify.com | email-confirmation bypass → escalation (store) | - |
| [PRIV-1032468](https://hackerone.com/reports/1032468) | x — *.twitter.com | read-only app publishes/deletes fleets | - |
| [PRIV-1084904](https://hackerone.com/reports/1084904) | shopify — Plus Web Admin with Single Domain Feature | store-mgmt → SAML convert calls | - |
| [PRIV-1084939](https://hackerone.com/reports/1084939) | shopify — Plus Web Admin with Single Domain Feature | store-mgmt → SAML enforce-domains call | - |
| [PRIV-1091380](https://hackerone.com/reports/1091380) | shopify — partners.shopify.com | partner team retrieves financial data | - |
| [PRIV-1102365](https://hackerone.com/reports/1102365) | reddit — 918820076 | dubmash update sound titles, no authz | - |
| [PRIV-1102652](https://hackerone.com/reports/1102652) | shopify — your-store.myshopify.com | settings staff → order-notification subscription create | - |
| [PRIV-1102660](https://hackerone.com/reports/1102660) | shopify — your-store.myshopify.com | settings staff → order-notification subscription delete | - |
| [PRIV-1114617](https://hackerone.com/reports/1114617) | mattermost — h1-*your-own-instance*.cloud.mattermost.com | post in channel without privilege | - |
| [PRIV-1174527](https://hackerone.com/reports/1174527) | logitech — *.streamlabs.com | owner access-token control → stream control | - |
| [PRIV-1350095](https://hackerone.com/reports/1350095) | shopify — your-store.myshopify.com | staff uses GraphQL BULK_OPERATIONS_FINISH | - |
| [PRIV-1466855](https://hackerone.com/reports/1466855) | shopify — your-store.myshopify.com | no Develop-apps → uninstall custom app | - |
| [PRIV-1572591](https://hackerone.com/reports/1572591) | linkedin — www.linkedin.com | Analyst views company email domains | - |
| [PRIV-1627980](https://hackerone.com/reports/1627980) | deptofdefense | unauthenticated internal API access | - |
| [PRIV-2081930](https://hackerone.com/reports/2081930) | security — api.hackerone.com | API-key bypass of submit restriction/ban | - |
| [PRIV-2188569](https://hackerone.com/reports/2188569) | zendesk — h1-your-domain.zendesk.com | support-contributor → admin via /api/v2 | - |
| [PRIV-2249299](https://hackerone.com/reports/2249299) | ibb — https://github.com/apache/airflow | Airflow broken access control (CVE-2023-47037) | - |
| [PRIV-2718253](https://hackerone.com/reports/2718253) | insightly — accounts.insightly.com | email-verification bypass via provisionuser | - |
| [PRIV-2999394](https://hackerone.com/reports/2999394) | wordpress — BBPress Core | CSRF → any user to Keymaster (BBPress) | - |

## 2. PRIV-689314: the $12,000 template-copy bypass

PRIV-689314 (gitlab, **$12,000**) — the vault's largest single row — is a three-way combination: a params-whitelist, a namespace guard that only runs for group namespaces, and a template importer that trusts the params the guard would have checked. The report's own summary is quoted because the corpus prices the combination, not any one leg:

> I've found a three minor vulnerabilities which, when combined, allow an attacker to copy private repositories, confidential issues, private snippets, and then some.

The root cause is then stated precisely:

> The code above is where the first vulnerability can be found.

The preceding code walk shows why: "In a normal situation, a Project Template can only be copied to a namespace (group) that is a descendant of the project template" — but `validate_namespace_used_with_template` returns early when the project is created in a *User* namespace (`return unless project.group`), so a `group_with_project_templates_id` for a private template, passed together with `template_name` and `use_custom_template`, sails past the descendant check entirely. The importer then copies the private template's repository, issues, and snippets into the attacker's own project. The operator lesson is the module's core doctrine: **authorization checks that are conditional on the namespace type, the entry path, or the feature flag are not checks at all** — they are second code paths. The attacker supplies the input that selects the unchecked path.

## 3. PRIV-418767: the $10,000 2FA bypass (policy bypass via second door)

PRIV-418767 (security / HackerOne programs, **$10,000**) is the vault's second-largest row and its cleanest statement of the same doctrine in policy form. A program enforces 2FA (and a reporter blacklist) before report submission on the main submission flow. The control is bypassed entirely by using the *embedded* submission form, which never calls the same guard:

> Now i was able to bypass this 2FA setup requirements by using the Parrot Sec program __Embedded Submission Form__.

> Now submit report using that embedded submission form and you can submit reports without setting-up your 2FA, despite the program __enforce__ the user to setup the 2FA before submitting new reports.

The steps are verbatim in the body (remove 2FA → hit Submit Report → blocked → open the embedded URL → submit unblocked). Paired with PRIV-2081930 (API-key bypass of the same submit restriction/ban, no figure) and PRIV-159512/412988 (mediation-request lifecycle bugs, $500 and no figure), this is the platform-level version of the GitLab lesson: the 2FA/blacklist/mediation state machine has two doors, and only one door checks.

## 4. The staff matrix: Shopify, GraphQL, and deactivated accounts

The Shopify staff cluster is the module's center of gravity (19 rows). Three sub-patterns repeat, each with a paid anchor:

- **(a) The admin endpoint that trusts the session, not the role.** PRIV-1245736 (Stocky, **$1,600**):
  > A non-privileged Stocky user (created within Stocky)  may be able to create a new admin user.
  The body shows the one-request proof — intercept any `/users/me` update, replay it as `POST /users/create_admin` with the same cookies/token, log in as the new admin. The same file system repeats as PRIV-763994 (Stocky discloses any store's products/files/POs via email; no figure), PRIV-860348 (no-permission staff deletes POS staff over `pos-channel.shopifycloud.com/graphql-proxy/admin`, **$500**), PRIV-1350095 (staff invokes `BULK_OPERATIONS_FINISH` GraphQL webhook without permission; no figure), and the Plus SAML pair PRIV-1084904/1084939 (store-management permission reaches `convertUsersFromSaml`/`enforceSamlOrganizationDomains`; no figure). The GraphQL lane (PRIV-792927, PRIV-1102652/1102660) is the identical bug over a different transport: the mutation's permission check is absent, so the staff role's REST boundary is decorative.
- **(b) Deactivated ≠ revoked.** PRIV-331223 (deactivated staff still receives order notifications, **$500**), PRIV-175490 (deactivated staff logs into the mobile app; no figure), PRIV-254588 (removed staff creates dev stores; no figure), PRIV-416983 (removed Apps staff modifies flow connections; no figure). The revocation path removes UI access but leaves a credential or subscription valid.
- **(c) OTP / identifier binding.** PRIV-1330529 (zomato, **$3,250**): the OTP is sent to the attacker's mobile (`number`/`resId` = attacker), then the verify request rebinds a *different* `resId` (the victim restaurant) to the attacker's email:
  > Here by changing the `verificationCode`  -  (Otp received on Attacker Mobile in response of Request :1 )& `requestId`  (Response of request:1) and `resId` to Victim Restaurant. Request:2 maps e-mail id of Attacker to Victim restaurant.
  The server verifies "a correct OTP was presented" without verifying "the OTP was issued for *this* `resId`." That is an authorization bug (missing object binding) disguised as an OTP bug, and the corpus prices it at $3,250 — above every pure staff-permission row except the two crown rows.

The GitLab token row, PRIV-1193062 (external-user maintainer → project-token bot with internal guest rights, **$1,020**), is the same binding error at the identity layer:

> An "external user" (a user account with the status external) which is granted "Maintainer" role on any project on the GitLab instance where "project tokens" are allowed can elevate its privilege to "Internal".

The desktop/mobile sibling — email-confirmation bypasses (910300, 2718253, 411337) and the store-level confirm bypasses in module 05 (791775/796956) — complete the identity half: anything the app treats as "verified" without binding the verification to the identifier it verified is a takeover.

## 5. The unpaid shelf (48 rows): what the corpus teaches by not pricing

Forty-eight of 71 rows carry no figure. They are not filler — they are the operator's enumeration checklist. The Nextcloud share cluster (153905 share-disable IDOR, 619484 read-only → write sub-folders, 633245 reshare delete-permission, 165229 external-storage masking, 508493 group-admin data-dir wipe) shows the same permission object (`share`) mutated through five different verbs, none re-checking the caller's original grant. The API-verb rows (810320 `DELETE /api/memberships/<membershipID>` with no role check; 1032468 read-only app publishes/deletes fleets; 1114617 post in an unprivileged channel) show that the missing check is on the mutation, not the query — read paths are guarded, write paths are not. And the state-lifecycle rows (300881 re-add after deletion, 605720 program-only → admin, 159512/412988 mediation windows, 411930 churned-program updates) show that time is the other input: deactivated, churned, published, and expired states retain write power.

## 6. What pays/what doesn't

- **Crown rows (both ≥ $10,000):** multi-leg authorization combinations (689314, $12,000) and second-door policy bypasses (418767, $10,000). The corpus prices the *combination* and the *alternate channel*, never the single missing check in isolation.
- **Ownership/binding rows:** OTP-to-wrong-object (1330529, $3,250), capability-model bypass (2930811, $2,000), stock-management admin creation (1245736, $1,600), token-bot identity hop (1193062, $1,020). The price follows what the hop reaches (restaurant ownership, store admin, internal code), not the cleverness of the bypass.
- **Staff-permission micro-rows:** $500–$650 for single-endpoint staff overreach (331223, 411930, 412988, 423198, 860348, 1112297, 1113289, 1819668). These are the module's bread-and-butter — one staff role, one privileged action, one request.
- **$0-in-record rows (48):** the unpaid shelf is dominated by small-surface permission gaps on programs whose tables top out low, plus a large shoulder of rows with bulky bodies (493324 impersonation-to-admin, 763994 cross-store disclosure, 905543 register cash, 1627980 internal API) that carry no figure at all. The corpus never prices a theoretical role matrix — every paid row demonstrates the action end-to-end (a created admin, a copied repo, a bound OTP).
- **Kill-gate from this module:** privacy-grade IDORs that never reach a privileged action (93020's deleted-page disclosure, 181748's comment edit, 157412's post-meta change) are the module's honest low end — filed as context, not as crowns.

## 7. Cross-references

- Module 05 holds the same staff/confirmation mechanism family from the unclassified merges (POS GraphQL email update 867513, POS Manage-Staff → Plan & Permissions 985150, wholesale invite-link reuse 1266828, confirm-any-email → SSO takeover 791775/796956) — read the two modules as one role-matrix sweep; the merge provenance differs, the primitive does not.
- The IDOR vault's object-reference modules and the Authentication-Session vault's 2FA modules are the neighboring shelves: 418767 belongs to both, and 792927 (GraphQL email leak) is the GraphQL vault's authorization lane.
- The playbook (PRIV-Testing-Agent-Playbook.md) P1 maps every role × endpoint pair; P2 replays deactivated/removed states; P5 enforces the "demonstrated the action" bar.
