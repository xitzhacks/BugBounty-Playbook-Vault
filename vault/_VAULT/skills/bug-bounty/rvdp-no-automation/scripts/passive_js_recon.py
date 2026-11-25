#!/usr/bin/env python3
# Passive JS/URL recon — SAFE under RVDP/no-automation rules.
# Fetches the page HTML, downloads referenced JS bundles, and extracts:
#   absolute URLs (incl. other TARGET subdomains), API/endpoint paths,
#   cloud storage refs, secret/key assignment candidates (manual review).
# No crawling, no fuzzing, no active scanning. Single GETs only.
import re, os, subprocess, sys

TARGET = os.environ.get("TARGET", "atherenergy.com")
BASE = os.path.expanduser("~/Bugbounty")
JS_DIR = os.path.join(BASE, "js")
os.makedirs(JS_DIR, exist_ok=True)
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"

# name -> page url to fetch (only IN-SCOPE hosts)
TARGETS = {
    "www": f"https://www.{TARGET}",
    "app": f"https://app.{TARGET}/login",
}

def fetch(url):
    try:
        return subprocess.run(["curl","-s","-A",UA,"--max-time","40","-L",url],
                              capture_output=True, text=True, timeout=60).stdout
    except Exception:
        return ""

def download(url, path):
    try:
        rc = subprocess.run(["curl","-s","-A",UA,"--max-time","60","-L",url,"-o",path],
                           capture_output=True, text=True, timeout=80).returncode
        return rc == 0 and os.path.getsize(path) > 0
    except Exception:
        return False

PAT = {
    "urls":    re.compile(r'https?://[a-zA-Z0-9_.\-]+(?::\d+)?(?:/[^\s"\')<>]*)?'),
    "athsubs": re.compile(r'\b([a-z0-9][a-z0-9-]{1,30}\.%s)\b' % re.escape(TARGET), re.I),
    "api":     re.compile(r'/(?:api|v[0-9]|graphql|rest|internal|admin|auth|oauth|user|account|payment|order|profile|referral|bank|dashboard|session|token|login|signup|register)[a-zA-Z0-9_/\-{}:]*', re.I),
    "cloud":   re.compile(r'(?:s3\.amazonaws\.com|s3-[a-z0-9\-]+\.amazonaws\.com|blob\.core\.windows\.net|storage\.googleapis\.com|digitaloceanspaces\.com|[a-z0-9\-]+\.supabase\.co|firebasestorage\.googleapis\.com)', re.I),
    "secret":  re.compile(r'(?i)(?:api[_-]?key|apikey|secret|client[_-]?secret|access[_-]?token|auth[_-]?token|bearer|private[_-]?key|aws[_-]?access|aws[_-]?secret|password|token|authorization)["\'\s:=]{1,3}["\']?[A-Za-z0-9_\-\.]{6,}'),
}

for name, page in TARGETS.items():
    html = fetch(page)
    js = set()
    for m in re.findall(r'<script[^>]+src=["\']([^"\']+)["\']', html):
        js.add(m)
    for m in re.findall(r'<link[^>]+href=["\']([^"\']+\.js[^"\']*)["\']', html):
        js.add(m)
    print(f"[*] {name}: {len(js)} script refs", file=sys.stderr)

    urls=set(); athsubs=set(); api=set(); cloud=set(); secret=set()
    for ref in js:
        if ref.startswith("//"): ref="https:"+ref
        elif ref.startswith("/"): ref="https://"+TARGET+ref
        elif not ref.startswith("http"): ref="https://"+TARGET+"/"+ref
        fname = re.sub(r'[^a-zA-Z0-9]','_', (ref.split('/')[-1] or "inline"))[:60]
        jpath = os.path.join(JS_DIR, f"{name}_{fname}.js")
        if not download(ref, jpath):
            continue
        try:
            code = open(jpath, encoding="utf-8", errors="ignore").read()
        except Exception:
            continue
        for k, pat in PAT.items():
            for hit in pat.findall(code):
                if k=="urls": urls.add(hit)
                elif k=="athsubs": athsubs.add(hit.lower())
                elif k=="api": api.add(hit)
                elif k=="cloud": cloud.add(hit)
                elif k=="secret": secret.add(hit)
    for k, pat in PAT.items():
        for hit in pat.findall(html):
            if k=="athsubs": athsubs.add(hit.lower())
            elif k=="api": api.add(hit)

    def w(fn, data):
        with open(os.path.join(JS_DIR, fn), "w") as f:
            f.write("\n".join(sorted(data)) + ("\n" if data else ""))
    w(f"{name}_urls.txt", urls)
    w(f"{name}_subdomains.txt", athsubs)
    w(f"{name}_api_endpoints.txt", api)
    w(f"{name}_cloud.txt", cloud)
    w(f"{name}_secret_candidates.txt", secret)
    print(f"[*] {name}: urls={len(urls)} athsubs={len(athsubs)} api={len(api)} cloud={len(cloud)} secret_cand={len(secret)}", file=sys.stderr)

print("DONE")
