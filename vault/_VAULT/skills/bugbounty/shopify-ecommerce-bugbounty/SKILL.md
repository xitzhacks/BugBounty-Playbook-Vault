---
name: shopify-ecommerce-bugbounty
description: "Full recon → hunt → report workflow for Shopify-based e-commerce bug bounty targets. Covers scope discipline (main-domain-only when specified), subdomain-to-main-domain escalation rules, JS bundle analysis for secrets/eval()/sinks, GraphQL Storefront API IDOR testing, OAuth flow security, and consolidated report formatting. Use when hunting on Shopify Hydrogen/Oxygen stores, headless storefronts, or any e-commerce target where Shopify is the backend."
---

# Shopify E-Commerce Bug Bounty — Recon → Hunt → Report

## Trigger Conditions

- Target runs Shopify (Hydrogen, Oxygen, headless storefront)
- Scope includes *.shopify.com or custom domains with Shopify backend
- Bug bounty program (H1, Bugcrowd, Intigriti, Immunefi)
- Recon needed: subdomains, JS bundles, API endpoints, OAuth flows

---

## 1. SCOPE DISCIPLINE (CRITICAL)

**Always confirm scope before reporting.** When user says "main domains only" or lists specific domains:

- **IMMEDIATELY** discard all subdomain findings (rewards.*, quiz.*, oldwww.*, etc.)
- Only report findings on the explicitly listed domains
- Subdomain takeovers, dangling CNAMEs, and API subdomain exposures are OUT OF SCOPE if only main domains are listed
- Do not waste time probing subdomains that are out of scope

**Scope confirmation questions to ask if unclear:**
1. Are subdomains in scope or only the main domain(s)?
2. Is the checkout subdomain in scope (e.g., checkout.target.com)?
3. Are regional/country subdomains in scope (e.g., ca.target.com, de.target.com)?

---

## 2. RECON PIPELINE (Shopify-Specific)

### Step 1: Identify Shopify
```bash
curl -sI https://target.com | grep -iE "x-shopify|x-generator|shopify"
curl -s https://target.com | grep -oE 'cdn.shopify.com[^"]+' | head -5
```

### Step 2: Subdomain Enumeration (if in scope)
```bash
subfinder -d target.com -silent 2>/dev/null
assetfinder --subs-only target.com 2>/dev/null
curl -s "https://crt.sh/?q=%.target.com&output=json" | python3 -c "import sys,json; [print(e['name_value']) for e in json.load(sys.stdin)]" 2>/dev/null
```

### Step 3: Tech Stack Fingerprinting
- **Shopify Hydrogen** → React/Vite storefront, headless
- **Shopify Oxygen** → framework with `oxygen-v2` in JS paths
- **Custom checkout** → Azure/AWS/GCP backend (not Shopify CDN)
- **WordPress blog** → check /wp-json API exposure
- **DataGrail** → privacy center on preferences.target.com

### Step 4: JS Bundle Extraction
```bash
# Get all JS URLs from main page
curl -s -L -m 15 "https://target.com" | grep -oE '(src|href)="[^"]+\.js[^"]*"' | sed 's/.*="//;s/"//' | sort -u

# Download all JS files
for js in $(cat js_urls.txt); do
    curl -s -m 15 -L -o "$(basename "$js" | cut -d'?' -f1)" "$js"
done
```

### Step 5: GraphQL Discovery
```bash
# Shopify Storefront API
curl -s -X POST -H "Content-Type: application/json" \
  -d '{"query":"{__schema{queryType{name}}}"}' \
  "https://target.com/api/graphql"

# Admin GraphQL (if exposed)
curl -s -X POST -H "Content-Type: application/json" \
  -d '{"query":"{__schema{queryType{name}}}"}' \
  "https://target.com/admin/api/2024-07/graphql"
```

---

## 3. JS BUNDLE ANALYSIS

### Critical Patterns to Find

| Pattern | Why It Matters |
|---------|----------------|
| `eval()` with variable argument | Admin-controlled code execution if XSS exists |
| `document.cookie =` without HttpOnly | Session theft via XSS |
| `storefrontAccessToken` | Token exposure in DOM attributes |
| `firebasestorage.googleapis.com` | Firebase project ID exposure |
| `s3.amazonaws.com/bucketname` | S3 bucket name exposure |
| `innerHTML =` / `outerHTML =` | DOM XSS sinks |
| `postMessage` | Cross-origin message handling |
| `/api/` endpoints | IDOR/BAC testing targets |

### Eval() Pattern (Shopify Extensions)
```javascript
// DANGER: eval() in Shopify extension JS
const customScript = gfg.settings.app.executeCustomScriptOnLoad;
if(customScript){
    eval(customScript);  // Attacker controls this via XSS or admin panel
}
```

**Impact:** If attacker can control `gfg.settings.app` settings (via XSS, mass assignment, or admin panel), they can execute arbitrary JavaScript → session hijack, payment manipulation, malware.

### Scan Script
```python
# Scan all JS files for critical patterns
import os, re

patterns = {
    'EVAL': r'(?i)\beval\s*\(([^)]+)\)',
    'INNERHTML': r'(?i)\.innerHTML\s*=\s*([^;]{1,100})',
    'COOKIE': r'(?i)document\.cookie\s*=\s*([^;]{1,100})',
    'FIREBASE': r'firebasestorage\.googleapis\.com/v0/b/([a-z0-9\-]+)',
    'S3_BUCKET': r's3\.[a-z0-9\-]+\.amazonaws\.com/([a-z0-9\-]+)',
    'API_KEY': r'(?i)(api[_-]?key|client[_-]?secret)\s*[:=]\s*["\']([A-Za-z0-9_\-]{16,})["\']',
}

for root, dirs, files in os.walk('js_files'):
    for f in files:
        if f.endswith('.js'):
            content = open(os.path.join(root, f), errors='ignore').read()
            for ptype, pattern in patterns.items():
                for m in re.finditer(pattern, content):
                    print(f"{ptype}: {f}: {m.group(0)[:100]}")
```

---

## 4. GRAPHQL STOREFRONT API — IDOR TESTING

### Schema Introspection
```bash
curl -s -X POST -H "Content-Type: application/json" \
  -d '{"query":"{__schema{queryType{fields{name args{name type{name kind ofType{name kind}}}}}}}"}' \
  "https://target.com/api/graphql" | python3 -m json.tool
```

### Key IDOR Targets
| Query/Mutation | Risk | Test |
|----------------|------|------|
| `cart(id:)` | HIGH | Swap cart ID, check if other user's cart data returns |
| `customer(token)` | HIGH | Test with empty/invalid token |
| `metaobjects(type:)` | MEDIUM | Test without auth |
| `node(id:)` | MEDIUM | Sequential ID enumeration |
| `product(id:)` | LOW | Usually public, check for hidden fields |

### Testing Method
```bash
# Test 1: Unauthenticated cart access
curl -s -X POST -H "Content-Type: application/json" \
  -d '{"query":"{cart(id:\"gid://shopify/Cart/abc123\"){id buyerIdentity{email}}}"}' \
  "https://target.com/api/graphql"

# Test 2: Sequential cart ID enumeration
for i in 1 2 3 100 1000; do
    curl -s -X POST -H "Content-Type: application/json" \
      -d "{\"query\":\"{cart(id:\\\"gid://shopify/Cart/$i\\\"){id}}\"}" \
      "https://target.com/api/graphql"
done

# Test 3: Customer query without token
curl -s -X POST -H "Content-Type: application/json" \
  -d '{"query":"{customer(customerAccessToken:\"\"){id email}}"}' \
  "https://target.com/api/graphql"
```

**Expected secure behavior:** All return ACCESS_DENIED or null without valid token.

---

## 5. OAUTH FLOW TESTING

### Google Sign-In (GSI) Vulnerabilities
1. **Missing state parameter** — OAuth CSRF → account takeover
2. **Client ID exposed** — aids targeted attacks
3. **Callback accepts fake codes** — weak error handling
4. **No PKCE** — authorization code interception

### Consolidated OAuth Report Format
```markdown
# Target OAuth — Consolidated Report

## DESCRIPTION
[Single paragraph covering all findings]

## FINDINGS
1. [Finding name] — [Severity] | [CWE]
   Impact: [Plain English]
   PoC: [URL or curl command]
   Mitigation: [One line]

## SUMMARY TABLE
| # | Finding | Severity | CVSS |
|---|---------|----------|------|

## REMEDIATION
1. [Action]
2. [Action]
```

---

## 6. REPORT FORMAT PREFERENCES

### User Preferences (from session feedback)
- **Concise:** 3-4 lines per finding, not heavy tables
- **Single description:** One paragraph covering all findings, then list findings separately
- **Plain-English impact:** "Attacker can steal session" not "Confidentiality violation via session token exfiltration"
- **Direct URLs for PoC:** User prefers to take screenshots themselves, provide URLs not automated scripts
- **Light reports:** No verbose tables, multiple sections, or redundant formatting

### Report Template
```
TARGET — CONSOLIDATED REPORT
Target: [domain]
Date: [date]

DESCRIPTION
[Single paragraph — what was tested, what was found]

FINDINGS
1. [Name] — [Severity] | [CWE]
   Impact: [Plain English]
   PoC: [URL/curl]
   Mitigation: [One line]

SUBMIT VIA: [URL]
```

---

## 7. PITFALLS

1. **Scope creep:** User says "main domains only" → immediately discard all subdomain findings
2. **Over-engineering reports:** User wants concise, not verbose tables and sections
3. **Automated PoC scripts:** User prefers direct URLs they can open in browser
4. **False positive eval():** Only report if attacker can control the eval input (XSS, admin panel, mass assignment)
5. **Shopify GraphQL:** Standard Storefront API is properly secured by default — don't report "GraphQL exists" as a finding
6. **Subdomain takeovers:** Only report if subdomains are in scope
7. **JS bundle secrets:** Framework constants (like `storefrontAccessToken` key name) are not hardcoded secrets — only report actual values

---

## 8. RELATED SKILLS

- `web2-recon` — General web2 recon pipeline (subdomain enum, URL crawl, nuclei)
- `hunt-idor` — IDOR hunting methodology (26 public reports)
- `hunt-api-misconfig` — API misconfiguration (mass assignment, JWT, prototype pollution)
- `evidence-hygiene` — PoC screenshot redaction and evidence capture
- `report-writing` — Bug bounty report writing for H1/Bugcrowd/Intigriti/Immunefi

---

## 9. SESSION REFERENCES

- `references/elfcosmetics-wellpeople-findings.md` — Detailed findings from e.l.f. Cosmetics + WellPeople engagement (2026-09-20): eval() vuln, token exposure, API endpoints, subdomain takeovers (out of scope)
