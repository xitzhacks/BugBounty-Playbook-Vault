# SENTINEL-style LLM-agent canary-exfil (CTF7 Blackglass, port 8081)

## What it is
A challenge-hosted "assistant"/chatbot (here: SENTINEL, a "deployment assistant") that holds a
canary token (the flag). It is hardened against DIRECT disclosure: it will not print, spell,
encode, translate, split, or wrap the secret in output. The brief teases the intended path:
"Saying a secret is not the only way to move one."

## Mechanics discovered (client `app.js` event map = ground truth for the server mechanics)
- `unlocked`  -> "operator tool group disclosed"  (a second tool set unlocks)
- `exfil`     -> "macro expanded . query emitted to external resolver"  <- THE SIDE CHANNEL
- `refused_plaintext` -> "plaintext canary in outbound name"  (refused if canary appears in
  plaintext in the outbound query name)
- `refused_secret`    -> "direct disclosure"  (refused if you ask it to print/encode the secret)

Base tools: `system_time()`, `uuid_gen()`, `calc(expr)`, `service_status(region)` (only 4 canned
regions — NO injection there). API: `POST /api/chat` `{message}` -> `{reply, tool, event,
unlocked}`.

## Exploit shape (plan, do not brute)
1. Trigger the OPERATOR unlock (a benign phrase — the failing keyword attempts returned empty/500,
   so the trigger is likely natural-language, like the base tools). Once `unlocked=true`, the
   operator tool group (incl. a macro/expand + external-resolver tool) is disclosed.
2. Trigger a MACRO expansion that emits a resolver query. Reference the canary by ROLE ("the
   deployment canary"/"the token") — NOT by spelling it — so the `refused_plaintext` gate doesn't
   fire. The macro expands and moves the canary to the outbound query.
3. CAPTURE: the intended capture is the ENCODED canary surfacing in the chat response JSON itself
   (e.g. `tool.note` / `tool.args` showing the resolver query with a hex/base64 canary). Scan the
   FULL response for `BI{...}` and for base64/hex blobs that decode to `BI{`. If it really egresses
   to a network resolver, you need a reachable listener (see capture caveats below).

## Capture caveats (important — know your egress)
- If the canary appears in the `/api/chat` JSON response (tool note/args), NO external egress is
  needed: just parse the response. This was the assumed-correct path for SENTINEL.
- If the resolver query is a REAL network call, capturing it requires either (a) an internal host
  you can read via the same SSRF sink (decimal-IP 2886795265 = 172.1.16.1 gateway), or (b) a
  public DNS/HTTP listener you control. Worker/agent boxes with NO external egress and NO public
  IP CANNOT capture a real outbound exfil — so prefer the in-response-JSON path first.

## Flaky-infra watcher pattern (CTF7 hosts drop to "000" / empty body)
Run a background loop that polls the host; when it returns 200, auto-fire the probe. Example:
```bash
cat > sentinel_watch.sh <<'SH'
#!/bin/bash
while true; do
  code=$(curl -s -o /dev/null -w "%{http_code}" --max-time 8 http://<host>:<port>/ 2>/dev/null)
  if [ "$code" = "200" ]; then
    echo "UP at $(date)" >> sentinel_watch.out
    python3 sentinel_exfil.py >> sentinel_watch.out 2>&1
    sleep 20
  else
    echo "$(date) down ($code)" >> sentinel_watch.out
    sleep 8
  fi
done
SH
```
Run with `terminal(background=true, notify_on_complete=false)` (long-lived watcher — correct for a
daemon). The probe script (`sentinel_exfil.py`) should: check base tool, try operator-unlock
candidates, try macro/expand triggers, and scan the full JSON for `BI{` + decoded base64/hex.

## Red-team value beyond CTF
This is the real-world "agent exfiltration" class: an LLM/agent with a tool that touches the
network (DNS lookup, fetch, resolver query) can leak secrets via an outbound request even when its
text output is filtered. Hardening must cover SIDE-CHANNEL egress (encode-then-exfil, DNS
exfiltration), not just output filtering. Pairs with `hunt-llm-ai` (tool-use exfiltration, ASCII
smuggling) and `ctf-ai-bot-exploit`.
