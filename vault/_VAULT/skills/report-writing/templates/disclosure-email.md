# Responsible Disclosure Email — Hall of Fame / Informational / No-Impact

Use when: the target has a published disclosure policy (see `security.txt` at
`/.well-known/security.txt` or a /security page) and your findings are LOW / INFO
or NOT a reportable vulnerability per their program rules, but you want to be a good
citizen and request HoF credit. This is an EMAIL, not a HackerOne/Bugcrowd submission.

## Tone rules
- Professional and good-faith. Triagers/security teams are people; be concise.
- State RoE compliance explicitly (passive, read-only, no patient/user data, no DoS).
- Do NOT overclaim. Mirror the "never say could potentially" rule from the main
  skill, but soften for courtesy disclosures: say "informational / low severity,
  no demonstrated exploit" rather than asserting impact you didn't prove.
- Request credit under your handle (e.g. the operator's handle from USER.md).

## Structure
```
Subject: Responsible Disclosure — <finding class> | <target>   [or HoF request]
To: security@<target>            (from security.txt Contact: line)

1. One-line intro: researcher, program reference, passive scope, RoE compliance.
2. Summary of findings (numbered). For each: what was found, where, why it matters, honest severity.
3. Impact — honest LOW/INFO. No demonstrated exploit.
4. Remediation suggestions (1–3 bullets, concrete).
5. Scope note — passive, read-only, no patient data, consistent with RoE/HIPAA.
6. Credit — request HoF acknowledgment under handle <X>. Offer to clarify / send evidence.
```

## Starter template (copy + modify)

```
Subject: Responsible Disclosure — Informational findings (client-side identifier &
API-surface exposure) | <TARGET>

To the <Target> Security Team,

I am a security researcher participating in your responsible disclosure program
(per <policy-url> and your published scope). I performed passive, non-intrusive
reconnaissance against your in-scope assets and identified a few informational /
low-severity items I wanted to share in good faith. No authentication was performed,
no user/patient data was accessed, and no testing was done against production systems
— fully within your rules of engagement.

== Summary of findings ==

1) Internal <auth-vendor> identifiers exposed in production client bundle
   <host>/assets/<bundle>.js embeds internal identifiers that aid attacker
   reconnaissance:
     - clientId: <value>            (public by design)
     - <vendor>-tenant-id: <uuid>   (INTERNAL — finding)
     - <vendor>-user-id:  <uuid>    (INTERNAL — finding)
   These also reveal your full <auth> API surface (e.g. /impersonation/v1,
   /api-tokens/*, /sso/callback), helping an attacker map exactly which auth flows
   and admin functions exist.

2) Demo credential pair hardcoded in production bundle
     clientId: "<CLIENT_ID_...>"
     secret:   "<SECRET_...>"
   Marked "preview only" in code. Even if non-functional, shipping demo secrets in
   production client code is poor practice.

3) Undocumented in-scope subdomains / API hosts
   Your scope page lists only <listed>. The bundles reference additional reachable
   hosts: <subdomain1>, <subdomain2>. I did not test these (out of documented scope +
   no account) — suggest adding them to the public scope or confirming coverage.

== Impact ==
Low. Informational disclosures — no demonstrated exploit, account takeover, or data
access. They primarily reduce attacker reconnaissance effort.

== Remediation suggestions ==
  - Remove internal <vendor> IDs and the demo token object from production client
    bundles (or move to server-side / non-shipped config).
  - Add the additional API subdomains to your published scope, or document they are
    out of scope.

== Scope note ==
All activity was passive and read-only. I did not attempt authentication, brute force,
DoS, or any interaction with user/patient data, consistent with your commitments.

== Credit ==
Per your policy, I would appreciate public acknowledgment under the handle "<X>" once
remediated. If you need clarification or additional evidence, please let me know.

Best regards,
<X> (security researcher)
```

## Notes
- This email is NOT a vulnerability report — don't force a CVSS score onto INFO findings.
- If you later get an authorized account and turn an INFO into a real vuln, write a
  proper platform report using the H1/Bugcrowd/Intigriti templates in this skill.
- Keep a local copy of the exact bundle references + line contexts as evidence.
