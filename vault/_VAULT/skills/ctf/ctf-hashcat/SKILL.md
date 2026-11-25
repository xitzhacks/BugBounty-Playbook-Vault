---
name: ctf-hashcat
description: Crack password hashes for CTF / wargame challenges with hashcat — mode identification (especially Argon2id / Argon2 / scrypt / bcrypt), version pitfalls, slow-KDF speed reality, wordlist generation, and pipeline-validation before long jobs. Use when a challenge hands you a hashed password (Argon2, bcrypt, scrypt, md5crypt/sha256crypt/sha512crypt, MD5/SHA) and says "crack it with hashcat" or "generate a wordlist and recover the password".
---

# CTF Hashcat — Password Cracking

## When to use
A challenge gives you a hash (or hash file) and asks you to recover the plaintext password. This skill covers all hashcat modes but focuses on the slow KDFs (Argon2, scrypt, bcrypt) where the easy mis-steps live, and on the discipline of *validating the toolchain before burning hours on a bruteforce*.

## Critical mode-number traps (easy to get wrong)
- `$argon2id$...`, `$argon2i$...`, `$argon2d$...` → **mode 70000** (Argon2id bridged reference impl) or **34000** (Argon2 generic). Use **70000** for an `argon2id` hash.
- Mode **8900 is SCRYPT, not Argon2.** Feeding an argon2 hash to `-m 8900` produces the confusing `Separator unmatched` / `No hashes loaded` error. That error almost always means **WRONG MODE**, not a malformed file.
- bcrypt `$2a$` / `$2b$` / `$2y$` → 3200.
- md5crypt `$1$` → 500, sha256crypt `$5$` → 7400, sha512crypt `$6$` → 1800.
- Unsure of the mode? `./hashcat.bin --example-hashes 2>/dev/null | grep -i <prefix>` (e.g. `argon2`).

## Version pitfall
- hashcat **6.2.6** (many distro packages) does **NOT** support Argon2 at all (mode 70000 landed in 7.x). Symptom: `hashcat --help` shows no argon2 entry, and `-m 8900` is labeled "scrypt".
- Fix: download a 7.x release tarball/7z from `github.com/hashcat/hashcat/releases` (e.g. `v7.1.1`, the `.7z`), extract with `7z x hashcat.7z`, and run the binary `./hashcat.bin` from inside the extracted dir (the launcher is `hashcat.bin`, not `hashcat`).
- CPU OpenCL works headless via `pocl` — no GPU required. Confirm a device with `./hashcat.bin -I`.

## Speed reality (plan the attack before launching)
Argon2id with typical CTF params (`m=65536,t=3,p=4`) on CPU OpenCL runs at only **~17–19 H/s** (H = passwords/sec here). Consequences:
- A ~20k-candidate 4-char wordlist ≈ 17 min.
- Full lowercase mask `?l?l?l?l` (26^4 = 456,976) ≈ **7 hours**.
- Wider charsets (`?l?d?l?l`, `?a?l?l?l`, mixed-case+digits) explode into days — not viable on CPU.
- Therefore **prefer WORDLIST attacks**: generate a tight candidate set first, only fall back to a mask as a long background job.

## Workflow
1. Identify the hash prefix → pick the mode (table above). Re-check the prefix if you see `Separator unmatched`.
2. Write the hash file cleanly: `printf '%s' '<hash>' > target.hash` (a single trailing LF is fine; ensure no BOM / CRLF).
3. Generate a wordlist:
   - rockyou 4-char: `gunzip -k /usr/share/wordlists/rockyou.txt.gz -c > /tmp/rockyou.txt; awk 'length($0)==4' /tmp/rockyou.txt > wl.txt` (awk multibyte-locale warnings are harmless for ASCII; regex `^.{4}$` also works).
   - layer in: dictionary 4-letter words (`/usr/share/dict/words` filtered to `^[a-zA-Z]{4}$`), seclists common passwords (`/usr/share/seclists/Passwords/Common-Credentials/*`), PINs `seq -w 0000 9999`, keyboard walks (`qwer,asdf,zxcv`...), and case/title variants of dictionary words.
   - dedupe: `sort -u in.txt > out.txt`.
4. **Validate the pipeline before any long job** (see `scripts/verify_pipeline.py` and `references/argon2-modes.md`): generate a known hash of `"test"` with the *exact same salt/params* as the target via `argon2.low_level.hash_secret`, then confirm hashcat cracks it. This proves mode + salt + params are correct so you don't burn hours on a broken setup.
5. Run: `./hashcat.bin -m 70000 -a 0 -D 1 --force -w 3 target.hash wl.txt -o cracked.txt`. `-D 1` = CPU, `-w 3` = max performance.
6. If the wordlist exhausts with `Recovered: 0/1`: escalate to a mask (`-a 3 ?l?l?l?l`) as a background job with `notify_on_complete=true`, or widen the charset only if time budget allows.

## Pitfalls
- `Separator unmatched` = wrong hash mode (most often 8900 used for an argon2 hash). Re-check the prefix, don't re-edit the file.
- `--force` bypasses the "not a real GPU" warning so hashcat runs on CPU OpenCL; it's safe here but hides genuine errors, so validate the pipeline separately first.
- The progress bar uses carriage returns and won't appear in captured logs; trust the final summary lines `Recovered:` and `Status: Exhausted|Cracked`.
- Background long jobs with `terminal(background=true)` + `notify_on_complete=true`; a 7-hour mask will never finish inside a foreground call.
- Race condition: if you generate the wordlist in the same turn you launch the attack, the attack can start before the file exists (`No such file or directory`). Build the wordlist in a separate command, confirm it has lines, then launch.
- **Persistence on restart:** a long mask job (e.g. 7-hour `?l?l?l?l`) can be **wiped if its working dir is ephemeral** (`/tmp` is cleared on a session/container restart — observed: target.hash, wordlists, and even the hashcat binary vanished, forcing a full rebuild from the hash string and a fresh 7.x download). Mitigations: (a) keep the hash, wordlist, potfile, and `hashcat.bin` in a **persistent** directory (e.g. `~/ctf7/`), not `/tmp`; (b) always use a **potfile** (`--potfile-path=...` or default) so a killed/resumed job doesn't restart from zero — re-run with the same args and hashcat skips already-tried candidates via the potfile; (c) save the target hash string and the exact hashcat download URL in your notes so a rebuild is one copy-paste. For a 7-hour job, prefer `--potfile-disable` ONLY for validation runs, never for the production bruteforce.

## Support files
- `references/argon2-modes.md` — full mode table, example hashes, benchmark comparison (70000 vs 34000), and copy-paste command recipes.
- `scripts/verify_pipeline.py` — parse a target argon2 hash, mint a `"test"` hash with identical salt/params, and run hashcat to prove the mode/salt/params are correct before a long crack.
