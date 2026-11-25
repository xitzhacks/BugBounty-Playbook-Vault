#!/usr/bin/env bash
# multi_root_recon.sh — targeted multi-root API recon pipeline
# Companion to targeted-subdomain-recon SKILL.md (§1/§2).
#
# Usage:  ./multi_root_recon.sh root1.tld root2.tld root3.tld ...
#   e.g.  ./multi_root_recon.sh abema.io abem.io abema-tv.com abema-tv.org
#
# Stages: enumerate subs (subfinder+assetfinder+crt.sh) -> httpx liveness ->
#         gau/wayback on LIVE API hosts -> strict in-scope filter ->
#         deduped REST path patterns. Writes everything to recon_<ts>/.
#
# Requires: subfinder, assetfinder, httpx, gau, waybackurls, curl, python3.
set -uo pipefail

roots=("$@")
if [ "${#roots[@]}" -eq 0 ]; then
  echo "Usage: $0 root1.tld root2.tld ..." >&2
  exit 1
fi

# Build a regex alternation of the roots (dots escaped).
root_alt=$(IFS='|'; echo "${roots[*]}" | sed 's/\./\\./g')

ts=$(date +%Y%m%d_%H%M%S)
out="recon_${ts}"
mkdir -p "$out"
cd "$out" || exit 1

echo "[*] Roots: ${roots[*]}"
echo "[*] Output dir: $out"

# --- 1. Enumerate subdomains (fast sources) ---
: > subs_raw.txt
for r in "${roots[@]}"; do
  echo "    enumerating $r ..."
  subfinder -d "$r" -silent >> subs_raw.txt 2>/dev/null || true
  assetfinder -subs-only "$r" >> subs_raw.txt 2>/dev/null || true
  # crt.sh — may be blocked by permissions in some envs; tolerate failure.
  curl -s --max-time 40 "https://crt.sh/?q=%25.${r}&output=json" 2>/dev/null \
    | python3 -c "import sys,json
try:
    [print(e['name_value']) for e in json.load(sys.stdin)]
except Exception: pass" 2>/dev/null >> subs_raw.txt || true
done
grep -oiE "[a-z0-9.-]+\\.(${root_alt})\$" subs_raw.txt | sort -u > all_subs.txt
echo "[+] all_subs.txt: $(wc -l < all_subs.txt) unique subdomains"

# --- 2. Liveness probe with httpx ---
cat all_subs.txt | httpx -silent -threads 60 -timeout 8 -retries 1 \
  -status-code -title -tech-detect -follow-redirects > live_raw.txt 2>/dev/null || true
# STRIP ANSI color codes (httpx embeds them, e.g. 32m200) before grepping.
sed -E 's/\x1b\[[0-9;]*m//g' live_raw.txt > live_clean.txt
echo "[+] live_clean.txt: $(grep -cE '^https?://' live_clean.txt) live hosts"
echo "    status spread:"
awk -F'[][]' '{print $3}' live_clean.txt | sort | uniq -c | sort -rn

# --- 3. URL extraction from LIVE API-ish hosts only ---
: > gau.txt
for h in $(grep -iE 'api|gateway|auth|realtime|user|service' live_clean.txt \
             | awk '{print $1}' | sed 's#https\?://##; s#/.*##'); do
  gau "$h" >> gau.txt 2>/dev/null || true
  waybackurls "$h" >> gau.txt 2>/dev/null || true
done
sort -u gau.txt > gau_uniq.txt
echo "[+] gau_uniq.txt: $(wc -l < gau_uniq.txt) URLs"

# --- 4. Strict in-scope filter ---
grep -iE "https?://[^/]*\\.(${root_alt})/" gau_uniq.txt | sort -u > gau_inscope.txt
echo "[+] gau_inscope.txt: $(wc -l < gau_inscope.txt) in-scope URLs"

# --- 5. Deduped REST path patterns ---
sed -E 's#https?://[^/]+##; s/\?.*$//' gau_inscope.txt | sort -u > api_paths.txt
echo "[+] api_paths.txt: $(wc -l < api_paths.txt) unique paths"
echo "    versioned REST paths: $(grep -cE '^/v[0-9]' api_paths.txt)"

# --- 6. Coverage cross-check ---
comm -12 <(sed -E 's#https?://##; s#/.*##' live_clean.txt | sort -u) \
          <(sort -u all_subs.txt) > live_in_scope.txt
echo "[+] live_in_scope.txt: $(wc -l < live_in_scope.txt) live hosts covered"

echo "[*] Done. Deliverables in $out/"
