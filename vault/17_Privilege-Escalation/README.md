---
title: "Vault/Privilege-Escalation — hop-then-reach playbook set"
type: index
category: "Privilege Escalation (all lanes in one vault: subdomain dangling takeover, broken access control / staff / GraphQL authorization, local privilege escalation, container & kernel escape, adjacent merges)"
built: "2026-11-07"
evidence: "172 rows from h1-brain DB (148 priv-esc bucket + 24 unclassified merges) → 167 full bodies read + 5 GHSL metadata-only · every bucket row appears in exactly one module (verified)"
bounty: "$106,265 roster-tagged (bucket $94,075/62 + merges $12,190/10) · pure class 01–04 $55,020/50 · adjacent merges 05 $51,245/22 · full reconciliation in references/case-register.md"
companion_vaults: "../IDOR · ../Authentication-Session · ../Race-Conditions · ../Subdomain-Takeover · ../Prototype-Pollution · ../RCE"
case_id_scheme: "PRIV-<HackerOne report id>"
quote_rule: "byte-true, (sic)-marked, from read bodies only; GHSL metadata rows recorded never quoted"
---

# Vault/Privilege-Escalation — the hop-then-reach playbook set

One vault, five lanes, per the build order: the class's money in this corpus is **what the hop reaches**, and the corpus prices it coherently — $100–$1,000 for a claimed subdomain, $250 flat for a writable load path, $2,500 for a cluster token, $10,000–$12,000 for a second door or a template copy, $0-in-record for everything the hunter merely asserts. The five modules are ordered by the hop's distance: DNS claim → application role hop → local service hop → orchestration hop → adjacent (sandbox/token) hops.

## Scoreboard (172 rows · 72 paid · $106,265 · max $12,000)

| Module | Rows | Paid | Bounty | Crown |
|---|---|---|---|---|
| 01 Subdomain-Dangling-Takeover | 24 | 4 | $1,400 | PRIV-779442 ($1,000) |
| 02 Broken-Access-Control-Staff-GraphQL | 71 | 23 | $35,970 | PRIV-689314 ($12,000) |
| 03 Local-Privilege-Escalation | 29 | 17 | $7,050 | PRIV-520903 ($1,500) |
| 04 Container-Kernel-Escape | 9 | 6 | $10,600 | PRIV-1382919 / PRIV-1842829 ($2,500 ×2) |
| 05 Adjacent-Merges | 39 | 22 | $51,245 | PRIV-852613 and PRIV-1168765 ($10,000 ×2) |
| **Vault total (148 bucket + 24 merges)** | **172** | **72** | **$106,265** | **PRIV-689314 ($12,000), PRIV-418767 ($10,000)** |

Bucket $94,075/62 + merges $12,190/10. Corpus program mix (top): shopify 31 · acronis 24 · ibb 14 · security 13 · gitlab 9.

## Vault map

| # | File | What it gives you |
|---|---|---|
| 1 | [`PRIV-Testing-Agent-Playbook.md`](PRIV-Testing-Agent-Playbook.md) | **The executable protocol.** P0 program/policy read → P1 surface inventory (role × endpoint matrix, alternate doors, service × load-path matrix, job-output × snippet inventory, dangling-record inventory) → P2 probe protocol (role-replay → deactivation probe → OTP re-binding → alternate-door → load-path canary → copy-path canary → dangling claim) → P3 proof ladder → P4 modern hardening fingerprints → P5 kill-gates. |
| 2 | [`01_Subdomain-Dangling-Takeover.md`](01_Subdomain-Dangling-Takeover.md) | Claimable DNS: S3 bucket re-registration, CloudFront origin claims, Webflow/Fastly claims, vendor claim-API bugs. Anchors: PRIV-779442 (lyst S3, $1,000), PRIV-716677 (Fastly CSP claim, $200), PRIV-202767 (UnbouncePages claim-any, ×4). |
| 3 | [`02_Broken-Access-Control-Staff-GraphQL.md`](02_Broken-Access-Control-Staff-GraphQL.md) | The vault's doctrinal center (71 rows / $35,970): group-check bypasses, 2FA second-door, OTP re-binding, staff mutations, deactivated accounts. Anchors: PRIV-689314 (GitLab template copy, $12,000 — the corpus crown), PRIV-418767 (embedded-submission 2FA bypass, $10,000), PRIV-1330529 (OTP swap, $3,250), PRIV-1245736 (Stocky admin, $1,600). |
| 4 | [`03_Local-Privilege-Escalation.md`](03_Local-Privilege-Escalation.md) | DLL search order, insecure install, kernel & installer bugs. Anchors: PRIV-520903 (Apache CVE-2019-0211, $1,500), PRIV-530292 (VeraCrypt UAC bypass, $1,250), PRIV-1010340 (eBPF CVE-2020-27194, $750), the Acronis $250 flat-rate genome (14 rows). |
| 5 | [`04_Container-Kernel-Escape.md`](04_Container-Kernel-Escape.md) | Worker escapes, ingress injection, runner policy, runc. Anchors: PRIV-1382919 (ingress SA token, $2,500), PRIV-694181/697055 (LGTM symlinks, $2,000 ×2), PRIV-692603 (prepare-step root, $1,500). |
| 6 | [`05_Adjacent-Merges.md`](05_Adjacent-Merges.md) | The last module: 15 classified-adjacent + 24 unclassified merges. Sandbox/RCE rows (Kibana $10,000 ×2 + $5,000; Electron $2,550; Node $2,540), the Shopify takeover family (confirm-any-email → SSO merge), and five GHSL query rows ($5,100, metadata-only). The merge rows are module-02 continuations. |

## References (provenance layer)

| File | Contents |
|---|---|
| [`references/source-index.md`](references/source-index.md) | Roster provenance (h1-brain DB, sha256, 3,673 rows, funnel to 148 bucket + 24 merges), classification funnel, bounty accounting, era discipline, 5 limitations. |
| [`references/case-register.md`](references/case-register.md) | Row-per-row ledger of all 172 rows: case ID, team, bounty, module, source (bucket/merge), evidence (full/metadata), DB weakness, asset, CVEs, title. |
| [`references/archive/PRIV-bodies-full-dump.txt`](references/archive/PRIV-bodies-full-dump.txt) | All 172 report bodies, verbatim dump (anchor for every quote). |
| [`references/archive/classes.json`](references/archive/classes.json) | The frozen 172-row module assignment (bodies-win classification). |

## How this vault was built (method)

1. **Roster**: h1-brain DB (3,673 rows, sha256 `8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4`) → `classified.json` bucket `priv-esc` (**148 rows**: 126 `Privilege Escalation` + 22 `Improper Authorization`) + `module_map_all.json` merges (`_adjacent_unclassified`, **24 rows** from the `unclassified` pool, `weakness_name = None`) → **172 rows**.
2. **Reading**: all 167 full bodies read end-to-end (5 GHSL rows are 54-byte metadata-only); every class decided by bodies, not titles. The 15 classified-adjacent rows are RCE/prototype-pollution/sandbox/token-theft by body despite their tags — kept adjacent rather than re-sorted, with module 05 labeled as the last module.
3. **Bounty accounting**: DB `bounty_amount` where present ($106,265 across 72 rows); `None` recorded as `-` (100 rows). Per-row `weakness_name / asset_identifier / asset_type / cve_ids / bounty_amount` pulled from the DB (see register Source/Evidence columns).
4. **Modules**: five class modules, each with verbatim evidence, case-stock tables with labeled bounties, what-pays/what-doesn't sections (§6), and cross-references (§7). Adjacent pools merged into the last module (39 rows).
5. **Quote audit (zero-miss gate)**: every blockquote across the README, playbook, and five modules mechanically checked against `references/archive/PRIV-bodies-full-dump.txt` — byte-exact (see verification note in `references/source-index.md` §2 and the build verification report).

## Cross-vault links

- `../IDOR/` — module 02's object-binding rows (PRIV-1330529 OTP `resId` swap, PRIV-153905 share IDOR, PRIV-181748 comment edit) are IDOR-vault object-reference bugs; cross-cite. Module 02's role-matrix sweep is the staff-side of the IDOR vault's object-reference modules.
- `../Authentication-Session/` — PRIV-418767 (2FA second-door, $10,000) and PRIV-1050244 (2FA enforcement bypass, $750) belong to its MFA-bypass module; PRIV-791775/796956 (confirm-any-email → SSO takeover) are its email-verification module.
- `../Race-Conditions/` — PRIV-578119 (logrotate race) and PRIV-1251464 (app-verification race) are check-use races in this vault's local-file-system slice; PRIV-1092859's dangling-NS takeover feeds SSRF-vault internal-network play.
- `../Subdomain-Takeover/` (upcoming) — module 01 is its priv-esc slice; PRIV-716677's CSP-whitelisted Fastly claim is the XSS vault's trusted-host precondition.
- `../Prototype-Pollution/` — PRIV-852613/861744 (Kibana `_.set` / SIEM pollution) are its pollution-taxonomy rows; this vault keeps them adjacent for the priv-esc framing.
- `../RCE/` — PRIV-495495 (runc), PRIV-852613 and PRIV-1168765 (Kibana RCE/hazard) are its endgame siblings; cross-cite for payload formatting.
- `../GraphQL/` — PRIV-792927 (ReportInvitation email leak), PRIV-860348 (POS GraphQL staff delete), PRIV-867513 (POS GraphQL email update) are its authorization lane.

## Coverage vs limitations

**Covered**: dangling-record takeover across S3/CloudFront/Webflow/Fastly + vendor claim APIs; broken access control across staff matrices, GraphQL mutations, deactivated/removed states, OTP/identifier binding, and second-door policy bypasses; local privilege escalation across DLL search order, insecure install/folder ACLs, UAC trust, kernel memory bugs, and logrotate races; container/kernel escape across worker symlink copies, prepare-step package installs, ingress path/snippet injection, runner Docker-socket policy, and runc; the adjacent sandbox/token/RCE merges and the shopify takeover continuations.

**Honest limitations**:
1. **Count basis differs from the master list.** Master row 17 cites "460" H1-disclosed counts from other sources; this vault quotes only the h1-brain DB subset (148 bucket + 24 merges). A v2 sweep of the remaining ~444-row unclassified pool may add cases.
2. **Weakness labels are historical triage artifacts** — the same class appears as `Privilege Escalation`, `Improper Authorization`, or `None` (merges). The adjacent classified pool (15 rows) is labelled priv-esc but contains RCE, prototype pollution, sandbox bypass, and token theft. Bodies are the class authority.
3. **Bounty `None` ≠ unpaid.** It means the DB row has no figure. 100 of 172 rows carry no figure; $106,265 is a corpus floor, not a total. The corpus's true ceiling is unknowable from this slice (e.g., PRIV-1249583's full token-theft walkthrough carries no figure).
4. **Five GHSL rows are metadata-only** (PRIV-891268/929288/1483919/1587150/1602234) — one-line bodies carrying $5,100 of real query-row payouts but no quotable technique. Recorded as corpus, never quoted.
5. **Chainpay vs pure hop**: the two largest rows ($12,000 template copy, $10,000 2FA second-door) and the ingress-token row ($2,500) pay because the hop feeds another bug (private-code exfiltration, policy enforcement, cluster secrets). Pure-hop micro-rows top out at $500–$650 (module 02 staff rows) and $250 (module 03 flat rate).
6. **Era honesty** — tool choices are historical evidence (Burp Intruder, curl replays, manual Lua snippets); modern hardening is fingerprinted in playbook P4 and labeled as outside the corpus.
7. **QA**: all block quotes in modules, playbook, and this README were byte-verified against `references/archive/PRIV-bodies-full-dump.txt`; `(sic)` marks author typos. No invented quotes, no paraphrase passing as quotation.

## The one-paragraph doctrine of this corpus

Privilege escalation in this corpus is priced by **what the hop reaches, not how it fires**: a claimed subdomain paid $100–$1,000; a writable load path paid $250 flat; a worker symlink paid $2,000 for a host file read; an ingress path paid $2,500 for a cluster token; a template copy paid $12,000 for private repositories; a second door paid $10,000 for defeating declared policy; a Kubernetes sandbox break paid $10,000 for RCE-in-container even with the last mile honestly unfinished; and the GHSL query rows paid $1,800 for a one-line tooling contribution. The finds that converted class-knowledge into money are tiny and testable (one role-replay, one `resId` swap, one `ln -s`, one embedded URL, one `copytruncate` race), the honest boundaries ("the descendant check blocks group namespaces; the User path is the finding") were priced rather than punished, and every class boundary dispute in the register — authorization-vs-OTP, priv-esc-vs-RCE, bucket-vs-merge — was settled by reading the body, never the title.


<!-- CASESTOCK-LINK:BEGIN -->

## Case stock — vault (`_VAULT/`)

**1,336 disclosed reports** routed to this category · 342 with a bounty figure · **$518,575** · 828 full write-ups stored locally.

- Full list: [`_VAULT/by-vault-category/17_Privilege-Escalation.md`](../_VAULT/by-vault-category/17_Privilege-Escalation.md)
- Query: `sqlite3 ../_VAULT/reports.sqlite "SELECT id,bounty,title FROM reports WHERE ..."`
- Pull one write-up: `python3 ../_VAULT/scripts/extract_report.py <id>`

| Top paid | Program | Bounty |
|---|---|---|
| [2293343](https://hackerone.com/reports/2293343) Account Takeover via Password Reset without user interactions | GitLab | $35,000 |
| [1685822](https://hackerone.com/reports/1685822) RepositoryPipeline allows importing of local git repos | GitLab | $22,300 |
| [2281075](https://hackerone.com/reports/2281075) access list owner can escalate his role to the highest roles | Teleport | $21,000 |
| [391217](https://hackerone.com/reports/391217) Getting all the CD keys of any game | Valve | $20,000 |
| [1379975](https://hackerone.com/reports/1379975) bd-j exploit chain | PlayStation | $20,000 |

_refreshed 2026-11-17 from the public HackerOne disclosed-report dataset_
<!-- CASESTOCK-LINK:END -->
