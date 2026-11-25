# APK secret patterns — concrete categories & verification

From real assessments (tv.abema v10.179.0). apkleaks catches most; manual grep
catches context. Verify before reporting — a redacted `«redacted:AIza…»` in
apktool strings.xml means the VALUE is elsewhere (aapt --values / grep AIza).

## Categories found (apkleaks section → meaning)
- [Google_API_Key]        AIza[0-9A-Za-z_-]{35}  → test live; Maps loader serves
                          ALL (key-or-no-key) so NOT proof. Only real API calls
                          prove usability. API-restricted keys → REQUEST_DENIED/403.
- [Facebook_Secret_Key]   FACEBOOK_SIGNATURE = 30820268...  → DER RSA PRIVATE KEY.
                          Hardcoded social SDK secret → CWE-798 Medium/High.
- [Twitter_Secret_Key]    twitter.android / twitter.android.beta = 3082025d... /
                          30820352...  → DER RSA PRIVATE KEY (Twitter Kit consumer
                          secret). Same severity class as Facebook.
- [Twitter_ClientID]      same 3082... blob (apkleaks labels it twice).
- [Generic_API_Key]       brazeApiKey = [REDACTED_SECRET] (Braze
                          SDK key — meant to ship, but still disclose).
- [Firebase]              <app>.firebaseio.com  → probe /.json + storage; deactivated(423)
                          or list-disallowed = SAFE, not a finding.
- [Google_Cloud_Platform_OAuth]  <num>-<hash>.apps.googleusercontent.com
                          (project number leak — info only).
- [Authorization_Basic]    empty in abema — confirm not a real cred.
- [IP_Address]            bare IPs (2.10.9.0 / 2.9.0.0) → internal/test endpoints,
                          attack-surface aid (INFO).

## DER private-key verification (proves the blob is a real RSA key)
The apkleaks prefix like `3082025d308201c6a00302010202044bd76cce...` is DER:
  30 82 02 5d   = SEQUENCE, length 0x25d (whole key)
  30 82 01 c6   = SEQUENCE (inner, length 0x1c6)
  02 01 02      = INTEGER 2  (RSA version)  ← starts at offset 8, NOT 7
Quick check:
```python
raw = bytes.fromhex(hexblob)
ok = raw[0]==0x30 and raw[4]==0x30 and raw[8]==0x02   # RSA private key structure
```
(Offset 7 is wrong because the inner SEQUENCE length is 3 bytes: 82 01 c6.)

## Triage rule
- Real PRIVATE key / consumer secret in binary → report (CWE-798). Highest value.
- Public key (BEGIN PUBLIC KEY) in assets → safe, not a finding.
- API key that returns DENIED on data calls → Low (info-leak of project id only).
- Firebase deactivated / storage list-denied → not vulnerable, note as verified-safe.

## Cross-engagement pivot (real example)
The GCP project number embedded in `default_web_client_id` (e.g. `135673081971-...`)
matched a Google Maps API key reviewed in a SEPARATE engagement (LINE WORKS).
Same project spans both apps → use the project number as a pivot to find related
keys/assets across targets. Always record the numeric project id, not just the key.

## Real backend hosts enumerated (attack-surface aid, INFO)
auth.abema.tv, api.twitter.com, gateway.p-c2-x.abema-tv.com,
dev-streaming-api-cf.d-c2-x.abema-tv.com, upload.abema.io,
zeus-api.d-c3-e.abema-tv.com, admob-gmats.uc.r.appspot.com, Braze SSE/iAM cache.
Bare IPs (2.10.9.0 / 2.9.0.0) = likely internal/test endpoints — useful for
scoping the dynamic phase, low direct risk.

## Third-party scope note
Confirm program scope before submitting hardcoded-secret findings on third-party
apps (Abema TV = Japanese third-party). The shared GCP project 135673081971 appeared
in both the LINE WORKS session key check and this APK — a reminder that one key can
recur across unrelated engagements.
