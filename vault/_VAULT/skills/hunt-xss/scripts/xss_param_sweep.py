#!/usr/bin/env python3
"""Exhaustive XSS param sweep with emission-form classification.

Usage:
    python3 xss_param_sweep.py pages.txt [--ua curl/8.5.0] [--out xss_sweep.json]

pages.txt: one URL per line (live, unauthenticated pages you are allowed to test).

What it does, per page:
  1. Harvests every query key from <a href>, <link href>, <script src>, <form action>
     and every name= on input/select/textarea.
  2. Injects a unique marker into each param, records body + header reflection and
     the surrounding context.
  3. For reflective params, re-injects `cpmarkx"><b>zq` and classifies the emission:
        RAW    -> payload verbatim          (exploitable, go prove execution)
        RAWQ   -> quote survives, tags coded (attribute breakout candidate)
        URLENC / ENTITY / NUMENT -> encoded (safe)
        STRIPPED -> hostile chars removed   (filter, test bypasses)
  4. Writes a JSON report keyed page -> param -> {class, status, context}.

Pitfalls baked in:
  * Unique marker, never an English word (targets echo "script"/"test" naturally).
  * UA is configurable: some WAFs 403 a bare Chrome UA but allow curl's. If every
    page comes back 403, re-run with --ua curl/8.5.0 before concluding anything.
  * Header reflections (Set-Cookie / Location) are captured too — cookie-write
    patterns like ?_go=<v> -> Set-Cookie are otherwise invisible.
"""
import argparse
import json
import re
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser

MARK = "cpmark987abczq"
HOSTILE = 'cpmarkx"><b>zq'

FORMS = {
    "RAW":     'cpmarkx"><b>zq',
    "URLENC":  'cpmarkx%22%3E%3Cb%3Ezq',
    "ENTITY":  'cpmarkx&quot;&gt;&lt;b&gt;zq',
    "NUMENT":  'cpmarkx&#34;&#62;&#60;b&#62;zq',
}
SKIP = {"ver", "nonce", "_wpnonce", "_wp_http_referer"}


class Params(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls, self.names = [], []

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag in ("a", "link", "script", "img", "form", "iframe"):
            for k in ("href", "src", "action"):
                if d.get(k):
                    self.urls.append(d[k])
        if tag in ("input", "select", "textarea") and d.get("name"):
            self.names.append(d["name"])


def make_ctx():
    c = ssl.create_default_context()
    c.check_hostname = False
    c.verify_mode = ssl.CERT_NONE
    return c


def fetch(url, ua, ctx):
    req = urllib.request.Request(url, headers={"User-Agent": ua})
    try:
        r = urllib.request.urlopen(req, timeout=25, context=ctx)
        return r.status, r.read().decode("utf-8", "replace"), dict(r.headers)
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace"), dict(e.headers)
    except Exception as e:  # noqa: BLE001 - surface the reason, don't swallow
        return 0, f"EXC {e}", {}


def harvest(page, body):
    p = Params()
    p.feed(body)
    params = set(p.names)
    for u in p.urls:
        try:
            q = urllib.parse.urlparse(urllib.parse.urljoin(page, u)).query
        except Exception:
            continue
        for kv in q.split("&"):
            k = kv.split("=")[0]
            if k and len(k) < 40:
                params.add(k)
    return sorted(x for x in params if x not in SKIP and not x.startswith("_wp"))


def with_param(page, param, value):
    sep = "&" if "?" in page else "?"
    return f"{page}{sep}{urllib.parse.quote(param)}={urllib.parse.quote(value, safe='')}"


def classify(body, headers):
    found = [name for name, form in FORMS.items() if form in body]
    hdr = [f"{k}: {v}" for k, v in headers.items() if MARK in str(v) or "cpmarkx" in str(v)]
    if found:
        return ",".join(found), hdr
    if re.search(r"cpmarkx\"", body):
        return "RAWQ", hdr
    if "cpmarkx" in body:
        return "STRIPPED", hdr
    return "", hdr


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pages")
    ap.add_argument("--ua", default="curl/8.5.0",
                    help="some WAFs 403 a bare Chrome UA; curl's UA often passes")
    ap.add_argument("--out", default="xss_sweep.json")
    args = ap.parse_args()

    ctx = make_ctx()
    pages = [l.strip() for l in open(args.pages) if l.strip() and not l.startswith("#")]
    report, totals = {}, {"params": 0, "reflective": 0, "raw": 0}

    for page in pages:
        status, body, _ = fetch(page, args.ua, ctx)
        if not body:
            report[page] = {"status": status, "error": "no body"}
            print(f"[{status}] {page}  NO BODY", file=sys.stderr)
            continue
        params = harvest(page, body)
        print(f"\n### [{status}] {page}  {len(body)}b  params({len(params)}): {params[:40]}")

        entry = {}
        for param in params:
            totals["params"] += 1
            st, b, h = fetch(with_param(page, param, MARK), args.ua, ctx)
            hits = [b[max(0, m.start() - 90):m.start() + len(MARK) + 90].replace("\n", " ")
                    for m in list(re.finditer(re.escape(MARK), b))[:2]]
            hdr_hits = [f"{k}: {v}" for k, v in h.items() if MARK in str(v)]
            rec = {"status": st, "reflected": bool(hits or hdr_hits), "context": hits[:2]}

            if hits or hdr_hits:
                totals["reflective"] += 1
                _, bh = fetch(with_param(page, param, HOSTILE), args.ua, ctx)
                st2, b2, h2 = fetch(with_param(page, param, HOSTILE), args.ua, ctx)
                cls, _ = classify(b2, h2)
                rec["class"] = cls or "UNKNOWN"
                if cls.startswith("RAW") and cls != "RAWQ":
                    totals["raw"] += 1
                print(f"   {rec['class']:16s} {param:18s} [{st2}]")
                if hits:
                    print(f"       {hits[0][:150]}")
                if hdr_hits:
                    print(f"       HDR {hdr_hits[0]}")
            entry[param] = rec
        report[page] = {"status": status, "params": entry}

    json.dump(report, open(args.out, "w"), indent=1)
    print(f"\nTOTAL params={totals['params']} reflective={totals['reflective']} "
          f"RAW={totals['raw']} -> {args.out}")
    if totals["reflective"] == 0:
        print("NOTE: zero reflections across every page usually means a UA/fingerprint "
              "block, not a clean target. Re-run with --ua curl/8.5.0 or a full browser "
              "header set before writing a negative.")


if __name__ == "__main__":
    main()
