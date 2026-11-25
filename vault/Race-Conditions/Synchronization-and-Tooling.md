# Synchronization & Tooling — evidenced techniques (Race-Conditions vault)

Every technique below was actually used in one of the 26 corpus cases. Quotes byte-true to `race_bodies.txt`.

## 1. curl `&` chains (oldest, zero-tooling)

RACE-429026 (H1 retest double-payment), Steps 2–3:

> 2. Intercept the request to retest the email. Right click the request in Burp Suite and select `Copy as curl command`.
> 3. Execute the request on the command line in the form `(request) & (request) & ...`. In testing, I executed the command 5 times.

RACE-1460373 (FetLife infinite invites) scripts the full chain of 10 in the body, with the framing:

> This is a chain of 10 curl commands in the form of `curl_command_1 & curl_command_2 & ... & curl_command_10`. It allows us to run 10 curl commands at the same time.

Practical notes for operators: put the last-sent request's noise (cookies, authenticity tokens) into every member; `&` starts all before any finishes — good enough when the server window is ≥ tens of ms.

## 2. Two-tab manual racing (for ≥1-second windows)

RACE-1717650 (Stripe promo code with redemption limit 1, redeemed twice) deliberately went tool-free:

> [In these steps i have used just a browser to show how easy this is to exploit and even a person with very limited knowledge on technology can exploit this. This can certainly be scaled using burp and other software .]

(sic: original spacing and bracket style; CACHE-style note kept outside the quote.)

> 4.Hit both link's pay/subscribe button as fast as you can.
> 5. Both payment will be successful using one coupon two times.

RACE-300305 (Shopify $15,250) measured the window and interleaved two tabs:

> 7. Now the tricky part. The "change email" takes anywhere from 1,100 - 2,500 ms to load so you need to take that into account. But let the request go through, wait for some milliseconds, then in another tab visit that email confirmation link from step 5.

## 3. Burp Intruder parallel + "Race The Web"

RACE-488985 (GraphQL `claimCredential`) fired 22 Intruder responses and parsed results: 21 × `was_successful:false`, 1 × `was_successful:true` with a fresh credential set — the classic claim-allowed-check race.

RACE-454949 describes the mid-2019 state of the art:

> 4. Then, you just have to submit the POST several times in a short time frame. I recommend a script with multi threads or "Race The Web" tool that I will mention below.

> With this tool we can send the requests faster than we could with Burp Intruder. Getting better results.

Tool link as in the body: `https://github.com/insp3ctre/race-the-web`.

## 4. Turbo Intruder gate (single connection, never misses byte alignment)

Full working script shipped inside RACE-1540969 (Hacker101 CTF group join, paid $500):

```python
# Find more example scripts at https://github.com/PortSwigger/turbo-intruder/blob/master/resources/examples/default.py
def queueRequests(target, wordlists):
    engine = RequestEngine(endpoint=target.endpoint,
                           concurrentConnections=100,
                           requestsPerConnection=100,
                           pipeline=True
                           )

    # the 'gate' argument blocks the final byte of each request until openGate is invoked
    for i in range(30):
        engine.queue(target.req, gate='race1')

    # wait until every 'race1' tagged request is ready
    # then send the final byte of each request
    # (this method is non-blocking, just like queue)
    engine.openGate('race1')

    engine.complete(timeout=60)

def handleResponse(req, interesting):
    table.add(req)
```

Comments in the script are the author's. The generic race.py example was also reused against Badoo in RACE-1037430:

> 4. Copy this script from this link https://raw.githubusercontent.com/PortSwigger/turbo-intruder/master/resources/examples/race.py and paste it in code section of turbo intruder and click attack and  after completion you'll see more than 1 sucessfull responses .

(The stock `race.py` example is referenced verbatim here, on top of the hand-written gate script in RACE-1540969.)

## 5. Filesystem synchronization primitives (server-side TOCTOU)

**`renameat2(RENAME_EXCHANGE)` atomic swap loop** — RACE-2078571 (curl CVE-2023-32001):

> Before we start, I will be using a little program called "rename". Which simply swaps atomically the names of two files to be able to showcase this race condition.

```c
int main(int argc, char *argv[]) {
  while (1) {
    syscall(SYS_renameat2, AT_FDCWD, argv[1], AT_FDCWD, argv[2], RENAME_EXCHANGE);
  }
  return 0;
}
```

(source credited in the body to the 35c3 logrotate challenge exploit by sroettger.)

**NTFS opportunistic locks on Windows** — RACE-768110 (NordVPN TOCTOU LPE):

> NTFS [opportunistic locks](https://docs.microsoft.com/en-us/windows/win32/fileio/opportunistic-locks) can be used to exploit this issue by detecting that a process is accessing a certain file. When this occurs, the file can be swapped for another file. The second read will thus return different content. The [BaitAndSwitch](https://github.com/googleprojectzero/symboliclink-testing-tools/releases) from [James Forshaw](https://twitter.com/tiraniddo) does exactly this and can be used to exploit this issue.

**Zero-TTL alternating DNS answers** — RACE-541169 (GitLab UrlBlocker SSRF):

> In order to perform this attack a DNS server must be configured to resolve a domain to alternating addresses with a low (or zero) Time To Live.

with `dig` evidence alternating `198.211.125.160` ↔ `127.0.0.1` at TTL 0; RACE-859962 (K8s CVE-2020-8562) repeats the pattern: `If the attacker sets the hostname to a custom DNS server, that is able return different values with zero TTL, it is possible to bypass that filter.` (sic: "that is able return").

## 6. Probabilistic disclosure etiquette

Two corpus reports pre-warm triagers for retries:

> 7) Please note that Race Condition is probabilistic vulnerability. It may be needed to do few attempts with PoC to reproduce it.

(RACE-55140)

> This may take several attempts due to the random nature of the `gitlabextssrf.webhooks.pw` DNS resolver, if it fails with a `500` error, try again until it is accepted.

(RACE-541169, web-hook creation)

State attempts and hit rate in every submission.
