# Proving an info-disclosure finding is NOT a data breach

Companion to `scripts/pii_audit.py`. Read this before answering any variant of
*"is there user data leaked in this?"* — especially when the finding is an
unauthenticated read of a large, structured dataset.

---

## Why this exists

An unauthenticated endpoint returning 167 records *looks* like a breach. It
usually isn't. The difference between a Medium 5.3 info-disclosure and a
Critical PII leak is **what is actually in the records**, and that is a
question you answer with an audit, not with an impression.

The trap runs both ways:

- **Overclaiming** — "unauth API returns data ⇒ user data leaked." Triage kills
  it, and a killed report costs credibility on the next one.
- **Underclaiming** — "it's just reference data, probably fine" without
  checking. If personal fields *were* present, you just talked yourself out of a
  Critical.

Both are avoided by resolving every regex hit and checking JSON **field names**.

---

## The audit, in order

### 1. Regex-scan for PII shapes

`email`, `phone`, `passport_no`, `civil_id`, `iban`, Arabic name runs, and
PII-named JSON fields. See `PII_PATTERNS` in the script.

### 2. RESOLVE every hit — this is the actual work

A regex match is a *question*, not an answer. Print ±200 chars of context and
identify what the value is. Real resolution table from a Java-portal assessment:

| Hit | What it actually was |
|---|---|
| `1005007009` | Liferay CMS **articleId** in a help-widget URL — a content-page ID, identical for every visitor |
| `130602337` | **Google Analytics** property ID — `gtag/js?id=UA-130602337-1` |
| `16070400` | **HSTS header value** — `max-age=16070400` (seconds, 186 days) |
| `148500557500`, `178747493400` | **Epoch-ms timestamps** — 1974-09-15, 1975-08-31 = Liferay 6.1.1 build dates |
| `18414964` | constant inside the framework's own `engine.js` |
| `26298821` | the **tester's own** test account userId |
| `P1234567`, `12345678`, `+96899999999`, `000000000` | **placeholders written into the tester's own scripts** |
| `[REDACTED_EMAIL]`, `+968 22848200` | **public contact details printed in the site footer** |
| `العربية`, `أيام`, `الأسبوع` | Arabic **UI/nav labels**, not names |

Ten of ten resolved benign. Note the last two rows: an email that matches the
email regex is not a leak if it is the company's published support address, and
Arabic text is not a person if it is the word "Tuesday."

**Sanity-check timestamps:** epoch-ms values land in 1970-2020. If a 12-digit
number resolves to a plausible date, it is a timestamp, not an identifier.
`datetime.fromtimestamp(n/1000)` settles it in one line.

**Filter your own test data.** Every engagement artifact contains the tester's
placeholders and their own account IDs. Pass `--own-marker` so they don't
pollute the result.

### 3. Structured check — field names, not values

Value-level regex can miss personal data whose format you didn't anticipate.
Field-level inspection cannot:

```
visa_categories.json: 167 records
  fields: arabicName, desc, englishName, period, sponsored,
          stayType, visaSubtypeId, visaTypeId, visaTypeName
  personal-data fields: NONE
  -> reference/config data only
```

Nine fields, zero personal. That single block is what makes the Medium rating
defensible and what a triager will accept.

---

## How this changes the finding

| Audit result | Report as |
|---|---|
| No personal fields; reference/config data only | **Medium 5.3**, `CWE-306`/`CWE-200`, `C:L` — "reference data disclosed + full method surface exposed" |
| Personal fields present, but only your own test rows | Still Medium — say so explicitly, do not inflate |
| Personal fields present with real third-party rows | **Critical**, but you must not have got there by enumeration — see below |

---

## The boundary this audit does NOT cross

Proving *absence* of PII in reference data is safe and necessary.

Proving *presence* of PII by reading real users' records is **not** an audit —
it is data theft, and a report built on it gets rejected. The correct proof of
an IDOR is **two accounts you control**: account A requests account B's record,
one captured request/response pair. "A can read B" is the finding; "here are
everyone's passports" is the incident.

If the audit shows the reference-data endpoint is clean, the PII question
belongs to a *different* endpoint (the one keyed on a user-controlled ID), and
it gets answered with the two-account method.

---

## Attaching the audit to the report

A PII-audit block strengthens an info-disclosure submission — it shows you
checked rather than assumed:

```markdown
## Data exposure assessment

The endpoint returns N records. Field-level audit of the full response:

| Field | Personal? |
|---|---|
| visaTypeId, visaSubtypeId | no — catalogue IDs |
| englishName, arabicName | no — product names |
| sponsored, stayType, period | no — business attributes |

**No applicant names, passport numbers, civil IDs, emails or application
records are present.** This is reference/configuration data of the same kind
published on the public "Types of Visa" page, returned here in structured form
with internal identifiers.

Audit reproducible with `scripts/pii_audit.py <artifacts-dir>`.
```

That paragraph is the difference between a Medium that gets accepted and a
Critical that gets closed as N/A.
