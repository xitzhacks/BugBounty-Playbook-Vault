---
name: targeted-subdomain-recon
description: >-
  Targeted multi-root subdomain enumeration and liveness recon for Web
  Service / REST API bug-bounty scopes. Covers fast enumeration (subfinder +
  assetfinder + crt.sh), httpx live-host probing with the ANSI-stripping
  pitfall, URL/endpoint extraction from LIVE hosts via gau/wayback, strict
  in-scope filtering, and deduped REST path-pattern extraction. Includes a
  re-runnable pipeline script. Use when a target has several roots
  (*.a.io, *.a.com, *.b.io) and the asset class is API/web service.
---

# SKILL: Targeted Multi-Root Subdomain & API Recon

> Use when scope spans multiple roots (e.g. `*.abema.io`, `*.abema-tv.com`,
> `*.abem.io`) and the target class is "Web Service / REST API". This is the
> API-focused companion to generic recon: it trades exhaustiveness for speed and
> keeps every artifact strictly in-scope.

## 1. PIPELINE (summary)

```
enumerate subs (subfinder + assetfinder + crt.sh)
  -> liveness probe (httpx, strip ANSI!)
    -> URL extraction from LIVE API hosts only (gau + waybackurls)
      -> strict in-scope root filter
        -> deduped REST path patterns (/vN/...)
```

A copy-paste re-runnable version is at `scripts/multi_root_recon.sh`.
Per-source yield, the candidate→records→live funnel shape, the RFC1918/Host-header
test and the sibling-domain tell-tales that expose staging:
`references/enumeration-source-matrix.md`.

## 2. STEP-BY-STEP

### 2.1 Enumerate subdomains (fast sources first)
```bash
roots=(abema.io abem.io abema-tv.com abema-tv.org)
: > subs_raw.txt
for r in "${roots[@]}"; do
  subfinder -d "$r" -silent >> subs_raw.txt 2>/dev/null
  assetfinder -subs-only "$r" >> subs_raw.txt 2>/dev/null
  # crt.sh — wrap in curl+python; tolerate permission BLOCKS / timeouts
  curl -s --max-time 40 "https://crt.sh/?q=%25.$r&output=json" 2>/dev/null \
    | python3 -c "import sys,json
try:
    [print(e['name_value']) for e in json.load(sys.stdin)]
except Exception: pass" 2>/dev/null >> subs_raw.txt
done
# tight regex: only keep the exact roots
root_alt=$(IFS='|'; echo "${roots[*]}" | sed 's/\./\\./g')
grep -oiE "[a-z0-9.-]+\\.(${root_alt})\$" subs_raw.txt | sort -u > all_subs.txt
```

### 2.1b Brute force + wildcard check — passive sources miss whole clusters

Passive sources return what CT logs and crawlers have seen. Legacy service names
and *staging clusters* are routinely absent: on a 2026 engagement the passive
union returned 30 names, while a wordlist brute added `ftp`, `mail`, `webmail`
and surfaced a completely separate `chartcalc.com` staging estate
(`staging-v2/v3/v5`, `ts01-staging*`, `wordpress-ts01-staging`) that no passive
source knew about — and that estate was the only place running Stripe **test**
keys.

```bash
# 0) wildcard check FIRST — if *.<root> resolves, every brute hit is fake
dig +short zzqxwv987.target.com          # NXDOMAIN => no wildcard, brute is valid

# 1) brute (dnsx; 150 threads eats 100k words in a couple of minutes per root)
for d in target.com target-staging.com; do
  echo "### $d"
  dnsx -d "$d" -w /usr/share/seclists/Discovery/DNS/bitquark-subdomains-top100000.txt \
    -silent -t 150 -retry 1
done > brute.txt
```

Caveats that cost time:
- Generic wordlists find dictionary names, not **naming conventions**. Numbered
  and versioned hosts (`1.host`, `staging-v5`) will never appear. Harvest the
  convention from CSP `frame-ancestors`/`script-src`, Sentry configs and JS
  bundles, then brute a custom list built from it.
- A brute returning 0 for a root you *know* is live means the loop ate the root
  — not that the root is empty. Sanity-check with one known-live name.

### 2.1c crt.sh is 502 as often as not — swap in certspotter + hackertarget

certspotter (`api.certspotter.com/v1/issuances?domain=…&expand=dns_names`) and
hackertarget (`api.hackertarget.com/hostsearch/?q=…`) both answered instantly
while crt.sh returned 502 for the whole session, and between them they produced
k8s ingress names subfinder never returned. Commands + caveats:
`recon-pitfalls` §4.

### 2.1d RFC1918 cluster names are testable, not "unreachable"

k8s ingress names resolving to `10.x.x.x` are not automatically dead — public
ALBs often route by `Host` header. Test each internal name against every public
ALB IP **with a baseline bogus-Host request first**, and record the negative.
Full matrix and result shape: `recon-pitfalls` §13.

### 2.1e CT logs are not a fallback — they are usually the highest-yield source

Treat crt.sh as a **primary** source, not the thing you try after subfinder. Measured 2026
engagement (`*.tnsi.com`, 3 scope roots): subfinder+assetfinder returned ~99 names; crt.sh
returned **1,096 unique names, 907 of which no DNS tool knew**. After filtering, 590 were
externally plausible and **69 were live — and BOTH findings of the engagement lived only on
CT-discovered hosts** (`dev.tnspaysb` Storybook, `tnsiqgen` Vite dev server). The subfinder-only
host list would have produced a clean, useless report.

```bash
# crt.sh 502s intermittently — retry before falling back to certspotter
for i in 1 2 3; do
  code=$(curl -sk -m 60 "https://crt.sh/?q=%25.$ROOT&output=json" -o crt.json -w "%{http_code}")
  [ "$code" = "200" ] && break; sleep 8
done
python3 - <<'PY'
import json
names=set()
for row in json.load(open('crt.json')):
    for n in str(row.get('name_value','')).split('\n'):
        n=n.strip().lower().lstrip('*.')          # strip wildcard prefix
        if n.endswith('tnsi.com') and '*' not in n: names.add(n)
open('ct_all.txt','w').write('\n'.join(sorted(names)))
PY

# separate EXTERNAL from internal naming conventions before probing — a 590-name
# list of *.corp / *.red / *.win2k.corp hosts is noise that burns httpx time
grep -vE '\.(corp|red|win2k|vprod)\.|\.corp\.|\.red\.|\.win2k\.' ct_all.txt > ct_ext.txt

# then the usual liveness probe, and diff against what you already had
comm -23 <(sort -u ct_all.txt) <(sort -u subs_raw.txt) > ct_new.txt
httpx -l ct_ext.txt -silent -t 50 -timeout 6 -retries 1 -status-code -title -tech-detect \
  -o ct_live.txt
```

Two reporting rules that come out of this:
- **Report the delta, not the total**: "99 from passive DNS, +907 from CT, 69 of those live" is
  the shape that explains why the sweep was worth running.
- **CT-only names are intel, not a finding.** ~900 `air*-*-*.corp.tnsi.com` infrastructure names
  appear in public certificate logs by design; never write them up as a leak. Use them to build
  the Host-header / ALB routing matrix (§2.1d) instead.

### 2.2 Liveness probe with httpx
```bash
cat all_subs.txt | httpx -silent -threads 60 -timeout 8 -retries 1 \
  -status-code -title -tech-detect -follow-redirects > live_raw.txt
```
**PITFALL (high-value):** httpx embeds ANSI color codes in its output
(e.g. `32m200`, `31m403`, `33m302`). A naive `grep '\[200\]'` will
SILENTLY miss everything. Always strip first:
```bash
sed -E 's/\x1b\[[0-9;]*m//g' live_raw.txt > live_clean.txt
grep -E '\[200\]' live_clean.txt          # now works
awk -F'[][]' '{print $3}' live_clean.txt | sort | uniq -c   # status spread
```

### 2.3 URL extraction from LIVE API hosts ONLY
```bash
: > gau.txt
for h in $(grep -iE 'api|gateway|auth|realtime|user|service' live_clean.txt \
             | awk '{print $1}' | sed 's#https\?://##; s#/.*##'); do
  gau "$h" >> gau.txt 2>/dev/null
  waybackurls "$h" >> gau.txt 2>/dev/null
done
sort -u gau.txt > gau_uniq.txt
```
Don't waste gau/wayback rate-limit budget on dead hosts — only feed live ones.

### 2.4 Strict in-scope filter
```bash
grep -iE "https?://[^/]*\\.(${root_alt})/" gau_uniq.txt | sort -u > gau_inscope.txt
```
gau/wayback routinely mix in unrelated domains — always scope-filter.

### 2.5 Deduped REST path patterns
```bash
sed -E 's#https?://[^/]+##; s/\?.*$//' gau_inscope.txt | sort -u > api_paths.txt
grep -E '^/v[0-9]' api_paths.txt      # versioned REST = prime targets
```

### 2.6 Coverage cross-check
```bash
comm -12 <(sed -E 's#https?://##; s#/.*##' live_clean.txt | sort -u) \
          <(sort -u all_subs.txt) > live_in_scope.txt
```

## 3. PITFALLS (learned the hard way)

- **Resuming an engagement is not a licence to reuse old recon.** If the target
  folder already has `recon_notes.md` / `subs_all.txt` from a previous session,
  those are a *seed*, not the inventory. Re-enumerate at the top of every
  session: passive union + brute + wildcard check. An operator who has been in
  the target before will ask "did you test all subdomains?" — and if the answer
  comes from stale notes, it is wrong. Cost of the refresh: ~10 minutes; cost of
  missing a cluster: the whole engagement (the staging estate that carried the
  test keys was invisible in the previous session's notes).
- **Report inventory as a funnel, not a list:** `48 candidate names → 87 DNS
  records → 30 live hosts`, each live host tagged tested / redirect / blocked /
  RFC1918. That is the only shape that survives scrutiny.
- **amass passive is SLOW over multiple roots.** Real run:
  `amass enum -passive -d r1 -d r2 -d r3 -d r4` produced ZERO output after
  9+ minutes, had to be killed. Prefer `subfinder` + `assetfinder` (both
  finish in seconds). If you must use amass: scope to a SINGLE root, or run
  backgrounded with a timeout and merge the partial file after `kill`
  (`cat amass.txt | grep -oE '...'`).
- **httpx ANSI codes** (§2.2) break status-code greps — strip before filtering.
- **Only run gau/wayback on LIVE hosts.** Dead subs waste budget, return nothing.
- **Always scope-filter the URL dump** with a strict root regex.
- **crt.sh may be permission-BLOCKED** in restricted command envs. Wrap in
  `curl + python` and tolerate failure; never let it abort the pipeline
  (use `|| true` / `2>/dev/null`).
- **API-focused scope:** when the user says "Web Service / REST API", prioritize
  hosts whose names contain `api|gateway|auth|realtime|service|v1|v2` and
  extract versioned (`/vN/...`) path patterns as the primary attack surface.
  Combine with the `js-secret-scan` skill (its §6 endpoint extraction) to also
  pull API hostnames from the target's JS bundles.

## 4. DELIVERABLE FILE NAMING

For each recon pass, write to the working dir:
- `subdomains_<tag>_all.txt`   — every unique subdomain found
- `live_subdomains_<tag>.txt`  — httpx-verified live hosts (filtered working)
- `gau_<tag>_inscope.txt`     — discovered URLs, strictly in-scope
- `api_paths_<tag>.txt`        — deduped REST path patterns
- `live_<tag>_clean.txt`       — live hosts w/ status+title+tech (ANSI stripped)

## 5. WHAT TO DO WITH THE OUTPUT

- Live `api.*` / `gateway.*` 200 hosts → primary REST surface.
- Auth-gated 401/403 hosts (Basic, Cloudflare Access, Google IAP) → probe for
  auth bypass / misconfig, but note they may be out of direct scope.
- Versioned paths like `/v1/users/{id}` and `/v1/media/slots/{id}` → BOLA/IDOR
  candidates (swap the ID). Business-logic endpoints (`/v1/auth/oneTimePassword`,
  `/v1/media/token`) → account-takeover / token-abuse surface.
- 415/405 on GET → the endpoint expects a POST/PUT body (wrong method/verb).
