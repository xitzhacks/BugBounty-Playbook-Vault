#!/usr/bin/env python3
"""
PII audit for a directory of engagement artifacts.

Answers the question every unauthenticated-data-exposure finding provokes:

    "is there any user data leaked in this?"

METHOD
  1. Regex-scan every artifact for PII SHAPES (email, phone, passport, civil ID,
     IBAN, Arabic names, PII-named JSON fields).
  2. RESOLVE every hit by printing +/-200 chars of surrounding context.
  3. Run a structured check on any JSON: field NAMES reveal whether personal
     fields exist at all, independent of whether a value matched a regex.

The job is NOT to find regex matches. The job is to prove each match is, or is
not, a person. Most hits in a webapp assessment are false positives:
  - Liferay CMS articleId in a help-widget URL  -> ?articleId=1005007009
  - Google Analytics property ID                -> gtag/js?id=UA-130602337-1
  - HSTS max-age header value (seconds)         -> max-age=16070400
  - Epoch-millisecond build timestamps          -> 148500557500 (1974-09-15)
  - Framework constants inside engine.js
  - The tester's OWN test data and placeholder values

Resolve before you answer. "A regex matched a 10-digit number" is not a leak
claim, and neither is its denial.

USAGE
  python3 pii_audit.py <artifacts_dir>
  python3 pii_audit.py ~/Bugbounty/<target> \
      --own-marker maxxspace --own-marker xitztest --own-marker test@

Exit code 0 always (this is a reporting tool, not a gate).
"""

import argparse
import datetime
import glob
import json
import os
import re

PII_PATTERNS = {
    "email":       r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
    "phone":       r"(?:\+968|00968|\+\d{1,3})[\s-]?\d{7,10}\b",
    "passport_no": r"\b[A-Z]{1,2}\d{6,8}\b",
    "civil_id":    r"\b\d{8,12}\b",
    "iban":        r"\b[A-Z]{2}\d{2}[A-Z0-9]{10,30}\b",
    "arabic_name": r"[\u0600-\u06FF]{3,}",
    "pii_field":   r'"(?:firstName|lastName|fullName|passportNumber|civilId|'
                   r'mobileNo|emailId|dateOfBirth|address|nationality)"\s*:',
}

# Field names that, if present as JSON keys, mean the response really is personal.
PERSONAL_KEYS = {
    "name", "firstname", "lastname", "fullname", "passportnumber", "civilid",
    "mobile", "mobileno", "email", "emailid", "dob", "dateofbirth", "address",
    "nationality", "gender", "birthdate",
}

BINARY_EXT = (".png", ".jpg", ".jpeg", ".gif", ".gz", ".zip", ".pdf", ".ico")


def resolve_hits(raw, label, pat):
    """Return the regex hits AND the context that identifies what they are."""
    out = []
    for m in re.finditer(pat, raw):
        i = m.start()
        ctx = re.sub(r"\s+", " ", raw[max(0, i - 200):i + 200])
        out.append((m.group(0), ctx))
    return out


def classify_context(ctx):
    """Heuristic label for WHY a hit is probably benign. Advisory only."""
    c = ctx.lower()
    if "articleid=" in c:
        return "Liferay CMS articleId (content page ID, same for all visitors)"
    if "gtag/js?id=ua-" in c or "gtag('config'" in c:
        return "Google Analytics property ID"
    if "max-age=" in c and "strict-transport-security" in c:
        return "HSTS max-age header value (seconds)"
    if "set-cookie" in c or "jsessionid" in c:
        return "session cookie material (redact, not user PII)"
    if "javascript" in c or "<script" in c:
        return "framework/JS constant"
    return "UNRESOLVED — inspect manually"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dir", help="artifacts directory to audit")
    ap.add_argument("--own-marker", action="append", default=[],
                    help="substring identifying the tester's OWN test data "
                         "(repeatable). Hits containing it are not third-party PII.")
    ap.add_argument("--context", action="store_true",
                    help="print surrounding context for every hit")
    args = ap.parse_args()

    own = [m.lower() for m in args.own_marker]
    print("=" * 74)
    print(f"PII AUDIT — {args.dir}")
    print("=" * 74)
    if own:
        print(f"own-markers (filtered out): {own}\n")

    any_hit = False
    for path in sorted(glob.glob(os.path.join(args.dir, "*"))):
        if os.path.isdir(path) or path.endswith(BINARY_EXT):
            continue
        try:
            raw = open(path, encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        if not raw:
            continue

        per_file = []
        for label, pat in PII_PATTERNS.items():
            for val, ctx in resolve_hits(raw, label, pat):
                if any(o in str(val).lower() or o in ctx.lower() for o in own):
                    continue
                per_file.append((label, val, ctx))

        if per_file:
            any_hit = True
            print(f"\n{os.path.basename(path)}:")
            seen = set()
            for label, val, ctx in per_file:
                key = (label, val)
                if key in seen:
                    continue
                seen.add(key)
                print(f"   [{label}] {val}")
                print(f"      -> {classify_context(ctx)}")
                if args.context:
                    print(f"      ctx: {ctx[:220]}")

    if not any_hit:
        print("\nNO third-party PII found in any artifact.")

    # ---- structured check: field NAMES, independent of value matching ----
    print("\n" + "=" * 74)
    print("STRUCTURED DATA CHECK (do field names reveal personal data?)")
    print("=" * 74)
    for path in sorted(glob.glob(os.path.join(args.dir, "*.json"))):
        try:
            data = json.load(open(path, encoding="utf-8"))
        except Exception:
            continue
        recs = data if isinstance(data, list) else [data]
        keys = sorted({k for r in recs if isinstance(r, dict) for k in r})
        if not keys:
            continue
        personal = [k for k in keys if k.lower() in PERSONAL_KEYS]
        n = len(recs) if isinstance(data, list) else 1
        print(f"\n{os.path.basename(path)}: {n} record(s)")
        print(f"  fields: {keys}")
        print(f"  personal-data fields: {personal if personal else 'NONE'}")
        print("  -> reference/config data only" if not personal
              else "  -> CONTAINS PERSONAL-DATA FIELDS — inspect values")

    print("\n" + "-" * 74)
    print("REMINDER: a resolved-benign hit is a POSITIVE result for the report.")
    print("'No PII, reference data only' with this audit attached is what makes a")
    print("Medium 5.3 defensible. An unresolved hit must be resolved before you")
    print("either claim a leak or deny one.")


if __name__ == "__main__":
    main()
