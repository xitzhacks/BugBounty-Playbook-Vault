---
title: "Memory-corruption vault module — adjacent & unclassified pools (last module)"
type: playbook
category: memory-corruption
cwe: "CWE-707"
source_count: 24
full_bodies_available: "14/24"
corpus: "h1-brain disclosed_reports.db (sha256 8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4) — 352-row vault; 336-row memory-corruption bucket + 16 unclassified merges"
list_accessed: "2026-11-07"
note: "MEM module 6/6 (last). 8 bucket-adjacent rows (1 paid $1,000) + 16 unclassified merges (10 GitHub-Security-Lab CodeQL-query rows $500–$4,500, 5 ibb upstream-link rows, 1 mruby UAF). The vault's negative space: disclosures, leaks, metadata, jokes."
---

# Adjacent & Unclassified

## 1. Overview

Twenty-four rows: 8 bucket-adjacent + 16 merges from the classifier's `unclassified` pool. The mercantile total ($18,000: $1,000 bucket-paid + $17,000 merge-paid) is almost entirely **CodeQL query reports** — GitHub Security Lab rows whose bodies are *"This bug was reported directly to GitHub Security Lab."* This module is the vault's negative space: its job is to *stop* the other five modules' doctrines from over-generalizing — leak vs corruption, query vs bug, joke vs finding.

**Case-stock (24 rows / $18,000):**

| Case | Target | Mechanism | Bounty |
|---|---|---|---|
| [MEM-1378946](https://hackerone.com/reports/1378946) | github-security-lab | [cpp] CWE-787: query to detect unsigned integer to signed integer conversions used in pointer arithmetics | $4,500 |
| [MEM-192896](https://hackerone.com/reports/192896) | shopify-scripts | Memory disclosure in timegm | $1,000 |
| [MEM-974370](https://hackerone.com/reports/974370) | github-security-lab | [CATENACYBER]: [CPP] CWE-476 Null Pointer Dereference : Another query to either missing or redundant NULL check | $1,800 |
| [MEM-1065401](https://hackerone.com/reports/1065401) | github-security-lab | CPP: CWE-191 into experimental this reveals a dangerous comparison | $1,800 |
| [MEM-1093242](https://hackerone.com/reports/1093242) | github-security-lab | ihsinme: CPP Add query for CWE-401 memory leak on unsuccessful call to realloc function | $1,800 |
| [MEM-1114027](https://hackerone.com/reports/1114027) | github-security-lab | ihsinme: CPP add query for CWE-788 Access of memory location after the end of a buffer using strncat. | $1,800 |
| [MEM-1219491](https://hackerone.com/reports/1219491) | github-security-lab | ihsinme:CPP Add query for CWE-415 Double Free | $1,800 |
| [MEM-1122664](https://hackerone.com/reports/1122664) | github-security-lab | ihsinme: CPP add query for CWE-788 Access of memory location after the end of a buffer using strlen. | $1,000 |
| [MEM-1738939](https://hackerone.com/reports/1738939) | github-security-lab | [CPP]: Add query for CWE-125 Out-of-bounds Read with different interpretation of the string when use mbtowc | $1,000 |
| [MEM-1950659](https://hackerone.com/reports/1950659) | github-security-lab | CPP: Add query for CWE-369: Divide By Zero. | $1,000 |
| [MEM-1564100](https://hackerone.com/reports/1564100) | github-security-lab | [CPP]: Add query for CWE-190: Integer Overflow or Wraparound when using transform after operation | $500 |
| [MEM-181319](https://hackerone.com/reports/181319) | shopify-scripts | Memory disclosure in mruby String#lines method | - |
| [MEM-203595](https://hackerone.com/reports/203595) | shopify-scripts | forgot to add the patch | - |
| [MEM-380102](https://hackerone.com/reports/380102) | nextcloud | Missing memory corruption protection on Windows release built | - |
| [MEM-484930](https://hackerone.com/reports/484930) | putty_h1c | puttygen: 160MB memory leak while trying to extract openssh public key from crafted key file | - |
| [MEM-503821](https://hackerone.com/reports/503821) | putty_h1c | Assertion `col >= 0 && col < line->cols' failed, process aborted while streaming ouput from remote server | - |
| [MEM-1217702](https://hackerone.com/reports/1217702) | h1-ctf | Adam and the  Deadly  Injections | - |
| [MEM-2779070](https://hackerone.com/reports/2779070) | hyperledger | Memory Leak in bytes_to_hexstring Function | - |
| [MEM-140865](https://hackerone.com/reports/140865) | ibb | Integer Overflow in php_html_entities() | - |
| [MEM-159686](https://hackerone.com/reports/159686) | ibb | integer overflow in the _csv module's join_append_data function | - |
| [MEM-159687](https://hackerone.com/reports/159687) | ibb | integer overflow in binascii.b2a_qp | - |
| [MEM-159696](https://hackerone.com/reports/159696) | ibb | Two vulnerabilities in the ssl module | - |
| [MEM-163087](https://hackerone.com/reports/163087) | ibb | use of uninitialized variables in operator.methodcaller | - |
| [MEM-216700](https://hackerone.com/reports/216700) | shopify-scripts | heap use-after-free in mrb_vm_exec() | - |

## 2. The GHSL CodeQL-query economy ($17,000/10)

Ten rows whose bodies are the one-liner:

> This bug was reported directly to GitHub Security Lab.

The titling pattern is `Add query for CWE-<n>` — these are *CodeQL detections authored*, not found vulnerabilities: query-design reports priced at $500–$4,500 (the CWE-787 integer-conversion query at **$4,500** is the pool's ceiling). The vocabulary is the bounty claim: CWE numbers 476 (null check), 191 (underflow), 401 (realloc leak), 788 (end-of-buffer), 415 (double free), 190 (wraparound), 125 (OOB read), 369 (divide by zero) — a taxonomy, not a find. Doctrine: when a program pays for *queries*, the deliverable is pattern coverage across many codebases; the vault keeps these rows labeled as their own economy so they are never mistaken for a memory-safety bug. Every downstream statistic that quotes "145 paid rows" is including them; label before you cite.

## 3. Disclosures that arm the next bug (181319 / 192896)

Two mruby *memory-disclosure* rows — class-adjacent because they are the leak leg of the sandbox hunt:

> while reviewing mruby for vulnerabilities, I stumble onto a case that allow an attacker to leak heap content including pointer that can be used along another vulnerability to craft a complete exploit.

> An attacker may disclose memory or/and crash mirb.

MEM-192896 (**$1,000**) is the `timegm` case — `tm_mon` attacker-controlled past an index the table assumes is 11 — with a heap-address hexline string as the receipt. MEM-181319 (`-`) is the `String#lines` cached-pointer case. Both bodies say explicitly that the disclosure *arms the next bug* (pointer leak → crafted exploit) — the Info-Disclosure vault's business logic operating inside a memory-corruption corpus. The paid one ($1,000) is the one with a working PoC of the *leaked pointer itself*; the unpaid one describes a leak *format*. Small difference, whole tier.

## 4. The leak & hardening & joke tail

- **Leaks** (MEM-484930, MEM-2779070; `-`): an ASan 160MB puttygen leak and a C `bytes_to_hexstring` `malloc`-without-free leak. Bodies, frankly, read as informational review commentary:
  > puttygen does not sufficiently track and release allocated memory after it has been used, which slowly consumes remaining memory.
- **Hardening** (MEM-380102; `-`): security *posture* — missing ASLR/DEP. Genuinely important, not a corruption primitive: the RCE vault's module 05 lesson (user-agent-trusted state) with the hardening angle.
- **Metadata** (MEM-203595; `-`) — the sandbox's mailing-list tail:
  > The patch of the report https://hackerone.com/reports/192896 you forgot to add here https://github.com/Shopify/mruby-engine
- **Noise** (MEM-1217702; `-`, h1-ctf): a flagged-entry joke row (`Hi team adding the flag here`). Intellectually honest: the classifier kept it in the merge; this module is where junk goes to be *labeled* junk, not where reports go to die.

## 5. The unpaid merges that belong to modules 01–05

Five ibb rows from the unclassified pool (140865, 159686, 159687, 159696, 163087) — all unpaid, all upstream-link-threaded Python/PHP integer-overflow reports (PSRT mail, bugs.python.org) — plus MEM-216700, the mruby `mrb_vm_exec` UAF:

> The code bellow triggers a heap use-after-free vulnerability:

(sic.) Doctrine: these five-plus-one were *nearly* promoted by a v2 sweep into their home modules — MEM-140865's body is the (size_t → signed int) narrowing exemplar for module 04 — but until that sweep exists they live here, labeled. No invented promotion: the frozen `classes.json` carries them as Adjacent, and the register's merge table shows the provenance disjointly.

## 6. What pays / what doesn't

- **Pays**: CodeQL query reports ($500–$4,500 — detector authorship economics); the mruby pointer-leak PoC ($1,000). **Nothing in this module pays as a memory-corruption bug.** Both paid pools are detector/metadata payments.
- **Doesn't pay**: the hardening request, the two leaks, the patch-mail row, the CTF joke. All `-`, all better filed as Information-Disclosure/DoS/Misconfiguration canon — the Information-Disclosure vault should link to §4's leak pair as a "leak-in-C" bridge.
- **Moral for triage**: if your report is a query (CodeQL/Semgrep pattern), file it into detector programs; if it's a hardening checklist, keep it below memory-corruption severity; if it's a joke, this module's §4 is its honest shelf.

## 7. Cross-references

- **Information-Disclosure vault** — MEM-181319/192896 are its in-memory cousin; MEM-484930/2779070 (leaks) are its mirror.
- **Cryptography vault** — MEM-159696 (`Two vulnerabilities in the ssl module`, `-`) and the GHSL query rows share the language-security tracking; the query economy's CWE list is a bridge to crypto's CWE-190/369.
- **DoS vault** — the leak pair (§4) is its long-tail; resource-exhaustion-by-leak is the DoS class wearing memory titles.
- **Module 02 (UAF)** — MEM-216700 is §5's mruby stub; promote it there if a v2 sweep fires.
- **Module 04 (overflow)** — MEM-140865/159686/159687 are §5's resurrection candidates; promotion requires the bodies-wins reclass this build did not perform.
