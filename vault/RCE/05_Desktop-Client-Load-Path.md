---
title: "Desktop-client load-path code injection — plugin hijacks, OpenSSL config hijack, save-file confusion"
type: playbook
category: desktop-loadpath
cwe: "CWE-427"
source_count: 3
full_bodies_available: 3
corpus: "h1.security.nathan.sx roster (150 rows), bodies via hackerone.com/reports/<id>.json"
list_accessed: "2026-11-04"
note: "Anchors: RCE-162955 (Slack OpenSSL config, resolved), RCE-155657 (ownCloud QT plugin). Claims trace to bodies read 2026-11-04."
---

# Desktop-client load-path code injection

## 1. Overview

Three rows, **$850/2 paid** — the smallest module, and the only one whose flaws execute on
*other users' machines* without a server being reachable. The shared mechanism: an
application loads code or system-trust material from a location an unprivileged local user
can plant files into. All three rows carry the same prerequisite honestly stated in body:
**any authenticated local user**, and the same delivery framing ("leads to Privilege
Escalation" in the Slack title).

**Case-stock (3 rows / $850):**

| Case | Target | Mechanism | Bounty |
|---|---|---|---|
| [RCE-162955](https://hackerone.com/reports/162955) | Slack | `openssl.cnf` expected at `C:\usr\local\ssl` is plantable → arbitrary code in other users' process | $750 (list) |
| [RCE-155657](https://hackerone.com/reports/155657) | ownCloud | QT plugin directory on `C:` stem plantable → arbitrary code injection | $100 (list) |
| [RCE-188078](https://hackerone.com/reports/188078) | Brave | save-page `.bat` on TLD → command execution (duplicate) | - |

## 2. The Slack OpenSSL row: the trust file nobody owns

RCE-162955 (weakness tag: Command Injection - Generic — mislabel; body is load-path code
injection) is the era's canonical Windows load-path bug, reported by the same hunter as
the ownCloud row:

> The issue is that slack.exe tries to load its OpenSSL configuration from the
> non-existing file C:\usr\local\ssl\openssl.cnf (See Procmon screenshot). As any
> authenticated Windows user is allowed to create new folders at the system drive's root,
> the expected folder structure can be created by anyone.

> This enables any local user to create the expected OpenSSL config file. Using this
> config file it is then possible to instruct OpenSSL to load additional libraries. This
> finally leads to arbitrary code execution in other user's slack.exe process.

The Procmon methodology (watch what the client opens and *fails* to find, then check who
can create that path) is the module's transferable skill. The title's own claim — "leads
to Privilege Escalation" — is the honest framing: the code runs as the *victim's* user,
not as SYSTEM.

## 3. The ownCloud row and the platform behavior RCE-188078

RCE-155657 (**$100 (list)**) plants a QT plugin (search-path hijack, same author). RCE-188078
(Brave, duplicate) is a different family — user double-click confusion: `save page`
performs TLD-extensions into executable file types; the triage merged it, which is why it
carries no bounty line. Its body walks a chain of severity arguments ("user must
double-click"), the classic Windows desktop debate.

## 4. What pays, what doesn't

- $750/$100 — the era priced *other-user session* desktop code injection lower than
  server RCE by an order of magnitude. The prerequisite line ("any authenticated Windows
  user") is what keeps it paid vs the module-08 local-only debates.
- The duplicate status on 188078 is the corpus's honest negative: file-type-confusion
  rows flood the queue; a novel one must carry the load-path structure to be unique.
- Modern echo (P4): every Electron client now retires to the load-path discipline —
  `NODE_OPTIONS`, library search paths, auto-updater verification. The bibliography's
  desktop/Electron section (blogs-index §2.5c) shows the lane's modern shape.

## 5. Cross-references

- Module 06 (devops consoles) shares the "execution at a trust boundary the owner did not
  audit" framing — but its attacks are remote; this module's are local.
- The register's metadata-only habit does not appear here: all three bodies are real
  read-throughs, the smallest module in the build with zero empty bodies.
