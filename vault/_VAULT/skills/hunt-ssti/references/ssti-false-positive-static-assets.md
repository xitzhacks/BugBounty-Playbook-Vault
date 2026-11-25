# SSTI False Positive: Static Asset Filenames

## The Problem

Testing `{{7*7}}` → `49` is the standard SSTI detection probe. But many modern web apps (especially Next.js, React SPAs, and CDN-hosted apps) serve CSS/JS bundles whose filenames or content contain `49`, `7777777`, `14`, etc.

### Real Example (2026-09-17)

Target: Barracks Bets casino app (Next.js) at `32.197.232.175`

Testing `/?q={{7*7}}` returned `49` **6 times** in the response. Initial assessment: "SSTI confirmed!"

**Reality:** All 6 occurrences were in static asset paths:
- `/_next/static/css/30e5c4cce496650d.css` (contains `49` in the hash)
- `/_next/static/media/bb3ef058b751a6ad-s.p.woff2`
- `/_next/static/media/e4af272ccee01ff0-s.p.woff2`
- JS bundle chunks with `49` in their content hashes

After stripping `<script>`, `<style>`, and all `/_next/static/` paths — **ZERO** instances of `49` remained. SSTI was **FALSE POSITIVE**.

## Verification Checklist

Before reporting SSTI:

1. **Strip static assets** — Remove `<script>...</script>`, `<style>...</style>`, and all URLs matching `/_next/static/`, `/static/`, `/assets/`, `/build/`, `/dist/`, `*.css`, `*.js`, `*.woff*`, `*.png`, etc.

2. **Use unique payloads** — `49` is ambiguous. Use values that won't appear in hex hashes or common numbers:
   - `{{13*13}}` → `169`
   - `{{47*3}}` → `141`
   - `{{99*99}}` → `9801`
   - `{{123*123}}` → `15129`

3. **Baseline comparison** — Send the same request with a non-SSTI value (e.g., `?q=test123`). Diff the responses. If identical, the signal is environmental.

4. **Cross-validate the vector** — If you think it's SSTI, try accessing `{{config}}`, `{{self}}`, `{{request}}`. If those return empty or are stripped, it's not SSTI.

5. **Check the framework** — Next.js, Gatsby, and other static-site generators rarely have SSTI. The server returns pre-built HTML. Template injection would only happen if the app uses server-side rendering with user input in templates (rare).

## When SSTI IS Likely

- The app uses Flask/Django/PHP/Ruby templates directly
- User input appears in the HTML body (not just in JS/CSS filenames)
- Error messages reveal the template engine (e.g., "jinja2.exceptions", "Template Error")
- The `{{config}}` or `{{self}}` payloads return actual Python objects

## When SSTI is UNLIKELY

- Next.js, Gatsby, or other static-site generators
- The numeric result only appears in CSS/JS filenames
- Responses are identical regardless of payload
- The app is a SPA that fetches data via API calls (check the API endpoints instead)
