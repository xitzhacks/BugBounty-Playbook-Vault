# Wordlist generation — locale silently drops candidates

## The trap
When building a candidate wordlist on a system with a UTF-8 locale (the Parrot/Kali default), commands like:

```bash
awk 'length($0)==4' rockyou.txt > wl.txt
grep -E '^.{4}$' rockyou.txt > wl.txt
```

emit errors like `awk: warning: Invalid multibyte data` (or silently) and can **skip valid ASCII entries**. In a CTF7 Argon2 4-char crack, a 4-char subset built under the default locale had to be regenerated to be trustworthy.

## The fix
Force the C locale so `length()`/`grep` operate on raw bytes and keep every ASCII line:

```bash
LC_ALL=C awk 'length($0)==4' rockyou.txt > wl.txt
LC_ALL=C grep -E '^[[:print:]]{4}$' rockyou.txt > wl.txt
```

## Why it matters for a slow KDF
Argon2id on CPU OpenCL runs at ~17 H/s. A 20k-wordlist run already takes ~17 min; if the locale silently dropped the *correct* candidate, you burn that whole run (and any 7-hour mask fallback) on a deficient wordlist. Always build with `LC_ALL=C` and `wc -l` the result to sanity-check the count.

## Other wordlist hygiene
- Extract rockyou to a writable dir (often `/usr/share/wordlists` is root-owned): `gunzip -k /usr/share/wordlists/rockyou.txt.gz -c > /tmp/rockyou.txt`.
- Dedupe before a long run: `sort -u in.txt > out.txt`.
- For a 4-char password, layer: rockyou 4-char + `/usr/share/dict/words` 4-letter + seclists common + 4-digit PINs (`seq -w 0000 9999`) + keyboard walks + case/title variants. If all exhaust, escalate to a mask (`?l?l?l?l`) as a background job.
- **Race condition:** generate the wordlist in a separate command and confirm it has lines BEFORE launching hashcat — launching in the same turn can start the attack before the file exists (`No such file or directory`).
