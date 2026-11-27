#!/usr/bin/env python3
"""Shared redaction rules for the public vault build.

Every rule replaces the sensitive value with a visible marker so the technique
in a write-up stays readable while the credential/identity does not ship.

Build-host note: the `path` rule and a few example patterns were written for this
build machine (/home/kali, kali@parrot, xitzhack). They are intentional historical
rules, not generic OS-agnostic defaults; other hosts do not need to match them.
"""
import re

MARK = {
    "private_key": "[REDACTED_PRIVATE_KEY]",
    "aws_key": "[REDACTED_AWS_KEY]",
    "github_token": "[REDACTED_GITHUB_TOKEN]",
    "slack_token": "[REDACTED_SLACK_TOKEN]",
    "google_key": "[REDACTED_GOOGLE_KEY]",
    "stripe_key": "[REDACTED_STRIPE_KEY]",
    "twilio_key": "[REDACTED_TWILIO_KEY]",
    "sendgrid_key": "[REDACTED_SENDGRID_KEY]",
    "mailgun_key": "[REDACTED_MAILGUN_KEY]",
    "jwt": "[REDACTED_JWT]",
    "ngrok_token": "[REDACTED_NGROK_TOKEN]",
    "bearer": r"\1[REDACTED_BEARER]",
    "url_creds": r"\1[REDACTED_CREDS]@",
    "email": "[REDACTED_EMAIL]",
    "path": "/home/user",
}

PLACEHOLDER = re.compile(
    r"^(?:"
    r"your[_-]?|example|sample|dummy|fake|test|placeholder|"
    r"x{3,}|X{3,}|\.{3,}|<[^>]*>|\{\{.*\}\}|\$\{?[A-Z_]+\}?|%[sd]|"
    r"password$|passwd$|secret$|changeme|change[_-]?me|admin$|root$|"
    r"null|none|nil|true|false|undefined|"
    r"[*•█]+|\[REDACTED[^\]]*\]|"
    r"0+$|1{3,}$|123456|qwerty"
    r")",
    re.I,
)

# (name, compiled regex, replacement)
RULES = [
    ("private_key", re.compile(
        r"-----BEGIN (?:[A-Z0-9 ]+ )?PRIVATE KEY-----.*?-----END (?:[A-Z0-9 ]+ )?PRIVATE KEY-----", re.S),
     MARK["private_key"]),
    ("aws_key", re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b"), MARK["aws_key"]),
    ("github_token", re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{36,}|github_pat_[A-Za-z0-9_]{22,})\b"),
     MARK["github_token"]),
    ("slack_token", re.compile(r"\bxox[baprs]-[0-9A-Za-z-]{10,}\b"), MARK["slack_token"]),
    ("google_key", re.compile(r"\bAIza[0-9A-Za-z\-_]{35}\b"), MARK["google_key"]),
    ("stripe_key", re.compile(r"\b(?:sk|rk)_(?:live|test)_[0-9A-Za-z]{16,}\b"), MARK["stripe_key"]),
    ("twilio_key", re.compile(r"\bSK[0-9a-fA-F]{32}\b"), MARK["twilio_key"]),
    ("sendgrid_key", re.compile(r"\bSG\.[A-Za-z0-9\-_]{22}\.[A-Za-z0-9\-_]{43}\b"), MARK["sendgrid_key"]),
    ("mailgun_key", re.compile(r"\bkey-[0-9a-zA-Z]{32}\b"), MARK["mailgun_key"]),
    ("jwt", re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b"),
     MARK["jwt"]),
    ("ngrok_token", re.compile(r"((?:authtoken|ngrok)[^\n]{0,40}?[=:]\s*[\"']?)([0-9A-Za-z_]{30,})", re.I),
     r"\1" + MARK["ngrok_token"]),
    ("bearer", re.compile(r"\b(Bearer\s+)[A-Za-z0-9\-_.=]{20,}"), MARK["bearer"]),
    ("url_creds", re.compile(r"\b([a-z][a-z0-9+.-]*://)[^/\s:@]+:[^/\s@]{3,}@"), MARK["url_creds"]),
    ("openai_key", re.compile(r"\bsk-(?:proj-|ant-)?[A-Za-z0-9_-]{32,}\b"), "[REDACTED_API_KEY]"),
    ("anthropic_key", re.compile(r"\bsk-ant-[A-Za-z0-9_-]{20,}\b"), "[REDACTED_API_KEY]"),
    ("huggingface_key", re.compile(r"\bhf_[A-Za-z0-9]{30,}\b"), "[REDACTED_API_KEY]"),
    ("gitlab_token", re.compile(r"\bglpat-[A-Za-z0-9_-]{20,}\b"), "[REDACTED_GITLAB_TOKEN]"),
    ("npm_token", re.compile(r"\bnpm_[A-Za-z0-9]{36}\b"), "[REDACTED_NPM_TOKEN]"),
    ("discord_webhook", re.compile(r"https://(?:discord|discordapp)\.com/api/webhooks/[0-9]+/[A-Za-z0-9_-]+"),
     "https://discord.com/api/webhooks/[REDACTED]"),
    ("telegram_bot", re.compile(r"\b\d{8,10}:[A-Za-z0-9_-]{35}\b"), "[REDACTED_TELEGRAM_TOKEN]"),
    # Facebook/Meta access tokens: EAA... ~200+ chars. GitHub's secret scanner
    # blocks the push on these, so the public build must redact them.
    ("facebook_token", re.compile(r"\bEAA[A-Za-z0-9]{20,}\b"), "[REDACTED_FACEBOOK_TOKEN]"),
]

OBFUSCATED_EMAIL = re.compile(
    r"\b[A-Za-z0-9._%+-]+\s*(?:\[|\(|\{)\s*at\s*(?:\]|\)|\})\s*[A-Za-z0-9.-]+\s*(?:\[|\(|\{)\s*dot\s*(?:\]|\)|\})\s*[A-Za-z]{2,}\b",
    re.I)

EMAIL_RX = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
GENERIC_RX = re.compile(
    r"((?:password|passwd|pwd|secret|api[_-]?key|apikey|access[_-]?token|auth[_-]?token|client[_-]?secret)"
    r"\s*[:=]\s*[\"']?)([^\s\"'<>,;]{6,80})", re.I)
PATH_RX = re.compile(re.escape("/home/" "kali") + r"\b")
PII_RX = re.compile(r"\bkali@" r"parrot\b|\bxitz" r"hack\b", re.I)


def scrub(text):
    """Return (scrubbed_text, counts_dict)."""
    if not text or not isinstance(text, str):
        return text, {}
    counts = {}
    out = text

    for name, rx, repl in RULES:
        out, n = rx.subn(repl, out)
        if n:
            counts[name] = counts.get(name, 0) + n

    def _generic(m):
        val = m.group(2)
        if PLACEHOLDER.match(val):
            return m.group(0)
        counts["generic_secret"] = counts.get("generic_secret", 0) + 1
        return m.group(1) + "[REDACTED_SECRET]"

    out = GENERIC_RX.sub(_generic, out)

    out, n = EMAIL_RX.subn(MARK["email"], out)
    if n:
        counts["email"] = counts.get("email", 0) + n

    out, n = OBFUSCATED_EMAIL.subn(MARK["email"], out)
    if n:
        counts["email"] = counts.get("email", 0) + n

    out, n = PATH_RX.subn(MARK["path"], out)
    if n:
        counts["path"] = counts.get("path", 0) + n

    out, n = PII_RX.subn("[REDACTED_PII]", out)
    if n:
        counts["pii"] = counts.get("pii", 0) + n

    return out, counts


def is_binary(path):
    low = path.lower()
    if ".part-" in low:
        return True
    return low.endswith((
        ".sqlite", ".db", ".sqlite-wal", ".sqlite-shm", ".zip", ".gz", ".bz2", ".xz",
        ".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".pdf",
        ".woff", ".woff2", ".ttf", ".otf", ".eot", ".mp4", ".mov", ".mp3", ".wav",
    ))
