#!/usr/bin/env python3
"""Build a technique index from the skills/vault doctrine.

Why: DVWA pass 3 showed the index answers technique names perfectly ("php filter chain" → rank 1)
but returns frontmatter for class names ("file inclusion"). This turns the section headings of the
doctrine into queryable technique rows, each pointing at the chunk that contains the how-to.

Table: techniques(id, name, class, chunk_id, path, source, keywords)
Tool:  vault_techniques(class|query) -> technique names + where to read them
"""
import os, re, sqlite3, time

DB = os.environ.get("VAULT_DB", os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "vault", "_VAULT", "reports.sqlite"))

TECH_RX = re.compile(r"bypass|payload|inject|traversal|wrapper|poison|enumerat|union|order\s*by|magic|polyglot|"
                     r"upload|smuggl|deserial|takeover|escalat|token|jwt|xxe|ssrf|idor|race|clickjack|template|"
                     r"ssti|webshell|command|dump|extract|filter|encod|confus|parser|redirect|cors|csrf|header|"
                     r"blind|time.based|oob|fuzz|brute|session|oauth|saml|graphql|nosql|ldap|xpath|prototype|"
                     r"cache|host.header|crlf|path|file\s*read|rce|exploit|chain", re.I)
NOISE = re.compile(r"^(related|anti-pattern|critical rules|when to use|overview|introduction|summary|"
                   r"contents|index|references|appendix|report template|checklist$|crown jewel|"
                   r"step \d+:|gate \d+|real-world finding|typical scores|severity escalation|"
                   r"report title|decision tree|bridge to|output format|key concepts|"
                   r"blogs index|fetched and|^\d+\s+[A-Z]{2,}-\d+|\$[\d,]+|^p\d+\s*[—-]|^\d+\s*[·.)]|^the url-in-upload|^the include that)", re.I)

CLASSES = [
    ("LFI",   r"lfi|file inclusion|traversal|wrapper|php://|log poison|local file"),
    ("SQLI",  r"\bsql\b|sqli|union select|order by|nosql"),
    ("XSS",   r"xss|cross.site|svg|dom|html inject|template"),
    ("SSRF",  r"ssrf"),
    ("IDOR",  r"idor|bfla|object reference"),
    ("RCE",   r"rce|command inject|code inject|deserial|webshell|upload|shell|template inject|ssti|filter chain"),
    ("UPLOAD",r"upload|magic byte|polyglot|extension|mime"),
    ("AUTH",  r"auth|2fa|otp|jwt|session|oauth|saml|password|token"),
    ("ACL",   r"access control|privilege|authoriz|idor|bfla"),
    ("CSRF",  r"csrf"),
    ("CRYPTO",r"crypto|certificate|tls|ssl|cipher|padding"),
    ("CONF",  r"cors|clickjack|header|hsts|cache|host header|misconfig|subdomain takeover"),
    ("INJ",   r"xxe|xml|smuggl|crlf|header inject|ldap|xpath|prototype"),
    ("DOS",   r"dos|resource|redos|exhaust"),
    ("LOGIC", r"race|business logic|toctou|coupon|price"),
]

PATH_CLASS = [
    ("LFI", r"hunt-lfi|file-inclusion|path-traversal|lfi"), ("SQLI", r"hunt-sqli|sql-injection|sqli"),
    ("XSS", r"hunt-xss|xss"), ("SSRF", r"hunt-ssrf|ssrf"), ("IDOR", r"hunt-idor|idor"),
    ("UPLOAD", r"upload"), ("RCE", r"hunt-rce|rce|deserial"),
    ("AUTH", r"hunt-auth|auth-bypass|hunt-session|jwt|oauth|saml|mfa|password"), ("ACL", r"hunt-mfa|privilege|access-control"),
    ("CSRF", r"hunt-csrf|csrf"), ("CRYPTO", r"hunt-jwt|crypto|tls"), ("CONF", r"cors|clickjack|misconfig|subdomain|host-header"),
    ("INJ", r"xxe|smuggl|ldap|xpath|prototype|graphql"), ("DOS", r"dos|rate-limit"), ("LOGIC", r"race|business-logic"),
]

def classify(name, path):
    p = (path or "").lower()
    if p.startswith("skills/"):
        for cls, rx in PATH_CLASS:
            if re.search(rx, p): return cls
    for cls, rx in CLASSES:
        if re.search(rx, name, re.I): return cls
    return "GENERIC"

STRONG = re.compile(r"bypass|payload|table|technique|→|poison|wrapper|magic byte|polyglot|union select|"
                    r"order by|time.based|blind|chain|enumeration|attack|exploit|dump|extraction", re.I)
JUNK = re.compile(r"^(e\.g\.|needs:|usage:|python3 |curl |analyzeHeadless)|http://|https://|\{[a-z]+:", re.I)

def clean(h):
    h = re.sub(r"^#+\s*", "", h or "").strip()
    h = re.sub(r"^(\d+[\.\)]\s*|phase\s*\d+\s*[—:-]\s*|step\s*\d+\s*[—:-]\s*)", "", h, flags=re.I)
    return h[:120]

def main():
    con = sqlite3.connect(DB, timeout=120)
    con.executescript("""
    DROP TABLE IF EXISTS techniques;
    CREATE TABLE IF NOT EXISTS techniques(
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL,
      cls TEXT NOT NULL,
      chunk_id INTEGER,
      path TEXT,
      source TEXT,
      keywords TEXT,
      confidence TEXT,
      built_at TEXT,
      UNIQUE(name, path)
    );
    CREATE INDEX IF NOT EXISTS techniques_cls ON techniques(cls);
    """)
    con.execute("DELETE FROM techniques")
    rows = con.execute("""SELECT id, heading, path, kind FROM chunks
                          WHERE kind='doc' AND heading IS NOT NULL AND length(heading) BETWEEN 6 AND 120""").fetchall()
    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    kept = 0
    for cid, heading, path, kind in rows:
        name = clean(heading)
        if not name or NOISE.match(name): continue
        if not TECH_RX.search(name): continue
        if JUNK.search(name) or name[0].islower(): continue
        if len(name.split()) > 14: continue
        cls = classify(name, path)
        from_path = bool(path) and path.startswith("skills/") and any(
            re.search(rx, path.lower()) for _, rx in PATH_CLASS)
        # keyword-only matches must look like an actual technique, not an incidental use of the word
        if not from_path and not STRONG.search(name): continue
        src = "skill" if (path or "").startswith("skills/") else ("playbook" if path else "report")
        con.execute("""INSERT OR IGNORE INTO techniques(name, cls, chunk_id, path, source, keywords, confidence, built_at)
                       VALUES (?,?,?,?,?,?,?,?)""",
                    (name, cls, cid, path, src,
                     ",".join(sorted({w.lower() for w in re.findall(r"[a-z]{4,}", name)})),
                     "path" if from_path else "kw", now))
        kept += 1
    con.commit()
    total = con.execute("SELECT COUNT(*) FROM techniques").fetchone()[0]
    print(f"techniques indexed: {total} from {len(rows)} headings")
    for cls, n in con.execute("SELECT cls, COUNT(*) FROM techniques GROUP BY 1 ORDER BY 2 DESC"):
        print(f"  {n:4d}  {cls}")

main()
