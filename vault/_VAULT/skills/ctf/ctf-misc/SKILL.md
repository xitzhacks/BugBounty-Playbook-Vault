---
name: ctf-misc
description: "Misc-category CTF challenges. Two sub-classes: (A) misaligned terminal-capture ASCII art (Tiranga / national flag in box-drawing + slash glyphs, hidden letters, wrapped at the wrong size realignment). (B) NON-HTTP custom line-protocol / raw-socket services (banner grab, case-sensitive verb discovery via 4xx codes, auth-bypass recon, chained-web-app pivots via .js.map leaks). Load when a CTF hands you a terminal capture .txt that needs to be realigned, OR a legacy network service / port that curl treats as HTTP/0.9 or returns empty and you must reverse its protocol over a raw socket."
---

# CTF Misc — Terminal-capture ASCII-art misalignment

## When to load
- A "misc" challenge gives a zip whose main artifact is a **terminal capture dump** (`.txt` with `N|content`-style rows, status comments, and ASCII art built from `/ \ - + > v ? = , . : ;` glyphs).
- The brief mentions a flag/art that is "still there" but the "output needs to be realigned" / "wrapped at the wrong size" / "your terminal is telling the truth badly".
- Theme is a flag drawn in art (Tiranga = saffron / white / green bands + chakra; other flags similar).
- The zip may ALSO contain a large **decoy subdirectory** (e.g. `Intercepted ... SMS/` with thousands of fake GSM/SMS log lines). That is noise — the answer is in the art file. (Generic decoy-log handling lives in `ctf-forensics`.)
- (Sub-class B) A "misc" / "legacy network service" challenge gives a URL or port where `curl` returns an **empty body** and complains `Received HTTP/0.9 when not allowed`, OR where every path returns the same `401`/`403` and no verb list is given. This is a **custom line protocol over TCP**, not HTTP. Reverse it with a raw socket (see below).

## Workflow
1. **Extract & triage.** `unzip`, then `find` the real artifact. Ignore huge decoy folders. The real capture is usually a single `.txt` with a regular `N|...` row format.
2. **Parse the capture.** Split each line on `^\s*(\d+)\|(.*)$`. Lines starting with `#` (e.g. `# redraw jitter 07: ignore this terminal status line`, `# --- END CAPTURE ---`) are status/comment markers — strip them; they are explicit "ignore me" hints, not data.
3. **Render to inspect.** Build a monochrome bitmap: non-space char → black pixel, space → white. Save as PNG. To use `vision_analyze` reliably, **downscale to ≤ ~160px wide first** (a tiny 160×24 or 194×120 view is enough for shape recognition and avoids request timeouts on large renders).
4. **Identify the art & its bands.** A Tiranga here = top band of `/ \` diagonals, middle (white) band containing a chakra (dense `? = , . : ;` glyph cluster = the wheel), bottom (green) band. Letters are embedded in the white and green bands.
5. **Locate embedded letters.** Scan for alphanumerics and record `(row, col, char)`. In slash-glyph art letters appear as `/X/` tokens (e.g. `/U/`, `/N/`, `/I/`, `/6/`, `/4/`); in the chakra band they appear as isolated `I`/`i`/`l` among `?=,.:;` noise. Verify ambiguous glyphs by context (I/l/1, N/M).
6. **Realign.** "Wrapped at the wrong size" ⇒ the art was captured at a terminal width that broke it. Two recovery shapes:
   - **Deshear (parallelogram slant).** If the art reads as a shape skewed down-to-the-right, shift each row `r` left by `round(slope*r) mod W` for slope ≈ 0.3–0.6, then re-extract letters in column order.
   - **Unwrap (line-wrap).** If the original lines were wider than the terminal, each logical line became 2+ physical rows. Join consecutive physical rows (try joining pairs → width ≈ 2×observed, i.e. ~194 for ~97-wide rows) and re-render.
   Test both; the correct one yields letters reading left-to-right as the flag.
7. **Assemble & verify.** Concatenate the realigned letters in corrected order. Match against the known flag wrapper (e.g. `TRIVARNA{...}`, `uni6ctf{...}`, `flag{...}`); if the platform demands a fixed wrapper, re-wrap the inner.

## Pitfalls
- **Reading-order extraction is wrong when sheared.** Naively concatenating alphanumerics top-to-bottom gives garbage (e.g. `vvvvvvvvvvvvUnNdIi64...`); you must realign first.
- **Decoy subdirectories** (fake SMS/GSM logs, huge config dumps) are ~99% noise by design — don't parse them; the flag is in the art file.
- **Status/comment lines** (`# redraw jitter ...`) are explicit skip markers — don't treat them as data.
- **Glyph confusion:** `I` vs `l` vs `1`, `N` vs `M` are easy to mix in slash art — confirm via the surrounding `/X/` token or neighboring context.
- **Vision timeouts:** large rendered PNGs make `vision_analyze` time out. Render a small (≤160px wide) version for shape questions; do exact letter extraction in code (positions), not via vision.
- **Don't over-invest in adjacent decoys:** a second file in the zip that looks "interesting" (SMS logs, routing tables) is usually a distractor.

## Sub-class B — custom line-protocol / raw-socket service recon
1. **Detect non-HTTP.** `curl -s -i http://host:port/` returns nothing or `Received HTTP/0.9 when not allowed` ⇒ it is a line protocol. Use a raw Python socket (`socket.socket()`, never `/dev/tcp` redirection — the agent safety layer blocks it). Connect, read the banner (e.g. `200 broken-protocol/1.0 ready`), then send each candidate verb as a `verb\r\n` line.
2. **Map verbs by 4xx code.** Send one verb per line; the reply discriminates:
   - `<verb> ...` → `401 not authenticated` / `403 auth rejected` ⇒ the verb EXISTS (needs auth / bad cred).
   - `<verb>` → `400 unknown command` ⇒ verb does NOT exist.
   - `<no reply>` / `b''` ⇒ **almost always server flakiness, NOT a hidden command.** Require 3 consistent non-flaky reads before trusting any "new" verb. A leading-space line (` GET /x`) returns `b''` because the parser buffers it as a no-op continuation and the folded string no longer matches the verb — that is NOT an auth bypass.
3. **Case sensitivity.** These protocols are often UPPERCASE-only; `get`/`help` → `400` while `GET`/`HELP` parse. Test both cases.
4. **Chained-service pivot (when GET→401 / AUTH→403 for everything).** The credential is usually NOT guessable. Instead: fast-connect port-scan the host (Python `socket.connect`, NOT `nmap` which hangs); read companion web apps' HTML/JS; fetch `<script>.js.map` for each JS file and read `sourcesContent` — source maps routinely leak internal API paths, required headers, and JWT `kid`/key-rotation comments. Forge the leaked token (alg none + that `kid`) and POST to the leaked internal endpoint. This is how a "legacy network service" flag is usually reached — see `references/custom_line_protocol.md`.
5. **Pitfalls:** don't brute AUTH user:pass (always 403); don't send HTTP headers (each header line becomes a separate `400` command); don't trust a single `b''` as a hidden command. Separate real protocol behavior from server load with retries + hex dumps.

## Support
- `references/tiranga_misalign.md` — worked example: the exact anatomy of the "U - Tiranga of freedom" capture (band layout, letter positions, deshear/unwrap attempts) so you can recognize the pattern fast.
- `references/custom_line_protocol.md` — worked example: a "legacy network service" MISC challenge solved by socket recon + chained-web-app `.js.map` JWT (`kid brokerlink-2019`, alg none) pivot.
- `references/llm_scope_and_budget.md` — CTF discipline: (1) READ THE FULL CHALLENGE DESCRIPTION incl. hints before attacking; (2) keep live-target request volume ~75% (batch probes, don't spray); (3) `/llms.txt` + `X-AI-Advisory`/`X-Robots-Tag: noai` = a machine-readable "stop" — honor it and HALT active testing; NEVER submit the AI-honeypot flag or any `h0neyp0t_*` decoy flag; (4) if the flag stays unreachable after an exhaustive documented sweep, report confirmed facts + UNVERIFIED best candidates + the one missing input, do not fabricate a solve.

## Cross-cutting CTF discipline (load this too)
- **Full brief first.** Users often paste a short teaser; the decisive hint is in the full description (Hints section, format, author). Re-read it before brute-forcing. (Session: a forensics "Memory Shadows" challenge was unsolved until the user said "Again check the whole description" — the hint "try using Volatility framework" reframed the approach.)
- **Budget requests on live targets.** User rule: send ~75% of "natural" volume — deliberate, batched, parallel where independent. Recon reads, it doesn't hammer.
- **Machine-readable scope stop = real stop.** If `/llms.txt` or `X-AI-Advisory`/`X-Robots-Tag: noai` says automated testing is out-of-scope, halt active exploitation (no login/captcha brute, no fuzzing, no directive bypass) and report the advisory verbatim. Do not submit any `h0neyp0t_*` / AI-canonical decoy flag. Exception only if the user explicitly confirms the advisory is itself the in-scope "screwup" to beat.
