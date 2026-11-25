# The playbook vault — layout convention

`/home/user/projects/FAN/Vault` is the user's long-running vulnerability playbook library.
Anything harvested (corpus, payloads, CVEs) is only useful once it is wired into this shape.

## Entry point

`00_MASTER_CATEGORY_LIST.md` — the build sequence: one row per category with H1 disclosed count,
status (✅ DONE → `DIR/`), module count, row count and bounty total. A new session reads this first;
**if you add a layer or a category, add it here or the next session never finds it.**

## Per-category directory

Every category dir (XSS, SQLi, SSRF, IDOR, CSRF, Open-Redirect, Authentication-Session, RCE,
File-Upload, Race-Conditions, XXE, and the numbered `12_`…`30_` set) follows the same shape:

```
README.md                      frontmatter (title, type: index, category, built, evidence, bounty,
                               companion_vaults, case_id_scheme, quote_rule) + "Start here" table
<CAT>-Testing-Agent-Playbook.md  the executable protocol: carrier inventory -> cheapest probes ->
                               lane decision tree -> escalation -> validation gates -> report assembly
NN_<Class-Module>.md           one file per sub-class: overview, case-stock table, verbatim evidence,
                               agent execution template, validation gates
references/case-register.md    row-per-row ledger: case id, program, bounty, module, CVE, title
references/source-index.md     provenance: roster, filters, funnel numbers, fetch mechanics, limits
references/blogs-index.md      bibliography (titles linked; marked when not byte-read)
references/archive/            verbatim report bodies + raw JSON cache
```

## Discipline the files already enforce (keep it)

- Case IDs are `<CLASS>-<HackerOne report id>`, e.g. `CACHE-1695604`.
- Quotes are byte-true and (sic)-marked, taken from bodies actually read. 404 rows are recorded as
  404 and **never quoted**. Titles alone are never presented as evidence.
- Bounty figures come from `bounty_amount` (JSON) where present, otherwise the mirror's list figure,
  always labeled; `-` means "no figure", not "unpaid".
- Each module states `source_count` / `full_bodies_available` in frontmatter so a reader knows how
  much of the case stock was actually read.

## Where the corpus layer plugs in

- `_HEXBRAIN/README.md` — dataset index, per-class and per-dir counts.
- `_HEXBRAIN/by-vault-category/<dir>.md` — every report routed to a playbook dir, richest first.
- `_HEXBRAIN/scripts/extract_report.py <id>` — pull a verbatim body before citing it in a module.
- Each playbook README carries a fenced `<!-- HEXBRAIN-CASE-STOCK -->` block injected by
  `scripts/inject_case_stock.py`; re-run it after every corpus refresh.
