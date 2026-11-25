# Argon2 / scrypt / slow-KDF hashcat modes

## Mode table (the ones people mix up)
| Hash prefix | Correct hashcat mode | Notes |
|---|---|---|
| `$argon2id$v=19$m=...$...` | **70000** | Argon2id, bridged reference impl. FASTEST of the argon2 modes on CPU. Use this for CTF argon2id. |
| `$argon2i$...` / `$argon2d$...` | **34000** | Argon2 generic (pure OpenCL). Slower than 70000 here (~7 H/s in benchmark vs ~17 H/s). |
| `$scrypt$...` | **8900** | SCRYPT — NOT argon2. Feeding an argon2 hash here gives `Separator unmatched`. |
| `$2a$` / `$2b$` / `$2y$` | 3200 | bcrypt |
| `$1$` | 500 | md5crypt |
| `$5$` | 7400 | sha256crypt |
| `$6$` | 1800 | sha512crypt |
| raw MD5 | 0 | — |
| raw SHA1 | 100 | — |
| raw SHA256 | 1400 | — |
| raw SHA512 | 1700 | — |

## Identify an unknown hash
```
./hashcat.bin --example-hashes 2>/dev/null | grep -i argon2
./hashcat.bin --example-hashes 2>/dev/null | grep -i scrypt
```
Then match the prefix in the output's `Example.Hash` column.

## Benchmark reality (CPU OpenCL / pocl, 8-thread i5)
```
Hash-Mode 70000 (Argon2id [Bridged])  Speed: ~17 H/s   (CTF params m=65536,t=3,p=4)
Hash-Mode 34000 (Argon2)               Speed:  ~7 H/s   (Iterations: 12)
Hash-Mode 8900  (scrypt)               Speed: ~79 H/s   (but it is NOT argon2)
```
Takeaway: for argon2id, **70000 is the mode to use** and expect ~17–19 H/s. A 26^4 lowercase mask = 456,976 / 18 ≈ 25,400 s ≈ 7 hours.

## Copy-paste recipes
Generate a clean hash file (no BOM/CRLF, optional single trailing LF):
```
printf '%s\n' '$argon2id$v=19$m=65536,t=3,p=4$SALT$HASH' > target.hash
```

Wordlist attack:
```
./hashcat.bin -m 70000 -a 0 -D 1 --force -w 3 target.hash wl.txt -o cracked.txt
```

Mask attack (lowercase 4-char, ~7h on CPU):
```
./hashcat.bin -m 70000 -a 3 -D 1 --force -w 3 target.hash ?l?l?l?l -o cracked.txt
```

Resume / show result:
```
./hashcat.bin -m 70000 --show target.hash          # if not using --potfile-disable
```

## Why 8900 fails on an argon2 hash
hashcat expects scrypt's field layout (`$scrypt$ln$rf$p$binary$salt`). argon2's `$argon2id$v=19$m=65536,t=3,p=4$salt$hash` doesn't match that separator scheme, so the parser throws `Separator unmatched` / `No hashes loaded`. The fix is the MODE, not the file.
