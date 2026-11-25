---
name: hunt-bulk-fleet
description: "Sweep MANY targets at once for the same classes of config/infra findings and separate real signal from scanner boilerplate. Built from a 111-host / 341-finding engagement where 147 findings (Lucky13 + BREACH) turned out to be ONE systemic TLS misconfig replicated across 94 hosts — i.e. per-host reporting would have been 147 noise reports. Use when you need to re-test a known finding class across a new fleet of hosts, when triaging a large auto-scanned finding dump, or when deciding which of hundreds of auto-generated findings to actually write up. Includes a working multi-target scanner (nuclei/httpx/stdlib) that sweeps TLS cipher state, security headers, CSP, cookie attributes, CORS, dangerous methods, Swagger/OpenAPI, info disclosure, error pages, rate limiting, open redirect, clickjacking and CSP-report-uri SSRF, then emits a grouped triage report."
sources: olam_findings_engagement, portswigger_research, ssl_labs_research, retirejs
---

# HUNT-BULK-FLEET — Same finding class, many targets, one sweep

## Reality Check (read before you fire anything)

You will end up with hundreds of auto-generated findings. **Most of them are one
misconfiguration multiplied across your fleet, not hundreds of bugs.** From a
real 111-host engagement:

| Finding class | Count | Reality |
|---|---|---|
| Lucky13 (CBC ciphers offered) | 89 | **ONE** root cause: TLS stack config |
| BREACH (CBC ciphers offered) | 58 | Same root cause, double-counted |
| Missing security headers | 25 | ONE root cause: web server config |
| Known vulnerable components | 20 | **Real** — per-host, per-CVE |
| Blind SSRF | 3 | **Real** — 3 separate bugs |
| Open redirect / clickjacking / forced browsing | 3 | **Real** |

Two SSL findings + one "info disclosure" finding on the same host, same root
cause, is **one finding with 3 evidence lines** — not 3 findings. A scanner
that enumerates each cipher as a separate issue is giving you raw signal, not
findings.

**Rules:**
1. **Group by root cause, not by host.** One systemic TLS config = one finding
   with a host table. Do not file 89 Lucky13 reports; you will burn your
   reputation and get the whole batch triaged as noise.
2. **A per-host finding is only per-host if the fix is per-host.** Apache on
   17 hosts with different versions = 17 findings. Same nginx default on 40
   hosts = 1 finding.
3. **Validate before you triage.** "Offered ≠ exploitable" applies to TLS
   ciphers (see `hunt-tls-network`). Missing headers are Info. Your report
   should contain the handful of things a triager will actually accept.

---

## Phase 0 — Scope and target list

```bash
# Build the target list. Confirm every host is IN SCOPE before scanning —
# a fleet scan that wanders outside scope is a policy violation, not a finding.
mkdir -p recon/$ENGAGEMENT && cd recon/$ENGAGEMENT
cat > targets.txt <<'EOF'
app.example.com
api.example.com
10.0.0.5:8443
EOF

# Sanity: resolve and confirm the list
httpx -l targets.txt -silent -o alive.txt -ports 80,443,8080,8443,8000,3000
wc -l alive.txt
```

Keep a separate `oos.txt` for hosts marked out of scope (e.g. a folder named
`FQ_0075_agripal-zuul.olamagri.com - Out of scope`). **Exclude them from the
sweep and from any aggregate report.**

---

## Phase 1 — Fleet sweep

The bundled scanner runs every check across every target concurrently and
emits a grouped triage report.

```bash
# Basic sweep
python3 ~/.hermes/profiles/batman/skills/hunt-bulk-fleet/scripts/fleet_scan.py \
  -t targets.txt -o out/

# With OOB callback (needed for the CSP-report-uri SSRF check)
python3 .../fleet_scan.py -t targets.txt -o out/ --oob yourid.oast.live

# Only the high-value classes
python3 .../fleet_scan.py -t targets.txt -o out/ --only ssrf,openredirect,swagger

# Live targets from httpx
python3 .../fleet_scan.py -t alive.txt -o out/ --deep
```

**Output layout:**
```
out/
  results.json          # machine-readable, one record per target
  summary.md            # THE TRIAGE REPORT — read this
  evidence/<host>_<check>.txt   # raw request/response per finding
```

### Complement with nuclei (broader template coverage)

```bash
nuclei -l alive.txt -severity medium,high,critical -o nuclei.txt -silent
nuclei -l alive.txt -t cves/ -t exposures/ -t misconfiguration/ -o nuclei2.txt -silent

# TLS-specific: catches the Lucky13/BREACH class in one pass
nuclei -l alive.txt -t ssl/ -o nuclei-tls.txt -silent

# Headless screenshot of each host for manual triage
nuclei -l alive.txt -t screenshots/ -o shots.txt -silent
```

### Sibling skills for depth on a specific class
`hunt-tls-network` (TLS/DNS), `hunt-ssrf`, `hunt-open-redirect`,
`hunt-idor`, `hunt-cors`, `hunt-rate-limit` (hunt-brute-force),
`hunt-xss`, `hunt-source-leak` (for JS bundles), `hunt-misc`.

---

## Phase 2 — Triage and group

Read `out/summary.md`. It separates:

- **SIGNAL** — findings that are real and per-host (SSRF, open redirect, known
  vulnerable component, forced browsing, Swagger exposure, dangerous methods).
- **BOILERPLATE** — group these by root cause. One representative per group.

Then fix the boilerplate grouping before it reaches a report:

```bash
# How many distinct root causes are hiding in the "boilerplate"?
jq -r '.findings[] | select(.class=="tls_cbc") | .target' out/results.json | \
  sed 's/\..*//' | sort | uniq -c | sort -rn     # group by registrable domain

# Same for headers / CSP / cookies
jq -r '.findings[] | select(.class=="headers") | .target' out/results.json | \
  sort | uniq -c | sort -rn
```

**Aggregation rule for a report:**

> "Missing HSTS on 94 of 111 hosts (list). All hosts resolve to the same
> load balancer / CDN front end, confirmed by identical `Server` header and
> certificate issuer. Single remediation at the edge fixes all."

That is a stronger, better-scoped report than 94 near-identical reports, and
triage will close the duplicates for you.

---

## Phase 3 — Validate the SIGNAL findings

Every class has a validation gate. The gate is what separates a finding from
a scanner opinion.

| Class | Gate — do not report without this |
|---|---|
| **Blind SSRF (CSP report-uri)** | OOB callback **actually received** from the target server. Show the callback log line. |
| **Open redirect** | `302`/`301` with `Location:` pointing to **your** domain, from the **victim's** host. Not a 200 page that merely renders the param. |
| **Clickjacking** | Target has no `X-Frame-Options` AND no `frame-ancestors` in CSP. Prove with a working iframe PoC hosted by you. |
| **Forced browsing / IDOR** | Show the **actual protected content** (real data), not just a `200` on a path that returns a login page. |
| **Known vulnerable component** | Exact library + version + CVE. Version must be **read from the artifact**, not guessed from a banner. |
| **Swagger / OpenAPI** | `200` + parseable spec listing real endpoints. Include the sensitive ones. |
| **HTTP dangerous methods** | `PUT`/`DELETE`/`TRACE` **actually accepted** and acted on (file written / file deleted / request reflected). |
| **Missing rate limiting** | N requests, **zero** 429/403/lockout, and the sensitive action still succeeds at the end. |
| **TLS ciphers (Lucky13/BREACH)** | Cipher is *offered* = hardening only, Info/Low. Never claim a decrypt. |
| **Missing headers / CSP / cookies** | Info. Do not file standalone. |

Full reproduction payloads for each class: `references/techniques.md`.

---

## Phase 4 — Report the grouped finding

Template: `templates/report-skeleton.md`

```markdown
## <Root cause title> — affecting N of M hosts

**Severity:** <realistic>
**Class:** <CWE>

### Summary
<one paragraph: the single root cause and why it affects N hosts>

### Affected hosts
| Host | Evidence |
|---|---|
| a.example.com | `Server: nginx/1.18.0`, no Strict-Transport-Security |

### Reproduction
<one reproducible request/response pair — NOT one per host>

### Impact
<what an attacker gains, concretely>

### Remediation
<one fix, applied at the shared component>
```

---

## Chain Table

| Finding | Realistic standalone severity | Raised by |
|---|---|---|
| Blind SSRF with confirmed OOB callback | **High** | Critical if it reaches cloud metadata (`169.254.169.254`) or an internal admin API |
| Open redirect on an auth flow | **Medium** | High if it carries a token/OAuth `redirect_uri` |
| Forced browsing exposing real data | **High** | Critical if PII/credentials |
| Known vulnerable component (exploitable) | **Medium–High** | Critical with a working exploit PoC |
| Swagger/OpenAPI with sensitive endpoints | **Medium** | High if it exposes admin/auth endpoints + schemas |
| HTTP dangerous methods (verified write/delete) | **High** | Critical if it yields RCE (e.g. `.jsp` upload) |
| Missing rate limiting on login/OTP | **Medium** | High on OTP/reset flows (account takeover) |
| Clickjacking on a sensitive action | **Medium** | High on payments/permission grants |
| Slowloris DoS | **Medium** | Only if you actually degraded the service |
| TLS ciphers offered (no decrypt) | **Info / Low** | Don't inflate |
| Missing headers / CSP / cookie attrs | **Info** | Usually don't file |

---

## Pitfalls

- **Filing per host.** 89 Lucky13 findings across 89 hosts is ONE config bug.
  Check the `Server` header and cert issuer before assuming hosts are
  independent — they usually share a front end.
- **Double-counting the same root cause.** Lucky13 and BREACH are the *same*
  condition (CBC cipher offered). BREACH additionally needs compression
  enabled. If both fire on the same host, it's one finding.
- **Claiming a decrypt.** No remote Lucky13/BREACH exploit in a normal
  engagement. Report cipher *support*, expect Info/Low.
- **Reporting `report-uri` SSRF without the callback.** "I set a CSP report
  endpoint" proves nothing. You need the target server to actually *make the
  outbound request* to your domain, and you need the log.
- **Guessing versions from banners.** `Server: Apache/2.4.29` is a banner, not
  a version confirmation. For JS libraries, read the version out of the file
  itself (the banner comment) and then map it to a CVE.
- **Leaving OOB/canary infrastructure live.** Tear down collaborators after
  the PoC. Never leave attacker-controlled content on a target domain.
- **Ignoring the out-of-scope marker.** A folder named `... - Out of scope`
  means the client excluded it. Exclude it from the sweep and from the
  aggregate report.
- **Rate-limit tests that lock you out.** Use a throwaway account and a
  modest N (30). Do not hammer a production auth endpoint.
- **Reporting a scanner's name as your finding.** "Nuclei found X" is not a
  finding. The finding is the vulnerability; the tool is how you found it.

---

## Files

- `scripts/fleet_scan.py` — multi-target scanner (stdlib + requests only).
- `references/techniques.md` — full reproduction payloads per class, with the
  exact request formats observed in a real engagement.
- `templates/report-skeleton.md` — grouped-root-cause report template.
