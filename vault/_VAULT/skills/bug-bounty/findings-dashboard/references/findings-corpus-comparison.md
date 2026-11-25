# Findings-corpus comparison — what is NEW across multiple finding sets

Distinct from building a dashboard (one tree, one review surface). This is the task
where the operator points at a folder holding **two or more finding sets** and asks
"list all types of findings present" / "what is new" / "what did each set find".

Real session: `/home/user/Downloads/Analysis/` held
`final-finding-upload/` (196 findings, 81 hosts, NSTAR-report.md format) and
`New Final Finding/` (1,015 findings, 213 hosts, folder-per-finding + Issue.txt format),
plus a master ledger `final-findings-tracker.csv` (646 rows) and
`EPT_2026_Master_Tracker.xlsx`.

## Step 1 — enumerate BOTH sets with the same extractor

Do not assume one layout. Write a walker that yields `(set, host, category, title,
path)` regardless of shape, handling all of:

| Shape | Where the title lives |
|---|---|
| `<host>/Findings/New/<title>/NSTAR-report.md` | directory name |
| `<host>/Findings/<title>/1.png` | directory name |
| `<host>/Revalidations/<title>/Issue.txt` | directory name |
| flat `<host>/<finding>.md` | filename |
| master `.csv` / `.xlsx` | `Finding Name` column |

Probe first: `find . -name '*.md' | wc -l`, per-directory `ls`. Two sets can share
**zero hosts** — that is the single most important fact to establish before any
"new findings" claim.

## Step 2 — establish the overlap FIRST

```python
h1 = {strip_prefix(h) for h,_ in set1}
h2 = {strip_prefix(h) for h,_,_,_ in set2}
```
`strip_prefix` removes the `FQ_0123_` / `IP_0456_` asset-id prefix, or you get false
"no overlap". In the real session the raw comparison said 0 common hosts; the stripped
comparison is what actually describes the engagement.

If overlap is genuinely zero, say so plainly — it means the sets are complementary
generations (e.g. "net-new 2026" vs "baseline + revalidation backlog"), NOT duplicates.

## Step 3 — classify into canonical buckets, not raw titles

Raw titles will never match across sets. Normalize hard, then bucket by regex over a
curated table. Two levels of normalization:

```python
def norm(t):
    t = t.lower()
    t = re.sub(r"[^a-z0-9]+", " ", t)
    return re.sub(r"\s+", " ", t).strip()

def canon(t):
    n = norm(t)
    # strip trailing workflow statuses — they are NOT finding types
    n = re.sub(r"\s*-\s*(closed|not testable|open|confirmed|need confirmation.*|"
               r"might be discarded.*|candidate.*|vulnerable|potential.*)$", "", n)
    return n
```

Bucket table (order matters — first match wins). Keep it coarse; 18-22 buckets is
enough. The real session used: TLS protocol/cipher, TLS certificate, security headers,
CORS, information disclosure, EOL/outdated components, RCE, cookie/session, rate
limiting, SSRF, user enumeration, sensitive-data-in-GET, unauthenticated exposed
endpoints, network/DNS, input validation, XSS, open redirect, auth bypass, HTTP
methods/cache.

**Report the bucket table with set1/set2/total columns.** That table IS the answer to
"list all types of findings present".

## Step 4 — diff, then report the DELTA not the union

The operator asked "only new findings from both". The useful output is:

1. **Buckets present in set A but absent from set B** (and vice versa).
2. Per-bucket counts in each set.
3. Hosts unique to each set.
4. A short "highest-value findings overall" table (severity + finding + host), filtered
   to the non-hygiene classes (auth bypass, RCE, injection, SSRF, credential exposure).

Do not dump all 1,200+ titles. Summarize the delta; list the high-value rows.

## Step 5 — mine the master ledger if one exists

A `*-tracker.csv` / `*Master_Tracker.xlsx` is the authoritative denominator and gives
dimensions the folder walk cannot: `Open/Closed`, `Revalidation Yes/No`, `Entity`.
Read it with `csv.DictReader(open(p, encoding="utf-8-sig"))` — the leading BOM
(`\ufeff`) will silently corrupt the first column name otherwise.

In the real session: 646 rows → 460 Open / 151 Closed / 35 Not Testable; 196 net-new vs
450 revalidated. That reframed the whole answer — the folder walk counted 1,211 finding
instances but the ledger's unique-finding count was 646.

## Step 6 — extract severity from the report bodies, not the folder names

Folder names carry no severity. Parse it:

```python
sev = re.search(r"\*\*Severity:\*\*\s*([A-Za-z]+)", txt)
title = re.search(r"\|\s*01\s*\|\s*\*\*Observation Title\*\*\s*\|\s*([^|]+)", txt)
vid  = re.search(r"\*\*Vuln ID:\*\*\s*`?([^`\n|]+)", txt)
cvss = re.search(r"\|\s*14\s*\|\s*\*\*CVSS v4\.0\*\*\s*\|\s*([^|]+)", txt)
```

Report the full severity histogram (it is usually dominated by Low/Info — say that,
because the operator reads "1,015 findings" as "1,015 problems"). In the real session:
200 low, 109 n/a-negative-revalidation, 69 medium, 62 info, 1 high, **1 critical**.

## Step 7 — surface CHAINS, not just flat findings

The most valuable output is composite narratives, because the corpus often holds the
primitives of one big bug scattered across many hosts. Real session produced three:

1. **Identity-layer collapse** — auth bypass (no password check → signed JWT) +
   unsalted SHA-512 digest-as-credential + no rate limiting → ATO. The headline.
2. **Magento estate systemic exposure** — 12 hosts sharing `cron.php` bootstrap + shared
   mismatched TLS certs + expired certs + XML-RPC multicall. One platform defect
   replicated; write it once, reference the hosts.
3. **SSRF → internal pivot** — 18 blind-SSRF instances on the same app farm. Blind alone
   is Low, but 18 copies means a template-level defect worth one deep-dive.

Tell the operator explicitly when N low-severity instances of one class are really ONE
finding, and when they are genuinely separate.

## Pitfalls

- **Trailing workflow statuses are not finding types.** `Missing security headers -
  Closed`, `- Not testable`, `- Open` are the SAME finding in different states. Strip
  them before diffing, or your "unique findings" count inflates ~3x.
- **Case/spacing variants multiply false deltas.** `Lucky13` / `Lucky 13` / `LUCKY13`;
  `Breach` / `BREACH` / `Brech`; `Missing Security Headers` / `Missing Secuirty
  Headers` (real typo) / `Misconfigiurted Headers`. Normalize before comparing.
- **`grep -r` on paths with spaces silently splits.** Finding titles contain spaces.
  Always iterate in Python (`os.walk`) or use `find -print0 | xargs -0`. A shell loop
  over `grep -rl` output produced garbage for the entire analysis in the real session.
- **Don't trust the folder count as the finding count.** Master ledger said 646; folder
  walk said 1,211. Both are true — different denominators. State which you are using.
- **Zero host overlap is a finding, not a failure.** It tells you the sets are
  generations of the same engagement, and it prevents you from wrongly reporting one
  set as a duplicate of the other.
- **Severity histograms from `grep -rhoP` on `NSTAR-report.md` can mislead** when the
  severity line has a trailing `(...)` qualifier. Count the clean token only.
