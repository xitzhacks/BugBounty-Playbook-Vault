# Grouped root-cause report template

Use this when a finding class affects **N hosts but has ONE root cause**.
Fill the placeholders. Delete the guidance lines before submitting.

---

## <Root cause title> — affecting <N> of <M> hosts

**Severity:** <Critical/High/Medium/Low/Info>
**Class:** <CWE-XXX: Name>
**Affected assets:** <N>
**Root cause:** <single sentence — the shared misconfiguration>

### Summary

<One paragraph. Name the shared component (load balancer / CDN / reverse
proxy / web server / TLS terminator) if you can establish it, and state the
single change that fixes all affected hosts. A triager reading this must
understand the scope from this paragraph alone.>

<If you could not prove the hosts share a front end, say so explicitly and
list the evidence that made you group them: identical `Server` header,
identical certificate issuer, identical `ETag`/`X-Generator` behaviour.
If you could NOT establish a shared root cause, split this into per-host
findings instead — do not over-claim.>

### Affected hosts

| Host | ID | Evidence | Status |
|---|---|---|---|
| `a.example.com` | FQ_0019 | `Server: nginx/1.18.0`, no `Strict-Transport-Security` | Open |
| `b.example.com` | FQ_0038 | `Server: nginx/1.18.0`, no `Strict-Transport-Security` | Open |

<Full list. Use a collapsible `<details>` block if the list is long.>

### Reproduction

<ONE reproducible request/response pair. Not one per host — the whole point is
that the request is identical apart from the hostname.>

```http
GET / HTTP/1.1
Host: a.example.com
```

```http
HTTP/1.1 200 OK
Server: nginx/1.18.0
<full response headers>
```

### Impact

<What an attacker actually gains. Be concrete and honest. If the realistic
impact is "low" because exploitation needs an on-path position, SAY THAT —
an honest Low beats an inflated High that gets rejected and burns the rest of
your submissions' credibility.>

<For a config-class finding, consider the chain: what does this combine with?
A missing HSTS on a login page + a valid session cookie = session hijack on
a shared network. Say that.>

### Remediation

<One fix, applied at the shared component. Give the config diff.>

```nginx
# /etc/nginx/conf.d/hardening.conf
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
```

<If the fix must be applied per-host, list the exact hosts and say so.>

### Scope notes

<Which hosts were excluded and why (out of scope, decommissioned, WAF
fronted). State it so the triager knows the sweep was deliberate.>

---

## Per-host finding template

Use this when the remediation genuinely IS per-host (e.g. a specific library
version on one app, a specific SSRF in one service).

---

## <Finding title> on <host>

**Severity:** <...>
**Class:** <CWE-XXX: Name>

### Summary

<One paragraph, specific to this host and this instance.>

### Affected assets

| Host | ID | Detail |
|---|---|---|
| `a.example.com` | FQ_0019 | <exact detail> |

### Reproduction

<Full request/response pair. Include every relevant header.>

```http
POST /csp_report HTTP/2
Host: a.example.com
Content-Type: application/csp-report

{"csp-report": { ... }}
```

```http
HTTP/2 200 OK
Content-Length: 0
```

### Proof of impact

<The part that makes it a finding rather than a scanner opinion.>

- **SSRF:** the OOB callback log line from your canary domain, showing the
  target server's outbound request.
- **Open redirect:** the `3xx` + `Location:` pointing at your domain, and
  confirmation the redirect was followed.
- **IDOR/forced browsing:** the actual protected content in the response body.
- **Dangerous method:** proof the method was acted on (file written/deleted).
- **Known vuln:** exact library + version + CVE, version read from the artifact.
- **Rate limit:** the request count, the absence of any `429`, and the fact the
  protected action still succeeded at the end.

### Impact

<...>

### Remediation

<...>

---

## Triage checklist before you submit

- [ ] Root cause is established, not assumed. If grouped, I compared the
      `Server` header and cert issuer across hosts.
- [ ] Severity matches the Chain Table in `hunt-bulk-fleet` — no inflation.
- [ ] Every claim has a captured artifact (screenshot, raw request/response,
      callback log). No "it should be possible to...".
- [ ] I did NOT claim a TLS decrypt I did not perform.
- [ ] For SSRF: I have the **OOB callback**, not just a `200`.
- [ ] For open redirect: I have a `3xx` with `Location` to **my** domain.
- [ ] For clickjacking: I have a screenshot of the target actually rendering
      inside my iframe.
- [ ] For IDOR: I have the **real data**, not a `200` on a login page.
- [ ] For known-vuln components: version read from the artifact, not the banner.
- [ ] Out-of-scope hosts are excluded from the list and mentioned in Scope notes.
- [ ] OOB/collaborator infrastructure is torn down.
- [ ] The program does not list this class as out of scope — I checked and can
      quote the scope line.
