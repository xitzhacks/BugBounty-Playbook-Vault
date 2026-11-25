---
title: "Adjacent merges — classified adjacent pool + unclassified merges: Kibana RCE, Electron/Node sandboxes, Shopify takeover family, GHSL queries"
type: playbook
category: adjacent-merges
cwe: "CWE-732"
source_count: 39
full_bodies_available: 34
corpus: "h1-brain disclosed_reports.db (3,673 rows), priv-esc bucket + module_map_all.json merges"
list_accessed: "2026-11-07"
note: "Last module: 15 classified-adjacent + 24 unclassified merges. Anchors: PRIV-852613 ($10,000), PRIV-1168765 ($10,000), PRIV-861744 ($5,000). GHSL rows (5) are metadata-only."
---

# Adjacent Merges — the last module: RCE-labelled rows, takeover continuations, and query rows

## 1. Overview

Thirty-nine rows, **$51,245/22 paid** — the vault's richest module by figure, and deliberately the last one the reader reaches. It holds two pools: 15 rows the classifier labelled `Privilege Escalation` / `Improper Authorization` but whose bodies are adjacent classes (RCE, prototype pollution, sandbox bypass, token theft), and 24 rows merged in from the `unclassified` pool (Shopify takeover continuations, GHSL query rows, IDORs) that `module_map_all.json` assigns to `priv-esc`. Together they are $39,055/12 + $12,190/10. The module exists because dropping either pool would silently drop the vault's two largest figures ($10,000 ×2) and because the merge rows are the direct continuations of module 02's staff/GraphQL mechanism family — same primitive, different provenance. Five rows (all GHSL, 54-byte one-liners) are metadata-only; every other body was read end-to-end (34 full bodies).

**Case-stock (39 rows / $51,245):**

| Case | Target | Mechanism | Bounty |
|---|---|---|---|
| [PRIV-852613](https://hackerone.com/reports/852613) | elastic — cloud.elastic.co | prototype pollution via _.set → Kibana RCE | $10,000 |
| [PRIV-1168765](https://hackerone.com/reports/1168765) | elastic — Kibana | reporting headless Chromium --no-sandbox → RCE hazard | $10,000 |
| [PRIV-861744](https://hackerone.com/reports/861744) | elastic — cloud.elastic.co | SIEM bulk_create_ml_signals pollution → RCE | $5,000 |
| [PRIV-2138080](https://hackerone.com/reports/2138080) | ibb — https://github.com/Electron | Electron bridge exception → isolated-world reach | $2,550 |
| [PRIV-2091137](https://hackerone.com/reports/2091137) | ibb — https://github.com/nodejs/node | OpenSSL engine → disable Node permission model (CVE-2023-30586) | $2,540 |
| [PRIV-2065306](https://hackerone.com/reports/2065306) | ibb — https://github.com/apache/airflow | Airflow odbc provider code execution | $2,480 |
| [PRIV-1861974](https://hackerone.com/reports/1861974) | pixiv — booth.pm | OAuth redirect_uri traversal → auth-code leak | $2,000 |
| [PRIV-1550400](https://hackerone.com/reports/1550400) | shopify — partners.shopify.com | Manage-public-listings → theme upload | $1,900 |
| [PRIV-891268](https://hackerone.com/reports/891268) | github-security-lab | Java CWE-939 improper URL auth (GHSL query row) | $1,800 |
| [PRIV-1483919](https://hackerone.com/reports/1483919) | github-security-lab | CPP CWE-266 incorrect privilege assignment (GHSL query) | $1,800 |
| [PRIV-1439552](https://hackerone.com/reports/1439552) | gitlab — https://gitlab.com/gitlab-org/gitlab-pages | Pages service-worker steals gitlab-pages cookies | $1,680 |
| [PRIV-1266828](https://hackerone.com/reports/1266828) | shopify — Shopify Developed Apps | wholesale invite-link reuse → account takeover | $1,600 |
| [PRIV-122113](https://hackerone.com/reports/122113) | ibb — IBB (Legacy) | OpenSSH/dropbear xauth command injection | $1,500 |
| [PRIV-929288](https://hackerone.com/reports/929288) | github-security-lab | Java CWE-939 improper URL auth (GHSL query row) | $1,500 |
| [PRIV-2079502](https://hackerone.com/reports/2079502) | security — support.hackerone.com | create ticket in any Helpdesk account | $1,000 |
| [PRIV-1679734](https://hackerone.com/reports/1679734) | shopify — Shopify Developed Apps | Collabs missing email verification → takeover | $800 |
| [PRIV-1050244](https://hackerone.com/reports/1050244) | nextcloud — nextcloud/server | 2FA enforcement bypass (Nextcloud) | $750 |
| [PRIV-2120719](https://hackerone.com/reports/2120719) | ibb — https://github.com/nodejs/node | process.binding dependency-policy bypass | $635 |
| [PRIV-2208656](https://hackerone.com/reports/2208656) | ibb — https://github.com/apache/airflow | Airflow permission bypass → task instances (CVE-2023-42663) | $540 |
| [PRIV-2065288](https://hackerone.com/reports/2065288) | ibb — https://github.com/apache/airflow | Airflow jdbc provider code execution | $520 |
| [PRIV-1279322](https://hackerone.com/reports/1279322) | shopify — Shopify Developed Apps | wholesale store adds address without staff | $500 |
| [PRIV-1398270](https://hackerone.com/reports/1398270) | evernote — www.evernote.com | server-log disclosure → info leak | $150 |
| [PRIV-150976](https://hackerone.com/reports/150976) | ibb — IBB (Legacy) | Flash local-with-filesystem bypass (CVE-2016-4178) | - |
| [PRIV-194351](https://hackerone.com/reports/194351) | yelp | download arbitrary PHP files | - |
| [PRIV-287789](https://hackerone.com/reports/287789) | bohemia | IDOR → user order information | - |
| [PRIV-541606](https://hackerone.com/reports/541606) | shopify — your-store.myshopify.com | Settings → Customer permission hop (Shopify Admin) | - |
| [PRIV-791775](https://hackerone.com/reports/791775) | shopify — your-store.myshopify.com | confirm arbitrary email → SSO takeover any owner | - |
| [PRIV-796808](https://hackerone.com/reports/796808) | shopify — your-store.myshopify.com | email-confirm bypass Part II (SSO merge) | - |
| [PRIV-796956](https://hackerone.com/reports/796956) | shopify — your-store.myshopify.com | SSO accounts merged via /accounts_merge/new-password | - |
| [PRIV-837018](https://hackerone.com/reports/837018) | wordpress — BuddyPress Core | BuddyPress Moderate → Administrator | - |
| [PRIV-867513](https://hackerone.com/reports/867513) | shopify — accounts.shopify.com | POS GraphQL email update → Shopify ID takeover | - |
| [PRIV-892904](https://hackerone.com/reports/892904) | shopify — your-store.myshopify.com | link Google account to owner/store owner | - |
| [PRIV-985150](https://hackerone.com/reports/985150) | shopify — Shopify Developed Apps | POS Manage-Staff → Plan & Permissions owner feats | - |
| [PRIV-1092859](https://hackerone.com/reports/1092859) | kubernetes — https://github.com/kubernetes/kops | kOps docs dangling NS → full DNS takeover | - |
| [PRIV-1587150](https://hackerone.com/reports/1587150) | github-security-lab | Python PAM authorization bypass (GHSL query) | - |
| [PRIV-1602234](https://hackerone.com/reports/1602234) | github-security-lab | CPP PAM authorization bypass (GHSL query) | - |
| [PRIV-1901713](https://hackerone.com/reports/1901713) | acronis — beta-cloud.acronis.com | IDOR in backup recovery | - |
| [PRIV-2037902](https://hackerone.com/reports/2037902) | automattic | JetPack SSO manager auth bypass → wp-admin | - |
| [PRIV-3178999](https://hackerone.com/reports/3178999) | security — api.hackerone.com | SCIM provisioning → existing-account takeover | - |

## 2. The Kibana trilogy: prototype pollution prices at $10,000, hazard at $10,000

PRIV-852613 (elastic, **$10,000**) is the vault's joint-largest row: a prototype pollution in the upgrade-assistant telemetry collector (`_.set` on a saved-object document) → RCE:

> A prototype pollution in Kibana can be used to gain remote code execution.

> We can pollute the prototype by providing a specially crafted "upgrade-assistant-telemetry" "saved object".

PRIV-861744 (elastic, **$5,000**) is the same researcher's follow-up on the pre-release SIEM signal feature (`bulk_create_ml_signals.ts`) — identical `__proto__.sourceURL` payload, different polluter. PRIV-1168765 (elastic, **$10,000**) is the third leg: reporting embeds a headless Chromium run with `--no-sandbox`:

> Reporting uses a headless Chromium to generate PNGs and PDFs.

The researcher demonstrates RCE inside the containerized headless shell via a malicious HTML file, but honestly labels it a "hazard" because the last mile (getting reporting to render attacker-controlled JS) needs an HTML-injection or open-redirect on the victim side. The corpus pays the hazard at the same $10,000 as the complete chain — the price follows the demonstrated engine break, not the completed chain. The adjacent lesson is the vault's thesis in miniature: a sandbox (`--no-sandbox`, a permission model, a `_.set` allowlist) that is correctly stated but incorrectly implemented is itself the finding.

## 3. The sandbox-bypass rows: Electron, Node, Airflow

Three paid rows price another system's sandbox at $2,400–$2,600 each — same shape as the Kibana hazard, different victim: PRIV-2138080 (Electron, **$2,550**) — an unserializable return value (or a throwing getter) at the `contextBridge` smuggles a privileged object into the isolated world:

> This is a context isolation bypass, meaning that code running in the main world context in the renderer can reach into the isolated Electron context and perform privileged actions.

PRIV-2091137 (Node, **$2,540**, CVE-2023-30586) — `crypto.setEngine()` loads arbitrary OpenSSL engines behind the permission model:

> Node.js 20 allows loading arbitrary OpenSSL engines even when the permission model is enabled, which can bypass and/or disable the permission model.

PRIV-2120719 (Node, **$635**) is its `process.binding` variant, and the Airflow quartet (2065288 jdbc $520, 2065306 odbc $2,480, 2208656 permission bypass $540/CVE-2023-42663, plus 2249299 in module 02) shows the same bypass from the provider side. The doctrine: when the corpus labels these `Privilege Escalation`, it means the attacker escapes a capability restriction the platform declared. The vault keeps them adjacent precisely so the operator reads the Kibana and Electron rows as one lesson.

## 4. The Shopify takeover family: the merge rows as module-02 continuations

The 24 unclassified merges are the strongest argument for the last-module design: they are module 02's mechanism family split by provenance. The clearest thread is the email-confirmation takeover trilogy: PRIV-791775 ("confirm arbitrary email" — the mailer sends the new email's confirmation to the old address) → PRIV-796808 (Part II) → PRIV-796956 ("Able to Takeover Merchants Accounts Even They Have Already Setup SSO, After Bypassing the Email Confirmation", via `/accounts_merge/new-password`). The anchor sentence of that thread:

> It's possible to take over any store account through bypassing the email confirmation step in *.myshopify.com.

The POS GraphQL thread (PRIV-867513: update a staff email via `pos-channel.shopifycloud.com/graphql-proxy/admin` with no confirmation, then mint a Shopify ID) and PRIV-985150 (POS Manage-Staff role navigating to Plan & Permissions owner features), the wholesale thread (PRIV-1266828, **$1,600** — "get invite link" reused for an already-activated customer → takeover; PRIV-1279322, **$500** — adds an address without staff), and PRIV-1550400 (Manage-public-listings → Theme Store upload, **$1,900**) complete the takeover family. GitLab Pages (PRIV-1439552, **$1,680**):

> It is possible to steal Gitlab Pages session tokens by intercepting requests to the `/auth` endpoint on a Pages site using service workers.

and the Nextcloud 2FA row (1050244, **$750**):

> the attacker could bypass the two-factor authentication enforcement

are the same primitive from the token side. The GHSL rows (891268 $1,800, 1483919 $1,800, 929288 $1,500, 1587150/1602234 no figure) are 54-byte metadata-only records — `[Java] CWE-939`, `CWE-266`, PAM queries — carrying $5,100 with no quotable technique; they are recorded as corpus, not evidence.

## 5. The remaining rows

No further quotes: PRIV-122113 (xauth injection, $1,500), PRIV-150976 (Flash bypass), PRIV-194351 (yellp PHP files), PRIV-1861974 (OAuth `redirect_uri` traversal, $2,000), PRIV-1398270 (log disclosure, $150), PRIV-1092859 (kOps dangling NS → full zone takeover — the DNS-class apex row, quoted in the register), PRIV-287789/541606/837018/892904/1901713/2037902/3178999/2079502 ($1,000 helpdesk ticket). Each body was read; none needed quoting beyond the anchors.

## 6. What pays/what doesn't

- **Sandbox breaks pay at $2,500–$10,000** (Kibana $10,000 ×2 + $5,000; Electron $2,550; Node $2,540). The corpus prices the sandbox escape even when the last mile is documented as missing (1168765's "hazard").
- **Takeover price follows the account reached:** wholesale/reusable-invite ($1,600), theme upload ($1,900), helpdesk ticket ($1,000), Collabs email verification ($800), 2FA enforcement ($750). The no-figure Shopify rows (791775/796956/867513/985150) are the same class with no figure recorded — the module does not invent prices for them.
- **GHSL query rows pay for the query, not the body:** $1,800/$1,800/$1,500/$0/$0 across five identical one-liners. The vault teaches them as the corpus's price list for tooling contributions, not as privilege-escalation technique.
- **Token-theft chains** (1439552 $1,680; 1861974 $2,000) pay when the stolen token is demonstrated working on a second site or read in Analytics — the "then some" doctrine again.

## 7. Cross-references

- Modules 02 and this module should be read as one staff/authorization sweep; the split is provenance (bucket vs merge), not mechanism.
- The Prototype-Pollution vault owns the pollution taxonomy; the RCE vault owns the Kibana endgame formatting; the IDOR vault owns the redirect/IDOR rows — cited here, not re-taught.
- The playbook (PRIV-Testing-Agent-Playbook.md) P2 replays the merge rows' confirmation-link and invite-link lanes alongside the bucket's staff lanes.
