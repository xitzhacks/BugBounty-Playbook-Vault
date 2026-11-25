#!/usr/bin/env python3
"""
Build a temporary local browsable dashboard over a findings/evidence tree.

Source tree shape (typical):
    <root>/<asset-folder>/<phase>/<finding-name>/<evidence files>
    <root>/<asset-folder>/<phase>/<finding-name>/<poc>.html
    <root>/<asset-folder>/<phase>/<finding-name>/<poc>.txt

Asset folder naming seen in the wild:
    FQ_0019_admin.app.dezaan.com
    IP_0373_41.77.173.33
    FQ_0075_agripal-zuul.olamagri.com - Out of scope

Phase dir naming varies: Finding / Revalidation / Closure.

Usage:
    python3 build_findings_dashboard.py \
        --source "/path/to/Findings part 1 - Updated" \
        --output "/path/to/Findings-Dashboard" \
        --template "/path/to/dashboard_template.html"

    # force thumbnail regeneration after source changes
    python3 build_findings_dashboard.py --source ... --output ... --rebuild-thumbs

The source tree is NEVER modified.
"""
import os
import re
import json
import shutil
import html
import hashlib
import argparse
import datetime
from pathlib import Path

PHASE_ORDER = ["Finding", "Revalidation", "Closure"]

# ---------------------------------------------------------------------------
# classification rules -- keys are normalised at load time (see norm())
# ---------------------------------------------------------------------------
CATS = [
    ("breach",             "Compression / Crypto Oracle"),
    ("brech",              "Compression / Crypto Oracle"),
    ("lucky13",            "Compression / Crypto Oracle"),
    ("beast",              "Compression / Crypto Oracle"),
    ("poodle",             "Compression / Crypto Oracle"),
    ("sweet32",            "Compression / Crypto Oracle"),
    ("rc4",                "Weak Cipher"),
    ("adhcipher",          "Weak Cipher"),
    ("sweet",              "Weak Cipher"),
    ("cipher",             "Weak Cipher"),
    ("expiressl",          "Weak Cipher"),
    ("expiredssl",         "Weak Cipher"),
    ("obsoletessl",        "Weak Cipher"),
    ("openssl eol",        "Weak Cipher"),
    ("nosslimplementation","Weak Cipher"),
    ("missingssl",         "Weak Cipher"),
    ("unencrypted",        "Weak Cipher"),
    ("telnet",             "Weak Cipher"),
    ("selfsigned",         "Weak Cipher"),
    ("weakencryptionencoding", "Weak Cipher"),
    ("clientinitiatedrenegotiation", "TLS Configuration"),
    ("renogotiation",      "TLS Configuration"),
    ("forwardsecrecy",     "TLS Configuration"),
    ("hsts",               "TLS Configuration"),
    ("ciphers",            "TLS Configuration"),
    ("tlsauth",            "TLS Configuration"),
    ("postgressql",        "End of Life"),
    ("sshv1",              "End of Life"),
    ("weakssh",            "End of Life"),
    ("ssrf",               "Server-Side Request Forgery"),
    ("openredirect",       "Open Redirect"),
    ("forcedbrowsing",     "Directory / Info Disclosure"),
    ("sitemap",            "Directory / Info Disclosure"),
    ("robots",             "Directory / Info Disclosure"),
    ("defaulterrorpage",   "Directory / Info Disclosure"),
    ("information",        "Information Disclosure"),
    ("sensitive",          "Information Disclosure"),
    ("senstive",           "Information Disclosure"),
    ("infoexpos",          "Information Disclosure"),
    ("infoexposure",       "Information Disclosure"),
    ("disclosed",          "Information Disclosure"),
    ("guid",               "Information Disclosure"),
    ("cookie",             "Cookie / Session"),
    ("cors",               "Access Control"),
    ("clickjack",          "Access Control"),
    ("dangerousmethods",   "Access Control"),
    ("csrf",               "Access Control"),
    ("rate limit",         "Rate Limiting"),
    ("ratelimit",          "Rate Limiting"),
    ("inputvalidation",    "Input Validation"),
    ("swagger",            "API Exposure"),
    ("knownvuln",          "Vulnerable Component"),
    ("knownvulner",        "Vulnerable Component"),
    ("vulnjs",             "Vulnerable Component"),
    ("vulnerablejs",       "Vulnerable Component"),
    ("js",                 "Vulnerable Component"),
    ("slowloris",          "Denial of Service"),
    ("dos",                "Denial of Service"),
    ("headers",            "Security Headers"),
    ("header",             "Security Headers"),
    ("csp",                "Security Headers"),
]

SEV_RULES = [
    ("ssrf",              "Critical"),
    ("rce",               "Critical"),
    ("sql",               "Critical"),
    ("openredirect",      "Medium"),
    ("clickjack",         "Medium"),
    ("cors",              "Medium"),
    ("rate limit",        "Medium"),
    ("ratelimit",         "Medium"),
    ("inputvalidation",   "Medium"),
    ("swagger",           "Medium"),
    ("dangerousmethods",  "Medium"),
    ("forwardsecrecy",    "Medium"),
    ("weakcipher",        "Medium"),
    ("cookie",            "Medium"),
    ("redirect",          "Medium"),
]

SEV_DEFAULT = {
    "Compression / Crypto Oracle":  "Medium",
    "Weak Cipher":                  "Medium",
    "TLS Configuration":            "Low",
    "End of Life":                  "Medium",
    "Server-Side Request Forgery":  "Critical",
    "Open Redirect":                "Medium",
    "Directory / Info Disclosure":  "Low",
    "Information Disclosure":       "Low",
    "Cookie / Session":             "Medium",
    "Access Control":               "Medium",
    "Rate Limiting":                "Medium",
    "Input Validation":             "Medium",
    "API Exposure":                 "Medium",
    "Vulnerable Component":         "High",
    "Denial of Service":            "High",
    "Security Headers":             "Low",
    "Other":                        "Info",
}

TEXT_EXTS = {".txt"}
HTML_EXTS = {".html", ".htm"}
IMG_EXTS = {".png"}


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def norm(s: str) -> str:
    """Lowercase and strip every non-alphanumeric char. Used for all matching."""
    return re.sub(r"[^a-z0-9]+", "", (s or "").lower())


# Rule keys are written in human form ("rate limit", "openssl eol"). Finding names
# are compared space-stripped, so the keys MUST be normalised the same way or they
# can never match -- which silently dumps every finding into "Other".
CATS = [(norm(k), v) for k, v in CATS]
SEV_RULES = [(norm(k), v) for k, v in SEV_RULES]


def slug(s: str) -> str:
    s = re.sub(r"[^A-Za-z0-9._-]+", "-", s).strip("-")
    return s or "x"


def safe_name(rel: str) -> str:
    """Unique, readable filename for a copy of a source asset."""
    p = Path(rel)
    h = hashlib.md5(rel.encode()).hexdigest()[:8]
    return f"{slug(p.stem)[:70]}_{h}{p.suffix.lower()}"


def thumb_name(rel: str) -> str:
    """Thumbnails are written as JPEG -- the extension must match the format."""
    p = Path(rel)
    h = hashlib.md5(rel.encode()).hexdigest()[:8]
    return f"{slug(p.stem)[:70]}_{h}.jpg"


def asset_type(folder: str) -> str:
    return "IP" if folder.upper().startswith("IP_") else "FQDN"


def asset_id(folder: str) -> str:
    """FQ_0019_admin.app.dezaan.com -> FQ_0019 (unique -- NOT just 'FQ')."""
    m = re.match(r"^([A-Za-z]+_\d+)", folder)
    return m.group(1) if m else folder[:12]


def host_of(folder: str) -> str:
    """FQ_0019_admin.app.dezaan.com -> admin.app.dezaan.com"""
    s = re.sub(r"^[A-Za-z]+_\d+_", "", folder)
    s = re.sub(r"\s*-\s*Out of scope\s*$", "", s, flags=re.I)
    return s.strip()


def classify(name: str):
    n = norm(name)
    cat = "Other"
    for k, v in CATS:
        if k in n:
            cat = v
            break
    sev = None
    for k, v in SEV_RULES:
        if k in n:
            sev = v
            break
    if sev is None:
        sev = SEV_DEFAULT.get(cat, "Info")
    return cat, sev


def status_of(name: str) -> str:
    """'... - Closed' / '... - Open' / '... - Closure' suffix drives the badge."""
    n = norm(name)
    if "closed" in n or "closure" in n:
        return "closed"
    if "open" in n:
        return "open"
    return "open"


# ---------------------------------------------------------------------------
# build
# ---------------------------------------------------------------------------
def build_thumbs(paths, outdir: Path, src: Path, force=False):
    """
    Resize PNGs to 640px JPEGs. Returns {relpath: 'thumbs/<file>'}.

    The mapping key MUST be the path RELATIVE to src -- that is the key the
    caller looks up with. Keying by the absolute path here silently produces
    an empty mapping and every image falls back to the full-res copy.
    """
    try:
        from PIL import Image
    except Exception as e:
        print(f"  [!] Pillow unavailable ({e}); falling back to raw PNGs")
        return {}

    outdir.mkdir(parents=True, exist_ok=True)
    mapping = {}
    for i, p in enumerate(paths, 1):
        rel = str(p.relative_to(src))
        tn = outdir / thumb_name(rel)
        if tn.exists() and not force:
            mapping[rel] = f"thumbs/{tn.name}"
            continue
        try:
            with Image.open(p) as im:
                im = im.convert("RGB")
                im.thumbnail((640, 640), Image.LANCZOS)
                im.save(tn, "JPEG", quality=78, optimize=True)
            mapping[rel] = f"thumbs/{tn.name}"
        except Exception as e:
            print(f"  [!] thumb failed {rel}: {e}")
            mapping[rel] = None
        if i % 100 == 0:
            print(f"  .. {i}/{len(paths)} thumbs")
    return mapping


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True, help="findings tree root")
    ap.add_argument("--output", required=True, help="dashboard output dir")
    ap.add_argument("--template", required=True, help="template html with __DATA__ placeholder")
    ap.add_argument("--rebuild-thumbs", action="store_true")
    args = ap.parse_args()

    SRC = Path(args.source).expanduser().resolve()
    OUT = Path(args.output).expanduser().resolve()
    TPL = Path(args.template).expanduser().resolve()

    if not SRC.is_dir():
        print(f"[!] source not found: {SRC}")
        return 1
    if not TPL.is_file():
        print(f"[!] template not found: {TPL}")
        return 1

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "_dashboard" / "assets").mkdir(parents=True, exist_ok=True)
    thumbs_dir = OUT / "thumbs"

    # ---- probe the tree -------------------------------------------------
    print("[*] scanning findings tree ...")
    imgs, txts, htmls = [], [], []
    for p in sorted(SRC.rglob("*")):
        if not p.is_file():
            continue
        e = p.suffix.lower()
        if e in IMG_EXTS:
            imgs.append(p)
        elif e in TEXT_EXTS:
            txts.append(p)
        elif e in HTML_EXTS:
            htmls.append(p)
    print(f"    {len(imgs)} img, {len(txts)} txt, {len(htmls)} html")

    print("[*] building thumbnails ...")
    thumb_map = build_thumbs(imgs, thumbs_dir, SRC, force=args.rebuild_thumbs)

    asset_dir = OUT / "_dashboard" / "assets"

    def store(p: Path) -> str:
        """Copy an evidence file into the output dir. The source is never modified."""
        rel = p.relative_to(SRC)
        dst = asset_dir / safe_name(str(rel))
        if not dst.exists() or dst.stat().st_size != p.stat().st_size:
            shutil.copy2(p, dst)
        return f"_dashboard/assets/{dst.name}"

    # ---- walk assets ----------------------------------------------------
    assets = []
    for folder in sorted(p for p in SRC.iterdir() if p.is_dir()):
        if folder.name.startswith("_"):
            continue
        aid = asset_id(folder.name)
        oos = "out of scope" in folder.name.lower()

        findings = []
        for ph_dir in sorted(folder.iterdir()):
            if not ph_dir.is_dir():
                continue
            ph = ph_dir.name
            for fdir in sorted(ph_dir.iterdir()):
                if not fdir.is_dir():
                    continue
                items = []
                for f in sorted(fdir.iterdir()):
                    if not f.is_file():
                        continue
                    rel = f.relative_to(SRC)
                    e = f.suffix.lower()
                    if e in IMG_EXTS:
                        t = thumb_map.get(str(rel))
                        items.append({
                            "kind": "img", "phase": ph, "rel": str(rel),
                            "src": t if t else store(f),
                            "full": store(f),
                        })
                    elif e in TEXT_EXTS:
                        try:
                            content = f.read_text(errors="replace")
                        except Exception:
                            content = ""
                        items.append({
                            "kind": "txt", "phase": ph, "rel": str(rel),
                            "content": content[:20000], "src": store(f),
                        })
                    elif e in HTML_EXTS:
                        items.append({
                            "kind": "html", "phase": ph, "rel": str(rel),
                            "src": store(f),
                        })
                if not items:
                    continue
                cat, sev = classify(fdir.name)
                # The key becomes a DOM id, so it MUST be unique per finding.
                # Truncating a long name can collide with another finding, so
                # append a short hash of the full path to guarantee uniqueness.
                full_key = f"{folder.name}__{ph}__{fdir.name}"
                key = slug(full_key)[:60] + "_" + hashlib.md5(full_key.encode()).hexdigest()[:8]
                findings.append({
                    "key": key,
                    "name": fdir.name, "phase": ph,
                    "status": status_of(fdir.name),
                    "cat": cat, "sev": sev, "phases": [ph], "items": items,
                })

        # merge same-named finding across phases (no-op when phases are disjoint)
        merged, order = {}, []
        for f in findings:
            k = norm(f["name"])
            if k in merged:
                m = merged[k]
                m["items"].extend(f["items"])
                if f["phase"] not in m["phases"]:
                    m["phases"].append(f["phase"])
            else:
                merged[k] = f
                order.append(k)
        findings = [merged[k] for k in order]
        for f in findings:
            f["phases"] = sorted(
                set(f["phases"]),
                key=lambda p: PHASE_ORDER.index(p) if p in PHASE_ORDER else 99,
            )
        findings.sort(key=lambda f: (0 if "closed" not in norm(f["name"]) else 1,
                                     f["name"].lower()))

        assets.append({
            "id": aid, "type": asset_type(folder.name),
            "host": host_of(folder.name), "folder": folder.name,
            "oos": oos, "findings": findings,
        })

    # ---- stats ----------------------------------------------------------
    n_find = sum(len(a["findings"]) for a in assets)
    n_open = sum(1 for a in assets for f in a["findings"] if f["status"] == "open")
    n_closed = n_find - n_open
    n_ev = sum(len(f["items"]) for a in assets for f in a["findings"])
    cats = {}
    for a in assets:
        for f in a["findings"]:
            cats[f["cat"]] = cats.get(f["cat"], 0) + 1

    data = {
        "assets": assets,
        "categories": cats,
        "catRules": [[k, v] for k, v in CATS],
        "sevRules": [[k, v] for k, v in SEV_RULES],
        "sevDefault": SEV_DEFAULT,
        "generated": datetime.datetime.now().isoformat(timespec="seconds"),
    }

    # ---- write output ---------------------------------------------------
    (OUT / "_dashboard" / "data.js").write_text(
        "window.__DATA__ = " + json.dumps(data, ensure_ascii=False) + ";\n",
        encoding="utf-8")

    print("[*] copying full-resolution evidence ...")
    for p in imgs:
        store(p)
    for p in txts:
        store(p)
    for p in htmls:
        store(p)

    tpl = TPL.read_text(encoding="utf-8")
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    (OUT / "index.html").write_text(tpl.replace("__DATA__", payload), encoding="utf-8")

    manifest = {
        "generated": data["generated"],
        "source": str(SRC),
        "counts": {
            "assets": len(assets), "findings": n_find, "open": n_open,
            "closed": n_closed, "evidence_files": n_ev, "categories": len(cats),
        },
        "categories": cats,
        "assets": [
            {
                "id": a["id"], "type": a["type"], "host": a["host"], "oos": a["oos"],
                "findings": [
                    {"name": f["name"], "status": f["status"], "cat": f["cat"],
                     "sev": f["sev"], "phases": f["phases"], "items": len(f["items"])}
                    for f in a["findings"]
                ],
            }
            for a in assets
        ],
    }
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    # ---- self-check (the gates) -----------------------------------------
    print()
    print("[*] self-check ...")
    ids = [a["id"] for a in assets]
    dupes = {i for i in ids if ids.count(i) > 1}
    print(f"    gate 1 asset ids unique : {'PASS' if not dupes else 'FAIL ' + str(dupes)}")
    other = cats.get("Other", 0)
    print(f"    gate 2 uncategorised    : {other} (should be ~0)")
    missing = []
    for a in assets:
        for f in a["findings"]:
            for i in f["items"]:
                for k in ("src", "full"):
                    p = i.get(k)
                    if p and not (OUT / p).exists():
                        missing.append(p)
    print(f"    gate 3 missing files    : {len(missing)} {missing[:3]}")
    print()
    print(f"[+] dashboard built -> {OUT / 'index.html'}")
    print(f"    assets={len(assets)}  findings={n_find}  open={n_open}  closed={n_closed}")
    print(f"    evidence={n_ev}  categories={len(cats)}")
    print(f"    size: {sum(f.stat().st_size for f in OUT.rglob('*') if f.is_file())/1e6:.1f} MB")
    print()
    print("    serve with:  cd %s && python3 -m http.server 8899 --bind 127.0.0.1" % OUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
