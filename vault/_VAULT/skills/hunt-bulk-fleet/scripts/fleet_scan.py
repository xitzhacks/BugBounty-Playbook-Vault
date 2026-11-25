#!/usr/bin/env python3
"""
fleet_scan.py — multi-target config/infra finding sweep.

Sweeps a list of targets for the classes that repeat across a fleet, then
emits a grouped triage report that separates real per-host signal from
systemic boilerplate (one root cause multiplied across N hosts).

Usage:
  python3 fleet_scan.py -t targets.txt -o out/
  python3 fleet_scan.py -t targets.txt -o out/ --oob yourid.oast.live
  python3 fleet_scan.py -t targets.txt -o out/ --only ssrf,openredirect,swagger
  python3 fleet_scan.py -t targets.txt -o out/ --deep

Only uses requests + stdlib. Falls back to urllib if requests is missing.
"""
import argparse, json, os, re, ssl, sys, time, socket
import concurrent.futures as cf
from urllib.parse import urlparse, urljoin, quote

try:
    import requests
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    HAVE_REQUESTS = True
except Exception:
    HAVE_REQUESTS = False
    import urllib.request, urllib.error

# ------------------------------------------------------------------ config
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36")

# Classes grouped by whether they are per-host signal or systemic boilerplate.
BOILERPLATE_CLASSES = {
    "tls_cbc", "tls_weak_protocol", "tls_cipher_suite", "tls_forward_secrecy",
    "headers", "hsts", "csp", "cookies", "server_disclosure", "cert",
}
SIGNAL_CLASSES = {
    "ssrf", "openredirect", "clickjacking", "forcedbrowsing", "swagger",
    "dangerous_methods", "rate_limit", "infoleak", "error_page", "slowloris",
}

SECURITY_HEADERS = [
    "Strict-Transport-Security", "Content-Security-Policy",
    "X-Frame-Options", "X-Content-Type-Options", "Referrer-Policy",
    "Permissions-Policy",
]

# Endpoint patterns worth probing per host.
API_DOC_PATHS = [
    "/swagger-ui.html", "/swagger-ui/", "/swagger/index.html",
    "/api-docs", "/api-docs/", "/api-docs/swagger.json", "/api-docs/swagger.yaml",
    "/swagger.json", "/swagger.yaml", "/v2/api-docs", "/v3/api-docs",
    "/openapi.json", "/openapi.yaml", "/api/swagger.json", "/api/swagger.yaml",
    "/api/api-docs", "/api/api-docs/", "/graphql", "/graphiql",
    "/actuator", "/actuator/env", "/actuator/health",
]
# Known CVE report-uri / callback endpoints seen in real engagements.
CSP_REPORT_PATHS = ["/csp_report", "/csp-report", "/report", "/csp", "/r"]
REDIRECT_PARAMS = [
    "redirecturl", "redirect", "redirect_uri", "redirect_uri_1", "url",
    "next", "returnUrl", "returnto", "return", "goto", "target", "dest",
    "destination", "continue", "view", "rurl", "forward", "callback",
    "returl", "u", "to", "out", "ref", "path",
]
FORCED_PATHS = [
    "/.git/config", "/.git/HEAD", "/.env", "/.DS_Store", "/.svn/entries",
    "/.hg/requires", "/backup.zip", "/backup.tar.gz", "/db.sql", "/dump.sql",
    "/config.php.bak", "/web.config", "/phpinfo.php", "/server-status",
    "/server-info", "/WEB-INF/web.xml", "/crossdomain.xml", "/.aws/credentials",
    "/actuator/env", "/actuator/heapdump", "/debug", "/trace", "/metrics",
]
DANGEROUS_METHODS = ["PUT", "DELETE", "TRACE", "PATCH", "PROPFIND"]
# TLS ciphers that trigger Lucky13 / BREACH reporting (CBC-mode, SHA1 MAC).
CBC_CIPHERS = [
    "ECDHE-RSA-AES128-SHA256", "ECDHE-RSA-AES256-SHA384",
    "ECDHE-RSA-AES128-SHA", "ECDHE-RSA-AES256-SHA",
    "AES128-SHA256", "AES256-SHA256", "AES128-SHA", "AES256-SHA",
    "DES-CBC3-SHA", "RC4-SHA", "IDEA-CBC-SHA", "SEED-SHA",
    "CAMELLIA128-SHA", "CAMELLIA256-SHA",
]
WEAK_PROTOCOLS = ["TLSv1.0", "TLSv1.1", "SSLv3", "SSLv2"]

# ------------------------------------------------------------------ helpers
def now():
    return time.strftime("%Y-%m-%dT%H:%M:%S")

def norm_url(t):
    """Accept bare host, host:port, or full URL. Return scheme://host:port."""
    t = t.strip()
    if not t or t.startswith("#"):
        return None
    if "://" not in t:
        t = "https://" + t
    p = urlparse(t)
    if not p.hostname:
        return None
    host = p.hostname
    port = p.port
    scheme = p.scheme if p.scheme in ("http", "https") else "https"
    netloc = host if not port else f"{host}:{port}"
    return f"{scheme}://{netloc}"

def http(method, url, body=None, headers=None, timeout=12, verify=False, allow_redirects=False):
    """Return (status, headers_dict, body_text). Never raises."""
    h = {"User-Agent": UA, "Accept": "*/*"}
    if headers:
        h.update(headers)
    if HAVE_REQUESTS:
        try:
            r = requests.request(method, url, data=body, headers=h, timeout=timeout,
                                 verify=verify, allow_redirects=allow_redirects)
            return r.status_code, dict(r.headers), r.text
        except requests.exceptions.RequestException as e:
            return 0, {}, f"__ERR__ {type(e).__name__}: {e}"
    else:
        try:
            req = urllib.request.Request(url, data=body.encode() if body else None,
                                         headers=h, method=method)
            ctx = ssl._create_unverified_context()
            op = urllib.request.build_opener(urllib.request.HTTPSHandler(context=ctx))
            if not allow_redirects:
                class NoRedir(urllib.request.HTTPRedirectHandler):
                    def redirect_request(self, *a, **k):
                        return None
                op = urllib.request.build_opener(NoRedir, urllib.request.HTTPSHandler(context=ctx))
            with op.open(req, timeout=timeout) as resp:
                return resp.status, dict(resp.headers), resp.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            return e.code, dict(e.headers or {}), e.read().decode("utf-8", "replace")
        except Exception as e:
            return 0, {}, f"__ERR__ {type(e).__name__}: {e}"

# ------------------------------------------------------------------ checks
def check_headers(url, ev):
    st, h, b = http("GET", url, allow_redirects=True)
    if st == 0:
        return []
    out = []
    missing = [x for x in SECURITY_HEADERS if x not in h]
    # X-Frame-Options / frame-ancestors = clickjacking
    csp = h.get("Content-Security-Policy", "")
    has_fa = "frame-ancestors" in csp.lower()
    has_xfo = "X-Frame-Options" in h
    if not has_xfo and not has_fa:
        out.append({"class": "clickjacking", "target": url,
                    "detail": "No X-Frame-Options and no CSP frame-ancestors",
                    "severity_hint": "Medium"})
    if missing:
        out.append({"class": "headers", "target": url,
                    "detail": "Missing: " + ", ".join(missing),
                    "missing": missing, "severity_hint": "Info"})
    if "Strict-Transport-Security" in missing:
        out.append({"class": "hsts", "target": url,
                    "detail": "No Strict-Transport-Security header",
                    "severity_hint": "Info"})
    if "Content-Security-Policy" in h:
        weak = []
        if "'unsafe-eval'" in csp: weak.append("unsafe-eval")
        if "'unsafe-inline'" in csp: weak.append("unsafe-inline")
        if "data:" in csp and "script-src" in csp: weak.append("data: in script-src")
        if not has_fa: weak.append("no frame-ancestors")
        if weak:
            out.append({"class": "csp", "target": url,
                        "detail": "Weak CSP: " + ", ".join(weak),
                        "csp": csp, "severity_hint": "Info"})
    else:
        out.append({"class": "csp", "target": url, "detail": "No CSP header",
                    "severity_hint": "Info"})
    # cookie attributes
    setc = h.get("Set-Cookie", "")
    if setc:
        probs = []
        if "secure" not in setc.lower(): probs.append("no Secure")
        if "httponly" not in setc.lower(): probs.append("no HttpOnly")
        if "samesite" not in setc.lower(): probs.append("no SameSite")
        if probs:
            out.append({"class": "cookies", "target": url,
                        "detail": "Set-Cookie " + ", ".join(probs),
                        "set_cookie": setc, "severity_hint": "Info"})
    # server / tech disclosure
    srv = h.get("Server", "")
    xpb = h.get("X-Powered-By", "")
    if srv or xpb:
        out.append({"class": "server_disclosure", "target": url,
                    "detail": f"Server: {srv} | X-Powered-By: {xpb}",
                    "server": srv, "x_powered_by": xpb, "severity_hint": "Info"})
    ev(f"headers {url}\nHTTP {st}\n" + "\n".join(f"{k}: {v}" for k, v in h.items())[:3000])
    return out

def _openssl(host, args, timeout=20):
    """Run openssl s_client and return stdout+stderr.

    IMPORTANT: openssl s_client writes its banner to STDERR, so capturing
    stdout only yields an empty string. Must merge both streams.
    """
    cmd = (f"timeout {timeout} openssl s_client -connect {host} -servername {host} "
           f"{args} </dev/null 2>&1")
    try:
        return os.popen(cmd).read()
    except Exception:
        return ""


def check_tls(url, ev, deep=False):
    """TLS cipher/protocol state via openssl s_client.

    A single handshake only reveals ONE negotiated cipher. To learn the full
    set the server is willing to negotiate (which is what the Lucky13/BREACH
    class is about) we must ask for the server's cipher list explicitly, and
    separately probe each weak protocol version.
    """
    if not url.startswith("https://"):
        return []
    host = urlparse(url).netloc
    out = []
    ciphers, proto = [], ""

    # --- negotiated cipher + protocol (banner goes to stderr) ---
    r = _openssl(host, "-brief")
    m = re.search(r"Ciphersuite:\s*(\S+)", r)
    if m:
        ciphers.append(m.group(1))
    m = re.search(r"Protocol version:\s*(\S+)", r)
    if m:
        proto = m.group(1)

    # --- full offered cipher list ---
    # -cipher 'ALL:@SECLEVEL=0' + -tls1_2 forces a TLS1.2 handshake where the
    # server prints every cipher it supports. SECLEVEL=0 allows 3DES/RC4 etc.
    listed = ""
    for extra in ("-cipher ALL:@SECLEVEL=0 -tls1_2", "-cipher ALL:@SECLEVEL=1 -tls1_2"):
        rr = _openssl(host, extra)
        block = re.search(r"^\s*Cipher\s*:\s*(.+)$", rr, re.M)
        if block:
            listed = block.group(1)
            break
    offered = [c.strip() for c in listed.split(":") if c.strip()] if listed else []

    all_ciphers = sorted(set(ciphers + offered))

    # --- weak protocol negotiation attempts ---
    weak_protos = []
    for p, label in (("-tls1", "TLSv1.0"), ("-tls1_1", "TLSv1.1"), ("-ssl3", "SSLv3")):
        rr = _openssl(host, p, timeout=15)
        if "Cipher" in rr and "alert" not in rr.lower()[:400]:
            weak_protos.append(label)
        elif re.search(r"Protocol\s*:\s*%s" % re.escape(label), rr):
            weak_protos.append(label)

    # --- CBC / SHA1 MAC ciphers -> Lucky13 + BREACH class ---
    cbc = []
    for c in all_ciphers:
        if re.search(r"CBC", c, re.I) or re.search(r"-SHA\b", c) or c.endswith("_SHA"):
            cbc.append(c)
    # normalise OpenSSL names to the short names used in reports
    short = []
    for c in cbc:
        s = re.sub(r"^TLS_", "", c)
        s = re.sub(r"_WITH_.*$", "", s)
        s = s.replace("_", "-")
        short.append(s)
    short = sorted(set(short))

    if short:
        out.append({"class": "tls_cbc", "target": url,
                    "detail": "CBC/SHA1 ciphers offered: " + ", ".join(short),
                    "ciphers": all_ciphers, "short": short,
                    "severity_hint": "Info"})
    if weak_protos:
        out.append({"class": "tls_weak_protocol", "target": url,
                    "detail": "Weak protocol(s) negotiable: " + ", ".join(weak_protos),
                    "protocols": weak_protos, "severity_hint": "Info"})
    if all_ciphers:
        out.append({"class": "tls_cipher_suite", "target": url,
                    "detail": f"Negotiated {ciphers[0] if ciphers else '?'} "
                              f"(proto {proto or '?'}); {len(all_ciphers)} ciphers offered",
                    "ciphers": all_ciphers, "protocol": proto,
                    "severity_hint": "Info"})

    # --- forward secrecy ---
    fs_ciphers = [c for c in all_ciphers if re.search(r"ECDHE|DHE|ECDSA", c, re.I)]
    if all_ciphers and not fs_ciphers:
        out.append({"class": "tls_forward_secrecy", "target": url,
                    "detail": "No forward secrecy cipher offered",
                    "severity_hint": "Info"})

    ev(f"tls {url}\nprotocol={proto}\nnegotiated={ciphers}\n"
       f"offered({len(all_ciphers)})={all_ciphers}\n"
       f"cbc={short}\nweak_protocols={weak_protos}\n")
    return out

def check_swagger(url, ev):
    out = []
    host = urlparse(url)
    base = f"{host.scheme}://{host.netloc}"
    for p in API_DOC_PATHS:
        st, h, b = http("GET", base + p, allow_redirects=True)
        if st == 0:
            continue
        body = (b or "").lower()
        looks = (("swagger" in body or "openapi" in body)
                 or p.endswith(("swagger.json", "swagger.yaml", "openapi.json", "openapi.yaml"))
                 or st == 200 and "api-docs" in p)
        if st == 200 and looks:
            endpoints = []
            if p.endswith(".json"):
                try:
                    j = json.loads(b)
                    for path in (j.get("paths") or {}):
                        endpoints.append(path)
                except Exception:
                    pass
            out.append({"class": "swagger", "target": base + p,
                        "detail": f"API docs exposed at {p} (HTTP {st})",
                        "path": p, "endpoint_count": len(endpoints),
                        "endpoints": endpoints[:50], "severity_hint": "Medium"})
            ev(f"swagger {base+p}\nHTTP {st}\n{b[:1500]}")
    return out

def check_ssrf(url, ev, oob=None):
    """CSP report-uri / report-to SSRF — server fetches an attacker URL."""
    out = []
    host = urlparse(url)
    base = f"{host.scheme}://{host.netloc}"
    csp = ""
    st, h, b = http("GET", base + "/", allow_redirects=True)
    csp = h.get("Content-Security-Policy", "")
    m = re.search(r"report-uri\s+([^\s;]+)", csp)
    targets = []
    if m:
        targets.append(m.group(1))
    for p in CSP_REPORT_PATHS:
        targets.append(p)
    for t in targets:
        if t.startswith("/"):
            endpoint = base + t
        elif "://" in t:
            endpoint = t
        else:
            continue
        cb = oob or "oast.live"
        canary = f"http://{cb.replace('oast.live','oast.fun')}"
        payload = {
            "csp-report": {
                "document-uri": f"{base}/",
                "referrer": "",
                "violated-directive": "script-src-elem",
                "effective-directive": "script-src-elem",
                "original-policy": csp or "default-src 'self'",
                "blocked-uri": canary,
                "status-code": 404,
            }
        }
        body = json.dumps(payload)
        st2, h2, b2 = http("POST", endpoint, body=body,
                           headers={"Content-Type": "application/csp-report",
                                    "Content-Type": "application/json"})
        if st2 in (200, 202, 204) or (st2 == 0):
            out.append({"class": "ssrf", "target": endpoint,
                        "detail": f"POST {endpoint} accepted CSP report payload "
                                  f"(HTTP {st2}); blocked-uri canary = {canary}",
                        "canary": canary, "status": st2, "severity_hint": "High",
                        "note": "CONFIRM the OOB callback actually fired before reporting"})
            ev(f"ssrf {endpoint}\nHTTP {st2}\ncanary={canary}\n{body[:800]}\n")
    return out

def check_openredirect(url, ev):
    out = []
    host = urlparse(url)
    base = f"{host.scheme}://{host.netloc}"
    ext = "https://example.com"
    st, h, b = http("GET", base + "/", allow_redirects=False)
    # SAP NetWeaver and friends expose a known redirect endpoint
    sap = ["/sap/public/bc/icf/logoff", "/sap/public/bc/icf/logoff/",
           "/nwa/irj/portal/logout", "/sap/bc/logout"]
    for p in sap:
        for param in ("redirecturl", "redirect", "sap-client"):
            u = f"{base}{p}?{param}={quote(ext, safe='')}"
            st2, h2, b2 = http("GET", u, allow_redirects=False)
            loc = h2.get("Location", "")
            if st2 in (301, 302, 303, 307, 308) and "example.com" in loc:
                out.append({"class": "openredirect", "target": u,
                            "detail": f"HTTP {st2} -> Location: {loc}",
                            "location": loc, "severity_hint": "Medium"})
                ev(f"openredirect {u}\nHTTP {st2}\nLocation: {loc}\n")
                break
    # Parameter fuzz on the main page
    for param in REDIRECT_PARAMS:
        u = f"{base}/?{param}={quote(ext, safe='')}"
        st2, h2, b2 = http("GET", u, allow_redirects=False)
        loc = h2.get("Location", "")
        if st2 in (301, 302, 303, 307, 308) and "example.com" in loc:
            out.append({"class": "openredirect", "target": u,
                        "detail": f"HTTP {st2} -> Location: {loc}",
                        "location": loc, "severity_hint": "Medium"})
            ev(f"openredirect {u}\nHTTP {st2}\nLocation: {loc}\n")
            break
    return out

def check_forcedbrowsing(url, ev):
    out = []
    host = urlparse(url)
    base = f"{host.scheme}://{host.netloc}"
    for p in FORCED_PATHS:
        st, h, b = http("GET", base + p, allow_redirects=False)
        if st == 0:
            continue
        low = (b or "").lower()
        interesting = False
        evidence = ""
        if p == "/.git/config" and "[core]" in low:
            interesting = True; evidence = "git config dumped"
        elif p == "/.git/HEAD" and "ref:" in low:
            interesting = True; evidence = "git HEAD exposed"
        elif p == "/.env" and re.search(r"\w+_key\s*=", low):
            interesting = True; evidence = "env var assignments in body"
        elif p == "/actuator/env" and '"propertySources"' in low:
            interesting = True; evidence = "Spring actuator env dump"
        elif p == "/actuator/heapdump" and st == 200 and len(b or "") > 1000:
            interesting = True; evidence = "heapdump served"
        elif p == "/WEB-INF/web.xml" and "<web-app" in low:
            interesting = True; evidence = "web.xml served"
        elif p in ("/backup.zip", "/backup.tar.gz", "/db.sql", "/dump.sql") and st == 200 and len(b or "") > 500:
            interesting = True; evidence = f"{p} served ({len(b)} bytes)"
        elif p == "/.aws/credentials" and "aws_access_key" in low:
            interesting = True; evidence = "AWS credentials"
        elif st == 200 and p.startswith("/.") and "not found" not in low and len(b or "") > 100:
            interesting = True; evidence = f"dotfile {p} served"
        if interesting:
            out.append({"class": "forcedbrowsing", "target": base + p,
                        "detail": f"{p} -> HTTP {st}: {evidence}",
                        "status": st, "severity_hint": "High"})
            ev(f"forcedbrowsing {base+p}\nHTTP {st}\n{evidence}\n{(b or '')[:1500]}\n")
    return out

def check_dangerous_methods(url, ev):
    out = []
    host = urlparse(url)
    base = f"{host.scheme}://{host.netloc}"
    for m in DANGEROUS_METHODS:
        st, h, b = http(m, base + "/", allow_redirects=False)
        if st in (200, 201, 204):
            out.append({"class": "dangerous_methods", "target": f"{m} {base}/",
                        "detail": f"{m} / returned HTTP {st}",
                        "method": m, "status": st, "severity_hint": "Medium",
                        "note": "Verify the method is ACTUALLY acted on before reporting"})
            ev(f"dangerous {m} {base}/\nHTTP {st}\n{(b or '')[:600]}\n")
    return out

def check_infoleak(url, ev):
    out = []
    host = urlparse(url)
    base = f"{host.scheme}://{host.netloc}"
    st, h, b = http("GET", base + "/", allow_redirects=True)
    if st == 0:
        return out
    for leak in ("stacktrace", "exception", "traceback", "at java.", "at org.",
                 "at com.", "error in", "debug mode", "internal server error"):
        if leak in (b or "").lower():
            out.append({"class": "error_page", "target": base + "/",
                        "detail": f"Error/debug info disclosed: '{leak}'",
                        "severity_hint": "Low"})
            ev(f"errorpage {base}/\nHTTP {st}\nmatch={leak}\n{(b or '')[:1500]}\n")
            break
    # version-ish strings in headers
    for hk in ("X-AspNet-Version", "X-AspNetMvc-Version", "X-Powered-By",
               "X-Generator", "X-Drupal-Cache", "X-Runtime"):
        if hk in h and h[hk]:
            out.append({"class": "infoleak", "target": base + "/",
                        "detail": f"{hk}: {h[hk]}", "severity_hint": "Low"})
    return out

def check_ratelimit(url, ev, n=30):
    """Test for missing rate limiting.

    Only meaningful on an endpoint that actually accepts the request. A 404
    or 405 means the endpoint does not exist / does not accept the method,
    which tells us NOTHING about rate limiting. We require a real auth-like
    response (401/403) to consider the endpoint live.
    """
    out = []
    host = urlparse(url)
    base = f"{host.scheme}://{host.netloc}"
    for path in ("/login", "/api/login", "/auth/login", "/signin",
                 "/api/auth/login", "/otp", "/verify"):
        target = base + path
        codes = []
        for i in range(min(n, 30)):
            st, h, b = http("POST", target,
                            body="username=testuser&password=[REDACTED_SECRET]",
                            headers={"Content-Type": "application/x-www-form-urlencoded"})
            codes.append(st)
            if st == 429:
                break
        if not codes:
            continue
        # Endpoint must look like a real auth endpoint (401/403), else skip.
        if not any(c in (401, 403) for c in codes):
            continue
        if 429 in codes:
            ev(f"ratelimit {target}\nrate limited after {codes.index(429)+1} requests "
               f"(statuses {sorted(set(codes))})\n")
            continue
        out.append({"class": "rate_limit", "target": target,
                    "detail": f"{len(codes)} POSTs to {path}, NO 429 returned "
                              f"(statuses: {sorted(set(codes))})",
                    "statuses": codes, "severity_hint": "Medium",
                    "note": "Verify against a real auth/OTP flow and use a "
                            "throwaway account; only meaningful where the "
                            "action is actually protected"})
        ev(f"ratelimit {target}\n{len(codes)} requests, statuses={sorted(set(codes))}\n")
        break
    return out

def check_clickjacking_poc(url, ev, oob=None):
    """Generate a ready-to-host clickjacking PoC (static HTML)."""
    return []

# ------------------------------------------------------------------ runner
def scan_target(t, only=None, oob=None, deep=False, timeout=12):
    findings = []
    ev_lines = []

    def ev(text):
        ev_lines.append(text)

    base = norm_url(t)
    if not base:
        return None

    def want(cls):
        return (not only) or (cls in only)

    # Always: headers, clickjacking, server disclosure
    if want("headers") or want("clickjacking") or want("csp") or want("cookies") \
       or want("server_disclosure"):
        findings += check_headers(base, ev)

    if want("swagger"):
        findings += check_swagger(base, ev)

    if want("ssrf"):
        findings += check_ssrf(base, ev, oob)

    if want("openredirect"):
        findings += check_openredirect(base, ev)

    if want("forcedbrowsing"):
        findings += check_forcedbrowsing(base, ev)

    if want("dangerous_methods"):
        findings += check_dangerous_methods(base, ev)

    if want("infoleak") or want("error_page"):
        findings += check_infoleak(base, ev)

    if want("rate_limit"):
        findings += check_ratelimit(base, ev)

    if deep and (want("tls_cbc") or want("tls_cipher_suite") or want("tls_weak_protocol")):
        findings += check_tls(base, ev)

    return {
        "target": t, "base": base, "findings": findings,
        "evidence": "\n\n".join(ev_lines),
    }

def write_report(results, outdir, only=None, oob=None):
    evdir = os.path.join(outdir, "evidence")
    os.makedirs(evdir, exist_ok=True)
    records = []
    for r in results:
        if not r:
            continue
        if r["evidence"]:
            safe = re.sub(r"[^A-Za-z0-9._-]+", "_", r["base"])[:100]
            with open(os.path.join(evdir, safe + ".txt"), "w") as f:
                f.write(r["evidence"])
        records.append({
            "target": r["base"], "original": r["target"],
            "findings": r["findings"],
        })

    with open(os.path.join(outdir, "results.json"), "w") as f:
        json.dump({"generated": now(), "oob": oob, "results": records}, f, indent=2)

    # ---- group
    signal, boiler = {}, {}
    for rec in records:
        for fd in rec["findings"]:
            bucket = boiler if fd["class"] in BOILERPLATE_CLASSES else signal
            bucket.setdefault(fd["class"], []).append((rec["target"], fd))

    def group_key(cls, items):
        """Group boilerplate by root-cause fingerprint, not just class."""
        if cls in ("tls_cbc", "tls_cipher_suite", "tls_weak_protocol"):
            return "TLS cipher/protocol state"
        if cls in ("headers", "hsts"):
            return "Missing security headers"
        if cls == "csp":
            return "Weak / missing CSP"
        if cls == "cookies":
            return "Missing cookie attributes"
        if cls in ("server_disclosure", "cert", "infoleak"):
            return "Technology version disclosure"
        return cls

    root_causes = {}
    for cls, items in boiler.items():
        gk = group_key(cls, items)
        root_causes.setdefault(gk, []).extend(items)

    L = []
    L.append("# Fleet Triage Report")
    L.append("")
    L.append(f"- Generated: `{now()}`")
    L.append(f"- Targets scanned: **{len(records)}**")
    L.append(f"- Total raw findings: **{sum(len(r['findings']) for r in records)}**")
    if oob:
        L.append(f"- OOB callback domain: `{oob}`")
    L.append("")
    L.append("> Triage rule: one systemic misconfiguration multiplied across N hosts is")
    L.append("> ONE finding with a host table — not N reports. Per-host findings are")
    L.append("> only per-host if the remediation is per-host.")
    L.append("")

    L.append("## 1. SIGNAL — real, per-host findings")
    L.append("")
    if not signal:
        L.append("_None._")
    else:
        for cls in sorted(signal, key=lambda c: -len(signal[c])):
            items = signal[cls]
            sev = items[0][1].get("severity_hint", "Info")
            L.append(f"### {cls} — {len(items)} occurrence(s) — severity hint: {sev}")
            L.append("")
            for tgt, fd in items:
                L.append(f"- `{tgt}` — {fd['detail']}")
                if fd.get("note"):
                    L.append(f"  - _note:_ {fd['note']}")
            L.append("")

    L.append("## 2. BOILERPLATE — group by root cause")
    L.append("")
    if not root_causes:
        L.append("_None._")
    else:
        for gk, items in sorted(root_causes.items(), key=lambda x: -len(x[1])):
            hosts = sorted({t for t, _ in items})
            L.append(f"### Root cause: {gk} — {len(items)} finding(s) across {len(hosts)} host(s)")
            L.append("")
            for h in hosts:
                L.append(f"- `{h}`")
            L.append("")
            L.append(f"_One report, {len(hosts)} affected hosts._ "
                     "Confirm the hosts share a front end (compare `Server` header "
                     "and certificate issuer) before asserting a single root cause.")
            L.append("")

    L.append("## 3. Raw counts by class")
    L.append("")
    L.append("| Class | Count | Kind |")
    L.append("|---|---|---|")
    allc = {}
    for cls, items in signal.items():
        allc[cls] = allc.get(cls, 0) + len(items)
    for cls, items in boiler.items():
        allc[cls] = allc.get(cls, 0) + len(items)
    for cls, n in sorted(allc.items(), key=lambda x: -x[1]):
        kind = "signal" if cls in SIGNAL_CLASSES else "boilerplate"
        L.append(f"| {cls} | {n} | {kind} |")
    L.append("")

    with open(os.path.join(outdir, "summary.md"), "w") as f:
        f.write("\n".join(L))
    return records

def main():
    ap = argparse.ArgumentParser(description="Multi-target fleet finding sweep")
    ap.add_argument("-t", "--targets", required=True, help="file with one target per line")
    ap.add_argument("-o", "--out", default="out", help="output directory")
    ap.add_argument("--only", help="comma-separated classes to run")
    ap.add_argument("--oob", help="OOB callback domain, e.g. yourid.oast.live")
    ap.add_argument("--deep", action="store_true", help="include TLS cipher inspection")
    ap.add_argument("--threads", type=int, default=20)
    ap.add_argument("--timeout", type=int, default=12)
    ap.add_argument("-v", "--verbose", action="store_true")
    a = ap.parse_args()

    if not os.path.exists(a.targets):
        print(f"[!] target file not found: {a.targets}", file=sys.stderr)
        return 1
    os.makedirs(a.out, exist_ok=True)

    targets = []
    seen = set()
    for line in open(a.targets, errors="replace"):
        t = line.strip()
        if not t or t.startswith("#"):
            continue
        if t.lower().endswith(".txt"):
            continue
        n = norm_url(t)
        if n and n not in seen:
            seen.add(n); targets.append(t)

    only = set(x.strip() for x in a.only.split(",")) if a.only else None
    print(f"[*] scanning {len(targets)} targets "
          f"(threads={a.threads}, deep={a.deep}, oob={a.oob or 'none'})")

    results = []
    done = 0
    with cf.ThreadPoolExecutor(max_workers=a.threads) as ex:
        futs = {ex.submit(scan_target, t, only, a.oob, a.deep, a.timeout): t for t in targets}
        for fut in cf.as_completed(futs):
            done += 1
            try:
                r = fut.result()
            except Exception as e:
                if a.verbose:
                    print(f"  [!] {futs[fut]}: {e}")
                r = None
            if r:
                results.append(r)
            if done % 10 == 0 or done == len(targets):
                print(f"  .. {done}/{len(targets)}")

    recs = write_report(results, a.out, only, a.oob)
    total = sum(len(r["findings"]) for r in recs)
    print()
    print(f"[+] scanned {len(recs)} targets, {total} raw findings")
    print(f"[+] report:  {os.path.join(a.out, 'summary.md')}")
    print(f"[+] raw:     {os.path.join(a.out, 'results.json')}")
    if a.oob:
        print(f"[!] OOB callback domain {a.oob} — check its logs for confirmed "
              f"SSRF callbacks, then tear it down.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
