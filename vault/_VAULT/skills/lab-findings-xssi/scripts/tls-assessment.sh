#!/bin/bash
# TLS Security 12-Point Assessment Script
# Usage: ./tls-assessment.sh <target>
# Example: ./tls-assessment.sh example.com:443

set -e

TARGET=${1:-"localhost:8080"}
HOST=$(echo $TARGET | cut -d: -f1)
PORT=$(echo $TARGET | cut -d: -f2)

echo "=== TLS Security 12-Point Assessment ==="
echo "Target: $TARGET"
echo ""

# 1. Port and service detection
echo "[1] Port/Service Detection:"
if nc -z $HOST $PORT 2>/dev/null; then
    echo "    Port $PORT: OPEN"
else
    echo "    Port $PORT: CLOSED"
fi

# 2. Check if it's HTTP or HTTPS
echo ""
echo "[2] Protocol Detection:"
HTTP_RESPONSE=$(curl -s -m 5 http://$TARGET/ -o /dev/null -w "%{http_code}" 2>/dev/null || echo "000")
if [ "$HTTP_RESPONSE" != "000" ]; then
    echo "    Protocol: HTTP only"
    echo "    HTTP Response: $HTTP_RESPONSE"
else
    echo "    Protocol: HTTPS or filtered"
fi

# 3. TLS version support check (if HTTPS works)
echo ""
echo "[3] TLS Version Support (if HTTPS):"
if command -v sslscan &>/dev/null; then
    sslscan $TARGET 2>/dev/null | grep -E "SSLv2|SSLv3|TLSv1|TLSv1.2|TLSv1.3|disabled|enabled" || echo "    No TLS/Not HTTPS"
else
    echo "    sslscan not available"
fi

# 4. Certificate info (if HTTPS)
echo ""
echo "[4] Certificate Information:"
echo | timeout 5 openssl s_client -connect $TARGET -servername $HOST 2>/dev/null | \
    openssl x509 -noout -dates -subject -issuer 2>/dev/null || echo "    No certificate (not HTTPS)"

# 5. Cipher suites (if HTTPS)
echo ""
echo "[5] Cipher Suite Check:"
timeout 5 openssl s_client -connect $TARGET -cipher 'HIGH' 2>/dev/null | \
    grep -i "cipher\|success" || echo "    No cipher suites (not HTTPS)"

# 6. HSTS header check
echo ""
echo "[6] HSTS Header:"
curl -s -I http://$TARGET/ 2>/dev/null | grep -i "strict-transport-security" || echo "    Not applicable (HTTP only / no HSTS)"

# 7. Security headers check
echo ""
echo "[7] Security Headers:"
HEADERS=$(curl -s -I http://$TARGET/ 2>/dev/null)
for H in "Content-Security-Policy" "X-Frame-Options" "X-Content-Type-Options" "Referrer-Policy"; do
    if echo "$HEADERS" | grep -qi "$H"; then
        echo "    $H: Present"
    else
        echo "    $H: MISSING"
    fi
done

# 8. HTTP to HTTPS redirect
echo ""
echo "[8] HTTP to HTTPS Redirect:"
LOCATION=$(curl -s -I http://$TARGET/ 2>/dev/null | grep -i "location" | head -1)
if [ -n "$LOCATION" ]; then
    echo "    Redirect: $LOCATION"
else
    echo "    No redirect (also HTTP only)"
fi

# 9. API endpoint testing
echo ""
echo "[9] API Endpoints Found:"
ENDPOINTS=("login" "customer/register" "employee/add" "users" "products")
for ep in "${ENDPOINTS[@]}"; do
    STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X POST -H "Content-Type: application/json" \
        -d '{"test":1}' "http://$TARGET/api/v1/$ep" 2>/dev/null || echo "000")
    echo "    /api/v1/$ep: $STATUS"
done

echo ""
echo "=== Assessment Complete ==="