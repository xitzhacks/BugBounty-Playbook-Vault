---
title: "Local privilege escalation — DLL search order, insecure install, kernel & installer bugs"
type: playbook
category: local-privilege-escalation
cwe: "CWE-732"
source_count: 29
full_bodies_available: 29
corpus: "h1-brain disclosed_reports.db (3,673 rows), priv-esc bucket + module_map_all.json merges"
list_accessed: "2026-11-07"
note: "Anchors: PRIV-520903 (Apache CVE-2019-0211, $1,500), PRIV-530292 (VeraCrypt UAC bypass, $1,250), PRIV-1010340 (eBPF CVE-2020-27194, $750). Acronis cluster = 20/29 rows."
---

# Local Privilege Escalation — the service that runs as someone else

## 1. Overview

Twenty-nine rows, **$7,050/17 paid** (12/29 carry no figure). Two disjoint populations share this module, and conflating them ruins both: (a) the **vendor-app cluster** — 24 rows that are variants of one root cause (a privileged service loads a writable file, executable, or DLL), concentrated on a single vendor family (acronis 20, plus glasswire, valve, nodejs, nordsecurity, gitlab); and (b) the **upstream memory/kernel cluster** — 5 rows (Apache, VeraCrypt, eBPF, Ubuntu dirty_sock, Steam driver) where the primitive is a race, UAC trust error, or kernel memory bug. The DB weakness is uniform (29/29 `Privilege Escalation`). The bibliography-grade detail of this module is that the $250 rows are flat-rated: the vendor's program pays $250 per LPE variant regardless of which sub-feature it uses, so fourteen Acronis rows at $250 are a price list, not fourteen different decisions.

**Case-stock (29 rows / $7,050):**

| Case | Target | Mechanism | Bounty |
|---|---|---|---|
| [PRIV-520903](https://hackerone.com/reports/520903) | ibb — Apache (Legacy) | www-data scoreboard bucket OOB → root fn call on graceful restart | $1,500 |
| [PRIV-530292](https://hackerone.com/reports/530292) | ibb — IBB (Legacy) | elevated ShellExecute trusts HKCU browser keys → UAC bypass | $1,250 |
| [PRIV-1010340](https://hackerone.com/reports/1010340) | ibb — IBB (Legacy) | eBPF verifier scalar32 OR bounds bug → OOB rw (CVE-2020-27194) | $750 |
| [PRIV-908162](https://hackerone.com/reports/908162) | acronis — Acronis Cyber Protect Home Office (formerly Acronis True Image) | drag-and-drop install → LaunchDaemon binaries replaceable | $300 |
| [PRIV-921675](https://hackerone.com/reports/921675) | glasswire | service loads DLLs from writable PATH → SYSTEM | $250 |
| [PRIV-924493](https://hackerone.com/reports/924493) | acronis — Acronis Cyber Protect Home Office (formerly Acronis True Image) | Sync Agent untrusted DLL search order | $250 |
| [PRIV-959017](https://hackerone.com/reports/959017) | acronis — Acronis Cyber Protect Home Office (formerly Acronis True Image) | TrueImage 2020 untrusted DLL search order → admin | $250 |
| [PRIV-966494](https://hackerone.com/reports/966494) | acronis — Acronis Cyber Protect Home Office (formerly Acronis True Image) | True Image 2021 XPC service LPE | $250 |
| [PRIV-980500](https://hackerone.com/reports/980500) | acronis — Acronis Cyber Protect Home Office (formerly Acronis True Image) | quarantine restore code execution | $250 |
| [PRIV-983363](https://hackerone.com/reports/983363) | acronis — Acronis Cyber Protect Home Office (formerly Acronis True Image) | quarantine delete LPE | $250 |
| [PRIV-996576](https://hackerone.com/reports/996576) | acronis — Acronis Cyber Protect Home Office (formerly Acronis True Image) | System Clean-up LPE | $250 |
| [PRIV-1003007](https://hackerone.com/reports/1003007) | acronis — Acronis Cyber Protect Home Office (formerly Acronis True Image) | Backup delete LPE | $250 |
| [PRIV-1004740](https://hackerone.com/reports/1004740) | acronis — Acronis Cyber Protect Home Office (formerly Acronis True Image) | Secure Zone DLL hijack | $250 |
| [PRIV-1008427](https://hackerone.com/reports/1008427) | acronis — Acronis Cyber Protect Home Office (formerly Acronis True Image) | feedback/crash-report DLL hijack | $250 |
| [PRIV-1010552](https://hackerone.com/reports/1010552) | acronis — Acronis Cyber Protect Home Office (formerly Acronis True Image) | Rescue Media Builder DLL hijack | $250 |
| [PRIV-1071832](https://hackerone.com/reports/1071832) | acronis — Acronis Cyber Protect Home Office (formerly Acronis True Image) | insecure MSI file | $250 |
| [PRIV-1075449](https://hackerone.com/reports/1075449) | acronis — Acronis Cyber Protect Home Office (formerly Acronis True Image) | update routine LPE | $250 |
| [PRIV-496285](https://hackerone.com/reports/496285) | ibb — IBB (Legacy) | kernel dirty_sock LPE | - |
| [PRIV-578119](https://hackerone.com/reports/578119) | gitlab — gitlab.com | logrotate race via git-owned logdir → root file write | - |
| [PRIV-852091](https://hackerone.com/reports/852091) | valve — steam.exe | Steam Remote Play → kernel-mode driver install | - |
| [PRIV-858598](https://hackerone.com/reports/858598) | acronis — Acronis Cyber Protect Home Office (formerly Acronis True Image) | anti_ransomware_service via quarantine | - |
| [PRIV-944735](https://hackerone.com/reports/944735) | acronis — Acronis Cyber Protect Home Office (formerly Acronis True Image) | mmsminisrv arbitrary DLL injection | - |
| [PRIV-945122](https://hackerone.com/reports/945122) | acronis — Acronis Cyber Protect Home Office (formerly Acronis True Image) | syncagentsrv symlink file creation | - |
| [PRIV-959608](https://hackerone.com/reports/959608) | acronis — Acronis Agent | systeminfo.exe DLL search-order hijack | - |
| [PRIV-959815](https://hackerone.com/reports/959815) | acronis — Acronis Agent | Managed Machine Service file/folder deletion | - |
| [PRIV-963103](https://hackerone.com/reports/963103) | acronis — Acronis Agent | tibxread.exe DLL search-order hijack | - |
| [PRIV-1211160](https://hackerone.com/reports/1211160) | nodejs — https://github.com/nodejs/node | Node installer LPE (CVE-2021-22921/29221/22117) | - |
| [PRIV-1218523](https://hackerone.com/reports/1218523) | nordsecurity — NordVPN - Linux Executable | NordVPN init/unit world-writable → root exec | - |
| [PRIV-1251464](https://hackerone.com/reports/1251464) | acronis — Acronis Cyber Protect Home Office (formerly Acronis True Image) | app-verification race LPE | - |

## 2. The Acronis $250 flat rate and the DLL-search-order genome

PRIV-921675 (glasswire, **$250**) states the class genome in its cleanest form — a privileged process loads libraries by bare name, so any writable directory on the search path is the attacker's:

> GlassWire contains a DLL hijacking vulnerability that could allow an authenticated attacker to execute arbitrary code on the targeted system.

The body then enumerates the nine DLLs the `GWCtlSrv.exe` service loads as SYSTEM (swift.dll, CSUNSAPI.dll, nfhwcrhk.dll, and six more) and the writable-PATH precondition. Every Acronis $250 row is this shape with a different feature name as the trigger surface: `mmsminisrv` arbitrary DLL injection (944735), Sync Agent search order (924493), TrueImage 2020 search order (959017), Secure Zone operations (1004740), feedback/crash-report sending (1008427), Rescue Media Builder (1010552), `systeminfo.exe` / `tibxread.exe` utility hijacks (959608/963103). The quarantine pair (980500 restore, 983363 delete, plus the no-figure 858598) and the XPC row (966494), System Clean-up (996576), Backup delete (1003007), MSI (1071832), and update routine (1075449) are the same writable-code mistake through non-DLL channels (a helper that writes to a user-writable path, an installer that drops a world-writable file, an updater that restarts a user-writable binary). PRIV-908162 (**$300** — the module's sole Acronis row above the flat rate) is the macOS variant: a drag-and-drop install leaves `/Applications/Acronis True Image.app` replaceable by any admin user, which is itself root via LaunchDaemon:

> As the installation happened with drag and drop, an admin user can replace any of the executables and achieve trivial privilege escalation to root.

The doctrine for the operator: **a privileged service + a writable load path = a $250 finding**, and a vendor that ships twenty load paths ships twenty findings. The fix is mechanical (safe DLL search mode, fully-qualified paths, correct ACLs) — which is why the program pays flat: it is buying instances, not insights.

## 3. The three upstream rows: race, UAC trust, kernel verifier

PRIV-520903 (Apache, **$1,500**, CVE-2019-0211/CVE-2019-6977) is the module's memory-corruption anchor — a low-privilege `www-data` worker corrupts a shared-memory `bucket` index so the root parent calls an attacker-chosen function on graceful restart:

> Basically, this is an arbitrary function call as root triggered whenever the server gracefully restarts, which is generally once a day.

PRIV-530292 (VeraCryptExpander, **$1,250**, CVE-2019-19501) is the UAC-trust variant — an elevated process opens a URL through `ShellExecute`, which resolves the browser handler from the user-writable `HKCU` hive:

> Your VeraCryptExpander.exe is vulnerable to a Local Privilege Escalation (UAC BYPASS) during execution.

The body pairs this with the HKCU browser-key tampering recipe and the `Explorer`-instead-of-`ShellExecute` fix. PRIV-1010340 (Linux kernel eBPF, **$750**, CVE-2020-27194) prices the kernel-verifier variant: an unprivileged BPF socket filter gets out-of-bounds read/write through the `scalar32_min_max_or` bounds-tracking bug. PRIV-496285 (Ubuntu dirty_sock) and PRIV-852091 (Steam kernel-driver install) are the no-figure remainder of this lane.

## 4. The remaining rows

No further quotes: PRIV-578119 (GitLab logrotate race through a `git`-owned log directory — root file write, no figure), PRIV-1211160 (Node installer, no figure), PRIV-1218523 (NordVPN world-writable init/unit, no figure), PRIV-945122 (syncagentsrv symlink file creation), PRIV-959815 (Managed Machine Service deletion), PRIV-1251464 (application-verification race), and the additional Acronis service rows are all tabulated above. Each body was read; none needed quoting beyond the anchors.

## 5. Cross-module notes

This module's race rows (578119 logrotate, 1251464 verification) are the local-file-system slice of the Race-Conditions vault's check-use module — same primitive, local receiver. The kernel rows (1010340 eBPF, 496285 dirty_sock, 495495 runc in module 04) belong to the Memory-Corruption vault's kernel lane and are cross-cited there.

## 6. What pays/what doesn't

- **Flat-rate economics:** Acronis at $250/variant (×14 paid rows) is the corpus's clearest pass-rate product line. The vendor buys each instance because the fix is per-path. Modern programs price this identically — writable-path LPE is a per-instance finding, not a research finding.
- **Upstream pricing:** the three memory/kernel rows ($1,500 / $1,250 / $750) pay above the flat rate because they are universal (every Apache install, every VeraCrypt user, every 5.8 kernel) rather than per-vendor.
- **$0-in-record (12 rows):** the Acronis no-figure rows (858598, 944735, 945122, 959608, 959815, 963103, 1251464) are the same class with no figure recorded — the vault does not read them as unpaid, only as figure-less. The no-figure upstream rows (496285 dirty_sock, 852091 Steam, 578119 logrotate, 1211160 Node, 1218523 NordVPN) are the honest zero-in-record tail: serious primitives on programs whose tables top out low or whose rows postdate the figure scrape.
- **Kill-gate from this module:** a DLL-hijack claim without a writable-path demonstration (the exact DLL name, the exact PATH entry, the service account, the load order) is a theory, not a finding — the $250 rows always name all four.

## 7. Cross-references

- Module 04's runc row (PRIV-495495) and module 02's logrotate-adjacent race note (578119) are the local/remote boundary of the same class.
- The Race-Conditions vault's Check-Use module owns the TOCTOU writeup; this module owns the per-vendor flat-rate context.
- The playbook (PRIV-Testing-Agent-Playbook.md) P3 inventories services × load paths × ACLs; P4 covers safe-DLL search mode and installer ACLs.
