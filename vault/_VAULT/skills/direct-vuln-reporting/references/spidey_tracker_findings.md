# Spidey Tracker (54.163.41.6) - Findings Reference

## API Endpoints Discovered

### Live Endpoints (GET)
- `/api/pulse` - Returns alerts, user data (no auth required)

### Auth Endpoints (POST)
- `/api/auth/login` - User login
- `/api/auth/signup` - User registration
- `/api/auth/recover` - Password recovery
- `/api/auth/reset` - Password reset
- `/api/auth/logout` - User logout

### User Endpoints (POST)
- `/api/me/checkin` - Daily checkin (requires auth)

## Discovered Vulnerabilities

### VULN-1: Information Disclosure via robots.txt
- **Location**: http://54.163.41.6/robots.txt
- **Disclosure**: 
  ```
  User-agent: *
  Disallow: /console
  Disallow: /circle
  Disallow: /inbox
  Disallow: /api/
  ```
- **Impact**: Attackers discover protected admin functionality
- **CWE**: CWE-538

### VULN-2: Insecure Password Recovery / Request Forgery
- **Location**: POST /api/auth/recover
- **Issue**: Accepts any handle value including SQL injection payloads
- **Evidence**: 
  ```json
  // All payloads return same response:
  {"relayed":true}
  POST {"handle":"admin' OR '1'='1"}
  POST {"handle":"' OR 1=1--"}
  POST {"handle":"admin"}
  ```
- **Impact**: User enumeration, potential password reset bypass
- **CWE**: CWE-204 (Observable Response Discrepancy)

### VULN-3: Unauthorized Admin Console Access
- **Location**: GET /console
- **Status**: 403 Forbidden
- **Message**: "CLEARANCE NOT RECOGNISED - This part of the tracker belongs to Ned."
- **Impact**: Confirms admin-only functionality, reveals username "Ned"
- **CWE**: CWE-284, CWE-200

### VULN-4: Unauthenticated API Data Exposure
- **Location**: GET /api/pulse
- **Data Exposed**:
  ```json
  {
    "alerts": [...],
    "me": null,
    "recent": 13,
    "sense": 83,
    "totals": {"hangs": 13, "pins": 91, "webheads": 13}
  }
  ```
- **Impact**: Reconnaissance, reveals application structure
- **CWE**: CWE-200

## Testing Notes

### Rate Limiting Observations
- Server returned timeout errors during enumeration
- Suggests rate limiting or backend throttling in place

### Authentication Model
- `/api/pulse` returns `me: null` for unauthenticated requests
- All user-specific endpoints require authentication
- No visible JWT/token in initial requests

## Next Steps (if authorized)
1. Register legitimate account and test checkin flow
2. Test recovery endpoint response differences for valid/invalid users
3. Attempt console access with admin credentials
4. Test password reset token validation