# CORS Misconfiguration Findings (2026-10, SignalStack)

## Case Study: app.signalstack.com/api/providers

**Finding**: `Access-Control-Allow-Origin: *` on unauthenticated endpoint with sensitive data.

**Headers**:
```
HTTP/2 200
Access-Control-Allow-Origin: *
(no Vary: Origin header)
(no Access-Control-Allow-Credentials)
Content-Type: application/json; charset=utf-8
```

**Analysis**:
- ACAO: * on an unauthenticated endpoint serving sensitive data (42 broker configs)
- No ACAC header → browser won't send credentials, but the data is readable from any origin
- No Vary: Origin → cached responses don't distinguish origins, potential cache side-channel
- Per hunt-cors validation rules: ACAO:* + no creds = Informational/Low (unless data is sensitive unauthenticated)

**Severity decision**: This is a **Low** finding. The data (provider configs) is already publicly accessible without auth, and without ACAC:true there's no credentialed cross-origin read. However, the missing `Vary: Origin` header is worth noting as a cache poisoning consideration — a response cached with ACAO:* could be served to a credentialed request on an allowed origin.

**What to report**: The missing `Vary: Origin` header combined with the unauthenticated data exposure is a minor finding. The main value is the info disclosure of provider configs (see hunt-api-misconfig).

## Testing pattern for CORS on API endpoints

Always test CORS headers on ALL API endpoints, not just the ones you expect to have them:
- Some endpoints reflect origins, others use wildcard, others omit headers entirely
- `/api/providers` had ACAO:*, `/api/connectors` had no CORS headers
- Endpoints that return 401 (auth required) may still have CORS headers — test before and after auth