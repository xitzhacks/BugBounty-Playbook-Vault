---
name: browser-isolation
description: Safe browser automation for security research and general web tasks. NEVER touch the user's logged-in browser. Always use an isolated throwaway profile. For this user, Firefox ONLY, never Chrome or Chromium. Covers the Marionette real-interaction technique, the browser-use and CDP auto-launch trap, and the rule to actually drive the app instead of only parsing source. Use whenever a task involves opening a website, viewing page source, clicking through an application, browser automation, or tools like browser-use, playwright, selenium, or geckodriver.
---

# Browser Isolation — safe browsing for research

## HARD RULES (non-negotiable for this user)
1. **Never use the user's default or logged-in browser profile.** Always launch a
   separate browser instance with a throwaway profile dir (e.g. /tmp/ff-iso for
   Firefox). Their Brave/Firefox login session must remain completely untouched —
   no shared profile, no shared CDP endpoint.
2. **Firefox ONLY. DO NOT OPEN CHROME OR CHROMIUM AT ALL.** This is an explicit,
   repeated user rule ("From now you use firefox, DO NOT OPEN CHROM AT ALL").
   Chrome-based tools (browser-use / browser-harness, Playwright Chromium) are
   OFF-LIMITS for live browsing. Use Firefox plus Marionette instead.
3. **Verify isolation before AND after** every browser action:
   ```
   echo "brave:  $(ps aux | grep '[b]rave' | wc -l)"
   echo "ff(mine):$(ps aux | grep '[f]irefox' | grep ff-iso | wc -l)"
   echo "chrome:  $(ps aux | grep '[c]hrome' | grep -v brave | wc -l)"  # must be 0
   ```
   Report to the user that their browser is untouched.

## Actually DRIVE the app, do not just parse source
User repeatedly rejected "I opened it and read the source" without real
interaction. When asked to "go through the application" or "interact with all
links", you MUST navigate and click in the real browser DOM, not just curl and
grep. A static page may have ZERO button elements, so enumerate anchors and
role=button, then actually click each one and read the resulting page.

## Technique — Firefox + Marionette (reliable scripted interaction)
Marionette is Firefox's native remote control. More reliable than computer_use
for scripted clicks on an isolated instance (cua-driver's app-name window
targeting failed on Wayland and returned 0 elements / 5x104).
```
# launch isolated Firefox with marionette (separate throwaway profile)
firefox --no-remote --new-instance --profile /tmp/ff-iso --no-sync --marionette 2828 about:blank &
# install driver (PEP668 env, use --break-system-packages)
pip3 install --break-system-packages marionette_driver
```
See references/marionette_walkthrough.py for a ready walkthrough that navigates to
a URL, enumerates interactive elements from the LIVE DOM, and clicks each link —
all inside the isolated instance.

## Verbose trap to avoid
Do NOT use browser-use or browser-harness for this user. Its CLI auto-launches
its own Chrome if it cannot find the CDP endpoint and prints a misleading
"Chrome isn't running, launching it / Allow remote debugging" message. That
fallback is what dragged in the user's browser and caused a serious complaint.
Even setting CDP_URL=http://127.0.0.1:9223 did NOT suppress the misleading
message (though it did connect to the isolated instance). Prefer Firefox plus
Marionette. If you ever must use browser-use, ALWAYS pass CDP_URL to a known
isolated Chrome AND verify no stray chrome spawned. But for this user, just use
Firefox. Do not install or run Chrome for browser tasks.

## Screenshot Capture for PoC Evidence

When capturing screenshots via Marionette for bug-bounty PoC evidence:

### save_screenshot() requires a file object, NOT a path string
```python
# WRONG — raises AttributeError: 'str' object has no attribute 'write'
m.save_screenshot("/tmp/shot.png")

# CORRECT — pass a file object
with open("/tmp/shot.png", "wb") as f:
    m.save_screenshot(f)
```

### Async fetch() in execute_script() returns None in headless context
Marionette's `execute_script()` does NOT await Promises. Async I/O (fetch,
XHR) inside `execute_script()` returns `None` because the script returns before
the Promise resolves.

**Workaround:** For proof of concept, use `curl` from terminal() for HTTP-level
verification. Use `execute_script()` only for synchronous DOM inspection
(getElementById, querySelector, etc.) or for injecting result text into the page
for screenshot display.

```python
# WRONG — returns None
result = m.execute_script("""
    (async () => {
        const r = await fetch('/api/test');
        return r.status;
    })()
""")

# CORRECT — synchronous DOM inspection
result = m.execute_script("""
    const el = document.querySelector('#result');
    return el ? el.textContent : 'NOT FOUND';
""")

# CORRECT — inject result text into page for screenshot
m.execute_script("""
    document.body.innerHTML = '<pre>Result: ' + someValue + '</pre>';
""")
m.save_screenshot(...)
```

### Session cleanup
```python
# WRONG — AttributeError: 'Marionette' object has no attribute 'close_session'
m.close_session()

# CORRECT
m.delete_session()
```

### Full PoC capture pattern
See references/marionette_poc_capture.py for a complete script that:
1. Launches isolated Firefox with Marionette
2. Navigates to target URLs
3. Captures full-page screenshots
4. Injects result text into page for evidence display
5. Cleans up session and process

## Capturing JS dialogs as proof (alert / confirm / prompt)

For an XSS PoC the dialog itself is the evidence — a screenshot of a static page proves nothing.
`switch_to_alert()` reads it directly:

```python
m.navigate(poc_url); time.sleep(3)
a = m.switch_to_alert()
print("DIALOG:", repr(a.text))   # e.g. '1'
a.accept()
```

- `m.title` (and most commands) raise `UnexpectedAlertOpen` while a dialog is open. That is not a
  failure — the exception message contains the dialog text, so it doubles as a fallback proof:
  `UnexpectedAlertOpen: Dialog text: TypeError: can't access property "y", self.x is undefined`.
- Reproduce twice before reporting; store both dialog texts + the sink's innerHTML.
- If `switch_to_alert()` raises `NoSuchAlertError`, the payload did not execute — check the sink
  HTML before touching the payload (attribute quoting/newline bugs look identical from outside).

## History hygiene ("don't save in history")

When the operator says not to leave traces: launch with `--private-window` on the throwaway
profile, then kill the process and `rm -rf` the profile directory. Verify with
`ls -d /tmp/ff-xxx` and report the wipe explicitly.

## Pitfalls
- computer_use app='Firefox' capture returned 0 elements / 5x104 on Wayland;
  cua-driver could not see the isolated window. Use Marionette for scripted work.
- A "find all buttons" request on a legacy static site yields 0 button tags;
  report the real interactive elements (anchor links) instead of claiming none.
- Always pass --no-sync --no-remote --new-instance so the isolated Firefox cannot
  attach to the user's running Firefox session.
- The harness "Chrome isn't running, launching it" line is misleading; treat it
  as a danger sign, not a status. Re-verify isolation when you see it.
- Marionette `save_screenshot()` takes a file object, not a path — passing a string
  raises AttributeError.
- Marionette `execute_script()` does NOT await Promises — async fetch() returns
  None. Use curl for HTTP-level proof, or inject results into DOM for screenshots.
- Marionette session cleanup is `delete_session()`, not `close_session()`.
- `--marionette-port N` is NOT reliably honoured. A launch with
  `--marionette --marionette-port 2829` bound the listener on the DEFAULT 2828, and the driver
  then died with `TimeoutError: Timed out waiting for connection on 127.0.0.1:2829`. Always
  confirm what actually bound before connecting (`ss -ltnp | grep -E '282[0-9]'`) and point the
  driver at that port. Cross-check `ps aux | grep '[f]irefox' | grep <your-profile-dir>` so you
  know the listening PID is YOUR throwaway instance and not the user's Firefox.
- `Marionette.set_script_timeout()` does not exist (AttributeError). Drop it — `navigate()` plus
  `time.sleep(load_wait)` covers SPA hydration; if you need a real cap use `m.timeout.script = 30`.
- **`execute_script()` returns `None` for EXPRESSION-form scripts — SILENTLY, with no exception.**
  Only a body with an explicit `return` yields a value:
  ```python
  m.execute_script("JSON.stringify({t:document.title})")        # -> None   (no error raised)
  m.execute_script("return JSON.stringify({t:document.title})") # -> '{"t":"..."}'
  ```
  This is the single most dangerous failure mode of a browser harness: every probe returns
  `None`, the loop's `if d.get("e")` is falsy, and you publish a clean "0 findings" sweep from
  a run that never inspected a single page. Defences: (a) always use `return`; (b) gate the
  loop on a pre-flight assertion — `assert m.execute_script("return 1+1") == 2` — and abort
  loudly if it fails; (c) when a run reports all-negative, re-probe ONE known-good page and
  confirm the harness can still see `document.title` before you believe the negative.
- **One Marionette session at a time.** While a harness script holds the session, a second
  `Marionette(port=...).start_session()` blocks then raises
  `TimeoutError: Timed out waiting for connection on 127.0.0.1:2828` — it reads as "the browser
  broke" when the browser is merely busy. Kill the holder (`pkill -f <harness>.py`), wait a
  couple of seconds, then attach a debug client. Never run two browser scripts concurrently
  against one instance.
- **Cloudflare-interstitial-aware navigation.** A nav landing on `<title>Just a moment...</title>`
  has not reached the app; the challenge self-solves in-browser within seconds. Poll the title
  until it clears (up to ~20-25 s) instead of a fixed `sleep`. A *persistent*
  `Attention Required! | Cloudflare` is a hard block — stop the run and report it as blocked
  (not as a negative result), and note that a brand-new profile may not clear it while plain
  HTTP on the same IP still returns 200 (block is fingerprint-scoped; see recon-pitfalls §11/§12).
- **`pkill -f <pattern>` can kill your own shell.** A command whose own command line contains the
  pattern (e.g. `pkill -9 -f 'profile /tmp/ff-xss'` inside a bash `-c` wrapper that also mentions
  `/tmp/ff-xss`) matches itself; the shell dies with SIGKILL and everything queued after it —
  including the `rm -rf` of the profile — never runs. Kill by PID from
  `ps -eo pid,cmd | grep '[f]irefox' | grep <profile>` instead, and verify afterwards with
  `pgrep -c firefox` plus a `ps` check. Note that `pgrep -f <pattern>` in a follow-up command
  also matches *that* command, so it can report "2 procs" when nothing is running.

## References
- references/marionette_walkthrough.py — copy and modify for any site walkthrough.
- references/marionette_poc_capture.py — full PoC screenshot capture script with
  OAuth finding evidence pattern.
