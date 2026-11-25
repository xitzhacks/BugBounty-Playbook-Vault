#!/usr/bin/env python3
"""Build the bypass index: protection → passage → payload.

Scans disclosed write-ups (bodies) and doctrine (skill/vault chunks) for the protections researchers
actually got past, keeps the passage around the mention, and lifts any fenced code block in that
window as the payload they used.

Table bypasses(tag, kind, report_id, path, chunk_id, title, program, passage, payloads, confidence)
CLI:
  python3 bypass.py                     # tag census
  python3 bypass.py waf --grep cloudflare
  python3 bypass.py csp --show 12
"""
import os, re, sqlite3, time, sys

DB = os.environ.get("VAULT_DB", os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "vault", "_VAULT", "reports.sqlite"))
WINDOW = 700           # chars either side of the match
MAX_PAYLOAD = 1500     # cap per row

TAGS = [
    ("waf",        r"\bWAF\b|cloudflare|akamai|incapsula|imperva|modsecurity|sucuri|f5 asm|awswaf"),
    ("csp",        r"content-security-policy|\bCSP\b|script-src|frame-ancestors"),
    ("twofa",      r"\b2fa\b|two.factor|\bMFA\b|\bOTP\b|verification code|authenticator"),
    ("rate_limit", r"rate.?limit|throttl|brute.?force protection|account lockout|too many requests"),
    ("allowlist",  r"allow.?list|whitelist|block.?list|black.?list|deny.?list|ip restriction"),
    ("sanitizer",  r"sanitiz|htmlspecialchars|strip_tags|escape|input filter|filtering"),
    ("earlier_fix",r"bypass (?:for|of) (?:the )?(?:fix|patch)|incomplete (?:fix|patch)|regression|still vulnerable after"),
    ("cors",       r"\bCORS\b|access-control-allow-origin"),
    ("authz",      r"auth(?:entication|orization) bypass|missing authoriz|no authoriz|access control bypass"),
]
TAG_RX = [(t, re.compile(rx, re.I)) for t, rx in TAGS]
CODE_RX = re.compile(r"```[a-zA-Z0-9_+-]*\n(.*?)```", re.S)
BYPASS_RX = re.compile(r"bypass|got past|evad|circumvent|work(?:ed)? around|still (?:vulnerable|work|execut)|"
                       r"blocked|filter(?:ed|ing)? out|escape|encode|payload|trick|smuggl", re.I)

def score(win, payloads, tag, title):
    sc = 0
    if BYPASS_RX.search(win): sc += 3
    if payloads: sc += 2
    if title and re.search(tag.replace("_", r"[ _]?"), title, re.I): sc += 1
    return sc

def windows(text, m):
    s = max(0, m.start() - WINDOW); e = min(len(text), m.end() + WINDOW)
    return text[s:e]

def code_in(chunk):
    blocks = CODE_RX.findall(chunk)
    out = []
    for b in blocks:
        b = b.strip()
        if len(b) < 6: continue
        out.append(b)
        if sum(len(x) for x in out) > MAX_PAYLOAD: break
    return "\n---\n".join(out)[:MAX_PAYLOAD]

def main():
    con = sqlite3.connect(DB, timeout=180)
    con.executescript("""
    DROP TABLE IF EXISTS bypasses;
    CREATE TABLE bypasses(
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      tag TEXT NOT NULL,
      kind TEXT NOT NULL,            -- report | skill | playbook
      report_id INTEGER, path TEXT, chunk_id INTEGER,
      title TEXT, program TEXT,
      passage TEXT, payloads TEXT, confidence TEXT, score INTEGER, built_at TEXT
    );
    CREATE INDEX bypasses_tag ON bypasses(tag);
    """)
    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    rows = []

    # --- reports: one row per (report, tag), passage = best window, payloads = code in that window
    for rid, title, program, body in con.execute(
            "SELECT b.id, r.title, r.program, b.body FROM bodies b JOIN reports r ON r.id=b.id "
            "WHERE length(COALESCE(b.body,''))>200"):
        for tag, rx in TAG_RX:
            m = None
            for mm in rx.finditer(body):
                m = mm
                break
            if not m: continue
            win = windows(body, m)
            # prefer a window that also contains a code block
            for mm in rx.finditer(body):
                w2 = windows(body, mm)
                if "```" in w2:
                    win = w2; m = mm; break
            pay = code_in(win)
            rows.append((tag, "report", rid, None, None, title, program, win[:1800], pay,
                         "code" if pay else "text", score(win, pay, tag, title), now))

    # --- doctrine chunks (skills + our playbooks)
    for cid, path, heading, text in con.execute(
            "SELECT id, path, heading, text FROM chunks WHERE kind='doc'"):
        for tag, rx in TAG_RX:
            m = rx.search(text)
            if not m: continue
            win = windows(text, m)
            pay = code_in(win)
            rows.append((tag, "skill" if (path or "").startswith("skills/") else "playbook",
                         None, path, cid, heading, None, win[:1800], pay,
                         "code" if pay else "text", score(win, pay, tag, heading), now))

    con.executemany("""INSERT INTO bypasses(tag,kind,report_id,path,chunk_id,title,program,passage,payloads,confidence,score,built_at)
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""", rows)
    con.commit()
    total = con.execute("SELECT COUNT(*) FROM bypasses").fetchone()[0]
    print(f"bypasses indexed: {total} rows")
    print(f"{'tag':12} {'rows':>6} {'relevance>=3':>13} {'reports':>8} {'doctrine':>9}")
    for tag, n, code, rep, doc in con.execute("""
            SELECT tag, COUNT(*), SUM(confidence='code'), SUM(kind='report'), SUM(kind!='report')
            FROM bypasses GROUP BY 1 ORDER BY 2 DESC"""):
        print(f"{tag:12} {n:6d} {code or 0:13d} {rep or 0:8d} {doc or 0:9d}")

main()
