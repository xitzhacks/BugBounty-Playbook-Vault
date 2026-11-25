---
title: "File inclusion — dispatcher LFI, fix-bypass, parser-included paths, XXE-in-upload"
type: playbook
category: file-inclusion-lfi-rfi
cwe: "CWE-98 · CWE-611"
source_count: 7
full_bodies_available: 7
corpus: "h1.security.nathan.sx roster (86 title-arm rows), bodies via hackerone.com/reports/<id>.json"
list_accessed: "2026-11-05"
note: "Anchor bodies: FU-59665 + FU-147570 (concrete5 pair), FU-39428 (Phabricator LFI→RCE, $500 json), FU-179034 (Airship RST), FU-232614 (Weblate XLF). Claims trace to bodies read 2026-11-05."
---

# Module 04 — inclusion: the include() argument you don't own

## 1. Overview

Seven rows, **$500/1 paid** (39428's Phabricator $500 (json) is the only priced row) — the
rawest classification line in the vault, and the reason is simple: pure-LFI rows in this
era's private-programs corpus mostly resolved unpaid or died at 404 (see the dead-list:
1675 Yahoo `$1,390`, 12388 InVision, 6674 Yahoo `$3,000`). What the live corpus gives is
instead the class's *mechanism catalog*, in clean isolation: a dispatcher-override LFI
(59665), the craft of *fix-review bypass* (147570), include-to-RCE via attacker-writable
paths (39428), a parser feature-space LFI (179034), and the upload-delivery XML variant the
XXE vault shares (232614, 105787).

**Case-stock (7 rows / $500):**

| Case | Target | Mechanism | Bounty |
|---|---|---|---|
| [FU-39428](https://hackerone.com/reports/39428) | Phabricator | Phame `skin=` traversal → attacker-writable `/tmp/test/` php include | $500 (json) |
| [FU-59665](https://hackerone.com/reports/59665) | concrete5 | `Request::getPathInfo()` header-driven dispatcher LFI | - (list) |
| [FU-147570](https://hackerone.com/reports/147570) | concrete5 | fix-bypass of 59665's `strpos()` patch (mixed separators) | - (list) |
| [FU-179034](https://hackerone.com/reports/179034) | Paragon Initiative Enterprises | Gregwar RST `.. include::` directive | - (list) |
| [FU-232614](https://hackerone.com/reports/232614) | Weblate | uploaded XLF external entities → `/etc/passwd` | - (list) |
| FU-105787 | Informatica | XXE in a file-upload feature (summary record) | - (list) |
| [FU-14092](https://hackerone.com/reports/14092) | Slack | the false-positive exhibit (see §4) | - (list) |

## 2. Anatomy

### 2.1 The dispatcher override (59665)

**FU-59665** writes the mechanism in one paragraph, byte-true:

> Concrete5 is vulnerable to a Local File Inclusion because it fails to properly validate
> the path for incoming requests during the dispatching process. This vulnerability exists
> because the path is retrieved using the Request::getPathInfo() method from the Symfony
> framework, which allows to specify the path for the request within some HTTP headers
> (like X-Original-URL and some others). However, this cannot be considered a vulnerability
> within the Symfony framework, but a vulnerability due to the way Concrete5 dispatches the
> request using that feature.

The class discipline in that closing sentence — blame the *consumer* of the header, not the
header — is the same rule the Host-header vault complains about. Path-override headers
arrive at dispatcher; dispatcher includes; module 04 files it because the include is the
sink.

### 2.2 Fix-review as a hunting lane (147570)

**FU-147570** is a second report submitted *against the patch of the first*. The body
re-derives the patched guard:

```php
$path = $request->getPathInfo();
$path = rawurldecode($request->getPathInfo());
 if (substr($path, 0, 3) == '../' || substr($path, -3) == '/..' || strpos($path, '/../') ||
     substr($path, 0, 3) == '..\\' || substr($path, -3) == '\\..' || strpos($path, '\\..\\')) {
```

and states the miss byte-true: "you forgot about ("../\", " ..\/", "/\.." & "\/..")
this works because some oses (unix like) parse the backslash to forward slash and
proceed. add those and I think you should be fine. :)"
The lane lesson: when a fix ships committed `strpos()` string lists, replay the exact guard
against every OS separator permutation before trusting it.

### 2.3 The include that becomes RCE (39428)

**FU-39428** — Phabricator's Phame blog skins. The POST body carries the traversal:

```
skin=%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%74%6d%70%2f%74%65%73%74
```

making Phabricator load skin templates from
`/var/www/phabricator/phabricator/externals/skins/../../../../../../../../../../tmp/test/` —
and the body's landing condition, byte-true: "In order to exploit the vulnerability a valid
skin structure must exist at the specified location, I have simply copied the oblivious
skin and modified it to output a phpinfo() within the header.php script with the expected
results." ("oblivious" sic.) The pre-condition ladder the body opens with — cohosted
uploading apps, ssh write-into-`/tmp` — is what makes an LFI report *to the program* the
rare full-RCE row: $500 (json).

### 2.4 Parser feature-space (179034)

**FU-179034** (high, unpaid) — Airship's Gregwar RST parser ships `include` built in, with
the body quoting the spec's own security note. Proof-of-concept from the body:

```php
$document = '*Test*

.. include:: /./../../../../../../../../../../../../../../../../../../etc/hosts

``test``
';

// Parse it
$html = $parser->parse($document);
```

### 2.5 The upload-delivery XML variant (232614, 105787)

**FU-232614** (Weblate, high) — Translate-group members upload `.XLF`; the XLIFF standard
is XML, so external entities ride the upload. The body's payload block, byte-true:

```
<!DOCTYPE foo [ <!ELEMENT foo ANY >
<!ENTITY xxe SYSTEM "file:///etc/passwd" >]>
```

with the result read back "as a translation" through the UI — and the body's honest
mitigation note ("because your web server is python based it is not vulnerable to the
trivial RCE that PHP servers are commonly vulnerable to"). **FU-105787** is its one-sentence
Informatica twin (summary record, 71 B): "The attacker was able to execute XXE in one of
the file upload feature." Both rows are cross-registered in the XXE vault
(XXE-232614 full-body; XXE-105787 metadata-only) — the XXE-class ledger line lives there;
this vault records the upload-delivery angle.

## 3. Techniques (corpus-derived)

1. **Header-read dispatchers**: audit every `Request::getPathInfo()`-style consumer; the
   override set is bigger than X-Original-URL (59665).
2. **Trusted parse features**: template/directive engines import `include` variants that
   their embedders forget ship file-read semantics (179034, 232614).
3. **Fix-diff replay**: every committed string-list guard gets a separator-permutation
   replay (147570).
4. **Include-to-RCE requires a writable landing**: enumerate co-hosted upload directories
   and `/tmp`, then make the file *parse* in the expected structure (39428).

## 4. Kill-gates + the FP exhibit

- 39428's landing quote is the gate template: a valid in-structure file must be *shown*
  executing. `phpinfo()` output inside the header was the proof.
- **FU-14092 is the module's false-positive exhibit**, preserved on purpose (informative):
  the title says RFI, the body walks Slack's `Change photo` page to
  `https://pran3hiva.slack.com/account/photo?url=https%3A%2F%2Fs3-us-west-2.amazonaws.com%2Fslack-files2%2Favatar-temp%2F2014-05-30%2F2364428212.jpg`
  (via `.../account/photo`), changes that `url` parameter, and announces RFI because a
  remote image loads into an `<img>`. Byte-true: "Everysite has a RFI vulnerability." A
  browser-side `<img src>` load is not server-side execution — the lane's cheapest
  misread. Record it; quote the report URL, teach the distinction.
