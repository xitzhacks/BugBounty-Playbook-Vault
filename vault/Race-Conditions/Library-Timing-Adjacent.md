# Library-Timing-Adjacent (Race-Conditions vault)

The money rows of this corpus's near-race pool. None of these is a request-parallelism race in the web sense — they are native-thread or side-channel races that the keyword classifier surfaced. Kept in this vault so the corpus stays honest; the bounty mix ($7,300 of the $43,260) is real.

## 1. libcurl `siglongjmp` race — RACE-1990421 (ibb, CVE-2023-28320, $480)

Synchronous-resolver builds time out slow resolves via `alarm()` + `siglongjmp()`. The longjmp target buffer is global and unfenced:

> When doing this, libcurl used a global buffer that was not mutex protected and a multi-threaded application might therefore crash or otherwise misbehave.

Impact as filed: `Denial of service due to a crash (likely) or possibly other impacts.`

Fix-class = per-thread buffers or a lock; report-class = library race, priced like a crash.

## 2. GitHub Security Lab timing-attack trio (metadata-only)

Three h1-brain rows whose entire body is `This bug was reported directly to GitHub Security Lab.` — title + bounty only, honestly labeled:

| Case | Title | Bounty |
|---|---|---|
| RACE-1301753 | Java: Timing attacks while comparing results of cryptographic operations | $4,500 |
| RACE-1943049 | [Python]: Timing attack | $1,800 |
| RACE-1496268 | [Java]: Timing attacks while comparing the headers value | $1,000 |

$7,300 — the second-largest money cluster in the corpus. Quoting stop: there is no body text to quote. Any module that builds timing methodology from these three rows is inventing; keep them as metadata anchors.

## 3. WooCommerce md5 oracle — RACE-239359 (automattic, bounty None)

`return_handler()` in `class-wc-gateway-simplify-commerce.php` compares the expected signature with `===`:

```php
$signature = strtoupper( md5( $_REQUEST['amount'] . $_REQUEST['reference'] . $_REQUEST['paymentId'] . $_REQUEST['paymentDate'] . $_REQUEST['paymentStatus'] . $this->private_key ) );
...
if ( $signature === $_REQUEST['signature'] ) {
```

> Here is used md5 for signature generation, but string comparison isn't safe towards timing attack. Having in mind the length of the md5 hash string 32 and minimal character set used for it `a-z` and `0-9`, then discovering the right signature will require 32 rounds * X requests per character => no need even for distributed attack regarding successful guessing the generated signature.

Proposed fix in the body: `hash_equals()` (PHP builtin / WP core):

`... if (hash_equals($signature, $_REQUEST['signature'])) ...`

Cross-class note: this is the timing oracle the Rate-Limiting vault prices for brute-force; mainline reporting here is the *payment-signature forgery* it enables, because the signature gates order completion.

## Boundary discipline (negative space of the race primitive)

- Non-constant-time compare with only a *latency* observable → timing/side-channel class.
- Same compare with a *success oracle* (order completes, token accepted) → this module's payment-gateway row.
- Multi-threaded native crash with no HTTP surface → library race; expect crash-tier pricing ($480 here).

## Cross-references

- `Misconfiguration/` (upcoming) — `hash_equals` absence is the canonical crypto-hygiene negative.
- `Rate-Limiting/` cross-cite pattern: user-enumeration via timing belongs there if the observable is binary.
