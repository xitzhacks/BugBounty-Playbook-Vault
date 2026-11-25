# Recon False-Positive Pitfalls (real-session discipline)

Two traps that waste a full engagement if uncaught — caught during a LINE WORKS bug-bounty.

## (1) Re-verify "anomaly" findings with a real body fetch BEFORE treating them as bugs
Automation/recon will flag things like "GET /wp/v2/notice/<id> returns 200 without auth — IDOR!".
Before investing, FETCH THE BODY and compare against the public site. In the LINE WORKS engagement
the "primary IDOR candidate" (public notice read via REST) was just `status=publish` WordPress
posts — public by design, identical to what `/notice/<id>/` serves anonymously. NOT a vuln.

Rule: any "authz anomaly" flagged by recon/historical notes must be confirmed by:
  (a) reading the actual response body,
  (b) checking the object's `status` field (publish/private/draft),
  (c) comparing to the unauthenticated public surface.
If it's publicly-intended data, CLOSE it — don't let a prior summary's hype drive the hunt. This is
the "KILL WEAK FINDINGS FAST" rule applied to inherited findings. (The 7-Question Gate in PHASE 4
assumes a real PoC; inherited "anomalies" often fail Q1 because they were never body-verified.)

## (2) Cloudflare / nginx catch-all false positives in exposed-file & path fuzzing
When fuzzing for `.env` / `.git` / backups / admin panels, a Cloudflare-fronted host may return
HTTP 200 for EVERY path (a 404 catch page: `<title>404 - Page not found</title>`) or 301/302
redirect unknown paths to the homepage. Both look like "hits" in a naive status-code grep but are
NOT real files.

Rule: for every fuzz "hit", fetch the body and confirm it is NOT:
  (a) a generic catch-all page (e.g. "404 - Page not found"),
  (b) a redirect to `/` / the homepage.
Only record 200s whose body is the actual expected resource (e.g. a real `robots.txt`, a real
`crossdomain.xml`). Strip catch-all hosts entirely — in the LINE WORKS case `go.line-works.com`
returned 200 for `.env`, `.git/HEAD`, `backup.zip`, `phpinfo.php`, etc., ALL serving the same
"404 - Page not found" body. Also: a `301` on `/.git/HEAD` that follows to the WP homepage is NOT
git exposure.
