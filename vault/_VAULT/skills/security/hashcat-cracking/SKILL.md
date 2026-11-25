---
name: hashcat-cracking
description: "Offline password/hash cracking with hashcat — picking the correct mode, handling algorithms the system binary lacks (Argon2 / scrypt / bcrypt variants), building wordlists, mask attacks, and validating the pipeline before long bruteforce jobs. Use when a challenge or engagement hands you a hash to crack (Argon2id, scrypt, bcrypt, SHA, NTLM, etc.) and asks for Hashcat."
sources: ctf7_ctf, hashcat_docs
report_count: 0
---

# HASHCAT-CRACKING — mode selection, gaps, and validation

## First rule: identify the algorithm BEFORE picking a mode
The hash prefix tells you the mode. Do NOT guess. Common CTF prefixes:
- `$argon2id$...` / `$argon2i$...` / `$argon2d$...` → **mode 70000** (Argon2id bridged) or **34000** (generic Argon2). Use 70000 for argon2id.
- `$scrypt$...` → **8900**. Do NOT confuse with Argon2 — `$argon2id$` is NOT scrypt.
- `$2y$` `$2b$` `$2a$` → bcrypt (**3200**).
- `$1$` MD5 crypt, `$5$` SHA-256 crypt, `$6$` SHA-512 crypt.
- `$pbkdf2$`, `$dynamic_...`, raw MD5/SHA → many modes; `hashcat --help | grep -i <algo>`.

### Gotcha: system hashcat (6.2.6) often LACKS modern modes
- Debian/Parrot hashcat 6.2.6 has **no Argon2 support**. Mode 70000/34000, and even 8900 scrypt, are absent or behave differently.
- Fix: install **hashcat 7.1.1** (precompiled `.7z` from hashcat.net):
  ```bash
  curl -sL -o /tmp/hc.7z https://hashcat.net/files/hashcat-7.1.1.7z
  7z x -y -o/tmp/hashcat71 /tmp/hc.7z
  /tmp/hashcat71/hashcat-7.1.1/hashcat.bin --version
  ```
  (GitHub releases also host the `.7z`; the `.tar.gz` asset may 404/redirect — prefer the hashcat.net `.7z`.) A patched/forked 6.2.6 build (e.g. with scrypt) exists in some distros but treat 6.2.6 as "no Argon2" by default.

### Wrong-mode symptom
`Hashfile '...' on line 1 (...): Separator unmatched` / `No hashes loaded` → you used the wrong `-m`. For `$argon2id$` that means you picked 8900 (scrypt) by mistake. Switch to 70000.

## Speed reality check (CPU-only OpenCL / POCL)
On a CPU-only box (no GPU, pocl), Argon2 is VERY slow — ~17–19 H/s for mode 70000 with t=3,m=65536,p=4. Plan keyspaces accordingly:
- 18k-word list ≈ 16 min.
- 26^4 lowercase mask (456,976) ≈ 7 hours.
- 36^4 (lower+digits, 1.68M) ≈ 24+ hours — usually infeasible; prefer wordlists.
- Mode 34000 benchmarks SLOWER than 70000 on CPU — prefer 70000 for argon2id.

## Validate the pipeline BEFORE a long bruteforce
A 7-hour job that's silently broken wastes the day. Prove the chain end-to-end with a known password first:
```python
# python3 -c 'pip install argon2-cffi'  (if missing)
import argon2, base64
salt = base64.b64decode("i/eOmAF+Qg40JHQAt4J/2A" + "==")   # salt from target hash
h = argon2.low_level.hash_secret(b"test", salt,
        time_cost=3, memory_cost=65536, parallelism=4, hash_len=32, type=argon2.Type.ID)
open("/tmp/verify.hash","w").write(h.decode()+"\n")
open("/tmp/verify.wl","w").write("test\nzzzz\n")
```
```bash
./hashcat.bin -m 70000 -a 0 -D 1 --force -w 3 /tmp/verify.hash /tmp/verify.wl --potfile-disable
# expect: "...:test" and Status: Cracked
```
If "test" cracks, your mode/params/salt handling are correct and a later Exhausted=0 genuinely means "not in wordlist."

## Wordlist strategy (challenge said "generate a wordlist")
1. rockyou 4-char subset (most CTF 4-char passwords live here):
   ```bash
   gunzip -k -c /usr/share/wordlists/rockyou.txt.gz > /tmp/rockyou.txt
   LC_ALL=C awk 'length($0)==4' /tmp/rockyou.txt > /tmp/wl_4char.txt
   ```
   (`LC_ALL=C` avoids the awk "Invalid multibyte data" warning dropping entries.)
2. Augment with dictionary 4-letter words, seclists common passwords, all 4-digit PINs (`seq -w 0000 9999`), keyboard walks (`qwer`, `asdf`), and case/Title/UPPER variants. Combine + `sort -u`.
3. If those exhaust at 0 recovered, the password is likely random → mask attack:
   - `?l?l?l?l` (lowercase, 456,976) is the first mask to try for a "word"-format flag.
   - Use a **persistent potfile** (`--potfile-path /tmp/hc.pot` without `--potfile-disable`) so an interrupted job can `--restore` instead of restarting.

## Resilience tips
- Write the target hash to a file with `printf '%s' '<hash>'` (no trailing newline) so `open()`/hashcat parse it cleanly.
- Background long jobs with `notify_on_complete=true`; they ping you on finish.
- If `/tmp` is wiped (container restart / session reset), ALL of: the hash, wordlists, and the hashcat binary disappear — rebuild before assuming the job died. Recreate `target.hash`, re-extract rockyou, re-fetch hashcat.
- `--force` is needed on pocl CPU (warns about unsafe but works); keep it, but never report hashcat bugs encountered under `--force`.

## Validation discipline (reporting)
- "Exhausted, 0 recovered" after a validated pipeline = the candidate set is wrong, not the tool. Expand the wordlist / widen the mask; do not re-run the same list.
- A cracked line is `hash:password`. Verify the plaintext independently (e.g. argon2-cffi re-hash) before submitting as a flag.
