#!/usr/bin/env python3
"""Pull an Instagram profile's bio, posts, captions, and profile-pic URL via the
public web_profile_info GraphQL endpoint. Use when a CTF planted secret names an IG
handle (e.g. "IG calls me Influencer at 16.404_127"). Expect the profile to be
MISDIRECTION; this just proves it and collects images for binwalk/zbar/vision.

Usage:  python3 ig_profile_pull.py <username> [outdir]
Needs:  requests (or works with urllib). The IG mobile UA is required or the endpoint
        returns "useragent mismatch".
"""
import sys, json, os, urllib.request

UA = "Instagram 269.0.0.18.75 Android"
URL = "https://www.instagram.com/api/v1/users/web_profile_info/?username={}"


def fetch(username):
    req = urllib.request.Request(URL.format(username), headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.load(r)


def main():
    if len(sys.argv) < 2:
        print("usage: ig_profile_pull.py <username> [outdir]"); sys.exit(1)
    user = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else "."
    os.makedirs(out, exist_ok=True)
    d = fetch(user)
    u = d.get("data", {}).get("user")
    if not u:
        print("no user:", str(d)[:200]); return
    print("FULL:", u.get("full_name"))
    print("BIO :", repr(u.get("biography")))
    print("EXT :", u.get("external_url"))
    print("PICP:", u.get("profile_pic_url"))
    posts = u["edge_owner_to_timeline_media"]["edges"]
    print("POSTS:", len(posts))
    for i, p in enumerate(posts):
        n = p["node"]
        cap = n["edge_media_to_caption"]["edges"]
        c = cap[0]["node"]["text"] if cap else ""
        print(f"  [{i}] CAP: {c!r}")
        print(f"       IMG: {n.get('display_url')}")
        # save image for offline stego checks
        try:
            iu = n.get("display_url")
            if iu:
                with urllib.request.urlopen(urllib.request.Request(iu, headers={"User-Agent": UA}), timeout=30) as ri:
                    open(os.path.join(out, f"post_{i}.jpg"), "wb").write(ri.read())
        except Exception as e:
            print("    img dl fail:", e)
    # save profile pic
    try:
        pu = u.get("profile_pic_url")
        if pu:
            with urllib.request.urlopen(urllib.request.Request(pu, headers={"User-Agent": UA}), timeout=30) as rp:
                open(os.path.join(out, "prof.jpg"), "wb").write(rp.read())
    except Exception as e:
        print("prof pic dl fail:", e)


if __name__ == "__main__":
    main()
