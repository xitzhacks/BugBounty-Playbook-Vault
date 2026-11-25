# Decoy WordPress CTF front — recognition checklist

If MOST of these are true, the WordPress is a CUSTOM decoy (not real WP) and the WAF masks all internals:

- [ ] `?p=N` / `?page_id=N` re-render the homepage (no individual post served).
- [ ] `/wp-content/plugins/<any>/` → 404 (whole tree masked, incl. 403-dir-presence trick fails).
- [ ] `/wp-json/wp/v2/users|posts` works but returns ONLY minimal fields (id/name/slug/title); single items 404; `_fields=` can't force more.
- [ ] Fake flags in HTML comments: `ctf7{h0neyp0t_html_n0tice...}`, `ctf7{r0b0ts_h0neyp0t_n0t_real}`, `ctf7{wp_c0nfig_bak_is_a_decoy...}`.
- [ ] `/wp-comments-post.php`, `admin-ajax.php`, `admin-post.php`, `xmlrpc.php` (non-pingback), `.git`, `.env` all 404/masked.
- [ ] Masked 404s return FULL WordPress HTML (~2621 bytes "NorthWind Journal" decoy), not a short 404.

Surviving (reachable) endpoints on a decoy front:
`/`, `/wp-login.php`, `/wp-json/wp/v2/{users,posts}` (collections only), `/feed/`,
`/xmlrpc.php` (pingback-only → "Pingback target not allowed" on anything else),
`/captcha.png`, `/pow`, `/robots.txt` (often honeypot).

Decision: once decoy confirmed, stop guessing plugin slugs. Pivot to the surviving endpoints and the
real-CVE delivery vector (see SKILL.md Step 1/2). If delivery is also masked, report clue + ask for secret.
