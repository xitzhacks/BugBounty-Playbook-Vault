#!/usr/bin/env python3
"""Comprehensive secret scanner for JS files.

Usage:
    python3 scan_secrets.py [JS_DIR]

If JS_DIR is omitted, uses the path hardcoded below (edit to your target).
Writes machine-readable results to <JS_DIR>/../secret_scan_results.json
and prints a triage-ready console report.

IMPORTANT: This scanner is a LEAD GENERATOR. Every high-signal match must be
manually verified (see js-secret-scan skill §4 triage rules) before being
called a real secret. Frontend JS is public by definition.
"""
import re, os, sys, json
from math import log2

DEFAULT_JS_DIR = "/home/user/Bugbounty/issuehunt/js_files"

PATTERNS = {
    "AWS Access Key ID": re.compile(r"AKIA[0-9A-Z]{16}"),
    "AWS Secret Access Key": re.compile(r"(?i)aws_secret_access_key[\"'=:\s]{1,20}[A-Za-z0-9/+=]{40}"),
    "AWS Session Token": re.compile(r"ASIA[0-9A-Z]{16}"),
    "Google API Key": re.compile(r"AIza[0-9A-Za-z\-_]{35}"),
    "Google OAuth Client ID": re.compile(r"[0-9]+-[0-9A-Za-z_]{20,}\.apps\.googleusercontent\.com"),
    "Stripe Live Key": re.compile(r"sk_live_[0-9A-Za-z]{16,}", re.I),
    "Stripe Restricted Key": re.compile(r"rk_live_[0-9A-Za-z]{16,}", re.I),
    "Stripe Publishable Key": re.compile(r"pk_live_[0-9A-Za-z]{16,}", re.I),
    "Stripe Test Secret": re.compile(r"sk_test_[0-9A-Za-z]{16,}", re.I),
    "Slack Token": re.compile(r"xox[baprs]-[0-9A-Za-z\-]{10,}"),
    "Slack Webhook": re.compile(r"https://hooks\.slack\.com/services/[A-Za-z0-9/]+"),
    "GitHub Token": re.compile(r"gh[pousr]_[A-Za-z0-9]{36,}"),
    "GitLab PAT": re.compile(r"glpat-[0-9A-Za-z_\-]{20,}"),
    "Generic API Key Assignment": re.compile(r"(?i)(api[_-]?key|apikey|secret[_-]?key|access[_-]?token|client[_-]?secret|private[_-]?key|auth[_-]?token|bearer)[\"'=:\s]{1,25}[A-Za-z0-9_\-\.]{12,}"),
    "JWT (header.payload.sig)": re.compile(r"eyJ[A-Za-z0-9_\-]{10,}\.eyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}"),
    "Private Key Block": re.compile(r"-----BEGIN (?:RSA |EC |DSA |OPENSSH |PGP )?PRIVATE KEY-----"),
    "SSH Private Key": re.compile(r"-----BEGIN OPENSSH PRIVATE KEY-----"),
    "PEM Certificate": re.compile(r"-----BEGIN CERTIFICATE-----"),
    "Basic Auth in URL": re.compile(r"https?://[A-Za-z0-9_\-]+:[A-Za-z0-9_\-]+@[A-Za-z0-9\.\-]+"),
    "Firebase URL": re.compile(r"https://[a-z0-9\-]+\.firebaseio\.com"),
    "Twilio SID": re.compile(r"AC[0-9a-fA-F]{32}"),
    "Twilio API Key": re.compile(r"SK[0-9a-fA-F]{32}"),
    "SendGrid Key": re.compile(r"SG\.[A-Za-z0-9_\-]{16,}\.[A-Za-z0-9_\-]{16,}"),
    "Mailgun Key": re.compile(r"key-[0-9A-Za-z]{32,}"),
    "PayPal Braintree": re.compile(r"(?i)access_token\$production\$[0-9a-z]{16,}\$[0-9a-f]{32,}"),
    "Facebook Access Token": re.compile(r"(?i)(fb|facebook)[_a-z]*(access_token|app_secret)[\"'=:\s]{1,20}[A-Za-z0-9]{20,}"),
    "Twitter API Key": re.compile(r"(?i)(twitter|consumer)(api_key|secret|access_token|access_secret)[\"'=:\s]{1,20}[A-Za-z0-9]{20,}"),
    "NPM Token": re.compile(r"npm_[0-9A-Za-z]{36,}"),
    "Telegram Bot Token": re.compile(r"\d{8,10}:[A-Za-z0-9_\-]{35,}"),
    "Discord Webhook": re.compile(r"https://discord(?:app)?\.com/api/webhooks/[0-9]+/[A-Za-z0-9_\-]+"),
    "Discord Bot Token": re.compile(r"[MN][A-Za-z0-9_\-]{23,25}\.[A-Za-z0-9_\-]{6,}\.[A-Za-z0-9_\-]{27,}"),
    "Sentry DSN": re.compile(r"https://[0-9a-f]{32,}@sentry\.io/[0-9]+"),
    "Azure Connection String": re.compile(r"(?i)AccountKey=[A-Za-z0-9+/=]{40,}"),
    "OpenAI API Key": re.compile(r"sk-[A-Za-z0-9]{20,}"),
    "Anthropic API Key": re.compile(r"sk-ant-[A-Za-z0-9\-]{20,}"),
    "HuggingFace Token": re.compile(r"hf_[A-Za-z0-9]{20,}"),
    "Mapbox Token": re.compile(r"pk\.[A-Za-z0-9_\-]{50,}"),
    "Shopify Access Token": re.compile(r"shpat_[0-9A-Za-z]{32,}"),
    "Square Token": re.compile(r"sq0atp-[0-9A-Za-z\-_]{22,}"),
    "Square Secret": re.compile(r"sq0csp-[0-9A-Za-z\-_]{43,}"),
    "S3 Bucket URL": re.compile(r"https?://[a-z0-9\.\-]+\.s3(?:\.|\-)[a-z0-9\-]+\.amazonaws\.com"),
    "Database Connection String": re.compile(r"(?i)(mongodb(\+srv)?|postgres(ql)?|mysql|redis|amqp)://[^\s'\"]+"),
    "Password Assignment": re.compile(r"(?i)(password|passwd|pwd)[\"'=:\s]{1,15}[^\s'\"]{6,}"),
    "Encryption Key": re.compile(r"(?i)(encryption_key|secret_key|signing_key|cipher_key|aes_key)[\"'=:\s]{1,25}[A-Za-z0-9_\-+/=]{16,}"),
    "Credit Card (loose)": re.compile(r"\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13}|6(?:011|5[0-9]{2})[0-9]{12})\b"),
}

HEX_RE = re.compile(r"^[0-9a-fA-F]+$")
B64_RE = re.compile(r"^[A-Za-z0-9+/=_\-]+$")

def shannon_entropy(s):
    if not s:
        return 0.0
    freq = {}
    for c in s:
        freq[c] = freq.get(c, 0) + 1
    n = len(s)
    return -sum((v / n) * log2(v / n) for v in freq.values())

def looks_like_secret(s):
    if len(s) < 16:
        return False
    if HEX_RE.match(s) and len(s) in (32, 40, 64):
        return False
    if not B64_RE.match(s):
        return False
    return shannon_entropy(s) >= 4.5

ASSIGN_CTX = re.compile(
    r"(?i)(?:const|let|var|window\.|globalThis\.|self\.|exports\.)?\s*"
    r"([\w\.]*?(?:key|token|secret|password|passwd|pwd|auth|api|client|credential|private)[A-Za-z0-9_\.\-]*)"
    r"\s*[:=]\s*([\"'`])([^\"'`]{16,120})\2"
)

def scan_file(path):
    results = {name: [] for name in PATTERNS}
    entropy_hits, ctx_hits = [], []
    try:
        with open(path, "r", errors="ignore") as f:
            content = f.read()
    except Exception as e:
        return None, str(e)

    lines = content.splitlines()
    for name, rx in PATTERNS.items():
        for i, line in enumerate(lines, 1):
            for m in rx.finditer(line):
                snippet = m.group(0)
                if name in ("Datadog Key", "Cloudflare Global API Key") and not looks_like_secret(snippet):
                    continue
                results[name].append((i, snippet[:200]))

    for m in ASSIGN_CTX.finditer(content):
        key, val = m.group(1), m.group(3)
        if looks_like_secret(val) or len(val) >= 20:
            ln = content[:m.start()].count("\n") + 1
            ctx_hits.append((ln, key, val[:200]))

    STR_RE = re.compile(r"[\"'`]([A-Za-z0-9_\-+/=]{20,120})[\"'`]")
    for m in STR_RE.finditer(content):
        s = m.group(1)
        if looks_like_secret(s):
            ln = content[:m.start()].count("\n") + 1
            entropy_hits.append((ln, s[:200]))

    return {"patterns": results, "context": ctx_hits, "entropy": entropy_hits}, None

HIGH_SIGNAL = ["AWS Access Key ID","AWS Secret Access Key","Google API Key","Google OAuth Client ID",
               "Stripe Live Key","Stripe Restricted Key","Slack Token","Slack Webhook","GitHub Token",
               "GitLab PAT","JWT (header.payload.sig)","Private Key Block","SSH Private Key",
               "Basic Auth in URL","Twilio SID","SendGrid Key","Mailgun Key","OpenAI API Key",
               "Anthropic API Key","Telegram Bot Token","Discord Webhook","Discord Bot Token",
               "Sentry DSN","Azure Connection String","Database Connection String",
               "Square Token","Square Secret","Shopify Access Token","Mapbox Token",
               "HuggingFace Token","NPM Token","Firebase URL","S3 Bucket URL","Credit Card (loose)"]

def main():
    js_dir = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_JS_DIR
    if not os.path.isdir(js_dir):
        print(f"[!] JS dir not found: {js_dir}")
        sys.exit(1)
    files = sorted(f for f in os.listdir(js_dir) if f.endswith(".js"))
    print(f"Scanning {len(files)} JS files in {js_dir}")
    all_findings, summary = {}, {}
    for f in files:
        res, err = scan_file(os.path.join(js_dir, f))
        if err:
            print(f"[!] Error reading {f}: {err}")
            continue
        pat_counts = {k: len(v) for k, v in res["patterns"].items() if v}
        total = sum(pat_counts.values()) + len(res["context"]) + len(res["entropy"])
        if total > 0:
            all_findings[f] = res
            summary[f] = {"patterns": pat_counts, "context": len(res["context"]),
                          "entropy": len(res["entropy"]), "total": total}

    print("="*80)
    print("SECRET SCAN REPORT")
    print("="*80)
    if not summary:
        print("No potential secrets found.")
        return

    for f in sorted(summary, key=lambda x: -summary[x]["total"]):
        s = summary[f]
        print(f"\n[FILE] {f}  —  total suspicious: {s['total']}")
        for pat, cnt in sorted(s["patterns"].items(), key=lambda x: -x[1]):
            print(f"    - {pat}: {cnt}")

    print("\n" + "="*80)
    print("HIGH-SIGNAL MATCHES (MANUALLY VERIFY EACH -- see triage rules)")
    print("="*80)
    found_high = False
    for f in all_findings:
        for pat in HIGH_SIGNAL:
            hits = all_findings[f]["patterns"].get(pat, [])
            if hits:
                found_high = True
                print(f"\n{f}  ::  {pat}")
                for ln, snip in hits[:10]:
                    print(f"    L{ln}: {snip}")
    if not found_high:
        print("None of the highest-confidence secret formats matched.")

    print("\n" + "="*80)
    print("CONTEXT-BASED POSSIBLE SECRETS (key=secret assignments)")
    print("="*80)
    ctx_total = 0
    for f in all_findings:
        for ln, key, val in all_findings[f]["context"][:40]:
            ctx_total += 1
            print(f"{f} L{ln}  {key} = {val}")
    if ctx_total == 0:
        print("None.")

    print("\n" + "="*80)
    print("HIGH-ENTROPY STANDALONE STRINGS (sample; may include non-secrets)")
    print("="*80)
    ent_total = 0
    for f in all_findings:
        for ln, s in all_findings[f]["entropy"][:30]:
            ent_total += 1
            print(f"{f} L{ln}: {s}")
    if ent_total == 0:
        print("None.")

    out = os.path.join(os.path.dirname(js_dir.rstrip("/")), "secret_scan_results.json")
    with open(out, "w") as f:
        json.dump(all_findings, f, indent=2)
    print("\n" + "="*80)
    print(f"Full results saved to: {out}")

if __name__ == "__main__":
    main()
