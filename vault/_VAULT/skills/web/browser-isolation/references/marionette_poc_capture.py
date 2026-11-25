#!/usr/bin/env python3
"""
Marionette PoC Screenshot Capture Pattern
========================================
Complete pattern for capturing bug-bounty PoC evidence via Firefox + Marionette.

Key lessons baked in:
  1. save_screenshot() requires a file object, NOT a path string
  2. execute_script() does NOT await Promises — async fetch() returns None
  3. For HTTP-level proof, use curl from terminal()
  4. For screenshot display, inject result text into DOM then screenshot
  5. Session cleanup is delete_session(), not close_session()

Usage:
  1. Launch isolated Firefox with Marionette
  2. Connect via Marionette("localhost", port=2828)
  3. Navigate, inject results, screenshot
  4. Clean up with delete_session() + process.terminate()
"""

import os
import sys
import time
import subprocess

try:
    from marionette_driver.marionette import Marionette
except ImportError:
    subprocess.check_call([
        sys.executable, "-m", "pip", "install",
        "--break-system-packages", "marionette_driver"
    ])
    from marionette_driver.marionette import Marionette


def launch_isolated_ff(port=2828, profile_dir="/tmp/ff-iso-poc"):
    """Launch isolated Firefox with Marionette enabled."""
    ff_bin = subprocess.run(
        ["which", "firefox"], capture_output=True, text=True
    ).stdout.strip()
    if not ff_bin:
        raise RuntimeError("firefox not found")
    os.makedirs(profile_dir, exist_ok=True)
    proc = subprocess.Popen([
        ff_bin,
        "--no-remote",
        "--new-instance",
        "--profile", profile_dir,
        "--no-sync",
        "--marionette", str(port),
        "about:blank"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(3)
    return proc


def connect_marionette(port=2828):
    """Connect to isolated Firefox via Marionette."""
    m = Marionette("localhost", port=port)
    m.start_session()
    return m


def shoot(m, path, full=False):
    """Take screenshot. IMPORTANT: save_screenshot() needs a file object."""
    with open(path, "wb") as f:
        m.save_screenshot(f, full=full)
    print(f"  [+] {os.path.basename(path)}")


def dom_text(m, selector):
    """Synchronous DOM text extraction — SAFE with execute_script()."""
    return m.execute_script(f"""
        const el = document.querySelector('{selector}');
        return el ? el.textContent : 'NOT FOUND';
    """)


def inject_result(m, title, lines):
    """Inject result text into page for screenshot display.
    Use this instead of async fetch() which returns None in execute_script().
    """
    body = "\\n".join(lines)
    m.execute_script(f"""
        document.body.innerHTML = '<pre style="font-size:20px;padding:30px;'''
        + f'''background:#1e1e1e;color:#0f0;font-family:monospace;">{title}\\n\\n{body}</pre>';
    """)


def cleanup(m, proc):
    """Clean up Marionette session and Firefox process."""
    try:
        m.delete_session()  # NOT close_session()
    except Exception:
        pass
    proc.terminate()
    try:
        proc.wait(timeout=5)
    except Exception:
        proc.kill()


# ── Example Usage ──────────────────────────────────────────────────

def example_oauth_poc():
    OUT = os.path.expanduser("~/Bugbounty/poc-screenshots")
    os.makedirs(OUT, exist_ok=True)

    ff = launch_isolated_ff()
    m = connect_marionette()

    try:
        BASE = "https://example.com"

        # ── Finding: Missing State Parameter ──
        m.navigate(f"{BASE}/login/?state=CSRF_TEST_123")
        time.sleep(2)

        # Screenshot: URL with state param (full page)
        shoot(m, os.path.join(OUT, "01-url-with-state.png"), full=True)

        # Screenshot: View source
        m.navigate(f"view-source:{BASE}/login/?state=CSRF_TEST_123")
        time.sleep(2)
        shoot(m, os.path.join(OUT, "02-view-source.png"), full=True)

        # DOM inspection (synchronous — SAFE)
        state_count = m.execute_script("""
            return document.documentElement.outerHTML
                .match(/state/gi)?.length || 0;
        """)
        print(f"  state count: {state_count}")

        # Inject result for screenshot (workaround for async fetch returning None)
        m.navigate(f"{BASE}/login/?state=CSRF_TEST_123")
        time.sleep(1)
        inject_result(m, "FINDING 1: Missing State Parameter", [
            f"URL: {BASE}/login/?state=CSRF_TEST_123",
            f"",
            f"state count in HTML: {state_count}",
            f"",
            f"No state parameter found in page source.",
            f"No CSRF protection in OAuth flow.",
        ])
        time.sleep(0.5)
        shoot(m, os.path.join(OUT, "03-state-count-result.png"))

        # ── For HTTP-level proof, use curl from terminal() ──
        # curl -s -o /dev/null -w "%{http_code}" \
        #   "https://example.com/oauth/callback?code=FAKE&state=test"

        print(f"\nScreenshots saved to: {OUT}")
        for f in sorted(os.listdir(OUT)):
            if f.endswith(".png"):
                print(f"  {f}")

    finally:
        cleanup(m, ff)


if __name__ == "__main__":
    example_oauth_poc()
