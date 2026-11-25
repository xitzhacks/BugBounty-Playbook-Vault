---
title: "PRIV Testing Agent Playbook — the executable protocol"
type: agent-playbook
category: priv-esc-all
cwe: "CWE-732, CWE-862"
built: "2026-11-07"
corpus: "172 rows (148 priv-esc bucket + 24 unclassified merges) → 167 full bodies read + 5 GHSL metadata-only · $106,265 (bucket $94,075/62 + merges $12,190/10)"
bounty: "$106,265 roster-tagged · modules 01–05: 01 $1,400/4 · 02 $35,970/23 · 03 $7,050/17 · 04 $10,600/6 · 05 $51,245/22"
companion_modules: "01 subdomain-dangling-takeover · 02 broken-access-control-staff-graphql · 03 local-privilege-escalation · 04 container-kernel-escape · 05 adjacent-merges"
quote_rule: "byte-true, from read bodies only; GHSL metadata rows recorded never quoted"
---

# PRIV Testing Agent Playbook

Executable protocol derived from 167 read bodies (priv-esc bucket + unclassified merges) + era-honest hardening notes. Run phases in order; abort at kill-gates. Crown-jewel doctrine up front: **payouts track what the hop reaches** — module 02's GitLab template copy paid $12,000 because it import *private* repositories, the embedded-submission 2FA bypass paid $10,000 because it defeats a program's declared policy through a second door, and the ingress-nginx token theft paid $2,500 because the token lists secrets cluster-wide — while the same class unchained (a staff permission micro-bug with no privileged action, module-02's unpaid shelf) paid nothing in-record. The vault's two complete 2FA cases (418767 $10,000 at policy level, 1050244 $750 at enforcement level) teach the same lesson at different depths: a bypass that names the guard it defeats and proves the alternate channel is a finding; a bypass that asserts the guard is missing is a theory.

## P0 — Program classification & policy read (before any payload)

1. Program type: SaaS bug bounty vs VDP vs source-code program. The corpus rows are almost all `resolved`-grade (bucket 148 rows are disclosed bounty-awarded reports; merges are `unclassified` by classifier v1, included by `module_map_all.json`). Note the metadata-only rows prove the opposite lesson: five GHSL one-liners (module 05) carry $5,100 with no body — **resolution metadata carries neither bounty nor class** in either direction. Read policy for allowed actions now: the corpus's floor is the *demonstrated* action (module 02's Stocky admin creation, module 04's `/etc/passwd` read) — find your program's modern equivalent (usually "demonstrate the privileged action on your own test account; no real user's data").
2. Environment signal: classify the fleet — SaaS/staffed applications (module 02's Shopify/GitLab/Nextcloud clusters) vs end-user software with privileged services (module 03's Acronis/GlassWire cluster) vs orchestration (module 04's Kubernetes/LGTM). The environment decides which module's inventory you run first: staff matrices for SaaS, services × load paths for end-user software, job outputs × snippet annotations for orchestration.
3. Kill-gate: no testing yet — P0 produces the *policy envelope* only.

## P1 — Surface inventory (roles, endpoints, load paths, records)

1. **Role × endpoint matrix** — every role (owner / admin / staff / viewer / guest / external / read-only / deactivated / removed) × every privileged action (create/delete/update/publish/send/approve/transfer). Corpus evidence: PRIV-1245736's `POST /users/create_admin` reachable by a non-privileged Stocky user ($1,600); PRIV-1050244's 2FA enforcement bypass ($750); `DELETE /api/memberships/<membershipID>` with no role check (PRIV-810320). Include removed/deactivated states (PRIV-331223 still-notified, PRIV-175490 still-logged-in, PRIV-254588 still-creating) — revocation paths are the inventory's blind spot.
2. **Alternate doors** — every privileged flow's second channel (embedded vs main submission, REST vs GraphQL, API-key vs session). Corpus evidence: PRIV-418767's embedded-submission 2FA bypass ($10,000); PRIV-860348's GraphQL `graphql-proxy/admin` path ($500); PRIV-867513's POS GraphQL email update. If a flow has a UI guard, find the API call the UI makes and replay it without the guard.
3. **Service × load-path matrix** (module 03) — every privileged service/daemon × every file it loads (DLL by bare name, helper binary in app dir, script in PATH, MSI, updater). Corpus evidence: PRIV-921675's nine DACLs-loaded DLLs (GlassWire, $250); the Acronis search-order genome (20 rows); PRIV-908162's drag-and-drop app dir ($300).
4. **Job-output & snippet inventory** (module 04) — every worker output file the host copies, every config file the worker assembles, every snippet annotation the controller renders. Corpus evidence: PRIV-694181's `build.log` symlink ($2,000); PRIV-1249583's Lua snippets; PRIV-1417211's Docker-socket mount ($100).
5. **Dangling-record inventory** (module 01) — every CNAME/NS/CloudFront/Fastly record + provider claim endpoint. Corpus evidence: PRIV-779442's S3 bucket ($1,000); PRIV-202767's vendor-claim API (×4); PRIV-716677's CSP-whitelisted Fastly domain ($200); PRIV-1092859's dangling NS (full zone).
6. Out-list: guest-visible list endpoints without object binding are *inventory*, not targets — the target is always the privileged mutation that reuses the same identifier.

## P2 — Probe protocol (from cheapest signal to hardest)

Per candidate hop, in corpus-proven order, with pricing attached:

1. **Role-replay** — serve each endpoint as each role and diff the result. The module-02 baseline: an unprivileged user replays the admin's intercepted request (Stocky `POST /users/create_admin`, $1,600; POS staff delete over GraphQL, $500). Record the exact role, the exact endpoint, the exact response delta.
2. **Deactivation probe** — log in as a deactivated/removed/disabled account and retry the last successful action. Corpus evidence: PRIV-331223 ($500), PRIV-175490, PRIV-254588, PRIV-416983.
3. **OTP/identifier re-binding** — request the OTP for your own object, then verify it against a different object ID. Corpus evidence: PRIV-1330529's `resId` swap ($3,250). Then test the confirmation-link variant: change email, check which inbox receives the confirmation link (module 05's 791775 thread).
4. **Alternate-door probe** — reach the same privileged state through the second channel (embedded form, API key, GraphQL mutation, `act-as` header). Corpus evidence: PRIV-418767 ($10,000), PRIV-2081930, PRIV-792927.
5. **Load-path probe** (module 03) — place a canary DLL / helper / marker file in the writable path and restart the service. Observe load or execution. Corpus evidence: PRIV-921675 (nine DLL names), PRIV-945122 (symlink file creation). No payload beyond the canary.
6. **Copy-path probe** (module 04) — replace a worker output file with a symlink to a host canary path (`/tmp/canary` first, `/etc/passwd` never as first test) and observe what the host copies back. Corpus evidence: PRIV-694181/697055 ($2,000 each). Then test the snippet annotation (`server-snippet` with a canary read) on ingress controllers.
7. **Dangling-claim probe** (module 01) — register the missing bucket / claim the distribution / request the provider claim and serve a benign POC page (title + marker + your email). Corpus evidence: PRIV-779442 ($1,000), PRIV-716677 ($200). Never serve a login honeypot with real credential fields — module 01's own bodies describe it as impact, the playbook forbids it as proof.
8. Skeleton quote (module 02 — the honest self-limit): "I think it can be a Remote Code Execution vulnerability but there is a length limit" is the RCE vault's sibling; this vault's equivalent is stating the guard you could not defeat (e.g., "the descendant check blocks group namespaces; the User-namespace path is the finding" in 689314) — naming the boundary is what priced $12,000.

## P3 — Proof ladder (the modest demonstrations paid)

1. Module 02's POC ladder: as low-priv user, perform the privileged action on *your own* object (create your own admin, delete your own POS staff, copy your own template) — then, if the program allows, escalate to a second test object. Never touch a third party's data.
2. Module 04's copy-path ladder: worker canary → symlink to `/tmp/canary` → host-visible flag → then (program-permitting) `/etc/passwd` head. The $2,000 rows stop at file read; the vault never teaches beyond it.
3. Module 03's load-path ladder: canary DLL with a benign marker (file write) → service reload → marker observed. The $250 rows never need a shell.
4. Module 01's claim ladder: register → serve benign POC → screenshot the POC on the real subdomain. The $1,000 row's XSS file is the ceiling, not the floor — a static page is sufficient.
5. Sandbox-bypass rows (module 05): the Kibana hazard priced at $10,000 shows that a demonstrated engine break + honest "chain incomplete" + file write inside the sandboxed process is the era's best bundle. Modern programs price a sandbox escape the same way.

## P4 — Modern hardening fingerprints (never corpus doctrine)

The corpus maps to these modern *expectations*; a corpus-identical trigger on a modern stack usually means the hardening is absent:

- **SaaS authorization**: server-side permission checks on every mutation (not UI-gated); GraphQL field-level checks; per-role API gateway (module 02's Stocky/POS rows are the before-state); deactivation that revokes sessions *and* subscriptions.
- **Identity binding**: OTP bound to the object it was issued for; email-confirmation links bound to the new address; invite links single-use and activation-scoped (module 05's wholesale rows are the before-state); 2FA enforced on every auth path including embedded/API channels.
- **Local software**: safe DLL search mode + fully-qualified load paths; installer ACLs (module 03's drag-and-drop row is the before-state); world-writable service units forbidden; UAC-elevated `ShellExecute` replaced by `Explorer`.
- **Orchestration**: ingress `path`/`snippet` annotations allowlisted (Lua snippets restricted or disabled); worker output copies that refuse symlinks (`O_NOFOLLOW` / `COPY --no-dereference`); Docker-socket mounts flagged as root-equivalent in docs (module 04's $100 row is the before-state); EndpointSlice validation strict.
- **DNS**: dangling-record monitoring and automatic removal; provider claim endpoints that verify DNS ownership (module 01's vendor-API rows are the before-state); CSPs that never whitelist claimable third-party domains.

## P5 — Pre-report gates (kill-gates)

1. **Class gate** — you can name the hop (low-priv role → privileged action / container → host / service → root / dangling → claimed) and its boundary. A claim that never performs the action — a bare permission-matrix assertion — dies here (module 02's unpaid shelf).
2. **Identity gate** — you demonstrated *the action*, not the theory: a created admin login, a copied file, a served POC, a token decode. Title-only rows (module 05's five GHSL one-liners, carrying $5,100) get *attributed* to their modules in the register but are never cited as proof in any report you write — their lesson is pricing only.
3. **Boundary gate** — state what you could not reach. The namespace-guard bypass in 689314 is a *finding because the group path is guarded and the user path is not* — cite both paths. Claims of "maybe" die here.
4. **Version/patch gate** — outdated-CVE claims need your own demo or die. The corpus's CVE rows (module 03's Apache/eBPF, module 04's runc) all carry working demonstrations; a version string alone is not a finding.
5. **Prereq gate** — state what auth context the finding needs: the staff rows that need an existing low-priv account (1245736), the ingress rows that need `create ingress` permission (1382919), the local rows that need an authenticated local user (921675). Unstated prerequisites die at triage.
6. **Noise gate** — the "it's not priv-esc"-check against module 01's wireframe row (1570591: one domain, one link, one impact line, no figure) and module 02's disclosure-grade IDORs (93020, 181748). Served POC or demonstrated action, or it is a TODO comment, not a report.

## Module ↔ phase table

| Phase | Corpus evidence (modules) | Anatomy of the paid pattern |
|---|---|---|
| P1 inventories roles × endpoints | 02 (§2-§5) | role-replay + alternate doors |
| P1 inventories load paths | 03 (§2-§4) | service × DLL/helper × writable path |
| P1 inventories job outputs & snippets | 04 (§2-§4) | build.log symlink; ingress Lua |
| P1 inventories dangling records | 01 (§2-§5) | S3/CloudFront/Fastly + claim APIs |
| P2 probes binding + doors | 02 §4, 05 §4 | OTP resId swap; embedded door |
| P2 probes copy paths | 04 §3-§4 | canary symlink → flag |
| P2 probes load paths | 03 §2-§3 | canary DLL → marker |
| P3 proofs ladder, honest boundaries | 01 §6, 02 §6, 04 §6 | served POC; copied repo; token decode |
| P4 hardening fingerprints | 02 §6, 03 §6, 04 §6, 05 §6 | server-side checks; safe load; nofollow |
| P5 kill-gates | 01 §6, 05 §4 | wireframe/GHSL exhibits |

## Non-goals

- Full account-takeover chains beyond the corpus's email-confirmation family: the merge rows (791775/796956/867513) demonstrate takeover via confirmation-link and SSO-merge bugs; general ATO orchestration is the Authentication-Session vault's doctrine.
- Memory-corruption exploitation beyond the corpus's kernel rows: eBPF verifier and dirty_sock are price anchors, not exploitation guides; heap feng shui is outside every module's claims.
- DNS-zone-restoration beyond dangling records: PRIV-1092859's full-zone NS takeover is the apex; broader zone-hijack technique is out of this vault's corpus.
