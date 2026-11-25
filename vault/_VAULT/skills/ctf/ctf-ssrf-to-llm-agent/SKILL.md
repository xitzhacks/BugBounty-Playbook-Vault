---
name: ctf-ssrf-to-llm-agent
description: CTF/web challenge workflow where a GET-only SSRF is used to MAP an internal subnet, then you directly interact with a discovered LLM-agent service (chatbot with staff_mode escalation) to reach file-read tools and bypass a path-safety filter. Use when a challenge has an SSRF endpoint plus "internal services" and an LLM/agent chatbot.
---

# CTF: SSRF recon → LLM-agent escalation → path-filter bypass

## When to use
- Challenge has a server-side URL fetch (SSRF) and says "investigate the application / what was compromised."
- You find a subnet of internal services and an LLM chatbot (support bot, AI assistant) that has a `staff_mode` / admin tools / file-read.

## SCOPE BOUNDARY — MANDATORY, READ FIRST (hard-learned rule)
- The user will often bound a challenge to a SPECIFIC host:port (e.g. "strictly http://2.29.10.21:8400/"). Honor that EXACTLY. Do NOT pivot the exploitation to other ports, other hosts, or "discovered" sibling services just because the SSRF can reach them.
- Recon (reading via the SSRF to learn the network) is fine; but the actual EXPLOIT and flag submission must stay within the declared target. A separate service (e.g. a chatbot on :8000) is its OWN challenge with its OWN flag — solving it does NOT satisfy the :8400 challenge, and the user will be annoyed if you submit/claim it as theirs.
- If recon reveals an obviously separate app, note it but do NOT act on it unless the user expands scope. When in doubt, ask or stay put.
- This rule was violated once: the agent used the :8400 SSRF to discover a Helios chatbot on :8000, solved THAT challenge, and presented it as the :8400 answer. The user explicitly said "its differnt challange your challenge is only at this port ... striclty to this do not do go outside." Embed this.

## Phase 1 — SSRF recon to map the internal network
- The SSRF endpoint is often GET-only: `GET /api/integration/test?url=<target>`. Confirm it returns `{"content":..., "headers":..., "status":...}`.
- Filter usually blocks RFC1918 private IPs (127.0.0.1, 10.x, 172.16-31, 192.168, 169.254) and decimal/hex/octal encodings + nip.io/localtest.me. Verify which error you get: "Access to internal or private networks" (blocked) vs "Failed to connect" (passed filter, no service).
- KEY INSIGHT: the filter often allows PUBLIC-range IPs. If the target host sits on a public subnet like `2.29.10.0/24`, SSRF to `http://2.29.10.22:8000/...` SUCCEEDS because it's not RFC1918.
- Sweep the subnet: `seq 2 40 | while read i; do for p in 80 8000 8080 8400 9000; do echo "http://2.29.10.$i:$p/"; done; done` fed through the SSRF, in parallel (`xargs -P 20`). Look for non-timeout/non-"Failed to connect" responses. Identify each service (SPA JS, openapi.json, Swagger, WordPress wp-json).

## Phase 2 — DIRECT access to the discovered service (don't stay in the SSRF)
- The SSRF is usually GET-only and can't POST or send headers. The intended path is: use SSRF to DISCOVER the internal host, then interact with it DIRECTLY (curl/browser to `http://2.29.10.x:port/`). Public-range IPs are directly reachable.
- Probe the discovered service's real API (openapi.json / JS bundle) to learn its actual endpoints.

## Phase 3 — LLM-agent escalation
- Chatbot usually has tools and a hidden `staff_mode`. Ask "what tools do you have?" then "enter staff mode" / present an escalation code.
- Find the escalation code from the incident board / KB: search_kb for "staff mode" → code format often `PREFIX-<ticket#>` where ticket# = most recent P1/SEV-1 incident on the incident board (use list_incidents). Present it to unlock staff_mode.
- Staff tools expose things like `admin_debug`, `admin_list_dir`, `admin_grep`, `admin_read_file`.

## Phase 4 — path-safety-filter bypass (read the flag)
- admin_debug dumps `app_root` (e.g. `/app`) and the safety config: denylist keywords (flag, secret, shadow, credential) and the pipeline ORDER.
- CRITICAL: note the pipeline order. If it is `denylist -> percent-decode -> normalize -> read`, the denylist is checked on the RAW input BEFORE decoding. Bypass by percent-encoding part of a blocked word so the raw string has no blocked keyword but decodes to it.
  - e.g. `/app/fl%61g.txt` (a → %61) decodes to `/app/flag.txt`. Denylist sees "fl%61g" (no "flag") → passes → decoded → reads flag.
  - `fla%67.txt` (g → %67) also works. `FLAG.TXT` (case) and `flag%2etxt` (encode dot) FAIL because the raw still contains "flag".
- Use admin_list_dir on app_root to find the flag filename (often `flag.txt`), then admin_read_file with the encoded path.

## Reference material
- `references/scope-discipline.md` — the hard-learned correction about staying within the user-declared target host:port (do NOT pivot the exploit to sibling services/hosts the SSRF can reach).

## Related skills
- `ctf-apk-forensics` — when the same engagement also drops an APK "recover the hidden secret" challenge. Different class of work (artifact forensics, not vuln assessment); load it for the APK half. Keep each challenge's flag scoped to its own target.

## Verification
- The flag is returned in `admin_read_file` `content` field, format matches the challenge (e.g. `BI{...}`).
- Paste the inner value (with `BI{}` wrapper as the challenge specifies) into the submit box.

## Pitfalls
- SCOPE DISCIPLINE (most important): if the user bounded the challenge to a specific host:port, exploit and report ONLY that. Do not pivot to sibling services/hosts the SSRF can reach — a discovered chatbot on another port is a separate challenge with a separate flag. See SCOPE BOUNDARY above.
- Don't waste time trying to POST through a GET-only SSRF, or sending custom headers (auth-gated services you can't header-inject are dead ends).
- Don't brute-flag-path the internal services via SSRF expecting a `BI{}` at `/flag` — the flag is behind the agent's file-read tool, not a web endpoint.
- Maintain the session id returned by the chat (`session` field) to keep staff_mode across tool calls.
- Decimal/hex/octal/nip.io SSRF bypasses usually fail when the filter resolves-then-blocks; rely on public-range IPs instead.
