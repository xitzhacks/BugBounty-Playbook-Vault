---
name: direct-vuln-reporting
description: "Direct vulnerability reporting format - findings only, no verbose explanations. Use when user requests 'find bugs' or 'give me findings' without asking for detailed writeups."
tags: ["bug-bounty", "reporting", "workflow"]
---

# Direct Vulnerability Reporting

When users ask for findings directly ("find bugs", "give me X", "do one thing"), use this minimalist format:

## BUG #N: [Vulnerability] at [Endpoint]
```
Severity: [High/Medium/Low]
Finding: [1 sentence - what it is]
PoC: [exact payload or request]
Impact: [what attacker gains]
CWE: [CWE-XXX]
```

## Key Rules
- NO paragraphs explaining "what I found"
- NO "initial recon showed..." 
- NO multiple examples unless asked
- Just the essentials: what, where, how, impact
- Save detailed reporting for when user explicitly asks

## Example Format

**BUG #1: Information Disclosure via robots.txt**
```
Severity: Medium
Finding: Publicly accessible robots.txt discloses protected admin paths /console, /api/, etc.
PoC: curl http://target/robots.txt → "Disallow: /console /api/"
Impact: Attackers discover hidden admin functionality
CWE: CWE-538
```

**BUG #2: Insecure Password Recovery**
```
Severity: High
Finding: /api/auth/recover accepts arbitrary handle with no validation
PoC: POST {"handle":"admin' OR '1'='1"} → {"relayed":true}
Impact: User enumeration, potential account takeover
CWE: CWE-204, CWE-89
```

## When NOT to use this format
- User asks for "detailed report" or "writeup"
- User asks for "explain this finding"
- User explicitly requests CVSS scores
- User wants remediation recommendations

In those cases, fall through to `triage-validation` → `report-writing`.