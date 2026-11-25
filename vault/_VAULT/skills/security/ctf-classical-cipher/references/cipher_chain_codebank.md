# Cipher Chain — worked example (TRIVARNA "U - Cipher Chain")

Reference recipe for the multi-layer decode; not a mirror of upstream docs.

## Layer map (this specific challenge)
- Given: `sggkh://ulinh.tov/zFUwWCQgOzmkCuD67`
  - Atbash -> `https://forms.gle/aUFdDXJtLanpXfW67`  (Google Form)
- Form `FB_PUBLIC_LOAD_DATA_` embeds 6 "Decode it" parts.

## Part decodes (what actually worked)
- Part 1: null-cipher / Atbash alphabet shell. Atbash then strip filler runs
  (`abcdefghijklmnopqrstuvwxyz`, `ABCDEFGHIJKLMNOPQRSTUVWXYZ`, ``_^]\[``,
  `@?>=<;:9876543210/.-,+*)`). Residual letters extracted but not a clean sentence.
- Part 2: CJK blob `䥦㚑闊䧆脑琕䢢麮䇸㭌疩槶䁡砽⬬ʝ`. Uniform shift / CJK-atbash / mod26 all fail
  (codepoints span 0x29D–0x9EAE across the CJK boundary => NOT a linear shift; likely dict sub). UNSOLVED.
- Part 3: CJK codepoint-shift. Codepoints 0x7C3A–0x7C86 (tight band, span 76).
  - `chr(o-31752)` -> `GMBH|N3yQ:wL5sU8{O2rM9dE6xG4~` -> Caesar −1 -> `FLAG|M3xP:vK5rT8{N2qL9cD6wF4~`
  - `chr(o-31753)` -> `FLAG{M2xP9vK4rT7zN1qL8cD5wF3}`  (proper braces; intended flag)
- Part 4: mixed CJK + rare chars `腆籁赻ꔴ济虰𔐲汔蝫𔔵框ᕽ`. Same class as Part 2. UNSOLVED.
- Part 5: emoji `🐽👃🐸🐾👲👇🐪👭👅🐮👢👏🐨👨👉🐰👤👋🐫👱👃🐯👚🐻🐩👮🐽🐭👴`.
  - `emoji_mod26(s, 0x1F300)` -> `flaggpmbnqqxkwrsstnflridlcfpi` (flag-shaped decoy/partial).
- Part 6: `}NVLXFTRDLcw$AzFqkp{m3281497G5`. Caesar(±26) / Vigenère(wordlist) / XOR(1–2 byte) /
  reverse all fail to land on readable text. UNSOLVED in-session.

## Flag recovered from the data
`FLAG{M2xP9vK4rT7zN1qL8cD5wF3}`  (Part 3, K=31753)
Note: event boilerplate said `TRIVARNA{...}` but the ciphertext decodes to `FLAG{...}` — submit
what the ciphertext actually contains.

## Lesson cliff-notes
- "Unicode Atbash" within 0x4E00–0x9FFF => more CJK, dead end. Use codepoint-shift / mod26.
- Tight codepoint band => Caesar-in-Unicode (try K around 0x7BE0–0x7C10; brute 0x4000–0x9FFF scoring printable).
- Emoji => mod26 from a base in 0x1F000–0x1F700; scan for a readable prefix.
- Converge on the layer that yields valid braces + coherent inner; that is the flag.
