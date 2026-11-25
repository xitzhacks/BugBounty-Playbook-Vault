# Case Study: ROP eVisa DWR Enumeration (October 2026)

**Target:** https://evisa.rop.gov.om  
**Stack:** Liferay Portal 6.1.1 CE front-end + `/eVisaSponsoredUnsponsored/` Java webapp (DWR)  
**WAF:** F5 BIG-IP ASM (cookie `TS01f3da37`)  
**Finding:** Unauthenticated DWR interface exposure (Medium 5.3)

---

## 1. Fingerprint

```
curl -skI https://evisa.rop.gov.om/ | grep -i 'set-cookie'
# Set-Cookie: jvmRouteeVisaNode1=1037110527; ...   <-- Java servlet LB route

# WAF presence:
TS01f3da37: 12345678
```

---

## 2. DWR Surface Map

**Methods enumerated (115 total):**

| Interface | Methods | Unauth result |
|-----------|---------|---------------|
| sponsoredapplyDwr | 18 | `getAllVisaTypes` → 167 visa subrecords |
| sponsoredDwr | 55 | `preArrivalMedicalStatus` → empty string |
| dwrService | 42 | `getOccupation`, `getDMSServiceStatus`, various `validationFor*` → status codes |

14 methods are `delete*`/`send*` (documented, NOT executed). 53 now WAF-blocked.

---

## 3. Key Code Pattern — ScriptSessionId

```python
# The server accepts ANY UUID as scriptSessionId on first call.
# After volume, WAF blocks it.
dwr.scriptSessionId = str(uuid.uuid4())
```

If calls start returning "Request Rejected", rotate the UUID and warm the session.

---

## 4. cN Index Pitfall (learned)

The `.js` stubs named parameters `p0..pN` but those **omit indices** for server-excluded params:
```
dwr_sponsoredDwr.js:
p.deleteDocument = function(p0, p2, callback)
```
My `dwr5.py` broke by using Java param numbers → `Failed to find parameter: c2-id`.  
FIX: Use **positional wire** (c1, c2, c3 for N args) regardless of param names.

---

## 5. PII Audit Result

The unauthenticated DWR calls returned **zero PII**:

```
visa_categories.json: 167 records
  fields: arabicName, desc, englishName, period, sponsored,
          stayType, visaSubtypeId, visaTypeId, visaTypeName
  personal-data fields: NONE
```

The timestamp-like numbers in the WAF-blocked response body? Liferay build epoch-ms:
```
148500557500 → 1974-09-15  → Liferay 6.1.1 build date
```

---

## 6. Vehicle Categories Discovered

```
12A–12I  Truck Driver Visa (ME7D, ME30D, JOR, TUR, YEM, SETUR, ME7DJOR)
18A      Sailor's Transit Visa
32A–32C  Cruise Ship Passenger Visa
```

Each includes validity period and sponsorship model — competitive intelligence.

---

## 7. WAF Behavior Observed

- GETs remained open throughout (200 OK, full content).  
- POSTs to `getAllVisaTypes` succeeded, then later returned "Request Rejected" (247-byte block).  
- POSTs to validation methods also blocked after saturation.  
- **Conclusion:** signature + rate, not a permanent fix.

---

## 8. The "deleteDocument returns true" Pattern

`sponsoredDwr.deleteDocument(2) → true` is not necessarily a confirmed write bug. Common outcomes:
1. "Nothing to delete" path returns `true` for non-existent document-id.  
2. Silent delete with no side effect observable without auth.

Report as: _"mutate method `deleteDocument` accepts no auth check in front of it (CWE-306) — verify backend authorisation flows"_.

---

## 9. Reference

- `scripts/dwr_client.py` — full working client  
- `scripts/pii_audit.py` — audit pipeline  
- `references/pii-vs-breach-triage.md` — PII audit methodology  
- `FINDING-01-unauthenticated-dwr-exposure.md` — full report