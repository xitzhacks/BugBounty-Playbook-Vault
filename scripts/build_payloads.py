#!/usr/bin/env python3
"""Build the payload table: every fenced code block from reports and doctrine, classified and deduped.

Why: DVWA showed technique names live in headings but payloads live in fenced blocks. The heading-only
router misses upload/phar/DOS techniques; this table indexes the actual strings an operator copies.

Table payloads(id, sha256, payload, lang, cls, kind, report_id, path, chunk_id, context, chars, built_at)
"""
import hashlib, os, re, sqlite3, time

DB = os.environ.get("VAULT_DB", os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "vault", "_VAULT", "reports.sqlite"))
CODE_RX = re.compile(r"```([a-zA-Z0-9_+.-]*)[ \t]*\n(.*?)```", re.S)
MIN_LEN, MAX_LEN = 4, 3000

CLASS_RX = [
    ("SQLI", r"sql injection|\bsqli\b|union select|\bselect .* from\b|information_schema"),
    ("XSS", r"cross-site scripting|\bxss\b|<script|onerror=|onload="),
    ("SSRF", r"\bssrf\b|169\.254\.169\.254|metadata"),
    ("LFI", r"traversal|php://|/etc/passwd|file inclusion|\blfi\b"),
    ("RCE", r"command injection|rce|shell_exec|system\(|deserial|webshell"),
    ("UPLOAD", r"upload|magic byte|polyglot|\.phtml|Content-Type"),
    ("IDOR", r"\bidor\b|object reference"),
    ("INJ", r"\bxxe\b|smuggling|crlf|entity|header inject"),
    ("AUTH", r"\bjwt\b|oauth|saml|\b2fa\b|password|session|token"),
    ("CRYPTO", r"openssl|cipher|tls|starttls|certificate"),
    ("CONF", r"\bcors\b|clickjack|hsts|x-frame"),
    ("DOS", r"denial of service|sleep\(|redos|exhaust"),
    ("LOGIC", r"race|coupon|price|quantity"),
]
CLASS_RX = [(c, re.compile(rx, re.I)) for c, rx in CLASS_RX]

PATH_CLASS = [("LFI", r"hunt-lfi|path-traversal"), ("SQLI", r"hunt-sqli|sql"), ("XSS", r"hunt-xss|xss"),
              ("SSRF", r"hunt-ssrf|ssrf"), ("IDOR", r"hunt-idor|idor"), ("UPLOAD", r"upload"),
              ("RCE", r"hunt-rce|rce|deserial"), ("AUTH", r"hunt-jwt|auth|oauth|saml|mfa|session"),
              ("INJ", r"xxe|smuggl|ldap|xpath|prototype"), ("CONF", r"cors|clickjack|misconfig|host-header"),
              ("DOS", r"rate-limit|dos"), ("LOGIC", r"race|business-logic"), ("CRYPTO", r"crypto|jwt")]

def classify(text, path, weakness):
    blob = (text or "")[:1200]
    if weakness:
        for c, rx in CLASS_RX:
            if rx.search(weakness): return c
    p = (path or "").lower()
    if p.startswith("skills/"):
        for c, rx in PATH_CLASS:
            if re.search(rx, p): return c
    for c, rx in CLASS_RX:
        if rx.search(blob): return c
    return "GENERIC"

def norm(t):
    return re.sub(r"\s+", " ", t.strip().lower())

def main():
    con = sqlite3.connect(DB, timeout=180)
    con.executescript("""
    DROP TABLE IF EXISTS payloads;
    CREATE TABLE payloads(
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      sha256 TEXT UNIQUE,
      payload TEXT NOT NULL,
      lang TEXT, cls TEXT NOT NULL, kind TEXT NOT NULL,
      report_id INTEGER, path TEXT, chunk_id INTEGER,
      context TEXT, chars INTEGER, score INTEGER, built_at TEXT
    );
    CREATE INDEX payloads_cls ON payloads(cls);
    CREATE INDEX payloads_kind ON payloads(kind);
    """)
    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    seen, rows = {}, []

    def add(payload, lang, cls, kind, rid, path, cid, context):
        p = payload.strip("\n").strip()
        if not (MIN_LEN <= len(p) <= MAX_LEN): return
        if p.count("\n") == 0 and len(p) < 12: return
        h = hashlib.sha256(norm(p).encode()).hexdigest()
        if h in seen: return
        seen[h] = 1
        ATTACK = re.compile(r"<script|onerror\s*=|onload\s*=|javascript:|<svg|<img|<iframe|\{\{|\$\{|"
                            r"union\s+select|or\s+1=1|sleep\(|\.\./\.\./|169\.254\.169\.254|"
                            r"<!ENTITY|\$\{jndi|php://|expect://|data:text/html|;\s*id\b|\|\s*id\b|"
                            r"curl\s+-|\bwget\s|/bin/sh|cmd=|exec\(|system\(", re.I)
        OUTPUT = re.compile(r"^HTTP/1\.[01]\s|^Date:|^Server:|Content-Length:|Content-Type:|"
                            r"^\s*\[?\d{4}-\d{2}-\d{2}|^\s*(uid=|root:x:|total\s+\d)", re.M)
        sc = 0
        attack = bool(ATTACK.search(p))
        if attack and len(p) < 400: sc += 5
        elif attack: sc += 2
        if 10 <= len(p) <= 300: sc += 2
        if len(p) > 800: sc -= 4
        if re.search(r"[<>\"'(){};|&$`]", p): sc += 1
        if OUTPUT.search(p[:300]): sc -= 5
        if re.match(r"^\s*(#!|import |from \w+ import|def |class |package |public class)", p) and not attack: sc -= 3
        if re.match(r"^(GET|POST|PUT|DELETE|PATCH) /\S+ HTTP/", p): sc += 2
        rows.append((h, p, lang or "", cls, kind, rid, path, cid, (context or "")[:220], len(p), sc, now))

    # reports
    for rid, title, weakness, body in con.execute(
            "SELECT b.id, r.title, r.weakness, b.body FROM bodies b JOIN reports r ON r.id=b.id "
            "WHERE length(COALESCE(b.body,''))>100"):
        for lang, code in CODE_RX.findall(body):
            add(code, lang, classify(title + " " + code, None, weakness), "report", rid, None, None, title)

    # doctrine chunks
    for cid, path, heading, text in con.execute(
            "SELECT id, path, heading, text FROM chunks WHERE kind='doc'"):
        for lang, code in CODE_RX.findall(text):
            kind = "skill" if (path or "").startswith("skills/") else "playbook"
            add(code, lang, classify(heading + " " + code, path, None), kind, None, path, cid, heading)

    con.executemany("""INSERT OR IGNORE INTO payloads(sha256,payload,lang,cls,kind,report_id,path,chunk_id,context,chars,score,built_at)
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""", rows)
    con.commit()
    total = con.execute("SELECT COUNT(*) FROM payloads").fetchone()[0]
    print(f"payloads indexed: {total} unique (from {len(rows)} candidates)")
    print(f"{'class':9} {'rows':>6}  {'reports':>8} {'doctrine':>9}")
    for c, n, rep in con.execute("""SELECT cls, COUNT(*), SUM(kind='report') FROM payloads
                                    GROUP BY 1 ORDER BY 2 DESC"""):
        print(f"{c:9} {n:6d}  {rep or 0:8d} {n-(rep or 0):9d}")

main()
