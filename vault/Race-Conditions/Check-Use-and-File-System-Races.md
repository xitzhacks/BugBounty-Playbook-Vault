# Check-Use & File-System Races (Race-Conditions vault)

Pattern: the server validates a resource, then fetches/uses it again — DNS names, Content-Type heads, config files, paths. The attacker swaps what the second operation sees. This module's cases end in SSRF, RCE and SYSTEM; the race is the guard-evasion primitive, not the destination.

## 1. DNS TOCTOU → full SSRF — RACE-541169 (GitLab `UrlBlocker`, bounty None)

`GitLab::UrlBlocker` resolves and blocklists IPs; `GitLab::HTTP` then re-resolves the same hostname to connect. Alternating DNS defeats the check:

> The `GitLab::UrlBlocker` IP address validation methods suffer from a Time of Check to Time of Use (ToCToU) vulnerability. The vulnerability occurs due to multiple DNS resolution requests performed before and after the checks.

> In order to perform this attack a DNS server must be configured to resolve a domain to alternating addresses with a low (or zero) Time To Live.

dig evidence in the body alternates `198.211.125.160` ↔ `127.0.0.1` at TTL 0. Weaponized through the Web Hook integration against `http://169.254.169.254/metadata/v1.json` (DigitalOcean metadata):

> This may take several attempts due to the random nature of the `gitlabextssrf.webhooks.pw` DNS resolver, if it fails with a `500` error, try again until it is accepted.

Correct behavior stated by the reporter: validate once and pin the connection:

> The validated resolved addresses should be returned by `GitLab::UrlBlocker` and used by `GitLab::HTTP` to make the TCP connection to the destination host.

## 2. Same pattern, K8s apiserver proxy filter — RACE-859962 (kubernetes, CVE-2020-8562)

> TL,DR: Time-of-check (apiserver proxy filter) Time-of-use (apiserver proxy request) Race Condition.

> When the apiserver is proxying a request to a node though one of its addresses, it performs a filter validation. If the address type is a DNS record (Hostname, ExternalDNS, InternalDNS), the apiserver performs two DNS queries, one for filter validation, another for proxying the request. If the attacker sets the hostname to a custom DNS server, that is able return different values with zero TTL, it is possible to bypass that filter.

Setup: delegate a subdomain NS to an attacker DNS server that answers consecutive queries differently; then `curl localhost:8001/api/v1/nodes/toctou:80/proxy/` through `kubectl proxy`. Impact: cloud metadata / localhost access via the proxy path.

## 3. HEAD-check / GET-use → RXSS filter bypass — RACE-2106708 (security, bounty None)

The fix for #2035332 validated `Content-Type` by issuing a HEAD request; the payload fetch used GET. Answer differently per method:

> After the bug patch, the server now validates the `Content-Type` of the requested resource. The check is done by making a `HEAD` based request to the resource to get the `Content-Type` then if it corresponds to a valid image mime type a second request is made this time `GET` based to retrieve the page resource content.

> TOCTOU ( time-of-check to time-of-use) : At the time of check the application relies upon HEAD request but at the time of use relies upon GET request this allows the attacker to bypass the protection.

Bypass is not a race in wall-clock time but a *semantic* one — two requests, two interpretations. The report also records an `Accept`-header sniffing quirk (Safari vs `*/*`) that mattered for delivery.

## 4. Config-swap TOCTOU → SYSTEM LPE — RACE-768110 (NordVPN Windows, bounty None)

NordVPN service validates an OpenVPN config file, then launches OpenVPN on the same path. Attacker-controlled `ServerDomain` makes the path attacker-writable; NTFS oplocks + `renameat2`-class swapping replaces the validated file with one containing `engine`/`DLL` entries:

> A time-of-check-time-of-use (TOCTOU) race condition exists in the way OpenVPN configuration files are validated/used. First the NordVPN service will validate the OpenVPN configuration that is located at the path that is constructed using the `ServerDomain` parameter. If the configuration file is valid, OpenVPN is launched with the same path. In the time between the validation and launching, the configuration file can be swapped for another one, and OpenVPN will used that file instead of the one that was validated by the NordVPN service.

> NTFS [opportunistic locks](https://docs.microsoft.com/en-us/windows/win32/fileio/opportunistic-locks) can be used to exploit this issue by detecting that a process is accessing a certain file. When this occurs, the file can be swapped for another file. The second read will thus return different content. The [BaitAndSwitch](https://github.com/googleprojectzero/symboliclink-testing-tools/releases) from [James Forshaw](https://twitter.com/tiraniddo) does exactly this and can be used to exploit this issue.

Fix direction from the body: copy the config into a SYSTEM-only directory, random name, validate *after* the copy, launch from there.

## 5. curl `stat`→`fopen` race — RACE-2078571 (ibb, CVE-2023-32001, $2,480)

`Curl_fopen` stats the path (following symlinks), and if it is not a regular file falls back to direct `fopen`. Between stat and fopen, an atomic `renameat2(RENAME_EXCHANGE)` swap flips a directory ↔ symlink, so the victim's cookie jar/HSTS write lands in an attacker-controlled file:

> There is a race condition between the moment "stat(filename, &sb)" is executed and the moment " fopen(filename, FOPEN_WRITETEXT);" is executed.

> This leads to undesirable behavior such as an attacker tricking a privileged user to overwrite protected files, or since this function (Curl_fopen) is also used for storing cookies an attacker could trick another user to send those cookies that might be very sensible to a file fully owned and controlled by the attacker.

The atomic-swap tool is in Synchronization-and-Tooling.md §5. Note the honest boundary the reporter draws:

> An attacker is able to overwrite files they shouldn't have access to, however the attacker does not control the data sent to those files.

## 6. Tomcat write-servlet race → RCE — RACE-2905013 (ibb, CVE-2024-50379, bounty None)

Two-line body, whole story:

> Code injection triggered by a race condition on a Windows machine.

## Impact

> Code injection

Windows case-insensitivity + write-enabled default servlet: the uploaded JSP's validation and its execution race on case variants. Cross-file to `RCE/` for the delivery class.

## 7. Traversal + Gitaly race → arbitrary file read — RACE-822262 (gitlab, CVE-2020-12448, $12,000)

Not a pure race — a path traversal (their class) whose *delivery* is a repository race (ours):

> There's a path traversal issue in Nuget package registry which was released to GitLab-EE recently. The issue allows an attacker to create any file with an extension “.nupkg” in the filesystem. By combining the bug with a race condition in Gitaly which I used several times before (#762421, #732330). It could finally be used to read sensitive files in a GitLab instance.

NuGet metadata (`id`/`version` XML elements) is concatenated into `package_filename`, so a `version` of `../../../../../nyangawa` writes a `.nupkg` anywhere the service can write. The Gitaly race then converts that planted file into a read primitive — `.gitlab_shell_secret` confirmed via `exp.rb`.

Chain doctrine: position your race as one link in a longer chain, and name the prior links (#762421, #732330) so the triager sees the lineage.

## Cross-references

- `SSRF/` — RACE-541169 and RACE-859962 are DNS-TOCTOU *SSRF* reports; sync primitive here, destination there.
- `RCE/` — RACE-2905013 (CVE-2024-50379) and RACE-768110's SYSTEM-LPE sibling land there.
- `XSS/` — RACE-2106708 re-opens a patched RXSS; a guard-bypass exemplar.
- `File-Upload/` — RACE-822262's traversal half.
