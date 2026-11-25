---
title: "Business Logic ("Payment, coupons, logic flaws) — vault index"
type: index
category: "Business Logic (master row 12): commerce/payments/rewards, account/invite/access workflows, race-condition replay, rate-limit & state abuse, adjacent noise"
built: "2026-11-07"
evidence: "118 bucket rows (classified.json business-logic, DB-verified byte-identical to disclosed_reports.db) + 9 unclassified merges from module_map_all.json, all 127 bodies read end-to-end"
bounty: "$60,090 corpus-floor · 55/127 rows paid · max $7,500 · bucket-only $56,590/52, merges add $3,500/3"
companion_vaults: "../Race-Conditions · ../Rate-Limiting · ../13_Subdomain-Takeover · ../Authentication-Session"
case_id_scheme: "BL-<HackerOne report id>"
quote_rule: "byte-true from read bodies, anchored in references/archive/BL-bodies-full-dump.txt"
---

# Business Logic — Vault

**Case-ID scheme:** `BL-<h1-id>` where `<h1-id>` is the row `id` in the h1-brain corpus DB (`/home/user/tools/h1-brain/disclosed_reports.db`, table `disclosed_reports`).

## Provenance (what this vault is built from)

- Source: h1-brain pre-built DB of publicly disclosed, bounty-awarded HackerOne reports — **3,673 rows**, full `vulnerability_information` bodies.
- DB fetched from the repo's Git-LFS pointer; sha256 verified `8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4`.
- Business-logic bucket = **118 rows** selected by the CWE-style weakness label `Business Logic Errors` plus the classifier's keyword net over titles/bodies; all 118 verified byte-identical between `classified.json` and the DB (title, body, program, bounty, weakness).
- Unclassified merges: 9 rows from the classifier's `unclassified` pool (no `classified.json` entry, DB `weakness_name=None`) merged in by `module_map_all.json` on body read — their bodies were pulled from the DB.
- Evidence levels, honestly labeled:
  - **Full body** — 127/127 cases read end-to-end and quoted from body text (no metadata-only rows in this bucket).
  - **Bodies-win classification** — module assignment decided by body, not title; 31 `_adjacent` rows are other-class by body (see module 05 §3–§5).

## Scoreboard (127 rows · 55 paid · $60,090 · max $7,500)

| Case | Title (short) | Program | Bounty | Module |
|---|---|---|---|---|
| BL-1295844 | In-flight signature smuggle → Steam wallet mint | valve | **$7,500** (max) | commerce |
| BL-1285598 | Unclaimed S3 bucket in Reddit build scripts → malware hosting | reddit | **$5,000** | adjacent |
| BL-1543159 | `admin_approval→APPROVED` PATCH → free ad delivery | reddit | **$5,000** | commerce |
| BL-1849626 | Fee-discount accept ×30 (serial) → $600k fee-free | stripe | **$5,000** | commerce |
| BL-1044285 | Empty `checkout_token` → most-recent-order download links | shopify | **$2,900** | merges |
| BL-334205 | Leave-program + `security@` invite harvest | security | **$2,500** | account/invite |
| BL-1565623 | curl `--no-clobber --remove-on-error` wrong-file removal | ibb | **$2,400** (CVE-2022-27778) | adjacent |
| BL-1565624 | curl TLS/SSH connection too-eager reuse | ibb | **$2,400** (CVE-2022-27782) | adjacent |
| BL-1614331 | curl state-file rename widens permissions | ibb | **$2,400** (CVE-2022-32207) | adjacent |
| BL-1912778 | libcurl FTP connection reuse with wrong credentials | ibb | **$2,400** (CVE-2023-27535) | adjacent |
| BL-2588329 | Change-phone OTP accepts `0000` → any phone number | indrive | **$2,000** | account/invite |
| BL-263760 | Widget preview cache revives private/deleted tweets | x | **$1,120** | adjacent |
| BL-226199 | Five-bug chain → victim program's JIRA re-pointed | security | **$1,000** | account/invite |
| BL-462503 | GitLab auto-link claims npm name → malicious module | gitlab | **$1,000** | rate/state |
| BL-1234760 | curl `CURLOPT_SSLCERT` keychain/cwd mixup | curl | **$1,000** (CVE-2021-22926) | adjacent |
| BL-1172857 | schannel cipher-list static override | curl | **$800** (CVE-2021-22897) | adjacent |
| BL-312118 | Unlimited GitLab Pages domains → 110 hijacks in 5s | gitlab | **$750** | rate/state |
| BL-1213175 | metalink hash-mismatch file kept on disk | curl | **$700** (CVE-2021-22922) | adjacent |
| BL-666632 | Inverted DM `conversation_id` deletes history | x | **$560** | account/invite |
| BL-361960 | Sides/modifiers count client-only validation | upserve | **$500** | commerce |
| BL-1213765 | PayPal `order_id` swap → big coin pack for $1.99 | reddit | **$500** | commerce |
| BL-413759 | Location-create race: 12 locations on a 4 cap | shopify | **$500** | race |
| BL-460920 | Response program creates full bounty table | security | **$500** | rate/state |
| BL-475660 | `eligible_for_bounty` persists into Response program | security | **$500** | rate/state |
| BL-331691 | Draft-program invite token never consumed | security | **$500** | account/invite |
| BL-463828 | Embedded-submission grant survives leaving program | security | **$500** | account/invite |
| BL-549364 | Recovery SMS points at registrable lookalike domain | security | **$500** | account/invite |
| BL-763177 | Low-priv `{F27}` plant → admin edit republishes private file | phabricator | **$500** | account/invite |
| BL-1770797 | `h1_analyst_*` strings in normal usernames | security | **$500** | account/invite |
| BL-1112679 | Dangling Workday IP at `vpn.inverselink.com` | security | **$500** | adjacent |
| BL-1297689 | S3 bucket → `www.*.affirm.com` takeover | affirm | **$500** | adjacent |
| BL-706934 | `Kernel#JSON` misses CVE-2013-0269 branch | ruby | **$500** (CVE-2013-0269) | adjacent |
| BL-1365738 | Legacy Yahoo server → any user's password hash | flickr | **$500** | adjacent |
| BL-1614332 | FTP-KRB message-verify failure handling | ibb | **$480** (CVE-2022-32208) | adjacent |
| BL-1397826 | Unclaimed `tendermint-packages` bucket | cosmos | **$400** | adjacent |
| BL-1182864 | Signed EC2 IP → `fr1.vpn.zomans.com` takeover | zomato | **$350** | adjacent |
| BL-434116 | Illegal `vote_id` unlocks gated poll results | phabricator | **$300** | merges |
| BL-1566325 | `feed.publish` `authorPHID` spoof | phabricator | **$300** | merges |
| BL-1523584 | Order-ID IDOR → another's WhatsApp updates | zomato | **$300** | account/invite |
| BL-3136790 | Airplane-mode past underage support lock | toolsforhumanity | **$300** | commerce |
| BL-2801036 | Malicious project name logs out all members | doppler | **$250** | rate/state |
| BL-2257374 | Premium+ cycle skips profile-pic review | x | **$250** | commerce |
| BL-974892 | Data-credits transfer race → free credits | helium | **$250** | race |
| BL-1364851 | WordPress plugin-update confusion (supply chain) | trafficfactory | **$200** | adjacent |
| BL-1538669 | Payment-status IDOR across accounts | omise | **$100** | commerce |
| BL-1406926 | Circles bypass forced share passwords | nextcloud | **$100** (CVE-2022-29163) | rate/state |
| BL-808287 | Contact image accepts any file type | nextcloud | **$100** (CVE-2020-8181) | account/invite |
| BL-1316650 | Unclaimed `brave-extensions` bucket | brave | **$50** | adjacent |
| BL-428660 | Silent password-policy failure leaves files public | nextcloud | **$50** | account/invite |

Corpus program mix (127 rows): security 19 · ibb 11 · automattic 8 · shopify 7 · x 5 · zomato 6 · gitlab 4 · chaturbate 4 · nextcloud 4 · legalrobot 3 · upserve 3 · curl 3 · reddit 3 · cosmos 3 · indrive 3 (bucket counts; merges add vimeo, phabricator ×2, mattermost, cs_money, shopify).

## Vault map

| File | Content |
|---|---|
| `BL-Testing-Agent-Playbook.md` | Agent-facing operational playbook: P0 program/policy → P1 entry-point inventory → P2 probe protocol (serial-first, boundary sweep) → P3 proof ladder → P4 modern hardening → P5 kill-gates · module↔phase table · non-goals |
| `Commerce-Payments-Rewards.md` | Money-math tampering: wallet-mint signature smuggle ($7,500), approval overwrite ($5,000), fee replay ($5,000), quantity/total/plan-ID family, entitlement abuse, makerdao protocol accounting |
| `Account-Invite-Access-Workflows.md` | Workflow-as-vulnerability: leave/rejoin invite harvest ($2,500), OTP-accept-anything ($2,000), JIRA re-pointing ($1,000), status/role gates, post-leave access |
| `Race-Condition-Replay.md` | Parallel-replay slice: gift-card (7×), credit-transfer mint, location-limit race, invite duplication; client-side postMessage race outlier |
| `Rate-Limit-State-Abuse.md` | Unthrottled endpoints, brute-forceable state (cookie-MD5 OTP), mass name/domain claims ($1,000/$750), HackerOne program-state abuse, Unicode-normalization bypass |
| `Adjacent-Unclassified-Noise.md` | Overflow shelf: 9 unclassified-merge true positives (incl. $2,900 download-link row), subdomain-takeover cluster, curl/ibb CVE shelf, drifted genuine logic rows |
| `references/source-index.md` | Provenance, funnel, classification mechanics, 5 limits |
| `references/case-register.md` | 127-row ledger with DB metadata, evidence level, CVEs |
| `references/archive/BL-bodies-full-dump.txt` | All 127 bodies verbatim (anchor for every quote) |
| `references/archive/classes.json` | Frozen module assignment for all 127 rows |

## Cross-vault links

- `Race-Conditions/` — module 03 is the same attack class's business-logic slice: BL-1849626's serial-replay-is-not-a-race and BL-759247/974892's Turbo-Intruder races are its shopping-list cases; the Stripe redemption-limit row there is this vault's BL-413759 sibling.
- `Rate-Limiting/` (`20_Rate-Limiting/`) — module 04 is its bucket slice; BL-905816 (cookie-MD5 brute-force) and BL-1991376 (SMS-code blasting) belong to both vaults' state-secret families.
- `13_Subdomain-Takeover/` — module 05 §3's 8 rows are their class; the cross-cite is recorded there.
- `Authentication-Session/` — BL-2588329 (universal OTP), BL-783258 (2FA password never verified), BL-1443211 (cross-account OTP) are its OTP/verification-module rows.
- `IDOR/` — BL-1538669 (payment status), BL-1523584 (order-ID→WhatsApp), BL-225831 (billing-admin enumeration) are its object-access slice.
- `Business-Logic/` self-refs in Race vault now resolve to this vault.

## Limitations

1. **Count basis differs from the master list.** Master row 12 cites a 378-row external count ("payment, coupons, logic flaws"); this vault quotes only the h1-brain DB subset (118 bucket rows + 9 unclassified merges). A v2 sweep of the ~468-row unclassified pool may add cases.
2. **Weakness label ≠ class authority.** All 118 bucket rows carry `Business Logic Errors` in the DB, yet 31 are other classes by body (subdomain takeover, curl CVEs, deserialization, misconfiguration). Bodies are the class authority; the register keeps the DB label.
3. **Bounty `None` ≠ unpaid.** 72 of 127 rows carry no figure; $60,090 is a corpus-floor, not a total. Five-figure rows are real-money deltas, not rate-card maxima.
4. **No metadata-only rows — but redacted bodies.** All 127 bodies are full text, yet 12 carry redactions (████ blocks, {F…} attachment markers) and several (e.g. BL-1089978, BL-423467) are frank that verification is incomplete. Quotes stop where the body stops.
5. **Program `security` skew (19 rows).** The class's densest surface is measured against HackerOne itself; vendor-diverse pricing evidence (valve, stripe, reddit, gitlab, indrive) is the better pay-rate guide.
6. **Chainpay vs logicpay.** Adjacent-pool money ($24,580, 41% of the total) pays under *other* classes' rules (takeover/CVE flat rates). Pure business-logic ceiling in this corpus: $7,500.
7. **QA**: all block quotes in modules were byte-verified against `references/archive/BL-bodies-full-dump.txt`; `(sic)` marks author typos.


<!-- CASESTOCK-LINK:BEGIN -->

## Case stock — vault (`_VAULT/`)

**360 disclosed reports** routed to this category · 79 with a bounty figure · **$104,913** · 246 full write-ups stored locally.

- Full list: [`_VAULT/by-vault-category/12_Business-Logic.md`](../_VAULT/by-vault-category/12_Business-Logic.md)
- Query: `sqlite3 ../_VAULT/reports.sqlite "SELECT id,bounty,title FROM reports WHERE ..."`
- Pull one write-up: `python3 ../_VAULT/scripts/extract_report.py <id>`

| Top paid | Program | Bounty |
|---|---|---|
| [894569](https://hackerone.com/reports/894569) An attacker can run pipeline jobs as arbitrary user | GitLab | $12,000 |
| [307239](https://hackerone.com/reports/307239) Double Payout via PayPal | Coinbase | $10,000 |
| [1295844](https://hackerone.com/reports/1295844) Modify in-flight data to payment provider Smart2Pay | Valve | $7,500 |
| [377398](https://hackerone.com/reports/377398) A miner can manipulate the gas reporting bond | Augur | $5,000 |
| [470041](https://hackerone.com/reports/470041) Дюп предметов lootdog и возможность их продавать. | Mail.ru | $5,000 |

_refreshed 2026-11-17 from the public HackerOne disclosed-report dataset_
<!-- CASESTOCK-LINK:END -->
