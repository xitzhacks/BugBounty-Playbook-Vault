# Heap Dump Binary Secret Extraction (Spring Boot actuatorlab & friends)

## Why `strings | grep` is not enough
A Java HPROF heap dump from a Spring Boot app leaks the `Environment` property
sources (DB passwords, AWS keys, the lab flag), but the property **name** and
**value** are stored as separate HPROF string records, separated by binary
delimiter bytes — NOT adjacent in any single `strings` line. Worse, the dump is
~90% JAR/internal class paths (`com/example/actuatorlab/...`,
`org/springframework/...`) that drown any `grep`.

## Repeatable workflow (proven on the actuatorlab heapdump)

1. **Confirm it's a heap dump.**
   `file heapdump` → "Java heap dump, version ...". If no extension, still check
   the first bytes for the `JAVA PROFILE` magic.

2. **Naive pass (fast, often enough for the obvious stuff).**
   `strings -n 6 heapdump > heapdump.strings.txt`
   `grep -iE 'password|secret|apikey|api_key|token|bearer|AKIA' heapdump.strings.txt`
   Look for lines where the value is NOT a Java symbol (no `/`, no `;`).

3. **Binary-level pass (when naive fails — this is the real technique).**
   The Spring `Environment` properties in the dump are delimited by raw `!`
   (0x21) bytes: `<property.name>!...<value>!`. A property NAME token ends with
   `!`, and its VALUE is the next printable run a few bytes later. Reconstruct
   name→value pairs by scanning the raw bytes, not `strings`.
   - AWS access key: grab raw bytes after `AKIA...` — the `...` in
     `AKIAQF...DHFI` is often a REDACTED PLACEHOLDER (non-printable dots), not a
     real key. The SECRET (`aws_secret_access_key=...`) is the genuinely leaked
     value. Don't assume the access key is valid just because it starts with AKIA.
   - Property values you want: `aws.secret.key`, `aws.access.key`,
     `management.endpoint.heapdump.path`, `spring.cloud.gateway.routes[...].uri`
     (look for `http://169.254.169.254` → SSRF-to-metadata route), `server.port`,
     `actuatorlab`.

4. **Distractor tokens.**
   Random-looking 20–40 char alnum strings (e.g. `GyMdkHmsSEDFwWahKzZYuXL`,
   `ojplmecpdpgccookcobabopnaifgidhf`) appear as method/class names or session
   IDs. They are NOT the flag. Verify before reporting. The cookie
   `ext_name=ojplmecpdpgccookcobabopnaifgidhf` in the actuatorlab dump is a
   decoy — it does not decode to anything meaningful.

5. **Where the actual flag is.**
   In actuatorlab-style labs the flag is a **property on the live
   `/actuator/env` (or `/actuator/configprops`) endpoint**, not a plaintext
   `flag{...}` string in the heapdump. The dump references
   `classpath:/application.properties` but the flag value is read live. If you
   downloaded the heapdump to find the flag and see no `flag{...}`, the intended
   path is to query the running app's `/env` — or use the SSRF route
   (`169.254.169.254`) the gateway routes expose.

## The SSRF chain the heapdump reveals
`spring.cloud.gateway.routes[...].uri = http://169.254.169.254` is the lab's
intended vulnerability: the gateway forwards requests to the cloud metadata
endpoint → grab `aws_secret_access_key` → that's the real credential. The heap
dump *contains* that secret too (see step 3), which is why the dump itself is
the "easy" path to the same prize.

## Gotchas that burned time this session
- HPROF struct parsing (id-size, STRING records) did NOT match this dump's
  layout — every homegrown parser returned 0 records. Don't trust a naive parser;
  go straight to raw-byte scanning + the `!`-delimiter heuristic.
- `strings` output was dominated by JAR paths; filter aggressively (drop lines
  with `/` or `;`).
- The access key `AKIAQF...DHFI` looked real but was a placeholder; the secret
  key was the real leak. Trust the secret, verify the access key.
- No `flag{...}` literal existed anywhere — the flag is live on `/env`.

## Ready-run extractor
`scripts/heapdump_secrets.py <heapdump> [--out findings.txt]` does steps 1–5:
raw AWS key/secret pull, `!`-delimited Spring property reconstruction, literal
flag search, and a low-confidence distractor-token dump.
