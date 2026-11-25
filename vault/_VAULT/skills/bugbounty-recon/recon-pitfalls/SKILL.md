---
name: recon-pitfalls
description: >-
  Operational pitfalls and workflow corrections for external recon (subdomain
  enumeration, liveness probing, URL/endpoint collection). Use alongside
  recon-and-methodology when actually RUNNING the tooling — covers the
  tooling gotchas that waste a session if you don't know them up front
  (httpx ANSI codes, amass slowness, gau cross-root leakage, scope filtering).

---

# SKILL: Recon Pitfalls (operational, tooling-level)

> Companion to recon-and-methodology. That skill lists the COMMANDS; this
> skill lists the GOTCHAS that bite when you run them for real. Learned
> the hard way during a 4-root AbemaTV enumeration.

## 1. httpx emits ANSI color codes — STRIP before parsing
httpx prints status/tech inside escape codes, e.g. `[32m200[0m` and
`[31m404[0m]. Any `grep -E '\[200\]'` / `awk -F'[][]'` filter
SILENTLY FAILS because the brackets are wrapped in `\x1b[..m`.

FIX (always do this first after httpx):
```bash
sed -E 's/\x1b\[[0-9;]*m//g' live_raw.txt > live_clean.txt
# now filters work:
grep -E '\[200\]' live_clean.txt
awk -F'[][]' '{print $3}' live_clean.txt | sort | uniq -c
```

**Same trap, `dnsx -resp`** (hit on a 459-host takeover sweep). `dnsx -cname -resp` prints
`host [\x1b[35mCNAME\x1b[0m] [\x1b[32mtarget\x1b[0m]`, so
`grep -oE '\[CNAME\] \[[^]]+\]'` returns ZERO matches and your whole CNAME/dangling-target
pipeline silently produces an empty list — which reads as "no CNAMEs anywhere", i.e. a false
negative on the exact class you are testing. FIX:
```bash
dnsx -l hosts.txt -cname -resp -no-color -silent > cnames.txt   # prefer -no-color
# and regardless, strip before parsing:
sed -E 's/\x1b\[[0-9;]*m//g' cnames.txt > cnames_clean.txt
```
Sanity-check the count: if you parsed 0 CNAMEs out of a few hundred hosts, it is the ANSI trap,
not a clean estate.

## 2. amass -passive over MULTIPLE roots is painfully slow
`amass enum -passive -d a -d b -d c -d d` ran 9+ minutes with ZERO
bytes written to its `-o` file (amass buffers, writes at end). It looks
hung. Meanwhile subfinder + assetfinder finished in seconds with full coverage.

FIX:
- Run `subfinder -d r1 -d r2 -d r3 -d r4` and `assetfinder --subs-only`
  per root IN PARALLEL — they finish in seconds.
- Only add amass if you specifically need its graph/relationship data, and
  run it BACKGROUNDED with `notify_on_complete=true`; don't block on it.
- If you must have amass results, merge AFTER the fast tools, not before.

## 3. gau / waybackurls return CROSS-ROOT URLs
gau and waybackurls pull every URL the host has EVER served across ALL
roots/domains it has indexed — not just your in-scope roots. If you
collect `gau target.com` you will get `target.net`, `target-cdn.io`, etc.
mixed in. Wasting effort on out-of-scope hosts is the silent failure mode.

FIX — strict in-scope filter immediately after collection:
```bash
# keep only your declared roots
grep -iE 'https?://[^/]*\.(scope1|scope2|scope3|scope4)\b' gau_all.txt | sort -u > in_scope.txt
```
Same for subdomain merge:
```bash
cat subfinder.txt assetfinder.txt amass.txt \
  | grep -oE '[a-z0-9.-]+\.(scope1|scope2|scope3)' \
  | sed 's/\r//' | sort -u > all_subdomains.txt
```

## 4. crt.sh via curl can be BLOCKED by the runtime
A `curl ... crt.sh/?q=...` call got hard-blocked by command permissions
in-session (user-denied / runtime guard). Don't rely on it as a required
step. subfinder already pulls cert-transparency sources; if crt.sh is
blocked, you lose little. Note it and move on.

**It also just goes down.** Repeated `HTTP 502` with a 150-byte HTML body for a whole session —
both `?q=%25.domain&output=json` and the bare page, every retry. Two substitutes that answered
immediately while crt.sh was 502, and between them surfaced names subfinder missed:
```bash
# certspotter (no key needed, 100 issuances free) — dns_names incl. k8s ingress hostnames
curl -sk "https://api.certspotter.com/v1/issuances?domain=target.com&include_subdomains=true&expand=dns_names"
# hackertarget hostsearch — host,IP pairs
curl -sk "https://api.hackertarget.com/hostsearch/?q=target.com"
```
Between them they produced `compliance.ts01-prod-main.k8s.`, `nginx-front.ts01-prod-main.k8s.`
and `inbound-request-gateway.ts01-prod-main.k8s.` — none of which subfinder/assetfinder returned.
Wayback CDX (`web.archive.org/cdx/search/cdx?url=host*`) is worth one call too, and an empty
result for a host is itself useful: it means no archived JS bundles exist, so you cannot recover
a gated SPA's chunk list from the archive (see §13).

**Wildcard-check BEFORE any DNS brute.** `dig +short zzqxwv987.target.com` → NXDOMAIN means brute
results are real; a wildcard A record means every word "resolves" and the run is worthless. Do it
first, every time, or you will either chase phantom hosts or discard a real one as noise.

## 5. Inline python3 -c blocks concurrent.futures in sandbox
`python3 -c "from concurrent.futures import ThreadPoolExecutor; ..."` gets silently
killed/truncated by the execution sandbox (no error, just zero output). This affects
any concurrent JS secret scanning or parallel URL processing done inline.

FIX: Write the script to a file first, then execute it as a file:
```bash
cat << 'EOF' > secrets/scan_js.py
import concurrent.futures
...
EOF
python3 secrets/scan_js.py
```
File-based execution always works; inline `-c` with concurrent imports is silently blocked.

## 6. katana flag syntax errors — -kf requires a value
katana's `-kf` (known filenames) flag REQUIRES an argument. `-kf` alone is an
"invalid flag error"; it must be `-kf all` (or a specific filelist).

FIX: Always verify flags with `katana -h` if the first run errors. When a
flag requires an argument, pass it explicitly: `-kf all` not bare `-kf`.

## 7. Merge + dedupe discipline
- Always `sort -u` after cat-ing multi-source subdomain lists.
- Cross-check: a subdomain is "live" only if it appears in BOTH your
  subdomain list AND the httpx live output. Verify with `comm`:
```bash
comm -12 <(sed -E 's#https?://##; s#/.*##' live_hosts.txt | sort -u) \
         <(sort -u all_subdomains.txt)
```

## 8. Recon output file manifest (recommended layout)
Per target dir:
- `target.txt` — scope roots (one per line, support `*.wildcard`)
- `subdomains_all.txt` — merged unique subdomains (all sources)
- `live_subdomains.txt` — httpx-confirmed live hosts (ANSI-stripped)
- `gau_inscope.txt` — discovered URLs filtered to scope
- `api_paths.txt` — deduped path templates (`/v1/users/{id}`)

## 9. A Cloudflare 403 does NOT mean the host is dead — send a browser header set
Default `curl` against a CF-fronted host returns `HTTP/2 403`, `cf-mitigated: challenge`,
`content-length: ~5.6k`, `<title>Just a moment...</title>`. That is a **managed challenge to
your client fingerprint**, not a dead app and not necessarily a WAF block on the target. The same
URL returns the real 200 page (34 KB of SSR HTML) once you send a coherent browser header set:
Firefox UA + `Accept` + `Accept-Language` + `Sec-Fetch-{Dest,Mode,Site,User}` +
`Upgrade-Insecure-Requests` + `--compressed`.

Ready-to-use wrapper: `scripts/cf_curl.sh <url> [-D -] ...` — drop it in the target dir as
`rq.sh` and route every probe through it. **Without this you will wrongly report "cloudflare
blocked everything" and skip the entire main app.**
Note what the *absence* of the CF challenge tells you too: sibling hosts that answer plain curl
(e.g. the ICM backend) are NOT behind CF — that is where your API testing belongs.

## 10. Archived URL corpora describe a HISTORICAL stack — re-fingerprint before hunting them
`gau`/`wayback`/`all_urls.txt` give you a 2-4 year old picture. On one target the corpus was
full of IBM WebSphere Portal (`/wps/wcm/connect/<uuid>/...?MOD=AJPERES`) and Lotus Domino
(`/RZ/NL/RZ_Main.nsf/...?OpenForm&Start=1&Count=30`) paths — every one of them now 301s into a
completely different Intershop/Angular SPA. Time spent enumerating `?Start=`, `?BaseTarget=`,
`?FieldElemFormat=` variants was pure waste.

Rule: after loading the corpus, fetch the live root + one archived path and compare the stack
(headers, `<title>`, `ng-app-id`, `<base href>`). If the stack changed, the archive is only a
source of *parameter names to try on the NEW app*, not a list of live endpoints.

## 11. WAF budget — a 200-request burst can flip you from challenge to hard block
A param-matrix run (~180 navigations) against a CF-fronted SPA moved the site from
`cf-mitigated: challenge` to `Sorry, you have been blocked` for that source IP,
mid-run — which invalidates the remaining tests (they return the block page, not the app).
Budget your browser-matrix runs (test the highest-value params first), watch for the transition,
and when it happens STOP and record it rather than hammering through the block. Treat IP
reputation as an engagement asset: a burned source IP ends active testing for hours.

**The block can be fingerprint-scoped, not IP-wide — check before you declare the target dead.**
After the same burst, plain `curl` (browser header set, §9) kept returning **200** on the same
URL while the isolated Firefox got `Attention Required! | Cloudflare` on its *first* navigation,
including on a brand-new throwaway profile. So "the browser is blocked" and "the IP is blocked"
are different states with different recoveries:
```bash
curl -sk -o /dev/null -w '%{http_code}\n' -A 'curl/8.5.0' https://target/page   # HTTP still alive?
```
- HTTP alive + browser blocked → switch that phase to HTTP-level testing (reflection/marker
  detection, header checks, static sink review of the bundles) instead of ending the engagement.
  Re-attempt the browser phase later or from different egress.
- Both blocked → stop active testing on the host entirely; continue on sibling hosts (on this
  target the ICM backend and the vendor SaaS hosts were unaffected while www was burning).
Do not spend a fresh profile per retry — a fresh profile is not a fresh identity when the
TLS/JS fingerprint and the source IP are unchanged.

**Prefer the analytic negative over the 20-minute matrix.** For "does any parameter reach a
sink", a static trace of the live bundles is faster AND immune to WAF budget: enumerate the
markup sinks, then grep for a source→sink edge (`(location.search|location.hash|queryParams)`
near `innerHTML|insertAdjacentHTML|bypassSecurityTrust*`). Zero edges plus a documented sink list
is a stronger, reproducible negative than a payload run that may have been silently no-op'd
(see browser-isolation: `execute_script` returns None without `return`).

## 12. The 403 fingerprint trap runs BOTH ways — a bare Chrome UA can be the thing that gets blocked

§9 says "plain curl 403s, send browser headers". The inverse happens just as often and is far
easier to misread as "the site hardened everything".

On trendspider.com a sweep of 69 page/param combinations returned 403 for **every single URL**
when the scanner sent `Mozilla/5.0 (X11; Linux x86_64) ... Chrome/126.0.0.0 Safari/537.36` and
nothing else. The same URLs answered 200 immediately:

```bash
curl -sk -A "curl/8.5.0" "https://trendspider.com/?s=cpmark987abczq"   # 200, 509389 bytes
curl -sk           "https://trendspider.com/?s=cpmark987abczq"          # 200, 509386 bytes
curl -sk -A "Mozilla/5.0 ... Chrome/126.0.0.0 Safari/537.36" ...        # 403,  75193 bytes
```

A bare vendor UA with no `Accept`/`Accept-Language`/`Sec-Fetch-*` is a *worse* fingerprint than
curl's own — bot management sees "claims to be Chrome, ships none of Chrome's headers" and
blocks it. Tell: a 403 body that is a fixed page-sized blob (75 KB here) rather than the target's
real 404/error page, and 100% uniform 403s across unrelated paths.

Rules:
- A sweep where **every page 403s** is a fingerprint result, not a coverage result. Re-probe one
  URL with `-A "curl/8.5.0"` (or no UA) before recording a single negative.
- Choose the UA deliberately per phase: bare `curl/8.5.0` for broad sweeps (passes most bot
  filters), full browser header set (per §9) only when the host actually demands it.
- Never mix: Chrome UA without Chrome's headers, or curl UA against a host that wants a browser
  set — both read as "blocked" and both are wrong.
- The same trap follows you into tooling: `httpx -H 'User-Agent: ...'` and headless Chrome inherit
  whatever you configured, so your HTTP sweep and your browser verification can disagree for
  fingerprint reasons and look like a broken finding.
- Related shape worth knowing: the hardening can also be *per-host*, not per-UA. On the same
  target `trendspider.com/markets/wp-json/` returned `403 rest_forbidden` while
  `markets.trendspider.com/wp-json/` (the legacy host that 301s to the apex) served the full
  308-route index and public REST endpoints. Differential-test the old hostname before believing
  a "fully locked down" API.

## 13. RFC1918-only k8s ingress names — test Host-header routing through the public ALBs before writing them off

Kubernetes-hosted estates leak their internal ingress hostnames into cert transparency:
`compliance.ts01-prod-main.k8s.target.com`, `nginx-front.*`, `inbound-request-gateway.*`,
`wordpress.*`. They resolve ONLY to private addresses (`10.200.26.7`, `10.200.88.241`,
`10.200.147.246`), so prior sessions record them as "internal, unreachable" — usually **without
ever testing it**. That conclusion is unproven: ingress controllers route by Host header, so the
same hostnames are reachable through any public ALB that fronts the same cluster.

Test it — collect every public A record from the sibling hosts, then send each internal name as
Host to each public IP:

```bash
for ip in 15.197.163.95 3.33.128.125 35.208.227.99; do
  for h in compliance.ts01-prod-main.k8s.target.com nginx-front.ts01-prod-main.k8s.target.com; do
    curl -sk --max-time 10 -H "Host: $h" "https://$ip/" \
      -o /dev/null -w "$ip $h %{http_code} %{size_download}\n"
  done
done
```

**Baseline first.** Send a bogus Host (`Host: nope.invalid`) to each IP and record the default
vhost response — on the tested estate that was a 162-byte `301` on two ALBs and a generic
1385-byte page on a third. A hit is a response that differs from that baseline (different body
size, different title, different status). Identical defaults across every internal name = no
routing, genuinely unreachable.

Record the result in the notes with the baseline sizes. It converts "we assumed internal" into
"tested, no route" and stops the next session re-deriving it — and it is the single fastest way
to turn a dead k8s hostname into a live finding if the cluster does leak.

## 14. Bulk sweeps: captcha/throttle pages ECHO your URL and fake a "reflection"

Any marker-based sweep (reflection hunting, param fuzzing, cache probing) that runs at high
concurrency will hit an anti-bot layer, and the block page usually repeats the request URL back
at you — which a naive `marker in body` detector scores as a hit.

SiteGround's captcha on a large marketing site did exactly this: at 12 threads 857/1,597
requests returned `503`, and on retry `202` with a 179-byte body:

```html
<meta http-equiv="refresh" content="0;/.well-known/sgcaptcha/?r=%2Fpricing%2F&y=ipc:…">
```

The marker was inside that `r=` parameter on every single one. Rules:

- Drop `202`, `503`, `0`, and any response carrying an anti-bot header
  (`sg-captcha: challenge`, `cf-mitigated: challenge`) **before** counting reflections.
- Retry the dropped set at 3–5 threads with exponential backoff.
- Report the surviving count, not the raw hit count — otherwise your "325 reflections" is really
  "325 captcha pages".

**Clearance cookies are usually User-Agent bound.** Solving the SiteGround PoW yields a 30-day
`_I_` cookie, but replaying it from a different UA silently returns `202` again — it reads as
"the bypass stopped working" when the client is simply mismatched. Carry the UA used at solve
time together with the cookie in the same session. Same class of trap as the Cloudflare
challenge in §9/§11: the fingerprint and the token are a pair.

Corollary for the report: a negative produced through a throttled sweep is not a negative until
the throttled requests have been re-run clean. Say which fraction was re-tested.

## 15. Background collectors keep appending after you start consuming them

A `katana` crawl launched in the background was still writing to `kata.txt` when the endpoint map
was built from it: the file read as 39,620 lines at merge time and finished at **894,284** lines
(47,729 with query strings). The sweep ran on the partial corpus, and a later re-merge found
"new" endpoints — i.e. the coverage claim was built on a file that grew underneath it.

Rules:

- **Consume a collector's output only after its completion notification**, or treat the run as
  provisional and re-merge at the end.
- **Always re-merge and diff at the end**, even if you think the job was done. Rebuild the
  endpoint→param map from the final files and compare against what you actually scanned:

```python
tested = set(json.load(open("endpoint_params_all.json")))
new = {f"https://{u.netloc}{u.path or '/'}" for u in map(urlsplit, corpus_urls)} - tested
print(len(new), sorted(new)[:15])
```

- **Diff ≠ gap.** Of 38 endpoints that appeared only in the completed crawl, every one was noise —
  `%5C`-encoded affiliate redirects (`/\%5C/www.cmegroup.com…`) and `wp-content/plugins/*.js|css`
  assets. Filter static extensions and junk hosts **before** calling something an untested
  endpoint, then scan whatever real endpoints remain (on this run: zero).
- State the corpus size you actually swept, with the file/line count, in the notes. "5,016 URLs"
  is auditable; "the crawl" is not.

Related: when a long job is a *server* rather than a collector (PoC harness, local proxy), kill it
by PID from the process manager. `pkill -f script.py` also matches the shell running the command
when that same command line mentions the filename, so it kills your own tool call
(`exit -15`, no output). Use `pkill -f "[s]cript.py"` and keep the bare filename out of the rest
of the command.

