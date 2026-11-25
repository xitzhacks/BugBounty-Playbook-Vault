---
name: ctf-classical-cipher
description: Decode multi-layer "classical + modern" CTF cipher chains — scrambled URLs, CJK/emoji/symbol blobs with "Decode it" prompts, and HTML/Google-Forms containers hiding layered ciphertexts. Covers Atbash (incl. URLs), Caesar, Vigenère, CJK codepoint-shift, emoji-mod26, null-cipher alphabet shells, and Google-Forms FB_PUBLIC_LOAD_DATA_ extraction. Use when a challenge ships a mangled URL, a wall of CJK/emoji text, or a form/page that points to further layers; goal is to recover the flag that the ciphertext actually contains (not the format the description claims).
---

# CTF Classical / Cipher-Chain Decoder

## When to use
A challenge that:
- Ships a scrambled URL (e.g. `sggkh://ulinh.tov/...`) or says "Decode it" with a blob of CJK / emoji / symbol text.
- Hides ciphertext inside a Google Form, HTML page, or "Decode it" list of parts, each part a different cipher.
- Mentions classical techniques (Atbash, Caesar, Vigenère, ROT, substitution) and/or modern ones, "pattern recognition", "layers".
Event-flag boilerplate (e.g. "flags look like TRIVARNA{...}") is often WRONG for the specific challenge — see Pitfalls.

## Layer 0 — Atbash (and Atbash on URLs)
Atbash = reverse the alphabet (a↔z, b↔y, A↔Z). Detect a scrambled URL when the scheme/host looks reversed: `sggkh` is reverse of `https`, `ulinh.tov` reverses to `forms.gle`/similar. Always try Atbash on any suspicious URL before fetching.
```python
def atbash(s):
    o=[]
    for c in s:
        if 'a'<=c<='z': o.append(chr(219-ord(c)))
        elif 'A'<=c<='Z': o.append(chr(155-ord(c)))
        else: o.append(c)
    return ''.join(o)
```

## Google Forms containers
Challenges love hiding the real ciphertext in a Google Form. Do NOT scrape rendered HTML — extract the embedded JSON:
```python
import re, json
m = re.search(r'FB_PUBLIC_LOAD_DATA_\s*=\s*(\[.*?\]);', html, re.S)
j = json.loads(m.group(1))
# recursively walk j; collect every string that startswith "Decode it"
# each such string = "Decode it[...]\n\n<CIPHERTEXT>"
```
See `scripts/decode_chain.py` → `extract_forms(html)`.

## CJK codepoint-shift (Caesar in Unicode space)
Many CTF CJK blobs are NOT "Unicode Atbash" — they are a constant codepoint offset. Signs: codepoints cluster in a TIGHT band (e.g. 0x7C3A–0x7C86, span ~76). Brute a constant K so `chr(ord(c)-K)` is all printable ASCII, THEN apply a classical Caesar on top.
- Part 3 of one chain: codepoints 0x7C3A–0x7C86, K=31752 → `GMBH|N3yQ:...` → Caesar −1 → `FLAG{M3xP:vK5rT8{N2qL9cD6wF4~}`; K=31753 directly → `FLAG{M2xP9vK4rT7zN1qL8cD5wF3}` (proper braces, the intended flag).
- Brute helper: `scripts/decode_chain.py` → `cjk_shift_brute(s)` returns top-K printable candidates.

## Emoji → mod26
Emoji sequences often encode letters via `(ord(emoji) - base) % 26`. Base varies; the chain used `base=0x1F300` giving `flaggpmbnqqxkwrsstnflridlcfpi` (a `flag{...}`-shaped decoy/partial). Try bases 0x1F000–0x1F700 and look for a readable prefix ("flag", "the", "key").
```python
def emoji_mod26(s, base=0x1F300):
    return ''.join(chr((ord(c)-base)%26+97) for c in s)
```

## Null-cipher alphabet shell
Some layers wrap ONE real letter per "frame" inside a filler of the full alphabet / reversed alphabet. Split on the frame delimiter, atbash if needed, then remove the constant filler runs (`abcdefghijklmnopqrstuvwxyz`, `ABCDEFGHIJKLMNOPQRSTUVWXYZ`, symbol tails like ``_^]\[`, `@?>=<;:9876543210/.-,+*)`). The residual per frame is the hidden letter. (This was only ~80% solved in-session — treat as a heuristic, not guaranteed.)

## Convergence check (the actual methodology)
1. Decode EVERY layer/part INDEPENDENTLY with the matching cipher.
2. Most layers reveal a `flag{...}` / `FLAG{...}` wrapper. The layer whose decode yields PROPER braces + coherent content is usually the intended flag.
3. If layers disagree on content, the challenge may want the SAME flag expressed in different encodings — pick the one with valid braces and readable inner.

## Pitfalls
- **Stated flag format is often a lie.** The challenge text may say `TRIVARNA{...}` but the decrypted data contains `FLAG{...}` (this challenge) or `CSEMA{...}` (Leaky Stream). SUBMIT WHAT THE CIPHERTEXT ACTUALLY DECODES TO. Boilerplate ≠ answer.
- **CJK "Unicode Atbash" (reflect within 0x4E00–0x9FFF) is usually WRONG** for these blobs — it just yields more CJK. Use codepoint-shift / mod26 instead.
- **Vigenère / XOR brute on a stubborn part often fails** because that part uses a substitution dictionary, not a simple transform. Don't burn time; the flag is almost always recoverable from the layers that DO decode cleanly.
- **Don't trust a single "consistent" decode if the full plaintext is garbage** — verify `pt[:len(header)]==header` AND overall readability before declaring victory (same lesson as LFSR seed ambiguity: extra known plaintext / proper packing matters).
- Wide codepoint span (e.g. 0x29D–0x9EAE across the CJK boundary) ⇒ NOT a single linear shift; it's a different cipher class.

## Tooling
- Run everything in `execute_code` (Python, absolute paths, `int.bit_count()` for speed).
- For each part: print `repr(ciphertext)` with exact codepoints (`[hex(ord(c)) for c in s]`) — the band/span of codepoints dictates the technique.

## Related
- `lfsr-xor-crib` — for XOR keystream / known-plaintext seed recovery (different class: stream ciphers, not classical substitution).
- `ctf-forensics` — broader encoded-blob capture work; overlaps on "decode encrypted blob" but this skill is the classical-cipher-specific playbook.
