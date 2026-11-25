# Findings tree shapes and parsing rules

Observed shapes from real engagements. **Probe your own tree before parsing** — the
naming varies per engagement and per scanner that produced it.

---

## Shape A — asset / phase / finding / evidence  (most common)

```
Findings part 1 - Updated/
  FQ_0019_admin.app.dezaan.com/
    Finding/
      No SSL Implementation/
        1.png
      Breach/
        1.png
        2.png
    Revalidation/
      Lucky13/
        1.png
        2.png
        Issues.txt
  FQ_0039_africarice-api-uat.olamagri.com/
    Finding/
      Lucky13/
        Issues.txt
  FQ_0075_agripal-zuul.olamagri.com - Out of scope/
    Finding/
      Lucky13/
        Issues.txt
  IP_0373_41.77.173.33/
    Finding/
      ...
```

- Level 1 = asset folder
- Level 2 = phase (`Finding` / `Revalidation` / `Closure`)
- Level 3 = finding name
- Level 4 = evidence files

**Asset folder naming:**

| Pattern | Parse | Notes |
|---|---|---|
| `FQ_0019_admin.app.dezaan.com` | id=`FQ_0019`, host=`admin.app.dezaan.com` | Parse the FULL `PREFIX_NNNN` token as the id. Using only the alpha prefix (`FQ`) makes every FQDN asset collide. |
| `IP_0373_41.77.173.33` | id=`IP_0373`, host=`41.77.173.33` | Type is `IP`, not `FQDN`. |
| `FQ_0075_agripal-zuul.olamagri.com - Out of scope` | strip the ` - Out of scope` suffix | Keep the OOS marker — render it as a badge. |

**Phase dir naming varies:** `Finding`, `Revalidation`, `Closure`, occasionally
`Re-test`. Sort with a canonical order (`Finding` → `Revalidation` → `Closure`) and
put unknown phases last.

---

## Shape B — asset / finding / evidence  (no phase layer)

```
target-01/
  IDOR in user API/
    1.png
  SSRF via webhook/
    request.txt
    2.png
```

Detection: level-2 dirs are finding names, not phase names. Heuristic — if a level-2
dir is named `Finding`/`Revalidation`/`Closure`, it's a phase; otherwise treat it as a
finding.

---

## Shape C — flat, finding-name-prefixed files

```
findings/
  FQ_0019__No_SSL_Implementation__1.png
  FQ_0019__Breach__2.png
```

Split on `__`. Less common; worth handling if the tree is a single flat dir.

---

## Naming variance in finding folder names

Real histograms from a 341-finding engagement (top of the list):

| Count | Spelling |
|---|---|
| 80 | `Lucky13` |
| 44 | `Breach` |
| 13 | `Missing Security Headers` |
| 12 | `Improper implementation of Cross Origin Resource Sharing(CORS) - Closed` |
| 9 | `Components with known vuln` |
| 8 | `Information disclosure through HTTP response header - Closed` |
| 7 | `Missing Cookie Attributes` |
| 7 | `Lucky 13` |
| 7 | `BEAST` |
| 6 | `Information disclosure through HTTP response header` |
| 6 | `Breach - Closed` |
| 5 | `Missing Security headers` |
| 5 | `BREACH & LUCKY13` |

Variants seen for the same concept:

```
Lucky13   Lucky 13   LUCKY13   Lucky13 - Open   LUCKY13 - 2 Ips
Breach    Breach - Closed    Breach - Open    Brech    BREACH & LUCKY13
Missing Security Headers    Missing security headers    MIssing Security Headers
Missing Security Headers - Open
Missing rate limit    Missing Rate Limit - Closed    Missing rate limit - Closure
```

**Rules that follow from this:**

1. **Normalise before matching** — strip all non-alphanumerics and lowercase. Then
   `Missing Security Headers`, `Missing security headers` and `MIssing Security
   Headers` all collapse to one key.
2. **Normalise the RULE KEYS the same way.** If the rule says `"rate limit"` and you
   compare it to a space-stripped finding name, it never matches. Normalise both
   sides at load time:
   ```python
   CATS = [(norm(k), v) for k, v in CATS]
   ```
3. **Status comes from the suffix** — `- Closed`, `-Closed`, `- Open`, `-Closure`
   (and `Closure` as a phase dir). Strip it before classifying the core name, or
   `Closed` leaks into the category match.
4. **Typos are real** — `Brech`, `MIssing`, `Senstive`, `ifnor`, `issurs`,
   `Isue`, `Issu`, `Fidnings`, `Offereed`. A fuzzy or generous rule set is needed;
   every remaining unmatched finding should be enumerated and given a rule.
5. **Casing-insensitive `js` matching is dangerous** — a bare `js` substring rule
   matches inside many words. Anchor it to the end of the name or use a more
   specific token (`vulnjs`, `vulnerablejs`).

---

## Evidence file types seen

| Type | Count in one tree | Handling |
|---|---|---|
| `.png` | 578 | Thumbnail grid + full-res lightbox |
| `.txt` | 99 | Render INLINE as a code block. These are usually the actual PoC (cipher lists, request/response, tool output). |
| `.html` | 1 | Render as a labelled link to the raw file. Do NOT iframe it — it may contain an active clickjacking payload. |

`.txt` basename variance: `Issues.txt`, `Issue.txt`, `Issu.txt`, `Isue.txt`,
`issurs.txt`, `Issueses.txt`, `Issseus.txt`, `issue.txt`, `issues.txt`,
`Issue-8172.txt`, `Issue-443.txt`, `Location.txt`, `Fidnings.txt`,
`Cipher.txt`, `Issue ciphers.txt`.

Treat **any** `.txt` under a finding folder as that finding's PoC/evidence, whatever
it is called. Do not match on a specific filename.

**Content shape:** the `.txt` files are frequently just a bare list — e.g. cipher
IDs from a TLS scanner:

```
xc027 ECDHE-RSA-AES128-SHA256	CBC
xc028 ECDHE-RSA-AES256-SHA384	CBC
x3c AES128-SHA256	CBC
```

That is still the finding's evidence and belongs on the card. Render it verbatim in a
monospace block.

---

## Phases — are they duplicates?

Before merging a finding that appears under both `Finding` and `Revalidation`,
check for real cross-phase collisions:

```python
import os, re, difflib
def core(n):
    n = re.sub(r'\s*[-–]?\s*(closed|open|closure)\s*$', '', n, flags=re.I).strip().lower()
    return re.sub(r'[^a-z0-9]+', '', n)

for d in sorted(os.listdir(base)):
    f1, f2 = os.path.join(base, d, 'Finding'), os.path.join(base, d, 'Revalidation')
    if not (os.path.isdir(f1) and os.path.isdir(f2)):
        continue
    A = {core(x) for x in os.listdir(f1) if os.path.isdir(os.path.join(f1, x))}
    B = {core(x) for x in os.listdir(f2) if os.path.isdir(os.path.join(f2, x))}
    print(d, "exact overlap:", A & B)
    # also fuzzy, for typo variants
    for a in A:
        for b in B:
            r = difflib.SequenceMatcher(None, a, b).ratio()
            if r >= 0.80:
                print("   fuzzy", r, a, b)
```

In the engagement referenced above: 15 assets had BOTH phases, and **zero** findings
shared a core name across them (exact and fuzzy). The phase sets were genuinely
disjoint — a revalidation pass found *different* issues than the original scan. A
merge was therefore a safe no-op, but it had to be verified, not assumed.

---

## Output directory placement

Keep the dashboard **beside** the source, never inside it:

```
/home/user/Downloads/
  Findings part 1 - Updated/          <- source, READ-ONLY
  OLAM-Findings-Dashboard/            <- generated output
```

The source tree is the operator's evidence. Never write thumbnails, scratch files or
an `index.html` into it.
