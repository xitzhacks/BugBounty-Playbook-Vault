---
title: "IDOR Source Index"
type: reference
cases: 73
full_bodies_available: 55
summary_only: 18
archive_accessed: "2026-10-16"
---

# IDOR Source Index

Each row maps a HackerOne report ID to a case ID (`IDOR-NNN`), the destination
playbook, and its evidence type. Case IDs in playbooks must match this table.

| Case | Report | Evidence | Team | Weakness (program-assigned) | Bounty | Playbook | Title |
| --- | --- | --- | --- | --- | --- | --- | --- |
| IDOR-001 | [156520](https://hackerone.com/reports/156520) | full | algolia | Improper Authentication - Generic | $400 | [Role-Scoping-and-Vertical-Escalation.md](../Role-Scoping-and-Vertical-Escalation.md) | Unauthorized team members can leak information and see all API calls through /1/admin/* endpoints, even after they have been removed. |
| IDOR-002 | [13959](https://hackerone.com/reports/13959) | full | automattic | Improper Authentication - Generic | - | [Parameter-Gate-and-Hidden-Functions.md](../Parameter-Gate-and-Hidden-Functions.md) | privilege escalation |
| IDOR-003 | [149907](https://hackerone.com/reports/149907) | full | bime | Information Disclosure | - | [Cross-Tenant-Object-Level.md](../Cross-Tenant-Object-Level.md) | Urgent: attacker can access every data source on Bime |
| IDOR-004 | [126861](https://hackerone.com/reports/126861) | summary | bumble | Privilege Escalation | - | [Role-Scoping-and-Vertical-Escalation.md](../Role-Scoping-and-Vertical-Escalation.md) | Insecure Direct Object Reference on badoo.com |
| IDOR-005 | [184933](https://hackerone.com/reports/184933) | summary | deptofdefense | Privilege Escalation | - | [Parameter-Gate-and-Hidden-Functions.md](../Parameter-Gate-and-Hidden-Functions.md) | Insecure direct object reference vulnerability on a DoD website |
| IDOR-006 | [199644](https://hackerone.com/reports/199644) | summary | deptofdefense | Privilege Escalation | - | [Parameter-Gate-and-Hidden-Functions.md](../Parameter-Gate-and-Hidden-Functions.md) | Privilege Escalation on a DoD Website |
| IDOR-007 | [203311](https://hackerone.com/reports/203311) | summary | deptofdefense | Improper Authentication - Generic | - | [Parameter-Gate-and-Hidden-Functions.md](../Parameter-Gate-and-Hidden-Functions.md) | Bypass file access control vulnerability on a DoD website |
| IDOR-008 | [207099](https://hackerone.com/reports/207099) | summary | deptofdefense | Violation of Secure Design Principles | - | [Parameter-Gate-and-Hidden-Functions.md](../Parameter-Gate-and-Hidden-Functions.md) | Insecure Direct Object Reference (IDOR) vulnerability in a DoD website |
| IDOR-009 | [85720](https://hackerone.com/reports/85720) | full | enter | Violation of Secure Design Principles | $250 | [Cross-Tenant-Object-Level.md](../Cross-Tenant-Object-Level.md) | IDOR on remoing Share |
| IDOR-010 | [214001](https://hackerone.com/reports/214001) | full | files | - | $600 | [Cross-Tenant-Object-Level.md](../Cross-Tenant-Object-Level.md) | File access controls incorrectly enforced for files shared via QuickLink - Unshared files can be accessed |
| IDOR-011 | [131210](https://hackerone.com/reports/131210) | full | gitlab | Privilege Escalation | - | [Cross-Tenant-Object-Level.md](../Cross-Tenant-Object-Level.md) | Privilege escalation to access all private groups and repositories |
| IDOR-012 | [215384](https://hackerone.com/reports/215384) | full | gitlab | Insecure Direct Object Reference (IDOR) | - | [Parameter-Gate-and-Hidden-Functions.md](../Parameter-Gate-and-Hidden-Functions.md) | [Subgroups] Unprivileged User Can Disclose Private Group Names |
| IDOR-013 | [245872](https://hackerone.com/reports/245872) | full | gsa_bbp | Insecure Direct Object Reference (IDOR) | - | [Cross-Tenant-Object-Level.md](../Cross-Tenant-Object-Level.md) | [IDOR] The authenticated user can restart website build or view build logs on any another Federalist account |
| IDOR-014 | [144000](https://hackerone.com/reports/144000) | full | instacart | Privilege Escalation | $100 | [Cross-Tenant-Object-Level.md](../Cross-Tenant-Object-Level.md) | Authorization Bypass in Delivery Chat Logs |
| IDOR-015 | [178506](https://hackerone.com/reports/178506) | full | instacart | Information Disclosure | $100 | [Cross-Tenant-Object-Level.md](../Cross-Tenant-Object-Level.md) | Access private list metadata |
| IDOR-016 | [21210](https://hackerone.com/reports/21210) | full | mavenlink | Privilege Escalation | - | [Stale-Permission-and-Own-Action.md](../Stale-Permission-and-Own-Action.md) | privilege escalation |
| IDOR-017 | [235059](https://hackerone.com/reports/235059) | summary | mixmax | Privilege Escalation | - | [Stale-Permission-and-Own-Action.md](../Stale-Permission-and-Own-Action.md) | Privilege escalation-User who does not have access is able to add notes to the contact |
| IDOR-018 | [145950](https://hackerone.com/reports/145950) | full | nextcloud | Improper Authentication - Generic | - | [Role-Scoping-and-Vertical-Escalation.md](../Role-Scoping-and-Vertical-Escalation.md) | Uploading files to a folder where invited user don't have any EDIT privilege |
| IDOR-019 | [153905](https://hackerone.com/reports/153905) | full | nextcloud | Privilege Escalation | - | [Cross-Tenant-Object-Level.md](../Cross-Tenant-Object-Level.md) | IDOR - Disable sharing |
| IDOR-020 | [166581](https://hackerone.com/reports/166581) | summary | nextcloud | Privilege Escalation | - | [Cross-Tenant-Object-Level.md](../Cross-Tenant-Object-Level.md) | Privilege escalation - Normal user can somehow make admin to delete shared folders |
| IDOR-021 | [38965](https://hackerone.com/reports/38965) | full | phabricator | Improper Authentication - Generic | $300 | [Stale-Permission-and-Own-Action.md](../Stale-Permission-and-Own-Action.md) | Phabricator Diffusion application allows unauthorized users to delete mirrors |
| IDOR-022 | [202499](https://hackerone.com/reports/202499) | full | phabricator | Privilege Escalation | $300 | [Stale-Permission-and-Own-Action.md](../Stale-Permission-and-Own-Action.md) | User with only Viewing Privilege can send message to Room |
| IDOR-023 | [204292](https://hackerone.com/reports/204292) | summary | rockstargames | Cross-Site Request Forgery (CSRF) | - | [Cross-Tenant-Object-Level.md](../Cross-Tenant-Object-Level.md) | <- Critical IDOR vulnerability in socialclub allow to insert and delete comments as another user and it discloses sensitive information -> |
| IDOR-024 | [46397](https://hackerone.com/reports/46397) | full | security | Violation of Secure Design Principles | $500 | [Parameter-Gate-and-Hidden-Functions.md](../Parameter-Gate-and-Hidden-Functions.md) | Insecure Direct Object Reference vulnerability |
| IDOR-025 | [123420](https://hackerone.com/reports/123420) | summary | security | Improper Authentication - Generic | $500 | [Parameter-Gate-and-Hidden-Functions.md](../Parameter-Gate-and-Hidden-Functions.md) | Mediation link can be accepted by other users |
| IDOR-026 | [123572](https://hackerone.com/reports/123572) | full | security | Improper Authentication - Generic | - | [Role-Scoping-and-Vertical-Escalation.md](../Role-Scoping-and-Vertical-Escalation.md) | Unauthorized Team members viewing |
| IDOR-027 | [56511](https://hackerone.com/reports/56511) | full | shopify | Improper Authentication - Generic | $1000 | [Cross-Tenant-Object-Level.md](../Cross-Tenant-Object-Level.md) | IDOR expire other user sessions |
| IDOR-028 | [64164](https://hackerone.com/reports/64164) | summary | shopify | Privilege Escalation | $1000 | [Stale-Permission-and-Own-Action.md](../Stale-Permission-and-Own-Action.md) | Privilege Escalation - A `MEMBER` with no ACCESS to `ORDERS` can still access the orders by using  `Order Printer APP`  |
| IDOR-029 | [90671](https://hackerone.com/reports/90671) | summary | shopify | Uncontrolled Resource Consumption | - | [Role-Scoping-and-Vertical-Escalation.md](../Role-Scoping-and-Vertical-Escalation.md) | Privilege escalation vulnerability |
| IDOR-030 | [92453](https://hackerone.com/reports/92453) | summary | shopify | Improper Authentication - Generic | $2500 | [Cross-Tenant-Object-Level.md](../Cross-Tenant-Object-Level.md) | unauthorized access to all customers first and last name  |
| IDOR-031 | [92481](https://hackerone.com/reports/92481) | summary | shopify | Privilege Escalation | $500 | [Cross-Tenant-Object-Level.md](../Cross-Tenant-Object-Level.md) | Accessing Payments page and adding payment methods with limited access accounts |
| IDOR-032 | [93004](https://hackerone.com/reports/93004) | full | shopify | Privilege Escalation | $2000 | [Cross-Tenant-Object-Level.md](../Cross-Tenant-Object-Level.md) | unauthorized access to all collections name |
| IDOR-033 | [93680](https://hackerone.com/reports/93680) | summary | shopify | Privilege Escalation | $500 | [Role-Scoping-and-Vertical-Escalation.md](../Role-Scoping-and-Vertical-Escalation.md) | Missing authorization check on dashboard overviews |
| IDOR-034 | [93921](https://hackerone.com/reports/93921) | full | shopify | Improper Authentication - Generic | $2500 | [Cross-Tenant-Object-Level.md](../Cross-Tenant-Object-Level.md) | Unauthorized access to all collections, products, pages from other stores |
| IDOR-035 | [95441](https://hackerone.com/reports/95441) | summary | shopify | Improper Authentication - Generic | - | [Cross-Tenant-Object-Level.md](../Cross-Tenant-Object-Level.md) | Unauthorized access to any Store Admin's First & Last name |
| IDOR-036 | [95589](https://hackerone.com/reports/95589) | full | shopify | Improper Authentication - Generic | - | [Stale-Permission-and-Own-Action.md](../Stale-Permission-and-Own-Action.md) | Privilege escalation and circumvention of permission to limited access user |
| IDOR-037 | [97452](https://hackerone.com/reports/97452) | full | shopify | Privilege Escalation | $500 | [Role-Scoping-and-Vertical-Escalation.md](../Role-Scoping-and-Vertical-Escalation.md) | Staff members with no permission can access to the files, uploaded by the administrator |
| IDOR-038 | [154410](https://hackerone.com/reports/154410) | full | shopify | Privilege Escalation | - | [Stale-Permission-and-Own-Action.md](../Stale-Permission-and-Own-Action.md) | Delete/modify  your own comment after limited access(IDOR) |
| IDOR-039 | [243943](https://hackerone.com/reports/243943) | full | shopify | Insecure Direct Object Reference (IDOR) | $500 | [Role-Scoping-and-Vertical-Escalation.md](../Role-Scoping-and-Vertical-Escalation.md) | IDOR [partners.shopify.com] - User with ONLY Manage apps permission is able to get shops info and staff names from inside the shop |
| IDOR-040 | [198494](https://hackerone.com/reports/198494) | full | starbucks | - | - | [Enumeration-and-Financial-Objects.md](../Enumeration-and-Financial-Objects.md) | Lack of Controls Allowing for Card and PIN Enumeration Leading to Fraud |
| IDOR-041 | [115209](https://hackerone.com/reports/115209) | summary | uber | Improper Authentication - Generic | - | [Cross-Tenant-Object-Level.md](../Cross-Tenant-Object-Level.md) | Unauthorized file (invoice) download |
| IDOR-042 | [127161](https://hackerone.com/reports/127161) | summary | uber | Information Disclosure | - | [Cross-Tenant-Object-Level.md](../Cross-Tenant-Object-Level.md) | Information regarding trips from other users |
| IDOR-043 | [119166](https://hackerone.com/reports/119166) | full | udemy | Improper Authentication - Generic | - | [Cross-Tenant-Object-Level.md](../Cross-Tenant-Object-Level.md) | Able to view others' gifts on /gift/share URL, giftId is predictable, and easy to manipulate |
| IDOR-044 | [156537](https://hackerone.com/reports/156537) | summary | ui | - | - | [Parameter-Gate-and-Hidden-Functions.md](../Parameter-Gate-and-Hidden-Functions.md) | IDOR Causing Deletion of any account |
| IDOR-045 | [120115](https://hackerone.com/reports/120115) | full | veris | Privilege Escalation | - | [Cross-Tenant-Object-Level.md](../Cross-Tenant-Object-Level.md) | Critical - Insecure Direct Object Reference - Deleting any member of any organization remotely |
| IDOR-046 | [120121](https://hackerone.com/reports/120121) | full | veris | Privilege Escalation | - | [Cross-Tenant-Object-Level.md](../Cross-Tenant-Object-Level.md) | Critical IDOR - Delete any group of any organization remotely |
| IDOR-047 | [120123](https://hackerone.com/reports/120123) | full | veris | Privilege Escalation | - | [Cross-Tenant-Object-Level.md](../Cross-Tenant-Object-Level.md) | Critical IDOR - Delete any venue of any organization remotely |
| IDOR-048 | [120126](https://hackerone.com/reports/120126) | full | veris | Privilege Escalation | - | [Cross-Tenant-Object-Level.md](../Cross-Tenant-Object-Level.md) | Critical IDOR - Delete any rule of any organization remotely |
| IDOR-049 | [120288](https://hackerone.com/reports/120288) | full | veris | Privilege Escalation | - | [Cross-Tenant-Object-Level.md](../Cross-Tenant-Object-Level.md) | Critical IDOR - Delete any terminal/gatekeeper of any organization remotely |
| IDOR-050 | [120289](https://hackerone.com/reports/120289) | full | veris | Privilege Escalation | - | [Cross-Tenant-Object-Level.md](../Cross-Tenant-Object-Level.md) | Critical IDOR - Get anyone's Terminal Data remotely |
| IDOR-051 | [120291](https://hackerone.com/reports/120291) | full | veris | Privilege Escalation | - | [Cross-Tenant-Object-Level.md](../Cross-Tenant-Object-Level.md) | Critical IDOR - Set anyone's Terminal Data remotely |
| IDOR-052 | [120293](https://hackerone.com/reports/120293) | full | veris | Privilege Escalation | - | [Cross-Tenant-Object-Level.md](../Cross-Tenant-Object-Level.md) | Critical IDOR - Get Authentication Details of any Terminal/Gatekeeper |
| IDOR-053 | [120305](https://hackerone.com/reports/120305) | full | veris | Privilege Escalation | - | [Cross-Tenant-Object-Level.md](../Cross-Tenant-Object-Level.md) | Critical IDOR - Get venue data of any organization remotely |
| IDOR-054 | [120312](https://hackerone.com/reports/120312) | full | veris | Privilege Escalation | - | [Cross-Tenant-Object-Level.md](../Cross-Tenant-Object-Level.md) | Critical IDOR - Can select any Parent while creating new Venue |
| IDOR-055 | [120314](https://hackerone.com/reports/120314) | full | veris | Privilege Escalation | - | [Cross-Tenant-Object-Level.md](../Cross-Tenant-Object-Level.md) | Critical IDOR - Get Rules of any organization remotely |
| IDOR-056 | [120318](https://hackerone.com/reports/120318) | full | veris | Privilege Escalation | - | [Cross-Tenant-Object-Level.md](../Cross-Tenant-Object-Level.md) | Critical IDOR - Make Rule for Any Group & Any Venue remotely |
| IDOR-057 | [42587](https://hackerone.com/reports/42587) | full | vimeo | Improper Authentication - Generic | - | [ID-Scoping-and-Predictable-IDs.md](../ID-Scoping-and-Predictable-IDs.md) | Vimeo.com Insecure Direct Object References Reset Password |
| IDOR-058 | [45960](https://hackerone.com/reports/45960) | full | vimeo | Privilege Escalation | - | [ID-Scoping-and-Predictable-IDs.md](../ID-Scoping-and-Predictable-IDs.md) | CRITICAL vulnerability - Insecure Direct Object Reference - Unauthorized access to `Videos` of Channel whose privacy is set to `Private`. |
| IDOR-059 | [52176](https://hackerone.com/reports/52176) | full | vimeo | Improper Authentication - Generic | - | [ID-Scoping-and-Predictable-IDs.md](../ID-Scoping-and-Predictable-IDs.md) | Insecure Direct Object References in https://vimeo.com/forums |
| IDOR-060 | [52181](https://hackerone.com/reports/52181) | full | vimeo | Improper Authentication - Generic | - | [ID-Scoping-and-Predictable-IDs.md](../ID-Scoping-and-Predictable-IDs.md) | Insecure Direct Object References that allows to read any comment (even if it should be private) |
| IDOR-061 | [137502](https://hackerone.com/reports/137502) | full | vimeo | Information Disclosure | - | [Cross-Tenant-Object-Level.md](../Cross-Tenant-Object-Level.md) | All Vimeo Private videos disclosure via Authorization Bypass |
| IDOR-062 | [244567](https://hackerone.com/reports/244567) | full | wakatime | Privilege Escalation | - | [Cross-Tenant-Object-Level.md](../Cross-Tenant-Object-Level.md) | [Privilege Escalation] Authenticated users can manipulate others fullname without their knowledge |
| IDOR-063 | [244636](https://hackerone.com/reports/244636) | full | wakatime | Insecure Direct Object Reference (IDOR) | - | [Invocation-Layer-Mass-Assignment.md](../Invocation-Layer-Mass-Assignment.md) | IDOR create accounts and verify them with original account email |
| IDOR-064 | [245340](https://hackerone.com/reports/245340) | full | wakatime | Improper Access Control - Generic | - | [Invocation-Layer-Mass-Assignment.md](../Invocation-Layer-Mass-Assignment.md) | Bypassing Access control, changing owner's name in a private leaderboard |
| IDOR-065 | [247225](https://hackerone.com/reports/247225) | full | wakatime | Improper Access Control - Generic | - | [Invocation-Layer-Mass-Assignment.md](../Invocation-Layer-Mass-Assignment.md) | Session Duplication due to Broken Access Control |
| IDOR-066 | [223434](https://hackerone.com/reports/223434) | full | weblate | Improper Access Control - Generic | - | [Role-Scoping-and-Vertical-Escalation.md](../Role-Scoping-and-Vertical-Escalation.md) | Improper access control when an added email address is deleted from authentication |
| IDOR-067 | [232994](https://hackerone.com/reports/232994) | full | weblate | Improper Access Control - Generic | - | [Role-Scoping-and-Vertical-Escalation.md](../Role-Scoping-and-Vertical-Escalation.md) | API Does Not Apply Access Controls to Translations |
| IDOR-068 | [31082](https://hackerone.com/reports/31082) | full | x | Violation of Secure Design Principles | $420 | [Enumeration-and-Financial-Objects.md](../Enumeration-and-Financial-Objects.md) | Unauthorized Tweeting on behalf of Account Owners |
| IDOR-069 | [31188](https://hackerone.com/reports/31188) | full | x | Violation of Secure Design Principles | - | [Parameter-Gate-and-Hidden-Functions.md](../Parameter-Gate-and-Hidden-Functions.md) | Creating Unauthorized Audience Lists |
| IDOR-070 | [52646](https://hackerone.com/reports/52646) | full | x | Improper Authentication - Generic | - | [ID-Scoping-and-Predictable-IDs.md](../ID-Scoping-and-Predictable-IDs.md) | Insecure direct object reference - have access to deleted DM's |
| IDOR-071 | [53858](https://hackerone.com/reports/53858) | full | x | Privilege Escalation | - | [ID-Scoping-and-Predictable-IDs.md](../ID-Scoping-and-Predictable-IDs.md) | Insecure Direct Object Reference - access to other user/group DM's |
| IDOR-072 | [95552](https://hackerone.com/reports/95552) | full | x | Improper Authentication - Generic | - | [Cross-Tenant-Object-Level.md](../Cross-Tenant-Object-Level.md) | IDOR- Activate Mopub on different organizations- steal api token- Fabric.io |
| IDOR-073 | [181748](https://hackerone.com/reports/181748) | full | x | Privilege Escalation | - | [ID-Scoping-and-Predictable-IDs.md](../ID-Scoping-and-Predictable-IDs.md) | [IDOR][translate.twitter.com] Opportunity to change any comment at the forum |

Totals: 73 cases; 19 with disclosed bounty; recorded bounty sum $14470; evidence split full=55 / summary=18.

## External blog sources (methodology + modern-era cases)

| Blog | Evidence | Use |
| --- | --- | --- |
| [How a "Fixed" IDOR and an Empty String Led to 5 Million+ File Leaks - Hacktus](https://hacktus.tech/how-a-fixed-idor-and-an-empty-string-led-to-5-million-file-leaks) | full | BLOG-001 - modern chain: obfuscated-id "fix" bypass + bucket-list leak; cited in Cross-Tenant 3.8 and Agent Playbook |
| [From JavaScript Analysis To UUID Pattern Exploration Revealed a Critical IDOR! - Omar Alzughaibi](https://omaralzughaibi.com/blog/javascript-analysis-uuid-pattern-idor) | full | BLOG-002 - modern UUID-pattern exploitation; cited in Cross-Tenant 3.8 and ID-Scoping 2.11 |
| [When Path Normalization Beats Middleware - Omar Alzughaibi](https://omaralzughaibi.com/blog/path-normalization-authorization-bypass/) | full | BLOG-003 - missing-Authorization-header bypass and backslash-path middleware confusion; cited in Invocation-Layer 2.7 |
| [How I Exposed Instagram's Private Posts by Blocking Users - 003random](https://003random.com/posts/meta-bountycon-instagram-writeup/) | full | BLOG-004 - oEmbed + User-Agent + block-state chain to read private-account media; cited in Parameter-Gate 2.11 |
| [Exploring Rails Mass Assignment Vulnerability - Robbie Jaeger](https://medium.com/@jaeger.rob/exploring-rails-mass-assignment-vulnerability-b8b3d19e20b6) | full | BLOG-005 - mass-assignment fundamentals; cited in Invocation-Layer 2.6 |
| [Critical Variable Mass Assignment in Adobe ColdFusion CVE-2023-44350 - HoyaHaxa](https://www.hoyahaxa.com/2023/11/critical-variable-mass-assignment.html) | full | BLOG-006 - modern mass assignment reaching ACL logic; cited in Invocation-Layer 2.5 |

### Read but excluded (not IDOR-class domains)

- Kubernetes RCE via Nodes/Proxy GET - Graham Helton (https://grahamhelton.com/blog/nodes-proxy-rce) - k8s RBAC, not web object-level authz
- Whos SHA is it Anyway (Cloud Build TOCTOU $30k) - Adnan Khan (https://adnanthekhan.com/posts/cloud-build-toctou/) - CI/CD race condition
- AWS IAM privilege-escalation series (Rhino Security Labs parts 1 and 2, BishopFox, PwnedLabs) - cloud-IAM domain
- ConfusedFunction - Tenable (https://www.tenable.com/blog/confusedfunction-a-privilege-escalation-vulnerability-impacting-gcp-cloud-functions) - GCP service-account escalation
- CVE-2023-22518 Confluence - ProjectDiscovery (https://blog.projectdiscovery.io/atlassian-confluence-auth-bypass/) - product CVE analysis
- Ruby-SAML / GitLab CVE-2024-45409 - ProjectDiscovery (https://blog.projectdiscovery.io/ruby-saml-gitlab-auth-bypass/) - SAML signature handling
- CVE-2023-4369 Chrome extension sandbox escape - 0x44.xyz (https://0x44.xyz/blog/cve-2023-4369/)

Non-IDOR archive reports fetched for exclusion check: 41 returned HTTP 404 or were not IDOR-class; candidates recorded in /tmp dataset.
