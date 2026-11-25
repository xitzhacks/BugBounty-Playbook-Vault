---
name: findings-dashboard
description: "Build a temporary local browsable dashboard over a findings/evidence tree so every finding, its name and its PoC are visible in ONE scroll without drill-down. Use when the user points at a folder of findings (screenshots + PoC txt/html) and asks for a dashboard, 'see each finding clearly', 'without switching', 'temporary dashboard', or 'parse this folder'. Covers tree probing, the builder script, auto-classification, and the four verification gates that catch silent breakage. NOT for writing a client report or a one-file handoff."
tags: ["bug-bounty", "reporting", "workflow", "artifacts"]
---

# Findings Dashboard — browsable evidence tree

Turn a folder-of-evidence (`<asset>/<phase>/<finding name>/<screenshot|poc>`) into a
single local page where every finding, its name, and its PoC are visible **without
switching or clicking through folders**.

## When to use

- The user hands you a findings/evidence folder and asks for a dashboard / "parse this
  and create a dashboard" / "see each finding clearly" / "without switching" / "temporary".
- Triggers: `dashboard`, `see each finding`, `without switching`, `parse this folder`,
  `one page for all findings`, `review all my findings`.
- Typical source shape: `~/Downloads/Findings part N/`, `~/Bugbounty/<target>/Findings/`,
  `.../engagement_log/poc/`.

**Do NOT use this skill for:**

| Task | Use instead |
|---|---|
| A client-facing report (MD/DOCX/PDF) | `redteam-report-template` |
| A platform submission body | `report-writing`, `bugcrowd-reporting` |
| One file summarising the engagement | `session-handoff`, `engagement-handoff` |
| One finding stated in chat | `direct-vuln-reporting` |
| Deciding *whether* a finding is valid | `triage-validation` |

The dashboard is a **review/triage surface**, not a deliverable. It lets the operator
see what they actually have. It does not assert validity, and it does not replace the
report.

---

## The core requirement — read this first

> "see each finding clearly **without switching** with poc and name"

This is the single hardest constraint and the thing most easily gotten wrong. It means:

1. **A flat "all findings" view is the deliverable**, not an optional extra. Every
   finding from every asset, rendered in ONE continuous scroll, grouped under a sticky
   per-asset header bar. The operator must never have to open a folder, click through
   a tree, or change view to see finding #212.
2. **PoC content is inline**, not behind a click. A `.txt` PoC renders as a visible
   code block under its finding. An `.html` PoC renders as a labelled link (it must
   open raw — do not iframe it).
3. **Screenshots are visible as thumbnails in the grid**, with a full-resolution
   lightbox on click.
4. The finding **name** is the card title, always visible — never a hover-only tooltip.

Ship the drill-down views (sidebar per asset, per-asset view) as a convenience, but the
flat view is what answers the request.

---

## Architecture — never hand-write the output

The output is **generated** by a builder script from a template. Hand-writing the
resulting HTML means the data, the categories and the asset list drift out of sync the
moment the source folder changes.

```
<output-dir>/
  index.html                       generated — data inlined, portable
  manifest.json                    machine-readable inventory (for scripts / diffing)
  thumbs/                          640px JPEG thumbnails (fast grid load)
  _dashboard/assets/               full-res PNGs + txt + html PoCs
  _dashboard/data.js               same data, standalone JS
```

Use the bundled builder:

```bash
python3 <skill-dir>/scripts/build_findings_dashboard.py \
        --source "/path/to/Findings part 1 - Updated" \
        --output "/path/to/Findings-Dashboard" \
        --template <skill-dir>/templates/dashboard_template.html
```

The template carries a `__DATA__` placeholder that the builder replaces with the
inlined JSON payload. **Edit the template, never the generated `index.html`** — editing
the output silently gets overwritten on the next rebuild.

---

## Procedure

### 1. Probe the tree BEFORE writing any code

Never assume the shape. Run the probes first and read the real output:

```bash
SRC="/path/to/Findings"
find "$SRC" -type f | wc -l                        # total file count
find "$SRC" -type f -printf '%f\n' | sed 's/.*\.//' | sort | uniq -c | sort -rn   # file types
find "$SRC" -mindepth 1 -maxdepth 2 -type d -printf '%P\n' | sort   # asset + phase dirs
find "$SRC" -mindepth 3 -maxdepth 3 -type d -printf '%f\n' | sort | uniq -c | sort -rn  # finding names
```

Read the finding-name histogram. It tells you the naming variance you must classify
around (`Lucky13` vs `Lucky 13` vs `LUCKY13`, `Breach - Closed` vs `Breach -Closed`,
`MIssing Security Headers` vs `Missing Security Headers`). Count them — you will use
this number to prove the classifier actually worked (gate 2).

Also read one `.txt` and one `.html` PoC to learn what "PoC" means in this tree. They
are frequently just a list of cipher IDs, not a narrative.

### 2. Pick the output dir — and keep the source READ-ONLY

The source tree is the operator's evidence. **Never mutate it.** No generated
thumbs, no scratch files, no `index.html` dropped into their findings folder. Copy
assets out into the output dir. If you need a scratch file while building, put it in
`/tmp` and clean it up.

The user said "temporary" — so the output is disposable and local. Do not deploy it,
do not push it, do not share it externally. Bind the server to `127.0.0.1`.

### 3. Build

```bash
python3 <skill-dir>/scripts/build_findings_dashboard.py --source "$SRC" --output "$OUT"
```

The script auto-classifies findings, generates thumbnails, copies full-res evidence,
inlines the payload and writes `manifest.json`.

### 4. Serve it — relative paths need a server

```bash
cd "$OUT" && python3 -m http.server 8899 --bind 127.0.0.1
```

`file://` will not load the JSON payload and the copied evidence reliably. Use a
server. `start.sh` in the output dir is a convenience wrapper.

### 5. Verify — run all four gates

See **Verification gates** below. Do not report the dashboard as done until the
browser check passes.

---

## Auto-classification

Findings are classified from their **folder name** (that is all you have). The rule
table lives in `CATS` / `SEV_RULES` inside the builder script.

**Normalise the rule keys at load time, not by hand:**

```python
def norm(s): return re.sub(r"[^a-z0-9]+", "", (s or "").lower())

CATS     = [(norm(k), v) for k, v in CATS]
SEV_RULES = [(norm(k), v) for k, v in SEV_RULES]
```

Finding names are compared space-stripped, so a rule key written as `"rate limit"` or
`"openssl eol"` can NEVER match unless it is normalised the same way. This is the
single most common cause of "every finding landed in Other" (gate 2).

Severity derived this way is **triage readability only**. It is not CVSS and must not
be copied into a report. Say so in the final summary to the operator.

---

## Verification gates

These four bugs are all silent — the page renders, looks fine, and is quietly wrong.
Each one shipped in a real build before it was caught. Run all four.

### Gate 1 — asset IDs are unique

Folder names look like `FQ_0019_admin.app.dezaan.com`. If you parse the ID as the
leading *alpha* prefix (`FQ`), every FQDN asset gets id `FQ` and **every sidebar click
opens the first asset**. Parse the full `PREFIX_NNNN` token, then assert:

```python
ids = [a["id"] for a in data["assets"]]
assert len(ids) == len(set(ids)), "duplicate asset ids"
```

### Gate 2 — the classifier actually classified

If one category holds ~all findings, the rules are not matching. Read the category
chips in the rendered page (or count in the payload) and confirm the distribution is
sane. "Other" should be small — ideally zero. Every remaining "Other" is a rule you
missed; enumerate them and add rules until it is empty or genuinely irreducible.

```python
from collections import Counter
c = Counter(f["cat"] for a in data["assets"] for f in a["findings"])
print(c.most_common())
```

### Gate 3 — every referenced file exists

Broken evidence paths render as silent empty boxes. Assert against the filesystem:

```python
missing = [p for a in data["assets"] for f in a["findings"] for i in f["items"]
           for p in (i.get("src"), i.get("full")) if p and not Path(p).exists()]
assert not missing, missing[:5]
```

### Gate 4 — DOM ids are unique in the flat view

The same finding name ("Lucky13") appears under many assets. In the flat all-findings
view, a DOM id built from the finding name alone collides — clicking one card toggles
another, and the lightbox opens the wrong evidence. Namespace the id with the asset id:

```js
const uid = (asset ? asset.id + '_' : '') + f.key;
```

Same for any image registry you build for the lightbox — **reset it on every
re-render** or stale indices point at the previous view's images.

---

## Pitfalls

- **Hand-writing the output.** Generated files drift. Template + builder, always.
- **Mutating the source tree.** Copy out; never write into the operator's evidence.
- **Not probing the tree first.** The folder naming varies wildly between engagements
  (`Finding` vs `Revalidation` vs `Closure`; `Issues.txt` vs `issurs.txt` vs
  `Isue.txt` vs `Issue-8172.txt`). Read it, don't assume.
- **Assuming phases merge.** Same-named finding under `Finding` and `Revalidation` may
  be genuinely different findings. Check for cross-phase collisions before merging;
  if there are none, a merge is a safe no-op — but verify rather than assume.
- **JSON rules read as objects in JS.** Python tuples serialise to JSON **arrays**.
  `rule.k` is `undefined` on an array; you need `rule[0]` / `rule[1]`. Symptom: every
  category reads "Other".
- **Thumbnails saved with the wrong extension.** Pillow writing JPEG bytes to a `.png`
  filename is a MIME mismatch. Give the thumb the extension of the format you actually
  save.
- **Keys with spaces compared to space-stripped names.** See Auto-classification.
- **Non-unique DOM ids in a flat list.** See gate 4.
- **Lightbox keyed by a parsed string.** `key.split('~')` with names containing the
  delimiter breaks silently. Use a global registry array and pass an index.
- **Stale background server.** A `python3 -m http.server` started in the background can
  die between turns; re-check with `curl -o /dev/null -w '%{http_code}'` before
  concluding the page is broken.
- **Browser context resets between navigations.** After a re-navigation, `browser_console`
  can no longer see page globals. Re-navigate before evaluating page state.
- **Bulk image re-categorization with missing extensions.** When copying/re-naming
  evidence images into a new findings tree, always wipe the destination first or verify
  exact destination keys — otherwise stale extensionless copies from earlier steps silently
  become duplicates or "extra" files after you add `.png`. Two images with the same content
  but different filenames (`POC2-3090` vs `POC2-3090.png`) will both exist and break
  integrity checks.
- **Category normalization mismatch across engagements.** Source categories may vary in
  casing and spacing (`Self signed`, `Self Signed`, `Weak SSL`, `Weak ssl`, `reneogotiation`
  typo, `Luck13` vs `Lucky13`). Normalize at ingestion time with the same key shape used
  for destination folders, otherwise files silently scatter or duplicate.
- **Verification by filename/size alone.** If two different source files happen to share
  the same basename, a naive list comparison will say "already copied" while the file
  body is actually the wrong one. Use content hashes when checking whether a destination
  file matches an intended source file.

---

## User preference notes

- **"Temporary" means temporary.** Local-only, disposable, `127.0.0.1`. No deploy, no
  push, no external share. Put it next to the source, not inside it.
- **"Without switching" is the acceptance criterion.** If the operator has to click
  a tree to see a finding, the deliverable failed — even if everything renders.
- **Show the real thing.** The operator wants to see the actual screenshot and the
  actual PoC text, not a summary of them. Do not substitute a table of names for
  rendered evidence.
- **Report the numbers, then the path.** State assets/findings/evidence counts and the
  URL, then the absolute path. Flag the highest-signal findings (the SSRF, the open
  redirect) — the operator does not want to hunt through 341 cards to find them.
- **Be honest about auto-derived severity.** Say plainly that the badge severity is
  derived for triage readability and is not the report severity.

---

## Support files

- `scripts/build_findings_dashboard.py` — the builder. Re-runnable against any
  findings tree; `--source`, `--output`, `--template`. Run with `--rebuild-thumbs`
  after the source changes materially.
- `templates/dashboard_template.html` — the UI template with the `__DATA__` placeholder.
  Edit this to change layout/colour; never edit the generated `index.html`.
- `references/findings-tree-shapes.md` — observed tree layouts, naming variance, and
  the parsing rules for each.
- `references/findings-corpus-comparison.md` — COMPARING two or more finding sets and
  answering "what is NEW / list all finding types". Covers: enumerating mixed layouts
  with one walker, host-overlap (strip the `FQ_NNNN_`/`IP_NNNN_` prefix first), canonical
  bucketing with trailing-status stripping, mining the master `*-tracker.csv` ledger,
  severity extraction from report bodies, and surfacing CHAINS (e.g. auth-bypass +
  password-equivalent hash + no rate-limit = ATO) instead of a flat list. Read this when
  the operator points at a folder holding MULTIPLE finding sets, not one.

## Related Skills & Chains

- **`session-handoff`** — When the engagement needs a single durable `.md` summary
  alongside the dashboard. The dashboard is the *review surface*; the MASTER file is
  the *persistence artifact*. Build both; they serve different purposes.
- **`triage-validation`** — When the operator starts using the dashboard to decide what
  to submit. The dashboard shows what exists; the 7-Question Gate decides what is
  valid. Do not treat a dashboard card as a validated finding.
- **`evidence-hygiene`** — When the dashboard's screenshots are reused in a submission.
  The dashboard copies raw evidence verbatim; redaction discipline still applies before
  anything goes to a platform.
- **`redteam-report-template`** — When the reviewed findings become a client
  deliverable. The dashboard feeds it; it does not replace it.
