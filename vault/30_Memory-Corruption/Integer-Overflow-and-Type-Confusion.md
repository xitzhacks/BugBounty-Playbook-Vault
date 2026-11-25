---
title: "Memory-corruption vault module — integer overflow & type confusion (22 full-body + 11 link-only rows)"
type: playbook
category: memory-corruption
cwe: "CWE-190"
source_count: 33
full_bodies_available: "22/33"
corpus: "h1-brain disclosed_reports.db (sha256 8bf566e78446c73d9bbc57ef47ad88d645ef1ff4354727cca43b00769c41ccd4) — 352-row vault; 336-row memory-corruption bucket"
list_accessed: "2026-11-07"
note: "MEM module 4/6. Anchors: MEM-175091 (Python itertools chain.__setstate__ type confusion, $1,000), MEM-141212 (fread/gzread integer underflow → arbitrary null write, $500), the 51-byte PHP string-function overflow batch ($500 × 11 — the vault's thinnest bodies). 19/33 rows carry bounty figures; module floor $10,100 — the vault's lowest-money module."
---

# Integer Overflow & Type Confusion

## 1. Overview

Thirty-three rows, 19 paid, **$10,100** — the vault's lowest-money module and its thinnest evidence. Two veins: (a) *integer overflows* in PHP's string-argument functions, each reported as a one-line bugs.php.net link at $500 flat, and (b) *type confusions* where a `__setstate__`/deserialization path stores an attacker object where an iterator belonged. Doctrine: overflow-to-allocation-size is the class; the report form is (size_t vs int) narrowing proven by a gdb length print or a single upstream ticket link. The module is the playbook's P2 root-cause module: every overflow here feeds a buffer whose size was computed from the wrapped integer.

**Case-stock (33 rows / $10,100):**

| Case | Target | Mechanism | Bounty |
|---|---|---|---|
| [MEM-127242](https://hackerone.com/reports/127242) | ibb | Negative size parameter (-1) in memcpy mbfl_strcut | $1,000 |
| [MEM-175091](https://hackerone.com/reports/175091) | ibb | chain.__setstate__ Type Confusion | $1,000 |
| [MEM-135293](https://hackerone.com/reports/135293) | ibb | bcpowmod accepts negative scale and corrupts _one_ definition | $500 |
| [MEM-141212](https://hackerone.com/reports/141212) | ibb | Integer underflow / arbitrary null write in fread/gzread | $500 |
| [MEM-143234](https://hackerone.com/reports/143234) | ibb | Integer Overflow in _gd2GetHeader() resulting in heap overflow | $500 |
| [MEM-159953](https://hackerone.com/reports/159953) | ibb | integer overflow in curl_escape caused heap corruption | $500 |
| [MEM-159954](https://hackerone.com/reports/159954) | ibb | integer overflow in base64_decode caused heap corruption | $500 |
| [MEM-159955](https://hackerone.com/reports/159955) | ibb | integer overflow in bzdecompress caused heap corruption | $500 |
| [MEM-161200](https://hackerone.com/reports/161200) | ibb | wddx_deserialize allows illegal memory access | $500 |
| [MEM-167903](https://hackerone.com/reports/167903) | ibb | integer overflow in str_pad caused heap corruption | $500 |
| [MEM-167905](https://hackerone.com/reports/167905) | ibb | integer overflow in pg_escape_bytea caused heap corruption | $500 |
| [MEM-167906](https://hackerone.com/reports/167906) | ibb | integer overflow in imap_binary caused heap corruption | $500 |
| [MEM-167907](https://hackerone.com/reports/167907) | ibb | integer overflow in preg_quote caused heap corruption | $500 |
| [MEM-167908](https://hackerone.com/reports/167908) | ibb | integer overflow in fgets cause heap corruption | $500 |
| [MEM-167911](https://hackerone.com/reports/167911) | ibb | integer overflow in fgetcsv caused heap corruption | $500 |
| [MEM-175311](https://hackerone.com/reports/175311) | ibb | memcpy negative size parameter in php_resolve_path | $500 |
| [MEM-175312](https://hackerone.com/reports/175312) | ibb | memcpy negative parameter _bc_new_num_ex | $500 |
| [MEM-178094](https://hackerone.com/reports/178094) | ibb | php_snmp_parse_oid integer overflow in memory allocation | $500 |
| [MEM-192235](https://hackerone.com/reports/192235) | shopify-scripts | Integer Overflow in mrb_ary_set | $100 |
| [MEM-113122](https://hackerone.com/reports/113122) | ibb | An integer overflow bug in php_str_to_str_ex() led arbitrary code execution. | - |
| [MEM-113268](https://hackerone.com/reports/113268) | ibb | Integer overflow in wordwrap | - |
| [MEM-146360](https://hackerone.com/reports/146360) | ibb | Heap Overflow Due To Integer Overflow | - |
| [MEM-167921](https://hackerone.com/reports/167921) | ibb | integer overflow in xml_utf8_encode | - |
| [MEM-167931](https://hackerone.com/reports/167931) | ibb | Memory Corruption in During Deserialized-object Destruction | - |
| [MEM-167977](https://hackerone.com/reports/167977) | ibb | Missing type check when unserializing SplArray | - |
| [MEM-170619](https://hackerone.com/reports/170619) | ibb | PHP Integer Overflow in gdImageWebpCtx | - |
| [MEM-172411](https://hackerone.com/reports/172411) | ibb | Heap overflow caused by type confusion vulnerability in merge_param() | - |
| [MEM-180563](https://hackerone.com/reports/180563) | ibb | Heap overflow due to integer overflow in bzdecompress() function | - |
| [MEM-180582](https://hackerone.com/reports/180582) | ibb | Heap overflow due to integer overflow in php_escape_html_entities_ex() function | - |
| [MEM-180584](https://hackerone.com/reports/180584) | ibb | Heap overflow due to integer overflow in pg_escape_string() function | - |
| [MEM-181073](https://hackerone.com/reports/181073) | ibb | malloc negative size parameter | - |
| [MEM-212241](https://hackerone.com/reports/212241) | ruby | sprintf combined format string attack | - |
| [MEM-271330](https://hackerone.com/reports/271330) | ibb | Format string implementation vulnerability, resulting in code execution | - |

## 2. The gzip no-buffer case: fread/gzread underflow (MEM-141212, $500)

The module's best full-body row — an integer underflow that becomes an *arbitrary null-byte write*, proven with a gdb length dump:

> Integer underflow in the  fread/gzread length parameter allows to write an arbitrary null byte on 64 bit platforms. This was identified with the help of ASAN and a custom fuzzer.

The mechanism, documented to the sign bit: the length wraps to a negative `len`, and the null-termination store lands at `Z_STRVAL_P(return_value)[Z_STRLEN_P(return_value)]` with the printed value `$1 = -2147483648`. This is the report form to copy for every size_t-vs-int bug in the corpus: **show the sign of the wrapped length in the debugger**, not just the crash. The write is limited to a null byte — the price ($500) reflects exactly that honesty.

## 3. Type confusion proper: itertools chain.__setstate__ (MEM-175091, $1,000)

Python's `chain.__setstate__` parses the state tuple and stores `source`/`active` without validating iterator-ness:

> Python 3.5.2 suffers from a type confusion vulnerability in the chain.__setstate__ method of the itertools module. The issue exists due to lack of argument validation in the chain_setstate() function:

> After parsing the argument tuple, source and active are set without validating that they are iterator objects.

The confused object is then passed to `PyIter_Next` where the type check should have been. This is the module's only modern interpreter-vuln row priced above the PHP flat, and it names the exact missing check. Its kingdom: pickle/deserialization-driven state restoration (the same tools that populate these `__setstate__` paths are the RCE vault's module 03).

## 4. The 51-byte batch: PHP string-function overflows

Eleven rows whose whole body is one upstream ticket link:

> Please check: https://bugs.php.net/bug.php?id=72807

Pattern across the batch (159953 `curl_escape`, 159954 `base64_decode`, 159955 `bzdecompress`, 167903 `str_pad`, 167905 `pg_escape_bytea`, 167906 `imap_binary`, 167907 `preg_quote`, 167908 `fgets`, 167911 `fgetcsv`, …): each title names the function; each body names the ticket; each figure is **$500**. The corpus's clearest statement that a *class sweep* (same primitive, many fixed functions) was itself the deliverable: one report per function, all resolving. MEM-127242 (**$1,000**) is the same genre at the class ceiling — the mbfl_strcut negative-size `memcpy` — with the report-to-fix dates in the body:

> Memory corruption issue on mbstring extension, issue reported to PHP developers on 2016-03-26,  fixed 2016-03-29 and released at 2016-03-31, affected PHP 5.5 , PHP 5.6 and PHP 7.

(sic — double space after the comma.) Note the fixed-in-weeks discipline: upstream fix, then H1 wrapper, then payout.

## 5. Underflow → heap overflow (_gd2GetHeader, MEM-143234, $500)

The GD member of the class, with the gdb proof format §2 requires:

> The _gd2GetHeader() is prone to an integer overflow, which result in heap based overflow.

(sic — "which result".) The body is the breakpoint transcript at `gd_gd2.c:139` during `imagecreatefromgd2("poc.gd")` — the poc-gd / poc-php file pair as the minimized repro. The unpaid sibling MEM-170619 (`PHP Integer Overflow in gdImageWebpCtx`, `-`) and MEM-180563/180582/180584 (`-`) show what the same primitive earned without the upstream ticket linkage: the corpus pays the *upstream-verified* overflow, not the raw title claim.

## 6. What pays / what doesn't

- **Pays**: the null-write underflow ($500, single byte, honestly bounded); the mbstring negative-size ($1,000); the type confusion ($1,000); the 51-byte batch ($500 × 11 + remnant checks at $500); GD underflow ($500); mruby `mrb_ary_set` ($100 — sandbox's cheapest tier).
- **Doesn't pay**: MEM-113122's `php_str_to_str_ex` overflow (claims arbitrary code execution in the title — the corpus's loudest unpaid claim; bounty's silence is the verdict); MEM-271330's format-string RCE (full claim, no figure); the `merge_param` type confusion (MEM-172411, `-`). Pattern: the more the title promises, the less the corpus paid — no row in this module carried an exploit beyond a crash or a byte-write.
- **Link-only rows (11)** are quoted by title only; no sentence exists to quote — hand-label them in any downstream use.

## 7. Cross-references

- **Heap module** — every overflow here *is* a heap allocation-size bug; the module split is cause (integer) vs effect (heap). The playbook sweeps them together (P2 §integer probe).
- **Out-of-Bounds module** — MEM-593229 (iconv overflow→OOB) is the bridge; this module's §5 GD row feeds the same image parsers.
- **RCE vault module 03** — the `__setstate__` type-confusion lane (175091) is deserialization's memory-corruption cousin.
- **Adjacent pool** — MEM-140865 (`Integer Overflow in php_html_entities()`, `-`, from the unclassified merges) is the same primitive one classifier sweep later; its body gives the cleanest statement of the (size_t → signed int) narrowing in the vault.
