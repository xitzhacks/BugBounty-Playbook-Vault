#!/bin/bash
# Passive subdomain enumeration — SAFE under RVDP/no-automation rules.
# Sources: subfinder (passive), assetfinder, crt.sh cert-transparency.
# NO dnsx/httpx mass probing, NO active scanning. Output deduped to all_subs.txt.
set -u
TARGET="${1:?usage: passive_subs.sh TARGET}"
OUT="${2:-./subdomains}"
mkdir -p "$OUT"
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"

echo "[*] subfinder (passive)..."
subfinder -d "$TARGET" -silent -o "$OUT/sf.txt" 2>/dev/null

echo "[*] assetfinder..."
assetfinder --subs-only "$TARGET" 2>/dev/null | sort -u > "$OUT/af.txt"

echo "[*] crt.sh (cert transparency)..."
curl -s -A "$UA" --max-time 60 "https://crt.sh/?q=%25.${TARGET}&output=json" -o "$OUT/crt.json"
grep -oE '"name_value":"[^"]*"' "$OUT/crt.json" | sed 's/"name_value":"//; s/"$//' | sort -u > "$OUT/crt.txt"

echo "[*] combining + dedup..."
cat "$OUT/sf.txt" "$OUT/af.txt" "$OUT/crt.txt" 2>/dev/null | sed 's/^\*\.//' | tr 'A-Z' 'a-z' | sed 's/[[:space:]]//g' | grep -v '^$' | grep "\.${TARGET}$" | sort -u > "$OUT/all_subs.txt"

# optional clean (strip embedded \n artifacts)
sed 's/\\n/\n/g' "$OUT/all_subs.txt" | grep "\.${TARGET}$" | sort -u > "$OUT/all_subs_clean.txt"

echo "[*] total unique: $(wc -l < "$OUT/all_subs_clean.txt")"
echo "[*] saved: $OUT/all_subs_clean.txt"
