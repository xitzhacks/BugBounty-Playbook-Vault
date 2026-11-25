---
title: "Server-side template injection & app-execution primitives — Jinja2, Smarty, Liquid, Rails render paths, Web Console"
type: playbook
category: ssti-app-primitives
cwe: "CWE-1336"
source_count: 6
full_bodies_available: 4
corpus: "h1.security.nathan.sx roster (150 rows), bodies via hackerone.com/reports/<id>.json"
list_accessed: "2026-11-04"
note: "Anchors: RCE-125980 (Uber Jinja2, $10,000 json — the corpus SSTI crown), RCE-164224 (Smarty {php}), RCE-98259 (Shopify Liquid $1,500 json). Claims trace to bodies read 2026-11-04."
---

# Server-side template injection & app-execution primitives

## 1. Overview

Six rows, **$14,400/6 paid — every row in this module carries a bounty**, the highest
paid-rate of any module (6/6). Two lanes share it: (1) template engines executing attacker
expressions (Jinja2, Smarty, Liquid), and (2) Rails/Rack app primitives that eval app code
(`render :inline`, dynamic render paths, Web Console). The corpus pattern is identical in
both lanes: an attacker-controlled *expression* reaches an engine that evaluates it — the
filter not being the engine's job, and the engine not being written as a sandbox.

**Case-stock (6 rows / $14,400):**

| Case | Target | Mechanism | Bounty |
|---|---|---|---|
| [RCE-125980](https://hackerone.com/reports/125980) | Uber | Jinja2 SSTI via profile name → email render | $10,000 (json) |
| [RCE-44513](https://hackerone.com/reports/44513) | Rails (VDP) | Web Console IP whitelist bypass via XFF parser differential | $500 (list) |
| [RCE-113928](https://hackerone.com/reports/113928) | (program in register) | `render :inline` RCE — metadata-only | $1,500 (json) |
| [RCE-98259](https://hackerone.com/reports/98259) | Shopify | Liquid "Limited RCE" — no-args boundary | $1,500 (json) |
| [RCE-46019](https://hackerone.com/reports/46019) | rails | dynamic render path + dir traversal | $500 (json), sev high |
| [RCE-164224](https://hackerone.com/reports/164224) | unikrn | Smarty `{php}` block → `file_get_contents(/etc/passwd)` | $400 (list) |

## 2. The Uber Jinja2 row: how a ten-thousand-dollar SSTI was written

RCE-125980 (**$10,000 (json)**, weakness Code Injection) is the corpus's model SSTI report.
The discovery trigger is a math probe in a profile field, witnessed in email rendering:

> First, if you change your profile name to {{ '7'*7 }}, and you will receive a mail
> "Your Uber account information has been updated" sent by [REDACTED_EMAIL]
>
> And in mail body, you can see your name become '7777777'

Then the escalation material, quoted verbatim because it is the standard Jinja2 ladder:

> {{ '7'*7 }}
> {{ [].__class__.__base__.__subclasses__() }} # get all classes
> {{''.__class__.mro()[1].__subclasses__()}}
> {%for c in [1,2,3] %}{{c,c,c}}{% endfor %}

The report is honest about its own boundary:

> I think it can be a Remote Code Execution vulnerability but there is a length limit :(
> But I still can "write" some Python code in "name" filed, there are more examples in
> attachments and bellow are my payloads

(sic) "filed"/"bellow" in the original. The **length limit** is named as the blocker —
the payload channel truncates the full gadget chain. The bounty paid **$10,000** for
demonstrated expression evaluation into an email-render path; the sandbox-escape-to-full-
RCE completion never needed to be shown. Discipline: the report proved the *class*
(engine evaluates attacker expressions) and priced the reach.

## 3. Smarty: `{php}` tags are exec primitives

RCE-164224 walks the same ladder in a different engine — probe, fingerprint, primitive,
file read:

> To start, I began with the payload {7*7} and received a template error in the email I received {F115749}
> Recognizing the injection, I then was able to confirm the version of smarty used via {$smarty.version} {F115750}
> Next I was able to test {php} tags by using ```{php}print "Hello"{/php}``` {F115751}. Finally I used file_get_contents to begin extracting the
> etc/pass file ```{php}$s = file_get_contents('/etc/passwd',NULL, NULL, 0, 100); var_dump($s);{/php}``` {F115752} …

> Since the {php} tags are being parsed and executed, we can execute php functions. In this
> case, you'll see I'm able to extract the etc/passwd file. While I haven't tried, an
> attacker can more than likely create a shell on the server.

(sic) "/etc/pass file". The trigger chain is worth teaching: profile fields → an *invite
email* render. The user-facing form was accepted; another user's invitation was the render
that fired the payload. Resolved at **$400 (list)** — the corpus prices Smarty-era `{php}` well below Uber's Jinja2 $10k: **a paid rate follows the target's recognizable
reach, not the engine's fame**.

## 4. Liquid: the sandbox that names its own limits

RCE-98259 (**$1,500 (json)**), titled "Limited RCE" — the corpus's rare *defensive-grade*
row: Shopify's Liquid restricts the template's calls; the report documents the boundary at
which execution still happens (no-args calls). It's the honest counter-example to the
"template injection always means RCE" folklore: Liquid's design proves expression
evaluation can be bound, and the $1,500 paid for the bound-but-real execution.

## 5. Rails primitives: render paths and the Web Console

**RCE-113928** (`render :inline`, **$1,500 (json)**; team `rails`) and **RCE-46019** (dynamic render
path + dir traversal, **$500 (json)**, high) are metadata-only rows (bodies absent;
source-index §7): title + severity + json bounty only. Both are the Rails render-lane
shelves — `render :inline` executing user text as ERB, and attacker-influenced template
path selection ([Dynamic render path] in the title) reaching file-system effects. No
quotes exist for them; nothing is invented.

**RCE-44513** (Rails VDP row, unresolved-to-team) is the dev-console lane anchor — the
Web Console's IP whitelist defeated by a *parser differential* between two Rails layers:

> This is due to the fact that Web Console parses the `request.remote_ip` to check if the
> IP is whitelisted with the Ruby class `IPAddr`. The Rails stack prior to 4.2 when
> calculating `request.remote_ip` uses [these regular expressions](https://github.com/rails/rails/blob/4-1-stable/actionpack/lib/action_dispatch/middleware/remote_ip.rb#L31-38) to strip out trusted
> Proxies from the HTTP Headers `X-Forwarded-For` and `Client-IP`.

> `X-Forwarded-For: 0000::1`

> As the Web Console is *intended* for debugging in the Development Environment this will
> most likely not affect Production setups, unless Web Console is explicitly enabled. But
> gaining RCE on Developer laptops might be fun as well ;).

The message: an *eval interface* (arbitrary Ruby statements by the product's own docs) is
an RCE primitive whose gate is set by a different class of bug (header parsing). The
modern hardening (P4): Web Console-gating by explicit middleware, console disabled
outside dev — but the "eval interface behind a config gate" pattern recurs in every era
(Client-side equivalent: RCE-217790's twine eval primitive, module 07).

## 6. The move (module-tied)

1. Fingerprint the engine before crafting (`{$smarty.version}` in 164224; `{{7*7}}` math
   probes are era-standard but BBH §1a bakes `{{ get_user_file("/etc/passwd") }}` and
   `{${sleep(10)}}` into its command-injection payload list — the same class smudge).
2. Render sink = the *third* party's context (an email to another user in 125980/164224) —
   never trust the response of the submit path alone.
3. Name the limit you could not break (125980's length limit) — honesty priced higher than
   a fake full-RCE claim.
4. `render :inline`/dynamic-path and Web-Console rows are config-gated classes: the gate is
   the real fix (44513's proposed mitigation is literally "disallow execution of Web
   Console within Rails < 4.2").

## 7. Cross-references

- Module 01 carries Command-injection probes (`{${sleep(10)}}`) that blur into this
  module's lane — the BBH payload list puts both in one list (blogs-index §1a note).
- Module 07's RCE-217790 (twine → eval primitive → XSS) is the client-side sibling.
- Module 04's mruby engine rows (RCE-181321 family) are the server-side sibling of this
  module's sandboxed-engine framing — their sandbox breakage went $20k/$18k/$10k (module 04).
