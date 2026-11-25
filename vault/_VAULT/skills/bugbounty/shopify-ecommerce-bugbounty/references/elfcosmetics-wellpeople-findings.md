# Session Findings — e.l.f. Cosmetics + WellPeople (BC Program)

**Date:** 2026-09-20
**Targets:** elfcosmetics.com, wellpeople.com
**Scope:** Main domains only (subdomains OUT OF SCOPE per user)

---

## Recon Summary

### elfcosmetics.com
- 97 subdomains enumerated, 87 live
- Tech: Shopify Hydrogen (React/Vite), Azure checkout, WordPress blog, DataGrail privacy center
- GraphQL: `checkout.elfcosmetics.com/api/graphql` (properly secured)
- Azure checkout: `www.global.elfcosmetics.com` (SPA, no exposed API)

### wellpeople.com
- 12 subdomains, 5 live
- Tech: Shopify Hydrogen (React/Vite)
- GraphQL: `www.wellpeople.com/api/graphql` (properly secured)
- Quiz S3 bucket: empty

---

## JS Analysis Findings

### CRITICAL: eval() in freeGiftLogicv1.js
- **File:** `freeGiftLogicv1.js` (loaded from cdn.shopify.com extensions on both targets)
- **Lines:** 1089, 1692, 3437
- **Pattern:** `eval(gfg.settings.app.executeCustomScriptOnLoad)` and similar
- **Impact:** If attacker controls `gfg.settings.app` (via XSS, admin panel, or mass assignment), arbitrary JS execution → session hijack, payment manipulation, malware
- **Mitigation:** Remove eval(), use Function() with strict CSP or sandboxed iframe

### MEDIUM: Storefront Access Token in DOM
- **File:** `portable-wallets.en.js` (WellPeople)
- **Pattern:** `get accessToken(){return this.getAttribute("access-token")}`
- **Impact:** Token readable via XSS on checkout page
- **Mitigation:** Use HttpOnly cookies instead of HTML attributes

### MEDIUM: Cookie Manipulation
- **Files:** `main.js` (WellPeople), `event-logger-pHrAqOE3.js` (ELF)
- **Pattern:** `document.cookie=` without HttpOnly flag
- **Impact:** XSS can steal/modify cookies
- **Mitigation:** HttpOnly flag for session cookies

### MEDIUM: Firebase Storage URL Exposed
- **File:** `content-DjE6_ikv.js` (ELF)
- **URL:** `https://firebasestorage.googleapis.com/v0/b/builder-3b0a2`
- **Impact:** Project ID exposed, potential bucket listing if misconfigured

### MEDIUM: S3 Bucket URL Exposed
- **File:** `client-app.js` (WellPeople)
- **URL:** `https://vidjetvideostorage.s3.eu-west-1.amazonaws.com/`
- **Impact:** Bucket name exposed, potential listing if misconfigured

---

## API Endpoints Found (all require auth)

| Endpoint | Source File |
|----------|-------------|
| `/api/loyalty` | loyalty-D_ZYHjXQ.js |
| `/api/bogos` | root-AW41oaZJ.js |
| `/api/cart/` | page-layout--vk0Dx6_.js |
| `/api/cart-promo-config` | root-AW41oaZJ.js |
| `/api/volume-discounts` | root-AW41oaZJ.js |
| `/api/delivery-estimates` | page-layout--vk0Dx6_.js |
| `/api/og-next-delivery` | page-layout--vk0Dx6_.js |
| `/api/og-add-item` | page-layout--vk0Dx6_.js |
| `/api/ordergroove-product` | page-layout--vk0Dx6_.js |
| `/api/quick-shop-product/` | product-card-BhtAaspE.js |
| `/api/braze/id` | root-AW41oaZJ.js |
| `/api/braze/ccc` | use-ga4-events-C9DcA3Q7.js |
| `/api/v1/track` | content-DjE6_ikv.js |
| `/api/v1/image` | content-DjE6_ikv.js |
| `/api/v1/file/` | image-Dol13hii.js |
| `/v1/ip/geo` | freeGiftLogicv1.js |
| `/api/unstable/graphql` | production-_raR3Sml.js |
| `/graphql` | production-_raR3Sml.js |

---

## Subdomain Takeovers (OUT OF SCOPE — for reference only)

| Subdomain | CNAME | Status |
|-----------|-------|--------|
| rewards.elfcosmetics.com | cname.vercel-dns.com | 404 (dangling Vercel) |
| quiz.elfcosmetics.com | do34hf0dfdfql.cloudfront.net | 404 (dangling CloudFront) |
| oldwww.elfcosmetics.com | t.sni.global.fastly.net | 000 (dangling Fastly) |

---

## Key Files

```
~/Bugbounty/BC/
├── elfcosmetics.com/
│   ├── recon/
│   │   ├── subs_all.txt (97 subdomains)
│   │   ├── live_raw.txt (87 live hosts)
│   │   ├── urls_all.txt (1242 URLs)
│   │   └── js_files.txt (46 JS files)
│   └── js_analysis/
│       ├── js_files/ (128 JS files downloaded)
│       └── scan_results.json (192 findings)
├── wellpeople.com/
│   ├── recon/
│   │   ├── subs_all.txt (12 subdomains)
│   │   └── live_raw.txt (5 live hosts)
│   └── js_analysis/
│       └── js_files/ (23 JS files downloaded)
├── js_analysis/
│   ├── scan.py (JS scanner script)
│   └── scan_results.json (all findings)
├── RECON_REPORT.md
├── IDOR_BAC_REPORT.md
└── JS_ANALYSIS_REPORT.md
```
