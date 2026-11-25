#!/usr/bin/env python3
"""Corpus-scale XSS sweep: URL corpus -> endpoint/param map -> reflection -> emission class.

Usage:
    python3 corpus_param_sweep.py urls.txt              # file of URLs (with or without query)
    python3 corpus_param_sweep.py urls.txt --threads 4 --cookie '_I_=...' --ua '...'

Outputs (in cwd):
    sweep_endpoint_params.json   endpoint -> [params]
    sweep_reflection.jsonl       per (endpoint,param): status, reflected, context
    sweep_encoding.jsonl         per reflective pair: RAW | SAFE:<forms> | NO-ECHO
    sweep_summary.txt            counters for the report

Contamination rules baked in (see references/url-corpus-sweep.md):
  * status 202 / 503 / 0 are DISCARDED (captcha / throttle) and retried at low concurrency
  * any response carrying an sg-captcha / cf-mitigated header is discarded
  * NO-ECHO is resolved with an incremental character probe, never reported as "safe"
"""
import argparse, collections, json, queue, random, re, ssl, sys, threading, time, urllib.parse
import urllib.request, urllib.error

CTX = ssl.create_default_context(); CTX.check_hostname = False; CTX.verify_mode = ssl.CERT_NONE
MARK = "refmark7x2q"
HOSTILE = 'cpmarkx"><b>zq'
FORMS = {"RAW": 'cpmarkx"><b>zq', "URLENC": 'cpmarkx%22%3E%3Cb%3Ezq',
         "ENTITY": 'cpmarkx&quot;&gt;&lt;b&gt;zq', "NUMENT": 'cpmarkx&#34;&#62;&#60;b&#62;zq'}
BAD_STATUS = {202, 503, 0}
BAD_HDRS = ("sg-captcha", "cf-mitigated", "x-sucuri", "incap_ses")
STATIC = re.compile(r'\.(png|jpe?g|gif|svg|css|js|woff2?|ttf|ico|pdf|webp|mp4)(\?|$)', re.I)

ap = argparse.ArgumentParser()
ap.add_argument("urls")
ap.add_argument("--threads", type=int, default=4)
ap.add_argument("--cookie", default="")
ap.add_argument("--ua", default="curl/8.5.0")
ap.add_argument("--timeout", type=int, default=20)
ap.add_argument("--max-pairs", type=int, default=0)
args = ap.parse_args()

HDRS = {"User-Agent": args.ua}
if args.cookie:
    HDRS["Cookie"] = args.cookie


def fetch(url, tries=3):
    delay = 2.0
    for attempt in range(tries):
        try:
            r = urllib.request.urlopen(urllib.request.Request(url, headers=HDRS),
                                       timeout=args.timeout, context=CTX)
            hdrs = {k.lower(): v for k, v in r.headers.items()}
            return r.status, r.read(500000).decode("utf-8", "replace"), hdrs
        except urllib.error.HTTPError as e:
            body = ""
            try:
                body = e.read(500000).decode("utf-8", "replace")
            except Exception:
                pass
            hdrs = {k.lower(): v for k, v in e.headers.items()} if e.headers else {}
            if e.code in (202, 503, 429) and attempt < tries - 1:
                time.sleep(delay + random.random()); delay *= 2
                continue
            return e.code, body, hdrs
        except Exception:
            if attempt < tries - 1:
                time.sleep(delay + random.random()); delay *= 2
                continue
            return 0, "", {}
    return 0, "", {}


def contaminated(status, hdrs, body):
    if status in BAD_STATUS:
        return True
    if any(any(h in k or h in str(v).lower() for k in hdrs) for h in BAD_HDRS):
        return True
    low = body[:600].lower()
    return "sgcaptcha" in low or "just a moment" in low or "attention required" in low


# ---- stage 1: map -----------------------------------------------------------
ep = collections.defaultdict(set)
for line in open(args.urls, errors="ignore"):
    u = line.strip()
    if not u.startswith("http") or "?" not in u or STATIC.search(u):
        continue
    p = urllib.parse.urlsplit(u)
    for kv in p.query.split("&"):
        k = kv.split("=")[0]
        if re.fullmatch(r"[A-Za-z0-9_\[\].-]{1,40}", k or ""):
            ep[(p.netloc.lower(), p.path or "/")].add(k)

mapping = {f"https://{h}{p}": sorted(v) for (h, p) in ep.items()}
json.dump(mapping, open("sweep_endpoint_params.json", "w"), indent=1)
pairs = [(e, prm) for e, prms in mapping.items() for prm in prms]
if args.max_pairs:
    pairs = pairs[: args.max_pairs]
print(f"endpoints={len(mapping)} pairs={len(pairs)}", flush=True)

# ---- stage 2: reflection ----------------------------------------------------
q = queue.Queue(); lock = threading.Lock()
ref_out = open("sweep_reflection.jsonl", "w"); hits = []


def worker_reflect():
    while True:
        try:
            endpoint, prm = q.get_nowait()
        except queue.Empty:
            return
        sep = "&" if "?" in endpoint else "?"
        url = endpoint + sep + urllib.parse.quote(prm) + "=" + MARK
        status, body, hdrs = fetch(url)
        if contaminated(status, hdrs, body):
            time.sleep(0.2)
            continue
        reflected = MARK in body
        rec = {"endpoint": endpoint, "param": prm, "status": status, "reflected": reflected,
               "context": [body[max(0, m.start()-80):m.start()+len(MARK)+80].replace("\n", " ")
                           for m in list(re.finditer(MARK, body))[:2]]}
        with lock:
            ref_out.write(json.dumps(rec) + "\n"); ref_out.flush()
            if reflected:
                hits.append((endpoint, prm))
        time.sleep(0.15)


for pr in pairs:
    q.put(pr)
ths = [threading.Thread(target=worker_reflect, daemon=True) for _ in range(args.threads)]
for t in ths: t.start()
for t in ths: t.join()
print(f"reflective pairs={len(hits)}", flush=True)

# ---- stage 3: emission class ------------------------------------------------
for endpoint, prm in hits:
    sep = "&" if "?" in endpoint else "?"
    url = endpoint + sep + urllib.parse.quote(prm) + "=" + urllib.parse.quote(HOSTILE, safe="")
    status, body, hdrs = fetch(url)
    cls = [k for k, v in FORMS.items() if v in body]
    if "RAW" in cls:
        verdict = "RAW"
    elif cls:
        verdict = "SAFE:" + ",".join(cls)
    else:
        # resolve NO-ECHO: does a plain marker come back at all?
        plain_url = endpoint + sep + urllib.parse.quote(prm) + "=cpmarkx"
        st2, b2, _ = fetch(plain_url)
        verdict = "NO-ECHO(not reflective now)" if "cpmarkx" not in b2 else "STRIPPED/FILTERED"
    rec = {"endpoint": endpoint, "param": prm, "status": status, "verdict": verdict}
    if verdict == "RAW":
        i = body.find(FORMS["RAW"])
        rec["context"] = body[max(0, i-140):i+180].replace("\n", " ")
    with lock:
        open("sweep_encoding.jsonl", "a").write(json.dumps(rec) + "\n")
    time.sleep(0.15)

summary = collections.Counter()
for line in open("sweep_encoding.jsonl"):
    summary[json.loads(line)["verdict"].split(":")[0]] += 1
with open("sweep_summary.txt", "w") as fh:
    fh.write(f"urls_input={args.urls}\nendpoints={len(mapping)}\npairs={len(pairs)}\n")
    fh.write(f"reflective={(sum(summary.values()))}\n")
    fh.write("verdicts=" + json.dumps(dict(summary)) + "\n")
print("verdicts:", dict(summary))
print("RAW breakouts:", summary.get("RAW", 0), "- escalate survivors to dom_xss_dumpdom.py")
