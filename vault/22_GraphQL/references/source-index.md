---
title: "GraphQL source index — provenance, funnel, classification, limitations"
type: source-index
built: "2026-11-07"
---

# Source index — GraphQL build

## 1. Corpus provenance

- **Primary source**: `/home/user/tools/h1-brain/disclosed_reports.db` — h1-brain's pre-built
  SQLite corpus of publicly disclosed HackerOne reports (**3,673 rows**), sha256
  `8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4`.
- **Working copies**: `/home/user/opencode-work/h1brain/classified.json` (bucket `graphql`, 18
  rows) and `module_map_all.json`. In-vault: `references/archive/GQL-bodies-full-dump.txt`
  (19 bodies), `classes.json`, `meta.json`.

## 2. Classification funnel

1. **Labeled/keyword net**: weakness labels (`GraphQL`) plus keyword arms (`graphql`, `mutation`,
   `__typename`, `query {`) → 18 rows.
2. **Body read**: all read before assignment.
3. **Module split** (frozen in `classes.json`):
   - 01 `authz-session-disclosure` 9 — read-side authorization/session-state gaps.
   - 02 `idor-mutation-type-confusion` 4 — mutation IDOR, undocumented mutations, type confusion.
   - 03 `injection-ssrf-csrf-xss-dos` 5 — sinks reached through GraphQL.
   - merge `_adjacent_unclassified` 1 — GQL-1276992, from the unclassified pool.

## 3. Bounty accounting

- **Rule**: DB `bounty_amount`; `-` when absent. Blank ≠ unpaid.
- **13/19 rows** carry figures, totaling **$58,340**; max $25,000 (GQL-1618347).
  Module totals: 01 $27,870/5 · 02 $19,500/3 · 03 $8,470/4 · merge $2,500/1.

## 4. Era discipline

- Rows span 2018–2024. Persisted-query allowlists, depth limits, and field-level authorization
  frameworks have landed widely since the earliest rows; the *probe* (mirror an existing rule onto
  the resolver) remains valid even when the specific schema does not.
- Weakness labels on HackerOne vary (`Information Disclosure`, `Privacy Violation`, `IDOR`);
  modules classify by body.

## 5. Limitations

1. **18-row bucket** — a disclosed-only slice; master-list row 22 cites an "API class" without a
   fixed count.
2. **Schema-specific findings age** — `node(id:)`, `fileCopy`, and `allTicks` are pattern
   examples, not a current map.
3. **One merge row** (GQL-1276992) is outside the bucket and labeled as such.
4. **No live testing** — all claims trace to archived bodies.
5. **Quote discipline**: every blockquote is byte-true to
   `references/archive/GQL-bodies-full-dump.txt`; `(sic)` marks author typos.
