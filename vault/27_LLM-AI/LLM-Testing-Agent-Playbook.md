---
title: "LLM Testing Agent Playbook — the executable protocol"
type: agent-playbook
category: llm-ai
cwe: "CWE-707"
built: "2026-11-07"
corpus: "1 classified row -> 1 body read (1 full-body / 0 metadata-only) · 0 adjacent rows"
bounty: "$2,500 across 1 row with a DB figure (max $2,500 LLM-2372363)"
companion_modules: "00 prompt-injection (sole module, 1 row)"
quote_rule: "byte-true, from read bodies only; invisible payloads described, never concealed"
---

# LLM Testing Agent Playbook — Invisible prompt injection

*Evidence base: 1 disclosed h1-brain corpus case (`LLM-2372363`). Every quoted sentence in the module is byte-true to `references/archive/llm-bodies-full-dump.txt`. Read the module before improvising; this file is the operational spine. **Boundary**: the corpus demonstrates advisory-suggestion steering only — no tool-use or exfiltration row exists.*

## P0 — Program classification & policy read (before any payload)

1. Program type: AI-assisted triage product (Hai-style assistant over user-submitted
   reports). The corpus pays one *advisory-suggestion* steer ($2,500, LLM-2372363). Read
   policy for allowed AI testing now: in-scope test reports and test accounts only; never
   production triage flows or real reporters' work.
2. Environment signal: classify the model input path — which user-submitted fields reach
   the model raw (no normalization), which are rendered to humans, and where the render
   path and the model path diverge. The divergence is the invisible-channel surface (P1).
3. Kill-gate: no testing yet — P0 produces the *policy envelope* only.

## P1 — Invisible-channel inventory (where the render path and the model path diverge)

| Channel | Corpus proof | What to map |
|---|---|---|
| Unicode tag characters (U+E0061–U+E007A family) | LLM-2372363 (`convert_from_tag_chars` decoder, `ord(ch) - 0xE0000`) | Every field accepted as free text and forwarded raw to the model |
| Other zero-width / format characters | _(none in corpus — hypothesis only)_ | Same fields, wider probe — label as hypothesis until demonstrated |
| Synthetic fixtures (fake reports, test accounts) | LLM-2372363 (blank-severity fake report, `rezo` fixture) | Test-account infrastructure for repeated submissions |

## P2 — Probe protocol (the tag-hidden → visible-fake → suggestion triple)

1. **Tag-hidden payload** — encode the instruction in tag characters, submit on a synthetic
   fixture report (blank severity). Verify the UI renders nothing (the invisible half).
2. **Visible-fake twin** — submit the same instruction as readable ASCII ("Additional
   details: …") so a human reviewer can verify the stream without a decoder (the corpus's
   readability half). Both halves ship in the report.
3. **Suggestion triple** — chat with the assistant asking for the analysis the payload
   targets the (severity, in the corpus). Three repetitions (the corpus's exact count:
   "We used the prompt injection payload 3 times"). Record suggestion text or state
   redaction honestly (the corpus's suggestion is redacted — do not guess it).
4. **Decode tool** — ship the decoder so any reviewer can verify the hidden stream
   (the corpus's `convert_from_tag_chars` script).

## P3 — Proof ladder (the modest demonstrations paid)

1. Submitted fixture (visible text + field states) + chat transcript showing the steered
   suggestion, ×3 runs.
2. Decoder reproduces the hidden text from the submitted bytes, in the report.
3. Remediation sentence (render-or-drop) written by the reporter — the corpus's remediation
   is one sentence and portable. Without it, the row is a steering anecdote.
4. No tool calls, no data access claimed beyond the suggestion. The impact list names
   advisory steers only (bounty, validity, severity).

## P4 — Modern hardening fingerprints (never corpus doctrine)

- **Render-or-drop on the model path**: show tag/format characters in the UI or strip them
  before the model sees the text (the corpus remediation, verbatim logic).
- **Input normalization before inference**: canonicalize free text (NFC, format-character
  policy) at the same boundary that serves the model — not only at render.
- **Fixture-aware evaluation**: test accounts and synthetic reports are marked so triage
  assistants never treat them as real reporter work (the `rezo` lesson).
- **Suggestion labeling**: advisory outputs carry provenance so a steered suggestion is
  visible as a suggestion, not a verdict.

## P5 — Pre-report gates (kill-gates)

1. **Triple gate** — hidden payload + visible twin + repeated suggestion. Any leg missing
   dies here (unverifiable in this corpus's terms).
2. **Decode gate** — the decoder is in the report and reproduces the payload from the
   submitted bytes. A hand-typed "hidden text" dies here.
3. **Fixture gate** — the report is synthetic and labeled as such. Re-filing the fake XSS
   as a real finding dies here (module §5).
4. **Scope gate** — suggestion-only impact. Tool-use/exfiltration claims without their own
   demonstrations die here; no corpus row supports them.
5. **Production gate** — in-scope test flows only. Any plan touching production triage or
   real reporters' reports dies here regardless of signal quality.

## Module ↔ phase table

| Phase | Corpus evidence (module) | Anatomy of the paid pattern |
|---|---|---|
| P1 inventories invisible channels | 00 (§2) | tag characters; render/model divergence; synthetic fixtures |
| P2 probes the triple | 00 (§§2–3) | tag-hidden → visible-fake → Hai suggestion ×3 |
| P3 proofs ladder, decode-first | 00 (§3) | fixture + transcript + decoder + remediation |
| P4 hardening fingerprints | 00 (§2) | render-or-drop; normalization; suggestion labeling |
| P5 kill-gates | 00 (§§5–6) | triple gate; decode gate; scope gate |

## Non-goals

- Tool-use hijack or data exfiltration via prompt injection — no corpus row demonstrates
  them; outside every module's claims and this playbook's protocol.
- General LLM red-teaming (jailbreaks, capability evals) — outside this vault; the module
  teaches the one demonstrated advisory-steer pattern only.
- Real-report or real-account targeting — outside P0/P5; synthetic fixtures only.
