---
title: "Unsafe Deserialization — PHP unserialize genome, POP at app level, Python pickle, Java ysoserial, Ruby Rails cookies, YAML"
type: playbook
category: unsafe-deserialization
cwe: "CWE-502"
source_count: 28
full_bodies_available: 27
corpus: "h1.security.nathan.sx roster (150 rows), bodies via hackerone.com/reports/<id>.json"
list_accessed: "2026-11-04"
note: "Anchors: RCE-134321 (Algolia Rails cookie RCE, $500 json), RCE-153026 (Starbucks ysoserial), RCE-98559 (ownCloud Jenkins), RCE-206227 (GitLab secret, $2,500 list). Claims trace to bodies read 2026-11-04."
---

# Unsafe Deserialization — trust nothing that unmarshals attacker bytes

## 1. Overview

Twenty-eight rows, **$28,075/25 paid**. The module splits by *who owns the deserializer*:
(a) the PHP engine's `unserialize()` genome — 18 rows reported through the PHP security
program, four figures ($500-$3,000) apiece, containing the single largest deser figure
(RCE-55033, $3,000 list); (b) app-level POP in plugins (WordPress's `unserialize()` calls,
$25/$50) ; (c) YAML's `!php/object` bridge ($500); (d) Python's pickle ($500/$500);
(e) Java (ysoserial-era Jenkins/JBoss rows — the famous infrastructure lane, unpaid here
but class-true); (f) Ruby's Rails CookieStore (the `$500` and `$2,500` cookie-signing
rows). The class boundary that decides money: **signing the bytes is not validating
them** — the Ruby rows prove reaching in with the key is the killer primitive.

**Case-stock (28 rows / $28,075):**

| Case | Target | Mechanism | Bounty |
|---|---|---|---|
| [RCE-55033](https://hackerone.com/reports/55033) | PHP (VDP) | unserialize() UAF | $3,000 (list) |
| [RCE-28445](https://hackerone.com/reports/28445) | PHP (VDP) | SPL ArrayObject unserialization type confusion | $2,500 (list) |
| [RCE-55029](https://hackerone.com/reports/55029) | PHP (VDP) | unserialize UAF DateTimeZone | $2,500 (list) |
| [RCE-55030](https://hackerone.com/reports/55030) | PHP (VDP) | SoapClient `__call` type confusion via unserialize | $2,500 (list) |
| [RCE-134321](https://hackerone.com/reports/134321) | Algolia | Rails secret leaked → signed Ruby-marshal cookie RCE | $500 (json) |
| [RCE-206227](https://hackerone.com/reports/206227) | imgur | GitLab static Rails secret → RCE | $2,500 (list) |
| [RCE-73235](https://hackerone.com/reports/73235) | PHP (VDP) | unserialize UAF via fake `__wakeup` | $1,500 (list) |
| [RCE-73244](https://hackerone.com/reports/73244) | PHP (VDP) | unserialize UAF DateInterval | $1,500 (list) |
| [RCE-104018](https://hackerone.com/reports/104018) | PHP (VDP) | multiple UAFs in unserialize | $1,500 (list) |
| [RCE-103995](https://hackerone.com/reports/103995) | PHP (VDP) | unserialize UAF SplDoublyLinkedList | $1,000 (list) |
| [RCE-103996](https://hackerone.com/reports/103996) | PHP (VDP) | unserialize UAF SplObjectStorage | $1,000 (list) |
| [RCE-103997](https://hackerone.com/reports/103997) | PHP (VDP) | unserialize UAF | $1,000 (list) |
| [RCE-104016](https://hackerone.com/reports/104016) | PHP (VDP) | dangling pointer unserializing ArrayObject | $1,000 (json) |
| [RCE-146233](https://hackerone.com/reports/146233) | PHP (VDP) | GC + unserialize UAF | $1,000 (list) |
| [RCE-146235](https://hackerone.com/reports/146235) | PHP (VDP) | ZipArchive GC + unserialize UAF | $1,000 (list) |
| [RCE-103998](https://hackerone.com/reports/103998) | PHP (VDP) | session deserializer UAF | $500 (list) |
| [RCE-103999](https://hackerone.com/reports/103999) | PHP (VDP) | unserialize UAF GMP | $500 (list) |
| [RCE-104012](https://hackerone.com/reports/104012) | PHP (VDP) | unserialize int overflow (32-bit) | $500 (json) |
| [RCE-195950](https://hackerone.com/reports/195950) | PHP (VDP) | unserialize uninitialized-memory → full RCE write | $500 (list) |
| [RCE-200909](https://hackerone.com/reports/200909) | PHP (VDP) | unserialize OOB read | $500 (json) |
| [RCE-73257](https://hackerone.com/reports/73257) | PHP (VDP) | yaml_parse `!php/object` → unserialize | $500 (json) |
| [RCE-73259](https://hackerone.com/reports/73259) | Python (VDP) | _pickle.c int overflow | $500 (json) |
| [RCE-103992](https://hackerone.com/reports/103992) | Python (VDP) | _Unpickler_Read int overflow | $500 (list) |
| [RCE-185907](https://hackerone.com/reports/185907) | WordPress (plugin) | unchecked unserialize usage | $25 (json) |
| [RCE-185909](https://hackerone.com/reports/185909) | WordPress (plugin) | unchecked unserialize in audit-trail | $50 (json) |
| [RCE-98559](https://hackerone.com/reports/98559) | ownCloud | Jenkins Java deser (CLI port) | - |
| [RCE-153026](https://hackerone.com/reports/153026) | Starbucks | JBoss JMXInvokerServlet ysoserial | - |
| [RCE-221294](https://hackerone.com/reports/221294) | Starbucks | JBoss deser (metadata-only) | - |

## 2. Ruby/Rails: sign then unmarshal — the killer primitive

RCE-134321 (Algolia, **$500 (json)**) is the composition none of the language rows shows
with this clarity: a leaked secret + CookieStore = arbitrary code

> Since the Rails app running at `facebooksearch.algolia.com` is using `CookieStore` as the
> session storage, this means an attacker knowing the session secret can craft any cookie
> that will then be accepted by the server.

> Cookie values are deserialized (unmarshalled) server-side. That combined with knowing the
> session secret creates the dangerous opportunity for an RCE. The attacker can sign a
> cookie that contains a Ruby object that evals arbitrary code when it is deserialized on
> the server side.

The delivery came from recon tooling, not fuzzing:

> I used [Gitrob](https://github.com/michenriksen/gitrob) to scan all of Algolia's public
> repositories (plus repositories from employees) and extract everything that is
> interesting. The `secret_token.rb` initializer immediately caught my attention since it
> usually contains the `secret_key_base`, which should never be public.

And the PoC is a Metasploit module (joernchen's `rails_secret_deserialization`) with a
one-line regex patch for cookie names containing `-`. RCE-206227 (team `imgur`; host
`Git.imgur-dev.com` — a GitLab-Enterprise deployment, **$2,500 (list)**) is the same lane: a static Rails secret shipping in
the product. Together they establish the lane's whole payout logic — **the secret is the
 killer primitive; the deserializer is the delivery**.

## 3. Java: ysoserial and the exposed-invoker lane

RCE-153026 (card.starbucks.in) is the era's canonical ysoserial write-up, quoted because
its *proof method* is the teaching: use error-differential as an oracle when the shell is
egress-filtered:

> Command to output serialized data to a file:
> $ java -jar ysoserial-0.0.4-all.jar CommonsCollections1 'cmd.exe' > serialdata

> You will notice I am searching for the string "cannot find" in the response tab. If a
> file is not found on the windows host it will return saying "The system cannot find the
> file specified" as well as another variation of that. Since the first request is for
> cmd.exe which IS found on the system this error is not present. This can also be
> verified by running telnet, ftp, calc.exe.

File-not-found vs found = a boolean over the target filesystem, no callback needed. The
row resolved unpaid; RCE-221294 (same host, same class, **metadata-only**) and RCE-98559
(ci.owncloud Jenkins) complete the lane. RCE-98559's mitigation section is the era's
exposed-Jenkins doctrine in the reporter's own words:

> **Mitigation**
> - Shut down ci.owncloud.com for the time being
> - Run ci.owncloud.com on a VPN instead of on a world-accessible public IP address
> - Firewall the Jenkins instance

## 4. PHP genome: the unserialize() monoculture

Eighteen rows — every UAF/type-confusion in the `php_var_unserialize()` family, reported via
the PHP security program (PHP program rows, with bugs.php.net links). Body-length varies from the full
Taoguang Chen texts (RCE-73235's fake-`__wakeup` zval) to single links (RCE-103995-104018).
The lane's shape: attacker bytes → engine acts on them → freed/allocated → integer overflow →
use-after-free → corruption. The **session deserializer** row (RCE-103998, $500 list) is
the lane's bridge to every web app: the session's `$ PHPC`-side serializer is the same
code path with attacker-controlled input — a server-side unserialization that nearly
every PHP deployment runs.

**YAML bridge** (RCE-73257, **$500 (json)**) — quoted because it's the taxonomy-completing
row: the safe-looking parser that secretly calls unserialize():

> Deserialization of built-in YAML types appears safe, as the serializer utilizes arrays
> and scalar types, prohibiting control of instantiation. However, this limitation can be
> overcome with the largely undocumented !php/object extension type, which in turn invokes
> unserialize(), effectively making the yaml_parse* functions just as dangerous.

> yaml_parse('x: !php/object O:1:"A":0:{}');

**Pickle** (RCE-73259/RCE-103992, $500 each) — Python's `_pickle.c` integer overflows.
Note the classification: memory-corruption bugs *inside* a deserializer stay in this
module (the deserializer is the attack surface); the module-04 memory lane is for VM/
parser/native-code corruption outside deserialization formats.

## 5. App-level POP: the plugin lane's tiny bounties

RCE-185907 (**$25 (json)**) quotes its own sink:

> $plugins = unserialize( $request['body']['plugins'] ); // todo use json now -- http://make.wordpress.org/core/2013/10/25/json-encoding-ssl-api-wordpress-3-7/

> without disallowing unneeded classes.
> thus, if attacker managed to control the value of $request['body']['plugins'] he will be
> able to: 1\. conduct PHP POP exploitation …

RCE-185909 (**$50 (json)**) is the same family in audit-trail-extension. The $25/$50
price tag is the honest record: untrusted `unserialize()` in a WordPress plugin is a
*pattern* finding in 2016-2017 — the corpus pays for the demonstrated chain, not the
sink. Modern hardening (P4): `allowed_classes: []` / PHP-blind POP scanners; the sink
itself pays almost nothing unchained (doctrine carried upstream by the playbook's
kill-gate 3).

## 6. What pays, what doesn't

- PHP engine genome = flat $500-$3,000 per bug, every single row paid (18/18 monetized:
  the single most *reliably* monetized sub-family of the corpus). Compare with module 01's
  $0 joke rows and module 08's informative rows — no deserialization row was unpaid
  without cause (the two unpaid ones are the Java metadata rows).
- Java rows ($0): the *exposed endpoint* lane at era-2015 — the cash went later, in the
  bundle era (module 06's $15,000 Jenkins row).
- The lane's ceiling is the reaching primitive: Ruby cookie rows picked $500/$2,500 for
  *signed-cookie* execution — the highest-trust deserialization input in the stack.

## 7. Cross-references

- RCE-178152 (module 07) delivers its RCE via marshalled cookies — the same class
  mechanics as 134321/206227, reached from a file-read chain.
- RCE-202774 (module 07) is the chain row: Type Juggling → PHP object injection → SQLi.
- The session deserializer (RCE-103998) pairs with `../Authentication-Session` session
  stores: the session is a serialized blob under attacker influence.
- Ruby YAML.load universal RCE is bibliography (blogs-index §2.2 third-party links;
  post-2017).
