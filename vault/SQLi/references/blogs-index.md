---
title: "Blogs and reference bibliography — sources cited inside the corpus bodies"
type: reference
category: bibliography
cached_sources: 5
unreachable_sources: 3
list_accessed: "2026-10-25"
note: "Quotes are byte-true from locally cached page copies in /tmp/opencode/sqli/blogs/ at access time. Cached-page HTML was stripped mechanically; quoted sentences are verbatim. Sources that could not be retrieved are recorded as such rather than paraphrased."
---

# Bibliography — sources the corpus bodies themselves cite

The corpus (2014–2022 reports) cites a small, stable reference canon for the
SQLi class. This file records each body-cited source, who cited it, what the
cached copy says, and the retrieval outcome. **Quotes below are byte-true
from the cached copies.**

## 1. OWASP: SQL Injection (the "SQL_Injection" canon page)

- URL: `https://owasp.org/www-community/attacks/SQL_Injection` (accessed
  2026-10-25; 42,968-byte copy cached)
- Cited by: SQL-1018621 (three separate URL lines in its body), SQL-319465
  and SQL-508346 (both `See https://www.owasp.org/index.php/SQL_Injection`
  — the era's old URL form, 301-redirected today)
- Definition, verbatim (the corpus's shared class reference):

> SQL injection attacks are a type of injection attack, in which SQL commands are injected into data-plane input in order to affect the execution of predefined SQL commands.

- Threat-model line, verbatim (the impact vocabulary several reports echo):

> SQL injection attacks allow attackers to spoof identity, tamper with existing data, cause repudiation issues such as voiding transactions or changing balances, allow the complete disclosure of all data on the system,

## 2. PortSwigger Web Security Academy: SQL injection topic

- URL: `https://portswigger.net/web-security/sql-injection` (accessed
  2026-10-25; 55,705-byte copy cached)
- Cited by: SQL-1018621 — `[1] https://portswigger.net/web-security/sql-injection - *SQL injection explained*`
- The cached page is the modern topic index; its section heading *"What is
  SQL injection?"* is the direct successor of the definitions these 2021-era
  reports point to. (The step-by-step payload doctrine equivalent to the
  corpus's series method lives in the topic's blind-SQLi pages, not on the
  index — quote-verified from the cached copy, not paraphrased here.)

## 3. SektionEins: Advisory 01/2014 — Drupal pre-auth SQLi (SQL-31756's anchor)

- URL: `https://www.sektioneins.de/en/advisories/advisory-012014-drupal-pre-auth-sql-injection-vulnerability.html`
  (accessed 2026-10-25; 14,016-byte copy cached)
- Cited by: SQL-31756 (`# Advisory` section)
- Verbatim, from the cached advisory header block:

> Advisory: Drupal - pre Auth SQL Injection Vulnerability
> Release Date: 2014/10/15
> Author: Stefan Horst [stefan.horst[at]sektioneins.de]
> Application: Drupal >= 7.0 <= 7.31
> Severity: Full SQL injection, which results in total control and code execution of Website.
> Risk: Highly Critical
> Vendor Status: Drupal 7.32 fixed this bug

- This is the source that supplies the remediation/patch line
  (`SQLi-to-RCE-Chains.md` §9 defers to it — *"SQL-31756 points to the
  vendor advisory*").

## 4. MongoDB docs: `$regex` operator (SQL-1130721's oracle authority)

- URL: `https://www.mongodb.com/docs/manual/reference/operator/query/regex/`
  (accessed 2026-10-25; 961,712-byte copy cached)
- Cited by: SQL-1130721 (inline link in its `$regex` oracle description)
- Definition, verbatim:

> Provides regular expression capabilities for pattern matching strings in queries.

## 5. MongoDB docs: `$where` operator (SQL-1130874's oracle authority)

- URL: `https://www.mongodb.com/docs/manual/reference/operator/query/where/`
  (accessed 2026-10-25; 885,422-byte copy cached)
- Cited by: SQL-1130874 (inline link in its `$where` oracle description)
- Definition, verbatim:

> Use the $where operator to pass either a string containing a JavaScript expression or a full JavaScript function to the query system. The $where provides greater flexibility, but requires that the database processes the JavaScript expression or function for each document in the collection.

## 6. Ruby on Rails rubyonrails-security group post (SQL-28449/28450's link)

- URL: `https://groups.google.com/forum/#!msg/rubyonrails-security/wDxePLJGZdI/WP7EasCJTA4J`
- Cited by: SQL-28449 and SQL-28450 (both bodies are exactly the link plus
  "_This vulnerability was reported directly to Rails._")
- **Retrieval outcome: NOT RETRIEVABLE as of 2026-10-25.** Three channels
  tried, none delivered the post text: live page (JS-gated redirect stub),
  `forum/message/raw?` endpoint (HTTP 404), Wayback copy (JS-required stub,
  55,554-byte page renders no announcement text). Content is therefore
  **not paraphrased** in this vault; the two H1 rows remain link-only records.

## 7. mysqltutorial.org — mysql WHERE tutorial (recorded dead)

- URL as cited: `https://www.mysqltutorial.org/mysql-where/` — cited by
  SQL-1018621 as `[2] https://www.mysqltutorial.org/mysql-where/ - *MYSQL WHERE statment explained*` (sic "statment")
- **Retrieval outcome: HTTP 404 on 2026-10-25.** The tutorial has moved;
  only the citation is preserved (verbatim, with its typo).

## 8. nextcloud-gmbh/h1 issue #197 (recorded dead)

- URL: `https://github.com/nextcloud-gmbh/h1/issues/197` — cited by
  SQL-1390331 in its Supporting Material block (*"For more details see:"*).
- **Retrieval outcome: HTTP 404 on 2026-10-25** (the tracker link is dead;
  the body's own three-step reproduction carries the whole technical record
  quoted in `Library-and-Framework-SQLi.md` §3.9).

## 9. Cross-references and use rules

- Each playbook's quotes come from **report bodies**, not from these external
  pages; this file exists so an agent can follow the corpus's own
  citations without re-walking the web.
- Retrieval discipline matches the vault's global rule: dead/404 sources stay
  recorded as dead; no content is reconstructed from secondary sources.
- Cache layout: `/tmp/opencode/sqli/blogs/` holds the fetched copies
  (`owasp-sqli.html`, `portswigger-sqli.html`, `sektioneins-drupal.html`,
  `mongodb-regex.html`, `mongodb-where.html`, `rails-group.html` [stub],
  `rails-group-wb.html` [stub], `rails-raw.txt` [404 page]).
