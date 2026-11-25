#!/usr/bin/env python3
"""
SSRF RECON — Phase 0 (read-only, no requests, no OOB needed).

Parses a gau/wayback URL dump and extracts candidate SSRF injection points:
  - URLs whose QUERY parameters match SSRF-prone names (url, file, redirect,
    webhook, import, avatar-by-URL, etc.)
  - PATH segments that look like proxy/fetch/import features.

Output = prioritized test list. Safe: it only reads the local URL file and
prints candidates. No outbound requests are made here.

Usage:
  python3 ssrf_recon.py [path_to_urls.txt]
  (defaults to /home/user/Bugbounty/issuehunt/gau_api_new4_inscope.txt)
"""
import re, sys, os
from collections import OrderedDict

DEFAULT = "/home/user/Bugbounty/issuehunt/gau_api_new4_inscope.txt"

# SSRF-prone parameter names
PARAMS = [
 "url","uri","link","src","href","file","doc","document","path","page","site",
 "html","image","img","media","video","audio","redirect","redirect_to",
 "redirecturl","redir","next","continue","return","ret","returnurl","to",
 "target","callback","webhook","hook","proxy","load","fetch","fetch_url",
 "import","feed","rss","api","endpoint","host","domain","ip","address",
 "server","data","u","nav","goto","open","srcdoc","remote","source","base",
 "ref","preview","thumbnail","avatar","photo","picture","resource","rurl",
 "external","view","frame","siteurl","pageurl","srcpage","ow2v5smg0tvlurl",
]
PARAM_RE = re.compile(r"[?&](%s)=([^&]*)" % "|".join(re.escape(p) for p in PARAMS), re.I)

# path segments that imply server-side fetch/proxy
PATH_FEATURES = re.compile(r"/(proxy|fetch|import|load|remote|webhook|callback|"
                           r"redirect|rss|feed|avatar|preview|thumbnail|"
                           r"translate|convert|screenshot|render|open|src)/", re.I)

def main():
    src = sys.argv[1] if len(sys.argv) > 1 else DEFAULT
    if not os.path.exists(src):
        print(f"[!] URL file not found: {src}")
        sys.exit(1)
    lines = [l.strip() for l in open(src, errors="ignore") if l.strip()]
    print(f"Loaded {len(lines)} URLs from {src}\n")

    param_hits = OrderedDict()   # (host, param) -> example url
    path_hits = OrderedDict()    # host -> example url
    seen_hosts = set()

    for u in lines:
        host = re.sub(r"^(https?://[^/]+).*", r"\1", u)
        seen_hosts.add(host)
        for m in PARAM_RE.finditer(u):
            pname = m.group(1).lower()
            param_hits.setdefault((host, pname), u)
        if PATH_FEATURES.search(u):
            path_hits.setdefault(host, u)

    print("="*70)
    print(f"SSRF-PRONE PARAMETERS: {len(param_hits)} (host+param unique)")
    print("="*70)
    # group by param name frequency
    byparam = {}
    for (host, p), ex in param_hits.items():
        byparam.setdefault(p, []).append((host, ex))
    for p in sorted(byparam, key=lambda k: -len(byparam[k])):
        print(f"\n  param '{p}'  ->  {len(byparam[p])} host(s)")
        for host, ex in byparam[p][:5]:
            print(f"    {host}    e.g. {ex[:90]}")

    print("\n" + "="*70)
    print(f"PROXY/FETCH/IMPORT PATH FEATURES: {len(path_hits)} host(s)")
    print("="*70)
    for host, ex in sorted(path_hits.items()):
        print(f"  {host}\n      {ex[:100]}")

    print("\nDONE — Phase-0 only. No requests sent, no OOB required.")
    print("Next: stand up an OOB host (interactsh / Burp Collaborator), then")
    print("inject http://<id>.interact.sh/ into each candidate param and watch")
    print("for inbound DNS/HTTP — that is the real blind-SSRF proof.")

if __name__ == "__main__":
    main()
