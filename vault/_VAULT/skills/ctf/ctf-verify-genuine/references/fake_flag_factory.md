# Reference: CTF7 "Fake Flag Factory" — full reverse-engineering attempt

## Setup
- Zip `challenge_hIIbswM.zip` contains `challenge/unit_NNNN.dat` (1000 files) + macOS metadata (`__MACOSX/`).
- Each `unit_NNNN.dat`:
  ```
  Fake Flag Factory :: assembly line
  unit_id: 833
  nonce: 2ddde235
  stamp: BI{f9fc22c5308aa5268112bc8a}
  notes: recycled housing
  notes: this one is definitely real, trust me
  ```
- Fields present: `unit_id` (all), `nonce` (all, 8 hex chars), `stamp: BI{<24 hex>}` (696 units), plus optional `notes` (multi), `qc`, `batch`, `shift`, `operator`.
- Stamp = 24 hex = **12 bytes**.
- `qc` field distribution among stamped units: 147 `PASS`, 33 `FAIL`, 516 absent.
- Raw-byte check (`cat` + `od -b`): file bytes are exactly as parsed — no hidden fields, no separator/whitespace tricks. Only universal fields are `unit_id` + `nonce`.

## Hints -> strategy
1. "derived deterministically from metadata" -> stamp = f(unit metadata).
2. "reproduce the stamping process for every unit and compare" -> brute-force f over ALL units; the genuine one matches.
3. "byte order, direction, field representation" -> try each field as ASCII string / raw hex bytes / int BE(4) / int LE(4) / ASCII-of-hex-string(8B) / hex-string-reversed; reverse or word-swap the digest; try different output slices.

## Exhaustive search performed (ALL 696 stamped units scored)
- Hashes: md5, sha1, sha256, sha512, blake2b.
- Field reps: nonce/uid as ASCII, raw hex bytes, BE/LE 2-byte, BE/LE 4-byte, decimal string, reversed bytes, ASCII-of-hex-string, hex-string-reversed.
- Field combos: single, double, triple (incl. batch/shift/operator/qc/notes).
- Output: slices ([:12],[4:16],[8:20],[2:14],[6:18],...), byte-reverse, 4-byte word-swap.
- CRC32/CRC64/Adler over every struct layout.
- Text inputs: whole file minus stamp line, field lines in file order, sorted key=val, notes text, exact metadata strings with separators/newlines, form/URL/JSON templates.
- Combined-integer packing (u<<32|n, n<<32|u as 8B BE/LE; 12B with zero pad) × 5 hashes × 3 transforms.
- Arithmetic/bitwise construction: 12-byte stamp as 96-bit int; `nonce<<32|uid`, `uid<<32|nonce`, `nonce^uid`, `nonce+uid`, `nonce*uid` (mod 2^96), packed BE/LE with raw/rev/word-swap. ZERO matches.
- Structural embedding: `stamp[:4]==nonce_bytes`, `==nonce_rev`, `stamp contains nonce_bytes(any repr)`, `stamp XOR nonce==uid_bytes(any repr)`, `stamp contains uid_bytes`, `int(stamp)==(nonce<<k)|uid`. ZERO matches.
- Header/constant salt: `md5(salt+nonce)`/`(nonce+salt)` with salt = `b"Fake Flag Factory :: assembly line"`, `b"Fake Flag Factory"`, `b"assembly line"`, `b"fakeflagfactory"`, `b"BI"`, `b"challenge"`, `b"verification"`. ZERO matches.
- HMAC: 19 guessed keys (author/challenge name, "secret", etc.) × 5 hashes × 9 message encodings. ZERO matches.
- Planted-flag / wordlist: grepped all records for any `BI{...}` outside `stamp:` (none); tested any stamp == hash of common CTF word ("genuine","real","flag",challenge name,author). ZERO hits.

## RESULT: only ONE deterministic match in the entire dataset
`md5(nonce as RAW 4 bytes)[:12]` matched exactly one unit:
```
unit_0380:  nonce b57be44a
md5(bytes.fromhex("b57be44a")).digest()[:12] = 5147dccdc34d33223dac7cb2
printed stamp = BI{5147dccdc34d33223dac7cb2}   <- MATCH (unique)
```

## CRITICAL: this match was a PLANTED DECOY, not the genuine stamp
- unit_0380 is flagged **qc: FAIL** (the genuine unit should not be a failed-QC item).
- The platform REJECTED `BI{5147dccdc34d33223dac7cb2}` as the flag.
- If the challenge generator had used `md5(nonce)[:12]` for the fakes, we would expect ~hundreds of matches; instead we saw exactly ONE. So 0380 is the *lone* unit satisfying the "obvious" formula, planted to trap solvers who stop at the first unique match.
- **Fake-generator pre-scan (decisive):** scored every single/double-field hash formula by match COUNT. `NO formula matched >=5 units` (best was 1). => the 695 fake stamps are **independent noise**, not produced by a shared generator. There is NO generator to invert; the genuine item cannot be reached by hashing metadata. (Script: `scripts/fakegen_scan.py` — run FIRST next time.)
- KEY EVIDENCE the genuine derivation was NOT found: all 147 `qc:PASS` units have high-entropy stamps with NO correlation to any metadata hash in the entire search space above. The genuine algorithm therefore uses something not enumerable from the visible metadata (e.g. a server-side secret/salt), OR the genuine item is identified by a property other than recomputing its stamp.

## Lesson (do NOT repeat)
- **A unique match is necessary but NOT sufficient.** When the single match has a contradictory marker (here: qc:FAIL) AND the platform rejects it, treat it as a decoy and keep hunting, or pivot to asking what the "verification process" actually is.
- Don't present a unique-match value as "the flag" without cross-checking it against the challenge's own validity signals (qc status, submission acceptance).
- The notes social-engineering lines ("this one is definitely real, trust me") are uniformly distributed across fakes — ignore them either way.

## What solved (and what didn't)
- SOLVED: the file format, field extraction, and a complete, reproducible scoring harness (`scripts/brute_stamp.py`, `scripts/landscape_stamp.py`, `scripts/fakegen_scan.py`).
- NOT SOLVED: the genuine stamp derivation. Left OPEN because the only deterministic match was a decoy and no other candidate matched any unit's metadata.

## Rejection / recheck procedure (on "invalid flag")
1. Re-extract the archive cleanly (`unzip`) + re-parse; confirm archive md5 unchanged (rules out corruption). Also checksum any re-downloaded file — `challenge_hIIbswM (1).zip` was BYTE-IDENTICAL to the original (md5 `68c834fa...`), so re-solving reproduced the same decoy; always verify before re-running.
2. Re-run the FULL scoring landscape; print EVERY candidate matching exactly 1 record, with that record's `qc` status.
3. Dedicated PASS-only check: does any `qc: PASS` record match a deterministic formula?
4. Run `scripts/fakegen_scan.py` FIRST: if no formula matches >=5 units, fakes are noise — stop brute-forcing hashes and pivot to secret/structural/validity-marker, or ask the user for the challenge source.
5. Only call a value THE flag once the platform accepts it; otherwise report strongest candidate + decoy caveat and ask for the verification process.

## Python / CTF scripting gotchas
- `bytes ^ bytes` is illegal in Py3. XOR equal-length bytestrings: `(int.from_bytes(a,'big') ^ int.from_bytes(b,'big')).to_bytes(len(a),'big')`.
- Never name a script `struct.py` / `hashlib.py` etc. — it shadows the stdlib. Use `structscan.py`.
- Don't define a hash dict as `H(x): hashlib.md5(x).digest()` (runs at def time). Use `lambda x: hashlib.md5(x).digest()`; same for transforms `{'raw': lambda d: d}` not `{'raw': d}`.
- Background brute jobs: `terminal(background=true, notify_on_complete=true)` then wait/poll. A heredoc containing `&` (bitwise AND, e.g. `& 0xffffffff`) can trip the shell-backgrounding validator — rewrite as `% 0xffffffff`.
- Always score by `count==1` across ALL records and print the match's `qc` field immediately so a `FAIL` decoy is obvious.

## Definitive unresolved status
`BI{5147dccdc34d33223dac7cb2}` (unit_0380) remains the ONLY unit satisfying any deterministic formula, is `qc:FAIL`, and is rejected by the platform. The genuine stamp was NOT recovered; the challenge requires the author's actual stamping source/verifier (not shipped in the zip) to solve. Next time: start with `scripts/fakegen_scan.py` to confirm noise early, then ask the user for the challenge's `verify.py`/`generator.py` rather than re-brute-forcing the full hash space.
