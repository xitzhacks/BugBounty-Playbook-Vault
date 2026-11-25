# TLS Security 12-Point Assessment - 10.13.101.122:8080

## Assessment Date: 2026-09-03

## Tools Used
- `sslscan` - TLS/SSL service and cipher discovery
- `nmap` - Port and service scanning  
- `openssl s_client` - Manual TLS handshake testing
- `nc` (netcat) - Port connectivity testing
- `curl` - HTTP/HTTPS endpoint testing

## Scan Results

### Port Scan
```
PORT     STATE SERVICE
8080/tcp open  http-proxy
443/tcp  closed https
8443/tcp closed https-alt
80/tcp   closed http
```

### SSL/TLS Scan (sslscan)
```
SSLv2     disabled
SSLv3     disabled  
TLSv1.0   disabled
TLSv1.1   disabled
TLSv1.2   disabled
TLSv1.3   disabled
```
*All show "disabled" because no TLS is configured*

### OpenSSL Connection Test
```
error:0A00010B:SSL routines:tls_validate_record_header:wrong version number
```
Server accepts plaintext HTTP on 8080, not HTTPS

## API Endpoints Discovered

| Endpoint | Method | Issue |
|----------|--------|-------|
| `/api/v1/login` | POST | Credentials sent in plaintext |
| `/api/v1/customer/register` | POST | PII sent in plaintext |
| `/api/v1/employee/add` | POST | XSSI - internal ID leakage |

## Missing Security Controls

### HTTP Security Headers
- No `Strict-Transport-Security` (HSTS) - No HTTPS exists
- No `Cross-Origin-Resource-Policy`
- No `Cross-Origin-Embedder-Policy`
- No `Cross-Origin-Opener-Policy`

### Certificate Protection
- No TLS = No certificate validation
- No OCSP stapling possible
- No ECH (Encrypted Client Hello) possible

## Critical Findings Summary

1. **Zero TLS configuration** - Server is HTTP-only
2. **Plaintext credential transmission** - Login API leaks passwords
3. **XSSI vulnerability** - Employee IDs leaked via JSON response
4. **Missing HTTP→HTTPS redirect** - Not applicable (no HTTPS)

## Remediation Priority

1. **IMMEDIATE:** Enable HTTPS on port 8443 or 443
2. **IMMEDIATE:** Configure TLS 1.2+ with strong ciphers
3. **HIGH:** Obtain valid certificate from trusted CA
4. **HIGH:** Add HSTS and security headers
5. **MEDIUM:** Add CORP/COOP/COEP protection to JSON responses
6. **MEDIUM:** Implement proper CSRF protection