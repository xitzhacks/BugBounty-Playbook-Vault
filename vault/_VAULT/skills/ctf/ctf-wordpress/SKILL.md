---
name: ctf-wordpress
description: WordPress CTF / hacking-challenge methodology — recognizing decoy WordPress fronts (404-honeypot masking of all internals), bypassing the cookie-leaked-captcha + PoW login gate, and exploiting the canonical "performance plugin" pre-auth RCE (W3 Total Cache CVE-2025-9501 mfunc eval). Use for any WordPress-themed CTF7 / CTF / bug-bounty target where the surface looks suspiciously locked down or AI-agent-honeypot comments appear.
category: ctf
---

# CTF WordPress — Decoy Fronts, Login Bypass, W3TC mfunc RCE

## When to use
- Target is a WordPress site in a CTF / lab / bug-bounty context.
- Especially when: homepage shows an `AI-AGENT-NOTICE ... SECURE ... ctf7{h0neyp0t...}` comment, OR every `/wp-content/plugins/*`, `admin-ajax.php`, `xmlrpc.php` (non-pingback), `/wp-comments-post.php` returns a 404 with a FULL WordPress HTML decoy page (not a real short 404).
- "Parth Bhandari" style challenges (CTF7) consistently use this decoy pattern.

## Key mental model
These are CUSTOM apps mimicking WordPress, NOT real WP. The front is a deliberate honeypot. The vuln still maps to a REAL CVE (author's pattern observed: Aegis→CVE-2025-29927 Next.js middleware; PantryPal→CVE-2025-23211 Tandoor Jinja SSTI; NorthWind→W3TC CVE-2025-9501). Your job: identify the real CVE from the description, then find the ONE reachable delivery vector among surviving endpoints.

## Step 0 — Recognize the decoy (don't waste time)
Signs the WordPress is a decoy front:
- `?p=N` / `?page_id=N` re-render the homepage (no individual post served).
- `/wp-content/plugins/<any-slug>/` → 404 (even via the 403-dir-presence trick; the WAF masks the whole tree).
- `/wp-json/wp/v2/users` or `/posts` works but returns ANONYMIZED minimal fields (only `id`,`name`,`slug`/`title`); single items `/users/1` → 404; `_fields=` can't force more.
- Multiple fake "flag" HTML comments: `ctf7{h0neyp0t_html_n0tice...}`, `ctf7{r0b0ts_h0neyp0t_n0t_real}`, `ctf7{wp_c0nfig_bak_is_a_decoy...}`.
- `/wp-comments-post.php`, `admin-ajax.php`, `admin-post.php`, `xmlrpc.php` (non-pingback), `.git`, `.env` all 404/masked.

Once recognized, STOP brute-forcing plugin slugs — the WAF masks the whole tree. Pivot to the SURVIVING endpoints only:
`/`, `/wp-login.php`, `/wp-json/wp/v2/{users,posts}` (collections), `/feed/`, `/xmlrpc.php` (pingback-only), `/captcha.png`, `/pow`, `/robots.txt` (often a honeypot too).

## Step 1 — Login gate bypass (cookie-leaked captcha + PoW)
These challenges gate login behind a captcha whose ANSWER leaks in the session token and a client-side PoW.
- Cookie name varies (`sessionid`, `wordpress_logged_in_<hash>`, `next-auth.session-token`). Decode the JWT/session header (base64urlsafe, NO verification) → find `cap` (captcha answer) and `pow_challenge`.
- `GET /pow` (or read the cookie after it) returns `{"bits":N,"challenge":"<hex>"}`. Solve: find k such that SHA-256(`challenge+":"+k`) has leading-zero BITS >= N (count LEADING ZERO BITS, not nibbles — see `scripts/wp_login_bypass.py`).
- POST `/wp-login.php` with `log`,`password`,`captcha=<cap>`,`pow=<challenge>:<k>`.
- IMPORTANT: brute-forcing passwords is NOT the intended path (locks with 429, no creds given). Use the bypass ONLY to AUTH as a provided low-priv user to reach an authenticated feature. If no creds given, login is a dead end — move on.

## Step 2 — The "performance plugin" hole = W3TC CVE-2025-9501
Description "obscure plugin / performance tweak / handle high traffic / massive hole" ⇒ **W3 Total Cache** pre-auth command injection (CVSS 9.0, all versions < 2.9.1). Full mechanics in `references/w3tc-cve-2025-9501.md`.
- Vuln: W3TC page-cache `eval()`s `<!-- mfunc <W3TC_DYNAMIC_SECURITY> PHP-CODE <!-- /mfunc <W3TC_DYNAMIC_SECURITY> -->` found in cached pages.
- Pre-auth delivery: unauthenticated COMMENT containing the mfunc tag (gets cached, then eval'd on next page load). Requires the `W3TC_DYNAMIC_SECURITY` secret (default doc value `mycode`; writeup used `rcesec`).
- If comments/ajax/plugin paths are masked (decoy), the delivery vector is firewalled → you CANNOT exploit via HTTP. Report the clue + state you need the secret or a non-masked endpoint.

## Rotation rule (user expectation)
When one enumeration approach dead-ends (e.g., plugin-slug guessing), ROTATE through delivery vectors BEFORE declaring "decoy, unsolvable":
comments → search/`?s=` reflection → custom REST routes (hit directly even if not in `/wp-json/` root) → xmlrpc `system.multicall` → `admin-post.php` `admin_post_nopriv_*` → login (if creds given) → cookie/UA reflection → root file backups (`/wp-config.php~`, `/robots.txt`). The user expects persistence + creativity, not an early dead-end.

## Pitfalls
- PER-PORT SCOPE: on multi-port CTF boxes each port is a SEPARATE challenge. Do NOT reuse tokens/creds/exploits across ports. Stay strictly within the assigned port unless told otherwise. (User: "strict to this port as every port has different challenges".)
- Do NOT submit honeypot flags (`ctf7{h0neyp0t...}`, `ctf7{r0b0ts...}`, `ctf7{wp_c0nfig_bak...}`).
- Decoy 404s return FULL WordPress HTML (~2621 bytes), not a short 404 — distinguish from real 404s.
- No reflected user input anywhere on a decoy front ⇒ the mfunc `eval()` has no reachable injection point; conclude delivery is firewalled.
- **POST-with-tokens bare-404 is NOT a WAF bypass.** A `POST` to a masked path (e.g. `/wp-comments-post.php`) carrying fresh captcha+PoW+cookies sometimes returns a *bare* WordPress 404 (real "no route") instead of the honeypot. This is a STALE-TOKEN RACE on that single attempt, not a method-based bypass — re-run with brand-new tokens; it will return the honeypot decoy. Confirmed empirically this session: all masked paths (GET and POST, with or without valid tokens) are firewalled. Do not pivot your whole exploit on that one-off bare 404.
- **`?s=` reflection / custom-REST direct-hits are dead on decoy fronts.** Even with proper URL-encoding, `?s=<mfunc>` returns the static homepage (no "Search results" heading) and unknown `wp-json/<ns>/` namespaces 404. Test each ONCE, but do not over-invest — on a confirmed decoy front the entire `/wp-content/*` + comment/ajax/xmlrpc surface is firewalled regardless of method/headers/encoding.
- **Login brute-force locks fast.** The server returns HTTP 429 after ~2 rapid `/wp-login.php` POSTs. If you must brute (user explicitly asks, e.g. "try admin/admin"), use the lock-aware template `scripts/wp_lock_aware_brute.py` (150s between attempts, 320s wait on 429). Brute is otherwise NOT the intended path — prefer the real CVE once identified.
- Observed PoW difficulty on these CTF7 boxes: `bits=12` (SHA-256 leading-zero bits). Solver in `scripts/wp_login_bypass.py` handles any `bits`.

## References
- `references/w3tc-cve-2025-9501.md` — mfunc eval mechanics, secret-bypass trick (2.8.13–2.9.1), payloads.
- `references/decoy-signals.md` — quick decoy-recognition checklist.
- `scripts/wp_login_bypass.py` — reusable captcha(cookie)+PoW login solver template.
- `scripts/wp_lock_aware_brute.py` — lock-aware admin-password brute (spacing + 429 wait); use only when the user explicitly wants credential guessing.
