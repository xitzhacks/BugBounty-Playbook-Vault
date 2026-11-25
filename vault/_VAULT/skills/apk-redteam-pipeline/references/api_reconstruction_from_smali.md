# API Reconstruction From Smali — Concrete Walkthrough (LINE WORKS, 2026-08)

Target APK: `com.gworks.oneapp.works` v4.6.1.11 (XAPK, 271MB; base apk 171MB).
Skill context: Stage 4.7 of apk-redteam-pipeline.

## The decoy
Recon `live_hosts.txt` listed `cxtalk-service.line-works.com` (Cloudflare, HTTP 400 on `/`).
Blind fuzzing of `/`, `/api`, `/api/v1`, `/v1`, `/health`, `/docs`, `/swagger.json`,
`/api/health` ALL returned `400` with body `Invalid Path`. That uniform error across every path
is the decoy signal — it is NOT the live API.

## The real endpoint (reconstructed from DEX)
1. Retrofit interface `HomeCXTalkApi.smali`:
   ```
   .annotation runtime Lx50/f;
       value = "home/widget/023/small"
   .end annotation
   ```
   => relative path `home/widget/023/small`. Sibling found: `home/widget/021/small`
   (HomeSchedulerApi) — sequential widget ID space.

2. Builder `yn/c.smali` method `b` (Dagger @Provides for HomeCXTalkApi):
   ```
   sget-object p1, Lcom/gworks/config/url/AliceServerUrl;->DEFAULT:Lcom/gworks/config/url/AliceServerUrl;
   invoke-virtual {p1}, ...->f()Ljava/lang/String;        # base URL
   invoke-virtual {p0, p1}, ...->f(Ljava/lang/String;)    # append "webhomegw"
   ```
   => full path = <AliceServerUrl.DEFAULT> + `/webhomegw` + `/home/widget/023/small`.

3. Base-URL builder `com/gworks/config/url/AliceServerUrl$c.smali`:
   ```
   const-string v0, "https://alice."
   ... append <baseDomain>            # prod
   const-string v0, "https://alpha-alice."   # alpha
   const-string v0, "https://stage-alice."   # stage
   ```
   => prod base host = `https://alice.<baseDomain>/webhomegw`.

4. Per-tenant resolution: `<baseDomain>` is the logged-in tenant's domain (dynamic, from auth
   config). `alice.line-works.com` has NO public DNS A record. The real request only fires for a
   tenant whose domain is `<baseDomain>` — confirmed by `dig +short alice.line-works.com` = empty.

## Second backend (same pattern)
`com/gworks/config/url/CSTalkServerUrl$a.smali` builds `"https://cxtalk." + baseDomain` (prod),
`"https://alpha-cxtalk."`, `"https://stage-cxtalk."`. Separate "CS Talk" channel/bot backend;
endpoint paths not extracted here — grep smali for `@GET/@POST` in
`com/navercloud/**/cxtalk/**` + `CSTalk*` to enumerate.

## Why this matters for the hunt
- The "real" API is per-tenant and auth-gated → it is the DYNAMIC lane, not the web lane.
- The sequential widget IDs (001..~023+) are a textbook BOLA/IDOR surface once you have a
  captured session: swap tenant context (2 own accounts) and check if a widget returns another
  tenant's data.
- The app permits MITM (no pinning + user-CA trust) → Frida/mitmproxy capture yields the real
  `alice.<tenant>/webhomegw/...` requests + auth headers with zero cert errors.

## Reproduce
```bash
APK=android/work_linework/extracted/com.gworks.oneapp.works.apk
DEC=android/work_linework/dec/apktool
# 1. relative paths
grep -rn 'value = "home/widget' "$DEC"
# 2. which builder appends the base
grep -rln 'AliceServerUrl;->DEFAULT' "$DEC"
# 3. base host string
grep -rn 'const-string v0, "https://alice\."' "$DEC"
```
