#!/bin/bash
# cf_curl.sh — GET a Cloudflare-fronted URL with a coherent browser header set.
#
# Why: default curl gets HTTP 403 "Just a moment..." / cf-mitigated: challenge on many
# CF-fronted targets. That is a client-fingerprint challenge, NOT a dead host and not
# necessarily a target-side block. With the headers below the same URL returns the real page.
#
# Usage:
#   ./cf_curl.sh https://target.com/en
#   ./cf_curl.sh https://target.com/ -D -            # dump response headers
#   ./cf_curl.sh https://target.com/api -H 'Accept: application/json'
#
# Install into the engagement dir as ./rq.sh and route every probe through it.
UA='Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0'
exec curl -sk -m 25 --compressed \
  -H "User-Agent: $UA" \
  -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8' \
  -H 'Accept-Language: en-US,en;q=0.5' \
  -H 'Sec-Fetch-Dest: document' \
  -H 'Sec-Fetch-Mode: navigate' \
  -H 'Sec-Fetch-Site: none' \
  -H 'Sec-Fetch-User: ?1' \
  -H 'Upgrade-Insecure-Requests: 1' \
  "$@"
