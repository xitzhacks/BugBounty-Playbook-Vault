# LFI "path-tricks" filter diagnostic (CTF / web)

When a file-read endpoint (e.g. `GET /read?path=<file>`) blocks `/proc`, `/root`, `/app`
and you need to reach an env var or source file, do NOT spray 100+ encodings blindly.
Run a small diagnostic ladder to characterize the filter, then decide if the bypass
exists at all. Derived from the Blackglass/CTF7 `5004` "path-tricks" service, which
returned `403 "Nice try. Reading the reader would make this far too easy."` — a
deliberate design tell that the simple `/proc/self/environ` read is intentionally blocked.

## Diagnostic ladder (each step is ONE request; compare the exact response string)

1. **Baseline read works?** `?path=/etc/passwd` -> 200 with real contents proves the LFI
   is live and the filter is path-specific, not a global block.
2. **Absolute block?** `?path=/proc/self/environ` -> if `403 "Access to this file is
   restricted"` the filter catches normalized `/proc`. If `404` it's a real-missing-file
   (case/encoding mismatch), not a block.
3. **Raw-prefix vs normalized?** Send `//proc/self/environ`, `/./proc/self/environ`,
   `/proc/./self/environ`. If ALL return the same 403 as step 2, the filter normalizes
   (`normpath`) before checking. If a variant slips to a different code, you've found the
   normalization mismatch -- that's the bypass.
4. **Relative-prefix?** Send `proc/self/environ` and `./proc/self/environ`. If `403
   "Nice try..."` (not 404), the filter ALSO blocks the relative `proc/` prefix -- so
   `..` traversal alone won't reach `/proc` (the normalized path still contains `/proc`).
5. **`..` traversal works at all?** Send `../etc/passwd` -> 200 means raw-prefix check is
   bypassed by `..` but normpath re-introduces absolute blocks. Use this to read files
   outside the blocked prefixes (e.g. `/srv/app.py`, `/opt/server.py`, `/main.py`) --
   NOTE these are reachable ONLY if the app source is NOT under `/app/` (which is itself
   blocked). In Blackglass 5004, source was unreachable: every std location 404'd.
6. **Encoding?** Single + double URL-encode (`%2Fproc`, `%252Fproc`), `..%2f`, encoded
   `..` (`%2e%2e%2f`). If all 403, filter decodes before checking.
7. **Custom transport?** Path-based (`/read/proc/self/environ`), alternate endpoints
   (`/file`,`/view`,`/open`,`/get` with `?path=`), custom headers (`X-File`,`X-Path`),
   POST body `{"path":...}` (405 = body not consumed), symlink candidates at allowed
   dirs (`/tmp/environ`,`/run/environ`,`/dev/shm/environ`). All 404/blocked in Blackglass.

## STOP rule (the actual lesson)
If steps 1-7 all return the SAME block message for every `/proc`-containing variant, the
filter blocks the `proc` substring comprehensively and there is NO path-encoding bypass
on Linux (the only env path is `/proc/self/environ`). The challenge wants a DIFFERENT
trick (not a path encoding): read the app SOURCE to find the real mechanism, find the
secret/key elsewhere, or pivot to another service. "Reading the reader would make this
far too easy" = explicit confirmation the simple read is the deliberately-blocked path.
Do NOT fire variant 51. Report the wall + the diagnostic evidence, ask the user for the
intended vector. This pairs with the `bb-methodology` "variant-spray without mechanism
check" anti-pattern and the `hunt-jwt` Step 0.6 wrong-secret probe (same "one diagnostic,
then pivot" discipline).

## Flask/Werkzeug note
These services answer on `Werkzeug/Flask` dev server. The filter is app-level (not a
web-server rule), so it's a Python `if '/proc' in normpath(path): abort(403)` -- which is
why substring + normalized checks catch every encoding. There is no `file://` SSRF
shortcut (the worker HTTP client rejected `file://`), and container bind-mounts at
non-`/proc` paths (`/host/proc`) also 404'd (no such mount).
